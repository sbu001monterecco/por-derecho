import fs from 'node:fs';
import path from 'node:path';

const playwright = await import(process.env.PSR_PLAYWRIGHT_PATH || 'playwright');
const { chromium } = playwright;

const base=(process.env.PSR_BASE_URL||'http://127.0.0.1:8000/por-derecho').replace(/\/$/,'');
const out=process.env.PSR_SCREENSHOT_DIR||'artifacts/unitary-public-shell';
const browserPath=(process.env.PSR_BROWSER_PATH||'').trim()||undefined;
fs.mkdirSync(out,{recursive:true});

const routes=[
  {name:'home-en',url:'/en/',kind:'home'},
  {name:'home-es',url:'/es/',kind:'home'},
  {name:'control-en',url:'/en/case-control-room/',kind:'control'},
  {name:'control-es',url:'/es/sala-control-caso/',kind:'control'},
  {name:'search-en',url:'/en/search/',kind:'search'},
  {name:'search-es',url:'/es/buscar/',kind:'search'},
  {name:'authority-register-en',url:'/en/red-sara-age-filings-authority-responses/',kind:'authority-register'},
  {name:'authority-register-es',url:'/es/registros-redsara-age-y-respuestas-autoridades/',kind:'authority-register'},
  {name:'dp1901-en',url:'/en/dp-1901-2026/',kind:'gateway'},
  {name:'dp1041-en',url:'/en/litigious-credit-retracto-1041-2017/',kind:'existing'},
  {name:'dp1041-es',url:'/es/retracto-credito-litigioso-1041-2017/',kind:'existing'},
  {name:'cuatrecasas-en',url:'/en/cuatrecasas-sun-park/',kind:'existing'},
  {name:'cuatrecasas-icam-en',url:'/en/cuatrecasas-icam-ccacm-2026/',kind:'existing'},
  {name:'cuatrecasas-icam-es',url:'/es/cuatrecasas-icam-ccacm-2026/',kind:'existing'},
  {name:'governance-tracks-en',url:'/en/community-instrumentalisation/two-competing-governance-records/',kind:'existing'},
  {name:'governance-tracks-es',url:'/es/comunidad-instrumentalizacion/dos-registros-gobernanza-competidores/',kind:'existing'},
  {name:'ac-en',url:'/en/insolvency-36-2012-insolvency-administrator/',kind:'existing'},
  {name:'ac-autos-en',url:'/en/insolvency-36-2012-orders-decisions/',kind:'ac-autos',section:'#unitary-analysis',marker:'What this thread proves'},
  {name:'ac-autos-es',url:'/es/concurso-36-2012-autos-resoluciones/',kind:'ac-autos',section:'#analisis-unitario',marker:'Qué prueba este hilo'},
  {name:'ac-thread-en',url:'/en/unitary-criminal-hypothesis-2011-present/',kind:'ac-thread',section:'#ac-removal-fees-thread',marker:'A notice-and-contradiction record'},
  {name:'ac-thread-es',url:'/es/hipotesis-criminal-unitaria-2011-presente/',kind:'ac-thread',section:'#hilo-separacion-honorarios-ac',marker:'Registro de aviso y contradicción'},
  {name:'ricpe-en',url:'/en/ric-private-equity-sun-park/',kind:'existing'},
  {name:'map-es',url:'/es/mapa-forense-sun-park-262-fincas/',kind:'existing'}
];
const viewports=[{name:'desktop',width:1440,height:1000},{name:'mobile',width:390,height:844}];
const failures=[];const evidence=[];
const browser=await chromium.launch({headless:true,...(browserPath?{executablePath:browserPath}:{})});

async function assertSearch(page,query,pattern,label){
  const input=page.locator('#psr-search-input');
  await input.fill(query);
  await page.waitForFunction(({patternSource,patternFlags})=>{
    const re=new RegExp(patternSource,patternFlags);
    return [...document.querySelectorAll('.psr-search-result h2')].some(el=>re.test(el.textContent||''));
  },{patternSource:pattern.source,patternFlags:pattern.flags},{timeout:15000});
  const titles=await page.locator('.psr-search-result h2').allTextContents();
  if(!titles.some(t=>pattern.test(t)))throw new Error(`${label} search failed for ${query}`);
}

async function assertAuthorityRegister(page){
  const input=page.locator('#pd-acr-search');
  await input.waitFor({state:'visible',timeout:15000});
  await input.fill('184368/2026');
  await page.waitForFunction(()=>document.querySelectorAll('.pd-acr-event').length===1,null,{timeout:15000});
  const first=page.locator('.pd-acr-event').first();
  if(await first.getAttribute('id')!=='communication-PD-SP-EVT-0141')throw new Error('Authority register does not resolve 184368/2026 to PD-SP-EVT-0141');
  const firstText=(await first.textContent())||'';
  if(!/Intervenci.n General/i.test(firstText))throw new Error('Authority register omits the Intervención General office');
  await input.fill('Intervención General');
  await page.waitForFunction(()=>document.querySelectorAll('.pd-acr-event').length>=3,null,{timeout:15000});
  const text=await page.locator('.pd-acr-event').allTextContents();
  for(const reference of ['184368/2026','497011/2026','699645/2026'])if(!text.some(value=>value.includes(reference)))throw new Error(`Authority register missing Intervención response ${reference}`);
}

try{
  for(const viewport of viewports){
    const context=await browser.newContext({viewport:{width:viewport.width,height:viewport.height}});
    for(const route of routes){
      const page=await context.newPage();
      const url=`${base}${route.url}`;
      try{
        const response=await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
        if(!response||response.status()>=400)throw new Error(`HTTP ${response?.status()}`);
        await page.waitForFunction(()=>document.documentElement.dataset.psrUnitaryShellVersion==='20260901a',null,{timeout:15000});
        if(route.kind==='home'){
          const progressiveRecord=page.locator('[data-audience-full-record] > details');
          if(await progressiveRecord.count())await progressiveRecord.evaluate(node=>{node.open=true;});
          await page.waitForSelector('.main-nav[data-psr-consolidated-nav="true"]',{state:'attached',timeout:10000});
          await page.waitForSelector('.psr-home-control-gateway',{timeout:10000});
        }
        if(route.kind==='control'){
          await page.waitForSelector('[data-case-control-room]',{timeout:10000});
          const cards=await page.locator('.psr-system-card').count();
          if(cards!==6)throw new Error(`Expected exactly six system cards, found ${cards}`);
          const hrefs=await page.locator('a').evaluateAll(els=>els.map(el=>el.getAttribute('href')||''));
          if(!hrefs.some(h=>/1041-2017/.test(h)))throw new Error('Control Room missing DP1041/retracto bridge');
          for(const needle of ['cuatrecasas-sun-park','cuatrecasas-icam-ccacm-2026'])if(!hrefs.some(h=>h.includes(needle)))throw new Error(`Control Room missing ${needle} bridge`);
        }
        if(route.kind==='search'){
          await assertSearch(page,'CEXP',/CEXP|Community|Comunidad|LPB/i,'CEXP');
          await assertSearch(page,'1041',/1041|retracto|litigious/i,'DP1041');
          await assertSearch(page,'Cuatrecasas',/Cuatrecasas/i,'Cuatrecasas');
          await assertSearch(page,'184368/2026',/184368\/2026/i,'Intervención General reference');
          if(await page.locator('.psr-search-result').count()!==1)throw new Error('Exact Intervención reference must not fall through to generic 2026 matches');
          await assertSearch(page,'Intervención General',/Intervenci.n General/i,'Intervención General office');
          const governanceQuery=route.url.includes('/es/')?'hipotesis de captura':'capture hypothesis';
          await assertSearch(page,governanceQuery,/Governance|Gobernanza/i,'governance visual');
          await assertSearch(page,'pwc canarias carlos saavedra',/Pwc|PwC.*Canarias|Carlos Saavedra/i,'specialist-sitemap fallback');
        }
        if(route.kind==='authority-register')await assertAuthorityRegister(page);
        if(route.kind==='existing'||route.kind==='gateway')await page.waitForSelector('.psr-utility-nav',{timeout:15000});
        if(route.kind==='ac-autos'||route.kind==='ac-thread'){
          const section=page.locator(route.section);
          await section.waitFor({state:'attached',timeout:15000});
          const sectionText=(await section.textContent())||'';
          if(!sectionText.includes(route.marker))throw new Error(`Missing controlled AC-thread marker: ${route.marker}`);
          if(!sectionText.includes('110,956.97')&&!sectionText.includes('110.956,97'))throw new Error('Missing pleaded-total boundary');
          if(!sectionText.includes('13 of 14')&&!sectionText.includes('13 de 14'))throw new Error('Missing CAEPR denominator');
          if(!sectionText.includes('^'))throw new Error('Missing caret-identity legend');
          if(route.kind==='ac-autos'){
            for(const id of ['R01','R09','R30','F01','F13','F17']){
              if(await page.locator(`#${id}`).count()!==1)throw new Error(`Missing controlled full-text anchor #${id}`);
            }
          }
        }
        const metrics=await page.evaluate(()=>{
          const ids=[...document.querySelectorAll('[id]')].map(el=>el.id).filter(Boolean);
          const duplicates=[...new Set(ids.filter((id,i)=>ids.indexOf(id)!==i))];
          const viewportWidth=document.documentElement.clientWidth;
          const isClipped=(el)=>{
            let p=el.parentElement;
            while(p&&p!==document.body){
              const style=getComputedStyle(p);
              const ox=style.overflowX;
              if(['auto','scroll','hidden','clip'].includes(ox)){
                const r=p.getBoundingClientRect();
                if(r.left>=-3&&r.right<=viewportWidth+3)return true;
              }
              p=p.parentElement;
            }
            return false;
          };
          const offenders=[...document.querySelectorAll('body *')].filter(el=>{
            const r=el.getBoundingClientRect();
            return (r.right>viewportWidth+3||r.left<-3)&&!isClipped(el);
          }).map(el=>{
            const r=el.getBoundingClientRect();
            const style=getComputedStyle(el);
            return {tag:el.tagName.toLowerCase(),id:el.id||'',className:typeof el.className==='string'?el.className.slice(0,120):'',left:Math.round(r.left),right:Math.round(r.right),width:Math.round(r.width),scrollWidth:el.scrollWidth||0,overflowX:style.overflowX,position:style.position};
          }).sort((a,b)=>Math.max(b.right-viewportWidth,-b.left)-Math.max(a.right-viewportWidth,-a.left)).slice(0,12);
          return {scrollWidth:document.documentElement.scrollWidth,bodyScrollWidth:document.body.scrollWidth,clientWidth:viewportWidth,duplicates,h1:document.querySelectorAll('h1').length,offenders};
        });
        if(metrics.scrollWidth>metrics.clientWidth+3)throw new Error(`Horizontal overflow ${metrics.scrollWidth} > ${metrics.clientWidth}; ${JSON.stringify(metrics.offenders)}`);
        if((route.kind==='control'||route.kind==='search'||route.kind==='gateway'||route.kind==='ac-autos'||route.kind==='ac-thread')&&metrics.duplicates.length)throw new Error(`Duplicate IDs: ${metrics.duplicates.join(', ')}`);
        if(metrics.h1<1)throw new Error('Missing H1');
        const shot=path.join(out,`${route.name}-${viewport.name}.png`);
        await page.screenshot({path:shot,fullPage:true});
        evidence.push({route:route.url,viewport:viewport.name,status:'pass',metrics,screenshot:shot});
      }catch(error){
        try{await page.screenshot({path:path.join(out,`${route.name}-${viewport.name}-failure.png`),fullPage:true});}catch{}
        failures.push({route:route.url,viewport:viewport.name,error:String(error)});
      }finally{await page.close();}
    }
    await context.close();
  }
}finally{await browser.close();}
fs.writeFileSync(path.join(out,'result.json'),JSON.stringify({base,browser_path:browserPath||'playwright-managed',checked_at:new Date().toISOString(),evidence,failures},null,2));
if(failures.length){console.error(JSON.stringify(failures,null,2));process.exit(1);}else console.log(`Unitary public shell checks passed: ${evidence.length}; curated + specialist-sitemap discovery verified; all tested routes overflow-free`);

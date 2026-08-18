import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const base=(process.env.PSR_BASE_URL||'http://127.0.0.1:8000/por-derecho').replace(/\/$/,'');
const out=process.env.PSR_SCREENSHOT_DIR||'artifacts/unitary-public-shell';
fs.mkdirSync(out,{recursive:true});

const routes=[
  {name:'home-en',url:'/en/',kind:'home'},
  {name:'home-es',url:'/es/',kind:'home'},
  {name:'control-en',url:'/en/case-control-room/',kind:'control'},
  {name:'control-es',url:'/es/sala-control-caso/',kind:'control'},
  {name:'search-en',url:'/en/search/',kind:'search'},
  {name:'search-es',url:'/es/buscar/',kind:'search'},
  {name:'dp1901-en',url:'/en/dp-1901-2026/',kind:'gateway'},
  {name:'ac-en',url:'/en/insolvency-36-2012-insolvency-administrator/',kind:'existing'},
  {name:'ricpe-en',url:'/en/ric-private-equity-sun-park/',kind:'existing'},
  {name:'map-es',url:'/es/mapa-forense-sun-park-262-fincas/',kind:'existing'}
];
const viewports=[{name:'desktop',width:1440,height:1000},{name:'mobile',width:390,height:844}];
const failures=[];const warnings=[];const evidence=[];
const browser=await chromium.launch({headless:true});
try{
  for(const viewport of viewports){
    const context=await browser.newContext({viewport:{width:viewport.width,height:viewport.height}});
    for(const route of routes){
      const page=await context.newPage();
      const url=`${base}${route.url}`;
      try{
        const response=await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
        if(!response||response.status()>=400)throw new Error(`HTTP ${response?.status()}`);
        await page.waitForFunction(()=>document.documentElement.dataset.psrUnitaryShellVersion==='20260818b',null,{timeout:15000});
        if(route.kind==='home'){
          await page.waitForSelector('.main-nav[data-psr-consolidated-nav="true"]',{state:'attached',timeout:10000});
          await page.waitForSelector('.psr-home-control-gateway',{timeout:10000});
        }
        if(route.kind==='control'){
          await page.waitForSelector('[data-case-control-room]',{timeout:10000});
          const cards=await page.locator('.psr-system-card').count();
          if(cards<6)throw new Error(`Expected six system cards, found ${cards}`);
        }
        if(route.kind==='search'){
          const input=page.locator('#psr-search-input');await input.fill('CEXP');
          await page.waitForFunction(()=>document.querySelectorAll('.psr-search-result').length>0,null,{timeout:15000});
          const titles=await page.locator('.psr-search-result h2').allTextContents();
          if(!titles.some(t=>/CEXP|Community|Comunidad|LPB/i.test(t)))throw new Error('CEXP search did not surface a controlled relevant result');
        }
        if(route.kind==='existing'||route.kind==='gateway')await page.waitForSelector('.psr-utility-nav',{timeout:15000});
        const metrics=await page.evaluate(()=>{
          const ids=[...document.querySelectorAll('[id]')].map(el=>el.id).filter(Boolean);
          const duplicates=[...new Set(ids.filter((id,i)=>ids.indexOf(id)!==i))];
          const viewportWidth=document.documentElement.clientWidth;
          const offenders=[...document.querySelectorAll('body *')].map(el=>{
            const r=el.getBoundingClientRect();
            return {tag:el.tagName.toLowerCase(),id:el.id||'',className:typeof el.className==='string'?el.className.slice(0,120):'',left:Math.round(r.left),right:Math.round(r.right),width:Math.round(r.width),scrollWidth:el.scrollWidth||0};
          }).filter(x=>x.right>viewportWidth+3||x.left<-3).sort((a,b)=>Math.max(b.right-viewportWidth,-b.left)-Math.max(a.right-viewportWidth,-a.left)).slice(0,8);
          return {scrollWidth:document.documentElement.scrollWidth,clientWidth:viewportWidth,duplicates,h1:document.querySelectorAll('h1').length,offenders};
        });
        const overflow=metrics.scrollWidth>metrics.clientWidth+3;
        if(overflow&&route.kind==='existing'){
          const warning={route:route.url,viewport:viewport.name,message:`Inherited horizontal overflow ${metrics.scrollWidth} > ${metrics.clientWidth}`,offenders:metrics.offenders};
          warnings.push(warning);console.warn(JSON.stringify(warning));
        }else if(overflow){throw new Error(`Horizontal overflow ${metrics.scrollWidth} > ${metrics.clientWidth}; ${JSON.stringify(metrics.offenders)}`);}
        if((route.kind==='control'||route.kind==='search'||route.kind==='gateway')&&metrics.duplicates.length)throw new Error(`Duplicate IDs: ${metrics.duplicates.join(', ')}`);
        if(metrics.h1<1)throw new Error('Missing H1');
        const shot=path.join(out,`${route.name}-${viewport.name}.png`);
        await page.screenshot({path:shot,fullPage:true});
        evidence.push({route:route.url,viewport:viewport.name,status:'pass',metrics,screenshot:shot});
      }catch(error){failures.push({route:route.url,viewport:viewport.name,error:String(error)});}
      finally{await page.close();}
    }
    await context.close();
  }
}finally{await browser.close();}
fs.writeFileSync(path.join(out,'result.json'),JSON.stringify({base,checked_at:new Date().toISOString(),evidence,warnings,failures},null,2));
if(failures.length){console.error(JSON.stringify(failures,null,2));process.exit(1);}else console.log(`Unitary public shell checks passed: ${evidence.length}; inherited warnings: ${warnings.length}`);

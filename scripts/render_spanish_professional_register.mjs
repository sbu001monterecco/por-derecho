import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
const base=(process.env.PD_SPR_BASE_URL||'http://127.0.0.1:8000/por-derecho').replace(/\/$/,'');
const out=process.env.PD_SPR_SCREENSHOT_DIR||'artifacts/spanish-professional-register-20260825';
await fs.mkdir(out,{recursive:true});
const cases=[
 {lang:'es',route:'/es/registro-identidad-materia/abogados-espanoles/',title:'Abogados españoles, asesores y participantes de la materia.',current:'Javier Sixto-Seijas',former:'Mónica Lasquibar Rodríguez'},
 {lang:'en',route:'/en/matter-identity-registry/spanish-lawyers/',title:'Spanish lawyers, advisers and matter participants.',current:'Javier Sixto-Seijas',former:'Mónica Lasquibar Rodríguez'}
];
const views=[{name:'desktop',width:1440,height:1050},{name:'mobile',width:390,height:844}];
const browser=await chromium.launch({headless:true});let failed=false;const metrics=[];
try{
 for(const item of cases)for(const view of views){
  const ctx=await browser.newContext({viewport:view});const page=await ctx.newPage();const errors=[];
  page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});page.on('pageerror',e=>errors.push(e.message));
  const url=base+item.route;const response=await page.goto(url,{waitUntil:'networkidle',timeout:90000});if(!response||!response.ok())throw new Error(`${url}: HTTP ${response?.status()}`);
  await page.waitForFunction(()=>{const s=document.querySelector('[data-spr-status]');return s&&!/Cargando|Loading|could not|No se pudo/i.test(s.textContent||'')},{timeout:30000});
  const h=await page.locator('h1').first().textContent();if(!h?.includes(item.title))throw new Error(`${url}: title mismatch`);
  const total=Number(await page.locator('[data-spr-stat="TOTAL"]').textContent());if(total<65)throw new Error(`${url}: classified total unexpectedly low: ${total}`);
  const cards=await page.locator('[data-spr-grid] .spr-card').count();if(cards!==total)throw new Error(`${url}: cards ${cards} != total ${total}`);
  await page.locator('[data-spr-filter="CURRENT_SPANISH_COUNSEL"]').click();const currentText=await page.locator('[data-spr-grid]').textContent();
  for(const name of ['Javier Sixto-Seijas','Estefanía Sixto Seijas','Carlos Llamas Sanz','Adriana Hernández Díaz'])if(!currentText.includes(name))throw new Error(`${url}: missing current counsel ${name}`);
  await page.locator('[data-spr-filter="FORMER_SPANISH_COUNSEL"]').click();const formerText=await page.locator('[data-spr-grid]').textContent();
  for(const name of ['Miguel Méndez Itarte','Mónica Lasquibar Rodríguez','Pablo Villaseca Rico','Cristo Ayose Suárez Pimentel','Manuel Gallego Águeda'])if(!formerText.includes(name))throw new Error(`${url}: missing former counsel ${name}`);
  await page.locator('[data-spr-filter="HISTORICAL_OWNER_COMMUNITY_PARTICIPANT"]').click();const ownerText=await page.locator('[data-spr-grid]').textContent();
  for(const name of ['Sebastián Molina Petit','Celia Guillén Pérez','Manuel Molina Climent','Daniel Van der Horst'])if(!ownerText.includes(name))throw new Error(`${url}: missing owner ${name}`);
  await page.locator('[data-spr-filter="ALL"]').click();await page.locator('[data-spr-search]').fill('PD-SP-P-0075');if(await page.locator('[data-spr-grid] .spr-card').count()!==1)throw new Error(`${url}: ID search failed`);
  const searched=await page.locator('[data-spr-grid]').textContent();if(!searched.includes('Gerardo Zacarías Acosta Matos'))throw new Error(`${url}: searched identity not rendered`);
  await page.locator('[data-spr-search]').fill('');
  const proposalText=await page.locator('[data-spr-review-body]').textContent();if(!proposalText.includes('Cases & Lacambra')||!proposalText.includes('ONTIER'))throw new Error(`${url}: proposal-only boundary missing`);
  const pageText=await page.locator('body').textContent();if(pageText.includes('Josep Ponsirenas')||pageText.includes('Oriol Huguet'))throw new Error(`${url}: transaction-only contacts leaked`);
  const screenshot=path.join(out,`${item.lang}-${view.name}.png`);await page.screenshot({path:screenshot,fullPage:true});const width=await page.evaluate(()=>document.body.scrollWidth);
  if(view.name==='mobile'&&width>view.width+20)throw new Error(`${url}: mobile overflow ${width}`);if(errors.length)throw new Error(`${url}: console errors ${errors.join(' | ')}`);
  metrics.push({lang:item.lang,view:view.name,total,cards,screenshot});await ctx.close();
 }
}catch(error){failed=true;console.error(error)}finally{await browser.close();await fs.writeFile(path.join(out,'metrics.json'),JSON.stringify(metrics,null,2))}
if(failed)process.exit(1);console.log(`Spanish professional register rendered successfully: ${metrics.length} cases`);
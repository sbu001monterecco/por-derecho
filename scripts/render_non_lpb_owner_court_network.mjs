import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';

const base=(process.env.PD_OCN_BASE_URL||'http://127.0.0.1:8000/por-derecho').replace(/\/$/,'');
const out=process.env.PD_OCN_SCREENSHOT_DIR||'artifacts/non-lpb-owner-court-network-20260826';
await fs.mkdir(out,{recursive:true});
const cases=[
  {lang:'es',route:'/es/registro-identidad-materia/perimetro-propietarios-no-lpb-matkator/',title:'Propiedad, parte procesal, representación y continuidad: cuatro preguntas distintas.',core:'Los siete actores propietarios confirmados por AP 89/2014.'},
  {lang:'en',route:'/en/matter-identity-registry/non-lpb-matkator-owner-network/',title:'Ownership, procedural-party status, representation and continuity are four different questions.',core:'The seven actors who owned the claimant apartments identified by AP 89/2014.'}
];
const views=[{name:'desktop',width:1440,height:1050},{name:'mobile',width:390,height:844}];
const requiredClaimants=['Acciones Canarias, S.L.','Muruga, S.L.','Roque Prieto, S.L.','Amenem, S.L.','Tengolf, S.L.','Miguel Molina Betancor','Francisco Luis Molina Molina'];
const requiredIndividuals=['Celia Guillén Pérez','Manuel Molina Climent','José Daniel Acosta Matos','Laura Patricia Acosta Matos','Gerardo Zacarías Acosta Matos','Javier Acosta Matos'];
const forbidden=['Josep Ponsirenas','Oriol Huguet','José Miguel Molina Petit','Anastasio Molina López','Lourdes Moreno'];
const browser=await chromium.launch({headless:true});let failed=false;const metrics=[];
try{
 for(const item of cases)for(const view of views){
  const context=await browser.newContext({viewport:view});const page=await context.newPage();const errors=[];
  page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});page.on('pageerror',e=>errors.push(e.message));
  const url=base+item.route;const response=await page.goto(url,{waitUntil:'networkidle',timeout:90000});if(!response||!response.ok())throw new Error(`${url}: HTTP ${response?.status()}`);
  const heading=await page.locator('h1').textContent();if(!heading?.includes(item.title))throw new Error(`${url}: heading mismatch`);
  const text=await page.locator('body').textContent();if(!text?.includes(item.core))throw new Error(`${url}: exact AP89 core heading missing`);
  for(const name of [...requiredClaimants,...requiredIndividuals])if(!text.includes(name))throw new Error(`${url}: missing ${name}`);
  for(const name of forbidden)if(text.includes(name))throw new Error(`${url}: prohibited name leaked: ${name}`);
  const stats=await page.locator('.ocn-stat strong').allTextContents();if(stats.join('|')!=='7|18|7|31|6')throw new Error(`${url}: stat denominator mismatch ${stats.join('|')}`);
  const familyCards=await page.locator('.ocn-card.family').count();if(familyCards!==4)throw new Error(`${url}: expected four Acosta Matos family/business cards, found ${familyCards}`);
  const adverse=await page.locator('.ocn-note').textContent();if(!/desalojo|eviction/i.test(adverse||''))throw new Error(`${url}: adverse AP89 result missing`);
  const networkJson=await page.locator('a[href*="non-lpb-matkator-owner-court-network-v1.json"]').count();if(networkJson<1)throw new Error(`${url}: canonical JSON link missing`);
  const screenshot=path.join(out,`${item.lang}-${view.name}.png`);await page.screenshot({path:screenshot,fullPage:true});
  const width=await page.evaluate(()=>document.body.scrollWidth);if(view.name==='mobile'&&width>view.width+20)throw new Error(`${url}: mobile overflow ${width}`);
  if(errors.length)throw new Error(`${url}: console errors ${errors.join(' | ')}`);
  metrics.push({lang:item.lang,view:view.name,url,stats,familyCards,screenshot});await context.close();
 }
}catch(error){failed=true;console.error(error)}finally{await browser.close();await fs.writeFile(path.join(out,'metrics.json'),JSON.stringify(metrics,null,2))}
if(failed)process.exit(1);console.log(`Owner/court-party network rendered successfully: ${metrics.length} cases`);
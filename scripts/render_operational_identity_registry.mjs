import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';

const baseURL = (process.env.PD_ID_BASE_URL || 'http://127.0.0.1:8000/por-derecho').replace(/\/$/, '');
const outputDir = process.env.PD_ID_SCREENSHOT_DIR || 'artifacts/operational-identity-registry-20260825';
const expectedTotal = 188;
await fs.mkdir(outputDir, { recursive: true });

const cases = [
  {language:'es',route:'/es/registro-identidad-materia/',loading:/Cargando|No se pudo/i,expectedTitle:'Una identidad. Un ID. Una cadena operativa.',targetName:'Francisco de Borja Rodríguez-Batllori Laffitte'},
  {language:'en',route:'/en/matter-identity-registry/',loading:/Loading|could not be loaded/i,expectedTitle:'One identity. One ID. One operational chain.',targetName:'Francisco de Borja Rodríguez-Batllori Laffitte'}
];
const viewports = [{name:'desktop',width:1440,height:1080},{name:'mobile',width:390,height:844}];
const browser = await chromium.launch({headless:true});
const metrics=[]; let failed=false;
try {
  for (const testCase of cases) for (const viewport of viewports) {
    const context=await browser.newContext({viewport}); const page=await context.newPage(); const consoleErrors=[];
    page.on('console',m=>{if(m.type()==='error') consoleErrors.push(m.text());}); page.on('pageerror',e=>consoleErrors.push(e.message));
    const url=`${baseURL}${testCase.route}`; const response=await page.goto(url,{waitUntil:'networkidle',timeout:90000});
    if(!response||!response.ok()) throw new Error(`${url} returned ${response?.status()}`);
    await page.waitForSelector('[data-registry-status]',{timeout:30000});
    await page.waitForFunction(({source,flags})=>{const n=document.querySelector('[data-registry-status]');return n && !(new RegExp(source,flags)).test(n.textContent||'');},{source:testCase.loading.source,flags:testCase.loading.flags},{timeout:30000});
    const heading=await page.locator('h1').first().textContent(); if(!heading?.includes(testCase.expectedTitle)) throw new Error(`${url}: missing expected heading`);
    const total=Number(await page.locator('[data-registry-stat="TOTAL"]').first().textContent()); if(total!==expectedTotal) throw new Error(`${url}: expected ${expectedTotal} identities, found ${total}`);
    const initialRows=await page.locator('tbody[data-registry-body] tr[data-identity-id]').count(); if(initialRows!==expectedTotal) throw new Error(`${url}: expected ${expectedTotal} rendered rows, found ${initialRows}`);
    const queueCounts={}; for(const queue of ['p0','unresolved','no-route','distinction']){const value=Number(await page.locator(`[data-queue-count="${queue}"]`).textContent());if(!(value>0))throw new Error(`${url}: ${queue} queue is empty`);queueCounts[queue]=value;}
    if(queueCounts.unresolved<14) throw new Error(`${url}: unresolved queue unexpectedly fell below the controlled baseline`);
    await page.locator('[data-operational-filter="UNRESOLVED"]').click(); const unresolvedRows=await page.locator('tbody[data-registry-body] tr[data-identity-id]').count();
    if(unresolvedRows!==queueCounts.unresolved) throw new Error(`${url}: unresolved filter rendered ${unresolvedRows}, queue reports ${queueCounts.unresolved}`);
    await page.locator('[data-operational-filter="P0"]').click(); const p0Rows=await page.locator('tbody[data-registry-body] tr[data-identity-id]').count(); if(!(p0Rows>0)) throw new Error(`${url}: P0 filter rendered no identities`);
    await page.locator('[data-operational-filter="ALL"]').click(); const search=page.locator('[data-registry-search]'); await search.fill('PD-SP-P-0010');
    const targetRows=await page.locator('tbody[data-registry-body] tr[data-identity-id]').count(); if(targetRows!==1) throw new Error(`${url}: ID search expected one result, found ${targetRows}`);
    await page.locator('tbody[data-registry-body] .id-name-button').click(); const dialog=page.locator('[data-identity-dialog]'); await dialog.waitFor({state:'visible',timeout:10000});
    const dialogText=await dialog.textContent(); if(!dialogText?.includes(testCase.targetName)||!dialogText.includes('PD-SP-ACT-0003')) throw new Error(`${url}: identity dialog lacks target name or action reference`);
    await dialog.locator('.id-dialog-close').click(); await search.fill('');
    await page.waitForFunction(()=>document.querySelector('tr[data-identity-id="PD-SP-P-0060"] .id-name-button strong')?.textContent?.includes('Javier Sixto-Seijas'),null,{timeout:15000});
    const withdrawnVisible=await page.locator('tr[data-identity-id="PD-SP-P-0065"]:visible, tr[data-identity-id="PD-SP-P-0066"]:visible').count(); if(withdrawnVisible!==0) throw new Error(`${url}: transaction-only records remain visible`);
    const screenshot=path.join(outputDir,`${testCase.language}-${viewport.name}.png`); await page.screenshot({path:screenshot,fullPage:true});
    const bodyWidth=await page.evaluate(()=>document.body.scrollWidth); if(bodyWidth>viewport.width+20&&viewport.name==='mobile') throw new Error(`${url}: mobile body overflows (${bodyWidth}px at ${viewport.width}px viewport)`);
    if(consoleErrors.length) throw new Error(`${url}: console/page errors: ${consoleErrors.join(' | ')}`);
    metrics.push({language:testCase.language,viewport:viewport.name,url,total,initialRows,unresolvedRows,p0Rows,queueCounts,screenshot,consoleErrors}); await context.close();
  }
} catch(error){failed=true;console.error(error);} finally {await browser.close();await fs.writeFile(path.join(outputDir,'metrics.json'),JSON.stringify(metrics,null,2));}
if(failed)process.exit(1); console.log(`Operational identity registry rendered successfully: ${metrics.length} cases`);
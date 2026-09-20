import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const base=(process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho').replace(/\/$/,'')+'/';
const output=process.env.PSR_NEXUS_SCREENSHOT_DIR || 'artifacts/dp1901-platform-nexus';
fs.mkdirSync(output,{recursive:true});
const data=JSON.parse(fs.readFileSync('assets/data/dp1901-platform-recovery-nexus-20260920.json','utf8'));
const routes=data.nodes.flatMap(n=>Object.values(n.routes).map(route=>({route,central:false})));
routes.push(...Object.values(data.central_routes).map(route=>({route,central:true})));
const browser=await chromium.launch({headless:true});
const results=[];
try {
  for (const width of [1280,390]) {
    const context=await browser.newContext({viewport:{width,height:900}});
    await context.route('**/*',route=>route.request().url().startsWith(base) || route.request().url().startsWith('data:') ? route.continue() : route.abort());
    for (const item of routes) {
      const page=await context.newPage();
      const record={route:item.route,width,central:item.central};
      const missing=[];
      page.on('response',r=>{if(r.url().includes('dp1901-platform-recovery-nexus-20260920') && r.status()>=400) missing.push(r.url());});
      try {
        const response=await page.goto(base+item.route,{waitUntil:'domcontentloaded',timeout:30000});
        assert.equal(response.status(),200);
        await page.waitForFunction(()=>document.documentElement.dataset.pd1901Nexus==='ready',null,{timeout:20000});
        assert.equal(missing.length,0);
        if(item.central){
          assert.equal(await page.locator('[data-dp1901-nexus-index] li').count(),21);
          await page.screenshot({path:path.join(output,`central-${item.route.slice(0,2)}-${width}.png`),fullPage:true});
        }else{
          const block=page.locator('#pd1901-platform-nexus');
          assert.equal(await block.count(),1);
          assert.ok(await block.locator('nav a').count()>=3);
          const rect=await block.boundingBox();assert.ok(rect.width<=width+1,JSON.stringify({rect,width}));
          assert.equal(await page.locator('main').count(),1);
          if(item.route.endsWith('/dp-1901-2026/') || item.route.includes('presidencia-'))
            await block.screenshot({path:path.join(output,`context-${item.route.replaceAll('/','_')}-${width}.png`)});
        }
        record.status='PASS';
      }catch(error){record.status='FAIL';record.error=String(error).slice(0,600);}
      results.push(record);await page.close();
    }
    await context.close();
  }
} finally {await browser.close();}
const report={control_id:data.control_id,source_sha:process.env.GITHUB_SHA || null,status:results.every(r=>r.status==='PASS')?'PASS':'FAIL',cases:results.length,passed:results.filter(r=>r.status==='PASS').length,routes:routes.length,results,scope:'Route-scoped module and central reader DOM/layout; exact checked-out source. Existing page legal merits and outside source authenticity are not tested.'};
fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({status:report.status,cases:report.cases,passed:report.passed,routes:report.routes}));
if(report.status!=='PASS')process.exitCode=1;

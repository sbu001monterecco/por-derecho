#!/usr/bin/env python3
"""Read-only visual/route safeguards on the prepared source; no private source intake."""
import asyncio,json,os,re
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path.cwd();OUT=Path(os.getenv('PD_AUDIT_OUT','/tmp/caixabank-candidate'));BASE=os.getenv('PD_AUDIT_BASE','http://127.0.0.1:8899/por-derecho/')
async def run():
 source=(ROOT/'assets/home-mission-critical-20260904.js').read_text()
 assert 'const isHome = /^' in source,'Home route must be anchored at the start'
 out=[]
 async with async_playwright() as p:
  for engine in ['chromium','firefox','webkit']:
   browser=await getattr(p,engine).launch();ctx=await browser.new_context(viewport={'width':390,'height':900})
   for route in ['es/','en/','es/reclamacion-caixabank-valencia/','en/caixabank-valencia-claim/']:
    page=await ctx.new_page();await page.goto(BASE+route,wait_until='domcontentloaded');await page.wait_for_timeout(3500)
    ishome=route in ['es/','en/'];n=await page.locator('[data-pd-home-mission="20260904"]').count()
    assert n==(1 if ishome else 0),(engine,route,'homepage module count',n)
    row={'engine':engine,'route':route,'home_module_count':n}
    if not ishome:
     metrics=await page.locator('#caixabank-lectura-inicial .button').evaluate_all("""els=>els.map(e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return {text:e.innerText,color:s.color,background:s.backgroundColor,height:r.height}})""")
     assert metrics and all(m['color']=='rgb(19, 37, 45)' and m['background']=='rgb(255, 255, 255)' and m['height']>=44 for m in metrics),(engine,metrics)
     row['quick_read_buttons']=metrics
     await page.locator('#caixabank-lectura-inicial').screenshot(path=str(OUT/(engine+'-'+route.replace('/','_')+'quick-review.png')))
    out.append(row);await page.close()
   await browser.close()
 OUT.mkdir(exist_ok=True,parents=True);(OUT/'final-reader-review.json').write_text(json.dumps({'passed':True,'checks':out},indent=2));print('FINAL_READER_REVIEW_PASS',len(out))
if __name__=='__main__':asyncio.run(run())

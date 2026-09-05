#!/usr/bin/env python3
"""Read-only checks of actual controls, not source-path existence alone."""
import json,subprocess,time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

def main():
 d=json.loads((ROOT/'ops/AUDITED_WEBSITE_REPAIRS_20260905.json').read_text())
 routes=[r['path'] for r in d['modified_html'] if any(e['kind']=='DOCUMENTARY_FALLBACK' for e in r['edits'])]
 assert len(routes)==2
 server=subprocess.Popen(['python','-m','http.server','8767','--bind','127.0.0.1','--directory',str(ROOT.parent)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 checks=0;report=[];out=ROOT/'diagnostics/audited-browser';out.mkdir(parents=True,exist_ok=True)
 try:
  time.sleep(1)
  with sync_playwright() as p:
   b=p.chromium.launch()
   for js in [True,False]:
    for width in [390,1440]:
     context=b.new_context(java_script_enabled=js,viewport={'width':width,'height':1000})
     page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
     for route in routes:
      response=page.goto('http://127.0.0.1:8767/por-derecho/'+route.removesuffix('index.html'),wait_until='networkidle')
      assert response.status==200;checks+=1
      assert page.locator('[data-audit-edge]').count()==d['graph_counts']['edges'];checks+=1
      if js:
       page.wait_for_selector('[data-graph-state="ready"]',timeout=15000)
       assert page.locator('[data-node-id]').count()==d['graph_counts']['nodes'];checks+=1
       assert page.locator('.fc-evidence-row').count()==d['graph_counts']['edges'];checks+=1
       page.locator('#fc-grade').select_option(index=1)
       assert 0<page.locator('.fc-evidence-row').count()<=d['graph_counts']['edges'];checks+=1
       page.locator('#fc-reset').click()
       assert page.locator('.fc-evidence-row').count()==d['graph_counts']['edges'];checks+=1
       page.locator('[data-node-id]').first.focus();page.keyboard.press('Enter')
       assert page.locator('#fc-detail h3').count()==1;checks+=1
       page.locator('#fc-search').fill('NON_EXISTENT_AUDIT_QUERY_0293')
       assert page.locator('.fc-evidence-row').count()==0;checks+=1
       page.locator('#fc-reset').click()
       assert page.locator('.fc-evidence-row').count()==d['graph_counts']['edges'];checks+=1
       assert not errors,'JavaScript error: '+repr(errors);checks+=1
      page.locator('[data-audit-edge] summary').first.click()
      assert page.locator('[data-audit-edge]').first.get_attribute('open') is not None;checks+=1
      overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth+2') if js else None
      page.screenshot(path=str(out/(route.split('/')[0]+'-'+str(width)+'-'+str(js)+'.png')))
      report.append({'route':route,'width':width,'javascript':js,'page_overflow':overflow,'result':'PASS'})
     context.close()
   b.close()
 finally:server.terminate()
 result={'checks':checks,'cases':report,'source_nodes':d['graph_counts']['nodes'],'source_edges':d['graph_counts']['edges']}
 (out/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
 assert not any(r['page_overflow'] for r in report),'Mobile/document overflow needs scoped repair'
 print('GRAPH_BROWSER_PASS',checks)

if __name__=='__main__':main()

#!/usr/bin/env python3
"""Read-only, finite-source and two-language desktop/mobile validation.
Exports reviewed files and receipts, never writes the repository or main.
"""
from __future__ import annotations
import csv
import hashlib
import http.server
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import threading
import urllib.parse
import urllib.request
import fitz
from playwright.sync_api import sync_playwright

ROOT = Path.cwd()
OUT = Path('/tmp/alzada4-reviewed-export')
BASE = 'e642b160bdbd60e2e6137edc86bbf2e34870f1c5'
OUT.mkdir(parents=True,exist_ok=True)
PLAN = json.loads(Path('governance/continuity/2026-10-13-alzada4-publication-plan.json').read_text())
CONTROL = Path('assets/data/eg17-20-26-alzada-continuity-20260924.json')
report = {'control_id':PLAN['control_id'],'candidate_sha':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'tests':[],'limits':['Scope-specific verification only; not legal merits, native signature verification or production RAG certification.']}


def require(ok, label):
    report['tests'].append({'test':label,'pass':bool(ok)})
    if not ok:raise AssertionError(label)


def old(path):
    return subprocess.check_output(['git','show',BASE+':'+path])


def csv_rows(raw):
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8'))))


def run():
    source=PLAN['source']
    for path,h,n in [(source['public_pdf_path'],source['public_pdf_sha256'],source['public_pdf_bytes']),(source['public_raster_path'],source['public_raster_sha256'],source['public_raster_bytes'])]:
        raw=Path(path).read_bytes()
        require(len(raw)==n and hashlib.sha256(raw).hexdigest()==h,'exact source '+path)
    pdf=fitz.open(source['public_pdf_path'])
    require(len(pdf)==5,'PDF has all five pages')
    require(pdf.embfile_count()==0,'No embedded files in public facsimile')
    for i,page in enumerate(pdf):
        require(len(page.get_images())==1,'Source image present on page '+str(i+1))
        page.get_pixmap(matrix=fitz.Matrix(.7,.7),alpha=False).save(OUT/f'pdf-page-{i+1}.png')
    current=json.loads(CONTROL.read_text())
    require(current['control_id']==PLAN['control_id'],'existing control identity unchanged')
    require(current['latest_decision']['outcome']=='DISMISSED','adverse outcome retained')
    require(current['filed_appeal']['presented_at_local']=='2026-09-24T20:46:23','unverified UTC offset not asserted')
    before=csv_rows(old('archive/PROCEEDINGS_MASTER_REGISTER.csv'))
    after=csv_rows(Path('archive/PROCEEDINGS_MASTER_REGISTER.csv').read_bytes())
    require(len(before)==len(after),'master row count unchanged')
    a=[r for r in before if r['Master_ID']!='GC-LAJ-021'];b=[r for r in after if r['Master_ID']!='GC-LAJ-021']
    require(a==b,'all other master rows unchanged')
    target=[r for r in after if r['Master_ID']=='GC-LAJ-021']
    require(len(target)==1 and 'dismissed' in target[0]['Status'],'one existing parent updated')
    readback=json.loads(Path('governance/continuity/2026-10-13-alzada4-projection-receipt.json').read_text())
    require(all(n==1 for n in readback['projection_matches'].values()),'one unambiguous record in each derived projection')
    for path in ['archive/THREAD_DELETION_CONTINUITY_AUDIT_EG17_20_26_ALZADA_24SEP2026.md','docs/continuity/2026-09-24-eg17-20-26-alzada.md','archive/SUN_PARK_COMUNIDAD_PROCEEDINGS_REGISTER_CANARY_ISLANDS_15AUG2026.md']:
        require(Path(path).read_bytes().startswith(old(path)),'historical Markdown preserved '+path)
    # Inspect the existing communications schema without fabricating a new master.
    registry=Path('assets/data/institutional-communications-register-v1.json')
    if registry.exists():
        obj=json.loads(registry.read_text())
        diag={'bytes':registry.stat().st_size,'top_level_type':type(obj).__name__,'keys':list(obj) if isinstance(obj,dict) else None}
        if isinstance(obj,dict):
            diag['lists']={k:len(v) for k,v in obj.items() if isinstance(v,list)}
            for k,v in obj.items():
                if isinstance(v,list) and v and isinstance(v[0],dict):
                    diag['first_record_keys']={k:list(v[0])}
                    diag['first_record_example']=v[0]
                    break
        ids=re.findall(r'PD-SP-EVT-\d+',registry.read_text())
        diag['highest_event_ids']=sorted(set(ids))[-12:]
        (OUT/'communications-schema-readback.json').write_text(json.dumps(diag,ensure_ascii=False,indent=2)+'\n')
    # Serve under the real /por-derecho/ project prefix, not merely at URL root.
    serve=Path('/tmp/alzada4-reader-server');serve.mkdir(exist_ok=True)
    link=serve/'por-derecho'
    if not link.exists():link.symlink_to(ROOT,target_is_directory=True)
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(serve),**kwargs)
        def log_message(self,*args):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}/por-derecho/'
    report['browser_checks']=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch()
            for lang in ('es','en'):
                for size in ({'width':1440,'height':1000},{'width':390,'height':844}):
                    context=browser.new_context(viewport=size)
                    page=context.new_page()
                    response=page.goto(base+lang+'/alzada-4-2026/',wait_until='networkidle')
                    require(response.status==200,f'{lang} reader HTTP200 {size["width"]}')
                    require(page.locator('figure.paper').count()==5,f'{lang} has five page figures')
                    require(page.locator('object[type="application/pdf"]').count()==1,f'{lang} has real PDF object')
                    body=page.locator('body').inner_text()
                    for actor in PLAN['private_actors']:require(actor in body,f'{lang} visible named core: {actor}')
                    require(page.locator('#actions tbody tr').count()==8,f'{lang} eight action states')
                    require(page.evaluate('document.documentElement.scrollWidth <= innerWidth + 2'),f'{lang} no horizontal page overflow {size["width"]}')
                    for i in range(1,6):
                        figure=page.locator('#page-'+str(i));figure.scroll_into_view_if_needed()
                        image=figure.locator('img');image.wait_for(state='visible')
                        page.wait_for_function('(i)=>{const x=document.querySelector("#page-"+i+" img");return x.complete&&x.naturalWidth===1191&&x.naturalHeight===8420}',arg=i)
                    page.locator('#position').scroll_into_view_if_needed()
                    page.screenshot(path=str(OUT/f'{lang}-{size["width"]}-position.png'))
                    page.locator('#page-4').screenshot(path=str(OUT/f'{lang}-{size["width"]}-page4.png'))
                    object_url=page.locator('object').get_attribute('data').split('#')[0]
                    response=context.request.get(urllib.parse.urljoin(page.url,object_url))
                    require(response.status==200 and hashlib.sha256(response.body()).hexdigest()==source['public_pdf_sha256'],f'{lang} PDF transport/hash from browser context')
                    local_links=page.locator('a[href]').evaluate_all('(xs)=>xs.map(x=>x.href)')
                    for url in sorted(set(local_links)):
                        if url.startswith(base):
                            r=context.request.get(url.split('#')[0]);require(r.status==200,f'{lang} local source/context link '+url.replace(base,''))
                    report['browser_checks'].append({'language':lang,'viewport':size,'five_images_loaded':True,'pdf_response_hash':source['public_pdf_sha256'],'pdf_plugin_rendering':'wrapper+PDF-byte/parser+five-image fallback verified; native PDF plug-in interaction not separately certified'})
                    context.close()
            browser.close()
    finally:server.shutdown()
    paths={PLAN['source']['public_pdf_path'],PLAN['source']['public_raster_path'],str(CONTROL),'assets/alzada4-viewer.css','governance/continuity/2026-10-13-alzada4-publication-plan.json','governance/continuity/2026-10-13-alzada4-projection-receipt.json','evidence/public/2026-10-13-alzada4/admission-receipt.json','es/alzada-4-2026/index.html','en/alzada-4-2026/index.html'}
    for name in paths:
        dst=OUT/'repository'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(name,dst)
    report['export_manifest']=[{'path':x,'bytes':Path(x).stat().st_size,'sha256':hashlib.sha256(Path(x).read_bytes()).hexdigest()} for x in sorted(paths)]
    report['status']='PASS_FINITE_SOURCE_AND_LOCAL_BROWSER_SCOPE'


try:
    run()
except Exception as exc:
    report['status']='FAILED';report['error']=str(exc)
    raise
finally:
    (OUT/'validation-receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':report.get('status'),'candidate_sha':report['candidate_sha'],'tests':len(report['tests']),'errors':report.get('error')},indent=2))

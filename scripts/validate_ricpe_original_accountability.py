#!/usr/bin/env python3
"""Read-only source, privacy, browser and exact public-byte acceptance for this release."""
from __future__ import annotations
import argparse
import functools
import hashlib
import http.server
import json
import re
import subprocess
import tempfile
import threading
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from ricpe_original_publication_policy import PATH, HASH, AUTH, authorised_original

ROOT = Path(__file__).resolve().parents[1]
OUT = Path('/tmp/ricpe-accountability')
OUT.mkdir(exist_ok=True)
DATA = 'assets/data/ricpe-original-accountability-20260905.json'
checks = []
def require(condition, label):
    checks.append({'check':label,'passed':bool(condition)})
    if not condition:
        (OUT/'scoped-failure.json').write_text(json.dumps(checks,indent=2))
        raise AssertionError(label)

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls=[]; self.ids=[]; self.frames=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if tag in ('a','link') and a.get('href'): self.urls.append(a['href'])
        if tag=='iframe': self.frames.append(a)

def local_target(page, href):
    parsed=urllib.parse.urlsplit(href)
    if parsed.scheme or parsed.netloc: return None
    path=urllib.parse.unquote(parsed.path)
    if not path: return ROOT/page
    if path.startswith('/por-derecho/'): target=ROOT/path.removeprefix('/por-derecho/')
    elif path.startswith('/'): target=ROOT/path.lstrip('/')
    else: target=(ROOT/page).parent/path
    target=target.resolve()
    if path.endswith('/') or target.is_dir(): target=target/'index.html'
    return target

def source_checks():
    data=json.loads((ROOT/DATA).read_text())
    native=(ROOT/PATH).read_bytes()
    require(authorised_original(ROOT,PATH,native),'Exact authorised native PDF path, size, digest and authority')
    require(native.startswith(b'%PDF-'),'Native file has PDF signature')
    info=subprocess.check_output(['pdfinfo',str(ROOT/PATH)],text=True)
    require(bool(re.search(r'Pages:\s+6\b',info)),'Native PDF decodes as six pages')
    require(not authorised_original(ROOT,'other.pdf',native),'Reject same native bytes at another path')
    require(not authorised_original(ROOT,PATH,native+b'changed'),'Reject modified native bytes')
    with tempfile.TemporaryDirectory() as tmp:
        sandbox=Path(tmp)
        require(not authorised_original(sandbox,PATH,native),'Reject missing authority')
        p=sandbox/AUTH;p.parent.mkdir(parents=True);auth=json.loads((ROOT/AUTH).read_text());auth['unaltered_original']=False;p.write_text(json.dumps(auth))
        require(not authorised_original(sandbox,PATH,native),'Reject incompatible authority')
    require(len(data['routes'])==8,'Eight bilingual entry-route pairs')
    require(len(data['native_history'])==9,'Nine separate native history occurrences')
    require(len({e['occurrence'] for e in data['native_history']})==9,'Unique source-occurrence aliases')
    require('not newly allocated global' in data['registration_boundary'],'No false global-event admission claim')
    for lang in ('es','en'):
        page=data['analysis'][lang];text=(ROOT/page).read_text();parser=Links();parser.feed(text)
        require(f'<html lang="{lang}">' in text,lang+' language declared')
        require(len(parser.ids)==len(set(parser.ids)),lang+' unique anchors')
        for anchor in ('original','secuencia','interes-publico','incumplimiento','ocultacion','control','rutas'):
            require(anchor in parser.ids,lang+' analysis anchor '+anchor)
        require(len(parser.frames)==1 and PATH in parser.frames[0]['src'],lang+' static native PDF iframe')
        for marker in ('35.2.a','Ithikios','PD-SP-EVT-0175','PD-SP-EVT-0177/0178','No mostrado al denunciante',HASH):
            require(marker in text,lang+' material source/legal qualification '+marker)
        for href in parser.urls:
            target=local_target(page,href)
            if target is not None: require(target.exists(),page+' local link '+href)
        for entry in data['routes']:
            path=entry[lang]+'index.html'
            require((ROOT/path).is_file(),'Existing entry route '+path)
            require(entry[lang] in (ROOT/'assets/ricpe-original-accountability-20260905.js').read_text(),'Runtime allowlist '+entry[lang])
            require(entry['context_'+lang].strip(),'Context for '+entry[lang])
    loader=(ROOT/'assets/site.js').read_text()
    require(loader.count("load('ricpe-original-accountability-20260905.js'")==1,'One new loader')
    base=subprocess.check_output(['git','show',data['source_main']+':assets/site.js'],text=True,cwd=ROOT)
    for call in re.findall(r"load\('[^\n]+",base): require(call in loader,'Preserved inherited loader: '+call)
    subprocess.run(['node','--check',str(ROOT/'assets/ricpe-original-accountability-20260905.js')],check=True)
    subprocess.run(['python3',str(ROOT/'scripts/validate_ricpe_channel_identifier_privacy.py')],check=True)
    return data

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

def browser_checks(data, live):
    from playwright.sync_api import sync_playwright
    server=None;thread=None;temp=None
    if live:
        base='https://sbu001monterecco.github.io/por-derecho/'
    else:
        temp=tempfile.TemporaryDirectory();(Path(temp.name)/'por-derecho').symlink_to(ROOT,target_is_directory=True)
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=temp.name))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        base=f'http://127.0.0.1:{server.server_port}/por-derecho/'
    routes=[r[lang] for r in data['routes'] for lang in ('es','en')]+[data['evidence_reader']]
    static=list(data['analysis'].values())
    screenshots=OUT/'screenshots';screenshots.mkdir(exist_ok=True)
    reports=[]
    try:
        with urllib.request.urlopen(base+PATH,timeout=45) as response:
            served=response.read();content_type=response.headers.get('Content-Type','')
        require(hashlib.sha256(served).hexdigest()==HASH,'Served PDF exact native bytes')
        require('pdf' in content_type.lower(),'Served PDF MIME type')
        with sync_playwright() as p:
            browser=p.chromium.launch()
            for width in (390,1280):
                context=browser.new_context(viewport={'width':width,'height':900})
                for route in routes+static:
                    page=context.new_page();response=page.goto(base+route,wait_until='domcontentloaded',timeout=60000)
                    require(response is not None and response.status==200,'HTTP200 '+route)
                    is_static=route in static
                    selector='#ricpe-channel-analysis' if is_static else '#ricpe-original-accountability'
                    page.locator(selector).wait_for(state='visible',timeout=45000)
                    require(page.locator(selector).count()==1,'Single reader/panel '+route)
                    frame=page.locator(selector+' iframe')
                    require(frame.count()==1 and PATH in frame.get_attribute('src'),'Native iframe target '+route)
                    if not is_static:
                        page.locator(selector+' details').evaluate('(el)=>el.open=true')
                        require(page.locator(selector+' a').filter(has_text=re.compile('Análisis crítico|Full critical')).count()==1,'Full analysis link '+route)
                        page.add_script_tag(url=base+'assets/ricpe-original-accountability-20260905.js')
                        require(page.locator(selector).count()==1,'Idempotent remount '+route)
                    if is_static:
                        require(page.locator('body').inner_text().find('35.2.a')>=0,'Protection qualification visible '+route)
                        require(page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),'No static-reader horizontal overflow '+route)
                    if route in ('es/ric-private-equity-sun-park/','en/ric-private-equity-sun-park/'):
                        require(page.locator('[data-ricpe-historical-status]').count()==1,'Stale front status corrected '+route)
                    if route in static or route in ('es/ric-private-equity-sun-park/','en/ricpe-perimeter-shareholders-media/'):
                        page.screenshot(path=str(screenshots/(str(width)+'-'+route.replace('/','_')+'.png')),full_page=False,animations='disabled')
                    reports.append({'route':route,'width':width,'browser':'chromium','javascript':True,'passed':True})
                    page.close()
                context.close()
            # Complete static analysis and PDF links remain accessible without JavaScript.
            for kind in ('chromium','firefox'):
                engine=p.chromium if kind=='chromium' else p.firefox
                other=engine.launch();context=other.new_context(java_script_enabled=False,viewport={'width':390,'height':900})
                for route in static:
                    page=context.new_page();page.goto(base+route,wait_until='domcontentloaded')
                    require(page.locator('#control').count()==1 and page.locator('iframe').count()==1,'No-JS complete reader '+kind+' '+route)
                    require('35.2.a' in page.locator('body').inner_text(),'No-JS legal qualification '+kind+' '+route)
                    reports.append({'route':route,'width':390,'browser':kind,'javascript':False,'passed':True});page.close()
                context.close();other.close()
            context=browser.new_context();page=context.new_page();page.goto(base+'en/puzzle/',wait_until='domcontentloaded');page.add_script_tag(url=base+'assets/ricpe-original-accountability-20260905.js')
            require(page.locator('#ricpe-original-accountability').count()==0,'Out-of-scope page unchanged')
            context.close();browser.close()
    finally:
        if server:server.shutdown();server.server_close()
        if temp:temp.cleanup()
        (OUT/('live-browser.json' if live else 'local-browser.json')).write_text(json.dumps(reports,indent=2))
    return reports

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--browser',action='store_true');ap.add_argument('--live',action='store_true');args=ap.parse_args()
    data=source_checks();reports=browser_checks(data,args.live) if args.browser or args.live else []
    result={'status':'PASS','sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'scope':'RICPE original/19 routes; not global proof or whole-site acceptance','live':args.live,'checks':checks,'browser_cases':len(reports),'open_gaps':data['open_gaps']}
    (OUT/('live-acceptance.json' if args.live else 'scoped-acceptance.json')).write_text(json.dumps(result,indent=2))
    print(json.dumps({'status':'PASS','checks':len(checks),'browser_cases':len(reports),'live':args.live},indent=2))

if __name__=='__main__':main()

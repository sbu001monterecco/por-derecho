#!/usr/bin/env python3
"""Read-only MASTER MYND candidate/production browser acceptance; never publishes."""
from __future__ import annotations
import argparse, functools, hashlib, http.server, json, pathlib, subprocess, threading, urllib.parse, urllib.request
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADDRESS = 'Calle Janubio 3, Playa Blanca, Lanzarote 35580, Spain'
DISCLOSURES = {'en':'SATIRICAL / CARICATURE REPRESENTATION — NOT A REAL ADVERTISEMENT', 'es':'CARICATURA / REPRESENTACIÓN SATÍRICA — NO ES UN ANUNCIO REAL'}

class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        clean=urllib.parse.unquote(urllib.parse.urlsplit(path).path)
        if clean.startswith('/por-derecho/'):
            clean=clean[len('/por-derecho/'):]
        else:
            clean=clean.lstrip('/')
        target=(ROOT/clean).resolve()
        if target!=ROOT and ROOT not in target.parents:
            return str(ROOT/'__invalid_path__')
        return str(target)
    def log_message(self,*args):
        pass

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url',default='')
    parser.add_argument('--output',default='/tmp/master-mynd-browser')
    parser.add_argument('--engines',default='chromium,firefox,webkit')
    args=parser.parse_args(); output=pathlib.Path(args.output);output.mkdir(parents=True,exist_ok=True)
    profile=json.loads((ROOT/'assets/data/sun-park-mynd-yaiza-site-v1.json').read_text())
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    server=None
    if args.base_url:
        base=args.base_url.rstrip('/')
    else:
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
        threading.Thread(target=server.serve_forever,daemon=True).start()
        base=f'http://127.0.0.1:{server.server_port}/por-derecho'
    report={'tested_sha':sha,'target':base,'production':bool(args.base_url),'cases':[],'resources':[],'errors':[]}
    routes=[]
    for language in ['es','en']:
        routes.extend([(language,profile['family_routes'][language],True),(language,profile['routes'][language],False)])
    resources={'assets/data/sun-park-mynd-yaiza-site-v1.json','assets/data/matter-identity-registry-v1.organisations.json','assets/data/matter-identity-registry-v1.json'}
    resources.update(image['path'] for image in profile['images'])
    resources.update(route.lstrip('/')+'index.html' for _,route,_ in routes)
    for language in ['es','en']:
        resources.update(edge['route'].lstrip('/')+'index.html' for edge in profile['discovery_routes'][language])
    try:
        for path in sorted(resources):
            url=base+'/'+path+'?pd_master_mynd='+sha
            try:
                with urllib.request.urlopen(url,timeout=35) as response:
                    received=response.read();status=response.status
                expected=(ROOT/path).read_bytes()
                item={'path':path,'status':status,'bytes':len(received),'sha256':hashlib.sha256(received).hexdigest(),'exact_match':received==expected}
                report['resources'].append(item)
                if status!=200 or received!=expected:report['errors'].append({'resource':path,'error':'not exact expected bytes'})
            except Exception as exc:report['errors'].append({'resource':path,'error':str(exc)})
        with sync_playwright() as p:
            for engine in args.engines.split(','):
                browser=getattr(p,engine).launch(headless=True)
                try:
                    for language,route,family in routes:
                        for width,javascript in [(320,True),(390,True),(1440,True),(390,False)]:
                            case={'engine':engine,'route':route,'width':width,'javascript':javascript,'errors':[]}
                            context=browser.new_context(viewport={'width':width,'height':900},java_script_enabled=javascript)
                            page=context.new_page(); exceptions=[];failed_responses=[]
                            page.on('pageerror',lambda exc:exceptions.append(str(exc)))
                            page.on('response',lambda response:failed_responses.append({'status':response.status,'url':response.url}) if response.status>=400 else None)
                            try:
                                response=page.goto(base+route+'?pd_master_mynd='+sha,wait_until='networkidle',timeout=45000)
                                if response is None or response.status!=200:case['errors'].append('route HTTP failure')
                                if page.locator('h1').count()!=1:case['errors'].append('not exactly one h1')
                                if ADDRESS not in page.locator('body').inner_text():case['errors'].append('canonical address missing')
                                if family and DISCLOSURES[language] not in page.locator('body').inner_text():case['errors'].append('satire disclosure missing')
                                if family:
                                    for image in profile['images']:
                                        locator=page.locator('img[src*="'+image['path']+'"]')
                                        if locator.count()!=1:case['errors'].append('image occurrence '+image['path']);continue
                                        locator.scroll_into_view_if_needed(timeout=10000)
                                        locator.evaluate('(i) => i.decode()')
                                        dimensions=locator.evaluate('(i) => [i.naturalWidth,i.naturalHeight]')
                                        if dimensions!=[image['width'],image['height']]:case['errors'].append('image dimensions '+image['path'])
                                    if language=='en' and page.locator('#aguiar-acosta-proposed-witness-pair').count()!=1:case['errors'].append('legacy witness anchor missing')
                                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                                page.wait_for_timeout(350)
                                geometry=page.evaluate('({viewport:innerWidth,scroll:document.documentElement.scrollWidth})')
                                case['geometry']=geometry
                                if geometry['scroll']>geometry['viewport']+1:case['errors'].append('horizontal overflow')
                                for image in page.locator('img').all():
                                    if image.is_visible():
                                        try:image.evaluate('(i) => i.decode()')
                                        except Exception:case['errors'].append('visible undecodable image: '+str(image.get_attribute('src')))
                                if exceptions:case['errors'].append({'page_exceptions':exceptions})
                                if failed_responses:case['errors'].append({'failed_http':failed_responses})
                                page.evaluate('window.scrollTo(0,0)')
                                if engine=='chromium' and width in [320,1440] and javascript:
                                    filename=language+'-'+route.strip('/').split('/')[-1]+'-'+str(width)+'.png'
                                    page.screenshot(path=str(output/filename),full_page=width==1440)
                                    case['screenshot']=filename
                            except Exception as exc:case['errors'].append(str(exc))
                            finally:context.close()
                            case['passed']=not case['errors'];report['cases'].append(case)
                            print(engine,route,width,javascript,'PASS' if case['passed'] else 'FAIL',flush=True)
                finally:browser.close()
    finally:
        if server:server.shutdown()
        report['passed']=not report['errors'] and bool(report['cases']) and all(case['passed'] for case in report['cases'])
        report['case_count']=len(report['cases']);report['resource_count']=len(report['resources'])
        (output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps({'passed':report['passed'],'cases':report['case_count'],'resources':report['resource_count']},indent=2))
    raise SystemExit(0 if report['passed'] else 1)

if __name__=='__main__':main()

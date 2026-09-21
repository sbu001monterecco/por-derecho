#!/usr/bin/env python3
"""Read-only local browser acceptance for CI projection and link corrections."""
from __future__ import annotations
import argparse
import functools
import http.server
import json
from pathlib import Path
import tempfile
import threading
from playwright.sync_api import sync_playwright
from reconcile_identity_registry_projections import ROOT, canonical_snapshot

ROUTES=('en/','es/','en/matter-identity-registry/','es/registro-identidad-materia/','en/acosta-matos-family/','es/acosta-matos-familia/')


def main() -> int:
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='/tmp/ci-control-plane/browser');args=parser.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    counts,_=canonical_snapshot();rows=[]
    with tempfile.TemporaryDirectory() as td:
        serve=Path(td);(serve/'por-derecho').symlink_to(ROOT,target_is_directory=True)
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self,*args):pass
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(serve)))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        try:
            with sync_playwright() as p:
                browser=p.chromium.launch()
                for width in (1440,390):
                    for js in (True,False):
                        context=browser.new_context(viewport={'width':width,'height':950},java_script_enabled=js,reduced_motion='reduce')
                        for route in ROUTES:
                            page=context.new_page()
                            response=page.goto(f'http://127.0.0.1:{server.server_port}/por-derecho/'+route,wait_until='domcontentloaded')
                            assert response and response.status==200,route
                            assert page.locator('main').count() and page.locator('h1').first.is_visible(),route
                            if 'identity-registry' in route or 'registro-identidad' in route:
                                assert page.locator('[data-registry-stat="TOTAL"]').first.inner_text().strip()==str(counts['total']),route
                                for kind in ('PERSON','ORGANISATION','STRUCTURE','INSTITUTION','PROCEEDING'):
                                    assert page.locator('[data-registry-stat="'+kind+'"]').first.inner_text().strip()==str(counts[kind]),(route,kind)
                            if route=='es/acosta-matos-familia/':
                                assert page.locator('a[href="../metodologia/"]').count()==0
                                assert page.locator('a[href="../por-derecho/como-funciona/"]').count()>=1
                            page.screenshot(path=str(out/(route.replace('/','_')+str(width)+'_'+str(js)+'.png')),animations='disabled')
                            rows.append({'route':route,'width':width,'javascript':js,'status':'PASS'})
                            page.close()
                        context.close()
                browser.close()
        finally:
            server.shutdown()
            (out/'results.json').write_text(json.dumps(rows,indent=2))
    print('BROWSER ACCEPTANCE: PASS',len(rows),'cases')
    return 0

if __name__=='__main__':raise SystemExit(main())

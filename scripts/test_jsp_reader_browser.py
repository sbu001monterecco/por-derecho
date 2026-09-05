#!/usr/bin/env python3
"""Read-only 24-case browser acceptance; local candidate or actual production."""
from __future__ import annotations
import argparse, hashlib, json, subprocess, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--live',action='store_true');a=ap.parse_args()
    out=Path('/tmp/jsp-browser-report');out.mkdir(exist_ok=True)
    origin='https://sbu001monterecco.github.io' if a.live else 'http://127.0.0.1:8765'
    base=origin+'/por-derecho/'
    evidence=json.loads((ROOT/'assets/data/jsp-2017-source-relationship-register.json').read_text())
    images=json.loads((ROOT/'assets/data/jsp-official-images-provenance-20260905.json').read_text())
    expected=sum(len(json.loads((ROOT/'assets/data'/p).read_text())['records']) for p in evidence['registry_parts'])
    report={'source_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'mode':'LIVE' if a.live else 'CANDIDATE','cases':[],'failures':[],'source_resource_checks':[],'boundary':'Browser-engine viewport tests, not physical-handset certification. No-JS checks static dossier and original-source/registry links; gallery enhancement uses JS.'}
    for item in [images['source'],*images['derivatives']]:
        with urllib.request.urlopen(base+item['path'],timeout=45) as r:raw=r.read();assert r.status==200
        assert hashlib.sha256(raw).hexdigest()==item['sha256']
        report['source_resource_checks'].append({'path':item['path'],'status':200,'sha256':item['sha256']})
    source=images['source']['url']
    routes={'es':'es/jsp-montelanza-concurso-liquidacion/','en':'en/jsp-montelanza-insolvency-liquidation/'}
    with sync_playwright() as pw:
        for engine in ('chromium','firefox','webkit'):
            browser=getattr(pw,engine).launch()
            for lang,route in routes.items():
                for width,js in [(320,True),(390,True),(1440,True),(390,False)]:
                    c={'browser':engine,'lang':lang,'width':width,'javascript':js,'errors':[],'console':[],'external_failed_requests':[]}
                    context=browser.new_context(viewport={'width':width,'height':1000},java_script_enabled=js)
                    page=context.new_page()
                    page.on('pageerror',lambda e,c=c:c['errors'].append(str(e)))
                    page.on('console',lambda msg,c=c:c['console'].append(msg.type+': '+msg.text))
                    page.on('response',lambda r,c=c:c['errors'].append('HTTP '+str(r.status)+' '+r.url) if r.status>=400 and r.url.startswith(base) else None)
                    # PDF viewer requests can be cancelled by a browser when handing
                    # them to its native viewer; exact bytes are verified separately.
                    page.on('requestfailed',lambda r,c=c:c['external_failed_requests'].append({'url':r.url,'failure':r.failure}))
                    try:
                        res=page.goto(base+route,wait_until='domcontentloaded',timeout=45000)
                        assert res.status==200 and page.locator('h1').count()==1
                        assert page.locator('a[href="'+source+'"]').count()>=1
                        body=page.locator('body').inner_text();assert '26.82%' in body or '26,82%' in body
                        if js:
                            page.wait_for_function("document.querySelector('#canonical-records table') !== null",timeout=20000)
                            assert page.locator('#canonical-records table').first.locator('tbody tr').count()==expected
                            assert page.locator('#official-notice-capture').count()==1
                            assert page.locator('#official-notice-frame').count()==1
                            assert page.locator('#official-notice-frame').get_attribute('src').startswith(base+images['source']['path'])
                            assert page.locator('#PD-SP-O-0085').count()==1 and page.locator('#PD-SP-O-0086').count()==1
                            assert page.locator('#source-records > p').count()==len(evidence['sources'])
                            assert page.locator('img[data-evidence-source="JSP-2017-S01"]').count()==2
                            page.wait_for_function("[...document.querySelectorAll('img[data-evidence-source]')].every(i=>i.complete&&i.naturalWidth>0)",timeout=20000)
                            c['images']=[]
                            for item in images['derivatives']:
                                loc=page.locator('img[src="'+base+item['path']+'"]')
                                size=loc.evaluate('(i)=>({width:i.naturalWidth,height:i.naturalHeight,box:i.getBoundingClientRect().toJSON(),alt:i.alt})')
                                assert (size['width'],size['height'])==(item['width'],item['height']) and size['alt']
                                assert 0<size['box']['width']<=width and size['box']['height']>0
                                assert loc.locator('..').get_attribute('href')==base+item['path']
                                c['images'].append(size)
                            page.locator('#jsp-evidence-item-five').scroll_into_view_if_needed()
                            page.screenshot(path=str(out/f'{engine}-{lang}-{width}-evidence.png'))
                            page.locator('#jsp-evidence-full-page').scroll_into_view_if_needed()
                        else:
                            assert page.locator('noscript a').count()>=3
                        overflow=page.evaluate('document.documentElement.scrollWidth-window.innerWidth');assert overflow<=2, str(overflow)
                        c['horizontal_overflow']=overflow
                        assert not c['errors'],str(c['errors'])
                        c['result']='PASS'
                    except Exception as e:
                        c['result']='FAIL';c['error']=str(e);report['failures'].append(c.copy())
                    page.screenshot(path=str(out/f'{engine}-{lang}-{width}-{js}.png'))
                    print(json.dumps(c,ensure_ascii=False));report['cases'].append(c);context.close()
            browser.close()
    report['case_count']=len(report['cases']);report['result']='PASS' if not report['failures'] else 'FAIL'
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'result':report['result'],'source_sha':report['source_sha'],'mode':report['mode'],'case_count':report['case_count'],'failures':report['failures']},ensure_ascii=False))
    assert report['case_count']==24 and not report['failures']
if __name__=='__main__':main()

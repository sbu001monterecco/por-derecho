#!/usr/bin/env python3
"""Read-only CR browser checks. Real links are clicked before capture.

Every review target is checked in the rendered DOM. Instant positioning is used
only for screenshots, avoiding Playwright's unrelated animation-stability wait.
Public DOM and screenshots are retained while the browser is alive on failure.
"""
from __future__ import annotations
import json,subprocess,time
from pathlib import Path
from urllib.parse import unquote,urlsplit
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'diagnostics';OUT.mkdir(exist_ok=True)
BASE='http://127.0.0.1:8765/por-derecho/'
PANEL='cr-continuity-closure-20260905'

def main():
    server=subprocess.Popen(['python','-m','http.server','8765','--bind','127.0.0.1','--directory',str(ROOT.parent)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    checks=0;observations=[];page=None;browser=None;p=None
    try:
        time.sleep(2);p=sync_playwright().start();browser=p.chromium.launch()
        for width in [390,1440]:
            for enabled in [False,True]:
                context=browser.new_context(viewport={'width':width,'height':1000},java_script_enabled=enabled,reduced_motion='reduce')
                for lang in ['es','en']:
                    label=f'{lang}-{width}-js{int(enabled)}';page=context.new_page();page.set_default_timeout(15000)
                    url=BASE+lang+'/cuatrecasas-sun-park/'
                    response=page.goto(url,wait_until='networkidle');assert response.status==200;checks+=1
                    panel=page.locator('[id="'+PANEL+'"]');assert panel.count()==1;checks+=1
                    assert panel.locator('tbody tr').count()==58;checks+=1
                    articles=panel.locator('article[data-gap-id]');assert articles.count()==7;checks+=1
                    ids=articles.evaluate_all('(els)=>els.map(e=>e.id)')
                    assert len(set(ids))==7 and all(ids);checks+=1
                    assert page.locator('.pd-cr-source').count()==4;checks+=1
                    assert page.locator('.pd-cr-identity').get_attribute('data-caret-state')=='CARET_CONFIRMED';checks+=1
                    before={'label':label,'url':page.url,'obligation_ids':ids}
                    for link in panel.locator('tbody a').all():
                        href=link.get_attribute('href');assert href and href.startswith('#')
                        target=unquote(href[1:]);assert page.locator('[id='+json.dumps(target)+']').count()==1,(label,href)
                        checks+=1
                    page.locator('[data-cr-continuity-jump] a').click();assert panel.is_visible();checks+=1
                    after=panel.locator('article[data-gap-id]').evaluate_all('(els)=>els.map(e=>e.id)')
                    before.update(after_jump_url=page.url,after_jump_obligation_ids=after);observations.append(before)
                    assert after==ids,'Jump navigation changed canonical targets'
                    assert panel.evaluate('(e)=>e.getBoundingClientRect().width<=innerWidth+2');checks+=1
                    # Position only after verifying the actual public navigation and targets.
                    panel.locator('article[data-gap-id]').first.evaluate('(e)=>e.scrollIntoView({block:"center",behavior:"instant"})')
                    assert panel.locator('article[data-gap-id]').first.evaluate('(e)=>{const r=e.getBoundingClientRect();return r.bottom>0&&r.top<innerHeight}')
                    checks+=1
                    page.screenshot(path=str(OUT/f'cr-continuity-{label}.png'),animations='disabled')
                    route=lang+'/'+('metodologia/' if lang=='es' else 'methodology/')
                    response=page.goto(BASE+route,wait_until='networkidle');assert response.status==200;checks+=1
                    assert page.locator('h1').count()==1;checks+=1
                    for link in page.locator('a').all():
                        href=link.get_attribute('href') or ''
                        if href.startswith('/por-derecho/'):
                            u=urlsplit(href);rel=u.path.removeprefix('/por-derecho/');rel+='index.html' if rel.endswith('/') else ''
                            assert (ROOT/rel).is_file(),rel;checks+=1
                    page.close();page=None
                context.close()
        result={'result':'BROWSER_PASS','checks':checks,'observations':observations,'widths':[390,1440],'languages':['es','en'],'java_script':[False,True],'correction_rows_per_language':58,'proof_obligations_per_language':7}
        (OUT/'cr-continuity-browser.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result))
    except Exception as exc:
        failure={'result':'BROWSER_FAIL','checks_completed':checks,'error':str(exc),'observations':observations}
        if page:
            try:
                failure['current_url']=page.url
                failure['rendered_article_ids']=page.locator('article').evaluate_all('(els)=>els.map(e=>e.id)')
                (OUT/'cr-continuity-failure-dom.html').write_text(page.content())
                page.screenshot(path=str(OUT/'cr-continuity-failure.png'),animations='disabled')
            except Exception as secondary:failure['capture_error']=str(secondary)
        (OUT/'cr-continuity-browser.json').write_text(json.dumps(failure,ensure_ascii=False,indent=2));print(json.dumps(failure));raise
    finally:
        if browser:browser.close()
        if p:p.stop()
        server.terminate()

if __name__=='__main__':main()

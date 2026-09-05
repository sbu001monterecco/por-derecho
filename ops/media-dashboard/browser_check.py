"""Read-only candidate browser check; no mail, mutation or production assertion."""
import json, os, pathlib, subprocess, time, urllib.request
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=pathlib.Path(os.environ.get('MEDIA_AUDIT_OUT','/tmp/media-candidate'));OUT.mkdir(exist_ok=True)
ROUTES=['es/medios-trazabilidad-relato-publico/','en/media-public-narrative-traceability/']
server=subprocess.Popen(['python3','-m','http.server','8765','--bind','127.0.0.1','--directory',str(ROOT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
results=[];live=[]
def visible_heading(heading,header,height):
 return bool(heading and heading['y']>=0 and heading['y']+heading['height']<height and (not header or heading['y']>=header['y']+header['height']-2))
try:
 time.sleep(1)
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for route in ROUTES:
   for width,height in [(390,844),(1280,900)]:
    page=browser.new_page(viewport={'width':width,'height':height});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    response=page.goto('http://127.0.0.1:8765/'+route+'#media-desk',wait_until='domcontentloaded');page.wait_for_timeout(6500)
    desk=page.locator('#media-desk');assert desk.count()==1
    assert page.locator('#media-desk article.card').count()==6
    assert page.locator('#media-desk form,#media-desk input,#media-desk script,#media-desk iframe').count()==0
    assert page.locator('#lpb-concurso-overreach-note').count()==1, 'Preserve inherited note'
    assert desk.locator('#lpb-concurso-overreach-note').count()==0, 'Do not inject inherited note into new heading'
    overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth + 2');assert not overflow
    assert response.status==200
    if width<=650:assert not page.locator('.main-nav').is_visible(), 'Mobile menu must start closed'
    initial_heading=page.locator('#media-desk-title').bounding_box();header=page.locator('.site-header').bounding_box()
    page.screenshot(path=str(OUT/f'{route[:2]}-{width}-initial-fragment.png'),full_page=False)
    initial={'route':route,'width':width,'heading':initial_heading,'header':header,'section':desk.bounding_box()}
    (OUT/f'{route[:2]}-{width}-initial-geometry.json').write_text(json.dumps(initial,indent=2))
    assert visible_heading(initial_heading,header,height),'Direct hash landing does not expose heading'
    # Also test a later explicit fragment navigation without smooth-animation screenshots.
    page.evaluate("document.querySelector('#media-desk').scrollIntoView({block:'start',behavior:'instant'})")
    page.wait_for_timeout(1000)
    heading=page.locator('#media-desk-title').bounding_box();header=page.locator('.site-header').bounding_box()
    assert visible_heading(heading,header,height),'Explicit fragment heading obscured'
    page.screenshot(path=str(OUT/f'{route[:2]}-{width}-desk-viewport.png'),full_page=False)
    desk.screenshot(path=str(OUT/f'{route[:2]}-{width}-desk-section.png'))
    page.screenshot(path=str(OUT/f'{route[:2]}-{width}.png'),full_page=True)
    assert not errors, 'Unexpected browser JavaScript error'
    results.append({'route':route,'width':width,'status':response.status,'overflow':overflow,'page_errors':errors,'desk_cards':6,'mobile_navigation_overlay':False if width<=650 else None,'initial_hash_heading':initial_heading,'settled_heading':heading,'sticky_header':header,'inherited_note_preserved_outside_desk':True,'direct_hash_heading_visible':True})
    page.close()
  for route in ROUTES:
   page=browser.new_page(java_script_enabled=False,viewport={'width':390,'height':844});page.goto('http://127.0.0.1:8765/'+route+'#media-desk');page.wait_for_timeout(1000)
   assert page.locator('#media-desk').is_visible();assert page.locator('#media-desk a').count()>=10
   assert visible_heading(page.locator('#media-desk-title').bounding_box(),page.locator('.site-header').bounding_box(),844),'No-JavaScript hash heading obscured'
   results.append({'route':route,'javascript':False,'static_desk':True,'direct_hash_heading_visible':True});page.close()
  for language,route in [('es','es/buscar/'),('en','en/search/')]:
   page=browser.new_page();page.goto('http://127.0.0.1:8765/'+route+'?q=media%20dashboard');page.wait_for_timeout(8000)
   needle=ROUTES[0 if language=='es' else 1]
   match=page.locator('#psr-search-results a[href*="'+needle+'"]');assert match.count()>0,'Existing search does not resolve desk'
   results.append({'search':route,'query':'media dashboard','canonical_result':needle,'matches':match.count()});page.close()
  browser.close()
 for route in ['es/','en/','es/ric-private-equity-sun-park/','es/reconstruccion-unitaria-autoridades-publicas/','es/registros-institucionales/']:
  url='https://sbu001monterecco.github.io/por-derecho/'+route+'?media_source_check=20260905'
  try:
   with urllib.request.urlopen(url,timeout=30) as r:
    body=r.read();live.append({'route':route,'status':r.status,'content_type':r.headers.get('Content-Type'),'bytes':len(body),'html':b'<html' in body.lower()})
  except Exception as e:live.append({'route':route,'error':type(e).__name__+': '+str(e)})
 assert all(x.get('status')==200 and x.get('html') for x in live),'Public source check failed'
 (OUT/'browser.json').write_text(json.dumps({'candidate_sha':os.environ.get('GITHUB_SHA'),'checks':results,'public_source_checks':live,'deployment_verified':False},ensure_ascii=False,indent=2))
finally:server.terminate()

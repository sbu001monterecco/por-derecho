#!/usr/bin/env python3
"""Read-only MASTER MYND candidate/production acceptance; no publication writes."""
from __future__ import annotations
import argparse, hashlib, http.server, json, pathlib, subprocess, threading, time, urllib.parse, urllib.request
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]
ADDRESS='Calle Janubio 3, Playa Blanca, Lanzarote 35580, Spain'
DISCLOSURES={'en':'SATIRICAL / CARICATURE REPRESENTATION — NOT A REAL ADVERTISEMENT','es':'CARICATURA / REPRESENTACIÓN SATÍRICA — NO ES UN ANUNCIO REAL'}
class Handler(http.server.SimpleHTTPRequestHandler):
 def translate_path(self,path):
  clean=urllib.parse.unquote(urllib.parse.urlsplit(path).path)
  clean=clean[len('/por-derecho/'):] if clean.startswith('/por-derecho/') else clean.lstrip('/')
  target=(ROOT/clean).resolve()
  return str(target if target==ROOT or ROOT in target.parents else ROOT/'__invalid_path__')
 def log_message(self,*args):pass

def image_pixels(locator):
 """Actual scroll/load and synchronous canvas decode, also when page JS is disabled.

 Image.decode() promises can remain pending in a no-script Firefox context.
 No timers/promises, source replacements or loading-attribute changes are used.
 """
 locator.scroll_into_view_if_needed(timeout=10000)
 deadline=time.monotonic()+10
 while time.monotonic()<deadline:
  state=locator.evaluate('(i)=>({complete:i.complete,w:i.naturalWidth,h:i.naturalHeight})')
  if state['complete'] and state['w']>0 and state['h']>0:
   painted=locator.evaluate('(i)=>{const c=document.createElement("canvas");c.width=8;c.height=8;const x=c.getContext("2d");x.drawImage(i,0,0,8,8);return Array.from(x.getImageData(0,0,8,8).data).some(v=>v!==0)}')
   if not painted:raise AssertionError('Decoded image produced no pixels: '+str(locator.get_attribute('src')))
   return [state['w'],state['h']]
  time.sleep(.15)
 raise AssertionError('Image did not become complete/decodable after actual scroll: '+str(locator.get_attribute('src')))

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--base-url',default='');parser.add_argument('--output',default='/tmp/master-mynd-browser');parser.add_argument('--engines',default='chromium,firefox,webkit')
 args=parser.parse_args();output=pathlib.Path(args.output);output.mkdir(parents=True,exist_ok=True)
 profile=json.loads((ROOT/'assets/data/sun-park-mynd-yaiza-site-v1.json').read_text())
 sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();server=None
 if args.base_url:base=args.base_url.rstrip('/')
 else:
  server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/por-derecho'
 report={'tested_sha':sha,'target':base,'production':bool(args.base_url),'cases':[],'resources':[],'errors':[],'complete':False}
 def save():
  report['case_count']=len(report['cases']);report['resource_count']=len(report['resources'])
  report['passed']=report['complete'] and not report['errors'] and len(report['cases'])==len(args.engines.split(','))*16 and all(c['passed'] for c in report['cases'])
  (output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 routes=[]
 for language in ['es','en']:routes.extend([(language,profile['family_routes'][language],True),(language,profile['routes'][language],False)])
 resources={'assets/master-mynd-reader-priority.js','assets/data/sun-park-mynd-yaiza-site-v1.json','assets/data/matter-identity-registry-v1.organisations.json','assets/data/matter-identity-registry-v1.json'}
 resources.update(i['path'] for i in profile['images']);resources.update(r.lstrip('/')+'index.html' for _,r,_ in routes)
 for language in ['es','en']:resources.update(e['route'].lstrip('/')+'index.html' for e in profile['discovery_routes'][language])
 try:
  for path in sorted(resources):
   try:
    with urllib.request.urlopen(base+'/'+path+'?pd_master_mynd='+sha,timeout=35) as response:received=response.read();status=response.status
    item={'path':path,'status':status,'bytes':len(received),'sha256':hashlib.sha256(received).hexdigest(),'exact_match':received==(ROOT/path).read_bytes()};report['resources'].append(item)
    if status!=200 or not item['exact_match']:report['errors'].append({'resource':path,'error':'not exact expected bytes'})
   except Exception as exc:report['errors'].append({'resource':path,'error':str(exc)})
  save()
  with sync_playwright() as p:
   for engine in args.engines.split(','):
    browser=getattr(p,engine).launch(headless=True)
    try:
     for language,route,family in routes:
      for width,javascript in [(320,True),(390,True),(1440,True),(390,False)]:
       case={'engine':engine,'route':route,'width':width,'javascript':javascript,'errors':[],'images':[]}
       context=browser.new_context(viewport={'width':width,'height':900},java_script_enabled=javascript);page=context.new_page();page.set_default_timeout(12000)
       exceptions=[];failed_responses=[]
       page.on('pageerror',lambda exc:exceptions.append(exc.stack or str(exc)))
       page.on('response',lambda r:failed_responses.append({'status':r.status,'url':r.url}) if r.status>=400 else None)
       try:
        response=page.goto(base+route+'?pd_master_mynd='+sha,wait_until='load',timeout=45000);page.wait_for_timeout(500)
        if response is None or response.status!=200:case['errors'].append('route HTTP failure')
        if page.locator('h1').count()!=1:case['errors'].append('not exactly one h1')
        body=page.locator('body').inner_text()
        if ADDRESS not in body:case['errors'].append('canonical address missing')
        if family and DISCLOSURES[language] not in body:case['errors'].append('satire disclosure missing')
        if family and language=='en':case['errors'].extend(page.locator('#master-mynd-record > h1, #master-mynd-record > p').evaluate_all("(els)=>{const rgb=s=>(s.match(/[0-9.]+/g)||[]).slice(0,3).map(Number);const lum=cs=>cs.map(c=>{c/=255;return c<=.04045?c/12.92:Math.pow((c+.055)/1.055,2.4)}).reduce((s,c,i)=>s+c*[.2126,.7152,.0722][i],0);return els.filter(e=>e.innerText.trim()).flatMap(e=>{let b=e;while(b&&getComputedStyle(b).backgroundColor==='rgba(0, 0, 0, 0)')b=b.parentElement;const fg=rgb(getComputedStyle(e).color),bg=b?rgb(getComputedStyle(b).backgroundColor):[255,255,255];const a=lum(fg),z=lum(bg),ratio=(Math.max(a,z)+.05)/(Math.min(a,z)+.05);return ratio>=4.5?[]:[{low_master_narrative_contrast:e.tagName,ratio,fg,bg}]})}"))
        if family:
         expected_first='master-mynd-record' if language=='en' else 'master-mynd'
         if page.locator('main').evaluate('(m)=>m.firstElementChild.id')!=expected_first:case['errors'].append('approved MASTER MYND content is not the first main section')
         for image in profile['images']:
          locators=page.locator('img[src*="'+image['path']+'"]')
          # English preserves its earlier unaltered photo in the legacy dossier.
          expected_count=2 if language=='en' and image['path'].endswith('hotel-plans.jpg') else 1
          if locators.count()!=expected_count:case['errors'].append('image occurrence '+image['path'])
          for locator in locators.all():
           dimensions=image_pixels(locator)
           if dimensions!=[image['width'],image['height']]:case['errors'].append('image dimensions '+image['path'])
         if language=='en' and page.locator('#aguiar-acosta-proposed-witness-pair').count()!=1:case['errors'].append('legacy witness anchor missing')
        for locator in page.locator('img').all():
         if locator.is_visible():
          try:case['images'].append({'src':locator.get_attribute('src'),'decoded_pixels':True,'dimensions':image_pixels(locator)})
          except Exception as exc:case['errors'].append(str(exc))
        page.evaluate('window.scrollTo(0,document.body.scrollHeight)');page.wait_for_timeout(350)
        geometry=page.evaluate('({viewport:innerWidth,scroll:document.documentElement.scrollWidth})');case['geometry']=geometry
        if geometry['scroll']>geometry['viewport']+1:case['errors'].append('horizontal overflow')
        if exceptions:case['errors'].append({'page_exceptions':exceptions})
        if failed_responses:case['errors'].append({'failed_http':failed_responses})
        page.evaluate('window.scrollTo(0,0)')
        if engine=='chromium' and width in [320,1440] and javascript:
         filename=language+'-'+route.strip('/').split('/')[-1]+'-'+str(width)+'.png'
         page.screenshot(path=str(output/filename),full_page=width==1440,timeout=15000);case['screenshot']=filename
       except Exception as exc:case['errors'].append(str(exc))
       finally:context.close()
       case['passed']=not case['errors'];report['cases'].append(case);save()
       print(json.dumps(case,ensure_ascii=False),flush=True)
    finally:browser.close()
  report['complete']=True
 finally:
  if server:server.shutdown()
  save()
 print(json.dumps({'passed':report['passed'],'cases':report['case_count'],'resources':report['resource_count']},indent=2))
 raise SystemExit(0 if report['passed'] else 1)
if __name__=='__main__':main()

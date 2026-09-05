#!/usr/bin/env python3
"""Read-only audit. Public repository/site inputs only; no mailbox credentials or writes.
The report is diagnostic evidence, not a whole-repository publication certificate.
"""
from __future__ import annotations
import argparse, asyncio, concurrent.futures, hashlib, json, os, pathlib, re, subprocess, time, zipfile
from urllib.parse import urljoin, urlsplit, unquote
import requests
from bs4 import BeautifulSoup

ROOT = pathlib.Path.cwd()
OUT = pathlib.Path(os.environ.get('PD_AUDIT_OUT', '/tmp/caixabank-audit'))
BASE = 'https://sbu001monterecco.github.io/por-derecho/'
REPO = 'sbu001monterecco/por-derecho'
ROUTES = ['es/reclamacion-caixabank-valencia/', 'en/caixabank-valencia-claim/']
for root, subs in [('es/reclamacion-caixabank-valencia/', ['documentos/', 'faq-contexto-unitario/', 'ob-rem-ac-cam-28nov2018/', 'senalamiento-28-enero-2027/']), ('en/caixabank-valencia-claim/', ['documents/', 'faq-unitary-context/', 'ob-rem-ac-cam-28nov2018/', 'hearing-28-january-2027/'])]:
    ROUTES.extend(root + sub for sub in subs)
TEXT_EXT = {'.html','.css','.js','.json','.md','.txt','.csv','.xml','.py','.yml','.yaml','.svg'}

def save(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def api(path):
    headers = {'Accept':'application/vnd.github+json'}
    token = os.environ.get('GH_TOKEN')
    if token: headers['Authorization'] = 'Bearer ' + token
    r = requests.get('https://api.github.com/repos/'+REPO+'/'+path, headers=headers, timeout=45)
    r.raise_for_status()
    return r.json()

def source_audit():
    OUT.mkdir(parents=True, exist_ok=True)
    sha = subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip()
    paths = subprocess.check_output(['git','ls-files'], text=True).splitlines()
    selected = []
    inbound = []
    sources = []
    for name in paths:
        p = ROOT/name
        if p.is_file() and p.suffix.lower() in TEXT_EXT:
            selected.append(name)
            if p.suffix.lower() == '.html':
                text = p.read_text(errors='replace')
                for a in BeautifulSoup(text,'html.parser').find_all('a',href=True):
                    target = urljoin(BASE+name, a['href'])
                    if any('/'+r in target for r in ROUTES[:2]):
                        inbound.append({'from':name,'to':target,'label':a.get_text(' ',strip=True)[:160]})
            if any(t in name.lower() for t in ['caixabank','valencia','uria','haya']) or name in ['AGENTS.md','CURRENT_START_HERE.md','CHATGPT_START_HERE.md']:
                sources.append({'path':name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    with zipfile.ZipFile(OUT/'public-source.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in selected: z.write(ROOT/name,name)
        for name in paths:
            if pathlib.Path(name).suffix.lower() in {'.jpg','.jpeg','.png','.webp'} and ('caixabank' in name.lower() or name in ['assets/sun-park-mynd-yaiza.jpg','assets/actors/francisco-de-borja-rodriguez-batllori.jpg']):
                z.write(ROOT/name,name)
        z.writestr('AUDIT_SOURCE_SHA',sha)
    save('source-inventory.json',{'sha':sha,'tracked_files':len(paths),'text_files':len(selected),'sources':sources,'inbound_links':inbound})
    try:
        prs=[]; branches=[]
        for page in range(1,101):
            rows=api('pulls?state=open&per_page=100&page='+str(page))
            prs.extend({k:p.get(k) for k in ['number','title','state','draft','updated_at','html_url']} | {'head':p['head']['ref'],'head_sha':p['head']['sha'],'base':p['base']['ref']} for p in rows)
            if len(rows)<100: break
        for page in range(1,101):
            rows=api('branches?per_page=100&page='+str(page))
            branches.extend({'name':b['name'],'sha':b['commit']['sha']} for b in rows)
            if len(rows)<100: break
        save('remote-state.json',{'observed_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'main':api('git/ref/heads/main')['object']['sha'],'open_prs':prs,'branches':branches})
    except Exception as e: save('remote-state-error.json',{'error':str(e)})
    print('SOURCE_AUDIT',len(paths),len(selected),len(sources),len(inbound),flush=True)

JS_SNAPSHOT = r'''() => {
 const root=document.documentElement, vw=innerWidth;
 const visible=e=>{const r=e.getBoundingClientRect(); const s=getComputedStyle(e);return r.width>0&&r.height>0&&s.display!=='none'&&s.visibility!=='hidden';};
 const containedScroller=e=>{for(let p=e.parentElement;p&&p!==document.body;p=p.parentElement){const s=getComputedStyle(p);if(['auto','scroll'].includes(s.overflowX))return true;}return false;};
 const over=[...document.querySelectorAll('main *')].filter(e=>visible(e)&&!containedScroller(e)&&e.getBoundingClientRect().right>vw+2).slice(0,50).map(e=>({tag:e.tagName,id:e.id,cls:typeof e.className==='string'?e.className:'',right:Math.round(e.getBoundingClientRect().right),width:Math.round(e.getBoundingClientRect().width)}));
 const ids=[...document.querySelectorAll('[id]')].map(e=>e.id), seen=new Set(), dup=ids.filter(x=>seen.has(x)||!seen.add(x));
 return {title:document.title,width:vw,documentWidth:root.scrollWidth,bodyWidth:document.body.scrollWidth,overflow:over,duplicateIds:[...new Set(dup)],images:[...document.images].map(e=>({src:e.currentSrc||e.src,alt:e.alt,complete:e.complete,naturalWidth:e.naturalWidth,naturalHeight:e.naturalHeight,displayWidth:e.getBoundingClientRect().width,displayHeight:e.getBoundingClientRect().height,visible:visible(e),loading:e.loading})),links:[...document.querySelectorAll('a[href]')].map(a=>({href:a.href,label:a.textContent.trim().slice(0,120)})),scripts:[...document.scripts].map(s=>s.src).filter(Boolean),headings:[...document.querySelectorAll('main h1,main h2')].map(e=>({id:e.id,text:e.textContent.trim()})),metadata:[...document.querySelectorAll('meta[property],meta[name="description"],link[rel="canonical"],link[rel="alternate"]')].map(e=>({key:e.getAttribute('property')||e.getAttribute('name')||e.getAttribute('rel'),value:e.getAttribute('content')||e.getAttribute('href')}))};
}'''

async def browser_audit():
    from playwright.async_api import async_playwright
    results=[]; urls=set(); failures=[]
    async with async_playwright() as p:
        for engine in ['chromium','firefox','webkit']:
            try: browser=await getattr(p,engine).launch()
            except Exception as e:
                failures.append({'engine':engine,'error':str(e)});continue
            context=await browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1)
            for index,route in enumerate(ROUTES):
                page=await context.new_page(); errors=[]; bad=[]
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('response', lambda r: bad.append({'url':r.url,'status':r.status}) if r.status>=400 else None)
                row={'engine':engine,'route':route,'javascript':True,'screens':[]}
                try:
                    response=await page.goto(BASE+route,wait_until='domcontentloaded',timeout=60000)
                    row['status']=response.status if response else None
                    await page.wait_for_timeout(5000)
                    for img in await page.locator('img').all():
                        await img.evaluate('(e)=>e.scrollIntoView({behavior:"instant",block:"center"})')
                        try: await img.evaluate('(e)=>Promise.race([e.decode().catch(()=>null),new Promise(r=>setTimeout(r,4000))])')
                        except Exception: pass
                    widths=[320,375,390,430,768,1024,1440] if index<2 else [390,1440]
                    row['viewports']=[]
                    for w in widths:
                        await page.set_viewport_size({'width':w,'height':900})
                        await page.wait_for_timeout(250)
                        snap=await page.evaluate(JS_SNAPSHOT)
                        urls.update(a['href'].split('#')[0] for a in snap['links'] if a['href'].startswith(BASE) or '1drv.ms/' in a['href'])
                        urls.update(i['src'].split('#')[0] for i in snap['images'] if i['src'].startswith('http'))
                        urls.update(s.split('#')[0] for s in snap['scripts'] if s.startswith(BASE))
                        row['viewports'].append(snap)
                        if w==390:
                            await page.evaluate('scrollTo({top:0,behavior:"instant"})')
                            fn=engine+'-'+route.replace('/','_')+'390.png'
                            await page.screenshot(path=str(OUT/fn),full_page=True,timeout=45000)
                            row['screens'].append(fn)
                    if engine=='chromium':
                        (OUT/(route.replace('/','_')+'rendered.html')).write_text(await page.content(),encoding='utf-8')
                    # Test the actual menu toggle when present, without assuming a broken menu if it is absent.
                    toggles=page.locator('.nav-toggle:visible')
                    if await toggles.count():
                        await page.set_viewport_size({'width':390,'height':900})
                        await toggles.first.click(timeout=5000)
                        row['menu_expanded']=await toggles.first.get_attribute('aria-expanded')
                    # A cached revisit is separately observed, not inferred from the fresh navigation.
                    if index<2:
                        await page.reload(wait_until='domcontentloaded',timeout=60000);await page.wait_for_timeout(2500)
                        row['cached_revisit']=await page.evaluate(JS_SNAPSHOT)
                except Exception as e: row['error']=str(e)
                row['page_errors']=errors;row['failed_responses']=bad;results.append(row)
                save('browser-results.json',{'results':results,'engine_failures':failures})
                print('BROWSER',engine,route,row.get('status'),row.get('error','OK'),flush=True)
                await page.close()
            await context.close()
            # No-JS on every direct dossier route: necessary for robust source access and static navigation.
            nojs=await browser.new_context(java_script_enabled=False,viewport={'width':390,'height':900})
            for route in ROUTES:
                page=await nojs.new_page()
                try:
                    res=await page.goto(BASE+route,wait_until='load',timeout=45000)
                    html=await page.content();soup=BeautifulSoup(html,'html.parser')
                    results.append({'engine':engine,'route':route,'javascript':False,'status':res.status if res else None,'static_links':[a.get('href') for a in soup.select('a[href]')],'images':[i.get('src') for i in soup.select('img')]})
                except Exception as e: results.append({'engine':engine,'route':route,'javascript':False,'error':str(e)})
                await page.close()
            await browser.close()
    save('browser-results.json',{'results':results,'engine_failures':failures})
    save('discovered-urls.json',sorted(urls))
    return urls

def http_one(url):
    row={'url':url}
    try:
        r=requests.get(url,timeout=35,allow_redirects=True)
        row.update(status=r.status_code,final_url=r.url,mime=r.headers.get('Content-Type',''),bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest(),redirects=[{'status':h.status_code,'url':h.url} for h in r.history])
        if url.startswith(BASE):
            rel=unquote(urlsplit(url).path[len('/por-derecho/'):])
            f=ROOT/rel
            if f.is_dir(): f=f/'index.html'
            if f.is_file(): row['matches_checked_out_bytes']=r.content==f.read_bytes()
        if r.content.startswith(b'%PDF-'):
            import fitz
            d=fitz.open(stream=r.content,filetype='pdf');row['pdf_pages']=len(d);row['is_pdf']=True
            fn='public-file-'+row['sha256'][:16]+'.pdf';(OUT/fn).write_bytes(r.content);row['public_binary_capture']=fn
        elif '1drv.ms' in url:
            row['is_pdf']=False;row['limitation']='Public viewer response is not verification of the PDF byte stream.'
        if 'text/html' in row['mime']:
            soup=BeautifulSoup(r.content,'html.parser');row['title']=soup.title.get_text() if soup.title else ''
            row['soft_404_suspected']='404' in row['title'] or 'Page not found' in row['title']
    except Exception as e: row['error']=str(e)
    return row

def http_audit(urls):
    urls=set(urls)
    for route in ROUTES:
        urls.add(BASE+route)
        f=ROOT/route/'index.html'
        if f.exists():
            soup=BeautifulSoup(f.read_text(),'html.parser')
            for e in soup.select('[href],[src]'):
                value=e.get('href') or e.get('src')
                u=urljoin(BASE+route,value).split('#')[0]
                if u.startswith(BASE) or '1drv.ms/' in u: urls.add(u)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: rows=list(pool.map(http_one,sorted(urls)))
    save('http-results.json',rows)
    print('HTTP_AUDIT',len(rows),'ERRORS',sum(1 for r in rows if r.get('status')!=200 or r.get('soft_404_suspected')),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['source','browser','http','all'],default='all');args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    if args.stage in ['source','all']: source_audit()
    urls=set()
    if args.stage in ['browser','all']: urls=asyncio.run(browser_audit())
    if args.stage in ['http','all']:
        f=OUT/'discovered-urls.json'
        if f.exists(): urls.update(json.loads(f.read_text()))
        http_audit(urls)

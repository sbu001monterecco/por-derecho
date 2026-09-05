#!/usr/bin/env python3
"""Read-only exact-source and rendered acceptance; never publishes or contacts."""
from __future__ import annotations
import argparse,copy,functools,hashlib,http.server,io,json,re,subprocess,tempfile,threading,urllib.request
from pathlib import Path
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
from jsonschema import Draft202012Validator
import fitz,markdown
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
MAN='assets/data/jsp-boc-release-manifest-20260905.json'
SUP='assets/data/jsp-incident-tourism-roster-supplement-20260905.json'
COM='assets/data/institutional-communications-register-v1.json'
BASE='https://sbu001monterecco.github.io/por-derecho/'
def load(p):return json.loads((ROOT/p).read_text())
def require(ok,msg):
    if not ok:raise AssertionError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def norm(s):return ' '.join(s.split())
def shape(x):
    require(x['coverage']['historical_events']==12,'twelve historic events')
    require(x['coverage']['combined_reference_count']==69,'69 reference denominator')
    require(x['coverage']['identity_admissions']==0,'no covert identity admission')
    require(len(x['canonical_events'])==12 and len({r['id']for r in x['canonical_events']})==12,'event identities')
    require(len(x['components'])==4 and sum(r['proposed_eur']for r in x['components'])==14543,'four proposed components and amount')
    require(x['components'][3]['date_in_notice']=='2007-02-14','unrepaired source date retained')
    require(len(x['witness_requests'])==22,'22 qualified evidence targets')
    require(x['claims_review']['state']=='ORIGINATING_CLAIMS_NOT_VERIFIED','claims boundary')
    require(x['saip_plan']['state']=='PREPARED_NOT_SIGNED_NOT_SUBMITTED' and x['saip_plan']['registry_receipt']is None,'no false filing')
    require(x['source_capture']['sha256']=='21d92223ac38b894054cc4ef70d7073df7d81de8da8ed2d53cc813e159041fc0','native BOC hash')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--live',action='store_true');ap.add_argument('--output',default='/tmp/jsp-boc-qa');a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    result={'scope':'PD-JSP-BOC-SIX-20260905','live':a.live,'checks':[],'byte_matches':[],'cases':[],'failures':[]};server=None
    try:
        manifest=load(MAN);extension=load(SUP)['execution'];shape(extension)
        require(len(extension['new_document_references'])==5,'five extra sources')
        for r in manifest['files']:
            b=(ROOT/r['path']).read_bytes();require(len(b)==r['bytes'] and digest(b)==r['sha256'],'manifest bytes '+r['path'])
        result['checks'].append('all prepared file bytes equal reviewed manifest')
        schema=load('.github/evidence-intelligence/schemas/institutional-communications.schema.json');reg=load(COM);Draft202012Validator(schema).validate(reg)
        ids=[e['event_id']for e in reg['events']];require(len(ids)==len(set(ids)),'unique global events')
        for row in extension['canonical_events']:
            matches=[e for e in reg['events']if e['event_id']==row['id']];require(len(matches)==1 and matches[0]['source_key']==row['source_key'] and matches[0]['event_date']==row['date'],'atomic event bridge')
        result['checks'].append('canonical schema and twelve atomic source/date/anchor bridges')
        for source in manifest['sources'].values():require(digest((ROOT/source['path']).read_bytes())==source['sha256'],'source hash')
        pdf=fitz.open(ROOT/extension['source_capture']['path']);require(len(pdf)==4,'complete four-page native BOC')
        for image in extension['images']:
            b=(ROOT/image['path']).read_bytes();require(digest(b)==image['sha256'],'image exact bytes');pix=pdf[image['pdf_page']-1].get_pixmap(matrix=fitz.Matrix(image['scale'],image['scale']),clip=fitz.Rect(image['clip_points']),alpha=False,colorspace=fitz.csRGB)
            with Image.open(io.BytesIO(b))as im:im.load();require(im.size==(pix.width,pix.height) and im.convert('RGB').tobytes()==pix.samples,'unannotated PDF pixel equality')
        result['checks'].append('native BOC/BORME and lossless source crop integrity')
        roots=manifest['pages'][:2]
        for route in roots:
            soup=BeautifulSoup((ROOT/route).read_text(),'html.parser');block=soup.select_one('#jsp-boc-six-sections');require(block is not None,'static main block')
            require(len(block.select('[data-full-section]'))==6,'six complete sections')
            source=(ROOT/f'archive/jsp-six-section-source-20260905.{route[:2]}.md').read_text();chunks=re.split(r'(?m)^## (?=[1-6]\. )',source)[1:];require(len(chunks)==6,'six source chunks')
            for n,chunk in enumerate(chunks,1):
                expected=BeautifulSoup(markdown.markdown('## '+chunk.split('\n---\n')[0].rstrip(),extensions=['tables']),'html.parser').get_text(' ')
                actual=block.select_one('[data-full-section="'+str(n)+'"]').get_text(' ');require(norm(actual).startswith(norm(expected)),'full section text preserved '+route+' '+str(n))
            require(len(block.select('.witness'))==22,'22 static witness records')
            for e in extension['canonical_events']:require(block.find(id='communication-'+e['id'])is not None,'event anchor')
            require(not re.search(r'mail\.google|@monterecco|file_000000|message_id|sk-proj-',str(block),re.I),'no private provider values')
            for link in block.select('[href],[src]'):
                target=link.get('href')or link.get('src');u=urlsplit(target)
                if u.scheme or u.netloc:continue
                path=((ROOT/route).parent/unquote(u.path)).resolve()if u.path else ROOT/route
                if path.is_dir():path/= 'index.html'
                require(path.exists(),'local target '+target)
        result['checks'].append('all twelve full source sections, static references and no private locators')
        mutations=[lambda x:x['canonical_events'].pop(),lambda x:x['coverage'].__setitem__('identity_admissions',1),lambda x:x['components'][0].__setitem__('proposed_eur',0),lambda x:x['saip_plan'].__setitem__('registry_receipt','FABRICATED'),lambda x:x['claims_review'].__setitem__('state','NO_CLAIMS_EXIST')]
        for mutation in mutations:
            bad=copy.deepcopy(extension);mutation(bad)
            try:shape(bad)
            except AssertionError:pass
            else:raise AssertionError('negative test accepted')
        result['negative_tests_rejected']=len(mutations)
        if a.live:
            base=BASE
            paths=[r['path']for r in manifest['files']]+[MAN,'archive/jsp-six-section-source-20260905.en.md','archive/jsp-six-section-source-20260905.es.md']+[s['path']for s in manifest['sources'].values()]
            for path in dict.fromkeys(paths):
                with urllib.request.urlopen(urllib.request.Request(base+path,headers={'Cache-Control':'no-cache','User-Agent':'PorDerecho-ExactLiveReadback/1.0'}),timeout=30)as response:actual=response.read()
                expected=(ROOT/path).read_bytes();require(actual==expected,'actual live bytes '+path);result['byte_matches'].append({'path':path,'bytes':len(actual),'sha256':digest(actual)})
        else:
            mount=Path(tempfile.mkdtemp());(mount/'por-derecho').symlink_to(ROOT,target_is_directory=True)
            class Quiet(http.server.SimpleHTTPRequestHandler):
                def log_message(self,*args):pass
            server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(mount)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/por-derecho/'
        from playwright.sync_api import sync_playwright
        with sync_playwright()as pw:
            for engine in ['chromium','firefox','webkit']:
                browser=getattr(pw,engine).launch()
                for route in roots:
                    for width,js in [(320,True),(390,True),(1440,True),(390,False)]:
                        context=browser.new_context(viewport={'width':width,'height':900},java_script_enabled=js);page=context.new_page();errors=[];bad=[]
                        page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:bad.append([r.status,r.url])if r.status>=400 and r.url.startswith(base)else None)
                        r=page.goto(base+route,wait_until='networkidle',timeout=60000);require(r.status==200,'page status')
                        require(page.locator('[data-full-section]').count()==6,'six full sections actually rendered');require(page.locator('#qualified-witnesses .witness').count()==22,'witness reader count')
                        page.locator('#boc-308-07').scroll_into_view_if_needed()
                        for im in page.locator('#boc-308-07 img').all():
                            im.scroll_into_view_if_needed()
                            # Native lazy loading is asynchronous, especially in Firefox.
                            # Wait for completion but still fail on HTTP/decode errors or timeout.
                            page.wait_for_function('(i)=>i.complete',arg=im.element_handle(),timeout=15000)
                            require(im.evaluate('async(i)=>{if(!i.naturalWidth)return false;try{await i.decode();return i.complete&&i.naturalWidth>0;}catch(e){return false;}}'),'BOC source image decodes')
                        for n in range(1,7):require(page.locator('#background-'+str(n)).inner_text().strip(),'full section visible')
                        broken=page.evaluate('''() => [...document.querySelectorAll('#jsp-boc-six-sections a[href]')].filter(a=>a.hash&&a.origin===location.origin&&a.pathname===location.pathname&&!document.getElementById(decodeURIComponent(a.hash.slice(1)))).map(a=>a.href)''');require(not broken,'in-page source anchors '+str(broken))
                        require(page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),'no horizontal overflow')
                        require(not errors and not bad,'browser errors '+str(errors+bad))
                        if engine=='chromium' and js and width in [390,1440]:
                            for anchor in ['boc-308-07','current-corrections','qualified-witnesses','full-background']:
                                page.locator('#'+anchor).scroll_into_view_if_needed();page.screenshot(path=str(out/f'{route[:2]}-{width}-{anchor}.png'))
                        result['cases'].append({'engine':engine,'route':route,'width':width,'javascript':js,'status':'PASS'});context.close()
                browser.close()
        require(len(result['cases'])==24,'24 exact root-reader browser cases')
        require(not subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip(),'read-only worktree')
        result['result']='PASS_LIVE_SCOPED'if a.live else'PASS_CANDIDATE_SCOPED'
    except Exception as e:result['result']='FAIL';result['failures'].append(str(e))
    finally:
        if server:server.shutdown()
        (out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
    return int(result['result']=='FAIL')
if __name__=='__main__':raise SystemExit(main())

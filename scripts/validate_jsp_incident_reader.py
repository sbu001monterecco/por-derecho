#!/usr/bin/env python3
"""Read-only acceptance for the public incident reference layer; never publishes."""
from __future__ import annotations
import argparse, copy, functools, hashlib, http.server, json, re, subprocess, tempfile, threading, time, unicodedata, urllib.request
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
ROOT=Path(__file__).resolve().parents[1]
ROUTES=['es/jsp-montelanza-concurso-liquidacion/registro-incidente/index.html','en/jsp-montelanza-insolvency-liquidation/incident-register/index.html']
INDEX='assets/data/jsp-incident-subregister-v1.json'
DIGEST='archive/JSP_INCIDENT_DOCUMENT_DIGEST_05SEP2026.md'
REF='assets/data/jsp-incident-reference/'
SOURCE='2fc339c92ac9312d8e21b5c70db80a89c88c29c3'
EXPECTED_IMAGES={'assets/evidence/jsp-2017/borme-c-2017-7368-item-five.webp':('2d83e06b6962b6e87f99ec9264303d4448ccaea8ebe2e7bc6cabd2ce555c0ff3',(1025,116)),'assets/evidence/jsp-2017/borme-c-2017-7368-full-page.webp':('bc713c9d9e07c3f696f4583f15589df283f77bb00eb81fb47f749207022a1e8f',(893,1263))}
def norm(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def load(path):return json.loads((ROOT/path).read_text())
def require(ok,message):
    if not ok:raise AssertionError(message)
def check_index(d):
    require(d['incident_id']=='PD-JSP-INC-2017-01','incident identity')
    ids=d['canonical_members_existing_main']+d['canonical_members_candidate']
    require(len(ids)==len(set(ids))==111,'111 distinct identity references')
    require(len(d['queue'])==48 and len({q[0] for q in d['queue']})==48,'48 explicit queue dispositions')
    require(sum(q[1].startswith('Private property-source label withheld') for q in d['queue'])==16,'16 private labels remain withheld')
    require(len(d['document_index'])==64 and len({r[0] for r in d['document_index']})==64,'64 distinct document/reference entries')
    require(len(d['open_gap_groups'])==20,'20 gap groups')
    require(not d['direct_incident']['meeting_occurrence_verified'],'no invented held meeting')
    require(d['direct_incident']['request_received']=='2017-08-03' and d['direct_incident']['notice_published']=='2017-08-10','separate dates')
    require(d['direct_incident']['separate_agenda_items'][1]['source_percentage']=='MAJORITY_NOT_EXACT_PERCENTAGE','no bakery100% transferred to Explobeach')
    roster=d['shareholder_roster_2013'];require(roster['meeting_date']=='2013-06-27','2013 not 2009 roster')
    require(roster['total_company_shares']==220 and roster['represented_shares']==80 and sum(r['shares'] for r in roster['rows'])==80,'equity and represented denominators')
    require(roster['rows'][0]['shares']==59 and len(roster['rows'])==8,'eight shareholder entries, JSP59')
    require(d['title_routes'][0]['finca']=='8498' and 'NOT_PROTOCOL_2026' in d['title_routes'][0]['status'],'8498 distinct')
    require(all(t['status']=='CONDITIONAL_NOT_VERIFIED_COMPLETED' for t in d['title_routes'][1:]),'conditional title not completed')
    require(not d['primary_recheck']['raw_private_original_included'],'no raw private original')
    return ids
class Page(HTMLParser):
    def __init__(self,text):super().__init__();self.ids=[];self.targets=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for key in ['href','src']:
            if key in a:self.targets.append(a[key])
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',default='origin/main');ap.add_argument('--url');ap.add_argument('--output',default='/tmp/jsp-incident-qa');ap.add_argument('--wait-live',action='store_true');args=ap.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    result={'control':'PD-JSP-INCIDENT-SUBREGISTER-20260905','source_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'checks':[],'cases':[],'failures':[],'live_url':args.url,'boundary':'Bounded public reference reader, not a complete private-file publication or proof of allegations.'}
    server=None
    try:
        d=load(INDEX);ids=check_index(d);result['checks'].append('finite reference, attribution, privacy and title boundaries')
        for path in [INDEX,DIGEST]:
            original=subprocess.check_output(['git','show',SOURCE+':'+path],cwd=ROOT);require((ROOT/path).read_bytes()==original,'preserve source '+path)
        result['checks'].append('source index and full digest byte-preserved')
        manifest=load('assets/data/matter-identity-registry-v1.json');records={}
        for p in manifest['parts']:
            rows=load('assets/data/'+p['path'])['records'];require(len(rows)==p['count'],'canonical part count')
            for r in rows:require(r['id'] not in records,'canonical duplicate');records[r['id']]=r
        require(len(records)==manifest['counts']['total'],'global count preserved')
        reference=load(REF+'manifest.json');require(reference['is_canonical_admission'] is False,'reference cache not admission');candidates={}
        for item in reference['files']:
            b=(ROOT/REF/item['path']).read_bytes();gitsha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();require(gitsha==item['git_blob'],'pinned reference bytes '+item['path']);rows=json.loads(b)['records'];require(len(rows)==item['count'],'reference count')
            for r in rows:require(r['id'] not in candidates,'duplicate candidate');candidates[r['id']]=r
        require(len(candidates)==59,'59 source proposals')
        for i in ids:
            require(i in records or i in candidates,'unresolved reference '+i)
            if i in records and i in candidates:require(norm(records[i]['name'])==norm(candidates[i]['name']),'canonical conflict '+i)
        require(not any(p['path'].startswith('jsp-incident-reference/') for p in manifest['parts']),'cache must not be admitted as global part')
        result['counts']={'references':len(ids),'current_canonical':sum(i in records for i in ids),'candidate_references':sum(i not in records for i in ids),'queue':48,'documents':64,'gaps':20,'global':len(records)}
        result['checks'].append('all references resolve; current canonical names prevail; no new global admission')
        from PIL import Image
        for p,(expected,size) in EXPECTED_IMAGES.items():
            b=(ROOT/p).read_bytes();require(hashlib.sha256(b).hexdigest()==expected,'genuine image hash '+p)
            with Image.open(ROOT/p) as im:im.load();require(im.size==size,'image dimensions '+p)
        pdf=(ROOT/'assets/evidence/jsp-2017/BORME-C-2017-7368.pdf').read_bytes();require(hashlib.sha256(pdf).hexdigest()=='78df26e04206117a5dbebaa2fc337643841c58e85455905eb53f686d7500fad9','native source PDF bytes')
        result['checks'].append('source-derived images decode and native PDF matches original hash')
        pages=[]
        for route in ROUTES:
            text=(ROOT/route).read_text();p=Page(text);pages.append(p);require(len(p.ids)==len(set(p.ids)),'duplicate static anchor')
            require('PD-JSP-INC-2017-01' in text and '59/220' in text and '59/80' in text and '2013' in text,'critical static facts')
            require(not re.search(r'@monterecco|mail\.google|gmail\.com|sk-proj-|file_000000|message_id',text,re.I),'private data in new page')
            for target in p.targets:
                u=urlparse(target)
                if u.scheme or u.netloc:continue
                t=(ROOT/route).parent/unquote(u.path) if u.path else ROOT/route
                if t.is_dir():t=t/'index.html'
                require(t.exists(),'missing local resource '+target)
        require(set(pages[0].ids)==set(pages[1].ids),'bilingual anchor parity')
        result['checks'].append('static ES/EN, links, image targets and privacy')
        mutations=[lambda x:x['queue'].pop(),lambda x:x['document_index'].pop(),lambda x:x['direct_incident'].__setitem__('meeting_occurrence_verified',True),lambda x:x['shareholder_roster_2013'].__setitem__('represented_shares',220),lambda x:x['title_routes'][1].__setitem__('status','COMPLETED'),lambda x:x['primary_recheck'].__setitem__('raw_private_original_included',True)]
        for mutation in mutations:
            bad=copy.deepcopy(d);mutation(bad)
            try:check_index(bad)
            except AssertionError:pass
            else:raise AssertionError('negative test not rejected')
        result['negative_tests_rejected']=len(mutations)
        subprocess.run(['node','--check',str(ROOT/'assets/jsp-incident-reader.js')],check=True)
        if args.url:
            base=args.url.rstrip('/')+'/'
            bytepaths=ROUTES+[INDEX,DIGEST,'assets/jsp-incident-reader.js','assets/jsp-incident-reader.css',REF+'manifest.json']+[REF+i['path'] for i in reference['files']]+list(EXPECTED_IMAGES)+['assets/evidence/jsp-2017/BORME-C-2017-7368.pdf']
            result['live_byte_matches']=[]
            for p in bytepaths:
                expected=(ROOT/p).read_bytes();last='';attempts=60 if args.wait_live else 1
                for attempt in range(attempts):
                    try:
                        req=urllib.request.Request(base+p,headers={'User-Agent':'PorDerecho-Incident-Verification/1.0','Cache-Control':'no-cache'})
                        with urllib.request.urlopen(req,timeout=25) as r:actual=r.read()
                        if actual==expected:break
                        last='byte mismatch'
                    except Exception as e:last=str(e)
                    if attempt+1<attempts:time.sleep(5)
                else:raise AssertionError('live resource '+p+': '+last)
                result['live_byte_matches'].append({'path':p,'bytes':len(expected),'sha256':hashlib.sha256(expected).hexdigest()})
        else:
            mount=Path(tempfile.mkdtemp(prefix='jsp-incident-http-'));(mount/'por-derecho').symlink_to(ROOT,target_is_directory=True)
            class Quiet(http.server.SimpleHTTPRequestHandler):
                def log_message(self,*a):pass
            server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(mount)))
            threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/por-derecho/'
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            for engine in ['chromium','firefox','webkit']:
                browser=getattr(pw,engine).launch()
                for route in ROUTES:
                    for width,js in [(320,True),(390,True),(1440,True),(390,False)]:
                        context=browser.new_context(viewport={'width':width,'height':900},java_script_enabled=js);page=context.new_page();errors=[];bad_http=[]
                        page.on('pageerror',lambda e:errors.append(str(e)))
                        page.on('response',lambda r:bad_http.append((r.status,r.url)) if r.status>=400 else None)
                        response=page.goto(base+route,wait_until='networkidle',timeout=60000);require(response.status==200,'page HTTP')
                        if js:
                            page.wait_for_selector('#jsp-incident-reader[data-loaded="true"]',timeout=45000)
                            require(page.locator('#identities-table tbody tr').count()==111,'111 rendered references')
                            require(page.locator('#queue-table tbody tr').count()==48,'48 rendered dispositions')
                            require(page.locator('#documents-table tbody tr').count()==64,'64 rendered documents')
                            require(page.locator('#shareholders-table tbody tr').count()==8,'8 rendered shareholders')
                            require(page.locator('#gaps-table tbody tr').count()==20,'20 rendered gaps')
                            require(page.locator('#jsp-incident-reader').get_attribute('data-identity-conflicts')=='0','no identity conflicts')
                            broken=page.evaluate('''() => Array.from(document.querySelectorAll('a[href]')).filter(a=>a.hash&&a.origin===location.origin&&a.pathname===location.pathname&&!document.getElementById(decodeURIComponent(a.hash.slice(1)))).map(a=>a.href)''');require(not broken,'broken rendered anchors '+str(broken))
                            for image_id in ['incident-evidence-crop','incident-evidence-page']:
                                im=page.locator('#'+image_id);im.scroll_into_view_if_needed();require(im.evaluate('(i)=>i.complete&&i.naturalWidth>0'),'image actual decoding')
                            page.locator('#subject-search').fill('Molina');require(0<page.locator('#identities-table tbody tr:visible').count()<111,'search filter works');page.locator('#subject-search').fill('')
                            page.locator('#JSP-DOC-008').scroll_into_view_if_needed();require(page.locator('#JSP-DOC-008').is_visible(),'direct document anchor')
                        require(page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),'page horizontal overflow')
                        require(not errors and not bad_http,'browser resource errors '+str(errors+bad_http))
                        if engine=='chromium' and width in [390,1440] and js:
                            page.locator('#evidence-images').scroll_into_view_if_needed();page.screenshot(path=str(out/f'{route[:2]}-{width}-evidence.png'))
                            page.locator('#shareholders').scroll_into_view_if_needed();page.screenshot(path=str(out/f'{route[:2]}-{width}-shareholders.png'))
                        result['cases'].append({'engine':engine,'route':route,'width':width,'javascript':js,'result':'PASS','page_errors':0,'http_errors':0});context.close()
                browser.close()
        require(len(result['cases'])==24,'all24 browser cases completed')
        require(not subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip(),'validator must leave worktree unchanged')
        result['result']='PASS_LIVE_SCOPED' if args.url else 'PASS_CANDIDATE_SCOPED'
    except Exception as e:result['result']='FAIL';result['failures'].append(str(e))
    finally:
        if server:server.shutdown()
        (out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
    return int(result['result']=='FAIL')
if __name__=='__main__':raise SystemExit(main())

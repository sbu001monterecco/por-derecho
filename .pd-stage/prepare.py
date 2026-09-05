import base64, concurrent.futures, hashlib, json, lzma, os
from pathlib import Path
import subprocess, sys, urllib.request
BASE='adc8c87585609709caafdd90f03ffbb4a4687d83'
API='https://api.github.com/repos/sbu001monterecco/por-derecho/'
OUT=Path('/tmp/pd-preparation');OUT.mkdir(exist_ok=True)
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args):raise ValueError('No authenticated redirects')
def api(path,data=None):
    req=urllib.request.Request(API+path,data=None if data is None else json.dumps(data).encode(),headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':'application/json'})
    with urllib.request.build_opener(NoRedirect()).open(req,timeout=40) as r:return json.load(r)
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
assert api('git/ref/heads/main')['object']['sha']==BASE,'Main changed; reconcile source first'
binary=b''.join(Path('.pd-stage/part'+str(i)).read_bytes() for i in range(4))
assert hashlib.sha256(binary).hexdigest()=='3361b33f73eb1c7781ee55904915e2015f6d000d2641cba9fa7275feec9883b1','Package transfer failed'
package=json.loads(lzma.decompress(binary));manifest=json.loads(package['package-manifest.json'])
assert set(package)==set(manifest)|{'package-manifest.json'},'Unexpected package entry'
for path,digest in manifest.items():
    assert not Path(path).is_absolute() and '..' not in Path(path).parts and '\\' not in path
    assert hashlib.sha256(package[path].encode()).hexdigest()==digest
migration=package['_stage/apply_release_repair.py']
subprocess.run(['git','checkout','--detach',BASE],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
assert git('status','--porcelain')=='','Current main checkout was not clean'
for path in manifest:
    if path.startswith('_stage/'):continue
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(package[path])
exec(compile(migration,'<reviewed-current-main-migration>','exec'),{'__name__':'__main__'})
assert not subprocess.check_output(['git','diff',BASE,'--','assets/data','evidence','archive','publication-manifests']), 'Canonical evidence or immutable manifest unexpectedly changed'
changed=sorted(set(git('diff','--name-only').splitlines()+git('ls-files','--others','--exclude-standard').splitlines()))
changed=[p for p in changed if not p.startswith(('diagnostics/','artifacts/'))]
subprocess.run(['git','diff','--check'],check=True)
subprocess.run(['git','add','--',*changed],check=True)
subprocess.run(['git','-c','user.name=Release repair preparation','-c','user.email=ci@example.invalid','commit','-qm','Validate bounded current-main release controller repair'],check=True)
os.environ['GITHUB_BASE_SHA']=BASE;os.environ['GITHUB_HEAD_SHA']=git('rev-parse','HEAD')
results=[]
for command in [['python3','scripts/check_release_acceptance.py'],['python3','scripts/verify_ci_control_plane_browser.py']]:
    r=subprocess.run(command,capture_output=True,text=True,timeout=650)
    name=Path(command[1]).name;(OUT/(name+'.log')).write_text(r.stdout+r.stderr)
    results.append({'check':name,'exit':r.returncode,'tail':(r.stdout+r.stderr)[-10000:] if r.returncode else (r.stdout+r.stderr)[-500:]})
    print('RESULT',json.dumps(results[-1]),flush=True)
    if r.returncode:break
(OUT/'required-results.json').write_text(json.dumps(results,indent=2))
assert len(results)==2 and all(r['exit']==0 for r in results),'Candidate acceptance failed; no ready-candidate claim or blob promotion'
import functools,http.server,tempfile,threading
from playwright.sync_api import sync_playwright
with tempfile.TemporaryDirectory() as temp:
    directory=Path(temp);(directory/'por-derecho').symlink_to(Path.cwd(),target_is_directory=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(directory)))
    threading.Thread(target=server.serve_forever,daemon=True).start();rows=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch()
            for width in (390,1440):
                for js in (False,True):
                    context=browser.new_context(viewport={'width':width,'height':900},java_script_enabled=js,reduced_motion='reduce')
                    for path in changed:
                        if not path.endswith('/index.html'):continue
                        page=context.new_page();r=page.goto(f'http://127.0.0.1:{server.server_port}/por-derecho/'+path,wait_until='domcontentloaded')
                        assert r and r.status==200 and page.locator('main').count(),path
                        if 'meeting-point-357-2024-' in path:
                            for identity in ('PD-SP-O-0070','PD-SP-P-0087'):
                                a=page.locator('[data-caepr-id="'+identity+'"]').first
                                assert a.count()==1 and a.get_attribute('data-caret-state')=='CARET_CONFIRMED'
                            page.locator('#canonical-identity-current-20260905').scroll_into_view_if_needed(timeout=15000)
                            page.screenshot(path=str(OUT/(path.replace('/','_')+str(width)+str(js)+'.png')),animations='disabled')
                        rows.append({'path':path,'width':width,'javascript':js,'status':'PASS'});page.close()
                    context.close()
            browser.close()
    finally:server.shutdown()
    (OUT/'changed-pages-browser.json').write_text(json.dumps(rows,indent=2))
    print('CHANGED_PAGE_BROWSER_CASES',len(rows))
assert git('diff','--name-only')=='','Validators mutated source'
assert api('git/ref/heads/main')['object']['sha']==BASE,'Main advanced during acceptance'
def blob(path):
    return {'path':path,'mode':'100644','type':'blob','sha':api('git/blobs',{'content':Path(path).read_text(),'encoding':'utf-8'})['sha']}
elements=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(blob,changed))
receipt={'state':'ACCEPTED_SOURCE_NOT_MERGED','base':BASE,'base_tree':git('rev-parse',BASE+'^{tree}'),'elements':elements,'required_results':results,'changed_page_browser_cases':len(rows)}
(OUT/'candidate-tree.json').write_text(json.dumps(receipt,indent=2));print('CANDIDATE_TREE',json.dumps(receipt))

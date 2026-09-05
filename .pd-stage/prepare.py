"""Prepare only automation safeguards; specialist/privacy source changes stay queued."""
import concurrent.futures,hashlib,json,lzma,os,subprocess,sys,traceback,urllib.request
from pathlib import Path
BASE='adc8c87585609709caafdd90f03ffbb4a4687d83'
API='https://api.github.com/repos/sbu001monterecco/por-derecho/'
OUT=Path('/tmp/pd-preparation');OUT.mkdir(exist_ok=True)
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args):raise ValueError('Authenticated redirect prohibited')
def api(path,data=None):
 req=urllib.request.Request(API+path,data=None if data is None else json.dumps(data).encode(),headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':'application/json'})
 with urllib.request.build_opener(NoRedirect()).open(req,timeout=40) as r:return json.load(r)
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
assert api('git/ref/heads/main')['object']['sha']==BASE
binary=b''.join(Path('.pd-stage/part'+str(i)).read_bytes() for i in range(4))
assert hashlib.sha256(binary).hexdigest()=='3361b33f73eb1c7781ee55904915e2015f6d000d2641cba9fa7275feec9883b1'
package=json.loads(lzma.decompress(binary));manifest=json.loads(package['package-manifest.json'])
assert set(package)==set(manifest)|{'package-manifest.json'}
for path,digest in manifest.items():
 assert not Path(path).is_absolute() and '..' not in Path(path).parts and '\\' not in path
 assert hashlib.sha256(package[path].encode()).hexdigest()==digest
for row in json.loads(Path('.pd-stage/corrections.json').read_text()):
 if row['path']=='_stage/apply_release_repair.py':continue
 assert package[row['path']].count(row['old'])==1
 package[row['path']]=package[row['path']].replace(row['old'],row['new'],1)
selected=set(manifest)-{'_stage/apply_release_repair.py','scripts/check_cnmv_owned_contract.py'}
path='scripts/check_release_acceptance.py'
old="            ('specialist-regressions',[sys.executable,'scripts/compare_inherited_ci_diagnostics.py']),\n            ('cnmv-owned-records',[sys.executable,'scripts/check_cnmv_owned_contract.py','--check'])]"
assert package[path].count(old)==1
package[path]=package[path].replace(old,"            ('specialist-regressions',[sys.executable,'scripts/compare_inherited_ci_diagnostics.py'])]",1)
# Recover the first installation only when an owner requests the exact already-
# merged current revision and all candidate checks are independently successful.
path='scripts/pd_release_controller.py';old="    if operation=='claim':\n"
new="""    if operation=='recover' and state['phase'] in TERMINAL and pr['merged']:
        merge=pr['merge_commit_sha']
        if api.request('git/ref/heads/main')['object']['sha']!=merge:
            raise ValueError('Bootstrap recovery requires the exact current merged PR')
        checks=successful_checks(api,sha)
        parent=api.request('commits/'+merge)['parents'][0]['sha']
        state={'schema':'por-derecho.publication-runtime.v1','fence':state['fence']+1,
               'owner':task,'phase':'CLAIMED','pr':number,'base_sha':parent,'candidate_sha':sha,
               'run_id':int(os.environ['GITHUB_RUN_ID']),'claimed_at':utc_now(),
               'receipts':state.get('receipts',[]),'checkpoints':[],
               'recovery_basis':'Explicit owner recovery of exact completed merge; not a retrospective exclusive-lock claim.'}
        blob=api.save(state,blob)
        state=advance(state,'ACCEPTED',task,state['fence'],{'checks':checks,'bootstrap_recovery':True});blob=api.save(state,blob)
    if operation=='claim':
"""
assert package[path].count(old)==1;package[path]=package[path].replace(old,new,1)
status=json.loads(package['ops/RELEASE_AUTOMATION_STATUS.json'])
status['release_scope']='Automation-only: fail-closed aggregation, semantic finding comparison, canonical ID stability, cooperative atomic permits and recoverable exact deployment readback. No specialist page or source changes.'
status['open_work'].append({'id':'PD-SPECIALIST-SOURCE-CONTRACTS','priority':'P1','state':'SEPARATE_CURRENT_MAIN_RECONCILIATION_REQUIRED','closure':'CNMV managed sections, Alberto/Meeting Point current projections, canonical occurrence defects and historical observations must be fixed in separately validated source deltas, not by suppressing failures.'})
package['ops/RELEASE_AUTOMATION_STATUS.json']=json.dumps(status,indent=2)+'\n'
path='ops/PUBLICATION_CONTROLLER.md';s=package[path];a=s.index('CNMV verifies its own generated blocks');b=s.index('\n## Evidence, privacy and completion',a)
s=s[:a]+'''The generic owned-block and original-record preservation primitives are tested,
but the existing CNMV generator and specialist page contracts are deliberately
unchanged by this automation-only release. Their inherited findings remain
visible and separately owned. Source-backed page and history repairs must not be
combined with controller installation simply to obtain a green preparation run.
Existing IDs cannot be silently assigned to another entity. Source-linked
correction history permits reviewed identity correction, not automatic proof.

For first installation or a completed release lacking runtime state, an explicit
owner `recover` command can record and verify the exact current merged PR after
checking its exact-head successful acceptance. This is recovery evidence, not a
claim that an exclusive lock existed before installation.
'''+s[b:];package[path]=s
subprocess.run(['git','checkout','--detach',BASE],check=True,capture_output=True)
assert not git('status','--porcelain')
for path in sorted(selected):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(package[path])
def patch(path,old,new):
 p=Path(path);s=p.read_text();assert s.count(old)==1,(path,'reviewed source anchor drift');p.write_text(s.replace(old,new,1));selected.add(path)
path='scripts/validate_mission_critical_repo.py'
patch(path,'ALLOWED_WRITE = {','ALLOWED_WRITE = {\n    "publication-controller.yml": {"contents"},')
patch(path,'        if "contents" in writes:\n            error(f"{rel}: contents: write is prohibited for production workflows", errors)', '''        if "contents" in writes:
            if path.name != "publication-controller.yml":
                error(f"{rel}: contents: write is prohibited for production workflows", errors)
            else:
                for marker in ("issue_comment:", "github.event.issue.number == 1428", "author_association == 'OWNER'", "ref: main", "persist-credentials: false", "cancel-in-progress: false", "queue: max", "python3 scripts/pd_release_controller.py"):
                    if marker not in text:
                        error(f"{rel}: state-only controller lost guard: {marker}", errors)
                for forbidden in ("pull_request:", "pull_request_target:", "git push", "gh pr merge", "persist-credentials: true"):
                    if forbidden in text:
                        error(f"{rel}: unsafe state-only controller command: {forbidden}", errors)''')
path='ops/CURRENT_COLLABORATION_STATE.json';d=json.loads(Path(path).read_text());d['publication_controller']={'workflow':'.github/workflows/publication-controller.yml','manual':'ops/PUBLICATION_CONTROLLER.md','acceptance':'PD release acceptance','state_branch':'pd-publication-state','exclusive_server_enforcement':False,'rule':'Owner commands in existing issue1428; exact-SHA atomic permit, normal connector merge and explicit verification/recovery. Administrative enforcement remains pending.'};Path(path).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');selected.add(path)
path='CHATGPT_START_HERE.md';p=Path(path);p.write_text(p.read_text()+'''\n\n## Publication-controller recovery and actual acceptance
Read `ops/PUBLICATION_CONTROLLER.md` and `ops/RELEASE_AUTOMATION_STATUS.json` before publication. Preserve completed PR1468. Runtime state is `pd-publication-state` and Control Tower1428, not chat memory. A required failed, skipped, missing or unreadable result blocks acceptance. Inherited findings stay open; they are not whole-site health. Exact source, deployment, browser and public-byte evidence are different stages. Server-exclusive merge enforcement remains pending administrative readback. Preserve RAUDA PD-SP-O-0084; do not reassign it to Uría or replay old whole-file generators.
''');selected.add(path)
assert not subprocess.check_output(['git','diff',BASE,'--','en','es','assets','evidence','archive','publication-manifests']),'Source/public evidence unexpectedly changed'
subprocess.run(['git','diff','--check'],check=True)
subprocess.run(['git','add','--',*sorted(selected)],check=True)
subprocess.run(['git','-c','user.name=Release control preparation','-c','user.email=ci@example.invalid','commit','-qm','Validate finite automation controls without source publication'],check=True)
os.environ['GITHUB_BASE_SHA']=BASE;os.environ['GITHUB_HEAD_SHA']=git('rev-parse','HEAD')
results=[]
for script in ('scripts/check_release_acceptance.py','scripts/verify_ci_control_plane_browser.py'):
 proc=subprocess.run([sys.executable,script],capture_output=True,text=True,timeout=650)
 (OUT/(Path(script).name+'.log')).write_text(proc.stdout+proc.stderr)
 row={'check':script,'exit':proc.returncode,'tail':(proc.stdout+proc.stderr)[-10000:] if proc.returncode else (proc.stdout+proc.stderr)[-500:]};results.append(row);print('CHECK',json.dumps(row),flush=True)
 if proc.returncode:break
(OUT/'required-results.json').write_text(json.dumps(results,indent=2))
assert len(results)==2 and all(r['exit']==0 for r in results),'Candidate blocked: every required child must pass'
assert not git('diff','--name-only')
assert api('git/ref/heads/main')['object']['sha']==BASE,'Main advanced before publication'
def blob(path):return {'path':path,'mode':'100644','type':'blob','sha':api('git/blobs',{'content':Path(path).read_text(),'encoding':'utf-8'})['sha']}
elements=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(blob,sorted(selected)))
receipt={'state':'ACCEPTED_SOURCE_NOT_MERGED','base':BASE,'base_tree':git('rev-parse',BASE+'^{tree}'),'elements':elements,'required_results':results,'source_files_unchanged':True}
(OUT/'candidate-tree.json').write_text(json.dumps(receipt,indent=2));print('CANDIDATE_TREE',json.dumps(receipt))

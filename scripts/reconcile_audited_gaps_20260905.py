#!/usr/bin/env python3
"""Reconcile PD-CR continuity and diagnose remaining audited publication gaps.

Writes are confined to one declared worker and current-main baseline. No main
writes, history rewriting, private source inputs, inferred evidence closure, or
blanket import of old PRs. Existing dated snapshot and workflow repairs prevail.
"""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='adc8c87585609709caafdd90f03ffbb4a4687d83'
OLD='090a678ad53cd9216e673b0cfc643cd084e5286c'
REVIEW='c02eeef12c0eb53807f372ba46f9ab974dd74daa'
BRANCH='worker/audited-gaps-reconcile-20260905'
CONTROL='PD-AUDITED-GAPS-20260905-01'
HIST='publication-manifests/historic-proceedings-authority-reintegration-20260903.json'
CANON='assets/data/la-laguna-proceeding-pages-v1.json'
MANIFEST='ops/AUDITED_GAPS_RECONCILIATION_20260905.json'
EXCLUDE={HIST,'.github/workflows/cr-continuity-gapclosure.yml','.github/workflows/cuatrecasas-rauda-publication.yml'}

def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def at(ref,path):
 r=subprocess.run(['git','show',ref+':'+path],cwd=ROOT,capture_output=True)
 return r.stdout if r.returncode==0 else None
def digest(b):return hashlib.sha256(b).hexdigest()
def write(path,data):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data if isinstance(data,bytes) else data.encode())
def dump(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'

def prepare():
 assert git('branch','--show-current')==BRANCH,'Not the isolated worker'
 assert git('rev-parse','origin/main')==BASE,'Main advanced: reconcile anew, never overwrite'
 assert not (ROOT/MANIFEST).exists(),'Already prepared; use --check'
 paths=git('diff','--name-only',OLD,REVIEW).splitlines()
 assert len(paths)==25,'Reviewed source inventory changed'
 ledger=[]
 for path in paths:
  if path in EXCLUDE:continue
  old=at(OLD,path);candidate=at(REVIEW,path);current=at(BASE,path)
  assert candidate is not None,'No deletion is authorised'
  if current==old:result=candidate;method='UNCHANGED_MAIN_PATH_REVIEWED_DELTA'
  elif current==candidate:result=current;method='ALREADY_ON_MAIN'
  else:
   assert old is not None and current is not None,'Unexpected new-file collision: '+path
   with tempfile.TemporaryDirectory() as td:
    p=[Path(td)/str(i) for i in range(3)]
    for f,b in zip(p,[current,old,candidate]):f.write_bytes(b)
    r=subprocess.run(['git','merge-file','-p',*map(str,p)],capture_output=True)
    assert r.returncode==0,'Semantic overlap requires explicit review: '+path
    result=r.stdout;method='THREE_WAY_TEXT_RECONCILIATION_REQUIRES_DIFF_REVIEW'
  write(path,result);ledger.append({'path':path,'method':method,'prior_sha256':digest(current) if current is not None else None})
 # Preserve immutable historical manifest and schema-aware validation from #1468.
 assert (ROOT/HIST).read_bytes()==at(BASE,HIST)
 path='scripts/close_cr_continuity_20260905.py';s=(ROOT/path).read_text()
 start=s.index('\ndef apply():\n');end=s.index('\ndef check():\n',start)
 s=s[:start]+"\ndef apply():\n raise SystemExit('Historical writer retired. Reconcile the reviewed canonical delta on current main; do not replay this snapshot.')\n"+s[end:]
 old=" assert all(k in load(HIST) for k in ['expected_routes','current_state','owner']);assert load(MANIFEST)['completion_record']['pull_request']==1465"
 assert s.count(old)==1
 s=s.replace(old," assert (ROOT/HIST).read_bytes()==subprocess.check_output(['git','show','"+BASE+"'+':'+HIST],cwd=ROOT),'Historical source was changed';assert load(MANIFEST)['completion_record']['pull_request']==1465")
 write(path,s)
 # Dependency helper also becomes a read-only historical verifier. The next
 # authorised integration owns fresh source generation, never an old worker.
 path='scripts/complete_cr_continuity_dependencies.py';s=(ROOT/path).read_text()
 start=s.index('\ndef apply():\n');end=s.index('\ndef check():\n',start)
 s=s[:start]+"\ndef apply():\n raise SystemExit('Historical dependency writer retired; reconcile current canonical sources before reviewed integration.')\n"+s[end:]
 write(path,s)
 # Remove rejected schema rewrite from the active closure inventory, retain
 # an explicit disposition rather than silently erasing preparation history.
 d=json.loads((ROOT/CANON).read_text());c=d['continuity_closure']
 c['changed_files']=[p for p in c['changed_files'] if p not in EXCLUDE]
 c['superseding_integration']={'control_id':CONTROL,'current_main_base':BASE,'reviewed_source':REVIEW,'preceding_pr':1467,'historical_snapshot_edit':'EXCLUDED_SUPERSEDED_BY_1468_SCHEMA_AWARE_VALIDATION','workflow_policy':'CURRENT_MAIN_REPAIRS_PRESERVED_READ_ONLY_CHECKS_TO_BE_RECONCILED','state':'PREPARED_NOT_MERGED_OR_LIVE','no_merits_closure':True}
 write(CANON,dump(d))
 # Refresh only source fingerprints in the existing graph. Changing a node,
 # relationship, evidence status or coverage is an explicit stop.
 sys.path.insert(0,str(ROOT/'scripts'))
 import build_community_acta_authority_interconnectivity as graph
 target=ROOT/'assets/data/community-acta-authority-interconnectivity-v1.json'
 previous=json.loads(target.read_text());generated=graph.build()
 differences=[k for k in set(previous)|set(generated) if k!='sources' and previous.get(k)!=generated.get(k)]
 assert not differences,'Substantive graph change: '+str(differences)
 target.write_text(dump(generated))
 note='ops/CUATRECASAS_RAUDA_CONTINUITY_20260905.md'
 write(note,(ROOT/note).read_text()+f'\n## Current-main reconciliation {CONTROL}\n\nThe earlier proposal to add compatibility fields to `{HIST}` is superseded and excluded. PR #1468 fixed schema-aware historical validation. Its immutable snapshot, pinned/read-only workflow and current-count protections are preserved. Source candidate {REVIEW} is provenance only; this reconciliation starts at {BASE}. Old CR and dependency --apply entrypoints now refuse writes. The source checks are not a merge or live certificate. Seven substantive obligations remain open.\n')
 manifest={'schema':'por-derecho.audited-gaps-reconciliation.v1','control_id':CONTROL,'source_base':BASE,'reviewed_worker':REVIEW,'state':'PREPARED_NOT_MERGED_OR_LIVE','imported_files':ledger,'excluded_source_paths':sorted(EXCLUDE),'historical_snapshot_sha256':digest(at(BASE,HIST)),'graph_substantive_fields_changed':[],'outstanding_implementation':['Website dependency and link defects','Pending-identity queue federation','Media-link worker reconciliation','Current-main workflow/browser acceptance','Active-integrator merge and exact Pages readback'],'remaining_proof':'Seven CR and sixteen overlapping UCF categories remain source-gated;22 aggregate communications must not become synthetic events.','not_authorized':['Private-source publication','Email or court filing','Branch-protection changes','Unreviewed old PR bulk merge'],'publication_owner':'Active lane resolved from Control Tower #1428; this worker cannot independently race it.'}
 write(MANIFEST,dump(manifest))
 check()
 print('GENERATED_FILES',dump(sorted({r['path'] for r in ledger}|{MANIFEST})))

def check():
 d=json.loads((ROOT/MANIFEST).read_text());assert d['source_base']==BASE
 assert (ROOT/HIST).read_bytes()==at(BASE,HIST),'Historical snapshot changed'
 rows=json.loads((ROOT/CANON).read_text())['continuity_closure']
 assert len(rows['review_controls'])==58 and len(rows['production_obligations'])==7
 for path in ['scripts/close_cr_continuity_20260905.py','scripts/complete_cr_continuity_dependencies.py']:
  compile((ROOT/path).read_text(),path,'exec')
  r=subprocess.run([sys.executable,path,'--apply'],capture_output=True,text=True)
  assert r.returncode!=0 and 'retired' in r.stdout+r.stderr,'Historical writer unexpectedly enabled'
 commands=['scripts/close_cr_continuity_20260905.py','scripts/complete_cr_continuity_dependencies.py','scripts/validate_publication_integrity.py','scripts/validate_publication_integrity_v2.py','scripts/validate_operational_identity_registry.py','scripts/validate_legal_professional_register.py','scripts/validate_operational_truth.py']
 failures=[];results=[]
 for path in commands:
  args=['--check'] if 'cr_continuity' in path else []
  r=subprocess.run([sys.executable,path,*args],cwd=ROOT,capture_output=True,text=True)
  row={'command':[path,*args],'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr};results.append(row)
  print(dump(row))
  if r.returncode:failures.append(path)
 write('diagnostics/audited-gaps-source-checks.json',dump(results))
 assert not failures,'Acceptance failed: '+','.join(failures)
 print('AUDITED_GAPS_SOURCE_ACCEPTANCE_PASS')

def inspect():
 print('HEAD',git('rev-parse','HEAD'))
 for path in ['assets/convergence-graph.js','assets/convergence-graph.css','assets/site.css']:
  matches=git('log','--all','--format=%H','-5','--',path).splitlines()
  print('ASSET_HISTORY',path,matches)
 for p in sorted((ROOT/'assets').rglob('*')):
  if p.is_file() and re.search('converg|institutional-action|historic-arrecife',p.name,re.I):print('ASSET_CANDIDATE',p.relative_to(ROOT),p.stat().st_size)
 for path in ['en/unitary-criminal-hypothesis-2011-present/acosta-matos-convergence/index.html','assets/data/acosta-matos-functional-convergence-map-v2.json','scripts/validate_audience_experience.py']:
  s=(ROOT/path).read_text();print('SOURCE_INSPECT',path,s[:27000])
 q=json.loads((ROOT/'assets/data/matter-identity-operational-control-v1.json').read_text());print('QUEUE_KEYS',list(q));print('QUEUE_EXAMPLE',dump(q.get('exact_identity_queue',[])[:2]))
 index=json.loads((ROOT/'assets/data/matter-identity-registry-v1.json').read_text())
 for part in index['parts']:
  for row in json.loads((ROOT/'assets/data'/part['path']).read_text())['records']:
   if row['id'] in ['PD-SP-P-0138','PD-SP-P-0139','PD-SP-P-0143']:print('PENDING_IDENTITY',dump(row))

if __name__=='__main__':
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--prepare',action='store_true');g.add_argument('--check',action='store_true');g.add_argument('--inspect',action='store_true');a=p.parse_args()
 if a.prepare:prepare()
 elif a.check:check()
 else:inspect()

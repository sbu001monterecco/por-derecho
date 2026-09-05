#!/usr/bin/env python3
"""One-shot branch-only integration, removed from its own prepared candidate."""
from pathlib import Path
import concurrent.futures, json, os, re, shlex, subprocess, urllib.request
import yaml
ROOT=Path.cwd(); OUT=Path('/tmp/ci-recovery-candidate');OUT.mkdir(exist_ok=True)
BRANCH='integration/ci-rules-open-work-20260905'
BASE='090a678ad53cd9216e673b0cfc643cd084e5286c'
PREV='379fcd617d66a1d73c6d574403aa837395d05be5'
P1437='32b9dcb8fdc940f1ba8d824e87c59d47d855550b'
API='https://api.github.com/repos/sbu001monterecco/por-derecho/'
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
def get(path):
    req=urllib.request.Request(API+path,headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(req,timeout=35) as r:return json.load(r)
def write(path,text):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def patch(path,old,new):
    p=ROOT/path;t=p.read_text()
    if new in t:return
    assert t.count(old)==1,(path,'unexpected patch count',t.count(old))
    write(path,t.replace(old,new,1))
assert os.environ.get('GITHUB_REF')=='refs/heads/'+BRANCH
assert git('branch','--show-current')==BRANCH
assert get('git/ref/heads/main')['object']['sha']==BASE,'main advanced; reconcile before preparing'
subprocess.run(['git','fetch','--no-tags','origin',BASE,PREV,P1437],check=True,stdout=subprocess.DEVNULL)
subprocess.run(['git','fetch','--no-tags','origin','main:refs/remotes/origin/main'],check=True,stdout=subprocess.DEVNULL)
assert git('rev-parse','origin/main')==BASE
# Preserve current versions; apply predecessor changes only where every hunk fits.
workflow_names=['migrate-gc-hc-010-master-projection-04sep2026.yml','production-smoke-monitor.yml','reconcile-proceedings-smoke-20260903.yml','validate-aguiar-acosta-caret-event-proceeding.yml','validate-control-22-24.yml','validate-homepage-mission-critical-20260904.yml','validate-hotel-finca-title-system.yml','validate-multithread-collaboration-v2.yml','validate-unitary-criminal-source-register-live.yml','verify-source-of-funds-notice-live.yml']
for name in workflow_names:
    path='.github/workflows/'+name
    diff=subprocess.check_output(['git','diff','7c5c423091778cb610879039c967af4288708a34',P1437,'--',path])
    if not diff:continue
    subprocess.run(['git','apply','--check','-'],input=diff,check=True)
    subprocess.run(['git','apply','-'],input=diff,check=True)
for path in ['schemas/publication-state-manifest-v1.schema.json','scripts/loader_graph.py','scripts/validate_loader_graph.py']:
    assert not (ROOT/path).exists(),path
    write(path,subprocess.check_output(['git','show',PREV+':'+path],text=True))
# Retain current transition implementation; explicit publication schema is additive.
p='scripts/validate_publication_integrity_v2.py'
diff=subprocess.check_output(['git','diff','56761b5fa7a06579b3db563d859d75c65fb0a0b6',PREV,'--',p])
subprocess.run(['git','apply','--check','-'],input=diff,check=True);subprocess.run(['git','apply','-'],input=diff,check=True)
write('scripts/production_smoke_check_v2.py',subprocess.check_output(['git','show',P1437+':scripts/production_smoke_check_v2.py'],text=True))
# CLI backward compatibility: every existing legacy caller receives schema-aware
# validation; legacy library validation functions and all their thresholds remain.
p='scripts/validate_publication_integrity.py';t=(ROOT/p).read_text()
match=re.search(r'if __name__ == [\'\"]__main__[\'\"]:\s*\n(?:    .*\n?)+\s*$',t)
assert match,'legacy CLI entrypoint'
write(p,t[:match.start()]+"if __name__ == '__main__':\n    from validate_publication_integrity_v2 import main as schema_aware_main\n    raise SystemExit(schema_aware_main())\n")
# Do not silently treat an unavailable declared Git range as zero changed files.
t=(ROOT/p).read_text();begin=t.index('def changed_files()');end=t.index('\ndef load_manifests',begin)
block=t[begin:end];assert block.count('except Exception:\n        return []')==1
block=block.replace('except Exception:\n        return []','except Exception as exc:\n        raise RuntimeError("Cannot validate the declared Git comparison range") from exc')
write(p,t[:begin]+block+t[end:])
# Remove only completed, branch-writing preparation jobs. Validation/live jobs stay.
retired=[]
for name,job,nextjob in [('cnmv-interim-measures.yml','prepare-integration-only','validate-read-only'),('cuatrecasas-rauda-publication.yml','prepare-integration-only','validate-read-only'),('orion-architecture-clarification-20260905.yml','prepare','validate'),('orion-notice-register-preparation.yml','prepare','validate')]:
    p='.github/workflows/'+name;t=(ROOT/p).read_text();a=t.index('  '+job+':\n');b=t.index('  '+nextjob+':\n',a)
    removed=t[a:b];assert 'contents: write' in removed and 'git' in removed
    t=t[:a]+t[b:]
    if name.startswith('orion-architecture'):
        t=t.replace('    needs: prepare\n','').replace("    if: always() && (needs.prepare.result == 'success' || needs.prepare.result == 'skipped')\n",'')
        t=t.replace('${{ needs.prepare.outputs.head || github.sha }}','${{ github.event.pull_request.head.sha || github.sha }}')
    assert 'needs.prepare' not in t and 'contents: write' not in t
    write(p,t);retired.append({'workflow':p,'retired_job':job})
# Completed one-off notice migration remains available as read-only manual checks.
write('.github/workflows/orion-notice-projection-reconciliation.yml','''name: Orion notice dependent projection reconciliation
on:
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: orion-notice-projection-${{ github.ref }}
  cancel-in-progress: true
jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          persist-credentials: false
      - name: Verify already-integrated notice and Fiscalia projections without mutation
        run: |
          python scripts/build_fiscalia_proceedings_interconnectivity.py --check
          python scripts/validate_fiscalia_proceedings_interconnectivity.py
          python -m unittest -v scripts/test_build_fiscalia_proceedings_interconnectivity.py
          python scripts/prepare_orion_notice_register_20260905.py check
          python scripts/reconcile_institutional_communications.py --check
          python scripts/validate_institutional_communications.py
''')
retired.append({'workflow':'.github/workflows/orion-notice-projection-reconciliation.yml','retired_job':'reconcile writer; checks retained'})
# Unpinned recent actions are brought under the already-adopted immutable-pin rule.
pins={'actions/checkout@v4':'actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1','actions/setup-python@v5':'actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97','actions/setup-node@v4':'actions/setup-node@820762786026740c76f36085b0efc47a31fe5020','actions/upload-artifact@v4':'actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a'}
for p in sorted((ROOT/'.github/workflows').glob('*.yml')):
    if p.name.startswith('ci-control-plane-recovery'):continue
    t=p.read_text();old=t
    for a,b in pins.items():t=re.sub(r'(?<=uses: )'+re.escape(a)+r'\b',b,t)
    data=yaml.safe_load(t)
    if not isinstance(data,dict):continue
    if p.name=='validate-puzzle-continuity-20260905.yml' and 'permissions' not in data:
        t=t.replace('\njobs:\n','\npermissions:\n  contents: read\njobs:\n',1)
    jobs=data.get('jobs',{})
    for key,job in jobs.items():
        if isinstance(job,dict) and 'runs-on' in job and 'timeout-minutes' not in job:
            start=t.index('\n  '+str(key)+':\n'); end=t.find('\n  ',start+len('\n  '+str(key)+':\n'))
            # Insert next to the literal runner declaration, bounded to this job.
            rx=r'(\n  '+re.escape(str(key))+r':\n(?:(?!\n  [^ ]).)*?\n    runs-on:[^\n]+\n)'
            t,n=re.subn(rx,lambda m:m[1]+'    timeout-minutes: 15\n',t,count=1,flags=re.S);assert n==1,(p.name,key)
    if t!=old:p.write_text(t)
# Replay the four pending dependency changes on the exact current files.
deps={1254:'b7a929484e6fa673073f95474cda30db4127ecfb',1253:'d57d23aea0d0c75a83dec781063070bf7fbced97',1252:'26d959a2205e86be3383e6b86254404fae7e3198',1251:'b96a74a1cac0f56b1c38b01117689f0d8af29927'}
for number,head in deps.items():
    pr=get('pulls/'+str(number));assert pr['head']['sha']==head
    files=get('pulls/'+str(number)+'/files?per_page=100');assert all(f['filename'].startswith('.github/workflows/') for f in files)
    for f in files:
        t=(ROOT/f['filename']).read_text();found=False
        lines=f.get('patch','').splitlines()
        before=[line[1:] for line in lines if line.startswith('-') and not line.startswith('---') and 'uses:' in line]
        after=[line[1:] for line in lines if line.startswith('+') and not line.startswith('+++') and 'uses:' in line]
        assert len(before)==len(after) and before,(number,f['filename'])
        for a,b in zip(before,after):
            if b in t:continue
            assert a in t,(number,'dependency anchor absent',a)
            t=t.replace(a,b);found=True
        write(f['filename'],t)
# Preserve all canonical identities: only display/state derivatives are generated.
proc=subprocess.run(['python3','scripts/reconcile_identity_registry_projections.py','--write'],capture_output=True,text=True)
print('PROJECTION_PREPARATION',proc.returncode,proc.stdout,proc.stderr)
# A date is current when it equals the canonical source, not a frozen release date.
p='scripts/validate_dp3205_2014_publication.py'
diff=subprocess.check_output(['git','diff','7c5c423091778cb610879039c967af4288708a34',P1437,'--',p])
subprocess.run(['git','apply','--check','-'],input=diff,check=True);subprocess.run(['git','apply','-'],input=diff,check=True)
# Inspect the absent methodology target; only one known live source route is selected.
method=[str(p.relative_to(ROOT)) for p in (ROOT/'es').rglob('index.html') if any(x in str(p.relative_to(ROOT)) for x in ['metodolog','methodolog'])]
print('METHODOLOGY_CANDIDATES',json.dumps(method))
# Check the whole core gate, not only the originally reported failures.
checks=['validate_repository_preservation.py','validate_publication_integrity_v2.py','validate_audience_experience.py','validate_ac_community_de_facto_administration.py','validate_insolvency_perimeter_language.py','validate_operational_items.py','validate_mission_critical_repo.py','validate_sent_email_link_continuity.py','validate_dp3205_2014_publication.py','validate_loader_graph.py','reconcile_identity_registry_projections.py']
# Remove bootstrap-only files from the candidate; history remains recoverable.
(ROOT/'.github/workflows/ci-control-plane-recovery-20260905.yml').unlink()
(ROOT/'.github/prepare-ci-recovery-20260905.py').unlink()
# Expose concise failure locations plus source context, without dumping whole CI logs.
def runcheck(script):
    p=subprocess.run(['python3','scripts/'+script],capture_output=True,text=True,timeout=150)
    text=p.stdout+p.stderr;(OUT/(script+'.log')).write_text(text)
    return {'script':script,'exit':p.returncode,'tail':text[-4500:] if p.returncode else text[-450:]}
results=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(runcheck,checks))
print('CORE_RESULTS',json.dumps(results));(OUT/'core-results.json').write_text(json.dumps(results,indent=2))
print('RETIRED_WRITERS',json.dumps(retired))
# Inventory the concrete main failures for the next repair pass.
runs=get('actions/runs?head_sha='+BASE+'&per_page=100')['workflow_runs']
failed=[r for r in runs if r['conclusion']=='failure']
def inspect_failure(run):
    rows=[]
    for job in get('actions/runs/'+str(run['id'])+'/jobs?per_page=100')['jobs']:
        if job['conclusion']!='failure':continue
        req=urllib.request.Request(API+'actions/jobs/'+str(job['id'])+'/logs',headers={'Authorization':'Bearer '+os.environ['GH_TOKEN']})
        try:
            with urllib.request.urlopen(req,timeout=45) as r:text=r.read().decode('utf-8','replace')
            (OUT/(str(job['id'])+'.log')).write_text(text)
            lines=[re.sub(r'^\S+Z\s*','',x) for x in text.splitlines()]
            candidates=[x for x in lines if ('##[error]' in x or x.startswith('- ') or x.startswith(' - ') or 'AssertionError' in x or 'missing marker' in x or 'global_loader' in x) and '\x1b' not in x]
            rows.append({'job':job['id'],'failed_steps':[s['name'] for s in job.get('steps',[]) if s.get('conclusion')=='failure'],'errors':candidates[-12:]})
        except Exception as e:rows.append({'job':job['id'],'read_error':str(e)})
    return {'run':run['id'],'workflow':run['path'],'name':run['name'],'jobs':rows}
failures=list(concurrent.futures.ThreadPoolExecutor(max_workers=5).map(inspect_failure,failed))
(OUT/'main-failures.json').write_text(json.dumps(failures,indent=2));print('MAIN_FAILURES',json.dumps(failures))
# Draft changes only: no merge/deployment/green certification occurs here.
subprocess.run(['git','diff','--check'],check=True)
changed=git('diff','--name-only').splitlines()+git('ls-files','--others','--exclude-standard').splitlines()
allowed_exact={'scripts/reconcile_identity_registry_projections.py','scripts/validate_publication_integrity.py','scripts/validate_publication_integrity_v2.py','scripts/loader_graph.py','scripts/validate_loader_graph.py','scripts/production_smoke_check_v2.py','scripts/validate_dp3205_2014_publication.py','schemas/publication-state-manifest-v1.schema.json','ops/CURRENT_UNITARY_STATE.json','en/matter-identity-registry/index.html','es/registro-identidad-materia/index.html','.github/prepare-ci-recovery-20260905.py'}
assert all(p in allowed_exact or p.startswith('.github/workflows/') for p in changed),changed
assert not git('diff',BASE,'--','assets/data','publication-manifests'), 'canonical source or immutable manifest changed'
assert get('git/ref/heads/main')['object']['sha']==BASE,'main advanced while preparing'
subprocess.run(['git','add','--',*changed],check=True)
subprocess.run(['git','-c','user.name=Por Derecho integration','-c','user.email=41898282+github-actions[bot]@users.noreply.github.com','commit','-m','Prepare current-main CI rules recovery from #1412 #1437 and four dependency deltas'],check=True,stdout=subprocess.DEVNULL)
subprocess.run(['git','push','origin','HEAD:refs/heads/'+BRANCH],check=True,stdout=subprocess.DEVNULL)
print('PREPARED_NOT_DEPLOYED',git('rev-parse','HEAD'),json.dumps(sorted(set(changed))))

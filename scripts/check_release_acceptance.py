#!/usr/bin/env python3
"""One explicit acceptance result: unknown/missing/failed required checks block."""
from __future__ import annotations
import json, os
from pathlib import Path
import subprocess, sys
from pd_release_contract import acceptance, identity_records, identity_collisions, run_check
ROOT=Path(__file__).resolve().parents[1]

def main():
    out=Path('/tmp/pd-release-acceptance');out.mkdir(exist_ok=True)
    base=os.environ.get('GITHUB_BASE_SHA') or subprocess.check_output(['git','rev-parse','HEAD^'],cwd=ROOT,text=True).strip()
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    checks=[('release-contract-tests',[sys.executable,'-m','unittest','discover','-s','scripts','-p','test_pd_release_contract.py','-v']),
            ('current-ci-contracts',[sys.executable,'scripts/validate_ci_control_plane.py']),
            ('specialist-regressions',[sys.executable,'scripts/compare_inherited_ci_diagnostics.py'])]
    results=[]
    try:
        errors=identity_collisions(identity_records(ROOT,base),identity_records(ROOT))
        results.append({'check':'canonical-identity-stability','completed':True,'exit':1 if errors else 0,'status':'FAIL' if errors else 'PASS','findings':errors})
    except Exception as error:
        results.append({'check':'canonical-identity-stability','completed':False,'exit':1,'status':'ERROR','error':str(error)})
    for name,command in checks:
        row=run_check(name,command,ROOT,timeout=360)
        (out/(name+'.log')).write_text(row.get('stdout','')+row.get('stderr',''))
        print(name,row['status'],flush=True)
        if row['exit']:print((row.get('stdout','')+row.get('stderr',''))[-6000:],flush=True)
        results.append({k:v for k,v in row.items() if k not in ('stdout','stderr')})
    report=acceptance(results,['canonical-identity-stability',*[x[0] for x in checks]])
    report.update(base_sha=base,source_sha=head,scope='Code/source acceptance only. Deployed host, administrative enforcement and case merits remain separate.')
    (out/'acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PD RELEASE ACCEPTANCE:',report['state'])
    return 0 if report['accepted'] else 1
if __name__=='__main__':raise SystemExit(main())

#!/usr/bin/env python3
"""Reproduce remaining specialist diagnostics on the base and reviewed candidate.

An identical inherited failure is recorded, not suppressed in its own workflow.
A new or changed failure blocks this comparative acceptance. Never change
source, historical attestations or the underlying specialist checks here.
"""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
COMMANDS=(
 ('validate_concurso36_complete_record_v2.py',),
 ('build_alberto_meeting_point_project_links.py','--check'),
 ('validate_alberto_meeting_point_cross_proceeding.py',),
 ('validate_alberto_meeting_point_first_hop_caret.py',),
 ('validate_current_reverse_engineered_digest.py',),
 ('validate_caret_public_surface.py',),
 ('build_cnmv_interim_measures_20260905.py','--check'),
 ('validate_fti_meeting_point_asset_transaction_monitor.py',),
 ('validate_fti_meeting_point_ricpe_continuity.py',),
 ('validate_fti_meeting_point_professional_institutional_caret.py',),
 ('audit_master_proceedings_publication.py',),
 ('audit_counsel_procurador_governance.py',),
)


def main() -> int:
    base=os.getenv('GITHUB_BASE_SHA') or '090a678ad53cd9216e673b0cfc643cd084e5286c'
    if not re.fullmatch(r'[a-f0-9]{40}',base) or base=='0'*40:
        raise ValueError('An exact resolvable comparison base is required')
    subprocess.run(['git','cat-file','-e',base+'^{commit}'],cwd=ROOT,check=True)
    output=Path('/tmp/ci-control-plane/specialist-comparison');output.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        baseline=Path(td)/'base'
        subprocess.run(['git','worktree','add','--detach',str(baseline),base],cwd=ROOT,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            def compare(command):
                row={'command':list(command)}
                for label,cwd in (('base',baseline),('candidate',ROOT)):
                    env=dict(os.environ)
                    # These commands validate a standalone source tree, not the PR diff.
                    env.pop('GITHUB_BASE_SHA',None);env.pop('GITHUB_HEAD_SHA',None)
                    proc=subprocess.run([sys.executable,'scripts/'+command[0],*command[1:]],cwd=cwd,env=env,capture_output=True,text=True,timeout=150)
                    text=(proc.stdout+proc.stderr).replace(str(cwd),'<ROOT>')
                    (output/(label+'-'+command[0]+'.log')).write_text(text)
                    row[label]={'exit':proc.returncode,'output':text}
                row['no_new_failure']=row['candidate']['exit']==0 or row['base']==row['candidate']
                row['status']='PASS' if row['candidate']['exit']==0 else ('INHERITED_FAILURE_UNCHANGED' if row['no_new_failure'] else 'CHANGED_OR_NEW_FAILURE')
                return row
            rows=list(ThreadPoolExecutor(max_workers=4).map(compare,COMMANDS))
            (output/'comparison.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
            for row in rows:
                print(row['status'],row['command'][0])
                if row['candidate']['exit']:
                    print(row['candidate']['output'][-1700:])
            good=all(r['no_new_failure'] for r in rows)
            print('SPECIALIST COMPARISON:', 'NO_NEW_FAILURE' if good else 'BLOCKED')
            return 0 if good else 1
        finally:
            subprocess.run(['git','worktree','remove','--force',str(baseline)],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)

if __name__=='__main__':raise SystemExit(main())

#!/usr/bin/env python3
"""Compare typed/explicit findings. Unknown output and all new defects fail closed."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from pd_release_contract import compare_results, run_check
ROOT = Path(__file__).resolve().parents[1]
COMMANDS = (
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
    base = os.getenv('GITHUB_BASE_SHA') or subprocess.check_output(['git','rev-parse','HEAD^'],cwd=ROOT,text=True).strip()
    if not re.fullmatch(r'[a-f0-9]{40}', base) or base == '0'*40:
        raise ValueError('An exact comparison base is required')
    subprocess.run(['git','cat-file','-e',base+'^{commit}'],cwd=ROOT,check=True)
    out = Path('/tmp/ci-control-plane/specialist-comparison'); out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as directory:
        baseline = Path(directory)/'base'
        subprocess.run(['git','worktree','add','--detach',str(baseline),base],cwd=ROOT,check=True,capture_output=True)
        try:
            def compare(command):
                row = {'command': list(command)}
                for label, cwd in (('base',baseline),('candidate',ROOT)):
                    env = dict(os.environ)
                    env.pop('GITHUB_BASE_SHA',None); env.pop('GITHUB_HEAD_SHA',None)
                    result = run_check(command[0], [sys.executable,'scripts/'+command[0],*command[1:]],cwd,150,env)
                    for key in ('stdout','stderr'):
                        result[key] = result[key].replace(str(cwd),'<ROOT>')
                    (out/(label+'-'+command[0]+'.log')).write_text(result['stdout']+result['stderr'])
                    row[label] = result
                row.update(compare_results(row['base'],row['candidate']))
                return row
            rows = list(ThreadPoolExecutor(max_workers=4).map(compare,COMMANDS))
            (out/'comparison.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
            for row in rows:
                print(row['status'],row['command'][0])
                for error in row['new']:
                    print('NEW', error['detail'])
                if not row['no_new_failure']:
                    print((row['candidate']['stdout']+row['candidate']['stderr'])[-2000:])
            ok = all(r['no_new_failure'] for r in rows)
            print('SPECIALIST COMPARISON:', 'NO_NEW_FAILURE' if ok else 'BLOCKED')
            return 0 if ok else 1
        finally:
            subprocess.run(['git','worktree','remove','--force',str(baseline)],cwd=ROOT,check=True,capture_output=True)

if __name__ == '__main__':
    raise SystemExit(main())

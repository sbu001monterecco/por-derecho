#!/usr/bin/env python3
"""Run the finite CI recovery acceptance suite without altering repository state."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
CHECKS=(
    'validate_repository_preservation.py', 'validate_publication_integrity_v2.py',
    'validate_audience_experience.py', 'validate_ac_community_de_facto_administration.py',
    'validate_insolvency_perimeter_language.py', 'validate_operational_items.py',
    'validate_mission_critical_repo.py', 'validate_sent_email_link_continuity.py',
    'validate_dp3205_2014_publication.py', 'validate_loader_graph.py',
    'reconcile_identity_registry_projections.py', 'validate_operational_truth.py',
    'validate_unitary_control_plane.py', 'validate_canonical_home_search.py',
    'validate_jdam_architecture_colegios.py', 'validate_san_telmo_attribution_rendered.py',
    'validate_cuatrecasas_linkedin_interlink.py', 'audit_proceedings_interconnectivity_map.py',
)


def governance_checks() -> list[str]:
    failures=[]
    retired={
        'cnmv-interim-measures.yml':'prepare-integration-only:',
        'cuatrecasas-rauda-publication.yml':'prepare-integration-only:',
        'orion-architecture-clarification-20260905.yml':'  prepare:',
        'orion-notice-register-preparation.yml':'  prepare:',
    }
    for name,marker in retired.items():
        text=(ROOT/'.github/workflows'/name).read_text()
        if marker in text or 'contents: write' in text:
            failures.append(name+': completed preparation writer was reintroduced')
    monitor=(ROOT/'.github/workflows/production-smoke-monitor.yml').read_text()
    for marker in ('workflow_run:', "['pages build and deployment']", 'pd-production-failure:', 'fingerprint', "github.event.pull_request.number || 'production'", '307309396', 'Preserve a failing status'):
        if marker not in monitor:failures.append('Production monitor lost contract: '+marker)
    if '\n  push:' in monitor:failures.append('Production monitor must not test an unbuilt main push')
    for path in ('.github/ci-final-edits.json','.github/workflows/prepare-ci-rules-finish.yml','.github/prepare-ci-recovery-20260905.py','.github/workflows/ci-control-plane-recovery-20260905.yml'):
        if (ROOT/path).exists():failures.append('Transient preparation file retained: '+path)
    return failures


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default='/tmp/ci-control-plane')
    args=parser.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    def run(command):
        name=Path(command[-1]).name if command[-1].endswith('.py') else 'negative-regressions'
        try:
            proc=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=180)
            text=proc.stdout+proc.stderr;(out/(name+'.log')).write_text(text)
            return {'check':name,'exit':proc.returncode,'status':'PASS' if proc.returncode==0 else 'FAIL','tail':text[-1700:] if proc.returncode else text[-200:]}
        except subprocess.TimeoutExpired:
            return {'check':name,'exit':124,'status':'FAIL','tail':'Bounded validation timeout'}
    commands=[[sys.executable,'scripts/'+s] for s in CHECKS]
    commands.append([sys.executable,'-m','unittest','discover','-s','scripts','-p','test_ci_control_plane.py','-v'])
    results=list(ThreadPoolExecutor(max_workers=4).map(run,commands))
    governance=governance_checks()
    payload={'schema':'por-derecho.ci-control-plane-audit.v1','source_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'base_sha':os.getenv('GITHUB_BASE_SHA'),'checks':results,'governance_errors':governance,'ok':not governance and all(r['exit']==0 for r in results)}
    (out/'summary.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
    for r in results:
        print(r['status'],r['check'])
        if r['exit']:print(r['tail'])
    for error in governance:print('FAIL',error)
    print('CI CONTROL PLANE:', 'PASS' if payload['ok'] else 'FAIL')
    return 0 if payload['ok'] else 1

if __name__=='__main__':raise SystemExit(main())

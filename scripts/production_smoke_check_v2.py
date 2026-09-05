#!/usr/bin/env python3
"""Keep all legacy route tests; verify the real loader graph and deployed hashes.

The reviewed checkout is the expected deployment. A renamed/delegated root is
valid only when all required modules remain reachable and every file in their
source paths is served byte-for-byte. Source reachability does not replace the
separate browser execution tests.
"""
from __future__ import annotations
from copy import deepcopy
import hashlib
from pathlib import Path
from typing import Any
import production_smoke_check as legacy
from loader_graph import ROOT, find_loader_path

REQUIRED_LOADERS = (
    'assets/site-pre-treasury-154-hq-20260828.js',
    'assets/treasury-154-hq-visual-20260828.js',
    'assets/calificacion-criminal-misuse-thesis-20260824.js',
    'assets/asset-recovery-preservation-20260821.js',
    'assets/cam-direct-instruction-shadow-admin-judicial-omission-20260823.js',
    'assets/concurso36-caret-incident-overlay-20260829.js',
)
ORIGINAL_CHECKS = deepcopy(legacy.CHECKS)
ORIGINAL_ONE_PASS = legacy.one_pass


def loader_contract(root: Path = ROOT, targets: tuple[str, ...] = REQUIRED_LOADERS) -> dict[str, dict[str, Any]]:
    nodes: dict[str, dict[str, Any]] = {}
    for target in targets:
        chain = find_loader_path('assets/site.js', target, root=root)
        if chain is None:
            raise ValueError('Required loader is unreachable from assets/site.js: '+target)
        for rel in chain:
            body = (root / rel).read_bytes()
            if not body:
                raise ValueError('Empty loader dependency: '+rel)
            nodes[rel] = {'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body)}
    return nodes


def verify_hashes(records: list[dict[str, Any]], expected: dict[str, dict[str, Any]]) -> tuple[bool, list[dict[str, Any]]]:
    seen: set[str] = set()
    for row in records:
        rel = row['path']
        if rel not in expected:
            continue
        seen.add(rel)
        row['expected_sha256'] = expected[rel]['sha256']
        row['expected_bytes'] = expected[rel]['bytes']
        row['source_hash_match'] = row.get('sha256') == expected[rel]['sha256'] and row.get('bytes') == expected[rel]['bytes']
        row['ok'] = bool(row.get('ok')) and row['source_hash_match']
        if not row['source_hash_match']:
            row['error'] = row.get('error') or 'Deployed loader differs from the reviewed checkout'
    for rel in sorted(set(expected) - seen):
        records.append({'path': rel, 'kind': 'loader_dependency', 'ok': False, 'error': 'Required loader was not checked'})
    return all(row.get('ok', False) for row in records), records


def apply_current_loader_contract(root: Path = ROOT) -> None:
    expected = loader_contract(root)
    checks = deepcopy(ORIGINAL_CHECKS)
    roots = [row for row in checks if row.get('kind') == 'global_loader']
    if len(roots) != 1 or roots[0]['path'] != 'assets/site.js':
        raise RuntimeError('Legacy smoke must declare exactly one global-loader contract')
    # No obsolete implementation-specific substring is substituted for another.
    # Exact file hashes below are a stronger contract than historic marker text.
    roots[0].update(kind='global_loader', markers=[], min_bytes=1)
    present = {row['path'] for row in checks}
    for rel in sorted(expected):
        if rel not in present:
            checks.append({'path': rel, 'kind': 'loader_dependency', 'markers': [], 'min_bytes': 1})
    legacy.CHECKS = checks
    def current_pass(base_url: str, timeout: int, attempt: int):
        _, rows = ORIGINAL_ONE_PASS(base_url, timeout, attempt)
        return verify_hashes(rows, expected)
    legacy.one_pass = current_pass


def verified_live_loader_text(base_url: str, timeout: int = 20, root: Path = ROOT) -> str:
    """Return only hash-verified deployed chain text for legacy live contracts."""
    from urllib.parse import urljoin
    expected = loader_contract(root)
    texts = []
    for rel, contract in expected.items():
        response = legacy.fetch(urljoin(base_url.rstrip('/')+'/', rel)+'?pd_loader_hash='+contract['sha256'][:16], timeout)
        if response['status'] != 200 or response['sha256'] != contract['sha256'] or response['bytes'] != contract['bytes']:
            raise ValueError('Deployed loader-chain integrity failed: '+rel)
        texts.append(response['text'])
    return '\n'.join(texts)


def production_trigger_errors(workflow_text: str) -> list[str]:
    """Validate post-deployment monitoring and PR path coverage separately."""
    import fnmatch
    import re
    errors = []
    for marker in ("workflow_run:", "['pages build and deployment']", "types: [completed]", "branches: [main]", "workflow_run.conclusion == 'success'", "307309396", "deployed.head_sha"):
        if marker not in workflow_text:
            errors.append('Production deployment trigger lost: '+marker)
    if re.search(r'^  push:', workflow_text, re.MULTILINE):
        errors.append('Production monitoring must follow successful Pages, not an unbuilt push')
    block = re.search(r'^  pull_request:\n(.*?)(?=^  [a-z_]+:|\Z)', workflow_text, re.MULTILINE|re.DOTALL)
    patterns = re.findall(r'^\s+-\s+[\'\"]([^\'\"]+)[\'\"]\s*$', block[1], re.MULTILINE) if block else []
    required = ('deployment-probes/mission-critical-hardening-20260818.json', 'assets/site.js', 'en/index.html', 'es/index.html', 'es/cnmv-ricpe-verificacion/index.html', 'en/cam-creditor-control-shadow-administration-judicial-omission/index.html', 'es/control-acreedor-cam-administracion-hecho-omision-judicial/index.html')
    for path in required:
        if not any(fnmatch.fnmatchcase(path,p) for p in patterns if not p.startswith('!')) or any(fnmatch.fnmatchcase(path,p[1:]) for p in patterns if p.startswith('!')):
            errors.append('Production smoke PR coverage omits '+path)
    return errors


def main() -> int:
    try:
        apply_current_loader_contract()
    except (OSError, ValueError, RuntimeError) as exc:
        print('PRODUCTION LOADER CONTRACT: FAIL —', exc)
        return 1
    return legacy.main()

if __name__ == '__main__':
    raise SystemExit(main())

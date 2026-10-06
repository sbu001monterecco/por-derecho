#!/usr/bin/env python3
"""Verify the original JSP release AND its incorporated additive successor.

The original validator, release date, denominator and source checks remain intact.
Historical QA runs in a temporary local clone against the original parent, never
by changing origin/main in the candidate checkout. Required job identity stays
unchanged. Failure of either phase fails the job. No network, credentials, tracked
file writes, ruleset changes or deployment are involved.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import unquote, urlparse

from validate_jsp_successor_preservation import GitReader, PARENT, RELEASE, audit, registry, require


def validate_current_links(root, candidate_ids):
    # Reuse the unchanged release parser; frozen-object check precedes this import.
    spec = importlib.util.spec_from_file_location('jsp_original', root / 'scripts/validate_jsp_2017_dossier.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sources = {s['id'] for s in json.loads((root / 'assets/data/jsp-2017-source-relationship-register.json').read_text())['sources']}
    pages, checked = {}, 0
    for route in module.ROUTES:
        path = root / route
        page = module.Page(path.read_text(encoding='utf-8'))
        pages[route] = page
        require(len(page.ids) == len(set(page.ids)), 'Duplicate current page anchor')
        require(page.lang == route[:2], 'Wrong current page language')
        for href in page.links:
            url = urlparse(href)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= 'index.html'
            require(target.exists(), 'Missing current JSP link target: ' + route + ' -> ' + href)
            if not url.path and url.fragment:
                require(url.fragment in page.ids or url.fragment in sources or url.fragment in candidate_ids, 'Missing current JSP anchor: ' + href)
            checked += 1
    require(set(pages[module.ROUTES[0]].ids) == set(pages[module.ROUTES[1]].ids), 'Current bilingual anchor mismatch')
    subprocess.run(['node', '--check', str(root / 'assets/jsp-dossier-2017.js')], check=True)
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True)
    parser.add_argument('--output', default='jsp-qa')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    out = (root / args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    report = {'result': 'FAIL', 'mode': 'HISTORICAL_RELEASE_AND_ADDITIVE_SUCCESSOR'}
    reader = GitReader(root)
    try:
        base = reader.git('rev-parse', 'refs/remotes/origin/main').decode().strip()
        candidate = reader.git('rev-parse', 'HEAD').decode().strip()
        report.update(base=base, candidate=candidate, requested_base=args.base)
        for older, newer in ((PARENT, RELEASE), (RELEASE, base), (args.base, base), (base, candidate)):
            reader.ancestor(older, newer)
        report['successor'] = audit(reader, base, candidate)
        # --shared borrows local objects read-only. Clone refs/index/worktree are
        # isolated; only this disposable clone gets the historical origin/main.
        with tempfile.TemporaryDirectory(prefix='jsp-historical-') as temp:
            historical = Path(temp) / 'checkout'
            subprocess.run(['git', 'clone', '--shared', '--no-checkout', '--quiet', str(root), str(historical)], check=True)
            subprocess.run(['git', '-C', str(historical), 'checkout', '--quiet', '--detach', RELEASE], check=True)
            subprocess.run(['git', '-C', str(historical), 'update-ref', 'refs/remotes/origin/main', PARENT], check=True)
            subprocess.run(['python3', 'scripts/validate_jsp_2017_dossier.py', '--base', PARENT, '--output', str(out / 'historical-release')], cwd=historical, check=True)
        old = json.loads((out / 'historical-release/report.json').read_text())
        require(old['candidate'] == RELEASE and old['base'] == PARENT and old['result'] == 'PASS_SCOPED_ONLY', 'Historical report identity/result mismatch')
        report['historical'] = {'release': RELEASE, 'parent': PARENT, 'result': old['result'], 'checks': len(old['checks']), 'counts': old['actual_counts']}
        _, _, identities = registry(reader, candidate)
        report['current_local_links_checked'] = validate_current_links(root, set(identities))
        subprocess.run(['python3', 'scripts/reconcile_identity_registry_projections.py', '--check'], cwd=root, check=True)
        subprocess.run(['python3', 'tests/test_jsp_successor_preservation.py', '--base', base], cwd=root, check=True)
        require(reader.git('rev-parse', 'refs/remotes/origin/main').decode().strip() == base, 'Candidate origin/main moved during validation')
        require(reader.git('rev-parse', 'HEAD').decode().strip() == candidate, 'Candidate HEAD moved during validation')
        subprocess.run(['git', 'diff', '--exit-code'], cwd=root, check=True)
        subprocess.run(['git', 'diff', '--cached', '--exit-code'], cwd=root, check=True)
        report['result'] = 'PASS_SCOPED_RELEASE_AND_SUCCESSOR'
        report['limitations'] = ['No substantive identity/source admission approval', 'No independent binary custody, browser, deployment or whole-repository certification']
        return 0
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as exc:
        report['error'] = str(exc)
        return 1
    finally:
        (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    raise SystemExit(main())

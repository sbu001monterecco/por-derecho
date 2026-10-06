#!/usr/bin/env python3
"""Advisory JSP successor preservation audit; does not replace required release QA.

Run from a full Git checkout after incorporating current origin/main:
python3 scripts/validate_jsp_successor_preservation.py --base <PR-base-SHA>
No tracked files are written. A passing result proves bounded conservation,
not identity admission, evidential truth, deployment or original-binary custody.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import unicodedata

RELEASE = '65d56cec10e11f5a5c0861bb087ee87e64f5effa'
PARENT = '01116d63e93eb1e2819ae53a4060104477883407'
MANIFEST = 'assets/data/matter-identity-registry-v1.json'
EVIDENCE = 'assets/data/jsp-2017-source-relationship-register.json'
TYPES = {'PERSON': 'P', 'ORGANISATION': 'O', 'STRUCTURE': 'S', 'INSTITUTION': 'I', 'PROCEEDING': 'R'}
RELEASE_COUNTS = {'total': 379, 'PERSON': 176, 'ORGANISATION': 99, 'STRUCTURE': 11, 'INSTITUTION': 49, 'PROCEEDING': 44}
FROZEN = [
  ".github/workflows/jsp-2017-dossier-scoped-qa.yml",
  ".github/workflows/jsp-evidence-object-ingress.yml",
  ".github/workflows/jsp-live-evidence-verification.yml",
  ".github/workflows/jsp-public-evidence-capture.yml",
  ".github/workflows/jsp-reader-browser-acceptance.yml",
  "archive/JSP_2017_CANONICAL_DOSSIER_RELEASE_05SEP2026.md",
  "archive/JSP_GENUINE_IMAGES_RELEASE_CONTROL_05SEP2026.md",
  "assets/data/jsp-2017-source-relationship-register.json",
  "assets/data/jsp-official-images-provenance-20260905.json",
  "assets/data/matter-identity-registry-v1.jsp-organisations-20260905.json",
  "assets/data/matter-identity-registry-v1.jsp-people-20260905.json",
  "assets/data/matter-identity-registry-v1.jsp-proceedings-20260905.json",
  "assets/evidence/jsp-2017/BORME-C-2017-7368.pdf",
  "assets/evidence/jsp-2017/borme-c-2017-7368-full-page.webp",
  "assets/evidence/jsp-2017/borme-c-2017-7368-item-five.webp",
  "assets/jsp-dossier-2017.css",
  "assets/jsp-dossier-2017.js",
  "en/jsp-montelanza-insolvency-liquidation/index.html",
  "es/jsp-montelanza-concurso-liquidacion/index.html",
  "scripts/prepare_jsp_official_image_objects.py",
  "scripts/test_jsp_reader_browser.py",
  "scripts/validate_jsp_2017_dossier.py",
  "scripts/verify_jsp_official_evidence.py"
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def norm(value):
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in unicodedata.normalize('NFKD', value.lower()) if not unicodedata.combining(c)))


def preserve_fields(old, new, label):
    """Only additive top-level fields are accepted; old values remain exact."""
    require(all(key in new and new[key] == value for key, value in old.items()), 'Changed or removed existing field: ' + label)


def unchanged_object(old, new, path):
    require(path in old and path in new and old[path] == new[path], 'Frozen object changed or missing: ' + path)


def registry(reader, ref):
    manifest = json.loads(reader.read(ref, MANIFEST))
    date.fromisoformat(manifest['control_date'])
    parts, records = {}, {}
    for part in manifest['parts']:
        name = part['path']
        require(isinstance(name, str) and PurePosixPath(name).name == name and name.endswith('.json'), 'Unsafe shard path')
        require(name not in parts, 'Duplicate shard path: ' + name)
        parts[name] = part
        rows = json.loads(reader.read(ref, 'assets/data/' + name))['records']
        require(len(rows) == part['count'], 'Shard count mismatch: ' + name)
        for row in rows:
            rid, kind = row['id'], row['type']
            require(kind in TYPES and kind == part['type'], 'Shard/record type mismatch')
            require(re.fullmatch('PD-SP-' + TYPES[kind] + r'-\d{4}', rid), 'ID/type mismatch: ' + rid)
            require(rid not in records, 'Duplicate identity: ' + rid)
            require(isinstance(row['name'], str) and bool(norm(row['name'])), 'Missing identity name')
            records[rid] = row
    counts = {'total': len(records), **{kind: sum(r['type'] == kind for r in records.values()) for kind in TYPES}}
    require(counts == manifest['counts'], 'Manifest counts mismatch')
    return manifest, parts, records


def delta(before, after):
    require(set(before) <= set(after), 'Existing identity removed')
    existing_names = defaultdict(set)
    for rid, row in before.items():
        preserve_fields(row, after[rid], rid)
        for name in [row['name'], *row.get('aliases', [])]:
            existing_names[norm(name)].add(rid)
    additions = sorted(set(after) - set(before))
    for rid in additions:
        row = after[rid]
        require(bool(row.get('identity_sources')), 'New identity lacks source: ' + rid)
        for name in [row['name'], *row.get('aliases', [])]:
            normalized = norm(name)
            require(normalized and not (existing_names[normalized] - {rid}), 'New identity/name collision: ' + rid)
            existing_names[normalized].add(rid)
    return additions


def audit(reader, base, candidate):
    pm, pp, pr = registry(reader, PARENT)
    rm, rp, rr = registry(reader, RELEASE)
    bm, bp, br = registry(reader, base)
    cm, cp, cr = registry(reader, candidate)
    require(rm['control_date'] == '2026-09-05' and rm['counts'] == RELEASE_COUNTS, 'Frozen release pins differ')
    require(set(pp) <= set(rp), 'Release lost predecessor shard')
    for name in pp:
        require(pp[name] == rp[name], 'Release changed predecessor metadata')
        require(reader.read(PARENT, 'assets/data/' + name) == reader.read(RELEASE, 'assets/data/' + name), 'Release changed predecessor bytes')
    released = delta(pr, rr)
    require(len(released) == 27 and Counter(rr[r]['type'] for r in released) == {'PERSON': 11, 'ORGANISATION': 15, 'PROCEEDING': 1}, 'Frozen scoped denominator differs')
    release_tree = reader.tree(RELEASE)
    for ref in (base, candidate):
        tree = reader.tree(ref)
        for path in FROZEN:
            unchanged_object(release_tree, tree, path)
    # Current main contains later corrections outside the frozen JSP shards.
    # Report them, never overwrite or silently certify them as unchanged.
    require(set(rr) <= set(br), 'Main lost a release-era identity')
    inherited = sorted(r for r in rr if rr[r] != br[r])
    added = delta(br, cr)
    require(set(bp) <= set(cp), 'Successor lost shard')
    for name, part in bp.items():
        preserve_fields({k: v for k, v in part.items() if k != 'count'}, cp[name], 'part ' + name)
    preserve_fields({k: v for k, v in bm.items() if k not in ('parts', 'counts', 'control_date')}, cm, 'manifest')
    require(date.fromisoformat(bm['control_date']) <= date.fromisoformat(cm['control_date']), 'Control date moved backward')
    evidence = json.loads(reader.read(candidate, EVIDENCE))
    source_ids = {s['id'] for s in evidence['sources']}
    require(len(source_ids) == len(evidence['sources']) == 8 and len(evidence['events']) == 7 and len(evidence['edges']) == 18, 'Frozen evidence cardinality differs')
    require(len(evidence['existing_id_reuse']) == 18, 'Reuse denominator differs')
    for item in evidence['existing_id_reuse']:
        require(item['id'] in cr and norm(item['name']) == norm(cr[item['id']]['name']), 'Reused identity differs')
    for edge in evidence['edges']:
        require(edge['from'] in cr and edge['to'] in cr and edge['source'] in source_ids, 'Unresolved relationship endpoint/source')
    require(not {'PD-SP-P-0174', 'PD-SP-P-0178'} & set(cr), 'Rejected duplicate admitted')
    return {
        'result': 'PASS_ADVISORY_PRESERVATION_ONLY', 'release': RELEASE, 'release_parent': PARENT,
        'base': base, 'candidate': candidate, 'frozen_objects': len(FROZEN),
        'historical_release_counts': rm['counts'], 'historical_new_identities': len(released),
        'candidate_counts': cm['counts'], 'added_ids': added,
        'inherited_main_changed_ids_not_reaudited': inherited,
        'additive_field_ids': sorted(r for r in br if br[r] != cr[r]),
        'limitations': ['Required JSP release gate remains controlling and unchanged',
                       'No approval of new identity admission or source truth',
                       'No browser, deployment, original-binary custody or whole-repository certification',
                       'Frozen Git object identity preserves bytes; it is not an independent custody copy'],
    }


class GitReader:
    def __init__(self, root):
        self.root = root

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root)

    def read(self, ref, path):
        return self.git('show', ref + ':' + path)

    def tree(self, ref):
        result = {}
        for row in self.git('ls-tree', '-rz', ref).split(b'\0'):
            if row:
                meta, path = row.split(b'\t', 1)
                result[path.decode()] = tuple(meta.decode().split())
        return result

    def ancestor(self, older, newer):
        require(subprocess.run(['git', 'merge-base', '--is-ancestor', older, newer], cwd=self.root).returncode == 0, 'Missing or incompatible ancestry: ' + older)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True)
    args = parser.parse_args()
    reader = GitReader(Path(__file__).resolve().parents[1])
    try:
        base = reader.git('rev-parse', 'refs/remotes/origin/main').decode().strip()
        candidate = reader.git('rev-parse', 'HEAD').decode().strip()
        for older, newer in ((PARENT, RELEASE), (RELEASE, base), (args.base, base), (base, candidate)):
            reader.ancestor(older, newer)
        result = audit(reader, base, candidate)
        # Keep current derived counts and dates verified by the existing checker.
        subprocess.run(['python3', 'scripts/reconcile_identity_registry_projections.py', '--check'], cwd=reader.root, check=True)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'result': 'FAIL', 'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

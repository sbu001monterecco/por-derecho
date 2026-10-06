#!/usr/bin/env python3
"""Negative controls against the real incorporated Git history; no file mutation."""
import argparse
import copy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_jsp_successor_preservation import GitReader, MANIFEST, audit, delta


class Overlay:
    def __init__(self, reader, candidate):
        self.reader, self.candidate = reader, candidate
        self.objects, self.entries = {}, copy.deepcopy(reader.tree(candidate))

    def tree(self, ref):
        return self.entries if ref == self.candidate else self.reader.tree(ref)

    def read(self, ref, path):
        return self.objects[path] if ref == self.candidate and path in self.objects else self.reader.read(ref, path)

    def edit(self, path, change):
        data = json.loads(self.read(self.candidate, path))
        change(data)
        self.objects[path] = json.dumps(data).encode()


def run(reader, base, candidate):
    audit(reader, base, candidate)
    manifest = json.loads(reader.read(candidate, MANIFEST))
    shard = 'assets/data/' + next(p['path'] for p in manifest['parts'] if p['type'] == 'ORGANISATION' and 'jsp-' not in p['path'])
    frozen = 'assets/evidence/jsp-2017/BORME-C-2017-7368.pdf'

    def replace_identity(data):
        data['records'][0]['name'] = 'REWRITTEN IDENTITY'

    def duplicate_identity(data):
        data['records'][1]['id'] = data['records'][0]['id']

    cases = [
        ('deleted source PDF', lambda x: x.entries.pop(frozen), 'Frozen object'),
        ('altered source PDF object', lambda x: x.entries.__setitem__(frozen, ('100644', 'blob', '0' * 40)), 'Frozen object'),
        ('source PDF changed to symlink', lambda x: x.entries.__setitem__(frozen, ('120000', 'blob', x.entries[frozen][2])), 'Frozen object'),
        ('rewritten existing identity', lambda x: x.edit(shard, replace_identity), 'Changed or removed existing field'),
        ('duplicate identity ID', lambda x: x.edit(shard, duplicate_identity), 'Duplicate identity'),
        ('stale aggregate count', lambda x: x.edit(MANIFEST, lambda d: d['counts'].__setitem__('total', 1)), 'Manifest counts'),
        ('backdated control date', lambda x: x.edit(MANIFEST, lambda d: d.__setitem__('control_date', '2020-01-01')), 'Control date'),
        ('unsafe shard path', lambda x: x.edit(MANIFEST, lambda d: d['parts'][0].__setitem__('path', '../escape.json')), 'Unsafe shard'),
        ('duplicate shard entry', lambda x: x.edit(MANIFEST, lambda d: d['parts'].append(copy.deepcopy(d['parts'][0]))), 'Duplicate shard'),
        ('wrong typed identity', lambda x: x.edit(shard, lambda d: d['records'][0].__setitem__('type', 'PERSON')), 'type mismatch'),
    ]
    outcomes = []
    for label, mutation, error in cases:
        overlay = Overlay(reader, candidate)
        mutation(overlay)
        try:
            audit(overlay, base, candidate)
        except ValueError as exc:
            if error not in str(exc):
                raise AssertionError(label + ': unexpected rejection: ' + str(exc)) from exc
            outcomes.append(label)
        else:
            raise AssertionError('Corruption accepted: ' + label)
    # Admission-boundary negatives supplement the real-tree corruption cases.
    old = {'PD-SP-O-0001': {'id': 'PD-SP-O-0001', 'name': 'Existing Company', 'type': 'ORGANISATION', 'identity_sources': ['PUBLIC-SOURCE-1']}}
    new = {'id': 'PD-SP-O-0002', 'name': 'New Company', 'type': 'ORGANISATION', 'identity_sources': ['PUBLIC-SOURCE-2']}
    delta(old, {**copy.deepcopy(old), new['id']: copy.deepcopy(new)})
    cases = [
        ('removed identity', {}),
        ('source-less new identity', {**old, new['id']: {**new, 'identity_sources': []}}),
        ('new alias collides with existing name', {**old, new['id']: {**new, 'aliases': ['Existing Company']}}),
        ('rewritten existing evidence source', {'PD-SP-O-0001': {**old['PD-SP-O-0001'], 'identity_sources': []}}),
    ]
    for label, candidate_rows in cases:
        try:
            delta(old, candidate_rows)
        except ValueError:
            outcomes.append(label)
        else:
            raise AssertionError('Corruption accepted: ' + label)
    return {'result': 'PASS_NEGATIVE_CONTROLS', 'baseline_passed': True, 'rejected_mutations': outcomes}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True)
    args = parser.parse_args()
    reader = GitReader(Path(__file__).resolve().parents[1])
    candidate = reader.git('rev-parse', 'HEAD').decode().strip()
    print(json.dumps(run(reader, args.base, candidate), indent=2))

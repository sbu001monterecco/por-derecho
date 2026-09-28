#!/usr/bin/env python3
"""Read-only REGAGE lookup. Public cache misses require private source retrieval."""
import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def normalize(value):
    text = unicodedata.normalize('NFKD', str(value))
    return re.sub(r'[^a-z0-9]+', '', ''.join(c for c in text if not unicodedata.combining(c)).lower())


def records_from(control, private_index=None):
    if private_index is not None:
        if private_index['summary']['source_sha256'] != control['source_sha256']:
            raise ValueError('Private snapshot hash differs from current control; reconcile versions before use.')
        records = private_index['records']
        if len(records) != control['full_private_row_count']:
            raise ValueError('Private snapshot row count differs from control.')
        if len({r['registration_id'] for r in records}) != len(records):
            raise ValueError('Duplicate registration references in private snapshot.')
        counts = {s: sum(r['portal_status_literal'] == s for r in records) for s in control['status_counts']}
        if counts != control['status_counts']:
            raise ValueError('Private snapshot status totals differ from control.')
        return records, 'FULL_PRIVATE_SNAPSHOT'
    family = control['known_family']
    records = [{'registration_id': reg, 'portal_status_literal': family['export_status_each'],
                'part': n, 'filing_family': 'EG745/2026 reposicion 10-part filing',
                'receipt_control': family['receipt_controls'] + reg + '.json'}
               for n, reg in enumerate(family['delivery_registration_ids'], 1)]
    records.append({'registration_id': family['separate_preservation_registration_id'],
                    'portal_status_literal': family['separate_preservation_export_status'],
                    'part': '', 'filing_family': 'EG745/2026 separate preservation communication'})
    return records, 'MINIMIZED_KNOWN_FAMILY_CACHE'


def lookup(control, query, private_index=None):
    records, scope = records_from(control, private_index)
    exact = [r for r in records if normalize(r['registration_id']) == normalize(query)]
    if exact:
        hits = exact
    elif normalize(query) in {normalize(x) for x in control['known_family']['aliases']}:
        expected = control['known_family']['delivery_registration_ids']
        hits = sorted([r for r in records if r['registration_id'] in expected], key=lambda r: expected.index(r['registration_id']))
    else:
        terms = [normalize(t) for t in query.split() if normalize(t)]
        hits = [r for r in records if terms and all(t in normalize(' '.join(str(v) for v in r.values())) for t in terms)]
    state = 'EXPORT_ENTRY_LOCATED' if hits else ('NOT_LOCATED_IN_BOUNDED_SNAPSHOT' if private_index else control['negative_cache_result'])
    return {'query': query, 'result': state, 'scope': scope, 'source_sha256': control['source_sha256'],
            'match_count': len(hits), 'matches': hits,
            'boundary': 'Not located is not not filed. Transport status is not admission, examination or merits. Inspect native receipt evidence before a filing-content or deadline conclusion.'}


def self_test(control, private_index=None):
    assert sum(control['status_counts'].values()) == control['full_private_row_count'] == 407
    for query in control['known_family']['aliases']:
        result = lookup(control, query, private_index)
        assert result['match_count'] == 10, query
        assert result['matches'][0]['registration_id'] == 'REGAGE26e00082068814'
        assert all(r['portal_status_literal'] == 'Recibido' for r in result['matches'])
    result = lookup(control, 'REGAGE26e00082033336', private_index)
    assert result['match_count'] == 1 and not result['matches'][0]['part']
    result = lookup(control, 'REGAGE00e00000000000', private_index)
    assert result['match_count'] == 0 and result['result'] != 'NOT_FILED'
    if not private_index:
        assert result['result'] == control['negative_cache_result']
    print('PASS: five aliases; ten received deliveries; preservation separation; count checks; negative-search boundary.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?')
    parser.add_argument('--control', type=Path, default=ROOT / 'ops/REGAGE_CURRENT_LOOKUP.json')
    parser.add_argument('--private-index', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    try:
        control = json.loads(args.control.read_text(encoding='utf-8'))
        private = json.loads(args.private_index.read_text(encoding='utf-8')) if args.private_index else None
        if args.self_test:
            self_test(control, private)
        elif args.query:
            print(json.dumps(lookup(control, args.query, private), ensure_ascii=False, indent=2))
        else:
            parser.error('provide a query or --self-test')
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, 'Source/control error; no filing conclusion: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()

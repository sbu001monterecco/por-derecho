#!/usr/bin/env python3
"""Validate only the 24 September execution projection, not case merits or deployment."""
import json
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        data = json.loads((root / 'ops/unitary-action-execution-20260924.json').read_text(encoding='utf-8'))
        actions = [item for group in data['groups'] for item in group['action_ids']]
        assert sorted(actions) == [f'A{i:03d}' for i in range(1, 61)], 'Missing, duplicated or reassigned action ID'
        assert data['claim_ids'] == [f'AC-CLM-{i:03d}' for i in range(1, 15)], 'Claim-family coverage changed'
        assert data['external_action_authorized'] is False, 'External authority must not be inferred'
        assert data['publication']['private_advice_included'] is False, 'Private advice is excluded'
        assert data['publication']['new_production_writer'] is False, 'Existing publication writer controls'
        assert data['coverage']['fresh_all_source_page_review_claimed'] is False, 'No fresh full-corpus certificate'
        for key in ('programme', 'canonical_register', 'canonical_router'):
            assert (root / data[key]).is_file(), f'Missing linked file: {data[key]}'
        text = (root / data['programme']).read_text(encoding='utf-8')
        for token in ('Ref.21', 'Ref.22', 'Ref.24', 'REGAGE26e00083453059', '29,208.88', 'RPL421/2026', 'RPL3304/2025'):
            assert token in text, f'Missing cross-track anchor: {token}'
        assert 'mail.google.com' not in text, 'Private message locator in public programme'
        print(json.dumps({'status': 'PASS', 'actions': 60, 'claim_families': 14, 'scope': 'execution projection only; not repository-wide acceptance or legal proof'}))
        return 0
    except (OSError, ValueError, KeyError, AssertionError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

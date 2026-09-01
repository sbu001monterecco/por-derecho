#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

root = load('assets/data/matter-identity-registry-v1.json')
people = load('assets/data/matter-identity-registry-v1.la-laguna-judicial-people.json')
inst = load('assets/data/matter-identity-registry-v1.la-laguna-judicial-institutions.json')
control = load('assets/data/la-laguna-judicial-actors-canonical-interlink-control-v1.json')
gaps = load('assets/data/la-laguna-judicial-actors-gap-closure-audit-v1.json')
dp = load('assets/data/dp748-2026-appeal-reopening-control-v1.json')

assert root['counts'] == {'total':339,'PERSON':160,'ORGANISATION':83,'STRUCTURE':11,'INSTITUTION':42,'PROCEEDING':43}
assert sum(p['count'] for p in root['parts']) == 339

p = {r['id']: r for r in people['records']}
for n in range(147,158):
    pid = f'PD-SP-P-{n:04d}'
    assert pid in p
    assert p[pid]['routes']['es'].startswith('/es/registro-judicial-la-laguna/')
    assert p[pid]['routes']['en'].startswith('/en/la-laguna-judicial-register/')

i = {r['id']: r for r in inst['records']}
for n in range(37,42):
    iid = f'PD-SP-I-{n:04d}'
    assert iid in i and 'routes' in i[iid]

assert {g['gap_id'] for g in gaps['gaps']} == {'LL-JUD-GAP-001','LL-JUD-GAP-002','LL-JUD-GAP-003'}
app = next(x for x in control['proceedings'] if x['master_id'] == 'TF-APP-004')
assert app['verification'] == 'UNVERIFIED_PLACEHOLDER'
assert app['judges'] == [] and app['lajs'] == []
assert dp['p0_appeal_control']['subsidiary_appeal_admitted'].startswith('VERIFIED')
assert dp['p0_appeal_control']['transmission_to_audiencia'] == 'NOT_LOCATED'
assert dp['p0_appeal_control']['appellate_roll'] == 'NOT_LOCATED'
assert dp['act_specific_professional_lineage'][0]['lawyer_caepr_id'] == 'PD-SP-P-0062'

for rel in ['es/registro-judicial-la-laguna/index.html','en/la-laguna-judicial-register/index.html']:
    text=(ROOT/rel).read_text(encoding='utf-8')
    for token in ['LL-JUD-GAP-001','LL-JUD-GAP-002','LL-JUD-GAP-003','PD-SP-P-0147','PD-SP-P-0155','PD-SP-I-0037','PD-SP-I-0039']:
        assert token in text

print('La Laguna judicial register current-main validation: PASS')

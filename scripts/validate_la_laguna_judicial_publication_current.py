#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
root=load('assets/data/matter-identity-registry-v1.json')
people=load('assets/data/matter-identity-registry-v1.la-laguna-judicial-people.json')
orgs=load('assets/data/matter-identity-registry-v1.la-laguna-judicial-institutions.json')
ctl=load('assets/data/la-laguna-judicial-actors-canonical-interlink-control-v1.json')
gaps=load('assets/data/la-laguna-judicial-actors-gap-closure-audit-v1.json')
appeal=load('assets/data/dp748-2026-appeal-reopening-control-v1.json')
filings=load('assets/data/counsel-filing-register-v1.json')
assert root['counts']['total']==339
assert sum(x['count'] for x in root['parts'])==339
p={r['id']:r for r in people['records']}
assert set(p)=={f'PD-SP-P-{n:04d}' for n in range(147,158)}
for r in p.values():
    assert r['routes']['es'].startswith('/es/registro-judicial-la-laguna/')
    assert r['routes']['en'].startswith('/en/la-laguna-judicial-register/')
i={r['id']:r for r in orgs['records']}
assert set(i)=={f'PD-SP-I-{n:04d}' for n in range(37,42)}
for r in i.values(): assert r.get('routes')
assert {g['gap_id'] for g in gaps['gaps']}=={'LL-JUD-GAP-001','LL-JUD-GAP-002','LL-JUD-GAP-003'}
g3=next(g for g in gaps['gaps'] if g['gap_id']=='LL-JUD-GAP-003')
assert 'admitted' in g3['verified_minimum'].lower() or 'admission' in g3['search_state'].lower()
app=next(x for x in ctl['proceedings'] if x['master_id']=='TF-APP-004')
assert app['verification']=='APPEAL_ADMISSION_VERIFIED_APPELLATE_ORGAN_ROLL_NOT_VERIFIED'
assert app['judges']==[] and app['lajs']==[]
assert ctl['identity_collision_boundary'].find('PD-SP-P-0062')>=0
carlos=next(x for x in filings['professional_registers'] if x['display_name']=='Carlos Llamas Sanz')
assert carlos['caepr_id']=='PD-SP-P-0062'
for page in ['es/registro-judicial-la-laguna/index.html','en/la-laguna-judicial-register/index.html']:
    t=(ROOT/page).read_text(encoding='utf-8')
    for token in ['LL-JUD-GAP-001','LL-JUD-GAP-002','LL-JUD-GAP-003','PD-SP-P-0147','PD-SP-P-0155','PD-SP-I-0037','PD-SP-I-0039','20-May-2026' if page.startswith('en/') else '20-may-2026']:
        assert token in t
print('La Laguna judicial current-main publication: PASS')

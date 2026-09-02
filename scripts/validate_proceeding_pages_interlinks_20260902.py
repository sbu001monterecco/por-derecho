#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'assets' / 'data'
public = json.loads((DATA/'proceedings-master-public-v1.json').read_text(encoding='utf-8'))
routes_doc = json.loads((DATA/'proceeding-page-routes-20260902.json').read_text(encoding='utf-8'))
graph_doc = json.loads((DATA/'proceeding-interlink-graph-20260902.json').read_text(encoding='utf-8'))
records = public['records']
by_id = {r['Master_ID']: r for r in records}
routes = routes_doc['routes']
graph = {r['master_id']: r for r in graph_doc['records']}

assert routes_doc['record_count'] == len(records) == len(routes), (routes_doc['record_count'], len(records), len(routes))
assert graph_doc['record_count'] == len(records) == len(graph)
assert set(routes) == set(by_id) == set(graph)

for mid, row in by_id.items():
    for lang in ('es','en'):
        route = routes[mid][lang]
        path = ROOT / route / 'index.html'
        assert path.is_file(), f'missing dedicated page {path}'
        html = path.read_text(encoding='utf-8')
        assert mid in html, f'{mid} missing from {route}'
        assert (row.get('Reference') or mid) in html, f'reference missing from {route}'
        assert row.get('Source_Status','') in html, f'source status missing from {route}'
        assert 'Registro Maestro' in html or 'Master Register' in html, f'master backlink missing from {route}'
        other = routes[mid]['en' if lang == 'es' else 'es']
        assert other in html, f'language reciprocal link missing from {route}'
    for other in graph[mid]['formal_related']:
        assert mid in graph[other]['formal_related'], f'formal backlink not reciprocal: {mid} <-> {other}'

for p in (ROOT/'es/procedimientos/index.html', ROOT/'en/proceedings/index.html'):
    assert p.is_file(), p
    h = p.read_text(encoding='utf-8')
    for mid in by_id:
        slug = re.sub(r'[^a-z0-9]+','-',mid.lower()).strip('-')
        assert f'./{slug}/' in h, f'{mid} absent from {p}'

search = (ROOT/'assets/canonical-home-search-20260902.js').read_text(encoding='utf-8')
for marker in ('proceeding-page-routes-20260902.json', 'proceedingRoutes[record.Master_ID]?.[lang]'):
    assert marker in search, marker

for path, marker in [
    (ROOT/'es/registro-maestro-procedimientos/index.html', '../procedimientos/'),
    (ROOT/'en/master-proceedings-register/index.html', '../proceedings/'),
]:
    assert marker in path.read_text(encoding='utf-8'), f'directory backlink missing in {path}'

# Recovered references must have dedicated pages and public rows.
required_refs = [
    'Procedimiento Ordinario 467/2010','Rollo 793/2012','DP 3017/2014','DP 168/2015','DP 2084/2016',
    'Rollo 526/2013','P.O. 1241/2011','Medidas cautelares 1355/2011','P.O. 562/2014','P.O. 213/2015',
    'Juicio Verbal 268/2016','Diligencias Preliminares 1041/2017','273/2013','302/2018','49/2018','92/2012'
]
refs = {r.get('Reference'): r['Master_ID'] for r in records}
for ref in required_refs:
    assert ref in refs, f'missing recovered reference {ref}'
    mid = refs[ref]
    assert (ROOT/routes[mid]['es']/'index.html').is_file()
    assert (ROOT/routes[mid]['en']/'index.html').is_file()

# Source-supported judge identities must remain explicit and unknown office-holders remain gaps.
coverage_doc = json.loads((DATA/'proceeding-justice-authority-coverage-20260902.json').read_text(encoding='utf-8'))
coverage = {r['master_id']: r for r in coverage_doc['records']}
assert coverage['LZ-CIV-045']['judge_or_magistrate']['person_ids'] == ['PD-SP-P-0163']
assert set(coverage['LZ-APP-046']['judge_or_magistrate']['person_ids']) == {'PD-SP-P-0164','PD-SP-P-0130','PD-SP-P-0129'}
assert coverage['LZ-JUD-047']['judge_or_magistrate']['state'] == 'SOURCE_GAP'
assert coverage['LZ-JUD-047']['laj']['state'] == 'SOURCE_GAP'

print('PASS dedicated proceeding pages/interlinks:', len(records), 'public records;', sum(len(v['formal_related']) for v in graph.values())//2, 'reciprocal formal edges')

#!/usr/bin/env python3
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
matrix=json.loads((root/'assets/data/concurso36-multitrack-judicial-failure-parallel-lives-20260829.json').read_text())
supp=json.loads((root/'assets/data/concurso36-lexnet-supplement-20260829.json').read_text())
assert matrix['status'].startswith('INVESTIGATIVE / PROSECUTORIAL')
assert len(matrix['failure_modes'])==6
assert len(matrix['control_opportunities'])==12
assert matrix['cross_border_eu_lane']['status']=='UNRESOLVED SOURCE IDENTIFICATION GAP'
assert 'does not presently establish an agreement' in matrix['neutralisation_shield_hypothesis']['statement']
ids={r.get('lexnet_id') for r in supp['records']}
for required in {'1201810205126334','1201810213090383','201810213906846'}:
    assert required in ids, required
assert supp['status'].startswith('CONTROLLED SUPPLEMENT')
for p in [
    'es/concurso-36-2012-fallos-judiciales-vidas-paralelas/index.html',
    'en/insolvency-36-2012-judicial-failures-parallel-lives/index.html']:
    txt=(root/p).read_text()
    assert 'concurso36-judicial-failure-parallel-lives.js' in txt
    assert 'neutral' in txt.lower()
for p in ['es/concurso-36-2012/index.html','en/insolvency-36-2012/index.html']:
    txt=(root/p).read_text()
    assert 'fallos-judiciales-vidas-paralelas' in txt or 'judicial-failures-parallel-lives' in txt
    assert 'concurso36-lexnet-supplement-20260829.json' in txt
print('OK: Concurso 36/2012 multitrack judicial-failure / parallel-lives layer validated')

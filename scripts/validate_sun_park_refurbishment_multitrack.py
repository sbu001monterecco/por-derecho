#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
errors=[]
required=[
 'archive/SUN_PARK_REFURBISHMENT_AUTHORITY_MULTITRACK_FORENSIC_CONTROL_20AUG2026.md',
 'archive/SUN_PARK_REFURBISHMENT_AUTHORITY_MULTITRACK_RETRIEVAL_GATE_20AUG2026.md',
 'archive/SUN_PARK_REFURBISHMENT_AUTHORITY_MULTITRACK_EXECUTION_PROMPT_20AUG2026.md',
 'archive/MISSING_EVIDENCE_REGISTER_REFURBISHMENT_MULTITRACK_ADDENDUM_20AUG2026.md',
 'archive/CORRECTION_REGISTER_REFURBISHMENT_MULTITRACK_ADDENDUM_20AUG2026.md',
 'archive/CONTINUOUS_MAINTENANCE_MATRIX_REFURBISHMENT_MULTITRACK_ADDENDUM_20AUG2026.md',
 'assets/data/sun-park-refurbishment-multitrack-v1.json',
 'assets/sun-park-refurbishment-multitrack-20260820.js',
 'es/reforma-derrama-suministros-sun-park/index.html',
 'en/sun-park-refurbishment-levy-utilities/index.html',
 'publication-manifests/sun-park-refurbishment-multitrack-2026-08-20.json'
]
for rel in required:
 p=ROOT/rel
 if not p.exists(): errors.append(f'missing {rel}')

def text(rel): return (ROOT/rel).read_text(encoding='utf-8')
try:
 data=json.loads(text('assets/data/sun-park-refurbishment-multitrack-v1.json'))
 if data.get('architecture') != 'ONE_UNITARY_CAUSAL_SPINE_FIVE_EVIDENCE_LANES': errors.append('dataset architecture must be one unitary spine')
 lanes=data.get('lanes',[])
 if len(lanes) != 5: errors.append('dataset must contain exactly five evidence lanes')
 keys={t.get('key') for t in lanes}
 expected={'LIVING_PRODUCTIVE_UNIT_AND_FUNDED_EXIT','PREPARATION_AND_FORCE_BASED_TAKEOVER','POST_TAKEOVER_ASSET_TRANSFORMATION_AND_DISPLACEMENT','FORMALISATION_FINANCE_AND_NORMALISATION','ENABLEMENT_HARM_BENEFIT_AND_REMEDY'}
 if keys != expected: errors.append(f'lane keys mismatch: {keys}')
 if data.get('defence_overlay',{}).get('kind') != 'NODE_BY_NODE_RED_TEAM_NOT_SEPARATE_TIMELINE': errors.append('defence must be nested red-team overlay')
 boundary=data.get('public_boundary',{})
 for key in ['criminal_takeover_proved','every_work_criminal_proved','ona_exit_certain','estate_or_productive_unit_destruction_proved','criminal_coordination_proved']:
  if boundary.get(key) is not False: errors.append(f'public boundary {key} must be false')
 if boundary.get('no_presumption_of_neutrality') is not True: errors.append('anti-neutrality control missing')
except Exception as exc: errors.append(f'dataset json: {exc}')
try: json.loads(text('publication-manifests/sun-park-refurbishment-multitrack-2026-08-20.json'))
except Exception as exc: errors.append(f'manifest json: {exc}')
checks={
 'es/reforma-derrama-suministros-sun-park/index.html':['data-refurbishment-multitrack-page="20260820b"','No separe la reforma','masa activa','unidad productiva','ONA','no es una declaración de culpabilidad'],
 'en/sun-park-refurbishment-levy-utilities/index.html':['data-refurbishment-multitrack-page="20260820b"','Do not separate the refurbishment','active estate','productive unit','ONA','not a finding of guilt'],
 'assets/sun-park-refurbishment-multitrack-20260820.js':['data-refurbishment-unitary-update','data-refurbishment-unitary-crosslink','No separe la reforma','Do not separate the refurbishment'],
 'assets/site.js':['sun-park-refurbishment-multitrack-20260820.js','data-sun-park-refurbishment-multitrack-loader'],
 'robots.txt':['sitemap-refurbishment-authority-multitrack.xml']
}
for rel,markers in checks.items():
 if not (ROOT/rel).exists(): errors.append(f'missing for marker check {rel}'); continue
 body=text(rel)
 for m in markers:
  if m not in body: errors.append(f'{rel} missing marker {m}')
for rel in ['es/reforma-derrama-suministros-sun-park/index.html','en/sun-park-refurbishment-levy-utilities/index.html']:
 body=text(rel).lower()
 for forbidden in ['criminal takeover proved','toma criminal probada','every work was criminal','toda obra fue delictiva','ona certainly would have closed','ona habría cerrado con certeza']:
  if forbidden in body: errors.append(f'forbidden public overstatement in {rel}: {forbidden}')
 if 'asserted_clean_start_2022' in body or 'inicio limpio alegado</h3>' in body: errors.append(f'co-equal clean-start lane remains in {rel}')
 if '1853f' in body or 'message_id' in body: errors.append(f'private message identifier leaked in {rel}')
if errors:
 print('\n'.join(f'ERROR: {e}' for e in errors)); sys.exit(1)
print('Sun Park unitary takeover/works validation: OK')

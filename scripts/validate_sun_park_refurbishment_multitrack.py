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
 'assets/data/sun-park-refurbishment-multitrack-v1.json',
 'assets/sun-park-refurbishment-multitrack-20260820.js',
 'es/reforma-derrama-suministros-sun-park/index.html',
 'en/sun-park-refurbishment-levy-utilities/index.html',
 'sitemap-refurbishment-authority-multitrack.xml',
 'operations/SUN_PARK_REFURBISHMENT_MULTITRACK_ACTIVATION_2026-08-20.md',
 'publication-manifests/sun-park-refurbishment-multitrack-2026-08-20.json'
]
for rel in required:
 p=ROOT/rel
 if not p.exists(): errors.append(f'missing {rel}')

def text(rel): return (ROOT/rel).read_text(encoding='utf-8')
try:
 data=json.loads(text('assets/data/sun-park-refurbishment-multitrack-v1.json'))
 if len(data.get('tracks',[])) != 5: errors.append('dataset must contain exactly five tracks')
 keys={t.get('key') for t in data.get('tracks',[])}
 expected={'ASSERTED_CLEAN_START_2022','PRE_TITLE_RECORD','PARALLEL_2022_REGULARISATION_FINANCE_OPENING','ENABLEMENT_AND_INDEPENDENT_VERIFICATION','ASSET_VALUE_UTILITIES_HARM_BENEFIT'}
 if keys != expected: errors.append(f'track keys mismatch: {keys}')
 if data.get('public_boundary',{}).get('clean_start_proved_false') is not False: errors.append('public boundary clean-start false flag')
except Exception as exc: errors.append(f'dataset json: {exc}')
try: json.loads(text('publication-manifests/sun-park-refurbishment-multitrack-2026-08-20.json'))
except Exception as exc: errors.append(f'manifest json: {exc}')
for rel, markers in {
 'es/reforma-derrama-suministros-sun-park/index.html':['data-refurbishment-multitrack-page="20260820"','no es una declaración de culpabilidad','hoja en blanco','4,467'],
 'en/sun-park-refurbishment-levy-utilities/index.html':['data-refurbishment-multitrack-page="20260820"','not a finding of guilt','blank page','4.467'],
 'assets/sun-park-refurbishment-multitrack-20260820.js':['data-refurbishment-multitrack-update','data-refurbishment-multitrack-crosslink'],
 'assets/site.js':['sun-park-refurbishment-multitrack-20260820.js','data-sun-park-refurbishment-multitrack-loader'],
 'robots.txt':['sitemap-refurbishment-authority-multitrack.xml']
}.items():
 if not (ROOT/rel).exists(): errors.append(f'missing for marker check {rel}'); continue
 body=text(rel)
 for m in markers:
  if m not in body: errors.append(f'{rel} missing marker {m}')
for rel in ['es/reforma-derrama-suministros-sun-park/index.html','en/sun-park-refurbishment-levy-utilities/index.html']:
 body=text(rel).lower()
 for forbidden in ['proven criminal sanitisation','sanitización criminal probada','cam cometió el delito','cam committed the crime']:
  if forbidden in body: errors.append(f'forbidden public overstatement in {rel}: {forbidden}')
 if '1853f' in body or 'message_id' in body: errors.append(f'private message identifier leaked in {rel}')
if errors:
 print('\n'.join(f'ERROR: {e}' for e in errors)); sys.exit(1)
print('Sun Park refurbishment multitrack validation: OK')

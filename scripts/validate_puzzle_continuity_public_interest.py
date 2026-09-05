#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]

def text(path):
    p=ROOT/path
    if not p.exists(): errors.append(f'missing {path}'); return ''
    return p.read_text(encoding='utf-8')

def data(path):
    try: return json.loads(text(path))
    except Exception as e: errors.append(f'invalid json {path}: {e}'); return {}

guide=data('data/puzzle/puzzle-reading-guide-2026.json')
pi=data('data/puzzle/puzzle-public-interest-alertador-20260905.json')
runtime=text('assets/puzzle-public-interest-continuity-20260905.js')
site=text('assets/site.js')
gov=text('.github/governance/PUZZLE_CONTINUITY_PUBLIC_INTEREST_ALERTADOR_STANDARD_05SEP2026.md')

expected_sha='e441bdb368c0092d5b15ca5ee911eeac266540bde54817e424f3075f4c5fdd47'
doc=guide.get('document',{})
if doc.get('sha256') != expected_sha: errors.append('PUZZLE SHA mismatch')
if doc.get('pageCount') != 32: errors.append('PUZZLE page contract is not 32')
if doc.get('sizeBytes') != 50046618: errors.append('PUZZLE size contract mismatch')
if doc.get('assetPath') != 'assets/docs/puzzle/PUZZLE-2024-original.pdf': errors.append('PUZZLE canonical asset path changed')

baseline=pi.get('baseline',{})
if '21 July 2026' not in baseline.get('current_reading_baseline',''): errors.append('21 July 2026 reading baseline missing')
if 'June-2024' not in baseline.get('historical_exhibit','') and '2024' not in baseline.get('historical_exhibit',''): errors.append('historical PUZZLE baseline missing')

for needle in ['Directive (EU) 2019/1937','Ley 2/2023','Hinweisgeberschutzgesetz','Employment Rights Act 1996','Aweswell Limited']:
    if needle not in json.dumps(pi,ensure_ascii=False): errors.append(f'capacity framework missing {needle}')
for needle in ['OPEN_PUBLIC_FUNDS_QUESTION','DOCUMENTED_INSTITUTIONAL_CONTACT','CLAIMANT_ALLEGATION']:
    if needle not in json.dumps(pi): errors.append(f'public-interest status missing {needle}')
for needle in ['data-pd-puzzle-download','download="PUZZLE-2024-original.pdf"','aria-disabled','21 de julio de 2026','21 July 2026']:
    if needle not in runtime: errors.append(f'runtime marker missing {needle}')
if 'puzzle-public-interest-continuity-20260905.js' not in site: errors.append('site loader missing continuity runtime')
for needle in ['PD-PUZZLE-GOV-20260905-01','public funds','Ley 2/2023','Hinweisgeberschutzgesetz','Public Interest Disclosure Act 1998']:
    if needle.lower() not in gov.lower(): errors.append(f'governance marker missing {needle}')

# No private/domain-only Drive link may be substituted for the public original.
for content,name in [(runtime,'runtime'),(json.dumps(pi),'public-interest data')]:
    if 'drive.google.com' in content or 'docs.google.com' in content:
        errors.append(f'{name} exposes a Drive link instead of controlled public asset')

# Strong attribution boundary must remain explicit.
if 'does not automatically' not in runtime and 'no determina automáticamente' not in runtime:
    errors.append('statutory-protection caveat missing')
if 'does not assert use, loss or diversion of public funds' not in runtime:
    errors.append('public-funds non-overstatement boundary missing')

print('PUZZLE CONTINUITY / PUBLIC INTEREST GATE:', 'PASS' if not errors else 'FAIL')
for e in errors: print(' -',e)
sys.exit(1 if errors else 0)

#!/usr/bin/env python3
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1]
errors=[]
def need(p,*terms):
    q=R/p
    if not q.exists(): errors.append(f'missing {p}'); return ''
    t=q.read_text(encoding='utf-8')
    for x in terms:
        if x not in t: errors.append(f'{p}: missing {x}')
    return t
b=need('data/puzzle/puzzle-baseline-june-25-2026.json','2026-06-25','CANONICAL_FILED_NARRATIVE_BASELINE','LATER_PROCEDURAL_LENS','HISTORICAL_VISUAL_EXHIBIT','OPEN_VERIFICATION','Law 2/2023')
try:
    d=json.loads(b)
    assert d['canonical_filed_baseline']['status']=='FILED_PARTY_PLEADING_BASELINE'
except Exception as e: errors.append(f'baseline json: {e}')
need('.github/governance/PUZZLE_CONTINUITY_PUBLICATION_AND_BASELINE_STANDARD_05SEP2026.md','25 June 2026','20/21 July 2026','50,046,618','e441bdb368c0092d5b15ca5ee911eeac266540bde54817e424f3075f4c5fdd47','Chronology','public funds','Law 2/2023')
need('assets/puzzle-continuity-enhancement-20260905.js','PUZZLE-2024-original.pdf','PUZZLE-2024-web-reading-copy.pdf','PUZZLE-2024-overview.jpg','Download PUZZLE PDF','Law 2/2023','public/EU funding')
need('assets/site.js','puzzle-continuity-enhancement-20260905.js')
# Original 2024 viewer must remain 32-page and seven-group controlled.
g=need('data/puzzle/puzzle-reading-guide-2026.json','"pageCount": 32','"groups"')
if errors:
    print('PUZZLE CONTINUITY GATE: FAIL'); [print(' -',e) for e in errors]; sys.exit(1)
print('PUZZLE CONTINUITY GATE: PASS')

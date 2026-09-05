#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,sys

R=Path(__file__).resolve().parents[1]
errors=[]

def need(p,*terms):
    q=R/p
    if not q.exists():
        errors.append(f'missing {p}')
        return ''
    t=q.read_text(encoding='utf-8')
    for x in terms:
        if x not in t:
            errors.append(f'{p}: missing {x}')
    return t

b=need(
    'data/puzzle/puzzle-baseline-june-25-2026.json',
    '2026-06-25','CANONICAL_FILED_NARRATIVE_BASELINE','LATER_PROCEDURAL_LENS',
    'HISTORICAL_VISUAL_EXHIBIT','OPEN_VERIFICATION','Law 2/2023'
)
try:
    d=json.loads(b)
    assert d['canonical_filed_baseline']['status']=='FILED_PARTY_PLEADING_BASELINE'
except Exception as e:
    errors.append(f'baseline json: {e}')

need(
    '.github/governance/PUZZLE_CONTINUITY_PUBLICATION_AND_BASELINE_STANDARD_05SEP2026.md',
    '25 June 2026','20/21 July 2026','50,046,618',
    'e441bdb368c0092d5b15ca5ee911eeac266540bde54817e424f3075f4c5fdd47',
    'Chronology','public funds','Law 2/2023'
)
need(
    'assets/puzzle-continuity-enhancement-20260905.js',
    'PUZZLE-2024-original.pdf','PUZZLE-2024-web-reading-copy.pdf','PUZZLE-2024-overview.jpg',
    'Download PUZZLE PDF','Law 2/2023','public/EU funding'
)
need('assets/site.js','puzzle-continuity-enhancement-20260905.js')

# Parse the current guide semantically. The guide evolved from a legacy `groups`
# layout to `tracks` + seven `chapters`; formatting/schema evolution must not make
# the continuity gate fail when the controlled 32-page structure is preserved.
guide_path=R/'data/puzzle/puzzle-reading-guide-2026.json'
try:
    guide=json.loads(guide_path.read_text(encoding='utf-8'))
    doc=guide['document']
    assert doc['pageCount']==32
    assert doc['sha256']=='e441bdb368c0092d5b15ca5ee911eeac266540bde54817e424f3075f4c5fdd47'
    assert doc['sizeBytes']==50046618
    assert doc['assetPath']=='assets/docs/puzzle/PUZZLE-2024-original.pdf'
    assert set(guide['tracks']) >= {'1956','1901'}
    assert len(guide['chapters'])==7
    covered=[]
    for chapter in guide['chapters']:
        start,end=chapter['pages']
        assert 1 <= start <= end <= 32
        covered.extend(range(start,end+1))
    assert set(covered)==set(range(1,33))
except Exception as e:
    errors.append(f'reading guide semantic control: {e}')

# The unified release now materialises the authenticated master. Verify bytes,
# rather than relying on an old pending-state label or a filename alone.
pdf=R/'assets/docs/puzzle/PUZZLE-2024-original.pdf'
if not pdf.exists():
    errors.append('missing authenticated Puzzle master')
else:
    raw_size=pdf.stat().st_size
    digest=hashlib.sha256()
    with pdf.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024*1024), b''):
            digest.update(chunk)
    if raw_size != 50046618:
        errors.append(f'Puzzle master size mismatch: {raw_size}')
    if digest.hexdigest() != 'e441bdb368c0092d5b15ca5ee911eeac266540bde54817e424f3075f4c5fdd47':
        errors.append('Puzzle master SHA-256 mismatch')

if errors:
    print('PUZZLE CONTINUITY GATE: FAIL')
    [print(' -',e) for e in errors]
    sys.exit(1)
print('PUZZLE CONTINUITY GATE: PASS')

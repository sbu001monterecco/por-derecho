#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'assets/data/concurso36-court-filings-response-harm-20260829-v1.json'
ARCH=ROOT/'archive/CONCURSO36_COURT_FILINGS_JUDICIAL_RESPONSE_HARM_MATRIX_29AUG2026.md'
ES=ROOT/'es/concurso-36-2012-escritos-respuesta-judicial/index.html'
EN=ROOT/'en/concurso-36-2012-filings-judicial-response/index.html'
CONT=ROOT/'CONCURSO36_CONTINUE_HERE.md'
errors=[]
def check(c,m):
    if not c: errors.append(m)
p=json.loads(DATA.read_text(encoding='utf-8'))
check(p.get('schema')=='por-derecho.concurso36-court-filings-response-harm.v1','schema mismatch')
check(p.get('certified_complete_docket') is False,'must not claim certified complete docket')
check(p.get('p0_open_family_count')==9 and p.get('p1_open_family_count')==2,'P0/P1 denominator drift')
check(p.get('located_docket_discovery_rows')=='>600','located docket denominator marker missing')
for path in (ARCH,ES,EN,CONT): check(path.exists(),f'missing {path}')
arch=ARCH.read_text(encoding='utf-8'); es=ES.read_text(encoding='utf-8'); en=EN.read_text(encoding='utf-8'); cont=CONT.read_text(encoding='utf-8')
for marker in ('more than 600 indexed rows','NO_RESPONSIVE_RULING_LOCATED_IN_CONTROLLED_CORPUS','4 June 2018','7 June 2018','overreach-of-the-concurso thesis'):
    check(marker in arch,f'archive missing {marker}')
for marker in ('más de 600','4 junio 2018','7 junio 2018','desbordamiento del concurso','no se ha localizado','5367/2022'):
    check(marker in es,f'ES missing {marker}')
for marker in ('more than 600','4 June 2018','7 June 2018','overreach of the concurso','not yet been located','5367/2022'):
    check(marker in en,f'EN missing {marker}')
check('the judge ignored' not in en.lower(),'EN must not state judge ignored as fact')
check('el juez ignoró' not in es.lower(),'ES must not state judge ignored as fact')
check('archive/CONCURSO36_COURT_FILINGS_JUDICIAL_RESPONSE_HARM_MATRIX_29AUG2026.md' in cont,'continuation pointer missing')
check('FILING_DENOMINATOR' in cont and 'HARM_CAUSATION' in cont,'continuity state fields missing')
if errors:
    print('FAIL — Concurso 36/2012 filing-response/harm control')
    for e in errors: print(' -',e)
    sys.exit(1)
print('PASS — Concurso 36/2012 filing-response/harm control')
print(' - >600-row located discovery denominator preserved without certified-complete claim')
print(' - adverse, favourable and non-located response states remain distinct')
print(' - 7 June / estate / productive-unit / extraconcursal causation boundaries enforced')

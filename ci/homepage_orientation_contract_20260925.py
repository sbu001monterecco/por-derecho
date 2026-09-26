#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
EN=ROOT/"en/index.html"; ES=ROOT/"es/index.html"
errors=[]
if EN.is_file() and ES.is_file():
    en=EN.read_text(encoding="utf-8"); es=ES.read_text(encoding="utf-8")
    req_en=['href="recovery-command-center/">Recovery</a>','href="future/">Future</a>','href="por-derecho/">Por Derecho</a>','href="evidence/">Evidence</a>','id="choose-route"','How to read the record']
    req_es=['href="centro-mando-recuperacion/">Recuperación</a>','href="futuro/">Futuro</a>','href="por-derecho/">Por Derecho</a>','href="evidencia/">Evidencia</a>','id="elegir-via"','Cómo leer el expediente']
    for x in req_en:
        if x not in en: errors.append("EN missing "+x)
    for x in req_es:
        if x not in es: errors.append("ES missing "+x)
    for label,body,x in [
      ("EN",en,"institutional-capital/"),("ES",es,"capital-institucional/"),
      ("EN",en,'href="#future"'),("ES",es,'href="#futuro"'),
      ("EN",en,'class="capital-entry"'),("ES",es,'class="capital-entry"')]:
        if x in body: errors.append(label+" forbidden "+x)
    if len(en.encode())>120000: errors.append("EN homepage >120KB")
    if len(es.encode())>125000: errors.append("ES homepage >125KB")
else: errors.append("homepage missing")
if errors:
    print("HOMEPAGE ORIENTATION CONTRACT: FAIL")
    for e in errors: print("-",e)
    sys.exit(1)
print("HOMEPAGE ORIENTATION CONTRACT: PASS")

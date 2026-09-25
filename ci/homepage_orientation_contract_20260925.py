#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
EN=ROOT/"en/index.html"
ES=ROOT/"es/index.html"
errors=[]

for path in (EN,ES):
    if not path.is_file():
        errors.append(f"missing {path.relative_to(ROOT)}")

if not errors:
    en=EN.read_text(encoding="utf-8")
    es=ES.read_text(encoding="utf-8")
    required_en=[
        'href="recovery-command-center/">Recovery</a>',
        'href="future/">Future</a>',
        'href="por-derecho/">Por Derecho</a>',
        'href="evidence/">Evidence</a>',
        'href="updates/">Updates',
        'id="choose-route"',
        'How to read the record',
    ]
    required_es=[
        'href="centro-mando-recuperacion/">Recuperación</a>',
        'href="futuro/">Futuro</a>',
        'href="por-derecho/">Por Derecho</a>',
        'href="evidencia/">Evidencia</a>',
        'href="actualizaciones/">Actualizaciones',
        'id="elegir-via"',
        'Cómo leer el expediente',
    ]
    for token in required_en:
        if token not in en: errors.append("EN missing homepage contract: "+token)
    for token in required_es:
        if token not in es: errors.append("ES missing homepage contract: "+token)
    forbidden=[
      ("EN direct capital",en,"institutional-capital/"),
      ("ES direct capital",es,"capital-institucional/"),
      ("EN Future anchor",en,'href="#future"'),
      ("ES Futuro anchor",es,'href="#futuro"'),
      ("EN capital block",en,'class="capital-entry"'),
      ("ES capital block",es,'class="capital-entry"'),
    ]
    for label,body,token in forbidden:
        if token in body: errors.append(label+": "+token)
    if len(en.encode())>120000: errors.append("EN homepage exceeds 120KB orientation budget")
    if len(es.encode())>125000: errors.append("ES homepage exceeds 125KB orientation budget")

if errors:
    print("HOMEPAGE ORIENTATION CONTRACT: FAIL")
    for e in errors: print("-",e)
    sys.exit(1)
print("HOMEPAGE ORIENTATION CONTRACT: PASS")

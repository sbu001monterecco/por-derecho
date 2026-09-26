#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
checks=[
 ("en/index.html",120000,["recovery-command-center/","future/","por-derecho/","evidence/","updates/","id=\"choose-route\"","How to read the record"],["institutional-capital/","href=\"#future\"","class=\"capital-entry\""]),
 ("es/index.html",125000,["centro-mando-recuperacion/","futuro/","por-derecho/","evidencia/","actualizaciones/","id=\"elegir-via\"","Cómo leer el expediente"],["capital-institucional/","href=\"#futuro\"","class=\"capital-entry\""]),
]
errors=[]
for rel,budget,required,forbidden in checks:
 p=ROOT/rel
 if not p.is_file():
  errors.append("missing "+rel); continue
 c=p.read_text(encoding="utf-8")
 if len(c.encode())>budget: errors.append(f"{rel} exceeds byte budget")
 for token in required:
  if token not in c: errors.append(f"{rel} missing {token}")
 for token in forbidden:
  if token in c: errors.append(f"{rel} forbidden {token}")
if errors:
 print("HOMEPAGE HEALTH CONTRACT: FAIL")
 for e in errors: print("-",e)
 sys.exit(1)
print("HOMEPAGE HEALTH CONTRACT: PASS")

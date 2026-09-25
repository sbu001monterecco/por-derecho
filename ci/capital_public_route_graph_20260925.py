#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
SEEDS=[
 "en/future/index.html","es/futuro/index.html",
 "en/institutional-capital/index.html","es/capital-institucional/index.html",
 "en/private-note-programme-administration/index.html","es/administracion-programa-notas-privadas/index.html",
 "en/montana-roja/index.html","es/montana-roja/index.html",
 "en/capital-relationships/index.html","es/relaciones-de-capital/index.html",
]
errors=[]
for rel in SEEDS:
 p=ROOT/rel
 if not p.is_file(): errors.append("missing capital route: "+rel)
if errors:
 print("\n".join(errors)); sys.exit(1)
print("CAPITAL PUBLIC ROUTE GRAPH: PASS")

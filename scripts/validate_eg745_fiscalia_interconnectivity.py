#!/usr/bin/env python3
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
ASSET="assets/eg745-fiscalia-interconnectivity-20260918.js"
DATA="assets/data/eg745-fiscalia-interconnectivity-20260918.json"
HUBS=[
 "es/eg-745-respuesta-inminente-matriz-fiscalia/index.html",
 "en/eg-745-imminent-response-prosecution-matrix/index.html",
]
PAGES=[
 "es/fiscalia-inspeccion-exp-gub-745-2026/index.html",
 "en/public-prosecution-inspection-exp-gub-745-2026/index.html",
 "es/carta-abierta-ministerio-fiscal/index.html",
 "en/open-letter-public-prosecution-service/index.html",
 "es/dp-1901-2026-auto-14-septiembre-2026/index.html",
 "en/dp-1901-2026-order-14-september-2026/index.html",
 "es/fiscalia-dip-2-2026/index.html",
 "en/fiscalia-dip-2-2026/index.html",
 "es/calificacion-concurso-36-2012-vidas-paralelas/index.html",
 "en/insolvency-classification-parallel-lives/index.html",
 "es/ricardo-de-mosteyrin-sampalo/index.html",
 "en/ricardo-de-mosteyrin-sampalo/index.html",
]
def fail(msg): raise SystemExit("FAIL: "+msg)
for rel in [ASSET,DATA,*HUBS,*PAGES]:
    if not (ROOT/rel).is_file(): fail("missing "+rel)
d=json.loads((ROOT/DATA).read_text(encoding="utf-8"))
if d.get("schema")!="por-derecho.eg745-fiscalia-interconnectivity.v1": fail("schema")
if d.get("filing_status")!="PREPARED_NOT_VERIFIED_FILED": fail("filing status")
ids={n["id"] for n in d["nodes"]}
for need in ["GC-FIS-013","GC-FIS-014","GC-FIS-016","GC-FIS-017","GC-CRI-008","NAT-FIS-004"]:
    if need not in ids: fail("missing node "+need)
needle="eg745-fiscalia-interconnectivity-20260918.js"
for rel in PAGES:
    if needle not in (ROOT/rel).read_text(encoding="utf-8"): fail(rel+" not connected")
for rel in HUBS:
    txt=(ROOT/rel).read_text(encoding="utf-8")
    for token in ["DI 248","DI 113","DI 22","DIP 2","DP 1901","E.G. 745"]:
        if token not in txt: fail(rel+" missing "+token)
print("PASS: E.G. 745 Fiscalía interconnectivity graph and filing hubs are wired")

#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"assets/data/ministerio-fiscal-pdf-room-20260918.json"
ES=ROOT/"es/ministerio-fiscal-documentos-pdf/index.html"
EN=ROOT/"en/public-prosecution-pdf-document-room/index.html"
BRIDGE=ROOT/"assets/eg745-fiscalia-interconnectivity-20260918.js"
EG745_ES=ROOT/"es/fiscalia-inspeccion-exp-gub-745-2026/facsimil-visual-31-agosto-2026.html"
EG745_EN=ROOT/"en/public-prosecution-inspection-exp-gub-745-2026/visual-facsimile-31-august-2026.html"

def fail(msg): raise SystemExit("FAIL: "+msg)

data=json.loads(REG.read_text(encoding="utf-8"))
if data.get("schema")!="por-derecho.ministerio-fiscal-pdf-room.v1":
    fail("unexpected registry schema")

registered=sorted(d["pdf_path"] for d in data["documents"])
actual=sorted(str(p.relative_to(ROOT)).replace("\\","/") for p in (ROOT/"evidence/fiscalia").rglob("*.pdf"))
if registered != actual:
    missing=sorted(set(actual)-set(registered))
    stale=sorted(set(registered)-set(actual))
    fail(f"PDF registry mismatch; unregistered={missing}; stale={stale}")

for rel in registered:
    if not (ROOT/rel).is_file():
        fail("missing registered PDF "+rel)

for room in (ES,EN):
    txt=room.read_text(encoding="utf-8")
    for d in data["documents"]:
        rel="../../"+d["pdf_path"]
        if rel+"#view=FitH" not in txt:
            fail(f"{room.relative_to(ROOT)} lacks embedded viewer for {d['id']}")
        if d["id"] not in txt:
            fail(f"{room.relative_to(ROOT)} lacks evidence ID {d['id']}")
    if txt.count('type="application/pdf"') != len(data["documents"]):
        fail(f"{room.relative_to(ROOT)} viewer count mismatch")
    for marker in ["boundary","related"]:
        if marker not in txt:
            fail(f"{room.relative_to(ROOT)} lacks contextual layer {marker}")

for page in (EG745_ES,EG745_EN):
    txt=page.read_text(encoding="utf-8")
    if 'data-mf-pdf-viewer="eg745"' not in txt:
        fail(f"{page.relative_to(ROOT)} lacks EG745 PDF viewer")
    if "oficio-decreto-eg-745-2026-public-redacted.pdf#view=FitH" not in txt:
        fail(f"{page.relative_to(ROOT)} viewer path missing")

bridge=BRIDGE.read_text(encoding="utf-8")
for marker in ["../ministerio-fiscal-documentos-pdf/","../public-prosecution-pdf-document-room/"]:
    if marker not in bridge:
        fail("shared interconnectivity bridge lacks "+marker)

for d in data["documents"]:
    for key in ("context_es","context_en","boundary_es","boundary_en","related_es","related_en"):
        if not d.get(key):
            fail(f"{d['id']} lacks {key}")
    if len(d["related_es"]) < 2 or len(d["related_en"]) < 2:
        fail(f"{d['id']} needs at least two related routes")

print(f"PASS: {len(actual)} public Fiscalía PDFs are registered, embedded, contextualised and interconnected")

#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
COV=ROOT/"assets/data/ministerio-fiscal-office-digitisation-20260919.json"
REG=ROOT/"assets/data/ministerio-fiscal-pdf-room-20260918.json"
ES=ROOT/"es/ministerio-fiscal-cobertura-oficinas/index.html"
EN=ROOT/"en/public-prosecution-office-coverage/index.html"

def fail(msg):
    raise SystemExit("FAIL: "+msg)

cov=json.loads(COV.read_text(encoding="utf-8"))
reg=json.loads(REG.read_text(encoding="utf-8"))
if cov.get("schema")!="por-derecho.ministerio-fiscal-office-digitisation.v1":
    fail("unexpected coverage schema")
if cov.get("completeness_claim") is not False:
    fail("coverage must not claim completeness")
if cov["public_pdf_room"].get("current_public_pdf_count") != len(reg.get("documents",[])):
    fail("public PDF count drifts from PDF-room registry")
offices=cov.get("offices",[])
ids=[o.get("id") for o in offices]
if len(ids)!=len(set(ids)) or any(not x for x in ids):
    fail("office IDs missing or duplicated")
allowed=set(cov.get("states",[]))
for o in offices:
    if o.get("evidence_state") not in allowed:
        fail(f"invalid evidence state for {o.get('id')}")
    for key in ("name","known_lane","open_gap","links_es","links_en"):
        if not o.get(key):
            fail(f"{o.get('id')} lacks {key}")
    if int(o.get("public_viewer_pdfs",0)) < 0:
        fail("negative viewer count")
if sum(int(o.get("public_viewer_pdfs",0)) for o in offices) != len(reg["documents"]):
    fail("office viewer totals do not equal PDF-room denominator")
for page in (ES,EN):
    text=page.read_text(encoding="utf-8")
    for oid in ids:
        if f'data-office-id="{oid}"' not in text:
            fail(f"{page.relative_to(ROOT)} lacks {oid}")
    if "certified file complete" not in text.lower() and "expediente certificado completo" not in text.lower():
        fail(f"{page.relative_to(ROOT)} lacks completeness boundary")
subprocess.run([sys.executable,str(ROOT/"scripts/validate_ministerio_fiscal_pdf_room.py")],cwd=ROOT,check=True)
print(f"PASS: {len(offices)} office rows controlled; {len(reg['documents'])} public PDFs retain bilingual viewers/context/interconnectivity")

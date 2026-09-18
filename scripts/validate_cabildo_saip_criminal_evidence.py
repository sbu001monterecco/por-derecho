#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA=ROOT/"assets"/"data"
INDEX=DATA/"cabildo-six-zip-register-index-v1.json"
MAP=DATA/"cabildo-saip-criminal-evidence-map-v1.json"
PUB=DATA/"cabildo-public-pdf-manifest-v2.json"
FAMILIES=["3671_2022","2984_2023","17070_2023","19995_2023","7206_2024","4887_2025"]
ROUTES=[
 ROOT/"es"/"evidencia-recibida-cabildo-lanzarote"/"index.html",
 ROOT/"en"/"evidence-received-cabildo-lanzarote"/"index.html",
 ROOT/"es"/"cabildo-lanzarote-mapa-penal"/"index.html",
 ROOT/"en"/"cabildo-lanzarote-criminal-evidence-map"/"index.html",
]
fail=[]

def need(cond,msg):
    if not cond: fail.append(msg)

idx=json.loads(INDEX.read_text(encoding="utf-8"))
need(idx["pdf_occurrences"]==191,"index pdf_occurrences must be 191")
need(idx["unique_pdf_binaries"]==190,"index unique_pdf_binaries must be 190")
need(idx["canonical_repository"]["project_id"]==86151898,"canonical GitLab project id must remain 86151898")

rows=[]
for fam in FAMILIES:
    p=DATA/"cabildo-six-zip-register"/f"{fam}.csv"
    need(p.is_file(),f"missing family register {p}")
    if p.is_file():
        with p.open(encoding="utf-8",newline="") as fh:
            rows.extend(csv.DictReader(fh))

need(len(rows)==191,f"family occurrence rows expected 191, got {len(rows)}")
ids={r["evidence_id"] for r in rows}
need(len(ids)==190,f"unique evidence IDs expected 190, got {len(ids)}")
dup=[r for r in rows if r["evidence_id"]=="PD-CAB-SAIP-PDF-0002"]
need(len(dup)==2,"PD-CAB-SAIP-PDF-0002 must occur exactly twice")
need(len({r["sha256"] for r in dup})==1 if dup else False,"cross-family duplicate SHA must match")
need({r["family"] for r in dup}=={"2984/2023","17070/2023"},"cross-family duplicate must be 2984 + 17070")

cm=json.loads(MAP.read_text(encoding="utf-8"))
need(len(cm.get("chain",[]))==6,"criminal map must contain six file-chain records")
need("SOURCE FACT" in cm.get("method",[]),"criminal map must preserve source-fact layer")
need("OPEN_PROOF" in cm.get("method",[]),"criminal map must preserve open-proof layer")

pm=json.loads(PUB.read_text(encoding="utf-8"))
for item in pm.get("items",[]):
    if item.get("viewer_live"):
        rel=item.get("public_path")
        need(bool(rel),f"{item['evidence_id']} live viewer missing public_path")
        if rel:
            fp=ROOT/rel
            need(fp.is_file(),f"{item['evidence_id']} public PDF path missing")
            if fp.is_file():
                digest=hashlib.sha256(fp.read_bytes()).hexdigest()
                need(digest==item["public_sha256"],f"{item['evidence_id']} public PDF hash mismatch")

for route in ROUTES:
    need(route.is_file(),f"missing public route {route.relative_to(ROOT)}")
    if route.is_file():
        text=route.read_text(encoding="utf-8")
        need("GitLab" in text or "gitlab" in text,f"{route} missing canonical-reconciliation boundary")
        need("criminal" in text.lower() or "penal" in text.lower(),f"{route} missing criminal-context boundary")

control=ROOT/"archive"/"CABILDO_SAIP_CRIMINAL_EVIDENCE_PUBLICATION_CONTROL_18SEP2026.md"
need(control.is_file(),"missing publication control")
if control.is_file():
    t=control.read_text(encoding="utf-8")
    need("191 PDF occurrences / 190 unique PDF binaries" in t,"publication control denominator mismatch")
    need("86151898" in t,"publication control missing canonical GitLab project id")

if fail:
    print("FAIL")
    for x in fail: print("-",x)
    sys.exit(1)
print("PASS: Cabildo SAIP six-file evidence controls")
print(f"- occurrences: {len(rows)}")
print(f"- unique evidence objects: {len(ids)}")
print(f"- live PDF viewers: {sum(bool(x.get('viewer_live')) for x in pm.get('items',[]))}")

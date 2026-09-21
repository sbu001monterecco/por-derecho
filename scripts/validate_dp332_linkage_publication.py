#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys

ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/"evidence/courts/dp-332-2014/public-pdfs/dp332-auto-31may2016-public-transcription.pdf"
README=ROOT/"evidence/courts/dp-332-2014/README.md"
GOV=ROOT/".github/governance/SOURCE_FIDELITY_LINKAGE_VISUAL_RULE_19SEP2026.md"
MAN=ROOT/"ops/continuity/THREAD_FILE_PRESERVATION_DP332_20260919.json"
LINK=ROOT/"assets/data/dp332-di273-linkage-20260919.json"
ES=ROOT/"es/procedimientos/lz-jud-002/index.html"
EN=ROOT/"en/proceedings/lz-jud-002/index.html"

errors=[]
for p in (PDF,README,GOV,MAN,LINK,ES,EN):
    if not p.exists(): errors.append(f"missing: {p.relative_to(ROOT)}")

if PDF.exists():
    h=hashlib.sha256(PDF.read_bytes()).hexdigest()
    if h!="acf37ad9fc4901548d8efeb44d0333efdc5c5379f34d19839dc6765d2c08d22a":
        errors.append("unexpected DP332 public derivative hash")

if MAN.exists():
    data=json.loads(MAN.read_text())
    names={x["name"]:x for x in data["files"]}
    if len(data["files"])!=7: errors.append("thread file manifest must contain exactly 7 audited objects")
    if names.get("Auto prórroga actuaciones tema penal..pdf",{}).get("sha256")!="2effd2f225797e013939a36d2cee255755873790c023aba3ec53f5deabc4473c":
        errors.append("DP332 native hash missing")
    if names.get("Querella Fiscalia 273-2013.pdf",{}).get("sha256")!="6531e1cd3677ddcfa600345c38fe69e463b0418b1025f27f0ee231a0817e697e":
        errors.append("DI273 native hash missing")

for page in (ES,EN):
    if page.exists():
        s=page.read_text()
        for marker in ("dp332-auto-31may2016-public-transcription.pdf","LINKAGE","3500443220140001497","2effd2f225797e013939a36d2cee255755873790c023aba3ec53f5deabc4473c"):
            if marker not in s: errors.append(f"{page.relative_to(ROOT)} missing {marker}")

if LINK.exists():
    data=json.loads(LINK.read_text())
    if data.get("proceeding",{}).get("nig")!="3500443220140001497": errors.append("linkage NIG mismatch")
    if "conspiracy" not in data.get("not_established",[]): errors.append("linkage proof boundary missing")

if GOV.exists():
    s=GOV.read_text()
    for marker in ("Malkator [sic] (Matkator S.L.)","LINKAGE / JOINING","RED","PURPLE"):
        if marker not in s: errors.append(f"governance missing {marker}")

if errors:
    print("\n".join("ERROR: "+x for x in errors))
    sys.exit(1)
print("DP332 THREAD PRESERVATION + VIEWER GOVERNANCE: PASS")

#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
POLICY=ROOT/"assets/data/named-person-visual-control-v1.json"
INCIDENT=ROOT/"archive/AI_IMAGE_HALLUCINATION_INCIDENT_JTP_25SEP2026.md"
JTP_EN=ROOT/"en/estate-payment-counsel-independence/index.html"
JTP_ES=ROOT/"es/pago-masa-independencia-defensa/index.html"
ACTIVE_POLICY=ROOT/"assets/data/active-named-person-visual-use-20260925.json"

def blob_sha(data:bytes)->str:
    return hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()

def main()->int:
    errors=[]
    p=json.loads(POLICY.read_text(encoding="utf-8"))
    if p.get("status")!="ACTIVE_FAIL_CLOSED": errors.append("policy not active")
    if p.get("rendering_mode")!="DETERMINISTIC_COMPOSITING_ONLY": errors.append("deterministic lock missing")
    for key in ("generative_named_person_faces","generative_face_swap","generative_face_inpainting","generative_factual_text"):
        if p.get(key) is not False: errors.append(key+" must be false")
    if p.get("missing_asset_action")!="HALT_AND_REPORT": errors.append("missing asset rule changed")

    sources=p.get("canonical_jtp_actor_sources",{})
    if set(sources)!={"jtp","borja","jdam","lpam","alberto"}: errors.append("canonical actor set changed")
    for actor,row in sources.items():
        f=ROOT/row["path"]
        if not f.is_file() or f.is_symlink():
            errors.append(f"{actor}: missing/unsafe canonical source")
            continue
        raw=f.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=row["sha256"]: errors.append(f"{actor}: sha256 mismatch")
        if blob_sha(raw)!=row["git_blob_sha1"]: errors.append(f"{actor}: git blob mismatch")


    active=json.loads(ACTIVE_POLICY.read_text(encoding="utf-8"))
    if active.get("status")!="ACTIVE_FAIL_CLOSED":
        errors.append("active named-person use policy not active")
    if active.get("exact_source_required") is not True:
        errors.append("active exact-source requirement lost")
    if active.get("active_use_of_legacy_stylised_named_person_assets") is not False:
        errors.append("legacy stylised active-use prohibition lost")

    exact_five=active.get("exact_five_actor_sources",{})
    if set(exact_five)!={"fmmm","jdam","lpam","borja","alberto"}:
        errors.append("exact five-actor source set changed")
    for actor,row in exact_five.items():
        f=ROOT/row["path"]
        if not f.is_file() or f.is_symlink():
            errors.append(f"{actor}: missing/unsafe exact five-actor source")
            continue
        raw=f.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=row["sha256"]:
            errors.append(f"{actor}: five-actor sha256 mismatch")
        if blob_sha(raw)!=row["git_blob_sha1"]:
            errors.append(f"{actor}: five-actor git blob mismatch")

    legacy_names={Path(x).name for x in active.get("legacy_assets_preserved_only",[])}
    active_files=[]
    active_files.extend(ROOT.glob("*.html"))
    for sub in ("en","es"):
        d=ROOT/sub
        if d.is_dir(): active_files.extend(d.rglob("*.html"))
    assets=ROOT/"assets"
    if assets.is_dir():
        active_files.extend(assets.glob("*.js"))
        active_files.extend(assets.glob("*.mjs"))
    for f in active_files:
        try: txt=f.read_text(encoding="utf-8")
        except UnicodeDecodeError: continue
        for name in legacy_names:
            if name in txt:
                errors.append(f"{f.relative_to(ROOT)} actively references quarantined stylised named-person asset {name}")

    incident=INCIDENT.read_text(encoding="utf-8")
    for gen in p.get("rejected_generation_ids",[]):
        if gen not in incident: errors.append("rejected generation not preserved: "+gen)

    # Stylised named-person composites may survive only with an explicit
    # non-documentary representation lock.
    comp=ROOT/"assets/composites"
    if comp.is_dir():
        for sidecar in comp.glob("*.asset-map.json"):
            try: obj=json.loads(sidecar.read_text(encoding="utf-8"))
            except Exception: continue
            mode=str(obj.get("representation_mode",""))
            if "STYLIZATION" in mode and "NOT_DOCUMENTARY_PORTRAIT_EVIDENCE" not in mode:
                errors.append(f"{sidecar.relative_to(ROOT)}: stylisation lacks non-documentary lock")

    for page in (JTP_EN,JTP_ES):
        text=page.read_text(encoding="utf-8")
        for bad in p.get("banned_jtp_hallucination_markers",[]):
            if bad in text: errors.append(f"{page.relative_to(ROOT)} contains rejected hallucination marker: {bad}")
        if not (
            "jtp-payment-actor-composite-real-sources-20260925" in text
            or 'data-named-person-rendering="deterministic-exact-source"' in text
        ):
            errors.append(f"{page.relative_to(ROOT)} lacks deterministic real-source actor presentation")

    if errors:
        print("NAMED PERSON VISUAL INTEGRITY: FAIL")
        for e in sorted(set(errors)): print("- "+e)
        return 1
    print("NAMED PERSON VISUAL INTEGRITY: PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())

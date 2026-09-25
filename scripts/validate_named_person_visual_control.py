#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
policy=json.loads((ROOT/"assets/data/named-person-visual-control-v1.json").read_text(encoding="utf-8"))
errors=[]
if policy.get("status")!="ACTIVE_FAIL_CLOSED": errors.append("policy not active")
if policy.get("rendering_mode")!="DETERMINISTIC_COMPOSITING_ONLY": errors.append("deterministic-only lock missing")
for k in ("generated_faces_for_named_people","generative_face_swap","generative_face_inpainting","generative_factual_text"):
    if policy.get(k) is not False: errors.append(k+" must be false")
if policy.get("missing_asset_action")!="HALT_AND_REPORT": errors.append("missing-asset action changed")
required={"JTP","AC","JDAM","LPAM","ALBERTO_LOPEZ_VILLARRUBIA"}
if set(policy.get("current_jtp_sources",{}))!=required: errors.append("JTP actor source set changed")
for actor,row in policy.get("current_jtp_sources",{}).items():
    if actor=="JTP":
        if row.get("drive_id")!="1BCJJ-dYoREQsEcDfyIhqHZzijKwoGs9l": errors.append("JTP Drive source changed")
    else:
        path=row.get("path")
        if not path: errors.append(actor+" path missing")
        # GitHub parity may be repaired separately; validator authenticates the declared lock rather than silently substituting.
        if not row.get("git_blob_sha") or not row.get("sha256"): errors.append(actor+" byte lock missing")
incident=(ROOT/"archive/AI_IMAGE_HALLUCINATION_INCIDENT_JTP_25SEP2026.md").read_text(encoding="utf-8")
for gen in policy.get("rejected_generation_ids",[]):
    if gen not in incident: errors.append("rejected generation not documented: "+gen)
if errors:
    print("NAMED PERSON VISUAL CONTROL: FAIL")
    [print("- "+e) for e in errors]
    raise SystemExit(1)
print("NAMED PERSON VISUAL CONTROL: PASS")

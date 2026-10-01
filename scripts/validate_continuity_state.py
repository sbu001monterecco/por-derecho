#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def require(path: str) -> Path:
    p = ROOT / path
    if not p.exists():
        raise SystemExit(f"missing continuity object: {path}")
    return p

state = json.loads(require("CONTINUITY_STATE.json").read_text(encoding="utf-8"))
positions = json.loads(require("governance/POSITION_SUPERSESSION_REGISTER_20261001.json").read_text(encoding="utf-8"))
props = json.loads(require("governance/PROPOSITION_REGISTER_20261001.json").read_text(encoding="utf-8"))
sources = json.loads(require("governance/SOURCE_OBJECT_REGISTRY_20261001.json").read_text(encoding="utf-8"))
require("archive/CONTINUITY_HANDOFF_20261001.md")
require("governance/AUDIT_LOG_20261001.ndjson")
require("archive/PINK_RENT_PREMISE_REJECTION_28SEP2026.md")
require("archive/JTP_POSITION_CORRECTION_28SEP2026.md")
require("governance/DISASTER_RECOVERY_MANIFEST_20261001.json")
require("governance/CLEAN_ROOM_RECOVERY_TEST_20261001.md")

if state.get("schema") != "PD-CONTINUITY-STATE-v1":
    raise SystemExit("unexpected continuity schema")
if state.get("deletion_safety") not in {"HOLD", "SAFE"}:
    raise SystemExit("invalid deletion_safety")
ids = {p["position_id"] for p in positions.get("positions", [])}
for required_id in {"PD-PINK-POSITION-20260928-01", "PD-JTP-POSITION-20260928-01"}:
    if required_id not in ids:
        raise SystemExit(f"missing controlling position: {required_id}")

prop_ids = {p["id"] for p in props.get("propositions", [])}
for required_id in {"PD-PROP-DI248-RETURN","PD-PROP-PINK-CURRENT","PD-PROP-JTP-CURRENT","PD-PROP-MERCANTIL-RESPONSE"}:
    if required_id not in prop_ids:
        raise SystemExit(f"missing proposition: {required_id}")

source_ids = {s["source_id"] for s in sources.get("objects", [])}
for required_id in {"PD-DRIVE-POSITION-AUDIT-20260928","PD-DRIVE-CEXP-COST-20260928","MF-DI248-SRC-ARCH-01"}:
    if required_id not in source_ids:
        raise SystemExit(f"missing source registry object: {required_id}")

for page in [
    "en/montelanza-molina-pink-ac-judicial-propagation/index.html",
    "es/montelanza-molina-pink-propagacion-ac-judicial/index.html",
]:
    text = require(page).read_text(encoding="utf-8")
    for marker in ['data-pd-criminal-mechanism="20260927"', 'data-pd-position="PD-PINK-POSITION-20260928-01"']:
        if marker not in text:
            raise SystemExit(f"{page}: missing marker {marker}")

jtp = require("archive/JUAN_TOMAS_PARRILLA_CORPUS_MASTERY_AUDIT_24AUG2026.md").read_text(encoding="utf-8")
if "PD-JTP-POSITION-20260928-01" not in jtp:
    raise SystemExit("JTP current position not propagated to mastery audit")

print("continuity controls: OK")

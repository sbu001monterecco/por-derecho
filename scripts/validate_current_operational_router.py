#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        raise SystemExit(f"missing required file: {path}")
    return target.read_text(encoding="utf-8")


def require(text: str, needle: str, path: str) -> None:
    if needle not in text:
        raise SystemExit(f"{path}: missing required continuity marker: {needle}")


start = read("CURRENT_START_HERE.md")
operational = read("CURRENT_OPERATIONAL_STATE_27AUG2026.md")
handover = read("CURRENT_HANDOVER_UNITARY_RECOVERY_27AUG2026.md")
historical = read("CURRENT_UNITARY_STATE.md")
renderer = read("assets/ricpe-cnmv-visual-evidence-20260827.js")
closure_loader = read("assets/ricpe-cnmv-closure-update-20260827.js")
root_loader = read("assets/site-pre-intervencion-highlight-20260820.js")

machine_path = ROOT / "ops/CURRENT_OPERATIONAL_STATE_27AUG2026.json"
if not machine_path.is_file():
    raise SystemExit("missing machine operational router")
machine = json.loads(machine_path.read_text(encoding="utf-8"))

require(start, "CURRENT_OPERATIONAL_STATE_27AUG2026.md", "CURRENT_START_HERE.md")
require(start, "Resolve the live `main` branch first", "CURRENT_START_HERE.md")
require(start, "PD-UNITARY-STATE-20260826-01", "CURRENT_START_HERE.md")

require(operational, "PD-CURRENT-OPERATIONAL-ROUTER-20260827-01", "CURRENT_OPERATIONAL_STATE_27AUG2026.md")
require(operational, "not a promise that a checked-in SHA remains the live head forever", "CURRENT_OPERATIONAL_STATE_27AUG2026.md")
require(operational, "HISTORICAL", "CURRENT_OPERATIONAL_STATE_27AUG2026.md")
require(operational, "san-telmo-ricpe-sun-park-stamp-v1-ES.png", "CURRENT_OPERATIONAL_STATE_27AUG2026.md")
require(operational, "pwc-five-actors-plus-ac-2016-knowledge-checkpoint-ES.png", "CURRENT_OPERATIONAL_STATE_27AUG2026.md")

require(handover, "CURRENT_START_HERE.md", "CURRENT_HANDOVER_UNITARY_RECOVERY_27AUG2026.md")
require(handover, "CURRENT_OPERATIONAL_STATE_27AUG2026.md", "CURRENT_HANDOVER_UNITARY_RECOVERY_27AUG2026.md")
require(handover, "PD-UNITARY-STATE-20260826-01", "CURRENT_HANDOVER_UNITARY_RECOVERY_27AUG2026.md")

require(historical, "PD-UNITARY-STATE-20260826-01", "CURRENT_UNITARY_STATE.md")

if machine.get("control_id") != "PD-CURRENT-OPERATIONAL-ROUTER-20260827-01":
    raise SystemExit("machine router: wrong control_id")
if machine.get("dynamic_resolution_required") is not True:
    raise SystemExit("machine router: dynamic_resolution_required must be true")
if machine.get("historical_release_preservation", {}).get("control_id") != "PD-UNITARY-STATE-20260826-01":
    raise SystemExit("machine router: historical 26-Aug control not preserved")
if machine.get("external_action_authority", {}).get("email") is not False:
    raise SystemExit("machine router: external email authority boundary weakened")

for png in (
    "san-telmo-ricpe-sun-park-stamp-v1-ES.png",
    "pwc-five-actors-plus-ac-2016-knowledge-checkpoint-ES.png",
):
    require(renderer, png, "assets/ricpe-cnmv-visual-evidence-20260827.js")
    if not (ROOT / "evidence/ricpe-cnmv/2026-08-27" / png).is_file():
        raise SystemExit(f"missing published RICPE/CNMV PNG: {png}")

require(closure_loader, "ricpe-cnmv-visual-evidence-20260827.js", "assets/ricpe-cnmv-closure-update-20260827.js")
require(root_loader, "ricpe-cnmv-closure-update-20260827.js", "assets/site-pre-intervencion-highlight-20260820.js")

print("PASS current operational router continuity")

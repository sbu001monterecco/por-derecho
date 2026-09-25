#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
POLICY=ROOT/".github/governance/THREAD_DELETION_SAFETY_SENTINEL_25SEP2026.md"
CONFIG=ROOT/"assets/data/thread-deletion-safety-sentinel-v1.json"

def main():
    if not POLICY.is_file() or not CONFIG.is_file():
        raise SystemExit("thread-safety sentinel files missing")
    data=json.loads(CONFIG.read_text(encoding="utf-8"))
    if data.get("control_id")!="PD-THREAD-SENTINEL-20260925-01":
        raise SystemExit("wrong sentinel control id")
    if data.get("default_state")!="ORANGE":
        raise SystemExit("new substantive threads must default ORANGE")
    states=data.get("states",{})
    if set(states)!={"GREEN","ORANGE","RED"}:
        raise SystemExit("sentinel must have exactly GREEN ORANGE RED")
    cues=data.get("visible_cues",{})
    expected={
        "GREEN":"🟢 THREAD — safe to delete",
        "ORANGE":"🟠 THREAD — preservation pending",
        "RED":"🔴 THREAD — do not delete",
    }
    if cues!=expected:
        raise SystemExit("visible cue contract changed")
    if states["GREEN"].get("deletion_allowed") is not True:
        raise SystemExit("GREEN must permit deletion")
    if states["ORANGE"].get("deletion_allowed") is not False or states["RED"].get("deletion_allowed") is not False:
        raise SystemExit("ORANGE and RED must block deletion")
    hard=set(states["RED"].get("hard_triggers",[]))
    for item in ("UNIQUE_CHAT_ONLY_MATERIAL","CHAT_BOUND_AUTOMATION_OR_TASK","LOCAL_ONLY_MATERIAL_WORK"):
        if item not in hard:
            raise SystemExit("missing RED trigger: "+item)
    policy=POLICY.read_text(encoding="utf-8")
    for marker in (
        "🟢 GREEN — SAFE TO DELETE",
        "🟠 ORANGE — PRESERVATION PENDING",
        "🔴 RED — DO NOT DELETE",
        "Automatic state transitions",
        "ChatGPT-level behavior",
        "Google Drive rule",
        "RED means deletion causes harm. ORANGE means deletion safety is not yet proved. GREEN means the work can continue without the chat."
    ):
        if marker not in policy:
            raise SystemExit("policy marker missing: "+marker)
    print("thread deletion-safety sentinel: OK")

if __name__=="__main__":
    main()

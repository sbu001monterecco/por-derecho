#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / ".github/governance/ARTIFACT_LIFECYCLE_CROSS_SURFACE_RECONCILIATION_07OCT2026.md"
CONFIG = ROOT / "assets/data/artifact-lifecycle-cross-surface-v1.json"
AGENTS = ROOT / "AGENTS.md"
START = ROOT / "CHATGPT_START_HERE.md"

CONTROL = "PD-GOV-ARTIFACT-LIFECYCLE-20261007-01"

def require(cond, msg):
    if not cond:
        raise SystemExit(msg)

def main():
    require(POLICY.exists(), "missing artifact lifecycle policy")
    require(CONFIG.exists(), "missing artifact lifecycle config")
    policy = POLICY.read_text(encoding="utf-8")
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    agents = AGENTS.read_text(encoding="utf-8")
    start = START.read_text(encoding="utf-8")

    require(CONTROL in policy, "policy missing control id")
    require(cfg.get("control_id") == CONTROL, "config control id mismatch")
    require("Mandatory write-back" in policy, "policy missing write-back gate")
    require("Reconciliation before “not found”" in policy, "policy missing reconciliation gate")
    require("Gmail Draft count is not an outstanding-task count." in policy, "policy missing Gmail draft boundary")
    require(CONTROL in agents, "AGENTS missing artifact lifecycle pickup")
    require(CONTROL in start, "CHATGPT_START_HERE missing artifact lifecycle pickup")

    order = cfg.get("required_reconciliation_order", [])
    require(order[:3] == ["conversation_files","chatgpt_library","canonical_private_drive"],
            "reconciliation order must begin conversation/files -> Library -> canonical Drive")

    states = set(cfg.get("lifecycle_states", []))
    for state in ("WORKING","APPROVED","SIGNED","SUBMITTED","REGISTERED","SUPERSEDED","HOLD","UNKNOWN"):
        require(state in states, f"missing lifecycle state {state}")

    require(cfg.get("library_only_active_artifact") == "AMBER_WRITEBACK_PENDING",
            "Library-only active artifact must fail closed to AMBER")

    print(f"{CONTROL}: PASS")
    print("- Library-only active reusable artifacts require canonical write-back or explicit AMBER gap")
    print("- absence claims require cross-surface scoped reconciliation")
    print("- Gmail Draft is not a task/current-version register")
    print("- policy/manual/runtime/assurance states remain separate")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Read-only audit for the zero-cost GitHub agent pilot.

This script deliberately verifies only repository-observable facts. It does not
claim account-level Copilot, CodeQL, secret-scanning, ruleset, billing or quota
state.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "ops/continuity/GITHUB_FREE_AGENT_PILOT_20260919.json"
PILOT_WORKFLOW = ROOT / ".github/workflows/github-free-agent-pilot.yml"

REQUIRED = [
    "AGENTS.md",
    "CHATGPT_START_HERE.md",
    ".github/copilot-instructions.md",
    ".github/dependabot.yml",
    ".github/workflows/outage-backend-parity.yml",
    ".github/workflows/release-acceptance.yml",
    ".github/workflows/publication-integrity-gate.yml",
    ".github/workflows/verify-publication-live.yml",
    ".github/workflows/off-github-preservation.yml",
    ".github/workflows/repository-backup-bundle.yml",
    ".github/workflows/tech-platform-monitor.yml",
    "ops/continuity/GITHUB_OPERATIONAL_BACKEND_RECOVERY_20260917.md",
]

FORBIDDEN_PILOT_MARKERS = [
    "contents: write",
    "pull-requests: write",
    "issues: write",
    "git push",
    "gh pr merge",
    "gh api",
]

def fail(message: str) -> None:
    raise SystemExit(message)

def main() -> None:
    if not CONTROL.is_file():
        fail("pilot control missing")
    control = json.loads(CONTROL.read_text(encoding="utf-8"))

    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        fail("required controls missing: " + ", ".join(missing))

    if control.get("phase") != "PHASE_1_ADVISORY":
        fail("pilot must remain advisory in phase 1")
    if control["cost_policy"].get("maximum_authorised_spend") != "0":
        fail("pilot cost boundary is not zero")
    if control["authority_boundary"].get("autonomous_merge_to_main") is not False:
        fail("autonomous merge must remain disabled")
    if control["authority_boundary"].get("substantive_legal_or_evidential_rewriting") is not False:
        fail("substantive autonomous rewriting must remain disabled")
    if control["authority_boundary"].get("new_required_repository_wide_gate") is not False:
        fail("pilot may not self-promote to a required hard gate")

    if not PILOT_WORKFLOW.is_file():
        fail("pilot workflow missing")
    workflow = PILOT_WORKFLOW.read_text(encoding="utf-8").lower()
    if "permissions:\n  contents: read" not in workflow:
        fail("pilot workflow is not explicitly contents-read")
    for marker in FORBIDDEN_PILOT_MARKERS:
        if marker in workflow:
            fail(f"pilot workflow contains forbidden write marker: {marker}")

    workflow_count = len(list((ROOT / ".github/workflows").glob("*.yml"))) + len(
        list((ROOT / ".github/workflows").glob("*.yaml"))
    )

    report = {
        "status": "PASS",
        "phase": control["phase"],
        "issue": control["issue"],
        "required_controls_checked": len(REQUIRED),
        "github_workflow_files_observed": workflow_count,
        "logical_workers": sorted(control["logical_workers"]),
        "cost_boundary": control["cost_policy"]["maximum_authorised_spend"],
        "repository_write_authority": False,
        "account_level_state_claimed": False,
        "account_level_checks_pending": control[
            "account_level_checks_not_proved_by_repository_source"
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

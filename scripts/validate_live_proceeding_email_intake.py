#!/usr/bin/env python3
"""Validate the live-proceeding email-intake governance package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE = ROOT / ".github/governance/LIVE_PROCEEDING_EMAIL_INTAKE_GOVERNANCE_01SEP2026.md"
CONTROL = ROOT / "ops/LIVE_PROCEEDING_EMAIL_INTAKE_V1.json"
COMMUNICATIONS = ROOT / "assets/data/institutional-communications-register-v1.json"
PROCEEDINGS = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
PUBLIC_PROCEEDINGS = ROOT / "assets/data/proceedings-master-public-v1.json"
WORKSPACE_REGISTER = ROOT / "data/workspace-register-v1.json"
CURRENT_HANDOFF = ROOT / "CURRENT_WORKSPACE_HANDOFF.md"
WORKSPACE_ID = "PD-WS-20260901-0004"
CONTROL_ID = "PD-LPEI-001"
EMAIL_RE = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
EXPECTED_LADDER = [
    "transmission",
    "registration",
    "delivery",
    "routing",
    "incorporation",
    "examination",
    "verification_or_rejection",
    "adoption",
    "decision_or_use",
    "effect",
    "causation",
    "benefit_or_loss",
]


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    for path in (GOVERNANCE, CONTROL, COMMUNICATIONS, PROCEEDINGS, PUBLIC_PROCEEDINGS, WORKSPACE_REGISTER, CURRENT_HANDOFF):
        if not path.exists():
            fail(f"missing required path: {path.relative_to(ROOT)}", errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    governance = GOVERNANCE.read_text(encoding="utf-8")
    control_text = CONTROL.read_text(encoding="utf-8")
    try:
        control = json.loads(control_text)
        communications = json.loads(COMMUNICATIONS.read_text(encoding="utf-8"))
        workspace_register = json.loads(WORKSPACE_REGISTER.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"FAIL: invalid JSON in controlled intake inputs: {exc}", file=sys.stderr)
        return 1

    if control.get("schema") != "por-derecho.live-proceeding-email-intake.v1":
        fail("unexpected machine-control schema", errors)
    if control.get("control_id") != CONTROL_ID:
        fail("machine-control ID drift", errors)
    if control.get("workspace_id") != WORKSPACE_ID:
        fail("machine-control workspace drift", errors)
    if control.get("status") != "ACTIVE_SPECIALIST_CONTROL":
        fail("specialist control is not active", errors)

    architecture = control.get("architecture", {})
    negative_flags = (
        "shadow_email_register_allowed",
        "silent_overwrite_allowed",
        "subject_only_proceeding_match_allowed",
        "duplicate_event_on_rerun_allowed",
        "unsupported_state_mutation_allowed",
        "deadline_without_source_allowed",
        "assumption_based_conflict_resolution_allowed",
    )
    for field in negative_flags:
        if architecture.get(field) is not False:
            fail(f"unsafe architecture flag is not false: {field}", errors)
    if architecture.get("append_only_history") is not True:
        fail("append-only history must remain enabled", errors)

    private = control.get("private_custody", {})
    for field in (
        "native_email_body_public",
        "provider_message_id_public",
        "provider_thread_id_public",
        "recipient_identity_public_by_default",
        "private_attachment_content_public_by_default",
    ):
        if private.get(field) is not False:
            fail(f"public/private boundary drift: {field}", errors)

    if control.get("default_timezone") != "Atlantic/Canary":
        fail("default action timezone must remain Atlantic/Canary", errors)
    if control.get("handling_state_ladder") != EXPECTED_LADDER:
        fail("intake handling-state ladder drift", errors)

    destinations = control.get("canonical_destinations", {})
    expected_destinations = {
        "communications_graph": "assets/data/institutional-communications-register-v1.json",
        "proceedings_source": "archive/PROCEEDINGS_MASTER_REGISTER.csv",
        "proceedings_public_projection": "assets/data/proceedings-master-public-v1.json",
        "workspace_register": "data/workspace-register-v1.json",
        "continuity_index": "CURRENT_WORKSPACE_HANDOFF.md",
    }
    for field, expected in expected_destinations.items():
        if destinations.get(field) != expected:
            fail(f"canonical destination drift for {field}", errors)

    governance_markers = (
        CONTROL_ID,
        WORKSPACE_ID,
        "subject-only matching is prohibited",
        "append one canonical event",
        "preserve supersession",
        "extract operational consequences",
        "refresh interlinks and search",
        "contradictions require review",
        "checkpoint continuity",
        "shadow email register",
        "assets/data/institutional-communications-register-v1.json",
        "archive/PROCEEDINGS_MASTER_REGISTER.csv",
    )
    governance_lower = governance.lower()
    for marker in governance_markers:
        if marker.lower() not in governance_lower:
            fail(f"governance marker missing: {marker}", errors)

    if EMAIL_RE.search(governance) or EMAIL_RE.search(control_text):
        fail("governance package contains a literal email address", errors)

    continuity_rules = communications.get("continuity_rules", [])
    if not any("provider identifiers" in rule for rule in continuity_rules):
        fail("canonical communications register lacks provider-identifier privacy rule", errors)
    if not any("receipt-to-decision" in rule for rule in continuity_rules):
        fail("canonical communications register lacks handling-state source rule", errors)

    workspace = next((row for row in workspace_register.get("workspaces", []) if row.get("workspace_id") == WORKSPACE_ID), None)
    if workspace is None:
        fail(f"workspace register lacks {WORKSPACE_ID}", errors)
    elif workspace.get("handoff_path") != "archive/handoffs/2026-09-01-live-proceeding-email-intake-workspace-handoff.md":
        fail("workspace handoff path drift", errors)

    handoff = CURRENT_HANDOFF.read_text(encoding="utf-8")
    for marker in (WORKSPACE_ID, "LIVE_PROCEEDING_EMAIL_INTAKE_GOVERNANCE_01SEP2026.md"):
        if marker not in handoff:
            fail(f"current workspace continuity index lacks {marker}", errors)

    external = control.get("external_authority", {})
    if any(external.get(field) is not False for field in external):
        fail("intake governance must not self-authorise external action", errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print("Live proceeding email-intake governance controls pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

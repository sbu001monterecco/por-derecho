#!/usr/bin/env python3
"""Validate the time-bounded GitHub-first continuity horizon."""
from __future__ import annotations

import datetime as dt
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTROL = ROOT / "ops" / "continuity" / "GITHUB_FIRST_48H_PLUS_36H_CONTINUITY_PLAN_20260917.json"

REQUIRED_CLASSES = {
    "EXACT_GITLAB_RECOVERY",
    "EXACT_ALREADY_MIRRORED",
    "FUNCTIONAL_GITHUB_EQUIVALENT",
    "PENDING_GITLAB_RESTORATION",
}
REQUIRED_GATES = {
    "Outage backend parity / validate",
    "PD release acceptance",
    "Publication integrity gate / publication-integrity",
}

def parse_utc(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))

def validate() -> list[str]:
    failures: list[str] = []
    data = json.loads(CONTROL.read_text(encoding="utf-8"))

    if data.get("schema") != "por-derecho.github-first-continuity-horizon.v1":
        failures.append("schema_mismatch")
    if data.get("status") != "ACTIVE":
        failures.append("plan_not_active")

    sha = data.get("baseline_github_main_sha", "")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        failures.append("baseline_sha_invalid")

    phases = data.get("phases", [])
    if [p.get("id") for p in phases] != [
        "GITHUB_FIRST_HARDENING",
        "STABILIZATION_RECONCILIATION_READINESS",
    ]:
        failures.append("phase_order_invalid")
    if [p.get("duration_hours") for p in phases] != [48, 36]:
        failures.append("phase_duration_invalid")
    if data.get("total_hours") != 84:
        failures.append("total_hours_invalid")

    try:
        start = parse_utc(data["start_utc"])
        end = parse_utc(data["end_utc"])
        if end - start != dt.timedelta(hours=84):
            failures.append("horizon_duration_mismatch")
        if len(phases) == 2:
            p0s, p0e = parse_utc(phases[0]["start_utc"]), parse_utc(phases[0]["end_utc"])
            p1s, p1e = parse_utc(phases[1]["start_utc"]), parse_utc(phases[1]["end_utc"])
            if p0s != start or p0e != p1s or p1e != end:
                failures.append("phase_boundary_mismatch")
            if p0e - p0s != dt.timedelta(hours=48):
                failures.append("phase_a_clock_mismatch")
            if p1e - p1s != dt.timedelta(hours=36):
                failures.append("phase_b_clock_mismatch")
    except (KeyError, ValueError):
        failures.append("invalid_horizon_timestamp")

    if set(data.get("recovery_classes", [])) != REQUIRED_CLASSES:
        failures.append("recovery_classes_invalid")
    if set(data.get("required_exact_head_gates", [])) != REQUIRED_GATES:
        failures.append("exact_head_gates_invalid")

    probe = data.get("gitlab_probe_policy", {})
    if probe.get("authenticated_probe_before_clear_restoration_signal") is not False:
        failures.append("gitlab_probe_fail_closed_missing")
    if probe.get("bounded_authenticated_verification_after_clear_signal") is not True:
        failures.append("restoration_verification_missing")

    preservation = data.get("preservation_policy", {})
    for key in (
        "checkpoint_after_material_main_change",
        "off_github_snapshot_once_per_material_main_sha",
        "duplicate_compute_prohibited",
    ):
        if preservation.get(key) is not True:
            failures.append(f"preservation_policy_missing:{key}")

    merge = data.get("merge_policy", {})
    if merge.get("branches_and_prs_required") is not True:
        failures.append("pr_policy_missing")
    if merge.get("exact_head_gates_required") is not True:
        failures.append("exact_head_gate_policy_missing")
    for key in (
        "force_push_allowed",
        "history_deletion_allowed",
        "mass_merge_stale_prs_allowed",
        "weaken_controls_to_merge_allowed",
    ):
        if merge.get(key) is not False:
            failures.append(f"unsafe_merge_policy:{key}")

    evidence = data.get("evidence_policy", {})
    if evidence.get("private_evidence_publication_allowed") is not False:
        failures.append("private_evidence_boundary_missing")
    if evidence.get("exact_gitlab_bytes_from_memory_or_snippets_allowed") is not False:
        failures.append("exact_byte_truth_boundary_missing")
    if evidence.get("source_provenance_required_for_recovery") is not True:
        failures.append("recovery_provenance_requirement_missing")

    pending = " ".join(data.get("gitlab_native_pending", [])).lower()
    for token in ("duo", "mr discussions", "pipelines", "variables", "runners", "settings", "orbit"):
        if token not in pending:
            failures.append(f"gitlab_native_pending_missing:{token}")

    return failures

def main() -> int:
    failures = validate()
    if failures:
        print(json.dumps({"status": "FAIL", "failures": failures}, indent=2))
        return 1
    print(json.dumps({"status": "PASS", "control": str(CONTROL.relative_to(ROOT))}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

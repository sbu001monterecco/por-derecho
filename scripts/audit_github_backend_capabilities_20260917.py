#!/usr/bin/env python3
"""Audit reconstructible GitHub operational-backend capabilities during the GitLab outage.

This audit measures repository-hosted controls only. It deliberately excludes GitLab-native
platform objects (Duo sessions, MR discussions, pipeline database state, variables, runners,
Orbit/index state) from the repository-capability denominator rather than pretending they can
be reconstructed from Git.
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

CAPABILITIES: dict[str, tuple[str, ...]] = {
    "registry": (
        "assets/data/matter-identity-registry-v1.json",
        "assets/data/matter-identity-operational-control-v1.json",
        "archive/PROCEEDINGS_MASTER_REGISTER.csv",
    ),
    "evidence_intelligence": (
        ".github/evidence-intelligence/README.md",
        ".github/evidence-intelligence/TECH_PLATFORM_ROADMAP.md",
        ".github/evidence-intelligence/id-extension-policy.json",
        ".github/evidence-intelligence/scripts/validate_identity_compatibility.py",
        ".github/evidence-intelligence/scripts/run_rpl2523_retrieval_pilot.py",
        ".github/evidence-intelligence/scripts/monitor_tech_platform.py",
        ".github/workflows/tech-platform-monitor.yml",
    ),
    "reasoning_frameworks": (
        "research/por-derecho/second-pair-of-eyes/validate.py",
        "assets/data/por-derecho-second-pair-applications.json",
        "assets/data/proceedings-case-prism-v1.json",
        "scripts/build_proceedings_case_prism_v2.py",
    ),
    "release_and_preservation": (
        "ops/PUBLICATION_CONTROLLER.md",
        ".github/workflows/publication-integrity-gate.yml",
        ".github/workflows/off-github-preservation.yml",
    ),
    "agent_and_continuity_governance": (
        "AGENTS.md",
        ".github/copilot-instructions.md",
        "ops/duo/DUO_ORCHESTRATION_PROTOCOL_20260917.md",
        "ops/continuity/GITHUB_OPERATIONAL_BACKEND_RECOVERY_20260917.md",
        "ops/continuity/GITHUB_OPERATIONAL_BACKEND_PARITY_20260917.json",
        "ops/continuity/GITLAB_EXACT_RECOVERY_QUEUE_20260917.json",
        "ops/continuity/GITHUB_FIRST_48H_PLUS_36H_CONTINUITY_PLAN_20260917.md",
        "ops/continuity/GITHUB_FIRST_48H_PLUS_36H_CONTINUITY_PLAN_20260917.json",
        "ops/continuity/GITLAB_PUBLIC_SURFACE_RECOVERY_LEDGER_20260918.json",
        "scripts/classify_public_impact_shadow_20260917.py",
        "scripts/validate_continuity_horizon_20260917.py",
        "scripts/validate_gitlab_public_surface_recovery_20260918.py",
        ".github/workflows/outage-backend-parity.yml",
    ),
}

PLATFORM_NATIVE_GAPS = (
    "GitLab merge-request discussions and approvals",
    "GitLab issues/work-items and Duo session state",
    "GitLab pipeline/job database history and artifacts not mirrored into Git",
    "GitLab CI variables, runner/environment and project/group settings",
    "GitLab Orbit/index state",
)


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def audit() -> dict:
    failures: list[str] = []
    categories: dict[str, dict] = {}
    passed = 0
    total = 0

    for category, paths in CAPABILITIES.items():
        category_failures: list[str] = []
        for relative in paths:
            total += 1
            path = ROOT / relative
            if path.is_file():
                passed += 1
            else:
                category_failures.append(f"missing:{relative}")
                failures.append(f"missing:{relative}")
        categories[category] = {
            "required": len(paths),
            "present": len(paths) - len(category_failures),
            "failures": category_failures,
        }

    # Semantic invariants: existence alone is insufficient.
    registry = json.loads(read_text("assets/data/matter-identity-registry-v1.json"))
    if registry.get("registry_id") != "PD-SP-IDENTITY-REGISTRY-001":
        failures.append("registry_id_mismatch")
    if registry.get("counts", {}).get("total") != 380:
        failures.append("registry_denominator_drift")

    parity = json.loads(read_text("ops/continuity/GITHUB_OPERATIONAL_BACKEND_PARITY_20260917.json"))
    if parity.get("status") != "ACTIVE_OUTAGE_CONTINUITY":
        failures.append("outage_parity_not_active")
    if parity.get("last_verified_gitlab_main_sha") != "7d086d098676eecc2c1647ed09b348d8dc0bdc69":
        failures.append("gitlab_anchor_drift")

    queue = json.loads(read_text("ops/continuity/GITLAB_EXACT_RECOVERY_QUEUE_20260917.json"))
    if queue.get("status") != "OPEN_BLOCKED_BY_GITLAB_AUTHENTICATION":
        failures.append("exact_recovery_queue_state_changed")
    if len(queue.get("items", [])) < 6:
        failures.append("exact_recovery_queue_incomplete")

    horizon = json.loads(read_text("ops/continuity/GITHUB_FIRST_48H_PLUS_36H_CONTINUITY_PLAN_20260917.json"))
    if horizon.get("status") != "ACTIVE":
        failures.append("continuity_horizon_not_active")
    if horizon.get("total_hours") != 84:
        failures.append("continuity_horizon_duration_drift")

    public_recovery = json.loads(read_text("ops/continuity/GITLAB_PUBLIC_SURFACE_RECOVERY_LEDGER_20260918.json"))
    if public_recovery.get("status") != "ACTIVE_PUBLIC_ONLY":
        failures.append("gitlab_public_surface_ledger_not_active")
    if public_recovery.get("authenticated_gitlab_restoration_verified") is not False:
        failures.append("gitlab_public_surface_ledger_claims_auth_restoration")
    if not public_recovery.get("items"):
        failures.append("gitlab_public_surface_ledger_empty")

    tech_monitor = read_text(".github/workflows/tech-platform-monitor.yml")
    for needle in ("validate_identity_compatibility.py", "run_rpl2523_retrieval_pilot.py", "monitor_tech_platform.py"):
        if needle not in tech_monitor:
            failures.append(f"tech_monitor_missing:{needle}")

    preservation = read_text(".github/workflows/off-github-preservation.yml")
    # Verify capabilities semantically rather than requiring one exact shell spelling.
    for needle in ("git clone --mirror", "fsck --full", "actions/upload-artifact"):
        if needle not in preservation:
            failures.append(f"preservation_missing:{needle}")

    controller = read_text("ops/PUBLICATION_CONTROLLER.md")
    for needle in ("/pd-release claim", "/pd-release verify", "compare-and-swap"):
        if needle not in controller:
            failures.append(f"publication_controller_missing:{needle}")

    outage_workflow = read_text(".github/workflows/outage-backend-parity.yml")
    if "- main" not in outage_workflow:
        failures.append("outage_parity_not_monitoring_main")
    if "audit_github_backend_capabilities_20260917.py" not in outage_workflow:
        failures.append("capability_audit_not_wired")
    if "validate_continuity_horizon_20260917.py" not in outage_workflow:
        failures.append("continuity_horizon_not_wired")
    if "validate_gitlab_public_surface_recovery_20260918.py" not in outage_workflow:
        failures.append("gitlab_public_surface_validation_not_wired")

    report = {
        "schema": "por-derecho.github-backend-capability-audit.v1",
        "status": "PASS" if not failures else "FAIL",
        "repository_capabilities": {
            "controls_present": passed,
            "controls_required": total,
            "coverage_percent": round((passed / total) * 100, 2) if total else 0.0,
            "categories": categories,
        },
        "platform_native_gaps_excluded_from_repository_denominator": list(PLATFORM_NATIVE_GAPS),
        "failures": failures,
        "truth_boundary": "100% repository-control coverage is not 100% GitLab platform parity.",
    }
    return report


def main() -> int:
    report = audit()
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

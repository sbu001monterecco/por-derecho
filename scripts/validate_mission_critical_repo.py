#!/usr/bin/env python3
"""Mission-critical repository policy guard for Por Derecho.

This guard validates repository-controlled invariants that should not depend on
a particular AI session or operator workstation. GitHub settings that are not
observable/writable from source remain explicit operational blockers.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
FULL_SHA_USES = re.compile(r"^\s*(?:-\s+)?uses:\s+([^#\s]+)\s*(?:#.*)?$", re.MULTILINE)
WRITE_SCOPE = re.compile(r"^\s{2,}([A-Za-z0-9_-]+):\s*write\s*$", re.MULTILINE)
SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")

CURRENT_SCHEMA_V2 = "por-derecho.operational-truth.current-state.v2"
PRODUCTION_SCHEMA_V2 = "por-derecho.operational-truth.production-status.v2"
ROLLBACK_SCHEMA_V2 = "por-derecho.operational-truth.rollback-anchor.v2"
LEDGER_SCHEMA_V1 = "por-derecho.operational-truth.release-ledger.v1"

REQUIRED_FILES = [
    "AGENTS.md",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    ".github/workflows/production-smoke-monitor.yml",
    ".github/workflows/repository-backup-bundle.yml",
    ".github/workflows/verify-mission-critical-hardening-live.yml",
    ".github/workflows/validate-operational-truth.yml",
    "scripts/validate_publication_integrity.py",
    "scripts/validate_repository_preservation.py",
    "scripts/production_smoke_check.py",
    "scripts/generate_operational_truth.py",
    "scripts/validate_operational_truth.py",
    "ops/GITHUB_MISSION_CRITICAL_RUNBOOK.md",
    "ops/CRITICAL_PATHS.txt",
    "ops/REPOSITORY_PRESERVATION_CONTRACT.json",
    "ops/FIVE_ACTOR_PRESERVATION_AND_READER_JOURNEY_BACKLOG.md",
    "ops/CURRENT_STATE.json",
    "ops/PRODUCTION_STATUS.json",
    "ops/LAST_KNOWN_GOOD.json",
    "ops/RELEASE_LEDGER.json",
    "ops/OPERATIONAL_TRUTH_PROTOCOL.md",
    "ops/INCIDENT_TEMPLATE.md",
    "operations/preservation-authorizations/README.md",
    "archive/FIVE_ACTOR_FRONT_PAGE_AND_DIRECT_ROUTE_PRESERVATION_LOCK_24AUG2026.md",
    "publication-manifests/five-actor-accountability-preservation-20260824.json",
    "docs/deletion-audits/2026-08-24-five-actor-visibility-preservation-thread.md",
    "deployment-probes/mission-critical-hardening-20260818.json",
]
ALLOWED_WRITE = {
    "verify-pages-propagation-optimum.yml": {"statuses"},
    "verify-mission-critical-hardening-live.yml": {"statuses"},
    "verify-ricpe-channel-status-live.yml": {"statuses"},
    "verify-adjudicacion-2022-live.yml": {"statuses"},
    "verify-criminal-engineering-investigation-live.yml": {"statuses"},
    "verify-san-telmo-rendered-attribution-live.yml": {"statuses"},
    "verify-por-derecho-foundation-stage-3-live.yml": {"statuses"},
    "verify-por-derecho-seller-readiness-live.yml": {"statuses"},
    "verify-ac-community-de-facto-administration-live.yml": {"statuses"},
    "verify-eleconomista-live.yml": {"statuses"},
    "verify-meeting-point-final-propagation-live.yml": {"statuses"},
    "production-smoke-monitor.yml": {"issues"},
    "repository-backup-bundle.yml": {"statuses"},
}


def error(message: str, errors: list[str]) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        error(f"{path.relative_to(ROOT)} invalid JSON: {exc}", errors)
        return None
    if not isinstance(value, dict):
        error(f"{path.relative_to(ROOT)} root must be an object", errors)
        return None
    return value


def validate_workflows(errors: list[str]) -> None:
    if not WORKFLOWS.is_dir():
        error(".github/workflows is missing", errors)
        return

    for path in sorted(WORKFLOWS.glob("*.yml")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        if "pull_request_target:" in text:
            error(f"{rel}: pull_request_target is prohibited", errors)
        if not re.search(r"^permissions:\s*$", text, re.MULTILINE):
            error(f"{rel}: explicit top-level permissions block is required", errors)
        if "timeout-minutes:" not in text:
            error(f"{rel}: every workflow job family must have an explicit timeout", errors)

        for ref in FULL_SHA_USES.findall(text):
            if ref.startswith("./") or ref.startswith("docker://"):
                continue
            if "@" not in ref:
                error(f"{rel}: external action has no immutable ref: {ref}", errors)
                continue
            action, version = ref.rsplit("@", 1)
            if not re.fullmatch(r"[0-9a-fA-F]{40}", version):
                error(f"{rel}: external action is not pinned to a full 40-char SHA: {action}@{version}", errors)

        writes = set(WRITE_SCOPE.findall(text))
        if "contents" in writes:
            error(f"{rel}: contents: write is prohibited for production workflows", errors)
        allowed = ALLOWED_WRITE.get(path.name, set())
        unexpected = writes - allowed
        if unexpected:
            error(f"{rel}: unexpected write permission(s): {sorted(unexpected)}", errors)


def validate_production_status(data: dict, errors: list[str]) -> None:
    if data.get("schema") == PRODUCTION_SCHEMA_V2:
        required = [
            "record_type",
            "observed_at",
            "production_repository",
            "production_branch",
            "public_host",
            "served_sha",
            "source_tree_sha",
            "deployment",
            "verification",
            "relationship_to_current_state",
        ]
        for key in required:
            if key not in data:
                error(f"ops/PRODUCTION_STATUS.json missing {key}", errors)
        if data.get("record_type") != "OBSERVED_GITHUB_PAGES_DEPLOYMENT":
            error("ops/PRODUCTION_STATUS.json v2 must describe an observed Pages deployment", errors)
        for key in ("served_sha", "source_tree_sha"):
            if not SHA_RE.fullmatch(str(data.get(key, ""))):
                error(f"ops/PRODUCTION_STATUS.json {key} must be a 40-char SHA", errors)
        deployment = data.get("deployment") or {}
        if deployment.get("status") != "completed":
            error("ops/PRODUCTION_STATUS.json deployment must be completed", errors)
        if deployment.get("conclusion") != "success":
            error("ops/PRODUCTION_STATUS.json deployment must have succeeded", errors)
        if not isinstance(deployment.get("workflow_run_id"), int):
            error("ops/PRODUCTION_STATUS.json workflow_run_id must be an integer", errors)
        verification = data.get("verification") or {}
        if verification.get("state") not in {"DEPLOYMENT_BUILD_SUCCESS", "LIVE_VERIFIED"}:
            error("ops/PRODUCTION_STATUS.json v2 verification state is invalid", errors)
        if "exact_route_content_verification" not in verification:
            error("ops/PRODUCTION_STATUS.json v2 route-verification boundary missing", errors)
        relationship = data.get("relationship_to_current_state") or {}
        if relationship.get("current_repository_truth_is_dynamic") is not True:
            error("ops/PRODUCTION_STATUS.json must preserve dynamic current-repository truth", errors)
        return

    # Legacy v1 compatibility for historical branches and rollback inspection.
    required = [
        "production_repository",
        "production_branch",
        "main_at_audit",
        "exact_live_sha",
        "last_live_verification",
        "branch_protection",
        "independent_backup",
    ]
    for key in required:
        if key not in data:
            error(f"ops/PRODUCTION_STATUS.json missing {key}", errors)
    exact_live = data.get("exact_live_sha")
    if exact_live not in {"UNKNOWN", None} and not SHA_RE.fullmatch(str(exact_live)):
        error("ops/PRODUCTION_STATUS.json exact_live_sha must be UNKNOWN or a 40-char SHA", errors)


def validate_current_state(data: dict, errors: list[str]) -> None:
    if data.get("schema") != CURRENT_SCHEMA_V2:
        return
    if data.get("record_type") != "CURRENT_STATE_CONTRACT_WITH_LAST_OBSERVATION":
        error("ops/CURRENT_STATE.json v2 has wrong record_type", errors)
    authority = data.get("authority") or {}
    for key in ("current_repository_truth", "current_deployment_truth", "historical_rollback_truth"):
        if not str(authority.get(key, "")).strip():
            error(f"ops/CURRENT_STATE.json v2 authority missing {key}", errors)
    observation = data.get("repository_observation") or {}
    if not SHA_RE.fullmatch(str(observation.get("sha", ""))):
        error("ops/CURRENT_STATE.json repository observation SHA invalid", errors)
    if not SHA_RE.fullmatch(str(observation.get("tree_sha", ""))):
        error("ops/CURRENT_STATE.json repository observation tree SHA invalid", errors)
    if observation.get("status") != "BASELINE_OBSERVED_BEFORE_OPERATIONAL_TRUTH_CHANGE":
        error("ops/CURRENT_STATE.json observation boundary is not explicit", errors)
    freshness = data.get("freshness_policy") or {}
    if freshness.get("runtime_generator") != "scripts/generate_operational_truth.py":
        error("ops/CURRENT_STATE.json runtime generator path mismatch", errors)
    if freshness.get("structural_validator") != "scripts/validate_operational_truth.py":
        error("ops/CURRENT_STATE.json structural validator path mismatch", errors)


def validate_rollback(data: dict, errors: list[str]) -> None:
    if data.get("schema") == ROLLBACK_SCHEMA_V2:
        if data.get("record_type") != "HISTORICAL_ROLLBACK_ANCHOR":
            error("ops/LAST_KNOWN_GOOD.json v2 must be an historical rollback anchor", errors)
        if data.get("is_current") is not False:
            error("ops/LAST_KNOWN_GOOD.json v2 must not claim to be current", errors)
        if data.get("rollback_eligible") is not True:
            error("ops/LAST_KNOWN_GOOD.json v2 must remain rollback-eligible", errors)
    if data.get("state") != "LIVE_VERIFIED":
        error("ops/LAST_KNOWN_GOOD.json must describe a LIVE_VERIFIED release", errors)
    if not SHA_RE.fullmatch(str(data.get("source_sha", ""))):
        error("ops/LAST_KNOWN_GOOD.json source_sha must be a 40-char SHA", errors)


def validate_release_ledger(data: dict, errors: list[str]) -> None:
    if data.get("schema") != LEDGER_SCHEMA_V1:
        error("ops/RELEASE_LEDGER.json schema is invalid", errors)
        return
    if data.get("record_type") != "APPEND_ONLY_RELEASE_LEDGER":
        error("ops/RELEASE_LEDGER.json must be append-only release ledger", errors)
    if data.get("append_only") is not True:
        error("ops/RELEASE_LEDGER.json append_only must be true", errors)
    releases = data.get("releases")
    if not isinstance(releases, list) or not releases:
        error("ops/RELEASE_LEDGER.json must contain release records", errors)
        return
    ids: set[str] = set()
    shas: set[str] = set()
    for release in releases:
        if not isinstance(release, dict):
            error("ops/RELEASE_LEDGER.json release must be an object", errors)
            continue
        release_id = release.get("release_id")
        source_sha = release.get("source_sha")
        if not isinstance(release_id, str) or not release_id.strip():
            error("ops/RELEASE_LEDGER.json release_id missing", errors)
        elif release_id in ids:
            error(f"ops/RELEASE_LEDGER.json duplicate release_id: {release_id}", errors)
        else:
            ids.add(release_id)
        if not SHA_RE.fullmatch(str(source_sha or "")):
            error(f"ops/RELEASE_LEDGER.json invalid source_sha for {release_id}", errors)
        elif source_sha in shas:
            error(f"ops/RELEASE_LEDGER.json duplicate source_sha: {source_sha}", errors)
        else:
            shas.add(source_sha)


def validate_operational_files(errors: list[str]) -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            error(f"required mission-critical control missing: {rel}", errors)

    current_path = ROOT / "ops" / "CURRENT_STATE.json"
    if current_path.is_file():
        current = load_json(current_path, errors)
        if current is not None:
            validate_current_state(current, errors)

    status_path = ROOT / "ops" / "PRODUCTION_STATUS.json"
    if status_path.is_file():
        status = load_json(status_path, errors)
        if status is not None:
            validate_production_status(status, errors)

    lkg_path = ROOT / "ops" / "LAST_KNOWN_GOOD.json"
    if lkg_path.is_file():
        rollback = load_json(lkg_path, errors)
        if rollback is not None:
            validate_rollback(rollback, errors)

    ledger_path = ROOT / "ops" / "RELEASE_LEDGER.json"
    if ledger_path.is_file():
        ledger = load_json(ledger_path, errors)
        if ledger is not None:
            validate_release_ledger(ledger, errors)

    critical = ROOT / "ops" / "CRITICAL_PATHS.txt"
    if critical.is_file():
        entries = [
            line.strip()
            for line in critical.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        if len(entries) < 8:
            error("ops/CRITICAL_PATHS.txt is unexpectedly small", errors)


def main() -> int:
    errors: list[str] = []
    validate_workflows(errors)
    validate_operational_files(errors)
    if errors:
        print("MISSION-CRITICAL REPOSITORY GATE: FAIL")
        for item in errors:
            print(f" - {item}")
        return 1
    workflow_count = len(list(WORKFLOWS.glob("*.yml")))
    print(f"MISSION-CRITICAL REPOSITORY GATE: PASS ({workflow_count} workflows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

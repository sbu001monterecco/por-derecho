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

REQUIRED_FILES = [
    "AGENTS.md",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    ".github/workflows/production-smoke-monitor.yml",
    ".github/workflows/repository-backup-bundle.yml",
    ".github/workflows/verify-mission-critical-hardening-live.yml",
    "scripts/validate_publication_integrity.py",
    "scripts/validate_repository_preservation.py",
    "scripts/production_smoke_check.py",
    "ops/GITHUB_MISSION_CRITICAL_RUNBOOK.md",
    "ops/CRITICAL_PATHS.txt",
    "ops/REPOSITORY_PRESERVATION_CONTRACT.json",
    "ops/FIVE_ACTOR_PRESERVATION_AND_READER_JOURNEY_BACKLOG.md",
    "ops/PRODUCTION_STATUS.json",
    "ops/LAST_KNOWN_GOOD.json",
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


def validate_operational_files(errors: list[str]) -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            error(f"required mission-critical control missing: {rel}", errors)

    status_path = ROOT / "ops" / "PRODUCTION_STATUS.json"
    if status_path.is_file():
        try:
            data = json.loads(status_path.read_text(encoding="utf-8"))
        except Exception as exc:
            error(f"ops/PRODUCTION_STATUS.json invalid JSON: {exc}", errors)
            return
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
        if exact_live not in {"UNKNOWN", None} and not re.fullmatch(r"[0-9a-f]{40}", str(exact_live)):
            error("ops/PRODUCTION_STATUS.json exact_live_sha must be UNKNOWN or a 40-char SHA", errors)

    lkg_path = ROOT / "ops" / "LAST_KNOWN_GOOD.json"
    if lkg_path.is_file():
        try:
            lkg = json.loads(lkg_path.read_text(encoding="utf-8"))
        except Exception as exc:
            error(f"ops/LAST_KNOWN_GOOD.json invalid JSON: {exc}", errors)
        else:
            if lkg.get("state") != "LIVE_VERIFIED":
                error("ops/LAST_KNOWN_GOOD.json must describe a LIVE_VERIFIED release", errors)
            if not re.fullmatch(r"[0-9a-fA-F]{40}", str(lkg.get("source_sha", ""))):
                error("ops/LAST_KNOWN_GOOD.json source_sha must be a 40-char SHA", errors)

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

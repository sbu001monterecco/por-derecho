#!/usr/bin/env python3
"""Validate Por Derecho evidence visibility, OCR, image and redaction continuity.

This validator deliberately permits truthful legacy backfill states. It rejects false
completeness, missing declared assets, unreasoned image gaps, unsafe redaction
metadata and continuity counts that do not match the package.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "evidence-visibility"
POLICY = ROOT / ".github/governance/EVIDENCE_VISIBILITY_IMAGE_OCR_REDACTION_AND_CONTINUITY_STANDARD_04SEP2026.md"
ROLE_OVERLAY = ROOT / ".github/governance/EVIDENCE_VISIBILITY_ROLE_CONTINUITY_OVERLAY_04SEP2026.json"
SCHEMA = ROOT / ".github/evidence-intelligence/schemas/evidence-visibility.schema.json"
PUBLIC_PAGES = [
    ROOT / "en/evidence-visibility/index.html",
    ROOT / "es/visibilidad-evidencia/index.html",
]
RUNTIME = ROOT / "assets/evidence-visibility-runtime-20260904.js"
SITE_LOADER = ROOT / "assets/site.js"
EVIDENCE_AGENTS = ROOT / "evidence/AGENTS.md"

SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")

ORIGINAL_STATES = {
    "PRESERVED_IN_REPOSITORY",
    "PRESERVED_EXTERNAL_CONNECTED_SOURCE",
    "SOURCE_PENDING",
    "NOT_APPLICABLE",
}
TEXT_STATES = {"PUBLISHED", "PARTIAL", "PENDING", "NOT_APPLICABLE"}
VISUAL_STATES = {"PUBLISHED", "PARTIAL", "SOURCE_PENDING", "BLOCKED_WITH_REASON", "NOT_APPLICABLE"}
REDACTION_STATES = {"NONE", "PUBLIC_REDACTED_DERIVATIVE", "REDACTION_REQUIRED", "NOT_ASSESSED"}
LIFECYCLE_STATES = {
    "SOURCE_PENDING",
    "SOURCE_PRESERVED",
    "TEXT_EXTRACTED",
    "IMAGE_RENDERED",
    "REDACTED_PUBLIC_DERIVATIVE",
    "LINKED",
    "LIVE_VERIFIED",
    "BLOCKED_WITH_REASON",
}
PUBLICATION_STATES = {"NOT_PUBLISHED", "REGISTERED", "PUBLISHED", "LIVE_VERIFIED", "BLOCKED_WITH_REASON"}
OWNER_ROLES = {"Worker", "Integrator", "Verifier", "Publication Coordinator", "Continuity / closeout role"}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.records = 0
        self.packages = 0

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")


def load_json(path: Path, report: Report) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        report.error(str(path.relative_to(ROOT)), f"invalid or unreadable JSON: {exc}")
        return None


def require_mapping(value: Any, where: str, report: Report) -> dict[str, Any]:
    if not isinstance(value, dict):
        report.error(where, "must be an object")
        return {}
    return value


def require_list(value: Any, where: str, report: Report) -> list[Any]:
    if not isinstance(value, list):
        report.error(where, "must be an array")
        return []
    return value


def require_nonempty_string(value: Any, where: str, report: Report) -> str:
    if not isinstance(value, str) or not value.strip():
        report.error(where, "must be a non-empty string")
        return ""
    return value


def repo_path_exists(raw: Any, where: str, report: Report) -> bool:
    path_text = require_nonempty_string(raw, where, report)
    if not path_text:
        return False
    if path_text.startswith(("http://", "https://", "/")) or ".." in Path(path_text).parts:
        report.error(where, "must be a safe repository-relative path")
        return False
    path = ROOT / path_text
    if not path.exists():
        report.error(where, f"declared repository asset does not exist: {path_text}")
        return False
    return True


def validate_asset(asset: Any, where: str, report: Report, require_hash: bool = False) -> None:
    item = require_mapping(asset, where, report)
    repo_path_exists(item.get("path"), f"{where}.path", report)
    require_nonempty_string(item.get("kind"), f"{where}.kind", report)
    require_nonempty_string(item.get("language"), f"{where}.language", report)
    digest = item.get("sha256")
    if require_hash and not isinstance(digest, str):
        report.error(f"{where}.sha256", "is required for published visual assets")
    if digest is not None and (not isinstance(digest, str) or not SHA256_RE.fullmatch(digest)):
        report.error(f"{where}.sha256", "must be a lowercase 64-character SHA-256")


def validate_gap(gap: Any, where: str, report: Report) -> str:
    item = require_mapping(gap, where, report)
    require_nonempty_string(item.get("gap_id"), f"{where}.gap_id", report)
    status = item.get("status")
    if status not in {"OPEN", "BLOCKED", "RESOLVED"}:
        report.error(f"{where}.status", "must be OPEN, BLOCKED or RESOLVED")
    require_nonempty_string(item.get("description"), f"{where}.description", report)
    require_nonempty_string(item.get("next_action"), f"{where}.next_action", report)
    owner = item.get("owner_role")
    if owner not in OWNER_ROLES:
        report.error(f"{where}.owner_role", f"must be one of {sorted(OWNER_ROLES)}")
    if status == "BLOCKED" and not item.get("blocking_reason"):
        report.error(f"{where}.blocking_reason", "is required for BLOCKED gaps")
    return status if isinstance(status, str) else ""


def validate_record(record: Any, package_path: Path, index: int, report: Report, seen_ids: set[str]) -> int:
    where = f"{package_path.relative_to(ROOT)}.records[{index}]"
    item = require_mapping(record, where, report)
    report.records += 1

    evidence_id = require_nonempty_string(item.get("evidence_id"), f"{where}.evidence_id", report)
    if evidence_id in seen_ids:
        report.error(f"{where}.evidence_id", f"duplicate evidence ID: {evidence_id}")
    seen_ids.add(evidence_id)

    require_nonempty_string(item.get("title"), f"{where}.title", report)
    require_nonempty_string(item.get("document_type"), f"{where}.document_type", report)
    require_list(item.get("languages"), f"{where}.languages", report)
    require_nonempty_string(item.get("source_type"), f"{where}.source_type", report)

    lifecycle = item.get("lifecycle_status")
    if lifecycle not in LIFECYCLE_STATES:
        report.error(f"{where}.lifecycle_status", f"must be one of {sorted(LIFECYCLE_STATES)}")

    provenance = require_mapping(item.get("provenance"), f"{where}.provenance", report)
    for field in ("custodian_class", "source_description", "verified_or_registered_date", "integrity_note"):
        require_nonempty_string(provenance.get(field), f"{where}.provenance.{field}", report)

    original = require_mapping(item.get("original_asset"), f"{where}.original_asset", report)
    original_status = original.get("status")
    if original_status not in ORIGINAL_STATES:
        report.error(f"{where}.original_asset.status", f"must be one of {sorted(ORIGINAL_STATES)}")
    digest = original.get("sha256")
    if digest is not None and (not isinstance(digest, str) or not SHA256_RE.fullmatch(digest)):
        report.error(f"{where}.original_asset.sha256", "must be null or a lowercase 64-character SHA-256")
    if original_status == "PRESERVED_IN_REPOSITORY":
        repo_path_exists(original.get("repository_path"), f"{where}.original_asset.repository_path", report)
        if not isinstance(digest, str):
            report.error(f"{where}.original_asset.sha256", "is required for a repository-preserved original")
    elif original.get("repository_path") is not None:
        report.error(f"{where}.original_asset.repository_path", "must be null unless the original is preserved in the repository")
    if original_status == "PRESERVED_EXTERNAL_CONNECTED_SOURCE" and not isinstance(digest, str):
        report.error(f"{where}.original_asset.sha256", "is required for a preserved connected source")

    text = require_mapping(item.get("searchable_text"), f"{where}.searchable_text", report)
    text_status = text.get("status")
    if text_status not in TEXT_STATES:
        report.error(f"{where}.searchable_text.status", f"must be one of {sorted(TEXT_STATES)}")
    text_assets = require_list(text.get("assets"), f"{where}.searchable_text.assets", report)
    if text_status in {"PUBLISHED", "PARTIAL"} and not text_assets:
        report.error(f"{where}.searchable_text.assets", f"must not be empty when status is {text_status}")
    for asset_index, asset in enumerate(text_assets):
        validate_asset(asset, f"{where}.searchable_text.assets[{asset_index}]", report)

    visual = require_mapping(item.get("visual_evidence"), f"{where}.visual_evidence", report)
    visual_status = visual.get("status")
    if visual_status not in VISUAL_STATES:
        report.error(f"{where}.visual_evidence.status", f"must be one of {sorted(VISUAL_STATES)}")
    images = require_list(visual.get("images"), f"{where}.visual_evidence.images", report)
    if visual_status in {"PUBLISHED", "PARTIAL"} and not images:
        report.error(f"{where}.visual_evidence.images", f"must not be empty when status is {visual_status}")
    if visual_status in {"SOURCE_PENDING", "BLOCKED_WITH_REASON"} and images:
        report.error(f"{where}.visual_evidence.images", f"must be empty while status is {visual_status}")
    for image_index, image in enumerate(images):
        validate_asset(image, f"{where}.visual_evidence.images[{image_index}]", report, require_hash=True)

    redaction = require_mapping(item.get("redaction"), f"{where}.redaction", report)
    redaction_status = redaction.get("status")
    if redaction_status not in REDACTION_STATES:
        report.error(f"{where}.redaction.status", f"must be one of {sorted(REDACTION_STATES)}")
    if redaction_status in {"PUBLIC_REDACTED_DERIVATIVE", "REDACTION_REQUIRED"} and not redaction.get("reason"):
        report.error(f"{where}.redaction.reason", f"is required when status is {redaction_status}")
    review = require_mapping(redaction.get("review"), f"{where}.redaction.review", report)
    if redaction_status == "PUBLIC_REDACTED_DERIVATIVE":
        if not redaction.get("public_version_of"):
            report.error(f"{where}.redaction.public_version_of", "is required for a public redacted derivative")
        if review.get("status") != "APPROVED" or not review.get("review_date"):
            report.error(f"{where}.redaction.review", "must be approved and dated for a public redacted derivative")

    relations = require_mapping(item.get("relations"), f"{where}.relations", report)
    for field in ("actors", "entities", "proceedings", "events", "parent_child"):
        require_list(relations.get(field), f"{where}.relations.{field}", report)
    for page_index, page in enumerate(require_list(relations.get("pages"), f"{where}.relations.pages", report)):
        repo_path_exists(page, f"{where}.relations.pages[{page_index}]", report)

    publication = require_mapping(item.get("publication"), f"{where}.publication", report)
    publication_status = publication.get("status")
    if publication_status not in PUBLICATION_STATES:
        report.error(f"{where}.publication.status", f"must be one of {sorted(PUBLICATION_STATES)}")
    for route_index, route in enumerate(require_list(publication.get("public_routes"), f"{where}.publication.public_routes", report)):
        repo_path_exists(route, f"{where}.publication.public_routes[{route_index}]", report)
    deployed_commit = publication.get("deployed_commit")
    if deployed_commit is not None and (not isinstance(deployed_commit, str) or not COMMIT_RE.fullmatch(deployed_commit)):
        report.error(f"{where}.publication.deployed_commit", "must be null or a 40-character commit SHA")

    gap_states = [
        validate_gap(gap_item, f"{where}.gaps[{gap_index}]", report)
        for gap_index, gap_item in enumerate(require_list(item.get("gaps"), f"{where}.gaps", report))
    ]
    open_gaps = sum(state in {"OPEN", "BLOCKED"} for state in gap_states)

    if visual_status in {"SOURCE_PENDING", "BLOCKED_WITH_REASON"} and open_gaps == 0:
        report.error(f"{where}.gaps", f"at least one open/blocked gap is required for visual status {visual_status}")
    if visual_status == "SOURCE_PENDING":
        report.warn(where, "source-derived evidence images remain pending")
    if text_status in {"PARTIAL", "PENDING"}:
        report.warn(where, f"searchable text state is {text_status}")

    if lifecycle == "LIVE_VERIFIED":
        if publication.get("status") != "LIVE_VERIFIED" or publication.get("live_verified") is not True:
            report.error(where, "LIVE_VERIFIED lifecycle requires matching publication status and live_verified=true")
        if visual_status not in {"PUBLISHED", "PARTIAL"}:
            report.error(where, "LIVE_VERIFIED lifecycle requires published visual evidence")
    if publication.get("live_verified") is True and not deployed_commit:
        report.error(f"{where}.publication.deployed_commit", "is required when live_verified=true")

    return open_gaps


def validate_package(path: Path, report: Report) -> None:
    payload = load_json(path, report)
    if payload is None:
        return
    item = require_mapping(payload, str(path.relative_to(ROOT)), report)
    report.packages += 1
    if item.get("schema_version") != "1.0.0":
        report.error(str(path.relative_to(ROOT)), "schema_version must be 1.0.0")
    require_nonempty_string(item.get("package_id"), f"{path.relative_to(ROOT)}.package_id", report)
    require_nonempty_string(item.get("title"), f"{path.relative_to(ROOT)}.title", report)
    require_nonempty_string(item.get("scope"), f"{path.relative_to(ROOT)}.scope", report)

    governance = require_mapping(item.get("governance"), f"{path.relative_to(ROOT)}.governance", report)
    if governance.get("control_id") != "PD-EVIS-20260904-01":
        report.error(f"{path.relative_to(ROOT)}.governance.control_id", "must be PD-EVIS-20260904-01")
    repo_path_exists(governance.get("policy_path"), f"{path.relative_to(ROOT)}.governance.policy_path", report)
    repo_path_exists(governance.get("schema_path"), f"{path.relative_to(ROOT)}.governance.schema_path", report)

    records = require_list(item.get("records"), f"{path.relative_to(ROOT)}.records", report)
    if not records:
        report.error(f"{path.relative_to(ROOT)}.records", "must contain at least one evidence record")
    seen_ids: set[str] = set()
    actual_open = sum(validate_record(record, path, idx, report, seen_ids) for idx, record in enumerate(records))

    continuity = require_mapping(item.get("role_continuity"), f"{path.relative_to(ROOT)}.role_continuity", report)
    declared_open = continuity.get("open_gap_count")
    if declared_open != actual_open:
        report.error(
            f"{path.relative_to(ROOT)}.role_continuity.open_gap_count",
            f"declares {declared_open!r}, but {actual_open} open/blocked gaps were found",
        )
    if continuity.get("handoff_status") == "CLOSED" and actual_open:
        report.error(f"{path.relative_to(ROOT)}.role_continuity.handoff_status", "cannot be CLOSED while open gaps remain")

    completeness = governance.get("visual_completeness_claim")
    has_incomplete_visual = any(
        isinstance(record, dict)
        and isinstance(record.get("visual_evidence"), dict)
        and record["visual_evidence"].get("status") in {"PARTIAL", "SOURCE_PENDING", "BLOCKED_WITH_REASON"}
        for record in records
    )
    if completeness == "COMPLETE" and has_incomplete_visual:
        report.error(f"{path.relative_to(ROOT)}.governance.visual_completeness_claim", "cannot be COMPLETE while visual records remain incomplete")


def validate_control_surface(report: Report) -> None:
    for required in [POLICY, ROLE_OVERLAY, SCHEMA, RUNTIME, SITE_LOADER, EVIDENCE_AGENTS, *PUBLIC_PAGES]:
        if not required.exists():
            report.error("control-surface", f"required file missing: {required.relative_to(ROOT)}")
    load_json(ROLE_OVERLAY, report)
    load_json(SCHEMA, report)

    if SITE_LOADER.exists():
        loader = SITE_LOADER.read_text(encoding="utf-8")
        if "evidence-visibility-runtime-20260904.js" not in loader:
            report.error("assets/site.js", "does not load the evidence-visibility runtime")
    if RUNTIME.exists():
        runtime = RUNTIME.read_text(encoding="utf-8")
        required_phrases = [
            "No synthetic substitute",
            "data/evidence-visibility/uria-ricpe-sun-park-20260904.json",
            "visual_evidence",
            "searchable_text",
        ]
        for phrase in required_phrases:
            if phrase not in runtime:
                report.error("assets/evidence-visibility-runtime-20260904.js", f"missing continuity marker: {phrase}")


def main() -> int:
    report = Report()
    validate_control_surface(report)

    if not DATA_DIR.exists():
        report.error("data/evidence-visibility", "registry directory is missing")
    else:
        packages = sorted(DATA_DIR.glob("*.json"))
        if not packages:
            report.error("data/evidence-visibility", "no evidence-visibility packages are registered")
        for package in packages:
            validate_package(package, report)

    if report.warnings:
        print(f"EVIDENCE VISIBILITY: {len(report.warnings)} truthful backfill warning(s)")
        for warning in report.warnings:
            print(f"WARNING: {warning}")

    if report.errors:
        print("EVIDENCE VISIBILITY / OCR / IMAGE / REDACTION CONTINUITY GATE: FAIL")
        for error in report.errors:
            print(f" - {error}")
        return 1

    print(
        "EVIDENCE VISIBILITY / OCR / IMAGE / REDACTION CONTINUITY GATE: PASS "
        f"({report.packages} package(s); {report.records} record(s); "
        f"{len(report.warnings)} explicit pending/partial state warning(s))"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

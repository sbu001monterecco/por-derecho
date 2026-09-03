#!/usr/bin/env python3
"""Schema-aware publication/deletion-safety guard.

This wrapper preserves the legacy publication-manifest validator while adding strict
validation for immutable reintegration-transition snapshots. A transition snapshot is
historical evidence of a reviewed candidate tree; it is not rewritten after merge and
must not be misclassified as a legacy LIVE/DELETION_SAFE publication manifest.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import validate_publication_integrity as legacy

ROOT = Path(__file__).resolve().parents[1]
TRANSITION_SCHEMA = "por-derecho.reintegration-transition.v1"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def safe_repo_path(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    candidate = Path(value)
    return not candidate.is_absolute() and ".." not in candidate.parts


def validate_optional_sha256(value: object, label: str, rel: Path, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, str) or not HEX64.fullmatch(value):
        fail(f"{rel}: {label} must be null or a 64-character lowercase SHA-256", errors)


def validate_reintegration_transition(path: Path, data: dict, errors: list[str]) -> None:
    """Validate an immutable candidate-transition snapshot without current-tree drift tests."""
    rel = path.relative_to(ROOT)
    required = [
        "schema",
        "publication_id",
        "control_date",
        "state",
        "purpose",
        "integration_branch",
        "base_main_sha",
        "current_denominator",
        "finite_test_family_counts",
        "candidate_delta_file_count",
        "transitions",
        "source_boundaries",
        "production",
    ]
    for key in required:
        if key not in data:
            fail(f"{rel}: transition snapshot missing required field {key!r}", errors)

    if data.get("schema") != TRANSITION_SCHEMA:
        fail(f"{rel}: unexpected transition schema {data.get('schema')!r}", errors)
    if data.get("state") != "RELEASE_CANDIDATE_VALIDATION":
        fail(f"{rel}: immutable transition snapshot must retain RELEASE_CANDIDATE_VALIDATION state", errors)
    if not isinstance(data.get("publication_id"), str) or not data.get("publication_id", "").strip():
        fail(f"{rel}: transition snapshot requires a non-empty publication_id", errors)
    if not isinstance(data.get("control_date"), str) or not data.get("control_date", "").strip():
        fail(f"{rel}: transition snapshot requires a non-empty control_date", errors)
    if not isinstance(data.get("purpose"), str) or not data.get("purpose", "").strip():
        fail(f"{rel}: transition snapshot requires a non-empty purpose", errors)
    if not isinstance(data.get("integration_branch"), str) or not data.get("integration_branch", "").strip():
        fail(f"{rel}: transition snapshot requires a non-empty integration_branch", errors)

    base_sha = data.get("base_main_sha")
    if not isinstance(base_sha, str) or not HEX40.fullmatch(base_sha):
        fail(f"{rel}: base_main_sha must be a 40-character lowercase Git SHA", errors)

    denominator = data.get("current_denominator")
    families = data.get("finite_test_family_counts")
    if not isinstance(denominator, dict) or not denominator:
        fail(f"{rel}: current_denominator must be a non-empty object", errors)
    if not isinstance(families, dict) or not families:
        fail(f"{rel}: finite_test_family_counts must be a non-empty object", errors)
    elif any(not isinstance(value, int) or value < 0 for value in families.values()):
        fail(f"{rel}: finite_test_family_counts values must be non-negative integers", errors)
    elif isinstance(denominator, dict) and denominator.get("FINITE_TEST_TOTAL") != sum(families.values()):
        fail(
            f"{rel}: current_denominator.FINITE_TEST_TOTAL does not equal finite_test_family_counts total",
            errors,
        )

    transitions = data.get("transitions")
    count = data.get("candidate_delta_file_count")
    if not isinstance(transitions, list):
        fail(f"{rel}: transitions must be an array", errors)
        transitions = []
    if not isinstance(count, int) or count < 0:
        fail(f"{rel}: candidate_delta_file_count must be a non-negative integer", errors)
    elif count != len(transitions):
        fail(f"{rel}: candidate_delta_file_count={count} but transitions has {len(transitions)} rows", errors)

    seen: set[str] = set()
    for index, row in enumerate(transitions):
        label = f"transitions[{index}]"
        if not isinstance(row, dict):
            fail(f"{rel}: {label} must be an object", errors)
            continue
        resource = row.get("resource")
        if not safe_repo_path(resource):
            fail(f"{rel}: {label}.resource is not a safe repository-relative path: {resource!r}", errors)
        elif resource in seen:
            fail(f"{rel}: duplicate transition resource {resource!r}", errors)
        else:
            seen.add(resource)
        if not isinstance(row.get("git_status"), str) or not row.get("git_status", "").strip():
            fail(f"{rel}: {label}.git_status must be a non-empty string", errors)
        validate_optional_sha256(row.get("preintegration_main_sha256"), f"{label}.preintegration_main_sha256", rel, errors)
        validate_optional_sha256(row.get("candidate_sha256"), f"{label}.candidate_sha256", rel, errors)
        anchors = row.get("historical_anchors")
        if not isinstance(anchors, list):
            fail(f"{rel}: {label}.historical_anchors must be an array", errors)
            continue
        for anchor_index, anchor in enumerate(anchors):
            anchor_label = f"{label}.historical_anchors[{anchor_index}]"
            if not isinstance(anchor, dict):
                fail(f"{rel}: {anchor_label} must be an object", errors)
                continue
            manifest = anchor.get("manifest")
            if not safe_repo_path(manifest):
                fail(f"{rel}: {anchor_label}.manifest is unsafe: {manifest!r}", errors)
            elif not (ROOT / manifest).is_file():
                fail(f"{rel}: {anchor_label}.manifest does not exist: {manifest}", errors)
            if not isinstance(anchor.get("publication_id"), str) or not anchor.get("publication_id", "").strip():
                fail(f"{rel}: {anchor_label}.publication_id must be non-empty", errors)
            if not isinstance(anchor.get("sha256"), str) or not HEX64.fullmatch(anchor.get("sha256", "")):
                fail(f"{rel}: {anchor_label}.sha256 must be a 64-character lowercase SHA-256", errors)
            if not isinstance(anchor.get("kind"), str) or not anchor.get("kind", "").strip():
                fail(f"{rel}: {anchor_label}.kind must be non-empty", errors)

    predecessors = data.get("historical_predecessors", [])
    if not isinstance(predecessors, list):
        fail(f"{rel}: historical_predecessors must be an array when present", errors)
    else:
        for index, predecessor in enumerate(predecessors):
            label = f"historical_predecessors[{index}]"
            if not isinstance(predecessor, dict):
                fail(f"{rel}: {label} must be an object", errors)
                continue
            manifest = predecessor.get("manifest")
            if not safe_repo_path(manifest):
                fail(f"{rel}: {label}.manifest is unsafe: {manifest!r}", errors)
            elif not (ROOT / manifest).is_file():
                fail(f"{rel}: {label}.manifest does not exist: {manifest}", errors)
            merge_sha = predecessor.get("merge_sha")
            if not isinstance(merge_sha, str) or not HEX40.fullmatch(merge_sha):
                fail(f"{rel}: {label}.merge_sha must be a 40-character lowercase Git SHA", errors)

    boundaries = data.get("source_boundaries")
    if not isinstance(boundaries, list) or not boundaries or any(not isinstance(v, str) or not v.strip() for v in boundaries):
        fail(f"{rel}: source_boundaries must be a non-empty array of strings", errors)

    obsolete = data.get("obsolete_duplicate_routes_absent", [])
    if not isinstance(obsolete, list) or any(not safe_repo_path(v) for v in obsolete):
        fail(f"{rel}: obsolete_duplicate_routes_absent must contain safe repository-relative paths", errors)

    production = data.get("production")
    if not isinstance(production, dict):
        fail(f"{rel}: production must be an object", errors)
    else:
        # These fields deliberately remain false/null forever: this file is a candidate-byte
        # snapshot, not a post-merge attestation. Production proof lives in the successor
        # continuity handoff and exact-SHA deployment/browser evidence.
        expected_snapshot = {
            "merged_to_main": False,
            "merge_sha": None,
            "pages_run_id": None,
            "live_browser_verified": False,
        }
        for key, expected in expected_snapshot.items():
            if production.get(key) is not expected and production.get(key) != expected:
                fail(f"{rel}: immutable transition production.{key} must remain {expected!r}", errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="also run legacy live URL checks for deployable legacy manifests")
    args = parser.parse_args()

    errors: list[str] = []
    manifests = legacy.load_manifests(errors)
    files = legacy.changed_files()
    legacy.validate_changed_files(files, manifests, errors)

    transition_count = 0
    legacy_count = 0
    for path, data in manifests:
        if data.get("schema") == TRANSITION_SCHEMA:
            transition_count += 1
            validate_reintegration_transition(path, data, errors)
        else:
            legacy_count += 1
            legacy.validate_manifest(path, data, errors)

    if args.live:
        legacy.live_check(manifests, errors)

    if errors:
        print("PUBLICATION INTEGRITY GATE V2: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1

    print(
        "PUBLICATION INTEGRITY GATE V2: PASS "
        f"({legacy_count} legacy manifests; {transition_count} transition snapshots; {len(files)} changed files inspected)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

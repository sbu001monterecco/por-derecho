#!/usr/bin/env python3
"""Schema-aware publication/deletion-safety guard.

The publication-manifests directory is a governed namespace. Every new or changed
record must declare a supported document schema. Existing canonical legacy
publication-state manifests remain readable until they are next changed, while
reintegration transition snapshots retain their separate immutable contract.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import validate_publication_integrity as legacy

ROOT = Path(__file__).resolve().parents[1]
TRANSITION_SCHEMA = "por-derecho.reintegration-transition.v1"
PUBLICATION_SCHEMA = "por-derecho.publication-state.v1"
PUBLICATION_SCHEMA_VERSION = "1.0.0"
PUBLICATION_CONTRACT = ROOT / "schemas" / "publication-state-manifest-v1.schema.json"
LEGACY_REQUIRED_FIELDS = frozenset({"publication_id", "current_state", "expected_routes", "owner"})
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


def validate_publication_contract(errors: list[str]) -> None:
    """Prove that the checked-in machine contract matches this validator."""
    rel = PUBLICATION_CONTRACT.relative_to(ROOT)
    try:
        contract = json.loads(PUBLICATION_CONTRACT.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{rel}: missing or invalid publication-state contract: {exc}", errors)
        return

    required = set(contract.get("required") or [])
    missing = sorted((LEGACY_REQUIRED_FIELDS | {"schema", "schema_version"}) - required)
    if missing:
        fail(f"{rel}: contract required list is missing {missing}", errors)

    properties = contract.get("properties") or {}
    if (properties.get("schema") or {}).get("const") != PUBLICATION_SCHEMA:
        fail(f"{rel}: schema const does not match {PUBLICATION_SCHEMA!r}", errors)
    if (properties.get("schema_version") or {}).get("const") != PUBLICATION_SCHEMA_VERSION:
        fail(f"{rel}: schema_version const does not match {PUBLICATION_SCHEMA_VERSION!r}", errors)

    state_enum = set((properties.get("current_state") or {}).get("enum") or [])
    if state_enum != legacy.VALID_STATES:
        fail(
            f"{rel}: current_state enum differs from the legacy validator "
            f"(contract={sorted(state_enum)}, validator={sorted(legacy.VALID_STATES)})",
            errors,
        )


def classify_document(data: dict, *, changed: bool) -> tuple[str | None, str | None]:
    """Return document kind and a precise contract error, if any.

    Unchanged canonical legacy manifests are grandfathered. As soon as a legacy
    manifest is changed, it must declare the publication-state schema. This gives
    backward compatibility without allowing new schema ambiguity.
    """
    schema = data.get("schema")
    complete_legacy = LEGACY_REQUIRED_FIELDS.issubset(data)

    if schema == TRANSITION_SCHEMA:
        return "transition", None
    if schema == PUBLICATION_SCHEMA:
        if data.get("schema_version") != PUBLICATION_SCHEMA_VERSION:
            return None, (
                f"publication-state schema requires schema_version "
                f"{PUBLICATION_SCHEMA_VERSION!r}"
            )
        return "publication", None

    if schema is None:
        if complete_legacy and not changed:
            return "legacy", None
        if complete_legacy:
            return None, (
                f"changed/new legacy manifest must declare schema "
                f"{PUBLICATION_SCHEMA!r} and schema_version "
                f"{PUBLICATION_SCHEMA_VERSION!r}"
            )
        return None, (
            "record has no supported schema and is not a complete canonical "
            "legacy publication-state manifest; add a supported schema or move "
            "the record to its governed document namespace"
        )

    if complete_legacy and not changed:
        # Existing explicit-schema legacy records are tolerated until changed.
        return "legacy", None
    return None, f"unsupported manifest schema {schema!r}"


def run_classifier_self_tests(errors: list[str]) -> None:
    canonical = {
        "publication_id": "PD-TEST",
        "current_state": "REMOTE_SOURCE",
        "expected_routes": {"es": [], "en": []},
        "owner": "test",
    }
    cases = [
        (
            "explicit publication",
            {**canonical, "schema": PUBLICATION_SCHEMA, "schema_version": PUBLICATION_SCHEMA_VERSION},
            True,
            "publication",
            None,
        ),
        (
            "explicit transition",
            {"schema": TRANSITION_SCHEMA},
            True,
            "transition",
            None,
        ),
        ("unchanged canonical legacy", canonical, False, "legacy", None),
        ("changed canonical legacy", canonical, True, None, "must declare schema"),
        (
            "changed unknown schema",
            {**canonical, "schema": "por-derecho.unknown.v1"},
            True,
            None,
            "unsupported manifest schema",
        ),
        (
            "schema-less heterogeneous record",
            {"release_id": "PD-TEST"},
            False,
            None,
            "no supported schema",
        ),
    ]
    for label, data, changed, expected_kind, expected_error in cases:
        kind, error = classify_document(data, changed=changed)
        if kind != expected_kind:
            fail(f"classifier self-test {label!r}: expected kind {expected_kind!r}, got {kind!r}", errors)
        if expected_error is None:
            if error is not None:
                fail(f"classifier self-test {label!r}: unexpected error {error!r}", errors)
        elif error is None or expected_error not in error:
            fail(
                f"classifier self-test {label!r}: expected error containing "
                f"{expected_error!r}, got {error!r}",
                errors,
            )


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
    parser.add_argument("--live", action="store_true", help="also run legacy live URL checks for deployable publication manifests")
    args = parser.parse_args()

    errors: list[str] = []
    validate_publication_contract(errors)
    run_classifier_self_tests(errors)

    manifests = legacy.load_manifests(errors)
    files = legacy.changed_files()
    changed = set(files)
    legacy.validate_changed_files(files, manifests, errors)

    transition_count = 0
    publication_count = 0
    grandfathered_count = 0
    deployable_manifests: list[tuple[Path, dict]] = []

    for path, data in manifests:
        rel = path.relative_to(ROOT).as_posix()
        if not isinstance(data, dict):
            fail(f"{rel}: manifest root must be a JSON object", errors)
            continue
        kind, contract_error = classify_document(data, changed=rel in changed)
        if contract_error:
            fail(f"{rel}: {contract_error}", errors)
            continue
        if kind == "transition":
            transition_count += 1
            validate_reintegration_transition(path, data, errors)
            continue

        if kind == "publication":
            publication_count += 1
        else:
            grandfathered_count += 1
        legacy.validate_manifest(path, data, errors)
        deployable_manifests.append((path, data))

    if args.live:
        legacy.live_check(deployable_manifests, errors)

    if errors:
        print("PUBLICATION INTEGRITY GATE V2: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1

    print(
        "PUBLICATION INTEGRITY GATE V2: PASS "
        f"({publication_count} explicit publication manifests; "
        f"{grandfathered_count} grandfathered legacy manifests; "
        f"{transition_count} transition snapshots; {len(files)} changed files inspected)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

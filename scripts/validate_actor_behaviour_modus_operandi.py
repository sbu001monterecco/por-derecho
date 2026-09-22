#!/usr/bin/env python3
"""Fail-closed structural validator for the actor behaviour / modus-operandi registry."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assets/data/actor-behaviour-modus-operandi-registry-v1.json"

EXPECTED = {
    "FMMM": ("PD-SP-P-0009", 8),
    "JDAM": ("PD-SP-P-0011", 10),
    "LPAM": ("PD-SP-P-0012", 8),
}
MACHINE_ID = re.compile(r"^MO-(FMMM|JDAM|LPAM)-(\d{2})$")


def validate(data: dict) -> list[str]:
    errors: list[str] = []

    if data.get("schema") != "por-derecho.actor-behaviour-modus-operandi.v1":
        errors.append("unexpected schema")
    if data.get("status") != "ANALYTICAL_PATTERN_CONTROL_NOT_FINDING":
        errors.append("status must remain ANALYTICAL_PATTERN_CONTROL_NOT_FINDING")

    recurrence = data.get("recurrence") or {}
    if recurrence.get("tag") != "MO-CONSISTENT":
        errors.append("recurrence tag must be MO-CONSISTENT")
    if recurrence.get("minimum_shared_operational_markers") != 3:
        errors.append("recurrence threshold must remain exactly three shared operational markers")

    required_true = (
        "requires_independent_actor_attribution",
        "requires_primary_or_contemporaneous_source",
        "requires_method_similarity_not_merely_common_dispute_or_outcome",
        "requires_contrary_evidence_and_legitimate_alternatives",
        "separates_proposal_preparation_implementation_result",
        "requires_explicit_not_a_finding_label",
    )
    for key in required_true:
        if recurrence.get(key) is not True:
            errors.append(f"recurrence safeguard {key} must be true")

    actors = data.get("actors") or {}
    seen_machine_ids: set[str] = set()

    for actor_key, (person_id, marker_count) in EXPECTED.items():
        actor = actors.get(actor_key)
        if not isinstance(actor, dict):
            errors.append(f"missing actor {actor_key}")
            continue
        if actor.get("person_id") != person_id:
            errors.append(f"{actor_key}: canonical person_id must be {person_id}")

        source_controls = actor.get("source_controls") or []
        if not source_controls:
            errors.append(f"{actor_key}: at least one source control is required")
        for path in source_controls:
            if not isinstance(path, str) or not path.strip():
                errors.append(f"{actor_key}: invalid source-control path")
                continue
            normalized = path.replace("\\", "/").lstrip("./")
            if normalized.startswith("private/"):
                errors.append(f"{actor_key}: private path must not be embedded in public registry: {path}")

        markers = actor.get("markers") or []
        if len(markers) != marker_count:
            errors.append(f"{actor_key}: expected {marker_count} markers, found {len(markers)}")

        for index, marker in enumerate(markers, start=1):
            machine_id = marker.get("machine_id")
            source_marker = marker.get("source_marker")
            expected_machine_id = f"MO-{actor_key}-{index:02d}"
            expected_source_marker = f"{actor_key}-{index:02d}"
            if machine_id != expected_machine_id:
                errors.append(f"{actor_key}: marker {index} machine_id must be {expected_machine_id}")
            if source_marker != expected_source_marker:
                errors.append(f"{actor_key}: marker {index} source_marker must be {expected_source_marker}")
            if machine_id in seen_machine_ids:
                errors.append(f"duplicate machine_id: {machine_id}")
            seen_machine_ids.add(machine_id)
            if not isinstance(machine_id, str) or MACHINE_ID.fullmatch(machine_id) is None:
                errors.append(f"invalid machine_id namespace: {machine_id}")
            if not marker.get("label") or not marker.get("description"):
                errors.append(f"{actor_key}: marker {index} requires label and description")

    if set(actors) != set(EXPECTED):
        errors.append(f"actor set must be exactly {sorted(EXPECTED)}")

    template = data.get("preferred_conclusion_template", "")
    for phrase in ("does not prove common intent", "actor-specific evidential bridges"):
        if phrase not in template:
            errors.append(f"preferred conclusion must retain safeguard phrase: {phrase}")

    return errors


def main() -> int:
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: cannot load {REGISTRY}: {exc}", file=sys.stderr)
        return 2

    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    total = sum(len(actor["markers"]) for actor in data["actors"].values())
    print(f"actor-behaviour registry OK: {len(data['actors'])} actors, {total} namespaced markers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
import json
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError, ValidationError
except ImportError as exc:
    raise SystemExit(
        "Evidence Control Plane validation requires jsonschema==4.25.1; "
        "install the pinned dependency before running this validator."
    ) from exc

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_AXES = {
    "ACCESS_STATUS","SOURCE_STATUS","EVIDENCE_STATUS","ASSERTION_STATUS","IDENTITY_STATUS",
    "REVIEW_STATUS","LEGAL_STATUS","PUBLICATION_STATUS","FILING_STATUS","PRESERVATION_STATUS","HOST_PARITY_STATUS"
}
REQUIRED_GAPS = {
    "PARITY_GAP","INTEGRITY_GAP","PROVENANCE_GAP","IDENTITY_GAP",
    "PROJECTION_GAP","STATUS_GAP","PRESERVATION_GAP"
}
REQUIRED_OBJECTS = {
    "SOURCE","EVIDENCE_OBJECT","DERIVATIVE","ACTOR","ENTITY","EVENT","ASSERTION","RELATIONSHIP",
    "CONTRADICTION","HYPOTHESIS","PROCEEDING","INVESTIGATIVE_ACTION","PRESERVATION_EVENT","PUBLICATION","WORKSPACE"
}

def load(path: Path):
    if not path.exists():
        raise ValueError(f"missing required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def require_exact_set(label: str, current, expected) -> None:
    current_set = set(current)
    expected_set = set(expected)
    if current_set != expected_set:
        raise ValueError(
            f"{label} drift: missing={sorted(expected_set - current_set)} "
            f"extra={sorted(current_set - expected_set)}"
        )

def validate_contract(root: Path = ROOT):
    base = root / "ops" / "evidence-control-plane"
    status_path = base / "STATUS_AXES.json"
    boot_path = base / "CONTROL_PLANE_BOOTSTRAP.json"
    census_path = base / "WORKSPACE_CENSUS_20260922.json"
    schema_path = root / "schemas" / "por-derecho-evidence-control-plane-v1.schema.json"
    archive_path = base / "ARCHIVE_INTAKE_CONTRACT.md"
    example_path = base / "EXAMPLE_ASSERTION.json"

    status = load(status_path)
    boot = load(boot_path)
    census = load(census_path)
    schema = load(schema_path)
    example = load(example_path)

    if not archive_path.exists():
        raise ValueError(f"missing archive intake contract: {archive_path}")

    axes = set(status.get("axes", {}))
    missing_axes = REQUIRED_AXES - axes
    extra_axes = axes - REQUIRED_AXES
    if missing_axes or extra_axes:
        raise ValueError(
            f"status-axis taxonomy drift: missing={sorted(missing_axes)} extra={sorted(extra_axes)}"
        )

    require_exact_set("gap taxonomy", boot.get("gap_types", []), REQUIRED_GAPS)
    require_exact_set("object taxonomy", boot.get("object_types", []), REQUIRED_OBJECTS)

    boundary = boot.get("authority_boundary", {})
    if boundary.get("canonical_host_migration") is not False:
        raise ValueError("authority boundary violation: canonical_host_migration must remain false")
    if boundary.get("external_action_authority") is not False:
        raise ValueError("authority boundary violation: external_action_authority must remain false")
    if boundary.get("public_content_change") is not False:
        raise ValueError("authority boundary violation: public_content_change must remain false")

    work = boot.get("initial_work_items", [])
    ids = [x.get("id") for x in work]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError(f"work-item IDs missing or duplicated: {ids}")
    for item in work:
        if not item.get("boundary"):
            raise ValueError(f"work item lacks evidential boundary: {item.get('id')}")

    active = census.get("active_lane", {})
    if active.get("public_content_change") is not False or active.get("external_contact") is not False:
        raise ValueError("workspace census exceeds bootstrap authority")

    obj_enum = set(schema["properties"]["object_type"]["enum"])
    require_exact_set("JSON Schema object taxonomy", obj_enum, REQUIRED_OBJECTS)

    assertion_rule = [
        item for item in schema.get("allOf", [])
        if item.get("if", {}).get("properties", {}).get("object_type", {}).get("const") == "ASSERTION"
    ]
    if not assertion_rule:
        raise ValueError("assertion-specific source/contrary-evidence rule absent")

    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise ValueError(f"JSON Schema is structurally invalid: {exc.message}") from exc

    schema_validator = Draft202012Validator(schema)
    try:
        schema_validator.validate(example)
    except ValidationError as exc:
        raise ValueError(
            f"example assertion violates schema at {list(exc.absolute_path)}: {exc.message}"
        ) from exc

    for axis, value in example.get("status_axes", {}).items():
        if axis not in status["axes"]:
            raise ValueError(f"example assertion uses unknown status axis: {axis}")
        if value not in status["axes"][axis]:
            raise ValueError(
                f"example assertion uses invalid {axis} value: observed={value!r} "
                f"expected_one_of={status['axes'][axis]}"
            )

    archive_text = archive_path.read_text(encoding="utf-8")
    for phrase in (
        "Preserve it unchanged before extraction",
        "extraction alone does not authenticate contents",
        "PRESERVATION_GAP",
    ):
        if phrase not in archive_text:
            raise ValueError(f"archive contract missing rule: {phrase}")

    return {
        "axes": len(axes),
        "objects": len(REQUIRED_OBJECTS),
        "gaps": len(REQUIRED_GAPS),
        "work_items": len(work),
        "schema_draft": "2020-12",
        "example_records_validated": 1,
    }

def main():
    try:
        stats = validate_contract(ROOT)
    except ValueError as exc:
        raise SystemExit(f"Evidence Control Plane bootstrap: FAIL — {exc}") from exc
    print("Evidence Control Plane bootstrap: PASS")
    print(" ".join(f"{key}={value}" for key, value in stats.items()))

if __name__ == "__main__":
    main()

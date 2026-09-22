#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "ops" / "evidence-control-plane"
STATUS = BASE / "STATUS_AXES.json"
BOOT = BASE / "CONTROL_PLANE_BOOTSTRAP.json"
CENSUS = BASE / "WORKSPACE_CENSUS_20260922.json"
SCHEMA = ROOT / "schemas" / "por-derecho-evidence-control-plane-v1.schema.json"
ARCHIVE = BASE / "ARCHIVE_INTAKE_CONTRACT.md"

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

def load(path):
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    status = load(STATUS)
    boot = load(BOOT)
    census = load(CENSUS)
    schema = load(SCHEMA)
    if not ARCHIVE.exists():
        raise SystemExit("missing archive intake contract")

    axes = set(status.get("axes", {}))
    missing_axes = REQUIRED_AXES - axes
    if missing_axes:
        raise SystemExit(f"missing status axes: {sorted(missing_axes)}")

    if set(boot.get("gap_types", [])) != REQUIRED_GAPS:
        raise SystemExit("gap taxonomy drift")

    if set(boot.get("object_types", [])) != REQUIRED_OBJECTS:
        raise SystemExit("object taxonomy drift")

    boundary = boot.get("authority_boundary", {})
    if boundary.get("canonical_host_migration") is not False:
        raise SystemExit("bootstrap must not migrate canonical host authority")
    if boundary.get("external_action_authority") is not False:
        raise SystemExit("bootstrap must not authorise external action")
    if boundary.get("public_content_change") is not False:
        raise SystemExit("bootstrap must remain non-public-content")

    work = boot.get("initial_work_items", [])
    ids = [x.get("id") for x in work]
    if len(ids) != len(set(ids)) or not ids:
        raise SystemExit("work-item IDs missing or duplicated")
    for item in work:
        if not item.get("boundary"):
            raise SystemExit(f"work item lacks evidential boundary: {item.get('id')}")

    active = census.get("active_lane", {})
    if active.get("public_content_change") is not False or active.get("external_contact") is not False:
        raise SystemExit("workspace census exceeds bootstrap authority")

    obj_enum = set(schema["properties"]["object_type"]["enum"])
    if obj_enum != REQUIRED_OBJECTS:
        raise SystemExit("JSON schema object taxonomy differs from bootstrap")

    assertion_rule = [x for x in schema.get("allOf", []) if x.get("if",{}).get("properties",{}).get("object_type",{}).get("const") == "ASSERTION"]
    if not assertion_rule:
        raise SystemExit("assertion-specific source/contrary-evidence rule absent")

    text = ARCHIVE.read_text(encoding="utf-8")
    for phrase in ("Preserve it unchanged before extraction", "extraction alone does not authenticate contents", "PRESERVATION_GAP"):
        if phrase not in text:
            raise SystemExit(f"archive contract missing rule: {phrase}")

    print("Evidence Control Plane bootstrap: PASS")
    print(f"axes={len(axes)} objects={len(REQUIRED_OBJECTS)} gaps={len(REQUIRED_GAPS)} work_items={len(work)}")

if __name__ == "__main__":
    main()

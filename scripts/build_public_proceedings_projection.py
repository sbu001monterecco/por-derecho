#!/usr/bin/env python3
"""Build the deterministic, allowlisted public Proceedings Master projection.

The canonical CSV is an operational source and is intentionally not modified by
this builder.  Browser code must consume the generated JSON projection instead
of downloading the canonical source and filtering it client-side.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
TARGET = ROOT / "assets/data/proceedings-master-public-v1.json"

FIELD_ALLOWLIST = (
    "Master_ID",
    "Legacy_ID",
    "Record_Type",
    "Is_Proceeding",
    "Proceeding_Class",
    "Stream",
    "Geography",
    "Origin_Organ",
    "Current_Custodian",
    "Reference",
    "Secondary_Reference",
    "NIG",
    "Date_or_Period",
    "Connection",
    "Object_or_Purpose",
    "Status",
    "Latest_Known_Event",
    "Appeal_or_Review",
    "Parent_Master_ID",
    "Linked_Proceedings",
    "Source_Status",
    "Open_Reference_Gap",
)

# Exact-value admission is deliberate.  A new classification must be reviewed
# before it can reach the public derivative; it is never silently published or
# silently omitted.
PUBLIC_TREATMENTS = (
    "INTERNAL_KNOWLEDGE_REGISTER_NOT_AUTO_PUBLISHED",
    "PUBLIC_CONTROLLED",
    "PUBLIC_CONTROLLED_PRIMARY_SOURCE_DERIVATIVE_OUTCOME_OPEN",
    "PUBLIC_FULLTEXT_REDACTED_WITH_KEY_PDFS",
    "PUBLIC_FULLTEXT_REDACTED_WITH_PROCEDURAL_LIMITS",
    "PUBLIC_ON_DEDICATED_RELEVANT_PAGE",
    "PUBLIC_SUMMARY_COMPLETE_REDACTED_FILE_OPEN",
    "PUBLIC_SUMMARY_DO_NOT_PUBLISH_RAW_PERSONAL_DATA",
    "PUBLIC_SUMMARY_WITH_IDENTITY_GAP",
    "PUBLIC_SUMMARY_WITH_PROCEDURAL_LIMITS",
)

EXCLUDED_TREATMENTS = (
    "INTERNAL_ONLY_NOT_SITE_AGGREGATED",
)

PRIVATE_SOURCE_FIELDS = (
    "Primary_Source_Anchor",
    "Repo_Canonical_Source",
    "Notes",
)

FORBIDDEN_PUBLIC_VALUE_PATTERNS = {
    "email address": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "private provider URL": re.compile(
        r"(?i)https?://(?:mail\.google\.com|drive\.google\.com|docs\.google\.com|chatgpt\.com)/"
    ),
    "provider message locator": re.compile(
        r"(?i)\b(?:message|thread|gmail)[ _-]?(?:id|locator)\b"
    ),
    "native mailbox filename": re.compile(r"(?i)\b[^\s/]+\.(?:eml|msg|mbox|pst|ost)\b"),
}


class ProjectionError(ValueError):
    """Raised when the canonical register cannot be projected safely."""


def read_source() -> tuple[bytes, list[dict[str, str]], tuple[str, ...]]:
    source_bytes = SOURCE.read_bytes()
    with SOURCE.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = tuple(reader.fieldnames or ())
        rows = list(reader)

    required = set(FIELD_ALLOWLIST) | {"Public_Treatment"} | set(PRIVATE_SOURCE_FIELDS)
    missing = sorted(required - set(headers))
    if missing:
        raise ProjectionError("canonical CSV missing required fields: " + ", ".join(missing))
    if not rows:
        raise ProjectionError("canonical CSV contains no records")
    if any(None in row for row in rows):
        raise ProjectionError("canonical CSV contains a malformed record with excess fields")
    return source_bytes, rows, headers


def build_projection() -> dict[str, object]:
    source_bytes, source_rows, _ = read_source()
    known_treatments = set(PUBLIC_TREATMENTS) | set(EXCLUDED_TREATMENTS)
    observed_treatments = {
        (row.get("Public_Treatment") or "").strip() for row in source_rows
    }
    unknown = sorted(observed_treatments - known_treatments)
    if unknown:
        raise ProjectionError(
            "unreviewed Public_Treatment value(s); update publication policy first: "
            + ", ".join(repr(value) for value in unknown)
        )

    source_ids: list[str] = []
    records: list[dict[str, str]] = []
    excluded_count = 0
    for line_number, row in enumerate(source_rows, start=2):
        master_id = (row.get("Master_ID") or "").strip()
        if not master_id:
            raise ProjectionError(f"canonical CSV line {line_number} has no Master_ID")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", master_id):
            raise ProjectionError(
                f"canonical CSV line {line_number} has a Master_ID unsafe for a public fragment"
            )
        source_ids.append(master_id)

        treatment = (row.get("Public_Treatment") or "").strip()
        if treatment in EXCLUDED_TREATMENTS:
            excluded_count += 1
            continue
        if treatment not in PUBLIC_TREATMENTS:
            raise ProjectionError(
                f"canonical CSV line {line_number} is not covered by the public policy"
            )
        public_record = {field: row.get(field, "") or "" for field in FIELD_ALLOWLIST}
        for field, value in public_record.items():
            for label, pattern in FORBIDDEN_PUBLIC_VALUE_PATTERNS.items():
                if pattern.search(value):
                    raise ProjectionError(
                        f"canonical CSV line {line_number} field {field} contains a forbidden {label}"
                    )
        records.append(public_record)

    if len(source_ids) != len(set(source_ids)):
        raise ProjectionError("canonical CSV contains duplicate Master_ID values")
    public_ids = [record["Master_ID"] for record in records]
    if len(public_ids) != len(set(public_ids)):
        raise ProjectionError("public projection contains duplicate Master_ID values")

    return {
        "schema_version": "1.0.0",
        "dataset": "por-derecho.public-proceedings-projection",
        "canonical_source_id": "PROCEEDINGS_MASTER_REGISTER",
        "derivation": "DETERMINISTIC_ALLOWLIST",
        "canonical_source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "publication_policy": {
            "eligibility_field": "Public_Treatment",
            "public_treatment_allowlist": list(PUBLIC_TREATMENTS),
            "excluded_treatment_values": list(EXCLUDED_TREATMENTS),
            "unknown_treatment_policy": "BUILD_ERROR",
        },
        "field_allowlist": list(FIELD_ALLOWLIST),
        "source_record_count": len(source_rows),
        "public_record_count": len(records),
        "excluded_record_count": excluded_count,
        "records": records,
    }


def serialise(payload: dict[str, object]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the committed public projection differs from a fresh build",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="write the generated projection to stdout without changing the target",
    )
    args = parser.parse_args()
    if args.check and args.stdout:
        parser.error("--check and --stdout are mutually exclusive")

    try:
        expected = serialise(build_projection())
    except (OSError, ProjectionError) as exc:
        print(f"PUBLIC PROCEEDINGS PROJECTION: FAILED — {exc}", file=sys.stderr)
        return 1

    if args.stdout:
        sys.stdout.write(expected)
        return 0

    if args.check:
        if not TARGET.is_file():
            print(
                f"PUBLIC PROCEEDINGS PROJECTION: FAILED — missing {TARGET.relative_to(ROOT)}",
                file=sys.stderr,
            )
            return 1
        if TARGET.read_text(encoding="utf-8") != expected:
            print(
                "PUBLIC PROCEEDINGS PROJECTION: FAILED — generated asset is stale; "
                "run python3 scripts/build_public_proceedings_projection.py",
                file=sys.stderr,
            )
            return 1
        payload = json.loads(expected)
        print(
            "PUBLIC PROCEEDINGS PROJECTION: VERIFIED — "
            f"{payload['public_record_count']} public records; "
            f"{payload['excluded_record_count']} excluded"
        )
        return 0

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(expected, encoding="utf-8")
    payload = json.loads(expected)
    print(
        "PUBLIC PROCEEDINGS PROJECTION: BUILT — "
        f"{payload['public_record_count']} public records; "
        f"{payload['excluded_record_count']} excluded"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

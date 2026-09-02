#!/usr/bin/env python3
"""Synchronise Master publication audit denominators from canonical controlled data.

The audit remains fail-closed and continues to verify the projection hash,
allowlist, field boundary, trace destinations and isolation destinations.  This
helper only removes stale snapshot arithmetic: its six expected denominators are
derived from the canonical CSV plus the deterministic public projection before
the audit runs.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from build_public_proceedings_projection import EXCLUDED_TREATMENTS, PUBLIC_TREATMENTS

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
PROJECTION = ROOT / "assets/data/proceedings-master-public-v1.json"
AUDIT = ROOT / "scripts/audit_master_proceedings_publication.py"


def main() -> int:
    with CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    projection = json.loads(PROJECTION.read_text(encoding="utf-8"))
    public_records = projection.get("records") or []

    if projection.get("source_record_count") != len(rows):
        raise SystemExit(
            f"projection source count {projection.get('source_record_count')} != canonical {len(rows)}"
        )
    eligible_rows = [
        row
        for row in rows
        if (row.get("Public_Treatment") or "").strip() in PUBLIC_TREATMENTS
    ]
    excluded_rows = [
        row
        for row in rows
        if (row.get("Public_Treatment") or "").strip() in EXCLUDED_TREATMENTS
    ]
    if len(public_records) != len(eligible_rows):
        raise SystemExit(
            f"projection public count {len(public_records)} != eligible canonical rows {len(eligible_rows)}"
        )

    canonical_exact = [
        row for row in rows if (row.get("Is_Proceeding") or "").strip().upper() == "TRUE"
    ]
    public_exact = [
        row
        for row in public_records
        if (row.get("Is_Proceeding") or "").strip().upper() == "TRUE"
    ]
    excluded_exact = [
        row
        for row in excluded_rows
        if (row.get("Is_Proceeding") or "").strip().upper() == "TRUE"
    ]
    public_non_exact = [
        row
        for row in public_records
        if (row.get("Is_Proceeding") or "").strip().upper() != "TRUE"
    ]

    if len(canonical_exact) != len(public_exact) + len(excluded_exact):
        raise SystemExit(
            "canonical exact denominator is not partitioned by public + excluded exact records"
        )
    if len(public_records) != len(public_exact) + len(public_non_exact):
        raise SystemExit("public denominator is not partitioned by exact + non-exact records")

    expected = {
        "EXPECTED_CANONICAL_RECORDS": len(rows),
        "EXPECTED_PUBLIC_RECORDS": len(public_records),
        "EXPECTED_CANONICAL_EXACT_PROCEEDINGS": len(canonical_exact),
        "EXPECTED_PUBLIC_EXACT_PROCEEDINGS": len(public_exact),
        "EXPECTED_PRIVATE_EXACT_PROCEEDINGS": len(excluded_exact),
        "EXPECTED_PUBLIC_NON_EXACT_RECORDS": len(public_non_exact),
    }

    text = AUDIT.read_text(encoding="utf-8")
    original = text
    for name, value in expected.items():
        pattern = rf"(?m)^{re.escape(name)}\s*=\s*\d+\s*$"
        text, n = re.subn(pattern, f"{name} = {value}", text, count=1)
        if n != 1:
            raise SystemExit(f"could not uniquely update {name} in {AUDIT}")
    AUDIT.write_text(text, encoding="utf-8")

    state = "IDEMPOTENT" if text == original else "UPDATED"
    print("MASTER_PROCEEDINGS_AUDIT_COUNTS_SYNCED", expected, state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

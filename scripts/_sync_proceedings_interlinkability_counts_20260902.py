#!/usr/bin/env python3
"""Synchronise stale interlinkability snapshot counts from canonical controlled sources.

This is deliberately narrow. It does not change relationship logic, finite-test
classification, source gaps, episode mappings, or publication policy. It only
refreshes record-denominator constants in build_proceedings_interlinkability_v1.py
after PROCEEDINGS_MASTER_REGISTER.csv and proceedings-master-public-v1.json have
been reconciled and independently projected.  The Fiscalía denominator is derived
with the builder's own membership rule: public rows whose canonical Stream contains
"FISCAL".
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
PUBLIC = ROOT / "assets/data/proceedings-master-public-v1.json"
BUILDER = ROOT / "scripts/build_proceedings_interlinkability_v1.py"


def main() -> int:
    with MASTER.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    projection = json.loads(PUBLIC.read_text(encoding="utf-8"))
    public_rows = projection.get("records") or []

    source_count = projection.get("source_record_count")
    public_count = projection.get("public_record_count")
    if source_count != len(rows):
        raise SystemExit(
            f"public projection source denominator mismatch: projection={source_count} master={len(rows)}"
        )
    if public_count != len(public_rows):
        raise SystemExit(
            f"public projection record denominator mismatch: declared={public_count} rows={len(public_rows)}"
        )

    canonical_exact_ids = {
        (row.get("Master_ID") or "").strip()
        for row in rows
        if (row.get("Is_Proceeding") or "").strip().upper() == "TRUE"
    }
    public_exact_ids = {
        (row.get("Master_ID") or "").strip()
        for row in public_rows
        if (row.get("Is_Proceeding") or "").strip().upper() == "TRUE"
    }
    if not public_exact_ids <= canonical_exact_ids:
        raise SystemExit(
            "public projection contains exact proceedings absent from canonical Master: "
            + ", ".join(sorted(public_exact_ids - canonical_exact_ids))
        )

    public_fiscalia_rows = [
        row for row in public_rows if "FISCAL" in (row.get("Stream") or "").upper()
    ]

    counts = {
        "EXPECTED_PUBLIC_RECORDS": len(public_rows),
        "EXPECTED_CANONICAL_EXACT_PROCEEDINGS": len(canonical_exact_ids),
        "EXPECTED_PUBLIC_EXACT_PROCEEDINGS": len(public_exact_ids),
        "EXPECTED_PRIVATE_EXACT_PROCEEDINGS": len(canonical_exact_ids - public_exact_ids),
        "EXPECTED_FISCALIA_OFFICE_FILE_RECORDS": len(public_fiscalia_rows),
    }

    text = BUILDER.read_text(encoding="utf-8")
    original = text
    for name, value in counts.items():
        pattern = rf"(?m)^{re.escape(name)}\s*=\s*\d+\s*$"
        replacement = f"{name} = {value}"
        text, n = re.subn(pattern, replacement, text, count=1)
        if n != 1:
            raise SystemExit(f"could not uniquely update {name} in {BUILDER}")

    BUILDER.write_text(text, encoding="utf-8")
    state = "IDEMPOTENT" if text == original else "UPDATED"
    print("PROCEEDINGS_INTERLINKABILITY_COUNTS_SYNCED", counts, state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

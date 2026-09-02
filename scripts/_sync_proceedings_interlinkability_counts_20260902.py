#!/usr/bin/env python3
"""Synchronise stale interlinkability snapshot counts from canonical controlled sources.

This is deliberately narrow. It does not change relationship logic, finite-test
questions, source gaps, episode mappings, or publication policy. It refreshes the
record-denominator constants and the expected finite-test family census in
build_proceedings_interlinkability_v1.py after the Master and public projection
have been reconciled.

The family census is independently derived here from the documented canonical
Record_Type / Stream taxonomy. The builder still classifies each file itself and
compares its observed census against this expected census, so a later change to
the builder taxonomy does not silently self-validate. No exact proceeding is
allowed to fall through to the general fallback family.

The Fiscalía matrix split is independently derived from the public Fiscalía rows'
canonical Is_Proceeding values. Exact and unresolved counts remain separate gates;
no unresolved file is promoted to an exact proceeding by this synchroniser.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
PUBLIC = ROOT / "assets/data/proceedings-master-public-v1.json"
BUILDER = ROOT / "scripts/build_proceedings_interlinkability_v1.py"

FAMILY_ORDER = (
    "ADMIN_AUTHORITY_TITLE_SOURCE",
    "CIVIL_FILE_DECISION",
    "CRIMINAL_FILE_DECISION",
    "FISCALIA_INSTITUTIONAL_MEMORY",
    "OMBUDSMAN_RECONSIDERATION",
    "PROFESSIONAL_SUPERVISION",
    "REGULATORY_PUBLIC_ROUTE",
    "TAX_CONTENTIOUS_CHAIN",
)


def expected_family(row: dict[str, str]) -> str:
    """Independent mirror of the documented conservative family taxonomy."""
    stream = (row.get("Stream") or "").upper()
    master_id = row.get("Master_ID") or ""
    record_type = (row.get("Record_Type") or "").upper()

    if "OMBUDSMAN" in stream or master_id.startswith("CAN-OMB-"):
        return "OMBUDSMAN_RECONSIDERATION"
    if "FISCAL" in stream or "-FIS-" in master_id:
        return "FISCALIA_INSTITUTIONAL_MEMORY"
    if (
        "AEAT" in stream
        or master_id.startswith("NAT-AEAT-")
        or master_id in {"MAD-AN-CONT-001", "MAD-AN-CONT-002"}
    ):
        return "TAX_CONTENTIOUS_CHAIN"
    if any(
        token in stream
        for token in ("CNMV", "SNCA", "TREASURY", "PUBLIC AID", "LAW 2/2023")
    ):
        return "REGULATORY_PUBLIC_ROUTE"
    if record_type == "PROFESSIONAL_DISCIPLINE":
        return "PROFESSIONAL_SUPERVISION"
    if record_type in {"ADMINISTRATIVE_FILE", "TRANSPARENCY_CLAIM"} or any(
        token in stream
        for token in (
            "ADMINISTRATIVE",
            "TOURISM",
            "MUNICIPAL",
            "TRANSPARENCY",
            "JUDICIAL GOVERNANCE",
        )
    ):
        return "ADMIN_AUTHORITY_TITLE_SOURCE"
    if "CRIMINAL" in stream:
        return "CRIMINAL_FILE_DECISION"
    if "CIVIL" in stream or "INSOLVENCY" in stream:
        return "CIVIL_FILE_DECISION"
    if "PROFESSIONAL" in stream:
        return "PROFESSIONAL_SUPERVISION"
    return "GENERAL_EXACT_FILE_DECISION_TEST"


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
    public_exact_rows = [
        row
        for row in public_rows
        if (row.get("Is_Proceeding") or "").strip().upper() == "TRUE"
    ]
    public_exact_ids = {(row.get("Master_ID") or "").strip() for row in public_exact_rows}
    if not public_exact_ids <= canonical_exact_ids:
        raise SystemExit(
            "public projection contains exact proceedings absent from canonical Master: "
            + ", ".join(sorted(public_exact_ids - canonical_exact_ids))
        )

    public_fiscalia_rows = [
        row for row in public_rows if "FISCAL" in (row.get("Stream") or "").upper()
    ]
    fiscalia_state_counts = Counter(
        (row.get("Is_Proceeding") or "").strip().upper() for row in public_fiscalia_rows
    )
    unsupported_fiscalia_states = sorted(
        state for state in fiscalia_state_counts if state not in {"TRUE", "UNVERIFIED"}
    )
    if unsupported_fiscalia_states:
        raise SystemExit(
            "public Fiscalía matrix contains unsupported Is_Proceeding states: "
            + ", ".join(unsupported_fiscalia_states)
        )
    if sum(fiscalia_state_counts.values()) != len(public_fiscalia_rows):
        raise SystemExit("Fiscalía exact/unresolved split does not cover its public denominator")

    family_by_id = {
        row["Master_ID"]: expected_family(row)
        for row in public_exact_rows
    }
    fallback_ids = sorted(
        master_id
        for master_id, family_id in family_by_id.items()
        if family_id == "GENERAL_EXACT_FILE_DECISION_TEST"
    )
    if fallback_ids:
        raise SystemExit(
            "exact proceedings reached the general finite-test fallback; classify source-led before release: "
            + ", ".join(fallback_ids)
        )
    family_counts = Counter(family_by_id.values())
    unexpected_families = sorted(set(family_counts) - set(FAMILY_ORDER))
    if unexpected_families:
        raise SystemExit("unexpected finite-test family ids: " + ", ".join(unexpected_families))
    if sum(family_counts.values()) != len(public_exact_rows):
        raise SystemExit("finite-test expected family census does not cover public exact denominator")

    counts = {
        "EXPECTED_PUBLIC_RECORDS": len(public_rows),
        "EXPECTED_CANONICAL_EXACT_PROCEEDINGS": len(canonical_exact_ids),
        "EXPECTED_PUBLIC_EXACT_PROCEEDINGS": len(public_exact_ids),
        "EXPECTED_PRIVATE_EXACT_PROCEEDINGS": len(canonical_exact_ids - public_exact_ids),
        "EXPECTED_FISCALIA_OFFICE_FILE_RECORDS": len(public_fiscalia_rows),
        "EXPECTED_FISCALIA_EXACT_RECORDS": fiscalia_state_counts["TRUE"],
        "EXPECTED_FISCALIA_UNVERIFIED_RECORDS": fiscalia_state_counts["UNVERIFIED"],
    }

    text = BUILDER.read_text(encoding="utf-8")
    original = text

    # Older builders pre-date the split constants. Insert them once, adjacent to
    # the existing Fiscalía denominator, then keep all three scalar expectations
    # synchronised from the public controlled projection.
    if "EXPECTED_FISCALIA_EXACT_RECORDS" not in text:
        anchor = re.search(
            r"(?m)^EXPECTED_FISCALIA_OFFICE_FILE_RECORDS\s*=\s*\d+\s*$",
            text,
        )
        if not anchor:
            raise SystemExit("Fiscalía office/file denominator anchor missing in builder")
        insertion = (
            anchor.group(0)
            + "\nEXPECTED_FISCALIA_EXACT_RECORDS = 0"
            + "\nEXPECTED_FISCALIA_UNVERIFIED_RECORDS = 0"
        )
        text = text[: anchor.start()] + insertion + text[anchor.end() :]

    for name, value in counts.items():
        pattern = rf"(?m)^{re.escape(name)}\s*=\s*\d+\s*$"
        replacement = f"{name} = {value}"
        text, n = re.subn(pattern, replacement, text, count=1)
        if n != 1:
            raise SystemExit(f"could not uniquely update {name} in {BUILDER}")

    family_block = "EXPECTED_FINITE_TEST_FAMILY_COUNTS = {\n" + "".join(
        f'    "{family_id}": {family_counts[family_id]},\n'
        for family_id in FAMILY_ORDER
        if family_counts[family_id]
    ) + "}"
    text, n = re.subn(
        r"EXPECTED_FINITE_TEST_FAMILY_COUNTS\s*=\s*\{.*?\n\}",
        family_block,
        text,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit(f"could not uniquely update EXPECTED_FINITE_TEST_FAMILY_COUNTS in {BUILDER}")

    split_pattern = re.compile(
        r"if \(fiscalia_matrix_exact_count, fiscalia_matrix_unverified_count\) != "
        r"(?:\(\d+,\s*\d+\)|\(EXPECTED_FISCALIA_EXACT_RECORDS,\s*EXPECTED_FISCALIA_UNVERIFIED_RECORDS\)):\n"
        r"\s*raise ValueError\(\n"
        r"\s*\"Fiscalía office/file matrix must preserve its .*? split\"\n"
        r"\s*\)",
        re.S,
    )
    split_replacement = (
        "if (fiscalia_matrix_exact_count, fiscalia_matrix_unverified_count) != (\n"
        "        EXPECTED_FISCALIA_EXACT_RECORDS,\n"
        "        EXPECTED_FISCALIA_UNVERIFIED_RECORDS,\n"
        "    ):\n"
        "        raise ValueError(\n"
        "            \"Fiscalía office/file exact/unresolved split is stale: \"\n"
        "            f\"expected {EXPECTED_FISCALIA_EXACT_RECORDS} exact + \"\n"
        "            f\"{EXPECTED_FISCALIA_UNVERIFIED_RECORDS} unresolved, found \"\n"
        "            f\"{fiscalia_matrix_exact_count} + {fiscalia_matrix_unverified_count}\"\n"
        "        )"
    )
    text, n = split_pattern.subn(split_replacement, text, count=1)
    if n != 1:
        raise SystemExit("could not uniquely update Fiscalía exact/unresolved matrix gate")

    BUILDER.write_text(text, encoding="utf-8")
    state = "IDEMPOTENT" if text == original else "UPDATED"
    print(
        "PROCEEDINGS_INTERLINKABILITY_COUNTS_SYNCED",
        counts,
        "families=",
        {family_id: family_counts[family_id] for family_id in FAMILY_ORDER if family_counts[family_id]},
        state,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

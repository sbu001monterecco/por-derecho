#!/usr/bin/env python3
"""Build the public-safe Red SARA/AGE filing and attachment projection.

The institutional communications register remains the sole canonical source for
communications.  This generated file is a narrow, deterministic public view:
all individually source-proved REGAGE rows plus the safe attachment index from
the 154-page baseline derivative.  It deliberately does not manufacture a
receipt-to-attachment map where the controlling public source does not provide
one.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/data/institutional-communications-register-v1.json"
ATTACHMENTS = ROOT / "archive/evidence/mf-redsara-anexo4/MF_REDSARA_UNIQUE_ATTACHMENT_INDEX.csv"
OUTPUT = ROOT / "assets/data/redsara-age-filings-register-v1.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def build() -> dict[str, Any]:
    source = load_json(SOURCE)
    events = source.get("events", [])
    if not isinstance(events, list):
        raise ValueError("communications events must be an array")
    filings = [event for event in events if isinstance(event, dict) and event.get("channel") == "REGAGE"]
    filings.sort(key=lambda event: (str(event.get("event_date", "")), str(event.get("official_reference", "")), str(event.get("event_id", ""))))
    attachment_rows: list[dict[str, Any]] = []
    with ATTACHMENTS.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            attachment_rows.append({
                "filename": row["Attachment_Filename"],
                "sha512_as_listed": row["SHA512_As_Listed"],
                "receipt_occurrences": int(row["Receipt_Occurrences"]),
            })
    denominator = source.get("denominator_control", {})
    source_controls = source.get("source_controls", {})
    return {
        "schema": "por-derecho.redsara-age-filings-register.v1",
        "register_id": "PD-SP-REDSARA-AGE-FILINGS-001",
        "control_date": source.get("control_date"),
        "derived_projection": {
            "canonical_communications_register": "assets/data/institutional-communications-register-v1.json",
            "canonical_communications_register_id": source.get("register_id"),
            "attachment_index": "archive/evidence/mf-redsara-anexo4/MF_REDSARA_UNIQUE_ATTACHMENT_INDEX.csv",
            "builder": "scripts/build_redsara_age_filings_register.py",
            "source_of_truth_rule": "This is a deterministic, read-only projection. The institutional communications register remains the sole canonical communications register.",
        },
        "scope_and_boundary": {
            "filing_event_rows_currently_individualised": len(filings),
            "detailed_baseline_receipts": denominator.get("detailed_baseline_receipt_rows_registered"),
            "separate_source_proved_regage_events": len([event for event in filings if event.get("cohort") != "BASELINE_REDSARA_ANEXO4_75"]),
            "historic_regage_total_reported": denominator.get("wider_regage_records_reported"),
            "aggregate_only_batch": source.get("unresolved_batches", []),
            "reconciliation_boundary": "The reported 97-record denominator is controlled as 75 detailed receipts plus one 22-record aggregate-only batch. It must not be described as a complete 97-row, duplicate-free receipt register without individual source-proved rows. The 92 current individual REGAGE event rows and that historic 97-record reporting denominator are separate controlled representations; do not arithmetically combine them or treat them as one unduplicated population without a source-proved crosswalk.",
            "receipt_boundary": "A registry receipt proves only the stated presentation, time, registry destination and listed annex metadata. It does not alone prove downstream delivery, incorporation, examination, decision, reliance, payment, effect, causation, intent, offence or guilt.",
            "attachment_boundary": "The public attachment index records 100 unique filename/SHA-512 pairs and their receipt-occurrence counts for the detailed 75-receipt baseline. The public source does not establish a complete individual receipt-to-attachment mapping, so none is inferred here.",
            "privacy_boundary": "No native receipt bundle, private email, direct contact detail, provider locator or unredacted private file is published by this projection.",
        },
        "source_controls": {
            "detailed_receipt_index": source_controls.get("detailed_index"),
            "detailed_receipt_index_sha256": source_controls.get("detailed_index_sha256"),
            "controlling_154_page_pdf_sha256": source_controls.get("controlling_154_page_pdf_sha256"),
            "baseline_annex_listings": source_controls.get("annex_listing_count"),
            "unique_public_safe_attachment_rows": len(attachment_rows),
        },
        "filings": [
            {
                key: event.get(key)
                for key in (
                    "event_id", "source_key", "cohort", "event_date", "presented_local", "record_type", "direction", "channel",
                    "official_reference", "office", "institution_key", "recipient_dir3", "source_pages", "annex_count",
                    "subject_category", "subject_label_status", "public_summary", "public_summary_es", "proves", "proves_es",
                    "does_not_prove", "does_not_prove_es", "evidence_classes", "evidence_state", "handling_state",
                    "matter_references", "canonical_anchor_en", "canonical_anchor_es", "source_integrity",
                )
                if key in event
            }
            for event in filings
        ],
        "attachment_index": attachment_rows,
    }


def serialized(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true", help="write the deterministic public projection")
    group.add_argument("--check", action="store_true", help="fail if the checked-in projection differs")
    args = parser.parse_args()
    expected = serialized(build())
    if args.write:
        OUTPUT.write_text(expected, encoding="utf-8")
        print(f"wrote {OUTPUT.relative_to(ROOT)}")
        return 0
    try:
        actual = OUTPUT.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"missing projection: {exc}", file=sys.stderr)
        return 1
    if actual != expected:
        print("Red SARA/AGE projection is stale; run scripts/build_redsara_age_filings_register.py --write", file=sys.stderr)
        return 1
    print("Red SARA/AGE filing and attachment projection is deterministic")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

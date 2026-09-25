#!/usr/bin/env python3
"""Regression tests for institutional communications reconciliation controls."""

from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from reconcile_institutional_communications import (
    DEFAULT_CHECKPOINT,
    DEFAULT_MAILBOX_INDEX,
    DEFAULT_REGISTER,
    DEFAULT_SOURCE,
    KEY_EVENTS,
    MAILBOX_COHORT,
    PRIVATE_MANIFEST_SHA256,
    RECEIPT_BOUNDARY,
    build_receipt_events,
    load_source_rows,
)
from build_public_mailbox_event_index import ALLOWED_DIRECTIONS, ALLOWED_OFFICE_ROUTES, TRANSPORT_STATE
from validate_institutional_communications import (
    REPO_ROOT,
    _scan_public_safety,
    load_json,
    validate_register,
)


def source_row(reference: str, presented: str) -> dict[str, object]:
    return {
        "source_pages": "1-1",
        "presented": datetime.fromisoformat(presented),
        "official_reference": reference,
        "office": "Fiscalia Provincial de Las Palmas",
        "source_subject": "Synthetic formal registration label",
        "annex_count": 1,
    }


class ReconciliationTests(unittest.TestCase):
    def test_real_baseline_has_exact_denominator(self) -> None:
        rows = load_source_rows(DEFAULT_SOURCE)
        self.assertEqual(len(rows), 75)
        self.assertEqual(sum(int(row["annex_count"]) for row in rows), 126)
        self.assertEqual(len({row["official_reference"] for row in rows}), 75)

    def test_stable_ids_survive_an_earlier_new_row(self) -> None:
        first_rows = [
            source_row("REGAGE26e00000000001", "2026-01-02T10:00:00"),
            source_row("REGAGE26e00000000002", "2026-01-03T10:00:00"),
        ]
        first = build_receipt_events(first_rows)
        existing = {"events": first + deepcopy(KEY_EVENTS)}
        prior_ids = {event["official_reference"]: event["event_id"] for event in first}

        later_rows = [source_row("REGAGE26e00000000003", "2026-01-01T10:00:00"), *first_rows]
        second = build_receipt_events(later_rows, existing)
        second_ids = {event["official_reference"]: event["event_id"] for event in second}
        self.assertEqual(second_ids["REGAGE26e00000000001"], prior_ids["REGAGE26e00000000001"])
        self.assertEqual(second_ids["REGAGE26e00000000002"], prior_ids["REGAGE26e00000000002"])
        self.assertEqual(second_ids["REGAGE26e00000000003"], "PD-SP-EVT-0003")

    def test_duplicate_regage_is_rejected_not_silently_collapsed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["Source_Pages", "Presented", "REGAGE", "Recipient", "Subject", "Annexes"],
                )
                writer.writeheader()
                writer.writerow({
                    "Source_Pages": "1-1",
                    "Presented": "01/01/2026 10:00:00",
                    "REGAGE": "REGAGE26e00000000001",
                    "Recipient": "Fiscalia Provincial de Las Palmas",
                    "Subject": "One",
                    "Annexes": "1",
                })
                writer.writerow({
                    "Source_Pages": "2-2",
                    "Presented": "01/01/2026 10:00:00",
                    "REGAGE": "REGAGE26e00000000001",
                    "Recipient": "Fiscalia Provincial de Las Palmas",
                    "Subject": "Conflicting two",
                    "Annexes": "1",
                })
            with self.assertRaisesRegex(ValueError, "conflicting duplicate REGAGE"):
                load_source_rows(path, expected_count=2)

    def test_private_provider_fields_are_rejected(self) -> None:
        errors: list[str] = []
        synthetic_provider_id = "deadbeef" * 2
        _scan_public_safety(
            {"gmail_message_id": synthetic_provider_id, "email_body": "synthetic private fixture"},
            "fixture",
            errors,
        )
        self.assertTrue(any("gmail_message_id" in error for error in errors))
        self.assertTrue(any("email_body" in error for error in errors))

    def test_receipt_cannot_be_upgraded_to_delivery_or_merits(self) -> None:
        register = load_json(DEFAULT_REGISTER)
        checkpoint = load_json(DEFAULT_CHECKPOINT)
        mutated = deepcopy(register)
        receipt = next(event for event in mutated["events"] if event["cohort"] == "BASELINE_REDSARA_ANEXO4_75")
        receipt["evidence_state"]["delivery"] = "DELIVERED_AND_EXAMINED"
        errors = validate_register(
            mutated,
            checkpoint,
            repo_root=REPO_ROOT,
            source_path=DEFAULT_SOURCE,
            register_path=DEFAULT_REGISTER,
        )
        self.assertTrue(any("receipt evidence-state boundary changed" in error for error in errors))
        self.assertTrue(any("receipt status improperly exceeds" in error for error in errors))

    def test_metadata_only_22_remain_one_batch(self) -> None:
        register = load_json(DEFAULT_REGISTER)
        self.assertEqual(len(register["unresolved_batches"]), 1)
        batch = register["unresolved_batches"][0]
        self.assertEqual(batch["record_count"], 22)
        self.assertEqual(batch["synthetic_event_rows_created"], 0)
        self.assertFalse(any(event.get("cohort") == "METADATA_ONLY_22" for event in register["events"]))

    def test_rediscovered_di113_and_di22_events_remain_individual(self) -> None:
        register = load_json(DEFAULT_REGISTER)
        curated = [event for event in register["events"] if event["cohort"] == "CURATED_SOURCE_PROVED_EVENT"]
        di113 = {
            event["event_date"]: event
            for event in curated
            if "DI 113/2022" in event.get("matter_references", []) and event["event_id"] != "PD-SP-EVT-0083"
        }
        self.assertEqual(set(di113), {"2023-02-08", "2026-02-23", "2026-02-25"})
        self.assertEqual(di113["2023-02-08"]["signatory_person_id"], "PD-SP-P-0103")
        self.assertEqual(di113["2026-02-23"]["signatory_person_id"], "PD-SP-P-0103")
        self.assertNotIn("signatory_person_id", di113["2026-02-25"])

        di22 = {
            event["event_date"]: event
            for event in curated
            if "DI 22/2026" in event.get("matter_references", []) and event["event_id"] != "PD-SP-EVT-0083"
        }
        signed_dates = {"2026-02-11", "2026-02-13", "2026-02-16", "2026-02-19", "2026-03-02", "2026-03-03"}
        office_only_dates = {"2026-06-03", "2026-06-30", "2026-07-08"}
        self.assertEqual(set(di22), signed_dates | office_only_dates)
        for date in signed_dates:
            self.assertEqual(di22[date]["attribution_state"], "SOURCE_PROVED_SIGNATORY")
            self.assertEqual(di22[date]["signatory_person_id"], "PD-SP-P-0103")
        for date in office_only_dates:
            self.assertEqual(di22[date]["attribution_state"], "INSTITUTION_ONLY_SIGNATURE_PENDING")
            self.assertNotIn("signatory_person_id", di22[date])

    def test_receipt_subjects_are_category_and_digest_only(self) -> None:
        register = load_json(DEFAULT_REGISTER)
        receipts = [event for event in register["events"] if event["cohort"] == "BASELINE_REDSARA_ANEXO4_75"]
        self.assertEqual(len(receipts), 75)
        for event in receipts:
            self.assertNotIn("public_subject", event)
            self.assertRegex(event["subject_digest_sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(event["subject_category"])

    def test_generated_receipt_boundary_is_exact(self) -> None:
        event = build_receipt_events([source_row("REGAGE26e00000000004", "2026-01-04T10:00:00")])[0]
        self.assertEqual(event["evidence_state"], RECEIPT_BOUNDARY)
        self.assertEqual(event["evidence_state"]["delivery"], "NOT_ESTABLISHED_BY_RECEIPT")
        self.assertEqual(event["evidence_state"]["merits"], "NOT_ESTABLISHED_BY_RECEIPT")

    def test_current_register_and_checkpoint_validate(self) -> None:
        register = load_json(DEFAULT_REGISTER)
        checkpoint = load_json(DEFAULT_CHECKPOINT)
        self.assertEqual(
            validate_register(
                register,
                checkpoint,
                repo_root=REPO_ROOT,
                source_path=DEFAULT_SOURCE,
                register_path=DEFAULT_REGISTER,
            ),
            [],
        )

    def test_public_mailbox_index_has_complete_safe_denominator(self) -> None:
        mailbox = load_json(DEFAULT_MAILBOX_INDEX)
        self.assertEqual(len(mailbox["events"]), 156)
        self.assertEqual(len({event["event_id"] for event in mailbox["events"]}), 156)
        self.assertEqual(len({event["public_event_match_key"] for event in mailbox["events"]}), 156)
        self.assertEqual(mailbox["source_custody"]["manifest_sha256"], PRIVATE_MANIFEST_SHA256)
        self.assertEqual(mailbox["source_custody"]["manifest_rows"], 231)
        self.assertEqual(mailbox["source_custody"]["persistence_status"], "PERSISTED_PRIVATE_CUSTODY")
        for event in mailbox["events"]:
            self.assertIn(event["direction"], ALLOWED_DIRECTIONS)
            self.assertIn(event["office_route"], ALLOWED_OFFICE_ROUTES)
            self.assertEqual(event["transport_state"], TRANSPORT_STATE[event["direction"]])
            self.assertFalse(event["subject_text_published"])

    def test_transport_and_official_act_layers_do_not_collapse(self) -> None:
        register = load_json(DEFAULT_REGISTER)
        mailbox_ids = {event["event_id"] for event in register["events"] if event["cohort"] == MAILBOX_COHORT}
        non_mailbox_ids = {event["event_id"] for event in register["events"] if event["cohort"] != MAILBOX_COHORT}
        self.assertEqual(len(mailbox_ids), 156)
        self.assertFalse(mailbox_ids & non_mailbox_ids)
        di22 = [
            event for event in register["events"]
            if "DI 22/2026" in event.get("matter_references", [])
            and event["cohort"] == "CURATED_SOURCE_PROVED_EVENT"
            and event["record_type"] in {"OFFICIAL_DECISION", "OFFICIAL_ROUTING_ACT"}
        ]
        self.assertEqual(len(di22), 11)
        self.assertEqual(sum(event["event_date"] == "2026-02-11" for event in di22), 2)
        self.assertEqual(sum(event["event_date"] == "2026-02-13" for event in di22), 2)

    def test_drafts_self_archive_and_august_receipts_keep_status_boundaries(self) -> None:
        register = load_json(DEFAULT_REGISTER)
        mailbox = [event for event in register["events"] if event["cohort"] == MAILBOX_COHORT]
        self.assertEqual(sum(event["record_type"] == "EMAIL_DRAFT" for event in mailbox), 3)
        self.assertEqual(sum(event["record_type"] == "SELF_ARCHIVE_CONTROL" for event in mailbox), 10)
        for event in mailbox:
            if event["record_type"] == "EMAIL_DRAFT":
                self.assertEqual(event["evidence_state"]["transmission"], "DRAFT_NOT_SENT")
            if event["record_type"] == "SELF_ARCHIVE_CONTROL":
                self.assertEqual(event["evidence_state"]["transmission"], "SELF_ARCHIVE_CONTROL_NOT_AN_INSTITUTIONAL_SEND")
        august = [
            event for event in register["events"]
            if event["record_type"] == "REGISTRATION_RECEIPT"
            and event["event_date"] == "2026-08-02"
            and "REGAGE26e000702" in event["official_reference"]
        ]
        self.assertEqual(len(august), 7)
        self.assertTrue(all(event["evidence_state"] == RECEIPT_BOUNDARY for event in august))


if __name__ == "__main__":
    unittest.main(verbosity=2)

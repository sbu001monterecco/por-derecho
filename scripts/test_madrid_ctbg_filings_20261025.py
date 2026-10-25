#!/usr/bin/env python3
"""Admission and provenance regressions for the finite October filing cohort."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from load_madrid_ctbg_filings_20261025 import CONTROL, EXPECTED, INPUT, load_filing_events, validate_items


def synthetic_items() -> list[dict]:
    return [
        {
            "event_id": f"PD-SP-EVT-{600 + index:04d}", "reference": reference, "date": date,
            "presented_literal": date + " 10:00:00", "registered_literal": date + " 10:00:03",
            "office": "Synthetic registry destination", "dir3": dir3,
            "matter_references": ["SYNTHETIC-RECEIPT-COHORT"],
            "purpose_en": "Synthetic test fixture, not a source claim.",
            "purpose_es": "Ejemplo sintético de prueba, no una afirmación de fuente.",
            "source_anchor": INPUT, "source_control_sha256": "a" * 64, "source_kind": "NATIVE_REGISTRY_RECEIPT",
            "attachment_count": 2, "attachment_hashes_verified": True,
        }
        for index, (reference, (date, dir3)) in enumerate(EXPECTED.items())
    ]


class FilingAdmissionTests(unittest.TestCase):
    def test_changed_reference_set_is_rejected_even_with_same_count(self) -> None:
        items = synthetic_items()
        items[-1]["reference"] = "REGAGE26e00000000000"
        with self.assertRaisesRegex(ValueError, "reference set"):
            validate_items(items)

    def test_duplicate_receipt_does_not_replace_missing_member(self) -> None:
        items = synthetic_items()
        items[-1] = deepcopy(items[0])
        with self.assertRaisesRegex(ValueError, "reference set"):
            validate_items(items)

    def test_malformed_event_identity_is_rejected(self) -> None:
        items = synthetic_items()
        items[0]["event_id"] = "PD-SP-EVT-99999"
        with self.assertRaisesRegex(ValueError, "event identity"):
            validate_items(items)

    def test_destination_cannot_be_inferred_from_neighbouring_receipt(self) -> None:
        items = synthetic_items()
        items[3]["dir3"] = "J00001430"
        with self.assertRaisesRegex(ValueError, "date/destination"):
            validate_items(items)

    def test_registration_cannot_precede_presentation(self) -> None:
        items = synthetic_items()
        items[0]["registered_literal"] = "2026-10-24 09:59:59"
        with self.assertRaisesRegex(ValueError, "Registration precedes"):
            validate_items(items)

    def test_verification_state_requires_explicit_boolean(self) -> None:
        items = synthetic_items()
        items[0]["attachment_hashes_verified"] = "verified"
        with self.assertRaisesRegex(ValueError, "explicit boolean"):
            validate_items(items)

    def test_private_locator_and_new_private_field_are_rejected(self) -> None:
        items = synthetic_items()
        items[0]["purpose_en"] = "Private source https://drive.google.com/file/d/synthetic"
        with self.assertRaisesRegex(ValueError, "Private locator"):
            validate_items(items)
        items = synthetic_items()
        items[0]["drive_file_id"] = "synthetic"
        with self.assertRaisesRegex(ValueError, "minimised public contract"):
            validate_items(items)

    def test_literal_timestamps_and_exact_input_digest_survive_projection(self) -> None:
        boundary = {"registration": "REGISTRATION_RECEIPT_LOCATED", "merits": "NOT_ESTABLISHED_BY_RECEIPT"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / INPUT
            path.parent.mkdir(parents=True)
            items = synthetic_items()
            items[-1]["presented_literal"] = "25/10/2026 02:48:52"
            items[-1]["registered_literal"] = "25/10/2026 02:49:03"
            raw = (json.dumps({"control_id": CONTROL, "control_date": "2026-10-25", "items": items}) + "\n").encode()
            path.write_bytes(raw)
            events = load_filing_events(root, boundary)
            self.assertEqual(len(events), 6)
            self.assertEqual(events[-1]["presented_local"], "2026-10-25T02:48:52")
            self.assertEqual(events[-1]["event_timestamp"], "2026-10-25T02:49:03")
            self.assertIn("without offset conversion", events[-1]["source_timezone"])
            self.assertEqual(events[-1]["source_integrity"]["sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(events[-1]["evidence_state"], boundary)
            self.assertIsNot(events[-1]["evidence_state"], boundary)
            self.assertNotIn("delivery", events[-1]["evidence_state"])

    def test_read_copy_hash_does_not_become_native_or_attachment_byte_proof(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / INPUT
            path.parent.mkdir(parents=True)
            items = synthetic_items()
            items[0]["source_kind"] = "COMPILED_RECEIPT_READ_COPY"
            items[0]["source_pages"] = "2-3"
            items[0]["attachment_hashes_verified"] = False
            path.write_text(json.dumps({"control_id": CONTROL, "control_date": "2026-10-25", "items": items}))
            event = load_filing_events(root, {"merits": "NOT_ESTABLISHED_BY_RECEIPT"})[0]
            self.assertEqual(event["source_pages"], "2-3")
            self.assertEqual(event["source_integrity"]["status"], "RECEIPT_READ_COPY_PUBLIC_SAFE_DERIVATIVE")
            self.assertEqual(event["proof_level"], "REGISTRATION_RECEIPT_READ_COPY_VERIFIED")
            self.assertNotIn("The listed attachment fingerprints match the retained submitted files.", event["proves"])
            self.assertTrue(any("not asserted to be the native receipt hash" in p for p in event["proves"]))


if __name__ == "__main__":
    unittest.main()

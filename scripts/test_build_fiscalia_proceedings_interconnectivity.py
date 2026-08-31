#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_fiscalia_proceedings_interconnectivity as builder  # noqa: E402


class FiscaliaInterconnectivityBuilderTest(unittest.TestCase):
    def test_reference_normalisation_is_presentation_only(self):
        self.assertEqual(builder.normalise_reference("E.G. 745/2026"), "EG7452026")
        self.assertEqual(builder.normalise_reference("NIG 3501670220260000245"), "NIG3501670220260000245")

    def test_supporting_receipts_are_not_promoted_to_proceedings(self):
        self.assertTrue(builder.is_support_reference("REGAGE26e00070235775"))
        self.assertFalse(builder.is_support_reference("EG 745/2026"))

    def test_complete_deterministic_denominators(self):
        payload = builder.build()
        self.assertEqual(payload["coverage"]["communication_events"], 296)
        self.assertEqual(payload["coverage"]["matter_linked_events"], 117)
        self.assertEqual(payload["coverage"]["fiscalia_identity_total"], 24)
        self.assertEqual(len(payload["priority_chains"]), 9)
        self.assertFalse(payload["coverage"]["unresolved_matter_reference_literals"])

    def test_dp1901_court_request_has_specific_relation(self):
        payload = builder.build()
        edge = next(
            edge for edge in payload["event_proceeding_edges"]
            if edge["event_id"] == "PD-SP-EVT-0082" and edge["master_id"] == "GC-CRI-008"
        )
        self.assertEqual(edge["relationship_type"], "COURT_REQUESTS_FISCAL_REPORT")
        self.assertEqual(edge["relationship_strength"], "DIRECT_FILE_REFERENCE")

    def test_unresolved_identities_remain_unresolved(self):
        payload = builder.build()
        unresolved = {f["master_id"] for f in payload["fiscalia_files"] if f["identity_state"] == "UNRESOLVED_REFERENCE"}
        self.assertEqual(unresolved, {"TF-FIS-009", "TF-FIS-010", "UNK-FIS-001"})


if __name__ == "__main__":
    unittest.main()

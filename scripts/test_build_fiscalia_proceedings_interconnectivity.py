#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_fiscalia_proceedings_interconnectivity as builder  # noqa: E402


class FiscaliaInterconnectivityBuilderTest(unittest.TestCase):
    def test_platform_cohort_is_source_checked_and_not_a_fiscalia_filing(self):
        import copy
        import json
        from prepare_platform_incibe_20260925 import validated_platform_event_ids
        events = json.loads(builder.COMMUNICATIONS.read_text())['events']
        cohort = validated_platform_event_ids(events, ROOT)
        projected = {e['event_id'] for e in builder.build()['events']}
        self.assertEqual(len(cohort), 11)
        self.assertFalse(cohort & projected)
        row = next(e for e in events if e['event_id'] in cohort)
        changed = copy.deepcopy(events)
        next(e for e in changed if e['event_id'] == row['event_id'])['public_summary'] += ' altered'
        with self.assertRaises(ValueError):
            validated_platform_event_ids(changed, ROOT)
        with self.assertRaises(ValueError):
            validated_platform_event_ids([e for e in events if e['event_id'] != row['event_id']], ROOT)
        with self.assertRaises(ValueError):
            validated_platform_event_ids(events + [row], ROOT)

    def test_reference_normalisation_is_presentation_only(self):
        self.assertEqual(builder.normalise_reference("E.G. 745/2026"), "EG7452026")
        self.assertEqual(builder.normalise_reference("NIG 3501670220260000245"), "NIG3501670220260000245")

    def test_supporting_receipts_are_not_promoted_to_proceedings(self):
        self.assertTrue(builder.is_support_reference("REGAGE26e00070235775"))
        self.assertTrue(builder.is_support_reference("A01"))
        self.assertTrue(builder.is_support_reference("IF/MCS"))
        self.assertFalse(builder.is_support_reference("EG 745/2026"))

    def test_complete_deterministic_denominators(self):
        payload = builder.build()
        events = json.loads(builder.COMMUNICATIONS.read_text())["events"]
        october_ids = builder.validated_october_filing_event_ids(events, ROOT)
        expected_successors = {'PD-SP-EVT-0497', 'PD-SP-EVT-0498', 'PD-SP-EVT-0499',
                               'PD-SP-EVT-1157', 'PD-SP-EVT-1158', 'PD-SP-EVT-1159'}
        projected = {e['event_id'] for e in payload['events']}
        self.assertEqual(len(projected - expected_successors - october_ids), 320)
        self.assertTrue(expected_successors <= projected)
        self.assertEqual(payload['coverage']['communication_events'], 326 + len(october_ids))
        self.assertEqual(payload["coverage"]["legacy_communication_events"], 326)
        self.assertEqual(payload["coverage"]["legacy_matter_linked_events"], 141)
        self.assertEqual(payload["coverage"]["matter_linked_events"], 141 + len(october_ids))
        self.assertEqual(payload["coverage"]["fiscalia_identity_total"], 26)
        self.assertEqual(len(payload["priority_chains"]), 9)
        self.assertEqual(payload["coverage"]["unresolved_matter_reference_literals"], payload["october_cohort_control"]["unresolved_matter_reference_literals"])

    def test_october_source_cohort_rejects_mutation_extra_and_reused_identity(self):
        events = json.loads(builder.COMMUNICATIONS.read_text())["events"]
        cohort = builder.validated_october_filing_event_ids(events, ROOT)
        self.assertEqual(len(cohort), 6)
        row = next(event for event in events if event["event_id"] in cohort)
        changed = copy.deepcopy(events)
        next(event for event in changed if event["event_id"] == row["event_id"])["public_summary"] += " altered"
        with self.assertRaises(ValueError):
            builder.validated_october_filing_event_ids(changed, ROOT)
        extra = copy.deepcopy(row)
        extra["event_id"] = "PD-SP-EVT-0999"
        with self.assertRaises(ValueError):
            builder.validated_october_filing_event_ids(events + [extra], ROOT)
        with self.assertRaises(ValueError):
            builder.validated_october_filing_event_ids(events + [row], ROOT)
        substituted = [event for event in events if event["event_id"] != row["event_id"]] + [extra]
        with self.assertRaises(ValueError):
            builder.validated_october_filing_event_ids(substituted, ROOT)
        reused = copy.deepcopy(events)
        next(event for event in reused if event["event_id"] not in cohort)["event_id"] = row["event_id"]
        with self.assertRaises(ValueError):
            builder.validated_october_filing_event_ids(reused, ROOT)

    def test_october_context_does_not_allocate_a_prosecution_or_transparency_file(self):
        payload = builder.build()
        ids = set(payload["october_cohort_control"]["event_ids"])
        rows = [event for event in payload["events"] if event["event_id"] in ids]
        self.assertEqual(len(rows), 6)
        for row in rows:
            self.assertEqual(row["allocation_state"], "UNRESOLVED_PROCEEDING_ALLOCATION")
            self.assertEqual(row["proceeding_mapping_state"], builder.OCTOBER_MAPPING_STATE)
            self.assertTrue(row["unresolved_matter_references"])
            self.assertTrue(set(row["master_ids"]) <= {"NAT-AID-001"})
            self.assertIn(builder.OCTOBER_MAPPING_BOUNDARY["en"], row["does_not_prove"])
            self.assertIn(builder.OCTOBER_MAPPING_BOUNDARY["es"], row["does_not_prove"])
        edges = [edge for edge in payload["event_proceeding_edges"] if edge["event_id"] in ids]
        self.assertEqual({edge["event_id"] for edge in edges}, {row["event_id"] for row in rows if "GC/836/P06" in row["matter_references"]})
        self.assertEqual(len(edges), 2)
        for edge in edges:
            self.assertEqual(edge["master_id"], "NAT-AID-001")
            self.assertEqual(edge["relationship_strength"], "CONTEXT_OR_CITATION")
            self.assertEqual(edge["relationship_type"], "SUBMISSION_REFERENCES_PROCEEDING")
            self.assertEqual(edge["operational_scope"], "OUTSIDE_JUDICIAL_PROCEEDING")

    def test_new_proceeding_allocation_requires_separate_source_review(self):
        original = builder.build_alias_index
        def altered_aliases(*args):
            return {**original(*args), builder.normalise_reference("PD-MAD-FP-20261022-001"): "NAT-FIS-007"}
        with mock.patch.object(builder, "build_alias_index", side_effect=altered_aliases):
            with self.assertRaisesRegex(ValueError, "separately source-controlled mapping"):
                builder.build()

    def test_legacy_projection_objects_and_edges_remain_exact(self):
        # Public projection digests recorded immediately before this bounded
        # extension: 326 event objects, 164 proceeding edges, 84 sequence edges.
        payload = builder.build()
        ids = set(payload["october_cohort_control"]["event_ids"])
        legacy = {
            "events": [event for event in payload["events"] if event["event_id"] not in ids],
            "event_proceeding_edges": [edge for edge in payload["event_proceeding_edges"] if edge["event_id"] not in ids],
            "event_event_edges": payload["event_event_edges"],
            "fiscalia_files": payload["fiscalia_files"],
            "by_master_id": {key: value for key, value in payload["by_master_id"].items() if key != "NAT-AID-001"},
            "priority_chains": payload["priority_chains"],
        }
        expected = {
            "events": "95a70df2dba4d88db23820bf43e4ca0809be5024d5d8c9b9dedb5782fec4d437",
            "event_proceeding_edges": "30e5d34266712cc10fca8879cbb05893992c3f8d40bc5714ab96940f02f9892a",
            "event_event_edges": "167c1a3f4af62af67cb8bdf852c9f6c4d704c42c5eadf9a6e0e282461b350a17",
            "fiscalia_files": "210d88c0631ca4de4fc216c5a63b04c44a8d4520d3ff1200e6d7326615a6f378",
            "by_master_id": "ac431ba901a43f6563ddb1818e562d1ba8e98bd6e6d2583b9076066b38fdcee5",
            "priority_chains": "c174287e6a1b303b91740d3857ed61c5178446043065864898186e09fd170d63",
        }
        for key, value in legacy.items():
            digest = hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
            self.assertEqual(digest, expected[key], key)

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

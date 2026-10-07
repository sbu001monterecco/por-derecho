#!/usr/bin/env python3
"""Synthetic regression tests; no network requests or real acknowledgements."""
import copy
import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

MODULE_PATH = Path(os.environ.get("FTI_MONITOR_TEST_MODULE", Path(__file__).with_name("monitor_fti_meeting_point_asset_transactions.py")))
spec = importlib.util.spec_from_file_location("fti_monitor", MODULE_PATH)
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)


class EmptySourceTests(unittest.TestCase):
    def test_empty_raw_sources_rejected(self):
        for source_type in ("PDF", "RSS", "HTML"):
            with self.subTest(source_type=source_type), self.assertRaisesRegex(ValueError, "EMPTY_SOURCE_RESPONSE"):
                monitor.normalize_source({"source_type": source_type}, b"", "text/html")

    def test_html_without_observable_text_rejected(self):
        for raw in (b"  \n", b"<html><body></body></html>", b"<script>data()</script><style>body{}</style><!-- hidden -->", b"<p>&nbsp;</p>"):
            with self.subTest(raw=raw), self.assertRaisesRegex(ValueError, "EMPTY_NORMALIZED_HTML_SOURCE"):
                monitor.normalize_source({"source_type": "HTML"}, raw, "text/html")

    def test_rss_without_observable_entries_rejected(self):
        for raw in (b"<rss><channel/></rss>", b"<feed xmlns='http://www.w3.org/2005/Atom'/>", b"<rss><channel><item/></channel></rss>", b"<rss><channel><item><title> </title></item></channel></rss>"):
            with self.subTest(raw=raw), self.assertRaisesRegex(ValueError, "EMPTY_NORMALIZED_RSS_SOURCE"):
                monitor.normalize_source({"source_type": "RSS"}, raw, "application/xml")

    def test_nonempty_html_preserves_normalization(self):
        self.assertEqual(monitor.normalize_source({"source_type": "HTML"}, b"<p>Source &amp; record</p>", "text/html"), (b"Source & record", "HTML_VISIBLE_TEXT_SHA256"))

    def test_nonempty_rss_preserves_normalization(self):
        self.assertEqual(monitor.normalize_source({"source_type": "RSS"}, b"<rss><channel><item><title>Source record</title></item></channel></rss>", "application/xml"), (b"title=Source record", "RSS_ENTRY_SET_SHA256"))

    def test_nonempty_pdf_preserves_binary(self):
        self.assertEqual(monitor.normalize_source({"source_type": "PDF"}, b"%PDF-synthetic", "application/pdf"), (b"%PDF-synthetic", "BINARY_SHA256"))

    def test_failure_retains_previous_baseline_and_pending_queue(self):
        source = {"source_id": "SYNTHETIC-001", "url": "https://example.invalid/", "priority": "P1_OFFICIAL", "access_lane": "AUTOMATED_SAFE", "source_type": "HTML", "required": True, "change_review_policy": "ANY_CHANGE", "enabled": True}
        previous = {"acknowledged_fingerprint": "a" * 64, "last_observed_fingerprint": "b" * 64}
        pending = [{"pending_id": "SYNTHETIC-PENDING", "observed_fingerprint": "b" * 64}]
        before = copy.deepcopy((previous, pending))
        with patch.object(monitor, "fetch", return_value=(b"<script>only()</script>", {"content_type": "text/html", "etag": None, "last_modified": None})):
            report, next_state, next_pending = monitor.process_source(source, previous, pending, {}, {}, [], "2026-10-03T00:00:00Z", 1, 1000)
        self.assertEqual(report["change_state"], "FETCH_ERROR")
        self.assertEqual(report["acknowledged_fingerprint_retained"], "a" * 64)
        self.assertTrue(report["review_required"])
        self.assertIsNone(next_state)
        self.assertEqual(next_pending, before[1])
        self.assertEqual((previous, pending), before)

    def test_failed_first_observation_cannot_create_baseline(self):
        source = {"source_id": "SYNTHETIC-001", "url": "https://example.invalid/", "priority": "P1_OFFICIAL", "access_lane": "AUTOMATED_SAFE", "source_type": "HTML", "required": True, "change_review_policy": "ANY_CHANGE", "enabled": True}
        with patch.object(monitor, "fetch", return_value=(b"", {"content_type": "text/html", "etag": None, "last_modified": None})):
            report, next_state, queue = monitor.process_source(source, {}, [], {}, {}, [], "2026-10-03T00:00:00Z", 1, 1000)
        self.assertEqual(report["change_state"], "FETCH_ERROR")
        self.assertIsNone(next_state)
        self.assertEqual(queue, [])


class StatusDimensionTests(unittest.TestCase):
    def test_successful_retrieval_does_not_close_pending_review(self):
        state = monitor.status_dimensions({"fetch_errors": 0, "pending_changes": 2}, [], True)
        self.assertEqual(state, {"execution": "PASS", "source_review": "REVIEW_REQUIRED", "continuity": "PRIOR_STATE_AVAILABLE", "overall_rag": "RED"})

    def test_required_source_failure_is_red(self):
        self.assertEqual(monitor.status_dimensions({"fetch_errors": 1, "pending_changes": 0}, ["SYNTHETIC-001"], True)["overall_rag"], "RED")

    def test_optional_source_gap_remains_amber(self):
        state = monitor.status_dimensions({"fetch_errors": 1, "pending_changes": 0}, [], True)
        self.assertEqual(state["execution"], "DEGRADED")
        self.assertEqual(state["overall_rag"], "AMBER")

    def test_first_baseline_is_not_complete_continuity(self):
        self.assertEqual(monitor.status_dimensions({"fetch_errors": 0, "pending_changes": 0}, [], False)["overall_rag"], "AMBER")

    def test_verified_empty_queue_can_be_green(self):
        self.assertEqual(monitor.status_dimensions({"fetch_errors": 0, "pending_changes": 0}, [], True)["overall_rag"], "GREEN")


if __name__ == "__main__":
    unittest.main(verbosity=2)

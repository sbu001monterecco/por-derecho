#!/usr/bin/env python3
"""Deterministic regression tests for operational review-date handling."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "scripts" / "validate_operational_items.py"
SPEC = importlib.util.spec_from_file_location("validate_operational_items", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"unable to load {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def item(item_id: str, review_by: str, *, status: str = "OPEN") -> dict:
    record = {
        "id": item_id,
        "title": f"Test item {item_id}",
        "severity": "P1",
        "status": status,
        "owner": "test-owner",
        "last_verified_at": "2026-08-20",
        "review_by": review_by,
        "tracking": {"repository_file": "operations/open-operational-items.json"},
        "blocks": {
            "publication": False,
            "repository_hardening": False,
            "security_assurance": False,
            "deletion_safety": False,
        },
        "evidence": ["Synthetic deterministic test evidence."],
        "next_action": "Run the deterministic test.",
        "closure_test": "Close only when the deterministic test passes.",
    }
    if status == "CLOSED":
        record["closure_evidence"] = ["Synthetic closure evidence."]
    if status == "BLOCKED":
        record["blocks"]["publication"] = True
    return record


def registry() -> dict:
    return {
        "registry_version": 1,
        "as_of": "2026-08-24",
        "owner": "Por Derecho test fixture",
        "items": [
            item("OPS-2026-101", "2026-08-27"),
            item("OPS-2026-102", "2026-08-27"),
            item("OPS-2026-103", "2026-08-27"),
            item("OPS-2026-104", "2026-08-27", status="MONITORING"),
            item("OPS-2026-105", "2026-08-29", status="BLOCKED"),
        ],
    }


class OperationalReviewPolicyTests(unittest.TestCase):
    def validate(self, data: dict, today: date):
        return VALIDATOR.validate_registry(data, today=today)

    def test_review_date_is_current_through_the_due_day(self) -> None:
        errors, warnings, metrics = self.validate(registry(), date(2026, 8, 27))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(metrics["review_due"], 0)

    def test_four_reviews_become_advisory_on_august_28(self) -> None:
        errors, warnings, metrics = self.validate(registry(), date(2026, 8, 28))
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 4)
        self.assertEqual(metrics["review_due"], 4)

    def test_all_five_reviews_are_advisory_on_august_30(self) -> None:
        errors, warnings, metrics = self.validate(registry(), date(2026, 8, 30))
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 5)
        self.assertEqual(metrics["review_due"], 5)

    def test_expired_closed_item_does_not_warn(self) -> None:
        data = registry()
        data["items"] = [item("OPS-2026-106", "2026-08-21", status="CLOSED")]
        errors, warnings, _ = self.validate(data, date(2026, 8, 30))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_malformed_date_remains_a_hard_failure(self) -> None:
        data = registry()
        data["items"][0]["review_by"] = "not-a-date"
        errors, warnings, _ = self.validate(data, date(2026, 8, 30))
        self.assertTrue(any("invalid ISO date" in error for error in errors))
        self.assertEqual(len(warnings), 4)

    def test_review_before_last_verification_remains_a_hard_failure(self) -> None:
        data = registry()
        data["items"][0]["review_by"] = "2026-08-19"
        errors, warnings, _ = self.validate(data, date(2026, 8, 30))
        self.assertTrue(any("review_by precedes last_verified_at" in error for error in errors))
        self.assertEqual(len(warnings), 5)

    def test_false_closure_and_unscoped_block_remain_hard_failures(self) -> None:
        closed = item("OPS-2026-106", "2026-08-21", status="CLOSED")
        closed.pop("closure_evidence")
        blocked = item("OPS-2026-107", "2026-08-29", status="BLOCKED")
        blocked["blocks"] = {key: False for key in VALIDATOR.BLOCK_KEYS}
        data = registry()
        data["items"] = [closed, blocked]
        errors, _, _ = self.validate(data, date(2026, 8, 30))
        self.assertTrue(any("CLOSED requires closure_evidence" in error for error in errors))
        self.assertTrue(any("BLOCKED item must declare" in error for error in errors))

    def test_current_registry_is_structurally_valid_even_when_reviews_are_due(self) -> None:
        current = json.loads(
            (ROOT / "operations" / "open-operational-items.json").read_text(encoding="utf-8")
        )
        errors, warnings, metrics = self.validate(current, date(2099, 1, 1))
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), metrics["active"])

    def test_top_level_registry_must_be_an_object(self) -> None:
        errors, warnings, metrics = VALIDATOR.validate_registry([], today=date(2026, 8, 30))
        self.assertEqual(errors, ["registry root must be an object"])
        self.assertEqual(warnings, [])
        self.assertEqual(metrics["items"], 0)

    def test_reporter_exits_successfully_with_five_prominent_warnings(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = VALIDATOR.report_validation(registry(), today=date(2026, 8, 30))
        rendered = output.getvalue()
        self.assertEqual(status, 0)
        self.assertIn("PASS WITH WARNINGS", rendered)
        self.assertEqual(rendered.count("WARNING:"), 5)

    def test_non_object_item_is_a_hard_failure_not_an_exception(self) -> None:
        data = registry()
        data["items"].append("not-an-object")
        errors, _, metrics = self.validate(data, date(2026, 8, 30))
        self.assertTrue(any("item must be an object" in error for error in errors))
        self.assertEqual(metrics["items"], 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)

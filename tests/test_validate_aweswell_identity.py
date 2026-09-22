#!/usr/bin/env python3
"""Focused regression tests for the AWESWELL LIMITED identity guard."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_aweswell_identity.py"
SPEC = importlib.util.spec_from_file_location("validate_aweswell_identity", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class IdentityGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rule = MODULE.load_json(MODULE.RULE)
        cls.pattern = MODULE.forbidden_pattern(cls.rule)

    def test_canonical_identity_passes(self) -> None:
        errors = MODULE.scan_text(
            "AWESWELL LIMITED (company number 07716847)",
            "draft.txt",
            self.pattern,
        )
        self.assertEqual(errors, [])

    def test_forbidden_current_assertion_fails(self) -> None:
        errors = MODULE.scan_text(
            "The claimant is " + "Os" + "well Limited.",
            "draft.txt",
            self.pattern,
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("unclassified forbidden identity variant", errors[0])

    def test_unrelated_spanish_entity_is_not_rewritten(self) -> None:
        errors = MODULE.scan_text(
            "OSWELL 426 S.L. is a distinct Spanish entity.",
            "source.txt",
            self.pattern,
        )
        self.assertEqual(errors, [])

    def test_partial_unrelated_entity_name_does_not_bypass_guard(self) -> None:
        errors = MODULE.scan_text(
            "This was an " + "OS" + "WELL 426 payment.",
            "draft.txt",
            self.pattern,
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("unclassified forbidden identity variant", errors[0])

    def test_exception_is_line_and_literal_bounded(self) -> None:
        exceptions = [{
            "path": "source.md",
            "start_line": 2,
            "end_line": 2,
            "allowed_literals": ["Aws" + "well"],
            "expected_matches": 1,
            "label": "source literal",
        }]
        usage: dict[int, int] = {}
        accepted = MODULE.scan_text(
            "header\nAws" + "well\nfooter",
            "source.md",
            self.pattern,
            exceptions,
            usage,
        )
        self.assertEqual(accepted, [])
        self.assertEqual(usage, {0: 1})

        rejected = MODULE.scan_text(
            "Aws" + "well\nheader\nfooter",
            "source.md",
            self.pattern,
            exceptions,
            {},
        )
        self.assertEqual(len(rejected), 1)


if __name__ == "__main__":
    unittest.main()

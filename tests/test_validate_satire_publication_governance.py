#!/usr/bin/env python3
"""Focused negative tests for the satire person-display gate."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_satire_publication_governance.py"
SPEC = importlib.util.spec_from_file_location("satire_validator", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def base_person() -> dict:
    return {
        "display_name": "Example Person",
        "naming_form": "FULL_NAME_STRONGLY_VERIFIED_EXCEPTION",
        "identity_state": "STRONGLY_VERIFIED_EXCEPTION",
        "caepr_id": None,
        "source_refs": ["SRC-EXAMPLE-1"],
        "direct_public_sources": ["https://example.invalid/professional-profile"],
        "full_name_necessity": "The exact name is necessary to distinguish the sourced professional role.",
        "no_resolved_caepr_record_available": True,
        "factual_role": {
            "label": "Source-described professional",
            "date_or_period": "2026-09-01",
            "source_refs": ["SRC-EXAMPLE-1"],
        },
        "affiliation": {"state": "NOT_APPLICABLE"},
        "satirical_function": {"state": "QUESTION", "label": "Who held the sourced role?"},
    }


class NamedPersonGateTests(unittest.TestCase):
    canonical = {"PD-SP-P-9999": "Canonical Person"}

    def validate(self, person: dict) -> list[str]:
        return MODULE.validate_named_person(person, self.canonical, "fixture")

    def test_valid_strongly_verified_exception(self) -> None:
        self.assertEqual(self.validate(base_person()), [])

    def test_pending_identity_cannot_use_known_full_canonical_name(self) -> None:
        person = base_person()
        person.update(
            {
                "display_name": "Canonical Person",
                "naming_form": "EXACT_SOURCE_SHORT_FORM",
                "identity_state": "CARET_PENDING",
                "caepr_id": None,
            }
        )
        self.assertTrue(any("known full canonical name" in error for error in self.validate(person)))

    def test_full_canonical_name_requires_matching_caret_id(self) -> None:
        person = base_person()
        person.update(
            {
                "display_name": "Canonical Person",
                "naming_form": "FULL_CANONICAL_CARET_CONFIRMED",
                "identity_state": "CARET_CONFIRMED",
                "caepr_id": "PD-SP-P-WRONG",
            }
        )
        self.assertTrue(any("immutable CAEPR" in error for error in self.validate(person)))

    def test_current_affiliation_requires_date_and_source(self) -> None:
        person = base_person()
        person["affiliation"] = {"state": "CURRENT_VERIFIED_ON_DATE"}
        errors = self.validate(person)
        self.assertTrue(any("verified_on" in error for error in errors))
        self.assertTrue(any("dated source_refs" in error for error in errors))

    def test_strong_exception_requires_necessity_and_direct_source(self) -> None:
        person = base_person()
        person.pop("direct_public_sources")
        person["full_name_necessity"] = "because"
        errors = self.validate(person)
        self.assertTrue(any("direct_public_sources" in error for error in errors))
        self.assertTrue(any("necessity rationale" in error for error in errors))

    def test_image_lock_cannot_be_used_as_caepr_state(self) -> None:
        person = base_person()
        person["identity_state"] = "LOCKED_CANONICAL_REPOSITORY_ASSET"
        self.assertTrue(any("matching state" in error for error in self.validate(person)))


if __name__ == "__main__":
    unittest.main()

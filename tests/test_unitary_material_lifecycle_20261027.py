"""Unitary September-history / October-current source and live boundary tests."""
import copy
import json
from pathlib import Path
import unittest

from scripts.unitary_material_lifecycle_20261027 import valid_material_stage

ROOT = Path(__file__).resolve().parents[1]


class MaterialLifecycleStageTests(unittest.TestCase):
    def setUp(self):
        state = json.loads((ROOT / "ops/CURRENT_UNITARY_STATE.json").read_text())
        self.material = state["material_updates"]
        self.control = json.loads(
            (ROOT / "assets/data/institutional-communications-20261025.json").read_text())
        self.expected_date = "2026-10-25"

    def accepts(self, value, source=None):
        return valid_material_stage(
            value, self.expected_date, self.control,
            self.material if source is None else source)

    def test_actual_current_and_history_are_independently_authenticated(self):
        self.assertTrue(self.accepts(copy.deepcopy(self.material)))
        self.assertEqual(self.material["pending_publication"]["control_id"],
                         "PD-MADRID-CTBG-REGISTERED-20261025")
        self.assertEqual(
            self.material["pending_publication_history"][0]["control_id"],
            "PD-CUATRECASAS-ETJ-DP748-20260918-01")

    def test_misplacing_old_record_as_current_fails(self):
        v = copy.deepcopy(self.material)
        v["pending_publication"] = copy.deepcopy(v["pending_publication_history"][0])
        self.assertFalse(self.accepts(v, v))

    def test_missing_or_duplicate_historical_record_fails(self):
        for bad in ([], self.material["pending_publication_history"] * 2):
            v = copy.deepcopy(self.material)
            v["pending_publication_history"] = bad
            self.assertFalse(self.accepts(v, v))

    def test_altered_historical_merge_or_status_fails(self):
        for field, replacement in (
            ("merge_sha", "0" * 40), ("merged_to", "other"),
            ("state", "LIVE_VERIFIED"), ("material_date", "2026-10-25")):
            v = copy.deepcopy(self.material)
            v["pending_publication_history"][0][field] = replacement
            self.assertFalse(self.accepts(v, v))

    def test_october_source_and_current_status_cannot_be_promoted(self):
        for field, replacement in (
            ("control_id", "PD-CUATRECASAS-ETJ-DP748-20260918-01"),
            ("state", "LIVE_VERIFIED"), ("material_date", "2026-09-18"),
            ("source_input", "private/secret.pdf")):
            v = copy.deepcopy(self.material)
            v["pending_publication"][field] = replacement
            self.assertFalse(self.accepts(v, v))

    def test_prepared_state_cannot_claim_merged_branch(self):
        v = copy.deepcopy(self.material)
        v["pending_publication"]["merge_sha"] = "0" * 40
        self.assertFalse(self.accepts(v, v))

    def test_live_manifest_must_equal_repository_stage(self):
        v = copy.deepcopy(self.material)
        v["pending_publication"]["state"] = "PREPARED_PENDING_MERGE"
        self.assertFalse(self.accepts(v))
        self.assertTrue(self.accepts(v, v))

    def test_false_complete_live_state_fails(self):
        v = copy.deepcopy(self.material)
        v["last_live_verified_material_date"] = self.expected_date
        self.assertFalse(self.accepts(v, v))

    def test_current_source_control_or_route_loss_fails(self):
        v = copy.deepcopy(self.material)
        v["pending_publication"]["routes"].remove("/en/updates/")
        self.assertFalse(self.accepts(v, v))
        self.assertFalse(valid_material_stage(
            self.material, self.expected_date, {"control_id": "UNVERIFIED"},
            self.material))


if __name__ == "__main__":
    unittest.main()

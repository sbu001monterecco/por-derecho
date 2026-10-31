"""Current canonical counts must not rewrite historical publication evidence."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_post7june_2022_deliberate_exclusion as control


class CurrentRegistryControlTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = self.root / "assets/data"
        self.data.mkdir(parents=True)
        self.workflow = self.root / "live.yml"
        self.index_path = self.data / "matter-identity-registry-v1.json"
        self.part_path = self.data / "people.json"
        self.index = {
            "control_date": "2026-10-31",
            "counts": {"total": 2, "PERSON": 2, "ORGANISATION": 0,
                       "STRUCTURE": 0, "INSTITUTION": 0, "PROCEEDING": 0},
            "parts": [{"path": "people.json", "type": "PERSON", "count": 2}],
        }
        self.part = {"records": [
            {"id": "PD-SP-P-0001", "type": "PERSON"},
            {"id": "PD-SP-P-0002", "type": "PERSON"},
        ]}
        self.write_registry()
        counts = self.index["counts"]
        self.workflow.write_text("\n".join([
            *(f"'{kind}': {count}" for kind, count in counts.items()),
            'data-static-registry-counts="2-2-0-0-0-0"',
            "identity_registry_parity'] == 204",
            "'identity_source_current': 2",
            "'specialist_historical_identity_snapshot': 204",
        ]), encoding="utf-8")
        self.addCleanup(patch.stopall)
        patch.object(control, "ROOT", self.root).start()
        patch.object(control, "ALBERTO_LIVE_WORKFLOW", self.workflow).start()

    def write_registry(self):
        self.index_path.write_text(json.dumps(self.index), encoding="utf-8")
        self.part_path.write_text(json.dumps(self.part), encoding="utf-8")

    def test_valid_current_counts_are_not_frozen_to_a_past_snapshot(self):
        control.validate_current_registry_control()

    def test_index_count_disagreement_with_shards_fails(self):
        self.index["counts"]["total"] = 3
        self.write_registry()
        with self.assertRaisesRegex(ValueError, "counts disagree"):
            control.validate_current_registry_control()

    def test_duplicate_identity_fails(self):
        self.part["records"][1]["id"] = "PD-SP-P-0001"
        self.write_registry()
        with self.assertRaisesRegex(ValueError, "Duplicate/invalid identity"):
            control.validate_current_registry_control()

    def test_stale_live_workflow_counts_fail(self):
        text = self.workflow.read_text(encoding="utf-8")
        self.workflow.write_text(text.replace("2-2-0-0-0-0", "1-1-0-0-0-0"), encoding="utf-8")
        with self.assertRaisesRegex(AssertionError, "data-static-registry-counts"):
            control.validate_current_registry_control()

    def test_historical_snapshot_remains_fixed(self):
        for marker in ("identity_registry_parity'] == 204", "'specialist_historical_identity_snapshot': 204"):
            with self.subTest(marker=marker):
                original = self.workflow.read_text(encoding="utf-8")
                self.workflow.write_text(original.replace(marker, marker.replace("204", "2")), encoding="utf-8")
                with self.assertRaisesRegex(AssertionError, "missing marker"):
                    control.validate_current_registry_control()
                self.workflow.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts/validate_actor_behaviour_modus_operandi.py"
REGISTRY_PATH = ROOT / "assets/data/actor-behaviour-modus-operandi-registry-v1.json"

spec = importlib.util.spec_from_file_location("actor_mo_validator", VALIDATOR_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def _data() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


class ActorBehaviourModusOperandiTests(unittest.TestCase):
    def test_registry_passes_fail_closed_validator(self) -> None:
        self.assertEqual(module.validate(_data()), [])

    def test_machine_ids_are_namespaced_from_source_markers(self) -> None:
        data = _data()
        fmmm = data["actors"]["FMMM"]["markers"][0]
        self.assertEqual(fmmm["source_marker"], "FMMM-01")
        self.assertEqual(fmmm["machine_id"], "MO-FMMM-01")
        all_ids = [
            marker["machine_id"]
            for actor in data["actors"].values()
            for marker in actor["markers"]
        ]
        self.assertEqual(len(all_ids), len(set(all_ids)))

    def test_recurrence_gate_remains_evidence_led(self) -> None:
        recurrence = _data()["recurrence"]
        self.assertEqual(recurrence["minimum_shared_operational_markers"], 3)
        self.assertTrue(recurrence["requires_independent_actor_attribution"])
        self.assertTrue(recurrence["requires_primary_or_contemporaneous_source"])
        self.assertTrue(recurrence["requires_contrary_evidence_and_legitimate_alternatives"])
        self.assertTrue(recurrence["separates_proposal_preparation_implementation_result"])
        self.assertTrue(recurrence["requires_explicit_not_a_finding_label"])

    def test_actor_specific_counts_and_ids_are_locked(self) -> None:
        actors = _data()["actors"]
        self.assertEqual(actors["FMMM"]["person_id"], "PD-SP-P-0009")
        self.assertEqual(actors["JDAM"]["person_id"], "PD-SP-P-0011")
        self.assertEqual(actors["LPAM"]["person_id"], "PD-SP-P-0012")
        self.assertEqual(len(actors["FMMM"]["markers"]), 8)
        self.assertEqual(len(actors["JDAM"]["markers"]), 10)
        self.assertEqual(len(actors["LPAM"]["markers"]), 8)


if __name__ == "__main__":
    unittest.main()

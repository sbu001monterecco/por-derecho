"""Synthetic regression tests; these are not vault restoration tests."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("vault_benchmark_validator", ROOT / "recovery_tools/validate_digital_memory_vault_benchmark.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class VaultBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.state = json.loads((ROOT / "ops/digital-memory-vault/STATE.json").read_text())

    def test_committed_state_is_valid_and_incomplete(self):
        self.assertEqual(MODULE.validate(self.state), [])
        self.assertIs(self.state["full"], False)
        self.assertIsNone(self.state["required_native_occurrences"])

    def test_cannot_claim_full_with_open_denominator(self):
        self.state["full"] = True
        self.assertTrue(MODULE.validate(self.state))

    def test_pass_needs_receipt(self):
        self.state["gates"]["PRIVATE_PROTECTION"] = "PASS"
        self.assertTrue(MODULE.validate(self.state))

    def test_court_gate_is_separate(self):
        self.state["official_court_file_complete"] = True
        self.assertTrue(MODULE.validate(self.state))

    def test_unknown_is_not_an_implicit_zero(self):
        self.assertIsNone(self.state["unresolved_required_gaps"])
        self.assertIsNone(self.state["verified_native_occurrences"])

    def test_negative_counter_rejected(self):
        self.state["required_native_occurrences"] = -1
        self.assertTrue(MODULE.validate(self.state))

    def test_missing_gate_rejected(self):
        del self.state["gates"]["INDEPENDENT_RESTORE"]
        self.assertTrue(MODULE.validate(self.state))

    def test_boolean_counter_rejected(self):
        self.state["required_native_occurrences"] = True
        self.assertTrue(MODULE.validate(self.state))

    def test_synthetic_complete_requires_all_recovery_conditions(self):
        d = copy.deepcopy(self.state)
        d.update(full=True, scope_version="SYNTHETIC_TEST_ONLY", whole_scope_denominator_closed=True,
                 required_native_occurrences=1, verified_native_occurrences=1, unresolved_required_gaps=0)
        for gate in MODULE.GATES:
            if gate != "OFFICIAL_DOCKET":
                d["gates"][gate] = "PASS"
                d["receipt_ids"][gate] = "SYNTHETIC_NOT_REAL_RECEIPT"
        self.assertEqual(MODULE.validate(d), [])
        d["unresolved_required_gaps"] = 1
        self.assertTrue(MODULE.validate(d))


if __name__ == "__main__":
    unittest.main()

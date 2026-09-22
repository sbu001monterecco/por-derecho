import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_evidence_control_plane as ecp  # noqa: E402

class EvidenceControlPlaneTests(unittest.TestCase):
    def test_current_contract_passes(self):
        stats = ecp.validate_contract(ROOT)
        self.assertEqual(stats["schema_draft"], "2020-12")
        self.assertGreaterEqual(stats["axes"], 10)
        self.assertEqual(stats["example_records_validated"], 1)

    def test_assertion_without_source_is_rejected_by_schema(self):
        schema = json.loads(
            (ROOT / "schemas" / "por-derecho-evidence-control-plane-v1.schema.json")
            .read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(schema)
        bad = {
            "id": "AST-BAD-001",
            "object_type": "ASSERTION",
            "event_time": "2018-01-01",
            "knowledge_time": "2026-09-22",
            "status_axes": {"ASSERTION_STATUS": "UNTRIAGED"},
            "provenance": {
                "source_system": "TEST",
                "custody_state": "TEST"
            },
            "contrary_evidence": [],
            "what_it_does_not_establish": ["test boundary"]
        }
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(bad)

    def test_taxonomy_drift_reports_missing_and_extra_values(self):
        with self.assertRaisesRegex(ValueError, r"missing=.*PARITY_GAP.*extra=.*NOT_A_REAL_GAP"):
            ecp.require_exact_set(
                "gap taxonomy",
                (ecp.REQUIRED_GAPS - {"PARITY_GAP"}) | {"NOT_A_REAL_GAP"},
                ecp.REQUIRED_GAPS,
            )

if __name__ == "__main__":
    unittest.main()

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_human_ai_narrative.py"

spec = importlib.util.spec_from_file_location("human_ai_narrative", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class HumanAINarrativeProtocolTests(unittest.TestCase):
    def test_current_repository_passes(self):
        result = module.validate()
        self.assertEqual(result["status"], "PASS", result["errors"])
        self.assertEqual(result["errors"], [])

    def test_control_id_is_stable(self):
        self.assertEqual(module.CONTROL_ID, "PD-GOV-HUMAN-AI-20260924-01")


if __name__ == "__main__":
    unittest.main()

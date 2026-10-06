import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class CorporateBrainAPlusTests(unittest.TestCase):
    def test_validator(self):
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_corporate_brain_a_plus.py")],
            cwd=ROOT,
            check=True,
        )

    def test_no_private_locator_fields_in_public_status(self):
        data = json.loads((ROOT / "ops" / "corporate-brain" / "A_PLUS_DEPLOYMENT_STATUS_20260929.json").read_text(encoding="utf-8"))
        raw = json.dumps(data).lower()
        for forbidden in ("drive.google.com/drive/folders/", "@gmail.com", "@monterecco.com", "message_id", "thread_id"):
            self.assertNotIn(forbidden, raw)

if __name__ == "__main__":
    unittest.main()

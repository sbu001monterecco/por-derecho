import json, subprocess, sys
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]

class NamedPersonVisualIntegrityTests(unittest.TestCase):
    def test_platform_validator_passes(self):
        r=subprocess.run([sys.executable,str(ROOT/"scripts/validate_named_person_visual_control.py")],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+"\n"+r.stderr)

    def test_rejected_generations_are_quarantined(self):
        p=json.loads((ROOT/"assets/data/named-person-visual-control-v1.json").read_text())
        self.assertEqual(len(p["rejected_generation_ids"]),2)
        self.assertFalse(p["generative_named_person_faces"])
        self.assertEqual(p["missing_asset_action"],"HALT_AND_REPORT")

    def test_jtp_pages_do_not_contain_known_hallucinated_material(self):
        p=json.loads((ROOT/"assets/data/named-person-visual-control-v1.json").read_text())
        for rel in ("en/estate-payment-counsel-independence/index.html","es/pago-masa-independencia-defensa/index.html"):
            text=(ROOT/rel).read_text()
            for marker in p["banned_jtp_hallucination_markers"]:
                self.assertNotIn(marker,text)

if __name__=="__main__":
    unittest.main()

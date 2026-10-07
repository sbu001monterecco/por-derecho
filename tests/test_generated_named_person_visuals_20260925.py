import subprocess,sys
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class GeneratedNamedPersonAuditTests(unittest.TestCase):
    def test_sidecar_audit_passes(self):
        r=subprocess.run([sys.executable,str(ROOT/"scripts/audit_generated_named_person_visuals.py")],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+"\n"+r.stderr)
        self.assertIn("AUDIT: PASS",r.stdout)
if __name__=="__main__": unittest.main()

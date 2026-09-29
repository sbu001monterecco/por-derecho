import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / "corporate_brain" / "runtime" / "preflight.py"
ENV_EXAMPLE = ROOT / "corporate_brain" / "runtime" / ".env.example"


class CorporateBrainKeyReadinessTests(unittest.TestCase):
    def test_env_template_contains_no_secret(self):
        text = ENV_EXAMPLE.read_text(encoding="utf-8")
        self.assertIn("OPENAI_API_KEY=", text)
        for line in text.splitlines():
            if line.startswith("OPENAI_API_KEY="):
                self.assertEqual(line, "OPENAI_API_KEY=")

    def test_preflight_is_key_ready_without_secret(self):
        env = os.environ.copy()
        env.pop("OPENAI_API_KEY", None)
        proc = subprocess.run(
            [sys.executable, str(PREFLIGHT)],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("CORPORATE_BRAIN_RUNTIME_KEY_READY", proc.stdout)

    def test_required_key_fails_closed_and_never_prints_fake_secret(self):
        env = os.environ.copy()
        env.pop("OPENAI_API_KEY", None)
        proc = subprocess.run(
            [sys.executable, str(PREFLIGHT), "--require-key"],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("OPENAI_API_KEY not installed", proc.stdout)

    def test_key_presence_passes_without_echoing_secret(self):
        secret = "sk-test-secret-must-never-appear"
        env = os.environ.copy()
        env["OPENAI_API_KEY"] = secret
        proc = subprocess.run(
            [sys.executable, str(PREFLIGHT), "--require-key"],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("CORPORATE_BRAIN_RUNTIME_PREFLIGHT_GREEN", proc.stdout)
        self.assertNotIn(secret, proc.stdout)
        self.assertNotIn(secret, proc.stderr)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "scripts" / "audit_github_backend_capabilities_20260917.py"

spec = importlib.util.spec_from_file_location("pd_backend_capability_audit", AUDIT_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class GitHubBackendHardeningTests(unittest.TestCase):
    def test_audit_script_exists(self):
        self.assertTrue(AUDIT_PATH.is_file())

    def test_repository_capability_audit_passes(self):
        report = mod.audit()
        self.assertEqual(report["status"], "PASS", report["failures"])
        caps = report["repository_capabilities"]
        self.assertEqual(caps["controls_present"], caps["controls_required"])
        self.assertEqual(caps["coverage_percent"], 100.0)

    def test_platform_native_gaps_are_not_hidden(self):
        report = mod.audit()
        gaps = report["platform_native_gaps_excluded_from_repository_denominator"]
        self.assertGreaterEqual(len(gaps), 5)
        self.assertIn("100% repository-control coverage is not 100% GitLab platform parity.", report["truth_boundary"])

    def test_critical_categories_are_present(self):
        categories = set(mod.CAPABILITIES)
        self.assertTrue({
            "registry",
            "evidence_intelligence",
            "reasoning_frameworks",
            "release_and_preservation",
            "agent_and_continuity_governance",
        }.issubset(categories))


if __name__ == "__main__":
    unittest.main()

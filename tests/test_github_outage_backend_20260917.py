#!/usr/bin/env python3

import importlib.util
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "outage-backend-parity.yml"
CLASSIFIER_PATH = ROOT / "scripts" / "classify_public_impact_shadow_20260917.py"
PARITY = ROOT / "ops" / "continuity" / "GITHUB_OPERATIONAL_BACKEND_PARITY_20260917.json"
RECOVERY = ROOT / "ops" / "continuity" / "GITHUB_OPERATIONAL_BACKEND_RECOVERY_20260917.md"
COPILOT = ROOT / ".github" / "copilot-instructions.md"
DUO_PROTOCOL = ROOT / "ops" / "duo" / "DUO_ORCHESTRATION_PROTOCOL_20260917.md"
REGISTRY = ROOT / "assets" / "data" / "matter-identity-registry-v1.json"

spec = importlib.util.spec_from_file_location("pd_public_impact_shadow", CLASSIFIER_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class OutageBackendParityTests(unittest.TestCase):
    def test_required_recovery_controls_exist(self):
        for path in (WORKFLOW_PATH, CLASSIFIER_PATH, PARITY, RECOVERY, COPILOT, DUO_PROTOCOL, REGISTRY):
            self.assertTrue(path.is_file(), path)

    def test_required_outage_context_runs_on_every_pull_request(self):
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        pull_request_block = workflow.split("  pull_request:", 1)[1].split("\n\npermissions:", 1)[0]
        self.assertNotIn("paths:", pull_request_block)
        self.assertIn("name: Outage backend parity / validate", workflow)

    def test_parity_manifest_anchors_are_exact(self):
        data = json.loads(PARITY.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "ACTIVE_OUTAGE_CONTINUITY")
        self.assertEqual(data["github_base_sha"], "da67c0c2731c550b0866dad1f679c437f2b612f9")
        self.assertEqual(data["last_verified_gitlab_main_sha"], "7d086d098676eecc2c1647ed09b348d8dc0bdc69")
        self.assertEqual(data["outage_working_branch"], "continuity/gitlab-block-working-lane-20260917")

    def test_registry_denominator_matches_recovery_manifest(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        parity = json.loads(PARITY.read_text(encoding="utf-8"))
        identity = next(x for x in parity["layers"] if x["id"] == "IDENTITY_REGISTRY")
        self.assertEqual(registry["counts"]["total"], identity["known_count"])
        self.assertEqual(registry["counts"]["total"], 379)

    def test_classifier_fails_closed_for_public_runtime(self):
        self.assertEqual(mod.classify(["assets/site.js"]).result, "YES_OR_UNKNOWN")
        self.assertEqual(mod.classify(["en/index.html"]).result, "YES_OR_UNKNOWN")
        self.assertEqual(mod.classify(["publication-manifests/x.json"]).result, "YES_OR_UNKNOWN")
        self.assertEqual(mod.classify(["robots.txt"]).result, "YES_OR_UNKNOWN")

    def test_classifier_fails_closed_for_workflow_changes(self):
        result = mod.classify([".github/workflows/release.yml"])
        self.assertEqual(result.result, "YES_OR_UNKNOWN")
        self.assertTrue(any(x.startswith("release_sensitive:") for x in result.reasons))

    def test_classifier_allows_only_narrow_non_runtime_set(self):
        result = mod.classify([
            "scripts/tool.py",
            "tests/test_tool.py",
            ".github/copilot-instructions.md",
        ])
        self.assertEqual(result.result, "NO")

    def test_classifier_unknown_path_fails_closed(self):
        self.assertEqual(mod.classify(["ops/new-control.json"]).result, "YES_OR_UNKNOWN")

    def test_classifier_empty_is_unknown(self):
        self.assertEqual(mod.classify([]).result, "UNKNOWN")

    def test_exact_gitlab_native_items_remain_pending_not_fabricated(self):
        data = json.loads(PARITY.read_text(encoding="utf-8"))
        layers = {x["id"]: x for x in data["layers"]}
        self.assertIn("PENDING", layers["GITLAB_DUO_EXECUTION_CONFIG"]["status"])
        self.assertIn("UNRECOVERED", layers["GITLAB_NATIVE_METADATA"]["status"])
        self.assertIn("PENDING", layers["RELEASE_BUNDLE_GUARD"]["status"])

    def test_agent_instructions_do_not_claim_duo_parity(self):
        text = COPILOT.read_text(encoding="utf-8")
        self.assertIn("does not assert", text.lower())
        self.assertIn("GitLab Duo Developer", text)
        self.assertIn("continuity/gitlab-block-working-lane-20260917", text)


if __name__ == "__main__":
    unittest.main()

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_control_plane_topology.py"
SPEC = importlib.util.spec_from_file_location("topology_audit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class ControlPlaneTopologyAuditTests(unittest.TestCase):
    def test_github_counts_reuse_pinning_and_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "a.yml").write_text(
                "on:\n  pull_request:\n  push:\n    branches: [main]\n"
                "jobs:\n  a:\n    steps:\n      - uses: actions/checkout@" + "a" * 40 + "\n"
                "      - run: python3 scripts/check.py\n",
                encoding="utf-8",
            )
            (workflows / "b.yaml").write_text(
                "on:\n  workflow_call:\n  schedule:\n    - cron: '0 1 * * *'\n"
                "jobs:\n  b:\n    steps:\n      - uses: owner/action@v1\n"
                "      - run: python scripts/check.py\n",
                encoding="utf-8",
            )
            result = MODULE.audit_github(root)
            self.assertEqual(result["workflow_count"], 2)
            self.assertEqual(result["reusable_workflow_count"], 1)
            self.assertEqual(result["scheduled_workflow_count"], 1)
            self.assertEqual(result["unpinned_external_action_uses"], ["owner/action@v1"])
            self.assertEqual(result["repeated_python_entrypoints"][0]["workflow_occurrences"], 2)

    def test_gitlab_follows_local_include_and_counts_jobs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ci").mkdir()
            (root / ".gitlab-ci.yml").write_text(
                "include:\n  - local: ci/jobs.yml\nroot-job:\n  script:\n    - python3 scripts/check.py\n",
                encoding="utf-8",
            )
            (root / "ci" / "jobs.yml").write_text(
                "child-job:\n  allow_failure: true\n  script:\n    - python scripts/check.py\n"
                "manual-job:\n  when: manual\n  artifacts:\n    paths: [out.json]\n",
                encoding="utf-8",
            )
            result = MODULE.audit_gitlab(root)
            self.assertEqual(result["config_file_count"], 2)
            self.assertEqual(result["top_level_job_count"], 3)
            self.assertEqual(result["manual_job_markers"], 1)
            self.assertEqual(result["allow_failure_markers"], 1)
            self.assertEqual(result["artifact_blocks"], 1)
            self.assertEqual(result["repeated_python_entrypoints"][0]["job_occurrences"], 2)

    def test_report_is_advisory_and_public_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = MODULE.build_report(Path(tmp))
            self.assertEqual(report["mode"], "SHADOW_ADVISORY_ONLY")
            self.assertFalse(report["invariants"]["may_skip_existing_required_jobs"])
            self.assertFalse(report["invariants"]["reads_credentials_or_private_evidence"])
            self.assertTrue(report["invariants"]["public_safe_aggregate_only"])

    def test_missing_git_binary_is_reported_as_unknown_head(self):
        with mock.patch.object(MODULE.subprocess, "run", side_effect=FileNotFoundError):
            self.assertIsNone(MODULE._head(Path(".")))


if __name__ == "__main__":
    unittest.main()

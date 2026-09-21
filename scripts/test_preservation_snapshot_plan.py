import unittest
from preservation_snapshot_plan import plan


class SnapshotDecisionTests(unittest.TestCase):
    sha = "a" * 40

    def event(self, sha=None, conclusion="success", branch="main"):
        return {"workflow_run": {"head_sha": sha or self.sha,
                                 "conclusion": conclusion, "head_branch": branch}}

    def artifact(self, **changes):
        return dict({"id": 123, "name": "por-derecho-off-github-backup-" + self.sha,
                     "expired": False, "size_in_bytes": 99, "digest": "sha256:" + "b" * 64}, **changes)

    def test_first_accepted_main_is_captured(self):
        self.assertEqual(plan(self.sha, "workflow_run", self.event(), [])["create"], "true")

    def test_same_main_reuses_retained_package(self):
        result = plan(self.sha, "workflow_run", self.event(), [self.artifact()])
        self.assertEqual(result["create"], "false")
        self.assertEqual(result["reused_artifact_id"], "123")

    def test_other_sha_or_incomplete_artifact_does_not_suppress_backup(self):
        for changes in ({"name": "other-main"}, {"expired": True}, {"size_in_bytes": 0}, {"digest": None}):
            with self.subTest(changes=changes):
                self.assertEqual(plan(self.sha, "workflow_run", self.event(), [self.artifact(**changes)])["create"], "true")

    def test_old_or_failed_or_pr_acceptance_cannot_start_capture(self):
        for event in (self.event(sha="c" * 40), self.event(conclusion="failure"), self.event(branch="feature")):
            self.assertEqual(plan(self.sha, "workflow_run", event, [])["create"], "false")

    def test_unsupported_event_and_unknown_inventory_fail_closed(self):
        with self.assertRaises(ValueError):
            plan(self.sha, "pull_request", {}, [])
        with self.assertRaises(ValueError):
            plan(self.sha, "workflow_dispatch", {}, None)


if __name__ == "__main__":
    unittest.main()

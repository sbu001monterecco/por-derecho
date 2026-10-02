#!/usr/bin/env python3
"""Standard-library tests for scripts/workspace_persistence.py."""
from __future__ import annotations

import json
import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/workspace_persistence.py"
WORKSPACE_ID = "PD-WS-20260901-9999"
sys.path.insert(0, str(ROOT / "scripts"))
import workspace_persistence as runtime


class WorkspacePersistenceTests(unittest.TestCase):
    def checkpoint_fields(self) -> dict:
        return {
            "action_ledger": {**{key: [] for key in runtime.LEDGER_LIST_FIELDS}, "next_thread_bootstrap": "Resolve the recorded workspace and current repository baseline."},
            "coverage": {"scope": "Unit-test runtime only", "status": "BOUNDED_COMPLETE", "inspected": ["runtime fixture"], "remaining": [], "observed_at_utc": "2026-10-02T00:00:00Z"},
            "host_availability": [{"host_id": "LOCAL_TEST", "status": "AVAILABLE", "checked_at_utc": "2026-10-02T00:00:00Z", "boundary": "No remote provider checked."}],
        }

    def approval(self, summary: dict) -> dict:
        return {"status": "APPROVED", "scope": "EXACT_PUBLIC_SUMMARY", "authority_ref": "TEST-EXPLICIT-AUTHORISATION", "approved_at_utc": "2026-10-02T00:00:00Z", "summary_sha256": runtime.sha256_bytes(runtime.canonical_bytes(summary))}

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.vault = Path(self.temp.name) / "vault"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(self, *args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != expect:
            self.fail(
                f"Expected exit {expect}, got {result.returncode}\n"
                f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )
        return result

    def initialise(self) -> dict:
        result = self.run_cli(
            "init",
            "--vault",
            str(self.vault),
            "--workspace-id",
            WORKSPACE_ID,
            "--title",
            "Persistence smoke test",
            "--objective",
            "Verify append-only workspace state",
            "--baseline",
            "test-baseline",
        )
        return json.loads(result.stdout)

    def test_init_append_checkpoint_validate(self) -> None:
        initial = self.initialise()
        self.assertEqual(initial["status"], "INITIALISED")
        appended = json.loads(
            self.run_cli(
                "append",
                "--vault",
                str(self.vault),
                "--workspace-id",
                WORKSPACE_ID,
                "--event-type",
                "FACT_CORRECTED",
                "--summary",
                "One fact was corrected",
                "--details-json",
                '{"old":"A","new":"B"}',
                "--artifact-ref",
                "PD-DMA-0001",
            ).stdout
        )
        self.assertEqual(appended["sequence"], 2)
        checkpoint = json.loads(
            self.run_cli(
                "checkpoint",
                "--vault",
                str(self.vault),
                "--workspace-id",
                WORKSPACE_ID,
                "--summary",
                "CI checkpoint",
                "--payload-json",
                json.dumps(self.checkpoint_fields()),
                "--status",
                "DELETION_SAFE_WITH_OPEN_WORK",
                "--objective",
                "Runtime validated",
                "--completed",
                "Initialisation and append succeeded",
                "--open-task",
                "Create a real private vault",
                "--next-action",
                "Use the vault in a substantive workspace",
                "--do-not-infer",
                "Private data is public",
                "--repository-baseline",
                "test-checkpoint",
            ).stdout
        )
        self.assertEqual(checkpoint["workspace_status"], "DELETION_SAFE_WITH_OPEN_WORK")
        validated = json.loads(
            self.run_cli("validate", "--vault", str(self.vault)).stdout
        )
        self.assertEqual(validated["status"], "PASS")
        state = json.loads(
            (
                self.vault
                / "workspaces"
                / WORKSPACE_ID
                / "state.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(state["event_count"], 3)
        self.assertEqual(len(state["last_event_hash"]), 64)
        self.assertIn("Runtime validated", (self.vault / "workspaces" / WORKSPACE_ID / "handoff.md").read_text())

    def test_tampering_is_detected(self) -> None:
        self.initialise()
        events_path = self.vault / "workspaces" / WORKSPACE_ID / "events.jsonl"
        rows = events_path.read_text(encoding="utf-8").splitlines()
        event = json.loads(rows[0])
        event["summary"] = "Tampered after append"
        rows[0] = json.dumps(event)
        events_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
        result = self.run_cli(
            "validate",
            "--vault",
            str(self.vault),
            expect=1,
        )
        self.assertIn("event_hash mismatch", result.stderr)
        self.assertIn("content_hash mismatch", result.stderr)

    def test_public_summary_requires_explicit_approved_object(self) -> None:
        self.initialise()
        output = Path(self.temp.name) / "public.json"
        result = self.run_cli(
            "public-summary",
            "--vault",
            str(self.vault),
            "--workspace-id",
            WORKSPACE_ID,
            "--output",
            str(output),
            expect=1,
        )
        self.assertIn("No public_summary object is approved", result.stderr)
        payload = Path(self.temp.name) / "checkpoint.json"
        payload.write_text(
            json.dumps(
                {
                    **self.checkpoint_fields(),
                    "status": "IN_PROGRESS",
                    "public_summary": {
                        "title": "Public-safe checkpoint",
                        "state": "No private transcript included",
                    },
                    "public_summary_approval": self.approval({"title": "Public-safe checkpoint", "state": "No private transcript included"}),
                }
            ),
            encoding="utf-8",
        )
        self.run_cli(
            "checkpoint",
            "--vault",
            str(self.vault),
            "--workspace-id",
            WORKSPACE_ID,
            "--payload",
            str(payload),
        )
        exported = json.loads(
            self.run_cli(
                "public-summary",
                "--vault",
                str(self.vault),
                "--workspace-id",
                WORKSPACE_ID,
                "--output",
                str(output),
            ).stdout
        )
        self.assertEqual(exported["status"], "PUBLIC_SUMMARY_EXPORTED")
        public = json.loads(output.read_text(encoding="utf-8"))
        self.assertNotIn("events", public)
        self.assertEqual(public["summary"]["title"], "Public-safe checkpoint")

    def test_new_checkpoint_requires_ledger_without_writing_event(self):
        self.initialise()
        events = self.vault / "workspaces" / WORKSPACE_ID / "events.jsonl"
        before = events.read_bytes()
        result = self.run_cli("checkpoint", "--vault", str(self.vault), "--workspace-id", WORKSPACE_ID, "--summary", "missing ledger", expect=1)
        self.assertIn("action_ledger", result.stderr)
        self.assertEqual(events.read_bytes(), before)

    def test_incomplete_ledger_and_unbounded_complete_coverage_rejected(self):
        payload = self.checkpoint_fields()
        del payload["action_ledger"]["connected_source_actions"]
        with self.assertRaises(runtime.PersistenceError): runtime.validate_checkpoint_contract(payload)
        payload = self.checkpoint_fields()
        payload["coverage"]["remaining"] = ["unread attachment"]
        with self.assertRaises(runtime.PersistenceError): runtime.validate_checkpoint_contract(payload)

    def test_unavailable_host_is_recorded_without_claiming_global_failure(self):
        payload = self.checkpoint_fields()
        payload["host_availability"][0]["status"] = "UNAVAILABLE"
        payload["coverage"]["status"] = "PARTIAL"
        payload["coverage"]["remaining"] = ["Remote custody readback"]
        runtime.validate_checkpoint_contract(payload)

    def test_host_identity_duplicate_or_invalid_timestamp_rejected(self):
        payload = self.checkpoint_fields()
        payload["host_availability"].append(copy.deepcopy(payload["host_availability"][0]))
        with self.assertRaises(runtime.PersistenceError): runtime.validate_checkpoint_contract(payload)
        payload = self.checkpoint_fields()
        payload["coverage"]["observed_at_utc"] = "yesterday"
        with self.assertRaises(runtime.PersistenceError): runtime.validate_checkpoint_contract(payload)

    def test_public_object_alone_is_not_approval(self):
        with self.assertRaises(runtime.PersistenceError):
            runtime.validate_public_summary({"title": "Public-safe"}, None)

    def test_exact_summary_hash_and_revocation_enforced(self):
        summary = {"title": "Approved summary"}
        approval = self.approval(summary)
        runtime.validate_public_summary(summary, approval)
        with self.assertRaises(runtime.PersistenceError): runtime.validate_public_summary({"title": "Changed"}, approval)
        approval["status"] = "REVOKED"
        with self.assertRaises(runtime.PersistenceError): runtime.validate_public_summary(summary, approval)

    def test_known_private_locators_rejected_despite_matching_approval(self):
        # Synthetic fixtures are assembled as data, never usable source-access links.
        fixture_hosts = ("drive.google.com", "mail.google.com")
        synthetic_urls = [f"https://{host}/synthetic-unit-test" for host in fixture_hosts]
        for secret in [*synthetic_urls, "person@example.test"]:
            summary = {"state": secret}
            with self.assertRaises(runtime.PersistenceError): runtime.validate_public_summary(summary, self.approval(summary))

    def test_arbitrary_nested_public_fields_rejected(self):
        summary = {"title": "Safe title", "private_source": {"provider_id": "secret"}}
        with self.assertRaises(runtime.PersistenceError): runtime.validate_public_summary(summary, self.approval(summary))

    def test_summary_change_clears_inherited_approval(self):
        original = {"title": "Before"}
        state = {"status": "IN_PROGRESS", "public_summary": original, "public_summary_approval": self.approval(original)}
        changed = runtime.merge_state(state, {"public_summary": {"title": "After"}})
        self.assertIsNone(changed["public_summary_approval"])

    def test_state_only_approval_cannot_bypass_event_chain(self):
        self.initialise()
        path = self.vault / "workspaces" / WORKSPACE_ID / "state.json"
        state = json.loads(path.read_text())
        state["public_summary"] = {"title": "Injected"}
        state["public_summary_approval"] = self.approval(state["public_summary"])
        path.write_text(json.dumps(state))
        result = self.run_cli("public-summary", "--vault", str(self.vault), "--workspace-id", WORKSPACE_ID, "--output", str(Path(self.temp.name)/"public.json"), expect=1)
        self.assertIn("event chain", result.stderr)

    def test_valid_looking_coverage_tamper_is_detected(self):
        self.initialise()
        self.run_cli("checkpoint", "--vault", str(self.vault), "--workspace-id", WORKSPACE_ID, "--payload-json", json.dumps(self.checkpoint_fields()))
        path = self.vault / "workspaces" / WORKSPACE_ID / "state.json"
        state = json.loads(path.read_text())
        state["coverage"]["scope"] = "Broader unverified scope"
        path.write_text(json.dumps(state))
        result = self.run_cli("validate", "--vault", str(self.vault), expect=1)
        self.assertIn("coverage differs", result.stderr)

    def test_chatgpt_export_import_is_private_and_excludes_tool_by_default(self) -> None:
        export_path = Path(self.temp.name) / "conversations.json"
        export_path.write_text(
            json.dumps(
                [
                    {
                        "id": "conversation-1",
                        "title": "Imported test",
                        "create_time": 1788260000,
                        "update_time": 1788260100,
                        "mapping": {
                            "a": {
                                "parent": None,
                                "message": {
                                    "author": {"role": "user"},
                                    "create_time": 1788260001,
                                    "content": {"content_type": "text", "parts": ["Hello"]},
                                    "metadata": {},
                                },
                            },
                            "b": {
                                "parent": "a",
                                "message": {
                                    "author": {"role": "assistant"},
                                    "create_time": 1788260002,
                                    "content": {"content_type": "text", "parts": ["Reply"]},
                                    "metadata": {},
                                },
                            },
                            "c": {
                                "parent": "b",
                                "message": {
                                    "author": {"role": "tool"},
                                    "create_time": 1788260003,
                                    "content": {"content_type": "text", "parts": ["Internal tool output"]},
                                    "metadata": {},
                                },
                            },
                        },
                    }
                ]
            ),
            encoding="utf-8",
        )
        imported = json.loads(
            self.run_cli(
                "import-chatgpt",
                "--vault",
                str(self.vault),
                "--source",
                str(export_path),
                "--batch-id",
                "PD-CGX-20260901-ci",
            ).stdout
        )
        self.assertEqual(imported["status"], "IMPORTED_PRIVATE_ONLY")
        self.assertEqual(imported["visible_message_count"], 2)
        batch = self.vault / "imports" / "chatgpt" / "PD-CGX-20260901-ci"
        manifest = json.loads((batch / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["raw_publication_status"], "PRIVATE_ONLY_DO_NOT_PUBLISH")
        normalized = (batch / "conversations" / "conversation-1.jsonl").read_text(encoding="utf-8")
        self.assertIn("Hello", normalized)
        self.assertIn("Reply", normalized)
        self.assertNotIn("Internal tool output", normalized)

    def test_vault_inside_public_repository_is_refused(self) -> None:
        unsafe = ROOT / ".workspace-vault"
        result = self.run_cli(
            "init",
            "--vault",
            str(unsafe),
            "--workspace-id",
            WORKSPACE_ID,
            "--title",
            "Unsafe",
            expect=1,
        )
        self.assertIn("Refusing to place private workspace data inside the public repository", result.stderr)
        self.assertFalse(unsafe.exists())


if __name__ == "__main__":
    unittest.main()

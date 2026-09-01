#!/usr/bin/env python3
"""Standard-library tests for scripts/workspace_persistence.py."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/workspace_persistence.py"
WORKSPACE_ID = "PD-WS-20260901-9999"


class WorkspacePersistenceTests(unittest.TestCase):
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
                    "status": "IN_PROGRESS",
                    "public_summary": {
                        "title": "Public-safe checkpoint",
                        "state": "No private transcript included",
                    },
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

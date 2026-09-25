#!/usr/bin/env python3
"""Private, append-only workspace persistence runtime for Por Derecho.

This tool intentionally stores raw workspace state outside the public repository.
It uses only the Python standard library so it can run locally and in CI.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
import zipfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_RE = re.compile(r"^PD-WS-(\d{8})-(\d{4})$")
EVENT_TYPE_RE = re.compile(r"^[A-Z][A-Z0-9_]{1,63}$")
ZERO_HASH = "0" * 64

VISIBILITY_CLASSES = {
    "PUBLIC_SOURCE_SAFE",
    "PUBLIC_DERIVED_SAFE",
    "PRIVATE_WORKSPACE",
    "CONFIDENTIAL_USER_SUPPLIED",
    "CONNECTED_SOURCE_RESTRICTED",
    "PUBLICATION_REVIEW_REQUIRED",
}
WORKSPACE_STATUSES = {
    "IN_PROGRESS",
    "HANDOFF_READY",
    "DELETION_SAFE",
    "DELETION_SAFE_WITH_OPEN_WORK",
    "PAUSED",
    "SUPERSEDED",
    "CLOSED",
}

REQUIRED_REPOSITORY_PATHS = [
    ".github/governance/AUTOMATIC_WORKSPACE_PERSISTENCE_ARCHITECTURE_01SEP2026.md",
    ".github/governance/WORKSPACE_THREAD_CONTINUITY_HANDOFF_STANDARD_01SEP2026.md",
    "ops/AUTOMATIC_WORKSPACE_PERSISTENCE_V1.json",
    "ops/WORKSPACE_THREAD_CONTINUITY_HANDOFF_V1.json",
    "data/workspace-register-v1.json",
    "CURRENT_WORKSPACE_HANDOFF.md",
    "scripts/workspace_persistence.py",
    "schemas/workspace-event-v1.schema.json",
    "schemas/workspace-state-v1.schema.json",
    "schemas/chatgpt-export-import-manifest-v1.schema.json",
    "docs/WORKSPACE_PERSISTENCE_RUNBOOK.md",
    ".github/workflows/audit-workspace-persistence.yml",
]
REQUIRED_GITIGNORE_MARKERS = [
    ".workspace-vault/",
    ".pd-workspace-vault/",
    "private-workspaces/",
    "workspaces-private/",
    "conversations.json",
    "*.chatgpt-export.zip",
]


class PersistenceError(RuntimeError):
    """Safe user-facing persistence error."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def utc_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def chmod_private(path: Path, mode: int) -> None:
    if os.name == "posix":
        try:
            path.chmod(mode)
        except OSError:
            pass


def atomic_write_bytes(path: Path, data: bytes, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    chmod_private(path.parent, 0o700)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
        chmod_private(path, mode)
    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)


def atomic_write_text(path: Path, text: str, mode: int = 0o600) -> None:
    atomic_write_bytes(path, text.encode("utf-8"), mode=mode)


def atomic_write_json(path: Path, value: Any, mode: int = 0o600) -> None:
    atomic_write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n", mode=mode)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PersistenceError(f"Missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PersistenceError(f"Invalid JSON in {path}: {exc}") from exc


def parse_json_argument(raw: str | None, file_path: str | None) -> dict[str, Any]:
    if raw and file_path:
        raise PersistenceError("Use either inline JSON or a JSON file, not both.")
    if file_path:
        value = load_json(Path(file_path).expanduser().resolve())
    elif raw:
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise PersistenceError(f"Invalid inline JSON: {exc}") from exc
    else:
        value = {}
    if not isinstance(value, dict):
        raise PersistenceError("JSON payload must be an object.")
    return value


@contextmanager
def exclusive_lock(path: Path, timeout_seconds: float = 15.0) -> Iterable[None]:
    """Portable lock using exclusive file creation."""
    deadline = time.monotonic() + timeout_seconds
    fd: int | None = None
    while fd is None:
        try:
            fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.write(fd, f"{os.getpid()} {utc_now()}\n".encode("utf-8"))
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise PersistenceError(f"Timed out waiting for lock: {path}")
            time.sleep(0.1)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
        path.unlink(missing_ok=True)


def resolve_vault(raw: str | None, create: bool = True) -> Path:
    candidate = raw or os.environ.get("PD_WORKSPACE_VAULT")
    if not candidate:
        raise PersistenceError(
            "Private vault path required. Pass --vault or set PD_WORKSPACE_VAULT."
        )
    unresolved = Path(candidate).expanduser()
    if unresolved.exists() and unresolved.is_symlink():
        raise PersistenceError("Vault root may not be a symlink.")
    vault = unresolved.resolve()
    if is_within(vault, ROOT):
        raise PersistenceError(
            f"Refusing to place private workspace data inside the public repository: {vault}"
        )
    if create:
        vault.mkdir(parents=True, exist_ok=True)
        chmod_private(vault, 0o700)
        marker = vault / ".pd-private-workspace-vault"
        if not marker.exists():
            atomic_write_json(
                marker,
                {
                    "schema": "por-derecho.private-workspace-vault.v1",
                    "created_at_utc": utc_now(),
                    "warning": "PRIVATE: do not mirror raw contents to the public por-derecho repository.",
                },
            )
    elif not vault.is_dir():
        raise PersistenceError(f"Vault does not exist: {vault}")
    return vault


def workspace_dir(vault: Path, workspace_id: str) -> Path:
    validate_workspace_id(workspace_id)
    return vault / "workspaces" / workspace_id


def validate_workspace_id(workspace_id: str) -> None:
    if not WORKSPACE_RE.fullmatch(workspace_id):
        raise PersistenceError(
            f"Invalid workspace ID {workspace_id!r}; expected PD-WS-YYYYMMDD-NNNN."
        )


def next_workspace_id(vault: Path) -> str:
    date = utc_date()
    workspaces = vault / "workspaces"
    workspaces.mkdir(parents=True, exist_ok=True)
    chmod_private(workspaces, 0o700)
    highest = 0
    for path in workspaces.glob(f"PD-WS-{date}-[0-9][0-9][0-9][0-9]"):
        match = WORKSPACE_RE.fullmatch(path.name)
        if match:
            highest = max(highest, int(match.group(2)))
    if highest >= 9999:
        raise PersistenceError(f"Workspace sequence exhausted for {date}.")
    return f"PD-WS-{date}-{highest + 1:04d}"


def read_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise PersistenceError(f"{path}:{line_no}: invalid JSONL: {exc}") from exc
            if not isinstance(value, dict):
                raise PersistenceError(f"{path}:{line_no}: event must be an object.")
            events.append(value)
    return events


def validate_event_chain(events: list[dict[str, Any]], workspace_id: str) -> list[str]:
    errors: list[str] = []
    previous = ZERO_HASH
    for index, event in enumerate(events, 1):
        prefix = f"event {index}"
        if event.get("workspace_id") != workspace_id:
            errors.append(f"{prefix}: workspace_id mismatch")
        if event.get("sequence") != index:
            errors.append(f"{prefix}: sequence must be {index}")
        if event.get("previous_event_hash") != previous:
            errors.append(f"{prefix}: previous_event_hash mismatch")
        event_hash = event.get("event_hash")
        if not isinstance(event_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", event_hash):
            errors.append(f"{prefix}: invalid event_hash")
            previous = event_hash if isinstance(event_hash, str) else previous
            continue
        core = {key: value for key, value in event.items() if key != "event_hash"}
        expected = sha256_bytes(canonical_bytes(core))
        if event_hash != expected:
            errors.append(f"{prefix}: event_hash mismatch")
        content_fields = {
            "event_type": event.get("event_type"),
            "visibility_class": event.get("visibility_class"),
            "summary": event.get("summary"),
            "details": event.get("details", {}),
            "repository_refs": event.get("repository_refs", []),
            "artifact_refs": event.get("artifact_refs", []),
            "source_refs": event.get("source_refs", []),
            "thread_refs": event.get("thread_refs", []),
        }
        expected_content = sha256_bytes(canonical_bytes(content_fields))
        if event.get("content_hash") != expected_content:
            errors.append(f"{prefix}: content_hash mismatch")
        previous = event_hash
    return errors


def append_event(
    wdir: Path,
    event_type: str,
    summary: str,
    visibility_class: str,
    details: dict[str, Any] | None = None,
    repository_refs: list[str] | None = None,
    artifact_refs: list[str] | None = None,
    source_refs: list[str] | None = None,
    thread_refs: list[str] | None = None,
) -> dict[str, Any]:
    if not EVENT_TYPE_RE.fullmatch(event_type):
        raise PersistenceError(
            "event_type must be uppercase snake-case, 2-64 characters."
        )
    if visibility_class not in VISIBILITY_CLASSES:
        raise PersistenceError(f"Unsupported visibility class: {visibility_class}")
    summary = summary.strip()
    if not summary:
        raise PersistenceError("Event summary may not be empty.")
    events_path = wdir / "events.jsonl"
    with exclusive_lock(wdir / ".events.lock"):
        events = read_events(events_path)
        chain_errors = validate_event_chain(events, wdir.name)
        if chain_errors:
            raise PersistenceError(
                "Refusing append because the existing event chain is invalid: "
                + "; ".join(chain_errors[:5])
            )
        sequence = len(events) + 1
        previous_hash = events[-1]["event_hash"] if events else ZERO_HASH
        content_fields = {
            "event_type": event_type,
            "visibility_class": visibility_class,
            "summary": summary,
            "details": details or {},
            "repository_refs": repository_refs or [],
            "artifact_refs": artifact_refs or [],
            "source_refs": source_refs or [],
            "thread_refs": thread_refs or [],
        }
        event = {
            "schema": "por-derecho.workspace-event.v1",
            "event_id": f"{wdir.name}-EVT-{sequence:06d}",
            "workspace_id": wdir.name,
            "sequence": sequence,
            "timestamp_utc": utc_now(),
            **content_fields,
            "content_hash": sha256_bytes(canonical_bytes(content_fields)),
            "previous_event_hash": previous_hash,
        }
        event["event_hash"] = sha256_bytes(canonical_bytes(event))
        encoded = json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n"
        with events_path.open("a", encoding="utf-8") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        chmod_private(events_path, 0o600)
    return event


def default_state(metadata: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    latest = events[-1] if events else None
    return {
        "schema": "por-derecho.workspace-state.v1",
        "workspace_id": metadata["workspace_id"],
        "title": metadata["title"],
        "status": metadata.get("status", "IN_PROGRESS"),
        "visibility_class": metadata.get("visibility_class", "PRIVATE_WORKSPACE"),
        "objective": metadata.get("current_objective", ""),
        "created_at_utc": metadata["created_at_utc"],
        "updated_at_utc": metadata.get("updated_at_utc", metadata["created_at_utc"]),
        "event_count": len(events),
        "last_event_id": latest.get("event_id") if latest else None,
        "last_event_hash": latest.get("event_hash") if latest else None,
        "repository_state": metadata.get("repository_state", {}),
        "thread_aliases": metadata.get("thread_aliases", []),
        "completed": [],
        "decisions": [],
        "open_tasks": [],
        "next_actions": [],
        "do_not_infer": [],
        "artifact_refs": [],
        "source_refs": [],
        "public_summary": None,
    }


def merge_state(base: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "status",
        "objective",
        "completed",
        "decisions",
        "open_tasks",
        "next_actions",
        "do_not_infer",
        "artifact_refs",
        "source_refs",
        "public_summary",
        "repository_state",
        "thread_aliases",
        "publication_state",
        "tool_failures",
        "notes",
    }
    unknown = sorted(set(payload) - allowed - {"summary", "visibility_class"})
    if unknown:
        raise PersistenceError(f"Unknown checkpoint payload fields: {', '.join(unknown)}")
    result = dict(base)
    for key in allowed:
        if key in payload:
            result[key] = payload[key]
    if result.get("status") not in WORKSPACE_STATUSES:
        raise PersistenceError(f"Unsupported workspace status: {result.get('status')}")
    for key in (
        "completed",
        "decisions",
        "open_tasks",
        "next_actions",
        "do_not_infer",
        "artifact_refs",
        "source_refs",
        "thread_aliases",
        "tool_failures",
    ):
        value = result.get(key, [])
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            raise PersistenceError(f"State field {key} must be a list of strings.")
    if result.get("public_summary") is not None and not isinstance(
        result["public_summary"], dict
    ):
        raise PersistenceError("public_summary must be an object or null.")
    return result


def render_handoff(state: dict[str, Any]) -> str:
    def section(title: str, values: list[str]) -> list[str]:
        lines = [f"## {title}", ""]
        if values:
            lines.extend(f"- {item}" for item in values)
        else:
            lines.append("- None recorded.")
        lines.append("")
        return lines

    lines = [
        f"# Workspace handoff — {state['title']}",
        "",
        f"**Workspace ID:** `{state['workspace_id']}`  ",
        f"**Status:** `{state['status']}`  ",
        f"**Visibility:** `{state['visibility_class']}`  ",
        f"**Last checkpoint:** `{state['updated_at_utc']}`  ",
        f"**Event count:** `{state['event_count']}`  ",
        f"**Last event hash:** `{state.get('last_event_hash') or 'NONE'}`",
        "",
        "## Current objective",
        "",
        state.get("objective") or "No objective recorded.",
        "",
        "## Repository state",
        "",
        "```json",
        json.dumps(state.get("repository_state", {}), ensure_ascii=False, indent=2),
        "```",
        "",
    ]
    lines += section("Completed", state.get("completed", []))
    lines += section("Decisions and terminology locks", state.get("decisions", []))
    lines += section("Open tasks", state.get("open_tasks", []))
    lines += section("Next actions", state.get("next_actions", []))
    lines += section("Do not infer / do not repeat", state.get("do_not_infer", []))
    lines += section("Artifact references", state.get("artifact_refs", []))
    lines += section("Source references", state.get("source_refs", []))
    lines += section("Thread/session aliases", state.get("thread_aliases", []))
    lines += section("Tool failures affecting continuity", state.get("tool_failures", []))
    lines += [
        "## Resume instruction",
        "",
        "> Reconcile the repository baseline and this private workspace state before acting. "
        "Continue from the recorded open work; do not infer publication, filing, service, "
        "ownership, responsibility or evidential proof from proximity or from a completed tool action.",
        "",
        "## Integrity note",
        "",
        "The authoritative chronological record is `events.jsonl`. Each event carries a SHA-256 "
        "hash and the previous event hash. This handoff is a derived current-state view, not a "
        "replacement for the append-only event chain.",
        "",
    ]
    return "\n".join(lines)


def write_state_and_handoff(
    wdir: Path, metadata: dict[str, Any], state: dict[str, Any]
) -> None:
    events = read_events(wdir / "events.jsonl")
    latest = events[-1] if events else None
    state = dict(state)
    state.update(
        {
            "schema": "por-derecho.workspace-state.v1",
            "workspace_id": metadata["workspace_id"],
            "title": metadata["title"],
            "visibility_class": metadata.get("visibility_class", "PRIVATE_WORKSPACE"),
            "created_at_utc": metadata["created_at_utc"],
            "updated_at_utc": utc_now(),
            "event_count": len(events),
            "last_event_id": latest.get("event_id") if latest else None,
            "last_event_hash": latest.get("event_hash") if latest else None,
        }
    )
    atomic_write_json(wdir / "state.json", state)
    atomic_write_text(wdir / "handoff.md", render_handoff(state))


def cmd_init(args: argparse.Namespace) -> dict[str, Any]:
    vault = resolve_vault(args.vault)
    with exclusive_lock(vault / ".workspace-id.lock"):
        workspace_id = args.workspace_id or next_workspace_id(vault)
        validate_workspace_id(workspace_id)
        wdir = workspace_dir(vault, workspace_id)
        if wdir.exists():
            if not args.resume:
                raise PersistenceError(
                    f"Workspace already exists: {workspace_id}; use --resume to recover it."
                )
            metadata = load_json(wdir / "workspace.json")
            return {
                "status": "RESUMED",
                "workspace_id": workspace_id,
                "path": str(wdir),
                "last_checkpoint": metadata.get("updated_at_utc"),
            }
        wdir.mkdir(parents=True)
        chmod_private(wdir, 0o700)
        now = utc_now()
        metadata = {
            "schema": "por-derecho.private-workspace.v1",
            "workspace_id": workspace_id,
            "title": args.title.strip(),
            "status": "IN_PROGRESS",
            "visibility_class": args.classification,
            "current_objective": args.objective.strip(),
            "created_at_utc": now,
            "updated_at_utc": now,
            "repository_state": {
                "repository": args.repository,
                "baseline": args.baseline,
            },
            "thread_aliases": args.thread_ref or [],
        }
        if not metadata["title"]:
            raise PersistenceError("Workspace title may not be empty.")
        if args.classification not in VISIBILITY_CLASSES:
            raise PersistenceError(f"Unsupported visibility class: {args.classification}")
        atomic_write_json(wdir / "workspace.json", metadata)
        for filename, initial in (
            ("artifacts.json", {"schema": "por-derecho.workspace-artifacts.v1", "items": []}),
            ("sources.json", {"schema": "por-derecho.workspace-sources.v1", "items": []}),
            (
                "attachments-manifest.json",
                {"schema": "por-derecho.workspace-attachments.v1", "items": []},
            ),
        ):
            atomic_write_json(wdir / filename, initial)
        atomic_write_text(wdir / "publication-events.jsonl", "")
        event = append_event(
            wdir,
            "WORKSPACE_INITIALISED",
            f"Workspace initialised: {metadata['title']}",
            args.classification,
            details={"objective": metadata["current_objective"]},
            repository_refs=[
                ref
                for ref in (args.repository, args.baseline)
                if isinstance(ref, str) and ref
            ],
            thread_refs=args.thread_ref or [],
        )
        state = default_state(metadata, [event])
        write_state_and_handoff(wdir, metadata, state)
        return {
            "status": "INITIALISED",
            "workspace_id": workspace_id,
            "path": str(wdir),
            "event_id": event["event_id"],
            "event_hash": event["event_hash"],
        }


def require_workspace(vault: Path, workspace_id: str) -> tuple[Path, dict[str, Any]]:
    wdir = workspace_dir(vault, workspace_id)
    if not wdir.is_dir():
        raise PersistenceError(f"Workspace does not exist: {workspace_id}")
    metadata = load_json(wdir / "workspace.json")
    if metadata.get("workspace_id") != workspace_id:
        raise PersistenceError("workspace.json identity mismatch.")
    return wdir, metadata


def cmd_append(args: argparse.Namespace) -> dict[str, Any]:
    vault = resolve_vault(args.vault, create=False)
    wdir, metadata = require_workspace(vault, args.workspace_id)
    details = parse_json_argument(args.details_json, args.details_file)
    event = append_event(
        wdir,
        args.event_type,
        args.summary,
        args.visibility,
        details=details,
        repository_refs=args.repository_ref or [],
        artifact_refs=args.artifact_ref or [],
        source_refs=args.source_ref or [],
        thread_refs=args.thread_ref or [],
    )
    metadata["updated_at_utc"] = event["timestamp_utc"]
    aliases = list(dict.fromkeys(metadata.get("thread_aliases", []) + (args.thread_ref or [])))
    metadata["thread_aliases"] = aliases
    atomic_write_json(wdir / "workspace.json", metadata)
    existing_state = (
        load_json(wdir / "state.json")
        if (wdir / "state.json").exists()
        else default_state(metadata, [])
    )
    write_state_and_handoff(wdir, metadata, existing_state)
    return {
        "status": "APPENDED",
        "workspace_id": args.workspace_id,
        "event_id": event["event_id"],
        "event_hash": event["event_hash"],
        "sequence": event["sequence"],
    }


def cmd_checkpoint(args: argparse.Namespace) -> dict[str, Any]:
    vault = resolve_vault(args.vault, create=False)
    wdir, metadata = require_workspace(vault, args.workspace_id)
    payload = parse_json_argument(args.payload_json, args.payload)
    if args.status:
        payload["status"] = args.status
    if args.objective:
        payload["objective"] = args.objective
    if args.completed:
        payload["completed"] = args.completed
    if args.open_task:
        payload["open_tasks"] = args.open_task
    if args.next_action:
        payload["next_actions"] = args.next_action
    if args.do_not_infer:
        payload["do_not_infer"] = args.do_not_infer
    if args.repository_baseline:
        repo_state = dict(payload.get("repository_state", {}))
        repo_state["baseline"] = args.repository_baseline
        payload["repository_state"] = repo_state
    summary = payload.pop("summary", None) or args.summary or "Workspace checkpoint"
    visibility = payload.pop("visibility_class", None) or args.visibility
    existing_state = (
        load_json(wdir / "state.json")
        if (wdir / "state.json").exists()
        else default_state(metadata, read_events(wdir / "events.jsonl"))
    )
    state = merge_state(existing_state, payload)
    event = append_event(
        wdir,
        "WORKSPACE_CHECKPOINT",
        summary,
        visibility,
        details=payload,
        repository_refs=args.repository_ref or [],
        artifact_refs=state.get("artifact_refs", []),
        source_refs=state.get("source_refs", []),
        thread_refs=state.get("thread_aliases", []),
    )
    metadata["status"] = state["status"]
    metadata["current_objective"] = state.get("objective", "")
    metadata["updated_at_utc"] = event["timestamp_utc"]
    metadata["repository_state"] = state.get(
        "repository_state", metadata.get("repository_state", {})
    )
    metadata["thread_aliases"] = state.get(
        "thread_aliases", metadata.get("thread_aliases", [])
    )
    atomic_write_json(wdir / "workspace.json", metadata)
    state["status"] = metadata["status"]
    write_state_and_handoff(wdir, metadata, state)
    return {
        "status": "CHECKPOINTED",
        "workspace_id": args.workspace_id,
        "workspace_status": metadata["status"],
        "event_id": event["event_id"],
        "event_hash": event["event_hash"],
        "handoff": str(wdir / "handoff.md"),
    }


def validate_workspace(wdir: Path) -> list[str]:
    errors: list[str] = []
    workspace_id = wdir.name
    try:
        validate_workspace_id(workspace_id)
    except PersistenceError as exc:
        errors.append(str(exc))
        return errors
    required = [
        "workspace.json",
        "events.jsonl",
        "state.json",
        "handoff.md",
        "artifacts.json",
        "sources.json",
        "attachments-manifest.json",
        "publication-events.jsonl",
    ]
    for name in required:
        if not (wdir / name).is_file():
            errors.append(f"{workspace_id}: missing {name}")
    if errors:
        return errors
    try:
        metadata = load_json(wdir / "workspace.json")
        state = load_json(wdir / "state.json")
        events = read_events(wdir / "events.jsonl")
    except PersistenceError as exc:
        errors.append(str(exc))
        return errors
    if metadata.get("workspace_id") != workspace_id:
        errors.append(f"{workspace_id}: workspace.json identity mismatch")
    if state.get("workspace_id") != workspace_id:
        errors.append(f"{workspace_id}: state.json identity mismatch")
    if metadata.get("status") not in WORKSPACE_STATUSES:
        errors.append(f"{workspace_id}: invalid workspace status")
    if metadata.get("visibility_class") not in VISIBILITY_CLASSES:
        errors.append(f"{workspace_id}: invalid visibility class")
    errors.extend(f"{workspace_id}: {item}" for item in validate_event_chain(events, workspace_id))
    if state.get("event_count") != len(events):
        errors.append(f"{workspace_id}: state event_count mismatch")
    if events and state.get("last_event_hash") != events[-1].get("event_hash"):
        errors.append(f"{workspace_id}: state last_event_hash mismatch")
    if not events:
        errors.append(f"{workspace_id}: event chain is empty")
    return errors


def cmd_validate(args: argparse.Namespace) -> dict[str, Any]:
    vault = resolve_vault(args.vault, create=False)
    root = vault / "workspaces"
    if args.workspace_id:
        targets = [workspace_dir(vault, args.workspace_id)]
    else:
        targets = sorted(path for path in root.glob("PD-WS-*") if path.is_dir()) if root.exists() else []
    errors: list[str] = []
    for target in targets:
        if not target.is_dir():
            errors.append(f"Missing workspace directory: {target}")
        else:
            errors.extend(validate_workspace(target))
    result = {
        "status": "PASS" if not errors else "FAIL",
        "vault": str(vault),
        "workspace_count": len(targets),
        "errors": errors,
    }
    if errors:
        raise PersistenceError(json.dumps(result, ensure_ascii=False))
    return result


def safe_component(value: str, fallback: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-._")
    return cleaned[:120] or fallback


def timestamp_from_epoch(value: Any) -> str | None:
    try:
        return datetime.fromtimestamp(float(value), timezone.utc).replace(
            microsecond=0
        ).isoformat().replace("+00:00", "Z")
    except (TypeError, ValueError, OSError):
        return None


def extract_message_text(message: dict[str, Any]) -> tuple[str, bool]:
    content = message.get("content") or {}
    parts = content.get("parts") if isinstance(content, dict) else None
    if not isinstance(parts, list):
        return "", False
    rendered: list[str] = []
    nontext = False
    for part in parts:
        if isinstance(part, str):
            rendered.append(part)
        elif isinstance(part, dict):
            text = part.get("text")
            if isinstance(text, str):
                rendered.append(text)
            else:
                nontext = True
        else:
            nontext = True
    return "\n".join(rendered), nontext


def load_chatgpt_conversations(source: Path) -> tuple[list[dict[str, Any]], bytes, str]:
    if not source.is_file():
        raise PersistenceError(f"ChatGPT export source not found: {source}")
    if zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as archive:
            names = [name for name in archive.namelist() if name.endswith("conversations.json")]
            if not names:
                raise PersistenceError("ZIP does not contain conversations.json.")
            name = sorted(names, key=lambda item: (item.count("/"), len(item)))[0]
            raw = archive.read(name)
            source_member = name
    else:
        raw = source.read_bytes()
        source_member = source.name
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PersistenceError(f"Cannot parse conversations JSON: {exc}") from exc
    if not isinstance(value, list):
        raise PersistenceError("conversations.json must contain a list.")
    conversations = [item for item in value if isinstance(item, dict)]
    return conversations, raw, source_member


def cmd_import_chatgpt(args: argparse.Namespace) -> dict[str, Any]:
    vault = resolve_vault(args.vault)
    source = Path(args.source).expanduser().resolve()
    conversations, raw_json, source_member = load_chatgpt_conversations(source)
    batch_id = args.batch_id or f"PD-CGX-{utc_date()}-{int(time.time())}"
    if not re.fullmatch(r"PD-CGX-\d{8}-[A-Za-z0-9_-]{1,32}", batch_id):
        raise PersistenceError("batch_id must match PD-CGX-YYYYMMDD-<token>.")
    batch_dir = vault / "imports" / "chatgpt" / batch_id
    if batch_dir.exists():
        raise PersistenceError(f"Import batch already exists: {batch_id}")
    conv_dir = batch_dir / "conversations"
    conv_dir.mkdir(parents=True)
    chmod_private(batch_dir, 0o700)
    chmod_private(conv_dir, 0o700)

    allowed_roles = {"user", "assistant"}
    if args.include_system:
        allowed_roles.update({"system", "tool"})
    manifest_rows: list[dict[str, Any]] = []
    clustering_queue: list[dict[str, Any]] = []
    message_total = 0
    branch_node_total = 0

    for index, conversation in enumerate(conversations, 1):
        conversation_id = str(
            conversation.get("id")
            or conversation.get("conversation_id")
            or f"conversation-{index:06d}"
        )
        filename = safe_component(conversation_id, f"conversation-{index:06d}") + ".jsonl"
        output = conv_dir / filename
        mapping = conversation.get("mapping")
        rows: list[dict[str, Any]] = []
        if isinstance(mapping, dict):
            for node_id, node in mapping.items():
                if not isinstance(node, dict):
                    continue
                message = node.get("message")
                if not isinstance(message, dict):
                    continue
                author = message.get("author") or {}
                role = author.get("role") if isinstance(author, dict) else None
                if role not in allowed_roles:
                    continue
                text, has_nontext = extract_message_text(message)
                if not text and not has_nontext:
                    continue
                row = {
                    "schema": "por-derecho.chatgpt-visible-message.v1",
                    "conversation_id": conversation_id,
                    "node_id": str(node_id),
                    "parent_node_id": node.get("parent"),
                    "role": role,
                    "created_at_utc": timestamp_from_epoch(message.get("create_time")),
                    "content_type": (
                        message.get("content", {}).get("content_type")
                        if isinstance(message.get("content"), dict)
                        else None
                    ),
                    "text": text,
                    "text_sha256": sha256_bytes(text.encode("utf-8")),
                    "has_nontext_parts": has_nontext,
                    "metadata_keys": sorted(
                        str(key) for key in (message.get("metadata") or {}).keys()
                    )
                    if isinstance(message.get("metadata"), dict)
                    else [],
                }
                rows.append(row)
        rows.sort(
            key=lambda item: (
                item.get("created_at_utc") or "9999",
                item.get("node_id") or "",
            )
        )
        for seq, row in enumerate(rows, 1):
            row["sequence_in_export_order"] = seq
        atomic_write_text(
            output,
            "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        )
        message_total += len(rows)
        branch_node_total += len(mapping) if isinstance(mapping, dict) else 0
        title = str(conversation.get("title") or "Untitled conversation")
        summary = {
            "conversation_id": conversation_id,
            "title": title,
            "created_at_utc": timestamp_from_epoch(conversation.get("create_time")),
            "updated_at_utc": timestamp_from_epoch(conversation.get("update_time")),
            "message_count": len(rows),
            "mapping_node_count": len(mapping) if isinstance(mapping, dict) else 0,
            "normalized_path": str(output.relative_to(batch_dir)),
            "normalized_sha256": sha256_file(output),
            "workspace_assignment": "UNASSIGNED_REVIEW_REQUIRED",
        }
        manifest_rows.append(summary)
        clustering_queue.append(
            {
                "conversation_id": conversation_id,
                "title": title,
                "created_at_utc": summary["created_at_utc"],
                "updated_at_utc": summary["updated_at_utc"],
                "message_count": len(rows),
                "proposed_workspace_id": None,
                "review_state": "UNREVIEWED",
            }
        )

    atomic_write_text(
        batch_dir / "conversations-manifest.jsonl",
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in manifest_rows),
    )
    atomic_write_json(
        batch_dir / "clustering-queue.json",
        {
            "schema": "por-derecho.chatgpt-workspace-clustering-queue.v1",
            "batch_id": batch_id,
            "items": clustering_queue,
            "rule": "Do not auto-publish or let stale chat state overwrite current repository truth.",
        },
    )
    source_sha = sha256_file(source)
    if args.copy_source:
        source_dir = batch_dir / "source"
        source_dir.mkdir()
        chmod_private(source_dir, 0o700)
        copied = source_dir / safe_component(source.name, "chatgpt-export")
        shutil.copy2(source, copied)
        chmod_private(copied, 0o600)
        copied_path: str | None = str(copied.relative_to(batch_dir))
    else:
        copied_path = None
    manifest = {
        "schema": "por-derecho.chatgpt-export-import-manifest.v1",
        "batch_id": batch_id,
        "imported_at_utc": utc_now(),
        "source_filename": source.name,
        "source_file_sha256": source_sha,
        "conversations_member": source_member,
        "conversations_json_sha256": sha256_bytes(raw_json),
        "source_copied_into_vault": bool(args.copy_source),
        "copied_source_path": copied_path,
        "conversation_count": len(manifest_rows),
        "visible_message_count": message_total,
        "mapping_node_count": branch_node_total,
        "included_roles": sorted(allowed_roles),
        "raw_publication_status": "PRIVATE_ONLY_DO_NOT_PUBLISH",
        "workspace_assignment_status": "UNASSIGNED_REVIEW_REQUIRED",
    }
    atomic_write_json(batch_dir / "manifest.json", manifest)
    return {
        "status": "IMPORTED_PRIVATE_ONLY",
        "batch_id": batch_id,
        "batch_path": str(batch_dir),
        "conversation_count": len(manifest_rows),
        "visible_message_count": message_total,
        "source_sha256": source_sha,
        "content_printed": False,
    }


def cmd_public_summary(args: argparse.Namespace) -> dict[str, Any]:
    vault = resolve_vault(args.vault, create=False)
    wdir, _ = require_workspace(vault, args.workspace_id)
    state = load_json(wdir / "state.json")
    summary = state.get("public_summary")
    if not isinstance(summary, dict):
        raise PersistenceError(
            "No public_summary object is approved in state.json; refusing export."
        )
    output = Path(args.output).expanduser().resolve()
    if is_within(output, vault):
        raise PersistenceError("Public summary output should not be written inside the private vault.")
    export = {
        "schema": "por-derecho.public-workspace-checkpoint.v1",
        "workspace_id": args.workspace_id,
        "generated_at_utc": utc_now(),
        "source_event_hash": state.get("last_event_hash"),
        "summary": summary,
        "boundary": "This is an expressly approved public-safe derivative, not the raw workspace event stream.",
    }
    atomic_write_json(output, export, mode=0o644)
    return {
        "status": "PUBLIC_SUMMARY_EXPORTED",
        "workspace_id": args.workspace_id,
        "output": str(output),
        "source_event_hash": state.get("last_event_hash"),
    }


def cmd_doctor(args: argparse.Namespace) -> dict[str, Any]:
    vault = resolve_vault(args.vault)
    marker = load_json(vault / ".pd-private-workspace-vault")
    return {
        "status": "PASS",
        "python": sys.version.split()[0],
        "vault": str(vault),
        "vault_outside_public_repo": not is_within(vault, ROOT),
        "marker_schema": marker.get("schema"),
        "note": "No OpenAI API key or GitHub token was read or required.",
    }


def cmd_validate_repository(args: argparse.Namespace) -> dict[str, Any]:
    errors: list[str] = []
    for rel in REQUIRED_REPOSITORY_PATHS:
        if not (ROOT / rel).is_file():
            errors.append(f"missing repository control: {rel}")
    try:
        register = load_json(ROOT / "data/workspace-register-v1.json")
    except PersistenceError as exc:
        errors.append(str(exc))
        register = {}
    entries = register.get("workspaces", []) if isinstance(register, dict) else []
    if not isinstance(entries, list):
        errors.append("workspace register workspaces must be a list")
        entries = []
    seen: set[str] = set()
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            errors.append(f"workspace register row {index} must be an object")
            continue
        workspace_id = entry.get("workspace_id")
        try:
            validate_workspace_id(str(workspace_id))
        except PersistenceError as exc:
            errors.append(f"workspace register row {index}: {exc}")
            continue
        if workspace_id in seen:
            errors.append(f"duplicate workspace ID: {workspace_id}")
        seen.add(workspace_id)
        handoff = entry.get("handoff_path")
        if handoff and not (ROOT / str(handoff)).is_file():
            errors.append(f"{workspace_id}: missing handoff_path {handoff}")
    pointer_path = ROOT / "CURRENT_WORKSPACE_HANDOFF.md"
    if pointer_path.is_file():
        pointer = pointer_path.read_text(encoding="utf-8")
        match = re.search(r"\*\*Current workspace:\*\*\s*`(PD-WS-\d{8}-\d{4})`", pointer)
        if not match:
            errors.append("CURRENT_WORKSPACE_HANDOFF.md lacks a valid current workspace")
        elif match.group(1) not in seen:
            errors.append("current workspace pointer is not present in workspace register")
    gitignore_path = ROOT / ".gitignore"
    if gitignore_path.is_file():
        gitignore = gitignore_path.read_text(encoding="utf-8")
        for marker in REQUIRED_GITIGNORE_MARKERS:
            if marker not in gitignore:
                errors.append(f".gitignore missing private-workspace marker: {marker}")
    else:
        errors.append("missing .gitignore")
    forbidden_roots = [
        ROOT / ".workspace-vault",
        ROOT / ".pd-workspace-vault",
        ROOT / "private-workspaces",
        ROOT / "workspaces-private",
    ]
    for path in forbidden_roots:
        if path.exists():
            errors.append(f"private vault material exists inside public repository: {path.name}")
    result = {
        "schema": "por-derecho.workspace-persistence-repository-audit.v1",
        "status": "PASS" if not errors else "FAIL",
        "workspace_register_count": len(entries),
        "current_workspace_count": len(seen),
        "errors": errors,
        "operational_note": "Read-only repository audit; it does not inspect private vault contents.",
    }
    if args.output:
        output = (ROOT / args.output).resolve()
        atomic_write_json(output, result, mode=0o644)
    if errors:
        raise PersistenceError(json.dumps(result, ensure_ascii=False))
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Append-only private workspace persistence for Por Derecho."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Check private vault safety and runtime.")
    doctor.add_argument("--vault")
    doctor.set_defaults(func=cmd_doctor)

    init = sub.add_parser("init", help="Initialise or recover a private workspace.")
    init.add_argument("--vault")
    init.add_argument("--workspace-id")
    init.add_argument("--title", required=True)
    init.add_argument("--objective", default="")
    init.add_argument("--classification", default="PRIVATE_WORKSPACE")
    init.add_argument("--repository", default="sbu001monterecco/por-derecho")
    init.add_argument("--baseline", default="")
    init.add_argument("--thread-ref", action="append")
    init.add_argument("--resume", action="store_true")
    init.set_defaults(func=cmd_init)

    append = sub.add_parser("append", help="Append one immutable workspace event.")
    append.add_argument("--vault")
    append.add_argument("--workspace-id", required=True)
    append.add_argument("--event-type", required=True)
    append.add_argument("--summary", required=True)
    append.add_argument("--visibility", default="PRIVATE_WORKSPACE")
    append.add_argument("--details-json")
    append.add_argument("--details-file")
    append.add_argument("--repository-ref", action="append")
    append.add_argument("--artifact-ref", action="append")
    append.add_argument("--source-ref", action="append")
    append.add_argument("--thread-ref", action="append")
    append.set_defaults(func=cmd_append)

    checkpoint = sub.add_parser(
        "checkpoint", help="Append a checkpoint and regenerate state/handoff."
    )
    checkpoint.add_argument("--vault")
    checkpoint.add_argument("--workspace-id", required=True)
    checkpoint.add_argument("--payload", help="Checkpoint JSON file.")
    checkpoint.add_argument("--payload-json")
    checkpoint.add_argument("--summary")
    checkpoint.add_argument("--status", choices=sorted(WORKSPACE_STATUSES))
    checkpoint.add_argument("--objective")
    checkpoint.add_argument("--completed", action="append")
    checkpoint.add_argument("--open-task", action="append")
    checkpoint.add_argument("--next-action", action="append")
    checkpoint.add_argument("--do-not-infer", action="append")
    checkpoint.add_argument("--repository-baseline")
    checkpoint.add_argument("--repository-ref", action="append")
    checkpoint.add_argument("--visibility", default="PRIVATE_WORKSPACE")
    checkpoint.set_defaults(func=cmd_checkpoint)

    validate = sub.add_parser("validate", help="Validate private workspace event chains.")
    validate.add_argument("--vault")
    validate.add_argument("--workspace-id")
    validate.set_defaults(func=cmd_validate)

    importer = sub.add_parser(
        "import-chatgpt",
        help="Privately normalise an authorised ChatGPT export without publishing it.",
    )
    importer.add_argument("--vault")
    importer.add_argument("--source", required=True)
    importer.add_argument("--batch-id")
    importer.add_argument("--include-system", action="store_true")
    importer.add_argument("--copy-source", action="store_true")
    importer.set_defaults(func=cmd_import_chatgpt)

    public = sub.add_parser(
        "public-summary",
        help="Export only an expressly approved public_summary from private state.",
    )
    public.add_argument("--vault")
    public.add_argument("--workspace-id", required=True)
    public.add_argument("--output", required=True)
    public.set_defaults(func=cmd_public_summary)

    audit = sub.add_parser(
        "validate-repository",
        help="Audit public repository persistence controls and privacy guardrails.",
    )
    audit.add_argument("--output")
    audit.set_defaults(func=cmd_validate_repository)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.func(args)
    except PersistenceError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

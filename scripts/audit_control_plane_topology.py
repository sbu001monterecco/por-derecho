#!/usr/bin/env python3
"""Emit a public-safe, advisory topology census for GitHub and GitLab CI.

The report measures configuration fan-out and repeated validator entry points. It
does not classify legal content, read secrets, change CI semantics, or authorize
skipping an existing required job.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


SCHEMA = "por-derecho.control-plane-topology-shadow.v1"
HEX40 = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)
PYTHON_ENTRY = re.compile(r"\bpython(?:3)?\s+([^\s'\"]+\.py)\b")
USES = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)", re.MULTILINE)
LOCAL_INCLUDE = re.compile(r"^\s*-\s*local:\s*['\"]?([^'\"\s]+)", re.MULTILINE)
TOP_LEVEL_KEY = re.compile(r"^([A-Za-z0-9_.-]+):\s*$", re.MULTILINE)
RESERVED_GITLAB_KEYS = {
    "include", "stages", "workflow", "default", "variables", "image",
    "services", "cache", "before_script", "after_script", "pages",
}


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _head(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except FileNotFoundError:
        return None
    value = result.stdout.strip()
    return value if result.returncode == 0 and HEX40.fullmatch(value) else None


def _action_ref_is_pinned(use: str) -> bool:
    if use.startswith(("./", "docker://")):
        return True
    if "@" not in use:
        return False
    return bool(HEX40.fullmatch(use.rsplit("@", 1)[1]))


def audit_github(root: Path) -> dict:
    workflow_dir = root / ".github" / "workflows"
    files = sorted(workflow_dir.glob("*.yml")) + sorted(workflow_dir.glob("*.yaml"))
    files = sorted(set(files))
    commands: Counter[str] = Counter()
    action_uses: list[str] = []
    rows = []
    for path in files:
        text = _text(path)
        entries = PYTHON_ENTRY.findall(text)
        commands.update(entries)
        uses = USES.findall(text)
        action_uses.extend(uses)
        rows.append(
            {
                "path": path.relative_to(root).as_posix(),
                "sha256": _sha256(path),
                "has_pull_request": bool(re.search(r"^\s{0,2}pull_request:\s*", text, re.MULTILINE)),
                "has_push": bool(re.search(r"^\s{0,2}push:\s*", text, re.MULTILINE)),
                "mentions_main": bool(re.search(r"\bmain\b", text)),
                "has_schedule": bool(re.search(r"^\s{0,2}schedule:\s*", text, re.MULTILINE)),
                "has_workflow_call": bool(re.search(r"^\s{0,4}workflow_call:\s*", text, re.MULTILINE)),
            }
        )
    duplicate_commands = [
        {"entrypoint": name, "workflow_occurrences": count}
        for name, count in sorted(commands.items(), key=lambda item: (-item[1], item[0]))
        if count > 1
    ]
    unpinned = sorted({use for use in action_uses if not _action_ref_is_pinned(use)})
    return {
        "present": workflow_dir.is_dir(),
        "workflow_count": len(files),
        "pull_request_workflow_count": sum(row["has_pull_request"] for row in rows),
        "push_workflow_count": sum(row["has_push"] for row in rows),
        "push_workflows_mentioning_main": sum(row["has_push"] and row["mentions_main"] for row in rows),
        "scheduled_workflow_count": sum(row["has_schedule"] for row in rows),
        "reusable_workflow_count": sum(row["has_workflow_call"] for row in rows),
        "action_use_count": len(action_uses),
        "unpinned_external_action_uses": unpinned,
        "repeated_python_entrypoints": duplicate_commands,
        "files": rows,
    }


def _gitlab_files(root: Path) -> list[Path]:
    first = root / ".gitlab-ci.yml"
    if not first.is_file():
        return []
    ordered = [first]
    seen = {first.resolve()}
    index = 0
    while index < len(ordered):
        current = ordered[index]
        index += 1
        for rel in LOCAL_INCLUDE.findall(_text(current)):
            candidate = (root / rel).resolve()
            if candidate.is_file() and candidate not in seen and candidate.is_relative_to(root.resolve()):
                seen.add(candidate)
                ordered.append(candidate)
    return ordered


def audit_gitlab(root: Path) -> dict:
    files = _gitlab_files(root)
    commands: Counter[str] = Counter()
    rows = []
    job_names: set[str] = set()
    manual = allow_failure = artifact_blocks = 0
    for path in files:
        text = _text(path)
        commands.update(PYTHON_ENTRY.findall(text))
        keys = [key for key in TOP_LEVEL_KEY.findall(text) if key not in RESERVED_GITLAB_KEYS and not key.startswith(".")]
        job_names.update(keys)
        manual += len(re.findall(r"^\s+when:\s*manual\s*$", text, re.MULTILINE))
        allow_failure += len(re.findall(r"^\s+allow_failure:\s*true\s*$", text, re.MULTILINE))
        artifact_blocks += len(re.findall(r"^\s+artifacts:\s*$", text, re.MULTILINE))
        rows.append({"path": path.relative_to(root).as_posix(), "sha256": _sha256(path)})
    duplicate_commands = [
        {"entrypoint": name, "job_occurrences": count}
        for name, count in sorted(commands.items(), key=lambda item: (-item[1], item[0]))
        if count > 1
    ]
    return {
        "present": bool(files),
        "config_file_count": len(files),
        "top_level_job_count": len(job_names),
        "manual_job_markers": manual,
        "allow_failure_markers": allow_failure,
        "artifact_blocks": artifact_blocks,
        "repeated_python_entrypoints": duplicate_commands,
        "files": rows,
    }


def build_report(root: Path) -> dict:
    return {
        "schema": SCHEMA,
        "mode": "SHADOW_ADVISORY_ONLY",
        "repository_head": _head(root),
        "github": audit_github(root),
        "gitlab": audit_gitlab(root),
        "invariants": {
            "may_skip_existing_required_jobs": False,
            "changes_release_semantics": False,
            "reads_credentials_or_private_evidence": False,
            "public_safe_aggregate_only": True,
        },
        "interpretation": [
            "Counts describe the checked-out tree only and are not platform-settings evidence.",
            "Repeated entry points are consolidation candidates, not proof that workflows are equivalent.",
            "No workflow or job may be retired until dependency, changed-path, failure and live-readback behavior are compared.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    report = build_report(root)
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

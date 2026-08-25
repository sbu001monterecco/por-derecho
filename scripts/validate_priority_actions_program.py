#!/usr/bin/env python3
"""Validate the repository priority-actions execution programme.

This validator is deliberately dependency-free. It verifies the machine record,
its task graph, referenced controls/templates, and the minimum safety invariants
needed for future threads to execute the programme without relying on chat.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "ops" / "priority-actions" / "program-v1.json"
SCHEMA = ROOT / "ops" / "priority-actions" / "program-v1.schema.json"
README = ROOT / "ops" / "priority-actions" / "README.md"
PROMPT = ROOT / "ops" / "priority-actions" / "FUTURE_THREAD_EXECUTION_PROMPT.md"
HANDOVER = ROOT / "CURRENT_PRIORITY_ACTIONS_HANDOVER_25AUG2026.md"

ALLOWED_STATES = {
    "PLANNED",
    "READY",
    "IN_PROGRESS",
    "BLOCKED",
    "REVIEW",
    "COMPLETE",
}
ALLOWED_PRIORITIES = {"P0", "P1", "P2"}
TASK_ID = re.compile(r"^(P[0-2])-[A-Z]+-[0-9]{2}$")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_TASK_IDS = {
    "P0-OPS-01",
    "P0-PRIV-01",
    "P0-TX-01",
    "P0-FIN-01",
    "P0-REC-01",
    "P1-ONA-01",
    "P1-PR-01",
    "P1-WEB-01",
    "P1-RUNTIME-01",
    "P2-TX-WS-01",
}
REQUIRED_TEMPLATES = {
    "ops/priority-actions/templates/release-state-register.template.json",
    "ops/priority-actions/templates/public-private-remediation-inventory.template.csv",
    "ops/priority-actions/templates/private-mailbox-requery-checklist.md",
    "ops/priority-actions/templates/financing-playbook-public-safe.template.csv",
    "ops/priority-actions/templates/recovery-denominator.template.csv",
    "ops/priority-actions/templates/pr-triage.template.csv",
    "ops/priority-actions/templates/ona-discovery-work-order.md",
    "ops/priority-actions/templates/reader-journey-route-map.template.csv",
    "ops/priority-actions/templates/runtime-module-manifest.template.json",
    "ops/priority-actions/templates/private-transaction-workspace-charter.md",
}


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        errors.append(f"missing JSON file: {path.relative_to(ROOT)}")
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostic path
        errors.append(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"top level must be object: {path.relative_to(ROOT)}")
        return {}
    return data


def require_file(rel: str, errors: list[str]) -> None:
    if not (ROOT / rel).is_file():
        errors.append(f"referenced file does not exist: {rel}")


def validate_program(data: dict[str, Any], errors: list[str]) -> None:
    if data.get("schema") != "por-derecho.priority-actions.v1":
        errors.append("program schema must be por-derecho.priority-actions.v1")

    sha = data.get("prepared_from_main")
    if not isinstance(sha, str) or not SHA40.fullmatch(sha):
        errors.append("prepared_from_main must be a lowercase 40-character SHA")

    if data.get("refresh_main_before_execution") is not True:
        errors.append("refresh_main_before_execution must be true")

    states = data.get("state_machine")
    if not isinstance(states, list) or set(states) != ALLOWED_STATES:
        errors.append("state_machine must contain the six controlled states exactly")

    global_controls = data.get("global_controls")
    if not isinstance(global_controls, list) or not global_controls:
        errors.append("global_controls must be a non-empty list")
    else:
        for rel in global_controls:
            if not isinstance(rel, str):
                errors.append("global control entries must be strings")
                continue
            require_file(rel, errors)

    tasks = data.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        errors.append("tasks must be a non-empty list")
        return

    ids: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    templates: set[str] = set()

    required_fields = {
        "id",
        "priority",
        "title",
        "state",
        "track",
        "privacy",
        "objective",
        "dependencies",
        "source_controls",
        "template",
        "suggested_branch",
        "allowed_actions",
        "prohibited_actions",
        "expected_outputs",
        "acceptance_criteria",
        "authority_gate",
        "next_action",
    }

    for index, task in enumerate(tasks):
        label = f"tasks[{index}]"
        if not isinstance(task, dict):
            errors.append(f"{label} must be an object")
            continue
        missing = sorted(required_fields - set(task))
        if missing:
            errors.append(f"{label} missing fields: {', '.join(missing)}")
            continue

        task_id = task.get("id")
        if not isinstance(task_id, str) or not TASK_ID.fullmatch(task_id):
            errors.append(f"{label}.id is invalid: {task_id!r}")
            continue
        ids.append(task_id)
        by_id[task_id] = task

        priority = task.get("priority")
        if priority not in ALLOWED_PRIORITIES:
            errors.append(f"{task_id}: invalid priority {priority!r}")
        elif not task_id.startswith(f"{priority}-"):
            errors.append(f"{task_id}: priority does not match task ID")

        if task.get("state") not in ALLOWED_STATES:
            errors.append(f"{task_id}: invalid state {task.get('state')!r}")

        for field in (
            "title",
            "track",
            "privacy",
            "objective",
            "template",
            "suggested_branch",
            "authority_gate",
            "next_action",
        ):
            value = task.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{task_id}: {field} must be a non-empty string")

        for field in (
            "dependencies",
            "source_controls",
            "allowed_actions",
            "prohibited_actions",
            "expected_outputs",
            "acceptance_criteria",
        ):
            value = task.get(field)
            if not isinstance(value, list):
                errors.append(f"{task_id}: {field} must be a list")
                continue
            if field != "dependencies" and not value:
                errors.append(f"{task_id}: {field} must not be empty")
            if any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(f"{task_id}: {field} entries must be non-empty strings")

        template = task.get("template")
        if isinstance(template, str):
            if not template.startswith("ops/priority-actions/templates/"):
                errors.append(f"{task_id}: template must be under ops/priority-actions/templates")
            else:
                templates.add(template)
                require_file(template, errors)

        # Source controls that are repository paths must exist. Descriptive
        # references such as "PR #1016 compare and patches" are intentionally
        # allowed and are not treated as paths.
        for control in task.get("source_controls", []):
            if isinstance(control, str) and "/" in control and not control.startswith("PR #"):
                require_file(control, errors)

        prohibited = " ".join(task.get("prohibited_actions", [])).lower()
        if "send" not in prohibited and task_id == "P0-TX-01":
            errors.append("P0-TX-01: read-only mailbox task must explicitly prohibit sending")

    if len(ids) != len(set(ids)):
        errors.append("task IDs must be unique")

    missing_required = REQUIRED_TASK_IDS - set(ids)
    unexpected = set(ids) - REQUIRED_TASK_IDS
    if missing_required:
        errors.append(f"missing required task IDs: {sorted(missing_required)}")
    if unexpected:
        errors.append(f"unexpected task IDs: {sorted(unexpected)}")

    for task_id, task in by_id.items():
        for dep in task.get("dependencies", []):
            if dep == task_id:
                errors.append(f"{task_id}: task cannot depend on itself")
            elif dep not in by_id:
                errors.append(f"{task_id}: unknown dependency {dep}")

    if templates != REQUIRED_TEMPLATES:
        errors.append(
            "template set mismatch: "
            f"missing={sorted(REQUIRED_TEMPLATES - templates)} "
            f"unexpected={sorted(templates - REQUIRED_TEMPLATES)}"
        )

    parallel = data.get("parallelisation")
    if not isinstance(parallel, dict):
        errors.append("parallelisation must be an object")
    else:
        public_lane = parallel.get("repository_public_lane")
        private_lane = parallel.get("private_read_only_lane")
        if not isinstance(public_lane, list) or not isinstance(private_lane, list):
            errors.append("parallelisation lanes must be lists")
        else:
            lane_ids = public_lane + private_lane
            if set(lane_ids) != set(ids):
                errors.append("parallelisation lanes must cover every task exactly once")
            if len(lane_ids) != len(set(lane_ids)):
                errors.append("parallelisation lanes must not duplicate task IDs")
        if parallel.get("same_path_parallel_edits_prohibited") is not True:
            errors.append("same_path_parallel_edits_prohibited must be true")


def validate_supporting_files(errors: list[str]) -> None:
    for path in (SCHEMA, README, PROMPT, HANDOVER):
        if not path.is_file():
            errors.append(f"missing supporting file: {path.relative_to(ROOT)}")

    # Ensure JSON templates are syntactically valid.
    for rel in (
        "ops/priority-actions/templates/release-state-register.template.json",
        "ops/priority-actions/templates/runtime-module-manifest.template.json",
        "ops/priority-actions/program-v1.schema.json",
    ):
        load_json(ROOT / rel, errors)


def main() -> int:
    errors: list[str] = []
    data = load_json(PROGRAM, errors)
    validate_supporting_files(errors)
    if data:
        validate_program(data, errors)

    if errors:
        print("PRIORITY ACTIONS PROGRAMME: FAIL")
        for item in errors:
            print(f" - {item}")
        return 1

    print(
        "PRIORITY ACTIONS PROGRAMME: PASS "
        f"({len(data['tasks'])} tasks; baseline {data['prepared_from_main']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

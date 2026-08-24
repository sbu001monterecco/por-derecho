#!/usr/bin/env python3
"""Fail closed on Por Derecho content loss and preservation-lock regression."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "ops" / "REPOSITORY_PRESERVATION_CONTRACT.json"


def add(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        add(errors, f"{path.relative_to(ROOT)}: invalid or missing JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        add(errors, f"{path.relative_to(ROOT)}: root must be an object")
        return {}
    return data


def tracked_files(errors: list[str]) -> list[str]:
    try:
        output = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    except Exception as exc:
        add(errors, f"cannot enumerate tracked files: {exc}")
        return []
    return [line for line in output.splitlines() if line]


def comparison_revisions(errors: list[str]) -> tuple[str, str, bool] | None:
    """Return base/head and whether the comparison is a CI commit-only diff.

    CI supplies immutable endpoints.  Local runs deliberately compare the current
    index/worktree with ``origin/main`` so an uncommitted deletion cannot obtain a
    misleading PASS.
    """

    base = os.getenv("GITHUB_BASE_SHA", "").strip()
    head = os.getenv("GITHUB_HEAD_SHA", "HEAD").strip() or "HEAD"
    if base and set(base) != {"0"}:
        return base, head, True
    try:
        base = subprocess.check_output(
            ["git", "rev-parse", "--verify", "origin/main"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()
    except Exception as exc:
        add(errors, f"cannot establish local preservation base origin/main: {exc}")
        return None
    return base, "HEAD", False


def diff_name_status(
    errors: list[str], *, include_renames: bool = False
) -> tuple[list[str], str, bool]:
    comparison = comparison_revisions(errors)
    if comparison is None:
        return [], "", False
    base, head, commit_only = comparison
    command = ["git", "diff", "--name-status"]
    if include_renames:
        command.append("--find-renames")
    # A two-endpoint diff is intentional. Branch freshness is checked separately;
    # a three-dot diff could hide base-side changes and weaken the deletion gate.
    command.extend([base, head] if commit_only else [base])
    try:
        output = subprocess.check_output(
            command,
            cwd=ROOT,
            text=True,
            stderr=subprocess.STDOUT,
        )
    except Exception as exc:
        add(errors, f"cannot compare preservation base {base} with {head}: {exc}")
        return [], base, commit_only
    return output.splitlines(), base, commit_only


def changed_entries(errors: list[str]) -> list[tuple[str, str, str | None]]:
    lines, _base, _commit_only = diff_name_status(errors, include_renames=True)
    entries: list[tuple[str, str, str | None]] = []
    for line in lines:
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("R") and len(parts) == 3:
            entries.append(("R", parts[1], parts[2]))
        elif status == "D" and len(parts) == 2:
            entries.append(("D", parts[1], None))
    return entries


def added_files(errors: list[str]) -> set[str]:
    lines, _base, commit_only = diff_name_status(errors)
    added: set[str] = set()
    for line in lines:
        parts = line.split("\t")
        if len(parts) == 2 and parts[0] == "A":
            added.add(parts[1])
    if not commit_only:
        try:
            untracked = subprocess.check_output(
                ["git", "ls-files", "--others", "--exclude-standard"],
                cwd=ROOT,
                text=True,
                stderr=subprocess.STDOUT,
            )
            added.update(line for line in untracked.splitlines() if line)
        except Exception as exc:
            add(errors, f"cannot enumerate local untracked authorization records: {exc}")
    return added


def validate_branch_freshness(errors: list[str]) -> None:
    comparison = comparison_revisions(errors)
    if comparison is None:
        return
    base, head, _commit_only = comparison
    try:
        merge_base = subprocess.check_output(
            ["git", "merge-base", base, head], cwd=ROOT, text=True, stderr=subprocess.STDOUT
        ).strip()
    except Exception as exc:
        add(errors, f"cannot prove branch freshness against {base}: {exc}")
        return
    if merge_base != base:
        add(errors, f"stale branch blocked: current base {base} is not an ancestor of proposed head {head}")


def authorization_paths(contract: dict, errors: list[str]) -> set[str]:
    control = contract.get("deletion_control", {})
    directory = ROOT / str(control.get("authorization_directory", ""))
    authorized: set[str] = set()
    if not directory.is_dir():
        add(errors, f"authorization directory missing: {directory.relative_to(ROOT)}")
        return authorized
    comparison = comparison_revisions(errors)
    base = comparison[0] if comparison else ""
    eligible = added_files(errors)
    seen_ids: set[str] = set()
    for path in sorted(directory.glob("*.json")):
        rel = str(path.relative_to(ROOT))
        if rel not in eligible:
            continue
        data = load_json(path, errors)
        if data.get("status") != control.get("authorization_status"):
            add(errors, f"{path.relative_to(ROOT)}: authorization status mismatch")
            continue
        if data.get("authorized_by") != control.get("authorized_by"):
            add(errors, f"{path.relative_to(ROOT)}: authorized_by mismatch")
            continue
        for key in ("authorization_id", "change_id", "base_sha", "authorized_on", "reason", "paths"):
            if not data.get(key):
                add(errors, f"{path.relative_to(ROOT)}: missing {key}")
        authorization_id = data.get("authorization_id")
        if isinstance(authorization_id, str):
            if authorization_id in seen_ids:
                add(errors, f"{path.relative_to(ROOT)}: duplicate authorization_id {authorization_id}")
            seen_ids.add(authorization_id)
        if base and data.get("base_sha") != base:
            add(errors, f"{path.relative_to(ROOT)}: base_sha does not match this change")
        paths = data.get("paths", [])
        if isinstance(paths, list):
            authorized.update(item for item in paths if isinstance(item, str))
    return authorized


def protected(path: str, contract: dict) -> bool:
    control = contract.get("deletion_control", {})
    return path in control.get("protected_exact_files", []) or any(
        path.startswith(prefix) for prefix in control.get("protected_prefixes", [])
    )


def validate_deletions(contract: dict, errors: list[str]) -> None:
    authorized = authorization_paths(contract, errors)
    for status, old, new in changed_entries(errors):
        if protected(old, contract) and old not in authorized:
            suffix = f" -> {new}" if new else ""
            add(
                errors,
                f"unapproved protected-path {'rename' if status == 'R' else 'deletion'}: {old}{suffix}",
            )


def validate_inventory(contract: dict, errors: list[str]) -> dict[str, int]:
    files = tracked_files(errors)
    counts = {
        "tracked_files": len(files),
        "bilingual_html_pages": sum(
            path.endswith(".html") and path.startswith(("es/", "en/")) for path in files
        ),
        "asset_files": sum(path.startswith("assets/") for path in files),
        "archive_files": sum(path.startswith("archive/") for path in files),
        "evidence_files": sum(path.startswith("evidence/") for path in files),
    }
    for key, minimum in contract.get("baseline_minimums", {}).items():
        if counts.get(key, 0) < int(minimum):
            add(errors, f"repository inventory shrank below baseline: {key}={counts.get(key, 0)} < {minimum}")
    return counts


def validate_five_actor_lock(contract: dict, errors: list[str]) -> None:
    lock = contract.get("five_actor_front_page_lock", {})
    private = lock.get("private_actors", [])
    institutions = lock.get("institutional_roles", {})
    administrator = institutions.get("insolvency_administrator", {}).get("name")
    judge = institutions.get("magistrate_judge", {}).get("name")

    required = list(lock.get("required_source_files", []))
    required += list(lock.get("homepages", []))
    required += list(lock.get("direct_routes", {}).get("es", []))
    required += list(lock.get("direct_routes", {}).get("en", []))
    required += list(lock.get("legacy_direct_routes", []))
    for rel in required:
        if not (ROOT / rel).is_file():
            add(errors, f"preservation-contract file missing: {rel}")

    expected = lock.get("required_homepage_structure", {})
    for rel in lock.get("homepages", []):
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        markers = [
            f'data-pd-five-ac="{lock.get("component_marker")}"',
            f'data-five-actor-front-page-lock="{lock.get("authorization_marker")}"',
            'data-five-actor-accountability-static="true"',
            'data-key-direct-route-presentation="front-page"',
            *private,
            administrator,
            judge,
        ]
        for marker in markers:
            if marker and marker not in text:
                add(errors, f"{rel}: locked homepage marker missing: {marker}")
        for marker, key in (
            ("data-private-actor-card=", "private_actor_cards"),
            ("data-institution-card=", "institutional_cards"),
            ("data-linkage-row", "linkage_rows"),
        ):
            actual = text.count(marker)
            wanted = int(expected.get(key, 0))
            if actual != wanted:
                add(errors, f"{rel}: {key}={actual}; expected {wanted}")

    direct_routes = (
        lock.get("direct_routes", {}).get("es", [])
        + lock.get("direct_routes", {}).get("en", [])
        + lock.get("legacy_direct_routes", [])
    )
    for rel in direct_routes:
        path = ROOT / rel
        if path.is_file() and "site.js?v=20260824d" not in path.read_text(encoding="utf-8"):
            add(errors, f"{rel}: protected direct-route loader missing")

    module_path = ROOT / "assets" / "homepage-actor-family-pwc-note-20260819.js"
    if module_path.is_file():
        module = module_path.read_text(encoding="utf-8")
        for marker in [
            "section.dataset.fiveActorFrontPageLock = 'express-authorization-required'",
            "data-private-actor-card",
            "data-private-actor-id",
            "data-institution-card",
            "data-linkage-row",
            "data-linkage-actor-id",
            "section.dataset.directRouteFirstReadPin = '20260824d'",
            "isCanonical",
            "isPwc",
            "isRicpe",
            "isAc",
            "isCourt",
            "isTakeover",
            "isAccountability",
            "concurso-36-2012-magistrado-juez/",
            *private,
            administrator,
            judge,
        ]:
            if marker and marker not in module:
                add(errors, f"five-actor runtime contract missing: {marker}")


def validate_governance_links(errors: list[str]) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for marker in ("AGENTS.md", "ops/REPOSITORY_PRESERVATION_CONTRACT.json"):
        if marker not in readme:
            add(errors, f"README.md does not surface {marker}")
    for marker in (
        "current remote `main`",
        "express authorization",
        "Laura Patricia Acosta Matos",
        "Francisco de Borja Rodríguez-Batllori Laffitte",
        "Alberto López Villarrubia",
        "validate_repository_preservation.py",
    ):
        if marker not in agents:
            add(errors, f"AGENTS.md missing stewardship rule marker: {marker}")


def main() -> int:
    errors: list[str] = []
    contract = load_json(CONTRACT_PATH, errors)
    if contract.get("schema_version") != 1:
        add(errors, "preservation contract schema_version must be 1")
    validate_branch_freshness(errors)
    validate_deletions(contract, errors)
    counts = validate_inventory(contract, errors)
    validate_five_actor_lock(contract, errors)
    validate_governance_links(errors)
    if errors:
        print("REPOSITORY PRESERVATION GATE: FAIL")
        for item in errors:
            print(f" - {item}")
        return 1
    print(
        "REPOSITORY PRESERVATION GATE: PASS "
        f"({counts['tracked_files']} tracked files; {counts['bilingual_html_pages']} bilingual HTML pages; "
        "two homepages + fourteen canonical direct routes + one preserved legacy route locked)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

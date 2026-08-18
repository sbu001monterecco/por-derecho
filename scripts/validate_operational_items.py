#!/usr/bin/env python3
"""Validate the Por Derecho operational control plane.

Open work is allowed. Forgotten, unowned, untracked, stale or falsely closed work is not.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "operations" / "open-operational-items.json"
VALID_STATUSES = {"OPEN", "BLOCKED", "WAITING_EXTERNAL", "MONITORING", "CLOSED"}
VALID_SEVERITIES = {"P0", "P1", "P2", "P3"}
BLOCK_KEYS = {"publication", "repository_hardening", "security_assurance", "deletion_safety"}
ID_RE = re.compile(r"^OPS-\d{4}-\d{3}$")


def parse_iso_day(value: object, label: str, errors: list[str]) -> date | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: missing ISO date")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label}: invalid ISO date {value!r}")
        return None


def main() -> int:
    errors: list[str] = []
    if not REGISTRY.is_file():
        print("OPERATIONAL INTEGRITY GATE: FAIL")
        print(" - operations/open-operational-items.json is missing")
        return 1

    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception as exc:
        print("OPERATIONAL INTEGRITY GATE: FAIL")
        print(f" - invalid JSON: {exc}")
        return 1

    if data.get("registry_version") != 1:
        errors.append("registry_version must be 1")
    if not data.get("owner"):
        errors.append("registry owner is required")
    parse_iso_day(data.get("as_of"), "registry.as_of", errors)

    items = data.get("items")
    if not isinstance(items, list) or not items:
        errors.append("items must be a non-empty array")
        items = []

    seen: set[str] = set()
    today = date.today()

    for index, item in enumerate(items):
        prefix = f"items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: item must be an object")
            continue

        item_id = item.get("id")
        if not isinstance(item_id, str) or not ID_RE.match(item_id):
            errors.append(f"{prefix}: invalid id {item_id!r}")
            item_id = prefix
        elif item_id in seen:
            errors.append(f"{item_id}: duplicate id")
        else:
            seen.add(item_id)

        for field in ("title", "owner", "next_action", "closure_test"):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{item_id}: {field} is required")

        severity = item.get("severity")
        if severity not in VALID_SEVERITIES:
            errors.append(f"{item_id}: invalid severity {severity!r}")

        status = item.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"{item_id}: invalid status {status!r}")

        last_verified = parse_iso_day(item.get("last_verified_at"), f"{item_id}.last_verified_at", errors)
        review_by = parse_iso_day(item.get("review_by"), f"{item_id}.review_by", errors)
        if last_verified and review_by and review_by < last_verified:
            errors.append(f"{item_id}: review_by precedes last_verified_at")
        if status != "CLOSED" and review_by and review_by < today:
            errors.append(
                f"{item_id}: review is stale (review_by={review_by.isoformat()}, today={today.isoformat()}); refresh status/evidence before merge"
            )

        tracking = item.get("tracking")
        if not isinstance(tracking, dict) or not tracking:
            errors.append(f"{item_id}: tracking must be a non-empty object")

        evidence = item.get("evidence")
        if not isinstance(evidence, list) or not evidence or not all(isinstance(v, str) and v.strip() for v in evidence):
            errors.append(f"{item_id}: evidence must be a non-empty string array")

        blocks = item.get("blocks")
        if not isinstance(blocks, dict):
            errors.append(f"{item_id}: blocks must be an object")
            blocks = {}
        else:
            if set(blocks) != BLOCK_KEYS:
                errors.append(f"{item_id}: blocks must contain exactly {sorted(BLOCK_KEYS)}")
            for key in BLOCK_KEYS:
                if key in blocks and not isinstance(blocks[key], bool):
                    errors.append(f"{item_id}: blocks.{key} must be boolean")

        closure_evidence = item.get("closure_evidence")
        if status == "CLOSED" and (not isinstance(closure_evidence, list) or not closure_evidence):
            errors.append(f"{item_id}: CLOSED requires closure_evidence")

        if status == "BLOCKED" and not any(bool(blocks.get(key)) for key in BLOCK_KEYS):
            errors.append(f"{item_id}: BLOCKED item must declare at least one blocking dimension")

    if errors:
        print("OPERATIONAL INTEGRITY GATE: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1

    active = sum(1 for item in items if item.get("status") != "CLOSED")
    blocking = sum(
        1
        for item in items
        if isinstance(item.get("blocks"), dict) and any(item["blocks"].values())
    )
    print(f"OPERATIONAL INTEGRITY GATE: PASS ({len(items)} items; {active} non-closed; {blocking} with blocking dimensions)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

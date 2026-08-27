#!/usr/bin/env python3
"""Validate the current unitary repository/website reverse-engineered digest."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "CURRENT_REVERSE_ENGINEERED_DIGEST.md"
STATE = ROOT / "ops" / "CURRENT_REVERSE_ENGINEERED_DIGEST.json"
MANIFEST = ROOT / "publication-manifests" / "unitary-repository-website-redigest-20260827.json"

required_markers = [
    "PD-UNITARY-REDIGEST-20260827-01",
    "Sun Park was one economically integrated hotel platform",
    "PP 1041 is the cleanest finite production demand",
    "19 / 24 confirmed",
    "superseded",
    "33 pull requests",
    "required-status-check enforcement was off",
    "CEXP succession",
    "single-satisfaction credit ledger",
]

text = MD.read_text(encoding="utf-8")
missing = [marker for marker in required_markers if marker not in text]
if missing:
    raise SystemExit(f"Missing digest markers: {missing}")

state = json.loads(STATE.read_text(encoding="utf-8"))
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

assert state["control_id"] == "PD-UNITARY-REDIGEST-20260827-01"
assert state["status"] in {
    "REPOSITORY_CONTROLLED_PUBLIC_SAFE",
    "LIVE_VERIFIED_PUBLIC_CONTROL",
}
assert state["source_base"]["main_sha"] == "8e8e83c5a337846245a942222efbc3120645b1fd"
assert state["identity_registry"] == {
    "total": 194,
    "PERSON": 86,
    "ORGANISATION": 66,
    "STRUCTURE": 10,
    "INSTITUTION": 15,
    "PROCEEDING": 17,
    "archive_backfill": "OPEN",
}
assert state["caret_scope"]["confirmed"] == 19
assert state["caret_scope"]["denominator"] == 24
assert state["caret_scope"]["pending"] == 5
assert state["caret_scope"]["old_local_24_of_24_package"] == "SUPERSEDED_NOT_MERGEABLE_AS_IS"
assert state["source_base"]["open_pull_requests"] == 33
assert state["source_base"]["required_status_check_enforcement"] == "off"

assert manifest["control_id"] == state["control_id"]
assert manifest["current_state"] in {"REPOSITORY_CONTROLLED", "LIVE_VERIFIED"}
assert manifest["reader_facing_material_update"] is False
assert manifest["material_date_change"] is False
assert manifest["identity_registry"] == state["identity_registry"]
assert manifest["caret_scope"] == state["caret_scope"]
assert len(manifest["live_urls"]) == 3

print("CURRENT REVERSE-ENGINEERED DIGEST: PASS")
print(" - control:", state["control_id"])
print(" - source base:", state["source_base"]["main_sha"])
print(" - identity denominator: 194 / 86 / 66 / 10 / 15 / 17")
print(" - caret scope: 19/24; old 24/24 package superseded")
print(" - public material date intentionally unchanged")

#!/usr/bin/env python3
"""Validate source-level P0 gap closure states for Concurso 36/2012."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/concurso36-p0-material-gap-closure-20260829-v1.json"
MAP = ROOT / "archive/CONCURSO36_P0_MATERIAL_GAP_CLOSURE_MAP_29AUG2026.md"
CONTINUE = ROOT / "CONCURSO36_CONTINUE_HERE.md"

EXPECTED_IDS = {
    "CERTIFIED-DENOMINATOR",
    "ORIGINALS-2014-2016",
    "BARE-REFERENCES",
    "REPORTED-JUDICIAL-ACTS",
    "OCTOBER-2021-CHAIN",
    "AC-REPORT-SERIES",
    "REVIEW-2022-2023",
    "CURRENT-APPEALS",
    "FINAL-STAGE",
}
ALLOWED = {
    "OPEN_UNLOCATED",
    "PRIMARY_LOCATED_PENDING_PROMOTION",
    "PARTIAL_FAMILY_LOCATED",
    "DISCOVERY_DENOMINATOR_LOCATED__CERTIFIED_OPEN",
    "PARTIAL_PROCEDURAL_CHAIN_LOCATED__MERITS_OPEN",
    "OPEN_UNLOCATED_POST_LIQUIDATION",
    "CLOSED",
}

errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


try:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"FAIL: cannot load {DATA}: {exc}")
    raise SystemExit(1)

families = payload.get("families") or []
ids = [item.get("id") for item in families if isinstance(item, dict)]
check(payload.get("schema") == "por-derecho.concurso36-p0-material-gap-closure.v1", "schema mismatch")
check(payload.get("p0_open_family_count") == 9, "P0 denominator must remain nine")
check(payload.get("p1_open_family_count") == 2, "P1 denominator must remain two")
check(payload.get("new_allegation_promoted") is False, "control must not promote a new allegation")
check(payload.get("external_action_authorized") is False, "control must not authorize external action")
check(set(payload.get("status_enum") or []) == ALLOWED, "status enum drift")
check(len(families) == 9, "exactly nine P0 families required")
check(set(ids) == EXPECTED_IDS, "P0 family IDs changed")
check(len(ids) == len(set(ids)), "duplicate P0 family ID")

for family in families:
    if not isinstance(family, dict):
        errors.append("non-object family")
        continue
    ident = family.get("id")
    status = family.get("status")
    check(status in ALLOWED, f"{ident}: invalid status {status!r}")
    check(status != "CLOSED", f"{ident}: no P0 family is closed by this control")
    check(bool(family.get("remaining_nodes")), f"{ident}: remaining_nodes must stay explicit")
    check(isinstance(family.get("priority"), int), f"{ident}: integer priority required")

by_id = {item["id"]: item for item in families if isinstance(item, dict) and item.get("id")}
ac = by_id["AC-REPORT-SERIES"]
final_stage = by_id["FINAL-STAGE"]
check(ac["priority"] == 1, "AC report series must remain top priority")
check("15th quarterly liquidation report" in ac["remaining_nodes"], "15th report target missing from AC series")
check("recover and authenticate underlying quarterly report filed as 5367/2022" in ac["remaining_nodes"], "5367/2022 source target missing")
check(final_stage["priority"] == 1, "final stage must remain top priority")
check("15th quarterly liquidation report" in final_stage["remaining_nodes"], "15th report target missing from final stage")
check(by_id["CURRENT-APPEALS"].get("merits_endpoint_located_in_that_sweep") is False, "current appeals must not be upgraded without merits")

july = ac.get("july_2022_delivery_control") or {}
check(july.get("filing_registration") == "5367/2022", "July filing registration mismatch")
check(july.get("laj_receipt_date") == "2022-07-27", "July LAJ receipt date mismatch")
check(july.get("receipt_located") is True, "July LAJ receipt must remain located")
check(july.get("notification_identifies_quarterly_report") is True, "notification must continue to identify a quarterly report")
check(july.get("notification_contains_underlying_report") is False, "do not claim the recovered notification contains the underlying report")
check(july.get("underlying_primary_report_located_in_targeted_connected_source_sweep") is False, "do not upgrade July report recovery without the primary report")
check(july.get("ordinal_proved") is False, "July report ordinal remains unproved")
check(july.get("identity_with_15th_report_proved") is False, "identity with 15th report remains unproved")

ranking = payload.get("highest_leverage_targets") or []
check(len(ranking) >= 5, "material-target ranking incomplete")
if ranking:
    check(
        ranking[0].get("target") == "underlying 5367/2022 quarterly report plus 15th quarterly liquidation report plus complete AC report denominator",
        "rank 1 target changed",
    )

map_text = MAP.read_text(encoding="utf-8")
continue_text = CONTINUE.read_text(encoding="utf-8")
for marker in (
    "nine P0 families open",
    "15th quarterly liquidation report",
    "5367/2022",
    "does **not** contain the underlying quarterly report itself",
    "Do **not** equate 5367/2022 with the 15th report from chronology alone",
    "without pretending that a located subnode closes the family",
    "does not authorise email, filing, preservation request or authority contact",
):
    check(marker in map_text, f"closure map missing marker: {marker}")
for marker in (
    "archive/CONCURSO36_P0_MATERIAL_GAP_CLOSURE_MAP_29AUG2026.md",
    "assets/data/concurso36-p0-material-gap-closure-20260829-v1.json",
    "Open: nine P0 and two P1 families remain controlled",
    "15th quarterly liquidation report",
):
    check(marker in continue_text, f"restart pointer missing marker: {marker}")

privacy = payload.get("privacy_rule", "")
for marker in ("private mailbox identifiers", "contact data", "counsel advice", "privacy review", "canonical hashing"):
    check(marker in privacy, f"privacy rule missing marker: {marker}")

if errors:
    print(f"FAIL — Concurso 36/2012 P0 material-gap closure control ({len(errors)} errors)")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print("PASS — Concurso 36/2012 P0 material-gap closure control")
print(" - nine P0 families remain open")
print(" - 5367/2022 receipt is located but the underlying report remains unlocated")
print(" - no ordinal or identity with the 15th report is inferred")
print(" - source-level partial states are preserved without denominator reduction")
print(" - no new allegation or external action authority is introduced")

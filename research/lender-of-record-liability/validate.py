#!/usr/bin/env python3
"""Validate the Por Derecho lender-liability structured research layer.

Run from repository root:
    python research/lender-of-record-liability/validate.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

ALLOWED_STATUS = {
    "verified_primary",
    "verified_official",
    "documented_party_statement",
    "corroborated_inference",
    "contested",
    "missing_primary",
    "unknown",
}
ALLOWED_PUBLICATION = {
    "public_safe",
    "internal_only",
    "privilege_review",
    "do_not_publish",
}
ID_PATTERNS = {
    "sources.json": re.compile(r"^SRC-[A-Z0-9-]+$"),
    "actors.json": re.compile(r"^ACT-[A-Z0-9-]+$"),
    "instruments.json": re.compile(r"^INS-[A-Z0-9-]+$"),
    "transfers.json": re.compile(r"^TR-[A-Z0-9-]+$"),
    "knowledge-events.json": re.compile(r"^KN-[A-Z0-9-]+$"),
    "conduct-decisions.json": re.compile(r"^CD-[A-Z0-9-]+$"),
    "proceedings.json": re.compile(r"^PROC-[A-Z0-9-]+$"),
    "evidence-gaps.json": re.compile(r"^GAP-[A-Z0-9-]+$"),
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
UNSAFE_PATTERNS = [
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    re.compile(r"\b(?:\+34|\+44)\s*\d[\d\s-]{7,}\b"),
    re.compile(r"\b(passport|número de pasaporte|bank account|cuenta bancaria)\b", re.I),
    re.compile(r"\b(proven fraud|fraude probado|criminally liable|responsabilidad penal probada)\b", re.I),
]

errors: list[str] = []


def load(name: str) -> list[dict[str, Any]]:
    path = DATA / name
    if not path.exists():
        errors.append(f"{name}: missing file")
        return []
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{name}: invalid JSON: {exc}")
        return []
    if not isinstance(value, list):
        errors.append(f"{name}: top-level value must be a list")
        return []
    return value


def load_object(name: str) -> dict[str, Any]:
    path = DATA / name
    if not path.exists():
        errors.append(f"{name}: missing file")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{name}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{name}: top-level value must be an object")
        return {}
    return value


datasets = {name: load(name) for name in ID_PATTERNS}
multiple_credit_lives = load_object("multiple-credit-lives.json")

all_ids: dict[str, str] = {}
for filename, rows in datasets.items():
    pattern = ID_PATTERNS[filename]
    local: set[str] = set()
    for index, row in enumerate(rows):
        where = f"{filename}[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{where}: row must be an object")
            continue
        rid = row.get("id")
        if not isinstance(rid, str) or not pattern.fullmatch(rid):
            errors.append(f"{where}: invalid id {rid!r}")
            continue
        if rid in local:
            errors.append(f"{filename}: duplicate id {rid}")
        local.add(rid)
        if rid in all_ids:
            errors.append(f"global duplicate id {rid}: {all_ids[rid]} and {filename}")
        all_ids[rid] = filename
        status = row.get("evidence_status")
        if status is not None and status not in ALLOWED_STATUS:
            errors.append(f"{where}: invalid evidence_status {status!r}")
        pub = row.get("publication")
        if pub is not None and pub not in ALLOWED_PUBLICATION:
            errors.append(f"{where}: invalid publication {pub!r}")
        date = row.get("date")
        if date is not None and (not isinstance(date, str) or not DATE_RE.fullmatch(date)):
            errors.append(f"{where}: date must be YYYY-MM-DD or null, got {date!r}")
        rendered = json.dumps(row, ensure_ascii=False)
        for unsafe in UNSAFE_PATTERNS:
            if unsafe.search(rendered):
                errors.append(f"{where}: possible unsafe/private or overclaiming content matched {unsafe.pattern!r}")

source_ids = {row.get("id") for row in datasets["sources.json"] if isinstance(row, dict)}
actor_ids = {row.get("id") for row in datasets["actors.json"] if isinstance(row, dict)}
instrument_ids = {row.get("id") for row in datasets["instruments.json"] if isinstance(row, dict)}
proceeding_ids = {row.get("id") for row in datasets["proceedings.json"] if isinstance(row, dict)}
conduct_ids = {row.get("id") for row in datasets["conduct-decisions.json"] if isinstance(row, dict)}


def validate_nested_source_refs(value: Any, location: str) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == "source_refs":
                if not isinstance(nested, list) or not all(isinstance(ref, str) for ref in nested):
                    errors.append(f"{location}: source_refs must be a list of strings")
                else:
                    for ref in nested:
                        if ref not in source_ids:
                            errors.append(f"{location}: unknown source_refs reference {ref}")
            else:
                validate_nested_source_refs(nested, f"{location}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            validate_nested_source_refs(nested, f"{location}[{index}]")


propositions = multiple_credit_lives.get("propositions", [])
if not isinstance(propositions, list):
    errors.append("multiple-credit-lives.json: propositions must be a list")
    propositions = []
multiple_life_ids: set[str] = set()
for index, proposition in enumerate(propositions):
    where = f"multiple-credit-lives.json.propositions[{index}]"
    if not isinstance(proposition, dict):
        errors.append(f"{where}: proposition must be an object")
        continue
    proposition_id = proposition.get("id")
    if not isinstance(proposition_id, str) or not proposition_id:
        errors.append(f"{where}: proposition must have a non-empty string id")
    elif proposition_id in multiple_life_ids:
        errors.append(f"multiple-credit-lives.json: duplicate proposition id {proposition_id}")
    else:
        multiple_life_ids.add(proposition_id)
    status = proposition.get("evidence_status")
    if status not in ALLOWED_STATUS:
        errors.append(f"{where}: invalid evidence_status {status!r}")
    publication = proposition.get("publication")
    if publication not in ALLOWED_PUBLICATION:
        errors.append(f"{where}: invalid publication {publication!r}")
    validate_nested_source_refs(proposition, where)


def refs(row: dict[str, Any], field: str) -> list[str]:
    value = row.get(field, [])
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"{row.get('id', '<unknown>')}: {field} must be a list of strings")
        return []
    return value


def check_refs(rows: list[dict[str, Any]], field: str, valid: set[str | None]) -> None:
    for row in rows:
        if not isinstance(row, dict):
            continue
        for ref in refs(row, field):
            if ref not in valid:
                errors.append(f"{row.get('id')}: unknown {field} reference {ref}")


for rows in datasets.values():
    check_refs(rows, "source_refs", source_ids)
    check_refs(rows, "actor_refs", actor_ids)
    check_refs(rows, "claimant_actor_refs", actor_ids)
    check_refs(rows, "defendant_actor_refs", actor_ids)
    check_refs(rows, "related_actor_refs", actor_ids)
    check_refs(rows, "target_actor_refs", actor_ids)
    check_refs(rows, "debtor_actor_refs", actor_ids)
    check_refs(rows, "holder_chain_actor_refs", actor_ids)
    check_refs(rows, "counterparty_successor_actor_refs", actor_ids)
    check_refs(rows, "instrument_refs", instrument_ids)
    check_refs(rows, "later_conduct_refs", conduct_ids)
    check_refs(rows, "proceeding_refs", proceeding_ids)

for row in datasets["knowledge-events.json"]:
    for field in ("knowledge_topic", "directly_establishes", "does_not_establish"):
        if not isinstance(row.get(field), str) or not row[field].strip():
            errors.append(f"{row.get('id')}: missing {field}")

for row in datasets["transfers.json"]:
    for field in ("transferor_actor_ref", "transferee_actor_ref", "transfer_type"):
        if not isinstance(row.get(field), str) or not row[field].strip():
            errors.append(f"{row.get('id')}: missing {field}")
    for field in ("transferor_actor_ref", "transferee_actor_ref"):
        if row.get(field) not in actor_ids:
            errors.append(f"{row.get('id')}: unknown {field} {row.get(field)!r}")

for row in datasets["evidence-gaps.json"]:
    if row.get("priority") not in {"P0", "P1", "P2", "P3"}:
        errors.append(f"{row.get('id')}: invalid priority")
    if row.get("status") not in {"open", "partial", "closed", "superseded"}:
        errors.append(f"{row.get('id')}: invalid gap status")
    if not isinstance(row.get("next_action"), str) or not row["next_action"].strip():
        errors.append(f"{row.get('id')}: missing next_action")


def by_id(filename: str, rid: str) -> dict[str, Any] | None:
    return next((row for row in datasets[filename] if row.get("id") == rid), None)


for required_actor in ("ACT-ORIGINATING-LENDER", "ACT-BFA", "ACT-BANKIA", "ACT-AWESWELL", "ACT-CAIXABANK"):
    if required_actor not in actor_ids:
        errors.append(f"actors.json: missing required banking-chain actor {required_actor}")

valencia = by_id("proceedings.json", "PROC-VALENCIA-1859-2023-9")
if valencia:
    if set(refs(valencia, "actor_refs")) != {"ACT-AWESWELL", "ACT-CAIXABANK"}:
        errors.append("PROC-VALENCIA-1859-2023-9: actor_refs must contain only Aweswell and CaixaBank")
    if refs(valencia, "claimant_actor_refs") != ["ACT-AWESWELL"]:
        errors.append("PROC-VALENCIA-1859-2023-9: claimant must be ACT-AWESWELL")
    if refs(valencia, "defendant_actor_refs") != ["ACT-CAIXABANK"]:
        errors.append("PROC-VALENCIA-1859-2023-9: defendant must be ACT-CAIXABANK")
    if valencia.get("nig") != "46250-42-1-2023-0049579":
        errors.append("PROC-VALENCIA-1859-2023-9: controlled NIG mismatch")

haya = by_id("actors.json", "ACT-HAYA")
if not haya or "not_established_as_credit_holder_or_assignee" not in haya.get("capacity_limits", []):
    errors.append("ACT-HAYA: non-holder capacity limit is required")
for instrument in datasets["instruments.json"]:
    if "ACT-HAYA" in refs(instrument, "holder_chain_actor_refs"):
        errors.append(f"{instrument.get('id')}: Haya must not appear as a credit holder")
for transfer in datasets["transfers.json"]:
    if transfer.get("transferor_actor_ref") == "ACT-HAYA" or transfer.get("transferee_actor_ref") == "ACT-HAYA":
        errors.append(f"{transfer.get('id')}: Haya must not be a transfer endpoint")

for required_transfer in ("TR-2011-CAJA-INSULAR-BFA", "TR-2011-BFA-BANKIA", "TR-2021-BANKIA-CAIXABANK"):
    if by_id("transfers.json", required_transfer) is None:
        errors.append(f"transfers.json: missing required succession event {required_transfer}")

if errors:
    print("Lender-liability validation FAILED", file=sys.stderr)
    for error in errors:
        print(f" - {error}", file=sys.stderr)
    raise SystemExit(1)

counts = ", ".join(f"{name}={len(rows)}" for name, rows in datasets.items())
counts += f", multiple-credit-lives.json={len(propositions)} propositions"
print(f"Lender-liability validation PASSED: {counts}")

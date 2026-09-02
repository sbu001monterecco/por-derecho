#!/usr/bin/env python3
"""Validate the canonical Ministerio Fiscal hub without promoting source gaps."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"


def load(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def all_identity_records(index: dict) -> list[dict]:
    rows: list[dict] = []
    for part in index["parts"]:
        shard = load(DATA / part["path"])
        records = shard.get("records", [])
        if len(records) != int(part["count"]):
            raise AssertionError(f"{part['path']}: expected {part['count']} records, found {len(records)}")
        if shard.get("type") != part["type"]:
            raise AssertionError(f"{part['path']}: type mismatch")
        rows.extend(records)
    return rows


def main() -> None:
    index = load(DATA / "matter-identity-registry-v1.json")
    config = load(DATA / "ministerio-fiscal-hub-config-v1.json")
    graph = load(DATA / "fiscalia-proceedings-interconnectivity-v1.json")
    communications = load(DATA / "institutional-communications-register-v1.json")
    identities = all_identity_records(index)

    if len(identities) != int(index["counts"]["total"]):
        raise AssertionError("identity total does not equal shard manifest")
    ids = [row["id"] for row in identities]
    dup_ids = [item for item, count in Counter(ids).items() if count > 1]
    if dup_ids:
        raise AssertionError(f"duplicate canonical identity IDs: {dup_ids}")

    by_id = {row["id"]: row for row in identities}
    institution_ids = {row["id"] for row in identities if row.get("type") == "INSTITUTION"}
    proceeding_rows = [row for row in identities if row.get("type") == "PROCEEDING"]

    expected_institutions = {item for group in config["groups"] for item in group["institution_ids"]}
    missing_institutions = sorted(expected_institutions - institution_ids)
    if missing_institutions:
        raise AssertionError(f"hub config references missing institution IDs: {missing_institutions}")

    for iid in ("PD-SP-I-0045", "PD-SP-I-0046"):
        record = by_id[iid]
        if record.get("identity_resolution") != "CARET_CONFIRMED":
            raise AssertionError(f"{iid} is not caret-confirmed")
        if "PD-SP-I-0002" not in record.get("not_same_as", []):
            raise AssertionError(f"{iid} must remain separate from Spanish Ministerio Fiscal")

    by_master: dict[str, list[str]] = defaultdict(list)
    for record in proceeding_rows:
        mids = []
        mids.extend(record.get("master_register_ids", []))
        if record.get("master_register_id"):
            mids.append(record["master_register_id"])
        for mid in mids:
            by_master[mid].append(record["id"])

    fiscal_files = graph.get("fiscal_files", [])
    if graph.get("coverage", {}).get("fiscalia_exact_files") != 21:
        raise AssertionError("Fiscalía exact-file denominator changed; reconcile source before publishing")
    if graph.get("coverage", {}).get("fiscalia_unresolved_references") != 3:
        raise AssertionError("Fiscalía unresolved-reference denominator changed; reconcile source before publishing")
    if len(fiscal_files) != 24:
        raise AssertionError(f"expected 24 Fiscalía file/reference rows, found {len(fiscal_files)}")

    missing = []
    multiple = []
    for file in fiscal_files:
        matches = by_master.get(file["master_id"], [])
        if not matches:
            missing.append(file["master_id"])
        elif len(matches) != 1:
            multiple.append((file["master_id"], matches))
    if missing:
        raise AssertionError(f"Fiscalía master rows without CAEPR proceeding identity: {missing}")
    if multiple:
        raise AssertionError(f"Fiscalía master rows resolve to multiple CAEPR identities: {multiple}")

    expected_backfill = {
        "GC-FIS-011": "PD-SP-R-0044",
        "GC-FIS-012": "PD-SP-R-0045",
        "GC-FIS-015": "PD-SP-R-0046",
    }
    for master_id, caepr_id in expected_backfill.items():
        if by_master.get(master_id) != [caepr_id]:
            raise AssertionError(f"backfill mismatch {master_id} -> {by_master.get(master_id)}")

    events = communications.get("events", [])
    event_ids = [event.get("event_id", "") for event in events]
    if len(event_ids) != len(set(event_ids)):
        raise AssertionError("duplicate communication event IDs")
    invalid_events = [eid for eid in event_ids if not re.fullmatch(r"PD-SP-EVT-\d{4}", eid)]
    if invalid_events:
        raise AssertionError(f"invalid communication event IDs: {invalid_events[:10]}")

    denominator = communications.get("denominator_control", {})
    if denominator.get("detailed_baseline_receipt_rows_expected") != 75 or denominator.get("detailed_baseline_receipt_rows_registered") != 75:
        raise AssertionError("75-row detailed REGAGE baseline is no longer 75/75")
    if denominator.get("metadata_only_records_reported") != 22:
        raise AssertionError("22-record aggregate-only RedSARA gap changed; reconcile before publishing")
    if denominator.get("metadata_only_representation") != "ONE_UNRESOLVED_BATCH_NOT_22_SYNTHETIC_EVENTS":
        raise AssertionError("aggregate-only RedSARA gap was improperly decomposed")

    required_html = {
        ROOT / "es" / "ministerio-fiscal" / "index.html": "ministerio-fiscal-hub-20260902.js",
        ROOT / "en" / "public-prosecution-service" / "index.html": "ministerio-fiscal-hub-20260902.js",
    }
    for path, needle in required_html.items():
        text = path.read_text(encoding="utf-8")
        if needle not in text or "data-mf-hub" not in text:
            raise AssertionError(f"hub page wiring missing in {path}")

    reciprocal_pages = {
        ROOT / "es" / "fiscalia-comunicaciones-procedimientos" / "index.html": "../ministerio-fiscal/",
        ROOT / "en" / "public-prosecution-communications-proceedings" / "index.html": "../public-prosecution-service/",
    }
    for path, needle in reciprocal_pages.items():
        if needle not in path.read_text(encoding="utf-8"):
            raise AssertionError(f"reciprocal hub link missing in {path}")

    print(
        "PASS Ministerio Fiscal hub: "
        f"{len(expected_institutions)} office identities; {len(fiscal_files)}/24 Fiscalía file identities; "
        f"{len(events)} unique canonical events; 75/75 detailed REGAGE receipts; 22 aggregate-only records preserved as one gap."
    )


if __name__ == "__main__":
    main()

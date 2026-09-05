#!/usr/bin/env python3
"""Validate the public Fiscalía communications/proceedings implementation."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/fiscalia-proceedings-interconnectivity-v1.json"
MASTER = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
COMMUNICATIONS = ROOT / "assets/data/institutional-communications-register-v1.json"
PRISM = ROOT / "assets/data/proceedings-case-prism-v1.json"
EXPECTED_FISCALIA_IDS = {
    "LZ-FIS-007", "GC-FIS-011", "GC-FIS-012", "GC-FIS-013", "GC-FIS-014",
    "GC-FIS-015", "GC-FIS-016", "GC-FIS-017", "GC-FIS-018", "LZ-FIS-036",
    "LZ-FIS-045", "TF-FIS-007", "GC-FIS-032", "TF-FIS-008", "GC-FIS-033",
    "NAT-FIS-004", "GC-FIS-034", "NAT-FIS-005", "GC-FIS-035", "NAT-FIS-006",
    "NAT-FIS-007", "LZ-FIS-049", "LZ-FIS-051", "TF-FIS-009", "TF-FIS-010", "UNK-FIS-001",
}
FORBIDDEN_PUBLIC_KEYS = {
    "recipient_email", "sender_email", "message_id", "thread_id", "account_id",
    "private_locator", "local_path", "Primary_Source_Anchor", "Notes",
}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def keys_recursive(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from keys_recursive(child)
    elif isinstance(value, list):
        for child in value:
            yield from keys_recursive(child)


def main() -> int:
    errors: list[str] = []
    required = [
        DATA, MASTER, COMMUNICATIONS, PRISM,
        ROOT / "assets/data/fiscalia-proceedings-link-assertions-v1.json",
        ROOT / "assets/fiscalia-proceedings-interconnectivity-20260831.js",
        ROOT / "assets/fiscalia-proceedings-interconnectivity-20260831.css",
        ROOT / "en/public-prosecution-communications-proceedings/index.html",
        ROOT / "es/fiscalia-comunicaciones-procedimientos/index.html",
    ]
    for path in required:
        require(path.exists(), f"missing required file: {path.relative_to(ROOT)}", errors)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1

    payload = json.loads(DATA.read_text(encoding="utf-8"))
    communications = json.loads(COMMUNICATIONS.read_text(encoding="utf-8"))
    prism = json.loads(PRISM.read_text(encoding="utf-8"))
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        master_rows = list(csv.DictReader(handle))
    master_ids = {row["Master_ID"] for row in master_rows}
    canonical_event_ids = {event["event_id"] for event in communications["events"]}
    excluded_authority_ids = set(
        communications.get("authority_scan_control", {}).get("new_event_ids", [])
    )
    from prepare_orion_notice_register_20260905 import load_notice_events
    expected_notices = {event["event_id"]: event for event in load_notice_events(ROOT)}
    actual_notices = {event["event_id"]: event for event in communications["events"]
                      if event.get("source_batch_id") == "PD-SP-ORION-NOTICE-20260905"}
    require(actual_notices == expected_notices, "financial notice source cohort mismatch", errors)
    event_ids = canonical_event_ids - excluded_authority_ids - set(expected_notices)
    projected_ids = {event["event_id"] for event in payload["events"]}

    require(payload.get("schema_version") == "1.0.0", "schema version changed", errors)
    require(payload.get("status") == "PUBLIC_SAFE_DERIVED_INTERCONNECTIVITY_PROJECTION", "projection status changed", errors)
    require(
        len(canonical_event_ids) == 313 + len(expected_notices)
        and len(excluded_authority_ids) == 17
        and excluded_authority_ids <= canonical_event_ids
        and len(event_ids) == len(projected_ids) == 296
        and event_ids == projected_ids,
        "event denominator or identity mismatch",
        errors,
    )
    require(payload["coverage"].get("matter_linked_events") == 117, "matter-linked event denominator mismatch", errors)
    require(payload["coverage"].get("fiscalia_exact_files") == 23, "exact Fiscalía denominator mismatch", errors)
    require(payload["coverage"].get("fiscalia_unresolved_references") == 3, "unresolved Fiscalía denominator mismatch", errors)
    require(payload["coverage"].get("fiscalia_identity_total") == 26, "Fiscalía total denominator mismatch", errors)
    require(len(payload.get("priority_chains", [])) == 9, "priority chain denominator mismatch", errors)
    require(not payload["coverage"].get("unresolved_matter_reference_literals"), "matter references remain orphaned", errors)
    require(all(event.get("allocation_state") and event.get("interconnectivity_scope") for event in payload["events"]), "an event lacks allocation/scope", errors)
    require(sum(bool(event.get("matter_references")) for event in payload["events"]) == 117, "projected matter-linked denominator mismatch", errors)

    projected_fiscal_ids = {file["master_id"] for file in payload["fiscalia_files"]}
    require(projected_fiscal_ids == EXPECTED_FISCALIA_IDS, f"Fiscalía identity set mismatch: {sorted(projected_fiscal_ids ^ EXPECTED_FISCALIA_IDS)}", errors)
    for file in payload["fiscalia_files"]:
        require(bool(file.get("open_reference_gap")), f"{file['master_id']} lacks an explicit next-source gap", errors)
        if file["identity_state"] == "UNRESOLVED_REFERENCE":
            require(file.get("source_status") in {"OPEN_REFERENCE", "CORPUS_REPORTED_PRIMARY_PENDING"}, f"{file['master_id']} unresolved identity source status overstated", errors)

    proceeding_edges = payload.get("event_proceeding_edges", [])
    edge_pairs = {(edge["event_id"], edge["master_id"]) for edge in proceeding_edges}
    require(len(edge_pairs) == len(proceeding_edges), "duplicate event/proceeding edge", errors)
    require(all(edge["event_id"] in event_ids for edge in proceeding_edges), "proceeding edge has unknown event", errors)
    require(all(edge["master_id"] in master_ids for edge in proceeding_edges), "proceeding edge has unknown Master ID", errors)
    require(all(edge["relationship_strength"] in {"DIRECT_FILE_REFERENCE", "CONTEXT_OR_CITATION"} for edge in proceeding_edges), "invalid edge strength", errors)
    event_edges = payload.get("event_event_edges", [])
    require(all(edge["from_event_id"] in event_ids and edge["to_event_id"] in event_ids for edge in event_edges), "event edge has unknown endpoint", errors)

    for master_id, summary in payload.get("by_master_id", {}).items():
        require(master_id in master_ids, f"by_master_id has unknown ID: {master_id}", errors)
        require(summary["event_count"] == len(set(summary["event_ids"])), f"{master_id} reciprocal event count mismatch", errors)
        require(all((event_id, master_id) in edge_pairs for event_id in summary["event_ids"]), f"{master_id} reciprocal index lacks an edge", errors)

    repository_anchors = [event["source"].get("repository_anchor", "") for event in payload["events"]]
    require(all(not anchor or (ROOT / anchor).exists() for anchor in repository_anchors), "a projected source anchor is missing", errors)
    exposed = set(keys_recursive(payload)) & FORBIDDEN_PUBLIC_KEYS
    require(not exposed, f"forbidden public field(s): {sorted(exposed)}", errors)

    p05 = next(prop for prop in prism["propositions"] if prop["id"] == "P05")
    require(set(p05["cells"]["fiscalia"]["master_ids"]) == EXPECTED_FISCALIA_IDS, "P05 Fiscalía denominator is incomplete", errors)
    require(prism["coverage"].get("explicit_coordinate_count") == 228, "Case Prism structural denominator changed", errors)

    js = (ROOT / "assets/fiscalia-proceedings-interconnectivity-20260831.js").read_text(encoding="utf-8")
    master_js = (ROOT / "assets/master-proceedings-publication-20260830.js").read_text(encoding="utf-8")
    map_js = (ROOT / "assets/proceedings-interconnectivity-map-20260830.js").read_text(encoding="utf-8")
    for token in ("#file=", "data-mf-interconnectivity", "priority_chains", "fiscalia-proceedings-interconnectivity-v1.json"):
        require(token in js, f"specialist renderer missing token: {token}", errors)
    require("data-fiscalia-master-id" in master_js and "fiscalia-proceedings-interconnectivity-v1.json" in master_js, "Master Register reciprocal link missing", errors)
    require("data-fiscalia-master-id" in map_js and "fiscalia-proceedings-interconnectivity-v1.json" in map_js, "Proceedings Map reciprocal link missing", errors)
    for page in required[-2:]:
        text = page.read_text(encoding="utf-8")
        require("data-mf-interconnectivity" in text, f"{page.relative_to(ROOT)} lacks app mount", errors)
        require("fiscalia-proceedings-interconnectivity-20260831.js?v=20260831a" in text, f"{page.relative_to(ROOT)} lacks cache-busted renderer", errors)
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    require("/en/public-prosecution-communications-proceedings/" in sitemap and "/es/fiscalia-comunicaciones-procedimientos/" in sitemap, "sitemap routes missing", errors)

    check = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_fiscalia_proceedings_interconnectivity.py"), "--check"],
        cwd=ROOT, capture_output=True, text=True,
    )
    require(check.returncode == 0, check.stdout.strip() or check.stderr.strip() or "deterministic builder check failed", errors)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("OK: Fiscalía communications/proceedings interconnectivity is complete, reciprocal, public-safe and deterministic")
    print(f"- events: {len(projected_ids)}; event/proceeding edges: {len(proceeding_edges)}; event/event edges: {len(event_edges)}")
    print("- Fiscalía identities: 23 exact + 3 unresolved; priority chains: 9")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build the public Ministerio Fiscal communications/proceedings graph.

The canonical communications register and proceedings master remain the two
authoritative registers.  This script emits a deterministic navigation and
audit projection between them.  It does not infer delivery, examination,
merits, knowledge, intent, joinder, or wrongdoing from a reference or date.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COMMUNICATIONS = ROOT / "assets/data/institutional-communications-register-v1.json"
MASTER = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
PUBLIC_MASTER = ROOT / "assets/data/proceedings-master-public-v1.json"
ASSERTIONS = ROOT / "assets/data/fiscalia-proceedings-link-assertions-v1.json"
TARGET = ROOT / "assets/data/fiscalia-proceedings-interconnectivity-v1.json"

EXPECTED_EVENTS = 296
EXPECTED_MATTER_LINKED_EVENTS = 117
EXPECTED_FISCALIA_EXACT = 23
EXPECTED_FISCALIA_UNRESOLVED = 3
SUPPORT_REFERENCE_PREFIXES = ("REGAGE",)
FISCALIA_RECORD_TYPES = {"FISCALIA_FILE", "UNRESOLVED_REFERENCE"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_master() -> list[dict[str, str]]:
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len({row["Master_ID"] for row in rows}) != len(rows):
        raise ValueError("Master_ID values must be unique")
    return rows


def normalise_reference(value: str) -> str:
    """Normalise presentation only; never perform fuzzy identity matching."""
    value = value.upper().replace("E.G.", "EG").replace("D.I.P.", "DIP")
    return re.sub(r"[^A-Z0-9]", "", value)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reference_aliases(row: dict[str, str]) -> set[str]:
    aliases: set[str] = set()
    for field in ("Reference", "Secondary_Reference", "NIG"):
        raw = row.get(field, "").strip()
        if not raw:
            continue
        values = [raw, *re.split(r"[;|]", raw)]
        for value in values:
            value = value.strip()
            if value:
                aliases.add(normalise_reference(value))
        if field == "NIG":
            digits = normalise_reference(raw)
            aliases.add(f"NIG{digits}")
    return aliases


def build_alias_index(
    public_rows: list[dict[str, str]], assertions: dict[str, Any]
) -> dict[str, str]:
    candidates: dict[str, set[str]] = defaultdict(set)
    for row in public_rows:
        for alias in reference_aliases(row):
            candidates[alias].add(row["Master_ID"])
    # A duplicated alias in the master is deliberately non-resolving.  It must
    # never be collapsed merely because two rows share a NIG or receipt label.
    index = {key: next(iter(value)) for key, value in candidates.items() if len(value) == 1}
    # An explicit source-controlled override is the sole permitted way to
    # resolve a presentation variant or a deliberately ambiguous literal.
    for raw, master_id in assertions["reference_overrides"].items():
        index[normalise_reference(raw)] = master_id
    return index


def is_support_reference(reference: str) -> bool:
    return normalise_reference(reference).startswith(SUPPORT_REFERENCE_PREFIXES)


def relation_type(event: dict[str, Any], direct: bool) -> str:
    record_type = event["record_type"]
    if record_type == "EMAIL_DRAFT":
        return "DRAFT_REFERENCES_PROCEEDING"
    if record_type == "SELF_ARCHIVE_CONTROL":
        return "SELF_ARCHIVE_REFERENCES_PROCEEDING"
    if record_type == "EMAIL_TRANSPORT":
        return "TRANSPORT_REFERENCES_PROCEEDING"
    if record_type == "REGISTRATION_RECEIPT":
        return "FORMAL_REGISTRATION_TO_PROCEEDING" if direct else "SUBMISSION_REFERENCES_PROCEEDING"
    if record_type == "OUTBOUND_COMMUNICATION":
        return "COMMUNICATION_TO_PROCEEDING" if direct else "COMMUNICATION_REFERENCES_PROCEEDING"
    if record_type == "INSTITUTIONAL_ACKNOWLEDGEMENT":
        return "ACKNOWLEDGEMENT_FOR_PROCEEDING" if direct else "ACKNOWLEDGEMENT_REFERENCES_PROCEEDING"
    if event["event_id"] == "PD-SP-EVT-0082" and direct:
        return "COURT_REQUESTS_FISCAL_REPORT"
    if direct:
        return "ACT_IN_PROCEEDING"
    return "ACT_REFERENCES_PROCEEDING"


def allocation_state(event: dict[str, Any], master_ids: list[str], support: list[str]) -> str:
    if event["record_type"] == "EMAIL_DRAFT":
        return "DRAFT"
    if event["record_type"] == "SELF_ARCHIVE_CONTROL":
        return "SELF_ARCHIVE"
    if master_ids:
        return "PROCEEDING_LINKED"
    if support:
        return "SUPPORT_REFERENCE_ONLY"
    if event["record_type"] == "EMAIL_TRANSPORT":
        return "UNALLOCATED_TRANSPORT"
    if event["record_type"] == "REGISTRATION_RECEIPT":
        return "UNALLOCATED_FORMAL_REGISTRATION"
    return "UNALLOCATED_OFFICIAL_EVENT"


def event_projection(event: dict[str, Any]) -> dict[str, Any]:
    source = event.get("source_integrity", {})
    allowed = {
        "event_id": event["event_id"],
        "event_date": event.get("event_date", ""),
        "direction": event["direction"],
        "record_type": event["record_type"],
        "channel": event.get("channel", ""),
        "layer": event.get("layer", ""),
        "office": event.get("office", ""),
        "official_reference": event.get("official_reference", ""),
        "matter_references": event.get("matter_references", []),
        "public_summary": event.get("public_summary", ""),
        "proof_level": event.get("proof_level", ""),
        "proves": event.get("proves", []),
        "does_not_prove": event.get("does_not_prove", []),
        "source": {
            "repository_anchor": source.get("repository_anchor", ""),
            "status": source.get("status", ""),
        },
    }
    return allowed


def build() -> dict[str, Any]:
    communications = load_json(COMMUNICATIONS)
    public_master = load_json(PUBLIC_MASTER)
    assertions = load_json(ASSERTIONS)
    master_rows = load_master()
    public_ids = {record["Master_ID"] for record in public_master["records"]}
    public_rows = [row for row in master_rows if row["Master_ID"] in public_ids]
    by_master = {row["Master_ID"]: row for row in public_rows}
    alias_index = build_alias_index(public_rows, assertions)
    non_fiscalia_authority_ids = set(
        communications.get("authority_scan_control", {}).get("new_event_ids", [])
    )
    # The separately controlled Orion/financial-notice cohort has no
    # source-allocated Fiscalia proceeding in this release. It remains fully
    # registered and interlinked in the institutional/Orion projections.
    non_fiscalia_notice_ids = {
        event["event_id"] for event in communications["events"]
        if event.get("source_batch_id") == "PD-SP-ORION-NOTICE-20260905"
    }
    events = [
        event
        for event in communications["events"]
        if event.get("event_id") not in non_fiscalia_authority_ids | non_fiscalia_notice_ids
    ]

    if len(events) != EXPECTED_EVENTS:
        raise ValueError(f"expected {EXPECTED_EVENTS} communication events, found {len(events)}")
    if sum(bool(e.get("matter_references")) for e in events) != EXPECTED_MATTER_LINKED_EVENTS:
        raise ValueError("matter-linked event denominator changed; reconcile before publishing")

    projections: list[dict[str, Any]] = []
    proceeding_edges: list[dict[str, Any]] = []
    event_master_ids: dict[str, list[str]] = {}
    event_support: dict[str, list[str]] = {}

    for event in events:
        resolved: list[tuple[str, str, bool]] = []
        support: list[str] = []
        unresolved: list[str] = []
        official_norm = normalise_reference(event.get("official_reference", ""))
        for reference in event.get("matter_references", []):
            if is_support_reference(reference):
                support.append(reference)
                continue
            normalised = normalise_reference(reference)
            master_id = alias_index.get(normalised)
            if not master_id:
                unresolved.append(reference)
                continue
            direct = bool(normalised and normalised in official_norm)
            resolved.append((reference, master_id, direct))

        master_ids = list(dict.fromkeys(item[1] for item in resolved))
        record_types = {by_master[mid]["Record_Type"] for mid in master_ids}
        has_fiscal = bool(record_types & FISCALIA_RECORD_TYPES)
        has_other = bool(record_types - FISCALIA_RECORD_TYPES)
        if has_fiscal and has_other:
            scope = "CROSS_FILE_BRIDGE"
        elif has_fiscal:
            scope = "OUTSIDE_JUDICIAL_PROCEEDING"
        elif has_other:
            scope = "INSIDE_JUDICIAL_PROCEEDING"
        elif support:
            scope = "SUPPORT_REFERENCE_ONLY"
        else:
            scope = "NO_PROCEEDING_LINK"

        projection = event_projection(event)
        projection.update(
            {
                "allocation_state": allocation_state(event, master_ids, support),
                "interconnectivity_scope": scope,
                "master_ids": master_ids,
                "supporting_references": support,
                "unresolved_matter_references": unresolved,
            }
        )
        projections.append(projection)
        event_master_ids[event["event_id"]] = master_ids
        event_support[event["event_id"]] = support

        resolved_by_master: dict[str, dict[str, Any]] = {}
        for reference, master_id, direct in resolved:
            bucket = resolved_by_master.setdefault(master_id, {"references": [], "direct": False})
            bucket["references"].append(reference)
            bucket["direct"] = bucket["direct"] or direct
        for master_id, match in resolved_by_master.items():
            direct = bool(match["direct"])
            row = by_master[master_id]
            proceeding_edges.append(
                {
                    "edge_id": f"MF-EDGE-{event['event_id']}-{master_id}",
                    "event_id": event["event_id"],
                    "master_id": master_id,
                    "reference_literals": match["references"],
                    "match_method": "EXACT_NORMALISED_REFERENCE_OR_CONTROLLED_OVERRIDE",
                    "relationship_type": relation_type(event, direct),
                    "relationship_strength": "DIRECT_FILE_REFERENCE" if direct else "CONTEXT_OR_CITATION",
                    "operational_scope": (
                        "OUTSIDE_JUDICIAL_PROCEEDING"
                        if row["Record_Type"] in FISCALIA_RECORD_TYPES
                        else "INSIDE_JUDICIAL_PROCEEDING"
                    ),
                    "boundary_en": "The edge proves only that this event names the canonical reference in the stated role.",
                    "boundary_es": "El enlace prueba únicamente que este evento identifica la referencia canónica en la función indicada.",
                }
            )

    event_ids = {event["event_id"] for event in events}
    event_event_candidates: list[dict[str, Any]] = []
    for event in events:
        for linked in event.get("linked_transport_event_ids", []):
            event_event_candidates.append(
                {
                    "from_event_id": event["event_id"],
                    "to_event_id": linked,
                    "relationship_type": "SOURCE_REGISTER_TRANSPORT_LINK",
                    "assertion_source": "CANONICAL_COMMUNICATIONS_REGISTER",
                }
            )
    for edge in assertions["event_event_edges"]:
        event_event_candidates.append(
            {
                "from_event_id": edge["from_event_id"],
                "to_event_id": edge["to_event_id"],
                "relationship_type": edge["relationship_type"],
                "assertion_source": "SOURCE_CONTROLLED_SPECIALIST_ASSERTION",
            }
        )
    event_event_edges: list[dict[str, Any]] = []
    seen_event_edges: set[tuple[str, str, str]] = set()
    for edge in event_event_candidates:
        if edge["from_event_id"] not in event_ids or edge["to_event_id"] not in event_ids:
            raise ValueError(f"event-event edge references unknown event: {edge}")
        key = (edge["from_event_id"], edge["to_event_id"], edge["relationship_type"])
        if key in seen_event_edges:
            continue
        seen_event_edges.add(key)
        event_event_edges.append(
            {
                "edge_id": f"MF-EVENT-EDGE-{len(event_event_edges) + 1:04d}",
                **edge,
                "boundary_en": "The link records sequence or transport correspondence only; it does not prove examination, agreement, causation or merits.",
                "boundary_es": "El enlace registra únicamente secuencia o correspondencia de transporte; no prueba examen, acuerdo, causalidad ni fondo.",
            }
        )

    edges_by_master: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in proceeding_edges:
        edges_by_master[edge["master_id"]].append(edge)

    fiscal_rows = [
        row
        for row in public_rows
        if row["Record_Type"] == "FISCALIA_FILE"
        or (row["Record_Type"] == "UNRESOLVED_REFERENCE" and row["Stream"] == "Fiscalía")
    ]
    exact = sum(row["Record_Type"] == "FISCALIA_FILE" for row in fiscal_rows)
    unresolved = sum(row["Record_Type"] == "UNRESOLVED_REFERENCE" for row in fiscal_rows)
    if (exact, unresolved) != (EXPECTED_FISCALIA_EXACT, EXPECTED_FISCALIA_UNRESOLVED):
        raise ValueError(
            f"expected {EXPECTED_FISCALIA_EXACT} exact + {EXPECTED_FISCALIA_UNRESOLVED} unresolved Fiscalía identities, "
            f"found {exact} + {unresolved}"
        )

    fiscal_files: list[dict[str, Any]] = []
    for row in fiscal_rows:
        edges = edges_by_master.get(row["Master_ID"], [])
        linked_event_ids = list(dict.fromkeys(edge["event_id"] for edge in edges))
        linked_ids = set()
        for field in ("Parent_Master_ID", "Linked_Proceedings"):
            linked_ids.update(re.findall(r"[A-Z]+(?:-[A-Z]+)*-\d{3}", row.get(field, "")))
        for event_id in linked_event_ids:
            linked_ids.update(mid for mid in event_master_ids[event_id] if mid != row["Master_ID"])
        linked_judicial = sorted(
            mid for mid in linked_ids if mid in by_master and by_master[mid]["Record_Type"] != "FISCALIA_FILE"
        )
        linked_events = [e for e in projections if e["event_id"] in linked_event_ids]
        fiscal_files.append(
            {
                "master_id": row["Master_ID"],
                "identity_state": "EXACT_CANONICAL" if row["Record_Type"] == "FISCALIA_FILE" else "UNRESOLVED_REFERENCE",
                "reference": row["Reference"],
                "secondary_reference": row["Secondary_Reference"],
                "office": row["Current_Custodian"],
                "geography": row["Geography"],
                "status": row["Status"],
                "latest_known_event": row["Latest_Known_Event"],
                "source_status": row["Source_Status"],
                "open_reference_gap": row["Open_Reference_Gap"],
                "linked_event_ids": linked_event_ids,
                "linked_judicial_master_ids": linked_judicial,
                "counts": {
                    "events": len(linked_events),
                    "outbound": sum(e["direction"] == "OUTBOUND_TO_INSTITUTION" for e in linked_events),
                    "inbound": sum(e["direction"] == "INBOUND_FROM_INSTITUTION" for e in linked_events),
                    "institution_to_institution": sum(e["direction"] == "INSTITUTION_TO_INSTITUTION" for e in linked_events),
                    "official_acts_or_decisions": sum(e["record_type"].startswith("OFFICIAL_") for e in linked_events),
                    "linked_judicial_proceedings": len(linked_judicial),
                },
            }
        )

    by_master_id: dict[str, Any] = {}
    for master_id, edges in sorted(edges_by_master.items()):
        row = by_master[master_id]
        event_ids_for_master = list(dict.fromkeys(edge["event_id"] for edge in edges))
        by_master_id[master_id] = {
            "reference": row["Reference"],
            "record_type": row["Record_Type"],
            "event_ids": event_ids_for_master,
            "event_count": len(event_ids_for_master),
            "direct_edge_count": sum(edge["relationship_strength"] == "DIRECT_FILE_REFERENCE" for edge in edges),
            "context_edge_count": sum(edge["relationship_strength"] == "CONTEXT_OR_CITATION" for edge in edges),
            "fiscalia_route_en": f"/en/public-prosecution-communications-proceedings/#file={master_id}",
            "fiscalia_route_es": f"/es/fiscalia-comunicaciones-procedimientos/#file={master_id}",
        }

    priority_chains: list[dict[str, Any]] = []
    for chain in assertions["priority_chains"]:
        unknown = sorted(set(chain["master_ids"]) - public_ids)
        if unknown:
            raise ValueError(f"priority chain {chain['chain_id']} has unknown Master IDs: {unknown}")
        chain_event_ids = [
            event["event_id"]
            for event in projections
            if set(event["master_ids"]) & set(chain["master_ids"])
        ]
        priority_chains.append({**chain, "event_ids": chain_event_ids, "event_count": len(chain_event_ids)})

    allocation_counts = Counter(event["allocation_state"] for event in projections)
    scope_counts = Counter(event["interconnectivity_scope"] for event in projections)
    unresolved_literals = sorted(
        {literal for event in projections for literal in event["unresolved_matter_references"]}
    )
    return {
        "schema_version": "1.0.0",
        "dataset": "fiscalia-proceedings-interconnectivity-v1",
        "control_date": "2026-09-03",
        "status": "PUBLIC_SAFE_DERIVED_INTERCONNECTIVITY_PROJECTION",
        "canonical_sources": {
            "communications_register": str(COMMUNICATIONS.relative_to(ROOT)),
            "communications_sha256": sha256(COMMUNICATIONS),
            "proceedings_master": str(MASTER.relative_to(ROOT)),
            "proceedings_master_sha256": sha256(MASTER),
            "public_proceedings_projection": str(PUBLIC_MASTER.relative_to(ROOT)),
            "link_assertions": str(ASSERTIONS.relative_to(ROOT)),
            "link_assertions_sha256": sha256(ASSERTIONS),
        },
        "boundaries": assertions["boundaries"],
        "coverage": {
            "communication_events": len(projections),
            "matter_linked_events": sum(bool(e["matter_references"]) for e in projections),
            "proceeding_linked_events": sum(bool(e["master_ids"]) for e in projections),
            "support_reference_only_events": allocation_counts["SUPPORT_REFERENCE_ONLY"],
            "event_proceeding_edges": len(proceeding_edges),
            "event_event_edges": len(event_event_edges),
            "fiscalia_exact_files": exact,
            "fiscalia_unresolved_references": unresolved,
            "fiscalia_identity_total": len(fiscal_files),
            "allocation_counts": dict(sorted(allocation_counts.items())),
            "scope_counts": dict(sorted(scope_counts.items())),
            "unresolved_matter_reference_literals": unresolved_literals,
        },
        "events": projections,
        "event_proceeding_edges": proceeding_edges,
        "event_event_edges": event_event_edges,
        "fiscalia_files": fiscal_files,
        "by_master_id": by_master_id,
        "priority_chains": priority_chains,
    }


def serialise(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true", help="write the generated projection")
    mode.add_argument("--check", action="store_true", help="verify that the generated projection is current")
    args = parser.parse_args()
    rendered = serialise(build())
    if args.check:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != rendered:
            print(f"stale or missing generated projection: {TARGET.relative_to(ROOT)}")
            print(f"current canonical source hashes: communications={sha256(COMMUNICATIONS)} master={sha256(MASTER)} assertions={sha256(ASSERTIONS)}")
            print(f"expected Fiscalía denominator: {EXPECTED_FISCALIA_EXACT} exact + {EXPECTED_FISCALIA_UNRESOLVED} unresolved")
            return 1
        print(f"OK: {TARGET.relative_to(ROOT)} is deterministic and current")
        return 0
    TARGET.write_text(rendered, encoding="utf-8")
    print(f"wrote {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

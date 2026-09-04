#!/usr/bin/env python3
"""Fail-closed validator for PD-C212224-001 continuity governance."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/control-21-22-24-continuity-v1.json"
PROTOCOL = ROOT / ".github/governance/CONTROL_21_22_24_CONTINUITY_INTERLINK_PROTOCOL_04SEP2026.md"
HANDOFF_MD = ROOT / "archive/handoffs/2026-09-04-control-21-22-24-continuity-handoff.md"
HANDOFF_JSON = ROOT / "archive/handoffs/2026-09-04-control-21-22-24-continuity-handoff.json"

REQUIRED_NODE_IDS = {
    "CONCURSO-36-2012",
    "CONTROL-21",
    "CONTROL-22",
    "CONTROL-24",
    "GC-CRI-008",
    "GC-CRI-009",
    "GC-REF-029",
    "GC-HC-010",
    "CONTROL-24-AMPLIACION-20260625",
    "CONTROL-21-OBJECT-20260625",
    "GC-GOV-019",
    "ALZADA-286-2026",
    "GC-FIS-017",
}

REQUIRED_ALIASES = {
    "Control 21",
    "Control 22",
    "Control 24",
    "DP 1901/2026",
    "DP 1956/2026",
    "GC-CRI-008",
    "GC-CRI-009",
    "GC-REF-029",
    "GC-HC-010",
    "DI 169/2026",
    "CGPJ 169/2026",
    "DIP 2/2026",
    "18 June 2026",
    "25 June 2026",
    "Concurso 36/2012",
}

CRITICAL_EDGES = {
    ("CONTROL-21", "GC-CRI-008", "UNVERIFIED_CANDIDATE_BRIDGE"),
    ("CONTROL-22", "GC-REF-029", "PROVEN_DOCUMENTARY_BRIDGE"),
    ("CONTROL-22", "GC-CRI-009", "UNVERIFIED_CANDIDATE_BRIDGE"),
    ("CONTROL-24", "GC-HC-010", "PROVEN_DOCUMENTARY_BRIDGE"),
    ("CONTROL-24", "CONTROL-24-AMPLIACION-20260625", "MATERIALLY_LINKED_DISTINCT_OBJECTS"),
    ("CONTROL-24", "GC-GOV-019", "RELATED_SEPARATE_ROUTE"),
    ("CONTROL-24", "GC-FIS-017", "RELATED_SEPARATE_ROUTE"),
    ("CONTROL-21-OBJECT-20260625", "CONTROL-24-AMPLIACION-20260625", "NO_BRIDGE"),
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path):
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def main() -> None:
    for required in (PROTOCOL, HANDOFF_MD, HANDOFF_JSON):
        if not required.is_file():
            fail(f"missing required continuity file: {required.relative_to(ROOT)}")

    data = load_json(DATA)
    handoff = load_json(HANDOFF_JSON)

    if data.get("control_id") != "PD-C212224-001":
        fail("unexpected control_id")
    if data.get("canonical_nucleus", {}).get("id") != "CONCURSO-36-2012":
        fail("Concurso 36/2012 canonical nucleus is missing")

    controls = {item.get("id"): item for item in data.get("controls", [])}
    if set(controls) != {"CONTROL-21", "CONTROL-22", "CONTROL-24"}:
        fail("exact Control 21/22/24 control set not preserved")

    c21 = controls["CONTROL-21"]
    if c21.get("bridge_status") != "UNVERIFIED_CANDIDATE_BRIDGE":
        fail("Control 21 -> DP 1901 bridge must remain unverified until source-certified")
    if c21.get("evidential_state") != "ATTRIBUTED_ALLEGATION":
        fail("Control 21 current intake/date claim must remain attributed, not promoted to documented fact")

    c22 = controls["CONTROL-22"]
    if c22.get("bridge_status") != "UNVERIFIED_CANDIDATE_BRIDGE":
        fail("Control 22 -> DP 1956 bridge must remain unverified until source-certified")
    if c22.get("canonical_repository_object") != "GC-REF-029":
        fail("Control 22 must retain GC-REF-029 as its canonical intake object")

    c24 = controls["CONTROL-24"]
    if c24.get("formal_destination_status") != "UNKNOWN":
        fail("Control 24 formal destination must remain UNKNOWN absent documentary bridge")
    if c24.get("canonical_repository_object") != "GC-HC-010":
        fail("Control 24 must retain GC-HC-010 as its canonical control record")
    if c24.get("judge_amplification_date") != "2026-06-25":
        fail("Control 24 judge-related amplification date must remain explicit")

    nodes = {item.get("id") for item in data.get("nodes", [])}
    missing_nodes = REQUIRED_NODE_IDS - nodes
    if missing_nodes:
        fail(f"missing required graph nodes: {sorted(missing_nodes)}")

    aliases = set(data.get("aliases", []))
    missing_aliases = REQUIRED_ALIASES - aliases
    if missing_aliases:
        fail(f"missing required search aliases: {sorted(missing_aliases)}")

    edge_keys = set()
    for edge in data.get("edges", []):
        if edge.get("bidirectional") is not True:
            fail(f"edge is not bidirectional: {edge.get('from')} -> {edge.get('to')}")
        if edge.get("from") not in nodes or edge.get("to") not in nodes:
            fail(f"edge references unknown node: {edge}")
        edge_keys.add((edge.get("from"), edge.get("to"), edge.get("bridge_status")))

    missing_edges = CRITICAL_EDGES - edge_keys
    if missing_edges:
        fail(f"missing/altered critical edges: {sorted(missing_edges)}")

    if "CONTROL-21-OBJECT-20260625" == "CONTROL-24-AMPLIACION-20260625":
        fail("25 June objects collapsed")

    public_routes = data.get("public_routes", {})
    for key in ("CONTROL-22_EN", "CONTROL-22_ES", "DP-1901_EN", "DP-1901_ES", "DP-1956_EN", "DP-1956_ES", "CONTROL-24_EN", "CONTROL-24_ES"):
        if not public_routes.get(key):
            fail(f"missing public route alias: {key}")

    if handoff.get("canonical_state") != "assets/data/control-21-22-24-continuity-v1.json":
        fail("handoff does not point to canonical machine state")
    if handoff.get("scope_state") != "RELATED_CONTINUITY_ACTIVE":
        fail("handoff scope state is not continuity-active")

    protocol_text = PROTOCOL.read_text(encoding="utf-8")
    for phrase in (
        "UNVERIFIED",
        "Two-documents-on-25-June safeguard",
        "Interlinking never transfers knowledge, intent, causation, guilt, liability, procedural status or evidential weight",
    ):
        if phrase not in protocol_text:
            fail(f"protocol safeguard missing: {phrase}")

    print("PASS: PD-C212224-001 continuity graph, bridge safeguards, aliases and handoff are coherent")


if __name__ == "__main__":
    main()

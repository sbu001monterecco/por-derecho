#!/usr/bin/env python3
"""Validate the Concurso 36/2012 accountability triangle continuity control.

This focused gate protects canonical identity, evidence-state, cross-link, public-route,
search and successor-thread invariants. It does not determine the truth or legal
merits of any allegation.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "data/concurso36-accountability-triangle-v1.json"
COMPONENT_PATH = ROOT / "data/control-22-24-interconnection-register.json"
MASTER_PATH = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
OVERLAY_PATH = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER_CONTROL24_OVERLAY_04SEP2026.md"
GOVERNANCE_PATH = ROOT / "governance/prompts/TRIANGLE_CONTROL_21_22_24_CONTINUITY.md"
HANDOVER_PATH = ROOT / "CURRENT_HANDOVER_CONCURSO36_TRIANGLE_04SEP2026.md"
MANIFEST_PATH = ROOT / "publication-manifests/2026-09-04-concurso36-accountability-triangle.json"

ES_PAGE = ROOT / "es/concurso-36-2012-triangulo-responsabilidad/index.html"
EN_PAGE = ROOT / "en/concurso-36-2012-accountability-triangle/index.html"
INTERLINK_JS = ROOT / "assets/control-22-24-interlink-20260904.js"
SEARCH_JS = ROOT / "assets/control-22-24-search-extension-20260904.js"
SITE_JS = ROOT / "assets/site.js"
SITEMAP = ROOT / "sitemap-concurso36-accountability-triangle.xml"
ROBOTS = ROOT / "robots.txt"

ALLOWED_STATES = {
    "VERIFIED_PRIMARY",
    "VERIFIED_PROCEDURAL",
    "PARTY_POSITION",
    "ANALYTICAL_INFERENCE",
    "CONTEXTUAL",
    "OPEN_REFERENCE",
}

REQUIRED_NODES = {
    "C36-NEXUS",
    "PRIVATE-ACTORS",
    "CONTROL-21",
    "GC-CRI-008",
    "ADMINISTRADOR-CONCURSAL",
    "CONTROL-22",
    "GC-CRI-009",
    "GC-PRO-023",
    "AC-SEPARATION-FEES",
    "CONCURSO-JUDGE",
    "CONTROL-24",
    "C24-SUPPLEMENT-25JUN2026",
    "GC-GOV-019",
    "CGPJ-169-AMPLIACION",
    "GC-GOV-020",
    "GC-FIS-017",
    "GC-APP-004",
    "FISCALIA-PERIMETER",
}

REQUIRED_MASTER_IDS = {
    "GC-REF-029",
    "GC-CRI-008",
    "GC-CRI-009",
    "GC-PRO-023",
    "GC-GOV-019",
    "GC-GOV-020",
    "GC-FIS-017",
    "GC-APP-004",
}

REQUIRED_ALIASES = {
    "control 21",
    "nexus 36",
    "dp 1901/2026",
    "control 22",
    "dp 1956/2026",
    "icalpa 80/2026",
    "control 24",
    "25 june 2026",
    "cgpj 169/2026",
    "alzada 286/2026",
    "dip 2/2026",
    "rpl 2523/2025",
    "concurso 36/2012",
}


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing JSON: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
    return {}


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return ""


def require_tokens(path: Path, tokens: list[str], errors: list[str]) -> None:
    text = read_text(path, errors)
    for token in tokens:
        if token not in text:
            errors.append(f"{path.relative_to(ROOT)} missing token: {token}")


def directed_reachable(start: str, adjacency: dict[str, set[str]]) -> set[str]:
    seen = {start}
    queue: deque[str] = deque([start])
    while queue:
        current = queue.popleft()
        for nxt in adjacency.get(current, set()):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def main() -> int:
    errors: list[str] = []

    for required in (
        GRAPH_PATH,
        COMPONENT_PATH,
        MASTER_PATH,
        OVERLAY_PATH,
        GOVERNANCE_PATH,
        HANDOVER_PATH,
        MANIFEST_PATH,
        ES_PAGE,
        EN_PAGE,
        INTERLINK_JS,
        SEARCH_JS,
        SITE_JS,
        SITEMAP,
        ROBOTS,
    ):
        if not required.exists():
            errors.append(f"missing required resource: {required.relative_to(ROOT)}")

    graph = load_json(GRAPH_PATH, errors)
    if not graph:
        print("\n".join(f"ERROR: {item}" for item in errors), file=sys.stderr)
        return 1

    if graph.get("canonical_id") != "PD-C36-ACCOUNTABILITY-TRIANGLE-20260904":
        errors.append("canonical graph ID changed or missing")
    if graph.get("common_nucleus") != "C36-NEXUS":
        errors.append("common nucleus must remain C36-NEXUS")

    declared_states = set(graph.get("evidence_states", []))
    if declared_states != ALLOWED_STATES:
        errors.append(f"evidence state declaration drift: {sorted(declared_states)}")

    nodes = graph.get("nodes", [])
    node_ids = [node.get("id") for node in nodes]
    if None in node_ids or len(node_ids) != len(set(node_ids)):
        errors.append("node IDs must be non-null and unique")
    node_map = {node["id"]: node for node in nodes if node.get("id")}

    missing_nodes = REQUIRED_NODES - set(node_map)
    if missing_nodes:
        errors.append(f"missing canonical nodes: {sorted(missing_nodes)}")

    vertices = graph.get("vertices", [])
    expected_vertices = ["PRIVATE-ACTORS", "ADMINISTRADOR-CONCURSAL", "CONCURSO-JUDGE"]
    if vertices != expected_vertices:
        errors.append(f"triangle vertices changed: {vertices}")
    if "FISCALIA-PERIMETER" in vertices:
        errors.append("Fiscalía must remain outside the three-vertex architecture")

    for node_id, node in node_map.items():
        state = node.get("evidence_state")
        if state not in ALLOWED_STATES:
            errors.append(f"node {node_id} has invalid evidence state {state!r}")

    c24 = node_map.get("CONTROL-24", {})
    if c24.get("is_proceeding") is not False:
        errors.append("CONTROL-24 must remain is_proceeding=false")
    if c24.get("nig") not in (None, ""):
        errors.append("CONTROL-24 must not receive a NIG without source-led governance")
    if c24.get("diligencias_previas") not in (None, ""):
        errors.append("CONTROL-24 must not receive a DP number without source-led governance")
    if c24.get("reparto_status") != "UNRESOLVED":
        errors.append("CONTROL-24 reparto must remain UNRESOLVED until primary proof is controlled")
    if c24.get("master_overlay_id") != "GC-DEC-024":
        errors.append("CONTROL-24 master overlay ID must remain GC-DEC-024")
    if c24.get("filing_date") != "2026-06-18" or c24.get("supplement_date") != "2026-06-25":
        errors.append("CONTROL-24 filing/supplement dates drifted")

    fiscal = node_map.get("FISCALIA-PERIMETER", {})
    if fiscal.get("evidence_state") != "PARTY_POSITION":
        errors.append("Fiscalía perimeter neutralisation/ineffectiveness proposition must remain PARTY_POSITION")
    if not fiscal.get("not_established"):
        errors.append("Fiscalía perimeter must carry an express not-established boundary")

    edges = graph.get("edges", [])
    edge_ids = [edge.get("id") for edge in edges]
    if None in edge_ids or len(edge_ids) != len(set(edge_ids)):
        errors.append("edge IDs must be non-null and unique")

    adjacency: dict[str, set[str]] = defaultdict(set)
    degree: dict[str, int] = defaultdict(int)
    for edge in edges:
        edge_id = edge.get("id", "<unknown>")
        source = edge.get("from")
        target = edge.get("to")
        state = edge.get("evidence_state")
        if source not in node_map or target not in node_map:
            errors.append(f"edge {edge_id} references missing node: {source} -> {target}")
            continue
        if state not in ALLOWED_STATES:
            errors.append(f"edge {edge_id} has invalid evidence state {state!r}")
        adjacency[source].add(target)
        degree[source] += 1
        degree[target] += 1

    orphan_nodes = sorted(node_id for node_id in node_map if degree[node_id] == 0)
    if orphan_nodes:
        errors.append(f"orphan graph nodes: {orphan_nodes}")

    c22_dp1956 = [
        edge for edge in edges
        if edge.get("from") == "CONTROL-22" and edge.get("to") == "GC-CRI-009"
    ]
    if len(c22_dp1956) != 1 or c22_dp1956[0].get("evidence_state") != "OPEN_REFERENCE":
        errors.append("Control 22 -> DP 1956 must exist exactly once and remain OPEN_REFERENCE")

    reachable_c24 = directed_reachable("CONTROL-24", adjacency)
    for expected in ("C24-SUPPLEMENT-25JUN2026", "GC-GOV-019", "CGPJ-169-AMPLIACION", "GC-GOV-020", "GC-FIS-017"):
        if expected not in reachable_c24:
            errors.append(f"Control 24 cannot reach required node {expected}")

    reachable_ac = directed_reachable("ADMINISTRADOR-CONCURSAL", adjacency)
    for expected in ("GC-PRO-023", "AC-SEPARATION-FEES"):
        if expected not in reachable_ac:
            errors.append(f"AC vertex cannot reach required node {expected}")

    reachable_nucleus = directed_reachable("C36-NEXUS", adjacency)
    for expected in ("CONTROL-21", "CONTROL-22", "CONTROL-24", "GC-APP-004"):
        if expected not in reachable_nucleus:
            errors.append(f"common nucleus cannot reach required node {expected}")

    aliases = graph.get("search_aliases", {})
    missing_aliases = REQUIRED_ALIASES - set(aliases)
    if missing_aliases:
        errors.append(f"missing search aliases: {sorted(missing_aliases)}")
    for alias, target in aliases.items():
        if target not in node_map:
            errors.append(f"search alias {alias!r} references unknown node {target!r}")

    component = load_json(COMPONENT_PATH, errors)
    component_nodes = {item.get("node_id"): item for item in component.get("nodes", [])}
    for required in ("control-21-dp-1901", "control-22", "dp-1956-2026", "control-24", "control-24-complement-2026-06-25", "dip-2-2026", "di-169-alzada-286"):
        if required not in component_nodes:
            errors.append(f"component register missing node {required}")
    component_c24 = component_nodes.get("control-24", {})
    identifiers = component_c24.get("official_identifiers", {})
    if any(identifiers.get(key) for key in ("procedure", "nig", "high_court_entry")):
        errors.append("component Control 24 record improperly carries an official proceeding identity")

    master_ids: set[str] = set()
    try:
        with MASTER_PATH.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                value = (row.get("Master_ID") or "").strip()
                if value:
                    master_ids.add(value)
    except FileNotFoundError:
        pass
    missing_master = REQUIRED_MASTER_IDS - master_ids
    if missing_master:
        errors.append(f"Master Register missing referenced IDs: {sorted(missing_master)}")

    overlay_text = read_text(OVERLAY_PATH, errors)
    if "GC-DEC-024" in master_ids:
        if "INTEGRATED_IN_MASTER" not in overlay_text:
            errors.append("GC-DEC-024 exists in Master Register but overlay is not marked INTEGRATED_IN_MASTER")
    else:
        for token in ("GC-DEC-024", "CONTROL-24", "INTAKE_REFERENCE", "Is proceeding", "FALSE", "None established"):
            if token not in overlay_text:
                errors.append(f"Control 24 overlay missing token: {token}")

    require_tokens(GOVERNANCE_PATH, [
        "TRIANGLE_CONTINUITY_GOVERNANCE_GATE",
        "Control 24 is a first-class canonical record",
        "Fiscalía on the perimeter",
        "Control 22 → DP 1956",
        "Successor-thread instruction",
    ], errors)

    require_tokens(ES_PAGE, [
        "PD-C36-ACCOUNTABILITY-TRIANGLE-20260904",
        "Control 21 / NEXUS 36",
        "Control 22",
        "Control 24",
        "CGPJ DI 169",
        "Alzada 286/2026",
        "DIP 2/2026",
        "ICALPA DIP 80/2026",
        "RPL 2523/2025",
        "hipótesis del denunciante",
        "no está probado",
        "GC-DEC-024",
    ], errors)
    require_tokens(EN_PAGE, [
        "PD-C36-ACCOUNTABILITY-TRIANGLE-20260904",
        "Control 21 / NEXUS 36",
        "Control 22",
        "Control 24",
        "CGPJ DI 169",
        "Appeal 286/2026",
        "DIP 2/2026",
        "ICALPA DIP 80/2026",
        "RPL 2523/2025",
        "claimant hypothesis",
        "not established",
        "GC-DEC-024",
    ], errors)

    require_tokens(INTERLINK_JS, [
        "data-concurso36-accountability-triangle",
        "concurso-36-2012-triangulo-responsabilidad",
        "concurso-36-2012-accountability-triangle",
        "Control 24",
        "CGPJ 169",
        "DIP 2/2026",
        "ICALPA 80",
        "neutralización o ineficacia",
        "not established",
    ], errors)
    require_tokens(SEARCH_JS, [
        "CONCURSO36-ACCOUNTABILITY-TRIANGLE-20260904",
        "control 21",
        "nexus 36",
        "dp 1901 2026",
        "control 22",
        "dp 1956 2026",
        "control 24",
        "cgpj 169 2026",
        "alzada 286 2026",
        "dip 2 2026",
        "icalpa 80 2026",
        "rpl 2523 2025",
    ], errors)
    require_tokens(SITE_JS, [
        "control-22-24-interlink-20260904.js",
        "control-22-24-search-extension-20260904.js",
        "20260904b",
    ], errors)
    require_tokens(SITEMAP, [
        "/es/concurso-36-2012-triangulo-responsabilidad/",
        "/en/concurso-36-2012-accountability-triangle/",
    ], errors)
    require_tokens(ROBOTS, ["sitemap-concurso36-accountability-triangle.xml"], errors)
    require_tokens(HANDOVER_PATH, [
        "PD-C36-ACCOUNTABILITY-TRIANGLE-20260904",
        "CONTROL-24",
        "GC-DEC-024",
        "successor",
    ], errors)

    manifest = load_json(MANIFEST_PATH, errors)
    if manifest and manifest.get("release_id") != "PD-C36-ACCOUNTABILITY-TRIANGLE-20260904":
        errors.append("publication manifest release ID drift")

    if errors:
        print("Concurso 36 accountability-triangle validation FAILED", file=sys.stderr)
        for item in errors:
            print(f"ERROR: {item}", file=sys.stderr)
        return 1

    print(
        "Concurso 36 accountability-triangle validation passed: "
        f"{len(nodes)} nodes, {len(edges)} edges, {len(aliases)} aliases, "
        "Control 24 non-proceeding identity locked, bilingual hubs and global discovery present."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

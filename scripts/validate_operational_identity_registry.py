#!/usr/bin/env python3
"""Validate the Por Derecho operational matter-identity registry.

The validator keeps the immutable actor registry, institutional-action matrix,
functional-convergence graph, operational backlog and public bilingual pages in
one referentially consistent control plane.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"

ID_RE = re.compile(r"^PD-SP-(P|O|S|I|R)-\d{4}$")
ACTION_RE = re.compile(r"^PD-SP-ACT-\d{4}$")
IDENTITY_ACTION_RE = re.compile(r"^PD-SP-ID-ACT-\d{4}$")


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostic path
        raise AssertionError(f"Cannot parse JSON {path.relative_to(ROOT)}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_registry() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    index_path = DATA / "matter-identity-registry-v1.json"
    index = load_json(index_path)
    require(index.get("registry_id") == "PD-SP-IDENTITY-REGISTRY-001", "Unexpected registry ID")

    records: dict[str, dict[str, Any]] = {}
    type_counts: dict[str, int] = {}
    for part in index.get("parts", []):
        part_path = DATA / part["path"]
        payload = load_json(part_path)
        expected_type = part["type"]
        require(payload.get("type") == expected_type, f"Type mismatch in {part_path.name}")
        part_records = payload.get("records", [])
        require(len(part_records) == part["count"], f"Count mismatch in {part_path.name}")
        for record in part_records:
            record_id = record.get("id", "")
            require(ID_RE.fullmatch(record_id) is not None, f"Invalid registry ID {record_id!r}")
            require(record_id not in records, f"Duplicate registry ID {record_id}")
            require(record.get("type") == expected_type, f"Record type mismatch for {record_id}")
            require(bool(record.get("name")), f"Missing canonical name for {record_id}")
            records[record_id] = record
            type_counts[expected_type] = type_counts.get(expected_type, 0) + 1

    counts = index.get("counts", {})
    require(len(records) == counts.get("total"), "Registry total count mismatch")
    for type_name, count in type_counts.items():
        require(count == counts.get(type_name), f"Registry count mismatch for {type_name}")

    for record_id, record in records.items():
        for other in record.get("not_same_as", []):
            require(other in records, f"Unknown not_same_as ID {other} referenced by {record_id}")
            require(other != record_id, f"Self-referential not_same_as for {record_id}")

    return index, records


def validate_action_matrix(records: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], set[str]]:
    path = DATA / "criminal-first-institutional-action-matrix-v1.json"
    matrix = load_json(path)
    require(matrix.get("protocol_id") == "PD-SP-ACTION-2011-CONVERGENCE-001", "Unexpected action protocol ID")
    action_ids: set[str] = set()
    for action in matrix.get("actions", []):
        action_id = action.get("action_id", "")
        require(ACTION_RE.fullmatch(action_id) is not None, f"Invalid institutional action ID {action_id}")
        require(action_id not in action_ids, f"Duplicate institutional action ID {action_id}")
        action_ids.add(action_id)
        for field in ("recipients", "actors", "proceedings"):
            for record_id in action.get(field, []):
                require(record_id in records, f"{action_id} references unknown {field} ID {record_id}")
    require(action_ids == {f"PD-SP-ACT-{number:04d}" for number in range(1, 16)}, "Institutional action range is incomplete")
    return matrix, action_ids


def validate_graph(records: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], set[str], set[str]]:
    path = DATA / "acosta-matos-functional-convergence-map-v2.json"
    graph = load_json(path)
    require(graph.get("graph_id") == "PD-SP-GRAPH-AMFC-002", "Unexpected convergence graph ID")

    node_keys: set[str] = set()
    node_registry_ids: set[str] = set()
    for part in graph.get("node_parts", []):
        payload = load_json(DATA / part["path"])
        nodes = payload.get("nodes", [])
        require(len(nodes) == part["count"], f"Node count mismatch in {part['path']}")
        for node in nodes:
            key = node.get("key", "")
            record_id = node.get("registry_id", "")
            require(key and key not in node_keys, f"Duplicate or empty graph node key {key!r}")
            require(record_id in records, f"Graph node {key} references unknown registry ID {record_id}")
            node_keys.add(key)
            node_registry_ids.add(record_id)

    edge_ids: set[str] = set()
    for part in graph.get("edge_parts", []):
        payload = load_json(DATA / part["path"])
        edges = payload.get("edges", [])
        require(len(edges) == part["count"], f"Edge count mismatch in {part['path']}")
        for edge in edges:
            edge_id = edge.get("id", "")
            require(edge_id and edge_id not in edge_ids, f"Duplicate or empty graph edge ID {edge_id!r}")
            require(edge.get("from") in node_keys, f"{edge_id} has unknown source node {edge.get('from')}")
            require(edge.get("to") in node_keys, f"{edge_id} has unknown target node {edge.get('to')}")
            edge_ids.add(edge_id)

    require(len(node_keys) == sum(part["count"] for part in graph.get("node_parts", [])), "Graph node total mismatch")
    require(len(edge_ids) == sum(part["count"] for part in graph.get("edge_parts", [])), "Graph edge total mismatch")
    return graph, node_registry_ids, edge_ids


def validate_operational_control(records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    path = DATA / "matter-identity-operational-control-v1.json"
    control = load_json(path)
    require(control.get("control_id") == "PD-SP-IDENTITY-OPS-001", "Unexpected operational-control ID")
    require(control.get("registry_id") == "PD-SP-IDENTITY-REGISTRY-001", "Operational control points to wrong registry")

    queue_ids: set[str] = set()
    for item in control.get("exact_identity_queue", []):
        record_id = item.get("id", "")
        require(record_id in records, f"Identity queue references unknown ID {record_id}")
        require(record_id not in queue_ids, f"Duplicate identity queue ID {record_id}")
        require(records[record_id].get("status"), f"Identity queue record {record_id} lacks an open status")
        queue_ids.add(record_id)
    require(len(queue_ids) == 14, f"Expected 14 exact-identity queue entries, found {len(queue_ids)}")

    for distinction in control.get("distinction_controls", []):
        ids = distinction.get("ids", [])
        require(len(ids) >= 2, "Distinction control must contain at least two IDs")
        require(all(record_id in records for record_id in ids), f"Distinction references unknown IDs {ids}")

    identity_action_ids: set[str] = set()
    for action in control.get("actions", []):
        action_id = action.get("action_id", "")
        require(IDENTITY_ACTION_RE.fullmatch(action_id) is not None, f"Invalid identity action ID {action_id}")
        require(action_id not in identity_action_ids, f"Duplicate identity action ID {action_id}")
        identity_action_ids.add(action_id)
    require(identity_action_ids == {f"PD-SP-ID-ACT-{number:04d}" for number in range(1, 10)}, "Identity action range is incomplete")

    patterns = [item.get("pattern") for item in control.get("extension_namespaces", [])]
    require(len(patterns) == 12 and len(patterns) == len(set(patterns)), "Evidence-extension namespace list is incomplete or duplicated")
    require(not any("PD-ENT" in json.dumps(item) for item in control.get("extension_namespaces", [])), "Forbidden PD-ENT namespace found")
    return control


def validate_public_surfaces() -> None:
    surfaces = {
        ROOT / "es" / "registro-identidad-materia" / "index.html": [
            "PD-SP-IDENTITY-OPS-001",
            "Una identidad. Un ID. Una cadena operativa.",
            'data-operational-url="../../assets/data/matter-identity-operational-control-v1.json"',
            'data-queue-list="p0"',
            'data-operational-filter="UNRESOLVED"',
            "data-export-json",
            "data-identity-dialog",
        ],
        ROOT / "en" / "matter-identity-registry" / "index.html": [
            "PD-SP-IDENTITY-OPS-001",
            "One identity. One ID. One operational chain.",
            'data-operational-url="../../assets/data/matter-identity-operational-control-v1.json"',
            'data-queue-list="p0"',
            'data-operational-filter="UNRESOLVED"',
            "data-export-json",
            "data-identity-dialog",
        ],
        ROOT / "assets" / "matter-identity-registry.js": [
            "buildOperationalRecords",
            "P0_ROUTE_COVERAGE",
            "matter-identity-operational-control-v1.json" if False else "data-operational-url",
            "exportRecords",
            "PD-SP-ID-ACT-",
        ],
        ROOT / "assets" / "matter-identity-registry.css": [
            ".id-workbench",
            ".id-queue",
            ".id-dialog",
            ".id-action-grid",
            ".id-extension-grid",
        ],
        ROOT / "sitemap-matter-identity-operational.xml": [
            "registro-identidad-materia",
            "matter-identity-registry",
        ],
        ROOT / "robots.txt": ["sitemap-matter-identity-operational.xml"],
    }
    for path, markers in surfaces.items():
        require(path.exists(), f"Missing controlled surface {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            require(marker in text, f"Missing marker {marker!r} in {path.relative_to(ROOT)}")

    manifest = load_json(ROOT / "publication-manifests" / "matter-identity-operational-registry-20260825.json")
    require(manifest.get("current_state") in {"PR_OPEN", "DEPLOYED", "LIVE_VERIFIED"}, "Invalid manifest state")
    for paths in manifest.get("expected_routes", {}).values():
        for relative in paths:
            require((ROOT / relative).exists(), f"Manifest route missing from Git source: {relative}")


def main() -> int:
    try:
        index, records = validate_registry()
        _, action_ids = validate_action_matrix(records)
        _, graph_ids, edge_ids = validate_graph(records)
        control = validate_operational_control(records)
        validate_public_surfaces()
    except AssertionError as exc:
        print(f"OPERATIONAL IDENTITY REGISTRY: FAIL\n - {exc}", file=sys.stderr)
        return 1

    unresolved = sum(1 for record in records.values() if record.get("status"))
    routed = sum(1 for record in records.values() if record.get("routes"))
    print("OPERATIONAL IDENTITY REGISTRY: PASS")
    print(f" - registry: {len(records)} immutable IDs across {len(index.get('parts', []))} classes")
    print(f" - institutional actions: {len(action_ids)}")
    print(f" - graph: {len(graph_ids)} identity-linked nodes, {len(edge_ids)} edges")
    print(f" - exact-identity queue: {len(control.get('exact_identity_queue', []))} records")
    print(f" - direct registry routes: {routed}; open-status records: {unresolved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
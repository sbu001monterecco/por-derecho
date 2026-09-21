#!/usr/bin/env python3
"""Validate the Por Derecho operational matter-identity registry.

The validator keeps the immutable identity registry, institutional-action
matrix, functional-convergence graph, operational backlog and bilingual public
surfaces in one referentially consistent control plane.

The checks are intentionally dependency-free so the same file can run locally
and in GitHub Actions.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"

REGISTRY_SCHEMA = "por-derecho.matter-identity-registry.v1"
PART_SCHEMA = "por-derecho.matter-identity-registry.part.v1"
ACTION_SCHEMA = "por-derecho.criminal-first-institutional-action-matrix.v1"

TYPE_CODES = {
    "PERSON": "P",
    "ORGANISATION": "O",
    "STRUCTURE": "S",
    "INSTITUTION": "I",
    "PROCEEDING": "R",
}

ID_RE = re.compile(r"^PD-SP-(P|O|S|I|R)-\d{4}$")
ACTION_RE = re.compile(r"^PD-SP-ACT-\d{4}$")
IDENTITY_ACTION_RE = re.compile(r"^PD-SP-ID-ACT-\d{4}$")


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostic path
        raise AssertionError(
            f"Cannot parse JSON {path.relative_to(ROOT)}: {exc}"
        ) from exc
    require(isinstance(payload, dict), f"JSON root must be an object: {path.relative_to(ROOT)}")
    return payload


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def normalise(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.casefold()).split())


def validate_string_list(record: dict[str, Any], record_id: str, field: str) -> list[str]:
    values = record.get(field, [])
    require(isinstance(values, list), f"{record_id}.{field} must be an array")
    for value in values:
        require(
            isinstance(value, str) and bool(value.strip()),
            f"{record_id}.{field} must contain only non-empty strings",
        )
    return values


def local_route_target(route: str, record_id: str, language: str) -> Path | None:
    require(
        isinstance(route, str) and bool(route.strip()),
        f"{record_id}.routes.{language} must be a non-empty string",
    )
    if route.startswith(("http://", "https://")):
        return None

    clean = route.split("?", 1)[0].split("#", 1)[0]
    require(clean.startswith("/"), f"{record_id}.routes.{language} must start with '/': {route}")
    require(".." not in Path(clean).parts, f"Unsafe route traversal for {record_id}: {route}")

    target = ROOT / clean.lstrip("/")
    if clean.endswith("/"):
        target /= "index.html"
    return target


def validate_registry() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    index_path = DATA / "matter-identity-registry-v1.json"
    index = load_json(index_path)
    require(index.get("schema") == REGISTRY_SCHEMA, "Unexpected registry index schema")
    require(index.get("registry_id") == "PD-SP-IDENTITY-REGISTRY-001", "Unexpected registry ID")

    formats = index.get("id_formats")
    require(isinstance(formats, dict), "Registry id_formats must be an object")
    for type_name, code in TYPE_CODES.items():
        require(
            formats.get(type_name) == f"PD-SP-{code}-####",
            f"Unexpected declared ID format for {type_name}",
        )

    declared_parts = index.get("parts")
    require(isinstance(declared_parts, list) and declared_parts, "Registry index has no parts")

    records: dict[str, dict[str, Any]] = {}
    type_counts: dict[str, int] = defaultdict(int)
    canonical_by_type: dict[str, dict[str, str]] = defaultdict(dict)
    identity_terms: set[str] = set()

    for descriptor in declared_parts:
        require(isinstance(descriptor, dict), "Registry part descriptor must be an object")
        relative_path = descriptor.get("path")
        require(
            isinstance(relative_path, str) and bool(relative_path),
            "Registry part path must be a non-empty string",
        )
        path_object = Path(relative_path)
        require(
            not path_object.is_absolute() and ".." not in path_object.parts,
            f"Unsafe registry part path: {relative_path}",
        )

        expected_type = descriptor.get("type")
        require(expected_type in TYPE_CODES, f"Unknown registry part type: {expected_type!r}")
        part_path = DATA / path_object
        require(part_path.is_file(), f"Missing registry part: {part_path.relative_to(ROOT)}")

        payload = load_json(part_path)
        require(payload.get("schema") == PART_SCHEMA, f"Unexpected part schema in {relative_path}")
        require(
            payload.get("registry_id") == index.get("registry_id"),
            f"Registry ID mismatch in {relative_path}",
        )
        require(payload.get("type") == expected_type, f"Type mismatch in {relative_path}")

        part_records = payload.get("records")
        require(isinstance(part_records, list), f"records must be an array in {relative_path}")
        require(
            len(part_records) == descriptor.get("count"),
            f"Count mismatch in {relative_path}",
        )

        for record in part_records:
            require(isinstance(record, dict), f"Non-object record in {relative_path}")
            record_id = record.get("id", "")
            record_type = record.get("type")
            name = record.get("name")

            require(
                isinstance(record_id, str) and ID_RE.fullmatch(record_id) is not None,
                f"Invalid registry ID {record_id!r}",
            )
            require(record_id not in records, f"Duplicate registry ID {record_id}")
            require(record_type == expected_type, f"Record type mismatch for {record_id}")
            require(
                record_id.split("-")[2] == TYPE_CODES[expected_type],
                f"ID/type prefix mismatch for {record_id} ({expected_type})",
            )
            require(isinstance(name, str) and bool(name.strip()), f"Missing canonical name for {record_id}")

            canonical_key = normalise(name)
            require(canonical_key, f"Canonical name normalises to empty for {record_id}")
            previous = canonical_by_type[expected_type].get(canonical_key)
            require(
                previous is None,
                f"Duplicate canonical name in {expected_type}: {previous} and {record_id} ({name})",
            )
            canonical_by_type[expected_type][canonical_key] = record_id
            identity_terms.add(canonical_key)

            aliases = validate_string_list(record, record_id, "aliases")
            validate_string_list(record, record_id, "legacy")
            validate_string_list(record, record_id, "not_same_as")
            identity_terms.update(normalise(alias) for alias in aliases)

            if "status" in record:
                require(
                    isinstance(record["status"], str) and bool(record["status"].strip()),
                    f"{record_id}.status must be a non-empty string",
                )
            if "identity_resolution" in record:
                require(
                    isinstance(record["identity_resolution"], str)
                    and bool(record["identity_resolution"].strip()),
                    f"{record_id}.identity_resolution must be a non-empty string",
                )

            routes = record.get("routes", {})
            require(isinstance(routes, dict), f"{record_id}.routes must be an object")
            for language, route in routes.items():
                require(language in {"es", "en"}, f"Unexpected route language for {record_id}: {language}")
                target = local_route_target(route, record_id, language)
                if target is not None:
                    require(
                        target.is_file(),
                        f"Public route target missing for {record_id}: {route}",
                    )

            records[record_id] = record
            type_counts[expected_type] += 1

    counts = index.get("counts")
    require(isinstance(counts, dict), "Registry counts must be an object")
    require(len(records) == counts.get("total"), "Registry total count mismatch")
    for type_name in TYPE_CODES:
        require(
            type_counts.get(type_name, 0) == counts.get(type_name),
            f"Registry count mismatch for {type_name}",
        )

    for record_id, record in records.items():
        for other in record.get("not_same_as", []):
            require(other in records, f"Unknown not_same_as ID {other} referenced by {record_id}")
            require(other != record_id, f"Self-referential not_same_as for {record_id}")
            require(
                record_id in records[other].get("not_same_as", []),
                f"Asymmetric not_same_as control: {record_id} -> {other}",
            )

        if record.get("record_kind") == "PROCEEDING_FAMILY_REFERENCE":
            require(
                record.get("is_exact_proceeding") is False,
                f"{record_id} proceeding-family reference must not be an exact proceeding",
            )
            require(
                record.get("identity_resolution") == "CANONICAL",
                f"{record_id} proceeding-family reference must use canonical-reference resolution",
            )
            require(
                record.get("caret_eligibility")
                == "NOT_ELIGIBLE_AGGREGATE_FAMILY_REFERENCE",
                f"{record_id} aggregate proceeding-family reference must not be caret-eligible",
            )
            exact_ids = record.get("exact_proceeding_ids")
            require(
                isinstance(exact_ids, list) and len(exact_ids) >= 2,
                f"{record_id} proceeding-family reference must identify its exact proceedings",
            )
            for exact_id in exact_ids:
                require(
                    exact_id in records
                    and records[exact_id].get("type") == "PROCEEDING"
                    and records[exact_id].get("record_kind")
                    != "PROCEEDING_FAMILY_REFERENCE",
                    f"{record_id} contains invalid exact proceeding ID {exact_id!r}",
                )

    coverage = index.get("coverage")
    require(isinstance(coverage, dict), "Registry coverage must be an object")
    required_names = coverage.get("required_names")
    require(isinstance(required_names, list), "coverage.required_names must be an array")
    for required_name in required_names:
        require(
            isinstance(required_name, str) and bool(required_name.strip()),
            "coverage.required_names must contain only non-empty strings",
        )
        require(
            normalise(required_name) in identity_terms,
            f"Required identity is not represented by a canonical name or alias: {required_name}",
        )

    return index, records


def validate_action_matrix(
    records: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], set[str]]:
    path = DATA / "criminal-first-institutional-action-matrix-v1.json"
    matrix = load_json(path)
    require(matrix.get("schema") == ACTION_SCHEMA, "Unexpected institutional action matrix schema")
    require(
        matrix.get("protocol_id") == "PD-SP-ACTION-2011-CONVERGENCE-001",
        "Unexpected action protocol ID",
    )

    actions = matrix.get("actions")
    require(isinstance(actions, list), "Institutional actions must be an array")
    action_ids: set[str] = set()

    for action in actions:
        require(isinstance(action, dict), "Institutional action must be an object")
        action_id = action.get("action_id", "")
        require(
            isinstance(action_id, str) and ACTION_RE.fullmatch(action_id) is not None,
            f"Invalid institutional action ID {action_id!r}",
        )
        require(action_id not in action_ids, f"Duplicate institutional action ID {action_id}")
        require(
            action.get("priority") in {"P0", "P1", "P2"},
            f"Unexpected priority for {action_id}: {action.get('priority')!r}",
        )
        action_ids.add(action_id)

        for field in ("recipients", "actors", "proceedings"):
            references = action.get(field, [])
            require(isinstance(references, list), f"{action_id}.{field} must be an array")
            for record_id in references:
                require(
                    isinstance(record_id, str) and record_id in records,
                    f"{action_id} references unknown {field} ID {record_id!r}",
                )
                if field == "actors":
                    require(
                        records[record_id].get("type") == "PERSON",
                        f"{action_id}.actors contains non-person ID {record_id}",
                    )
                elif field == "proceedings":
                    require(
                        records[record_id].get("type") == "PROCEEDING"
                        and records[record_id].get("record_kind")
                        != "PROCEEDING_FAMILY_REFERENCE",
                        f"{action_id}.proceedings contains non-exact proceeding ID {record_id}",
                    )

    require(
        action_ids == {f"PD-SP-ACT-{number:04d}" for number in range(1, 16)},
        "Institutional action range is incomplete",
    )
    return matrix, action_ids


def validate_graph(
    records: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], set[str], set[str]]:
    path = DATA / "acosta-matos-functional-convergence-map-v2.json"
    graph = load_json(path)
    require(graph.get("graph_id") == "PD-SP-GRAPH-AMFC-002", "Unexpected convergence graph ID")

    node_parts = graph.get("node_parts")
    edge_parts = graph.get("edge_parts")
    require(isinstance(node_parts, list), "Graph node_parts must be an array")
    require(isinstance(edge_parts, list), "Graph edge_parts must be an array")

    node_keys: set[str] = set()
    node_registry_ids: set[str] = set()
    for part in node_parts:
        require(isinstance(part, dict), "Graph node-part descriptor must be an object")
        relative = part.get("path")
        require(isinstance(relative, str) and bool(relative), "Graph node-part path is invalid")
        path_object = Path(relative)
        require(
            not path_object.is_absolute() and ".." not in path_object.parts,
            f"Unsafe graph node-part path: {relative}",
        )
        payload = load_json(DATA / path_object)
        nodes = payload.get("nodes")
        require(isinstance(nodes, list), f"Graph nodes must be an array in {relative}")
        require(len(nodes) == part.get("count"), f"Node count mismatch in {relative}")

        for node in nodes:
            require(isinstance(node, dict), f"Non-object graph node in {relative}")
            key = node.get("key", "")
            record_id = node.get("registry_id", "")
            require(
                isinstance(key, str) and bool(key) and key not in node_keys,
                f"Duplicate or empty graph node key {key!r}",
            )
            require(
                record_id in records,
                f"Graph node {key} references unknown registry ID {record_id}",
            )
            node_keys.add(key)
            node_registry_ids.add(record_id)

    edge_ids: set[str] = set()
    for part in edge_parts:
        require(isinstance(part, dict), "Graph edge-part descriptor must be an object")
        relative = part.get("path")
        require(isinstance(relative, str) and bool(relative), "Graph edge-part path is invalid")
        path_object = Path(relative)
        require(
            not path_object.is_absolute() and ".." not in path_object.parts,
            f"Unsafe graph edge-part path: {relative}",
        )
        payload = load_json(DATA / path_object)
        edges = payload.get("edges")
        require(isinstance(edges, list), f"Graph edges must be an array in {relative}")
        require(len(edges) == part.get("count"), f"Edge count mismatch in {relative}")

        for edge in edges:
            require(isinstance(edge, dict), f"Non-object graph edge in {relative}")
            edge_id = edge.get("id", "")
            require(
                isinstance(edge_id, str) and bool(edge_id) and edge_id not in edge_ids,
                f"Duplicate or empty graph edge ID {edge_id!r}",
            )
            require(edge.get("from") in node_keys, f"{edge_id} has unknown source node {edge.get('from')}")
            require(edge.get("to") in node_keys, f"{edge_id} has unknown target node {edge.get('to')}")
            edge_ids.add(edge_id)

    require(
        len(node_keys) == sum(int(part["count"]) for part in node_parts),
        "Graph node total mismatch",
    )
    require(
        len(edge_ids) == sum(int(part["count"]) for part in edge_parts),
        "Graph edge total mismatch",
    )
    return graph, node_registry_ids, edge_ids


def validate_operational_control(records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    path = DATA / "matter-identity-operational-control-v1.json"
    control = load_json(path)
    require(control.get("control_id") == "PD-SP-IDENTITY-OPS-001", "Unexpected operational-control ID")
    require(
        control.get("registry_id") == "PD-SP-IDENTITY-REGISTRY-001",
        "Operational control points to wrong registry",
    )

    exact_queue = control.get("exact_identity_queue")
    require(isinstance(exact_queue, list), "exact_identity_queue must be an array")
    queue_ids: set[str] = set()
    for item in exact_queue:
        require(isinstance(item, dict), "Identity queue item must be an object")
        record_id = item.get("id", "")
        require(record_id in records, f"Identity queue references unknown ID {record_id}")
        require(record_id not in queue_ids, f"Duplicate identity queue ID {record_id}")
        require(records[record_id].get("status"), f"Identity queue record {record_id} lacks an open status")
        require(
            item.get("priority") in {"P0", "P1", "P2"},
            f"Unexpected identity-queue priority for {record_id}",
        )
        queue_ids.add(record_id)

    unresolved_ids = {record_id for record_id, record in records.items() if record.get("status")}
    require(
        queue_ids == unresolved_ids,
        "Exact-identity queue does not match the registry's qualified/unresolved record set",
    )

    resolution_statuses = control.get("resolution_statuses")
    require(isinstance(resolution_statuses, dict), "resolution_statuses must be an object")
    require(
        {"CANONICAL", "CARET_CONFIRMED", "CARET_PENDING_EXACT_ORGAN_AND_CERTIFIED_DOCKET"}
        <= set(resolution_statuses),
        "Proceeding-resolution status set is incomplete",
    )
    for record_id, record in records.items():
        resolution = record.get("identity_resolution")
        if resolution:
            require(
                resolution in resolution_statuses,
                f"Unknown identity_resolution for {record_id}: {resolution}",
            )

    proceeding_queue = control.get("proceeding_identity_queue")
    require(isinstance(proceeding_queue, list), "proceeding_identity_queue must be an array")
    proceeding_queue_ids: set[str] = set()
    for item in proceeding_queue:
        require(isinstance(item, dict), "Proceeding identity queue item must be an object")
        record_id = item.get("id", "")
        require(record_id in records, f"Proceeding identity queue references unknown ID {record_id}")
        require(
            records[record_id].get("type") == "PROCEEDING"
            and records[record_id].get("record_kind")
            != "PROCEEDING_FAMILY_REFERENCE",
            f"Proceeding identity queue contains non-exact proceeding ID {record_id}",
        )
        require(record_id not in proceeding_queue_ids, f"Duplicate proceeding queue ID {record_id}")
        require(
            item.get("priority") in {"P0", "P1", "P2"},
            f"Unexpected proceeding-identity priority for {record_id}",
        )
        proceeding_queue_ids.add(record_id)

    pending_proceeding_ids = {
        record_id
        for record_id, record in records.items()
        if record.get("type") == "PROCEEDING"
        and record.get("record_kind") != "PROCEEDING_FAMILY_REFERENCE"
        and record.get("identity_resolution") not in {None, "CANONICAL", "CARET_CONFIRMED"}
    }
    require(
        proceeding_queue_ids == pending_proceeding_ids,
        "Proceeding-identity queue does not match the registry's pending proceeding set",
    )

    distinctions = control.get("distinction_controls")
    require(isinstance(distinctions, list), "distinction_controls must be an array")
    for distinction in distinctions:
        require(isinstance(distinction, dict), "Distinction control must be an object")
        ids = distinction.get("ids", [])
        require(isinstance(ids, list), "Distinction IDs must be an array")
        require(len(ids) >= 2, "Distinction control must contain at least two IDs")
        require(len(ids) == len(set(ids)), f"Distinction control contains duplicate IDs: {ids}")
        require(all(record_id in records for record_id in ids), f"Distinction references unknown IDs {ids}")

    identity_actions = control.get("actions")
    require(isinstance(identity_actions, list), "Identity actions must be an array")
    identity_action_ids: set[str] = set()
    for action in identity_actions:
        require(isinstance(action, dict), "Identity action must be an object")
        action_id = action.get("action_id", "")
        require(
            isinstance(action_id, str) and IDENTITY_ACTION_RE.fullmatch(action_id) is not None,
            f"Invalid identity action ID {action_id!r}",
        )
        require(action_id not in identity_action_ids, f"Duplicate identity action ID {action_id}")
        require(
            action.get("priority") in {"P0", "P1", "P2"},
            f"Unexpected identity-action priority for {action_id}",
        )
        identity_action_ids.add(action_id)

    require(
        identity_action_ids == {f"PD-SP-ID-ACT-{number:04d}" for number in range(1, 10)},
        "Identity action range is incomplete",
    )

    namespaces = control.get("extension_namespaces")
    require(isinstance(namespaces, list), "extension_namespaces must be an array")
    patterns = [item.get("pattern") for item in namespaces if isinstance(item, dict)]
    require(
        len(patterns) == 12 and len(patterns) == len(set(patterns)),
        "Evidence-extension namespace list is incomplete or duplicated",
    )
    require(
        not any("PD-ENT" in json.dumps(item) for item in namespaces),
        "Forbidden PD-ENT namespace found",
    )
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
            "operationalUrl",
            "exportRecords",
            "renderOperationalActions",
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

    manifest = load_json(
        ROOT / "publication-manifests" / "matter-identity-operational-registry-20260825.json"
    )
    require(
        manifest.get("current_state") in {"PR_OPEN", "DEPLOYED", "LIVE_VERIFIED"},
        "Invalid manifest state",
    )
    expected_routes = manifest.get("expected_routes")
    require(isinstance(expected_routes, dict), "Manifest expected_routes must be an object")
    for paths in expected_routes.values():
        require(isinstance(paths, list), "Manifest route collection must be an array")
        for relative in paths:
            require(isinstance(relative, str) and bool(relative), "Manifest route is invalid")
            require(
                (ROOT / relative).exists(),
                f"Manifest route missing from Git source: {relative}",
            )


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

    unresolved = sum(
        1
        for record in records.values()
        if record.get("status")
        or record.get("identity_resolution") not in {None, "CANONICAL", "CARET_CONFIRMED"}
    )
    routed = sum(1 for record in records.values() if record.get("routes"))
    distinction_edges = sum(len(record.get("not_same_as", [])) for record in records.values()) // 2

    print("OPERATIONAL IDENTITY REGISTRY: PASS")
    print(f" - registry: {len(records)} immutable IDs across {len(index.get('parts', []))} classes")
    print(f" - institutional actions: {len(action_ids)}")
    print(f" - graph: {len(graph_ids)} identity-linked nodes, {len(edge_ids)} edges")
    print(f" - exact-identity queue: {len(control.get('exact_identity_queue', []))} records")
    print(f" - proceeding-identity queue: {len(control.get('proceeding_identity_queue', []))} records")
    print(f" - symmetric non-equivalence controls: {distinction_edges}")
    print(f" - direct registry routes: {routed}; unresolved identity records: {unresolved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

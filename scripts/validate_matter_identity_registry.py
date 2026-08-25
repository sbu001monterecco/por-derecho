#!/usr/bin/env python3
"""Validate the Por Derecho immutable matter identity registry.

The validator is deliberately dependency-free so it can run in GitHub Actions and
locally. It validates identity uniqueness and format, part/index counts,
non-equivalence references, public routes, required-name coverage, and every
identity reference used by the institutional action matrix.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
INDEX_PATH = DATA / "matter-identity-registry-v1.json"
ACTION_PATH = DATA / "criminal-first-institutional-action-matrix-v1.json"
PAGES = [
    ROOT / "es" / "registro-identidad-materia" / "index.html",
    ROOT / "en" / "matter-identity-registry" / "index.html",
]
JS_PATH = ROOT / "assets" / "matter-identity-registry.js"
CSS_PATH = ROOT / "assets" / "matter-identity-registry.css"

TYPE_CODES = {
    "PERSON": "P",
    "ORGANISATION": "O",
    "STRUCTURE": "S",
    "INSTITUTION": "I",
    "PROCEEDING": "R",
}
ID_RE = re.compile(r"^PD-SP-([POSIR])-(\d{4})$")
ACTION_ID_RE = re.compile(r"^PD-SP-ACT-\d{4}$")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {path.relative_to(ROOT)}:{exc.lineno}:{exc.colno}: {exc.msg}")
    raise AssertionError("unreachable")


def norm(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.casefold()).split())


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def route_path(route: str) -> Path | None:
    if route.startswith(("http://", "https://")):
        return None
    clean = route.split("?", 1)[0].split("#", 1)[0]
    if not clean.startswith("/"):
        return Path("__INVALID_RELATIVE_ROUTE__")
    target = ROOT / clean.lstrip("/")
    if clean.endswith("/"):
        target /= "index.html"
    return target


def validate() -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    index = load_json(INDEX_PATH)

    if index.get("schema") != "por-derecho.matter-identity-registry.v1":
        errors.append("unexpected registry index schema")
    registry_id = index.get("registry_id")
    if not registry_id:
        errors.append("registry_id is missing")

    parts: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    declared_parts = index.get("parts") or []
    if not declared_parts:
        errors.append("registry index has no parts")

    for descriptor in declared_parts:
        rel = descriptor.get("path")
        if not isinstance(rel, str) or not rel or Path(rel).name != rel:
            errors.append(f"unsafe or invalid part path: {rel!r}")
            continue
        part_path = DATA / rel
        if not part_path.is_file():
            errors.append(f"missing registry part: assets/data/{rel}")
            continue
        part = load_json(part_path)
        parts.append(part)
        if part.get("schema") != "por-derecho.matter-identity-registry.part.v1":
            errors.append(f"unexpected part schema: {rel}")
        if part.get("registry_id") != registry_id:
            errors.append(f"registry_id mismatch: {rel}")
        if part.get("type") != descriptor.get("type"):
            errors.append(f"part type mismatch: {rel}")
        part_records = part.get("records")
        if not isinstance(part_records, list):
            errors.append(f"records is not an array: {rel}")
            continue
        if descriptor.get("count") != len(part_records):
            errors.append(
                f"part count mismatch for {rel}: declared {descriptor.get('count')}, actual {len(part_records)}"
            )
        for record in part_records:
            if isinstance(record, dict):
                record = {**record, "__part": rel}
            records.append(record)

    by_id: dict[str, dict[str, Any]] = {}
    canonical_by_type: dict[str, dict[str, str]] = defaultdict(dict)
    search_terms: dict[str, set[str]] = defaultdict(set)
    counts: Counter[str] = Counter()

    for position, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            errors.append(f"record #{position} is not an object")
            continue
        record_id = record.get("id")
        record_type = record.get("type")
        name = record.get("name")
        part_name = record.get("__part", "unknown part")
        if not isinstance(record_id, str) or not record_id:
            errors.append(f"record without id in {part_name}")
            continue
        if record_id in by_id:
            errors.append(f"duplicate ID: {record_id}")
        else:
            by_id[record_id] = record
        if record_type not in TYPE_CODES:
            errors.append(f"unknown type for {record_id}: {record_type!r}")
            continue
        counts[record_type] += 1
        match = ID_RE.fullmatch(record_id)
        if not match or match.group(1) != TYPE_CODES[record_type]:
            errors.append(f"ID/type format mismatch: {record_id} ({record_type})")
        expected_prefix = str(index.get("id_formats", {}).get(record_type, "")).replace("####", "")
        if expected_prefix and not record_id.startswith(expected_prefix):
            errors.append(f"ID does not match declared format: {record_id}")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"missing canonical name: {record_id}")
        else:
            key = norm(name)
            previous = canonical_by_type[record_type].get(key)
            if previous and previous != record_id:
                errors.append(f"duplicate canonical name in {record_type}: {previous} and {record_id}: {name}")
            canonical_by_type[record_type][key] = record_id
            search_terms[key].add(record_id)

        for field in ("aliases", "legacy", "not_same_as"):
            value = record.get(field, [])
            if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(f"{record_id}.{field} must be an array of non-empty strings")
        for alias in record.get("aliases", []):
            search_terms[norm(alias)].add(record_id)

        routes = record.get("routes", {})
        if routes is not None and not isinstance(routes, dict):
            errors.append(f"{record_id}.routes must be an object")
        elif isinstance(routes, dict):
            for language, route in routes.items():
                if language not in {"es", "en"}:
                    warnings.append(f"{record_id} has unexpected route language: {language}")
                if not isinstance(route, str) or not route:
                    errors.append(f"{record_id}.routes.{language} is invalid")
                    continue
                target = route_path(route)
                if target == Path("__INVALID_RELATIVE_ROUTE__"):
                    errors.append(f"{record_id}.routes.{language} must start with '/': {route}")
                elif target is not None and not target.is_file():
                    errors.append(f"public route target missing for {record_id}: {route}")

    declared_counts = index.get("counts") or {}
    if declared_counts.get("total") != len(records):
        errors.append(
            f"total count mismatch: declared {declared_counts.get('total')}, actual {len(records)}"
        )
    for record_type in TYPE_CODES:
        if declared_counts.get(record_type) != counts[record_type]:
            errors.append(
                f"{record_type} count mismatch: declared {declared_counts.get(record_type)}, actual {counts[record_type]}"
            )

    for record_id, record in by_id.items():
        for other_id in record.get("not_same_as", []):
            if other_id == record_id:
                errors.append(f"self-reference in not_same_as: {record_id}")
            elif other_id not in by_id:
                errors.append(f"unknown not_same_as reference: {record_id} -> {other_id}")
            elif record_id not in by_id[other_id].get("not_same_as", []):
                warnings.append(f"non-symmetric not_same_as reference: {record_id} -> {other_id}")

    for required_name in index.get("coverage", {}).get("required_names", []):
        key = norm(required_name)
        if not search_terms.get(key):
            errors.append(f"required identity name is not represented: {required_name}")

    # A term shared by multiple IDs is not automatically an error: several legacy
    # graph keys are intentionally shared. Canonical-name/alias collisions are,
    # however, surfaced for human review.
    for key, ids in sorted(search_terms.items()):
        if key and len(ids) > 1:
            canonical_holders = {
                record_id
                for type_map in canonical_by_type.values()
                for canonical_key, record_id in type_map.items()
                if canonical_key == key
            }
            if canonical_holders:
                warnings.append(f"canonical/alias collision '{key}': {', '.join(sorted(ids))}")

    action_matrix = load_json(ACTION_PATH)
    if action_matrix.get("schema") != "por-derecho.criminal-first-institutional-action-matrix.v1":
        errors.append("unexpected institutional action matrix schema")
    action_ids: set[str] = set()
    referenced_identity_ids: set[str] = set()
    for action in action_matrix.get("actions") or []:
        action_id = action.get("action_id")
        if not isinstance(action_id, str) or not ACTION_ID_RE.fullmatch(action_id):
            errors.append(f"invalid action_id: {action_id!r}")
            continue
        if action_id in action_ids:
            errors.append(f"duplicate action_id: {action_id}")
        action_ids.add(action_id)
        if action.get("priority") not in {"P0", "P1", "P2"}:
            errors.append(f"unexpected priority for {action_id}: {action.get('priority')!r}")
        for field in ("recipients", "actors", "proceedings"):
            refs = action.get(field, [])
            if not isinstance(refs, list):
                errors.append(f"{action_id}.{field} must be an array")
                continue
            for ref in refs:
                if ref not in by_id:
                    errors.append(f"unknown identity in action matrix: {action_id}.{field} -> {ref}")
                else:
                    referenced_identity_ids.add(ref)
                if field == "actors" and isinstance(ref, str) and not ref.startswith("PD-SP-P-"):
                    warnings.append(f"non-person actor reference: {action_id}.{field} -> {ref}")
                if field == "proceedings" and isinstance(ref, str) and not ref.startswith("PD-SP-R-"):
                    errors.append(f"non-proceeding reference: {action_id}.{field} -> {ref}")

    required_page_tokens = [
        "data-identity-registry",
        "matter-identity-registry-v1.json",
        "criminal-first-institutional-action-matrix-v1.json",
        "data-control-filter=\"QUALIFIED\"",
        "data-registry-integrity",
    ]
    for page in PAGES:
        if not page.is_file():
            errors.append(f"missing public registry page: {page.relative_to(ROOT)}")
            continue
        html = page.read_text(encoding="utf-8")
        for token in required_page_tokens:
            if token not in html:
                errors.append(f"{page.relative_to(ROOT)} missing required token: {token}")
    for asset in (JS_PATH, CSS_PATH):
        if not asset.is_file() or not asset.read_text(encoding="utf-8").strip():
            errors.append(f"missing or empty registry asset: {asset.relative_to(ROOT)}")

    summary = {
        "registry_id": registry_id,
        "records": len(records),
        "counts": dict(sorted(counts.items())),
        "qualified_records": sum(bool(record.get("status")) for record in by_id.values()),
        "public_routes": sum(bool(record.get("routes")) for record in by_id.values()),
        "actions": len(action_ids),
        "action_linked_identities": len(referenced_identity_ids),
        "warnings": len(set(warnings)),
        "errors": len(set(errors)),
    }
    return sorted(set(errors)), sorted(set(warnings)), summary


def main() -> int:
    errors, warnings, summary = validate()
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"Matter identity registry validation FAILED with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Matter identity registry validation passed with {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

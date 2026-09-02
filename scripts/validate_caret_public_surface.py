#!/usr/bin/env python3
"""Validate CAEPR identity propagation to public editorial surfaces.

The validator deliberately separates:

* canonical identity admission in the federated CAEPR registry;
* source-specific act/capacity attribution;
* public occurrence markup and canonical linking; and
* advisory archive-wide discovery of likely unmarked occurrences.

Strict failures are limited to the finite surfaces declared in
``assets/data/caret-public-surface-coverage-v1.json`` and to objectively invalid
``data-caepr-id`` declarations. Archive-wide exact-name discoveries are reported
as advisory candidates unless ``--fail-on-advisory`` is supplied.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
CONTROL_PATH = DATA / "caret-public-surface-coverage-v1.json"
REGISTRY_PATH = DATA / "matter-identity-registry-v1.json"
QUEUE_PATH = DATA / "justice-professionals-evidence-production-queue-v1.json"
LA_LAGUNA_GAPS_PATH = DATA / "la-laguna-judicial-actors-gap-closure-audit-v1.json"

CONTROL_SCHEMA = "por-derecho.caret-public-surface-coverage.v1"
REGISTRY_SCHEMA = "por-derecho.matter-identity-registry.v1"
PART_SCHEMA = "por-derecho.matter-identity-registry.part.v1"

TAG_RE = re.compile(r"<[^>]+>", re.S)
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.I | re.S)
DECLARATION_TAG_RE = re.compile(r"<[^>]*\bdata-caepr-id\s*=\s*([\"'])(?P<id>[^\"']+)\1[^>]*>", re.I | re.S)
DECLARED_ELEMENT_RE = re.compile(
    r"<(?P<tag>a|span|strong|div|article|li|p)\b"
    r"(?P<attrs>[^>]*\bdata-caepr-id\s*=\s*([\"'])(?P<id>[^\"']+)\3[^>]*)>"
    r"(?P<body>.*?)</(?P=tag)>",
    re.I | re.S,
)
ATTRIBUTE_RE = re.compile(r"(?P<name>[A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*([\"'])(?P<value>.*?)\2", re.S)
CARET_RE = re.compile(r"<sup\b[^>]*>\s*\^\s*</sup>", re.I | re.S)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostic path
        raise AssertionError(f"Cannot parse {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(payload, dict):
        raise AssertionError(f"JSON root must be an object: {path.relative_to(ROOT)}")
    return payload


def safe_repo_path(relative: str, errors: list[str], label: str) -> Path | None:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        errors.append(f"Unsafe {label} path: {relative!r}")
        return None
    return ROOT / candidate


def load_registry(errors: list[str]) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    index = load_json(REGISTRY_PATH)
    require(index.get("schema") == REGISTRY_SCHEMA, "Unexpected registry schema", errors)
    require(index.get("registry_id") == "PD-SP-IDENTITY-REGISTRY-001", "Unexpected registry ID", errors)

    records: dict[str, dict[str, Any]] = {}
    for descriptor in index.get("parts", []):
        if not isinstance(descriptor, dict):
            errors.append("Registry part descriptor must be an object")
            continue
        relative = descriptor.get("path")
        if not isinstance(relative, str) or not relative:
            errors.append("Registry part path must be a non-empty string")
            continue
        path = safe_repo_path(f"assets/data/{relative}", errors, "registry part")
        if path is None or not path.is_file():
            errors.append(f"Missing registry part: {relative}")
            continue
        part = load_json(path)
        require(part.get("schema") == PART_SCHEMA, f"Unexpected part schema: {relative}", errors)
        require(part.get("registry_id") == index.get("registry_id"), f"Registry ID mismatch: {relative}", errors)
        part_records = part.get("records")
        if not isinstance(part_records, list):
            errors.append(f"Registry records must be an array: {relative}")
            continue
        require(len(part_records) == descriptor.get("count"), f"Registry count mismatch: {relative}", errors)
        for record in part_records:
            if not isinstance(record, dict):
                errors.append(f"Non-object registry record: {relative}")
                continue
            record_id = record.get("id")
            if not isinstance(record_id, str) or not record_id:
                errors.append(f"Registry record without ID: {relative}")
                continue
            if record_id in records:
                errors.append(f"Duplicate registry ID: {record_id}")
                continue
            records[record_id] = record

    declared_total = index.get("counts", {}).get("total")
    require(len(records) == declared_total, f"Registry total mismatch: loaded {len(records)}, declared {declared_total}", errors)
    return index, records


def parse_attributes(raw: str) -> dict[str, str]:
    return {match.group("name").casefold(): html.unescape(match.group("value")) for match in ATTRIBUTE_RE.finditer(raw)}


def text_content(fragment: str) -> str:
    without_scripts = SCRIPT_STYLE_RE.sub(" ", fragment)
    without_tags = TAG_RE.sub(" ", without_scripts)
    return " ".join(html.unescape(without_tags).split())


def iter_declared_elements(document: str) -> Iterable[dict[str, Any]]:
    for match in DECLARED_ELEMENT_RE.finditer(document):
        attrs = parse_attributes(match.group("attrs"))
        yield {
            "tag": match.group("tag").casefold(),
            "id": match.group("id"),
            "attrs": attrs,
            "body": match.group("body"),
            "text": text_content(match.group("body")),
            "has_caret": bool(CARET_RE.search(match.group("body"))),
        }


def validate_all_declarations(
    public_files: list[Path], records: dict[str, dict[str, Any]], errors: list[str]
) -> tuple[int, Counter[str]]:
    declaration_count = 0
    state_counts: Counter[str] = Counter()

    for path in public_files:
        document = path.read_text(encoding="utf-8", errors="replace")
        relative = path.relative_to(ROOT).as_posix()

        for tag_match in DECLARATION_TAG_RE.finditer(document):
            declaration_count += 1
            record_id = tag_match.group("id")
            record = records.get(record_id)
            require(record is not None, f"{relative}: unknown data-caepr-id {record_id}", errors)

        for element in iter_declared_elements(document):
            record_id = element["id"]
            record = records.get(record_id)
            if record is None:
                continue
            declared_state = element["attrs"].get("data-caret-state", "")
            registry_state = str(record.get("identity_resolution") or record.get("status") or "")
            if declared_state:
                state_counts[declared_state] += 1
            if declared_state == "CARET_CONFIRMED":
                require(
                    registry_state == "CARET_CONFIRMED",
                    f"{relative}: {record_id} declared CARET_CONFIRMED but registry state is {registry_state or 'unset'}",
                    errors,
                )
            if element["has_caret"] and registry_state in {"CARET_PENDING", "CARET_SUSPENDED"}:
                errors.append(
                    f"{relative}: {record_id} is {registry_state} but its declared element renders a visible caret"
                )
    return declaration_count, state_counts


def validate_strict_surfaces(
    control: dict[str, Any], records: dict[str, dict[str, Any]], errors: list[str]
) -> tuple[int, int]:
    surface_count = 0
    row_count = 0
    languages: dict[str, set[str]] = {}

    strict_surfaces = control.get("strict_surfaces")
    if not isinstance(strict_surfaces, list) or not strict_surfaces:
        errors.append("Control strict_surfaces must be a non-empty array")
        return 0, 0

    for surface in strict_surfaces:
        if not isinstance(surface, dict):
            errors.append("Strict surface must be an object")
            continue
        relative = surface.get("path")
        language = surface.get("language")
        if not isinstance(relative, str) or not relative:
            errors.append("Strict surface path must be a non-empty string")
            continue
        path = safe_repo_path(relative, errors, "strict surface")
        if path is None or not path.is_file():
            errors.append(f"Missing strict public surface: {relative}")
            continue
        document = path.read_text(encoding="utf-8", errors="replace")
        declared = list(iter_declared_elements(document))
        surface_count += 1
        surface_ids: set[str] = set()

        rows = surface.get("records")
        if not isinstance(rows, list) or not rows:
            errors.append(f"{relative}: records must be a non-empty array")
            continue

        for row in rows:
            row_count += 1
            if not isinstance(row, dict):
                errors.append(f"{relative}: strict record row must be an object")
                continue
            record_id = row.get("id")
            display_name = row.get("display_name")
            required_state = row.get("required_state")
            required_href = row.get("required_href")
            minimum = row.get("minimum_declared_occurrences", 1)

            if not isinstance(record_id, str) or not record_id:
                errors.append(f"{relative}: strict row without an ID")
                continue
            record = records.get(record_id)
            require(record is not None, f"{relative}: strict row references unknown ID {record_id}", errors)
            if record is None:
                continue
            surface_ids.add(record_id)

            require(required_state == "CARET_CONFIRMED", f"{relative}: strict state must be CARET_CONFIRMED for {record_id}", errors)
            require(
                record.get("identity_resolution") == "CARET_CONFIRMED",
                f"{relative}: {record_id} is not CARET_CONFIRMED in the registry",
                errors,
            )
            if isinstance(display_name, str):
                allowed_names = {str(record.get("name", "")), *[str(alias) for alias in record.get("aliases", [])]}
                require(
                    display_name in allowed_names,
                    f"{relative}: display_name {display_name!r} is not canonical or an alias for {record_id}",
                    errors,
                )
            else:
                errors.append(f"{relative}: display_name missing for {record_id}")
                display_name = ""

            matching = []
            for element in declared:
                if element["id"] != record_id:
                    continue
                attrs = element["attrs"]
                if attrs.get("data-caret-state") != required_state:
                    continue
                if required_href and attrs.get("href") != required_href:
                    continue
                if display_name and display_name not in element["text"]:
                    continue
                if not element["has_caret"]:
                    continue
                if record_id not in element["text"]:
                    continue
                matching.append(element)

            require(
                isinstance(minimum, int) and minimum >= 1,
                f"{relative}: invalid minimum_declared_occurrences for {record_id}",
                errors,
            )
            if isinstance(minimum, int):
                require(
                    len(matching) >= minimum,
                    f"{relative}: {record_id} has {len(matching)} compliant declared occurrences; requires {minimum}",
                    errors,
                )

        if isinstance(language, str):
            languages[language] = surface_ids

    if "es" in languages and "en" in languages:
        require(
            languages["es"] == languages["en"],
            f"Strict ES/EN identity parity mismatch: es={sorted(languages['es'])}, en={sorted(languages['en'])}",
            errors,
        )
    return surface_count, row_count


def validate_source_gap_reuse(
    control: dict[str, Any], records: dict[str, dict[str, Any]], errors: list[str]
) -> None:
    queue = load_json(QUEUE_PATH)
    task_ids = {
        item.get("task_id")
        for item in queue.get("production_queue", [])
        if isinstance(item, dict) and isinstance(item.get("task_id"), str)
    }
    laguna = load_json(LA_LAGUNA_GAPS_PATH)
    laguna_ids = {
        item.get("gap_id")
        for item in laguna.get("gaps", [])
        if isinstance(item, dict) and isinstance(item.get("gap_id"), str)
    }
    reusable_refs = task_ids | laguna_ids

    pending_rows = control.get("named_caret_pending_reused", [])
    if not isinstance(pending_rows, list):
        errors.append("named_caret_pending_reused must be an array")
        pending_rows = []
    for row in pending_rows:
        if not isinstance(row, dict):
            errors.append("named_caret_pending_reused row must be an object")
            continue
        record_id = row.get("id")
        task_id = row.get("existing_task")
        record = records.get(str(record_id))
        require(record is not None, f"Pending row references unknown ID {record_id}", errors)
        if record is not None:
            require(
                record.get("identity_resolution") == "CARET_PENDING",
                f"{record_id} must remain CARET_PENDING until its source trigger is met",
                errors,
            )
        require(task_id in task_ids, f"Pending row references unknown production task {task_id}", errors)

    gap_rows = control.get("unknown_actor_source_gap_families_reused", [])
    if not isinstance(gap_rows, list):
        errors.append("unknown_actor_source_gap_families_reused must be an array")
        gap_rows = []
    for row in gap_rows:
        if not isinstance(row, dict):
            errors.append("unknown_actor_source_gap_families_reused row must be an object")
            continue
        reference = row.get("reference")
        require(reference in reusable_refs, f"Unknown reused source-gap reference {reference}", errors)


def collect_public_files(control: dict[str, Any]) -> tuple[list[Path], list[str]]:
    policy = control.get("candidate_scan_policy", {})
    roots = policy.get("roots", ["es", "en"])
    excluded = [str(value) for value in policy.get("excluded_path_fragments", [])]
    files: list[Path] = []
    skipped: list[str] = []

    for root_name in roots:
        root_path = safe_repo_path(str(root_name), skipped, "scan root")
        if root_path is None or not root_path.is_dir():
            skipped.append(f"Missing scan root: {root_name}")
            continue
        for path in root_path.rglob("*.html"):
            relative = "/" + path.relative_to(ROOT).as_posix()
            if any(fragment in relative for fragment in excluded):
                continue
            try:
                if path.stat().st_size > 2_000_000:
                    skipped.append(f"Skipped over-size HTML: {relative.lstrip('/')}")
                    continue
            except OSError as exc:
                skipped.append(f"Cannot stat {relative.lstrip('/')}: {exc}")
                continue
            files.append(path)
    return sorted(set(files)), skipped


def advisory_candidates(
    control: dict[str, Any], records: dict[str, dict[str, Any]], public_files: list[Path]
) -> list[dict[str, Any]]:
    policy = control.get("candidate_scan_policy", {})
    minimum_length = int(policy.get("minimum_canonical_name_length", 8))

    terms: list[tuple[str, str, str]] = []
    for record_id, record in records.items():
        if record.get("identity_resolution") != "CARET_CONFIRMED":
            continue
        canonical = record.get("name")
        if not isinstance(canonical, str) or len(canonical.strip()) < minimum_length:
            continue
        terms.append((record_id, canonical, "canonical"))
        for alias in record.get("aliases", []):
            if isinstance(alias, str) and len(alias.strip()) >= minimum_length:
                terms.append((record_id, alias, "alias"))

    candidates: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for path in public_files:
        document = path.read_text(encoding="utf-8", errors="replace")
        editorial_text = text_content(document)
        declared_ids = {match.group("id") for match in DECLARATION_TAG_RE.finditer(document)}
        relative = path.relative_to(ROOT).as_posix()
        for record_id, term, term_kind in terms:
            key = (relative, record_id)
            if key in seen or record_id in declared_ids:
                continue
            count = editorial_text.count(term)
            if count:
                seen.add(key)
                candidates.append(
                    {
                        "path": relative,
                        "identity_id": record_id,
                        "canonical_name": records[record_id].get("name"),
                        "matched_term": term,
                        "term_kind": term_kind,
                        "exact_occurrence_count": count,
                        "state": "ADVISORY_REVIEW_REQUIRED",
                        "boundary": "Exact-name discovery is not automatic authority to edit or promote the page. Review quotation/source context and first-reference policy.",
                    }
                )
    return candidates


def validate_control_shape(control: dict[str, Any], errors: list[str]) -> None:
    require(control.get("schema") == CONTROL_SCHEMA, "Unexpected caret public-surface control schema", errors)
    require(control.get("control_id") == "PD-SP-CARET-SURFACE-20260902-01", "Unexpected control ID", errors)
    base_sha = control.get("base_main_sha")
    require(isinstance(base_sha, str) and re.fullmatch(r"[0-9a-f]{40}", base_sha) is not None, "base_main_sha must be a full commit SHA", errors)

    for key in ("governance", "parent_governance", "validator", "workflow", "registry_authority", "source_gap_authority"):
        value = control.get(key)
        require(isinstance(value, str) and bool(value), f"Control {key} must be a path", errors)
        if isinstance(value, str) and value:
            path = safe_repo_path(value, errors, key)
            if path is not None:
                require(path.is_file(), f"Control path does not exist: {value}", errors)

    gap_rows = control.get("resolved_occurrence_gaps", [])
    strict_rows = sum(len(surface.get("records", [])) for surface in control.get("strict_surfaces", []) if isinstance(surface, dict))
    require(isinstance(gap_rows, list), "resolved_occurrence_gaps must be an array", errors)
    if isinstance(gap_rows, list):
        require(len(gap_rows) == strict_rows, "Each initial strict surface/identity row must have one resolved occurrence-gap record", errors)
        for row in gap_rows:
            if isinstance(row, dict):
                require(
                    row.get("state") == "REPAIRED_ON_IMPLEMENTATION_BRANCH",
                    f"Unexpected resolved gap state for {row.get('gap_id')}",
                    errors,
                )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "artifacts" / "caret-public-surface-audit" / "report.json",
        help="JSON artifact path (default: artifacts/caret-public-surface-audit/report.json)",
    )
    parser.add_argument(
        "--fail-on-advisory",
        action="store_true",
        help="Treat every archive-wide advisory candidate as a failure after false-positive review.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    control = load_json(CONTROL_PATH)
    validate_control_shape(control, errors)
    registry_index, records = load_registry(errors)
    validate_source_gap_reuse(control, records, errors)

    public_files, skipped = collect_public_files(control)
    declaration_count, declaration_states = validate_all_declarations(public_files, records, errors)
    strict_surface_count, strict_row_count = validate_strict_surfaces(control, records, errors)
    candidates = advisory_candidates(control, records, public_files)

    if args.fail_on_advisory and candidates:
        errors.append(f"Archive-wide advisory candidates remain: {len(candidates)}")

    report = {
        "schema": "por-derecho.caret-public-surface-validation-report.v1",
        "control_id": control.get("control_id"),
        "base_main_sha": control.get("base_main_sha"),
        "registry_id": registry_index.get("registry_id"),
        "registry_record_count": len(records),
        "strict_surface_count": strict_surface_count,
        "strict_surface_identity_rows": strict_row_count,
        "public_html_files_scanned": len(public_files),
        "machine_readable_declaration_count": declaration_count,
        "declaration_state_counts": dict(sorted(declaration_states.items())),
        "advisory_candidate_count": len(candidates),
        "advisory_candidates": candidates,
        "skipped": skipped,
        "strict_errors": errors,
        "result": "PASS" if not errors else "FAIL",
        "mode": "STRICT_DECLARED_SURFACES_PLUS_ADVISORY_ARCHIVE_DISCOVERY",
    }

    report_path = args.report
    if not report_path.is_absolute():
        report_path = ROOT / report_path
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({key: value for key, value in report.items() if key != "advisory_candidates"}, ensure_ascii=False, indent=2))
    if candidates:
        print(f"ADVISORY: {len(candidates)} exact-name page/identity candidates written to {report_path.relative_to(ROOT)}")
    if errors:
        print("STRICT FAILURES:", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1
    print("CARET PUBLIC-SURFACE PROPAGATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

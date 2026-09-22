#!/usr/bin/env python3
"""Fail closed on noncanonical references to UK company 07716847."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULE = ROOT / "ops/AWESWELL_CANONICAL_NAME_RULE_27AUG2026.json"
REGISTER = ROOT / "ops/CANONICAL_ENTITY_NAMES.json"
MATTER_REGISTER = ROOT / "assets/data/matter-identity-registry-v1.organisations.json"
EXCEPTIONS = ROOT / "ops/AWESWELL_IDENTITY_EXCEPTION_REGISTRY_22SEP2026.json"
EXCEPTION_REL = EXCEPTIONS.relative_to(ROOT).as_posix()
TEXT_SUFFIXES = {
    ".md", ".txt", ".html", ".htm", ".json", ".jsonl", ".csv",
    ".tsv", ".xml", ".yml", ".yaml", ".py", ".js", ".mjs", ".cjs", ".css",
}
DISTINCT_ENTITY = re.compile(
    r"(?<![A-Za-z0-9])OS" r"WELL\s+426\s+S\.?\s*L\.?(?![A-Za-z0-9])",
    re.IGNORECASE,
)
ALLOWED_CATEGORIES = {
    "CONTROL_DEFINITION",
    "NEGATIVE_TEST",
    "LABELLED_SOURCE_LITERAL",
    "LABELLED_CORRECTION_RECORD",
}


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def forbidden_variants(rule: dict) -> list[str]:
    values = rule.get("forbidden_generated_aliases") or []
    if not values or not all(isinstance(value, str) and value for value in values):
        raise ValueError("canonical rule has no valid forbidden_generated_aliases")
    unique: dict[str, str] = {}
    for value in values:
        unique.setdefault(value.casefold(), value)
    return sorted(unique.values(), key=len, reverse=True)


def forbidden_pattern(rule: dict) -> re.Pattern[str]:
    alternatives = "|".join(re.escape(value) for value in forbidden_variants(rule))
    return re.compile(rf"(?<![A-Za-z])(?:{alternatives})(?![A-Za-z])", re.IGNORECASE)


def distinct_entity_hit(line: str, hit: re.Match[str]) -> bool:
    return any(
        match.start() <= hit.start() and hit.end() <= match.end()
        for match in DISTINCT_ENTITY.finditer(line)
    )


def load_line_exceptions(errors: list[str]) -> list[dict]:
    data = load_json(EXCEPTIONS)
    if data.get("schema") != "por-derecho.aweswell-identity-exceptions.v2":
        errors.append("identity exception registry schema mismatch")
    if set(data.get("allowed_categories") or []) != ALLOWED_CATEGORIES:
        errors.append("identity exception category set mismatch")

    result: list[dict] = []
    occupied: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for index, item in enumerate(data.get("line_exceptions") or []):
        label = f"identity exception #{index + 1}"
        if not isinstance(item, dict):
            errors.append(f"{label} is not an object")
            continue
        path = item.get("path")
        start = item.get("start_line")
        end = item.get("end_line")
        category = item.get("category")
        literals = item.get("allowed_literals")
        expected = item.get("expected_matches")
        if not isinstance(path, str) or not path or path.startswith("/") or ".." in Path(path).parts:
            errors.append(f"{label} has an unsafe path")
            continue
        if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start:
            errors.append(f"{label} has invalid line bounds")
            continue
        if category not in ALLOWED_CATEGORIES:
            errors.append(f"{label} has invalid category")
        if not item.get("label") or not item.get("justification"):
            errors.append(f"{label} requires a label and justification")
        if not isinstance(literals, list) or not literals or not all(isinstance(v, str) and v for v in literals):
            errors.append(f"{label} has invalid allowed_literals")
            continue
        if not isinstance(expected, int) or expected < 1:
            errors.append(f"{label} has invalid expected_matches")
            continue
        target = ROOT / path
        if not target.is_file():
            errors.append(f"{label} target is missing: {path}")
            continue
        line_count = len(target.read_text(encoding="utf-8", errors="replace").splitlines())
        if end > line_count:
            errors.append(f"{label} exceeds {path} line count {line_count}")
        for prior_start, prior_end in occupied[path]:
            if max(start, prior_start) <= min(end, prior_end):
                errors.append(f"{label} overlaps another exception in {path}")
        occupied[path].append((start, end))
        result.append(item)
    return result


def matching_exception(
    path: str,
    line_number: int,
    literal: str,
    exceptions: list[dict],
) -> int | None:
    for index, item in enumerate(exceptions):
        if item["path"] != path:
            continue
        if not item["start_line"] <= line_number <= item["end_line"]:
            continue
        if literal not in item["allowed_literals"]:
            continue
        return index
    return None


def scan_text(
    text: str,
    path: str,
    pattern: re.Pattern[str],
    exceptions: list[dict] | None = None,
    usage: dict[int, int] | None = None,
) -> list[str]:
    errors: list[str] = []
    exceptions = exceptions or []
    usage = usage if usage is not None else {}
    for line_number, line in enumerate(text.splitlines(), 1):
        for hit in pattern.finditer(line):
            if distinct_entity_hit(line, hit):
                continue
            exception_index = matching_exception(
                path,
                line_number,
                hit.group(0),
                exceptions,
            )
            if exception_index is not None:
                usage[exception_index] = usage.get(exception_index, 0) + 1
                expected = exceptions[exception_index]["expected_matches"]
                if usage[exception_index] > expected:
                    errors.append(
                        f"{path}:{line_number}: exception match count exceeds {expected} "
                        f"for {exceptions[exception_index]['label']}"
                    )
                continue
            errors.append(
                f"{path}:{line_number}: unclassified forbidden identity variant {hit.group(0)!r}"
            )
    return errors


def repository_files() -> list[Path]:
    output = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    paths: list[Path] = []
    for raw in output.split(b"\0"):
        if not raw:
            continue
        path = ROOT / raw.decode()
        if path.suffix.lower() in TEXT_SUFFIXES and path.is_file():
            paths.append(path)
    return paths


def validate_controls(rule: dict, errors: list[str]) -> None:
    register = load_json(REGISTER)
    records = register.get("records") or []
    entity = next((item for item in records if item.get("id") == "E005"), None)
    if not entity or entity.get("identifier", {}).get("value") != "07716847":
        errors.append("canonical register E005/company 07716847 missing")
    if not entity or entity.get("canonical_name") != "AWESWELL LIMITED":
        errors.append("canonical register current name mismatch")
    if not entity or entity.get("official_registered_name") != "AWESWELL LIMITED":
        errors.append("canonical register official name mismatch")
    if rule.get("entity", {}).get("canonical_name") != "AWESWELL LIMITED":
        errors.append("canonical-name rule current name mismatch")
    if rule.get("entity", {}).get("company_number") != "07716847":
        errors.append("canonical-name rule company number mismatch")

    matter = load_json(MATTER_REGISTER)
    matter_entity = next(
        (item for item in matter.get("records") or [] if item.get("id") == "PD-SP-O-0001"),
        None,
    )
    if not matter_entity or matter_entity.get("name") != "AWESWELL LIMITED":
        errors.append("matter identity registry current name mismatch")
    if not matter_entity or matter_entity.get("company_number") != "07716847":
        errors.append("matter identity registry company number mismatch")
    if not matter_entity or matter_entity.get("aliases") != []:
        errors.append("AWESWELL LIMITED must have no current-name aliases")

    required = {
        "Os" + "well",
        "Os" + "well Limited",
        "Awe" + "sell",
        "Aws" + "well",
        "Awes" + "wel",
        "Awes" + "welll",
    }
    present = set(rule.get("forbidden_generated_aliases") or [])
    if not required <= present:
        errors.append("canonical-name rule is missing required forbidden variants")


def validate_repository(rule: dict, errors: list[str]) -> None:
    exceptions = load_line_exceptions(errors)
    usage: dict[int, int] = {}
    pattern = forbidden_pattern(rule)
    for path in repository_files():
        relative = path.relative_to(ROOT).as_posix()
        if relative == EXCEPTION_REL:
            continue
        errors.extend(
            scan_text(
                path.read_text(encoding="utf-8", errors="replace"),
                relative,
                pattern,
                exceptions,
                usage,
            )
        )
    for index, item in enumerate(exceptions):
        actual = usage.get(index, 0)
        expected = item["expected_matches"]
        if actual != expected:
            errors.append(
                f"unused or drifted exception {item['path']}:{item['start_line']}-"
                f"{item['end_line']} ({item['label']}): expected {expected}, found {actual}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--all", action="store_true", help="scan every tracked text file")
    mode.add_argument("--outbound", nargs="*", help="scan draft files; use '-' for stdin")
    args = parser.parse_args()

    errors: list[str] = []
    try:
        rule = load_json(RULE)
        validate_controls(rule, errors)
        pattern = forbidden_pattern(rule)
        if args.all:
            validate_repository(rule, errors)
        else:
            targets = args.outbound or ["-"]
            for target in targets:
                text = sys.stdin.read() if target == "-" else Path(target).read_text(encoding="utf-8")
                errors.extend(scan_text(text, target, pattern))
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        errors.append(f"validator control failure: {exc}")

    if errors:
        print("AWESWELL identity validation FAILED", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1
    print("AWESWELL identity validation PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

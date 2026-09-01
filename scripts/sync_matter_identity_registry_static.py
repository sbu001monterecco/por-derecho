#!/usr/bin/env python3
"""Synchronize derived identity-registry surfaces from the canonical JSON.

Canonical source:
  assets/data/matter-identity-registry-v1.json

Derived surfaces:
  en/matter-identity-registry/index.html
  es/registro-identidad-materia/index.html
  ops/CURRENT_UNITARY_STATE.json
  scripts/validate_dp3205_2014_publication.py (legacy date migration only)

The synchronizer is intentionally structural: it updates named metadata, JSON-LD,
static counters and the bounded coverage sentences without depending on one exact
editorial suffix.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assets/data/matter-identity-registry-v1.json"
EN_PAGE = ROOT / "en/matter-identity-registry/index.html"
ES_PAGE = ROOT / "es/registro-identidad-materia/index.html"
UNITARY_STATE = ROOT / "ops/CURRENT_UNITARY_STATE.json"
DP3205_VALIDATOR = ROOT / "scripts/validate_dp3205_2014_publication.py"

TYPES = ("PERSON", "ORGANISATION", "STRUCTURE", "INSTITUTION", "PROCEEDING")
EN_MONTHS = {
    1: "JANUARY", 2: "FEBRUARY", 3: "MARCH", 4: "APRIL",
    5: "MAY", 6: "JUNE", 7: "JULY", 8: "AUGUST",
    9: "SEPTEMBER", 10: "OCTOBER", 11: "NOVEMBER", 12: "DECEMBER",
}
ES_MONTHS = {
    1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
    5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
    9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE",
}


class SyncError(RuntimeError):
    """Fail-closed synchronization error."""


def load_object(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SyncError(f"cannot read {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise SyncError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def replace_exactly_once(
    text: str,
    pattern: str,
    replacement: str | Callable[[re.Match[str]], str],
    label: str,
) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.DOTALL)
    if count != 1:
        raise SyncError(f"{label}: expected exactly one match, observed {count}")
    return updated


def iso_and_human_dates(control_date: str) -> tuple[str, str]:
    match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", control_date)
    if not match:
        raise SyncError(f"invalid registry control_date: {control_date!r}")
    year, month, day = (int(part) for part in match.groups())
    if month not in EN_MONTHS or not 1 <= day <= 31:
        raise SyncError(f"invalid registry control_date: {control_date!r}")
    return (
        f"{day} {EN_MONTHS[month]} {year}",
        f"{day} {ES_MONTHS[month]} {year}",
    )


def synchronize_page(
    path: Path,
    language: str,
    counts: dict[str, int],
    control_date: str,
) -> str:
    text = path.read_text(encoding="utf-8")
    total = counts["total"]
    people = counts["PERSON"]
    organisations = counts["ORGANISATION"]
    structures = counts["STRUCTURE"]
    institutions = counts["INSTITUTION"]
    proceedings = counts["PROCEEDING"]
    marker = f"{total}-{people}-{organisations}-{structures}-{institutions}-{proceedings}"
    en_date, es_date = iso_and_human_dates(control_date)

    if language == "en":
        meta = (
            f"Operational Por Derecho register of {total} immutable IDs: {people} people, "
            f"{organisations} organisations, {structures} structures, {institutions} institutions "
            f"and {proceedings} proceedings"
        )
        og = (
            f"{total} canonical identities: {people} people, {organisations} organisations, "
            f"{structures} structures, {institutions} institutions and {proceedings} proceedings."
        )
        json_description = (
            f"Canonical register of {total} identities: {people} people, {organisations} organisations, "
            f"{structures} structures, {institutions} institutions and {proceedings} proceedings, "
            "connected to institutional actions and an evidence graph."
        )
        coverage = (
            f"The <strong>{total} IDs</strong> cover the current canonical register: {people} people, "
            f"{organisations} organisations, {structures} structures, {institutions} institutions and "
            f"{proceedings} proceedings."
        )
        noscript = (
            f"The static canonical denominator is {total}: {people} people, {organisations} organisations, "
            f"{structures} structures, {institutions} institutions and {proceedings} proceedings."
        )
        text = replace_exactly_once(
            text,
            r'(?<=<meta name="description" content=")Operational Por Derecho register of \d+ immutable IDs: \d+ people, \d+ organisations, \d+ structures, \d+ institutions and \d+ proceedings',
            meta,
            "English meta description",
        )
        text = replace_exactly_once(
            text,
            r'(?<=<meta property="og:description" content=")\d+ canonical identities: \d+ people, \d+ organisations, \d+ structures, \d+ institutions and \d+ proceedings\.',
            og,
            "English Open Graph description",
        )
        text = replace_exactly_once(
            text,
            r'(?<="inLanguage":"en","description":")Canonical register of \d+ identities: \d+ people, \d+ organisations, \d+ structures, \d+ institutions and \d+ proceedings, [^"]+',
            json_description,
            "English JSON-LD description",
        )
        value_names = {
            "Total": total,
            "People": people,
            "Organisations": organisations,
            "Structures": structures,
            "Institutions": institutions,
            "Proceedings": proceedings,
        }
        human_date = en_date
        date_pattern = r'(?<=PD-SP-IDENTITY-REGISTRY-001 · PD-SP-IDENTITY-OPS-001 · )\d{1,2} [A-Z]+ \d{4}'
        coverage_pattern = (
            r'The <strong>\d+ IDs</strong> cover the current canonical register: \d+ people, '
            r'\d+ organisations, \d+ structures, \d+ institutions and \d+ proceedings\.'
        )
        noscript_pattern = (
            r'The static canonical denominator is \d+: \d+ people, \d+ organisations, '
            r'\d+ structures, \d+ institutions and \d+ proceedings\.'
        )
    elif language == "es":
        meta = (
            f"Registro operativo de {total} IDs inmutables de Por Derecho: {people} personas, "
            f"{organisations} organizaciones, {structures} estructuras, {institutions} instituciones "
            f"y {proceedings} procedimientos"
        )
        og = (
            f"{total} identidades canónicas: {people} personas, {organisations} organizaciones, "
            f"{structures} estructuras, {institutions} instituciones y {proceedings} procedimientos."
        )
        json_description = (
            f"Registro canónico de {total} identidades: {people} personas, {organisations} organizaciones, "
            f"{structures} estructuras, {institutions} instituciones y {proceedings} procedimientos, "
            "conectado con acciones institucionales y un grafo probatorio."
        )
        coverage = (
            f"Los <strong>{total} IDs</strong> cubren el registro canónico actual: {people} personas, "
            f"{organisations} organizaciones, {structures} estructuras, {institutions} instituciones "
            f"y {proceedings} procedimientos."
        )
        noscript = (
            f"El denominador canónico estático es {total}: {people} personas, {organisations} organizaciones, "
            f"{structures} estructuras, {institutions} instituciones y {proceedings} procedimientos."
        )
        text = replace_exactly_once(
            text,
            r'(?<=<meta name="description" content=")Registro operativo de \d+ IDs inmutables de Por Derecho: \d+ personas, \d+ organizaciones, \d+ estructuras, \d+ instituciones y \d+ procedimientos',
            meta,
            "Spanish meta description",
        )
        text = replace_exactly_once(
            text,
            r'(?<=<meta property="og:description" content=")\d+ identidades canónicas: \d+ personas, \d+ organizaciones, \d+ estructuras, \d+ instituciones y \d+ procedimientos\.',
            og,
            "Spanish Open Graph description",
        )
        text = replace_exactly_once(
            text,
            r'(?<="inLanguage":"es","description":")Registro canónico de \d+ identidades: \d+ personas, \d+ organizaciones, \d+ estructuras, \d+ instituciones y \d+ procedimientos, [^"]+',
            json_description,
            "Spanish JSON-LD description",
        )
        value_names = {
            "Total": total,
            "Personas": people,
            "Organizaciones": organisations,
            "Estructuras": structures,
            "Instituciones": institutions,
            "Procedimientos": proceedings,
        }
        human_date = es_date
        date_pattern = r'(?<=PD-SP-IDENTITY-REGISTRY-001 · PD-SP-IDENTITY-OPS-001 · )\d{1,2} [A-ZÁÉÍÓÚÑ]+ \d{4}'
        coverage_pattern = (
            r'Los <strong>\d+ IDs</strong> cubren el registro canónico actual: \d+ personas, '
            r'\d+ organizaciones, \d+ estructuras, \d+ instituciones y \d+ procedimientos\.'
        )
        noscript_pattern = (
            r'El denominador canónico estático es \d+: \d+ personas, \d+ organizaciones, '
            r'\d+ estructuras, \d+ instituciones y \d+ procedimientos\.'
        )
    else:
        raise SyncError(f"unsupported language: {language}")

    text = replace_exactly_once(
        text,
        r'(?<="dateModified":")\d{4}-\d{2}-\d{2}',
        control_date,
        f"{language} JSON-LD date",
    )
    for name, value in value_names.items():
        text = replace_exactly_once(
            text,
            rf'(?<="name":"{re.escape(name)}","value":)\d+',
            str(value),
            f"{language} JSON-LD value {name}",
        )
    text = replace_exactly_once(text, date_pattern, human_date, f"{language} human date")
    text = replace_exactly_once(text, coverage_pattern, coverage, f"{language} coverage sentence")
    text = replace_exactly_once(text, noscript_pattern, noscript, f"{language} noscript denominator")
    text = replace_exactly_once(
        text,
        r'(?<=data-static-registry-counts=")[0-9-]+',
        marker,
        f"{language} static marker",
    )
    stat_values = {
        "TOTAL": total,
        "PERSON": people,
        "ORGANISATION": organisations,
        "STRUCTURE": structures,
        "INSTITUTION": institutions,
        "PROCEEDING": proceedings,
    }
    for stat_name, value in stat_values.items():
        text = replace_exactly_once(
            text,
            rf'(?<=<strong data-registry-stat="{stat_name}">)\d+',
            str(value),
            f"{language} static stat {stat_name}",
        )
    return text


def update_unitary_state(counts: dict[str, int], control_date: str) -> str:
    state = load_object(UNITARY_STATE)
    identity = state.get("identity_registry")
    if not isinstance(identity, dict):
        raise SyncError("CURRENT_UNITARY_STATE lacks identity_registry object")
    identity["control_date"] = control_date
    identity["counts"] = dict(counts)
    for key in ("total", *TYPES):
        if key in identity:
            identity[key] = counts[key]
    identity["static_page_parity"] = "LOCAL_SOURCE_STATIC_CANDIDATE_NOT_YET_LIVE_VERIFIED"
    return json.dumps(state, ensure_ascii=False, indent=2) + "\n"


def update_dp3205_validator() -> str:
    text = DP3205_VALIDATOR.read_text(encoding="utf-8")
    if "registry_date_match = re.fullmatch" in text:
        return text

    start_marker = 'registry_control_date = registry.get("control_date") if isinstance(registry, dict) else None'
    end_marker = 'includes(registry_es, "31 AGOSTO 2026", relative(REGISTRY_ES))'
    start = text.find(start_marker)
    end = text.find(end_marker, start if start >= 0 else 0)
    if start < 0 or end < 0:
        raise SyncError("DP3205 validator legacy date block was not found")
    end += len(end_marker)
    if text[end:end + 2] == "\r\n":
        end += 2
    elif text[end:end + 1] == "\n":
        end += 1

    replacement = "\n".join([
        'registry_control_date = registry.get("control_date") if isinstance(registry, dict) else None',
        'registry_date_match = re.fullmatch(r"(\\d{4})-(\\d{2})-(\\d{2})", str(registry_control_date or ""))',
        'require(bool(registry_date_match), "canonical current registry control date is not a valid ISO date")',
        'includes(registry_en, f\'"dateModified":"{registry_control_date}"\', relative(REGISTRY_EN))',
        'includes(registry_es, f\'"dateModified":"{registry_control_date}"\', relative(REGISTRY_ES))',
        'if registry_date_match:',
        '    registry_year, registry_month, registry_day = (int(part) for part in registry_date_match.groups())',
        '    registry_en_months = {1:"JANUARY",2:"FEBRUARY",3:"MARCH",4:"APRIL",5:"MAY",6:"JUNE",7:"JULY",8:"AUGUST",9:"SEPTEMBER",10:"OCTOBER",11:"NOVEMBER",12:"DECEMBER"}',
        '    registry_es_months = {1:"ENERO",2:"FEBRERO",3:"MARZO",4:"ABRIL",5:"MAYO",6:"JUNIO",7:"JULIO",8:"AGOSTO",9:"SEPTIEMBRE",10:"OCTUBRE",11:"NOVIEMBRE",12:"DICIEMBRE"}',
        '    require(registry_month in registry_en_months, "canonical registry control date has an invalid month")',
        '    if registry_month in registry_en_months:',
        '        includes(registry_en, f"{registry_day} {registry_en_months[registry_month]} {registry_year}", relative(REGISTRY_EN))',
        '        includes(registry_es, f"{registry_day} {registry_es_months[registry_month]} {registry_year}", relative(REGISTRY_ES))',
        '',
    ])
    return text[:start] + replacement + text[end:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write synchronized derived files")
    mode.add_argument("--check", action="store_true", help="fail if a derived file is stale")
    args = parser.parse_args()

    registry = load_object(REGISTRY)
    raw_counts = registry.get("counts")
    expected_keys = {"total", *TYPES}
    if not isinstance(raw_counts, dict) or set(raw_counts) != expected_keys:
        raise SyncError("canonical registry count schema is incomplete")
    counts = {key: int(raw_counts[key]) for key in ("total", *TYPES)}
    if sum(counts[key] for key in TYPES) != counts["total"]:
        raise SyncError("canonical registry total does not equal class totals")
    control_date = str(registry.get("control_date") or "")
    iso_and_human_dates(control_date)

    outputs = {
        EN_PAGE: synchronize_page(EN_PAGE, "en", counts, control_date),
        ES_PAGE: synchronize_page(ES_PAGE, "es", counts, control_date),
        UNITARY_STATE: update_unitary_state(counts, control_date),
        DP3205_VALIDATOR: update_dp3205_validator(),
    }
    changed = [path for path, content in outputs.items() if path.read_text(encoding="utf-8") != content]

    if args.check:
        if changed:
            print("IDENTITY REGISTRY STATIC SYNCHRONIZATION: FAIL")
            for path in changed:
                print(f"- stale derived surface: {path.relative_to(ROOT)}")
            return 1
        print("IDENTITY REGISTRY STATIC SYNCHRONIZATION: PASS")
        return 0

    for path, content in outputs.items():
        if path in changed:
            path.write_text(content, encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")
    print(f"IDENTITY REGISTRY STATIC SYNCHRONIZATION: WROTE {len(changed)} FILE(S)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SyncError as exc:
        print(f"IDENTITY REGISTRY STATIC SYNCHRONIZATION: FAIL\n- {exc}", file=sys.stderr)
        raise SystemExit(1)

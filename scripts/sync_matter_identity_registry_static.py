#!/usr/bin/env python3
"""Synchronize static identity-registry surfaces from the canonical registry.

The canonical denominator lives in assets/data/matter-identity-registry-v1.json.
This script updates only derived public/static mirrors and makes the legacy
DP3205 validator date-aware rather than frozen to one registry revision.
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
    1: "JANUARY",
    2: "FEBRUARY",
    3: "MARCH",
    4: "APRIL",
    5: "MAY",
    6: "JUNE",
    7: "JULY",
    8: "AUGUST",
    9: "SEPTEMBER",
    10: "OCTOBER",
    11: "NOVEMBER",
    12: "DECEMBER",
}
ES_MONTHS = {
    1: "ENERO",
    2: "FEBRERO",
    3: "MARZO",
    4: "ABRIL",
    5: "MAYO",
    6: "JUNIO",
    7: "JULIO",
    8: "AGOSTO",
    9: "SEPTIEMBRE",
    10: "OCTUBRE",
    11: "NOVIEMBRE",
    12: "DICIEMBRE",
}


class SyncError(RuntimeError):
    pass


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SyncError(f"cannot read JSON {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise SyncError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def replace_once(text: str, pattern: str, replacement: str | Callable[[re.Match[str]], str], label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.DOTALL)
    if count != 1:
        raise SyncError(f"{label}: expected exactly one match, observed {count}")
    return updated


def replace_all_required(text: str, pattern: str, replacement: str | Callable[[re.Match[str]], str], label: str, minimum: int = 1) -> str:
    updated, count = re.subn(pattern, replacement, text, flags=re.DOTALL)
    if count < minimum:
        raise SyncError(f"{label}: expected at least {minimum} matches, observed {count}")
    return updated


def human_dates(control_date: str) -> tuple[str, str]:
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


def synchronize_page(path: Path, language: str, counts: dict[str, int], control_date: str) -> str:
    text = path.read_text(encoding="utf-8")
    total = counts["total"]
    people = counts["PERSON"]
    orgs = counts["ORGANISATION"]
    structures = counts["STRUCTURE"]
    institutions = counts["INSTITUTION"]
    proceedings = counts["PROCEEDING"]
    marker = f"{total}-{people}-{orgs}-{structures}-{institutions}-{proceedings}"
    en_date, es_date = human_dates(control_date)

    if language == "en":
        text = replace_once(
            text,
            r'(<meta name="description" content=")Operational Por Derecho register of \d+ immutable IDs: \d+ people, \d+ organisations, \d+ structures, \d+ institutions and \d+ proceedings',
            rf'\1Operational Por Derecho register of {total} immutable IDs: {people} people, {orgs} organisations, {structures} structures, {institutions} institutions and {proceedings} proceedings',
            "English meta description",
        )
        text = replace_once(
            text,
            r'(<meta property="og:description" content=")\d+ canonical identities: \d+ people, \d+ organisations, \d+ structures, \d+ institutions and \d+ proceedings\.',
            rf'\1{total} canonical identities: {people} people, {orgs} organisations, {structures} structures, {institutions} institutions and {proceedings} proceedings.',
            "English Open Graph description",
        )
        text = replace_once(text, r'"dateModified":"\d{4}-\d{2}-\d{2}"', f'"dateModified":"{control_date}"', "English JSON-LD date")
        text = replace_once(
            text,
            r'"description":"Canonical register of \d+ identities: \d+ people, \d+ organisations, \d+ structures, \d+ institutions and \d+ proceedings, connected with actions and an evidence graph\."',
            f'"description":"Canonical register of {total} identities: {people} people, {orgs} organisations, {structures} structures, {institutions} institutions and {proceedings} proceedings, connected with actions and an evidence graph."',
            "English JSON-LD description",
        )
        value_names = {
            "Total": total,
            "People": people,
            "Organisations": orgs,
            "Structures": structures,
            "Institutions": institutions,
            "Proceedings": proceedings,
        }
        for name, value in value_names.items():
            text = replace_once(
                text,
                rf'("name":"{re.escape(name)}","value":)\d+',
                rf'\g<1>{value}',
                f"English JSON-LD {name}",
            )
        text = replace_once(
            text,
            r'(PD-SP-IDENTITY-REGISTRY-001 · PD-SP-IDENTITY-OPS-001 · )\d{1,2} [A-Z]+ \d{4}',
            rf'\1{en_date}',
            "English human date",
        )
        text = replace_once(
            text,
            r'The <strong>\d+ IDs</strong> cover the current canonical register: \d+ people, \d+ organisations, \d+ structures, \d+ institutions and \d+ proceedings\.',
            f'The <strong>{total} IDs</strong> cover the current canonical register: {people} people, {orgs} organisations, {structures} structures, {institutions} institutions and {proceedings} proceedings.',
            "English coverage boundary",
        )
        text = replace_once(
            text,
            r'The static canonical denominator is \d+: \d+ people, \d+ organisations, \d+ structures, \d+ institutions and \d+ proceedings\.',
            f'The static canonical denominator is {total}: {people} people, {orgs} organisations, {structures} structures, {institutions} institutions and {proceedings} proceedings.',
            "English noscript denominator",
        )
    else:
        text = replace_once(
            text,
            r'(<meta name="description" content=")Registro operativo de \d+ IDs inmutables de Por Derecho: \d+ personas, \d+ organizaciones, \d+ estructuras, \d+ instituciones y \d+ procedimientos',
            rf'\1Registro operativo de {total} IDs inmutables de Por Derecho: {people} personas, {orgs} organizaciones, {structures} estructuras, {institutions} instituciones y {proceedings} procedimientos',
            "Spanish meta description",
        )
        text = replace_once(
            text,
            r'(<meta property="og:description" content=")\d+ identidades canónicas: \d+ personas, \d+ organizaciones, \d+ estructuras, \d+ instituciones y \d+ procedimientos\.',
            rf'\1{total} identidades canónicas: {people} personas, {orgs} organizaciones, {structures} estructuras, {institutions} instituciones y {proceedings} procedimientos.',
            "Spanish Open Graph description",
        )
        text = replace_once(text, r'"dateModified":"\d{4}-\d{2}-\d{2}"', f'"dateModified":"{control_date}"', "Spanish JSON-LD date")
        text = replace_once(
            text,
            r'"description":"Registro canónico de \d+ identidades: \d+ personas, \d+ organizaciones, \d+ estructuras, \d+ instituciones y \d+ procedimientos, conectado con acciones institucionales y un grafo probatorio\."',
            f'"description":"Registro canónico de {total} identidades: {people} personas, {orgs} organizaciones, {structures} estructuras, {institutions} instituciones y {proceedings} procedimientos, conectado con acciones institucionales y un grafo probatorio."',
            "Spanish JSON-LD description",
        )
        value_names = {
            "Total": total,
            "Personas": people,
            "Organizaciones": orgs,
            "Estructuras": structures,
            "Instituciones": institutions,
            "Procedimientos": proceedings,
        }
        for name, value in value_names.items():
            text = replace_once(
                text,
                rf'("name":"{re.escape(name)}","value":)\d+',
                rf'\g<1>{value}',
                f"Spanish JSON-LD {name}",
            )
        text = replace_once(
            text,
            r'(PD-SP-IDENTITY-REGISTRY-001 · PD-SP-IDENTITY-OPS-001 · )\d{1,2} [A-ZÁÉÍÓÚÑ]+ \d{4}',
            rf'\1{es_date}',
            "Spanish human date",
        )
        text = replace_once(
            text,
            r'Los <strong>\d+ IDs</strong> cubren el registro canónico actual: \d+ personas, \d+ organizaciones, \d+ estructuras, \d+ instituciones y \d+ procedimientos\.',
            f'Los <strong>{total} IDs</strong> cubren el registro canónico actual: {people} personas, {orgs} organizaciones, {structures} estructuras, {institutions} instituciones y {proceedings} procedimientos.',
            "Spanish coverage boundary",
        )
        text = replace_once(
            text,
            r'El denominador canónico estático es \d+: \d+ personas, \d+ organizaciones, \d+ estructuras, \d+ instituciones y \d+ procedimientos\.',
            f'El denominador canónico estático es {total}: {people} personas, {orgs} organizaciones, {structures} estructuras, {institutions} instituciones y {proceedings} procedimientos.',
            "Spanish noscript denominator",
        )

    text = replace_once(text, r'data-static-registry-counts="[0-9-]+"', f'data-static-registry-counts="{marker}"', f"{language} static marker")
    stat_values = {
        "TOTAL": total,
        "PERSON": people,
        "ORGANISATION": orgs,
        "STRUCTURE": structures,
        "INSTITUTION": institutions,
        "PROCEEDING": proceedings,
    }
    for name, value in stat_values.items():
        text = replace_once(
            text,
            rf'(<strong data-registry-stat="{name}">)\d+(</strong>)',
            rf'\g<1>{value}\2',
            f"{language} static stat {name}",
        )
    return text


def update_unitary_state(counts: dict[str, int], control_date: str) -> str:
    state = load_json(UNITARY_STATE)
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
    old = '''registry_control_date = registry.get("control_date") if isinstance(registry, dict) else None
require(registry_control_date == "2026-08-31", "canonical current registry control date is stale")
includes(registry_en, f'"dateModified":"{registry_control_date}"', relative(REGISTRY_EN))
includes(registry_en, "31 AUGUST 2026", relative(REGISTRY_EN))
includes(registry_es, f'"dateModified":"{registry_control_date}"', relative(REGISTRY_ES))
includes(registry_es, "31 AGOSTO 2026", relative(REGISTRY_ES))
'''
    new = '''registry_control_date = registry.get("control_date") if isinstance(registry, dict) else None
registry_date_match = re.fullmatch(r"(\\d{4})-(\\d{2})-(\\d{2})", str(registry_control_date or ""))
require(bool(registry_date_match), "canonical current registry control date is not a valid ISO date")
includes(registry_en, f'"dateModified":"{registry_control_date}"', relative(REGISTRY_EN))
includes(registry_es, f'"dateModified":"{registry_control_date}"', relative(REGISTRY_ES))
if registry_date_match:
    registry_year, registry_month, registry_day = (int(part) for part in registry_date_match.groups())
    registry_en_months = {1:"JANUARY",2:"FEBRUARY",3:"MARCH",4:"APRIL",5:"MAY",6:"JUNE",7:"JULY",8:"AUGUST",9:"SEPTEMBER",10:"OCTOBER",11:"NOVEMBER",12:"DECEMBER"}
    registry_es_months = {1:"ENERO",2:"FEBRERO",3:"MARZO",4:"ABRIL",5:"MAYO",6:"JUNIO",7:"JULIO",8:"AGOSTO",9:"SEPTIEMBRE",10:"OCTUBRE",11:"NOVIEMBRE",12:"DICIEMBRE"}
    require(registry_month in registry_en_months, "canonical registry control date has an invalid month")
    if registry_month in registry_en_months:
        includes(registry_en, f"{registry_day} {registry_en_months[registry_month]} {registry_year}", relative(REGISTRY_EN))
        includes(registry_es, f"{registry_day} {registry_es_months[registry_month]} {registry_year}", relative(REGISTRY_ES))
'''
    if old in text:
        return text.replace(old, new, 1)
    if "registry_date_match = re.fullmatch" in text:
        return text
    raise SyncError("DP3205 validator date block is neither legacy nor synchronized")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write synchronized files")
    parser.add_argument("--check", action="store_true", help="fail if synchronization would change files")
    args = parser.parse_args()
    if not args.write and not args.check:
        parser.error("choose --write or --check")

    registry = load_json(REGISTRY)
    counts = registry.get("counts")
    if not isinstance(counts, dict) or set(counts) != {"total", *TYPES}:
        raise SyncError("canonical registry count schema is incomplete")
    integer_counts = {key: int(counts[key]) for key in ("total", *TYPES)}
    if sum(integer_counts[key] for key in TYPES) != integer_counts["total"]:
        raise SyncError("canonical registry total does not equal class totals")
    control_date = str(registry.get("control_date") or "")
    human_dates(control_date)

    outputs = {
        EN_PAGE: synchronize_page(EN_PAGE, "en", integer_counts, control_date),
        ES_PAGE: synchronize_page(ES_PAGE, "es", integer_counts, control_date),
        UNITARY_STATE: update_unitary_state(integer_counts, control_date),
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

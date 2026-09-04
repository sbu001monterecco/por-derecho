#!/usr/bin/env python3
"""Generate and verify identity-registry projections from the canonical registry.

The canonical federated registry is the source of truth. The two bilingual static
registry pages and the identity subsection of CURRENT_UNITARY_STATE are derived
projections. This command prevents a canonical identity addition from leaving
stale counts or dates on reader and continuity surfaces.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assets/data/matter-identity-registry-v1.json"
STATE = ROOT / "ops/CURRENT_UNITARY_STATE.json"
EN_PAGE = ROOT / "en/matter-identity-registry/index.html"
ES_PAGE = ROOT / "es/registro-identidad-materia/index.html"
RECONCILIATION = ROOT / "ops/reconciliations/identity-registry-20260903-valencia-court.json"
SOURCE_COMMIT = "621b108f5d3a99dd40697a8964a10a26213e2f37"
ADDED_ID = "PD-SP-I-0049"
ADDED_NAME = "Juzgado de Primera Instancia nº 27 de Valencia"
PREVIOUS_DATE = "2026-09-02"
PREVIOUS_COUNTS = {
    "total": 350,
    "PERSON": 165,
    "ORGANISATION": 83,
    "STRUCTURE": 11,
    "INSTITUTION": 48,
    "PROCEEDING": 43,
}
COUNT_KEYS = ("total", "PERSON", "ORGANISATION", "STRUCTURE", "INSTITUTION", "PROCEEDING")
MONTHS_EN = (
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
    "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER",
)
MONTHS_ES = (
    "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
    "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE",
)


class ProjectionError(RuntimeError):
    pass


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ProjectionError(f"cannot parse {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ProjectionError(f"{path.relative_to(ROOT)} root must be an object")
    return value


def dump_json(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def replace_exact_once(body: str, old: str, new: str, label: str) -> str:
    count = body.count(old)
    if count != 1:
        raise ProjectionError(f"{label}: expected one exact source fragment, found {count}")
    return body.replace(old, new, 1)


def replace_regex_once(body: str, pattern: str, replacement: str | Callable[[re.Match[str]], str], label: str) -> str:
    updated, count = re.subn(pattern, replacement, body, count=1, flags=re.DOTALL)
    if count != 1:
        raise ProjectionError(f"{label}: expected one pattern match, found {count}")
    return updated


def canonical_registry() -> tuple[dict, dict[str, int], str, dict]:
    registry = load_json(REGISTRY)
    counts = registry.get("counts")
    if not isinstance(counts, dict) or set(counts) != set(COUNT_KEYS):
        raise ProjectionError("canonical registry count schema is incomplete or contains an unexpected class")
    if any(not isinstance(counts[key], int) or counts[key] < 0 for key in COUNT_KEYS):
        raise ProjectionError("canonical registry counts must be non-negative integers")
    if counts["total"] != sum(counts[key] for key in COUNT_KEYS[1:]):
        raise ProjectionError("canonical registry total does not equal its class counts")

    control_date = registry.get("control_date")
    if not isinstance(control_date, str):
        raise ProjectionError("canonical registry control_date is missing")
    try:
        date.fromisoformat(control_date)
    except ValueError as exc:
        raise ProjectionError("canonical registry control_date must be ISO YYYY-MM-DD") from exc

    found: dict | None = None
    seen_ids: set[str] = set()
    actual = {key: 0 for key in COUNT_KEYS[1:]}
    for descriptor in registry.get("parts", []):
        if not isinstance(descriptor, dict) or not descriptor.get("path"):
            raise ProjectionError("canonical registry contains a malformed part descriptor")
        part = load_json(REGISTRY.parent / str(descriptor["path"]))
        records = part.get("records")
        if not isinstance(records, list) or len(records) != descriptor.get("count"):
            raise ProjectionError(f"registry part count mismatch: {descriptor['path']}")
        for record in records:
            if not isinstance(record, dict):
                raise ProjectionError(f"registry part contains a non-object record: {descriptor['path']}")
            rid = record.get("id")
            record_type = record.get("type")
            if not isinstance(rid, str) or not rid or rid in seen_ids:
                raise ProjectionError(f"duplicate or empty canonical identity ID: {rid!r}")
            if record_type not in actual:
                raise ProjectionError(f"unsupported canonical identity type: {record_type!r}")
            seen_ids.add(rid)
            actual[record_type] += 1
            if rid == ADDED_ID:
                found = record
    if len(seen_ids) != counts["total"] or any(actual[key] != counts[key] for key in actual):
        raise ProjectionError("federated identity parts do not match the canonical denominator")
    if not found or found.get("name") != ADDED_NAME or found.get("type") != "INSTITUTION":
        raise ProjectionError(f"source-verified delta object {ADDED_ID} is absent or inconsistent")
    return registry, counts, control_date, found


def human_date(control_date: str, lang: str) -> str:
    parsed = date.fromisoformat(control_date)
    months = MONTHS_ES if lang == "es" else MONTHS_EN
    return f"{parsed.day} {months[parsed.month - 1]} {parsed.year}"


def count_phrase(counts: dict[str, int], lang: str) -> str:
    if lang == "es":
        return (
            f"{counts['total']} identidades canónicas: {counts['PERSON']} personas, "
            f"{counts['ORGANISATION']} organizaciones, {counts['STRUCTURE']} estructuras, "
            f"{counts['INSTITUTION']} instituciones y {counts['PROCEEDING']} procedimientos."
        )
    return (
        f"{counts['total']} canonical identities: {counts['PERSON']} people, "
        f"{counts['ORGANISATION']} organisations, {counts['STRUCTURE']} structures, "
        f"{counts['INSTITUTION']} institutions and {counts['PROCEEDING']} proceedings."
    )


def update_json_ld(body: str, counts: dict[str, int], control_date: str, lang: str, label: str) -> str:
    pattern = r'(<script type="application/ld\+json">)(\{.*?"identifier":"PD-SP-IDENTITY-REGISTRY-001".*?\})(</script>)'

    def replacement(match: re.Match[str]) -> str:
        try:
            data = json.loads(match.group(2))
        except json.JSONDecodeError as exc:
            raise ProjectionError(f"{label}: invalid inline Dataset JSON-LD: {exc}") from exc
        data["dateModified"] = control_date
        data["description"] = (
            f"Registro canónico de {counts['total']} identidades: {counts['PERSON']} personas, "
            f"{counts['ORGANISATION']} organizaciones, {counts['STRUCTURE']} estructuras, "
            f"{counts['INSTITUTION']} instituciones y {counts['PROCEEDING']} procedimientos, "
            "conectado con acciones institucionales y un grafo probatorio."
            if lang == "es"
            else f"Canonical register of {counts['total']} identities: {counts['PERSON']} people, "
            f"{counts['ORGANISATION']} organisations, {counts['STRUCTURE']} structures, "
            f"{counts['INSTITUTION']} institutions and {counts['PROCEEDING']} proceedings, "
            "connected to institutional actions and an evidence graph."
        )
        expected_names = (
            ("Total", "Personas", "Organizaciones", "Estructuras", "Instituciones", "Procedimientos")
            if lang == "es"
            else ("Total", "People", "Organisations", "Structures", "Institutions", "Proceedings")
        )
        values = dict(zip(expected_names, (counts[key] for key in COUNT_KEYS), strict=True))
        measured = data.get("variableMeasured")
        if not isinstance(measured, list):
            raise ProjectionError(f"{label}: Dataset JSON-LD lacks variableMeasured")
        seen: set[str] = set()
        for item in measured:
            if isinstance(item, dict) and item.get("name") in values:
                item["value"] = values[str(item["name"])]
                seen.add(str(item["name"]))
        if seen != set(expected_names):
            raise ProjectionError(f"{label}: Dataset JSON-LD count labels are incomplete")
        compact = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        return f"{match.group(1)}{compact}{match.group(3)}"

    return replace_regex_once(body, pattern, replacement, f"{label} JSON-LD")


def project_page(original: str, counts: dict[str, int], control_date: str, lang: str, label: str) -> str:
    marker = "-".join(str(counts[key]) for key in COUNT_KEYS)
    human = human_date(control_date, lang)
    body = original

    if lang == "es":
        description = (
            f"Registro operativo de {counts['total']} IDs inmutables de Por Derecho: "
            f"{counts['PERSON']} personas, {counts['ORGANISATION']} organizaciones, "
            f"{counts['STRUCTURE']} estructuras, {counts['INSTITUTION']} instituciones y "
            f"{counts['PROCEEDING']} procedimientos, conectados con acciones, grafo, rutas públicas y controles de identidad."
        )
        boundary = (
            f'<div class="id-boundary"><strong>Límite de cobertura.</strong> Los <strong>{counts["total"]} IDs</strong> '
            f'cubren el registro canónico actual: {counts["PERSON"]} personas, {counts["ORGANISATION"]} organizaciones, '
            f'{counts["STRUCTURE"]} estructuras, {counts["INSTITUTION"]} instituciones y {counts["PROCEEDING"]} procedimientos. '
            'El backfill retrospectivo de correos, anexos, escritos y archivos autorizados sigue abierto. Una coincidencia de nombre '
            'no crea identidad, no fusiona sociedades y no transfiere conocimiento, intención, control, beneficio ni responsabilidad.</div>'
        )
        noscript = (
            f'La capa estática canónica es {counts["total"]}: {counts["PERSON"]} personas, '
            f'{counts["ORGANISATION"]} organizaciones, {counts["STRUCTURE"]} estructuras, '
            f'{counts["INSTITUTION"]} instituciones y {counts["PROCEEDING"]} procedimientos.'
        )
        body = replace_regex_once(body, r'<meta name="description" content="Registro operativo de .*?">', f'<meta name="description" content="{description}">', f"{label} meta description")
        body = replace_regex_once(body, r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{count_phrase(counts, lang)}">', f"{label} Open Graph description")
        body = replace_regex_once(body, r'(PD-SP-IDENTITY-REGISTRY-001 · PD-SP-IDENTITY-OPS-001 · )[^<]+', rf'\g<1>{human}', f"{label} human date")
        body = replace_regex_once(body, r'<div class="id-boundary">.*?</div>', boundary, f"{label} coverage boundary")
        body = replace_regex_once(body, r'La capa estática canónica es \d+: \d+ personas, \d+ organizaciones, \d+ estructuras, \d+ instituciones y \d+ procedimientos\.', noscript, f"{label} noscript denominator")
    else:
        description = (
            f"Operational Por Derecho register of {counts['total']} immutable IDs: "
            f"{counts['PERSON']} people, {counts['ORGANISATION']} organisations, "
            f"{counts['STRUCTURE']} structures, {counts['INSTITUTION']} institutions and "
            f"{counts['PROCEEDING']} proceedings, connected to actions, graph, public routes and identity controls."
        )
        boundary = (
            f'<div class="id-boundary"><strong>Coverage boundary.</strong> The <strong>{counts["total"]} IDs</strong> '
            f'cover the current canonical register: {counts["PERSON"]} people, {counts["ORGANISATION"]} organisations, '
            f'{counts["STRUCTURE"]} structures, {counts["INSTITUTION"]} institutions and {counts["PROCEEDING"]} proceedings. '
            'Retrospective backfill across emails, attachments, pleadings and authorised records remains open. A name match does not '
            'create identity, merge companies, or transfer knowledge, intention, control, benefit or responsibility.</div>'
        )
        noscript = (
            f'The static canonical denominator is {counts["total"]}: {counts["PERSON"]} people, '
            f'{counts["ORGANISATION"]} organisations, {counts["STRUCTURE"]} structures, '
            f'{counts["INSTITUTION"]} institutions and {counts["PROCEEDING"]} proceedings.'
        )
        body = replace_regex_once(body, r'<meta name="description" content="Operational Por Derecho register of .*?">', f'<meta name="description" content="{description}">', f"{label} meta description")
        body = replace_regex_once(body, r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{count_phrase(counts, lang)}">', f"{label} Open Graph description")
        body = replace_regex_once(body, r'(PD-SP-IDENTITY-REGISTRY-001 · PD-SP-IDENTITY-OPS-001 · )[^<]+', rf'\g<1>{human}', f"{label} human date")
        body = replace_regex_once(body, r'<div class="id-boundary">.*?</div>', boundary, f"{label} coverage boundary")
        body = replace_regex_once(body, r'The static canonical denominator is \d+: \d+ people, \d+ organisations, \d+ structures, \d+ institutions and \d+ proceedings\.', noscript, f"{label} noscript denominator")

    body = update_json_ld(body, counts, control_date, lang, label)
    body = replace_regex_once(body, r'data-static-registry-counts="[0-9-]+"', f'data-static-registry-counts="{marker}"', f"{label} static marker")
    for key in COUNT_KEYS:
        body = replace_regex_once(
            body,
            rf'(<strong data-registry-stat="{key}">)\d+(</strong>)',
            rf'\g<1>{counts[key]}\g<2>',
            f"{label} {key} stat",
        )
    return body


def project_state(original: dict, counts: dict[str, int], control_date: str) -> dict:
    state = deepcopy(original)
    identity = state.get("identity_registry")
    if not isinstance(identity, dict):
        raise ProjectionError("CURRENT_UNITARY_STATE lacks identity_registry object")
    identity["control_date"] = control_date
    identity["counts"] = dict(counts)
    identity["static_page_parity"] = "LOCAL_SOURCE_STATIC_RECONCILED_NOT_YET_LIVE_VERIFIED"
    identity["reconciliation_record"] = str(RECONCILIATION.relative_to(ROOT))
    for key in COUNT_KEYS:
        identity[key] = counts[key]
    return state


def reconciliation_record(counts: dict[str, int], control_date: str, added: dict) -> dict:
    delta = {key: counts[key] - PREVIOUS_COUNTS[key] for key in COUNT_KEYS}
    expected_delta = {
        "total": 1,
        "PERSON": 0,
        "ORGANISATION": 0,
        "STRUCTURE": 0,
        "INSTITUTION": 1,
        "PROCEEDING": 0,
    }
    if control_date != "2026-09-03" or counts != {
        "total": 351,
        "PERSON": 165,
        "ORGANISATION": 83,
        "STRUCTURE": 11,
        "INSTITUTION": 49,
        "PROCEEDING": 43,
    } or delta != expected_delta:
        raise ProjectionError("the current canonical denominator no longer matches the controlled Valencia-court reconciliation")
    return {
        "schema": "por-derecho.identity-registry-reconciliation.v1",
        "reconciliation_id": "PD-ID-REC-20260903-VALENCIA-COURT-01",
        "control_date": control_date,
        "source_commit": SOURCE_COMMIT,
        "reason": "Synchronize the source-confirmed Valencia court caret into every canonical identity projection.",
        "previous": {"control_date": PREVIOUS_DATE, "counts": PREVIOUS_COUNTS},
        "current": {"control_date": control_date, "counts": counts},
        "delta": delta,
        "added_objects": [
            {
                "id": added.get("id"),
                "type": added.get("type"),
                "name": added.get("name"),
                "identity_resolution": added.get("identity_resolution"),
                "routes": added.get("routes"),
            }
        ],
        "projection_paths": [
            str(EN_PAGE.relative_to(ROOT)),
            str(ES_PAGE.relative_to(ROOT)),
            str(STATE.relative_to(ROOT)),
        ],
        "state": "SOURCE_RECONCILED_PENDING_EXACT_SHA_DEPLOYMENT_AND_LIVE_READBACK",
        "boundaries": [
            "This reconciliation changes identity denominator and routing projections only.",
            "It does not identify an individual judge, LAJ, panel or office-holder for any act.",
            "It does not transfer knowledge, merits, conduct, intent, responsibility or procedural allocation.",
            "Live parity must not be claimed until the exact merged SHA is deployed and read back."
        ],
    }


def expected_outputs() -> dict[Path, str]:
    _registry, counts, control_date, added = canonical_registry()
    en = project_page(EN_PAGE.read_text(encoding="utf-8"), counts, control_date, "en", str(EN_PAGE.relative_to(ROOT)))
    es = project_page(ES_PAGE.read_text(encoding="utf-8"), counts, control_date, "es", str(ES_PAGE.relative_to(ROOT)))
    state = project_state(load_json(STATE), counts, control_date)
    record = reconciliation_record(counts, control_date, added)
    return {
        EN_PAGE: en,
        ES_PAGE: es,
        STATE: dump_json(state),
        RECONCILIATION: dump_json(record),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write deterministic projections instead of checking them")
    args = parser.parse_args()
    try:
        outputs = expected_outputs()
    except (ProjectionError, OSError, UnicodeError) as exc:
        print(f"IDENTITY REGISTRY PROJECTION RECONCILIATION: FAIL\n - {exc}")
        return 1

    drift: list[str] = []
    for path, expected in outputs.items():
        current = path.read_text(encoding="utf-8") if path.is_file() else ""
        if current == expected:
            continue
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
        else:
            drift.append(str(path.relative_to(ROOT)))

    if drift:
        print("IDENTITY REGISTRY PROJECTION RECONCILIATION: FAIL")
        for path in drift:
            print(f" - stale derived projection: {path}")
        print("Run: python scripts/reconcile_identity_registry_projections.py --write")
        return 1

    action = "WROTE" if args.write else "PASS"
    print(f"IDENTITY REGISTRY PROJECTION RECONCILIATION: {action}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Validate the public-safe Sun Park 262-finca journey release."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "research/sun-park-262-fincas/sun-park-262-fincas.csv"
EVIDENCE = ROOT / "research/sun-park-262-fincas/finca-journey-evidence-v1.json"
PROJECTION = ROOT / "assets/data/sun-park-262-finca-journey-v1.json"
ROUTES = {
    "en": ROOT / "en/262-properties-journey-2008-present/index.html",
    "es": ROOT / "es/fincas-262-recorrido-2008-hoy/index.html",
}
MAPS = {
    "en": ROOT / "en/sun-park-forensic-map-262-properties/index.html",
    "es": ROOT / "es/mapa-forense-sun-park-262-fincas/index.html",
}
REGISTRY = {
    "en": ROOT / "en/land-registry-implementation-property-by-property/index.html",
    "es": ROOT / "es/implementacion-registral-finca-por-finca/index.html",
}
ROUTE_REGISTRY = ROOT / "assets/data/unitary-route-registry-v1.json"
SITEMAP = ROOT / "sitemap-case-governance.xml"

ALLOWED_COVERAGE = {
    "NOT_YET_RECONSTRUCTED",
    "SOURCE_POINTER_ONLY",
    "PARTIALLY_RECONSTRUCTED",
    "IDENTIFIER_CONFLICT_OPEN",
}
ALLOWED_EVENT_STATUS = {
    "VERIFIED_OFFICIAL",
    "DOCUMENTED_REPRESENTATION",
    "DOCUMENTED_CONTEXT",
    "PARTY_ALLEGATION",
    "WORKING_LEAD",
    "PUBLIC_REPORT",
}
ALLOWED_LAYERS = {
    "title",
    "physical",
    "possession",
    "operation",
    "community",
    "concurso",
    "registry",
    "works",
    "valuation",
    "funding",
}
DATE_PATTERN = re.compile(r"^(?:\d{4}|\d{4}-\d{2}|\d{4}-\d{2}-\d{2}|\d{4}-\d{4})$")
FORBIDDEN_KEYS = {
    "address",
    "bank",
    "bank_account",
    "credential",
    "dni",
    "drive_id",
    "email",
    "iban",
    "password",
    "payment_amount",
    "phone",
    "price",
    "raw_document",
    "signature",
}


def load_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return None


def require_bilingual(value: object, location: str, errors: list[str]) -> None:
    if not isinstance(value, dict) or not all(isinstance(value.get(lang), (str, list)) for lang in ("en", "es")):
        errors.append(f"{location}: requires both English and Spanish text")


def assert_no_forbidden_keys(value: object, location: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if key.lower() in FORBIDDEN_KEYS:
                errors.append(f"{location}: forbidden public field {key!r}")
            assert_no_forbidden_keys(nested, f"{location}.{key}", errors)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            assert_no_forbidden_keys(nested, f"{location}[{index}]", errors)


def generated_projection_is_current(errors: list[str]) -> None:
    spec = importlib.util.spec_from_file_location("build_262_finca_journey", ROOT / "scripts/build_262_finca_journey.py")
    if not spec or not spec.loader:
        errors.append("Could not load journey builder")
        return
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    try:
        expected = builder.serialise(builder.build())
        actual = PROJECTION.read_bytes()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        errors.append(f"generated projection check failed: {exc}")
        return
    if actual != expected:
        errors.append("assets/data/sun-park-262-finca-journey-v1.json is stale; run scripts/build_262_finca_journey.py")


def validate_data(data: dict, errors: list[str]) -> None:
    if data.get("schema_version") != "sun-park-262-finca-journey/v1":
        errors.append("Projection schema_version is not sun-park-262-finca-journey/v1")
    properties = data.get("properties")
    if not isinstance(properties, list) or len(properties) != 262:
        errors.append(f"Projection must contain exactly 262 properties; found {len(properties) if isinstance(properties, list) else 'invalid'}")
        return

    expected_fincas = set()
    for line in MASTER.read_text(encoding="utf-8").splitlines()[1:]:
        expected_fincas.add(line.split(",", 2)[1])
    observed_fincas = [property_.get("registry_finca") for property_ in properties]
    if len(set(observed_fincas)) != 262 or set(observed_fincas) != expected_fincas:
        errors.append("Projection fincas do not match the canonical 262-row master register exactly")

    source_ids = {source.get("id") for source in data.get("source_ledger", []) if source.get("id")}
    if not source_ids:
        errors.append("Projection has no source ledger")
    for source in data.get("source_ledger", []):
        require_bilingual(source.get("label"), f"source {source.get('id', '?')} label", errors)
        require_bilingual(source.get("caution"), f"source {source.get('id', '?')} caution", errors)
        reference_url = source.get("reference_url")
        if reference_url and not str(reference_url).startswith("https://github.com/"):
            errors.append(f"source {source.get('id', '?')}: direct source URLs must be GitHub URLs or omitted")

    coverage = data.get("coverage", {})
    if coverage.get("total_properties") != 262:
        errors.append("coverage.total_properties must equal 262")
    require_bilingual(coverage.get("rule"), "coverage.rule", errors)
    defaults = data.get("defaults") or {}
    require_bilingual(defaults.get("historic_source_caution"), "defaults.historic_source_caution", errors)
    require_bilingual(defaults.get("open_questions"), "defaults.open_questions", errors)
    require_bilingual(defaults.get("next_document_needed"), "defaults.next_document_needed", errors)

    for event in data.get("complex_context_events", []):
        validate_event(event, "complex context", source_ids, errors, expected_scope="COMPLEX_CONTEXT")

    for property_ in properties:
        finca = property_.get("registry_finca", "?")
        state = property_.get("coverage_state")
        if state not in ALLOWED_COVERAGE:
            errors.append(f"{finca}: unsupported coverage_state {state!r}")
        physical = property_.get("physical") or {}
        if not all(key in physical for key in ("type", "area_m2", "block_or_zone")):
            errors.append(f"{finca}: missing physical baseline")
        historic = property_.get("historic_source_label")
        if not isinstance(historic, str) or not historic:
            errors.append(f"{finca}: missing historical GESVALT source label")
        for event in property_.get("events", []):
            validate_event(event, finca, source_ids, errors, expected_scope="PROPERTY_SPECIFIC")
        if state == "NOT_YET_RECONSTRUCTED" and property_.get("events"):
            errors.append(f"{finca}: NOT_YET_RECONSTRUCTED cannot contain a property event")
        if state == "IDENTIFIER_CONFLICT_OPEN" and not property_.get("identifier_conflicts"):
            errors.append(f"{finca}: identifier-conflict state needs an explicit conflict record")
        open_questions = property_.get("open_questions")
        if open_questions is not None:
            require_bilingual(open_questions, f"{finca}: open_questions", errors)
        next_document_needed = property_.get("next_document_needed")
        if next_document_needed is not None:
            require_bilingual(next_document_needed, f"{finca}: next_document_needed", errors)

    priority = {property_["registry_finca"]: property_ for property_ in properties}
    for finca in ("8497", "8498", "8584", "8587", "8588", "8499", "8500", "8503", "8504", "8505", "8506", "8507", "8557"):
        if finca not in priority:
            errors.append(f"Priority finca {finca} is absent")
    conflict_text = json.dumps(priority.get("8557", {}), ensure_ascii=False)
    if "707" not in conflict_text or "708" not in conflict_text:
        errors.append("8557 must preserve the 707/708 crosswalk conflict")
    for finca in ("8497", "8498"):
        if not any(event.get("evidence_status") == "PARTY_ALLEGATION" for event in priority.get(finca, {}).get("events", [])):
            errors.append(f"{finca} must retain its party-allegation status rather than a title conclusion")
    if not any(event.get("id") == "FINCA-8588-2016-06-01-DEED" for event in priority.get("8588", {}).get("events", [])):
        errors.append("8588 must retain its dated deed-family representation")
    assert_no_forbidden_keys(data, "projection", errors)


def validate_event(event: dict, location: str, source_ids: set[str], errors: list[str], expected_scope: str) -> None:
    event_id = event.get("id", "?")
    if event.get("scope") != expected_scope:
        errors.append(f"{location}/{event_id}: expected scope {expected_scope}")
    if event.get("evidence_status") not in ALLOWED_EVENT_STATUS:
        errors.append(f"{location}/{event_id}: unsupported evidence_status")
    if event.get("layer") not in ALLOWED_LAYERS:
        errors.append(f"{location}/{event_id}: unsupported layer")
    if not isinstance(event.get("date"), str) or not DATE_PATTERN.match(event["date"]):
        errors.append(f"{location}/{event_id}: invalid bounded date {event.get('date')!r}")
    for field in ("proposition", "limitation", "next_document_needed"):
        require_bilingual(event.get(field), f"{location}/{event_id}: {field}", errors)
    for source_id in event.get("source_ids", []):
        if source_id not in source_ids:
            errors.append(f"{location}/{event_id}: unknown source ID {source_id!r}")


def validate_routes(errors: list[str]) -> None:
    expected = {
        "en": {
            "canonical": "https://sbu001monterecco.github.io/por-derecho/en/262-properties-journey-2008-present/",
            "alternate": "https://sbu001monterecco.github.io/por-derecho/es/fincas-262-recorrido-2008-hoy/",
        },
        "es": {
            "canonical": "https://sbu001monterecco.github.io/por-derecho/es/fincas-262-recorrido-2008-hoy/",
            "alternate": "https://sbu001monterecco.github.io/por-derecho/en/262-properties-journey-2008-present/",
        },
    }
    for lang, path in ROUTES.items():
        if not path.is_file():
            errors.append(f"Missing direct journey route: {path.relative_to(ROOT)}")
            continue
        body = path.read_text(encoding="utf-8")
        for marker in (
            expected[lang]["canonical"],
            expected[lang]["alternate"],
            "data-finca-journey",
            "assets/finca-journey-2008-present-20260822.js",
            "assets/finca-journey-2008-present-20260822.css",
            "262",
        ):
            if marker not in body:
                errors.append(f"{path.relative_to(ROOT)}: missing {marker!r}")
    for related_routes in (MAPS, REGISTRY):
        for lang, path in related_routes.items():
            if not path.is_file():
                errors.append(f"Missing related route: {path.relative_to(ROOT)}")
                continue
            body = path.read_text(encoding="utf-8")
            target = "../262-properties-journey-2008-present/" if lang == "en" else "../fincas-262-recorrido-2008-hoy/"
            if target not in body:
                errors.append(f"{path.relative_to(ROOT)}: missing journey cross-link")

    registry_body = REGISTRY["en"].read_text(encoding="utf-8") if REGISTRY["en"].is_file() else ""
    if "sun-park-262-property-forensic-map" in registry_body:
        errors.append("English Registry route retains a stale nonexistent map route")
    criminal_data = ROOT / "assets/data/criminal-engineering-investigation-v1.json"
    if criminal_data.is_file() and "sun-park-262-property-forensic-map" in criminal_data.read_text(encoding="utf-8"):
        errors.append("criminal-engineering data retains a stale nonexistent map route")

    registry = load_json(ROUTE_REGISTRY, errors)
    if isinstance(registry, list):
        paths = {entry.get("path") for entry in registry}
        for expected_path in ("en/262-properties-journey-2008-present/", "es/fincas-262-recorrido-2008-hoy/"):
            if expected_path not in paths:
                errors.append(f"Route registry missing {expected_path}")
    sitemap = SITEMAP.read_text(encoding="utf-8") if SITEMAP.is_file() else ""
    for expected_path in (
        "/en/sun-park-forensic-map-262-properties/",
        "/es/mapa-forense-sun-park-262-fincas/",
        "/en/262-properties-journey-2008-present/",
        "/es/fincas-262-recorrido-2008-hoy/",
    ):
        if expected_path not in sitemap:
            errors.append(f"Case-governance sitemap missing {expected_path}")


def main() -> int:
    errors: list[str] = []
    for path in (MASTER, EVIDENCE, PROJECTION):
        if not path.is_file():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")
    if not errors:
        generated_projection_is_current(errors)
        data = load_json(PROJECTION, errors)
        if isinstance(data, dict):
            validate_data(data, errors)
        validate_routes(errors)

    if errors:
        print("262-FINCA JOURNEY VALIDATION: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1
    print("262-FINCA JOURNEY VALIDATION: PASS — 262 canonical fincas, source/status gates and ES/EN routes verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

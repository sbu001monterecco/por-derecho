#!/usr/bin/env python3
"""Validate the bilingual Calificación / RPL 2523 evidence-addressability package."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT_STATE_V2 = "por-derecho.operational-truth.current-state.v2"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    es_path = "es/calificacion-rpl-2523-mapa-prueba/index.html"
    en_path = "en/calificacion-rpl-2523-evidence-map/index.html"
    es = read(es_path)
    en = read(en_path)

    required_es = [
        "tres instrumentos de apelación localizados o reportados para cuatro intereses apelantes",
        "Esta es la posición pública de Gil Marer / Por Derecho",
        "no habla por ninguna representación procesal",
        "Cortafuegos de apelación",
        "Alegaciones materialmente excesivas",
        "Dictamen excepcionalmente severo de dos páginas",
        "Circularidad institucional",
        "Adopción judicial selectiva",
        "Posible beneficio para el perímetro Acosta Matos",
        "No localizado no significa inexistente",
        "ACTÚA–GESVALT no se presenta como prueba del recurso",
        "El silencio no se tratará como admisión",
    ]
    required_en = [
        "three located or reported appeal instruments for four appellant interests",
        "This is the public position of Gil Marer / Por Derecho",
        "does not speak for any procedural representative",
        "Appeal firewall",
        "Materially excessive allegations",
        "Exceptionally severe two-page opinion",
        "Institutional circularity",
        "Selected judicial adoption",
        "Possible benefit to the Acosta Matos perimeter",
        "Not located does not mean nonexistent",
        "ACTÚA–GESVALT is not presented as appeal evidence",
        "Silence is not admission",
    ]
    for marker in required_es:
        if marker not in es:
            errors.append(f"{es_path}: missing {marker!r}")
    for marker in required_en:
        if marker not in en:
            errors.append(f"{en_path}: missing {marker!r}")

    for path, body in [(es_path, es), (en_path, en)]:
        if body.count("<tr><td>") != 8:
            errors.append(f"{path}: expected eight party/stage instrument rows")
        for prohibited in ["Carlos Llamas", "Joaquín Ruiz", "Betancor", "Ruiz de Infante"]:
            if prohibited in body:
                errors.append(f"{path}: current/former counsel name leaked: {prohibited!r}")

    data = json.loads(read("assets/data/calificacion-rpl2523-evidence-map-v1.json"))
    if data.get("schema") != "por-derecho.calificacion-rpl2523-evidence-map.v1":
        errors.append("evidence map JSON: unexpected schema")
    if data.get("proceeding", {}).get("appeal_roll") != "RPL 2523/2025":
        errors.append("evidence map JSON: current Calificación roll missing")
    instruments = data.get("instrument_map", [])
    if len(instruments) != 8:
        errors.append("evidence map JSON: expected eight party/stage records")
    appeals = [item for item in instruments if item.get("stage") == "APPEAL"]
    if sum(item.get("instrument_count", 0) for item in appeals) != 3:
        errors.append("evidence map JSON: expected three appeal instruments")
    appeal_interests = {name for item in appeals if item.get("instrument_count") for name in item.get("party_interests", [])}
    if len(appeal_interests) != 4:
        errors.append("evidence map JSON: expected four appellant interests")
    if len(data.get("five_pillar_map", [])) != 5:
        errors.append("evidence map JSON: expected five investigative pillars")
    if data.get("proof_boundary", {}).get("silence_is_admission") is not False:
        errors.append("evidence map JSON: silence/admission boundary missing")
    if data.get("proceeding", {}).get("later_merits_decision_located") is not False:
        errors.append("evidence map JSON: latest controlled merits state is not preserved")

    for path in [
        "es/index.html",
        "en/index.html",
    ]:
        body = read(path)
        if body.count('data-calificacion-misuse-thesis="featured"') != 1:
            errors.append(f"{path}: expected one statically rendered homepage thesis block")
    homepage_markers = {
        "es/index.html": ["tesis investigativa seria y documental", "calificacion-rpl-2523-mapa-prueba/"],
        "en/index.html": ["serious, document-based investigative thesis", "calificacion-rpl-2523-evidence-map/"],
    }
    for path, markers in homepage_markers.items():
        body = read(path)
        for marker in markers:
            if marker not in body:
                errors.append(f"{path}: missing static strategic marker {marker!r}")

    appeal_markers = {
        "es/concurso-36-2012-ap-seccion-4/index.html": [
            "Tres recursos para cuatro intereses apelantes",
            "calificacion-rpl-2523-mapa-prueba/",
            "No habla colectivamente por las partes apelantes",
        ],
        "en/insolvency-36-2012-ap-section-4/index.html": [
            "Three appeals for four appellant interests",
            "calificacion-rpl-2523-evidence-map/",
            "does not speak collectively for the appellants",
        ],
    }
    for path, markers in appeal_markers.items():
        body = read(path)
        for marker in markers:
            if marker not in body:
                errors.append(f"{path}: missing appellant/instrument control {marker!r}")

    for path in [
        "es/tesis-uso-criminal-procedimiento-calificacion/index.html",
        "en/insolvency-classification-criminal-misuse-thesis/index.html",
    ]:
        body = read(path)
        if "Gil Marer / Por Derecho" not in body:
            errors.append(f"{path}: publisher attribution missing")

    routes = [
        "/es/calificacion-rpl-2523-mapa-prueba/",
        "/en/calificacion-rpl-2523-evidence-map/",
    ]
    for sitemap_path in ["sitemap.xml", "sitemap-calificacion.xml"]:
        sitemap = read(sitemap_path)
        for route in routes:
            if route not in sitemap:
                errors.append(f"{sitemap_path}: missing {route}")
    registry = json.loads(read("assets/data/unitary-route-registry-v1.json"))
    registered = {item.get("path") for item in registry}
    for route in [value.lstrip("/") for value in routes]:
        if route not in registered:
            errors.append(f"unitary route registry: missing {route}")

    # Operational truth v2 deliberately no longer stores specialist case facts.
    # The canonical evidence map above controls the RPL roll and denominator.
    # Legacy v1 branches retain the historical checks for backwards compatibility.
    current = json.loads(read("ops/CURRENT_STATE.json"))
    if current.get("schema") == CURRENT_STATE_V2:
        if current.get("record_type") != "CURRENT_STATE_CONTRACT_WITH_LAST_OBSERVATION":
            errors.append("ops/CURRENT_STATE.json: operational truth v2 record type missing")
        purpose = str(current.get("purpose", ""))
        if "Specialist source controls remain authoritative" not in purpose:
            errors.append("ops/CURRENT_STATE.json: specialist-source authority boundary missing")
        priority_sources = current.get("current_priority_sources")
        if not isinstance(priority_sources, list) or not priority_sources:
            errors.append("ops/CURRENT_STATE.json: priority-source routing missing")
    else:
        if current.get("calificacion", {}).get("appeal_roll") != "RPL 2523/2025":
            errors.append("ops/CURRENT_STATE.json: current Calificación roll missing")
        if current.get("calificacion", {}).get("instrument_count_rule") != "THREE_APPEAL_INSTRUMENTS_FOUR_APPELLANT_INTERESTS":
            errors.append("ops/CURRENT_STATE.json: appeal denominator rule missing")

    if errors:
        print("CALIFICACION RPL2523 EVIDENCE MAP: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1
    print("CALIFICACION RPL2523 EVIDENCE MAP: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Validate the Calificación criminal-misuse thesis publication and safeguards."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []

    es_path = "es/tesis-uso-criminal-procedimiento-calificacion/index.html"
    en_path = "en/insolvency-classification-criminal-misuse-thesis/index.html"
    es = read(es_path)
    en = read(en_path)

    required_es = [
        "tesis investigativa seria y basada en documentos",
        "Alegaciones del AC materialmente excesivas",
        "Dictamen fiscal excepcionalmente severo",
        "Circularidad institucional en DI 248",
        "Adopción judicial selectiva",
        "Posible beneficio privado",
        "RPL 2523/2025 no es el foro para decidir esta tesis penal",
        "El silencio no se tratará como admisión",
    ]
    required_en = [
        "serious, document-based investigative thesis",
        "Materially excessive Administrator allegations",
        "Exceptionally severe Fiscal opinion",
        "Institutional circularity in DI 248",
        "Selected judicial adoption",
        "Possible private benefit",
        "RPL 2523/2025 is not the forum for deciding this criminal thesis",
        "Silence will not be treated as admission",
    ]
    for marker in required_es:
        if marker not in es:
            errors.append(f"{es_path}: missing marker {marker!r}")
    for marker in required_en:
        if marker not in en:
            errors.append(f"{en_path}: missing marker {marker!r}")

    if es.count('class="cm-thesis-pillar"') != 5:
        errors.append(f"{es_path}: expected exactly five thesis pillars")
    if en.count('class="cm-thesis-pillar"') != 5:
        errors.append(f"{en_path}: expected exactly five thesis pillars")

    static_routes = {
        "es/calificacion-concurso-36-2012-vidas-paralelas/index.html": [
            'data-calificacion-misuse-thesis="featured"',
            "informe íntegro de 47 páginas",
            "DOC4–DOC8",
        ],
        "en/insolvency-classification-parallel-lives/index.html": [
            'data-calificacion-misuse-thesis="featured"',
            "complete 47-page report",
            "DOC4–DOC8",
        ],
        "es/concurso-36-2012-ap-seccion-4/index.html": [
            'data-calificacion-misuse-thesis="appeal"',
            "copia privada localizada ≠ grabación judicial certificada",
            "RPL 2523/2025 debe decidirse sólo",
        ],
        "en/insolvency-36-2012-ap-section-4/index.html": [
            'data-calificacion-misuse-thesis="appeal"',
            "located private copy ≠ court-certified recording",
            "RPL 2523/2025 must be decided only",
        ],
        "es/nota-independencia-judicial-estado-procesal-reserva-acciones/index.html": [
            'data-calificacion-misuse-thesis="independence-note"',
            "no solicita a la Audiencia Provincial",
            "tesis-uso-criminal-procedimiento-calificacion",
        ],
    }
    for path, markers in static_routes.items():
        body = read(path)
        for marker in markers:
            if marker not in body:
                errors.append(f"{path}: missing static control {marker!r}")

    context_routes = {
        "es/calificacion-concurso-36-2012-vidas-paralelas/index.html": [
            "LECTURA PENAL PRIMERO · PROTECCIÓN CIVIL EN PARALELO",
            "cinco de los seis instrumentos",
            "../concurso-36-2012-autos-resoluciones/",
            "MADRID DP 913/2025",
        ],
        "en/insolvency-classification-parallel-lives/index.html": [
            "CRIMINAL FIRST · CIVIL PROTECTION IN PARALLEL",
            "five of the six asserted instruments",
            "../insolvency-36-2012-orders-decisions/",
            "MADRID DP 913/2025",
        ],
        "es/eleconomista-javier-romera-enero2025/index.html": [
            "HISTORIA PROPUESTA → ALCANCE JUDICIAL → EFECTO DOCUMENTADO",
            "DP 913/2025 · JUZGADO DE INSTRUCCIÓN Nº 44 DE MADRID",
            "../calificacion-concurso-36-2012-vidas-paralelas/#eleconomista",
            "../concurso-36-2012-ap-seccion-4/",
            "../concurso-36-2012-autos-resoluciones/",
        ],
        "en/eleconomista-javier-romera-january2025/index.html": [
            "PROPOSED STORY → JUDICIAL SCOPE → DOCUMENTED EFFECT",
            "DP 913/2025 · MADRID INVESTIGATING COURT NO. 44",
            "../insolvency-classification-parallel-lives/#eleconomista",
            "../insolvency-36-2012-ap-section-4/",
            "../insolvency-36-2012-orders-decisions/",
        ],
        "es/concurso-36-2012-autos-resoluciones/index.html": [
            "TEXTO ÍNTEGRO → POSICIÓN → CONSECUENCIA",
            "../calificacion-concurso-36-2012-vidas-paralelas/",
            "../eleconomista-javier-romera-enero2025/#madrid-2025-media",
        ],
        "en/insolvency-36-2012-orders-decisions/index.html": [
            "FULL TEXT → POSITION → CONSEQUENCE",
            "../insolvency-classification-parallel-lives/",
            "../eleconomista-javier-romera-january2025/#madrid-2025-media",
        ],
    }
    for path, markers in context_routes.items():
        body = read(path)
        for marker in markers:
            if marker not in body:
                errors.append(f"{path}: missing criminal-first/context-link control {marker!r}")

    stale = {
        "es/calificacion-concurso-36-2012-vidas-paralelas/index.html": [
            "Siguen pendientes el informe/anexos auténticos e íntegros del AC",
            "debe completarse el informe original íntegro de calificación del AC",
        ],
        "en/insolvency-classification-parallel-lives/index.html": [
            "complete original AC classification report and every annex must be source-completed",
            "The complete AC report/annexes, complete DI 248 expediente",
        ],
        "es/concurso-36-2012-ap-seccion-4/index.html": [
            "Acta y grabación originales de la vista",
        ],
        "en/insolvency-36-2012-ap-section-4/index.html": [
            "The original record and recording of the 25 July 2023 hearing",
        ],
    }
    for path, phrases in stale.items():
        body = read(path)
        for phrase in phrases:
            if phrase in body:
                errors.append(f"{path}: stale source-status wording remains: {phrase!r}")

    loader = read("assets/calificacion-criminal-misuse-thesis-20260824.js")
    site = read("assets/site.js")
    css = read("assets/styles.css")
    render = read("scripts/render_calificacion_criminal_misuse_thesis.mjs")
    workflow = read(".github/workflows/validate-calificacion-criminal-misuse-thesis.yml")
    for marker in ["'/es/'", "'/en/'", "carta-abierta-ministerio-fiscal", "acosta-matos-perimetro", "dataset.calificacionMisuseThesis"]:
        if marker not in loader:
            errors.append(f"scoped loader missing {marker!r}")
    if "calificacion-criminal-misuse-thesis-20260824.js?v=20260824d" not in site:
        errors.append("assets/site.js: criminal-misuse loader not registered")
    if "CALIFICACION-CRIMINAL-MISUSE-THESIS-20260824" not in css:
        errors.append("assets/styles.css: scoped thesis styles missing")
    for marker in ["priorityStatic", "concurso-36-2012-ap-seccion-4", "nota-independencia-judicial-estado-procesal-reserva-acciones", "pinFirstRead", "source-funds-notice-section--featured", "const anchor = sourceFunds || hero", "observer.observe(main, { childList: true })", "calificacionMisusePin", "window.setInterval(pin, 1000)", "22000, 30000"]:
        if marker not in loader:
            errors.append(f"scoped loader missing first-read stability control {marker!r}")
    for marker in ["es-institutional", "en-appeal", "es-acosta", "es-guided-calificacion", "sourceFundsCount", "appealFirewall", "positionCount", "closureTests", "20260824d"]:
        if marker not in render:
            errors.append(f"rendered first-read gate missing {marker!r}")
    if "render_calificacion_criminal_misuse_thesis.mjs" not in workflow or "Upload rendered validation evidence" not in workflow:
        errors.append("Calificación thesis workflow does not execute and preserve the rendered first-read gate")
    reader = read("assets/calificacion-reader-experience-20260817.js")
    if "criminalMisuse = block('[data-calificacion-misuse-thesis]')" not in reader or "gateway,\n        criminalMisuse," not in reader:
        errors.append("Calificación reader order does not keep the thesis in the first-read sequence")
    audience = read("assets/audience-experience-order-20260823.js")
    if "const criminalMisuse = main.querySelector('[data-calificacion-misuse-thesis]')" not in audience or "[criminalMisuse, priority, prosecution" not in audience:
        errors.append("Homepage audience organiser does not protect the thesis in the first-read sequence")

    sitemap = read("sitemap-calificacion.xml")
    for route in ["/es/tesis-uso-criminal-procedimiento-calificacion/", "/en/insolvency-classification-criminal-misuse-thesis/"]:
        if route not in sitemap:
            errors.append(f"sitemap-calificacion.xml: missing {route}")
    registry = json.loads(read("assets/data/unitary-route-registry-v1.json"))
    registered = {item.get("path") for item in registry}
    for route in ["es/tesis-uso-criminal-procedimiento-calificacion/", "en/insolvency-classification-criminal-misuse-thesis/"]:
        if route not in registered:
            errors.append(f"unitary route registry: missing {route}")

    data = json.loads(read("assets/data/calificacion-criminal-misuse-thesis-v1.json"))
    if len(data.get("pillars", [])) != 5:
        errors.append("machine-readable ledger must contain five pillars")
    if data.get("proof_boundary", {}).get("criminal_guilt_adjudicated") is not False:
        errors.append("machine-readable ledger must preserve non-adjudication boundary")

    if errors:
        print("CALIFICACION CRIMINAL-MISUSE THESIS: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1
    print("CALIFICACION CRIMINAL-MISUSE THESIS: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

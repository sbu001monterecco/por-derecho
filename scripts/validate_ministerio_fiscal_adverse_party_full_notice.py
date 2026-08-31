#!/usr/bin/env python3
"""Validate the Ministerio Fiscal adverse-party/full-notice controlled release."""
from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in {"a", "link", "script"}:
            return
        key = "href" if tag in {"a", "link"} else "src"
        value = dict(attrs).get(key)
        if value:
            self.links.append(value)


def check_markers(errors: list[str], path: str, markers: list[str]) -> None:
    body = read(path)
    for marker in markers:
        if marker not in body:
            errors.append(f"{path}: missing marker {marker!r}")


def check_local_links(errors: list[str], path: str) -> None:
    parser = LinkParser()
    parser.feed(read(path))
    base = (ROOT / path).parent
    for raw in parser.links:
        parsed = urlsplit(raw)
        if parsed.scheme or raw.startswith("//") or raw.startswith("#"):
            continue
        target_text = unquote(parsed.path)
        if not target_text:
            continue
        if target_text.startswith("/por-derecho/"):
            target = ROOT / target_text.removeprefix("/por-derecho/")
        elif target_text.startswith("/"):
            continue
        else:
            target = (base / target_text).resolve()
        if target.is_dir() or target_text.endswith("/"):
            target = target / "index.html"
        if not target.exists():
            errors.append(f"{path}: unresolved local link {raw!r} -> {target.relative_to(ROOT) if ROOT in target.parents else target}")


def main() -> int:
    errors: list[str] = []

    pages = {
        "es/ministerio-fiscal-aviso-expreso-dano-patrimonial/index.html": [
            "actor institucional adverso",
            "antes o, a más tardar",
            "instrumentalización",
            "escudo institucional",
            "DP 1901/2026 · ADVERTENCIA DE HABILITACIÓN ACTIVA",
            "habilitar activamente",
            "Publicar no equivale a servir, recibir, leer o responder",
            "no una declaración judicial de culpabilidad",
            "../ricardo-de-mosteyrin-sampalo/",
            "../fiscalia-inspeccion-exp-gub-745-2026/#respuesta-paralela",
        ],
        "en/public-prosecution-full-notice-patrimonial-harm/index.html": [
            "adverse institutional actor",
            "before or, at the latest",
            "active instrumentalisation",
            "institutional shield",
            "DP 1901/2026 · ACTIVE-ENABLEMENT WARNING",
            "actively enable",
            "Publication is not service, receipt, reading or response",
            "not a judicial finding of institutional or collective guilt",
            "../ricardo-de-mosteyrin-sampalo/",
            "../public-prosecution-inspection-exp-gub-745-2026/#parallel-response",
        ],
        "es/ricardo-de-mosteyrin-sampalo/index.html": [
            "Ricardo de Mosteyrín Sampalo",
            "El blanqueo de capitales y el delito de fraude fiscal",
            "30 de noviembre de 2016",
            "Fiscal de delitos económicos",
            "12 MARZO 2019 · DOCUMENTADO",
            "25 JULIO 2023 · DOS CAPAS",
            "antes o, a más tardar",
            "NO ES UNA CONDENA",
            "El silencio no se tratará como admisión",
        ],
        "en/ricardo-de-mosteyrin-sampalo/index.html": [
            "Ricardo de Mosteyrín Sampalo",
            "El blanqueo de capitales y el delito de fraude fiscal",
            "30 November 2016",
            "Economic Crimes Prosecutor",
            "12 MARCH 2019 · DOCUMENTED",
            "25 JULY 2023 · TWO LAYERS",
            "before or, at the latest",
            "NOT A CONVICTION",
            "Silence will not be treated as admission",
        ],
        "es/fiscalia-inspeccion-exp-gub-745-2026/index.html": [
            "POSTURA ADVERSA · RESPUESTA MULTIVÍA PARALELA",
            "PREPARADA / PENDIENTE — NO VERIFICADA COMO PRESENTADA",
            "Producción DP 1901",
            "Responsabilidad actor-específica",
            "No ejecutado por esta publicación",
        ],
        "en/public-prosecution-inspection-exp-gub-745-2026/index.html": [
            "ADVERSE POSTURE · PARALLEL MULTITRACK RESPONSE",
            "PREPARED / OUTSTANDING — NOT VERIFIED FILED",
            "DP 1901 production",
            "Actor-specific accountability",
            "Not executed by this publication",
        ],
    }
    for path, markers in pages.items():
        check_markers(errors, path, markers)
        check_local_links(errors, path)

    cross_links = {
        "es/tesis-uso-criminal-procedimiento-calificacion/index.html": [
            "../ministerio-fiscal-aviso-expreso-dano-patrimonial/",
        ],
        "en/insolvency-classification-criminal-misuse-thesis/index.html": [
            "../public-prosecution-full-notice-patrimonial-harm/",
        ],
        "es/dp-1901-2026/index.html": ["../ministerio-fiscal-aviso-expreso-dano-patrimonial/"],
        "en/dp-1901-2026/index.html": ["../public-prosecution-full-notice-patrimonial-harm/"],
        "es/carta-abierta-ministerio-fiscal/index.html": ["../ministerio-fiscal-aviso-expreso-dano-patrimonial/"],
        "en/open-letter-public-prosecution-service/index.html": ["../public-prosecution-full-notice-patrimonial-harm/"],
        "es/justicia-registro-institucional/index.html": ["../ministerio-fiscal-aviso-expreso-dano-patrimonial/"],
        "en/justice-institutional-record/index.html": ["../public-prosecution-full-notice-patrimonial-harm/"],
        "es/calificacion-concurso-36-2012-vidas-paralelas/index.html": ["../ricardo-de-mosteyrin-sampalo/"],
        "en/insolvency-classification-parallel-lives/index.html": ["../ricardo-de-mosteyrin-sampalo/"],
    }
    for path, markers in cross_links.items():
        check_markers(errors, path, markers)

    for path in [
        ".github/governance/MINISTERIO_FISCAL_ADVERSE_PARTY_FULL_NOTICE_PROTOCOL_31AUG2026.md",
        "archive/prompts/MINISTERIO_FISCAL_ADVERSE_PARTY_FULL_NOTICE_EXECUTION_PROMPT_31AUG2026.md",
        "publication-manifests/ministerio-fiscal-adverse-party-full-notice-20260831.json",
        "assets/data/ministerio-fiscal-adverse-party-full-notice-v1.json",
        "assets/data/ricardo-de-mosteyrin-sampalo-v1.json",
    ]:
        if not (ROOT / path).exists():
            errors.append(f"missing controlled artifact {path}")

    notice = json.loads(read("assets/data/ministerio-fiscal-adverse-party-full-notice-v1.json"))
    person = json.loads(read("assets/data/ricardo-de-mosteyrin-sampalo-v1.json"))
    people_registry = json.loads(read("assets/data/matter-identity-registry-v1.people.json"))
    manifest = json.loads(read("publication-manifests/ministerio-fiscal-adverse-party-full-notice-20260831.json"))
    calificacion = json.loads(read("assets/data/calificacion-criminal-misuse-thesis-v1.json"))

    if notice.get("formal_finding") is not False:
        errors.append("notice ledger must preserve formal_finding=false")
    states = notice.get("notice_states", {})
    for key in ["registered_or_served_by_this_release", "institutionally_received_from_this_release", "personally_accessed", "substantively_answered"]:
        if states.get(key) is not False:
            errors.append(f"notice state {key} must remain false absent independent proof")
    if "PREPARED_OUTSTANDING_NOT_VERIFIED_FILED" != notice.get("eg745_parallel_response", {}).get("reconsideration"):
        errors.append("E.G. 745 reconsideration status is not controlled")
    if person.get("person", {}).get("registry_id") != "PD-SP-P-0058":
        errors.append("Ricardo actor record has wrong identity-registry ID")
    registry_person = next(
        (record for record in people_registry.get("records", []) if record.get("id") == "PD-SP-P-0058"),
        None,
    )
    if not registry_person:
        errors.append("Ricardo is missing from the canonical people registry")
    elif registry_person.get("routes") != {
        "es": "/es/ricardo-de-mosteyrin-sampalo/",
        "en": "/en/ricardo-de-mosteyrin-sampalo/",
    }:
        errors.append("Ricardo canonical identity record does not point to both dedicated routes")
    if "competence context" not in person.get("knowledge_boundary", ""):
        errors.append("Ricardo actor record lacks specialist-competence boundary")
    if calificacion.get("fiscal_threshold_and_notice", {}).get("threshold_allegation") != "BEFORE_OR_AT_LATEST_DURING_25_JULY_2023_HEARING":
        errors.append("Calificación ledger does not preserve corrected threshold timing")

    live = manifest.get("current_state") == "LIVE_VERIFIED"
    if live and states.get("publicly_published") is not True:
        errors.append("LIVE_VERIFIED manifest requires publicly_published=true")
    if not live and states.get("publicly_published") is not False:
        errors.append("pre-live manifest requires publicly_published=false")

    sitemap = read("sitemap-prosecution-evidence.xml")
    for route in [
        "/es/ministerio-fiscal-aviso-expreso-dano-patrimonial/",
        "/en/public-prosecution-full-notice-patrimonial-harm/",
        "/es/ricardo-de-mosteyrin-sampalo/",
        "/en/ricardo-de-mosteyrin-sampalo/",
    ]:
        if route not in sitemap:
            errors.append(f"sitemap-prosecution-evidence.xml: missing {route}")

    combined = "\n".join(read(path) for path in pages)
    forbidden = [
        "Fiscalía es culpable",
        "Fiscalía is guilty",
        "culpabilidad está probada",
        "guilt is proved",
        "publicación acredita servicio formal",
        "publication proves formal service",
    ]
    for phrase in forbidden:
        if phrase.lower() in combined.lower():
            errors.append(f"forbidden categorical statement present: {phrase!r}")

    if errors:
        print("MINISTERIO FISCAL ADVERSE-PARTY FULL NOTICE: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1
    print("MINISTERIO FISCAL ADVERSE-PARTY FULL NOTICE: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Validate the bilingual Community professional/corporate network package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://sbu001monterecco.github.io/por-derecho/"
SLUGS = (
    "alvaro-campanario-hernandez",
    "juan-carlos-prieto-puente",
    "esteban-lopez-noriega",
    "antonio-cogolludo-rojas",
    "millan-and-miners-slp",
    "pamanil-sl",
    "pamalexsha-servicios-integrales-sl",
    "explotaciones-noalpa-sl",
    "santa-lucia-real-estate-sl",
    "shaila-maria-cogolludo-ramos",
    "francisco-mario-matos-matas",
    "francisco-de-borja-rodriguez-batllori-laffitte",
    "asuncion-aizpurua-sanchez",
    "montelanza-monte-lanza-sl",
    "inversiones-salinetas-sl",
)

SPECIAL_MARKERS = {
    ("es", "shaila-maria-cogolludo-ramos"): ("no prueban parentesco", "transfieren actos"),
    ("en", "shaila-maria-cogolludo-ramos"): ("do not prove kinship", "transfer acts"),
    ("es", "francisco-mario-matos-matas"): ("mata/matas", "dni", "francisco matos matas"),
    ("en", "francisco-mario-matos-matas"): ("mata/matas", "national id", "francisco matos matas"),
    ("es", "francisco-de-borja-rodriguez-batllori-laffitte"): ("no es un actor privado", "no fue el juez"),
    ("en", "francisco-de-borja-rodriguez-batllori-laffitte"): ("not a private actor", "was not the judge"),
    ("es", "asuncion-aizpurua-sanchez"): ("maría asunción aizpurúa sánchez", "se rechaza como puente"),
    ("en", "asuncion-aizpurua-sanchez"): ("maría asunción aizpurúa sánchez", "rejected as a bridge"),
    ("es", "montelanza-monte-lanza-sl"): ("cif b35279850", "gc1339", "certificado"),
    ("en", "montelanza-monte-lanza-sl"): ("cif b35279850", "gc1339", "certificate"),
    ("es", "inversiones-salinetas-sl"): ("no ha cerrado", "cadena finca por finca"),
    ("en", "inversiones-salinetas-sl"): ("has not closed", "unit-by-unit chain"),
}


def read(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        fail(f"missing file: {relative}")
    return path.read_text(encoding="utf-8")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_data() -> None:
    relative = "assets/data/community-professional-corporate-network-v1.json"
    try:
        data = json.loads(read(relative))
    except json.JSONDecodeError as exc:
        fail(f"invalid network JSON: {exc}")

    require(data.get("schema_version") == "1.0.0", "unexpected network schema version")
    require(data.get("publication_date") == "2026-08-25", "unexpected publication date")
    nodes = data.get("nodes")
    edges = data.get("edges")
    sources = data.get("sources")
    require(isinstance(nodes, list) and len(nodes) == 15, "network must contain exactly fifteen nodes")
    require(isinstance(edges, list) and len(edges) >= 10, "network must contain a meaningful edge register")
    require(isinstance(sources, dict) and len(sources) >= 15, "network source register is incomplete")

    routes = set()
    for node in nodes:
        canonical = node.get("canonical_name")
        require(isinstance(canonical, str) and canonical.strip(), "node missing canonical name")
        node_routes = node.get("routes")
        require(isinstance(node_routes, dict), f"{canonical}: missing routes")
        require(set(node_routes) == {"es", "en"}, f"{canonical}: bilingual route mismatch")
        routes.update((lang, route) for lang, route in node_routes.items())
        require(node.get("lanes"), f"{canonical}: evidence lanes missing")
        require(node.get("corrections"), f"{canonical}: correction controls missing")
        require(node.get("questions"), f"{canonical}: open questions missing")
        node_sources = [sources[source_id] for source_id in node.get("source_ids", [])]
        source_classes = {source.get("class") for source in node_sources}
        require("internal" in source_classes, f"{canonical}: internal source missing")
        require("official" in source_classes or node.get("official_gap"), f"{canonical}: official source or explicit gap missing")

    expected_routes = {(lang, slug) for lang in ("es", "en") for slug in SLUGS}
    require(routes == expected_routes, "data routes do not match the 30-route package")
    by_id = {node["id"]: node for node in nodes}
    require(set(by_id) == {"campanario", "prieto", "noriega", "antonio", "millan", "pamanil", "pamalexsha", "noalpa", "santa_lucia", "shaila", "fmmm", "rodriguez_batllori", "asuncion", "montelanza", "salinetas"}, "node identity register mismatch")
    for node_id in ("asuncion", "salinetas"):
        classes = {sources[source_id]["class"] for source_id in by_id[node_id]["source_ids"]}
        require("official" not in classes and by_id[node_id].get("official_gap"), f"{node_id}: bounded official gap must remain explicit")
    official_edges = [edge for edge in edges if edge.get("status") == "official"]
    attributed_edges = [edge for edge in edges if edge.get("status") == "attributed"]
    require(len(official_edges) >= 6, "official relationship lane is incomplete")
    require(len(attributed_edges) >= 2, "attributed relationship lane is incomplete")


def validate_pages() -> None:
    for lang in ("es", "en"):
        other = "en" if lang == "es" else "es"
        for slug in SLUGS:
            relative = f"{lang}/{slug}/index.html"
            html = read(relative)
            canonical = f"{BASE}{lang}/{slug}/"
            counterpart = f"{BASE}{other}/{slug}/"
            require(re.search(rf'<html[^>]+lang=["\']{lang}["\']', html, re.I) is not None, f"{relative}: wrong lang")
            require(f'<link rel="canonical" href="{canonical}">' in html, f"{relative}: canonical mismatch")
            require(f'hreflang="{lang}" href="{canonical}"' in html, f"{relative}: own hreflang missing")
            require(f'hreflang="{other}" href="{counterpart}"' in html, f"{relative}: reciprocal hreflang missing")
            require('hreflang="x-default"' in html, f"{relative}: x-default missing")
            require("<main" in html and "<h1" in html, f"{relative}: main heading structure missing")
            require("skip-link" in html, f"{relative}: skip link missing")
            provenance = "DECL011" in html or "011_WITNESS_GIL_PERIMETER" in html or "source-intunitaryscan" in html
            require(provenance, f"{relative}: controlled declaration/scan provenance missing")
            right_of_reply = "derecho de respuesta" if lang == "es" else "right of reply"
            require(right_of_reply in html.lower(), f"{relative}: right-of-reply section missing")
            for linked_slug in SLUGS:
                linked = f"/{lang}/{linked_slug}/" in html or f'href="../{linked_slug}/"' in html
                require(linked, f"{relative}: missing cross-link to {linked_slug}")
            for marker in SPECIAL_MARKERS.get((lang, slug), ()):
                require(marker in html.lower(), f"{relative}: missing controlled caveat marker {marker}")


def validate_discovery() -> None:
    discovery_files = (
        "es/actores-partes-abogados-representantes/index.html",
        "en/actors-parties-lawyers-representatives/index.html",
        "es/comunidad-instrumentalizacion/index.html",
        "en/community-instrumentalisation/index.html",
        "es/indice-web/index.html",
        "en/site-index/index.html",
    )
    for relative in discovery_files:
        text = read(relative)
        for slug in SLUGS:
            require(slug in text, f"{relative}: missing discovery link for {slug}")

    registry = json.loads(read("assets/data/unitary-route-registry-v1.json"))
    paths = [record.get("path") for record in registry]
    for lang in ("es", "en"):
        for slug in SLUGS:
            route = f"{lang}/{slug}/"
            require(paths.count(route) == 1, f"route registry must contain exactly one {route}")

    for relative in ("sitemap.xml", "sitemap-community-governance.xml"):
        text = read(relative)
        for lang in ("es", "en"):
            for slug in SLUGS:
                url = f"{BASE}{lang}/{slug}/"
                require(text.count(f"<loc>{url}</loc>") == 1, f"{relative}: expected one loc for {url}")


def validate_declaration_and_scan() -> None:
    declaration = read(
        "archive/declarations/011_WITNESS_GIL_PERIMETER_CAMPANARIO_PRIETO_NORIEGA_COMMUNITY_NETWORK_20260825.md"
    )
    required = (
        "Testigo del perímetro de Gil Marer — identidad reservada",
        "no firmada",
        "no jurada",
        "no ratificada palabra por palabra",
        "No existe certificación conjunta ni de verdad final",
        "84,988%",
        "74,90%",
        "22 de junio de 2011",
        "MILLAN AND MINERS SOCIEDAD LIMITADA PROFESIONAL",
        "Santa Lucia Real Estate",
        "Atilio Alberto Maddonni Citara",
    )
    for marker in required:
        require(marker in declaration, f"Declaration 011 missing control: {marker}")

    scan = read("archive/CAMPANARIO_PRIETO_NORIEGA_COMMUNITY_CORPORATE_UNITARY_SCAN_25AUG2026.md")
    for marker in (
        "resultado de búsqueda finita",
        "1995",
        "2002–2004",
        "2004",
        "marzo–abril de 2009",
        "No se localizaron pruebas independientes",
    ):
        require(marker in scan, f"unitary scan missing boundary: {marker}")


def main() -> None:
    validate_data()
    validate_pages()
    validate_discovery()
    validate_declaration_and_scan()
    print("PASS: Community professional/corporate network package validated")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate Por Derecho technical-partner and Second Pair publication controls."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

ROUTES = {
    "en_second_pair": ROOT / "en/por-derecho/second-pair-of-eyes/index.html",
    "es_second_pair": ROOT / "es/por-derecho/segundo-par-de-ojos/index.html",
    "en_technical_partners": ROOT / "en/por-derecho/technical-partners/index.html",
    "es_technical_partners": ROOT / "es/por-derecho/socios-tecnicos/index.html",
    "en_home": ROOT / "en/por-derecho/index.html",
    "es_home": ROOT / "es/por-derecho/index.html",
    "en_apps": ROOT / "en/por-derecho/applications-and-collaboration/index.html",
    "es_apps": ROOT / "es/por-derecho/aplicaciones-y-colaboracion/index.html",
    "en_pilot": ROOT / "en/por-derecho/applications-and-collaboration/pilot-pack/index.html",
    "es_pilot": ROOT / "es/por-derecho/aplicaciones-y-colaboracion/paquete-piloto/index.html",
}

SITEMAPS = [
    ROOT / "sitemap.xml",
    ROOT / "sitemap-por-derecho-foundation.xml",
]

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang = ""
        self.title_count = 0
        self.main_count = 0
        self.ids: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "html":
            self.lang = data.get("lang") or ""
        if tag == "title":
            self.title_count += 1
        if tag == "main":
            self.main_count += 1
        if data.get("id"):
            self.ids.append(data["id"] or "")


html = {name: read(path) for name, path in ROUTES.items()}
lower = {name: body.lower() for name, body in html.items()}

for name in ("en_second_pair", "es_second_pair", "en_technical_partners", "es_technical_partners"):
    parser = StructureParser()
    parser.feed(html[name])
    expected_lang = "es" if name.startswith("es_") else "en"
    require(parser.lang == expected_lang, f"{name}: incorrect html lang")
    require(parser.title_count == 1, f"{name}: expected one title")
    require(parser.main_count == 1, f"{name}: expected one main element")
    require(len(parser.ids) == len(set(parser.ids)), f"{name}: duplicate ids")
    require('content="index,follow"' in lower[name], f"{name}: missing index/follow")
    require("por-derecho.css" in html[name], f"{name}: missing Por Derecho stylesheet")
    require("pd-language" in html[name], f"{name}: missing language control")

pairs = [
    (
        "en_second_pair",
        "es_second_pair",
        "/en/por-derecho/second-pair-of-eyes/",
        "/es/por-derecho/segundo-par-de-ojos/",
    ),
    (
        "en_technical_partners",
        "es_technical_partners",
        "/en/por-derecho/technical-partners/",
        "/es/por-derecho/socios-tecnicos/",
    ),
]

for en_name, es_name, en_route, es_route in pairs:
    require(en_route in html[en_name], f"{en_name}: missing English canonical/route")
    require(es_route in html[en_name], f"{en_name}: missing Spanish reciprocal")
    require(es_route in html[es_name], f"{es_name}: missing Spanish canonical/route")
    require(en_route in html[es_name], f"{es_name}: missing English reciprocal")

for name in ("en_second_pair", "en_technical_partners"):
    body = lower[name]
    require("initiative in formation" in body, f"{name}: formation status missing")
    require("no automated decision" in body or "automated decisions" in body, f"{name}: automated-decision boundary missing")
    require("no institutional adoption" in body or "institutional adoption" in body, f"{name}: adoption boundary missing")
    require("no confidential" in body or "confidential evidence" in body, f"{name}: confidential-file boundary missing")
    require("synthetic" in body, f"{name}: synthetic-first route missing")
    require("technical partner" in body or "technical partners" in body, f"{name}: technical-partner language missing")

for name in ("es_second_pair", "es_technical_partners"):
    body = lower[name]
    require("iniciativa en formación" in body, f"{name}: formation status missing")
    require("decisión automatizada" in body or "decisiones automatizadas" in body, f"{name}: automated-decision boundary missing")
    require("adopción institucional" in body, f"{name}: adoption boundary missing")
    require("confidencial" in body, f"{name}: confidential-file boundary missing")
    require("sintético" in body or "sintética" in body, f"{name}: synthetic-first route missing")
    require("socio técnico" in body or "socios técnicos" in body, f"{name}: technical-partner language missing")

for name in ("en_home", "en_apps", "en_pilot"):
    require("technical-partners/" in html[name], f"{name}: missing technical-partner route")
for name in ("es_home", "es_apps", "es_pilot"):
    require("socios-tecnicos/" in html[name], f"{name}: missing socios-tecnicos route")

for name in ("en_home", "es_home"):
    require("founding stress test" in lower[name] or "prueba de tensión fundacional" in lower[name], f"{name}: live matter bridge missing")

joined = "\n".join(lower.values())
for phrase in (
    "source",
    "authority",
    "perimeter",
    "contradiction",
    "consequence",
    "reversibility",
    "fuente",
    "autoridad",
    "perímetro",
    "contradicción",
    "consecuencia",
    "reversibilidad",
):
    require(phrase in joined, f"missing Second Pair check phrase: {phrase}")

for pattern in (
    r"\bcib (has|is|will be) (partner|partnering|engaged|endorsing)\b",
    r"\bcib ha (colaborado|adoptado|respaldado|aceptado)\b",
    r"\btechnical partner engagement is confirmed\b",
    r"\binterlocución con cib confirmada\b",
    r"\bpor derecho is a registered foundation\b",
    r"\bpor derecho es una fundación registrada\b",
    r"\binstitutional adoption is confirmed\b",
    r"\badopción institucional confirmada\b",
    r"\bautomated legal decision\b",
    r"\bdecisión jurídica automatizada\b",
    r"(?<!no )\bguilt score is permitted\b",
    r"(?<!no )\bcredibility score is permitted\b",
    r"\bse permite puntuación de culpabilidad\b",
    r"\bse permite puntuación de credibilidad\b",
):
    require(re.search(pattern, joined) is None, f"forbidden public status/control phrase matched: {pattern}")

for sitemap_path in SITEMAPS:
    body = read(sitemap_path)
    try:
        ET.parse(sitemap_path)
    except ET.ParseError as exc:
        errors.append(f"invalid XML {sitemap_path.name}: {exc}")
    for route in (
        "/en/por-derecho/second-pair-of-eyes/",
        "/es/por-derecho/segundo-par-de-ojos/",
        "/en/por-derecho/technical-partners/",
        "/es/por-derecho/socios-tecnicos/",
    ):
        require(route in body, f"{sitemap_path.name}: missing {route}")

if errors:
    print("Por Derecho technical-partner validation: FAIL")
    for item in errors:
        print(f"- {item}")
    sys.exit(1)

print("Por Derecho technical-partner validation: PASS")
print("Validated bilingual partner routes, Second Pair routes, navigation bridges, status boundaries and sitemap entries.")

#!/usr/bin/env python3
"""Validate Por Derecho Foundation stage-two publication and governance boundaries."""
from __future__ import annotations

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]

ROUTES = {
    "es_origin": ROOT / "es/por-derecho/origen/index.html",
    "en_origin": ROOT / "en/por-derecho/origin/index.html",
    "es_governance": ROOT / "es/por-derecho/gobernanza-e-independencia/index.html",
    "en_governance": ROOT / "en/por-derecho/governance-and-independence/index.html",
    "es_research": ROOT / "es/por-derecho/investigacion-y-formacion/index.html",
    "en_research": ROOT / "en/por-derecho/research-and-training/index.html",
    "es_palacete": ROOT / "es/por-derecho/palacete/index.html",
    "en_palacete": ROOT / "en/por-derecho/palacete/index.html",
}

SOURCE_DOCS = {
    "formation": ROOT / "research/por-derecho/foundation-stage-2/01_FORMATION_AND_GOVERNANCE_WORKING_DRAFT_20AUG2026.md",
    "review": ROOT / "research/por-derecho/foundation-stage-2/02_INDEPENDENT_RED_TEAM_REVIEW_PROTOCOL_20AUG2026.md",
    "preservation": ROOT / "research/por-derecho/foundation-stage-2/03_SAN_BERNARDO_PRESERVATION_BRIEF_20AUG2026.md",
}

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def text(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


html = {name: text(path) for name, path in ROUTES.items()}
docs = {name: text(path) for name, path in SOURCE_DOCS.items()}
css = text(ROOT / "assets/por-derecho/foundation-stage-2.css")
js = text(ROOT / "assets/por-derecho/por-derecho.js")
robots = text(ROOT / "robots.txt")
sitemap_path = ROOT / "sitemap-por-derecho-foundation.xml"
sitemap = text(sitemap_path)
private_palacete = text(ROOT / "es/fundacion-por-derecho/palacete-por-derecho/index.html")
es_apps = text(ROOT / "es/por-derecho/aplicaciones-y-colaboracion/index.html")
en_apps = text(ROOT / "en/por-derecho/applications-and-collaboration/index.html")

# Required common assets and public indexing posture.
require(len(css) > 3000, "Foundation stage-two stylesheet is unexpectedly short")
for name, body in html.items():
    require("foundation-stage-2.css" in body, f"{name}: missing stage-two stylesheet")
    require("por-derecho.css" in body, f"{name}: missing Por Derecho base stylesheet")
    require('<meta name="robots" content="index,follow">' in body, f"{name}: public route is not index/follow")
    require("initiative in formation" in body.lower() or "iniciativa en formación" in body.lower(), f"{name}: formation status is not visible")
    require("pd-language" in body, f"{name}: missing language control")

# Canonical and reciprocal bilingual routes.
pairs = [
    ("es_origin", "en_origin", "/es/por-derecho/origen/", "/en/por-derecho/origin/"),
    ("es_governance", "en_governance", "/es/por-derecho/gobernanza-e-independencia/", "/en/por-derecho/governance-and-independence/"),
    ("es_research", "en_research", "/es/por-derecho/investigacion-y-formacion/", "/en/por-derecho/research-and-training/"),
    ("es_palacete", "en_palacete", "/es/por-derecho/palacete/", "/en/por-derecho/palacete/"),
]
for es_name, en_name, es_path, en_path in pairs:
    require(es_path in html[es_name], f"{es_name}: canonical/alternate route missing")
    require(en_path in html[es_name], f"{es_name}: English reciprocal route missing")
    require(en_path in html[en_name], f"{en_name}: canonical/alternate route missing")
    require(es_path in html[en_name], f"{en_name}: Spanish reciprocal route missing")

# Correct legal and institutional status.
for name in ("es_governance", "en_governance"):
    body = html[name].lower()
    require("borrador" in body or "draft" in body, f"{name}: draft status missing")
    require("no existe todavía fundación registrada" in body or "there is not yet a registered foundation" in body, f"{name}: exact non-registration statement missing")
    require("no está constituido" in body or "has not yet been constituted" in body or "not constituted" in body, f"{name}: proposed-body boundary missing")

for name in ("es_research", "en_research"):
    body = html[name].lower()
    require("revisión independiente no realizada" in body or "independent review not performed" in body, f"{name}: no-review status missing")
    require("caso prisma" in body or "case prism" in body, f"{name}: Case Prism status missing")
    require("validación interna" in body or "internal validation" in body, f"{name}: internal-validation status missing")
    require("no desplegar" in body or "do not deploy" in body, f"{name}: stop outcome missing")
    require("no puntuación" in body or "no scoring" in body, f"{name}: person-scoring prohibition missing")

for name in ("es_origin", "en_origin"):
    body = html[name].lower()
    require("dip 80/2026" in body and "dip 79/2026" in body, f"{name}: founder-related applications not identified")
    require("no constituyen validación externa" in body or "not external validation" in body, f"{name}: external-validation boundary missing")
    require("respaldo de icalpa" in body or "icalpa endorsement" in body, f"{name}: ICALPA endorsement boundary missing")

# Public Palacete must be preservation-only and transaction-safe.
for name in ("es_palacete", "en_palacete"):
    body = html[name].lower()
    require("adquisición no está completada" in body or "acquisition has not been completed" in body, f"{name}: acquisition status missing")
    require("no es" in body and "diligencia" in body or "not acquisition diligence" in body, f"{name}: diligence separation missing")
    require("no autoriza" in body or "does not authorise" in body, f"{name}: no-authority boundary missing")
    require("la casa no es la fundación" in body or "the house is not the foundation" in body, f"{name}: house/Foundation boundary missing")
    for forbidden in (
        "carlos llamas sanz",
        "entendimiento verbal",
        "verbal understanding",
        "purchase price",
        "precio de compra",
        "payment mechanics",
        "mecánica de pago",
        "family confirmation",
        "confirmación escrita de la familia",
        "ownership percentages",
        "porcentajes de titularidad",
    ):
        require(forbidden not in body, f"{name}: transaction-sensitive phrase leaked: {forbidden}")

# Private seller/adviser page must remain non-indexed and excluded from the public sitemap.
private_lower = private_palacete.lower()
require('content="noindex,nofollow,noarchive"' in private_lower, "private Palacete page lost noindex/nofollow/noarchive")
require("/es/fundacion-por-derecho/palacete-por-derecho/" not in sitemap, "private Palacete route leaked into public sitemap")

# Underlying source instruments must preserve the controlling boundaries.
formation = docs["formation"].lower()
require("working draft" in formation and "not an executed instrument" in formation, "formation document status boundary missing")
require("founder-related matter protocol" in formation, "formation document lacks founder-related protocol")
require("the house is not the foundation" in formation, "formation document lacks property independence")
require("guilt scores" in formation and "credibility scores" in formation, "formation document lacks prohibited output controls")

review = docs["review"].lower()
require("independent review not yet" in review, "review protocol falsely implies completed review")
require("wholly synthetic" in review, "review protocol lacks synthetic-first scope")
require("do not deploy" in review, "review protocol lacks stop outcome")
require("no case in the first independent round may be an anonymised live matter" in review, "review protocol lacks no-anonymised-live-case rule")
require("dip 79/2026" in review and "dip 80/2026" in review, "review protocol lacks founder-related application status")

preservation = docs["preservation"].lower()
require("not acquisition diligence" in preservation, "preservation brief lacks diligence separation")
require("creates no authority" in preservation, "preservation brief lacks no-authority statement")
require("the house is not the foundation" in preservation, "preservation brief lacks institutional independence")
require("no action on this list is authorised by this document itself" in preservation, "preservation brief lacks final no-authority gate")

# Runtime integration and corrected maturity ladder.
require("data-pd-foundation-stage2" in js or "pdFoundationStage2" in js, "home integration marker missing from runtime")
require("data-pd-maturity-20260820" in js or "pdMaturity20260820" in js, "maturity ladder marker missing from runtime")
for marker in (
    "Case Prism is under internal validation",
    "Caso Prisma prueba",
    "experimental founder-related research applications",
    "aplicaciones experimentales de investigación relacionadas con el fundador",
    "No institutional pilot is presently claimed",
    "No se afirma actualmente ningún piloto institucional",
):
    require(marker in js, f"runtime maturity statement missing: {marker}")
require("por-derecho.js" in es_apps and "por-derecho.js" in en_apps, "applications pages do not load common runtime")

# XML and robots controls.
try:
    ET.parse(sitemap_path)
except ET.ParseError as exc:
    errors.append(f"invalid Foundation sitemap XML: {exc}")
for _, _, es_path, en_path in pairs:
    require(es_path in sitemap and en_path in sitemap, f"sitemap missing pair: {es_path} / {en_path}")
require("sitemap-por-derecho-foundation.xml" in robots, "Foundation sitemap not registered in robots.txt")

# Guard against affirmative false status claims in the new public route family.
joined = "\n".join(html.values()).lower()
for pattern in (
    r"\bpor derecho is a registered foundation\b",
    r"\bpor derecho es una fundación registrada\b",
    r"\bcase prism is externally validated\b",
    r"\bcaso prisma está validado externamente\b",
    r"\bicalpa has adopted\b",
    r"\bicalpa ha adoptado\b",
    r"\bthe acquisition is complete\b",
    r"\bla adquisición está completada\b",
):
    require(re.search(pattern, joined) is None, f"false affirmative status claim matched: {pattern}")

if errors:
    print("Foundation stage-two validation: FAIL")
    for item in errors:
        print(f"- {item}")
    sys.exit(1)

print("Foundation stage-two validation: PASS")
print(f"Validated {len(ROUTES)} public routes, {len(SOURCE_DOCS)} source instruments, runtime integration, private/public separation and sitemap controls.")

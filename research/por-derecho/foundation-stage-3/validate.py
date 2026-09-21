#!/usr/bin/env python3
"""Validate Por Derecho Foundation stage-three execution controls."""
from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]

ES_PAGE = ROOT / "es/por-derecho/ejecucion-institucional/index.html"
EN_PAGE = ROOT / "en/por-derecho/institutional-execution/index.html"
PRIVATE_PALACETE = ROOT / "es/fundacion-por-derecho/palacete-por-derecho/index.html"
SITEMAP = ROOT / "sitemap-por-derecho-foundation.xml"
JS = ROOT / "assets/por-derecho/por-derecho.js"
CSS = ROOT / "assets/por-derecho/foundation-stage-3.css"
REGISTER = ROOT / "research/por-derecho/foundation-stage-3/foundation-stage-3-execution-register.json"

DOCS = [
    ROOT / "research/por-derecho/foundation-stage-3/01_FOUNDATION_LEGAL_NOTARIAL_INSTRUCTION_PACK_20AUG2026.md",
    ROOT / "research/por-derecho/foundation-stage-3/02_PROSPECTIVE_TRUSTEE_RECRUITMENT_AND_ACCEPTANCE_PACK_20AUG2026.md",
    ROOT / "research/por-derecho/foundation-stage-3/03_INDEPENDENT_RED_TEAM_COMMISSION_PACK_20AUG2026.md",
    ROOT / "research/por-derecho/foundation-stage-3/04_SAN_BERNARDO_CONSERVATION_ARCHITECT_RFP_20AUG2026.md",
    ROOT / "research/por-derecho/foundation-stage-3/05_NINETY_DAY_EXECUTION_CONTROL_REGISTER_20AUG2026.md",
    ROOT / "research/por-derecho/foundation-stage-3/06_OUTREACH_DRAFTS_AND_SEND_GATES_20AUG2026.md",
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


def validate_html(path: Path, language: str, reciprocal: str, canonical: str) -> str:
    body = read(path)
    parser = StructureParser()
    parser.feed(body)
    require(parser.lang == language, f"{path}: incorrect html lang")
    require(parser.title_count == 1, f"{path}: expected one title")
    require(parser.main_count == 1, f"{path}: expected one main element")
    require(len(parser.ids) == len(set(parser.ids)), f"{path}: duplicate ids")
    require('content="index,follow"' in body, f"{path}: public route must be index,follow")
    require(canonical in body, f"{path}: canonical route missing")
    require(reciprocal in body, f"{path}: reciprocal route missing")
    require("foundation-stage-3.css" in body, f"{path}: stage-three stylesheet missing")
    require("data-pd-foundation-stage3=\"20260820\"" in body, f"{path}: stage-three marker missing")
    return body


es = validate_html(
    ES_PAGE,
    "es",
    "/en/por-derecho/institutional-execution/",
    "/es/por-derecho/ejecucion-institucional/",
)
en = validate_html(
    EN_PAGE,
    "en",
    "/es/por-derecho/ejecucion-institucional/",
    "/en/por-derecho/institutional-execution/",
)
joined_public = f"{es}\n{en}".lower()

# Exact public status boundaries.
for phrase in (
    "iniciativa en formación",
    "no existe todavía fundación registrada",
    "sin nombramientos",
    "revisión no realizada",
    "sin acceso · sin arquitecto",
    "adquisición no completada",
    "la casa no es la fundación",
):
    require(phrase in es.lower(), f"Spanish execution page missing status: {phrase}")
for phrase in (
    "initiative in formation",
    "there is not yet a registered foundation",
    "no appointments",
    "review not performed",
    "no access · no architect",
    "acquisition incomplete",
    "the house is not the foundation",
):
    require(phrase in en.lower(), f"English execution page missing status: {phrase}")

# Names and transaction-sensitive material must not leak into public execution pages.
for forbidden in (
    "carlos llamas",
    "safira cantos",
    "ignacio gomá",
    "natividad martínez",
    "purchase price",
    "precio de compra",
    "payment mechanics",
    "mecánica de pago",
    "verbal understanding",
    "entendimiento verbal",
    "written family confirmation",
    "confirmación escrita de la familia",
):
    require(forbidden not in joined_public, f"public execution page leaked: {forbidden}")

# Guard against affirmative false status claims.
for pattern in (
    r"\bpor derecho es una fundación registrada\b",
    r"\bpor derecho is a registered foundation\b",
    r"\bel patronato está constituido\b",
    r"\bthe board has been constituted\b",
    r"\bla revisión independiente (ha sido|está) completada\b",
    r"\bindependent review (has been|is) completed\b",
    r"\bcaso prisma está validado externamente\b",
    r"\bcase prism is externally validated\b",
    r"\bla adquisición está completada\b",
    r"\bthe acquisition is complete\b",
    r"\bicalpa ha adoptado\b",
    r"\bicalpa has adopted\b",
):
    require(re.search(pattern, joined_public) is None, f"false public status matched: {pattern}")

# Validate source documents.
doc_text = [read(path) for path in DOCS]
legal, trustees, redteam, architect, control, outreach = [item.lower() for item in doc_text]

for marker in (
    "not legal advice",
    "not an executed mandate",
    "initiative in formation",
    "€30,000",
    "first action programme",
    "founder-related matter protocol",
    "the house is not the foundation",
    "official legal source anchors",
):
    require(marker.lower() in legal, f"legal instruction missing: {marker}")
require("sede.gobiernodecanarias.org" in legal, "legal instruction lacks official Canary registration source")
require("boe.es/eli/es/l/2002/12/26/50" in legal, "legal instruction lacks official state foundation-law source")
require("agenciatributaria.gob.es" in legal, "legal instruction lacks official tax source")

for marker in (
    "no person named or contacted through this pack is a patron",
    "not a search for prestige",
    "no permission",
    "recusal",
    "do not deploy",
):
    require(marker in trustees, f"trustee pack missing: {marker}")
require(
    "i do not by considering or accepting office endorse" in trustees
    or "does not by considering or accepting office endorse" in trustees,
    "trustee pack lacks the no-endorsement acceptance boundary",
)

for marker in (
    "no independent review has yet been performed",
    "wholly synthetic",
    "must not contain or require",
    "false positives",
    "false negatives",
    "do not deploy",
    "not performed",
):
    require(marker in redteam, f"red-team pack missing: {marker}")
require(
    "the first independent round must use a wholly synthetic record" in redteam,
    "red-team pack lacks the synthetic-first rule",
)
require("sun park" in redteam and "icalpa" in redteam, "red-team pack must expressly exclude live founder-related sources")

for marker in (
    "not sent",
    "not authority to access",
    "no professional may",
    "desk-based",
    "not acquisition diligence",
):
    require(marker in architect, f"architect RFP missing: {marker}")
require(
    "proposed future palacete por derecho; acquisition not completed" in architect,
    "architect RFP lacks the incomplete-acquisition context",
)
require(
    "architect appointed: **no**" in architect,
    "architect RFP lacks the no-appointment status",
)
require(
    "institutional plan subordinate to safety, fabric and legal constraints" in architect,
    "architect RFP lacks the building-over-programme boundary",
)

for marker in (
    "planned, prepared, sent, accepted, commissioned, completed, merged and publicly live are different states",
    "day 0–15",
    "day 16–30",
    "day 31–60",
    "day 61–90",
    "public status reconciliation",
):
    require(marker in control, f"90-day register missing: {marker}")

for marker in (
    "drafts only",
    "do not attach sun park",
    "no endorsement",
    "send gate",
    "no architect copied",
):
    require(marker in outreach, f"outreach control missing: {marker}")
require(
    "no public announcement without written institutional confirmation" in outreach
    or "the institution’s express written confirmation" in outreach,
    "outreach control lacks the institution-only confirmation rule",
)

# Machine-readable register.
register_text = read(REGISTER)
try:
    data = json.loads(register_text)
except json.JSONDecodeError as exc:
    errors.append(f"invalid stage-three JSON: {exc}")
    data = {}
require(data.get("register_id") == "PD-FDN-STAGE3-20260820", "incorrect execution register id")
require(data.get("institution", {}).get("registered_foundation") is False, "JSON falsely records a registered foundation")
require(data.get("institution", {}).get("patronato_constituted") is False, "JSON falsely records a constituted Patronato")
require(data.get("method_status", {}).get("independent_review") == "NOT_PERFORMED", "JSON review status is not NOT_PERFORMED")
require(data.get("property_status", {}).get("acquisition_complete") is False, "JSON falsely records completed acquisition")
require(data.get("property_status", {}).get("access_authorised_by_this_register") is False, "JSON falsely authorises property access")
require(len(data.get("workstreams", [])) == 6, "execution register must contain six workstreams")

# Runtime and sitemap integration.
js = read(JS)
css = read(CSS)
require(len(css) > 3500, "stage-three stylesheet unexpectedly short")
require("data-pd-foundation-stage3" in js, "runtime lacks stage-three home marker")
require("institutional-execution" in js and "ejecucion-institucional" in js, "runtime lacks bilingual execution links")
require("Four commission-ready packs" in js, "runtime lacks English execution gateway")
require("Cuatro paquetes preparados" in js, "runtime lacks Spanish execution gateway")
require("Independent review not performed" in js or "review not yet performed" in js, "runtime must preserve no-review status")

sitemap_text = read(SITEMAP)
try:
    ET.parse(SITEMAP)
except ET.ParseError as exc:
    errors.append(f"invalid Foundation sitemap: {exc}")
for route in (
    "/es/por-derecho/ejecucion-institucional/",
    "/en/por-derecho/institutional-execution/",
):
    require(route in sitemap_text, f"sitemap missing {route}")
require("/es/fundacion-por-derecho/palacete-por-derecho/" not in sitemap_text, "private Palacete route leaked to sitemap")

private_palacete = read(PRIVATE_PALACETE).lower()
require('content="noindex,nofollow,noarchive"' in private_palacete, "private Palacete page lost noindex/nofollow/noarchive")

if errors:
    print("Por Derecho Foundation stage-three validation: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Por Derecho Foundation stage-three validation: PASS")
print("Validated bilingual execution pages, six professional packs, machine-readable status, runtime integration and Palacete public/private boundary.")

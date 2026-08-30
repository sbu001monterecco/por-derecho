#!/usr/bin/env python3
"""Validate the controlled bilingual publication for DP 3205/2014."""

from __future__ import annotations

import csv
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

ES_PAGE = ROOT / "es/dp-3205-2014-arrecife/index.html"
EN_PAGE = ROOT / "en/dp-3205-2014-arrecife/index.html"
INSTITUTION_PART = ROOT / "assets/data/matter-identity-registry-v1.dp3205-institutions.json"
PROCEEDING_PART = ROOT / "assets/data/matter-identity-registry-v1.dp3205-proceedings.json"
REGISTRY = ROOT / "assets/data/matter-identity-registry-v1.json"
DP_DATA = ROOT / "assets/data/dp3205-2014-arrecife-v1.json"
MASTER = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
PRISM = ROOT / "assets/data/proceedings-case-prism-v1.json"
ROUTES = ROOT / "assets/data/unitary-route-registry-v1.json"
CONTROL = ROOT / "archive/DP3205_2014_ARRECIFE_SOURCE_TRANSLATION_AUTHORITY_ALLEGATIONS_CONTROL_30AUG2026.md"
MISSING = ROOT / "archive/MISSING_EVIDENCE_REGISTER.md"
MISSING_APPEND = ROOT / "archive/MISSING_EVIDENCE_REGISTER_DP3205_2014_APPEND_30AUG2026.md"
COUNSEL_GAPS = ROOT / "assets/data/counsel-procurador-gap-register-v1.json"
MASTER_RENDERER = ROOT / "assets/master-proceedings-publication-20260830.js"
MAP_RENDERER = ROOT / "assets/proceedings-interconnectivity-map-20260830.js"
REGISTRY_EN = ROOT / "en/matter-identity-registry/index.html"
REGISTRY_ES = ROOT / "es/registro-identidad-materia/index.html"

SITEMAPS = (
    ROOT / "sitemap.xml",
    ROOT / "sitemap-community-governance.xml",
    ROOT / "sitemap-judicial-spine.xml",
    ROOT / "sitemap-criminal-engineering.xml",
)

REVERSE_LINK_PAGES = (
    ROOT / "en/asuncion-aizpurua-sanchez/index.html",
    ROOT / "es/asuncion-aizpurua-sanchez/index.html",
    ROOT / "en/francisco-mario-matos-matas/index.html",
    ROOT / "es/francisco-mario-matos-matas/index.html",
    ROOT / "en/actors-parties-lawyers-representatives/index.html",
    ROOT / "es/actores-partes-abogados-representantes/index.html",
    ROOT / "en/community-instrumentalisation/index.html",
    ROOT / "es/comunidad-instrumentalizacion/index.html",
    ROOT / "en/insolvency-36-2012-community-authority/index.html",
    ROOT / "es/concurso-36-2012-autoridad-comunidad/index.html",
    ROOT / "en/insolvency-36-2012-arrecife-mercantile-bridge/index.html",
    ROOT / "es/concurso-36-2012-puente-arrecife-mercantil/index.html",
    ROOT / "en/unitary-criminal-hypothesis-2011-present/index.html",
    ROOT / "es/hipotesis-criminal-unitaria-2011-presente/index.html",
    ROOT / "en/site-index/index.html",
    ROOT / "es/indice-web/index.html",
)

PROCEEDING_ID = "PD-SP-R-0020"
INSTITUTION_ID = "PD-SP-I-0023"
MASTER_ID = "LZ-JUD-042"
REFERENCE = "DP 3205/2014"
SOURCE_ID = "PD-SP-SRC-DP3205-2014-SUMMARY-20181120"
SOURCE_CLASS = "DATED_SECONDARY_LEGAL_ADVISER_STATUS_SUMMARY"
SOURCE_STATUS = "SECONDARY_DATED_LEGAL_ADVISER_SUMMARY_PRIMARY_FILE_PENDING"
HISTORIC_ORGAN = "Juzgado de Instrucción nº 1 de Arrecife"
CURRENT_ORGAN = "Sección de Instrucción del Tribunal de Instancia de Arrecife — plaza nº 1"
ES_ROUTE = "/es/dp-3205-2014-arrecife/"
EN_ROUTE = "/en/dp-3205-2014-arrecife/"
PUBLIC_BASE = "https://sbu001monterecco.github.io/por-derecho"
EXPECTED_COUNTS = {
    "total": 228,
    "PERSON": 95,
    "ORGANISATION": 79,
    "STRUCTURE": 11,
    "INSTITUTION": 23,
    "PROCEEDING": 20,
}

failures: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    if not path.is_file():
        require(False, f"missing required file: {relative(path)}")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        require(False, f"cannot read UTF-8 text {relative(path)}: {exc}")
        return ""


def read_json(path: Path) -> Any:
    body = read_text(path)
    if not body:
        return {}
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        require(False, f"invalid JSON in {relative(path)}: {exc}")
        return {}


def includes(body: str, marker: str, location: str) -> None:
    require(marker.casefold() in body.casefold(), f"{location} missing marker: {marker}")


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, str]] = []
        self.html_lang = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag.casefold() == "html":
            self.html_lang = values.get("lang", "")
        if tag.casefold() == "link":
            self.links.append(values)


def check_page_metadata(path: Path, lang: str, own_route: str) -> None:
    body = read_text(path)
    parser = LinkParser()
    parser.feed(body)
    own_url = PUBLIC_BASE + own_route
    es_url = PUBLIC_BASE + ES_ROUTE
    en_url = PUBLIC_BASE + EN_ROUTE
    canonicals = [item.get("href", "") for item in parser.links if item.get("rel", "").casefold() == "canonical"]
    alternates = {
        item.get("hreflang", "").casefold(): item.get("href", "")
        for item in parser.links
        if "alternate" in item.get("rel", "").casefold().split()
    }
    require(parser.html_lang.casefold() == lang, f"{relative(path)} has wrong html lang")
    require(canonicals == [own_url], f"{relative(path)} canonical is not the exact self URL")
    require(alternates.get("es") == es_url, f"{relative(path)} lacks exact Spanish hreflang")
    require(alternates.get("en") == en_url, f"{relative(path)} lacks exact English hreflang")
    require(alternates.get("x-default") == es_url, f"{relative(path)} lacks the controlled x-default")


REQUIRED_FILES = (
    ES_PAGE,
    EN_PAGE,
    INSTITUTION_PART,
    PROCEEDING_PART,
    REGISTRY,
    DP_DATA,
    MASTER,
    PRISM,
    ROUTES,
    CONTROL,
    MISSING,
    MISSING_APPEND,
    COUNSEL_GAPS,
    MASTER_RENDERER,
    MAP_RENDERER,
    REGISTRY_EN,
    REGISTRY_ES,
    *SITEMAPS,
    *REVERSE_LINK_PAGES,
)

for required_file in REQUIRED_FILES:
    require(required_file.is_file(), f"missing required publication file: {relative(required_file)}")


# The public bilingual route must be canonical, reciprocal and visibly qualified.
check_page_metadata(ES_PAGE, "es", ES_ROUTE)
check_page_metadata(EN_PAGE, "en", EN_ROUTE)
es_page = read_text(ES_PAGE)
en_page = read_text(EN_PAGE)

page_markers = {
    ES_PAGE: (
        "DP 3205/2014<sup>^</sup>",
        "AMBER · identidad confirmada · fondo y resultado abiertos",
        "Qué significa el caret",
        "confirma únicamente la referencia exacta del procedimiento y la identidad del órgano histórico",
        "No autentica la denuncia",
        HISTORIC_ORGAN,
        "Sección de Instrucción del Tribunal de Instancia de Arrecife · Plaza nº 1",
        "31 diciembre 2025",
        "nombre completo omitido",
        "no son corroboración independiente",
        "ANÁLISIS DE ALEGACIONES · NO ES UN HALLAZGO",
        "alegaciones más amplias atribuidas a Gil Marer",
        "Otras no-inferencias",
        "Alternativa razonable no culpable",
        "evento de verificación de autoridad",
        "Ninguna fuente primaria localizada prueba acumulación",
    ),
    EN_PAGE: (
        "DP 3205/2014<sup>^</sup>",
        "AMBER · identity confirmed · merits and outcome open",
        "What the caret means",
        "confirms the exact proceeding reference and historic organ identity only",
        "does not authenticate the complaint",
        HISTORIC_ORGAN,
        "Sección de Instrucción del Tribunal de Instancia de Arrecife · Plaza nº 1",
        "31 December 2025",
        "full name withheld",
        "not independent corroboration",
        "ALLEGATION ANALYSIS · NOT A FINDING",
        "Gil Marer’s wider attributed allegations",
        "Further non-inferences",
        "Reasonable non-culpable alternative",
        "authority-verification event",
        "No located primary source proves joinder",
    ),
}
for page, markers in page_markers.items():
    body = es_page if page == ES_PAGE else en_page
    for marker in markers:
        includes(body, marker, relative(page))
    for proposition_number in range(1, 5):
        includes(body, f"DP3205-P0{proposition_number}", relative(page))

for marker in (
    "Controlled English translation",
    "Spanish source-language reconstruction",
    "The author adds that no further information was available",
):
    includes(en_page, marker, relative(EN_PAGE))
for marker in (
    "Reconstrucción controlada en español",
    "Traducción inglesa controlada",
    "El autor añade que no dispone de más información",
):
    includes(es_page, marker, relative(ES_PAGE))


# Resolve the proceeding and organ to the same immutable IDs in every canonical layer.
institution_data = read_json(INSTITUTION_PART)
proceeding_data = read_json(PROCEEDING_PART)
dp_data = read_json(DP_DATA)

institution_records = institution_data.get("records", []) if isinstance(institution_data, dict) else []
proceeding_records = proceeding_data.get("records", []) if isinstance(proceeding_data, dict) else []
require(len(institution_records) == 1, "DP3205 institution part must contain exactly one record")
require(len(proceeding_records) == 1, "DP3205 proceeding part must contain exactly one record")
institution = institution_records[0] if institution_records else {}
proceeding = proceeding_records[0] if proceeding_records else {}

require(institution.get("id") == INSTITUTION_ID, "institution part has the wrong immutable ID")
require(institution.get("type") == "INSTITUTION", "DP3205 organ must be an INSTITUTION record")
require(institution.get("identity_resolution") == "CARET_CONFIRMED", "institution caret identity is not confirmed")
require(HISTORIC_ORGAN in institution.get("name", ""), "institution name lacks the exact historic organ")
require(CURRENT_ORGAN in institution.get("name", ""), "institution name lacks the exact successor nomenclature")
includes(institution.get("date_boundary", ""), "31-Dec-2025", "institution date boundary")
require(institution.get("routes") == {"es": ES_ROUTE + "#organo", "en": EN_ROUTE + "#court"}, "institution routes are inconsistent")

require(proceeding.get("id") == PROCEEDING_ID, "proceeding part has the wrong immutable ID")
require(proceeding.get("type") == "PROCEEDING", "DP3205 must be a PROCEEDING record")
require(proceeding.get("identity_resolution") == "CARET_CONFIRMED", "proceeding caret identity is not confirmed")
require(proceeding.get("master_register_id") == MASTER_ID, "proceeding part has the wrong master ID")
require(proceeding.get("competent_organ") == INSTITUTION_ID, "proceeding part has the wrong organ ID")
require(proceeding.get("routes") == {"es": ES_ROUTE, "en": EN_ROUTE}, "proceeding routes are inconsistent")
require(proceeding.get("procedural_state") == "IDENTIFIED_OUTCOME_NOT_LOCATED", "proceeding state overclaims the outcome")
require(proceeding.get("identity_sources") == [SOURCE_ID], "proceeding source lineage is inconsistent")
includes(proceeding.get("identity_boundary", ""), "caret confirms only", "proceeding identity boundary")

identity = dp_data.get("identity", {}) if isinstance(dp_data, dict) else {}
require(dp_data.get("status") == "AMBER_IDENTIFIED_MERITS_AUTHORITY_OUTCOME_OPEN", "DP data lacks the exact AMBER state")
require(identity.get("registry_id") == PROCEEDING_ID, "DP data has the wrong registry ID")
require(identity.get("master_id") == MASTER_ID, "DP data has the wrong master ID")
require(identity.get("reference") == REFERENCE, "DP data has the wrong reference")
require(identity.get("organ_id") == INSTITUTION_ID, "DP data has the wrong organ ID")
require(identity.get("historic_organ") == HISTORIC_ORGAN, "DP data has the wrong historic organ")
require(identity.get("current_successor_name") == CURRENT_ORGAN, "DP data has the wrong successor nomenclature")
require(identity.get("caret_scope") == "Exact proceeding and organ identity only", "DP data overstates caret semantics")

expected_propositions = {
    "DP3205-P01": "SOURCE_REPORTED",
    "DP3205-P02": "SOURCE_REPORTED_IDENTITY_BRIDGES_OPEN",
    "DP3205-P03": "SOURCE_REPORTED_PRIMARY_FILE_OPEN",
    "DP3205-P04": "SOURCE_REPORTED",
}
propositions = dp_data.get("reported_propositions", []) if isinstance(dp_data, dict) else []
observed_propositions = {item.get("id"): item.get("state") for item in propositions if isinstance(item, dict)}
require(observed_propositions == expected_propositions, "DP3205 P01-P04 IDs or source states are incomplete")


# The protected respondent remains anonymised and the duplicate lineage stays singular.
participants = dp_data.get("participants", []) if isinstance(dp_data, dict) else []
private_candidates = [item for item in participants if isinstance(item, dict) and item.get("private_candidate") is True]
require(len(private_candidates) == 1, "DP data must contain exactly one anonymised private candidate")
if private_candidates:
    candidate = private_candidates[0]
    require(candidate.get("public_label") == "Second reported respondent", "private candidate uses a non-controlled public label")
    require("WITHHELD" in candidate.get("bridge_state", ""), "private candidate lacks the withheld-publication state")
    require("name" not in candidate and "registry_id" not in candidate, "private candidate exposes a name or public registry ID")

source_lineage = dp_data.get("source_lineage", {}) if isinstance(dp_data, dict) else {}
require(source_lineage.get("source_id") == SOURCE_ID, "DP data source ID is inconsistent")
require(source_lineage.get("source_class") == SOURCE_CLASS, "DP data must classify the source as a dated secondary summary")
includes(source_lineage.get("preservation", ""), "not independent corroboration", "DP source lineage")
includes(source_lineage.get("preservation", ""), "same source lineage", "DP source lineage")
includes(source_lineage.get("privacy", ""), "private-candidate full name", "DP privacy boundary")

# Construct protected literals at runtime so this validator cannot trigger its own repository scan.
protected_literals = (
    b"".join((b"Ste", b"phen ", b"Peter ", b"Hail")),
    b"".join((b"Ste", b"phen ", b"Hail")),
)
require(len(set(protected_literals)) == 2, "protected-name scan does not cover both required variants")
for path in ROOT.rglob("*"):
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        continue
    if ".git" in rel.parts or not path.is_file() or path.is_symlink():
        continue
    try:
        payload = path.read_bytes().lower()
    except OSError as exc:
        require(False, f"could not privacy-scan {relative(path)}: {exc}")
        continue
    if any(literal.lower() in payload for literal in protected_literals):
        require(False, f"protected respondent name appears in public repository file: {relative(path)}")


# Allegation analysis must retain non-inference, an innocent alternative and formal isolation.
context = dp_data.get("allegations_context", {}) if isinstance(dp_data, dict) else {}
includes(context.get("safe_use", ""), "Authority-verification event", "DP allegations context")
includes(context.get("safe_use", ""), "wider attributed Community-instrumentalisation theory", "DP allegations context")
not_established = context.get("does_not_establish", [])
require(isinstance(not_established, list) and len(not_established) >= 9, "DP allegations context lacks a finite non-inference list")
for marker in ("valid appointment or authority", "the alleged incident or injury", "knowledge, intent", "procedural outcome or finality"):
    includes("\n".join(str(item) for item in not_established), marker, "DP non-inference list")
includes(context.get("reasonable_alternative", ""), "ordinary personal complaint", "DP reasonable alternative")
includes(context.get("reasonable_alternative", ""), "non-culpable explanation", "DP reasonable alternative")

formal = dp_data.get("formal_relationships", {}) if isinstance(dp_data, dict) else {}
require(formal.get("linked_proceedings") == [], "DP data creates a formal proceeding link")
includes(formal.get("rule", ""), "legally distinct", "DP formal-isolation rule")
includes(formal.get("rule", ""), "primary source", "DP formal-isolation rule")


# The Master Register must carry the same identity without inventing a parent, link or review.
master_rows: list[dict[str, str]] = []
if MASTER.is_file():
    try:
        with MASTER.open(encoding="utf-8", newline="") as handle:
            master_rows = list(csv.DictReader(handle))
    except (OSError, UnicodeError, csv.Error) as exc:
        require(False, f"cannot parse {relative(MASTER)}: {exc}")
master_matches = [row for row in master_rows if row.get("Master_ID") == MASTER_ID]
require(len(master_matches) == 1, "Master Register must contain exactly one LZ-JUD-042 row")
master_row = master_matches[0] if master_matches else {}
for field, expected in {
    "Reference": REFERENCE,
    "Origin_Organ": HISTORIC_ORGAN,
    "Current_Custodian": CURRENT_ORGAN,
    "Primary_Source_Anchor": SOURCE_ID,
    "Source_Status": SOURCE_STATUS,
    "Is_Proceeding": "TRUE",
    "Stream": "Criminal",
}.items():
    require(master_row.get(field) == expected, f"Master Register {field} is inconsistent for {MASTER_ID}")
for field in ("Parent_Master_ID", "Linked_Proceedings", "Appeal_or_Review", "Secondary_Reference"):
    require(not master_row.get(field, "").strip(), f"Master Register incorrectly creates a formal link in {field}")
includes(master_row.get("Notes", ""), "Keep distinct", "Master Register isolation note")
includes(master_row.get("Notes", ""), "absent primary proof", "Master Register isolation note")


# P10 is direct only in the Arrecife lane and creates no other procedural bridge.
prism = read_json(PRISM)
lanes = prism.get("lanes", []) if isinstance(prism, dict) else []
arrecife_lanes = [lane for lane in lanes if isinstance(lane, dict) and lane.get("id") == "arrecife"]
require(len(arrecife_lanes) == 1, "prism must contain exactly one Arrecife lane")
if arrecife_lanes:
    require(MASTER_ID in arrecife_lanes[0].get("master_ids", []), "Arrecife lane lacks LZ-JUD-042")
lane_locations = [
    str(lane.get("id"))
    for lane in lanes
    if isinstance(lane, dict) and MASTER_ID in lane.get("master_ids", [])
]
require(lane_locations == ["arrecife"], "LZ-JUD-042 appears in a prism lane other than Arrecife")

prism_propositions = prism.get("propositions", []) if isinstance(prism, dict) else []
p10_matches = [item for item in prism_propositions if isinstance(item, dict) and item.get("id") == "P10"]
require(len(p10_matches) == 1, "prism must contain exactly one P10")
p10 = p10_matches[0] if p10_matches else {}
require(p10.get("sort") == 2014 and p10.get("period") == "2014", "P10 chronology is inconsistent")
require(p10.get("source_status") == SOURCE_STATUS, "P10 must retain the dated-secondary source classification")
require(set(p10.get("cells", {})) == {"arrecife"}, "P10 must have only an Arrecife cell")
p10_arrecife = p10.get("cells", {}).get("arrecife", {})
require(p10_arrecife.get("status") == "DIRECT", "P10 Arrecife cell must be DIRECT")
require(p10_arrecife.get("master_ids") == [MASTER_ID], "P10 Arrecife cell has an unexpected master ID")
includes(p10.get("title_en", ""), "not a procedural bridge", "P10 English title")
includes(p10.get("title_es", ""), "no un puente procesal", "P10 Spanish title")
includes(p10_arrecife.get("note_en", ""), "creates no procedural relationship", "P10 English isolation note")
includes(p10_arrecife.get("note_es", ""), "no crea relación procesal", "P10 Spanish isolation note")

master_id_locations: list[tuple[str, str]] = []
for item in prism_propositions:
    if not isinstance(item, dict):
        continue
    for lane_id, cell in item.get("cells", {}).items():
        if isinstance(cell, dict) and MASTER_ID in cell.get("master_ids", []):
            master_id_locations.append((str(item.get("id")), str(lane_id)))
require(master_id_locations == [("P10", "arrecife")], "LZ-JUD-042 appears outside the isolated P10 Arrecife cell")


# The archive control preserves full translation, source lineage and limitations.
control = read_text(CONTROL)
for marker in (
    "Complete controlled Spanish reconstruction",
    "Full controlled English translation",
    PROCEEDING_ID,
    INSTITUTION_ID,
    MASTER_ID,
    "not independent corroboration",
    "newly discovered private-candidate full name",
    "Evidentiary analysis in the context of allegations",
    "reasonable non-culpable alternative",
    "Association, title, chronology and repeated copies of the same source cannot substitute",
    "No located primary source proves joinder",
):
    includes(control, marker, relative(CONTROL))


# Every adjacent public surface must link back, and both renderers must expose the detail route.
for page in REVERSE_LINK_PAGES:
    includes(read_text(page), "dp-3205-2014-arrecife/", relative(page))

dedicated_links = {
    ES_PAGE: (
        "asuncion-aizpurua-sanchez/",
        "francisco-mario-matos-matas/",
        "actores-partes-abogados-representantes/",
        "comunidad-instrumentalizacion/",
        "concurso-36-2012-autoridad-comunidad/",
        "concurso-36-2012-puente-arrecife-mercantil/",
        "registro-maestro-procedimientos/",
        "mapa-procedimientos/",
        "hipotesis-criminal-unitaria-2011-presente/",
        CONTROL.name,
        DP_DATA.name,
        MISSING_APPEND.name,
    ),
    EN_PAGE: (
        "asuncion-aizpurua-sanchez/",
        "francisco-mario-matos-matas/",
        "actors-parties-lawyers-representatives/",
        "community-instrumentalisation/",
        "insolvency-36-2012-community-authority/",
        "insolvency-36-2012-arrecife-mercantile-bridge/",
        "master-proceedings-register/",
        "proceedings-map/",
        "unitary-criminal-hypothesis-2011-present/",
        CONTROL.name,
        DP_DATA.name,
        MISSING_APPEND.name,
    ),
}
for page, markers in dedicated_links.items():
    body = es_page if page == ES_PAGE else en_page
    for marker in markers:
        includes(body, marker, relative(page))

for renderer, renderer_markers in {
    MASTER_RENDERER: (
        "const detailRoutes",
        f"'{MASTER_ID}'",
        "en/dp-3205-2014-arrecife/",
        "es/dp-3205-2014-arrecife/",
        "detailRoutes[r.Master_ID]",
        '<a class="pd-ref"',
    ),
    MAP_RENDERER: (
        "const detailRoutes",
        f"'{MASTER_ID}'",
        "en/dp-3205-2014-arrecife/",
        "es/dp-3205-2014-arrecife/",
        "detailUrlFor",
        "detailAnchor",
        "pdim-detail-link",
    ),
}.items():
    body = read_text(renderer)
    for marker in renderer_markers:
        includes(body, marker, relative(renderer))


# The unitary route registry and every relevant sitemap must publish both routes.
route_data = read_json(ROUTES)
require(isinstance(route_data, list), "unitary route registry must be a JSON list")
route_matches = {
    path: [item for item in route_data if isinstance(item, dict) and item.get("path") == path.lstrip("/")]
    for path in (EN_ROUTE, ES_ROUTE)
}
for path, matches in route_matches.items():
    require(len(matches) == 1, f"unitary route registry must contain exactly one {path}")
    if matches:
        item = matches[0]
        require(item.get("lang") == path.split("/")[1], f"unitary route {path} has the wrong language")
        require(item.get("type") == "proceeding", f"unitary route {path} has the wrong type")
        aliases = item.get("aliases", [])
        require(MASTER_ID in aliases and PROCEEDING_ID in aliases, f"unitary route {path} lacks immutable ID aliases")
        includes(item.get("title", ""), "DP 3205/2014^", f"unitary route {path} title")

for sitemap in SITEMAPS:
    if sitemap.is_file():
        try:
            ET.parse(sitemap)
        except ET.ParseError as exc:
            require(False, f"invalid XML in {relative(sitemap)}: {exc}")
        body = read_text(sitemap)
        for route in (ES_ROUTE, EN_ROUTE):
            includes(body, PUBLIC_BASE + route, relative(sitemap))
        includes(body, 'hreflang="es"', relative(sitemap))
        includes(body, 'hreflang="en"', relative(sitemap))


# Missing-evidence and counsel/procurador gaps remain explicit and finite.
missing = read_text(MISSING)
includes(missing, "| ME-108 |", relative(MISSING))
includes(missing, "Complete primary court, authority, participant, representation and outcome file for DP 3205/2014", relative(MISSING))
includes(missing, MISSING_APPEND.name, relative(MISSING))

missing_append = read_text(MISSING_APPEND)
for number in range(1, 9):
    marker = f"ME-DP3205-{number:02d}"
    require(missing_append.count(marker) == 1, f"{relative(MISSING_APPEND)} must contain exactly one {marker}")
includes(missing_append, "no adverse inference from absence", relative(MISSING_APPEND))
includes(missing_append, "do not independently corroborate", relative(MISSING_APPEND))

counsel_data = read_json(COUNSEL_GAPS)
gaps = counsel_data.get("gaps", []) if isinstance(counsel_data, dict) else []
counsel_matches = [gap for gap in gaps if isinstance(gap, dict) and gap.get("gap_id") == "CP-GAP-008"]
require(len(counsel_matches) == 1, "counsel gap register must contain exactly one CP-GAP-008")
if counsel_matches:
    counsel_gap = counsel_matches[0]
    require(counsel_gap.get("proceeding_id") == REFERENCE, "CP-GAP-008 has the wrong proceeding")
    require(counsel_gap.get("status") == "OPEN", "CP-GAP-008 must remain OPEN")
    includes(counsel_gap.get("what_missing", ""), "No primary source presently identifies", "CP-GAP-008")


# The federated registry denominator must agree with the static bilingual presentation.
registry = read_json(REGISTRY)
require(registry.get("counts") == EXPECTED_COUNTS, "canonical registry counts are not 228/95/79/11/23/20")
parts = registry.get("parts", []) if isinstance(registry, dict) else []
part_index = {item.get("path"): item for item in parts if isinstance(item, dict)}
for path_name, expected_type in (
    (INSTITUTION_PART.name, "INSTITUTION"),
    (PROCEEDING_PART.name, "PROCEEDING"),
):
    require(path_name in part_index, f"canonical registry omits part {path_name}")
    if path_name in part_index:
        require(part_index[path_name].get("type") == expected_type, f"registry part {path_name} has wrong type")
        require(part_index[path_name].get("count") == 1, f"registry part {path_name} has wrong declared count")

actual_counts: Counter[str] = Counter()
actual_total = 0
for part in parts:
    if not isinstance(part, dict) or not part.get("path"):
        require(False, "canonical registry contains a malformed part descriptor")
        continue
    part_path = REGISTRY.parent / str(part["path"])
    part_data = read_json(part_path)
    records = part_data.get("records", []) if isinstance(part_data, dict) else []
    require(isinstance(records, list), f"registry part {part['path']} has no records list")
    if not isinstance(records, list):
        continue
    require(len(records) == part.get("count"), f"registry part {part['path']} declared count is stale")
    actual_total += len(records)
    actual_counts[str(part.get("type"))] += len(records)
require(actual_total == EXPECTED_COUNTS["total"], "federated registry actual total is not 228")
for record_type in ("PERSON", "ORGANISATION", "STRUCTURE", "INSTITUTION", "PROCEEDING"):
    require(actual_counts[record_type] == EXPECTED_COUNTS[record_type], f"federated registry actual {record_type} count is stale")

for page in (REGISTRY_EN, REGISTRY_ES):
    includes(read_text(page), 'data-static-registry-counts="228-95-79-11-23-20"', relative(page))


if failures:
    print("DP 3205/2014 PUBLICATION VALIDATION: FAIL")
    for failure in failures:
        print(f"- {failure}")
    sys.exit(1)

print("DP 3205/2014 PUBLICATION VALIDATION: PASS")

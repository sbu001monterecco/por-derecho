#!/usr/bin/env python3
"""Validate the controlled bilingual publication for 3205/2014 Arrecife."""

from __future__ import annotations

import ast
import csv
import json
import os
import re
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
PEOPLE_REGISTRY = ROOT / "assets/data/matter-identity-registry-v1.people.json"
DP_DATA = ROOT / "assets/data/dp3205-2014-arrecife-v1.json"
PERSON_INTERLINK = ROOT / "assets/data/caepr-caret-dp3205-predecessor-acosta-person-interlink-v1.json"
ACTOR_ACTION_MATRIX = ROOT / "assets/data/dp3205-contemporaneous-retrospective-actor-action-matrix-v1.json"
CONVERGENCE_GRAPH = ROOT / "assets/data/acosta-matos-functional-convergence-map-v2.json"
CONVERGENCE_STAGE2 = ROOT / "assets/data/acosta-matos-functional-convergence-map-v2.nodes-stage-2.json"
CONVERGENCE_DIRECT2 = ROOT / "assets/data/acosta-matos-functional-convergence-map-v2.edges-direct-2.json"
CONVERGENCE_FUNCTIONAL = ROOT / "assets/data/acosta-matos-functional-convergence-map-v2.edges-functional.json"
CONVERGENCE_INFERENCE = ROOT / "assets/data/acosta-matos-functional-convergence-map-v2.edges-inference-open.json"
ACOSTA_EN = ROOT / "en/acosta-matos-perimeter/index.html"
ACOSTA_ES = ROOT / "es/acosta-matos-perimetro/index.html"
MASTER = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
PRISM = ROOT / "assets/data/proceedings-case-prism-v1.json"
ROUTES = ROOT / "assets/data/unitary-route-registry-v1.json"
CONTROL = ROOT / "archive/DP3205_2014_ARRECIFE_SOURCE_TRANSLATION_AUTHORITY_ALLEGATIONS_CONTROL_30AUG2026.md"
GOVERNANCE = ROOT / ".github/governance/COMMUNITY_CLAIMED_OFFICE_CRIMINAL_FIRST_AUTHORITY_PROTOCOL_30AUG2026.md"
DECLARATION_019 = ROOT / "archive/declarations/019_GIL_DP3205_CLAIMED_AUTHORITY_GUEST_CONTEXT_CONTINUITY_20260830.md"
DECLARATION_INDEX = ROOT / "archive/declarations/INDEX.md"
MISSING = ROOT / "archive/MISSING_EVIDENCE_REGISTER.md"
MISSING_APPEND = ROOT / "archive/MISSING_EVIDENCE_REGISTER_DP3205_2014_APPEND_30AUG2026.md"
COUNSEL_GAPS = ROOT / "assets/data/counsel-procurador-gap-register-v1.json"
MANIFEST = ROOT / "publication-manifests/dp3205-2014-arrecife-caret-interlink-20260830.json"
DELETION_AUDIT = ROOT / "docs/deletion-audits/2026-08-30-dp3205-2014-arrecife-caret-interlink.md"
CRIMINAL_GRAPH = ROOT / "assets/data/criminal-first-2011-unitary-graph-v1.json"
SHADOW_GRAPH = ROOT / "assets/data/criminal-first-shadow-administration-allegation-v1.json"
MASTER_RENDERER = ROOT / "assets/master-proceedings-publication-20260830.js"
MAP_RENDERER = ROOT / "assets/proceedings-interconnectivity-map-20260830.js"
REGISTRY_EN = ROOT / "en/matter-identity-registry/index.html"
REGISTRY_ES = ROOT / "es/registro-identidad-materia/index.html"
CURRENT_UNITARY_STATE = ROOT / "ops/CURRENT_UNITARY_STATE.json"

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

PROCEEDING_ID = "PD-SP-R-0021"
INSTITUTION_ID = "PD-SP-I-0023"
MASTER_ID = "LZ-JUD-043"
REFERENCE = "3205/2014"
BASE_REVISION = "710e4bc0c85a05a693f29dc2ed64ce6f1f5e64b8"
COURT_SOURCE_ID = "PD-SP-SRC-DP3205-2014-COURT-SUMMONS-20140919"
COMPLAINT_SOURCE_ID = "PD-SP-SRC-DP3205-2014-POLICE-COMPLAINT-20140903"
SUMMARY_SOURCE_ID = "PD-SP-SRC-DP3205-2014-SUMMARY-20181120"
COUNTERACCOUNT_SOURCE_ID = "PD-SP-SRC-DP3205-2014-COUNTERACCOUNT-20141007"
HOTEL_COMMUNITY_SOURCE_ID = "PD-SP-SRC-SUNPARK-50PLUS-COMMUNITY-2013-2014"
PRE_7JUNE_SOURCE_ID = "PD-SP-SRC-COMMUNITY-SUMMARY-20180430"
NEXUS36_SOURCE_ID = "PD-SP-SRC-NEXUS36-COMPLAINT-20260625"
GIL_RETROSPECTIVE_SOURCE_ID = "PD-SP-SRC-GIL-DP3205-RETROSPECTIVE-20260830"
SOURCE_STATUS = "PRIMARY_COMPLAINT_AND_OFFICIAL_SUMMONS_LOCATED_OUTCOME_OPEN"
HISTORIC_ORGAN = "Juzgado de Instrucción nº 1 de Arrecife"
CURRENT_ORGAN = "Sección de Instrucción del Tribunal de Instancia de Arrecife — plaza nº 1"
ES_ROUTE = "/es/dp-3205-2014-arrecife/"
EN_ROUTE = "/en/dp-3205-2014-arrecife/"
PUBLIC_BASE = "https://sbu001monterecco.github.io/por-derecho"
EXPECTED_COUNTS = {
    "total": 230,
    "PERSON": 95,
    "ORGANISATION": 79,
    "STRUCTURE": 11,
    "INSTITUTION": 23,
    "PROCEEDING": 22,
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
    PEOPLE_REGISTRY,
    DP_DATA,
    PERSON_INTERLINK,
    ACTOR_ACTION_MATRIX,
    CONVERGENCE_GRAPH,
    CONVERGENCE_STAGE2,
    CONVERGENCE_DIRECT2,
    CONVERGENCE_FUNCTIONAL,
    CONVERGENCE_INFERENCE,
    ACOSTA_EN,
    ACOSTA_ES,
    MASTER,
    PRISM,
    ROUTES,
    CONTROL,
    GOVERNANCE,
    DECLARATION_019,
    DECLARATION_INDEX,
    MISSING,
    MISSING_APPEND,
    COUNSEL_GAPS,
    MANIFEST,
    DELETION_AUDIT,
    CRIMINAL_GRAPH,
    SHADOW_GRAPH,
    MASTER_RENDERER,
    MAP_RENDERER,
    REGISTRY_EN,
    REGISTRY_ES,
    CURRENT_UNITARY_STATE,
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
        "3205/2014<sup>^</sup> · Arrecife",
        "AMBER · fuentes primarias localizadas · autoridad y resultado abiertos",
        "Qué significa el caret",
        "confirma únicamente el número 3205/2014 y el órgano histórico",
        "Juicio de faltas",
        "posterior DP",
        HISTORIC_ORGAN,
        "Sección de Instrucción del Tribunal de Instancia de Arrecife · Plaza nº 1",
        "31 diciembre 2025",
        "Los documentos localizados identifican una denunciante y un perjudicado",
        "segunda persona denunciada permanece plenamente anonimizada",
        "La denuncia no le atribuye presencia ni acto físico",
        "se identificó como turista",
        "consta recibida oficialmente después del incidente",
        "no prueba presentación, recepción o actuación previa",
        "ANÁLISIS MULTIVÍA · NO ES UNA CONCLUSIÓN PENAL",
        "ALEGACIÓN PENAL DIRECTA DE GIL MARER",
        "títulos comunicados, no legitimidad",
        "correo de 7 de octubre de 2014",
        "2011 → 2014 → 7 JUNIO 2018 → DP 1901",
        "FMMM<sup>^</sup> · dentro de los cinco",
        "Aizpurúa<sup>^</sup> · estado actual separado",
        "CENSO FINITO DE PERSONAS",
        "REGISTRO CONTEMPORÁNEO ↔ RECONSTRUCCIÓN RETROSPECTIVA",
        "Esto es Gil Marer hablando",
        "criminal, no meramente civil ni inocuo",
        "17 personas + 3 funciones protegidas",
        "comunidad 50+ en actividad",
        "7 de junio de 2018, no 7 de julio de 2018",
        "No se puede concluir",
        "Alternativas razonables",
        "AISLAMIENTO FORMAL",
    ),
    EN_PAGE: (
        "3205/2014<sup>^</sup> · Arrecife",
        "AMBER · primary sources located · authority and outcome open",
        "What the caret means",
        "confirms only case number 3205/2014 and the historic court",
        "Juicio de faltas",
        "later DP",
        HISTORIC_ORGAN,
        "Sección de Instrucción del Tribunal de Instancia de Arrecife · Plaza nº 1",
        "31 December 2025",
        "The located records identify one complainant and one affected party",
        "second reported respondent remains fully anonymised",
        "complaint attributes no presence or physical act to him",
        "identified himself as a tourist",
        "officially received after the incident",
        "does not prove filing, receipt or action before 3 September",
        "MULTI-TRACK ANALYSIS · NOT A CRIMINAL CONCLUSION",
        "GIL MARER'S DIRECT CRIMINAL ALLEGATION",
        "reported titles, not legitimacy",
        "7 October 2014 email",
        "2011 → 2014 → 7 JUNE 2018 → DP 1901",
        "FMMM<sup>^</sup> · inside the five",
        "Aizpurúa<sup>^</sup> · separate present status",
        "FINITE PERSON CENSUS",
        "CONTEMPORANEOUS RECORD ↔ RETROSPECTIVE RECONSTRUCTION",
        "This is Gil Marer speaking",
        "criminal, not merely civil or innocuous",
        "17-person + 3 protected-role matrix",
        "Operating 50+ community context",
        "7 June 2018, not 7 July 2018",
        "Cannot be concluded",
        "Reasonable alternatives",
        "FORMAL ISOLATION",
    ),
}
for page, markers in page_markers.items():
    body = es_page if page == ES_PAGE else en_page
    for marker in markers:
        includes(body, marker, relative(page))
    for proposition_id in ("DP3205-P01", "DP3205-P03", "DP3205-P10", "DP3205-P16", "DP3205-P17"):
        includes(body, proposition_id, relative(page))


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
require(
    proceeding.get("procedural_state") == "PRIMARY_SUMMONS_LOCATED_HEARING_SCHEDULED_OUTCOME_NOT_LOCATED",
    "proceeding state does not preserve the scheduled-hearing/outcome-open boundary",
)
require(
    proceeding.get("identity_sources") == [COURT_SOURCE_ID, COMPLAINT_SOURCE_ID, SUMMARY_SOURCE_ID],
    "proceeding source lineage is inconsistent",
)
includes(proceeding.get("identity_boundary", ""), "caret confirms only case number 3205/2014", "proceeding identity boundary")
includes(proceeding.get("identity_boundary", ""), "summons says Juicio de faltas", "proceeding label boundary")
includes(proceeding.get("identity_boundary", ""), "later summary says DP", "proceeding label boundary")

identity = dp_data.get("identity", {}) if isinstance(dp_data, dict) else {}
require(
    dp_data.get("status") == "AMBER_PRIMARY_COMPLAINT_AND_SUMMONS_LOCATED_AUTHORITY_MERITS_OUTCOME_OPEN",
    "DP data lacks the exact primary-source AMBER state",
)
require(dp_data.get("record_revision") == 5, "DP data is not the superseding revision 5 record")
require(dp_data.get("control_id") == "PD-SP-DP3205-2014-20260830-05", "DP data has the wrong superseding control ID")
require(identity.get("registry_id") == PROCEEDING_ID, "DP data has the wrong registry ID")
require(identity.get("master_id") == MASTER_ID, "DP data has the wrong master ID")
require(identity.get("reference") == REFERENCE, "DP data has the wrong reference")
require(identity.get("organ_id") == INSTITUTION_ID, "DP data has the wrong organ ID")
require(identity.get("historic_organ") == HISTORIC_ORGAN, "DP data has the wrong historic organ")
require(identity.get("current_successor_name") == CURRENT_ORGAN, "DP data has the wrong successor nomenclature")
require(identity.get("caret_scope") == "Case number and historic organ identity only", "DP data overstates caret semantics")
require(
    identity.get("source_labels")
    == [
        "Juicio de faltas 3205/2014 — contemporaneous court summons",
        "DP 3205/2014 — later legal-adviser summary",
    ],
    "DP data does not preserve both time-controlled source labels",
)
require(identity.get("procedural_label_bridge") == "OPEN_PENDING_CERTIFIED_DOCKET", "DP label bridge is overclaimed")

expected_propositions = {
    "DP3205-P01": "OFFICIAL_PROCEDURAL_SOURCE",
    "DP3205-P02": "OFFICIAL_PROCEDURAL_SOURCE_OUTCOME_OPEN",
    "DP3205-P03": "PRIMARY_PARTICIPANT_ALLEGATION",
    "DP3205-P04": "PRIMARY_PARTICIPANT_ALLEGATION",
    "DP3205-P05": "PRIMARY_PARTICIPANT_ALLEGATION",
    "DP3205-P06": "PRIMARY_SOURCE_LIMIT",
    "DP3205-P07": "PRIMARY_SOURCE_NEGATIVE",
    "DP3205-P08": "INCIDENT_DATE_CAPACITY_UNVERIFIED",
    "DP3205-P09": "CONTEXTUAL_NOT_FORMALLY_LINKED",
    "DP3205-P10": "OUTCOME_OPEN",
    "DP3205-P11": "GIL_DIRECT_CRIMINAL_ALLEGATION_NOT_ADJUDICATED",
    "DP3205-P12": "CONTEMPORANEOUS_COUNTERALLEGATION_DOCUMENTED_TRUTH_OPEN",
    "DP3205-P13": "PRIVACY_MINIMISED_CAPACITY_CLARIFICATION",
    "DP3205-P14": "ATTRIBUTED_CONTINUITY_HYPOTHESIS_WITH_LIMIT",
    "DP3205-P15": "DP1901_PERIMETER_CONTROL",
    "DP3205-P16": "GIL_RETROSPECTIVE_CRIMINAL_ATTRIBUTION_NOT_ADJUDICATED",
    "DP3205-P17": "FINITE_ACTOR_ACTION_MULTI_TRACK_CONTROL",
}
propositions = dp_data.get("reported_propositions", []) if isinstance(dp_data, dict) else []
observed_propositions = {item.get("id"): item.get("state") for item in propositions if isinstance(item, dict)}
require(observed_propositions == expected_propositions, "DP3205 P01-P17 IDs or source states are incomplete")
proposition_text = {
    item.get("id"): item.get("proposition", "")
    for item in propositions
    if isinstance(item, dict)
}
includes(
    proposition_text.get("DP3205-P06", ""),
    "complainant's husband did not witness the alleged assault itself",
    "DP3205-P06 witness limit",
)
includes(
    proposition_text.get("DP3205-P06", ""),
    "police arrived afterwards",
    "DP3205-P06 police timing",
)
includes(
    proposition_text.get("DP3205-P06", ""),
    "does not establish that nobody else witnessed it",
    "DP3205-P06 non-overgeneralisation boundary",
)


# The protected respondent remains anonymised and the duplicate lineage stays singular.
participants = dp_data.get("participants", []) if isinstance(dp_data, dict) else []
private_candidates = [item for item in participants if isinstance(item, dict) and item.get("private_candidate") is True]
require(len(private_candidates) == 1, "DP data must contain exactly one anonymised private candidate")
if private_candidates:
    candidate = private_candidates[0]
    expected_private_candidate = {
        "public_label": "Second reported respondent",
        "private_candidate": True,
        "capacity_reported": "court-cited respondent and alleged physical actor",
        "bridge_state": "ROLE_ONLY_IDENTITY_AND_INCIDENT_DATE_CAPACITY_WITHHELD",
    }
    require(candidate == expected_private_candidate, "private candidate projection is not the exact anonymous schema")

participant_index = {
    item.get("candidate_registry_id", item.get("registry_id")): item
    for item in participants
    if isinstance(item, dict) and (item.get("candidate_registry_id") or item.get("registry_id"))
}
require(
    participant_index.get("PD-SP-P-0004", {}).get("capacity_reported")
    == "complainant and claimed Community president",
    "the reported president must be the complainant, not an undifferentiated complainant pair",
)
require(
    participant_index.get("PD-SP-P-0009", {}).get("capacity_reported")
    == "affected party and claimed Community administrator",
    "the reported administrator must be the affected party, not a second formal complainant",
)
require(
    participant_index.get("PD-SP-P-0001", {}).get("bridge_state")
    == "CANONICAL_NAME_MATCH_NO_DIRECT_PHYSICAL_ACT_ALLEGED_IN_COMPLAINT",
    "Gil act allocation is not controlled",
)
require(
    participant_index.get("PD-SP-P-0004", {}).get("bridge_state")
    == "CARET_CONFIRMED_IDENTITY_ONLY_REPORTED_OFFICE_AND_AUTHORITY_OPEN",
    "Aizpurúa identity caret is not separated from claimed office/authority",
)
require(
    participant_index.get("PD-SP-P-0009", {}).get("bridge_state")
    == "CARET_CONFIRMED_CANONICAL_MATAS_IDENTITY_ONLY_REPORTED_OFFICE_AND_AUTHORITY_OPEN",
    "FMMM canonical identity caret is not separated from claimed office/authority",
)

# The finite person census and central registry must agree exactly on the resolved pair,
# the present five-person complaint perimeter and protected role-only references.
people_data = read_json(PEOPLE_REGISTRY)
people_records = people_data.get("records", []) if isinstance(people_data, dict) else []
people_index = {item.get("id"): item for item in people_records if isinstance(item, dict)}
for person_id in ("PD-SP-P-0004", "PD-SP-P-0007", "PD-SP-P-0008", "PD-SP-P-0009"):
    record = people_index.get(person_id, {})
    require(record.get("identity_resolution") == "CARET_CONFIRMED", f"{person_id} is not CARET_CONFIRMED in the central people registry")
    require(bool(record.get("identity_sources")), f"{person_id} lacks identity sources")
    require(bool(record.get("identity_boundary")), f"{person_id} lacks an identity boundary")
require("Asunción Asperua" in people_index.get("PD-SP-P-0004", {}).get("aliases", []), "Asperua transcription variant is not controlled")
includes(people_index.get("PD-SP-P-0004", {}).get("identity_boundary", ""), "caret does not establish lawful office", "Aizpurúa caret boundary")
includes(people_index.get("PD-SP-P-0009", {}).get("identity_boundary", ""), "isolated 1-Mar-2024 BORME source-literal", "FMMM MATA boundary")

interlink = read_json(PERSON_INTERLINK)
interlink_people = interlink.get("people", []) if isinstance(interlink, dict) else []
require(len(interlink_people) == 17, "person interlink census must contain exactly 17 public people")
interlink_ids = [item.get("registry_id") for item in interlink_people if isinstance(item, dict)]
require(len(set(interlink_ids)) == 17, "person interlink census contains duplicate person IDs")
exact_five = ["PD-SP-P-0007", "PD-SP-P-0008", "PD-SP-P-0009", "PD-SP-P-0011", "PD-SP-P-0012"]
require(interlink.get("exact_dp1901_five") == exact_five, "person interlink census does not preserve the exact DP1901 five")
require(
    [item.get("registry_id") for item in interlink_people if isinstance(item, dict) and item.get("dp1901_five") is True] == exact_five,
    "person records do not mark exactly the controlled five",
)
protected_roles = interlink.get("protected_role_only", [])
require(len(protected_roles) == 3, "person interlink census must contain exactly three protected role-only records")
require(all(item.get("caret_state") == "PROHIBITED_NO_PUBLIC_IDENTITY" for item in protected_roles if isinstance(item, dict)), "a protected role is caret-eligible")
links = interlink.get("reciprocal_interlinks", [])
require(any(item.get("from") == "PD-SP-P-0004" and item.get("to") == "PD-SP-P-0009" for item in links if isinstance(item, dict)), "Aizpurúa→FMMM reciprocal census link is missing")

# Every finite-scope person and protected role must resolve to an actor-specific
# action/omission record across the two non-merged temporal ledgers.
actor_matrix = read_json(ACTOR_ACTION_MATRIX)
require(actor_matrix.get("control_id") == "PD-SP-DP3205-ACTOR-ACTION-001", "actor/action matrix has the wrong control ID")
includes(actor_matrix.get("speaker_attribution", ""), "Gil Marer expressly adopts", "actor/action speaker attribution")
includes(actor_matrix.get("criminal_attribution_rule", ""), "criminal, not merely civil or innocuous", "actor/action criminal attribution")
includes(actor_matrix.get("non_transfer_rule", ""), "transfers conduct, knowledge, intent, guilt or liability", "actor/action non-transfer rule")
ledgers = actor_matrix.get("temporal_ledgers", {})
require(set(ledgers) == {"CONTEMPORANEOUS", "RETROSPECTIVE", "rule"}, "actor/action temporal ledgers are incomplete")
includes(ledgers.get("rule", ""), "never silently merged", "actor/action two-ledger rule")
expected_tracks = {
    "COMMUNITY_AUTHORITY", "HOTEL_TRADE", "ACCESS_POSSESSION", "COMPLAINT_PROCEDURE",
    "INSOLVENCY", "PROPERTY_FINANCE", "CRIMINAL_PROSECUTORIAL",
    "REGULATORY_PUBLIC_SUPPORT", "WITNESS_CUSTODY",
}
require(set(actor_matrix.get("track_definitions", {})) == expected_tracks, "actor/action track denominator is incomplete")
matrix_people = actor_matrix.get("people", [])
require(len(matrix_people) == 17, "actor/action matrix must contain exactly 17 public people")
matrix_ids = [item.get("registry_id") for item in matrix_people if isinstance(item, dict)]
require(matrix_ids == interlink_ids, "actor/action people must reconcile one-to-one and in census order")
allowed_evidence_states = set(actor_matrix.get("evidence_states", []))
allowed_temporal_layers = {"CONTEMPORANEOUS", "RETROSPECTIVE", "CONTEMPORANEOUS_AND_RETROSPECTIVE"}
for person in matrix_people:
    if not isinstance(person, dict):
        require(False, "actor/action matrix contains a malformed person record")
        continue
    require(bool(person.get("classification")), f"{person.get('registry_id')} lacks classification")
    tracks = person.get("tracks", [])
    require(bool(tracks) and set(tracks).issubset(expected_tracks), f"{person.get('registry_id')} has invalid tracks")
    actions = person.get("actions", [])
    require(bool(actions), f"{person.get('registry_id')} lacks an action or no-located-act statement")
    for action in actions:
        require(action.get("temporal_layer") in allowed_temporal_layers, f"{person.get('registry_id')} action has invalid temporal layer")
        evidence_parts = set(str(action.get("evidence_status", "")).split("_AND_"))
        require(bool(evidence_parts) and evidence_parts.issubset(allowed_evidence_states), f"{person.get('registry_id')} action has invalid evidence state")
        for field in ("date", "capacity", "action_or_omission", "limit_open_proof"):
            require(bool(action.get(field)), f"{person.get('registry_id')} action lacks {field}")
        require(bool(action.get("source_refs")), f"{person.get('registry_id')} action lacks source references")

matrix_roles = actor_matrix.get("protected_role_actions", [])
require(len(matrix_roles) == 3, "actor/action matrix must contain exactly three protected role actions")
require(
    [item.get("role_id") for item in matrix_roles if isinstance(item, dict)]
    == [item.get("role_id") for item in protected_roles if isinstance(item, dict)],
    "protected role actions do not reconcile one-to-one with the finite census",
)
for role in matrix_roles:
    require(bool(role.get("action_or_omission")) and bool(role.get("limit_open_proof")), f"{role.get('role_id')} lacks controlled action/limit")
    require(bool(role.get("source_refs")), f"{role.get('role_id')} lacks source references")
coverage = actor_matrix.get("coverage", {})
require(coverage == {"public_people":17,"protected_role_only":3,"action_control":"EVERY_RECORD_HAS_ACTION_OR_EXPRESS_NO_LOCATED_ACT","verdict":"COMPLETE_FOR_STATED_FINITE_SCOPE"}, "actor/action coverage declaration is inconsistent")

sources = dp_data.get("sources", []) if isinstance(dp_data, dict) else []
expected_sources = {
    COURT_SOURCE_ID: "CONTEMPORANEOUS_OFFICIAL_PROCEDURAL_NOTICE_LOCATED_COPY",
    COMPLAINT_SOURCE_ID: "CONTEMPORANEOUS_POLICE_RECORDED_PARTICIPANT_ALLEGATION_LOCATED_COPY",
    SUMMARY_SOURCE_ID: "DATED_SECONDARY_LEGAL_ADVISER_STATUS_SUMMARY",
    COUNTERACCOUNT_SOURCE_ID: "CONTEMPORANEOUS_PARTY_EMAIL_TO_LEGAL_ADVISERS",
    HOTEL_COMMUNITY_SOURCE_ID: "CONTEMPORANEOUS_HOTEL_COMMUNITY_AND_PROMOTIONAL_COMMUNICATIONS",
    PRE_7JUNE_SOURCE_ID: "CONTEMPORANEOUS_PRE_7JUNE_PARTY_SUMMARY",
    NEXUS36_SOURCE_ID: "FILED_PARTY_CRIMINAL_COMPLAINT_ARCHITECTURE",
    GIL_RETROSPECTIVE_SOURCE_ID: "GIL_CURRENT_PROPOSITION_SPECIFIC_ADOPTION",
}
observed_sources = {
    item.get("source_id"): item.get("source_class")
    for item in sources
    if isinstance(item, dict)
}
require(observed_sources == expected_sources, "DP data source hierarchy is incomplete or misclassified")
includes(dp_data.get("privacy", ""), "No raw message, source filename or locator", "DP privacy boundary")
includes(dp_data.get("privacy", ""), "exact unit or room number", "DP privacy boundary")
includes(dp_data.get("privacy", ""), "private respondent identity or name variant", "DP privacy boundary")

# Validate the minimized public projection without embedding, hashing or reconstructing
# the withheld identity in this public repository. Exact-name screening belongs in the
# access-controlled identity system; this gate enforces the public side of that boundary.
privacy_surfaces = (DP_DATA, ACTOR_ACTION_MATRIX, CONTROL, GOVERNANCE, DECLARATION_019, ES_PAGE, EN_PAGE)
allowed_public_person_ids = {
    "PD-SP-P-0001", "PD-SP-P-0002", "PD-SP-P-0003", "PD-SP-P-0004", "PD-SP-P-0005",
    "PD-SP-P-0006", "PD-SP-P-0007", "PD-SP-P-0008", "PD-SP-P-0009", "PD-SP-P-0010",
    "PD-SP-P-0011", "PD-SP-P-0012", "PD-SP-P-0013", "PD-SP-P-0088", "PD-SP-P-0093",
    "PD-SP-P-0094", "PD-SP-P-0095",
}
person_id_pattern = re.compile(r"\bPD-SP-P-\d{4}\b")
sensitive_identity_fields = (
    '"private_name"',
    '"private_full_name"',
    '"source_name"',
    '"respondent_name"',
    '"aliases"',
    '"initials"',
)
for path in privacy_surfaces:
    body = read_text(path)
    observed_person_ids = set(person_id_pattern.findall(body))
    require(
        observed_person_ids.issubset(allowed_public_person_ids),
        f"{relative(path)} exposes an unapproved person identifier in the DP3205 public projection",
    )
    lowered = body.casefold()
    for field in sensitive_identity_fields:
        require(field.casefold() not in lowered, f"{relative(path)} exposes a private identity field: {field}")


def collect_json_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key).casefold())
            keys.update(collect_json_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(collect_json_keys(child))
    return keys


forbidden_dp_keys = {
    "nig",
    "police_reference",
    "raw_filename",
    "raw_file_id",
    "source_locator",
    "address",
    "telephone",
    "phone",
    "signature",
    "passport",
    "nie",
    "dni",
    "unit_number",
    "room_number",
    "booking_reference",
    "guest_ledger",
    "guest_name",
}
require(
    not (collect_json_keys(dp_data) & forbidden_dp_keys),
    "DP data exposes a prohibited raw identifier, contact, location or guest-data field",
)

superseding_surfaces = (
    DP_DATA,
    CONTROL,
    ES_PAGE,
    EN_PAGE,
    MISSING_APPEND,
    MASTER,
    PRISM,
    DELETION_AUDIT,
    CRIMINAL_GRAPH,
    SHADOW_GRAPH,
)
stale_phrases = (
    "reports two complainants under Community titles",
    "reported Community-capacity complaint by two",
    "secondary identification source only",
    "secondary-summary-only publication",
    "original complaint remains unlocated",
    "denuncia original sigue no localizada",
)
for path in superseding_surfaces:
    lowered = read_text(path).casefold()
    for phrase in stale_phrases:
        require(phrase.casefold() not in lowered, f"{relative(path)} retains stale DP3205 wording: {phrase}")


# The repository-wide claimed-office rule and Declaration 019 must remain explicit,
# source-graded, privacy-minimised and aligned with the exact DP 1901 perimeter.
governance_body = read_text(GOVERNANCE)
declaration_body = read_text(DECLARATION_019)
declaration_index_body = read_text(DECLARATION_INDEX)
for marker in (
    "The title is evidence of a claim, not proof of lawful authority",
    "criminal hijacking or capture",
    "7 October 2014 email is contemporaneous evidence",
    "not 7 July 2018",
    "José Daniel Acosta Matos",
    "Laura Patricia Acosta Matos",
    "Francisco Mario Matos Matas",
    "Antonio Cogolludo Rojas",
    "Shaila María Cogolludo Ramos",
    "silently added as a sixth accused/denounced person",
):
    includes(governance_body, marker, relative(GOVERNANCE))
for marker in (
    "no legitimate office or work mandate",
    "7 October 2014 email",
    "operating hotel/community setting",
    "indirect identity bridge",
    "7 June 2018",
    "is one of the five private actors expressly named",
    "is not one of those five",
    "material historical witness and potential future additional party",
    "Gail",
    "transcription error",
):
    includes(declaration_body, marker, relative(DECLARATION_019))
includes(declaration_index_body, "| 019 | 2026-08-30 | Gil Marer |", relative(DECLARATION_INDEX))
includes(declaration_index_body, "siguiente declaración disponible es **020**", relative(DECLARATION_INDEX))

validator_body = read_text(Path(__file__))
try:
    validator_ast = ast.parse(validator_body)
except SyntaxError as exc:
    require(False, f"validator source cannot be parsed for privacy review: {exc}")
else:
    require(
        not any(isinstance(node, ast.Constant) and isinstance(node.value, bytes) for node in ast.walk(validator_ast)),
        "validator must not embed byte fragments that could reconstruct withheld identity data",
    )

# A private pre-publication runner may provide the exact denylist at runtime. The
# values are never committed, hashed or printed; only the affected repository path
# is reported. Public CI still enforces the anonymous schema and identifier allowlist.
private_denylist_json = os.environ.get("DP3205_PRIVATE_DENYLIST_JSON", "")
if private_denylist_json:
    try:
        private_denylist = json.loads(private_denylist_json)
    except json.JSONDecodeError as exc:
        require(False, f"private DP3205 denylist is invalid JSON: {exc}")
        private_denylist = []
    require(
        isinstance(private_denylist, list)
        and private_denylist
        and all(isinstance(item, str) and item.strip() for item in private_denylist),
        "private DP3205 denylist must be a non-empty JSON string array",
    )
    private_terms = [item.casefold().encode("utf-8") for item in private_denylist if isinstance(item, str) and item.strip()]
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
            require(False, f"could not run private DP3205 denylist scan on {relative(path)}: {exc}")
            continue
        if any(term in payload for term in private_terms):
            require(False, f"private DP3205 denylist match in tracked publication surface: {relative(path)}")


# Allegation analysis must retain non-inference, an innocent alternative and formal isolation.
context = dp_data.get("allegations_context", {}) if isinstance(dp_data, dict) else {}
includes(context.get("safe_use", ""), "Authority, access, possession, key-control", "DP allegations context")
includes(context.get("safe_use", ""), "wider attributed Community-instrumentalisation theory", "DP allegations context")
not_established = context.get("does_not_establish", [])
require(isinstance(not_established, list) and len(not_established) >= 9, "DP allegations context lacks a finite non-inference list")
for marker in (
    "valid incident-date appointment",
    "truth, falsity or legal characterization",
    "presence, instruction, agency or a physical act by Gil Marer",
    "knowledge, intent",
    "hearing occurrence, procedural outcome or finality",
):
    includes("\n".join(str(item) for item in not_established), marker, "DP non-inference list")
alternatives = context.get("reasonable_alternatives", [])
require(isinstance(alternatives, list) and len(alternatives) >= 5, "DP reasonable-alternatives list is incomplete")
for marker in ("genuine Community", "personal or family-property", "unauthorized or excessive entry", "mutual or defensive", "independent intervention"):
    includes("\n".join(str(item) for item in alternatives), marker, "DP reasonable alternatives")

attendance_reasons = dp_data.get("attendance_reasons", {}) if isinstance(dp_data, dict) else {}
includes(attendance_reasons.get("contemporaneous_claim", ""), "unspecified work", "DP attendance reason")
includes(attendance_reasons.get("later_candidate_account", ""), "not formally linked", "DP later attendance account")
includes(attendance_reasons.get("regulatory_context", ""), "officially received after the incident", "DP regulatory chronology")
includes(attendance_reasons.get("regulatory_context", ""), "does not prove pre-incident filing", "DP regulatory chronology")

guest_status = dp_data.get("guest_status", {}) if isinstance(dp_data, dict) else {}
includes(guest_status.get("reported", ""), "identified himself as a tourist", "DP reported tourist status")
includes(guest_status.get("not_proved", ""), "booking", "DP incident-date capacity boundary")
includes(guest_status.get("non_inference", ""), "would not itself prove employment", "DP guest-status non-inference")
includes(guest_status.get("non_inference", ""), "agency", "DP guest-status non-inference")

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
require(len(master_matches) == 1, "Master Register must contain exactly one LZ-JUD-043 row")
master_row = master_matches[0] if master_matches else {}
for field, expected in {
    "Reference": REFERENCE,
    "Origin_Organ": HISTORIC_ORGAN,
    "Current_Custodian": CURRENT_ORGAN,
    "Primary_Source_Anchor": f"{COURT_SOURCE_ID}; {COMPLAINT_SOURCE_ID}; {SUMMARY_SOURCE_ID}",
    "Source_Status": SOURCE_STATUS,
    "Is_Proceeding": "TRUE",
    "Stream": "Criminal",
}.items():
    require(master_row.get(field) == expected, f"Master Register {field} is inconsistent for {MASTER_ID}")
require(
    master_row.get("Secondary_Reference") == "Juicio de faltas 3205/2014; later DP 3205/2014",
    "Master Register does not preserve both source labels",
)
for field in ("Parent_Master_ID", "Linked_Proceedings", "Appeal_or_Review"):
    require(not master_row.get(field, "").strip(), f"Master Register incorrectly creates a formal link in {field}")
includes(master_row.get("Notes", ""), "Keep distinct", "Master Register isolation note")
includes(master_row.get("Notes", ""), "absent primary proof", "Master Register isolation note")


# P19 is direct only in the Arrecife lane; its other materialised coordinates
# make formal isolation explicit without creating another procedural bridge.
prism = read_json(PRISM)
lanes = prism.get("lanes", []) if isinstance(prism, dict) else []
arrecife_lanes = [lane for lane in lanes if isinstance(lane, dict) and lane.get("id") == "arrecife"]
require(len(arrecife_lanes) == 1, "prism must contain exactly one Arrecife lane")
if arrecife_lanes:
    require(MASTER_ID in arrecife_lanes[0].get("master_ids", []), "Arrecife lane lacks LZ-JUD-043")
lane_locations = [
    str(lane.get("id"))
    for lane in lanes
    if isinstance(lane, dict) and MASTER_ID in lane.get("master_ids", [])
]
require(lane_locations == ["arrecife"], "LZ-JUD-043 appears in a prism lane other than Arrecife")

prism_propositions = prism.get("propositions", []) if isinstance(prism, dict) else []
p19_matches = [item for item in prism_propositions if isinstance(item, dict) and item.get("id") == "P19"]
require(len(p19_matches) == 1, "prism must contain exactly one P19")
p19 = p19_matches[0] if p19_matches else {}
require(
    p19.get("sort") == 2014 and p19.get("period_en") == "2014" and p19.get("period_es") == "2014",
    "P19 chronology is inconsistent",
)
require(p19.get("source_status") == SOURCE_STATUS, "P19 must retain the primary complaint/summons outcome-open classification")
p19_cells = p19.get("cells", {}) if isinstance(p19, dict) else {}
expected_lane_ids = {str(lane.get("id")) for lane in lanes if isinstance(lane, dict)}
require(set(p19_cells) == expected_lane_ids, "P19 must materialise every Case Prism lane")
p19_arrecife = p19_cells.get("arrecife", {})
require(p19_arrecife.get("status") == "DIRECT", "P19 Arrecife cell must be DIRECT")
require(p19_arrecife.get("treatment") == "DIRECTLY_IN_FILE", "P19 Arrecife treatment must be direct")
require(p19_arrecife.get("master_ids") == [MASTER_ID], "P19 Arrecife cell has an unexpected master ID")
require(
    p19_arrecife.get("representation_gap_ids") == ["CP-GAP-008"],
    "P19 Arrecife cell must preserve the proceeding-specific representation gap",
)
non_outside_p19 = [
    (lane_id, cell.get("status"))
    for lane_id, cell in p19_cells.items()
    if isinstance(cell, dict) and cell.get("status") != "OUTSIDE"
]
require(non_outside_p19 == [("arrecife", "DIRECT")], "P19 must be non-OUTSIDE only in Arrecife")
for lane_id, cell in p19_cells.items():
    if lane_id == "arrecife" or not isinstance(cell, dict):
        continue
    require(cell.get("treatment") == "OUTSIDE_PROCEDURAL_SCOPE", f"P19/{lane_id} is not formally isolated")
    require(cell.get("master_ids") == [], f"P19/{lane_id} creates an unexpected proceeding link")
includes(p19.get("title_en", ""), "not a procedural bridge", "P19 English title")
includes(p19.get("title_es", ""), "no un puente procesal", "P19 Spanish title")
includes(p19_arrecife.get("note_en", ""), "creates no procedural relationship", "P19 English isolation note")
includes(p19_arrecife.get("note_es", ""), "no crea relación procesal", "P19 Spanish isolation note")

master_id_locations: list[tuple[str, str]] = []
for item in prism_propositions:
    if not isinstance(item, dict):
        continue
    for lane_id, cell in item.get("cells", {}).items():
        if isinstance(cell, dict) and MASTER_ID in cell.get("master_ids", []):
            master_id_locations.append((str(item.get("id")), str(lane_id)))
require(master_id_locations == [("P19", "arrecife")], "LZ-JUD-043 appears outside the isolated P19 Arrecife cell")


# The archive control preserves full translation, source lineage and limitations.
control = read_text(CONTROL)
for marker in (
    "Complete controlled Spanish reconstruction",
    "Full controlled English translation",
    PROCEEDING_ID,
    INSTITUTION_ID,
    MASTER_ID,
    "not independent corroboration",
    "a complainant described in the sources as Community president",
    "an affected party described as administrator",
    "fully anonymised second respondent",
    "la sujetó fuertemente del brazo y posiblemente le dio un codazo en la espalda",
    "luxación del pulgar izquierdo y después un empujón",
    "held her tightly by the arm and possibly elbowed her in the back",
    "dislocation of the left thumb and was then pushed",
    "había recibido una llamada desde un número omitido",
    "had later received a call from an omitted number",
    "does not identify Gil Marer as the caller or recipient",
    "no presence at the incident, instruction, agency relationship or physical contact to Gil",
    "Meaning of the reported tourist and physical altercation",
    "officially received after 3 September 2014",
    "cannot be used to prove that it was filed, received or acted upon before the incident",
    "Multi-track control",
    "No located source proves joinder",
    "Bounded authorised searches across the accessible connected Gmail, Drive and repository sources",
    "Gil Marer's direct criminal allegation and the contemporaneous counter-record",
    "no legitimate Community office or work mandate",
    "7 October 2014 email",
    "active-retirement/community offer",
    "7 June 2018 continuity and DP 1901 perimeter",
    "five private actors",
    "material historical witness and possible future additional party",
):
    includes(control, marker, relative(CONTROL))
for forbidden in ("llamaron a Gil Marer", "they later called Gil Marer", "complete authorised email/file/repository scan"):
    require(forbidden.casefold() not in control.casefold(), f"{relative(CONTROL)} contains superseded wording: {forbidden}")


# Every adjacent public surface must link back, and both renderers must expose the detail route.
for page in REVERSE_LINK_PAGES:
    includes(read_text(page), "dp-3205-2014-arrecife/", relative(page))
for index_page in (ROOT / "en/site-index/index.html", ROOT / "es/indice-web/index.html"):
    includes(read_text(index_page), "3205/2014^ · Arrecife", relative(index_page))

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
        "dp-1901-2026/",
        DECLARATION_019.name,
        GOVERNANCE.name,
        ACTOR_ACTION_MATRIX.name,
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
        "dp-1901-2026/",
        DECLARATION_019.name,
        GOVERNANCE.name,
        ACTOR_ACTION_MATRIX.name,
    ),
}
for page, markers in dedicated_links.items():
    body = es_page if page == ES_PAGE else en_page
    for marker in markers:
        includes(body, marker, relative(page))

for page in (ES_PAGE, EN_PAGE, ACOSTA_ES, ACOSTA_EN):
    body = read_text(page)
    for marker in (
        'data-caepr-id="PD-SP-P-0004"',
        'data-caepr-id="PD-SP-P-0009"',
        PERSON_INTERLINK.name,
        CONVERGENCE_GRAPH.name,
        ACTOR_ACTION_MATRIX.name,
    ):
        includes(body, marker, relative(page))

for page in (
    ROOT / "es/asuncion-aizpurua-sanchez/index.html",
    ROOT / "en/asuncion-aizpurua-sanchez/index.html",
):
    body = read_text(page)
    includes(body, 'data-caepr-id="PD-SP-P-0004"', relative(page))
    includes(body, 'data-caepr-id="PD-SP-P-0009"', relative(page))
    includes(body, "francisco-mario-matos-matas/", relative(page))
    includes(body, "dp-3205-2014-arrecife/", relative(page))
for page in (
    ROOT / "es/francisco-mario-matos-matas/index.html",
    ROOT / "en/francisco-mario-matos-matas/index.html",
):
    body = read_text(page)
    includes(body, 'data-caepr-id="PD-SP-P-0009"', relative(page))
    includes(body, 'data-caepr-id="PD-SP-P-0004"', relative(page))
    includes(body, "asuncion-aizpurua-sanchez/", relative(page))
    includes(body, "dp-3205-2014-arrecife/", relative(page))

# The convergence graph must expose DP3205 as a bounded mid-chain node and retain
# direct, functional and attributed-inference grades without transferring mens rea.
graph = read_json(CONVERGENCE_GRAPH)
require(graph.get("control_date") == "2026-08-30", "convergence graph control date is stale")
require(graph.get("parallel_spines", {}).get("claimed_office_incident") == ["aizpurua", "fmmm", "dp3205", "community", "cam"], "claimed-office incident spine is incomplete")
stage2 = read_json(CONVERGENCE_STAGE2).get("nodes", [])
require(any(item.get("key") == "dp3205" and item.get("registry_id") == PROCEEDING_ID for item in stage2 if isinstance(item, dict)), "convergence graph lacks the DP3205 proceeding node")
direct2 = read_json(CONVERGENCE_DIRECT2).get("edges", [])
functional = read_json(CONVERGENCE_FUNCTIONAL).get("edges", [])
inference = read_json(CONVERGENCE_INFERENCE).get("edges", [])
require(any(item.get("from") == "aizpurua" and item.get("to") == "dp3205" for item in direct2 if isinstance(item, dict)), "graph lacks direct Aizpurúa→DP3205 edge")
require(any(item.get("from") == "fmmm" and item.get("to") == "dp3205" for item in direct2 if isinstance(item, dict)), "graph lacks direct FMMM→DP3205 edge")
require(any(item.get("from") == "dp3205" and item.get("to") == "community" for item in functional if isinstance(item, dict)), "graph lacks bounded DP3205→Community functional edge")
require(any(item.get("from") == "dp3205" and item.get("to") == "cam" and item.get("grade") == "ATTRIBUTED_INFERENCE" for item in inference if isinstance(item, dict)), "graph lacks attributed DP3205→CAM inference edge")

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
        includes(item.get("title", ""), "3205/2014^ · Arrecife", f"unitary route {path} title")
        require(not item.get("title", "").startswith("DP "), f"unitary route {path} does not use the neutral title")

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
includes(missing, "| ME-112 |", relative(MISSING))
includes(missing, "Complete primary court, authority, participant, representation and outcome file for 3205/2014", relative(MISSING))
includes(missing, MISSING_APPEND.name, relative(MISSING))

missing_append = read_text(MISSING_APPEND)
for number in range(1, 18):
    marker = f"ME-DP3205-{number:02d}"
    require(missing_append.count(marker) == 1, f"{relative(MISSING_APPEND)} must contain exactly one {marker}")
includes(missing_append, "no adverse inference from absence", relative(MISSING_APPEND))
includes(missing_append, "do not independently corroborate", relative(MISSING_APPEND))
includes(
    missing_append,
    "complainant's husband did not witness the alleged assault itself",
    relative(MISSING_APPEND),
)
includes(
    missing_append,
    "does not establish that nobody else witnessed it",
    relative(MISSING_APPEND),
)
for marker in (
    "Exact 2011–2014 office, term and act-specific work mandate",
    "Native contemporaneous counter-record",
    "Hotel 50+ community context",
    "30-Apr-2018 pre-takeover authority/debt/vote narrative",
    "NEXUS 36 / DP 1901 present procedural and actor-status record",
):
    includes(missing_append, marker, relative(MISSING_APPEND))

counsel_data = read_json(COUNSEL_GAPS)
gaps = counsel_data.get("gaps", []) if isinstance(counsel_data, dict) else []
counsel_matches = [gap for gap in gaps if isinstance(gap, dict) and gap.get("gap_id") == "CP-GAP-008"]
require(len(counsel_matches) == 1, "counsel gap register must contain exactly one CP-GAP-008")
if counsel_matches:
    counsel_gap = counsel_matches[0]
    require(counsel_gap.get("proceeding_id") == REFERENCE, "CP-GAP-008 has the wrong proceeding")
    require(counsel_gap.get("status") == "OPEN", "CP-GAP-008 must remain OPEN")
    includes(counsel_gap.get("what_missing", ""), "A primary complaint and court summons are located", "CP-GAP-008")
    includes(counsel_gap.get("what_missing", ""), "do not close the lawyers, procuradores", "CP-GAP-008")


# The superseding manifest must record the user's express authority and exact scope.
manifest = read_json(MANIFEST)
require(manifest.get("publication_id") == "PD-SP-DP3205-2014-20260830-05", "manifest has the wrong superseding publication ID")
require(manifest.get("supersedes") == "PD-SP-DP3205-2014-20260830-04", "manifest does not identify the superseded control")
require(manifest.get("base_revision") == BASE_REVISION, "manifest base revision is stale or incorrect")
require(
    manifest.get("current_state") == "PREPARED_PENDING_MERGE"
    and manifest.get("state") == "PREPARED_PENDING_MERGE",
    "manifest must record the authorised publication state",
)
require(
    manifest.get("publication_gate") == "EXPRESS_USER_PUBLICATION_AUTHORITY_30AUG2026",
    "manifest does not record the express publication gate",
)
require(manifest.get("local_preparation_complete") is True, "manifest does not record completed local preparation")
require(manifest.get("external_mutation_authorized") is True, "manifest does not authorise the normal publication chain")
includes(manifest.get("attribution_confirmation", ""), "transcription error for Gil Marer", "manifest attribution confirmation")
for marker in (
    "continuity audit",
    "governance and automation updates",
    "commit, push, pull-request, merge and Pages",
    "does not extend to email",
):
    includes(manifest.get("publication_authority", ""), marker, "manifest publication authority")
manifest_files = manifest.get("expected_source_files", [])
require(isinstance(manifest_files, list), "manifest expected_source_files must be an array")
if isinstance(manifest_files, list):
    require(len(manifest_files) == 115, "manifest must inventory all 115 changed publication paths")
    require(len(set(manifest_files)) == len(manifest_files), "manifest source inventory contains duplicates")
    for manifest_path in manifest_files:
        require(isinstance(manifest_path, str) and (ROOT / manifest_path).is_file(), f"manifest source file is missing: {manifest_path}")
    for required_path in (
        str(CONTROL.relative_to(ROOT)),
        str(DP_DATA.relative_to(ROOT)),
        str(MISSING_APPEND.relative_to(ROOT)),
        str(CRIMINAL_GRAPH.relative_to(ROOT)),
        str(SHADOW_GRAPH.relative_to(ROOT)),
        str(GOVERNANCE.relative_to(ROOT)),
        str(DECLARATION_019.relative_to(ROOT)),
        str(DECLARATION_INDEX.relative_to(ROOT)),
        str(ROUTES.relative_to(ROOT)),
        str(Path(__file__).resolve().relative_to(ROOT)),
        str(PERSON_INTERLINK.relative_to(ROOT)),
        str(CONVERGENCE_GRAPH.relative_to(ROOT)),
        str(PEOPLE_REGISTRY.relative_to(ROOT)),
        str(ACTOR_ACTION_MATRIX.relative_to(ROOT)),
    ):
        require(required_path in manifest_files, f"manifest omits required superseding source: {required_path}")
verification = manifest.get("verification", {})
require(verification.get("local_validation") is True, "manifest does not record successful local validation")
for remote_state in ("ci_green", "merged", "main_readback", "pages_deployed", "public_readback"):
    require(verification.get(remote_state) is False, f"manifest overclaims remote state: {remote_state}")
scope_changes = manifest.get("material_scope_changes", [])
for marker in (
    "primary incident narrative",
    "one complainant and one affected party",
    "scheduled oral hearing",
    "no direct physical act is attributed to Gil Marer",
    "reported tourist self-identification",
    "source-reported-title rule",
    "criminal-hijacking and holding-out allegation",
    "7 October 2014 contemporaneous counter-allegation",
    "50+ guest and resident community context",
    "7 June 2018 to NEXUS 36 / DP 1901 continuity",
    "exact five-person DP 1901 perimeter",
    "CARET confirmation of Asunción Aizpurúa Sánchez",
    "Asperua transcription/search-variant reconciliation",
    "finite 17-person census",
    "two linked but non-merged ledgers",
    "criminal-not-merely-civil-and-not-innocuous",
    "exactly 17 public people and three protected role-only references",
    "continuous-integration enforcement",
):
    includes("\n".join(str(item) for item in scope_changes), marker, "manifest material-scope changes")
publication_boundaries = manifest.get("publication_boundaries", [])
for marker in (
    "neutral title is 3205/2014",
    "summons says Juicio de faltas",
    "later summary says DP",
    "second respondent remains fully anonymised",
    "officially received after the incident",
    "No raw source, filename, external locator",
    "source-reported titles",
    "criminal hijacking or capture allegation",
    "7 October 2014 email",
    "7 June 2018, not 7 July",
    "exactly five named private actors",
    "carets for Aizpurúa and canonical FMMM confirm identity only",
    "isolated MATA source-literal remains unresolved",
    "not rewritten with hindsight",
    "Later corroborative significance is not erased",
    "No knowledge, intent, agreement, criminal attribution, guilt or liability transfers",
):
    includes("\n".join(str(item) for item in publication_boundaries), marker, "manifest publication boundaries")

deletion_audit = read_text(DELETION_AUDIT)
includes(deletion_audit, f"**Superseding base:** `{BASE_REVISION}`", relative(DELETION_AUDIT))
for marker in (
    "3205/2014^ · Arrecife",
    "supersedes the earlier secondary-summary-only control",
    "one complainant described as Community president and one affected party described as administrator",
    "officially received after the 3 September incident",
    "criminal-first claimed-office supplement",
    "transcription error for `Gil Marer`",
    "7-Oct-2014 adviser email",
    "operating 50+ guest/resident community",
    "exactly five private actors",
    "two-ledger",
    "criminal, not merely",
    "normal publication chain",
    "does not extend to email",
    "17 named people and three protected role-only references",
    "PD-SP-P-0004",
    "PD-SP-P-0009",
):
    includes(deletion_audit, marker, relative(DELETION_AUDIT))


# The federated registry denominator must agree with the static bilingual presentation.
registry = read_json(REGISTRY)
require(registry.get("counts") == EXPECTED_COUNTS, "canonical registry counts are not 230/95/79/11/23/22")
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
require(actual_total == EXPECTED_COUNTS["total"], "federated registry actual total is not 230")
for record_type in ("PERSON", "ORGANISATION", "STRUCTURE", "INSTITUTION", "PROCEEDING"):
    require(actual_counts[record_type] == EXPECTED_COUNTS[record_type], f"federated registry actual {record_type} count is stale")

for page in (REGISTRY_EN, REGISTRY_ES):
    includes(read_text(page), 'data-static-registry-counts="230-95-79-11-23-22"', relative(page))

registry_en = read_text(REGISTRY_EN)
registry_es = read_text(REGISTRY_ES)
includes(registry_en, '"dateModified":"2026-08-30"', relative(REGISTRY_EN))
includes(registry_en, "30 AUGUST 2026", relative(REGISTRY_EN))
includes(registry_es, '"dateModified":"2026-08-30"', relative(REGISTRY_ES))
includes(registry_es, "30 AGOSTO 2026", relative(REGISTRY_ES))

current_unitary_state = read_json(CURRENT_UNITARY_STATE)
identity_registry_state = (
    current_unitary_state.get("identity_registry", {})
    if isinstance(current_unitary_state, dict)
    else {}
)
require(
    identity_registry_state.get("control_date") == "2026-08-30",
    "CURRENT_UNITARY_STATE identity-registry control date is stale",
)
require(
    identity_registry_state.get("counts") == EXPECTED_COUNTS,
    "CURRENT_UNITARY_STATE identity-registry counts are inconsistent",
)


if failures:
    print("3205/2014 ARRECIFE PUBLICATION VALIDATION: FAIL")
    for failure in failures:
        print(f"- {failure}")
    sys.exit(1)

print("3205/2014 ARRECIFE PUBLICATION VALIDATION: PASS")

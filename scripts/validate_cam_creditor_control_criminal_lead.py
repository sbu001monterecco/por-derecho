#!/usr/bin/env python3
"""Validate CAM direct criminal attribution, source fidelity and publication boundaries."""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NON_DILUTION_REL = "archive/EXPRESS_CRIMINAL_ATTRIBUTION_NON_DILUTION_SOURCE_FIDELITY_RULE_23AUG2026.md"
IDENTITY_REL = "archive/IDENTITY_CONTROL_LAURA_PATRICIA_ACOSTA_MATOS_23AUG2026.md"
SOURCE_REL = "archive/CAM_2017_2018_DIRECT_INSTRUCTION_LENDER_POSSESSION_SHADOW_ADMINISTRATION_JUDICIAL_OMISSION_LEAD_23AUG2026.md"
CORRECTION_REL = "archive/CORRECTION_REGISTER_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md"
MISSING_REL = "archive/MISSING_EVIDENCE_REGISTER_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md"
MAINTENANCE_REL = "archive/CONTINUOUS_MAINTENANCE_MATRIX_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md"
DATA_REL = "assets/data/cam-creditor-control-criminal-lead-v1.json"
MANIFEST_REL = "publication-manifests/cam-creditor-control-criminal-lead-20260823.json"
PROBE_REL = "deployment-probes/cam-creditor-control-criminal-lead-20260823.json"
EN_REL = "en/cam-creditor-control-shadow-administration-judicial-omission/index.html"
ES_REL = "es/control-acreedor-cam-administracion-hecho-omision-judicial/index.html"
CAM_MODULE_REL = "assets/cam-direct-instruction-shadow-admin-judicial-omission-20260823.js"
PROSECUTION_REL = "assets/prosecution-public-entry-20260821.js"
AUDIENCE_ORDER_REL = "assets/audience-experience-order-20260823.js"
AUDIENCE_RENDER_REL = "scripts/render_audience_experience.mjs"
LOADER_REL = "assets/sitewide-discovery-nav-20260821.js"
SITEMAP_REL = "sitemap-criminal-engineering.xml"
GENERAL_SITEMAP_REL = "sitemap.xml"

EN_AC_REL = "en/insolvency-36-2012-insolvency-administrator/index.html"
ES_AC_REL = "es/concurso-36-2012-administrador-concursal/index.html"
EN_DF_REL = "en/de-facto-administration-community-ac/index.html"
ES_DF_REL = "es/administracion-de-hecho-comunidad-ac/index.html"
AC_DATA_REL = "assets/data/ac-private-actor-de-facto-administration-v1.json"
MATERIAL_CONTROL_MODULE_REL = "assets/calificacion-2018-creditor-material-control-20260816.js"
AC_MANIFEST_REL = "publication-manifests/ac-community-de-facto-administration-2026-08-20.json"

PUBLICATION_ID = "CAM-CREDITOR-CONTROL-CRIMINAL-LEAD-20260823"
CONTROL_MARKER = "cam-creditor-control-criminal-lead-20260824"
HISTORICAL_MANIFEST_CONTROL_MARKER = "cam-creditor-control-criminal-lead-20260823"
EN_ROUTE = "/en/cam-creditor-control-shadow-administration-judicial-omission/"
ES_ROUTE = "/es/control-acreedor-cam-administracion-hecho-omision-judicial/"
BASE_URL = "https://sbu001monterecco.github.io/por-derecho"

errors: list[str] = []


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing file: {rel}")
        return ""
    return path.read_text(encoding="utf-8")


def load_json(rel: str) -> dict:
    text = read(rel)
    if not text:
        return {}
    try:
        value = json.loads(text)
    except Exception as exc:
        errors.append(f"invalid JSON {rel}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"JSON root must be an object: {rel}")
        return {}
    return value


def require(rel: str, text: str, markers: tuple[str, ...] | list[str]) -> None:
    for marker in markers:
        if marker not in text:
            errors.append(f"{rel}: missing marker {marker!r}")


def prohibit(rel: str, text: str, markers: tuple[str, ...] | list[str]) -> None:
    for marker in markers:
        if marker in text:
            errors.append(f"{rel}: prohibited marker present {marker!r}")


def require_before(rel: str, text: str, first: str, second: str) -> None:
    left = text.find(first)
    right = text.find(second)
    if left < 0 or right < 0 or left >= right:
        errors.append(f"{rel}: required order missing: {first!r} before {second!r}")


non_dilution = read(NON_DILUTION_REL)
identity_rule = read(IDENTITY_REL)
source = read(SOURCE_REL)
correction = read(CORRECTION_REL)
missing = read(MISSING_REL)
maintenance = read(MAINTENANCE_REL)
data_text = read(DATA_REL)
data = load_json(DATA_REL)
manifest = load_json(MANIFEST_REL)
probe = load_json(PROBE_REL)
en = read(EN_REL)
es = read(ES_REL)
cam_module = read(CAM_MODULE_REL)
prosecution = read(PROSECUTION_REL)
audience_order = read(AUDIENCE_ORDER_REL)
audience_render = read(AUDIENCE_RENDER_REL)
loader = read(LOADER_REL)
sitemap_text = read(SITEMAP_REL)
general_sitemap_text = read(GENERAL_SITEMAP_REL)
en_ac = read(EN_AC_REL)
es_ac = read(ES_AC_REL)
en_df = read(EN_DF_REL)
es_df = read(ES_DF_REL)
ac_data_text = read(AC_DATA_REL)
ac_data = load_json(AC_DATA_REL)
material_control_module = read(MATERIAL_CONTROL_MODULE_REL)
ac_manifest_text = read(AC_MANIFEST_REL)

# Repository-controlling hierarchy.
require(
    NON_DILUTION_REL,
    non_dilution,
    (
        "REPOSITORY-CONTROLLING · SITEWIDE · ANTI-REGRESSION",
        "express criminal allegation",
        "Four independent axes",
        "Attribution:",
        "Evidence:",
        "Adjudication and procedure:",
        "Source literal:",
        "Mandatory public architecture",
        "Prohibited dilution",
        "Audience-first design, progressive disclosure, summaries or homepage simplification must not bury the criminal attribution",
        "Publication validation must fail",
        "It preserves Gil Marer / Aweswell's position at full attributed strength.",
    ),
)
require(
    IDENTITY_REL,
    identity_rule,
    (
        "CONTROLLING IDENTITY, ATTRIBUTION AND SOURCE-FIDELITY RULE",
        "Gil Marer expressly attributes actor-specific participation and direct-instruction responsibility",
        "Source literal is not canonical identity",
        "Laura Matos",
        "No repository text, dataset or validator may say that those sources literally contain the full corrected name when they do not.",
        "The absence of completed proof does not weaken or erase the fact that Gil directly makes the allegation.",
        "Validation must not prohibit a faithful, expressly marked source-literal quotation",
    ),
)
require(
    SOURCE_REL,
    source,
    (
        "CANONICAL CRIMINAL-ALLEGATION / EVIDENCE-STATUS / PUBLICATION-CONTROL RECORD",
        "These are **Gil Marer / Aweswell criminal allegations**, not judicial findings.",
        "They are direct actor-specific attributions, not merely concerns, questions or investigative leads.",
        "the first 7 June 2018 email says **“la abogada de CAM, Laura Matos”**",
        "what the source literally says, the repository's canonical identity and Gil's direct attribution",
        "Gil Marer directly alleges that the 7 June event was not an unauthorised improvisation",
        "It does not convert Gil's direct allegation into a merely hypothetical question.",
        "The evidence is **not yet sufficient to publish those allegations as proved criminal facts**.",
        "The remaining gaps are not hidden weaknesses and are not reasons to dilute the direct attribution",
        "Silence is not admission.",
    ),
)
prohibit(
    SOURCE_REL,
    source,
    (
        "The filed complaint amendment alleges that Antonio Cogolludo and Laura Patricia Acosta Matos",
        "The 7 June complaint amendment identifies Antonio Cogolludo and Laura Patricia Acosta Matos",
        "precise identification of the Laura actor",
    ),
)
require(
    CORRECTION_REL,
    correction,
    (
        "CR-CAM7J-012",
        "CR-CAM7J-013",
        "CR-CAM7J-014",
        "Express criminal attribution.",
        "not merely questions or investigative leads",
        "Source fidelity.",
    ),
)
require(
    MISSING_REL,
    missing,
    (
        "not reasons to suppress, neutralise or euphemistically dilute",
        "ME-CAM7J-014",
        "It does not mean that Gil's direct allegation is merely hypothetical",
    ),
)
require(
    MAINTENANCE_REL,
    maintenance,
    (
        "Express attribution strength",
        "Source fidelity",
        "First-read prominence",
        "The need for proof does not dilute the allegation. The allegation does not establish guilt.",
    ),
)

# Bilingual canonical pages: direct allegation first, literal source intact, adverse record visible.
require(
    EN_REL,
    en,
    (
        'lang="en"',
        'data-express-criminal-attribution="20260824"',
        "UPDATED 24 AUGUST 2026",
        f'href="{BASE_URL}{EN_ROUTE}"',
        f'hreflang="en" href="{BASE_URL}{EN_ROUTE}"',
        f'hreflang="es" href="{BASE_URL}{ES_ROUTE}"',
        f'hreflang="x-default" href="{BASE_URL}{ES_ROUTE}"',
        "Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila Cogolludo Ramos, José Daniel Acosta Matos and Laura Patricia Acosta Matos",
        "These are direct criminal allegations supported by a multi-layer evidential corpus. They are not judicial findings.",
        "not merely an investigative question",
        "The attribution is direct.",
        '<span data-source-literal>“Laura Matos”</span>',
        "Source-fidelity rule.",
        "actor-specific participation to all five",
        "participation and responsibility to <strong>Laura Patricia Acosta Matos</strong>",
        "DIRECT CRIMINAL-ATTRIBUTION · PRIVATE INSTRUCTION",
        "criminally enabled, approved or ratified the 7 June operation",
        "role did not consist only of omissions",
        "not an adjudicated criminal fact",
        "Provisional dismissal upheld",
        "Contrary judicial record",
        "Right of reply.",
        "Silence is not admission.",
    ),
)
require_before(
    EN_REL,
    en,
    "These are direct criminal allegations",
    "Controlling boundary.",
)
prohibit(
    EN_REL,
    en,
    (
        "The first 7 June email says CAM’s lawyer Laura Patricia Acosta Matos",
        "The 7 June amendment alleged that Antonio Cogolludo and Laura Patricia Acosta Matos",
        "evidence supports the serious question whether those positions crossed",
    ),
)

require(
    ES_REL,
    es,
    (
        'lang="es"',
        'data-express-criminal-attribution="20260824"',
        "ACTUALIZADO 24 AGOSTO 2026",
        f'href="{BASE_URL}{ES_ROUTE}"',
        f'hreflang="en" href="{BASE_URL}{EN_ROUTE}"',
        f'hreflang="es" href="{BASE_URL}{ES_ROUTE}"',
        f'hreflang="x-default" href="{BASE_URL}{ES_ROUTE}"',
        "Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila Cogolludo Ramos, José Daniel Acosta Matos y Laura Patricia Acosta Matos",
        "Son acusaciones penales directas apoyadas en un corpus probatorio de varias capas. No son declaraciones judiciales.",
        "no es una mera pregunta investigativa",
        "La atribución es directa.",
        '<span data-source-literal>«Laura Matos»</span>',
        "Regla de fidelidad de fuente.",
        "participación actor-específica a los cinco",
        "participación y responsabilidad a <strong>Laura Patricia Acosta Matos</strong>",
        "ATRIBUCIÓN PENAL DIRECTA · INSTRUCCIÓN PRIVADA",
        "habilitó, aprobó o ratificó penalmente la operación de 7 de junio",
        "no consistió sólo en omisiones",
        "no un hecho penal declarado",
        "Archivo provisional confirmado",
        "Registro judicial contrario",
        "Derecho de respuesta.",
        "El silencio no es admisión.",
    ),
)
require_before(
    ES_REL,
    es,
    "Son acusaciones penales directas",
    "Límite rector.",
)
prohibit(
    ES_REL,
    es,
    (
        "El primer correo de 7 de junio dice que la abogada de CAM Laura Patricia Acosta Matos",
        "La ampliación de 7 de junio alegó que Antonio Cogolludo y Laura Patricia Acosta Matos",
        "la prueba plantea seriamente si esos derechos cruzaron",
    ),
)

# Cross-site and homepage modules cannot soften or bury the attribution.
require(
    CAM_MODULE_REL,
    cam_module,
    (
        'data-cam-criminal-lead="20260824"',
        "five identified private actors",
        "cinco actores privados identificados",
        "not merely questions, and not adjudicated findings",
        "no meras preguntas ni declaraciones judiciales",
        "FMMM · Antonio · Shaila · JDAM · Laura Patricia",
        "Affirmative criminal enablement plus omission",
        "Habilitación penal afirmativa más omisión",
        "allegedly sabotaging or frustrating a developed, finance-backed exit",
        "saboteando o frustrando con ello una salida desarrollada y respaldada por financiación",
        "Attribution and source-fidelity control — Laura Patricia Acosta Matos",
        "Control de atribución y fidelidad de fuente — Laura Patricia Acosta Matos",
        "data-source-literal",
        "Direct allegation ≠ adjudicated finding",
        "Acusación directa ≠ declaración judicial",
        "The 2018 criminal proceedings were provisionally dismissed",
        "Las diligencias penales de 2018 fueron archivadas provisionalmente",
    ),
)
require(
    PROSECUTION_REL,
    prosecution,
    (
        "dataset.expressCriminalAttribution = '20260824'",
        "Gil Marer and Aweswell allege one continuing economic-criminal enterprise, advanced through successive adoption and divided functions.",
        "Gil Marer y Aweswell alegan una sola empresa continuada de criminalidad económica, desarrollada mediante adopción sucesiva y división de funciones.",
        "This is only a factual allegation of connection: it does not characterise the conduct as a continuing or permanent offence",
        "Esta es solo una alegación fáctica de conexión: no califica los hechos como delito continuado o permanente",
        "Relationship is not responsibility; missing proof does not erase the allegation.",
        "Relación no es responsabilidad; la prueba pendiente no borra la acusación.",
        "José Daniel Acosta Matos",
        "Laura Patricia Acosta Matos",
        "Francisco Mario Matos Matas",
        "Antonio Cogolludo Rojas",
        "Shaila María Cogolludo Ramos",
        "affirmative enablement through emails, meetings, requests, authorisations, decisions, implementation, adoption and ratification, as well as omissions",
        "Judge Alberto López Villarrubia",
        "sabotaging or frustrating a developed, finance-backed exit",
        "provisional dismissal",
        "archivo provisional",
    ),
)
require(
    AUDIENCE_ORDER_REL,
    audience_order,
    (
        "const prosecution = main.querySelector",
        "[hero, controlling, detailed, criminalMisuse, priority, prosecution, summary, audiences, perimeters]",
        "audienceProtectedAttribution",
        "expressCriminalAttributionVisible",
    ),
)
require(
    AUDIENCE_RENDER_REL,
    audience_render,
    (
        "attributionVisibleBeforeCollapse",
        "directAttributionTextPresent",
        "protectedAttributionMarker",
        "contraryRecordPresent",
        "direct attribution is hidden in collapsed full record",
    ),
)
require(
    LOADER_REL,
    loader,
    (
        "CAM-DIRECT-INSTRUCTION-SHADOW-ADMIN-JUDICIAL-OMISSION-ROUTE-LOADER-20260823",
        "cam-direct-instruction-shadow-admin-judicial-omission-20260823.js?v=20260824a",
        "data-cam-direct-instruction-loader",
    ),
)

# Existing cross-track 15-February creditor-substitution correction remains intact.
for rel, text, marker in (
    (EN_DF_REL, en_df, "15 February 2018: formal Promontoria-to-CAM holder substitution"),
    (EN_DF_REL, en_df, 'href="../lpb-solvency-record/"'),
    (ES_DF_REL, es_df, "15/02/2018: modificación formal del titular Promontoria→CAM"),
    (ES_DF_REL, es_df, 'href="../expediente-solvencia-lpb/"'),
    (AC_DATA_REL, ac_data_text, '"event": "2018-02-15 Article 97 bis order"'),
    (MATERIAL_CONTROL_MODULE_REL, material_control_module, "20 OCT 2017 → 15 FEB 2018"),
    (AC_MANIFEST_REL, ac_manifest_text, "The 15 February 2018 Article 97 bis order changed the credit holder to CAM"),
):
    if marker not in text:
        errors.append(f"{rel}: corrected 15-Feb-2018 creditor-substitution marker missing")
for rel, text, old in (
    (SOURCE_REL, source, "8 February 2018"),
    (EN_REL, en, "judicial recognition on 8 February 2018"),
    (ES_REL, es, "reconocimiento judicial el 8 febrero 2018"),
    (EN_DF_REL, en_df, "8 February 2018: formal Promontoria-to-CAM holder substitution"),
    (ES_DF_REL, es_df, "08/02/2018: modificación formal del titular Promontoria→CAM"),
    (AC_DATA_REL, ac_data_text, '"event": "2018-02-08 Article 97 bis order"'),
    (MATERIAL_CONTROL_MODULE_REL, material_control_module, "8 FEB 2018"),
    (AC_MANIFEST_REL, ac_manifest_text, "The 8 February 2018 Article 97 bis order changed the credit holder to CAM"),
):
    if old in text:
        errors.append(f"{rel}: superseded 8-February marker repeated: {old!r}")

# Insolvency-administrator cross-pages retain the allegation/not-finding distinction.
require(
    EN_AC_REL,
    en_ac,
    (
        "This page does not establish corruption, collusion or unlawful intent.",
        "separately preserves Gil Marer's attributed approval, enablement, ratification or legally equivalent omission allegation",
        "it is an allegation for investigation, not a finding.",
    ),
)
require(
    ES_AC_REL,
    es_ac,
    (
        "Esta página no establece delito",
        "preserva separadamente la alegación atribuida a Gil Marer de aprobación, facilitación, ratificación u omisión jurídicamente equivalente",
        "es una alegación para investigar, no una declaración judicial.",
    ),
)

# Sitemap/canonical parity.
for rel, text in ((SITEMAP_REL, sitemap_text), (GENERAL_SITEMAP_REL, general_sitemap_text)):
    if not text:
        continue
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        errors.append(f"invalid XML {rel}: {exc}")
        continue
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9", "xhtml": "http://www.w3.org/1999/xhtml"}
    expected = {
        "en": f"{BASE_URL}{EN_ROUTE}",
        "es": f"{BASE_URL}{ES_ROUTE}",
        "x-default": f"{BASE_URL}{ES_ROUTE}",
    }
    urls = root.findall("sm:url", ns)
    locations = {node.text.strip() for node in root.findall("sm:url/sm:loc", ns) if node.text}
    for location in {expected["en"], expected["es"]}:
        if location not in locations:
            errors.append(f"{rel}: missing canonical location {location}")
    for url in urls:
        loc = url.find("sm:loc", ns)
        if loc is None or not loc.text or loc.text.strip() not in expected.values():
            continue
        alternates = {link.get("hreflang"): link.get("href") for link in url.findall("xhtml:link", ns)}
        if alternates != expected:
            errors.append(f"{rel}: CAM alternate map mismatch: {alternates}")

# Machine-readable control.
if data.get("schema_version") != "1.3":
    errors.append("dataset schema_version must be 1.3")
if data.get("publication_id") != PUBLICATION_ID or data.get("control_marker") != CONTROL_MARKER:
    errors.append("dataset publication identity mismatch")
if data.get("control_date") != "2026-08-24":
    errors.append("dataset control date must reflect the 20260824 substantive update")
update_marker = "five-actor-shadow-administration-ac-judicial-acts-omissions-funded-exit-20260824"
if data.get("substantive_update_marker") != update_marker:
    errors.append("dataset 20260824 substantive-update marker mismatch")
expected_update_controls = {
    "FIVE_ACTOR_SHADOW_DE_FACTO_ADMINISTRATION_DIRECT_ALLEGATION_20260824",
    "AC_AFFIRMATIVE_COMMISSIONS_ENABLEMENT_AND_OMISSIONS_DIRECT_ALLEGATION_20260824",
    "JUDICIAL_AFFIRMATIVE_ACTS_OMISSIONS_FUNDED_EXIT_SABOTAGE_DIRECT_ALLEGATION_20260824",
    "AWESWELL_SPONSOR_PERFORMANCE_COLLATERAL_AND_INSTITUTIONAL_DEPENDENCIES_20260824",
}
if set(data.get("update_controls", [])) != expected_update_controls:
    errors.append("dataset must contain the four exact 20260824 allegation and finance controls")
if data.get("status") != "DRAFT_ATTRIBUTED_CRIMINAL_ALLEGATION_NOT_FINDING":
    errors.append("dataset allegation/not-finding status mismatch")
if data.get("canonical_source") != SOURCE_REL or data.get("non_dilution_rule") != NON_DILUTION_REL:
    errors.append("dataset controlling source/rule mismatch")
if data.get("public_routes") != {"en": EN_ROUTE, "es": ES_ROUTE}:
    errors.append("dataset bilingual route map mismatch")

position = data.get("controlling_position", {})
expected_position = {
    "attribution_strength": "DIRECT_ACTOR_SPECIFIC_CRIMINAL_ATTRIBUTION_NOT_MERE_QUESTION_OR_LEAD",
    "evidence_sufficiency": "SUFFICIENT_TO_MAKE_PRESERVE_PUBLISH_AS_ATTRIBUTED_AND_REQUEST_INVESTIGATION",
    "non_dilution_required": True,
    "first_read_prominence_required": True,
    "source_literals_preserved": True,
    "five_actor_shadow_administration_allegation_preserved": True,
    "administrator_affirmative_commission_and_omission_allegation_preserved": True,
    "judicial_acts_omissions_and_funded_exit_sabotage_allegation_preserved": True,
    "finance_condition_allocation_and_source_status_preserved": True,
    "criminal_guilt_adjudicated": False,
    "collective_guilt_presumed": False,
    "presumption_of_innocence_preserved": True,
    "right_of_reply_preserved": True,
}
for key, expected in expected_position.items():
    if position.get(key) != expected:
        errors.append(f"dataset controlling-position mismatch: {key}")

expected_private_actors = [
    ("ACT-FMMM", "Francisco Mario Matos Matas"),
    ("ACT-ACR", "Antonio Cogolludo Rojas"),
    ("ACT-SMCR", "Shaila María Cogolludo Ramos"),
    ("ACT-JDAM", "José Daniel Acosta Matos"),
    ("ACT-LPAM", "Laura Patricia Acosta Matos"),
]
private_perimeter = data.get("canonical_private_actor_perimeter_20260824", {})
actual_private_actors = [
    (actor.get("id"), actor.get("name"))
    for actor in private_perimeter.get("actors", [])
    if isinstance(actor, dict)
]
if actual_private_actors != expected_private_actors:
    errors.append("dataset five-private-actor perimeter is missing, reordered or misnamed")
if private_perimeter.get("marker") != "FIVE_ACTOR_SHADOW_DE_FACTO_ADMINISTRATION_DIRECT_ALLEGATION_20260824":
    errors.append("dataset five-actor 20260824 marker mismatch")
if private_perimeter.get("attributed_to") != "Gil Marer":
    errors.append("dataset five-actor allegation must be attributed to Gil Marer")
if private_perimeter.get("criminal_finding") is not False:
    errors.append("dataset five-actor allegation must not be represented as a criminal finding")
for key in ("collective_participation_in_every_step_established", "shared_criminal_intent_established"):
    if private_perimeter.get(key) is not False:
        errors.append(f"dataset five-actor perimeter boundary mismatch: {key}")
for phrase in ("five named private actors", "shadow or de facto administration", "allegedly concealed parallel-control architecture"):
    if phrase not in private_perimeter.get("direct_shadow_administration_allegation", ""):
        errors.append(f"dataset five-actor direct allegation missing required copy: {phrase}")

lanes = data.get("allegation_lanes", [])
if not isinstance(lanes, list) or {item.get("id") for item in lanes if isinstance(item, dict)} != {"CAM-LEAD-01", "CAM-LEAD-02", "CAM-LEAD-03"}:
    errors.append("dataset must contain the three controlled allegation lanes")
else:
    for lane in lanes:
        if lane.get("attributed") is not True or not str(lane.get("attribution_strength", "")).startswith("DIRECT_"):
            errors.append(f"{lane.get('id')}: direct attribution missing")
        if lane.get("criminal_finding") is not False:
            errors.append(f"{lane.get('id')}: allegation incorrectly represented as finding")
        if not lane.get("unresolved_bridges"):
            errors.append(f"{lane.get('id')}: unresolved proof must remain explicit")

lane_by_id = {lane.get("id"): lane for lane in lanes if isinstance(lane, dict)}
private_lane = lane_by_id.get("CAM-LEAD-01", {})
administrator_lane = lane_by_id.get("CAM-LEAD-02", {})
judge_lane = lane_by_id.get("CAM-LEAD-03", {})

expected_named_actor_mentions = {
    "José Daniel Acosta Matos (JDAM)",
    "Laura Patricia Acosta Matos (LPAM)",
    "Francisco Mario Matos Matas (FMMM)",
    "Antonio Cogolludo Rojas",
    "Shaila María Cogolludo Ramos",
}
if not expected_named_actor_mentions.issubset(set(private_lane.get("actors", []))):
    errors.append("CAM-LEAD-01 must name all five controlled private actors")
if private_lane.get("marker") != "FIVE_ACTOR_SHADOW_DE_FACTO_ADMINISTRATION_DIRECT_ALLEGATION_20260824":
    errors.append("CAM-LEAD-01 20260824 marker mismatch")
for phrase in ("five named actors", "shadow or de facto administration", "allegedly concealed parallel material-control architecture"):
    if phrase not in private_lane.get("direct_shadow_administration_allegation", ""):
        errors.append(f"CAM-LEAD-01 missing required direct-allegation copy: {phrase}")

if administrator_lane.get("marker") != "AC_AFFIRMATIVE_COMMISSIONS_ENABLEMENT_AND_OMISSIONS_DIRECT_ALLEGATION_20260824":
    errors.append("CAM-LEAD-02 20260824 marker mismatch")
if administrator_lane.get("actor") != "Francisco de Borja Rodríguez-Batllori Laffitte":
    errors.append("CAM-LEAD-02 Administrator identity mismatch")
for phrase in ("affirmative commission and enablement", "emails and meetings", "failed to protect, recover, account, report or preserve the funded exit"):
    if phrase not in administrator_lane.get("direct_criminal_allegation", ""):
        errors.append(f"CAM-LEAD-02 missing required direct-allegation copy: {phrase}")
for key, minimum in (
    ("affirmative_commissions_and_enablement_alleged", 5),
    ("omissions_alleged", 5),
    ("documented_basis", 6),
    ("contrary_evidence", 3),
    ("unresolved_bridges", 6),
):
    if len(administrator_lane.get(key, [])) < minimum:
        errors.append(f"CAM-LEAD-02 20260824 control is too thin: {key}")
if "conditionally closable exit" not in administrator_lane.get("funded_exit_sabotage_claim", "").lower():
    errors.append("CAM-LEAD-02 conditional finance-exit allegation is missing")

if judge_lane.get("marker") != "JUDICIAL_AFFIRMATIVE_ACTS_OMISSIONS_FUNDED_EXIT_SABOTAGE_DIRECT_ALLEGATION_20260824":
    errors.append("CAM-LEAD-03 20260824 marker mismatch")
if judge_lane.get("actor") != "Alberto López Villarrubia":
    errors.append("CAM-LEAD-03 judge identity mismatch")
for phrase in ("strongest act-and-omission form", "affirmative resolutions, refusals, procedural directions", "sabotaged the funded exit"):
    if phrase not in judge_lane.get("direct_criminal_allegation", ""):
        errors.append(f"CAM-LEAD-03 missing required direct-allegation copy: {phrase}")
for key, minimum in (
    ("affirmative_acts_alleged", 3),
    ("omissions_alleged", 4),
    ("documented_basis", 5),
    ("contrary_evidence", 4),
    ("unresolved_bridges", 6),
):
    if len(judge_lane.get(key, [])) < minimum:
        errors.append(f"CAM-LEAD-03 20260824 control is too thin: {key}")
for phrase in ("direct enabling role", "affirmative acts and omissions", "Daniel Irigoyen", "conditionally closable exit"):
    if phrase not in judge_lane.get("funded_exit_sabotage_claim", ""):
        errors.append(f"CAM-LEAD-03 funded-exit allegation missing required copy: {phrase}")

funded_exit = data.get("funded_exit_control_20260824", {})
if funded_exit.get("attributed_to") != "Gil Marer" or funded_exit.get("criminal_finding") is not False:
    errors.append("funded-exit control must be attributed to Gil and preserved as a non-finding")
for phrase in ("five-actor private-control architecture", "Administrator's affirmative enablement and omissions", "judge's affirmative acts and omissions", "conditionally closable exit", "performed or could perform all sponsor-side"):
    if phrase not in funded_exit.get("direct_allegation", ""):
        errors.append(f"funded-exit control missing required direct-allegation copy: {phrase}")
if len(funded_exit.get("documented_components", [])) < 5:
    errors.append("funded-exit control must retain the five documentary components")
if len(funded_exit.get("contrary_evidence_and_limits", [])) < 4:
    errors.append("funded-exit control must preserve meaningful contrary evidence and limits")
if len(funded_exit.get("unresolved_bridges", [])) < 4:
    errors.append("funded-exit control must preserve unresolved proof")

finance_marker = "AWESWELL_SPONSOR_PERFORMANCE_COLLATERAL_AND_INSTITUTIONAL_DEPENDENCIES_20260824"
finance = data.get("finance_condition_allocation_20260824", {})
if finance.get("marker") != finance_marker or finance.get("attributed_to") != "Gil Marer":
    errors.append("finance-condition control marker or attribution mismatch")
finance_direct = finance.get("direct_allegation", {})
if finance_direct.get("criminal_finding") is not False or finance_direct.get("causation_adjudicated") is not False:
    errors.append("finance-condition allegation must remain a non-finding")
for phrase in (
    "performed or could perform all sponsor-side",
    "staged security and collateral package",
    "Insolvency Administrator debt certificate",
    "lender-in-possession mechanism obstructing redemption and refinancing",
):
    if phrase not in finance_direct.get("en", ""):
        errors.append(f"finance-condition allegation missing required copy: {phrase}")
finance_classes = finance.get("condition_classes", {})
for key in ("sponsor_borrower_or_counterparty_side", "court_administrator_and_collateral_dependencies", "lender_internal_or_third_party"):
    if len(finance_classes.get(key, {}).get("documented_conditions", [])) < 4:
        errors.append(f"finance-condition class is too thin: {key}")
finance_routes = finance.get("route_source_status", {})
if set(finance_routes) != {"ona_clubotel", "stoneweg_vso", "ben_oldman", "lagune_elaia"}:
    errors.append("finance-condition control must preserve ONA, VSO, Ben Oldman and Elaia source status")
for route in finance_routes.values():
    if not route.get("status") or not route.get("limits"):
        errors.append("finance route lacks exact status or limits")
if len(finance.get("publication_boundaries", [])) < 5 or len(finance.get("unresolved_evidence", [])) < 6:
    errors.append("finance-condition boundaries or unresolved-evidence ledger is too thin")

# Both machine-readable records must carry the same 20260824 perimeter and institutional identities.
if ac_data.get("substantive_update_marker") != update_marker:
    errors.append("AC de-facto dataset is not aligned to the 20260824 substantive marker")
ac_private = ac_data.get("canonical_private_actor_perimeter_20260824", {})
ac_private_actors = [
    (actor.get("id"), actor.get("name"))
    for actor in ac_private.get("actors", [])
    if isinstance(actor, dict)
]
if ac_private_actors != actual_private_actors:
    errors.append("CAM and AC datasets disagree on the canonical five-private-actor perimeter")
ac_institutional = ac_data.get("institutional_attributions_20260824", {})
if ac_institutional.get("insolvency_administrator", {}).get("actor") != administrator_lane.get("actor"):
    errors.append("CAM and AC datasets disagree on the Administrator identity")
if ac_institutional.get("judge", {}).get("actor") != judge_lane.get("actor"):
    errors.append("CAM and AC datasets disagree on the judge identity")

identity = data.get("identity_control", {})
expected_identity = {
    "canonical_identity": "Laura Patricia Acosta Matos",
    "repository_lpam_name": "Laura Patricia Acosta Matos",
    "contemporaneous_email_source_literal": "Laura Matos",
    "filed_7_june_amendment_source_literal_status": "DIFFERENT_FORENAME_TYPO_PRESERVED_IN_NATIVE_SOURCE",
    "source_literal_rewritten_as_canonical_identity": False,
    "source_literal_public_only_if_expressly_marked": True,
    "name_controlled_as_typographical_error": True,
    "direct_attribution_preserved": True,
    "laura_patricia_physical_presence_established": False,
    "laura_patricia_direct_instruction_established": False,
}
for key, expected in expected_identity.items():
    if identity.get(key) != expected:
        errors.append(f"dataset identity/source-literal mismatch: {key}")
for old_key in ("contemporaneous_email_name", "filed_7_june_amendment_name"):
    if old_key in identity:
        errors.append(f"dataset retains source/canonical conflation field: {old_key}")
prohibit(
    DATA_REL,
    data_text,
    (
        "contemporaneous placement of CAM lawyer Laura Patricia Acosta Matos",
        "filed 7 June amendment naming Laura Patricia Acosta Matos",
    ),
)

boundaries = data.get("publication_boundaries", {})
for key in (
    "criminal_guilt_as_established",
    "direct_instruction_as_adjudicated_fact",
    "administrator_criminal_approval_as_adjudicated_fact",
    "five_actor_shadow_administration_as_adjudicated_fact",
    "administrator_affirmative_commission_or_omission_as_adjudicated_fact",
    "judicial_prevarication_as_established",
    "judicial_affirmative_acts_or_omissions_as_adjudicated_prevarication",
    "funded_exit_sabotage_as_adjudicated_fact",
    "all_sponsor_side_conditions_as_independently_verified_fact",
    "single_or_only_closing_condition_as_verified_fact",
    "lender_internal_approval_as_borrower_side_performance",
    "non_institutional_criminal_epithet_as_fact",
    "dilute_direct_attribution_to_question_or_lead",
    "rewrite_source_literal_as_canonical_identity",
    "treat_source_typo_as_separate_actor",
    "hide_direct_attribution_in_collapsed_content",
    "infer_later_evidence_was_before_earlier_actor",
    "treat_valid_credit_as_whole_hotel_title",
    "treat_later_adjudication_as_retroactive_authority",
    "publish_raw_private_evidence",
):
    if boundaries.get(key) is not False:
        errors.append(f"dataset publication boundary mismatch: {key}")
for key in (
    "state_allegations_as_attributed",
    "state_direct_attribution_before_caveats",
    "first_read_direct_attribution_required",
    "preserve_strongest_defences",
    "preserve_20260824_direct_allegations",
    "preserve_finance_condition_allocation_and_route_source_status",
    "preserve_right_of_reply",
):
    if boundaries.get(key) is not True:
        errors.append(f"dataset publication safeguard mismatch: {key}")

contrary = data.get("contrary_record", {})
for key in (
    "provisional_dismissal_2018",
    "appellate_confirmation",
    "administrator_denied_main_lock_takeover_instruction",
    "administrator_described_narrower_access_authority",
    "irigoyen_report_is_not_official_judicial_minute",
    "funding_routes_had_conditions",
):
    if contrary.get(key) is not True:
        errors.append(f"dataset contrary-record safeguard missing: {key}")
if contrary.get("funded_exit_sabotage_adjudicated") is not False:
    errors.append("dataset contrary record must state that funded-exit sabotage is not adjudicated")
for key in (
    "sponsor_side_performance_complete_for_every_route_independently_proved",
    "all_lender_credit_management_or_board_approvals_proved",
    "single_operational_blocking_condition_proved",
):
    if contrary.get(key) is not False:
        errors.append(f"dataset finance contrary-record boundary missing: {key}")
if len(contrary.get("judicial_corrective_or_contrary_acts_preserved", [])) < 3:
    errors.append("dataset must preserve the identified judicial corrective or contrary acts")

# Manifest controls and historical deployment record.
if manifest.get("publication_id") != PUBLICATION_ID or manifest.get("control_marker") != HISTORICAL_MANIFEST_CONTROL_MARKER:
    errors.append("manifest publication identity mismatch")
if manifest.get("expected_routes") != {"en": [EN_REL], "es": [ES_REL]}:
    errors.append("manifest expected route map mismatch")
for rel in manifest.get("expected_source_files", []):
    if not isinstance(rel, str) or not (ROOT / rel).is_file():
        errors.append(f"manifest expected source missing: {rel!r}")
for rel in (NON_DILUTION_REL, IDENTITY_REL, SOURCE_REL, CORRECTION_REL, MISSING_REL, MAINTENANCE_REL):
    if rel not in manifest.get("expected_source_files", []):
        errors.append(f"manifest omits controlling source: {rel}")

non_dilution_manifest = manifest.get("non_dilution_control", {})
expected_non_dilution = {
    "control_file": NON_DILUTION_REL,
    "direct_attribution_required": True,
    "soften_to_question_or_lead": False,
    "first_read_prominence_required": True,
    "hide_in_collapsed_content": False,
    "evidential_gap_erases_attribution": False,
    "criminal_guilt_adjudicated": False,
}
for key, expected in expected_non_dilution.items():
    if non_dilution_manifest.get(key) != expected:
        errors.append(f"manifest non-dilution mismatch: {key}")

identity_manifest = manifest.get("superseding_identity_control", {})
for key, expected in {
    "identity": "Laura Patricia Acosta Matos",
    "source_typo_creates_separate_actor": False,
    "source_literal_rewritten_as_canonical_identity": False,
    "contemporaneous_email_source_literal": "Laura Matos",
    "control_file": IDENTITY_REL,
}.items():
    if identity_manifest.get(key) != expected:
        errors.append(f"manifest identity/source-fidelity mismatch: {key}")

safety = manifest.get("publication_safety", {})
for key in (
    "raw_private_emails_committed",
    "private_message_ids_committed",
    "privileged_advice_committed",
    "unnecessary_personal_identifiers_committed",
    "criminal_guilt_stated_as_final",
    "direct_instruction_stated_as_adjudicated",
    "administrator_criminal_approval_stated_as_adjudicated",
    "judicial_prevarication_stated_as_established",
    "source_typo_treated_as_separate_actor",
    "source_literal_rewritten_as_canonical_identity",
    "direct_attribution_diluted_to_question_or_lead",
    "direct_attribution_hidden_in_collapsed_content",
):
    if safety.get(key) is not False:
        errors.append(f"manifest publication-safety mismatch: {key}")
for key in ("presumption_of_innocence_preserved", "right_of_reply_preserved"):
    if safety.get(key) is not True:
        errors.append(f"manifest publication safeguard mismatch: {key}")

if manifest.get("current_state") == "DELETION_SAFE":
    if manifest.get("merge_sha") != "c2f77661371384a79fb7e0caaef79c6345cabecf":
        errors.append("historical deployment merge SHA mismatch")
    if manifest.get("validation", {}).get("status") != "CI_GREEN_LIVE_VERIFIED":
        errors.append("historical validation state mismatch")
    if probe.get("publication_id") != PUBLICATION_ID or probe.get("verified") is not True:
        errors.append("historical deployment probe is not controlled/verified")

# Public privacy and source-literal discipline.
for rel, text in ((EN_REL, en), (ES_REL, es), (CAM_MODULE_REL, cam_module), (DATA_REL, data_text), (PROSECUTION_REL, prosecution)):
    if re.search(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", text):
        errors.append(f"{rel}: email address exposed")
    for token in ("message_id", "thread_id", "drive_item_id", "44700629Z"):
        if token.lower() in text.lower():
            errors.append(f"{rel}: private source identifier exposed: {token}")
    if "Laura Isabel" in text:
        errors.append(f"{rel}: erroneous public identity variant exposed")
    if rel in (DATA_REL,) and "mafia" in text.lower():
        errors.append(f"{rel}: non-institutional criminal epithet exposed")
    if "Laura Matos" in text:
        allowed = (
            "data-source-literal" in text
            or '"contemporaneous_email_source_literal": "Laura Matos"' in text
            or '"source_literal"' in text
        )
        if not allowed:
            errors.append(f"{rel}: source-literal name lacks an explicit source-literal marker")

if errors:
    print("CAM DIRECT CRIMINAL ATTRIBUTION / SOURCE FIDELITY: FAIL", file=sys.stderr)
    for error in errors:
        print(f" - {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "CAM DIRECT CRIMINAL ATTRIBUTION / SOURCE FIDELITY: PASS "
    f"({len(lanes)} direct allegation lanes; bilingual first-read attribution; marked source literal; contrary record and non-finding boundary preserved)"
)

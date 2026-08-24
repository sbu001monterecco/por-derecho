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
CONTROL_MARKER = "cam-creditor-control-criminal-lead-20260823"
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
        'data-express-criminal-attribution="20260823"',
        f'href="{BASE_URL}{EN_ROUTE}"',
        f'hreflang="en" href="{BASE_URL}{EN_ROUTE}"',
        f'hreflang="es" href="{BASE_URL}{ES_ROUTE}"',
        f'hreflang="x-default" href="{BASE_URL}{ES_ROUTE}"',
        "Gil Marer and Aweswell expressly allege that identified CAM / Acosta Matos and connected private actors",
        "These are direct criminal allegations supported by a multi-layer evidential corpus. They are not judicial findings.",
        "not merely an investigative question",
        "The attribution is direct.",
        '<span data-source-literal>“Laura Matos”</span>',
        "Source-fidelity rule.",
        "Gil directly attributes participation and responsibility to <strong>Laura Patricia Acosta Matos</strong>",
        "DIRECT CRIMINAL-ATTRIBUTION · PRIVATE INSTRUCTION",
        "Gil alleges that the insolvency administrator criminally enabled, approved or ratified the 7 June operation",
        "Gil directly alleges omissionary judicial prevarication.",
        "Provisional dismissal upheld",
        "Right of reply.",
        "Silence is not admission.",
    ),
)
require_before(
    EN_REL,
    en,
    "Gil Marer and Aweswell expressly allege that identified CAM / Acosta Matos and connected private actors",
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
        'data-express-criminal-attribution="20260823"',
        f'href="{BASE_URL}{ES_ROUTE}"',
        f'hreflang="en" href="{BASE_URL}{EN_ROUTE}"',
        f'hreflang="es" href="{BASE_URL}{ES_ROUTE}"',
        f'hreflang="x-default" href="{BASE_URL}{ES_ROUTE}"',
        "Gil Marer y Aweswell atribuyen directamente a actores identificados de CAM / Acosta Matos",
        "Son acusaciones penales directas apoyadas en un corpus probatorio de varias capas. No son declaraciones judiciales.",
        "no es una mera pregunta investigativa",
        "La atribución es directa.",
        '<span data-source-literal>«Laura Matos»</span>',
        "Regla de fidelidad de fuente.",
        "Gil atribuye directamente participación y responsabilidad a <strong>Laura Patricia Acosta Matos</strong>",
        "ATRIBUCIÓN PENAL DIRECTA · INSTRUCCIÓN PRIVADA",
        "Gil alega que el administrador concursal habilitó, aprobó o ratificó penalmente la operación de 7 de junio",
        "Gil alega directamente prevaricación judicial por omisión.",
        "Archivo provisional confirmado",
        "Derecho de respuesta.",
        "El silencio no es admisión.",
    ),
)
require_before(
    ES_REL,
    es,
    "Gil Marer y Aweswell atribuyen directamente a actores identificados de CAM / Acosta Matos",
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
        'data-cam-criminal-lead="20260823"',
        "directly allege that identified CAM / Acosta Matos",
        "atribuyen directamente a actores identificados de CAM / Acosta Matos",
        "not merely questions or investigative leads",
        "no meras preguntas ni simples líneas de investigación",
        "CAM / JDAM / Laura Patricia / FMMM",
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
        "dataset.expressCriminalAttribution = '20260823'",
        "Gil Marer and Aweswell directly allege an organised criminal course",
        "Gil Marer y Aweswell alegan directamente un curso delictivo organizado",
        "not merely a set of questions",
        "no una mera serie de preguntas",
        "Relationship is not responsibility; missing proof does not erase the allegation.",
        "Relación no es responsabilidad; la prueba pendiente no borra la acusación.",
        "José Daniel Acosta Matos",
        "Laura Patricia Acosta Matos",
        "provisional dismissal",
        "archivo provisional",
    ),
)
require(
    AUDIENCE_ORDER_REL,
    audience_order,
    (
        "const prosecution = main.querySelector",
        "[hero, criminalMisuse, priority, prosecution, summary, audiences, perimeters]",
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
        "cam-direct-instruction-shadow-admin-judicial-omission-20260823.js?v=20260823a",
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
if data.get("schema_version") != "1.1":
    errors.append("dataset schema_version must be 1.1")
if data.get("publication_id") != PUBLICATION_ID or data.get("control_marker") != CONTROL_MARKER:
    errors.append("dataset publication identity mismatch")
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
    "criminal_guilt_adjudicated": False,
    "collective_guilt_presumed": False,
    "presumption_of_innocence_preserved": True,
    "right_of_reply_preserved": True,
}
for key, expected in expected_position.items():
    if position.get(key) != expected:
        errors.append(f"dataset controlling-position mismatch: {key}")

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
    "judicial_prevarication_as_established",
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
    "preserve_right_of_reply",
):
    if boundaries.get(key) is not True:
        errors.append(f"dataset publication safeguard mismatch: {key}")

# Manifest controls and historical deployment record.
if manifest.get("publication_id") != PUBLICATION_ID or manifest.get("control_marker") != CONTROL_MARKER:
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

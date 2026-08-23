#!/usr/bin/env python3
"""Validate the CAM creditor-control criminal-lead publication controls."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_REL = "assets/data/cam-creditor-control-criminal-lead-v1.json"
MANIFEST_REL = "publication-manifests/cam-creditor-control-criminal-lead-20260823.json"
PROBE_REL = "deployment-probes/cam-creditor-control-criminal-lead-20260823.json"
SOURCE_REL = "archive/CAM_2017_2018_DIRECT_INSTRUCTION_LENDER_POSSESSION_SHADOW_ADMINISTRATION_JUDICIAL_OMISSION_LEAD_23AUG2026.md"
EN_REL = "en/cam-creditor-control-shadow-administration-judicial-omission/index.html"
ES_REL = "es/control-acreedor-cam-administracion-hecho-omision-judicial/index.html"
EN_AC_REL = "en/insolvency-36-2012-insolvency-administrator/index.html"
ES_AC_REL = "es/concurso-36-2012-administrador-concursal/index.html"
EN_DF_REL = "en/de-facto-administration-community-ac/index.html"
ES_DF_REL = "es/administracion-de-hecho-comunidad-ac/index.html"
AC_DATA_REL = "assets/data/ac-private-actor-de-facto-administration-v1.json"
MATERIAL_CONTROL_MODULE_REL = "assets/calificacion-2018-creditor-material-control-20260816.js"
AC_MANIFEST_REL = "publication-manifests/ac-community-de-facto-administration-2026-08-20.json"
MODULE_REL = "assets/cam-direct-instruction-shadow-admin-judicial-omission-20260823.js"
LOADER_REL = "assets/sitewide-discovery-nav-20260821.js"
SITEMAP_REL = "sitemap-criminal-engineering.xml"
GENERAL_SITEMAP_REL = "sitemap.xml"

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
        data = json.loads(text)
    except Exception as exc:
        errors.append(f"invalid JSON {rel}: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"JSON root must be an object: {rel}")
        return {}
    return data


def require_markers(rel: str, text: str, markers: list[str]) -> None:
    for marker in markers:
        if marker not in text:
            errors.append(f"{rel}: missing marker {marker!r}")


source = read(SOURCE_REL)
en = read(EN_REL)
es = read(ES_REL)
en_ac = read(EN_AC_REL)
es_ac = read(ES_AC_REL)
en_df = read(EN_DF_REL)
es_df = read(ES_DF_REL)
ac_data_text = read(AC_DATA_REL)
material_control_module = read(MATERIAL_CONTROL_MODULE_REL)
ac_manifest_text = read(AC_MANIFEST_REL)
module = read(MODULE_REL)
loader = read(LOADER_REL)
sitemap_text = read(SITEMAP_REL)
general_sitemap_text = read(GENERAL_SITEMAP_REL)
data = load_json(DATA_REL)
manifest = load_json(MANIFEST_REL)
probe = load_json(PROBE_REL)

require_markers(
    SOURCE_REL,
    source,
    [
        "CANONICAL CRIMINAL-ALLEGATION / EVIDENCE-STATUS / PUBLICATION-CONTROL RECORD",
        "These are **Gil Marer / Aweswell criminal allegations**, not judicial findings.",
        "Direct instruction and coordinated implementation.",
        "Criminal approval or ratification by the insolvency administrator.",
        "Judicial omission / prevarication allegation.",
        "The controlling identity rule is `IDENTITY_CONTROL_LAURA_PATRICIA_ACOSTA_MATOS_23AUG2026.md`.",
        "The filed complaint amendment alleges that Antonio Cogolludo and Laura Patricia Acosta Matos",
        "the repository’s established abbreviation **LPAM** refers to **Laura Patricia Acosta Matos**",
        "No public page may state as an established fact that Laura Patricia Acosta Matos was physically present",
        "provisional dismissal of the 2018 criminal proceedings and appellate confirmation",
        "15 February 2018 — CAM recognised as credit holder",
        "Each alleged act must be classified under the criminal provision in force when it was committed",
        "knowingly issuing an unjust judicial resolution",
        "refusal to judge without legal cause",
        "malicious delay intended to achieve an illegitimate purpose",
        "The evidence is **not yet sufficient to publish those allegations as proved criminal facts**.",
        "Silence is not admission.",
    ],
)

require_markers(
    EN_REL,
    en,
    [
        f'lang="en"',
        f'href="{BASE_URL}{EN_ROUTE}"',
        f'hreflang="en" href="{BASE_URL}{EN_ROUTE}"',
        f'hreflang="es" href="{BASE_URL}{ES_ROUTE}"',
        f'hreflang="x-default" href="{BASE_URL}{ES_ROUTE}"',
        "They are not judicial findings.",
        "DIRECT-INSTRUCTION ALLEGATION",
        "The allegation is affirmative approval or ratification—not silence alone.",
        "Gil alleges that the insolvency administrator criminally enabled, approved or ratified the 7 June operation",
        "Gil alleges omissionary judicial prevarication.",
        "“The judge did not grant the requested remedy” is not by itself prevarication.",
        "Laura Patricia Acosta Matos",
        "Attribution control.",
        "mandate, orders, knowledge, purpose and any criminal responsibility require independent proof",
        "The 2018 provisional dismissal and appellate confirmation remain prominently preserved.",
        "Provisional dismissal upheld",
        "judicial recognition on 15 February 2018",
        "subject to retroactive application of a later law more favourable to the accused under Criminal Code Article 2.2",
        "https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444",
        "https://www.boe.es/buscar/act.php?id=BOE-A-2010-10544#a236",
        "Right of reply.",
        "Silence is not admission.",
    ],
)

require_markers(
    ES_REL,
    es,
    [
        f'lang="es"',
        f'href="{BASE_URL}{ES_ROUTE}"',
        f'hreflang="en" href="{BASE_URL}{EN_ROUTE}"',
        f'hreflang="es" href="{BASE_URL}{ES_ROUTE}"',
        f'hreflang="x-default" href="{BASE_URL}{ES_ROUTE}"',
        "No son declaraciones judiciales.",
        "ALEGACIÓN DE INSTRUCCIÓN DIRECTA",
        "La alegación es de aprobación o ratificación afirmativa, no de mero silencio.",
        "Gil alega que el administrador concursal habilitó, aprobó o ratificó penalmente la operación de 7 de junio",
        "Gil alega prevaricación judicial por omisión.",
        "Que el juez no concediera la medida solicitada no constituye por sí solo prevaricación.",
        "Laura Patricia Acosta Matos",
        "Control de atribución.",
        "el mandato, las órdenes, el conocimiento, la finalidad y cualquier responsabilidad penal requieren prueba independiente",
        "el archivo provisional de 2018 y su confirmación en apelación",
        "Archivo provisional confirmado",
        "reconocimiento judicial el 15 febrero 2018",
        "sin perjuicio de la aplicación retroactiva de la ley posterior más favorable al reo conforme al artículo 2.2 CP",
        "https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444",
        "https://www.boe.es/buscar/act.php?id=BOE-A-2010-10544#a236",
        "Derecho de respuesta.",
        "El silencio no es admisión.",
    ],
)

require_markers(
    EN_AC_REL,
    en_ac,
    [
        "This page does not establish corruption, collusion or unlawful intent.",
        "separately preserves Gil Marer's attributed approval, enablement, ratification or legally equivalent omission allegation",
        "it is an allegation for investigation, not a finding.",
    ],
)

require_markers(
    ES_AC_REL,
    es_ac,
    [
        "Esta página no establece delito",
        "preserva separadamente la alegación atribuida a Gil Marer de aprobación, facilitación, ratificación u omisión jurídicamente equivalente",
        "es una alegación para investigar, no una declaración judicial.",
    ],
)

for rel, text, marker in [
    (EN_DF_REL, en_df, "15 February 2018: formal Promontoria-to-CAM holder substitution"),
    (EN_DF_REL, en_df, 'href="../lpb-solvency-record/"'),
    (ES_DF_REL, es_df, "15/02/2018: modificación formal del titular Promontoria→CAM"),
    (ES_DF_REL, es_df, 'href="../expediente-solvencia-lpb/"'),
    (AC_DATA_REL, ac_data_text, '"event": "2018-02-15 Article 97 bis order"'),
    (MATERIAL_CONTROL_MODULE_REL, material_control_module, "20 OCT 2017 → 15 FEB 2018"),
    (AC_MANIFEST_REL, ac_manifest_text, "The 15 February 2018 Article 97 bis order changed the credit holder to CAM"),
]:
    if marker not in text:
        errors.append(f"{rel}: corrected 15-Feb-2018 creditor-substitution marker missing")

for rel, text, prohibited in [
    (SOURCE_REL, source, "8 February 2018"),
    (EN_REL, en, "judicial recognition on 8 February 2018"),
    (ES_REL, es, "reconocimiento judicial el 8 febrero 2018"),
    (EN_AC_REL, en_ac, "This page does not allege corruption, collusion or unlawful intent."),
    (EN_DF_REL, en_df, "8 February 2018: formal Promontoria-to-CAM holder substitution"),
    (ES_DF_REL, es_df, "08/02/2018: modificación formal del titular Promontoria→CAM"),
    (AC_DATA_REL, ac_data_text, '"event": "2018-02-08 Article 97 bis order"'),
    (MATERIAL_CONTROL_MODULE_REL, material_control_module, "8 FEB 2018"),
    (AC_MANIFEST_REL, ac_manifest_text, "The 8 February 2018 Article 97 bis order changed the credit holder to CAM"),
]:
    if prohibited in text:
        errors.append(f"{rel}: forbidden or superseded marker repeated: {prohibited!r}")

require_markers(
    MODULE_REL,
    module,
    [
        'data-cam-criminal-lead="20260823"',
        "CAM / JDAM / FMMM / relevant Laura actor",
        "Attribution control — Laura Patricia Acosta Matos",
        "The 2018 criminal proceedings were provisionally dismissed and that result was upheld on appeal.",
        "Allegation ≠ adjudicated finding",
        "CAM / JDAM / FMMM / actor Laura pertinente",
        "Control de atribución — Laura Patricia Acosta Matos",
        "Las diligencias penales de 2018 fueron archivadas provisionalmente y el resultado se confirmó en apelación.",
        "Alegación ≠ declaración judicial",
    ],
)

require_markers(
    LOADER_REL,
    loader,
    [
        "CAM-DIRECT-INSTRUCTION-SHADOW-ADMIN-JUDICIAL-OMISSION-ROUTE-LOADER-20260823",
        "cam-direct-instruction-shadow-admin-judicial-omission-20260823.js?v=20260823a",
        "data-cam-direct-instruction-loader",
        "/en/sun-park-takeover-7-june-2018/",
        "/es/toma-control-sun-park-7-junio-2018/",
    ],
)

for sitemap_rel, current_sitemap_text in [
    (SITEMAP_REL, sitemap_text),
    (GENERAL_SITEMAP_REL, general_sitemap_text),
]:
    if not current_sitemap_text:
        continue
    try:
        root = ET.fromstring(current_sitemap_text)
        namespace = {
            "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xhtml": "http://www.w3.org/1999/xhtml",
        }
        locations = {
            element.text.strip()
            for element in root.findall("sm:url/sm:loc", namespace)
            if element.text
        }
        for expected in {f"{BASE_URL}{EN_ROUTE}", f"{BASE_URL}{ES_ROUTE}"}:
            if expected not in locations:
                errors.append(f"{sitemap_rel}: missing canonical location {expected}")
        expected_alternates = {
            "en": f"{BASE_URL}{EN_ROUTE}",
            "es": f"{BASE_URL}{ES_ROUTE}",
            "x-default": f"{BASE_URL}{ES_ROUTE}",
        }
        for url in root.findall("sm:url", namespace):
            loc = url.find("sm:loc", namespace)
            if loc is None or not loc.text or loc.text.strip() not in expected_alternates.values():
                continue
            alternates = {
                link.get("hreflang"): link.get("href")
                for link in url.findall("xhtml:link", namespace)
            }
            if alternates != expected_alternates:
                errors.append(f"{sitemap_rel}: CAM route alternate map mismatch: {alternates}")
    except ET.ParseError as exc:
        errors.append(f"invalid XML {sitemap_rel}: {exc}")

if data.get("schema_version") != "1.0":
    errors.append("dataset schema_version must be 1.0")
if data.get("publication_id") != PUBLICATION_ID:
    errors.append("dataset publication_id mismatch")
if data.get("control_marker") != CONTROL_MARKER:
    errors.append("dataset control_marker mismatch")
if data.get("status") != "DRAFT_ATTRIBUTED_CRIMINAL_ALLEGATION_NOT_FINDING":
    errors.append("dataset status boundary mismatch")
if data.get("canonical_source") != SOURCE_REL:
    errors.append("dataset canonical source mismatch")
if data.get("public_routes") != {"en": EN_ROUTE, "es": ES_ROUTE}:
    errors.append("dataset bilingual route map mismatch")

position = data.get("controlling_position", {})
if position.get("evidence_sufficiency") != "SUFFICIENT_TO_MAKE_PRESERVE_AND_REQUEST_INVESTIGATION":
    errors.append("dataset evidence-sufficiency boundary mismatch")
for key in ["criminal_guilt_adjudicated", "collective_guilt_presumed"]:
    if position.get(key) is not False:
        errors.append(f"dataset controlling-position boundary mismatch: {key}")
for key in ["presumption_of_innocence_preserved", "right_of_reply_preserved"]:
    if position.get(key) is not True:
        errors.append(f"dataset controlling-position safeguard mismatch: {key}")

lanes = data.get("allegation_lanes", [])
if not isinstance(lanes, list) or len(lanes) != 3:
    errors.append("dataset must contain exactly three allegation lanes")
else:
    expected_ids = {"CAM-LEAD-01", "CAM-LEAD-02", "CAM-LEAD-03"}
    if {lane.get("id") for lane in lanes if isinstance(lane, dict)} != expected_ids:
        errors.append("dataset allegation-lane ids mismatch")
    for lane in lanes:
        if not isinstance(lane, dict):
            errors.append("dataset allegation lane must be an object")
            continue
        if lane.get("attributed") is not True:
            errors.append(f"{lane.get('id')}: allegation must be expressly attributed")
        if lane.get("criminal_finding") is not False:
            errors.append(f"{lane.get('id')}: allegation must not be a criminal finding")
        if not lane.get("unresolved_bridges"):
            errors.append(f"{lane.get('id')}: unresolved evidential bridges are required")

evidence_types = data.get("evidence_types", [])
if not isinstance(evidence_types, list) or len(evidence_types) < 10:
    errors.append("dataset evidence-type coverage is unexpectedly narrow")

identity = data.get("identity_control", {})
identity_expected = {
    "filed_7_june_amendment_name": "Laura Patricia Acosta Matos",
    "repository_lpam_name": "Laura Patricia Acosta Matos",
    "name_controlled_as_typographical_error": True,
    "laura_patricia_physical_presence_established": False,
    "laura_patricia_direct_instruction_established": False,
}
for key, expected in identity_expected.items():
    if identity.get(key) != expected:
        errors.append(f"dataset identity-control mismatch: {key}")

contrary = data.get("contrary_record", {})
for key in [
    "provisional_dismissal_2018",
    "appellate_confirmation",
    "administrator_denied_main_lock_takeover_instruction",
    "administrator_described_narrower_access_authority",
    "later_adjudication_legally_distinct_and_non_retroactive",
]:
    if contrary.get(key) is not True:
        errors.append(f"dataset contrary-record safeguard mismatch: {key}")
if contrary.get("conviction_from_physical_entry_complaint") is not False:
    errors.append("dataset must not represent the physical-entry complaint as a conviction")

boundaries = data.get("publication_boundaries", {})
for key in [
    "criminal_guilt_as_established",
    "direct_instruction_as_adjudicated_fact",
    "administrator_criminal_approval_as_adjudicated_fact",
    "judicial_prevarication_as_established",
    "treat_source_typo_as_separate_actor",
    "infer_later_evidence_was_before_earlier_actor",
    "treat_valid_credit_as_whole_hotel_title",
    "treat_later_adjudication_as_retroactive_authority",
    "publish_raw_private_evidence",
]:
    if boundaries.get(key) is not False:
        errors.append(f"dataset publication boundary mismatch: {key}")
for key in ["state_allegations_as_attributed", "preserve_strongest_defences", "preserve_right_of_reply"]:
    if boundaries.get(key) is not True:
        errors.append(f"dataset publication safeguard mismatch: {key}")

statutes = {
    item.get("provision")
    for item in data.get("legal_boundaries", {}).get("statutory_tests", [])
    if isinstance(item, dict)
}
required_statutes = {
    "CP 2.2",
    "CP 11",
    "CP 12",
    "CP 31",
    "CP 251",
    "CP 252",
    "CP 435.4",
    "CP 446",
    "CP 447",
    "CP 448",
    "CP 449",
    "CP 455",
    "CC 1859",
    "CC 1876",
    "LH 104",
    "LEC 690",
    "LECrim 641",
    "LSC 236.3",
}
if statutes != required_statutes:
    errors.append(f"dataset statutory-control set mismatch: {sorted(statutes)}")

for rel in data.get("controlled_sources", []):
    if not isinstance(rel, str) or not (ROOT / rel).is_file():
        errors.append(f"dataset controlled source missing: {rel!r}")

if manifest.get("publication_id") != PUBLICATION_ID:
    errors.append("manifest publication_id mismatch")
if manifest.get("control_marker") != CONTROL_MARKER:
    errors.append("manifest control_marker mismatch")
manifest_state = manifest.get("current_state")
if manifest_state not in {"DRAFT", "DELETION_SAFE"}:
    errors.append(f"manifest current_state is not controlled: {manifest_state!r}")
if manifest.get("expected_routes") != {"en": [EN_REL], "es": [ES_REL]}:
    errors.append("manifest expected bilingual routes mismatch")
for rel in manifest.get("expected_source_files", []):
    if not isinstance(rel, str) or not (ROOT / rel).is_file():
        errors.append(f"manifest expected source missing: {rel!r}")

superseding_identity = manifest.get("superseding_identity_control", {})
if superseding_identity.get("identity") != "Laura Patricia Acosta Matos":
    errors.append("manifest superseding identity mismatch")
if superseding_identity.get("source_typo_creates_separate_actor") is not False:
    errors.append("manifest must not treat the source typo as a separate actor")
if superseding_identity.get("control_file") != "archive/IDENTITY_CONTROL_LAURA_PATRICIA_ACOSTA_MATOS_23AUG2026.md":
    errors.append("manifest superseding identity control file mismatch")

if manifest_state == "DELETION_SAFE":
    expected_merge = "c2f77661371384a79fb7e0caaef79c6345cabecf"
    if manifest.get("deletion_status") != "DELETION_SAFE_WITH_OPEN_EVIDENCE":
        errors.append("manifest deletion status mismatch")
    if manifest.get("merge_sha") != expected_merge:
        errors.append("manifest exact merge SHA mismatch")
    if manifest.get("validation", {}).get("status") != "CI_GREEN_LIVE_VERIFIED":
        errors.append("manifest CI/live validation state mismatch")
    if manifest.get("deployment_evidence", {}).get("exact_merge_sha") != expected_merge:
        errors.append("manifest deployment evidence is not tied to the exact merge SHA")
    if manifest.get("deployment_evidence", {}).get("workflow_run_id") != 32609842885:
        errors.append("manifest GitHub Pages run mismatch")
    if manifest.get("live_verification_evidence", {}).get("status") != "PASS":
        errors.append("manifest live verification is not PASS")
    if manifest.get("deletion_record", {}).get("status") != "DELETION_SAFE_WITH_OPEN_EVIDENCE":
        errors.append("manifest deletion record mismatch")
    if not set(manifest.get("expected_live_urls", [])).issubset(set(manifest.get("live_urls", []))):
        errors.append("manifest live URL set does not include every expected public URL")

    if probe.get("publication_id") != PUBLICATION_ID:
        errors.append("deployment probe publication_id mismatch")
    if probe.get("source_merge_sha") != expected_merge:
        errors.append("deployment probe exact merge SHA mismatch")
    if probe.get("pages_run_id") != 32609842885:
        errors.append("deployment probe Pages run mismatch")
    if probe.get("verified") is not True:
        errors.append("deployment probe must be verified")
    probe_checks = probe.get("checks", [])
    if not isinstance(probe_checks, list) or len(probe_checks) != 11:
        errors.append("deployment probe must contain exactly 11 controlled readbacks")
    else:
        for check in probe_checks:
            if check.get("status") != 200 or check.get("missing_markers") != []:
                errors.append(f"deployment probe failed control: {check.get('kind')!r}")
        probe_by_kind = {check.get("kind"): check for check in probe_checks}
        exact_source_map = {"criminal_sitemap": SITEMAP_REL}
        # The probe is immutable evidence of the earlier deployment. Current
        # canonical pages, data, runtime and update surfaces may be superseded
        # by a later controlled publication; their current content is validated
        # above rather than falsely required to match an historical byte hash.
        for kind, rel in exact_source_map.items():
            expected_sha = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
            if probe_by_kind.get(kind, {}).get("sha256") != expected_sha:
                errors.append(f"deployment probe SHA-256 mismatch for {kind}: {rel}")

safety = manifest.get("publication_safety", {})
for key in [
    "raw_private_emails_committed",
    "private_message_ids_committed",
    "privileged_advice_committed",
    "unnecessary_personal_identifiers_committed",
    "criminal_guilt_stated_as_final",
    "direct_instruction_stated_as_adjudicated",
    "administrator_criminal_approval_stated_as_adjudicated",
    "judicial_prevarication_stated_as_established",
    "source_typo_treated_as_separate_actor",
]:
    if safety.get(key) is not False:
        errors.append(f"manifest publication-safety mismatch: {key}")

# Public assets must not expose private addresses or connector identifiers.
for rel, text in [(EN_REL, en), (ES_REL, es), (MODULE_REL, module), (DATA_REL, read(DATA_REL))]:
    if re.search(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", text):
        errors.append(f"{rel}: private email address exposed")
    for forbidden in ["message_id", "thread_id", "drive_item_id", "44700629Z"]:
        if forbidden.lower() in text.lower():
            errors.append(f"{rel}: private source identifier exposed: {forbidden}")
    for forbidden_identity in ["Laura Isabel", "Laura Matos"]:
        if forbidden_identity in text:
            errors.append(f"{rel}: superseded public identity form exposed: {forbidden_identity}")

if errors:
    print("CAM CREDITOR-CONTROL CRIMINAL LEAD: FAIL", file=sys.stderr)
    for error in errors:
        print(f" - {error}", file=sys.stderr)
    raise SystemExit(1)

print(
    "CAM CREDITOR-CONTROL CRIMINAL LEAD: PASS "
    f"({len(lanes)} attributed allegation lanes; {len(evidence_types)} evidence types; "
    f"{len(required_statutes)} statutory controls)"
)

#!/usr/bin/env python3
"""Load the one reviewed Lanzarote filing without exposing private registry IDs."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

INPUT = "ops/continuity/LANZAROTE_18735_2026_REGAGE_FILED_CANON_AUDIT_20261123.json"
CONTROL = "PD-LZ-URIP-18735-CANON-AUDIT-20261123-001/REGAGE-20261123-01"
SOURCE_PREFIX = "REGISTERED-LANZAROTE-18735-20261123:"
EVENT_ID = "PD-SP-EVT-0607"
SOURCE_KEY = "LANZAROTE-18735-FILING-20261123"
FIELDS = {"source_key", "event_id", "date", "reference", "office", "workspace_id", "attachment_count", "attachment_pages", "attachment_hashes_verified", "purpose_en", "purpose_es"}
PRIVATE = re.compile(r"(?i)REGAGE[0-9]{2}e[0-9]+|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|https?://|\b(?:[XYZ][0-9]{7}[A-Z]|[0-9]{8}[A-Z])\b")
EXCLUSION_BOUNDARY = {
    "en": "The source-verified Lanzarote 18735/2026 transparency complaint remains in the canonical communications and REG-AGE registers. It assigns no prosecution proceeding and is excluded from this specialist Fiscalía graph. Its conditional article 262 LECrim request does not establish an offence, investigation, admission or merits finding.",
    "es": "La reclamación de transparencia de Lanzarote 18735/2026, verificada con su fuente, permanece en los registros canónicos de comunicaciones y REG-AGE. No asigna un procedimiento fiscal y se excluye de este grafo especializado de Fiscalía. La petición condicionada del artículo 262 LECrim no acredita delito, investigación, admisión ni decisión de fondo."
}

def load_filing_events(root: Path, receipt_boundary: dict) -> list[dict]:
    raw = (root / INPUT).read_bytes()
    data = json.loads(raw)
    if data.get("control_id") != CONTROL or data.get("control_date") != "2026-11-23":
        raise ValueError("Lanzarote filing control identity/date drift")
    items = data.get("items")
    if not isinstance(items, list) or len(items) != 1 or not isinstance(items[0], dict):
        raise ValueError("Lanzarote cohort requires exactly one reviewed filing descriptor")
    item = items[0]
    if set(item) != FIELDS:
        raise ValueError("Lanzarote descriptor fields differ from the minimised contract")
    expected = {"source_key": SOURCE_KEY, "event_id": EVENT_ID, "date": "2026-11-23", "reference": "Cabildo Decree 2026-8922 / information-access file 18735/2026", "office": "Comisionado de Transparencia y Acceso a la Información Pública", "workspace_id": "PD-WS-20260901-0002", "attachment_count": 5, "attachment_pages": 85, "attachment_hashes_verified": True}
    if any(item.get(key) != value or type(item.get(key)) is not type(value) for key, value in expected.items()):
        raise ValueError("Lanzarote reviewed identity, date, destination or package drift")
    if any(not isinstance(item.get(key), str) or not item[key].strip() for key in ("purpose_en", "purpose_es")):
        raise ValueError("Lanzarote requires both public-safe language summaries")
    if PRIVATE.search(json.dumps(data, ensure_ascii=False)):
        raise ValueError("Lanzarote public descriptor contains a private identifier or locator")
    verification = data.get("verification", {})
    if verification.get("official_registration_receipt_reviewed") is not True or verification.get("attachment_fingerprints_exact_matches") != 5 or verification.get("registration_form_fields_match") is not True:
        raise ValueError("Lanzarote receipt, attachment or form verification is not established")
    if data.get("master_link_state") != "OPEN" or data.get("requested_relief", {}).get("established_criminal_finding_asserted") is not False:
        raise ValueError("Lanzarote master-reference or criminal-finding boundary drift")
    limit = "Registration does not itself establish entry in the Commissioner's own register, admission, internal allocation, incorporation, examination, a Commissioner claim reference, relief or a merits decision. The conditional article 262 request is not an established criminal finding. This complaint remains separate from R865/2026 and Decree 2026-7000 / file 13817/2026."
    limit_es = "El registro no acredita por sí solo entrada en el registro propio del Comisionado, admisión, reparto interno, incorporación, examen, referencia de reclamación asignada, estimación ni decisión de fondo. La petición condicionada del artículo 262 no equivale a una responsabilidad penal declarada. La reclamación permanece separada de R865/2026 y del Decreto 2026-7000 / expediente 13817/2026."
    return [{
        "event_id": EVENT_ID, "cohort": "CURATED_SOURCE_PROVED_EVENT", "layer": "FORMAL_REGISTRATION",
        "source_key": SOURCE_PREFIX + SOURCE_KEY,
        "record_type": "REGISTRATION_RECEIPT", "event_date": item["date"],
        "direction": "OUTBOUND_TO_INSTITUTION", "channel": "REGAGE", "office": item["office"],
        "official_reference": item["reference"], "annex_count": item["attachment_count"],
        "matter_references": [item["reference"], CONTROL, item["workspace_id"]],
        "master_ids": [], "master_link_state": "OPEN",
        "source_integrity": {"status": "RECEIPT_VERIFIED_PUBLIC_SAFE_DERIVATIVE", "repository_anchor": INPUT, "sha256": hashlib.sha256(raw).hexdigest()},
        "evidence_state": deepcopy(receipt_boundary),
        "public_summary": item["purpose_en"], "public_summary_es": item["purpose_es"],
        "proves": [item["purpose_en"], "The exact registry identifier and native receipt remain in authorised private custody; the opaque project key is not an official registration number."],
        "proves_es": item["purpose_es"] + " El identificador registral exacto y el justificante nativo permanecen en custodia privada; la referencia opaca del proyecto no es un número registral oficial.",
        "does_not_prove": [limit], "does_not_prove_es": limit_es,
        "canonical_anchor_en": "en/institutional-records/#communication-" + EVENT_ID,
        "canonical_anchor_es": "es/registros-institucionales/#communication-" + EVENT_ID,
        "attribution_state": "NO_PERSON_ATTRIBUTED_IN_PUBLIC_REGISTER", "linked_transport_event_ids": [],
        "transport_link_state": "REGISTRATION_RECEIPT_SEPARATE_FROM_ANY_EMAIL_TRANSPORT",
        "proof_level": "REGISTRATION_RECEIPT_VERIFIED_AND_ATTACHMENT_HASHES_VERIFIED",
        "criminal_responsibility_transfer": False, "public_derivative_state": "PUBLIC_SAFE_MINIMISED_DERIVATIVE"
    }]

def validated_filing_event_ids(events: list[dict], root: Path, receipt_boundary: dict) -> set[str]:
    """Match the full source object before excluding it from a specialist graph."""
    expected = {event["event_id"]: event for event in load_filing_events(root, receipt_boundary)}
    references = {event["official_reference"] for event in expected.values()}
    actual_rows = [event for event in events if str(event.get("source_key", "")).startswith(SOURCE_PREFIX) or event.get("event_id") in expected or event.get("official_reference") in references]
    if len(actual_rows) != 1 or {event["event_id"]: event for event in actual_rows} != expected:
        raise ValueError("Lanzarote filing source cohort mismatch")
    return set(expected)

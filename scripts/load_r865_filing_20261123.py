#!/usr/bin/env python3
"""Load exactly one public-safe R865 filing descriptor; preserve private receipt IDs."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

INPUT = "ops/continuity/R865_2026_REGAGE_FILED_CANON_AUDIT_20261123.json"
CONTROL = "PD-CANON-AUDIT-20261024-001/R865-REGAGE-20261123-01"
SOURCE_PREFIX = "REGISTERED-R865-20261123:"
EVENT_ID = "PD-SP-EVT-0606"
SOURCE_KEY = "R865-FILING-20261123"
FIELDS = {"source_key", "event_id", "date", "reference", "office", "master_id", "workspace_id", "attachment_count", "attachment_pages", "attachment_hashes_verified", "purpose_en", "purpose_es"}
PRIVATE = re.compile(r"(?i)REGAGE[0-9]{2}e[0-9]+|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|https?://|\b(?:[XYZ][0-9]{7}[A-Z]|[0-9]{8}[A-Z])\b")

def load_filing_events(root: Path, receipt_boundary: dict) -> list[dict]:
    raw = (root / INPUT).read_bytes()
    data = json.loads(raw)
    if data.get("control_id") != CONTROL or data.get("control_date") != "2026-11-23":
        raise ValueError("R865 filing control identity/date drift")
    items = data.get("items")
    if not isinstance(items, list) or len(items) != 1 or not isinstance(items[0], dict):
        raise ValueError("R865 cohort requires exactly one reviewed filing descriptor")
    item = items[0]
    if set(item) != FIELDS:
        raise ValueError("R865 descriptor fields differ from the minimised contract")
    expected = {"source_key": SOURCE_KEY, "event_id": EVENT_ID, "date": "2026-11-23", "reference": "R865/2026 / RDR2026000865", "office": "Comisionado de Transparencia y Acceso a la Información Pública", "master_id": "LZ-TRA-028", "workspace_id": "PD-WS-20260901-0002", "attachment_count": 5, "attachment_pages": 40, "attachment_hashes_verified": True}
    if any(item.get(key) != value or type(item.get(key)) is not type(value) for key, value in expected.items()):
        raise ValueError("R865 reviewed identity, date, destination or package drift")
    if any(not isinstance(item.get(key), str) or not item[key].strip() for key in ("purpose_en", "purpose_es")):
        raise ValueError("R865 requires both public-safe language summaries")
    if PRIVATE.search(json.dumps(item, ensure_ascii=False)):
        raise ValueError("R865 public descriptor contains a private identifier or locator")
    verification = data.get("verification", {})
    if verification.get("official_registration_receipt_reviewed") is not True or verification.get("attachment_fingerprints_exact_matches") != 5:
        raise ValueError("R865 receipt/five-fingerprint verification is not established")
    limit = "The filing does not itself establish reopening, admission, incorporation, examination, disclosure, acceptance of allegations or a decision on the merits. The 5 October withdrawal/archive remains historical evidence."
    limit_es = "El registro no acredita por sí solo reapertura, admisión, incorporación, examen, entrega de información, aceptación de alegaciones ni decisión de fondo. El desistimiento y archivo de 5 de octubre se conserva como antecedente."
    return [{
        "event_id": EVENT_ID, "cohort": "CURATED_SOURCE_PROVED_EVENT", "layer": "FORMAL_REGISTRATION",
        "source_key": SOURCE_PREFIX + SOURCE_KEY,
        "record_type": "REGISTRATION_RECEIPT", "event_date": item["date"],
        "direction": "OUTBOUND_TO_INSTITUTION", "channel": "REGAGE", "office": item["office"],
        "official_reference": item["reference"], "annex_count": item["attachment_count"],
        "matter_references": [item["reference"], item["master_id"], item["workspace_id"]],
        "master_ids": [item["master_id"]], "master_link_state": "RESOLVED",
        "source_integrity": {"status": "RECEIPT_VERIFIED_PUBLIC_SAFE_DERIVATIVE", "repository_anchor": INPUT, "sha256": hashlib.sha256(raw).hexdigest()},
        "evidence_state": deepcopy(receipt_boundary),
        "public_summary": item["purpose_en"], "public_summary_es": item["purpose_es"],
        "proves": [item["purpose_en"], "The exact registration identifier and original receipt remain in authorised private custody; the opaque public source key is not a replacement official registration number."],
        "proves_es": item["purpose_es"] + " El identificador registral exacto y el justificante original permanecen en custodia privada; la referencia pública opaca no sustituye el número oficial.",
        "does_not_prove": [limit], "does_not_prove_es": limit_es,
        "canonical_anchor_en": "en/institutional-records/#communication-" + EVENT_ID,
        "canonical_anchor_es": "es/registros-institucionales/#communication-" + EVENT_ID,
        "attribution_state": "NO_PERSON_ATTRIBUTED_IN_PUBLIC_REGISTER", "linked_transport_event_ids": [],
        "transport_link_state": "REGISTRATION_RECEIPT_SEPARATE_FROM_ANY_EMAIL_TRANSPORT",
        "proof_level": "REGISTRATION_RECEIPT_VERIFIED_AND_ATTACHMENT_HASHES_VERIFIED",
        "criminal_responsibility_transfer": False, "public_derivative_state": "PUBLIC_SAFE_MINIMISED_DERIVATIVE"
    }]

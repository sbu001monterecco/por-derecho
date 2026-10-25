#!/usr/bin/env python3
"""Load the finite, receipt-verified October Madrid/CTBG filing cohort.

The input is a minimised public descriptor, not a second event register or a
native receipt archive. The existing event namespace and receipt boundary stay
authoritative. Its fixed reference set and explicit event descriptors prevent a
changed denominator from silently admitting an unrelated filing.
"""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

from load_completed_filings_20260921 import normalise_presented_local

INPUT = "assets/data/institutional-communications-20261025.json"
CONTROL = "PD-MADRID-CTBG-REGISTERED-20261025"
SOURCE_PREFIX = "REGISTERED-20261025:"
EXPECTED = {
    "REGAGE26e00091776746": ("2026-10-24", "J00001430"),
    "REGAGE26e00091777235": ("2026-10-24", "J00001430"),
    "REGAGE26e00091777533": ("2026-10-24", "J00001430"),
    "REGAGE26e00091778502": ("2026-10-24", "EA0040111"),
    "REGAGE26e00091804140": ("2026-10-25", "J00001430"),
    "REGAGE26e00091804303": ("2026-10-25", "EA0040111"),
}
REQUIRED_FIELDS = {
    "event_id", "reference", "date", "presented_literal", "registered_literal",
    "office", "dir3", "matter_references", "purpose_en", "purpose_es",
    "source_anchor", "source_control_sha256", "source_kind", "attachment_count", "attachment_hashes_verified",
}
OPTIONAL_FIELDS = {"limit_en", "limit_es", "source_pages"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PRIVATE_URL_RE = re.compile(r"(?i)https?://[^\s]*(?:drive\.google|docs\.google|mail\.google|gmail)[^\s]*")
EMAIL_RE = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")


def validate_items(items: object) -> list[dict]:
    if not isinstance(items, list) or len(items) != len(EXPECTED):
        raise ValueError("October filing cohort requires exactly six receipt descriptors")
    if any(not isinstance(item, dict) for item in items):
        raise ValueError("October filing descriptors must be objects")
    if {item.get("reference") for item in items} != set(EXPECTED):
        raise ValueError("October filing cohort reference set differs from the six reviewed receipts")
    if len({item.get("event_id") for item in items}) != len(EXPECTED):
        raise ValueError("October filing event identities must remain distinct")
    for item in items:
        if set(item) - REQUIRED_FIELDS - OPTIONAL_FIELDS or REQUIRED_FIELDS - set(item):
            raise ValueError("October filing descriptor fields differ from the minimised public contract")
        reference = item["reference"]
        date, dir3 = EXPECTED[reference]
        if not isinstance(item["event_id"], str) or not re.fullmatch(r"PD-SP-EVT-[0-9]{4}", item["event_id"]):
            raise ValueError(f"October filing event identity is invalid: {reference}")
        if (item["date"], item["dir3"]) != (date, dir3):
            raise ValueError(f"October filing date/destination drift: {reference}")
        presented = normalise_presented_local(item["presented_literal"])
        registered = normalise_presented_local(item["registered_literal"])
        if datetime.fromisoformat(presented).date().isoformat() != date:
            raise ValueError(f"Presentation date differs from the receipt event: {reference}")
        if datetime.fromisoformat(registered).date().isoformat() != date or registered < presented:
            raise ValueError(f"Registration precedes presentation or has another date: {reference}")
        if not isinstance(item["source_control_sha256"], str) or not SHA256_RE.fullmatch(item["source_control_sha256"]):
            raise ValueError(f"Source-control SHA-256 is missing or invalid: {reference}")
        if item["source_kind"] not in {"NATIVE_REGISTRY_RECEIPT", "COMPILED_RECEIPT_READ_COPY"}:
            raise ValueError(f"Receipt source kind is missing or invalid: {reference}")
        if item["source_kind"] == "COMPILED_RECEIPT_READ_COPY" and not re.fullmatch(r"[0-9]+-[0-9]+", str(item.get("source_pages", ""))):
            raise ValueError(f"Compiled receipt copy needs its controlling page range: {reference}")
        if item.get("source_pages") and not re.fullmatch(r"[0-9]+-[0-9]+", str(item["source_pages"])):
            raise ValueError(f"Receipt source page range is invalid: {reference}")
        count = item["attachment_count"]
        if type(count) is not int or not 0 <= count <= 5:
            raise ValueError(f"Receipt attachment count is invalid: {reference}")
        if type(item["attachment_hashes_verified"]) is not bool:
            raise ValueError(f"Attachment fingerprint verification must have an explicit boolean state: {reference}")
        if not isinstance(item["matter_references"], list) or not item["matter_references"] or len(item["matter_references"]) != len(set(item["matter_references"])):
            raise ValueError(f"Matter references must be a nonempty unique list: {reference}")
        anchor = item["source_anchor"]
        if not isinstance(anchor, str) or not anchor or ":" in anchor or anchor.startswith("/") or ".." in Path(anchor).parts:
            raise ValueError(f"Source anchor must remain a relative repository path: {reference}")
        for key in ("office", "purpose_en", "purpose_es"):
            if not isinstance(item[key], str) or not item[key].strip():
                raise ValueError(f"Public filing descriptor lacks {key}: {reference}")
        descriptor_text = json.dumps(item, ensure_ascii=False)
        if EMAIL_RE.search(descriptor_text) or PRIVATE_URL_RE.search(descriptor_text):
            raise ValueError(f"Private locator or direct email in public descriptor: {reference}")
    return items


def load_filing_events(root: Path, receipt_boundary: dict) -> list[dict]:
    raw = (root / INPUT).read_bytes()
    data = json.loads(raw)
    if data.get("control_id") != CONTROL or data.get("control_date") != "2026-10-25":
        raise ValueError("October filing descriptor control identity/date drift")
    items = validate_items(data.get("items"))
    input_sha256 = hashlib.sha256(raw).hexdigest()
    events = []
    for item in items:
        event_id, reference = item["event_id"], item["reference"]
        summary_en = f"Registered {reference}: {item['purpose_en']}"
        summary_es = f"Registrado {reference}: {item['purpose_es']}"
        event = {
            "event_id": event_id,
            "cohort": "CURATED_SOURCE_PROVED_EVENT",
            "layer": "FORMAL_REGISTRATION",
            "source_key": SOURCE_PREFIX + reference,
            "record_type": "REGISTRATION_RECEIPT",
            "event_date": item["date"],
            "presented_local": normalise_presented_local(item["presented_literal"]),
            "event_timestamp": normalise_presented_local(item["registered_literal"]),
            "source_timezone": "NOT_STATED; printed electronic-headquarters times retained without offset conversion",
            "direction": "OUTBOUND_TO_INSTITUTION",
            "channel": "REGAGE",
            "office": item["office"],
            "official_reference": reference,
            "recipient_dir3": item["dir3"],
            "annex_count": item["attachment_count"],
            "matter_references": deepcopy(item["matter_references"]),
            "source_integrity": {
                "status": "RECEIPT_VERIFIED_PUBLIC_SAFE_DERIVATIVE" if item["source_kind"] == "NATIVE_REGISTRY_RECEIPT" else "RECEIPT_READ_COPY_PUBLIC_SAFE_DERIVATIVE",
                "repository_anchor": item["source_anchor"],
                "sha256": input_sha256,
                "controlling_source_pdf_sha256": item["source_control_sha256"],
            },
            "evidence_state": deepcopy(receipt_boundary),
            "public_summary": summary_en,
            "public_summary_es": summary_es,
            "proves": [summary_en, "The retained receipt records the stated presentation and registration timestamps and destination.", "The controlling source is a native registry receipt." if item["source_kind"] == "NATIVE_REGISTRY_RECEIPT" else "This event is checked against a compiled receipt read copy; its control hash is not asserted to be the native receipt hash."],
            "proves_es": summary_es + " El justificante conservado registra las fechas y horas indicadas y el destino." + (" La fuente de control es el justificante registral nativo." if item["source_kind"] == "NATIVE_REGISTRY_RECEIPT" else " Se contrasta una copia de lectura compilada; su huella de control no se presenta como la huella del justificante nativo."),
            "does_not_prove": [item.get("limit_en", "The filing does not determine the underlying allegations."), "Registration does not establish downstream delivery, admission, incorporation, examination, opening of an investigation, criminal responsibility or merits."],
            "does_not_prove_es": item.get("limit_es", "La presentación no decide las alegaciones de fondo.") + " El registro no acredita entrega ulterior, admisión, incorporación, examen, incoación de investigación, responsabilidad penal ni el fondo.",
            "canonical_anchor_en": f"en/institutional-records/#communication-{event_id}",
            "canonical_anchor_es": f"es/registros-institucionales/#communication-{event_id}",
            "attribution_state": "NO_PERSON_ATTRIBUTED_IN_PUBLIC_REGISTER",
            "linked_transport_event_ids": [],
            "transport_link_state": "REGISTRATION_RECEIPT_SEPARATE_FROM_ANY_EMAIL_TRANSPORT",
            "proof_level": "REGISTRATION_RECEIPT_VERIFIED" if item["source_kind"] == "NATIVE_REGISTRY_RECEIPT" else "REGISTRATION_RECEIPT_READ_COPY_VERIFIED",
            "criminal_responsibility_transfer": False,
            "public_derivative_state": "PUBLIC_SAFE_MINIMISED_DERIVATIVE",
        }
        if item["attachment_hashes_verified"]:
            event["proves"].append("The listed attachment fingerprints match the retained submitted files.")
            event["proves_es"] += " Las huellas de los anexos indicados coinciden con los archivos presentados conservados."
            event["proof_level"] += "_AND_ATTACHMENT_HASHES_VERIFIED"
        else:
            event["does_not_prove"].append("No fresh byte-level verification of this receipt's submitted attachments is claimed by this descriptor.")
            event["does_not_prove_es"] += " Este descriptor no afirma una nueva comprobación de bytes de los anexos presentados con este justificante."
        if item.get("source_pages"):
            event["source_pages"] = item["source_pages"]
        events.append(event)
    return events

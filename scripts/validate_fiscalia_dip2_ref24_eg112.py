#!/usr/bin/env python3
"""Validate the DIP 2/2026, reference 24 and EG 112 public update."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

import fitz
from pypdf import PdfReader
from pypdf.generic import NullObject


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "evidence/fiscalia/eg-112-2026/public-pdfs/decreto-aclaracion-eg-112-2026-23ago2026-public-redacted.pdf"
TRANSCRIPT = ROOT / "evidence/fiscalia/eg-112-2026/full-text/decreto-aclaracion-eg-112-2026-23ago2026-public-transcription.md"
TRANSLATION = ROOT / "evidence/fiscalia/eg-112-2026/full-text/decreto-aclaracion-eg-112-2026-23ago2026-english-translation.md"
README = ROOT / "evidence/fiscalia/eg-112-2026/README.md"
REF24_README = ROOT / "evidence/judicial-governance/decanato-reference-24/README.md"
ES = ROOT / "es/fiscalia-dip-2-2026/index.html"
EN = ROOT / "en/fiscalia-dip-2-2026/index.html"
CLOSEOUT = ROOT / "docs/deletion-audits/2026-08-25-fiscalia-eg112-notification-cross-thread-closeout.md"
HANDOFF = ROOT / "ops/continuity/FISCALIA_EG112_IMMEDIATE_RESPONSE_GITHUB_HANDOFF_20260919.md"
ES_PROFESSIONAL = ROOT / "es/fiscalia-evidencia-profesional-pwc-grant-thornton-rsm/index.html"
EN_PROFESSIONAL = ROOT / "en/prosecutorial-professional-evidence-pwc-grant-thornton-rsm/index.html"
ROUTING = ROOT / "archive/FISCALIA_PROFESSIONAL_EVIDENCE_ROUTING_20AUG2026.md"
DISPATCH_CONTROL = ROOT / "archive/FISCALIA_NINE_OFFICE_DISPATCH_CONTROL_20AUG2026.md"
DISPATCH_REGISTER = ROOT / "archive/FISCALIA_NINE_OFFICE_DISPATCH_REGISTER_20AUG2026.csv"
SCAN_PROMPT = ROOT / "archive/PROMPT_FISCALIA_EMAIL_SCAN_AND_PERSONALISED_DRAFTING_20AUG2026.md"
COMMUNICATIONS_REGISTER = ROOT / "assets/data/institutional-communications-register-v1.json"
SEND_AUTH_RULE = ROOT / "EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md"
GMAIL_HISTORY_GATE = ROOT / "archive/PRE_SEND_GMAIL_PERSON_OUTLET_HISTORY_GATE_23AUG2026.md"
OUTBOUND_PROTOCOL = ROOT / "archive/OUTBOUND_EMAIL_COMMUNICATIONS_PROTOCOL_23AUG2026.md"
PWC_INDEX = ROOT / "assets/evidence/email-used-20260822/pwc-five-actors-plus-ac-2016-knowledge-checkpoint-ES.png"
SAN_TELMO_INDEX = ROOT / "assets/evidence/email-used-20260822/san-telmo-ricpe-sun-park-stamp-v1-ES.png"

EXPECTED = {
    PDF: "fe9111aca4aa4cc82627af6c97a8408e3ed5e3db9e0382a6e302783f281b6783",
    TRANSCRIPT: "edcbeb9ca68ff33b0dbd8cb4bc9442c30f63d0db1ad570c0c7d72c0222bb919a",
    TRANSLATION: "faee0700814b3ffbe309d47c2a5a2697833fac72ad2ca21e3d6272c8e78d9ebe",
}

EXPECTED_INDEXES = {
    PWC_INDEX: (
        "6b3dfac14865f8bd9cdaf6eda6b610ff67175a96761f9d5ab7a0819b935643bf",
        489_983,
    ),
    SAN_TELMO_INDEX: (
        "f50790d29a0dc55521e03693b9023d55241212bbb4fd78977187dbe8bf544add",
        827_315,
    ),
}

PUBLIC_SAFE_CONTROLS = (
    HANDOFF,
    CLOSEOUT,
    ES_PROFESSIONAL,
    EN_PROFESSIONAL,
    ROUTING,
    DISPATCH_CONTROL,
    DISPATCH_REGISTER,
    SCAN_PROMPT,
)

CANONICAL_EVENT_IDS = (
    "PD-SP-EVT-0125",
    "PD-SP-EVT-0126",
    "PD-SP-EVT-0127",
    "PD-SP-EVT-0136",
    "PD-SP-EVT-1030",
    "PD-SP-EVT-1031",
    "PD-SP-EVT-1044",
    "PD-SP-EVT-1045",
    "PD-SP-EVT-1046",
)

BANNED = (
    "@justiciaencanarias.org",
    "928306511",
    "Plaza de San Agustín",
    "***7368**",
    "AC Sector Público",
)

SPANISH_ID_PATTERN = re.compile(r"\b(?:\d{8}|[XYZ]\d{7})[A-Z]\b", flags=re.IGNORECASE)

EXPECTED_EVENT_FIELDS = {
    "PD-SP-EVT-0125": {
        "event_date": "2026-08-19",
        "record_type": "OFFICIAL_DECISION",
        "proof_level": "SIGNED_ACT_LOCATED",
    },
    "PD-SP-EVT-0126": {
        "event_date": "2026-08-23",
        "record_type": "OFFICIAL_DECISION",
        "proof_level": "SIGNED_CLARIFICATION_LOCATED",
    },
    "PD-SP-EVT-0127": {
        "event_date": "2026-08-25",
        "record_type": "OFFICIAL_NOTIFICATION",
        "proof_level": "OFFICIAL_NOTICE_LOCATED",
    },
    "PD-SP-EVT-0136": {
        "event_date": "2026-08-02",
        "record_type": "REGISTRATION_RECEIPT",
        "proof_level": "PRIMARY_REGISTRATION_RECEIPT_LOCATED; ONE_TO_ONE_PUBLIC_DESTINATION_LABEL_NORMALISATION_PENDING",
    },
    "PD-SP-EVT-1030": {
        "event_date": "2026-08-25",
        "record_type": "EMAIL_TRANSPORT",
        "proof_level": "SENT_EMAIL_LOCATED",
        "direction": "OUTBOUND_TO_INSTITUTION",
        "transport_state": "SENT_EMAIL_LOCATED",
    },
    "PD-SP-EVT-1031": {
        "event_date": "2026-08-25",
        "record_type": "EMAIL_TRANSPORT",
        "proof_level": "RECEIVED_EMAIL_LOCATED",
        "direction": "INBOUND_FROM_INSTITUTION",
        "transport_state": "RECEIVED_EMAIL_LOCATED",
    },
    "PD-SP-EVT-1044": {
        "event_date": "2026-08-20",
        "record_type": "EMAIL_TRANSPORT",
        "proof_level": "SENT_EMAIL_LOCATED",
        "direction": "OUTBOUND_TO_INSTITUTION",
        "transport_state": "SENT_EMAIL_LOCATED",
    },
    "PD-SP-EVT-1045": {
        "event_date": "2026-08-20",
        "record_type": "EMAIL_TRANSPORT",
        "proof_level": "SENT_EMAIL_LOCATED",
        "direction": "OUTBOUND_TO_INSTITUTION",
        "transport_state": "SENT_EMAIL_LOCATED",
    },
    "PD-SP-EVT-1046": {
        "event_date": "2026-08-20",
        "record_type": "EMAIL_TRANSPORT",
        "proof_level": "SENT_EMAIL_LOCATED",
        "direction": "OUTBOUND_TO_INSTITUTION",
        "transport_state": "SENT_EMAIL_LOCATED",
    },
    "PD-SP-EVT-1113": {
        "event_date": "2026-08-02",
        "record_type": "SELF_ARCHIVE_CONTROL",
        "proof_level": "SELF_ARCHIVE_CONTROL_NOT_AN_INSTITUTIONAL_SEND",
        "direction": "SELF_ARCHIVE_CONTROL",
        "transport_state": "SELF_ARCHIVE_CONTROL_NOT_AN_INSTITUTIONAL_SEND",
    },
}

EXPECTED_DISPATCH_HEADER = (
    "order",
    "destination",
    "function",
    "subject_category",
    "sent_date",
    "public_dispatch_reference",
    "attachment_categories",
    "video",
    "status",
)

EXPECTED_HANDOFF_BINDINGS = (
    "`PD-SP-EVT-0125` | Signed opening/archive decision dated 19 August 2026",
    "`PD-SP-EVT-0126` | Signed clarification decree dated 23 August 2026",
    "`PD-SP-EVT-0127` | Official notice received 25 August 2026 transmitting that decree",
    "`PD-SP-EVT-0136` | Primary 2 August REG-AGE receipt `REGAGE26e00070236067`",
    "`PD-SP-EVT-1030` | Outbound 25 August email transport; `SENT_EMAIL_LOCATED` only",
    "`PD-SP-EVT-1031` | Inbound 25 August email transport; `RECEIVED_EMAIL_LOCATED` only",
    "`PD-SP-EVT-1044` | Outbound 20 August email transport; `SENT_EMAIL_LOCATED` only",
    "`PD-SP-EVT-1045` | Outbound 20 August email transport; `SENT_EMAIL_LOCATED` only",
    "`PD-SP-EVT-1046` | Outbound 20 August routing/remittal email transport; `SENT_EMAIL_LOCATED` only",
    "`PD-SP-EVT-1113` | Linked 2 August receipt-family self-archive control; `SELF_ARCHIVE_CONTROL_NOT_AN_INSTITUTIONAL_SEND`",
)

FAILURES: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


for path, expected_hash in EXPECTED.items():
    require(path.is_file(), f"missing derivative: {path.relative_to(ROOT)}")
    if path.is_file():
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == expected_hash, f"hash mismatch for {path.relative_to(ROOT)}: {actual}")

for path, (expected_hash, expected_size) in EXPECTED_INDEXES.items():
    require(path.is_file(), f"missing explanatory index: {path.relative_to(ROOT)}")
    if path.is_file():
        data = path.read_bytes()
        actual_hash = hashlib.sha256(data).hexdigest()
        require(actual_hash == expected_hash, f"hash mismatch for {path.relative_to(ROOT)}: {actual_hash}")
        require(len(data) == expected_size, f"size mismatch for {path.relative_to(ROOT)}: {len(data)}")
        require(data.startswith(b"\x89PNG\r\n\x1a\n"), f"invalid PNG signature: {path.relative_to(ROOT)}")

if PDF.is_file():
    reader = PdfReader(PDF)
    require(len(reader.pages) == 3, "EG 112 public PDF must have three pages")
    acroform = reader.trailer["/Root"].get("/AcroForm")
    require(acroform is None or isinstance(acroform, NullObject), "EG 112 public PDF still has an AcroForm dictionary")
    for page_number, page in enumerate(reader.pages, start=1):
        widgets = [
            annotation
            for annotation in page.get("/Annots", [])
            if annotation.get_object().get("/Subtype") == "/Widget"
        ]
        require(not widgets, f"EG 112 public PDF page {page_number} contains a widget")
    fitz_document = fitz.open(PDF)
    pdf_text = "\n".join(page.get_text("text") for page in fitz_document)
    fitz_document.close()
    for banned in BANNED:
        require(banned.casefold() not in pdf_text.casefold(), f"private literal remains in PDF text: {banned}")
    require(not SPANISH_ID_PATTERN.search(pdf_text), "full Spanish identifier pattern remains in PDF text")

transcript = read(TRANSCRIPT)
normalized_transcript = " ".join(transcript.split())
for marker in (
    "Expediente gubernativo n.º 112/2026",
    "## Página 1 de 3",
    "## Página 2 de 3",
    "## Página 3 de 3",
    "No le falta razón al Sr. Marer",
    "Fiscalía Provincial de Las Palmas de Gran Canaria",
):
    require(
        " ".join(marker.split()) in normalized_transcript,
        f"transcription missing marker: {marker}",
    )
for banned in BANNED:
    require(banned.casefold() not in transcript.casefold(), f"private literal remains in transcription: {banned}")
require(not SPANISH_ID_PATTERN.search(transcript), "full Spanish identifier pattern remains in transcription")

translation = read(TRANSLATION)
normalized_translation = " ".join(translation.split())
for marker in (
    "Clarification Decree — Governmental File 112/2026",
    "## Page 1 of 3",
    "## Page 2 of 3",
    "## Page 3 of 3",
    "Mr Marer is not wrong",
    "Provincial Public Prosecutor's Office of Las Palmas de Gran Canaria",
):
    require(
        " ".join(marker.split()) in normalized_translation,
        f"English translation missing marker: {marker}",
    )
for banned in BANNED:
    require(banned.casefold() not in translation.casefold(), f"private literal remains in English translation: {banned}")
require(not SPANISH_ID_PATTERN.search(translation), "full Spanish identifier pattern remains in English translation")

readme = read(README)
for marker in ("EVID-2026-FISCALIA-EG112-ACLARACION-003", *EXPECTED.values()):
    require(marker in readme, f"EG 112 README missing marker: {marker}")

ref24 = read(REF24_README)
for marker in (
    "Later institutional references located on 25 August 2026",
    "CGPJ Promotor's agreement dated **10 July 2026**",
    "TSJC Government Secretariat's signed agreement dated **20 August 2026**",
    "remains unlocated",
):
    require(marker in ref24, f"reference-24 README missing marker: {marker}")

for path, markers in {
    ES: (
        'id="eg112-aclaracion"',
        "EVID-2026-FISCALIA-EG112-ACLARACION-003",
        "Auditoría de congruencia institucional",
        "Objeto real",
        "Integridad de la fuente",
        "no se representa como NIG ni como procedimiento confirmado",
        "Referencia expresa al «control n.º 24»",
        "tsj-canarias-exp-gub-38-2026/",
    ),
    EN: (
        'id="eg112-clarification"',
        "EVID-2026-FISCALIA-EG112-ACLARACION-003",
        "Institutional congruence audit",
        "Actual object",
        "Source integrity",
        "not represented as a NIG or confirmed proceeding",
        "Express reference to “control no. 24”",
        "tsj-canarias-exp-gub-38-2026/",
    ),
}.items():
    page = read(path)
    for marker in markers:
        require(
            marker.casefold() in page.casefold(),
            f"{path.relative_to(ROOT)} missing marker: {marker}",
        )
    require(PDF.name in page, f"{path.relative_to(ROOT)} does not link the EG 112 PDF")
    require(TRANSCRIPT.name in page, f"{path.relative_to(ROOT)} does not link the EG 112 transcription")
require(TRANSLATION.name in read(EN), "English page does not link the complete EG 112 English translation")

closeout = read(CLOSEOUT)
for marker in (
    "Cross-thread continuity and deletion audit — Fiscalía EG 112/2026 notification",
    "Controlling institutional contradiction map",
    "Office-level attribution rule",
    "Procedure and module separation",
    "Privacy and evidence-custody lock",
    "Future-thread restart order",
    "FISCALIA_EG112_IMMEDIATE_RESPONSE_GITHUB_HANDOFF_20260919.md",
):
    require(marker in closeout, f"EG 112 closeout missing marker: {marker}")

for path, markers in {
    SEND_AUTH_RULE: (
        "SEND STATUS: PREPARED — NOT SENT.",
        "pagination-complete dual Gmail history gate",
        "PREPARED → AUTHORIZED → SENT → VERIFIED",
    ),
    GMAIL_HISTORY_GATE: (
        "PAGINATION = EXHAUSTED / TOKEN REMAINS",
        "SEND STATUS: BLOCKED — PERSON/ORGANISATION GMAIL HISTORY GATE INCOMPLETE.",
        "Every search must be paginated until the connector returns no continuation or next-page token.",
    ),
    OUTBOUND_PROTOCOL: (
        "PERSON + ORGANISATION GMAIL HISTORY GATE PASSED",
        "EXACT OUTBOUND PACKAGE PRESENTED TO USER",
        "USER FINAL APPROVAL",
        "SEND STATUS: NOT AUTHORISED / AUTHORISED / SENT / SENT + VERIFIED",
    ),
}.items():
    policy = read(path)
    normalized_policy = " ".join(policy.split()).casefold()
    for marker in markers:
        require(
            " ".join(marker.split()).casefold() in normalized_policy,
            f"{path.relative_to(ROOT)} missing controlling marker: {marker}",
        )

handoff = read(HANDOFF)
normalized_handoff = " ".join(handoff.split()).casefold()
for marker in (
    "GITHUB_ACTIVE",
    "BLOCKED_PENDING_ADDITIVE_RECONCILIATION",
    "SEND STATUS: PREPARED — NOT SENT",
    "BLOCKED — FRESH PAGINATION-COMPLETE GMAIL HISTORY GATE REQUIRED",
    "FILING STATUS: PROPOSED — NOT DRAFTED / NOT FILED",
    "REGAGE26e00070236067",
    "objective appearance of possible influence, fragmentation or",
    "functional neutralisation",
    "historical transport events do not establish transmission",
    "GitHub Integration Controller",
    "PD-SP-EVT-1113",
    "Nine existing principal canonical event IDs",
    "certified transfer from Fiscalía Superior to Fiscalía Provincial de Las Palmas",
    "recipient acknowledgement by Fiscalía Provincial de Las Palmas for the EG 112-separated modules",
    "re-query Gmail",
    "PAGINATION = EXHAUSTED",
    "EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md",
    "PRE_SEND_GMAIL_PERSON_OUTLET_HISTORY_GATE_23AUG2026.md",
    "OUTBOUND_EMAIL_COMMUNICATIONS_PROTOCOL_23AUG2026.md",
    "fresh, explicit send authorisation",
    "no GitLab write attempted",
    *CANONICAL_EVENT_IDS,
):
    normalized_marker = " ".join(marker.split()).casefold()
    require(normalized_marker in normalized_handoff, f"EG 112 handoff missing marker: {marker}")

for binding in EXPECTED_HANDOFF_BINDINGS:
    require(
        " ".join(binding.split()).casefold() in normalized_handoff,
        f"EG 112 handoff changed canonical event binding: {binding}",
    )

for path, (expected_hash, expected_size) in EXPECTED_INDEXES.items():
    relative_path = path.relative_to(ROOT).as_posix()
    expected_size_text = f"{expected_size:,} bytes"
    require(relative_path in handoff, f"handoff missing explanatory-index path: {relative_path}")
    require(expected_hash in handoff, f"handoff missing explanatory-index hash: {expected_hash}")
    require(expected_size_text in handoff, f"handoff missing explanatory-index size: {expected_size_text}")

register = json.loads(read(COMMUNICATIONS_REGISTER))
events = register.get("events", [])
require(isinstance(events, list), "canonical communications register must contain an events list")
event_ids = [event.get("event_id") for event in events if isinstance(event, dict)]
for event_id in (*CANONICAL_EVENT_IDS, "PD-SP-EVT-1113"):
    require(event_ids.count(event_id) == 1, f"canonical communications register must contain {event_id} exactly once")
events_by_id = {
    event.get("event_id"): event
    for event in events
    if isinstance(event, dict) and isinstance(event.get("event_id"), str)
}
for event_id, expected_fields in EXPECTED_EVENT_FIELDS.items():
    event = events_by_id.get(event_id, {})
    for field, expected_value in expected_fields.items():
        require(
            event.get(field) == expected_value,
            f"canonical communications register changed {event_id} {field}",
        )
for event_id in (
    "PD-SP-EVT-0125",
    "PD-SP-EVT-0126",
    "PD-SP-EVT-0127",
    "PD-SP-EVT-1030",
    "PD-SP-EVT-1031",
    "PD-SP-EVT-1044",
    "PD-SP-EVT-1045",
    "PD-SP-EVT-1046",
):
    require(
        "EG 112/2026" in events_by_id.get(event_id, {}).get("matter_references", []),
        f"canonical communications register semantically rebound {event_id} away from EG 112/2026",
    )
receipt_event = next(
    (event for event in events if isinstance(event, dict) and event.get("event_id") == "PD-SP-EVT-0136"),
    {},
)
require(receipt_event.get("official_reference") == "REGAGE26e00070236067", "PD-SP-EVT-0136 receipt mapping changed")
for field, expected_value in {
    "filing": "FORMALLY_PRESENTED_TO_STATED_REGISTRY",
    "registration": "REGISTRATION_RECEIPT_LOCATED",
    "delivery": "NOT_ESTABLISHED_BY_RECEIPT",
    "internal_association": "NOT_ESTABLISHED_BY_RECEIPT",
    "merits": "NOT_ESTABLISHED_BY_RECEIPT",
    "substantive_examination": "NOT_ESTABLISHED_BY_RECEIPT",
}.items():
    require(
        receipt_event.get("evidence_state", {}).get(field) == expected_value,
        f"PD-SP-EVT-0136 {field} proof ceiling changed",
    )
require(
    "PD-SP-EVT-1113" in receipt_event.get("linked_transport_event_ids", []),
    "PD-SP-EVT-0136 linked transport provenance changed",
)
require(
    "normalization pending" in receipt_event.get("office", "").casefold(),
    "PD-SP-EVT-0136 one-to-one public office-label normalisation is no longer explicit",
)
self_archive_event = events_by_id.get("PD-SP-EVT-1113", {})
require(
    self_archive_event.get("evidence_state", {}).get("transmission")
    == "SELF_ARCHIVE_CONTROL_NOT_AN_INSTITUTIONAL_SEND",
    "PD-SP-EVT-1113 transmission proof ceiling changed",
)
require(
    "REGAGE26e00070236067" in self_archive_event.get("matter_references", []),
    "PD-SP-EVT-1113 no longer contains the linked receipt reference",
)

public_safe_text = {path: read(path) for path in PUBLIC_SAFE_CONTROLS}
address_pattern = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63}\b", flags=re.IGNORECASE)
second_timestamp_pattern = re.compile(r"\b(?:[01]?\d|2[0-3]):[0-5]\d:[0-5]\d\b")
draft_header_pattern = re.compile(
    r"^\s*(?:[-*>#`]+\s*)?(?:To|From|De|Cc|Bcc|Reply-To|Date|Fecha|Para|Copia|Asunto|Subject|Message-ID|Id\.?\s+de\s+mensaje)\s*:\s*\S+",
    flags=re.IGNORECASE | re.MULTILINE,
)
for path, text in public_safe_text.items():
    relative_path = path.relative_to(ROOT)
    for banned in BANNED:
        require(banned.casefold() not in text.casefold(), f"private literal remains in {relative_path}: {banned}")
    require(not address_pattern.search(text), f"operational address remains in {relative_path}")
    require(not second_timestamp_pattern.search(text), f"second-level mailbox time remains in {relative_path}")
    require(not draft_header_pattern.search(text), f"private draft header remains in {relative_path}")
    require(not SPANISH_ID_PATTERN.search(text), f"full Spanish identifier pattern remains in {relative_path}")

scan_prompt = public_safe_text[SCAN_PROMPT]
normalized_scan_prompt = " ".join(scan_prompt.split()).casefold()
for marker in (
    "SUPERSEDED EXECUTION CONTROL — DO NOT REPLAY",
    "HISTORICAL DECISION RECORD — SUPERSEDED / DO NOT EXECUTE",
    "SEND STATUS: PREPARED — NOT SENT",
    "fresh pagination-exhausted dual Gmail history gate",
):
    require(
        " ".join(marker.split()).casefold() in normalized_scan_prompt,
        f"historical scan prompt missing supersession marker: {marker}",
    )
for stale_directive in ("SEND FIRST:", "SEND SECOND:", "REVIEW BEFORE SENDING:"):
    require(stale_directive.casefold() not in scan_prompt.casefold(), f"historical scan prompt still contains executable directive: {stale_directive}")

professional_and_routing = {
    ES_PROFESSIONAL: read(ES_PROFESSIONAL),
    EN_PROFESSIONAL: read(EN_PROFESSIONAL),
    ROUTING: public_safe_text[ROUTING],
    DISPATCH_CONTROL: public_safe_text[DISPATCH_CONTROL],
}
for path, text in professional_and_routing.items():
    lowered = text.casefold()
    for stale in (
        "eg 112/2026 requiere aclaración",
        "eg 112/2026 requires clarification",
        "government file 112/2026 requires clarification",
        "other eight destinations",
        "otros ocho destinos",
        "other seven destinations",
        "otros siete destinos",
        "two procedural responses located",
        "dos respuestas procesales localizadas",
        "one concrete cure; all other substantive responses remain open",
        "una subsanación concreta; las demás respuestas siguen abiertas",
    ):
        require(stale.casefold() not in lowered, f"stale EG 112 wording remains in {path.relative_to(ROOT)}: {stale}")

for path, markers in {
    ES_PROFESSIONAL: (
        "EG 112/2026 ya recibió aclaración",
        "acusación penal nueva o similar",
        "mantiene el archivo",
        "Fiscalía Provincial de Las Palmas",
        "No documenta por sí solo traslado, recepción o decisión individual",
        "Una decisión, una subsanación y un acuse central",
        "Secretaría Técnica FGE",
        "asociación con E.G. 745 ni examen",
    ),
    EN_PROFESSIONAL: (
        "Government File 112/2026 has now been clarified",
        "new or similar criminal accusation",
        "maintains closure",
        "Las Palmas Provincial Prosecutor",
        "does not by itself document transfer, receipt or individual disposition",
        "One decision, one cure request and one central receipt",
        "FGE Technical Secretariat",
        "E.G. 745 association or examination",
    ),
    ROUTING: (
        "EG 112/2026 has now been clarified",
        "maintains closure",
        "territorial route",
        "separate disposition",
        "ONE CLARIFICATION DECISION",
        "ONE CURE REQUEST",
        "ONE CENTRAL RECEIPT CHECKPOINT",
        "other six institutional destinations",
        "FILING STATUS: PROPOSED — NOT DRAFTED / NOT FILED",
        "SEND STATUS: PROPOSED — NOT DRAFTED / NOT SENT",
    ),
    DISPATCH_CONTROL: (
        "EG 112/2026 has now been clarified",
        "new or similar criminal accusation",
        "maintains closure",
        "territorial route",
        "traceable disposition",
        "ONE CLARIFICATION DECISION",
        "ONE CURE REQUEST",
        "ONE CENTRAL RECEIPT CHECKPOINT",
        "Public CSV schema",
        "privacy-minimising breaking schema change",
        "FILING STATUS: PROPOSED — NOT DRAFTED / NOT FILED",
        "SEND STATUS: PROPOSED — NOT DRAFTED / NOT SENT",
    ),
}.items():
    text = professional_and_routing[path]
    normalized_text = " ".join(text.split()).casefold()
    for marker in markers:
        normalized_marker = " ".join(marker.split()).casefold()
        require(normalized_marker in normalized_text, f"{path.relative_to(ROOT)} missing EG 112 status marker: {marker}")

register_text = public_safe_text[DISPATCH_REGISTER]
reader = csv.DictReader(register_text.splitlines())
rows = list(reader)
require(tuple(reader.fieldnames or ()) == EXPECTED_DISPATCH_HEADER, "public dispatch register v2 header changed")
require(len(rows) == 9, "public dispatch register must contain exactly nine rows")
require(
    [row.get("order") for row in rows] == [str(order) for order in range(1, 10)],
    "public dispatch register orders must be exactly 1 through 9",
)
require(
    len({row.get("public_dispatch_reference") for row in rows}) == 9,
    "public dispatch references must be unique",
)
for row in rows:
    order = row.get("order", "?")
    require(None not in row, f"dispatch row {order} contains an extra unheaded field")
    require(
        all(value is not None and value.strip() for value in row.values()),
        f"dispatch row {order} contains a blank field",
    )
    require(row.get("sent_date") == "2026-08-20", f"dispatch row {row.get('order')} must use the date-only value")
    if order.isdigit():
        require(
            row.get("public_dispatch_reference") == f"MF-DSP-20260820-{int(order):02d}",
            f"dispatch row {order} reference does not match its order",
        )
row_three = next((row for row in rows if row.get("order") == "3"), {})
for marker in ("2026-08-23", "2026-08-25", "closure maintained", "territorial route", "traceability remains open"):
    require(marker.casefold() in row_three.get("status", "").casefold(), f"dispatch row 3 missing marker: {marker}")
row_four = next((row for row in rows if row.get("order") == "4"), {})
for marker in ("2026-08-21", "CENTRAL RECEIPT ACKNOWLEDGED", "functional transfer", "association remain unproved"):
    require(marker.casefold() in row_four.get("status", "").casefold(), f"dispatch row 4 missing marker: {marker}")

if FAILURES:
    print("FISCALIA DIP2 / REF24 / EG112 VALIDATION: FAIL")
    for failure in FAILURES:
        print(f"- {failure}")
    sys.exit(1)

print("FISCALIA DIP2 / REF24 / EG112 VALIDATION: PASS")

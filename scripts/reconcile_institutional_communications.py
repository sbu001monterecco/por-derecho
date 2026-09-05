#!/usr/bin/env python3
"""Deterministically reconcile the public-safe institutional communications register.

The 75-row RedSARA short index is the canonical detailed baseline.  This script
never expands the later 22 metadata-only records into invented event rows.  It
also merges only source-controlled curated/public-authority events and never
imports mailbox/provider locators into the public repository.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "archive/evidence/mf-redsara-anexo4/MF_REDSARA_REGISTRATION_INDEX_SHORT.csv"
DEFAULT_MAILBOX_INDEX = REPO_ROOT / "assets/data/institutional-communications-mailbox-index-v1.json"
DEFAULT_REGISTER = REPO_ROOT / "assets/data/institutional-communications-register-v1.json"
DEFAULT_CHECKPOINT = REPO_ROOT / "ops/INSTITUTIONAL_COMMUNICATIONS_SCAN_CHECKPOINT.json"
AUTHORITY_SCAN_CHECKPOINT = REPO_ROOT / "ops/PUBLIC_AUTHORITY_COMMUNICATIONS_SCAN_CHECKPOINT_20260901.json"
BASELINE_COHORT = "BASELINE_REDSARA_ANEXO4_75"
BASELINE_EXPECTED = 75
BASELINE_SOURCE_SHA256 = "784b45bb9ef9e5934d4b4dedc7068dfef90b6e19a10d55bfc1170933d097dcc3"
REGISTER_SOURCE_PDF_SHA256 = "4636b0da487f9150cd8f229d36f9c44f1bd16c9005f6bfa1415bcbc84595e03f"
PUBLIC_TRANSCRIPT_SHA256 = "18a5d1687234e18d9293a3563d51118ea7b16fb5611adac9b8b428876d875df1"
EVENT_ID_RE = re.compile(r"^PD-SP-EVT-(\d{4})$")
MAILBOX_COHORT = "MAILBOX_TRANSPORT_SOURCE_PROVED"
MAILBOX_EXPECTED = 156
PRIVATE_MANIFEST_SHA256 = "bdd12a8fa62b5058525e1c37053fb7899ac24a60d12ff48ab8b74bda617cd6f6"
PRIVATE_MANIFEST_ROWS = 231


RECIPIENTS: dict[str, tuple[str, str]] = {
    "Fiscalia Provincial de Las Palmas": ("J00001657", "PD-SP-I-0020"),
    "Fiscalia de la Comunidad Autonoma de Canarias": ("J00015401", "PD-SP-I-0002"),
    "Fiscalia de Area de Arrecife de Lanzarote-Puerto del Rosario": ("J00017154", "PD-SP-I-0002"),
    "Fiscalia Provincial de Santa Cruz de Tenerife": ("J00001853", "PD-SP-I-0002"),
    "Fiscalia Especial contra la Corrupcion y Criminalidad Organizada": ("J00004991", "PD-SP-I-0002"),
    "Fiscalía Europea": ("J00024141", "PD-SP-I-0002"),
    "Fiscalía General del Estado": ("J00003992", "PD-SP-I-0002"),
    "Fiscalia Provincial de Valencia": ("J00004143", "PD-SP-I-0002"),
    "Fiscalía de la Sala de lo Penal del Tribunal Supremo": ("J00020146", "PD-SP-I-0002"),
    "Fiscalia de la Audiencia Nacional": ("J00003864", "PD-SP-I-0002"),
    "Unidad de Apoyo a la Fiscalía Europea": ("EA0052807", "PD-SP-I-0002"),
}


RECEIPT_BOUNDARY = {
    "transmission": "OFFICIAL_REGISTRATION_RECEIPT_LOCATED",
    "registration": "REGISTRATION_RECEIPT_LOCATED",
    "filing": "FORMALLY_PRESENTED_TO_STATED_REGISTRY",
    "destination": "DESTINATION_AS_STATED_ON_RECEIPT",
    "delivery": "NOT_ESTABLISHED_BY_RECEIPT",
    "internal_association": "NOT_ESTABLISHED_BY_RECEIPT",
    "substantive_examination": "NOT_ESTABLISHED_BY_RECEIPT",
    "merits": "NOT_ESTABLISHED_BY_RECEIPT",
}


def _key_event(
    event_id: str,
    event_date: str,
    record_type: str,
    direction: str,
    channel: str,
    office: str,
    reference: str,
    summary: str,
    source_anchor: str,
    proves: list[str],
    does_not_prove: list[str],
    *,
    source_sha256: str | None = None,
    matter_references: list[str] | None = None,
    evidence_state: dict[str, str] | None = None,
    attribution_state: str = "NO_PERSON_ATTRIBUTED_IN_PUBLIC_REGISTER",
    signatory_person_id: str | None = None,
    signatory_person_label: str | None = None,
    linked_transport_event_ids: list[str] | None = None,
    transport_link_state: str = "NO_PUBLIC_TRANSPORT_LINK_ASSERTED",
    proof_level: str = "SOURCE_PROVED_PUBLIC_SAFE_DERIVATIVE",
    event_sequence: str | None = None,
    institution_id: str | None = "PD-SP-I-0002",
    authority_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source_integrity: dict[str, str] = {
        "status": "SOURCE_PROVED_PUBLIC_SAFE_DERIVATIVE",
        "repository_anchor": source_anchor,
    }
    if source_sha256:
        source_integrity["sha256"] = source_sha256
    event = {
        "event_id": event_id,
        "cohort": "CURATED_SOURCE_PROVED_EVENT",
        "layer": "FORMAL_REGISTRATION" if record_type == "REGISTRATION_RECEIPT" else "OFFICIAL_ACT_OR_CORRESPONDENCE",
        "source_key": f"CURATED:{event_id}",
        "record_type": record_type,
        "event_date": event_date,
        "direction": direction,
        "channel": channel,
        "office": office,
        "official_reference": reference,
        "public_summary": summary,
        "matter_references": matter_references or [reference],
        "source_integrity": source_integrity,
        "attribution_state": attribution_state,
        "linked_transport_event_ids": linked_transport_event_ids or [],
        "transport_link_state": transport_link_state,
        "proof_level": proof_level,
        "evidence_state": evidence_state or {
            "transmission": "SOURCE_ACT_OR_CORRESPONDENCE_LOCATED",
            "registration": "NOT_INFERRED_UNLESS_EXPRESSLY_STATED",
            "filing": "NOT_INFERRED_UNLESS_EXPRESSLY_STATED",
            "destination": "ONLY_AS_STATED_IN_SOURCE",
            "delivery": "ONLY_AS_STATED_IN_SOURCE",
            "internal_association": "NOT_ESTABLISHED_UNLESS_EXPRESSLY_STATED",
            "substantive_examination": "NOT_ESTABLISHED_UNLESS_EXPRESSLY_STATED",
            "merits": "PROCEDURAL_ACT_ONLY_NOT_TRUTH_OF_UNDERLYING_ALLEGATIONS",
        },
        "proves": proves,
        "does_not_prove": does_not_prove,
    }
    if institution_id:
        event["institution_id"] = institution_id
    if authority_metadata:
        event.update(deepcopy(authority_metadata))
    if signatory_person_id:
        event["signatory_person_id"] = signatory_person_id
    if signatory_person_label:
        event["signatory_person_label"] = signatory_person_label
    if event_sequence:
        event["event_sequence"] = event_sequence
    return event


KEY_EVENTS: list[dict[str, Any]] = [
    _key_event(
        "PD-SP-EVT-0076",
        "2019-05-07",
        "OFFICIAL_DECISION",
        "INBOUND_FROM_INSTITUTION",
        "SIGNED_DECREE",
        "Fiscalía Provincial de Las Palmas",
        "DI 248/2018",
        "Archive decree located; the decree records the adverse criminal assessment and the article 773 LECrim judicial route.",
        "archive/SUN_PARK_2011_2019_OPERATOR_CONTROL_DP1132_DI248_NONCONVALIDATION_TEN_SOURCE_SUPPLEMENT_17AUG2026.md",
        ["A signed archive disposition dated 7 May 2019 is controlled."],
        ["Complete-file review, every requested diligence, coordination, obstruction, prevarication or criminality."],
        matter_references=["DI 248/2018", "Concurso 36/2012"],
        attribution_state="SOURCE_PROVED_SIGNATORY",
        signatory_person_id="PD-SP-P-0104",
        signatory_person_label="Elena Herrera Rodríguez",
    ),
    _key_event(
        "PD-SP-EVT-0077",
        "2026-01-27",
        "OFFICIAL_ROUTING_ACT",
        "INBOUND_FROM_INSTITUTION",
        "SIGNED_DECREE",
        "Fiscalía Provincial de Santa Cruz de Tenerife",
        "DIP 20/2026",
        "Opening and territorial inhibition/remission act located for the separate Tenerife file.",
        "archive/public_office_communications/fiscalia_tenerife/2026-01-30_DIP20/2026-01-27_30__FISCALIA_TENERIFE__DIP20_2026__CONTROLLED_RECORD_ES_EN.md",
        ["The located act records opening and territorial transfer to Las Palmas."],
        ["Receipt, allocation, joinder, examination or outcome in Las Palmas."],
        source_sha256="efd4eee1d4c9f4bddf2d5ca1f0c413f18bbb83ad19d2535b554cdb2f66ffb501",
        matter_references=["DIP 20/2026"],
    ),
    _key_event(
        "PD-SP-EVT-0078",
        "2026-03-06",
        "OFFICIAL_DECISION",
        "INBOUND_FROM_INSTITUTION",
        "SIGNED_DECREE",
        "Fiscalía Provincial de Las Palmas",
        "DIP 2/2026",
        "Archive without res judicata is recorded in the located signed decree.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["A signed archive decision dated 6 March 2026 is source-controlled."],
        ["Incorporation or examination of the later registered correction, coordination or unlawful intent."],
        matter_references=["DIP 2/2026", "NIG 3501670220260000245"],
        attribution_state="SOURCE_PROVED_SIGNATORY",
        signatory_person_id="PD-SP-P-0110",
        signatory_person_label="Juan Manuel González-Casanova Ruiz",
        proof_level="SIGNED_ACT_LOCATED",
    ),
    _key_event(
        "PD-SP-EVT-0079",
        "2026-03-09",
        "OFFICIAL_NOTIFICATION",
        "INBOUND_FROM_INSTITUTION",
        "OFFICIAL_NOTICE",
        "Fiscalía Provincial de Las Palmas",
        "DIP 2/2026",
        "Official notice of the 6 March archive decision is located.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["Notice of the decision is controlled."],
        ["Agreement with the decision, waiver of later correction, or merits correctness."],
        matter_references=["DIP 2/2026", "NIG 3501670220260000245"],
        attribution_state="SOURCE_PROVED_SIGNATORY",
        signatory_person_id="PD-SP-P-0111",
        signatory_person_label="Ernesto Vieira Morante",
        proof_level="OFFICIAL_NOTICE_LOCATED",
    ),
    _key_event(
        "PD-SP-EVT-0080",
        "2026-06-03",
        "OFFICIAL_DECISION",
        "INBOUND_FROM_INSTITUTION",
        "SIGNED_DECREE",
        "Fiscalía General del Estado",
        "EG 49/2026 / outgoing 226",
        "Located signed decision records the central route and declines/archives the request.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The signed 3 June decision and its stated procedural reasoning are controlled."],
        ["Personal review of every source, complete routing, coordination, obstruction, prevarication or criminality."],
        source_sha256="4e5d3486cc052ea699029a8744e21a2040918f4e03a085cc066a3b6ff8f12b88",
        matter_references=["EG 49/2026"],
        attribution_state="SOURCE_PROVED_SIGNATORY",
        signatory_person_id="PD-SP-P-0109",
        signatory_person_label="Emilio Jesús Sánchez Ulled",
        linked_transport_event_ids=["PD-SP-EVT-1047"],
        transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED_TO_DECISION_ATTACHMENT",
        proof_level="SIGNED_ACT_LOCATED",
    ),
    _key_event(
        "PD-SP-EVT-0081",
        "2026-06-09",
        "OFFICIAL_DECISION",
        "INBOUND_FROM_INSTITUTION",
        "SIGNED_DECREE",
        "Fiscalía General del Estado",
        "EG 49/2026 / outgoing 230",
        "Located signed decision records accumulation of the renewed request and again declines/archives.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The signed 8/9 June decision and its stated disposition are controlled."],
        ["A complete merits re-audit, examination of every source or an inter-office agreement."],
        source_sha256="32a06dbf5745edc2e7ea6f9c88a22231d8238ce1e1a9faa5418db2eab253a383",
        matter_references=["EG 49/2026"],
        attribution_state="SOURCE_PROVED_SIGNATORY",
        signatory_person_id="PD-SP-P-0109",
        signatory_person_label="Emilio Jesús Sánchez Ulled",
        linked_transport_event_ids=["PD-SP-EVT-1048"],
        transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED_TO_DECISION_ATTACHMENT",
        proof_level="SIGNED_ACT_LOCATED",
    ),
    _key_event(
        "PD-SP-EVT-0082",
        "2026-07-12",
        "OFFICIAL_ROUTING_ACT",
        "INSTITUTION_TO_INSTITUTION",
        "JUDICIAL_ORDER",
        "Juzgado de Instrucción — plaza 6 de Las Palmas",
        "DP 1901/2026 / NIG 3501643220260016977",
        "Located judicial providencia gives Fiscalía five days to report on admission.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["A court-to-Fiscalía report request is controlled."],
        ["The report's existence, author, contents, transmission or the later judicial outcome."],
        matter_references=["DP 1901/2026", "NIG 3501643220260016977", "DIP 2/2026"],
    ),
    _key_event(
        "PD-SP-EVT-0083",
        "2026-08-02",
        "REGISTRATION_RECEIPT",
        "OUTBOUND_TO_INSTITUTION",
        "REGAGE",
        "Fiscalía General del Estado — Inspección Fiscal",
        "REGAGE26e00070235775 / E.G. 745/2026",
        "Official REG-AGE receipt for the Inspection filing is controlled.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The identified submission was formally registered to the stated destination."],
        ["Internal allocation, association with a later email, examination, admission, merits acceptance or requested relief."],
        matter_references=["E.G. 745/2026", "DI 248/2018", "DI 113/2022", "DI 22/2026", "DIP 2/2026", "EG 49/2026", "DP 1901/2026"],
        evidence_state=deepcopy(RECEIPT_BOUNDARY),
        linked_transport_event_ids=["PD-SP-EVT-1113"],
        transport_link_state="PRIMARY_RECEIPT_COPY_LOCATED_IN_SELF_ARCHIVE_TRANSPORT",
        proof_level="PRIMARY_REGISTRATION_RECEIPT_LOCATED",
    ),
    _key_event(
        "PD-SP-EVT-0084",
        "2026-08-20",
        "OUTBOUND_COMMUNICATION",
        "OUTBOUND_TO_INSTITUTION",
        "OFFICIAL_EMAIL",
        "Fiscalía General del Estado — Inspección Fiscal",
        "E.G. 745/2026 / REGAGE26e00070235775",
        "Inspection-directed communication requested transfer, association, traceability and preservation.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The communication was sent with the stated requests."],
        ["Central receipt, transfer to Inspection, association, allocation, examination or action."],
        matter_references=["E.G. 745/2026", "REGAGE26e00070235775"],
        linked_transport_event_ids=["PD-SP-EVT-1082"],
        transport_link_state="EXACT_OUTBOUND_TRANSPORT_LINKED",
    ),
    _key_event(
        "PD-SP-EVT-0085",
        "2026-08-21",
        "INSTITUTIONAL_ACKNOWLEDGEMENT",
        "INBOUND_FROM_INSTITUTION",
        "OFFICIAL_EMAIL",
        "Fiscalía General del Estado — Secretaría Técnica",
        "E.G. 745/2026 / REGAGE26e00070235775",
        "The Technical Secretariat acknowledged central receipt and stated that corresponding management would follow.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["Central receipt of the 20 August communication and the stated prospective management."],
        ["Transfer to Inspection, file association, allocation, pre-decision incorporation, examination or merits action."],
        matter_references=["E.G. 745/2026", "REGAGE26e00070235775"],
        linked_transport_event_ids=["PD-SP-EVT-1084", "PD-SP-EVT-1085", "PD-SP-EVT-1086", "PD-SP-EVT-1117"],
        transport_link_state="FOUR_ACKNOWLEDGEMENT_BUNDLE_LINKS_PRESERVED; ONE_TO_ONE_ALLOCATION_NOT_INFERRED",
    ),
    _key_event(
        "PD-SP-EVT-0086",
        "2026-08-26",
        "OFFICIAL_DECISION",
        "INBOUND_FROM_INSTITUTION",
        "SIGNED_DECREE_AND_NOTICE",
        "Fiscalía General del Estado — Inspección Fiscal",
        "E.G. 745/2026",
        "Located official decree/notice archives E.G. 745/2026 and states review routes.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The dated archive disposition and stated review routes are controlled."],
        ["The complete file, every source examined, request-by-request treatment, merits correctness, coordination, obstruction, prevarication or criminality."],
        source_sha256="1e09c8eb3bce26e28dc5f22e5d6ebad3f458212cf8d85f5920e869fa42554abe",
        matter_references=["E.G. 745/2026"],
        attribution_state="SOURCE_PROVED_SIGNATORY",
        signatory_person_id="PD-SP-P-0108",
        signatory_person_label="María José Osuna Cerezo",
        linked_transport_event_ids=["PD-SP-EVT-1063"],
        transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED_TO_DECISION_ATTACHMENT",
        proof_level="SIGNED_ACT_LOCATED",
    ),
    _key_event(
        "PD-SP-EVT-0087",
        "2023-02-08",
        "OFFICIAL_DECISION",
        "INBOUND_FROM_INSTITUTION",
        "SIGNED_DECREE",
        "Fiscalía Provincial de Las Palmas",
        "DI 113/2022 / NIG 3501670220220003722",
        "Located signed decree archives DI 113/2022 and records its stated reasoning and prior-route recital.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The archive act, date, signatory and stated reasons are source-controlled."],
        ["Truth of the complaint, complete-file completeness, every diligence, complete remittal, improper motive or criminality."],
        matter_references=["DI 113/2022", "NIG 3501670220220003722", "DP 668/2021"],
        attribution_state="SOURCE_PROVED_SIGNATORY",
        signatory_person_id="PD-SP-P-0103",
        signatory_person_label="Beatriz Sánchez Carreras",
        linked_transport_event_ids=["PD-SP-EVT-1105"],
        transport_link_state="HISTORIC_ACT_LOCATED_IN_2026_OFFICIAL_NOTICE_BUNDLE",
        proof_level="SIGNED_ACT_LOCATED",
    ),
    _key_event(
        "PD-SP-EVT-0088",
        "2026-02-23",
        "OFFICIAL_DECISION",
        "INBOUND_FROM_INSTITUTION",
        "SIGNED_DECREE",
        "Fiscalía Provincial de Las Palmas",
        "DI 113/2022 / information-copy request",
        "Located signed decision addresses the later information/copy request in DI 113/2022.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The 23 February decision, signatory and stated disposition are source-controlled."],
        ["Production of the complete file, complete merits review or cure of every source gap."],
        matter_references=["DI 113/2022", "NIG 3501670220220003722"],
        attribution_state="SOURCE_PROVED_SIGNATORY",
        signatory_person_id="PD-SP-P-0103",
        signatory_person_label="Beatriz Sánchez Carreras",
        linked_transport_event_ids=["PD-SP-EVT-1105"],
        transport_link_state="OFFICIAL_NOTICE_BUNDLE_LINKED",
        proof_level="SIGNED_ACT_LOCATED",
    ),
    _key_event(
        "PD-SP-EVT-0089",
        "2026-02-25",
        "OFFICIAL_NOTIFICATION",
        "INBOUND_FROM_INSTITUTION",
        "OFFICIAL_NOTICE",
        "Fiscalía Provincial de Las Palmas",
        "DI 113/2022 / information-copy request",
        "Official notice of the 23 February DI 113/2022 decision is located.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The notification event and its relationship to the copy decision are controlled."],
        ["Agreement, waiver, complete production or merits correctness."],
        matter_references=["DI 113/2022", "NIG 3501670220220003722"],
        attribution_state="INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED",
        linked_transport_event_ids=["PD-SP-EVT-1105"],
        transport_link_state="EXACT_OFFICIAL_NOTICE_TRANSPORT_LINKED",
        proof_level="OFFICIAL_NOTICE_LOCATED",
    ),
    _key_event(
        "PD-SP-EVT-0090",
        "2026-02-11",
        "OFFICIAL_DECISION",
        "INBOUND_FROM_INSTITUTION",
        "SIGNED_DECREE",
        "Fiscalía Provincial de Las Palmas",
        "DI 22/2026 / NIG 3501670220260000369",
        "Located signed decree opens DI 22/2026 and records its archive/classification disposition.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The opening/archive act, date, signatory and stated classification are source-controlled."],
        ["Complete examination of each distinct module, every diligence, improper purpose, prevarication or criminality."],
        matter_references=["DI 22/2026", "NIG 3501670220260000369"],
        attribution_state="SOURCE_PROVED_SIGNATORY",
        signatory_person_id="PD-SP-P-0103",
        signatory_person_label="Beatriz Sánchez Carreras",
        linked_transport_event_ids=["PD-SP-EVT-1101", "PD-SP-EVT-1102"],
        transport_link_state="TWO_NOTICE_BUNDLES_CONTROLLED; ACT_TO_BUNDLE_ALLOCATION_NOT_INFERRED",
        proof_level="SIGNED_ACT_LOCATED",
        event_sequence="DI22-2026-02-11-A",
    ),
    _key_event(
        "PD-SP-EVT-0091",
        "2026-02-13",
        "OFFICIAL_DECISION",
        "INBOUND_FROM_INSTITUTION",
        "SIGNED_DECREE",
        "Fiscalía Provincial de Las Palmas",
        "DI 22/2026 / NIG 3501670220260000369",
        "A located signed act is individually controlled within the DI 22 joinder, archive-maintenance or certification sequence; no narrower subtype is inferred here.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The dated act and source-proved signatory are controlled."],
        ["Which distinct module was substantively examined, complete-source treatment or improper purpose."],
        matter_references=["DI 22/2026", "NIG 3501670220260000369"],
        attribution_state="SOURCE_PROVED_SIGNATORY",
        signatory_person_id="PD-SP-P-0103",
        signatory_person_label="Beatriz Sánchez Carreras",
        linked_transport_event_ids=["PD-SP-EVT-1101", "PD-SP-EVT-1102"],
        transport_link_state="TWO_NOTICE_BUNDLES_CONTROLLED; ACT_TO_BUNDLE_ALLOCATION_NOT_INFERRED",
        proof_level="SIGNED_ACT_LOCATED",
        event_sequence="DI22-2026-02-13-A",
    ),
    _key_event(
        "PD-SP-EVT-0092",
        "2026-02-16",
        "OFFICIAL_DECISION",
        "INBOUND_FROM_INSTITUTION",
        "SIGNED_DECREE",
        "Fiscalía Provincial de Las Palmas",
        "DI 22/2026 / NIG 3501670220260000369",
        "A located signed act is individually controlled within the DI 22 joinder, archive-maintenance or certification sequence; no narrower subtype is inferred here.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The dated act and source-proved signatory are controlled."],
        ["Which distinct module was substantively examined, complete-source treatment or improper purpose."],
        matter_references=["DI 22/2026", "NIG 3501670220260000369"],
        attribution_state="SOURCE_PROVED_SIGNATORY",
        signatory_person_id="PD-SP-P-0103",
        signatory_person_label="Beatriz Sánchez Carreras",
        linked_transport_event_ids=["PD-SP-EVT-1103"],
        transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED",
        proof_level="SIGNED_ACT_LOCATED",
    ),
    _key_event(
        "PD-SP-EVT-0093",
        "2026-02-19",
        "OFFICIAL_DECISION",
        "INBOUND_FROM_INSTITUTION",
        "SIGNED_DECREE",
        "Fiscalía Provincial de Las Palmas",
        "DI 22/2026 / NIG 3501670220260000369",
        "A located signed act is individually controlled within the DI 22 joinder, archive-maintenance or certification sequence; no narrower subtype is inferred here.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The dated act and source-proved signatory are controlled."],
        ["Which distinct module was substantively examined, complete-source treatment or improper purpose."],
        matter_references=["DI 22/2026", "NIG 3501670220260000369"],
        attribution_state="SOURCE_PROVED_SIGNATORY",
        signatory_person_id="PD-SP-P-0103",
        signatory_person_label="Beatriz Sánchez Carreras",
        linked_transport_event_ids=["PD-SP-EVT-1104"],
        transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED",
        proof_level="SIGNED_ACT_LOCATED",
    ),
    _key_event(
        "PD-SP-EVT-0094",
        "2026-03-02",
        "OFFICIAL_DECISION",
        "INBOUND_FROM_INSTITUTION",
        "SIGNED_DECREE",
        "Fiscalía Provincial de Las Palmas",
        "DI 22/2026 / NIG 3501670220260000369",
        "A located signed act is individually controlled within the DI 22 joinder, archive-maintenance or certification sequence; no narrower subtype is inferred here.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The dated act and source-proved signatory are controlled."],
        ["Which distinct module was substantively examined, complete-source treatment or improper purpose."],
        matter_references=["DI 22/2026", "NIG 3501670220260000369"],
        attribution_state="SOURCE_PROVED_SIGNATORY",
        signatory_person_id="PD-SP-P-0103",
        signatory_person_label="Beatriz Sánchez Carreras",
        linked_transport_event_ids=["PD-SP-EVT-1106"],
        transport_link_state="MULTI_ACT_NOTICE_BUNDLE_LINKED",
        proof_level="SIGNED_ACT_LOCATED",
    ),
    _key_event(
        "PD-SP-EVT-0095",
        "2026-03-03",
        "OFFICIAL_DECISION",
        "INBOUND_FROM_INSTITUTION",
        "SIGNED_DECREE",
        "Fiscalía Provincial de Las Palmas",
        "DI 22/2026 / NIG 3501670220260000369",
        "A located signed act is individually controlled within the DI 22 joinder, archive-maintenance or certification sequence; no narrower subtype is inferred here.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The dated act and source-proved signatory are controlled."],
        ["Which distinct module was substantively examined, complete-source treatment or improper purpose."],
        matter_references=["DI 22/2026", "NIG 3501670220260000369"],
        attribution_state="SOURCE_PROVED_SIGNATORY",
        signatory_person_id="PD-SP-P-0103",
        signatory_person_label="Beatriz Sánchez Carreras",
        linked_transport_event_ids=["PD-SP-EVT-1106"],
        transport_link_state="MULTI_ACT_NOTICE_BUNDLE_LINKED",
        proof_level="SIGNED_ACT_LOCATED",
    ),
    _key_event(
        "PD-SP-EVT-0096",
        "2026-06-03",
        "OFFICIAL_ROUTING_ACT",
        "INBOUND_FROM_INSTITUTION",
        "OFFICE_ACT",
        "Fiscalía Provincial de Las Palmas",
        "DI 22/2026 / NIG 3501670220260000369",
        "A later office act records further remitted material joined to DI 22 and archived treatment maintained.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The office act, date and stated procedural treatment are controlled."],
        ["Personal signatory, personal direction, merits examination of each item or improper purpose."],
        matter_references=["DI 22/2026", "NIG 3501670220260000369"],
        attribution_state="INSTITUTION_ONLY_SIGNATURE_PENDING",
        linked_transport_event_ids=["PD-SP-EVT-1107"],
        transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED",
        proof_level="OFFICIAL_NOTICE_AND_ACT_LOCATED_SIGNATURE_NORMALISATION_PENDING",
    ),
    _key_event(
        "PD-SP-EVT-0097",
        "2026-06-30",
        "OFFICIAL_ROUTING_ACT",
        "INBOUND_FROM_INSTITUTION",
        "OFFICE_ACT",
        "Fiscalía Provincial de Las Palmas",
        "DI 22/2026 / NIG 3501670220260000369",
        "A later office act records further remitted material joined to DI 22 and archived treatment maintained.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The office act, date and stated procedural treatment are controlled."],
        ["Personal signatory, personal direction, merits examination of each item or improper purpose."],
        matter_references=["DI 22/2026", "NIG 3501670220260000369"],
        attribution_state="INSTITUTION_ONLY_SIGNATURE_PENDING",
        linked_transport_event_ids=["PD-SP-EVT-1018"],
        transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED",
        proof_level="OFFICIAL_NOTICE_AND_ACT_LOCATED_SIGNATURE_NORMALISATION_PENDING",
    ),
    _key_event(
        "PD-SP-EVT-0098",
        "2026-07-08",
        "OFFICIAL_ROUTING_ACT",
        "INBOUND_FROM_INSTITUTION",
        "OFFICE_ACT",
        "Fiscalía Provincial de Las Palmas",
        "DI 22/2026 / NIG 3501670220260000369",
        "A later office act records further remitted material joined to DI 22 and archived treatment maintained.",
        "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        ["The office act, date and stated procedural treatment are controlled."],
        ["Personal signatory, personal direction, merits examination of each item or improper purpose."],
        matter_references=["DI 22/2026", "NIG 3501670220260000369"],
        attribution_state="INSTITUTION_ONLY_SIGNATURE_PENDING",
        linked_transport_event_ids=["PD-SP-EVT-1108"],
        transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED",
        proof_level="OFFICIAL_NOTICE_AND_ACT_LOCATED_SIGNATURE_NORMALISATION_PENDING",
    ),
]


def _mail_control_event(
    event_id: str,
    event_date: str,
    record_type: str,
    office: str,
    reference: str,
    summary: str,
    *,
    direction: str = "INBOUND_FROM_INSTITUTION",
    channel: str = "OFFICIAL_NOTICE_OR_CONTROLLED_ACT",
    matter_references: list[str] | None = None,
    linked_transport_event_ids: list[str] | None = None,
    transport_link_state: str = "NO_PUBLIC_TRANSPORT_LINK_ASSERTED",
    proof_level: str = "OFFICIAL_NOTICE_OR_ACT_LOCATED",
    attribution_state: str = "NO_PERSON_ATTRIBUTED_IN_PUBLIC_REGISTER",
    signatory_person_id: str | None = None,
    signatory_person_label: str | None = None,
    event_sequence: str | None = None,
    evidence_state: dict[str, str] | None = None,
) -> dict[str, Any]:
    return _key_event(
        event_id,
        event_date,
        record_type,
        direction,
        channel,
        office,
        reference,
        summary,
        "evidence/fiscalia/2026/MF_MAILBOX_REGAGE_CONTROL_31AUG2026.md",
        ["The discrete event, date, office/reference relationship and stated procedural character are controlled at the published proof level."],
        ["Truth of underlying allegations, complete-file review, internal allocation beyond the source, improper motive, coordination, obstruction, prevarication or criminality."],
        matter_references=matter_references or [reference],
        evidence_state=evidence_state,
        attribution_state=attribution_state,
        signatory_person_id=signatory_person_id,
        signatory_person_label=signatory_person_label,
        linked_transport_event_ids=linked_transport_event_ids,
        transport_link_state=transport_link_state,
        proof_level=proof_level,
        event_sequence=event_sequence,
    )


KEY_EVENTS.extend(
    [
        _mail_control_event(
            "PD-SP-EVT-0099", "2026-02-11", "OFFICIAL_DECISION", "Fiscalía Provincial de Las Palmas",
            "DI 22/2026 / NIG 3501670220260000369",
            "Second distinct 11-February signed decision joins a further filing and maintains the archive disposition.",
            matter_references=["DI 22/2026", "NIG 3501670220260000369"],
            linked_transport_event_ids=["PD-SP-EVT-1101", "PD-SP-EVT-1102"],
            transport_link_state="TWO_NOTICE_BUNDLES_CONTROLLED; ACT_TO_BUNDLE_ALLOCATION_NOT_INFERRED",
            proof_level="SIGNED_ACT_LOCATED",
            attribution_state="SOURCE_PROVED_SIGNATORY",
            signatory_person_id="PD-SP-P-0103",
            signatory_person_label="Beatriz Sánchez Carreras",
            event_sequence="DI22-2026-02-11-B",
        ),
        _mail_control_event(
            "PD-SP-EVT-0100", "2026-02-13", "OFFICIAL_DECISION", "Fiscalía Provincial de Las Palmas",
            "DI 22/2026 / NIG 3501670220260000369",
            "Second distinct 13-February signed decision joins additional material linked to other prosecutorial routes and maintains archive.",
            matter_references=["DI 22/2026", "NIG 3501670220260000369"],
            linked_transport_event_ids=["PD-SP-EVT-1101", "PD-SP-EVT-1102"],
            transport_link_state="TWO_NOTICE_BUNDLES_CONTROLLED; ACT_TO_BUNDLE_ALLOCATION_NOT_INFERRED",
            proof_level="SIGNED_ACT_LOCATED",
            attribution_state="SOURCE_PROVED_SIGNATORY",
            signatory_person_id="PD-SP-P-0103",
            signatory_person_label="Beatriz Sánchez Carreras",
            event_sequence="DI22-2026-02-13-B",
        ),
        _mail_control_event(
            "PD-SP-EVT-0101", "2026-01-14", "OFFICIAL_DECISION", "Fiscalía de Área de Arrecife–Puerto del Rosario",
            "DI 114/2025 / NIG 3501670220250003875",
            "Three-page scanned archive decision is located; the visible substantive signature is generic and no person is attributed.",
            matter_references=["DI 114/2025", "NIG 3501670220250003875"],
            linked_transport_event_ids=["PD-SP-EVT-1092"],
            transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED_TO_DECISION_ATTACHMENT",
            proof_level="OFFICIAL_NOTICE_AND_SCANNED_ACT_LOCATED; NATIVE_SEARCHABLE_SIGNATURE_CONTROL_DESIRABLE",
            attribution_state="INSTITUTION_ONLY_SIGNATURE_PENDING",
        ),
        _mail_control_event(
            "PD-SP-EVT-0102", "2026-01-14", "OFFICIAL_NOTIFICATION", "Fiscalía de Área de Arrecife–Puerto del Rosario",
            "DI 114/2025 / NIG 3501670220250003875",
            "Official notice transmitting the DI 114/2025 archive decision is located.",
            matter_references=["DI 114/2025", "NIG 3501670220250003875"],
            linked_transport_event_ids=["PD-SP-EVT-1092"],
            transport_link_state="EXACT_OFFICIAL_NOTICE_TRANSPORT_LINKED",
            proof_level="OFFICIAL_NOTICE_LOCATED",
            attribution_state="SOURCE_PROVED_SIGNATORY",
            signatory_person_id="PD-SP-P-0105",
            signatory_person_label="Ramona Muñoz Casas",
        ),
        _mail_control_event(
            "PD-SP-EVT-0103", "2026-01-27", "OFFICIAL_DECISION", "Fiscalía Provincial de Santa Cruz de Tenerife",
            "DIP 20/2026 / NIG 3803870220260000387",
            "Signed decree opens DIP 20/2026 and orders territorial inhibition/remission to Las Palmas.",
            matter_references=["DIP 20/2026", "NIG 3803870220260000387"],
            linked_transport_event_ids=["PD-SP-EVT-1019"],
            transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED_TO_DECREE_AND_OFFICIO",
            proof_level="SIGNED_ACT_LOCATED",
            attribution_state="SOURCE_PROVED_SIGNATORY",
            signatory_person_id="PD-SP-P-0107",
            signatory_person_label="José Luis Sánchez-Jáuregui y Alcaide",
            event_sequence="DIP20-DECREE",
        ),
        _mail_control_event(
            "PD-SP-EVT-0104", "2026-01-27", "OFFICIAL_ROUTING_ACT", "Fiscalía Provincial de Santa Cruz de Tenerife",
            "DIP 20/2026 / NIG 3803870220260000387",
            "Separate signed oficio communicates archive/inhibition and the stated article 773 LECrim judicial route.",
            matter_references=["DIP 20/2026", "NIG 3803870220260000387"],
            linked_transport_event_ids=["PD-SP-EVT-1019"],
            transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED_TO_DECREE_AND_OFFICIO",
            proof_level="SIGNED_ACT_LOCATED",
            attribution_state="SOURCE_PROVED_SIGNATORY",
            signatory_person_id="PD-SP-P-0107",
            signatory_person_label="José Luis Sánchez-Jáuregui y Alcaide",
            event_sequence="DIP20-OFFICIO",
        ),
        _mail_control_event(
            "PD-SP-EVT-0105", "2026-01-30", "OFFICIAL_NOTIFICATION", "Fiscalía Provincial de Santa Cruz de Tenerife",
            "DIP 20/2026 / NIG 3803870220260000387",
            "Official email notice transmits the decree and oficio.",
            matter_references=["DIP 20/2026", "NIG 3803870220260000387"],
            linked_transport_event_ids=["PD-SP-EVT-1019"],
            transport_link_state="EXACT_OFFICIAL_NOTICE_TRANSPORT_LINKED",
            proof_level="OFFICIAL_NOTICE_LOCATED",
            attribution_state="INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0106", "2025-03-03", "OFFICIAL_ACT_UNCLASSIFIED", "Fiscalía Provincial de Las Palmas",
            "EG 33/2025",
            "Inception/opening document is located; no later disposition is inferred.",
            linked_transport_event_ids=["PD-SP-EVT-1032"],
            transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED_TO_OPENING_ATTACHMENT",
            proof_level="OFFICIAL_OPENING_DOCUMENT_LOCATED; COMPLETE_FILE_AND_LATER_DISPOSITION_REQUIRED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0107", "2025-03-03", "OFFICIAL_NOTIFICATION", "Fiscalía Provincial de Las Palmas",
            "EG 33/2025",
            "Official notice transmits the inception/opening document.",
            linked_transport_event_ids=["PD-SP-EVT-1032"],
            transport_link_state="EXACT_OFFICIAL_NOTICE_TRANSPORT_LINKED",
            proof_level="OFFICIAL_NOTICE_LOCATED",
            attribution_state="INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0108", "2026-02-11", "OFFICIAL_ACT_UNCLASSIFIED", "Fiscalía de la Comunidad Autónoma de Canarias",
            "EG 6/2026",
            "An underlying official act is present in the located notice bundle; its substantive digest remains pending and no outcome is inferred.",
            linked_transport_event_ids=["PD-SP-EVT-1043"],
            transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED_TO_UNDIGESTED_ACT",
            proof_level="OFFICIAL_ACT_LOCATED; SUBSTANTIVE_DIGEST_PENDING",
            attribution_state="INSTITUTION_ONLY_SIGNATURE_PENDING",
        ),
        _mail_control_event(
            "PD-SP-EVT-0109", "2026-02-11", "OFFICIAL_NOTIFICATION", "Fiscalía de la Comunidad Autónoma de Canarias",
            "EG 6/2026",
            "Official notice establishes the correspondence provenance and distinct expediente reference only.",
            linked_transport_event_ids=["PD-SP-EVT-1043"],
            transport_link_state="EXACT_OFFICIAL_NOTICE_TRANSPORT_LINKED",
            proof_level="OFFICIAL_NOTICE_LOCATED; SUBSTANTIVE_ACT_DIGEST_PENDING",
            attribution_state="INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0110", "2026-03-30", "OFFICIAL_DECISION", "Fiscalía de la Comunidad Autónoma de Canarias",
            "EG 44/2026",
            "Signed decree opens and archives EG 44/2026 on the stated competence grounds and records copies/remissions.",
            linked_transport_event_ids=["PD-SP-EVT-1033"],
            transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED_TO_DECISION_ATTACHMENT",
            proof_level="SIGNED_ACT_LOCATED",
            attribution_state="SOURCE_PROVED_SIGNATORY",
            signatory_person_id="PD-SP-P-0113",
            signatory_person_label="Vicente Máximo Garrido García",
        ),
        _mail_control_event(
            "PD-SP-EVT-0111", "2026-03-30", "OFFICIAL_NOTIFICATION", "Fiscalía de la Comunidad Autónoma de Canarias",
            "EG 44/2026",
            "Official notice transmits the EG 44/2026 decree.",
            linked_transport_event_ids=["PD-SP-EVT-1033"],
            transport_link_state="EXACT_OFFICIAL_NOTICE_TRANSPORT_LINKED",
            proof_level="OFFICIAL_NOTICE_LOCATED",
            attribution_state="INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0112", "2026-06-04", "OFFICIAL_NOTIFICATION", "Fiscalía General del Estado",
            "EG 49/2026 / outgoing 226",
            "Official notice transmits the signed 3-June EG 49/2026 decision.",
            matter_references=["EG 49/2026"],
            linked_transport_event_ids=["PD-SP-EVT-1047"],
            transport_link_state="EXACT_OFFICIAL_NOTICE_TRANSPORT_LINKED",
            proof_level="OFFICIAL_NOTICE_LOCATED",
            attribution_state="INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0113", "2026-06-10", "OFFICIAL_NOTIFICATION", "Fiscalía General del Estado",
            "EG 49/2026 / outgoing 230",
            "Official notice transmits the signed 8/9-June EG 49/2026 decision.",
            matter_references=["EG 49/2026"],
            linked_transport_event_ids=["PD-SP-EVT-1048"],
            transport_link_state="EXACT_OFFICIAL_NOTICE_TRANSPORT_LINKED",
            proof_level="OFFICIAL_NOTICE_LOCATED",
            attribution_state="INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0114", "2026-07-02", "INSTITUTIONAL_ACKNOWLEDGEMENT", "Fiscalía General del Estado — Secretaría Técnica",
            "ST 553/2026",
            "Signed acknowledgement act records central receipt/handling only.",
            linked_transport_event_ids=["PD-SP-EVT-1115"],
            transport_link_state="ACT_DATED_2_JULY_LINKED_TO_6_JULY_NOTICE_TRANSPORT",
            proof_level="SIGNED_ACKNOWLEDGEMENT_ACT_LOCATED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0115", "2026-07-06", "OFFICIAL_NOTIFICATION", "Fiscalía General del Estado — Secretaría Técnica",
            "ST 553/2026",
            "Official notice transmits the signed acknowledgement act.",
            linked_transport_event_ids=["PD-SP-EVT-1115"],
            transport_link_state="EXACT_OFFICIAL_NOTICE_TRANSPORT_LINKED",
            proof_level="OFFICIAL_NOTICE_LOCATED",
            attribution_state="INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0116", "2026-08-20", "OUTBOUND_COMMUNICATION", "Fiscalía General del Estado — Secretaría Técnica",
            "ST 553/2026 / ST 104/2025",
            "Later user-originated continuation communication is located as an email transmission, not a formal filing.",
            direction="OUTBOUND_TO_INSTITUTION", channel="OFFICIAL_EMAIL",
            matter_references=["ST 553/2026", "ST 104/2025"],
            linked_transport_event_ids=["PD-SP-EVT-1116"],
            transport_link_state="EXACT_OUTBOUND_TRANSPORT_LINKED",
            proof_level="EMAIL_TRANSMISSION_LOCATED_NOT_FORMAL_FILING",
        ),
        _mail_control_event(
            "PD-SP-EVT-0117", "2026-08-21", "INSTITUTIONAL_ACKNOWLEDGEMENT", "Fiscalía General del Estado — Secretaría Técnica",
            "ST 553/2026 / ST 104/2025",
            "Official acknowledgement proves central receipt and stated prospective handling only.",
            matter_references=["ST 553/2026", "ST 104/2025"],
            linked_transport_event_ids=["PD-SP-EVT-1117"],
            transport_link_state="EXACT_ACKNOWLEDGEMENT_TRANSPORT_LINKED",
            proof_level="OFFICIAL_ACKNOWLEDGEMENT_LOCATED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0118", "2026-08-26", "OFFICIAL_NOTIFICATION", "Fiscalía General del Estado — Inspección Fiscal",
            "E.G. 745/2026",
            "Official notice transmits the separately registered 26-August archive decree and review-route statement.",
            linked_transport_event_ids=["PD-SP-EVT-1063"],
            transport_link_state="EXACT_OFFICIAL_NOTICE_TRANSPORT_LINKED",
            proof_level="OFFICIAL_NOTICE_LOCATED",
            attribution_state="SOURCE_PROVED_SIGNATORY",
            signatory_person_id="PD-SP-P-0112",
            signatory_person_label="Olalla Vázquez Moraga",
        ),
        _mail_control_event(
            "PD-SP-EVT-0119", "2025-01-27", "INSTITUTIONAL_ACKNOWLEDGEMENT", "Fiscalía General del Estado — Atención al Ciudadano",
            "CC/CA 12/2025",
            "Official central citizen-attention correspondence is located; no merits disposition is inferred.",
            linked_transport_event_ids=["PD-SP-EVT-1001"],
            transport_link_state="EXACT_INBOUND_TRANSPORT_LINKED",
            proof_level="OFFICIAL_CORRESPONDENCE_LOCATED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0120", "2025-07-25", "INSTITUTIONAL_ACKNOWLEDGEMENT", "Fiscalía Especial contra la Corrupción y la Criminalidad Organizada",
            "EG 352/2025",
            "Official receipt/handling response is located; admission and merits are not inferred.",
            linked_transport_event_ids=["PD-SP-EVT-1089"],
            transport_link_state="EXACT_INBOUND_TRANSPORT_LINKED",
            proof_level="OFFICIAL_ACKNOWLEDGEMENT_LOCATED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0121", "2025-09-26", "OFFICIAL_NOTIFICATION", "Fiscalía Especial contra la Corrupción y la Criminalidad Organizada",
            "EG 352/2025",
            "Later official notice/reference in the same distinct expediente is located.",
            linked_transport_event_ids=["PD-SP-EVT-1058"],
            transport_link_state="EXACT_INBOUND_TRANSPORT_LINKED",
            proof_level="OFFICIAL_NOTICE_LOCATED",
            attribution_state="INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0122", "2026-08-20", "INSTITUTIONAL_ACKNOWLEDGEMENT", "Fiscalía Especial contra la Corrupción y la Criminalidad Organizada",
            "EG 352/2025 / REGAGE26e00070236245",
            "Official response states that admission remained pending a compliant electronic signature; it is a signature-cure checkpoint, not a merits rejection.",
            linked_transport_event_ids=["PD-SP-EVT-1060"],
            transport_link_state="EXACT_INBOUND_TRANSPORT_LINKED",
            proof_level="OFFICIAL_SIGNATURE_CURE_RESPONSE_LOCATED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0123", "2026-08-10", "OFFICIAL_ROUTING_ACT", "Fiscalía de la Audiencia Nacional",
            "EG 86/2026",
            "Signed initiation/archive-for-competence decision records territorial remittal to Arrecife.",
            linked_transport_event_ids=["PD-SP-EVT-1093"],
            transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED_TO_DECISION_PACKAGE",
            proof_level="SIGNED_ROUTING_ACT_LOCATED",
            attribution_state="INSTITUTION_ONLY_SIGNATURE_PENDING",
        ),
        _mail_control_event(
            "PD-SP-EVT-0124", "2026-08-10", "OFFICIAL_NOTIFICATION", "Fiscalía de la Audiencia Nacional",
            "EG 86/2026",
            "Official notice transmits the competence/remittal decision and controlled package.",
            linked_transport_event_ids=["PD-SP-EVT-1093"],
            transport_link_state="EXACT_OFFICIAL_NOTICE_TRANSPORT_LINKED",
            proof_level="OFFICIAL_NOTICE_LOCATED",
            attribution_state="INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0125", "2026-08-19", "OFFICIAL_DECISION", "Fiscalía de la Comunidad Autónoma de Canarias",
            "EG 112/2026",
            "Signed opening/archive decision is located; it is registered separately from the later clarification.",
            linked_transport_event_ids=["PD-SP-EVT-1099"],
            transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED_TO_DECISION_ATTACHMENT",
            proof_level="SIGNED_ACT_LOCATED",
            attribution_state="INSTITUTION_ONLY_SIGNATURE_PENDING",
        ),
        _mail_control_event(
            "PD-SP-EVT-0126", "2026-08-23", "OFFICIAL_DECISION", "Fiscalía de la Comunidad Autónoma de Canarias",
            "EG 112/2026",
            "Signed clarification recognises the historic aforado module while maintaining the stated classification and territorial route.",
            linked_transport_event_ids=["PD-SP-EVT-1031"],
            transport_link_state="25_AUGUST_NOTICE_TRANSPORT_LINKED_TO_23_AUGUST_CLARIFICATION",
            proof_level="SIGNED_CLARIFICATION_LOCATED",
            attribution_state="SOURCE_PROVED_SIGNATORY",
            signatory_person_id="PD-SP-P-0106",
            signatory_person_label="Jaime Serrano-Jover González",
        ),
        _mail_control_event(
            "PD-SP-EVT-0127", "2026-08-25", "OFFICIAL_NOTIFICATION", "Fiscalía de la Comunidad Autónoma de Canarias",
            "EG 112/2026",
            "Official notice transmits the clarification decision.",
            linked_transport_event_ids=["PD-SP-EVT-1031"],
            transport_link_state="EXACT_OFFICIAL_NOTICE_TRANSPORT_LINKED",
            proof_level="OFFICIAL_NOTICE_LOCATED",
            attribution_state="INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED",
        ),
        _mail_control_event(
            "PD-SP-EVT-0128", "2026-08-21", "OFFICIAL_DECISION", "Fiscalía Provincial de Santa Cruz de Tenerife",
            "EG 95/2026",
            "Signed decree opens and archives EG 95/2026 on the stated judicialisation/parallel-investigation reasoning.",
            linked_transport_event_ids=["PD-SP-EVT-1111"],
            transport_link_state="OFFICIAL_NOTICE_TRANSPORT_LINKED_TO_DECISION_ATTACHMENT",
            proof_level="SIGNED_ACT_LOCATED",
            attribution_state="SOURCE_PROVED_SIGNATORY",
            signatory_person_id="PD-SP-P-0107",
            signatory_person_label="José Luis Sánchez-Jáuregui y Alcaide",
        ),
        _mail_control_event(
            "PD-SP-EVT-0129", "2026-08-21", "OFFICIAL_NOTIFICATION", "Fiscalía Provincial de Santa Cruz de Tenerife",
            "EG 95/2026",
            "Official notice transmits the EG 95/2026 decree.",
            linked_transport_event_ids=["PD-SP-EVT-1111"],
            transport_link_state="EXACT_OFFICIAL_NOTICE_TRANSPORT_LINKED",
            proof_level="OFFICIAL_NOTICE_LOCATED",
            attribution_state="INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED",
        ),
    ]
)


for event_id, event_date, transport_id in (
    ("PD-SP-EVT-0130", "2025-02-20", "PD-SP-EVT-1072"),
    ("PD-SP-EVT-0131", "2025-02-27", "PD-SP-EVT-1074"),
    ("PD-SP-EVT-0132", "2025-06-13", "PD-SP-EVT-1077"),
    ("PD-SP-EVT-0133", "2025-06-13", "PD-SP-EVT-1078"),
    ("PD-SP-EVT-0134", "2025-12-18", "PD-SP-EVT-1080"),
):
    KEY_EVENTS.append(
        _mail_control_event(
            event_id,
            event_date,
            "INSTITUTIONAL_ACKNOWLEDGEMENT",
            "Fiscalía General del Estado — Secretaría Técnica",
            "ST 104/2025",
            "One of five separately located official ST 104/2025 acknowledgement checkpoints; receipt/handling only, not merits review.",
            linked_transport_event_ids=[transport_id],
            transport_link_state="EXACT_INBOUND_TRANSPORT_LINKED",
            proof_level="OFFICIAL_ACKNOWLEDGEMENT_LOCATED",
            event_sequence=f"ST104-ACK-{event_date}-{transport_id[-4:]}",
        )
    )


for event_id, reference in (
    ("PD-SP-EVT-0135", "REGAGE26e00070235399"),
    ("PD-SP-EVT-0136", "REGAGE26e00070236067"),
    ("PD-SP-EVT-0137", "REGAGE26e00070236245"),
    ("PD-SP-EVT-0138", "REGAGE26e00070236543"),
    ("PD-SP-EVT-0139", "REGAGE26e00070236749"),
    ("PD-SP-EVT-0140", "REGAGE26e00070237051"),
):
    KEY_EVENTS.append(
        _mail_control_event(
            event_id,
            "2026-08-02",
            "REGISTRATION_RECEIPT",
            "Ministerio Fiscal — seven-destination 2–3 August receipt family; one-to-one public office-label normalization pending",
            reference,
            "A distinct primary REG-AGE receipt in the seven-destination August family is controlled; its exact registration reference is independently rowed.",
            direction="OUTBOUND_TO_INSTITUTION",
            channel="REGAGE",
            matter_references=[reference, "E.G. 745/2026 wider Ministerio Fiscal submission family"],
            linked_transport_event_ids=["PD-SP-EVT-1113"],
            transport_link_state="PRIMARY_RECEIPT_COPY_LOCATED_IN_SEVEN_ATTACHMENT_SELF_ARCHIVE_TRANSPORT",
            proof_level="PRIMARY_REGISTRATION_RECEIPT_LOCATED; ONE_TO_ONE_PUBLIC_DESTINATION_LABEL_NORMALISATION_PENDING",
            evidence_state=deepcopy(RECEIPT_BOUNDARY),
        )
    )


def _authority_handling_state(kind: str) -> dict[str, str]:
    if kind == "REGISTRATION_RECEIPT":
        return {
            "transmission": "PROVEN",
            "registration": "PROVEN",
            "delivery": "OPEN",
            "routing": "OPEN",
            "incorporation": "OPEN",
            "examination": "OPEN",
            "verification_or_rejection": "NOT_PROVEN",
            "adoption": "NOT_PROVEN",
            "decision_or_use": "NOT_PROVEN",
            "effect": "NOT_PROVEN",
            "causation": "NOT_PROVEN",
            "benefit_or_loss": "NOT_PROVEN",
        }
    if kind == "ROUTING_NOTICE":
        return {
            "transmission": "PROVEN",
            "registration": "PROVEN",
            "delivery": "ONLY_AS_STATED_IN_SOURCE",
            "routing": "PROVEN_AS_STATED_IN_SOURCE",
            "incorporation": "OPEN",
            "examination": "OPEN",
            "verification_or_rejection": "NOT_PROVEN",
            "adoption": "NOT_PROVEN",
            "decision_or_use": "NOT_PROVEN",
            "effect": "NOT_PROVEN",
            "causation": "NOT_PROVEN",
            "benefit_or_loss": "NOT_PROVEN",
        }
    return {
        "transmission": "PROVEN",
        "registration": "ONLY_AS_STATED_IN_SOURCE",
        "delivery": "PROVEN_BY_LOCATED_RECEIPT_OR_NOTICE",
        "routing": "ONLY_AS_STATED_IN_SOURCE",
        "incorporation": "OPEN",
        "examination": "ONLY_AS_STATED_IN_SOURCE",
        "verification_or_rejection": "NOT_PROVEN",
        "adoption": "NOT_PROVEN",
        "decision_or_use": "ONLY_THE_LOCATED_PROCEDURAL_ACT",
        "effect": "NOT_PROVEN",
        "causation": "NOT_PROVEN",
        "benefit_or_loss": "NOT_PROVEN",
    }


def _authority_event(spec: dict[str, Any]) -> dict[str, Any]:
    record_type = str(spec["record_type"])
    handling_kind = str(spec.get("handling_kind", record_type))
    receipt = record_type == "REGISTRATION_RECEIPT"
    authority_metadata = {
        "institution_key": spec["institution_key"],
        "institution_caret_state": "CARET_CONFIRMED" if spec.get("institution_id") else "CARET_PENDING",
        "authority_tier_id": spec["authority_tier_id"],
        "tier_resolution_state": "CONFIRMED",
        "master_ids": spec.get("master_ids", []),
        "context_master_ids": spec.get("context_master_ids", []),
        "master_link_state": "RESOLVED" if spec.get("master_ids") else "OPEN",
        "authority_stage_ids": spec["authority_stage_ids"],
        "track_ids": spec["track_ids"],
        "gap_ids": spec["gap_ids"],
        "evidence_classes": spec["evidence_classes"],
        "handling_state": _authority_handling_state(handling_kind),
        "public_summary_es": spec["summary_es"],
        "proves_es": spec["proves_es"],
        "does_not_prove_es": spec["does_not_prove_es"],
        "canonical_anchor_es": f"es/ingenieria-inversa-criminal-unitaria/#communication-{spec['event_id']}",
        "canonical_anchor_en": f"en/unitary-criminal-reverse-engineering/#communication-{spec['event_id']}",
        "public_derivative_state": "PUBLIC_SAFE_MINIMISED_DERIVATIVE",
        "command_caret_audit": "EVENT_REGISTERED_IDENTITY_CARET_SEPARATELY_CONTROLLED",
        "criminal_relevance_state": "OPEN_HYPOTHESIS_LINK",
        "criminal_responsibility_transfer": False,
        "source_batch_id": "PD-SP-AUTH-COMMS-SCAN-20260901",
        "legacy_evidence_ids": spec.get("legacy_evidence_ids", []),
    }
    return _key_event(
        spec["event_id"],
        spec["event_date"],
        record_type,
        spec["direction"],
        spec["channel"],
        spec["office"],
        spec["official_reference"],
        spec["summary_en"],
        spec["source_anchor"],
        [spec["proves_en"]],
        [spec["does_not_prove_en"]],
        matter_references=spec.get("matter_references", [spec["official_reference"]]),
        evidence_state=deepcopy(RECEIPT_BOUNDARY) if receipt else None,
        attribution_state="INSTITUTIONAL_NOTICE_NO_PERSONAL_SIGNATORY_ASSERTED",
        transport_link_state="NO_PUBLIC_TRANSPORT_LINK_ASSERTED",
        proof_level=spec["proof_level"],
        institution_id=spec.get("institution_id"),
        authority_metadata=authority_metadata,
    )


_FUNDS_STAGES = ["AUTH-UCF-009"]
_FUNDS_TRACKS = ["T13", "T14", "T15", "T17", "T18"]
_FUNDS_GAPS = ["PD-GAP-UCF-009", "PD-GAP-UCF-012", "PD-GAP-UCF-015", "PD-GAP-UCF-016"]
_FUNDS_NOT_PROVED_EN = "Registration, notice or routing does not prove downstream receipt, incorporation, examination, adoption, reliance, a qualifying payment, misuse, personal knowledge, intent, causation, criminal organisation, offence or guilt."
_FUNDS_NOT_PROVED_ES = "El registro, aviso o traslado no prueba recepción posterior, incorporación, examen, adopción, utilización, pago elegible, uso indebido, conocimiento personal, dolo, causalidad, organización criminal, delito ni culpabilidad."


AUTHORITY_EVENT_SPECS: list[dict[str, Any]] = [
    {
        "event_id": "PD-SP-EVT-0141", "event_date": "2026-03-06", "record_type": "OFFICIAL_ROUTING_ACT",
        "handling_kind": "ROUTING_NOTICE", "direction": "INBOUND_FROM_INSTITUTION", "channel": "OFFICIAL_RESPONSE",
        "office": "Intervención General de la Comunidad Autónoma de Canarias", "institution_key": "INTERVENCION_GENERAL_EXACT",
        "authority_tier_id": "ES_CANARY_AUTONOMOUS", "official_reference": "184368/2026",
        "summary_en": "The first located response records Commission analysis, anonymised referral to Justice and stated public-grant control competence.",
        "summary_es": "La primera respuesta localizada consigna análisis de la Comisión, traslado anonimizado a Justicia y competencia declarada de control de subvenciones públicas.",
        "proves_en": "The official response and its stated Commission-analysis and referral steps are controlled.",
        "proves_es": "Se controlan la respuesta oficial y los pasos de análisis y traslado que declara.",
        "does_not_prove_en": _FUNDS_NOT_PROVED_EN, "does_not_prove_es": _FUNDS_NOT_PROVED_ES,
        "source_anchor": "es/intervencion-general-699645-2026/index.html", "proof_level": "OFFICIAL_RESPONSE_PUBLIC_SAFE_DERIVATIVE_LOCATED",
        "master_ids": ["X-INT-004"], "authority_stage_ids": ["AUTH-UCF-005", "AUTH-UCF-009", "AUTH-UCF-010"],
        "track_ids": ["T08", "T14", "T15", "T17", "T18"], "gap_ids": ["PD-GAP-UCF-015", "PD-GAP-UCF-016"],
        "evidence_classes": ["DOC", "NOTICE", "OPEN"], "legacy_evidence_ids": ["PD-EV-UCF-INT-184368-2026"],
    },
    {
        "event_id": "PD-SP-EVT-0142", "event_date": "2026-06-11", "record_type": "OFFICIAL_ROUTING_ACT",
        "handling_kind": "ROUTING_NOTICE", "direction": "INBOUND_FROM_INSTITUTION", "channel": "OFFICIAL_RESPONSE",
        "office": "Intervención General de la Comunidad Autónoma de Canarias", "institution_key": "INTERVENCION_GENERAL_EXACT",
        "authority_tier_id": "ES_CANARY_AUTONOMOUS", "official_reference": "497011/2026",
        "summary_en": "The second located response identifies the RIC lane, an AEAT report and a Canary decision, and states a transfer to the competent Finance office.",
        "summary_es": "La segunda respuesta localizada identifica el carril RIC, un informe AEAT y una decisión canaria, y declara el traslado al órgano competente de Hacienda.",
        "proves_en": "The response proves only its stated competence analysis and referral.", "proves_es": "La respuesta prueba únicamente el análisis competencial y traslado que declara.",
        "does_not_prove_en": _FUNDS_NOT_PROVED_EN, "does_not_prove_es": _FUNDS_NOT_PROVED_ES,
        "source_anchor": "es/intervencion-general-699645-2026/index.html", "proof_level": "OFFICIAL_RESPONSE_PUBLIC_SAFE_DERIVATIVE_LOCATED",
        "master_ids": ["X-INT-004"], "authority_stage_ids": _FUNDS_STAGES, "track_ids": _FUNDS_TRACKS, "gap_ids": _FUNDS_GAPS,
        "evidence_classes": ["DOC", "NOTICE", "OPEN"],
    },
    {
        "event_id": "PD-SP-EVT-0143", "event_date": "2026-08-19", "record_type": "OFFICIAL_NOTIFICATION",
        "direction": "INBOUND_FROM_INSTITUTION", "channel": "OFFICIAL_RESPONSE",
        "office": "Intervención General de la Comunidad Autónoma de Canarias", "institution_key": "INTERVENCION_GENERAL_EXACT",
        "authority_tier_id": "ES_CANARY_AUTONOMOUS", "official_reference": "699645/2026",
        "summary_en": "The third response narrows the Comptroller's remit and prevents treating 497011/2026 as a universal no-funds or no-files certificate.",
        "summary_es": "La tercera respuesta delimita el ámbito de Intervención e impide tratar 497011/2026 como certificado universal de inexistencia de fondos o expedientes.",
        "proves_en": "The located derivative controls the stated clarification and competence boundary.", "proves_es": "El derivado localizado controla la aclaración y el límite competencial declarados.",
        "does_not_prove_en": _FUNDS_NOT_PROVED_EN, "does_not_prove_es": _FUNDS_NOT_PROVED_ES,
        "source_anchor": "es/intervencion-general-699645-2026/index.html", "proof_level": "OFFICIAL_RESPONSE_PUBLIC_SAFE_DERIVATIVE_LOCATED_NATIVE_SIGNED_BINARY_OPEN",
        "master_ids": ["X-INT-004"], "authority_stage_ids": _FUNDS_STAGES, "track_ids": _FUNDS_TRACKS, "gap_ids": _FUNDS_GAPS,
        "evidence_classes": ["DOC", "NOTICE", "OPEN"],
    },
    {
        "event_id": "PD-SP-EVT-0144", "event_date": "2026-08-26", "record_type": "OFFICIAL_ROUTING_ACT",
        "handling_kind": "ROUTING_NOTICE", "direction": "INBOUND_FROM_INSTITUTION", "channel": "OFFICIAL_TRANSPARENCY_NOTICE",
        "office": "Canary Finance and EU Relations public-information unit", "institution_key": "CANARY_FEDER_TRANSPARENCY_ORGAN",
        "authority_tier_id": "ES_CANARY_AUTONOMOUS", "official_reference": "16/2026-0825121919",
        "summary_en": "The notice states that the request entered the Canary Finance public-information unit and was referred to the regional economic-promotion directorate.",
        "summary_es": "La notificación declara que la solicitud entró en la unidad de información pública de Hacienda y fue remitida a la dirección general regional de promoción económica.",
        "proves_en": "The notice proves the administrative description and referral stated in the notice.", "proves_es": "La notificación prueba la descripción administrativa y la remisión que en ella se declaran.",
        "does_not_prove_en": _FUNDS_NOT_PROVED_EN, "does_not_prove_es": _FUNDS_NOT_PROVED_ES,
        "source_anchor": "es/gobierno-canarias-transparencia-feder-remision-16-2026-0825121919/index.html", "proof_level": "OFFICIAL_NOTICE_REDACTED_DERIVATIVE_LOCATED",
        "master_ids": ["NAT-AID-001"], "authority_stage_ids": _FUNDS_STAGES, "track_ids": _FUNDS_TRACKS, "gap_ids": _FUNDS_GAPS,
        "evidence_classes": ["DOC", "NOTICE", "OPEN"],
    },
]


for number, reference, office, institution_key, institution_id, tier, master_ids, context_master_ids in (
    (145, "REGAGE26e00075132698", "Comisionado de Transparencia y Acceso a la Información Pública", "CANARY_TRANSPARENCY_COMMISSIONER", None, "ES_CANARY_AUTONOMOUS", ["LZ-TRA-028"], []),
    (146, "REGAGE26e00075135054", "Canary Presidency, Public Administrations, Justice and Security", "CANARY_PRESIDENCY_JUSTICE_RECIPIENT", None, "ES_CANARY_AUTONOMOUS", [], []),
    (147, "REGAGE26e00075135386", "Agencia Estatal de Administración Tributaria", "AEAT", "PD-SP-I-0006", "ES_STATE", [], []),
    (148, "REGAGE26e00075135813", "Canary regional-incentives registry destination", "CANARY_REGIONAL_INCENTIVES_RECIPIENT", None, "ES_CANARY_AUTONOMOUS", ["NAT-AID-001"], []),
    (149, "REGAGE26e00075136198", "Spanish State regional-incentives directorate", "STATE_REGIONAL_INCENTIVES_RECIPIENT", None, "ES_STATE", ["NAT-AID-001"], []),
    (150, "REGAGE26e00075136446", "Canary Finance and EU Relations registry destination", "CANARY_FEDER_RECIPIENT", None, "ES_CANARY_AUTONOMOUS", [], ["NAT-AID-001"]),
    (151, "REGAGE26e00075136691", "Spanish Directorate-General for European Funds", "STATE_EUROPEAN_FUNDS_DIRECTORATE", None, "ES_STATE", [], ["NAT-AID-001"]),
    (152, "REGAGE26e00075136953", "Comisión Nacional del Mercado de Valores", "CNMV", None, "ES_STATE", [], ["X-REG-001", "NAT-CNMV-001", "NAT-CNMV-002"]),
):
    AUTHORITY_EVENT_SPECS.append({
        "event_id": f"PD-SP-EVT-{number:04d}", "event_date": "2026-08-24", "record_type": "REGISTRATION_RECEIPT",
        "direction": "OUTBOUND_TO_INSTITUTION", "channel": "REGAGE", "office": office, "institution_key": institution_key,
        "institution_id": institution_id, "authority_tier_id": tier, "official_reference": reference,
        "summary_en": "One of eight separately registered RICPE, regional-incentives and European-funds access routes; the receipt is controlled at registration level.",
        "summary_es": "Una de ocho rutas de acceso RICPE, incentivos regionales y fondos europeos registradas por separado; el acuse se controla al nivel de registro.",
        "proves_en": "The receipt proves formal presentation to the registry destination and time stated on the receipt.",
        "proves_es": "El acuse prueba la presentación formal al destino registral y en el momento que declara.",
        "does_not_prove_en": _FUNDS_NOT_PROVED_EN, "does_not_prove_es": _FUNDS_NOT_PROVED_ES,
        "source_anchor": "es/ricpe-acciones-pendientes-ahora/index.html", "proof_level": "PRIMARY_REGISTRATION_RECEIPT_LOCATED_PUBLIC_SAFE_SUMMARY",
        "master_ids": master_ids, "context_master_ids": context_master_ids, "authority_stage_ids": _FUNDS_STAGES,
        "track_ids": _FUNDS_TRACKS, "gap_ids": _FUNDS_GAPS, "evidence_classes": ["NOTICE", "OPEN"],
    })


AUTHORITY_EVENT_SPECS.extend([
    {
        "event_id": "PD-SP-EVT-0153", "event_date": "2026-08-05", "record_type": "OFFICIAL_NOTIFICATION",
        "direction": "INBOUND_FROM_INSTITUTION", "channel": "OFFICIAL_MUNICIPAL_NOTICE", "office": "Ayuntamiento de Yaiza",
        "institution_key": "AYUNTAMIENTO_DE_YAIZA", "institution_id": "PD-SP-I-0009", "authority_tier_id": "ES_LOCAL_MUNICIPAL",
        "official_reference": "7066/2026", "summary_en": "A source-controlled municipal notification identifies archive-funds consultation file 7066/2026.",
        "summary_es": "Una notificación municipal controlada identifica el expediente 7066/2026 de consulta de fondos del archivo.",
        "proves_en": "The official notification, date and municipal file reference are controlled.", "proves_es": "Se controlan la notificación oficial, la fecha y la referencia del expediente municipal.",
        "does_not_prove_en": "The notice does not prove a complete file, title, authority, valid licence, reliance on an ACTA, intent, offence or guilt.",
        "does_not_prove_es": "La notificación no prueba expediente completo, título, autoridad, licencia válida, utilización de un ACTA, dolo, delito ni culpabilidad.",
        "source_anchor": "assets/data/proceedings-master-public-v1.json", "proof_level": "OFFICIAL_NOTIFICATION_MASTER_RECONCILED",
        "master_ids": ["LZ-YAI-031"], "authority_stage_ids": ["AUTH-UCF-010"], "track_ids": ["T16", "T17", "T18"],
        "gap_ids": ["PD-GAP-UCF-010", "PD-GAP-UCF-015"], "evidence_classes": ["DOC", "NOTICE", "OPEN"],
    },
    {
        "event_id": "PD-SP-EVT-0154", "event_date": "2026-08-13", "record_type": "REGISTRATION_RECEIPT",
        "direction": "OUTBOUND_TO_INSTITUTION", "channel": "REGAGE", "office": "Cabildo de Lanzarote",
        "institution_key": "CABILDO_DE_LANZAROTE", "institution_id": "PD-SP-I-0010", "authority_tier_id": "ES_ISLAND_CABILDO",
        "official_reference": "REGAGE26e00072883405", "summary_en": "The receipt records a request to implement access in file 614/2026 and obtain four identified tourism files.",
        "summary_es": "El acuse consigna una solicitud de ejecución del acceso en el expediente 614/2026 y de obtención de cuatro expedientes turísticos identificados.",
        "proves_en": "The receipt proves formal presentation of the stated access request to the Cabildo registry.",
        "proves_es": "El acuse prueba la presentación formal de la solicitud de acceso indicada al registro del Cabildo.",
        "does_not_prove_en": "It does not prove internal assignment, delivery of the files, ACTA reliance, valid title or authority, intent, offence or guilt.",
        "does_not_prove_es": "No prueba asignación interna, entrega de expedientes, utilización de ACTAS, título o autoridad válidos, dolo, delito ni culpabilidad.",
        "source_anchor": "es/cabildo-lanzarote-turismo-trazabilidad/index.html", "proof_level": "PRIMARY_REGISTRATION_RECEIPT_PUBLIC_SUMMARY_LOCATED",
        "master_ids": ["LZ-CAB-025"], "authority_stage_ids": ["AUTH-UCF-010"], "track_ids": ["T16", "T17", "T18"],
        "gap_ids": ["PD-GAP-UCF-010", "PD-GAP-UCF-015"], "evidence_classes": ["NOTICE", "OPEN"],
    },
    {
        "event_id": "PD-SP-EVT-0155", "event_date": "2026-08-28", "record_type": "OFFICIAL_NOTIFICATION",
        "direction": "INBOUND_FROM_INSTITUTION", "channel": "OFFICIAL_TREASURY_DELIVERY", "office": "Canary Directorate-General for the Treasury and Financial Policy",
        "institution_key": "CANARY_TREASURY_DG", "authority_tier_id": "ES_CANARY_AUTONOMOUS", "official_reference": "Colabora 7-2026-0316134247",
        "summary_en": "The signed implementation notice records partial access moving into staged delivery, including the first controlled tranche.",
        "summary_es": "La notificación firmada de ejecución consigna el paso del acceso parcial a entrega escalonada, incluida la primera tanda controlada.",
        "proves_en": "The notice proves the stated implementation act and first staged production state.", "proves_es": "La notificación prueba el acto de ejecución y el estado de primera producción escalonada que declara.",
        "does_not_prove_en": _FUNDS_NOT_PROVED_EN, "does_not_prove_es": _FUNDS_NOT_PROVED_ES,
        "source_anchor": "es/tesoro-transparencia-7-2026-28agosto/index.html", "proof_level": "SIGNED_IMPLEMENTATION_ACT_AND_PUBLIC_SAFE_PRODUCTION_CONTROL_LOCATED",
        "master_ids": ["NAT-TES-001"], "authority_stage_ids": _FUNDS_STAGES, "track_ids": ["T13", "T14", "T17", "T18"],
        "gap_ids": ["PD-GAP-UCF-009", "PD-GAP-UCF-012", "PD-GAP-UCF-015"], "evidence_classes": ["DOC", "NOTICE", "OPEN"],
    },
    {
        "event_id": "PD-SP-EVT-0156", "event_date": "2026-07-30", "record_type": "REGISTRATION_RECEIPT",
        "direction": "OUTBOUND_TO_INSTITUTION", "channel": "REGAGE", "office": "SNCA / AFCOS registry route",
        "institution_key": "SNCA", "authority_tier_id": "ES_STATE", "official_reference": "REGAGE26e00069678966",
        "summary_en": "A controlled registration receipt is linked to the Spanish national antifraud-coordination file 141-2026-IRR02.",
        "summary_es": "Un acuse de registro controlado se vincula al expediente español de coordinación antifraude 141-2026-IRR02.",
        "proves_en": "The receipt proves formal presentation to the stated Spanish registry route.", "proves_es": "El acuse prueba la presentación formal a la ruta registral española indicada.",
        "does_not_prove_en": _FUNDS_NOT_PROVED_EN, "does_not_prove_es": _FUNDS_NOT_PROVED_ES,
        "source_anchor": "es/snca-fondos-europeos-trazabilidad/index.html", "proof_level": "PRIMARY_REGISTRATION_RECEIPT_REFERENCE_CONTROLLED",
        "master_ids": ["X-EU-003"], "authority_stage_ids": _FUNDS_STAGES, "track_ids": _FUNDS_TRACKS, "gap_ids": _FUNDS_GAPS,
        "evidence_classes": ["NOTICE", "OPEN"],
    },
    {
        "event_id": "PD-SP-EVT-0157", "event_date": "2026-07-30", "record_type": "INSTITUTIONAL_ACKNOWLEDGEMENT",
        "direction": "INBOUND_FROM_INSTITUTION", "channel": "OFFICIAL_RESPONSE", "office": "SNCA / AFCOS",
        "institution_key": "SNCA", "authority_tier_id": "ES_STATE", "official_reference": "141-2026-IRR02",
        "summary_en": "The located response identifies the file and supplies general channel and competence material; the concrete EU-funds nexus and treatment remain open.",
        "summary_es": "La respuesta localizada identifica el expediente y aporta material general sobre canal y competencia; el nexo concreto con fondos UE y su tratamiento siguen abiertos.",
        "proves_en": "The identifiable file and the response's stated channel and scope are controlled.", "proves_es": "Se controlan el expediente identificable y el canal y alcance declarados por la respuesta.",
        "does_not_prove_en": _FUNDS_NOT_PROVED_EN, "does_not_prove_es": _FUNDS_NOT_PROVED_ES,
        "source_anchor": "es/snca-fondos-europeos-trazabilidad/index.html", "proof_level": "OFFICIAL_RESPONSE_PUBLIC_SUMMARY_LOCATED",
        "master_ids": ["X-EU-003"], "authority_stage_ids": _FUNDS_STAGES, "track_ids": _FUNDS_TRACKS, "gap_ids": _FUNDS_GAPS,
        "evidence_classes": ["DOC", "NOTICE", "OPEN"],
    },
])


KEY_EVENTS.extend(_authority_event(spec) for spec in AUTHORITY_EVENT_SPECS)


EU_BASELINE_AUTHORITY_ENRICHMENTS: dict[str, dict[str, Any]] = {
    event_id: {
        "institution_key": "EUROPEAN_PUBLIC_PROSECUTOR_OFFICE_EXACT",
        "institution_caret_state": "CARET_PENDING",
        "authority_tier_id": "EU_SUPRANATIONAL",
        "tier_resolution_state": "CONFIRMED",
        "master_ids": [],
        "context_master_ids": [],
        "master_link_state": "OPEN",
        "authority_stage_ids": ["AUTH-UCF-009"],
        "track_ids": ["T15", "T17", "T18"],
        "gap_ids": ["PD-GAP-UCF-009", "PD-GAP-UCF-012", "PD-GAP-UCF-015", "PD-GAP-UCF-016"],
        "evidence_classes": ["NOTICE", "OPEN"],
        "handling_state": _authority_handling_state("REGISTRATION_RECEIPT"),
        "public_summary_es": "Acuse REGAGE dirigido a la Fiscalía Europea; prueba presentación registral, no entrega interna ni examen de fondo.",
        "proves_es": "Prueba la presentación formal al destino registral indicado en el acuse.",
        "does_not_prove_es": "No prueba reparto, incorporación, examen, investigación, adopción, nexo con fondos UE, delito ni culpabilidad.",
        "canonical_anchor_es": f"es/ingenieria-inversa-criminal-unitaria/#communication-{event_id}",
        "canonical_anchor_en": f"en/unitary-criminal-reverse-engineering/#communication-{event_id}",
        "public_derivative_state": "PUBLIC_SAFE_MINIMISED_DERIVATIVE",
        "command_caret_audit": "EVENT_REGISTERED_IDENTITY_CARET_SEPARATELY_CONTROLLED",
        "criminal_relevance_state": "OPEN_HYPOTHESIS_LINK",
        "criminal_responsibility_transfer": False,
        "source_batch_id": "PD-SP-AUTH-COMMS-SCAN-20260901",
        "legacy_evidence_ids": [],
    }
    for event_id in ("PD-SP-EVT-0004", "PD-SP-EVT-0014")
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def subject_digest(label: str) -> str:
    normalized = unicodedata.normalize("NFC", label.strip())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def subject_category(label: str) -> str:
    normalized = "".join(
        character for character in unicodedata.normalize("NFKD", label.casefold()) if not unicodedata.combining(character)
    )
    rules = (
        (("informacion y copia", "información y copia", "copia –", "copia -"), "INFORMATION_OR_COPY_REQUEST"),
        (("trazabilidad", "certificacion", "certificación", "saip"), "TRACEABILITY_OR_CERTIFICATION_REQUEST"),
        (("preservacion", "preservación", "custodia"), "PRESERVATION_OR_CUSTODY_REQUEST"),
        (("denuncia penal", "ampliacion denuncia", "ampliación denuncia"), "CRIMINAL_NOTICE_OR_AMPLIFICATION"),
        (("aportacion", "aportación", "documentacion", "documentación"), "EVIDENCE_OR_DOCUMENT_CONTRIBUTION"),
        (("impulso", "valoracion", "valoración", "revision", "revisión"), "REVIEW_OR_INVESTIGATIVE_IMPULSE"),
        (("remision", "remisión", "traslado", "inhibicion", "inhibición"), "ROUTING_OR_REMITTAL"),
        (("comunicacion institucional", "comunicación institucional"), "INSTITUTIONAL_COMMUNICATION"),
    )
    for needles, category in rules:
        if any(needle in normalized for needle in needles):
            return category
    return "OTHER_FORMAL_REGISTRATION_LABEL"


def load_source_rows(path: Path, expected_count: int | None = BASELINE_EXPECTED) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"Source_Pages", "Presented", "REGAGE", "Recipient", "Subject", "Annexes"}
    if not rows or set(rows[0]) != required:
        raise ValueError(f"unexpected source columns: {set(rows[0]) if rows else set()}")
    if expected_count is not None and len(rows) != expected_count:
        raise ValueError(f"expected {expected_count} detailed source rows; found {len(rows)}")

    normalized: list[dict[str, Any]] = []
    seen: dict[str, dict[str, Any]] = {}
    for row in rows:
        reference = row["REGAGE"].strip()
        if not re.fullmatch(r"REGAGE\d{2}e\d{11}", reference):
            raise ValueError(f"invalid REGAGE reference: {reference}")
        recipient = row["Recipient"].strip()
        if recipient not in RECIPIENTS:
            raise ValueError(f"recipient lacks controlled DIR3 mapping: {recipient}")
        presented = datetime.strptime(row["Presented"].strip(), "%d/%m/%Y %H:%M:%S")
        item = {
            "source_pages": row["Source_Pages"].strip(),
            "presented": presented,
            "official_reference": reference,
            "office": recipient,
            "source_subject": row["Subject"].strip(),
            "annex_count": int(row["Annexes"]),
        }
        if reference in seen:
            if seen[reference] != item:
                raise ValueError(f"conflicting duplicate REGAGE reference: {reference}")
            raise ValueError(f"duplicate REGAGE reference: {reference}")
        seen[reference] = item
        normalized.append(item)
    return sorted(normalized, key=lambda item: (item["presented"], item["official_reference"]))


def load_mailbox_index(path: Path) -> dict[str, Any]:
    value = load_json(path)
    if value is None:
        raise ValueError(f"public mailbox index missing: {path}")
    if value.get("schema") != "por-derecho.institutional-communications-mailbox-index.v1":
        raise ValueError("unexpected public mailbox-index schema")
    custody = value.get("source_custody", {})
    expected_custody = {
        "custody_reference": "PD-SP-CUST-0001",
        "manifest_sha256": PRIVATE_MANIFEST_SHA256,
        "manifest_rows": PRIVATE_MANIFEST_ROWS,
        "mailbox_event_rows": MAILBOX_EXPECTED,
        "baseline_receipt_rows": BASELINE_EXPECTED,
        "persistence_status": "PERSISTED_PRIVATE_CUSTODY",
        "provider_or_storage_identifier_published": False,
    }
    if custody != expected_custody:
        raise ValueError("public mailbox-index custody control mismatch")
    events = value.get("events")
    if not isinstance(events, list) or len(events) != MAILBOX_EXPECTED:
        raise ValueError(f"expected {MAILBOX_EXPECTED} public mailbox rows")
    ids = [event.get("event_id") for event in events]
    keys = [event.get("public_event_match_key") for event in events]
    if len(set(ids)) != MAILBOX_EXPECTED or len(set(keys)) != MAILBOX_EXPECTED:
        raise ValueError("public mailbox event IDs/match keys are not unique")
    return value


def mailbox_evidence_state(direction: str, route: str) -> dict[str, str]:
    destination = "CONTROLLED_OFFICE_CLASS_ONLY" if route != "ROUTE_NOT_PUBLICLY_ATTESTED" else "ROUTE_NOT_PUBLICLY_ATTESTED"
    if direction == "OUTBOUND_EMAIL":
        transmission = "SENT_EMAIL_LOCATED"
    elif direction == "INBOUND_EMAIL":
        transmission = "RECEIVED_EMAIL_LOCATED"
    elif direction == "SELF_ARCHIVE":
        transmission = "SELF_ARCHIVE_CONTROL_NOT_AN_INSTITUTIONAL_SEND"
    else:
        transmission = "DRAFT_NOT_SENT"
    return {
        "transmission": transmission,
        "registration": "NOT_ESTABLISHED_BY_EMAIL_TRANSPORT",
        "filing": "NOT_ESTABLISHED_BY_EMAIL_TRANSPORT",
        "destination": destination,
        "delivery": "NOT_ESTABLISHED_BEYOND_THE_LOCATED_TRANSPORT_STATE",
        "internal_association": "NOT_ESTABLISHED_BY_EMAIL_TRANSPORT",
        "substantive_examination": "NOT_ESTABLISHED_BY_EMAIL_TRANSPORT",
        "merits": "NOT_ESTABLISHED_BY_EMAIL_TRANSPORT",
    }


def build_mailbox_events(index: dict[str, Any], index_sha256: str) -> list[dict[str, Any]]:
    direction_map = {
        "OUTBOUND_EMAIL": "OUTBOUND_TO_INSTITUTION",
        "INBOUND_EMAIL": "INBOUND_FROM_INSTITUTION",
        "SELF_ARCHIVE": "SELF_ARCHIVE_CONTROL",
        "DRAFT": "NON_SENT_DRAFT",
    }
    record_type_map = {
        "OUTBOUND_EMAIL": "EMAIL_TRANSPORT",
        "INBOUND_EMAIL": "EMAIL_TRANSPORT",
        "SELF_ARCHIVE": "SELF_ARCHIVE_CONTROL",
        "DRAFT": "EMAIL_DRAFT",
    }
    events: list[dict[str, Any]] = []
    for source in index["events"]:
        direction = str(source["direction"])
        route = str(source["office_route"])
        references = list(source.get("official_references", []))
        events.append(
            {
                "event_id": source["event_id"],
                "cohort": MAILBOX_COHORT,
                "layer": "TRANSPORT",
                "source_key": f"MAILBOX:{source['public_event_match_key']}",
                "record_type": record_type_map[direction],
                "event_date": source["event_date"],
                "event_timestamp": source["event_timestamp"],
                "direction": direction_map[direction],
                "channel": "EMAIL",
                "institution_id": "PD-SP-I-0002",
                "office": route,
                "official_reference": " / ".join(references) if references else "NO_PUBLIC_SAFE_REFERENCE",
                "public_match_key": source["public_event_match_key"],
                "transport_state": source["transport_state"],
                "route_proof_state": source["route_proof_state"],
                "subject_category": source["subject_category"],
                "subject_digest_sha256": source["subject_digest_sha256"],
                "subject_text_published": False,
                "attachment_count": source["attachment_count"],
                "attachment_count_basis": source["attachment_count_basis"],
                "public_summary": source["proof_ceiling"],
                "matter_references": references,
                "source_integrity": {
                    "status": "PRIVATE_NATIVE_EVENT_LOCATED_PUBLIC_SAFE_DERIVATIVE",
                    "repository_anchor": "assets/data/institutional-communications-mailbox-index-v1.json",
                    "sha256": index_sha256,
                },
                "attribution_state": "NO_PERSON_ATTRIBUTED_IN_PUBLIC_REGISTER",
                "linked_transport_event_ids": [],
                "transport_link_state": "THIS_ROW_IS_THE_TRANSPORT_LAYER",
                "proof_level": source["transport_state"],
                "evidence_state": mailbox_evidence_state(direction, route),
                "proves": [source["proof_ceiling"]],
                "does_not_prove": [
                    "Coordination, obstruction, capture, favouritism, prevarication, criminality or merits correctness without additional actor-specific evidence."
                ],
            }
        )
    return events


# Source-controlled additive notice cohort; canonical register remains authoritative.
from prepare_orion_notice_register_20260905 import load_notice_events
KEY_EVENTS.extend(load_notice_events(REPO_ROOT))


def _existing_receipt_ids(register: dict[str, Any] | None) -> dict[str, str]:
    if not register:
        return {}
    mapping: dict[str, str] = {}
    for event in register.get("events", []):
        if event.get("cohort") != BASELINE_COHORT:
            continue
        reference = event.get("official_reference")
        event_id = event.get("event_id")
        if isinstance(reference, str) and isinstance(event_id, str):
            mapping[reference] = event_id
    return mapping


def _used_event_numbers(register: dict[str, Any] | None) -> set[int]:
    used: set[int] = set()
    sources: Iterable[dict[str, Any]] = [] if not register else register.get("events", [])
    for event in [*sources, *KEY_EVENTS]:
        match = EVENT_ID_RE.fullmatch(str(event.get("event_id", "")))
        if match:
            used.add(int(match.group(1)))
    return used


def build_receipt_events(rows: list[dict[str, Any]], existing: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    id_by_reference = _existing_receipt_ids(existing)
    used = _used_event_numbers(existing)
    next_number = 1

    def allocate() -> str:
        nonlocal next_number
        while next_number in used:
            next_number += 1
        if next_number > 9999:
            raise ValueError("PD-SP-EVT namespace exhausted")
        used.add(next_number)
        result = f"PD-SP-EVT-{next_number:04d}"
        next_number += 1
        return result

    events: list[dict[str, Any]] = []
    for row in rows:
        event_id = id_by_reference.get(row["official_reference"]) or allocate()
        dir3, institution_id = RECIPIENTS[row["office"]]
        event = {
                "event_id": event_id,
                "cohort": BASELINE_COHORT,
                "layer": "FORMAL_REGISTRATION",
                "source_key": f"REGAGE:{row['official_reference']}",
                "record_type": "REGISTRATION_RECEIPT",
                "event_date": row["presented"].date().isoformat(),
                "presented_local": row["presented"].isoformat(timespec="seconds"),
                "source_timezone": "NOT_STATED_IN_RECEIPT_INDEX",
                "direction": "OUTBOUND_TO_INSTITUTION",
                "channel": "REGAGE",
                "institution_id": institution_id,
                "office": row["office"],
                "recipient_dir3": dir3,
                "official_reference": row["official_reference"],
                "subject_category": subject_category(str(row["source_subject"])),
                "subject_digest_sha256": subject_digest(str(row["source_subject"])),
                "subject_label_status": "FORMAL_REGISTRATION_LABEL_IN_CANONICAL_SOURCE_NOT_REPEATED_HERE",
                "source_pages": row["source_pages"],
                "annex_count": row["annex_count"],
                "matter_references": [],
                "source_integrity": {
                    "status": "PRIMARY_RECEIPT_INDEXED_IN_PUBLIC_SAFE_DERIVATIVE",
                    "repository_anchor": "archive/evidence/mf-redsara-anexo4/MF_REDSARA_REGISTRATION_INDEX_SHORT.csv",
                    "controlling_source_pdf_sha256": REGISTER_SOURCE_PDF_SHA256,
                },
                "evidence_state": deepcopy(RECEIPT_BOUNDARY),
                "proves": [
                    "The stated text and annex metadata were formally registered at the stated time to the stated registry destination."
                ],
                "does_not_prove": [
                    "Truth of the submission's allegations.",
                    "Delivery beyond the registry state shown, internal assignment, joinder, examination, admission, investigation, merits acceptance or requested relief.",
                ],
            }
        if event_id in EU_BASELINE_AUTHORITY_ENRICHMENTS:
            event.update(deepcopy(EU_BASELINE_AUTHORITY_ENRICHMENTS[event_id]))
        events.append(event)
    return events


def base_register() -> dict[str, Any]:
    return {
        "schema": "por-derecho.institutional-communications-register.v1",
        "register_id": "PD-SP-INSTITUTIONAL-COMMUNICATIONS-001",
        "control_date": "2026-09-01",
        "scope": {
            "institution": "Multi-authority register; Fiscalía baseline retained as one controlled cohort",
            "focus_case": "Unitary Sun Park / LPB / RICPE authority, public-funds and ACTA continuity",
            "purpose": "Canonical public-safe continuity register for source-proved transport, registration, decision, notice, routing and production events across local, island, autonomous, State and EU tiers.",
            "interpretive_boundary": "Adverse outcomes, silence, routing gaps, repeated institutional contact and cross-tier communication do not prove coordination, obstruction, prevarication, criminal organisation, offence or guilt without actor-specific evidence.",
        },
        "denominator_control": {
            "wider_regage_records_reported": 97,
            "reported_received": 90,
            "reported_rejected": 7,
            "detailed_baseline_receipt_rows_expected": 75,
            "detailed_baseline_receipt_rows_registered": 75,
            "metadata_only_records_reported": 22,
            "metadata_only_representation": "ONE_UNRESOLVED_BATCH_NOT_22_SYNTHETIC_EVENTS",
            "arithmetic_check": "75 detailed + 22 metadata-only = 97 reported total",
            "private_manifest_rows": PRIVATE_MANIFEST_ROWS,
            "private_manifest_baseline_receipt_rows": BASELINE_EXPECTED,
            "private_manifest_mailbox_event_rows": MAILBOX_EXPECTED,
            "mailbox_outbound_email_rows": 42,
            "mailbox_inbound_email_rows": 101,
            "mailbox_self_archive_rows": 10,
            "mailbox_draft_rows": 3,
            "mailbox_route_not_publicly_attested_rows": 81,
            "public_authority_communication_events": 19,
            "new_public_authority_communication_events": 17,
        },
        "authority_scan_control": {
            "checkpoint_path": "ops/PUBLIC_AUTHORITY_COMMUNICATIONS_SCAN_CHECKPOINT_20260901.json",
            "checkpoint_sha256": sha256_file(AUTHORITY_SCAN_CHECKPOINT),
            "scope_status": "BOUNDED_METADATA_CENSUS_COMPLETE_ITEM_LEVEL_MERITS_REVIEW_OPEN",
            "gmail_unique_messages_across_lanes": 5514,
            "drive_unique_documents_across_lanes": 326,
            "canonical_authority_events": 19,
            "new_event_ids": [f"PD-SP-EVT-{number:04d}" for number in range(141, 158)],
            "existing_reused_event_ids": ["PD-SP-EVT-0004", "PD-SP-EVT-0014"],
            "universal_completeness_claim": False,
        },
        "source_controls": {
            "detailed_index": "archive/evidence/mf-redsara-anexo4/MF_REDSARA_REGISTRATION_INDEX_SHORT.csv",
            "detailed_index_sha256": BASELINE_SOURCE_SHA256,
            "controlling_154_page_pdf_sha256": REGISTER_SOURCE_PDF_SHA256,
            "public_safe_transcript_sha256": PUBLIC_TRANSCRIPT_SHA256,
            "detailed_row_count": 75,
            "annex_listing_count": 126,
            "mailbox_index": "assets/data/institutional-communications-mailbox-index-v1.json",
            "mailbox_event_row_count": MAILBOX_EXPECTED,
            "private_custody_manifest_sha256": PRIVATE_MANIFEST_SHA256,
            "private_custody_manifest_row_count": PRIVATE_MANIFEST_ROWS,
        },
        "private_locator_boundary": {
            "status": "ENFORCED",
            "public_register_contains": [
                "official references, dates, public-safe receipt subjects, stated offices, DIR3 codes, repository anchors and evidence-status boundaries"
            ],
            "public_register_excludes": [
                "mailbox provider message/thread identifiers, Gmail or Drive URLs, exact private mailbox subjects or bodies, direct contact details, access tokens and vault locators"
            ],
            "reconciliation_order": [
                "exact official registration or expediente reference",
                "source-controlled document hash where publication is authorised",
                "date + direction + office + public-safe subject digest inside a private workspace only",
            ],
            "custody_rule": "Provider locators and private-message fingerprints remain outside the public repository; their absence here is intentional, not a source gap.",
            "custody_manifest": {
                "custody_reference": "PD-SP-CUST-0001",
                "status": "PERSISTED_PRIVATE_CUSTODY",
                "manifest_sha256": PRIVATE_MANIFEST_SHA256,
                "manifest_row_count": PRIVATE_MANIFEST_ROWS,
                "provider_or_storage_identifier_published": False,
            },
        },
        "id_namespace_authority": {
            "policy_path": ".github/evidence-intelligence/id-extension-policy.json",
            "extension": "EVENT",
            "declared_pattern": "^PD-SP-EVT-[0-9]{4}$",
            "status": "DECLARED_IN_EXISTING_POLICY_AND_VALIDATED",
        },
        "id_allocation": {
            "pattern": "PD-SP-EVT-####",
            "baseline_rule": "The 75 detailed receipts retain their first assigned IDs by official REGAGE reference.",
            "extension_rule": "A genuinely new public-safe event receives the lowest unused ID; existing IDs are never renumbered.",
            "mailbox_rule": "Mailbox transport rows use the stable public match key and the reserved PD-SP-EVT-1001+ allocation band; existing IDs are never renumbered.",
        },
        "events": [],
        "unresolved_batches": [
            {
                "batch_id": "MF-UNRESOLVED-BATCH-001",
                "description": "Later RedSARA/AGE records represented only by aggregate metadata in the controlled 97-record total.",
                "record_count": 22,
                "aggregate_received_count": 15,
                "aggregate_rejected_count": 7,
                "individual_identity_status": "NOT_AVAILABLE_IN_PUBLIC_SAFE_DETAILED_SOURCE",
                "individual_status_allocation": "NOT_CREATED_OR_INFERRED",
                "synthetic_event_rows_created": 0,
                "resolution_gate": "Add individual rows only from a source-proved receipt/status export, preserving any rejection state exactly.",
                "source_anchor": "archive/MF_EXTRACONCURSAL_REQUERIMIENTO_31JUL2026_FULL_TEXT_20AUG2026.md",
            }
        ],
        "continuity_rules": [
            "Reconcile this register and checkpoint before rescanning previously covered mail or evidence bundles.",
            "A sent email, draft, webpage or repository publication is not a legal filing receipt.",
            "A registration receipt proves formal presentation to the stated registry, not downstream delivery, association, examination, admission or merits.",
            "Never create one event per aggregate-only record without individual source proof.",
            "Never publish provider identifiers or private custody locators.",
            "Transport, formal registration and official-act layers remain distinct and are linked rather than collapsed.",
            "Each authority event must preserve jurisdictional tier separately from funding subject; Spanish SNCA and the Spanish Directorate-General for European Funds are State-tier, not EU institutions.",
            "Every receipt-to-decision step requires its own source: transmission, registration, delivery, routing, incorporation, examination, verification or rejection, adoption, decision, effect, causation and benefit remain separate.",
            "The caret marker remains identity-only; communication events receive stable IDs and bilingual anchors, never presentation carets.",
            "Criminal relevance may be linked as an open hypothesis, but criminal responsibility never transfers through an ACTA, communication, referral, office or institutional tier.",
        ],
    }


def reconcile_register(
    rows: list[dict[str, Any]],
    mailbox_index: dict[str, Any],
    mailbox_index_sha256: str,
    existing: dict[str, Any] | None = None,
) -> dict[str, Any]:
    register = base_register()
    receipts = build_receipt_events(rows, existing)
    key_events = deepcopy(KEY_EVENTS)
    mailbox_events = build_mailbox_events(mailbox_index, mailbox_index_sha256)

    event_ids = [event["event_id"] for event in receipts + key_events + mailbox_events]
    if len(event_ids) != len(set(event_ids)):
        raise ValueError("event ID collision during reconciliation")
    source_keys = [event["source_key"] for event in receipts + key_events + mailbox_events]
    if len(source_keys) != len(set(source_keys)):
        raise ValueError("source-key collision during reconciliation")

    register["events"] = sorted(receipts + key_events + mailbox_events, key=lambda event: event["event_id"])
    register["denominator_control"]["curated_source_proved_events"] = len(key_events)
    register["denominator_control"]["mailbox_transport_events"] = len(mailbox_events)
    register["denominator_control"]["event_rows_total"] = len(register["events"])
    register["source_controls"]["mailbox_index_sha256"] = mailbox_index_sha256
    return register


def build_checkpoint(register_sha256: str, source_sha256: str, mailbox_index_sha256: str) -> dict[str, Any]:
    return {
        "schema": "por-derecho.institutional-communications-scan-checkpoint.v1",
        "checkpoint_id": "PD-SP-MF-SCAN-CHECKPOINT-001",
        "control_date": "2026-09-01",
        "register_path": "assets/data/institutional-communications-register-v1.json",
        "register_sha256": register_sha256,
        "private_custody": {
            "custody_reference": "PD-SP-CUST-0001",
            "status": "PERSISTED_PRIVATE_CUSTODY",
            "manifest_sha256": PRIVATE_MANIFEST_SHA256,
            "manifest_rows": PRIVATE_MANIFEST_ROWS,
            "provider_or_storage_identifier_published": False,
        },
        "mailbox_index": {
            "source_path": "assets/data/institutional-communications-mailbox-index-v1.json",
            "source_sha256": mailbox_index_sha256,
            "event_rows": MAILBOX_EXPECTED,
            "outbound_email_rows": 42,
            "inbound_email_rows": 101,
            "self_archive_rows": 10,
            "draft_rows": 3,
            "route_not_publicly_attested_rows": 81,
            "source_exhausted": True,
        },
        "baseline_import": {
            "source_path": "archive/evidence/mf-redsara-anexo4/MF_REDSARA_REGISTRATION_INDEX_SHORT.csv",
            "source_sha256": source_sha256,
            "expected_rows": 75,
            "imported_rows": 75,
            "unique_regage_references": 75,
            "annex_listings": 126,
            "first_presented_local": "2025-12-15T20:53:36",
            "last_presented_local": "2026-02-26T22:35:27",
            "source_exhausted": True,
        },
        "aggregate_only_control": {
            "reported_rows": 22,
            "representation": "MF-UNRESOLVED-BATCH-001",
            "synthetic_event_rows": 0,
        },
        "public_authority_scan": {
            "checkpoint_path": "ops/PUBLIC_AUTHORITY_COMMUNICATIONS_SCAN_CHECKPOINT_20260901.json",
            "checkpoint_sha256": sha256_file(AUTHORITY_SCAN_CHECKPOINT),
            "scope_status": "BOUNDED_METADATA_CENSUS_COMPLETE_ITEM_LEVEL_MERITS_REVIEW_OPEN",
            "gmail_unique_messages_across_lanes": 5514,
            "drive_unique_documents_across_lanes": 326,
            "existing_event_ids_reused": ["PD-SP-EVT-0004", "PD-SP-EVT-0014"],
            "new_event_ids": [f"PD-SP-EVT-{number:04d}" for number in range(141, 158)],
            "canonical_authority_event_count": 19,
            "provider_locators_or_exact_subjects_published": False,
            "universal_completeness_claim": False,
        },
        "source_required_and_normalisation_gates": [
            "22 later RedSARA/AGE records remain aggregate-only; no synthetic individual rows were created.",
            "EG 58/2026 discrete official act remains source-required.",
            "DP 1901/2026 signed Fiscal report and later judicial act remain source-required.",
            "EG 6/2026 underlying act substantive digest remains pending.",
            "Six August-family receipt rows await one-to-one public destination-label normalisation; no destination is guessed.",
            "81 mailbox rows retain ROUTE_NOT_PUBLICLY_ATTESTED pending a primary bridge.",
            "No post-notification E.G. 745/2026 reposicion receipt was located.",
        ],
        "last_month_mail_control": {
            "performed_date": "2026-08-31",
            "covered_date_from": "2026-07-31",
            "covered_date_through": "2026-08-31",
            "scope": "Ministerio Fiscal offices and controlled expediente/REGAGE references; Gmail plus REG-AGE filing-proof control.",
            "pagination_complete": True,
            "provider_locators_published": False,
            "result": "No post-notification E.G. 745/2026 reposicion, matching REG-AGE receipt or equivalent merits-filing proof located.",
            "source_anchor": "evidence/fiscalia/2026/MINISTERIO_FISCAL_WIDER_MATTER_EG745_UNITARY_EVIDENCE_ACTION_DIGEST_31AUG2026.md",
        },
        "incremental_refresh_2026_08_31": {
            "performed_at_utc": "2026-08-31T14:12:58Z",
            "scope": "Control-day overlap query for Ministerio Fiscal, Fiscalia, E.G. 745/2026 and REG-AGE references after the pagination-complete last-month scan.",
            "pagination_complete": True,
            "search_hits": 11,
            "already_indexed_in_scope_events": 7,
            "new_in_scope_institutional_events": 0,
            "excluded_automated_repository_notifications": 4,
            "exclusion_reason": "Automated GitHub list notifications matched only because repository text mentioned Ministerio Fiscal; they are not communications to or from a public institution and are not added to the institutional register or native-source manifest.",
            "new_filing_proof": False,
            "filing_status_change": False,
            "provider_locators_or_exact_subjects_published": False,
        },
        "next_incremental_scan": {
            "overlap_from_date": "2026-08-24",
            "strictly_new_after_date": "2026-08-31",
            "rule": "Scan an overlap window, reconcile exact official references first, then add only source-proved public-safe events; keep private provider IDs outside Git.",
        },
    }


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def run(args: argparse.Namespace) -> int:
    source = args.source_index.resolve()
    mailbox_index_path = args.mailbox_index.resolve()
    register_path = args.register.resolve()
    checkpoint_path = args.checkpoint.resolve()
    source_sha256 = sha256_file(source)
    if source == DEFAULT_SOURCE.resolve() and source_sha256 != BASELINE_SOURCE_SHA256:
        raise ValueError(
            f"canonical source index hash drift: expected {BASELINE_SOURCE_SHA256}, found {source_sha256}"
        )
    rows = load_source_rows(source, args.expected_count)
    mailbox_index = load_mailbox_index(mailbox_index_path)
    mailbox_index_sha256 = sha256_file(mailbox_index_path)
    existing = load_json(register_path)
    expected_register = reconcile_register(rows, mailbox_index, mailbox_index_sha256, existing)
    register_bytes = canonical_json_bytes(expected_register)
    register_sha256 = hashlib.sha256(register_bytes).hexdigest()
    expected_checkpoint = build_checkpoint(register_sha256, source_sha256, mailbox_index_sha256)
    checkpoint_bytes = canonical_json_bytes(expected_checkpoint)

    if args.check:
        failures: list[str] = []
        if not register_path.exists() or register_path.read_bytes() != register_bytes:
            failures.append(str(register_path))
        if not checkpoint_path.exists() or checkpoint_path.read_bytes() != checkpoint_bytes:
            failures.append(str(checkpoint_path))
        if failures:
            print("reconciliation drift:", *failures, sep="\n  - ", file=sys.stderr)
            return 1
        print(
            f"OK: {len(rows)} baseline receipts; {len(mailbox_index['events'])} mailbox transport events; "
            f"{len(KEY_EVENTS)} curated events; "
            "22 aggregate-only records remain one unresolved batch"
        )
        return 0

    write_bytes(register_path, register_bytes)
    write_bytes(checkpoint_path, checkpoint_bytes)
    print(f"wrote {register_path}")
    print(f"wrote {checkpoint_path}")
    print(f"register sha256 {register_sha256}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true", help="write the deterministic register and checkpoint")
    mode.add_argument("--check", action="store_true", help="fail if either generated file has drifted")
    parser.add_argument("--source-index", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--mailbox-index", type=Path, default=DEFAULT_MAILBOX_INDEX)
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument("--expected-count", type=int, default=BASELINE_EXPECTED)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        return run(parse_args(argv))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

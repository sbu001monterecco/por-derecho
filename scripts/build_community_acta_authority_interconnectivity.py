#!/usr/bin/env python3
"""Build the public ACTA / 2022 parallel-track / authority-file graph.

The output is a deterministic navigation and audit projection.  It deliberately
keeps Community authority, judicial approval, deed/Registry implementation,
public-authority receipt and criminal characterisation on separate proof axes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ACTA_INDEX = ROOT / "evidence/community/actas/public-index.json"
MASTER = ROOT / "assets/data/proceedings-master-public-v1.json"
PRISM = ROOT / "assets/data/proceedings-case-prism-v1.json"
DECISIONS = ROOT / "archive/judicial-intelligence/decisions.jsonl"
POST7JUNE = ROOT / "assets/data/sun-park-post-7june-2018-2022-continuing-harm-v1.json"
ASSERTIONS = ROOT / "assets/data/community-acta-authority-link-assertions-v1.json"
COMMUNICATIONS = ROOT / "assets/data/institutional-communications-register-v1.json"
AUTHORITY_SCAN = ROOT / "ops/PUBLIC_AUTHORITY_COMMUNICATIONS_SCAN_CHECKPOINT_20260901.json"
UNITARY = ROOT / "assets/data/unitary-multitrack-criminal-first-gap-closure-v1.json"
INSTITUTIONS = ROOT / "assets/data/matter-identity-registry-v1.institutions.json"
TARGET = ROOT / "assets/data/community-acta-authority-interconnectivity-v1.json"

EXPECTED_ACTAS = 20
EXPECTED_AUTHORITIES = 49
EXPECTED_ADJUDICATION_DECISIONS = 5
EXPECTED_AUTHORITY_COMMUNICATIONS = 19

AUTHORITY_TIERS = [
    {
        "id": "ES_LOCAL_MUNICIPAL",
        "label_en": "Local / municipal",
        "label_es": "Local / municipal",
        "boundary_en": "A municipal receipt or act proves only the municipal event and source-bounded handling stated; it does not decide private title, criminal liability or another tier's treatment.",
        "boundary_es": "Un acuse o acto municipal prueba solo el evento municipal y el tratamiento delimitado por la fuente; no decide título privado, responsabilidad penal ni el tratamiento de otro nivel.",
    },
    {
        "id": "ES_ISLAND_CABILDO",
        "label_en": "Island / Cabildo",
        "label_es": "Insular / Cabildo",
        "boundary_en": "Tourism administration and private property are distinct; registry presentation does not prove file delivery, title, authority or reliance.",
        "boundary_es": "La administración turística y la propiedad privada son distintas; la presentación registral no prueba entrega, título, autoridad ni utilización.",
    },
    {
        "id": "ES_CANARY_AUTONOMOUS",
        "label_en": "Canary autonomous administration",
        "label_es": "Administración autonómica canaria",
        "boundary_en": "Separate Canary departments retain separate competence, files and proof chains; one referral is not whole-government knowledge or adoption.",
        "boundary_es": "Los departamentos canarios conservan competencias, expedientes y cadenas probatorias separadas; un traslado no es conocimiento ni adopción de todo el Gobierno.",
    },
    {
        "id": "ES_STATE",
        "label_en": "Spanish State administration",
        "label_es": "Administración estatal española",
        "boundary_en": "A European-funds subject does not turn a Spanish State body into an EU institution; receipt and competence remain organ-specific.",
        "boundary_es": "La materia de fondos europeos no convierte a un órgano estatal español en institución UE; recepción y competencia siguen siendo específicas de cada órgano.",
    },
    {
        "id": "EU_SUPRANATIONAL",
        "label_en": "European Union institution",
        "label_es": "Institución de la Unión Europea",
        "boundary_en": "A REGAGE destination receipt does not establish internal EU delivery, EPPO or OLAF competence, investigation, merits review or liability.",
        "boundary_es": "Un acuse dirigido por REGAGE no acredita entrega interna UE, competencia de Fiscalía Europea u OLAF, investigación, examen de fondo ni responsabilidad.",
    },
]

DECISION_ES = {
    "C36-E044": {
        "safe": "Aprobó definitivamente la propuesta de CAM tras consignar la incomparecencia y falta de depósito de la garantía por el tercer licitador.",
        "not": "No completó por sí solo firmeza, cálculo lícito de deuda, escritura, costes, comunicación al juzgado, cancelaciones, Registro, contabilidad ni pretensión alguna sobre activos de Matkator o terceros.",
    },
    "C36-E046": {
        "safe": "Desestimó las impugnaciones de LPB/Aweswell y confirmó la aprobación de 18 de mayo, describiendo un procedimiento de mejora de oferta y no una subasta formal.",
        "not": "No probó por sí solo cumplimiento, deuda final, escritura, inscripción, cancelación, contabilidad ni remanente.",
    },
    "C36-E047": {
        "safe": "Desestimó por pérdida sobrevenida de objeto las impugnaciones a la providencia de 12 de mayo, con terminología de subasta/adjudicación aclarada después.",
        "not": "La fecha compartida con el otro Auto de 15 de octubre no fusiona instrumentos; este acto no amplió activos ni probó cumplimiento posterior.",
    },
    "C36-E050": {
        "safe": "Aclaró que el evento relativo a la providencia de 12 de mayo fue una comparecencia de licitación para mejora de oferta, no una subasta.",
        "not": "Fue solo aclaración: no hizo la aprobación original, una nueva adjudicación, transmisión, decisión sobre contraprestación, ampliación de activos ni cálculo de remanente.",
    },
    "C36-E051": {
        "safe": "Aclaró y completó el otro Auto de 15 de octubre y consignó que la publicidad dominical de julio de 2021 fue planteada pero considerada irrelevante para realizar las fincas identificadas.",
        "not": "Fue solo aclaración: la mención no es un pronunciamiento de título sobre todo el hotel, nueva adjudicación, transmisión, determinación de deuda ni decisión sobre remanente.",
    },
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_decisions() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    with DECISIONS.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            canonical = record.get("canonical_record")
            if canonical:
                result[canonical] = record
    return result


def authority_group(master_id: str, assertions: dict[str, Any]) -> dict[str, Any]:
    matches = [
        group
        for group in assertions["authority_groups"]
        if any(master_id.startswith(prefix) for prefix in group["prefixes"])
    ]
    if len(matches) != 1:
        raise ValueError(f"{master_id} must match exactly one authority group, found {len(matches)}")
    return matches[0]


def prism_memberships(prism: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    memberships: dict[str, list[dict[str, str]]] = defaultdict(list)
    for proposition in prism["propositions"]:
        for lane_id, cell in proposition["cells"].items():
            for master_id in cell.get("master_ids", []):
                memberships[master_id].append(
                    {
                        "proposition_id": proposition["id"],
                        "title_en": proposition["title_en"],
                        "title_es": proposition["title_es"],
                        "lane_id": lane_id,
                        "status": cell["status"],
                        "treatment": cell["treatment"],
                    }
                )
    return memberships


def build() -> dict[str, Any]:
    acta_index = load_json(ACTA_INDEX)
    master = load_json(MASTER)
    prism = load_json(PRISM)
    post7june = load_json(POST7JUNE)
    assertions = load_json(ASSERTIONS)
    communications = load_json(COMMUNICATIONS)
    authority_scan = load_json(AUTHORITY_SCAN)
    unitary = load_json(UNITARY)
    institutions = load_json(INSTITUTIONS)
    decisions = load_decisions()

    tier_ids = {tier["id"] for tier in AUTHORITY_TIERS}
    identity_ids = {record["id"] for record in institutions["records"]}
    unitary_stage_ids = {stage["id"] for stage in unitary["authority_legitimacy_propagation"]["stages"]}
    unitary_track_ids = {track["id"] for track in unitary["tracks"]}
    unitary_gap_ids = {gap["id"] for gap in unitary["gaps"]}
    authority_communication_events = sorted(
        (event for event in communications["events"] if event.get("authority_tier_id")),
        key=lambda event: event["event_id"],
    )
    if len(authority_communication_events) != EXPECTED_AUTHORITY_COMMUNICATIONS:
        raise ValueError(
            f"expected {EXPECTED_AUTHORITY_COMMUNICATIONS} canonical authority communications, "
            f"found {len(authority_communication_events)}"
        )
    if [event["event_id"] for event in authority_communication_events] != authority_scan["canonical_event_ids"]:
        raise ValueError("authority communication IDs do not reconcile to the bounded scan checkpoint")

    master_ids_all = {record["Master_ID"] for record in master["records"]}
    events_by_master: dict[str, list[str]] = defaultdict(list)
    public_communications: list[dict[str, Any]] = []
    by_evidence_id: dict[str, dict[str, Any]] = {}
    tier_counts: Counter[str] = Counter()
    for event in authority_communication_events:
        event_id = event["event_id"]
        tier_id = event["authority_tier_id"]
        if tier_id not in tier_ids:
            raise ValueError(f"{event_id} has unknown authority tier {tier_id}")
        tier_counts[tier_id] += 1
        master_ids = event.get("master_ids", [])
        context_master_ids = event.get("context_master_ids", [])
        unknown_master_ids = (set(master_ids) | set(context_master_ids)) - master_ids_all
        if unknown_master_ids:
            raise ValueError(f"{event_id} has unknown Master IDs: {sorted(unknown_master_ids)}")
        if not set(event.get("authority_stage_ids", [])).issubset(unitary_stage_ids):
            raise ValueError(f"{event_id} has unknown unitary authority stage")
        if not set(event.get("track_ids", [])).issubset(unitary_track_ids):
            raise ValueError(f"{event_id} has unknown unitary track")
        if not set(event.get("gap_ids", [])).issubset(unitary_gap_ids):
            raise ValueError(f"{event_id} has unknown unitary gap")
        if event.get("institution_caret_state") == "CARET_CONFIRMED" and event.get("institution_id") not in identity_ids:
            raise ValueError(f"{event_id} has an unresolved confirmed institution ID")
        for master_id in master_ids:
            events_by_master[master_id].append(event_id)
        projection = {
            "event_id": event_id,
            "legacy_evidence_ids": event.get("legacy_evidence_ids", []),
            "date": event["event_date"],
            "direction": event["direction"],
            "channel": event["channel"],
            "record_type": event["record_type"],
            "official_reference": event["official_reference"],
            "primary_authority_tier_id": tier_id,
            "tier_resolution_state": event["tier_resolution_state"],
            "institution_label": event["office"],
            "institution_id": event.get("institution_id") if event.get("institution_caret_state") == "CARET_CONFIRMED" else None,
            "institution_identity_state": event["institution_caret_state"],
            "master_ids": master_ids,
            "context_master_ids": context_master_ids,
            "master_link_state": event["master_link_state"],
            "authority_stage_ids": event["authority_stage_ids"],
            "track_ids": event["track_ids"],
            "gap_ids": event["gap_ids"],
            "evidence_classes": event["evidence_classes"],
            "handling_state": event["handling_state"],
            "source_anchor": event["source_integrity"]["repository_anchor"],
            "proves_en": " ".join(event["proves"]),
            "proves_es": event["proves_es"],
            "does_not_prove_en": " ".join(event["does_not_prove"]),
            "does_not_prove_es": event["does_not_prove_es"],
            "summary_en": event.get("public_summary") or " ".join(event["proves"]),
            "summary_es": event["public_summary_es"],
            "canonical_anchor_es": event["canonical_anchor_es"],
            "canonical_anchor_en": event["canonical_anchor_en"],
            "public_derivative_state": event["public_derivative_state"],
            "criminal_relevance_state": event["criminal_relevance_state"],
            "criminal_responsibility_transfer": event["criminal_responsibility_transfer"],
        }
        public_communications.append(projection)
        by_evidence_id[event_id] = {
            "primary_authority_tier_id": tier_id,
            "institution_identity_state": event["institution_caret_state"],
            "master_ids": master_ids,
            "authority_stage_ids": event["authority_stage_ids"],
            "track_ids": event["track_ids"],
            "gap_ids": event["gap_ids"],
            "canonical_anchor_es": event["canonical_anchor_es"],
            "canonical_anchor_en": event["canonical_anchor_en"],
        }

    acta_items = sorted(acta_index["items"], key=lambda item: (item["date"], item["id"]))
    if len(acta_items) != EXPECTED_ACTAS:
        raise ValueError(f"expected {EXPECTED_ACTAS} public ACTA packages, found {len(acta_items)}")

    actas = []
    for item in acta_items:
        public_slug = "2022-03-11-ricpe" if item["id"] == "SP-MEETING-2022-03-11-RICPE" else item["slug"]
        actas.append(
            {
                "id": item["id"],
                "date": item["date"],
                "title_en": item["title_en"],
                "title_es": item["title_es"],
                "body": item["body"],
                "meeting_type": item["meeting_type"],
                "status": item["status"],
                "source_document_id": item.get("source_document_id", ""),
                "source_pages": item.get("source_pages"),
                "manual_source_line_verification": item.get("manual_source_line_verification", False),
                "route_en": f"en/community-instrumentalisation/acta-document-room/{public_slug}/",
                "route_es": f"es/comunidad-instrumentalizacion/sala-documental-actas/{public_slug}/",
                "manifest": item["manifest_path"],
                "limitations_en": item.get("source_variant_note_en", "") + " OCR is not certified line by line.",
                "limitations_es": item.get("source_variant_note_es", "") + " El OCR no está certificado línea por línea.",
                "proposition_links": [
                    {
                        "proposition_id": "P10",
                        "relationship_type": "COMMUNITY_AUTHORITY_SOURCE_FAMILY",
                        "boundary_en": "The ACTA package is a source for event-specific authority analysis, not proof of validity, service, complete attendance or later use.",
                        "boundary_es": "El paquete de ACTA es fuente para analizar la autoridad de cada evento, no prueba de validez, notificación, asistencia completa ni uso posterior.",
                    }
                ],
            }
        )

    allowed_types = set(assertions["authority_record_types"])
    memberships = prism_memberships(prism)
    authority_rows = sorted(
        (record for record in master["records"] if record["Record_Type"] in allowed_types),
        key=lambda record: record["Master_ID"],
    )
    if len(authority_rows) != EXPECTED_AUTHORITIES:
        raise ValueError(f"expected {EXPECTED_AUTHORITIES} public-authority records, found {len(authority_rows)}")

    authority_files = []
    by_master_id: dict[str, Any] = {}
    group_counts: Counter[str] = Counter()
    for row in authority_rows:
        group = authority_group(row["Master_ID"], assertions)
        group_counts[group["id"]] += 1
        links = memberships.get(row["Master_ID"], [])
        communication_event_ids = sorted(events_by_master.get(row["Master_ID"], []))
        linked_events = [by_evidence_id[event_id] for event_id in communication_event_ids]
        unitary_links: dict[str, Any] = {}
        if communication_event_ids:
            unitary_links = {
                "communication_event_ids": communication_event_ids,
                "unitary_authority_stage_ids": sorted({value for event in linked_events for value in event["authority_stage_ids"]}),
                "unitary_gap_ids": sorted({value for event in linked_events for value in event["gap_ids"]}),
            }
        if row["Master_ID"] == "X-INT-004":
            unitary_links["canonical_evidence_refs"] = [
                "PD-EV-UCF-INT-184368-2026", "PD-SP-EVT-0141", "PD-SP-EVT-0142", "PD-SP-EVT-0143"
            ]
        authority_file = {
            "master_id": row["Master_ID"],
            "record_type": row["Record_Type"],
            "stream": row["Stream"],
            "organ": row["Origin_Organ"],
            "current_custodian": row["Current_Custodian"],
            "reference": row["Reference"],
            "period": row["Date_or_Period"],
            "connection": row["Connection"],
            "object": row["Object_or_Purpose"],
            "status": row["Status"],
            "source_status": row["Source_Status"],
            "open_reference_gap": row["Open_Reference_Gap"],
            "group_id": group["id"],
            "axis_ids": group["axis_ids"],
            "proposition_links": links,
            "relationship_strength": "DEPENDENCY_TEST_ONLY",
            "boundary_en": group["boundary_en"],
            "boundary_es": group["boundary_es"],
            **unitary_links,
        }
        authority_files.append(authority_file)
        by_master_id[row["Master_ID"]] = {
            "group_id": group["id"],
            "axis_ids": group["axis_ids"],
            "proposition_ids": sorted({link["proposition_id"] for link in links}),
            "relationship_strength": "DEPENDENCY_TEST_ONLY",
            "boundary_en": "This reciprocal link exposes the applicable evidence questions; it does not prove ACTA delivery, receipt, examination, reliance, knowledge or merits.",
            "boundary_es": "Este enlace recíproco expone las preguntas probatorias aplicables; no prueba entrega, recepción, examen, utilización, conocimiento ni fondo del ACTA.",
            **unitary_links,
        }

    selected_decisions = []
    for canonical_id in assertions["adjudication_decision_ids"]:
        record = decisions.get(canonical_id)
        if not record:
            raise ValueError(f"missing canonical adjudication decision {canonical_id}")
        selected_decisions.append(
            {
                "id": canonical_id,
                "date": record["date"],
                "kind_en": record["decision_type"],
                "kind_es": record["decision_type"],
                "source_status": record["source_status"],
                "safe_en": record["decided"],
                "safe_es": DECISION_ES[canonical_id]["safe"],
                "not_established_en": record["not_decided"],
                "not_established_es": DECISION_ES[canonical_id]["not"],
                "source_anchor": "archive/judicial-intelligence/decisions.jsonl",
            }
        )
    if len(selected_decisions) != EXPECTED_ADJUDICATION_DECISIONS:
        raise ValueError("adjudication-decision denominator changed")
    selected_decisions.append({**assertions["deed_milestone"], "source_status": "VERIFIED_PRIMARY"})

    meeting = post7june["meeting_2022_02_04"]
    if meeting["source_id"] != "SP-ACTA-2022-02-04" or meeting["days_before_deed_457"] != 17:
        raise ValueError("2022 meeting/deed control changed")
    community_milestones = [
        {
            "id": "SP-ACTA-2022-02-04-ATTENDANCE",
            "date": "2022-02-04",
            "kind_en": "Recorded attendance and voting frame",
            "kind_es": "Marco consignado de asistencia y votación",
            "safe_en": "The located copy records 20.993% present or represented and unanimity among those present for the stated resolutions.",
            "safe_es": "La copia localizada consigna 20,993 % presente o representado y unanimidad entre los presentes para los acuerdos indicados.",
            "not_established_en": "It does not establish the complete owner/title denominator, lawful notice, proxies, vote qualification, validity, a controlled minority or criminal agreement.",
            "not_established_es": "No acredita el denominador completo de propietarios/título, convocatoria válida, poderes, habilitación de voto, validez, minoría controlada ni acuerdo criminal.",
            "source_anchor": "evidence/community/actas/2022-02-04/transcript-es.md",
        },
        {
            "id": "SP-ACTA-2022-02-04-DEBT",
            "date": "2022-02-04",
            "kind_en": "Debt approval and collection authority recorded",
            "kind_es": "Aprobación de deuda y autorización de cobro consignadas",
            "safe_en": "The ACTA records that balances were explained, approved unanimously among attendees and that the president was authorised to claim them.",
            "safe_es": "El ACTA consigna que los saldos fueron explicados, aprobados por unanimidad de asistentes y que se autorizó al presidente para reclamarlos.",
            "not_established_en": "Accuracy, enforceability, notice, certification, payment, fabrication, false documentation, author, knowledge, intent and single satisfaction are not established.",
            "not_established_es": "No están acreditados exactitud, exigibilidad, notificación, certificación, pago, fabricación, falsedad documental, autoría, conocimiento, intención ni satisfacción única.",
            "source_anchor": "evidence/community/actas/2022-02-04/transcript-es.md",
        },
        {
            "id": "SP-ACTA-2022-02-04-PROJECT",
            "date": "2022-02-04",
            "kind_en": "Sole CAM project, licences and unitary operation recorded",
            "kind_es": "Único proyecto CAM, licencias y unidad de explotación consignados",
            "safe_en": "The ACTA records only the CAM works project as submitted, approves it among attendees, authorises public permissions and a Cabildo request for all units/places and unitary tourism operation, and records a CAM-funded four-star conversion proposal.",
            "safe_es": "El ACTA consigna como presentado solo el proyecto de obras de CAM, lo aprueba entre asistentes, autoriza permisos públicos y solicitud al Cabildo para todas las unidades/plazas y explotación turística unitaria, y registra una propuesta de conversión a cuatro estrellas a coste de CAM.",
            "not_established_en": "Community competence over every private unit, lawful cost allocation, title, implementation, public-authority receipt, approval, funding, benefit capture, causal coordination or criminality is not established.",
            "not_established_es": "No están acreditados competencia comunitaria sobre cada finca privada, imputación lícita de costes, título, ejecución, recepción/aprobación por autoridad, financiación, captura de beneficio, coordinación causal ni delito.",
            "source_anchor": "evidence/community/actas/2022-02-04/transcript-es.md",
        },
    ]

    authority_groups = []
    for group in assertions["authority_groups"]:
        authority_groups.append(
            {
                "id": group["id"],
                "label_en": group["label_en"],
                "label_es": group["label_es"],
                "axis_ids": group["axis_ids"],
                "record_count": group_counts[group["id"]],
                "boundary_en": group["boundary_en"],
                "boundary_es": group["boundary_es"],
            }
        )

    axes = assertions["evidentiary_axes"]
    axis_ids = {axis["id"] for axis in axes}
    for group in authority_groups:
        if not set(group["axis_ids"]).issubset(axis_ids):
            raise ValueError(f"unknown axis in authority group {group['id']}")

    source_files = [
        ACTA_INDEX, MASTER, PRISM, DECISIONS, POST7JUNE, ASSERTIONS,
        COMMUNICATIONS, AUTHORITY_SCAN, UNITARY, INSTITUTIONS,
    ]
    return {
        "schema_version": "1.0.0",
        "generated": "2026-09-01",
        "status": "PUBLIC_SAFE_DERIVED_INTERCONNECTIVITY_PROJECTION",
        "title_en": "Community ACTAs, the 2022 parallel track and public-authority files",
        "title_es": "ACTAs comunitarias, vía paralela de 2022 y expedientes de autoridades públicas",
        "scope_en": assertions["scope_en"],
        "scope_es": assertions["scope_es"],
        "global_boundary_en": assertions["global_boundary_en"],
        "global_boundary_es": assertions["global_boundary_es"],
        "sources": [
            {"path": str(path.relative_to(ROOT)), "sha256": sha256(path)} for path in source_files
        ],
        "coverage": {
            "public_acta_packages": len(actas),
            "public_authority_files": len(authority_files),
            "authority_groups": len(authority_groups),
            "evidentiary_axes": len(axes),
            "community_2022_milestones": len(community_milestones),
            "adjudication_and_deed_milestones": len(selected_decisions),
            "verified_primary_authority_files": sum(file["source_status"] == "VERIFIED_PRIMARY" for file in authority_files),
            "verified_procedural_authority_files": sum(file["source_status"] == "VERIFIED_PROCEDURAL" for file in authority_files),
            "open_or_primary_pending_authority_files": sum(file["source_status"] in {"OPEN_REFERENCE", "CORPUS_REPORTED_PRIMARY_PENDING"} for file in authority_files),
            "public_authority_communication_events": len(public_communications),
            "authority_tiers_represented": sum(tier_counts[tier["id"]] > 0 for tier in AUTHORITY_TIERS),
            "confirmed_identity_communication_events": sum(event["institution_identity_state"] == "CARET_CONFIRMED" for event in public_communications),
            "pending_identity_communication_events": sum(event["institution_identity_state"] == "CARET_PENDING" for event in public_communications),
        },
        "actas": actas,
        "authority_tiers": [
            {**tier, "event_count": tier_counts[tier["id"]]} for tier in AUTHORITY_TIERS
        ],
        "public_communications": public_communications,
        "by_evidence_id": by_evidence_id,
        "communication_scan_control": {
            **communications["authority_scan_control"],
            "proof_boundary_en": authority_scan["proof_boundary"],
            "proof_boundary_es": "Los resultados de búsqueda son pistas. Transporte, registro, entrega, remisión, incorporación, examen, adopción, utilización, conocimiento, dolo, causalidad y responsabilidad requieren fuentes separadas.",
            "responsibility_boundary_en": "Apparent authority and documents may propagate as inputs; criminal responsibility never propagates through an ACTA, communication, referral, office or tier.",
            "responsibility_boundary_es": "La autoridad aparente y los documentos pueden propagarse como insumos; la responsabilidad penal nunca se propaga por ACTA, comunicación, traslado, órgano o nivel.",
        },
        "authority_groups": authority_groups,
        "authority_files": authority_files,
        "by_master_id": by_master_id,
        "parallel_2022": {
            "relationship_type": "TEMPORAL_AND_SUBJECT_MATTER_COMPARISON_ONLY",
            "days_from_acta_to_deed": meeting["days_before_deed_457"],
            "community_track": community_milestones,
            "adjudication_track": selected_decisions,
            "shared_proposition_ids": ["P10", "P11", "P14", "P15", "P18"],
            "boundary_en": "The ACTA was recorded 17 days before deed 457. Date and shared asset/project subject matter permit comparison and source production; they do not prove causal use, coordination, notice, knowledge, intent or wrongdoing.",
            "boundary_es": "El ACTA se consignó 17 días antes de la escritura 457. La fecha y la materia compartida de activos/proyecto permiten comparación y producción de fuentes; no prueban uso causal, coordinación, notificación, conocimiento, intención ni ilicitud.",
        },
        "evidentiary_axes": axes,
        "attributed_allegation": {
            "status": "SERIOUS_FALSIFIABLE_PARTY_ALLEGATION_NOT_ESTABLISHED",
            "en": meeting["deliberate_non_notice_hypothesis"]["allegation"],
            "es": "Gil Marer y Aweswell alegan que intereses relevantes de LPB/Matkator/Aweswell fueron mantenidos intencionadamente sin conocimiento de la reunión hasta después de celebrarse, impidiendo supuestamente asistencia, voto, disenso, preservación y resistencia a su ejecución.",
            "boundary_en": meeting["deliberate_non_notice_hypothesis"]["status"] + ". The public package does not establish lawful-recipient non-service, a false ACTA, fabricated debt, unlawful title removal, causation, actor-specific intent or criminality.",
            "boundary_es": "ALEGACIÓN SERIA Y FALSABLE DE PARTE NO ACREDITADA. El paquete público no acredita falta de notificación al destinatario legal, ACTA falsa, deuda fabricada, despojo ilícito de título, causalidad, intención individual ni delito.",
        },
        "reading_rules": [
            "ACTA_COPY_IS_NOT_DILIGENCED_OR_CERTIFIED_ORIGINAL",
            "ATTENDEE_UNANIMITY_IS_NOT_UNANIMITY_OF_ALL_OWNERS",
            "REGISTRATION_IS_NOT_DELIVERY_OR_EXAMINATION",
            "INSTITUTIONAL_POSSESSION_IS_NOT_PERSONAL_KNOWLEDGE",
            "TEMPORAL_PROXIMITY_IS_NOT_CAUSATION",
            "ADJUDICATION_IS_NOT_FINCA_BY_FINCA_IMPLEMENTATION_OR_FINAL_ACCOUNTING",
            "PUBLIC_AUTHORITY_FILE_EXISTENCE_IS_NOT_MERITS_CONFIRMATION",
            "ALLEGATION_IS_NOT_FINDING"
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = json.dumps(build(), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != output:
            print(f"ERROR: {TARGET.relative_to(ROOT)} is stale; run {Path(__file__).name}")
            return 1
        print("OK: Community ACTA / 2022 / public-authority projection is deterministic")
        return 0
    TARGET.write_text(output, encoding="utf-8")
    print(f"Wrote {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

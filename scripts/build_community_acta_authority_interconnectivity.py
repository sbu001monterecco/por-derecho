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
TARGET = ROOT / "assets/data/community-acta-authority-interconnectivity-v1.json"

EXPECTED_ACTAS = 20
EXPECTED_AUTHORITIES = 49
EXPECTED_ADJUDICATION_DECISIONS = 5

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
    decisions = load_decisions()

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
        }
        authority_files.append(authority_file)
        by_master_id[row["Master_ID"]] = {
            "group_id": group["id"],
            "axis_ids": group["axis_ids"],
            "proposition_ids": sorted({link["proposition_id"] for link in links}),
            "relationship_strength": "DEPENDENCY_TEST_ONLY",
            "boundary_en": "This reciprocal link exposes the applicable evidence questions; it does not prove ACTA delivery, receipt, examination, reliance, knowledge or merits.",
            "boundary_es": "Este enlace recíproco expone las preguntas probatorias aplicables; no prueba entrega, recepción, examen, utilización, conocimiento ni fondo del ACTA.",
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

    source_files = [ACTA_INDEX, MASTER, PRISM, DECISIONS, POST7JUNE, ASSERTIONS]
    return {
        "schema_version": "1.0.0",
        "generated": "2026-08-31",
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
        },
        "actas": actas,
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

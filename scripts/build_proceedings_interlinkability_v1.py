#!/usr/bin/env python3
"""Build the public exact-proceeding interlinkability coverage registry.

The registry is a navigation and audit projection, not a second proceedings
master.  Direct relationships are admitted only from explicit canonical fields.
Context clusters remain visibly non-procedural.  Every public exact proceeding
must resolve to one disposition, including an express gap or independent-track
state when no supported relationship is available.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from build_public_proceedings_projection import (
    EXCLUDED_TREATMENTS,
    PUBLIC_TREATMENTS,
)


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
PRISM = ROOT / "assets/data/proceedings-case-prism-v1.json"
TARGET = ROOT / "assets/data/proceedings-interlinkability-v1.json"

EXPECTED_PUBLIC_RECORDS = 106
EXPECTED_CANONICAL_EXACT_PROCEEDINGS = 86
EXPECTED_PUBLIC_EXACT_PROCEEDINGS = 85
EXPECTED_PRIVATE_EXACT_PROCEEDINGS = 1
EXPECTED_CASE_PRISM_EXACT_COVERED = 25

DIRECT_TYPE_PRIORITY = {
    "PARENT_CHILD": 0,
    "APPEAL_REVIEW_ID_LINK": 1,
    "LINKED_PROCEEDING": 2,
}

DIRECT_SOURCE_VERIFIED_STATUSES = {
    "VERIFIED_PRIMARY",
    "VERIFIED_PRIMARY_COPY",
    "VERIFIED_PROCEDURAL",
}

GAP_ES = {
    "CAN-OMB-001": "Resultado del escrito de reconsideración.",
    "ESP-TS-001": "Resolución firmada del TS sobre admisión, decisión y estado actual, y acto exacto de la AN recurrido.",
    "GC-CIV-003": "Auto firmado de 19 de diciembre de 2017, producción, decreto de 5 de marzo de 2018 y anexos.",
    "GC-CIV-027": "Expediente certificado que concilie 134/2024, 582/2024 y 641/2024; decreto citado de 1 de septiembre de 2025 que falta; firmeza.",
    "GC-CONT-025": "Originales firmados de 18 de septiembre y 24 de octubre, trazabilidad del reparto, expediente completo de los tres deudores y cualquier nexo real con una operación de Sun Park.",
    "GC-CRI-008": "Informe del Ministerio Fiscal, resolución posterior, expediente e índice de anexos.",
    "GC-CRI-009": "Auto firmado de sobreseimiento provisional, denuncia y anexos, y certificación del estado actual y la firmeza.",
    "GC-APP-004": "Rollo completo, acto recurrido, partes, expediente remitido y respuestas.",
    "GC-APP-005": "Rollo certificado completo, decisión sobre documentación posterior, resolución sobre el fondo y firmeza.",
    "GC-APP-006": "Rollo certificado completo, motivos, oposición, resolución sobre el fondo y firmeza.",
    "GC-APP-028": "Rollo de apelación certificado completo, resolución actual y firmeza.",
    "GC-CAL-002": "Expediente completo del recurso y resultado actual.",
    "GC-FIS-011": "Expediente completo, comunicación de origen, diligencias y remisión.",
    "GC-FIS-012": "Expediente primario, oficina, objeto, partes y resolución.",
    "GC-FIS-013": "Expediente certificado completo, matriz de lo solicitado frente a lo practicado y fundamento del archivo.",
    "GC-FIS-014": "Expediente nativo, oficina, objeto, material recibido y resolución.",
    "GC-FIS-015": "Resolución o remisión nativa, decisor, destino y resultado.",
    "GC-FIS-016": "Expediente completo, decreto de archivo y tratamiento de hechos posteriores o nuevos.",
    "GC-FIS-017": "Expediente certificado completo, decreto separado de incoación de 11 de febrero, tratamiento posterior a la corrección y remisión.",
    "GC-FIS-018": "Resolución nativa, material puesto ante el decisor, remisiones y tratamiento posterior.",
    "GC-GOV-019": "Expediente administrativo completo y material examinado.",
    "GC-GOV-020": "Expediente completo del recurso, informes y resolución final.",
    "GC-JUD-001": "Índice electrónico certificado completo y todas las secciones o incidentes materiales.",
    "GC-PRO-022": "Expediente oficial completo, respuesta, prueba y resolución final.",
    "GC-PRO-023": "Expediente oficial completo, respuesta, prueba y resolución final.",
    "LZ-APP-004": "Rollo exacto, auto firmado, composición de la Sala, motivos del recurso, posición de Fiscalía y firmeza.",
    "LZ-CAB-011": "Índice completo y expediente autenticado.",
    "LZ-CAB-012": "Índice completo y expediente autenticado.",
    "LZ-CAB-013": "Índice completo y expediente autenticado.",
    "LZ-CAB-019": "Expediente completo, declarante, autoridad, listado de unidades, título, comprobaciones y acto final.",
    "LZ-CAB-020": "Índice y estado actuales, y acto final.",
    "LZ-CAB-021": "Índice completo, objeto, partes y acto final.",
    "LZ-CAB-022": "Índice completo, objeto, partes y acto final.",
    "LZ-CAB-023": "Estado actual y acto final.",
    "LZ-CAB-024": "Índice completo, objeto, partes y acto final.",
    "LZ-CAB-025": "Ejecución del acceso, documentación autenticada producida y respuesta posterior.",
    "LZ-CIV-033": "Juzgado, partes y objeto exactos, y sentencia, recurso y firmeza completos.",
    "LZ-CIV-034": "Juzgado, partes y objeto exactos, rollo de apelación y firmeza.",
    "LZ-CIV-040": "Índice certificado; demanda y contestación; anexos; sentencia firmada; recurso y firmeza.",
    "LZ-CIV-041": "Índice certificado; solicitud y oposición; caución; auto firmado; recurso en ejecución y firmeza.",
    "LZ-FIS-007": "Referencia de destino, fiscal asignado, diligencias y resolución.",
    "LZ-FIS-036": "Referencia asignada en destino, fiscal, diligencias y resultado.",
    "LZ-JUD-001": "Rollo exacto, juzgado de primera instancia, sentencia firmada, partes, fincas y firmeza.",
    "LZ-JUD-002": "Expediente certificado, resolución final firmada, notificación y firmeza.",
    "LZ-JUD-003": "Denuncia completa, declaraciones del testigo y del AC, auto de archivo y notificaciones.",
    "LZ-JUD-005": "Juzgado y referencia exactos, título ejecutivo, partes, escritura de dación, cuenta de satisfacción y resolución firmada de terminación.",
    "LZ-JUD-043": "Expediente certificado y puente entre rótulos; prueba médica y objetiva del incidente; autoridad, acceso, huésped y agencia en la fecha; vista, resolución, recurso y firmeza.",
    "LZ-PRO-029": "Número oficial del expediente, custodio, preservación o traslado y resolución final.",
    "LZ-TRA-027": "Expediente de cumplimiento, documentos aportados y seguimiento.",
    "LZ-TRA-028": "Referencia asignada, admisión, expediente y resolución final.",
    "LZ-TRA-032": "Referencia asignada del Comisionado, admisión, respuesta y resolución final.",
    "LZ-TUR-008": "Acta certificada, anexos, entidad y capacidad inspeccionadas y seguimiento.",
    "LZ-TUR-009": "Resolución o asiento causado por la presentación, o certificación negativa.",
    "LZ-TUR-010": "Acta certificada, anexos, entidad y capacidad, unidades y seguimiento.",
    "LZ-YAI-014": "Índice completo, solicitudes, poderes, título o consentimiento, planos, informes y actos finales.",
    "LZ-YAI-015": "Índice completo y documentos fuente autenticados.",
    "LZ-YAI-016": "Índice completo y documentos fuente autenticados.",
    "LZ-YAI-017": "Índice completo y documentos fuente autenticados.",
    "LZ-YAI-018": "Índice completo y documentos fuente autenticados.",
    "LZ-YAI-026": "Índice, objeto, cadena de presentaciones, documentos de título y unidades, y estado actual.",
    "LZ-YAI-031": "Expediente e índice completos y cualquier producción o acto final.",
    "LZ-YAI-037": "Original oficial del expediente de Yaiza, índice, objeto y estado final o actual.",
    "MAD-AN-CONT-001": "Expediente judicial actual, plazo o resolución para la demanda y tramitación sobre el fondo.",
    "MAD-AN-CONT-002": "Referencia exacta PSS y resolución judicial firmada.",
    "MAD-AN-CRI-003": "Expediente completo, objeto, partes, pronunciamientos de la parte dispositiva y estado actual o final.",
    "MAD-AN-CRI-004": "Rollo completo, motivos del recurso, Auto 119/2024 firmado, firmeza y revisión posterior.",
    "MAD-CCACM-002": "Expediente completo, relación procesal con el expediente ICAM y resolución final.",
    "MAD-ICAM-001": "Expediente oficial completo, parte reclamada y ámbito, estado actual y resolución final.",
    "MAD-ICAM-003": "Resolución de archivo, registro del recurso o referencia asignada y revisión final.",
    "MAD-ICAM-004": "Expediente completo y cualquier recurso o revisión.",
    "MAD-ICAM-005": "Parte reclamada y ámbito exactos, estado procesal y resolución final.",
    "NAT-AEAT-001": "Expediente administrativo completo, actos impugnados y estado actual de recaudación.",
    "NAT-AEAT-002": "Expediente sancionador completo, acto impugnado, estado del recurso o revisión y relación con PO 496/2026.",
    "NAT-AID-001": "Órgano competente exacto, solicitud, beneficiario, costes elegibles e historial de concesión, aprobación, pago y reintegro.",
    "NAT-CNMV-001": "Material completo presentado y examinado, y resolución actual, sujeto al secreto supervisor.",
    "NAT-CNMV-002": "Material completo presentado y examinado, y resolución actual, sujeto al secreto supervisor.",
    "NAT-TES-001": "Expediente asignado, responsable, remisiones, examen y acto final.",
    "TF-CIV-001": "Demanda completa, título, oposición, resoluciones, firmeza y nexo con la ejecución.",
    "TF-CIV-002": "Expediente completo, documentos de remate o adjudicación y estado actual de la ejecución y del título.",
    "TF-CIV-006": "Índice certificado, demanda, contestación, anexos, vistas, costas y recurso o firmeza.",
    "TF-CRI-003": "Denuncia completa, auto de archivo, recurso de reforma, informe de Fiscalía, apelación y estado actual.",
    "VAL-CIV-001": "Completitud del expediente nativo o certificado, escritos, resolución sobre el fondo, notificación y firmeza, cuyo seguimiento permanece en el dossier de Valencia.",
    "X-EU-003": "Nexo o actuación concreta de la UE, transferencias y tratamiento final.",
    "X-REG-001": "Corpus supervisor nativo completo cuando pueda obtenerse legalmente.",
    "X-WB-005": "Responsable y expediente asignados, preservación y tratamiento sustantivo.",
}


def is_public(row: dict[str, str]) -> bool:
    """Apply the same closed publication vocabulary as the public projection."""
    treatment = row.get("Public_Treatment", "").strip()
    if treatment in PUBLIC_TREATMENTS:
        return True
    if treatment in EXCLUDED_TREATMENTS:
        return False
    raise ValueError(
        "unreviewed Public_Treatment value; update the publication policy before "
        f"building interlinkability: {treatment!r}"
    )


def compact_id(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:12].upper()
    return f"{prefix}-{digest}"


def source_literal(value: str) -> str:
    return value.strip() or "(empty)"


def load_rows() -> list[dict[str, str]]:
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len({row["Master_ID"] for row in rows}) != len(rows):
        raise ValueError("Master_ID values must be unique")
    return rows


def ids_in(value: str, ordered_ids: list[str]) -> list[str]:
    text = (value or "").upper()
    return [
        candidate
        for candidate in ordered_ids
        if re.search(
            rf"(?<![A-Z0-9-]){re.escape(candidate.upper())}(?![A-Z0-9-])",
            text,
        )
    ]


def direct_relationships(
    public_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    by_id = {row["Master_ID"]: row for row in public_rows}
    ordered_ids = list(by_id)
    candidates: list[dict[str, Any]] = []

    def add(
        from_id: str,
        to_id: str,
        relationship_type: str,
        source_row: dict[str, str],
        source_field: str,
        source_token: str,
    ) -> None:
        if from_id == to_id or from_id not in by_id or to_id not in by_id:
            return
        if relationship_type == "PARENT_CHILD":
            why_en = (
                f"{to_id} records {from_id} in Parent_Master_ID. This is an "
                "explicit procedural lineage, not adoption of any merits proposition."
            )
            why_es = (
                f"{to_id} registra {from_id} en Parent_Master_ID. Es una filiación "
                "procesal expresa, no la adopción de ninguna proposición de fondo."
            )
        elif relationship_type == "APPEAL_REVIEW_ID_LINK":
            why_en = (
                f"{source_row['Master_ID']} names {source_token} in Appeal_or_Review. "
                "The link records review routing only."
            )
            why_es = (
                f"{source_row['Master_ID']} identifica {source_token} en Appeal_or_Review. "
                "El enlace registra únicamente la vía de revisión."
            )
        else:
            why_en = (
                f"{source_row['Master_ID']} names {source_token} in Linked_Proceedings. "
                "The canonical link is preserved without inferring joinder or shared merits."
            )
            why_es = (
                f"{source_row['Master_ID']} identifica {source_token} en Linked_Proceedings. "
                "Se conserva el enlace canónico sin inferir acumulación ni fondo común."
            )

        candidates.append(
            {
                "id": f"REL-{relationship_type}-{from_id}-{to_id}",
                "from_master_id": from_id,
                "to_master_id": to_id,
                "relationship_class": "DIRECT_PROCEDURAL_EDGE",
                "relationship_type": relationship_type,
                "direction": "FORWARD",
                "why_en": why_en,
                "why_es": why_es,
                "source": {
                    "kind": "MASTER_REGISTER_FIELD",
                    "source_id": "PROCEEDINGS_MASTER_REGISTER",
                    "record_master_id": source_row["Master_ID"],
                    "field": source_field,
                    "value_token": source_token,
                    "evidence_status": source_row.get("Source_Status", ""),
                },
                "source_assertions": [
                    {
                        "source_id": "PROCEEDINGS_MASTER_REGISTER",
                        "source_record_master_id": source_row["Master_ID"],
                        "field": source_field,
                        "value_token": source_token,
                        "evidence_status": source_row.get("Source_Status", ""),
                        "assertion_relationship_type": relationship_type,
                        "assertion_direction": "FORWARD",
                        "assertion_from_master_id": from_id,
                        "assertion_to_master_id": to_id,
                    }
                ],
                "limitations_en": (
                    "Reverse navigation may be derived from this recorded field. The edge "
                    "does not establish joinder, notice, admissibility, knowledge, agreement, "
                    "wrongdoing or liability."
                ),
                "limitations_es": (
                    "Puede derivarse navegación inversa de este campo registrado. El enlace "
                    "no acredita acumulación, conocimiento formal, admisibilidad, conocimiento "
                    "personal, acuerdo, ilicitud ni responsabilidad."
                ),
                "public_safe": True,
            }
        )

    for row in public_rows:
        source_id = row["Master_ID"]
        parent_id = row.get("Parent_Master_ID", "").strip()
        if parent_id:
            add(parent_id, source_id, "PARENT_CHILD", row, "Parent_Master_ID", parent_id)
        for field, relationship_type in (
            ("Linked_Proceedings", "LINKED_PROCEEDING"),
            ("Appeal_or_Review", "APPEAL_REVIEW_ID_LINK"),
        ):
            for target_id in ids_in(row.get(field, ""), ordered_ids):
                if target_id != source_id:
                    add(source_id, target_id, relationship_type, row, field, target_id)

    # One strongest direct edge per unordered pair matches the public trace's
    # current semantics while the canonical fields remain the complete record.
    strongest: dict[tuple[str, str], dict[str, Any]] = {}
    assertions_by_pair: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for relationship in candidates:
        pair = tuple(
            sorted(
                (
                    relationship["from_master_id"],
                    relationship["to_master_id"],
                )
            )
        )
        existing = strongest.get(pair)
        assertions_by_pair[pair].extend(relationship["source_assertions"])
        if existing is None or DIRECT_TYPE_PRIORITY[
            relationship["relationship_type"]
        ] < DIRECT_TYPE_PRIORITY[existing["relationship_type"]]:
            strongest[pair] = relationship
    for pair, relationship in strongest.items():
        assertions = sorted(
            assertions_by_pair[pair],
            key=lambda item: (
                item["source_record_master_id"],
                item["field"],
                item["value_token"],
                item["assertion_relationship_type"],
                item["assertion_direction"],
                item["assertion_from_master_id"],
                item["assertion_to_master_id"],
            ),
        )
        relationship["source_assertions"] = assertions
        relationship["supporting_assertion_count"] = len(assertions)
    return sorted(
        strongest.values(),
        key=lambda item: (
            item["from_master_id"],
            item["to_master_id"],
            item["relationship_type"],
        ),
    )


def master_context_clusters(
    exact_rows: list[dict[str, str]], field: str, context_type: str, prefix: str
) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in exact_rows:
        value = row.get(field, "").strip()
        if value:
            groups[value].append(row)

    clusters: list[dict[str, Any]] = []
    for value, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        member_ids = [row["Master_ID"] for row in members]
        if context_type == "RECORDED_CONNECTION":
            label_en = f"Same recorded connection: {source_literal(value)}"
            label_es = f"Misma conexión registrada: {source_literal(value)}"
            why_en = (
                "Each member has the same exact non-empty Connection value in the "
                "canonical register."
            )
            why_es = (
                "Cada miembro tiene el mismo valor exacto y no vacío de Connection "
                "en el registro canónico."
            )
            limitations_en = (
                "A shared recorded connection is controlled navigation context only; it "
                "does not establish a procedural edge, joinder, notice, causation or liability."
            )
            limitations_es = (
                "Una conexión registrada compartida es solo contexto controlado de navegación; "
                "no acredita enlace procesal, acumulación, conocimiento formal, causalidad ni responsabilidad."
            )
        else:
            label_en = f"Same recorded stream: {source_literal(value)}"
            label_es = f"Misma vía registrada: {source_literal(value)}"
            why_en = (
                "Each member has the same exact non-empty Stream value in the canonical register."
            )
            why_es = (
                "Cada miembro tiene el mismo valor exacto y no vacío de Stream en el registro canónico."
            )
            limitations_en = (
                "A shared stream is taxonomy and navigation context only; it does not establish "
                "a material factual dependency, joinder or any procedural relationship."
            )
            limitations_es = (
                "Una vía compartida es solo taxonomía y contexto de navegación; no acredita "
                "dependencia fáctica material, acumulación ni relación procesal alguna."
            )
        clusters.append(
            {
                "id": compact_id(prefix, value),
                "context_type": context_type,
                "label_en": label_en,
                "label_es": label_es,
                "member_master_ids": member_ids,
                "why_en": why_en,
                "why_es": why_es,
                "source": {
                    "kind": "MASTER_REGISTER_FIELD_GROUP",
                    "source_id": "PROCEEDINGS_MASTER_REGISTER",
                    "field": field,
                    "value": value,
                    "member_provenance": [
                        {
                            "master_id": row["Master_ID"],
                            "evidence_status": row.get("Source_Status", ""),
                        }
                        for row in members
                    ],
                },
                "limitations_en": limitations_en,
                "limitations_es": limitations_es,
                "public_safe": True,
            }
        )
    return clusters


def prism_context_clusters(
    exact_ids: list[str], prism: dict[str, Any]
) -> list[dict[str, Any]]:
    exact_set = set(exact_ids)
    exact_order = {master_id: index for index, master_id in enumerate(exact_ids)}
    clusters: list[dict[str, Any]] = []
    for proposition in prism.get("propositions", []):
        provenance: dict[str, dict[str, Any]] = {}
        for lane_id, cell in proposition.get("cells", {}).items():
            if cell.get("status") == "OUTSIDE":
                continue
            for master_id in cell.get("master_ids", []):
                if master_id not in exact_set:
                    continue
                entry = provenance.setdefault(
                    master_id,
                    {
                        "master_id": master_id,
                        "cell_refs": [],
                        "cell_statuses": [],
                        "evidence_statuses": [],
                    },
                )
                entry["cell_refs"].append(f"{proposition['id']}/{lane_id}")
                entry["cell_statuses"].append(cell.get("status", ""))
                entry["evidence_statuses"].append(cell.get("evidence_status", ""))
        if len(provenance) < 2:
            continue
        member_ids = sorted(provenance, key=exact_order.__getitem__)
        member_provenance = []
        for master_id in member_ids:
            item = provenance[master_id]
            statuses = sorted(set(item.pop("evidence_statuses")))
            item["cell_refs"] = sorted(set(item["cell_refs"]))
            item["cell_statuses"] = sorted(set(item["cell_statuses"]))
            item["evidence_status"] = statuses[0] if len(statuses) == 1 else "MIXED_CELL_EVIDENCE_STATUS"
            member_provenance.append(item)
        clusters.append(
            {
                "id": f"CTX-PRISM-{proposition['id']}",
                "context_type": "CASE_PRISM_PROPOSITION",
                "label_en": f"Case Prism proposition {proposition['id']}: {proposition.get('title_en', proposition['id'])}",
                "label_es": f"Proposición {proposition['id']} del Prisma del caso: {proposition.get('title_es', proposition['id'])}",
                "member_master_ids": member_ids,
                "why_en": (
                    f"Each member is explicitly keyed to proposition {proposition['id']} in a "
                    "non-OUTSIDE Case Prism coordinate."
                ),
                "why_es": (
                    f"Cada miembro está vinculado expresamente a la proposición {proposition['id']} "
                    "en una coordenada del Prisma distinta de OUTSIDE."
                ),
                "source": {
                    "kind": "CASE_PRISM_PROPOSITION_MEMBERSHIP",
                    "path": "assets/data/proceedings-case-prism-v1.json",
                    "field": "propositions[].cells[].master_ids",
                    "record_id": proposition["id"],
                    "member_provenance": member_provenance,
                },
                "limitations_en": (
                    "Shared proposition membership is a controlled cross-reading aid. Cell statuses "
                    "may differ and proposition-level sources do not prove receipt or treatment in every file "
                    "and do not imply joinder."
                ),
                "limitations_es": (
                    "La pertenencia a una proposición compartida es una ayuda controlada de lectura cruzada. "
                    "Los estados de celda pueden diferir y las fuentes de la proposición no prueban recepción ni "
                    "tratamiento en cada expediente ni implican acumulación."
                ),
                "public_safe": True,
            }
        )
    return clusters


def node_dispositions(
    exact_rows: list[dict[str, str]],
    relationships: list[dict[str, Any]],
    context_clusters: list[dict[str, Any]],
    require_specific_gap_es: bool = True,
) -> list[dict[str, Any]]:
    relationship_ids: dict[str, list[str]] = defaultdict(list)
    for relationship in relationships:
        for master_id in (
            relationship["from_master_id"],
            relationship["to_master_id"],
        ):
            relationship_ids[master_id].append(relationship["id"])

    clusters_by_id = {cluster["id"]: cluster for cluster in context_clusters}
    clusters_for_node: dict[str, list[str]] = defaultdict(list)
    for cluster in context_clusters:
        for master_id in cluster["member_master_ids"]:
            clusters_for_node[master_id].append(cluster["id"])

    context_priority = {
        "RECORDED_CONNECTION": 0,
        "CASE_PRISM_PROPOSITION": 1,
    }
    dispositions: list[dict[str, Any]] = []
    for row in exact_rows:
        master_id = row["Master_ID"]
        direct_ids = sorted(relationship_ids.get(master_id, []))
        cluster_ids = sorted(
            clusters_for_node.get(master_id, []),
            key=lambda cluster_id: (
                context_priority[clusters_by_id[cluster_id]["context_type"]],
                cluster_id,
            ),
        )
        open_gap = row.get("Open_Reference_Gap", "").strip()

        if direct_ids:
            classification = "DIRECT_PROCEDURAL_EDGE"
            why_en = (
                "At least one direct relationship is supported by an explicit canonical "
                "Parent_Master_ID, Linked_Proceedings or Appeal_or_Review field."
            )
            why_es = (
                "Al menos una relación directa está respaldada por un campo canónico expreso "
                "Parent_Master_ID, Linked_Proceedings o Appeal_or_Review."
            )
            basis = {
                "kind": "DIRECT_RELATIONSHIP_MEMBERSHIP",
                "relationship_ids": direct_ids,
            }
        elif cluster_ids:
            classification = "CONTROLLED_CONTEXTUAL_BRIDGE"
            primary_cluster = clusters_by_id[cluster_ids[0]]
            why_en = (
                f"No direct edge is asserted. The primary controlled bridge is "
                f"{primary_cluster['context_type']}; its limitations remain attached."
            )
            why_es = (
                "No se afirma enlace directo. El puente controlado principal es "
                f"{primary_cluster['context_type']}; se mantienen sus limitaciones."
            )
            basis = {
                "kind": "CONTEXT_CLUSTER_MEMBERSHIP",
                "primary_context_cluster_id": cluster_ids[0],
            }
        elif open_gap:
            classification = "EXPLICIT_RELATIONSHIP_GAP"
            why_en = (
                "No direct edge or admitted controlled contextual cluster is currently materialised. "
                "The row's open primary-source requirement is carried as an explicit relationship gap."
            )
            why_es = (
                "Actualmente no se materializa ningún enlace directo ni grupo contextual controlado admitido. "
                "La necesidad de fuente primaria abierta de la fila se mantiene como laguna relacional expresa."
            )
            basis = {
                "kind": "MASTER_REGISTER_FIELD",
                "source_id": "PROCEEDINGS_MASTER_REGISTER",
                "record_master_id": master_id,
                "field": "Open_Reference_Gap",
                "evidence_status": row.get("Source_Status", ""),
            }
        else:
            classification = "INDEPENDENT_TRACK"
            why_en = (
                "No direct or controlled contextual relationship is currently asserted. "
                "The exact proceeding remains independently navigable without a fabricated edge."
            )
            why_es = (
                "Actualmente no se afirma ninguna relación directa ni contextual controlada. "
                "El procedimiento exacto sigue siendo navegable de forma independiente sin inventar enlaces."
            )
            basis = {
                "kind": "NO_ADMITTED_RELATION_OR_GAP",
                "source_id": "PROCEEDINGS_MASTER_REGISTER",
                "record_master_id": master_id,
            }

        if open_gap:
            if require_specific_gap_es and master_id not in GAP_ES:
                raise ValueError(
                    f"{master_id} open source requirement lacks a specific Spanish formulation"
                )
            next_en = open_gap
            next_es = GAP_ES.get(
                master_id,
                "Revisar la fuente primaria indicada en Open_Reference_Gap antes de afirmar una relación adicional.",
            )
        else:
            next_en = (
                "No additional relationship source is specified; admit a new edge only from "
                "an explicit canonical field or specialist source record."
            )
            next_es = (
                "No se especifica una fuente relacional adicional; admita un nuevo enlace solo "
                "desde un campo canónico expreso o un registro de fuente especializada."
            )

        dispositions.append(
            {
                "master_id": master_id,
                "primary_classification": classification,
                "relationship_ids": direct_ids,
                "context_cluster_ids": cluster_ids,
                "why_en": why_en,
                "why_es": why_es,
                "limitations_en": (
                    "This disposition controls navigation only. It does not prove joinder, receipt, "
                    "admissibility, knowledge, agreement, causation, wrongdoing or liability."
                ),
                "limitations_es": (
                    "Esta clasificación controla solo la navegación. No prueba acumulación, recepción, "
                    "admisibilidad, conocimiento, acuerdo, causalidad, ilicitud ni responsabilidad."
                ),
                "next_source_needed_en": next_en,
                "next_source_needed_es": next_es,
                "source_status": row.get("Source_Status", ""),
                "basis": basis,
            }
        )
    return dispositions


def build() -> dict[str, Any]:
    rows = load_rows()
    public_rows = [row for row in rows if is_public(row)]
    canonical_exact_rows = [row for row in rows if row.get("Is_Proceeding") == "TRUE"]
    exact_rows = [row for row in public_rows if row.get("Is_Proceeding") == "TRUE"]
    private_exact_rows = [row for row in canonical_exact_rows if not is_public(row)]
    if len(public_rows) != EXPECTED_PUBLIC_RECORDS:
        raise ValueError(
            f"expected {EXPECTED_PUBLIC_RECORDS} public records, found {len(public_rows)}"
        )
    if len(exact_rows) != EXPECTED_PUBLIC_EXACT_PROCEEDINGS:
        raise ValueError(
            "expected "
            f"{EXPECTED_PUBLIC_EXACT_PROCEEDINGS} public exact proceedings, found {len(exact_rows)}"
        )
    if len(canonical_exact_rows) != EXPECTED_CANONICAL_EXACT_PROCEEDINGS:
        raise ValueError(
            "expected "
            f"{EXPECTED_CANONICAL_EXACT_PROCEEDINGS} canonical exact proceedings, "
            f"found {len(canonical_exact_rows)}"
        )
    if len(private_exact_rows) != EXPECTED_PRIVATE_EXACT_PROCEEDINGS:
        raise ValueError(
            "expected "
            f"{EXPECTED_PRIVATE_EXACT_PROCEEDINGS} private exact proceeding, "
            f"found {len(private_exact_rows)}"
        )
    public_exact_open_gap_ids = {
        row["Master_ID"] for row in exact_rows if row.get("Open_Reference_Gap", "").strip()
    }
    if set(GAP_ES) != public_exact_open_gap_ids:
        raise ValueError(
            "GAP_ES must match the public exact open-source denominator exactly; "
            f"missing={sorted(public_exact_open_gap_ids - set(GAP_ES))}; "
            f"extra={sorted(set(GAP_ES) - public_exact_open_gap_ids)}"
        )
    bilingual_specific_next_source_count = sum(
        bool(row.get("Open_Reference_Gap", "").strip()) and row["Master_ID"] in GAP_ES
        for row in exact_rows
    )

    exact_ids = [row["Master_ID"] for row in exact_rows]
    # This is an exact-proceeding relationship registry. Aggregate, technical,
    # FALSE and UNVERIFIED public nodes remain available in the Master Register
    # and general renderer, but cannot become direct endpoints here.
    relationships = direct_relationships(exact_rows)
    source_verified_relationship_count = sum(
        all(
            assertion.get("evidence_status") in DIRECT_SOURCE_VERIFIED_STATUSES
            for assertion in relationship.get("source_assertions", [])
        )
        for relationship in relationships
    )
    source_reported_pending_relationship_count = (
        len(relationships) - source_verified_relationship_count
    )
    direct_assertions = [
        assertion
        for relationship in relationships
        for assertion in relationship.get("source_assertions", [])
    ]
    source_verified_assertion_count = sum(
        assertion.get("evidence_status") in DIRECT_SOURCE_VERIFIED_STATUSES
        for assertion in direct_assertions
    )
    source_reported_pending_assertion_count = (
        len(direct_assertions) - source_verified_assertion_count
    )
    prism = json.loads(PRISM.read_text(encoding="utf-8"))
    context_clusters = (
        master_context_clusters(
            exact_rows, "Connection", "RECORDED_CONNECTION", "CTX-CONNECTION"
        )
        + prism_context_clusters(exact_ids, prism)
    )
    context_clusters = sorted(
        context_clusters,
        key=lambda item: (
            {
                "RECORDED_CONNECTION": 0,
                "CASE_PRISM_PROPOSITION": 1,
            }[item["context_type"]],
            item["id"],
        ),
    )
    exact_id_set = set(exact_ids)
    case_prism_exact_ids = {
        master_id
        for proposition in prism.get("propositions", [])
        for cell in proposition.get("cells", {}).values()
        if cell.get("status") != "OUTSIDE"
        for master_id in cell.get("master_ids", [])
        if master_id in exact_id_set
    }
    if len(case_prism_exact_ids) != EXPECTED_CASE_PRISM_EXACT_COVERED:
        raise ValueError(
            "expected "
            f"{EXPECTED_CASE_PRISM_EXACT_COVERED} Case Prism-covered exact proceedings, "
            f"found {len(case_prism_exact_ids)}"
        )
    dispositions = node_dispositions(exact_rows, relationships, context_clusters)
    classification_counts: dict[str, int] = defaultdict(int)
    for disposition in dispositions:
        classification_counts[disposition["primary_classification"]] += 1

    # Verify the full canonical denominator without serialising any excluded
    # identifier, locator or description into the public registry.  The private
    # exact object is still given an internal disposition so exclusion cannot be
    # mistaken for an unexplained orphan.
    canonical_relationships = direct_relationships(canonical_exact_rows)
    canonical_context_clusters = (
        master_context_clusters(
            canonical_exact_rows,
            "Connection",
            "RECORDED_CONNECTION",
            "CTX-CONNECTION",
        )
        + prism_context_clusters(
            [row["Master_ID"] for row in canonical_exact_rows], prism
        )
    )
    canonical_dispositions = node_dispositions(
        canonical_exact_rows,
        canonical_relationships,
        canonical_context_clusters,
        require_specific_gap_es=False,
    )
    private_id_set = {row["Master_ID"] for row in private_exact_rows}
    private_disposition_counts: dict[str, int] = defaultdict(int)
    for disposition in canonical_dispositions:
        if disposition["master_id"] in private_id_set:
            private_disposition_counts[disposition["primary_classification"]] += 1
    if sum(private_disposition_counts.values()) != len(private_exact_rows):
        raise ValueError("every excluded private exact proceeding requires an internal disposition")
    if private_disposition_counts != {"EXPLICIT_RELATIONSHIP_GAP": 1}:
        raise ValueError(
            "the excluded private exact proceeding must remain an explicit relationship gap"
        )

    data = {
        "schema_version": "1.0.0",
        "control_date": "2026-08-30",
        "status": "PUBLIC_DERIVED_EXACT_PROCEEDING_INTERLINKABILITY_CONTROL",
        "canonical_node_source_id": "PROCEEDINGS_MASTER_REGISTER",
        "public_node_projection": "assets/data/proceedings-master-public-v1.json",
        "case_prism_source": "assets/data/proceedings-case-prism-v1.json",
        "boundary_en": (
            "Every public exact proceeding receives one navigation disposition. A contextual "
            "bridge or gap is not a procedural edge and no relationship proves joinder or merits."
        ),
        "boundary_es": (
            "Cada procedimiento exacto público recibe una clasificación de navegación. Un puente "
            "contextual o una laguna no es un enlace procesal y ninguna relación prueba acumulación ni fondo."
        ),
        "navigation_contract": {
            "exact_id_to_master_register": "REQUIRED",
            "exact_id_to_renderer": "REQUIRED",
            "dossier_route_relationship": "NOT_INFERRED",
            "en": (
                "Every exact ID remains navigable to its canonical public Master Register row and "
                "renderer state. Known dossier links may be additive, but this registry does not "
                "infer or claim a complete exact-ID-to-dossier relationship denominator."
            ),
            "es": (
                "Cada ID exacto sigue siendo navegable hacia su fila canónica del Registro Maestro "
                "público y su estado en el visualizador. Los enlaces conocidos a expedientes pueden "
                "ser aditivos, pero este registro no infiere ni afirma un denominador completo de "
                "relaciones entre ID exacto y expediente temático."
            ),
        },
        "scope": {
            "selector": "public-safe rows where Is_Proceeding is exactly TRUE",
            "public_exact_proceeding_ids": exact_ids,
            "expected_count": EXPECTED_PUBLIC_EXACT_PROCEEDINGS,
            "excluded_aggregate_reference_ids": ["GC-APP-007"],
        },
        "classification_catalog": {
            "DIRECT_PROCEDURAL_EDGE": {
                "en": "Direct procedural edge",
                "es": "Enlace procesal directo",
            },
            "CONTROLLED_CONTEXTUAL_BRIDGE": {
                "en": "Controlled contextual bridge",
                "es": "Puente contextual controlado",
            },
            "INDEPENDENT_TRACK": {
                "en": "Independent track",
                "es": "Vía independiente",
            },
            "EXPLICIT_RELATIONSHIP_GAP": {
                "en": "Explicit relationship gap",
                "es": "Laguna relacional expresa",
            },
        },
        "relationship_type_catalog": {
            "PARENT_CHILD": {"en": "Parent / child", "es": "Padre / hijo"},
            "LINKED_PROCEEDING": {
                "en": "Explicit linked proceeding",
                "es": "Procedimiento enlazado expresamente",
            },
            "APPEAL_REVIEW_ID_LINK": {
                "en": "Appeal / review ID link",
                "es": "Enlace de recurso / revisión",
            },
            "SPECIALIST_SOURCE_EDGE": {
                "en": "Specialist source edge",
                "es": "Enlace de fuente especializada",
            },
        },
        "context_type_catalog": {
            "RECORDED_CONNECTION": {
                "en": "Same recorded connection",
                "es": "Misma conexión registrada",
            },
            "CASE_PRISM_PROPOSITION": {
                "en": "Same Case Prism proposition",
                "es": "Misma proposición del Prisma del caso",
            },
        },
        "relationships": relationships,
        "context_clusters": context_clusters,
        "node_dispositions": dispositions,
        "coverage": {
            "public_record_count": len(public_rows),
            "canonical_exact_proceeding_count": len(canonical_exact_rows),
            "public_exact_proceeding_count": len(exact_rows),
            "private_exact_excluded_count": len(private_exact_rows),
            "private_exact_excluded_disposition_counts": dict(
                sorted(private_disposition_counts.items())
            ),
            "node_disposition_count": len(dispositions),
            "direct_relationship_count": len(relationships),
            "direct_relationship_source_verified_pair_count": source_verified_relationship_count,
            "direct_relationship_source_reported_pending_pair_count": source_reported_pending_relationship_count,
            "direct_source_assertion_count": sum(
                relationship["supporting_assertion_count"]
                for relationship in relationships
            ),
            "direct_source_verified_assertion_count": source_verified_assertion_count,
            "direct_source_reported_pending_assertion_count": source_reported_pending_assertion_count,
            "context_cluster_count": len(context_clusters),
            "recorded_connection_cluster_count": sum(
                cluster["context_type"] == "RECORDED_CONNECTION"
                for cluster in context_clusters
            ),
            "recorded_stream_cluster_count": sum(
                cluster["context_type"] == "RECORDED_STREAM"
                for cluster in context_clusters
            ),
            "case_prism_proposition_cluster_count": sum(
                cluster["context_type"] == "CASE_PRISM_PROPOSITION"
                for cluster in context_clusters
            ),
            "case_prism_exact_proceeding_covered_count": len(case_prism_exact_ids),
            "case_prism_exact_proceeding_uncovered_count": len(exact_rows)
            - len(case_prism_exact_ids),
            "decision_dependency_exact_coverage": "GAP_25_OF_85",
            "bilingual_specific_next_source_count": bilingual_specific_next_source_count,
            "bilingual_specific_next_source_coverage": (
                f"VERIFIED_{bilingual_specific_next_source_count}_OF_{len(exact_rows)}"
            ),
            "exact_proceeding_full_finite_test_count": 0,
            "exact_proceeding_full_finite_test_coverage": "GAP_0_OF_85",
            "classification_counts": {
                token: classification_counts.get(token, 0)
                for token in (
                    "DIRECT_PROCEDURAL_EDGE",
                    "CONTROLLED_CONTEXTUAL_BRIDGE",
                    "INDEPENDENT_TRACK",
                    "EXPLICIT_RELATIONSHIP_GAP",
                )
            },
            "unexplained_exact_proceeding_count": len(exact_rows) - len(dispositions),
            "geography_only_bridge_count": 0,
        },
    }
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the committed registry is not in builder-normalised form",
    )
    args = parser.parse_args()
    rendered = json.dumps(build(), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != rendered:
            print(f"{TARGET.relative_to(ROOT)} is stale; run {Path(__file__).name}")
            return 1
        print(f"{TARGET.relative_to(ROOT)} matches the interlinkability builder")
        return 0
    TARGET.write_text(rendered, encoding="utf-8")
    print(f"wrote {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

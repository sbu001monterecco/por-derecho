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
FISCALIA_RESPONSES = ROOT / "assets/data/fiscalia-response-correspondence.json"
TARGET = ROOT / "assets/data/proceedings-interlinkability-v1.json"
CONTEXT_SOURCE_FILES = (
    ROOT / "assets/data/treasury-transparency-7-2026-v1.json",
)

EXPECTED_PUBLIC_RECORDS = 130
EXPECTED_CANONICAL_EXACT_PROCEEDINGS = 107
EXPECTED_PUBLIC_EXACT_PROCEEDINGS = 106
EXPECTED_PRIVATE_EXACT_PROCEEDINGS = 1
EXPECTED_CASE_PRISM_EXACT_COVERED = 45
EXPECTED_FISCALIA_OFFICE_FILE_RECORDS = 26
EXPECTED_FISCALIA_EXACT_RECORDS = 23
EXPECTED_FISCALIA_UNVERIFIED_RECORDS = 3
EXPECTED_FISCALIA_RESPONSE_EPISODES = 9

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

FINITE_TEST_FAMILY_CATALOG = {
    "OMBUDSMAN_RECONSIDERATION": {
        "en": "Ombudsman reconsideration",
        "es": "Reconsideración ante el órgano autonómico de queja",
    },
    "CRIMINAL_FILE_DECISION": {
        "en": "Criminal-file decision",
        "es": "Decisión en expediente penal",
    },
    "CIVIL_FILE_DECISION": {
        "en": "Civil-file decision",
        "es": "Decisión en expediente civil",
    },
    "FISCALIA_INSTITUTIONAL_MEMORY": {
        "en": "Prosecution institutional memory",
        "es": "Memoria institucional del Ministerio Fiscal",
    },
    "PROFESSIONAL_SUPERVISION": {
        "en": "Professional supervision",
        "es": "Supervisión profesional",
    },
    "ADMIN_AUTHORITY_TITLE_SOURCE": {
        "en": "Administrative authority / title source",
        "es": "Autoridad administrativa / fuente de título",
    },
    "TAX_CONTENTIOUS_CHAIN": {
        "en": "Tax / contentious chain",
        "es": "Cadena tributaria / contenciosa",
    },
    "REGULATORY_PUBLIC_ROUTE": {
        "en": "Regulatory / public route",
        "es": "Vía regulatoria / pública",
    },
    "GENERAL_EXACT_FILE_DECISION_TEST": {
        "en": "General exact-file decision test",
        "es": "Prueba general de decisión del expediente exacto",
    },
}

EXPECTED_FINITE_TEST_FAMILY_COUNTS = {
    "ADMIN_AUTHORITY_TITLE_SOURCE": 26,
    "CIVIL_FILE_DECISION": 23,
    "CRIMINAL_FILE_DECISION": 14,
    "FISCALIA_INSTITUTIONAL_MEMORY": 23,
    "OMBUDSMAN_RECONSIDERATION": 1,
    "PROFESSIONAL_SUPERVISION": 8,
    "REGULATORY_PUBLIC_ROUTE": 7,
    "TAX_CONTENTIOUS_CHAIN": 4,
}

FISCALIA_EPISODE_TO_MASTER_ID = {
    "first-frame-2013": "GC-FIS-011",
    "di248-2018": "GC-FIS-013",
    "di113-2022": "GC-FIS-014",
    "di22-2026": "GC-FIS-016",
    "dip2-2026": "GC-FIS-017",
    "eg49-2026": "GC-FIS-018",
    "dp1901-2026": "GC-CRI-008",
    "eg745-2026": "NAT-FIS-004",
    "gub86-2026": "LZ-FIS-007",
}

# These grades are source-controlled institutional axes for the nine curated
# correspondence episodes.  They do not infer personal receipt, knowledge or
# incorporation from a raw matter-reference string.
FISCALIA_EPISODE_AXES = {
    "first-frame-2013": {
        "transmission_status": "PARTLY_DOCUMENTED", "material_received_status": "PARTLY_DOCUMENTED",
        "referral_status": "NOT_LOCATED", "registration_status": "DOCUMENTED",
        "file_incorporation_status": "STATUS_UNRESOLVED", "recipient_attribution_status": "NOT_LOCATED",
        "substantive_examination_status": "NOT_LOCATED", "decision_use_status": "DOCUMENTED",
        "cross_file_acknowledgement_status": "NOT_LOCATED",
    },
    "di248-2018": {
        "transmission_status": "DOCUMENTED", "material_received_status": "PARTLY_DOCUMENTED",
        "referral_status": "NOT_LOCATED", "registration_status": "DOCUMENTED",
        "file_incorporation_status": "PARTLY_DOCUMENTED", "recipient_attribution_status": "PARTLY_DOCUMENTED",
        "substantive_examination_status": "PARTLY_DOCUMENTED", "decision_use_status": "DOCUMENTED",
        "cross_file_acknowledgement_status": "STATUS_UNRESOLVED",
    },
    "di113-2022": {
        "transmission_status": "DOCUMENTED", "material_received_status": "PARTLY_DOCUMENTED",
        "referral_status": "NOT_LOCATED", "registration_status": "DOCUMENTED",
        "file_incorporation_status": "PARTLY_DOCUMENTED", "recipient_attribution_status": "PARTLY_DOCUMENTED",
        "substantive_examination_status": "PARTLY_DOCUMENTED", "decision_use_status": "DOCUMENTED",
        "cross_file_acknowledgement_status": "PARTLY_DOCUMENTED",
    },
    "di22-2026": {
        "transmission_status": "DOCUMENTED", "material_received_status": "PARTLY_DOCUMENTED",
        "referral_status": "NOT_LOCATED", "registration_status": "DOCUMENTED",
        "file_incorporation_status": "DOCUMENTED", "recipient_attribution_status": "PARTLY_DOCUMENTED",
        "substantive_examination_status": "PARTLY_DOCUMENTED", "decision_use_status": "DOCUMENTED",
        "cross_file_acknowledgement_status": "NOT_LOCATED",
    },
    "dip2-2026": {
        "transmission_status": "DOCUMENTED", "material_received_status": "DOCUMENTED",
        "referral_status": "NOT_LOCATED", "registration_status": "DOCUMENTED",
        "file_incorporation_status": "STATUS_UNRESOLVED", "recipient_attribution_status": "PARTLY_DOCUMENTED",
        "substantive_examination_status": "PARTLY_DOCUMENTED", "decision_use_status": "PARTLY_DOCUMENTED",
        "cross_file_acknowledgement_status": "NOT_LOCATED",
    },
    "eg49-2026": {
        "transmission_status": "DOCUMENTED", "material_received_status": "PARTLY_DOCUMENTED",
        "referral_status": "NOT_LOCATED", "registration_status": "DOCUMENTED",
        "file_incorporation_status": "STATUS_UNRESOLVED", "recipient_attribution_status": "PARTLY_DOCUMENTED",
        "substantive_examination_status": "PARTLY_DOCUMENTED", "decision_use_status": "DOCUMENTED",
        "cross_file_acknowledgement_status": "NOT_LOCATED",
    },
    "dp1901-2026": {
        "transmission_status": "ROUTING_DOCUMENTED", "material_received_status": "NOT_LOCATED",
        "referral_status": "ROUTING_DOCUMENTED", "registration_status": "NOT_LOCATED",
        "file_incorporation_status": "NOT_LOCATED", "recipient_attribution_status": "NOT_LOCATED",
        "substantive_examination_status": "NOT_LOCATED", "decision_use_status": "NOT_LOCATED",
        "cross_file_acknowledgement_status": "DOCUMENTED",
    },
    "eg745-2026": {
        "transmission_status": "DOCUMENTED", "material_received_status": "DOCUMENTED",
        "referral_status": "NOT_LOCATED", "registration_status": "DOCUMENTED",
        "file_incorporation_status": "PARTLY_DOCUMENTED", "recipient_attribution_status": "NOT_LOCATED",
        "substantive_examination_status": "PARTLY_DOCUMENTED", "decision_use_status": "DOCUMENTED",
        "cross_file_acknowledgement_status": "STATUS_UNRESOLVED",
    },
    "gub86-2026": {
        "transmission_status": "ROUTING_DOCUMENTED", "material_received_status": "NOT_LOCATED",
        "referral_status": "ROUTING_DOCUMENTED", "registration_status": "NOT_LOCATED",
        "file_incorporation_status": "NOT_LOCATED", "recipient_attribution_status": "NOT_LOCATED",
        "substantive_examination_status": "NOT_LOCATED", "decision_use_status": "ROUTING_DOCUMENTED",
        "cross_file_acknowledgement_status": "NOT_LOCATED",
    },
}


def bi(en: str, es: str) -> dict[str, str]:
    return {"en": en, "es": es}


RECEIPT_KNOWLEDGE_STATUS_CATALOG = {
    "DOCUMENTED": {"en": "Documented", "es": "Documentado"},
    "PARTLY_DOCUMENTED": {"en": "Partly documented", "es": "Documentado parcialmente"},
    "ROUTING_DOCUMENTED": {"en": "Routing documented; destination receipt not inferred", "es": "Remisión documentada; no se infiere recepción en destino"},
    "NOT_LOCATED": {"en": "Not located in the controlled corpus", "es": "No localizado en el corpus controlado"},
    "STATUS_UNRESOLVED": {"en": "Status unresolved", "es": "Estado no resuelto"},
    "NOT_ESTABLISHED": {"en": "Not established", "es": "No establecido"},
    "RECORDED_CURRENT_CUSTODIAN": {"en": "Recorded current custodian; legal competence not inferred", "es": "Custodio actual registrado; no se infiere competencia jurídica"},
    "CONTROLLED_NAVIGATION_ONLY": {"en": "Controlled navigation only; institutional receipt not inferred", "es": "Solo navegación controlada; no se infiere recepción institucional"},
}

FISCALIA_AXIS_SOURCE_FIELDS = {
    "transmission_status": "source_authored_known_summary",
    "material_received_status": "source_authored_known_summary",
    # The two positive routing grades are established by the source-authored
    # known-event field that describes the transfer/referral itself.  A later
    # response or missing report cannot be substituted as referral evidence.
    "referral_status": "source_authored_known_summary",
    "registration_status": "source_authored_known_summary",
    "file_incorporation_status": "institutional_response",
    "recipient_attribution_status": "institutional_response",
    "substantive_examination_status": "institutional_response",
    "decision_use_status": "institutional_response",
    "cross_file_acknowledgement_status": "source_authored_known_summary",
}

FISCALIA_EPISODE_AXIS_SOURCE_FIELD_OVERRIDES = {
    # These institutional/signatory attributions are stated in the known-event
    # field, not in the generic response summary.
    ("di22-2026", "recipient_attribution_status"): "source_authored_known_summary",
    ("eg49-2026", "recipient_attribution_status"): "source_authored_known_summary",
    # The bounded examination grade rests on the premise used in the 6 March
    # decree; the response field does not establish post-correction review.
    ("dip2-2026", "substantive_examination_status"): "source_authored_known_summary",
}

FISCALIA_AXIS_LABELS = {
    "transmission_status": bi("Transmission", "Transmisión"),
    "material_received_status": bi("Material received", "Material recibido"),
    "referral_status": bi("Referral", "Remisión"),
    "registration_status": bi("Registration", "Registro"),
    "file_incorporation_status": bi("File incorporation", "Incorporación al expediente"),
    "recipient_attribution_status": bi("Recipient attribution", "Atribución del destinatario"),
    "substantive_examination_status": bi("Substantive examination", "Examen sustantivo"),
    "decision_use_status": bi("Decision use", "Uso en decisión"),
    "cross_file_acknowledgement_status": bi("Cross-file acknowledgement", "Reconocimiento entre expedientes"),
}

FISCALIA_AXIS_LIMITS = {
    "transmission_status": bi(
        "Transmission does not by itself prove destination receipt, completeness, incorporation or examination.",
        "La transmisión no acredita por sí sola recepción en destino, integridad, incorporación ni examen.",
    ),
    "material_received_status": bi(
        "A received-material grade does not establish a complete inventory, incorporation, examination or decision use.",
        "El grado de material recibido no acredita inventario completo, incorporación, examen ni uso decisorio.",
    ),
    "referral_status": bi(
        "Referral does not by itself prove destination receipt, acceptance of competence, incorporation or merits review.",
        "La remisión no acredita por sí sola recepción en destino, aceptación de competencia, incorporación ni examen de fondo.",
    ),
    "registration_status": bi(
        "Registration does not by itself prove file incorporation, examination, reliance or personal knowledge.",
        "El registro no acredita por sí solo incorporación, examen, uso ni conocimiento personal.",
    ),
    "file_incorporation_status": bi(
        "File incorporation does not by itself prove substantive examination, reliance or legal correctness.",
        "La incorporación al expediente no acredita por sí sola examen sustantivo, uso ni corrección jurídica.",
    ),
    "recipient_attribution_status": bi(
        "Institutional or signatory attribution does not prove personal receipt, reading, understanding or knowledge of every item.",
        "La atribución institucional o de firma no prueba recepción, lectura, comprensión o conocimiento personal de cada elemento.",
    ),
    "substantive_examination_status": bi(
        "A bounded examination grade does not prove that every item was examined, correctly assessed or known by a named person.",
        "Un grado limitado de examen no acredita que cada elemento fuera examinado, correctamente valorado o conocido por una persona identificada.",
    ),
    "decision_use_status": bi(
        "A documented decision does not by itself prove which materials were relied on, legal correctness, intent or wrongdoing.",
        "Una decisión documentada no acredita por sí sola qué materiales se utilizaron, corrección jurídica, intención ni ilicitud.",
    ),
    "cross_file_acknowledgement_status": bi(
        "A cross-file reference is not a unitary acknowledgement, complete comparison or procedural joinder.",
        "Una referencia entre expedientes no equivale a reconocimiento unitario, comparación completa ni acumulación procesal.",
    ),
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
    "NAT-TES-001": "Producción restante de la Resolución 154/2026 bajo ME-110; siguen abiertas bajo ME-108/109 la identidad de suscriptores y las reglas de asignación.",
    "TF-CIV-001": "Demanda completa, título, oposición, resoluciones, firmeza y nexo con la ejecución.",
    "TF-CIV-002": "Expediente completo, documentos de remate o adjudicación y estado actual de la ejecución y del título.",
    "TF-CIV-006": "Índice certificado, demanda, contestación, anexos, vistas, costas y recurso o firmeza.",
    "TF-CRI-003": "Denuncia completa, auto de archivo, recurso de reforma, informe de Fiscalía, apelación y estado actual.",
    "VAL-CIV-001": "Completitud del expediente nativo o certificado, escritos, resolución sobre el fondo, notificación y firmeza, cuyo seguimiento permanece en el dossier de Valencia.",
    "X-EU-003": "Nexo o actuación concreta de la UE, transferencias y tratamiento final.",
    "X-REG-001": "Corpus supervisor nativo completo cuando pueda obtenerse legalmente.",
    "X-WB-005": "Responsable y expediente asignados, preservación y tratamiento sustantivo.",
    "LZ-FIS-045": "Expediente certificado completo; fiscal investigador; diligencias practicadas e inventario de fuentes; y cualquier reiteración judicial posterior o su destino.",
    "TF-FIS-007": "Referencia de recepción, corpus trasladado completo, fiscal asignado y tratamiento diferenciado en Las Palmas.",
    "GC-FIS-032": "Expediente e índice completos; destinos receptores exactos y acuses; material puesto ante el decisor; y tratamiento territorial posterior.",
    "TF-FIS-008": "Resolución judicial de 16 de julio citada por el decreto; identidades y ámbitos nativos de DIP 7/2026 y DIP 12/2026; prueba de incorporación a DP 748; y tratamiento individual de cada solicitud.",
    "GC-FIS-033": "Expediente e índice completos; decreto original de 20 de agosto; corpus exacto examinado; y tratamiento del traslado o asociación por la Fiscalía Provincial de Las Palmas.",
    "NAT-FIS-004": "Expediente e índice completos; trazabilidad del 2 y 3 de agosto; tratamiento solicitud por solicitud; inventario de examen de los seis expedientes; registro de preservación y remisión; acto nativo verificable; y cadena de actores.",
    "LZ-JUD-046": "Expediente certificado y puente de reparto; autos nativos; NIG; denuncia completa e índice de anexos; recepción o informe del Ministerio Fiscal; notificación y firmeza.",
    "GC-FIS-034": "Expediente e índice completos; acto nativo firmado de incoación; cualquier disposición posterior, incluida la referencia comunicada de 28 de febrero; NIG; firmante; y material examinado.",
    "NAT-FIS-005": "Expediente e índice completos; objeto; acto subyacente, si existe; traslado o asignación; NIG; firmante; y resultado.",
    "GC-FIS-035": "Acto subyacente; objeto; expediente e índice completos; disposición; NIG; firmante; material examinado; y cualquier traslado o tratamiento posterior.",
    "NAT-FIS-006": "Expediente e índice completos; objeto; traslado o asociación interna; funcionario asignado; NIG; identidad del firmante; y actuación o resultado posterior.",
    "NAT-FIS-007": "Expediente e índice completos; objeto; traslado o asociación interna; funcionario asignado; NIG; identidad del firmante; y actuación o resultado posterior.",
    "LZ-APP-046": "Identidad del LAJ; rollo certificado completo; registro de notificación y firmeza.",
    "LZ-APP-054": "NIG; resolución final firmada exacta; identidades del panel o Juez cuando proceda por el acto judicial; LAJ; notificación y firmeza.",
    "LZ-CIV-045": "Identidad del LAJ; expediente completo; recurso, firmeza y registro de notificación.",
    "LZ-FIS-049": "Extracción del Fiscal asignado o firmante; destino judicial y NIG; expediente completo de investigación; disposición y firmeza.",
    "LZ-FIS-051": "Clase exacta del expediente de Fiscalía; Fiscal asignado o firmante; decretos de incoación y archivo; anexos; notificación y firmeza.",
    "LZ-JUD-047": "Auto inicial o denuncia firmados; Juez; LAJ; Fiscal; acto de acumulación con DP 168/2015; disposición final, notificación y firmeza.",
    "LZ-JUD-048": "NIG; querella o denuncia; partes y capacidades exactas; Juez; LAJ; Fiscal; auto de archivo y firmeza.",
    "LZ-REF-038": "NIG; denuncia o querella; acto firmado de acumulación o ampliación de 15 de julio de 2017; Juez; LAJ; Fiscal; disposición final y notificación.",
    "LZ-REF-039": "NIG; sentencia firmada; Juez; LAJ; escritos de las partes; notificación y firmeza.",
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


def finite_test_family(row: dict[str, str]) -> str:
    """Return a conservative UI taxonomy; never a relationship classification."""
    stream = row.get("Stream", "").upper()
    master_id = row.get("Master_ID", "")
    record_type = row.get("Record_Type", "").upper()
    if "OMBUDSMAN" in stream or master_id.startswith("CAN-OMB-"):
        return "OMBUDSMAN_RECONSIDERATION"
    if "FISCAL" in stream or "-FIS-" in master_id:
        return "FISCALIA_INSTITUTIONAL_MEMORY"
    if (
        "AEAT" in stream
        or master_id.startswith("NAT-AEAT-")
        or master_id in {"MAD-AN-CONT-001", "MAD-AN-CONT-002"}
    ):
        return "TAX_CONTENTIOUS_CHAIN"
    if any(token in stream for token in ("CNMV", "SNCA", "TREASURY", "PUBLIC AID", "LAW 2/2023")):
        return "REGULATORY_PUBLIC_ROUTE"
    if record_type == "PROFESSIONAL_DISCIPLINE":
        return "PROFESSIONAL_SUPERVISION"
    # Record type/class take precedence over a mixed Stream label.  In
    # particular, "Administrative / professional" is an administrative
    # perimeter, not a disciplinary file, and a civil professional-liability
    # action remains a civil judicial proceeding.
    if record_type in {"ADMINISTRATIVE_FILE", "TRANSPARENCY_CLAIM"} or any(
        token in stream
        for token in (
            "ADMINISTRATIVE",
            "TOURISM",
            "MUNICIPAL",
            "TRANSPARENCY",
            "JUDICIAL GOVERNANCE",
        )
    ):
        return "ADMIN_AUTHORITY_TITLE_SOURCE"
    if "CRIMINAL" in stream:
        return "CRIMINAL_FILE_DECISION"
    if "CIVIL" in stream or "INSOLVENCY" in stream:
        return "CIVIL_FILE_DECISION"
    if "PROFESSIONAL" in stream:
        return "PROFESSIONAL_SUPERVISION"
    return "GENERAL_EXACT_FILE_DECISION_TEST"


def finite_question(row: dict[str, str], family_id: str) -> dict[str, str]:
    reference = row["Reference"].strip()
    purpose = row["Object_or_Purpose"].strip()
    organ = row["Origin_Organ"].strip()
    if family_id == "FISCALIA_INSTITUTIONAL_MEMORY":
        return bi(
            f"For {reference}, what did {organ} receive, incorporate, examine, refer and decide about {purpose}; what cross-file relevance was expressly acknowledged; and what remains unresolved?",
            f"Para {reference}, ¿qué recibió, incorporó, examinó, remitió y decidió {organ} sobre el objeto registrado; qué relevancia entre expedientes fue reconocida expresamente; y qué sigue sin resolver?",
        )
    if family_id == "CRIMINAL_FILE_DECISION":
        return bi(
            f"For {reference}, what exact source establishes {purpose}; what complaint, evidence and prosecution/court material was before {organ}; what was decided or referred; and what is the current review/finality status?",
            f"Para {reference}, ¿qué fuente exacta acredita el objeto registrado; qué denuncia, prueba y material fiscal/judicial estuvo ante {organ}; qué se decidió o remitió; y cuál es el estado actual de revisión/firmeza?",
        )
    if family_id == "CIVIL_FILE_DECISION":
        return bi(
            f"For {reference}, what exact source establishes {purpose}; what claim, title, opposition and evidence was before {organ}; what was decided or enforced; and what is the current appeal/finality status?",
            f"Para {reference}, ¿qué fuente exacta acredita el objeto registrado; qué demanda, título, oposición y prueba estuvo ante {organ}; qué se decidió o ejecutó; y cuál es el estado actual de recurso/firmeza?",
        )
    if family_id == "OMBUDSMAN_RECONSIDERATION":
        return bi(
            f"For {reference}, what submission and record concerning {purpose} was before {organ}; what reconsideration was requested; and what signed outcome and current status can be verified?",
            f"Para {reference}, ¿qué escrito y expediente sobre el objeto registrado estuvo ante {organ}; qué reconsideración se solicitó; y qué resultado firmado y estado actual pueden verificarse?",
        )
    if family_id == "PROFESSIONAL_SUPERVISION":
        return bi(
            f"For {reference}, what exact source establishes {purpose}; what mandate, complaint, response and evidence was before {organ}; and what decision, review and finality followed?",
            f"Para {reference}, ¿qué fuente exacta acredita el objeto registrado; qué encargo, queja, respuesta y prueba estuvo ante {organ}; y qué decisión, revisión y firmeza siguieron?",
        )
    if family_id == "TAX_CONTENTIOUS_CHAIN":
        return bi(
            f"For {reference}, what exact source establishes {purpose}; which tax act, evidence, challenge and collection consequence was before {organ}; and what review/finality status followed?",
            f"Para {reference}, ¿qué fuente exacta acredita el objeto registrado; qué acto tributario, prueba, impugnación y consecuencia recaudatoria estuvo ante {organ}; y qué estado de revisión/firmeza siguió?",
        )
    if family_id == "REGULATORY_PUBLIC_ROUTE":
        return bi(
            f"For {reference}, what exact source establishes {purpose}; what material was received or held by {organ}; what competence, secrecy, routing or merits treatment followed; and what remains open?",
            f"Para {reference}, ¿qué fuente exacta acredita el objeto registrado; qué material recibió o custodió {organ}; qué tratamiento competencial, de secreto, remisión o fondo siguió; y qué queda abierto?",
        )
    if family_id == "ADMIN_AUTHORITY_TITLE_SOURCE":
        return bi(
            f"For {reference}, what exact source establishes {purpose}; what authority, title, application or underlying record was before {organ}; what act followed; and what is its current effect/finality?",
            f"Para {reference}, ¿qué fuente exacta acredita el objeto registrado; qué autoridad, título, solicitud o registro de base estuvo ante {organ}; qué acto siguió; y cuál es su efecto/firmeza actual?",
        )
    return bi(
        f"For {reference}, what exact source establishes {purpose}; what material was before {organ}; what was decided or referred; and what is the current review/finality status?",
        f"Para {reference}, ¿qué fuente exacta acredita el objeto registrado; qué material estuvo ante {organ}; qué se decidió o remitió; y cuál es el estado actual de revisión/firmeza?",
    )


def finite_decision_fields(
    row: dict[str, str],
    family_id: str,
    direct_master_ids: list[str],
    context_master_ids: list[str],
) -> dict[str, dict[str, str]]:
    """Create file-specific, legally bounded dependencies and consequences."""
    reference = source_literal(row.get("Reference", "") or row["Master_ID"])
    purpose = source_literal(row.get("Object_or_Purpose", ""))
    organ = source_literal(
        row.get("Current_Custodian", "") or row.get("Origin_Organ", "")
    )
    direct_en = ", ".join(direct_master_ids) or "none currently admitted"
    direct_es = ", ".join(direct_master_ids) or "ninguno admitido actualmente"
    context_en = ", ".join(context_master_ids) or "none currently admitted"
    context_es = ", ".join(context_master_ids) or "ninguno admitido actualmente"
    related_en = (
        f"Controlled navigation currently identifies direct files [{direct_en}] and contextual files "
        f"[{context_en}]. Their presence does not establish receipt, admissibility or a duty to consider them."
    )
    related_es = (
        f"La navegación controlada identifica actualmente expedientes directos [{direct_es}] y contextuales "
        f"[{context_es}]. Su presencia no acredita recepción, admisibilidad ni deber de examinarlos."
    )

    family = {
        "OMBUDSMAN_RECONSIDERATION": {
            "decision_en": "whether the reconsideration/access record supports admission, response, correction and finality within the ombudsman body's competence",
            "decision_es": "si el expediente de reconsideración/acceso sustenta admisión, respuesta, corrección y firmeza dentro de la competencia del órgano de queja",
            "action_en": "retain or revise the recorded reconsideration/access treatment and identify the response or review still lawfully due",
            "action_es": "mantener o revisar el tratamiento registrado de reconsideración/acceso e identificar la respuesta o revisión aún legalmente debida",
            "contrary_en": "competence, admissibility, duplication, time limits or a lawful view that the requested material did not change the prior response",
            "contrary_es": "competencia, admisibilidad, duplicidad, plazos o una valoración lícita de que el material solicitado no cambiaba la respuesta anterior",
        },
        "CRIMINAL_FILE_DECISION": {
            "decision_en": "whether the complete criminal file supports its admission, investigative steps, closure, review and current finality",
            "decision_es": "si el expediente penal completo sustenta su admisión, diligencias, archivo, revisión y firmeza actual",
            "action_en": "retain or revise the recorded admission/investigation/closure/review treatment and identify any next investigative or judicial step",
            "action_es": "mantener o revisar el tratamiento registrado de admisión/investigación/archivo/revisión e identificar cualquier siguiente diligencia o actuación judicial",
            "contrary_en": "a lawful application of competence, duplication or judicialisation rules, the criminal threshold, admissibility, evidential sufficiency or procedural finality",
            "contrary_es": "una aplicación lícita de reglas de competencia, duplicidad o judicialización, umbral penal, admisibilidad, suficiencia probatoria o firmeza procesal",
        },
        "CIVIL_FILE_DECISION": {
            "decision_en": "whether the complete civil file supports the recorded claim, defence, title, enforcement or relief and its appeal/finality status",
            "decision_es": "si el expediente civil completo sustenta la pretensión, defensa, título, ejecución o tutela registradas y su estado de recurso/firmeza",
            "action_en": "retain or revise the recorded civil, title, enforcement or appeal treatment within the competent court's powers",
            "action_es": "mantener o revisar el tratamiento civil, de título, ejecución o recurso registrado dentro de las potestades del órgano competente",
            "contrary_en": "a lawful application of party scope, title, standing, res judicata, evidence, procedural discretion, enforcement or finality rules",
            "contrary_es": "una aplicación lícita de reglas sobre partes, título, legitimación, cosa juzgada, prueba, discrecionalidad procesal, ejecución o firmeza",
        },
        "FISCALIA_INSTITUTIONAL_MEMORY": {
            "decision_en": "whether the complete prosecution file supports the recorded receipt, allocation, referral, examination, response, closure and cross-file treatment",
            "decision_es": "si el expediente fiscal completo sustenta la recepción, reparto, remisión, examen, respuesta, archivo y tratamiento entre expedientes registrados",
            "action_en": "retain or revise the file-specific receipt/referral/examination/response record and identify any competent investigative, review or preservation step",
            "action_es": "mantener o revisar el registro específico de recepción/remisión/examen/respuesta e identificar cualquier diligencia, revisión o preservación competente",
            "contrary_en": "a lawful limitation based on competence, territorial routing, duplication, judicialisation, evidential threshold, confidentiality or independent file-specific reasoning",
            "contrary_es": "una limitación lícita basada en competencia, remisión territorial, duplicidad, judicialización, umbral probatorio, confidencialidad o razonamiento independiente del expediente",
        },
        "PROFESSIONAL_SUPERVISION": {
            "decision_en": "whether the complete professional-supervision file supports competence, receipt, investigation, response, referral and finality",
            "decision_es": "si el expediente completo de supervisión profesional sustenta competencia, recepción, investigación, respuesta, remisión y firmeza",
            "action_en": "retain or revise the recorded professional-supervision disposition and identify any response, referral, disciplinary or review step within competence",
            "action_es": "mantener o revisar la disposición registrada de supervisión profesional e identificar cualquier respuesta, remisión, actuación disciplinaria o revisión competente",
            "contrary_en": "a lawful limitation based on territorial or subject-matter competence, professional secrecy, standing, admissibility, duplication or procedural finality",
            "contrary_es": "una limitación lícita basada en competencia territorial o material, secreto profesional, legitimación, admisibilidad, duplicidad o firmeza procesal",
        },
        "ADMIN_AUTHORITY_TITLE_SOURCE": {
            "decision_en": "whether the complete administrative file supports the recorded authority, title, access, licence, application, act and current legal effect",
            "decision_es": "si el expediente administrativo completo sustenta la autoridad, título, acceso, licencia, solicitud, acto y efecto jurídico actual registrados",
            "action_en": "retain, correct or review the recorded administrative act, title, access or authority status within the competent body's powers",
            "action_es": "mantener, corregir o revisar el acto, título, acceso o estado de autoridad registrado dentro de las potestades del órgano competente",
            "contrary_en": "a lawful application of competence, title, data-protection, confidentiality, access, licensing, time-limit or administrative-discretion rules",
            "contrary_es": "una aplicación lícita de reglas de competencia, título, protección de datos, confidencialidad, acceso, licencia, plazos o discrecionalidad administrativa",
        },
        "TAX_CONTENTIOUS_CHAIN": {
            "decision_en": "whether the complete tax/contentious file supports the recorded tax act, evidence, challenge, collection consequence, review and finality",
            "decision_es": "si el expediente tributario/contencioso completo sustenta el acto tributario, prueba, impugnación, consecuencia recaudatoria, revisión y firmeza registrados",
            "action_en": "retain or revise the recorded tax, collection or contentious-review treatment within the competent organ's powers",
            "action_es": "mantener o revisar el tratamiento tributario, recaudatorio o contencioso registrado dentro de las potestades del órgano competente",
            "contrary_en": "a lawful application of tax confidentiality, competence, assessment, evidence, collection, limitation, review or finality rules",
            "contrary_es": "una aplicación lícita de reglas de confidencialidad tributaria, competencia, liquidación, prueba, recaudación, prescripción, revisión o firmeza",
        },
        "REGULATORY_PUBLIC_ROUTE": {
            "decision_en": "whether the complete regulatory/public-authority file supports the recorded receipt, competence, secrecy, referral, merits response and finality",
            "decision_es": "si el expediente regulatorio/de autoridad pública completo sustenta la recepción, competencia, secreto, remisión, respuesta de fondo y firmeza registradas",
            "action_en": "retain or revise the recorded regulatory response, referral, access or supervisory treatment and identify the competent next step",
            "action_es": "mantener o revisar la respuesta, remisión, acceso o tratamiento supervisor registrado e identificar la siguiente actuación competente",
            "contrary_en": "a lawful application of competence, secrecy, data-protection, admissibility, referral, supervisory discretion or finality rules",
            "contrary_es": "una aplicación lícita de reglas de competencia, secreto, protección de datos, admisibilidad, remisión, discrecionalidad supervisora o firmeza",
        },
        "GENERAL_EXACT_FILE_DECISION_TEST": {
            "decision_en": "whether the complete exact file supports its recorded object, evidence treatment, decision or referral and current review/finality status",
            "decision_es": "si el expediente exacto completo sustenta su objeto registrado, tratamiento probatorio, decisión o remisión y estado actual de revisión/firmeza",
            "action_en": "retain or revise the recorded file-specific disposition and identify the next competent procedural or institutional step",
            "action_es": "mantener o revisar la disposición específica registrada e identificar la siguiente actuación procesal o institucional competente",
            "contrary_en": "a lawful file-specific application of competence, scope, admissibility, evidence, procedural discretion, referral or finality rules",
            "contrary_es": "una aplicación lícita y específica del expediente de reglas de competencia, ámbito, admisibilidad, prueba, discrecionalidad procesal, remisión o firmeza",
        },
    }[family_id]

    decision = bi(
        f"For {reference}, the finite decision question is whether the legally competent organ must determine {family['decision_en']} for the recorded object “{purpose}”. {organ} is only the recorded custodian/organ candidate and is not treated here as legally competent or obliged to act. {related_en}",
        f"Para {reference}, la cuestión decisoria finita es si el órgano legalmente competente debe determinar {family['decision_es']} respecto del objeto registrado «{purpose}». {organ} es solo el candidato registrado como custodio/órgano y aquí no se le atribuye competencia jurídica ni obligación de actuar. {related_es}",
    )
    contrary = bi(
        f"For {reference}, the strongest hypothetical innocent or contrary explanation could be {family['contrary_en']}, but only if the primary record establishes that the legally competent organ applied it to “{purpose}”. No act is attributed by this model to the recorded candidate {organ}. A different treatment, missing public inventory or related-file membership alone does not establish concealment, coordination, error or wrongdoing.",
        f"Para {reference}, la explicación inocente o contraria hipotética más fuerte podría ser {family['contrary_es']}, pero solo si la fuente primaria acredita que el órgano legalmente competente la aplicó a «{purpose}». Este modelo no atribuye actuación alguna al candidato registrado {organ}. Un tratamiento distinto, la falta de inventario público o la pertenencia a expedientes relacionados no acreditan por sí solos ocultación, coordinación, error ni ilicitud.",
    )
    confirmed = bi(
        f"If the requested primary record confirms the recorded object, treatment and current status in {reference}, the legally competent organ could determine within its powers whether to {family['action_en']}. The recorded candidate {organ} is not treated as competent merely because it is named in the register. Confirmation remains file-specific and does not establish another file's treatment, personal knowledge, causation, wrongdoing or liability.",
        f"Si la fuente primaria solicitada confirma el objeto, tratamiento y estado actual registrados en {reference}, el órgano legalmente competente podría determinar dentro de sus potestades si procede {family['action_es']}. El candidato registrado {organ} no se considera competente por el mero hecho de figurar en el registro. La confirmación sigue siendo específica del expediente y no acredita el tratamiento de otro expediente, conocimiento personal, causalidad, ilicitud ni responsabilidad.",
    )
    refuted = bi(
        f"If the primary record refutes the recorded object, treatment or status in {reference}, that discrepancy would call for correction of the canonical record and every affected direct/context classification, preservation of the contrary source, and assessment by the legally competent organ of any file-specific consequence. The recorded candidate {organ} is not treated as competent or required to act by this model.",
        f"Si la fuente primaria refuta el objeto, tratamiento o estado registrado en {reference}, esa discrepancia exigiría corregir el registro canónico y toda clasificación directa/contextual afectada, conservar la fuente contraria y que el órgano legalmente competente valore cualquier consecuencia específica del expediente. Este modelo no considera competente ni obliga a actuar al candidato registrado {organ}.",
    )
    return {
        "decision_dependency": decision,
        "contrary": contrary,
        "if_confirmed": confirmed,
        "if_refuted": refuted,
    }


def fiscalia_axis_basis(
    master_id: str,
    axes: dict[str, str],
    profile: dict[str, Any] | None,
) -> dict[str, dict[str, Any]]:
    """Explain every institutional grade without converting it into actor proof."""
    result: dict[str, dict[str, Any]] = {}
    for axis, label in FISCALIA_AXIS_LABELS.items():
        status = axes[axis]
        if profile:
            source_field = FISCALIA_EPISODE_AXIS_SOURCE_FIELD_OVERRIDES.get(
                (profile["episode_id"], axis), FISCALIA_AXIS_SOURCE_FIELDS[axis]
            )
            raw_field = {
                "source_authored_known_summary": "known",
                "institutional_response": "response",
            }[source_field]
            if status in {"NOT_LOCATED", "STATUS_UNRESOLVED"}:
                basis = bi(
                    f"The reviewed episode does not establish {label['en'].lower()} at a stronger grade. Open source-controlled question: {profile['open_question_en']}",
                    f"El episodio revisado no acredita {label['es'].lower()} con un grado más fuerte. Pregunta abierta controlada por fuente: {profile['open_question_es']}",
                )
                basis_kind = "CONTROLLED_CORPUS_GAP_STATEMENT"
                source_field = "open_question"
                raw_field = "unresolved"
            else:
                basis = bi(
                    profile[f"{source_field}_en"],
                    profile[f"{source_field}_es"],
                )
                basis_kind = "ANALYTICAL_GRADE_FROM_SOURCE_AUTHORED_EPISODE_FIELD"
            source = {
                "kind": "CONTROLLED_FISCALIA_RESPONSE_EPISODE",
                "path": "assets/data/fiscalia-response-correspondence.json",
                "field": f"episodes[].{raw_field}_en/{raw_field}_es",
                "record_id": profile["episode_id"],
                "profile_id": profile["profile_id"],
            }
        else:
            basis = bi(
                f"No source-controlled episode profile establishing {label['en'].lower()} has been located for {master_id}. NOT_LOCATED describes the controlled corpus, not nonexistence.",
                f"No se ha localizado para {master_id} un perfil de episodio controlado por fuente que acredite {label['es'].lower()}. NOT_LOCATED describe el corpus controlado, no inexistencia.",
            )
            basis_kind = "EXPLICIT_SOURCE_NOT_LOCATED"
            source = {
                "kind": "PUBLIC_SOURCE_NOT_LOCATED",
                "record_id": master_id,
                "status": "NOT_LOCATED",
            }
        result[axis] = {
            "status": status,
            "basis_kind": basis_kind,
            "basis_en": basis["en"],
            "basis_es": basis["es"],
            "limitation_en": FISCALIA_AXIS_LIMITS[axis]["en"],
            "limitation_es": FISCALIA_AXIS_LIMITS[axis]["es"],
            "source": source,
        }
    return result


def receipt_knowledge_profile(
    master_id: str,
    episode_profiles: list[dict[str, Any]],
) -> dict[str, Any]:
    matched_profiles = [
        profile for profile in episode_profiles if profile["master_id"] == master_id
    ]
    profile_ids = [profile["profile_id"] for profile in matched_profiles]
    if profile_ids:
        matched_profile = matched_profiles[0]
        axes = FISCALIA_EPISODE_AXES[matched_profile["episode_id"]]
        classification = "SOURCE_BACKED_INSTITUTIONAL_TRACE"
    else:
        matched_profile = None
        axes = {
            "transmission_status": "NOT_LOCATED",
            "material_received_status": "NOT_LOCATED",
            "referral_status": "NOT_LOCATED",
            "registration_status": "NOT_LOCATED",
            "file_incorporation_status": "NOT_LOCATED",
            "recipient_attribution_status": "NOT_LOCATED",
            "substantive_examination_status": "NOT_LOCATED",
            "decision_use_status": "NOT_LOCATED",
            "cross_file_acknowledgement_status": "NOT_LOCATED",
        }
        classification = "EXPLICIT_SOURCE_NOT_LOCATED"
    return {
        "classification": classification,
        "source_profile_ids": profile_ids,
        "event_refs": [
            {
                "profile_id": profile["profile_id"],
                "event_id": profile["episode_id"],
                "date": profile["date"],
                "source_kind": "CONTROLLED_FISCALIA_RESPONSE_EPISODE",
                "proves_en": (
                    "A source-controlled institutional episode profile is mapped to this exact "
                    "Master ID at the stated evidential grades."
                ),
                "proves_es": (
                    "Un perfil institucional de episodio controlado por fuente está asociado a "
                    "este Master ID exacto con los grados probatorios indicados."
                ),
                "does_not_prove_en": (
                    "It does not by itself prove personal receipt, complete incorporation, "
                    "complete examination, agreement, intent, causation, wrongdoing or liability."
                ),
                "does_not_prove_es": (
                    "No acredita por sí solo recepción personal, incorporación completa, examen "
                    "completo, acuerdo, intención, causalidad, ilicitud ni responsabilidad."
                ),
            }
            for profile in matched_profiles
        ],
        "institutional_axes": {
            field: axes[field]
            for field in (
                "transmission_status",
                "registration_status",
                "file_incorporation_status",
                "recipient_attribution_status",
                "substantive_examination_status",
                "decision_use_status",
            )
        },
        "institutional_axis_basis": fiscalia_axis_basis(
            master_id, axes, matched_profile
        ),
        "cross_file_acknowledgement_status": axes[
            "cross_file_acknowledgement_status"
        ],
        "actor_specific": {
            "receipt_status": "NOT_ESTABLISHED",
            "knowledge_status": "NOT_ESTABLISHED",
            "source_status": "NO_ACTOR_SPECIFIC_SOURCE_LOCATED",
            "actor_ids": [],
            "boundary_en": (
                "No person-specific receipt or knowledge is inferred from institutional "
                "possession, routing, office, signature or chronology."
            ),
            "boundary_es": (
                "No se infiere recepción ni conocimiento personal de la posesión institucional, "
                "remisión, cargo, firma o cronología."
            ),
        },
        "limitations_en": (
            "Institutional handling does not establish personal receipt, knowledge, "
            "instruction, agreement, intent, causation, wrongdoing or liability."
        ),
        "limitations_es": (
            "La tramitación institucional no acredita recepción personal, conocimiento, "
            "instrucción, acuerdo, intención, causalidad, ilicitud ni responsabilidad."
        ),
    }


def fiscalia_response_episode_profiles(
    public_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    payload = json.loads(FISCALIA_RESPONSES.read_text(encoding="utf-8"))
    episodes = payload.get("episodes", [])
    by_id = {row["Master_ID"]: row for row in public_rows}
    episode_ids = {episode.get("id") for episode in episodes}
    if len(episodes) != EXPECTED_FISCALIA_RESPONSE_EPISODES:
        raise ValueError(
            "expected "
            f"{EXPECTED_FISCALIA_RESPONSE_EPISODES} Fiscalía response episodes, "
            f"found {len(episodes)}"
        )
    if episode_ids != set(FISCALIA_EPISODE_TO_MASTER_ID):
        raise ValueError("Fiscalía episode-to-Master mapping is incomplete or stale")
    if set(FISCALIA_EPISODE_AXES) != episode_ids:
        raise ValueError("Fiscalía episode institutional-axis mapping is incomplete or stale")

    profiles: list[dict[str, Any]] = []
    for episode in episodes:
        episode_id = episode["id"]
        master_id = FISCALIA_EPISODE_TO_MASTER_ID[episode_id]
        row = by_id.get(master_id)
        if not row or row.get("Is_Proceeding") != "TRUE":
            raise ValueError(
                f"{episode_id} maps to a missing or non-exact public Master ID: {master_id}"
            )
        axes = FISCALIA_EPISODE_AXES[episode_id]
        profile = {
                "profile_id": f"FISCALIA-RESPONSE-{episode_id}",
                "episode_id": episode_id,
                "master_id": master_id,
                "date": episode.get("date", ""),
                "title_en": episode.get("title_en", ""),
                "title_es": episode.get("title_es", ""),
                "source_authored_known_summary_en": episode.get("known_en", ""),
                "source_authored_known_summary_es": episode.get("known_es", ""),
                "source_authored_request_summary_en": episode.get("requested_en", ""),
                "source_authored_request_summary_es": episode.get("requested_es", ""),
                "institutional_response_en": episode.get("response_en", ""),
                "institutional_response_es": episode.get("response_es", ""),
                "open_question_en": episode.get("unresolved_en", ""),
                "open_question_es": episode.get("unresolved_es", ""),
                "later_event_en": episode.get("next_en", ""),
                "later_event_es": episode.get("next_es", ""),
                "contrary_or_limiting_record_en": episode.get("causation_en", ""),
                "contrary_or_limiting_record_es": episode.get("causation_es", ""),
                "causation_status": episode.get("causation_level", ""),
                "institutional_axes": {
                    field: axes[field]
                    for field in (
                        "transmission_status",
                        "registration_status",
                        "file_incorporation_status",
                        "recipient_attribution_status",
                        "substantive_examination_status",
                        "decision_use_status",
                    )
                },
                "cross_file_acknowledgement_status": axes[
                    "cross_file_acknowledgement_status"
                ],
                "attribution_boundary": (
                    "SOURCE_AUTHORED_MIXED_SUMMARY_FIELDS; read each statement at its stated "
                    "document/authority/party attribution; no actor-specific receipt or knowledge inferred"
                ),
                "source": {
                    "kind": "CONTROLLED_FISCALIA_RESPONSE_EPISODE",
                    "path": "assets/data/fiscalia-response-correspondence.json",
                    "field": "episodes[]",
                    "record_id": episode_id,
                },
            }
        profile["institutional_axis_basis"] = fiscalia_axis_basis(
            master_id, axes, profile
        )
        profiles.append(profile)
    return profiles


def fiscalia_office_file_matrix(
    public_rows: list[dict[str, str]],
    relationships: list[dict[str, Any]],
    context_clusters: list[dict[str, Any]],
    episode_profiles: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build the finite public Fiscalía office/file denominator.

    Membership comes only from the canonical Stream taxonomy.  Episode links
    come only from the reviewed explicit map above; raw matter_references are
    deliberately ignored.
    """
    rows = [row for row in public_rows if "FISCAL" in row.get("Stream", "").upper()]
    if len(rows) != EXPECTED_FISCALIA_OFFICE_FILE_RECORDS:
        raise ValueError(
            "expected "
            f"{EXPECTED_FISCALIA_OFFICE_FILE_RECORDS} public Fiscalía records, "
            f"found {len(rows)}"
        )
    profile_by_master: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for profile in episode_profiles:
        profile_by_master[profile["master_id"]].append(profile)
    related_by_master: dict[str, set[str]] = defaultdict(set)
    for relationship in relationships:
        left = relationship["from_master_id"]
        right = relationship["to_master_id"]
        related_by_master[left].add(right)
        related_by_master[right].add(left)
    context_by_master: dict[str, set[str]] = defaultdict(set)
    for cluster in context_clusters:
        members = set(cluster.get("member_master_ids", []))
        for member in members:
            context_by_master[member].update(members - {member})

    matrix: list[dict[str, Any]] = []
    for row in rows:
        master_id = row["Master_ID"]
        profiles = profile_by_master.get(master_id, [])
        if profiles:
            profile = profiles[0]
            known = bi(
                profile["source_authored_known_summary_en"],
                profile["source_authored_known_summary_es"],
            )
            requested = bi(
                profile["source_authored_request_summary_en"],
                profile["source_authored_request_summary_es"],
            )
            response = bi(
                profile["institutional_response_en"],
                profile["institutional_response_es"],
            )
            open_question = bi(
                profile["open_question_en"], profile["open_question_es"]
            )
            axes = FISCALIA_EPISODE_AXES[profile["episode_id"]]
            cross_file_status = profile["cross_file_acknowledgement_status"]
            axis_basis = profile["institutional_axis_basis"]
            profile_status = "SOURCE_CONTROLLED_PROFILE"
        else:
            known = bi(
                "No source-controlled received/known profile is located for this office/file row.",
                "No se ha localizado un perfil controlado de recepción/conocimiento para esta fila de oficina/expediente.",
            )
            requested = bi(
                "Obtain the native submission, registration, allocation and annex inventory.",
                "Obtener el escrito nativo, registro, reparto e inventario de anexos.",
            )
            response = bi(
                "No source-controlled response profile is located in this matrix.",
                "No se ha localizado en esta matriz un perfil controlado de respuesta.",
            )
            open_question = bi(
                row.get("Open_Reference_Gap", "").strip()
                or "Native file, exact identity, receipt, examination and outcome.",
                GAP_ES.get(
                    master_id,
                    "Expediente nativo, identidad exacta, recepción, examen y resultado.",
                ),
            )
            axes = {
                "transmission_status": "NOT_LOCATED",
                "material_received_status": "NOT_LOCATED",
                "referral_status": "NOT_LOCATED",
                "registration_status": "NOT_LOCATED",
                "file_incorporation_status": "NOT_LOCATED",
                "recipient_attribution_status": "NOT_LOCATED",
                "substantive_examination_status": "NOT_LOCATED",
                "decision_use_status": "NOT_LOCATED",
                "cross_file_acknowledgement_status": "NOT_LOCATED",
            }
            cross_file_status = "NOT_LOCATED"
            axis_basis = fiscalia_axis_basis(master_id, axes, None)
            profile_status = "EXPLICIT_PROFILE_GAP"

        direct_master_ids = sorted(related_by_master.get(master_id, set()))
        context_master_ids = sorted(context_by_master.get(master_id, set()))
        related_master_ids = sorted(set(direct_master_ids) | set(context_master_ids))
        related_status = (
            "CONTROLLED_NAVIGATION_ONLY" if related_master_ids else "NOT_LOCATED"
        )
        material_allegations_evidence = (
            [
                {
                    "kind": "SOURCE_AUTHORED_KNOWN_SUMMARY",
                    "text_en": profile["source_authored_known_summary_en"],
                    "text_es": profile["source_authored_known_summary_es"],
                    "attribution": "SOURCE_AUTHORED_MIXED_SUMMARY_NOT_RECEIPT_INVENTORY",
                },
                {
                    "kind": "SOURCE_AUTHORED_REQUEST_SUMMARY",
                    "text_en": profile["source_authored_request_summary_en"],
                    "text_es": profile["source_authored_request_summary_es"],
                    "attribution": "REQUESTED_MATERIAL_NOT_PROOF_OF_RECEIPT_OR_EXAMINATION",
                },
            ]
            if profiles
            else []
        )
        if axes["referral_status"] == "ROUTING_DOCUMENTED":
            what_was_referred = bi(
                profile["source_authored_known_summary_en"],
                profile["source_authored_known_summary_es"],
            )
        else:
            what_was_referred = bi(
                "No source-controlled referral of identified material has been located for this office/file row.",
                "No se ha localizado para esta fila de oficina/expediente una remisión controlada por fuente de material identificado.",
            )
        if axes["substantive_examination_status"] in {
            "DOCUMENTED",
            "PARTLY_DOCUMENTED",
        }:
            what_was_actually_examined = bi(
                "No complete itemised corpus actually examined has been located. The controlled response establishes only this bounded treatment: "
                + profile["institutional_response_en"],
                "No se ha localizado un corpus completo e individualizado efectivamente examinado. La respuesta controlada acredita solo este tratamiento limitado: "
                + profile["institutional_response_es"],
            )
        else:
            what_was_actually_examined = bi(
                "No source-controlled inventory of the material actually examined has been located for this office/file row.",
                "No se ha localizado para esta fila de oficina/expediente un inventario controlado por fuente del material efectivamente examinado.",
            )

        matrix.append(
            {
                "master_id": master_id,
                "reference": row.get("Reference", ""),
                "origin_office": row.get("Origin_Organ", ""),
                "current_custodian": row.get("Current_Custodian", ""),
                "is_proceeding": row.get("Is_Proceeding", ""),
                "record_type": row.get("Record_Type", ""),
                "date_or_period": profiles[0]["date"] if profiles else row.get("Date_or_Period", ""),
                "source_status": row.get("Source_Status", ""),
                "profile_status": profile_status,
                "source_profile_ids": [profile["profile_id"] for profile in profiles],
                "received_or_known": known,
                "requested": requested,
                "institutional_response": response,
                "material_allegations_evidence": material_allegations_evidence,
                "material_received": [],
                "material_received_status": axes["material_received_status"],
                "material_inventory_gap": bi(
                    "No complete item-by-item received-material inventory has been located in the controlled corpus.",
                    "No se ha localizado en el corpus controlado un inventario completo elemento por elemento del material recibido.",
                ),
                "related_master_ids": related_master_ids,
                "related_direct_master_ids": direct_master_ids,
                "related_context_master_ids": context_master_ids,
                "related_proceedings_status": related_status,
                "related_assets": [],
                "related_assets_status": "NOT_LOCATED",
                "related_assets_gap": bi(
                    "No separate source-controlled asset inventory is established by this matrix row.",
                    "Esta fila de la matriz no acredita un inventario separado de activos controlado por fuente.",
                ),
                "related_proceedings_assets_status": related_status,
                "transmission_status": axes["transmission_status"],
                "referral_status": axes["referral_status"],
                "what_was_referred": what_was_referred,
                "registration_status": axes["registration_status"],
                "file_incorporation_status": axes["file_incorporation_status"],
                "recipient_attribution_status": axes["recipient_attribution_status"],
                "substantive_examination_status": axes["substantive_examination_status"],
                "what_was_actually_examined": what_was_actually_examined,
                "decision_use_status": axes["decision_use_status"],
                "cross_file_acknowledgement_status": cross_file_status,
                "unitary_acknowledgement_status": "NOT_LOCATED",
                "institutional_axis_basis": axis_basis,
                "strongest_contrary": bi(
                    "The office may have lawfully narrowed, referred or decided the material within its competence; a missing public inventory does not establish that no internal review occurred.",
                    "La oficina pudo acotar, remitir o resolver lícitamente el material dentro de su competencia; la ausencia de inventario público no acredita que no existiera revisión interna.",
                ),
                "unanswered_or_source_gap": open_question,
                "boundary_en": (
                    "This row does not infer receipt, incorporation, examination or cross-file "
                    "acknowledgement from raw matter references."
                ),
                "boundary_es": (
                    "Esta fila no infiere recepción, incorporación, examen ni reconocimiento "
                    "entre expedientes a partir de referencias de asunto sin controlar."
                ),
            }
        )
    return matrix


def finite_test_for_row(
    row: dict[str, str],
    direct_ids: list[str],
    cluster_ids: list[str],
    relationships_by_id: dict[str, dict[str, Any]],
    clusters_by_id: dict[str, dict[str, Any]],
    episode_profiles: list[dict[str, Any]],
) -> dict[str, Any]:
    master_id = row["Master_ID"]
    family_id = finite_test_family(row)
    direct_master_ids = sorted(
        {
            relationship["to_master_id"]
            if relationship["from_master_id"] == master_id
            else relationship["from_master_id"]
            for relationship_id in direct_ids
            for relationship in [relationships_by_id[relationship_id]]
        }
    )
    context_master_ids = sorted(
        {
            related_id
            for cluster_id in cluster_ids
            for related_id in clusters_by_id[cluster_id]["member_master_ids"]
            if related_id != master_id
        }
    )
    connection_statuses: list[str] = []
    if direct_master_ids:
        connection_statuses.append("DIRECT_PROCEDURAL_EDGE")
    if context_master_ids:
        connection_statuses.append("MATERIALLY_RELEVANT_CONTEXT")
    if not connection_statuses:
        connection_statuses.append("NOT_LOCATED")

    source_status = row.get("Source_Status", "").strip()
    source_needed_status = (
        "NOT_LOCATED"
        if source_status in {"OPEN_REFERENCE", "CORPUS_REPORTED_PRIMARY_PENDING"}
        else "STATUS_UNRESOLVED"
    )
    custodian = row.get("Current_Custodian", "").strip() or row.get("Origin_Organ", "").strip()
    organ_status = (
        "STATUS_UNRESOLVED"
        if re.search(r"pending|to verify|por determinar|exact custodian", custodian, re.I)
        else "RECORDED_CURRENT_CUSTODIAN"
    )
    attribution = (
        "DOCUMENTED_PROCEDURAL_RECORD_WITH_OPEN_COMPLETION"
        if source_status.startswith("VERIFIED_")
        or source_status.startswith("PRIMARY_COMPLAINT_")
        else "OPEN_QUESTION_SOURCE_NOT_LOCATED_OR_PRIMARY_PENDING"
    )

    decision_fields = finite_decision_fields(
        row,
        family_id,
        direct_master_ids,
        context_master_ids,
    )
    return {
        "id": f"FT-{master_id}",
        "status": "STATUS_UNRESOLVED",
        "family_template_id": family_id,
        "family_taxonomy_only": True,
        "question": finite_question(row, family_id),
        "recorded_object": row.get("Object_or_Purpose", ""),
        "attribution": attribution,
        "source_needed": bi(row.get("Open_Reference_Gap", "").strip(), GAP_ES[master_id]),
        "current_source_status": source_status,
        "source_needed_status": source_needed_status,
        "source_refs": [
            {
                "kind": "CANONICAL_PUBLIC_RECORD",
                "source_id": master_id,
                "status": "CANONICAL_METADATA_ONLY_NOT_PRIMARY_SOURCE",
                "label_en": f"Canonical public record {master_id}",
                "label_es": f"Registro público canónico {master_id}",
                "href_en": f"en/master-proceedings-register/#record-{master_id}",
                "href_es": f"es/registro-maestro-procedimientos/#record-{master_id}",
                "limitations_en": "This route proves the controlled metadata entry, not the underlying primary file or its merits.",
                "limitations_es": "Esta ruta acredita la entrada de metadatos controlada, no el expediente primario subyacente ni el fondo.",
            },
            {
                "kind": "PUBLIC_SOURCE_ROUTE_GAP",
                "status": "PUBLIC_SOURCE_ROUTE_NOT_ESTABLISHED",
                "label_en": "Proceeding-specific public primary-source route not established",
                "label_es": "No se ha establecido una ruta pública de fuente primaria específica del expediente",
            }
        ],
        "competent_organ": {
            "recorded_candidate": custodian,
            "basis_field": (
                "Current_Custodian"
                if row.get("Current_Custodian", "").strip()
                else "Origin_Organ"
            ),
            "status": organ_status,
        },
        "related_proceedings": {
            "direct_master_ids": direct_master_ids,
            "context_master_ids": context_master_ids,
            "context_cluster_ids": cluster_ids,
            "direct": direct_master_ids,
            "context": context_master_ids,
            "connection_statuses": connection_statuses,
            "treatment_status": "STATUS_UNRESOLVED",
        },
        "procedural_availability": bi(
            "Whether another file or source was lawfully available, admissible or within scope must be determined in the selected proceeding; no availability or duty to consider is inferred from this navigation model.",
            "La disponibilidad lícita, admisibilidad o inclusión en el ámbito de otro expediente o fuente debe determinarse en el procedimiento seleccionado; este modelo de navegación no infiere disponibilidad ni deber de examen.",
        ),
        "decision_dependency": decision_fields["decision_dependency"],
        "contrary_explanation": decision_fields["contrary"],
        "strongest_contrary_or_innocent_explanation": decision_fields["contrary"],
        "if_confirmed": decision_fields["if_confirmed"],
        "if_refuted": decision_fields["if_refuted"],
        "receipt_knowledge": receipt_knowledge_profile(master_id, episode_profiles),
        "navigation": {
            "controlled_trace_fragment": f"#trace-proceeding={master_id}",
            "controlled_isolation_fragment": f"#isolation-test={master_id}",
            "master_register_route_en": f"en/master-proceedings-register/#record-{master_id}",
            "master_register_route_es": f"es/registro-maestro-procedimientos/#record-{master_id}",
            "controlled_trace_route_en": f"en/proceedings-map/#trace-proceeding={master_id}",
            "controlled_trace_route_es": f"es/mapa-procedimientos/#trace-proceeding={master_id}",
            "controlled_isolation_route_en": f"en/proceedings-map/#isolation-test={master_id}",
            "controlled_isolation_route_es": f"es/mapa-procedimientos/#isolation-test={master_id}",
            "controlled_navigation_status": "AVAILABLE",
            "dedicated_narrative_dossier_status": "PARTIAL_NOT_INFERRED",
        },
    }


def finite_test_is_complete(test: dict[str, Any]) -> bool:
    bilingual_fields = (
        "question",
        "source_needed",
        "procedural_availability",
        "decision_dependency",
        "contrary_explanation",
        "if_confirmed",
        "if_refuted",
    )
    if any(
        not isinstance(test.get(field), dict)
        or not test[field].get("en")
        or not test[field].get("es")
        for field in bilingual_fields
    ):
        return False
    receipt = test.get("receipt_knowledge", {})
    axes = receipt.get("institutional_axes", {})
    mandatory_axes = {
        "transmission_status",
        "registration_status",
        "file_incorporation_status",
        "recipient_attribution_status",
        "substantive_examination_status",
        "decision_use_status",
    }
    return all(
        (
            test.get("id"),
            test.get("status"),
            test.get("family_template_id"),
            test.get("current_source_status"),
            test.get("source_needed_status"),
            test.get("competent_organ", {}).get("recorded_candidate"),
            test.get("competent_organ", {}).get("status"),
            test.get("related_proceedings", {}).get("treatment_status"),
            test.get("source_refs"),
            test.get("navigation", {}).get("controlled_trace_route_en"),
            test.get("navigation", {}).get("controlled_trace_route_es"),
            test.get("navigation", {}).get("controlled_isolation_route_en"),
            test.get("navigation", {}).get("controlled_isolation_route_es"),
            receipt.get("classification"),
            set(axes) == mandatory_axes,
            receipt.get("cross_file_acknowledgement_status"),
            receipt.get("actor_specific", {}).get("source_status")
            == "NO_ACTOR_SPECIFIC_SOURCE_LOCATED",
        )
    )


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


def source_controlled_context_clusters(
    exact_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Materialise explicit contextual corridors from specialist source controls."""
    by_id = {row["Master_ID"]: row for row in exact_rows}
    clusters: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for path in CONTEXT_SOURCE_FILES:
        payload = json.loads(path.read_text(encoding="utf-8"))
        relative_path = path.relative_to(ROOT).as_posix()
        for corridor in payload.get("proceedings_context_corridors", []):
            record_id = corridor.get("id", "").strip()
            cluster_id = f"CTX-SOURCE-{record_id}"
            member_ids = corridor.get("member_master_ids", [])
            if not record_id or cluster_id in seen_ids:
                raise ValueError(f"duplicate or missing source-controlled corridor ID in {relative_path}")
            if corridor.get("context_type") != "SOURCE_CONTROLLED_CORRIDOR":
                raise ValueError(f"{record_id} has an unsupported specialist context type")
            if len(member_ids) < 2 or len(member_ids) != len(set(member_ids)):
                raise ValueError(f"{record_id} requires at least two unique exact members")
            if any(master_id not in by_id for master_id in member_ids):
                raise ValueError(f"{record_id} names a non-exact or unavailable member")
            required_text = (
                "label_en", "label_es", "why_en", "why_es",
                "limitations_en", "limitations_es", "evidence_status",
            )
            if any(not corridor.get(field) for field in required_text):
                raise ValueError(f"{record_id} lacks bilingual source-controlled corridor fields")
            if corridor.get("public_safe") is not True:
                raise ValueError(f"{record_id} is not explicitly public-safe")
            seen_ids.add(cluster_id)
            clusters.append(
                {
                    "id": cluster_id,
                    "context_type": "SOURCE_CONTROLLED_CORRIDOR",
                    "label_en": corridor["label_en"],
                    "label_es": corridor["label_es"],
                    "member_master_ids": member_ids,
                    "why_en": corridor["why_en"],
                    "why_es": corridor["why_es"],
                    "source": {
                        "kind": "SPECIALIST_SOURCE_CONTEXT_CORRIDOR",
                        "path": relative_path,
                        "field": "proceedings_context_corridors[]",
                        "record_id": record_id,
                        "evidence_status": corridor["evidence_status"],
                        "member_provenance": [
                            {
                                "master_id": master_id,
                                "evidence_status": by_id[master_id].get("Source_Status", ""),
                            }
                            for master_id in member_ids
                        ],
                    },
                    "limitations_en": corridor["limitations_en"],
                    "limitations_es": corridor["limitations_es"],
                    "public_safe": True,
                }
            )
    return clusters


def node_dispositions(
    exact_rows: list[dict[str, str]],
    relationships: list[dict[str, Any]],
    context_clusters: list[dict[str, Any]],
    episode_profiles: list[dict[str, Any]] | None = None,
    require_specific_gap_es: bool = True,
    include_finite_tests: bool = True,
) -> list[dict[str, Any]]:
    relationship_ids: dict[str, list[str]] = defaultdict(list)
    for relationship in relationships:
        for master_id in (
            relationship["from_master_id"],
            relationship["to_master_id"],
        ):
            relationship_ids[master_id].append(relationship["id"])

    relationships_by_id = {
        relationship["id"]: relationship for relationship in relationships
    }
    clusters_by_id = {cluster["id"]: cluster for cluster in context_clusters}
    clusters_for_node: dict[str, list[str]] = defaultdict(list)
    for cluster in context_clusters:
        for master_id in cluster["member_master_ids"]:
            clusters_for_node[master_id].append(cluster["id"])

    context_priority = {
        "RECORDED_CONNECTION": 0,
        "SOURCE_CONTROLLED_CORRIDOR": 1,
        "CASE_PRISM_PROPOSITION": 2,
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

        disposition: dict[str, Any] = {
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
        if include_finite_tests:
            disposition["finite_test"] = finite_test_for_row(
                row,
                direct_ids,
                cluster_ids,
                relationships_by_id,
                clusters_by_id,
                episode_profiles or [],
            )
        dispositions.append(disposition)
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
        + source_controlled_context_clusters(exact_rows)
        + prism_context_clusters(exact_ids, prism)
    )
    context_clusters = sorted(
        context_clusters,
        key=lambda item: (
            {
                "RECORDED_CONNECTION": 0,
                "SOURCE_CONTROLLED_CORRIDOR": 1,
                "CASE_PRISM_PROPOSITION": 2,
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
    episode_profiles = fiscalia_response_episode_profiles(public_rows)
    dispositions = node_dispositions(
        exact_rows,
        relationships,
        context_clusters,
        episode_profiles=episode_profiles,
    )
    fiscalia_matrix = fiscalia_office_file_matrix(
        public_rows,
        relationships,
        context_clusters,
        episode_profiles,
    )
    finite_test_count = sum(
        finite_test_is_complete(disposition.get("finite_test", {}))
        for disposition in dispositions
    )
    if finite_test_count != len(exact_rows):
        raise ValueError(
            "every public exact proceeding requires a complete finite test; "
            f"found {finite_test_count} of {len(exact_rows)}"
        )
    finite_test_family_counts = {
        family_id: sum(
            disposition["finite_test"]["family_template_id"] == family_id
            for disposition in dispositions
        )
        for family_id in FINITE_TEST_FAMILY_CATALOG
    }
    finite_test_family_counts = {
        family_id: count
        for family_id, count in finite_test_family_counts.items()
        if count
    }
    if finite_test_family_counts != EXPECTED_FINITE_TEST_FAMILY_COUNTS:
        raise ValueError(
            "finite-test family taxonomy diverges from the controlled record type/class "
            f"denominator: {finite_test_family_counts}"
        )
    for field in (
        "question",
        "decision_dependency",
        "contrary_explanation",
        "if_confirmed",
        "if_refuted",
    ):
        unique_en = {
            disposition["finite_test"][field]["en"] for disposition in dispositions
        }
        unique_es = {
            disposition["finite_test"][field]["es"] for disposition in dispositions
        }
        if len(unique_en) != len(exact_rows) or len(unique_es) != len(exact_rows):
            raise ValueError(
                f"{field} must be file-specific in both languages; "
                f"found {len(unique_en)} EN / {len(unique_es)} ES for {len(exact_rows)} files"
            )
    if len(
        {
            json.dumps(
                disposition["finite_test"]["source_refs"],
                ensure_ascii=False,
                sort_keys=True,
            )
            for disposition in dispositions
        }
    ) != len(exact_rows):
        raise ValueError("finite-test source routes are not exact-file specific")
    mandatory_receipt_axes = {
        "transmission_status",
        "registration_status",
        "file_incorporation_status",
        "recipient_attribution_status",
        "substantive_examination_status",
        "decision_use_status",
    }
    receipt_knowledge_classification_count = sum(
        set(
            disposition.get("finite_test", {})
            .get("receipt_knowledge", {})
            .get("institutional_axes", {})
        )
        == mandatory_receipt_axes
        and bool(
            disposition.get("finite_test", {})
            .get("receipt_knowledge", {})
            .get("cross_file_acknowledgement_status")
        )
        and disposition.get("finite_test", {})
        .get("receipt_knowledge", {})
        .get("actor_specific", {})
        .get("source_status")
        == "NO_ACTOR_SPECIFIC_SOURCE_LOCATED"
        for disposition in dispositions
    )
    if receipt_knowledge_classification_count != len(exact_rows):
        raise ValueError(
            "every public exact proceeding requires the controlled receipt/knowledge model; "
            f"found {receipt_knowledge_classification_count} of {len(exact_rows)}"
        )
    status_vocabulary = set(RECEIPT_KNOWLEDGE_STATUS_CATALOG)
    basis_axes = set(FISCALIA_AXIS_LABELS)
    for disposition in dispositions:
        master_id = disposition["master_id"]
        receipt = disposition["finite_test"]["receipt_knowledge"]
        statuses = {
            **receipt["institutional_axes"],
            "cross_file_acknowledgement_status": receipt[
                "cross_file_acknowledgement_status"
            ],
        }
        if not set(statuses.values()) <= status_vocabulary:
            raise ValueError(f"{master_id} has an uncatalogued institutional status")
        basis = receipt.get("institutional_axis_basis", {})
        if set(basis) != basis_axes:
            raise ValueError(f"{master_id} institutional axis basis is incomplete")
        all_axis_statuses = {
            **statuses,
            "material_received_status": (
                FISCALIA_EPISODE_AXES[
                    next(
                        profile["episode_id"]
                        for profile in episode_profiles
                        if profile["master_id"] == master_id
                    )
                ]["material_received_status"]
                if receipt["source_profile_ids"]
                else "NOT_LOCATED"
            ),
            "referral_status": (
                FISCALIA_EPISODE_AXES[
                    next(
                        profile["episode_id"]
                        for profile in episode_profiles
                        if profile["master_id"] == master_id
                    )
                ]["referral_status"]
                if receipt["source_profile_ids"]
                else "NOT_LOCATED"
            ),
        }
        for axis in basis_axes:
            item = basis[axis]
            if (
                item.get("status") != all_axis_statuses[axis]
                or not item.get("basis_en")
                or not item.get("basis_es")
                or not item.get("limitation_en")
                or not item.get("limitation_es")
                or not item.get("source")
            ):
                raise ValueError(f"{master_id} lacks source-controlled basis for {axis}")
        actor = receipt.get("actor_specific", {})
        if (
            actor.get("receipt_status") != "NOT_ESTABLISHED"
            or actor.get("knowledge_status") != "NOT_ESTABLISHED"
            or actor.get("source_status") != "NO_ACTOR_SPECIFIC_SOURCE_LOCATED"
            or actor.get("actor_ids") != []
        ):
            raise ValueError(
                f"{master_id} institutional evidence was promoted into actor-specific proof"
            )
    receipt_knowledge_positive_source_profile_count = sum(
        bool(
            disposition["finite_test"]["receipt_knowledge"].get(
                "source_profile_ids"
            )
        )
        for disposition in dispositions
    )
    if receipt_knowledge_positive_source_profile_count != len(episode_profiles):
        raise ValueError(
            "each controlled Fiscalía episode must map to one exact finite-test receipt "
            "profile without expanding the positive-source denominator"
        )
    if len(fiscalia_matrix) != EXPECTED_FISCALIA_OFFICE_FILE_RECORDS:
        raise ValueError("Fiscalía office/file matrix denominator is stale")
    fiscalia_matrix_exact_count = sum(
        row.get("is_proceeding") == "TRUE" for row in fiscalia_matrix
    )
    fiscalia_matrix_unverified_count = sum(
        row.get("is_proceeding") == "UNVERIFIED" for row in fiscalia_matrix
    )
    if (fiscalia_matrix_exact_count, fiscalia_matrix_unverified_count) != (
        EXPECTED_FISCALIA_EXACT_RECORDS,
        EXPECTED_FISCALIA_UNVERIFIED_RECORDS,
    ):
        raise ValueError(
            "Fiscalía office/file exact/unresolved split is stale: "
            f"expected {EXPECTED_FISCALIA_EXACT_RECORDS} exact + "
            f"{EXPECTED_FISCALIA_UNVERIFIED_RECORDS} unresolved, found "
            f"{fiscalia_matrix_exact_count} + {fiscalia_matrix_unverified_count}"
        )
    fiscalia_matrix_source_profiled_record_count = sum(
        bool(row.get("source_profile_ids")) for row in fiscalia_matrix
    )
    if fiscalia_matrix_source_profiled_record_count != 8:
        raise ValueError(
            "Fiscalía office/file matrix must contain eight explicitly source-profiled rows; "
            "the ninth controlled episode belongs to a judicial/criminal file"
        )
    expected_direct: dict[str, set[str]] = defaultdict(set)
    for relationship in relationships:
        left = relationship["from_master_id"]
        right = relationship["to_master_id"]
        expected_direct[left].add(right)
        expected_direct[right].add(left)
    expected_context: dict[str, set[str]] = defaultdict(set)
    for cluster in context_clusters:
        members = set(cluster["member_master_ids"])
        for member in members:
            expected_context[member].update(members - {member})
    for row in fiscalia_matrix:
        master_id = row["master_id"]
        if row["related_direct_master_ids"] != sorted(expected_direct[master_id]):
            raise ValueError(f"{master_id} Fiscalía direct-file matrix is incomplete")
        if row["related_context_master_ids"] != sorted(expected_context[master_id]):
            raise ValueError(f"{master_id} Fiscalía contextual-file matrix is incomplete")
        expected_union = sorted(expected_direct[master_id] | expected_context[master_id])
        if row["related_master_ids"] != expected_union:
            raise ValueError(f"{master_id} Fiscalía related-file union is incomplete")
        if row.get("related_assets") != [] or row.get("related_assets_status") != "NOT_LOCATED":
            raise ValueError(f"{master_id} invents a Fiscalía asset inventory")
        if not row.get("related_assets_gap", {}).get("en") or not row.get(
            "related_assets_gap", {}
        ).get("es"):
            raise ValueError(f"{master_id} lacks an explicit related-assets gap")
        if row.get("material_received") != [] or not row.get(
            "material_inventory_gap", {}
        ).get("en") or not row.get("material_inventory_gap", {}).get("es"):
            raise ValueError(f"{master_id} conflates a summary with a received-material inventory")
        evidence_items = row.get("material_allegations_evidence", [])
        expected_evidence_items = 2 if row.get("source_profile_ids") else 0
        if len(evidence_items) != expected_evidence_items:
            raise ValueError(f"{master_id} Fiscalía allegations/evidence summary is incomplete")
        if any(
            not item.get("text_en")
            or not item.get("text_es")
            or not item.get("attribution")
            for item in evidence_items
        ):
            raise ValueError(f"{master_id} has unattributed Fiscalía material summaries")
        for field in (
            "received_or_known",
            "requested",
            "institutional_response",
            "what_was_referred",
            "what_was_actually_examined",
            "strongest_contrary",
            "unanswered_or_source_gap",
        ):
            if not row.get(field, {}).get("en") or not row.get(field, {}).get("es"):
                raise ValueError(f"{master_id} Fiscalía matrix lacks bilingual {field}")
        if set(row.get("institutional_axis_basis", {})) != basis_axes:
            raise ValueError(f"{master_id} Fiscalía matrix lacks per-axis provenance")
        row_statuses = {
            axis: row[axis]
            for axis in basis_axes
        }
        if not set(row_statuses.values()) <= status_vocabulary:
            raise ValueError(f"{master_id} Fiscalía matrix has an uncatalogued status")
        for axis, status in row_statuses.items():
            if row["institutional_axis_basis"][axis].get("status") != status:
                raise ValueError(f"{master_id} Fiscalía {axis} basis/status mismatch")
        expected_referral = (
            "ROUTING_DOCUMENTED" if master_id == "LZ-FIS-007" else "NOT_LOCATED"
        )
        if row["referral_status"] != expected_referral:
            raise ValueError(f"{master_id} referral was inferred from transmission")
    if next(
        row for row in fiscalia_matrix if row["master_id"] == "GC-FIS-013"
    )["referral_status"] == next(
        row for row in fiscalia_matrix if row["master_id"] == "GC-FIS-013"
    )["transmission_status"]:
        raise ValueError("DI 248 referral is still conflated with transmission")
    controlled_trace_route_count = sum(
        bool(
            disposition["finite_test"]["navigation"].get(
                "controlled_trace_route_en"
            )
            and disposition["finite_test"]["navigation"].get(
                "controlled_trace_route_es"
            )
        )
        for disposition in dispositions
    )
    controlled_isolation_route_count = sum(
        bool(
            disposition["finite_test"]["navigation"].get(
                "controlled_isolation_route_en"
            )
            and disposition["finite_test"]["navigation"].get(
                "controlled_isolation_route_es"
            )
        )
        for disposition in dispositions
    )
    if (
        controlled_trace_route_count != len(exact_rows)
        or controlled_isolation_route_count != len(exact_rows)
    ):
        raise ValueError(
            "every public exact proceeding requires bilingual trace and isolation routes"
        )
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
        + source_controlled_context_clusters(canonical_exact_rows)
        + prism_context_clusters(
            [row["Master_ID"] for row in canonical_exact_rows], prism
        )
    )
    canonical_dispositions = node_dispositions(
        canonical_exact_rows,
        canonical_relationships,
        canonical_context_clusters,
        require_specific_gap_es=False,
        include_finite_tests=False,
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
        "schema_version": "1.1.0",
        "control_date": "2026-08-31",
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
            "SOURCE_CONTROLLED_CORRIDOR": {
                "en": "Source-controlled contextual corridor",
                "es": "Corredor contextual controlado por fuente",
            },
        },
        "finite_test_family_catalog": FINITE_TEST_FAMILY_CATALOG,
        "finite_test_contract": {
            "status": "COMPLETE_FOR_PUBLIC_EXACT_DENOMINATOR",
            "family_taxonomy_effect": "UI_ONLY_NO_EDGE_OR_CLUSTER_EFFECT",
            "family_assignment_rule": "CANONICAL_RECORD_TYPE_BEFORE_MIXED_STREAM_SUBSTRING",
            "recorded_candidate_authority_status": "NOT_COMPETENCE_OR_DUTY",
            "required_sequence": [
                "QUESTION",
                "SOURCE_NEEDED",
                "CURRENT_SOURCE_STATUS",
                "COMPETENT_ORGAN",
                "RELATED_PROCEEDINGS",
                "PROCEDURAL_AVAILABILITY",
                "DECISION_DEPENDENCY",
                "STRONGEST_CONTRARY_EXPLANATION",
                "CONSEQUENCE_IF_CONFIRMED",
                "CONSEQUENCE_IF_REFUTED",
            ],
            "boundary_en": (
                "A complete finite-test object makes the next evidential decision inspectable. "
                "It does not upgrade source status, create a relationship, prove availability "
                "in another file or establish wrongdoing."
            ),
            "boundary_es": (
                "Un objeto de prueba finita completo hace examinable la siguiente decisión "
                "probatoria. No eleva el estado de la fuente, crea una relación, acredita "
                "disponibilidad en otro expediente ni establece ilicitud."
            ),
        },
        "receipt_knowledge_status_catalog": RECEIPT_KNOWLEDGE_STATUS_CATALOG,
        "receipt_knowledge_contract": {
            "institutional_axis_ids": [
                "transmission_status",
                "registration_status",
                "file_incorporation_status",
                "recipient_attribution_status",
                "substantive_examination_status",
                "decision_use_status",
            ],
            "public_renderer_axis_ids": [
                "transmission_status",
                "material_received_status",
                "referral_status",
                "registration_status",
                "file_incorporation_status",
                "recipient_attribution_status",
                "substantive_examination_status",
                "decision_use_status",
                "cross_file_acknowledgement_status",
            ],
            "public_renderer_axis_provenance_requirement": (
                "FAIL_CLOSED_STATUS_BILINGUAL_BASIS_LIMITATION_AND_SOURCE"
            ),
            "public_renderer_axis_status_locations": {
                "transmission_status": "receipt_knowledge.institutional_axes",
                "material_received_status": "receipt_knowledge.institutional_axis_basis.status",
                "referral_status": "receipt_knowledge.institutional_axis_basis.status",
                "registration_status": "receipt_knowledge.institutional_axes",
                "file_incorporation_status": "receipt_knowledge.institutional_axes",
                "recipient_attribution_status": "receipt_knowledge.institutional_axes",
                "substantive_examination_status": "receipt_knowledge.institutional_axes",
                "decision_use_status": "receipt_knowledge.institutional_axes",
                "cross_file_acknowledgement_status": "receipt_knowledge.root",
            },
            "cross_file_acknowledgement_is_separate": True,
            "institutional_axis_basis_required": True,
            "positive_axis_source_field_rule": "EXACT_EPISODE_FIELD_MUST_SUPPORT_AXIS_GRADE",
            "institutional_axis_basis_fields": [
                "status",
                "basis_kind",
                "basis_en",
                "basis_es",
                "limitation_en",
                "limitation_es",
                "source",
            ],
            "actor_specific_status_is_separate": True,
            "positive_source_membership_rule": (
                "EXPLICIT_REVIEWED_FISCALIA_EPISODE_TO_MASTER_ID_ONLY"
            ),
            "raw_matter_reference_join": "PROHIBITED",
            "boundary_en": (
                "Institutional transmission, material received, referral, registration, "
                "incorporation, recipient attribution, examination, decision-use and cross-file "
                "acknowledgement are independent grades. No institutional grade establishes "
                "personal receipt or knowledge."
            ),
            "boundary_es": (
                "La transmisión, el material recibido, la remisión, el registro, la incorporación, "
                "la atribución al destinatario, el examen, el uso decisorio y el reconocimiento "
                "entre expedientes son grados institucionales independientes. Ningún grado "
                "institucional acredita recepción ni conocimiento personal."
            ),
        },
        "fiscalia_office_file_matrix_contract": {
            "row_denominator": EXPECTED_FISCALIA_OFFICE_FILE_RECORDS,
            "required_independent_status_axes": list(FISCALIA_AXIS_LABELS),
            "required_substantive_columns": [
                "date_or_period",
                "received_or_known",
                "material_allegations_evidence",
                "material_received",
                "material_inventory_gap",
                "related_direct_master_ids",
                "related_context_master_ids",
                "related_assets",
                "what_was_referred",
                "what_was_actually_examined",
                "institutional_response",
                "cross_file_acknowledgement_status",
                "unitary_acknowledgement_status",
                "strongest_contrary",
                "unanswered_or_source_gap",
            ],
            "referral_is_not_transmission": True,
            "direct_context_and_assets_are_separate": True,
            "material_summary_is_not_received_inventory": True,
            "axis_provenance_required": True,
        },
        "fiscalia_response_episode_profiles": episode_profiles,
        "fiscalia_office_file_matrix": fiscalia_matrix,
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
            "source_controlled_corridor_count": sum(
                cluster["context_type"] == "SOURCE_CONTROLLED_CORRIDOR"
                for cluster in context_clusters
            ),
            "case_prism_exact_proceeding_covered_count": len(case_prism_exact_ids),
            "case_prism_exact_proceeding_uncovered_count": len(exact_rows)
            - len(case_prism_exact_ids),
            "decision_dependency_exact_coverage": (
                f"VERIFIED_{finite_test_count}_OF_{len(exact_rows)}"
            ),
            "decision_dependency_exact_coverage_scope": (
                "PUBLIC_EXACT_FILE_FINITE_TEST_REGISTER"
            ),
            "shared_case_prism_proposition_membership_coverage": (
                f"GAP_{len(case_prism_exact_ids)}_OF_{len(exact_rows)}"
            ),
            "shared_case_prism_proposition_membership_scope": (
                "SHARED_CASE_PRISM_PROPOSITION_MEMBERSHIP_ONLY"
            ),
            "exact_file_decision_dependency_actionability_count": finite_test_count,
            "exact_file_decision_dependency_actionability_coverage": (
                f"VERIFIED_{finite_test_count}_OF_{len(exact_rows)}"
            ),
            "bilingual_specific_next_source_count": bilingual_specific_next_source_count,
            "bilingual_specific_next_source_coverage": (
                f"VERIFIED_{bilingual_specific_next_source_count}_OF_{len(exact_rows)}"
            ),
            "exact_proceeding_full_finite_test_count": finite_test_count,
            "exact_proceeding_full_finite_test_coverage": (
                f"VERIFIED_{finite_test_count}_OF_{len(exact_rows)}"
            ),
            "finite_test_family_counts": finite_test_family_counts,
            "receipt_knowledge_classification_count": receipt_knowledge_classification_count,
            "receipt_knowledge_classification_coverage": (
                f"VERIFIED_{receipt_knowledge_classification_count}_OF_{len(exact_rows)}"
            ),
            "receipt_knowledge_axis_provenance_count": receipt_knowledge_classification_count,
            "receipt_knowledge_axis_provenance_coverage": (
                f"VERIFIED_{receipt_knowledge_classification_count}_OF_{len(exact_rows)}"
            ),
            "receipt_knowledge_positive_source_profile_count": (
                receipt_knowledge_positive_source_profile_count
            ),
            "fiscalia_office_file_matrix_count": len(fiscalia_matrix),
            "fiscalia_office_file_matrix_coverage": (
                f"VERIFIED_{len(fiscalia_matrix)}_OF_{EXPECTED_FISCALIA_OFFICE_FILE_RECORDS}"
            ),
            "fiscalia_office_file_matrix_substantive_column_count": len(fiscalia_matrix),
            "fiscalia_office_file_matrix_substantive_column_coverage": (
                f"VERIFIED_{len(fiscalia_matrix)}_OF_{EXPECTED_FISCALIA_OFFICE_FILE_RECORDS}"
            ),
            "fiscalia_office_file_matrix_exact_count": fiscalia_matrix_exact_count,
            "fiscalia_office_file_matrix_unverified_count": (
                fiscalia_matrix_unverified_count
            ),
            "fiscalia_response_episode_profile_count": len(episode_profiles),
            "fiscalia_office_file_matrix_source_profiled_record_count": (
                fiscalia_matrix_source_profiled_record_count
            ),
            "controlled_trace_route_count": controlled_trace_route_count,
            "controlled_isolation_route_count": controlled_isolation_route_count,
            "controlled_navigation_coverage": (
                f"VERIFIED_{min(controlled_trace_route_count, controlled_isolation_route_count)}_OF_{len(exact_rows)}"
            ),
            "dedicated_narrative_dossier_coverage": "PARTIAL_NOT_INFERRED",
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

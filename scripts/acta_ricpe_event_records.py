#!/usr/bin/env python3
"""Add the two controlled RICPE meeting families found in the final Drive audit.

The 29 December 2021 family is a later recital with its primary records still
unlocated.  The March 2022 family is controlled by a five-page notice/agenda;
the notice is not minutes and does not prove that the meeting occurred or
adopted any resolution.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from acta_capacity_sequence_annotations import EVENT_IDS, annotation_for_event


REPO = Path(__file__).resolve().parents[1]
DEFAULT_CONTINUITY = REPO / "evidence/community/actas/event-family-continuity-v1.json"


def bi(es: str, en: str) -> dict[str, str]:
    return {"es": es, "en": en}


RICPE_RECITAL_ID = "SP-RECITAL-2021-12-29-RICPE"
RICPE_NOTICE_EVENT_ID = "SP-MEETING-2022-03-11-RICPE"
RICPE_MISSING_SOURCE_ID = "SP-SRC-RICPE-2021-12-29-PRIMARY-UNLOCATED"
RICPE_NOTICE_SOURCE_ID = "SP-SRC-NOTICE-RICPE-2022-02-11-5P"
SOURCE_REGISTER_SOURCE_ROW_COUNT = 45


EVENT_FAMILIES = {
    RICPE_RECITAL_ID: {
        "stable_id": RICPE_RECITAL_ID,
        "legacy_id_aliases": [],
        "documented_date_or_range": "2021-12-29",
        "document_type": bi(
            "mención posterior de junta societaria; fuente primaria no localizada",
            "later recital of corporate meeting; primary source unlocated",
        ),
        "issuer_sender": bi(
            "Fuente posterior que menciona una junta de accionistas de RICPE; emisor primario no localizado",
            "Later source reciting a RICPE shareholders' meeting; primary issuer unlocated",
        ),
        "stated_capacity": bi(
            "mención posterior; no convocante, secretario ni órgano primario probado",
            "later recital; not a proved primary convener, secretary or organ record",
        ),
        "recipients": bi(
            "destinatarios de la fuente posterior; destinatarios primarios no localizados",
            "later-source recipients; primary recipients unlocated",
        ),
        "meeting_body_if_any": bi(
            "Junta de accionistas de RIC Private Equity Investment Partners S.C.R., S.A. (RICPE), según mención posterior",
            "RIC Private Equity Investment Partners S.C.R., S.A. (RICPE) shareholders' meeting, according to a later recital",
        ),
        "documented_convener": bi(
            "no localizado/no resuelto; la mención posterior no prueba convocante",
            "not located/unresolved; the later recital does not prove a convener",
        ),
        "perimeter": "unresolved",
        "perimeter_code": "D-OPEN",
        "source_provenance_status": bi(
            "mención posterior localizada; convocatoria, ACTA, lista, votos y acuerdo primarios no localizados",
            "later recital located; primary notice, minutes, list, votes and resolution unlocated",
        ),
        "public_private_status": bi(
            "página bilingüe de carencia; fuentes primarias no localizadas",
            "public bilingual gap page; primary sources unlocated",
        ),
        "relationship_to_other_documents_or_events": [
            "SP-RECITAL-2018-11-20",
            "SP-ACTA-2022-02-04",
            RICPE_NOTICE_EVENT_ID,
        ],
        "unresolved_evidential_issues": [bi(
            "Siguen abiertos ocurrencia, convocatoria, orden del día, accionistas, poderes, asistencia, cuórum, votos, texto del acuerdo de capital, ACTA, circulación, ejecución, autenticidad y validez.",
            "Occurrence, notice, agenda, shareholders, proxies, attendance, quorum, votes, capital-resolution wording, minutes, circulation, implementation, authenticity and validity remain open.",
        )],
        "bilingual_event_routes": {
            "es": "es/comunidad-instrumentalizacion/sala-documental-actas/2021-12-29-ricpe-recital/index.html",
            "en": "en/community-instrumentalisation/acta-document-room/2021-12-29-ricpe-recital/index.html",
        },
        "no_page_reason": None,
        "document_record_ids": [RICPE_MISSING_SOURCE_ID],
        "continuity_audit": {
            "before": bi(
                "La mención no aporta la cadena previa de propuesta, convocatoria o comunicaciones societarias.",
                "The recital does not supply the preceding proposal, notice or corporate-communications chain.",
            ),
            "knowledge": bi(
                "El documento posterior recibido contiene la mención; no establece por sí solo quién lo redactó o recibió ni qué sabía persona alguna.",
                "The received later document contains the recital; it does not independently establish who authored or received it, or what any person knew.",
            ),
            "notice_service": bi(
                "No se han localizado convocatoria, orden del día, lista de envío ni prueba de servicio.",
                "No notice, agenda, distribution list or service proof has been located.",
            ),
            "omitted_excluded_allegation": bi(
                "Sin denominador de accionistas, destinatarios y poderes no puede evaluarse omisión o exclusión.",
                "Omission or exclusion cannot be assessed without the shareholder, recipient and proxy denominator.",
            ),
            "convener": bi(
                "No resuelto; una mención posterior no prueba quién convocó ni su autoridad.",
                "Unresolved; a later recital does not prove who convened the meeting or their authority.",
            ),
            "body": bi(
                "Junta de accionistas RICPE según mención; entidad societaria distinta de Comunidad de Propietarios y CAM.",
                "RICPE shareholders' meeting according to the recital; a corporate entity distinct from the Owners' Community and CAM.",
            ),
            "attendance_representation": bi(
                "No se han localizado asistencia, representaciones, poderes o participaciones.",
                "No attendance, representation, proxy or shareholding record has been located.",
            ),
            "resolutions_proposed_voted": bi(
                "La fuente posterior menciona un acuerdo de capital; no se han localizado propuesta, texto, mayoría, voto ni adopción primarios.",
                "The later source recites a capital resolution; no primary proposal, wording, majority, vote or adoption record has been located.",
            ),
            "objections": bi(
                "No se han localizado objeciones o reservas contemporáneas.",
                "No contemporaneous objection or reservation has been located.",
            ),
            "minutes_versions": bi(
                "No se ha localizado ACTA, certificado ni versión competidora; la mención no se convierte en ACTA.",
                "No minutes, certificate or competing version has been located; the recital is not converted into minutes.",
            ),
            "circulation_receipt_withholding": bi(
                "No se ha localizado circulación, recepción o retención de registros primarios.",
                "No circulation, receipt or withholding chain for primary records has been located.",
            ),
            "implementation": bi(
                "No se atribuye una operación, asiento, pago o ejecución a esta junta sin documentos primarios separados.",
                "No transaction, filing, payment or implementation is attributed to this meeting without separate primary documents.",
            ),
            "later_reliance": bi(
                "La reunión y el acuerdo aparecen sólo como mención posterior en el corpus controlado.",
                "The meeting and resolution appear only as a later recital in the controlled corpus.",
            ),
            "contradictions": bi(
                "No hay fuente primaria para comparar fecha, órgano, participantes, texto o resultado; la ausencia no prueba inexistencia.",
                "No primary source is available to compare date, organ, participants, wording or outcome; absence does not prove nonexistence.",
            ),
            "unproved": bi(
                "Siguen abiertos ocurrencia, convocatoria, orden del día, accionistas, poderes, asistencia, cuórum, votos, texto del acuerdo de capital, ACTA, circulación, ejecución, autenticidad y validez.",
                "Occurrence, notice, agenda, shareholders, proxies, attendance, quorum, votes, capital-resolution wording, minutes, circulation, implementation, authenticity and validity remain open.",
            ),
        },
    },
    RICPE_NOTICE_EVENT_ID: {
        "stable_id": RICPE_NOTICE_EVENT_ID,
        "legacy_id_aliases": [],
        "documented_date_or_range": "2022-03-11–2022-03-12",
        "document_type": bi(
            "junta societaria extraordinaria convocada; ocurrencia no probada",
            "scheduled extraordinary corporate meeting; occurrence unproved",
        ),
        "issuer_sender": bi(
            "Consejo de administración de RICPE mediante su secretario, según convocatoria de 11-Feb-2022",
            "RICPE board through its secretary, according to the 11-Feb-2022 notice",
        ),
        "stated_capacity": bi(
            "secretario del consejo emisor; la capacidad consta en la convocatoria y no prueba por sí sola autoridad o servicio correcto",
            "secretary of the issuing board; the notice records the capacity but does not itself prove authority or proper service",
        ),
        "recipients": bi(
            "accionistas de RICPE según convocatoria; lista completa de servicio/recepción no localizada",
            "RICPE shareholders according to the notice; complete service/receipt list unlocated",
        ),
        "meeting_body_if_any": bi(
            "Junta general extraordinaria de accionistas de RIC Private Equity Investment Partners S.C.R., S.A. (RICPE)",
            "Extraordinary general shareholders' meeting of RIC Private Equity Investment Partners S.C.R., S.A. (RICPE)",
        ),
        "documented_convener": bi(
            "Consejo de administración de RICPE, por medio de su secretario, según la convocatoria; autoridad, servicio y celebración no adjudicados",
            "RICPE board, through its secretary, according to the notice; authority, service and occurrence not adjudicated",
        ),
        "perimeter": "mixed_or_contested",
        "perimeter_code": "D-MIXED",
        "source_provenance_status": bi(
            "convocatoria/orden del día de cinco páginas localizada y controlada; no se localizó ACTA o resultado",
            "five-page notice/agenda located and controlled; no minutes or outcome located",
        ),
        "public_private_status": bi(
            "nativo privado; metadatos públicos seguros y derivados públicos sujetos al control del paquete",
            "private native; public-safe metadata and any public derivatives remain under package control",
        ),
        "relationship_to_other_documents_or_events": [
            RICPE_RECITAL_ID,
            "SP-ACTA-2022-02-04",
        ],
        "unresolved_evidential_issues": [bi(
            "Siguen abiertos servicio completo, autoridad, celebración en primera o segunda convocatoria, asistentes, poderes, cuórum, votos, acuerdos, ACTA, variantes, circulación, ejecución y validez.",
            "Complete service, authority, occurrence at first or second call, attendees, proxies, quorum, votes, resolutions, minutes, variants, circulation, implementation and validity remain open.",
        )],
        "bilingual_event_routes": {
            "es": "es/comunidad-instrumentalizacion/sala-documental-actas/2022-03-11-ricpe/index.html",
            "en": "en/community-instrumentalisation/acta-document-room/2022-03-11-ricpe/index.html",
        },
        "no_page_reason": None,
        "document_record_ids": [RICPE_NOTICE_SOURCE_ID],
        "continuity_audit": {
            "before": bi(
                "El documento recibido de cinco páginas está fechado el 11-Feb-2022 y atribuye la convocatoria propuesta al consejo de RICPE por medio de su secretario; la mención de 29-Dec-2021 se conserva como evento separado y no prueba esta junta.",
                "The received five-page document is dated 11-Feb-2022 and attributes the proposed call to the RICPE board through its secretary; the 29-Dec-2021 recital remains a separate event and does not prove this meeting.",
            ),
            "knowledge": bi(
                "El documento atribuye la convocatoria al consejo/secretaría en la capacidad declarada; autoría, emisión efectiva, servicio y conocimiento de cada destinatario siguen abiertos.",
                "The document attributes the call to the board/secretary in the stated capacity; actual authorship, issuance, service and each recipient's knowledge remain open.",
            ),
            "notice_service": bi(
                "Se localizó la convocatoria/orden del día de cinco páginas; faltan lista completa, canal, entrega y acuses.",
                "The five-page notice/agenda is located; the complete list, channel, delivery and acknowledgements are not.",
            ),
            "omitted_excluded_allegation": bi(
                "Sin denominador completo de accionistas, direcciones, poderes y servicio no puede determinarse omisión o exclusión.",
                "Omission or exclusion cannot be determined without the complete shareholder, address, proxy and service denominator.",
            ),
            "convener": bi(
                "La convocatoria identifica al consejo de RICPE y al secretario emisor; ello no adjudica autoridad o regularidad.",
                "The notice identifies the RICPE board and issuing secretary; that does not adjudicate authority or regularity.",
            ),
            "body": bi(
                "Junta societaria RICPE, distinta de la Comunidad de Propietarios, CAM y sus órganos/personas.",
                "RICPE corporate shareholders' meeting, distinct from the Owners' Community, CAM and their organs/persons.",
            ),
            "attendance_representation": bi(
                "No se han localizado lista de asistentes, poderes, participaciones o representaciones de la reunión.",
                "No attendee list, proxies, shareholdings or meeting representations have been located.",
            ),
            "resolutions_proposed_voted": bi(
                "La convocatoria acredita puntos propuestos, no que fueran tratados, votados o aprobados; texto y resultado permanecen abiertos.",
                "The notice establishes proposed agenda items, not that they were addressed, voted or approved; wording and outcome remain open.",
            ),
            "objections": bi(
                "No se han localizado objeciones o reservas contemporáneas.",
                "No contemporaneous objections or reservations have been located.",
            ),
            "minutes_versions": bi(
                "No se ha localizado ACTA, certificado, audio, transcripción o versión competidora; la convocatoria no se clasifica como ACTA.",
                "No minutes, certificate, audio, transcript or competing version has been located; the notice is not classified as minutes.",
            ),
            "circulation_receipt_withholding": bi(
                "La fuente prueba una copia de convocatoria, no su entrega completa ni la circulación/retención de un ACTA posterior.",
                "The source proves a notice copy, not complete delivery or circulation/withholding of later minutes.",
            ),
            "implementation": bi(
                "No se ha conectado una actuación, asiento, pago o decisión posterior a un acuerdo probado de esta reunión.",
                "No later act, filing, payment or decision has been connected to a proved resolution of this meeting.",
            ),
            "later_reliance": bi(
                "No se ha localizado uso posterior que pruebe celebración o resultado; uso eventual deberá separarse de la mera convocatoria.",
                "No later reliance proving occurrence or outcome has been located; any later use must be separated from the notice alone.",
            ),
            "contradictions": bi(
                "La junta comunitaria de 4-Feb-2022 es un órgano distinto y no prueba convocante, cuórum, voto o resultado de RICPE.",
                "The 4-Feb-2022 Community meeting is a distinct organ and does not prove RICPE convener, quorum, voting or outcome.",
            ),
            "unproved": bi(
                "Siguen abiertos servicio completo, autoridad, celebración en primera o segunda convocatoria, asistentes, poderes, cuórum, votos, acuerdos, ACTA, variantes, circulación, ejecución y validez.",
                "Complete service, authority, occurrence at first or second call, attendees, proxies, quorum, votes, resolutions, minutes, variants, circulation, implementation and validity remain open.",
            ),
        },
    },
}


DOCUMENTS = {
    RICPE_MISSING_SOURCE_ID: {
        "stable_id": RICPE_MISSING_SOURCE_ID,
        "legacy_id_aliases": [],
        "register_source_ids": [],
        "event_family_ids": [RICPE_RECITAL_ID],
        "documented_date_or_range": "2021-12-29",
        "document_type": bi(
            "registro de carencia de convocatoria/ACTA/acuerdo societario primario",
            "gap record for primary corporate notice/minutes/resolution",
        ),
        "relationship_stage": "meeting_record",
        "record_class": "explicit-missing-source-continuity-record",
        "issuer_sender": bi(
            "no localizado; una fuente posterior menciona una junta RICPE",
            "unlocated; a later source recites a RICPE meeting",
        ),
        "stated_capacity": bi(
            "registro de carencia del repositorio; no emisor histórico ni ACTA",
            "repository gap record; not a historical issuer or minutes",
        ),
        "recipients": bi(
            "destinatarios primarios no localizados",
            "primary recipients unlocated",
        ),
        "meeting_body_if_any": bi(
            "Junta de accionistas RICPE según mención posterior; ocurrencia no establecida",
            "RICPE shareholders' meeting according to a later recital; occurrence not established",
        ),
        "documented_convener": bi(
            "no localizado/no resuelto",
            "not located/unresolved",
        ),
        "perimeter": "unresolved",
        "perimeter_code": "D-OPEN",
        "source_provenance_status": bi(
            "fuentes primarias no localizadas en el universo finito buscado; mención posterior conservada",
            "primary sources not located in the finite searched universe; later recital preserved",
        ),
        "public_private_status": bi(
            "metadatos públicos de carencia; no existe binario primario localizado para publicar",
            "public gap metadata; no located primary binary exists to publish",
        ),
        "source_custody": {
            "public_safe_label": RICPE_MISSING_SOURCE_ID,
            "source_location_class": "unlocated in finite searched universe",
            "acquisition_path_class": "negative connected-repository/Drive/email review; absence is not nonexistence",
            "private_locator_published": False,
        },
        "integrity": {
            "size_bytes": None,
            "page_count": None,
            "sha256": None,
            "hash_status": "not applicable until a source copy is located",
            "conflicts": [
                "A later recital does not prove meeting occurrence, notice, attendance, vote, resolution wording or validity."
            ],
        },
        "variant_role": bi(
            "registro explícito de fuente primaria no localizada; no es ACTA",
            "explicit unlocated-primary-source record; not minutes",
        ),
        "relationship_to_other_documents_or_event": {
            "event_family_ids": [RICPE_RECITAL_ID],
            "related_document_ids": [RICPE_NOTICE_SOURCE_ID],
        },
        "unresolved_evidential_issues": [bi(
            "No se han localizado convocatoria, orden del día, ACTA, lista, poderes, votos, acuerdo, anexos, certificado, circulación o integridad primaria; ausencia no es inexistencia.",
            "No primary notice, agenda, minutes, list, proxies, votes, resolution, annexes, certificate, circulation or integrity record has been located; absence is not nonexistence.",
        )],
        "bilingual_event_routes": EVENT_FAMILIES[RICPE_RECITAL_ID]["bilingual_event_routes"],
        "no_page_reason": bi(
            "La entrada estable es esta página bilingüe de carencia; no puede producirse una página fuente completa sin inventar un documento no localizado.",
            "The stable entry is this bilingual gap page; no complete source page can be produced without inventing an unlocated document.",
        ),
    },
    RICPE_NOTICE_SOURCE_ID: {
        "stable_id": RICPE_NOTICE_SOURCE_ID,
        "legacy_id_aliases": [],
        "register_source_ids": [],
        "event_family_ids": [RICPE_NOTICE_EVENT_ID],
        "documented_date_or_range": "2022-02-11; meeting scheduled 2022-03-11–2022-03-12",
        "document_type": bi(
            "convocatoria y orden del día de cinco páginas; no ACTA",
            "five-page meeting notice and agenda; not minutes",
        ),
        "relationship_stage": "pre_meeting",
        "record_class": "concrete-source-copy-or-source-record",
        "issuer_sender": bi(
            "Consejo de administración de RICPE mediante su secretario, según la fuente",
            "RICPE board through its secretary, according to the source",
        ),
        "stated_capacity": bi(
            "secretario del consejo emisor; capacidad declarada en la convocatoria",
            "secretary of the issuing board; capacity stated in the notice",
        ),
        "recipients": bi(
            "accionistas de RICPE según convocatoria; lista completa de entrega/recepción no localizada",
            "RICPE shareholders according to the notice; complete delivery/receipt list unlocated",
        ),
        "meeting_body_if_any": bi(
            "Junta general extraordinaria de accionistas RICPE prevista el 11/12-Mar-2022",
            "RICPE extraordinary general shareholders' meeting scheduled for 11/12-Mar-2022",
        ),
        "documented_convener": bi(
            "Consejo de administración de RICPE, por medio de su secretario, según la convocatoria",
            "RICPE board, through its secretary, according to the notice",
        ),
        "perimeter": "mixed_or_contested",
        "perimeter_code": "D-MIXED",
        "source_provenance_status": bi(
            "fuente de cinco páginas localizada en Drive/custodia privada y controlada por tamaño, páginas y SHA-256",
            "five-page source located in Drive/private custody and controlled by size, pages and SHA-256",
        ),
        "public_private_status": bi(
            "fuente nativa privada; metadatos públicos seguros y derivados públicos sujetos al manifiesto del paquete",
            "private native source; public-safe metadata and public derivatives governed by the package manifest",
        ),
        "source_custody": {
            "public_safe_label": bi(
                "Convocatoria RICPE de 11-Feb-2022 · cinco páginas",
                "11-Feb-2022 RICPE notice · five pages",
            ),
            "source_location_class": bi(
                "Drive/custodia privada controlada; localizador exacto omitido",
                "Drive/controlled private custody; exact locator omitted",
            ),
            "acquisition_path_class": bi(
                "recuperación conectada de Drive y entrada privada controlada",
                "connected Drive recovery and controlled private ingest",
            ),
            "private_locator_published": False,
            "source_literal_filename": None,
        },
        "integrity": {
            "size_bytes": 191251,
            "page_count": 5,
            "sha256": "3858b928d4eee8a4f5e9b21f5452c9e58cbbfbd22debccb38bfe3dd07db303c4",
            "hash_status": bi(
                "tamaño, cinco páginas y SHA-256 controlados para la copia localizada",
                "size, five pages and SHA-256 controlled for the located copy",
            ),
            "authenticity_status": bi(
                "integridad de copia controlada; autenticidad, autoridad, servicio y resultado de la reunión abiertos",
                "copy integrity controlled; authenticity, authority, service and meeting outcome open",
            ),
        },
        "variant_role": bi(
            "copia de control localizada de convocatoria/orden del día; no ACTA ni prueba de resultado",
            "located notice/agenda control copy; not minutes or proof of outcome",
        ),
        "relationship_to_other_documents_or_event": {
            "event_family_ids": [RICPE_NOTICE_EVENT_ID],
            "related_document_ids": [RICPE_MISSING_SOURCE_ID, "SP-ACTA-2022-02-04"],
        },
        "unresolved_evidential_issues": [bi(
            "Siguen abiertos original/autenticidad, lista y servicio completos, celebración, asistentes, poderes, cuórum, votos, acuerdos, ACTA, variantes, circulación, ejecución y validez; la convocatoria no es ACTA.",
            "Original/authenticity, complete list and service, occurrence, attendees, proxies, quorum, votes, resolutions, minutes, variants, circulation, implementation and validity remain open; the notice is not minutes.",
        )],
        "bilingual_event_routes": EVENT_FAMILIES[RICPE_NOTICE_EVENT_ID]["bilingual_event_routes"],
        "no_page_reason": bi(
            "La entrada bilingüe estable de la fuente es su ancla en la familia del evento; evita una ruta autónoma duplicada y mantiene separada la convocatoria del ACTA no localizada.",
            "The source's stable bilingual entry is its event-family anchor; it avoids a duplicate standalone route and keeps the notice separate from the unlocated minutes.",
        ),
    },
}


def apply_records(payload: dict) -> dict:
    result = copy.deepcopy(payload)
    families_by_id = {
        family["stable_id"]: family for family in result.get("event_families", [])
    }
    documents_by_id = {
        document["stable_id"]: document for document in result.get("documents", [])
    }

    for event_id, controlled in EVENT_FAMILIES.items():
        existing = families_by_id.get(event_id, {})
        for field, expected in controlled.items():
            if field in existing and existing[field] != expected:
                raise ValueError(
                    f"Refusing to overwrite {event_id} controlled field {field}"
                )
        family = copy.deepcopy(existing)
        family.update(copy.deepcopy(controlled))
        family.update(annotation_for_event(event_id))
        families_by_id[event_id] = family
    for source_id, controlled in DOCUMENTS.items():
        existing = documents_by_id.get(source_id, {})
        for field, expected in controlled.items():
            if field in existing and existing[field] != expected:
                raise ValueError(
                    f"Refusing to overwrite {source_id} controlled field {field}"
                )
        merged = copy.deepcopy(existing)
        merged.update(copy.deepcopy(controlled))
        documents_by_id[source_id] = merged

    # Preserve reciprocal event-family navigation without altering other fields.
    reciprocal = {
        "SP-RECITAL-2018-11-20": [RICPE_RECITAL_ID],
        "SP-ACTA-2022-02-04": [RICPE_RECITAL_ID, RICPE_NOTICE_EVENT_ID],
    }
    for event_id, additions in reciprocal.items():
        related = families_by_id[event_id]["relationship_to_other_documents_or_events"]
        for addition in additions:
            if addition not in related:
                related.append(addition)

    result["event_families"] = [families_by_id[event_id] for event_id in EVENT_IDS]
    result["documents"] = list(documents_by_id.values())
    result["controlled_event_family_count"] = len(result["event_families"])
    result["document_record_count"] = len(result["documents"])
    result["scope"] = (
        "Twenty-three controlled Sun Park ACTA/meeting/event families, including separate "
        "Community, CEXP, professional and RICPE corporate records. The 29-Dec-2021 RICPE "
        "family remains later-recital-only; the located 11-Feb-2022 five-page RICPE notice "
        "is not minutes and does not prove occurrence or outcome."
    )

    source_documents = [
        document for document in result["documents"]
        if document["stable_id"].startswith("SP-SRC-")
    ]
    missing_sources = [
        document for document in source_documents
        if document.get("record_class") == "explicit-missing-source-continuity-record"
    ]
    concrete_sources = [
        document for document in source_documents
        if document.get("record_class") != "explicit-missing-source-continuity-record"
    ]
    result["concrete_source_record_count"] = len(concrete_sources)
    result["concrete_source_record_coverage_count"] = len(concrete_sources)
    result["missing_source_continuity_record_count"] = len(missing_sources)
    result["missing_source_continuity_record_coverage_count"] = len(missing_sources)
    result["newly_located_event_record_count"] = 3
    result["newly_located_source_record_count"] = 7
    coverage = result.setdefault("coverage", {})
    coverage["controlled_event_families"] = {
        "denominator": len(result["event_families"]),
        "covered": len(result["event_families"]),
    }
    coverage["concrete_source_copy_or_source_records"] = {
        "denominator": len(concrete_sources),
        "covered": len(concrete_sources),
    }
    coverage["explicit_missing_source_continuity_records"] = {
        "denominator": len(missing_sources),
        "covered": len(missing_sources),
    }
    coverage["newly_located_post_register_event_records"] = {
        "denominator": 3,
        "covered": 3,
    }
    coverage["newly_located_post_register_source_records"] = {
        "denominator": 7,
        "covered": 7,
    }
    # The two RICPE rows are also separate entries in section 4 of the public
    # source register: one explicit gap record and one located notice source.
    result["source_register_source_row_count"] = SOURCE_REGISTER_SOURCE_ROW_COUNT
    result["source_register_source_row_coverage_count"] = SOURCE_REGISTER_SOURCE_ROW_COUNT
    coverage["canonical_source_table_rows"] = {
        "denominator": SOURCE_REGISTER_SOURCE_ROW_COUNT,
        "covered": SOURCE_REGISTER_SOURCE_ROW_COUNT,
    }
    c1 = result["perimeters"]["adverse_montelanza_molina"]
    c1["label"] = "Alleged adverse perimeter: AAS → FMMM/Cogolludo/Pamanil"
    c1["boundary"] = (
        "Gil Marer's attributed sequence AAS → FMMM/Cogolludo/Pamanil and the project's "
        "documentary classification. Every actor, office and act remains separate; this is not "
        "an adjudicated finding of common control, conspiracy, fraud, criminal purpose or guilt."
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--continuity", type=Path, default=DEFAULT_CONTINUITY)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = args.continuity.resolve()
    original = json.loads(path.read_text(encoding="utf-8"))
    updated = apply_records(original)
    if args.check:
        if original != updated:
            raise SystemExit("RICPE continuity records differ from deterministic control")
        print("RICPE continuity records verified")
        return
    path.write_text(
        json.dumps(updated, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Controlled {len(updated['event_families'])} event families and "
        f"{len(updated['documents'])} document records"
    )


if __name__ == "__main__":
    main()

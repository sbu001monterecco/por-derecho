#!/usr/bin/env python3
"""Deterministic LPH lifecycle controls for Sun Park Community meetings.

This module does not decide legal validity.  It separates the evidence needed
to test each historical meeting under the Ley de Propiedad Horizontal (LPH)
version applicable on the meeting date.  Stable IDs are repository references;
an ID marked unlocated/reference-only is not a claim that a source exists.
"""

from __future__ import annotations


LPH_GATES = {
    "G1": {
        "label_es": "Autoridad y convocatoria",
        "label_en": "Authority and call",
        "articles": "LPH arts. 13, 16",
        "question_es": "¿Quién tenía capacidad para convocar y cuál fue el orden del día?",
        "question_en": "Who had authority to call the meeting and what was the agenda?",
    },
    "G2": {
        "label_es": "Aviso, destinatarios y servicio",
        "label_en": "Notice, recipients and service",
        "articles": "LPH arts. 9.1.h, 16",
        "question_es": "¿Se notificó a cada propietario en el domicilio/control aplicable y puede probarse la entrega o el intento?",
        "question_en": "Was every owner notified at the applicable address/control point, and can delivery or attempted delivery be proved?",
    },
    "G3": {
        "label_es": "Asistencia, deuda, voto y mayoría",
        "label_en": "Attendance, debt, vote and majority",
        "articles": "LPH arts. 15, 17, 21",
        "question_es": "¿Están cerrados propietarios, poderes, cuotas, deuda, privación de voto, conflicto, votos y mayoría por punto?",
        "question_en": "Are owners, proxies, coefficients, debt, voting exclusion, conflicts, votes and the item-by-item majority closed?",
    },
    "G4": {
        "label_es": "ACTA, cierre, firma y libro",
        "label_en": "Minutes, closure, signature and book",
        "articles": "LPH arts. 19, 20",
        "question_es": "¿Constan contenido mínimo, cierre, firmas, subsanaciones y custodia del libro/original?",
        "question_en": "Are the minimum contents, closure, signatures, corrections and custody of the book/original established?",
    },
    "G5": {
        "label_es": "Circulación, objeción, impugnación y uso",
        "label_en": "Circulation, objection, challenge and use",
        "articles": "LPH arts. 9.1.h, 18, 19, 21",
        "question_es": "¿Puede probarse el envío del ACTA, conocimiento, disconformidad, impugnación, certificado y uso posterior?",
        "question_en": "Can delivery of the minutes, knowledge, dissent, challenge, certification and later use be proved?",
    },
}


STATUS = {
    "facial-concern": {
        "code": "!",
        "label_es": "preocupación facial / incumplimiento alegado",
        "label_en": "facial concern / alleged non-compliance",
        "boundary_es": "El propio registro muestra una divergencia o una alegación concreta que exige prueba jurídica y factual; no es una declaración judicial de invalidez.",
        "boundary_en": "The record itself shows a divergence or a specific allegation requiring legal and factual proof; this is not a judicial finding of invalidity.",
    },
    "contested": {
        "code": "?",
        "label_es": "controvertido",
        "label_en": "contested",
        "boundary_es": "Existen posiciones o fuentes contrapuestas; deben conservarse juntas.",
        "boundary_en": "Competing positions or sources exist and must be preserved together.",
    },
    "located-open": {
        "code": "~",
        "label_es": "fuente localizada; prueba incompleta",
        "label_en": "source located; proof incomplete",
        "boundary_es": "Hay una fuente concreta, pero no cierra autoridad, servicio, autenticidad, integridad o efecto.",
        "boundary_en": "A concrete source exists but does not close authority, service, authenticity, integrity or effect.",
    },
    "unlocated": {
        "code": "Ø",
        "label_es": "no localizado",
        "label_en": "unlocated",
        "boundary_es": "La fuente requerida no se ha localizado en el universo finito revisado; ausencia no significa inexistencia.",
        "boundary_en": "The required source has not been located in the finite reviewed universe; absence does not mean nonexistence.",
    },
    "reference-only": {
        "code": "R",
        "label_es": "referencia posterior solamente",
        "label_en": "later reference only",
        "boundary_es": "Una fuente posterior refiere el evento, pero no sustituye la fuente primaria.",
        "boundary_en": "A later source recites the event but does not replace the primary source.",
    },
    "not-applicable": {
        "code": "—",
        "label_es": "no aplicable al registro",
        "label_en": "not applicable to this record",
        "boundary_es": "La puerta no se aplica al tipo de registro controlado.",
        "boundary_en": "The gate does not apply to the controlled record type.",
    },
}


HISTORICAL_LPH_VERSIONS = {
    "2011-pre-august": {
        "label_es": "Redacción anterior a la modificación publicada el 2 agosto 2011; para febrero/junio 2011 debe usarse la redacción vigente por artículo en esas fechas.",
        "label_en": "Text before the amendment published on 2 August 2011; the article-by-article text in force on the February/June 2011 date must be used.",
        "boe_url": "https://www.boe.es/buscar/act.php?id=BOE-A-1960-10906&p=20091124&tn=0",
    },
    "2013-2018-pre-december": {
        "label_es": "Redacción aplicable tras la modificación publicada el 27 junio 2013 y antes de la de 18 diciembre 2018, con control artículo por artículo.",
        "label_en": "Text applicable after the amendment published on 27 June 2013 and before the 18 December 2018 amendment, checked article by article.",
        "boe_url": "https://www.boe.es/buscar/act.php?id=BOE-A-1960-10906&p=20150610&tn=0",
    },
    "2021-2022": {
        "label_es": "Redacción consolidada tras la modificación publicada el 6 octubre 2021 y vigente el 4 febrero 2022, con control artículo por artículo.",
        "label_en": "Consolidated text after the amendment published on 6 October 2021 and in force on 4 February 2022, checked article by article.",
        "boe_url": "https://www.boe.es/buscar/act.php?id=BOE-A-1960-10906&p=20211006&tn=0",
    },
}


def _gate(status: str, es: str, en: str, evidence: list[str]) -> dict:
    return {"status": status, "es": es, "en": en, "evidence_ids": evidence}


CRITICAL_LPH_TIMELINE = {
    "SP-ACTA-2011-02-02": {
        "version": "2011-pre-august",
        "lineage_phase": "C1",
        "summary_es": "Cambio de cargos documentado; convocatoria, servicio, poderes y libro oficial no cerrados.",
        "summary_en": "Office changes documented; notice, service, proxies and official book not closed.",
        "gates": {
            "G1": _gate("unlocated", "La convocatoria completa y la autoridad individual del convocante no están localizadas.", "The complete notice and the individual caller's authority are unlocated.", []),
            "G2": _gate("unlocated", "No se ha localizado el paquete propietario-por-propietario de destinatarios y servicio.", "No owner-by-owner recipient and service package has been located.", []),
            "G3": _gate("located-open", "El ACTA registra asistentes, representaciones y elección de cargos; poderes, fincas, cuotas y denominador completo siguen abiertos.", "The minutes record attendees, representations and election of officers; proxies, properties, coefficients and the complete denominator remain open.", ["SP-EVT-2011-02-02-COM-MEETING", "SP-SRC-ACTA-2011-02-02-A"]),
            "G4": _gate("located-open", "Tres copias/variantes están controladas; original/libro, cierre, firmas y cotejo certificado permanecen abiertos.", "Three copies/variants are controlled; the original/book, closure, signatures and certified comparison remain open.", ["SP-SRC-ACTA-2011-02-02-A", "SP-SRC-ACTA-2011-02-02-B", "SP-SRC-ACTA-2011-02-02-C"]),
            "G5": _gate("contested", "La impugnación y resultados procesales posteriores están referidos, pero el expediente judicial completo y la circulación original no están cerrados.", "The challenge and later procedural outcomes are recited, but the complete court file and original circulation are not closed.", ["SP-EVT-2011-CHALLENGE-LITIGATION", "SP-REL-2011-CIVIL-CHALLENGE", "SP-EVT-2018-07-09-ACTA-CIRCULATION"]),
        },
    },
    "SP-ACTA-2011-06-22": {
        "version": "2011-pre-august",
        "lineage_phase": "C1",
        "summary_es": "Nodo controvertido de deuda, privación de voto, administración y propuesta Pamanil; incumplimiento alegado, no adjudicado aquí.",
        "summary_en": "Contested debt, voting-exclusion, administration and Pamanil-proposal node; non-compliance alleged, not adjudicated here.",
        "gates": {
            "G1": _gate("located-open", "El ACTA refiere convocatoria por la presidenta, pero no se ha localizado el aviso/orden del día autónomo ni la base completa de autoridad.", "The minutes refer to notice by the chair, but the standalone notice/agenda and complete authority basis are unlocated.", ["SP-EVT-2011-06-22-NOTICE"]),
            "G2": _gate("unlocated", "Destinatarios, domicilios, entrega/intentos y plazo completo no están localizados.", "Recipients, addresses, delivery/attempts and complete timing are unlocated.", ["SP-EVT-2011-06-22-NOTICE"]),
            "G3": _gate("facial-concern", "El ACTA registra a LPB con gran cuota pero sin voto por deuda atribuida; poderes, deuda, liquidación y aritmética de voto siguen abiertos.", "The minutes record LPB with a large coefficient but without a vote because of attributed debt; proxies, debt, accounting and voting arithmetic remain open.", ["SP-EVT-2011-06-22-COM-MEETING", "SP-EVT-2011-06-22-PAMANIL-PROPOSAL", "SP-SRC-ACTA-2011-06-22-B"]),
            "G4": _gate("located-open", "La copia registra a FMMM dando fe como secretario; libro oficial, audio, firmas y comparación de variantes no están cerrados.", "The copy records FMMM attesting as secretary; the official book, audio, signatures and variant comparison are not closed.", ["SP-SRC-ACTA-2011-06-22-A", "SP-SRC-ACTA-2011-06-22-B", "SP-SRC-ACTA-2011-06-22-C", "SP-SRC-ACTA-2011-06-22-D-PDF24"]),
            "G5": _gate("contested", "Objeciones y litigio posterior están documentados por referencias; deben leerse con los resultados adversos y el expediente completo pendiente.", "Objections and later litigation are documented by references; they must be read with the adverse outcomes and the complete file still pending.", ["SP-EVT-2011-CHALLENGE-LITIGATION", "SP-REL-2011-CIVIL-CHALLENGE", "SP-EVT-2018-07-09-ACTA-CIRCULATION"]),
        },
    },
    "SP-ACTA-2015-11-19": {
        "version": "2013-2018-pre-december",
        "lineage_phase": "C1",
        "summary_es": "La convocatoria/carta y el ACTA están localizados; la divergencia aproximada 89,02% representado / 0,770% con voto exige reconstrucción de deuda y voto.",
        "summary_en": "The notice/letter and minutes are located; the approximately 89.02% represented / 0.770% vote-qualified divergence requires debt and voting reconstruction.",
        "gates": {
            "G1": _gate("located-open", "Se controla una cadena de convocatoria, resumen de deuda y carta; autoridad y versión exacta por destinatario siguen abiertas.", "A notice, debt-summary and letter chain is controlled; authority and the exact recipient-specific version remain open.", ["SP-EVT-2015-11-03-CONVOCATION"]),
            "G2": _gate("located-open", "Existe cadena directa de circulación, pero faltan cabeceras nativas, lista completa, entrega y acuse por propietario.", "A direct circulation chain exists, but native headers, complete list, delivery and owner-by-owner receipt remain open.", ["SP-EVT-2015-11-03-CONVOCATION"]),
            "G3": _gate("facial-concern", "El registro presenta una divergencia extrema entre representación y voto, basada en deuda cuya aritmética y soporte siguen abiertos.", "The record presents an extreme represented/vote-qualified divergence based on debt whose arithmetic and support remain open.", ["SP-EVT-2015-11-19-COM-MEETING", "SP-SRC-ACTA-2015-11-19-C"]),
            "G4": _gate("located-open", "Dos ACTAS de 38 páginas y dos extractos procesales distintos están separados; libro, audio y cotejo final permanecen abiertos.", "Two 38-page minutes records and two distinct procedural extracts are separated; book, audio and final comparison remain open.", ["SP-SRC-ACTA-2015-11-19-C", "SP-SRC-ACTA-2015-11-19-D-ANNOTATED-38P", "SP-SRC-ACTA-2015-11-19-A", "SP-SRC-ACTA-2015-11-19-B"]),
            "G5": _gate("located-open", "La comunicación posterior está referida y el ACTA reaparece en circulación de 2018; envío directo completo, recepción y uso siguen abiertos.", "Later communication is recited and the minutes reappear in 2018 circulation; complete direct delivery, receipt and use remain open.", ["SP-EVT-2018-07-09-ACTA-CIRCULATION"]),
        },
    },
    "SP-ACTA-2016-04-26": {
        "version": "2013-2018-pre-december",
        "lineage_phase": "C1",
        "summary_es": "La convocatoria y la asistencia de Patricia/LPB están documentadas; la divergencia 89,727% representado / 11,039% con voto requiere soporte finca-deuda-voto.",
        "summary_en": "The notice and Patricia/LPB attendance are documented; the 89.727% represented / 11.039% vote-qualified divergence requires property-debt-vote support.",
        "gates": {
            "G1": _gate("located-open", "Existe aviso separado y cadena de convocatoria/análisis; emisor, autoridad y anexos deben cerrarse fuente por fuente.", "A separate notice and notice/analysis chain exist; issuer, authority and annexes must be closed source by source.", ["SP-EVT-2016-04-15-CONVOCATION-CHAIN", "SP-SRC-ACTA-2016-04-26-NOTICE-01"]),
            "G2": _gate("located-open", "El paquete fue conocido y la reunión fue atendida por el perímetro LPB; la prueba completa de servicio a todos los propietarios sigue abierta.", "The package was known and the LPB perimeter attended the meeting; complete service proof for every owner remains open.", ["SP-EVT-2016-04-15-CONVOCATION-CHAIN", "SP-EVT-2016-04-20-RECORD-REQUEST", "SP-EVT-2016-04-21-AC-PWC-AUTHORITY"]),
            "G3": _gate("facial-concern", "La fuente registra 89,727% representado, LPB 72,976% y 11,039% con voto; cuentas, deuda, poderes y cálculo por punto siguen abiertos.", "The source records 89.727% represented, LPB 72.976% and 11.039% vote-qualified; accounts, debt, proxies and item-by-item calculation remain open.", ["SP-EVT-2016-04-26-COM-MEETING", "SP-SRC-ACTA-2016-04-26-A"]),
            "G4": _gate("located-open", "Dos familias completas de 77 páginas y tres parciales están separadas; audio, libro y certificación manual permanecen abiertos.", "Two complete 77-page families and three partials are separated; audio, book and manual certification remain open.", ["SP-SRC-ACTA-2016-04-26-A", "SP-SRC-ACTA-2016-04-26-B", "SP-SRC-ACTA-2016-04-26-C", "SP-SRC-ACTA-2016-04-26-C-47P", "SP-SRC-ACTA-2016-04-26-C-50P"]),
            "G5": _gate("located-open", "Solicitudes, análisis posjunta y transmisión posterior están controlados; distribución oficial completa, respuesta y adopción siguen abiertas.", "Requests, post-meeting analysis and later transmission are controlled; complete official distribution, response and adoption remain open.", ["SP-EVT-2016-06-10-DEBT-ANALYSIS", "SP-EVT-2022-05-03-10-ACTA-TRANSMISSION"]),
        },
    },
    "SP-ACTA-2017-06-12": {
        "version": "2013-2018-pre-december",
        "lineage_phase": "C1",
        "summary_es": "Continuidad C1 con administración FMMM/Pamalexsha; 87,098% representado / 6,545% con voto y votación del informe de morosidad abiertas.",
        "summary_en": "C1 continuity with FMMM/Pamalexsha administration; 87.098% represented / 6.545% vote-qualified and the vote on the arrears report remain open.",
        "gates": {
            "G1": _gate("located-open", "Se controlan comunicaciones de acuerdos/ACTA, pero la convocatoria autónoma, autoridad y agenda exacta requieren cierre.", "Agreement/minutes communications are controlled, but the standalone notice, authority and exact agenda require closure.", ["SP-EVT-2017-PAMALEXSHA-COMMUNICATIONS"]),
            "G2": _gate("located-open", "Hay metadatos de entrega/circulación; lista completa, servicio y recepción propietario por propietario no están cerrados.", "Delivery/circulation metadata exists; the complete list, service and owner-by-owner receipt are not closed.", ["SP-EVT-2017-PAMALEXSHA-COMMUNICATIONS", "SP-DOC-2017-06-12-JONATHAN-DELIVERY-RECITAL"]),
            "G3": _gate("facial-concern", "El ACTA registra 87,098% representado y 6,545% con voto; deuda, poderes y si el informe de morosidad fue votado siguen abiertos.", "The minutes record 87.098% represented and 6.545% vote-qualified; debt, proxies and whether the arrears report was voted remain open.", ["SP-EVT-2017-06-12-COM-MEETING", "SP-SRC-ACTA-2017-06-12"]),
            "G4": _gate("located-open", "ACTA de 13 páginas localizada; original/libro, audio, anexos y cotejo final permanecen abiertos.", "A 13-page minutes record is located; original/book, audio, annexes and final comparison remain open.", ["SP-SRC-ACTA-2017-06-12"]),
            "G5": _gate("located-open", "Hay recital de entrega y comunicaciones, pero la cadena nativa, acuses, objeciones y uso completo no están cerrados.", "There is a delivery recital and communications, but the native chain, receipts, objections and complete use are not closed.", ["SP-DOC-2017-06-12-JONATHAN-DELIVERY-RECITAL", "SP-EVT-2017-PAMALEXSHA-COMMUNICATIONS"]),
        },
    },
    "SP-ACTA-2018-05-18": {
        "version": "2013-2018-pre-december",
        "lineage_phase": "C1→C2",
        "summary_es": "Puente documentado hacia C2: seguridad/acceso, CAM 13,034%, LPB 72,976% representada por el AC y sólo 0,385% con voto según el ACTA.",
        "summary_en": "Documented bridge into C2: security/access, CAM 13.034%, LPB 72.976% represented by the Insolvency Administrator and only 0.385% vote-qualified according to the minutes.",
        "gates": {
            "G1": _gate("unlocated", "No se ha localizado una convocatoria autónoma que cierre órgano convocante, autoridad y agenda final.", "No standalone notice closing the calling body, authority and final agenda has been located.", []),
            "G2": _gate("unlocated", "No está localizada la lista completa de destinatarios, domicilios, entrega/intentos y acuses.", "The complete recipient list, addresses, delivery/attempts and receipts are unlocated.", []),
            "G3": _gate("facial-concern", "El ACTA registra 86,715% representado, LPB 72,976%, CAM 13,034% y sólo 0,385% con voto; deuda, poderes, conflictos y mayoría por punto siguen abiertos.", "The minutes record 86.715% represented, LPB 72.976%, CAM 13.034% and only 0.385% vote-qualified; debt, proxies, conflicts and item-by-item majority remain open.", ["SP-EVT-2018-05-18-COM-MEETING", "SP-SRC-ACTA-2018-05-18-B"]),
            "G4": _gate("located-open", "Una copia de nueve páginas, su hermana y dos parciales están separadas; libro, audio y comparación final siguen abiertos.", "A nine-page copy, its sibling and two partials are separated; book, audio and final comparison remain open.", ["SP-SRC-ACTA-2018-05-18-A", "SP-SRC-ACTA-2018-05-18-B", "SP-SRC-ACTA-2018-05-18-B-ALT", "SP-SRC-ACTA-2018-05-18-C"]),
            "G5": _gate("facial-concern", "La ejecución de seguridad/acceso y DP1132 están conectadas; faltan circulación del ACTA, instrucciones, contrato, llaves/cerraduras, alcance por finca y exceso eventual.", "Security/access implementation and DP1132 are connected; minutes circulation, instructions, contract, key/lock records, property scope and any excess remain open.", ["SP-EVT-2018-DP1132-IMPLEMENTATION", "SP-REL-2018-AC-LPB-SECURITY"]),
        },
    },
    "SP-ACTA-2018-07-05": {
        "version": "2013-2018-pre-december",
        "lineage_phase": "C2",
        "summary_es": "Fase C2 con convocatoria separada localizada y posterior circulación; autoridad, servicio completo, voto y ejecución siguen abiertos.",
        "summary_en": "C2 phase with a separate located notice and later circulation; authority, complete service, voting and implementation remain open.",
        "gates": {
            "G1": _gate("located-open", "Existe una convocatoria de una página; emisor, autoridad y relación exacta con la reunión siguen abiertos.", "A one-page notice exists; issuer, authority and exact relationship to the meeting remain open.", ["SP-SRC-ACTA-2018-07-05-NOTICE-01"]),
            "G2": _gate("located-open", "La convocatoria está preservada, pero no la prueba completa de destinatarios, entrega y recepción.", "The notice is preserved, but complete recipient, delivery and receipt proof is not.", ["SP-SRC-ACTA-2018-07-05-NOTICE-01"]),
            "G3": _gate("facial-concern", "El ACTA trata deuda, acceso, servicios, zonas comunes y voto; poderes, derecho de voto, coeficientes y resultado por punto requieren cotejo.", "The minutes address debt, access, utilities, common areas and voting; proxies, voting entitlement, coefficients and item-by-item outcome require comparison.", ["SP-EVT-2018-07-05-COM-MEETING", "SP-SRC-ACTA-2018-07-05"]),
            "G4": _gate("located-open", "Copia de nueve páginas y variante alternativa localizadas; original/libro, audio, anexos y verificación manual siguen abiertos.", "A nine-page copy and alternate variant are located; original/book, audio, annexes and manual verification remain open.", ["SP-SRC-ACTA-2018-07-05", "SP-SRC-ACTA-2018-07-05-ALT"]),
            "G5": _gate("located-open", "La circulación por correo de ACTAS y la ejecución de seguridad/acceso están registradas; destinatarios, adjuntos, acuses y alcance causal completos siguen abiertos.", "Email circulation of minutes and security/access implementation are registered; complete recipients, attachments, receipts and causal scope remain open.", ["SP-EVT-2018-07-09-ACTA-CIRCULATION", "SP-EVT-2018-DP1132-IMPLEMENTATION", "SP-REL-2018-AUTO804"]),
        },
    },
    "SP-RECITAL-2018-11-20": {
        "version": "2013-2018-pre-december",
        "lineage_phase": "C2",
        "summary_es": "Evento referido en 2022: convocatoria, asistencia, votos, ACTA y circulación autónomos no localizados.",
        "summary_en": "Event recited in 2022: standalone notice, attendance, votes, minutes and circulation are unlocated.",
        "gates": {
            "G1": _gate("unlocated", "Convocatoria, autoridad y agenda no localizadas.", "Notice, authority and agenda are unlocated.", []),
            "G2": _gate("unlocated", "Destinatarios y servicio no localizados.", "Recipients and service are unlocated.", []),
            "G3": _gate("unlocated", "Asistencia, poderes, cuotas, deuda, votos y mayorías no localizados.", "Attendance, proxies, coefficients, debt, votes and majorities are unlocated.", []),
            "G4": _gate("unlocated", "ACTA autónoma, firmas y libro no localizados.", "Standalone minutes, signatures and book are unlocated.", ["SP-SRC-RECITAL-2018-11-20"]),
            "G5": _gate("reference-only", "El ACTA de 2022 refiere el estudio de reforma; esa referencia no prueba el contenido ni la validez del evento de 2018.", "The 2022 minutes recite the reform study; that recital does not prove the content or validity of the 2018 event.", ["SP-EVT-2018-11-20-REFORM-STUDY", "SP-SRC-RECITAL-2018-11-20", "SP-EVT-2019-10-24-NONCONVALIDATION"]),
        },
    },
    "SP-ACTA-2022-02-04": {
        "version": "2021-2022",
        "lineage_phase": "C2",
        "summary_es": "Nodo proyecto/CAM: 20,993% registrado, proyecto CAM, derrama y deuda LPB; Gil/Aweswell alegan falta de convocatoria y comunicación directa.",
        "summary_en": "CAM/project node: 20.993% recorded, CAM project, levy and LPB debt; Gil/Aweswell allege no notice and no direct communication.",
        "gates": {
            "G1": _gate("facial-concern", "El ACTA registra órgano y presidencia, pero la convocatoria nativa, autoridad exacta y agenda servida no están localizadas.", "The minutes record the body and chair, but the native notice, exact authority and served agenda are unlocated.", ["SP-EVT-2022-02-04-COM-MEETING"]),
            "G2": _gate("facial-concern", "Gil declara que su perímetro no recibió invitación ni conocimiento previo; falta el paquete propietario-por-propietario para probar o refutar selección, error o servicio alternativo.", "Gil states that his perimeter received no invitation or prior knowledge; the owner-by-owner package needed to prove or refute selection, error or alternative service is missing.", ["SP-EVT-2022-02-04-COM-MEETING"]),
            "G3": _gate("facial-concern", "El ACTA registra 20,993%, llama a CAM propietaria mayoritaria y el anexo carga a LPB 72,976%; títulos, poderes, deuda, conflictos, abstenciones y votos por punto deben reconciliarse.", "The minutes record 20.993%, call CAM the majority owner and charge LPB at 72.976% in the annex; title, proxies, debt, conflicts, abstentions and item-by-item votes require reconciliation.", ["SP-EVT-2022-02-04-COM-MEETING", "SP-SRC-ACTA-2022-02-04"]),
            "G4": _gate("located-open", "Tres variantes de siete páginas están controladas; libro diligenciado, cierre, firmas, anexos y audio siguen abiertos.", "Three seven-page variants are controlled; the diligenced book, closure, signatures, annexes and audio remain open.", ["SP-SRC-ACTA-2022-02-04", "SP-SRC-ACTA-2022-02-04-ALT", "SP-SRC-ACTA-2022-02-04-ALT-3492026"]),
            "G5": _gate("facial-concern", "Gil atribuye conocimiento posterior a reenvío Thompson y no a comunicación directa de la Comunidad; mensaje nativo, hash, cadena anterior, servicio oficial y usos posteriores siguen abiertos.", "Gil attributes later knowledge to Thompson forwarding rather than direct Community delivery; native message, hash, upstream chain, official service and later uses remain open.", ["SP-EVT-2022-05-03-10-ACTA-TRANSMISSION", "SP-REL-2022-PROJECT"]),
        },
    },
}


STAGE_TO_GATE = {
    "pre_meeting": "G1/G2",
    "pre_meeting_notice": "G1/G2",
    "meeting_record": "G3/G4",
    "annex_objection": "G3/G5",
    "post_circulation": "G5",
    "implementation": "G5",
    "later_reliance": "G5",
}


CANONICAL_REFERENCE_RULE = {
    "es": (
        "Cada pieza localizada o cada hueco material recibe un ID estable único. "
        "La referencia canónica es ID + URL bilingüe + fragmento. Un ID de hueco "
        "no fabrica un documento: conserva la obligación de localizarlo."
    ),
    "en": (
        "Every located item or material gap receives one unique stable ID. The "
        "canonical reference is ID + bilingual URL + fragment. A gap ID does not "
        "fabricate a document; it preserves the duty to locate it."
    ),
}


CROSS_TRACK_MODEL = {
    "boundary_es": (
        "La visualización expone la hipótesis criminal atribuida de creación, adopción o uso "
        "consciente de autoridad, deuda, voto o ACTAS materialmente falsos/ineficaces para "
        "producir exclusión, control, coste, financiación o beneficio. No declara delito: cada "
        "puente exige autor, conocimiento, propósito, acto de uso, efecto patrimonial, nexo causal, "
        "beneficiario y exclusión razonada de error o título independiente."
    ),
    "boundary_en": (
        "The visualisation exposes the attributed criminal hypothesis that materially false or "
        "ineffective authority, debt, voting or minutes were knowingly created, adopted or used "
        "to produce exclusion, control, cost, finance or benefit. It does not declare a crime: "
        "every bridge requires author, knowledge, purpose, act of use, patrimonial effect, causal "
        "link, beneficiary and reasoned exclusion of error or independent title."
    ),
    "grades": {
        "direct-documentary": {
            "code": "DOC",
            "label_es": "puente documental directo",
            "label_en": "direct documentary bridge",
        },
        "attributed-criminal-hypothesis": {
            "code": "HIP",
            "label_es": "hipótesis criminal atribuida",
            "label_en": "attributed criminal hypothesis",
        },
        "reliance-open": {
            "code": "OPEN",
            "label_es": "dependencia o uso por producir",
            "label_en": "dependency or use to be produced",
        },
        "institutional-notice": {
            "code": "NOTICE",
            "label_es": "institución puesta en conocimiento / SAIP",
            "label_en": "institution notified / access request",
        },
    },
    "spine": [
        {
            "id": "community-2011",
            "label_es": "2011 · deuda, voto y autoridad C1",
            "label_en": "2011 · C1 debt, voting and authority",
            "grade": "attributed-criminal-hypothesis",
            "evidence_ids": ["SP-ACTA-2011-06-22", "SP-EVT-2011-06-22-COM-MEETING"],
        },
        {
            "id": "community-2018",
            "label_es": "2018 · seguridad/acceso y giro C1→C2",
            "label_en": "2018 · security/access and C1→C2 turn",
            "grade": "direct-documentary",
            "evidence_ids": ["SP-ACTA-2018-05-18", "SP-REL-2018-AC-LPB-SECURITY"],
        },
        {
            "id": "reform-2018",
            "label_es": "20 nov 2018 · reforma referida; ACTA no localizada",
            "label_en": "20 Nov 2018 · reform recited; minutes unlocated",
            "grade": "reliance-open",
            "evidence_ids": ["SP-RECITAL-2018-11-20", "SP-SRC-RECITAL-2018-11-20"],
        },
        {
            "id": "community-2022",
            "label_es": "4 feb 2022 · proyecto CAM, derrama, deuda y autorizaciones",
            "label_en": "4 Feb 2022 · CAM project, levy, debt and authorisations",
            "grade": "direct-documentary",
            "evidence_ids": ["SP-ACTA-2022-02-04", "SP-REL-2022-PROJECT"],
        },
    ],
    "tracks": [
        {
            "id": "ricpe-ric",
            "label_es": "RICPE / RIC · capital, gobierno, DD y conflicto",
            "label_en": "RICPE / RIC · capital, governance, DD and conflict",
            "grade": "reliance-open",
            "route_es": "es/ric-private-equity-sun-park/",
            "route_en": "en/ric-private-equity-sun-park/",
            "basis_es": "La conexión proyecto/personas/certificación está documentada; qué ACTA o autoridad comunitaria se entregó, verificó o adoptó en cada decisión RICPE/RIC sigue abierto.",
            "basis_en": "The project/person/certification connection is documented; which Community minutes or authority was supplied, checked or adopted in each RICPE/RIC decision remains open.",
        },
        {
            "id": "refurbishment-mynd",
            "label_es": "Reforma / HNT / MYND · obras, explotación y valor",
            "label_en": "Refurbishment / HNT / MYND · works, operation and value",
            "grade": "attributed-criminal-hypothesis",
            "route_es": "es/cadena-instrumentalizacion-ric-fondos-incentivos/",
            "route_en": "en/institutionalisation-chain-ric-eu-incentives/",
            "basis_es": "El resultado de reforma/explotación es visible y el proyecto aparece en el ACTA 2022; deben reconciliarse obra por obra la autoridad, finca, coste, factura, pagador, ingreso y beneficio.",
            "basis_en": "The refurbishment/operation outcome is visible and the project appears in the 2022 minutes; authority, property, cost, invoice, payer, income and benefit require works-level reconciliation.",
        },
        {
            "id": "regional-incentive",
            "label_es": "Incentivo regional GC/836/P06 · inversión y 60 empleos",
            "label_en": "Regional incentive GC/836/P06 · investment and 60 jobs",
            "grade": "reliance-open",
            "route_es": "es/incentivos-regionales-gc836-p06/",
            "route_en": "en/regional-incentives-gc836-p06/",
            "basis_es": "La ayuda y su expediente están identificados; falta producir qué título, disponibilidad, permisos, ACTAS, costes y otras ayudas fueron declarados y verificados.",
            "basis_en": "The aid and file are identified; production is required of the title, availability, permissions, minutes, costs and other aid declared and checked.",
        },
        {
            "id": "feder",
            "label_es": "FEDER / fondos europeos · gasto, certificación y acumulación",
            "label_en": "ERDF / EU funds · expenditure, certification and cumulation",
            "grade": "reliance-open",
            "route_es": "es/snca-fondos-europeos-trazabilidad/",
            "route_en": "en/snca-eu-funds-traceability/",
            "basis_es": "La operación publicitada y las solicitudes de trazabilidad están controladas; faltan selección, beneficiario, gasto, verificaciones, auditoría y cualquier dependencia de autoridad comunitaria.",
            "basis_en": "The publicised operation and traceability requests are controlled; selection, beneficiary, expenditure, checks, audit and any dependency on Community authority remain to be produced.",
        },
        {
            "id": "yaiza",
            "label_es": "Ayuntamiento de Yaiza · obra, licencia, primera ocupación y uso",
            "label_en": "Yaiza Council · works, licence, first occupation and use",
            "grade": "reliance-open",
            "route_es": "es/yaiza-trazabilidad-institucional/",
            "route_en": "en/yaiza-institutional-traceability/",
            "basis_es": "Existen expedientes municipales y puesta en conocimiento; debe producirse cada título/ACTA/autorización aportado, su verificación y el alcance finca por finca.",
            "basis_en": "Municipal files and notice exist; every supplied title/minutes/authorisation, its verification and property-by-property scope must be produced.",
        },
        {
            "id": "cabildo",
            "label_es": "Cabildo de Lanzarote · título/explotación turística",
            "label_en": "Cabildo de Lanzarote · tourism title/operation",
            "grade": "reliance-open",
            "route_es": "es/cabildo-lanzarote-turismo-trazabilidad/",
            "route_en": "en/cabildo-lanzarote-tourism-traceability/",
            "basis_es": "La ruta turística está documentada y ha sido puesta en conocimiento; falta el expediente completo que muestre qué autoridad comunitaria se invocó o comprobó.",
            "basis_en": "The tourism route is documented and has been notified; the complete file showing which Community authority was invoked or checked remains outstanding.",
        },
        {
            "id": "saip",
            "label_es": "SAIP / entregas registradas · producción y respuesta pendientes",
            "label_en": "Access requests / registered deliveries · production and response pending",
            "grade": "institutional-notice",
            "route_es": "es/ricpe-acciones-pendientes-ahora/",
            "route_en": "en/ricpe-outstanding-actions-now/",
            "basis_es": "Los justificantes prueban presentación/puesta en conocimiento, no dependencia, irregularidad ni respuesta de fondo. Deben interconectarse las producciones futuras por documento y expediente.",
            "basis_en": "Receipts prove filing/notice, not dependency, irregularity or a merits response. Future productions must be interconnected by document and file.",
        },
    ],
}


def validate_lph_control(document_ids: set[str]) -> None:
    if set(LPH_GATES) != {"G1", "G2", "G3", "G4", "G5"}:
        raise ValueError("LPH lifecycle must define exactly gates G1-G5")
    if len(STATUS) != len(set(STATUS)):
        raise ValueError("duplicate LPH status keys")
    for event_id, event in CRITICAL_LPH_TIMELINE.items():
        if event["version"] not in HISTORICAL_LPH_VERSIONS:
            raise ValueError(f"{event_id}: unknown historical LPH version")
        if set(event["gates"]) != set(LPH_GATES):
            raise ValueError(f"{event_id}: incomplete LPH gate set")
        for gate_id, gate in event["gates"].items():
            if gate["status"] not in STATUS:
                raise ValueError(f"{event_id}/{gate_id}: unknown status")
            missing = sorted(set(gate["evidence_ids"]) - document_ids)
            if missing:
                raise ValueError(f"{event_id}/{gate_id}: unknown evidence IDs {missing}")
    for node in CROSS_TRACK_MODEL["spine"]:
        missing = sorted(set(node["evidence_ids"]) - document_ids - set(CRITICAL_LPH_TIMELINE))
        if missing:
            raise ValueError(f"cross-track node {node['id']}: unknown evidence IDs {missing}")
        if node["grade"] not in CROSS_TRACK_MODEL["grades"]:
            raise ValueError(f"cross-track node {node['id']}: unknown grade")
    track_ids = [track["id"] for track in CROSS_TRACK_MODEL["tracks"]]
    if len(track_ids) != len(set(track_ids)):
        raise ValueError("duplicate cross-track IDs")
    for track in CROSS_TRACK_MODEL["tracks"]:
        if track["grade"] not in CROSS_TRACK_MODEL["grades"]:
            raise ValueError(f"cross-track {track['id']}: unknown grade")

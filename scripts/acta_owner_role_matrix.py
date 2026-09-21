"""Controlled role attribution for Sun Park Owners' Community ACTA events.

The matrix separates five functions that must never be collapsed into one:
caller/convener, chair or meeting manager, secretary/administrator, ACTA
author/attestor, and custody/circulation.  A perimeter label is documentary and
date-specific.  It does not establish authority, validity, legal succession,
joint conduct, intent, criminality or guilt.
"""

from __future__ import annotations


PRINCIPAL_LINEAGES = {
    "A": {
        "label_es": "A · Montelanza/JPS original · pre-venta",
        "label_en": "A · Original Montelanza/JPS · pre-sale",
        "definition_es": (
            "Fase anterior a la transacción de activos de junio de 2008. "
            "«JPS» identifica el perímetro histórico indicado por Gil; la relación "
            "societaria o dominical JPS–Montelanza debe acreditarse fuente por fuente."
        ),
        "definition_en": (
            "Period before the June 2008 asset transaction. ‘JPS’ identifies the "
            "historical perimeter stated by Gil; the JPS–Montelanza corporate or title "
            "relationship must be proved source by source."
        ),
    },
    "B": {
        "label_es": "B · Proyecto LPB → Aweswell/LPB · Gil y Patricia",
        "label_en": "B · LPB project → Aweswell/LPB · Gil and Patricia",
        "definition_es": (
            "Sucesión documental del lado del proyecto. B0 identifica Multimatrix/LPB "
            "antes de la entrada documentada de Gil y Patricia; B1 identifica la fase "
            "Aweswell/LPB. Ningún acto B0 se atribuye personalmente a Gil o Patricia."
        ),
        "definition_en": (
            "Documentary project-side succession. B0 identifies Multimatrix/LPB before "
            "Gil and Patricia's documented entry; B1 identifies the Aweswell/LPB phase. "
            "No B0 act is attributed personally to Gil or Patricia."
        ),
    },
    "C": {
        "label_es": "C · Línea adversa alegada · disidentes → Acosta Matos",
        "label_en": "C · Alleged adverse lineage · dissidents → Acosta Matos",
        "definition_es": (
            "C1 identifica la fase Aizpurúa/Molina–Roque Prieto/FMMM/Pamanil–Cogolludo; "
            "C2 identifica la fase posterior Acosta Matos/CAM. La flecha expresa la "
            "secuencia atribuida por Gil y nodos documentados, no sucesión jurídica, "
            "dirección común, concierto, ilicitud o culpabilidad ya probados."
        ),
        "definition_en": (
            "C1 identifies the Aizpurúa/Molina–Roque Prieto/FMMM/Pamanil–Cogolludo phase; "
            "C2 identifies the later Acosta Matos/CAM phase. The arrow records Gil's "
            "attributed sequence and documented nodes, not proved legal succession, common "
            "control, agreement, illegality or guilt."
        ),
    },
    "D": {
        "label_es": "D · Cruce o prueba insuficiente",
        "label_en": "D · Cross-lane or insufficient proof",
        "definition_es": (
            "Estado probatorio, no cuarto perímetro: la fuente cruza A/B/C o no permite "
            "atribuir con seguridad la convocatoria y producción documental."
        ),
        "definition_en": (
            "Evidence status, not a fourth perimeter: the source crosses A/B/C or does not "
            "safely attribute the call and documentary production."
        ),
    },
}


def _role(es: str, en: str, status: str = "documented-with-limitations") -> dict:
    return {"status": status, "es": es, "en": en}


OWNER_ROLE_MATRIX = {
    "SP-ACTA-2008-04-29": {
        "principal_lineage": "A", "phase_code": "A",
        "caller": _role(
            "La copia acredita convocatoria por correo certificado; persona convocante no identificada con seguridad.",
            "The copy records registered-mail notice; the individual convener is not safely identified.",
            "unresolved",
        ),
        "meeting_management": _role(
            "Reunión del período Montelanza/JPS original; durante la sesión se eligen presidencia, tesorería y secretaría, con nombres reservados en la edición pública.",
            "Original Montelanza/JPS-period meeting; chair, treasurer and secretary are elected during the session, with names withheld in the public edition.",
        ),
        "acta_authorship": _role(
            "El ACTA dice que fue redactada, leída y aprobada; el secretario da fe con visto bueno del presidente. La identidad pública del redactor material no está cerrada.",
            "The minutes say they were drafted, read and approved; the secretary attests with the chair's approval. The public identity of the material drafter is not closed.",
        ),
        "custody_circulation": _role(
            "Copia posterior localizada; libro diligenciado, original, custodia y circulación inicial no cotejados.",
            "Later copy located; diligenced book, original, custody and initial circulation have not been reconciled.",
            "open",
        ),
    },
    "SP-ACTA-2008-07-15": {
        "principal_lineage": "D", "phase_code": "D-MIXED",
        "caller": _role("Convocante exacto no resuelto.", "Exact convener unresolved.", "unresolved"),
        "meeting_management": _role(
            "Constan presidencia accidental y secretario-administrador; sus nombres permanecen reservados públicamente.",
            "An acting chair and secretary-administrator are recorded; their names remain publicly withheld.",
        ),
        "acta_authorship": _role(
            "El secretario-administrador cierra y da fe del ACTA; no se atribuye automáticamente a LPB ni a Montelanza.",
            "The secretary-administrator closes and attests the minutes; authorship is not automatically assigned to LPB or Montelanza.",
        ),
        "custody_circulation": _role(
            "Copia completa de nueve páginas y variante parcial de seis; libro, anexos y circulación inicial abiertos.",
            "Complete nine-page copy and partial six-page variant; book, annexes and initial circulation remain open.",
            "open",
        ),
    },
    "SP-ACTA-2008-07-25": {
        "principal_lineage": "B", "phase_code": "B0",
        "caller": _role("Convocante formal no identificado.", "Formal convener not identified.", "unresolved"),
        "meeting_management": _role(
            "La fuente registra a la representante de LPB actuando también para CEXP; es fase Multimatrix/LPB, no actuación personal de Gil o Patricia.",
            "The source records LPB's representative also acting for CEXP; this is the Multimatrix/LPB phase, not a personal act by Gil or Patricia.",
        ),
        "acta_authorship": _role(
            "Se registra redacción, lectura, aprobación y firma de los presentes; no consta un redactor individual separado.",
            "Drafting, reading, approval and signatures by attendees are recorded; no separate individual drafter is established.",
        ),
        "custody_circulation": _role(
            "Copia de trabajo localizada; original, libro, anexos y mensaje nativo permanecen abiertos.",
            "Working copy located; original, book, annexes and native message remain open.",
            "open",
        ),
    },
    "SP-ACTA-2008-12-17": {
        "principal_lineage": "D", "phase_code": "D-MIXED",
        "caller": _role("La convocatoria fuente no está unida; convocante no resuelto.", "Source notice not joined; convener unresolved.", "unresolved"),
        "meeting_management": _role(
            "Constan presidente y secretario accidental, con identidades reservadas; la fecha cae en la transición posterior a la compra.",
            "A chair and acting secretary are recorded with identities withheld; the date falls in the post-acquisition transition.",
        ),
        "acta_authorship": _role(
            "El secretario accidental da fe; redactor material y relación con A/B no cerrados.",
            "The acting secretary attests; material drafter and A/B relationship are not closed.",
        ),
        "custody_circulation": _role(
            "Copias Drive/correo localizadas; equivalencia, avisos, anexos y libro oficial abiertos.",
            "Drive/email copies located; equivalence, notices, annexes and official book remain open.",
            "open",
        ),
    },
    "SP-ACTA-2009-05-28": {
        "principal_lineage": "B", "phase_code": "B0",
        "caller": _role(
            "El ACTA sitúa la reunión bajo presidencia LPB; la convocatoria y servicio completos no están cerrados.",
            "The minutes place the meeting under the LPB chair; complete notice and service are not closed.",
        ),
        "meeting_management": _role(
            "Presidente actuando por LPB; secretario accidental y administrador Muyay. Fase Multimatrix/LPB anterior a Gil y Patricia.",
            "Chair acting for LPB; acting secretary and Muyay administrator. Multimatrix/LPB phase before Gil and Patricia.",
        ),
        "acta_authorship": _role(
            "El secretario accidental da fe con visto bueno del presidente; no se publica su identidad personal.",
            "The acting secretary attests with the chair's approval; the individual's identity is not published.",
        ),
        "custody_circulation": _role(
            "Copias posteriores localizadas; cuentas/anexos, equivalencia y libro diligenciado abiertos.",
            "Later copies located; accounts/annexes, equivalence and diligenced book remain open.",
            "open",
        ),
    },
    "SP-ACTA-2011-02-02": {
        "principal_lineage": "C", "phase_code": "C1",
        "caller": _role(
            "La fuente registra ausencia inicial de presidente y secretario; convocatoria original completa no localizada.",
            "The source records the initial absence of chair and secretary; the complete original notice is unlocated.",
            "unresolved",
        ),
        "meeting_management": _role(
            "Asunción Aizpurúa Sánchez es elegida presidenta por Roque Prieto, S.L.; Ana Jiménez Lort, secretaria; Cristina Molina Petit, tesorera. Álvaro Campanario Hernández aparece con representaciones múltiples.",
            "Asunción Aizpurúa Sánchez is elected chair for Roque Prieto, S.L.; Ana Jiménez Lort, secretary; Cristina Molina Petit, treasurer. Álvaro Campanario Hernández appears with multiple representations.",
        ),
        "acta_authorship": _role(
            "El ACTA registra la elección de secretaría, pero la copia no cierra quién preparó materialmente el texto ni cuándo se incorporó al libro.",
            "The minutes record the secretary's election, but the copy does not close who materially prepared the text or when it entered the book.",
            "open",
        ),
        "custody_circulation": _role(
            "Control y variantes localizados; libro, convocatoria, audio, poderes y cadena de entrega abiertos.",
            "Control copy and variants located; book, notice, audio, proxies and delivery chain remain open.",
            "open",
        ),
    },
    "SP-ACTA-2011-06-22": {
        "principal_lineage": "C", "phase_code": "C1",
        "caller": _role("Convocatoria atribuida en el ACTA a la presidenta Asunción Aizpurúa Sánchez.", "The minutes attribute the notice to chair Asunción Aizpurúa Sánchez."),
        "meeting_management": _role(
            "Aizpurúa preside; Francisco Mario Matos Matas actúa como administrador, estructura lista/deuda, lee documentos y participa en la gestión de la sesión.",
            "Aizpurúa chairs; Francisco Mario Matos Matas acts as administrator, structures attendance/debt, reads documents and participates in managing the session.",
        ),
        "acta_authorship": _role(
            "El cierre dice «yo como secretario doy fe» y la propuesta/contrato del administrador incluía actuar como secretario y custodiar documentación; la firma y libro oficiales siguen abiertos.",
            "The closing says ‘I as secretary attest’ and the administrator proposal/contract included acting as secretary and keeping records; official signature and book remain open.",
        ),
        "custody_circulation": _role(
            "Carril FMMM/Pamanil de administración y custodia documentado; variantes, original, libro y distribución completa no reconciliados.",
            "FMMM/Pamanil administration-and-custody lane documented; variants, original, book and complete distribution not reconciled.",
            "open",
        ),
    },
    "SP-ACTA-2012-08-10": {
        "principal_lineage": "B", "phase_code": "B1",
        "caller": _role(
            "LPB/Gil aparece en presidencia y firma; asistentes adversos impugnaron la legalidad de la convocatoria.",
            "LPB/Gil appears in the chair and signature block; adverse attendees challenged the legality of the notice.",
        ),
        "meeting_management": _role(
            "Gil Marer dirige la sesión por LPB; Álvaro Campanario Hernández fue designado secretario de la reunión según la correspondencia controlada.",
            "Gil Marer manages the session for LPB; Álvaro Campanario Hernández was appointed meeting secretary according to controlled correspondence.",
        ),
        "acta_authorship": _role(
            "Campanario debía finalizar el ACTA y remitió posteriormente una copia; la fuente registra que no se sometió acuerdo a votación.",
            "Campanario was to finalise the minutes and later sent a copy; the source records that no resolution was put to a vote.",
        ),
        "custody_circulation": _role(
            "Copia remitida después de la reunión; declaración presidencial localizada, objeción separada no localizada y libro/custodia oficial abiertos.",
            "Copy sent after the meeting; president's statement located, separate objection unlocated, and official book/custody open.",
            "open",
        ),
    },
    "SP-ACTA-2014-04-10": {
        "principal_lineage": "B", "phase_code": "B1",
        "caller": _role("LPB, representada por Gil Marer, figura como convocante en las capacidades reivindicadas.", "LPB, represented by Gil Marer, is recorded as convener in the asserted capacities."),
        "meeting_management": _role(
            "Gil/LPB promueve y preside el carril competidor; asistencia, poderes y aceptación permanecen controvertidos.",
            "Gil/LPB promotes and chairs the competing lane; attendance, proxies and acceptance remain contested.",
        ),
        "acta_authorship": _role(
            "El notario autoriza el ACTA DE PRESENCIA/protocolo 422B. La versión mecanografiada distinta conserva solo páginas 1, 5 y 6 y su autor material no está cerrado.",
            "The notary authorises the ACTA DE PRESENCIA/protocol 422B. The distinct typed version survives only as pages 1, 5 and 6 and its material author is not closed.",
        ),
        "custody_circulation": _role(
            "Dos portadores posteriores son byte-idénticos; el enlace de circulación inicial devuelve 404. Original notarial, servicio y recepción inicial abiertos.",
            "Two later carriers are byte-identical; the initial-circulation link returns 404. Notarial original, service and initial receipt remain open.",
            "open",
        ),
    },
    "SP-ACTA-2014-08-28-CP": {
        "principal_lineage": "B", "phase_code": "B1",
        "caller": _role("Convocatoria previa de 8 de agosto bajo presidencia LPB, representada por Gil Marer.", "Prior 8 August notice under the LPB chair, represented by Gil Marer."),
        "meeting_management": _role(
            "LPB/Gil preside; consta secretario accidental y traductora; es distinto del ACTA CEXP del mismo día.",
            "LPB/Gil chairs; an acting secretary and interpreter are recorded; this is distinct from the same-day CEXP minutes.",
        ),
        "acta_authorship": _role(
            "La fuente dice que el notario levanta acta; presidencia y secretaría conservan funciones propias separadas.",
            "The source says the notary records the meeting; chair and secretary retain their separate functions.",
        ),
        "custody_circulation": _role(
            "Control de 21 páginas localizado; nativo/certificado, anexos, libro y circulación completa abiertos.",
            "Twenty-one-page control located; native/certified copy, annexes, book and complete circulation remain open.",
            "open",
        ),
    },
    "SP-ACTA-2015-11-19": {
        "principal_lineage": "C", "phase_code": "C1",
        "caller": _role("ACTA bajo presidencia de Asunción Aizpurúa Sánchez; aviso/servicio completos abiertos.", "Minutes under chair Asunción Aizpurúa Sánchez; complete notice/service remains open."),
        "meeting_management": _role("Aizpurúa preside; Francisco Mario Matos Matas actúa como administrador y gestiona lectura, cuentas, seguridad y desarrollo documental.", "Aizpurúa chairs; Francisco Mario Matos Matas acts as administrator and manages readings, accounts, security and the documentary process."),
        "acta_authorship": _role("FMMM aparece en el carril secretario/administrador; autor material, firma y libro oficial requieren cotejo.", "FMMM appears in the secretary/administrator lane; material authorship, signature and official book require reconciliation.", "open"),
        "custody_circulation": _role("ACTA posterior de 2016 afirma que FMMM la envió a propietarios; copias y extractos variantes requieren conciliación.", "The later 2016 minutes state that FMMM sent it to owners; copies and extract variants require reconciliation.", "open"),
    },
    "SP-ACTA-2016-04-26": {
        "principal_lineage": "C", "phase_code": "C1",
        "caller": _role("Cadena de convocatoria 15–20 abril bajo presidencia de Asunción Aizpurúa Sánchez y administración FMMM.", "15–20 April notice chain under chair Asunción Aizpurúa Sánchez and FMMM administration."),
        "meeting_management": _role(
            "Aizpurúa preside y FMMM administra/estructura la sesión. Patricia Domínguez comparece por LPB y Matkator según la fuente; no es convocante, presidenta ni autora del ACTA.",
            "Aizpurúa chairs and FMMM administers/structures the session. Patricia Domínguez appears for LPB and Matkator according to the source; she is not the convener, chair or ACTA author.",
        ),
        "acta_authorship": _role("FMMM ocupa el carril de secretario-administrador; firma, audio y libro oficial no están cotejados.", "FMMM occupies the secretary-administrator lane; signature, audio and official book are not reconciled.", "open"),
        "custody_circulation": _role("Dos binarios completos de 77 páginas y paquetes parciales; transmisión posterior localizada, circulación original y audio abiertos.", "Two complete 77-page binaries and partial packages; later transmission located, original circulation and audio remain open.", "open"),
    },
    "SP-ACTA-2017-06-12": {
        "principal_lineage": "C", "phase_code": "C1",
        "caller": _role("La reunión se abre bajo la presidencia saliente Aizpurúa/FMMM; servicio completo abierto.", "The meeting opens under the outgoing Aizpurúa/FMMM administration; complete service remains open."),
        "meeting_management": _role("Aizpurúa abre; Antonio Cogolludo Rojas resulta elegido presidente; FMMM continúa como secretario-administrador; Shaila María Cogolludo Ramos figura en la junta rectora.", "Aizpurúa opens; Antonio Cogolludo Rojas is elected chair; FMMM continues as secretary-administrator; Shaila María Cogolludo Ramos appears in the governing board."),
        "acta_authorship": _role("El ACTA sitúa a FMMM como secretario por su función de administrador; autor material y firmas requieren cotejo del original.", "The minutes place FMMM as secretary through his administrator function; material author and signatures require original-copy reconciliation.", "open"),
        "custody_circulation": _role("Control y correo de entrega localizados; destinatarios completos, anexos y libro oficial abiertos.", "Control copy and delivery email located; complete recipients, annexes and official book remain open.", "open"),
    },
    "SP-ACTA-2018-05-18": {
        "principal_lineage": "C", "phase_code": "C1→C2",
        "caller": _role("Autoridad jurídica exacta del convocante abierta; ACTA bajo cargos Cogolludo/FMMM y presencia CAM.", "Exact legal-convener authority open; minutes under Cogolludo/FMMM officeholders with CAM present.", "open"),
        "meeting_management": _role("Antonio Cogolludo Rojas preside; FMMM actúa como secretario-administrador; Shaila María Cogolludo Ramos figura en la junta rectora. CAM interviene, pero presencia no equivale a convocatoria o autoría.", "Antonio Cogolludo Rojas chairs; FMMM acts as secretary-administrator; Shaila María Cogolludo Ramos appears in the governing board. CAM participates, but presence is not convocation or authorship."),
        "acta_authorship": _role("Carril presidente + secretario/administrador; autor material, audio y libro oficial abiertos.", "Chair plus secretary/administrator lane; material author, audio and official book remain open.", "open"),
        "custody_circulation": _role("Control de nueve páginas y variantes localizados; custodia oficial y comparación completa abiertas.", "Nine-page control and variants located; official custody and full comparison remain open.", "open"),
    },
    "SP-ACTA-2018-07-05": {
        "principal_lineage": "C", "phase_code": "C2",
        "caller": _role("ACTA bajo cargos comunitarios Cogolludo/FMMM; autoridad exacta y servicio dependen de la fuente completa.", "Minutes under Cogolludo/FMMM Community officeholders; exact authority and service depend on the complete source."),
        "meeting_management": _role("Antonio Cogolludo Rojas preside y FMMM/Pamalexsha actúa como secretario-administrador; CAM financia o asume partidas registradas, sin que ello pruebe autoría del ACTA.", "Antonio Cogolludo Rojas chairs and FMMM/Pamalexsha acts as secretary-administrator; CAM funds or assumes recorded items, which does not prove ACTA authorship."),
        "acta_authorship": _role("Bloque de firma presidente + secretario/administrador; redactor material y libro oficial abiertos.", "Chair plus secretary/administrator signature block; material drafter and official book remain open.", "open"),
        "custody_circulation": _role("Dos binarios visualmente equivalentes y aviso separado; destinatarios, servicio y uso judicial exacto abiertos.", "Two visually equivalent binaries and a separate notice; recipients, service and exact judicial use remain open.", "open"),
    },
    "SP-RECITAL-2018-11-20": {
        "principal_lineage": "C", "phase_code": "C2-REFERENCE-ONLY",
        "caller": _role("ACTA autónoma y convocatoria no localizadas; el convocante no puede certificarse desde la mención posterior.", "Standalone minutes and notice unlocated; the convener cannot be certified from the later recital.", "unlocated"),
        "meeting_management": _role("Material posterior sitúa a José Daniel Acosta Matos en presidencia y a FMMM/Pamalexsha en secretaría-administración; requiere la fuente primaria.", "Later material places José Daniel Acosta Matos in the chair and FMMM/Pamalexsha in the secretary-administration role; the primary source is required.", "later-recital-only"),
        "acta_authorship": _role("No determinable sin el ACTA autónoma, firmas y libro.", "Not determinable without the standalone minutes, signatures and book.", "unlocated"),
        "custody_circulation": _role("Solo mención posterior controlada; ACTA, aviso, asistencia, votos y anexos no localizados.", "Only a controlled later recital; minutes, notice, attendance, votes and annexes unlocated.", "unlocated"),
    },
    "SP-ACTA-2022-02-04": {
        "principal_lineage": "C", "phase_code": "C2",
        "caller": _role("La copia no cierra la autoridad y servicio del convocante; registra actuación del órgano bajo presidencia Acosta Matos.", "The copy does not close convener authority and service; it records organ action under the Acosta Matos chair.", "open"),
        "meeting_management": _role("José Daniel Acosta Matos preside y explica el proyecto CAM; FMMM/Pamalexsha actúa como secretario-administrador. Laura Patricia y Javier Acosta Matos aparecen en representaciones separadas; no son por ello autores.", "José Daniel Acosta Matos chairs and explains the CAM project; FMMM/Pamalexsha acts as secretary-administrator. Laura Patricia and Javier Acosta Matos appear in separate representations; that does not make them authors."),
        "acta_authorship": _role("La copia contiene firma de presidente, secretario/administrador y una secretaría separada públicamente expurgada; redactor material, cierre y libro siguen abiertos.", "The copy contains chair, secretary-administrator and a separate publicly redacted secretary signature; material drafter, closure and book remain open.", "open"),
        "custody_circulation": _role("Tres variantes de siete páginas; Gil atribuye conocimiento posterior a reenvío Thompson. Mensaje nativo, adjunto/hash, servicio directo y custodia oficial abiertos.", "Three seven-page variants; Gil attributes later knowledge to Thompson forwarding. Native message, attachment/hash, direct service and official custody remain open.", "open"),
    },
}


PRE_2008_CONTROL = {
    "status": "no-located-or-date-specific-referenced-acta",
    "es": (
        "No se ha localizado ni identificado por fecha una ACTA comunitaria anterior al 29 de abril de 2008. "
        "Los estatutos/título horizontal y referencias históricas anteriores no se convierten en ACTAS."
    ),
    "en": (
        "No Owners' Community ACTA earlier than 29 April 2008 has been located or identified by date. "
        "Earlier statutes/title instruments and historical references are not converted into minutes."
    ),
}


def validate_owner_role_matrix(event_ids: list[str]) -> None:
    expected = set(event_ids)
    actual = set(OWNER_ROLE_MATRIX)
    missing = expected - actual
    extra = actual - expected
    if missing or extra:
        raise RuntimeError(
            f"Owners' ACTA role matrix drift; missing={sorted(missing)} extra={sorted(extra)}"
        )
    for event_id, record in OWNER_ROLE_MATRIX.items():
        if record.get("principal_lineage") not in PRINCIPAL_LINEAGES:
            raise RuntimeError(f"{event_id}: invalid principal lineage")
        for role in ("caller", "meeting_management", "acta_authorship", "custody_circulation"):
            value = record.get(role)
            if not isinstance(value, dict) or not all(value.get(key) for key in ("status", "es", "en")):
                raise RuntimeError(f"{event_id}: incomplete role {role}")

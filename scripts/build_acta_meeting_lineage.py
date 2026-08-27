#!/usr/bin/env python3
"""Build the bilingual ACTA/meeting lineage pages and public lineage index.

The lineage layer never changes the source digitisation.  It records the
documented convener/body separately from Gil Marer's attributed perimeter
classification, gives every controlled meeting/ACTA event its own URL and
interlinks the full public OCR, redacted source facsimile, source-page gallery,
provenance and integrity material when those artifacts exist.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
INDEX = REPO / "evidence/community/actas/public-index.json"
LINEAGE = REPO / "evidence/community/actas/meeting-lineage-index-v1.json"
BASE_URL = "https://sbu001monterecco.github.io/por-derecho"


EVENTS = [
    {
        "id": "SP-ACTA-2008-04-29", "slug": "2008-04-29", "date": "2008-04-29", "record_type": "acta",
        "body": "owners", "title_es": "29 abril 2008 · formación de CEXP", "title_en": "29 April 2008 · CEXP formation",
        "perimeter": "pre_sale_montelanza", "attribution_status": "documented-context; convener identity unresolved", "confidence": "medium",
        "convener_es": "La copia consigna convocatoria por correo certificado, pero la edición pública no identifica con seguridad a la persona convocante.",
        "convener_en": "The copy records notice by registered mail, but the public edition does not safely identify the individual convener.",
        "basis_es": "Reunión anterior a la transacción de activos anunciada en junio de 2008; trata de sustituir a Montelanza en la explotación mediante CEXP. Es una clasificación temporal/documental, no una imputación.",
        "basis_en": "The meeting predates the asset transaction reported for June 2008 and addresses replacing Montelanza in operation through CEXP. This is a temporal/documentary classification, not an accusation.",
        "phase_es": "Montelanza · fase previa a la venta de activos", "phase_en": "Montelanza · pre-asset-sale phase",
        "related": ["SP-ACTA-2008-07-15", "SP-ACTA-2008-07-25"],
    },
    {
        "id": "SP-ACTA-2008-07-15", "slug": "2008-07-15", "date": "2008-07-15", "record_type": "acta",
        "body": "owners", "title_es": "15 julio 2008 · Comunidad de Propietarios", "title_en": "15 July 2008 · Owners' Community",
        "perimeter": "mixed_or_contested", "attribution_status": "unresolved", "confidence": "low",
        "convener_es": "La copia identifica presidencia accidental y secretario-administrador, cuyos nombres se reservan en la edición pública; el convocante exacto no queda resuelto.",
        "convener_en": "The copy identifies an acting chair and secretary-administrator whose names are withheld in the public edition; the exact convener remains unresolved.",
        "basis_es": "La fecha es posterior al acuerdo de activos de junio de 2008, pero la fuente pública no permite asignar con seguridad la convocatoria al perímetro Multimatrix/LPB ni al perímetro histórico Montelanza.",
        "basis_en": "The date follows the June 2008 asset agreement, but the public source does not safely assign the call to either the Multimatrix/LPB lane or the historical Montelanza lane.",
        "phase_es": "Transición 2008 · atribución abierta", "phase_en": "2008 transition · attribution open",
        "related": ["SP-ACTA-2008-04-29", "SP-ACTA-2008-07-25"],
    },
    {
        "id": "SP-ACTA-2008-07-25", "slug": "2008-07-25", "date": "2008-07-25", "record_type": "acta",
        "body": "owners", "title_es": "25 julio 2008 · costes y explotación", "title_en": "25 July 2008 · costs and operation",
        "perimeter": "project_lpb_aweswell_gil", "attribution_status": "documented context; lineage label", "confidence": "medium",
        "convener_es": "La copia no cierra por sí sola la identidad formal del convocante; registra a la representante de LPB actuando también para CEXP.",
        "convener_en": "The copy does not by itself settle the formal convener's identity; it records LPB's representative also acting for CEXP.",
        "basis_es": "Registro posterior a la adquisición de activos en la fase Multimatrix/LPB. Se incluye en la sucesión del proyecto que después pasa a Aweswell/LPB; Gil no se presenta como director de esta reunión de 2008.",
        "basis_en": "Post-acquisition record from the Multimatrix/LPB phase. It is placed in the project succession later led through Aweswell/LPB; Gil is not presented as directing this 2008 meeting.",
        "phase_es": "Multimatrix/LPB · fase posterior a la compra", "phase_en": "Multimatrix/LPB · post-acquisition phase",
        "related": ["SP-ACTA-2008-07-15", "SP-ACTA-2009-05-28"],
    },
    {
        "id": "SP-ACTA-2008-12-17", "slug": "2008-12-17", "date": "2008-12-17", "record_type": "acta",
        "body": "owners", "title_es": "17 diciembre 2008 · Comunidad de Propietarios", "title_en": "17 December 2008 · Owners' Community",
        "perimeter": "mixed_or_contested", "attribution_status": "unresolved", "confidence": "low",
        "convener_es": "La copia identifica presidencia y secretaría accidental, pero sus nombres están expurgados y no se ha unido todavía la convocatoria fuente.",
        "convener_en": "The copy identifies a chair and acting secretary, but their names are redacted and the source notice has not yet been joined.",
        "basis_es": "La reunión cae en la fase LPB posterior a la compra, pero la copia pública no permite atribuir con seguridad la llamada a un perímetro concreto.",
        "basis_en": "The meeting falls in the post-acquisition LPB period, but the public copy does not safely attribute the call to a specific perimeter.",
        "phase_es": "Transición LPB 2008 · convocante abierto", "phase_en": "2008 LPB transition · convener open",
        "related": ["SP-ACTA-2008-07-25", "SP-ACTA-2009-05-28"],
    },
    {
        "id": "SP-ACTA-2009-05-28", "slug": "2009-05-28", "date": "2009-05-28", "record_type": "acta",
        "body": "owners", "title_es": "28 mayo 2009 · Comunidad de Propietarios", "title_en": "28 May 2009 · Owners' Community",
        "perimeter": "project_lpb_aweswell_gil", "attribution_status": "documented", "confidence": "high",
        "convener_es": "El ACTA consigna la reelección del presidente actuando en nombre y representación de LPB.",
        "convener_en": "The minutes record the re-election of the chair acting in the name and on behalf of LPB.",
        "basis_es": "Fuente de la fase Multimatrix/LPB; se integra en la continuidad patrimonial del proyecto que pasó en 2011 a Monterecco Sun Park Limited, después Aweswell. No atribuye a Gil una función en 2009.",
        "basis_en": "A Multimatrix/LPB-period source within the property-project continuity transferred in 2011 to Monterecco Sun Park Limited, later Aweswell. It does not attribute a 2009 role to Gil.",
        "phase_es": "Multimatrix/LPB · presidencia LPB documentada", "phase_en": "Multimatrix/LPB · documented LPB chair",
        "related": ["SP-ACTA-2008-12-17", "SP-ACTA-2011-02-02"],
    },
    {
        "id": "SP-ACTA-2011-02-02", "slug": "2011-02-02", "date": "2011-02-02", "record_type": "acta",
        "body": "owners", "title_es": "2 febrero 2011 · cambio de cargos comunitarios", "title_en": "2 February 2011 · Community office changes",
        "perimeter": "adverse_montelanza_molina", "attribution_status": "Gil attribution supported by office/representation record", "confidence": "medium",
        "convener_es": "La copia registra ausencia de presidente y secretario al inicio y elección de nuevos cargos durante la propia reunión; la convocatoria fuente completa permanece abierta.",
        "convener_en": "The copy records the chair and secretary absent at the outset and new officeholders elected during the meeting; the complete source notice remains open.",
        "basis_es": "Gil atribuye este cambio a la consolidación del perímetro adverso Montelanza/Molina–Comunidad. La fuente prueba el cambio de cargos y posiciones expresadas, no una finalidad ilícita ni una actuación conjunta de todos los propietarios.",
        "basis_en": "Gil attributes this change to consolidation of the adverse Montelanza/Molina–Community lane. The source proves office changes and recorded positions, not an unlawful purpose or joint conduct by all owners.",
        "phase_es": "Perímetro adverso alegado · Montelanza/Molina–Comunidad", "phase_en": "Alleged adverse perimeter · Montelanza/Molina–Community",
        "related": ["SP-ACTA-2009-05-28", "SP-ACTA-2011-06-22"],
    },
    {
        "id": "SP-ACTA-2011-06-22", "slug": "2011-06-22", "date": "2011-06-22", "record_type": "acta",
        "body": "owners", "title_es": "22 junio 2011 · deuda, voto y administración", "title_en": "22 June 2011 · debt, vote and administration",
        "perimeter": "adverse_montelanza_molina", "attribution_status": "Gil attribution; meeting roles documented", "confidence": "high",
        "convener_es": "El ACTA consigna convocatoria por la presidenta y actuación de Francisco Mario Matos Matas como administrador.",
        "convener_en": "The minutes record notice by the chair and Francisco Mario Matos Matas acting as administrator.",
        "basis_es": "Nodo documental central del perímetro Comunidad/Pamanil que Gil vincula con Montelanza/Molina: deuda, exclusión de voto, administración, litigios y propuesta Pamanil. La vinculación y criminalidad siguen siendo alegaciones a probar acto por acto.",
        "basis_en": "Central document node in the Community/Pamanil lane Gil associates with Montelanza/Molina: debt, voting exclusion, administration, litigation and the Pamanil proposal. Alignment and criminality remain allegations requiring act-by-act proof.",
        "phase_es": "Perímetro adverso alegado · Montelanza/Molina–Pamanil", "phase_en": "Alleged adverse perimeter · Montelanza/Molina–Pamanil",
        "related": ["SP-ACTA-2011-02-02", "SP-ACTA-2012-08-10"],
    },
    {
        "id": "SP-ACTA-2012-08-10", "slug": "2012-08-10", "date": "2012-08-10", "record_type": "acta",
        "body": "owners", "title_es": "10 agosto 2012 · reunión LPB/Gil controvertida", "title_en": "10 August 2012 · contested LPB/Gil meeting",
        "perimeter": "project_lpb_aweswell_gil", "attribution_status": "documented; validity contested", "confidence": "high",
        "convener_es": "La copia registra al presidente exponiendo la reanudación de funciones; la firma final identifica a LPB y Gil Marer. Oponentes presentes calificaron la convocatoria de ilegal.",
        "convener_en": "The copy records the chair explaining resumed functions; the closing signature block identifies LPB and Gil Marer. Attending opponents called the notice unlawful.",
        "basis_es": "Reunión del carril LPB/Gil posterior a la adquisición de LPB por Monterecco Sun Park Limited (después Aweswell). La copia afirma que no se sometió acuerdo a votación y conserva la objeción adversa.",
        "basis_en": "A meeting in the LPB/Gil lane after Monterecco Sun Park Limited (later Aweswell) acquired LPB. The copy says no resolution was put to a vote and preserves the adverse objection.",
        "phase_es": "Aweswell/LPB · liderazgo de Gil · controvertida", "phase_en": "Aweswell/LPB · Gil-led · contested",
        "related": ["SP-ACTA-2011-06-22", "SP-ACTA-2014-04-10"],
    },
    {
        "id": "SP-ACTA-2014-04-10", "slug": "2014-04-10", "date": "2014-04-10", "record_type": "acta-source-gap",
        "body": "owners", "status": "located-package-partial", "title_es": "10 abril 2014 · junta competidora LPB/Gil", "title_en": "10 April 2014 · competing LPB/Gil meeting",
        "perimeter": "project_lpb_aweswell_gil", "attribution_status": "documented through controlled dossier; source package incomplete", "confidence": "high",
        "convener_es": "El registro controlado identifica una convocatoria/junta promovida por LPB/Gil y un acta notarial; el paquete primario público íntegro sigue pendiente.",
        "convener_en": "The controlled record identifies an LPB/Gil-promoted call/meeting and a notarial record; the complete public primary package remains pending.",
        "basis_es": "Carril de gobernanza alternativo LPB/Gil. La suspensión cautelar posterior en PO 562/2014 y las impugnaciones deben acompañar cualquier uso de esta reunión.",
        "basis_en": "Alternative LPB/Gil governance lane. The later interim suspension in PO 562/2014 and challenges must accompany any use of this meeting.",
        "phase_es": "Aweswell/LPB · liderazgo de Gil · impugnada", "phase_en": "Aweswell/LPB · Gil-led · challenged",
        "notes_es": "Existe una fuente notarial controlada, pero este lote no contiene todavía un paquete público completo de OCR, facsímil y páginas.",
        "notes_en": "A controlled notarial source exists, but this release does not yet contain its complete public OCR, facsimile and page package.",
        "related": ["SP-ACTA-2012-08-10", "SP-ACTA-2014-08-28-CP"],
    },
    {
        "id": "SP-ACTA-2014-08-28-CP", "slug": "2014-08-28-cp", "date": "2014-08-28", "record_type": "acta",
        "body": "owners", "title_es": "28 agosto 2014 · Comunidad bajo presidencia LPB", "title_en": "28 August 2014 · Community under LPB chair",
        "perimeter": "project_lpb_aweswell_gil", "attribution_status": "documented; validity disputed", "confidence": "high",
        "convener_es": "El ACTA identifica la presidencia de LPB, representada por su administrador, y una convocatoria previa de 8 de agosto.",
        "convener_en": "The minutes identify LPB as chair, represented by its director, and a prior notice dated 8 August.",
        "basis_es": "Registro del carril Aweswell/LPB–Gil, separado del acta CEXP del mismo día. El propio texto discute la reunión competidora de abril y la autoridad Pamanil.",
        "basis_en": "An Aweswell/LPB–Gil lane record, separate from the CEXP minutes of the same date. Its own text addresses the competing April meeting and Pamanil authority.",
        "phase_es": "Aweswell/LPB · liderazgo de Gil", "phase_en": "Aweswell/LPB · Gil-led",
        "related": ["SP-ACTA-2014-04-10", "SP-ACTA-2014-08-28-CEXP", "SP-ACTA-2015-11-19"],
    },
    {
        "id": "SP-ACTA-2014-08-28-CEXP", "slug": "2014-08-28-cexp", "date": "2014-08-28", "record_type": "acta",
        "body": "cexp", "title_es": "28 agosto 2014 · ACTA CEXP", "title_en": "28 August 2014 · CEXP minutes",
        "perimeter": "project_lpb_aweswell_gil", "attribution_status": "documented", "confidence": "high",
        "convener_es": "ACTA de la Junta General de CEXP celebrada en Sun Park; los nombres y firmas se protegen en la edición pública.",
        "convener_en": "Minutes of the CEXP General Meeting held at Sun Park; names and signatures are protected in the public edition.",
        "basis_es": "Carril CEXP del proyecto Aweswell/LPB–Gil. No es una junta de la Comunidad de Propietarios y no prueba por sí sola posesión u operación efectiva.",
        "basis_en": "The CEXP lane of the Aweswell/LPB–Gil project. It is not an Owners' Community meeting and does not by itself prove effective possession or operation.",
        "phase_es": "CEXP · perímetro del proyecto Aweswell/LPB", "phase_en": "CEXP · Aweswell/LPB project perimeter",
        "related": ["SP-ACTA-2014-08-28-CP", "SP-ACTA-2017-04-07-CEXP"],
    },
    {
        "id": "SP-ACTA-2015-11-19", "slug": "2015-11-19", "date": "2015-11-19", "record_type": "acta",
        "body": "owners", "title_es": "19 noviembre 2015 · Comunidad/Pamanil", "title_en": "19 November 2015 · Community/Pamanil",
        "perimeter": "adverse_montelanza_molina", "attribution_status": "Gil attribution; officeholders documented", "confidence": "high",
        "convener_es": "El ACTA identifica a Asunción Aizpurúa Sánchez como presidenta y a Francisco Matos Matas como administrador; registra seguridad contratada a propuesta de la presidenta.",
        "convener_en": "The minutes identify Asunción Aizpurúa Sánchez as chair and Francisco Matos Matas as administrator; they record security hired at the chair's proposal.",
        "basis_es": "Pertenece al carril Comunidad/Pamanil que Gil atribuye al perímetro adverso Montelanza/Molina. La presencia y objeciones de Gil/LPB no convierten la reunión en una reunión promovida por su perímetro.",
        "basis_en": "It belongs to the Community/Pamanil lane Gil attributes to the adverse Montelanza/Molina perimeter. Gil/LPB's attendance and objections do not make it a meeting promoted by his perimeter.",
        "phase_es": "Perímetro adverso alegado · Montelanza/Molina–Pamanil", "phase_en": "Alleged adverse perimeter · Montelanza/Molina–Pamanil",
        "related": ["SP-ACTA-2014-08-28-CP", "SP-ACTA-2016-04-26"],
    },
    {
        "id": "SP-ACTA-2016-04-26", "slug": "2016-04-26", "date": "2016-04-26", "record_type": "acta",
        "body": "owners", "title_es": "26 abril 2016 · Comunidad/Pamanil", "title_en": "26 April 2016 · Community/Pamanil",
        "perimeter": "adverse_montelanza_molina", "attribution_status": "Gil attribution; officeholders documented", "confidence": "high",
        "convener_es": "El ACTA identifica a Asunción Aizpurúa Sánchez como presidenta y a Francisco Matos Matas como administrador; la cadena de convocatoria de 15–20 abril está registrada por separado.",
        "convener_en": "The minutes identify Asunción Aizpurúa Sánchez as chair and Francisco Matos Matas as administrator; the 15–20 April notice chain is separately registered.",
        "basis_es": "Carril Comunidad/Pamanil atribuido por Gil al perímetro adverso Montelanza/Molina. El acta contiene la versión de ese órgano, el historial litigioso y las objeciones LPB; no adjudica criminalidad.",
        "basis_en": "Community/Pamanil lane attributed by Gil to the adverse Montelanza/Molina perimeter. The minutes contain that body's account, litigation history and LPB objections; they do not adjudicate criminality.",
        "phase_es": "Perímetro adverso alegado · Montelanza/Molina–Pamanil", "phase_en": "Alleged adverse perimeter · Montelanza/Molina–Pamanil",
        "related": ["SP-ACTA-2015-11-19", "SP-MEETING-2016-06-11", "SP-ACTA-2017-06-12"],
    },
    {
        "id": "SP-MEETING-2016-06-11", "slug": "2016-06-11-working-meeting", "date": "2016-06-11", "record_type": "working-meeting",
        "body": "event", "status": "non-acta-event", "title_es": "11 junio 2016 · reunión profesional de trabajo", "title_en": "11 June 2016 · professional working meeting",
        "perimeter": "mixed_or_contested", "attribution_status": "mixed attendance; initiator/capacities incomplete", "confidence": "medium",
        "convener_es": "Reunión de trabajo del carril LPB/asesores con participación o interlocución del administrador comunitario; convocante, asistentes y capacidades requieren cierre desde audio y correos.",
        "convener_en": "A working meeting in the LPB/adviser lane involving or addressing the Community administrator; convener, attendees and capacities require closure from the audio and emails.",
        "basis_es": "No es ACTA ni reunión de órgano. La asistencia cruza los dos perímetros y por ello se marca mixta, sin convertir conocimiento profesional en alineación o responsabilidad.",
        "basis_en": "It is neither minutes nor an organ meeting. Attendance crosses the two perimeters, so it is marked mixed without turning professional knowledge into alignment or responsibility.",
        "phase_es": "Reunión mixta · LPB/asesores y Comunidad", "phase_en": "Mixed meeting · LPB/advisers and Community",
        "notes_es": "Grabación de trabajo registrada. No pertenece al libro de actas de la Comunidad ni al de CEXP; el audio/transcripción aprobada y el mapa de capacidades siguen pendientes.",
        "notes_en": "Recorded working session. It belongs in neither the Owners' Community nor CEXP minutes book; native audio/approved transcript and the capacity map remain pending.",
        "related": ["SP-ACTA-2016-04-26", "SP-ACTA-2017-04-07-CEXP"],
    },
    {
        "id": "SP-ACTA-2017-04-07-CEXP", "slug": "2017-04-07-cexp", "date": "2017-04-07", "record_type": "acta",
        "body": "cexp", "title_es": "7 abril 2017 · ACTA CEXP", "title_en": "7 April 2017 · CEXP minutes",
        "perimeter": "project_lpb_aweswell_gil", "attribution_status": "documented", "confidence": "high",
        "convener_es": "ACTA firmada de la Junta General de CEXP celebrada en Sun Park; los identificadores personales se protegen públicamente.",
        "convener_en": "Signed minutes of the CEXP General Meeting held at Sun Park; personal identifiers are publicly protected.",
        "basis_es": "Carril CEXP del proyecto Aweswell/LPB–Gil, separado de la Comunidad de Propietarios y de su junta de junio de 2017.",
        "basis_en": "The CEXP lane of the Aweswell/LPB–Gil project, separate from the Owners' Community and its June 2017 meeting.",
        "phase_es": "CEXP · perímetro del proyecto Aweswell/LPB", "phase_en": "CEXP · Aweswell/LPB project perimeter",
        "related": ["SP-ACTA-2014-08-28-CEXP", "SP-ACTA-2017-06-12"],
    },
    {
        "id": "SP-ACTA-2017-06-12", "slug": "2017-06-12", "date": "2017-06-12", "record_type": "acta",
        "body": "owners", "title_es": "12 junio 2017 · Comunidad/Pamanil", "title_en": "12 June 2017 · Community/Pamanil",
        "perimeter": "adverse_montelanza_molina", "attribution_status": "Gil attribution; continuity documented", "confidence": "high",
        "convener_es": "El ACTA registra presidencia, administrador, abogados/asesores comunitarios y elección de cargos; los nombres privados expurgados se conservan en la fuente de custodia.",
        "convener_en": "The minutes record the chair, administrator, Community lawyers/advisers and office elections; redacted private names remain in the custody source.",
        "basis_es": "Continuidad del carril Comunidad/Pamanil que Gil atribuye al perímetro Montelanza/Molina antes de la fase Acosta Matos.",
        "basis_en": "Continuation of the Community/Pamanil lane Gil attributes to the Montelanza/Molina perimeter before the Acosta Matos phase.",
        "phase_es": "Perímetro adverso alegado · Montelanza/Molina–Pamanil", "phase_en": "Alleged adverse perimeter · Montelanza/Molina–Pamanil",
        "related": ["SP-ACTA-2016-04-26", "SP-ACTA-2018-05-18"],
    },
    {
        "id": "SP-ACTA-2018-05-18", "slug": "2018-05-18", "date": "2018-05-18", "record_type": "acta",
        "body": "owners", "title_es": "18 mayo 2018 · seguridad/acceso", "title_en": "18 May 2018 · security/access",
        "perimeter": "adverse_acosta_matos", "attribution_status": "Gil attribution; CAM/Community facts documented", "confidence": "high",
        "convener_es": "ACTA comunitaria bajo los cargos del carril Pamanil; registra presencia CAM, deuda/voto y una propuesta de seguridad/acceso vinculada a solicitudes de LPB/AC.",
        "convener_en": "Community minutes under the Pamanil-lane officeholders; they record CAM presence, debt/vote and a security/access proposal linked to LPB/insolvency-administrator requests.",
        "basis_es": "Primer ACTA localizada de la fase Comunidad/CAM–Acosta Matos en la cadena de acceso. Gil la atribuye al perímetro adverso; la fuente no demuestra por sí sola toma total, título, exceso ni intención penal.",
        "basis_en": "The first located minutes in the Community/CAM–Acosta Matos access phase. Gil attributes it to the adverse perimeter; the source alone does not prove total takeover, title, excess or criminal intent.",
        "phase_es": "Perímetro adverso alegado · fase Acosta Matos/CAM", "phase_en": "Alleged adverse perimeter · Acosta Matos/CAM phase",
        "related": ["SP-ACTA-2017-06-12", "SP-ACTA-2018-07-05", "SP-RECITAL-2018-11-20"],
    },
    {
        "id": "SP-ACTA-2018-07-05", "slug": "2018-07-05", "date": "2018-07-05", "record_type": "acta",
        "body": "owners", "title_es": "5 julio 2018 · control material y litigios", "title_en": "5 July 2018 · material control and litigation",
        "perimeter": "adverse_acosta_matos", "attribution_status": "Gil attribution; CAM role recorded", "confidence": "high",
        "convener_es": "ACTA de la Comunidad posterior al evento de 7 junio; registra actuaciones, denuncia de Gil, costes y funciones de CAM/órganos comunitarios.",
        "convener_en": "Owners' Community minutes after the 7 June event; they record actions, Gil's complaint, costs and CAM/Community-organ functions.",
        "basis_es": "Carril Comunidad/CAM–Acosta Matos que Gil atribuye al perímetro adverso. Sus afirmaciones son versión de la fuente y deben confrontarse con DP 1132/2018, AP 804/2018 y los registros materiales.",
        "basis_en": "Community/CAM–Acosta Matos lane attributed by Gil to the adverse perimeter. Its statements are the source's account and must be tested against DP 1132/2018, AP 804/2018 and material records.",
        "phase_es": "Perímetro adverso alegado · fase Acosta Matos/CAM", "phase_en": "Alleged adverse perimeter · Acosta Matos/CAM phase",
        "related": ["SP-ACTA-2018-05-18", "SP-RECITAL-2018-11-20", "SP-ACTA-2022-02-04"],
    },
    {
        "id": "SP-RECITAL-2018-11-20", "slug": "2018-11-20-recital", "date": "2018-11-20", "record_type": "later-recital",
        "body": "reference", "status": "referenced-original-not-located", "title_es": "20 noviembre 2018 · reunión mencionada posteriormente", "title_en": "20 November 2018 · later-recited meeting",
        "perimeter": "unresolved", "attribution_status": "later recital only", "confidence": "low",
        "convener_es": "No se ha localizado convocatoria ni ACTA independiente. La existencia y contenido sólo aparecen referidos en el ACTA de 4 febrero 2022.",
        "convener_en": "No independent notice or minutes have been located. The event and its content appear only as a recital in the 4 February 2022 minutes.",
        "basis_es": "La mención procede de una fuente de la fase Acosta Matos, pero eso no prueba quién convocó la reunión de 2018 ni su asistencia, votación, texto o validez.",
        "basis_en": "The recital comes from an Acosta Matos-era source, but that does not prove who called the 2018 meeting or its attendance, vote, wording or validity.",
        "phase_es": "Atribución no resuelta · sólo mención de 2022", "phase_en": "Unresolved attribution · 2022 recital only",
        "notes_es": "El original independiente sigue sin localizarse. Esta página evita que la mención posterior se convierta silenciosamente en ACTA.",
        "notes_en": "The independent original remains unlocated. This page prevents a later recital from silently becoming minutes.",
        "related": ["SP-ACTA-2018-05-18", "SP-ACTA-2018-07-05", "SP-ACTA-2022-02-04"],
    },
    {
        "id": "SP-ACTA-2022-02-04", "slug": "2022-02-04", "date": "2022-02-04", "record_type": "acta",
        "body": "owners", "title_es": "4 febrero 2022 · proyecto y explotación unitaria", "title_en": "4 February 2022 · project and unitary operation",
        "perimeter": "adverse_acosta_matos", "attribution_status": "Gil attribution; CAM/officeholder role documented", "confidence": "high",
        "convener_es": "ACTA comunitaria que registra intervenciones de José Daniel Acosta Matos, un proyecto aportado por CAM y autorizaciones al presidente; convocatoria, poderes y abstenciones completas siguen abiertos.",
        "convener_en": "Community minutes recording interventions by José Daniel Acosta Matos, a CAM-supplied project and authorisations to the chair; complete notice, proxies and abstentions remain open.",
        "basis_es": "Fuente de la fase Acosta Matos/CAM–Comunidad. Gil la atribuye al perímetro adverso y cuestiona autoridad, voto y conflicto; el ACTA no convierte esas alegaciones en hallazgos ni prueba por sí sola financiación o licencia válida.",
        "basis_en": "An Acosta Matos/CAM–Community phase source. Gil attributes it to the adverse perimeter and challenges authority, voting and conflict; the minutes do not turn those allegations into findings or by themselves prove valid finance or licensing.",
        "phase_es": "Perímetro adverso alegado · fase Acosta Matos/CAM", "phase_en": "Alleged adverse perimeter · Acosta Matos/CAM phase",
        "related": ["SP-ACTA-2018-07-05", "SP-RECITAL-2018-11-20"],
    },
]


PERIMETERS = {
    "pre_sale_montelanza": {
        "label_es": "Montelanza · pre-venta", "label_en": "Montelanza · pre-sale",
        "definition_es": "Registro anterior a la transacción de activos anunciada en junio de 2008.",
        "definition_en": "Record predating the asset transaction reported for June 2008.",
    },
    "project_lpb_aweswell_gil": {
        "label_es": "Proyecto · Multimatrix/LPB → Aweswell/LPB–Gil", "label_en": "Project · Multimatrix/LPB → Aweswell/LPB–Gil",
        "definition_es": "Sucesión del lado del proyecto. La etiqueta no atribuye a Gil actos anteriores a su entrada documentada.",
        "definition_en": "Project-side succession. The label does not attribute acts to Gil before his documented entry.",
    },
    "adverse_montelanza_molina": {
        "label_es": "Adverso alegado · Montelanza/Molina–Pamanil", "label_en": "Alleged adverse · Montelanza/Molina–Pamanil",
        "definition_es": "Alineación atribuida por Gil; los cargos, representaciones y actos concretos se prueban por separado.",
        "definition_en": "Alignment attributed by Gil; specific offices, representations and acts are proved separately.",
    },
    "adverse_acosta_matos": {
        "label_es": "Adverso alegado · Acosta Matos/CAM", "label_en": "Alleged adverse · Acosta Matos/CAM",
        "definition_es": "Fase posterior atribuida por Gil; no es una declaración judicial de actuación conjunta o culpabilidad.",
        "definition_en": "Later phase attributed by Gil; not a judicial finding of joint conduct or guilt.",
    },
    "mixed_or_contested": {
        "label_es": "Mixto o controvertido", "label_en": "Mixed or contested",
        "definition_es": "La fuente cruza perímetros o no permite resolver el convocante/alineación con seguridad.",
        "definition_en": "The source crosses perimeters or does not safely resolve convener/alignment.",
    },
    "unresolved": {
        "label_es": "No resuelto", "label_en": "Unresolved",
        "definition_es": "Fuente o atribución insuficiente; no se fuerza una clasificación.",
        "definition_en": "Insufficient source or attribution; no classification is forced.",
    },
}


def root_href(path: str) -> str:
    return "../../../../" + path.lstrip("/")


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def title_for(event: dict, locale: str) -> str:
    return event.get(f"title_{locale}") or event.get("id", "ACTA")


def event_page(event: dict, locale: str, all_events: list[dict], index: int) -> str:
    es = locale == "es"
    title = title_for(event, locale)
    perimeter = PERIMETERS[event["perimeter"]]
    detail_other = event["detail_page_en" if es else "detail_page_es"]
    transcript = event.get("transcript_path") or event.get("transcript_source")
    source_images = event.get("source_preview_pages", [])
    notes = event.get("notes_es" if es else "notes_en", "")
    full_text = ""
    if transcript and (REPO / transcript).is_file():
        full_text = (REPO / transcript).read_text(encoding="utf-8")
        # Keep the source transcript linked verbatim, but do not propagate a
        # known OCR-created legal-entity alias into reader-facing HTML.
        full_text = re.sub(
            r"(?i)LUCHI\s+PLAYA\s+BLANCA\s+SAU\.?,?",
            "LUCHY PLAYA BLANCA, S.L.U. [NOMBRE LEGAL NORMALIZADO DESDE OCR BORROSO]",
            full_text,
        )
    actions = []
    labels = {
        "transcript": "Abrir Markdown OCR" if es else "Open OCR Markdown",
        "pdf": "PDF de edición textual" if es else "Text-edition PDF",
        "facsimile": "Facsímil fuente expurgado" if es else "Redacted source facsimile",
        "manifest": "Manifiesto de integridad" if es else "Integrity manifest",
        "provenance": "Procedencia" if es else "Provenance",
        "redactions": "Registro de expurgación" if es else "Redaction log",
    }
    for key, label in (
        ("transcript_path", labels["transcript"]),
        ("public_pdf_path", labels["pdf"]),
        ("redacted_source_facsimile", labels["facsimile"]),
        ("manifest_path", labels["manifest"]),
        ("provenance_path", labels["provenance"]),
        ("redaction_log_path", labels["redactions"]),
    ):
        if event.get(key):
            actions.append(f'<a class="button secondary" href="{h(root_href(event[key]))}">{h(label)}</a>')

    gallery = ""
    if source_images:
        cards = []
        for page_no, path in enumerate(source_images, 1):
            label = f"Página fuente {page_no}" if es else f"Source page {page_no}"
            cards.append(
                f'<a class="acta-source-page" href="{h(root_href(path))}">'
                f'<img loading="lazy" decoding="async" src="{h(root_href(path))}" alt="{h(title)}, {h(label)}">'
                f'<span>{h(label)}</span></a>'
            )
        gallery = (
            f'<section class="section alt" id="paginas-fuente"><div class="shell">'
            f'<div class="section-head"><div><p class="kicker">{"Facsímil página por página" if es else "Page-by-page facsimile"}</p>'
            f'<h2>{"Todas las páginas fuente públicas expurgadas." if es else "Every public redacted source page."}</h2></div>'
            f'<p>{"Las imágenes son derivados rasterizados irreversiblemente expurgados; no son el original ni una copia certificada." if es else "The images are irreversibly redacted raster derivatives; they are neither the original nor a certified copy."}</p></div>'
            f'<div class="acta-source-gallery">{"".join(cards)}</div></div></section>'
        )

    text_section = ""
    if full_text:
        text_section = (
            f'<section class="section" id="texto-ocr"><div class="shell acta-event-narrow">'
            f'<div class="section-head"><div><p class="kicker">{"Texto fuente completo publicado" if es else "Full published source text"}</p>'
            f'<h2>{"OCR secuenciado por página, con redacciones visibles." if es else "Page-sequenced OCR with visible redactions."}</h2></div>'
            f'<p>{"No es transcripción pericial ni cotejo línea por línea. Los marcadores conservan la posición de material reservado o ilegible; una grafía OCR incompatible con una entidad jurídica controlada se normaliza y se marca." if es else "This is not an expert transcription or line-by-line certification. Markers preserve withheld or illegible material; an OCR spelling incompatible with a controlled legal entity is normalised and marked."}</p></div>'
            f'<pre class="acta-full-ocr" lang="es">{h(full_text)}</pre></div></section>'
        )
    else:
        text_section = (
            f'<section class="section" id="texto-ocr"><div class="shell acta-event-narrow"><div class="acta-source-gap">'
            f'<strong>{"Paquete fuente completo pendiente" if es else "Complete source package pending"}</strong>'
            f'<p>{h(notes or ("No hay OCR/facsímil público para este evento." if es else "No public OCR/facsimile exists for this event."))}</p>'
            f'</div></div></section>'
        )

    by_id = {item["id"]: item for item in all_events}
    related = []
    for event_id in event.get("related", []):
        item = by_id.get(event_id)
        if item:
            related.append(f'<li><a href="{h(root_href(item["detail_page_es" if es else "detail_page_en"]))}">{h(title_for(item, locale))}</a></li>')
    previous = all_events[index - 1] if index > 0 else None
    following = all_events[index + 1] if index + 1 < len(all_events) else None
    nav_links = []
    if previous:
        nav_links.append(f'<a href="{h(root_href(previous["detail_page_es" if es else "detail_page_en"]))}">← {h(title_for(previous, locale))}</a>')
    if following:
        nav_links.append(f'<a href="{h(root_href(following["detail_page_es" if es else "detail_page_en"]))}">{h(title_for(following, locale))} →</a>')

    canonical = f'{BASE_URL}/{event["detail_page_es" if es else "detail_page_en"].removesuffix("index.html")}'
    other_url = f'{BASE_URL}/{detail_other.removesuffix("index.html")}'
    room = "es/comunidad-instrumentalizacion/sala-documental-actas/" if es else "en/community-instrumentalisation/acta-document-room/"
    chronology = "es/comunidad-instrumentalizacion/actas-2011-2022/" if es else "en/community-instrumentalisation/minutes-2011-2022/"
    lang_label = "English" if es else "Español"
    classification = perimeter["label_es" if es else "label_en"]
    definition = perimeter["definition_es" if es else "definition_en"]
    status_label = {
        "documented": "Documentado" if es else "Documented",
        "record": "Registro" if es else "Record",
    }
    return f'''<!doctype html>
<html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{h(title)} | {"Sala documental ACTAS Sun Park" if es else "Sun Park ACTA document room"}</title>
<meta name="description" content="{h(("Página individual de ACTA/reunión con perímetro, convocante, OCR completo, facsímil e interconexiones probatorias." if es else "Individual ACTA/meeting page with perimeter, convener, full OCR, facsimile and evidence links."))}">
<link rel="canonical" href="{h(canonical)}"><link rel="alternate" hreflang="{locale}" href="{h(canonical)}"><link rel="alternate" hreflang="{'en' if es else 'es'}" href="{h(other_url)}">
<link rel="stylesheet" href="../../../../assets/styles.css"><link rel="stylesheet" href="../../../../assets/acta-document-room-20260822.css"><script src="../../../../assets/site.js" defer></script></head>
<body class="dossier-page acta-event-page" data-perimeter="{h(event['perimeter'])}"><a class="skip-link" href="#ficha">{"Saltar a la ficha" if es else "Skip to record"}</a>
<header class="site-header"><div class="shell header-inner"><a class="brand" href="{h(root_href(room))}"><span class="brand-mark">SR</span><span class="brand-copy"><strong>Project Sun Rock</strong><small>{"Sala ACTAS" if es else "ACTA room"}</small></span></a><nav class="main-nav"><a href="{h(root_href(room))}">{"Todas las reuniones" if es else "All meetings"}</a><a href="{h(root_href(chronology))}">{"Cronología" if es else "Chronology"}</a><a href="#texto-ocr">OCR</a><a href="#paginas-fuente">{"Páginas" if es else "Pages"}</a><a class="language-link" href="{h(root_href(detail_other))}">{lang_label}</a></nav></div></header>
<main><section class="acta-event-hero"><div class="shell acta-event-hero-grid"><div><p class="eyebrow">{h(event['id'])} · {h(event['date'])}</p><h1>{h(title)}</h1><p class="lead">{h(event['phase_es' if es else 'phase_en'])}</p><div class="acta-perimeter-ribbon" data-perimeter="{h(event['perimeter'])}"><strong>{h(classification)}</strong><span>{h(definition)}</span></div></div><aside class="acta-room-rule"><strong>{"Regla de atribución" if es else "Attribution rule"}</strong><span>{"El color distingue carriles documentales. No acredita por sí solo convocatoria, validez, actuación conjunta, fraude o culpabilidad." if es else "Colour distinguishes documentary lanes. It does not itself prove convocation, validity, joint conduct, fraud or guilt."}</span></aside></div></section>
<section class="section" id="ficha"><div class="shell acta-event-narrow"><div class="acta-fact-grid"><article><span>{"Órgano / tipo" if es else "Body / type"}</span><strong>{h(event.get('body', '—'))} · {h(event.get('record_type', '—'))}</strong></article><article><span>{"Estado de atribución" if es else "Attribution status"}</span><strong>{h(event['attribution_status'])} · {h(event['confidence'])}</strong></article></div><article class="acta-convener"><h2>{"Quién convocó o generó el registro" if es else "Who called or generated the record"}</h2><p>{h(event['convener_es' if es else 'convener_en'])}</p></article><article class="acta-basis"><h2>{"Base de la clasificación" if es else "Classification basis"}</h2><p>{h(event['basis_es' if es else 'basis_en'])}</p></article><div class="actions">{''.join(actions)}</div><p class="source-note"><strong>{"Límite" if es else "Boundary"}:</strong> {h(notes)}</p></div></section>
{text_section}{gallery}
<section class="section" id="interlinks"><div class="shell acta-event-narrow"><div class="section-head"><div><p class="kicker">{"Continuidad" if es else "Continuity"}</p><h2>{"Registros relacionados y navegación temporal." if es else "Related records and chronological navigation."}</h2></div></div><ul class="acta-related">{''.join(related)}</ul><nav class="acta-prev-next" aria-label="{"ACTAS anterior y siguiente" if es else "Previous and next ACTA"}">{''.join(nav_links)}</nav><p><a href="{h(root_href(room))}">← {"Volver a la sala documental completa" if es else "Return to the complete document room"}</a></p></div></section></main>
<aside class="disclaimer"><div class="shell"><p><strong>{"Aviso" if es else "Notice"}:</strong> {"La publicación acredita el contenido de una copia localizada, no la verdad, validez, ejecución ni intención delictiva. Las alineaciones adversas son atribuciones de Gil Marer salvo que se indique un hecho documental concreto." if es else "Publication establishes what a located copy records, not truth, validity, implementation or criminal intent. Adverse alignment is attributed to Gil Marer unless a specific documentary fact is stated."}</p></div></aside>
<footer class="site-footer"><div class="shell"><p>Project Sun Rock · {"registro ACTAS y reuniones" if es else "ACTA and meeting register"} · 27 August 2026</p></div></footer></body></html>'''


def update_sitemap(events: list[dict]) -> None:
    path = REPO / "sitemap.xml"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    additions: list[str] = []
    for event in events:
        es_url = f"{BASE_URL}/{event['detail_page_es'].removesuffix('index.html')}"
        en_url = f"{BASE_URL}/{event['detail_page_en'].removesuffix('index.html')}"
        for url in (es_url, en_url):
            if f"<loc>{url}</loc>" in text:
                continue
            additions.append(
                "  <url>\n"
                f"    <loc>{url}</loc><lastmod>2026-08-27</lastmod>\n"
                f"    <xhtml:link rel=\"alternate\" hreflang=\"es\" href=\"{es_url}\"/>\n"
                f"    <xhtml:link rel=\"alternate\" hreflang=\"en\" href=\"{en_url}\"/>\n"
                f"    <xhtml:link rel=\"alternate\" hreflang=\"x-default\" href=\"{es_url}\"/>\n"
                "  </url>"
            )
    if additions:
        text = text.replace("</urlset>", "\n" + "\n".join(additions) + "\n</urlset>")
        path.write_text(text, encoding="utf-8")


def update_chronology(events: list[dict], locale: str) -> None:
    es = locale == "es"
    path = REPO / (
        "es/comunidad-instrumentalizacion/actas-2011-2022/index.html"
        if es else "en/community-instrumentalisation/minutes-2011-2022/index.html"
    )
    text = path.read_text(encoding="utf-8")
    css = '<link rel="stylesheet" href="../../../assets/acta-document-room-20260822.css">'
    if css not in text:
        text = text.replace('<link rel="stylesheet" href="../../../assets/ric-pressure.css">', '<link rel="stylesheet" href="../../../assets/ric-pressure.css">\n  ' + css)
    cards = []
    for event in events:
        route = event["detail_page_es" if es else "detail_page_en"]
        label = PERIMETERS[event["perimeter"]]["label_es" if es else "label_en"]
        cards.append(
            f'<article class="acta-perimeter-chip" data-perimeter="{h(event["perimeter"])}">'
            f'<strong>{h(event["date"])} · {h(title_for(event, locale))}</strong>'
            f'<span>{h(label)} · <a href="{h("../../../" + route)}">{"abrir ficha completa" if es else "open complete record"} →</a></span></article>'
        )
    block = (
        '<!-- ACTA-LINEAGE-LINKS:START -->'
        f'<section class="section" id="meeting-lineage"><div class="shell"><div class="section-head"><div>'
        f'<p class="kicker">{"Mapa de convocatoria y perímetro" if es else "Convener and perimeter map"}</p>'
        f'<h2>{"Cada reunión y ACTA tiene ficha propia." if es else "Every meeting and ACTA has its own page."}</h2></div>'
        f'<p>{"El color distingue la fase documental, mientras la ficha separa convocante, órgano, atribución, fuente, OCR, facsímil e interconexiones. Una clasificación adversa es la posición atribuida de Gil, no un fallo de culpabilidad." if es else "Colour distinguishes the documentary phase, while each page separates convener, body, attribution, source, OCR, facsimile and interlinks. An adverse classification is Gil’s attributed position, not a finding of guilt."}</p></div>'
        f'<div class="acta-perimeter-legend">{"".join(cards)}</div></div></section>'
        '<!-- ACTA-LINEAGE-LINKS:END -->'
    )
    pattern = re.compile(r'<!-- ACTA-LINEAGE-LINKS:START -->.*?<!-- ACTA-LINEAGE-LINKS:END -->', re.S)
    if pattern.search(text):
        text = pattern.sub(block, text)
    else:
        text = text.replace('</main>', block + '\n  </main>', 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    public = json.loads(INDEX.read_text(encoding="utf-8"))
    public_by_id = {event["id"]: event for event in public["events"]}
    merged: list[dict] = []
    for order, configured in enumerate(EVENTS, 1):
        event = dict(public_by_id.get(configured["id"], {}))
        event.update(configured)
        event["order"] = order
        event["detail_page_es"] = f"es/comunidad-instrumentalizacion/sala-documental-actas/{event['slug']}/index.html"
        event["detail_page_en"] = f"en/community-instrumentalisation/acta-document-room/{event['slug']}/index.html"
        event["notes_es"] = configured.get("notes_es") or event.get("source_variant_note_es") or event.get("notes_es", "")
        event["notes_en"] = configured.get("notes_en") or event.get("source_variant_note_en") or event.get("notes_en", "")
        merged.append(event)

    payload = {
        "schema_version": "1.0",
        "generated": "2026-08-27",
        "scope": "Twenty controlled ACTA/meeting events with separate convener, body, attributed perimeter, confidence, full public-artifact links and bilingual event pages.",
        "classification_boundary": "Perimeter colour is an editorial/documentary attribution. It is not proof of validity, joint action, criminality or guilt.",
        "perimeters": PERIMETERS,
        "events": merged,
    }
    LINEAGE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for index, event in enumerate(merged):
        for locale, key in (("es", "detail_page_es"), ("en", "detail_page_en")):
            target = REPO / event[key]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(event_page(event, locale, merged, index), encoding="utf-8")
    update_chronology(merged, "es")
    update_chronology(merged, "en")
    update_sitemap(merged)
    print(f"Built {len(merged)} lineage events, {len(merged) * 2} pages and {LINEAGE.relative_to(REPO)}")


if __name__ == "__main__":
    main()

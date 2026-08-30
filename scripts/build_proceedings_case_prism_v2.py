#!/usr/bin/env python3
"""Build the explicit, bilingual Case Prism v2 public data projection.

The compact code below deliberately materialises every proposition/lane coordinate
in the published JSON.  Missing coordinates therefore cannot degrade to an
unexplained dash in the public renderer.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "assets/data/proceedings-case-prism-v1.json"
SEED = ROOT / "archive/PROCEEDINGS_CASE_PRISM_V1_SEED_30AUG2026.json"


def bi(en: str, es: str) -> dict[str, str]:
    return {"en": en, "es": es}


LANES = [
    {"id": "concurso", "en": "Concurso 36/2012", "es": "Concurso 36/2012", "master_ids": ["GC-JUD-001"]},
    {"id": "calificacion", "en": "Calificación · RPL 2523/2025", "es": "Calificación · RPL 2523/2025", "master_ids": ["GC-CAL-002", "GC-APP-004"]},
    {"id": "removal", "en": "AC removal · RPL 3304 + 3319/2025", "es": "Separación AC · RPL 3304 + 3319/2025", "master_ids": ["GC-APP-005", "GC-APP-006"]},
    {"id": "fees", "en": "AC remuneration · RPL 421/2026", "es": "Remuneración AC · RPL 421/2026", "master_ids": ["GC-CIV-027", "GC-APP-028"]},
    {"id": "arrecife", "en": "Arrecife · authority / control / mortgage / title", "es": "Arrecife · autoridad / control / hipoteca / título", "master_ids": ["LZ-JUD-042", "LZ-JUD-043", "LZ-JUD-003", "LZ-APP-004", "LZ-JUD-005"]},
    {"id": "valencia", "en": "Valencia · CaixaBank", "es": "Valencia · CaixaBank", "master_ids": ["VAL-CIV-001"]},
    {"id": "meetingpoint", "en": "Meeting Point 357/2024 · FTI bridge open", "es": "Meeting Point 357/2024 · puente FTI abierto", "master_ids": ["GC-CONT-025"]},
    {"id": "tenerife", "en": "Tenerife · separate Matkator / Cuatrecasas files", "es": "Tenerife · expedientes separados Matkator / Cuatrecasas", "master_ids": ["TF-CIV-001", "TF-CIV-002", "TF-CRI-003"]},
    {"id": "fiscalia", "en": "Ministerio Fiscal · selected controlled files", "es": "Ministerio Fiscal · expedientes controlados seleccionados", "master_ids": ["GC-FIS-013", "GC-FIS-016", "GC-FIS-017", "GC-FIS-018"]},
    {"id": "supervision", "en": "CGPJ supervision / LAJ registrations", "es": "Supervisión CGPJ / registros LAJ", "master_ids": ["GC-GOV-019", "GC-GOV-020", "GC-LAJ-021"]},
    {"id": "historical", "en": "Historical possession / exploitation", "es": "Posesión / explotación histórica", "master_ids": ["LZ-JUD-001", "LZ-JUD-FAM-006", "LZ-REF-042"]},
    {"id": "publicmoney", "en": "Administrative / public-money routes", "es": "Vías administrativas / fondos públicos", "master_ids": ["NAT-AID-001", "NAT-TES-001", "X-REG-001", "X-TAX-002"]},
]


SOURCES = {
    "SRC-MASTER": {
        "label_en": "Public Proceedings Master Register",
        "label_es": "Registro Maestro público de procedimientos",
        "href_en": "en/master-proceedings-register/",
        "href_es": "es/registro-maestro-procedimientos/",
        "evidence_status": "CANONICAL_PUBLIC_PROCEEDING_INDEX",
    },
    "SRC-CLEANROOM": {
        "label_en": "Public-authority unitary reconstruction",
        "label_es": "Reconstrucción unitaria para autoridades públicas",
        "href_en": "en/public-authority-unitary-case-reconstruction/",
        "href_es": "es/reconstruccion-unitaria-autoridades-publicas/",
        "evidence_status": "PUBLIC_CONTROLLED_RECONSTRUCTION",
    },
    "SRC-CAL": {
        "label_en": "Calificación / RPL 2523 evidence map",
        "label_es": "Mapa probatorio de Calificación / RPL 2523",
        "href_en": "en/calificacion-rpl-2523-evidence-map/",
        "href_es": "es/calificacion-rpl-2523-mapa-prueba/",
        "evidence_status": "PUBLIC_CONTROLLED_EVIDENCE_MAP",
    },
    "SRC-AC": {
        "label_en": "AC removal and remuneration record",
        "label_es": "Registro de separación y remuneración del AC",
        "href_en": "en/insolvency-36-2012-administrator-removal-fees/",
        "href_es": "es/concurso-36-2012-separacion-ac-honorarios/",
        "evidence_status": "PUBLIC_CONTROLLED_PROCEDURAL_RECONSTRUCTION",
    },
    "SRC-COMMUNITY": {
        "label_en": "Concurso 36/2012 community-authority audit",
        "label_es": "Auditoría de autoridad comunitaria del Concurso 36/2012",
        "href_en": "en/insolvency-36-2012-community-authority/",
        "href_es": "es/concurso-36-2012-autoridad-comunidad/",
        "evidence_status": "PUBLIC_CONTROLLED_AUTHORITY_MATRIX",
    },
    "SRC-ONA": {
        "label_en": "Pre-7 June 2018 funded ONA exit",
        "label_es": "Salida ONA financiada anterior al 7 de junio de 2018",
        "href_en": "en/pre-7-june-2018-funded-ona-exit/",
        "href_es": "es/salida-financiada-ona-antes-7-junio-2018/",
        "evidence_status": "PUBLIC_CONTROLLED_RECONSTRUCTION",
    },
    "SRC-ACCESS": {
        "label_en": "Before, during and after 7 June 2018",
        "label_es": "Antes, durante y después del 7 de junio de 2018",
        "href_en": "en/ona-hotels-insolvency-exit-36-2012/before-during-after-7-june-2018/",
        "href_es": "es/ona-hotels-salida-concurso-36-2012/antes-durante-despues-7-junio-2018/",
        "evidence_status": "PUBLIC_CONTROLLED_EVENT_RECONSTRUCTION",
    },
    "SRC-VALENCIA": {
        "label_en": "CaixaBank Valencia claim",
        "label_es": "Reclamación CaixaBank Valencia",
        "href_en": "en/caixabank-valencia-claim/",
        "href_es": "es/reclamacion-caixabank-valencia/",
        "evidence_status": "PUBLIC_CONTROLLED_PROCEDURAL_DOSSIER",
    },
    "SRC-FISCALIA": {
        "label_en": "Fiscalía DIP 2/2026 public dossier",
        "label_es": "Expediente público Fiscalía DIP 2/2026",
        "href_en": "en/fiscalia-dip-2-2026/",
        "href_es": "es/fiscalia-dip-2-2026/",
        "evidence_status": "PUBLIC_CONTROLLED_INSTITUTIONAL_DOSSIER",
    },
    "SRC-MEETING": {
        "label_en": "Meeting Point 357/2024 judicial trace",
        "label_es": "Trazabilidad judicial Meeting Point 357/2024",
        "href_en": "en/legal-notebook/meeting-point-357-2024-judicial-traceability/",
        "href_es": "es/cuaderno-juridico/meeting-point-357-2024-trazabilidad-judicial/",
        "evidence_status": "PUBLIC_CONTEXTUAL_PROCEEDING_DOSSIER",
    },
    "SRC-RICPE": {
        "label_en": "RIC Private Equity / Sun Park controlled chronology",
        "label_es": "Cronología controlada RIC Private Equity / Sun Park",
        "href_en": "en/ric-private-equity-sun-park/",
        "href_es": "es/ric-private-equity-sun-park/",
        "evidence_status": "PUBLIC_CONTROLLED_CHRONOLOGY",
    },
    "SRC-WEBINAR": {
        "label_en": "11 November 2020 RICPE webinar",
        "label_es": "Webinar RICPE de 11 de noviembre de 2020",
        "href_en": "en/ricpe-webinar-11nov2020/",
        "href_es": "es/ricpe-webinar-11nov2020/",
        "evidence_status": "CONTEMPORANEOUS_PUBLIC_SOURCE_WITH_ATTRIBUTION",
    },
    "SRC-ADJ": {
        "label_en": "2022 adjudication documentary reconstruction",
        "label_es": "Reconstrucción documental de la adjudicación de 2022",
        "href_en": "en/2022-adjudication-documentary-reconstruction/",
        "href_es": "es/adjudicacion-2022-reconstruccion-documental/",
        "evidence_status": "PUBLIC_CONTROLLED_DOCUMENTARY_RECONSTRUCTION",
    },
    "SRC-INCENTIVES": {
        "label_en": "Regional incentives GC/836/P06",
        "label_es": "Incentivos regionales GC/836/P06",
        "href_en": "en/regional-incentives-gc836-p06/",
        "href_es": "es/incentivos-regionales-gc836-p06/",
        "evidence_status": "PUBLIC_PRIMARY_DERIVED_CONTROL",
    },
    "SRC-TREASURY": {
        "label_en": "Treasury transparency 7/2026 delivery control",
        "label_es": "Control de entrega de transparencia Tesoro 7/2026",
        "href_en": "en/treasury-transparency-7-2026-28-august/",
        "href_es": "es/tesoro-transparencia-7-2026-28agosto/",
        "evidence_status": "VERIFIED_PRIMARY_WITH_STAGED_PRODUCTION_OPEN",
    },
    "SRC-FUNDS": {
        "label_en": "RIC / EU / incentives institutionalisation chain",
        "label_es": "Cadena de institucionalización RIC / UE / incentivos",
        "href_en": "en/institutionalisation-chain-ric-eu-incentives/",
        "href_es": "es/cadena-instrumentalizacion-ric-fondos-incentivos/",
        "evidence_status": "PUBLIC_CONTROLLED_RECONSTRUCTION",
    },
    "SRC-MATKATOR": {
        "label_en": "Tenerife / Matkator connected-proceedings route",
        "label_es": "Vía de procedimientos conectados Tenerife / Matkator",
        "href_en": "en/tenerife-south-active-holiday-community/",
        "href_es": "es/tenerife-sur-comunidad-vacacional-activa/",
        "evidence_status": "PUBLIC_CONTROLLED_CONTEXT_ROUTE",
    },
    "SRC-HISTORICAL": {
        "label_en": "Community instrumentalisation chronology",
        "label_es": "Cronología de instrumentalización de la Comunidad",
        "href_en": "en/community-instrumentalisation/",
        "href_es": "es/comunidad-instrumentalizacion/",
        "evidence_status": "PUBLIC_CONTROLLED_HISTORICAL_RECONSTRUCTION",
    },
    "SRC-SUPERVISION": {
        "label_en": "Justice institutional record",
        "label_es": "Registro institucional de justicia",
        "href_en": "en/justice-institutional-record/",
        "href_es": "es/justicia-registro-institucional/",
        "evidence_status": "PUBLIC_CONTROLLED_INSTITUTIONAL_RECORD",
    },
    "SRC-DP3205": {
        "label_en": "3205/2014 Arrecife controlled record",
        "label_es": "Registro controlado 3205/2014 Arrecife",
        "href_en": "en/dp-3205-2014-arrecife/",
        "href_es": "es/dp-3205-2014-arrecife/",
        "evidence_status": "PRIMARY_COMPLAINT_AND_OFFICIAL_SUMMONS_LOCATED_OUTCOME_OPEN",
    },
}


EVIDENCE_STATUS_ES = {
    "CANONICAL_PUBLIC_PROCEEDING_INDEX": "Índice canónico público de procedimientos",
    "CONTEMPORANEOUS_PUBLIC_REPRESENTATION_REQUIRES_REALITY_TEST": "Manifestación pública contemporánea; requiere contraste con la realidad",
    "CONTEMPORANEOUS_PUBLIC_SOURCE_WITH_ATTRIBUTION": "Fuente pública contemporánea con atribución",
    "HISTORICAL_PRIMARY_COMPLETION_PENDING": "Pendiente completar fuentes primarias históricas",
    "MIXED_PUBLIC_RECORD_TRANSACTION_ACCOUNTING_INCOMPLETE": "Registro público mixto; transacción y contabilidad incompletas",
    "MIXED_VERIFIED_AND_CONTEXTUAL": "Mixto: verificado y contextual",
    "MULTIPLE_VERIFIED_AND_OPEN_FISCALIA_FILES": "Múltiples expedientes de Fiscalía verificados y abiertos",
    "OPEN_UNIT_LEVEL_RECONCILIATION": "Conciliación por unidad abierta",
    "PARTLY_DOCUMENTED_AUTHORITY_CHAIN_INCOMPLETE": "Cadena de autoridad parcialmente documentada e incompleta",
    "PRIMARY_COMPLAINT_AND_OFFICIAL_SUMMONS_LOCATED_OUTCOME_OPEN": "Denuncia primaria y citación oficial localizadas; resultado abierto",
    "PUBLIC_CONTEXTUAL_PROCEEDING_DOSSIER": "Expediente procesal público contextual",
    "PUBLIC_CONTROLLED_AUTHORITY_MATRIX": "Matriz pública controlada de autoridad",
    "PUBLIC_CONTROLLED_CHRONOLOGY": "Cronología pública controlada",
    "PUBLIC_CONTROLLED_CONTEXT_ROUTE": "Vía pública controlada de contexto",
    "PUBLIC_CONTROLLED_DOCUMENTARY_RECONSTRUCTION": "Reconstrucción documental pública controlada",
    "PUBLIC_CONTROLLED_EVENT_RECONSTRUCTION": "Reconstrucción pública controlada del evento",
    "PUBLIC_CONTROLLED_EVIDENCE_MAP": "Mapa probatorio público controlado",
    "PUBLIC_CONTROLLED_HISTORICAL_RECONSTRUCTION": "Reconstrucción histórica pública controlada",
    "PUBLIC_CONTROLLED_INSTITUTIONAL_DOSSIER": "Expediente institucional público controlado",
    "PUBLIC_CONTROLLED_INSTITUTIONAL_RECORD": "Registro institucional público controlado",
    "PUBLIC_CONTROLLED_PROCEDURAL_DOSSIER": "Expediente procesal público controlado",
    "PUBLIC_CONTROLLED_PROCEDURAL_RECONSTRUCTION": "Reconstrucción procesal pública controlada",
    "PUBLIC_CONTROLLED_RECONSTRUCTION": "Reconstrucción pública controlada",
    "PUBLIC_CONTROLLED_RECOVERY_RECORD_WITH_OPEN_IMPLEMENTATION": "Registro público controlado de recuperación; implementación abierta",
    "PUBLIC_FUNDING_LAYER_VERIFIED_DEPENDENCY_AND_USE_OPEN": "Capa de financiación pública verificada; dependencia y uso abiertos",
    "PUBLIC_PRIMARY_DERIVED_CONTROL": "Control público derivado de fuente primaria",
    "SOURCE_SUPPORTED_WITH_PERIMETER_LIMITS": "Respaldado por fuentes con límites de perímetro",
    "VERIFIED_CONTEXTUAL_PROCEEDING_WITH_OPEN_TRANSACTION_BRIDGE": "Procedimiento contextual verificado con puente transaccional abierto",
    "VERIFIED_PROCEDURAL": "Procesal verificado",
    "VERIFIED_PROCEDURAL_OBJECTS_MERITS_AND_DENOMINATOR_OPEN": "Objetos procesales verificados; fondo y denominador abiertos",
    "VERIFIED_PROCEDURAL_PLUS_CROSS_READING_RULE": "Procesal verificado más regla de lectura cruzada",
    "VERIFIED_PROCEDURAL_WITH_OPEN_BRIDGES": "Procesal verificado con puentes abiertos",
    "VERIFIED_PROCEDURAL_WITH_OPEN_RECORD_COMPLETION": "Procesal verificado con expediente pendiente de completar",
    "VERIFIED_PRIMARY_WITH_STAGED_PRODUCTION_OPEN": "Fuente primaria verificada; producción escalonada restante abierta",
    "VERIFIED_WITH_LIMITATION_FINCA_RECONCILIATION_OPEN": "Verificado con limitación; conciliación por finca abierta",
    "VERIFIED_WITH_LIMITATION_NATIVE_BINDING_OPEN": "Verificado con limitación; vinculación nativa abierta",
}


def evidence_status_catalog() -> dict[str, dict[str, str]]:
    return {
        token: bi(token.replace("_", " ").title(), label_es)
        for token, label_es in EVIDENCE_STATUS_ES.items()
    }


AUDIENCES = [
    ("all", "All readers", "Todos los lectores", "Which factual dependencies cross legally separate files, and what is the controlled status of each connection?", "¿Qué dependencias fácticas cruzan expedientes jurídicamente separados y cuál es el estado controlado de cada conexión?", "Start with the finite question, then open the source and contrary record.", "Empiece por la pregunta concreta y abra después la fuente y el registro contrario."),
    ("court", "Court / magistrate", "Órgano judicial / magistratura", "What materially connected record should be tested before treating the isolated file as factually complete?", "¿Qué expediente materialmente conectado debe contrastarse antes de tratar el expediente aislado como fácticamente completo?", "Prioritise procedural availability, the decision dependency and the strongest contrary explanation.", "Priorice la disponibilidad procesal, la dependencia decisoria y la explicación contraria más fuerte."),
    ("appellate", "Audiencia Provincial", "Audiencia Provincial", "How do calificación, removal and remuneration treat the common insolvency-administration facts without implying joinder?", "¿Cómo tratan calificación, separación y remuneración los hechos comunes de administración concursal sin implicar acumulación?", "Compare the three appellate objects and keep each transmitted record separate.", "Compare los tres objetos apelativos y mantenga separado cada expediente remitido."),
    ("fiscal", "Ministerio Fiscal", "Ministerio Fiscal", "What did each office receive, examine, refer or leave unresolved, and is any cross-file acknowledgment located?", "¿Qué recibió, examinó, remitió o dejó sin resolver cada oficina y se ha localizado algún reconocimiento entre expedientes?", "Follow the office/file chronology and actor-specific receipt trail.", "Siga la cronología oficina/expediente y la trazabilidad de recepción por actor."),
    ("supervision", "CGPJ / judicial supervision", "CGPJ / supervisión judicial", "Did the supervisory record consider the relevant institutional handling while remaining outside the merits?", "¿Consideró el expediente supervisor el tratamiento institucional relevante manteniéndose fuera del fondo?", "Separate judicial remedies, supervisory competence and LAJ registration objects.", "Separe recursos judiciales, competencia supervisora y objetos registrales LAJ."),
    ("authority", "Regulator / public authority", "Regulador / autoridad pública", "Which finite proposition lies within this authority's competence and which primary file answers it?", "¿Qué proposición concreta entra en la competencia de esta autoridad y qué expediente primario la responde?", "Lead with competence, source needed, confirm/refute consequences and public-money dependencies.", "Empiece por competencia, fuente necesaria, consecuencias de confirmar/refutar y dependencias de fondos públicos."),
    ("research", "Journalist / researcher", "Periodista / investigador", "Which propositions are documented, attributed, contested or open, and where is the primary trail?", "¿Qué proposiciones están documentadas, atribuidas, controvertidas o abiertas y dónde está la trazabilidad primaria?", "Keep allegations, authority statements, inferences and contrary records visibly separate.", "Mantenga separadas las alegaciones, declaraciones de autoridad, inferencias y registros contrarios."),
    ("owner", "Owner / affected party / creditor", "Propietario / afectado / acreedor", "Which authority, title, debt, voting, income or estate-value proposition affects this legal position?", "¿Qué proposición de autoridad, título, deuda, voto, ingresos o valor de la masa afecta a esta posición jurídica?", "Start with capacity and unit/credit/title records; do not infer authority from possession or later title.", "Empiece por capacidad y registros de unidad/crédito/título; no infiera autoridad de la posesión o título posterior."),
    ("professional", "Professional / funder", "Profesional / financiador", "Which mandate, knowledge, reliance, source-of-funds or decision-control record is actually actor-specific?", "¿Qué mandato, conocimiento, confianza, origen de fondos o control decisorio es realmente específico del actor?", "Follow engagement, conflict, KYC, representation and transaction-level records.", "Siga encargos, conflictos, KYC, representación y registros transaccionales."),
]


def lens_rows() -> list[dict[str, str]]:
    return [
        {
            "id": row[0], "en": row[1], "es": row[2],
            "question_en": row[3], "question_es": row[4],
            "source_path_en": row[5], "source_path_es": row[6],
        }
        for row in AUDIENCES
    ]


def action(source_en: str, source_es: str, organ_en: str, organ_es: str,
           yes_en: str = "", yes_es: str = "", no_en: str = "", no_es: str = "") -> dict:
    return {
        "source_needed": bi(source_en, source_es),
        "competent_organ": bi(organ_en, organ_es),
        "if_confirmed": bi(yes_en, yes_es),
        "if_refuted": bi(no_en, no_es),
    }


RICH = {
    "P01": {
        "period_en": "2012–present", "period_es": "2012–actualidad", "attribution": "DOCUMENTED_FACT",
        "contrary_record": bi("A shared insolvency origin does not make later civil, criminal, appellate or supervisory files one proceeding.", "Un origen concursal común no convierte los expedientes civiles, penales, apelativos o supervisores posteriores en un único procedimiento."),
        "decision_dependency": bi("Whether a later decision depends on an act, asset, credit or administration event within Concurso 36/2012.", "Si una decisión posterior depende de un acto, activo, crédito o evento de administración del Concurso 36/2012."),
        "actionability": action("Certified docket, transmitted record and the exact originating act.", "Expediente certificado, testimonio remitido y acto de origen exacto.", "The court or organ competent for the selected file.", "El juzgado u órgano competente para el expediente seleccionado.", "The connected act can be tested through the lawful route.", "El acto conectado puede contrastarse por la vía legal.", "The asserted dependency should be removed or narrowed.", "La dependencia afirmada debe eliminarse o limitarse."),
        "source_ids": ["SRC-MASTER", "SRC-CLEANROOM", "SRC-CAL", "SRC-AC"],
    },
    "P02": {
        "period_en": "2012–2027", "period_es": "2012–2027", "attribution": "MIXED_DOCUMENTED_AND_OPEN",
        "contrary_record": bi("Enforcement, creditor rights, satisfaction, title and later banking claims may each be lawful and analytically distinct; the exact Arrecife EH 90 identity remains incomplete.", "La ejecución, los derechos del acreedor, la satisfacción, el título y la reclamación bancaria posterior pueden ser lícitos y analíticamente distintos; la identidad exacta de la EH 90 de Arrecife sigue incompleta."),
        "decision_dependency": bi("The legal and accounting life of the secured credit, its satisfaction and the asset-title consequences.", "La vida jurídica y contable del crédito garantizado, su satisfacción y las consecuencias sobre el título del activo."),
        "actionability": action("Certified EH 90/2012 file, deeds, registry history, credit ledger and Valencia pleadings.", "Expediente certificado EH 90/2012, escrituras, historial registral, mayor del crédito y escritos de Valencia.", "The respective insolvency, Arrecife, registry and Valencia organs.", "Los respectivos órganos concursales, de Arrecife, registrales y de Valencia.", "A common credit/title dependency can be reconciled without merging proceedings.", "Puede conciliarse una dependencia común crédito/título sin fusionar procedimientos.", "The corridor must remain only historical context.", "El corredor debe quedar solo como contexto histórico."),
        "source_ids": ["SRC-MASTER", "SRC-VALENCIA", "SRC-ADJ"],
    },
    "P03": {
        "period_en": "7 June 2018", "period_es": "7 de junio de 2018", "attribution": "MIXED_DOCUMENTED_AND_PARTY_ALLEGATION",
        "contrary_record": bi("The located DI 1103/2018-00 → DP 1132/2018 → Rollo 1010/2018 / Auto 804/2018 route ended in provisional archive confirmed on appeal; the AC/CEXP record contains a contrary position, and the main witness did not place José Daniel Acosta Matos on site.", "La vía localizada DI 1103/2018-00 → DP 1132/2018 → Rollo 1010/2018 / Auto 804/2018 terminó en sobreseimiento provisional confirmado en apelación; el registro AC/CEXP contiene una posición contraria y el testigo principal no situó a José Daniel Acosta Matos en el lugar."),
        "decision_dependency": bi("Whether the event was lawful access, material control, or neither, and what estate/productive-unit consequences followed.", "Si el evento fue acceso lícito, control material o ninguno de ellos y qué consecuencias siguieron para la masa/unidad productiva."),
        "actionability": action("Court-certified complete DP 1132/2018 and Rollo 1010/2018 files, witness record, authority instruments and contemporaneous access/operation evidence.", "Expedientes completos certificados de DP 1132/2018 y Rollo 1010/2018, testimonio, instrumentos de autoridad y pruebas contemporáneas de acceso/explotación.", "The competent criminal/civil/insolvency organ for each distinct issue.", "El órgano penal/civil/concursal competente para cada cuestión distinta.", "Actor-specific authority, conduct and consequences can be determined.", "Pueden determinarse autoridad, conducta y consecuencias específicas por actor.", "The control allegation must be withdrawn or reframed as an unresolved event.", "La alegación de control debe retirarse o reformularse como evento no resuelto."),
        "source_ids": ["SRC-ACCESS", "SRC-MASTER", "SRC-CLEANROOM"],
    },
    "P04": {
        "period_en": "2023–present", "period_es": "2023–actualidad", "attribution": "DOCUMENTED_PROCEDURAL_COMPARISON",
        "contrary_record": bi("The first-instance removal applications were dismissed; the 11 November order recorded no indication for ex officio removal; the fees judgment decided standing, not fee legality or quantum; later appellate merits outcomes are not located.", "Las solicitudes de separación fueron desestimadas en primera instancia; el auto de 11 de noviembre no apreció indicios para separación de oficio; la sentencia de honorarios resolvió legitimación, no legalidad ni cuantía; no se han localizado decisiones apelativas de fondo posteriores."),
        "decision_dependency": bi("Common AC facts may receive different treatment in calificación, removal and remuneration while each appeal remains separate.", "Hechos comunes del AC pueden recibir tratamiento distinto en calificación, separación y remuneración manteniéndose separado cada recurso."),
        "actionability": action("Complete certified records and signed merits/finality outcomes for RPL 2523, 3304+3319 and 421.", "Expedientes certificados completos y resoluciones firmadas de fondo/firmeza para RPL 2523, 3304+3319 y 421.", "Audiencia Provincial de Las Palmas, competent section for each roll.", "Audiencia Provincial de Las Palmas, sección competente para cada rollo.", "The comparison can identify a legally material common fact and its different treatment.", "La comparación puede identificar un hecho común jurídicamente material y su tratamiento diferente.", "Any claimed cross-appeal dependency should be narrowed to context.", "Toda dependencia afirmada entre recursos debe limitarse a contexto."),
        "source_ids": ["SRC-CAL", "SRC-AC", "SRC-MASTER"],
    },
    "P05": {
        "period_en": "2013–2026", "period_es": "2013–2026", "attribution": "DOCUMENTED_SELECTED_SUBSET",
        "contrary_record": bi("Different Fiscalía offices may have independently and lawfully narrowed, referred or archived the material before them; the current Prism is a selected subset, not the complete cross-office denominator.", "Distintas Fiscalías pueden haber acotado, remitido o archivado lícitamente y de forma independiente el material recibido; el Prisma actual es una selección, no el denominador completo entre oficinas."),
        "decision_dependency": bi("What each office/file actually received, examined, referred or answered and whether it acknowledged cross-file relevance.", "Qué recibió, examinó, remitió o respondió realmente cada oficina/expediente y si reconoció relevancia entre expedientes."),
        "actionability": action("Stamped submissions, annex inventories, referral records, decrees and current file-status certifications office by office.", "Escritos sellados, inventarios de anexos, remisiones, decretos y certificaciones actuales expediente por expediente.", "The Fiscalía office holding each file and any competent judicial recipient.", "La Fiscalía titular de cada expediente y cualquier receptor judicial competente.", "A unitary or file-limited institutional treatment can be shown from the record.", "Puede acreditarse un tratamiento institucional unitario o limitado al expediente.", "The claimed institutional-memory bridge must remain not located.", "El puente de memoria institucional afirmado debe seguir como no localizado."),
        "source_ids": ["SRC-FISCALIA", "SRC-MASTER", "SRC-CLEANROOM"],
    },
    "P06": {
        "period_en": "2019–present", "period_es": "2019–actualidad", "attribution": "DOCUMENTED_SEPARATE_FILES_WITH_OPEN_CONTEXT",
        "contrary_record": bi("Juicio Cambiario 1048/2019, ETJ 163/2020 and DP 748/2026 are separate files; no parent/continuation edge is established, and Matkator remains a separate legal person.", "Juicio Cambiario 1048/2019, ETJ 163/2020 y DP 748/2026 son expedientes separados; no se ha establecido una relación padre/continuación y Matkator sigue siendo persona jurídica separada."),
        "decision_dependency": bi("Whether a specific mandate, enforcement act, asset/right or alleged harm creates a source-backed contextual bridge.", "Si un encargo, acto de ejecución, activo/derecho o daño alegado específico crea un puente contextual respaldado por fuente."),
        "actionability": action("Complete pleadings, enforcement record, mandate/engagement files and actor-specific receipt/instruction evidence.", "Escritos completos, expediente de ejecución, archivos de encargo y pruebas específicas de recepción/instrucción por actor.", "The separate Tenerife civil/criminal organs and any competent professional regulator.", "Los órganos civiles/penales separados de Tenerife y cualquier regulador profesional competente.", "A precise professional-work or patrimonial bridge can be tested.", "Puede contrastarse un puente preciso de trabajo profesional o patrimonial.", "The files remain merely separate matters with thematic overlap.", "Los expedientes quedan como asuntos separados con coincidencia temática."),
        "source_ids": ["SRC-MATKATOR", "SRC-MASTER", "SRC-CLEANROOM"],
    },
    "P07": {
        "period_en": "2008–present", "period_es": "2008–actualidad", "attribution": "MIXED_VERIFIED_AND_UNVERIFIED_FAMILY",
        "contrary_record": bi("Possession, exploitation and party-substitution decisions may reflect valid title, standing or procedural discretion; AP 89/2014 is verified, while the broader family remains unverified case by case.", "Las decisiones de posesión, explotación y sustitución procesal pueden reflejar título, legitimación o discreción válidos; AP 89/2014 está verificado, mientras la familia más amplia sigue sin verificar caso por caso."),
        "decision_dependency": bi("Which legal person held which capacity, possession or exploitation right at each material date.", "Qué persona jurídica ostentaba qué capacidad, posesión o derecho de explotación en cada fecha material."),
        "actionability": action("Certified historical dockets, party-substitution acts, deeds, registry entries, contracts and implementation records.", "Expedientes históricos certificados, actos de sustitución, escrituras, asientos registrales, contratos y registros de ejecución.", "The organ competent for each historical file and the relevant registry.", "El órgano competente para cada expediente histórico y el registro correspondiente.", "A lawful lineage or a material break can be proved date by date.", "Puede probarse fecha por fecha una línea lícita o una ruptura material.", "The later-control narrative must not rely on the historical family.", "La narrativa de control posterior no debe apoyarse en la familia histórica."),
        "source_ids": ["SRC-HISTORICAL", "SRC-MASTER", "SRC-COMMUNITY"],
    },
    "P08": {
        "period_en": "2020–2025", "period_es": "2020–2025", "attribution": "DOCUMENTED_CONTEXT_WITH_OPEN_TRANSACTION_BRIDGE",
        "contrary_record": bi("COVID disruption is a plausible explanation for restructuring; brochures do not prove a contract, booking, payment or revenue transfer, and the exact contracting legal person remains unresolved.", "La disrupción COVID es una explicación plausible para la reestructuración; los folletos no prueban contrato, reserva, pago ni transferencia de ingresos y la persona jurídica contratante exacta sigue sin resolver."),
        "decision_dependency": bi("Whether any specific operator, stock, contract, booking, revenue or public-money flow connected Meeting Point/FTI to Sun Park.", "Si algún operador, stock, contrato, reserva, ingreso o flujo público específico conectó Meeting Point/FTI con Sun Park."),
        "actionability": action("Contracting-entity records, operator agreements, booking/revenue ledgers, source-and-use records and the complete 357/2024 file.", "Registros de entidad contratante, contratos de operador, mayores de reservas/ingresos, origen y uso de fondos y expediente 357/2024 completo.", "The restructuring court, contracting entities and competent public-funds organs.", "El juzgado de reestructuración, las entidades contratantes y órganos competentes de fondos públicos.", "A transaction-level bridge can be stated with its amount, actor and source.", "Puede afirmarse un puente transaccional con cuantía, actor y fuente.", "The Meeting Point lane remains contextual only.", "La vía Meeting Point queda solo como contexto."),
        "source_ids": ["SRC-MEETING", "SRC-MASTER", "SRC-FUNDS"],
    },
    "P09": {
        "period_en": "2026", "period_es": "2026", "attribution": "DOCUMENTED_SUPERVISORY_AND_REGISTRATION_OBJECTS",
        "contrary_record": bi("DI 169/2026 was archived and maintained on 10 July; the Alzada 286 merits decision is not located; LAJ items are registrations, not proceedings or merits findings.", "DI 169/2026 fue archivada y mantenida el 10 de julio; no se ha localizado decisión de fondo de Alzada 286; los elementos LAJ son registros, no procedimientos ni pronunciamientos de fondo."),
        "decision_dependency": bi("Whether the supervisory body had and addressed the relevant institutional-handling record within its competence.", "Si el órgano supervisor recibió y trató el registro de actuación institucional relevante dentro de su competencia."),
        "actionability": action("Complete supervisory submissions, annex indexes, decisions, service/finality and exact LAJ registration objects.", "Escritos supervisores completos, índices de anexos, decisiones, notificación/firmeza y objetos registrales LAJ exactos.", "CGPJ supervisory/appeals bodies or the judicial-office authority within their respective competence.", "Órganos supervisores/de recursos del CGPJ o autoridad de oficina judicial dentro de su competencia respectiva.", "The scope and completeness of the institutional response can be tested.", "Puede contrastarse el alcance y completitud de la respuesta institucional.", "The alleged omission must remain an open record question.", "La omisión alegada debe seguir como cuestión documental abierta."),
        "source_ids": ["SRC-SUPERVISION", "SRC-MASTER", "SRC-CLEANROOM"],
    },
    "P10": {
        "sort": 2011.0, "period_en": "2011–present", "period_es": "2011–actualidad",
        "title_en": "Community authority must be proved act by act", "title_es": "La autoridad comunitaria debe probarse acto por acto",
        "question_en": "Who acted, for which exact Community/legal person, in what capacity, and what contemporaneous instrument established authority?", "question_es": "¿Quién actuó, para qué Comunidad/persona jurídica exacta, en qué capacidad y qué instrumento contemporáneo acreditó la autoridad?",
        "source_status": "PARTLY_DOCUMENTED_AUTHORITY_CHAIN_INCOMPLETE", "attribution": "OPEN_AUTHORITY_QUESTION",
        "contrary_record": bi("A valid ACTA, office, proxy, owner right, creditor right or later ratification may explain an act; association, possession or later title alone does not.", "Un ACTA, cargo, poder, derecho de propietario/acreedor o ratificación posterior válidos pueden explicar un acto; la asociación, posesión o título posterior por sí solos no."),
        "decision_dependency": bi("Standing, notice, reliance and legal effect of any act presented as a Community act.", "Legitimación, conocimiento, confianza y efecto jurídico de cualquier acto presentado como comunitario."),
        "actionability": action("Complete ACTA, notice, attendance/proxy, coefficient, office, power and personación package for the date and act.", "Paquete completo de ACTA, convocatoria, asistencia/poder, coeficiente, cargo, poder y personación para fecha y acto.", "The deciding court, Community records custodian or competent registry for the specific act.", "El juzgado decisor, custodio comunitario o registro competente para el acto específico.", "The act can be attributed to a legally authorised person/body.", "El acto puede atribuirse a una persona/órgano jurídicamente autorizado.", "Any procedural or patrimonial effect based on that asserted authority requires reassessment.", "Todo efecto procesal o patrimonial basado en esa autoridad afirmada requiere reevaluación."),
        "source_ids": ["SRC-COMMUNITY", "SRC-HISTORICAL", "SRC-CLEANROOM"],
    },
    "P11": {
        "sort": 2011.2, "period_en": "2008–2018", "period_es": "2008–2018",
        "title_en": "Debt and voting require a unit-level denominator", "title_es": "Deuda y voto requieren un denominador por unidad",
        "question_en": "Which units, owners, coefficients, debts, proxies and exclusions formed the asserted majority or creditor position?", "question_es": "¿Qué unidades, propietarios, coeficientes, deudas, poderes y exclusiones formaron la mayoría o posición acreedora afirmada?",
        "source_status": "OPEN_UNIT_LEVEL_RECONCILIATION", "attribution": "OPEN_ACCOUNTING_AND_AUTHORITY_QUESTION",
        "contrary_record": bi("The asserted debts, exclusions and votes may be valid once the complete unit ledger and resolutions are produced.", "Las deudas, exclusiones y votaciones afirmadas pueden ser válidas cuando se aporte el mayor completo por unidad y las resoluciones."),
        "decision_dependency": bi("Authority, creditor standing, quorum/majority and any consequence attributed to Community decisions.", "Autoridad, legitimación acreedora, quórum/mayoría y toda consecuencia atribuida a decisiones comunitarias."),
        "actionability": action("Unit ownership/completion ledger, debt basis, notices, proxies, exclusions, coefficients and counterfactual vote calculation.", "Mayor de titularidad/cierre por unidad, base de deuda, convocatorias, poderes, exclusiones, coeficientes y cálculo contrafactual.", "The competent Community/civil/insolvency organ for the exact decision.", "El órgano comunitario/civil/concursal competente para la decisión exacta.", "The majority and resulting authority can be reproduced.", "La mayoría y la autoridad resultante pueden reproducirse.", "The relied-upon resolution or creditor position may lack the asserted denominator.", "La resolución o posición acreedora utilizada puede carecer del denominador afirmado."),
        "source_ids": ["SRC-COMMUNITY", "SRC-HISTORICAL", "SRC-CLEANROOM"],
    },
    "P12": {
        "sort": 2017.6, "period_en": "2017–7 June 2018", "period_es": "2017–7 de junio de 2018",
        "title_en": "The funded ONA exit is a separate recovery and counterfactual record", "title_es": "La salida ONA financiada es un registro separado de recuperación y contrafactual",
        "question_en": "What finance, operator, viability, creditor and implementation steps existed before the 7 June 2018 event, and what happened to them?", "question_es": "¿Qué pasos de financiación, operador, viabilidad, acreedores y ejecución existían antes del 7 de junio de 2018 y qué ocurrió con ellos?",
        "source_status": "PUBLIC_CONTROLLED_RECOVERY_RECORD_WITH_OPEN_IMPLEMENTATION", "attribution": "DOCUMENTED_RECOVERY_POSITION_AND_OPEN_CAUSATION",
        "contrary_record": bi("A proposed exit or term sheet does not prove binding finance, completed recovery, causation or that an alternative would have succeeded.", "Una salida propuesta o term sheet no prueba financiación vinculante, recuperación completada, causalidad ni que la alternativa hubiera prosperado."),
        "decision_dependency": bi("Viability, estate-value counterfactual, loss causation and the completeness of later characterisations of the pre-event position.", "Viabilidad, contrafactual de valor de la masa, causalidad del daño y completitud de caracterizaciones posteriores de la posición previa."),
        "actionability": action("Executed finance/operator documents, conditions precedent, creditor consents, implementation trail and contemporaneous valuations.", "Documentos ejecutados de financiación/operador, condiciones, consentimientos, trazabilidad de ejecución y valoraciones contemporáneas.", "The insolvency court/AC and any organ deciding a causation or damage proposition.", "El juzgado/AC concursal y cualquier órgano que decida causalidad o daño.", "A viable financed alternative and its lost consequence can be measured.", "Puede medirse una alternativa financiada viable y su consecuencia perdida.", "The record remains a proposal, not a proved counterfactual loss.", "El registro queda como propuesta, no como pérdida contrafactual probada."),
        "source_ids": ["SRC-ONA", "SRC-ACCESS", "SRC-CLEANROOM"],
    },
    "P13": {
        "sort": 2020.0, "period_en": "11 November 2020", "period_es": "11 de noviembre de 2020",
        "title_en": "The 2020 project promotion is an attributed representation", "title_es": "La promoción del proyecto de 2020 es una manifestación atribuida",
        "question_en": "Who represented title, availability, due diligence, project cost and investment status, to whom, and from which underlying records?", "question_es": "¿Quién manifestó título, disponibilidad, due diligence, coste y estado de inversión, ante quién y desde qué registros subyacentes?",
        "source_status": "CONTEMPORANEOUS_PUBLIC_REPRESENTATION_REQUIRES_REALITY_TEST", "attribution": "SOURCE_AUTHORED_STATEMENT",
        "contrary_record": bi("Promotional language may have been shorthand, conditional, corrected or based on information reasonably supplied at the time; it is not itself proof of falsehood or intent.", "El lenguaje promocional puede haber sido abreviado, condicionado, corregido o basado razonablemente en información entonces suministrada; no prueba por sí solo falsedad ni intención."),
        "decision_dependency": bi("Investor/regulator/funder reliance and reconciliation of the promoted asset/title picture with the underlying record.", "Confianza de inversores/reguladores/financiadores y conciliación de la imagen promovida de activo/título con el registro subyacente."),
        "actionability": action("Native webinar, presentation pack, source/title/DD pack, approvals, attendee distribution and later corrections.", "Webinar nativo, presentación, paquete fuente/título/DD, aprobaciones, distribución y correcciones posteriores.", "The competent regulator, funder or court for the specific reliance proposition.", "El regulador, financiador o juzgado competente para la proposición específica de confianza."),
        "if_confirmed": "", "source_ids": ["SRC-WEBINAR", "SRC-RICPE", "SRC-CLEANROOM"],
    },
    "P14": {
        "sort": 2021.55, "period_en": "July 2021", "period_es": "julio de 2021",
        "title_en": "The 54 / 190 / 18 ownership record is a knowledge checkpoint", "title_es": "El registro de titularidad 54 / 190 / 18 es un punto de conocimiento",
        "question_en": "Was the native certification authentic, who received it, how was the split treated and what correction or decision followed?", "question_es": "¿Era auténtica la certificación nativa, quién la recibió, cómo se trató el reparto y qué corrección o decisión siguió?",
        "source_status": "VERIFIED_WITH_LIMITATION_NATIVE_BINDING_OPEN", "attribution": "DOCUMENTED_RECORD_WITH_PROVENANCE_GAP",
        "contrary_record": bi("The split may reflect a transitional, conditional or incomplete title position and does not itself prove any false prior statement or improper later decision.", "El reparto puede reflejar una situación transitoria, condicional o incompleta y no prueba por sí solo falsedad previa ni decisión posterior impropia."),
        "decision_dependency": bi("Knowledge of fragmented title before later investment, finance, adjudication or public-support decisions.", "Conocimiento de título fragmentado antes de decisiones posteriores de inversión, financiación, adjudicación o apoyo público."),
        "actionability": action("Native signed certification, drafts, circulation/receipt trail, underlying registry extract, minutes and correction/decision record.", "Certificación nativa firmada, borradores, trazabilidad de circulación/recepción, nota registral, actas y registro de corrección/decisión.", "The receiving corporate bodies, regulator/funder and any deciding court within competence.", "Los órganos societarios receptores, regulador/financiador y cualquier juzgado competente."),
        "if_confirmed": "", "source_ids": ["SRC-RICPE", "SRC-CLEANROOM", "SRC-FUNDS"],
    },
    "P15": {
        "sort": 2022.1, "period_en": "2022–2025", "period_es": "2022–2025",
        "title_en": "Adjudication, deed and registration must remain date-specific", "title_es": "Adjudicación, escritura y registro deben mantenerse específicos por fecha",
        "question_en": "What exactly was adjudicated, on what conditions and value, when did title pass, what was registered and what remained third-party owned?", "question_es": "¿Qué se adjudicó exactamente, bajo qué condiciones y valor, cuándo pasó el título, qué se registró y qué siguió perteneciendo a terceros?",
        "source_status": "VERIFIED_WITH_LIMITATION_FINCA_RECONCILIATION_OPEN", "attribution": "DOCUMENTED_TRANSACTION_THRESHOLD",
        "contrary_record": bi("A valid adjudication/deed/registration may establish later title and creditor satisfaction; later title does not retroactively establish earlier authority or possession.", "Una adjudicación/escritura/inscripción válida puede establecer título posterior y satisfacción del acreedor; el título posterior no acredita retroactivamente autoridad o posesión anterior."),
        "decision_dependency": bi("Title, estate value, creditor satisfaction, surplus/conditions and the perimeter available for later project/funding decisions.", "Título, valor de la masa, satisfacción del acreedor, sobrante/condiciones y perímetro disponible para decisiones posteriores de proyecto/financiación."),
        "actionability": action("Signed adjudication order/deed, schedules, price/accounting, conditions, registry implementation and finca-by-finca ownership map.", "Auto/escritura de adjudicación firmados, anexos, precio/contabilidad, condiciones, ejecución registral y mapa finca por finca.", "The insolvency court, notary/registry and any organ relying on title/availability.", "El juzgado concursal, notario/registro y cualquier órgano que dependa de título/disponibilidad."),
        "if_confirmed": "", "source_ids": ["SRC-ADJ", "SRC-MASTER", "SRC-FUNDS"],
    },
    "P16": {
        "sort": 2018.8, "period_en": "2018–present", "period_es": "2018–actualidad",
        "title_en": "Productive-unit, income and value consequences require accounting", "title_es": "Las consecuencias sobre unidad productiva, ingresos y valor requieren contabilidad",
        "question_en": "Which operator controlled which productive assets, contracts, bookings, income and expenditure, and what entered or left the estate?", "question_es": "¿Qué operador controló qué activos productivos, contratos, reservas, ingresos y gastos y qué entró o salió de la masa?",
        "source_status": "MIXED_PUBLIC_RECORD_TRANSACTION_ACCOUNTING_INCOMPLETE", "attribution": "OPEN_ACCOUNTING_AND_CAUSATION_QUESTION",
        "contrary_record": bi("Changes in operation, value or income may follow lawful contracts, market/COVID conditions, maintenance needs or independent business decisions.", "Los cambios de explotación, valor o ingresos pueden derivar de contratos lícitos, mercado/COVID, mantenimiento o decisiones empresariales independientes."),
        "decision_dependency": bi("Estate conservation, counterfactual value, damages, benefit and any public/private funding dependency.", "Conservación de la masa, valor contrafactual, daños, beneficio y cualquier dependencia de financiación pública/privada."),
        "actionability": action("Operator/booking contracts, bank and booking ledgers, taxes, payroll, utilities, occupancy, capex, valuations and estate accounts.", "Contratos de operador/reservas, mayores bancarios/de reservas, impuestos, nóminas, suministros, ocupación, capex, valoraciones y cuentas de masa.", "The insolvency court/AC, tax/public-funds organs and any damages court within competence.", "El juzgado/AC concursal, órganos fiscales/de fondos y cualquier juzgado de daños competente."),
        "if_confirmed": "", "source_ids": ["SRC-ONA", "SRC-MEETING", "SRC-FUNDS", "SRC-ADJ"],
    },
    "P17": {
        "sort": 2024.2, "period_en": "2024–2026", "period_es": "2024–2026",
        "title_en": "AC conduct and remuneration are different appellate questions", "title_es": "Conducta y remuneración del AC son cuestiones apelativas distintas",
        "question_en": "Which exact act/omission, duty, knowledge, capacity, consequence and remuneration item was put before each competent file?", "question_es": "¿Qué acto/omisión, deber, conocimiento, capacidad, consecuencia y partida retributiva exactos se sometieron a cada expediente competente?",
        "source_status": "VERIFIED_PROCEDURAL_OBJECTS_MERITS_AND_DENOMINATOR_OPEN", "attribution": "PARTY_SUBMISSION_AND_PROCEDURAL_RECORD",
        "contrary_record": bi("Removal was refused at first instance; ex officio indications were not found in the located 11 November order; the fees judgment addressed standing rather than fee legality/quantum; appellate outcomes remain open.", "La separación fue denegada en primera instancia; el auto localizado de 11 de noviembre no apreció indicios de oficio; la sentencia de honorarios trató legitimación y no legalidad/cuantía; los resultados apelativos siguen abiertos."),
        "decision_dependency": bi("Separate determinations of removal, conduct, standing, restitution and remuneration—never a single global AC conclusion.", "Determinaciones separadas de separación, conducta, legitimación, restitución y remuneración—nunca una conclusión global sobre el AC."),
        "actionability": action("Complete applications/oppositions, underlying acts, accounts, fee decisions, insurance, appellate records and signed current outcomes.", "Solicitudes/oposiciones completas, actos subyacentes, cuentas, decisiones de honorarios, seguro, expedientes apelativos y resultados firmados actuales.", "The distinct first-instance and appellate organs for removal and remuneration.", "Los órganos distintos de primera instancia y apelación para separación y remuneración."),
        "if_confirmed": "", "source_ids": ["SRC-AC", "SRC-CAL", "SRC-MASTER"],
    },
    "P18": {
        "sort": 2022.5, "period_en": "2021–present", "period_es": "2021–actualidad",
        "title_en": "RIC, incentives and ERDF require programme-by-programme dependency tests", "title_es": "RIC, incentivos y FEDER requieren pruebas de dependencia programa por programa",
        "question_en": "What title/availability, eligible-cost, payment, job, source-of-funds and control representations were required and actually verified for each programme?", "question_es": "¿Qué manifestaciones de título/disponibilidad, coste elegible, pago, empleo, origen de fondos y control exigió y verificó realmente cada programa?",
        "source_status": "PUBLIC_FUNDING_LAYER_VERIFIED_DEPENDENCY_AND_USE_OPEN", "attribution": "DOCUMENTED_PUBLIC_FUNDING_IDENTIFICATION_WITH_OPEN_CAUSATION",
        "contrary_record": bi("The published award and ERDF identification do not prove payment, overlap, misuse, fraud or criminal causation; each programme may have independently valid controls.", "La concesión publicada y la identificación FEDER no prueban pago, solapamiento, uso indebido, fraude ni causalidad penal; cada programa puede tener controles válidos independientes."),
        "decision_dependency": bi("Eligibility, payment/certification, title/availability reliance, double-funding risk and any recovery consequence.", "Elegibilidad, pago/certificación, confianza en título/disponibilidad, riesgo de doble financiación y eventual reintegro."),
        "actionability": action("Complete applications, resolutions, eligible-cost schedules, payment/certification/control files, title declarations and source-and-use ledger.", "Solicitudes, resoluciones, anexos de coste elegible, expedientes de pago/certificación/control, declaraciones de título y mayor de origen/uso.", "The granting/controlling authority, AEAT/CNMV where competent, audit bodies and any judicial organ for a distinct legal issue.", "La autoridad concedente/controladora, AEAT/CNMV según competencia, órganos de auditoría y cualquier órgano judicial para una cuestión distinta."),
        "if_confirmed": "", "source_ids": ["SRC-INCENTIVES", "SRC-TREASURY", "SRC-FUNDS", "SRC-RICPE"],
    },
    "P19": {
        "sort": 2014.0, "period_en": "2014", "period_es": "2014",
        "title_en": "3205/2014 is an access, key and Community-authority verification event, not a procedural bridge", "title_es": "3205/2014 es un evento de verificación de acceso, llave y autoridad comunitaria, no un puente procesal",
        "question_en": "What authority supported the reported entry and inspection, what happened in the key dispute, and what do the complaint, summons and missing outcome permit the reader to conclude?", "question_es": "¿Qué autoridad sustentó la entrada e inspección comunicadas, qué ocurrió en la disputa por la llave y qué permiten concluir la denuncia, la citación y el resultado ausente?",
        "source_status": "PRIMARY_COMPLAINT_AND_OFFICIAL_SUMMONS_LOCATED_OUTCOME_OPEN", "attribution": "PARTY_SUBMISSION_AND_PROCEDURAL_RECORD",
        "contrary_record": bi("The complaint records attributed allegations and the summons records a procedural step; neither proves the incident, injury, agency, guilt or outcome. A contrary account exists, while decisive corroboration and the outcome remain unlocated.", "La denuncia registra alegaciones atribuidas y la citación registra un acto procesal; ninguna prueba el incidente, la lesión, la agencia, la culpabilidad ni el resultado. Existe un relato contrario, mientras siguen sin localizarse la corroboración decisiva y el resultado."),
        "decision_dependency": bi("Authority for the reported entry and inspection, actor-specific conduct and capacity, injury corroboration, and the hearing and outcome within 3205/2014.", "Autoridad para la entrada e inspección comunicadas, conducta y capacidad específicas de cada actor, corroboración de lesiones y celebración y resultado dentro de 3205/2014."),
        "actionability": action("Certified docket, hearing, decision and finality records; contemporaneous medical, independent-witness and CCTV evidence; and actor-specific role, instruction and authority records.", "Expediente certificado, acta de vista, resolución y firmeza; prueba médica contemporánea, testigo independiente y CCTV; y registros de función, instrucción y autoridad específicos de cada actor.", "The historic file custodian and the competent deciding organ for each distinct issue.", "El custodio del expediente histórico y el órgano decisor competente para cada cuestión distinta.", "The event can be characterised act by act inside its own file without extension to another proceeding.", "El evento puede caracterizarse acto por acto dentro de su propio expediente sin extenderlo a otro procedimiento.", "Unsupported authority, agency, injury or cross-file propositions must be narrowed or removed.", "Deben limitarse o retirarse las proposiciones no respaldadas de autoridad, agencia, lesión o conexión entre expedientes."),
        "source_ids": ["SRC-DP3205", "SRC-MASTER", "SRC-COMMUNITY"],
    },
}


# New rows use source-led, finite propositions. Existing rows retain their titles,
# questions and curated cells, but receive the same actionability contract.
NEW_PROP_IDS = ["P10", "P11", "P12", "P13", "P14", "P15", "P16", "P17", "P18", "P19"]


CELL_OVERRIDES = {
    "P02": {
        "arrecife": {"status": "OPEN", "treatment": "STATUS_UNRESOLVED", "master_ids": ["LZ-JUD-005"], "note_en": "The generic Arrecife mortgage/dación/title row is relevant, but the exact EH 90/2012 identity, organ and complete primary file remain open.", "note_es": "La fila genérica hipotecaria/dación/título de Arrecife es relevante, pero siguen abiertos la identidad exacta EH 90/2012, el órgano y el expediente primario completo."},
    },
    "P03": {
        "arrecife": {"status": "DIRECT", "treatment": "CONTRADICTED", "master_ids": ["LZ-JUD-003", "LZ-APP-004"], "note_en": "The event was directly examined in DI 1103/2018-00 → DP 1132/2018 and Rollo 1010/2018 / Auto 804/2018 before AP Las Palmas Section Two; the confirmed provisional dismissal is adverse treatment, not confirmation of the allegation.", "note_es": "El evento fue examinado directamente en DI 1103/2018-00 → DP 1132/2018 y Rollo 1010/2018 / Auto 804/2018 ante la Sección Segunda de la AP de Las Palmas; el sobreseimiento provisional confirmado es tratamiento adverso, no confirmación de la alegación."},
    },
    "P05": {
        "calificacion": {"master_ids": ["GC-APP-004"]},
        "fiscalia": {"note_en": "Selected controlled subset: DI 248/2018, DI 22/2026, DIP 2/2026 and EG 49/2026. This is not the complete cross-office denominator.", "note_es": "Selección controlada: DI 248/2018, DI 22/2026, DIP 2/2026 y EG 49/2026. No es el denominador completo entre oficinas."},
    },
    "P06": {
        "tenerife": {"note_en": "Juicio Cambiario 1048/2019, ETJ 163/2020 and DP 748/2026 are separately registered files; no parent/continuation edge is asserted.", "note_es": "Juicio Cambiario 1048/2019, ETJ 163/2020 y DP 748/2026 son expedientes registrados por separado; no se afirma relación padre/continuación."},
    },
    "P07": {
        "historical": {"status": "OPEN", "treatment": "STATUS_UNRESOLVED", "note_en": "AP 89/2014 is verified; the broader Community/CEXP/unit family is unverified and requires case-by-case primary completion.", "note_es": "AP 89/2014 está verificado; la familia más amplia Comunidad/CEXP/unidades no está verificada y exige completitud primaria caso por caso."},
    },
    "P09": {
        "supervision": {"master_ids": ["GC-GOV-019", "GC-GOV-020"], "note_en": "DI 169/2026 and Alzada 286/2026 are the direct supervisory files. GC-LAJ-021 is a separate registration-only object and is not upgraded to a proceeding.", "note_es": "DI 169/2026 y Alzada 286/2026 son los expedientes supervisores directos. GC-LAJ-021 es un objeto registral separado y no se eleva a procedimiento."},
    },
    "P10": {
        "historical": {"status": "OPEN", "master_ids": ["LZ-JUD-001", "LZ-JUD-FAM-006"]},
        "concurso": {"status": "NOT_LOCATED", "master_ids": ["GC-JUD-001"]},
        "calificacion": {"status": "NOT_LOCATED", "master_ids": ["GC-APP-004"]},
        "removal": {"status": "CONTEXT", "master_ids": ["GC-APP-005", "GC-APP-006"]},
        "arrecife": {"status": "CONTEXT", "master_ids": ["LZ-JUD-003"]},
        "fiscalia": {"status": "CONTEXT", "master_ids": ["GC-FIS-013", "GC-FIS-017"]},
        "supervision": {"status": "NOT_LOCATED", "master_ids": ["GC-GOV-019", "GC-GOV-020"]},
    },
    "P11": {
        "historical": {"status": "OPEN", "master_ids": ["LZ-JUD-001", "LZ-JUD-FAM-006"]},
        "concurso": {"status": "OPEN", "master_ids": ["GC-JUD-001"]},
        "calificacion": {"status": "NOT_LOCATED", "master_ids": ["GC-APP-004"]},
        "removal": {"status": "CONTEXT", "master_ids": ["GC-APP-005", "GC-APP-006"]},
        "fiscalia": {"status": "CONTEXT", "master_ids": ["GC-FIS-013"]},
    },
    "P12": {
        "concurso": {"status": "DIRECT", "master_ids": ["GC-JUD-001"]},
        "calificacion": {"status": "CONTEXT", "master_ids": ["GC-APP-004"]},
        "removal": {"status": "CONTEXT", "master_ids": ["GC-APP-005", "GC-APP-006"]},
        "arrecife": {"status": "CONTEXT", "master_ids": ["LZ-JUD-003"]},
        "fiscalia": {"status": "CONTEXT", "master_ids": ["GC-FIS-013", "GC-FIS-017"]},
        "historical": {"status": "CONTEXT", "master_ids": ["LZ-JUD-001"]},
    },
    "P13": {
        "concurso": {"status": "CONTEXT", "master_ids": ["GC-JUD-001"]},
        "meetingpoint": {"status": "OPEN", "master_ids": ["GC-CONT-025"]},
        "fiscalia": {"status": "OPEN", "master_ids": ["GC-FIS-018"]},
        "publicmoney": {"status": "CONTEXT", "master_ids": ["X-REG-001"]},
    },
    "P14": {
        "concurso": {"status": "CONTEXT", "master_ids": ["GC-JUD-001"]},
        "calificacion": {"status": "NOT_LOCATED", "master_ids": ["GC-APP-004"]},
        "meetingpoint": {"status": "OPEN", "master_ids": ["GC-CONT-025"]},
        "fiscalia": {"status": "OPEN", "master_ids": ["GC-FIS-018"]},
        "publicmoney": {"status": "CONTEXT", "master_ids": ["X-REG-001"]},
    },
    "P15": {
        "concurso": {"status": "DIRECT", "master_ids": ["GC-JUD-001"]},
        "calificacion": {"status": "CONTEXT", "master_ids": ["GC-APP-004"]},
        "removal": {"status": "CONTEXT", "master_ids": ["GC-APP-005", "GC-APP-006"]},
        "arrecife": {"status": "OPEN", "master_ids": ["LZ-JUD-005"]},
        "fiscalia": {"status": "CONTEXT", "master_ids": ["GC-FIS-017", "GC-FIS-018"]},
        "historical": {"status": "CONTEXT", "master_ids": ["LZ-JUD-001"]},
        "publicmoney": {"status": "CONTEXT", "master_ids": ["NAT-AID-001"]},
    },
    "P16": {
        "concurso": {"status": "DIRECT", "master_ids": ["GC-JUD-001"]},
        "calificacion": {"status": "OPEN", "master_ids": ["GC-APP-004"]},
        "removal": {"status": "CONTEXT", "master_ids": ["GC-APP-005", "GC-APP-006"]},
        "fees": {"status": "CONTEXT", "master_ids": ["GC-CIV-027", "GC-APP-028"]},
        "arrecife": {"status": "CONTEXT", "master_ids": ["LZ-JUD-003", "LZ-JUD-005"]},
        "meetingpoint": {"status": "OPEN", "master_ids": ["GC-CONT-025"]},
        "fiscalia": {"status": "CONTEXT", "master_ids": ["GC-FIS-013", "GC-FIS-018"]},
        "historical": {"status": "CONTEXT", "master_ids": ["LZ-JUD-001"]},
        "publicmoney": {"status": "OPEN", "master_ids": ["NAT-AID-001"]},
    },
    "P17": {
        "concurso": {"status": "DIRECT", "master_ids": ["GC-JUD-001"]},
        "calificacion": {"status": "CONTEXT", "master_ids": ["GC-APP-004"]},
        "removal": {"status": "DIRECT", "master_ids": ["GC-APP-005", "GC-APP-006"]},
        "fees": {"status": "DIRECT", "master_ids": ["GC-CIV-027", "GC-APP-028"]},
        "fiscalia": {"status": "CONTEXT", "master_ids": ["GC-FIS-017", "GC-FIS-018"]},
        "supervision": {"status": "CONTEXT", "master_ids": ["GC-GOV-019", "GC-GOV-020"]},
    },
    "P18": {
        "concurso": {"status": "CONTEXT", "master_ids": ["GC-JUD-001"]},
        "calificacion": {"status": "OPEN", "master_ids": ["GC-APP-004"]},
        "meetingpoint": {"status": "OPEN", "master_ids": ["GC-CONT-025"]},
        "fiscalia": {"status": "OPEN", "master_ids": ["GC-FIS-018"]},
        "supervision": {"status": "CONTEXT", "master_ids": ["GC-GOV-019"]},
        "publicmoney": {
            "status": "DIRECT",
            "master_ids": ["NAT-AID-001", "NAT-TES-001"],
            "note_en": "NAT-TES-001 controls the first Treasury 7/2026 tranche, including 2024–2025 public RIC issue material; NAT-AID-001 remains the separate GC/836/P06 programme file. Their shared programme-dependency question is contextual across files and does not create procedural lineage.",
            "note_es": "NAT-TES-001 controla la primera entrega de Tesoro 7/2026, incluido material de emisiones públicas RIC 2024–2025; NAT-AID-001 sigue siendo el expediente separado del programa GC/836/P06. La cuestión compartida de dependencia del programa es contextual entre expedientes y no crea filiación procesal.",
        },
    },
    "P19": {
        "arrecife": {
            "status": "DIRECT",
            "treatment": "DIRECTLY_IN_FILE",
            "master_ids": ["LZ-JUD-043"],
            "note_en": "LZ-JUD-043 has a contemporaneous complaint and official summons. The summons says Juicio de faltas; a later summary says DP. One complainant and one affected party are recorded, the complaint attributes no direct physical act to Gil, and authority, corroboration, hearing occurrence and outcome remain open. This cell creates no procedural relationship or Concurso 36/2012 bridge.",
            "note_es": "LZ-JUD-043 cuenta con denuncia contemporánea y citación oficial. La citación dice Juicio de faltas; un resumen posterior dice DP. Constan una denunciante y un perjudicado, la denuncia no atribuye acto físico directo a Gil y siguen abiertos autoridad, corroboración, celebración de la vista y resultado. Esta celda no crea relación procesal ni puente con el Concurso 36/2012.",
            "representation_lineage_status": "PROCEEDING_SPECIFIC_DENOMINATOR_OPEN",
            "representation_gap_ids": ["CP-GAP-008"],
        },
    },
}


STATUS_TO_TREATMENT = {
    "DIRECT": "DIRECTLY_IN_FILE",
    "CONTEXT": "MATERIALLY_RELEVANT_CONTEXT",
    "OPEN": "STATUS_UNRESOLVED",
    "NOT_LOCATED": "NOT_RAISED_OR_NOT_LOCATED",
    "OUTSIDE": "OUTSIDE_PROCEDURAL_SCOPE",
}


def default_note(status: str, lane: dict, prop: dict) -> dict[str, str]:
    if status == "OUTSIDE":
        return bi(
            f"No decision dependency is asserted between {prop['id']} and this lane in the controlled public projection.",
            f"No se afirma dependencia decisoria entre {prop['id']} y esta vía en la proyección pública controlada.",
        )
    if status == "NOT_LOCATED":
        return bi(
            "Lane-specific treatment has not been located in the controlled corpus. This does not mean that no treatment exists.",
            "No se ha localizado tratamiento específico de esta vía en el corpus controlado. Esto no significa que no exista.",
        )
    if status == "OPEN":
        return bi(
            "A potentially material bridge is identified, but the source, receipt, treatment or procedural-availability chain is incomplete.",
            "Se identifica un puente potencialmente material, pero está incompleta la cadena de fuente, recepción, tratamiento o disponibilidad procesal.",
        )
    if status == "CONTEXT":
        return bi(
            "This lane contains materially relevant context only; no joinder, notice, reliance or merits treatment is inferred.",
            "Esta vía contiene solo contexto materialmente relevante; no se infiere acumulación, conocimiento, confianza ni tratamiento de fondo.",
        )
    return bi(
        "The proposition is directly present in the controlled lane; the treatment label states no more than the located record.",
        "La proposición está directamente presente en la vía controlada; la etiqueta de tratamiento no afirma más que el registro localizado.",
    )


def default_cell(prop: dict, lane: dict, status: str = "OUTSIDE") -> dict:
    note = default_note(status, lane, prop)
    active = status != "OUTSIDE"
    return {
        "status": status,
        "treatment": STATUS_TO_TREATMENT[status],
        "evidence_status": prop.get("source_status", "STATUS_UNRESOLVED"),
        "note_en": note["en"],
        "note_es": note["es"],
        "decision_en": prop["decision_dependency"]["en"] if active else "No decision dependency is asserted for this coordinate.",
        "decision_es": prop["decision_dependency"]["es"] if active else "No se afirma dependencia decisoria para esta coordenada.",
        "master_ids": [],
        "representation_lineage_status": "GLOBAL_DENOMINATOR_OPEN" if active else "NOT_APPLICABLE_TO_THIS_COORDINATE",
        "representation_gap_ids": ["CP-GAP-004", "CP-GAP-005"] if active else [],
    }


def complete_new_actionability(prop: dict) -> None:
    """Finish compact new rows that share the same confirm/refute discipline."""
    if prop["id"] == "P13":
        prop["actionability"]["if_confirmed"] = bi("The exact representation, recipient and reliance path can be tested.", "Puede contrastarse la manifestación exacta, su receptor y la vía de confianza.")
        prop["actionability"]["if_refuted"] = bi("The promotion should be treated as conditional, corrected or unsupported rather than knowingly false.", "La promoción debe tratarse como condicionada, corregida o no respaldada y no como falsedad consciente.")
    elif prop["id"] == "P14":
        prop["actionability"]["if_confirmed"] = bi("The decision-maker's knowledge and response to fragmented title can be established.", "Puede establecerse el conocimiento y respuesta del decisor ante el título fragmentado.")
        prop["actionability"]["if_refuted"] = bi("The knowledge checkpoint must be removed or reduced to an unauthenticated report.", "El punto de conocimiento debe eliminarse o reducirse a un informe no autenticado.")
    elif prop["id"] == "P15":
        prop["actionability"]["if_confirmed"] = bi("Later title/value/condition consequences can be reconciled finca by finca.", "Pueden conciliarse finca por finca las consecuencias posteriores de título/valor/condición.")
        prop["actionability"]["if_refuted"] = bi("The asserted adjudication perimeter or downstream title consequence must be corrected.", "Debe corregirse el perímetro de adjudicación o la consecuencia posterior de título afirmada.")
    elif prop["id"] == "P16":
        prop["actionability"]["if_confirmed"] = bi("Income, value, benefit and loss can be quantified and attributed.", "Pueden cuantificarse y atribuirse ingresos, valor, beneficio y pérdida.")
        prop["actionability"]["if_refuted"] = bi("The economic-consequence theory must be narrowed to what the accounts support.", "La teoría de consecuencia económica debe limitarse a lo respaldado por las cuentas.")
    elif prop["id"] == "P17":
        prop["actionability"]["if_confirmed"] = bi("Each act and remedy can be determined in its correct removal or remuneration lane.", "Cada acto y remedio puede determinarse en su vía correcta de separación o remuneración.")
        prop["actionability"]["if_refuted"] = bi("The challenged act or monetary consequence should be removed from that lane.", "El acto impugnado o consecuencia monetaria debe eliminarse de esa vía.")
    elif prop["id"] == "P18":
        prop["actionability"]["if_confirmed"] = bi("A programme-specific review or recovery question may arise without implying criminality.", "Puede surgir una revisión o reintegro específico del programa sin implicar criminalidad.")
        prop["actionability"]["if_refuted"] = bi("The public-money allegation must be withdrawn for that programme.", "La alegación de fondos públicos debe retirarse para ese programa.")


def build() -> dict:
    data = json.loads(SEED.read_text(encoding="utf-8"))
    existing = {prop["id"]: prop for prop in data.get("propositions", [])}

    for prop_id in NEW_PROP_IDS:
        if prop_id not in existing:
            existing[prop_id] = {"id": prop_id, "cells": {}}

    for prop_id, rich in RICH.items():
        prop = existing[prop_id]
        prop.update(rich)
        prop.pop("period", None)
        prop.setdefault("sort", 9999)
        prop.setdefault("source_status", "STATUS_UNRESOLVED")
        prop.setdefault("attribution", "OPEN_QUESTION")
        prop.setdefault("title_en", prop_id)
        prop.setdefault("title_es", prop_id)
        prop.setdefault("question_en", prop["title_en"])
        prop.setdefault("question_es", prop["title_es"])
        prop.pop("if_confirmed", None)
        prop.setdefault("audience_priority", {})
        for rank, audience in enumerate([row[0] for row in AUDIENCES]):
            prop["audience_priority"].setdefault(audience, int(prop.get("sort", 9999) * 10 + rank))
        complete_new_actionability(prop)

    # Preserve the original hand-curated priorities and give appellate readers
    # an explicit three-object ordering.
    existing["P04"]["audience_priority"]["appellate"] = 0
    existing["P17"]["audience_priority"]["appellate"] = 1
    existing["P01"]["audience_priority"]["appellate"] = 2
    existing["P10"]["audience_priority"].update({"owner": 0, "court": 2})
    existing["P11"]["audience_priority"].update({"owner": 1})
    existing["P12"]["audience_priority"].update({"owner": 2, "professional": 3})
    existing["P13"]["audience_priority"].update({"professional": 0, "research": 3})
    existing["P14"]["audience_priority"].update({"professional": 1, "authority": 2})
    existing["P15"]["audience_priority"].update({"owner": 3, "court": 5})
    existing["P16"]["audience_priority"].update({"owner": 4, "authority": 3})
    existing["P18"]["audience_priority"].update({"authority": 0, "professional": 2})
    existing["P19"]["audience_priority"].update({"all": 4, "court": 2, "appellate": 190, "fiscal": 1, "supervision": 5, "authority": 0, "research": 9, "owner": 3, "professional": 8})

    lane_by_id = {lane["id"]: lane for lane in LANES}
    for prop in existing.values():
        old_cells = prop.get("cells", {})
        explicit = {}
        for lane in LANES:
            cell = default_cell(prop, lane)
            if lane["id"] in old_cells:
                old = old_cells[lane["id"]]
                cell = default_cell(prop, lane, old.get("status", "OPEN"))
                cell.update(old)
                cell["treatment"] = old.get("treatment", STATUS_TO_TREATMENT[cell["status"]])
                cell["evidence_status"] = old.get("evidence_status", prop["source_status"])
                cell["decision_en"] = old.get("decision_en", prop["decision_dependency"]["en"])
                cell["decision_es"] = old.get("decision_es", prop["decision_dependency"]["es"])
                cell["representation_lineage_status"] = old.get("representation_lineage_status", "GLOBAL_DENOMINATOR_OPEN")
                cell["representation_gap_ids"] = old.get("representation_gap_ids", ["CP-GAP-004", "CP-GAP-005"])
            override = CELL_OVERRIDES.get(prop["id"], {}).get(lane["id"])
            if override:
                status = override.get("status", cell["status"])
                baseline = default_cell(prop, lane, status)
                baseline.update(cell)
                baseline.update(override)
                baseline["status"] = status
                baseline["treatment"] = override.get("treatment", STATUS_TO_TREATMENT[status])
                if not override.get("note_en") and lane["id"] not in old_cells:
                    note = default_note(status, lane, prop)
                    baseline["note_en"], baseline["note_es"] = note["en"], note["es"]
                baseline["decision_en"] = prop["decision_dependency"]["en"]
                baseline["decision_es"] = prop["decision_dependency"]["es"]
                baseline["representation_lineage_status"] = override.get(
                    "representation_lineage_status",
                    "GLOBAL_DENOMINATOR_OPEN" if status != "OUTSIDE" else "NOT_APPLICABLE_TO_THIS_COORDINATE",
                )
                baseline["representation_gap_ids"] = override.get(
                    "representation_gap_ids",
                    ["CP-GAP-004", "CP-GAP-005"] if status != "OUTSIDE" else [],
                )
                cell = baseline
            explicit[lane["id"]] = cell
        prop["cells"] = explicit

    # Cell-specific treatment that must not be inferred from relationship type.
    existing["P03"]["cells"]["arrecife"]["treatment"] = "CONTRADICTED"
    existing["P04"]["cells"]["calificacion"]["treatment"] = "DIRECTLY_IN_FILE"
    existing["P04"]["cells"]["removal"]["treatment"] = "DIRECTLY_IN_FILE"
    existing["P04"]["cells"]["fees"]["treatment"] = "DIRECTLY_IN_FILE"
    existing["P09"]["cells"]["supervision"]["treatment"] = "DIRECTLY_IN_FILE"
    existing["P18"]["cells"]["publicmoney"]["treatment"] = "DIRECTLY_IN_FILE"

    data.update({
        "schema_version": "2.0.0",
        "status": "PUBLIC_DERIVED_CASE_PRISM_ACTIONABLE",
        "source_catalog": SOURCES,
        "evidence_statuses": evidence_status_catalog(),
        "treatments": {
            "DIRECTLY_IN_FILE": bi("Directly in file", "Directamente en el expediente"),
            "EXPRESSLY_ACKNOWLEDGED": bi("Expressly acknowledged", "Reconocido expresamente"),
            "RELIED_UPON": bi("Relied upon", "Utilizado como fundamento"),
            "CONTRADICTED": bi("Contradicted / adverse treatment", "Contradicho / tratamiento adverso"),
            "MATERIALLY_RELEVANT_CONTEXT": bi("Materially relevant context", "Contexto materialmente relevante"),
            "NOT_RAISED_OR_NOT_LOCATED": bi("Not raised / not located", "No planteado / no localizado"),
            "OUTSIDE_PROCEDURAL_SCOPE": bi("Outside procedural scope", "Fuera del ámbito procesal"),
            "STATUS_UNRESOLVED": bi("Treatment unresolved", "Tratamiento no resuelto"),
        },
        "attribution_classes": {
            "DOCUMENTED_FACT": bi("Documented fact", "Hecho documentado"),
            "SOURCE_AUTHORED_STATEMENT": bi("Source-authored statement", "Manifestación de la fuente"),
            "PARTY_SUBMISSION_AND_PROCEDURAL_RECORD": bi("Party submission and procedural record", "Alegación de parte y registro procesal"),
            "OPEN_QUESTION": bi("Open question", "Pregunta abierta"),
        },
        "audience_lenses": lens_rows(),
        "lanes": LANES,
        "propositions": sorted(existing.values(), key=lambda p: (float(p.get("sort", 9999)), p["id"])),
        "coverage": {
            "proposition_count": len(existing),
            "lane_count": len(LANES),
            "coordinate_count": len(existing) * len(LANES),
            "explicit_coordinate_count": len(existing) * len(LANES),
            "unexplained_coordinate_count": 0,
            "counsel_procurador_denominator": "GAP",
            "counsel_procurador_gap_ids": ["CP-GAP-004", "CP-GAP-005"],
        },
    })
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the committed public projection is not in builder-normalised form",
    )
    args = parser.parse_args()
    output = build()
    rendered = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if TARGET.read_text(encoding="utf-8") != rendered:
            print(f"{TARGET.relative_to(ROOT)} is stale; run {Path(__file__).name}", flush=True)
            return 1
        print(f"{TARGET.relative_to(ROOT)} matches the Case Prism v2 builder", flush=True)
        return 0

    TARGET.write_text(rendered, encoding="utf-8")
    print(
        f"wrote {TARGET.relative_to(ROOT)}: "
        f"{output['coverage']['proposition_count']} propositions × "
        f"{output['coverage']['lane_count']} lanes = "
        f"{output['coverage']['coordinate_count']} explicit coordinates"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

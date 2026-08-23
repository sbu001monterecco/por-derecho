#!/usr/bin/env python3
"""Build the redacted full-text corpus for the two AC procedural tracks.

The private source set is intentionally not committed.  This builder accepts the
controlled local source directory, extracts page-addressable text from PDFs (or
plain text from DOCX), removes administrative/contact/verification data, and
writes the public Markdown corpus plus a machine-readable manifest.

Redaction is deliberately narrow: it removes court administrative headers,
contact and identity numbers, bank/verification data, electronic-signature
metadata and names of non-decision-making procedural professionals.  It does
not rewrite the allegations, reasoning or operative parts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_ROOT = ROOT / "tmp/pdfs/ac-core"
DEFAULT_OUTPUT_ROOT = ROOT / "evidence/insolvency-36-2012/concurso-autos/full-text"
DEFAULT_MANIFEST = ROOT / "assets/data/concurso36-autos-fulltext-v1.json"


@dataclass(frozen=True)
class Document:
    id: str
    lane: str
    date: str
    title: str
    actor: str
    instrument: str
    procedure: str
    source: str
    source_anchor: str
    start: str
    public_status: str = "Copia fuente localizada"
    editorial_notes: tuple[str, ...] = field(default_factory=tuple)
    outcome: str = ""
    merits: str = "No aplica: escrito o trámite procesal."
    public_pdf: str = ""

    @property
    def output_name(self) -> str:
        return f"{self.id}-{slug(self.title)}-redacted.md"


DOCUMENTS: tuple[Document, ...] = (
    Document(
        "R01", "separacion", "2025-04-23",
        "Solicitud de separación del Administrador Concursal",
        "Aweswell Limited", "Solicitud de parte", "Concurso 36/2012 · Sección 2.ª",
        "removal-application-source.pdf",
        "Paquete aportado, pp. 23–80; Gmail 19663da50d6eb73e",
        "party",
        editorial_notes=(
            "La fuente menciona «Disposición Adicional Tercera»; el control normativo del repositorio identifica como referencia correcta la Disposición Transitoria Tercera de la Ley 25/2015. La transcripción conserva la etiqueta usada por el escrito.",
            "El índice del escrito salta aparentemente del Documento 5 al Documento 7. Se conserva el salto y no se presume el contenido de un eventual Documento 6.",
        ),
    ),
    Document(
        "R02", "separacion", "2025-04-28",
        "Diligencia de traslado de la solicitud de separación",
        "LAJ Águeda Reyes Almeida", "Diligencia de ordenación", "Concurso 36/2012 · Sección 2.ª",
        "gmail/removal-laj-transfer-2025-04-28.pdf", "Gmail 196c920189b01dbe", "court",
        editorial_notes=(
            "La diligencia atribuye el escrito a la representación de Gil Marer, mientras la solicitud transcrita se presenta bajo la representación de Aweswell Limited. Se conserva la diferencia de identificación sin corregirla por inferencia.",
        ),
        outcome="Incorpora el escrito y concede cinco días al Administrador Concursal para alegaciones.",
        public_pdf="evidence/insolvency-36-2012/concurso-autos/public-pdfs/laj-28abr2025-traslado-separacion-public-redacted.pdf",
    ),
    Document(
        "R03", "separacion", "2025-05-12",
        "Oposición del Administrador Concursal a la separación",
        "Administrador Concursal", "Escrito de oposición", "Concurso 36/2012 · Sección 2.ª",
        "gmail/removal-ac-opposition-2025-05-12.pdf", "Gmail 196f702b5820ec1a", "party",
    ),
    Document(
        "R04", "separacion", "2025-05-20",
        "Diligencia de unión de la oposición y puesta a resolver",
        "LAJ Águeda Reyes Almeida", "Diligencia de ordenación", "Concurso 36/2012 · Sección 2.ª",
        "gmail/removal-laj-table-for-decision-2025-05-20.pdf", "Gmail 196f702b5820ec1a", "court",
        outcome="Une la oposición y pone las actuaciones sobre la mesa del juez para resolver.",
        public_pdf="evidence/insolvency-36-2012/concurso-autos/public-pdfs/laj-20may2025-puesta-a-resolver-public-redacted.pdf",
    ),
    Document(
        "R05", "separacion", "2025-09-12",
        "Auto 1377/2025 sobre la solicitud de separación",
        "Magistrado-juez Alberto López Villarrubia", "Auto", "Concurso 36/2012 · Sección 2.ª",
        "auto-1377-source.pdf", "Paquete aportado, pp. 81–83; Gmail 19952646b51e374b", "court",
        editorial_notes=(
            "El fundamento reproduce el artículo 3 TRLC y después contiene una remisión interna al «apartado tercero del artículo 100». La transcripción conserva literalmente esa referencia.",
        ),
        outcome="Desestima la solicitud por falta de legitimación activa de Aweswell.",
        merits="No entra en los motivos de fondo; lo declara expresamente.",
        public_pdf="evidence/insolvency-36-2012/ac-removal-fees/auto-1377-2025-removal-public-redacted.pdf",
    ),
    Document(
        "R06", "separacion", "2025-09-12",
        "Auto que deniega aclarar la providencia de 25 de julio",
        "Magistrado-juez Alberto López Villarrubia", "Auto complementario", "Concurso 36/2012 · Sección 1.ª",
        "auto-clarification-source.pdf", "Paquete aportado, pp. 84–85", "court",
        editorial_notes=(
            "Este auto no es la resolución del recurso contra el Auto 1377/2025. Resuelve una solicitud distinta de aclaración de una providencia sobre exhibición documental y se publica como antecedente complementario.",
        ),
        outcome="No aclara la providencia de 25 de julio de 2025.",
        merits="No decide la solicitud de separación.",
        public_pdf="evidence/insolvency-36-2012/concurso-autos/public-pdfs/auto-12sep2025-aclaracion-providencia-public-redacted.pdf",
    ),
    Document(
        "R07", "separacion", "2025-09-21",
        "Recurso de reposición de Aweswell contra el Auto 1377/2025",
        "Aweswell Limited", "Recurso de reposición", "Concurso 36/2012 · Sección 2.ª",
        "gmail/removal-reconsideration-aweswell-2025-09-19.docx", "Gmail 19962e9c78aaf74d", "party",
        public_status="Copia editable remitida por letrado; el corpus no contiene acuse independiente",
        editorial_notes=(
            "El encabezamiento de la copia editable identifica representación de Gil Marer aunque el cuerpo recurre por Aweswell. Se conserva la diferencia y no se homogeneiza por inferencia.",
        ),
    ),
    Document(
        "R08", "separacion", "2025-09-22",
        "Recurso de reposición de LPB contra el Auto 1377/2025",
        "Luchy Playa Blanca, S.L.U.", "Recurso de reposición", "Concurso 36/2012 · Sección 2.ª",
        "gmail/removal-reconsideration-lpb-2025-09-21.docx", "Gmail 1996d275177e44a8", "party",
        public_status="Copia editable remitida por letrado; el corpus no contiene acuse independiente",
    ),
    Document(
        "R09", "separacion", "2025-11-11",
        "Auto que resuelve los recursos de reposición",
        "Magistrado-juez Alberto López Villarrubia", "Auto", "Concurso 36/2012 · Sección 2.ª",
        "auto-reconsideration-source.pdf", "Paquete aportado, pp. 86–89; Gmail 19a7d06c03e1c731", "court",
        editorial_notes=(
            "En el apartado dedicado a LPB aparece Aweswell en una frase final; la parte dispositiva desestima separadamente ambos recursos. Se conserva el desajuste nominal.",
        ),
        outcome="Desestima los recursos de LPB y Aweswell, confirma el auto y no impone costas.",
        merits="Mantiene la barrera procesal; añade una apreciación ex officio de ausencia de indicios, pero no realiza una adjudicación documental de cada motivo de separación.",
        public_pdf="evidence/insolvency-36-2012/ac-removal-fees/auto-11nov2025-reconsideration-public-redacted.pdf",
    ),
    Document(
        "R10", "separacion", "2025-12-09",
        "Recurso de apelación de LPB",
        "Luchy Playa Blanca, S.L.U.", "Recurso de apelación", "RPL 3304/2025",
        "gmail/removal-appeal-lpb-2025-12-09.pdf", "Gmail 19b04094f9c30145", "party",
    ),
    Document(
        "R11", "separacion", "2025-12-10",
        "Recurso de apelación de Aweswell",
        "Aweswell Limited", "Recurso de apelación", "RPL 3319/2025",
        "gmail/removal-appeal-aweswell-2025-12-10.pdf", "Gmail 19b0796510d29c61", "party",
    ),
    Document(
        "R12", "separacion", "2026-01-28",
        "Diligencia de formación del RPL 3319/2025",
        "LAJ María Victoria Henríquez Santana", "Diligencia de ordenación", "RPL 3319/2025",
        "gmail/removal-laj-appeal-elevation-aweswell-2026-01-28.pdf", "Gmail 19c065bd368bf2fd", "court",
        outcome="Forma el rollo, designa ponente y requiere elevación, emplazamiento y depósito.",
    ),
    Document(
        "R13", "separacion", "2026-02-20",
        "Diligencia y cédula de emplazamiento en la apelación",
        "LAJ del órgano de origen", "Cédula de emplazamiento", "Concurso 36/2012 · RPL 3319/2025",
        "gmail/removal-laj-appeal-summons-lpb-2026-02-20.pdf", "Gmail 19c8a7b4d4fe393d", "court",
        outcome="Emplaza a LPB para comparecer ante la Audiencia Provincial.",
    ),
    Document(
        "R14", "separacion", "2026-02-20",
        "Diligencia de remisión y emplazamiento a segunda instancia",
        "LAJ del órgano de origen", "Diligencia de ordenación", "Concurso 36/2012 · RPL 3319/2025",
        "gmail/removal-laj-remission-summons-2026-02-20.pdf", "Gmail 19c8a7b4d4fe393d", "court",
        outcome="Ordena la remisión/visibilidad de actuaciones y el emplazamiento correspondiente.",
    ),
    Document(
        "R15", "separacion", "2026-02-23",
        "Personación de LPB en el RPL 3319/2025",
        "Luchy Playa Blanca, S.L.U.", "Escrito de personación", "RPL 3319/2025",
        "gmail/removal-appeal-appearance-lpb-2026-02-23.pdf", "Gmail 19c8a7b4d4fe393d", "party",
    ),
    Document(
        "R16", "separacion", "2026-03-25",
        "Diligencia de formación del RPL 3304/2025",
        "LAJ Francisco Javier Labella Ribes", "Diligencia de ordenación", "RPL 3304/2025",
        "gmail/removal-laj-appeal-elevation-2026-03-25.pdf", "Gmail 19d25c002b6c122d", "court",
        editorial_notes=(
            "La diligencia dice «Auto de fecha 11/11/2026»; el auto recurrido incorporado al expediente es de 11/11/2025. Se conserva el año escrito en la resolución y se señala el desajuste.",
        ),
        outcome="Forma el rollo, designa ponente y requiere elevación, emplazamiento y depósito.",
    ),
    Document(
        "R17", "separacion", "2026-04-17",
        "Impugnación de LPB a la resolución apelada",
        "Luchy Playa Blanca, S.L.U.", "Escrito de impugnación", "RPL 3319/2025",
        "gmail/removal-appeal-impugnation-lpb-2026-04-16.docx", "Gmail 19d96cc44c8ff878", "party",
        public_status="Copia editable remitida por letrado; la diligencia de 19 de mayo registra el escrito",
    ),
    Document(
        "R18", "separacion", "2026-04-29",
        "Oposición del Administrador Concursal a la apelación de Aweswell",
        "Administrador Concursal", "Escrito de oposición", "RPL 3319/2025",
        "gmail/removal-ap-ac-opposition-aweswell-appeal-2026-05-11.pdf", "Gmail 19e49b22de990be2", "party",
    ),
    Document(
        "R19", "separacion", "2026-05-05",
        "Diligencia que tiene por impugnada la resolución apelada",
        "LAJ de la Sección Cuarta", "Diligencia de ordenación", "RPL 3319/2025",
        "gmail/removal-ap-laj-opposition-impugnation-2026-05-05.pdf", "Gmail 19df8a5b371ed339", "court",
        outcome="Tiene por formalizada la impugnación de LPB y ordena su traslado.",
    ),
    Document(
        "R20", "separacion", "2026-05-11",
        "Reposición del Administrador Concursal contra la diligencia de 5 de mayo",
        "Administrador Concursal", "Recurso de reposición", "RPL 3319/2025",
        "gmail/removal-ap-ac-reconsideration-2026-05-11.pdf", "Gmail 19e49b22de990be2", "party",
        editorial_notes=(
            "El antecedente primero fecha la solicitud de separación el 23 de marzo de 2025; la solicitud fuente está fechada el 23 de abril de 2025. Se conserva el mes escrito en el recurso.",
        ),
    ),
    Document(
        "R21", "separacion", "2026-05-19",
        "Diligencia de traslado del recurso de reposición del AC",
        "LAJ Amelia Villarreal Sancho", "Diligencia de ordenación", "RPL 3319/2025",
        "gmail/removal-ap-laj-transfer-ac-reconsideration-2026-05-19.pdf", "Gmail 19e49b22de990be2", "court",
        outcome="Admite la reposición del AC y concede cinco días comunes para impugnarla.",
    ),
    Document(
        "R22", "separacion", "2026-05-19",
        "Diligencia de traslado de oposición e impugnación",
        "LAJ de la Sección Cuarta", "Diligencia de ordenación", "RPL 3319/2025",
        "gmail/removal-ap-laj-appeal-opposition-and-impugnation-2026-05-19.pdf", "Gmail 19e49b22de990be2", "court",
        editorial_notes=(
            "El cuerpo identifica a Amelia Villarreal Sancho y el bloque de firma electrónica a Francisco Javier Labella Ribes. Ambos datos se conservan como aparecen en la fuente.",
        ),
        outcome="Traslada a la apelante la oposición del AC y la impugnación de LPB por diez días.",
    ),
    Document(
        "R23", "separacion", "2026-05-22",
        "Impugnación de LPB a la reposición del Administrador Concursal",
        "Luchy Playa Blanca, S.L.U.", "Escrito de impugnación", "RPL 3319/2025",
        "gmail/removal-ap-opposition-ac-reconsideration-2026-05-22.docx", "Gmail 19e4e9d5364218d5", "party",
        public_status="Copia editable remitida por letrado; existe acuse separado en el correo de 22 de mayo",
    ),
    Document(
        "R24", "separacion", "2026-05-25",
        "Impugnación de Aweswell a la reposición del Administrador Concursal",
        "Aweswell Limited", "Escrito de impugnación", "RPL 3319/2025",
        "gmail/removal-ap-opposition-ac-reconsideration-aweswell-2026-05-25.docx", "Gmail 19e5fc3ae1a5ab58", "party",
        public_status="Copia editable remitida por letrado; el corpus no contiene acuse independiente",
    ),
    Document(
        "R25", "separacion", "2026-06-02",
        "Manifestaciones de Aweswell al amparo del artículo 461.4 LEC",
        "Aweswell Limited", "Escrito de manifestaciones", "RPL 3319/2025",
        "gmail/removal-appeal-allegations-461-4-2026-06-02.docx", "Gmail 19e8772593ab4016", "party",
        public_status="Copia editable remitida por letrado; el corpus no contiene acuse independiente",
    ),
    Document(
        "R26", "separacion", "2026-06-09",
        "Providencia de señalamiento para estudio, votación y fallo",
        "Sección Cuarta de la Audiencia Provincial", "Providencia", "RPL 3304/2025",
        "gmail/removal-ap-providencia-hearing-2026-06-09.pdf", "Gmail 19eb0de9f7d935b6", "court",
        outcome="Señala estudio, votación y fallo y resuelve sobre la documentación entonces aportada.",
    ),
    Document(
        "R27", "separacion", "2026-06-10",
        "Aportación documental de LPB al amparo del artículo 271.2 LEC",
        "Luchy Playa Blanca, S.L.U.", "Escrito de aportación documental", "RPL 3304/2025",
        "gmail/removal-ap-evidence-lpb-2026-06-10.docx", "Gmail 19eb0de9f7d935b6", "party",
        public_status="Copia editable remitida por letrado; la diligencia de 19 de junio registra la aportación",
    ),
    Document(
        "R28", "separacion", "2026-06-19",
        "Diligencia que promueve la acumulación desde el RPL 3304/2025",
        "LAJ Francisco Javier Labella Ribes", "Diligencia de ordenación", "RPL 3304/2025",
        "gmail/removal-ap-laj-accumulation-1-2026-06.pdf", "Gmail 19ee061600a5d9b0", "court",
        outcome="Promueve acumulación de oficio y concede audiencia común de diez días.",
    ),
    Document(
        "R29", "separacion", "2026-06-19",
        "Diligencia sobre acumulación en el RPL 3319/2025",
        "LAJ Amelia Villarreal Sancho", "Diligencia de ordenación", "RPL 3319/2025",
        "gmail/removal-ap-laj-accumulation-2-2026-06.pdf", "Gmail 19ee061600a5d9b0", "court",
        outcome="Deja sin efecto una diligencia anterior y queda a lo resuelto en el rollo más antiguo.",
    ),
    Document(
        "R30", "separacion", "2026-07-15",
        "Auto 223/2026 de acumulación de apelaciones",
        "Sección Cuarta de la Audiencia Provincial", "Auto", "RPL 3304/2025 + RPL 3319/2025",
        "gmail/removal-ap-auto-223-2026-07-15.pdf", "Gmail 19f8a422471edc64", "court",
        outcome="Acumula el RPL 3319/2025 al RPL 3304/2025 y ordena completar trámites.",
        merits="No resuelve el fondo de la separación.",
        public_pdf="evidence/insolvency-36-2012/concurso-autos/public-pdfs/auto-223-2026-acumulacion-public-redacted.pdf",
    ),
    Document(
        "R31", "separacion", "2026-07-23",
        "Alegaciones de LPB tras el Auto 223/2026",
        "Luchy Playa Blanca, S.L.U.", "Escrito de alegaciones", "RPL 3304/2025 acumulado",
        "gmail/removal-ap-allegations-lpb-2026-07-24.pdf", "Gmail 19f938cf72496e5b", "party",
    ),
    Document(
        "R32", "separacion", "2026-07-24",
        "Alegaciones de Aweswell tras el Auto 223/2026",
        "Aweswell Limited", "Escrito de alegaciones", "RPL 3304/2025 acumulado",
        "gmail/removal-ap-allegations-aweswell-2026-07-24.pdf", "Gmail 19f938cf72496e5b", "party",
    ),
    Document(
        "F01", "honorarios", "2024-09-01",
        "Demanda de responsabilidad y reintegro de honorarios a la masa",
        "Aweswell Limited", "Demanda de juicio ordinario", "ORD 641/2024 · origen 582/2024",
        "fee-claim-source.pdf", "Paquete aportado, pp. 2–22; Gmail 193a8015d8eee373", "party",
        editorial_notes=(
            "La demanda denomina «Disposición Adicional Tercera» a la regla temporal de remuneración. El control normativo del repositorio identifica como referencia correcta la Disposición Transitoria Tercera de la Ley 25/2015. La transcripción conserva la formulación original.",
        ),
    ),
    Document(
        "F02", "honorarios", "2024-10-07",
        "Decreto 113/2024 de inhibición a favor del Juzgado Mercantil 1",
        "LAJ del Juzgado Mercantil 2", "Decreto", "ORD 582/2024 → ORD 641/2024",
        "gmail/fees-auto-inhibition-2024-10-08.pdf", "Gmail (fuente recuperada del expediente de honorarios)", "court",
        editorial_notes=(
            "La parte dispositiva dice «SE ACUERDA LA INHIBICIÓN del Juzgado de lo Mercantil nº 1» aunque la resolución procede del Juzgado Mercantil 2 y ordena remitir al Mercantil 1. Se conserva literalmente la frase.",
            "El bloque de firma electrónica identifica a Miriam González Marrero mientras el cierre del texto menciona a Román García-Varela Iglesias. Se conserva el desajuste de la fuente.",
        ),
        outcome="Declara la inhibición y remite el asunto al órgano que conoce del Concurso 36/2012.",
        public_pdf="evidence/insolvency-36-2012/concurso-autos/public-pdfs/decreto-113-2024-inhibicion-public-redacted.pdf",
    ),
    Document(
        "F03", "honorarios", "2024-11-28",
        "Decreto de admisión de la demanda de honorarios",
        "LAJ Águeda Reyes Almeida", "Decreto", "ORD 641/2024",
        "gmail/fees-admission-2-2024-11-28.pdf", "Gmail (fuente recuperada del expediente de honorarios)", "court",
        outcome="Admite la demanda, fija cuantía de 110.956,97 euros y emplaza a los demandados.",
        public_pdf="evidence/insolvency-36-2012/concurso-autos/public-pdfs/decreto-28nov2024-admision-honorarios-public-redacted.pdf",
    ),
    Document(
        "F04", "honorarios", "2024-11-28",
        "Diligencia de emplazamiento electrónico de la aseguradora",
        "LAJ Águeda Reyes Almeida", "Diligencia de ordenación", "ORD 641/2024",
        "gmail/fees-admission-1-2024-11-28.pdf", "Gmail (fuente recuperada del expediente de honorarios)", "court",
        outcome="Ordena el emplazamiento electrónico de la aseguradora.",
    ),
    Document(
        "F05", "honorarios", "2025-01-07",
        "Contestación de la aseguradora a la demanda",
        "Occident GCO, S.A.U.", "Contestación a la demanda", "ORD 641/2024",
        "gmail/fees-insurer-opposition-2025-01-07.pdf", "Gmail 19442467f65c63e5", "party",
    ),
    Document(
        "F06", "honorarios", "2025-01-08",
        "Contestación del Administrador Concursal a la demanda",
        "Administrador Concursal", "Contestación a la demanda", "ORD 641/2024",
        "gmail/fees-ac-opposition-2025-01-08.pdf", "Gmail 195afde2fddd8c0d", "party",
    ),
    Document(
        "F07", "honorarios", "2025-03-17",
        "Diligencia que tiene por contestada la demanda y convoca audiencia previa",
        "LAJ Águeda Reyes Almeida", "Diligencia de ordenación", "ORD 641/2024",
        "gmail/fees-laj-defences-hearing-2025-03-19.pdf", "Gmail 195afdddc67acf6e", "court",
        outcome="Incorpora ambas contestaciones y convoca audiencia previa.",
    ),
    Document(
        "F08", "honorarios", "2025-03-26",
        "Alegaciones de Aweswell tras las contestaciones",
        "Aweswell Limited", "Escrito de alegaciones", "ORD 641/2024",
        "gmail/fees-allegations-timeliness-2025-03-26.docx", "Gmail 195d37a036038b9d", "party",
        public_status="Copia editable remitida por letrado; el corpus no contiene acuse independiente",
    ),
    Document(
        "F09", "honorarios", "2025-09-02",
        "Diligencia que vuelve a señalar audiencia previa",
        "LAJ Águeda Reyes Almeida", "Diligencia de ordenación", "ORD 641/2024",
        "gmail/fees-hearing-setting-2025-09-10.pdf", "Gmail 19937d11d054046c", "court",
        outcome="Señala audiencia previa para el 20 de enero de 2026 y difiere la prueba al acto.",
    ),
    Document(
        "F10", "honorarios", "2025-09-08",
        "Solicitud de aclaración de Aweswell sobre el Decreto de 1 de septiembre",
        "Aweswell Limited", "Solicitud de aclaración", "ORD 641/2024",
        "gmail/fees-clarification-request-2026-01.pdf", "Gmail 19928fb34997d4e7", "party",
        editorial_notes=(
            "El escrito refiere alternativamente una diligencia de 26 de marzo de 2025 y un decreto de 1 de septiembre de 2025. Ninguna de esas dos resoluciones se encuentra como archivo autónomo en el corpus fuente recuperado.",
        ),
    ),
    Document(
        "F11", "honorarios", "2025-09-23",
        "Oposición del Administrador Concursal a la aclaración",
        "Administrador Concursal", "Escrito de oposición", "ORD 641/2024",
        "gmail/fees-clarification-opposition-ac-2025-09.pdf", "Gmail 199850dae6b3e23a", "party",
    ),
    Document(
        "F12", "honorarios", "2025-09-24",
        "Oposición de la aseguradora a la aclaración",
        "Occident GCO, S.A.U.", "Escrito de oposición", "ORD 641/2024",
        "gmail/fees-clarification-opposition-insurer-2025-09.pdf", "Gmail 199850dae6b3e23a", "party",
    ),
    Document(
        "F13", "honorarios", "2026-01-21",
        "Sentencia 4/2026 sobre la demanda de honorarios",
        "Magistrado-juez Alberto López Villarrubia", "Sentencia", "ORD 641/2024",
        "fee-judgment-source.pdf", "Paquete aportado, pp. 90–94; Gmail 19bfb3134cbaf69a", "court",
        outcome="Desestima la demanda por falta de legitimación activa e impone costas a Aweswell.",
        merits="No entra en las restantes defensas ni decide si los honorarios e intereses eran debidos.",
        public_pdf="evidence/insolvency-36-2012/concurso-autos/public-pdfs/sentencia-4-2026-honorarios-public-redacted.pdf",
    ),
    Document(
        "F14", "honorarios", "2026-01-21",
        "Decreto que deniega la aclaración del decreto de 1 de septiembre",
        "LAJ Águeda Reyes Almeida", "Decreto", "ORD 641/2024",
        "gmail/fees-laj-decree-no-clarification-2026-01.pdf", "Gmail 19bfb3134cbaf69a", "court",
        outcome="No aclara el decreto de 1 de septiembre de 2025.",
        merits="No resuelve la legalidad ni cuantía de los honorarios.",
        public_pdf="evidence/insolvency-36-2012/concurso-autos/public-pdfs/decreto-21ene2026-no-aclaracion-public-redacted.pdf",
    ),
    Document(
        "F15", "honorarios", "2026-02-23",
        "Recurso de apelación de Aweswell contra la Sentencia 4/2026",
        "Aweswell Limited", "Recurso de apelación", "RPL 421/2026",
        "gmail/fees-appeal-aweswell-2026-02.pdf", "Gmail 19c8a7b4d4fe393d", "party",
    ),
    Document(
        "F16", "honorarios", "2026-03-06",
        "Solicitud del Administrador Concursal para declarar firme la sentencia",
        "Administrador Concursal", "Escrito de parte", "ORD 641/2024",
        "gmail/fees-postjudgment-filing-2026-03-06.pdf", "Gmail 19cd8d1e9fa4e531", "party",
        editorial_notes=(
            "El escrito afirma que no se había dado traslado de apelación a esa parte; el recurso de Aweswell está fechado el 23 de febrero de 2026 y el rollo se formó en resolución firmada el 6 de marzo. Se conservan ambos hitos sin inferir el momento exacto de conocimiento.",
        ),
    ),
    Document(
        "F17", "honorarios", "2026-03-06",
        "Diligencia de formación del RPL 421/2026",
        "LAJ Francisco Javier Labella Ribes", "Diligencia de ordenación", "RPL 421/2026",
        "gmail/fees-laj-appeal-elevation-2026-03-09.pdf", "Gmail 19cd8d1e9fa4e531", "court",
        outcome="Forma el rollo, requiere elevación/emplazamiento y depósito de apelación.",
    ),
    Document(
        "F18", "honorarios", "2026-04-07",
        "Diligencia que tiene por interpuesta la apelación y da traslado",
        "LAJ Amelia Villarreal Sancho", "Diligencia de ordenación", "RPL 421/2026",
        "gmail/fees-laj-appeal-transfer-2026-04-07.pdf", "Gmail 19d685f9784b385a", "court",
        outcome="Tiene por interpuesta la apelación, da traslado por diez días y pasa la prueba solicitada a la ponencia.",
    ),
)


PROFESSIONAL_NAMES = (
    "María Luisa Díaz Vecino", "Maria Luisa Diaz Vecino", "María Díaz Vecino", "Maria Diaz Vecino",
    "María del Pilar García Coello", "Maria del Pilar Garcia Coello", "Pilar García Coello",
    "Tania Alejandra Domínguez Limiñana", "Tania Alejandra Domínguez", "Tania Domínguez Limiñana",
    "Javier Sixto Seijas", "Alejandro Alfredo Valido Farray", "Alejandro Valido Farray",
    "Javier Sixto", "Juan Tomás Parrilla", "Ignacio Delgado", "Ramón Biforcos Sancho",
    "Estefanía Sixto", "Estefanía",
    "Tomás Ramírez Hernández", "Tomas Ramirez Hernandez", "Juan Carlos Hernández Cruz",
    "Juan Carlos Hernandez Cruz", "Juan Carlos Hernández", "Juan Carlos Hernandez", "Juan Carlos Cruz",
    "Salvador Cuyás Morales", "Salvador Cuyas Morales",
)


def flexible_name_pattern(value: str) -> str:
    """Match a name across PDF wrapping and common accent loss."""
    equivalents = {
        "a": "[aá]", "á": "[aá]",
        "e": "[eé]", "é": "[eé]",
        "i": "[ií]", "í": "[ií]",
        "o": "[oó]", "ó": "[oó]",
        "u": "[uúü]", "ú": "[uúü]", "ü": "[uúü]",
        "n": "[nñ]", "ñ": "[nñ]",
    }
    tokens = []
    for token in value.split():
        tokens.append("".join(equivalents.get(char.casefold(), re.escape(char)) for char in token))
    return r"\s+".join(tokens)


def slug(value: str) -> str:
    table = str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN")
    value = value.translate(table).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:78]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def extract_pdf(path: Path) -> list[str]:
    result = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    pages = result.stdout.replace("\r\n", "\n").split("\f")
    while pages and not pages[-1].strip():
        pages.pop()
    return pages


def extract_docx(path: Path) -> list[str]:
    result = subprocess.run(
        ["pandoc", str(path), "-t", "plain", "--wrap=none"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [result.stdout.replace("\r\n", "\n")]


def trim_first_page(text: str, start: str) -> str:
    lines = text.splitlines()
    if start == "court":
        markers = (
            "AUTO", "SENTENCIA", "DECRETO", "DILIGENCIA DE ORDENACIÓN",
            "DILIGENCIA DE ORDENACION", "PROVIDENCIA", "CÉDULA DE EMPLAZAMIENTO",
            "CEDULA DE EMPLAZAMIENTO",
        )
    else:
        markers = ("A LA ", "AL JUZGADO", "A LA ILMA", "A LA AUDIENCIA")
    for index, line in enumerate(lines[:90]):
        candidate = re.sub(r"\s+", " ", line.strip()).upper()
        if any(candidate == marker or candidate.startswith(marker) for marker in markers):
            return "\n".join(lines[index:])
    return text


def redact_page(text: str, *, first_page: bool, start: str) -> str:
    if first_page:
        text = trim_first_page(text, start)
    text = text.replace("\u00a0", " ").replace("\u200b", "").replace("\ufeff", "")
    lines = text.splitlines()
    cleaned: list[str] = []
    for line in lines:
        stripped = line.strip()
        if re.search(r"\bNOTIFICADO\b", stripped, flags=re.I):
            continue
        if re.match(r"^Este documento ha sido firmado electrónicamente por:", stripped, flags=re.I):
            break
        if re.match(r"^Firmado digitalmente por", stripped, flags=re.I):
            cleaned.append("[datos de firma electrónica suprimidos]")
            break
        if re.match(r"^Firmado por\b", stripped, flags=re.I):
            cleaned.append("[datos de firma electrónica suprimidos]")
            break
        if re.match(r"^(?:Página\s+)?\d+\s+(?:de\s+\d+)?$", stripped, flags=re.I):
            continue
        cleaned.append(line.rstrip())
    text = "\n".join(cleaned)

    # Direct contact and identity/verification data.
    text = re.sub(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", "[correo electrónico suprimido]", text, flags=re.I)
    text = re.sub(r"(?im)^\s*(?:Tel[eé]fono|Fax|Email|Correo electrónico)\s*[:.]?.*$", "[dato de contacto suprimido]", text)
    text = re.sub(r"\b(?:[XYZ]\d{7}[A-Z]|\d{8}[A-Z]|[A-Z]\d{8})\b", "[identificador personal suprimido]", text, flags=re.I)
    text = re.sub(r"\((?:7716847|N8262488C)\)", "[identificador societario suprimido]", text, flags=re.I)
    text = re.sub(r"\b(?:NIG|IUP)\s*:\s*[A-Z0-9]+", "[identificador judicial administrativo suprimido]", text, flags=re.I)
    text = re.sub(r"\*{2,}\d{2,}\*{2,}", "[identificador personal suprimido]", text)
    text = re.sub(r"\bES\d{2}(?:[ -]?\d){20}\b", "[cuenta bancaria suprimida]", text, flags=re.I)
    text = re.sub(r"\b8-6\.937\.696-E\b", "[número de póliza suprimido]", text, flags=re.I)
    text = re.sub(
        r"\b(?:Tel(?:[eé]fono)?|M[oó]vil|Fax)\.?\s*:?\s*(?:\+?34[ .-]*)?(?:\d[ .()-]*){8,11}",
        "[dato de contacto suprimido]",
        text,
        flags=re.I,
    )
    text = re.sub(r"A05003250-?[0-9a-f\-]+", "[código de verificación suprimido]", text, flags=re.I)
    text = re.sub(r"https?://sede\.justiciaencanarias\.es/\S+", "[URL de verificación suprimida]", text, flags=re.I)
    text = re.sub(r"(?im)^\s*(?:De|Para|CC|CCO)\s*:\s*.*@.*$", "[cabecera de correo suprimida]", text)
    text = re.sub(
        r"(?i)domicilio en Paseo de la Castellana,?\s*(?:n[ºo]\s*)?4,?\s*28043 Madrid(?:\s*\(Madrid\))?",
        "domicilio [suprimido]",
        text,
    )
    text = re.sub(
        r"(?i)domicilio en Madrid,\s*Paseo de la Castellana\s*(?:n[ºo]\s*)?4",
        "domicilio [suprimido]",
        text,
    )
    text = re.sub(
        r"(?i)cuyo domicilio social se encuentra\s+en\s+la calle Hero\s+12-1[ºo],?\s*38008\s+de\s+Santa Cruz de Tenerife",
        "cuyo domicilio social [suprimido]",
        text,
    )

    for name in PROFESSIONAL_NAMES:
        # PDF text extraction frequently wraps a person's given name and
        # surnames onto separate lines.  Match flexible whitespace so the
        # minimisation rule is consistent even across those line breaks.
        pattern = flexible_name_pattern(name)
        text = re.sub(pattern, "[profesional procesal suprimido]", text, flags=re.I)
    text = re.sub(
        r"colegiad[oa]\s+(?:(?:n[úu]mero|n[úu]m\.?|n\.?)\s*)?[\d.]+",
        "colegiación [suprimida]",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"(?i)(\b(?:letrado\s+)?Sr\.\s+)Arturo\b",
        r"\1[profesional procesal suprimido]",
        text,
    )

    # Remove detached signature-certificate continuation lines.
    text = re.sub(r"(?im)^\s*(?:día|emitido por|Fecha y hora:).{0,120}$", "", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def build_markdown(doc: Document, source_path: Path) -> tuple[str, int, str]:
    suffix = source_path.suffix.lower()
    if suffix == ".pdf":
        pages = extract_pdf(source_path)
        pagination = f"{len(pages)} páginas PDF"
    elif suffix == ".docx":
        pages = extract_docx(source_path)
        pagination = "DOCX sin paginación autoritativa"
    else:
        raise ValueError(f"unsupported source: {source_path}")
    source_hash = sha256(source_path)
    redacted = [redact_page(page, first_page=(index == 0), start=doc.start) for index, page in enumerate(pages)]

    lines = [
        f"# {doc.title}", "",
        f"- **ID documental:** {doc.id}",
        f"- **Carril:** {'Separación del Administrador Concursal' if doc.lane == 'separacion' else 'Honorarios / responsabilidad civil'}",
        f"- **Fecha del documento:** {doc.date}",
        f"- **Emisor / parte:** {doc.actor}",
        f"- **Clase:** {doc.instrument}",
        f"- **Procedimiento:** {doc.procedure}",
        f"- **Extensión fuente:** {pagination}",
        f"- **Anclaje de procedencia:** {doc.source_anchor}",
        f"- **SHA-256 de la fuente controlada:** `{source_hash}`",
        f"- **Estado de la copia:** {doc.public_status}",
        "",
        "> Transcripción pública íntegra del contenido sustantivo localizado. Se han suprimido únicamente cabeceras administrativas repetitivas, datos de contacto/identificación, cuentas o códigos de verificación, metadatos de firma y nombres de profesionales procesales no necesarios. Los marcadores de redacción son visibles. Alegaciones de parte no equivalen a hechos probados.",
    ]
    if doc.outcome:
        lines.extend(["", "## Efecto procesal controlado", "", doc.outcome, "", f"**Alcance de fondo:** {doc.merits}"])
    if doc.editorial_notes:
        lines.extend(["", "## Notas editoriales", ""])
        lines.extend(f"- {note}" for note in doc.editorial_notes)
    lines.extend(["", "## Texto íntegro redactado", ""])
    for index, page in enumerate(redacted, start=1):
        if suffix == ".pdf":
            lines.extend([f"### Página {index} de {len(redacted)}", ""])
        else:
            lines.extend(["### Texto de la copia DOCX", ""])
        safe_page = page.replace("```", "` ` `")
        lines.extend(["```text", safe_page, "```", ""])
    return "\n".join(lines).rstrip() + "\n", len(pages), source_hash


def write_index(records: list[dict], output_root: Path) -> None:
    lines = [
        "# Concurso 36/2012 — Autos, resoluciones y escritos: corpus íntegro redactado",
        "",
        "Corte documental: 23 de agosto de 2026.",
        "",
        "Este índice reúne el texto sustantivo completo de todas las piezas localizadas en los dos carriles controlados: (1) solicitud de separación del Administrador Concursal y sus recursos; y (2) demanda de responsabilidad/reintegro de honorarios y su apelación. La ausencia de una pieza se registra expresamente y no se rellena por inferencia.",
        "",
        "## Límites de completitud",
        "",
        "- No se ha localizado como archivo autónomo el Decreto de 1 de septiembre de 2025 ni la diligencia de 17/26 de marzo de 2025 citados en el incidente de aclaración de honorarios.",
        "- No se ha localizado acta o grabación de la audiencia previa de 20 de enero de 2026, ni una resolución firmada posterior que decida el RPL 421/2026.",
        "- No se ha localizado una resolución de fondo posterior al Auto 223/2026 en los RPL 3304/2025 y 3319/2025 acumulados.",
        "- Varias piezas de parte están disponibles como copias DOCX remitidas por el equipo letrado. Su texto se transcribe, pero su ficha indica cuando el corpus no contiene acuse independiente.",
        "",
    ]
    for lane, heading in (("separacion", "Separación y apelaciones"), ("honorarios", "Honorarios y apelación")):
        lines.extend([f"## {heading}", "", "| ID | Fecha | Emisor | Pieza | Texto |", "|---|---|---|---|---|"])
        for record in (item for item in records if item["lane"] == lane):
            lines.append(
                f"| {record['id']} | {record['date']} | {record['actor']} | {record['title']} | [Abrir]({record['href']}) |"
            )
        lines.append("")
    lines.extend([
        "## Regla de lectura", "",
        "Los escritos de parte documentan posiciones y solicitudes. Las resoluciones judiciales documentan únicamente lo que su motivación y parte dispositiva deciden. En particular, la primera instancia desestimó las dos acciones principales por legitimación activa; no decidió el fondo de los siete motivos de separación ni la legalidad material y cuantía de los honorarios.",
    ])
    (output_root / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    args.output_root.mkdir(parents=True, exist_ok=True)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    for doc in DOCUMENTS:
        source_path = args.source_root / doc.source
        if not source_path.is_file():
            raise FileNotFoundError(f"missing controlled source for {doc.id}: {source_path}")
        markdown, pages, source_hash = build_markdown(doc, source_path)
        output_path = args.output_root / doc.output_name
        output_path.write_text(markdown, encoding="utf-8")
        records.append(
            {
                "id": doc.id,
                "lane": doc.lane,
                "record_class": doc.start,
                "date": doc.date,
                "title": doc.title,
                "actor": doc.actor,
                "instrument": doc.instrument,
                "procedure": doc.procedure,
                "source_pages_or_units": pages,
                "source_sha256": source_hash,
                "source_anchor": doc.source_anchor,
                "copy_status": doc.public_status,
                "outcome": doc.outcome,
                "merits_scope": doc.merits,
                "href": doc.output_name,
                "public_pdf": doc.public_pdf or None,
            }
        )
    write_index(records, args.output_root)
    payload = {
        "schema": "concurso36-autos-fulltext-v1",
        "cutoff": "2026-08-23",
        "language": "es",
        "redaction_policy": "Substantive text retained; administrative/contact/identity/bank/verification/signature data and unnecessary procedural-professional names removed with visible markers.",
        "known_gaps": [
            "Decreto de 1 septiembre 2025 and the cited March 2025 diligence in ORD 641/2024 are not present as autonomous source files.",
            "No located minutes or recording of the 20 January 2026 preliminary hearing.",
            "No located signed merits outcome after Auto 223/2026 in accumulated RPL 3304/2025 and 3319/2025.",
            "No located signed merits outcome after the 7 April 2026 transfer in RPL 421/2026.",
            "No certified chronological docket/index has been obtained for the whole Concurso 36/2012 court file.",
        ],
        "documents": records,
    }
    args.manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"built {len(records)} full-text records")


if __name__ == "__main__":
    main()

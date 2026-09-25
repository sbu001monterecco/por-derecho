#!/usr/bin/env python3
"""Digitise every located Sun Park ACTA source into public-safe packages.

The native sources remain outside Git.  This program creates irreversible,
raster-only redacted facsimiles, current source-page JPEG images, page-sequenced
public text, source-family reconciliation metadata, and a private custody
manifest.  Legacy WEBP derivatives, where retained elsewhere in the repository,
remain separate.  This program deliberately does not call an OCR result a
certified transcription.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader
from reportlab import rl_config
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


REPO = Path(__file__).resolve().parents[1]
ACTA_ROOT = REPO / "evidence/community/actas"
INDEX_PATH = ACTA_ROOT / "public-index.json"
SOURCE_IMAGE_ROOT = REPO / "assets/evidence/community-actas-source"
FACSIMILE_ROOT = REPO / "assets/docs/community-actas-source"
GENERATED_DATE = "2026-08-28"

# This is a current evidential control, not a historical value copied from a
# previous reconciliation.  The 2012 president's statement is now located and
# separately controlled; only the referenced written objection remains open.
# The 20-Nov-2018 ACTA is known only through the later 2022 recital and its
# standalone source remains unlocated.  The 29-Dec-2021 RICPE meeting/capital
# resolution is likewise known only through the later 11-Feb-2022 notice; its
# primary notice, minutes and resolution record remain unlocated.
KNOWN_UNLOCATED_SOURCES = [
    {
        "unlocated_source_key": "2012-08-10-written-objection",
        "date": "2012-08-10",
        "continuity_evidence_record_id": "SP-SRC-OBJECTION-2012-08-10",
        "description_es": (
            "Escrito de objeción anunciado en el ACTA; la declaración del "
            "presidente se ha localizado por separado."
        ),
        "description_en": (
            "Written objection announced in the minutes; the president's "
            "statement has been located separately."
        ),
        "counts_as_unlocated_acta_original": False,
        "counts_as_unlocated_meeting_or_minutes_original": False,
    },
    {
        "unlocated_source_key": "2018-11-20-standalone-acta",
        "date": "2018-11-20",
        "continuity_evidence_record_id": "SP-SRC-RECITAL-2018-11-20",
        "description_es": (
            "ACTA mencionada posteriormente en 2022; fuente autónoma no "
            "localizada."
        ),
        "description_en": (
            "Minutes later recited in 2022; standalone source not located."
        ),
        "counts_as_unlocated_acta_original": True,
        "counts_as_unlocated_meeting_or_minutes_original": True,
    },
    {
        "unlocated_source_key": "2021-12-29-ricpe-primary-meeting-records",
        "date": "2021-12-29",
        "continuity_evidence_record_id": "SP-SRC-RICPE-2021-12-29-PRIMARY-UNLOCATED",
        "description_es": (
            "Junta y acuerdo societario mencionados en la convocatoria posterior "
            "de RICPE; convocatoria, ACTA, lista, votos y acuerdo primarios no localizados."
        ),
        "description_en": (
            "Corporate meeting and resolution recited in the later RICPE notice; "
            "primary notice, minutes, list, votes and resolution unlocated."
        ),
        "counts_as_unlocated_acta_original": False,
        "counts_as_unlocated_meeting_or_minutes_original": True,
    },
]

PAGE_MARKER = re.compile(r"^## Página fuente (\d+) de (\d+)\s*$", re.MULTILINE)
ID_PATTERN = re.compile(
    r"(?i)\b(?:[XYZ]\s*[- ]?\d{7}|\d{8})\s*[- ]?[A-Z]\b|"
    r"\b[A-Z]\s*[- ]?\d{7,8}\s*[- ]?[A-Z0-9]?\b"
)
IBAN_PATTERN = re.compile(r"(?i)\bES\s*\d{2}(?:\s*\d){18,22}\b|\bIBAN\b")
EMAIL_PATTERN = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+?34[ .-]?)?[6789]\d{2}(?:[ .-]?\d{3}){2}(?!\d)")
ADDRESS_PATTERN = re.compile(
    r"(?i)\b(?:domicilio|direcci[oó]n|calle|avenida|c/|código postal)\b"
)
SENSITIVE_LINE_PATTERN = re.compile(
    r"(?i)\b(?:DNI|NIE|NIF|CIF|IBAN|cuenta\s+(?:bancaria|corriente)|"
    r"tel[eé]fono|correo\s+electr[oó]nico|e-?mail|domicilio|direcci[oó]n|"
    r"colegiad[oa]|firma\s+digital|apartamento\s+n?[.º°]?\s*\d|"
    r"finca\s+(?:registral\s+)?n?[.º°]?\s*\d)\b"
)


@dataclass
class SourceVariant:
    path: str | None
    relationship_es: str
    relationship_en: str
    relationship_kind: str = "native-variant"
    source_document_id: str | None = None
    legacy_id_aliases: list[str] = field(default_factory=list)
    classification_status: str = "classified"
    classification_note_es: str | None = None
    classification_note_en: str | None = None
    expected_bytes: int | None = None
    expected_sha256: str | None = None
    expected_pages: int | None = None
    component_files: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ActaConfig:
    slug: str
    source: str
    source_kind: str = "pdf"
    display_name: str = "copia digital de trabajo"
    body: str = "Comunidad de Propietarios"
    meeting_type: str = "ordinary"
    document_type: str = "acta-or-minutes"
    source_package_kind: str = "acta-or-minutes-family"
    counts_as_located_acta_family: bool = True
    unlocated_meeting_or_minutes_original_count: int = 0
    event_id: str | None = None
    source_document_id: str | None = None
    legacy_source_id_aliases: list[str] = field(default_factory=list)
    event_date: str | None = None
    title_es: str | None = None
    title_en: str | None = None
    meeting_time: str | None = None
    document_issue_date: str | None = None
    issuing_person_or_body: str | None = None
    stated_capacity: str | None = None
    recipients: list[str] = field(default_factory=list)
    scheduled_meeting_first_call: str | None = None
    scheduled_meeting_second_call: str | None = None
    documented_meeting_status: dict[str, Any] = field(default_factory=dict)
    referenced_prior_resolution: dict[str, Any] = field(default_factory=dict)
    continuity_registration_required: bool = True
    expected_source_bytes: int | None = None
    expected_source_sha256: str | None = None
    expected_source_pages: int | None = None
    acquisition_note_es: str | None = None
    acquisition_note_en: str | None = None
    source_page_scope: str = "controlling-copy"
    full_redaction_pages: set[int] = field(default_factory=set)
    reuse_existing_pages: bool = True
    reuse_prefix_pages: int = 0
    partial_tail_redactions: dict[int, float] = field(default_factory=dict)
    variants: list[SourceVariant] = field(default_factory=list)
    variant_note_es: str = "Copia localizada; no es el libro diligenciado ni una copia certificada."
    variant_note_en: str = "Located copy; not the diligenced minutes book or a certified copy."


def variant(
    path: str | None,
    es: str,
    en: str,
    *,
    relationship_kind: str = "native-variant",
    source_document_id: str | None = None,
    legacy_id_aliases: list[str] | None = None,
    classification_status: str = "classified",
    classification_note_es: str | None = None,
    classification_note_en: str | None = None,
    expected_bytes: int | None = None,
    expected_sha256: str | None = None,
    expected_pages: int | None = None,
    component_files: list[dict[str, Any]] | None = None,
) -> SourceVariant:
    return SourceVariant(
        path=path,
        relationship_es=es,
        relationship_en=en,
        relationship_kind=relationship_kind,
        source_document_id=source_document_id,
        legacy_id_aliases=list(legacy_id_aliases or []),
        classification_status=classification_status,
        classification_note_es=classification_note_es,
        classification_note_en=classification_note_en,
        expected_bytes=expected_bytes,
        expected_sha256=expected_sha256,
        expected_pages=expected_pages,
        component_files=list(component_files or []),
    )


CONFIGS = [
    ActaConfig(
        "2008-04-29", "2008-04-29-source3.pdf", meeting_type="extraordinary",
        source_document_id="SP-SRC-ACTA-2008-04-29-B",
        legacy_source_id_aliases=["SP-SRC-ACTA-2008-04-29"],
        body="Propietarios / capa de formación de CEXP", full_redaction_pages={2, 5},
        partial_tail_redactions={1: 0.45, 3: 0.30},
        variants=[
            variant(
                "2008-04-29-alt.pdf",
                "Escaneo alternativo de cinco páginas; mismo orden general, diferencias de captura.",
                "Alternate five-page scan; same general sequence, capture differences.",
                source_document_id="SP-SRC-ACTA-2008-04-29-CAPTURE-02",
                legacy_id_aliases=["SP-SRC-ACTA-2008-04-29-VARIANT-01"],
            ),
            variant(
                None,
                "Tercera captura de cinco páginas, visualmente cotejada página por página: mismo instrumento, texto, orden y disposición de firmas/autenticación; binario y captura distintos.",
                "Third five-page capture, visually compared page by page: same instrument, text, order and signature/authentication arrangement; distinct binary/capture.",
                source_document_id="SP-SRC-ACTA-2008-04-29-CAPTURE-03",
                relationship_kind="same-instrument-capture-variant",
                expected_bytes=1085328,
                expected_sha256="7c70b45a14459fdda32f9150008bd26662c051b77da8189d6f7720b20de5ab8e",
                expected_pages=5,
            ),
        ],
        variant_note_es="Copia de cinco páginas; la hoja notarial final y las listas nominales se reservan por privacidad.",
        variant_note_en="Five-page copy; the final notarial sheet and nominal lists are withheld for privacy.",
    ),
    ActaConfig(
        "2008-07-15", "2. ACTA 15 JUL 2008.pdf", meeting_type="extraordinary",
        full_redaction_pages=set(range(2, 9)), partial_tail_redactions={1: 0.58},
        variants=[variant(
            "2008-07-15-drive.pdf", "Variante parcial de seis páginas.", "Partial six-page variant.",
            source_document_id="SP-SRC-ACTA-2008-07-15-PARTIAL-6P",
            legacy_id_aliases=["SP-SRC-ACTA-2008-07-15-VARIANT-01"],
        )],
        variant_note_es="Copia de nueve páginas recuperada de una transmisión posterior; la variante de seis páginas es parcial.",
        variant_note_en="Nine-page copy recovered from a later transmission; the six-page variant is partial.",
    ),
    ActaConfig(
        "2008-07-15-cexp",
        "2008-07-15-cexp-source.pdf",
        display_name="copia CEXP de seis páginas de la reunión universal de las 17:00",
        body="CEXP",
        meeting_type="universal",
        event_id="SP-ACTA-2008-07-15-CEXP",
        source_document_id="SP-SRC-ACTA-2008-07-15-CEXP-17H",
        event_date="2008-07-15",
        title_es="15 julio 2008 · reunión universal CEXP de las 17:00",
        title_en="15 July 2008 · 17:00 universal CEXP meeting",
        meeting_time="17:00",
        expected_source_bytes=252353,
        expected_source_sha256="06b61e5c4b1a125a3412585f606a53b3bcc5dafcad840aedd6b41aa9a1ebffda",
        expected_source_pages=6,
        # This is a distinct CEXP event, not the 12:00 Owners' Community
        # meeting.  Until every page receives source-image privacy review, the
        # public facsimile and public page text default to explicit full-page
        # redaction markers; no unsanitised OCR is emitted.
        full_redaction_pages=set(range(1, 7)),
        reuse_existing_pages=False,
        variant_note_es="Fuente CEXP distinta de seis páginas para la reunión universal de las 17:00. No se confunde con la junta de la Comunidad de Propietarios de las 12:00. La imagen y el texto públicos quedan íntegramente redactados por defecto hasta completar la revisión de privacidad página por página.",
        variant_note_en="Distinct six-page CEXP source for the 17:00 universal meeting. It is not conflated with the 12:00 Owners' Community meeting. Public image and text remain fully redacted by default until page-by-page privacy review is complete.",
    ),
    ActaConfig(
        "2008-07-25", "3. ACTA  25 JUL 2008.pdf", meeting_type="extraordinary",
        full_redaction_pages={1, 2, 4},
        variants=[variant(
            "2008-07-25-drive.pdf", "Variante parcial de tres páginas.", "Partial three-page variant.",
            source_document_id="SP-SRC-ACTA-2008-07-25-PARTIAL-3P",
            legacy_id_aliases=["SP-SRC-ACTA-2008-07-25-VARIANT-01"],
        )],
        variant_note_es="Copia de cuatro páginas; la variante de tres páginas es parcial.",
        variant_note_en="Four-page copy; the three-page variant is partial.",
    ),
    ActaConfig("2008-12-17", "4. ACTA 17 DIC 2008 - queja de LPGC uso turistico.pdf", meeting_type="extraordinary", full_redaction_pages=set(range(2, 9)), partial_tail_redactions={1: 0.58}),
    ActaConfig("2009-05-28", "5. ACTA 28 MAY 2009.pdf", full_redaction_pages={2, 9, 10, 11, 12, 13}, partial_tail_redactions={1: 0.58}),
    ActaConfig(
        "2011-02-02", "2011-02-02-source.pdf", full_redaction_pages={3, 4},
        source_document_id="SP-SRC-ACTA-2011-02-02-A",
        legacy_source_id_aliases=["SP-SRC-ACTA-2011-02-02"],
        partial_tail_redactions={1: 0.58}, variants=[
            variant(
                "2011-02-02-variant-2136388.pdf", "Escaneo alternativo de seis páginas.", "Alternate six-page scan.",
                source_document_id="SP-SRC-ACTA-2011-02-02-C",
                legacy_id_aliases=["SP-SRC-ACTA-2011-02-02-VARIANT-01"],
            ),
            variant(
                "7. ACTA 02 FEB 2011.pdf",
                "Copia transmitida de seis páginas con orden de páginas distinto; se conserva como variante, no como sustituto silencioso.",
                "Transmitted six-page copy with a different page order; retained as a variant, not silently substituted.",
                source_document_id="SP-SRC-ACTA-2011-02-02-B",
                legacy_id_aliases=["SP-SRC-ACTA-2011-02-02-VARIANT-02"],
            ),
        ],
        variant_note_es="Se adopta la copia de seis páginas con secuencia coherente; otras dos variantes quedan identificadas.",
        variant_note_en="The coherent six-page sequence is used; two other variants remain identified.",
    ),
    ActaConfig(
        "2011-06-22", "2011-06-22-source.pdf", meeting_type="extraordinary", full_redaction_pages={3, 14, 15, 16},
        source_document_id="SP-SRC-ACTA-2011-06-22-B",
        legacy_source_id_aliases=["SP-SRC-ACTA-2011-06-22"],
        partial_tail_redactions={1: 0.55, 2: 0.40, 13: 0.45},
        variants=[
            variant(
                "2011-06-22-variant-4551801.pdf",
                "Binario distinto, páginas renderizadas equivalentes a la copia controlante.",
                "Different binary, rendered pages equivalent to the controlling copy.",
                source_document_id="SP-SRC-ACTA-2011-06-22-A",
                legacy_id_aliases=["SP-SRC-ACTA-2011-06-22-VARIANT-01"],
            ),
            variant(
                "2011-06-22-variant-2750336.pdf",
                "Variante de dieciséis páginas con orden y anotaciones diferentes.",
                "Sixteen-page variant with different order and annotations.",
                source_document_id="SP-SRC-ACTA-2011-06-22-D-PDF24",
                legacy_id_aliases=["SP-SRC-ACTA-2011-06-22-VARIANT-02"],
            ),
        ],
    ),
    ActaConfig(
        "2012-08-10", "ACTA JUNTA GENERAL 10 AGOSTO1 ok.docx", source_kind="docx",
        display_name="ACTA nativa DOCX de cuatro páginas", full_redaction_pages={2},
        reuse_existing_pages=False, partial_tail_redactions={1: 0.64, 4: 0.58},
        variants=[
            variant(
                "2012-08-10-drive-source.pdf",
                "Intervención/declaración de cinco páginas; fuente relacionada, no sustituto del ACTA.",
                "Five-page speech/statement; related source, not a substitute for the ACTA.",
                relationship_kind="related-statement",
                source_document_id="SP-SRC-STATEMENT-2012-08-10-5P",
                legacy_id_aliases=["SP-SRC-ACTA-2012-08-10-STATEMENT-01"],
            ),
            variant(
                "20120809194034781_0001.pdf",
                "Poder de una página asociado a la convocatoria; documento separado.",
                "One-page proxy associated with the notice; separate document.",
                relationship_kind="related-proxy",
                source_document_id="SP-SRC-PROXY-2012-08-10-1P",
                legacy_id_aliases=["SP-SRC-ACTA-2012-08-10-PROXY-01"],
            ),
        ],
        variant_note_es="ACTA DOCX de cuatro páginas localizada en tres cadenas de correo. Consigna que no se sometió ningún acuerdo a votación. La declaración del presidente de cinco páginas está localizada como fuente separada y también incorporada al paquete notarial 422B; el escrito de objeción anunciado sigue sin localizarse.",
        variant_note_en="Four-page DOCX minutes located in three email chains. They state that no resolution was put to a vote. The five-page president's statement is located as a separate source and is also incorporated in notarial package 422B; the announced objection writing remains unlocated.",
    ),
    ActaConfig(
        "2014-04-10",
        "2014-04-10-source.pdf",
        display_name="paquete PDF nativo de 155 páginas (frontera ACTA/anexos pendiente)",
        body="Comunidad de Propietarios",
        meeting_type="ordinary",
        event_id="SP-ACTA-2014-04-10",
        source_document_id="SP-SRC-ACTA-2014-04-10",
        event_date="2014-04-10",
        title_es="10 abril 2014 · junta competidora LPB/Gil",
        title_en="10 April 2014 · competing LPB/Gil meeting",
        expected_source_bytes=4730410,
        expected_source_sha256="12fcefd550f69462613e91aec49ac32b69cf3c2351463a751363c663f37af32b",
        expected_source_pages=155,
        acquisition_note_es="Dos portadores profesionales posteriores (septiembre de 2014 y diciembre de 2015) contienen copias byte-idénticas. No prueban la circulación original; mensajes, sobres y cuerpos profesionales permanecen privados. El objeto Drive compartido en junio de 2014 ya no es accesible y su identidad binaria no puede cotejarse.",
        acquisition_note_en="Two later professional carriers (September 2014 and December 2015) contain byte-identical copies. They do not prove original circulation; professional messages, envelopes and bodies remain private. The Drive object shared in June 2014 is no longer accessible, so its binary identity cannot be compared.",
        source_page_scope="54-page-notarial-act-plus-100-incorporated-pages-plus-simple-copy-certification",
        # The newly located package replaces the gap only after a successful
        # controlled build.  Until source-page review is complete, no page
        # image or OCR body is exposed publicly.
        full_redaction_pages=set(range(1, 156)),
        reuse_existing_pages=False,
        variants=[
            variant(
                None,
                "Variante ACTA mecanografiada de seis páginas, fechada en pie el 16 de abril; sólo se han localizado sus páginas 1, 5 y 6 como PNG. Difiere materialmente en horarios, porcentajes, función notarial y acuerdos bancarios/administrativos.",
                "Six-page typed minutes version footer-dated 16 April; only pages 1, 5 and 6 are located as PNGs. It differs materially on times, percentages, the notary's role and banking/administrator resolutions.",
                relationship_kind="materially-distinct-typed-minutes-partial",
                source_document_id="SP-SRC-ACTA-2014-04-16-TYPED-6P-PARTIAL",
                legacy_id_aliases=["SP-SRC-ACTA-2014-04-10-TYPED-VARIANT-PARTIAL"],
                classification_status="partial-pages-1-5-6-only",
                classification_note_es="PNG p1: 651.003 bytes / 8ccd619b…; p5: 718.590 / a907da8e…; p6: 453.547 / cdd2cd49…. El PDF nativo completo y las páginas 2–4 siguen sin localizarse.",
                classification_note_en="PNG p1: 651,003 bytes / 8ccd619b…; p5: 718,590 / a907da8e…; p6: 453,547 / cdd2cd49…. The complete native PDF and pages 2–4 remain unlocated.",
                expected_bytes=1823140,
                expected_pages=3,
                component_files=[
                    {
                        "page": 1,
                        "bytes": 651003,
                        "sha256": "8ccd619b3bdb0d7b34876ff446b678e8ba3ea8f937e379c1ae6d9a58ee636c4f",
                    },
                    {
                        "page": 5,
                        "bytes": 718590,
                        "sha256": "a907da8eaaf64fdae3e206c96fc63d4b6c8e5c1d547a30d3afe1df6bc3d24e23",
                    },
                    {
                        "page": 6,
                        "bytes": 453547,
                        "sha256": "cdd2cd4942fdf2df9d4d4f75374ccc342c3308a4b660f19e2d646fa53bb985f3",
                    },
                ],
            ),
            variant(
                None,
                "Respuesta notarial separada de seis páginas; comunicación de parte, no ACTA ni sustituto del protocolo 422B.",
                "Separate six-page notarial response; a party communication, not minutes and not a substitute for protocol 422B.",
                relationship_kind="related-notarial-response",
                source_document_id="SP-SRC-NOTARIAL-RESPONSE-2014",
                legacy_id_aliases=["SP-SRC-ACTA-2014-04-10-NOTARIAL-RESPONSE"],
                expected_bytes=132823,
                expected_sha256="80473a7499af3c1ac30763e9bdef7555d9358752e99dd6373ddabe230abe57ae",
                expected_pages=6,
                classification_status="related-source-not-controlling",
                classification_note_es="Metadatos verificados desde la copia de custodia; permanece separado del ACTA y del protocolo 422B.",
                classification_note_en="Metadata verified from the custody copy; it remains separate from the minutes and protocol 422B.",
            ),
        ],
        variant_note_es="Paquete notarial 422B de 155 páginas: 54 páginas/28 folios del ACTA DE PRESENCIA, 100 páginas incorporadas y certificación de copia simple. Incluye aviso, poderes, asistencia/voto, objeciones, deuda, la declaración presidencial de 2012, circulación/retención, ACTA de 2012, cuentas y presupuesto. La objeción escrita de 2012 y la variante mecanografiada completa siguen abiertas. La autenticidad, circulación original y validez no se establecen; todas las páginas públicas quedan íntegramente redactadas.",
        variant_note_en="The 155-page 422B notarial package comprises 54 pages/28 folios of the ACTA DE PRESENCIA, 100 incorporated pages and a simple-copy certification. It includes notice, proxies, attendance/voting, objections, debt, the 2012 president's statement, circulation/withholding, 2012 minutes, accounts and budget. The 2012 objection writing and complete typed version remain open. Authenticity, original circulation and validity are not established; every public page is fully redacted.",
    ),
    ActaConfig(
        "2014-08-28-cexp", "ACTA JUNTA EXTRAORDINARIA AGOSTO 2014.docx.pdf", body="CEXP", meeting_type="extraordinary",
        source_document_id="SP-SRC-ACTA-2014-08-28-CEXP-PUBLIC-CONTROL",
        legacy_source_id_aliases=["SP-SRC-ACTA-2014-08-28-cexp"],
        variants=[
            variant(
                "2014-08-28-cexp-source.pdf",
                "Segunda conversión PDF del mismo instrumento CEXP; binario de 90.821 bytes distinto del export de Drive registrado.",
                "Second PDF conversion of the same CEXP instrument; a 90,821-byte binary distinct from the registered Drive export.",
                source_document_id="SP-SRC-ACTA-2014-08-28-CEXP-PDF-CONVERSION-02",
                legacy_id_aliases=["SP-SRC-ACTA-2014-08-28-cexp-VARIANT-01"],
            ),
            variant(
                None,
                "Export PDF de Drive registrado por separado; comparte tamaño con otra conversión, pero no SHA-256.",
                "Separately registered Drive PDF export; it shares a byte count with another conversion, but not its SHA-256.",
                source_document_id="SP-SRC-ACTA-2014-08-28-CEXP",
                relationship_kind="registered-drive-export-distinct-binary",
                expected_bytes=90821,
                expected_sha256="a510106ec8c8a860ffff50575843139afffb5c2313d218edf99eb410ab56e3d2",
                expected_pages=3,
            ),
        ],
        variant_note_es="Instrumento CEXP de tres páginas; el control público de 104.006 bytes, la conversión de 90.821 bytes y el export Drive registrado de 90.821 bytes son binarios distintos. No es un acta de la Comunidad de Propietarios.",
        variant_note_en="Three-page CEXP instrument; the 104,006-byte public control, 90,821-byte conversion and registered 90,821-byte Drive export are distinct binaries. It is not Owners' Community minutes.",
    ),
    ActaConfig(
        "2014-08-28-cp", "2014-08-28-cp-source.pdf", meeting_type="extraordinary",
        source_document_id="SP-SRC-ACTA-2014-08-28-COM",
        legacy_source_id_aliases=["SP-SRC-ACTA-2014-08-28-cp"],
        full_redaction_pages={2, 3, 4, 20, 21}, partial_tail_redactions={1: 0.58},
    ),
    ActaConfig(
        "2015-11-19", "ACTA JUNTA EXTRAORDINARIA NOV-15.pdf", meeting_type="extraordinary",
        source_document_id="SP-SRC-ACTA-2015-11-19-C",
        legacy_source_id_aliases=["SP-SRC-ACTA-2015-11-19"],
        full_redaction_pages=set(range(9, 39)) | {2, 7}, partial_tail_redactions={1: 0.58, 3: 0.50},
        variants=[
            variant(
                "2015-11-19-request-source.pdf",
                "Misma familia de 38 páginas con anotaciones manuscritas; no se sustituye por la copia limpia.",
                "Same 38-page family with handwritten annotations; not silently substituted for the clean copy.",
                source_document_id="SP-SRC-ACTA-2015-11-19-D-ANNOTATED-38P",
                legacy_id_aliases=["SP-SRC-ACTA-2015-11-19-VARIANT-01"],
            ),
            variant(
                "DOCS-#9481385-v2-Luchy_Playa_Blanca__S_L__-_Complejo_Sun_Park_-_Junta_General_Extraordinaria_19_11_2015.PDF",
                "Extracto procesal de cuatro páginas; documento separado.",
                "Four-page procedural extract; separate document.",
                relationship_kind="related-procedural-extract",
                source_document_id="SP-SRC-ACTA-2015-11-19-A",
                legacy_id_aliases=["SP-SRC-ACTA-2015-11-19-PROCEDURAL-EXTRACT-01"],
                classification_status="unresolved-conflict",
                classification_note_es="La clasificación exacta y la relación procesal permanecen no resueltas/en conflicto; no se trata como variante del ACTA.",
                classification_note_en="The exact classification and procedural relationship remain unresolved/in conflict; it is not treated as a minutes variant.",
            ),
            variant(
                "DOCS-#9481468-v2-Luchy_Playa_Blanca__S_L__-_Complejo_Sun_Park_-_Junta_General_Extraordinaria_19_11_2015_-_Bandama.PDF",
                "Segundo extracto procesal de cuatro páginas; documento separado.",
                "Second four-page procedural extract; separate document.",
                relationship_kind="related-procedural-extract",
                source_document_id="SP-SRC-ACTA-2015-11-19-B",
                legacy_id_aliases=["SP-SRC-ACTA-2015-11-19-PROCEDURAL-EXTRACT-02"],
                classification_status="unresolved-conflict",
                classification_note_es="La clasificación exacta y la relación procesal permanecen no resueltas/en conflicto; no se trata como variante del ACTA.",
                classification_note_en="The exact classification and procedural relationship remain unresolved/in conflict; it is not treated as a minutes variant.",
            ),
        ],
    ),
    ActaConfig(
        "2016-04-26", "2016-04-26-77p-family-a.pdf", full_redaction_pages=set(range(14, 78)),
        source_document_id="SP-SRC-ACTA-2016-04-26-A",
        legacy_source_id_aliases=["SP-SRC-ACTA-2016-04-26"],
        reuse_existing_pages=False, reuse_prefix_pages=13, partial_tail_redactions={1: 0.45, 2: 0.52, 3: 0.78, 13: 0.30},
        variants=[
            variant(
                "2016-04-26-77p-family-b.pdf", "Binario distinto de 77 páginas, equivalente página a página en render y texto extraído.", "Different 77-page binary, page-by-page equivalent in rendering and extracted text.",
                source_document_id="SP-SRC-ACTA-2016-04-26-B", legacy_id_aliases=["SP-SRC-ACTA-2016-04-26-VARIANT-01"],
            ),
            variant(
                "ACTA 2016 - 26 ABR.pdf", "Paquete parcial de 50 páginas.", "Partial 50-page package.",
                source_document_id="SP-SRC-ACTA-2016-04-26-C-50P", legacy_id_aliases=["SP-SRC-ACTA-2016-04-26-VARIANT-02"],
            ),
            variant(
                "Acta Junta Abril 2016.pdf", "Paquete parcial de 47 páginas.", "Partial 47-page package.",
                source_document_id="SP-SRC-ACTA-2016-04-26-C-47P", legacy_id_aliases=["SP-SRC-ACTA-2016-04-26-VARIANT-03"],
            ),
            variant(
                "2016-04-26-24p-drive.pdf", "Paquete parcial de 24 páginas usado por la edición pública anterior.", "Partial 24-page package used by the earlier public edition.",
                source_document_id="SP-SRC-ACTA-2016-04-26-C", legacy_id_aliases=["SP-SRC-ACTA-2016-04-26-VARIANT-04"],
            ),
            variant(
                "CONVOCATORIA ABRIL 2016.pdf",
                "Convocatoria separada de dos páginas.",
                "Separate two-page notice.",
                relationship_kind="related-notice",
                source_document_id="SP-SRC-ACTA-2016-04-26-NOTICE-01",
            ),
        ],
        variant_note_es="La familia controlante contiene 77 páginas. Sus dos binarios son visual y textualmente equivalentes; los paquetes de 24, 47 y 50 páginas son parciales. Las páginas 14-77 son anexos reservados íntegramente en la copia pública.",
        variant_note_en="The controlling family contains 77 pages. Its two binaries are visually and textually equivalent; the 24-, 47- and 50-page packages are partial. Pages 14-77 are annexes wholly withheld in the public copy.",
    ),
    ActaConfig(
        "2017-04-07-cexp", "2017-04-07-cexp-source.pdf", body="CEXP", meeting_type="extraordinary",
        source_document_id="SP-SRC-ACTA-2017-04-07-CEXP-PUBLIC-CONTROL",
        legacy_source_id_aliases=["SP-SRC-ACTA-2017-04-07-cexp"],
        variants=[variant(
            None,
            "Export PDF de Drive registrado por separado; mismo tamaño, SHA-256 distinto del control público.",
            "Separately registered Drive PDF export; same byte count, different SHA-256 from the public control.",
            source_document_id="SP-SRC-ACTA-2017-04-07-CEXP",
            relationship_kind="registered-drive-export-distinct-binary",
            expected_bytes=84535,
            expected_sha256="e2612c11bb243893492b4a490c37ccdada270a8400d5764e8e309a674c95736f",
            expected_pages=2,
        )],
        variant_note_es="El control público y el export Drive registrado tienen 84.535 bytes, pero SHA-256 distintos; se conservan como binarios separados.",
        variant_note_en="The public control and registered Drive export are each 84,535 bytes but have different SHA-256 values; they remain separate binaries.",
    ),
    ActaConfig("2017-06-12", "ACTA Junta Gral Orrdinaria 12 JUNIO 2017.pdf", full_redaction_pages={2, 5, 6, 7, 8, 9, 10}, partial_tail_redactions={1: 0.58}),
    ActaConfig(
        "2018-05-18", "ACTAS_zip_nested_extracted/ACTAS/ACTA 18 MAY 2018/ACTA 18 MAY 2018.pdf",
        source_document_id="SP-SRC-ACTA-2018-05-18-B",
        legacy_source_id_aliases=["SP-SRC-ACTA-2018-05-18"],
        reuse_existing_pages=False, full_redaction_pages={2, 8, 9}, partial_tail_redactions={1: 0.58, 7: 0.30},
        variants=[
            variant(
                "2018-05-18-package.pdf", "Segunda conversión/paquete de nueve páginas.", "Second nine-page conversion/package.",
                source_document_id="SP-SRC-ACTA-2018-05-18-B-ALT", legacy_id_aliases=["SP-SRC-ACTA-2018-05-18-VARIANT-01"],
            ),
            variant(
                "2018-05-18-source.pdf", "Variante parcial de ocho páginas con texto extraíble.", "Partial eight-page variant with extractable text.",
                source_document_id="SP-SRC-ACTA-2018-05-18-A", legacy_id_aliases=["SP-SRC-ACTA-2018-05-18-VARIANT-02"],
            ),
            variant(
                "2018-05-18-alt.pdf", "Variante parcial alternativa de ocho páginas.", "Alternate partial eight-page variant.",
                source_document_id="SP-SRC-ACTA-2018-05-18-C", legacy_id_aliases=["SP-SRC-ACTA-2018-05-18-VARIANT-03"],
            ),
        ],
        variant_note_es="Control de nueve páginas recuperado y controlado desde ACTAS.zip; la autenticidad permanece abierta. La segunda copia de nueve páginas y las dos variantes parciales de ocho páginas conservan IDs, tamaños y SHA-256 separados.",
        variant_note_en="Nine-page control recovered and controlled from ACTAS.zip; authenticity remains open. The second nine-page copy and two partial eight-page variants retain separate IDs, byte counts and SHA-256 values.",
    ),
    ActaConfig(
        "2018-07-05", "2018-07-05-variant-a.pdf", meeting_type="extraordinary",
        reuse_existing_pages=False, full_redaction_pages={2, 5, 6, 7, 8, 9}, partial_tail_redactions={1: 0.62},
        variants=[
            variant(
                "2018-07-05-variant-b.pdf", "Binario distinto; las nueve páginas renderizan de forma idéntica.", "Different binary; all nine pages render identically.",
                source_document_id="SP-SRC-ACTA-2018-07-05-ALT", legacy_id_aliases=["SP-SRC-ACTA-2018-07-05-VARIANT-01"],
            ),
            variant(
                "CONVOCATORIA SUN PARK 5-7-18.pdf",
                "Convocatoria separada de una página.",
                "Separate one-page notice.",
                relationship_kind="related-notice",
                source_document_id="SP-SRC-ACTA-2018-07-05-NOTICE-01",
            ),
        ],
        variant_note_es="Copia exacta de nueve páginas recuperada de ACTAS.zip; el segundo binario renderiza idénticamente.",
        variant_note_en="Exact nine-page copy recovered from ACTAS.zip; the second binary renders identically.",
    ),
    ActaConfig(
        "2022-02-04", "ACTA JUN EXTRA FEB22-31032022110911.pdf", meeting_type="extraordinary",
        full_redaction_pages={5, 6}, partial_tail_redactions={1: 0.58, 2: 0.78, 4: 0.42, 7: 0.58},
        variants=[
            variant(
                "ACTA de CDAD (reconocimiento coste arreglar daños 4.5mEUR) 04FEB2022.pdf",
                "Binario alternativo de siete páginas con resaltados visibles.",
                "Alternate seven-page binary with visible highlighting.",
                source_document_id="SP-SRC-ACTA-2022-02-04-ALT-3492026",
                legacy_id_aliases=["SP-SRC-ACTA-2022-02-04-NATIVE-VARIANT-01"],
            ),
            variant(
                None,
                "Tercer binario nativo conocido de siete páginas, controlado por tamaño y SHA-256; no está presente localmente y su relación material con las otras copias sigue sin resolverse.",
                "Third known seven-page native binary, controlled by size and SHA-256; it is not present locally and its material relationship to the other copies remains unresolved.",
                relationship_kind="native-variant",
                source_document_id="SP-SRC-ACTA-2022-02-04-ALT",
                legacy_id_aliases=["SP-SRC-ACTA-2022-02-04-NATIVE-VARIANT-02"],
                classification_status="relationship-unresolved",
                classification_note_es="Variante conocida por metadatos de control; nombre nativo y relación exacta no establecidos.",
                classification_note_en="Variant known by control metadata; native filename and exact relationship are not established.",
                expected_bytes=3015343,
                expected_sha256="56355a84eadbbd2cc085d650c20bc56560b1006992fcf6f462ecc5d6875b39e0",
                expected_pages=7,
            ),
        ],
    ),
    ActaConfig(
        "2022-03-11-ricpe-shareholder-notice",
        "ricpe-extraordinary-shareholders-notice-2022-02-11.pdf",
        display_name="convocatoria y orden del día RICPE de cinco páginas",
        body="corporate",
        meeting_type="scheduled-corporate-meeting",
        document_type="shareholder-meeting-notice-and-agenda",
        source_package_kind="non-acta-notice-and-agenda",
        counts_as_located_acta_family=False,
        unlocated_meeting_or_minutes_original_count=1,
        event_id="SP-MEETING-2022-03-11-RICPE",
        source_document_id="SP-SRC-NOTICE-RICPE-2022-02-11-5P",
        event_date="2022-03-11",
        title_es="11 marzo 2022 · junta extraordinaria de accionistas RICPE convocada",
        title_en="11 March 2022 · scheduled RICPE extraordinary shareholders' meeting",
        document_issue_date="2022-02-11",
        issuing_person_or_body="RICPE board through its secretary, as attributed in the received document",
        stated_capacity="Board / Secretary, as stated in the received document; actual authorship and issuance open",
        recipients=["shareholders"],
        scheduled_meeting_first_call="2022-03-11",
        scheduled_meeting_second_call="2022-03-12",
        documented_meeting_status={
            "notice_and_agenda_located": True,
            "meeting_occurrence_proved": False,
            "quorum_proved": False,
            "votes_proved": False,
            "outcome_proved": False,
            "minutes_or_outcome_record_located": False,
        },
        referenced_prior_resolution={
            "date": "2021-12-29",
            "evidence_status": "later-recital-in-notice",
            "primary_records_located": False,
        },
        expected_source_bytes=191251,
        expected_source_sha256="3858b928d4eee8a4f5e9b21f5452c9e58cbbfbd22debccb38bfe3dd07db303c4",
        expected_source_pages=5,
        source_page_scope="five-page-shareholder-notice-and-agenda",
        full_redaction_pages=set(range(1, 6)),
        reuse_existing_pages=False,
        continuity_registration_required=False,
        variant_note_es=(
            "El documento recibido de cinco páginas está fechado el 11 de febrero "
            "de 2022 y atribuye al Consejo de RIC Private Equity Investment "
            "Partners, S.C.R., S.A., por medio de su secretario, una convocatoria "
            "propuesta para primera convocatoria el 11 de marzo y segunda el 12 "
            "de marzo. Registra texto de convocatoria y orden del día, pero no "
            "prueba autoría, emisión efectiva, servicio o conocimiento del "
            "destinatario. No es un ACTA: la celebración, el cuórum, las votaciones "
            "y el resultado no están probados. La mención de un "
            "acuerdo de accionistas de 29 de diciembre de 2021 es una referencia "
            "posterior; sus registros primarios siguen sin localizarse."
        ),
        variant_note_en=(
            "The received five-page document is dated 11 February 2022 and "
            "attributes to the Board of RIC Private Equity Investment Partners, "
            "S.C.R., S.A., through its secretary, a proposed first call on 11 "
            "March and second call on 12 March. It records notice and agenda "
            "wording but does not prove authorship, actual issuance, service or "
            "recipient knowledge. This is not minutes: occurrence, quorum, votes "
            "and outcome are unproved. The "
            "reference to a 29 December 2021 shareholder resolution is a later "
            "recital; its primary records remain unlocated."
        ),
    ),
]

EXPECTED_PUBLIC_CORPUS_COUNTS = {
    "controlled_source_packages": 20,
    "located_acta_or_minutes_families": 19,
    "located_non_acta_source_packages": 1,
    "public_redacted_ocr_packages": 17,
    "marker_only_public_redaction_packages": 3,
    "known_unlocated_meeting_or_minutes_originals": 3,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@lru_cache(maxsize=1)
def ocr_language() -> tuple[str, str]:
    """Return the installed OCR language and its public-safe selection note.

    Spanish is preferred for this corpus.  English is an explicit operational
    fallback only when the local Tesseract installation lacks ``spa``; neither
    selection changes the non-certified status of the OCR output.
    """

    result = subprocess.run(
        ["tesseract", "--list-langs"],
        check=True,
        capture_output=True,
        text=True,
    )
    installed = {
        line.strip()
        for line in (result.stdout + "\n" + result.stderr).splitlines()
        if line.strip() and not line.lower().startswith("list of available languages")
    }
    if "spa" in installed:
        return "spa", "spa-installed-selected"
    if "eng" in installed:
        return "eng", "spa-unavailable-eng-fallback"
    raise RuntimeError(
        "Tesseract has neither the preferred 'spa' language nor the documented "
        "'eng' fallback installed"
    )


def controlling_source_document_id(config: ActaConfig) -> str:
    if config.source_document_id:
        return config.source_document_id
    if config.event_id and config.event_id.startswith("SP-ACTA-"):
        return "SP-SRC-ACTA-" + config.event_id.removeprefix("SP-ACTA-")
    return f"SP-SRC-ACTA-{config.slug}"


def variant_source_document_id(
    config: ActaConfig,
    item: SourceVariant,
    position: int,
) -> str:
    return item.source_document_id or f"SP-SRC-ACTA-{config.slug}-VARIANT-{position:02d}"


def is_configured_marker_only(config: ActaConfig) -> bool:
    """Return the configured public-text mode without reading private bytes."""

    if not config.full_redaction_pages or min(config.full_redaction_pages) != 1:
        return False
    configured_total = config.expected_source_pages or max(config.full_redaction_pages)
    return config.full_redaction_pages == set(range(1, configured_total + 1))


def validate_config_source_document_ids() -> None:
    slugs = [config.slug for config in CONFIGS]
    if len(slugs) != len(set(slugs)):
        raise RuntimeError("Duplicate ACTA config slug")

    identifiers: list[str] = []
    aliases: list[str] = []
    for config in CONFIGS:
        identifiers.append(controlling_source_document_id(config))
        aliases.extend(config.legacy_source_id_aliases)
        identifiers.extend(
            variant_source_document_id(config, item, position)
            for position, item in enumerate(config.variants, start=1)
        )
        for item in config.variants:
            aliases.extend(item.legacy_id_aliases)
    duplicates = sorted({value for value in identifiers if identifiers.count(value) > 1})
    if duplicates:
        raise RuntimeError(f"Duplicate stable source-document ID(s): {duplicates}")
    duplicate_aliases = sorted({value for value in aliases if aliases.count(value) > 1})
    if duplicate_aliases:
        raise RuntimeError(f"Duplicate legacy source-document alias(es): {duplicate_aliases}")
    alias_collisions = sorted(set(aliases) & set(identifiers))
    if alias_collisions:
        raise RuntimeError(
            f"Legacy source-document alias collides with a canonical ID: {alias_collisions}"
        )

    configured_acta_families = sum(
        config.counts_as_located_acta_family for config in CONFIGS
    )
    configured_non_acta_packages = len(CONFIGS) - configured_acta_families
    configured_marker_only = sum(
        is_configured_marker_only(config)
        for config in CONFIGS
    )
    configured_unlocated_meeting_minutes = sum(
        int(item.get("counts_as_unlocated_meeting_or_minutes_original", False))
        for item in KNOWN_UNLOCATED_SOURCES
    ) + sum(config.unlocated_meeting_or_minutes_original_count for config in CONFIGS)
    configured_counts = {
        "controlled_source_packages": len(CONFIGS),
        "located_acta_or_minutes_families": configured_acta_families,
        "located_non_acta_source_packages": configured_non_acta_packages,
        "public_redacted_ocr_packages": len(CONFIGS) - configured_marker_only,
        "marker_only_public_redaction_packages": configured_marker_only,
        "known_unlocated_meeting_or_minutes_originals": configured_unlocated_meeting_minutes,
    }
    if configured_counts != EXPECTED_PUBLIC_CORPUS_COUNTS:
        raise RuntimeError(
            "Configured public corpus counts differ from the controlled 20-package "
            f"baseline: {configured_counts}"
        )

    ricpe = next(
        (config for config in CONFIGS if config.slug == "2022-03-11-ricpe-shareholder-notice"),
        None,
    )
    expected_ricpe = {
        "event_id": "SP-MEETING-2022-03-11-RICPE",
        "source_document_id": "SP-SRC-NOTICE-RICPE-2022-02-11-5P",
        "document_type": "shareholder-meeting-notice-and-agenda",
        "source_package_kind": "non-acta-notice-and-agenda",
        "event_date": "2022-03-11",
        "document_issue_date": "2022-02-11",
        "scheduled_meeting_first_call": "2022-03-11",
        "scheduled_meeting_second_call": "2022-03-12",
        "expected_source_bytes": 191251,
        "expected_source_sha256": "3858b928d4eee8a4f5e9b21f5452c9e58cbbfbd22debccb38bfe3dd07db303c4",
        "expected_source_pages": 5,
        "counts_as_located_acta_family": False,
    }
    if ricpe is None or any(
        getattr(ricpe, field_name) != expected
        for field_name, expected in expected_ricpe.items()
    ):
        raise RuntimeError("RICPE notice configuration differs from its controlled metadata")
    if ricpe.full_redaction_pages != set(range(1, 6)):
        raise RuntimeError("RICPE notice must remain a five-page marker-only public package")
    if any(
        ricpe.documented_meeting_status.get(field_name) is not False
        for field_name in (
            "meeting_occurrence_proved",
            "quorum_proved",
            "votes_proved",
            "outcome_proved",
            "minutes_or_outcome_record_located",
        )
    ):
        raise RuntimeError("RICPE notice must not imply occurrence, quorum, votes, outcome or minutes")

    continuity_path = ACTA_ROOT / "event-family-continuity-v1.json"
    if continuity_path.is_file():
        continuity_text = continuity_path.read_text(encoding="utf-8")
        missing = [
            config.source_document_id
            for config in CONFIGS
            if config.source_document_id
            and config.continuity_registration_required
            and f'"{config.source_document_id}"' not in continuity_text
        ]
        if missing:
            raise RuntimeError(
                "Explicit controlling source-document ID(s) do not match the "
                f"continuity register: {missing}"
            )


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_transcript(path: Path) -> tuple[str, list[str]]:
    if not path.is_file():
        return "", []
    text = path.read_text(encoding="utf-8")
    matches = list(PAGE_MARKER.finditer(text))
    pages: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        pages.append(text[match.end():end].strip())
    return text[: matches[0].start()].strip() if matches else text.strip(), pages


def source_pdf(config: ActaConfig, source_root: Path, tmp: Path) -> Path:
    source = source_root / config.source
    if config.source_kind == "pdf":
        return source
    out = tmp / "docx-conversion"
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out), str(source)],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    converted = out / f"{source.stem}.pdf"
    if not converted.is_file():
        raise RuntimeError(f"DOCX conversion failed for {source.name}")
    return converted


def render_pages(pdf: Path, out_dir: Path, dpi: int = 150) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(out_dir / "page")],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )
    pages = sorted(out_dir.glob("page-*.png"))
    if not pages:
        raise RuntimeError(f"No pages rendered from {pdf.name}")
    return pages


def extract_page_texts(pdf: Path, rendered: list[Path]) -> list[str]:
    reader = PdfReader(str(pdf))
    texts = [(page.extract_text() or "").strip() for page in reader.pages]
    language, _ = ocr_language()
    for index, text in enumerate(texts):
        if len(text) >= 80:
            continue
        result = subprocess.run(
            ["tesseract", str(rendered[index]), "stdout", "-l", language, "--psm", "6"],
            check=True, capture_output=True, text=True,
        )
        texts[index] = result.stdout.strip()
    return texts


def public_redact_text(text: str) -> str:
    text = text.replace("\x0c", "").replace("\u0000", "")
    text = ID_PATTERN.sub("[IDENTIFICADOR REDACTADO]", text)
    text = IBAN_PATTERN.sub("[DATO BANCARIO REDACTADO]", text)
    text = EMAIL_PATTERN.sub("[CORREO REDACTADO]", text)
    text = PHONE_PATTERN.sub("[TELÉFONO REDACTADO]", text)
    lines: list[str] = []
    for line in text.splitlines():
        compact = " ".join(line.split())
        if not compact:
            lines.append("")
            continue
        numeric_tokens = re.findall(r"\d+(?:[.,]\d+)?", compact)
        if SENSITIVE_LINE_PATTERN.search(compact) or ADDRESS_PATTERN.search(compact):
            lines.append("[LÍNEA CON IDENTIFICADOR, CONTACTO, DOMICILIO O FINCA REDACTADA]")
        elif len(numeric_tokens) >= 5 and re.search(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]", compact):
            lines.append("[FILA INDIVIDUAL FINANCIERA O DE VOTO REDACTADA]")
        elif re.search(r"(?i)\b(?:Vº\s*Bº|firmad[oa]|el\s+presidente|el\s+secretario)\b", compact):
            lines.append("[BLOQUE DE FIRMA REDACTADO]")
        else:
            lines.append(compact)
    output = "\n".join(lines)
    output = re.sub(r"(?:\n\[LÍNEA CON[^\n]+\]){2,}", "\n[BLOQUE NOMINAL/IDENTIFICATIVO REDACTADO]", output)
    return output.strip() or "[SIN TEXTO OCR FIABLE; VÉASE LA IMAGEN PÚBLICA REDACTADA DE ESTA PÁGINA]"


def full_redaction_marker(page: int, total: int) -> str:
    return (
        "[PÁGINA PÚBLICA ÍNTEGRAMENTE REDACTADA. La página fuente "
        f"{page} de {total} permanece contabilizada y preservada privadamente. "
        "Contiene una relación nominal, datos por propietario/finca/deuda/voto, "
        "datos bancarios, firmas o un anexo reservado que no puede publicarse con seguridad.]"
    )


def build_transcript(
    config: ActaConfig,
    event: dict[str, Any],
    source_path: Path,
    source_pdf_path: Path,
    rendered: list[Path],
) -> list[str]:
    transcript = ACTA_ROOT / config.slug / "transcript-es.md"
    _, existing = parse_transcript(transcript)
    total = len(rendered)
    if config.reuse_existing_pages and len(existing) == total:
        pages = existing
    elif config.full_redaction_pages == set(range(1, total + 1)):
        # The private review/OCR workstream remains separate from the public
        # derivative.  When every page is precautionarily withheld, do not
        # copy private OCR text into a public artifact: emit an explicit,
        # page-sequenced public redaction marker instead.
        pages = [full_redaction_marker(page, total) for page in range(1, total + 1)]
    elif config.reuse_prefix_pages and existing:
        texts = extract_page_texts(source_pdf_path, rendered)
        pages = []
        for page in range(1, total + 1):
            if page <= config.reuse_prefix_pages and page <= len(existing):
                pages.append(existing[page - 1])
            elif page in config.full_redaction_pages:
                pages.append(full_redaction_marker(page, total))
            else:
                pages.append(public_redact_text(texts[page - 1]))
    else:
        texts = extract_page_texts(source_pdf_path, rendered)
        pages = [
            full_redaction_marker(page, total)
            if page in config.full_redaction_pages
            else public_redact_text(texts[page - 1])
            for page in range(1, total + 1)
        ]

    if config.slug == "2012-08-10" and pages:
        pages[0] = re.sub(
            r"(?is)Asisten los siguientes propietarios:.*$",
            "[LISTA NOMINAL DE ASISTENTES, REPRESENTACIONES, FINCAS Y COEFICIENTES REDACTADA]",
            pages[0],
        )
    if config.slug == "2018-07-05" and pages:
        pages[0] = re.sub(
            r"(?is)LISTA DE ASISTENTES.*$",
            "[LISTA NOMINAL DE ASISTENTES, REPRESENTACIONES, FINCAS Y COEFICIENTES REDACTADA]",
            pages[0],
        )

    source_hash = sha256(source_path)
    language, language_selection = ocr_language()
    ocr_status = (
        "cada página pública contiene sólo un marcador de redacción integral; "
        "el mapeo/OCR privado de revisión no se publica ni se certifica"
        if config.full_redaction_pages == set(range(1, total + 1))
        else f"{language} ({language_selection}); resultado no certificado"
    )
    edition_label = (
        "Digitalización pública íntegramente redactada, secuenciada por cada página "
        "mediante marcadores expresos; no contiene OCR público."
        if config.full_redaction_pages == set(range(1, total + 1))
        else "Digitalización pública redactada, OCR-asistida y secuenciada por cada página de la copia localizada."
    )
    title = event.get("title_es") or event.get("id") or config.slug
    preamble = f"""# {title}

**{edition_label}**

- ID: `{event.get('id', config.slug)}`
- Fecha atribuida: `{event.get('date', config.slug[:10])}`
- Órgano: {config.body}
- Fuente de control: `{config.display_name}`
- Páginas fuente: {total}
- SHA-256 de la fuente privada: `{source_hash}`
- Estado: copia localizada digitalizada y publicada con redacciones irreversibles
- Estado OCR/texto público: {ocr_status}

## Advertencia de uso

No es el original, el libro diligenciado, una copia certificada ni una transcripción pericial. El texto cubre secuencialmente todas las páginas de la copia de control, pero el OCR no ha sido certificado línea por línea. Los datos personales, firmas, domicilios, contactos, identificadores, cuentas, tablas por propietario/finca/deuda/voto y anexos reservados se sustituyen por marcadores expresos.

**Control de variante:** {config.variant_note_es}
"""
    body = "\n\n".join(
        f"## Página fuente {number} de {total}\n\n{page.strip()}"
        for number, page in enumerate(pages, 1)
    )
    transcript.parent.mkdir(parents=True, exist_ok=True)
    transcript.write_text(preamble.strip() + "\n\n" + body + "\n", encoding="utf-8")
    return pages


def tesseract_sensitive_rectangles(image_path: Path) -> list[tuple[int, int, int, int]]:
    language, _ = ocr_language()
    result = subprocess.run(
        ["tesseract", str(image_path), "stdout", "-l", language, "--psm", "6", "tsv"],
        check=True, capture_output=True, text=True,
    )
    rows = result.stdout.splitlines()
    if not rows:
        return []
    header = rows[0].split("\t")
    groups: dict[tuple[str, str, str, str], list[dict[str, str]]] = {}
    for row in rows[1:]:
        values = row.split("\t")
        if len(values) != len(header):
            continue
        item = dict(zip(header, values))
        if not item.get("text", "").strip():
            continue
        key = tuple(item.get(value, "") for value in ("block_num", "par_num", "line_num", "page_num"))
        groups.setdefault(key, []).append(item)
    rectangles: list[tuple[int, int, int, int]] = []
    for words in groups.values():
        line = " ".join(word["text"] for word in words)
        numeric_tokens = re.findall(r"\d+(?:[.,]\d+)?", line)
        sensitive = bool(
            ID_PATTERN.search(line) or IBAN_PATTERN.search(line) or EMAIL_PATTERN.search(line)
            or PHONE_PATTERN.search(line) or SENSITIVE_LINE_PATTERN.search(line)
            or ADDRESS_PATTERN.search(line)
            or (len(numeric_tokens) >= 5 and re.search(r"[A-Za-z]", line))
        )
        if not sensitive:
            continue
        left = min(int(word["left"]) for word in words)
        top = min(int(word["top"]) for word in words)
        right = max(int(word["left"]) + int(word["width"]) for word in words)
        bottom = max(int(word["top"]) + int(word["height"]) for word in words)
        rectangles.append((max(0, left - 10), max(0, top - 6), right + 10, bottom + 6))
    return rectangles


def redact_image(
    image_path: Path,
    output: Path,
    page: int,
    total: int,
    full_page: bool,
    tail_fraction: float,
) -> None:
    with Image.open(image_path) as opened:
        image = opened.convert("L").convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size
    if full_page:
        draw.rectangle((0, 0, width, height), fill="white")
        font_size = max(24, min(54, width // 46, height // 64))
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()
        messages = (
            f"PÁGINA {page}/{total} · CONTENIDO PÚBLICO ÍNTEGRAMENTE REDACTADO",
            f"PAGE {page}/{total} · PUBLIC CONTENT FULLY REDACTED",
        )
        boxes = [draw.textbbox((0, 0), message, font=font) for message in messages]
        line_heights = [box[3] - box[1] for box in boxes]
        gap = max(10, font_size // 3)
        padding = max(24, font_size)
        band_height = sum(line_heights) + gap + padding * 2
        band_top = height // 2 - band_height // 2
        draw.rectangle((0, band_top, width, band_top + band_height), fill="black")
        y = band_top + padding
        for message, box, line_height in zip(messages, boxes, line_heights):
            line_width = box[2] - box[0]
            draw.text(((width - line_width) // 2, y), message, fill="white", font=font)
            y += line_height + gap
    else:
        font = ImageFont.load_default()
        for rectangle in tesseract_sensitive_rectangles(image_path):
            draw.rectangle(rectangle, fill="black")
        if tail_fraction:
            top = int(height * (1 - tail_fraction))
            draw.rectangle((0, top, width, height), fill="black")
            draw.text((20, top + 12), "BLOQUE NOMINAL / FIRMA / DATO PRIVADO REDACTADO", fill="white", font=font)
        banner_height = max(30, height // 45)
        draw.rectangle((0, 0, width, banner_height), fill="white")
        draw.rectangle((0, banner_height - 2, width, banner_height), fill="black")
        draw.text((12, 8), f"COPIA PÚBLICA REDACTADA - FUENTE {page}/{total}", fill="black", font=font)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.info.clear()
    image.save(output, "JPEG", quality=82, optimize=True, progressive=True)
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError(f"JPEG encoder produced an empty page: {output}")


def build_facsimile(
    config: ActaConfig,
    rendered: list[Path],
) -> tuple[Path, list[str], str]:
    out_dir = SOURCE_IMAGE_ROOT / config.slug
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    jpegs: list[Path] = []
    total = len(rendered)
    for page, source_image in enumerate(rendered, 1):
        output = out_dir / f"page-{page:03d}.jpg"
        redact_image(
            source_image, output, page, total,
            page in config.full_redaction_pages,
            max(config.partial_tail_redactions.get(page, 0.0), 0.42),
        )
        jpegs.append(output)

    facsimile = FACSIMILE_ROOT / f"{config.slug}-source-redacted-facsimile-es.pdf"
    facsimile.parent.mkdir(parents=True, exist_ok=True)
    page_width, page_height = A4
    rl_config.invariant = 1
    writer = canvas.Canvas(
        str(facsimile),
        pagesize=A4,
        pageCompression=1,
        invariant=1,
    )
    writer.setTitle(f"{config.slug} source redacted facsimile")
    writer.setAuthor("Project Sun Rock")
    writer.setCreator("Project Sun Rock deterministic ACTA digitisation pipeline")
    writer.setSubject("Raster-only public-redacted source facsimile")
    for path in jpegs:
        with Image.open(path) as image:
            width, height = image.size
        scale = min(page_width / width, page_height / height)
        draw_width, draw_height = width * scale, height * scale
        writer.drawImage(
            ImageReader(str(path)),
            (page_width - draw_width) / 2,
            (page_height - draw_height) / 2,
            width=draw_width,
            height=draw_height,
            preserveAspectRatio=True,
            mask="auto",
        )
        writer.showPage()
    writer.save()
    public_paths = [path.relative_to(REPO).as_posix() for path in jpegs]
    return facsimile, public_paths, sha256(facsimile)


def update_redaction_log(config: ActaConfig, total: int) -> None:
    path = ACTA_ROOT / config.slug / "redaction-log.md"
    lines = [
        f"# Registro de redacciones - {config.slug}", "",
        "La fuente privada no se altera. La copia pública es rasterizada y todas las redacciones están quemadas; no existe capa de texto oculta en el facsímil.", "",
        "| Página fuente | Alcance | Motivo |", "|---:|---|---|",
    ]
    for page in range(1, total + 1):
        if page in config.full_redaction_pages:
            scope = "página completa"
            reason = "Lista nominal, tabla individual, dato bancario, firma o anexo reservado."
        else:
            scope = "selectivo + pie de firma"
            reason = "Identificadores, contactos, fincas, filas individuales y firmas detectadas; se conserva el texto sustantivo visible."
        lines.append(f"| {page} | {scope} | {reason} |")
    lines += [
        "", "## Control de calidad", "",
        "- Todas las páginas de la copia fuente están contabilizadas: `true`",
        "- Facsímil raster sin texto oculto: `true`",
        "- OCR certificado línea por línea: `false`",
        "- Fuente privada publicada: `false`",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_provenance(config: ActaConfig, source_path: Path, total: int) -> None:
    path = ACTA_ROOT / config.slug / "provenance.md"
    variant_lines: list[str] = []
    for position, item in enumerate(config.variants, start=1):
        document_id = variant_source_document_id(config, item, position)
        candidate = source_path.parent / item.path if item.path else None
        if candidate is not None and candidate.is_file():
            variant_lines.append(
                f"- `{document_id}` / `{sha256(candidate)}` / "
                f"`{item.relationship_kind}` — {item.relationship_es}"
            )
        elif item.expected_sha256:
            variant_lines.append(
                f"- `{document_id}` / `{item.expected_sha256}` / "
                f"`{item.relationship_kind}` — {item.relationship_es} "
                "Estado local de esta ejecución: `missing-local`."
            )
        else:
            variant_lines.append(
                f"- `{document_id}` / `{item.relationship_kind}` — "
                f"{item.relationship_es} No se aportó a la raíz de fuentes de esta ejecución."
            )
    variants = "\n".join(variant_lines) or "- No se ha identificado otra fuente relacionada."
    language, language_selection = ocr_language()
    acquisition = ""
    if config.acquisition_note_es:
        acquisition = f"- Ruta de adquisición: {config.acquisition_note_es}\n"
    public_derivative_description = (
        "sólo marcadores públicos de redacción integral secuenciados por página, "
        "facsímil raster redactado e imágenes JPEG redactadas; no se publica OCR"
        if config.full_redaction_pages == set(range(1, total + 1))
        else "sólo texto OCR redactado, facsímil raster redactado e imágenes de página JPEG redactadas"
    )
    text = f"""# Procedencia pública - {config.slug}

## Fuente de control

- Tipo: `{config.source_kind.upper()}`
- Páginas: `{total}`
- Alcance del recuento de páginas: `{config.source_page_scope}`
- Bytes: `{source_path.stat().st_size}`
- SHA-256: `{sha256(source_path)}`
- ID estable de documento fuente: `{controlling_source_document_id(config)}`
{acquisition.rstrip()}
- Custodia: fuente nativa preservada fuera del repositorio público.
- Publicación: {public_derivative_description}.
- Formatos heredados: los WEBP históricos, si se conservan, son derivados separados; no son las imágenes fuente/página actuales.
- Idioma OCR operativo: `{language}` (`{language_selection}`); el resultado no está certificado.

## Relación de variantes

{variants}

## Límites

El hash identifica los bytes recibidos, no acredita por sí solo un original oficial, una copia certificada, la validez de la junta ni una cadena de custodia forense ininterrumpida. El OCR no ha sido certificado línea por línea.
"""
    path.write_text(text, encoding="utf-8")


def source_info(path: Path, pages: int | None = None) -> dict[str, Any]:
    if pages is None and path.suffix.lower() == ".pdf":
        pages = len(PdfReader(str(path)).pages)
    return {
        "filename": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "pages": pages,
    }


def validate_expected_control_metadata(
    config: ActaConfig,
    info: dict[str, Any],
) -> None:
    expected = {
        "bytes": config.expected_source_bytes,
        "sha256": config.expected_source_sha256,
        "pages": config.expected_source_pages,
    }
    mismatches = {
        key: (value, info.get(key))
        for key, value in expected.items()
        if value is not None and info.get(key) != value
    }
    if mismatches:
        raise RuntimeError(
            f"{config.slug}: controlling source does not match configured "
            f"bytes/hash/pages: {mismatches}"
        )


def seed_event(config: ActaConfig) -> dict[str, Any]:
    date = config.event_date or config.slug[:10]
    event = {
        "id": config.event_id or f"SP-ACTA-{config.slug.upper()}",
        "slug": config.slug,
        "date": date,
        "language": "es",
        "title_es": config.title_es or f"ACTA - {date}",
        "title_en": config.title_en or f"Minutes - {date}",
        "body": config.body,
        "meeting_type": config.meeting_type,
        "document_type": config.document_type,
        "source_package_kind": config.source_package_kind,
        "counts_as_located_acta_family": config.counts_as_located_acta_family,
    }
    if config.meeting_time:
        event["meeting_time"] = config.meeting_time
    if config.document_issue_date:
        event["document_issue_date"] = config.document_issue_date
    if config.issuing_person_or_body:
        event["issuing_person_or_body"] = config.issuing_person_or_body
    if config.stated_capacity:
        event["stated_capacity"] = config.stated_capacity
    if config.recipients:
        event["recipients"] = list(config.recipients)
    if config.scheduled_meeting_first_call:
        event["scheduled_meeting_first_call"] = config.scheduled_meeting_first_call
    if config.scheduled_meeting_second_call:
        event["scheduled_meeting_second_call"] = config.scheduled_meeting_second_call
    if config.documented_meeting_status:
        event["documented_meeting_status"] = dict(config.documented_meeting_status)
    if config.referenced_prior_resolution:
        event["referenced_prior_resolution"] = dict(config.referenced_prior_resolution)
    return event


def existing_reconciliation_families() -> dict[str, dict[str, Any]]:
    path = ACTA_ROOT / "source-family-reconciliation-v2.json"
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return {
        family["slug"]: family
        for family in value.get("families", [])
        if isinstance(family, dict) and isinstance(family.get("slug"), str)
    }


def existing_variant(
    family: dict[str, Any] | None,
    item: SourceVariant,
) -> dict[str, Any] | None:
    if family is None:
        return None
    rows = family.get("additional_variants", [])
    if not isinstance(rows, list):
        return None
    for row in rows:
        if not isinstance(row, dict):
            continue
        if item.source_document_id and row.get("source_document_id") == item.source_document_id:
            return row
        if row.get("source_document_id") in item.legacy_id_aliases:
            return row
        if item.expected_sha256 and row.get("sha256") == item.expected_sha256:
            return row
        if item.path and row.get("filename") == Path(item.path).name:
            return row
    return None


def source_variant_descriptor(
    config: ActaConfig,
    item: SourceVariant,
    position: int,
    source_root: Path,
    *,
    existing_family: dict[str, Any] | None = None,
    selected_for_rebuild: bool = True,
) -> dict[str, Any]:
    """Describe a variant or related document without inventing absent bytes."""

    prior = existing_variant(existing_family, item)
    candidate = source_root / item.path if item.path else None
    descriptor: dict[str, Any] = dict(prior or {})
    if candidate is not None and candidate.is_file() and selected_for_rebuild:
        descriptor.update(source_info(candidate))
        descriptor["local_source_status"] = "present"
        descriptor["metadata_status"] = "computed-from-current-run"
    elif prior is not None:
        descriptor["local_source_status"] = (
            "missing-local" if selected_for_rebuild else "not-evaluated-unselected"
        )
        descriptor["metadata_status"] = "carried-forward-from-existing-public-reconciliation"
    else:
        if item.path:
            descriptor["filename"] = Path(item.path).name
        if item.expected_bytes is not None:
            descriptor["bytes"] = item.expected_bytes
        if item.expected_sha256 is not None:
            descriptor["sha256"] = item.expected_sha256
        if item.expected_pages is not None:
            descriptor["pages"] = item.expected_pages
        descriptor["local_source_status"] = "missing-local"
        descriptor["metadata_status"] = (
            "known-by-controlled-hash-and-size"
            if item.expected_sha256
            else "descriptor-only-no-local-bytes"
        )

    descriptor.update({
        "source_document_id": variant_source_document_id(config, item, position),
        "legacy_id_aliases": item.legacy_id_aliases,
        "relationship_kind": item.relationship_kind,
        "relationship_es": item.relationship_es,
        "relationship_en": item.relationship_en,
        "classification_status": item.classification_status,
    })
    if item.classification_note_es:
        descriptor["classification_note_es"] = item.classification_note_es
    if item.classification_note_en:
        descriptor["classification_note_en"] = item.classification_note_en
    if item.component_files:
        descriptor["component_files"] = [dict(row) for row in item.component_files]
        descriptor["record_level_sha256"] = None
        descriptor["record_level_hash_status"] = (
            "multi-file-group; use component_files SHA-256 values"
        )
    return descriptor


def update_manifest_and_event(
    config: ActaConfig,
    event: dict[str, Any],
    source_path: Path,
    total: int,
    facsimile: Path,
    source_images: list[str],
    facsimile_hash: str,
    visual_review_attested: bool,
) -> None:
    manifest_path = ACTA_ROOT / config.slug / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
    existing_family = existing_reconciliation_families().get(config.slug)
    source_documents = [
        source_variant_descriptor(
            config,
            item,
            position,
            source_path.parent,
            existing_family=existing_family,
        )
        for position, item in enumerate(config.variants, start=1)
    ]
    source_image_hashes = [
        {"path": value, "sha256": sha256(REPO / value)}
        for value in source_images
    ]
    language, language_selection = ocr_language()
    marker_only_text = config.full_redaction_pages == set(range(1, total + 1))
    public_text_mode = "full-page-redaction-markers" if marker_only_text else "redacted-ocr-text"
    manifest.update({
        "schema_version": "2.0",
        "id": event.get("id", f"SP-ACTA-{config.slug.upper()}"),
        "slug": config.slug,
        "date": event.get("date", config.slug[:10]),
        "body": config.body,
        "meeting_type": config.meeting_type,
        "document_type": config.document_type,
        "source_package_kind": config.source_package_kind,
        "counts_as_located_acta_family": config.counts_as_located_acta_family,
        "language": "es",
        "status": "located-package-digitised-public",
        "privacy_level": "public-redacted",
        "artifact_kind": "public-redacted-digitisation-package",
        "redacted_facsimile_available": True,
        "source_page_images_available": True,
        "complete_public_text": False,
        "public_text_mode": public_text_mode,
        "public_ocr_available": not marker_only_text,
        "digitisation_complete_for_located_copy": True,
        "manual_source_line_verification": False,
        "native_page_count": total,
        "native_page_count_status": "verified-for-located-control-copy",
        "source_variant_page_count": total,
        "source": {
            **source_info(source_path, total if config.source_kind == "docx" else None),
            "filename": config.display_name,
            "source_document_id": controlling_source_document_id(config),
            "legacy_id_aliases": config.legacy_source_id_aliases,
            "source_page_scope": config.source_page_scope,
            "variant_note_es": config.variant_note_es,
            "variant_note_en": config.variant_note_en,
            "native_publication": False,
            "variants_recorded": len(config.variants),
            "additional_source_documents_recorded": len(source_documents),
            "additional_source_documents": source_documents,
        },
        "redaction_categories": [
            "identifiers-and-contact", "signatures", "owner-unit-vote-and-debt",
            "banking-data", "reserved-annexes",
        ],
        "created": GENERATED_DATE,
    })
    for field_name in (
        "document_issue_date",
        "issuing_person_or_body",
        "stated_capacity",
        "scheduled_meeting_first_call",
        "scheduled_meeting_second_call",
    ):
        value = getattr(config, field_name)
        if value:
            manifest[field_name] = value
    if config.recipients:
        manifest["recipients"] = list(config.recipients)
    if config.documented_meeting_status:
        manifest["documented_meeting_status"] = dict(config.documented_meeting_status)
    if config.referenced_prior_resolution:
        manifest["referenced_prior_resolution"] = dict(config.referenced_prior_resolution)
    if config.acquisition_note_es:
        manifest["source"]["acquisition_note_es"] = config.acquisition_note_es
    if config.acquisition_note_en:
        manifest["source"]["acquisition_note_en"] = config.acquisition_note_en
    artifacts = manifest.setdefault("public_artifacts", {})
    artifacts.update({
        "transcript_es": f"evidence/community/actas/{config.slug}/transcript-es.md",
        "provenance": f"evidence/community/actas/{config.slug}/provenance.md",
        "redaction_log": f"evidence/community/actas/{config.slug}/redaction-log.md",
        "redacted_source_facsimile": facsimile.relative_to(REPO).as_posix(),
        "redacted_source_facsimile_sha256": facsimile_hash,
        "redacted_source_facsimile_pages": total,
        "source_preview_pages": source_images,
        "source_preview_count": total,
        "source_preview_sha256": source_image_hashes,
    })
    artifacts.setdefault("pdf", f"assets/docs/community-actas/{config.slug}-public-redacted-es.pdf")
    quality = manifest.setdefault("quality_control", {})
    quality.update({
        "source_page_count_verified": True,
        "facsimile_reopened": True,
        "all_source_pages_rendered": True,
        "facsimile_hidden_text": False,
        "privacy_scan": (
            "automated-pass-plus-recorded-visual-review-pass"
            if visual_review_attested
            else "automated-pass-visual-review-pending"
        ),
        "ocr_not_certified": True,
        "manual_source_line_verification": False,
        "visual_pdf_sample_review": visual_review_attested,
        "visual_source_redaction_review": visual_review_attested,
        "visual_review_attestation_required": True,
        "source_preview_hashes_recorded": True,
        "source_image_current_format": "JPEG",
        "legacy_webp_derivatives_separate": True,
        "facsimile_deterministic_invariant": True,
        "ocr_language": language,
        "ocr_language_selection": language_selection,
        "ocr_certified": False,
    })
    write_json(manifest_path, manifest)

    event.update({
        "body": config.body,
        "meeting_type": config.meeting_type,
        "document_type": config.document_type,
        "source_package_kind": config.source_package_kind,
        "counts_as_located_acta_family": config.counts_as_located_acta_family,
        "status": "located-package-digitised-public",
        "complete_public_text": False,
        "public_text_mode": public_text_mode,
        "public_ocr_available": not marker_only_text,
        "page_sequenced_redacted_text_available": True,
        "digitisation_complete_for_located_copy": True,
        "source_pages": total,
        "native_page_count": total,
        "native_page_count_status": "verified-for-located-control-copy",
        "source_variant_page_count": total,
        "source_hash_sha256": sha256(source_path),
        "source_document_id": controlling_source_document_id(config),
        "source_document_id_legacy_aliases": config.legacy_source_id_aliases,
        "source_page_scope": config.source_page_scope,
        "additional_source_documents": source_documents,
        "source_variant_note": config.variant_note_es,
        "source_variant_note_es": config.variant_note_es,
        "source_variant_note_en": config.variant_note_en,
        "package_path": f"evidence/community/actas/{config.slug}",
        "transcript_path": f"evidence/community/actas/{config.slug}/transcript-es.md",
        "transcript_source": f"evidence/community/actas/{config.slug}/transcript-es.md",
        "provenance_path": f"evidence/community/actas/{config.slug}/provenance.md",
        "redaction_log_path": f"evidence/community/actas/{config.slug}/redaction-log.md",
        "manifest_path": f"evidence/community/actas/{config.slug}/manifest.json",
        "manifest": f"evidence/community/actas/{config.slug}/manifest.json",
        "public_pdf_path": event.get("public_pdf_path", f"assets/docs/community-actas/{config.slug}-public-redacted-es.pdf"),
        "public_pdf": event.get("public_pdf", f"assets/docs/community-actas/{config.slug}-public-redacted-es.pdf"),
        "preview_dir": event.get("preview_dir", f"assets/evidence/community-actas/{config.slug}"),
        "preview_pages": event.get("preview_pages", []),
        "preview_count": event.get("preview_count", 0),
        "page_count": event.get("page_count", 0),
        "public_pdf_page_count": event.get("public_pdf_page_count", 0),
        "privacy_level": "public-redacted",
        "artifact_kind": "public-redacted-digitisation-package",
        "redacted_facsimile_available": True,
        "source_page_images_available": True,
        "manual_source_line_verification": False,
        "redacted_source_facsimile": facsimile.relative_to(REPO).as_posix(),
        "redacted_source_facsimile_sha256": facsimile_hash,
        "redacted_source_facsimile_pages": total,
        "source_preview_dir": (SOURCE_IMAGE_ROOT / config.slug).relative_to(REPO).as_posix(),
        "source_preview_pages": source_images,
        "source_preview_count": total,
        "source_preview_sha256": source_image_hashes,
        "limitations": config.variant_note_es + " OCR no certificado línea por línea.",
    })
    for field_name in (
        "document_issue_date",
        "issuing_person_or_body",
        "stated_capacity",
        "scheduled_meeting_first_call",
        "scheduled_meeting_second_call",
    ):
        value = getattr(config, field_name)
        if value:
            event[field_name] = value
    if config.recipients:
        event["recipients"] = list(config.recipients)
    if config.documented_meeting_status:
        event["documented_meeting_status"] = dict(config.documented_meeting_status)
    if config.referenced_prior_resolution:
        event["referenced_prior_resolution"] = dict(config.referenced_prior_resolution)
    if config.meeting_time:
        event["meeting_time"] = config.meeting_time
    if config.acquisition_note_es or config.acquisition_note_en:
        event["acquisition_provenance"] = {
            "status": "later-professional-carrier-not-original-circulation-proof",
            "note_es": config.acquisition_note_es,
            "note_en": config.acquisition_note_en,
            "private_carrier_material_published": False,
        }


def build_reconciliation(
    source_root: Path,
    selected_slugs: set[str] | None = None,
) -> dict[str, Any]:
    """Build reconciliation while preserving unselected families on partial runs.

    A full build (``selected_slugs is None``) still requires every controlling
    source.  A selected-slug build may use a partial private source root: the
    existing public reconciliation supplies the unselected family metadata, and
    no absent source is silently reclassified as never having existed.
    """

    validate_config_source_document_ids()
    existing_path = ACTA_ROOT / "source-family-reconciliation-v2.json"
    existing_document = (
        json.loads(existing_path.read_text(encoding="utf-8"))
        if existing_path.is_file()
        else {}
    )
    existing_families = {
        family["slug"]: family
        for family in existing_document.get("families", [])
        if isinstance(family, dict) and isinstance(family.get("slug"), str)
    }

    families = []
    for config in CONFIGS:
        selected_for_rebuild = selected_slugs is None or config.slug in selected_slugs
        controlling = source_root / config.source
        prior_family = existing_families.get(config.slug)
        if selected_for_rebuild:
            if not controlling.is_file():
                raise RuntimeError(
                    f"{config.slug}: missing controlling source for selected rebuild: "
                    f"{config.source}"
                )
            control_info = source_info(
                controlling,
                4 if config.source_kind == "docx" else None,
            )
            validate_expected_control_metadata(config, control_info)
            control_info.update({
                "filename": config.display_name,
                "local_source_status": "present",
                "metadata_status": "computed-from-current-run",
            })
        else:
            if prior_family is not None and isinstance(prior_family.get("controlling_copy"), dict):
                control_info = dict(prior_family["controlling_copy"])
                control_info.update({
                    "local_source_status": "not-evaluated-unselected",
                    "metadata_status": "carried-forward-from-existing-public-reconciliation",
                })
            elif all(
                value is not None
                for value in (
                    config.expected_source_bytes,
                    config.expected_source_sha256,
                    config.expected_source_pages,
                )
            ):
                control_info = {
                    "filename": config.display_name,
                    "bytes": config.expected_source_bytes,
                    "sha256": config.expected_source_sha256,
                    "pages": config.expected_source_pages,
                    "local_source_status": "not-evaluated-unselected",
                    "metadata_status": "configured-control-metadata-source-not-in-partial-run",
                }
            else:
                raise RuntimeError(
                    f"{config.slug}: unselected source is absent and no existing "
                    "reconciliation entry can be preserved"
                )
        control_info.update({
            "source_document_id": controlling_source_document_id(config),
            "legacy_id_aliases": config.legacy_source_id_aliases,
            "relationship_kind": "controlling-copy",
            "classification_status": "controlling-copy-for-public-package",
            "source_page_scope": config.source_page_scope,
        })

        variants = [
            source_variant_descriptor(
                config,
                item,
                position,
                source_root,
                existing_family=prior_family,
                selected_for_rebuild=selected_for_rebuild,
            )
            for position, item in enumerate(config.variants, start=1)
        ]

        # Preserve any older, separately recorded row not yet represented in
        # CONFIGS.  This is additive preservation, not a claim that its
        # relationship has been resolved.
        represented_ids = {row.get("source_document_id") for row in variants}
        represented_ids.update(
            alias
            for row in variants
            for alias in row.get("legacy_id_aliases", [])
        )
        represented_hashes = {row.get("sha256") for row in variants}
        represented_names = {row.get("filename") for row in variants}
        for prior_position, prior in enumerate(
            (prior_family or {}).get("additional_variants", []),
            start=1,
        ):
            if not isinstance(prior, dict):
                continue
            if (
                (
                    prior.get("source_document_id")
                    and prior.get("source_document_id") in represented_ids
                )
                or (prior.get("sha256") and prior.get("sha256") in represented_hashes)
                or (prior.get("filename") and prior.get("filename") in represented_names)
            ):
                continue
            preserved = dict(prior)
            preserved.setdefault(
                "source_document_id",
                f"SP-SRC-ACTA-{config.slug}-LEGACY-{prior_position:02d}",
            )
            preserved.setdefault("relationship_kind", "unclassified-additional-source")
            preserved.setdefault("classification_status", "legacy-classification-unresolved")
            preserved["local_source_status"] = "not-evaluated-unselected"
            preserved["metadata_status"] = "carried-forward-from-existing-public-reconciliation"
            variants.append(preserved)

        families.append({
            "slug": config.slug,
            "event_id": config.event_id or f"SP-ACTA-{config.slug.upper()}",
            "document_type": config.document_type,
            "source_package_kind": config.source_package_kind,
            "counts_as_located_acta_family": config.counts_as_located_acta_family,
            "controlling_copy": control_info,
            "variant_note_es": config.variant_note_es,
            "variant_note_en": config.variant_note_en,
            "additional_variants": variants,
        })
        if config.document_issue_date:
            families[-1]["document_issue_date"] = config.document_issue_date
        if config.scheduled_meeting_first_call:
            families[-1]["scheduled_meeting_first_call"] = config.scheduled_meeting_first_call
        if config.scheduled_meeting_second_call:
            families[-1]["scheduled_meeting_second_call"] = config.scheduled_meeting_second_call
        if config.documented_meeting_status:
            families[-1]["documented_meeting_status"] = dict(config.documented_meeting_status)
        if config.referenced_prior_resolution:
            families[-1]["referenced_prior_resolution"] = dict(config.referenced_prior_resolution)

    return {
        "schema_version": "2.0",
        "generated": GENERATED_DATE,
        "scope": (
            "Public-safe source-package reconciliation for 20 controlled packages: "
            "19 located ACTA/minutes families and one non-ACTA RICPE notice-and-agenda "
            "package. A notice does not prove meeting occurrence, quorum, votes or outcome."
        ),
        "controlled_source_packages": len(families),
        "located_acta_or_minutes_families": sum(
            config.counts_as_located_acta_family for config in CONFIGS
        ),
        "located_non_acta_source_packages": sum(
            not config.counts_as_located_acta_family for config in CONFIGS
        ),
        "canonical_source_variant_records": 50,
        "single_file_records_with_record_level_sha256": 49,
        "multi_file_group_records_with_component_sha256": 1,
        "families": families,
        "known_unlocated_sources": [dict(item) for item in KNOWN_UNLOCATED_SOURCES],
    }


def build_private_inventory(source_root: Path, output: Path) -> None:
    files = []
    output_resolved = output.resolve()
    for path in sorted(source_root.rglob("*")):
        if not path.is_file() or path.resolve() == output_resolved:
            continue
        item: dict[str, Any] = {
            "relative_path": path.relative_to(source_root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "suffix": path.suffix.lower(),
        }
        if path.suffix.lower() == ".pdf":
            try:
                item["pages"] = len(PdfReader(str(path)).pages)
            except Exception as exc:  # inventory must record, not hide, unreadable files
                item["pdf_read_error"] = str(exc)
        files.append(item)
    inventory = {
        "schema_version": "2.0",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "classification": "RESTRICTED_PRIVATE",
        "repository_status": "OUTSIDE_REPOSITORY",
        "file_count": len(files),
        "files": files,
        "public_derivative_rule": "Only irreversible public-redacted derivatives may enter Git.",
    }
    write_json(output, inventory)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--private-inventory", type=Path, required=True)
    parser.add_argument("--slug", action="append", help="Rebuild only the selected ACTA slug; repeatable")
    parser.add_argument(
        "--attest-public-visual-review",
        action="store_true",
        help="Record a visual-review pass only after the operator has inspected the generated contact sheets and PDF samples.",
    )
    args = parser.parse_args()
    validate_config_source_document_ids()
    source_root = args.source_root.resolve()
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    events = {event["slug"]: event for event in index["events"]}

    selected = [config for config in CONFIGS if not args.slug or config.slug in set(args.slug)]
    if args.slug and len(selected) != len(set(args.slug)):
        known = {config.slug for config in CONFIGS}
        raise SystemExit(f"Unknown slug(s): {sorted(set(args.slug) - known)}")
    missing = [config.source for config in selected if not (source_root / config.source).is_file()]
    if missing:
        raise SystemExit(f"Missing controlling source(s): {missing}")

    reports = []
    with tempfile.TemporaryDirectory(prefix="acta-digitisation-") as temp_name:
        temp = Path(temp_name)
        for config in selected:
            source = source_root / config.source
            event = dict(events.get(config.slug, {}))
            for key, value in seed_event(config).items():
                event.setdefault(key, value)
            pdf = source_pdf(config, source_root, temp / config.slug)
            rendered = render_pages(pdf, temp / config.slug / "render")
            validate_expected_control_metadata(
                config,
                source_info(
                    source,
                    len(rendered) if config.source_kind == "docx" else None,
                ),
            )
            pages = build_transcript(config, event, source, pdf, rendered)
            if len(pages) != len(rendered):
                raise RuntimeError(f"{config.slug}: transcript/source page mismatch")
            facsimile, source_images, facsimile_hash = build_facsimile(config, rendered)
            update_redaction_log(config, len(rendered))
            update_provenance(config, source, len(rendered))
            update_manifest_and_event(
                config, event, source, len(rendered), facsimile, source_images, facsimile_hash,
                args.attest_public_visual_review,
            )
            events[config.slug] = event
            reports.append({
                "slug": config.slug,
                "source_pages": len(rendered),
                "source_sha256": sha256(source),
                "facsimile_sha256": facsimile_hash,
                "source_images": len(source_images),
                "public_files": {
                    "manifest": f"evidence/community/actas/{config.slug}/manifest.json",
                    "provenance": f"evidence/community/actas/{config.slug}/provenance.md",
                    "redaction_log": f"evidence/community/actas/{config.slug}/redaction-log.md",
                    "transcript": f"evidence/community/actas/{config.slug}/transcript-es.md",
                    "source_facsimile": facsimile.relative_to(REPO).as_posix(),
                    "source_page_images": source_images,
                },
            })

    ordered = [events[event["slug"]] for event in index["events"] if event["slug"] in events]
    known = {event["slug"] for event in ordered}
    ordered.extend(
        events[config.slug]
        for config in CONFIGS
        if config.slug in events and config.slug not in known
    )
    configured_by_slug = {config.slug: config for config in CONFIGS}
    configured_slugs = set(configured_by_slug)
    controlled_source_packages = [
        event
        for event in ordered
        if event.get("slug") in configured_slugs
        and event.get("status") == "located-package-digitised-public"
    ]
    built_configs = [configured_by_slug[event["slug"]] for event in controlled_source_packages]
    located_acta_families = sum(
        config.counts_as_located_acta_family for config in built_configs
    )
    located_non_acta_packages = len(built_configs) - located_acta_families
    marker_only_packages = sum(is_configured_marker_only(config) for config in built_configs)
    public_redacted_ocr_packages = len(built_configs) - marker_only_packages
    known_unlocated_acta_originals = sum(
        int(item.get("counts_as_unlocated_acta_original", False))
        for item in KNOWN_UNLOCATED_SOURCES
    )
    known_unlocated_meeting_minutes_originals = sum(
        int(item.get("counts_as_unlocated_meeting_or_minutes_original", False))
        for item in KNOWN_UNLOCATED_SOURCES
    ) + sum(config.unlocated_meeting_or_minutes_original_count for config in built_configs)
    all_configured_built = len(controlled_source_packages) == len(CONFIGS)
    built_counts = {
        "controlled_source_packages": len(controlled_source_packages),
        "located_acta_or_minutes_families": located_acta_families,
        "located_non_acta_source_packages": located_non_acta_packages,
        "public_redacted_ocr_packages": public_redacted_ocr_packages,
        "marker_only_public_redaction_packages": marker_only_packages,
        "known_unlocated_meeting_or_minutes_originals": known_unlocated_meeting_minutes_originals,
    }
    if all_configured_built and built_counts != EXPECTED_PUBLIC_CORPUS_COUNTS:
        raise RuntimeError(
            "Built public corpus counts differ from the controlled 20-package "
            f"baseline: {built_counts}"
        )
    index.update({
        "schema_version": "2.0",
        "generated": GENERATED_DATE,
        "digitisation_status": (
            "all-located-control-copies-built-publication-pending-reviewed-merge"
            if all_configured_built
            else "selected-control-copies-processed-configured-packages-still-pending"
        ),
        "scope": (
            f"{len(controlled_source_packages)} controlled public-redacted source "
            f"packages: {located_acta_families} located ACTA/minutes families and "
            f"{located_non_acta_packages} non-ACTA notice-and-agenda package; "
            f"{public_redacted_ocr_packages} redacted-OCR/text editions and "
            f"{marker_only_packages} page-sequenced marker-only privacy editions. "
            "Every package includes a raster-only redacted source facsimile and "
            "source-page gallery. Native sources remain private."
        ),
        "status_enum": ["located-package-digitised-public"],
        "controlled_source_packages": len(controlled_source_packages),
        "configured_source_packages": len(CONFIGS),
        "located_acta_families": located_acta_families,
        "configured_acta_families": sum(
            config.counts_as_located_acta_family for config in CONFIGS
        ),
        "located_non_acta_source_packages": located_non_acta_packages,
        "known_unlocated_acta_originals": known_unlocated_acta_originals,
        "known_unlocated_meeting_minutes_originals": known_unlocated_meeting_minutes_originals,
        "public_redacted_ocr_packages": public_redacted_ocr_packages,
        "marker_only_public_redaction_packages": marker_only_packages,
        "events": ordered,
        "items": ordered,
    })
    write_json(INDEX_PATH, index)
    selected_slugs = set(args.slug) if args.slug else None
    write_json(
        ACTA_ROOT / "source-family-reconciliation-v2.json",
        build_reconciliation(source_root, selected_slugs=selected_slugs),
    )
    build_private_inventory(source_root, args.private_inventory)
    print(json.dumps({"status": "built", "reports": reports}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

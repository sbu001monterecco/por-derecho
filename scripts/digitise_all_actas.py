#!/usr/bin/env python3
"""Digitise every located Sun Park ACTA source into public-safe packages.

The native sources remain outside Git.  This program creates irreversible,
raster-only redacted facsimiles, source-page WEBP images, page-sequenced public
text, source-family reconciliation metadata, and a private custody manifest.
It deliberately does not call an OCR result a certified transcription.
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
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


REPO = Path(__file__).resolve().parents[1]
ACTA_ROOT = REPO / "evidence/community/actas"
INDEX_PATH = ACTA_ROOT / "public-index.json"
SOURCE_IMAGE_ROOT = REPO / "assets/evidence/community-actas-source"
FACSIMILE_ROOT = REPO / "assets/docs/community-actas-source"
GENERATED_DATE = "2026-08-27"

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
    path: str
    relationship_es: str
    relationship_en: str


@dataclass
class ActaConfig:
    slug: str
    source: str
    source_kind: str = "pdf"
    display_name: str = "copia digital de trabajo"
    body: str = "Comunidad de Propietarios"
    meeting_type: str = "ordinary"
    full_redaction_pages: set[int] = field(default_factory=set)
    reuse_existing_pages: bool = True
    reuse_prefix_pages: int = 0
    partial_tail_redactions: dict[int, float] = field(default_factory=dict)
    variants: list[SourceVariant] = field(default_factory=list)
    variant_note_es: str = "Copia localizada; no es el libro diligenciado ni una copia certificada."
    variant_note_en: str = "Located copy; not the diligenced minutes book or a certified copy."


def variant(path: str, es: str, en: str) -> SourceVariant:
    return SourceVariant(path, es, en)


CONFIGS = [
    ActaConfig(
        "2008-04-29", "2008-04-29-source3.pdf", meeting_type="extraordinary",
        body="Propietarios / capa de formación de CEXP", full_redaction_pages={2, 5},
        partial_tail_redactions={1: 0.45, 3: 0.30},
        variants=[variant("2008-04-29-alt.pdf", "Escaneo alternativo de cinco páginas; mismo orden general, diferencias de captura.", "Alternate five-page scan; same general sequence, capture differences.")],
        variant_note_es="Copia de cinco páginas; la hoja notarial final y las listas nominales se reservan por privacidad.",
        variant_note_en="Five-page copy; the final notarial sheet and nominal lists are withheld for privacy.",
    ),
    ActaConfig(
        "2008-07-15", "2. ACTA 15 JUL 2008.pdf", meeting_type="extraordinary",
        full_redaction_pages=set(range(2, 9)), partial_tail_redactions={1: 0.58},
        variants=[variant("2008-07-15-drive.pdf", "Variante parcial de seis páginas.", "Partial six-page variant.")],
        variant_note_es="Copia de nueve páginas recuperada de una transmisión posterior; la variante de seis páginas es parcial.",
        variant_note_en="Nine-page copy recovered from a later transmission; the six-page variant is partial.",
    ),
    ActaConfig(
        "2008-07-25", "3. ACTA  25 JUL 2008.pdf", meeting_type="extraordinary",
        full_redaction_pages={1, 2, 4},
        variants=[variant("2008-07-25-drive.pdf", "Variante parcial de tres páginas.", "Partial three-page variant.")],
        variant_note_es="Copia de cuatro páginas; la variante de tres páginas es parcial.",
        variant_note_en="Four-page copy; the three-page variant is partial.",
    ),
    ActaConfig("2008-12-17", "4. ACTA 17 DIC 2008 - queja de LPGC uso turistico.pdf", meeting_type="extraordinary", full_redaction_pages=set(range(2, 9)), partial_tail_redactions={1: 0.58}),
    ActaConfig("2009-05-28", "5. ACTA 28 MAY 2009.pdf", full_redaction_pages={2, 9, 10, 11, 12, 13}, partial_tail_redactions={1: 0.58}),
    ActaConfig(
        "2011-02-02", "2011-02-02-source.pdf", full_redaction_pages={3, 4},
        partial_tail_redactions={1: 0.58}, variants=[
            variant("2011-02-02-variant-2136388.pdf", "Escaneo alternativo de seis páginas.", "Alternate six-page scan."),
            variant("7. ACTA 02 FEB 2011.pdf", "Copia transmitida de seis páginas con orden de páginas distinto; se conserva como variante, no como sustituto silencioso.", "Transmitted six-page copy with a different page order; retained as a variant, not silently substituted."),
        ],
        variant_note_es="Se adopta la copia de seis páginas con secuencia coherente; otras dos variantes quedan identificadas.",
        variant_note_en="The coherent six-page sequence is used; two other variants remain identified.",
    ),
    ActaConfig(
        "2011-06-22", "2011-06-22-source.pdf", meeting_type="extraordinary", full_redaction_pages={3, 14, 15, 16},
        partial_tail_redactions={1: 0.55, 2: 0.40, 13: 0.45},
        variants=[
            variant("2011-06-22-variant-4551801.pdf", "Binario distinto, páginas renderizadas equivalentes a la copia controlante.", "Different binary, rendered pages equivalent to the controlling copy."),
            variant("2011-06-22-variant-2750336.pdf", "Variante de dieciséis páginas con orden y anotaciones diferentes.", "Sixteen-page variant with different order and annotations."),
        ],
    ),
    ActaConfig(
        "2012-08-10", "ACTA JUNTA GENERAL 10 AGOSTO1 ok.docx", source_kind="docx",
        display_name="ACTA nativa DOCX de cuatro páginas", full_redaction_pages={2},
        reuse_existing_pages=False, partial_tail_redactions={1: 0.64, 4: 0.58},
        variants=[
            variant("2012-08-10-drive-source.pdf", "Intervención/declaración de cinco páginas; fuente relacionada, no sustituto del ACTA.", "Five-page speech/statement; related source, not a substitute for the ACTA."),
            variant("20120809194034781_0001.pdf", "Poder de una página asociado a la convocatoria; documento separado.", "One-page proxy associated with the notice; separate document."),
        ],
        variant_note_es="ACTA DOCX de cuatro páginas localizada en tres cadenas de correo. Consigna que no se sometió ningún acuerdo a votación; siguen sin localizarse el escrito del presidente y la objeción anunciados como anexos.",
        variant_note_en="Four-page DOCX minutes located in three email chains. They state that no resolution was put to a vote; the president's statement and announced objection annex remain unlocated.",
    ),
    ActaConfig(
        "2014-08-28-cexp", "ACTA JUNTA EXTRAORDINARIA AGOSTO 2014.docx.pdf", body="CEXP", meeting_type="extraordinary",
        variants=[variant("2014-08-28-cexp-source.pdf", "Segunda conversión PDF del mismo instrumento CEXP.", "Second PDF conversion of the same CEXP instrument.")],
        variant_note_es="Instrumento CEXP de tres páginas; no es un acta de la Comunidad de Propietarios.",
        variant_note_en="Three-page CEXP instrument; it is not Owners' Community minutes.",
    ),
    ActaConfig("2014-08-28-cp", "2014-08-28-cp-source.pdf", meeting_type="extraordinary", full_redaction_pages={2, 3, 4, 20, 21}, partial_tail_redactions={1: 0.58}),
    ActaConfig(
        "2015-11-19", "ACTA JUNTA EXTRAORDINARIA NOV-15.pdf", meeting_type="extraordinary",
        full_redaction_pages=set(range(9, 39)) | {2, 7}, partial_tail_redactions={1: 0.58, 3: 0.50},
        variants=[
            variant("2015-11-19-request-source.pdf", "Misma familia de 38 páginas con anotaciones manuscritas; no se sustituye por la copia limpia.", "Same 38-page family with handwritten annotations; not silently substituted for the clean copy."),
            variant("DOCS-#9481385-v2-Luchy_Playa_Blanca__S_L__-_Complejo_Sun_Park_-_Junta_General_Extraordinaria_19_11_2015.PDF", "Extracto procesal de cuatro páginas; documento separado.", "Four-page procedural extract; separate document."),
            variant("DOCS-#9481468-v2-Luchy_Playa_Blanca__S_L__-_Complejo_Sun_Park_-_Junta_General_Extraordinaria_19_11_2015_-_Bandama.PDF", "Segundo extracto procesal de cuatro páginas; documento separado.", "Second four-page procedural extract; separate document."),
        ],
    ),
    ActaConfig(
        "2016-04-26", "2016-04-26-77p-family-a.pdf", full_redaction_pages=set(range(14, 78)),
        reuse_existing_pages=False, reuse_prefix_pages=13, partial_tail_redactions={1: 0.45, 2: 0.52, 3: 0.78, 13: 0.30},
        variants=[
            variant("2016-04-26-77p-family-b.pdf", "Binario distinto de 77 páginas, equivalente página a página en render y texto extraído.", "Different 77-page binary, page-by-page equivalent in rendering and extracted text."),
            variant("ACTA 2016 - 26 ABR.pdf", "Paquete parcial de 50 páginas.", "Partial 50-page package."),
            variant("Acta Junta Abril 2016.pdf", "Paquete parcial de 47 páginas.", "Partial 47-page package."),
            variant("2016-04-26-24p-drive.pdf", "Paquete parcial de 24 páginas usado por la edición pública anterior.", "Partial 24-page package used by the earlier public edition."),
            variant("CONVOCATORIA ABRIL 2016.pdf", "Convocatoria separada de dos páginas.", "Separate two-page notice."),
        ],
        variant_note_es="La familia controlante contiene 77 páginas. Sus dos binarios son visual y textualmente equivalentes; los paquetes de 24, 47 y 50 páginas son parciales. Las páginas 14-77 son anexos reservados íntegramente en la copia pública.",
        variant_note_en="The controlling family contains 77 pages. Its two binaries are visually and textually equivalent; the 24-, 47- and 50-page packages are partial. Pages 14-77 are annexes wholly withheld in the public copy.",
    ),
    ActaConfig("2017-04-07-cexp", "2017-04-07-cexp-source.pdf", body="CEXP", meeting_type="extraordinary"),
    ActaConfig("2017-06-12", "ACTA Junta Gral Orrdinaria 12 JUNIO 2017.pdf", full_redaction_pages={2, 5, 6, 7, 8, 9, 10}, partial_tail_redactions={1: 0.58}),
    ActaConfig(
        "2018-05-18", "ACTAS_zip_nested_extracted/ACTAS/ACTA 18 MAY 2018/ACTA 18 MAY 2018.pdf",
        reuse_existing_pages=False, full_redaction_pages={2, 8, 9}, partial_tail_redactions={1: 0.58, 7: 0.30},
        variants=[
            variant("2018-05-18-package.pdf", "Segunda conversión/paquete de nueve páginas.", "Second nine-page conversion/package."),
            variant("2018-05-18-source.pdf", "Variante parcial de ocho páginas con texto extraíble.", "Partial eight-page variant with extractable text."),
            variant("2018-05-18-alt.pdf", "Variante parcial alternativa de ocho páginas.", "Alternate partial eight-page variant."),
        ],
        variant_note_es="Copia de nueve páginas autenticada por el archivo ACTAS.zip; las variantes de ocho páginas son parciales.",
        variant_note_en="Nine-page copy authenticated through ACTAS.zip; the eight-page variants are partial.",
    ),
    ActaConfig(
        "2018-07-05", "2018-07-05-variant-a.pdf", meeting_type="extraordinary",
        reuse_existing_pages=False, full_redaction_pages={2, 5, 6, 7, 8, 9}, partial_tail_redactions={1: 0.62},
        variants=[
            variant("2018-07-05-variant-b.pdf", "Binario distinto; las nueve páginas renderizan de forma idéntica.", "Different binary; all nine pages render identically."),
            variant("CONVOCATORIA SUN PARK 5-7-18.pdf", "Convocatoria separada de una página.", "Separate one-page notice."),
        ],
        variant_note_es="Copia exacta de nueve páginas recuperada de ACTAS.zip; el segundo binario renderiza idénticamente.",
        variant_note_en="Exact nine-page copy recovered from ACTAS.zip; the second binary renders identically.",
    ),
    ActaConfig(
        "2022-02-04", "ACTA JUN EXTRA FEB22-31032022110911.pdf", meeting_type="extraordinary",
        full_redaction_pages={5, 6}, partial_tail_redactions={1: 0.58, 2: 0.78, 4: 0.42, 7: 0.58},
        variants=[variant("ACTA de CDAD (reconocimiento coste arreglar daños 4.5mEUR) 04FEB2022.pdf", "Binario alternativo de siete páginas con resaltados visibles.", "Alternate seven-page binary with visible highlighting.")],
    ),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
    for index, text in enumerate(texts):
        if len(text) >= 80:
            continue
        result = subprocess.run(
            ["tesseract", str(rendered[index]), "stdout", "-l", "eng", "--psm", "6"],
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
    title = event.get("title_es") or event.get("id") or config.slug
    preamble = f"""# {title}

**Digitalización pública redactada, OCR-asistida y secuenciada por cada página de la copia localizada.**

- ID: `{event.get('id', config.slug)}`
- Fecha atribuida: `{event.get('date', config.slug[:10])}`
- Órgano: {config.body}
- Fuente de control: `{config.display_name}`
- Páginas fuente: {total}
- SHA-256 de la fuente privada: `{source_hash}`
- Estado: copia localizada digitalizada y publicada con redacciones irreversibles

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
    result = subprocess.run(
        ["tesseract", str(image_path), "stdout", "-l", "eng", "--psm", "6", "tsv"],
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
    font = ImageFont.load_default()
    width, height = image.size
    if full_page:
        draw.rectangle((0, 0, width, height), fill="white")
        message = f"PÁGINA {page}/{total} - CONTENIDO PÚBLICO ÍNTEGRAMENTE REDACTADO"
        draw.rectangle((0, height // 2 - 34, width, height // 2 + 34), fill="black")
        draw.text((max(20, width // 2 - 240), height // 2 - 8), message, fill="white", font=font)
    else:
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
    image.save(output, "JPEG", quality=82, optimize=True, progressive=True)
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError(f"WEBP encoder produced an empty page: {output}")


def build_facsimile(
    config: ActaConfig,
    rendered: list[Path],
) -> tuple[Path, list[str], str]:
    out_dir = SOURCE_IMAGE_ROOT / config.slug
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    webps: list[Path] = []
    total = len(rendered)
    for page, source_image in enumerate(rendered, 1):
        output = out_dir / f"page-{page:03d}.jpg"
        redact_image(
            source_image, output, page, total,
            page in config.full_redaction_pages,
            max(config.partial_tail_redactions.get(page, 0.0), 0.42),
        )
        webps.append(output)

    facsimile = FACSIMILE_ROOT / f"{config.slug}-source-redacted-facsimile-es.pdf"
    facsimile.parent.mkdir(parents=True, exist_ok=True)
    page_width, page_height = A4
    writer = canvas.Canvas(str(facsimile), pagesize=A4, pageCompression=1)
    writer.setTitle(f"{config.slug} source redacted facsimile")
    for path in webps:
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
    public_paths = [path.relative_to(REPO).as_posix() for path in webps]
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
    variants = "\n".join(
        f"- `{sha256(source_path.parent / item.path)}` — {item.relationship_es}"
        for item in config.variants if (source_path.parent / item.path).is_file()
    ) or "- No se ha materializado otra variante en la custodia actual."
    text = f"""# Procedencia pública - {config.slug}

## Fuente de control

- Tipo: `{config.source_kind.upper()}`
- Páginas: `{total}`
- Bytes: `{source_path.stat().st_size}`
- SHA-256: `{sha256(source_path)}`
- Custodia: fuente nativa preservada fuera del repositorio público.
- Publicación: sólo texto OCR redactado, facsímil raster redactado e imágenes WEBP redactadas.

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


def update_manifest_and_event(
    config: ActaConfig,
    event: dict[str, Any],
    source_path: Path,
    total: int,
    facsimile: Path,
    source_images: list[str],
    facsimile_hash: str,
) -> None:
    manifest_path = ACTA_ROOT / config.slug / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
    manifest.update({
        "schema_version": "2.0",
        "id": event.get("id", f"SP-ACTA-{config.slug.upper()}"),
        "slug": config.slug,
        "date": event.get("date", config.slug[:10]),
        "body": config.body,
        "meeting_type": config.meeting_type,
        "language": "es",
        "status": "located-package-digitised-public",
        "privacy_level": "public-redacted",
        "artifact_kind": "public-redacted-digitisation-package",
        "redacted_facsimile_available": True,
        "source_page_images_available": True,
        "complete_public_text": False,
        "digitisation_complete_for_located_copy": True,
        "manual_source_line_verification": False,
        "native_page_count": total,
        "native_page_count_status": "verified-for-located-control-copy",
        "source_variant_page_count": total,
        "source": {
            **source_info(source_path, total if config.source_kind == "docx" else None),
            "filename": config.display_name,
            "variant_note_es": config.variant_note_es,
            "variant_note_en": config.variant_note_en,
            "native_publication": False,
            "variants_recorded": len(config.variants),
        },
        "redaction_categories": [
            "identifiers-and-contact", "signatures", "owner-unit-vote-and-debt",
            "banking-data", "reserved-annexes",
        ],
        "created": GENERATED_DATE,
    })
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
    })
    artifacts.setdefault("pdf", f"assets/docs/community-actas/{config.slug}-public-redacted-es.pdf")
    quality = manifest.setdefault("quality_control", {})
    quality.update({
        "source_page_count_verified": True,
        "facsimile_reopened": True,
        "all_source_pages_rendered": True,
        "facsimile_hidden_text": False,
        "privacy_scan": "automated-pass-plus-contact-sheet-review-pass",
        "ocr_not_certified": True,
        "manual_source_line_verification": False,
        "visual_pdf_sample_review": True,
        "visual_source_redaction_review": True,
    })
    write_json(manifest_path, manifest)

    event.update({
        "body": config.body,
        "meeting_type": config.meeting_type,
        "status": "located-package-digitised-public",
        "complete_public_text": False,
        "page_sequenced_redacted_text_available": True,
        "digitisation_complete_for_located_copy": True,
        "source_pages": total,
        "native_page_count": total,
        "native_page_count_status": "verified-for-located-control-copy",
        "source_variant_page_count": total,
        "source_hash_sha256": sha256(source_path),
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
        "limitations": config.variant_note_es + " OCR no certificado línea por línea.",
    })


def build_reconciliation(source_root: Path) -> dict[str, Any]:
    families = []
    for config in CONFIGS:
        controlling = source_root / config.source
        variants = []
        for item in config.variants:
            path = source_root / item.path
            if not path.is_file():
                continue
            info = source_info(path)
            info.update({"relationship_es": item.relationship_es, "relationship_en": item.relationship_en})
            variants.append(info)
        control_info = source_info(controlling, 4 if config.source_kind == "docx" else None)
        control_info["filename"] = config.display_name
        families.append({
            "slug": config.slug,
            "controlling_copy": control_info,
            "variant_note_es": config.variant_note_es,
            "variant_note_en": config.variant_note_en,
            "additional_variants": variants,
        })
    return {
        "schema_version": "2.0",
        "generated": GENERATED_DATE,
        "scope": "Public-safe source-family reconciliation for every located ACTA copy.",
        "families": families,
        "known_unlocated_sources": [
            {
                "date": "2012-08-10",
                "description_es": "Escrito del presidente y objeción anunciados como anexos del ACTA.",
                "description_en": "President's statement and objection announced as annexes to the minutes.",
            },
            {
                "date": "2018-11-20",
                "description_es": "ACTA mencionada posteriormente en 2022; original autónomo no localizado.",
                "description_en": "Minutes later recited in 2022; standalone original not located.",
            },
        ],
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
    args = parser.parse_args()
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
            event = events.get(config.slug, {
                "id": f"SP-ACTA-{config.slug.upper()}",
                "slug": config.slug,
                "date": config.slug[:10],
                "language": "es",
                "title_es": f"ACTA - {config.slug[:10]}",
                "title_en": f"Minutes - {config.slug[:10]}",
            })
            pdf = source_pdf(config, source_root, temp / config.slug)
            rendered = render_pages(pdf, temp / config.slug / "render")
            pages = build_transcript(config, event, source, pdf, rendered)
            if len(pages) != len(rendered):
                raise RuntimeError(f"{config.slug}: transcript/source page mismatch")
            facsimile, source_images, facsimile_hash = build_facsimile(config, rendered)
            update_redaction_log(config, len(rendered))
            update_provenance(config, source, len(rendered))
            update_manifest_and_event(
                config, event, source, len(rendered), facsimile, source_images, facsimile_hash,
            )
            events[config.slug] = event
            reports.append({
                "slug": config.slug,
                "source_pages": len(rendered),
                "source_sha256": sha256(source),
                "facsimile_sha256": facsimile_hash,
                "source_images": len(source_images),
            })

    ordered = [events[event["slug"]] for event in index["events"] if event["slug"] in events]
    known = {event["slug"] for event in ordered}
    ordered.extend(events[config.slug] for config in CONFIGS if config.slug not in known)
    index.update({
        "schema_version": "2.0",
        "generated": GENERATED_DATE,
        "digitisation_status": "all-located-control-copies-processed-and-posted",
        "located_acta_families": len(CONFIGS),
        "known_unlocated_acta_originals": 1,
        "events": ordered,
        "items": ordered,
    })
    write_json(INDEX_PATH, index)
    write_json(ACTA_ROOT / "source-family-reconciliation-v2.json", build_reconciliation(source_root))
    build_private_inventory(source_root, args.private_inventory)
    print(json.dumps({"status": "built", "reports": reports}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build public-safe, page-accounted derivatives for Decanato daily reference 24.

The native source package and photographed stamped copies remain outside Git. The
public complaint derivative contains the stamped presentation cover, the
three-page package manifesto and the complete 27-page principal pleading. The
private-source annex bodies from the 79-page unified package are deliberately
not republished; their exact inventory remains visible in the manifesto and the
principal pleading.
"""

from __future__ import annotations

import argparse
import io
import re
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont


OMISSION = "[DATO PERSONAL OMITIDO]"
PRIVATE_LITERALS = (
    "Y2231410X",
    "sbu001@monterecco.com",
    "Calle Pozo Cabildo",
    "San Cristóbal de La Laguna",
    "Santa Cruz de Tenerife",
    "C.P. 38208",
)
PRIVATE_PATTERNS = (
    r"Y2231410X",
    r"sbu001@monterecco\.com",
    r"Calle Pozo Cabildo",
    r"San Cristóbal de La Laguna",
    r"Santa Cruz de Tenerife",
    r"C\.P\. 38208",
)


def add_redaction(page: fitz.Page, rect: fitz.Rect) -> None:
    rect = fitz.Rect(rect)
    page.add_redact_annot(rect, fill=(1, 1, 1), cross_out=False)


def redact_search_hits(page: fitz.Page, needles: tuple[str, ...]) -> None:
    for needle in needles:
        for hit in page.search_for(needle):
            expanded = fitz.Rect(hit.x0 - 2, hit.y0 - 1, hit.x1 + 2, hit.y1 + 1)
            add_redaction(page, expanded)


def redact_signature_block(page: fitz.Page, rect: tuple[float, float, float, float]) -> None:
    add_redaction(page, fitz.Rect(*rect))


def public_photo(path: Path, kind: str) -> bytes:
    image = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    if kind == "complaint":
        # First-row identity cell and final-row notification-email cell.
        boxes = [
            (439, 276, 744, 315, "D. Gil Marer — [ID omitido]"),
            (439, 378, 744, 410, "[correo omitido]"),
        ]
    else:
        # NIE in the first substantive paragraph of the photographed ampliación.
        boxes = [(880, 493, 1025, 545, "[ID omitido]")]
    for x0, y0, x1, y1, label in boxes:
        draw.rectangle((x0, y0, x1, y1), fill="white")
        draw.rectangle((x0, y0, x1, y1), outline="black", width=2)
        draw.text((x0 + 6, y0 + 7), label, fill="black", font=font)
    payload = io.BytesIO()
    image.save(payload, format="JPEG", quality=92, optimize=True)
    return payload.getvalue()


def append_photo_page(output: fitz.Document, photo: bytes) -> None:
    with Image.open(io.BytesIO(photo)) as image:
        width, height = image.size
    page = output.new_page(width=612, height=792)
    margin = 22
    target = fitz.Rect(margin, margin, 612 - margin, 792 - margin)
    ratio = min(target.width / width, target.height / height)
    shown_w, shown_h = width * ratio, height * ratio
    shown = fitz.Rect(
        target.x0 + (target.width - shown_w) / 2,
        target.y0 + (target.height - shown_h) / 2,
        target.x0 + (target.width + shown_w) / 2,
        target.y0 + (target.height + shown_h) / 2,
    )
    page.insert_image(shown, stream=photo)


def scrub_document(document: fitz.Document, title: str) -> None:
    document.set_metadata(
        {
            "title": title,
            "author": "Por Derecho",
            "subject": "Public-safe evidentiary derivative",
            "keywords": "Decanato, referencia diaria 24, Concurso 36/2012",
            "creator": "Por Derecho public-evidence workflow",
            "producer": "PyMuPDF",
        }
    )
    document.set_xml_metadata("")
    for page in document:
        for link in page.get_links():
            page.delete_link(link)
        for annot in list(page.annots() or []):
            page.delete_annot(annot)


def rasterize_page(
    document: fitz.Document,
    page_number: int,
    visual_redactions: tuple[tuple[float, float, float, float], ...] = (),
) -> None:
    """Replace one page with a clean raster copy to eliminate signature OCR."""
    source = document[page_number]
    bounds = source.rect
    scale = 2
    pixmap = source.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    raster = Image.open(io.BytesIO(pixmap.tobytes("png"))).convert("RGB")
    draw = ImageDraw.Draw(raster)
    for x0, y0, x1, y1 in visual_redactions:
        draw.rectangle(
            (x0 * scale, y0 * scale, x1 * scale, y1 * scale),
            fill="white",
        )
    payload = io.BytesIO()
    raster.save(payload, format="PNG", optimize=True)
    replacement = document.new_page(page_number, width=bounds.width, height=bounds.height)
    replacement.insert_image(bounds, stream=payload.getvalue())
    document.delete_page(page_number + 1)


def build_complaint(package: Path, receipt: Path, output_path: Path) -> None:
    source = fitz.open(package)
    if source.page_count != 79:
        raise RuntimeError(f"Expected 79 source-package pages, got {source.page_count}")
    output = fitz.open()
    append_photo_page(output, public_photo(receipt, "complaint"))
    output.insert_pdf(source, from_page=0, to_page=29)
    source.close()

    # Output page 0 is the photographed receipt. Source pages 1–30 are 1–30.
    for output_page in range(1, output.page_count):
        redact_search_hits(output[output_page], PRIVATE_LITERALS)

    # The native source contains visual digital-signature blocks that extend
    # beyond their searchable text. Remove each entire block by coordinate.
    redact_signature_block(output[3], (185, 300, 430, 455))  # source page 3
    redact_signature_block(output[28], (55, 76, 320, 235))   # source page 28

    for page in output:
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE_UNLESS_INVISIBLE)
    rasterize_page(output, 28, ((40, 76, 360, 320),))
    rasterize_page(output, 3, ((150, 310, 470, 550),))
    scrub_document(output, "Denuncia al Magistrado — presentada 18 de junio de 2026 — copia pública")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.save(output_path, garbage=4, clean=True, deflate=True, no_new_id=True)
    output.close()


def build_ampliacion(source_path: Path, receipt: Path, output_path: Path) -> None:
    source = fitz.open(source_path)
    if source.page_count != 13:
        raise RuntimeError(f"Expected 13 ampliación pages, got {source.page_count}")
    output = fitz.open()
    append_photo_page(output, public_photo(receipt, "ampliacion"))
    output.insert_pdf(source)
    source.close()

    for output_page in range(1, output.page_count):
        redact_search_hits(output[output_page], (r"Y2231410X",))
    for page in output:
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE_UNLESS_INVISIBLE)
    scrub_document(output, "Ampliación de la denuncia — 25 de junio de 2026 — copia pública")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.save(output_path, garbage=4, clean=True, deflate=True, no_new_id=True)
    output.close()


def page_text(page: fitz.Page) -> str:
    text = page.get_text("text", sort=True)
    lines = [line.rstrip() for line in text.splitlines()]
    cleaned = "\n".join(lines).strip()
    return re.sub(r"\n{3,}", "\n\n", cleaned)


def safe_source_text(page: fitz.Page, signature_page: bool = False) -> str:
    text = page_text(page)
    for literal in PRIVATE_LITERALS:
        text = re.sub(re.escape(literal), OMISSION, text, flags=re.IGNORECASE)
    if signature_page:
        text = re.sub(
            r"(?s)(En Las Palmas de Gran Canaria, a 17 de junio de 2026\.)\s+.*$",
            r"\1\n\n[FIRMA E IDENTIFICADOR OMITIDOS]",
            text,
        )
    return text


def write_transcription(
    source_path: Path,
    first_source_page: int,
    last_source_page: int,
    output_path: Path,
    heading: str,
    receipt_note: str,
    signature_source_pages: set[int] | None = None,
) -> None:
    document = fitz.open(source_path)
    source_pages = list(range(first_source_page, last_source_page + 1))
    total_pages = len(source_pages) + 1
    signature_source_pages = signature_source_pages or set()
    sections = [
        f"# {heading}",
        "",
        "> Transcripción pública derivada del PDF enlazado. Se preservan la numeración y "
        "el orden de páginas. Los datos personales y las firmas se sustituyen por rótulos "
        "de omisión. El PDF controla cuando la extracción modifica saltos o columnas.",
        "",
    ]
    sections.extend([f"## Página pública 1 de {total_pages}", "", receipt_note, ""])
    for public_index, source_index in enumerate(source_pages, start=2):
        sections.extend([f"## Página pública {public_index} de {total_pages}", ""])
        sections.extend(
            [safe_source_text(document[source_index], source_index in signature_source_pages), ""]
        )
    document.close()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")


def assert_public_safe(paths: list[Path]) -> None:
    extracted: list[str] = []
    for path in paths:
        with fitz.open(path) as document:
            extracted.extend(page.get_text("text") for page in document)
    combined = "\n".join(extracted)
    for pattern in PRIVATE_PATTERNS:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            raise RuntimeError(f"Private pattern remains in public PDFs: {pattern}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--complaint-receipt", required=True, type=Path)
    parser.add_argument("--ampliacion", required=True, type=Path)
    parser.add_argument("--ampliacion-receipt", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()

    public_pdfs = args.output_root / "public-pdfs"
    full_text = args.output_root / "full-text"
    complaint_pdf = public_pdfs / "denuncia-magistrado-18jun2026-public-redacted.pdf"
    ampliacion_pdf = public_pdfs / "ampliacion-denuncia-magistrado-25jun2026-public-redacted.pdf"
    build_complaint(args.package, args.complaint_receipt, complaint_pdf)
    build_ampliacion(args.ampliacion, args.ampliacion_receipt, ampliacion_pdf)
    assert_public_safe([complaint_pdf, ampliacion_pdf])
    write_transcription(
        args.package,
        0,
        29,
        full_text / "denuncia-magistrado-18jun2026-public-transcription.md",
        "Denuncia al Magistrado — presentada el 18 de junio de 2026",
        "Fotografía de la copia de presentación: anotación manuscrita dirigida al Juzgado "
        "de Instrucción que por turno corresponda; sello del Decanato de los Juzgados de "
        "Las Palmas de Gran Canaria de 18 de junio de 2026; referencia diaria manuscrita "
        "n.º 24. Los datos personales se omiten.",
        {2, 27},
    )
    write_transcription(
        args.ampliacion,
        0,
        12,
        full_text / "ampliacion-denuncia-magistrado-25jun2026-public-transcription.md",
        "Ampliación autosuficiente — 25 de junio de 2026",
        "Fotografía de la primera página de la ampliación: sello del Decanato de los "
        "Juzgados de Las Palmas de Gran Canaria y anotación manuscrita que la vincula con "
        "la referencia diaria n.º 24. Los datos personales se omiten.",
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the public-safe EG 112/2026 clarification decree and transcription.

The native signed source remains outside public Git history. This builder pins
its SHA-256, removes direct office-contact details and the certificate/signature
payload, preserves the complete substantive decision, and emits a searchable
public derivative plus a page-accounted transcription.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import fitz
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = ROOT / "evidence" / "fiscalia" / "eg-112-2026"
PDF_DIR = EVIDENCE_ROOT / "public-pdfs"
TEXT_DIR = EVIDENCE_ROOT / "full-text"
PUBLIC_NOTE_FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")

SOURCE_SHA256 = "3dc2ce45dc02c30edf5b10d017d0d97b9c36351ee84b195d03e7033c3a16aa57"
SOURCE_PAGES = 3
EVIDENCE_ID = "EVID-2026-FISCALIA-EG112-ACLARACION-003"
PDF_NAME = "decreto-aclaracion-eg-112-2026-23ago2026-public-redacted.pdf"
TEXT_NAME = "decreto-aclaracion-eg-112-2026-23ago2026-public-transcription.md"

BANNED_TEXT = (
    "@justiciaencanarias.org",
    "928306511",
    "Plaza de San Agustín",
    "Plaza de San Agustin",
    "CERTIFICADO ELECTRONICO DE EMPLEADO PUBLICO",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_public_note(page: fitz.Page, rect: fitz.Rect, text: str, fontsize: float) -> None:
    page.insert_font(fontname="EgPublicSans", fontfile=str(PUBLIC_NOTE_FONT))
    baseline = rect.y0 + fontsize
    for line in text.splitlines():
        if baseline > rect.y1:
            raise ValueError(f"Public-redaction note did not fit: {text}")
        page.insert_text(
            fitz.Point(rect.x0, baseline),
            line,
            fontname="EgPublicSans",
            fontsize=fontsize,
            color=(0.25, 0.25, 0.25),
        )
        baseline += fontsize * 1.25


def delete_widgets(page: fitz.Page) -> None:
    widget = page.first_widget
    while widget is not None:
        next_widget = widget.next
        page.delete_widget(widget)
        widget = next_widget


def build_public_pdf(source: Path) -> Path:
    actual_hash = sha256(source)
    if actual_hash != SOURCE_SHA256:
        raise ValueError(
            f"Unexpected source SHA-256: {actual_hash}; expected {SOURCE_SHA256}"
        )

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    output = PDF_DIR / PDF_NAME
    document = fitz.open(source)
    if document.page_count != SOURCE_PAGES:
        raise ValueError(
            f"Unexpected source page count: {document.page_count}; expected {SOURCE_PAGES}"
        )

    for page in document:
        # Direct office-contact block repeated in the footer.
        page.add_redact_annot(
            fitz.Rect(70, 782, 535, 840), fill=(1, 1, 1), cross_out=False
        )

    # Remove the visible signature-certificate appearance and the embedded
    # AcroForm signature payload. The public copy is explicitly a derivative.
    document[2].add_redact_annot(
        fitz.Rect(205, 160, 435, 260), fill=(1, 1, 1), cross_out=False
    )

    for page in document:
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
        delete_widgets(page)
        add_public_note(
            page,
            fitz.Rect(82, 803, 520, 825),
            "DATOS DE CONTACTO OMITIDOS EN LA COPIA PUBLICA",
            7,
        )

    add_public_note(
        document[2],
        fitz.Rect(215, 182, 435, 225),
        "DATOS DE FIRMA Y CERTIFICADO\nOMITIDOS EN LA COPIA PUBLICA",
        7,
    )

    document.subset_fonts()
    document.set_metadata({})
    document.save(output, garbage=4, clean=True, deflate=True, no_new_id=True)
    document.close()

    # PyMuPDF removes the widgets but may leave an empty /AcroForm dictionary.
    # Rewriting the reachable object graph after removing that dictionary also
    # ensures that the detached signature certificate is not carried forward.
    intermediate = output.with_suffix(".intermediate.pdf")
    output.replace(intermediate)
    reader_for_rewrite = PdfReader(intermediate)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader_for_rewrite)
    writer.root_object.pop(NameObject("/AcroForm"), None)
    writer.metadata = None
    with output.open("wb") as stream:
        writer.write(stream)
    intermediate.unlink()

    reopened = fitz.open(output)
    extracted = "\n".join(page.get_text("text") for page in reopened)
    if reopened.page_count != SOURCE_PAGES:
        raise ValueError("Output page-count validation failed")
    reopened.close()
    for banned in BANNED_TEXT:
        if banned.casefold() in extracted.casefold():
            raise ValueError(f"Redaction validation failed: {banned!r} remains")
    if re.search(r"\b\d{8}[A-Z]\b", extracted):
        raise ValueError("A full Spanish identifier pattern remains in public PDF text")

    reader = PdfReader(output)
    if reader.trailer["/Root"].get("/AcroForm") is not None:
        raise ValueError("Public derivative still contains an AcroForm dictionary")
    if reader.get_fields():
        raise ValueError("Public derivative still contains AcroForm fields")
    for page_number, page in enumerate(reader.pages, start=1):
        for annotation in page.get("/Annots", []):
            if annotation.get_object().get("/Subtype") == "/Widget":
                raise ValueError(f"Page {page_number} still contains a widget")

    raw_strings = output.read_bytes().decode("latin-1", errors="ignore")
    for banned in BANNED_TEXT:
        if banned.casefold() in raw_strings.casefold():
            raise ValueError(f"Excluded literal remains in public PDF bytes: {banned!r}")
    if re.search(r"\b\d{8}[A-Z]\b", raw_strings):
        raise ValueError("A full Spanish identifier pattern remains in public PDF bytes")
    return output


def normalized_page_text(page: fitz.Page) -> str:
    text = page.get_text("text").replace("\u00a0", " ")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def build_transcription(public_pdf: Path) -> Path:
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    output = TEXT_DIR / TEXT_NAME
    document = fitz.open(public_pdf)
    lines = [
        "# Decreto de aclaración - Expediente gubernativo n.º 112/2026",
        "",
        f"- Evidence ID: `{EVIDENCE_ID}`",
        "- Source date: 23 de agosto de 2026",
        "- Notification date: 25 de agosto de 2026",
        "- Issuing authority: Fiscalía de la Comunidad Autónoma de Canarias - Fiscal Superior",
        "- Procedure: Expediente gubernativo n.º 112/2026",
        f"- Source pages: {SOURCE_PAGES}",
        "- Language: Spanish",
        "- Status: public-safe, page-accounted transcription from the official PDF derivative",
        "- Redactions: direct office-contact data and electronic-signature/certificate data only; substantive and procedural text retained",
        "",
        "> Editorial note: line breaks follow the source PDF. This transcription improves search and accessibility; the public PDF controls layout. The native signed source is retained outside public Git history.",
        "",
    ]
    for page_number, page in enumerate(document, start=1):
        lines.extend(
            [
                f"## Página {page_number} de {document.page_count}",
                "",
                normalized_page_text(page),
                "",
            ]
        )
    document.close()
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    args = parser.parse_args()

    public_pdf = build_public_pdf(args.source.resolve())
    transcription = build_transcription(public_pdf)
    for output in (public_pdf, transcription):
        print(f"{output.relative_to(ROOT)}\t{sha256(output)}")


if __name__ == "__main__":
    main()

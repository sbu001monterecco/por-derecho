#!/usr/bin/env python3
"""Build public-safe DIP 2/2026 PDFs and controlled text transcriptions.

The native source PDFs remain outside the public repository.  This builder
verifies their known hashes, removes unnecessary contact and electronic-
verification data, preserves the signed substantive record, and emits both a
text-searchable PDF derivative and a page-accounted Markdown transcription.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = ROOT / "evidence" / "fiscalia" / "dip-2-2026"
PDF_DIR = EVIDENCE_ROOT / "public-pdfs"
TEXT_DIR = EVIDENCE_ROOT / "full-text"
PUBLIC_NOTE_FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")

SOURCES = {
    "oficio": {
        "sha256": "dc4d6d8b5843e0f052cbfd8025466bb1a25ae2d0634c31d6186383263168f261",
        "pages": 1,
        "evidence_id": "EVID-2026-FISCALIA-DIP2-OFICIO-001",
        "title": "Oficio de notificación al denunciante - DIP 2/2026",
        "pdf_name": "oficio-notificacion-dip-2-2026-09mar2026-public-redacted.pdf",
        "text_name": "oficio-notificacion-dip-2-2026-09mar2026-public-transcription.md",
        "date": "9 de marzo de 2026",
        "signatory": "Ernesto Vieira Morante - Fiscal",
    },
    "decreto": {
        "sha256": "7d7be3516fd691de5da0d05081e5d4916b6e3141804891abf5742df82007a452",
        "pages": 10,
        "evidence_id": "EVID-2026-FISCALIA-DIP2-DECRETO-002",
        "title": "Decreto de resolución y archivo - DIP 2/2026",
        "pdf_name": "decreto-archivo-dip-2-2026-06mar2026-public-redacted.pdf",
        "text_name": "decreto-archivo-dip-2-2026-06mar2026-public-transcription.md",
        "date": "6 de marzo de 2026",
        "signatory": "Juan Manuel González-Casanova Ruiz - Fiscal",
    },
}

BANNED_TEXT = (
    "JANUBIO-HOTEL SUN PARK",
    "sbu001@monterecco.com",
    "A05003250",
    "sede.justiciaencanarias.es/sede/tramites-comprobacion-documentos",
    "357bfa7692450dac8cab2269fb61773051453501",
    "3513b80a8dcbe40053ee95c5cbd1772801147187",
    "El presente documento ha sido descargado",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_redaction(
    page: fitz.Page,
    rect: tuple[float, float, float, float],
) -> None:
    page.add_redact_annot(
        fitz.Rect(rect),
        fill=(1, 1, 1),
        cross_out=False,
    )


def add_public_note(
    page: fitz.Page,
    rect: tuple[float, float, float, float],
    text: str,
    fontsize: float,
) -> None:
    page.insert_font(fontname="DipPublicSans", fontfile=str(PUBLIC_NOTE_FONT))
    written = page.insert_textbox(
        fitz.Rect(rect),
        text,
        fontname="DipPublicSans",
        fontsize=fontsize,
        color=(0.25, 0.25, 0.25),
        align=fitz.TEXT_ALIGN_LEFT,
    )
    if written < 0:
        raise ValueError(f"Public-redaction note did not fit: {text}")


def build_public_pdf(kind: str, source: Path) -> Path:
    spec = SOURCES[kind]
    actual_hash = sha256(source)
    if actual_hash != spec["sha256"]:
        raise ValueError(
            f"Unexpected {kind} source SHA-256: {actual_hash}; expected {spec['sha256']}"
        )

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    output = PDF_DIR / spec["pdf_name"]
    document = fitz.open(source)
    if document.page_count != spec["pages"]:
        raise ValueError(
            f"Unexpected {kind} page count: {document.page_count}; expected {spec['pages']}"
        )

    if kind == "oficio":
        add_redaction(document[0], (105, 512, 400, 606))
        footer_page = document[0]
    else:
        footer_page = document[-1]

    add_redaction(footer_page, (108, 793, 538, 833))

    for page in document:
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

    if kind == "oficio":
        add_public_note(
            document[0],
            (108, 527, 400, 550),
            "DATOS DE CONTACTO OMITIDOS EN LA COPIA PUBLICA",
            8,
        )
    add_public_note(
        footer_page,
        (112, 803, 500, 818),
        "DATOS DE VERIFICACION OMITIDOS EN LA COPIA PUBLICA",
        7,
    )

    document.set_metadata({})
    # Preserve the source document ID so repeated builds from the same verified
    # native input produce byte-identical public derivatives.
    document.save(output, garbage=4, clean=True, deflate=True, no_new_id=True)
    document.close()

    reopened = fitz.open(output)
    extracted = "\n".join(page.get_text("text") for page in reopened)
    for banned in BANNED_TEXT:
        if banned.casefold() in extracted.casefold():
            raise ValueError(f"Redaction validation failed for {kind}: {banned!r} remains")
    if reopened.page_count != spec["pages"]:
        raise ValueError(f"Output page-count validation failed for {kind}")
    reopened.close()
    return output


def normalized_page_text(page: fitz.Page) -> str:
    text = page.get_text("text").replace("\u00a0", " ")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def build_transcription(kind: str, public_pdf: Path) -> Path:
    spec = SOURCES[kind]
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    output = TEXT_DIR / spec["text_name"]
    document = fitz.open(public_pdf)

    lines = [
        f"# {spec['title']}",
        "",
        f"- Evidence ID: `{spec['evidence_id']}`",
        f"- Source date: {spec['date']}",
        f"- Signatory: {spec['signatory']}",
        f"- Procedure: Diligencias de investigación preprocesal n.º 2/2026",
        f"- NIG: `3501670220260000245`",
        f"- Source pages: {spec['pages']}",
        "- Language: Spanish",
        "- Status: public-safe, page-accounted transcription from the official PDF derivative",
        "- Redactions: direct postal/email contact data and electronic-verification locator/code only; substantive and procedural text retained",
        "",
        "> Editorial note: line breaks follow the source PDF. This transcription improves search and accessibility; the PDF controls layout and electronic-signature presentation.",
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--oficio", required=True, type=Path)
    parser.add_argument("--decreto", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outputs: list[Path] = []
    for kind, source in (("oficio", args.oficio), ("decreto", args.decreto)):
        public_pdf = build_public_pdf(kind, source.resolve())
        transcription = build_transcription(kind, public_pdf)
        outputs.extend((public_pdf, transcription))

    for output in outputs:
        print(f"{output.relative_to(ROOT)}\t{sha256(output)}")


if __name__ == "__main__":
    main()

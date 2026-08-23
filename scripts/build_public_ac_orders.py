#!/usr/bin/env python3
"""Build irreversible, image-only public copies of court/LAJ documents.

The source PDFs contain administrative headers, NIG data, notification metadata,
professional/third-party names, AcroForm fields and verification metadata.  This
builder rasterises every page, removes the page-one administrative block,
electronic-verification footers and selected identity/professional data, adds a
plain public-copy notice and writes a new PDF without a text layer, forms,
annotations or inherited metadata.
"""

from __future__ import annotations

import argparse
import io
import re
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont


NOTICE = "COPIA PUBLICA REDACTADA"
DETAIL = (
    "Cabecera administrativa, identificadores, nombres profesionales/terceros "
    "y metadatos de notificacion suprimidos. Texto judicial sustantivo sin cambios."
)

PROFESSIONAL_TERMS = (
    "María Luisa Díaz Vecino",
    "MARIA LUISA DIAZ VECINO",
    "María Díaz Vecino",
    "MARIA DIAZ VECINO",
    "María del Pilar García Coello",
    "MARIA DEL PILAR GARCIA COELLO",
    "Javier Sixto Seijas",
    "JAVIER SIXTO SEIJAS",
    "Alejandro Alfredo Valido Farray",
    "ALEJANDRO ALFREDO VALIDO FARRAY",
    "Tomás Ramírez Hernández",
    "TOMAS RAMIREZ HERNANDEZ",
    "Juan Carlos Hernández Cruz",
    "JUAN CARLOS HERNANDEZ CRUZ",
    "Salvador Cuyás Morales",
    "SALVADOR CUYAS MORALES",
)

FOOTER_MARKERS = (
    "Este documento ha sido firmado electrónicamente por:",
    "En la dirección https://sede.justiciaencanarias.es",
    "El presente documento ha sido descargado",
)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = Path("/usr/share/fonts/truetype/dejavu") / name
    return ImageFont.truetype(str(path), size=size)


def wrap(draw: ImageDraw.ImageDraw, text: str, maximum: int, face: ImageFont.FreeTypeFont) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=face) <= maximum:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _pixel_rect(rect: fitz.Rect, scale: float, width: int, height: int) -> tuple[int, int, int, int]:
    margin = 2 * scale
    return (
        max(0, int(rect.x0 * scale - margin)),
        max(0, int(rect.y0 * scale - margin)),
        min(width, int(rect.x1 * scale + margin)),
        min(height, int(rect.y1 * scale + margin)),
    )


def _footer_start(page: fitz.Page) -> float | None:
    starts: list[float] = []
    for block in page.get_text("blocks"):
        compact = " ".join(block[4].split())
        if any(marker.lower() in compact.lower() for marker in FOOTER_MARKERS):
            starts.append(float(block[1]))
    return min(starts) if starts else None


def _sensitive_rects(page: fitz.Page) -> list[fitz.Rect]:
    rects: list[fitz.Rect] = []
    for term in PROFESSIONAL_TERMS:
        rects.extend(page.search_for(term))
    for word in page.get_text("words"):
        token = word[4].strip("(),.;:")
        if re.fullmatch(r"(?:[XYZ]\d{7}[A-Z]|\d{8}[A-Z]|[A-Z]\d{8})", token, flags=re.I):
            rects.append(fitz.Rect(word[:4]))
        elif "@" in token and "." in token:
            rects.append(fitz.Rect(word[:4]))
    return rects


def build(
    source: Path,
    output: Path,
    dpi: int = 200,
    header_cutoff: float = 300,
    title: str = "Copia publica redactada de resolucion judicial",
) -> None:
    source_doc = fitz.open(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    public_doc = fitz.open()
    scale = dpi / 72

    for index, page in enumerate(source_doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        draw = ImageDraw.Draw(image)

        if index == 0:
            cutoff = int(header_cutoff * scale)
            draw.rectangle((0, 0, image.width, cutoff), fill="white")
            margin = int(54 * scale)
            title_face = font(max(18, int(13 * scale)), bold=True)
            detail_face = font(max(13, int(8.4 * scale)))
            draw.text((margin, int(40 * scale)), NOTICE, fill="#7d251f", font=title_face)
            y = int(67 * scale)
            for line in wrap(draw, DETAIL, image.width - 2 * margin, detail_face):
                draw.text((margin, y), line, fill="#30383c", font=detail_face)
                y += int(13 * scale)

        footer_start = _footer_start(page)
        if footer_start is not None:
            draw.rectangle((0, int(footer_start * scale - 2), image.width, image.height), fill="white")

        for rect in _sensitive_rects(page):
            if index == 0 and rect.y0 < header_cutoff:
                # The administrative header is already irreversibly removed;
                # do not let source-coordinate redactions overwrite the notice.
                continue
            draw.rectangle(_pixel_rect(rect, scale, image.width, image.height), fill="white")

        jpeg = io.BytesIO()
        image.save(jpeg, format="JPEG", quality=92, subsampling=0, optimize=True)
        public_page = public_doc.new_page(width=page.rect.width, height=page.rect.height)
        public_page.insert_image(public_page.rect, stream=jpeg.getvalue())

    public_doc.set_metadata(
        {
            "title": title,
            "author": "",
            "subject": "Publicacion documental con minimizacion de datos",
            "keywords": "",
            "creator": "Por Derecho",
            "producer": "",
            "creationDate": "",
            "modDate": "",
        }
    )
    public_doc.save(output, garbage=4, clean=True, deflate=True, no_new_id=True)
    public_doc.close()
    source_doc.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--dpi", type=int, default=200)
    parser.add_argument(
        "--header-cutoff",
        type=float,
        default=300,
        help="Page-one PDF y-coordinate through which the administrative header is removed.",
    )
    parser.add_argument(
        "--title",
        default="Copia publica redactada de resolucion judicial",
        help="Plain PDF metadata title for the rebuilt public copy.",
    )
    args = parser.parse_args()
    build(args.source, args.output, args.dpi, args.header_cutoff, args.title)


if __name__ == "__main__":
    main()

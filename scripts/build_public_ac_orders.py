#!/usr/bin/env python3
"""Build irreversible, image-only public copies of the two AC-removal orders.

The source PDFs contain administrative headers, NIG data, notification metadata,
professional/third-party names, AcroForm fields and verification metadata.  This
builder rasterises every page, removes the page-one administrative block, adds a
plain public-copy notice and writes a new PDF without a text layer, forms,
annotations or inherited metadata.
"""

from __future__ import annotations

import argparse
import io
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont


NOTICE = "COPIA PUBLICA REDACTADA"
DETAIL = (
    "Cabecera administrativa, identificadores, nombres profesionales/terceros "
    "y metadatos de notificacion suprimidos. Texto judicial sustantivo sin cambios."
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


def build(source: Path, output: Path, dpi: int = 200, header_cutoff: float = 300) -> None:
    source_doc = fitz.open(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    public_doc = fitz.open()
    scale = dpi / 72

    for index, page in enumerate(source_doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

        if index == 0:
            draw = ImageDraw.Draw(image)
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

        jpeg = io.BytesIO()
        image.save(jpeg, format="JPEG", quality=92, subsampling=0, optimize=True)
        public_page = public_doc.new_page(width=page.rect.width, height=page.rect.height)
        public_page.insert_image(public_page.rect, stream=jpeg.getvalue())

    public_doc.set_metadata(
        {
            "title": "Copia publica redactada de resolucion judicial",
            "author": "",
            "subject": "Publicacion documental con minimizacion de datos",
            "keywords": "",
            "creator": "Por Derecho",
            "producer": "",
            "creationDate": "",
            "modDate": "",
        }
    )
    public_doc.save(output, garbage=4, clean=True, deflate=True)
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
    args = parser.parse_args()
    build(args.source, args.output, args.dpi, args.header_cutoff)


if __name__ == "__main__":
    main()

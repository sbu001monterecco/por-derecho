#!/usr/bin/env python3
"""Build the public-safe derivative of the 6 April 2022 AEAT diligence.

The received five-page PDF contains later editorial highlight annotations,
official contact details, officer NUMA identifiers and handwritten signatures.
This builder verifies the native source hash, renders every page without
annotations, burns the limited redactions into a raster derivative and then
validates that no hidden text, annotations, forms or source metadata remain.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter


SOURCE_SHA256 = "b6ffc7cf29928a41bac7a466d16e513cc5e2f1c8d8db5069ae86ba64e117bb16"
SOURCE_PAGE_COUNT = 5
EVIDENCE_ID = "EVID-AEAT-PINK-VA-20220406-001"
OUTPUT_NAME = "diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022-public-redacted.pdf"
PREVIEW_NAME = "diligencia-aeat-vigilancia-aduanera-sun-park-6abril2022-page1-public.png"
RENDER_DPI = 140


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def scale_rect(rect: fitz.Rect, sx: float, sy: float, pad: int = 4) -> tuple[int, int, int, int]:
    return (
        max(0, round(rect.x0 * sx) - pad),
        max(0, round(rect.y0 * sy) - pad),
        round(rect.x1 * sx) + pad,
        round(rect.y1 * sy) + pad,
    )


def whiteout(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str | None = None) -> None:
    draw.rectangle(box, fill="white", outline="#67747a", width=2)
    if not label:
        return
    font = load_font(max(14, min(25, (box[3] - box[1]) // 4)))
    draw.multiline_text(
        (box[0] + 10, box[1] + 10),
        label,
        fill="#24343b",
        font=font,
        spacing=4,
    )


def render_page(page: fitz.Page, page_number: int) -> Image.Image:
    matrix = fitz.Matrix(RENDER_DPI / 72, RENDER_DPI / 72)
    pixmap = page.get_pixmap(matrix=matrix, alpha=False, annots=False)
    image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
    draw = ImageDraw.Draw(image)
    sx = image.width / page.rect.width
    sy = image.height / page.rect.height

    # Every page repeats the issuing office's contact block. It is not
    # needed to understand or test the document's substantive propositions.
    if page_number in {1, 2, 3, 4, 5}:
        footer = scale_rect(fitz.Rect(326, 731, 595, 842), sx, sy, pad=0)
        whiteout(draw, footer, "DATOS DE CONTACTO\nOMITIDOS EN LA COPIA PUBLICA")

    if page_number == 1:
        # Officer identifiers and the corporate contact telephone are removed.
        # Identify them by validated format and page position so the redaction
        # builder does not itself publish the sensitive literal values.
        numa_rects: list[fitz.Rect] = []
        phone_rects: list[fitz.Rect] = []
        for x0, y0, x1, y1, token, *_ in page.get_text("words"):
            if y0 >= 720:
                continue
            if re.fullmatch(r"\d{5}", token):
                numa_rects.append(fitz.Rect(x0, y0, x1, y1))
            if re.fullmatch(r"\d{9}", token):
                phone_rects.append(fitz.Rect(x0, y0, x1, y1))
        if len(numa_rects) != 3 or len(phone_rects) != 1:
            raise RuntimeError(
                "Unexpected identifier pattern count on source page 1: "
                f"NUMA={len(numa_rects)}, telephone={len(phone_rects)}"
            )
        for rect in numa_rects + phone_rects:
            whiteout(draw, scale_rect(rect, sx, sy))

    if page_number == 5:
        signature = scale_rect(fitz.Rect(44, 210, 280, 372), sx, sy, pad=0)
        whiteout(draw, signature, "FIRMAS Y NUMA\nOMITIDOS EN LA COPIA PUBLICA")

    return image


def validate_output(pdf_path: Path, preview_path: Path) -> None:
    reader = PdfReader(pdf_path)
    if len(reader.pages) != SOURCE_PAGE_COUNT:
        raise RuntimeError(f"Unexpected public PDF page count: {len(reader.pages)}")
    if reader.get_fields():
        raise RuntimeError("Public PDF still contains AcroForm fields")
    if reader.trailer["/Root"].get("/AcroForm"):
        raise RuntimeError("Public PDF still contains an AcroForm dictionary")
    for index, page in enumerate(reader.pages, start=1):
        if page.get("/Annots"):
            raise RuntimeError(f"Public PDF page {index} still contains annotations")
        if (page.extract_text() or "").strip():
            raise RuntimeError(f"Public PDF page {index} unexpectedly contains a text layer")
    if not preview_path.exists() or preview_path.stat().st_size == 0:
        raise RuntimeError("Public page-one preview was not created")


def canonicalise_pdf_metadata(pdf_path: Path) -> None:
    """Remove Pillow's run-time metadata so repeated builds are byte-stable."""
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata(
        {
            "/Title": f"{EVIDENCE_ID} - public redacted derivative",
            "/Author": "Por Derecho",
            "/Subject": "Public-safe derivative; Spanish official source controls",
            "/CreationDate": "D:20220406000000+00'00'",
            "/ModDate": "D:20260828000000+00'00'",
        }
    )
    temporary_path = pdf_path.with_name(f"{pdf_path.stem}.canonical.tmp.pdf")
    with temporary_path.open("wb") as stream:
        writer.write(stream)
    temporary_path.replace(pdf_path)


def build(source: Path, output_root: Path) -> tuple[Path, Path]:
    actual_sha = sha256(source)
    if actual_sha != SOURCE_SHA256:
        raise RuntimeError(f"Native source hash mismatch: {actual_sha}")

    document = fitz.open(source)
    if document.page_count != SOURCE_PAGE_COUNT:
        raise RuntimeError(f"Unexpected native page count: {document.page_count}")

    output_pdf_dir = output_root / "public-pdfs"
    output_page_dir = output_root / "public-pages"
    output_pdf_dir.mkdir(parents=True, exist_ok=True)
    output_page_dir.mkdir(parents=True, exist_ok=True)

    pages = [render_page(document.load_page(i), i + 1) for i in range(document.page_count)]
    document.close()

    pdf_path = output_pdf_dir / OUTPUT_NAME
    preview_path = output_page_dir / PREVIEW_NAME
    pages[0].save(preview_path, format="PNG", optimize=True)
    pages[0].save(
        pdf_path,
        format="PDF",
        save_all=True,
        append_images=pages[1:],
        resolution=RENDER_DPI,
        quality=70,
        optimize=True,
        title=f"{EVIDENCE_ID} - public redacted derivative",
        author="Por Derecho",
        subject="Public-safe derivative; Spanish official source controls",
    )
    canonicalise_pdf_metadata(pdf_path)
    for page in pages:
        page.close()

    validate_output(pdf_path, preview_path)
    print(f"PDF={pdf_path}")
    print(f"PREVIEW={preview_path}")
    print(f"PDF_SHA256={sha256(pdf_path)}")
    print(f"PREVIEW_SHA256={sha256(preview_path)}")
    return pdf_path, preview_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("evidence/aeat/pink/2022-04-06-vigilancia-aduanera"),
    )
    args = parser.parse_args()
    build(args.source.resolve(), args.output_root.resolve())


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the privacy-controlled public visual derivative for E.G. 745/2026.

The native PDF is private and must never be written into the repository.  This
builder accepts only the byte-identified native source, extracts its three
embedded scan images, masks the recipient's personal email on page 1 at the
controlled pixel rectangle, and writes raster-only public derivatives.

The PDF is rebuilt from the redacted raster pages.  It therefore contains no
overlay that could be removed to recover the recipient email and no OCR layer.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import shutil
import tempfile
from pathlib import Path

import fitz
from PIL import Image, ImageChops, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


NATIVE_SHA256 = "1e09c8eb3bce26e28dc5f22e5d6ebad3f458212cf8d85f5920e869fa42554abe"
EXPECTED_PAGE_COUNT = 3
EXPECTED_SCAN_SIZE = (1654, 2338)

# Controlled against the 1654 x 2338 embedded scan on page 1.  The underlying
# personal-email glyphs occupy x=250..606 and y=488..518.  The margin below is
# deliberate; it does not touch the recipient name above or body text below.
# Pillow ImageDraw treats both maximum coordinates as inclusive.  The matching
# half-open box is recorded separately for crop/difference validation.
PAGE_1_REDACTION_RECT_PIL_INCLUSIVE = (232, 474, 625, 535)
PAGE_1_REDACTION_BOX_HALF_OPEN = (232, 474, 626, 536)
REDACTION_FILL = (32, 32, 32)

PUBLIC_PDF = "oficio-decreto-eg-745-2026-public-redacted.pdf"
PNG_NAMES = (
    "page-1-public-redacted.png",
    "page-2-public.png",
    "page-3-public.png",
)
WEBP_NAMES = (
    "page-1-public-redacted.webp",
    "page-2-public.webp",
    "page-3-public.webp",
)
HASH_MANIFEST = "eg745-public-visual-sha256.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_scans(source: Path) -> list[Image.Image]:
    document = fitz.open(source)
    if document.page_count != EXPECTED_PAGE_COUNT:
        raise ValueError(
            f"expected {EXPECTED_PAGE_COUNT} pages, found {document.page_count}"
        )

    scans: list[Image.Image] = []
    for page_number, page in enumerate(document, start=1):
        images = page.get_images(full=True)
        if len(images) != 1:
            raise ValueError(
                f"page {page_number}: expected one embedded scan, found {len(images)}"
            )
        extracted = document.extract_image(images[0][0])
        image = Image.open(io.BytesIO(extracted["image"])).convert("RGB")
        if image.size != EXPECTED_SCAN_SIZE:
            raise ValueError(
                f"page {page_number}: expected {EXPECTED_SCAN_SIZE}, found {image.size}"
            )
        scans.append(image.copy())
    document.close()
    return scans


def save_png(image: Image.Image, destination: Path) -> None:
    image.save(destination, "PNG", optimize=False, compress_level=9)


def save_webp(image: Image.Image, destination: Path) -> None:
    target_width = 1240
    target_height = round(image.height * target_width / image.width)
    preview = image.resize(
        (target_width, target_height), resample=Image.Resampling.LANCZOS
    )
    preview.save(
        destination,
        "WEBP",
        quality=90,
        method=6,
        exact=True,
    )


def save_raster_pdf(images: list[Image.Image], destination: Path) -> None:
    page_width, page_height = A4
    pdf = canvas.Canvas(
        str(destination),
        pagesize=A4,
        invariant=1,
        pageCompression=1,
    )
    pdf.setTitle("E.G. 745/2026 - privacy-controlled public derivative")
    pdf.setAuthor("Por Derecho / Project Sun Rock")
    pdf.setSubject("Raster-only public copy; recipient personal email redacted")
    pdf.setCreator("Por Derecho deterministic raster-first publication pipeline")
    for image in images:
        encoded = io.BytesIO()
        image.save(
            encoded,
            "JPEG",
            quality=92,
            subsampling=0,
            optimize=True,
        )
        encoded.seek(0)
        pdf.drawImage(
            ImageReader(encoded),
            0,
            0,
            width=page_width,
            height=page_height,
            preserveAspectRatio=False,
            mask=None,
        )
        pdf.showPage()
    pdf.save()


def build(source: Path, output_dir: Path) -> dict[str, object]:
    if sha256_file(source) != NATIVE_SHA256:
        raise ValueError("native source SHA-256 does not match the controlling source")

    scans = extract_scans(source)
    original_page_1 = scans[0].copy()
    ImageDraw.Draw(scans[0]).rectangle(
        PAGE_1_REDACTION_RECT_PIL_INCLUSIVE,
        fill=REDACTION_FILL,
        outline=REDACTION_FILL,
        width=1,
    )
    changed_box = ImageChops.difference(original_page_1, scans[0]).getbbox()
    if changed_box != PAGE_1_REDACTION_BOX_HALF_OPEN:
        raise ValueError(
            "page-1 changed-pixel box does not match the controlled redaction box"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix="eg745-public-visual-", dir=output_dir))
    try:
        for image, filename in zip(scans, PNG_NAMES, strict=True):
            save_png(image, temp_dir / filename)
        for image, filename in zip(scans, WEBP_NAMES, strict=True):
            save_webp(image, temp_dir / filename)
        save_raster_pdf(scans, temp_dir / PUBLIC_PDF)

        outputs = [PUBLIC_PDF, *PNG_NAMES, *WEBP_NAMES]
        manifest: dict[str, object] = {
            "schema": "por-derecho.eg745-public-visual-hashes.v1",
            "source": {
                "filename": "OFICIO Y DECRETO EXP. 745-26.pdf",
                "pages": EXPECTED_PAGE_COUNT,
                "sha256": NATIVE_SHA256,
                "public": False,
            },
            "privacy_control": {
                "page_1_redaction": "recipient personal email only",
                "pixel_rectangle_pillow_inclusive": list(
                    PAGE_1_REDACTION_RECT_PIL_INCLUSIVE
                ),
                "pixel_box_half_open": list(PAGE_1_REDACTION_BOX_HALF_OPEN),
                "raster_first": True,
                "ocr_layer": False,
            },
            "outputs": {
                filename: {
                    "bytes": (temp_dir / filename).stat().st_size,
                    "sha256": sha256_file(temp_dir / filename),
                }
                for filename in outputs
            },
        }
        manifest_path = temp_dir / HASH_MANIFEST
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        for filename in [*outputs, HASH_MANIFEST]:
            os.replace(temp_dir / filename, output_dir / filename)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    manifest = build(args.source.resolve(), args.output_dir.resolve())
    for filename, control in manifest["outputs"].items():
        print(f"{control['sha256']}  {filename}")


if __name__ == "__main__":
    main()

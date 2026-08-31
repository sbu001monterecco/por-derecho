#!/usr/bin/env python3
"""Validate the prepared E.G. 745/2026 privacy-controlled visual release."""

from __future__ import annotations

import base64
import hashlib
import io
import json
from pathlib import Path

import fitz
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "evidence/fiscalia/2026/eg745-visual-assets"
PUBLICATION_MANIFEST = (
    ROOT / "publication-manifests/eg-745-2026-visual-publication-20260831.json"
)
HASH_MANIFEST = ASSET_DIR / "eg745-public-visual-sha256.json"

VIEWERS = (
    ROOT
    / "es/fiscalia-inspeccion-exp-gub-745-2026/facsimil-visual-31-agosto-2026.html",
    ROOT
    / "en/public-prosecution-inspection-exp-gub-745-2026/visual-facsimile-31-august-2026.html",
)

VIEWER_ROUTES = (
    "https://sbu001monterecco.github.io/por-derecho/es/fiscalia-inspeccion-exp-gub-745-2026/facsimil-visual-31-agosto-2026.html",
    "https://sbu001monterecco.github.io/por-derecho/en/public-prosecution-inspection-exp-gub-745-2026/visual-facsimile-31-august-2026.html",
)

SITEMAPS = (ROOT / "sitemap-fiscalia-exp-gub-745.xml", ROOT / "sitemap.xml")

STATUS_PAGES = (
    ROOT / "es/fiscalia-inspeccion-exp-gub-745-2026/index.html",
    ROOT / "es/fiscalia-inspeccion-exp-gub-745-2026/paquete-respuesta-29-agosto-2026.html",
    ROOT
    / "es/fiscalia-inspeccion-exp-gub-745-2026/persecucion-abierta-transparencia-31-agosto-2026.html",
    ROOT / "es/fiscalia-inspeccion-exp-gub-745-2026/diario-actuaciones-29-agosto-2026.html",
    ROOT / "en/public-prosecution-inspection-exp-gub-745-2026/index.html",
    ROOT
    / "en/public-prosecution-inspection-exp-gub-745-2026/response-package-29-august-2026.html",
    ROOT
    / "en/public-prosecution-inspection-exp-gub-745-2026/open-prosecution-transparency-31-august-2026.html",
    ROOT
    / "en/public-prosecution-inspection-exp-gub-745-2026/action-diary-29-august-2026.html",
)

PNG_FILES = (
    "page-1-public-redacted.png",
    "page-2-public.png",
    "page-3-public.png",
)
WEBP_FILES = (
    "page-1-public-redacted.webp",
    "page-2-public.webp",
    "page-3-public.webp",
)
PDF_FILE = "oficio-decreto-eg-745-2026-public-redacted.pdf"
EXPECTED_SCAN_SIZE = (1654, 2338)
EXPECTED_PREVIEW_SIZE = (1240, 1753)
PAGE_1_REDACTION_RECT_PIL_INCLUSIVE = (232, 474, 625, 535)
PAGE_1_REDACTION_BOX_HALF_OPEN = (232, 474, 626, 536)
EXPECTED_OLD_PAGE_3_SHA256 = (
    "b73a712a27c737dd8e22bf462c6e1cce095d05f8d12a3b93b1d0c763f84b528b"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_hashes() -> None:
    manifest = json.loads(PUBLICATION_MANIFEST.read_text(encoding="utf-8"))
    require(
        manifest["current_state"] == "PREPARED_PENDING_MERGE",
        "visual publication must remain PREPARED_PENDING_MERGE before deployment",
    )
    controls = json.loads(HASH_MANIFEST.read_text(encoding="utf-8"))
    require(controls["source"]["public"] is False, "native source must remain private")
    privacy = controls["privacy_control"]
    require(
        tuple(privacy["pixel_rectangle_pillow_inclusive"])
        == PAGE_1_REDACTION_RECT_PIL_INCLUSIVE,
        "Pillow-inclusive redaction rectangle control mismatch",
    )
    require(
        tuple(privacy["pixel_box_half_open"]) == PAGE_1_REDACTION_BOX_HALF_OPEN,
        "half-open redaction box control mismatch",
    )

    expected = {item["path"]: item for item in manifest["expected_assets"]}
    require(len(expected) == 7, "expected exactly seven public derivatives")
    for relative_path, item in expected.items():
        path = ROOT / relative_path
        require(path.is_file(), f"missing derivative: {relative_path}")
        require(path.stat().st_size == item["bytes"], f"byte mismatch: {relative_path}")
        require(sha256(path) == item["sha256"], f"SHA-256 mismatch: {relative_path}")
        local_name = path.name
        require(local_name in controls["outputs"], f"missing local hash control: {local_name}")
        require(
            controls["outputs"][local_name]["sha256"] == item["sha256"],
            f"hash-control mismatch: {local_name}",
        )


def validate_images() -> None:
    for filename in PNG_FILES:
        with Image.open(ASSET_DIR / filename) as image:
            require(image.format == "PNG", f"not PNG: {filename}")
            require(image.size == EXPECTED_SCAN_SIZE, f"wrong PNG dimensions: {filename}")
            require(image.mode == "RGB", f"wrong PNG mode: {filename}")
    for filename in WEBP_FILES:
        with Image.open(ASSET_DIR / filename) as image:
            require(image.format == "WEBP", f"not WebP: {filename}")
            require(
                image.size == EXPECTED_PREVIEW_SIZE,
                f"wrong WebP dimensions: {filename}",
            )

    with Image.open(ASSET_DIR / PNG_FILES[0]) as image:
        crop = image.convert("RGB").crop(PAGE_1_REDACTION_BOX_HALF_OPEN)
        colors = crop.getcolors(maxcolors=2)
        expected_pixels = (
            (PAGE_1_REDACTION_BOX_HALF_OPEN[2] - PAGE_1_REDACTION_BOX_HALF_OPEN[0])
            * (PAGE_1_REDACTION_BOX_HALF_OPEN[3] - PAGE_1_REDACTION_BOX_HALF_OPEN[1])
        )
        require(
            colors == [(expected_pixels, (32, 32, 32))],
            "page-1 PNG redaction rectangle is not opaque and uniform",
        )


def validate_pdf() -> None:
    path = ASSET_DIR / PDF_FILE
    document = fitz.open(path)
    require(document.page_count == 3, "public PDF must contain three pages")
    require(not document.is_form_pdf, "public PDF must not contain a form")
    metadata_text = " ".join(str(value or "") for value in document.metadata.values()).lower()
    require("monterecco" not in metadata_text, "private token present in PDF metadata")
    for page_number, page in enumerate(document, start=1):
        require(not page.get_text().strip(), f"PDF page {page_number} contains a text/OCR layer")
        annotations = list(page.annots() or [])
        require(not annotations, f"PDF page {page_number} contains annotations")
        images = page.get_images(full=True)
        require(len(images) == 1, f"PDF page {page_number} must contain one raster image")
        extracted = document.extract_image(images[0][0])
        with Image.open(io.BytesIO(extracted["image"])) as image:
            require(image.size == EXPECTED_SCAN_SIZE, f"PDF page {page_number} image size mismatch")
            if page_number == 1:
                interior = image.convert("RGB").crop((245, 485, 612, 524))
                extrema = interior.getextrema()
                require(
                    max(channel[1] for channel in extrema) < 55,
                    "PDF page-1 redaction interior is not opaque",
                )
    document.close()
    binary = path.read_bytes().lower()
    require(b"monterecco" not in binary and b"sbu001" not in binary, "private token in PDF bytes")


def validate_viewers_and_status() -> None:
    required_assets = [PDF_FILE, *PNG_FILES, *WEBP_FILES]
    for viewer in VIEWERS:
        text = viewer.read_text(encoding="utf-8")
        require("PREPARED_PENDING_MERGE" in text, f"missing pending status: {viewer}")
        require(".b64" not in text, f"viewer still reconstructs Base64 assets: {viewer}")
        for filename in required_assets:
            require(filename in text, f"viewer does not reference {filename}: {viewer}")
    for page in STATUS_PAGES:
        require(
            "PREPARED_PENDING_MERGE" in page.read_text(encoding="utf-8"),
            f"status page does not carry pending visual state: {page}",
        )
    for sitemap in SITEMAPS:
        text = sitemap.read_text(encoding="utf-8")
        for route in VIEWER_ROUTES:
            require(route in text, f"viewer route missing from {sitemap}: {route}")


def validate_inherited_page_3_correction() -> None:
    chunks = sorted(ASSET_DIR.glob("p3-*.b64"))
    require(len(chunks) == 3, "expected three inherited page-3 Base64 chunks")
    encoded = "".join(path.read_text(encoding="ascii") for path in chunks)
    decoded = base64.b64decode("".join(encoded.split()), validate=True)
    require(
        hashlib.sha256(decoded).hexdigest() == EXPECTED_OLD_PAGE_3_SHA256,
        "inherited page-3 Base64 correction no longer matches the preserved chunks",
    )


def main() -> None:
    validate_hashes()
    validate_images()
    validate_pdf()
    validate_viewers_and_status()
    validate_inherited_page_3_correction()
    print("E.G. 745 public visual validation: PASS")
    print("7 derivatives; 3 PNG; 3 WebP; 3-page raster-only PDF")
    print("status: PREPARED_PENDING_MERGE")


if __name__ == "__main__":
    main()

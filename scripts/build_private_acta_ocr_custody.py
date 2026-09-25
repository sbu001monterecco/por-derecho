#!/usr/bin/env python3
"""Build a page-sequenced, private OCR derivative without publishing source text.

The output directory must be outside the repository.  It contains rendered page
images, one UTF-8 OCR text file per page, a combined text file and a private
manifest.  The manifest distinguishes automated page association from manual
line-by-line verification; it never calls Tesseract output certified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageStat
from pypdf import PdfReader


REPO = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def available_languages() -> set[str]:
    result = subprocess.run(
        ["tesseract", "--list-langs"],
        check=True,
        capture_output=True,
        text=True,
    )
    return {
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip() and "List of available languages" not in line
    }


def ocr_page(image: Path, text_path: Path, language: str) -> dict[str, object]:
    environment = dict(os.environ)
    environment["OMP_THREAD_LIMIT"] = "1"
    result = subprocess.run(
        ["tesseract", str(image), "stdout", "-l", language, "--psm", "6"],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )
    text = result.stdout.replace("\r\n", "\n")
    text_path.write_text(text, encoding="utf-8")
    text_path.chmod(0o600)
    with Image.open(image) as opened:
        grayscale = opened.convert("L")
        stat = ImageStat.Stat(grayscale)
        width, height = grayscale.size
        extrema = grayscale.getextrema()
    return {
        "page": int(image.stem.rsplit("-", 1)[-1]),
        "image_file": image.name,
        "image_bytes": image.stat().st_size,
        "image_sha256": sha256(image),
        "image_width": width,
        "image_height": height,
        "image_extrema": list(extrema),
        "image_stddev": round(float(stat.stddev[0]), 6),
        "ocr_file": text_path.name,
        "ocr_bytes": text_path.stat().st_size,
        "ocr_sha256": sha256(text_path),
        "ocr_characters": len(text),
        "ocr_non_whitespace_characters": len("".join(text.split())),
        "automated_image_nonblank": bool(stat.stddev[0] > 0.25 or extrema[0] != extrema[1]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--expected-pages", type=int, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--dpi", type=int, default=200)
    args = parser.parse_args()

    source = args.source.resolve()
    output_root = args.output_root.resolve()
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,127}", args.slug):
        raise SystemExit("Slug must be a single safe lowercase path component")
    try:
        output_root.relative_to(REPO)
    except ValueError:
        pass
    else:
        raise SystemExit("Private OCR output must remain outside the repository")
    try:
        source.relative_to(REPO)
    except ValueError:
        pass
    else:
        raise SystemExit("Private OCR native source must remain outside the repository")
    if not source.is_file():
        raise SystemExit(f"Source not found: {source}")
    if sha256(source) != args.expected_sha256:
        raise SystemExit("Source SHA-256 does not match the expected control")
    if len(PdfReader(str(source)).pages) != args.expected_pages:
        raise SystemExit("Source page count does not match the expected control")

    package = (output_root / args.slug).resolve()
    try:
        package.relative_to(output_root)
    except ValueError as exc:
        raise SystemExit("Private OCR package escaped the approved output root") from exc
    if package.exists() and any(package.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty private OCR package: {package}")
    images = package / "page-images"
    texts = package / "page-ocr"
    images.mkdir(parents=True, exist_ok=True, mode=0o700)
    texts.mkdir(parents=True, exist_ok=True, mode=0o700)
    package.chmod(0o700)

    subprocess.run(
        [
            "pdftoppm", "-r", str(args.dpi), "-jpeg", "-jpegopt", "quality=90",
            str(source), str(images / "page"),
        ],
        check=True,
    )
    rendered = sorted(images.glob("page-*.jpg"))
    if len(rendered) != args.expected_pages:
        raise SystemExit(f"Rendered page count {len(rendered)} != {args.expected_pages}")
    for image in rendered:
        image.chmod(0o600)

    languages = available_languages()
    language = "spa" if "spa" in languages else "eng"
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = [
            pool.submit(ocr_page, image, texts / f"page-{page:03d}.txt", language)
            for page, image in enumerate(rendered, 1)
        ]
        pages = [future.result() for future in futures]
    pages.sort(key=lambda item: int(item["page"]))
    blank_pages = [
        int(item["page"])
        for item in pages
        if not bool(item["automated_image_nonblank"])
    ]
    if blank_pages:
        raise SystemExit(f"Refusing corrupt/blank rendered page images: {blank_pages}")

    combined = package / "page-sequenced-ocr.txt"
    with combined.open("w", encoding="utf-8", newline="\n") as handle:
        for item in pages:
            page = int(item["page"])
            handle.write(f"===== PAGE {page}/{args.expected_pages} =====\n")
            handle.write((texts / str(item["ocr_file"])).read_text(encoding="utf-8"))
            handle.write("\n")
    combined.chmod(0o600)

    manifest = {
        "schema_version": "1.0",
        "classification": "RESTRICTED_PRIVATE_OCR_DERIVATIVE",
        "repository_status": "OUTSIDE_PUBLIC_REPOSITORY",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "slug": args.slug,
        "source": {
            "bytes": source.stat().st_size,
            "pages": args.expected_pages,
            "sha256": args.expected_sha256,
        },
        "ocr": {
            "engine": subprocess.run(
                ["tesseract", "--version"], check=True, capture_output=True, text=True
            ).stdout.splitlines()[0],
            "requested_language": "spa",
            "effective_language": language,
            "language_fallback": language != "spa",
            "mode": "automated-ocr-uncertified",
            "page_association_verified": True,
            "page_order_verified": True,
            "rendered_image_count": len(rendered),
            "ocr_text_count": len(pages),
            "combined_text_file": combined.name,
            "combined_text_bytes": combined.stat().st_size,
            "combined_text_sha256": sha256(combined),
            "manual_line_by_line_verification": False,
            "source_authenticity_established": False,
        },
        "automated_comparison": {
            "all_page_images_decode": True,
            "all_page_images_nonblank": all(bool(item["automated_image_nonblank"]) for item in pages),
            "pages_with_zero_ocr_characters": [
                int(item["page"]) for item in pages if int(item["ocr_non_whitespace_characters"]) == 0
            ],
            "boundary": "Image/OCR page association and nonblank checks are automated; wording is not manually certified.",
        },
        "pages": pages,
    }
    manifest_path = package / "private-ocr-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_path.chmod(0o600)
    package_inventory = {
        "slug": args.slug,
        "files": [
            {
                "path": path.relative_to(package).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in sorted(package.rglob("*"))
            if path.is_file()
        ],
    }
    inventory_path = package / "private-ocr-package-inventory.json"
    inventory_path.write_text(
        json.dumps(package_inventory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    inventory_path.chmod(0o600)
    print(json.dumps({
        "status": "pass",
        "slug": args.slug,
        "pages": len(pages),
        "language": language,
        "manual_line_by_line_verification": False,
        "manifest_sha256": sha256(manifest_path),
        "inventory_sha256": sha256(inventory_path),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Rebuild and validate the public-redacted ACTA document packages.

This script deliberately contains no native-source or private filesystem paths.
The versioned, public-redacted ``transcript-es.md`` files are the build inputs for
the public text-edition PDFs and current JPEG previews.  Legacy WEBP previews may
remain in their existing directories as separate derivatives.  An optional
private source map may be supplied at validation time to verify source hashes and
page counts without copying or persisting those paths.

Examples::

    python3 evidence/community/actas/build_public_packages.py validate
    python3 evidence/community/actas/build_public_packages.py validate \
        --source-map /path/to/private-source-map.json
    python3 evidence/community/actas/build_public_packages.py build --all
    python3 evidence/community/actas/build_public_packages.py build \
        --slug 2011-06-22 --slug 2022-02-04

``build`` rewrites public PDFs/previews and synchronises their hashes/counts in
the package manifests and public index.  ``validate`` is read-only with respect to
the repository and renders PDFs only inside a temporary directory.

The private source map remains a JSON object keyed by package slug.  A PDF may
retain the legacy string value.  A typed PDF or DOCX control uses this shape::

    {
      "2012-08-10": {
        "path": "/private/native-control.docx",
        "media_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "page_count_method": "recorded-deterministic-docx-to-pdf",
        "page_count": 4
      }
    }

For DOCX, ``temporary-libreoffice-docx-to-pdf`` privately converts into an
isolated temporary directory and counts the resulting PDF.  ``page_count`` is
optional for that method and, when supplied, is independently checked.  Neither
the native source nor the temporary PDF is written into the repository.
The source-map file and every mapped native source must resolve outside the
repository; private absolute paths are never included in validation errors.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Iterable

import fitz
from PIL import Image, ImageChops, ImageStat
from pypdf import PdfReader
from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


REPO = Path(__file__).resolve().parents[3]
PACKAGE_ROOT = REPO / "evidence/community/actas"
INDEX_PATH = PACKAGE_ROOT / "public-index.json"
PDF_ROOT = REPO / "assets/docs/community-actas"
PREVIEW_ROOT = REPO / "assets/evidence/community-actas"

EXPECTED_ARTIFACT_KINDS = {
    "public-redacted-text-edition",
    "public-redacted-digitisation-package",
}
EXPECTED_STATUSES = {
    "located-package-partial",
    "located-package-digitised-public",
}

PDF_MEDIA_TYPE = "application/pdf"
DOCX_MEDIA_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)
PDF_PAGE_COUNT_METHOD = "pdf-page-tree"
DOCX_RECORDED_PAGE_COUNT_METHOD = "recorded-deterministic-docx-to-pdf"
DOCX_TEMPORARY_PAGE_COUNT_METHOD = "temporary-libreoffice-docx-to-pdf"
PRIVATE_SOURCE_MAP_FIELDS = {
    "path",
    "media_type",
    "page_count_method",
    "page_count",
}
PYMUPDF_VERSION = "1.26.6"
PUBLIC_TEXT_MODE_REDACTED_OCR = "redacted-ocr-text"
PUBLIC_TEXT_MODE_MARKERS = "full-page-redaction-markers"
PUBLIC_TEXT_MODES = {
    PUBLIC_TEXT_MODE_REDACTED_OCR,
    PUBLIC_TEXT_MODE_MARKERS,
}
PDF_PUBLIC_TEXT_COPY = {
    PUBLIC_TEXT_MODE_REDACTED_OCR: {
        "subtitle": "Edición pública redactada · texto asistido por OCR no certificado",
        "subject": "ACTA public redacted OCR-assisted text edition; not certified",
        "boundary": (
            "No es el original, el libro diligenciado, una copia certificada ni una "
            "transcripción pericial. El texto público está asistido por OCR y no ha "
            "sido certificado ni cotejado línea por línea. Todas las páginas de la "
            "copia usada están secuenciadas; los datos privados y reservados se "
            "sustituyen por marcadores expresos."
        ),
    },
    PUBLIC_TEXT_MODE_MARKERS: {
        "subtitle": (
            "Edición pública secuenciada por páginas con marcadores de expurgación · "
            "sin OCR público"
        ),
        "subject": "ACTA public page-sequenced redaction-marker edition; no public OCR",
        "boundary": (
            "No es el original, el libro diligenciado, una copia certificada ni una "
            "transcripción pericial. Esta edición conserva la secuencia de páginas "
            "mediante marcadores expresos de expurgación. No contiene OCR público ni "
            "una transcripción pública del texto fuente."
        ),
    },
}

PRIVATE_PATH_PATTERN = re.compile(
    r"(?i)(?:/tmp/|/workspace/|/home/|/Users/|file://|[A-Z]:[\\/]|drive:)"
)
EMAIL_PATTERN = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
IBAN_PATTERN = re.compile(
    r"(?i)\bES(?:\s|_)*\d{2}\b|"
    r"\bES\s*\d{2}(?:\s*\d){20}\b|"
    r"(?<!\d)\d{4}(?:[ .-]?\d{4}){2}[ .-]?\d{2}[ .-]?\d{10}(?!\d)"
)
SPANISH_ID_PATTERN = re.compile(
    r"(?i)\b(?:[XYZ]\s*[- ]?\d{7}|\d{8})\s*[- ]?[A-Z]\b|"
    r"\b\d{1,3}(?:[. ]\d{3}){2}\s*[- ]?\s*[A-Z]\b|"
    r"\b[A-Z]\s*[- ]?\d{7,8}\s*[- ]?[A-Z0-9]?\b|"
    r"\b[A-Z][ .-]?\d{2}(?:[ .-]?\d{3}){2}[ .-]?[A-Z0-9]\b"
)
PHONE_PATTERN = re.compile(
    r"(?<![0-9A-Fa-f])(?:\+?34[ .-]?)?[6789]\d{2}(?:(?:[ .-]?\d{3}){2}|(?:[ .-]?\d{2}){3})(?![0-9A-Fa-f])"
)
ADDRESS_POSTCODE_PATTERN = re.compile(
    r"(?i)(?:calle|avenida|c/|domicilio|playa blanca|yaiza)[^\n]{0,80}\b35\d{3}\b|"
    r"\b35\d{3}\s+(?:yaiza|playa blanca)\b"
)
BANK_ACCOUNT_PATTERN = re.compile(r"(?<!\d)(?:\d[ .-]?){19}\d(?!\d)")
OWNER_LEVEL_FINANCIAL_PATTERN = re.compile(
    r"(?im)(?:N[°º]?\s*ORDEN|N[°º]?\s*APART)[^\n]{0,80}PROPIETARIO"
    r"[^\n]{0,80}(?:CANTIDAD|DEUDA|SALDO|RECLAMADA)|"
    r"^\s*(?:\{?LOC[- ]?\d+(?:-\d+)?|\d{1,3}\s+\d{3})\s+"
    r"[A-ZÁÉÍÓÚÑ][^\n]{1,100}\s+\d{1,3}(?:[.,]\d{3})*[.,]\d{2}[|)}\]]?\s*$"
)


class ValidationError(RuntimeError):
    """Raised when the public package fails an integrity/privacy check."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"Expected JSON object: {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def repo_path(value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValidationError(f"Public artifact path is not repository-relative: {value}")
    resolved = (REPO / candidate).resolve()
    try:
        resolved.relative_to(REPO.resolve())
    except ValueError as exc:
        raise ValidationError(f"Public artifact escapes repository: {value}") from exc
    return resolved


def load_index() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    index = load_json(INDEX_PATH)
    events = index.get("events")
    items = index.get("items")
    if not isinstance(events, list) or not all(isinstance(row, dict) for row in events):
        raise ValidationError("public-index.json must contain an object array named events")
    if not isinstance(items, list):
        raise ValidationError("public-index.json must contain an object array named items")
    # ``events`` is canonical during a controlled rebuild.  The build command
    # rewrites the legacy ``items`` alias after package metadata changes.
    return index, events


def selected_events(slugs: Iterable[str] | None = None) -> list[dict[str, Any]]:
    _, events = load_index()
    wanted = set(slugs or ())
    if not wanted:
        return events
    selected = [event for event in events if event.get("slug") in wanted]
    found = {event.get("slug") for event in selected}
    missing = wanted - found
    if missing:
        raise ValidationError(f"Unknown package slug(s): {sorted(missing)}")
    return selected


def parse_transcript(path: Path) -> tuple[str, list[str], int]:
    text = path.read_text(encoding="utf-8")
    marker = re.compile(r"^## Página fuente (\d+) de (\d+)\s*$", re.MULTILINE)
    matches = list(marker.finditer(text))
    if not matches:
        raise ValidationError(f"No source-page headings found in {path}")
    totals = {int(match.group(2)) for match in matches}
    if len(totals) != 1:
        raise ValidationError(f"Inconsistent source-page totals in {path}: {totals}")
    total = totals.pop()
    numbers = [int(match.group(1)) for match in matches]
    if numbers != list(range(1, total + 1)):
        raise ValidationError(
            f"Source-page sequence in {path} is {numbers}, expected 1..{total}"
        )
    preamble = text[: matches[0].start()].strip()
    pages: list[str] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        pages.append(text[start:end].strip())
    return preamble, pages, total


def privacy_failures(text: str) -> list[str]:
    tests = {
        "private-filesystem-path": PRIVATE_PATH_PATTERN,
        "email-address": EMAIL_PATTERN,
        "IBAN": IBAN_PATTERN,
        "Spanish-ID-like-value": SPANISH_ID_PATTERN,
        "phone-number": PHONE_PATTERN,
        "address-postcode": ADDRESS_POSTCODE_PATTERN,
        "20-digit-bank-account-like-value": BANK_ACCOUNT_PATTERN,
        "owner-level-financial-row": OWNER_LEVEL_FINANCIAL_PATTERN,
    }
    return [label for label, pattern in tests.items() if pattern.search(text)]


def validate_public_image(path: Path, *, require_current_jpeg: bool = True) -> str:
    """Reject blank/corrupt images and private metadata; return SHA-256."""

    if require_current_jpeg and path.suffix.lower() not in {".jpg", ".jpeg"}:
        raise ValidationError(
            f"Current declared preview must be JPEG (legacy WEBP stays separate): {path}"
        )
    with Image.open(path) as image:
        if require_current_jpeg and image.format != "JPEG":
            raise ValidationError(f"JPEG suffix/format mismatch: {path}")
        image.verify()
    with Image.open(path) as image:
        if image.getexif():
            raise ValidationError(f"Public image contains EXIF metadata: {path}")
        sensitive_metadata = {
            key
            for key in image.info
            if key.lower() in {
                "exif", "xmp", "xml", "photoshop", "iptc", "comment",
                "description", "author", "copyright", "icc_profile",
            }
        }
        if sensitive_metadata:
            raise ValidationError(
                f"Public image contains disallowed metadata {sorted(sensitive_metadata)}: {path}"
            )
        if ImageChops.invert(image.convert("L")).getbbox() is None:
            raise ValidationError(f"Blank public image: {path}")
    return sha256(path)


def normalise_hash_records(
    value: Any,
    *,
    label: str,
) -> list[dict[str, str]] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        raise ValidationError(f"{label}: image hash records must be a list")
    records: list[dict[str, str]] = []
    for row in value:
        if (
            not isinstance(row, dict)
            or not isinstance(row.get("path"), str)
            or not re.fullmatch(r"[0-9a-f]{64}", str(row.get("sha256", "")))
        ):
            raise ValidationError(f"{label}: invalid image hash record {row!r}")
        records.append({"path": row["path"], "sha256": row["sha256"]})
    return records


def verify_image_hash_records(
    slug: str,
    label: str,
    actual: list[dict[str, str]],
    event_value: Any,
    manifest_value: Any,
) -> str:
    event_records = normalise_hash_records(event_value, label=f"{slug}/{label}/index")
    manifest_records = normalise_hash_records(
        manifest_value,
        label=f"{slug}/{label}/manifest",
    )
    if event_records is None and manifest_records is None:
        # Backward-compatible validation for packages created before per-image
        # hash records were introduced: every current JPEG is still hashed and
        # reported deterministically during this read-only validation.
        return "computed-current-jpegs-legacy-unpinned"
    if event_records is None or manifest_records is None:
        raise ValidationError(f"{slug}: {label} hash records must agree in index and manifest")
    if event_records != manifest_records:
        raise ValidationError(f"{slug}: {label} index/manifest hash records differ")
    if event_records != actual:
        raise ValidationError(f"{slug}: {label} JPEG hash mismatch")
    return "declared-hashes-match"


def validate_pdf_metadata(path: Path, reader: PdfReader) -> None:
    metadata = reader.metadata or {}
    public_metadata = "\n".join(
        f"{key}: {value}"
        for key, value in metadata.items()
        if value is not None
    )
    failures = privacy_failures(public_metadata)
    if failures:
        raise ValidationError(f"{path}: PDF metadata privacy scan failed: {failures}")


def validate_facsimile_source_equivalence(
    slug: str,
    facsimile: Path,
    source_images: list[Path],
) -> int:
    """Verify each raster facsimile page embeds and renders its declared JPEG.

    The embedded raster is compared page-for-page with the source-page JPEG.
    Poppler then renders every facsimile page in a temporary directory, proving
    that the PDF page sequence is renderable and non-empty.  No generated file
    is written back to the repository.
    """

    reader = PdfReader(str(facsimile))
    if len(reader.pages) != len(source_images):
        raise ValidationError(f"{slug}: facsimile/source-image count mismatch")
    for number, (page, source_path) in enumerate(
        zip(reader.pages, source_images, strict=True),
        start=1,
    ):
        embedded = list(page.images)
        if len(embedded) != 1:
            raise ValidationError(
                f"{slug}: facsimile page {number} must contain exactly one raster image"
            )
        with Image.open(io.BytesIO(embedded[0].data)) as facsimile_image:
            embedded_rgb = facsimile_image.convert("RGB")
        with Image.open(source_path) as source_image:
            source_rgb = source_image.convert("RGB")
        if embedded_rgb.size != source_rgb.size:
            raise ValidationError(
                f"{slug}: facsimile page {number} raster dimensions differ from source JPEG"
            )
        difference = ImageChops.difference(embedded_rgb, source_rgb)
        rms = max(ImageStat.Stat(difference).rms)
        if rms > 2.0:
            raise ValidationError(
                f"{slug}: facsimile page {number} raster differs from source JPEG "
                f"(RMS {rms:.3f})"
            )

    with tempfile.TemporaryDirectory(prefix=f"acta-facsimile-validate-{slug}-") as tmp:
        prefix = Path(tmp) / "page"
        subprocess.run(
            ["pdftoppm", "-png", "-r", "72", str(facsimile), str(prefix)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        rendered = sorted(Path(tmp).glob("page-*.png"))
        if len(rendered) != len(source_images):
            raise ValidationError(f"{slug}: facsimile render page count mismatch")
        for number, page in enumerate(rendered, start=1):
            with Image.open(page) as image:
                image.verify()
            with Image.open(page) as image:
                if ImageChops.invert(image.convert("L")).getbbox() is None:
                    raise ValidationError(
                        f"{slug}: blank rendered facsimile page {number}"
                    )
    return len(source_images)


def pdf_text(path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", str(path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def resolve_private_path_outside_repository(
    path: Path,
    *,
    label: str,
    slug: str | None = None,
) -> Path:
    """Resolve a private control path and enforce the public Git boundary."""

    diagnostic = f"{slug}: {label}" if slug else label
    try:
        resolved = path.resolve()
    except OSError as exc:
        raise ValidationError(f"{diagnostic} cannot be resolved") from exc
    try:
        resolved.relative_to(REPO.resolve())
    except ValueError:
        return resolved
    raise ValidationError(f"{diagnostic} must remain outside the repository")


def derive_source_media_type(source_path: Path) -> str:
    """Return the controlled media type for a supported private source."""

    suffix = source_path.suffix.lower()
    if suffix == ".pdf":
        return PDF_MEDIA_TYPE
    if suffix == ".docx":
        return DOCX_MEDIA_TYPE
    raise ValidationError(
        f"Unsupported private source extension: {suffix or '(none)'}"
    )


def normalise_private_source_entry(slug: str, value: Any) -> dict[str, Any]:
    """Validate and normalise one private source-map entry.

    A legacy string remains valid and is interpreted from its extension.  The
    structured form makes the native media type and page-count evidence
    explicit.  DOCX page counts either come from a recorded deterministic
    conversion control or from a private, temporary LibreOffice conversion.
    """

    if isinstance(value, str):
        row: dict[str, Any] = {"path": value}
    elif isinstance(value, dict):
        row = dict(value)
        unknown = sorted(set(row) - PRIVATE_SOURCE_MAP_FIELDS)
        if unknown:
            raise ValidationError(
                f"{slug}: unsupported private source-map field(s): {unknown}"
            )
    else:
        raise ValidationError(
            f"{slug}: private source-map entry must be a path string or object"
        )

    raw_path = row.get("path")
    if not isinstance(raw_path, str) or not raw_path.strip() or "\x00" in raw_path:
        raise ValidationError(f"{slug}: private source-map path must be a non-empty string")
    source_path = resolve_private_path_outside_repository(
        Path(raw_path).expanduser(),
        label="private native source",
        slug=slug,
    )
    derived_media_type = derive_source_media_type(source_path)

    supplied_media_type = row.get("media_type")
    if supplied_media_type is None:
        media_type = derived_media_type
    elif not isinstance(supplied_media_type, str):
        raise ValidationError(f"{slug}: media_type must be a string")
    elif supplied_media_type != derived_media_type:
        raise ValidationError(
            f"{slug}: media_type {supplied_media_type!r} does not match "
            f"{source_path.suffix.lower()!r} source"
        )
    else:
        media_type = supplied_media_type

    supplied_method = row.get("page_count_method")
    if supplied_method is not None and not isinstance(supplied_method, str):
        raise ValidationError(f"{slug}: page_count_method must be a string")
    if media_type == PDF_MEDIA_TYPE:
        page_count_method = supplied_method or PDF_PAGE_COUNT_METHOD
        allowed_methods = {PDF_PAGE_COUNT_METHOD}
    else:
        page_count_method = supplied_method or DOCX_TEMPORARY_PAGE_COUNT_METHOD
        allowed_methods = {
            DOCX_RECORDED_PAGE_COUNT_METHOD,
            DOCX_TEMPORARY_PAGE_COUNT_METHOD,
        }
    if page_count_method not in allowed_methods:
        raise ValidationError(
            f"{slug}: page_count_method {page_count_method!r} is invalid for "
            f"{media_type}"
        )

    page_count = row.get("page_count")
    if page_count is not None and (
        isinstance(page_count, bool) or not isinstance(page_count, int) or page_count < 1
    ):
        raise ValidationError(f"{slug}: page_count must be a positive integer")
    if (
        page_count_method == DOCX_RECORDED_PAGE_COUNT_METHOD
        and page_count is None
    ):
        raise ValidationError(
            f"{slug}: {DOCX_RECORDED_PAGE_COUNT_METHOD!r} requires page_count"
        )

    return {
        "path": source_path,
        "media_type": media_type,
        "page_count_method": page_count_method,
        "page_count": page_count,
    }


def count_pdf_pages(path: Path, *, slug: str) -> int:
    try:
        page_count = len(PdfReader(str(path)).pages)
    except Exception as exc:
        raise ValidationError(f"{slug}: private PDF cannot be parsed") from exc
    if page_count < 1:
        raise ValidationError(f"{slug}: private PDF contains no pages")
    return page_count


def validate_docx_container(path: Path, *, slug: str) -> None:
    """Reject a corrupt/non-DOCX ZIP before invoking the private converter."""

    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            if not {"[Content_Types].xml", "word/document.xml"}.issubset(names):
                raise ValidationError(
                    f"{slug}: private DOCX lacks required Open XML members"
                )
            if len(names) > 10_000:
                raise ValidationError(f"{slug}: private DOCX has too many ZIP members")
            expanded_bytes = sum(info.file_size for info in archive.infolist())
            if expanded_bytes > 512 * 1024 * 1024:
                raise ValidationError(
                    f"{slug}: private DOCX expanded size exceeds the safety limit"
                )
            corrupt_member = archive.testzip()
            if corrupt_member is not None:
                raise ValidationError(f"{slug}: private DOCX contains a corrupt ZIP member")
    except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        raise ValidationError(f"{slug}: private DOCX container is invalid") from exc


def count_docx_pages_with_libreoffice(path: Path, *, slug: str) -> int:
    """Convert a private DOCX only in an isolated temporary directory."""

    validate_docx_container(path, slug=slug)
    converter = shutil.which("soffice") or shutil.which("libreoffice")
    if converter is None:
        raise ValidationError(
            f"{slug}: LibreOffice is required for temporary DOCX page counting; "
            f"use {DOCX_RECORDED_PAGE_COUNT_METHOD!r} with a controlled page_count "
            "when conversion has already been recorded"
        )

    with tempfile.TemporaryDirectory(prefix=f"acta-private-docx-{slug}-") as tmp:
        temporary_root = Path(tmp).resolve()
        try:
            temporary_root.relative_to(REPO.resolve())
        except ValueError:
            pass
        else:
            raise ValidationError(
                f"{slug}: refusing private DOCX conversion inside the repository"
            )
        output_dir = temporary_root / "output"
        profile_dir = temporary_root / "profile"
        output_dir.mkdir(mode=0o700)
        profile_dir.mkdir(mode=0o700)
        environment = os.environ.copy()
        environment.update(
            {
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
                "SAL_USE_VCLPLUGIN": "svp",
            }
        )
        command = [
            converter,
            "--headless",
            "--nologo",
            "--nodefault",
            "--nolockcheck",
            "--nofirststartwizard",
            f"-env:UserInstallation={profile_dir.as_uri()}",
            "--convert-to",
            "pdf:writer_pdf_Export",
            "--outdir",
            str(output_dir),
            str(path),
        ]
        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=180,
                env=environment,
            )
        except subprocess.TimeoutExpired as exc:
            raise ValidationError(f"{slug}: private DOCX conversion timed out") from exc
        except OSError as exc:
            raise ValidationError(
                f"{slug}: private DOCX converter could not be started"
            ) from exc
        converted = sorted(output_dir.glob("*.pdf"))
        if result.returncode != 0 or len(converted) != 1:
            raise ValidationError(
                f"{slug}: private DOCX conversion did not produce exactly one PDF"
            )
        return count_pdf_pages(converted[0], slug=slug)


def private_source_page_count(entry: dict[str, Any], *, slug: str) -> int:
    media_type = entry["media_type"]
    method = entry["page_count_method"]
    source_path = entry["path"]
    recorded_count = entry["page_count"]

    if media_type == PDF_MEDIA_TYPE:
        actual_pages = count_pdf_pages(source_path, slug=slug)
    elif method == DOCX_RECORDED_PAGE_COUNT_METHOD:
        validate_docx_container(source_path, slug=slug)
        actual_pages = recorded_count
    else:
        actual_pages = count_docx_pages_with_libreoffice(source_path, slug=slug)

    if recorded_count is not None and recorded_count != actual_pages:
        raise ValidationError(
            f"{slug}: private source counted pages {actual_pages} != "
            f"source-map page_count {recorded_count}"
        )
    return actual_pages


def validate_private_source_map(
    source_map_path: Path | None,
    events: list[dict[str, Any]],
) -> list[str]:
    if source_map_path is None:
        return []
    source_map_path = resolve_private_path_outside_repository(
        source_map_path,
        label="private source map",
    )
    try:
        source_map = load_json(source_map_path)
    except ValidationError as exc:
        raise ValidationError("private source map cannot be read or parsed") from exc
    messages: list[str] = []
    for event in events:
        slug = event["slug"]
        value = source_map.get(slug)
        if value is None:
            messages.append(f"{slug}: private source not supplied; skipped")
            continue
        entry = normalise_private_source_entry(slug, value)
        source_path = entry["path"]
        if not source_path.is_file():
            raise ValidationError(f"{slug}: private native source does not exist")
        manifest = load_json(repo_path(event["manifest"]))
        expected_hash = manifest["source"]["sha256"]
        expected_pages = manifest["source_variant_page_count"]
        try:
            actual_hash = sha256(source_path)
        except OSError as exc:
            raise ValidationError(f"{slug}: private native source cannot be read") from exc
        if actual_hash != expected_hash:
            raise ValidationError(
                f"{slug}: private source hash mismatch: {actual_hash} != {expected_hash}"
            )
        actual_pages = private_source_page_count(entry, slug=slug)
        if actual_pages != expected_pages:
            raise ValidationError(
                f"{slug}: private source page mismatch: {actual_pages} != {expected_pages}"
            )
        messages.append(
            f"{slug}: private source hash/pages verified "
            f"({entry['media_type']}; {entry['page_count_method']})"
        )
    return messages


def controlled_public_text_mode(
    event: dict[str, Any],
    manifest: dict[str, Any],
) -> str:
    """Resolve and cross-check the public text mode for PDF labelling."""

    slug = str(event.get("slug") or manifest.get("slug") or "unknown-package")
    declared_modes = [
        value
        for value in (
            event.get("public_text_mode"),
            manifest.get("public_text_mode"),
        )
        if value is not None
    ]
    for mode in declared_modes:
        if mode not in PUBLIC_TEXT_MODES:
            raise ValidationError(f"{slug}: unsupported public_text_mode {mode!r}")
    if len(set(declared_modes)) > 1:
        raise ValidationError(f"{slug}: manifest/index public_text_mode mismatch")

    if declared_modes:
        mode = declared_modes[0]
    elif manifest.get("quality_control", {}).get("ocr_not_certified") is True:
        # Historical redacted-OCR packages predate the explicit mode field.
        # Marker-only mode is never inferred from this legacy control.
        mode = PUBLIC_TEXT_MODE_REDACTED_OCR
    else:
        raise ValidationError(f"{slug}: controlled public_text_mode is missing")

    expected_public_ocr = mode == PUBLIC_TEXT_MODE_REDACTED_OCR
    for label, container in (("index", event), ("manifest", manifest)):
        if "public_ocr_available" in container and (
            container["public_ocr_available"] is not expected_public_ocr
        ):
            raise ValidationError(
                f"{slug}: {label} public_ocr_available conflicts with public_text_mode"
            )
    return mode


def public_text_pdf_copy(
    event: dict[str, Any],
    manifest: dict[str, Any],
) -> tuple[str, dict[str, str]]:
    mode = controlled_public_text_mode(event, manifest)
    return mode, PDF_PUBLIC_TEXT_COPY[mode]


def validate_pdf_public_text_boundary(
    slug: str,
    extracted_text: str,
    mode: str,
) -> None:
    compact = re.sub(r"\s+", " ", extracted_text).strip()
    expected = PDF_PUBLIC_TEXT_COPY[mode]
    for field in ("subtitle", "boundary"):
        if expected[field] not in compact:
            raise ValidationError(
                f"{slug}: public PDF lacks the controlled {mode} {field}"
            )
    other_mode = (
        PUBLIC_TEXT_MODE_MARKERS
        if mode == PUBLIC_TEXT_MODE_REDACTED_OCR
        else PUBLIC_TEXT_MODE_REDACTED_OCR
    )
    if PDF_PUBLIC_TEXT_COPY[other_mode]["subtitle"] in compact:
        raise ValidationError(f"{slug}: public PDF contains a conflicting text-mode label")


def validate_event(event: dict[str, Any], render: bool = True) -> dict[str, Any]:
    slug = event.get("slug")
    if not isinstance(slug, str) or not slug:
        raise ValidationError("Index event lacks slug")
    if event.get("status") not in EXPECTED_STATUSES:
        raise ValidationError(f"{slug}: unexpected status {event.get('status')!r}")
    if event.get("artifact_kind") not in EXPECTED_ARTIFACT_KINDS:
        raise ValidationError(f"{slug}: unexpected artifact_kind")
    if event.get("manual_source_line_verification") is not False:
        raise ValidationError(f"{slug}: manual source-line verification must remain false")

    manifest_path = repo_path(event["manifest"])
    transcript_path = repo_path(event["transcript_source"])
    provenance_path = repo_path(event["provenance_path"])
    redaction_path = repo_path(event["redaction_log_path"])
    public_pdf = repo_path(event["public_pdf"])
    for required in (
        manifest_path,
        transcript_path,
        provenance_path,
        redaction_path,
        public_pdf,
    ):
        if not required.is_file():
            raise ValidationError(f"{slug}: required artifact missing: {required}")

    manifest = load_json(manifest_path)
    if manifest.get("id") != event.get("id") or manifest.get("slug") != slug:
        raise ValidationError(f"{slug}: manifest/index identity mismatch")
    if manifest.get("artifact_kind") not in EXPECTED_ARTIFACT_KINDS:
        raise ValidationError(f"{slug}: manifest artifact_kind mismatch")
    if manifest.get("redacted_facsimile_available") != event.get("redacted_facsimile_available"):
        raise ValidationError(f"{slug}: manifest/index facsimile flag mismatch")
    if manifest.get("source_page_images_available") != event.get("source_page_images_available"):
        raise ValidationError(f"{slug}: manifest/index source-image flag mismatch")
    if manifest.get("complete_public_text") is not False:
        raise ValidationError(
            f"{slug}: manifest complete_public_text must remain false until manual verification"
        )
    public_text_mode, public_text_copy = public_text_pdf_copy(event, manifest)

    _, transcript_pages, transcript_total = parse_transcript(transcript_path)
    source_variant_pages = event.get("source_variant_page_count")
    if transcript_total != source_variant_pages:
        raise ValidationError(
            f"{slug}: transcript source pages {transcript_total} != {source_variant_pages}"
        )
    if len(transcript_pages) != source_variant_pages:
        raise ValidationError(f"{slug}: transcript page body count mismatch")

    public_text = "\n".join(
        (
            transcript_path.read_text(encoding="utf-8"),
            provenance_path.read_text(encoding="utf-8"),
            redaction_path.read_text(encoding="utf-8"),
        )
    )
    privacy = privacy_failures(public_text)
    if privacy:
        raise ValidationError(f"{slug}: public Markdown privacy scan failed: {privacy}")

    reader = PdfReader(str(public_pdf))
    validate_pdf_metadata(public_pdf, reader)
    if str((reader.metadata or {}).get("/Subject", "")) != public_text_copy["subject"]:
        raise ValidationError(f"{slug}: public PDF subject conflicts with public_text_mode")
    pdf_pages = len(reader.pages)
    expected_pdf_pages = event.get("public_pdf_page_count")
    expected_previews = event.get("preview_count")
    if pdf_pages != expected_pdf_pages:
        raise ValidationError(
            f"{slug}: PDF pages {pdf_pages} != index {expected_pdf_pages}"
        )
    if event.get("page_count") != pdf_pages:
        raise ValidationError(f"{slug}: viewer page_count must equal public PDF pages")
    if expected_previews != pdf_pages:
        raise ValidationError(f"{slug}: preview count must equal public PDF pages")
    previews = event.get("preview_pages")
    if not isinstance(previews, list) or len(previews) != pdf_pages:
        raise ValidationError(f"{slug}: preview_pages list/count mismatch")
    preview_dir = repo_path(event["preview_dir"])
    declared_previews = {repo_path(value).resolve() for value in previews}
    actual_previews = {
        path.resolve()
        for path in preview_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".webp", ".jpg", ".jpeg"}
    }
    if not declared_previews.issubset(actual_previews):
        missing = sorted(path.name for path in declared_previews - actual_previews)
        raise ValidationError(
            f"{slug}: declared preview image(s) missing: {missing}"
        )
    current_jpegs = {
        path.resolve()
        for path in preview_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg"}
    }
    if current_jpegs != declared_previews:
        unexpected = sorted(path.name for path in current_jpegs - declared_previews)
        raise ValidationError(
            f"{slug}: unlisted current JPEG preview(s): {unexpected}"
        )
    preview_hashes: list[dict[str, str]] = []
    for preview_value in previews:
        preview = repo_path(preview_value)
        if not preview.is_file():
            raise ValidationError(f"{slug}: missing/invalid preview image: {preview}")
        preview_hashes.append({
            "path": preview_value,
            "sha256": validate_public_image(preview, require_current_jpeg=True),
        })
    preview_hash_status = verify_image_hash_records(
        slug,
        "preview",
        preview_hashes,
        event.get("preview_sha256"),
        manifest["public_artifacts"].get("preview_sha256"),
    )

    actual_pdf_hash = sha256(public_pdf)
    if event.get("public_pdf_sha256") != actual_pdf_hash:
        raise ValidationError(f"{slug}: index PDF hash mismatch")
    if manifest["public_artifacts"].get("pdf_sha256") != actual_pdf_hash:
        raise ValidationError(f"{slug}: manifest PDF hash mismatch")
    if manifest["public_artifacts"].get("pdf_pages") != pdf_pages:
        raise ValidationError(f"{slug}: manifest PDF page count mismatch")
    if manifest["public_artifacts"].get("preview_count") != pdf_pages:
        raise ValidationError(f"{slug}: manifest preview count mismatch")

    extracted = pdf_text(public_pdf)
    privacy = privacy_failures(extracted)
    if privacy:
        raise ValidationError(f"{slug}: public PDF privacy scan failed: {privacy}")
    validate_pdf_public_text_boundary(slug, extracted, public_text_mode)

    rendered_pages = 0
    if render:
        with tempfile.TemporaryDirectory(prefix=f"acta-validate-{slug}-") as tmp:
            prefix = Path(tmp) / "page"
            subprocess.run(
                ["pdftoppm", "-png", "-r", "72", str(public_pdf), str(prefix)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
            pngs = sorted(Path(tmp).glob("page-*.png"))
            rendered_pages = len(pngs)
            if rendered_pages != pdf_pages:
                raise ValidationError(
                    f"{slug}: rendered pages {rendered_pages} != PDF pages {pdf_pages}"
                )
            for png in pngs:
                with Image.open(png) as image:
                    image.verify()
                with Image.open(png) as image:
                    if ImageChops.invert(image.convert("L")).getbbox() is None:
                        raise ValidationError(f"{slug}: blank rendered PDF page: {png.name}")

    if event.get("manual_source_line_verification") is False and event.get("complete_public_text") is not False:
        raise ValidationError(
            f"{slug}: complete_public_text must remain false until manual source-line verification"
        )

    source_facsimile_pages = 0
    facsimile: Path | None = None
    if event.get("redacted_facsimile_available") is True:
        facsimile_value = event.get("redacted_source_facsimile")
        if not isinstance(facsimile_value, str):
            raise ValidationError(f"{slug}: redacted source facsimile path missing")
        facsimile = repo_path(facsimile_value)
        if not facsimile.is_file():
            raise ValidationError(f"{slug}: redacted source facsimile missing")
        source_reader = PdfReader(str(facsimile))
        validate_pdf_metadata(facsimile, source_reader)
        source_facsimile_pages = len(source_reader.pages)
        if source_facsimile_pages != event.get("source_variant_page_count"):
            raise ValidationError(f"{slug}: facsimile/source page mismatch")
        if pdf_text(facsimile).strip():
            raise ValidationError(f"{slug}: facsimile must be raster-only with no hidden text")
        expected_hash = event.get("redacted_source_facsimile_sha256")
        if expected_hash != sha256(facsimile):
            raise ValidationError(f"{slug}: facsimile hash mismatch")
        manifest_facsimile_hash = manifest["public_artifacts"].get(
            "redacted_source_facsimile_sha256"
        )
        if manifest_facsimile_hash != expected_hash:
            raise ValidationError(f"{slug}: manifest/index facsimile hash mismatch")

    source_hashes: list[dict[str, str]] = []
    source_image_paths: list[Path] = []
    source_hash_status = "not-applicable"
    facsimile_equivalent_pages = 0
    if event.get("source_page_images_available") is True:
        source_previews = event.get("source_preview_pages")
        if not isinstance(source_previews, list):
            raise ValidationError(f"{slug}: source preview list missing")
        if len(source_previews) != event.get("source_variant_page_count"):
            raise ValidationError(f"{slug}: source preview/source page mismatch")
        source_preview_dir_value = event.get("source_preview_dir")
        if not isinstance(source_preview_dir_value, str):
            raise ValidationError(f"{slug}: source preview directory missing")
        source_preview_dir = repo_path(source_preview_dir_value)
        if not source_preview_dir.is_dir():
            raise ValidationError(f"{slug}: source preview directory missing")
        declared_source_images = {
            repo_path(value).resolve()
            for value in source_previews
        }
        current_source_jpegs = {
            path.resolve()
            for path in source_preview_dir.iterdir()
            if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg"}
        }
        if current_source_jpegs != declared_source_images:
            unexpected = sorted(
                path.name for path in current_source_jpegs - declared_source_images
            )
            raise ValidationError(
                f"{slug}: unlisted current source JPEG(s): {unexpected}"
            )
        for preview_value in source_previews:
            preview = repo_path(preview_value)
            if not preview.is_file():
                raise ValidationError(f"{slug}: source preview missing/invalid: {preview}")
            source_image_paths.append(preview)
            source_hashes.append({
                "path": preview_value,
                "sha256": validate_public_image(preview, require_current_jpeg=True),
            })
        source_hash_status = verify_image_hash_records(
            slug,
            "source-preview",
            source_hashes,
            event.get("source_preview_sha256"),
            manifest["public_artifacts"].get("source_preview_sha256"),
        )
        if facsimile is not None:
            facsimile_equivalent_pages = validate_facsimile_source_equivalence(
                slug,
                facsimile,
                source_image_paths,
            )

    return {
        "slug": slug,
        "source_variant_pages": source_variant_pages,
        "public_pdf_pages": pdf_pages,
        "previews": expected_previews,
        "rendered_pages": rendered_pages,
        "pdf_sha256": actual_pdf_hash,
        "privacy_scan": "pass",
        "source_facsimile_pages": source_facsimile_pages,
        "preview_jpeg_hashes": preview_hash_status,
        "source_preview_jpeg_hashes": source_hash_status,
        "facsimile_source_equivalent_pages": facsimile_equivalent_pages,
        "public_image_metadata_scan": "pass",
        "public_text_mode": public_text_mode,
    }


def validate_command(args: argparse.Namespace) -> int:
    events = selected_events(args.slug)
    reports = [validate_event(event, render=not args.skip_render) for event in events]
    private_reports = validate_private_source_map(args.source_map, events)
    print(
        json.dumps(
            {
                "status": "pass",
                "packages": reports,
                "private_source_checks": private_reports,
                "repository_writes": False,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def register_fonts() -> tuple[str, str]:
    regular_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    bold_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    if not regular_path.is_file() or not bold_path.is_file():
        raise ValidationError("Required DejaVu Sans fonts are unavailable")
    if "ActaSans" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("ActaSans", str(regular_path)))
    if "ActaSans-Bold" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("ActaSans-Bold", str(bold_path)))
    return "ActaSans", "ActaSans-Bold"


def pdf_header_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("ActaSans", 7)
    canvas.setFillColor(colors.HexColor("#51616B"))
    canvas.drawString(18 * mm, 10 * mm, "Project Sun Rock - edición pública redactada")
    canvas.drawRightString(192 * mm, 10 * mm, f"Página PDF {doc.page}")
    canvas.restoreState()


def make_pdf(
    event: dict[str, Any],
    manifest: dict[str, Any],
    pages: list[str],
    out_pdf: Path,
) -> None:
    rl_config.invariant = 1
    regular, bold = register_fonts()
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleActa",
        parent=styles["Title"],
        fontName=bold,
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#17313D"),
        alignment=TA_LEFT,
        spaceAfter=10,
    )
    subtitle = ParagraphStyle(
        "SubtitleActa",
        parent=styles["Normal"],
        fontName=regular,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#425964"),
        spaceAfter=9,
    )
    h2 = ParagraphStyle(
        "H2Acta",
        parent=styles["Heading2"],
        fontName=bold,
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#164F66"),
        spaceBefore=6,
        spaceAfter=7,
    )
    body = ParagraphStyle(
        "BodyActa",
        parent=styles["BodyText"],
        fontName=regular,
        fontSize=8.4,
        leading=11.4,
        textColor=colors.HexColor("#16262D"),
        alignment=TA_LEFT,
        spaceAfter=5,
    )
    redact = ParagraphStyle(
        "RedactActa",
        parent=body,
        fontName=bold,
        textColor=colors.HexColor("#8A2E2E"),
        backColor=colors.HexColor("#FFF2EF"),
        borderColor=colors.HexColor("#E1B5AD"),
        borderWidth=0.5,
        borderPadding=5,
        spaceBefore=4,
        spaceAfter=6,
    )
    small = ParagraphStyle(
        "SmallActa",
        parent=body,
        fontSize=7.4,
        leading=10,
        textColor=colors.HexColor("#53636B"),
    )

    source = manifest["source"]
    _, mode_copy = public_text_pdf_copy(event, manifest)
    doc = SimpleDocTemplate(
        str(out_pdf),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=17 * mm,
        title=f"{event['id']} - edición pública redactada",
        author="Project Sun Rock",
        subject=mode_copy["subject"],
    )
    story = [
        Paragraph(event["title_es"], title),
        Paragraph(mode_copy["subtitle"], subtitle),
        Spacer(1, 4 * mm),
        Table(
            [
                ["ID", event["id"]],
                ["Órgano", event["body"]],
                ["Fecha", event["date"]],
                ["Páginas fuente", str(event["source_variant_page_count"])],
                ["SHA-256 fuente", source["sha256"]],
            ],
            colWidths=[34 * mm, 130 * mm],
            style=TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, -1), regular),
                    ("FONTNAME", (0, 0), (0, -1), bold),
                    ("FONTSIZE", (0, 0), (-1, -1), 7.6),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#164F66")),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F3F7F8")),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C9D6DA")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            ),
        ),
        Spacer(1, 5 * mm),
        Paragraph("Advertencia", h2),
        Paragraph(mode_copy["boundary"], body),
        Paragraph(f"Control de variante: {source['variant_note_es']}", small),
        PageBreak(),
    ]

    for index, page_text in enumerate(pages, start=1):
        story.append(
            KeepTogether(
                [
                    Paragraph(
                        f"Página fuente {index} de {len(pages)}",
                        h2,
                    ),
                    Paragraph(f"Copia: {source['filename']}", small),
                ]
            )
        )
        for block in re.split(r"\n\s*\n", page_text):
            block = block.strip()
            if not block:
                continue
            safe = (
                block.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br/>")
            )
            story.append(Paragraph(safe, redact if block.startswith("[") else body))
        if index < len(pages):
            story.append(PageBreak())
    doc.build(story, onFirstPage=pdf_header_footer, onLaterPages=pdf_header_footer)


def make_previews(pdf_path: Path, preview_dir: Path) -> list[str]:
    if fitz.VersionBind != PYMUPDF_VERSION:
        raise ValidationError(
            f"Pinned PyMuPDF {PYMUPDF_VERSION} is required for deterministic "
            f"preview rendering; found {fitz.VersionBind}"
        )
    preview_dir = preview_dir.resolve()
    try:
        preview_dir.relative_to(PREVIEW_ROOT.resolve())
    except ValueError as exc:
        raise ValidationError(f"Refusing preview output outside expected root: {preview_dir}") from exc
    preview_dir.mkdir(parents=True, exist_ok=True)
    # Current JPEG previews are deterministically replaced, while the legacy
    # WEBP derivatives remain as separately identified historical outputs.
    # Removing the directory here would silently reduce the published corpus.
    for existing in preview_dir.iterdir():
        if existing.is_file() and existing.suffix.lower() in {".jpg", ".jpeg"}:
            existing.unlink()
    matrix = fitz.Matrix(105 / 72, 105 / 72)
    try:
        document = fitz.open(pdf_path)
    except Exception as exc:
        raise ValidationError(f"Cannot open generated PDF for previews: {pdf_path}") from exc
    try:
        outputs: list[str] = []
        for number, page in enumerate(document, start=1):
            output = preview_dir / f"page-{number:03d}.jpg"
            pixmap = page.get_pixmap(
                matrix=matrix,
                colorspace=fitz.csRGB,
                alpha=False,
                annots=True,
            )
            current = Image.frombytes(
                "RGB",
                (pixmap.width, pixmap.height),
                pixmap.samples,
            )
            try:
                current.info.clear()
                current.save(output, "JPEG", quality=82, optimize=True, progressive=True)
            finally:
                current.close()
            outputs.append(output.relative_to(REPO).as_posix())
        return outputs
    finally:
        document.close()


def build_event(event: dict[str, Any]) -> dict[str, Any]:
    slug = event["slug"]
    manifest_path = repo_path(event["manifest"])
    manifest = load_json(manifest_path)
    transcript_path = repo_path(event["transcript_source"])
    _, pages, source_total = parse_transcript(transcript_path)
    if source_total != event["source_variant_page_count"]:
        raise ValidationError(f"{slug}: transcript/index source-page mismatch")

    output_pdf = repo_path(event["public_pdf"])
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    make_pdf(event, manifest, pages, output_pdf)
    pdf_count = len(PdfReader(str(output_pdf)).pages)
    preview_dir = repo_path(event["preview_dir"])
    previews = make_previews(output_pdf, preview_dir)
    if len(previews) != pdf_count:
        raise ValidationError(f"{slug}: preview render count mismatch after build")
    preview_hashes = [
        {"path": value, "sha256": sha256(repo_path(value))}
        for value in previews
    ]

    pdf_hash = sha256(output_pdf)
    manifest["public_pdf_page_count"] = pdf_count
    manifest["public_artifacts"]["pdf_sha256"] = pdf_hash
    manifest["public_artifacts"]["pdf_pages"] = pdf_count
    manifest["public_artifacts"]["preview_pages"] = previews
    manifest["public_artifacts"]["preview_count"] = len(previews)
    manifest["public_artifacts"]["preview_sha256"] = preview_hashes
    manifest["quality_control"]["pdf_reopened"] = True
    manifest["quality_control"]["all_pdf_pages_rendered"] = True
    manifest["quality_control"]["preview_hashes_recorded"] = True
    manifest["quality_control"]["preview_current_format"] = "JPEG"
    manifest["quality_control"]["legacy_webp_derivatives_separate"] = True
    manifest["quality_control"]["public_pdf_deterministic_invariant"] = True
    write_json(manifest_path, manifest)

    event["public_pdf_sha256"] = pdf_hash
    event["public_pdf_page_count"] = pdf_count
    event["page_count"] = pdf_count
    event["preview_pages"] = previews
    event["preview_count"] = len(previews)
    event["preview_sha256"] = preview_hashes
    return event


def build_command(args: argparse.Namespace) -> int:
    index, events = load_index()
    selected = {event["slug"] for event in selected_events(args.slug)}
    rebuilt: list[dict[str, Any]] = []
    updated_events: list[dict[str, Any]] = []
    for event in events:
        if event["slug"] in selected:
            event = build_event(dict(event))
            rebuilt.append(event)
        updated_events.append(event)
    index["events"] = updated_events
    index["items"] = updated_events
    write_json(INDEX_PATH, index)

    reports = [validate_event(event, render=True) for event in rebuilt]
    print(
        json.dumps(
            {
                "status": "pass",
                "rebuilt": reports,
                "artifact_kinds": sorted(EXPECTED_ARTIFACT_KINDS),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate without repository writes")
    validate.add_argument("--slug", action="append", help="Validate only this slug; repeatable")
    validate.add_argument(
        "--source-map",
        type=Path,
        help=(
            "Optional private JSON object mapping slug to a PDF/DOCX path or typed "
            "source-control object; never persisted"
        ),
    )
    validate.add_argument(
        "--skip-render",
        action="store_true",
        help="Skip temporary Poppler render; other PDF/preview checks still run",
    )
    validate.set_defaults(func=validate_command)

    build = sub.add_parser("build", help="Rebuild public PDFs/previews from public transcripts")
    choice = build.add_mutually_exclusive_group(required=True)
    choice.add_argument("--all", action="store_true", help="Rebuild every indexed package")
    choice.add_argument("--slug", action="append", help="Rebuild this slug; repeatable")
    build.set_defaults(func=build_command)
    return cli


def main() -> int:
    args = parser().parse_args()
    if getattr(args, "all", False):
        args.slug = None
    try:
        return args.func(args)
    except (ValidationError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Rebuild and validate the public-redacted ACTA document packages.

This script deliberately contains no native-source or private filesystem paths.
The versioned, public-redacted ``transcript-es.md`` files are the build inputs for
the public text-edition PDFs and WEBP previews.  An optional private source map may
be supplied at validation time to verify source hashes and page counts without
copying or persisting those paths.

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
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageChops
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


def webp_has_content(path: Path) -> bool:
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        gray = image.convert("L")
        inverted = ImageChops.invert(gray)
        return inverted.getbbox() is not None


def pdf_text(path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", str(path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def validate_private_source_map(
    source_map_path: Path | None,
    events: list[dict[str, Any]],
) -> list[str]:
    if source_map_path is None:
        return []
    source_map = load_json(source_map_path)
    messages: list[str] = []
    for event in events:
        slug = event["slug"]
        value = source_map.get(slug)
        if value is None:
            messages.append(f"{slug}: private source not supplied; skipped")
            continue
        source_path = Path(value).expanduser()
        if not source_path.is_file():
            raise ValidationError(f"{slug}: private source does not exist: {source_path}")
        manifest = load_json(repo_path(event["manifest"]))
        expected_hash = manifest["source"]["sha256"]
        expected_pages = manifest["source_variant_page_count"]
        actual_hash = sha256(source_path)
        actual_pages = len(PdfReader(str(source_path)).pages)
        if actual_hash != expected_hash:
            raise ValidationError(
                f"{slug}: private source hash mismatch: {actual_hash} != {expected_hash}"
            )
        if actual_pages != expected_pages:
            raise ValidationError(
                f"{slug}: private source page mismatch: {actual_pages} != {expected_pages}"
            )
        messages.append(f"{slug}: private source hash/pages verified")
    return messages


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
    for preview_value in previews:
        preview = repo_path(preview_value)
        if preview.suffix.lower() not in {".webp", ".jpg", ".jpeg"} or not preview.is_file():
            raise ValidationError(f"{slug}: missing/invalid preview image: {preview}")
        if not webp_has_content(preview):
            raise ValidationError(f"{slug}: blank WEBP preview: {preview}")

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
    if event.get("redacted_facsimile_available") is True:
        facsimile_value = event.get("redacted_source_facsimile")
        if not isinstance(facsimile_value, str):
            raise ValidationError(f"{slug}: redacted source facsimile path missing")
        facsimile = repo_path(facsimile_value)
        if not facsimile.is_file():
            raise ValidationError(f"{slug}: redacted source facsimile missing")
        source_reader = PdfReader(str(facsimile))
        source_facsimile_pages = len(source_reader.pages)
        if source_facsimile_pages != event.get("source_variant_page_count"):
            raise ValidationError(f"{slug}: facsimile/source page mismatch")
        if pdf_text(facsimile).strip():
            raise ValidationError(f"{slug}: facsimile must be raster-only with no hidden text")
        expected_hash = event.get("redacted_source_facsimile_sha256")
        if expected_hash != sha256(facsimile):
            raise ValidationError(f"{slug}: facsimile hash mismatch")

    if event.get("source_page_images_available") is True:
        source_previews = event.get("source_preview_pages")
        if not isinstance(source_previews, list):
            raise ValidationError(f"{slug}: source preview list missing")
        if len(source_previews) != event.get("source_variant_page_count"):
            raise ValidationError(f"{slug}: source preview/source page mismatch")
        for preview_value in source_previews:
            preview = repo_path(preview_value)
            if not preview.is_file() or preview.suffix.lower() not in {".webp", ".jpg", ".jpeg"}:
                raise ValidationError(f"{slug}: source preview missing/invalid: {preview}")
            if not webp_has_content(preview):
                raise ValidationError(f"{slug}: blank source preview: {preview}")

    return {
        "slug": slug,
        "source_variant_pages": source_variant_pages,
        "public_pdf_pages": pdf_pages,
        "previews": expected_previews,
        "rendered_pages": rendered_pages,
        "pdf_sha256": actual_pdf_hash,
        "privacy_scan": "pass",
        "source_facsimile_pages": source_facsimile_pages,
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
    doc = SimpleDocTemplate(
        str(out_pdf),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=17 * mm,
        title=f"{event['id']} - edición pública redactada",
        author="Project Sun Rock",
        subject="ACTA public redacted text edition",
    )
    story = [
        Paragraph(event["title_es"], title),
        Paragraph("Edición pública redactada y OCR-asistida", subtitle),
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
        Paragraph(
            "No es el original, el libro diligenciado, una copia certificada ni una "
            "transcripción pericial. Todas las páginas de la copia usada están "
            "secuenciadas; los datos privados y reservados se sustituyen por "
            "marcadores expresos.",
            body,
        ),
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
    preview_dir = preview_dir.resolve()
    try:
        preview_dir.relative_to(PREVIEW_ROOT.resolve())
    except ValueError as exc:
        raise ValidationError(f"Refusing preview output outside expected root: {preview_dir}") from exc
    if preview_dir.exists():
        shutil.rmtree(preview_dir)
    preview_dir.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix="acta-public-preview-") as tmp:
        prefix = Path(tmp) / "page"
        subprocess.run(
            ["pdftoppm", "-png", "-r", "105", str(pdf_path), str(prefix)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        outputs: list[str] = []
        for number, png in enumerate(sorted(Path(tmp).glob("page-*.png")), start=1):
            output = preview_dir / f"page-{number:03d}.jpg"
            with Image.open(png) as image:
                image.convert("RGB").save(output, "JPEG", quality=82, optimize=True, progressive=True)
            outputs.append(output.relative_to(REPO).as_posix())
        return outputs


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

    pdf_hash = sha256(output_pdf)
    manifest["public_pdf_page_count"] = pdf_count
    manifest["public_artifacts"]["pdf_sha256"] = pdf_hash
    manifest["public_artifacts"]["pdf_pages"] = pdf_count
    manifest["public_artifacts"]["preview_pages"] = previews
    manifest["public_artifacts"]["preview_count"] = len(previews)
    manifest["quality_control"]["pdf_reopened"] = True
    manifest["quality_control"]["all_pdf_pages_rendered"] = True
    write_json(manifest_path, manifest)

    event["public_pdf_sha256"] = pdf_hash
    event["public_pdf_page_count"] = pdf_count
    event["page_count"] = pdf_count
    event["preview_pages"] = previews
    event["preview_count"] = len(previews)
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
        help="Optional private JSON object mapping slug to source-PDF path; never persisted",
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

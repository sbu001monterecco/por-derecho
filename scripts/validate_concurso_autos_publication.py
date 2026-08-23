#!/usr/bin/env python3
"""Validate the dedicated Concurso 36/2012 Autos/full-text publication."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import fitz


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "assets/data/concurso36-autos-fulltext-v1.json"
FULL_ROOT = ROOT / "evidence/insolvency-36-2012/concurso-autos/full-text"
ES_PATH = ROOT / "es/concurso-36-2012-autos-resoluciones/index.html"
EN_PATH = ROOT / "en/insolvency-36-2012-orders-decisions/index.html"
PROVENANCE_PATH = ROOT / "evidence/insolvency-36-2012/ac-removal-fees/provenance.md"
UNITARY_PATH = ROOT / "archive/CONCURSO36_AUTOS_FULLTEXT_UNITARY_RECORD_23AUG2026.md"
WHOLE_FILE_PROMPT_PATH = ROOT / "archive/prompts/CONCURSO36_COMPLETE_JUDICIAL_PARTY_RECORD_ACQUISITION_DIGITISATION_PUBLICATION_PROMPT_23AUG2026.md"

PDF_SPECS = {
    "evidence/insolvency-36-2012/ac-removal-fees/auto-1377-2025-removal-public-redacted.pdf": (3, "a19975991ddf5aceb17f95247d05c7a7cd115bf9cd4ce6e7b3c7f127aeeba5b7"),
    "evidence/insolvency-36-2012/ac-removal-fees/auto-11nov2025-reconsideration-public-redacted.pdf": (4, "da1fc63c666cf20167d1075dbc06e85afd66fc985a8c9255507b7364c1358220"),
    "evidence/insolvency-36-2012/concurso-autos/public-pdfs/laj-28abr2025-traslado-separacion-public-redacted.pdf": (1, "051a06dcd025b0cad795b27828b697bf0d9dcae11e5db4a8ad071b5ec034c49c"),
    "evidence/insolvency-36-2012/concurso-autos/public-pdfs/laj-20may2025-puesta-a-resolver-public-redacted.pdf": (1, "9270af9e90950003ab48903e30a98e1c1a4abfa7e4790ab067cc681b6c658204"),
    "evidence/insolvency-36-2012/concurso-autos/public-pdfs/auto-12sep2025-aclaracion-providencia-public-redacted.pdf": (2, "93a0adef54dd3723b0f459a96f69a4951d73b0b0adf0fe7e6c96eb65011ddfb4"),
    "evidence/insolvency-36-2012/concurso-autos/public-pdfs/auto-223-2026-acumulacion-public-redacted.pdf": (4, "5c7238860f599acc46492c8d255f23a07d71c7d7baefd5242f97894ece518fe5"),
    "evidence/insolvency-36-2012/concurso-autos/public-pdfs/decreto-113-2024-inhibicion-public-redacted.pdf": (2, "6e6d92c2c004f8101bed2335beed2a56139747d4120371e32c1d91e6486eebb8"),
    "evidence/insolvency-36-2012/concurso-autos/public-pdfs/decreto-28nov2024-admision-honorarios-public-redacted.pdf": (2, "35a598c84620cb9ab2b450894e88be206e35c8255d887448486041abed883ddd"),
    "evidence/insolvency-36-2012/concurso-autos/public-pdfs/sentencia-4-2026-honorarios-public-redacted.pdf": (5, "5f2377f91b5b1b6d3fbdc38c00b7b68523a7677ad9b9d7f2cb50ce04c89f9653"),
    "evidence/insolvency-36-2012/concurso-autos/public-pdfs/decreto-21ene2026-no-aclaracion-public-redacted.pdf": (2, "880f46de585bfa9251416eae7d693f73bfdaa0adfa8dbaf9ddef0a147d2c4773"),
}

PRIVACY_PATTERNS = {
    "email address": r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    "Spanish DNI/NIE/NIF": r"\b(?:[XYZ]\d{7}[A-Z]|\d{8}[A-Z]|[A-Z]\d{8})\b",
    "Spanish mobile": r"(?<!\d)(?:\+34\s*)?[67]\d{8}(?!\d)",
    "labelled telephone contact": r"\b(?:Tel(?:[eé]fono)?|M[oó]vil|Fax)\.?\s*:?\s*(?:\+?34[ .-]*)?(?:\d[ .()-]*){8,11}",
    "UK mobile": r"(?<!\d)(?:\+44|0044)\s*\d(?:[\s()-]*\d){8,11}(?!\d)",
    "NIG/IUP": r"\b(?:NIG|IUP)\s*:",
    "court verification code": r"A05003250|sede\.justiciaencanarias\.es/sede/tramites-comprobacion",
    "electronic-signature metadata": r"Firmado digitalmente por\b|^\s*Firmado por\b|NOMBRE\s+[A-ZÁÉÍÓÚÜÑ ]+\s+-\s+NIF",
    "masked personal identifier": r"\*{2,}\d{2,}\*{2,}",
    "signature certificate tail": r"\b(?:FNMT Usuarios|certificado emitido por ACA)\b",
    "unnecessary published postal address": r"Paseo de la Castellana\s*(?:n[ºo]\s*)?4|calle Hero\s+12-1",
    "IBAN": r"\bES\d{2}(?:[ -]?\d){20}\b",
}

errors: list[str] = []


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.ids: list[str] = []
        self.details = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.append(str(data["id"]))
        if tag == "a" and data.get("href"):
            self.hrefs.append(str(data["href"]))
        if tag == "details" and "decision" in str(data.get("class", "")).split():
            self.details += 1


def read(path: Path) -> str:
    if not path.is_file():
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def require(path: Path, text: str, markers: list[str]) -> None:
    for marker in markers:
        if marker not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing marker {marker!r}")


try:
    manifest = json.loads(read(MANIFEST_PATH))
except Exception as exc:
    errors.append(f"manifest JSON invalid: {exc}")
    manifest = {"documents": []}

documents = manifest.get("documents", [])
if manifest.get("schema") != "concurso36-autos-fulltext-v1":
    errors.append("manifest: wrong schema")
if manifest.get("cutoff") != "2026-08-23":
    errors.append("manifest: wrong cut-off")
for marker in (
    "20 January 2026 preliminary hearing",
    "certified chronological docket/index",
):
    if not any(marker in gap for gap in manifest.get("known_gaps", [])):
        errors.append(f"manifest known_gaps: missing {marker!r}")
if len(documents) != 50:
    errors.append(f"manifest: expected 50 records, found {len(documents)}")

ids = [record.get("id") for record in documents]
if len(ids) != len(set(ids)):
    errors.append("manifest: duplicate record IDs")
expected_ids = {f"R{number:02d}" for number in range(1, 33)} | {f"F{number:02d}" for number in range(1, 19)}
if set(ids) != expected_ids:
    errors.append(f"manifest: ID set mismatch; missing={sorted(expected_ids - set(ids))}, extra={sorted(set(ids) - expected_ids)}")

court = [record for record in documents if record.get("record_class") == "court"]
party = [record for record in documents if record.get("record_class") == "party"]
if (len(court), len(party)) != (25, 25):
    errors.append(f"manifest: expected 25 court / 25 party records, found {len(court)} / {len(party)}")
if sum(record.get("lane") == "separacion" for record in documents) != 32:
    errors.append("manifest: removal lane must contain 32 records")
if sum(record.get("lane") == "honorarios" for record in documents) != 18:
    errors.append("manifest: remuneration lane must contain 18 records")
if sum(bool(record.get("public_pdf")) for record in documents) != 10:
    errors.append("manifest: exactly ten records must expose public PDFs")

manifest_hrefs: set[str] = set()
for record in documents:
    rel = record.get("href", "")
    if not rel:
        errors.append(f"manifest {record.get('id')}: missing href")
        continue
    manifest_hrefs.add(rel)
    path = FULL_ROOT / rel
    text = read(path)
    require(
        path,
        text,
        [
            f"**ID documental:** {record.get('id')}",
            f"**SHA-256 de la fuente controlada:** `{record.get('source_sha256')}`",
            "## Texto íntegro redactado",
            "Alegaciones de parte no equivalen a hechos probados",
        ],
    )
    text_blocks = re.findall(r"```text\n(.*?)\n```", text, flags=re.S)
    if len(text_blocks) != record.get("source_pages_or_units"):
        errors.append(
            f"{path.relative_to(ROOT)}: expected {record.get('source_pages_or_units')} "
            f"page/unit text blocks, found {len(text_blocks)}"
        )
    if not text_blocks or any(not block.strip() for block in text_blocks):
        errors.append(f"{path.relative_to(ROOT)}: empty or missing text block")
    privacy_text = re.sub(r"`[0-9a-f]{64}`", "", text, flags=re.I)
    for label, pattern in PRIVACY_PATTERNS.items():
        if re.search(pattern, privacy_text, flags=re.I | re.M):
            errors.append(f"{path.relative_to(ROOT)}: possible {label} leakage")

actual_transcripts = {path.name for path in FULL_ROOT.glob("[RF][0-9][0-9]-*.md")}
if actual_transcripts != manifest_hrefs:
    errors.append(
        f"full-text directory/manifest mismatch: unlisted={sorted(actual_transcripts - manifest_hrefs)}, missing={sorted(manifest_hrefs - actual_transcripts)}"
    )

for rel, (expected_pages, expected_hash) in PDF_SPECS.items():
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing public PDF: {rel}")
        continue
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual_hash != expected_hash:
        errors.append(f"{rel}: SHA-256 mismatch {actual_hash}")
    doc = fitz.open(path)
    if doc.page_count != expected_pages:
        errors.append(f"{rel}: expected {expected_pages} pages, found {doc.page_count}")
    if doc.is_form_pdf:
        errors.append(f"{rel}: contains AcroForm data")
    if doc.get_xml_metadata():
        errors.append(f"{rel}: contains XML metadata")
    for page_number, page in enumerate(doc, start=1):
        if page.get_text().strip():
            errors.append(f"{rel}: page {page_number} contains a searchable text layer")
        if page.first_annot is not None:
            errors.append(f"{rel}: page {page_number} contains annotations")
        if not page.get_images(full=True):
            errors.append(f"{rel}: page {page_number} has no raster image")
    doc.close()

es = read(ES_PATH)
en = read(EN_PATH)
require(
    ES_PATH,
    es,
    [
        "Autos, decisiones y escritos localizados del Concurso 36/2012",
        "50</strong><span>piezas especialistas digitizadas",
        "25</strong><span>actos judiciales / LAJ",
        "La solicitud de separación y la demanda de honorarios fueron desestimadas en primera instancia por legitimación activa",
        "Texto íntegro de Juez, Sala y LAJ",
        "Lo que falta se registra; no se inventa",
        "Derecho de respuesta y corrección",
    ],
)
require(
    EN_PATH,
    en,
    [
        "Located orders, decisions and filings in Insolvency 36/2012",
        "50</strong><span>digitised specialist records",
        "25</strong><span>court / LAJ acts",
        "The removal application and the remuneration claim were dismissed at first instance on active-standing grounds",
        "Complete Judge, Appeal Court and LAJ text",
        "Missing material is logged, not invented",
        "Right of response and correction",
    ],
)

for path, text in ((ES_PATH, es), (EN_PATH, en)):
    parser = PageParser()
    parser.feed(text)
    if parser.details != 25:
        errors.append(f"{path.relative_to(ROOT)}: expected 25 decision details, found {parser.details}")
    if not {record["id"] for record in court}.issubset(parser.ids):
        errors.append(f"{path.relative_to(ROOT)}: missing court decision anchors")
    transcript_links = {Path(urlsplit(href).path).name for href in parser.hrefs if href.endswith("-redacted.md")}
    if transcript_links != manifest_hrefs:
        errors.append(f"{path.relative_to(ROOT)}: does not link all 50 unique transcripts")
    pdf_links = {href for href in parser.hrefs if href.endswith(".pdf")}
    if len(pdf_links) != 10:
        errors.append(f"{path.relative_to(ROOT)}: expected 10 unique public-PDF links, found {len(pdf_links)}")
    for href in parser.hrefs:
        parts = urlsplit(href)
        if parts.scheme or parts.netloc or href.startswith("#"):
            continue
        target = (path.parent / unquote(parts.path)).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: link escapes repository: {href}")
            continue
        if parts.path.endswith("/"):
            target = target / "index.html"
        if not target.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken link {href}")
    for label, pattern in PRIVACY_PATTERNS.items():
        if re.search(pattern, text, flags=re.I):
            errors.append(f"{path.relative_to(ROOT)}: possible {label} leakage")

provenance = read(PROVENANCE_PATH)
unitary = read(UNITARY_PATH)
require(PROVENANCE_PATH, provenance, ["50 redacted full-text records", "Ten generated public PDFs", "Known gaps"] + [spec[1] for spec in PDF_SPECS.values()])
require(
    UNITARY_PATH,
    unitary,
    [
        "50 complete redacted transcriptions",
        "## 2. Controlling procedural distinction",
        "## 4. Decision matrix",
        "## 7. Known gaps at the cut-off",
        "No public text may say that the court found the remuneration lawful or unlawful",
        "Whole-file continuation",
        str(WHOLE_FILE_PROMPT_PATH.relative_to(ROOT)),
    ],
)

whole_file_prompt = read(WHOLE_FILE_PROMPT_PATH)
require(
    WHOLE_FILE_PROMPT_PATH,
    whole_file_prompt,
    [
        "complete Concurso 36/2012 judicial and party record",
        "AUDIT_ACQUIRE_DIGITISE_PREPARE",
        "PUBLISH_PUBLIC_SAFE",
        "derive the expected denominator",
        "Communications by parties",
        "Authorisation ≠ implementation",
        "CERTIFIED_COURT_COPY",
        "Public/private and privilege boundary",
        "Existing public archive: extend, do not duplicate",
        "Current P0 source demands",
        "Validation and release gate",
        "Never claim the file is complete until a certified court index has been reconciled record by record",
        "The prompt does not authorise sending, resending, forwarding or self-emailing any message",
    ],
)

for rel, markers in {
    "CHATGPT_START_HERE.md": [str(WHOLE_FILE_PROMPT_PATH.relative_to(ROOT)), "31. For **any request to obtain"],
    "archive/CHATGPT_PROMPT_LIBRARY.md": [str(WHOLE_FILE_PROMPT_PATH.relative_to(ROOT)), "## P25 — Complete Concurso 36/2012 judicial and party record"],
    "archive/CONTINUOUS_MAINTENANCE_MATRIX.md": [str(WHOLE_FILE_PROMPT_PATH.relative_to(ROOT)), "Complete Concurso 36/2012 judicial and party record"],
}.items():
    path = ROOT / rel
    require(path, read(path), markers)

route_pairs = (
    "/es/concurso-36-2012-autos-resoluciones/",
    "/en/insolvency-36-2012-orders-decisions/",
)
for sitemap_rel in ("sitemap.xml", "sitemap-unitary-shell.xml"):
    path = ROOT / sitemap_rel
    try:
        ET.parse(path)
    except Exception as exc:
        errors.append(f"{sitemap_rel}: invalid XML: {exc}")
        continue
    text = read(path)
    for route in route_pairs:
        if route not in text:
            errors.append(f"{sitemap_rel}: missing {route}")

registry_path = ROOT / "assets/data/unitary-route-registry-v1.json"
try:
    registry = json.loads(read(registry_path))
except Exception as exc:
    errors.append(f"route registry invalid JSON: {exc}")
    registry = []
registry_paths = {"/" + item.get("path", "") for item in registry}
for route in route_pairs:
    if route not in registry_paths:
        errors.append(f"route registry: missing {route}")

discovery = {
    "es/indice-web/index.html": ["Autos y resoluciones · texto íntegro", "../concurso-36-2012-autos-resoluciones/"],
    "en/site-index/index.html": ["Orders and decisions · full text", "../insolvency-36-2012-orders-decisions/"],
    "es/concurso-36-2012-separacion-ac-honorarios/index.html": ["50 piezas", "../concurso-36-2012-autos-resoluciones/"],
    "en/insolvency-36-2012-administrator-removal-fees/index.html": ["50 items", "../insolvency-36-2012-orders-decisions/"],
    "README.md": [route_pairs[0], route_pairs[1]],
}
for rel, markers in discovery.items():
    path = ROOT / rel
    require(path, read(path), markers)

register_path = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
with register_path.open(encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.reader(handle))
if not rows:
    errors.append("PROCEEDINGS_MASTER_REGISTER.csv: empty")
else:
    width = len(rows[0])
    for number, row in enumerate(rows, start=1):
        if len(row) != width:
            errors.append(f"PROCEEDINGS_MASTER_REGISTER.csv:{number}: {len(row)} columns; expected {width}")
    joined = "\n".join(",".join(row) for row in rows)
    for marker in ("GC-APP-007", "GC-CIV-027", "GC-APP-028", "PUBLIC_FULLTEXT_REDACTED_WITH_KEY_PDFS"):
        if marker not in joined:
            errors.append(f"PROCEEDINGS_MASTER_REGISTER.csv: missing {marker}")

if errors:
    print("concurso-autos validation: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("concurso-autos validation: PASS")

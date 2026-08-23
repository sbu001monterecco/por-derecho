#!/usr/bin/env python3
"""Validate the AC removal, remuneration and judicial-order publication."""

from __future__ import annotations

import csv
import hashlib
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
ES_REL = "es/concurso-36-2012-separacion-ac-honorarios/index.html"
EN_REL = "en/insolvency-36-2012-administrator-removal-fees/index.html"
DIGEST_REL = "archive/AC_SEPARATION_FEES_AUTOS_DP1901_REFERENCE22_UNITARY_DIGEST_23AUG2026.md"
PROVENANCE_REL = "evidence/insolvency-36-2012/ac-removal-fees/provenance.md"
PDF_SPECS = {
    "evidence/insolvency-36-2012/ac-removal-fees/auto-1377-2025-removal-public-redacted.pdf": (
        3,
        "a19975991ddf5aceb17f95247d05c7a7cd115bf9cd4ce6e7b3c7f127aeeba5b7",
    ),
    "evidence/insolvency-36-2012/ac-removal-fees/auto-11nov2025-reconsideration-public-redacted.pdf": (
        4,
        "da1fc63c666cf20167d1075dbc06e85afd66fc985a8c9255507b7364c1358220",
    ),
}

errors: list[str] = []


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing file: {rel}")
        return ""
    return path.read_text(encoding="utf-8")


def require(rel: str, text: str, markers: list[str]) -> None:
    for marker in markers:
        if marker not in text:
            errors.append(f"{rel}: missing marker {marker!r}")


es = read(ES_REL)
en = read(EN_REL)
digest = read(DIGEST_REL)
provenance = read(PROVENANCE_REL)

require(
    ES_REL,
    es,
    [
        "Separación, honorarios y control integral del Administrador Concursal",
        "23 abril 2025 · 58 páginas",
        "110.956,97 € para la masa",
        "Auto 1377/2025 · PDF",
        "Abrir Autos y resoluciones",
        "sin necesidad de entrar en los motivos de fondo",
        "RPL 3304/2025",
        "RPL 3319/2025",
        "Disposición Transitoria Tercera de la Ley 25/2015",
        "Sentencia 4/2026",
        "RPL 421/2026",
        "referencia diaria 22",
        "no es un número oficial de causa",
        "DP 1901 aporta preguntas y documentos; no sustituye la denuncia AC",
        "Derecho de respuesta y corrección",
    ],
)
require(
    EN_REL,
    en,
    [
        "Removal, remuneration and integrated control of the Insolvency Administrator",
        "23 April 2025 · 58 pages",
        "EUR 110,956.97 for the estate",
        "Order 1377/2025 · PDF",
        "Open Orders and decisions",
        "without needing to enter the merits grounds",
        "RPL 3304/2025",
        "RPL 3319/2025",
        "Third Transitional Provision of Law 25/2015",
        "Judgment 4/2026",
        "RPL 421/2026",
        "daily intake reference 22",
        "it is not an official case number",
        "DP 1901 supplies questions and documents; it does not replace the AC complaint",
        "Right of response and correction",
    ],
)
require(
    DIGEST_REL,
    digest,
    [
        "## 3. The 23 April 2025 removal application — complete structured digest",
        "## 4. The two removal orders",
        "## 6. The remuneration / professional-liability action",
        "## 7. Criminal complaint associated with Decanato daily intake/reference 22",
        "## 8. DP 1901/2026, additions and cross-evidence",
        "## 9. Mandatory AC analytical gateway",
        "Do not write `Control 22 → DP 1956/2026` as an established allocation",
    ],
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
        errors.append(f"{rel}: public copy still contains form fields")
    if doc.get_xml_metadata():
        errors.append(f"{rel}: public copy contains XML metadata")
    for page_number, page in enumerate(doc, start=1):
        if page.get_text().strip():
            errors.append(f"{rel}: page {page_number} contains a searchable text layer")
        if page.first_annot is not None:
            errors.append(f"{rel}: page {page_number} contains annotations")
        if not page.get_images(full=True):
            errors.append(f"{rel}: page {page_number} has no raster image")
    doc.close()

require(
    PROVENANCE_REL,
    provenance,
    [
        "5665ec05ae42f18fc64b1209ed7984c39ece015933bdfc9dd8bcf1a8ece6bf26",
        "6f44c28781f56a46eb5df12b54f33eebd0848a05167eac2dc4f3fe19a5d90430",
        "5f2925609563caec6c82f4e95fa16abb660f372a34051133fe0f01aa785483f7",
        PDF_SPECS[next(iter(PDF_SPECS))][1],
    ],
)

for sitemap_rel in ["sitemap.xml", "sitemap-unitary-shell.xml"]:
    sitemap_path = ROOT / sitemap_rel
    try:
        ET.parse(sitemap_path)
    except Exception as exc:
        errors.append(f"{sitemap_rel}: invalid XML: {exc}")
        continue
    sitemap = read(sitemap_rel)
    for route in [
        "/es/concurso-36-2012-separacion-ac-honorarios/",
        "/en/insolvency-36-2012-administrator-removal-fees/",
    ]:
        if route not in sitemap:
            errors.append(f"{sitemap_rel}: missing route {route}")

discovery_markers = {
    "assets/data/unitary-route-registry-v1.json": [
        "en/insolvency-36-2012-administrator-removal-fees/",
        "es/concurso-36-2012-separacion-ac-honorarios/",
    ],
    "en/site-index/index.html": [
        "Administrator removal, remuneration and orders",
        "../insolvency-36-2012-administrator-removal-fees/",
    ],
    "es/indice-web/index.html": [
        "Separación del AC, honorarios y autos",
        "../concurso-36-2012-separacion-ac-honorarios/",
    ],
}
for rel, markers in discovery_markers.items():
    require(rel, read(rel), markers)

# The public site must not retain the superseded pseudo-case labels.
for base in [ROOT / "es", ROOT / "en"]:
    for path in base.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        if re.search(r"\bControl\s+(?:22|24)\b", text, flags=re.IGNORECASE):
            errors.append(f"{path.relative_to(ROOT)}: superseded Control 22/24 label")
        if re.search(r"(?:22\s*[→=-]+\s*DP\s*1956|Control\s*22.{0,80}DP\s*1956)", text, flags=re.IGNORECASE | re.DOTALL):
            errors.append(f"{path.relative_to(ROOT)}: unproved reference-22 to DP1956 mapping")

# Basic personal-data leakage guard for the new public pages.
for rel, text in [(ES_REL, es), (EN_REL, en)]:
    for label, pattern in [
        ("email address", r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
        ("Spanish DNI/NIE", r"\b(?:[XYZ]\d{7}[A-Z]|\d{8}[A-Z])\b"),
        ("Spanish mobile number", r"(?<!\d)(?:\+34\s*)?[67]\d{8}(?!\d)"),
    ]:
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"{rel}: possible {label} leakage")

register_path = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
with register_path.open(encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.reader(handle))
if not rows:
    errors.append("archive/PROCEEDINGS_MASTER_REGISTER.csv: empty")
else:
    width = len(rows[0])
    for number, row in enumerate(rows, start=1):
        if len(row) != width:
            errors.append(f"archive/PROCEEDINGS_MASTER_REGISTER.csv:{number}: {len(row)} columns, expected {width}")
    register = "\n".join(",".join(row) for row in rows)
    for marker in ["GC-CIV-027", "GC-APP-028", "GC-REF-029", "RPL 3304/2025", "RPL 3319/2025"]:
        if marker not in register:
            errors.append(f"archive/PROCEEDINGS_MASTER_REGISTER.csv: missing {marker}")

if errors:
    print("validation: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("validation: PASS")

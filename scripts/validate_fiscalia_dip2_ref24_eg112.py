#!/usr/bin/env python3
"""Validate the DIP 2/2026, reference 24 and EG 112 public update."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import fitz
from pypdf import PdfReader
from pypdf.generic import NullObject


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "evidence/fiscalia/eg-112-2026/public-pdfs/decreto-aclaracion-eg-112-2026-23ago2026-public-redacted.pdf"
TRANSCRIPT = ROOT / "evidence/fiscalia/eg-112-2026/full-text/decreto-aclaracion-eg-112-2026-23ago2026-public-transcription.md"
TRANSLATION = ROOT / "evidence/fiscalia/eg-112-2026/full-text/decreto-aclaracion-eg-112-2026-23ago2026-english-translation.md"
README = ROOT / "evidence/fiscalia/eg-112-2026/README.md"
REF24_README = ROOT / "evidence/judicial-governance/decanato-reference-24/README.md"
ES = ROOT / "es/fiscalia-dip-2-2026/index.html"
EN = ROOT / "en/fiscalia-dip-2-2026/index.html"
CLOSEOUT = ROOT / "docs/deletion-audits/2026-08-25-fiscalia-eg112-notification-cross-thread-closeout.md"

EXPECTED = {
    PDF: "fe9111aca4aa4cc82627af6c97a8408e3ed5e3db9e0382a6e302783f281b6783",
    TRANSCRIPT: "edcbeb9ca68ff33b0dbd8cb4bc9442c30f63d0db1ad570c0c7d72c0222bb919a",
    TRANSLATION: "faee0700814b3ffbe309d47c2a5a2697833fac72ad2ca21e3d6272c8e78d9ebe",
}

BANNED = (
    "@justiciaencanarias.org",
    "928306511",
    "Plaza de San Agustín",
    "***7368**",
    "AC Sector Público",
)

FAILURES: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


for path, expected_hash in EXPECTED.items():
    require(path.is_file(), f"missing derivative: {path.relative_to(ROOT)}")
    if path.is_file():
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == expected_hash, f"hash mismatch for {path.relative_to(ROOT)}: {actual}")

if PDF.is_file():
    reader = PdfReader(PDF)
    require(len(reader.pages) == 3, "EG 112 public PDF must have three pages")
    acroform = reader.trailer["/Root"].get("/AcroForm")
    require(acroform is None or isinstance(acroform, NullObject), "EG 112 public PDF still has an AcroForm dictionary")
    for page_number, page in enumerate(reader.pages, start=1):
        widgets = [
            annotation
            for annotation in page.get("/Annots", [])
            if annotation.get_object().get("/Subtype") == "/Widget"
        ]
        require(not widgets, f"EG 112 public PDF page {page_number} contains a widget")
    fitz_document = fitz.open(PDF)
    pdf_text = "\n".join(page.get_text("text") for page in fitz_document)
    fitz_document.close()
    for banned in BANNED:
        require(banned.casefold() not in pdf_text.casefold(), f"private literal remains in PDF text: {banned}")
    require(not re.search(r"\b\d{8}[A-Z]\b", pdf_text), "full Spanish identifier pattern remains in PDF text")

transcript = read(TRANSCRIPT)
normalized_transcript = " ".join(transcript.split())
for marker in (
    "Expediente gubernativo n.º 112/2026",
    "## Página 1 de 3",
    "## Página 2 de 3",
    "## Página 3 de 3",
    "No le falta razón al Sr. Marer",
    "Fiscalía Provincial de Las Palmas de Gran Canaria",
):
    require(
        " ".join(marker.split()) in normalized_transcript,
        f"transcription missing marker: {marker}",
    )
for banned in BANNED:
    require(banned.casefold() not in transcript.casefold(), f"private literal remains in transcription: {banned}")
require(not re.search(r"\b\d{8}[A-Z]\b", transcript), "full Spanish identifier pattern remains in transcription")

translation = read(TRANSLATION)
normalized_translation = " ".join(translation.split())
for marker in (
    "Clarification Decree — Governmental File 112/2026",
    "## Page 1 of 3",
    "## Page 2 of 3",
    "## Page 3 of 3",
    "Mr Marer is not wrong",
    "Provincial Public Prosecutor's Office of Las Palmas de Gran Canaria",
):
    require(
        " ".join(marker.split()) in normalized_translation,
        f"English translation missing marker: {marker}",
    )
for banned in BANNED:
    require(banned.casefold() not in translation.casefold(), f"private literal remains in English translation: {banned}")
require(not re.search(r"\b\d{8}[A-Z]\b", translation), "full Spanish identifier pattern remains in English translation")

readme = read(README)
for marker in ("EVID-2026-FISCALIA-EG112-ACLARACION-003", *EXPECTED.values()):
    require(marker in readme, f"EG 112 README missing marker: {marker}")

ref24 = read(REF24_README)
for marker in (
    "Later institutional references located on 25 August 2026",
    "CGPJ Promotor's agreement dated **10 July 2026**",
    "TSJC Government Secretariat's signed agreement dated **20 August 2026**",
    "remains unlocated",
):
    require(marker in ref24, f"reference-24 README missing marker: {marker}")

for path, markers in {
    ES: (
        'id="eg112-aclaracion"',
        "EVID-2026-FISCALIA-EG112-ACLARACION-003",
        "Auditoría de congruencia institucional",
        "Objeto real",
        "Integridad de la fuente",
        "no se representa como NIG ni como procedimiento confirmado",
        "Referencia expresa al «control 24»",
        "tsj-canarias-exp-gub-38-2026/",
    ),
    EN: (
        'id="eg112-clarification"',
        "EVID-2026-FISCALIA-EG112-ACLARACION-003",
        "Institutional congruence audit",
        "Actual object",
        "Source integrity",
        "not represented as a NIG or confirmed proceeding",
        "Express reference to “control 24”",
        "tsj-canarias-exp-gub-38-2026/",
    ),
}.items():
    page = read(path)
    for marker in markers:
        require(
            marker.casefold() in page.casefold(),
            f"{path.relative_to(ROOT)} missing marker: {marker}",
        )
    require(PDF.name in page, f"{path.relative_to(ROOT)} does not link the EG 112 PDF")
    require(TRANSCRIPT.name in page, f"{path.relative_to(ROOT)} does not link the EG 112 transcription")
require(TRANSLATION.name in read(EN), "English page does not link the complete EG 112 English translation")

closeout = read(CLOSEOUT)
for marker in (
    "Cross-thread continuity and deletion audit — Fiscalía EG 112/2026 notification",
    "Controlling institutional contradiction map",
    "Office-level attribution rule",
    "Procedure and module separation",
    "Privacy and evidence-custody lock",
    "Future-thread restart order",
):
    require(marker in closeout, f"EG 112 closeout missing marker: {marker}")

if FAILURES:
    print("FISCALIA DIP2 / REF24 / EG112 VALIDATION: FAIL")
    for failure in FAILURES:
        print(f"- {failure}")
    sys.exit(1)

print("FISCALIA DIP2 / REF24 / EG112 VALIDATION: PASS")

#!/usr/bin/env python3
"""Remove unnecessary contact details from the public RICPE PDF derivative.

The private source remains outside public Git. This builder operates only on the
already-redacted public derivative, removes the two first-page contact rows from
the PDF content stream, inserts explicit minimisation labels, and regenerates the
public page-one JPEG. It never contains or logs the removed values.
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / (
    "evidence/ricpe-cnmv/2026-08-27/"
    "RICPE_Canal_Etico_Certificado_Resolucion_27AGO2026_PUBLICO_REDACTADO.pdf"
)
PAGE_ONE = ROOT / (
    "evidence/ricpe-cnmv/2026-08-27/"
    "resolution-pages-public-redacted/page-1.jpg"
)
EXPECTED_INPUT_SHA256 = (
    "1571939659af5df4891157958ebfc041748768d96a70bdf45aa6c3e247c65470"
)
LABELS = ("Teléfono contacto:", "Correo electrónico:")
REPLACEMENTS = (
    "Teléfono contacto: [DATO PERSONAL REDACTADO]",
    "Correo electrónico: [DATO PERSONAL REDACTADO]",
)
EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
PHONE_RE = re.compile(r"\+[0-9][0-9 ()-]{8,}[0-9]")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    if sha256(PDF) != EXPECTED_INPUT_SHA256:
        fail("Refusing to edit an unexpected RICPE public PDF derivative")

    temp_dir = ROOT / "tmp/pdfs/ricpe-contact-minimization"
    temp_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = temp_dir / PDF.name
    output_jpg_prefix = temp_dir / "page-1"
    output_jpg = temp_dir / "page-1.jpg"

    document = fitz.open(PDF)
    if document.page_count != 6:
        fail(f"Expected six pages, found {document.page_count}")
    page = document[0]

    hits = []
    for label in LABELS:
        matches = page.search_for(label)
        if len(matches) != 1:
            fail(f"Expected one first-page label for {label!r}, found {len(matches)}")
        hits.append(matches[0])

    redaction = fitz.Rect(
        min(rect.x0 for rect in hits) - 2,
        min(rect.y0 for rect in hits) - 3,
        520,
        max(rect.y1 for rect in hits) + 3,
    )
    page.add_redact_annot(redaction, fill=(1, 1, 1))
    page.apply_redactions()

    blue = (0.30, 0.47, 1.00)
    gray = (0.22, 0.25, 0.29)
    for rect, replacement in zip(hits, REPLACEMENTS, strict=True):
        label, value = replacement.split(": ", 1)
        baseline = rect.y1 - 1
        page.insert_text((rect.x0, baseline), f"{label}:", fontsize=9.5, color=blue)
        page.insert_text((rect.x0 + 102, baseline), value, fontsize=9.5, color=gray)

    metadata = document.metadata
    metadata["title"] = (
        "RICPE Canal Etico - certificado publico con identificador y datos "
        "de contacto redactados"
    )
    metadata["subject"] = (
        "Derivado publico minimizado; el original integro se conserva bajo "
        "custodia privada"
    )
    document.set_metadata(metadata)
    # Preserve the existing trailer ID so identical source bytes yield an
    # identical public derivative across recovery worktrees.
    document.save(
        output_pdf,
        garbage=4,
        clean=True,
        deflate=True,
        no_new_id=True,
    )
    document.close()

    extracted = subprocess.run(
        ["pdftotext", "-layout", str(output_pdf), "-"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    if EMAIL_RE.search(extracted) or PHONE_RE.search(extracted):
        fail("Contact data remains extractable from the minimized derivative")
    if extracted.count("DATO PERSONAL REDACTADO") != 2:
        fail("The minimized derivative lacks both explicit contact-data labels")

    subprocess.run(
        [
            "pdftoppm",
            "-f",
            "1",
            "-singlefile",
            "-jpeg",
            "-r",
            "110",
            "-jpegopt",
            "quality=90",
            str(output_pdf),
            str(output_jpg_prefix),
        ],
        check=True,
    )
    if not output_jpg.is_file():
        fail("Page-one JPEG rendering failed")

    os.replace(output_pdf, PDF)
    os.replace(output_jpg, PAGE_ONE)
    shutil.rmtree(temp_dir)

    print("RICPE public contact minimization: PASS")
    print(f"- PDF SHA-256: {sha256(PDF)}")
    print(f"- page-one JPEG SHA-256: {sha256(PAGE_ONE)}")


if __name__ == "__main__":
    main()

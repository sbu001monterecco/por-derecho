#!/usr/bin/env python3
"""Fail-closed validation for the eight-document Canary Treasury room."""

from __future__ import annotations

import hashlib
import base64
import json
import re
import sys
import tempfile
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/canary-ric-public-debt/2026-08-28-production"
MANIFEST = EVIDENCE / "manifest-v1.json"
ES = ROOT / "es/evidencia/tesoro-deuda-ric-2022-2025-documentos/index.html"
EN = ROOT / "en/evidence/treasury-ric-debt-2022-2025-documents/index.html"
ES_VIEWER = ES.parent / "visor-pdf.html"
EN_VIEWER = EN.parent / "pdf-viewer.html"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(message: str) -> None:
    raise AssertionError(message)


def reconstruct(transport_path: Path, output: Path, expected_sha: str, expected_size: int) -> None:
    transport = json.loads(transport_path.read_text(encoding="utf-8"))
    chunks = transport.get("chunks", [])
    if len(chunks) != transport.get("chunk_count") or not chunks:
        fail(f"invalid transport inventory: {transport_path.relative_to(ROOT)}")
    digest = hashlib.sha256()
    size = 0
    with output.open("wb") as target:
        for rel in chunks:
            chunk = transport_path.parent / rel
            if not chunk.is_file() or chunk.stat().st_size > 1_000_000:
                fail(f"missing or oversized transport chunk: {chunk.relative_to(ROOT)}")
            try:
                payload = json.loads(chunk.read_text(encoding="utf-8"))
                if payload.get("encoding") != "base64-tilde-segments-16":
                    fail(f"invalid chunk encoding: {chunk.relative_to(ROOT)}")
                segments = payload.get("data", "").split("~")
                if not segments or any(len(segment) > 16 for segment in segments):
                    fail(f"invalid Base64 segment inventory: {chunk.relative_to(ROOT)}")
                decoded = base64.b64decode("".join(segments), validate=True)
            except Exception as exc:
                fail(f"invalid Base64 transport chunk {chunk.relative_to(ROOT)}: {exc}")
            target.write(decoded)
            digest.update(decoded)
            size += len(decoded)
    if size != expected_size or digest.hexdigest() != expected_sha:
        fail(f"lossless reconstruction mismatch: {transport_path.relative_to(ROOT)}")
    if transport.get("source_pdf_size_bytes") != size or transport.get("source_pdf_sha256") != expected_sha:
        fail(f"transport metadata mismatch: {transport_path.relative_to(ROOT)}")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["source_file_count"] != 8 or manifest["public_derivative_count"] != 8:
        fail("document denominator is not 8/8")
    if manifest["source_page_count"] != 734 or manifest["native_sources_public"]:
        fail("source denominator/custody boundary failed")
    if manifest["ocr_line_certified"]:
        fail("OCR must remain non-certified")

    ids: set[str] = set()
    pages = 0
    public_pdf_pages = 0
    with tempfile.TemporaryDirectory(prefix="ric-pdf-validation-") as temp_dir:
        temp_root = Path(temp_dir)
        for item in manifest["sources"]:
            evidence_id = item["evidence_id"]
            if evidence_id in ids:
                fail(f"duplicate evidence ID: {evidence_id}")
            ids.add(evidence_id)
            pages += item["source_pages"]
            local_pdf = ROOT / item["public_pdf"]
            pdf = temp_root / f"{evidence_id}.pdf"
            transport = ROOT / item["transport_manifest"]
            transcript = ROOT / item["transcript"]
            if not transport.is_file() or not transcript.is_file():
                fail(f"missing public derivative transport: {evidence_id}")
            reconstruct(transport, pdf, item["public_pdf_sha256"], item["public_pdf_size_bytes"])
            if local_pdf.exists() and (sha(local_pdf) != item["public_pdf_sha256"] or local_pdf.stat().st_size != item["public_pdf_size_bytes"]):
                fail(f"local PDF manifest mismatch: {evidence_id}")
            if sha(transcript) != item["transcript_sha256"]:
                fail(f"transcript manifest mismatch: {evidence_id}")
            doc = fitz.open(pdf)
            if len(doc) != item["source_pages"] + 1 or len(doc) != item["public_pdf_pages"]:
                fail(f"PDF page mismatch: {evidence_id}")
            if any(list(page.widgets() or []) for page in doc):
                fail(f"interactive form/signature field remains: {evidence_id}")
            extracted = "\n".join(page.get_text() for page in doc)
            if evidence_id == "CAN-RIC-TREAS-001":
                for source_page in doc.pages(1, 3):
                    token_region = source_page.get_pixmap(
                        clip=fitz.Rect(260, 775, 560, 811), colorspace=fitz.csGRAY, alpha=False
                    )
                    if any(pixel < 40 for pixel in token_region.samples):
                        fail("machine-readable barcode/QR region remains in access act")
            doc.close()
            public_pdf_pages += item["public_pdf_pages"]
            transcript_text = transcript.read_text(encoding="utf-8")
            if len(re.findall(r"^## Página fuente \d+ de \d+$", transcript_text, re.M)) != item["source_pages"]:
                fail(f"transcript page-marker mismatch: {evidence_id}")
            public_text = extracted + "\n" + transcript_text
            for forbidden in ("44.962.384-Y", "Virginia González Pérez", "sbu001@"):
                if forbidden.casefold() in public_text.casefold():
                    fail(f"forbidden private token in public derivative: {evidence_id}")

        exhibit_row = manifest.get("sharing_exhibit", {})
        exhibit = temp_root / "sharing-exhibit.pdf"
        exhibit_transport = ROOT / exhibit_row.get("transport_manifest", "")
        reconstruct(exhibit_transport, exhibit, exhibit_row.get("sha256"), exhibit_row.get("size_bytes"))
        local_exhibit = ROOT / exhibit_row.get("path", "")
        if local_exhibit.exists() and (sha(local_exhibit) != exhibit_row.get("sha256") or local_exhibit.stat().st_size != exhibit_row.get("size_bytes")):
            fail("local sharing exhibit manifest mismatch")
        exhibit_pdf = fitz.open(exhibit)
        if len(exhibit_pdf) != 2 or any(list(page.widgets() or []) for page in exhibit_pdf):
            fail("sharing exhibit must be a two-page static PDF")
        exhibit_pdf.close()

    if pages != 734 or public_pdf_pages != 742:
        fail(f"aggregate page mismatch: {pages} source / {public_pdf_pages} derivative")
    page_index = ROOT / manifest["page_index"]
    if sha(page_index) != manifest["page_index_sha256"]:
        fail("page-index manifest mismatch")
    index = json.loads(page_index.read_text(encoding="utf-8"))
    indexed_pages = []
    if index.get("storage") != "PARTITIONED_COMPLETE_INDEX":
        fail("page index must use the complete partitioned form")
    for part in index.get("parts", []):
        part_path = ROOT / part["path"]
        if sha(part_path) != part["sha256"]:
            fail(f"page-index part mismatch: {part['path']}")
        payload = json.loads(part_path.read_text(encoding="utf-8"))["pages"]
        if len(payload) != part["page_count"]:
            fail(f"page-index part count mismatch: {part['path']}")
        indexed_pages.extend(payload)
    if len(indexed_pages) != 734 or index.get("part_count") != len(index.get("parts", [])):
        fail("page index does not contain 734 entries")

    es = ES.read_text(encoding="utf-8")
    en = EN.read_text(encoding="utf-8")
    for evidence_id in sorted(ids):
        if evidence_id not in es or evidence_id not in en:
            fail(f"bilingual inventory missing {evidence_id}")
    requirements = {
        ES: ("734", "2022", "menor cupón", "no acredita", "custodia protegida"),
        EN: ("734", "2022", "lower coupon", "does not establish", "protected custody"),
        ROOT / "es/deuda-publica-ric-canarias/index.html": ("aliviar la carga financiera de Canarias", "2022: autorización prevista", "Sala documental"),
        ROOT / "en/canary-ric-public-debt/index.html": ("financing burden", "2022 authorisation planning", "eight-document room"),
    }
    for path, needles in requirements.items():
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                fail(f"required wording missing from {path.relative_to(ROOT)}: {needle}")
    if "visor-pdf.html?doc=exhibit-access" not in es or "pdf-viewer.html?doc=exhibit-access" not in en:
        fail("sharing exhibit is not linked from both document-room routes")
    for viewer in (ES_VIEWER, EN_VIEWER):
        viewer_text = viewer.read_text(encoding="utf-8")
        for key in ("puesta-disposicion", "operaciones-2022", "operaciones-2023", "operaciones-2024", "emision-ric-2024", "operaciones-2025", "emision-ric-2025", "contratos", "exhibit-access"):
            if key not in viewer_text:
                fail(f"viewer inventory missing {key}: {viewer.relative_to(ROOT)}")

    private_names = {item["original_filename"] for item in manifest["sources"]}
    tracked = {str(path.relative_to(ROOT)) for path in ROOT.rglob("*.pdf")}
    if any(Path(path).name in private_names for path in tracked):
        fail("a native source filename appears in public Git scope")

    print("PASS: 8/8 public derivatives; 734/734 source pages; 742 derivative pages; hashes, transcripts, privacy, custody and bilingual routes validated")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise

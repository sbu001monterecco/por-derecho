#!/usr/bin/env python3
"""Build public-safe, page-faithful derivatives of the Canary Treasury production.

The eight native PDFs remain outside public Git.  This builder consumes those
private originals plus reviewed OCR working copies and emits public-redacted,
searchable PDFs, page-sequenced OCR text editions, provenance controls and a
machine-readable 734-page index.  OCR is explicitly non-certified and never
silently replaces the native source.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import fitz
from pypdf import PdfReader
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


CONTROL_ID = "PD-CANARY-RIC-PUBLIC-DEBT-DOCROOM-20260831-01"
PUBLIC_ROOT = Path("evidence/canary-ric-public-debt/2026-08-28-production")


@dataclass(frozen=True)
class Source:
    evidence_id: str
    original_name: str
    slug: str
    pages: int
    original_sha256: str
    ocr_pdf_name: str | None
    ocr_text_name: str | None
    family_es: str
    family_en: str


SOURCES = (
    Source("CAN-RIC-TREAS-001", "Escrito puesta a disposicion I firmado.pdf", "puesta-disposicion-154-2026", 3, "6f21dffe62759de498830db28c571685a7afefadee4dbea20d17014a6dfe6187", None, None, "Acto de puesta a disposición", "Access-delivery act"),
    Source("CAN-RIC-TREAS-002", "OPERACIONES 2025.pdf", "operaciones-2025", 110, "056cbc067689b680d45026e148e4535fecbecb74545ed3d9a782ebbdb76cc98b", "operaciones-2025.pdf", "operaciones-2025.txt", "Operaciones de endeudamiento 2025", "2025 debt operations"),
    Source("CAN-RIC-TREAS-003", "EMISIÓN RIC 2025.pdf", "emision-ric-2025", 36, "89b294c91abe60d30ca73bc7f6a33bbeaf43595358d98d70811c55de70847030", "emision-ric-2025.pdf", "emision-ric-2025.txt", "Emisión RIC 2025", "2025 RIC issue"),
    Source("CAN-RIC-TREAS-004", "OPERACIONES 2024.pdf", "operaciones-2024", 129, "775d227b8403dfc5be9d0aca61af9436f05809f51c6c2b075b3436be7db19353", "operaciones-2024.pdf", "operaciones-2024.txt", "Operaciones de endeudamiento 2024", "2024 debt operations"),
    Source("CAN-RIC-TREAS-005", "EMISIÓN RIC 2024.pdf", "emision-ric-2024", 49, "43bd233abdfea9413c6c7fcc41758bb5987dccbe4b78918719bca7606f1f1341", "emision-ric-2024.pdf", "emision-ric-2024.txt", "Emisión RIC 2024", "2024 RIC issue"),
    Source("CAN-RIC-TREAS-006", "OPERACIONES 2023.pdf", "operaciones-2023", 117, "f559bfb2d8d811caa287c373dbf65005d60f07a4575f48feccd45cbda30c1004", "operaciones-2023.pdf", "operaciones-2023.txt", "Operaciones de endeudamiento 2023", "2023 debt operations"),
    Source("CAN-RIC-TREAS-007", "OPERACIONES 2022-1.pdf", "operaciones-2022", 114, "19efcbd1e95a53161e8e19243d471c3240b45bdb8199818f4a52c28d39818571", "operaciones-2022.pdf", "operaciones-2022.txt", "Operaciones de endeudamiento 2022", "2022 debt operations"),
    Source("CAN-RIC-TREAS-008", "Contratos.pdf", "contratos", 176, "d69bbb797f7da157f5687ec9850d0eb206d924613e20f3bf33ff5d2487c614a8", "contratos-force.pdf", "contratos-force.txt", "Contratación y asesoramiento financiero", "Financial-advisory contracting"),
)


EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
DNI_RE = re.compile(r"(?<!\d)(?:\d{1,2}[.\s]\d{3}[.\s]\d{3}|\d{8})[-\s]?[A-Z](?!\w)", re.I)
LONG_CODE_RE = re.compile(r"(?<!\w)(?:GEN[-\w]+|RP\d+[-\w+/=]+|[A-Za-z0-9+/=_-]{22,})(?!\w)")
PRIVATE_NAMES = ("Virginia González Pérez",)
TERM_PATTERNS = {
    "ric": re.compile(r"\bRIC\b", re.I),
    "public_issue": re.compile(r"emisi[oó]n|bonos|obligaciones", re.I),
    "subscription": re.compile(r"suscripci[oó]n|prorrateo|sorteo", re.I),
    "ordinary_debt": re.compile(r"pr[eé]stamo|refinanciar|vencimientos ordinarios", re.I),
    "afi": re.compile(r"Analistas Financieros Internacionales|\bAFI\b", re.I),
    "market_infrastructure": re.compile(r"IBERCLEAR|AIAF|Banco de Espa[ñn]a", re.I),
    "acosta_hnt_ricpe": re.compile(r"Acosta|Hotel New Trend|MYND|RICPE", re.I),
}


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_pages(text: str, expected: int) -> list[str]:
    pages = text.replace("\r\n", "\n").replace("\r", "\n").split("\f")
    if len(pages) == expected + 1 and not pages[-1].strip():
        pages.pop()
    if len(pages) != expected:
        raise ValueError(f"OCR page mismatch: expected {expected}, found {len(pages)}")
    return pages


def source_text(source: Source, source_dir: Path, ocr_dir: Path) -> list[str]:
    if source.ocr_text_name:
        return normalize_pages((ocr_dir / source.ocr_text_name).read_text(encoding="utf-8", errors="replace"), source.pages)
    reader = PdfReader(source_dir / source.original_name)
    return [(page.extract_text() or "") for page in reader.pages]


def sanitize_text(text: str) -> tuple[str, int]:
    redactions = 0

    def replace(rx: re.Pattern[str], marker: str, value: str) -> str:
        nonlocal redactions
        value, count = rx.subn(marker, value)
        redactions += count
        return value

    text = replace(EMAIL_RE, "[CORREO ELECTRÓNICO OMITIDO]", text)
    text = replace(DNI_RE, "[IDENTIFICADOR PERSONAL OMITIDO]", text)
    text = replace(LONG_CODE_RE, "[CÓDIGO DE VERIFICACIÓN OMITIDO]", text)
    for name in PRIVATE_NAMES:
        count = text.lower().count(name.lower())
        if count:
            text = re.sub(re.escape(name), "[REPRESENTANTE DE LA CONTRATISTA OMITIDA]", text, flags=re.I)
            redactions += count
    cleaned = "\n".join(line.rstrip() for line in text.splitlines())
    return cleaned.strip(), redactions


def redaction_rects(source: Source, page: fitz.Page) -> list[fitz.Rect]:
    rects: list[fitz.Rect] = []
    for phrase in PRIVATE_NAMES + ("sbu001@monterecco.com", "44.962.384-Y"):
        rects.extend(page.search_for(phrase))
    for word in page.get_text("words"):
        token = str(word[4]).strip()
        if EMAIL_RE.search(token) or DNI_RE.search(token) or LONG_CODE_RE.fullmatch(token):
            rects.append(fitz.Rect(word[:4]))
    if source.evidence_id == "CAN-RIC-TREAS-001":
        # The signed act encodes the electronic-verification token as a
        # machine-readable barcode/QR image as well as text.  Remove that
        # image region while retaining the public signer, capacity and date.
        rects.append(fitz.Rect(260, 775, 560, 811))
    return rects


def make_cover(source: Source, redaction_count: int) -> bytes:
    buf = io.BytesIO()
    styles = getSampleStyleSheet()
    styles["Title"].textColor = HexColor("#14324a")
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=24 * mm, rightMargin=24 * mm, topMargin=24 * mm, bottomMargin=24 * mm)
    story = [
        Paragraph("Por Derecho · Canary Treasury production", styles["Title"]),
        Spacer(1, 8 * mm),
        Paragraph(f"<b>{source.family_es}</b> / {source.family_en}", styles["Heading2"]),
        Spacer(1, 5 * mm),
        Paragraph(f"Evidence ID: <b>{source.evidence_id}</b><br/>Control: {CONTROL_ID}<br/>Native filename: {source.original_name}<br/>Native source pages: {source.pages}<br/>Native SHA-256: {source.original_sha256}", styles["BodyText"]),
        Spacer(1, 7 * mm),
        Paragraph("<b>PUBLIC-REDACTED OCR DERIVATIVE / DERIVADO OCR PÚBLICO REDACTADO</b>", styles["Heading3"]),
        Paragraph("The native source remains in private custody. This derivative adds a non-certified OCR text layer and does not preserve or replace any native digital signature. Personal contact data, personal identifiers, private representative names and electronic verification tokens are omitted where detected. Public officials, public bodies, corporate identities, financial terms and evidentially material text remain visible. / La fuente nativa permanece en custodia privada. Este derivado añade OCR no certificado y no conserva ni sustituye las firmas digitales nativas. Se omiten, cuando se detectan, datos de contacto, identificadores personales, nombres privados de representantes y códigos electrónicos de verificación.", styles["BodyText"]),
        Spacer(1, 5 * mm),
        Paragraph(f"Automated redaction targets applied: {redaction_count}. OCR has not been manually certified line by line; consult the page image and the privately retained native source for any material quotation.", styles["BodyText"]),
    ]
    doc.build(story)
    return buf.getvalue()


def build_pdf(source: Source, base_pdf: Path, output: Path) -> int:
    body = fitz.open(base_pdf)
    redaction_count = 0
    for page in body:
        rects = redaction_rects(source, page)
        for rect in rects:
            page.add_redact_annot(rect + (-1, -1, 1, 1), fill=(1, 1, 1), text="[OMITIDO]", fontsize=6, text_color=(0.2, 0.2, 0.2))
        if rects:
            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_PIXELS)
            redaction_count += len(rects)
    cover = fitz.open(stream=make_cover(source, redaction_count), filetype="pdf")
    final = fitz.open()
    final.insert_pdf(cover)
    final.insert_pdf(body)
    for page in final:
        for widget in list(page.widgets() or []):
            page.delete_widget(widget)
    final.set_metadata({"title": f"{source.family_es} - derivado OCR público redactado", "author": "Por Derecho / Project Sun Rock", "subject": CONTROL_ID, "keywords": f"{source.evidence_id}, OCR, public-redacted"})
    output.parent.mkdir(parents=True, exist_ok=True)
    # PyMuPDF must not save over a stale or interrupted derivative: doing so can
    # leave orphaned page-tree references even when the apparent page count is
    # correct.  The inputs remain the hash-verified native/OCR working copies.
    output.unlink(missing_ok=True)
    final.save(output, garbage=4, deflate=True, clean=True)
    final.close()
    cover.close()
    body.close()
    if output.stat().st_size > 90_000_000:
        compressed = output.with_name(f"{output.stem}-compressed.pdf")
        subprocess.run(
            [
                "gs",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.7",
                "-dPDFSETTINGS=/ebook",
                "-dDetectDuplicateImages=true",
                "-dCompressFonts=true",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                f"-sOutputFile={compressed}",
                str(output),
            ],
            check=True,
        )
        if len(fitz.open(compressed)) != source.pages + 1:
            raise ValueError(f"Compressed derivative page mismatch: {source.evidence_id}")
        compressed.replace(output)
    return redaction_count


def markdown_transcript(source: Source, pages: list[dict[str, object]]) -> str:
    head = f"""# {source.family_es} — edición OCR pública redactada

**Evidence ID:** `{source.evidence_id}`
**Control:** `{CONTROL_ID}`
**Fuente nativa:** `{source.original_name}` · {source.pages} páginas · SHA-256 `{source.original_sha256}`

Esta edición reproduce secuencialmente las {source.pages} páginas de la copia de control. No es el original, una copia certificada ni una transcripción pericial. El OCR español/inglés no está certificado línea por línea. Las omisiones expresas protegen datos personales y códigos de verificación; no eliminan términos financieros o institucionales materiales.

"""
    blocks = []
    for item in pages:
        blocks.append(f"\n## Página fuente {item['source_page']} de {source.pages}\n\n{item['text'] or '[SIN TEXTO OCR FIABLE; CONSÚLTESE EL FACSÍMIL PÚBLICO REDACTADO]'}\n")
    return head + "".join(blocks)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--ocr-dir", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()

    public_root = args.repo_root / PUBLIC_ROOT
    public_root.mkdir(parents=True, exist_ok=True)
    manifest_sources: list[dict[str, object]] = []
    page_index: list[dict[str, object]] = []

    for source in SOURCES:
        original = args.source_dir / source.original_name
        if sha256_path(original) != source.original_sha256:
            raise ValueError(f"Native hash mismatch: {source.original_name}")
        base_pdf = args.ocr_dir / source.ocr_pdf_name if source.ocr_pdf_name else original
        pages_raw = source_text(source, args.source_dir, args.ocr_dir)
        page_rows: list[dict[str, object]] = []
        text_redactions = 0
        for number, raw in enumerate(pages_raw, 1):
            clean, count = sanitize_text(raw)
            text_redactions += count
            row = {
                "evidence_id": source.evidence_id,
                "source_page": number,
                "text": clean,
                "text_sha256": hashlib.sha256(clean.encode("utf-8")).hexdigest(),
                "ocr_characters": len(clean),
                "redaction_markers": count,
                "terms": [key for key, rx in TERM_PATTERNS.items() if rx.search(clean)],
            }
            page_rows.append(row)
            page_index.append(row)

        source_dir = public_root / source.slug
        pdf_path = source_dir / f"{source.slug}-publico-redactado-ocr.pdf"
        pdf_redactions = build_pdf(source, base_pdf, pdf_path)
        transcript_path = source_dir / "transcript-es.md"
        transcript_path.write_text(markdown_transcript(source, page_rows), encoding="utf-8")
        redaction_log = f"""# Redaction and OCR log — {source.evidence_id}

- Native source pages: `{source.pages}`
- Native SHA-256: `{source.original_sha256}`
- Native publication: `PRIVATE_CUSTODY_RETAINED`
- Public derivative: `{pdf_path.name}`
- PDF redaction targets applied: `{pdf_redactions}`
- Text redaction markers applied: `{text_redactions}`
- OCR languages: `spa+eng`
- OCR line-by-line certification: `false`
- Native digital-signature preservation in derivative: `false`
- Public omissions: personal email/contact data, detected personal DNI, private contractor-representative name and long electronic verification tokens.
- Retained: public officials and capacities, public bodies, corporate identities/NIFs, public-office contacts, financial terms, dates, amounts, ISINs and institutionally material text.
"""
        (source_dir / "redaction-log.md").write_text(redaction_log, encoding="utf-8")
        manifest_sources.append({
            "evidence_id": source.evidence_id,
            "original_filename": source.original_name,
            "source_pages": source.pages,
            "original_sha256": source.original_sha256,
            "original_size_bytes": original.stat().st_size,
            "public_pdf": str(pdf_path.relative_to(args.repo_root)),
            "public_pdf_pages": len(fitz.open(pdf_path)),
            "public_pdf_sha256": sha256_path(pdf_path),
            "public_pdf_size_bytes": pdf_path.stat().st_size,
            "transcript": str(transcript_path.relative_to(args.repo_root)),
            "transcript_sha256": sha256_path(transcript_path),
            "pdf_redaction_targets": pdf_redactions,
            "text_redaction_markers": text_redactions,
        })

    if len(page_index) != 734:
        raise ValueError(f"Expected 734 indexed source pages, found {len(page_index)}")
    index_path = public_root / "page-index-v1.json"
    index_path.write_text(json.dumps({"control_id": CONTROL_ID, "source_page_count": 734, "ocr_line_certified": False, "pages": page_index}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "control_id": CONTROL_ID,
        "state": "LOCAL_PUBLIC_SAFE_DERIVATIVES_BUILT",
        "source_file_count": 8,
        "source_page_count": 734,
        "native_sources_public": False,
        "public_derivative_count": 8,
        "ocr_line_certified": False,
        "redaction_policy": "Personal contacts, detected personal identifiers, private representative names and verification tokens omitted; public institutional and financial content retained.",
        "sources": manifest_sources,
        "page_index": str(index_path.relative_to(args.repo_root)),
        "page_index_sha256": sha256_path(index_path),
    }
    (public_root / "manifest-v1.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

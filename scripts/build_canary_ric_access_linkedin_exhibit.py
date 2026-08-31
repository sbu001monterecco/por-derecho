#!/usr/bin/env python3
"""Build a two-page, public-safe LinkedIn document from the Treasury access act."""

from __future__ import annotations

import io
from pathlib import Path

import fitz
from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence/canary-ric-public-debt/2026-08-28-production/puesta-disposicion-154-2026/puesta-disposicion-154-2026-publico-redactado-ocr.pdf"
OUTPUT = ROOT / "evidence/canary-ric-public-debt/2026-08-28-production/puesta-disposicion-154-2026/exhibit-access-granted-gil-marer-20260828.pdf"
PAGE_W, PAGE_H = 1080, 1350  # LinkedIn-friendly 4:5 portrait document.
NAVY = HexColor("#102B36")
TEAL = HexColor("#1B6570")
GOLD = HexColor("#D4A94B")
PALE = HexColor("#EDF4F3")
INK = HexColor("#17313B")


def font_setup() -> None:
    regular = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    bold = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    pdfmetrics.registerFont(TTFont("DejaVu", regular))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", bold))


def wrapped(c: canvas.Canvas, text: str, x: float, y: float, width: float, font: str, size: float, leading: float, color=INK) -> float:
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if pdfmetrics.stringWidth(candidate, font, size) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def cover(c: canvas.Canvas) -> None:
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(72, PAGE_H - 128, 170, 7, fill=1, stroke=0)
    c.setFont("DejaVu-Bold", 23)
    c.setFillColor(PALE)
    c.drawString(72, PAGE_H - 92, "POR DERECHO  |  EVIDENCIA PUBLICA")
    c.setFont("DejaVu-Bold", 76)
    c.setFillColor(white)
    c.drawString(72, PAGE_H - 250, "ACCESO")
    c.drawString(72, PAGE_H - 335, "MATERIALIZADO")
    c.setFont("DejaVu", 26)
    c.setFillColor(PALE)
    c.drawString(76, PAGE_H - 390, "PUBLIC ACCESS MATERIALISED")

    c.setFillColor(Color(1, 1, 1, alpha=.07))
    c.roundRect(68, 390, PAGE_W - 136, 480, 22, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("DejaVu-Bold", 23)
    c.drawString(104, 817, "COMUNICACION OFICIAL DIRIGIDA A GIL MARER")
    y = 753
    y = wrapped(c, "\u201cHabiendo transcurrido dicho plazo sin que conste la formalización de recurso contencioso-administrativo que impida la materialización del acceso reconocido, procede dar cumplimiento a lo dispuesto en la referida resolución.\u201d", 104, y, PAGE_W - 208, "DejaVu-Bold", 30, 43, white)
    y -= 34
    wrapped(c, "\u201cLa información objeto de acceso se pone a disposición de la persona solicitante.\u201d", 104, y, PAGE_W - 208, "DejaVu-Bold", 30, 43, white)

    c.setFillColor(TEAL)
    c.roundRect(68, 260, PAGE_W - 136, 120, 18, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("DejaVu-Bold", 28)
    c.drawString(104, 331, "RESOLUCION 154/2026  |  TESORO DE CANARIAS")
    c.setFont("DejaVu", 22)
    c.drawString(104, 291, "28 agosto 2026  |  8 archivos  |  734 paginas")
    c.setFont("DejaVu", 17)
    c.setFillColor(PALE)
    url = "sbu001monterecco.github.io/por-derecho/es/evidencia/tesoro-deuda-ric-2022-2025-documentos/"
    c.drawString(72, 108, url)
    c.linkURL("https://" + url, (72, 88, PAGE_W - 72, 130), relative=0)
    c.setFont("DejaVu", 14)
    c.drawRightString(PAGE_W - 72, 55, "Cita textual del derivado publico redactado; original en custodia protegida.")
    c.showPage()


def facsimile(c: canvas.Canvas) -> None:
    doc = fitz.open(SOURCE)
    page = doc[1]  # Cover is page 1; source page 1 is derivative page 2.
    pix = page.get_pixmap(matrix=fitz.Matrix(2.1, 2.1), alpha=False)
    image = ImageReader(io.BytesIO(pix.tobytes("png")))
    c.setFillColor(PALE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 92, PAGE_W, 92, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("DejaVu-Bold", 24)
    c.drawString(54, PAGE_H - 57, "COMUNICACION DE ACCESO  |  28.08.2026")
    margin_x, bottom, top_gap = 56, 56, 118
    avail_w, avail_h = PAGE_W - 2 * margin_x, PAGE_H - bottom - top_gap
    scale = min(avail_w / page.rect.width, avail_h / page.rect.height)
    draw_w, draw_h = page.rect.width * scale, page.rect.height * scale
    x, y = (PAGE_W - draw_w) / 2, bottom
    c.drawImage(image, x, y, draw_w, draw_h, preserveAspectRatio=True, mask="auto")

    phrases = (
        "Gil Marer",
        "procede dar cumplimiento a lo",
        "la información objeto de acceso se pone",
        "a disposición de la persona solicitante",
    )
    c.setFillColor(Color(1, .82, .18, alpha=.24))
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.2)
    for phrase in phrases:
        for rect in page.search_for(phrase):
            rx = x + rect.x0 * scale
            ry = y + (page.rect.height - rect.y1) * scale
            rw, rh = rect.width * scale, rect.height * scale
            c.roundRect(rx - 3, ry - 2, rw + 6, rh + 4, 3, fill=1, stroke=1)
    c.showPage()
    doc.close()


def main() -> None:
    font_setup()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.unlink(missing_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=(PAGE_W, PAGE_H), pageCompression=1, invariant=1)
    c.setTitle("Acceso materializado - Resolución 154/2026 - Gil Marer")
    c.setAuthor("Por Derecho / Project Sun Rock")
    c.setSubject("Public-safe sharing exhibit derived from CAN-RIC-TREAS-001")
    cover(c)
    facsimile(c)
    c.save()
    check = fitz.open(OUTPUT)
    if len(check) != 2 or any(list(page.widgets() or []) for page in check):
        raise RuntimeError("Exhibit validation failed")
    check.close()
    print(OUTPUT)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the deterministic public redacted digital copy of the 27-Feb-2018 communication.

Requires reportlab==4.4.9. Run from any working directory; output is written to the
canonical evidence path in this repository.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/sun-park/2018-02-27-ac-security-request/public/2018-02-27-ac-community-security-request-redacted-searchable.pdf"
SOURCE_SHA256 = "497ecb49495badbcee155397fe70d37d090c36c4e7998308172e7a612046dbed"
EVIDENCE_ID = "SP-2018-02-27-AC-SECURITY-REQUEST"
PAGE_W, PAGE_H = A4
LEFT = 24 * mm
RIGHT = 24 * mm
TOP = PAGE_H - 22 * mm
BOTTOM = 19 * mm
TEXT_W = PAGE_W - LEFT - RIGHT
FONT_ROOT = Path("/usr/share/fonts/truetype/dejavu")
SANS = "PublicDejaVuSans"
SANS_BOLD = "PublicDejaVuSans-Bold"
SERIF = "PublicDejaVuSerif"
SERIF_BOLD = "PublicDejaVuSerif-Bold"
FONT_SPECS = (
    (SANS, "DejaVuSans.ttf", "ae7b7855e115a5966d8b1b3f80f254ccc117ec86f9965e202ee2940453837280"),
    (SANS_BOLD, "DejaVuSans-Bold.ttf", "5c1247acef7f2b8522a31742c76d6adcb5569bacc0be7ceaa4dc39dd252ce895"),
    (SERIF, "DejaVuSerif.ttf", "8f2c103bfa3fd5de71f1b92b18f21906b5a26871fb7e19a9a4c9af539c3cc7ab"),
    (SERIF_BOLD, "DejaVuSerif-Bold.ttf", "847b33e13925f19ff87e4d934d6b3cf7cac35ce16424f6f670e40c2f377cf2df"),
)


def register_fonts() -> None:
    for public_name, filename, expected_sha256 in FONT_SPECS:
        path = FONT_ROOT / filename
        actual_sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_sha256 != expected_sha256:
            raise RuntimeError(f"font integrity mismatch for {path}: {actual_sha256}")
        pdfmetrics.registerFont(TTFont(public_name, str(path)))


def wrap(text: str, font: str, size: float, width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        candidate = word if not line else f"{line} {word}"
        if stringWidth(candidate, font, size) <= width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, *, font: str, size: float, leading: float, width: float) -> float:
    c.setFont(font, size)
    for line in wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_redaction(c: canvas.Canvas, x: float, y: float, width: float = 86 * mm, height: float = 5.8 * mm) -> None:
    c.setFillColorRGB(0.04, 0.04, 0.04)
    c.roundRect(x, y - height + 1.5, width, height, 1.4 * mm, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont(SANS_BOLD, 6.8)
    c.drawCentredString(x + width / 2, y - height / 2 + 0.6, "REDACTED — DIRECT CONTACT DATA")
    c.setFillColorRGB(0, 0, 0)


def build() -> None:
    register_fonts()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1, invariant=1, pdfVersion=(1, 5))
    c.setTitle("27 February 2018 — public redacted digital copy")
    c.setAuthor("Project Sun Rock / Por Derecho")
    c.setSubject(EVIDENCE_ID)
    c.setCreator("Source-controlled deterministic publication script")

    c.setFillColorRGB(0.075, 0.145, 0.18)
    c.rect(0, PAGE_H - 31 * mm, PAGE_W, 31 * mm, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont(SANS_BOLD, 15)
    c.drawString(LEFT, PAGE_H - 13 * mm, "PUBLIC REDACTED DIGITAL COPY")
    c.setFont(SANS, 8.5)
    c.drawString(LEFT, PAGE_H - 19 * mm, "Primary-source transcript · direct electronic addresses removed")
    c.drawRightString(PAGE_W - RIGHT, PAGE_H - 13 * mm, "PROJECT SUN ROCK")
    c.drawRightString(PAGE_W - RIGHT, PAGE_H - 19 * mm, EVIDENCE_ID)

    y = PAGE_H - 40 * mm
    c.setFillColorRGB(0, 0, 0)
    c.setFont(SANS_BOLD, 10)
    c.drawString(LEFT, y, "ASUNTO / SUBJECT")
    y -= 5.5 * mm
    c.setFont(SANS_BOLD, 11)
    c.drawString(LEFT, y, "CONVOCATORIA JUNTA GENERAL COMUNIDAD DE PROPIETARIOS SUN PARK")
    y -= 8.5 * mm

    c.setFont(SANS_BOLD, 9)
    for label, marker in (("DE / FROM", "R1"), ("PARA / TO", "R2"), ("CC", "R3")):
        c.drawString(LEFT, y, label)
        c.setFont(SANS, 7.4)
        c.drawRightString(LEFT + 30 * mm, y, marker)
        draw_redaction(c, LEFT + 34 * mm, y + 1.5)
        y -= 7.3 * mm
        c.setFont(SANS_BOLD, 9)

    c.drawString(LEFT, y, "FECHA / DATE")
    c.setFont(SANS, 9.3)
    c.drawString(LEFT + 34 * mm, y, "martes, 27 de febrero de 2018 10:16:06 WET")
    y -= 10 * mm
    c.setStrokeColorRGB(0.75, 0.78, 0.78)
    c.line(LEFT, y, PAGE_W - RIGHT, y)
    y -= 9 * mm

    body_font = SERIF
    body_size = 11.2
    leading = 15.5
    c.setFont(body_font, body_size)
    c.drawString(LEFT, y, "Estimado Antonio:")
    y -= 8 * mm
    paragraphs = [
        "Le escrito [sic] en su condición de Presidente de la Comunidad de Propietarios Sun Park, y en mi condición de administrador concursal de Luchy Playa Blanca, S.L.U., entidad que ostenta la mayoría de cuotas de participación en la referida Comunidad, rogándole proceda a convocar Junta General con la finalidad de adoptar el acuerdo de contratar un servicio de seguridad que impida el accedo [sic] al complejo de personas no autorizadas y con ello el deterioro y uso indebido de las zonas comunes y privativas.",
        "Quedo a su disposición para tratar cualquier aspecto que considere oportuno.",
        "Atentamente,",
    ]
    for idx, paragraph in enumerate(paragraphs):
        y = draw_wrapped(c, paragraph, LEFT, y, font=body_font, size=body_size, leading=leading, width=TEXT_W)
        y -= 5.2 * mm if idx < 2 else 4 * mm
    c.setFont(SERIF_BOLD, 11.2)
    c.drawString(LEFT, y, "Borja Rodríguez-Batllori Laffitte")
    y -= 5.5 * mm
    c.setFont(SERIF, 11.2)
    c.drawString(LEFT, y, "Abogado")

    panel_y = BOTTOM + 21 * mm
    c.setFillColorRGB(0.95, 0.965, 0.96)
    c.roundRect(LEFT, panel_y, TEXT_W, 24 * mm, 2.2 * mm, fill=1, stroke=0)
    c.setFillColorRGB(0.07, 0.16, 0.14)
    c.setFont(SANS_BOLD, 8)
    c.drawString(LEFT + 4 * mm, panel_y + 17 * mm, "PUBLICATION CONTROL")
    notes = (
        "Diplomatic transcription: visible forms ‘Le escrito’ and ‘accedo’ are preserved and marked [sic]; no silent correction.",
        "This derivative proves the wording of the request; it does not itself establish later authority, implementation or legal characterisation.",
        f"Restricted-source SHA-256: {SOURCE_SHA256}",
    )
    yy = panel_y + 12.5 * mm
    for note in notes:
        yy = draw_wrapped(c, note, LEFT + 4 * mm, yy, font=SANS, size=7.2, leading=9, width=TEXT_W - 8 * mm)
        yy -= 1.2 * mm

    c.setFillColorRGB(0.22, 0.22, 0.22)
    c.setFont(SANS, 6.4)
    c.drawString(LEFT, BOTTOM, "Digitised public derivative · unredacted source retained outside the public repository")
    c.drawRightString(PAGE_W - RIGHT, BOTTOM, "Generated deterministically · reportlab 4.4.9")
    c.showPage()
    c.save()


if __name__ == "__main__":
    build()

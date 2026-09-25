#!/usr/bin/env python3
"""Validate the 24-Aug-2026 Cuatrecasas billing/email continuation and public sync."""
from __future__ import annotations

import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class StrictHTMLParser(HTMLParser):
    pass


errors: list[str] = []


def require(rel: str, markers: tuple[str, ...]) -> str:
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing file: {rel}")
        return ""
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"{rel}: missing marker {marker!r}")
    if path.suffix == ".html":
        try:
            StrictHTMLParser().feed(text)
        except Exception as exc:
            errors.append(f"{rel}: HTML parse failed: {exc}")
    return text


control = require(
    "archive/CUATRECASAS_PERIMETER_BILLING_EMAIL_AGENTIC_CONTINUATION_24AUG2026.md",
    (
        "2014-to-present",
        "Required line-by-line audit model",
        "June 2018 package lock",
        "Litigation-communications readiness gate",
        "Repository work, draft approval and campaign readiness never constitute email-send authorization",
    ),
)

handover = require(
    "CURRENT_HANDOVER.md",
    (
        "Cuatrecasas billing/email continuation — controlling 24 August route",
        "It may not move to transmission",
    ),
)

core_en = require(
    "en/cuatrecasas-sun-park/index.html",
    (
        "THE PACKAGE TAKEN TO LAS PALMAS",
        "sender-issued binding conditional offer",
        "integrated Elaia/Lagune EUR 26m downside route",
        "EUR 327,608.32",
    ),
)
core_es = require(
    "es/cuatrecasas-sun-park/index.html",
    (
        "EL PAQUETE LLEVADO A LAS PALMAS",
        "oferta vinculante condicionada emitida por el financiador",
        "ruta integrada Elaia/Lagune de 26 M EUR",
        "327.608,32 EUR",
    ),
)

route_markers = {
    "en/ona-hotels-insolvency-exit-36-2012/index.html": (
        "The package taken to Las Palmas",
        "12 JUN 2018 · 21:46",
        "The offer stage had therefore closed",
        'href="../cuatrecasas-sun-park/"',
    ),
    "es/ona-hotels-salida-concurso-36-2012/index.html": (
        "El paquete llevado a Las Palmas",
        "12 JUN 2018 · 21:46",
        "La fase de oferta había quedado, por tanto, cerrada",
        'href="../cuatrecasas-sun-park/"',
    ),
    "en/sun-park-takeover-7-june-2018/index.html": (
        "Stoneweg / Varia binding conditional offer",
        "documented Elaia/Lagune route",
        'href="../cuatrecasas-sun-park/"',
    ),
    "es/toma-control-sun-park-7-junio-2018/index.html": (
        "Oferta vinculante condicional Stoneweg / Varia",
        "ruta Elaia/Lagune documentada",
        'href="../cuatrecasas-sun-park/"',
    ),
    "en/index.html": (
        "Stoneweg binding conditional offer issued",
        "documented Elaia/Lagune downside route",
        'href="cuatrecasas-sun-park/"',
    ),
    "es/index.html": (
        "oferta vinculante condicional Stoneweg emitida",
        "ruta Elaia/Lagune documentada",
        'href="cuatrecasas-sun-park/"',
    ),
    "en/updates/index.html": (
        "cuatrecasas-package-billing-24aug",
        "Campaign research and drafting may resume",
    ),
    "es/actualizaciones/index.html": (
        "cuatrecasas-paquete-facturacion-24ago",
        "Pueden reanudarse investigación y preparación de borradores",
    ),
}
texts = {rel: require(rel, markers) for rel, markers in route_markers.items()}

stale_fragments = (
    "preliminary approval subject to ECO/65% LTV",
    "aprobación preliminar sujeta a ECO/65% LTV",
    "document whose filename/title was “Oferta Vinculante”",
    "documento de Stoneweg cuyo nombre/título era «Oferta Vinculante»",
    "indicative Lagune offer",
    "oferta Lagune indicativa",
    "separately documented EUR 26m downside-exit route",
    "vía separada de salida por 26 M EUR",
)
for rel, text in {**texts, "en-core": core_en, "es-core": core_es}.items():
    for fragment in stale_fragments:
        if fragment in text:
            errors.append(f"{rel}: stale fragment remains {fragment!r}")

for rel in ("en/updates/feed.xml", "es/actualizaciones/feed.xml"):
    path = ROOT / rel
    try:
        ET.parse(path)
    except Exception as exc:
        errors.append(f"{rel}: XML parse failed: {exc}")

try:
    state = json.loads((ROOT / "ops/CURRENT_STATE.json").read_text(encoding="utf-8"))
    cua = state["cuatrecasas"]
    if cua["communications_campaign"]["transmission_authorized"] is not False:
        errors.append("ops/CURRENT_STATE.json: transmission_authorized must be false")
    if not cua["communications_campaign"]["research_recipient_resolution_and_drafting_may_resume"]:
        errors.append("ops/CURRENT_STATE.json: campaign research/drafting readiness missing")
except Exception as exc:
    errors.append(f"ops/CURRENT_STATE.json: Cuatrecasas state invalid: {exc}")

try:
    tracked = subprocess.check_output(
        ["git", "ls-files"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
    ).splitlines()
    forbidden_names = (
        "CUATRECASAS_TIMECARD_TRANSCRIPTION_WORKING_",
        "CUATRECASAS_DISBURSEMENT_TRANSCRIPTION_WORKING_",
        "CUATRECASAS_BILLING_ACCOUNT_AND_EXPLANATION_DRAFT_",
    )
    for rel in tracked:
        if any(name in rel for name in forbidden_names):
            errors.append(f"private working artifact is tracked: {rel}")
except Exception as exc:
    errors.append(f"unable to inspect tracked private artifacts: {exc}")

if "No email may be sent" not in control or "exact recipients" not in handover:
    errors.append("send-authorization boundary is incomplete")

if errors:
    print("CUATRECASAS BILLING/EMAIL SYNC: FAIL")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print("CUATRECASAS BILLING/EMAIL SYNC: PASS")

#!/usr/bin/env python3
"""Validate the dedicated PP 1041 decisive-production publication."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "pp1041-single-most-important-production-20260820"

required = {
    "en/pp1041-single-most-important-production/index.html": [
        "THE SINGLE MOST IMPORTANT PRODUCTION",
        "The certified PP 1041/2017 file together with the Insolvency Administrator's internal authority, instruction and estate-interest record.",
        MARKER,
        "../../es/pp1041-produccion-documental-decisiva/",
    ],
    "es/pp1041-produccion-documental-decisiva/index.html": [
        "LA PRODUCCIÓN DOCUMENTAL MÁS IMPORTANTE",
        "El expediente certificado PP 1041/2017 junto con el expediente interno del Administrador concursal relativo a autoridad, instrucciones y análisis del interés de la masa.",
        MARKER,
        "../../en/pp1041-single-most-important-production/",
    ],
    "research/unitary-criminal-reverse-engineering/PP1041-SINGLE-MOST-IMPORTANT-PRODUCTION.md": [
        "THE SINGLE MOST IMPORTANT PRODUCTION",
        MARKER,
    ],
    "assets/unitary-criminal-reverse-engineering-20260820.js": [
        "pp1041-single-most-important-production",
        "pp1041-produccion-documental-decisiva",
        MARKER,
    ],
    "sitemap-criminal-engineering.xml": [
        "pp1041-single-most-important-production",
        "pp1041-produccion-documental-decisiva",
    ],
}

errors: list[str] = []
for rel, markers in required.items():
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"{rel}: missing marker {marker!r}")

structured = ROOT / "research/unitary-criminal-reverse-engineering/data/pp1041_decisive_production.json"
try:
    data = json.loads(structured.read_text(encoding="utf-8"))
    if data.get("marker") != MARKER:
        errors.append("structured PP 1041 record marker mismatch")
    if data.get("status") != "formal_allegation_pending_certified_primary_production":
        errors.append("structured PP 1041 record status mismatch")
    if len(data.get("p0_production") or []) < 15:
        errors.append("structured PP 1041 record must preserve at least 15 P0 production items")
except Exception as exc:
    errors.append(f"invalid structured PP 1041 record: {exc}")

# The dedicated pages must not autonomously attribute a voluntary withdrawal to LPB.
banned = [
    re.compile(r"\bLPB\s+(?:then\s+|later\s+)?withdrew\b", re.I),
    re.compile(r"\bLPB\s+desistió\b", re.I),
    re.compile(r"\bLPB\s+solicitó\s+el\s+desistimiento\b", re.I),
]
for rel in [
    "en/pp1041-single-most-important-production/index.html",
    "es/pp1041-produccion-documental-decisiva/index.html",
]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    for pattern in banned:
        if pattern.search(text):
            errors.append(f"{rel}: prohibited autonomous LPB-withdrawal wording: {pattern.pattern}")
    if re.search(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", text):
        errors.append(f"{rel}: email address leaked into public page")

if errors:
    print("PP 1041 DECISIVE PRODUCTION: FAIL")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print(f"PP 1041 DECISIVE PRODUCTION: PASS ({len(required)} controlled source groups)")

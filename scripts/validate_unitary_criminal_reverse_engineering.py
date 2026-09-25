#!/usr/bin/env python3
"""Validate the criminal-first Sun Park reverse-engineering architecture."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "unitary-criminal-reverse-engineering-20260820"

errors: list[str] = []

required = {
    "es/ingenieria-inversa-criminal-unitaria/index.html": [
        "¿Existió una sola empresa continuada y, en su caso, cómo convirtió crédito y control en título, financiación y explotación?",
        "Gil Marer y Aweswell alegan una sola empresa continuada de criminalidad económica, desarrollada mediante adopción sucesiva y división de funciones.",
        "Los quince puntos más fuertes",
        MARKER,
    ],
    "en/unitary-criminal-reverse-engineering/index.html": [
        "Was there one continuing enterprise and, if so, how did it convert credit and control into title, finance and operation?",
        "Gil Marer and Aweswell allege one continuing economic-criminal enterprise, advanced through successive adoption and divided functions.",
        "The fifteen strongest points",
        MARKER,
    ],
    "es/retracto-credito-litigioso-1041-2017/index.html": [
        "Se presentó un desistimiento en nombre de LPB",
        MARKER,
    ],
    "en/litigious-credit-retracto-1041-2017/index.html": [
        "A withdrawal was filed in LPB",
        MARKER,
    ],
    "es/administrador-concursal-puerta-credito-titulo/index.html": [
        "Se presentó un desistimiento en nombre de LPB",
        "Las nueve compuertas",
        MARKER,
    ],
    "en/insolvency-administrator-credit-to-title-gatekeeper/index.html": [
        "A withdrawal was filed in LPB",
        "The nine gates",
        MARKER,
    ],
    "assets/unitary-criminal-reverse-engineering-20260820.js": [
        MARKER,
        "unitaryCriminalGateway",
    ],
    "sitemap-criminal-engineering.xml": [
        "ingenieria-inversa-criminal-unitaria",
        "unitary-criminal-reverse-engineering",
    ],
}

for rel, markers in required.items():
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"{rel}: missing marker {marker!r}")

for rel in [
    "research/unitary-criminal-reverse-engineering/data/top_points.json",
    "research/unitary-criminal-reverse-engineering/data/offence_matrix.json",
    "research/unitary-criminal-reverse-engineering/data/critical_bridges.json",
]:
    path = ROOT / rel
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("marker") != MARKER:
            errors.append(f"{rel}: control marker mismatch")
    except Exception as exc:
        errors.append(f"{rel}: invalid JSON: {exc}")

# The controlling source rule applies to the PP 1041 and focused AC pages.
# A court decree may be reported as attributing a withdrawal request to LPB,
# but the site may not state as an independent fact that LPB voluntarily withdrew.
controlled_routes = [
    "es/retracto-credito-litigioso-1041-2017/index.html",
    "en/litigious-credit-retracto-1041-2017/index.html",
    "es/administrador-concursal-puerta-credito-titulo/index.html",
    "en/insolvency-administrator-credit-to-title-gatekeeper/index.html",
]

banned = [
    re.compile(r"\bLPB\s+desiste\b", re.I),
    re.compile(r"\bLPB\s+desistió\b", re.I),
    re.compile(r"\bLPB\s+solicitó\s+el\s+desistimiento\b", re.I),
    re.compile(r"\bLPB\s+(?:then\s+|later\s+)?withdrew\b", re.I),
    re.compile(r"\bLPB\s+requested\s+withdrawal\b", re.I),
    re.compile(r"\bLPB['’]s\s+(?:own\s+)?withdrawal\b", re.I),
]

for rel in controlled_routes:
    text = (ROOT / rel).read_text(encoding="utf-8")
    for pattern in banned:
        if pattern.search(text):
            errors.append(
                f"{rel}: prohibited autonomous-withdrawal attribution: {pattern.pattern}"
            )

# Keep private or privileged material out of the public/research output.
for root in [
    ROOT / "es/ingenieria-inversa-criminal-unitaria",
    ROOT / "en/unitary-criminal-reverse-engineering",
    ROOT / "research/unitary-criminal-reverse-engineering",
]:
    if not root.exists():
        continue
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in {".html", ".md", ".json"}:
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(
            r"\b[\w.+-]+@(gmail|cuatrecasas|jtparrilla|despachosantelmo)\.",
            text,
            re.I,
        ):
            errors.append(f"{path.relative_to(ROOT)}: private email address leaked")

if errors:
    print("UNITARY CRIMINAL REVERSE ENGINEERING: FAIL")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print(
    "UNITARY CRIMINAL REVERSE ENGINEERING: PASS "
    f"({len(required)} controlled sources; {len(controlled_routes)} withdrawal-attribution routes)"
)

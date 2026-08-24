#!/usr/bin/env python3
"""Validate the bilingual Cuatrecasas DP 748 / civil-action publication."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "cuatrecasas-dp748-civil-action-20260824"

ROUTES = {
    "es/cuatrecasas-dp748-accion-civil/index.html": [
        MARKER,
        "La tesis causal, sin sustitución de responsables",
        "DP 748/2026 no es la acción civil",
        "hipótesis principal y concreta",
        "Alcance público de la vía civil contemplada",
        "estimación parcial por insuficiencia de la motivación concreta",
        "esta página no afirma que se haya presentado notificación",
        "omite deliberadamente los nombres",
    ],
    "en/cuatrecasas-dp748-civil-action/index.html": [
        MARKER,
        "The causal thesis, without substituting defendants",
        "DP 748/2026 is not the civil action",
        "leading concrete hypothesis",
        "Public scope of the contemplated civil route",
        "partial allowance because the dismissal’s specific reasoning was insufficient",
        "this page does not state that a notification has been filed",
        "deliberately omits the names",
    ],
}

# These names are controlled only as a negative publication test. Their appearance
# here does not authorise their publication on either public route.
FORBIDDEN_CURRENT_TEAM_NAMES = (
    "Javier Sixto",
    "Estefanía Sixto",
    "Estefania Sixto",
    "Carlos Llamas",
    "Adriana Hernández",
    "Adriana Hernandez",
)

errors: list[str] = []
texts: dict[str, str] = {}
for rel, markers in ROUTES.items():
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing route: {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    texts[rel] = text
    for marker in markers:
        if marker not in text:
            errors.append(f"{rel}: missing marker {marker!r}")
    for name in FORBIDDEN_CURRENT_TEAM_NAMES:
        if name.casefold() in text.casefold():
            errors.append(f"{rel}: current legal-team identity leaked")

required_shared = (
    "Acosta Matos",
    "DP 748/2026",
    "ETJ 163/2020",
    "KYC/AML",
    "SRA",
)
for marker in required_shared:
    for rel, text in texts.items():
        if marker not in text:
            errors.append(f"{rel}: missing shared proposition {marker!r}")

for rel in (
    "sitemap.xml",
    "sitemap-legal-advisers.xml",
    "README.md",
    "assets/data/unitary-route-registry-v1.json",
):
    text = (ROOT / rel).read_text(encoding="utf-8")
    for slug in ("cuatrecasas-dp748-accion-civil", "cuatrecasas-dp748-civil-action"):
        if slug not in text:
            errors.append(f"{rel}: missing route {slug}")

manifest_path = ROOT / "publication-manifests/cuatrecasas-dp748-civil-action-20260824.json"
try:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("control_marker") != MARKER:
        errors.append("publication manifest marker mismatch")
except Exception as exc:
    errors.append(f"invalid publication manifest: {exc}")

if errors:
    print("CUATRECASAS DP748 / CIVIL ACTION: FAIL")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print("CUATRECASAS DP748 / CIVIL ACTION: PASS (2 bilingual routes; privacy lock active)")

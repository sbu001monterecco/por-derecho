#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

required = [
    "archive/MONTELANZA_2008_GOVERNANCE_ORIGIN_CRIMINAL_FORENSIC_CONTROL_21AUG2026.md",
    "archive/MONTELANZA_2008_GOVERNANCE_ORIGIN_RETRIEVAL_GATE_21AUG2026.md",
    "assets/data/montelanza-2008/manifest.json",
    "assets/data/montelanza-2008/governance-origin-v1.json",
    "assets/montelanza-governance-origin-20260821.js",
    "assets/site.js",
    "es/montelanza-cuentas-2008/index.html",
    "en/montelanza-accounts-2008/index.html",
    "sitemap-montelanza-governance-origin.xml",
    "publication-manifests/montelanza-governance-origin-2026-08-21.json",
    "operations/MONTELANZA_GOVERNANCE_ORIGIN_ACTIVATION_2026-08-21.md",
    "archive/THREAD_DELETION_AUDIT_MONTELANZA_GOVERNANCE_ORIGIN_21AUG2026.md",
]

for rel in required:
    if not (ROOT / rel).exists():
        errors.append(f"missing required file: {rel}")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


for rel in [
    "assets/data/montelanza-2008/manifest.json",
    "assets/data/montelanza-2008/governance-origin-v1.json",
    "publication-manifests/montelanza-governance-origin-2026-08-21.json",
]:
    try:
        json.loads(read(rel))
    except Exception as exc:
        errors.append(f"invalid JSON {rel}: {exc}")

try:
    governance = json.loads(read("assets/data/montelanza-2008/governance-origin-v1.json"))
    boundary = governance.get("sourceBoundary", {})
    for key in [
        "purchaserIdentityProvedByAccounts",
        "communitySuccessionProvedByAccounts",
        "criminalCaptureProved",
        "historicalRicEqualsLaterRicpe",
    ]:
        if boundary.get(key) is not False:
            errors.append(f"governance source boundary must keep {key}=false")
    if boundary.get("scanControlsOverOcr") is not True:
        errors.append("scanControlsOverOcr must be true")
except Exception:
    pass

chunks = [
    "01-06", "07-09", "10-12", "13-15", "16-18", "19-21",
    "22-24", "25-27", "28-30", "31-33", "34-36", "37-38",
]
ocr_text = ""
for chunk in chunks:
    rel = f"assets/data/montelanza-2008/ocr-pages-{chunk}.txt"
    path = ROOT / rel
    if not path.exists():
        errors.append(f"missing OCR chunk: {rel}")
        continue
    body = path.read_text(encoding="utf-8")
    if len(body.encode("utf-8")) < 500:
        errors.append(f"OCR chunk is implausibly small: {rel}")
    upper = body.upper()
    for forbidden in ["TEMPORARY", "PLACEHOLDER", "THIS PATH WILL BE REPLACED"]:
        if forbidden in upper:
            errors.append(f"OCR chunk contains forbidden placeholder text: {rel}")
    ocr_text += "\n" + body

pages = [int(value) for value in re.findall(r"===== SOURCE PDF PAGE (\d+) / 38 =====", ocr_text)]
if pages != list(range(1, 39)):
    errors.append(f"OCR page markers must be exactly 1..38 in order; got {pages}")

checks: dict[str, list[str]] = {
    "es/montelanza-cuentas-2008/index.html": [
        'data-montelanza-page="20260821"',
        "Montelanza 2008",
        "1.368.000",
        "11 locales",
        "2008 → 2011",
        "no prueban",
        "'37-38'",
        "../actores-privados-per-comunero-administracion-de-hecho/",
    ],
    "en/montelanza-accounts-2008/index.html": [
        'data-montelanza-page="20260821"',
        "Montelanza 2008",
        "EUR 1,368,000",
        "11 unsold premises",
        "2008 → 2011",
        "do not prove",
        "'37-38'",
        "../private-actors-related-party-community-de-facto-administration/",
    ],
    "assets/montelanza-governance-origin-20260821.js": [
        "montelanzaGovernanceOrigin",
        "es/montelanza-cuentas-2008/",
        "en/montelanza-accounts-2008/",
        "do not prove criminal capture",
        "No prueban una captura criminal",
    ],
    "assets/site.js": [
        "montelanza-governance-origin-20260821.js?v=20260821a",
        "data-montelanza-governance-origin-loader",
    ],
    "sitemap-montelanza-governance-origin.xml": [
        "es/montelanza-cuentas-2008/",
        "en/montelanza-accounts-2008/",
        "hreflang=\"es\"",
        "hreflang=\"en\"",
    ],
}
for rel, markers in checks.items():
    path = ROOT / rel
    if not path.exists():
        continue
    body = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in body:
            errors.append(f"{rel} missing marker: {marker}")

es = read("es/montelanza-cuentas-2008/index.html") if (ROOT / "es/montelanza-cuentas-2008/index.html").exists() else ""
en = read("en/montelanza-accounts-2008/index.html") if (ROOT / "en/montelanza-accounts-2008/index.html").exists() else ""
if 'hreflang="en" href="https://sbu001monterecco.github.io/por-derecho/en/montelanza-accounts-2008/"' not in es:
    errors.append("Spanish page missing English hreflang")
if 'hreflang="es" href="https://sbu001monterecco.github.io/por-derecho/es/montelanza-cuentas-2008/"' not in en:
    errors.append("English page missing Spanish hreflang")

for rel in [
    "es/montelanza-cuentas-2008/index.html",
    "en/montelanza-accounts-2008/index.html",
    "assets/montelanza-governance-origin-20260821.js",
]:
    if not (ROOT / rel).exists():
        continue
    lower = read(rel).lower()
    for phrase in [
        "criminal capture is proved",
        "proved criminal capture",
        "captura criminal probada",
        "demuestra la captura criminal",
        "every community act was criminal",
        "todos los actos comunitarios fueron criminales",
        "historic ric proves",
        "el ric histórico prueba",
    ]:
        if phrase in lower:
            errors.append(f"forbidden public overstatement in {rel}: {phrase}")

control = read(required[0]) if (ROOT / required[0]).exists() else ""
for marker in [
    "The 2008 filing does **not** by itself prove",
    "CRIMINAL-FORENSIC HYPOTHESIS — NOT PROVED",
    "Strongest lawful explanation",
    "MONTELANZA HISTORIC RIC/DIC",
]:
    if marker not in control:
        errors.append(f"canonical control missing source-boundary marker: {marker}")

if errors:
    print("\n".join(f"ERROR: {error}" for error in errors))
    sys.exit(1)

print("Montelanza governance-origin validation: OK")

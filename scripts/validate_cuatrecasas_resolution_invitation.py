#!/usr/bin/env python3
"""Validate the bilingual public-safe Cuatrecasas resolution invitation."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ROUTES = {
    "en/cuatrecasas-sun-park/index.html": (
        'id="resolution-invitation"',
        "OPEN RESOLUTION LANE · 24 AUGUST 2026",
        "Aweswell has invited Cuatrecasas to reconcile the complete account and talk.",
        "One interlocutor",
        "One bridge schedule",
        "One 45-minute call",
        "Controlled reconciliation",
        "Dialogue is open; rights and accountability routes remain preserved.",
        "No acceptance, standstill or resolution by Cuatrecasas is asserted.",
        "An unanswered invitation is recorded only as unanswered",
    ),
    "es/cuatrecasas-sun-park/index.html": (
        'id="invitacion-resolucion"',
        "VÍA ABIERTA DE RESOLUCIÓN · 24 AGOSTO 2026",
        "Aweswell ha invitado a Cuatrecasas a conciliar la cuenta completa y dialogar.",
        "Un interlocutor",
        "Un cuadro puente",
        "Una llamada de 45 minutos",
        "Conciliación controlada",
        "El diálogo está abierto; los derechos y vías de rendición de cuentas quedan preservados.",
        "No se afirma aceptación, espera ni resolución por parte de Cuatrecasas.",
        "Una invitación no contestada se registra únicamente como no contestada",
    ),
}

FORBIDDEN_PUBLIC_PATTERNS = (
    re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE),
    re.compile(r"\b1a03578d8f56e0e2\b", re.IGNORECASE),
    re.compile(r"\b(?:Javier\s+Sixto|Carlos\s+Llamas\s+Sanz)\b", re.IGNORECASE),
)

errors: list[str] = []
texts: dict[str, str] = {}
for rel, markers in ROUTES.items():
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing public route: {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    texts[rel] = text
    for marker in markers:
        if marker not in text:
            errors.append(f"{rel}: missing marker {marker!r}")
    for pattern in FORBIDDEN_PUBLIC_PATTERNS:
        if pattern.search(text):
            errors.append(f"{rel}: private/current-counsel material matched {pattern.pattern!r}")

if len(texts) == 2:
    for rel, text in texts.items():
        if text.count('class="resolutionstep"') != 4:
            errors.append(f"{rel}: expected exactly four resolution steps")
        if text.count('class="resolutionscope"') != 1:
            errors.append(f"{rel}: expected exactly one reconciliation-scope block")
        if "Spanish MASC" not in text and "MASC español" not in text:
            errors.append(f"{rel}: missing MASC non-initiation boundary")

control = ROOT / "archive/CUATRECASAS_RESOLUTION_INVITATION_PUBLIC_CONTROL_24AUG2026.md"
if not control.is_file():
    errors.append("missing resolution invitation control")
else:
    control_text = control.read_text(encoding="utf-8")
    for marker in (
        "cuatrecasas-resolution-invitation-20260824",
        "ONE RESPONSIBLE INTERLOCUTOR → ONE BRIDGE SCHEDULE → ONE 45-MINUTE CALL → CONTROLLED RECONCILIATION",
        "Keep Aweswell Limited, LPB and Matkator legally separate.",
        "Record silence only as unanswered.",
    ):
        if marker not in control_text:
            errors.append(f"control: missing marker {marker!r}")

manifest_path = ROOT / "publication-manifests/cuatrecasas-resolution-invitation-20260824.json"
if not manifest_path.is_file():
    errors.append("missing resolution invitation publication manifest")
else:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("publication_id") != "CUATRECASAS-RESOLUTION-INVITATION-20260824":
        errors.append("manifest: incorrect publication_id")
    safety = manifest.get("publication_safety", {})
    if any(value is not False for value in safety.values()):
        errors.append("manifest: every publication_safety risk flag must remain false")

if errors:
    print("CUATRECASAS RESOLUTION INVITATION: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("CUATRECASAS RESOLUTION INVITATION: PASS")
print("- bilingual four-step resolution lane present")
print("- private communication and current-counsel boundary preserved")
print("- non-admission, non-MASC, no-standstill and no-waiver controls present")

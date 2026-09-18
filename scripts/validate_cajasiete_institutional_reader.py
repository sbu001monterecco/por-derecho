#!/usr/bin/env python3
"""Validate the CajaSiete institutional-reader release and sent-link continuity."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

checks = {
    "es/cajasiete-responsabilidad-cumplimiento-trazabilidad/index.html": [
        "Registro público independiente",
        "Una parte directamente afectada. Una persona informante desde 2021.",
        "2021002141",
        "Cinco preguntas finitas para una respuesta institucional",
        "Precisión sobre la Comisión de Auditoría y Riesgos",
        "snapshots/2026-09-18-1716/",
    ],
    "en/cajasiete-accountability-compliance-traceability/index.html": [
        "Independent public record",
        "A directly affected party. A reporting person since 2021.",
        "2021002141",
        "Five finite questions for an institutional response",
        "Precision on the Audit & Risk Commission",
        "snapshots/2026-09-18-1716/",
    ],
    "es/cajasiete-sun-park-financiacion-comparabilidad/index.html": [
        "Dos carriles, una separación obligatoria",
        "cajasiete-responsabilidad-cumplimiento-trazabilidad",
    ],
    "en/cajasiete-sun-park-financing-comparability/index.html": [
        "Two lanes, one mandatory separation",
        "cajasiete-accountability-compliance-traceability",
    ],
    "es/registros-institucionales/index.html": [
        "18 septiembre 2026",
        "communication-PD-SP-EVT-0180",
    ],
    "en/institutional-records/index.html": [
        "18 September 2026",
        "communication-PD-SP-EVT-0180",
    ],
    "es/cajasiete-responsabilidad-cumplimiento-trazabilidad/snapshots/2026-09-18-1716/index.html": [
        "PD-CAJASIETE-ACCOUNTABILITY-20260918",
    ],
    "en/cajasiete-accountability-compliance-traceability/snapshots/2026-09-18-1716/index.html": [
        "PD-CAJASIETE-ACCOUNTABILITY-20260918",
    ],
}

errors = []
for rel, markers in checks.items():
    path = ROOT / rel
    if not path.exists():
        errors.append(f"missing: {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"{rel}: missing marker {marker!r}")

stale = ROOT / "archive/knowledge-project/SUN_PARK_PROFESSIONAL_ADVISERS_REPRESENTATIVES_REGISTER.md"
if stale.exists() and "Portfolio's 11 September response is registered as PD-SP-EVT-0180" in stale.read_text(encoding="utf-8"):
    errors.append("stale Portfolio PD-SP-EVT-0180 collision remains")

for rel in (
    "es/cajasiete-responsabilidad-cumplimiento-trazabilidad/index.html",
    "en/cajasiete-accountability-compliance-traceability/index.html",
):
    text = (ROOT / rel).read_text(encoding="utf-8")
    banned = ("culpabilidad institucional", "institutional-liability question")
    for phrase in banned:
        if phrase in text:
            errors.append(f"{rel}: superseded framing remains: {phrase}")

if errors:
    raise SystemExit("\n".join(errors))
print("CajaSiete institutional reader validation: OK")

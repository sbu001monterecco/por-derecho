#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

specs = {
    "en": {
        "page": ROOT / "en/index.html",
        "routes": [
            'href="recovery-command-center/"',
            'href="future/"',
            'href="por-derecho/"',
            'href="evidence/"',
            'href="updates/"',
            'href="legal-notebook/"',
        ],
        "copy": [
            "Three paths. Different purposes. Clear boundaries.",
            "How to read the record",
            "Understand the case in 60 seconds",
        ],
        "forbidden": ["institutional-capital/", 'href="#future"', 'class="capital-entry"', "data-private-actor-card="],
    },
    "es": {
        "page": ROOT / "es/index.html",
        "routes": [
            'href="centro-mando-recuperacion/"',
            'href="futuro/"',
            'href="por-derecho/"',
            'href="evidencia/"',
            'href="actualizaciones/"',
            'href="cuaderno-juridico/"',
        ],
        "copy": [
            "Tres vías. Propósitos distintos. Límites claros.",
            "Cómo leer el expediente",
            "Entender el caso en 60 segundos",
        ],
        "forbidden": ["capital-institucional/", 'href="#futuro"', 'class="capital-entry"', "data-private-actor-card="],
    },
}

for lang, spec in specs.items():
    page = spec["page"]
    if not page.exists():
        errors.append(f"missing homepage: {page.relative_to(ROOT)}")
        continue
    body = page.read_text(encoding="utf-8")
    for token in spec["routes"] + spec["copy"]:
        if token not in body:
            errors.append(f"{lang}/index.html missing homepage contract token: {token}")
    for token in spec["forbidden"]:
        if token in body:
            errors.append(f"{lang}/index.html violates homepage contract: {token}")
    if "../assets/sun-park-mynd-yaiza.jpg" not in body:
        errors.append(f"{lang}/index.html missing controlled hero asset")
    if body.count('class="panel"') < 8:
        errors.append(f"{lang}/index.html has insufficient orientation/status cards")

future = ROOT / "en/future/index.html"
futuro = ROOT / "es/futuro/index.html"
if not future.exists() or "../institutional-capital/" not in future.read_text(encoding="utf-8"):
    errors.append("en/future must retain controlled onward institutional-capital route")
if not futuro.exists() or "../capital-institucional/" not in futuro.read_text(encoding="utf-8"):
    errors.append("es/futuro must retain controlled onward capital-institucional route")

if errors:
    print("HOMEPAGE ORIENTATION CONTRACT: FAIL")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("HOMEPAGE ORIENTATION CONTRACT: PASS")

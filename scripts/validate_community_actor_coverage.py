#!/usr/bin/env python3
"""Keep the 2011–2016 actor register visual, source-led and non-conflating."""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FMMM_ASSET = "person.francisco-mario-matos-matas.primary"

PAGES = {
    "en/actors-parties-lawyers-representatives/index.html": (
        "Visual and digitisation register: 2011–2016 authority",
        "data-visual-asset-id=\"person.francisco-mario-matos-matas.primary\"",
        "it does not allocate responsibility",
        "Full OCR/ACTA X-ray remains outstanding",
        "does not itself establish collaboration or criminal intent by every attendee",
        "full digitisation of the native 2011 package and integrity custody of every original are not claimed complete",
    ),
    "es/actores-partes-abogados-representantes/index.html": (
        "Registro visual y de digitización: autoridad 2011–2016",
        "data-visual-asset-id=\"person.francisco-mario-matos-matas.primary\"",
        "no atribuye responsabilidad",
        "extracción OCR/acta-radiografía completa sigue pendiente",
        "No acredita por sí sola colaboración o intención criminal de toda persona presente",
        "la digitización íntegra del paquete nativo de 2011 y la custodia con integridad de todos los originales no se afirman completas",
    ),
}


def main() -> int:
    errors: list[str] = []

    for rel, required in PAGES.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for phrase in required:
            if phrase not in text:
                errors.append(f"{rel}: missing required actor-coverage control: {phrase!r}")

    register = (ROOT / "archive/SUN_PARK_ACTA_2011_2016_DIGITISATION_SOURCE_REGISTER_17AUG2026.md").read_text(encoding="utf-8")
    for phrase in (
        "22-Aug-2026 retrieval check",
        "scanned PDF with no machine-readable text",
        "must not be represented publicly as a fully transcribed or fully preserved repository item",
    ):
        if phrase not in register:
            errors.append(f"2011–2016 digitisation register: missing retrieval control: {phrase!r}")

    registry = json.loads((ROOT / "assets/visual-asset-registry.json").read_text(encoding="utf-8"))
    fmmm = registry.get("assets", {}).get(FMMM_ASSET, {})
    if fmmm.get("identity_status") != "LOCKED_CANONICAL_REPOSITORY_ASSET":
        errors.append("FMMM visual asset is not an active canonical asset")
    approved = fmmm.get("approved_contexts", [])
    if "Community authority / actor register" not in approved:
        errors.append("FMMM visual asset lacks actor-register publication approval")

    if errors:
        print("COMMUNITY ACTOR COVERAGE: FAIL")
        for item in errors:
            print(f" - {item}")
        return 1
    print("COMMUNITY ACTOR COVERAGE: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

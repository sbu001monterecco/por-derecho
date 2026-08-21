#!/usr/bin/env python3
"""Guard public continuity corrections that materially affect source status."""
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://sbu001monterecco.github.io/por-derecho"

CANONICALS = {
    "en/dp-1956-2026/index.html": f"{SITE}/en/dp-1956-2026/",
    "es/dp-1956-2026/index.html": f"{SITE}/es/dp-1956-2026/",
    "en/rsm/nnr4-1025c2f66/index.html": f"{SITE}/en/rsm/nnr4-1025c2f66/",
    "es/rsm/nnr4-1025c2f66/index.html": f"{SITE}/es/rsm/nnr4-1025c2f66/",
    "en/grant-thornton/2024-04/index.html": f"{SITE}/en/grant-thornton/2024-04/",
    "es/grant-thornton/2024-04/index.html": f"{SITE}/es/grant-thornton/2024-04/",
    "en/grant-thornton/cuyas-canarias/index.html": f"{SITE}/en/grant-thornton/cuyas-canarias/",
    "es/grant-thornton/cuyas-canarias/index.html": f"{SITE}/es/grant-thornton/cuyas-canarias/",
}

REQUIRED_TEXT = {
    "en/community-instrumentalisation/minutes-2011-2022/index.html": "The controlled Correos delivery proof records delivery of the notice.",
    "es/comunidad-instrumentalizacion/actas-2011-2022/index.html": "La prueba controlada de Correos acredita la entrega del aviso.",
    "en/updates/index.html": "controlled delivery proof for the 12 July burofax establishes delivery of the notice, not the truth or merits of its assertions.",
    "es/actualizaciones/index.html": "la prueba controlada de entrega del burofax de 12 julio acredita la entrega del aviso, no la verdad ni el fondo de sus afirmaciones.",
}

PROHIBITED_PUBLIC_TEXT = ("Control 24", "control 24")
JUDICIAL_SITEMAP = f"Sitemap: {SITE}/sitemap-judicial-spine.xml"


def main() -> int:
    errors: list[str] = []
    for rel, canonical in CANONICALS.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        if f'<link rel="canonical" href="{canonical}">' not in text:
            errors.append(f"{rel}: self canonical is missing or incorrect")
        if "https://aweswell.com/" in text:
            errors.append(f"{rel}: unavailable external canonical or alternate remains")

    for rel, expected in REQUIRED_TEXT.items():
        if expected not in (ROOT / rel).read_text(encoding="utf-8"):
            errors.append(f"{rel}: controlled 2016 delivery-proof wording is missing")

    for directory in (ROOT / "es", ROOT / "en"):
        for path in directory.rglob("index.html"):
            text = path.read_text(encoding="utf-8")
            if any(term in text for term in PROHIBITED_PUBLIC_TEXT):
                errors.append(f"{path.relative_to(ROOT)}: prohibited Control 24 shorthand")

    if JUDICIAL_SITEMAP not in (ROOT / "robots.txt").read_text(encoding="utf-8"):
        errors.append("robots.txt: judicial-spine sitemap is not declared")

    if errors:
        print("PUBLIC CONTINUITY CONTROLS: FAIL")
        for item in errors:
            print(f" - {item}")
        return 1
    print("PUBLIC CONTINUITY CONTROLS: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

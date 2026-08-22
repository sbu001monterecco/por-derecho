#!/usr/bin/env python3
"""Keep public criminal-law material evidence-led and actor-specific."""
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://sbu001monterecco.github.io/por-derecho"

CHARTERS = {
    "en/criminal-law-reading-rules/index.html": {
        "canonical": f"{SITE}/en/criminal-law-reading-rules/",
        "peer": f"{SITE}/es/reglas-lectura-derecho-penal/",
        "phrases": (
            "A sequence is not a plan; a relationship is not responsibility; receipt is not endorsement; an adverse decision or legal error is not criminal intent.",
            "Individual attribution",
            "strongest contrary evidence",
            "native records, confidential communications, personal data",
        ),
    },
    "es/reglas-lectura-derecho-penal/index.html": {
        "canonical": f"{SITE}/es/reglas-lectura-derecho-penal/",
        "peer": f"{SITE}/en/criminal-law-reading-rules/",
        "phrases": (
            "Una secuencia no es un plan; una relación no es responsabilidad; una recepción no es respaldo; una decisión adversa o un error jurídico no son dolo penal.",
            "Atribución individual",
            "prueba contraria más fuerte",
            "registros nativos, comunicaciones confidenciales, datos personales",
        ),
    },
}

ENGINE_PAGES = {
    "en/sun-park-criminal-engineering-investigation/index.html": (
        "A documentary sequence requires separate questions, not a collective conclusion.",
        "No person or entity is publicly categorised as an “enabler”.",
        "No public “enabler” scale",
    ),
    "es/ingenieria-forense-criminal-sun-park/index.html": (
        "Una secuencia documental exige preguntas separadas, no una conclusión colectiva.",
        "Ninguna persona o entidad se clasifica públicamente como «facilitadora».",
        "No existe una escala pública de «facilitación»",
    ),
}

BOUNDARY_TARGETS = (
    "/es/ingenieria-forense-criminal-sun-park/",
    "/en/sun-park-criminal-engineering-investigation/",
    "/es/ingenieria-inversa-criminal-unitaria/",
    "/en/unitary-criminal-reverse-engineering/",
    "/es/recuperacion-activos-intervencion-decomiso/",
    "/en/asset-recovery-intervention-confiscation/",
)

STALE_ENGINE_LABELS = (
    "LIVE INVESTIGATION · ARCHITECTURE · ENABLERS",
    "INVESTIGACIÓN VIVA · ARQUITECTURA · FACILITADORES",
    "E0–E7 enabler ladder",
    "Escala de facilitación E0–E7",
    "assisted by knowing, reckless, negligent or passive enablers",
    "asistidos por facilitadores conscientes, imprudentes, negligentes o pasivos",
)


def main() -> int:
    errors: list[str] = []

    for rel, expected in CHARTERS.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        if f'<link rel="canonical" href="{expected["canonical"]}">' not in text:
            errors.append(f"{rel}: self canonical is missing or incorrect")
        if f'hreflang="en" href="{expected["peer"]}"' not in text and f'hreflang="es" href="{expected["peer"]}"' not in text:
            errors.append(f"{rel}: bilingual alternate is missing")
        for phrase in expected["phrases"]:
            if phrase not in text:
                errors.append(f"{rel}: required public-boundary text is missing: {phrase!r}")

    for rel, phrases in ENGINE_PAGES.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"{rel}: required actor-specific safeguard is missing: {phrase!r}")
        for stale in STALE_ENGINE_LABELS:
            if stale in text:
                errors.append(f"{rel}: stale public categorisation remains: {stale!r}")

    module = (ROOT / "assets/criminal-public-boundaries-20260822.js").read_text(encoding="utf-8")
    for target in BOUNDARY_TARGETS:
        if target not in module:
            errors.append(f"criminal public-boundaries module: missing route {target}")
    for phrase in (
        "Evidence first. Individual attribution. No collective guilt.",
        "Prueba primero. Atribución individual. Sin culpabilidad colectiva.",
        "evidence-collection priority only",
        "prioridad de obtención de prueba",
    ):
        if phrase not in module:
            errors.append(f"criminal public-boundaries module: missing safeguard {phrase!r}")

    loader = (ROOT / "assets/site.js").read_text(encoding="utf-8")
    if "CRIMINAL-PUBLIC-BOUNDARIES-20260822" not in loader:
        errors.append("assets/site.js: criminal public-boundaries loader is missing")

    sitemap = (ROOT / "sitemap-prosecution-evidence.xml").read_text(encoding="utf-8")
    for url in (
        f"{SITE}/en/criminal-law-reading-rules/",
        f"{SITE}/es/reglas-lectura-derecho-penal/",
    ):
        if url not in sitemap:
            errors.append(f"sitemap-prosecution-evidence.xml: missing {url}")

    if errors:
        print("CRIMINAL PUBLIC BOUNDARIES: FAIL")
        for item in errors:
            print(f" - {item}")
        return 1
    print("CRIMINAL PUBLIC BOUNDARIES: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

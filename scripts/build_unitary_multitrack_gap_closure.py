#!/usr/bin/env python3
"""Install/check the additive unitary multi-track gap-closure surface.

The existing bilingual unitary reverse-engineering routes remain canonical.
This builder adds one deterministic mount and reciprocal specialist links; it
does not replace or abridge the existing long-form analysis.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_ID = "PD-UCF-20260901-01"
CSS = "unitary-multitrack-gap-closure-20260901.css?v=20260901c"
JS = "unitary-multitrack-gap-closure-20260901.js?v=20260901c"
OLD_CSS = "unitary-multitrack-gap-closure-20260901.css?v=20260901b"
OLD_JS = "unitary-multitrack-gap-closure-20260901.js?v=20260901b"

UNITARY_PAGES = {
    "es": ROOT / "es/ingenieria-inversa-criminal-unitaria/index.html",
    "en": ROOT / "en/unitary-criminal-reverse-engineering/index.html",
}

AUTHORITY_PAGES = {
    "es": ROOT / "es/actas-comunidad-autoridades-publicas/index.html",
    "en": ROOT / "en/community-actas-public-authorities/index.html",
}

PROPAGATION_SPECIALIST_PAGES = {
    "es": [
        ROOT / "es/administracion-de-hecho-comunidad-ac/index.html",
        ROOT / "es/concurso-36-2012-analisis-penal-forense-unitario/index.html",
        ROOT / "es/ric-private-equity-sun-park/index.html",
        ROOT / "es/intervencion-general-siinf-trazabilidad/index.html",
    ],
    "en": [
        ROOT / "en/de-facto-administration-community-ac/index.html",
        ROOT / "en/insolvency-36-2012-unitary-criminal-forensic-analysis/index.html",
        ROOT / "en/ric-private-equity-sun-park/index.html",
        ROOT / "en/intervencion-general-siinf-traceability/index.html",
    ],
}


def mount(locale: str) -> str:
    if locale == "es":
        loading = "Cargando reconstrucción unitaria multivía y registro canónico de brechas…"
        no_script = (
            "El control penal/fiscal primero requiere JavaScript para los filtros y el grafo. "
            "El análisis histórico completo continúa debajo; abra también el control LPH y el registro de autoridades."
        )
    else:
        loading = "Loading the unitary multi-track reconstruction and canonical gap register…"
        no_script = (
            "The criminal/prosecutorial-first control requires JavaScript for filters and the graph. "
            "The complete historic analysis continues below; also open the LPH control and authority register."
        )
    return (
        f'<section class="pd-ucf-mount" data-unitary-gap-closure data-ucf-control="{CONTROL_ID}">'
        f'<div class="pd-ucf"><p>{loading}</p><noscript><p class="pd-ucf-error">{no_script}</p></noscript></div>'
        "</section>"
    )


def install_unitary_page(text: str, locale: str) -> str:
    text = text.replace(OLD_CSS, CSS).replace(OLD_JS, JS)
    css_tag = f'<link rel="stylesheet" href="../../assets/{CSS}">'
    js_tag = f'<script src="../../assets/{JS}" defer></script>'
    if css_tag not in text:
        needle = '<link rel="stylesheet" href="../../assets/styles.css">'
        if needle not in text:
            raise ValueError(f"{locale}: base stylesheet marker missing")
        text = text.replace(needle, needle + css_tag, 1)
    if js_tag not in text:
        needle = '<script src="../../assets/site.js" defer></script>'
        if needle not in text:
            raise ValueError(f"{locale}: base script marker missing")
        text = text.replace(needle, needle + js_tag, 1)
    block = mount(locale)
    if f'data-ucf-control="{CONTROL_ID}"' not in text:
        if "<main>" not in text:
            raise ValueError(f"{locale}: main marker missing")
        text = text.replace("<main>", "<main>" + block, 1)
    return text


def install_propagation_link(text: str, locale: str) -> str:
    marker = 'data-ucf-authority-propagation-link="PD-UCF-20260901-01"'
    if locale == "es":
        link = "../ingenieria-inversa-criminal-unitaria/#unitary-authority-propagation"
        label = "Abrir la cadena unitaria autoridad → legitimidad aparente → uso"
        checkpoint_link = "../ingenieria-inversa-criminal-unitaria/#evidence-PD-EV-UCF-INT-184368-2026"
        checkpoint_label = "Primera respuesta de Intervención · evidencia canónica"
        communications_link = "../ingenieria-inversa-criminal-unitaria/#unitary-public-authority-communications"
        communications_label = "19 comunicaciones · tratamiento por nivel"
        body = (
            "Gil Marer/Aweswell alegan un mecanismo criminal organizado, coordinado y continuado; "
            "esta es una imputación directa que no debe reducirse a una mera controversia civil/LPH. "
            "La cadena exige prueba individual de cada actor, documento, recepción, conocimiento, uso, efecto y nexo; "
            "no es una declaración judicial de delito, organización o culpabilidad."
        )
    else:
        link = "../unitary-criminal-reverse-engineering/#unitary-authority-propagation"
        label = "Open the unitary authority → apparent legitimacy → use chain"
        checkpoint_link = "../unitary-criminal-reverse-engineering/#evidence-PD-EV-UCF-INT-184368-2026"
        checkpoint_label = "First Intervención response · canonical evidence"
        communications_link = "../unitary-criminal-reverse-engineering/#unitary-public-authority-communications"
        communications_label = "19 communications · handling by tier"
        body = (
            "Gil Marer/Aweswell allege an organised, coordinated and continuous criminal mechanism; "
            "this is a direct attribution that must not be reduced to a merely civil/LPH dispute. "
            "The chain requires individual proof of every actor, document, receipt, knowledge, use, effect and nexus; "
            "it is not an adjudicated finding of an offence, organisation or guilt."
        )
    block = (
        f'<aside class="note" {marker}><strong>{label}.</strong> {body} '
        f'<a href="{link}">{label} →</a> · '
        f'<a href="{checkpoint_link}">{checkpoint_label} →</a> · '
        f'<a href="{communications_link}">{communications_label} →</a></aside>'
    )
    if marker in text:
        if text.count(marker) != 1:
            raise ValueError(f"{locale}: specialist propagation marker is not unique")
        start = text.find(f'<aside class="note" {marker}>')
        end = text.find("</aside>", start)
        if start < 0 or end < 0:
            raise ValueError(f"{locale}: specialist propagation block is malformed")
        return text[:start] + block + text[end + len("</aside>"):]
    if "</main>" not in text:
        raise ValueError(f"{locale}: specialist main closing marker missing")
    return text.replace("</main>", block + "</main>", 1)


def install_authority_links(text: str, locale: str) -> str:
    if locale == "es":
        marker = '<a href="../comunidad-instrumentalizacion/sala-documental-actas/">Sala documental de ACTAs</a>'
        old_addition = (
            '<a href="../comunidad-instrumentalizacion/sala-documental-actas/control-lph-ciclo-juntas/">Control LPH · 122 referencias</a>'
            '<a href="../ingenieria-inversa-criminal-unitaria/#unitary-gap-register">Reconstrucción penal unitaria · brechas</a>'
        )
        addition = (
            '<a href="../comunidad-instrumentalizacion/sala-documental-actas/control-lph-ciclo-juntas/">Control LPH · 122 referencias</a>'
            '<a href="../ingenieria-inversa-criminal-unitaria/#unitary-gap-register">Reconstrucción penal unitaria · brechas</a>'
            '<a href="../ingenieria-inversa-criminal-unitaria/#unitary-public-authority-communications">19 comunicaciones · niveles y tratamiento</a>'
        )
    else:
        marker = '<a href="../community-instrumentalisation/acta-document-room/">ACTA document room</a>'
        old_addition = (
            '<a href="../community-instrumentalisation/acta-document-room/meeting-lifecycle-lph-control/">LPH control · 122 references</a>'
            '<a href="../unitary-criminal-reverse-engineering/#unitary-gap-register">Unitary criminal reconstruction · gaps</a>'
        )
        addition = (
            '<a href="../community-instrumentalisation/acta-document-room/meeting-lifecycle-lph-control/">LPH control · 122 references</a>'
            '<a href="../unitary-criminal-reverse-engineering/#unitary-gap-register">Unitary criminal reconstruction · gaps</a>'
            '<a href="../unitary-criminal-reverse-engineering/#unitary-public-authority-communications">19 communications · tiers and handling</a>'
        )
    if old_addition in text and addition not in text:
        text = text.replace(old_addition, addition, 1)
    elif addition not in text:
        if marker not in text:
            raise ValueError(f"{locale}: authority action marker missing")
        text = text.replace(marker, marker + addition, 1)
    return text


def update_sitemap(text: str) -> str:
    routes = (
        "https://sbu001monterecco.github.io/por-derecho/es/ingenieria-inversa-criminal-unitaria/",
        "https://sbu001monterecco.github.io/por-derecho/en/unitary-criminal-reverse-engineering/",
    )
    for route in routes:
        old = f"<loc>{route}</loc><lastmod>2026-08-26</lastmod>"
        new = f"<loc>{route}</loc><lastmod>2026-09-01</lastmod>"
        if old in text:
            text = text.replace(old, new, 1)
        elif new not in text:
            raise ValueError(f"specialist sitemap route/date marker missing: {route}")
    return text


def expected_files() -> dict[Path, str]:
    expected: dict[Path, str] = {}
    for locale, path in UNITARY_PAGES.items():
        expected[path] = install_unitary_page(path.read_text(encoding="utf-8"), locale)
    for locale, path in AUTHORITY_PAGES.items():
        expected[path] = install_authority_links(path.read_text(encoding="utf-8"), locale)
    for locale, pages in PROPAGATION_SPECIALIST_PAGES.items():
        for path in pages:
            expected[path] = install_propagation_link(path.read_text(encoding="utf-8"), locale)
    sitemap = ROOT / "sitemap-criminal-engineering.xml"
    expected[sitemap] = update_sitemap(sitemap.read_text(encoding="utf-8"))
    return expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        expected = expected_files()
    except (OSError, ValueError) as exc:
        print(f"UNITARY MULTI-TRACK BUILD: FAIL — {exc}", file=sys.stderr)
        return 1

    stale = [path for path, value in expected.items() if path.read_text(encoding="utf-8") != value]
    if args.check:
        if stale:
            for path in stale:
                print(f"stale: {path.relative_to(ROOT)}", file=sys.stderr)
            return 1
        print("UNITARY MULTI-TRACK BUILD: PASS — canonical routes and reciprocal links are current")
        return 0

    for path in stale:
        path.write_text(expected[path], encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")
    if not stale:
        print("unitary multi-track surfaces already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

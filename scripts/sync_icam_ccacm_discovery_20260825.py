#!/usr/bin/env python3
"""Synchronise ICAM/CCACM discovery surfaces and validate bilingual parity.

The script is intentionally idempotent. Use --apply to make the controlled
25-August-2026 synchronization; use --check in CI to verify that the public
surfaces remain aligned and evidence-bounded.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = "2026-08-25T19:34:00Z"


class SyncError(RuntimeError):
    pass


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        raise SyncError(f"missing required file: {rel}")
    return path.read_text(encoding="utf-8")


def write(rel: str, text: str, changed: list[str]) -> None:
    path = ROOT / rel
    old = path.read_text(encoding="utf-8")
    if text != old:
        path.write_text(text, encoding="utf-8")
        changed.append(rel)


def replace_once(text: str, old: str, new: str, rel: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SyncError(f"{rel}: expected one occurrence of {old!r}, found {count}")
    return text.replace(old, new, 1)


def update_four_body_pages(changed: list[str]) -> None:
    rel = "es/registros-institucionales-colegios-abogacia-2026/index.html"
    text = read(rel)
    text = text.replace(
        "<h2>Dos correos de hoy: qué añaden</h2>",
        "<h2>Dos correos del 25 de agosto de 2026: qué añaden</h2>",
        1,
    )
    write(rel, text, changed)

    rel = "en/institutional-records-bar-bodies-2026/index.html"
    text = read(rel)
    text = text.replace(
        "<h2>Today's two emails: what they add</h2>",
        "<h2>The two emails of 25 August 2026: what they add</h2>",
        1,
    )
    write(rel, text, changed)


def update_general_registers(changed: list[str]) -> None:
    rel = "es/registros-institucionales/index.html"
    text = read(rel)
    if "registros-institucionales-colegios-abogacia-2026/" not in text:
        text = replace_once(
            text,
            "Registro controlado por fuentes · verificado hasta 20 agosto 2026",
            "Registro controlado por fuentes · registros base verificados hasta 20 agosto 2026 · suplemento colegial actualizado a 25 agosto 2026",
            rel,
        )
        text = replace_once(text, '<a href="#records">Catorce registros</a>', '<a href="#records">Registros + suplemento</a>', rel)
        text = replace_once(
            text,
            "Catorce registros estables consolidan comunicaciones clave y referencias técnicas delimitadas relativas a organismos públicos, vías de administración judicial y corporaciones profesionales de derecho público de la arquitectura de control. Cada uno separa competencia, hitos trazables, límites probatorios y una acción finita pendiente.</p>",
            "Catorce registros base consolidan comunicaciones clave y referencias técnicas delimitadas relativas a organismos públicos, vías de administración judicial y corporaciones profesionales de derecho público de la arquitectura de control. Cada uno separa competencia, hitos trazables, límites probatorios y una acción finita pendiente. Un suplemento colegial actualizado a 25 de agosto de 2026 reúne, sin fusionarlos, ICAM, CCACM, ICALPA e ICATF.</p>",
            rel,
        )
        text = replace_once(
            text,
            "<strong>Catorce registros de organismos públicos, administración judicial y corporaciones profesionales de derecho público</strong>",
            "<strong>Catorce registros base + suplemento colegial ICAM · CCACM · ICALPA · ICATF</strong>",
            rel,
        )
        marker = '<aside class="ir-notice" aria-label="Aviso de identificación institucional">'
        supplement = (
            '<aside class="ir-notice" aria-label="Suplemento colegial 2026">'
            '<strong>Suplemento de regulación profesional · actualizado a 25 agosto 2026.</strong> '
            'El mapa separado <a href="../registros-institucionales-colegios-abogacia-2026/">ICAM · CCACM · ICALPA · ICATF</a> '
            'distingue primera instancia, alzada y competencia territorial. El expediente '
            '<a href="../cuatrecasas-icam-ccacm-2026/">Cuatrecasas · ICAM / CCACM</a> '
            'expone la cuestión limitada de conducta individual, decisión o supervisión de socio y controles de la sociedad profesional. '
            'Los dos acuses de 25 agosto acreditan recepción solamente; no aceptación, investigación general ni decisión de fondo.</aside>'
        )
        # Correct the deliberately split closing tag above without obscuring the public copy.
        if marker not in text:
            raise SyncError(f"{rel}: institutional notice marker not found")
        text = text.replace(marker, supplement + marker, 1)
    write(rel, text, changed)

    rel = "en/institutional-records/index.html"
    text = read(rel)
    if "institutional-records-bar-bodies-2026/" not in text:
        text = replace_once(
            text,
            "Source-controlled register · verified to 20 August 2026",
            "Source-controlled register · core records verified to 20 August 2026 · professional-regulation supplement updated to 25 August 2026",
            rel,
        )
        text = replace_once(text, '<a href="#records">Fourteen records</a>', '<a href="#records">Records + supplement</a>', rel)
        text = replace_once(
            text,
            "Fourteen stable records consolidate key communications and bounded technical-record references concerning public bodies, judicial-administration routes and statutory professional corporations shown or discussed in the accountability architecture. Each separates competence, traceable events, evidential limits and one finite outstanding action.</p>",
            "Fourteen core records consolidate key communications and bounded technical-record references concerning public bodies, judicial-administration routes and statutory professional corporations shown or discussed in the accountability architecture. Each separates competence, traceable events, evidential limits and one finite outstanding action. A professional-regulation supplement updated to 25 August 2026 maps ICAM, CCACM, ICALPA and ICATF without merging their files or competences.</p>",
            rel,
        )
        text = replace_once(
            text,
            "<strong>Fourteen public-body, judicial-administration and statutory professional-corporation records</strong>",
            "<strong>Fourteen core records + ICAM · CCACM · ICALPA · ICATF supplement</strong>",
            rel,
        )
        marker = '<aside class="ir-notice" aria-label="Institutional identification disclaimer">'
        supplement = (
            '<aside class="ir-notice" aria-label="2026 professional-regulation supplement">'
            '<strong>Professional-regulation supplement · updated 25 August 2026.</strong> '
            'The separate <a href="../institutional-records-bar-bodies-2026/">ICAM · CCACM · ICALPA · ICATF map</a> '
            'distinguishes first instance, appeal and territorial competence. The '
            '<a href="../cuatrecasas-icam-ccacm-2026/">Cuatrecasas · ICAM / CCACM record</a> '
            'sets out the bounded individual, partner-decision and professional-firm-control questions. '
            'The two 25 August acknowledgements prove receipt only—not acceptance, a general investigation or a merits decision.</aside>'
        )
        if marker not in text:
            raise SyncError(f"{rel}: institutional notice marker not found")
        text = text.replace(marker, supplement + marker, 1)
    write(rel, text, changed)


def insert_home_card(rel: str, href: str, card: str, changed: list[str]) -> None:
    text = read(rel)
    if href in text:
        write(rel, text, changed)
        return
    marker = "assets/institutions/icalpa.png"
    pos = text.find(marker)
    if pos < 0:
        raise SyncError(f"{rel}: ICALPA identity-card marker not found")
    section_start = text.rfind('<section class="identity-group"', 0, pos)
    section_end = text.find("</section>", pos)
    if section_start < 0 or section_end < 0:
        raise SyncError(f"{rel}: deontology identity section boundaries not found")
    grid_close = text.rfind("</div>", section_start, section_end)
    if grid_close < 0:
        raise SyncError(f"{rel}: identity-logo-grid closing div not found")
    text = text[:grid_close] + card + text[grid_close:]
    write(rel, text, changed)


def update_homepages(changed: list[str]) -> None:
    es_card = (
        '\n                <a class="identity-logo-card" href="registros-institucionales-colegios-abogacia-2026/" '
        'aria-label="Abrir el mapa colegial 2026 de ICAM, CCACM, ICALPA e ICATF">\n'
        '                  <span class="identity-logo-frame"><span class="identity-wordmark" aria-hidden="true">ICAM · CCACM<small>Madrid + Canarias</small></span></span>\n'
        '                  <span class="identity-logo-copy"><strong>Mapa colegial 2026 — ICAM · CCACM · ICALPA · ICATF</strong><small>Competencias separadas, recursos, acuses y preguntas abiertas</small></span><span class="identity-external" aria-hidden="true">→</span>\n'
        '                </a>\n              '
    )
    insert_home_card(
        "es/index.html",
        "registros-institucionales-colegios-abogacia-2026/",
        es_card,
        changed,
    )

    en_card = (
        '\n                <a class="identity-logo-card" href="institutional-records-bar-bodies-2026/" '
        'aria-label="Open the 2026 ICAM, CCACM, ICALPA and ICATF professional-regulation map">\n'
        '                  <span class="identity-logo-frame"><span class="identity-wordmark" aria-hidden="true">ICAM · CCACM<small>Madrid + Canary Islands</small></span></span>\n'
        '                  <span class="identity-logo-copy"><strong>2026 professional-regulation map — ICAM · CCACM · ICALPA · ICATF</strong><small>Separate competence, appeals, acknowledgements and open questions</small></span><span class="identity-external" aria-hidden="true">→</span>\n'
        '                </a>\n              '
    )
    insert_home_card(
        "en/index.html",
        "institutional-records-bar-bodies-2026/",
        en_card,
        changed,
    )


def update_sitemap(changed: list[str]) -> None:
    rel = "sitemap.xml"
    text = read(rel)
    routes = {
        "es_dedicated": "https://sbu001monterecco.github.io/por-derecho/es/cuatrecasas-icam-ccacm-2026/",
        "en_dedicated": "https://sbu001monterecco.github.io/por-derecho/en/cuatrecasas-icam-ccacm-2026/",
        "es_map": "https://sbu001monterecco.github.io/por-derecho/es/registros-institucionales-colegios-abogacia-2026/",
        "en_map": "https://sbu001monterecco.github.io/por-derecho/en/institutional-records-bar-bodies-2026/",
    }
    if routes["es_dedicated"] not in text:
        blocks = f'''  <url>
    <loc>{routes["es_dedicated"]}</loc><lastmod>2026-08-25</lastmod>
    <xhtml:link rel="alternate" hreflang="es" href="{routes["es_dedicated"]}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{routes["en_dedicated"]}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{routes["en_dedicated"]}"/>
  </url>
  <url>
    <loc>{routes["en_dedicated"]}</loc><lastmod>2026-08-25</lastmod>
    <xhtml:link rel="alternate" hreflang="es" href="{routes["es_dedicated"]}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{routes["en_dedicated"]}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{routes["en_dedicated"]}"/>
  </url>
  <url>
    <loc>{routes["es_map"]}</loc><lastmod>2026-08-25</lastmod>
    <xhtml:link rel="alternate" hreflang="es" href="{routes["es_map"]}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{routes["en_map"]}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{routes["en_map"]}"/>
  </url>
  <url>
    <loc>{routes["en_map"]}</loc><lastmod>2026-08-25</lastmod>
    <xhtml:link rel="alternate" hreflang="es" href="{routes["es_map"]}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{routes["en_map"]}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{routes["en_map"]}"/>
  </url>
'''
        if "</urlset>" not in text:
            raise SyncError("sitemap.xml: closing urlset not found")
        text = text.replace("</urlset>", blocks + "</urlset>", 1)
    write(rel, text, changed)


def update_updates_pages(changed: list[str]) -> None:
    rel = "es/actualizaciones/index.html"
    text = read(rel)
    if 'id="icam-ccacm-control-institucional-25ago"' not in text:
        marker = '    <section class="updates-section">'
        entry = '''    <section class="updates-section"><div class="shell"><section class="date-group" aria-labelledby="fecha-icam-ccacm-25ago"><h2 id="fecha-icam-ccacm-25ago">25 agosto 2026 · ICAM / CCACM</h2><div class="update-stream"><article class="material-update institutional" id="icam-ccacm-control-institucional-25ago"><div class="update-meta"><span class="new">Registro fortalecido</span><span>ICAM</span><span>CCACM 193/2026</span><span>Control deontológico</span></div><h3>La ruta dedicada existente distingue conducta individual, decisión de socio y controles de la sociedad profesional</h3><p>La página bilingüe Cuatrecasas–ICAM/CCACM se ha reforzado como ayuda de decisión institucional: presenta la defensa más fuerte de Cuatrecasas, ocho preguntas finitas capaces también de exonerar, la separación entre ICAM, CCACM, ICALPA e ICATF y el precedente técnico 493/26 para interpretar 1566/26 sin presumir su efectiva remisión.</p><p><strong>Estado a 25 agosto:</strong> CCACM confirmó por dos correos separados la recepción de la aportación sobre hechos posteriores y de dos anexos gráficos. Cada “RECIBIDO” acredita recepción solamente. No se ha localizado resolución final en 193/2026, aceptación de las alegaciones, investigación general de la firma ni número CCACM para la segunda alzada.</p><p><strong>Decisión de comunicación:</strong> no se envió una nueva respuesta. El expediente queda en espera de un requerimiento, trámite, providencia, propuesta, resolución, certificación materialmente relevante o hecho verdaderamente sobrevenido.</p><div class="update-links"><a href="../cuatrecasas-icam-ccacm-2026/">Abrir el expediente ICAM / CCACM →</a><a href="../registros-institucionales-colegios-abogacia-2026/">Mapa de los cuatro colegios/consejos →</a><a href="../../en/cuatrecasas-icam-ccacm-2026/" lang="en">English →</a></div></article></div></section></div></section>\n\n'''
        if marker not in text:
            raise SyncError(f"{rel}: updates-section marker not found")
        text = text.replace(marker, entry + marker, 1)
    write(rel, text, changed)

    rel = "en/updates/index.html"
    text = read(rel)
    if 'id="icam-ccacm-institutional-control-25aug"' not in text:
        marker = '    <section class="updates-section">'
        entry = '''    <section class="updates-section"><div class="shell"><section class="date-group" aria-labelledby="date-icam-ccacm-25aug"><h2 id="date-icam-ccacm-25aug">25 August 2026 · ICAM / CCACM</h2><div class="update-stream"><article class="material-update institutional" id="icam-ccacm-institutional-control-25aug"><div class="update-meta"><span class="new">Strengthened record</span><span>ICAM</span><span>CCACM 193/2026</span><span>Professional conduct</span></div><h3>The existing dedicated route now separates individual conduct, partner decision-making and professional-firm controls</h3><p>The bilingual Cuatrecasas–ICAM/CCACM page has been strengthened as an institutional decision aid. It presents Cuatrecasas' strongest defence, eight finite questions also capable of exonerating, the separation between ICAM, CCACM, ICALPA and ICATF, and the 493/26 technical-intake precedent for interpreting 1566/26 without presuming effective forwarding.</p><p><strong>Status at 25 August:</strong> CCACM sent two separate acknowledgements confirming receipt of the later-facts supplement and two visual annexes. Each “RECIBIDO” proves receipt only. No final 193/2026 decision, acceptance of the allegations, general firm investigation or CCACM number for the second appeal has been located.</p><p><strong>Communication decision:</strong> no new response was sent. The record remains on hold pending a request, hearing step, procedural order, proposal, decision, materially relevant routing certificate or genuinely supervening fact.</p><div class="update-links"><a href="../cuatrecasas-icam-ccacm-2026/">Open the ICAM / CCACM record →</a><a href="../institutional-records-bar-bodies-2026/">Open the four-body map →</a><a href="../../es/cuatrecasas-icam-ccacm-2026/" lang="es">Español →</a></div></article></div></section></div></section>\n\n'''
        if marker not in text:
            raise SyncError(f"{rel}: updates-section marker not found")
        text = text.replace(marker, entry + marker, 1)
    write(rel, text, changed)


def update_feeds(changed: list[str]) -> None:
    rel = "es/actualizaciones/feed.xml"
    text = read(rel)
    if "#icam-ccacm-control-institucional-25ago" not in text:
        text = re.sub(r"<updated>[^<]+</updated>", f"<updated>{STAMP}</updated>", text, count=1)
        marker = "  <author><name>Project Sun Rock</name></author>"
        entry = f'''\n  <entry>
    <title>ICAM / CCACM: fortalecido el registro institucional y aplicada la regla de no respuesta</title>
    <id>https://sbu001monterecco.github.io/por-derecho/es/actualizaciones/#icam-ccacm-control-institucional-25ago</id>
    <link href="https://sbu001monterecco.github.io/por-derecho/es/cuatrecasas-icam-ccacm-2026/"/>
    <link rel="related" href="https://sbu001monterecco.github.io/por-derecho/es/registros-institucionales-colegios-abogacia-2026/"/>
    <published>{STAMP}</published>
    <updated>{STAMP}</updated>
    <summary>La ruta dedicada existente distingue conducta individual, decisión o supervisión de socio y controles de la sociedad profesional; presenta la defensa más fuerte y ocho preguntas también exculpatorias. Los dos RECIBIDO de 25 agosto prueban recepción solamente. No se ha localizado decisión final ni número CCACM de la segunda alzada, y no se envió una nueva respuesta sin un desencadenante procesal.</summary>
  </entry>'''
        if marker not in text:
            raise SyncError(f"{rel}: feed author marker not found")
        text = text.replace(marker, marker + entry, 1)
    write(rel, text, changed)

    rel = "en/updates/feed.xml"
    text = read(rel)
    if "#icam-ccacm-institutional-control-25aug" not in text:
        text = re.sub(r"<updated>[^<]+</updated>", f"<updated>{STAMP}</updated>", text, count=1)
        marker = "  <author><name>Project Sun Rock</name></author>"
        entry = f'''\n  <entry>
    <title>ICAM / CCACM: institutional record strengthened and no-response rule applied</title>
    <id>https://sbu001monterecco.github.io/por-derecho/en/updates/#icam-ccacm-institutional-control-25aug</id>
    <link href="https://sbu001monterecco.github.io/por-derecho/en/cuatrecasas-icam-ccacm-2026/"/>
    <link rel="related" href="https://sbu001monterecco.github.io/por-derecho/en/institutional-records-bar-bodies-2026/"/>
    <published>{STAMP}</published>
    <updated>{STAMP}</updated>
    <summary>The existing dedicated route separates individual conduct, partner authorisation or supervision and professional-firm controls, while presenting the strongest defence and eight questions also capable of exonerating. The two 25 August RECIBIDO messages prove receipt only. No final decision or CCACM number for the second appeal has been located, and no new response was sent without a procedural trigger.</summary>
  </entry>'''
        if marker not in text:
            raise SyncError(f"{rel}: feed author marker not found")
        text = text.replace(marker, marker + entry, 1)
    write(rel, text, changed)


def apply() -> list[str]:
    changed: list[str] = []
    update_four_body_pages(changed)
    update_general_registers(changed)
    update_homepages(changed)
    update_sitemap(changed)
    update_updates_pages(changed)
    update_feeds(changed)
    return changed


def require(rel: str, *needles: str) -> None:
    text = read(rel)
    for needle in needles:
        if needle not in text:
            raise SyncError(f"{rel}: missing required marker {needle!r}")


def forbid(rel: str, *needles: str) -> None:
    text = read(rel)
    for needle in needles:
        if needle in text:
            raise SyncError(f"{rel}: forbidden stale/overstated marker remains: {needle!r}")


def check() -> None:
    require(
        "es/registros-institucionales-colegios-abogacia-2026/index.html",
        "Dos correos del 25 de agosto de 2026",
        "Un acuse de recibo solo acredita recepción",
        "CCACM es Madrid",
    )
    forbid("es/registros-institucionales-colegios-abogacia-2026/index.html", "Dos correos de hoy")
    require(
        "en/institutional-records-bar-bodies-2026/index.html",
        "The two emails of 25 August 2026",
        "An acknowledgement proves receipt only",
        "CCACM is Madrid",
    )
    forbid("en/institutional-records-bar-bodies-2026/index.html", "Today's two emails")

    require(
        "es/registros-institucionales/index.html",
        "registros-institucionales-colegios-abogacia-2026/",
        "cuatrecasas-icam-ccacm-2026/",
        "Catorce registros base + suplemento colegial",
    )
    require(
        "en/institutional-records/index.html",
        "institutional-records-bar-bodies-2026/",
        "cuatrecasas-icam-ccacm-2026/",
        "Fourteen core records + ICAM",
    )
    require("es/index.html", "registros-institucionales-colegios-abogacia-2026/")
    require("en/index.html", "institutional-records-bar-bodies-2026/")

    for route in (
        "https://sbu001monterecco.github.io/por-derecho/es/cuatrecasas-icam-ccacm-2026/",
        "https://sbu001monterecco.github.io/por-derecho/en/cuatrecasas-icam-ccacm-2026/",
        "https://sbu001monterecco.github.io/por-derecho/es/registros-institucionales-colegios-abogacia-2026/",
        "https://sbu001monterecco.github.io/por-derecho/en/institutional-records-bar-bodies-2026/",
    ):
        require("sitemap.xml", route)

    require("es/actualizaciones/index.html", 'id="icam-ccacm-control-institucional-25ago"', "no se envió una nueva respuesta")
    require("en/updates/index.html", 'id="icam-ccacm-institutional-control-25aug"', "no new response was sent")
    require("es/actualizaciones/feed.xml", "#icam-ccacm-control-institucional-25ago", STAMP)
    require("en/updates/feed.xml", "#icam-ccacm-institutional-control-25aug", STAMP)

    require(
        "es/cuatrecasas-icam-ccacm-2026/index.html",
        "No está probada una conducta deontológica generalizada de toda la firma",
        "Recepción no es admisión, acuerdo ni valoración",
    )
    require(
        "en/cuatrecasas-icam-ccacm-2026/index.html",
        "Firm-wide misconduct has not been proved",
        "Receipt is not admissibility, agreement or evaluation",
    )

    print("ICAM/CCACM discovery and evidential-boundary validation passed")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        if args.apply:
            changed = apply()
            check()
            print("changed files:")
            for rel in changed:
                print(f" - {rel}")
        else:
            check()
    except SyncError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

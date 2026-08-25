#!/usr/bin/env python3
"""One-off discovery patch for the David Espejo bilingual evidence release."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = "2026-08-25T18:30:00Z"


def insert_before(path: Path, closing: str, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    if closing not in text:
        raise RuntimeError(f"{path}: closing anchor not found: {closing}")
    path.write_text(text.replace(closing, block + "\n" + closing, 1), encoding="utf-8")


def update_feed(path: Path, marker: str, entry: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<updated>[^<]+</updated>", f"<updated>{STAMP}</updated>", text, count=1)
    if marker not in text:
        if "<entry>" in text:
            text = text.replace("<entry>", entry + "\n  <entry>", 1)
        elif "</feed>" in text:
            text = text.replace("</feed>", entry + "\n</feed>", 1)
        else:
            raise RuntimeError(f"{path}: no Atom entry insertion point")
    path.write_text(text, encoding="utf-8")


def update_sitemap(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    marker = "/es/actualizaciones/david-espejo-evidencia-pericial/"
    if marker in text:
        return
    block = """  <url>
    <loc>https://sbu001monterecco.github.io/por-derecho/es/actualizaciones/david-espejo-evidencia-pericial/</loc>
    <lastmod>2026-08-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
    <xhtml:link rel=\"alternate\" hreflang=\"es\" href=\"https://sbu001monterecco.github.io/por-derecho/es/actualizaciones/david-espejo-evidencia-pericial/\"/>
    <xhtml:link rel=\"alternate\" hreflang=\"en\" href=\"https://sbu001monterecco.github.io/por-derecho/en/updates/david-espejo-expert-evidence/\"/>
    <xhtml:link rel=\"alternate\" hreflang=\"x-default\" href=\"https://sbu001monterecco.github.io/por-derecho/es/actualizaciones/david-espejo-evidencia-pericial/\"/>
  </url>
  <url>
    <loc>https://sbu001monterecco.github.io/por-derecho/en/updates/david-espejo-expert-evidence/</loc>
    <lastmod>2026-08-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
    <xhtml:link rel=\"alternate\" hreflang=\"es\" href=\"https://sbu001monterecco.github.io/por-derecho/es/actualizaciones/david-espejo-evidencia-pericial/\"/>
    <xhtml:link rel=\"alternate\" hreflang=\"en\" href=\"https://sbu001monterecco.github.io/por-derecho/en/updates/david-espejo-expert-evidence/\"/>
    <xhtml:link rel=\"alternate\" hreflang=\"x-default\" href=\"https://sbu001monterecco.github.io/por-derecho/es/actualizaciones/david-espejo-evidencia-pericial/\"/>
  </url>"""
    if "</urlset>" not in text:
        raise RuntimeError("sitemap-david-espejo.xml: closing urlset not found")
    path.write_text(text.replace("</urlset>", block + "\n</urlset>", 1), encoding="utf-8")


def main() -> None:
    es_home = """
<section class=\"section alt\" data-david-espejo-home-route=\"20260825\">
  <div class=\"shell\"><p class=\"eyebrow\">NUEVO NODO DE PRUEBA PERICIAL</p><h2>David Espejo / eXW: versión, custodia, presentación y uso judicial</h2><p>Cuatro finales firmados, dos anexos identificados en la oposición de LPB y una cuestión de acceso a las versiones del expediente antes de la vista, con límites probatorios expresos.</p><p><a class=\"button\" href=\"david-espejo-perito-forense/\">Abrir el expediente pericial →</a> <a class=\"button secondary\" href=\"actualizaciones/david-espejo-evidencia-pericial/\">Leer la actualización →</a></p></div>
</section>"""
    en_home = """
<section class=\"section alt\" data-david-espejo-home-route=\"20260825\">
  <div class=\"shell\"><p class=\"eyebrow\">NEW EXPERT-EVIDENCE NODE</p><h2>David Espejo / eXW: version, custody, filing and judicial use</h2><p>Four signed finals, two identified annexes in LPB’s opposition and a pre-hearing court-file version issue, with express evidential limits.</p><p><a class=\"button\" href=\"david-espejo-expert-witness/\">Open the expert-evidence dossier →</a> <a class=\"button secondary\" href=\"updates/david-espejo-expert-evidence/\">Read the update →</a></p></div>
</section>"""
    es_updates = """
<section class=\"section alt\" data-david-espejo-update-card=\"20260825\">
  <div class=\"shell\"><p class=\"eyebrow\">25 AGOSTO 2026 · PRUEBA PERICIAL</p><h2>David Espejo / eXW: matriz de procedencia actualizada</h2><p>La publicación distingue cuatro informes firmados, dos anexos identificados, el acceso a versiones antes de la vista y el uso judicial posterior, sin convertir las cuestiones abiertas en acusaciones.</p><p><a class=\"button\" href=\"david-espejo-evidencia-pericial/\">Leer la actualización →</a></p></div>
</section>"""
    en_updates = """
<section class=\"section alt\" data-david-espejo-update-card=\"20260825\">
  <div class=\"shell\"><p class=\"eyebrow\">25 AUGUST 2026 · EXPERT EVIDENCE</p><h2>David Espejo / eXW: updated provenance matrix</h2><p>The release distinguishes four signed reports, two identified annexes, pre-hearing version access and later judicial use without converting open questions into allegations.</p><p><a class=\"button\" href=\"david-espejo-expert-evidence/\">Read the update →</a></p></div>
</section>"""

    insert_before(ROOT / "es/index.html", "</main>", "data-david-espejo-home-route", es_home)
    insert_before(ROOT / "en/index.html", "</main>", "data-david-espejo-home-route", en_home)
    insert_before(ROOT / "es/actualizaciones/index.html", "</main>", "data-david-espejo-update-card", es_updates)
    insert_before(ROOT / "en/updates/index.html", "</main>", "data-david-espejo-update-card", en_updates)

    es_entry = """  <entry>
    <title>David Espejo / eXW: matriz de procedencia y uso judicial actualizada</title>
    <id>https://sbu001monterecco.github.io/por-derecho/es/actualizaciones/david-espejo-evidencia-pericial/</id>
    <link href=\"https://sbu001monterecco.github.io/por-derecho/es/actualizaciones/david-espejo-evidencia-pericial/\"/>
    <updated>2026-08-25T18:30:00Z</updated>
    <summary>Cuatro informes firmados, dos anexos identificados y una cuestión de versión antes de la vista, con límites probatorios expresos.</summary>
  </entry>"""
    en_entry = """  <entry>
    <title>David Espejo / eXW: updated provenance and judicial-use matrix</title>
    <id>https://sbu001monterecco.github.io/por-derecho/en/updates/david-espejo-expert-evidence/</id>
    <link href=\"https://sbu001monterecco.github.io/por-derecho/en/updates/david-espejo-expert-evidence/\"/>
    <updated>2026-08-25T18:30:00Z</updated>
    <summary>Four signed reports, two identified annexes and a pre-hearing version issue, with express evidential limits.</summary>
  </entry>"""
    update_feed(ROOT / "es/actualizaciones/feed.xml", "david-espejo-evidencia-pericial", es_entry)
    update_feed(ROOT / "en/updates/feed.xml", "david-espejo-expert-evidence", en_entry)
    update_sitemap(ROOT / "sitemap-david-espejo.xml")

    # Remove one-off machinery from the resulting branch commit.
    (ROOT / "scripts/apply_david_espejo_discovery_patch_once.py").unlink(missing_ok=True)
    (ROOT / ".github/workflows/david-espejo-one-off-discovery-patch.yml").unlink(missing_ok=True)


if __name__ == "__main__":
    main()

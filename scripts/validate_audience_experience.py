#!/usr/bin/env python3
"""Release gate for the 23 August 2026 audience-experience update."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIRS = (ROOT / "es", ROOT / "en", ROOT / "assets")
HTML_ROOTS = (ROOT / "es", ROOT / "en")
FORBIDDEN_PUBLIC_IDENTITIES = (b"Laura Isabel",)
SOURCE_LITERAL_MARKERS = (
    b"data-source-literal",
    b'"contemporaneous_email_source_literal"',
    b"source literal",
    b"literal de fuente",
    b"literal de la fuente",
)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.links.append(href)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def internal_target(source: Path, href: str) -> Path | None:
    value = href.strip()
    if not value or value.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None
    route = unquote(parsed.path)
    if not route:
        return None
    if route.startswith("/por-derecho/"):
        target = ROOT / route.removeprefix("/por-derecho/")
    elif route.startswith("/"):
        target = ROOT / route.removeprefix("/")
    else:
        target = source.parent / route
    target = target.resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        return target
    if route.endswith("/") or target.is_dir():
        target /= "index.html"
    return target


def validate_links(errors: list[str]) -> tuple[int, int]:
    pages = sorted(path for base in HTML_ROOTS for path in base.rglob("*.html"))
    checked = 0
    for page in pages:
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for href in parser.links:
            target = internal_target(page, href)
            if target is None:
                continue
            checked += 1
            if not target.exists():
                fail(errors, f"broken internal link: {page.relative_to(ROOT)}: {href} -> {target}")
    return len(pages), checked


def validate_identity(errors: list[str]) -> int:
    checked = 0
    for base in PUBLIC_DIRS:
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            checked += 1
            try:
                data = path.read_bytes()
            except OSError as exc:
                fail(errors, f"cannot read public file {path.relative_to(ROOT)}: {exc}")
                continue
            for forbidden in FORBIDDEN_PUBLIC_IDENTITIES:
                if forbidden in data:
                    fail(errors, f"forbidden public identity variant {forbidden!r}: {path.relative_to(ROOT)}")
            if b"Laura Matos" in data and not any(marker in data for marker in SOURCE_LITERAL_MARKERS):
                fail(errors, f"unmarked source-literal name used as narrative identity: {path.relative_to(ROOT)}")
    return checked


def validate_home(errors: list[str], lang: str) -> None:
    page = ROOT / lang / "index.html"
    text = page.read_text(encoding="utf-8")
    if lang == "es":
        ordered_ids = ("inicio", "resumen-60-segundos", "psr-reader-intent", "perimetros-del-caso", "historia-reconstruida")
        required_routes = (
            "reconstruccion-unitaria-autoridades-publicas/",
            "medios-trazabilidad-relato-publico/",
            "objetivos-recuperacion-restitucion/",
            "colaborar/",
            "mapa-forense-sun-park-262-fincas/",
            "comunidad-instrumentalizacion/",
            "matkator-nucleo-extraconcursal/",
            "control-acreedor-cam-administracion-hecho-omision-judicial/",
        )
    else:
        ordered_ids = ("home", "sixty-second-summary", "psr-reader-intent", "case-perimeters", "reverse-engineered-story")
        required_routes = (
            "public-authority-unitary-case-reconstruction/",
            "media-public-narrative-traceability/",
            "recovery-restitution-objectives/",
            "collaborate/",
            "sun-park-forensic-map-262-properties/",
            "community-instrumentalisation/",
            "matkator-extraconcursal-core/",
            "cam-creditor-control-shadow-administration-judicial-omission/",
        )

    positions = [text.find(f'id="{item}"') for item in ordered_ids]
    if any(position < 0 for position in positions):
        fail(errors, f"{lang}/index.html: missing audience-order id; got {positions}")
    elif positions != sorted(positions):
        fail(errors, f"{lang}/index.html: source audience order is incorrect: {positions}")

    ids = re.findall(r'\bid="([^"]+)"', text)
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        fail(errors, f"{lang}/index.html: duplicate ids: {', '.join(duplicates)}")

    for route in required_routes:
        if f'href="{route}"' not in text:
            fail(errors, f"{lang}/index.html: missing audience route {route}")
    if text.count('class="psr-intent-card"') != 4:
        fail(errors, f"{lang}/index.html: expected exactly four role gateways")
    for marker in (
        'rel="canonical"',
        'hreflang="es"',
        'hreflang="en"',
        'hreflang="x-default"',
        'name="twitter:card"',
        'data-optimum-reader-journey="20260823"',
    ):
        if marker not in text:
            fail(errors, f"{lang}/index.html: missing metadata/stylesheet marker {marker}")


def validate_runtime_contract(errors: list[str]) -> None:
    module = (ROOT / "assets/audience-experience-order-20260823.js").read_text(encoding="utf-8")
    loader = (ROOT / "assets/site.js").read_text(encoding="utf-8")
    prosecution = (ROOT / "assets/prosecution-public-entry-20260821.js").read_text(encoding="utf-8")
    cam_module = (ROOT / "assets/cam-direct-instruction-shadow-admin-judicial-omission-20260823.js").read_text(encoding="utf-8")
    renderer = (ROOT / "scripts/render_audience_experience.mjs").read_text(encoding="utf-8")

    for marker in (
        "MutationObserver",
        "deduplicate('.ac-dfa-update-section')",
        "deduplicate('.prosecution-entry-20260821')",
        "sixty-second-summary",
        "resumen-60-segundos",
        "psr-reader-intent",
        "case-perimeters",
        "perimetros-del-caso",
        "data-audience-full-record",
        "openHashTarget",
        "const prosecution = main.querySelector",
        "[hero, controlling, criminalMisuse, priority, prosecution, summary, audiences, perimeters]",
        "main.dataset.expressCriminalAttributionVisible",
        "main.dataset.fiveActorControllingAllegationVisible",
        "audienceProtectedAttribution",
    ):
        if marker not in module:
            fail(errors, f"audience runtime missing contract marker: {marker}")
    if "audience-experience-order-20260823.js?v=20260824a" not in loader:
        fail(errors, "site.js does not load the audience-order release module")

    for marker in (
        "section.dataset.expressCriminalAttribution = '20260824'",
        "Gil Marer and Aweswell directly allege an organised criminal course",
        "Gil Marer y Aweswell alegan directamente un curso delictivo organizado",
        "not merely a set of questions",
        "no una mera serie de preguntas",
        "Relationship is not responsibility; missing proof does not erase the allegation.",
        "Relación no es responsabilidad; la prueba pendiente no borra la acusación.",
        "provisional dismissal",
        "archivo provisional",
    ):
        if marker not in prosecution:
            fail(errors, f"homepage prosecution module missing non-dilution marker: {marker}")

    for marker in (
        "five identified private actors operated",
        "cinco actores privados identificados operaron",
        "Affirmative criminal enablement plus omission",
        "Habilitación penal afirmativa más omisión",
        "Judge Alberto López Villarrubia",
        "Magistrado-Juez Alberto López Villarrubia",
        "data-source-literal",
        "source literal",
        "literal de fuente",
        "Direct allegation ≠ adjudicated finding",
        "Acusación directa ≠ declaración judicial",
    ):
        if marker not in cam_module:
            fail(errors, f"cross-site CAM module missing attribution/source-fidelity marker: {marker}")

    for marker in (
        "attributionVisibleBeforeCollapse",
        "controllingVisibleBeforeCollapse",
        "controllingFiveActorTextPresent",
        "controllingInstitutionalTextPresent",
        "directAttributionTextPresent",
        "protectedAttributionMarker",
        "contraryRecordPresent",
        "direct attribution is hidden in collapsed full record",
    ):
        if marker not in renderer:
            fail(errors, f"audience renderer missing non-dilution check: {marker}")


def main() -> int:
    errors: list[str] = []
    pages, links = validate_links(errors)
    public_files = validate_identity(errors)
    validate_home(errors, "es")
    validate_home(errors, "en")
    validate_runtime_contract(errors)

    if errors:
        print("AUDIENCE EXPERIENCE VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "AUDIENCE EXPERIENCE VALIDATION PASSED — "
        f"{pages} HTML pages, {links} internal links, {public_files} public files; "
        "bilingual role gateways, perimeter controls, marked source literals, visible direct criminal attribution and runtime order verified."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

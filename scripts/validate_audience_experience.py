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

    for marker in (
        'data-pd-five-ac="20260824b"',
        'data-five-actor-accountability-static="true"',
        'data-five-actor-front-page-lock="express-authorization-required"',
        'data-key-direct-route-presentation="front-page"',
        'data-pd-five-ac-css="20260824b"',
        '../assets/actors/francisco-mario-matos-matas.jpg',
        '../assets/actors/francisco-de-borja-rodriguez-batllori.jpg',
        '../assets/actors/alberto-lopez-villarrubia.jpg',
        'Francisco Mario Matos Matas',
        'Antonio Cogolludo Rojas',
        'Shaila María Cogolludo Ramos',
        'José Daniel Acosta Matos',
        'Laura Patricia Acosta Matos',
    ):
        if marker not in text:
            fail(errors, f"{lang}/index.html: missing static five-actor accountability marker {marker}")
    for marker, expected in (
        ('data-private-actor-card=', 5),
        ('data-institution-card=', 2),
        ('data-linkage-row', 5),
    ):
        count = text.count(marker)
        if count != expected:
            fail(errors, f"{lang}/index.html: expected {expected} {marker} markers, got {count}")


def validate_key_direct_routes(errors: list[str]) -> None:
    routes = (
        "es/administracion-de-hecho-comunidad-ac/index.html",
        "en/de-facto-administration-community-ac/index.html",
        "es/pwc-canarias-carlos-saavedra-sun-park/index.html",
        "en/pwc-canarias-carlos-saavedra-sun-park/index.html",
        "es/ric-private-equity-sun-park/index.html",
        "en/ric-private-equity-sun-park/index.html",
        "es/concurso-36-2012-administrador-concursal/index.html",
        "en/insolvency-36-2012-insolvency-administrator/index.html",
        "es/concurso-36-2012-juzgado-mercantil-1/index.html",
        "en/insolvency-36-2012-mercantile-court-1/index.html",
        "es/toma-control-sun-park-7-junio-2018/index.html",
        "en/sun-park-takeover-7-june-2018/index.html",
        "es/concurso-36-2012-responsabilidad-institucional/index.html",
        "en/insolvency-36-2012-institutional-accountability/index.html",
    )
    for relative in routes:
        page = ROOT / relative
        if not page.exists():
            fail(errors, f"missing locked five-actor direct route: {relative}")
            continue
        text = page.read_text(encoding="utf-8")
        if "site.js?v=20260824c" not in text:
            fail(errors, f"{relative}: missing cache-busted five-actor direct-route loader")


def validate_runtime_contract(errors: list[str]) -> None:
    module = (ROOT / "assets/audience-experience-order-20260823.js").read_text(encoding="utf-8")
    loader = (ROOT / "assets/site.js").read_text(encoding="utf-8")
    prosecution = (ROOT / "assets/prosecution-public-entry-20260821.js").read_text(encoding="utf-8")
    cam_module = (ROOT / "assets/cam-direct-instruction-shadow-admin-judicial-omission-20260823.js").read_text(encoding="utf-8")
    five_actor_module = (ROOT / "assets/homepage-actor-family-pwc-note-20260819.js").read_text(encoding="utf-8")
    five_actor_css = (ROOT / "assets/five-actor-accountability-20260824.css").read_text(encoding="utf-8")
    preservation = (ROOT / "archive/FIVE_ACTOR_FRONT_PAGE_AND_DIRECT_ROUTE_PRESERVATION_LOCK_24AUG2026.md").read_text(encoding="utf-8")
    ricpe_loader = (ROOT / "assets/ricpe-identity-correction-20260815.js").read_text(encoding="utf-8")
    site_base = (ROOT / "assets/site-base-20260819.js").read_text(encoding="utf-8")
    pre_intervencion = (ROOT / "assets/site-pre-intervencion-highlight-before-eg95-20260823.js").read_text(encoding="utf-8")
    site_wrapper = (ROOT / "assets/site-pre-intervencion-highlight-20260820.js").read_text(encoding="utf-8")
    renderer = (ROOT / "scripts/render_audience_experience.mjs").read_text(encoding="utf-8")

    for marker in (
        "MutationObserver",
        "deduplicate('.ac-dfa-update-section')",
        "deduplicate('section[data-pd-five-ac]')",
        "deduplicate('.prosecution-entry-20260821')",
        "sixty-second-summary",
        "resumen-60-segundos",
        "psr-reader-intent",
        "case-perimeters",
        "perimetros-del-caso",
        "data-audience-full-record",
        "openHashTarget",
        "const detailed = main.querySelector('section[data-pd-five-ac]')",
        "const prosecution = main.querySelector",
        "[hero, controlling, detailed, criminalMisuse, priority, prosecution, summary, audiences, perimeters]",
        "main.dataset.expressCriminalAttributionVisible",
        "main.dataset.fiveActorControllingAllegationVisible",
        "main.dataset.fiveActorVisualVisible",
        "audienceProtectedAttribution",
        "audienceProtectedFiveActorVisual",
        "pd:five-actor-visual-ready",
    ):
        if marker not in module:
            fail(errors, f"audience runtime missing contract marker: {marker}")
    if "audience-experience-order-20260823.js?v=20260824b" not in loader:
        fail(errors, "site.js does not load the audience-order release module")
    for marker, source, label in (
        ("homepage-actor-family-pwc-note-20260819.js?v=20260824c", ricpe_loader, "five-actor component"),
        ("ricpe-identity-correction-20260815.js?v=20260824c", site_base, "RICPE identity loader"),
        ("site-base-20260819.js?v=20260824c", pre_intervencion, "site base loader"),
        ("site-pre-intervencion-highlight-before-eg95-20260823.js?v=20260824c", site_wrapper, "pre-intervencion loader"),
        ("site-pre-intervencion-highlight-20260820.js?v=20260824c", loader, "site wrapper loader"),
    ):
        if marker not in source:
            fail(errors, f"cache-busted direct-route loader chain missing {label}: {marker}")

    for marker in (
        "section.dataset.pdFiveAc = '20260824b'",
        "section.dataset.fiveActorFrontPageLock = 'express-authorization-required'",
        "section.dataset.keyDirectRoutePresentation = isHome ? 'front-page' : contextKey",
        "isCanonical",
        "isCourt",
        "data-private-actor-card",
        "data-institution-card",
        "data-linkage-row",
        "pd:five-actor-visual-ready",
        "francisco-de-borja-rodriguez-batllori.jpg",
        "alberto-lopez-villarrubia.jpg",
        "NO ROW DECLARES GUILT",
        "NINGUNA FILA DECLARA CULPABILIDAD",
    ):
        if marker not in five_actor_module:
            fail(errors, f"five-actor module missing static/runtime accountability marker: {marker}")
    for marker in (
        ".pd-five-ac__cards",
        ".pd-five-ac__institutional-grid",
        ".pd-five-ac__institution-portrait",
        ".pd-five-ac__linkage-row",
        "@media (max-width: 780px)",
    ):
        if marker not in five_actor_css:
            fail(errors, f"five-actor stylesheet missing responsive marker: {marker}")
    for marker in (
        "express-authorization-required",
        "court-appointed and judicial-adjacent",
        "Magistrate-Judge exercises judicial power",
        "Key direct routes",
        "may not be removed, hidden behind a closed disclosure",
    ):
        if marker not in preservation:
            fail(errors, f"five-actor preservation lock missing instruction marker: {marker}")

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
        "fiveActorVisualVisibleBeforeCollapse",
        "fiveActorFrontPageLock",
        "keyDirectRoutePresentation",
        "fiveActorCards",
        "institutionCards",
        "linkageRows",
        "institutionPortraitsLoaded",
    ):
        if marker not in renderer:
            fail(errors, f"audience renderer missing non-dilution check: {marker}")


def main() -> int:
    errors: list[str] = []
    pages, links = validate_links(errors)
    public_files = validate_identity(errors)
    validate_home(errors, "es")
    validate_home(errors, "en")
    validate_key_direct_routes(errors)
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

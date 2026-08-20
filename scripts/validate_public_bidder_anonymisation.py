#!/usr/bin/env python3
"""Enforce name-only bidder anonymisation on public surfaces and preserve the bid.

The protected bidder name is represented only by its SHA-256 digest. The validator
has two independent public-publication gates:

1. the protected name must be absent from public website source, public filenames
   and any explicitly supplied public URLs; and
2. the bilingual adjudication and corrections pages must retain the material bid,
   comparison, procedural, deed, Registry and accounts markers.

Private/archive, research, prompt and evidence-custody files are deliberately outside
this public-source gate. They may retain the original legal name and native source
references for evidential retrieval. This is a current-public-tree/public-URL control;
it is not a Git-history clearance tool and it never deletes underlying evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
PUBLIC_ROOTS = [ROOT / "es", ROOT / "en", ROOT / "assets"]
TEXT_SUFFIXES = {
    ".css",
    ".csv",
    ".htm",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".rst",
    ".svg",
    ".toml",
    ".tsv",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
ROOT_PUBLIC_EXACT = {
    "index.html",
    "404.html",
    "robots.txt",
    "sitemap.xml",
    "rss.xml",
}
ROOT_PUBLIC_GLOBS = (
    "sitemap*.xml",
    "rss*.xml",
    "feed*.xml",
    "manifest*.json",
)

# SHA-256 of the protected lower-case name token. Never replace with plaintext.
PROTECTED_TOKEN_HASHES = {
    "33c594e4e36529842cb1344043ec59e9f4d026466fd7ba0112a635fbe30baf3e"
}

WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9_-]+", re.UNICODE)

# Build superseded formulations from fragments so the source does not contain
# the prohibited wording as a single literal.
FORBIDDEN_BROAD_WORDING = (
    "La identidad del tercero se mantiene " + "anonimizada en la publicación.",
    "La web mantiene deliberadamente anonimizada la " + "identidad del tercer oferente.",
    "Su identidad se mantiene " + "anonimizada públicamente",
    "su identidad se mantiene " + "anonimizada en la publicación.",
    "The bidder's identity is deliberately " + "anonymised in the public record.",
    "The website deliberately anonymises the third-party bidder's " + "identity.",
    "The bidder remains publicly " + "anonymised",
    "the bidder identity is " + "anonymised in the public record.",
    "protected bidder " + "identity is absent",
    "Anonymise the " + "bidder; preserve the competitive fact.",
)

LOCAL_REQUIRED_MARKERS: dict[str, tuple[str, ...]] = {
    "es/adjudicacion-2022-reconstruccion-documental/index.html": (
        "08/02/2021",
        "14,8 M€",
        "perímetro de fincas identificado",
        "14.713.880,31 €",
        "tercer oferente",
        "presentación procesal",
        "capacidad/fondos",
        "tratamiento en la licitación",
        "escritura n.º 457",
        "13.168.082,02 €",
        "400.000 €",
        "cinco días naturales",
        "Registro",
        "cuentas",
        "Únicamente el nombre del tercer oferente se mantiene anonimizado",
        "La web anonimiza únicamente el nombre del tercer oferente",
    ),
    "en/2022-adjudication-documentary-reconstruction/index.html": (
        "8 February 2021",
        "EUR 14.8m",
        "identified property perimeter",
        "EUR 14,713,880.31",
        "third-party bidder",
        "Procedural filing",
        "authority/funds",
        "treatment at the licitation",
        "deed no. 457",
        "EUR 13,168,082.02",
        "EUR 400,000",
        "five calendar days",
        "Registry",
        "accounts",
        "Only the bidder's name is anonymised",
        "The website anonymises only the third-party bidder's name",
    ),
    "es/correcciones-control-versiones/index.html": (
        "Existe una propuesta documentada de un tercer oferente por 14,8 M€.",
        "Únicamente su nombre se mantiene anonimizado públicamente",
        "presentación, capacidad/fondos y tratamiento en la licitación",
    ),
    "en/corrections-version-control/index.html": (
        "A documented EUR 14.8m proposal by a third-party bidder exists.",
        "Only the bidder's name remains publicly anonymised",
        "filing, authority/funds and licitation treatment remain open",
    ),
    "assets/adjudicacion-provenance-cross-site-20260819.js": (
        "14,8 M€",
        "EUR 14.8m",
        "13.168.082,02 €",
        "EUR 13,168,082.02",
        "únicamente su nombre se mantiene anonimizado en la publicación",
        "only the bidder's name is anonymised in the public record",
    ),
}

URL_REQUIRED_MARKERS: dict[str, tuple[str, ...]] = {
    "/es/adjudicacion-2022-reconstruccion-documental/": LOCAL_REQUIRED_MARKERS[
        "es/adjudicacion-2022-reconstruccion-documental/index.html"
    ],
    "/en/2022-adjudication-documentary-reconstruction/": LOCAL_REQUIRED_MARKERS[
        "en/2022-adjudication-documentary-reconstruction/index.html"
    ],
    "/es/correcciones-control-versiones/": LOCAL_REQUIRED_MARKERS[
        "es/correcciones-control-versiones/index.html"
    ],
    "/en/corrections-version-control/": LOCAL_REQUIRED_MARKERS[
        "en/corrections-version-control/index.html"
    ],
    "/assets/adjudicacion-provenance-cross-site-20260819.js": LOCAL_REQUIRED_MARKERS[
        "assets/adjudicacion-provenance-cross-site-20260819.js"
    ],
}


def digest(token: str) -> str:
    return hashlib.sha256(token.casefold().encode("utf-8")).hexdigest()


def contains_protected_token(text: str) -> bool:
    return any(digest(token) in PROTECTED_TOKEN_HASHES for token in WORD_RE.findall(text))


def public_text_files():
    """Yield only files that are actually published by the static website."""
    yielded: set[pathlib.Path] = set()

    for base in PUBLIC_ROOTS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                resolved = path.resolve()
                if resolved not in yielded:
                    yielded.add(resolved)
                    yield path

    for name in ROOT_PUBLIC_EXACT:
        path = ROOT / name
        if path.is_file():
            resolved = path.resolve()
            if resolved not in yielded:
                yielded.add(resolved)
                yield path

    for pattern in ROOT_PUBLIC_GLOBS:
        for path in ROOT.glob(pattern):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                resolved = path.resolve()
                if resolved not in yielded:
                    yielded.add(resolved)
                    yield path


def fetch_url(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Por-Derecho-public-bidder-name-only-control/3.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}")
        return response.read().decode("utf-8", "replace")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        action="append",
        default=[],
        help=(
            "Public URL to scan. Repeat for multiple URLs. When supplied, local "
            "public-source scanning is skipped unless --also-local is used."
        ),
    )
    parser.add_argument(
        "--also-local",
        action="store_true",
        help="Scan current public website source in addition to any --url values.",
    )
    return parser.parse_args()


def check_text(
    *,
    label: str,
    text: str,
    required_markers: tuple[str, ...] = (),
    failures: list[str],
) -> None:
    if contains_protected_token(text):
        failures.append(f"Protected third-party bidder name found on public surface: {label}")

    for wording in FORBIDDEN_BROAD_WORDING:
        if wording in text:
            failures.append(
                f"Superseded broad bidder-anonymisation wording found in {label}: {wording!r}"
            )

    for marker in required_markers:
        if marker not in text:
            failures.append(f"Required bid-preservation marker missing from {label}: {marker!r}")


def scan_local(failures: list[str]) -> int:
    scanned = 0
    seen_required: set[str] = set()

    for path in public_text_files():
        scanned += 1
        rel = path.relative_to(ROOT).as_posix()

        if contains_protected_token(rel):
            failures.append(f"Protected third-party bidder name found in public path: {rel}")

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            failures.append(f"READ ERROR {rel}: {exc}")
            continue

        required = LOCAL_REQUIRED_MARKERS.get(rel, ())
        if required:
            seen_required.add(rel)
        check_text(label=rel, text=text, required_markers=required, failures=failures)

    for rel in LOCAL_REQUIRED_MARKERS:
        if rel not in seen_required:
            failures.append(f"Required bid-control public file missing from current tree: {rel}")

    return scanned


def required_markers_for_url(url: str) -> tuple[str, ...]:
    for route, markers in URL_REQUIRED_MARKERS.items():
        if route in url:
            return markers
    return ()


def scan_urls(urls: list[str], failures: list[str]) -> int:
    scanned = 0
    for url in urls:
        scanned += 1
        try:
            text = fetch_url(url)
        except Exception as exc:  # noqa: BLE001 - report every verification failure
            failures.append(f"URL READ ERROR {url}: {exc}")
            continue
        check_text(
            label=url,
            text=text,
            required_markers=required_markers_for_url(url),
            failures=failures,
        )
    return scanned


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    scanned_local = 0
    scanned_urls = 0

    if not args.url or args.also_local:
        scanned_local = scan_local(failures)
    if args.url:
        scanned_urls = scan_urls(args.url, failures)

    if failures:
        print("PUBLIC BIDDER NAME-ONLY AND BID-PRESERVATION GATE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    scope = []
    if scanned_local:
        scope.append(f"{scanned_local} public-source files")
    if scanned_urls:
        scope.append(f"{scanned_urls} public URLs")
    print(
        "PUBLIC BIDDER NAME-ONLY AND BID-PRESERVATION GATE: "
        f"PASS ({', '.join(scope)})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

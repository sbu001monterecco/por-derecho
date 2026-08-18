#!/usr/bin/env python3
"""Validate the open-file supervisory-practice routes using only stdlib."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]

HTML_FILES = [
    "es/cnmv-ricpe-verificacion/index.html",
    "en/cnmv-ricpe-verification/index.html",
    "es/incentivos-regionales-gc836-p06/index.html",
    "en/regional-incentives-gc836-p06/index.html",
    "es/snca-fondos-europeos-trazabilidad/index.html",
    "en/snca-eu-funds-traceability/index.html",
]

JS_FILES = [
    "assets/practitioner-open-kimono-20260818.js",
    "assets/supervisory-practice-entrypoints-20260818.js",
    "assets/same-asset-multiple-financial-lives-20260816.js",
    "assets/public-authority-case-reconstruction-20260817.js",
    "assets/ricpe-filed-status-20260817.js",
]

ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def load(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        fail(f"missing file: {rel}")
        return ""
    return path.read_text(encoding="utf-8")


def check_html(rel: str, text: str) -> None:
    lower = text.lower()
    for marker in ("<!doctype html", "<html", "</html>", "<head", "</head>", "<body", "</body>", "<main", "</main>"):
        if marker not in lower:
            fail(f"{rel}: missing {marker}")
    if '<link rel="canonical"' not in lower:
        fail(f"{rel}: missing canonical link")
    if 'hreflang="es"' not in lower or 'hreflang="en"' not in lower:
        fail(f"{rel}: incomplete ES/EN hreflang")
    if "open kimono" not in lower:
        fail(f"{rel}: missing open-kimono practice section")
    if "private follow-up code" in lower and re.search(r"private follow-up code\s*[:=]\s*[a-z0-9-]{6,}", lower):
        fail(f"{rel}: appears to expose a follow-up code")
    if "código privado" in lower and re.search(r"código privado[^<]{0,20}[:=]\s*[a-z0-9-]{6,}", lower):
        fail(f"{rel}: appears to expose a private code")


def resolve_internal_links(rel: str, text: str) -> None:
    source = ROOT / rel
    for href in re.findall(r'href=["\']([^"\']+)', text, flags=re.IGNORECASE):
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc:
            continue
        path_part = parsed.path
        if path_part.startswith("/por-derecho/"):
            target = ROOT / path_part.removeprefix("/por-derecho/")
        elif path_part.startswith("/"):
            continue
        else:
            target = (source.parent / path_part).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"{rel}: internal link escapes repository: {href}")
            continue
        if path_part.endswith("/") or target.is_dir():
            target = target / "index.html"
        if not target.exists():
            fail(f"{rel}: broken internal link {href} -> {target.relative_to(ROOT)}")


def check_number_control(rel: str, text: str) -> None:
    if "cnmv" in rel or "incentiv" in rel or "snca" in rel:
        if rel.startswith("es/"):
            required = ("€6.570.713,56", "€6.573.703,10", "€2.989,54")
        else:
            required = ("€6,570,713.56", "€6,573,703.10", "€2,989.54")
        for number in required:
            if number not in text:
                fail(f"{rel}: missing controlled financing number {number}")


def check_knowledge_wording(rel: str, text: str) -> None:
    banned = ("Qué sabía RICPE", "qué sabía RICPE", "What RICPE knew", "what RICPE knew")
    for phrase in banned:
        if phrase in text:
            fail(f"{rel}: undifferentiated corporate-knowledge wording remains: {phrase}")


def main() -> int:
    for rel in HTML_FILES:
        text = load(rel)
        if not text:
            continue
        check_html(rel, text)
        resolve_internal_links(rel, text)
        check_number_control(rel, text)
        check_knowledge_wording(rel, text)

    for rel in JS_FILES:
        text = load(rel)
        if not text:
            continue
        if not text.lstrip().startswith("(() =>") or not text.rstrip().endswith("})();"):
            fail(f"{rel}: unexpected IIFE boundary")

    generic = load("assets/same-asset-multiple-financial-lives-20260816.js")
    authority = load("assets/public-authority-case-reconstruction-20260817.js")
    for route in ("cnmv-ricpe-verificacion", "cnmv-ricpe-verification", "incentivos-regionales-gc836-p06", "regional-incentives-gc836-p06", "snca-fondos-europeos-trazabilidad", "snca-eu-funds-traceability"):
        if route not in generic:
            fail(f"generic funding module lacks dedicated-route guard: {route}")
        if route not in authority:
            fail(f"public-authority module lacks dedicated-route guard: {route}")

    try:
        ET.parse(ROOT / "sitemap-supervisory-practice.xml")
    except Exception as exc:  # noqa: BLE001
        fail(f"invalid sitemap-supervisory-practice.xml: {exc}")

    robots = load("robots.txt")
    if "sitemap-supervisory-practice.xml" not in robots:
        fail("robots.txt does not expose supervisory-practice sitemap")

    if ERRORS:
        print("SUPERVISORY PRACTICE VALIDATION FAILED", file=sys.stderr)
        for item in ERRORS:
            print(f"- {item}", file=sys.stderr)
        return 1

    print("SUPERVISORY PRACTICE VALIDATION PASSED")
    print(f"HTML routes checked: {len(HTML_FILES)}")
    print(f"JavaScript files checked: {len(JS_FILES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

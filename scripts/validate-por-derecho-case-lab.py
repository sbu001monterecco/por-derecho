#!/usr/bin/env python3
"""Validate the bilingual, synthetic-only Por Derecho Case Laboratory."""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    ROOT / "es/por-derecho/laboratorio-de-casos/index.html",
    ROOT / "es/por-derecho/laboratorio-de-casos/caso-prisma/index.html",
    ROOT / "en/por-derecho/case-lab/index.html",
    ROOT / "en/por-derecho/case-lab/case-prism/index.html",
]
REQUIRED_FILES = PAGES + [
    ROOT / "assets/por-derecho/case-lab.css",
    ROOT / "assets/por-derecho/case-lab.js",
    ROOT / "sitemap-por-derecho-case-lab.xml",
]
PROHIBITED_REAL_MATTER_TERMS = [
    "acosta matos", "mynd yaiza", "luchy playa blanca", "matkator",
    "concurso 36/2012", "ric private equity", "carlos saavedra",
]

class IdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.links: list[str] = []
        self.lang: str | None = None
        self.title_seen = False
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "html": self.lang = data.get("lang")
        if data.get("id"): self.ids.append(data["id"] or "")
        if tag == "a" and data.get("href"): self.links.append(data["href"] or "")
        if tag == "title": self.title_seen = True

errors: list[str] = []
for path in REQUIRED_FILES:
    if not path.exists(): errors.append(f"missing file: {path.relative_to(ROOT)}")

for page in PAGES:
    if not page.exists(): continue
    text = page.read_text(encoding="utf-8")
    parser = IdParser(); parser.feed(text)
    duplicates = sorted({value for value in parser.ids if parser.ids.count(value) > 1})
    if duplicates: errors.append(f"duplicate ids in {page.relative_to(ROOT)}: {duplicates}")
    expected_lang = "es" if "/es/" in page.as_posix() else "en"
    if parser.lang != expected_lang: errors.append(f"wrong lang in {page.relative_to(ROOT)}")
    if not parser.title_seen: errors.append(f"missing title in {page.relative_to(ROOT)}")
    lower = text.lower()
    for term in PROHIBITED_REAL_MATTER_TERMS:
        if term in lower: errors.append(f"real-matter term '{term}' in {page.relative_to(ROOT)}")
    if "synt" not in lower and "fict" not in lower:
        errors.append(f"synthetic/fictitious boundary absent in {page.relative_to(ROOT)}")

spanish_case = PAGES[1].read_text(encoding="utf-8") if PAGES[1].exists() else ""
english_case = PAGES[3].read_text(encoding="utf-8") if PAGES[3].exists() else ""
for needle in ["data-perimeter-map", "data-time-button", "data-role-button", "data-lab-decision", "data-outcome-button", "data-report-log"]:
    if needle not in spanish_case: errors.append(f"Spanish case missing interaction: {needle}")
    if needle not in english_case: errors.append(f"English case missing interaction: {needle}")
if spanish_case.count('data-doc ') != 12: errors.append("Spanish case must contain exactly 12 synthetic documents")
if english_case.count('data-doc ') != 12: errors.append("English case must contain exactly 12 synthetic documents")
if spanish_case.count('data-role-panel=') != 4: errors.append("Spanish case must contain four role panels")
if english_case.count('data-role-panel=') != 4: errors.append("English case must contain four role panels")
if spanish_case.count('data-outcome-panel=') != 3: errors.append("Spanish case must contain three outcome panels")
if english_case.count('data-outcome-panel=') != 3: errors.append("English case must contain three outcome panels")

try:
    ET.parse(ROOT / "sitemap-por-derecho-case-lab.xml")
except Exception as exc: errors.append(f"invalid case-lab sitemap: {exc}")

css = (ROOT / "assets/por-derecho/case-lab.css").read_text(encoding="utf-8") if (ROOT / "assets/por-derecho/case-lab.css").exists() else ""
if css.count("{") != css.count("}"): errors.append("unbalanced CSS braces")
js = (ROOT / "assets/por-derecho/case-lab.js").read_text(encoding="utf-8") if (ROOT / "assets/por-derecho/case-lab.js").exists() else ""
for token in ["data-perimeter-map", "data-report-log", "setTime('t0'", "window.print"]:
    if token not in js: errors.append(f"case-lab JS missing token: {token}")

if errors:
    print("Case Laboratory validation failed:")
    for error in errors: print(f"- {error}")
    sys.exit(1)
print("Case Laboratory validation passed: 4 pages, 12 documents per flagship case, 4 roles, 3 outcomes, synthetic-only boundary intact.")

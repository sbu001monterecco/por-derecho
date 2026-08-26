#!/usr/bin/env python3
"""Validate the DI 273/2013 bilingual evidence publication."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
ES = ROOT / "es/fiscalia-di273-2013-querella-gil-patricia/index.html"
EN = ROOT / "en/prosecution-di273-2013-complaint-gil-patricia/index.html"
PDF = ROOT / "evidence/fiscalia/di-273-2013/public-pdfs/querella-fiscalia-di273-2013-27dic2013-public-redacted.pdf"
README = ROOT / "evidence/fiscalia/di-273-2013/README.md"
CONTROL = ROOT / "archive/FISCALIA_DI273_2013_CAUSAL_ATTRIBUTION_AND_ARCHIVE_RECOVERY_CONTROL_26AUG2026.md"
AUDIT = ROOT / "docs/deletion-audits/2026-08-26-fiscalia-di273-2013-causal-attribution.md"
JUSTICE = ROOT / "assets/data/justice-map.json"
REGISTER = ROOT / "evidence/sun-park/labory-catrude/archive-register.csv"
SITEMAPS = (ROOT / "sitemap.xml",)

EXPECTED_PDF_HASH = "5515b4cbedafc7c419f401769926ba1349553eb99abf87df7702354e972462c2"
NATIVE_HASH = "6531e1cd3677ddcfa600345c38fe69e463b0418b1025f27f0ee231a0817e697e"
FORBIDDEN = (
    "Y2231410X",
    "800291405",
    "45.449.955T",
    "45449955T",
    "ANGjdJ",
    "14860f88a3ee4150",
    "148423b1a61dc6bd",
    "17887636c71891a0",
    "18bfc5edd4d74d3c",
)

failures: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def text(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


for path in (ES, EN, PDF, README, CONTROL, AUDIT, JUSTICE, REGISTER, *SITEMAPS):
    require(path.is_file(), f"missing required publication file: {path.relative_to(ROOT)}")

if PDF.is_file():
    require(hashlib.sha256(PDF.read_bytes()).hexdigest() == EXPECTED_PDF_HASH, "public PDF hash mismatch")
    reader = PdfReader(PDF)
    require(len(reader.pages) == 8, "public querella must preserve all eight scan pages")
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    require(not extracted.strip(), "raster-redacted public PDF unexpectedly contains a text layer")
    require(not reader.is_encrypted, "public PDF must not be encrypted")

es = text(ES)
en = text(EN)
readme = text(README)
control = text(CONTROL)
audit = text(AUDIT)
combined_public = "\n".join((es, en, readme, control, audit))

for forbidden in FORBIDDEN:
    require(forbidden.casefold() not in combined_public.casefold(), f"private/provider literal published: {forbidden}")

for page, markers in {
    ES: (
        "ACTO FISCAL DOCUMENTADO",
        "Hipótesis acusatoria no adjudicada",
        "2013, no 2012",
        "Tomás Fernández de Páiz",
        "La alegación sostenible es inversión causal",
        "Lo que no está probado",
        "Ley 2/2023",
        "Armata",
        EXPECTED_PDF_HASH,
        NATIVE_HASH,
    ),
    EN: (
        "Documented prosecution act",
        "Unadjudicated accusatory hypothesis",
        "2013, not 2012",
        "Tomás Fernández de Páiz",
        "The supportable allegation is causal inversion",
        "What is not proved",
        "Law 2/2023",
        "Armata",
        EXPECTED_PDF_HASH,
        NATIVE_HASH,
    ),
}.items():
    content = text(page)
    for marker in markers:
        require(marker.casefold() in content.casefold(), f"{page.relative_to(ROOT)} missing marker: {marker}")
    require(PDF.name in content, f"{page.relative_to(ROOT)} does not link public PDF")

require("fiscalia-di273-2013-querella-gil-patricia" in en, "English page lacks reciprocal Spanish route")
require("prosecution-di273-2013-complaint-gil-patricia" in es, "Spanish page lacks reciprocal English route")

for marker in (EXPECTED_PDF_HASH, NATIVE_HASH, "page-complete raster derivative", "blank sixth scan page"):
    require(marker.casefold() in readme.casefold(), f"README missing marker: {marker}")

for marker in (
    "Verified institutional chain",
    "Transformation audit",
    "Actor/date/capacity matrix",
    "Evidence preventing overclaim",
    "Reported archived in 2021",
    "Article 36.2",
    "No separate entity, case or actor named **Armata**",
    "dc7fb8c5cf988fef46a6c0130a7c8d505b312a50f561b0f6f5d2e03664a46079",
    "03aa4f5869f1aab416c53e08ac1bf32d46a2caddf12ae237efa608d48f358abb",
):
    require(marker.casefold() in control.casefold(), f"control missing marker: {marker}")

if JUSTICE.is_file():
    data = json.loads(JUSTICE.read_text(encoding="utf-8"))
    require(data["meta"]["updated"] == "2026-08-26", "justice map update date not advanced")
    people = {item["id"]: item for item in data["people"]}
    proceedings = {item["id"]: item for item in data["proceedings"]}
    require("tomas-fernandez-de-paiz" in people, "justice map missing fiscal signatory")
    require("arrival-2011-2012" in proceedings, "justice map lacks transition node")
    require(proceedings.get("di-273-2013", {}).get("public_route_es") == "/es/fiscalia-di273-2013-querella-gil-patricia/", "justice map lacks DI273 public route")

if REGISTER.is_file():
    with REGISTER.open(encoding="utf-8", newline="") as handle:
        rows = {row["archive_id"]: row for row in csv.DictReader(handle)}
    for archive_id in ("GMAIL-ZIP-002", "GMAIL-ZIP-005"):
        row = rows.get(archive_id, {})
        require(row.get("byte_access_status") == "recovered_and_sha256_verified", f"{archive_id} not marked recovered")
        require(row.get("priority") == "completed", f"{archive_id} priority not completed")

for sitemap in SITEMAPS:
    if sitemap.is_file():
        ET.parse(sitemap)
        body = sitemap.read_text(encoding="utf-8")
        require("/es/fiscalia-di273-2013-querella-gil-patricia/" in body, f"Spanish route absent from {sitemap.name}")
        require("/en/prosecution-di273-2013-complaint-gil-patricia/" in body, f"English route absent from {sitemap.name}")

for path in (ROOT / "assets/data/fiscalia-response-correspondence.json",):
    if path.is_file():
        json.loads(path.read_text(encoding="utf-8"))
        require("investigó la hipótesis" not in path.read_text(encoding="utf-8"), "overstated investigation wording remains")

if failures:
    print("FISCALIA DI273 PUBLICATION VALIDATION: FAIL")
    for failure in failures:
        print(f"- {failure}")
    sys.exit(1)

print("FISCALIA DI273 PUBLICATION VALIDATION: PASS")

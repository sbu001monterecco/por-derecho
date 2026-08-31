#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/canary-ric-public-debt-v1.json"
ES = ROOT / "es/deuda-publica-ric-canarias/index.html"
EN = ROOT / "en/canary-ric-public-debt/index.html"
SITEMAP = ROOT / "sitemap-canary-ric-public-debt.xml"
MANIFEST = ROOT / "publication-manifests/canary-ric-public-debt-20260830.json"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


required = [
    DATA,
    ES,
    EN,
    SITEMAP,
    MANIFEST,
    ROOT / "archive/CANARY_PUBLIC_DEBT_RIC_UNITARY_CONTROL_30AUG2026.md",
    ROOT / "CURRENT_REVERSE_ENGINEERED_DIGEST.md",
    ROOT / "docs/deletion-audits/2026-08-30-canary-ric-public-debt.md",
]
for path in required:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")

data = json.loads(DATA.read_text(encoding="utf-8"))
if data.get("control_id") != "PD-CANARY-RIC-PUBLIC-DEBT-20260830-01":
    fail("wrong control ID")
corpus = data.get("reviewed_corpus", {})
items = corpus.get("items", [])
if corpus.get("files") != 8 or corpus.get("pages") != 734 or len(items) != 8:
    fail("source denominator must be 8 files / 734 pages")
if sum(item.get("pages", 0) for item in items) != 734:
    fail("source item pages do not sum to 734")
for item in items:
    if not re.fullmatch(r"[0-9a-f]{64}", item.get("sha256", "")):
        fail(f"invalid source hash: {item.get('title')}")

issues = data.get("issues", [])
if len(issues) != 2 or [item.get("year") for item in issues] != [2024, 2025]:
    fail("expected 2024 and 2025 issue records")
offered = sum(item["amount_offered_eur"] for item in issues)
requested = sum(item["amount_requested_eur"] for item in issues)
aggregate = data.get("aggregate", {})
if offered != 250_000_000 or requested != 1_139_779_000:
    fail("controlled issue totals changed")
if aggregate.get("amount_offered_eur") != offered or aggregate.get("amount_requested_eur") != requested:
    fail("aggregate totals do not reconcile")
if aggregate.get("excess_demand_eur") != requested - offered:
    fail("excess-demand arithmetic does not reconcile")
if abs(aggregate.get("demand_multiple", 0) - requested / offered) > 0.000001:
    fail("aggregate demand multiple does not reconcile")
if issues[1].get("initial_minimum_allocation_eur") != 80_000 or "100,000" not in issues[1].get("open_reconciliation", ""):
    fail("2025 EUR 80,000 / EUR 100,000 reconciliation boundary missing")

es = ES.read_text(encoding="utf-8")
en = EN.read_text(encoding="utf-8")
for token in ["No es conexión cero", "Tampoco es el mismo dinero", "250 M€", "1.139,779 M€", "ES0000093478", "ES0000093494", "6.573.703,10 €", "80.000 € / 100.000 €", "734 páginas"]:
    if token not in es:
        fail(f"Spanish page missing {token!r}")
for token in ["Not zero connection", "Not the same money either", "€250m", "€1,139.779m", "ES0000093478", "ES0000093494", "€6,573,703.10", "€80,000 / €100,000", "734 pages"]:
    if token not in en:
        fail(f"English page missing {token!r}")
for html, canonical, alternate in [
    (es, "https://sbu001monterecco.github.io/por-derecho/es/deuda-publica-ric-canarias/", "https://sbu001monterecco.github.io/por-derecho/en/canary-ric-public-debt/"),
    (en, "https://sbu001monterecco.github.io/por-derecho/en/canary-ric-public-debt/", "https://sbu001monterecco.github.io/por-derecho/es/deuda-publica-ric-canarias/"),
]:
    if f'rel="canonical" href="{canonical}"' not in html or alternate not in html:
        fail("canonical/hreflang parity missing")
    for boc in ["2024/215/3523.html", "2024/231/3816.html", "2025/224/3808.html", "2025/235/4021.html"]:
        if boc not in html:
            fail(f"official source link missing: {boc}")

reciprocal = {
    "es/index.html": "deuda-publica-ric-canarias/",
    "en/index.html": "canary-ric-public-debt/",
    "es/acosta-matos-perimetro/index.html": "../deuda-publica-ric-canarias/",
    "en/acosta-matos-perimeter/index.html": "../canary-ric-public-debt/",
    "es/ric-private-equity-sun-park/index.html": "../deuda-publica-ric-canarias/",
    "en/ric-private-equity-sun-park/index.html": "../canary-ric-public-debt/",
    "es/ricpe-idoneidad-series-f-g/index.html": "../deuda-publica-ric-canarias/",
    "en/ricpe-idoneidad-series-f-g/index.html": "../canary-ric-public-debt/",
    "es/ricpe-hnt-gc836-trazabilidad/index.html": "../deuda-publica-ric-canarias/",
    "en/ricpe-hnt-gc836-traceability/index.html": "../canary-ric-public-debt/",
    "es/mismo-hotel-multiples-vidas-financieras/index.html": "../deuda-publica-ric-canarias/",
    "en/same-hotel-multiple-financial-lives/index.html": "../canary-ric-public-debt/",
    "es/incentivos-regionales-gc836-p06/index.html": "../deuda-publica-ric-canarias/",
    "en/regional-incentives-gc836-p06/index.html": "../canary-ric-public-debt/",
}
for rel, link in reciprocal.items():
    path = ROOT / rel
    if not path.exists() or link not in path.read_text(encoding="utf-8"):
        fail(f"reciprocal route missing from {rel}")

registry = json.loads((ROOT / "assets/data/unitary-route-registry-v1.json").read_text(encoding="utf-8"))
paths = [item.get("path") for item in registry]
for route in ["es/deuda-publica-ric-canarias/", "en/canary-ric-public-debt/"]:
    if paths.count(route) != 1:
        fail(f"route registry count must be one for {route}")

ET.parse(SITEMAP)
sitemap = SITEMAP.read_text(encoding="utf-8")
if sitemap.count("<url>") != 4 or sitemap.count("hreflang=\"x-default\"") != 4:
    fail("sitemap must contain four bilingual analysis/document-room URL records")
if "sitemap-canary-ric-public-debt.xml" not in (ROOT / "robots.txt").read_text(encoding="utf-8"):
    fail("robots.txt does not expose the dedicated sitemap")

digest = (ROOT / "CURRENT_REVERSE_ENGINEERED_DIGEST.md").read_text(encoding="utf-8")
for token in ["2022–2025 public RIC debt", "not zero", "not shown to be the same", "lower coupon"]:
    if token not in digest:
        fail(f"unitary digest missing {token!r}")
for rel, ids in [
    ("archive/MISSING_EVIDENCE_REGISTER.md", ["ME-108", "ME-109", "ME-110"]),
    ("archive/CORRECTION_REGISTER.md", ["CR-139", "CR-140", "CR-141"]),
    ("archive/CONTINUOUS_MAINTENANCE_MATRIX.md", ["Canary public debt apt for RIC"]),
]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    for identifier in ids:
        if identifier not in text:
            fail(f"{identifier} missing from {rel}")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("publication_id") != data.get("control_id"):
    fail("manifest/control ID mismatch")
if manifest.get("source_corpus", {}).get("binary_publication") != "EXCLUDED_PRIVATE_SOURCE_BINARIES":
    fail("private-source binary exclusion missing")

print("Canary RIC public-debt validation passed: 8 files / 734 pages, issue arithmetic, bilingual routes, reciprocal links, discovery, registers and privacy boundaries OK.")

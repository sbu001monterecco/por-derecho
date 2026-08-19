#!/usr/bin/env python3
"""Validate the LPB definitive-texts repository and public-site activation."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read(path: str) -> str:
    target = ROOT / path
    if not target.exists():
        fail(f"missing required file: {path}")
        return ""
    return target.read_text(encoding="utf-8")


def load_json(path: str):
    text = read(path)
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON {path}: {exc}")
        return None


required = [
    "archive/LPB_TEXTOS_DEFINITIVOS_LIQUIDATION_BASELINE_UNITARY_DIGEST_20AUG2026.md",
    "archive/THREAD_DELETION_AUDIT_LPB_TEXTOS_DEFINITIVOS_20AUG2026.md",
    "assets/data/lpb-definitive-texts-v1.json",
    "assets/data/lpb-definitive-texts-route-v1.json",
    "assets/lpb-definitive-texts-unitary-20260820.js",
    "es/textos-definitivos-lpb-base-liquidacion/index.html",
    "en/lpb-definitive-texts-liquidation-baseline/index.html",
    "operations/LPB_TEXTOS_DEFINITIVOS_LIQUIDATION_BASELINE_ACTIVATION_2026-08-20.md",
    "publication-manifests/lpb-textos-definitivos-liquidation-baseline-2026-08-20.json",
    "sitemap-lpb-definitive-texts.xml",
    "scripts/render_lpb_definitive_texts_unitary.mjs",
    ".github/workflows/validate-lpb-definitive-texts-unitary.yml",
    ".github/workflows/verify-lpb-definitive-texts-live.yml",
]
for item in required:
    read(item)

es = read("es/textos-definitivos-lpb-base-liquidacion/index.html")
en = read("en/lpb-definitive-texts-liquidation-baseline/index.html")
module = read("assets/lpb-definitive-texts-unitary-20260820.js")

page_pairs = [
    ("19.486.498,94", "19,486,498.94"),
    ("10.125.752,00", "10,125,752.00"),
    ("9.052.251,69", "9,052,251.69"),
    ("159", "159"),
    ("29", "29"),
]
for es_marker, en_marker in page_pairs:
    if es_marker not in es:
        fail(f"Spanish page missing marker: {es_marker}")
    if en_marker not in en:
        fail(f"English page missing marker: {en_marker}")

for name, text in [("Spanish page", es), ("English page", en)]:
    if 'data-lpb-definitive-texts-page="20260820"' not in text:
        fail(f"{name} missing stable page marker")
    if re.search(r'href=["\'][^"\']+\.pdf(?:[?#][^"\']*)?["\']', text, re.I):
        fail(f"{name} links directly to a PDF")
    if "44700629Z" in text:
        fail(f"{name} contains a personal identifier")

if "../../en/lpb-definitive-texts-liquidation-baseline/" not in es:
    fail("Spanish page lacks reciprocal English link")
if "../../es/textos-definitivos-lpb-base-liquidacion/" not in en:
    fail("English page lacks reciprocal Spanish link")

for marker in [
    "data-lpb-td-primary-promotion",
    "data-lpb-td-crosslink",
    "data-lpb-td-update",
    "LPB-TD-UNITARY-20260820",
]:
    if marker not in module:
        fail(f"cross-site module missing marker: {marker}")

control = load_json("assets/data/lpb-definitive-texts-v1.json")
if control:
    expected = {
        "active_mass_definitive": 19486498.94,
        "passive_mass_definitive": 10125752.0,
        "special_privilege": 9052251.69,
        "claims_against_estate": 304779.42,
    }
    actual = control.get("definitive_amounts_eur", {})
    for key, value in expected.items():
        if actual.get(key) != value:
            fail(f"control JSON mismatch for {key}: {actual.get(key)!r}")
    sources = {item.get("evidence_id"): item for item in control.get("source_chain", [])}
    hashes = {
        "EVID-LPB-2013-ART75": "a48441aafcddd63ae792f46fc88188b17a32cecba943b8db956587ecd8c8a073",
        "EVID-LPB-2016-TD-FILING": "b62970419a699f07c48777c300f9259721df2072c0f8739aa9aa9d2db9e9aa79",
        "EVID-LPB-2016-TD-CREDITORS": "9004df2fbc361b5f6a4b7042014e025b7643520f68c863c5835f572bdd071c31",
        "EVID-LPB-2018-TD-HOLDER": "22f4149590ef80e050640c9691b7c34dc3a5306f87e2d727bc4f852990980b88",
        "EVID-LPB-2018-LIQ-PLAN": "767b5966bc2d380a35633b3dcb884256e0067cc3e4be3b07e5cf5d2f947b1a78",
    }
    for evidence_id, digest in hashes.items():
        if sources.get(evidence_id, {}).get("sha256") != digest:
            fail(f"source hash mismatch for {evidence_id}")

routes = load_json("assets/data/lpb-definitive-texts-route-v1.json")
if not isinstance(routes, list) or len(routes) != 2:
    fail("route registry must contain exactly two bilingual entries")

manifest = load_json("publication-manifests/lpb-textos-definitivos-liquidation-baseline-2026-08-20.json")
if manifest:
    if manifest.get("publication_id") != "LPB-TEXTOS-DEFINITIVOS-LIQUIDATION-BASELINE-20260820":
        fail("publication manifest ID mismatch")
    if manifest.get("privacy", {}).get("raw_primary_pdfs_committed") is not False:
        fail("manifest must record that raw primary PDFs are not committed")

case_seed = load_json("assets/data/case-reconstruction-v1.json")
if case_seed:
    evidence_ids = {item.get("id") for item in case_seed.get("evidence", [])}
    for required_id in ["EVID-LPB-2013-ART75", "EVID-LPB-2016-TD-FILING", "EVID-LPB-2016-TD-CREDITORS", "EVID-LPB-2018-TD-HOLDER"]:
        if required_id not in evidence_ids:
            fail(f"case reconstruction seed missing {required_id}")

criminal = load_json("assets/data/criminal-engineering-investigation-v1.json")
if criminal:
    issues = {item.get("id"): item for item in criminal.get("priority_issues", [])}
    ce1 = issues.get("CE-001", {})
    if ce1.get("last_reviewed") != "2026-08-20":
        fail("CE-001 has not been source-promoted to 20 August 2026")
    if "textos-definitivos-lpb-base-liquidacion" not in ce1.get("route_es", ""):
        fail("CE-001 Spanish route does not point to the definitive-text baseline")
    if "lpb-definitive-texts-liquidation-baseline" not in ce1.get("route_en", ""):
        fail("CE-001 English route does not point to the definitive-text baseline")

site_base = read("assets/site-base-20260819.js")
if "lpb-definitive-texts-unitary-20260820.js" not in site_base:
    fail("global site loader does not load the LPB definitive-texts module")

shell = read("assets/unitary-public-shell-20260818.js")
if "data/lpb-definitive-texts-route-v1.json" not in shell:
    fail("controlled search does not load the LPB route registry")

architecture = read("assets/case-information-architecture-20260819.js")
if "Paquete judicial certificado completo de los textos definitivos" not in architecture:
    fail("case architecture still lacks the corrected definitive-text missing-evidence wording")
if "Los textos definitivos de abril de 2016" not in architecture:
    fail("case architecture lacks the primary-source promotion statement")
if "textos-definitivos-lpb" not in architecture:
    fail("case architecture does not classify the new route")

for path, marker in [
    ("archive/AC_ACCOUNTING_BRIDGE_15AUG2026.md", "PRIMARY SOURCE PROMOTION — 20 AUG 2026"),
    ("archive/MISSING_EVIDENCE_REGISTER.md", "LPB definitive texts primary baseline located"),
    ("archive/CORRECTION_REGISTER.md", "LPB definitive texts treated as available only through later reconstructions"),
    ("archive/CONTINUOUS_MAINTENANCE_MATRIX.md", "LPB definitive-text baseline"),
    ("archive/SUN_PARK_MASTER_STORYLINE_TIMELINE_1989_2022_16AUG2026.md", "20 August 2026 — LPB definitive-text source promotion"),
    ("CHATGPT_START_HERE.md", "LPB definitive texts / liquidation baseline"),
    ("README.md", "es/textos-definitivos-lpb-base-liquidacion/"),
    ("robots.txt", "sitemap-lpb-definitive-texts.xml"),
    ("sitemap.xml", "/por-derecho/es/textos-definitivos-lpb-base-liquidacion/"),
]:
    if marker not in read(path):
        fail(f"{path} missing propagation marker: {marker}")

sitemap = read("sitemap-lpb-definitive-texts.xml")
for route in [
    "/por-derecho/es/textos-definitivos-lpb-base-liquidacion/",
    "/por-derecho/en/lpb-definitive-texts-liquidation-baseline/",
]:
    if route not in sitemap:
        fail(f"dedicated sitemap missing {route}")

if ERRORS:
    print("LPB definitive-texts validation: FAIL", file=sys.stderr)
    for error in ERRORS:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("LPB definitive-texts validation: PASS")

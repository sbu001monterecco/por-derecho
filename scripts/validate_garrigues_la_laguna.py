#!/usr/bin/env python3
"""Validate the Garrigues / La Laguna publication package."""

from __future__ import annotations

import csv
import json
import re
import sys
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/garrigues-la-laguna-proceeding-v1.json"
ES = ROOT / "es/garrigues-la-laguna/index.html"
EN = ROOT / "en/garrigues-la-laguna/index.html"
TRANSCRIPT = ROOT / "evidence/garrigues-la-laguna/SENTENCIA_41_2014_PUBLIC_TRANSCRIPTION_ES.md"
PUBLIC_COVERAGE = ROOT / "evidence/garrigues-la-laguna/JUAN_TOMAS_PARRILLA_WIDER_MATTER_COVERAGE_REGISTER_ES.md"
REGISTER = ROOT / "archive/GARRIGUES_LA_LAGUNA_344_2013_EVIDENCE_AND_COMMUNICATIONS_REGISTER_24AUG2026.md"
MANIFEST = ROOT / "publication-manifests/garrigues-la-laguna-20260824.json"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


for path in (DATA, ES, EN, TRANSCRIPT, PUBLIC_COVERAGE, REGISTER, MANIFEST):
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")

data = json.loads(DATA.read_text(encoding="utf-8"))
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
texts = {path: path.read_text(encoding="utf-8") for path in (ES, EN, TRANSCRIPT, PUBLIC_COVERAGE, REGISTER)}

if data["proceeding"]["claim_eur"] != 63441.67:
    fail("claim total changed")

invoice_total = sum(Decimal(str(row["amount_eur"])) for row in data["invoices"])
if invoice_total != Decimal("63441.67"):
    fail(f"invoice total is {invoice_total}, expected 63441.67")

excluded = sum(
    Decimal(str(row["amount_eur"]))
    for row in data["invoices"]
    if row["2016_insolvency_treatment"].startswith("Excluded")
)
retained = invoice_total - excluded
if excluded != Decimal("51156.67") or retained != Decimal("12285.00"):
    fail(f"2016 split is excluded={excluded}, retained={retained}")

demand_total = sum(Decimal(str(row["amount_eur"])) for row in data["june_2012_demand_package"]["invoices"])
if demand_total != Decimal("64318.20"):
    fail(f"June 2012 demand total is {demand_total}, expected 64318.20")
if demand_total - Decimal(str(data["proceeding"]["claim_eur"])) != Decimal("876.53"):
    fail("June demand-to-court-claim bridge is not EUR 876.53")

vendor = data["lpb_vendor_ledger_2012"]
vendor_invoice_total = sum(Decimal(str(row["amount_eur"])) for row in vendor["invoice_entries"])
vendor_credit_total = sum(Decimal(str(row["amount_eur"])) for row in vendor["credit_entries"])
if vendor_invoice_total != Decimal("85353.06") or vendor_credit_total != Decimal("66945.90"):
    fail(f"vendor ledger totals changed: invoices={vendor_invoice_total}, credits={vendor_credit_total}")
if vendor_invoice_total - vendor_credit_total != Decimal("18407.16"):
    fail("vendor ledger closing balance is not EUR 18,407.16")

fee = data["parrilla_fee_reconciliation"]
internal_aweswell = sum(Decimal(str(value)) for value in fee["internal_aweswell_accounting"]["entries_eur"])
if internal_aweswell != Decimal("30000.00"):
    fail(f"Aweswell internal accounting entries total is {internal_aweswell}, expected 30000.00")
receipts = sum(Decimal(str(row["amount_eur"])) for row in fee["acknowledged_receipts_2020_account"])
if receipts != Decimal("32250.00"):
    fail(f"Parrilla acknowledged receipts total is {receipts}, expected 32250.00")
if Decimal(str(fee["administrator_reported_payment"]["gross_eur"])) != Decimal("26750.00"):
    fail("Administrator-reported Parrilla payment is not EUR 26,750")

payment_by_track = {row["track"]: Decimal(str(row["amount_eur"])) for row in data["payment_tracks"]}
if payment_by_track.get("HAVAVIDA_TO_GARRIGUES") != Decimal("9450.0"):
    fail("HAVAVIDA→Garrigues track missing or altered")
if payment_by_track.get("CLIENT_TO_PARRILLA_INITIAL", 0) + payment_by_track.get("COSTS_TO_PARRILLA_CREDIT", 0) != Decimal("2500.0"):
    fail("Parrilla defence fee legs do not total EUR 2,500")

required_es = [
    "63.441,67 €",
    "desestimó íntegramente",
    "HAVAVIDA pagó 9.450 € a Garrigues",
    "No fue un pago a Juan Tomás Parrilla",
    "RECONSTRUCCIÓN SECUNDARIA",
    "51.156,67 € excluidos",
    "64.318,20 €",
    "85.353,06 €",
    "Cuadro contable interno Aweswell",
    "26.750 €",
    "no es correcto afirmar que todos los escritos y resoluciones de Parrilla estén ya publicados",
]
required_en = [
    "€63,441.67",
    "dismissed the claim in full",
    "HAVAVIDA paid €9,450 to Garrigues",
    "not a payment to Juan Tomás Parrilla",
    "SECONDARY RECONSTRUCTION",
    "€51,156.67 excluded",
    "€64,318.20",
    "€85,353.06",
    "Internal Aweswell accounting schedule",
    "€26,750",
    "it would be inaccurate to say that every Parrilla pleading and decision is already online",
    "Non-certified translation and summary",
]
for marker in required_es:
    if marker not in texts[ES]:
        fail(f"Spanish marker absent: {marker}")
for marker in required_en:
    if marker not in texts[EN]:
        fail(f"English marker absent: {marker}")

for marker in ("ANTECEDENTES DE HECHO", "FUNDAMENTOS DE DERECHO", "FALLO", "Páginas fuente revisadas: 7/7"):
    if marker not in texts[TRANSCRIPT]:
        fail(f"transcription marker absent: {marker}")

for marker in (
    "No puede confirmarse que todos los escritos y resoluciones judiciales",
    "2.090 mensajes únicos",
    "PO 1241/2011",
    "Medidas cautelares 1355/2011",
    "Concurso 36/2012",
    "Proforma de 29 mayo 2012",
):
    if marker not in texts[PUBLIC_COVERAGE]:
        fail(f"public coverage marker absent: {marker}")

for route in ("es/garrigues-la-laguna/", "en/garrigues-la-laguna/"):
    if route not in manifest["routes"]:
        fail(f"manifest route absent: {route}")
    for sitemap in (ROOT / "sitemap.xml", ROOT / "sitemap-legal-advisers.xml"):
        if route not in sitemap.read_text(encoding="utf-8"):
            fail(f"{route} absent from {sitemap.name}")

for source_page, fragment in (
    (ROOT / "es/continuidad-defensa-letrados/index.html", "../garrigues-la-laguna/"),
    (ROOT / "en/counsel-defence-continuity/index.html", "../garrigues-la-laguna/"),
):
    if fragment not in source_page.read_text(encoding="utf-8"):
        fail(f"missing inbound link in {source_page.relative_to(ROOT)}")

public_package = "\n".join(texts.values())
if re.search(r"\b[0-9a-f]{16}\b", public_package, flags=re.I):
    # The 64-character SHA is intentional. Isolated 16-character Gmail-style IDs are not.
    for match in re.findall(r"\b[0-9a-f]{16}\b", public_package, flags=re.I):
        if match not in data["judgment_source"]["sha256"]:
            fail(f"possible private message identifier exposed: {match}")
if re.search(r"\bES\d{2}[A-Z0-9]{20,}\b", public_package):
    fail("possible IBAN exposed")
if "NIG: 380" in public_package or "IUP: CR" in public_package:
    fail("administrative identifier exposed")

with (ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv").open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
for master_id in ("TF-CIV-006", "LZ-CIV-040", "LZ-CIV-041"):
    matches = [row for row in rows if row.get("Master_ID") == master_id]
    if len(matches) != 1:
        fail(f"expected one {master_id} row, found {len(matches)}")
    if len(matches[0]) != len(rows[0]):
        fail(f"{master_id} CSV column count is malformed")

for marker, path in (
    ("ME-086", ROOT / "archive/MISSING_EVIDENCE_REGISTER.md"),
    ("ME-087", ROOT / "archive/MISSING_EVIDENCE_REGISTER.md"),
    ("CR-088", ROOT / "archive/CORRECTION_REGISTER.md"),
    ("CR-089", ROOT / "archive/CORRECTION_REGISTER.md"),
    ("CR-090", ROOT / "archive/CORRECTION_REGISTER.md"),
):
    if marker not in path.read_text(encoding="utf-8"):
        fail(f"{marker} missing from {path.name}")

print("PASS: Garrigues / La Laguna publication package is internally consistent")

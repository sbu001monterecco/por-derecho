#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/treasury-transparency-7-2026-v1.json"
ES = ROOT / "es/tesoro-transparencia-7-2026-28agosto/index.html"
EN = ROOT / "en/treasury-transparency-7-2026-28-august/index.html"
SITEMAP = ROOT / "sitemap-treasury-transparency-7-2026.xml"
MANIFEST = ROOT / "publication-manifests/treasury-transparency-7-2026-20260830.json"
CONTROL_ID = "PD-TREASURY-TRANSPARENCY-7-2026-20260830-01"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


required = [
    DATA,
    ES,
    EN,
    SITEMAP,
    MANIFEST,
    ROOT / "archive/TESORO_TRANSPARENCIA_7_2026_CONTINUITY_AUDIT_28AUG2026.md",
    ROOT / "docs/deletion-audits/2026-08-30-treasury-transparency-7-2026.md",
]
for path in required:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")

data = json.loads(DATA.read_text(encoding="utf-8"))
if data.get("control_id") != CONTROL_ID:
    fail("wrong control ID")
record = data.get("canonical_administrative_record", {})
if record.get("master_id") != "NAT-TES-001" or record.get("organ") != "Dirección General del Tesoro y Política Financiera":
    fail("canonical administrative identity or organ drift")
if record.get("resolution") != "Resolution 154/2026":
    fail("Resolution 154/2026 not controlled")

official = data.get("official_capacity", {})
if official.get("name") != "María Teresa Bosch Llinares" or official.get("office") != "Directora General del Tesoro y Política Financiera":
    fail("official-capacity attribution drift")

act = data.get("signed_implementation_act", {})
if act.get("pages") != 3 or not re.fullmatch(r"[0-9a-f]{64}", act.get("sha256", "")):
    fail("signed-act denominator or hash invalid")
tranche = data.get("current_production_tranche", {})
if tranche.get("files") != 8 or tranche.get("pages") != 734 or tranche.get("review_status") != "REVIEWED":
    fail("first production tranche must remain reviewed at 8 files / 734 pages")
if tranche.get("remaining_production") != "OPEN_UNDER_ME_110":
    fail("later staged production must remain open under ME-110")

transport = data.get("transport", {})
if transport.get("share_transmissions") != 2 or transport.get("paired_password_transmissions") != 2 or transport.get("event_count") != 1:
    fail("automated transport must remain two paired transmission families / one delivery event")

es = ES.read_text(encoding="utf-8")
en = EN.read_text(encoding="utf-8")
for token in ["María Teresa Bosch Llinares", "Resolución 154/2026", "8 archivos y 734 páginas", "Dos avisos de recurso + dos avisos de contraseña", "producción posterior abierta", "Resolución 28/2026"]:
    if token not in es:
        fail(f"Spanish page missing {token!r}")
for token in ["María Teresa Bosch Llinares", "Resolution 154/2026", "8 files and 734 pages", "Two resource notices + two password notices", "later production open", "Resolution 28/2026"]:
    if token not in en:
        fail(f"English page missing {token!r}")

for html, canonical, alternate in [
    (es, "https://sbu001monterecco.github.io/por-derecho/es/tesoro-transparencia-7-2026-28agosto/", "https://sbu001monterecco.github.io/por-derecho/en/treasury-transparency-7-2026-28-august/"),
    (en, "https://sbu001monterecco.github.io/por-derecho/en/treasury-transparency-7-2026-28-august/", "https://sbu001monterecco.github.io/por-derecho/es/tesoro-transparencia-7-2026-28agosto/"),
]:
    if f'rel="canonical" href="{canonical}"' not in html or alternate not in html or 'hreflang="x-default"' not in html:
        fail("canonical/hreflang parity missing")

public_files = [DATA, ES, EN, MANIFEST, ROOT / "archive/TESORO_TRANSPARENCIA_7_2026_CONTINUITY_AUDIT_28AUG2026.md"]
for path in public_files:
    text = path.read_text(encoding="utf-8")
    for forbidden in ["colabora.tic@", "09:10:56", "09:10:57", "09:11:43", "message_id", "thread_id"]:
        if forbidden.lower() in text.lower():
            fail(f"private transport metadata leaked in {path.relative_to(ROOT)}: {forbidden}")

reciprocal = {
    "es/deuda-publica-ric-canarias/index.html": "../tesoro-transparencia-7-2026-28agosto/",
    "en/canary-ric-public-debt/index.html": "../treasury-transparency-7-2026-28-august/",
    "es/ricpe-responsabilidad-documental/index.html": "../tesoro-transparencia-7-2026-28agosto/",
    "en/ricpe-documentary-accountability/index.html": "../treasury-transparency-7-2026-28-august/",
    "es/registros-institucionales/index.html": "../tesoro-transparencia-7-2026-28agosto/",
    "en/institutional-records/index.html": "../treasury-transparency-7-2026-28-august/",
}
for rel, link in reciprocal.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    if link not in text:
        fail(f"reciprocal route missing from {rel}")

registry = json.loads((ROOT / "assets/data/unitary-route-registry-v1.json").read_text(encoding="utf-8"))
paths = [item.get("path") for item in registry]
for route in ["es/tesoro-transparencia-7-2026-28agosto/", "en/treasury-transparency-7-2026-28-august/"]:
    if paths.count(route) != 1:
        fail(f"route registry count must be one for {route}")

ET.parse(SITEMAP)
sitemap = SITEMAP.read_text(encoding="utf-8")
if sitemap.count("<url>") != 2 or 'hreflang="x-default"' not in sitemap:
    fail("dedicated sitemap must contain two bilingual URL records")
if "sitemap-treasury-transparency-7-2026.xml" not in (ROOT / "robots.txt").read_text(encoding="utf-8"):
    fail("robots.txt does not expose the dedicated sitemap")

with (ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv").open("r", encoding="utf-8-sig", newline="") as handle:
    rows = {row["Master_ID"]: row for row in csv.DictReader(handle)}
row = rows.get("NAT-TES-001")
if not row:
    fail("NAT-TES-001 missing from canonical proceedings register")
if row.get("Origin_Organ") != "Dirección General del Tesoro y Política Financiera" or row.get("Source_Status") != "VERIFIED_PRIMARY":
    fail("NAT-TES-001 organ or source status not corrected")
if "7/2026" not in row.get("Reference", "") or "734 pages" not in row.get("Latest_Known_Event", ""):
    fail("NAT-TES-001 does not expose the corrected reference and reviewed denominator")
if "Gmail " in row.get("Primary_Source_Anchor", ""):
    fail("NAT-TES-001 retains a provider-native private source anchor")

internal = (ROOT / "archive/MASTER_PROCEEDINGS_REGISTER_INTERNAL_20AUG2026.md").read_text(encoding="utf-8")
if "ADM-CAN-002 | Dirección General del Tesoro y Política Financiera" not in internal:
    fail("internal summary does not correct ADM-CAN-002")
if "ADM-CAN-002 | Viceconsejería de Hacienda" in internal:
    fail("stale Resolution 154/2026 organ attribution remains")

for rel, token in [
    ("archive/CORRECTION_REGISTER.md", "CR-151"),
    ("archive/MISSING_EVIDENCE_REGISTER.md", "ME-110"),
    ("archive/CONTINUOUS_MAINTENANCE_MATRIX.md", "Treasury transparency 7/2026"),
]:
    if token not in (ROOT / rel).read_text(encoding="utf-8"):
        fail(f"{token} missing from {rel}")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("publication_id") != CONTROL_ID:
    fail("manifest/control ID mismatch")
if manifest.get("source_corpus", {}).get("binary_publication") != "EXCLUDED_PRIVATE_SOURCE_BINARIES":
    fail("private-source binary exclusion missing")

print("Treasury transparency 7/2026 validation passed: official capacity, 8-file / 734-page review, one Colabora delivery event, file separation, privacy, bilingual discovery and canonical proceedings correction OK.")

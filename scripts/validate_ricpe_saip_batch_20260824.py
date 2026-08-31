#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ricpe-saip-batch-20260824.json"
ES = ROOT / "es" / "ricpe-acciones-pendientes-ahora" / "index.html"
EN = ROOT / "en" / "ricpe-outstanding-actions-now" / "index.html"
OPS = ROOT / "operations" / "RICPE_SAIP_BATCH_24AUG2026.md"
MODULE = ROOT / "assets" / "ricpe-saip-batch-status-20260824.js"
SITE = ROOT / "assets" / "site.js"

EXPECTED = [
    "REGAGE26e00075132698",
    "REGAGE26e00075135054",
    "REGAGE26e00075135386",
    "REGAGE26e00075135813",
    "REGAGE26e00075136198",
    "REGAGE26e00075136446",
    "REGAGE26e00075136691",
    "REGAGE26e00075136953",
]
PUBLIC_FILES = [DATA, ES, EN, OPS, MODULE]
PRIVATE_TYPE_PATTERNS = (
    ("Spanish identity document", re.compile(r"\b(?:[XYZ]\d{7}[A-Z]|\d{8}[A-Z])\b", re.IGNORECASE)),
    ("email address", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)),
)
PRIVATE_TWO_WORD_PHRASE_DIGESTS = {
    "e6e16c4f92c018a6844166b8ab7c274d7c2d763d152281c456b7e671e7cd9c0f"
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def contains_private_phrase(value: str) -> bool:
    """Match the protected street-name fragment without storing it in public Git."""

    words = re.findall(r"\w+", value.casefold(), flags=re.UNICODE)
    for start in range(len(words) - 1):
        candidate = " ".join(words[start : start + 2])
        digest = hashlib.sha256(candidate.encode("utf-8")).hexdigest()
        if digest in PRIVATE_TWO_WORD_PHRASE_DIGESTS:
            return True
    return False


for path in [DATA, ES, EN, OPS, MODULE, SITE]:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")

data = json.loads(DATA.read_text(encoding="utf-8"))
filings = data.get("filings", [])
if len(filings) != 8:
    fail(f"expected 8 filings, found {len(filings)}")
if data.get("counts") != {"total": 8, "new_access_requests": 5, "supplements": 3}:
    fail("count object must be exactly 8 / 5 / 3")

registrations = [item.get("registration") for item in filings]
if registrations != EXPECTED:
    fail("REGAGE sequence differs from controlled batch")

if sum(item.get("type_es") == "Nueva SAIP" for item in filings) != 5:
    fail("expected five new SAIPs")
if sum(item.get("type_es") == "Aportación" for item in filings) != 3:
    fail("expected three supplements")

es = ES.read_text(encoding="utf-8")
en = EN.read_text(encoding="utf-8")
for reg in EXPECTED:
    if reg not in es or reg not in en:
        fail(f"{reg} missing from one or both canonical pages")

if "A05033187" not in es or not any(term in es for term in ("remisión interna", "traslado interno")):
    fail("Presidency route must retain actual recipient and internal-transfer qualification")
if "separada de comunicaciones supervisoras" not in es:
    fail("CNMV access route must remain separate from supervisory communications")
if "Do not infer the opening of a supervisory investigation" not in en:
    fail("English CNMV boundary missing")

for path in PUBLIC_FILES:
    text = path.read_text(encoding="utf-8")
    for label, pattern in PRIVATE_TYPE_PATTERNS:
        if pattern.search(text):
            fail(f"private {label} found in {path.relative_to(ROOT)}")
    if contains_private_phrase(text):
        fail(f"digest-matched private street fragment found in {path.relative_to(ROOT)}")

site = SITE.read_text(encoding="utf-8")
if "ricpe-saip-batch-status-20260824.js" not in site:
    fail("site.js does not load the batch status module")
for inherited in [
    "SOURCE-OF-FUNDS-NOTICE-20260820",
    "AC-COMMUNITY-DE-FACTO-ADMINISTRATION-LOADERS-20260824",
    "CALIFICACION-CRIMINAL-MISUSE-THESIS-20260824",
]:
    if inherited not in site:
        fail(f"inherited site loader marker missing: {inherited}")

print("RICPE SAIP batch validation passed: 8 filings, 5 new requests, 3 supplements, privacy, parity and inherited-loader controls OK.")

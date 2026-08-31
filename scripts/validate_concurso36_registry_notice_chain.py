#!/usr/bin/env python3
"""Validate the public-safe Concurso 36/2012 Registry notice publication."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets/data/concurso36-court-record-reconstruction-registry-notice-20260831.json"
ES_PATH = ROOT / "es/concurso-36-2012-aviso-registro-ob-rem/index.html"
EN_PATH = ROOT / "en/insolvency-36-2012-registry-ob-rem-notice/index.html"

EXPECTED_ATTACHMENTS = {
    "EVID-2018-REG-NOTICE-ATT-01": (4, "be2580c8f112992e09afacb820a848ab4a22a18fb98fe7fb0bc942dfc31c2870"),
    "EVID-2018-REG-NOTICE-ATT-02": (2, "69bee623d50d63245a0b0d2012f91c1c1d669aa0d6cc002d8880eb47b2c4ab26"),
    "EVID-2018-REG-NOTICE-ATT-03": (13, "c4b1a374d57e391a18ab30f3ee68a12289d6a649f42fb8eba8bf6ff0a4f5ee0a"),
    "EVID-2018-REG-NOTICE-ATT-04": (16, "aa255f3d4660815bc8019df05e4e534778e3b6a3ccf8b4a3a46d83ab30151d39"),
    "EVID-2018-REG-NOTICE-ATT-05": (4, "3967fc7030ce045f5b5d7ef698229023e9e1cd8b6e2df58c41382775e075d557"),
    "EVID-2018-REG-NOTICE-ATT-06": (8, "2f0d6e97e81ade3a5c3c104fdc248e342a479a0440e6371525765c8a3c4a1b50"),
    "EVID-2018-REG-NOTICE-ATT-07": (18, "4bb344b12c3fdb5f931352af9e5a191830136e5df8bfe27caf539f111bfe886f"),
    "EVID-2018-REG-NOTICE-ATT-08": (13, "60ad417a2fb4c6cbb3335d2b85e35f0547efbc08e0d3f9ffdf621499a852ed29"),
    "EVID-2018-REG-NOTICE-ATT-09": (18, "60922c8436d1f7cb0bf616e97c256372a33a4c385af16cb20e1f0d99c267c842"),
    "EVID-2018-REG-NOTICE-ATT-10": (2, "4f23ad7e30191b1d32c8708851729f42151c3b095476255d5fe1a5fc43509099"),
}


errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def text(path: Path) -> str:
    require(path.is_file(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


data = json.loads(text(DATA_PATH))
families = data.get("additional_families", [])
require(len(families) == 1, "supplement must contain exactly one additional family")
family = families[0] if families else {}
require(family.get("family_id") == "C36-FAM-2018-2019-REGISTRY-NOTICE", "family ID mismatch")
records = family.get("records", [])
require(len(records) == 8, "Registry notice family must contain eight records")
record_ids = [item.get("id") for item in records]
require(len(record_ids) == len(set(record_ids)), "record IDs must be unique")
require("C36-REC-20190104-BUROFAX-DELIVERED" in record_ids, "4-Jan delivery event missing")
require("C36-REC-20190109-REGISTRAR-RESPONSE" in record_ids, "Registrar response event missing")
require("C36-REC-20190109-REGISTRY-QUALIFICATION-2018-DEED" in record_ids, "qualification event missing")

attachments = data.get("attachment_evidence_bundle", [])
require(len(attachments) == 10, "attachment bundle must contain ten items")
observed = {item.get("evidence_id"): (item.get("pages"), item.get("sha256")) for item in attachments}
require(observed == EXPECTED_ATTACHMENTS, "attachment page counts or SHA-256 values differ from control set")
for item in attachments:
    require(bool(re.fullmatch(r"[0-9a-f]{64}", item.get("sha256", ""))), f"invalid SHA-256 for {item.get('evidence_id')}")

es = text(ES_PATH)
en = text(EN_PATH)
for marker in ["4 de enero de 2019 a las 11:58", "24 de octubre de 2019", "estafa procesal", "ob rem", "Francisco Javier Nieto González", "Alberto López Villarrubia"]:
    require(marker.casefold() in es.casefold(), f"Spanish page missing marker: {marker}")
for marker in ["4 January 2019 at 11:58", "24 October 2019", "procedural fraud", "ob rem", "Francisco Javier Nieto González", "Alberto López Villarrubia"]:
    require(marker.casefold() in en.casefold(), f"English page missing marker: {marker}")
require("href=\"../../en/insolvency-36-2012-registry-ob-rem-notice/\"" in es, "Spanish alternate link missing")
require("href=\"../../es/concurso-36-2012-aviso-registro-ob-rem/\"" in en, "English alternate link missing")

js = text(ROOT / "assets/concurso36-court-record-reconstruction.js")
require("concurso36-court-record-reconstruction-registry-notice-20260831.json" in js, "control-room loader does not fetch new supplement")
for page in [ROOT / "es/concurso-36-2012-registro-procesal/index.html", ROOT / "en/insolvency-36-2012-court-record/index.html"]:
    body = text(page)
    require("45" in body, f"45-node status missing from {page.relative_to(ROOT)}")
    require("registry-notice-20260831.json" in body, f"supplement link missing from {page.relative_to(ROOT)}")

crosslinks = {
    "es/2018-proteccion-leal-masa/index.html": "concurso-36-2012-aviso-registro-ob-rem/",
    "en/2018-loyal-protection-estate/index.html": "insolvency-36-2012-registry-ob-rem-notice/",
    "es/cuatrecasas-sun-park/index.html": "concurso-36-2012-aviso-registro-ob-rem/",
    "en/cuatrecasas-sun-park/index.html": "insolvency-36-2012-registry-ob-rem-notice/",
    "es/cuatrecasas-dp748-accion-civil/index.html": "concurso-36-2012-aviso-registro-ob-rem/",
    "en/cuatrecasas-dp748-civil-action/index.html": "insolvency-36-2012-registry-ob-rem-notice/",
    "es/concurso-36-2012-administrador-concursal/index.html": "concurso-36-2012-aviso-registro-ob-rem/",
    "en/insolvency-36-2012-insolvency-administrator/index.html": "insolvency-36-2012-registry-ob-rem-notice/",
    "es/ric-private-equity-sun-park/index.html": "concurso-36-2012-aviso-registro-ob-rem/",
    "en/ric-private-equity-sun-park/index.html": "insolvency-36-2012-registry-ob-rem-notice/",
}
for relative, marker in crosslinks.items():
    require(marker in text(ROOT / relative), f"cross-link missing from {relative}")

for sitemap in [ROOT / "sitemap.xml", ROOT / "sitemap-concurso36-court-orders.xml"]:
    body = text(sitemap)
    require("/es/concurso-36-2012-aviso-registro-ob-rem/" in body, f"Spanish route missing from {sitemap.name}")
    require("/en/insolvency-36-2012-registry-ob-rem-notice/" in body, f"English route missing from {sitemap.name}")

require((ROOT / "archive/CONCURSO36_REGISTRY_NOTICE_OBREM_CHAIN_31AUG2026.md").is_file(), "continuity record missing")
manifest = json.loads(text(ROOT / "publication-manifests/concurso36-registry-notice-obrem-20260831.json"))
require(manifest.get("controlled_node_count_after_merge") == 45, "manifest node count mismatch")
require(manifest.get("current_state") in {"PREPARED_PENDING_MERGE", "PR_OPEN", "CI_GREEN", "MERGED", "DEPLOYED", "LIVE_VERIFIED", "DELETION_SAFE"}, "manifest state invalid")

public_bundle = "\n".join([es, en, json.dumps(data, ensure_ascii=False)])
privacy_patterns = [
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    r"message[_ -]?id",
    r"gmail[^\s<]*\.com",
]
for pattern in privacy_patterns:
    require(not re.search(pattern, public_bundle, re.IGNORECASE), f"private locator pattern exposed: {pattern}")

if errors:
    print("Registry notice chain validation FAILED", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Registry notice chain validation passed: 8 events, 10 attachments, 45-node control-room target, bilingual routes and cross-links verified.")

#!/usr/bin/env python3
"""Validate the Concurso 36/2012 linked-continuity release."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CONTROL = "PD-C36-LINKED-CONTINUITY-20260829-01"

REQUIRED = [
    "CONCURSO36_CONTINUE_HERE.md",
    "archive/CONCURSO36_DOCKET_CONTINUITY_RECONCILIATION_29AUG2026.md",
    "archive/MASTER_CONTINUATION_PROMPT_CONCURSO36_AND_LINKED_THREADS_29AUG2026.md",
    "archive/OTHER_THREAD_RECONCILIATION_QUEUE_29AUG2026.md",
    "archive/MISSING_EVIDENCE_REGISTER_CONCURSO36_DECISION_CONTINUITY_ADDENDUM_28AUG2026.md",
    "archive/CONCURSO_36_2012_DOCKET_WIDE_DISCOVERY_PROMOTION_REGISTER_17AUG2026.md",
    "assets/data/concurso36-linked-continuity-20260829-v1.json",
    "en/insolvency-36-2012-continuity-control/index.html",
    "es/concurso-36-2012-control-continuidad/index.html",
    "sitemap-concurso36-court-orders.xml",
    "publication-manifests/concurso36-linked-continuity-20260829.json",
    "docs/deletion-audits/2026-08-29-concurso36-linked-continuity.md",
]

CANONICAL_HASHES = {
    "archive/MISSING_EVIDENCE_REGISTER_CONCURSO36_DECISION_CONTINUITY_ADDENDUM_28AUG2026.md":
        "6e4351dec0516c4908d57f22fbd0ccade66ba80d2b17080a6ea6807fb536ff2c",
    "archive/CONCURSO_36_2012_DOCKET_WIDE_DISCOVERY_PROMOTION_REGISTER_17AUG2026.md":
        "d804bd43373fb24004ac41fe6271e4ed626e0e454f999fded4bf48db1d03552b",
}

errors: list[str] = []

for rel in REQUIRED:
    if not (ROOT / rel).is_file():
        errors.append(f"missing required file: {rel}")

for rel, expected in CANONICAL_HASHES.items():
    p = ROOT / rel
    if p.is_file():
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != expected:
            errors.append(f"canonical source hash changed: {rel}: {actual} != {expected}")

data_path = ROOT / "assets/data/concurso36-linked-continuity-20260829-v1.json"
manifest_path = ROOT / "publication-manifests/concurso36-linked-continuity-20260829.json"

if data_path.is_file():
    data = json.loads(data_path.read_text(encoding="utf-8"))
    if data.get("control_id") != CONTROL:
        errors.append("machine register control_id mismatch")
    if data.get("release_type") != "continuity_reconciliation_no_new_evidence_promotion":
        errors.append("machine register release type changed")
    if data.get("external_action_authorized") is not False:
        errors.append("external action must remain false")
    if len(data.get("open_evidence_gates", {}).get("P0", [])) != 9:
        errors.append("expected nine P0 evidence gates")
    if len(data.get("open_evidence_gates", {}).get("P1", [])) != 2:
        errors.append("expected two P1 evidence gates")
    if data.get("source_equivalence", {}).get("result") != "EXACT_MATCH__CANONICAL_MAIN_COPIES_CONTROL":
        errors.append("exact source-equivalence control missing")
    statuses = {w.get("status", "") for w in data.get("workstreams", [])}
    if not any("LEGAL_PRIVACY_GATE" in s for s in statuses):
        errors.append("legal/privacy legacy gate missing")
    if data.get("legacy_pr_default") != "COMPARE_CURRENT_MAIN__TRANSPLANT_ONLY__NO_WHOLESALE_MERGE":
        errors.append("legacy PR default weakened")

if manifest_path.is_file():
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("control_id") != CONTROL:
        errors.append("manifest control_id mismatch")
    if manifest.get("controlled_result", {}).get("new_evidence_promoted") is not False:
        errors.append("manifest must state no new evidence promoted")
    if manifest.get("authority", {}).get("email") is not False:
        errors.append("manifest email authority must remain false")
    if manifest.get("authority", {}).get("filing") is not False:
        errors.append("manifest filing authority must remain false")

html_checks = {
    "en/insolvency-36-2012-continuity-control/index.html": [
        "Continuity closed. Evidence gaps remain open.",
        "No new evidence promoted",
        "../../es/concurso-36-2012-control-continuidad/",
        "filing → receipt → opposition → decision",
    ],
    "es/concurso-36-2012-control-continuidad/index.html": [
        "Continuidad cerrada. Las lagunas probatorias siguen abiertas.",
        "Sin nueva prueba promovida",
        "../../en/insolvency-36-2012-continuity-control/",
        "escrito → recepción → oposición → resolución",
        "Denominador certificado",
        "Serie de informes de la Administración Concursal",
    ],
}

for rel, needles in html_checks.items():
    p = ROOT / rel
    if p.is_file():
        text = p.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing marker {needle!r}")
        if "mailto:" in text.lower():
            errors.append(f"{rel}: mailto link is not permitted")
        if "tel:" in text.lower():
            errors.append(f"{rel}: telephone link is not permitted")

prompt_path = ROOT / "archive/MASTER_CONTINUATION_PROMPT_CONCURSO36_AND_LINKED_THREADS_29AUG2026.md"
if prompt_path.is_file():
    prompt = prompt_path.read_text(encoding="utf-8")
    for needle in [
        "WORKBOOK OR REFERENCE → LOCATE SOURCE",
        "Never merge an old branch wholesale",
        "Not authorised:",
        "private counsel identities, advice or drafts",
        "Never substitute rhetorical completion for evidential completion.",
    ]:
        if needle not in prompt:
            errors.append(f"master prompt missing control: {needle}")

sitemap = ROOT / "sitemap-concurso36-court-orders.xml"
if sitemap.is_file():
    try:
        tree = ET.parse(sitemap)
        locs = {
            node.text
            for node in tree.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/"
                                      "{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        }
        required_locs = {
            "https://sbu001monterecco.github.io/por-derecho/en/insolvency-36-2012-continuity-control/",
            "https://sbu001monterecco.github.io/por-derecho/es/concurso-36-2012-control-continuidad/",
        }
        if not required_locs.issubset(locs):
            errors.append("continuity routes missing from court-orders sitemap")
    except ET.ParseError as exc:
        errors.append(f"invalid sitemap XML: {exc}")

if errors:
    print("FAIL — Concurso 36/2012 linked continuity")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print("PASS — Concurso 36/2012 linked continuity")
print(" - exact canonical source hashes preserved")
print(" - 9 P0 and 2 P1 gates remain explicit")
print(" - bilingual routes and reciprocal links present")
print(" - no new evidence promotion and no external action")
print(" - legacy branches remain current-main/transplant gated")

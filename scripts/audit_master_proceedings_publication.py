#!/usr/bin/env python3
"""Fail closed on Master Proceedings Register publication and continuity drift."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
PROTOCOL = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER_PROTOCOL.md"
GOVERNANCE = ROOT / "archive/MASTER_PROCEEDINGS_PUBLICATION_GOVERNANCE_30AUG2026.md"
EN = ROOT / "en/master-proceedings-register/index.html"
ES = ROOT / "es/registro-maestro-procedimientos/index.html"
JS = ROOT / "assets/master-proceedings-publication-20260830.js"
CSS = ROOT / "assets/master-proceedings-publication-20260830.css"
SITE = ROOT / "assets/site.js"
MANIFEST = ROOT / "publication-manifests/master-proceedings-publication-20260830.json"
MARKER = "MASTER_PROCEEDINGS_PUBLICATION_GATE"


def main() -> int:
    errors: list[str] = []
    required = [CSV, PROTOCOL, GOVERNANCE, EN, ES, JS, CSS, SITE, MANIFEST]
    for path in required:
        if not path.exists():
            errors.append(f"missing required publication control: {path.relative_to(ROOT)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    protocol = PROTOCOL.read_text(encoding="utf-8")
    governance = GOVERNANCE.read_text(encoding="utf-8")
    en = EN.read_text(encoding="utf-8")
    es = ES.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    site = SITE.read_text(encoding="utf-8")

    for path, text in ((PROTOCOL, protocol), (GOVERNANCE, governance), (SITE, site)):
        if MARKER not in text:
            errors.append(f"{path.relative_to(ROOT)} missing {MARKER}")

    for path, text, route, alternate in (
        (EN, en, "/en/master-proceedings-register/", "/es/registro-maestro-procedimientos/"),
        (ES, es, "/es/registro-maestro-procedimientos/", "/en/master-proceedings-register/"),
    ):
        if "data-master-proceedings-page" not in text:
            errors.append(f"{path.relative_to(ROOT)} missing public-register mount")
        if route not in text or alternate not in text:
            errors.append(f"{path.relative_to(ROOT)} missing canonical/reciprocal route linkage")
        if "TRUE" not in text or "FALSE" not in text or "UNVERIFIED" not in text:
            errors.append(f"{path.relative_to(ROOT)} must explain TRUE/FALSE/UNVERIFIED")

    required_js_phrases = (
        "PROCEEDINGS_MASTER_REGISTER.csv",
        "INTERNAL_ONLY",
        "NOT_SITE_AGGREGATED",
        "data-master-proceedings-nav",
        "data-master-proceedings-timeline-link",
        "Open_Reference_Gap",
        "Parent_Master_ID",
        "Linked_Proceedings",
    )
    for phrase in required_js_phrases:
        if phrase not in js:
            errors.append(f"public projection runtime missing control phrase: {phrase}")

    if "master-proceedings-publication-20260830.js" not in site:
        errors.append("assets/site.js does not load the master proceedings public runtime")

    required_columns = {
        "Master_ID", "Record_Type", "Is_Proceeding", "Proceeding_Class", "Stream",
        "Origin_Organ", "Current_Custodian", "Reference", "Date_or_Period", "Connection",
        "Object_or_Purpose", "Status", "Latest_Known_Event", "Appeal_or_Review",
        "Parent_Master_ID", "Linked_Proceedings", "Source_Status", "Open_Reference_Gap",
        "Public_Treatment",
    }
    with CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = sorted(required_columns - columns)
        if missing:
            errors.append("master CSV missing public-spine columns: " + ", ".join(missing))
        rows = list(reader)

    if not rows:
        errors.append("master CSV contains no rows")
    true_count = sum(1 for row in rows if (row.get("Is_Proceeding") or "").strip().upper() == "TRUE")
    unverified_count = sum(1 for row in rows if (row.get("Is_Proceeding") or "").strip().upper() == "UNVERIFIED")
    legacy_count = sum(1 for row in rows if (row.get("Public_Treatment") or "").strip() == "INTERNAL_KNOWLEDGE_REGISTER_NOT_AUTO_PUBLISHED")
    if true_count == 0:
        errors.append("master CSV unexpectedly contains no TRUE proceeding/file rows")
    if legacy_count and "legacy non-automatic-publication" not in protocol:
        errors.append("protocol must explain legacy public-treatment compatibility")

    for forbidden in ("do not create or promote a public aggregate proceedings page", "not a public-facing “all cases” page"):
        if forbidden.lower() in protocol.lower():
            errors.append(f"stale anti-publication rule remains in protocol: {forbidden}")

    if errors:
        print("MASTER PROCEEDINGS PUBLICATION AUDIT: FAILED")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("MASTER PROCEEDINGS PUBLICATION AUDIT: PASSED")
    print(f"Canonical rows: {len(rows)}")
    print(f"TRUE proceedings/files: {true_count}")
    print(f"UNVERIFIED candidates: {unverified_count}")
    print(f"Legacy public-treatment rows eligible for controlled projection: {legacy_count}")
    print("Bilingual routes, sitewide navigation/timeline interlinking, public-field boundaries and continuity governance verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

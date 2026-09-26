#!/usr/bin/env python3
"""Regression controls for Red SARA/AGE and authority-response discovery."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from build_redsara_age_filings_register import OUTPUT, build, serialized
from prepare_orion_notice_register_20260905 import load_notice_events
from load_completed_filings_20260921 import load_existing_cajasiete_events

ROOT = Path(__file__).resolve().parents[1]
COMMUNICATIONS = ROOT / "assets/data/institutional-communications-register-v1.json"
SHELL = ROOT / "assets/unitary-public-shell-20260818.js"
REGISTER_SCRIPT = ROOT / "assets/authority-communications-register-20260901.js"
EN_PAGE = ROOT / "en/red-sara-age-filings-authority-responses/index.html"
ES_PAGE = ROOT / "es/registros-redsara-age-y-respuestas-autoridades/index.html"
ROUTES = [
    ROOT / "assets/data/unitary-route-registry-v1.json",
    ROOT / "assets/data/unitary-route-registry-sync-20260819.json",
]
EMAIL_RE = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
INTERVENCION_REFERENCES = ("184368/2026", "497011/2026", "699645/2026")


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    try:
        actual = OUTPUT.read_text(encoding="utf-8")
        projection = json.loads(actual)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot load Red SARA/AGE projection: {exc}", file=sys.stderr)
        return 1
    if actual != serialized(build()):
        fail("Red SARA/AGE projection is not deterministic", errors)
    if projection.get("schema") != "por-derecho.redsara-age-filings-register.v1":
        fail("unexpected Red SARA/AGE projection schema", errors)
    scope = projection.get("scope_and_boundary", {})
    if scope.get("filing_event_rows_currently_individualised") != 400:
        fail("projection must contain the 398-row 21-Sep census plus two source-proved 24-Sep REGAGE successors", errors)
    if scope.get("separate_source_proved_regage_events") != 325:
        fail("projection must contain 325 non-baseline source-proved REGAGE events after the two 24-Sep successors", errors)
    if scope.get("detailed_baseline_receipts") != 75:
        fail("projection must retain 75 detailed baseline receipts", errors)
    if scope.get("historic_regage_total_reported") != 97:
        fail("projection must retain the 97-record historical denominator", errors)
    if "current 21-Sep-2026 census contains 398" not in str(scope.get("reconciliation_boundary", "")):
        fail("projection lacks the current-vs-historical REGAGE reconciliation boundary", errors)
    if len(projection.get("attachment_index", [])) != 100:
        fail("projection must retain the 100-entry public-safe attachment index", errors)
    if EMAIL_RE.search(actual):
        fail("projection contains an email address", errors)

    communications = json.loads(COMMUNICATIONS.read_text(encoding="utf-8"))
    events = communications.get("events", [])
    regage = [event for event in events if event.get("channel") == "REGAGE"]
    incoming = [event for event in events if event.get("direction") == "INBOUND_FROM_INSTITUTION"]
    from prepare_platform_incibe_20260925 import validated_platform_event_ids
    platform_ids = validated_platform_event_ids(events, ROOT)
    platform_incoming = [e for e in incoming if e['event_id'] in platform_ids]
    if len(regage) != 400:
        fail(f"canonical source has {len(regage)} rather than 400 REGAGE events", errors)
    status_export_regage = [event for event in regage if str(event.get("source_key", "")).startswith("REGAGE_STATUS_EXPORT_20260921:")]
    formal_regage = [event for event in regage if not str(event.get("source_key", "")).startswith("REGAGE_STATUS_EXPORT_20260921:")]
    if len(status_export_regage) != 284:
        fail(f"canonical source has {len(status_export_regage)} rather than 284 status-export-only REGAGE events", errors)
    if len(formal_regage) != 116:
        fail(f"canonical source has {len(formal_regage)} rather than 116 formal REGAGE event identities", errors)
    # The historical 163-row incoming cohort is preserved, not silently redefined.
    # New notice rows are independently compared with their controlled source set.
    notice_expected = {
        event['event_id']: event for event in load_notice_events(ROOT)
        if event.get('direction') == 'INBOUND_FROM_INSTITUTION'
    }
    cajasiete_expected = {
        event['event_id']: event for event in load_existing_cajasiete_events(ROOT)
        if event.get('direction') == 'INBOUND_FROM_INSTITUTION'
    }
    additive_batches = {'PD-SP-ORION-NOTICE-20260905', 'PD-CAJASIETE-ACCOUNTABILITY-20260918'}
    supplemental_incoming = [event for event in incoming if str(event.get('source_key', '')).startswith('SUPPLEMENTAL_20260924:')]
    legacy_incoming = [event for event in incoming if event.get('source_batch_id') not in additive_batches and not str(event.get('source_key', '')).startswith('SUPPLEMENTAL_20260924:') and event['event_id'] not in platform_ids]
    notice_found = {event['event_id']: event for event in incoming if event.get('source_batch_id') == 'PD-SP-ORION-NOTICE-20260905'}
    cajasiete_found = {event['event_id']: event for event in incoming if event.get('source_batch_id') == 'PD-CAJASIETE-ACCOUNTABILITY-20260918'}
    if len(legacy_incoming) != 163:
        fail(f"canonical source has {len(legacy_incoming)} rather than 163 legacy incoming institutional events", errors)
    if notice_found != notice_expected:
        fail("additive Orion notice incoming cohort differs from its source-controlled records", errors)
    if cajasiete_found != cajasiete_expected:
        fail("additive Cajasiete incoming cohort differs from its source-controlled records", errors)
    if len(supplemental_incoming) != 3:
        fail(f"24-Sep supplemental incoming cohort has {len(supplemental_incoming)} rather than 3 events", errors)
    if len(incoming) != 163 + len(notice_expected) + len(cajasiete_expected) + len(supplemental_incoming) + len(platform_incoming):
        fail("combined incoming-event denominator does not reconcile", errors)
    for event in incoming:
        for field in ("event_id", "event_date", "official_reference", "office", "source_integrity"):
            if not event.get(field):
                fail(f"incoming authority event lacks {field}: {event.get('event_id')}", errors)
    matching = [event for event in incoming if event.get("official_reference") in INTERVENCION_REFERENCES]
    if [event.get("official_reference") for event in matching] != list(INTERVENCION_REFERENCES):
        fail("the three controlled Intervención references are not fully registered in order", errors)
    if any(event.get("office") != "Intervención General de la Comunidad Autónoma de Canarias" for event in matching):
        fail("Intervención office identity drift", errors)

    shell = SHELL.read_text(encoding="utf-8")
    for marker in (
        "institutional-communications-register-v1.json",
        "buildInstitutionalEntries",
        "exactTerms",
        "const exact=scored.filter",
        "authorityRegister",
    ):
        if marker not in shell:
            fail(f"global search omits authority-discovery control: {marker}", errors)
    for page in (EN_PAGE, ES_PAGE):
        text = page.read_text(encoding="utf-8")
        for marker in ("data-authority-register", "authority-communications-register-20260901.js", "authority-communications-register-20260901.css"):
            if marker not in text:
                fail(f"{page.relative_to(ROOT)} omits {marker}", errors)
    if "communication-PD-SP-EVT-0141" not in REGISTER_SCRIPT.read_text(encoding="utf-8") and "event.event_id" not in REGISTER_SCRIPT.read_text(encoding="utf-8"):
        fail("authority-register renderer cannot produce canonical event anchors", errors)
    expected_paths = {
        "en": "en/red-sara-age-filings-authority-responses/",
        "es": "es/registros-redsara-age-y-respuestas-autoridades/",
    }
    for route_path in ROUTES:
        rows = json.loads(route_path.read_text(encoding="utf-8"))
        for lang, path in expected_paths.items():
            row = next((item for item in rows if item.get("lang") == lang and item.get("path") == path), None)
            if row is None:
                fail(f"{route_path.relative_to(ROOT)} lacks {lang} authority-register route", errors)
            elif "184368/2026" not in row.get("aliases", []):
                fail(f"{route_path.relative_to(ROOT)} does not expose 184368/2026 as a route alias", errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("Red SARA/AGE and authority-response discovery controls pass; legacy cohort and additive notice rows reconcile")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

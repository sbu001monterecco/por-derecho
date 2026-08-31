#!/usr/bin/env python3
"""Validate the ACTA lifecycle, LPH and cross-track canonical controls."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from acta_lph_lifecycle_control import (
    CANONICAL_REFERENCE_RULE,
    CRITICAL_LPH_TIMELINE,
    CROSS_TRACK_MODEL,
    HISTORICAL_LPH_VERSIONS,
    LPH_GATES,
    STAGE_TO_GATE,
    STATUS,
    validate_lph_control,
)


REPO = Path(__file__).resolve().parents[1]
CONTINUITY = REPO / "evidence/community/actas/event-family-continuity-v1.json"
LINEAGE = REPO / "evidence/community/actas/meeting-lineage-index-v1.json"
ROUTES = {
    "es": "es/comunidad-instrumentalizacion/sala-documental-actas/control-lph-ciclo-juntas/index.html",
    "en": "en/community-instrumentalisation/acta-document-room/meeting-lifecycle-lph-control/index.html",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    continuity = json.loads(CONTINUITY.read_text(encoding="utf-8"))
    lineage = json.loads(LINEAGE.read_text(encoding="utf-8"))
    documents = continuity["documents"]
    document_ids = [document["stable_id"] for document in documents]
    document_id_set = set(document_ids)

    if len(documents) != 122:
        fail(errors, f"expected 122 continuity documents, found {len(documents)}")
    if len(document_id_set) != len(document_ids):
        fail(errors, "continuity document stable IDs are not unique")
    try:
        validate_lph_control(document_id_set)
    except ValueError as exc:
        fail(errors, str(exc))

    if lineage.get("canonical_evidence_reference_count") != 122:
        fail(errors, "machine lineage canonical evidence count is not 122")
    if lineage.get("canonical_evidence_reference_rule") != CANONICAL_REFERENCE_RULE:
        fail(errors, "machine lineage canonical reference rule drift")
    if lineage.get("lph_lifecycle_gate_definitions") != LPH_GATES:
        fail(errors, "machine lineage LPH gate drift")
    if lineage.get("lph_lifecycle_status_definitions") != STATUS:
        fail(errors, "machine lineage LPH status drift")
    if lineage.get("historical_lph_versions") != HISTORICAL_LPH_VERSIONS:
        fail(errors, "machine lineage historical LPH version drift")
    if lineage.get("cross_track_criminal_hypothesis_model") != CROSS_TRACK_MODEL:
        fail(errors, "machine lineage cross-track model drift")
    if lineage.get("critical_lph_timeline_event_count") != len(CRITICAL_LPH_TIMELINE):
        fail(errors, "machine lineage critical LPH event count drift")

    lineage_events = {event["id"]: event for event in lineage["events"]}
    machine_docs: dict[str, dict] = {}
    for event in lineage["events"]:
        for document in event.get("documents", []):
            stable_id = document["stable_id"]
            reference = document.get("canonical_reference", {})
            if reference.get("stable_id") != stable_id:
                fail(errors, f"{stable_id}: missing canonical-reference stable ID")
            if set(reference).issuperset({"stable_id", "es", "en", "reference_status"}) is False:
                fail(errors, f"{stable_id}: incomplete canonical-reference object")
            expected_gate = STAGE_TO_GATE.get(document.get("relationship_stage"), "—")
            if document.get("lph_gate_codes") != expected_gate:
                fail(errors, f"{stable_id}: lifecycle gate drift")
            existing = machine_docs.get(stable_id)
            if existing and existing.get("canonical_reference") != reference:
                fail(errors, f"{stable_id}: conflicting repeated canonical reference")
            machine_docs[stable_id] = document
    if set(machine_docs) != document_id_set:
        fail(errors, "machine lineage does not cover exactly all 122 continuity documents")

    for event_id, control in CRITICAL_LPH_TIMELINE.items():
        event = lineage_events.get(event_id)
        if not event:
            fail(errors, f"missing critical event {event_id}")
            continue
        if event.get("lph_lifecycle_control") != control:
            fail(errors, f"{event_id}: machine LPH control drift")
        for locale, page_key in (("es", "detail_page_es"), ("en", "detail_page_en")):
            page = REPO / event[page_key]
            text = page.read_text(encoding="utf-8")
            if 'id="control-lph-ciclo"' not in text:
                fail(errors, f"{page}: missing event LPH section")
            if text.count('class="lph-gate-code"') < 5:
                fail(errors, f"{page}: fewer than five visible LPH gates")
            for gate_id, gate in control["gates"].items():
                if gate_id not in text or f'data-lph-status="{gate["status"]}"' not in text:
                    fail(errors, f"{page}: missing {gate_id}/{gate['status']}")
                for evidence_id in gate["evidence_ids"]:
                    if evidence_id not in text:
                        fail(errors, f"{page}: missing LPH evidence link {evidence_id}")

    for locale, route in ROUTES.items():
        page = REPO / route
        if not page.is_file():
            fail(errors, f"missing dedicated LPH page {route}")
            continue
        text = page.read_text(encoding="utf-8")
        if "122 / 122" not in text:
            fail(errors, f"{route}: missing canonical denominator")
        for gate_id in LPH_GATES:
            if gate_id not in text:
                fail(errors, f"{route}: missing visible gate {gate_id}")
        for status_id in STATUS:
            if f'data-lph-status="{status_id}"' not in text:
                fail(errors, f"{route}: missing status {status_id}")
        for grade_id in CROSS_TRACK_MODEL["grades"]:
            if f'data-cross-grade="{grade_id}"' not in text:
                fail(errors, f"{route}: missing cross-track grade {grade_id}")
        for stable_id in document_ids:
            if f"<code>{stable_id}</code>" not in text:
                fail(errors, f"{route}: canonical ledger missing {stable_id}")
        for document in documents:
            stable_id = document["stable_id"]
            canonical = document["bilingual_event_routes"][locale]
            target = REPO / canonical
            if not target.is_file():
                fail(errors, f"{stable_id}: missing {locale} canonical target {canonical}")
                continue
            target_text = target.read_text(encoding="utf-8")
            if f'id="{stable_id}"' not in target_text:
                fail(errors, f"{stable_id}: missing {locale} canonical fragment")
        for track in CROSS_TRACK_MODEL["tracks"]:
            target = track[f"route_{locale}"]
            if not (REPO / target / "index.html").is_file():
                fail(errors, f"cross-track {track['id']}: missing route {target}")
            if target not in text:
                fail(errors, f"{route}: missing cross-track link {target}")
        for phrase in (
            "D-MIXED/D-OPEN",
            "SP-ACTA-2011-06-22",
            "SP-ACTA-2018-05-18",
            "SP-RECITAL-2018-11-20",
            "SP-ACTA-2022-02-04",
        ):
            if phrase not in text:
                fail(errors, f"{route}: missing boundary/spine phrase {phrase}")

    sitemap = (REPO / "sitemap.xml").read_text(encoding="utf-8")
    for route in ROUTES.values():
        public = route.removesuffix("index.html")
        if public not in sitemap:
            fail(errors, f"sitemap missing {public}")

    css = (REPO / "assets/acta-document-room-20260822.css").read_text(encoding="utf-8")
    for selector in (
        '[data-lph-status="facial-concern"]',
        '[data-lph-status="unlocated"]',
        '.lph-gate-flow',
        '.lph-timeline-matrix',
        '.lph-canonical-ledger',
        '[data-cross-grade="attributed-criminal-hypothesis"]',
        '.cross-track-spine',
        '.cross-track-branches',
    ):
        if selector not in css:
            fail(errors, f"CSS missing {selector}")

    governance = (
        REPO / ".github/governance/COMMUNITY_MEETING_LIFECYCLE_CANONICAL_EVIDENCE_PROTOCOL_31AUG2026.md"
    ).read_text(encoding="utf-8")
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    for phrase in (
        "G1 — authority and call",
        "Canonical evidence reference",
        "Criminal-investigative interconnectivity",
        "D-MIXED",
        "document-specific transmission",
    ):
        if phrase.lower() not in governance.lower():
            fail(errors, f"governance missing {phrase}")
    if "COMMUNITY_MEETING_LIFECYCLE_CANONICAL_EVIDENCE_PROTOCOL_31AUG2026.md" not in agents:
        fail(errors, "AGENTS.md does not activate Community lifecycle governance")

    if errors:
        print("ACTA LPH lifecycle validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("ACTA LPH lifecycle validation: PASS")
    print("- 122/122 unique evidence/communication IDs have bilingual canonical route+fragment controls")
    print(f"- {len(CRITICAL_LPH_TIMELINE)} critical C1→C2 events carry five historical LPH gates")
    print("- criminal-hypothesis, direct-documentary, open-reliance and institutional-notice links remain distinct")
    print("- D-MIXED/D-OPEN remains an evidence status, not a criminal actor perimeter")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

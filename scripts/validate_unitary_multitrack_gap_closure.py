#!/usr/bin/env python3
"""Validate the advisory unitary criminal-first gap-closure control."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/unitary-multitrack-criminal-first-gap-closure-v1.json"
LINEAGE = ROOT / "evidence/community/actas/meeting-lineage-index-v1.json"
AUTHORITY = ROOT / "assets/data/community-acta-authority-interconnectivity-v1.json"
CRIMINAL_GRAPH = ROOT / "assets/data/criminal-first-2011-unitary-graph-v1.json"
EVENT_CONTINUITY = ROOT / "evidence/community/actas/event-family-continuity-v1.json"
INTERVENCION_RESPONSE = ROOT / "es/intervencion-general-699645-2026/index.html"
COMMUNICATIONS = ROOT / "assets/data/institutional-communications-register-v1.json"
CAEPR_PROFESSIONAL = ROOT / "assets/data/caepr-caret-fti-meeting-point-professional-institutional-v1.json"
CAEPR_RICPE = ROOT / "assets/data/caepr-caret-fti-meeting-point-ricpe-continuity-v1.json"
CAEPR_INSTITUTIONS = ROOT / "assets/data/matter-identity-registry-v1.institutions.json"
PUBLICATION_MANIFEST = ROOT / "publication-manifests/unitary-public-authority-communications-20260901.json"
LIVE_CLOSEOUT = ROOT / "archive/UNITARY_PUBLIC_AUTHORITY_COMMUNICATIONS_LIVE_CLOSEOUT_01SEP2026.md"
CONTROL_ID = "PD-UCF-20260901-01"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    required = [
        DATA,
        LINEAGE,
        AUTHORITY,
        CRIMINAL_GRAPH,
        EVENT_CONTINUITY,
        ROOT / "assets/unitary-multitrack-gap-closure-20260901.css",
        ROOT / "assets/unitary-multitrack-gap-closure-20260901.js",
        ROOT / "scripts/build_unitary_multitrack_gap_closure.py",
        ROOT / "scripts/build_community_acta_authority_interconnectivity.py",
        ROOT / ".github/workflows/advisory-unitary-multitrack-gap-closure.yml",
        ROOT / ".github/governance/UNITARY_MULTI_TRACK_CRIMINAL_FIRST_PROSECUTORIAL_FORENSIC_PROTOCOL_01SEP2026.md",
        ROOT / "archive/UNITARY_MULTITRACK_CRIMINAL_FIRST_GAP_CLOSURE_CONTROL_01SEP2026.md",
        ROOT / "archive/prompts/UNITARY_MULTI_TRACK_CRIMINAL_FIRST_GAP_CLOSURE_EXECUTION_PROMPT_01SEP2026.md",
        ROOT / "es/ingenieria-inversa-criminal-unitaria/index.html",
        ROOT / "en/unitary-criminal-reverse-engineering/index.html",
        ROOT / "es/comunidad-instrumentalizacion/sala-documental-actas/control-lph-ciclo-juntas/index.html",
        ROOT / "en/community-instrumentalisation/acta-document-room/meeting-lifecycle-lph-control/index.html",
        ROOT / "es/actas-comunidad-autoridades-publicas/index.html",
        ROOT / "en/community-actas-public-authorities/index.html",
        INTERVENCION_RESPONSE,
        CAEPR_PROFESSIONAL,
        CAEPR_RICPE,
        CAEPR_INSTITUTIONS,
        COMMUNICATIONS,
        PUBLICATION_MANIFEST,
        LIVE_CLOSEOUT,
        ROOT / "es/administracion-de-hecho-comunidad-ac/index.html",
        ROOT / "en/de-facto-administration-community-ac/index.html",
        ROOT / "es/concurso-36-2012-analisis-penal-forense-unitario/index.html",
        ROOT / "en/insolvency-36-2012-unitary-criminal-forensic-analysis/index.html",
        ROOT / "es/ric-private-equity-sun-park/index.html",
        ROOT / "en/ric-private-equity-sun-park/index.html",
        ROOT / "es/intervencion-general-siinf-trazabilidad/index.html",
        ROOT / "en/intervencion-general-siinf-traceability/index.html",
    ]
    for path in required:
        require(path.exists(), f"missing required file: {path.relative_to(ROOT)}", errors)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1

    data = load(DATA)
    lineage = load(LINEAGE)
    authority = load(AUTHORITY)
    criminal = load(CRIMINAL_GRAPH)
    continuity = load(EVENT_CONTINUITY)
    caepr_professional = load(CAEPR_PROFESSIONAL)
    caepr_ricpe = load(CAEPR_RICPE)
    communications = load(COMMUNICATIONS)
    publication_manifest = load(PUBLICATION_MANIFEST)

    require(data.get("schema_version") == "1.0.0", "schema version changed", errors)
    require(data.get("control_id") == CONTROL_ID, "control ID changed", errors)
    require(
        data.get("status") == "PUBLICATION_AUTHORISED_VALIDATION_PENDING",
        "pre-deployment machine snapshot state changed; live status belongs to the successor manifest",
        errors,
    )
    require(
        publication_manifest.get("publication_id")
        == "PD-SP-UNITARY-PUBLIC-AUTHORITY-COMMS-20260901-01"
        and publication_manifest.get("current_state") == "LIVE_VERIFIED"
        and publication_manifest.get("state")
        == "LIVE_VERIFIED_WITH_ACCEPTED_PUBLICATION_BOUNDARY_GAP"
        and publication_manifest.get("merge_sha")
        == "a2873cd865567da1b6644f32821bb15ece53a160"
        and publication_manifest.get("verification", {}).get("live_http_readback")
        is True
        and publication_manifest.get("verification", {}).get("deletion_safe")
        is False
        and publication_manifest.get("closeout_record")
        == "archive/UNITARY_PUBLIC_AUTHORITY_COMMUNICATIONS_LIVE_CLOSEOUT_01SEP2026.md",
        "successor publication manifest is not live-verified with the accepted boundary gap",
        errors,
    )
    require(data.get("canonical_routes") == {
        "es": "es/ingenieria-inversa-criminal-unitaria/",
        "en": "en/unitary-criminal-reverse-engineering/",
    }, "canonical route pair changed", errors)

    classes = data.get("evidence_classes", [])
    class_ids = [item.get("id") for item in classes]
    require(class_ids == ["DOC", "HIP", "OPEN", "NOTICE", "CONTRARY", "ADVERSE", "GAP"], "evidence-class order/identity changed", errors)
    for item in classes:
        require(item.get("symbol"), f"{item.get('id')}: text/symbol fallback missing", errors)
        require(item.get("label_es") and item.get("label_en"), f"{item.get('id')}: bilingual label missing", errors)

    tracks = data.get("tracks", [])
    track_ids = [track.get("id") for track in tracks]
    require(track_ids == [f"T{number:02d}" for number in range(1, 19)], "18-track finite set changed", errors)
    for track in tracks:
        require(track.get("label_es") and track.get("label_en"), f"{track.get('id')}: bilingual label missing", errors)
        require(track.get("criminal_question_es") and track.get("criminal_question_en"), f"{track.get('id')}: criminal question missing", errors)
        require(set(track.get("primary_classes", [])).issubset(class_ids), f"{track.get('id')}: unknown evidence class", errors)

    threshold_fields = data.get("method", {}).get("criminal_threshold_fields", [])
    require(len(threshold_fields) == 17 and len(set(threshold_fields)) == 17, "criminal-threshold matrix must contain 17 unique fields", errors)
    require(data.get("method", {}).get("output_order") == [
        "criminal_prosecutorial",
        "civil_horizontal_property",
        "insolvency",
        "administrative",
        "regulatory_public_funds",
        "professional_discipline",
        "recovery_restitution",
    ], "criminal-first legal-output order changed", errors)

    hypotheses = data.get("criminal_threshold_hypotheses", [])
    hypothesis_ids = {item.get("id") for item in hypotheses}
    require(len(hypotheses) == 5 and len(hypothesis_ids) == 5, "five finite threshold hypotheses required", errors)
    require(hypothesis_ids == {f"PD-HYP-UCF-{number:03d}" for number in range(1, 6)}, "five canonical hypothesis IDs changed", errors)
    hypothesis_required = {
        "status", "actor_capacity_es", "actor_capacity_en", "act_es", "act_en",
        "knowledge_intent_es", "knowledge_intent_en", "use_effect_benefit_es",
        "use_effect_benefit_en", "contrary_es", "contrary_en", "open_proof_es",
        "open_proof_en", "potential_relevance", "source_refs",
    }
    for item in hypotheses:
        missing = hypothesis_required - set(item)
        require(not missing, f"{item.get('id')}: missing threshold fields {sorted(missing)}", errors)
        require(item.get("contrary_es") and item.get("contrary_en"), f"{item.get('id')}: contrary case missing", errors)

    gaps = data.get("gaps", [])
    gap_ids = [gap.get("id") for gap in gaps]
    require(gap_ids == [f"PD-GAP-UCF-{number:03d}" for number in range(1, 17)], "16 canonical gap IDs changed", errors)
    require(len(set(gap_ids)) == 16, "duplicate canonical gap ID", errors)
    require(sum(gap.get("priority") == "P1" for gap in gaps) == 2, "P1 denominator changed", errors)
    for gap in gaps:
        require(gap.get("priority") in {"P0", "P1"}, f"{gap.get('id')}: invalid priority", errors)
        require(gap.get("status"), f"{gap.get('id')}: closure status missing", errors)
        require(set(gap.get("tracks", [])).issubset(track_ids), f"{gap.get('id')}: unknown track", errors)
        require(gap.get("source_refs"), f"{gap.get('id')}: canonical/source reference missing", errors)
        for key in ("title_es", "title_en", "custodian_es", "custodian_en", "closure_es", "closure_en"):
            require(gap.get(key), f"{gap.get('id')}: missing {key}", errors)

    nodes = data.get("reverse_chain", {}).get("nodes", [])
    edges = data.get("reverse_chain", {}).get("edges", [])
    node_ids = [node.get("id") for node in nodes]
    require(node_ids == [f"RC{number:02d}" for number in range(12)], "12-node reverse chain changed", errors)
    require(len(edges) == 11, "reverse chain must have 11 finite edges", errors)
    for position, edge in enumerate(edges):
        require(edge.get("from") == node_ids[position] and edge.get("to") == node_ids[position + 1], f"edge {position}: reverse-chain order broken", errors)
        require(edge.get("status") in class_ids, f"edge {position}: unknown evidence class", errors)
        require(edge.get("closure_gap") in gap_ids, f"edge {position}: unknown closure gap", errors)
    for node in nodes:
        require(set(node.get("classes", [])).issubset(class_ids), f"{node.get('id')}: unknown evidence class", errors)
        require(set(node.get("tracks", [])).issubset(track_ids), f"{node.get('id')}: unknown track", errors)

    propagation = data.get("authority_legitimacy_propagation", {})
    stages = propagation.get("stages", [])
    stage_ids = [stage.get("id") for stage in stages]
    require(stage_ids == [f"AUTH-UCF-{number:03d}" for number in range(1, 11)], "10-stage authority-propagation chain changed", errors)
    for stage in stages:
        for key in ("label_es", "label_en", "proposition_es", "proposition_en", "test_es", "test_en", "source_refs", "gap_ids", "route_es", "route_en"):
            require(stage.get(key), f"{stage.get('id')}: missing {key}", errors)
        require(set(stage.get("classes", [])).issubset(class_ids), f"{stage.get('id')}: unknown evidence class", errors)
        require(set(stage.get("tracks", [])).issubset(track_ids), f"{stage.get('id')}: unknown track", errors)
        require(set(stage.get("gap_ids", [])).issubset(gap_ids), f"{stage.get('id')}: unknown closure gap", errors)
    notice = propagation.get("notice_checkpoint", {})
    require(notice.get("id") == "PD-EV-UCF-INT-184368-2026", "first Intervención response canonical evidence ID missing", errors)
    require(notice.get("master_file_id") == "X-INT-004", "first Intervención response master-file link missing", errors)
    require(notice.get("canonical_event_id") == "PD-SP-EVT-0141", "first Intervención legacy/event crosswalk missing", errors)
    require(notice.get("commission_date") == "2026-02-24", "first Intervención Commission date changed", errors)
    require(notice.get("presentation_caret_state") == "CARET_NOT_APPLICABLE", "document must not receive a presentation caret", errors)
    require(notice.get("issuing_institution_identity_state") == "CARET_CONFIRMED", "institution identity threshold closure missing", errors)
    require(notice.get("issuing_institution_caepr_id") == "PD-SP-I-0043", "issuing institution CAEPR crosslink missing", errors)
    require(notice.get("caret_command_audit") == "REPAIRED_VERIFIED_IDENTITY_OPEN_MERITS", "user-command caret audit state missing", errors)
    require(notice.get("caret_command_audit_label") == "REPAIRED / VERIFIED IDENTITY / OPEN MERITS", "human-readable caret audit state missing", errors)
    institutions = load(CAEPR_INSTITUTIONS).get("records", [])
    intervention_identity = next((item for item in institutions if item.get("id") == "PD-SP-I-0043"), {})
    require(intervention_identity.get("identity_resolution") == "CARET_CONFIRMED", "PD-SP-I-0043 is not caret-confirmed", errors)
    require(len(intervention_identity.get("source_urls", [])) >= 2, "PD-SP-I-0043 lacks official identity sources", errors)
    authority_intervencion = next((item for item in authority.get("authority_files", []) if item.get("master_id") == "X-INT-004"), {})
    expected_intervencion_refs = ["PD-EV-UCF-INT-184368-2026", "PD-SP-EVT-0141", "PD-SP-EVT-0142", "PD-SP-EVT-0143"]
    require(authority_intervencion.get("canonical_evidence_refs") == expected_intervencion_refs, "authority register lacks the three-response canonical evidence interlink", errors)
    require(authority_intervencion.get("communication_event_ids") == ["PD-SP-EVT-0141", "PD-SP-EVT-0142", "PD-SP-EVT-0143"], "authority register lacks the three-response communication sequence", errors)
    require(authority_intervencion.get("unitary_authority_stage_ids") == ["AUTH-UCF-005", "AUTH-UCF-009", "AUTH-UCF-010"], "authority register lacks propagation-stage interlinks", errors)
    require(authority_intervencion.get("unitary_gap_ids") == ["PD-GAP-UCF-009", "PD-GAP-UCF-012", "PD-GAP-UCF-015", "PD-GAP-UCF-016"], "authority register lacks canonical gap interlinks", errors)
    require(authority.get("by_master_id", {}).get("X-INT-004", {}).get("canonical_evidence_refs") == expected_intervencion_refs, "reciprocal authority index lacks the three-response interlink", errors)
    professional_intervencion = next((item for item in caepr_professional.get("records", []) if item.get("object_key") == "INTERVENCION_GENERAL_EXACT"), {})
    ricpe_intervencion = next((item for item in caepr_ricpe.get("records", []) if item.get("object_key") == "INTERVENCION_GENERAL"), {})
    for item, label in ((professional_intervencion, "professional CAEPR"), (ricpe_intervencion, "RICPE CAEPR")):
        require(item.get("state") == "CARET_PENDING", f"{label}: dated predecessor snapshot changed without a successor transition", errors)
        require(item.get("label") == "Intervención General de la Comunidad Autónoma de Canarias", f"{label}: resolved regional organ name missing", errors)
        require(item.get("evidence_refs") == ["PD-EV-UCF-INT-184368-2026", "X-INT-004"], f"{label}: canonical evidence interlink missing", errors)
        require("DIR3" in item.get("next_source_needed", ""), f"{label}: remaining identity source not stated", errors)

    denominators = {item["id"]: item["value"] for item in data.get("denominator_crosswalk", [])}
    expected_denominators = {
        "DEN-UCF-001": lineage["controlled_event_family_count"],
        "DEN-UCF-002": lineage["controlled_event_family_count"] * 2,
        "DEN-UCF-003": authority["coverage"]["public_acta_packages"],
        "DEN-UCF-004": lineage["canonical_evidence_reference_count"],
        "DEN-UCF-005": lineage["critical_lph_timeline_event_count"],
        "DEN-UCF-006": authority["coverage"]["public_authority_files"],
        "DEN-UCF-007": authority["coverage"]["evidentiary_axes"],
        "DEN-UCF-008": len(criminal["nodes"]),
        "DEN-UCF-009": len(tracks),
        "DEN-UCF-010": len(gaps),
        "DEN-UCF-011": authority["coverage"]["public_authority_communication_events"],
    }
    require(denominators == expected_denominators, f"denominator crosswalk drift: expected {expected_denominators}, got {denominators}", errors)
    require(lineage.get("canonical_evidence_reference_count") == lineage.get("source_communication_document_count") == len(continuity.get("documents", [])) == 122, "122-object lifecycle denominator drift", errors)
    require(authority["coverage"] == {
        "public_acta_packages": 20,
        "public_authority_files": 49,
        "authority_groups": 6,
        "evidentiary_axes": 7,
        "community_2022_milestones": 3,
        "adjudication_and_deed_milestones": 6,
        "verified_primary_authority_files": 33,
        "verified_procedural_authority_files": 8,
        "open_or_primary_pending_authority_files": 8,
        "public_authority_communication_events": 19,
        "authority_tiers_represented": 5,
        "confirmed_identity_communication_events": 3,
        "pending_identity_communication_events": 16,
    }, "20/49/7 authority denominator source drift", errors)

    public_authority_control = propagation.get("public_authority_communications", {})
    expected_event_ids = ["PD-SP-EVT-0004", "PD-SP-EVT-0014", *[f"PD-SP-EVT-{number:04d}" for number in range(141, 158)]]
    require(public_authority_control.get("checkpoint_event_ids") == expected_event_ids, "19-event authority checkpoint set changed", errors)
    require(public_authority_control.get("legacy_crosswalk") == {"PD-EV-UCF-INT-184368-2026": "PD-SP-EVT-0141"}, "legacy evidence crosswalk changed", errors)
    require(public_authority_control.get("required_tier_ids") == ["ES_LOCAL_MUNICIPAL", "ES_ISLAND_CABILDO", "ES_CANARY_AUTONOMOUS", "ES_STATE", "EU_SUPRANATIONAL"], "five-tier communication requirement changed", errors)
    authority_event_ids = [event["event_id"] for event in authority.get("public_communications", [])]
    register_event_ids = [event["event_id"] for event in communications.get("events", []) if event.get("authority_tier_id")]
    require(authority_event_ids == register_event_ids == expected_event_ids, "unitary, authority and communications event sets do not reconcile", errors)
    canonical_master_ids = {record["master_id"] for record in authority.get("authority_files", [])}
    axis_ids = {axis["id"] for axis in authority.get("evidentiary_axes", [])}
    recognised_refs = canonical_master_ids | set(expected_event_ids) | axis_ids | {"PD-EV-UCF-INT-184368-2026", *stage_ids, *hypothesis_ids}
    for gap in gaps:
        for source_ref in gap.get("source_refs", []):
            if source_ref.startswith(("LZ-", "NAT-", "X-", "PD-SP-EVT-", "PD-EV-UCF-", "AX-", "AUTH-UCF-", "PD-HYP-UCF-")):
                require(source_ref in recognised_refs, f"{gap['id']}: unresolved canonical source reference {source_ref}", errors)
    canonical_gap_refs = json.dumps([gap.get("source_refs", []) for gap in gaps], ensure_ascii=False)
    require(not any(alias in canonical_gap_refs for alias in ("LZ-YAIZA-", "LZ-CABILDO-", "SALIDA-184368-2026")), "orphan Yaiza/Cabildo/Intervención aliases remain in canonical source_refs", errors)

    serial = json.dumps(data, ensure_ascii=False)
    lower = serial.lower()
    require("d_mixed_and_d_open_are_evidence_statuses_not_criminal_perimeters" in lower, "D-MIXED/D-OPEN non-actor rule missing", errors)
    require("^ marker confirms only" in lower and "signo ^ confirma únicamente" in lower, "caret identity-only rule missing", errors)
    require("criminal group" in lower and "grupo criminal" in lower, "collective-guilt boundary missing", errors)
    require("mecanismo criminal organizado, coordinado y continuado" in lower, "direct Spanish organised/coordinated/continuous criminal attribution missing", errors)
    require("organised, coordinated and continuous criminal mechanism" in lower, "direct English organised/coordinated/continuous criminal attribution missing", errors)
    require("deuda supuestamente fabricada o inexacta" in lower and "allegedly fabricated or inaccurate debt" in lower, "attributed fabricated/inaccurate-debt position missing", errors)
    require("mera irregularidad civil/lph" in lower and "merely civil/lph irregularity" in lower, "non-dilution civil/LPH rule missing", errors)
    require("apparent_authority_may_propagate_as_input_criminal_responsibility_does_not" in lower, "authority-input/responsibility non-transfer rule missing", errors)
    for forbidden in ("recipient_email", "sender_email", "private_locator", "source_locator", "message_id", "password", "access_token"):
        require(forbidden not in lower, f"forbidden public/private key or value: {forbidden}", errors)
    require(not re.search(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", serial), "email address exposed in public dataset", errors)

    css_marker = "unitary-multitrack-gap-closure-20260901.css?v=20260901c"
    js_marker = "unitary-multitrack-gap-closure-20260901.js?v=20260901c"
    unitary_pages = [
        ROOT / "es/ingenieria-inversa-criminal-unitaria/index.html",
        ROOT / "en/unitary-criminal-reverse-engineering/index.html",
    ]
    for page in unitary_pages:
        text = page.read_text(encoding="utf-8")
        require(f'data-ucf-control="{CONTROL_ID}"' in text, f"{page.relative_to(ROOT)}: mount missing", errors)
        require(css_marker in text and js_marker in text, f"{page.relative_to(ROOT)}: cache-busted assets missing", errors)
        require("unitary-criminal-reverse-engineering-20260820" in text, f"{page.relative_to(ROOT)}: preserved legacy analysis marker missing", errors)
        require("community-acta-authority-interconnectivity-v1.json" in (ROOT / "assets/unitary-multitrack-gap-closure-20260901.js").read_text(encoding="utf-8"), "unitary renderer lacks canonical authority-communications source", errors)

    reciprocal_expectations = {
        ROOT / "es/comunidad-instrumentalizacion/sala-documental-actas/control-lph-ciclo-juntas/index.html": [
            "/es/actas-comunidad-autoridades-publicas/", "/es/ingenieria-inversa-criminal-unitaria/",
        ],
        ROOT / "en/community-instrumentalisation/acta-document-room/meeting-lifecycle-lph-control/index.html": [
            "/en/community-actas-public-authorities/", "/en/unitary-criminal-reverse-engineering/",
        ],
        ROOT / "es/actas-comunidad-autoridades-publicas/index.html": [
            "../comunidad-instrumentalizacion/sala-documental-actas/control-lph-ciclo-juntas/", "../ingenieria-inversa-criminal-unitaria/#unitary-gap-register",
        ],
        ROOT / "en/community-actas-public-authorities/index.html": [
            "../community-instrumentalisation/acta-document-room/meeting-lifecycle-lph-control/", "../unitary-criminal-reverse-engineering/#unitary-gap-register",
        ],
    }
    for page, markers in reciprocal_expectations.items():
        text = page.read_text(encoding="utf-8")
        for marker in markers:
            require(marker in text, f"{page.relative_to(ROOT)}: reciprocal marker missing {marker}", errors)

    propagation_pages = [
        ROOT / "es/administracion-de-hecho-comunidad-ac/index.html",
        ROOT / "en/de-facto-administration-community-ac/index.html",
        ROOT / "es/concurso-36-2012-analisis-penal-forense-unitario/index.html",
        ROOT / "en/insolvency-36-2012-unitary-criminal-forensic-analysis/index.html",
        ROOT / "es/ric-private-equity-sun-park/index.html",
        ROOT / "en/ric-private-equity-sun-park/index.html",
        ROOT / "es/intervencion-general-siinf-trazabilidad/index.html",
        ROOT / "en/intervencion-general-siinf-traceability/index.html",
    ]
    for page in propagation_pages:
        text = page.read_text(encoding="utf-8")
        require('data-ucf-authority-propagation-link="PD-UCF-20260901-01"' in text, f"{page.relative_to(ROOT)}: authority-propagation reciprocal link missing", errors)
        require("#unitary-authority-propagation" in text, f"{page.relative_to(ROOT)}: propagation anchor missing", errors)
        require("#evidence-PD-EV-UCF-INT-184368-2026" in text, f"{page.relative_to(ROOT)}: Intervención evidence anchor missing", errors)

    response_text = INTERVENCION_RESPONSE.read_text(encoding="utf-8")
    for marker in ("184368/2026", "497011/2026", "699645/2026", "No certifica"):
        require(marker.lower() in response_text.lower(), f"public Intervención three-response source missing: {marker}", errors)

    governance = (ROOT / ".github/governance/UNITARY_MULTI_TRACK_CRIMINAL_FIRST_PROSECUTORIAL_FORENSIC_PROTOCOL_01SEP2026.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    bootstrap = (ROOT / "CHATGPT_START_HERE.md").read_text(encoding="utf-8")
    maintenance = (ROOT / "archive/CONTINUOUS_MAINTENANCE_MATRIX.md").read_text(encoding="utf-8")
    for text, label in ((governance, "protocol"), (agents, "AGENTS"), (bootstrap, "bootstrap"), (maintenance, "maintenance")):
        require(CONTROL_ID in text, f"{label}: control activation marker missing", errors)
        require("criminal-first" in text.lower() or "penal" in text.lower(), f"{label}: criminal-first rule missing", errors)
        require("PD-EV-UCF-INT-184368-2026" in text, f"{label}: first Intervención evidence continuity marker missing", errors)
        require("PD-GAP-UCF-015" in text and "PD-GAP-UCF-016" in text, f"{label}: new gap continuity markers missing", errors)
    require("advisory" in governance.lower() and "shadow" in governance.lower(), "new validator must remain advisory/shadow", errors)

    workflow = (ROOT / ".github/workflows/advisory-unitary-multitrack-gap-closure.yml").read_text(encoding="utf-8")
    for marker in (
        "continue-on-error: true",
        "assets/data/caepr-caret-fti-meeting-point-professional-institutional-v1.json",
        "assets/data/caepr-caret-fti-meeting-point-ricpe-continuity-v1.json",
        "assets/data/community-acta-authority-interconnectivity-v1.json",
        "scripts/build_community_acta_authority_interconnectivity.py",
        "en/de-facto-administration-community-ac/index.html",
        "en/insolvency-36-2012-unitary-criminal-forensic-analysis/index.html",
        "en/intervencion-general-siinf-traceability/index.html",
        "en/ric-private-equity-sun-park/index.html",
        "es/administracion-de-hecho-comunidad-ac/index.html",
        "es/concurso-36-2012-analisis-penal-forense-unitario/index.html",
        "es/intervencion-general-siinf-trazabilidad/index.html",
        "es/ric-private-equity-sun-park/index.html",
    ):
        require(marker in workflow, f"advisory workflow continuity marker missing: {marker}", errors)

    authority_build = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_community_acta_authority_interconnectivity.py"), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(authority_build.returncode == 0, authority_build.stdout.strip() or authority_build.stderr.strip() or "authority interconnectivity builder check failed", errors)
    build = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_unitary_multitrack_gap_closure.py"), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(build.returncode == 0, build.stdout.strip() or build.stderr.strip() or "deterministic builder check failed", errors)
    node = subprocess.run(
        ["node", "--check", str(ROOT / "assets/unitary-multitrack-gap-closure-20260901.js")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(node.returncode == 0, node.stdout.strip() or node.stderr.strip() or "JavaScript syntax check failed", errors)

    if errors:
        print("UNITARY MULTI-TRACK GAP CLOSURE: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1
    print("UNITARY MULTI-TRACK GAP CLOSURE: PASS")
    print(" - 18 tracks; 12 reverse-chain nodes; 10 authority-propagation stages; 7 evidence classes; 5 threshold hypotheses")
    print(" - 16 canonical gaps; 23 events; 122 lifecycle objects; 20 ACTA packages; 49 authority files; 19 authority communications")
    print(" - validator mode: advisory/shadow; preparation snapshot retained; successor manifest is LIVE_VERIFIED with an accepted publication-boundary gap")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

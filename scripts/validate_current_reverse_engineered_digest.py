#!/usr/bin/env python3
"""Validate the current unitary repository/website reverse-engineered digest."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "CURRENT_REVERSE_ENGINEERED_DIGEST.md"
STATE = ROOT / "ops" / "CURRENT_REVERSE_ENGINEERED_DIGEST.json"
HISTORICAL_MANIFEST = ROOT / "publication-manifests" / "unitary-repository-website-redigest-20260827.json"
ALBERTO_MANIFEST = ROOT / "publication-manifests" / "alberto-meeting-point-multidirectional-criminal-first-20260827.json"
FTI_MANIFEST = ROOT / "publication-manifests" / "fti-meeting-point-ricpe-continuity-20260827.json"
CLOSEOUT = ROOT / "archive" / "CURRENT_REVERSE_ENGINEERED_DIGEST_LIVE_CLOSEOUT_27AUG2026.md"
MATRIX = ROOT / "assets" / "data" / "alberto-meeting-point-357-multidirectional-evidence-v1.json"
SPECIALIST_CARET = ROOT / "assets" / "data" / "caepr-caret-alberto-meeting-point-357-v1.json"
FIRST_HOP_CARET = ROOT / "assets" / "data" / "caepr-caret-alberto-meeting-point-first-hop-v1.json"
FTI_CONTINUITY_CARET = ROOT / "assets" / "data" / "caepr-caret-fti-meeting-point-ricpe-continuity-v1.json"
FTI_PROFESSIONAL_CARET = ROOT / "assets" / "data" / "caepr-caret-fti-meeting-point-professional-institutional-v1.json"
FTI_ACTIONS = ROOT / "ops" / "FTI_MEETING_POINT_RICPE_CROSSBORDER_ACTION_REGISTER_27AUG2026.json"
FTI_MONITOR = ROOT / "ops" / "FTI_MEETING_POINT_CANARY_SPAIN_ASSET_TRANSACTION_MONITOR_CONTROL_27AUG2026.json"
FTI_MONITOR_REGISTER = ROOT / "assets" / "data" / "fti-meeting-point-canary-spain-asset-transaction-register-v1.json"
CURRENT_UNITARY_STATE = ROOT / "ops" / "CURRENT_UNITARY_STATE.json"
UNITARY_CARET = ROOT / "assets" / "data" / "caepr-caret-unitary-digest-v1.json"
REGISTRY = ROOT / "assets" / "data" / "matter-identity-registry-v1.json"

DIGEST_SNAPSHOT_IDENTITY_COUNTS = {
    "total": 336,
    "PERSON": 157,
    "ORGANISATION": 83,
    "STRUCTURE": 11,
    "INSTITUTION": 42,
    "PROCEEDING": 43,
}

# The reverse-engineered digest is a dated 27-August control and must retain
# its exact source/static denominator.  The canonical registry is additive and
# has since gained the La Laguna judicial perimeter plus this DP 748 source
# control; validate that current denominator independently.
CURRENT_CANONICAL_IDENTITY_COUNTS = {
    "total": 341,
    "PERSON": 162,
    "ORGANISATION": 83,
    "STRUCTURE": 11,
    "INSTITUTION": 42,
    "PROCEEDING": 43,
}

LAST_LIVE_IDENTITY_COUNTS = {
    "total": 204,
    "PERSON": 87,
    "ORGANISATION": 71,
    "STRUCTURE": 10,
    "INSTITUTION": 18,
    "PROCEEDING": 18,
}

HISTORICAL_LIVE_IDENTITY = {
    "total": 194,
    "PERSON": 86,
    "ORGANISATION": 66,
    "STRUCTURE": 10,
    "INSTITUTION": 15,
    "PROCEEDING": 17,
}

ALBERTO_LIFECYCLE = (
    "DRAFT",
    "PREPARED_PENDING_MERGE",
    "REMOTE_SOURCE",
    "PR_OPEN",
    "CI_GREEN",
    "MERGED",
    "DEPLOYED",
    "LIVE_VERIFIED",
    "DELETION_SAFE",
)
ALBERTO_BLOCKED_LIFECYCLE = "BLOCKED_RECOVERY"
ALBERTO_STATUS_BY_STATE = {
    "DRAFT": "not_live",
    "PREPARED_PENDING_MERGE": "release_candidate_not_yet_verified_live",
    "REMOTE_SOURCE": "remote_source_not_merged",
    "PR_OPEN": "pull_request_open_not_merged",
    "CI_GREEN": "pull_request_checks_green_not_merged",
    "MERGED": "merged_awaiting_pages_deployment",
    "DEPLOYED": "deployed_awaiting_exact_live_closeout",
    "LIVE_VERIFIED": "live_verified",
    "DELETION_SAFE": "deletion_safe_live_verified",
    ALBERTO_BLOCKED_LIFECYCLE: "blocked_recovery",
}


def is_full_sha(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None

required_markers = [
    "PD-UNITARY-REDIGEST-20260827-01",
    "Sun Park was one economically integrated hotel platform",
    "PP 1041 is the cleanest finite production demand",
    "21 / 24 confirmed",
    "superseded",
    "33 pull requests",
    "required-status-check enforcement was off",
    "CEXP succession",
    "single-satisfaction credit ledger",
    "PD-ALV-MP357-MULTI-20260827-01",
    "31/31 unique identities",
    "61 confirmed, 69 pending",
    "assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json",
    "does not add to, subtract from or close",
    "assets/data/caepr-caret-unitary-digest-v1.json",
    "publication-manifests/alberto-meeting-point-multidirectional-criminal-first-20260827.json",
    "PD-FTI-MP-RICPE-CONTINUITY-20260827-01",
    "39/65 confirmed",
    "43/101 confirmed",
    "31 actions, 12 package definitions",
    "3 heritage scopes, 11 known entity",
    "DELETION_SAFE",
    "Ithikios /",
    "DIGITAL PRODUCTS DEVELOPMENT SL",
    "ops/FTI_MEETING_POINT_CANARY_SPAIN_ASSET_TRANSACTION_MONITOR_CONTROL_27AUG2026.json",
    "Repository and website publication authority does not authorise email",
    "RedSARA/AGE or other notice",
]

text = MD.read_text(encoding="utf-8")
missing = [marker for marker in required_markers if marker not in text]
if missing:
    raise SystemExit(f"Missing digest markers: {missing}")

state = json.loads(STATE.read_text(encoding="utf-8"))
historical_manifest = json.loads(HISTORICAL_MANIFEST.read_text(encoding="utf-8"))
alberto_manifest = json.loads(ALBERTO_MANIFEST.read_text(encoding="utf-8"))
fti_manifest = json.loads(FTI_MANIFEST.read_text(encoding="utf-8"))
closeout = CLOSEOUT.read_text(encoding="utf-8")
matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
specialist_caret = json.loads(SPECIALIST_CARET.read_text(encoding="utf-8"))
first_hop_caret = json.loads(FIRST_HOP_CARET.read_text(encoding="utf-8"))
fti_continuity_caret = json.loads(FTI_CONTINUITY_CARET.read_text(encoding="utf-8"))
fti_professional_caret = json.loads(FTI_PROFESSIONAL_CARET.read_text(encoding="utf-8"))
fti_actions = json.loads(FTI_ACTIONS.read_text(encoding="utf-8"))
fti_monitor = json.loads(FTI_MONITOR.read_text(encoding="utf-8"))
fti_monitor_register = json.loads(FTI_MONITOR_REGISTER.read_text(encoding="utf-8"))
current_unitary_state = json.loads(CURRENT_UNITARY_STATE.read_text(encoding="utf-8"))
unitary_caret = json.loads(UNITARY_CARET.read_text(encoding="utf-8"))
registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

assert state["control_id"] == "PD-UNITARY-REDIGEST-20260827-01"
assert state["status"] in {
    "REPOSITORY_CONTROLLED_PUBLIC_SAFE",
    "LIVE_VERIFIED_PUBLIC_CONTROL",
}
assert state["source_base"]["main_sha"] == "8e8e83c5a337846245a942222efbc3120645b1fd"
for key, value in DIGEST_SNAPSHOT_IDENTITY_COUNTS.items():
    assert state["identity_registry"][key] == value
assert state["identity_registry"]["archive_backfill"] == "OPEN"
assert state["identity_registry"]["last_live_verified_counts"] == LAST_LIVE_IDENTITY_COUNTS
assert registry["counts"] == CURRENT_CANONICAL_IDENTITY_COUNTS
assert state["caret_scope"]["control_id"] == unitary_caret["control_id"]
assert state["caret_scope"]["control_file"] == "assets/data/caepr-caret-unitary-digest-v1.json"
assert state["caret_scope"]["confirmed"] == 21
assert state["caret_scope"]["denominator"] == 24
assert state["caret_scope"]["pending"] == 3
assert unitary_caret["result"]["confirmed"] == state["caret_scope"]["confirmed"]
assert unitary_caret["result"]["denominator"] == state["caret_scope"]["denominator"]
assert unitary_caret["result"]["pending"] == state["caret_scope"]["pending"]
assert unitary_caret["result"]["suspended"] == 0
assert unitary_caret["result"]["verdict"] == "PARTIAL_NOT_ALL_IS_CARET"
assert len(unitary_caret["confirmed_objects"]) == 21
assert len(unitary_caret["exceptions"]) == 3
assert {item["id"] for item in unitary_caret["confirmed_objects"]} >= {"PD-SP-O-0003", "PD-SP-O-0075"}
assert "PD-SP-O-0033" not in {item["id"] for item in unitary_caret["confirmed_objects"]}
assert any(
    item.get("existing_id") == "PD-SP-O-0033" and item.get("state") == "CARET_PENDING"
    for item in unitary_caret["exceptions"]
)
assert current_unitary_state["identity_registry"]["separate_caret_scopes"]["unitary"] == {
    "confirmed": 21,
    "pending": 3,
    "denominator": 24,
}
assert state["caret_scope"]["old_local_24_of_24_package"] == "SUPERSEDED_NOT_MERGEABLE_AS_IS"
assert state["source_base"]["open_pull_requests"] == 33
assert state["source_base"]["required_status_check_enforcement"] == "off"

# The exhaustive specialist census remains separate from, and may not mutate,
# the independently controlled repository-wide current 21/24 unitary census.
modules = {item["module_id"]: item for item in state["specialist_modules"]}

# The 27-August FTI / Meeting Point / RICPE release is additive. It must remain
# restartable without changing the historical source-base snapshot or opening
# any email, filing, notice or authority-contact channel.
fti = modules["PD-FTI-MP-RICPE-CONTINUITY-20260827-01"]
assert fti["module_relation"] == "ADDITIVE_SPECIALIST_RELEASE_DOES_NOT_REWRITE_HISTORICAL_SOURCE_BASE"
assert fti["analysis_order"][0] == "CRIMINAL_FIRST"
assert fti["digest"] == "archive/FTI_MEETING_POINT_RICPE_UNITARY_CRIMINAL_FIRST_DIGEST_27AUG2026.md"
assert fti["action_register"] == "ops/FTI_MEETING_POINT_RICPE_CROSSBORDER_ACTION_REGISTER_27AUG2026.json"
assert fti["deletion_audit"] == "docs/deletion-audits/2026-08-27-fti-meeting-point-ricpe-continuity-thread.md"
assert fti["publication_manifest"] == "publication-manifests/fti-meeting-point-ricpe-continuity-20260827.json"
for relative_path in (
    fti["digest"],
    fti["action_register"],
    fti["deletion_audit"],
    fti["publication_manifest"],
    fti["caret_controls"]["continuity_spine"]["control_file"],
    fti["caret_controls"]["professional_institutional"]["control_file"],
    fti["asset_transaction_monitor"]["control"],
    fti["asset_transaction_monitor"]["register"],
    fti["asset_transaction_monitor"]["schema"],
    fti["asset_transaction_monitor"]["script"],
    fti["asset_transaction_monitor"]["workflow"],
    fti["judicial_title_control"]["control"],
):
    assert (ROOT / relative_path).exists(), relative_path

expected_fti_continuity_scope = {
    "confirmed": 39,
    "pending": 26,
    "suspended": 0,
    "denominator": 65,
    "verdict": "FULL_FINITE_CONTINUITY_SPINE_CENSUS_PARTIAL_NOT_ALL_IS",
}
expected_fti_professional_scope = {
    "confirmed": 43,
    "pending": 58,
    "suspended": 0,
    "denominator": 101,
    "verdict": "FULL_ROLE_SELECTED_CENSUS_PARTIAL_NOT_ALL_IS",
}
assert {
    key: fti["caret_controls"]["continuity_spine"][key]
    for key in expected_fti_continuity_scope
} == expected_fti_continuity_scope
assert {
    key: fti["caret_controls"]["professional_institutional"][key]
    for key in expected_fti_professional_scope
} == expected_fti_professional_scope
assert fti["caret_controls"]["identity_only"] is True
assert fti["caret_controls"]["scopes_remain_separate"] is True
assert fti_continuity_caret["control_id"] == "PD-FTI-MP-RICPE-CARET-20260827-01"
assert fti_continuity_caret["counts"]["confirmed"] == 39
assert fti_continuity_caret["counts"]["eligible"] == 65
assert fti_continuity_caret["counts"]["pending"] == 26
assert fti_continuity_caret["counts"]["suspended"] == 0
assert len(fti_continuity_caret["records"]) == 65
assert fti_professional_caret["control_id"] == "PD-FTI-MP-PROF-INST-CARET-20260827-01"
assert fti_professional_caret["counts"]["confirmed"] == 43
assert fti_professional_caret["counts"]["eligible"] == 101
assert fti_professional_caret["counts"]["pending"] == 58
assert fti_professional_caret["counts"]["suspended"] == 0
assert len(fti_professional_caret["records"]) == 101

expected_action_state = {
    "actions": 31,
    "package_definitions": 12,
    "mapped_proceeding_files": 18,
    "external_action_authorized": False,
}
assert fti["action_state"] == expected_action_state
assert fti_actions["control_id"] == "PD-FTI-MP-RICPE-ACTIONS-20260827-01"
assert len(fti_actions["actions"]) == 31
assert len(fti_actions["package_definitions"]) == 12
assert len(fti_actions["proceeding_file_mapping"]) == 18
assert fti_actions["external_action_authorized"] is False

expected_monitor_counts = {
    "heritage_scopes": 3,
    "entity_objects": 11,
    "automated_safe_public_sources": 12,
    "baseline_events": 2,
    "open_gaps": 8,
}
for key, expected in expected_monitor_counts.items():
    assert fti["asset_transaction_monitor"][key] == expected
assert fti["asset_transaction_monitor"]["coverage"] == "BOUNDED_MONITOR_NOT_COMPREHENSIVE"
assert fti["asset_transaction_monitor"]["automatic_public_promotion"] is False
assert fti_monitor["control_id"] == "PD-FTI-MP-ASSET-TX-MONITOR-20260827-01"
assert fti_monitor["coverage_boundary"]["configured_heritage_scopes"] == 3
assert fti_monitor["coverage_boundary"]["configured_public_sources"] == 12
assert fti_monitor["coverage_boundary"]["configured_open_gaps"] == 8
assert fti_monitor["external_action_authorized"] is False
assert len(fti_monitor_register["heritage_scopes"]) == 3
assert len(fti_monitor_register["known_entities"]) == 11
assert len(fti_monitor_register["sources"]) == 12
assert len(fti_monitor_register["events"]) == 2
assert len(fti_monitor_register["coverage_gaps"]) == 8

historical_title = "el Ilmo. Sr. D. Alberto López Villarrubia, Magistrado-Juez del entonces Juzgado de lo Mercantil n.º 1 de Las Palmas de Gran Canaria"
current_title = "el magistrado D. Alberto López Villarrubia, titular de la plaza n.º 1 de la Sección de lo Mercantil del Tribunal de Instancia de Las Palmas de Gran Canaria"
assert fti["judicial_title_control"]["historical_own_court_reference"] == historical_title
assert fti["judicial_title_control"]["current_reference"] == current_title
for open_question in ("signature", "substitution or allocation", "capacity", "knowledge", "conflict", "disclosure"):
    assert open_question in fti["judicial_title_control"]["former_court_3_boundary"]
assert fti["ricpe_resolver_boundary"]["named_individual_resolver"] is False
assert fti["ricpe_resolver_boundary"]["provider_perimeter"] == "Ithikios / DIGITAL PRODUCTS DEVELOPMENT SL"
for authority_key, expected in {
    "repository_and_website_publication_authorized": True,
    "email_authorized": False,
    "filing_authorized": False,
    "notice_authorized": False,
    "portal_submission_authorized": False,
    "authority_contact_authorized": False,
}.items():
    assert fti["external_action_authority"][authority_key] is expected

assert fti_manifest["control_id"] == fti["module_id"]
assert fti_manifest["current_state"] in {"LIVE_VERIFIED", "DELETION_SAFE"}
assert fti["publication_state"] == fti_manifest["current_state"]
assert fti_manifest["publication_authorized"] is True
assert fti_manifest["communication_authorized"] is False
assert fti_manifest["email_or_filing_action"] == "HOLD_NOT_AUTHORISED"
assert fti_manifest["publication_authorization"]["repository_and_website_only"] is True
assert fti_manifest["publication_authorization"]["email_authorized"] is False
assert fti_manifest["publication_authorization"]["filing_authorized"] is False
assert is_full_sha(fti_manifest.get("merge_sha"))
assert fti_manifest["deployment_evidence"]["workflow"] == "pages build and deployment"
assert fti_manifest["deployment_evidence"]["conclusion"] == "success"
assert fti_manifest["deployment_evidence"]["head_sha"] == fti_manifest["merge_sha"]
assert fti_manifest["live_readback"]["result"] == "PASS_EXACT_BYTES"
assert fti_manifest["live_readback"]["head_sha"] == fti_manifest["merge_sha"]
assert len(fti_manifest["live_readback"]["sha256_by_route"]) == 34
fti_closeout = fti_manifest["closeout_control"]
assert fti_closeout["kind"] == "SEPARATE_WORKFLOW_ARTIFACT"
assert fti_closeout["result"] == "LIVE_VERIFIED"
assert fti_closeout["head_sha"] == fti_manifest["merge_sha"]
assert fti_closeout["workflow_run_id"] == 33083264897
assert fti_closeout["artifact_id"] == 9651057259
for key in (
    "communication_authorized",
    "email_authorized",
    "filing_authorized",
    "red_sara_age_notification_authorized",
    "portal_submission_authorized",
    "authority_contact_authorized",
):
    assert fti_closeout[key] is False
assert fti_manifest["caret_scope"] == {
    "control_id": "PD-FTI-MP-RICPE-CARET-20260827-01",
    **expected_fti_continuity_scope,
    "identity_only": True,
    "separate_from": [
        "31/31 unique and 32/32 occurrence-row specialist all-is scope",
        "61/130 first-hop",
        "21/24 repository-wide unitary",
    ],
}
assert {
    key: fti_manifest["professional_institutional_caret_scope"][key]
    for key in ("confirmed", "pending", "suspended", "denominator", "verdict")
} == expected_fti_professional_scope
assert fti_manifest["action_register"] == expected_action_state

unitary_candidates = {
    item["control_id"]: item
    for item in current_unitary_state["specialist_continuity_candidates"]
}
unitary_fti = unitary_candidates[fti["module_id"]]
assert unitary_fti["state"] == fti["publication_state"]
assert unitary_fti["restart_controls"]["digest"] == fti["digest"]
assert unitary_fti["restart_controls"]["action_register"] == fti["action_register"]
assert unitary_fti["restart_controls"]["deletion_audit"] == fti["deletion_audit"]
assert unitary_fti["restart_controls"]["publication_manifest"] == fti["publication_manifest"]
assert unitary_fti["caret_scopes"]["continuity_spine"] == {
    "confirmed": 39, "pending": 26, "suspended": 0, "denominator": 65
}
assert unitary_fti["caret_scopes"]["professional_institutional"] == {
    "confirmed": 43, "pending": 58, "suspended": 0, "denominator": 101
}
assert unitary_fti["action_state"] == expected_action_state
for key, expected in expected_monitor_counts.items():
    assert unitary_fti["asset_transaction_monitor"][key] == expected
assert unitary_fti["judicial_title_rule"]["historical_own_court_reference"] == historical_title
assert unitary_fti["judicial_title_rule"]["current_reference"] == current_title
assert unitary_fti["authorization_boundary"] == fti["external_action_authority"]

additive = state["additive_publication_evidence"]
assert additive["relation_to_source_base"] == "ADDITIVE_RELEASE_DOES_NOT_REWRITE_HISTORICAL_SOURCE_BASE"
assert additive["pull_request"] == 1111
assert additive["validated_pr_head"] == "677906e303ad91cc436803d8d47e410deefbbd6f"
assert additive["merge_sha"] == "41a8250ffdcd27e820bbc89b8238fb98ba23a6db"
assert additive["merge_tree_sha"] == "0f2b75347de048d449160a69d087b592bd51b35c"
assert additive["pages"] == {
    "run_id": 33083261099,
    "run_number": 1184,
    "status": "completed",
    "conclusion": "success",
}
assert additive["current_digest_closeout"]["workflow_run_id"] == 33083264830
assert additive["current_digest_closeout"]["artifact_id"] == 9651039104
assert additive["current_digest_closeout"]["exact_route_count"] == 43
assert additive["current_digest_closeout"]["identity_registry_parity"] == 204
assert additive["fti_live_closeout"]["workflow_run_id"] == 33083264897
assert additive["fti_live_closeout"]["artifact_id"] == 9651057259
assert additive["asset_transaction_monitor"]["workflow_run_id"] == 33083264530
assert additive["asset_transaction_monitor"]["artifact_id"] == 9651009448
assert additive["asset_transaction_monitor"]["sources_fetched"] == 12
assert additive["asset_transaction_monitor"]["fetch_errors"] == 0
assert additive["asset_transaction_monitor"]["review_signals"] == 0
assert all(value is False for value in additive["external_action_authority"].values())

specialist = modules["PD-ALV-MP357-MULTI-20260827-01"]
assert specialist["caret_scope"] == {
    "confirmed": 31,
    "pending": 0,
    "suspended": 0,
    "denominator": 31,
    "occurrence_rows": 32,
    "confirmed_occurrence_rows": 32,
    "verdict": "ALL_IS_VERIFIED_FOR_STATED_SCOPE",
}
assert specialist["unitary_caret_scope_unchanged"] is False
assert specialist["caret_control"] == "assets/data/caepr-caret-alberto-meeting-point-357-v1.json"
assert specialist["first_hop_caret_control"] == "assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json"
assert specialist["first_hop_caret_scope"] == {
    "confirmed": 61,
    "pending": 69,
    "suspended": 0,
    "denominator": 130,
    "verdict": "FULL_FIRST_HOP_CENSUS_PARTIAL_NOT_ALL_IS",
}
assert specialist["publication_manifest"] == "publication-manifests/alberto-meeting-point-multidirectional-criminal-first-20260827.json"
assert matrix["control_id"] == specialist["module_id"]
assert matrix["scope_separation"]["unitary_caret_scope"] == {
    "control_id": "PD-UNITARY-REDIGEST-20260827-01",
    "confirmed": 21,
    "pending": 3,
    "denominator": 24,
    "changed_by_this_module": True,
}
assert matrix["scope_separation"]["specialist_caret_scope"] == {
    "control_id": "PD-ALV-MP357-CARET-20260827-01",
    "confirmed": 31,
    "pending": 0,
    "denominator": 31,
    "occurrence_rows": 32,
    "confirmed_occurrence_rows": 32,
    "verdict": "ALL_IS_VERIFIED_FOR_STATED_SCOPE",
}
assert matrix["scope_separation"]["first_hop_caret_scope"] == {
    "control_id": "PD-ALV-MP357-FIRST-HOP-CARET-20260827-01",
    "confirmed": 61,
    "pending": 69,
    "denominator": 130,
    "verdict": "FULL_FIRST_HOP_CENSUS_PARTIAL_NOT_ALL_IS",
    "changed_by_this_module": True,
}
assert specialist_caret["control_id"] == "PD-ALV-MP357-CARET-20260827-01"
assert specialist_caret["counts"]["confirmed"] == 31
assert specialist_caret["counts"]["eligible"] == 31
assert specialist_caret["counts"]["confirmed_occurrence_rows"] == 32
assert specialist_caret["counts"]["pending"] == 0
assert specialist_caret["counts"]["suspended"] == 0
assert len(specialist_caret["records"]) == 32
assert sum(record["state"] == "CARET_CONFIRMED" for record in specialist_caret["records"]) == 32
assert sum(record["state"] == "CARET_PENDING" for record in specialist_caret["records"]) == 0
assert specialist_caret["verdict"] == "ALL IS^ — VERIFIED FOR THE STATED SIX-SURFACE SCOPE; 31/31 UNIQUE IDENTITIES AND 32/32 OCCURRENCE ROWS CARET_CONFIRMED; 0 PENDING"
assert first_hop_caret["control_id"] == "PD-ALV-MP357-FIRST-HOP-CARET-20260827-01"
assert first_hop_caret["counts"]["eligible"] == 130
assert first_hop_caret["counts"]["confirmed"] == 61
assert first_hop_caret["counts"]["pending"] == 69
assert first_hop_caret["counts"]["suspended"] == 0
assert len(first_hop_caret["records"]) == 130
assert sum(record["state"] == "CARET_CONFIRMED" for record in first_hop_caret["records"]) == 61
assert sum(record["state"] == "CARET_PENDING" for record in first_hop_caret["records"]) == 69
assert all(record.get("next_source_needed") for record in first_hop_caret["records"] if record["state"] == "CARET_PENDING")
assert first_hop_caret["verdict"] == "FULL FIRST-HOP CENSUS COMPLETE; 61/130 CARET_CONFIRMED; 69 CARET_PENDING; 0 CARET_SUSPENDED; PARTIAL — NOT ALL IS^"

# Bind the separate Magistrate López Villarrubia candidate without treating a
# locally valid DRAFT or an authorised pre-live release state as LIVE_VERIFIED,
# and without changing the immutable historical unitary snapshot below.
assert alberto_manifest["publication_id"] == "alberto-meeting-point-multidirectional-criminal-first-20260827"
assert alberto_manifest["control_id"] == specialist["module_id"]
alberto_lifecycle = alberto_manifest["current_state"]
assert alberto_lifecycle in set(ALBERTO_LIFECYCLE) | {ALBERTO_BLOCKED_LIFECYCLE}
expected_specialist_publication_state = (
    "DRAFT_CANDIDATE_NOT_LIVE_NOT_AUTHORISED"
    if alberto_lifecycle == "DRAFT"
    else alberto_lifecycle
)
assert specialist["publication_state"] == expected_specialist_publication_state
assert alberto_manifest["status"] == ALBERTO_STATUS_BY_STATE[alberto_lifecycle]
alberto_rank = ALBERTO_LIFECYCLE.index(alberto_lifecycle) if alberto_lifecycle in ALBERTO_LIFECYCLE else -1
if alberto_lifecycle in {"DRAFT", ALBERTO_BLOCKED_LIFECYCLE}:
    assert alberto_manifest["publication_authorized"] is False
    assert not alberto_manifest.get("publication_authorization")
else:
    assert alberto_manifest["publication_authorized"] is True
    authorization = alberto_manifest.get("publication_authorization") or {}
    assert isinstance(authorization, dict)
    assert authorization.get("scope_control_id") == specialist["module_id"]
    assert authorization.get("repository_and_website_only") is True
    assert authorization.get("email_authorized") is False
    assert authorization.get("filing_authorized") is False
    assert authorization.get("user_instruction")
    assert authorization.get("recorded_at")
assert alberto_manifest["communication_authorized"] is False
assert alberto_manifest["email_or_filing_action"] == "HOLD_NOT_AUTHORISED"
if alberto_lifecycle == "DRAFT":
    assert alberto_manifest.get("validation", {}).get("live_readback") == "not_run_not_authorised"
    for forbidden_key in ("merge_sha", "deployment_evidence", "live_urls", "live_readback", "closeout_control"):
        assert not alberto_manifest.get(forbidden_key)
if alberto_rank >= ALBERTO_LIFECYCLE.index("MERGED"):
    assert is_full_sha(alberto_manifest.get("merge_sha"))
if alberto_rank >= ALBERTO_LIFECYCLE.index("DEPLOYED"):
    deployment = alberto_manifest.get("deployment_evidence") or {}
    assert deployment.get("workflow") == "pages build and deployment"
    assert deployment.get("conclusion") == "success"
    assert isinstance(deployment.get("run_id"), int) and deployment["run_id"] > 0
    assert deployment.get("head_sha") == alberto_manifest.get("merge_sha")
if alberto_rank >= ALBERTO_LIFECYCLE.index("LIVE_VERIFIED"):
    readback = alberto_manifest.get("live_readback") or {}
    assert readback.get("result") == "PASS_EXACT_BYTES"
    assert readback.get("head_sha") == alberto_manifest.get("merge_sha")
    assert isinstance(readback.get("workflow_run_id"), int) and readback["workflow_run_id"] > 0
    hashes = readback.get("sha256_by_route") or {}
    assert isinstance(hashes, dict) and len(hashes) >= 37
    assert all(isinstance(route, str) and route.startswith("/") for route in hashes)
    assert all(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest) for digest in hashes.values())
    closeout_control = alberto_manifest.get("closeout_control") or {}
    assert closeout_control.get("kind") == "SEPARATE_WORKFLOW_ARTIFACT"
    assert closeout_control.get("result") == "LIVE_VERIFIED"
    assert closeout_control.get("head_sha") == alberto_manifest.get("merge_sha")
    assert isinstance(closeout_control.get("workflow_run_id"), int) and closeout_control["workflow_run_id"] > 0
    assert isinstance(closeout_control.get("artifact_id"), int) and closeout_control["artifact_id"] > 0
    assert closeout_control.get("artifact_name")
    assert closeout_control.get("communication_authorized") is False
    assert closeout_control.get("filing_authorized") is False
if alberto_lifecycle == "DELETION_SAFE":
    assert alberto_manifest.get("deletion_audit")
if os.environ.get("GITHUB_ACTIONS") == "true" and os.environ.get("GITHUB_EVENT_NAME") in {"pull_request", "push"}:
    assert alberto_lifecycle not in {"DRAFT", ALBERTO_BLOCKED_LIFECYCLE}
assert alberto_manifest["unitary_caret_scope"] == matrix["scope_separation"]["unitary_caret_scope"]
assert alberto_manifest["specialist_caret_scope"] == {
    "control_id": "PD-ALV-MP357-CARET-20260827-01",
    "confirmed": 31,
    "pending": 0,
    "suspended": 0,
    "denominator": 31,
    "occurrence_rows": 32,
    "confirmed_occurrence_rows": 32,
    "verdict": "ALL_IS_VERIFIED_FOR_STATED_SCOPE",
    "identity_only": True,
}
assert alberto_manifest["first_hop_caret_scope"] == {
    "control_id": "PD-ALV-MP357-FIRST-HOP-CARET-20260827-01",
    "confirmed": 61,
    "pending": 69,
    "suspended": 0,
    "denominator": 130,
    "verdict": "FULL_FIRST_HOP_CENSUS_PARTIAL_NOT_ALL_IS",
    "identity_only": True,
}
assert str(STATE.relative_to(ROOT)) in alberto_manifest["expected_source_files"]
assert str(MD.relative_to(ROOT)) in alberto_manifest["expected_source_files"]
assert specialist["machine_matrix"] in alberto_manifest["expected_source_files"]
assert specialist["caret_control"] in alberto_manifest["expected_source_files"]
assert specialist["first_hop_caret_control"] in alberto_manifest["expected_source_files"]

assert historical_manifest["publication_id"] == "unitary-repository-website-redigest-20260827"
assert historical_manifest["control_id"] == state["control_id"]
assert historical_manifest["current_state"] in {
    "PR_OPEN",
    "CI_GREEN",
    "MERGED",
    "DEPLOYED",
    "LIVE_VERIFIED",
}
assert historical_manifest["expected_routes"] == {"es": [], "en": []}
assert historical_manifest["reader_facing_material_update"] is False
assert historical_manifest["material_date_change"] is False
# PR #1091's manifest is a historical live snapshot. It must not be rewritten
# to imply that its earlier deployment verified the new 204-record candidate.
assert historical_manifest["identity_registry"] == {**HISTORICAL_LIVE_IDENTITY, "archive_backfill": "OPEN"}
for key in ("current_live_state", "denominator", "old_local_24_of_24_package"):
    assert historical_manifest["caret_scope"][key] == state["caret_scope"][key]
assert len(historical_manifest["live_urls"]) == 3

if historical_manifest["current_state"] == "LIVE_VERIFIED":
    assert state["status"] == "LIVE_VERIFIED_PUBLIC_CONTROL"
    assert historical_manifest["merge_sha"] == "0367a3759cf372bce35a3f2c292092e2f06cad25"
    assert historical_manifest["deployment_evidence"]["conclusion"] == "success"
    assert historical_manifest["live_verification_evidence"]["conclusion"] == "success"
    assert historical_manifest["live_verification_evidence"]["verified_url_count"] == 3
    assert historical_manifest["preservation_evidence"]["tree_matches_merge_tree"] is True
    assert historical_manifest["preservation_evidence"]["artifact_sha256"] == "a65e812d5ffdc36f41dcaee5297a86d02cd12004759d89815c5c0c0f406028a3"
    for marker in [
        "LIVE_VERIFIED_PUBLIC_CONTROL",
        "0367a3759cf372bce35a3f2c292092e2f06cad25",
        "a65e812d5ffdc36f41dcaee5297a86d02cd12004759d89815c5c0c0f406028a3",
        "MERGED → PAGES DEPLOYED → EXACT PUBLIC READBACK PASSED",
    ]:
        assert marker in closeout, marker

print("CURRENT REVERSE-ENGINEERED DIGEST: PASS")
print(" - control:", state["control_id"])
print(" - source base:", state["source_base"]["main_sha"])
print(" - dated digest identity denominator: 336 / 157 / 83 / 11 / 42 / 43")
print(" - current canonical identity denominator: 341 / 162 / 83 / 11 / 42 / 43")
print(" - current live-verified identity snapshot: 204 / 87 / 71 / 10 / 18 / 18")
print(" - caret scope: 21/24; 3 pending; old 24/24 package superseded")
print(" - separate Magistrate López Villarrubia / Meeting Point scope: 31/31 unique and 32/32 rows; all-is for stated scope")
print(" - first-hop Magistrate López Villarrubia / Meeting Point evidence corpus: 61/130 partial")
print(" - Magistrate López Villarrubia publication:", alberto_lifecycle, "/ lifecycle-controlled; communication and filing remain closed")
print(" - FTI / Meeting Point / RICPE live continuity: 39/65 partial; professional/institutional scope: 43/101 partial")
print(" - FTI future-action state: 31 actions / 12 packages / 18 proceeding-file mappings; external action closed")
print(" - FTI bounded asset monitor: 3 heritage scopes / 11 entities / 12 sources / 2 baseline events / 8 gaps")
print(" - historical unitary lifecycle:", historical_manifest["current_state"])
print(" - public material date intentionally unchanged")

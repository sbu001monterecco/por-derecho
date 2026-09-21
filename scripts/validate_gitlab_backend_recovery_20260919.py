#!/usr/bin/env python3
"""Validate the public-safe GitLab backend recovery ledger."""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER = ROOT / "ops" / "continuity" / "GITLAB_BACKEND_RECOVERY_LEDGER_20260919.json"

ALLOWED = {
    "EXACT_GITLAB_RECOVERY",
    "EXACT_ALREADY_MIRRORED",
    "FUNCTIONAL_GITHUB_EQUIVALENT",
    "PENDING_GITLAB_RESTORATION",
}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_PUBLIC_KEYS = {
    "token",
    "password",
    "key_base64",
    "credential",
    "drive_folder_id",
    "drive_parent_folder_id",
    "gmail_message_id",
    "support_ticket",
}


def _walk_keys(value, path="root"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield path, str(key)
            yield from _walk_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_keys(child, f"{path}[{index}]")


def validate() -> list[str]:
    failures: list[str] = []
    data = json.loads(LEDGER.read_text(encoding="utf-8"))

    if data.get("schema") != "por-derecho.gitlab-backend-recovery-ledger.v1":
        failures.append("schema_mismatch")
    if data.get("status") != "RECOVERY_EVIDENCE_ESTABLISHED_GITLAB_AUTH_STILL_BLOCKED":
        failures.append("status_mismatch")
    if data.get("authenticated_gitlab_restoration_verified") is not False:
        failures.append("authenticated_gitlab_restoration_must_remain_false")

    project = data.get("project") or {}
    if project.get("id") != 86151898:
        failures.append("project_id_mismatch")
    if project.get("path") != "por-derecho/por-derecho-setup-or-gitlab-setup":
        failures.append("project_path_mismatch")
    if not SHA40.fullmatch(project.get("last_verified_gitlab_main_sha", "")):
        failures.append("last_verified_gitlab_main_sha_invalid")
    elif project["last_verified_gitlab_main_sha"] != "7d086d098676eecc2c1647ed09b348d8dc0bdc69":
        failures.append("last_verified_gitlab_main_sha_drift")

    if set(data.get("recovery_classes", [])) != ALLOWED:
        failures.append("recovery_class_enum_drift")

    recovered = data.get("verified_off_platform_recovery") or {}
    bundle = recovered.get("reconstructed_git_bundle") or {}
    expected_bundle = {
        "bytes": 154913687,
        "sha256": "fd343b972b83bb9a57da8d8b3ce4b216abb2093ddb8da1f5e4efc538fe1a897a",
        "candidate_commit": "2e7c78b47c8064cd9b02f3abde5036679e691074",
        "candidate_tree": "81541762b01df1eaf94e7bf1293c725bd849d43a",
    }
    for key, expected in expected_bundle.items():
        if bundle.get(key) != expected:
            failures.append(f"bundle_{key}_mismatch")
    if bundle.get("git_bundle_verify") != "PASS":
        failures.append("bundle_verify_not_pass")
    if bundle.get("is_original_final_gitlab_tree") is not False:
        failures.append("bundle_improper_final_tree_claim")
    if bundle.get("public_release_approved") is not False:
        failures.append("bundle_improper_public_release_claim")
    if not SHA256.fullmatch(bundle.get("sha256", "")):
        failures.append("bundle_sha256_invalid")

    corpus = recovered.get("rehydrated_source_corpus") or {}
    expected_corpus = {
        "bytes": 394817347,
        "sha256": "3497c6904e1bb0018373ee757076b0c7077d943bc3fa9116e0f8bcfa64d052da",
        "object_files_verified": 3851,
        "unique_sha256": 3850,
        "path_version_rows_verified": 2540,
        "candidate_paths": 1857,
        "conflicting_paths_requiring_reconciliation": 575,
    }
    for key, expected in expected_corpus.items():
        if corpus.get(key) != expected:
            failures.append(f"corpus_{key}_mismatch")
    if corpus.get("is_final_original_site_certified") is not False:
        failures.append("corpus_improper_final_site_claim")
    if corpus.get("public_release_approved") is not False:
        failures.append("corpus_improper_public_release_claim")

    anchors = data.get("gitlab_chronology_anchors") or []
    if not anchors:
        failures.append("chronology_empty")
    seen_commits: set[str] = set()
    for item in anchors:
        commit = item.get("commit", "")
        if not SHA40.fullmatch(commit):
            failures.append(f"chronology_commit_invalid:{commit}")
        if commit in seen_commits:
            failures.append(f"chronology_commit_duplicate:{commit}")
        seen_commits.add(commit)
        if not item.get("provenance"):
            failures.append(f"chronology_provenance_missing:{commit}")
        if item.get("pipeline_status") not in {"PASS", "FAIL", "NOT_ASSERTED"}:
            failures.append(f"chronology_pipeline_status_invalid:{commit}")
    if anchors and anchors[-1].get("commit") != project.get("last_verified_gitlab_main_sha"):
        failures.append("chronology_last_anchor_not_last_verified_main")

    graph = data.get("notification_event_graph") or {}
    if graph.get("project_notifications_count") != 981:
        failures.append("notification_count_drift")
    if graph.get("distinct_merge_requests_observed") != 93:
        failures.append("mr_count_drift")
    if graph.get("distinct_work_items_observed") != 21:
        failures.append("work_item_count_drift")
    if graph.get("classification") != "FUNCTIONAL_GITHUB_EQUIVALENT":
        failures.append("event_graph_classification_invalid")
    if not graph.get("boundary"):
        failures.append("event_graph_boundary_missing")

    capabilities = {item.get("id"): item for item in data.get("capabilities", [])}
    required_caps = {
        "DUO_ORCHESTRATION_PROTOCOL",
        "DUO_EXECUTION_CONFIG",
        "FINAL_GITLAB_CI_CONFIG",
        "MR_WORK_ITEM_PIPELINE_EVENT_GRAPH",
        "GITLAB_NATIVE_PLATFORM_STATE",
    }
    if not required_caps.issubset(capabilities):
        failures.append("required_capability_missing")
    for ident, item in capabilities.items():
        if item.get("classification") not in ALLOWED:
            failures.append(f"invalid_capability_classification:{ident}")
        if not item.get("boundary"):
            failures.append(f"capability_boundary_missing:{ident}")

    protocol = capabilities.get("DUO_ORCHESTRATION_PROTOCOL") or {}
    if protocol.get("classification") != "EXACT_ALREADY_MIRRORED":
        failures.append("duo_protocol_not_exact_already_mirrored")
    protocol_path = ROOT / protocol.get("github_path", "")
    if not protocol_path.is_file():
        failures.append("duo_protocol_github_path_missing")

    for ident in ("DUO_EXECUTION_CONFIG", "FINAL_GITLAB_CI_CONFIG", "GITLAB_NATIVE_PLATFORM_STATE"):
        item = capabilities.get(ident) or {}
        if item.get("classification") != "PENDING_GITLAB_RESTORATION":
            failures.append(f"gitlab_native_item_not_pending:{ident}")

    pending_text = " ".join((capabilities.get("GITLAB_NATIVE_PLATFORM_STATE") or {}).get("components", [])).lower()
    for token in (
        "merge request discussions",
        "approvals",
        "pipeline/job logs",
        "variables",
        "runner",
        "environments",
        "settings",
        "duo sessions",
        "orbit/index",
        "tokens",
    ):
        if token not in pending_text:
            failures.append(f"pending_native_component_missing:{token}")

    rules = " ".join(data.get("reconciliation_policy", [])).lower()
    for token in (
        "never reconstruct unavailable exact gitlab bytes",
        "never publish the private recovery bundle",
        "historical recovery seed",
        "575 conflicting",
        "additively",
        "force-reset",
        "exact-head outage backend parity",
    ):
        if token not in rules:
            failures.append(f"reconciliation_rule_missing:{token}")

    safety = data.get("public_safety") or {}
    for key in (
        "contains_private_evidence",
        "contains_private_storage_locators",
        "contains_mailbox_message_ids",
        "contains_support_ticket_ids",
        "contains_credentials_or_secret_values",
    ):
        if safety.get(key) is not False:
            failures.append(f"public_safety_not_false:{key}")

    for path, key in _walk_keys(data):
        if key.lower() in FORBIDDEN_PUBLIC_KEYS:
            failures.append(f"forbidden_public_key:{path}.{key}")

    return failures


def main() -> int:
    failures = validate()
    report = {
        "schema": "por-derecho.gitlab-backend-recovery-validation.v1",
        "status": "PASS" if not failures else "FAIL",
        "ledger": str(LEDGER.relative_to(ROOT)),
        "failures": failures,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())

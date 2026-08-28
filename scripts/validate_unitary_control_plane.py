#!/usr/bin/env python3
"""Validate the synchronized Por Derecho specialist and operational control planes."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
EXPECTED = {
    "total": 214,
    "PERSON": 94,
    "ORGANISATION": 74,
    "STRUCTURE": 10,
    "INSTITUTION": 18,
    "PROCEEDING": 18,
}
LAST_LIVE_IDENTITY_COUNTS = {
    "total": 204,
    "PERSON": 87,
    "ORGANISATION": 71,
    "STRUCTURE": 10,
    "INSTITUTION": 18,
    "PROCEEDING": 18,
}
UNITARY_CONTROL_ID = "PD-UNITARY-STATE-20260826-01"
HISTORICAL_CONTROL_ID = "PD-UNITARY-STATE-20260825-01"
HISTORICAL_VERIFY_RUN = 32912919872
SOURCE_MAIN_26 = "5b1652e00151a3ea2944cd0519cdaf2e04da4453"
MERGE_SHA = "77e2ba300af45a953947160af63283a64512e876"
TREE_SHA = "4f0ac26c5548ae44c68933306c68165cbb6c973e"
PAGES_RUN_ID = 32942972472
PAGES_RUN_NUMBER = 1128
PAGES_COMPLETED_AT = "2026-08-26T07:29:45Z"
UNITARY_VERIFY_RUN = 32942975508
UNITARY_VERIFY_RUN_NUMBER = 4
UNITARY_VERIFY_JOB = 98097657687
UNITARY_VERIFY_COMPLETED_AT = "2026-08-26T07:29:55Z"


def load_json(path: Path):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AssertionError(f"cannot parse {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise AssertionError(f"{path.relative_to(ROOT)} root must be object")
    return value


def require(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


def require_markers(path: Path, markers: list[str], forbidden: list[str] | None = None):
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        require(marker in text, f"missing {marker!r} in {path.relative_to(ROOT)}")
    for marker in forbidden or []:
        require(marker not in text, f"stale marker {marker!r} in {path.relative_to(ROOT)}")
    return text


def main() -> int:
    try:
        index = load_json(DATA / "matter-identity-registry-v1.json")
        require(index.get("counts") == EXPECTED, f"unexpected identity counts: {index.get('counts')}")

        actual = {key: 0 for key in EXPECTED if key != "total"}
        ids: set[str] = set()
        for descriptor in index.get("parts", []):
            part = load_json(DATA / descriptor["path"])
            records = part.get("records", [])
            require(len(records) == descriptor["count"], f"part count mismatch: {descriptor['path']}")
            for record in records:
                rid = record.get("id")
                require(rid and rid not in ids, f"duplicate or empty ID: {rid}")
                ids.add(rid)
                actual[record["type"]] += 1
        require(len(ids) == EXPECTED["total"], "identity part total mismatch")
        for key in actual:
            require(actual[key] == EXPECTED[key], f"identity class mismatch {key}: {actual[key]}")

        es_identity = require_markers(
            ROOT / "es/registro-identidad-materia/index.html",
            [
                'content="Registro operativo de 214 IDs inmutables',
                'data-static-registry-counts="214-94-74-10-18-18"',
                'data-registry-stat="TOTAL">214',
                'data-registry-stat="PERSON">94',
                'data-registry-stat="ORGANISATION">74',
                '"name":"Total","value":214',
                '../../ops/CURRENT_UNITARY_STATE.json',
            ],
            ['Los 159 IDs', 'data-registry-stat="TOTAL">159', '159 identidades canónicas'],
        )
        en_identity = require_markers(
            ROOT / "en/matter-identity-registry/index.html",
            [
                'content="Operational Por Derecho register of 214 immutable IDs',
                'data-static-registry-counts="214-94-74-10-18-18"',
                'data-registry-stat="TOTAL">214',
                'data-registry-stat="PERSON">94',
                'data-registry-stat="ORGANISATION">74',
                '"name":"Total","value":214',
                '../../ops/CURRENT_UNITARY_STATE.json',
            ],
            ['The 159 IDs', 'data-registry-stat="TOTAL">159', '159 canonical identities'],
        )
        require(es_identity.count('data-registry-stat="') >= 6, "Spanish identity stat set incomplete")
        require(en_identity.count('data-registry-stat="') >= 6, "English identity stat set incomplete")

        updates = load_json(DATA / "material-updates-v1.json")
        require(updates.get("control_id") == "PD-MATERIAL-UPDATES-001", "unexpected material-updates control")
        require(updates.get("latest_material_date") == "2026-08-26", "latest material date mismatch")
        require(len(updates.get("entries", [])) >= 5, "material update source too small")
        require(
            all(item.get("date") <= updates["latest_material_date"] for item in updates["entries"]),
            "future update date present",
        )
        require_markers(
            ROOT / "es/actualizaciones/index.html",
            ["Última actualización material", "<strong>26 agosto 2026</strong>", "ALG-ENT-018"],
        )
        require_markers(
            ROOT / "en/updates/index.html",
            ["Latest material update", "<strong>26 August 2026</strong>", "ALG-ENT-018"],
        )

        state = load_json(ROOT / "ops/CURRENT_UNITARY_STATE.json")
        require(state.get("schema") == "por-derecho.current-unitary-state.v1", "unexpected unitary schema")
        require(state.get("control_id") == UNITARY_CONTROL_ID, "unexpected unitary-state control")
        require(state.get("status") == "LIVE_VERIFIED", "unitary state is not live verified")
        require(
            re.fullmatch(r"[0-9a-f]{40}", state["repository"]["current_main_sha_at_preparation"]),
            "invalid preparation SHA",
        )
        require(state["identity_registry"]["counts"] == EXPECTED, "state identity counts drift")
        require(
            state["identity_registry"]["last_live_verified_counts"]
            == LAST_LIVE_IDENTITY_COUNTS,
            "state last-live identity counts drift",
        )
        require(
            state["material_updates"]["repository_latest_material_date"] == updates["latest_material_date"],
            "state/update date drift",
        )
        require(state["material_updates"]["latest_material_date"] == "2026-08-26", "compatibility material date drift")
        require(
            state["material_updates"]["last_live_verified_material_date"] == "2026-08-26",
            "last live-verified material date drift",
        )
        require(
            state["material_updates"]["public_parity"] == "2026-08-26_LIVE_VERIFIED",
            "repository/live material parity boundary drift",
        )
        repository = state.get("repository") or {}
        require(repository.get("current_main_sha_at_preparation") == MERGE_SHA, "unitary merge SHA drift")
        require(repository.get("source_publication_merge_sha") == MERGE_SHA, "publication merge SHA drift")
        require(repository.get("verified_tree_sha") == TREE_SHA, "unitary tree SHA drift")
        promoted = state.get("promoted_material_publication") or {}
        require(promoted.get("control_id") == UNITARY_CONTROL_ID, "promoted 26-Aug control missing")
        require(promoted.get("state") == "LIVE_VERIFIED", "promoted 26-Aug state is not live verified")
        require(promoted.get("source_main_sha") == SOURCE_MAIN_26, "promoted 26-Aug source-main drift")
        require(promoted.get("publication_merge_sha") == MERGE_SHA, "promoted 26-Aug merge drift")
        require(promoted.get("publication_tree_sha") == TREE_SHA, "promoted 26-Aug tree drift")
        require(
            promoted.get("publication_manifest")
            == "publication-manifests/unitary-enterprise-rdm-manifest-analysis-20260826.json",
            "promoted 26-Aug publication manifest missing",
        )
        require(promoted.get("pages_run_id") == PAGES_RUN_ID, "promoted Pages run drift")
        require(promoted.get("live_verification_run_id") == UNITARY_VERIFY_RUN, "promoted verifier drift")
        require(promoted.get("live_verification_job_id") == UNITARY_VERIFY_JOB, "promoted verifier job drift")
        require(
            promoted.get("live_verification") == "EXACT_SHA_DEPLOYMENT_AND_21_URL_NO_CACHE_READBACK_VERIFIED",
            "promoted 26-Aug live-verification boundary drift",
        )
        pages = state["publication"]["last_pages_deployment"]
        for key, expected in {
            "sha": MERGE_SHA,
            "tree_sha": TREE_SHA,
            "run_id": PAGES_RUN_ID,
            "run_number": PAGES_RUN_NUMBER,
            "status": "completed",
            "conclusion": "success",
            "completed_at": PAGES_COMPLETED_AT,
        }.items():
            require(pages.get(key) == expected, f"unitary Pages evidence drift: {key}")
        readback = state["publication"]["current_sha_edge_readback"]
        require(readback["state"] == "LIVE_VERIFIED", "state readback is not live verified")
        require(readback["workflow_run_id"] == UNITARY_VERIFY_RUN, "unexpected unitary verifier run")
        require(readback.get("workflow_run_number") == UNITARY_VERIFY_RUN_NUMBER, "unitary verifier number drift")
        require(readback.get("job_id") == UNITARY_VERIFY_JOB, "unitary verifier job drift")
        require(readback.get("head_sha") == MERGE_SHA, "unitary readback merge drift")
        require(readback.get("tree_sha") == TREE_SHA, "unitary readback tree drift")
        require(readback.get("completed_at") == UNITARY_VERIFY_COMPLETED_AT, "unitary verifier completion drift")
        require(readback.get("verified_url_count") == 21, "unitary verifier URL scope drift")
        require(len(state["publication"].get("live_urls") or []) == 21, "unitary live-URL scope drift")
        require(state["pull_requests"]["observed_open_count"] == 36, "unitary open-PR snapshot drift")

        current = load_json(ROOT / "ops/CURRENT_STATE.json")
        require(
            current.get("schema") == "por-derecho.operational-truth.current-state.v2",
            "operational current-state schema drift",
        )
        require(
            current.get("record_type") == "CURRENT_STATE_CONTRACT_WITH_LAST_OBSERVATION",
            "operational current-state record type drift",
        )
        routing = current.get("specialist_state_routing") or {}
        require(
            routing.get("unitary_case_and_evidence_state") == "ops/CURRENT_UNITARY_STATE.json",
            "operational→unitary routing missing",
        )
        require(routing.get("expected_control_id") == UNITARY_CONTROL_ID, "operational unitary-control expectation drift")
        require(routing.get("expected_status") == "LIVE_VERIFIED", "operational unitary-status expectation drift")
        require(
            "Neither layer substitutes" in str(routing.get("rule", "")),
            "operational/unitary non-substitution rule missing",
        )
        require(
            current.get("corpus", {}).get("identity_registry", {}).get("counts") == EXPECTED,
            "operational identity counts drift",
        )
        observation = current.get("repository_observation") or {}
        require(observation.get("sha") == MERGE_SHA, "operational repository merge drift")
        require(observation.get("tree_sha") == TREE_SHA, "operational repository tree drift")
        deployment_observation = current.get("deployment_observation") or {}
        require(deployment_observation.get("last_observed_pages_run_id") == PAGES_RUN_ID, "operational Pages run drift")
        require(
            deployment_observation.get("verification_level") == "LIVE_VERIFIED_FOR_SERVED_SHA",
            "operational served-SHA verification state drift",
        )
        require(
            deployment_observation.get("last_exact_route_verification_run_id") == UNITARY_VERIFY_RUN,
            "operational exact-route verifier drift",
        )

        production = load_json(ROOT / "ops/PRODUCTION_STATUS.json")
        require(
            production.get("schema") == "por-derecho.operational-truth.production-status.v2",
            "production status schema drift",
        )
        require(
            production.get("record_type") == "OBSERVED_GITHUB_PAGES_DEPLOYMENT",
            "production status record type drift",
        )
        require(production.get("deployment", {}).get("conclusion") == "success", "observed Pages deployment is not successful")
        require(production.get("served_sha") == MERGE_SHA, "production served merge drift")
        require(production.get("source_tree_sha") == TREE_SHA, "production tree drift")
        require(production.get("deployment", {}).get("workflow_run_id") == PAGES_RUN_ID, "production Pages run drift")
        require(production.get("verification", {}).get("state") == "LIVE_VERIFIED", "production verification is not live")
        require(
            production.get("verification", {}).get("current_exact_route_content_verification")
            == "LIVE_VERIFIED_FOR_SERVED_SHA",
            "current served-SHA exact readback is not live verified",
        )
        specialist = production.get("verification", {}).get("latest_live_verified_specialist_release") or {}
        require(specialist.get("state") == "LIVE_VERIFIED", "production specialist readback evidence missing")
        require(specialist.get("control_id") == UNITARY_CONTROL_ID, "production specialist control mismatch")
        require(specialist.get("workflow_run_id") == UNITARY_VERIFY_RUN, "production specialist verifier mismatch")
        require(specialist.get("workflow_run_number") == UNITARY_VERIFY_RUN_NUMBER, "production verifier number mismatch")
        require(specialist.get("job_id") == UNITARY_VERIFY_JOB, "production verifier job mismatch")
        require(specialist.get("source_publication_sha") == MERGE_SHA, "production specialist merge mismatch")
        require(specialist.get("source_tree_sha") == TREE_SHA, "production specialist tree mismatch")
        require(
            production.get("specialist_state_routing", {}).get("unitary_case_and_evidence_state")
            == "ops/CURRENT_UNITARY_STATE.json",
            "production→unitary routing missing",
        )

        ledger = load_json(ROOT / "ops/PR_RECONCILIATION_LEDGER.json")
        require(isinstance(ledger.get("open_pull_request_count"), int), "PR ledger count missing")
        entries = {item["pr"]: item for item in ledger.get("priority_entries", [])}
        require(entries.get(1016, {}).get("state") == "REBUILD_ON_CURRENT_MAIN", "PR #1016 is not controlled")
        require(entries.get(771, {}).get("state") == "EXTRACT_UNIQUE_DELTA", "262-finca PR not controlled")

        require_markers(
            ROOT / "sitemap-unitary-control-plane.xml",
            [
                "https://sbu001monterecco.github.io/por-derecho/es/",
                "https://sbu001monterecco.github.io/por-derecho/en/updates/",
                "https://sbu001monterecco.github.io/por-derecho/es/registro-identidad-materia/",
                "<lastmod>2026-08-26</lastmod>",
            ],
        )
        require_markers(
            ROOT / "robots.txt",
            ["sitemap-unitary-control-plane.xml", "sitemap-prescription-recovery.xml"],
        )
        require_markers(
            ROOT / "CURRENT_UNITARY_STATE.md",
            [
                UNITARY_CONTROL_ID,
                "LIVE_VERIFIED",
                str(UNITARY_VERIFY_RUN),
                str(UNITARY_VERIFY_JOB),
                MERGE_SHA,
                TREE_SHA,
                "2026-08-26_LIVE_VERIFIED",
                "PR #1016",
            ],
        )

        manifest = load_json(ROOT / "publication-manifests/unitary-control-plane-sync-20260825.json")
        require(manifest.get("current_state") == "LIVE_VERIFIED", "manifest is not live verified")
        require(manifest.get("status") == "live_verified", "manifest status mismatch")
        require(manifest.get("control_id") == HISTORICAL_CONTROL_ID, "historical manifest/control mismatch")
        require(
            manifest.get("live_verification_evidence", {}).get("workflow_run_id") == HISTORICAL_VERIFY_RUN,
            "historical manifest verifier run mismatch",
        )
        require(
            manifest.get("expected_routes", {}).get("es")
            and manifest.get("expected_routes", {}).get("en"),
            "manifest expected routes missing",
        )

        promoted_manifest = load_json(
            ROOT / "publication-manifests/unitary-enterprise-rdm-manifest-analysis-20260826.json"
        )
        require(promoted_manifest.get("control_id") == UNITARY_CONTROL_ID, "promoted manifest/control mismatch")
        require(promoted_manifest.get("current_state") == "LIVE_VERIFIED", "promoted manifest state mismatch")
        require(promoted_manifest.get("status") == "live_verified", "promoted manifest status mismatch")
        require(promoted_manifest.get("source_main_sha") == SOURCE_MAIN_26, "promoted manifest source-main drift")
        require(promoted_manifest.get("publication_merge_sha") == MERGE_SHA, "promoted manifest merge drift")
        require(promoted_manifest.get("publication_tree_sha") == TREE_SHA, "promoted manifest tree drift")
        require(promoted_manifest.get("pages_run_id") == PAGES_RUN_ID, "promoted manifest Pages run drift")
        require(
            promoted_manifest.get("live_verification") == "passed_exact_no_cache",
            "promoted manifest exact no-cache verification state drift",
        )
        promoted_verifier = promoted_manifest.get("live_verification_evidence") or {}
        for key, expected in {
            "workflow_run_id": UNITARY_VERIFY_RUN,
            "workflow_run_number": UNITARY_VERIFY_RUN_NUMBER,
            "job_id": UNITARY_VERIFY_JOB,
            "head_sha": MERGE_SHA,
            "tree_sha": TREE_SHA,
            "completed_at": UNITARY_VERIFY_COMPLETED_AT,
            "verified_url_count": 21,
        }.items():
            require(promoted_verifier.get(key) == expected, f"promoted manifest verifier drift: {key}")
        allegation = promoted_manifest.get("controlling_allegation") or {}
        require(allegation.get("not_a_finding") is True, "promoted manifest allegation/finding boundary missing")
        require(allegation.get("independent_of_rdm_manifest") is True, "promoted manifest independence boundary missing")
        require(
            allegation.get("rdm_manifest_evidential_support")
            == "NONE_UNTIL_RELEVANT_NATIVES_ARE_ACQUIRED_AUTHENTICATED_AND_TESTED",
            "promoted manifest/native evidential boundary drift",
        )
    except AssertionError as exc:
        print(f"UNITARY CONTROL PLANE: FAIL\n - {exc}", file=sys.stderr)
        return 1

    print("UNITARY CONTROL PLANE: PASS")
    print(" - specialist status: LIVE_VERIFIED")
    print(" - operational repository/deployment state remains separate")
    print(" - source/static identity denominator: 214 / 94 / 74 / 10 / 18 / 18")
    print(" - latest live-verified identity snapshot: 204 / 87 / 71 / 10 / 18 / 18")
    print(" - promoted 26-Aug unitary snapshot remains 194 / 86 / 66 / 10 / 15 / 17")
    print(" - repository latest material date: 2026-08-26")
    print(" - last live-verified material date: 2026-08-26")
    print(" - promoted publication: PD-UNITARY-STATE-20260826-01 / LIVE_VERIFIED")
    print(f" - specialist verifier run: {UNITARY_VERIFY_RUN}")
    print(" - PR #1016 controlled as rebuild-on-current-main")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

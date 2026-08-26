#!/usr/bin/env python3
"""Validate separation and referential integrity of Por Derecho operational truth."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "ops"
DATA = ROOT / "assets" / "data"

CURRENT_PATH = OPS / "CURRENT_STATE.json"
PRODUCTION_PATH = OPS / "PRODUCTION_STATUS.json"
ROLLBACK_PATH = OPS / "LAST_KNOWN_GOOD.json"
LEDGER_PATH = OPS / "RELEASE_LEDGER.json"
UNITARY_PATH = OPS / "CURRENT_UNITARY_STATE.json"
IDENTITY_PATH = DATA / "matter-identity-registry-v1.json"
PROFESSIONAL_PATH = DATA / "legal-professionals-register-v1.json"

CURRENT_SCHEMA = "por-derecho.operational-truth.current-state.v2"
PRODUCTION_SCHEMA = "por-derecho.operational-truth.production-status.v2"
ROLLBACK_SCHEMA = "por-derecho.operational-truth.rollback-anchor.v2"
LEDGER_SCHEMA = "por-derecho.operational-truth.release-ledger.v1"
UNITARY_SCHEMA = "por-derecho.current-unitary-state.v1"
UNITARY_CONTROL_ID = "PD-UNITARY-STATE-20260825-01"
HISTORICAL_PR922_SHA = "ed98b0ac634afc34f00a425e9ed67ca58fd77cb8"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_OBSERVATION_STATES = {
    "BASELINE_OBSERVED_BEFORE_OPERATIONAL_TRUTH_CHANGE",
    "POST_MERGE_MAIN_AND_DEPLOYMENT_OBSERVED",
}


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AssertionError(f"cannot parse {path.relative_to(ROOT)}: {exc}") from exc
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} root must be object")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parse_time(value: Any, context: str) -> dt.datetime:
    require(isinstance(value, str) and value.strip(), f"{context} timestamp missing")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AssertionError(f"{context} timestamp invalid: {value}") from exc
    require(parsed.tzinfo is not None, f"{context} must be timezone-aware")
    return parsed


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, stderr=subprocess.STDOUT
    ).strip()


def git_object_exists(sha: str) -> bool:
    try:
        subprocess.check_call(
            ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def is_ancestor(ancestor: str, descendant: str = "HEAD") -> bool:
    try:
        subprocess.check_call(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def validate_append_only(new_ledger: dict[str, Any]) -> None:
    base_sha = os.getenv("GITHUB_BASE_SHA", "").strip()
    if not SHA_RE.fullmatch(base_sha):
        return
    try:
        old_text = subprocess.check_output(
            ["git", "show", f"{base_sha}:ops/RELEASE_LEDGER.json"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError:
        # First introduction of the ledger.
        return
    old_ledger = json.loads(old_text)
    old_releases = old_ledger.get("releases") or []
    new_releases = new_ledger.get("releases") or []
    require(
        new_releases[: len(old_releases)] == old_releases,
        "release ledger is not append-only: an existing release changed or disappeared",
    )


def main() -> int:
    try:
        current = load(CURRENT_PATH)
        production = load(PRODUCTION_PATH)
        rollback = load(ROLLBACK_PATH)
        ledger = load(LEDGER_PATH)
        unitary = load(UNITARY_PATH)
        identity = load(IDENTITY_PATH)
        professional = load(PROFESSIONAL_PATH)

        require(current.get("schema") == CURRENT_SCHEMA, "unexpected CURRENT_STATE schema")
        require(
            current.get("record_type") == "CURRENT_STATE_CONTRACT_WITH_LAST_OBSERVATION",
            "CURRENT_STATE must be a contract plus last observation",
        )
        require(production.get("schema") == PRODUCTION_SCHEMA, "unexpected PRODUCTION_STATUS schema")
        require(
            production.get("record_type") == "OBSERVED_GITHUB_PAGES_DEPLOYMENT",
            "PRODUCTION_STATUS must describe an observed deployment",
        )
        require(rollback.get("schema") == ROLLBACK_SCHEMA, "unexpected LAST_KNOWN_GOOD schema")
        require(
            rollback.get("record_type") == "HISTORICAL_ROLLBACK_ANCHOR",
            "LAST_KNOWN_GOOD must be an historical rollback anchor",
        )
        require(ledger.get("schema") == LEDGER_SCHEMA, "unexpected RELEASE_LEDGER schema")
        require(
            ledger.get("record_type") == "APPEND_ONLY_RELEASE_LEDGER",
            "release-ledger role missing",
        )
        require(ledger.get("append_only") is True, "release ledger must declare append_only=true")
        require(
            isinstance(ledger.get("latest_observation_release_id"), str)
            and ledger["latest_observation_release_id"].strip(),
            "release ledger latest-observation pointer missing",
        )

        observation = current.get("repository_observation") or {}
        observation_sha = observation.get("sha")
        tree_sha = observation.get("tree_sha")
        require(
            isinstance(observation_sha, str) and SHA_RE.fullmatch(observation_sha),
            "observed main SHA invalid",
        )
        require(
            isinstance(tree_sha, str) and SHA_RE.fullmatch(tree_sha),
            "observed tree SHA invalid",
        )
        require(git_object_exists(observation_sha), "observed main SHA is absent from checkout history")
        require(is_ancestor(observation_sha), "observed main SHA is not an ancestor of HEAD")
        require(
            git("show", "-s", "--format=%T", observation_sha) == tree_sha,
            "observed main tree SHA does not match the observed commit",
        )
        parse_time(observation.get("commit_time"), "repository_observation.commit_time")
        parse_time(observation.get("observed_at"), "repository_observation.observed_at")
        require(
            observation.get("status") in ALLOWED_OBSERVATION_STATES,
            "repository observation boundary is not explicit",
        )

        freshness = current.get("freshness_policy") or {}
        for key in (
            "max_main_ahead_commits_before_refresh",
            "max_observation_age_hours_before_refresh",
            "max_open_pr_count_drift_before_refresh",
        ):
            require(
                isinstance(freshness.get(key), (int, float)),
                f"freshness policy missing {key}",
            )
            require(float(freshness[key]) >= 0, f"freshness policy {key} must be non-negative")
        require(
            freshness.get("runtime_generator") == "scripts/generate_operational_truth.py",
            "runtime generator path mismatch",
        )
        require(
            freshness.get("structural_validator") == "scripts/validate_operational_truth.py",
            "structural validator path mismatch",
        )

        inventory = current.get("repository_inventory_observation") or {}
        require(
            isinstance(inventory.get("open_pull_requests"), int),
            "open-PR observation must be integer",
        )
        require(inventory["open_pull_requests"] >= 0, "open-PR observation cannot be negative")
        require(
            "Observation only" in str(inventory.get("meaning")),
            "open-PR observational boundary missing",
        )
        parse_time(inventory.get("observed_at"), "repository_inventory_observation.observed_at")

        corpus = current.get("corpus") or {}
        current_identity = (corpus.get("identity_registry") or {}).get("counts")
        current_professional = (corpus.get("legal_professional_register") or {}).get("counts")
        require(current_identity == identity.get("counts"), "CURRENT_STATE identity counts drift")
        require(
            current_professional == professional.get("counts"),
            "CURRENT_STATE professional counts drift",
        )
        require(
            (corpus.get("identity_registry") or {}).get("registry_id")
            == identity.get("registry_id"),
            "CURRENT_STATE identity registry ID mismatch",
        )
        require(
            (corpus.get("legal_professional_register") or {}).get("register_id")
            == professional.get("register_id"),
            "CURRENT_STATE professional register ID mismatch",
        )

        routing = current.get("specialist_state_routing") or {}
        require(
            routing.get("unitary_case_and_evidence_state")
            == "ops/CURRENT_UNITARY_STATE.json",
            "operational-to-unitary routing missing",
        )
        require(
            routing.get("expected_control_id") == UNITARY_CONTROL_ID,
            "unitary control expectation drift",
        )
        require(
            routing.get("expected_status") == "LIVE_VERIFIED",
            "unitary status expectation drift",
        )
        require(
            "Neither layer substitutes" in str(routing.get("rule")),
            "non-substitution rule missing",
        )

        require(unitary.get("schema") == UNITARY_SCHEMA, "unitary specialist schema drift")
        require(
            unitary.get("control_id") == UNITARY_CONTROL_ID,
            "unitary specialist control ID drift",
        )
        require(
            unitary.get("status") == "LIVE_VERIFIED",
            "unitary specialist state is not LIVE_VERIFIED",
        )
        require(
            (unitary.get("identity_registry") or {}).get("counts")
            == identity.get("counts"),
            "unitary identity counts drift from canonical registry",
        )

        served_sha = production.get("served_sha")
        served_tree = production.get("source_tree_sha")
        require(
            isinstance(served_sha, str) and SHA_RE.fullmatch(served_sha),
            "production served SHA invalid",
        )
        require(
            isinstance(served_tree, str) and SHA_RE.fullmatch(served_tree),
            "production tree SHA invalid",
        )
        require(git_object_exists(served_sha), "production served SHA absent from checkout history")
        require(
            git("show", "-s", "--format=%T", served_sha) == served_tree,
            "production source tree does not match served commit",
        )
        deployment = production.get("deployment") or {}
        require(
            deployment.get("status") == "completed",
            "observed Pages deployment is not completed",
        )
        require(
            deployment.get("conclusion") == "success",
            "observed Pages deployment did not succeed",
        )
        require(
            isinstance(deployment.get("workflow_run_id"), int),
            "Pages workflow run ID must be integer",
        )
        parse_time(production.get("observed_at"), "PRODUCTION_STATUS.observed_at")
        verification = production.get("verification") or {}
        require(
            verification.get("state") == "DEPLOYMENT_BUILD_SUCCESS",
            "production status overclaims or understates deployment",
        )
        require(
            verification.get("current_exact_route_content_verification")
            == "NOT_RECORDED_FOR_SERVED_SHA",
            "current served-SHA readback boundary missing",
        )
        specialist_release = verification.get("latest_live_verified_specialist_release") or {}
        require(
            specialist_release.get("state") == "LIVE_VERIFIED",
            "live-verified specialist release missing",
        )
        require(
            specialist_release.get("control_id") == UNITARY_CONTROL_ID,
            "specialist release control mismatch",
        )
        require(
            SHA_RE.fullmatch(str(specialist_release.get("source_publication_sha", "")))
            is not None,
            "specialist source SHA invalid",
        )
        require(
            SHA_RE.fullmatch(str(specialist_release.get("verification_fix_sha", "")))
            is not None,
            "specialist verification SHA invalid",
        )
        require(
            isinstance(specialist_release.get("workflow_run_id"), int),
            "specialist verification run missing",
        )
        require(
            (production.get("specialist_state_routing") or {}).get(
                "unitary_case_and_evidence_state"
            )
            == "ops/CURRENT_UNITARY_STATE.json",
            "production-to-unitary routing missing",
        )

        current_deployment = current.get("deployment_observation") or {}
        require(
            current_deployment.get("status_file") == "ops/PRODUCTION_STATUS.json",
            "CURRENT_STATE deployment-status path mismatch",
        )
        require(
            current_deployment.get("last_observed_served_sha") == served_sha,
            "CURRENT_STATE deployment SHA does not match PRODUCTION_STATUS",
        )
        require(
            current_deployment.get("last_observed_pages_run_id")
            == deployment.get("workflow_run_id"),
            "CURRENT_STATE Pages run does not match PRODUCTION_STATUS",
        )
        require(
            current_deployment.get("verification_level") == "DEPLOYMENT_BUILD_SUCCESS",
            "CURRENT_STATE deployment verification level drift",
        )
        parse_time(
            current_deployment.get("last_observed_at"),
            "deployment_observation.last_observed_at",
        )

        require(rollback.get("is_current") is False, "rollback anchor must not claim current status")
        require(
            rollback.get("rollback_eligible") is True,
            "rollback anchor must remain eligible",
        )
        require(
            rollback.get("state") == "LIVE_VERIFIED",
            "rollback anchor lost LIVE_VERIFIED state",
        )
        require(
            rollback.get("source_sha") == HISTORICAL_PR922_SHA,
            "historical PR #922 SHA changed",
        )

        releases = ledger.get("releases")
        require(isinstance(releases, list) and releases, "release ledger must contain releases")
        release_ids: set[str] = set()
        release_shas: set[str] = set()
        effective_times: list[dt.datetime] = []
        release_by_sha: dict[str, dict[str, Any]] = {}
        current_records: list[dict[str, Any]] = []
        for index, release in enumerate(releases, start=1):
            require(isinstance(release, dict), f"release #{index} must be object")
            release_id = release.get("release_id")
            source_sha = release.get("source_sha")
            require(
                isinstance(release_id, str) and release_id.strip(),
                f"release #{index} ID missing",
            )
            require(release_id not in release_ids, f"duplicate release_id: {release_id}")
            release_ids.add(release_id)
            require(
                isinstance(source_sha, str) and SHA_RE.fullmatch(source_sha),
                f"invalid source SHA: {release_id}",
            )
            require(source_sha not in release_shas, f"duplicate source SHA in ledger: {source_sha}")
            release_shas.add(source_sha)
            release_by_sha[source_sha] = release
            effective_times.append(
                parse_time(release.get("effective_at"), f"release {release_id}")
            )
            require(
                isinstance(release.get("current_at_observation"), bool),
                f"release current_at_observation must be boolean: {release_id}",
            )
            if release.get("current_at_observation") is True:
                current_records.append(release)
        require(effective_times == sorted(effective_times), "release ledger is not chronological")
        require(current_records, "release ledger has no current-at-observation records")
        latest_observation_id = ledger.get("latest_observation_release_id")
        latest_current = current_records[-1]
        require(
            latest_current.get("release_id") == latest_observation_id,
            "latest-observation pointer does not resolve to the last current-at-observation release",
        )
        require(
            latest_current.get("source_sha") == served_sha,
            "latest observed ledger release does not match served SHA",
        )
        require(
            HISTORICAL_PR922_SHA in release_by_sha,
            "rollback anchor absent from ledger",
        )
        require(
            release_by_sha[HISTORICAL_PR922_SHA].get("rollback_eligible") is True,
            "rollback release not eligible in ledger",
        )

        corrections = ledger.get("corrections")
        require(isinstance(corrections, list), "release ledger corrections must be an array")
        require(
            any(
                isinstance(item, dict)
                and item.get("correction_id")
                == "release-ledger-current-observation-semantics-20260826"
                for item in corrections
            ),
            "release-ledger current-observation semantics correction missing",
        )

        for path in [
            OPS / "OPERATIONAL_TRUTH_PROTOCOL.md",
            ROOT / "archive" / "ops-snapshots" / "README.md",
            ROOT / "archive" / "ops-snapshots" / "CURRENT_STATE_20260824.json",
            ROOT / "archive" / "ops-snapshots" / "PRODUCTION_STATUS_20260824.json",
            ROOT / "scripts" / "generate_operational_truth.py",
            ROOT / "scripts" / "validate_operational_truth.py",
            ROOT / ".github" / "workflows" / "validate-operational-truth.yml",
        ]:
            require(
                path.is_file(),
                f"required operational-truth file missing: {path.relative_to(ROOT)}",
            )

        old_current = load(ROOT / "archive" / "ops-snapshots" / "CURRENT_STATE_20260824.json")
        old_production = load(
            ROOT / "archive" / "ops-snapshots" / "PRODUCTION_STATUS_20260824.json"
        )
        require(
            (old_current.get("repository") or {}).get("baseline_main_sha")
            == HISTORICAL_PR922_SHA,
            "historical CURRENT_STATE snapshot lost PR #922 baseline",
        )
        require(
            old_production.get("exact_live_sha") == HISTORICAL_PR922_SHA,
            "historical PRODUCTION_STATUS snapshot lost PR #922 exact SHA",
        )

        for prohibited in (
            "baseline_main_sha",
            "baseline_release",
            "main_at_audit",
            "exact_live_sha",
        ):
            require(
                prohibited not in current,
                f"legacy current-truth key remains at CURRENT_STATE root: {prohibited}",
            )

        validate_append_only(ledger)

        print("OPERATIONAL TRUTH: PASS")
        print(f" - observed repository baseline: {observation_sha}")
        print(f" - checked-out head: {git('rev-parse', 'HEAD')}")
        print(f" - observed Pages SHA: {served_sha}; run {deployment.get('workflow_run_id')}")
        print(f" - specialist state: {unitary.get('control_id')} / {unitary.get('status')}")
        print(f" - canonical identities: {identity.get('counts', {}).get('total')}")
        print(f" - professional records: {professional.get('counts', {}).get('total')}")
        print(f" - release-ledger entries: {len(releases)}")
        print(f" - latest observed release: {latest_observation_id}")
        print(" - PR #922 preserved as historical rollback anchor, not current truth")
        return 0
    except (AssertionError, subprocess.CalledProcessError) as exc:
        print(f"OPERATIONAL TRUTH: FAIL\n - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

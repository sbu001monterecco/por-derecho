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

CURRENT_PATH = OPS / "CURRENT_STATE.json"
PRODUCTION_PATH = OPS / "PRODUCTION_STATUS.json"
ROLLBACK_PATH = OPS / "LAST_KNOWN_GOOD.json"
LEDGER_PATH = OPS / "RELEASE_LEDGER.json"
IDENTITY_PATH = ROOT / "assets" / "data" / "matter-identity-registry-v1.json"
PROFESSIONAL_PATH = ROOT / "assets" / "data" / "legal-professionals-register-v1.json"

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
CURRENT_SCHEMA = "por-derecho.operational-truth.current-state.v2"
PRODUCTION_SCHEMA = "por-derecho.operational-truth.production-status.v2"
ROLLBACK_SCHEMA = "por-derecho.operational-truth.rollback-anchor.v2"
LEDGER_SCHEMA = "por-derecho.operational-truth.release-ledger.v1"
HISTORICAL_PR922_SHA = "ed98b0ac634afc34f00a425e9ed67ca58fd77cb8"


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AssertionError(f"cannot parse {path.relative_to(ROOT)}: {exc}") from exc
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} root must be an object")
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
    require(parsed.tzinfo is not None, f"{context} timestamp must be timezone-aware")
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
        # The first introduction of the ledger has no base copy.
        return
    try:
        old_ledger = json.loads(old_text)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"base release ledger is invalid JSON: {exc}") from exc
    old_releases = old_ledger.get("releases") or []
    new_releases = new_ledger.get("releases") or []
    require(
        new_releases[: len(old_releases)] == old_releases,
        "release ledger is not append-only: existing release records changed or disappeared",
    )


def main() -> int:
    try:
        current = load(CURRENT_PATH)
        production = load(PRODUCTION_PATH)
        rollback = load(ROLLBACK_PATH)
        ledger = load(LEDGER_PATH)
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
        require(rollback.get("is_current") is False, "rollback anchor must not claim to be current")
        require(rollback.get("rollback_eligible") is True, "rollback anchor must remain rollback-eligible")
        require(ledger.get("schema") == LEDGER_SCHEMA, "unexpected RELEASE_LEDGER schema")
        require(ledger.get("record_type") == "APPEND_ONLY_RELEASE_LEDGER", "release-ledger role missing")
        require(ledger.get("append_only") is True, "release ledger must declare append_only=true")

        observation = current.get("repository_observation") or {}
        observation_sha = observation.get("sha")
        tree_sha = observation.get("tree_sha")
        require(isinstance(observation_sha, str) and SHA_RE.fullmatch(observation_sha), "observed main SHA invalid")
        require(isinstance(tree_sha, str) and SHA_RE.fullmatch(tree_sha), "observed tree SHA invalid")
        require(git_object_exists(observation_sha), "observed main SHA is not present in checkout history")
        require(is_ancestor(observation_sha), "observed main SHA is not an ancestor of checked-out HEAD")
        parse_time(observation.get("commit_time"), "repository_observation.commit_time")
        parse_time(observation.get("observed_at"), "repository_observation.observed_at")
        require(
            observation.get("status") == "BASELINE_OBSERVED_BEFORE_OPERATIONAL_TRUTH_CHANGE",
            "repository observation status must make its pre-change boundary explicit",
        )

        freshness = current.get("freshness_policy") or {}
        for key in (
            "max_main_ahead_commits_before_refresh",
            "max_observation_age_hours_before_refresh",
            "max_open_pr_count_drift_before_refresh",
        ):
            require(isinstance(freshness.get(key), (int, float)), f"freshness policy missing numeric {key}")
            require(float(freshness[key]) >= 0, f"freshness policy {key} must be non-negative")
        require(
            freshness.get("runtime_generator") == "scripts/generate_operational_truth.py",
            "runtime generator path mismatch",
        )
        require(
            freshness.get("structural_validator") == "scripts/validate_operational_truth.py",
            "structural validator path mismatch",
        )

        pr_observation = current.get("repository_inventory_observation") or {}
        require(isinstance(pr_observation.get("open_pull_requests"), int), "open-PR observation must be integer")
        require(pr_observation["open_pull_requests"] >= 0, "open-PR observation cannot be negative")
        require(
            "Observation only" in str(pr_observation.get("meaning")),
            "open-PR snapshot must state that it is observational",
        )
        parse_time(pr_observation.get("observed_at"), "repository_inventory_observation.observed_at")

        corpus = current.get("corpus") or {}
        current_identity = (corpus.get("identity_registry") or {}).get("counts")
        current_professional = (corpus.get("legal_professional_register") or {}).get("counts")
        require(current_identity == identity.get("counts"), "CURRENT_STATE identity counts drift from canonical JSON")
        require(
            (corpus.get("identity_registry") or {}).get("registry_id") == identity.get("registry_id"),
            "CURRENT_STATE identity registry ID mismatch",
        )
        require(current_professional == professional.get("counts"), "CURRENT_STATE professional counts drift")
        require(
            (corpus.get("legal_professional_register") or {}).get("register_id") == professional.get("register_id"),
            "CURRENT_STATE professional register ID mismatch",
        )

        served_sha = production.get("served_sha")
        served_tree = production.get("source_tree_sha")
        require(isinstance(served_sha, str) and SHA_RE.fullmatch(served_sha), "production served SHA invalid")
        require(isinstance(served_tree, str) and SHA_RE.fullmatch(served_tree), "production tree SHA invalid")
        require(git_object_exists(served_sha), "production served SHA is not present in checkout history")
        deployment = production.get("deployment") or {}
        require(deployment.get("status") == "completed", "observed Pages deployment is not completed")
        require(deployment.get("conclusion") == "success", "observed Pages deployment did not succeed")
        require(isinstance(deployment.get("workflow_run_id"), int), "Pages workflow run ID must be integer")
        parse_time(production.get("observed_at"), "PRODUCTION_STATUS.observed_at")
        verification = production.get("verification") or {}
        require(
            verification.get("state") == "DEPLOYMENT_BUILD_SUCCESS",
            "production status must not overclaim live route verification",
        )
        require(
            verification.get("exact_route_content_verification") == "NOT_RECORDED_FOR_THIS_SHA",
            "production status must state route-verification boundary",
        )

        releases = ledger.get("releases")
        require(isinstance(releases, list) and releases, "release ledger must contain releases")
        release_ids: set[str] = set()
        release_shas: set[str] = set()
        ordered_times: list[dt.datetime] = []
        release_by_sha: dict[str, dict[str, Any]] = {}
        for index, release in enumerate(releases, start=1):
            require(isinstance(release, dict), f"release #{index} must be object")
            release_id = release.get("release_id")
            source_sha = release.get("source_sha")
            require(isinstance(release_id, str) and release_id.strip(), f"release #{index} ID missing")
            require(release_id not in release_ids, f"duplicate release_id: {release_id}")
            release_ids.add(release_id)
            require(isinstance(source_sha, str) and SHA_RE.fullmatch(source_sha), f"invalid source SHA: {release_id}")
            require(source_sha not in release_shas, f"duplicate source SHA in ledger: {source_sha}")
            release_shas.add(source_sha)
            release_by_sha[source_sha] = release
            time_value = (
                release.get("deployed_at")
                or release.get("verified_at")
                or release.get("merged_at")
                or release.get("observed_at")
            )
            ordered_times.append(parse_time(time_value, f"release {release_id}"))
        require(ordered_times == sorted(ordered_times), "release ledger is not chronological")

        rollback_sha = rollback.get("source_sha")
        require(rollback_sha == HISTORICAL_PR922_SHA, "historical rollback SHA changed unexpectedly")
        require(rollback_sha in release_by_sha, "rollback anchor is absent from release ledger")
        rollback_release = release_by_sha[rollback_sha]
        require(rollback_release.get("state") == "LIVE_VERIFIED", "rollback release lost LIVE_VERIFIED state")
        require(rollback_release.get("rollback_eligible") is True, "rollback release is not eligible")
        require(rollback_release.get("current_at_observation") is False, "rollback release wrongly marked current")

        require(served_sha in release_by_sha, "observed production SHA is absent from release ledger")
        served_release = release_by_sha[served_sha]
        require(
            served_release.get("pages_run_id") == deployment.get("workflow_run_id"),
            "production Pages run does not match release-ledger entry",
        )

        required_paths = [
            OPS / "OPERATIONAL_TRUTH_PROTOCOL.md",
            OPS / "history" / "README.md",
            OPS / "history" / "CURRENT_STATE_2026-08-24_PR922.json",
            OPS / "history" / "PRODUCTION_STATUS_2026-08-24_PR922.json",
            ROOT / "scripts" / "generate_operational_truth.py",
            ROOT / "scripts" / "validate_operational_truth.py",
            ROOT / ".github" / "workflows" / "validate-operational-truth.yml",
        ]
        for path in required_paths:
            require(path.is_file(), f"required operational-truth file missing: {path.relative_to(ROOT)}")

        old_current = load(OPS / "history" / "CURRENT_STATE_2026-08-24_PR922.json")
        old_production = load(OPS / "history" / "PRODUCTION_STATUS_2026-08-24_PR922.json")
        require(
            (old_current.get("repository") or {}).get("baseline_main_sha") == HISTORICAL_PR922_SHA,
            "historical CURRENT_STATE snapshot lost PR #922 baseline",
        )
        require(
            old_production.get("exact_live_sha") == HISTORICAL_PR922_SHA,
            "historical PRODUCTION_STATUS snapshot lost exact PR #922 SHA",
        )

        for prohibited in ("main_at_audit", "exact_live_sha", "baseline_main_sha", "baseline_release"):
            require(prohibited not in current, f"legacy exact-current key remains at CURRENT_STATE root: {prohibited}")

        validate_append_only(ledger)

        print("OPERATIONAL TRUTH: PASS")
        print(f" - observed repository baseline: {observation_sha}")
        print(f" - checked-out head: {git('rev-parse', 'HEAD')}")
        print(f" - observed Pages SHA: {served_sha}; run {deployment.get('workflow_run_id')}")
        print(f" - canonical identities: {identity.get('counts', {}).get('total')}")
        print(f" - professional records: {professional.get('counts', {}).get('total')}")
        print(f" - release-ledger entries: {len(releases)}")
        print(" - PR #922 preserved as historical rollback anchor, not current truth")
        return 0
    except (AssertionError, subprocess.CalledProcessError) as exc:
        print(f"OPERATIONAL TRUTH: FAIL\n - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

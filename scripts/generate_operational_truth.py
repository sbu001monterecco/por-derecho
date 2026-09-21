#!/usr/bin/env python3
"""Generate a runtime operational-truth report for Por Derecho.

Checked-in operational files are contracts and last observations. They are not
permanent current truth. This script resolves current repository/deployment
facts locally or, with --live, through GitHub's API.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPOSITORY = "sbu001monterecco/por-derecho"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} root must be an object")
    return value


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, stderr=subprocess.STDOUT
    ).strip()


def api_request(url: str, token: str | None) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Por-Derecho-Operational-Truth/2.0",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        value = json.load(response)
    if not isinstance(value, dict):
        raise ValueError(f"unexpected GitHub response for {url}")
    return value


def github_get(repository: str, path: str, token: str | None) -> dict[str, Any]:
    return api_request(
        f"https://api.github.com/repos/{repository}/{path.lstrip('/')}", token
    )


def github_search(repository: str, query: str, token: str | None) -> dict[str, Any]:
    encoded = urllib.parse.urlencode({"q": f"repo:{repository} {query}", "per_page": 1})
    return api_request(f"https://api.github.com/search/issues?{encoded}", token)


def local_repository_state() -> dict[str, Any]:
    try:
        branch = git("symbolic-ref", "--short", "HEAD")
    except subprocess.CalledProcessError:
        branch = "DETACHED"
    return {
        "mode": "LOCAL_GIT",
        "branch": branch,
        "sha": git("rev-parse", "HEAD"),
        "tree_sha": git("rev-parse", "HEAD^{tree}"),
        "commit_time": git("show", "-s", "--format=%cI", "HEAD"),
    }


def latest_successful_pages_run(
    repository: str, sha: str, token: str | None
) -> dict[str, Any] | None:
    query = urllib.parse.urlencode({"head_sha": sha, "per_page": 100})
    runs = github_get(repository, f"actions/runs?{query}", token).get(
        "workflow_runs", []
    )
    if not isinstance(runs, list):
        return None
    candidates = [
        item
        for item in runs
        if isinstance(item, dict)
        and item.get("status") == "completed"
        and item.get("conclusion") == "success"
        and (
            item.get("name") == "pages build and deployment"
            or item.get("path") == "dynamic/pages/pages-build-deployment"
        )
    ]
    if not candidates:
        return None
    candidates.sort(
        key=lambda item: str(item.get("updated_at") or item.get("created_at") or ""),
        reverse=True,
    )
    item = candidates[0]
    return {
        "workflow_run_id": item.get("id"),
        "run_number": item.get("run_number"),
        "name": item.get("name"),
        "path": item.get("path"),
        "status": item.get("status"),
        "conclusion": item.get("conclusion"),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "head_sha": item.get("head_sha"),
    }


def live_repository_state(repository: str, token: str | None) -> dict[str, Any]:
    branch = github_get(repository, "branches/main", token)
    commit = branch.get("commit") or {}
    sha = commit.get("sha")
    if not isinstance(sha, str):
        raise ValueError("GitHub branch response did not contain main SHA")
    commit_data = commit.get("commit") or {}
    tree = commit_data.get("tree") or {}
    open_prs = github_search(repository, "is:pr is:open", token)
    return {
        "mode": "LIVE_GITHUB",
        "branch": "main",
        "sha": sha,
        "tree_sha": tree.get("sha"),
        "commit_time": (commit_data.get("committer") or {}).get("date"),
        "open_pull_requests": open_prs.get("total_count"),
        "latest_successful_pages_run_for_main": latest_successful_pages_run(
            repository, sha, token
        ),
    }


def compare_observation_to_live(
    repository: str,
    observation_sha: str,
    live_sha: str,
    token: str | None,
) -> dict[str, Any]:
    if observation_sha == live_sha:
        return {"status": "identical", "ahead_by": 0, "behind_by": 0}
    value = github_get(repository, f"compare/{observation_sha}...{live_sha}", token)
    return {
        "status": value.get("status"),
        "ahead_by": value.get("ahead_by"),
        "behind_by": value.get("behind_by"),
        "total_commits": value.get("total_commits"),
    }


def parse_time(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def build_report(repository: str, live: bool, token: str | None) -> dict[str, Any]:
    current = load_json(ROOT / "ops" / "CURRENT_STATE.json")
    production = load_json(ROOT / "ops" / "PRODUCTION_STATUS.json")
    rollback = load_json(ROOT / "ops" / "LAST_KNOWN_GOOD.json")
    ledger = load_json(ROOT / "ops" / "RELEASE_LEDGER.json")
    identity = load_json(
        ROOT / "assets" / "data" / "matter-identity-registry-v1.json"
    )
    professional = load_json(
        ROOT / "assets" / "data" / "legal-professionals-register-v1.json"
    )
    unitary = load_json(ROOT / "ops" / "CURRENT_UNITARY_STATE.json")
    repo_state = (
        live_repository_state(repository, token) if live else local_repository_state()
    )

    observation = current.get("repository_observation") or {}
    inventory_observation = current.get("repository_inventory_observation") or {}
    freshness = current.get("freshness_policy") or {}
    drift: dict[str, Any] = {
        "static_observation_sha": observation.get("sha"),
        "static_open_pr_count": inventory_observation.get("open_pull_requests"),
        "static_production_served_sha": production.get("served_sha"),
    }

    if live:
        comparison = compare_observation_to_live(
            repository, str(observation.get("sha")), str(repo_state.get("sha")), token
        )
        drift["repository_comparison"] = comparison
        observed_at = parse_time(str(observation.get("observed_at")))
        age_hours = (
            dt.datetime.now(dt.timezone.utc) - observed_at
        ).total_seconds() / 3600
        drift["observation_age_hours"] = round(age_hours, 2)
        current_prs = repo_state.get("open_pull_requests")
        previous_prs = inventory_observation.get("open_pull_requests")
        drift["open_pr_count_delta"] = (
            int(current_prs) - int(previous_prs)
            if isinstance(current_prs, int) and isinstance(previous_prs, int)
            else None
        )
        pages = repo_state.get("latest_successful_pages_run_for_main")
        drift["production_status_matches_latest_successful_pages"] = bool(
            pages
            and pages.get("head_sha") == production.get("served_sha")
            and pages.get("workflow_run_id")
            == (production.get("deployment") or {}).get("workflow_run_id")
        )
        drift["within_freshness_policy"] = bool(
            comparison.get("status") in {"ahead", "identical"}
            and int(comparison.get("ahead_by") or 0)
            <= int(freshness.get("max_main_ahead_commits_before_refresh", 0))
            and age_hours
            <= float(freshness.get("max_observation_age_hours_before_refresh", 0))
            and abs(int(drift.get("open_pr_count_delta") or 0))
            <= int(freshness.get("max_open_pr_count_drift_before_refresh", 0))
        )
    else:
        try:
            subprocess.check_call(
                [
                    "git",
                    "merge-base",
                    "--is-ancestor",
                    str(observation.get("sha")),
                    "HEAD",
                ],
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            drift["static_observation_is_ancestor_of_head"] = True
        except subprocess.CalledProcessError:
            drift["static_observation_is_ancestor_of_head"] = False

    return {
        "schema": "por-derecho.operational-truth.runtime-report.v1",
        "generated_at": utc_now(),
        "repository": repository,
        "mode": "LIVE" if live else "LOCAL",
        "repository_state": repo_state,
        "corpus": {
            "identity_registry": {
                "registry_id": identity.get("registry_id"),
                "counts": identity.get("counts"),
            },
            "legal_professional_register": {
                "register_id": professional.get("register_id"),
                "counts": professional.get("counts"),
            },
        },
        "specialist_state": {
            "path": "ops/CURRENT_UNITARY_STATE.json",
            "control_id": unitary.get("control_id"),
            "status": unitary.get("status"),
            "identity_counts": (unitary.get("identity_registry") or {}).get("counts"),
        },
        "controls": {
            "current_state_schema": current.get("schema"),
            "production_status_schema": production.get("schema"),
            "rollback_record_type": rollback.get("record_type"),
            "release_ledger_entries": len(ledger.get("releases") or []),
        },
        "drift": drift,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repository", default=os.getenv("GITHUB_REPOSITORY", DEFAULT_REPOSITORY)
    )
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--fail-on-drift", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()

    try:
        report = build_report(args.repository, args.live, os.getenv("GITHUB_TOKEN"))
    except Exception as exc:
        print(f"OPERATIONAL TRUTH GENERATOR: FAIL\n - {exc}", file=sys.stderr)
        return 1

    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    if (
        args.fail_on_drift
        and args.live
        and not report["drift"].get("within_freshness_policy")
    ):
        print("OPERATIONAL TRUTH GENERATOR: DRIFT OUTSIDE POLICY", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

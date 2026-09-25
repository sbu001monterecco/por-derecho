#!/usr/bin/env python3
"""Poll the public GitHub Pages host until the optimum reader journey is live.

This is a public-content verification only. It does not use private credentials or
GitHub Pages administration APIs. A unique probe committed after the minimum
implementation commit, plus implementation-specific asset markers, proves that
the public host is serving the minimum commit or a descendant.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

MINIMUM_COMMIT = "6deaba19d8db5c5c5e20f2965ae8ab7deb28d8de"
PROBE_ID = "psr-pages-optimum-reader-journey-20260818-v1"

CHECKS = [
    {
        "path": "deployment-probes/optimum-reader-journey-20260818.json",
        "markers": [PROBE_ID, MINIMUM_COMMIT],
        "kind": "deployment_probe",
    },
    {
        "path": "assets/optimum-reader-journey-20260818.js",
        "markers": [
            "2026-08-18-optimum-reader-journey-v1",
            "psr-reader-intent",
            "psr-next-step",
        ],
        "kind": "core_asset",
    },
    {
        "path": "assets/optimum-reader-journey-finish-20260818.js",
        "markers": [
            "simplifyHeaderNavigation",
            "psr-hero-shortcuts",
            "movePrefaceModulesAfterHero",
        ],
        "kind": "finish_asset",
    },
    {
        "path": "assets/ricpe-filed-status-20260817.js",
        "markers": [
            "optimum-reader-journey-20260818.js",
            "optimum-reader-journey-finish-20260818.js",
        ],
        "kind": "loader_asset",
    },
    {
        "path": "es/",
        "markers": ["Project Sun Rock", "resumen-60-segundos"],
        "kind": "public_home",
    },
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def fetch(url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Por-Derecho-Pages-Propagation-Check/1.0",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
            "Accept": "text/html,application/json,text/javascript,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read()
        text = body.decode("utf-8", errors="replace")
        return {
            "status": response.status,
            "final_url": response.geturl(),
            "headers": {
                "etag": response.headers.get("ETag"),
                "last_modified": response.headers.get("Last-Modified"),
                "cache_control": response.headers.get("Cache-Control"),
                "age": response.headers.get("Age"),
                "server": response.headers.get("Server"),
                "x_github_request_id": response.headers.get("X-GitHub-Request-Id"),
                "x_cache": response.headers.get("X-Cache"),
                "via": response.headers.get("Via"),
            },
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "text": text,
        }


def check_once(base_url: str, attempt: int, timeout: int) -> tuple[bool, list[dict[str, Any]]]:
    results: list[dict[str, Any]] = []
    all_ok = True
    nonce = f"{int(time.time())}-{attempt}"

    for item in CHECKS:
        path = str(item["path"])
        url = urllib.parse.urljoin(base_url.rstrip("/") + "/", path)
        separator = "&" if "?" in url else "?"
        cache_busted_url = f"{url}{separator}psr_pages_probe={nonce}"
        record: dict[str, Any] = {
            "kind": item["kind"],
            "path": path,
            "url": url,
            "checked_url": cache_busted_url,
            "required_markers": item["markers"],
            "checked_at": utc_now(),
        }
        try:
            response = fetch(cache_busted_url, timeout)
            missing = [marker for marker in item["markers"] if marker not in response["text"]]
            record.update({key: value for key, value in response.items() if key != "text"})
            record["missing_markers"] = missing
            record["ok"] = response["status"] == 200 and not missing
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            record["ok"] = False
            record["error"] = f"{type(exc).__name__}: {exc}"
        if not record["ok"]:
            all_ok = False
        results.append(record)

    return all_ok, results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-url",
        default="https://sbu001monterecco.github.io/por-derecho/",
        help="Public GitHub Pages base URL.",
    )
    parser.add_argument("--attempts", type=int, default=72)
    parser.add_argument("--interval", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument(
        "--output",
        default="artifacts/pages-propagation/verification.json",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    started_at = utc_now()
    final_results: list[dict[str, Any]] = []

    for attempt in range(1, args.attempts + 1):
        ok, results = check_once(args.base_url, attempt, args.timeout)
        final_results = results
        summary = ", ".join(
            f"{item['kind']}={'OK' if item['ok'] else 'WAIT'}" for item in results
        )
        print(f"Attempt {attempt}/{args.attempts}: {summary}", flush=True)
        if ok:
            payload = {
                "verified": True,
                "verification_basis": (
                    "The live public host serves a probe file committed after the minimum "
                    "commit and all implementation-specific assets/markers introduced by "
                    "that implementation. The workflow commit is separately verified as a "
                    "Git descendant of the minimum commit."
                ),
                "minimum_commit": MINIMUM_COMMIT,
                "workflow_commit": os.environ.get("GITHUB_SHA"),
                "repository": os.environ.get("GITHUB_REPOSITORY"),
                "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
                "workflow_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
                "base_url": args.base_url,
                "started_at": started_at,
                "verified_at": utc_now(),
                "attempt": attempt,
                "checks": results,
            }
            output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print(
                "PUBLIC GITHUB PAGES PROPAGATION VERIFIED: "
                f"{MINIMUM_COMMIT} OR DESCENDANT",
                flush=True,
            )
            return 0
        if attempt < args.attempts:
            time.sleep(args.interval)

    payload = {
        "verified": False,
        "minimum_commit": MINIMUM_COMMIT,
        "workflow_commit": os.environ.get("GITHUB_SHA"),
        "repository": os.environ.get("GITHUB_REPOSITORY"),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
        "base_url": args.base_url,
        "started_at": started_at,
        "failed_at": utc_now(),
        "attempts": args.attempts,
        "checks": final_results,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(
        "PUBLIC GITHUB PAGES PROPAGATION NOT VERIFIED WITHIN POLLING WINDOW",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

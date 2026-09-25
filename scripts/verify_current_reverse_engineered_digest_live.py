#!/usr/bin/env python3
"""Attest and exactly read back the current redigest publication candidate.

This verifier is intentionally release-state aware. It proves that a successful
GitHub Pages run used the exact expected SHA and that the finite controlled
files are byte-identical to that checkout. It does not turn a prepared or
merged publication manifest into a LIVE_VERIFIED closeout.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_DEFAULT = "https://sbu001monterecco.github.io/por-derecho"
MANIFEST = "publication-manifests/alberto-meeting-point-multidirectional-criminal-first-20260827.json"

CONTROLLED_PATHS = (
    "CURRENT_REVERSE_ENGINEERED_DIGEST.md",
    "ops/CURRENT_REVERSE_ENGINEERED_DIGEST.json",
    "publication-manifests/unitary-repository-website-redigest-20260827.json",
    "archive/CURRENT_REVERSE_ENGINEERED_DIGEST_LIVE_CLOSEOUT_27AUG2026.md",
    "assets/data/alberto-meeting-point-357-multidirectional-evidence-v1.json",
    "assets/data/caepr-caret-alberto-meeting-point-357-v1.json",
    "assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json",
    "assets/data/caepr-caret-unitary-digest-v1.json",
    "assets/data/matter-identity-registry-v1.json",
    MANIFEST,
    "es/alberto-lopez-villarrubia-meeting-point-357-masa-activa/index.html",
    "en/alberto-lopez-villarrubia-meeting-point-357-active-estate/index.html",
)
SUPPORTING_PUBLIC_PATHS = (
    "es/registro-identidad-materia/index.html",
    "es/verificacion-caepr-caret-digest-unitario/index.html",
    "es/ingenieria-inversa-criminal-unitaria/index.html",
    "es/hipotesis-criminal-unitaria-2011-presente/index.html",
    "en/matter-identity-registry/index.html",
    "en/caepr-caret-unitary-digest/index.html",
    "en/unitary-criminal-reverse-engineering/index.html",
    "en/unitary-criminal-hypothesis-2011-present/index.html",
    "es/concurso-36-2012-juzgado-mercantil-1/index.html",
    "sitemap.xml",
    "sitemap-cgpj.xml",
    "sitemap-judicial-spine.xml",
    "sitemap-meeting-point.xml",
)

ALLOWED_STATES = {
    "PREPARED_PENDING_MERGE": "release_candidate_not_yet_verified_live",
    "REMOTE_SOURCE": "remote_source_not_merged",
    "PR_OPEN": "pull_request_open_not_merged",
    "CI_GREEN": "pull_request_checks_green_not_merged",
    "MERGED": "merged_awaiting_pages_deployment",
    "DEPLOYED": "deployed_awaiting_exact_live_closeout",
    "LIVE_VERIFIED": "live_verified",
    "DELETION_SAFE": "deletion_safe_live_verified",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=BASE_DEFAULT)
    parser.add_argument("--expected-sha", default=os.environ.get("GITHUB_SHA", ""))
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--token", default=os.environ.get("GH_TOKEN", ""))
    parser.add_argument("--attempts", type=int, default=48)
    parser.add_argument("--interval", type=float, default=10.0)
    parser.add_argument("--closeout-output")
    return parser.parse_args()


def request_bytes(url: str, token: str = "") -> bytes:
    headers = {
        "Accept": "application/vnd.github+json",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "User-Agent": "por-derecho-current-redigest-exact-readback/2",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"{url}: HTTP {response.status}")
        return response.read()


def attest_pages(repository: str, token: str, expected_sha: str, attempts: int, interval: float) -> dict[str, object]:
    if not repository or not token:
        raise RuntimeError("repository and GitHub token are required for Pages attestation")
    api = f"https://api.github.com/repos/{repository}/actions/runs?head_sha={expected_sha}&per_page=100"
    last_seen: list[dict[str, object]] = []
    for attempt in range(1, attempts + 1):
        payload = json.loads(request_bytes(api, token).decode("utf-8"))
        candidates = [
            run
            for run in payload.get("workflow_runs", [])
            if run.get("name") == "pages build and deployment"
            and run.get("path") == "dynamic/pages/pages-build-deployment"
            and run.get("head_sha") == expected_sha
        ]
        last_seen = [
            {
                "id": run.get("id"),
                "head_sha": run.get("head_sha"),
                "status": run.get("status"),
                "conclusion": run.get("conclusion"),
            }
            for run in candidates
        ]
        successful = next(
            (
                run
                for run in candidates
                if run.get("status") == "completed" and run.get("conclusion") == "success"
            ),
            None,
        )
        if successful:
            return {
                "run_id": successful.get("id"),
                "head_sha": successful.get("head_sha"),
                "conclusion": successful.get("conclusion"),
                "attempt": attempt,
            }
        if attempt < attempts:
            time.sleep(interval)
    raise RuntimeError(f"no successful exact-SHA Pages run; last_seen={last_seen!r}")


def path_to_route(path: str) -> str:
    if path.endswith("/index.html"):
        return "/" + path[: -len("index.html")]
    return "/" + path


def exact_readback(base_url: str, expected_sha: str, paths: list[str], attempts: int, interval: float) -> dict[str, str]:
    local = {path: (ROOT / path).read_bytes() for path in paths}
    base = base_url.rstrip("/")
    last_mismatches: list[dict[str, str]] = []
    for attempt in range(1, attempts + 1):
        hashes: dict[str, str] = {}
        mismatches: list[dict[str, str]] = []
        for path in paths:
            route = path_to_route(path)
            separator = "&" if "?" in route else "?"
            url = f"{base}{route}{separator}current_redigest={expected_sha}-{time.time_ns()}"
            try:
                remote = request_bytes(url)
            except Exception as exc:  # a pending Pages rollout is expected
                mismatches.append({"path": path, "error": str(exc)})
                continue
            local_hash = hashlib.sha256(local[path]).hexdigest()
            live_hash = hashlib.sha256(remote).hexdigest()
            hashes[route] = live_hash
            if remote != local[path]:
                mismatches.append(
                    {"path": path, "local_sha256": local_hash, "live_sha256": live_hash}
                )
        if not mismatches:
            return hashes
        last_mismatches = mismatches
        print(f"Exact readback attempt {attempt}/{attempts}: {len(mismatches)} mismatch(es)", flush=True)
        if attempt < attempts:
            time.sleep(interval)
    raise RuntimeError(f"exact-byte readback failed: {last_mismatches!r}")


def main() -> int:
    args = parse_args()
    if len(args.expected_sha) != 40 or any(character not in "0123456789abcdef" for character in args.expected_sha):
        raise SystemExit("--expected-sha must be a full lowercase 40-hex commit SHA")

    checkout_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if checkout_sha != args.expected_sha:
        raise SystemExit(
            f"checkout HEAD {checkout_sha!r} does not equal --expected-sha {args.expected_sha!r}"
        )

    manifest = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
    manifest_state = manifest.get("current_state")
    if manifest_state in {"DRAFT", "BLOCKED_RECOVERY"}:
        raise SystemExit("candidate manifest has not reached an authorised publication state")
    if manifest_state not in ALLOWED_STATES:
        raise SystemExit(f"candidate manifest has unknown publication state: {manifest_state!r}")
    if manifest.get("status") != ALLOWED_STATES[manifest_state]:
        raise SystemExit(f"candidate manifest status does not match {manifest_state}")
    if manifest.get("publication_authorized") is not True:
        raise SystemExit("candidate manifest does not record publication authorization")
    if manifest.get("communication_authorized") is not False or manifest.get("email_or_filing_action") != "HOLD_NOT_AUTHORISED":
        raise SystemExit("candidate manifest improperly opens communication or filing")

    expected_routes = manifest.get("expected_routes") or {}
    if set(expected_routes) != {"es", "en"}:
        raise SystemExit("candidate manifest expected_routes must contain exact es/en keys")
    route_paths = [
        path
        for language in ("es", "en")
        for path in expected_routes.get(language, [])
    ]
    if len(route_paths) != 20 or len(set(route_paths)) != 20:
        raise SystemExit("candidate manifest must declare exactly 20 unique hub/primary-route files")
    paths = list(dict.fromkeys((*CONTROLLED_PATHS, *route_paths, *SUPPORTING_PUBLIC_PATHS)))
    unsafe = [
        path
        for path in paths
        if not isinstance(path, str)
        or not path
        or path.startswith("/")
        or "#" in path
        or (ROOT not in (ROOT / path).resolve().parents)
    ]
    if unsafe:
        raise SystemExit(f"unsafe controlled paths: {unsafe!r}")
    missing = [path for path in paths if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit(f"controlled paths missing: {missing!r}")

    final_state = manifest_state in {"LIVE_VERIFIED", "DELETION_SAFE"}
    if final_state:
        recorded_closeout = manifest.get("closeout_control") or {}
        if (
            recorded_closeout.get("kind") != "SEPARATE_WORKFLOW_ARTIFACT"
            or recorded_closeout.get("result") != "LIVE_VERIFIED"
            or not isinstance(recorded_closeout.get("workflow_run_id"), int)
            or recorded_closeout.get("workflow_run_id", 0) <= 0
            or not isinstance(recorded_closeout.get("artifact_id"), int)
            or recorded_closeout.get("artifact_id", 0) <= 0
            or not recorded_closeout.get("artifact_name")
            or recorded_closeout.get("communication_authorized") is not False
            or recorded_closeout.get("filing_authorized") is not False
        ):
            raise SystemExit("final manifest lacks a valid separate recorded closeout control")
    if not args.closeout_output:
        raise SystemExit("--closeout-output is required for a separate deployment/readback control")

    deployment = attest_pages(
        args.repository,
        args.token,
        args.expected_sha,
        args.attempts,
        args.interval,
    )
    hashes = exact_readback(
        args.base_url,
        args.expected_sha,
        paths,
        args.attempts,
        args.interval,
    )
    reported_state = (
        "LIVE_VERIFIED"
        if final_state
        else "DEPLOYED_EXACT_READBACK_PASS_CLOSEOUT_REQUIRED"
    )
    run_id_raw = os.environ.get("GITHUB_RUN_ID", "")
    workflow_run_id = int(run_id_raw) if run_id_raw.isdigit() else None
    if final_state and not workflow_run_id:
        raise SystemExit("a positive GITHUB_RUN_ID is required for a final live closeout")
    closeout = {
        "schema": "por-derecho.deployment-readback-closeout.v1",
        "control_id": f"PD-ALV-MP357-DEPLOYMENT-CLOSEOUT-{args.expected_sha[:12]}",
        "publication_control_id": manifest.get("control_id"),
        "state": reported_state,
        "head_sha": args.expected_sha,
        "workflow_run_id": workflow_run_id,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "pages_attestation": deployment,
        "exact_readback": {
            "result": "PASS_EXACT_BYTES",
            "surface_count": len(paths),
            "sha256_by_route": hashes,
        },
        "communication_authorized": False,
        "filing_authorized": False,
        "email_or_filing_action": "HOLD_NOT_AUTHORISED",
    }
    closeout_path = Path(args.closeout_output)
    if not closeout_path.is_absolute():
        closeout_path = ROOT / closeout_path
    closeout_path = closeout_path.resolve()
    if ROOT not in closeout_path.parents:
        raise SystemExit("--closeout-output must remain inside the checkout")
    closeout_path.parent.mkdir(parents=True, exist_ok=True)
    closeout_path.write_text(
        json.dumps(closeout, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    recorded = json.loads(closeout_path.read_text(encoding="utf-8"))
    if recorded != closeout:
        raise SystemExit("separate closeout control failed its write/read integrity check")
    print(
        json.dumps(
            {
                "state": reported_state,
                "head_sha": args.expected_sha,
                "manifest_state": manifest_state,
                "pages": deployment,
                "exact_byte_surfaces": len(paths),
                "sha256_by_route": hashes,
                "separate_closeout_control": str(closeout_path.relative_to(ROOT)),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

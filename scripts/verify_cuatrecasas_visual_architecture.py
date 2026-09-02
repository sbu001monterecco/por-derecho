#!/usr/bin/env python3
"""Verify the Cuatrecasas bilingual visual architecture in source and on public Pages.

This verifier is deployment/governance evidence only. It confirms that the
localized atlases, renderer/loader chain and expected bilingual routes are
present. It does not establish any underlying factual allegation.
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

MINIMUM_VISUAL_MERGE = "2a26e4a201099633491ba24741c46baade1c1eea"
PROBE_ID = "pd-cuatrecasas-visual-architecture-live-20260902-v1"

ROUTES = [
    "en/cuatrecasas-sun-park/",
    "en/cuatrecasas-mandate-ric-continuity/",
    "en/cuatrecasas-dp748-civil-action/",
    "en/matkator-asset-rights-register/",
    "en/reverse-engineering-360-sun-park-chain/",
    "en/unitary-record/",
    "en/ric-private-equity-sun-park/",
    "en/ricpe-cnmv-dossier-2021/",
    "en/same-hotel-multiple-financial-lives/",
    "es/cuatrecasas-sun-park/",
    "es/cuatrecasas-mandato-continuidad-ric/",
    "es/cuatrecasas-dp748-accion-civil/",
    "es/registro-activos-derechos-matkator/",
    "es/ingenieria-inversa-360-cadena-sun-park/",
    "es/registro-unitario/",
    "es/ric-private-equity-sun-park/",
    "es/ricpe-cnmv-dossier-2021/",
    "es/mismo-hotel-multiples-vidas-financieras/",
]

FILE_CHECKS = [
    {
        "path": "deployment-probes/cuatrecasas-visual-architecture-20260902.json",
        "markers": [PROBE_ID, MINIMUM_VISUAL_MERGE],
        "kind": "deployment_probe",
    },
    {
        "path": "assets/cuatrecasas-visual-bridge-atlas-en-20260902.svg",
        "markers": [
            "Cuatrecasas visual bridge atlas — English",
            "What Step 4 can — and cannot —",
            "Aweswell is not the executed debtor.",
        ],
        "kind": "english_atlas",
    },
    {
        "path": "assets/cuatrecasas-visual-bridge-atlas-es-20260902.svg",
        "markers": [
            "Atlas visual de puentes Cuatrecasas — español",
            "Qué puede — y qué no puede —",
            "Aweswell no es la ejecutada.",
        ],
        "kind": "spanish_atlas",
    },
    {
        "path": "assets/cuatrecasas-visual-architecture-v2-20260902.js",
        "markers": [
            "data-cuatrecasas-visual-architecture-v2",
            "panels = ['A','B','C','D']",
            "cuatrecasas-visual-bridge-atlas-en-20260902.svg",
            "cuatrecasas-visual-bridge-atlas-es-20260902.svg",
            "What Step 4 can — and cannot — reach",
            "Qué puede — y qué no puede — alcanzar el Paso 4",
            "@media(max-width:820px)",
        ],
        "kind": "visual_renderer",
    },
    {
        "path": "assets/site.js",
        "markers": ["cuatrecasas-mandate-ric-inbound-20260902.js"],
        "kind": "site_loader",
    },
    {
        "path": "assets/cuatrecasas-mandate-ric-inbound-20260902.js",
        "markers": ["cuatrecasas-visual-bridges-across-pages-20260902.js"],
        "kind": "inbound_loader",
    },
    {
        "path": "assets/cuatrecasas-visual-bridges-across-pages-20260902.js",
        "markers": [
            "cuatrecasas-visual-architecture-v2-20260902.js",
            "finca 8,584",
            "does not replace sources or convert inferences or allegations into adjudicated facts",
        ],
        "kind": "cross_page_loader",
    },
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_check(root: Path) -> tuple[bool, list[dict[str, Any]]]:
    results: list[dict[str, Any]] = []
    all_ok = True

    for item in FILE_CHECKS:
        path = root / item["path"]
        record: dict[str, Any] = {
            "kind": item["kind"],
            "path": item["path"],
            "required_markers": item["markers"],
        }
        if not path.is_file():
            record.update(ok=False, error="missing file")
        else:
            data = path.read_bytes()
            text = data.decode("utf-8", errors="replace")
            missing = [marker for marker in item["markers"] if marker not in text]
            record.update(
                ok=not missing,
                bytes=len(data),
                sha256=sha256_bytes(data),
                missing_markers=missing,
            )
        if not record["ok"]:
            all_ok = False
        results.append(record)

    for route in ROUTES:
        path = root / route / "index.html"
        ok = path.is_file()
        record = {
            "kind": "route_source",
            "path": str(path.relative_to(root)),
            "ok": ok,
        }
        if ok:
            data = path.read_bytes()
            record["bytes"] = len(data)
            record["sha256"] = sha256_bytes(data)
        else:
            record["error"] = "missing route index.html"
            all_ok = False
        results.append(record)

    return all_ok, results


def fetch(url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Por-Derecho-Cuatrecasas-Visual-Live-Check/1.0",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
            "Accept": "text/html,application/json,image/svg+xml,text/javascript,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read()
        text = body.decode("utf-8", errors="replace")
        return {
            "status": response.status,
            "final_url": response.geturl(),
            "bytes": len(body),
            "sha256": sha256_bytes(body),
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified"),
            "text": text,
        }


def live_check_once(base_url: str, attempt: int, timeout: int) -> tuple[bool, list[dict[str, Any]]]:
    results: list[dict[str, Any]] = []
    all_ok = True
    nonce = f"{int(time.time())}-{attempt}"

    for item in FILE_CHECKS:
        url = urllib.parse.urljoin(base_url.rstrip("/") + "/", item["path"])
        checked_url = f"{url}?pd_visual_probe={nonce}"
        record: dict[str, Any] = {
            "kind": item["kind"],
            "path": item["path"],
            "url": url,
            "required_markers": item["markers"],
            "checked_at": utc_now(),
        }
        try:
            response = fetch(checked_url, timeout)
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

    for route in ROUTES:
        url = urllib.parse.urljoin(base_url.rstrip("/") + "/", route)
        checked_url = f"{url}?pd_visual_probe={nonce}"
        record = {
            "kind": "public_route",
            "path": route,
            "url": url,
            "checked_at": utc_now(),
        }
        try:
            response = fetch(checked_url, timeout)
            record.update({key: value for key, value in response.items() if key != "text"})
            record["ok"] = response["status"] == 200 and response["bytes"] > 0
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            record["ok"] = False
            record["error"] = f"{type(exc).__name__}: {exc}"
        if not record["ok"]:
            all_ok = False
        results.append(record)

    return all_ok, results


def write_output(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["source", "live"], required=True)
    parser.add_argument("--source-root", default=".")
    parser.add_argument(
        "--base-url",
        default="https://sbu001monterecco.github.io/por-derecho/",
    )
    parser.add_argument("--attempts", type=int, default=72)
    parser.add_argument("--interval", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument(
        "--output",
        default="artifacts/cuatrecasas-visual-architecture/verification.json",
    )
    args = parser.parse_args()

    output = Path(args.output)
    started_at = utc_now()

    if args.mode == "source":
        ok, results = source_check(Path(args.source_root))
        payload = {
            "verified": ok,
            "mode": "source",
            "minimum_visual_merge": MINIMUM_VISUAL_MERGE,
            "probe_id": PROBE_ID,
            "workflow_commit": os.environ.get("GITHUB_SHA"),
            "started_at": started_at,
            "completed_at": utc_now(),
            "checks": results,
        }
        write_output(output, payload)
        print("CUATRECASAS VISUAL SOURCE CHECK " + ("PASSED" if ok else "FAILED"))
        return 0 if ok else 1

    final_results: list[dict[str, Any]] = []
    for attempt in range(1, args.attempts + 1):
        ok, results = live_check_once(args.base_url, attempt, args.timeout)
        final_results = results
        passed = sum(1 for item in results if item.get("ok"))
        print(f"Attempt {attempt}/{args.attempts}: {passed}/{len(results)} live checks OK", flush=True)
        if ok:
            payload = {
                "verified": True,
                "mode": "live",
                "verification_basis": (
                    "The public Pages host serves the post-PR-1365 deployment probe, localized EN/ES atlases, "
                    "the renderer/loader chain and every expected bilingual route. This verifies deployment "
                    "availability only; underlying evidential propositions remain source-controlled."
                ),
                "minimum_visual_merge": MINIMUM_VISUAL_MERGE,
                "probe_id": PROBE_ID,
                "workflow_commit": os.environ.get("GITHUB_SHA"),
                "repository": os.environ.get("GITHUB_REPOSITORY"),
                "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
                "base_url": args.base_url,
                "started_at": started_at,
                "verified_at": utc_now(),
                "attempt": attempt,
                "checks": results,
            }
            write_output(output, payload)
            print("PUBLIC CUATRECASAS VISUAL ARCHITECTURE VERIFIED", flush=True)
            return 0
        if attempt < args.attempts:
            time.sleep(args.interval)

    payload = {
        "verified": False,
        "mode": "live",
        "minimum_visual_merge": MINIMUM_VISUAL_MERGE,
        "probe_id": PROBE_ID,
        "workflow_commit": os.environ.get("GITHUB_SHA"),
        "repository": os.environ.get("GITHUB_REPOSITORY"),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
        "base_url": args.base_url,
        "started_at": started_at,
        "failed_at": utc_now(),
        "attempts": args.attempts,
        "checks": final_results,
    }
    write_output(output, payload)
    print("PUBLIC CUATRECASAS VISUAL ARCHITECTURE NOT VERIFIED", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

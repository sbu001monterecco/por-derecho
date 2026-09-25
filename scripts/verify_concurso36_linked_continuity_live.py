#!/usr/bin/env python3
"""Verify the linked-continuity bilingual routes and machine register exactly.

This is a deployment/readback control. It does not certify the court-file
denominator, close any P0/P1 evidence gate or authorise external action.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = "https://sbu001monterecco.github.io/por-derecho/"
CONTROL = "PD-C36-LINKED-CONTINUITY-20260829-01"
TARGETS = [
    {
        "kind": "route_en",
        "source_path": "en/insolvency-36-2012-continuity-control/index.html",
        "url_path": "en/insolvency-36-2012-continuity-control/",
    },
    {
        "kind": "route_es",
        "source_path": "es/concurso-36-2012-control-continuidad/index.html",
        "url_path": "es/concurso-36-2012-control-continuidad/",
    },
    {
        "kind": "machine_register",
        "source_path": "assets/data/concurso36-linked-continuity-20260829-v1.json",
        "url_path": "assets/data/concurso36-linked-continuity-20260829-v1.json",
    },
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_targets() -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    for item in TARGETS:
        source = ROOT / item["source_path"]
        if not source.is_file():
            raise FileNotFoundError(f"missing source surface: {item['source_path']}")
        if item["url_path"] in seen_urls:
            raise ValueError(f"duplicate public target: {item['url_path']}")
        seen_urls.add(item["url_path"])
        body = source.read_bytes()
        result.append({
            **item,
            "expected_bytes": len(body),
            "expected_sha256": sha256_bytes(body),
        })
    if len(result) != 3 or {item["kind"] for item in result} != {"route_en", "route_es", "machine_register"}:
        raise ValueError("linked-continuity target inventory drifted")
    return result


def semantic_control() -> dict[str, Any]:
    register = json.loads((ROOT / TARGETS[2]["source_path"]).read_text(encoding="utf-8"))
    en_page = (ROOT / TARGETS[0]["source_path"]).read_text(encoding="utf-8")
    es_page = (ROOT / TARGETS[1]["source_path"]).read_text(encoding="utf-8")
    gates = register.get("open_evidence_gates") or {}
    checks = {
        "control_id": register.get("control_id") == CONTROL,
        "release_is_no_new_evidence": register.get("release_type")
        == "continuity_reconciliation_no_new_evidence_promotion",
        "nine_p0_gates_open": len(gates.get("P0") or []) == 9,
        "two_p1_gates_open": len(gates.get("P1") or []) == 2,
        "external_action_not_authorized": register.get("external_action_authorized") is False,
        "english_truth_heading": "Continuation control reconciled; evidential closure remains open." in en_page,
        "spanish_truth_heading": "Control de continuidad conciliado; el cierre probatorio sigue abierto." in es_page,
        "english_state_panel": 'data-c36-continuity-truth="20260829"' in en_page,
        "spanish_state_panel": 'data-c36-continuity-truth="20260829"' in es_page,
    }
    return {"ok": all(checks.values()), "checks": checks}


def fetch_target(base_url: str, target: dict[str, Any], timeout: int, nonce: str) -> dict[str, Any]:
    url = urllib.parse.urljoin(base_url.rstrip("/") + "/", target["url_path"])
    request = urllib.request.Request(
        f"{url}{'&' if '?' in url else '?'}c36_linked_live={nonce}",
        headers={
            "User-Agent": "Por-Derecho-Concurso36-Linked-Continuity-Live/1.0",
            "Accept": "*/*",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )
    record = {key: value for key, value in target.items() if key != "url_path"}
    record["url"] = url
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            record.update({
                "status": int(response.status),
                "actual_bytes": len(body),
                "actual_sha256": sha256_bytes(body),
                "content_type": response.headers.get("Content-Type"),
            })
            record["ok"] = (
                record["status"] == 200
                and record["actual_bytes"] == record["expected_bytes"]
                and record["actual_sha256"] == record["expected_sha256"]
            )
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as exc:
        record["ok"] = False
        record["error"] = f"{type(exc).__name__}: {exc}"
    return record


def one_pass(base_url: str, targets: list[dict[str, Any]], timeout: int, attempt: int) -> dict[str, Any]:
    nonce = f"{int(time.time())}-{attempt}"
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        records = list(executor.map(
            lambda target: fetch_target(base_url, target, timeout, nonce),
            targets,
        ))
    records.sort(key=lambda item: item["source_path"])
    semantic = semantic_control()
    return {
        "ok": semantic["ok"] and all(record.get("ok") for record in records),
        "attempt": attempt,
        "verified_at": utc_now(),
        "base_url": base_url,
        "surface_count": len(records),
        "semantic": semantic,
        "records": records,
        "evidential_effect": "NONE__DEPLOYMENT_READBACK_ONLY",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE)
    parser.add_argument("--attempts", type=int, default=1)
    parser.add_argument("--interval", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument(
        "--output",
        default="artifacts/concurso36-linked-continuity-live/result.json",
    )
    args = parser.parse_args()

    targets = build_targets()
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    result: dict[str, Any] = {}

    for attempt in range(1, max(1, args.attempts) + 1):
        result = one_pass(args.base_url, targets, args.timeout, attempt)
        failed = [record["source_path"] for record in result["records"] if not record.get("ok")]
        exact = result["surface_count"] - len(failed)
        print(
            f"attempt {attempt}/{max(1, args.attempts)}: "
            f"{exact}/{result['surface_count']} byte-exact surfaces; "
            f"semantic={'PASS' if result['semantic']['ok'] else 'FAIL'}",
            flush=True,
        )
        if result["ok"]:
            output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print("CONCURSO 36/2012 LINKED-CONTINUITY LIVE READBACK: PASS")
            return 0
        if failed:
            print("not yet exact: " + ", ".join(failed), flush=True)
        if attempt < max(1, args.attempts):
            time.sleep(max(1, args.interval))

    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("CONCURSO 36/2012 LINKED-CONTINUITY LIVE READBACK: FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Verify the deployed PwC / Carlos Saavedra package byte-for-byte."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "https://sbu001monterecco.github.io/por-derecho/"

RESOURCES = [
    {
        "key": "es_page",
        "url_path": "es/pwc-canarias-carlos-saavedra-sun-park/",
        "source_path": "es/pwc-canarias-carlos-saavedra-sun-park/index.html",
        "markers": [
            "32/35",
            "PARCIAL — NO TODO ES^",
            "12–16 may 2016",
            "6–10 jun 2016",
            "PD-SP-I-0042",
            "carlos-saavedra--linkedin-profile--20260901.jpg",
        ],
    },
    {
        "key": "en_page",
        "url_path": "en/pwc-canarias-carlos-saavedra-sun-park/",
        "source_path": "en/pwc-canarias-carlos-saavedra-sun-park/index.html",
        "markers": [
            "32/35",
            "PARTIAL — NOT ALL IS^",
            "12–16 May 2016",
            "6–10 Jun 2016",
            "PD-SP-I-0042",
            "carlos-saavedra--linkedin-profile--20260901.jpg",
        ],
    },
    {
        "key": "portrait",
        "url_path": "assets/actors/carlos-saavedra--linkedin-profile--20260901.jpg",
        "source_path": "assets/actors/carlos-saavedra--linkedin-profile--20260901.jpg",
        "expected_bytes": 143942,
    },
    {
        "key": "pwc_ledger",
        "url_path": "assets/data/caepr-caret-pwc-carlos-saavedra-first-hop-v1.json",
        "source_path": "assets/data/caepr-caret-pwc-carlos-saavedra-first-hop-v1.json",
        "json_control": "pwc",
    },
    {
        "key": "identity_page",
        "url_path": "es/registro-identidad-materia/",
        "source_path": "es/registro-identidad-materia/index.html",
        "markers": ['data-static-registry-counts="339-160-83-11-42-43"'],
    },
    {
        "key": "unitary_page",
        "url_path": "en/caepr-caret-unitary-digest/",
        "source_path": "en/caepr-caret-unitary-digest/index.html",
        "markers": ["21/24", "three explicit exceptions", "Matkator, S.L.U."],
    },
    {
        "key": "unitary_ledger",
        "url_path": "assets/data/caepr-caret-unitary-digest-v1.json",
        "source_path": "assets/data/caepr-caret-unitary-digest-v1.json",
        "json_control": "unitary",
    },
    {
        "key": "identity_registry",
        "url_path": "assets/data/matter-identity-registry-v1.json",
        "source_path": "assets/data/matter-identity-registry-v1.json",
        "json_control": "identity",
    },
    {
        "key": "authority_graph",
        "url_path": "assets/data/community-acta-authority-interconnectivity-v1.json",
        "source_path": "assets/data/community-acta-authority-interconnectivity-v1.json",
        "json_control": "authority",
    },
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_json(kind: str, data: dict) -> dict[str, bool]:
    if kind == "pwc":
        counts = data.get("counts", {})
        return {
            "status_partial": data.get("status") == "PARTIAL_NOT_ALL_IS",
            "eligible_35": counts.get("identity_eligible") == 35,
            "confirmed_32": counts.get("identity_confirmed") == 32,
            "pending_3": counts.get("identity_pending") == 3,
            "events_20": counts.get("events_registered") == 20,
            "evidence_19": counts.get("evidence_records_registered") == 19,
            "visual_1": counts.get("visual_assets_registered") == 1,
            "verdict_partial": data.get("verdict", "").endswith("PARTIAL — NOT ALL IS^"),
        }
    if kind == "unitary":
        result = data.get("result", {})
        addendum = data.get("identity_reconciliation_addendum", {})
        return {
            "historical_control_date_preserved": data.get("control_date") == "2026-08-31",
            "reconciliation_addendum_date": addendum.get("date") == "2026-09-01",
            "denominator_24": result.get("denominator") == 24,
            "confirmed_21": result.get("confirmed") == 21,
            "pending_3": result.get("pending") == 3,
            "coverage_21_24": result.get("coverage_fraction") == "21/24",
        }
    if kind == "identity":
        return {
            "registry_id": data.get("registry_id") == "PD-SP-IDENTITY-REGISTRY-001",
            "counts": data.get("counts")
            == {
                "total": 339,
                "PERSON": 160,
                "ORGANISATION": 83,
                "STRUCTURE": 11,
                "INSTITUTION": 42,
                "PROCEEDING": 43,
            },
        }
    if kind == "authority":
        coverage = data.get("coverage", {})
        return {
            "acta_packages_20": coverage.get("public_acta_packages") == 20,
            "authority_files_49": coverage.get("public_authority_files") == 49,
            "authority_groups_6": coverage.get("authority_groups") == 6,
            "evidentiary_axes_7": coverage.get("evidentiary_axes") == 7,
            "communications_19": coverage.get("public_authority_communication_events") == 19,
        }
    return {"known_json_control": False}


def fetch(url: str) -> tuple[int, bytes, dict[str, str]]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Por-Derecho-PwC-Carlos-Saavedra-Live-Verify/1.0",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.status, response.read(), dict(response.headers)


def verify_once(base_url: str, nonce: str, attempt: int) -> dict:
    checks = []
    healthy = True
    for spec in RESOURCES:
        source = ROOT / spec["source_path"]
        expected = source.read_bytes()
        url = urllib.parse.urljoin(base_url, spec["url_path"])
        separator = "&" if "?" in url else "?"
        row = {
            "key": spec["key"],
            "url": url,
            "source_path": spec["source_path"],
            "attempt": attempt,
            "expected_bytes": len(expected),
            "expected_sha256": sha256(expected),
        }
        try:
            status, body, headers = fetch(f"{url}{separator}verify={nonce}-{attempt}")
            text = body.decode("utf-8", errors="replace") if spec.get("markers") else ""
            missing = [marker for marker in spec.get("markers", []) if marker not in text]
            json_checks: dict[str, bool] = {}
            if spec.get("json_control"):
                json_checks = validate_json(spec["json_control"], json.loads(body.decode("utf-8")))
            row.update(
                {
                    "status": status,
                    "bytes": len(body),
                    "sha256": sha256(body),
                    "content_type": headers.get("Content-Type"),
                    "etag": headers.get("ETag"),
                    "last_modified": headers.get("Last-Modified"),
                    "missing_markers": missing,
                    "json_checks": json_checks,
                }
            )
            row["ok"] = (
                status == 200
                and len(body) == len(expected)
                and row["sha256"] == row["expected_sha256"]
                and not missing
                and all(json_checks.values())
                and (spec.get("expected_bytes") is None or len(body) == spec["expected_bytes"])
            )
        except Exception as exc:
            row.update({"ok": False, "error": f"{type(exc).__name__}: {exc}"})
        healthy = healthy and row["ok"]
        checks.append(row)
    return {
        "schema": "por-derecho.pwc-carlos-saavedra-live-verification.v1",
        "checked_at": utc_now(),
        "github_sha": os.environ.get("GITHUB_SHA"),
        "base_url": base_url,
        "attempt": attempt,
        "healthy": healthy,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--attempts", type=int, default=1)
    parser.add_argument("--delay", type=float, default=15.0)
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.attempts < 1:
        parser.error("--attempts must be at least 1")

    base_url = args.base_url.rstrip("/") + "/"
    nonce = os.environ.get("GITHUB_SHA") or str(int(time.time()))
    result = None
    for attempt in range(1, args.attempts + 1):
        result = verify_once(base_url, nonce, attempt)
        if result["healthy"]:
            break
        if attempt < args.attempts:
            time.sleep(args.delay)

    assert result is not None
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(
        "PWC / CARLOS SAAVEDRA LIVE VERIFICATION: "
        + ("PASS" if result["healthy"] else "FAIL")
    )
    return 0 if result["healthy"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

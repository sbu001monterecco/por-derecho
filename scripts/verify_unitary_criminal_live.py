#!/usr/bin/env python3
"""External production verification for the unitary criminal reverse-engineering publication."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_BASE = "https://sbu001monterecco.github.io/por-derecho/"
MARKER = "unitary-criminal-reverse-engineering-20260820"
CHECKS = [
    {
        "path": "es/ingenieria-inversa-criminal-unitaria/",
        "kind": "unitary_criminal_es",
        "markers": [MARKER, "¿Existió una sola empresa continuada", "Los quince puntos más fuertes"],
        "min_bytes": 5000,
    },
    {
        "path": "en/unitary-criminal-reverse-engineering/",
        "kind": "unitary_criminal_en",
        "markers": [MARKER, "Was there one continuing enterprise", "The fifteen strongest points"],
        "min_bytes": 5000,
    },
    {
        "path": "es/retracto-credito-litigioso-1041-2017/",
        "kind": "pp1041_es",
        "markers": [MARKER, "Se presentó un desistimiento en nombre de LPB"],
        "min_bytes": 5000,
    },
    {
        "path": "en/litigious-credit-retracto-1041-2017/",
        "kind": "pp1041_en",
        "markers": [MARKER, "A withdrawal was filed in LPB"],
        "min_bytes": 5000,
    },
    {
        "path": "es/administrador-concursal-puerta-credito-titulo/",
        "kind": "administrator_gate_es",
        "markers": [MARKER, "Se presentó un desistimiento en nombre de LPB"],
        "min_bytes": 5000,
    },
    {
        "path": "en/insolvency-administrator-credit-to-title-gatekeeper/",
        "kind": "administrator_gate_en",
        "markers": [MARKER, "A withdrawal was filed in LPB"],
        "min_bytes": 5000,
    },
    {
        "path": "assets/unitary-criminal-reverse-engineering-20260820.js",
        "kind": "unitary_criminal_gateway",
        "markers": [MARKER, "unitaryCriminalGateway"],
        "min_bytes": 500,
    },
    {
        "path": "sitemap-criminal-engineering.xml",
        "kind": "unitary_criminal_sitemap",
        "markers": ["ingenieria-inversa-criminal-unitaria", "unitary-criminal-reverse-engineering"],
        "min_bytes": 300,
    },
]


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def fetch(url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Por-Derecho-Unitary-Criminal-Live-Verification/1.1",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
            "Accept": "text/html,application/xml,text/javascript,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read()
        return {
            "status": response.status,
            "final_url": response.geturl(),
            "bytes": len(body),
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified"),
            "sha256": hashlib.sha256(body).hexdigest(),
            "text": body.decode("utf-8", errors="replace"),
        }


def run_once(base_url: str, timeout: int, attempt: int) -> tuple[bool, list[dict[str, Any]]]:
    ok_all = True
    records: list[dict[str, Any]] = []
    nonce = f"{int(time.time())}-{attempt}"
    for check in CHECKS:
        url = urllib.parse.urljoin(base_url.rstrip("/") + "/", check["path"])
        checked_url = f"{url}{'&' if '?' in url else '?'}unitary_criminal_verify={nonce}"
        record: dict[str, Any] = {
            "kind": check["kind"],
            "path": check["path"],
            "url": url,
            "checked_at": now_utc(),
            "required_markers": check["markers"],
        }
        try:
            response = fetch(checked_url, timeout)
            missing = [marker for marker in check["markers"] if marker not in response["text"]]
            record.update({key: value for key, value in response.items() if key != "text"})
            record["missing_markers"] = missing
            record["ok"] = (
                response["status"] == 200
                and response["bytes"] >= check["min_bytes"]
                and not missing
            )
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            record["ok"] = False
            record["error"] = f"{type(exc).__name__}: {exc}"
        ok_all = ok_all and bool(record["ok"])
        records.append(record)
    return ok_all, records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE)
    parser.add_argument("--attempts", type=int, default=4)
    parser.add_argument("--interval", type=int, default=20)
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument("--output", default="artifacts/unitary-criminal-live/latest.json")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    started_at = now_utc()
    last_records: list[dict[str, Any]] = []

    for attempt in range(1, max(1, args.attempts) + 1):
        ok, records = run_once(args.base_url, args.timeout, attempt)
        last_records = records
        print(", ".join(f"{r['kind']}={'OK' if r['ok'] else 'FAIL'}" for r in records), flush=True)
        if ok:
            output.write_text(
                json.dumps(
                    {
                        "ok": True,
                        "marker": MARKER,
                        "base_url": args.base_url,
                        "started_at": started_at,
                        "verified_at": now_utc(),
                        "attempt": attempt,
                        "checks": records,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            print("UNITARY CRIMINAL LIVE VERIFICATION: PASS")
            return 0
        if attempt < args.attempts:
            time.sleep(max(1, args.interval))

    output.write_text(
        json.dumps(
            {
                "ok": False,
                "marker": MARKER,
                "base_url": args.base_url,
                "started_at": started_at,
                "failed_at": now_utc(),
                "attempts": args.attempts,
                "checks": last_records,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("UNITARY CRIMINAL LIVE VERIFICATION: FAIL", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

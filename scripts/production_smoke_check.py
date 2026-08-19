#!/usr/bin/env python3
"""External smoke test for the Por Derecho production GitHub Pages host."""
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
CHECKS = [
    {"path": "deployment-probes/mission-critical-hardening-20260818.json",
     "markers": ["psr-mission-critical-hardening-20260818-v1"], "kind": "hardening_probe", "min_bytes": 80},
    {"path": "es/", "markers": ["Project Sun Rock", "resumen-60-segundos"],
     "kind": "homepage_es", "min_bytes": 1000},
    {"path": "en/", "markers": ["Project Sun Rock", "sixty-second-summary"],
     "kind": "homepage_en", "min_bytes": 1000},
    {"path": "es/ric-private-equity-sun-park/", "markers": ["RIC Private Equity", "Registro unitario"],
     "kind": "ricpe_es", "min_bytes": 1000},
    {"path": "es/cnmv-ricpe-verificacion/", "markers": ["CNMV / RICPE", "EXPEDIENTE ABIERTO"],
     "kind": "cnmv_es", "min_bytes": 1000},
    {"path": "es/rsm/nnr4-1025c2f66/", "markers": ["NNR4-1025C2F66", "Perímetro profesional y preservación", "18 ago 2026"],
     "kind": "rsm_es", "min_bytes": 1000},
    {"path": "en/rsm/nnr4-1025c2f66/", "markers": ["NNR4-1025C2F66", "Professional perimeter and preservation", "18 Aug 2026"],
     "kind": "rsm_en", "min_bytes": 1000},
    {"path": "es/fundacion-por-derecho/palacete-por-derecho/",
     "markers": [
         "Propuesta de futuro Palacete Por Derecho",
         "palacete-san-bernardo-historica-marco.webp",
         "palacete-san-bernardo-historica-detalle.webp",
         "palacete-por-derecho-vision-01.webp",
         "palacete-por-derecho-vision-02.webp",
         "Memoria visual",
         "Visualización conceptual",
     ],
     "kind": "palacete_page", "min_bytes": 5000},
    {"path": "assets/palacete-san-bernardo-historica-marco.webp",
     "markers": ["RIFF", "WEBP"], "kind": "palacete_history_frame", "min_bytes": 5000},
    {"path": "assets/palacete-san-bernardo-historica-detalle.webp",
     "markers": ["RIFF", "WEBP"], "kind": "palacete_history_detail", "min_bytes": 5000},
    {"path": "assets/palacete-por-derecho-vision-01.webp",
     "markers": ["RIFF", "WEBP"], "kind": "palacete_vision_01", "min_bytes": 5000},
    {"path": "assets/palacete-por-derecho-vision-02.webp",
     "markers": ["RIFF", "WEBP"], "kind": "palacete_vision_02", "min_bytes": 5000},
    {"path": "assets/site.js", "markers": ["site-base-20260819.js", "pd-history-visuals"],
     "kind": "global_loader", "min_bytes": 1000},
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def fetch(url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={
        "User-Agent": "Por-Derecho-Mission-Critical-Smoke/1.0",
        "Cache-Control": "no-cache, no-store, max-age=0",
        "Pragma": "no-cache",
        "Accept": "text/html,application/json,text/javascript,image/webp,*/*;q=0.8",
    })
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read()
        return {
            "status": response.status,
            "final_url": response.geturl(),
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified"),
            "server": response.headers.get("Server"),
            "content_type": response.headers.get("Content-Type"),
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "text": body.decode("latin-1", errors="replace"),
        }


def one_pass(base_url: str, timeout: int, attempt: int) -> tuple[bool, list[dict[str, Any]]]:
    all_ok = True
    records: list[dict[str, Any]] = []
    nonce = f"{int(time.time())}-{attempt}"
    for check in CHECKS:
        url = urllib.parse.urljoin(base_url.rstrip("/") + "/", check["path"])
        checked_url = f"{url}{'&' if '?' in url else '?'}psr_smoke={nonce}"
        record: dict[str, Any] = {
            "kind": check["kind"],
            "path": check["path"],
            "url": url,
            "checked_at": utc_now(),
            "required_markers": check["markers"],
        }
        try:
            response = fetch(checked_url, timeout)
            missing = [m for m in check["markers"] if m not in response["text"]]
            record.update({k: v for k, v in response.items() if k != "text"})
            record["missing_markers"] = missing
            record["ok"] = (
                response["status"] == 200
                and response["bytes"] >= check["min_bytes"]
                and not missing
            )
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            record["ok"] = False
            record["error"] = f"{type(exc).__name__}: {exc}"
        if not record["ok"]:
            all_ok = False
        records.append(record)
    return all_ok, records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE)
    parser.add_argument("--attempts", type=int, default=1)
    parser.add_argument("--interval", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--output", default="artifacts/production-smoke/latest.json")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    started_at = utc_now()
    final_records: list[dict[str, Any]] = []

    for attempt in range(1, max(1, args.attempts) + 1):
        ok, records = one_pass(args.base_url, args.timeout, attempt)
        final_records = records
        print(", ".join(f"{r['kind']}={'OK' if r['ok'] else 'FAIL'}" for r in records), flush=True)
        if ok:
            payload = {
                "ok": True,
                "base_url": args.base_url,
                "started_at": started_at,
                "verified_at": utc_now(),
                "attempt": attempt,
                "checks": records,
            }
            output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print("PRODUCTION SMOKE CHECK: PASS")
            return 0
        if attempt < args.attempts:
            time.sleep(max(1, args.interval))

    output.write_text(json.dumps({
        "ok": False,
        "base_url": args.base_url,
        "started_at": started_at,
        "failed_at": utc_now(),
        "attempts": args.attempts,
        "checks": final_records,
    }, indent=2), encoding="utf-8")
    print("PRODUCTION SMOKE CHECK: FAIL", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

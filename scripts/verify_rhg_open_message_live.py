#!/usr/bin/env python3
"""Poll the public Por Derecho host for the RHG/open-message publication."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

BASE = "https://sbu001monterecco.github.io/por-derecho/"
CHECKS = [
    {
        "path": "es/acosta-matos-perimetro/mensaje-abierto-colaborador-rhg/",
        "markers": [
            "Radisson Blu Lanzarote: aviso central",
            "Correo enviado · recepción, enrutamiento y revisión pendientes",
            "Mensaje abierto parcialmente anonimizado",
            "El silencio no será presentado como admisión",
            "mHn9IJU0qI4",
        ],
        "min_bytes": 9000,
    },
    {
        "path": "en/acosta-matos-perimeter/open-message-rhg-collaborator/",
        "markers": [
            "Radisson Blu Lanzarote: central notice",
            "Email sent · receipt, routing and review pending",
            "Partly anonymised open message",
            "Silence will not be represented as an admission",
            "mHn9IJU0qI4",
        ],
        "min_bytes": 9000,
    },
    {
        "path": "assets/evidence/rhg-open-message-20aug2026/pwc-five-actors-plus-ac-2016-knowledge-checkpoint-EN.svg",
        "markers": [
            "PWC · 2016 KNOWLEDGE CHECKPOINT",
            "FIVE PRIVATE ACTORS",
            "EVIDENTIAL BOUNDARY",
        ],
        "min_bytes": 3000,
    },
    {
        "path": "assets/evidence/rhg-open-message-20aug2026/san-telmo-ricpe-sun-park-stamp-v1-EN.svg",
        "markers": [
            "SAN TELMO · RICPE · SUN PARK",
            "INSOLVENCY LIFE",
            "DOCUMENTARY QUESTION",
        ],
        "min_bytes": 3000,
    },
    {
        "path": "sitemap-rhg-open-message.xml",
        "markers": [
            "es/acosta-matos-perimetro/mensaje-abierto-colaborador-rhg/",
            "en/acosta-matos-perimeter/open-message-rhg-collaborator/",
        ],
        "min_bytes": 700,
    },
    {
        "path": "robots.txt",
        "markers": ["sitemap-rhg-open-message.xml"],
        "min_bytes": 1000,
    },
]


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def fetch(url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Por-Derecho-RHG-Open-Message-Live-Verifier/1.0",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
            "Accept": "text/html,application/xml,image/svg+xml,text/plain,*/*;q=0.8",
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


def one_pass(base: str, timeout: int, attempt: int) -> tuple[bool, list[dict[str, Any]]]:
    nonce = f"{int(time.time())}-{attempt}"
    overall = True
    records: list[dict[str, Any]] = []
    for check in CHECKS:
        url = urllib.parse.urljoin(base.rstrip("/") + "/", check["path"])
        checked = f"{url}{'&' if '?' in url else '?'}pd_rhg={nonce}"
        record: dict[str, Any] = {
            "path": check["path"],
            "url": url,
            "checked_at": now(),
            "required_markers": check["markers"],
            "minimum_bytes": check["min_bytes"],
        }
        try:
            response = fetch(checked, timeout)
            missing = [marker for marker in check["markers"] if marker not in response["text"]]
            record.update({key: value for key, value in response.items() if key != "text"})
            record["missing_markers"] = missing
            record["ok"] = (
                response["status"] == 200
                and response["bytes"] >= check["min_bytes"]
                and not missing
            )
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as exc:
            record["ok"] = False
            record["error"] = f"{type(exc).__name__}: {exc}"
        overall = overall and bool(record["ok"])
        records.append(record)
    return overall, records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=BASE)
    parser.add_argument("--attempts", type=int, default=36)
    parser.add_argument("--interval", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--output", default="artifacts/rhg-open-message-live/verification.json")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    started = now()
    final_records: list[dict[str, Any]] = []

    for attempt in range(1, max(1, args.attempts) + 1):
        ok, records = one_pass(args.base_url, args.timeout, attempt)
        final_records = records
        print(", ".join(f"{r['path']}={'OK' if r['ok'] else 'FAIL'}" for r in records), flush=True)
        if ok:
            output.write_text(
                json.dumps(
                    {
                        "ok": True,
                        "base_url": args.base_url,
                        "started_at": started,
                        "verified_at": now(),
                        "attempt": attempt,
                        "checks": records,
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            print("RHG OPEN MESSAGE LIVE VERIFICATION: PASS")
            return 0
        if attempt < args.attempts:
            time.sleep(max(1, args.interval))

    output.write_text(
        json.dumps(
            {
                "ok": False,
                "base_url": args.base_url,
                "started_at": started,
                "failed_at": now(),
                "attempts": args.attempts,
                "checks": final_records,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print("RHG OPEN MESSAGE LIVE VERIFICATION: FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

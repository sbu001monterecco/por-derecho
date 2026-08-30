#!/usr/bin/env python3
"""Verify the 21 August 2026 asset-recovery, CGPJ and Por Derecho routes on production."""
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

CHECKS: list[dict[str, Any]] = [
    {
        "path": "en/asset-recovery-intervention-confiscation/",
        "kind": "asset_recovery_en",
        "markers": [
            "PRESERVE FIRST · TRACE THE VALUE · DECIDE THE MERITS AFTER",
            "The remedy must not arrive after the value has gone.",
            "Follow the value, not the label.",
        ],
        "min_bytes": 8000,
    },
    {
        "path": "es/recuperacion-activos-intervencion-decomiso/",
        "kind": "asset_recovery_es",
        "markers": [
            "PRESERVAR PRIMERO · SEGUIR EL VALOR · DECIDIR EL FONDO DESPUÉS",
            "El remedio no puede llegar cuando el valor ya se ha ido.",
            "Seguir el valor, no la etiqueta.",
        ],
        "min_bytes": 8000,
    },
    {
        "path": "en/cgpj-public-prosecution-routing-update-20-august-2026/",
        "kind": "cgpj_current_status_en",
        "markers": [
            "Appeals: five-file package + two later annexes + audiovisual link incorporated",
            "Four central acknowledgements · 21 August.",
            "Do not resend the material already confirmed as joined.",
        ],
        "min_bytes": 7000,
    },
    {
        "path": "es/actualizacion-cgpj-fiscalia-20-agosto-2026/",
        "kind": "cgpj_current_status_es",
        "markers": [
            "Recursos: paquete de cinco archivos + dos anexos posteriores + enlace audiovisual incorporados",
            "Cuatro acuses centrales · 21 de agosto.",
            "No reenviar el material ya confirmado como unido.",
        ],
        "min_bytes": 7000,
    },
    {
        "path": "sitemap-asset-recovery.xml",
        "kind": "asset_recovery_sitemap",
        "markers": [
            "asset-recovery-intervention-confiscation",
            "recuperacion-activos-intervencion-decomiso",
        ],
        "min_bytes": 300,
    },
    {
        "path": "sitemap-cgpj.xml",
        "kind": "cgpj_sitemap",
        "markers": [
            "cgpj-public-prosecution-routing-update-20-august-2026",
            "actualizacion-cgpj-fiscalia-20-agosto-2026",
            "2026-08-21",
        ],
        "min_bytes": 500,
    },
    {
        "path": "sitemap-por-derecho-technical.xml",
        "kind": "por_derecho_technical_sitemap",
        "markers": [
            "/en/por-derecho/second-pair-of-eyes/",
            "/es/por-derecho/segundo-par-de-ojos/",
            "/en/por-derecho/technical-partners/",
            "/es/por-derecho/socios-tecnicos/",
        ],
        "min_bytes": 900,
    },
    {
        "path": "robots.txt",
        "kind": "por_derecho_technical_robots",
        "markers": [
            "Sitemap: https://sbu001monterecco.github.io/por-derecho/sitemap-por-derecho-technical.xml",
        ],
        "min_bytes": 1000,
    },
    {
        "path": "assets/site.js",
        "kind": "global_site_loader_chain",
        "markers": [
            "site-pre-treasury-154-hq-20260828.js?v=",
            "data-pre-treasury-154-site-loader",
        ],
        "min_bytes": 500,
    },
    {
        "path": "assets/site-pre-treasury-154-hq-20260828.js",
        "kind": "asset_recovery_global_loader",
        "markers": [
            "asset-recovery-preservation-20260821.js?v=",
            "data-asset-recovery-intervention-loader",
        ],
        "min_bytes": 5000,
    },
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def fetch(url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Por-Derecho-Recent-Live-Verification/20260821",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
            "Accept": "text/html,application/xml,text/plain,text/javascript,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read()
        return {
            "status": response.status,
            "final_url": response.geturl(),
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified"),
            "server": response.headers.get("Server"),
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "text": body.decode("utf-8", errors="replace"),
        }


def one_pass(base_url: str, timeout: int, attempt: int) -> tuple[bool, list[dict[str, Any]]]:
    all_ok = True
    records: list[dict[str, Any]] = []
    nonce = f"{int(time.time())}-{attempt}"

    for check in CHECKS:
        url = urllib.parse.urljoin(base_url.rstrip("/") + "/", check["path"])
        checked_url = f"{url}{'&' if '?' in url else '?'}psr_recent_verify={nonce}"
        record: dict[str, Any] = {
            "kind": check["kind"],
            "path": check["path"],
            "url": url,
            "checked_at": utc_now(),
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

        all_ok = all_ok and bool(record["ok"])
        records.append(record)

    return all_ok, records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE)
    parser.add_argument("--attempts", type=int, default=5)
    parser.add_argument("--interval", type=int, default=20)
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument("--output", default="artifacts/recent-live-20260821/result.json")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    started_at = utc_now()
    final_records: list[dict[str, Any]] = []

    for attempt in range(1, max(1, args.attempts) + 1):
        ok, records = one_pass(args.base_url, args.timeout, attempt)
        final_records = records
        print(", ".join(f"{record['kind']}={'OK' if record['ok'] else 'FAIL'}" for record in records), flush=True)
        if ok:
            payload = {
                "ok": True,
                "base_url": args.base_url,
                "started_at": started_at,
                "verified_at": utc_now(),
                "attempt": attempt,
                "checks": records,
            }
            output.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            print("RECENT LIVE VERIFICATION: PASS")
            return 0
        if attempt < args.attempts:
            time.sleep(max(1, args.interval))

    output.write_text(
        json.dumps(
            {
                "ok": False,
                "base_url": args.base_url,
                "started_at": started_at,
                "failed_at": utc_now(),
                "attempts": args.attempts,
                "checks": final_records,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print("RECENT LIVE VERIFICATION: FAIL", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

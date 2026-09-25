#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
import urllib.request
from pathlib import Path

TARGETS = [
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/es/ricpe-idoneidad-series-f-g/",
        "markers": ["Serie F, Serie G y Decreto 224/2022", "1.598.849,32", "4.974.853,78", "100% TRANSPARENCIA"],
    },
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/en/ricpe-idoneidad-series-f-g/",
        "markers": ["Series F, Series G and Decree 224/2022", "1,598,849.32", "4,974,853.78", "100% TRANSPARENCY"],
    },
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/assets/ricpe-idoneidad-public-questions-20260818.js",
        "markers": ["ricpe-idoneidad-series-f-g-20260818", "CUESTIÓN DOCUMENTAL ABIERTA", "OPEN DOCUMENTARY QUESTION"],
    },
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/sitemap-ricpe-idoneidad.xml",
        "markers": ["/es/ricpe-idoneidad-series-f-g/", "/en/ricpe-idoneidad-series-f-g/"],
    },
    {
        "url": "https://sbu001monterecco.github.io/por-derecho/robots.txt",
        "markers": ["sitemap-ricpe-idoneidad.xml"],
    },
]


def fetch(url: str, timeout: int) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "por-derecho-ricpe-live-verifier/1"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.status, response.read().decode("utf-8", errors="replace")


def verify_once(timeout: int) -> tuple[bool, list[dict]]:
    rows = []
    ok = True
    for target in TARGETS:
        row = {"url": target["url"], "status": None, "missing_markers": [], "error": None}
        try:
            status, body = fetch(target["url"], timeout)
            row["status"] = status
            row["missing_markers"] = [m for m in target["markers"] if m not in body]
            if status != 200 or row["missing_markers"]:
                ok = False
        except Exception as exc:
            row["error"] = repr(exc)
            ok = False
        rows.append(row)
    return ok, rows


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--attempts", type=int, default=30)
    p.add_argument("--interval", type=int, default=10)
    p.add_argument("--timeout", type=int, default=20)
    p.add_argument("--output", default="artifacts/ricpe-idoneidad-live/verification.json")
    args = p.parse_args()

    last = []
    for attempt in range(1, args.attempts + 1):
        ok, rows = verify_once(args.timeout)
        last = rows
        print(json.dumps({"attempt": attempt, "ok": ok, "results": rows}, ensure_ascii=False, indent=2))
        if ok:
            payload = {"verified": True, "attempt": attempt, "results": rows}
            out = Path(args.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            return 0
        if attempt < args.attempts:
            time.sleep(args.interval)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"verified": False, "results": last}, ensure_ascii=False, indent=2), encoding="utf-8")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

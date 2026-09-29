#!/usr/bin/env python3
"""Bounded public-source snapshot for the RICPE capital-ecosystem source baseline.

This is intake only. It does not promote facts, identify investors or modify the
canonical actor/investor registers. Promotion remains PR/MR-gated.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, pathlib, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTER = ROOT / "assets/data/ricpe-capital-ecosystem-actor-register-v1.json"

def utcnow():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={
        "User-Agent": "PorDerecho-RICPE-PublicSourceWatch/1.0 (+source-control audit)",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
    })
    started = utcnow()
    try:
        with urllib.request.urlopen(req, timeout=35) as r:
            raw = r.read(10_000_000)
            return {
                "url": url, "retrieved_at": started, "http_status": getattr(r, "status", 200),
                "final_url": r.geturl(), "content_type": r.headers.get("Content-Type"),
                "etag": r.headers.get("ETag"), "last_modified": r.headers.get("Last-Modified"),
                "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                "truncated_at_10mb": len(raw) == 10_000_000,
                "state": "FETCHED"
            }
    except urllib.error.HTTPError as e:
        return {"url": url, "retrieved_at": started, "http_status": e.code, "state": "HTTP_ERROR"}
    except Exception as e:
        return {"url": url, "retrieved_at": started, "state": "FETCH_ERROR",
                "error_type": type(e).__name__, "error": str(e)[:300]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    data = json.loads(REGISTER.read_text(encoding="utf-8"))
    rows = []
    for src in data.get("source_baseline", []):
        row = fetch(src["url"])
        row["source_id"] = src["id"]
        row["source_kind"] = src["kind"]
        rows.append(row)
    report = {
        "schema": "por-derecho.ricpe-public-source-watch.v1",
        "generated_at": utcnow(),
        "canonical_register": str(REGISTER.relative_to(ROOT)),
        "classification": "RAW_AUTOMATED_INTAKE_NOT_CANONICAL_FACT",
        "promotion_rule": "Review -> identity reconcile -> evidence state -> contradiction check -> PR/MR before canonical use.",
        "sources": rows,
    }
    out = pathlib.Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"sources": len(rows), "output": str(out), "generated_at": report["generated_at"]}))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verify the identified public-safe Concurso 36/2012 corpus byte-for-byte.

This is a deployment verifier, not a claim that the certified court docket is
complete. It binds the declared bilingual routes, the 50-record specialist
corpus, the public-safe PDF set and the 27-Feb-2018 communication package to
the checked-out Git tree.
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
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PUBLICATION_MANIFEST = ROOT / "publication-manifests/concurso36-complete-record-20260823.json"
CATALOGUE = ROOT / "assets/data/concurso36-complete-record-v1.json"
SPECIALIST_MANIFEST = ROOT / "assets/data/concurso36-autos-fulltext-v1.json"
SPECIALIST_TEXT_ROOT = ROOT / "evidence/insolvency-36-2012/concurso-autos/full-text"
SECURITY_ROOT = ROOT / "evidence/sun-park/2018-02-27-ac-security-request"
SECURITY_MANIFEST = SECURITY_ROOT / "manifest.json"
DEFAULT_BASE = "https://sbu001monterecco.github.io/por-derecho/"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_targets() -> list[dict[str, Any]]:
    publication = load_json(PUBLICATION_MANIFEST)
    specialist = load_json(SPECIALIST_MANIFEST)
    security = load_json(SECURITY_MANIFEST)
    targets: dict[str, dict[str, Any]] = {}

    def add(path: Path, *, kind: str, url_path: str | None = None) -> None:
        source_path = rel(path)
        target_url_path = url_path or source_path
        if target_url_path in targets:
            previous = targets[target_url_path]["source_path"]
            raise ValueError(
                f"duplicate public target {target_url_path!r}: "
                f"{previous!r} and {source_path!r}"
            )
        body = path.read_bytes()
        targets[target_url_path] = {
            "kind": kind,
            "source_path": source_path,
            "url_path": target_url_path,
            "expected_bytes": len(body),
            "expected_sha256": sha256_bytes(body),
        }

    for language in ("es", "en"):
        for route in publication["expected_routes"][language]:
            path = ROOT / route
            add(path, kind=f"route_{language}", url_path=route.removesuffix("index.html"))

    for path in (CATALOGUE, SPECIALIST_MANIFEST, PUBLICATION_MANIFEST, SECURITY_MANIFEST):
        add(path, kind="control_json")

    for document in specialist["documents"]:
        add(SPECIALIST_TEXT_ROOT / document["href"], kind="specialist_full_text")
        if document.get("public_pdf"):
            add(ROOT / document["public_pdf"], kind="public_pdf")

    derivative = SECURITY_ROOT / security["public_derivative"]["path"]
    add(derivative, kind="public_pdf")
    add(SECURITY_ROOT / security["public_derivative"]["authoritative_transcript"], kind="security_transcript")
    add(SECURITY_ROOT / security["public_derivative"]["translation"], kind="security_transcript")

    result = [targets[key] for key in sorted(targets)]
    expected_kinds = Counter({
        "route_es": 9,
        "route_en": 9,
        "control_json": 4,
        "specialist_full_text": 50,
        "security_transcript": 2,
        "public_pdf": 11,
    })
    actual_kinds = Counter(target["kind"] for target in result)
    if len(result) != 85 or actual_kinds != expected_kinds:
        raise ValueError(
            "exact public target inventory drifted: "
            f"count={len(result)} kinds={dict(sorted(actual_kinds.items()))}; "
            f"expected_count=85 expected_kinds={dict(sorted(expected_kinds.items()))}"
        )
    return result


def fetch_target(base_url: str, target: dict[str, Any], timeout: int, nonce: str) -> dict[str, Any]:
    url = urllib.parse.urljoin(base_url.rstrip("/") + "/", target["url_path"])
    request = urllib.request.Request(
        f"{url}{'&' if '?' in url else '?'}c36_live={nonce}",
        headers={
            "User-Agent": "Por-Derecho-Concurso36-Complete-Record-Live/1.0",
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


def semantic_control() -> dict[str, Any]:
    catalogue = load_json(CATALOGUE)
    specialist = load_json(SPECIALIST_MANIFEST)
    publication = load_json(PUBLICATION_MANIFEST)
    security = load_json(SECURITY_MANIFEST)
    counts = catalogue.get("counts", {})
    result = catalogue.get("result", {})
    documents = specialist.get("documents", [])
    public_pdfs = {document["public_pdf"] for document in documents if document.get("public_pdf")}
    checks = {
        "catalogue_records_127": len(catalogue.get("records", [])) == 127,
        "catalogue_count_127": counts.get("canonical_records") == 127,
        "specialist_records_50": len(documents) == 50,
        "specialist_public_pdfs_10": len(public_pdfs) == 10,
        "security_public_pdf_hash_bound": security.get("public_derivative", {}).get("sha256")
        == "129cfdd2b74fe7f5e35b0db7890878aa10c5b81e6d4d6c9d3eaf0845eb820607",
        "inventory_partial": result.get("inventory_status")
        == "INVENTORY PARTIAL — CERTIFIED DOCKET OR RECORDS STILL MISSING",
        "whole_file_claim_prohibited": result.get("complete_or_all_uploaded_claim_permitted") is False,
        "publication_state_controlled": publication.get("current_state") in {"LIVE_VERIFIED", "DELETION_SAFE"},
        "email_not_authorized_or_sent": publication.get("email_control") == {
            "email_authorized_by_this_publication": False,
            "email_sent": False,
        },
    }
    return {"ok": all(checks.values()), "checks": checks}


def one_pass(base_url: str, targets: list[dict[str, Any]], timeout: int, attempt: int) -> dict[str, Any]:
    nonce = f"{int(time.time())}-{attempt}"
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        records = list(executor.map(
            lambda target: fetch_target(base_url, target, timeout, nonce),
            targets,
        ))
    records.sort(key=lambda item: item["source_path"])
    semantic = semantic_control()
    kind_counts: dict[str, int] = {}
    for record in records:
        kind_counts[record["kind"]] = kind_counts.get(record["kind"], 0) + 1
    return {
        "ok": semantic["ok"] and all(record["ok"] for record in records),
        "attempt": attempt,
        "verified_at": utc_now(),
        "base_url": base_url,
        "surface_count": len(records),
        "kind_counts": kind_counts,
        "semantic": semantic,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE)
    parser.add_argument("--attempts", type=int, default=1)
    parser.add_argument("--interval", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument("--output", default="artifacts/concurso36-complete-record-live/result.json")
    args = parser.parse_args()

    targets = build_targets()
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    result: dict[str, Any] = {}
    for attempt in range(1, max(1, args.attempts) + 1):
        result = one_pass(args.base_url, targets, args.timeout, attempt)
        failed = [record["source_path"] for record in result["records"] if not record["ok"]]
        print(
            f"attempt {attempt}/{args.attempts}: "
            f"{result['surface_count'] - len(failed)}/{result['surface_count']} byte-exact surfaces; "
            f"semantic={'PASS' if result['semantic']['ok'] else 'FAIL'}",
            flush=True,
        )
        if result["ok"]:
            output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print("CONCURSO 36/2012 COMPLETE-RECORD LIVE READBACK: PASS")
            return 0
        if failed:
            print("not yet exact: " + ", ".join(failed[:12]), flush=True)
        if attempt < args.attempts:
            time.sleep(max(1, args.interval))

    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("CONCURSO 36/2012 COMPLETE-RECORD LIVE READBACK: FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

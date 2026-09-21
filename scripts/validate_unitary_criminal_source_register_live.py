#!/usr/bin/env python3
"""Live HTTP readback for the unitary RedSARA / Ministerio Fiscal publication.

This validator checks the public Pages host, not repository source. It deliberately
keeps evidential meanings separate: HTTP availability and byte/data consistency do
not establish the truth or merits of any allegation.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urljoin

DEFAULT_BASE = "https://sbu001monterecco.github.io/por-derecho/"


def fetch(base: str, path: str) -> str:
    url = urljoin(base.rstrip("/") + "/", path.lstrip("/"))
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "por-derecho-unitary-criminal-source-live/20260904",
            "Cache-Control": "no-cache",
        },
    )
    with urllib.request.urlopen(req, timeout=25) as response:
        body = response.read().decode("utf-8", errors="strict")
        if response.status != 200:
            raise RuntimeError(f"{url} returned HTTP {response.status}")
        return body


def require(body: str, marker: str, label: str) -> None:
    if marker not in body:
        raise AssertionError(f"{label}: missing marker {marker!r}")


def validate(base: str) -> None:
    es_source = fetch(base, "es/registro-fuentes-penales/")
    en_source = fetch(base, "en/criminal-source-register/")
    es_cont = fetch(base, "es/ministerio-fiscal-continuidad-redsara/")
    en_cont = fetch(base, "en/ministerio-fiscal-redsara-continuity/")
    register_text = fetch(base, "data/unitary-criminal-redsara-register-20260903.json")
    csv_text = fetch(base, "data/unitary-criminal-redsara-register-20260903.csv")
    ledger_text = fetch(base, "data/ministry-fiscal-continuity-ledger-20260904.json")
    sitemap = fetch(base, "sitemap-unitary-digest-20260903.xml")
    site_js = fetch(base, "assets/site.js")
    search_js = fetch(base, "assets/unitary-criminal-source-register-search-extension-20260904.js")

    for marker in (
        "PD-REDSARA-MF-REGISTER-20260903-01",
        "Buscar las 75 comunicaciones registradas",
        "unitary-criminal-redsara-register-20260903.json",
        "unitary-criminal-redsara-register-20260903.csv",
        "https://sbu001monterecco.github.io/por-derecho/en/criminal-source-register/",
    ):
        require(es_source, marker, "ES source register")
    for marker in (
        "PD-REDSARA-MF-REGISTER-20260903-01",
        "Search all 75 registered communications",
        "unitary-criminal-redsara-register-20260903.json",
        "unitary-criminal-redsara-register-20260903.csv",
        "https://sbu001monterecco.github.io/por-derecho/es/registro-fuentes-penales/",
    ):
        require(en_source, marker, "EN source register")

    for body, label, pair in (
        (es_cont, "ES continuity", "https://sbu001monterecco.github.io/por-derecho/en/ministerio-fiscal-redsara-continuity/"),
        (en_cont, "EN continuity", "https://sbu001monterecco.github.io/por-derecho/es/ministerio-fiscal-continuidad-redsara/"),
    ):
        require(body, "PD-MF-CONTINUITY-20260904-01", label)
        require(body, "75", label)
        require(body, "22", label)
        require(body, "97", label)
        require(body, "ministry-fiscal-continuity-ledger-20260904.json", label)
        require(body, pair, label)

    register = json.loads(register_text)
    if register.get("control") != "PD-REDSARA-MF-REGISTER-20260903-01":
        raise AssertionError("register control mismatch")
    expected_counts = {
        "registered_communications": 75,
        "attachment_hash_records": 125,
        "communications_with_no_hashed_attachment": 15,
        "verified_current_conversation_pdfs_by_exact_sha512": 9,
    }
    if register.get("counts") != expected_counts:
        raise AssertionError(f"register counts mismatch: {register.get('counts')!r}")
    shards = register.get("record_shards") or []
    if len(shards) != 5 or sum(int(item.get("records", 0)) for item in shards) != 75:
        raise AssertionError("register shard denominator mismatch")

    csv_rows = list(csv.DictReader(io.StringIO(csv_text)))
    if len(csv_rows) != 75:
        raise AssertionError(f"CSV row denominator mismatch: {len(csv_rows)}")

    ledger = json.loads(ledger_text)
    if ledger.get("control") != "PD-MF-CONTINUITY-20260904-01":
        raise AssertionError("continuity ledger control mismatch")
    layers = {row.get("id"): row for row in ledger.get("layers", []) if isinstance(row, dict)}
    if layers.get("MF-LAYER-01", {}).get("count") != 75:
        raise AssertionError("continuity baseline count mismatch")
    if layers.get("MF-LAYER-02", {}).get("count") != 22:
        raise AssertionError("continuity post-Anexo count mismatch")
    aggregate = layers.get("MF-LAYER-02", {}).get("aggregate_through_cutoff") or {}
    if aggregate != {"registrations": 97, "received": 90, "rejected": 7}:
        raise AssertionError(f"continuity June cutoff mismatch: {aggregate!r}")
    if layers.get("MF-LAYER-03", {}).get("count_status") != "OPEN_DENOMINATOR_PENDING_DEDUP_STATUS_RECONCILIATION":
        raise AssertionError("later formal denominator must remain OPEN")

    for url in (
        "https://sbu001monterecco.github.io/por-derecho/es/registro-fuentes-penales/",
        "https://sbu001monterecco.github.io/por-derecho/en/criminal-source-register/",
        "https://sbu001monterecco.github.io/por-derecho/es/ministerio-fiscal-continuidad-redsara/",
        "https://sbu001monterecco.github.io/por-derecho/en/ministerio-fiscal-redsara-continuity/",
    ):
        require(sitemap, url, "unitary sitemap")

    require(site_js, "unitary-criminal-source-register-search-extension-20260904.js", "site loader")
    for marker in (
        "UNITARY-CRIMINAL-SOURCE-REGISTER-SEARCH-20260904",
        "PD-REDSARA-MF-REGISTER-20260903-01",
        "PD-MF-CONTINUITY-20260904-01",
        "/por-derecho/es/registro-fuentes-penales/",
        "/por-derecho/en/criminal-source-register/",
        "/por-derecho/es/ministerio-fiscal-continuidad-redsara/",
        "/por-derecho/en/ministerio-fiscal-redsara-continuity/",
    ):
        require(search_js, marker, "homepage search extension")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--attempts", type=int, default=1)
    parser.add_argument("--delay", type=float, default=5.0)
    args = parser.parse_args()

    attempts = max(1, args.attempts)
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            validate(args.base)
            print(f"UNITARY CRIMINAL SOURCE LIVE READBACK: PASS ({args.base})")
            return 0
        except (AssertionError, RuntimeError, urllib.error.URLError, UnicodeError, json.JSONDecodeError) as exc:
            last_error = exc
            print(f"Attempt {attempt}/{attempts}: {exc}", file=sys.stderr)
            if attempt < attempts:
                time.sleep(max(0.0, args.delay))

    print(f"UNITARY CRIMINAL SOURCE LIVE READBACK: FAIL: {last_error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the public-safe RedSARA criminal-source register.

This validator checks provenance structure, not the truth or legal merits of any
allegation. It intentionally works only on the minimised public derivative.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "unitary-criminal-redsara-register-20260903.json"
ES_PAGE = ROOT / "es" / "registro-fuentes-penales" / "index.html"
EN_PAGE = ROOT / "en" / "criminal-source-register" / "index.html"
CSV_PATH = ROOT / "data" / "unitary-criminal-redsara-register-20260903.csv"

EXPECTED = {
    "registered_communications": 75,
    "attachment_hash_records": 125,
    "communications_with_no_hashed_attachment": 15,
    "verified_current_conversation_pdfs_by_exact_sha512": 9,
}

HEX512 = re.compile(r"^[0-9a-f]{128}$")
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
SPANISH_ID = re.compile(r"\b(?:\d{8}[A-Z]|[XYZ]\d{7}[A-Z])\b", re.I)


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("counts") != EXPECTED:
        fail(f"count header mismatch: {manifest.get('counts')!r}")

    shard_specs = manifest.get("record_shards") or []
    if len(shard_specs) != 5:
        fail(f"expected five shards, got {len(shard_specs)}")

    records = []
    for spec in shard_specs:
        path = ROOT / "data" / spec["file"]
        payload = json.loads(path.read_text(encoding="utf-8"))
        shard_records = payload.get("records") or []
        if len(shard_records) != spec.get("records"):
            fail(f"shard count mismatch: {path.name}")
        records.extend(shard_records)

    if len(records) != 75:
        fail(f"expected 75 registrations, got {len(records)}")
    regages = [row.get("regage") for row in records]
    if len(set(regages)) != len(regages):
        fail("duplicate REGAGE record detected")

    attachments = [a for row in records for a in (row.get("attachments") or [])]
    if len(attachments) != 125:
        fail(f"expected 125 attachment hashes, got {len(attachments)}")
    no_hash = sum(1 for row in records if not row.get("attachments"))
    if no_hash != 15:
        fail(f"expected 15 no-hash receipt records, got {no_hash}")
    for attachment in attachments:
        if attachment.get("algorithm") != "SHA-512" or not HEX512.fullmatch(attachment.get("sha512", "")):
            fail(f"invalid SHA-512 record: {attachment!r}")

    hash_index = {(row["regage"], a["filename"], a["sha512"]) for row in records for a in row.get("attachments", [])}
    verified = manifest.get("verified_current_uploads") or []
    if len(verified) != 9:
        fail(f"expected nine current-upload bridges, got {len(verified)}")
    for item in verified:
        if not HEX512.fullmatch(item.get("sha512", "")):
            fail(f"invalid current-upload hash: {item.get('uploaded_filename')}")
        matches = item.get("matches") or []
        if not matches:
            fail(f"current upload has no registered match: {item.get('uploaded_filename')}")
        for match in matches:
            key = (match["regage"], match["registered_filename"], item["sha512"])
            if key not in hash_index:
                fail(f"current-upload bridge not present in shard ledger: {key!r}")

    public_paths = [MANIFEST, CSV_PATH, ES_PAGE, EN_PAGE] + [ROOT / "data" / x["file"] for x in shard_specs]
    for path in public_paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        if EMAIL.search(text):
            fail(f"email-like PII leaked into public derivative: {path}")
        if SPANISH_ID.search(text):
            fail(f"DNI/NIE-like PII leaked into public derivative: {path}")

    for page in (ES_PAGE, EN_PAGE):
        text = page.read_text(encoding="utf-8")
        for regage in ("REGAGE26e00004212180", "REGAGE26e00004639835", "REGAGE26e00009989396"):
            if regage not in text:
                fail(f"key current REGAGE missing from {page}: {regage}")
        if "record_shards" not in text:
            fail(f"source page is not loading the five-shard ledger: {page}")

    print("PASS: 75 REGAGE records / 125 SHA-512 attachments / 15 no-hash receipts / 9 current exact bridges")
    print("PASS: public derivative PII scan (email + DNI/NIE patterns)")
    print("PASS: bilingual source pages expose key current REGAGE bridges and shard loader")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)

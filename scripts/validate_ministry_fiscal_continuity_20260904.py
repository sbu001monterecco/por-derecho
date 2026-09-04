#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/ministry-fiscal-continuity-ledger-20260904.json"
EN = ROOT / "en/ministry-fiscal-continuity/index.html"
ES = ROOT / "es/continuidad-ministerio-fiscal/index.html"
REPORT = ROOT / "reports/MINISTERIO_FISCAL_CONTINUITY_RECONCILIATION_04SEP2026.md"
SITEMAP = ROOT / "sitemap-ministry-fiscal-continuity.xml"
ROBOTS = ROOT / "robots.txt"

EXPECTED_SHA256 = "1e09c8eb3bce26e28dc5f22e5d6ebad3f458212cf8d85f5920e869fa42554abe"
EXPECTED_SHA512 = "e31f92fcf4462aa79d963e62d20b5afb7d84820785daeb823eb313c24c356a40d9846498ed770bb39368bfdfba07dda6214827b85f32a316d0bfbf843cff8196"


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def require(cond: bool, msg: str) -> None:
    if not cond:
        fail(msg)


def main() -> None:
    for path in (LEDGER, EN, ES, REPORT, SITEMAP, ROBOTS):
        require(path.exists(), f"missing {path.relative_to(ROOT)}")

    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    require(data.get("control_id") == "PD-MF-CONTINUITY-20260904-02", "wrong control id")
    require(data.get("status") == "ACTIVE_RECONCILIATION", "continuity status must remain ACTIVE_RECONCILIATION")

    formal = {row["layer_id"]: row for row in data["formal_layers"]}
    require(formal["MF-LAYER-01"]["count"] == 75, "Anexo 4 baseline must remain 75")
    require(formal["MF-LAYER-01"]["attachment_hash_records"] == 125, "attachment hash denominator must remain 125")
    require(formal["MF-LAYER-02"]["aggregate_through_cutoff"] == 97, "historical 21-Jun checkpoint must remain 97")
    require(formal["MF-LAYER-03"]["count"] is None, "post-June final denominator must remain open")
    require(len(formal["MF-LAYER-03"]["known_checkpoint_regage"]) == 8, "expected eight later REGAGE checkpoint ids")

    email = {row["layer_id"]: row for row in data["email_layers"]}
    require(email["MF-LAYER-04"]["raw_candidate_count"] == 17, "targeted SENT raw candidate count changed")
    require(email["MF-LAYER-04"]["substantive_unique_count"] is None, "raw SENT must not be promoted to unique count")
    require(email["MF-LAYER-05"]["prosecution_side_candidate_floor"] == 9, "targeted inbound floor changed")
    require(email["MF-LAYER-05"]["final_count"] is None, "inbound denominator must remain open")

    verifications = {row["verification_id"]: row for row in data["source_verifications"]}
    eg = verifications["MF-EG745-BYTE-PARITY-20260904"]
    require(eg["master_id"] == "NAT-FIS-004", "E.G. 745 master id drift")
    require(eg["pages"] == 3 and eg["bytes"] == 1111997, "E.G. 745 page/byte fingerprint drift")
    require(eg["sha256"] == EXPECTED_SHA256, "E.G. 745 SHA-256 drift")
    require(eg["sha512"] == EXPECTED_SHA512, "E.G. 745 SHA-512 drift")
    require(eg["status"] == "EXACT_FILE_PARITY_CONFIRMED_WITH_EXISTING_PUBLIC_CONTROL", "E.G. 745 parity must remain confirmed")

    public_text = EN.read_text(encoding="utf-8") + "\n" + ES.read_text(encoding="utf-8")
    for token in ("PD-MF-CONTINUITY-20260904-02", EXPECTED_SHA256, "NAT-FIS-004", "REGAGE26e00070235775"):
        require(token in public_text, f"public continuity pages missing {token}")

    # Public minimisation: the new continuity pages must not re-publish source contact/private identifiers.
    forbidden_public = ["sbu001@monterecco.com", "91 3352129", "c/ Fortuny", "DNI", "NIE"]
    for token in forbidden_public:
        require(token.lower() not in public_text.lower(), f"public continuity pages expose forbidden token {token}")

    # Guard against a discarded provisional interpretation being reintroduced into this control release.
    new_release_text = LEDGER.read_text(encoding="utf-8") + "\n" + REPORT.read_text(encoding="utf-8") + "\n" + public_text
    require("0d96284231db1d126cf9477dd5f9b837819bde475e89623ab512749396eda4cf" not in new_release_text, "discarded provisional transport/hash value reintroduced")
    require("MF-REF-COLLISION-745-2026" not in new_release_text, "discarded E.G. 745 collision hypothesis reintroduced")

    sitemap = SITEMAP.read_text(encoding="utf-8")
    require("/es/continuidad-ministerio-fiscal/" in sitemap, "Spanish continuity route missing from sitemap")
    require("/en/ministry-fiscal-continuity/" in sitemap, "English continuity route missing from sitemap")
    require("sitemap-ministry-fiscal-continuity.xml" in ROBOTS.read_text(encoding="utf-8"), "robots.txt does not declare continuity sitemap")

    print("PASS: Ministerio Fiscal continuity controls, denominator locks, E.G. 745 byte parity and public-safety gates")


if __name__ == "__main__":
    main()

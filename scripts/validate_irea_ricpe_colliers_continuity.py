#!/usr/bin/env python3
"""Validate the finite IREA / RICPE / Colliers continuity publication."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


registry_index = load(DATA / "matter-identity-registry-v1.json")
registry: dict[str, dict] = {}
for part in registry_index["parts"]:
    for record in load(DATA / part["path"])["records"]:
        registry[record["id"]] = record

control_path = DATA / "caepr-caret-irea-ricpe-colliers-continuity-v1.json"
control = load(control_path)
records = control.get("records", [])
states = Counter(record.get("state") for record in records)

check(control.get("control_id") == "PD-IREA-RICPE-COLLIERS-CARET-20260828-01", "control ID drift")
check(len(records) == 13, "finite identity denominator must be 13")
check(states == Counter({"CARET_CONFIRMED": 13}), f"unexpected caret state split: {states}")
check(control.get("counts", {}).get("denominator") == 13, "declared denominator drift")
check(control.get("counts", {}).get("coverage_percent") == 100, "coverage must be 100%")
check(all(record.get("caepr_id") in registry for record in records), "confirmed object lacks registry ID")
check(
    all(registry[record["caepr_id"]].get("identity_resolution") in {None, "CANONICAL", "CARET_CONFIRMED"} for record in records),
    "a confirmed object points to a non-admitted registry state",
)
check(
    any(item.get("classification") == "RELATIONSHIP_NOT_IDENTITY; UNVERIFIED" for item in control.get("non_identity_exceptions", [])),
    "family relationship must remain outside the identity denominator and unverified",
)

people = {record["id"]: record for record in load(DATA / "matter-identity-registry-v1.people.json")["records"]}
check(people["PD-SP-P-0088"]["name"] == "Fernando Aguiar Acosta", "Fernando Aguiar identity drift")
check(people["PD-SP-P-0091"]["name"] == "Fernando Banderas Monis", "Fernando Banderas identity drift")
check("PD-SP-P-0091" in people["PD-SP-P-0088"].get("not_same_as", []), "two-Fernando distinction missing")
check("PD-SP-P-0088" in people["PD-SP-P-0091"].get("not_same_as", []), "two-Fernando distinction must be symmetric")

pages = {
    "en_lender": ROOT / "en/lender-of-record/index.html",
    "es_lender": ROOT / "es/acreedor-de-registro/index.html",
    "en_acosta": ROOT / "en/acosta-matos-perimeter/index.html",
    "es_acosta": ROOT / "es/acosta-matos-perimetro/index.html",
    "en_ricpe": ROOT / "en/ricpe-documentary-accountability/index.html",
    "es_ricpe": ROOT / "es/ricpe-responsabilidad-documental/index.html",
}
texts = {key: path.read_text(encoding="utf-8") for key, path in pages.items()}

for key, text in texts.items():
    check("Fernando Aguiar Acosta^" in text, f"{key}: exact witness identity/caret missing")
    check("data-caepr-id=\"PD-SP-P-0088\"" in text, f"{key}: witness CAEPR binding missing")

for key in ("en_lender", "es_lender"):
    text = texts[key]
    check("PD-SP-P-0091" in text and "Fernando Banderas Monis^" in text, f"{key}: 2017 Fernando correction missing")
    check("PD-SP-O-0072" in text and "PD-SP-O-0073" in text, f"{key}: IREA-Colliers identity chain missing")
    check("13/13 CARET_CONFIRMED" in text, f"{key}: caret coverage report missing")
    check("BORME-C-2018-5506" in text, f"{key}: official merger source missing")

for key in ("en_acosta", "es_acosta"):
    text = texts[key]
    check("PD-SP-O-0020" in text and "PD-SP-O-0073" in text, f"{key}: RICPE-Colliers witness chain missing")
    check(
        "not an adverse actor" in text.lower()
        or "not an adverse-actor classification" in text.lower()
        or "no clasificación como actor adverso" in text.lower(),
        f"{key}: witness/adverse boundary missing",
    )

evidence = (ROOT / "evidence/osint/2026-08-28-irea-colliers-meridian-fernando-aguiar-acosta.md").read_text(encoding="utf-8")
check("@" not in evidence, "public derivative contains an email address marker")
check("PSRC-IREA-2017-01" in evidence and "PSRC-IREA-2017-05" in evidence, "opaque private-source classes incomplete")
check("not “Fernando Acosta Matos”" in evidence, "identity correction missing from evidence note")
check("Circumstantial lead only" in evidence, "inference boundary missing from evidence note")

if failures:
    print("IREA / RICPE / COLLIERS CONTINUITY: FAIL")
    for failure in failures:
        print(f" - {failure}")
    raise SystemExit(1)

print("IREA / RICPE / COLLIERS CONTINUITY: PASS")
print(" - finite identity census: 13/13 CARET_CONFIRMED")
print(" - two-Fernando identity separation: PASS")
print(" - bilingual IREA, RICPE, Colliers and witness interlinks: PASS")
print(" - private-source minimization controls: PASS")

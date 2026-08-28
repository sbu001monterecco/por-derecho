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
    "en_unitary": ROOT / "en/irea-colliers-meridian-sun-park/index.html",
    "es_unitary": ROOT / "es/irea-colliers-meridian-sun-park/index.html",
    "en_ph122": ROOT / "en/ph122-cerberus-haya-bankia-external-perimeter/index.html",
    "es_ph122": ROOT / "es/perimetro-ph122-cerberus-haya-bankia-externo/index.html",
    "en_cuatrecasas": ROOT / "en/cuatrecasas-sun-park/index.html",
    "es_cuatrecasas": ROOT / "es/cuatrecasas-sun-park/index.html",
    "en_acosta": ROOT / "en/acosta-matos-perimeter/index.html",
    "es_acosta": ROOT / "es/acosta-matos-perimetro/index.html",
    "en_ricpe": ROOT / "en/ricpe-documentary-accountability/index.html",
    "es_ricpe": ROOT / "es/ricpe-responsabilidad-documental/index.html",
}
texts = {key: path.read_text(encoding="utf-8") for key, path in pages.items()}

for key in ("en_lender", "es_lender", "en_unitary", "es_unitary", "en_acosta", "es_acosta", "en_ricpe", "es_ricpe"):
    text = texts[key]
    check("Fernando Aguiar Acosta^" in text, f"{key}: exact witness identity/caret missing")
    check("data-caepr-id=\"PD-SP-P-0088\"" in text, f"{key}: witness CAEPR binding missing")

for key in ("en_lender", "es_lender"):
    text = texts[key]
    check("PD-SP-P-0091" in text and "Fernando Banderas Monis^" in text, f"{key}: 2017 Fernando correction missing")
    check("PD-SP-O-0072" in text and "PD-SP-O-0073" in text, f"{key}: IREA-Colliers identity chain missing")
    check("13/13 CARET_CONFIRMED" in text, f"{key}: caret coverage report missing")
    check("BORME-C-2018-5506" in text, f"{key}: official merger source missing")
    check("irea-colliers-meridian-sun-park/" in text, f"{key}: canonical unitary dossier link missing")

for key in ("en_unitary", "es_unitary"):
    text = texts[key]
    check(text.count('id="fernando-aguiar-acosta"') == 1, f"{key}: Fernando witness anchor must be unique")
    check(text.count('class="relationship-map"') == 1, f"{key}: relationship map must render exactly once")
    check(text.count('data-relationship-status="DOCUMENTED_PROFESSIONAL_SEQUENCE"') == 1, f"{key}: documented relationship edge must render exactly once")
    check(text.count('data-relationship-status="PROVISIONAL_UNVERIFIED_FAMILY_HYPOTHESIS"') == 1, f"{key}: provisional family edge must render exactly once")
    check("13/13 CARET_CONFIRMED" in text, f"{key}: caret coverage report missing")
    check("PD-SP-P-0090" in text and "PD-SP-P-0091" in text and "PD-SP-P-0089" in text, f"{key}: IREA people matrix incomplete")
    check("Financecommunity" in text or "financial-media" in text or "medio financiero" in text, f"{key}: 2026 hotel-finance corroboration missing")
    check("not the lender" in text.lower() or "no fue el prestamista" in text.lower(), f"{key}: lender-capacity correction missing")
    check("not expressly identify her as a Meridian participant" in text or "no la identifica expresamente como participante de Meridian" in text, f"{key}: Laura/Meridian boundary missing")
    check("not an adverse actor" in text.lower() or "no actor adverso" in text.lower(), f"{key}: Fernando witness boundary missing")
    check("family relationship" in text.lower() or "relación familiar" in text.lower() or "parentesco" in text.lower(), f"{key}: family boundary missing")
    check('data-relationship-status="DOCUMENTED_PROFESSIONAL_SEQUENCE"' in text, f"{key}: documented RICPE visual edge missing")
    check('data-relationship-status="PROVISIONAL_UNVERIFIED_FAMILY_HYPOTHESIS"' in text, f"{key}: provisional family visual edge missing")
    check("rel-edge documented" in text and "rel-edge hypothesis" in text, f"{key}: solid/dashed relationship code missing")

check("../../es/irea-colliers-meridian-sun-park/" in texts["en_unitary"], "EN unitary alternate/language link missing")
check("../../en/irea-colliers-meridian-sun-park/" in texts["es_unitary"], "ES unitary alternate/language link missing")

for key in ("en_ph122", "es_ph122", "en_cuatrecasas", "es_cuatrecasas", "en_ricpe", "es_ricpe", "en_acosta", "es_acosta"):
    check("irea-colliers-meridian-sun-park/" in texts[key], f"{key}: reciprocal unitary dossier link missing")

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
check("SRC-FINANCECOMMUNITY-FERNANDO-HOTEL-FINANCE-2026" in (ROOT / "research/lender-of-record-liability/data/sources.json").read_text(encoding="utf-8"), "2026 hotel-finance source missing")
check("Capacity correction" in evidence and "not the lender" in evidence, "IREA lender-capacity correction missing from evidence note")

unitary = load(DATA / "irea-colliers-meridian-sun-park-unitary-v1.json")
check(unitary.get("control_id") == "PD-IREA-COLLIERS-UNITARY-20260828-01", "unitary machine control ID drift")
check(len(unitary.get("capacity_lanes", [])) == 4, "unitary capacity-lane denominator must be 4")
check(len(unitary.get("people", [])) == 4, "unitary people denominator must be 4")
check("13/13 CARET_CONFIRMED" == unitary.get("identity_control", {}).get("result"), "unitary identity result drift")
check(unitary.get("relationship_presentation", {}).get("documented_professional_edge", {}).get("visual_code") == "SOLID_BURGUNDY", "documented RICPE visual code drift")
check(unitary.get("relationship_presentation", {}).get("provisional_family_edge", {}).get("visual_code") == "DASHED_AMBER", "provisional family visual code drift")

sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
check("/en/irea-colliers-meridian-sun-park/" in sitemap, "EN unitary route absent from sitemap")
check("/es/irea-colliers-meridian-sun-park/" in sitemap, "ES unitary route absent from sitemap")

if failures:
    print("IREA / RICPE / COLLIERS CONTINUITY: FAIL")
    for failure in failures:
        print(f" - {failure}")
    raise SystemExit(1)

print("IREA / RICPE / COLLIERS CONTINUITY: PASS")
print(" - finite identity census: 13/13 CARET_CONFIRMED")
print(" - two-Fernando identity separation: PASS")
print(" - bilingual IREA, RICPE, Colliers and witness interlinks: PASS")
print(" - holder / servicer / adviser / legal-adviser capacity separation: PASS")
print(" - 2026 independent hotel-finance corroboration with project/family limits: PASS")
print(" - solid documented RICPE edge / dashed provisional family edge: PASS")
print(" - unique bilingual Fernando witness anchor and relationship map: PASS")
print(" - private-source minimization controls: PASS")

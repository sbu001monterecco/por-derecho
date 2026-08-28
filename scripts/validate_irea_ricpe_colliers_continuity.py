#!/usr/bin/env python3
"""Validate the finite IREA / RICPE / Colliers continuity publication."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
LAURA_CAPTURE_SHA256 = "f6581bfa4d804c6d6fb3de654e9faa09f3781c2ac3fff2f123162209363e2964"
FERNANDO_PROFILE_SHA256 = "7b3ce8c4cb0f047991595eb3e4de6cb9d85d18919c8f42cc0e45d9b35ceac466"
LAURA_PROFILE_SHA256 = "d2438087f18b9f9e210bb9b196208b6bee4ee8b4ee7533f3aa0740236354c04e"
LAURA_SOURCE_IDS = {
    "SRC-LINKEDIN-LAURA-AGUIAR-ACOSTA-2026",
    "SRC-MAEC-LAURA-AGUIAR-ACOSTA-IE-2023",
    "SRC-RICPE-MYND-YAIZA-CANARIAN",
    "SRC-RICPE-RADISSON-BLU-LANZAROTE-CANARIAN",
    "SRC-CANARIAN-HOSPITALITY-ACOSTA-MATOS-BACKING-2021",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def check_no_unsupported_laura_ricpe_employment(text: str, surface: str) -> None:
    """Reject affirmative employer claims that the corrected public record does not support."""
    lowered = text.lower()
    forbidden = (
        "laura aguiar acosta worked at ric private equity",
        "laura aguiar acosta worked for ric private equity",
        "laura aguiar acosta was employed by ric private equity",
        "laura aguiar acosta was a ric private equity employee",
        "laura aguiar acosta trabajó en ric private equity",
        "laura aguiar acosta trabajó para ric private equity",
        "laura aguiar acosta fue empleada de ric private equity",
    )
    for phrase in forbidden:
        check(phrase not in lowered, f"{surface}: unsupported direct Laura-RICPE employment wording: {phrase!r}")
    check(
        'data-relationship-status="DOCUMENTED_RICPE_EMPLOYMENT"' not in text,
        f"{surface}: unsupported documented Laura-RICPE employment edge",
    )


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
check(len(records) == 20, "finite identity denominator must be 20")
check(states == Counter({"CARET_CONFIRMED": 20}), f"unexpected caret state split: {states}")
check(control.get("counts", {}).get("denominator") == 20, "declared denominator drift")
check(control.get("counts", {}).get("CARET_CONFIRMED") == 20, "declared confirmed count drift")
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
check(
    any(
        item.get("classification")
        == "ALLEGED_SIBLING_RELATIONSHIP_NOT_IDENTITY; ATTRIBUTED_TO_GIL_MARER; INDEPENDENTLY_UNVERIFIED"
        for item in control.get("non_identity_exceptions", [])
    ),
    "Fernando-Laura sibling claim must remain attributed, unverified and outside identity",
)
check(
    any(
        item.get("classification") == "RELATIONSHIP_NOT_IDENTITY; NOT_SHOWN_IN_CURRENT_PUBLIC_PROFILE"
        and "RIC Private Equity direct employment" in item.get("label", "")
        for item in control.get("non_identity_exceptions", [])
    ),
    "Laura direct-RICPE-employment correction missing from identity exceptions",
)

people = {record["id"]: record for record in load(DATA / "matter-identity-registry-v1.people.json")["records"]}
check(people["PD-SP-P-0088"]["name"] == "Fernando Aguiar Acosta", "Fernando Aguiar identity drift")
check(people["PD-SP-P-0091"]["name"] == "Fernando Banderas Monis", "Fernando Banderas identity drift")
check(people["PD-SP-P-0095"]["name"] == "Laura Aguiar Acosta", "Laura Aguiar identity drift")
check(people["PD-SP-P-0095"].get("identity_resolution") == "CARET_CONFIRMED", "Laura Aguiar caret admission missing")
check("PD-SP-P-0091" in people["PD-SP-P-0088"].get("not_same_as", []), "two-Fernando distinction missing")
check("PD-SP-P-0088" in people["PD-SP-P-0091"].get("not_same_as", []), "two-Fernando distinction must be symmetric")
for distinct_id in ("PD-SP-P-0012", "PD-SP-P-0089"):
    check(distinct_id in people["PD-SP-P-0095"].get("not_same_as", []), f"Laura Aguiar distinction missing: {distinct_id}")
    check("PD-SP-P-0095" in people[distinct_id].get("not_same_as", []), f"Laura Aguiar distinction not symmetric: {distinct_id}")
check(
    "does not show direct RIC Private Equity employment" in people["PD-SP-P-0095"].get("capacity_boundary", ""),
    "Laura registry boundary must reject direct RICPE employment",
)
for caepr_id, name in {
    "PD-SP-O-0007": "Construcciones Acosta Matos, S.A.",
    "PD-SP-O-0077": "ACHM Spain Management, S.L.",
    "PD-SP-O-0078": "Belagua 2013, S.A.",
    "PD-SP-O-0079": "Hotel Project Tenerife, S.L.",
    "PD-SP-O-0019": "Canarian Hospitality, S.L.",
    "PD-SP-S-0011": "AC Hotel Tenerife",
}.items():
    check(registry.get(caepr_id, {}).get("name") == name, f"ACHM/hotel identity drift: {caepr_id}")
    check(registry.get(caepr_id, {}).get("identity_resolution") == "CARET_CONFIRMED", f"ACHM/hotel caret missing: {caepr_id}")

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
    "en_family": ROOT / "en/acosta-matos-family/index.html",
    "es_family": ROOT / "es/acosta-matos-familia/index.html",
    "en_ricpe_genealogy": ROOT / "en/ric-private-equity-sun-park/index.html",
    "es_ricpe_genealogy": ROOT / "es/ric-private-equity-sun-park/index.html",
}
texts = {key: path.read_text(encoding="utf-8") for key, path in pages.items()}

for key in ("en_lender", "es_lender", "en_unitary", "es_unitary", "en_acosta", "es_acosta", "en_ricpe", "es_ricpe"):
    text = texts[key]
    check("Fernando Aguiar Acosta^" in text, f"{key}: exact witness identity/caret missing")
    check("data-caepr-id=\"PD-SP-P-0088\"" in text, f"{key}: witness CAEPR binding missing")

for key in ("en_unitary", "es_unitary", "en_acosta", "es_acosta", "en_ricpe", "es_ricpe"):
    text = texts[key]
    check("Laura Aguiar Acosta^" in text, f"{key}: exact Laura witness identity/caret missing")
    check('data-caepr-id="PD-SP-P-0095"' in text, f"{key}: Laura witness CAEPR binding missing")
    check('data-caepr-id="PD-SP-O-0019"' in text, f"{key}: Canarian Hospitality CAEPR binding missing")
    check_no_unsupported_laura_ricpe_employment(text, key)
    check(
        "does not show direct RIC Private Equity employment" in text
        or "does not show direct employment by RIC Private Equity" in text
        or "direct RICPE employment is not shown" in text
        or "not direct RICPE employment" in text
        or "not a direct RICPE job" in text
        or "DIRECT_RICPE_EMPLOYMENT_NOT_SHOWN" in text
        or "no muestra empleo directo en RIC Private Equity" in text
        or "no consta empleo directo en RICPE" in text
        or "no empleo directo en RICPE" in text
        or "no un puesto directo en RICPE" in text,
        f"{key}: direct Laura-RICPE employment correction missing",
    )

for key in ("en_lender", "es_lender"):
    text = texts[key]
    check("PD-SP-P-0091" in text and "Fernando Banderas Monis^" in text, f"{key}: 2017 Fernando correction missing")
    check("PD-SP-O-0072" in text and "PD-SP-O-0073" in text, f"{key}: IREA-Colliers identity chain missing")
    check("20/20 CARET_CONFIRMED" in text, f"{key}: caret coverage report missing")
    check("BORME-C-2018-5506" in text, f"{key}: official merger source missing")
    check("irea-colliers-meridian-sun-park/" in text, f"{key}: canonical unitary dossier link missing")

for key in ("en_unitary", "es_unitary"):
    text = texts[key]
    check(text.count('id="fernando-aguiar-acosta"') == 1, f"{key}: Fernando witness anchor must be unique")
    check(text.count('id="laura-aguiar-acosta"') == 1, f"{key}: Laura witness anchor must be unique")
    check(text.count('class="relationship-map"') == 1, f"{key}: relationship map must render exactly once")
    check(text.count('data-relationship-status="DOCUMENTED_PROFESSIONAL_SEQUENCE"') == 1, f"{key}: documented relationship edge must render exactly once")
    check(text.count('data-relationship-status="PROVISIONAL_UNVERIFIED_FAMILY_HYPOTHESIS"') == 1, f"{key}: provisional family edge must render exactly once")
    check("20/20 CARET_CONFIRMED" in text, f"{key}: caret coverage report missing")
    check("PD-SP-P-0090" in text and "PD-SP-P-0091" in text and "PD-SP-P-0089" in text, f"{key}: IREA people matrix incomplete")
    check("Financecommunity" in text or "financial-media" in text or "medio financiero" in text, f"{key}: 2026 hotel-finance corroboration missing")
    check("not the lender" in text.lower() or "no fue el prestamista" in text.lower(), f"{key}: lender-capacity correction missing")
    check("not expressly identify her as a Meridian participant" in text or "no la identifica expresamente como participante de Meridian" in text, f"{key}: Laura/Meridian boundary missing")
    check("not an adverse actor" in text.lower() or "no actor adverso" in text.lower(), f"{key}: Fernando witness boundary missing")
    check("family relationship" in text.lower() or "relación familiar" in text.lower() or "parentesco" in text.lower(), f"{key}: family boundary missing")
    check('data-relationship-status="DOCUMENTED_PROFESSIONAL_SEQUENCE"' in text, f"{key}: documented RICPE visual edge missing")
    check('data-relationship-status="PROVISIONAL_UNVERIFIED_FAMILY_HYPOTHESIS"' in text, f"{key}: provisional family visual edge missing")
    check("rel-edge documented" in text and "rel-edge hypothesis" in text, f"{key}: solid/dashed relationship code missing")
    check(text.count('data-evidence-view="FOUR_OF_FOUR_CV_SEQUENCE"') == 1, f"{key}: 4/4 CV visual must render exactly once")
    check(text.count('data-cv-placement="') == 4, f"{key}: 4/4 CV visual must contain four placements")
    check(text.count('data-interpretation-status="ATTRIBUTED_CHECKERS_INTERPRETATION"') == 1, f"{key}: attributed checkers interpretation missing")
    check(text.count('data-proof-status="FAMILY_RELATIONSHIP_UNVERIFIED"') == 1, f"{key}: family proof counter missing")
    check(text.count('data-proof-status="COORDINATED_PLACEMENT_UNPROVED"') == 1, f"{key}: placement proof counter missing")
    check(text.count('data-proof-status="PERSONAL_WRONGDOING_UNPROVED"') == 1, f"{key}: personal wrongdoing proof counter missing")
    check(text.count('data-evidence-status="LINKEDIN_EXPERIENCE_CAPTURE_PRESERVED"') == 1, f"{key}: LinkedIn capture explanation missing")
    check("4/4" in text and "0/1" in text, f"{key}: evidence scorecard missing")
    check("Gil Marer" in text and ("pawn" in text or "peón" in text), f"{key}: checkers allegation is not expressly attributed")
    check('id="achm-ac-hotel-tenerife"' in text, f"{key}: ACHM / AC Hotel Tenerife section missing")
    check(all(caepr_id in text for caepr_id in ("PD-SP-O-0007", "PD-SP-O-0077", "PD-SP-O-0078", "PD-SP-O-0079", "PD-SP-S-0011")), f"{key}: ACHM/hotel identity chain incomplete")
    check("22 February 2018" in text or "22 febrero 2018" in text, f"{key}: management-contract date missing")
    check("0.25%" in text or "0,25%" in text, f"{key}: management-fee control missing")
    check(
        "does not prove that he worked on AC Hotel Tenerife" in text
        or "not proof that he worked on AC Hotel Tenerife" in text
        or "no prueba que trabajara en AC Hotel Tenerife" in text,
        f"{key}: personal-project boundary missing",
    )
    for marker in (
        'data-evidence-status="LAURA_CURRENT_PROFILE_CAPTURED_RICPE_EMPLOYMENT_NOT_SHOWN"',
        'data-relationship-status="DOCUMENTED_PROFESSIONAL_PLACEMENT"',
        'data-relationship-status="ALLEGED_FERNANDO_LAURA_SIBLING_RELATIONSHIP_UNVERIFIED"',
        'data-witness-status="PROPOSED_FACT_RECORDS_CUSTODY_WITNESS_NOT_ADVERSE_ACTOR"',
        "DIRECT_RICPE_EMPLOYMENT_NOT_SHOWN",
    ):
        check(text.count(marker) == 1, f"{key}: Laura visual/evidence marker must render exactly once: {marker}")
    check(
        "Gil Marer" in text
        and ("sibling" in text.lower() or "herman" in text.lower())
        and ("unverified" in text.lower() or "no verific" in text.lower()),
        f"{key}: alleged sibling relationship must be attributed and unverified",
    )

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

check(
    texts["en_acosta"].count('id="witness-laura-aguiar-acosta"') == 1,
    "en_acosta: Laura witness anchor must be unique",
)
check(
    texts["es_acosta"].count('id="testigo-laura-aguiar-acosta"') == 1,
    "es_acosta: Laura witness anchor must be unique",
)
for key in ("en_ricpe", "es_ricpe"):
    check(texts[key].count('id="laura-aguiar-acosta"') == 1, f"{key}: Laura RICPE-page anchor must be unique")

for key in ("en_family", "es_family", "en_acosta", "es_acosta", "en_ricpe_genealogy", "es_ricpe_genealogy"):
    text = texts[key]
    check(text.count('id="aguiar-acosta-proposed-witness-pair"') == 1, f"{key}: paired witness/tree anchor must be unique")
    check("Fernando Aguiar Acosta^" in text and "Laura Aguiar Acosta^" in text, f"{key}: exact paired identities/carets missing")
    check(
        'data-witness-status="PROPOSED_FACT_RECORDS_CUSTODY_WITNESS_PAIR_NOT_ADVERSE_ACTORS"' in text,
        f"{key}: paired proposed-witness/not-adverse status missing",
    )
    check(
        'data-relationship-status="ALLEGED_FERNANDO_LAURA_SIBLING_RELATIONSHIP_UNVERIFIED"' in text,
        f"{key}: attributed/unverified sibling status missing",
    )
    check("Gil Marer" in text and ("unverified" in text.lower() or "no verific" in text.lower()), f"{key}: sibling attribution/proof limit missing")
    check("fernando-aguiar-acosta--linkedin-profile--20260828.png" in text, f"{key}: Fernando profile asset missing")
    check("laura-aguiar-acosta--linkedin-profile--20260828.jpg" in text, f"{key}: Laura profile asset missing")
    check("Sun Park, currently marketed as MYND Yaiza" in text or "Sun Park, actualmente comercializado como MYND Yaiza" in text, f"{key}: controlled Sun Park nomenclature missing")

for key in ("en_family", "es_family"):
    text = texts[key]
    check("laura-aguiar-acosta-linkedin-experience-user-supplied-20260828.jpg" in text, f"{key}: Laura native experience exhibit missing")
    check("five-person denominator" in text or "denominador confirmado de cinco personas" in text, f"{key}: confirmed-family denominator boundary missing")
    check("irea-colliers-meridian-sun-park/" in text, f"{key}: unitary reciprocal link missing")
    check("ric-private-equity-sun-park/" in text, f"{key}: RICPE genealogy reciprocal link missing")

evidence = (ROOT / "evidence/osint/2026-08-28-irea-colliers-meridian-fernando-aguiar-acosta.md").read_text(encoding="utf-8")
check("@" not in evidence, "public derivative contains an email address marker")
check("PSRC-IREA-2017-01" in evidence and "PSRC-IREA-2017-05" in evidence, "opaque private-source classes incomplete")
check("not “Fernando Acosta Matos”" in evidence, "identity correction missing from evidence note")
check("Documented organisational overlap; personal-project link open" in evidence, "inference boundary missing from evidence note")
check("ACHM / AC Hotel Tenerife architecture" in evidence, "ACHM hotel architecture missing from evidence note")
check("does not prove that Fernando Aguiar Acosta personally worked on" in evidence, "Fernando/AC Hotel Tenerife limit missing")
check("4/4 PUBLIC-PROFILE PLACEMENTS DOCUMENTED" in evidence, "finite 4/4 résumé denominator missing from evidence note")
check("Marer's attributed investigative hypothesis" in evidence, "pawn/plant attribution boundary missing from evidence note")
check("b9bd97a3a49c35ec230fae8170e1e521fa161ab4afe0a196027192e785f07dd9" in evidence, "LinkedIn capture fingerprint missing")
check("user-supplied native" in evidence.lower() and "repository-preserved" in evidence.lower(), "Laura native screenshot custody statement missing")
check("PD-SP-P-0095" in evidence and "Laura Aguiar Acosta" in evidence, "Laura identity missing from evidence note")
check("Canarian Hospitality" in evidence and "July–August 2024" in evidence, "Laura documented placement missing from evidence note")
check("does not show direct RIC Private Equity employment" in evidence, "Laura direct-RICPE-employment correction missing from evidence note")
check("Gil Marer identifies Laura and Fernando as siblings" in evidence, "Laura sibling attribution missing from evidence note")
check("independently proves that relationship" in evidence, "Laura sibling non-proof boundary missing from evidence note")
check(LAURA_CAPTURE_SHA256 in evidence, "Laura LinkedIn capture fingerprint missing from evidence note")
check(FERNANDO_PROFILE_SHA256 in evidence, "Fernando profile-photo fingerprint missing from evidence note")
check(LAURA_PROFILE_SHA256 in evidence, "Laura profile-photo fingerprint missing from evidence note")
sources_path = ROOT / "research/lender-of-record-liability/data/sources.json"
sources = load(sources_path)
source_by_id = {record.get("id"): record for record in sources}
check("SRC-FINANCECOMMUNITY-FERNANDO-HOTEL-FINANCE-2026" in source_by_id, "2026 hotel-finance source missing")
source_id_set = set(source_by_id)
check(LAURA_SOURCE_IDS <= source_id_set, f"Laura public-source set incomplete: {sorted(LAURA_SOURCE_IDS - source_id_set)}")
check(
    LAURA_CAPTURE_SHA256 in source_by_id.get("SRC-LINKEDIN-LAURA-AGUIAR-ACOSTA-2026", {}).get("notes", ""),
    "Laura source record lacks capture fingerprint",
)
check(
    "does not show direct RIC Private Equity employment"
    in source_by_id.get("SRC-LINKEDIN-LAURA-AGUIAR-ACOSTA-2026", {}).get("notes", ""),
    "Laura source record must reject direct RICPE employment",
)
check("Capacity correction" in evidence and "not the lender" in evidence, "IREA lender-capacity correction missing from evidence note")

unitary = load(DATA / "irea-colliers-meridian-sun-park-unitary-v1.json")
check(unitary.get("control_id") == "PD-IREA-COLLIERS-UNITARY-20260828-01", "unitary machine control ID drift")
check(len(unitary.get("capacity_lanes", [])) == 4, "unitary capacity-lane denominator must be 4")
check(len(unitary.get("people", [])) == 5, "unitary people denominator must be 5")
check("20/20 CARET_CONFIRMED" == unitary.get("identity_control", {}).get("result"), "unitary identity result drift")
check(unitary.get("adjacent_hotel_architecture", {}).get("management_operator_caepr_id") == "PD-SP-O-0077", "ACHM management operator missing")
check(unitary.get("adjacent_hotel_architecture", {}).get("establishment_caepr_id") == "PD-SP-S-0011", "AC Hotel Tenerife identity missing")
check(unitary.get("cv_sequence_interpretation", {}).get("score") == "4/4 PUBLIC-PROFILE PLACEMENTS DOCUMENTED", "4/4 machine score drift")
check(unitary.get("cv_sequence_interpretation", {}).get("attributed_checkers_hypothesis", {}).get("status") == "ATTRIBUTED_INVESTIGATIVE_HYPOTHESIS_NOT_ESTABLISHED_FACT", "checkers attribution status drift")
check(unitary.get("cv_sequence_interpretation", {}).get("proof_counters", {}).get("family_relationship_established") == "0/1", "family proof counter drift")
check(unitary.get("cv_sequence_interpretation", {}).get("proof_counters", {}).get("coordinated_placement_established") == "0/1", "placement proof counter drift")
check(unitary.get("public_profile_capture", {}).get("sha256") == "b9bd97a3a49c35ec230fae8170e1e521fa161ab4afe0a196027192e785f07dd9", "LinkedIn capture hash drift")
check(unitary.get("public_profile_capture", {}).get("pixel_dimensions") == {"width": 1363, "height": 936}, "LinkedIn capture dimensions drift")
check(unitary.get("relationship_presentation", {}).get("documented_professional_edge", {}).get("visual_code") == "SOLID_BURGUNDY", "documented RICPE visual code drift")
check(unitary.get("relationship_presentation", {}).get("provisional_family_edge", {}).get("visual_code") == "DASHED_AMBER", "provisional family visual code drift")
laura_capture = unitary.get("laura_public_profile_capture", {})
check(laura_capture.get("sha256") == LAURA_CAPTURE_SHA256, "Laura LinkedIn capture hash drift")
check(laura_capture.get("pixel_dimensions") == {"width": 691, "height": 1536}, "Laura LinkedIn capture dimensions drift")
check(
    laura_capture.get("repository_path")
    == "assets/evidence/aguiar-acosta/laura-aguiar-acosta-linkedin-experience-user-supplied-20260828.jpg",
    "Laura repository exhibit path drift",
)
check(
    laura_capture.get("finding")
    == "DIRECT_RICPE_EMPLOYMENT_NOT_SHOWN; DOCUMENTED_CANARIAN_HOSPITALITY_PLACEMENT",
    "Laura capture finding drift",
)
laura_witness = unitary.get("laura_witness_presentation", {})
check(laura_witness.get("subject_caepr_id") == "PD-SP-P-0095", "Laura witness identity missing from unitary record")
check(
    laura_witness.get("classification") == "PROPOSED_FACT_AND_RECORDS_CUSTODY_WITNESS_NOT_ADVERSE_ACTOR",
    "Laura witness/adverse-actor boundary drift",
)
check(
    laura_witness.get("documented_professional_edge", {}).get("to_caepr_id") == "PD-SP-O-0019"
    and laura_witness.get("documented_professional_edge", {}).get("status") == "DOCUMENTED_PROFESSIONAL_PLACEMENT"
    and laura_witness.get("documented_professional_edge", {}).get("visual_code") == "SOLID_BURGUNDY",
    "Laura documented Canarian Hospitality edge drift",
)
check(
    laura_witness.get("direct_ricpe_employment")
    == {"shown": False, "status": "DIRECT_RICPE_EMPLOYMENT_NOT_SHOWN"},
    "Laura direct-RICPE-employment non-finding drift",
)
check(
    laura_witness.get("alleged_sibling_edge", {}).get("to_caepr_id") == "PD-SP-P-0088"
    and laura_witness.get("alleged_sibling_edge", {}).get("attributed_to") == "Gil Marer"
    and laura_witness.get("alleged_sibling_edge", {}).get("status")
    == "ALLEGED_FERNANDO_LAURA_SIBLING_RELATIONSHIP_UNVERIFIED"
    and laura_witness.get("alleged_sibling_edge", {}).get("visual_code") == "DASHED_AMBER",
    "Laura-Fernando attributed sibling edge drift",
)
check(
    set(laura_witness.get("excluded_edges", [])) == {"IREA", "Colliers", "Project Meridian"},
    "Laura IREA/Colliers/Meridian exclusion boundary drift",
)
profile_portraits = unitary.get("profile_portraits", {})
check(profile_portraits.get("fernando_aguiar_acosta", {}).get("sha256") == FERNANDO_PROFILE_SHA256, "Fernando profile portrait hash drift")
check(profile_portraits.get("laura_aguiar_acosta", {}).get("sha256") == LAURA_PROFILE_SHA256, "Laura profile portrait hash drift")
check(
    unitary.get("nomenclature_control", {}).get("physical_asset_en")
    == "Sun Park, currently marketed as MYND Yaiza",
    "Sun Park/MYND English nomenclature control missing",
)
check(
    unitary.get("nomenclature_control", {}).get("physical_asset_es")
    == "Sun Park, actualmente comercializado como MYND Yaiza",
    "Sun Park/MYND Spanish nomenclature control missing",
)
check(LAURA_SOURCE_IDS <= set(unitary.get("source_refs", [])), "Laura source references missing from unitary record")
unitary_blob = json.dumps(unitary, ensure_ascii=False)
check_no_unsupported_laura_ricpe_employment(unitary_blob, "unitary JSON")

sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
check("/en/irea-colliers-meridian-sun-park/" in sitemap, "EN unitary route absent from sitemap")
check("/es/irea-colliers-meridian-sun-park/" in sitemap, "ES unitary route absent from sitemap")
check("/en/acosta-matos-family/" in sitemap, "EN family route absent from sitemap")
check("/es/acosta-matos-familia/" in sitemap, "ES family route absent from sitemap")
family_sitemap = (ROOT / "sitemap-acosta-matos-family.xml").read_text(encoding="utf-8")
check("/en/acosta-matos-family/" in family_sitemap and "/es/acosta-matos-familia/" in family_sitemap, "dedicated family sitemap incomplete")
robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
check("sitemap-acosta-matos-family.xml" in robots, "family sitemap absent from robots.txt")
corrections = (ROOT / "archive/CORRECTION_REGISTER.md").read_text(encoding="utf-8")
check("| CR-130 |" in corrections, "CR-130 Laura/Fernando continuity correction missing")
check(
    "Sun Park, currently marketed as MYND Yaiza" in corrections
    and "direct employment by RIC Private Equity" in corrections
    and "confirmed five-person denominator" in corrections,
    "CR-130 proof and nomenclature boundaries incomplete",
)

if failures:
    print("IREA / RICPE / COLLIERS CONTINUITY: FAIL")
    for failure in failures:
        print(f" - {failure}")
    raise SystemExit(1)

print("IREA / RICPE / COLLIERS CONTINUITY: PASS")
print(" - finite identity census: 20/20 CARET_CONFIRMED")
print(" - two-Fernando identity separation: PASS")
print(" - bilingual IREA, RICPE, Colliers and witness interlinks: PASS")
print(" - holder / servicer / adviser / legal-adviser capacity separation: PASS")
print(" - 2026 independent hotel-finance corroboration with project/family limits: PASS")
print(" - ACHM / Belagua / Hotel Project Tenerife / AC Hotel Tenerife architecture: PASS")
print(" - solid documented RICPE edge / dashed provisional family edge: PASS")
print(" - 4/4 checkers visual / attributed hypothesis / zero-proved counters: PASS")
print(" - LinkedIn image-capture fingerprint and contextual explanation: PASS")
print(" - unique bilingual Fernando witness anchor and relationship map: PASS")
print(" - Laura identity / Canarian placement / attributed sibling / no-direct-RICPE boundary: PASS")
print(" - private-source minimization controls: PASS")

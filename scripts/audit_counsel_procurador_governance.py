#!/usr/bin/env python3
"""Fail closed on counsel/procurador perimeter and filing-lineage governance drift."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERIMETER = ROOT / "assets/data/counsel-procurador-perimeter-register-v1.json"
FILINGS = ROOT / "assets/data/counsel-filing-register-v1.json"
PROCURADORES = ROOT / "assets/data/procurador-master-register-v1.json"
GAPS = ROOT / "assets/data/counsel-procurador-gap-register-v1.json"
GOVERNANCE = ROOT / "archive/COUNSEL_PROCURADOR_FILING_LINEAGE_GOVERNANCE_30AUG2026.md"
PROTOCOL = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER_PROTOCOL.md"
GATE_MARKER = "COUNSEL_PROCURADOR_GOVERNANCE_GATE"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []

    for path in (PERIMETER, FILINGS, PROCURADORES, GAPS, GOVERNANCE, PROTOCOL):
        if not path.exists():
            fail(f"missing required control: {path.relative_to(ROOT)}", errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    perimeter = load_json(PERIMETER)
    filings = load_json(FILINGS)
    procuradores = load_json(PROCURADORES)
    gaps = load_json(GAPS)
    protocol_text = PROTOCOL.read_text(encoding="utf-8")
    governance_text = GOVERNANCE.read_text(encoding="utf-8")

    if perimeter.get("status") != "seed_control_not_complete_denominator":
        fail("perimeter register must remain explicitly non-complete until denominator reconciliation is evidenced", errors)

    professionals = {p.get("display_name"): p for p in perimeter.get("professionals", [])}
    expected_external = ("Juan Carlos Roque Prieto", "Esteban Noriega", "Álvaro Campanario")
    for name in expected_external:
        row = professionals.get(name)
        if not row:
            fail(f"missing controlled professional: {name}", errors)
            continue
        if row.get("our_perimeter") is not False or row.get("classification") != "external_opposing_dissident_side":
            fail(f"perimeter drift: {name} must remain external/opposing/dissident-side", errors)

    cristo = professionals.get("Cristo Ayose Suárez Pimentel")
    if not cristo or cristo.get("our_perimeter") is not True or cristo.get("classification") != "our_former_counsel":
        fail("Cristo Ayose Suárez Pimentel must remain in our former-counsel register", errors)
    if cristo and "Cristro Suarez Pimentel" not in cristo.get("aliases", []):
        fail("user-supplied Cristo alias/provenance spelling must remain preserved", errors)

    parrilla = professionals.get("Juan Tomás Parrilla Suárez")
    if not parrilla or "independent_from_garrigues" not in parrilla.get("classification", ""):
        fail("Juan Tomás Parrilla Suárez independence-from-Garrigues control is missing", errors)
    if parrilla and "do_not_fuse_with_Garrigues" not in parrilla.get("firm_rule", ""):
        fail("Juan Tomás Parrilla Suárez firm anti-fusion rule is missing", errors)

    javier = professionals.get("Javier Sixto Seijas")
    estefania = professionals.get("Estefanía Sixto Seijas")
    if not javier or javier.get("working_relationship") != "professional_pair_with_Estefania":
        fail("Javier Sixto Seijas-to-Estefanía working-pair control is missing", errors)
    if javier and javier.get("professional_detail", {}).get("colegiado") != "99.513":
        fail("Javier Sixto Seijas ICAM 99.513 primary-source identity control is missing", errors)
    if not estefania or estefania.get("working_relationship") != "professional_pair_with_Javier":
        fail("Estefanía Sixto Seijas-to-Javier working-pair control is missing", errors)

    if GATE_MARKER not in protocol_text:
        fail("proceedings protocol does not contain the mandatory counsel/procurador governance gate marker", errors)

    for required_phrase in (
        "Dedicated filing register",
        "Procurador/a register",
        "Future-thread completion gate",
    ):
        if required_phrase not in governance_text:
            fail(f"governance markdown missing required section: {required_phrase}", errors)

    for canonical in (
        "Cristo Ayose Suárez Pimentel",
        "Javier Sixto Seijas",
        "Estefanía Sixto Seijas",
        "María del Pilar García Coello",
        "María Luisa Díaz Vecino",
        "Adriana Hernández Díaz",
    ):
        if canonical not in governance_text:
            fail(f"governance markdown missing source-reconciled identity: {canonical}", errors)

    if filings.get("status") != "initialized_not_complete_denominator":
        fail("counsel filing register must state initialized_not_complete_denominator", errors)
    scan_status = filings.get("global_scan_status", {})
    for key in ("complete_lawyer_denominator", "complete_filing_denominator", "complete_procurador_denominator"):
        if scan_status.get(key) is not False:
            fail(f"{key} may not be true before a source-verified full scan", errors)

    filing_required = set(filings.get("required_filing_fields", []))
    minimum_filing_fields = {
        "lawyer", "side_perimeter", "client_party", "procurador", "procurador_status",
        "authority_personacion_status", "proceeding_id", "filing_title", "document_ref",
        "court_laj_response_status", "appeal_followup_status", "timeline_event_ref", "verification_status"
    }
    missing_schema = sorted(minimum_filing_fields - filing_required)
    if missing_schema:
        fail(f"filing schema missing required linkage fields: {', '.join(missing_schema)}", errors)

    filing_professionals = {p.get("display_name"): p for p in filings.get("professional_registers", [])}
    for name in professionals:
        if name not in filing_professionals:
            fail(f"no dedicated initialized filing register for seed professional: {name}", errors)

    javier_filings = filing_professionals.get("Javier Sixto Seijas", {}).get("filings", [])
    required_filing_ids = {
        "RPL-3304-2025-LPB-20260724-AC-REPOSICION-ALEGACIONES",
        "RPL-3304-2025-AWESWELL-20260724-AC-REPOSICION-ALEGACIONES",
    }
    located_filing_ids = {row.get("filing_id") for row in javier_filings}
    if not required_filing_ids.issubset(located_filing_ids):
        fail("the two source-verified Javier Sixto Seijas RPL 3304/2025 filings must remain promoted", errors)
    for row in javier_filings:
        missing = [field for field in filings.get("required_filing_fields", []) if field not in row]
        if missing:
            fail(f"filing {row.get('filing_id')} missing required fields: {', '.join(missing)}", errors)
        if row.get("lawyer") != "Javier Sixto Seijas":
            fail(f"filing attribution drift for {row.get('filing_id')}", errors)

    if procuradores.get("status") != "initialized_denominator_not_yet_established":
        fail("procurador register must explicitly state that the denominator is not yet established", errors)
    if procuradores.get("denominator_status", {}).get("complete") is not False:
        fail("procurador denominator must remain false until verified", errors)

    proc_rows = {p.get("canonical_name"): p for p in procuradores.get("procuradores", [])}
    required_procuradores = {
        "María del Pilar García Coello",
        "María Luisa Díaz Vecino",
        "Adriana Hernández Díaz",
    }
    missing_procuradores = sorted(required_procuradores - set(proc_rows))
    if missing_procuradores:
        fail(f"verified procuradoras missing from master register: {', '.join(missing_procuradores)}", errors)
    if procuradores.get("denominator_status", {}).get("known_count") != len(proc_rows):
        fail("procurador known_count must equal promoted source-verified rows", errors)
    for name, row in proc_rows.items():
        missing = [field for field in procuradores.get("required_fields", []) if field not in row]
        if missing:
            fail(f"procurador {name} missing required fields: {', '.join(missing)}", errors)

    allowed_gap_statuses = set(gaps.get("allowed_statuses", []))
    gap_rows = {g.get("gap_id"): g for g in gaps.get("gaps", [])}
    for gap in gaps.get("gaps", []):
        if gap.get("status") not in allowed_gap_statuses:
            fail(f"invalid gap status for {gap.get('gap_id')}", errors)
        for field in ("gap_id", "gap_type", "what_missing", "why_it_matters", "next_retrieval_route", "status"):
            if field not in gap:
                fail(f"gap {gap.get('gap_id')} missing field {field}", errors)
    if gap_rows.get("CP-GAP-001", {}).get("status") != "RESOLVED_VERIFIED":
        fail("Cristo canonical identity gap must remain resolved with provenance preserved", errors)
    if gap_rows.get("CP-GAP-002", {}).get("status") != "RESOLVED_VERIFIED":
        fail("Javier canonical identity gap must remain resolved from primary procedural sources", errors)
    if gap_rows.get("CP-GAP-003", {}).get("status") != "SOURCE_LOCATED_REVIEW_PENDING":
        fail("Estefanía identity/file-attribution gap must remain source-located but filing-attribution controlled", errors)
    for open_gap in ("CP-GAP-004", "CP-GAP-005", "CP-GAP-006", "CP-GAP-007", "CP-GAP-008", "CP-GAP-009", "CP-GAP-010"):
        if gap_rows.get(open_gap, {}).get("status") != "OPEN":
            fail(f"{open_gap} must remain open until its evidential denominator/authority issue is resolved", errors)
    if gap_rows.get("CP-GAP-010", {}).get("proceeding_id") != "LZ-REF-044 / 1304/2014":
        fail("CP-GAP-010 must remain attached to the unresolved Arrecife 1304/2014 reference", errors)

    if errors:
        print("Counsel/procurador governance audit FAILED")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Counsel/procurador governance audit PASSED")
    print(f"Controlled professionals checked: {len(professionals)}")
    print(f"Dedicated filing registers: {len(filing_professionals)}")
    print(f"Source-verified Javier filings promoted: {len(javier_filings)}")
    print(f"Verified procuradoras currently promoted: {len(proc_rows)}")
    print(f"Open/controlled gaps: {len(gaps.get('gaps', []))}")
    print("Denominator completeness remains explicitly false pending full primary-source reconciliation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

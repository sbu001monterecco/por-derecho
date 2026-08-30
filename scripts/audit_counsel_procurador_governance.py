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

    cristro = professionals.get("Cristro Suarez Pimentel")
    if not cristro or cristro.get("our_perimeter") is not True or cristro.get("classification") != "our_former_counsel":
        fail("Cristro Suarez Pimentel must remain in our former-counsel seed register pending name verification", errors)

    parrilla = professionals.get("Juan Tomás Parrilla Suárez")
    if not parrilla or "independent_from_garrigues" not in parrilla.get("classification", ""):
        fail("Juan Tomás Parrilla Suárez independence-from-Garrigues control is missing", errors)
    if parrilla and "do_not_fuse_with_Garrigues" not in parrilla.get("firm_rule", ""):
        fail("Juan Tomás Parrilla Suárez firm anti-fusion rule is missing", errors)

    javier = professionals.get("Javier")
    estefania = professionals.get("Estefanía")
    if not javier or javier.get("working_relationship") != "professional_pair_with_Estefania":
        fail("Javier-to-Estefanía working-pair control is missing", errors)
    if not estefania or estefania.get("working_relationship") != "professional_pair_with_Javier":
        fail("Estefanía-to-Javier working-pair control is missing", errors)

    if GATE_MARKER not in protocol_text:
        fail("proceedings protocol does not contain the mandatory counsel/procurador governance gate marker", errors)

    for required_phrase in (
        "Dedicated filing register",
        "Procurador/a register",
        "Future-thread completion gate",
    ):
        if required_phrase not in governance_text:
            fail(f"governance markdown missing required section: {required_phrase}", errors)

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

    if procuradores.get("status") != "initialized_denominator_not_yet_established":
        fail("procurador register must explicitly state that the denominator is not yet established", errors)
    if procuradores.get("denominator_status", {}).get("complete") is not False:
        fail("procurador denominator must remain false until verified", errors)

    allowed_gap_statuses = set(gaps.get("allowed_statuses", []))
    for gap in gaps.get("gaps", []):
        if gap.get("status") not in allowed_gap_statuses:
            fail(f"invalid gap status for {gap.get('gap_id')}", errors)
        for field in ("gap_id", "gap_type", "what_missing", "why_it_matters", "next_retrieval_route", "status"):
            if field not in gap:
                fail(f"gap {gap.get('gap_id')} missing field {field}", errors)

    if errors:
        print("Counsel/procurador governance audit FAILED")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Counsel/procurador governance audit PASSED")
    print(f"Seed professionals checked: {len(professionals)}")
    print(f"Dedicated filing registers initialized: {len(filing_professionals)}")
    print(f"Verified procuradores currently promoted: {len(procuradores.get('procuradores', []))}")
    print(f"Open/controlled gaps: {len(gaps.get('gaps', []))}")
    print("Denominator completeness remains explicitly false pending full primary-source reconciliation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

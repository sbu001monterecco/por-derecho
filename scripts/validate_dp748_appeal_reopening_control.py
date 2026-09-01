#!/usr/bin/env python3
"""Fail closed on DP 748/2026 appeal/reopening lineage and public-safe boundaries."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
CONTROL = DATA / "dp748-2026-appeal-reopening-control-v1.json"
MASTER = ROOT / "archive" / "PROCEEDINGS_MASTER_REGISTER.csv"
INDEX = DATA / "matter-identity-registry-v1.json"
PROCEEDINGS = DATA / "matter-identity-registry-v1.proceedings.json"
JUDICIAL = DATA / "la-laguna-judicial-actors-canonical-interlink-control-v1.json"
FILINGS = DATA / "counsel-filing-register-v1.json"
PROCURADORES = DATA / "procurador-master-register-v1.json"
GAPS = DATA / "counsel-procurador-gap-register-v1.json"

EXPECTED_SOURCE_HASHES = {
    "DP748-SRC-DENUNCIA-20260204": "f48e4d7ca705064bce04a2d323f083aa4cb02de4a8ee20b21f2e26c7565d2b28",
    "DP748-SRC-REFORMA-APELACION-20260417": "16ad4333afacc2df27399d9b8e6329af6af88185992a34b4ba177a0de6815252",
    "DP748-SRC-PROVIDENCIA-20260520": "429a2728aedbad73cdceb9b4ab40899e4e46c5f09c9c0b3369347d66d6965d04",
    "DP748-SRC-FISCAL-20260608": "64a010f4980790615e8c2f4b0feebe0268af00a3c64b357ef4986927c4c50a41",
    "DP748-SRC-AUTO-20260716": "32f70f813113870609127b5f35e2a8859c734236efe1577cdd3dc7703813d8a4",
    "DP748-SRC-NOTIFICATION-20260901": "54ddaf2954a1ab51c3a556f43f432f7ddee0efbf9fd6ffd51d25d3f3622078dc",
    "ETJ163-SRC-AUCTION-EDICT": "fc1abc2261ccd3244bfdc46d23edc21ca5f723540052fd2673f614a7fa1a3beb",
    "ETJ163-SRC-CUATRECASAS-20250425": "49b54b3820a233e30783bc18e301d8a79148f09b7c852d1b6b4ea7cb8be1632e",
    "ETJ163-SRC-REPOSICION-20260626": "9cdd1f0d2a0c954aacb3695ca7045f3bf4ec73a605c95088407b2f5c97473f23",
    "ETJ163-SRC-DIOR-20260728": "6c8fdcf5f0a8d1e68d3144916979197aaa5b10e655d7907a708d72f0abc97127",
}


def load(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def records(path: Path):
    return load(path).get("records", [])


def main() -> int:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    for path in (CONTROL, MASTER, INDEX, PROCEEDINGS, JUDICIAL, FILINGS, PROCURADORES, GAPS):
        require(path.is_file(), f"missing control: {path.relative_to(ROOT)}")
    if errors:
        return finish(errors)

    control = load(CONTROL)
    require(
        control.get("schema") == "por-derecho.dp748-2026-appeal-reopening-control.v1",
        "unexpected DP 748 control schema",
    )
    proceeding = control.get("proceeding", {})
    require(proceeding.get("master_id") == "TF-CRI-003", "DP 748 Master ID drift")
    require(proceeding.get("caepr_id") == "PD-SP-R-0003", "DP 748 CAEPR ID drift")
    require(proceeding.get("court_caepr_id") == "PD-SP-I-0037", "DP 748 court ID drift")
    require(proceeding.get("nig") == "3802343220260002351", "DP 748 NIG drift")

    index = load(INDEX)
    identity_records = {}
    for descriptor in index.get("parts", []):
        path = DATA / descriptor.get("path", "")
        if path.is_file():
            identity_records.update({row.get("id"): row for row in records(path)})
    expected_identities = {
        "PD-SP-R-0003": "DP 748/2026 — La Laguna",
        "PD-SP-I-0037": "Plaza nº 4 del Tribunal de Instancia (Sección Instrucción) de San Cristóbal de La Laguna",
        "PD-SP-P-0001": "Gil Marer",
        "PD-SP-O-0049": "Cuatrecasas, Gonçalves Pereira, S.L.P.",
        "PD-SP-P-0062": "Carlos Llamas Sanz",
        "PD-SP-P-0067": "Adriana Hernández Díaz",
        "PD-SP-P-0147": "Graciela Pérez-Valencia Díaz",
        "PD-SP-P-0148": "María del Pilar Luis Medina",
        "PD-SP-P-0158": "Teresa Morenés Basabe",
        "PD-SP-P-0159": "José Javier Bueno Mesa",
        "PD-SP-P-0160": "María Francisca Sánchez Álvarez",
    }
    for identity_id, expected_name in expected_identities.items():
        require(identity_records.get(identity_id, {}).get("name") == expected_name, f"missing/drifted identity {identity_id}")
    require(
        identity_records.get("PD-SP-P-0146", {}).get("name") == "Simon Peter Thompson",
        "current-main PD-SP-P-0146 identity was overwritten by the stale PR #1324 Carlos proposal",
    )
    require(
        identity_records.get("PD-SP-P-0062", {}).get("name") == "Carlos Llamas Sanz",
        "Carlos Llamas must remain canonical PD-SP-P-0062",
    )

    p0 = control.get("p0_appeal_control", {})
    require(p0.get("subsidiary_appeal_filed") == "VERIFIED", "subsidiary appeal filing not locked")
    require(
        p0.get("subsidiary_appeal_admitted") == "VERIFIED_BY_20MAY_PROVIDENCIA_INTERPOSED_IN_TIME_AND_FORM",
        "20-May admission state not locked",
    )
    require(p0.get("article_766_4_transfer_to_appellant") == "NOT_LOCATED", "Article 766.4 gap was silently closed")
    require(p0.get("transmission_to_audiencia") == "NOT_LOCATED", "Audiencia transmission was invented")
    require(p0.get("appellate_roll") == "NOT_LOCATED", "appellate roll was invented")
    require(p0.get("tf_app_004") == "UNVERIFIED_PLACEHOLDER", "TF-APP-004 was over-promoted")
    require(p0.get("protective_operational_deadline") == "FILE_04SEP2026_OR_EARLIER", "protective deadline drift")

    deficiency = {row.get("deficiency"): row for row in control.get("judicial_deficiency_matrix", [])}
    require(deficiency.get("exact_act", {}).get("record_before_criminal_court") == "PARTIAL", "exact-act assessment drift")
    require(deficiency.get("concrete_property", {}).get("record_before_criminal_court") == "INSUFFICIENT", "property assessment drift")
    require(deficiency.get("minimum_criminal_indicia", {}).get("record_before_criminal_court") == "INCOMPLETE", "indicia assessment drift")
    require(control.get("narrow_case_definition", {}).get("property") == "Finca registral 8584 only", "narrow property core drift")

    source_rows = control.get("source_register", [])
    source_by_id = {row.get("source_id"): row for row in source_rows}
    require(len(source_by_id) == len(source_rows), "duplicate DP/ETJ source ID")
    for source_id, expected_hash in EXPECTED_SOURCE_HASHES.items():
        require(source_by_id.get(source_id, {}).get("sha256") == expected_hash, f"source hash drift: {source_id}")
    for row in source_rows:
        require(re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", "")) is not None, f"invalid SHA-256: {row.get('source_id')}")

    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        master_rows = {row["Master_ID"]: row for row in csv.DictReader(handle)}
    dp_master = master_rows.get("TF-CRI-003", {})
    app_master = master_rows.get("TF-APP-004", {})
    etj_master = master_rows.get("TF-CIV-002", {})
    require(dp_master.get("NIG") == "3802343220260002351", "Master DP NIG missing")
    require("subsidiary appeal recorded in time and form" in dp_master.get("Appeal_or_Review", ""), "Master DP appeal posture stale")
    require(app_master.get("Is_Proceeding") == "UNVERIFIED", "TF-APP-004 must remain unverified")
    require(app_master.get("Parent_Master_ID") == "TF-CRI-003", "TF-APP-004 parent drift")
    require(etj_master.get("NIG") == "3802342120190009565", "ETJ NIG missing")

    proceeding_by_id = {row.get("id"): row for row in records(PROCEEDINGS)}
    dp_identity = proceeding_by_id.get("PD-SP-R-0003", {})
    require(dp_identity.get("competent_organ") == "PD-SP-I-0037", "DP proceeding organ link missing")
    require("TF-CRI-003" in dp_identity.get("master_register_ids", []), "DP proceeding Master link missing")

    filing_rows = {
        row.get("filing_id"): row
        for professional in load(FILINGS).get("professional_registers", [])
        for row in professional.get("filings", [])
    }
    for filing_id in (
        "DP748-2026-GIL-20260417-REFORMA-SUB-APELACION",
        "DP748-2026-GIL-20260626-SINTESIS",
        "ETJ163-2020-MATKATOR-20260626-REPOSICION-SUSPENSION",
        "ETJ163-2020-CUATRECASAS-20250425-ALEGACIONES-FINCAS",
    ):
        require(filing_id in filing_rows, f"missing filing lineage {filing_id}")

    procuradores = {row.get("procurador_id"): row for row in load(PROCURADORES).get("procuradores", [])}
    require(procuradores.get("PROC-ADRIANA-HERNANDEZ-DIAZ", {}).get("caepr_id") == "PD-SP-P-0067", "Adriana register link drift")
    require(procuradores.get("PROC-JOSE-JAVIER-BUENO-MESA", {}).get("caepr_id") == "PD-SP-P-0159", "Bueno register link drift")

    gaps = {row.get("gap_id"): row for row in load(GAPS).get("gaps", [])}
    require(gaps.get("CP-GAP-012", {}).get("status") == "SOURCE_LOCATED_REVIEW_PENDING", "P0 appeal gap status drift")
    require(gaps.get("CP-GAP-014", {}).get("status") == "RESOLVED_VERIFIED", "same-day filing classification not resolved")
    for gap_id in ("CP-GAP-015", "CP-GAP-016", "CP-GAP-017", "CP-GAP-018"):
        require(gaps.get(gap_id, {}).get("status") == "OPEN", f"{gap_id} was silently closed")

    judicial = load(JUDICIAL)
    judicial_dp = next((row for row in judicial.get("proceedings", []) if row.get("master_id") == "TF-CRI-003"), {})
    require(judicial_dp.get("organ_caepr_id") == "PD-SP-I-0037", "judicial control DP organ drift")
    require({row.get("caepr_id") for row in judicial_dp.get("judges", [])} == {"PD-SP-P-0147"}, "judicial control judge drift")
    require({row.get("caepr_id") for row in judicial_dp.get("lajs", [])} == {"PD-SP-P-0148"}, "judicial control LAJ drift")

    public_blob = CONTROL.read_text(encoding="utf-8")
    forbidden = {
        "email address": r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}",
        "private-provider URL": r"https?://(?:mail|drive|docs)\.google\.com/",
        "LexNET message identifier": r"(?i)IdLexNet",
        "Spanish personal ID": r"(?i)\b(?:DNI|NIE)\b",
    }
    for label, pattern in forbidden.items():
        require(re.search(pattern, public_blob, re.IGNORECASE) is None, f"public-safe control exposes forbidden {label}")

    return finish(errors)


def finish(errors: list[str]) -> int:
    if errors:
        print("DP 748 appeal/reopening control: FAIL")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("DP 748 appeal/reopening control: PASS")
    print(" - admitted subsidiary appeal preserved; Article 766.4/remittal/roll gaps remain open")
    print(" - canonical actors, filings, properties, source hashes and Master links reconcile")
    print(" - TF-APP-004 remains an unverified placeholder")
    print(" - source-safe public boundary passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

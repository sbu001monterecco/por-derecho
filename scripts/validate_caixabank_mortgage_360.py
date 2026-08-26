#!/usr/bin/env python3
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "es": ROOT / "es/reclamacion-caixabank-valencia/index.html",
    "en": ROOT / "en/caixabank-valencia-claim/index.html",
    "control": ROOT / "archive/CAIXABANK_MORTGAGE_SWAP_ACCOUNT_360_CONTROL_26AUG2026.md",
    "declaration": ROOT / "archive/declarations/014_WITNESS_GIL_PERIMETER_MORTGAGE_SWAP_ACCOUNTS_EXECUTION_20260826.md",
    "index": ROOT / "archive/declarations/INDEX.md",
    "gaps": ROOT / "archive/MISSING_EVIDENCE_REGISTER.md",
    "closeout": ROOT / "docs/deletion-audits/2026-08-26-caixabank-mortgage-swap-360-thread.md",
    "sitemap": ROOT / "sitemap-banking-recovery.xml",
    "actors": ROOT / "research/lender-of-record-liability/data/actors.json",
    "proceedings": ROOT / "research/lender-of-record-liability/data/proceedings.json",
    "transfers": ROOT / "research/lender-of-record-liability/data/transfers.json",
    "instruments": ROOT / "research/lender-of-record-liability/data/instruments.json",
}

REQUIRED = {
    "es": [
        'id="alegacion-paquete-financiero"',
        "119.000 € brutos",
        "210.000 €",
        "29-Nov-2011",
        "1-Ene-2012",
        "SAREB → PH122 → CAM",
        "no titular probado del crédito",
        "TAE 3,717 %",
        "no sustituía jurídicamente provisiones",
        "Actualizado el 26 de agosto de 2026",
    ],
    "en": [
        'id="financial-package-allegation"',
        "€119,000 gross",
        "€210,000",
        "29-Nov-2011",
        "1-Jan-2012",
        "SAREB → PH122 → CAM",
        "not a proved credit holder",
        "TAE 3.717%",
        "did not legally replace the bank's provisions",
        "Updated 26 August 2026",
    ],
    "control": [
        "one economic package",
        "actor by actor",
        "€55,000 × 2 is €110,000",
        "Bankia burofax",
        "provision-transfer theories",
    ],
    "declaration": [
        "**N.º:** 014",
        "**Atribución:** `S1`",
        "**Versión:** `V2`",
        "55.000 × 2 = 110.000",
        "no sustituye la adopción personal",
    ],
    "index": [
        "| 014 | 2026-08-26 |",
        "siguiente declaración disponible es **017**",
    ],
    "gaps": ["| ME-092 |", "€60k", "€59k", "119.000 € brutos"],
    "closeout": ["THREAD_REASONING_CONTINUITY", "PRIMARY_EVIDENCE_COMPLETENESS"],
    "sitemap": ["es/reclamacion-caixabank-valencia/", "en/caixabank-valencia-claim/", "2026-08-26"],
    "actors": ["ACT-BFA", "ACT-AWESWELL", "ACT-CAIXABANK", "not_established_as_credit_holder_or_assignee"],
    "proceedings": ["ACT-AWESWELL", "ACT-CAIXABANK", "46250-42-1-2023-0049579"],
    "transfers": ["TR-2011-CAJA-INSULAR-BFA", "TR-2011-BFA-BANKIA", "TR-2021-BANKIA-CAIXABANK"],
    "instruments": ["counterparty_successor_actor_refs", "2012-01-01", "5.55"],
}


def main() -> None:
    failures = []
    for key, path in FILES.items():
        if not path.is_file():
            failures.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in REQUIRED[key]:
            if marker not in text:
                failures.append(f"{path.relative_to(ROOT)} missing marker: {marker}")

    es = FILES["es"].read_text(encoding="utf-8") if FILES["es"].is_file() else ""
    en = FILES["en"].read_text(encoding="utf-8") if FILES["en"].is_file() else ""
    if es.count("<table") != en.count("<table"):
        failures.append("ES/EN table-count parity failed")
    if es.count("<section") != en.count("<section"):
        failures.append("ES/EN section-count parity failed")

    try:
        ET.parse(FILES["sitemap"])
    except Exception as exc:
        failures.append(f"sitemap-banking-recovery.xml is invalid XML: {exc}")

    try:
        actors = {row["id"]: row for row in json.loads(FILES["actors"].read_text(encoding="utf-8"))}
        proceedings = {row["id"]: row for row in json.loads(FILES["proceedings"].read_text(encoding="utf-8"))}
        transfers = json.loads(FILES["transfers"].read_text(encoding="utf-8"))
        instruments = json.loads(FILES["instruments"].read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"lender structured data is invalid JSON: {exc}")
    else:
        valencia = proceedings.get("PROC-VALENCIA-1859-2023-9", {})
        if valencia.get("claimant_actor_refs") != ["ACT-AWESWELL"]:
            failures.append("Valencia claimant capacity must be Aweswell")
        if valencia.get("defendant_actor_refs") != ["ACT-CAIXABANK"]:
            failures.append("Valencia defendant capacity must be CaixaBank")
        haya_limits = actors.get("ACT-HAYA", {}).get("capacity_limits", [])
        if "not_established_as_credit_holder_or_assignee" not in haya_limits:
            failures.append("Haya non-holder capacity lock missing")
        if any("ACT-HAYA" in row.get("holder_chain_actor_refs", []) for row in instruments):
            failures.append("Haya appears in an instrument holder chain")
        if any(row.get("transferor_actor_ref") == "ACT-HAYA" or row.get("transferee_actor_ref") == "ACT-HAYA" for row in transfers):
            failures.append("Haya appears as a transfer endpoint")

    if failures:
        raise SystemExit("\n".join(f"FAIL: {item}" for item in failures))
    print("PASS: CaixaBank mortgage/swap/account 360 controls and ES/EN parity")


if __name__ == "__main__":
    main()

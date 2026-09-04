#!/usr/bin/env python3
"""One-record migration for GC-HC-010 / Reg. No. 24.

This migration removes the stale TSJ-origin/current-custodian inference from the
canonical Proceedings Master CSV, preserves Reg. No. 24 as a reception/control
record with a dependent 25 June supplement, then regenerates the allowlisted
public JSON projection using the repository's canonical builder.

The script is intentionally idempotent and changes no CSV row other than
GC-HC-010.
"""

from __future__ import annotations

import csv
import io
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
BUILDER = ROOT / "scripts/build_public_proceedings_projection.py"
TARGET_ID = "GC-HC-010"

UPDATES = {
    "Record_Type": "INTAKE_REFERENCE",
    "Is_Proceeding": "FALSE",
    "Proceeding_Class": "RECEPTION_LOCATOR_NOT_PROCEEDING",
    "Stream": "Criminal intake / judicial complaint control",
    "Geography": "Gran Canaria",
    "Origin_Organ": "Decanato / Registro y Reparto Las Palmas",
    "Current_Custodian": "Official destination not yet identified",
    "Reference": "Daily registration no. 24 / GC-HC-010",
    "Secondary_Reference": "Original 18/06/2026; dependent supplement 25/06/2026; later reported to CGPJ 169/2026",
    "NIG": "",
    "Date_or_Period": "2026-06-18; 2026-06-25",
    "Connection": "Concurso 36/2012 / judge-related complaint and dependent supplement",
    "Object_or_Purpose": "Reception/control record for complaint/notitia concerning judicial acts; one Reg. No. 24 record with dependent supplement",
    "Status": "Filed/presented under daily registration no. 24; formal allocation, current custodian and outcome unknown",
    "Latest_Known_Event": "25 Jun 2026 dependent supplement presented; combined matter later reported to CGPJ within 169/2026",
    "Appeal_or_Review": "CGPJ 169/2026 is a separate later institutional route; exact nomenclature/treatment remains to reconcile",
    "Parent_Master_ID": "",
    "Linked_Proceedings": "GC-GOV-019; GC-GOV-020; GC-JUD-001",
    "Source_Status": "SOURCE_PACKAGE_DIGITISED_ALLOCATION_OPEN",
    "Primary_Source_Anchor": "Signed 79-page Control 24 package SHA-256 1cae1912a20202c5f5779db07e77c7e1d3f0ae514676e07d3ace4dd56f6f76a0; 10-page supplement SHA-256 a552c10094a3bdbf21132f7083689d79bee39b8d51ed96de19090a3d638b7c48",
    "Repo_Canonical_Source": "archive/GC_HC_010_DECANATO24_CGPJ169_CORRECTION_04SEP2026.md",
    "Open_Reference_Gap": "Certified Decanato/reparto trail; electronic joinder/remittal metadata for 25 Jun supplement; assigned organ/NIG/current status; exact CGPJ 169/2026 document treatment",
    "Public_Treatment": "PUBLIC_SUMMARY_WITH_PROCEDURAL_LIMITS",
    "Last_Scan_Date": "2026-09-04",
    "Notes": "Canonical identity: 18 Jun complaint + 25 Jun dependent supplement = one Reg. No. 24 / GC-HC-010 filing record. Supplement retains document-level provenance but is not a separate proceeding. Do not infer TSJ/TSJC origin or current custody from intended addressee/competence framing.",
}


def serialise_row(values: list[str]) -> str:
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="")
    writer.writerow(values)
    return out.getvalue()


def main() -> int:
    if not CSV_PATH.is_file():
        raise SystemExit(f"missing canonical CSV: {CSV_PATH.relative_to(ROOT)}")

    raw = CSV_PATH.read_text(encoding="utf-8-sig")
    lines = raw.splitlines(keepends=True)
    if not lines:
        raise SystemExit("canonical CSV is empty")

    header = next(csv.reader([lines[0].rstrip("\r\n")]))
    missing = [name for name in UPDATES if name not in header]
    if missing:
        raise SystemExit(f"canonical CSV missing expected columns: {missing}")

    target_indexes = [i for i, line in enumerate(lines[1:], start=1) if line.startswith(TARGET_ID + ",")]
    if len(target_indexes) != 1:
        raise SystemExit(f"expected exactly one {TARGET_ID} row; found {len(target_indexes)}")

    index = target_indexes[0]
    original_line = lines[index]
    ending = "\r\n" if original_line.endswith("\r\n") else ("\n" if original_line.endswith("\n") else "")
    row = next(csv.reader([original_line.rstrip("\r\n")]))
    if len(row) != len(header):
        raise SystemExit(f"{TARGET_ID} row has {len(row)} fields; expected {len(header)}")

    current = dict(zip(header, row))
    stale_tsj = "TSJ Canarias" in current.get("Origin_Organ", "") or "TSJ Canarias" in current.get("Current_Custodian", "")
    already_correct = all(current.get(key, "") == value for key, value in UPDATES.items())

    if not already_correct:
        if not stale_tsj and current.get("Reference") != "Daily registration no. 24 / GC-HC-010":
            raise SystemExit(
                "GC-HC-010 no longer matches the known stale row or the intended corrected row; "
                "refusing to overwrite a newer unknown state"
            )
        for key, value in UPDATES.items():
            row[header.index(key)] = value
        lines[index] = serialise_row(row) + ending
        CSV_PATH.write_text("".join(lines), encoding="utf-8")
        print("UPDATED: canonical GC-HC-010 row")
    else:
        print("UNCHANGED: canonical GC-HC-010 row already corrected")

    subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(BUILDER), "--check"], cwd=ROOT, check=True)
    print("PASS: GC-HC-010 canonical row and public projection are coherent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

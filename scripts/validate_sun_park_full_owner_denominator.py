#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
INDEX = DATA / "sun-park-unit-owner-ledger-v1.json"
MANIFEST = DATA / "sun-park-unit-owner-ledger-v1.precam-full-denominator.json"
RECONCILIATION = DATA / "sun-park-unit-owner-ledger-v1.reconciliation.json"
IDENTITY_INDEX = DATA / "matter-identity-registry-v1.json"
REPORT = ROOT / "archive" / "SUN_PARK_FULL_PRECAM_OWNER_DENOMINATOR_IMPLEMENTATION_26AUG2026.md"
PUBLIC_ES = ROOT / "es" / "registro-propietarios-sun-park" / "index.html"
PUBLIC_EN = ROOT / "en" / "sun-park-owner-register" / "index.html"

EXPECTED_COLUMNS = [
    "record_type", "record_id", "finca_id", "urbana_id", "unit_or_label",
    "source_unit_count_or_expression", "quota_percent",
    "source_contact_classification", "source_reported_owner_label",
    "canonical_identity_ids", "association_codes", "cross_source_refs",
    "anomaly_flags", "source_variant_note",
]
EXPECTED_UNITS = {
    "109", "110", "301", "314", "403", "404", "405", "406", "407", "408",
    "454", "455", "456", "457", "458", "501", "503", "504", "505", "506",
    "507", "508", "509", "510", "511", "512", "513", "514", "551", "553",
    "554", "555", "556", "557", "558", "559", "560", "561", "562", "563",
    "564", "603", "701", "705", "708", "801", "802", "805", "807", "901",
    "902", "903", "904", "905", "906", "907", "908", "909", "910", "911",
    "914", "1-Gym", "2-Gym", "3-Juegos", "4-Juegos", "5-MiniClub",
    "6-MiniClub", "7-Super", "8-Super", "9-Super", "10-Super",
    "11-HallSuper",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    try:
        index = load(INDEX)
        manifest = load(MANIFEST)
        reconciliation = load(RECONCILIATION)

        require(index.get("control_id") == "PD-SP-UNIT-OWNER-LEDGER-001", "index control drift")
        ref = index.get("full_pre_cam_denominator_ref", {})
        require(
            ref.get("manifest_path") == MANIFEST.name,
            "full-denominator manifest pointer drift",
        )
        require(
            ref.get("data_path") == manifest.get("data_path"),
            "full-denominator data pointer drift",
        )
        require(
            manifest.get("schema")
            == "por-derecho.sun-park-unit-owner-ledger.part.precam-full-denominator.v1",
            "manifest schema drift",
        )
        require(
            manifest.get("source_id") == "SRC-PRECAM-OWNER-SCHEDULE",
            "source id drift",
        )
        data_path = DATA / manifest["data_path"]
        require(data_path.is_file(), "full denominator TSV missing")

        with data_path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            require(reader.fieldnames == EXPECTED_COLUMNS, "TSV column drift")
            rows = list(reader)

        exact = [row for row in rows if row["record_type"] == "EXACT"]
        aggregate = [row for row in rows if row["record_type"] == "AGGREGATE"]
        require(len(rows) == 74, "source row denominator must be 74")
        require(len(exact) == 72, "exact row denominator must be 72")
        require(len(aggregate) == 2, "aggregate row denominator must be two")
        require(
            len({row["record_id"] for row in rows}) == 74,
            "record ids must be unique",
        )
        require(
            {row["unit_or_label"] for row in exact} == EXPECTED_UNITS,
            "exact unit/premises set drift",
        )

        direct = [row for row in exact if row["source_contact_classification"] == "DIRECT"]
        bank = [row for row in exact if row["source_contact_classification"] == "BANCO"]
        require(len(direct) == 62, "DIRECT count drift")
        require(len(bank) == 10, "BANCO count drift")
        require(
            all(row["source_contact_classification"] in {"DIRECT", "BANCO"} for row in exact),
            "invalid source classification",
        )
        require(
            all(row["source_reported_owner_label"].strip() for row in rows),
            "empty source owner label",
        )

        finca_units: dict[str, list[str]] = defaultdict(list)
        for row in exact:
            finca_units[row["finca_id"]].append(row["unit_or_label"])
        duplicates = {finca: units for finca, units in finca_units.items() if len(units) > 1}
        require(duplicates == {"8652": ["902", "903"]}, "duplicate-finca set drift")
        for unit in ("902", "903"):
            row = next(item for item in exact if item["unit_or_label"] == unit)
            require(
                "DUPLICATE_FINCA_IN_SOURCE_SCHEDULE" in row["anomaly_flags"],
                f"source anomaly flag missing for {unit}",
            )
            require("PD-SP-REC-008" in row["cross_source_refs"], f"issue link missing for {unit}")

        matkator = [row for row in exact if "MATKATOR_SOURCE_ASSOCIATION" in row["association_codes"]]
        require(len(matkator) == 5, "Matkator source-reference count drift")
        require(
            all("PD-SP-O-0003" in row["association_codes"] for row in matkator),
            "Matkator identity link drift",
        )

        aggregate_fincas = {row["finca_id"] for row in aggregate}
        require(aggregate_fincas == {"8645+", "8508-"}, "aggregate finca expressions drift")
        require(
            all(row["canonical_identity_ids"] == "PD-SP-O-0002" for row in aggregate),
            "aggregate LPB identity drift",
        )
        require(
            all("without unit-level deconvolution" in row["source_variant_note"] for row in aggregate),
            "aggregate non-deconvolution boundary missing",
        )

        summary = manifest.get("summary", {})
        require(summary.get("exact_records") == 72, "manifest exact count drift")
        require(summary.get("aggregate_rows") == 2, "manifest aggregate count drift")
        require(summary.get("total_source_rows") == 74, "manifest source total drift")
        require(summary.get("direct_classified_exact_records") == 62, "manifest DIRECT drift")
        require(summary.get("bank_classified_exact_records") == 10, "manifest BANCO drift")
        require(summary.get("source_rows_referencing_matkator") == 5, "manifest Matkator drift")
        require(summary.get("duplicate_finca_groups") == 1, "manifest duplicate finca drift")
        require(
            summary.get("confirmed_completed_direct_lpb_transfers") == 0,
            "manifest overstates direct LPB transfers",
        )

        boundaries = " ".join(manifest.get("interpretation_boundaries", []))
        for marker in [
            "DIRECT is not treated as proof",
            "not a Registry certificate",
            "non-adverse by default",
            "never overwrite source ownership provenance",
            "not deconvolved into invented unit-level records",
        ]:
            require(marker in boundaries, f"manifest boundary missing: {marker}")
        require(
            manifest.get("common_fields", {}).get("ownership_edge", {}).get("perimeter_id")
            == "PD-SP-PER-OTHER-MINORITY-001",
            "default ownership perimeter drift",
        )

        identity_manifest = load(IDENTITY_INDEX)
        known_ids: set[str] = set()
        for descriptor in identity_manifest.get("parts", []):
            part = load(DATA / descriptor["path"])
            known_ids.update(record["id"] for record in part.get("records", []))
        local_ids = {
            item["local_identity_id"] for item in index.get("local_identities", [])
        }
        valid_ids = known_ids | local_ids
        for row in rows:
            for identity_id in filter(None, row["canonical_identity_ids"].split(";")):
                require(identity_id in valid_ids, f"unknown identity id {identity_id}")

        issues = {
            item["issue_id"]: item
            for item in reconciliation.get("reconciliation_issues", [])
        }
        require(len(issues) == 8, "reconciliation issue denominator drift")
        require("PD-SP-REC-008" in issues, "duplicate-finca issue missing")
        require(
            issues["PD-SP-REC-008"].get("finca_id") == "8652"
            and set(issues["PD-SP-REC-008"].get("unit_labels", [])) == {"902", "903"},
            "duplicate-finca issue content drift",
        )

        index_summary = index.get("summary", {})
        expected_summary = {
            "pre_cam_full_source_rows": 74,
            "pre_cam_full_exact_records": 72,
            "pre_cam_full_aggregate_rows": 2,
            "source_schedule_direct_classified_exact_records": 62,
            "source_schedule_bank_classified_exact_records": 10,
            "source_schedule_matkator_reference_rows": 5,
            "source_schedule_duplicate_finca_groups": 1,
            "open_reconciliation_issues": 8,
            "confirmed_completed_direct_lpb_transfers": 0,
        }
        for key, value in expected_summary.items():
            require(index_summary.get(key) == value, f"index summary drift: {key}")

        combined_text = (
            MANIFEST.read_text(encoding="utf-8")
            + data_path.read_text(encoding="utf-8")
            + RECONCILIATION.read_text(encoding="utf-8")
        )
        privacy_patterns = {
            "email": re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
            "phone": re.compile(r"\+\d[\d\s-]{7,}\d"),
            "container path": re.compile(r"/mnt/(?:data|home)/"),
            "Gmail id": re.compile(r"(?:mail\.google\.com|gmail-attachment|message_id)"),
            "IBAN/SWIFT": re.compile(r"\b(?:IBAN|SWIFT)\b"),
        }
        for label, pattern in privacy_patterns.items():
            require(pattern.search(combined_text) is None, f"private {label} leaked")

        require(REPORT.is_file(), "implementation report missing")
        for page in (PUBLIC_ES, PUBLIC_EN):
            require(page.is_file(), f"public route missing: {page}")
            text = page.read_text(encoding="utf-8")
            require(manifest["data_path"] in text, f"public route data link drift: {page}")
            require("72" in text and "74" in text, f"public route denominator markers missing: {page}")
            require("owner-perimeter-tokens.css" in text, f"perimeter tokens missing: {page}")

        print("SUN PARK FULL PRE-CAM OWNER DENOMINATOR: PASS")
        print(" - 74 source rows = 72 exact + 2 aggregate")
        print(" - 62 DIRECT / 10 BANCO source classifications")
        print(" - 5 Matkator source-reference rows; no ownership implication added")
        print(" - duplicate finca 8652 for units 902/903 preserved as issue PD-SP-REC-008")
        print(" - 0 completed direct LPB transfers confirmed")
        print(" - bilingual public register and privacy boundary validated")
        return 0
    except (AssertionError, KeyError, json.JSONDecodeError, csv.Error) as exc:
        print(f"SUN PARK FULL PRE-CAM OWNER DENOMINATOR: FAIL\n - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

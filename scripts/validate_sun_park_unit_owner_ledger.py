#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
INDEX = DATA / "sun-park-unit-owner-ledger-v1.json"
CLASSIFICATION = DATA / "sun-park-owner-perimeter-classification-v1.json"
IDENTITY_INDEX = DATA / "matter-identity-registry-v1.json"
PROTOCOL = ROOT / "archive" / "SUN_PARK_UNIT_OWNER_LEDGER_PROTOCOL_26AUG2026.md"

AP89_UNITS = {
    "404", "405", "406", "407", "408",
    "453", "454", "455", "456", "457", "458",
    "503", "504", "509", "553", "907", "908", "911",
}
SCHEDULE_COMPARISON_UNITS = {
    "403", "404", "405", "406", "407", "408",
    "454", "455", "456", "457", "458",
    "503", "504", "509", "553", "907", "908", "911",
}
AP89_CLAIMANTS = {
    "PD-SP-O-0015",
    "PD-SP-O-0011",
    "PD-SP-O-0012",
    "PD-SP-O-0009",
    "PD-SP-O-0010",
    "PD-SP-P-0025",
    "PD-SP-P-0020",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def walk(value: Any):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key, item
            yield from walk(item)
    elif isinstance(value, list):
        for item in value:
            yield None, item
            yield from walk(item)


def main() -> int:
    try:
        index = load(INDEX)
        classification = load(CLASSIFICATION)

        require(
            index.get("schema") == "por-derecho.sun-park-unit-owner-ledger.index.v1",
            "unexpected ledger index schema",
        )
        require(
            index.get("control_id") == "PD-SP-UNIT-OWNER-LEDGER-001",
            "unexpected ledger control id",
        )
        require(
            index.get("classification_control_ref")
            == "assets/data/sun-park-owner-perimeter-classification-v1.json",
            "classification control reference drift",
        )

        part_descriptors = index.get("parts", [])
        require(len(part_descriptors) == 5, "ledger part denominator drift")
        parts = {desc["part_id"]: load(DATA / desc["path"]) for desc in part_descriptors}
        require(set(parts) == {"AP89", "PRECAM_SCHEDULE", "LPB12", "EVENTS", "RECONCILIATION"}, "ledger part set drift")
        for part in parts.values():
            require(
                part.get("control_id") == "PD-SP-UNIT-OWNER-LEDGER-001",
                "part control id drift",
            )

        identity_manifest = load(IDENTITY_INDEX)
        canonical_ids: set[str] = set()
        for descriptor in identity_manifest.get("parts", []):
            part = load(DATA / descriptor["path"])
            records = part.get("records", [])
            require(
                len(records) == descriptor.get("count"),
                f"identity-registry part count drift: {descriptor['path']}",
            )
            canonical_ids.update(record["id"] for record in records)
        require(
            len(canonical_ids) == identity_manifest.get("counts", {}).get("total"),
            "identity-registry total mismatch",
        )

        local_identities = index.get("local_identities", [])
        local_ids = {record["local_identity_id"] for record in local_identities}
        require(len(local_ids) == len(local_identities), "duplicate local identity id")

        perimeter_ids = {
            item["perimeter_id"] for item in classification.get("perimeters", [])
        }
        require(
            {
                "PD-SP-PER-MM-AP89-001",
                "PD-SP-PER-OTHER-MINORITY-001",
                "PD-SP-PER-LPB-12-001",
            }
            <= perimeter_ids,
            "required perimeter controls missing",
        )

        sources = index.get("source_registry", [])
        source_ids = {item["source_id"] for item in sources}
        require(len(source_ids) == len(sources), "duplicate source id")

        ap89 = parts["AP89"]
        roster = ap89.get("ap89_claimant_roster", {})
        require(roster.get("claimant_count") == 7, "AP89 claimant denominator must be seven")
        require(
            roster.get("litigated_unit_count") == 18,
            "AP89 litigated-unit denominator must be eighteen",
        )
        claimant_ids = {item["identity_id"] for item in roster.get("claimants", [])}
        require(claimant_ids == AP89_CLAIMANTS, "AP89 claimant roster drift")
        require(
            sum(item.get("count", 0) for item in roster.get("claimants", [])) == 18,
            "AP89 claimant unit counts do not sum to eighteen",
        )

        ap89_map = ap89["unit_map"]
        ap89_records = ap89_map.get("records", [])
        require(ap89_map.get("unit_count") == 18, "AP89 map count field drift")
        require(len(ap89_records) == 18, "AP89 map must contain eighteen rows")
        ap89_units = {item["unit_label"] for item in ap89_records}
        require(ap89_units == AP89_UNITS, "AP89 unit set drift")
        require(len(ap89_units) == 18, "AP89 unit labels are not unique")
        unit_453 = next(item for item in ap89_records if item["unit_label"] == "453")
        require(
            set(unit_453.get("owner_identity_ids", []))
            == {"PD-SP-O-0009", "PD-SP-O-0010"},
            "unit 453 combined Amenem/Tengolf attribution missing",
        )
        ap89_common = ap89_map.get("common_fields", {})
        require(
            ap89_common.get("perimeter_edge", {}).get("perimeter_id")
            == "PD-SP-PER-MM-AP89-001",
            "AP89 common perimeter edge drift",
        )
        require(
            ap89_common.get("representative_edge", {}).get("ownership_implication")
            == "NONE",
            "AP89 representation must not imply ownership",
        )
        for record in ap89_records:
            require(
                set(record.get("owner_identity_ids", [])) <= AP89_CLAIMANTS,
                f"non-claimant owner in AP89 row {record.get('record_id')}",
            )
            require(
                record.get("finca_id") is None,
                "AP89 finca must remain open until f.48-79 notes simples are reconciled",
            )

        schedule = parts["PRECAM_SCHEDULE"]["unit_map"]
        schedule_records = schedule.get("records", [])
        require(schedule.get("unit_count") == 18, "schedule comparison count field drift")
        require(len(schedule_records) == 18, "schedule comparison must contain eighteen rows")
        schedule_units = {item["unit_label"] for item in schedule_records}
        require(
            schedule_units == SCHEDULE_COMPARISON_UNITS,
            "pre-CAM schedule comparison unit set drift",
        )
        require(ap89_units != schedule_units, "parallel unit maps were silently collapsed")
        schedule_common = schedule.get("common_fields", {})
        require(
            "NOT_REGISTRY_PROOF" in schedule_common.get("ownership_status", ""),
            "schedule comparison overstates title proof",
        )
        require(
            "not treated as proof that LPB was the seller"
            in schedule_common.get("interpretation_boundary", ""),
            "DIRECT-column boundary missing",
        )
        require(
            schedule_common.get("perimeter_edge", {}).get("perimeter_id")
            == "PD-SP-PER-OTHER-MINORITY-001",
            "schedule ownership edge must remain non-adverse by default",
        )

        cohort = parts["LPB12"].get("reconstruction", {})
        slots = cohort.get("slots", [])
        require(cohort.get("reported_denominator") == 12, "LPB cohort denominator drift")
        require(len(slots) == 12, "LPB cohort must contain exactly twelve slots")
        require(
            cohort.get("confirmed_completed_transfer_count") == 0,
            "no completed direct LPB transfer is presently confirmed",
        )
        candidates = [slot for slot in slots if slot.get("status", "").startswith("CANDIDATE")]
        unresolved = [slot for slot in slots if slot.get("status", "").startswith("UNRESOLVED")]
        require(len(candidates) == 5, "candidate-slot count drift")
        require(len(unresolved) == 7, "unresolved-slot count drift")
        require(cohort.get("candidate_slot_count") == len(candidates), "candidate count field drift")
        require(cohort.get("unresolved_slot_count") == len(unresolved), "unresolved count field drift")
        for slot in unresolved:
            require(slot.get("unit_label") is None, "unresolved slot invents a unit")
            require(
                slot.get("candidate_owner_local_identity_id") is None,
                "unresolved slot invents an owner",
            )
        require(
            not any("CONFIRMED" in slot.get("status", "") for slot in slots),
            "a reconstruction slot was wrongly promoted to confirmed",
        )

        events = parts["EVENTS"]
        option_events = [
            event
            for event in events.get("instrument_events", [])
            if event.get("instrument_type") == "OPTION_TO_PURCHASE"
        ]
        require(len(option_events) == 1, "exactly one reviewed option event expected")
        option = option_events[0]
        require(set(option.get("unit_labels", [])) == {"907", "908"}, "option-unit drift")
        require(option.get("seller_identity_id") == "PD-SP-O-0002", "option seller drift")
        require(option.get("completion_status") == "NOT_ESTABLISHED", "option completion overstated")
        require(
            option.get("ownership_effect") == "NONE_UNLESS_EXERCISED_AND_CONVEYANCE_COMPLETED",
            "option ownership boundary missing",
        )
        for event in events.get("representation_events", []):
            require(
                event.get("ownership_implication") == "NONE",
                f"representation event implies ownership: {event.get('event_id')}",
            )

        reconciliation = parts["RECONCILIATION"]
        issues = {
            item["issue_id"]: item
            for item in reconciliation.get("reconciliation_issues", [])
        }
        for issue_id in {
            "PD-SP-REC-001",
            "PD-SP-REC-002",
            "PD-SP-REC-003",
            "PD-SP-REC-004",
            "PD-SP-REC-005",
            "PD-SP-REC-006",
            "PD-SP-REC-007",
        }:
            require(issue_id in issues, f"missing reconciliation issue {issue_id}")
        require(issues["PD-SP-REC-002"].get("unit_label") == "503", "unit 503 conflict missing")
        require(issues["PD-SP-REC-003"].get("unit_label") == "908", "unit 908 conflict missing")
        require(
            "403" in issues["PD-SP-REC-001"].get("detail", "")
            and "453" in issues["PD-SP-REC-001"].get("detail", ""),
            "403/453 mismatch not preserved",
        )

        combined = {
            "index": index,
            "ap89": parts["AP89"],
            "schedule": parts["PRECAM_SCHEDULE"],
            "lpb12": parts["LPB12"],
            "events": parts["EVENTS"],
            "reconciliation": parts["RECONCILIATION"],
        }
        all_valid_ids = canonical_ids | local_ids
        for key, value in walk(combined):
            if key and key.endswith("_identity_id") and value is not None:
                require(value in all_valid_ids, f"unknown identity id {value}")
            if key and key.endswith("_identity_ids") and isinstance(value, list):
                for identity_id in value:
                    require(identity_id in all_valid_ids, f"unknown identity id {identity_id}")
            if key == "source_id" and isinstance(value, str):
                require(value in source_ids, f"unknown source id {value}")
            if key in {"basis", "sources"} and isinstance(value, list):
                for source_id in value:
                    require(source_id in source_ids, f"unknown source id {source_id}")

        serialized = json.dumps(combined, ensure_ascii=False)
        privacy_patterns = {
            "email address": re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
            "container path": re.compile(r"/mnt/(?:data|home)/"),
            "Gmail identifier": re.compile(r"(?:mail\.google\.com|gmail-attachment|message_id)"),
            "international phone": re.compile(r"\+\d[\d\s-]{7,}\d"),
            "IBAN/SWIFT": re.compile(r"\b(?:IBAN|SWIFT)\b"),
        }
        for label, pattern in privacy_patterns.items():
            require(pattern.search(serialized) is None, f"private {label} leaked into public ledger")

        require(PROTOCOL.is_file(), "unit-owner ledger protocol missing")
        protocol = PROTOCOL.read_text(encoding="utf-8")
        for marker in [
            "NON-LPB/MATKATOR OWNER ≠ MONTELANZA/MOLINA DISSIDENT",
            "An **option to purchase** is not a completed sale",
            "Candidate leads in the twelve-slot reconstruction: five",
            "Deliberately unresolved slots: seven",
        ]:
            require(marker in protocol, f"protocol marker missing: {marker}")

        rules = " ".join(index.get("governing_rules", []))
        require(
            "NON_LPB_MATKATOR_OWNER does not mean MONTELANZA_MOLINA_DISSIDENT"
            in rules,
            "central non-collapse rule missing",
        )
        require("option to purchase is not a completed sale" in rules, "option boundary missing")
        require("remain parallel sources" in rules, "parallel-source rule missing")

        summary = index.get("summary", {})
        require(summary.get("ap89_claimants") == 7, "summary claimant count drift")
        require(summary.get("ap89_units") == 18, "summary AP89 unit count drift")
        require(summary.get("reported_lpb_transfer_slots") == 12, "summary LPB slot count drift")
        require(summary.get("candidate_slots") == 5, "summary candidate count drift")
        require(summary.get("unresolved_slots") == 7, "summary unresolved count drift")
        require(
            summary.get("confirmed_completed_direct_lpb_transfers") == 0,
            "summary completed-transfer count drift",
        )

        print("SUN PARK UNIT/OWNER LEDGER: PASS")
        print(" - AP89: 7 claimants / 18 source-extracted units")
        print(" - pre-CAM comparison: 18 source-reported rows kept parallel")
        print(" - LPB reported cohort: 12 slots = 5 candidate leads + 7 unresolved")
        print(" - completed direct LPB transfers confirmed in current review: 0")
        print(" - option, ownership, representation and adverse alignment remain separate")
        print(" - 403/453, 503 and 908 reconciliation issues preserved")
        print(" - no private contact, identity-document or local-path data published")
        return 0
    except (AssertionError, KeyError, json.JSONDecodeError) as exc:
        print(f"SUN PARK UNIT/OWNER LEDGER: FAIL\n - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

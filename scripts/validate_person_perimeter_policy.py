#!/usr/bin/env python3
"""Validate the person-perimeter governance contract.

This check validates architecture only. It deliberately does not create or
validate a complete person-to-perimeter map because that map is private and each
natural-person public decision remains authorization-controlled.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / ".github" / "governance" / "person-perimeter-classification-policy-v1.json"
PROTOCOL_PATH = ROOT / ".github" / "governance" / "PERSON_PERIMETER_SEPARATION_AND_PUBLICATION_PROTOCOL.md"
DECISION_PATH = ROOT / ".github" / "governance" / "records" / "PERIMETER_SEPARATION_DECISION_20260825.md"
START_PATH = ROOT / "PERSON_PERIMETER_START_HERE.md"

EXPECTED_LIST_ORDER = [
    "OUR_PERIMETER",
    "ADVERSE_PRIVATE_PERIMETER",
    "PROFESSIONALS",
    "INSTITUTIONS",
    "WITNESSES",
]

EXPECTED_CLASSIFICATIONS = {
    "OUR_CORE",
    "OUR_REPRESENTED_INTEREST",
    "ADVERSE_FORMAL_PARTY",
    "ADVERSE_PRIVATE_FUNCTIONAL_ACTOR",
    "OUR_CURRENT_PROFESSIONAL",
    "OUR_FORMER_PROFESSIONAL",
    "ADVERSE_PARTY_PROFESSIONAL",
    "INSTITUTIONAL_OFFICEHOLDER",
    "WITNESS_EXPERT_CUSTODIAN",
    "TRANSACTION_DEVELOPMENT_PRIVATE",
    "UNRESOLVED_PRIVATE_CANDIDATE",
}

EXPECTED_DISPLAY_MODES = {
    "PRIVATE_ONLY",
    "PUBLIC_AGGREGATE_ANONYMOUS",
    "PUBLIC_ROLE_PSEUDONYM",
    "PUBLIC_PARTIAL_NAME",
    "PUBLIC_FULL_NAME",
    "PUBLIC_WITHDRAWN",
}

EXPECTED_SPECIFIC_IDS = {"PD-SP-P-0065", "PD-SP-P-0066"}
PERSON_ID_RE = re.compile(r"^PD-SP-P-\d{4}$")
EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"Missing policy file: {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"Invalid JSON in {path.relative_to(ROOT)}:{exc.lineno}:{exc.colno}: {exc.msg}"
        ) from exc
    require(isinstance(data, dict), "Policy root must be an object")
    return data


def validate_text_file(path: Path, markers: list[str]) -> str:
    require(path.is_file(), f"Missing governance file: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    require(text.strip(), f"Empty governance file: {path.relative_to(ROOT)}")
    for marker in markers:
        require(marker in text, f"Missing marker {marker!r} in {path.relative_to(ROOT)}")
    require(not EMAIL_RE.search(text), f"Email address found in public governance file: {path.relative_to(ROOT)}")
    return text


def validate_policy(policy: dict[str, Any]) -> None:
    require(
        policy.get("schema") == "por-derecho.person-perimeter-classification-policy.v1",
        "Unexpected person-perimeter policy schema",
    )
    require(policy.get("policy_id") == "PD-PERIMETER-GOV-001", "Unexpected policy ID")
    require(policy.get("status") == "GOVERNANCE_APPROVED_PERSON_DECISIONS_PENDING", "Unexpected policy status")

    lists = policy.get("public_list_order")
    require(isinstance(lists, list), "public_list_order must be an array")
    keys = [item.get("key") for item in lists if isinstance(item, dict)]
    require(keys == EXPECTED_LIST_ORDER, f"Unexpected public list order: {keys}")

    classifications = policy.get("classifications")
    require(isinstance(classifications, dict), "classifications must be an object")
    require(set(classifications) == EXPECTED_CLASSIFICATIONS, "Classification taxonomy is incomplete or expanded without review")

    assigned_to_lists: list[str] = []
    for item in lists:
        require(isinstance(item, dict), "Public-list entry must be an object")
        allowed = item.get("allowed_classifications")
        require(isinstance(allowed, list) and allowed, f"{item.get('key')} has no classifications")
        require(all(value in EXPECTED_CLASSIFICATIONS for value in allowed), f"Unknown classification in {item.get('key')}")
        assigned_to_lists.extend(allowed)
    require(len(assigned_to_lists) == len(set(assigned_to_lists)), "A classification appears in more than one public list")

    private_only = policy.get("private_only_classes")
    require(
        private_only == ["TRANSACTION_DEVELOPMENT_PRIVATE", "UNRESOLVED_PRIVATE_CANDIDATE"],
        "Unexpected private-only classes",
    )
    require(not set(private_only) & set(assigned_to_lists), "A private-only class appears in a public list")

    modes = policy.get("display_modes")
    require(isinstance(modes, list), "display_modes must be an array")
    require(set(modes) == EXPECTED_DISPLAY_MODES and len(modes) == len(EXPECTED_DISPLAY_MODES), "Display modes are incomplete or duplicated")

    defaults = policy.get("default_rules")
    require(isinstance(defaults, dict), "default_rules must be an object")
    require(defaults.get("newly_discovered_person") == "UNRESOLVED_PRIVATE_CANDIDATE", "New-person default must remain private")
    require(defaults.get("transaction_contact") == "TRANSACTION_DEVELOPMENT_PRIVATE", "Transaction default must remain private")
    require(defaults.get("blank_or_ambiguous_authorization") == "PRIVATE_ONLY", "Ambiguous authority must mean PRIVATE_ONLY")

    required_fields = policy.get("person_authorization_required_fields")
    require(isinstance(required_fields, list) and len(required_fields) >= 15, "Person-authorization field set is incomplete")
    require("authorization_reference" in required_fields, "Authorization reference is required")
    require("privacy_and_reidentification_assessment" in required_fields, "Privacy assessment is required")

    specific = policy.get("current_specific_controls")
    require(isinstance(specific, list), "current_specific_controls must be an array")
    ids = {item.get("id") for item in specific if isinstance(item, dict)}
    require(ids == EXPECTED_SPECIFIC_IDS, f"Unexpected specific-control IDs: {sorted(ids)}")
    for item in specific:
        require(PERSON_ID_RE.fullmatch(str(item.get("id", ""))) is not None, "Malformed specific person ID")
        require(item.get("classification") == "TRANSACTION_DEVELOPMENT_PRIVATE", f"{item.get('id')} must remain transaction-private")
        require(item.get("public_principal_perimeter_eligibility") == "NOT_AUTHORIZED", f"{item.get('id')} principal-list eligibility changed")
        require(item.get("display_decision") == "PENDING_PERSON_SPECIFIC_AUTHORIZATION", f"{item.get('id')} display gate changed")

    rendering = policy.get("rendering_contract")
    require(isinstance(rendering, dict), "rendering_contract must be an object")
    require(rendering.get("single_undifferentiated_people_list") == "PROHIBITED", "Mixed people list must remain prohibited")
    require(rendering.get("principal_perimeters_visibly_separate") is True, "Principal perimeters must remain separate")
    require(rendering.get("transaction_and_unresolved_people_public_by_default") is False, "Private queues cannot be public by default")
    require(rendering.get("person_level_publication_requires_authorization") is True, "Person-level publication gate missing")

    implementation = policy.get("implementation_state")
    require(isinstance(implementation, dict), "implementation_state must be an object")
    require(implementation.get("person_by_person_authorization_matrix") == "PENDING", "Person decisions must not be marked complete")
    require(
        implementation.get("public_projection_and_bilingual_rendering") == "PENDING_AUTHORIZED_IMPLEMENTATION",
        "Public rendering must remain pending authorized implementation",
    )


def main() -> int:
    try:
        policy = load_json(POLICY_PATH)
        validate_policy(policy)
        validate_text_file(
            PROTOCOL_PATH,
            [
                "PD-PERIMETER-GOV-001",
                "Our perimeter / Perímetro propio",
                "Adverse private parties and documented opposing interests",
                "A blank, general, incomplete or ambiguous decision means `PRIVATE_ONLY`.",
                "PD-SP-P-0065",
                "PD-SP-P-0066",
            ],
        )
        validate_text_file(
            START_PATH,
            [
                "Mandatory presentation rule",
                "No automatic assignment",
                "TRANSACTION_DEVELOPMENT_PRIVATE",
            ],
        )
        validate_text_file(
            DECISION_PATH,
            [
                "PD-PERIMETER-DEC-20260825-01",
                "person-level implementation remains pending express decisions",
                "New names are private candidates",
            ],
        )
    except AssertionError as exc:
        print(f"PERSON PERIMETER POLICY: FAIL\n - {exc}", file=sys.stderr)
        return 1

    print("PERSON PERIMETER POLICY: PASS")
    print(" - two principal private-party perimeters are separate")
    print(" - professionals, institutions and witnesses are separate")
    print(" - transaction and unresolved identities are private by default")
    print(" - natural-person publication remains person-specific and authorization-controlled")
    print(" - PD-SP-P-0065 and PD-SP-P-0066 remain transaction-private pending decisions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

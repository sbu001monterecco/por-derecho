#!/usr/bin/env python3
"""Synchronise current proceedings audit/schema denominators from controlled outputs.

Historical deployment manifests remain immutable. This helper updates only the
*current* projection contract used by audit_proceedings_interconnectivity_map.py
and proceedings-interconnectivity-schema-v1.json after the interlinkability
builder has regenerated its public exact-file control.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
PUBLIC = ROOT / "assets/data/proceedings-master-public-v1.json"
INTERLINK = ROOT / "assets/data/proceedings-interlinkability-v1.json"
SCHEMA = ROOT / "assets/data/proceedings-interconnectivity-schema-v1.json"
AUDIT = ROOT / "scripts/audit_proceedings_interconnectivity_map.py"

FAMILY_ORDER = (
    "ADMIN_AUTHORITY_TITLE_SOURCE",
    "CIVIL_FILE_DECISION",
    "CRIMINAL_FILE_DECISION",
    "FISCALIA_INSTITUTIONAL_MEMORY",
    "OMBUDSMAN_RECONSIDERATION",
    "PROFESSIONAL_SUPERVISION",
    "REGULATORY_PUBLIC_ROUTE",
    "TAX_CONTENTIOUS_CHAIN",
)


def scalar_replace(text: str, name: str, value: int) -> str:
    pattern = rf"(?m)^{re.escape(name)}\s*=\s*\d+\s*$"
    replacement = f"{name} = {value}"
    text, count = re.subn(pattern, replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"could not uniquely update {name} in {AUDIT}")
    return text


def main() -> int:
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        master_rows = list(csv.DictReader(handle))
    public = json.loads(PUBLIC.read_text(encoding="utf-8"))
    public_rows = public.get("records") or []
    inter = json.loads(INTERLINK.read_text(encoding="utf-8"))
    coverage = inter.get("coverage") or {}

    canonical_exact = [r for r in master_rows if (r.get("Is_Proceeding") or "").upper() == "TRUE"]
    public_exact = [r for r in public_rows if (r.get("Is_Proceeding") or "").upper() == "TRUE"]
    private_exact = {r["Master_ID"] for r in canonical_exact} - {r["Master_ID"] for r in public_exact}
    public_fiscalia = [r for r in public_rows if "FISCAL" in (r.get("Stream") or "").upper()]
    fiscalia_split = Counter((r.get("Is_Proceeding") or "").upper() for r in public_fiscalia)

    expected = {
        "CURRENT_CANONICAL_RECORDS": len(master_rows),
        "CURRENT_PUBLIC_RECORDS": len(public_rows),
        "CURRENT_CANONICAL_EXACT": len(canonical_exact),
        "CURRENT_PUBLIC_EXACT": len(public_exact),
        "CURRENT_PRIVATE_EXACT": len(private_exact),
        "CURRENT_CASE_PRISM_EXACT_COVERED": int(coverage["case_prism_exact_proceeding_covered_count"]),
        "CURRENT_CASE_PRISM_EXACT_UNCOVERED": int(coverage["case_prism_exact_proceeding_uncovered_count"]),
        "CURRENT_DIRECT_PAIRS": int(coverage["direct_relationship_count"]),
        "CURRENT_VERIFIED_DIRECT_PAIRS": int(coverage["direct_relationship_source_verified_pair_count"]),
        "CURRENT_PENDING_DIRECT_PAIRS": int(coverage["direct_relationship_source_reported_pending_pair_count"]),
        "CURRENT_DIRECT_ASSERTIONS": int(coverage["direct_source_assertion_count"]),
        "CURRENT_VERIFIED_DIRECT_ASSERTIONS": int(coverage["direct_source_verified_assertion_count"]),
        "CURRENT_PENDING_DIRECT_ASSERTIONS": int(coverage["direct_source_reported_pending_assertion_count"]),
        "CURRENT_FISCALIA_OFFICE_FILE_RECORDS": len(public_fiscalia),
        "CURRENT_FISCALIA_EXACT_RECORDS": fiscalia_split["TRUE"],
        "CURRENT_FISCALIA_UNRESOLVED_RECORDS": fiscalia_split["UNVERIFIED"],
        "CURRENT_FISCALIA_RESPONSE_EPISODES": int(coverage["fiscalia_response_episode_profile_count"]),
        "CURRENT_FISCALIA_PROFILED_MATRIX_RECORDS": int(coverage["fiscalia_office_file_matrix_source_profiled_record_count"]),
    }

    # Fail closed if the generated control and canonical/public sources disagree.
    checks = {
        "public_record_count": len(public_rows),
        "canonical_exact_proceeding_count": len(canonical_exact),
        "public_exact_proceeding_count": len(public_exact),
        "private_exact_excluded_count": len(private_exact),
        "fiscalia_office_file_matrix_count": len(public_fiscalia),
        "fiscalia_office_file_matrix_exact_count": fiscalia_split["TRUE"],
        "fiscalia_office_file_matrix_unverified_count": fiscalia_split["UNVERIFIED"],
    }
    for key, value in checks.items():
        if coverage.get(key) != value:
            raise SystemExit(f"interlinkability coverage mismatch for {key}: generated={coverage.get(key)} source={value}")
    if expected["CURRENT_CASE_PRISM_EXACT_COVERED"] + expected["CURRENT_CASE_PRISM_EXACT_UNCOVERED"] != len(public_exact):
        raise SystemExit("Case Prism covered/uncovered split does not equal public exact denominator")
    if expected["CURRENT_VERIFIED_DIRECT_PAIRS"] + expected["CURRENT_PENDING_DIRECT_PAIRS"] != expected["CURRENT_DIRECT_PAIRS"]:
        raise SystemExit("direct pair source-grade split is incomplete")
    if expected["CURRENT_VERIFIED_DIRECT_ASSERTIONS"] + expected["CURRENT_PENDING_DIRECT_ASSERTIONS"] != expected["CURRENT_DIRECT_ASSERTIONS"]:
        raise SystemExit("direct assertion source-grade split is incomplete")

    family_counts = coverage.get("finite_test_family_counts") or {}
    if sum(family_counts.values()) != len(public_exact):
        raise SystemExit("finite-test family census does not cover the public exact denominator")
    if set(family_counts) - set(FAMILY_ORDER):
        raise SystemExit("unexpected finite-test family in generated control")

    audit_text = AUDIT.read_text(encoding="utf-8")
    original_audit = audit_text
    for name, value in expected.items():
        audit_text = scalar_replace(audit_text, name, value)

    family_block = "EXPECTED_FINITE_TEST_FAMILY_COUNTS = {\n" + "".join(
        f'    "{family}": {family_counts[family]},\n'
        for family in FAMILY_ORDER
        if family_counts.get(family)
    ) + "}"
    audit_text, count = re.subn(
        r"EXPECTED_FINITE_TEST_FAMILY_COUNTS\s*=\s*\{.*?\n\}",
        family_block,
        audit_text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit("could not update audit finite-test family census")

    exact_n = len(public_exact)
    fiscalia_n = len(public_fiscalia)
    profiled_n = expected["CURRENT_FISCALIA_PROFILED_MATRIX_RECORDS"]
    episode_n = expected["CURRENT_FISCALIA_RESPONSE_EPISODES"]
    covered_n = expected["CURRENT_CASE_PRISM_EXACT_COVERED"]

    # Convert the few remaining current-contract literals into expressions based
    # on the current denominators. Historical lifecycle assertions elsewhere in
    # this audit deliberately remain untouched.
    current_literal_replacements = {
        '"receipt_knowledge_axis_provenance_coverage_status": (\n            "VERIFIED_97_OF_97_WITH_STATUS_BASIS_LIMITATION_AND_SOURCE"\n        )': '"receipt_knowledge_axis_provenance_coverage_status": (\n            f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}_WITH_STATUS_BASIS_LIMITATION_AND_SOURCE"\n        )',
        '"fiscalia_office_file_matrix_coverage_status": (\n            "VERIFIED_24_OF_24_WITH_INDEPENDENT_MATERIAL_DIRECT_CONTEXT_ASSET_"\n            "REFERRAL_EXAMINATION_RESPONSE_ACKNOWLEDGEMENT_CONTRARY_AND_GAP_COLUMNS"\n        )': '"fiscalia_office_file_matrix_coverage_status": (\n            f"VERIFIED_{CURRENT_FISCALIA_OFFICE_FILE_RECORDS}_OF_{CURRENT_FISCALIA_OFFICE_FILE_RECORDS}_WITH_INDEPENDENT_MATERIAL_DIRECT_CONTEXT_ASSET_"\n            "REFERRAL_EXAMINATION_RESPONSE_ACKNOWLEDGEMENT_CONTRARY_AND_GAP_COLUMNS"\n        )',
        '"fiscalia_matrix_profiled_row_coverage_status": "VERIFIED_8_PROFILED_16_EXPLICIT_GAPS"': '"fiscalia_matrix_profiled_row_coverage_status": (\n            f"VERIFIED_{CURRENT_FISCALIA_PROFILED_MATRIX_RECORDS}_PROFILED_"\n            f"{CURRENT_FISCALIA_OFFICE_FILE_RECORDS - CURRENT_FISCALIA_PROFILED_MATRIX_RECORDS}_EXPLICIT_GAPS"\n        )',
        '"fiscalia_source_controlled_episode_profile_coverage_status": "VERIFIED_9_OF_9"': '"fiscalia_source_controlled_episode_profile_coverage_status": (\n            f"VERIFIED_{CURRENT_FISCALIA_RESPONSE_EPISODES}_OF_{CURRENT_FISCALIA_RESPONSE_EPISODES}"\n        )',
        '"exact_id_master_trace_isolation_route_coverage_status": "VERIFIED_97_OF_97"': '"exact_id_master_trace_isolation_route_coverage_status": (\n            f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}"\n        )',
        '"exact_id_to_dossier_source_route_coverage_status": (\n            "MASTER_TRACE_ISOLATION_VERIFIED_97_OF_97_"\n            "DEDICATED_NARRATIVE_DOSSIER_PARTIAL_UNCLAIMED"\n        )': '"exact_id_to_dossier_source_route_coverage_status": (\n            f"MASTER_TRACE_ISOLATION_VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}_"\n            "DEDICATED_NARRATIVE_DOSSIER_PARTIAL_UNCLAIMED"\n        )',
    }
    for old, new in current_literal_replacements.items():
        if old in audit_text:
            audit_text = audit_text.replace(old, new)
        elif new not in audit_text:
            raise SystemExit("current audit contract literal is neither legacy nor governed form")
    AUDIT.write_text(audit_text, encoding="utf-8")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    contract = schema.setdefault("implementation_contract", {})
    contract.update({
        "public_record_trace_denominator": len(public_rows),
        "canonical_exact_proceeding_denominator": len(canonical_exact),
        "public_exact_proceeding_denominator": exact_n,
        "private_exact_proceeding_excluded_denominator": len(private_exact),
        "public_exact_disposition_denominator": exact_n,
        "exact_direct_relationship_pair_denominator": expected["CURRENT_DIRECT_PAIRS"],
        "exact_direct_relationship_source_verified_pair_denominator": expected["CURRENT_VERIFIED_DIRECT_PAIRS"],
        "exact_direct_relationship_source_reported_pending_pair_denominator": expected["CURRENT_PENDING_DIRECT_PAIRS"],
        "exact_direct_source_assertion_denominator": expected["CURRENT_DIRECT_ASSERTIONS"],
        "exact_direct_source_verified_assertion_denominator": expected["CURRENT_VERIFIED_DIRECT_ASSERTIONS"],
        "exact_direct_source_reported_pending_assertion_denominator": expected["CURRENT_PENDING_DIRECT_ASSERTIONS"],
        "material_context_cluster_denominator": int(coverage["context_cluster_count"]),
        "case_prism_exact_proceeding_covered_denominator": covered_n,
        "case_prism_exact_proceeding_uncovered_denominator": exact_n - covered_n,
        "bilingual_specific_next_source_denominator": exact_n,
        "bilingual_specific_next_source_coverage_status": f"VERIFIED_{exact_n}_OF_{exact_n}",
        "exact_proceeding_full_finite_test_denominator": exact_n,
        "exact_proceeding_full_finite_test_coverage_status": f"VERIFIED_{exact_n}_OF_{exact_n}",
        "exact_file_decision_dependency_actionability_coverage_status": f"VERIFIED_{exact_n}_OF_{exact_n}",
        "decision_dependency_exact_coverage_status": f"VERIFIED_{exact_n}_OF_{exact_n}",
        "shared_case_prism_proposition_membership_coverage_status": f"GAP_{covered_n}_OF_{exact_n}",
        "receipt_knowledge_classification_denominator": exact_n,
        "receipt_knowledge_classification_coverage_status": f"VERIFIED_{exact_n}_OF_{exact_n}_POSITIVE_EVIDENCE_SEPARATELY_COUNTED",
        "receipt_knowledge_axis_provenance_denominator": exact_n,
        "receipt_knowledge_axis_provenance_coverage_status": f"VERIFIED_{exact_n}_OF_{exact_n}_WITH_STATUS_BASIS_LIMITATION_AND_SOURCE",
        "actor_specific_knowledge_receipt_trace_status": f"MODELLED_{exact_n}_OF_{exact_n}_WITH_EXPLICIT_NOT_ESTABLISHED_STATES",
        "fiscalia_public_master_row_denominator": fiscalia_n,
        "fiscalia_exact_proceeding_row_denominator": fiscalia_split["TRUE"],
        "fiscalia_unverified_reference_row_denominator": fiscalia_split["UNVERIFIED"],
        "fiscalia_office_file_matrix_coverage_status": f"VERIFIED_{fiscalia_n}_OF_{fiscalia_n}_WITH_INDEPENDENT_MATERIAL_DIRECT_CONTEXT_ASSET_REFERRAL_EXAMINATION_RESPONSE_ACKNOWLEDGEMENT_CONTRARY_AND_GAP_COLUMNS",
        "fiscalia_matrix_profiled_row_denominator": profiled_n,
        "fiscalia_matrix_profiled_row_coverage_status": f"VERIFIED_{profiled_n}_PROFILED_{fiscalia_n-profiled_n}_EXPLICIT_GAPS",
        "fiscalia_source_controlled_episode_profile_denominator": episode_n,
        "fiscalia_source_controlled_episode_profile_coverage_status": f"VERIFIED_{episode_n}_OF_{episode_n}",
        "exact_id_master_trace_isolation_route_coverage_status": f"VERIFIED_{exact_n}_OF_{exact_n}",
        "exact_id_to_dossier_source_route_coverage_status": f"MASTER_TRACE_ISOLATION_VERIFIED_{exact_n}_OF_{exact_n}_DEDICATED_NARRATIVE_DOSSIER_PARTIAL_UNCLAIMED",
        "fragmentation_selector_coverage_status": f"VERIFIED_{exact_n}_OF_{exact_n}",
        "fragmentation_content_coverage_status": f"VERIFIED_{exact_n}_OF_{exact_n}_EXACT_FILE_ISOLATION_AUDIT",
        "finite_test_family_counts": family_counts,
    })
    SCHEMA.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "PROCEEDINGS_INTERCONNECTIVITY_AUDIT_SYNCED",
        expected,
        "families=", family_counts,
        "audit=", "IDEMPOTENT" if audit_text == original_audit else "UPDATED",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

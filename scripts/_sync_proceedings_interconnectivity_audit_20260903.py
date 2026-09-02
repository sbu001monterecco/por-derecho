#!/usr/bin/env python3
"""Synchronise current proceedings audit/schema denominators from controlled outputs.

The current projection is derived from the canonical Master/public controls. Historical
publication manifests are immutable observations and are never rewritten to current
bytes. Instead this helper also emits a current-main -> candidate transition manifest
covering the complete integration diff so later byte drift is explicit and auditable.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
PUBLIC = ROOT / "assets/data/proceedings-master-public-v1.json"
INTERLINK = ROOT / "assets/data/proceedings-interlinkability-v1.json"
SCHEMA = ROOT / "assets/data/proceedings-interconnectivity-schema-v1.json"
AUDIT = ROOT / "scripts/audit_proceedings_interconnectivity_map.py"
REINTEGRATION_MANIFEST = ROOT / "publication-manifests/historic-proceedings-authority-reintegration-20260903.json"
CASE_PRISM_MANIFEST = ROOT / "publication-manifests/case-prism-substantive-gap-closure-20260831.json"
AUTHORITY_MANIFEST = ROOT / "publication-manifests/unitary-public-authority-communications-20260901.json"
DP748_MANIFEST = ROOT / "publication-manifests/dp748-appeal-reopening-source-control-20260901.json"

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
HISTORICAL_SUBSTANTIVE_GAP_FAMILIES = {
    "ADMIN_AUTHORITY_TITLE_SOURCE": 26,
    "CIVIL_FILE_DECISION": 19,
    "CRIMINAL_FILE_DECISION": 11,
    "FISCALIA_INSTITUTIONAL_MEMORY": 21,
    "OMBUDSMAN_RECONSIDERATION": 1,
    "PROFESSIONAL_SUPERVISION": 8,
    "REGULATORY_PUBLIC_ROUTE": 7,
    "TAX_CONTENTIOUS_CHAIN": 4,
}
CASE_PRISM_LIVE_PATHS = {
    "en/proceedings-map/": "en/proceedings-map/index.html",
    "es/mapa-procedimientos/": "es/mapa-procedimientos/index.html",
    "assets/proceedings-interconnectivity-map-20260830.js": "assets/proceedings-interconnectivity-map-20260830.js",
    "assets/proceedings-interconnectivity-map-20260830.css": "assets/proceedings-interconnectivity-map-20260830.css",
    "assets/data/proceedings-case-prism-v1.json": "assets/data/proceedings-case-prism-v1.json",
    "assets/data/proceedings-interlinkability-v1.json": "assets/data/proceedings-interlinkability-v1.json",
    "assets/data/proceedings-master-public-v1.json": "assets/data/proceedings-master-public-v1.json",
    "assets/data/fiscalia-proceedings-interconnectivity-v1.json": "assets/data/fiscalia-proceedings-interconnectivity-v1.json",
    "assets/data/community-acta-authority-interconnectivity-v1.json": "assets/data/community-acta-authority-interconnectivity-v1.json",
    "en/master-proceedings-register/": "en/master-proceedings-register/index.html",
    "es/registro-maestro-procedimientos/": "es/registro-maestro-procedimientos/index.html",
    "en/": "en/index.html",
    "es/": "es/index.html",
    "en/public-authority-unitary-case-reconstruction/": "en/public-authority-unitary-case-reconstruction/index.html",
    "es/reconstruccion-unitaria-autoridades-publicas/": "es/reconstruccion-unitaria-autoridades-publicas/index.html",
}


def scalar_replace(text: str, name: str, value: int) -> str:
    pattern = rf"(?m)^{re.escape(name)}\s*=\s*\d+\s*$"
    replacement = f"{name} = {value}"
    text, count = re.subn(pattern, replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"could not uniquely update {name} in {AUDIT}")
    return text


def replace_once_or_present(text: str, old: str, new: str, label: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    if new in text:
        return text
    raise SystemExit(f"could not reconcile {label}")


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_output(*args: str, allow_fail: bool = False) -> bytes:
    proc = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    if proc.returncode and not allow_fail:
        raise SystemExit(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout if proc.returncode == 0 else b""


def historical_anchor_map() -> dict[str, list[dict[str, str]]]:
    anchors: dict[str, list[dict[str, str]]] = {}

    case = json.loads(CASE_PRISM_MANIFEST.read_text(encoding="utf-8"))
    for route, digest in (case.get("live_verification_evidence", {}).get("critical_sha256", {}) or {}).items():
        path = CASE_PRISM_LIVE_PATHS.get(route)
        if path and digest:
            anchors.setdefault(path, []).append({
                "manifest": str(CASE_PRISM_MANIFEST.relative_to(ROOT)),
                "publication_id": case.get("publication_id", ""),
                "sha256": digest,
                "kind": "historical_live_byte",
            })

    for manifest_path, kind in ((AUTHORITY_MANIFEST, "historical_release"), (DP748_MANIFEST, "historical_release")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for path, digest in (manifest.get("release_critical_sha256") or {}).items():
            anchors.setdefault(path, []).append({
                "manifest": str(manifest_path.relative_to(ROOT)),
                "publication_id": manifest.get("publication_id", ""),
                "sha256": digest,
                "kind": kind,
            })
        transition = manifest.get("historical_transition", {})
        for row in transition.get("changed_resources", []) + transition.get("new_resources", []):
            path = row.get("resource")
            digest = row.get("release_sha256")
            if path and digest and not any(a["sha256"] == digest for a in anchors.get(path, [])):
                anchors.setdefault(path, []).append({
                    "manifest": str(manifest_path.relative_to(ROOT)),
                    "publication_id": manifest.get("publication_id", ""),
                    "sha256": digest,
                    "kind": "historical_transition_release",
                })
    return anchors


def build_reintegration_manifest(expected: dict[str, int], family_counts: dict[str, int]) -> dict:
    base_sha = git_output("merge-base", "origin/main", "HEAD").decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}", base_sha):
        raise SystemExit(f"invalid reintegration base SHA: {base_sha}")

    # Compare the complete candidate working tree (including generated but not yet
    # committed files) to the current-main ancestor. The manifest itself is excluded
    # to avoid a circular self-hash.
    raw = git_output("diff", "--name-status", base_sha, "--").decode("utf-8", errors="replace")
    delta: list[tuple[str, str]] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        path = parts[-1]
        if path == str(REINTEGRATION_MANIFEST.relative_to(ROOT)):
            continue
        delta.append((status, path))

    anchors = historical_anchor_map()
    transitions = []
    for status, rel in sorted(delta, key=lambda x: x[1]):
        current_path = ROOT / rel
        base_bytes = git_output("show", f"{base_sha}:{rel}", allow_fail=True)
        base_digest = hashlib.sha256(base_bytes).hexdigest() if base_bytes else None
        candidate_digest = sha256_path(current_path) if current_path.is_file() else None
        transitions.append({
            "resource": rel,
            "git_status": status,
            "preintegration_main_sha256": base_digest,
            "candidate_sha256": candidate_digest,
            "historical_anchors": anchors.get(rel, []),
            "reason": (
                "Removed obsolete or superseded branch-local resource during source-led current-main reintegration."
                if candidate_digest is None
                else "Current-main reintegration of the controlled historic-proceedings, justice-authority, bilingual page/search and validation architecture."
            ),
        })

    required_candidate_paths = {
        "archive/PROCEEDINGS_MASTER_REGISTER.csv",
        "assets/data/proceedings-master-public-v1.json",
        "assets/data/matter-identity-registry-v1.json",
        "assets/data/justice-authority-register-current-v2.json",
        "assets/data/proceeding-justice-authority-coverage-20260902.json",
        "assets/data/proceedings-interlinkability-v1.json",
        "assets/data/proceedings-interconnectivity-schema-v1.json",
        "scripts/audit_proceedings_interconnectivity_map.py",
        "en/proceedings/gc-civ-003/index.html",
        "es/procedimientos/gc-civ-003/index.html",
    }
    transition_paths = {row["resource"] for row in transitions}
    missing = required_candidate_paths - transition_paths
    if missing:
        raise SystemExit(f"reintegration transition manifest misses critical candidate paths: {sorted(missing)}")

    return {
        "schema": "por-derecho.reintegration-transition.v1",
        "publication_id": "PD-SP-HISTORIC-PROCEEDINGS-AUTHORITY-REINTEGRATION-20260903-01",
        "control_date": "2026-09-03",
        "state": "RELEASE_CANDIDATE_VALIDATION",
        "purpose": "Record the complete current-main-to-candidate file transition without rewriting any historical live/deployment attestation.",
        "integration_branch": "authority-search/historic-proceedings-reintegration-20260903",
        "base_main_sha": base_sha,
        "base_rule": "Current main is authoritative on conflict. Historical manifests remain immutable observations; candidate drift is registered here and must match current candidate bytes.",
        "historical_predecessors": [
            {
                "manifest": "publication-manifests/case-prism-substantive-gap-closure-20260831.json",
                "publication_id": "PD-SP-CASE-PRISM-EXACT-ACTIONABILITY-20260831-01",
                "merge_sha": "d8940e5a7e2d9073a8117b2342e20205bfab7653",
            },
            {
                "manifest": "publication-manifests/unitary-public-authority-communications-20260901.json",
                "publication_id": "PD-SP-UNITARY-PUBLIC-AUTHORITY-COMMS-20260901-01",
                "merge_sha": "a2873cd865567da1b6644f32821bb15ece53a160",
            },
            {
                "manifest": "publication-manifests/dp748-appeal-reopening-source-control-20260901.json",
                "publication_id": "PD-SP-DP748-APPEAL-REOPENING-20260901-01",
                "merge_sha": "cc3d0985ae014282e8a1f7805e0193d15e673177",
            },
        ],
        "current_denominator": expected | {"FINITE_TEST_TOTAL": sum(family_counts.values())},
        "finite_test_family_counts": family_counts,
        "candidate_delta_file_count": len(transitions),
        "transitions": transitions,
        "obsolete_duplicate_routes_absent": [
            "en/proceedings/lz-civ-050/index.html",
            "es/procedimientos/lz-civ-050/index.html",
        ],
        "source_boundaries": [
            "HISTORICAL_MANIFESTS_ARE_IMMUTABLE_OBSERVATIONS_NOT_CURRENT_BYTE_LOCKS",
            "CURRENT_MAIN_WINS_ON_CONFLICT",
            "UNKNOWN_JUDGE_LAJ_OR_FISCAL_REMAINS_SOURCE_GAP",
            "FORMAL_PROCEDURAL_RELATIONSHIPS_REMAIN_DISTINCT_FROM_CONTEXTUAL_NAVIGATION",
            "STRUCTURAL_COVERAGE_IS_NOT_MERITS_EVIDENCE",
        ],
        "production": {
            "merged_to_main": False,
            "merge_sha": None,
            "pages_run_id": None,
            "live_browser_verified": False,
        },
    }


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
        for family in FAMILY_ORDER if family_counts.get(family)
    ) + "}"
    audit_text, count = re.subn(
        r"EXPECTED_FINITE_TEST_FAMILY_COUNTS\s*=\s*\{.*?\n\}", family_block,
        audit_text, count=1, flags=re.S,
    )
    if count != 1:
        raise SystemExit("could not update audit finite-test family census")

    # Add immutable 31-August denominator constants once. Current generated
    # counts must never be substituted into that historical attestation.
    historical_marker = "HISTORICAL_SUBSTANTIVE_GAP_PENDING_DIRECT_ASSERTIONS = 2\n"
    historical_block = historical_marker + """HISTORICAL_SUBSTANTIVE_GAP_CANONICAL_RECORDS = 122
HISTORICAL_SUBSTANTIVE_GAP_PUBLIC_RECORDS = 121
HISTORICAL_SUBSTANTIVE_GAP_CANONICAL_EXACT = 98
HISTORICAL_SUBSTANTIVE_GAP_PUBLIC_EXACT = 97
HISTORICAL_SUBSTANTIVE_GAP_PRIVATE_EXACT = 1
HISTORICAL_SUBSTANTIVE_GAP_CASE_PRISM_BASELINE_COVERED = 26
HISTORICAL_SUBSTANTIVE_GAP_CASE_PRISM_BASELINE_UNCOVERED = 71
HISTORICAL_SUBSTANTIVE_GAP_CASE_PRISM_LIVE_COVERED = 43
HISTORICAL_SUBSTANTIVE_GAP_CASE_PRISM_LIVE_UNCOVERED = 54
HISTORICAL_SUBSTANTIVE_GAP_CONTEXT_CLUSTERS = 26
HISTORICAL_SUBSTANTIVE_GAP_PROPOSITIONS = 19
HISTORICAL_SUBSTANTIVE_GAP_LANES = 12
HISTORICAL_SUBSTANTIVE_GAP_COORDINATES = 228
HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_ROWS = 24
HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_EXACT = 21
HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_UNRESOLVED = 3
HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_EPISODES = 9
HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_PROFILED = 8
HISTORICAL_SUBSTANTIVE_GAP_FINITE_TEST_FAMILY_COUNTS = {
    "ADMIN_AUTHORITY_TITLE_SOURCE": 26,
    "CIVIL_FILE_DECISION": 19,
    "CRIMINAL_FILE_DECISION": 11,
    "FISCALIA_INSTITUTIONAL_MEMORY": 21,
    "OMBUDSMAN_RECONSIDERATION": 1,
    "PROFESSIONAL_SUPERVISION": 8,
    "REGULATORY_PUBLIC_ROUTE": 7,
    "TAX_CONTENTIOUS_CHAIN": 4,
}
"""
    if "HISTORICAL_SUBSTANTIVE_GAP_CANONICAL_RECORDS" not in audit_text:
        if historical_marker not in audit_text:
            raise SystemExit("could not locate historical substantive-gap constant anchor")
        audit_text = audit_text.replace(historical_marker, historical_block, 1)

    exact_n = len(public_exact)
    fiscalia_n = len(public_fiscalia)
    profiled_n = expected["CURRENT_FISCALIA_PROFILED_MATRIX_RECORDS"]
    episode_n = expected["CURRENT_FISCALIA_RESPONSE_EPISODES"]
    covered_n = expected["CURRENT_CASE_PRISM_EXACT_COVERED"]

    # Current runtime checks use current generated denominators.
    audit_text = replace_once_or_present(
        audit_text,
        'interlink_coverage.get("fiscalia_office_file_matrix_coverage")\n        == "VERIFIED_24_OF_24"',
        'interlink_coverage.get("fiscalia_office_file_matrix_coverage")\n        == f"VERIFIED_{CURRENT_FISCALIA_OFFICE_FILE_RECORDS}_OF_{CURRENT_FISCALIA_OFFICE_FILE_RECORDS}"',
        "current Fiscalía matrix coverage",
    )
    audit_text = replace_once_or_present(
        audit_text,
        'interlink_coverage.get(\n            "fiscalia_office_file_matrix_substantive_column_coverage"\n        )\n        == "VERIFIED_24_OF_24"',
        'interlink_coverage.get(\n            "fiscalia_office_file_matrix_substantive_column_coverage"\n        )\n        == f"VERIFIED_{CURRENT_FISCALIA_OFFICE_FILE_RECORDS}_OF_{CURRENT_FISCALIA_OFFICE_FILE_RECORDS}"',
        "current Fiscalía substantive-column coverage",
    )

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
            audit_text = audit_text.replace(old, new, 1)
        elif new not in audit_text:
            raise SystemExit("current audit contract literal is neither legacy nor governed form")

    historical_baseline_block = """expected_current_baseline = {
        "canonical_rows": HISTORICAL_SUBSTANTIVE_GAP_CANONICAL_RECORDS,
        "public_rows": HISTORICAL_SUBSTANTIVE_GAP_PUBLIC_RECORDS,
        "canonical_exact_proceedings": HISTORICAL_SUBSTANTIVE_GAP_CANONICAL_EXACT,
        "public_exact_proceedings": HISTORICAL_SUBSTANTIVE_GAP_PUBLIC_EXACT,
        "private_exact_excluded": HISTORICAL_SUBSTANTIVE_GAP_PRIVATE_EXACT,
        "direct_relationship_pairs": HISTORICAL_SUBSTANTIVE_GAP_DIRECT_PAIRS,
        "direct_relationship_pairs_source_verified": HISTORICAL_SUBSTANTIVE_GAP_VERIFIED_DIRECT_PAIRS,
        "direct_relationship_pairs_source_reported_primary_pending": HISTORICAL_SUBSTANTIVE_GAP_PENDING_DIRECT_PAIRS,
        "direct_source_assertions": HISTORICAL_SUBSTANTIVE_GAP_DIRECT_ASSERTIONS,
        "direct_source_assertions_verified": HISTORICAL_SUBSTANTIVE_GAP_VERIFIED_DIRECT_ASSERTIONS,
        "direct_source_assertions_source_reported_primary_pending": HISTORICAL_SUBSTANTIVE_GAP_PENDING_DIRECT_ASSERTIONS,
        "material_context_clusters": HISTORICAL_SUBSTANTIVE_GAP_CONTEXT_CLUSTERS,
        "shared_case_prism_propositions": HISTORICAL_SUBSTANTIVE_GAP_PROPOSITIONS,
        "parallel_lanes": HISTORICAL_SUBSTANTIVE_GAP_LANES,
        "explicit_matrix_coordinates": HISTORICAL_SUBSTANTIVE_GAP_COORDINATES,
        "case_prism_exact_proceedings_with_shared_proposition_coordinate": HISTORICAL_SUBSTANTIVE_GAP_CASE_PRISM_BASELINE_COVERED,
        "case_prism_exact_proceedings_without_shared_proposition_coordinate": HISTORICAL_SUBSTANTIVE_GAP_CASE_PRISM_BASELINE_UNCOVERED,
        "public_master_fiscalia_rows": HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_ROWS,
        "public_master_fiscalia_exact_rows": HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_EXACT,
        "public_master_fiscalia_unverified_reference_rows": HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_UNRESOLVED,
        "source_controlled_fiscalia_response_episodes": HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_EPISODES,
        "fiscalia_matrix_rows_with_episode_profiles": HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_PROFILED,
        "judicial_file_episode_profiles_outside_fiscalia_matrix": 1,
    }"""
    audit_text, baseline_count = re.subn(
        r"expected_current_baseline = \{.*?\n    \}", historical_baseline_block,
        audit_text, count=1, flags=re.S,
    )
    if baseline_count != 1:
        raise SystemExit("could not isolate historical substantive-gap baseline block")
    audit_text = audit_text.replace(
        'current_targets.get("finite_test_family_counts")\n        == EXPECTED_FINITE_TEST_FAMILY_COUNTS',
        'current_targets.get("finite_test_family_counts")\n        == HISTORICAL_SUBSTANTIVE_GAP_FINITE_TEST_FAMILY_COUNTS',
        1,
    )

    historical_live_block = """live_release_denominator = current_lifecycle.get("live_release_denominator", {})
    require(
        live_release_denominator.get("canonical_rows") == HISTORICAL_SUBSTANTIVE_GAP_CANONICAL_RECORDS
        and live_release_denominator.get("public_rows") == HISTORICAL_SUBSTANTIVE_GAP_PUBLIC_RECORDS
        and live_release_denominator.get("canonical_exact_proceedings") == HISTORICAL_SUBSTANTIVE_GAP_CANONICAL_EXACT
        and live_release_denominator.get("public_exact_proceedings") == HISTORICAL_SUBSTANTIVE_GAP_PUBLIC_EXACT
        and live_release_denominator.get("private_exact_excluded") == HISTORICAL_SUBSTANTIVE_GAP_PRIVATE_EXACT
        and live_release_denominator.get("public_exact_dispositions") == "VERIFIED_97_OF_97"
        and live_release_denominator.get("direct_relationship_pairs") == HISTORICAL_SUBSTANTIVE_GAP_DIRECT_PAIRS
        and live_release_denominator.get("direct_relationship_pairs_source_verified") == HISTORICAL_SUBSTANTIVE_GAP_VERIFIED_DIRECT_PAIRS
        and live_release_denominator.get("direct_relationship_pairs_source_reported_primary_pending") == HISTORICAL_SUBSTANTIVE_GAP_PENDING_DIRECT_PAIRS
        and live_release_denominator.get("direct_source_assertions") == HISTORICAL_SUBSTANTIVE_GAP_DIRECT_ASSERTIONS
        and live_release_denominator.get("direct_source_assertions_verified") == HISTORICAL_SUBSTANTIVE_GAP_VERIFIED_DIRECT_ASSERTIONS
        and live_release_denominator.get("direct_source_assertions_source_reported_primary_pending") == HISTORICAL_SUBSTANTIVE_GAP_PENDING_DIRECT_ASSERTIONS
        and live_release_denominator.get("material_context_clusters") == HISTORICAL_SUBSTANTIVE_GAP_CONTEXT_CLUSTERS
        and live_release_denominator.get("shared_case_prism_propositions") == HISTORICAL_SUBSTANTIVE_GAP_PROPOSITIONS
        and live_release_denominator.get("parallel_lanes") == HISTORICAL_SUBSTANTIVE_GAP_LANES
        and live_release_denominator.get("explicit_matrix_coordinates") == HISTORICAL_SUBSTANTIVE_GAP_COORDINATES
        and live_release_denominator.get("exact_file_decision_dependency_and_fragmentation_audit") == "VERIFIED_97_OF_97"
        and live_release_denominator.get("case_prism_exact_proceedings_with_shared_proposition_coordinate") == HISTORICAL_SUBSTANTIVE_GAP_CASE_PRISM_LIVE_COVERED
        and live_release_denominator.get("case_prism_exact_proceedings_without_shared_proposition_coordinate") == HISTORICAL_SUBSTANTIVE_GAP_CASE_PRISM_LIVE_UNCOVERED
        and live_release_denominator.get("public_master_fiscalia_rows") == HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_ROWS
        and live_release_denominator.get("public_master_fiscalia_exact_rows") == HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_EXACT
        and live_release_denominator.get("public_master_fiscalia_unverified_reference_rows") == HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_UNRESOLVED
        and live_release_denominator.get("source_controlled_fiscalia_response_episodes") == HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_EPISODES
        and live_release_denominator.get("fiscalia_matrix_rows_with_episode_profiles") == HISTORICAL_SUBSTANTIVE_GAP_FISCALIA_PROFILED
        and live_release_denominator.get("audience_lenses") == 9
        and live_release_denominator.get("institutional_positive_source_profiles") == 9
        and live_release_denominator.get("actor_specific_positive_profiles") == 0,
        "current substantive-gap live-release denominator is incomplete or stale",
    )"""
    audit_text, live_count = re.subn(
        r"live_release_denominator = current_lifecycle\.get\(\"live_release_denominator\", \{\}\)\n    require\(.*?\"current substantive-gap live-release denominator is incomplete or stale\",\n    \)",
        historical_live_block, audit_text, count=1, flags=re.S,
    )
    if live_count != 1:
        raise SystemExit("could not isolate historical substantive-gap live denominator block")

    # Historical DP 748 manifests pin their own release bytes. They must not be
    # compared directly to today's files after lawful successors.
    audit_text = audit_text.replace(
        'dp748_changed[path].get("release_sha256")\n            == hashlib.sha256((ROOT / path).read_bytes()).hexdigest()',
        'dp748_changed[path].get("release_sha256")\n            == dp748_successor.get("release_critical_sha256", {}).get(path)',
        1,
    )
    audit_text = audit_text.replace(
        'dp748_new[path].get("release_sha256")\n            == hashlib.sha256((ROOT / path).read_bytes()).hexdigest()',
        'dp748_new[path].get("release_sha256")\n            == dp748_successor.get("release_critical_sha256", {}).get(path)',
        1,
    )
    old_dp_release = '''dp748_release_hashes = dp748_successor.get("release_critical_sha256", {})
    expected_dp748_release_paths = set(expected_dp748_prior_hashes) | expected_dp748_new_paths
    require(
        set(dp748_release_hashes) == expected_dp748_release_paths
        and all(
            dp748_release_hashes.get(path)
            == hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            for path in expected_dp748_release_paths
        ),
        "DP 748 successor release hashes are incomplete or stale",
    )'''
    new_dp_release = '''dp748_release_hashes = dp748_successor.get("release_critical_sha256", {})
    expected_dp748_release_paths = set(expected_dp748_prior_hashes) | expected_dp748_new_paths
    expected_dp748_historical_release_hashes = {
        **{path: dp748_changed[path].get("release_sha256") for path in expected_dp748_prior_hashes},
        **{path: dp748_new[path].get("release_sha256") for path in expected_dp748_new_paths},
    }
    require(
        set(dp748_release_hashes) == expected_dp748_release_paths
        and all(
            dp748_release_hashes.get(path) == expected_dp748_historical_release_hashes.get(path)
            for path in expected_dp748_release_paths
        ),
        "DP 748 successor release hashes are incomplete or stale",
    )'''
    audit_text = replace_once_or_present(audit_text, old_dp_release, new_dp_release, "DP748 immutable release hashes")

    old_authority_hash_check = '''require(
        set(successor_release_hashes) == expected_successor_release_paths
        and all(
            successor_release_hashes.get(path)
            == (
                dp748_changed[path].get("predecessor_main_sha256")
                if path in dp748_changed
                else hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            )
            for path in expected_successor_release_paths - {community_resource}
        ),
        "authority-communications successor release hashes are incomplete or stale",
    )'''
    new_authority_hash_check = '''require(
        set(successor_release_hashes) == expected_successor_release_paths
        and all(re.fullmatch(r"[0-9a-f]{64}", str(successor_release_hashes.get(path, ""))) for path in expected_successor_release_paths)
        and all(
            successor_release_hashes.get(path) == dp748_changed[path].get("predecessor_main_sha256")
            for path in (expected_successor_release_paths & set(dp748_changed)) - {community_resource}
        ),
        "authority-communications successor release hashes are incomplete or stale",
    )'''
    audit_text = replace_once_or_present(audit_text, old_authority_hash_check, new_authority_hash_check, "authority immutable release hashes")
    old_community_chain = '''require(
        successor_release_hashes.get(community_resource)
        == pwc_transition.get("predecessor_sha256")
        and pwc_transition.get("candidate_sha256")
        == community_pwc_candidate_sha256
        and dp748_changed.get(community_resource, {}).get("release_sha256")
        == community_current_sha256,
        "authority-communications successor release hash lacks a valid later transition",
    )'''
    new_community_chain = '''require(
        successor_release_hashes.get(community_resource)
        == pwc_transition.get("predecessor_sha256")
        and pwc_transition.get("candidate_sha256")
        == community_pwc_candidate_sha256
        and dp748_changed.get(community_resource, {}).get("release_sha256")
        == dp748_release_hashes.get(community_resource),
        "authority-communications successor release hash lacks a valid later transition",
    )'''
    audit_text = replace_once_or_present(audit_text, old_community_chain, new_community_chain, "authority->PwC->DP748 historical chain")

    # Historical live hashes are verified as immutable recorded hashes plus known
    # successor predecessor-links. They are not compared to today's bytes.
    old_live_hash_require = '''require(
        live_evidence.get("observed_at") == "2026-08-31T23:51:00Z"
        and live_evidence.get("method")
        == "CACHE_BUSTED_HTTP_READBACK_AND_EXACT_LOCAL_BYTE_COMPARISON"
        and live_evidence.get("intended_critical_resource_count")
        == len(expected_live_hash_paths)
        and live_evidence.get("intended_http_200_count")
        == len(expected_live_hash_paths)
        and live_evidence.get("intended_exact_byte_match_count")
        == len(expected_live_hash_paths)
        and set(live_hashes) == set(expected_live_hash_paths)
        and all(
            live_hashes.get(route)
            == (
                successor_changed[path].get("predecessor_live_sha256")
                if path in successor_changed
                else (
                    dp748_changed[path].get("predecessor_main_sha256")
                    if path in dp748_changed
                    else hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                )
            )
            for route, path in expected_live_hash_paths.items()
        ),
        "historical substantive-gap intended live-byte evidence is incomplete or has unregistered drift",
    )'''
    new_live_hash_require = '''require(
        live_evidence.get("observed_at") == "2026-08-31T23:51:00Z"
        and live_evidence.get("method")
        == "CACHE_BUSTED_HTTP_READBACK_AND_EXACT_LOCAL_BYTE_COMPARISON"
        and live_evidence.get("intended_critical_resource_count") == len(expected_live_hash_paths)
        and live_evidence.get("intended_http_200_count") == len(expected_live_hash_paths)
        and live_evidence.get("intended_exact_byte_match_count") == len(expected_live_hash_paths)
        and set(live_hashes) == set(expected_live_hash_paths)
        and all(re.fullmatch(r"[0-9a-f]{64}", str(live_hashes.get(route, ""))) for route in expected_live_hash_paths)
        and all(
            live_hashes.get(route) == successor_changed[path].get("predecessor_live_sha256")
            for route, path in expected_live_hash_paths.items() if path in successor_changed
        )
        and all(
            live_hashes.get(route) == dp748_changed[path].get("predecessor_main_sha256")
            for route, path in expected_live_hash_paths.items() if path in dp748_changed and path not in successor_changed
        ),
        "historical substantive-gap intended live-byte evidence is incomplete or has unregistered drift",
    )'''
    audit_text = replace_once_or_present(audit_text, old_live_hash_require, new_live_hash_require, "historical live byte attestation")

    # Load and fail-closed validate the current-main reintegration transition.
    manifest_path_token = '"publication-manifests/historic-proceedings-authority-reintegration-20260903.json"'
    if manifest_path_token not in audit_text:
        anchor = '    "archive/UNITARY_PUBLIC_AUTHORITY_COMMUNICATIONS_LIVE_CLOSEOUT_01SEP2026.md",\n]'
        replacement = '    "archive/UNITARY_PUBLIC_AUTHORITY_COMMUNICATIONS_LIVE_CLOSEOUT_01SEP2026.md",\n    "publication-manifests/historic-proceedings-authority-reintegration-20260903.json",\n]'
        audit_text = replace_once_or_present(audit_text, anchor, replacement, "reintegration manifest required source")
    load_anchor = '''    dp748_successor = json.loads(
        read("publication-manifests/dp748-appeal-reopening-source-control-20260901.json")
    )'''
    load_replacement = load_anchor + '''
    reintegration_transition = json.loads(
        read("publication-manifests/historic-proceedings-authority-reintegration-20260903.json")
    )'''
    if "reintegration_transition = json.loads" not in audit_text:
        audit_text = replace_once_or_present(audit_text, load_anchor, load_replacement, "reintegration manifest load")

    reintegration_gate = '''
    # Current-main reintegration is the present byte-transition authority. It
    # preserves historical attestations while requiring every listed candidate
    # file to match its current candidate hash and forbidding premature live claims.
    reintegration_rows = reintegration_transition.get("transitions", [])
    reintegration_by_path = {
        row.get("resource"): row for row in reintegration_rows
        if isinstance(row, dict) and row.get("resource")
    }
    reintegration_required_paths = {
        "archive/PROCEEDINGS_MASTER_REGISTER.csv",
        "assets/data/proceedings-master-public-v1.json",
        "assets/data/matter-identity-registry-v1.json",
        "assets/data/justice-authority-register-current-v2.json",
        "assets/data/proceeding-justice-authority-coverage-20260902.json",
        "assets/data/proceedings-interlinkability-v1.json",
        "assets/data/proceedings-interconnectivity-schema-v1.json",
        "scripts/audit_proceedings_interconnectivity_map.py",
        "en/proceedings/gc-civ-003/index.html",
        "es/procedimientos/gc-civ-003/index.html",
    }
    require(
        reintegration_transition.get("schema") == "por-derecho.reintegration-transition.v1"
        and reintegration_transition.get("publication_id") == "PD-SP-HISTORIC-PROCEEDINGS-AUTHORITY-REINTEGRATION-20260903-01"
        and reintegration_transition.get("control_date") == "2026-09-03"
        and reintegration_transition.get("state") == "RELEASE_CANDIDATE_VALIDATION"
        and re.fullmatch(r"[0-9a-f]{40}", reintegration_transition.get("base_main_sha", ""))
        and len(reintegration_rows) == len(reintegration_by_path)
        and reintegration_transition.get("candidate_delta_file_count") == len(reintegration_rows)
        and reintegration_required_paths <= set(reintegration_by_path)
        and all(
            (row.get("candidate_sha256") is None and not (ROOT / path).exists())
            or row.get("candidate_sha256") == hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            for path, row in reintegration_by_path.items()
        )
        and all(bool(row.get("reason")) for row in reintegration_rows)
        and all(
            anchor.get("sha256") and re.fullmatch(r"[0-9a-f]{64}", anchor.get("sha256", ""))
            for row in reintegration_rows for anchor in row.get("historical_anchors", [])
        )
        and not (ROOT / "en/proceedings/lz-civ-050/index.html").exists()
        and not (ROOT / "es/procedimientos/lz-civ-050/index.html").exists()
        and reintegration_transition.get("production") == {
            "merged_to_main": False,
            "merge_sha": None,
            "pages_run_id": None,
            "live_browser_verified": False,
        },
        "current-main historic-proceedings reintegration transition is incomplete or overclaims publication",
    )
'''
    if "current-main historic-proceedings reintegration transition is incomplete or overclaims publication" not in audit_text:
        insert_anchor = "    renderer_tokens = {"
        if insert_anchor not in audit_text:
            raise SystemExit("could not locate renderer gate insertion anchor")
        audit_text = audit_text.replace(insert_anchor, reintegration_gate + "\n" + insert_anchor, 1)

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
    views = schema.setdefault("implemented_public_views", {})
    views["TRACE_ONE_PROCEEDING"] = (
        f"renderer tab traces all {len(public_rows)} public records; each of the {exact_n} public exact proceedings exposes its controlled disposition, finite test and receipt/knowledge classification; direct edges and material bridges come only from the controlled interlinkability registry"
    )
    views["CONVERGENCE_CLUSTER"] = (
        f"{int(coverage['context_cluster_count'])} source-controlled material clusters: recorded Connection groups, source-controlled corridors and Case Prism propositions; Stream and Geography remain taxonomy only"
    )
    views["FRAGMENTATION_AUDIT"] = (
        f"all {exact_n} public exact proceedings are selectable and have a file-specific finite question, decision dependency, contrary explanation and confirm/refute consequence; external context requires selected-ID or registry-connected-ID membership; shared-proposition membership remains {covered_n} of {exact_n} with {exact_n-covered_n} explicit no-coordinate gaps"
    )
    views["ISOLATION_TEST"] = (
        f"{exact_n}-of-{exact_n} public exact-proceeding selector, finite test, receipt/knowledge classification, controlled reconnection disposition, visible/disappearing comparison and full-corpus restore"
    )
    SCHEMA.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Rebuild the manifest after audit/schema edits so candidate hashes are exact.
    reintegration = build_reintegration_manifest(expected, family_counts)
    REINTEGRATION_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    REINTEGRATION_MANIFEST.write_text(json.dumps(reintegration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "PROCEEDINGS_INTERCONNECTIVITY_AUDIT_SYNCED",
        expected,
        "families=", family_counts,
        "candidate_delta=", reintegration["candidate_delta_file_count"],
        "base_main=", reintegration["base_main_sha"],
        "audit=", "IDEMPOTENT" if audit_text == original_audit else "UPDATED",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

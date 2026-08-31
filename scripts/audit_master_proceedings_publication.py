#!/usr/bin/env python3
"""Fail closed on Master Proceedings Register publication and continuity drift."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

from build_public_proceedings_projection import (
    EXCLUDED_TREATMENTS,
    FIELD_ALLOWLIST,
    PRIVATE_SOURCE_FIELDS,
    PUBLIC_TREATMENTS,
)

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"
PROJECTION = ROOT / "assets/data/proceedings-master-public-v1.json"
BUILDER = ROOT / "scripts/build_public_proceedings_projection.py"
PROTOCOL = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER_PROTOCOL.md"
GOVERNANCE = ROOT / "archive/MASTER_PROCEEDINGS_PUBLICATION_GOVERNANCE_30AUG2026.md"
STORYING = ROOT / "archive/PROCEEDINGS_FULL_IDENTITY_STORYING_GOVERNANCE_30AUG2026.md"
INTERCONNECTIVITY = ROOT / ".github/governance/UNITARY_PROCEEDINGS_INTERCONNECTIVITY_MAP_PROTOCOL_30AUG2026.md"
EN = ROOT / "en/master-proceedings-register/index.html"
ES = ROOT / "es/registro-maestro-procedimientos/index.html"
JS = ROOT / "assets/master-proceedings-publication-20260830.js"
CSS = ROOT / "assets/master-proceedings-publication-20260830.css"
SITE = ROOT / "assets/site.js"
MANIFEST = ROOT / "publication-manifests/master-proceedings-publication-20260830.json"
MARKER = "MASTER_PROCEEDINGS_PUBLICATION_GATE"
STORYING_MARKER = "PROCEEDINGS_FULL_IDENTITY_STORYING_GATE"


def main() -> int:
    errors: list[str] = []
    required = [CSV, PROJECTION, BUILDER, PROTOCOL, GOVERNANCE, EN, ES, JS, CSS, SITE, MANIFEST]
    for path in required:
        if not path.exists():
            errors.append(f"missing required publication control: {path.relative_to(ROOT)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    protocol = PROTOCOL.read_text(encoding="utf-8")
    governance = GOVERNANCE.read_text(encoding="utf-8")
    storying = STORYING.read_text(encoding="utf-8")
    interconnectivity = INTERCONNECTIVITY.read_text(encoding="utf-8")
    en = EN.read_text(encoding="utf-8")
    es = ES.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    site = SITE.read_text(encoding="utf-8")
    projection_text = PROJECTION.read_text(encoding="utf-8")
    projection = json.loads(projection_text)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if manifest.get("public_projection", {}).get("source") != "canonical_csv_runtime_projection":
        errors.append("historical deployed Master Register projection source changed")
    migration = manifest.get("projection_migration", {})
    if not (
        migration.get("target") == "assets/data/proceedings-master-public-v1.json"
        and migration.get("derivation") == "DETERMINISTIC_ALLOWLIST_FROM_CANONICAL_REGISTER"
        and migration.get("state") == "LIVE_VERIFIED"
        and migration.get("pull_request") == 1235
        and migration.get("reviewed_head_sha") == "40ccc3c699bcc1147a9ac65a52e93fec240633ce"
        and migration.get("reviewed_tree_sha") == "c64ae7547fed024ad0e82397f09fc5f61e2f5da7"
        and migration.get("merge_sha") == "e13652bb8b3f51dd050c431a58e2bd70b83f5676"
        and migration.get("merge_tree_sha") == "c64ae7547fed024ad0e82397f09fc5f61e2f5da7"
        and migration.get("pages_run_id") == 33342771113
        and migration.get("pages_run_number") == 1314
        and migration.get("live_readback") == "PASS_16_OF_16_INTENDED_CRITICAL_RESOURCES"
        and migration.get("controlling_manifest") == "publication-manifests/all-proceedings-interlinkability-20260830.json"
        and set(migration.get("expected_source_files", [])) == {
            "assets/data/proceedings-master-public-v1.json",
            "scripts/build_public_proceedings_projection.py",
        }
    ):
        errors.append("allowlisted Master Register projection migration lacks exact LIVE_VERIFIED #1235 evidence")

    for path, text in ((PROTOCOL, protocol), (GOVERNANCE, governance), (SITE, site)):
        if MARKER not in text:
            errors.append(f"{path.relative_to(ROOT)} missing {MARKER}")

    for path, text in ((PROTOCOL, protocol), (STORYING, storying), (INTERCONNECTIVITY, interconnectivity)):
        if STORYING_MARKER not in text:
            errors.append(f"{path.relative_to(ROOT)} missing {STORYING_MARKER}")

    for phrase in (
        "decision number",
        "NIG",
        "exact organ/section",
        "what was not decided",
        "explicit evidenced gap",
        "Rollo 1010/2018",
        "Auto 804/2018",
        "3500443220180003508",
        "Audiencia Provincial de Las Palmas — Sección Segunda",
    ):
        if phrase not in storying:
            errors.append(f"full-identity/storying governance missing control phrase: {phrase}")

    for path, text, route, alternate in (
        (EN, en, "/en/master-proceedings-register/", "/es/registro-maestro-procedimientos/"),
        (ES, es, "/es/registro-maestro-procedimientos/", "/en/master-proceedings-register/"),
    ):
        if "data-master-proceedings-page" not in text:
            errors.append(f"{path.relative_to(ROOT)} missing public-register mount")
        if route not in text or alternate not in text:
            errors.append(f"{path.relative_to(ROOT)} missing canonical/reciprocal route linkage")
        if "TRUE" not in text or "FALSE" not in text or "UNVERIFIED" not in text:
            errors.append(f"{path.relative_to(ROOT)} must explain TRUE/FALSE/UNVERIFIED")
        if "assets/data/proceedings-master-public-v1.json" not in text:
            errors.append(f"{path.relative_to(ROOT)} does not identify the public-safe derivative")
        if "archive/PROCEEDINGS_MASTER_REGISTER.csv" in text:
            errors.append(f"{path.relative_to(ROOT)} prints the non-browser operational path")
        if "assets/site.js?v=20260830c" not in text:
            errors.append(f"{path.relative_to(ROOT)} does not cache-bust the repaired runtime loader")

    required_js_phrases = (
        "assets/data/proceedings-master-public-v1.json",
        "#trace-proceeding=",
        "#isolation-test=",
        "#record-",
        "encodeURIComponent(r.Master_ID)",
        "data-master-id",
        "data-isolation-master-id",
        "isExactProceeding = stateValue === 'TRUE'",
        "const isolationLink = isExactProceeding",
        "isolation: 'Isolation test'",
        "isolation: 'Prueba de aislamiento'",
        "data-master-proceedings-nav",
        "data-master-proceedings-timeline-link",
        "Open_Reference_Gap",
        "Parent_Master_ID",
        "Linked_Proceedings",
        "linkMasterReferences",
        "#record-$1",
        "LZ-JUD-003",
        "LZ-APP-004",
        "arrecife-1103-2018-procedural-lineage",
        "arrecife-1103-2018-cadena-procesal",
    )
    for phrase in required_js_phrases:
        if phrase not in js:
            errors.append(f"public projection runtime missing control phrase: {phrase}")

    for forbidden in (
        "archive/PROCEEDINGS_MASTER_REGISTER.csv",
        "parseCsv",
        "isPublicRow",
        "Primary_Source_Anchor",
        "Repo_Canonical_Source",
        "Notes",
    ):
        if forbidden in js:
            errors.append(f"public runtime retains forbidden canonical/private token: {forbidden}")

    if "master-proceedings-publication-20260830.js" not in site:
        errors.append("assets/site.js does not load the master proceedings public runtime")
    if "master-proceedings-publication-20260830.js?v=20260830c" not in site:
        errors.append("assets/site.js does not cache-bust the repaired public runtime")
    if "data-master-proceedings-publication-loader', '20260830c'" not in site:
        errors.append("assets/site.js public-runtime loader marker is stale")

    required_columns = {
        "Master_ID", "Record_Type", "Is_Proceeding", "Proceeding_Class", "Stream",
        "Origin_Organ", "Current_Custodian", "Reference", "Date_or_Period", "Connection",
        "Object_or_Purpose", "Status", "Latest_Known_Event", "Appeal_or_Review",
        "Parent_Master_ID", "Linked_Proceedings", "Source_Status", "Open_Reference_Gap",
        "Public_Treatment",
    }
    with CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = sorted(required_columns - columns)
        if missing:
            errors.append("master CSV missing public-spine columns: " + ", ".join(missing))
        rows = list(reader)

    observed_treatments = {(row.get("Public_Treatment") or "").strip() for row in rows}
    governed_treatments = set(PUBLIC_TREATMENTS) | set(EXCLUDED_TREATMENTS)
    unknown_treatments = sorted(observed_treatments - governed_treatments)
    if unknown_treatments:
        errors.append("canonical CSV contains unreviewed public treatments")

    expected_public = [
        {field: row.get(field, "") or "" for field in FIELD_ALLOWLIST}
        for row in rows
        if (row.get("Public_Treatment") or "").strip() in PUBLIC_TREATMENTS
    ]
    expected_excluded = [
        row for row in rows
        if (row.get("Public_Treatment") or "").strip() in EXCLUDED_TREATMENTS
    ]
    public_records = projection.get("records", [])
    if projection.get("schema_version") != "1.0.0":
        errors.append("public proceedings projection schema version changed")
    if projection.get("canonical_source_id") != "PROCEEDINGS_MASTER_REGISTER":
        errors.append("public proceedings projection canonical source identity changed")
    if projection.get("derivation") != "DETERMINISTIC_ALLOWLIST":
        errors.append("public proceedings projection derivation control changed")
    if projection.get("canonical_source_sha256") != hashlib.sha256(CSV.read_bytes()).hexdigest():
        errors.append("public proceedings projection canonical source hash is stale")
    if projection.get("field_allowlist") != list(FIELD_ALLOWLIST):
        errors.append("public proceedings projection field allowlist changed")
    if projection.get("source_record_count") != len(rows):
        errors.append("public proceedings projection source denominator mismatch")
    if projection.get("public_record_count") != len(expected_public):
        errors.append("public proceedings projection public denominator mismatch")
    if projection.get("excluded_record_count") != len(expected_excluded):
        errors.append("public proceedings projection excluded denominator mismatch")
    if public_records != expected_public:
        errors.append("public proceedings projection does not exactly match the governed allowlisted rows")
    if not isinstance(public_records, list) or any(
        not isinstance(record, dict) or set(record) != set(FIELD_ALLOWLIST)
        for record in public_records
    ):
        errors.append("public proceedings projection contains missing or non-allowlisted record fields")
    public_ids = [record.get("Master_ID") for record in public_records if isinstance(record, dict)]
    expected_ids = [record["Master_ID"] for record in expected_public]
    if public_ids != expected_ids or len(public_ids) != len(set(public_ids)):
        errors.append("public proceedings projection does not preserve unique eligible Master_ID values")
    for private_field in PRIVATE_SOURCE_FIELDS:
        if f'"{private_field}"' in projection_text:
            errors.append(f"public proceedings projection exposes forbidden field: {private_field}")

    exact_public_records = [
        record for record in public_records
        if isinstance(record, dict) and (record.get("Is_Proceeding") or "").strip().upper() == "TRUE"
    ]
    non_exact_public_records = [
        record for record in public_records
        if isinstance(record, dict) and (record.get("Is_Proceeding") or "").strip().upper() != "TRUE"
    ]
    trace_destination_ids = {record["Master_ID"] for record in public_records if isinstance(record, dict)}
    isolation_destination_ids = {record["Master_ID"] for record in exact_public_records}
    if len(trace_destination_ids) != len(public_records) or trace_destination_ids != set(public_ids):
        errors.append("not every public record receives one exact trace destination")
    if len(exact_public_records) != 85 or len(isolation_destination_ids) != 85:
        errors.append("exact public isolation-link denominator must be 85/85")
    if len(non_exact_public_records) != 21:
        errors.append("FALSE/UNVERIFIED public isolation-ineligibility denominator must be 21")

    if not rows:
        errors.append("master CSV contains no rows")
    true_count = sum(1 for row in rows if (row.get("Is_Proceeding") or "").strip().upper() == "TRUE")
    unverified_count = sum(1 for row in rows if (row.get("Is_Proceeding") or "").strip().upper() == "UNVERIFIED")
    legacy_count = sum(1 for row in rows if (row.get("Public_Treatment") or "").strip() == "INTERNAL_KNOWLEDGE_REGISTER_NOT_AUTO_PUBLISHED")
    if true_count == 0:
        errors.append("master CSV unexpectedly contains no TRUE proceeding/file rows")
    if legacy_count and "legacy non-automatic-publication" not in protocol:
        errors.append("protocol must explain legacy public-treatment compatibility")

    for forbidden in ("do not create or promote a public aggregate proceedings page", "not a public-facing “all cases” page"):
        if forbidden.lower() in protocol.lower():
            errors.append(f"stale anti-publication rule remains in protocol: {forbidden}")

    if errors:
        print("MASTER PROCEEDINGS PUBLICATION AUDIT: FAILED")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("MASTER PROCEEDINGS PUBLIC RUNTIME AUDIT: PASSED (ADDITIVE STAGE)")
    print(f"Canonical rows: {len(rows)}")
    print(f"TRUE proceedings/files: {true_count}")
    print(f"UNVERIFIED candidates: {unverified_count}")
    print(f"Legacy public-treatment rows eligible for controlled projection: {legacy_count}")
    print(f"Public-safe projection: {len(public_records)} records; {len(expected_excluded)} excluded")
    print(f"Exact trace destinations: {len(trace_destination_ids)}/{len(public_records)} public records")
    print(f"Static isolation eligibility: {len(isolation_destination_ids)}/{len(exact_public_records)} TRUE records eligible; {len(non_exact_public_records)}/{len(non_exact_public_records)} FALSE/UNVERIFIED records ineligible")
    print("Browser-rendered isolation-link enforcement must be verified by the dedicated Playwright smoke; this static audit does not infer it.")
    print("Runtime allowlisted projection, bilingual routes, exact-trace/isolation links and navigation/timeline interlinking verified.")
    print("PUBLICATION BOUNDARY GAP: current-tree/Pages unpublishing of the canonical operational source is not verified by this audit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

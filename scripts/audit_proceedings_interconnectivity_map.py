#!/usr/bin/env python3
"""Structural/evidential audit for the proceedings map and Case Prism."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ".github/governance/UNITARY_PROCEEDINGS_INTERCONNECTIVITY_MAP_PROTOCOL_30AUG2026.md",
    ".github/governance/A_SCAN_360_CASE_PRISM_AND_READER_LENS_PROTOCOL_30AUG2026.md",
    "archive/PROCEEDINGS_ANTI_FRAGMENTATION_CONVERGENCE_RULE_30AUG2026.md",
    "archive/INSTITUTIONAL_READER_UNITARY_PROCEEDINGS_RULE_30AUG2026.md",
    "archive/CAIXABANK_VALENCIA_01859_2023_REGISTRATION_GAP_30AUG2026.md",
    "archive/PROCEEDINGS_MASTER_REGISTER_VALENCIA_1859_2023_OVERLAY_30AUG2026.md",
    "archive/PROCEEDINGS_CASE_PRISM_V1_SEED_30AUG2026.json",
    "archive/knowledge-project/DP1956_STATUS_REOPENING_CORRECTION_18AUG2026.md",
    "archive/PROCEEDINGS_MASTER_REGISTER.csv",
    "assets/data/proceedings-interconnectivity-schema-v1.json",
    "assets/data/proceedings-case-prism-v1.json",
    "assets/data/proceedings-master-public-v1.json",
    "assets/data/proceedings-interlinkability-v1.json",
    "assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json",
    "assets/data/counsel-procurador-gap-register-v1.json",
    "assets/proceedings-interconnectivity-map-20260830.js",
    "assets/proceedings-interconnectivity-map-20260830.css",
    "assets/master-proceedings-publication-20260830.js",
    "en/proceedings-map/index.html", "es/mapa-procedimientos/index.html",
    "en/master-proceedings-register/index.html", "es/registro-maestro-procedimientos/index.html",
    "en/public-authority-unitary-case-reconstruction/index.html",
    "es/reconstruccion-unitaria-autoridades-publicas/index.html",
    "en/calificacion-rpl-2523-evidence-map/index.html",
    "es/calificacion-rpl-2523-mapa-prueba/index.html",
    "en/insolvency-36-2012-administrator-removal-fees/index.html",
    "es/concurso-36-2012-separacion-ac-honorarios/index.html",
    "en/insolvency-36-2012-ap-section-4/index.html",
    "es/concurso-36-2012-ap-seccion-4/index.html",
    "en/insolvency-36-2012-insolvency-administrator/index.html",
    "es/concurso-36-2012-administrador-concursal/index.html",
    "en/insolvency-classification-parallel-lives/index.html",
    "es/calificacion-concurso-36-2012-vidas-paralelas/index.html",
    "en/fiscalia-dip-2-2026/index.html",
    "es/fiscalia-dip-2-2026/index.html",
    "en/public-prosecution-inspection-exp-gub-745-2026/index.html",
    "es/fiscalia-inspeccion-exp-gub-745-2026/index.html",
    "scripts/build_proceedings_case_prism_v2.py",
    "scripts/build_public_proceedings_projection.py",
    "scripts/build_proceedings_interlinkability_v1.py",
    "publication-manifests/all-proceedings-interlinkability-20260830.json",
    "docs/deletion-audits/2026-08-30-all-proceedings-interlinkability-continuity.md",
]
errors: list[str] = []


def require(condition: bool, label: str) -> None:
    if not condition:
        errors.append(label)


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def canonical_ids_in(value: str, candidates: set[str]) -> set[str]:
    """Return delimiter-safe canonical IDs named by one public field."""
    text = str(value or "")
    return {
        master_id
        for master_id in candidates
        if re.search(
            rf"(?<![A-Z0-9-]){re.escape(master_id)}(?![A-Z0-9-])",
            text,
            flags=re.IGNORECASE,
        )
    }


for relative in REQUIRED:
    require((ROOT / relative).is_file(), f"missing required file: {relative}")

if not errors:
    en, es = read("en/proceedings-map/index.html"), read("es/mapa-procedimientos/index.html")
    en_master, es_master = read("en/master-proceedings-register/index.html"), read("es/registro-maestro-procedimientos/index.html")
    en_clean = read("en/public-authority-unitary-case-reconstruction/index.html")
    es_clean = read("es/reconstruccion-unitaria-autoridades-publicas/index.html")
    institutional_feeders = {
        "EN Calificación": (read("en/calificacion-rpl-2523-evidence-map/index.html"), ("GC-APP-004",)),
        "ES Calificación": (read("es/calificacion-rpl-2523-mapa-prueba/index.html"), ("GC-APP-004",)),
        "EN AC": (read("en/insolvency-36-2012-administrator-removal-fees/index.html"), ("GC-APP-005", "GC-APP-006", "GC-APP-028")),
        "ES AC": (read("es/concurso-36-2012-separacion-ac-honorarios/index.html"), ("GC-APP-005", "GC-APP-006", "GC-APP-028")),
        "EN Fiscalía": (read("en/fiscalia-dip-2-2026/index.html"), ("GC-FIS-017",)),
        "ES Fiscalía": (read("es/fiscalia-dip-2-2026/index.html"), ("GC-FIS-017",)),
        "EN AP section 4": (read("en/insolvency-36-2012-ap-section-4/index.html"), ("GC-APP-004",)),
        "ES AP sección 4": (read("es/concurso-36-2012-ap-seccion-4/index.html"), ("GC-APP-004",)),
        "EN parallel lives": (read("en/insolvency-classification-parallel-lives/index.html"), ("GC-APP-004",)),
        "ES vidas paralelas": (read("es/calificacion-concurso-36-2012-vidas-paralelas/index.html"), ("GC-APP-004",)),
    }
    general_institutional_feeders = {
        "EN AC profile": read("en/insolvency-36-2012-insolvency-administrator/index.html"),
        "ES perfil AC": read("es/concurso-36-2012-administrador-concursal/index.html"),
        "EN Fiscalía inspection": read("en/public-prosecution-inspection-exp-gub-745-2026/index.html"),
        "ES Inspección Fiscalía": read("es/fiscalia-inspeccion-exp-gub-745-2026/index.html"),
    }
    js, css = read("assets/proceedings-interconnectivity-map-20260830.js"), read("assets/proceedings-interconnectivity-map-20260830.css")
    master_js = read("assets/master-proceedings-publication-20260830.js")
    gov = read(".github/governance/UNITARY_PROCEEDINGS_INTERCONNECTIVITY_MAP_PROTOCOL_30AUG2026.md")
    ascan = read(".github/governance/A_SCAN_360_CASE_PRISM_AND_READER_LENS_PROTOCOL_30AUG2026.md")
    anti = read("archive/PROCEEDINGS_ANTI_FRAGMENTATION_CONVERGENCE_RULE_30AUG2026.md")
    institutional = read("archive/INSTITUTIONAL_READER_UNITARY_PROCEEDINGS_RULE_30AUG2026.md")
    val_gap = read("archive/CAIXABANK_VALENCIA_01859_2023_REGISTRATION_GAP_30AUG2026.md")
    val_overlay = read("archive/PROCEEDINGS_MASTER_REGISTER_VALENCIA_1859_2023_OVERLAY_30AUG2026.md")
    dp_control = read("archive/knowledge-project/DP1956_STATUS_REOPENING_CORRECTION_18AUG2026.md")
    builder = read("scripts/build_proceedings_case_prism_v2.py")
    workflow = read(".github/workflows/audit-proceedings-interconnectivity-map.yml")
    schema = json.loads(read("assets/data/proceedings-interconnectivity-schema-v1.json"))
    prism = json.loads(read("assets/data/proceedings-case-prism-v1.json"))
    public_projection = json.loads(read("assets/data/proceedings-master-public-v1.json"))
    interlinkability = json.loads(read("assets/data/proceedings-interlinkability-v1.json"))
    lifecycle = json.loads(read("publication-manifests/all-proceedings-interlinkability-20260830.json"))
    counsel_gaps = json.loads(read("assets/data/counsel-procurador-gap-register-v1.json"))
    with (ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    ids = [row["Master_ID"].strip() for row in rows]
    by_id = {row["Master_ID"].strip(): row for row in rows}
    public_rows = public_projection.get("records", [])
    public_ids = [row.get("Master_ID", "").strip() for row in public_rows]
    public_by_id = {row.get("Master_ID", "").strip(): row for row in public_rows}
    exact_public_rows = [row for row in public_rows if row.get("Is_Proceeding", "").strip().upper() == "TRUE"]
    exact_public_ids = {row.get("Master_ID", "").strip() for row in exact_public_rows}
    require(len(rows) == 102, f"canonical denominator: expected 102, found {len(rows)}")
    require(len(ids) == len(set(ids)), "duplicate canonical Master_ID")
    require(public_projection.get("canonical_source_id") == "PROCEEDINGS_MASTER_REGISTER", "public projection canonical source identity changed")
    require(public_projection.get("derivation") == "DETERMINISTIC_ALLOWLIST", "public projection derivation is not allowlisted")
    require(
        public_projection.get("canonical_source_sha256")
        == hashlib.sha256((ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv").read_bytes()).hexdigest(),
        "public projection canonical-source digest mismatch",
    )
    require(public_projection.get("source_record_count") == len(rows), "public projection source denominator mismatch")
    require(public_projection.get("public_record_count") == len(public_rows), "public projection public denominator mismatch")
    require(len(public_ids) == len(set(public_ids)), "duplicate public-projection Master_ID")
    require(set(public_ids) <= set(ids), "public projection contains a non-canonical Master_ID")
    require(len(public_rows) == 101, f"public denominator: expected 101, found {len(public_rows)}")
    public_field_allowlist = set(public_projection.get("field_allowlist", []))
    forbidden_public_fields = {
        "Primary_Source_Anchor", "Repo_Canonical_Source", "Notes",
        "Public_Treatment", "Last_Scan_Date",
    }
    require(public_field_allowlist and not (public_field_allowlist & forbidden_public_fields), "public projection field allowlist admits a private/operational field")
    require(
        all(set(row) == public_field_allowlist for row in public_rows),
        "public projection records do not exactly match the field allowlist",
    )

    # An exact-proceeding denominator may never admit a synthetic family or
    # aggregate continuity object.  Such objects remain useful public nodes,
    # but they are not selectable as an exact file.
    for row in exact_public_rows:
        aggregate_markers = " ".join(
            (row.get("Record_Type", ""), row.get("Proceeding_Class", ""))
        ).upper()
        require(
            not any(marker in aggregate_markers for marker in ("FAMILY", "AGGREGATE")),
            f"aggregate/family object admitted as exact proceeding: {row.get('Master_ID')}",
        )

    # Complete exact-proceeding interlinkability denominator.  The canonical
    # source retains one excluded private exact file; neither its ID nor its
    # details may leak into the public registry.  Every one of the 84 public
    # exact files must then receive one controlled disposition.
    canonical_exact_ids = {
        row["Master_ID"].strip()
        for row in rows
        if row.get("Is_Proceeding", "").strip().upper() == "TRUE"
    }
    private_exact_ids = canonical_exact_ids - exact_public_ids
    require(len(canonical_exact_ids) == 85, f"canonical exact-proceeding denominator: expected 85, found {len(canonical_exact_ids)}")
    require(len(exact_public_ids) == 84, f"public exact-proceeding denominator: expected 84, found {len(exact_public_ids)}")
    require(len(private_exact_ids) == 1, "private exact-proceeding exclusion denominator must be one")
    interlink_serialised = json.dumps(interlinkability, ensure_ascii=False)
    require(not any(private_id in interlink_serialised for private_id in private_exact_ids), "private exact proceeding leaked into public interlinkability registry")
    require("archive/PROCEEDINGS_MASTER_REGISTER.csv" not in interlink_serialised, "public interlinkability registry exposes the operational canonical path")
    require(interlinkability.get("canonical_node_source_id") == "PROCEEDINGS_MASTER_REGISTER", "interlinkability canonical source identity changed")
    require(interlinkability.get("public_node_projection") == "assets/data/proceedings-master-public-v1.json", "interlinkability public projection changed")
    require(interlinkability.get("case_prism_source") == "assets/data/proceedings-case-prism-v1.json", "interlinkability Case Prism source changed")
    require(
        "joinder" in interlinkability.get("boundary_en", "").lower()
        and "acumul" in interlinkability.get("boundary_es", "").lower(),
        "interlinkability boundary is not bilingual or omits anti-joinder language",
    )

    scope = interlinkability.get("scope", {})
    scope_ids = scope.get("public_exact_proceeding_ids", [])
    require(scope.get("expected_count") == len(exact_public_ids) == 84, "interlinkability scope denominator mismatch")
    require(scope_ids == [row["Master_ID"] for row in exact_public_rows], "interlinkability scope does not exactly follow the public projection")
    require(set(scope.get("excluded_aggregate_reference_ids", [])) == {"GC-APP-007"}, "aggregate appeal-family exclusion not explicit")
    navigation_contract = interlinkability.get("navigation_contract", {})
    require(navigation_contract.get("exact_id_to_master_register") == "REQUIRED", "exact-ID Master Register navigation is not required")
    require(navigation_contract.get("exact_id_to_renderer") == "REQUIRED", "exact-ID renderer navigation is not required")
    require(navigation_contract.get("dossier_route_relationship") == "NOT_INFERRED", "registry overclaims a complete exact-ID dossier relationship")
    require(navigation_contract.get("en") and navigation_contract.get("es"), "interlinkability navigation contract is not bilingual")
    aggregate = public_by_id.get("GC-APP-007", {})
    require(aggregate.get("Is_Proceeding") == "FALSE", "GC-APP-007 remains selectable as an exact proceeding")
    require(aggregate.get("Record_Type") == "APPEAL_FAMILY_REFERENCE", "GC-APP-007 record type is not an aggregate reference")
    require(aggregate.get("Proceeding_Class") == "AGGREGATE_REFERENCE_NOT_PROCEEDING", "GC-APP-007 proceeding class is not an aggregate reference")

    classifications = {
        "DIRECT_PROCEDURAL_EDGE", "CONTROLLED_CONTEXTUAL_BRIDGE",
        "INDEPENDENT_TRACK", "EXPLICIT_RELATIONSHIP_GAP",
    }
    classification_catalog = interlinkability.get("classification_catalog", {})
    require(set(classification_catalog) == classifications, "interlinkability classification vocabulary mismatch")
    require(all(meta.get("en") and meta.get("es") for meta in classification_catalog.values()), "interlinkability classifications are not bilingual")
    for catalog_name in ("relationship_type_catalog", "context_type_catalog"):
        catalog = interlinkability.get(catalog_name, {})
        require(catalog and all(meta.get("en") and meta.get("es") for meta in catalog.values()), f"{catalog_name} is not bilingual")

    relationships = interlinkability.get("relationships", [])
    relationship_ids = [relationship.get("id") for relationship in relationships]
    relationship_by_id = {relationship.get("id"): relationship for relationship in relationships}
    require(len(relationship_ids) == len(set(relationship_ids)), "duplicate controlled relationship ID")
    expected_direct_pairs: set[tuple[str, str]] = set()
    for row in exact_public_rows:
        source_id = row["Master_ID"]
        parent_id = row.get("Parent_Master_ID", "").strip()
        if parent_id in exact_public_ids and parent_id != source_id:
            expected_direct_pairs.add(tuple(sorted((source_id, parent_id))))
        for field in ("Linked_Proceedings", "Appeal_or_Review"):
            for target_id in canonical_ids_in(row.get(field, ""), exact_public_ids):
                if target_id != source_id:
                    expected_direct_pairs.add(tuple(sorted((source_id, target_id))))
    actual_direct_pairs = {
        tuple(sorted((relationship.get("from_master_id", ""), relationship.get("to_master_id", ""))))
        for relationship in relationships
    }
    require(len(actual_direct_pairs) == len(relationships), "multiple direct relationships silently compete for one exact-proceeding pair")
    require(actual_direct_pairs == expected_direct_pairs, "controlled direct-edge registry omits or invents an exact canonical relationship pair")
    direct_field_by_type = {
        "PARENT_CHILD": "Parent_Master_ID",
        "LINKED_PROCEEDING": "Linked_Proceedings",
        "APPEAL_REVIEW_ID_LINK": "Appeal_or_Review",
    }
    assertion_fields = (
        "source_id", "source_record_master_id", "field", "value_token",
        "evidence_status", "assertion_relationship_type", "assertion_direction",
        "assertion_from_master_id", "assertion_to_master_id",
    )
    expected_source_assertions = []
    for source_row in exact_public_rows:
        source_id = source_row["Master_ID"]
        parent_id = source_row.get("Parent_Master_ID", "").strip()
        if parent_id in exact_public_ids and parent_id != source_id:
            expected_source_assertions.append(
                (
                    "PROCEEDINGS_MASTER_REGISTER", source_id, "Parent_Master_ID",
                    parent_id, source_row.get("Source_Status", ""), "PARENT_CHILD",
                    "FORWARD", parent_id, source_id,
                )
            )
        for field, relationship_type in (
            ("Linked_Proceedings", "LINKED_PROCEEDING"),
            ("Appeal_or_Review", "APPEAL_REVIEW_ID_LINK"),
        ):
            for target_id in sorted(canonical_ids_in(source_row.get(field, ""), exact_public_ids)):
                if target_id != source_id:
                    expected_source_assertions.append(
                        (
                            "PROCEEDINGS_MASTER_REGISTER", source_id, field, target_id,
                            source_row.get("Source_Status", ""), relationship_type,
                            "FORWARD", source_id, target_id,
                        )
                    )
    actual_source_assertions = []
    for relationship in relationships:
        rid = relationship.get("id", "<missing relationship ID>")
        source = relationship.get("source", {})
        from_id, to_id = relationship.get("from_master_id"), relationship.get("to_master_id")
        require(from_id in exact_public_ids and to_id in exact_public_ids and from_id != to_id, f"{rid} has a non-exact/private/self endpoint")
        require(relationship.get("relationship_class") == "DIRECT_PROCEDURAL_EDGE", f"{rid} is not a controlled direct edge")
        require(relationship.get("relationship_type") in direct_field_by_type, f"{rid} has an unsupported direct-edge type")
        require(relationship.get("direction") in {"FORWARD", "REVERSE_DERIVED", "BIDIRECTIONAL", "ONE_WAY"}, f"{rid} has an invalid direction")
        require(relationship.get("why_en") and relationship.get("why_es"), f"{rid} lacks bilingual why-connected text")
        require("joinder" in relationship.get("limitations_en", "").lower() and "acumul" in relationship.get("limitations_es", "").lower(), f"{rid} lacks bilingual anti-joinder limitations")
        require(relationship.get("public_safe") is True, f"{rid} is not explicitly public-safe")
        source_record_id = source.get("record_master_id")
        source_field = source.get("field")
        source_token = source.get("value_token")
        require(source.get("kind") == "MASTER_REGISTER_FIELD" and source.get("source_id") == "PROCEEDINGS_MASTER_REGISTER", f"{rid} lacks canonical-field provenance")
        require(source_field == direct_field_by_type.get(relationship.get("relationship_type")), f"{rid} source field does not match relationship type")
        source_row = by_id.get(source_record_id, {})
        require(source_record_id in {from_id, to_id} and source_token in {from_id, to_id} - {source_record_id}, f"{rid} source record/token do not match its endpoints")
        require(source_token and source_token in source_row.get(source_field, ""), f"{rid} is not supported by its claimed canonical field")
        source_assertions = relationship.get("source_assertions", [])
        require(relationship.get("supporting_assertion_count") == len(source_assertions) >= 1, f"{rid} supporting assertion count mismatch")
        for assertion in source_assertions:
            assertion_tuple = tuple(assertion.get(field) for field in assertion_fields)
            actual_source_assertions.append(assertion_tuple)
            require(
                {assertion.get("assertion_from_master_id"), assertion.get("assertion_to_master_id")}
                == {from_id, to_id},
                f"{rid} contains a source assertion for a different pair",
            )
    require(len(expected_source_assertions) == 19, f"expected 19 canonical direct assertions, found {len(expected_source_assertions)}")
    require(
        Counter(actual_source_assertions) == Counter(expected_source_assertions),
        "direct relationship source assertions do not exactly preserve the canonical-field assertion multiset",
    )
    source_verified_statuses = {"VERIFIED_PRIMARY", "VERIFIED_PROCEDURAL"}
    source_verified_pair_count = sum(
        all(
            assertion.get("evidence_status") in source_verified_statuses
            for assertion in relationship.get("source_assertions", [])
        )
        for relationship in relationships
    )
    source_reported_pending_pair_count = len(relationships) - source_verified_pair_count
    source_verified_assertion_count = sum(
        assertion[4] in source_verified_statuses
        for assertion in actual_source_assertions
    )
    source_reported_pending_assertion_count = (
        len(actual_source_assertions) - source_verified_assertion_count
    )
    require(
        (source_verified_pair_count, source_reported_pending_pair_count) == (15, 1),
        "direct-pair source grades must remain explicit at 15 verified / 1 reported-primary-pending",
    )
    require(
        (source_verified_assertion_count, source_reported_pending_assertion_count) == (18, 1),
        "direct-assertion source grades must remain explicit at 18 verified / 1 reported-primary-pending",
    )

    context_clusters = interlinkability.get("context_clusters", [])
    context_ids = [cluster.get("id") for cluster in context_clusters]
    context_by_id = {cluster.get("id"): cluster for cluster in context_clusters}
    require(len(context_ids) == len(set(context_ids)), "duplicate context-cluster ID")
    permitted_context_types = {"RECORDED_CONNECTION", "CASE_PRISM_PROPOSITION"}
    require(set(interlinkability.get("context_type_catalog", {})) == permitted_context_types, "context catalog admits a taxonomy-only or unknown bridge")
    prism_prop_by_id = {prop.get("id"): prop for prop in prism.get("propositions", [])}
    expected_connection_groups: dict[str, set[str]] = {}
    for row in exact_public_rows:
        connection = row.get("Connection", "").strip()
        if connection:
            expected_connection_groups.setdefault(connection, set()).add(row["Master_ID"])
    expected_connection_groups = {
        connection: members
        for connection, members in expected_connection_groups.items()
        if len(members) >= 2
    }
    actual_connection_groups = {
        cluster.get("source", {}).get("value"): set(cluster.get("member_master_ids", []))
        for cluster in context_clusters
        if cluster.get("context_type") == "RECORDED_CONNECTION"
    }
    require(actual_connection_groups == expected_connection_groups, "recorded-Connection clusters omit or invent an exact public member group")

    expected_prism_groups: dict[str, set[str]] = {}
    for prop in prism.get("propositions", []):
        members = {
            mid
            for cell in prop.get("cells", {}).values()
            if cell.get("status") != "OUTSIDE"
            for mid in cell.get("master_ids", [])
            if mid in exact_public_ids
        }
        if len(members) >= 2:
            expected_prism_groups[prop.get("id")] = members
    actual_prism_groups = {
        cluster.get("source", {}).get("record_id"): set(cluster.get("member_master_ids", []))
        for cluster in context_clusters
        if cluster.get("context_type") == "CASE_PRISM_PROPOSITION"
    }
    require(actual_prism_groups == expected_prism_groups, "Case Prism context clusters omit or invent a proposition-member group")
    for cluster in context_clusters:
        cid = cluster.get("id", "<missing context ID>")
        context_type = cluster.get("context_type")
        members = cluster.get("member_master_ids", [])
        source = cluster.get("source", {})
        require(context_type in permitted_context_types, f"{cid} has an unapproved context type")
        require(len(members) >= 2 and len(members) == len(set(members)) and set(members) <= exact_public_ids, f"{cid} has invalid context members")
        require(cluster.get("label_en") and cluster.get("label_es") and cluster.get("why_en") and cluster.get("why_es"), f"{cid} lacks bilingual reader text")
        limitations_en = cluster.get("limitations_en", "").lower()
        limitations_es = cluster.get("limitations_es", "").lower()
        require(limitations_en and limitations_es, f"{cid} lacks bilingual limitations")
        require(cluster.get("public_safe") is True, f"{cid} is not explicitly public-safe")
        if context_type == "RECORDED_CONNECTION":
            expected_field = "Connection"
            require(source.get("kind") == "MASTER_REGISTER_FIELD_GROUP" and source.get("source_id") == "PROCEEDINGS_MASTER_REGISTER", f"{cid} lacks canonical-group provenance")
            require(source.get("field") == expected_field and source.get("value"), f"{cid} source field/value mismatch")
            require(all(public_by_id[mid].get(expected_field) == source.get("value") for mid in members), f"{cid} invents a canonical-field grouping")
            require({item.get("master_id") for item in source.get("member_provenance", [])} == set(members), f"{cid} member provenance mismatch")
            require("joinder" in limitations_en and "acumul" in limitations_es, f"{cid} lacks bilingual anti-joinder limits")
        else:
            prop_id = source.get("record_id")
            prop = prism_prop_by_id.get(prop_id, {})
            admitted_members = {
                mid
                for cell in prop.get("cells", {}).values()
                if cell.get("status") != "OUTSIDE"
                for mid in cell.get("master_ids", [])
                if mid in exact_public_ids
            }
            require(source.get("kind") == "CASE_PRISM_PROPOSITION_MEMBERSHIP", f"{cid} lacks Case Prism provenance")
            require(source.get("path") == "assets/data/proceedings-case-prism-v1.json" and prop_id in prism_prop_by_id, f"{cid} references an unknown Case Prism proposition")
            require(set(members) == admitted_members, f"{cid} membership does not match its Case Prism proposition")
            require("do not prove receipt or treatment" in limitations_en and "no prueban recepción ni tratamiento" in limitations_es, f"{cid} does not preserve the proposition/file-treatment boundary")

    dispositions = interlinkability.get("node_dispositions", [])
    disposition_ids = [disposition.get("master_id") for disposition in dispositions]
    require(len(disposition_ids) == len(set(disposition_ids)) and set(disposition_ids) == exact_public_ids, "every public exact proceeding must have exactly one controlled disposition")
    disposition_counts = Counter(disposition.get("primary_classification") for disposition in dispositions)
    for disposition in dispositions:
        master_id = disposition.get("master_id", "<missing proceeding ID>")
        classification = disposition.get("primary_classification")
        direct_ids = disposition.get("relationship_ids", [])
        cluster_ids = disposition.get("context_cluster_ids", [])
        expected_disposition_relationship_ids = {
            relationship.get("id")
            for relationship in relationships
            if master_id in {
                relationship.get("from_master_id"), relationship.get("to_master_id")
            }
        }
        expected_disposition_cluster_ids = {
            cluster.get("id")
            for cluster in context_clusters
            if master_id in cluster.get("member_master_ids", [])
        }
        require(classification in classifications, f"{master_id} has an invalid interlink classification")
        require(disposition.get("why_en") and disposition.get("why_es"), f"{master_id} disposition lacks bilingual explanation")
        require("joinder" in disposition.get("limitations_en", "").lower() and "acumul" in disposition.get("limitations_es", "").lower(), f"{master_id} disposition lacks bilingual anti-joinder limitations")
        require(disposition.get("next_source_needed_en") and disposition.get("next_source_needed_es"), f"{master_id} disposition lacks a bilingual finite next-source test")
        require(disposition.get("next_source_needed_es") != "Revisar la fuente primaria indicada en Open_Reference_Gap antes de afirmar una relación adicional.", f"{master_id} disposition uses the generic Spanish next-source fallback")
        require(len(direct_ids) == len(set(direct_ids)) and set(direct_ids) == expected_disposition_relationship_ids, f"{master_id} disposition omits, duplicates or invents a direct relationship membership")
        require(len(cluster_ids) == len(set(cluster_ids)) and set(cluster_ids) == expected_disposition_cluster_ids, f"{master_id} disposition omits, duplicates or invents a material context-cluster membership")
        if public_by_id[master_id].get("Open_Reference_Gap", "").strip():
            require(disposition.get("next_source_needed_en") == public_by_id[master_id].get("Open_Reference_Gap"), f"{master_id} English next-source text diverges from the canonical finite request")
            require(
                disposition.get("next_source_needed_es")
                and disposition.get("next_source_needed_es")
                != "Revisar la fuente primaria indicada en Open_Reference_Gap antes de afirmar una relación adicional.",
                f"{master_id} uses a missing/generic Spanish next-source formulation",
            )
        require(all(rid in relationship_by_id and master_id in {relationship_by_id[rid].get("from_master_id"), relationship_by_id[rid].get("to_master_id")} for rid in direct_ids), f"{master_id} disposition has a foreign/unknown direct relationship")
        require(all(cid in context_by_id and master_id in context_by_id[cid].get("member_master_ids", []) for cid in cluster_ids), f"{master_id} disposition has a foreign/unknown context cluster")
        if classification == "DIRECT_PROCEDURAL_EDGE":
            require(bool(direct_ids) and disposition.get("basis", {}).get("kind") == "DIRECT_RELATIONSHIP_MEMBERSHIP", f"{master_id} direct classification lacks direct provenance")
        elif classification == "CONTROLLED_CONTEXTUAL_BRIDGE":
            require(not direct_ids and bool(cluster_ids) and disposition.get("basis", {}).get("kind") == "CONTEXT_CLUSTER_MEMBERSHIP", f"{master_id} context classification lacks controlled-cluster provenance")
        elif classification == "EXPLICIT_RELATIONSHIP_GAP":
            require(not direct_ids and not cluster_ids, f"{master_id} relationship gap fabricates a connection")
            require(disposition.get("next_source_needed_en") and disposition.get("next_source_needed_es"), f"{master_id} relationship gap lacks a bilingual next-source test")
            require(
                disposition.get("next_source_needed_es")
                != "Revisar la fuente primaria indicada en Open_Reference_Gap antes de afirmar una relación adicional.",
                f"{master_id} relationship gap uses the generic Spanish next-source fallback",
            )
            basis = disposition.get("basis", {})
            require(basis.get("kind") == "MASTER_REGISTER_FIELD" and basis.get("source_id") == "PROCEEDINGS_MASTER_REGISTER" and basis.get("field") == "Open_Reference_Gap", f"{master_id} relationship gap lacks canonical-field provenance")
            require(public_by_id[master_id].get("Open_Reference_Gap"), f"{master_id} relationship gap has no recorded source gap")
        else:
            require(not direct_ids and not cluster_ids and disposition.get("basis", {}).get("kind") == "NO_ADMITTED_RELATION_OR_GAP", f"{master_id} independent track fabricates a connection")

    interlink_coverage = interlinkability.get("coverage", {})
    case_prism_exact_ids = {
        mid
        for prop in prism.get("propositions", [])
        for cell in prop.get("cells", {}).values()
        if cell.get("status") != "OUTSIDE"
        for mid in cell.get("master_ids", [])
        if mid in exact_public_ids
    }
    require(interlink_coverage.get("canonical_exact_proceeding_count") == 85, "canonical exact-proceeding interlink denominator mismatch")
    require(interlink_coverage.get("public_exact_proceeding_count") == interlink_coverage.get("node_disposition_count") == 84, "public exact-proceeding interlink denominator mismatch")
    require(interlink_coverage.get("private_exact_excluded_count") == 1, "private exact-proceeding exclusion count mismatch")
    require(interlink_coverage.get("direct_relationship_count") == len(relationships), "direct relationship coverage count mismatch")
    require(interlink_coverage.get("direct_relationship_source_verified_pair_count") == source_verified_pair_count, "source-verified direct-pair coverage mismatch")
    require(interlink_coverage.get("direct_relationship_source_reported_pending_pair_count") == source_reported_pending_pair_count, "source-reported-pending direct-pair coverage mismatch")
    require(interlink_coverage.get("direct_source_assertion_count") == len(actual_source_assertions) == 19, "direct source-assertion coverage mismatch")
    require(interlink_coverage.get("direct_source_verified_assertion_count") == source_verified_assertion_count, "source-verified direct-assertion coverage mismatch")
    require(interlink_coverage.get("direct_source_reported_pending_assertion_count") == source_reported_pending_assertion_count, "source-reported-pending direct-assertion coverage mismatch")
    require(interlink_coverage.get("context_cluster_count") == len(context_clusters), "context-cluster coverage count mismatch")
    require(interlink_coverage.get("recorded_stream_cluster_count") == 0, "same-stream taxonomy was promoted into material reconnection context")
    require(interlink_coverage.get("case_prism_exact_proceeding_covered_count") == len(case_prism_exact_ids) == 24, "Case Prism exact-proceeding covered denominator mismatch")
    require(interlink_coverage.get("case_prism_exact_proceeding_uncovered_count") == len(exact_public_ids - case_prism_exact_ids) == 60, "Case Prism exact-proceeding uncovered denominator mismatch")
    require(interlink_coverage.get("decision_dependency_exact_coverage") == "GAP_24_OF_84", "decision-dependency exact coverage is overstated")
    require(interlink_coverage.get("bilingual_specific_next_source_count") == 84, "bilingual next-source denominator is not 84/84")
    require(interlink_coverage.get("bilingual_specific_next_source_coverage") == "VERIFIED_84_OF_84", "bilingual specific next-source coverage is not verified 84/84")
    require(interlink_coverage.get("exact_proceeding_full_finite_test_count") == 0, "exact-proceeding disposition actionability count is overstated")
    require(interlink_coverage.get("exact_proceeding_full_finite_test_coverage") == "GAP_0_OF_84", "exact-proceeding full finite-test gap is not explicit")
    require("bilingual_actionability" not in interlink_coverage, "next-source coverage is mislabeled as full bilingual actionability")
    require(interlink_coverage.get("classification_counts") == {token: disposition_counts.get(token, 0) for token in classifications}, "disposition classification coverage mismatch")
    require(interlink_coverage.get("unexplained_exact_proceeding_count") == 0, "public exact proceeding remains unclassified")
    require(interlink_coverage.get("geography_only_bridge_count") == 0, "Geography-only bridge admitted")

    # Corrections must be consolidated into the runtime source, not left as overlays.
    val = by_id.get("VAL-CIV-001", {})
    expected_val = {
        "Record_Type": "JUDICIAL_PROCEEDING", "Is_Proceeding": "TRUE", "Proceeding_Class": "DIRECT",
        "Origin_Organ": "Juzgado de Primera Instancia nº 27 de Valencia",
        "Current_Custodian": "Juzgado de Primera Instancia nº 27 de Valencia",
        "Reference": "ORD 1859/2023-9", "Secondary_Reference": "Aweswell Limited v CAIXABANK, S.A.",
        "NIG": "46250-42-1-2023-0049579", "Status": "Pending and contested",
        "Source_Status": "VERIFIED_PRIMARY_DERIVED_PUBLIC_CONTROL", "Public_Treatment": "PUBLIC_CONTROLLED",
    }
    for field, value in expected_val.items():
        require(val.get(field) == value, f"VAL-CIV-001 {field} not consolidated")
    require("28 Jan 2027 at 10:00" in val.get("Latest_Known_Event", ""), "VAL-CIV-001 hearing not consolidated")
    overlay_retired = (
        "RETIRED IN CORRECTIVE SOURCE TREE" in val_overlay
        and "public/main retirement effective" in val_overlay
    ) or "RETIRED AFTER CANONICAL CONSOLIDATION" in val_overlay
    gap_consolidated = (
        "SOURCE-TREE CONSOLIDATION COMPLETE" in val_gap
        and "public/main closure effective" in val_gap
    ) or ("CLOSED" in val_gap and "physically consolidated" in val_gap)
    require(overlay_retired, "Valencia overlay retirement state missing")
    require(gap_consolidated, "Valencia reconciliation consolidation state missing")
    dp = by_id.get("GC-CRI-009", {})
    require("Provisional dismissal" in dp.get("Status", ""), "GC-CRI-009 provisional dismissal missing")
    require("no filed reform/subsidiary appeal" in dp.get("Status", ""), "GC-CRI-009 filed-appeal correction missing")
    require("No filed reform/subsidiary appeal" in dp.get("Appeal_or_Review", ""), "GC-CRI-009 appeal field stale")
    require("A draft challenge is not a filed act" in dp.get("Notes", ""), "GC-CRI-009 draft/filed boundary missing")
    require("No filed reform/subsidiary appeal" in dp_control, "DP1956 provenance correction lost")
    require(by_id.get("GC-APP-004", {}).get("Parent_Master_ID") == "GC-CAL-002", "RPL 2523 parent must be GC-CAL-002")

    # Parent relationships must resolve and be acyclic.
    parents = {row["Master_ID"]: row["Parent_Master_ID"].strip() for row in rows if row["Parent_Master_ID"].strip()}
    for child, parent_id in parents.items():
        require(parent_id in by_id, f"unresolved parent {parent_id} for {child}")
    for start in parents:
        seen, cursor = set(), start
        while cursor in parents:
            if cursor in seen:
                errors.append(f"parent cycle from {start}: {cursor}")
                break
            seen.add(cursor)
            cursor = parents[cursor]

    statuses = {"DIRECT", "CONTEXT", "OPEN", "NOT_LOCATED", "OUTSIDE"}
    treatments = {"DIRECTLY_IN_FILE", "EXPRESSLY_ACKNOWLEDGED", "RELIED_UPON", "CONTRADICTED", "MATERIALLY_RELEVANT_CONTEXT", "NOT_RAISED_OR_NOT_LOCATED", "OUTSIDE_PROCEDURAL_SCOPE", "STATUS_UNRESOLVED"}
    expected_lanes = {"concurso", "calificacion", "removal", "fees", "arrecife", "valencia", "meetingpoint", "tenerife", "fiscalia", "supervision", "historical", "publicmoney"}
    expected_audiences = {"all", "court", "appellate", "fiscal", "supervision", "authority", "research", "owner", "professional"}
    lanes, props = prism.get("lanes", []), prism.get("propositions", [])
    lane_ids = [lane.get("id") for lane in lanes]
    lane_set = set(lane_ids)
    lane_master_ids = {lane.get("id"): set(lane.get("master_ids", [])) for lane in lanes}
    prop_ids = {prop.get("id") for prop in props}
    audience_ids = {lens.get("id") for lens in prism.get("audience_lenses", [])}
    cells = [cell for prop in props for cell in prop.get("cells", {}).values()]
    referenced_ids = {mid for lane in lanes for mid in lane.get("master_ids", [])} | {mid for cell in cells for mid in cell.get("master_ids", [])}
    require(prism.get("schema_version") == "2.0.0", "Case Prism schema must be 2.0.0")
    require(prism.get("canonical_node_source_id") == "PROCEEDINGS_MASTER_REGISTER", "Case Prism canonical source identity changed")
    require(len(lane_ids) == len(lane_set) == 12 and lane_set == expected_lanes, "Case Prism lane denominator changed")
    require(prop_ids == {f"P{i:02d}" for i in range(1, 19)}, "Case Prism proposition denominator must be P01-P18")
    require(audience_ids == expected_audiences, "Case Prism audience denominator changed")
    require(set(prism.get("statuses", {})) == statuses, "relationship vocabulary mismatch")
    require(set(prism.get("treatments", {})) == treatments, "treatment vocabulary mismatch")
    require(referenced_ids <= set(by_id), f"unknown Case Prism IDs: {sorted(referenced_ids - set(by_id))}")
    require("GC-APP-007" not in referenced_ids, "synthetic removal-family object exposed as a third exact proceeding")
    require({"GC-APP-004", "GC-APP-005", "GC-APP-006", "GC-APP-028"} <= referenced_ids, "exact appellate IDs missing")
    prism_exact_covered_ids = {
        mid
        for cell in cells
        if cell.get("status") != "OUTSIDE"
        for mid in cell.get("master_ids", [])
        if mid in exact_public_ids
    }
    prism_exact_uncovered_ids = exact_public_ids - prism_exact_covered_ids
    require(len(prism_exact_covered_ids) == 24 and len(prism_exact_uncovered_ids) == 60, "Case Prism exact-file content denominator must remain explicit at 24/84 covered and 60/84 uncovered")

    prop_fields = {"id", "sort", "period_en", "period_es", "title_en", "title_es", "question_en", "question_es", "source_status", "attribution", "contrary_record", "decision_dependency", "actionability", "source_ids", "audience_priority", "cells"}
    cell_fields = {"status", "treatment", "evidence_status", "note_en", "note_es", "decision_en", "decision_es", "master_ids", "representation_lineage_status", "representation_gap_ids"}
    action_fields = {"source_needed", "competent_organ", "if_confirmed", "if_refuted"}
    source_catalog = prism.get("source_catalog", {})
    evidence_tokens = (
        {prop.get("source_status") for prop in props}
        | {cell.get("evidence_status") for cell in cells}
        | {source.get("evidence_status") for source in source_catalog.values()}
    )
    evidence_catalog = prism.get("evidence_statuses", {})
    require(set(evidence_catalog) == evidence_tokens, "bilingual evidence-status catalog denominator mismatch")
    require(all(meta.get("en") and meta.get("es") for meta in evidence_catalog.values()), "evidence-status catalog is not bilingual")
    counsel_gap_rows = counsel_gaps.get("gaps", []) if isinstance(counsel_gaps, dict) else counsel_gaps
    known_gap_ids = {item.get("gap_id") for item in counsel_gap_rows}
    for prop in props:
        pid = prop.get("id")
        require(prop_fields <= set(prop), f"{pid} missing proposition fields")
        require(set(prop.get("cells", {})) == lane_set, f"{pid} does not materialise every lane")
        require(set(prop.get("audience_priority", {})) >= audience_ids, f"{pid} lacks lens priorities")
        require(action_fields <= set(prop.get("actionability", {})), f"{pid} lacks finite actionability")
        require(prop.get("period_en") and prop.get("period_es") and "period" not in prop, f"{pid} period is not bilingual")
        for source_id in prop.get("source_ids", []):
            require(source_id in source_catalog, f"{pid} references unknown source {source_id}")
        for lane_id, cell in prop.get("cells", {}).items():
            require(cell_fields <= set(cell), f"{pid}/{lane_id} missing cell fields")
            require(set(cell.get("master_ids", [])) <= lane_master_ids[lane_id], f"{pid}/{lane_id} contains a cross-lane Master ID")
            require(cell.get("status") in statuses, f"{pid}/{lane_id} invalid relationship status")
            require(cell.get("treatment") in treatments, f"{pid}/{lane_id} invalid treatment")
            require(cell.get("note_en") and cell.get("note_es"), f"{pid}/{lane_id} lacks bilingual reason")
            require(cell.get("decision_en") and cell.get("decision_es"), f"{pid}/{lane_id} lacks decision dependency")
            require(set(cell.get("representation_gap_ids", [])) <= known_gap_ids, f"{pid}/{lane_id} unknown representation gap")

    relation_counts, treatment_counts = Counter(c["status"] for c in cells), Counter(c["treatment"] for c in cells)
    require(len(cells) == len(lanes) * len(props) == 216, f"expected 216 coordinates, found {len(cells)}")
    require(set(relation_counts) == statuses, "every relationship status must be used")
    require(treatment_counts["CONTRADICTED"] >= 1, "adverse/contrary treatment not represented")
    coverage = prism.get("coverage", {})
    require(coverage.get("explicit_coordinate_count") == 216 and coverage.get("unexplained_coordinate_count") == 0, "coverage denominator mismatch")
    require(coverage.get("counsel_procurador_denominator") == "GAP", "counsel/procurador incompleteness not explicit")
    for source_id, source in source_catalog.items():
        for language in ("en", "es"):
            href = source.get(f"href_{language}", "")
            require(href and (ROOT / href / "index.html").is_file(), f"{source_id} {language} route unresolved: {href}")

    required_views = {"CONVERGENCE_CLUSTER", "FRAGMENTATION_AUDIT", "DECISION_DEPENDENCY_MATRIX", "PARALLEL_PROCEEDINGS_LANES", "ISOLATION_TEST", "AUDIENCE_LENS"}
    require(schema.get("schema_version") == "1.5.0", "interconnectivity schema must be 1.5.0")
    require(schema.get("canonical_node_source_id") == "PROCEEDINGS_MASTER_REGISTER", "schema canonical source identity changed")
    require(required_views <= set(schema.get("required_views", [])), "schema required views missing")
    require(required_views <= set(schema.get("implemented_public_views", {})), "schema runtime mappings missing")
    require(set(schema.get("case_prism_cell_statuses", [])) == statuses, "schema relationship vocabulary mismatch")
    require(schema.get("implementation_contract", {}).get("bilingual_evidence_status_catalog_required") is True, "schema bilingual evidence-status requirement missing")
    require(schema.get("implementation_contract", {}).get("independent_case_prism_generation_seed_required") is True, "schema independent generation-seed requirement missing")
    implementation_contract = schema.get("implementation_contract", {})
    exact_contract = {
        "public_record_trace_denominator": 101,
        "canonical_exact_proceeding_denominator": 85,
        "public_exact_proceeding_denominator": 84,
        "private_exact_proceeding_excluded_denominator": 1,
        "public_exact_disposition_denominator": 84,
        "exact_direct_relationship_pair_denominator": len(expected_direct_pairs),
        "exact_direct_relationship_source_verified_pair_denominator": source_verified_pair_count,
        "exact_direct_relationship_source_reported_pending_pair_denominator": source_reported_pending_pair_count,
        "exact_direct_source_assertion_denominator": len(actual_source_assertions),
        "exact_direct_source_verified_assertion_denominator": source_verified_assertion_count,
        "exact_direct_source_reported_pending_assertion_denominator": source_reported_pending_assertion_count,
        "material_context_cluster_denominator": len(context_clusters),
        "case_prism_exact_proceeding_covered_denominator": len(prism_exact_covered_ids),
        "case_prism_exact_proceeding_uncovered_denominator": len(prism_exact_uncovered_ids),
        "decision_dependency_exact_coverage_status": "GAP_24_OF_84",
        "cell_treatment_source_coverage_status": "GAP_PROPOSITION_LEVEL_SOURCES_ONLY",
        "actor_specific_knowledge_receipt_trace_status": "GAP_NOT_MODELLED",
        "exact_id_to_dossier_source_route_coverage_status": "GAP_DENOMINATOR_NOT_ESTABLISHED",
        "fragmentation_selector_coverage_status": "VERIFIED_84_OF_84",
        "fragmentation_content_coverage_status": "GAP_24_OF_84_WITH_CASE_PRISM_COORDINATE",
        "bilingual_specific_next_source_denominator": 84,
        "bilingual_specific_next_source_coverage_status": "VERIFIED_84_OF_84",
        "exact_proceeding_full_finite_test_coverage_status": "GAP_0_OF_84",
        "stable_exact_trace_fragment": "#trace-proceeding=<Master_ID>",
        "stable_exact_isolation_fragment": "#isolation-test=<Master_ID>",
        "aggregate_reference_excluded_from_exact_selection": "GC-APP-007",
    }
    for field, expected in exact_contract.items():
        require(implementation_contract.get(field) == expected, f"schema implementation contract mismatch: {field}")
    require(implementation_contract.get("material_context_types") == ["RECORDED_CONNECTION", "CASE_PRISM_PROPOSITION"], "schema material context types changed")
    require(implementation_contract.get("taxonomy_only_context_types") == ["STREAM", "GEOGRAPHY", "CHRONOLOGY"], "schema taxonomy-only context boundary changed")

    lifecycle_denominator = lifecycle.get("implementation_denominator", {})
    lifecycle_completion = lifecycle.get("completion_denominator", {})
    require(lifecycle.get("current_state") in {"PREPARED_PENDING_MERGE", "PR_OPEN", "CI_GREEN", "MERGED", "DEPLOYED", "LIVE_VERIFIED", "DELETION_SAFE"}, "interlinkability lifecycle state is invalid")
    require(lifecycle_denominator.get("public_records_traceable") == 101, "lifecycle public trace denominator mismatch")
    require(lifecycle_denominator.get("public_exact_proceedings") == 84 and lifecycle_denominator.get("public_exact_dispositions") == 84, "lifecycle exact interlink denominator mismatch")
    require(lifecycle_denominator.get("direct_procedural_pairs_source_verified") == 15 and lifecycle_denominator.get("direct_procedural_pairs_source_reported_primary_pending") == 1, "lifecycle direct-pair evidence grades are incomplete")
    require(lifecycle_completion.get("decision_dependency_coverage") == "GAP_24_OF_84", "lifecycle overstates decision-dependency coverage")
    require(lifecycle_completion.get("cell_treatment_source_coverage") == "GAP_PROPOSITION_LEVEL_SOURCES_ONLY", "lifecycle overstates cell-level source coverage")
    require(lifecycle_completion.get("actor_specific_knowledge_receipt_trace") == "GAP_NOT_MODELLED", "lifecycle overstates actor-specific knowledge/receipt tracing")
    require(lifecycle_completion.get("exact_id_to_dossier_source_route_coverage") == "GAP_DENOMINATOR_NOT_ESTABLISHED", "lifecycle overstates exact-ID dossier/source routing")
    require(lifecycle_completion.get("exact_proceeding_full_finite_test_coverage") == "GAP_0_OF_84_AT_DISPOSITION_LEVEL", "lifecycle overstates exact-proceeding finite actionability")

    renderer_tokens = {
        "pdim-prism-table": "decision matrix", "pdim-swimlane": "stable swimlane", "data-lane-heading": "lane headings",
        "data-isolation-id": "exact-file isolation", "data-isolation-restore": "restore control", "sourceLinks": "source links",
        "contrary_record": "contrary record", "decision_dependency": "decision dependency", "actionability": "actionability",
        "representation_lineage_status": "representation gaps", "#case-prism": "hash activation",
        "role=\"tabpanel\"": "tab panel", "role=\"tab\"": "semantic tabs", "prismUnavailable": "degraded state",
        "sourceScope": "proposition-level source boundary", "outsideSelected": "accessible suppressed state",
        "evidenceStatusLabel": "bilingual evidence status",
        "revealActivePanel": "deep-link panel reveal", "mapped || 'map'": "hash back-navigation restore",
        "addEventListener('input', () => draw())": "safe filter redraw",
        "assets/data/proceedings-master-public-v1.json": "minimised public proceedings projection",
        "assets/data/proceedings-interlinkability-v1.json": "controlled interlinkability registry",
        "data-isolation-reconnection": "selected-file reconnection surface",
        "data-isolation-direct": "direct-edge reconnection section",
        "data-isolation-context": "controlled-context reconnection section",
        "data-isolation-unresolved": "independent/gap reconnection section",
        "data-interlink-disposition": "controlled node disposition",
        "#trace-proceeding=": "stable exact trace deep link",
        "#isolation-test=": "stable exact isolation deep link",
        "direct_relationship_source_verified_pair_count": "direct-edge evidence-grade denominator",
        "if (initialHash.canonicalize) replaceActiveHash();": "cold-load invalid-isolation canonicalisation",
        "if (parsed.canonicalize) replaceActiveHash();": "hashchange invalid-isolation canonicalisation",
    }
    for token, label in renderer_tokens.items():
        require(token in js, f"renderer missing {label}")
    require("pdim-prism-dash" not in js, "renderer can emit unexplained dashes")
    require("data-isolation-lane" not in js, "aggregate-lane isolation remains")
    require("toUpperCase() === 'TRUE'" in js, "exact isolation admits unverified objects")
    require("archive/PROCEEDINGS_MASTER_REGISTER.csv" not in js, "renderer still downloads the operational canonical CSV")
    require("parseCsv" not in js, "renderer still carries client-side canonical CSV parsing")
    require("fallbackEdges" not in js, "renderer can infer a direct edge for a non-exact/unclassified node")
    require("if (cluster.context_type === 'CASE_PRISM_PROPOSITION')" in js and "linkedPrismPropIds.add(propositionId)" in js, "renderer does not bound a Case Prism cluster to its own proposition")
    require("else if (cluster.context_type === 'RECORDED_CONNECTION')" in js, "renderer does not keep recorded-Connection reconnection separate")
    require("return cell.status === 'DIRECT' && cell.master_ids.some((id) => reconnectIds.has(id));" in js, "renderer lets a one-hop neighbour's contextual coordinate expand the isolation result")
    require("#trace-proceeding=${encodeURIComponent(r.Master_ID)}" in master_js, "Master Register lacks exact-ID trace links")
    require('id="record-${esc(r.Master_ID)}"' in master_js, "Master Register lacks stable exact-ID row anchors")
    require("archive/PROCEEDINGS_MASTER_REGISTER.csv" not in master_js and "assets/data/proceedings-master-public-v1.json" in master_js, "Master Register still consumes the operational canonical CSV")
    require('role="tabpanel" aria-live=' not in js and 'data-proceedings-map="20260830" aria-live=' not in en + es, "nested broad live regions remain")
    require(all(token in css for token in (".pdim-swimlane", ".pdim-isolation-map", ".pdim-dependency-grid", ":focus-visible", "prefers-reduced-motion")), "Prism CSS/accessibility contract incomplete")
    require("json.loads(SEED.read_text" in builder and "json.loads(TARGET.read_text" not in builder, "Case Prism builder is not independent of its generated target")
    require("archive/PROCEEDINGS_CASE_PRISM_V1_SEED_30AUG2026.json" in builder, "Case Prism builder seed path missing")
    require(all(field not in js for field in ("Primary_Source_Anchor", "Repo_Canonical_Source", "Notes")), "renderer exposes non-public raw source fields")

    for page, label in [(en, "EN map"), (es, "ES map"), (en_master, "EN Master"), (es_master, "ES Master")]:
        require("public-authority-unitary-case-reconstruction" in page or "reconstruccion-unitaria-autoridades-publicas" in page, f"{label} lacks clean-room route")
    for page, label in ((en, "EN map"), (es, "ES map")):
        require("PROCEEDINGS_MASTER_REGISTER" in page and "assets/data/proceedings-master-public-v1.json" in page, f"{label} does not disclose the minimised public projection")
        require("archive/PROCEEDINGS_MASTER_REGISTER.csv" not in page, f"{label} exposes the operational canonical path")
    require("proceedings-map" in en_clean and "master-proceedings-register" in en_clean, "EN clean room lacks map/register links")
    require("mapa-procedimientos" in es_clean and "registro-maestro-procedimientos" in es_clean, "ES clean room lacks map/register links")
    for label, (page, master_ids) in institutional_feeders.items():
        for master_id in master_ids:
            require(f"#trace-proceeding={master_id}" in page, f"{label} lacks exact trace link for {master_id}")
            require(f"#isolation-test={master_id}" in page, f"{label} lacks exact isolation link for {master_id}")
    for label, page in general_institutional_feeders.items():
        require("#case-prism" in page and "#isolation-test" in page, f"{label} lacks Case Prism/isolation navigation")
        require("master-proceedings-register" in page or "registro-maestro-procedimientos" in page, f"{label} lacks Master Register navigation")
        require("public-authority-unitary-case-reconstruction" in page or "reconstruccion-unitaria-autoridades-publicas" in page, f"{label} lacks institutional clean-room navigation")
    require("#case-prism" in en and "#case-prism" in es, "Case Prism CTA fragment missing")
    require(all(f'id="{anchor}"' in en and f'id="{anchor}"' in es for anchor in ("parallel-lanes", "isolation-test")), "deep-link anchors missing")
    require(all(f"proceedings-interconnectivity-map-20260830.{ext}?v=20260830g" in en and f"proceedings-interconnectivity-map-20260830.{ext}?v=20260830g" in es for ext in ("js", "css")), "Case Prism asset cache version not advanced")

    refs = ["RPL 2523/2025", "RPL 3304/2025", "RPL 3319/2025", "RPL 421/2026"]
    require(all(ref in institutional for ref in refs), "three-appellate-object correction missing")
    require("Do not describe `RPL 3319/2025` as the fees appeal" in institutional, "RPL 3319 fees correction missing")
    require("beginning → end" in gov and "end → beginning" in gov, "bidirectional governance missing")
    require("DIRECT PROCEDURAL EDGE" in gov and "CONTEXTUAL BRIDGE" in gov, "direct/context split missing")
    require("Fragmentation / atomisation audit" in gov, "fragmentation governance missing")
    require(all(word in ascan for word in ("Architecture", "Authority", "Attribution", "Audience", "Actionability")), "A-SCAN governance incomplete")
    require("does not prove that an organ knew" in ascan, "isolation boundary missing")
    require("procedural separateness" in anti.lower() and "patrimonial" in anti.lower(), "anti-fragmentation rule incomplete")

    for path in [
        "archive/PROCEEDINGS_ANTI_FRAGMENTATION_CONVERGENCE_RULE_30AUG2026.md",
        "archive/INSTITUTIONAL_READER_UNITARY_PROCEEDINGS_RULE_30AUG2026.md",
        "archive/CAIXABANK_VALENCIA_01859_2023_REGISTRATION_GAP_30AUG2026.md",
        "archive/PROCEEDINGS_MASTER_REGISTER_VALENCIA_1859_2023_OVERLAY_30AUG2026.md",
        "archive/PROCEEDINGS_CASE_PRISM_V1_SEED_30AUG2026.json",
        "assets/data/proceedings-master-public-v1.json",
        "assets/data/proceedings-interlinkability-v1.json",
        "assets/master-proceedings-publication-20260830.js",
        "assets/site.js",
        "assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json",
        "scripts/build_public_proceedings_projection.py",
        "scripts/build_proceedings_case_prism_v2.py",
        "scripts/build_proceedings_interlinkability_v1.py",
        "assets/data/counsel-procurador-gap-register-v1.json",
        "publication-manifests/all-proceedings-interlinkability-20260830.json",
        "docs/deletion-audits/2026-08-30-all-proceedings-interlinkability-continuity.md",
    ]:
        require(path in workflow, f"workflow filter missing dependency: {path}")
    require("python3 scripts/build_public_proceedings_projection.py --check" in workflow, "workflow does not rebuild-check the public proceedings projection")
    require("python3 scripts/build_proceedings_interlinkability_v1.py --check" in workflow, "workflow does not rebuild-check exact-proceeding interlinkability")
    smoke = read("scripts/smoke_proceedings_case_prism.mjs")
    require("#isolation-test=GC-APP-007" in smoke and "hashchange aggregate isolation" in smoke, "browser smoke does not reject/canonicalise aggregate isolation deep links")

if errors:
    print("PROCEEDINGS INTERCONNECTIVITY MAP AUDIT: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("PROCEEDINGS INTERCONNECTIVITY MAP AUDIT: PASS")
print("- canonical denominator: 102 rows / 101 controlled public rows")
print("- exact proceedings: 85 canonical / 84 public / 1 private exact record excluded")
print("- interlinkability: 84/84 public exact proceedings classified / 0 unexplained")
print(f"- controlled reconnection: {len(relationships)} exact pairs ({source_verified_pair_count} source-verified / {source_reported_pending_pair_count} source-reported pending) / {len(actual_source_assertions)} canonical assertions ({source_verified_assertion_count} verified / {source_reported_pending_assertion_count} pending) / {len(context_clusters)} material context clusters")
print("- structural exact selector/reconnection: VERIFIED 84/84; full-corpus restore available")
print("- decision-dependency / fragmentation content coverage: GAP — 24/84 exact proceedings covered; 60 without Case Prism coordinate")
print("- Stream, Geography and Chronology remain taxonomy/navigation only")
print("- aggregate appeal-family reference retained but excluded from exact selection")
print("- overlays consolidated and parent graph acyclic")
print("- Case Prism structure: 18 propositions x 12 lanes = 216 explicit coordinates / 0 structural blanks")
print("- relationship and file-treatment vocabularies structurally validated; cell-level evidentiary completeness is not inferred")
print("- cell-treatment source coverage: GAP — source routes are proposition-level; actor-specific knowledge/receipt trace: GAP — not modelled")
print("- exact-ID to proceeding-specific dossier/source-route coverage: GAP — denominator not established")
print("- proposition-level source routes, contrary record, decision dependency and finite actionability fields validated")
print("- stable parallel lanes and structural isolation mechanics validated; content remains GAP 24/84")
print("- nine audience lenses and bilingual source routes validated")
print("- bilingual specific next-source coverage: VERIFIED 84/84; full exact-proceeding finite-test objects: GAP 0/84")
print("- EN/ES institutional feeders expose exact trace and isolation deep links")
print("- counsel/procurador denominator remains an explicit GAP")

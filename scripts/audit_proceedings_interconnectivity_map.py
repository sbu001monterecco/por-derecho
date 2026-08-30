#!/usr/bin/env python3
"""Structural/evidential audit for the proceedings map and Case Prism."""

from __future__ import annotations

import csv
import json
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
    "assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json",
    "assets/data/counsel-procurador-gap-register-v1.json",
    "assets/proceedings-interconnectivity-map-20260830.js",
    "assets/proceedings-interconnectivity-map-20260830.css",
    "en/proceedings-map/index.html", "es/mapa-procedimientos/index.html",
    "en/master-proceedings-register/index.html", "es/registro-maestro-procedimientos/index.html",
    "en/public-authority-unitary-case-reconstruction/index.html",
    "es/reconstruccion-unitaria-autoridades-publicas/index.html",
    "scripts/build_proceedings_case_prism_v2.py",
]
errors: list[str] = []


def require(condition: bool, label: str) -> None:
    if not condition:
        errors.append(label)


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


for relative in REQUIRED:
    require((ROOT / relative).is_file(), f"missing required file: {relative}")

if not errors:
    en, es = read("en/proceedings-map/index.html"), read("es/mapa-procedimientos/index.html")
    en_master, es_master = read("en/master-proceedings-register/index.html"), read("es/registro-maestro-procedimientos/index.html")
    en_clean = read("en/public-authority-unitary-case-reconstruction/index.html")
    es_clean = read("es/reconstruccion-unitaria-autoridades-publicas/index.html")
    js, css = read("assets/proceedings-interconnectivity-map-20260830.js"), read("assets/proceedings-interconnectivity-map-20260830.css")
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
    counsel_gaps = json.loads(read("assets/data/counsel-procurador-gap-register-v1.json"))
    with (ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    ids = [row["Master_ID"].strip() for row in rows]
    by_id = {row["Master_ID"].strip(): row for row in rows}
    public_rows = [row for row in rows if not any(token in row["Public_Treatment"].upper() for token in ("INTERNAL_ONLY", "PRIVATE", "NOT_SITE_AGGREGATED"))]
    require(len(rows) == 103, f"canonical denominator: expected 103, found {len(rows)}")
    require(len(ids) == len(set(ids)), "duplicate canonical Master_ID")
    require(len(public_rows) == 102, f"public denominator: expected 102, found {len(public_rows)}")

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
    require(prism.get("canonical_node_source") == "archive/PROCEEDINGS_MASTER_REGISTER.csv", "Case Prism canonical source changed")
    require(len(lane_ids) == len(lane_set) == 12 and lane_set == expected_lanes, "Case Prism lane denominator changed")
    require(prop_ids == {f"P{i:02d}" for i in range(1, 20)}, "Case Prism proposition denominator must be P01-P19")
    require(audience_ids == expected_audiences, "Case Prism audience denominator changed")
    require(set(prism.get("statuses", {})) == statuses, "relationship vocabulary mismatch")
    require(set(prism.get("treatments", {})) == treatments, "treatment vocabulary mismatch")
    require(referenced_ids <= set(by_id), f"unknown Case Prism IDs: {sorted(referenced_ids - set(by_id))}")
    require("GC-APP-007" not in referenced_ids, "synthetic removal-family object exposed as a third exact proceeding")
    require({"GC-APP-004", "GC-APP-005", "GC-APP-006", "GC-APP-028"} <= referenced_ids, "exact appellate IDs missing")

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
    require(len(cells) == len(lanes) * len(props) == 228, f"expected 228 coordinates, found {len(cells)}")
    require(set(relation_counts) == statuses, "every relationship status must be used")
    require(treatment_counts["CONTRADICTED"] >= 1, "adverse/contrary treatment not represented")
    coverage = prism.get("coverage", {})
    require(coverage.get("explicit_coordinate_count") == 228 and coverage.get("unexplained_coordinate_count") == 0, "coverage denominator mismatch")
    require(coverage.get("counsel_procurador_denominator") == "GAP", "counsel/procurador incompleteness not explicit")
    for source_id, source in source_catalog.items():
        for language in ("en", "es"):
            href = source.get(f"href_{language}", "")
            require(href and (ROOT / href / "index.html").is_file(), f"{source_id} {language} route unresolved: {href}")

    required_views = {"CONVERGENCE_CLUSTER", "FRAGMENTATION_AUDIT", "DECISION_DEPENDENCY_MATRIX", "PARALLEL_PROCEEDINGS_LANES", "ISOLATION_TEST", "AUDIENCE_LENS"}
    require(schema.get("schema_version") == "1.4.0", "interconnectivity schema must be 1.4.0")
    require(schema.get("canonical_node_source") == "archive/PROCEEDINGS_MASTER_REGISTER.csv", "schema canonical source changed")
    require(required_views <= set(schema.get("required_views", [])), "schema required views missing")
    require(required_views <= set(schema.get("implemented_public_views", {})), "schema runtime mappings missing")
    require(set(schema.get("case_prism_cell_statuses", [])) == statuses, "schema relationship vocabulary mismatch")
    require(schema.get("implementation_contract", {}).get("bilingual_evidence_status_catalog_required") is True, "schema bilingual evidence-status requirement missing")
    require(schema.get("implementation_contract", {}).get("independent_case_prism_generation_seed_required") is True, "schema independent generation-seed requirement missing")

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
    }
    for token, label in renderer_tokens.items():
        require(token in js, f"renderer missing {label}")
    require("pdim-prism-dash" not in js, "renderer can emit unexplained dashes")
    require("data-isolation-lane" not in js, "aggregate-lane isolation remains")
    require("toUpperCase() === 'TRUE'" in js, "exact isolation admits unverified objects")
    require('role="tabpanel" aria-live=' not in js and 'data-proceedings-map="20260830" aria-live=' not in en + es, "nested broad live regions remain")
    require(all(token in css for token in (".pdim-swimlane", ".pdim-isolation-map", ".pdim-dependency-grid", ":focus-visible", "prefers-reduced-motion")), "Prism CSS/accessibility contract incomplete")
    require("json.loads(SEED.read_text" in builder and "json.loads(TARGET.read_text" not in builder, "Case Prism builder is not independent of its generated target")
    require("archive/PROCEEDINGS_CASE_PRISM_V1_SEED_30AUG2026.json" in builder, "Case Prism builder seed path missing")
    require(all(field not in js for field in ("Primary_Source_Anchor", "Repo_Canonical_Source", "Notes")), "renderer exposes non-public raw source fields")

    for page, label in [(en, "EN map"), (es, "ES map"), (en_master, "EN Master"), (es_master, "ES Master")]:
        require("public-authority-unitary-case-reconstruction" in page or "reconstruccion-unitaria-autoridades-publicas" in page, f"{label} lacks clean-room route")
    require("proceedings-map" in en_clean and "master-proceedings-register" in en_clean, "EN clean room lacks map/register links")
    require("mapa-procedimientos" in es_clean and "registro-maestro-procedimientos" in es_clean, "ES clean room lacks map/register links")
    require("#case-prism" in en and "#case-prism" in es, "Case Prism CTA fragment missing")
    require(all(f'id="{anchor}"' in en and f'id="{anchor}"' in es for anchor in ("parallel-lanes", "isolation-test")), "deep-link anchors missing")
    require(all(f"proceedings-interconnectivity-map-20260830.{ext}?v=20260830d" in en and f"proceedings-interconnectivity-map-20260830.{ext}?v=20260830d" in es for ext in ("js", "css")), "Case Prism asset cache version not advanced")

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
        "assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json",
        "scripts/build_proceedings_case_prism_v2.py", "assets/data/counsel-procurador-gap-register-v1.json",
    ]:
        require(path in workflow, f"workflow filter missing dependency: {path}")

if errors:
    print("PROCEEDINGS INTERCONNECTIVITY MAP AUDIT: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("PROCEEDINGS INTERCONNECTIVITY MAP AUDIT: PASS")
print("- canonical denominator: 103 rows / 102 controlled public rows")
print("- overlays consolidated and parent graph acyclic")
print("- Case Prism: 19 propositions x 12 lanes = 228 explicit coordinates / 0 unexplained")
print("- relationship and file-treatment axes independently validated")
print("- source, contrary record, decision dependency and finite actionability validated")
print("- exact-file isolation, full-corpus restore and stable parallel lanes validated")
print("- nine audience lenses and bilingual source routes validated")
print("- counsel/procurador denominator remains an explicit GAP")

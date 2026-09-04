#!/usr/bin/env python3
"""Validation core for the Por Derecho Uría search/graph LegalTech release."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data"


def run() -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    metrics: dict[str, int] = {}

    def fail(message: str) -> None:
        errors.append(message)

    def load(path: str | Path) -> Any:
        target = path if isinstance(path, Path) and path.is_absolute() else ROOT / path
        try:
            return json.loads(target.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(f"{target.relative_to(ROOT)}: invalid JSON: {exc}")
            return {}

    def read(path: str) -> str:
        try:
            return (ROOT / path).read_text(encoding="utf-8")
        except OSError as exc:
            fail(f"{path}: cannot read: {exc}")
            return ""

    root = load("assets/data/matter-identity-registry-v1.json")
    records: list[dict[str, Any]] = []
    actual_counts = {kind: 0 for kind in ("PERSON", "ORGANISATION", "STRUCTURE", "INSTITUTION", "PROCEEDING")}
    for part in root.get("parts", []):
        path = DATA / str(part.get("path", ""))
        if not path.is_file():
            fail(f"missing registry shard {path.relative_to(ROOT)}")
            continue
        shard = load(path)
        rows = shard.get("records", [])
        if shard.get("type") != part.get("type"):
            fail(f"{path.relative_to(ROOT)}: shard type mismatch")
        if len(rows) != part.get("count"):
            fail(f"{path.relative_to(ROOT)}: count {len(rows)} != declared {part.get('count')}")
        records.extend(rows)
        actual_counts[str(part.get("type"))] = actual_counts.get(str(part.get("type")), 0) + len(rows)

    ids: dict[str, dict[str, Any]] = {}
    names: dict[str, str] = {}
    for record in records:
        record_id = str(record.get("id", ""))
        if not re.fullmatch(r"PD-SP-[POSIR]-\d{4}", record_id):
            fail(f"invalid canonical ID {record_id!r}")
        if record_id in ids:
            fail(f"duplicate canonical ID {record_id}")
        ids[record_id] = record
        name = str(record.get("name", "")).strip()
        key = re.sub(r"\W+", "", name.casefold())
        if not name:
            fail(f"{record_id}: missing name")
        if key in names and names[key] != record_id:
            fail(f"probable duplicate canonical name {name!r}: {names[key]}, {record_id}")
        names[key] = record_id

    declared = root.get("counts", {})
    if declared.get("total") != len(records):
        fail(f"root total {declared.get('total')} != actual {len(records)}")
    for kind, count in actual_counts.items():
        if declared.get(kind) != count:
            fail(f"root {kind} {declared.get(kind)} != actual {count}")

    required = {
        "PD-SP-P-0163": "Javier Rubio Sanz", "PD-SP-P-0164": "Javier González Guimaraes-Da Silva",
        "PD-SP-P-0165": "Raimon Tagliavini Sansa", "PD-SP-P-0166": "David García Martín",
        "PD-SP-P-0167": "Juan Francisco Falcón", "PD-SP-P-0168": "Juan Miguel Hernández Herrera",
        "PD-SP-P-0169": "Ángel Alonso Hernández", "PD-SP-P-0170": "Aitor Cohrs",
        "PD-SP-P-0171": "Ana María Tabada Pinzón", "PD-SP-P-0172": "César Guadalupe Plaza",
        "PD-SP-O-0084": "URÍA MENÉNDEZ ABOGADOS, S.L.P.", "PD-SP-O-0085": "Haya Real Estate",
        "PD-SP-O-0086": "Cerberus Capital Management, L.P.", "PD-SP-O-0087": "Banco Financiero y de Ahorros, S.A.",
    }
    for record_id, expected_name in required.items():
        record = ids.get(record_id)
        if not record:
            fail(f"missing required canonical object {record_id} {expected_name}")
            continue
        if record.get("name") != expected_name:
            fail(f"{record_id}: expected {expected_name!r}, got {record.get('name')!r}")
        for field in ("identity_sources", "capacity_boundary"):
            if not record.get(field):
                fail(f"{record_id}: missing {field}")
        routes = record.get("routes", {})
        if not routes.get("es") or not routes.get("en"):
            fail(f"{record_id}: bilingual routes required")

    graph = load("data/legaltech/uria-bankia-caixabank-unitary-graph-20260904.json")
    graph_nodes = {node.get("id"): node for node in graph.get("nodes", [])}
    for node_id, node in graph_nodes.items():
        canonical_id = node.get("canonical_id")
        if canonical_id and canonical_id not in ids:
            fail(f"graph node {node_id}: unknown canonical ID {canonical_id}")
        if not node.get("route_es") or not node.get("route_en"):
            fail(f"graph node {node_id}: bilingual routes required")
    for event in graph.get("events", []):
        if not all(event.get(field) for field in ("id", "date", "label", "status", "proposition")):
            fail(f"graph event missing required field: {event}")
        for node_id in event.get("nodes", []):
            if node_id not in graph_nodes:
                fail(f"event {event.get('id')}: unknown node {node_id}")
    for edge in graph.get("edges", []):
        if edge.get("from") not in graph_nodes or edge.get("to") not in graph_nodes:
            fail(f"edge has unknown node: {edge}")
        if not edge.get("type") or not edge.get("status"):
            fail(f"edge lacks type/status: {edge}")

    required_events = {
        "e-2015-04-09-28", "e-2015-04-30", "e-2015-07-03", "e-2017-05-15",
        "e-2019-2020-falcon", "e-2020-11-11", "e-2021-07-20", "e-2021-07-21",
        "e-2024-01-29", "e-2026-07-09", "e-2026-08-27", "e-2027-01-28",
    }
    present_events = {event.get("id") for event in graph.get("events", [])}
    for event_id in sorted(required_events - present_events):
        fail(f"missing required graph event {event_id}")

    review = load("data/canonical-discovery/review-candidates-20260904.json")
    seen_candidates: set[str] = set()
    for candidate in review.get("candidates", []):
        candidate_id = str(candidate.get("candidate_id", ""))
        if not re.fullmatch(r"PD-MAYBE-\d{4}", candidate_id):
            fail(f"invalid candidate ID {candidate_id!r}")
        if candidate_id in seen_candidates:
            fail(f"duplicate candidate ID {candidate_id}")
        seen_candidates.add(candidate_id)
        for field in ("name", "why_found", "why_not_canonical_yet", "suggested_action", "source_refs"):
            if not candidate.get(field):
                fail(f"{candidate_id}: missing {field}")

    selection = load("data/canonical-discovery/library-evidence-selection-20260904.json")
    if "Recursive Google Drive" not in str(selection.get("scope_note", "")):
        fail("Library selection must disclose recursive Google Drive limitation")
    selection_ids: set[str] = set()
    classes = set(selection.get("publication_classes", {}))
    for record in selection.get("priority_records", []):
        record_id = str(record.get("record_id", ""))
        if record_id in selection_ids:
            fail(f"duplicate selection ID {record_id}")
        selection_ids.add(record_id)
        if record.get("class") not in classes:
            fail(f"{record_id}: invalid selection class {record.get('class')}")

    matrix = load("data/legaltech/notice-continued-conduct-matrix-20260904.json")
    matrix_fields = {
        "row_id", "actor", "capacity", "first_documented_notice", "information_available",
        "subsequent_conduct", "claimant_position", "outcome_or_benefit",
        "innocent_or_lawful_explanation", "missing_evidence", "possible_issues_if_proved", "status",
    }
    for row in matrix.get("rows", []):
        missing = matrix_fields - set(row)
        if missing:
            fail(f"matrix {row.get('row_id')}: missing {sorted(missing)}")

    email_package = load("data/canonical-discovery/email-candidates-20260904.json")
    if email_package.get("privacy_state") != "PUBLIC_SAFE_SANITISED_PROPOSITIONS_ONLY":
        fail("email candidate package lacks sanitised privacy state")

    public_safe_paths = [
        "data/canonical-discovery/review-candidates-20260904.json",
        "data/canonical-discovery/email-candidates-20260904.json",
        "data/canonical-discovery/library-evidence-selection-20260904.json",
        "data/legaltech/notice-continued-conduct-matrix-20260904.json",
        "data/legaltech/uria-bankia-caixabank-unitary-graph-20260904.json",
    ]
    privacy_patterns = {
        "email address": re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I),
        "plus-prefixed phone": re.compile(r"(?<!\w)\+\d[\d .()/-]{8,}\d(?!\w)"),
        "contiguous phone/account-like number": re.compile(r"(?<![\w-])\d{9,15}(?![\w-])"),
        "provider-style 16-hex ID": re.compile(r"\b[0-9a-f]{16}\b", re.I),
        "UUID": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    }
    for path in public_safe_paths:
        payload = read(path)
        for label, pattern in privacy_patterns.items():
            if pattern.search(payload):
                fail(f"{path}: prohibited {label}")

    required_files = [
        "assets/canonical-knowledge-search-20260904.js",
        "assets/legaltech-uria-unitary-gap-closure-20260904.js",
        "assets/legaltech-review-and-matrix-20260904.js",
        "assets/ricpe-2020-representation-evidentiary-correction-20260904.js",
        "scripts/build_canonical_discovery_candidates.py",
        ".github/governance/CANONICAL_DISCOVERY_EMAIL_LIBRARY_AND_INTERCONNECTIVITY_PROTOCOL_04SEP2026.md",
        "evidence/uria-ricpe-sun-park/manifest-legaltech-supplement-20260904.json",
        "en/canonical-review/index.html", "es/revision-canonica/index.html",
        "en/notice-continued-conduct-matrix/index.html", "es/matriz-aviso-conducta-continuada/index.html",
        "en/evidence-intake-selection/index.html", "es/seleccion-ingesta-evidencia/index.html",
        "evidence/ricpe-cnmv/2026-08-27/RICPE_Canal_Etico_Certificado_Resolucion_27AGO2026_PUBLICO_REDACTADO.pdf",
        "evidence/ricpe-cnmv/2026-08-27/resolution.txt",
        *[f"evidence/ricpe-cnmv/2026-08-27/resolution-pages-public-redacted/page-{page}.jpg" for page in range(1, 7)],
    ]
    for path in required_files:
        if not (ROOT / path).is_file():
            fail(f"missing required file {path}")

    site = read("assets/site.js")
    for loader in (
        "canonical-knowledge-search-20260904.js", "legaltech-uria-unitary-gap-closure-20260904.js",
        "legaltech-review-and-matrix-20260904.js", "ricpe-2020-representation-evidentiary-correction-20260904.js",
    ):
        if loader not in site:
            fail(f"site loader missing {loader}")

    unitary = read("assets/legaltech-uria-unitary-gap-closure-20260904.js")
    for marker in (
        "e-2017-05-15", "e-2024-01-29", "e-2026-08-27", "Juan Francisco Falcón",
        "Raimon Tagliavini Sansa", "David García Martín", "CaixaBank sought",
        "CaixaBank solicitó", "without opening an internal investigation", "sin abrir investigación interna",
    ):
        if marker not in unitary:
            fail(f"unitary layer missing marker {marker}")

    correction = read("assets/ricpe-2020-representation-evidentiary-correction-20260904.js")
    for marker in ("Por Derecho sostiene que", "Por Derecho alleges that", "not a judicial finding", "no es una conclusión judicial"):
        if marker not in correction:
            fail(f"RICPE evidentiary correction missing marker {marker}")

    search = read("assets/canonical-knowledge-search-20260904.js")
    for marker in ("editDistance", "trigrams", "review-candidates-20260904.json", "matter-identity-registry-v1.json"):
        if marker not in search:
            fail(f"search layer missing marker {marker}")

    metrics.update(
        canonical_objects=len(records), graph_nodes=len(graph_nodes), events=len(graph.get("events", [])),
        review_candidates=len(review.get("candidates", [])), evidence_selections=len(selection.get("priority_records", [])),
        matrix_rows=len(matrix.get("rows", [])),
    )
    return errors, metrics

#!/usr/bin/env python3
"""Validate the Uría/Bankia/CaixaBank LegalTech search, graph and intake release."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data"
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def load(path: str | Path) -> Any:
    target = ROOT / path if not isinstance(path, Path) or not path.is_absolute() else path
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except Exception as exc:  # validator must report all structural failures together
        fail(f"{target.relative_to(ROOT)}: cannot parse JSON: {exc}")
        return {}


def require_path(path: str) -> None:
    if not (ROOT / path).is_file():
        fail(f"missing required file: {path}")


def text(path: str) -> str:
    try:
        return (ROOT / path).read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read {path}: {exc}")
        return ""


def main() -> int:
    root = load("assets/data/matter-identity-registry-v1.json")
    parts = root.get("parts", []) if isinstance(root, dict) else []
    records: list[dict[str, Any]] = []
    part_counts: dict[str, int] = {}
    for part in parts:
        path = DATA / str(part.get("path", ""))
        if not path.is_file():
            fail(f"registry part missing: {path.relative_to(ROOT)}")
            continue
        shard = load(path)
        shard_records = shard.get("records", []) if isinstance(shard, dict) else []
        declared = int(part.get("count", -1))
        if declared != len(shard_records):
            fail(f"{path.relative_to(ROOT)}: declared count {declared}, actual {len(shard_records)}")
        if shard.get("type") != part.get("type"):
            fail(f"{path.relative_to(ROOT)}: type mismatch {shard.get('type')} != {part.get('type')}")
        records.extend(shard_records)
        part_counts[str(part.get("type"))] = part_counts.get(str(part.get("type")), 0) + len(shard_records)

    ids: dict[str, dict[str, Any]] = {}
    normalized_names: dict[str, str] = {}
    for record in records:
        record_id = str(record.get("id", ""))
        if not re.fullmatch(r"PD-SP-[POSIR]-\d{4}", record_id):
            fail(f"invalid canonical id: {record_id!r}")
        if record_id in ids:
            fail(f"duplicate canonical id: {record_id}")
        ids[record_id] = record
        name = str(record.get("name", "")).strip()
        if not name:
            fail(f"{record_id}: missing name")
        key = re.sub(r"\W+", "", name.casefold())
        prior = normalized_names.get(key)
        if prior and prior != record_id:
            fail(f"probable duplicate canonical name: {name!r} ({prior}, {record_id})")
        normalized_names[key] = record_id

    declared_counts = root.get("counts", {}) if isinstance(root, dict) else {}
    if int(declared_counts.get("total", -1)) != len(records):
        fail(f"root total count {declared_counts.get('total')} != actual {len(records)}")
    for kind in ("PERSON", "ORGANISATION", "STRUCTURE", "INSTITUTION", "PROCEEDING"):
        if int(declared_counts.get(kind, -1)) != part_counts.get(kind, 0):
            fail(f"root {kind} count {declared_counts.get(kind)} != actual {part_counts.get(kind, 0)}")

    required = {
        "PD-SP-P-0163": "Javier Rubio Sanz",
        "PD-SP-P-0164": "Javier González Guimaraes-Da Silva",
        "PD-SP-P-0165": "Raimon Tagliavini Sansa",
        "PD-SP-P-0166": "David García Martín",
        "PD-SP-P-0167": "Juan Francisco Falcón",
        "PD-SP-P-0168": "Juan Miguel Hernández Herrera",
        "PD-SP-P-0169": "Ángel Alonso Hernández",
        "PD-SP-P-0170": "Aitor Cohrs",
        "PD-SP-P-0171": "Ana María Tabada Pinzón",
        "PD-SP-P-0172": "César Guadalupe Plaza",
        "PD-SP-O-0084": "URÍA MENÉNDEZ ABOGADOS, S.L.P.",
        "PD-SP-O-0085": "Haya Real Estate",
        "PD-SP-O-0086": "Cerberus Capital Management, L.P.",
        "PD-SP-O-0087": "Banco Financiero y de Ahorros, S.A.",
    }
    for record_id, name in required.items():
        record = ids.get(record_id)
        if not record:
            fail(f"missing required identity {record_id} {name}")
        elif record.get("name") != name:
            fail(f"{record_id}: expected {name!r}, got {record.get('name')!r}")
        else:
            routes = record.get("routes", {})
            if not routes.get("es") or not routes.get("en"):
                fail(f"{record_id}: bilingual route required")
            if not record.get("capacity_boundary"):
                fail(f"{record_id}: capacity boundary required")
            if not record.get("identity_sources"):
                fail(f"{record_id}: identity sources required")

    graph = load("data/legaltech/uria-bankia-caixabank-unitary-graph-20260904.json")
    graph_nodes = {node.get("id"): node for node in graph.get("nodes", [])}
    for node in graph.get("nodes", []):
        canonical_id = node.get("canonical_id")
        if canonical_id and canonical_id not in ids:
            fail(f"graph node {node.get('id')}: unresolved canonical_id {canonical_id}")
        if not node.get("route_es") or not node.get("route_en"):
            fail(f"graph node {node.get('id')}: bilingual routes required")
    for event in graph.get("events", []):
        if not event.get("date") or not event.get("status") or not event.get("proposition"):
            fail(f"graph event {event.get('id')}: date/status/proposition required")
        for node_id in event.get("nodes", []):
            if node_id not in graph_nodes:
                fail(f"graph event {event.get('id')}: missing node {node_id}")
    for edge in graph.get("edges", []):
        for key in ("from", "to"):
            if edge.get(key) not in graph_nodes:
                fail(f"graph edge {edge}: missing {key} node")
        if not edge.get("type") or not edge.get("status"):
            fail(f"graph edge {edge}: typed status required")

    event_ids = {event.get("id") for event in graph.get("events", [])}
    for required_event in {
        "e-2015-04-09-28", "e-2015-04-30", "e-2015-07-03", "e-2017-05-15",
        "e-2019-2020-falcon", "e-2020-11-11", "e-2021-07-20", "e-2024-01-29",
        "e-2026-07-09", "e-2026-08-27", "e-2027-01-28",
    }:
        if required_event not in event_ids:
            fail(f"graph missing required event {required_event}")

    review = load("data/canonical-discovery/review-candidates-20260904.json")
    candidate_ids: set[str] = set()
    for candidate in review.get("candidates", []):
        candidate_id = str(candidate.get("candidate_id", ""))
        if not re.fullmatch(r"PD-MAYBE-\d{4}", candidate_id):
            fail(f"invalid review candidate id {candidate_id!r}")
        if candidate_id in candidate_ids:
            fail(f"duplicate review candidate id {candidate_id}")
        candidate_ids.add(candidate_id)
        for field in ("name", "why_found", "why_not_canonical_yet", "suggested_action"):
            if not candidate.get(field):
                fail(f"{candidate_id}: missing {field}")

    selection = load("data/canonical-discovery/library-evidence-selection-20260904.json")
    if "Recursive Google Drive" not in str(selection.get("scope_note", "")):
        fail("Library selection must disclose recursive Google Drive limitation")
    selection_ids: set[str] = set()
    for record in selection.get("priority_records", []):
        record_id = str(record.get("record_id", ""))
        if record_id in selection_ids:
            fail(f"duplicate evidence selection id {record_id}")
        selection_ids.add(record_id)
        if record.get("class") not in selection.get("publication_classes", {}):
            fail(f"{record_id}: unknown publication class {record.get('class')}")

    matrix = load("data/legaltech/notice-continued-conduct-matrix-20260904.json")
    required_matrix_fields = {
        "row_id", "actor", "capacity", "first_documented_notice", "information_available",
        "subsequent_conduct", "claimant_position", "outcome_or_benefit",
        "innocent_or_lawful_explanation", "missing_evidence", "possible_issues_if_proved", "status",
    }
    for row in matrix.get("rows", []):
        missing = sorted(required_matrix_fields - set(row))
        if missing:
            fail(f"matrix row {row.get('row_id')}: missing {missing}")
        if not row.get("innocent_or_lawful_explanation"):
            fail(f"matrix row {row.get('row_id')}: lawful/innocent explanation required")

    email_package = load("data/canonical-discovery/email-candidates-20260904.json")
    public_safe_paths = [
        "data/canonical-discovery/review-candidates-20260904.json",
        "data/canonical-discovery/email-candidates-20260904.json",
        "data/canonical-discovery/library-evidence-selection-20260904.json",
        "data/legaltech/notice-continued-conduct-matrix-20260904.json",
        "data/legaltech/uria-bankia-caixabank-unitary-graph-20260904.json",
    ]
    privacy_patterns = {
        "email address": re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I),
        "phone-like number": re.compile(r"(?<!\w)(?:\+?\d[\d .()/-]{7,}\d)(?!\w)"),
        "Gmail provider id": re.compile(r"\b[0-9a-f]{16}\b", re.I),
        "UUID": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    }
    for path in public_safe_paths:
        payload = text(path)
        for label, pattern in privacy_patterns.items():
            if pattern.search(payload):
                fail(f"{path}: contains prohibited {label}")
    if email_package.get("privacy_state") != "PUBLIC_SAFE_SANITISED_PROPOSITIONS_ONLY":
        fail("email discovery package must declare public-safe sanitised state")

    required_files = [
        "assets/canonical-knowledge-search-20260904.js",
        "assets/legaltech-uria-unitary-gap-closure-20260904.js",
        "assets/legaltech-review-and-matrix-20260904.js",
        "scripts/build_canonical_discovery_candidates.py",
        ".github/governance/CANONICAL_DISCOVERY_EMAIL_LIBRARY_AND_INTERCONNECTIVITY_PROTOCOL_04SEP2026.md",
        "en/canonical-review/index.html", "es/revision-canonica/index.html",
        "en/notice-continued-conduct-matrix/index.html", "es/matriz-aviso-conducta-continuada/index.html",
        "en/evidence-intake-selection/index.html", "es/seleccion-ingesta-evidencia/index.html",
        "evidence/ricpe-cnmv/2026-08-27/RICPE_Canal_Etico_Certificado_Resolucion_27AGO2026_PUBLICO_REDACTADO.pdf",
        "evidence/ricpe-cnmv/2026-08-27/resolution.txt",
    ]
    required_files.extend(
        f"evidence/ricpe-cnmv/2026-08-27/resolution-pages-public-redacted/page-{page}.jpg"
        for page in range(1, 7)
    )
    for path in required_files:
        require_path(path)

    site = text("assets/site.js")
    for loader in (
        "canonical-knowledge-search-20260904.js",
        "legaltech-uria-unitary-gap-closure-20260904.js",
        "legaltech-review-and-matrix-20260904.js",
    ):
        if loader not in site:
            fail(f"assets/site.js does not load {loader}")

    unitary = text("assets/legaltech-uria-unitary-gap-closure-20260904.js")
    for marker in (
        "e-2017-05-15", "e-2024-01-29", "e-2026-08-27", "Juan Francisco Falcón",
        "Raimon Tagliavini Sansa", "David García Martín", "CaixaBank sought",
        "CaixaBank solicitó", "without opening an internal investigation",
        "sin abrir investigación interna",
    ):
        if marker not in unitary:
            fail(f"unitary public layer missing marker: {marker}")

    search = text("assets/canonical-knowledge-search-20260904.js")
    for marker in ("editDistance", "trigrams", "review-candidates-20260904.json", "matter-identity-registry-v1.json"):
        if marker not in search:
            fail(f"search enhancement missing marker: {marker}")

    if ERRORS:
        print("LEGALTECH URÍA SEARCH/GRAPH GATE: FAIL")
        for error in ERRORS:
            print(f" - {error}")
        return 1

    print(
        "LEGALTECH URÍA SEARCH/GRAPH GATE: PASS "
        f"({len(records)} canonical objects; {len(graph_nodes)} graph nodes; "
        f"{len(graph.get('events', []))} events; {len(review.get('candidates', []))} review candidates; "
        f"{len(selection.get('priority_records', []))} evidence selections; {len(matrix.get('rows', []))} matrix rows)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

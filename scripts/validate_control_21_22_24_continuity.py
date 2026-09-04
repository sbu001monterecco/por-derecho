#!/usr/bin/env python3
"""Fail-closed validator for PD-C212224-001 continuity governance."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/control-21-22-24-continuity-v1.json"
PROTOCOL = ROOT / ".github/governance/CONTROL_21_22_24_CONTINUITY_INTERLINK_PROTOCOL_04SEP2026.md"
HANDOFF_MD = ROOT / "archive/handoffs/2026-09-04-control-21-22-24-continuity-handoff.md"
HANDOFF_JSON = ROOT / "archive/handoffs/2026-09-04-control-21-22-24-continuity-handoff.json"
CORRECTION = ROOT / "archive/GC_HC_010_DECANATO24_CGPJ169_CORRECTION_04SEP2026.md"
EN_CONTROL24 = ROOT / "en/proceedings/gc-hc-010/index.html"
ES_CONTROL24 = ROOT / "es/procedimientos/gc-hc-010/index.html"

REQUIRED_NODE_IDS = {
    "CONCURSO-36-2012",
    "CONTROL-21",
    "CONTROL-22",
    "CONTROL-24",
    "GC-CRI-008",
    "GC-CRI-009",
    "GC-REF-029",
    "GC-HC-010",
    "CONTROL-24-AMPLIACION-20260625",
    "CONTROL-21-OBJECT-20260625",
    "GC-GOV-019",
    "ALZADA-286-2026",
    "GC-FIS-017",
}

REQUIRED_ALIASES = {
    "Control 21",
    "Control 22",
    "Control 24",
    "Reg. No. 24",
    "Registro n.º 24",
    "DP 1901/2026",
    "DP 1956/2026",
    "GC-CRI-008",
    "GC-CRI-009",
    "GC-REF-029",
    "GC-HC-010",
    "DI 169/2026",
    "CGPJ 169/2026",
    "Alzada 286/2026",
    "DIP 2/2026",
    "TSJ Canarias",
    "TSJC",
    "18 June 2026",
    "25 June 2026",
    "Concurso 36/2012",
}

CRITICAL_EDGES = {
    ("CONTROL-21", "GC-CRI-008", "UNVERIFIED_CANDIDATE_BRIDGE"),
    ("CONTROL-22", "GC-REF-029", "PROVEN_DOCUMENTARY_BRIDGE"),
    ("CONTROL-22", "GC-CRI-009", "UNVERIFIED_CANDIDATE_BRIDGE"),
    ("CONTROL-24", "GC-HC-010", "PROVEN_DOCUMENTARY_BRIDGE"),
    ("CONTROL-24", "CONTROL-24-AMPLIACION-20260625", "PROVEN_SAME_RECORD_DEPENDENT_SUPPLEMENT"),
    ("CONTROL-24", "GC-GOV-019", "RELATED_SEPARATE_ROUTE"),
    ("CONTROL-24", "GC-FIS-017", "RELATED_SEPARATE_ROUTE"),
    ("CONTROL-21-OBJECT-20260625", "CONTROL-24-AMPLIACION-20260625", "NO_BRIDGE"),
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path):
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def require_phrases(path: Path, phrases: tuple[str, ...]) -> None:
    if not path.is_file():
        fail(f"missing required continuity/public file: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        if phrase not in text:
            fail(f"required phrase missing from {path.relative_to(ROOT)}: {phrase}")


def main() -> None:
    for required in (PROTOCOL, HANDOFF_MD, HANDOFF_JSON, CORRECTION, EN_CONTROL24, ES_CONTROL24):
        if not required.is_file():
            fail(f"missing required continuity file: {required.relative_to(ROOT)}")

    data = load_json(DATA)
    handoff = load_json(HANDOFF_JSON)

    if data.get("control_id") != "PD-C212224-001":
        fail("unexpected control_id")
    if data.get("canonical_nucleus", {}).get("id") != "CONCURSO-36-2012":
        fail("Concurso 36/2012 canonical nucleus is missing")

    controls = {item.get("id"): item for item in data.get("controls", [])}
    if set(controls) != {"CONTROL-21", "CONTROL-22", "CONTROL-24"}:
        fail("exact Control 21/22/24 control set not preserved")

    c21 = controls["CONTROL-21"]
    if c21.get("bridge_status") != "UNVERIFIED_CANDIDATE_BRIDGE":
        fail("Control 21 -> DP 1901 bridge must remain unverified until source-certified")
    if c21.get("evidential_state") != "ATTRIBUTED_ALLEGATION":
        fail("Control 21 current intake/date claim must remain attributed, not promoted to documented fact")

    c22 = controls["CONTROL-22"]
    if c22.get("bridge_status") != "UNVERIFIED_CANDIDATE_BRIDGE":
        fail("Control 22 -> DP 1956 bridge must remain unverified until source-certified")
    if c22.get("canonical_repository_object") != "GC-REF-029":
        fail("Control 22 must retain GC-REF-029 as its canonical intake object")

    c24 = controls["CONTROL-24"]
    if c24.get("formal_destination_status") != "UNKNOWN":
        fail("Control 24 formal destination must remain UNKNOWN absent documentary bridge")
    if c24.get("canonical_repository_object") != "GC-HC-010":
        fail("Control 24 must retain GC-HC-010 as its canonical control record")
    if c24.get("judge_amplification_date") != "2026-06-25":
        fail("Control 24 judge-related supplement date must remain explicit")
    if c24.get("supplement_status") != "DEPENDENT_SAME_RECORD":
        fail("25 June Control 24 supplement must remain dependent within the same Reg. No. 24 record")
    if "one Reg. No. 24" not in c24.get("canonical_identity_rule", ""):
        fail("Control 24 canonical identity rule must explicitly preserve one Reg. No. 24 record")
    presumed = c24.get("expected_or_presumed_route", "")
    if "TSJ Canarias / TSJC" not in presumed or "not verified" not in presumed:
        fail("Control 24 must preserve TSJC only as an expected/presumed, unverified route")
    if c24.get("trace_status") != "ACTIVE_TRACE_REQUESTED":
        fail("Control 24 active trace status must remain explicit")
    if set(c24.get("trace_targets", [])) != {
        "Decanato / Registro y Reparto Las Palmas", "TSJ Canarias / TSJC", "CGPJ"
    }:
        fail("Control 24 trace targets must remain Decanato + TSJC + CGPJ")
    trace_rule = c24.get("trace_rule", "")
    for required_phrase in ("fact of filing", "post-intake route remains untraced", "must not be promoted"):
        if required_phrase not in trace_rule:
            fail(f"Control 24 trace rule missing safeguard: {required_phrase}")

    node_map = {item.get("id"): item for item in data.get("nodes", [])}
    nodes = set(node_map)
    missing_nodes = REQUIRED_NODE_IDS - nodes
    if missing_nodes:
        fail(f"missing required graph nodes: {sorted(missing_nodes)}")
    if node_map["CONTROL-24-AMPLIACION-20260625"].get("type") != "DEPENDENT_FILING_EVENT":
        fail("Control 24 supplement must be typed as a dependent filing event, not an autonomous proceeding")

    aliases = set(data.get("aliases", []))
    missing_aliases = REQUIRED_ALIASES - aliases
    if missing_aliases:
        fail(f"missing required search aliases: {sorted(missing_aliases)}")

    edge_keys = set()
    for edge in data.get("edges", []):
        if edge.get("bidirectional") is not True:
            fail(f"edge is not bidirectional: {edge.get('from')} -> {edge.get('to')}")
        if edge.get("from") not in nodes or edge.get("to") not in nodes:
            fail(f"edge references unknown node: {edge}")
        edge_keys.add((edge.get("from"), edge.get("to"), edge.get("bridge_status")))

    missing_edges = CRITICAL_EDGES - edge_keys
    if missing_edges:
        fail(f"missing/altered critical edges: {sorted(missing_edges)}")

    if "CONTROL-21-OBJECT-20260625" == "CONTROL-24-AMPLIACION-20260625":
        fail("25 June Control-21 and Control-24 document objects collapsed")

    public_routes = data.get("public_routes", {})
    for key in (
        "CONTROL-22_EN", "CONTROL-22_ES", "DP-1901_EN", "DP-1901_ES",
        "DP-1956_EN", "DP-1956_ES", "CONTROL-24_EN", "CONTROL-24_ES",
        "CONTROL-24-DOSSIER_EN", "CONTROL-24-DOSSIER_ES",
    ):
        if not public_routes.get(key):
            fail(f"missing public route alias: {key}")

    if handoff.get("canonical_state") != "assets/data/control-21-22-24-continuity-v1.json":
        fail("handoff does not point to canonical machine state")
    if handoff.get("scope_state") != "RELATED_CONTINUITY_ACTIVE":
        fail("handoff scope state is not continuity-active")

    require_phrases(PROTOCOL, (
        "UNVERIFIED",
        "Two-documents-on-25-June safeguard",
        "one Reg. No. 24 filing record, two dated filing events",
        "separate document object, same Reg. No. 24 procedural record",
        "fact of filing",
        "post-intake route remains untraced",
        "Decanato + TSJC + CGPJ",
        "Interlinking never transfers knowledge, intent, causation, guilt, liability, procedural status or evidential weight",
    ))
    require_phrases(CORRECTION, (
        "18 June 2026",
        "25 June 2026",
        "one continuous filing record",
        "expected or presumed competence route",
        "post-intake route",
        "Decanato / Registro y Reparto",
        "TSJ Canarias / TSJC",
        "CGPJ",
        "169/2026",
    ))
    require_phrases(EN_CONTROL24, (
        "GC-HC-010",
        "18 June 2026",
        "25 June 2026",
        "same Daily Registration No. 24 record",
        "Current status",
        "untraced",
        "Expected / presumed judicial route",
        "Decanato, TSJC and CGPJ",
        "169/2026",
    ))
    require_phrases(ES_CONTROL24, (
        "GC-HC-010",
        "18 de junio de 2026",
        "25 de junio de 2026",
        "mismo Registro diario n.º 24",
        "Estado actual",
        "sin localizarse",
        "Vía judicial esperada / presumida",
        "Decanato, TSJC y CGPJ",
        "169/2026",
    ))

    print("PASS: PD-C212224-001 preserves Reg. No. 24 as one filed-but-untraced record, TSJC only as presumed/unverified route, active Decanato-TSJC-CGPJ tracing, typed cross-links and source-status boundaries")


if __name__ == "__main__":
    main()

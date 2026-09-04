#!/usr/bin/env python3
"""Fail-closed continuity checks for the Concurso 36/2012 Control 21/22/24 graph."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "data/concurso-36-2012-triangle-register-v1.json"
GOV = ROOT / ".github/governance/CONCURSO_36_2012_TRIANGLE_CONTROL_21_22_24_CONTINUITY_PROTOCOL_04SEP2026.md"
VIS = ROOT / "assets/concurso-36-2012-triangle-20260904.js"
SEARCH = ROOT / "assets/concurso-36-2012-triangle-search-20260904.js"
LOADER = ROOT / "assets/site.js"

errors: list[str] = []

for path in (REGISTER, GOV, VIS, SEARCH, LOADER):
    if not path.is_file():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")

if not errors:
    data = json.loads(REGISTER.read_text(encoding="utf-8"))
    node_ids = {n.get("node_id") for n in data.get("nodes", [])}
    required_nodes = {
        "control-21", "nexus-36", "dp-1901-2026", "control-22", "dp-1956-2026",
        "icalpa-dip-80-2026", "ac-removal-fees", "control-24", "gc-hc-010",
        "control-24-supplement-2026-06-25", "cgpj-di-169-2026", "cgpj-alzada-286-2026",
        "dip-2-2026", "judge-querella-lane", "rpl-2523-2025"
    }
    missing = sorted(required_nodes - node_ids)
    if missing:
        errors.append("missing mandatory graph nodes: " + ", ".join(missing))

    vertex_ids = {v.get("vertex_id") for v in data.get("vertices", [])}
    expected_vertices = {"private-actors", "insolvency-administrator", "concurso-judge"}
    if vertex_ids != expected_vertices:
        errors.append(f"triangle vertices changed: {sorted(vertex_ids)}")

    aliases = set(data.get("mandatory_aliases", []))
    required_aliases = {
        "Control 21", "Control 22", "Control 24", "NEXUS 36", "GC-HC-010",
        "DP 1901/2026", "DP 1956/2026", "CGPJ 169/2026", "DI 169/2026",
        "Alzada 286/2026", "DIP 2/2026", "ICALPA 80/2026", "DIP 80/2026",
        "RPL 2523/2025", "Concurso 36/2012"
    }
    if required_aliases - aliases:
        errors.append("mandatory aliases lost: " + ", ".join(sorted(required_aliases - aliases)))

    serial = json.dumps(data, ensure_ascii=False)
    boundary_needles = [
        "Control 22 is not DP 1956/2026",
        "Control 24 is Decanato daily registration no. 24",
        "Fiscalía neutralisation language is attributed allegation/inference",
        "must not be merged with a different 25 June filing"
    ]
    for needle in boundary_needles:
        if needle not in serial:
            errors.append(f"missing evidential boundary: {needle}")

    edges = {(e.get("from"), e.get("to")) for e in data.get("edges", [])}
    required_edges = {
        ("control-21", "dp-1901-2026"), ("control-22", "dp-1956-2026"),
        ("control-22", "icalpa-dip-80-2026"), ("control-22", "ac-removal-fees"),
        ("control-24", "gc-hc-010"), ("control-24-supplement-2026-06-25", "control-24"),
        ("control-24", "cgpj-di-169-2026"), ("cgpj-di-169-2026", "cgpj-alzada-286-2026"),
        ("control-24", "dip-2-2026"), ("control-24", "judge-querella-lane"),
        ("control-21", "control-22"), ("control-22", "control-24"), ("control-24", "control-21"),
        ("concurso-36-2012", "rpl-2523-2025")
    }
    for edge in sorted(required_edges - edges):
        errors.append(f"missing mandatory edge: {edge[0]} -> {edge[1]}")

    vis = VIS.read_text(encoding="utf-8")
    for needle in ("data-concurso36-triangle", "GC-HC-010", "ICALPA 80", "CGPJ 169/286", "DIP 2/2026", "RPL 2523/2025"):
        if needle not in vis:
            errors.append(f"public triangle asset missing marker: {needle}")

    search = SEARCH.read_text(encoding="utf-8")
    for needle in ("control 21", "control 22", "control 24", "gc hc 010", "icalpa 80 2026", "rpl 2523 2025"):
        if needle not in search.lower():
            errors.append(f"search alias missing: {needle}")

    loader = LOADER.read_text(encoding="utf-8")
    for needle in ("concurso-36-2012-triangle-20260904.js", "concurso-36-2012-triangle-search-20260904.js"):
        if needle not in loader:
            errors.append(f"site loader not wired: {needle}")

    gov = GOV.read_text(encoding="utf-8")
    for needle in ("INTERLINK ≠ MERGE", "GC-HC-010", "OFFICIAL_BRIDGE_COPY_REQUIRED", "25 June"):
        if needle not in gov:
            errors.append(f"governance invariant missing: {needle}")

if errors:
    print("Concurso 36 triangle continuity validation: FAIL", file=sys.stderr)
    for err in errors:
        print(f" - {err}", file=sys.stderr)
    raise SystemExit(1)

print("Concurso 36 triangle continuity validation: PASS")

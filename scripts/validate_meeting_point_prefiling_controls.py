#!/usr/bin/env python3
"""Validate mandatory Meeting Point pre-filing protection markers.

Usage:
  python scripts/validate_meeting_point_prefiling_controls.py DOC1.txt DOC2.txt

Inputs should be deterministic text extractions of the exact regenerated PDFs.
This checker is a gate, not a legal merits decision.
"""
from __future__ import annotations
import sys
from pathlib import Path

REQUIRED_DOC1 = {
    "historical_non_adoption": ["no constituye", "reiteración automática"],
    "cexp_extinction_control": ["CEXP", "extinción"],
    "capacity_specific": ["capacidad", "procedimiento"],
    "historic_damages_control": ["cuantificaciones históricas", "no constituyen"],
    "criminal_allegation_control": ["calificaciones penales históricas", "hechos probados"],
    "hava_vida_control": ["Hava Vida", "titularidad registral"],
    "term_sheet_control": ["Hoja de Términos", "exigibilidad"],
    "historical_current_controller": ["posición actual", "Documento 1"],
}

FORBIDDEN_UNQUALIFIED = [
    "la cexp quedó extinguida",
    "la cexp fue disuelta por",
    "todos los propietarios eran miembros de la cexp",
    "la cifra de 89.646.211,25 euros se reclama",
    "la hoja de términos prueba el desembolso",
]

def norm(s: str) -> str:
    return " ".join(s.lower().split())

def main() -> int:
    if len(sys.argv) != 3:
        print("BLOCKED: provide DOC1.txt DOC2.txt")
        return 2
    doc1 = norm(Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace"))
    doc2 = norm(Path(sys.argv[2]).read_text(encoding="utf-8", errors="replace"))
    failures = []
    for gate, needles in REQUIRED_DOC1.items():
        if not all(norm(n) in doc1 for n in needles):
            failures.append(f"{gate}: missing {needles}")
    for phrase in FORBIDDEN_UNQUALIFIED:
        if norm(phrase) in doc1:
            failures.append(f"forbidden unqualified phrase in Document 1: {phrase}")
    if "documento 2" not in doc1 or "históric" not in doc1:
        failures.append("Document 1 does not clearly control Document 2 historical-source status")
    # Document 2 must either contain its own front control or be expressly cross-referenced in DOC1.
    doc2_has_control = ("no constituye" in doc2 and "documento 1" in doc2 and "históric" in doc2)
    if not doc2_has_control:
        print("WARN: Document 2 does not appear to contain its own front non-adoption control; acceptable only if final package design intentionally relies on the prominent Document 1 controller.")
    if failures:
        print("BLOCKED")
        for f in failures:
            print(" -", f)
        return 1
    print("READY_FOR_COUNSEL_OR_OWNER_FINAL_REVIEW")
    print("Machine markers pass. Human page-by-page review and final PDF hashes remain mandatory.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

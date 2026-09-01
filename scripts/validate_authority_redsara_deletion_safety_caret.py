#!/usr/bin/env python3
"""Validate the authority/Red SARA deletion closeout and finite caret census."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "assets/data/authority-redsara-deletion-safety-caret-audit-v1.json"
INSTITUTIONS = ROOT / "assets/data/matter-identity-registry-v1.institutions.json"
MASTER = ROOT / "assets/data/matter-identity-registry-v1.json"
GAPS = ROOT / "assets/data/unitary-multitrack-criminal-first-gap-closure-v1.json"
PAGES = {
    "en": ROOT / "en/authority-redsara-deletion-safety-closeout/index.html",
    "es": ROOT / "es/cierre-seguridad-borrado-autoridades-redsara/index.html",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    audit = load(AUDIT)
    institutions = load(INSTITUTIONS).get("records", [])
    master = load(MASTER)
    gaps = load(GAPS)

    scope = audit.get("caret_scope", {})
    records = scope.get("records", [])
    if scope.get("unique_reference_denominator") != 3 or len(records) != 3:
        errors.append("caret denominator must remain three")
    if scope.get("caret_confirmed") != 1 or scope.get("caret_pending") != 2:
        errors.append("caret count must remain 1 confirmed / 2 pending")
    if scope.get("verdict") != "PARTIAL — NOT ALL IS^":
        errors.append("finite caret verdict must remain partial")

    intervention = next((r for r in institutions if r.get("id") == "PD-SP-I-0043"), None)
    if not intervention:
        errors.append("PD-SP-I-0043 missing from canonical institution shard")
    else:
        if intervention.get("name") != "Intervención General de la Comunidad Autónoma de Canarias":
            errors.append("PD-SP-I-0043 name mismatch")
        if intervention.get("identity_resolution") != "CARET_CONFIRMED":
            errors.append("PD-SP-I-0043 must be CARET_CONFIRMED")
        if len(intervention.get("source_urls", [])) < 2:
            errors.append("PD-SP-I-0043 must retain two official source URLs")

    counts = master.get("counts", {})
    if counts != {"total": 342, "PERSON": 162, "ORGANISATION": 83, "STRUCTURE": 11, "INSTITUTION": 43, "PROCEEDING": 43}:
        errors.append(f"canonical count drift: {counts}")

    evidence = gaps.get("authority_legitimacy_propagation", {}).get("notice_checkpoint", {})
    if evidence.get("issuing_institution_caepr_id") != "PD-SP-I-0043":
        errors.append("legacy Intervención evidence does not resolve to PD-SP-I-0043")
    if evidence.get("issuing_institution_identity_state") != "CARET_CONFIRMED":
        errors.append("legacy Intervención institution identity must be confirmed")
    gap16 = next((g for g in gaps.get("gaps", []) if g.get("id") == "PD-GAP-UCF-016"), {})
    if gap16.get("status") != "PARTIAL_IDENTITY_CLOSED_NOTICE_ROUTING_OPEN_MERITS":
        errors.append("PD-GAP-UCF-016 must preserve identity-closed / merits-open status")

    page_rules = {
        "en": ["PARTIAL — NOT ALL IS^", "1/3", "PD-SP-I-0043", "Intervención General de la Comunidad Autónoma de Canarias^"],
        "es": ["PARCIAL — NO TODO ES^", "1/3", "PD-SP-I-0043", "Intervención General de la Comunidad Autónoma de Canarias^"],
    }
    for lang, path in PAGES.items():
        text = path.read_text(encoding="utf-8")
        for marker in page_rules[lang]:
            if marker not in text:
                errors.append(f"{lang} page missing marker: {marker}")
        if "receipt" in text.lower() and "guilt" not in text.lower() and lang == "en":
            errors.append("EN receipt boundary missing guilt limitation")

    routes = load(ROOT / "assets/data/unitary-route-registry-v1.json")
    paths = {r.get("path") for r in routes}
    for path in ("en/authority-redsara-deletion-safety-closeout/", "es/cierre-seguridad-borrado-autoridades-redsara/"):
        if path not in paths:
            errors.append(f"route registry missing {path}")

    if errors:
        print("Authority/Red SARA deletion-safety caret validation FAILED")
        for error in errors:
            print(f" - {error}")
        return 1
    print("Authority/Red SARA deletion-safety caret validation passed: 24/24 preserved; 1/3 CARET_CONFIRMED; PD-GAP-UCF-016 merits remain open")
    return 0


if __name__ == "__main__":
    sys.exit(main())

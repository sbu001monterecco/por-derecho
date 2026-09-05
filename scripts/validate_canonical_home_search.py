#!/usr/bin/env python3
"""Validate canonical identity, search quality, entity census and evidence triage."""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from build_entity_census import DATA, ROOT, load_json, load_registry, normalise


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def strings(value: Any) -> list[str]:
    output: list[str] = []
    if value is None:
        return output
    if isinstance(value, (str, int, float)):
        return [str(value)]
    if isinstance(value, list):
        for item in value:
            output.extend(strings(item))
    elif isinstance(value, dict):
        for key, item in value.items():
            if key.lower() not in {"url", "hash", "sha256", "email", "phone"}:
                output.extend(strings(item))
    return output


def search(records: dict[str, dict[str, Any]], query: str) -> list[str]:
    needle = normalise(query)
    terms = needle.split()
    ranked: list[tuple[int, str]] = []
    for identifier, record in records.items():
        exact_values = [record.get("name"), *(record.get("aliases") or []), identifier]
        exact = {normalise(value) for value in exact_values if value}
        haystack = normalise(" | ".join(strings(record)))
        score = 0
        if needle in exact:
            score = 1000
        elif all(term in haystack for term in terms):
            score = 600
            if needle in normalise(record.get("name")):
                score += 200
            if needle in haystack:
                score += 100
        if score:
            ranked.append((score, identifier))
    return [identifier for _, identifier in sorted(ranked, key=lambda row: (-row[0], row[1]))]


def main() -> None:
    records, alias_to_id, index = load_registry()
    require(index.get("registry_id") == "PD-SP-IDENTITY-REGISTRY-001", "Unexpected canonical registry ID")
    require(index.get("control_date") == "2026-09-04", "Canonical registry control date must be 2026-09-04")

    expected_uria = {
        "PD-SP-O-0084": "URÍA MENÉNDEZ ABOGADOS, S.L.P.",
        "PD-SP-P-0166": "Juan Miguel Hernández Herrera",
        "PD-SP-P-0167": "Ángel Alonso Hernández",
        "PD-SP-P-0168": "Javier Rubio Sanz",
        "PD-SP-P-0169": "Juan Francisco Falcón",
        "PD-SP-P-0170": "Raimon Tagliavini Sansa",
        "PD-SP-P-0171": "David García Martín",
    }
    for identifier, name in expected_uria.items():
        require(records.get(identifier, {}).get("name") == name, f"Missing Uría canonical record: {identifier} {name}")
    require(alias_to_id.get(normalise("Uria Menendez")) == "PD-SP-O-0084", "Unaccented Uría alias does not resolve")
    require(alias_to_id.get(normalise("Uría")) == "PD-SP-O-0084", "Short Uría alias does not resolve")
    require(alias_to_id.get(normalise("Uriel Abogados")) != "PD-SP-O-0084", "Uría / Uriel collision")

    smoke_tests = {
        "Uria Menendez": "PD-SP-O-0084",
        "URÍA MENÉNDEZ ABOGADOS": "PD-SP-O-0084",
        "B28563963": "PD-SP-O-0084",
        "Juan Miguel Hernandez Herrera": "PD-SP-P-0166",
        "Angel Alonso Hernandez": "PD-SP-P-0167",
        "Javier Rubio Sanz": "PD-SP-P-0168",
        "Juan Francisco Falcon": "PD-SP-P-0169",
        "Raimon Tagliavini": "PD-SP-P-0170",
        "David Garcia Martin": "PD-SP-P-0171",
        "PD-SP-P-0169": "PD-SP-P-0169",
    }
    for query, expected in smoke_tests.items():
        matches = search(records, query)
        require(expected in matches[:12], f"Search query {query!r} did not return {expected}; got {matches[:12]}")
    require("PD-SP-O-0084" not in search(records, "Uriel Abogados")[:12], "Uriel query returned Uría")

    # Preserve the existing court-hierarchy invariant.
    master_court = records.get("PD-SP-I-0044")
    require(master_court and master_court.get("name") == "Audiencia Provincial de Las Palmas", "Missing master Audiencia identity")
    children = {row.get("institution_id") for row in master_court.get("child_institutions", [])}
    require({"PD-SP-I-0014", "PD-SP-I-0025"} <= children, "Master court lost a controlled child section")

    current = load_json(DATA / "justice-authority-register-current-v2.json")
    derived = current.get("derived_counts", {})
    require(derived.get("unique_named_people", 0) == derived.get("confirmed", 0) + derived.get("pending", 0), "Current authority denominator is internally inconsistent")

    search_path = ROOT / "assets" / "canonical-home-search-20260904.js"
    site_path = ROOT / "assets" / "site.js"
    require(search_path.is_file(), "Missing 20260904 canonical search runtime")
    search_script = search_path.read_text(encoding="utf-8")
    site_script = site_path.read_text(encoding="utf-8")
    for marker in (
        "matter-identity-registry-v1.json", "proceedings-master-public-v1.json",
        "URLSearchParams", "PorDerechoCanonicalSearch", "register", "oneEditApart",
        "section.closest('details')", "data-canonical-home-search', '20260904'"
    ):
        require(marker in search_script, f"Canonical search lacks marker: {marker}")
    require("canonical-home-search-20260904.js" in site_script, "site.js does not pre-load the 20260904 search runtime")
    require("data-canonical-home-search-loader" in site_script, "site.js does not block the inherited stale search loader")

    decisions = load_json(ROOT / "ops" / "legaltech-entity-evidence" / "candidate-decisions.json")
    valid_decisions = {"YES_NOW", "MAYBE_HOLD", "NO_REJECT"}
    candidate_ids = set()
    for row in decisions.get("candidates", []):
        require(row.get("candidate_id") not in candidate_ids, f"Duplicate candidate ID: {row.get('candidate_id')}")
        candidate_ids.add(row.get("candidate_id"))
        require(row.get("decision") in valid_decisions, f"Invalid candidate decision: {row}")
    require(any(row.get("candidate_name") == "Javier González" and row.get("decision") == "MAYBE_HOLD" for row in decisions.get("candidates", [])), "Javier González ambiguity control is missing")
    require(any(row.get("candidate_name") == "Uriel Abogados" and row.get("decision") == "NO_REJECT" for row in decisions.get("candidates", [])), "Uría/Uriel rejection control is missing")

    triage = load_json(ROOT / "ops" / "legaltech-entity-evidence" / "evidence-triage-v1.json")
    allowed_modes = set(triage.get("publication_modes", {}))
    triage_ids = set()
    for row in triage.get("items", []):
        require(row.get("id") not in triage_ids, f"Duplicate evidence-triage ID: {row.get('id')}")
        triage_ids.add(row.get("id"))
        require(row.get("mode") in allowed_modes, f"Unknown evidence mode for {row.get('id')}")
        require(row.get("controls"), f"Evidence item lacks publication controls: {row.get('id')}")
    require(len(triage_ids) >= 25, "Initial Library evidence triage is too small")

    report = Path("/tmp/por-derecho-entity-census.json")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_entity_census.py"), "--check", "--output", str(report)], check=True)
    generated = json.loads(report.read_text(encoding="utf-8"))
    require(generated.get("counts", {}).get("controlled_id_errors") == 0, "Entity census found unknown controlled IDs")

    type_counts = Counter(record["type"] for record in records.values())
    print(f"PASS canonical identity/search/evidence audit: {len(records)} records {dict(type_counts)}; {len(smoke_tests)} Uría search tests; {len(candidate_ids)} review candidates; {len(triage_ids)} Library triage items")


if __name__ == "__main__":
    main()

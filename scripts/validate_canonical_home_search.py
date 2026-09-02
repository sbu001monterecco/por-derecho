#!/usr/bin/env python3
"""Validate the current justice-authority register, court hierarchy and homepage search without frozen denominators."""

from __future__ import annotations

from collections import Counter
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain an object")
    return value


def normalise(value: object) -> str:
    text = unicodedata.normalize("NFD", str(value or ""))
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    text = text.lower().replace("–", "-").replace("—", "-")
    text = re.sub(r"[^a-z0-9^]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def id_variants(identifier: str) -> list[str]:
    match = re.fullmatch(r"PD-SP-([POSIR])-(\d{4})", identifier.upper())
    if not match:
        return [identifier] if identifier else []
    kind, number = match.groups()
    compact = str(int(number))
    return [identifier.upper(), f"{kind}-{number}", f"{kind}{number}", f"^{kind}-{number}", f"^{kind}{number}", f"^{number}", f"^{compact}"]


@dataclass(frozen=True)
class SearchEntry:
    identifier: str
    name: str
    haystack: str
    exact: frozenset[str]


def make_caepr_entry(record: dict) -> SearchEntry:
    aliases: list[object] = []
    for key in ("aliases", "legacy_ambiguous_aliases", "master_register_ids"):
        value = record.get(key)
        if isinstance(value, list): aliases.extend(value)
    for key in ("master_register_id", "nig", "procedural_state", "identity_resolution"):
        if record.get(key): aliases.append(record[key])
    aliases.extend(id_variants(str(record.get("id", ""))))
    name = str(record.get("name") or record.get("id") or "")
    values = [record.get("id"), name, *aliases]
    return SearchEntry(str(record["id"]), name, normalise(" | ".join(str(v) for v in values if v)), frozenset(normalise(v) for v in values if normalise(v)))


def make_master_entry(record: dict) -> SearchEntry:
    values = [record.get("Master_ID"), record.get("Reference"), record.get("Legacy_ID"), record.get("Secondary_Reference"), record.get("NIG"), record.get("Origin_Organ"), record.get("Current_Custodian"), record.get("Stream"), record.get("Geography"), record.get("Parent_Master_ID"), record.get("Linked_Proceedings"), record.get("Appeal_or_Review"), record.get("Object_or_Purpose"), record.get("Connection")]
    name = str(record.get("Reference") or record.get("Object_or_Purpose") or record.get("Master_ID"))
    return SearchEntry(str(record["Master_ID"]), name, normalise(" | ".join(str(v) for v in values if v)), frozenset(normalise(v) for v in values[:12] if normalise(v)))


def score(entry: SearchEntry, raw_query: str) -> int:
    query = normalise(raw_query)
    if not query: return 0
    if query in entry.exact: return 1000
    if normalise(entry.identifier) == query: return 990
    if entry.haystack.startswith(query): return 850
    terms = [term for term in query.split(" ") if term]
    if not all(term in entry.haystack for term in terms): return 0
    value = 500
    if query in normalise(entry.name): value += 220
    if query in normalise(entry.identifier): value += 180
    return value + max(0, 80 - len(entry.name))


def main() -> None:
    index = load_json(DATA / "matter-identity-registry-v1.json")
    require(index.get("registry_id") == "PD-SP-IDENTITY-REGISTRY-001", "Unexpected CAEPR registry ID")
    require(index.get("control_date") == "2026-09-02", "CAEPR index control date was not advanced")

    records: dict[str, dict] = {}
    type_counts = Counter()
    part_total = 0
    for descriptor in index.get("parts", []):
        shard_path = DATA / descriptor["path"]
        require(shard_path.is_file(), f"Missing registry shard: {descriptor['path']}")
        shard = load_json(shard_path)
        shard_records = shard.get("records")
        require(isinstance(shard_records, list), f"Registry shard lacks records: {descriptor['path']}")
        require(len(shard_records) == descriptor["count"], f"Registry shard count mismatch: {descriptor['path']}")
        part_total += len(shard_records)
        for record in shard_records:
            identifier = record.get("id")
            require(isinstance(identifier, str) and identifier, f"Registry record without ID in {descriptor['path']}")
            require(identifier not in records, f"Duplicate CAEPR ID: {identifier}")
            require(record.get("type") == descriptor["type"], f"Type mismatch for {identifier}")
            records[identifier] = record; type_counts[descriptor["type"]] += 1
    require(part_total == index["counts"]["total"], "CAEPR total count mismatch")
    for kind in ("PERSON", "ORGANISATION", "STRUCTURE", "INSTITUTION", "PROCEEDING"):
        require(type_counts[kind] == index["counts"][kind], f"CAEPR {kind} count mismatch")

    master_court = records.get("PD-SP-I-0044")
    require(master_court is not None and master_court.get("name") == "Audiencia Provincial de Las Palmas", "Missing master Audiencia identity")
    require(master_court.get("identity_resolution") == "CARET_CONFIRMED", "Master court must be CARET_CONFIRMED")
    children = {row.get("institution_id") for row in master_court.get("child_institutions", [])}
    require({"PD-SP-I-0014", "PD-SP-I-0025"} <= children, "Master court section set lost a controlled child section")
    for child in children: require(child in records and records[child]["type"] == "INSTITUTION", f"Missing child court identity: {child}")

    current = load_json(DATA / "justice-authority-register-current-v2.json")
    require(current.get("control_id") == "PD-SP-JUSTICE-AUTHORITY-CURRENT-20260902-01", "Unexpected current authority control ID")
    authority_ids: set[str] = set(); confirmed_count = 0; pending_count = 0; role_counts = Counter(); pending_roles = Counter()
    for descriptor in current.get("person_sources", []):
        source = load_json(ROOT / descriptor["path"])
        source_rows: list[tuple[str, str, str]] = []
        if isinstance(source.get("roles"), dict):
            for role, rows in source.get("roles", {}).items():
                for row in rows: source_rows.append((row["caepr_id"], row.get("state", ""), role))
        else:
            for row in source.get("records", []): source_rows.append((row["id"], row.get("identity_resolution", ""), row.get("role", "")))
        ids = {row[0] for row in source_rows}
        require(authority_ids.isdisjoint(ids), f"Current authority sources contain duplicate people in {descriptor['path']}")
        authority_ids |= ids
        confirmed_count += sum(state == "CARET_CONFIRMED" for _, state, _ in source_rows)
        pending_count += sum(state == "CARET_PENDING" for _, state, _ in source_rows)
        for _, state, role in source_rows:
            require(role in {"MINISTERIO_FISCAL", "JUDGE_OR_MAGISTRATE", "LAJ", "NOTARY"}, f"Missing/invalid derived role {role!r} in {descriptor['path']}")
            role_counts[role] += 1
            if state == "CARET_PENDING": pending_roles[role] += 1
    derived = current["derived_counts"]
    require(len(authority_ids) == derived["unique_named_people"], "Derived people count mismatch")
    require(confirmed_count == derived["confirmed"], "Derived confirmed count mismatch")
    require(pending_count == derived["pending"], "Derived pending count mismatch")
    require(dict(role_counts) == derived["by_role"], f"Derived role count mismatch: {role_counts} vs {derived['by_role']}")
    require(pending_roles.get("JUDGE_OR_MAGISTRATE", 0) == 0 and pending_roles.get("LAJ", 0) == 0, "A Judge/LAJ remains pending contrary to current denominator")
    for identifier in authority_ids: require(identifier in records, f"Current authority person absent from CAEPR: {identifier}")

    search_script = (ROOT / "assets" / "canonical-home-search-20260902.js").read_text(encoding="utf-8")
    site_script = (ROOT / "assets" / "site.js").read_text(encoding="utf-8")
    overlay_script = (ROOT / "assets" / "justice-professionals-current-overlay-20260902.js").read_text(encoding="utf-8")
    for marker in ("matter-identity-registry-v1.json", "proceedings-master-public-v1.json", "proceeding-page-routes-20260902.json", "^P-0147", "^I-0044", "URLSearchParams", "PorDerechoCanonicalSearch"):
        require(marker in search_script, f"Canonical search script lacks marker: {marker}")
    require("canonical-home-search-20260902.js" in site_script, "site.js does not load canonical homepage search")
    require("justice-professionals-current-overlay-20260902.js" in site_script, "site.js does not load current justice overlay")
    require("siteHeader.insertAdjacentElement('afterend', section)" in search_script, "Homepage search is not mounted after site header")
    require("section.closest('details')" in search_script, "Homepage search lacks closed-details mount guard")
    require("main.insertBefore(section" not in search_script, "Homepage search retains unsafe main-child insertion")
    for marker in ("justice-authority-register-current-v2.json", "derived_counts", "proceeding-justice-authority-coverage-20260902.json", "proceeding-page-routes-20260902.json"):
        require(marker in overlay_script, f"Justice overlay is not dynamic/reciprocal: {marker}")
    require("[['61'" not in overlay_script and "['61', 0]" not in overlay_script, "Justice overlay still freezes a prior denominator")

    master_projection = load_json(DATA / "proceedings-master-public-v1.json")
    entries = [make_caepr_entry(record) for record in records.values()]
    entries.extend(make_master_entry(record) for record in master_projection.get("records", []))
    def search(query: str) -> list[str]:
        ranked = sorted(((score(entry, query), entry.identifier) for entry in entries), key=lambda item: (-item[0], item[1]))
        return [identifier for value, identifier in ranked if value > 0]

    smoke_tests = {
        "Graciela Pérez-Valencia Díaz": "PD-SP-P-0147", "PD-SP-P-0147": "PD-SP-P-0147", "^P-0147": "PD-SP-P-0147",
        "DP 748/2026": "PD-SP-R-0003", "TF-CRI-003": "PD-SP-R-0003", "3802343220260002351": "PD-SP-R-0003",
        "Ricardo de Mosteyrín Sampalo": "PD-SP-P-0058", "Audiencia Provincial de Las Palmas": "PD-SP-I-0044", "^I-0044": "PD-SP-I-0044",
        "Rollo 1010/2018": "LZ-APP-004", "Procedimiento Ordinario 467/2010": "LZ-CIV-045", "3500441120100004798": "LZ-CIV-045",
        "Emma Galcerán Solsona": "PD-SP-P-0164", "Diligencias Preliminares 1041/2017": "GC-CIV-003", "3501642120170028407": "GC-CIV-003",
        "Fernando Pérez Polo": "PD-SP-P-0165", "PD-SP-P-0165": "PD-SP-P-0165", "^P-0165": "PD-SP-P-0165",
        "Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria": "PD-SP-I-0048", "^I-0048": "PD-SP-I-0048",
    }
    for query, expected in smoke_tests.items():
        matches = search(query); require(expected in matches[:12], f"Search query {query!r} did not return {expected}; got {matches[:12]}")

    refs = [r.get("Reference") for r in master_projection.get("records", [])]
    require(refs.count("Diligencias Preliminares 1041/2017") == 1, "1041/2017 is duplicated in public Master projection")

    for path, title in {
        ROOT/"es/registro-judicial-audiencia-provincial-las-palmas/index.html": "Audiencia Provincial de Las Palmas",
        ROOT/"en/las-palmas-provincial-court-register/index.html": "Las Palmas Provincial Court",
        ROOT/"es/registro-autoridad-historica-las-palmas-civil/index.html": "Diligencias Preliminares 1041/2017",
        ROOT/"en/historic-las-palmas-civil-justice-authority-register/index.html": "Diligencias Preliminares 1041/2017",
    }.items():
        require(path.is_file(), f"Missing public authority page: {path.relative_to(ROOT)}")
        require(title in path.read_text(encoding="utf-8"), f"{path.relative_to(ROOT)} lacks {title}")

    require((ROOT/".github/governance/JUDICIAL_PROSECUTORIAL_AUTHORITY_REGISTER_CONTINUITY_02SEP2026.md").is_file(), "Missing authority continuity governance")
    require((ROOT/".github/workflows/audit-canonical-home-search.yml").is_file(), "Missing canonical home-search workflow")
    print(f"PASS canonical authority/search audit: {len(records)} CAEPR records; {len(authority_ids)} current justice professionals; {confirmed_count} confirmed; {pending_count} pending; {dict(role_counts)}; {len(smoke_tests)} search tests")


if __name__ == "__main__": main()

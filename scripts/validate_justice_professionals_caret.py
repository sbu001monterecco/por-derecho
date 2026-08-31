#!/usr/bin/env python3
"""Validate the finite justice-professionals CAEPR caret census."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
AUDIT_PATH = DATA / "justice-professionals-caret-audit-v1.json"
REGISTRY_INDEX = DATA / "matter-identity-registry-v1.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain an object")
    return value


def load_registry() -> dict[str, dict]:
    index = load_json(REGISTRY_INDEX)
    records: dict[str, dict] = {}
    for descriptor in index["parts"]:
        shard = load_json(DATA / descriptor["path"])
        require(len(shard["records"]) == descriptor["count"], f"Registry shard count mismatch: {descriptor['path']}")
        for record in shard["records"]:
            require(record["id"] not in records, f"Duplicate registry ID: {record['id']}")
            records[record["id"]] = record
    require(len(records) == index["counts"]["total"], "Registry total does not match master count")
    return records


def public_text(path: str) -> str:
    target = ROOT / path
    require(target.is_file(), f"Missing public route: {path}")
    return target.read_text(encoding="utf-8")


def main() -> None:
    audit = load_json(AUDIT_PATH)
    registry = load_registry()

    require(audit.get("schema") == "por-derecho.justice-professionals-caret-audit.v1", "Unexpected audit schema")
    require(audit.get("control_id") == "PD-SP-JUSTICE-PROFESSIONALS-CARET-20260831-01", "Unexpected control ID")
    require(audit.get("status") == "PARTIAL_NOT_ALL_IS_CARET", "Audit must preserve partial verdict")

    roles = audit.get("roles")
    require(isinstance(roles, dict), "Audit roles must be an object")
    expected_roles = {"MINISTERIO_FISCAL", "JUDGE_OR_MAGISTRATE", "LAJ", "NOTARY", "PROPERTY_REGISTRY_PERSON"}
    require(set(roles) == expected_roles, "Audit role set is incomplete or contains an unexpected role")

    rows = [row for role_rows in roles.values() for row in role_rows]
    ids = [row["caepr_id"] for row in rows]
    require(len(rows) == 48, f"Expected 48 named people, found {len(rows)}")
    require(len(ids) == len(set(ids)), "Justice-professional audit contains duplicate CAEPR IDs")
    require(len({row['name'] for row in rows}) == len(rows), "Justice-professional audit contains duplicate names")

    confirmed = [row for row in rows if row["state"] == "CARET_CONFIRMED"]
    pending = [row for row in rows if row["state"] == "CARET_PENDING"]
    require(len(confirmed) == 45, f"Expected 45 confirmed people, found {len(confirmed)}")
    require(len(pending) == 3, f"Expected 3 pending people, found {len(pending)}")
    require({row["caepr_id"] for row in pending} == {"PD-SP-P-0138", "PD-SP-P-0139", "PD-SP-P-0143"}, "Pending set changed without audit update")

    counts = audit["counts"]
    require(counts["named_people"] == len(rows), "Audit named-person count mismatch")
    require(counts["confirmed"] == len(confirmed), "Audit confirmed count mismatch")
    require(counts["pending"] == len(pending), "Audit pending count mismatch")
    require(abs(counts["coverage_percent"] - 93.75) < 0.0001, "Unexpected coverage percentage")

    for role, role_rows in roles.items():
        declared = counts["by_role"][role]
        require(declared["named"] == len(role_rows), f"{role} named count mismatch")
        require(declared["confirmed"] == sum(row["state"] == "CARET_CONFIRMED" for row in role_rows), f"{role} confirmed count mismatch")
        require(declared["pending"] == sum(row["state"] == "CARET_PENDING" for row in role_rows), f"{role} pending count mismatch")

    for row in rows:
        record = registry.get(row["caepr_id"])
        require(record is not None, f"Audit ID missing from master registry: {row['caepr_id']}")
        require(record.get("type") == "PERSON", f"Audit ID is not a person: {row['caepr_id']}")
        require(record.get("name") == row["name"], f"Name mismatch for {row['caepr_id']}")
        require(record.get("identity_resolution") == row["state"], f"State mismatch for {row['caepr_id']}")
        sources = record.get("identity_sources")
        require(isinstance(sources, list) and sources, f"Missing identity sources for {row['caepr_id']}")
        boundary = record.get("capacity_boundary") or record.get("identity_boundary")
        require(isinstance(boundary, str) and len(boundary) >= 40, f"Missing capacity boundary for {row['caepr_id']}")
        if row["state"] == "CARET_PENDING":
            require(isinstance(row.get("missing_source"), str) and row["missing_source"], f"Pending row lacks missing-source target: {row['caepr_id']}")

    registry_control = audit["property_registry_control"]
    require(counts["property_registry_named_people"] == 0, "Property Registry named-person denominator must remain zero")
    require(roles["PROPERTY_REGISTRY_PERSON"] == [], "No Property Registry person may be inferred from a generic literal")
    require(registry_control["exact_named_people"] == [], "Property Registry control unexpectedly contains a named person")
    require(registry_control["result"] == "NO_EXACT_PERSON_NAME_LOCATED_IN_REVIEWED_CORPUS", "Property Registry gap status changed")

    es = public_text("es/registro-identidad-profesionales-justicia/index.html")
    en = public_text("en/justice-professionals-identity-register/index.html")
    for row in rows:
        for language, html in (("ES", es), ("EN", en)):
            require(row["name"] in html, f"{language} census missing {row['name']}")
            marker = f'data-caepr-id="{row["caepr_id"]}" data-caret-state="{row["state"]}"'
            require(marker in html, f"{language} census missing state marker for {row['caepr_id']}")
            element_pattern = re.compile(
                rf'<(?P<tag>span|a)[^>]*data-caepr-id="{re.escape(row["caepr_id"])}"[^>]*>(?P<label>.*?)</(?P=tag)>',
                re.DOTALL,
            )
            element_match = element_pattern.search(html)
            require(element_match is not None, f"{language} census element missing: {row['caepr_id']}")
            label = element_match.group("label")
            label_text = re.sub(r"<[^>]+>", "", label)
            require(row["name"] in label_text, f"{language} CAEPR ID/name mismatch: {row['caepr_id']}")
            if row["state"] == "CARET_CONFIRMED":
                require("<sup>^</sup>" in label or f"{row['name']}^" in label_text, f"{language} confirmed row lacks visible caret: {row['caepr_id']}")
            else:
                require("<sup>^</sup>" not in label and f"{row['name']}^" not in label_text, f"{language} pending row incorrectly displays a caret: {row['caepr_id']}")

    for source in audit["source_surfaces"]:
        require((ROOT / source).is_file(), f"Declared source surface missing: {source}")

    ricardo_es = public_text("es/ricardo-de-mosteyrin-sampalo/index.html")
    ricardo_en = public_text("en/ricardo-de-mosteyrin-sampalo/index.html")
    required_ricardo_tokens = [
        "PD-SP-P-0058",
        "calificacion-rpl-2523",
        "dp-1901-2026",
        "fiscalia-inspeccion-exp-gub-745-2026",
        "BOE-A-2026-1094",
        "justice-professionals-identity-register",
    ]
    for token in required_ricardo_tokens:
        require(token in ricardo_es or token in ricardo_en, f"Ricardo page pair lacks required token: {token}")
    require("No se ha localizado" in ricardo_es, "Spanish Ricardo page lacks DP 1901 non-attribution boundary")
    require("does not contain the signed report" in ricardo_en, "English Ricardo page lacks DP 1901 non-attribution boundary")

    reciprocal_pages = {
        "es/calificacion-concurso-36-2012-vidas-paralelas/index.html": "../ricardo-de-mosteyrin-sampalo/",
        "en/insolvency-classification-parallel-lives/index.html": "../ricardo-de-mosteyrin-sampalo/",
        "es/calificacion-rpl-2523-mapa-prueba/index.html": "../ricardo-de-mosteyrin-sampalo/",
        "en/calificacion-rpl-2523-evidence-map/index.html": "../ricardo-de-mosteyrin-sampalo/",
        "es/dp-1901-2026/index.html": "../ricardo-de-mosteyrin-sampalo/",
        "en/dp-1901-2026/index.html": "../ricardo-de-mosteyrin-sampalo/",
        "es/fiscalia-inspeccion-exp-gub-745-2026/index.html": "../ricardo-de-mosteyrin-sampalo/",
        "en/public-prosecution-inspection-exp-gub-745-2026/index.html": "../ricardo-de-mosteyrin-sampalo/",
    }
    for path, link in reciprocal_pages.items():
        require(link in public_text(path), f"Missing reciprocal Ricardo link: {path}")

    print("Justice-professionals caret audit validated: 48 named; 45 confirmed; 3 pending; Registry named-person denominator 0")


if __name__ == "__main__":
    main()

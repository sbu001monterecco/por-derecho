#!/usr/bin/env python3
"""Validate the public ACTA / 2022 / authority interconnectivity surface."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/community-acta-authority-interconnectivity-v1.json"
MASTER = ROOT / "assets/data/proceedings-master-public-v1.json"
ACTAS = ROOT / "evidence/community/actas/public-index.json"
ASSERTIONS = ROOT / "assets/data/community-acta-authority-link-assertions-v1.json"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def keys_recursive(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from keys_recursive(child)
    elif isinstance(value, list):
        for child in value:
            yield from keys_recursive(child)


def main() -> int:
    errors: list[str] = []
    required = [
        DATA, MASTER, ACTAS, ASSERTIONS,
        ROOT / "scripts/build_community_acta_authority_interconnectivity.py",
        ROOT / "assets/community-acta-authority-interconnectivity-20260831.js",
        ROOT / "assets/community-acta-authority-interconnectivity-20260831.css",
        ROOT / "assets/acta-authority-interlink-20260831.js",
        ROOT / "en/community-actas-public-authorities/index.html",
        ROOT / "es/actas-comunidad-autoridades-publicas/index.html",
    ]
    for path in required:
        require(path.exists(), f"missing required file: {path.relative_to(ROOT)}", errors)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1

    payload = json.loads(DATA.read_text(encoding="utf-8"))
    master = json.loads(MASTER.read_text(encoding="utf-8"))
    assertions = json.loads(ASSERTIONS.read_text(encoding="utf-8"))
    prism = json.loads((ROOT / "assets/data/proceedings-case-prism-v1.json").read_text(encoding="utf-8"))
    master_ids = {record["Master_ID"] for record in master["records"]}
    allowed_types = set(assertions["authority_record_types"])
    expected_authority_ids = {record["Master_ID"] for record in master["records"] if record["Record_Type"] in allowed_types}
    authority_ids = {record["master_id"] for record in payload["authority_files"]}
    acta_ids = {record["id"] for record in payload["actas"]}
    proposition_ids = {record["id"] for record in prism["propositions"]}
    c = payload["coverage"]

    require(payload.get("schema_version") == "1.0.0", "schema version changed", errors)
    require(payload.get("status") == "PUBLIC_SAFE_DERIVED_INTERCONNECTIVITY_PROJECTION", "status changed", errors)
    require(c.get("public_acta_packages") == len(acta_ids) == 20, "ACTA denominator is not 20", errors)
    require(c.get("public_authority_files") == len(authority_ids) == 49, "authority denominator is not 49", errors)
    require(authority_ids == expected_authority_ids, f"authority identity mismatch: {sorted(authority_ids ^ expected_authority_ids)}", errors)
    require(authority_ids.issubset(master_ids), "unknown authority Master ID", errors)
    require(c.get("authority_groups") == len(payload["authority_groups"]) == 6, "authority-group denominator is not six", errors)
    require(c.get("evidentiary_axes") == len(payload["evidentiary_axes"]) == 7, "evidence-axis denominator is not seven", errors)
    require(c.get("community_2022_milestones") == len(payload["parallel_2022"]["community_track"]) == 3, "community-milestone denominator changed", errors)
    require(c.get("adjudication_and_deed_milestones") == len(payload["parallel_2022"]["adjudication_track"]) == 6, "adjudication/deed denominator changed", errors)
    require(payload["parallel_2022"].get("days_from_acta_to_deed") == 17, "17-day comparison is missing", errors)
    require(payload["attributed_allegation"].get("status") == "SERIOUS_FALSIFIABLE_PARTY_ALLEGATION_NOT_ESTABLISHED", "allegation attribution boundary changed", errors)

    axis_ids = {axis["id"] for axis in payload["evidentiary_axes"]}
    require(axis_ids == {"AX-NOTICE-LPB", "AX-NOTICE-MATKATOR", "AX-VOTING-CONTROL", "AX-DEBT-COST", "AX-TITLE-BENEFIT", "AX-FUNDING", "AX-AUTHORITY"}, "axis identities changed", errors)
    for axis in payload["evidentiary_axes"]:
        require("not_established_en" in axis and "not_established_es" in axis, f"{axis['id']} lacks a non-finding boundary", errors)
        require("next_source_en" in axis and "contrary_en" in axis, f"{axis['id']} lacks source/contrary controls", errors)
    for record in payload["authority_files"]:
        require(record["group_id"] in {group["id"] for group in payload["authority_groups"]}, f"{record['master_id']} has unknown group", errors)
        require(set(record["axis_ids"]).issubset(axis_ids), f"{record['master_id']} has unknown axis", errors)
        require(all(link["proposition_id"] in proposition_ids for link in record["proposition_links"]), f"{record['master_id']} has unknown Case Prism proposition", errors)
        require(record.get("relationship_strength") == "DEPENDENCY_TEST_ONLY", f"{record['master_id']} overstates relationship strength", errors)
        require(record["master_id"] in payload["by_master_id"], f"{record['master_id']} missing reciprocal index", errors)
    require(set(payload["by_master_id"]) == authority_ids, "reciprocal authority index mismatch", errors)

    for acta in payload["actas"]:
        require((ROOT / acta["route_en"]).is_dir() and (ROOT / acta["route_es"]).is_dir(), f"missing bilingual ACTA route: {acta['id']}", errors)
        require((ROOT / acta["manifest"]).exists(), f"missing ACTA manifest: {acta['id']}", errors)
    require("SP-ACTA-2022-02-04" in acta_ids, "2022 ACTA missing", errors)

    forbidden_keys = {"actor_name", "source_locator", "recipient_email", "sender_email", "private_locator", "local_path"}
    exposed = set(keys_recursive(payload)) & forbidden_keys
    require(not exposed, f"forbidden public key(s): {sorted(exposed)}", errors)
    serialised = json.dumps(payload, ensure_ascii=False).lower()
    for token in ("temporal_proximity_is_not_causation", "allegation_is_not_finding", "institutional_possession_is_not_personal_knowledge"):
        require(token in serialised, f"reading rule missing: {token}", errors)

    master_js = (ROOT / "assets/master-proceedings-publication-20260830.js").read_text(encoding="utf-8")
    map_js = (ROOT / "assets/proceedings-interconnectivity-map-20260830.js").read_text(encoding="utf-8")
    site_js = (ROOT / "assets/site.js").read_text(encoding="utf-8")
    for text, label in ((master_js, "Master Register"), (map_js, "Proceedings Map")):
        require("data-community-authority-master-id" in text, f"{label} reciprocal marker missing", errors)
        require("community-acta-authority-interconnectivity-v1.json" in text, f"{label} dataset missing", errors)
    require("acta-authority-interlink-20260831.js" in site_js, "ACTA/adjudication reciprocal loader missing", errors)

    for page in required[-2:]:
        text = page.read_text(encoding="utf-8")
        require("data-ca-interconnectivity" in text, f"{page.relative_to(ROOT)} lacks app mount", errors)
        require("community-acta-authority-interconnectivity-20260831.js?v=20260831a" in text, f"{page.relative_to(ROOT)} lacks cache-busted renderer", errors)
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    require("/en/community-actas-public-authorities/" in sitemap and "/es/actas-comunidad-autoridades-publicas/" in sitemap, "sitemap routes missing", errors)

    check = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_community_acta_authority_interconnectivity.py"), "--check"],
        cwd=ROOT, capture_output=True, text=True,
    )
    require(check.returncode == 0, check.stdout.strip() or check.stderr.strip() or "deterministic builder check failed", errors)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("OK: ACTA / 2022 parallel-track / public-authority interconnectivity is complete, reciprocal, qualified and deterministic")
    print("- ACTAs: 20; authority files: 49 in 6 groups; evidence axes: 7")
    print("- 2022 milestones: 3 Community + 5 judicial decisions + deed 457; temporal comparison: 17 days")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

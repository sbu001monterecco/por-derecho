#!/usr/bin/env python3
"""Validate the synchronized Por Derecho unitary control plane."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AssertionError(f"cannot parse {path.relative_to(ROOT)}: {exc}") from exc


def require(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


def require_markers(path: Path, markers: list[str], forbidden: list[str] | None = None):
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        require(marker in text, f"missing {marker!r} in {path.relative_to(ROOT)}")
    for marker in forbidden or []:
        require(marker not in text, f"stale marker {marker!r} in {path.relative_to(ROOT)}")
    return text


def main() -> int:
    try:
        index = load_json(DATA / "matter-identity-registry-v1.json")
        counts = index.get("counts", {})
        expected = {"total": 185, "PERSON": 86, "ORGANISATION": 66, "STRUCTURE": 10, "INSTITUTION": 13, "PROCEEDING": 10}
        require(counts == expected, f"unexpected canonical identity counts: {counts}")

        actual = {"PERSON": 0, "ORGANISATION": 0, "STRUCTURE": 0, "INSTITUTION": 0, "PROCEEDING": 0}
        ids: set[str] = set()
        for descriptor in index.get("parts", []):
            part = load_json(DATA / descriptor["path"])
            records = part.get("records", [])
            require(len(records) == descriptor["count"], f"part count mismatch: {descriptor['path']}")
            for record in records:
                rid = record.get("id")
                require(rid and rid not in ids, f"duplicate or empty ID: {rid}")
                ids.add(rid)
                actual[record["type"]] += 1
        require(len(ids) == expected["total"], "identity part total mismatch")
        for key in actual:
            require(actual[key] == expected[key], f"identity class mismatch {key}: {actual[key]}")

        es_identity = require_markers(
            ROOT / "es/registro-identidad-materia/index.html",
            [
                'content="Registro operativo de 185 IDs inmutables',
                'data-static-registry-counts="185-86-66-10-13-10"',
                'data-registry-stat="TOTAL">185',
                'data-registry-stat="PERSON">86',
                'data-registry-stat="ORGANISATION">66',
                '"name":"Total","value":185',
                '../../ops/CURRENT_UNITARY_STATE.json',
            ],
            ['Los 159 IDs', 'data-registry-stat="TOTAL">159', '159 identidades canónicas']
        )
        en_identity = require_markers(
            ROOT / "en/matter-identity-registry/index.html",
            [
                'content="Operational Por Derecho register of 185 immutable IDs',
                'data-static-registry-counts="185-86-66-10-13-10"',
                'data-registry-stat="TOTAL">185',
                'data-registry-stat="PERSON">86',
                'data-registry-stat="ORGANISATION">66',
                '"name":"Total","value":185',
                '../../ops/CURRENT_UNITARY_STATE.json',
            ],
            ['The 159 IDs', 'data-registry-stat="TOTAL">159', '159 canonical identities']
        )
        require(es_identity.count('data-registry-stat="') >= 6, "Spanish identity stat set incomplete")
        require(en_identity.count('data-registry-stat="') >= 6, "English identity stat set incomplete")

        updates = load_json(DATA / "material-updates-v1.json")
        require(updates.get("control_id") == "PD-MATERIAL-UPDATES-001", "unexpected material-updates control")
        require(updates.get("latest_material_date") == "2026-08-25", "latest material date mismatch")
        require(len(updates.get("entries", [])) >= 4, "material update source too small")
        require(all(item.get("date") <= updates["latest_material_date"] for item in updates["entries"]), "future update date present")
        require_markers(ROOT / "es/actualizaciones/index.html", ["Última actualización material", "<strong>25 agosto 2026</strong>"])
        require_markers(ROOT / "en/updates/index.html", ["Latest material update", "<strong>25 August 2026</strong>"])

        state = load_json(ROOT / "ops/CURRENT_UNITARY_STATE.json")
        require(state.get("control_id") == "PD-UNITARY-STATE-20260825-01", "unexpected unitary-state control")
        require(re.fullmatch(r"[0-9a-f]{40}", state["repository"]["current_main_sha_at_preparation"]), "invalid preparation SHA")
        require(state["identity_registry"]["counts"] == expected, "state identity counts drift")
        require(state["material_updates"]["latest_material_date"] == updates["latest_material_date"], "state/update date drift")
        require(state["pull_requests"]["observed_open_count"] == 36, "open PR snapshot drift")

        current_pointer = load_json(ROOT / "ops/CURRENT_STATE.json")
        require(current_pointer.get("current_authority") == "ops/CURRENT_UNITARY_STATE.json", "CURRENT_STATE is not a unitary pointer")
        require(current_pointer.get("calificacion", {}).get("appeal_roll") == "RPL 2523/2025", "CURRENT_STATE compatibility roll missing")
        production = load_json(ROOT / "ops/PRODUCTION_STATUS.json")
        require(production.get("current_state") == "ops/CURRENT_UNITARY_STATE.json", "PRODUCTION_STATUS does not point to unitary state")
        require(production["exact_public_content_verification"]["state"] == "PENDING_AFTER_CONTROL_PLANE_MERGE", "production verification state overstated")
        require((ROOT / current_pointer["historical_snapshot"]).is_file(), "historical CURRENT_STATE snapshot missing")
        require((ROOT / production["historical_snapshot"]).is_file(), "historical PRODUCTION_STATUS snapshot missing")

        ledger = load_json(ROOT / "ops/PR_RECONCILIATION_LEDGER.json")
        require(ledger.get("open_pull_request_count") == 36, "PR ledger count drift")
        entries = {item["pr"]: item for item in ledger.get("priority_entries", [])}
        require(entries.get(1016, {}).get("state") == "REBUILD_ON_CURRENT_MAIN", "PR #1016 is not controlled")
        require(entries.get(771, {}).get("state") == "EXTRACT_UNIQUE_DELTA", "262-finca PR not controlled")

        require_markers(ROOT / "sitemap-unitary-control-plane.xml", [
            "https://sbu001monterecco.github.io/por-derecho/es/",
            "https://sbu001monterecco.github.io/por-derecho/en/updates/",
            "https://sbu001monterecco.github.io/por-derecho/es/registro-identidad-materia/",
            "<lastmod>2026-08-25</lastmod>",
        ])
        require_markers(ROOT / "robots.txt", ["sitemap-unitary-control-plane.xml", "sitemap-prescription-recovery.xml"])
        require_markers(ROOT / "CURRENT_UNITARY_STATE.md", ["PD-UNITARY-STATE-20260825-01", "185", "PR #1016"])

        manifest = load_json(ROOT / "publication-manifests/unitary-control-plane-sync-20260825.json")
        require(manifest.get("current_state") in {"PR_OPEN", "DEPLOYED", "LIVE_VERIFIED"}, "invalid manifest state")
        require(manifest.get("control_id") == "PD-UNITARY-STATE-20260825-01", "manifest/control mismatch")
        require(manifest.get("expected_routes", {}).get("es") and manifest.get("expected_routes", {}).get("en"), "manifest expected routes missing")
    except AssertionError as exc:
        print(f"UNITARY CONTROL PLANE: FAIL\n - {exc}", file=sys.stderr)
        return 1

    print("UNITARY CONTROL PLANE: PASS")
    print(" - identity denominator: 185 / 86 / 66 / 10 / 13 / 10")
    print(" - latest material date: 2026-08-25")
    print(" - current-state and production snapshots separated")
    print(" - PR #1016 controlled as rebuild-on-current-main")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
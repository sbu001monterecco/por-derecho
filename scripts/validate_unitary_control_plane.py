#!/usr/bin/env python3
"""Validate the synchronized Por Derecho specialist and operational control planes."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
EXPECTED = {
    "total": 185,
    "PERSON": 86,
    "ORGANISATION": 66,
    "STRUCTURE": 10,
    "INSTITUTION": 13,
    "PROCEEDING": 10,
}
UNITARY_CONTROL_ID = "PD-UNITARY-STATE-20260825-01"
UNITARY_VERIFY_RUN = 32912919872


def load_json(path: Path):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AssertionError(f"cannot parse {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise AssertionError(f"{path.relative_to(ROOT)} root must be object")
    return value


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
        require(index.get("counts") == EXPECTED, f"unexpected identity counts: {index.get('counts')}")

        actual = {key: 0 for key in EXPECTED if key != "total"}
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
        require(len(ids) == EXPECTED["total"], "identity part total mismatch")
        for key in actual:
            require(actual[key] == EXPECTED[key], f"identity class mismatch {key}: {actual[key]}")

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
            ['Los 159 IDs', 'data-registry-stat="TOTAL">159', '159 identidades canónicas'],
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
            ['The 159 IDs', 'data-registry-stat="TOTAL">159', '159 canonical identities'],
        )
        require(es_identity.count('data-registry-stat="') >= 6, "Spanish identity stat set incomplete")
        require(en_identity.count('data-registry-stat="') >= 6, "English identity stat set incomplete")

        updates = load_json(DATA / "material-updates-v1.json")
        require(updates.get("control_id") == "PD-MATERIAL-UPDATES-001", "unexpected material-updates control")
        require(updates.get("latest_material_date") == "2026-08-25", "latest material date mismatch")
        require(len(updates.get("entries", [])) >= 4, "material update source too small")
        require(
            all(item.get("date") <= updates["latest_material_date"] for item in updates["entries"]),
            "future update date present",
        )
        require_markers(
            ROOT / "es/actualizaciones/index.html",
            ["Última actualización material", "<strong>25 agosto 2026</strong>"],
        )
        require_markers(
            ROOT / "en/updates/index.html",
            ["Latest material update", "<strong>25 August 2026</strong>"],
        )

        state = load_json(ROOT / "ops/CURRENT_UNITARY_STATE.json")
        require(state.get("schema") == "por-derecho.current-unitary-state.v1", "unexpected unitary schema")
        require(state.get("control_id") == UNITARY_CONTROL_ID, "unexpected unitary-state control")
        require(state.get("status") == "LIVE_VERIFIED", "unitary state is not live verified")
        require(
            re.fullmatch(r"[0-9a-f]{40}", state["repository"]["current_main_sha_at_preparation"]),
            "invalid preparation SHA",
        )
        require(state["identity_registry"]["counts"] == EXPECTED, "state identity counts drift")
        require(
            state["material_updates"]["latest_material_date"] == updates["latest_material_date"],
            "state/update date drift",
        )
        readback = state["publication"]["current_sha_edge_readback"]
        require(readback["state"] == "LIVE_VERIFIED", "state readback is not live verified")
        require(readback["workflow_run_id"] == UNITARY_VERIFY_RUN, "unexpected unitary verifier run")
        require(state["pull_requests"]["observed_open_count"] == 36, "unitary open-PR snapshot drift")

        current = load_json(ROOT / "ops/CURRENT_STATE.json")
        require(
            current.get("schema") == "por-derecho.operational-truth.current-state.v2",
            "operational current-state schema drift",
        )
        require(
            current.get("record_type") == "CURRENT_STATE_CONTRACT_WITH_LAST_OBSERVATION",
            "operational current-state record type drift",
        )
        routing = current.get("specialist_state_routing") or {}
        require(
            routing.get("unitary_case_and_evidence_state") == "ops/CURRENT_UNITARY_STATE.json",
            "operational→unitary routing missing",
        )
        require(routing.get("expected_control_id") == UNITARY_CONTROL_ID, "operational unitary-control expectation drift")
        require(routing.get("expected_status") == "LIVE_VERIFIED", "operational unitary-status expectation drift")
        require(
            "Neither layer substitutes" in str(routing.get("rule", "")),
            "operational/unitary non-substitution rule missing",
        )
        require(
            current.get("corpus", {}).get("identity_registry", {}).get("counts") == EXPECTED,
            "operational identity counts drift",
        )

        production = load_json(ROOT / "ops/PRODUCTION_STATUS.json")
        require(
            production.get("schema") == "por-derecho.operational-truth.production-status.v2",
            "production status schema drift",
        )
        require(
            production.get("record_type") == "OBSERVED_GITHUB_PAGES_DEPLOYMENT",
            "production status record type drift",
        )
        require(production.get("deployment", {}).get("conclusion") == "success", "observed Pages deployment is not successful")
        require(
            production.get("verification", {}).get("current_exact_route_content_verification")
            == "NOT_RECORDED_FOR_SERVED_SHA",
            "current served-SHA readback boundary is overstated or missing",
        )
        specialist = production.get("verification", {}).get("latest_live_verified_specialist_release") or {}
        require(specialist.get("state") == "LIVE_VERIFIED", "production specialist readback evidence missing")
        require(specialist.get("control_id") == UNITARY_CONTROL_ID, "production specialist control mismatch")
        require(specialist.get("workflow_run_id") == UNITARY_VERIFY_RUN, "production specialist verifier mismatch")
        require(
            production.get("specialist_state_routing", {}).get("unitary_case_and_evidence_state")
            == "ops/CURRENT_UNITARY_STATE.json",
            "production→unitary routing missing",
        )

        ledger = load_json(ROOT / "ops/PR_RECONCILIATION_LEDGER.json")
        require(isinstance(ledger.get("open_pull_request_count"), int), "PR ledger count missing")
        entries = {item["pr"]: item for item in ledger.get("priority_entries", [])}
        require(entries.get(1016, {}).get("state") == "REBUILD_ON_CURRENT_MAIN", "PR #1016 is not controlled")
        require(entries.get(771, {}).get("state") == "EXTRACT_UNIQUE_DELTA", "262-finca PR not controlled")

        require_markers(
            ROOT / "sitemap-unitary-control-plane.xml",
            [
                "https://sbu001monterecco.github.io/por-derecho/es/",
                "https://sbu001monterecco.github.io/por-derecho/en/updates/",
                "https://sbu001monterecco.github.io/por-derecho/es/registro-identidad-materia/",
                "<lastmod>2026-08-25</lastmod>",
            ],
        )
        require_markers(
            ROOT / "robots.txt",
            ["sitemap-unitary-control-plane.xml", "sitemap-prescription-recovery.xml"],
        )
        require_markers(
            ROOT / "CURRENT_UNITARY_STATE.md",
            [UNITARY_CONTROL_ID, "LIVE_VERIFIED", str(UNITARY_VERIFY_RUN), "PR #1016"],
        )

        manifest = load_json(ROOT / "publication-manifests/unitary-control-plane-sync-20260825.json")
        require(manifest.get("current_state") == "LIVE_VERIFIED", "manifest is not live verified")
        require(manifest.get("status") == "live_verified", "manifest status mismatch")
        require(manifest.get("control_id") == UNITARY_CONTROL_ID, "manifest/control mismatch")
        require(
            manifest.get("live_verification_evidence", {}).get("workflow_run_id") == UNITARY_VERIFY_RUN,
            "manifest verifier run mismatch",
        )
        require(
            manifest.get("expected_routes", {}).get("es")
            and manifest.get("expected_routes", {}).get("en"),
            "manifest expected routes missing",
        )
    except AssertionError as exc:
        print(f"UNITARY CONTROL PLANE: FAIL\n - {exc}", file=sys.stderr)
        return 1

    print("UNITARY CONTROL PLANE: PASS")
    print(" - specialist status: LIVE_VERIFIED")
    print(" - operational repository/deployment state remains separate")
    print(" - identity denominator: 185 / 86 / 66 / 10 / 13 / 10")
    print(" - latest material date: 2026-08-25")
    print(f" - specialist verifier run: {UNITARY_VERIFY_RUN}")
    print(" - PR #1016 controlled as rebuild-on-current-main")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

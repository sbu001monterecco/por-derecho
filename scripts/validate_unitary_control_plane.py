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
    "total": 187,
    "PERSON": 88,
    "ORGANISATION": 66,
    "STRUCTURE": 10,
    "INSTITUTION": 13,
    "PROCEEDING": 10,
}
UNITARY_CONTROL_ID = "PD-UNITARY-STATE-20260825-01"
ALLOWED_SPECIALIST_STATES = {"PREPARED_PENDING_MERGE_AND_LIVE_READBACK", "LIVE_VERIFIED"}


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
        require("PD-SP-P-0087" in ids and "PD-SP-P-0088" in ids, "Acosta Matos owner-network IDs missing")

        es_identity = require_markers(
            ROOT / "es/registro-identidad-materia/index.html",
            [
                'content="Registro operativo de 187 IDs inmutables',
                'data-static-registry-counts="187-88-66-10-13-10"',
                'data-registry-stat="TOTAL">187',
                'data-registry-stat="PERSON">88',
                'data-registry-stat="ORGANISATION">66',
                '"name":"Total","value":187',
                'perimetro-propietarios-no-lpb-matkator/',
                '../../ops/CURRENT_UNITARY_STATE.json',
            ],
            ['Los 159 IDs', 'data-registry-stat="TOTAL">159', '159 identidades canónicas'],
        )
        en_identity = require_markers(
            ROOT / "en/matter-identity-registry/index.html",
            [
                'content="Operational Por Derecho register of 187 immutable IDs',
                'data-static-registry-counts="187-88-66-10-13-10"',
                'data-registry-stat="TOTAL">187',
                'data-registry-stat="PERSON">88',
                'data-registry-stat="ORGANISATION">66',
                '"name":"Total","value":187',
                'non-lpb-matkator-owner-network/',
                '../../ops/CURRENT_UNITARY_STATE.json',
            ],
            ['The 159 IDs', 'data-registry-stat="TOTAL">159', '159 canonical identities'],
        )
        require(es_identity.count('data-registry-stat="') >= 6, "Spanish identity stat set incomplete")
        require(en_identity.count('data-registry-stat="') >= 6, "English identity stat set incomplete")

        owner_network = load_json(DATA / "non-lpb-matkator-owner-court-network-v1.json")
        require(owner_network.get("control_id") == "PD-SP-OWNER-COURT-NETWORK-001", "owner-network control missing")
        core = owner_network.get("judicial_core") or {}
        require(len(core.get("claimant_owner_ids", [])) == 7, "AP89 claimant-owner core must remain exactly seven")
        require("PD-SP-P-0027" in {item.get("person_id") for item in owner_network.get("individualised_propositions", [])}, "Celia proposition missing")
        require("PD-SP-P-0031" in {item.get("person_id") for item in owner_network.get("individualised_propositions", [])}, "Manuel proposition missing")
        require({"PD-SP-P-0011","PD-SP-P-0012","PD-SP-P-0087","PD-SP-P-0088"} == {item.get("id") for item in owner_network.get("acosta_matos_people", [])}, "Acosta Matos cluster mismatch")
        require_markers(ROOT / "es/registro-identidad-materia/perimetro-propietarios-no-lpb-matkator/index.html", ["PD-SP-OWNER-COURT-NETWORK-001","Celia Guillén Pérez","Manuel Molina Climent","Gerardo Zacarías Acosta Matos","Javier Acosta Matos"])
        require_markers(ROOT / "en/matter-identity-registry/non-lpb-matkator-owner-network/index.html", ["PD-SP-OWNER-COURT-NETWORK-001","Celia Guillén Pérez","Manuel Molina Climent","Gerardo Zacarías Acosta Matos","Javier Acosta Matos"])

        updates = load_json(DATA / "material-updates-v1.json")
        require(updates.get("control_id") == "PD-MATERIAL-UPDATES-001", "unexpected material-updates control")
        require(updates.get("latest_material_date") == "2026-08-25", "latest material date mismatch")
        require(len(updates.get("entries", [])) >= 4, "material update source too small")
        require(all(item.get("date") <= updates["latest_material_date"] for item in updates["entries"]), "future update date present")
        require_markers(ROOT / "es/actualizaciones/index.html", ["Última actualización material", "<strong>25 agosto 2026</strong>"])
        require_markers(ROOT / "en/updates/index.html", ["Latest material update", "<strong>25 August 2026</strong>"])

        state = load_json(ROOT / "ops/CURRENT_UNITARY_STATE.json")
        require(state.get("schema") == "por-derecho.current-unitary-state.v1", "unexpected unitary schema")
        require(state.get("control_id") == UNITARY_CONTROL_ID, "unexpected unitary-state control")
        require(state.get("status") in ALLOWED_SPECIALIST_STATES, f"unexpected unitary state {state.get('status')}")
        require(re.fullmatch(r"[0-9a-f]{40}", state["repository"]["current_main_sha_at_preparation"]), "invalid preparation SHA")
        require(state["identity_registry"]["counts"] == EXPECTED, "state identity counts drift")
        require(state["material_updates"]["latest_material_date"] == updates["latest_material_date"], "state/update date drift")
        require("owner_network" in state.get("canonical_routes", {}), "unitary owner-network routes missing")

        current = load_json(ROOT / "ops/CURRENT_STATE.json")
        require(current.get("schema") == "por-derecho.operational-truth.current-state.v2", "operational current-state schema drift")
        require(current.get("record_type") == "CURRENT_STATE_CONTRACT_WITH_LAST_OBSERVATION", "operational current-state record type drift")
        routing = current.get("specialist_state_routing") or {}
        require(routing.get("unitary_case_and_evidence_state") == "ops/CURRENT_UNITARY_STATE.json", "operational→unitary routing missing")
        require(routing.get("expected_control_id") == UNITARY_CONTROL_ID, "operational unitary-control expectation drift")
        require(routing.get("expected_status") in ALLOWED_SPECIALIST_STATES, "operational unitary-status expectation drift")
        require("Neither layer substitutes" in str(routing.get("rule", "")), "operational/unitary non-substitution rule missing")
        require(current.get("corpus", {}).get("identity_registry", {}).get("counts") == EXPECTED, "operational identity counts drift")
        require(current.get("corpus", {}).get("owner_court_network", {}).get("control_id") == "PD-SP-OWNER-COURT-NETWORK-001", "operational owner-network route missing")

        production = load_json(ROOT / "ops/PRODUCTION_STATUS.json")
        require(production.get("schema") == "por-derecho.operational-truth.production-status.v2", "production status schema drift")
        require(production.get("record_type") == "OBSERVED_GITHUB_PAGES_DEPLOYMENT", "production status record type drift")
        require(production.get("deployment", {}).get("conclusion") == "success", "observed Pages deployment is not successful")

        ledger = load_json(ROOT / "ops/PR_RECONCILIATION_LEDGER.json")
        require(isinstance(ledger.get("open_pull_request_count"), int), "PR ledger count missing")
        entries = {item["pr"]: item for item in ledger.get("priority_entries", [])}
        require(entries.get(1016, {}).get("state") in {"REBUILD_ON_CURRENT_MAIN","SUPERSEDED"}, "PR #1016 is not controlled")
        require(entries.get(771, {}).get("state") == "EXTRACT_UNIQUE_DELTA", "262-finca PR not controlled")

        require_markers(ROOT / "sitemap-unitary-control-plane.xml", ["https://sbu001monterecco.github.io/por-derecho/es/", "https://sbu001monterecco.github.io/por-derecho/en/updates/", "https://sbu001monterecco.github.io/por-derecho/es/registro-identidad-materia/", "<lastmod>2026-08-25</lastmod>"])
        require_markers(ROOT / "robots.txt", ["sitemap-unitary-control-plane.xml", "sitemap-prescription-recovery.xml"])
        require_markers(ROOT / "CURRENT_UNITARY_STATE.md", [UNITARY_CONTROL_ID, "187", "PR #1016", "Gerardo Zacarías Acosta Matos"])

        manifest = load_json(ROOT / "publication-manifests/unitary-control-plane-sync-20260825.json")
        require(manifest.get("control_id") == UNITARY_CONTROL_ID, "manifest/control mismatch")
    except AssertionError as exc:
        print(f"UNITARY CONTROL PLANE: FAIL\n - {exc}", file=sys.stderr)
        return 1

    print("UNITARY CONTROL PLANE: PASS")
    print(" - unitary state source is synchronized for the 187-ID owner-network candidate")
    print(" - operational repository/deployment state remains separate")
    print(" - identity denominator: 187 / 88 / 66 / 10 / 13 / 10")
    print(" - latest material-evidence date remains 2026-08-25")
    print(" - AP89 core: seven claimant-owners; wider residual perimeter separate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
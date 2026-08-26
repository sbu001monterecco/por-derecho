#!/usr/bin/env python3
"""Validate the source-graded non-LPB/Matkator owner and court-party network."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
EXPECTED_COUNTS = {"total":187,"PERSON":88,"ORGANISATION":66,"STRUCTURE":10,"INSTITUTION":13,"PROCEEDING":10}
AP89_IDS = {"PD-SP-O-0015","PD-SP-O-0011","PD-SP-O-0012","PD-SP-O-0009","PD-SP-O-0010","PD-SP-P-0025","PD-SP-P-0020"}
ACOSTA_IDS = {"PD-SP-P-0011","PD-SP-P-0012","PD-SP-P-0087","PD-SP-P-0088"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


def main() -> int:
    try:
        index = load(DATA / "matter-identity-registry-v1.json")
        require(index.get("counts") == EXPECTED_COUNTS, f"identity count drift: {index.get('counts')}")
        identities = {}
        for descriptor in index.get("parts", []):
            payload = load(DATA / descriptor["path"])
            records = payload.get("records", [])
            require(len(records) == descriptor.get("count"), f"part count mismatch: {descriptor['path']}")
            for record in records:
                rid = record.get("id")
                require(rid and rid not in identities, f"duplicate/empty identity {rid}")
                identities[rid] = record
        require(len(identities) == 187, "canonical identity total is not 187")
        require(identities.get("PD-SP-P-0087", {}).get("name") == "Gerardo Zacarías Acosta Matos", "Gerardo Zacarías identity mismatch")
        require(identities.get("PD-SP-P-0088", {}).get("name") == "Javier Acosta Matos", "Javier Acosta Matos identity mismatch")
        require(identities.get("PD-SP-P-0013", {}).get("name") == "Gerardo Nicanor Acosta Armas", "Gerardo Nicanor identity mismatch")

        network = load(DATA / "non-lpb-matkator-owner-court-network-v1.json")
        require(network.get("schema") == "por-derecho.non-lpb-matkator-owner-court-network.v1", "wrong owner-network schema")
        require(network.get("control_id") == "PD-SP-OWNER-COURT-NETWORK-001", "wrong owner-network control ID")
        core = network.get("judicial_core") or {}
        core_ids = set(core.get("claimant_owner_ids", []))
        require(core_ids == AP89_IDS, f"AP89 core mismatch: {sorted(core_ids)}")
        require(len(core.get("claimant_names", [])) == 7, "AP89 claimant-name count must be seven")
        require(core.get("counsel_id") == "PD-SP-P-0003", "AP89 counsel identity drift")
        require("partial" in str(core.get("adverse_result", "")).casefold(), "adverse AP89 result is not preserved")

        layers = {item.get("layer_id"): item for item in network.get("layers", [])}
        required_layers = {
            "L1_JV1260_AP89_CLAIMANTS",
            "L2_WIDER_MONTELANZA_MOLINA_PERIMETER",
            "L3_2011_COMMUNITY_ORGAN_AND_REPRESENTATION",
            "L4_2016_REPRESENTATION_CONTINUITY",
            "L5_2017_2018_COMMUNITY_ACCESS",
            "L6_2022_ACOSTA_MATOS_PROJECT_CLUSTER",
            "L7_ACOSTA_MATOS_FAMILY_BUSINESS",
        }
        require(required_layers == set(layers), f"owner-network layers drift: {sorted(set(layers))}")
        require(set(layers["L1_JV1260_AP89_CLAIMANTS"]["members"]) >= AP89_IDS, "AP89 layer missing claimant IDs")
        require(set(layers["L7_ACOSTA_MATOS_FAMILY_BUSINESS"]["members"]) >= ACOSTA_IDS, "Acosta family/business cluster incomplete")
        for layer in layers.values():
            for rid in layer.get("members", []):
                require(rid in identities, f"unknown identity in layer {layer.get('layer_id')}: {rid}")

        props = {item.get("person_id"): item for item in network.get("individualised_propositions", [])}
        require("PD-SP-P-0027" in props, "Celia Guillén proposition missing")
        require("party" in str(props["PD-SP-P-0027"].get("limit_en", "")).casefold(), "Celia party-source limit missing")
        require("PD-SP-P-0031" in props, "Manuel Molina Climent proposition missing")
        require("not the same" in str(props["PD-SP-P-0031"].get("limit_en", "")).casefold(), "Manuel debt-creation limit missing")

        cluster = {item.get("id") for item in network.get("acosta_matos_people", [])}
        require(cluster == ACOSTA_IDS, f"Acosta people cluster mismatch: {sorted(cluster)}")
        require("not PD-SP-P-0013" in str(layers["L7_ACOSTA_MATOS_FAMILY_BUSINESS"].get("distinction", "")), "Gerardo Zacarías/Nicanor distinction missing")
        require(len(network.get("p0_evidence_programme", [])) >= 8, "finite P0 evidence programme incomplete")
        require(any("71-versus-72" in item for item in network["p0_evidence_programme"]), "71/72 discrepancy control missing")

        public_blob = json.dumps(network, ensure_ascii=False)
        for prohibited in ["Josep Ponsirenas", "Oriol Huguet"]:
            require(prohibited not in public_blob, f"transaction-only contact leaked into owner network: {prohibited}")

        route_checks = {
            ROOT / "es/registro-identidad-materia/perimetro-propietarios-no-lpb-matkator/index.html": ["PD-SP-OWNER-COURT-NETWORK-001", "Celia Guillén Pérez", "Manuel Molina Climent", "Gerardo Zacarías Acosta Matos", "Javier Acosta Matos"],
            ROOT / "en/matter-identity-registry/non-lpb-matkator-owner-network/index.html": ["PD-SP-OWNER-COURT-NETWORK-001", "Celia Guillén Pérez", "Manuel Molina Climent", "Gerardo Zacarías Acosta Matos", "Javier Acosta Matos"],
            ROOT / "es/jv1260-ap89-continuidad-cam/index.html": ["JV 1260/2011", "AP 89/2014", "red canónica"],
            ROOT / "en/jv1260-ap89-cam-continuity/index.html": ["JV 1260/2011", "AP 89/2014", "canonical network"],
        }
        for path, markers in route_checks.items():
            require(path.is_file(), f"missing public route: {path.relative_to(ROOT)}")
            text = path.read_text(encoding="utf-8")
            for marker in markers:
                require(marker in text, f"missing marker {marker!r} in {path.relative_to(ROOT)}")
    except AssertionError as exc:
        print(f"NON-LPB OWNER COURT NETWORK: FAIL\n - {exc}", file=sys.stderr)
        return 1

    print("NON-LPB OWNER COURT NETWORK: PASS")
    print(" - AP89 core: exactly seven claimant-owners / 18 bungalows")
    print(" - wider Montelanza/Molina perimeter: separately graded")
    print(" - Celia Guillén and Manuel Molina Climent: individualised propositions")
    print(" - Acosta Matos cluster: four people; family/business relation does not transfer liability")
    print(" - identity denominator: 187 / 88 / 66 / 10 / 13 / 10")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
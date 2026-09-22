from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts/validate_actor_behaviour_modus_operandi.py"
REGISTRY_PATH = ROOT / "assets/data/actor-behaviour-modus-operandi-registry-v1.json"

spec = importlib.util.spec_from_file_location("actor_mo_validator", VALIDATOR_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def _data() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def test_registry_passes_fail_closed_validator() -> None:
    assert module.validate(_data()) == []


def test_machine_ids_are_namespaced_from_source_markers() -> None:
    data = _data()
    fmmm = data["actors"]["FMMM"]["markers"][0]
    assert fmmm["source_marker"] == "FMMM-01"
    assert fmmm["machine_id"] == "MO-FMMM-01"
    all_ids = [
        marker["machine_id"]
        for actor in data["actors"].values()
        for marker in actor["markers"]
    ]
    assert len(all_ids) == len(set(all_ids))


def test_recurrence_gate_remains_evidence_led() -> None:
    recurrence = _data()["recurrence"]
    assert recurrence["minimum_shared_operational_markers"] == 3
    assert recurrence["requires_independent_actor_attribution"] is True
    assert recurrence["requires_primary_or_contemporaneous_source"] is True
    assert recurrence["requires_contrary_evidence_and_legitimate_alternatives"] is True
    assert recurrence["separates_proposal_preparation_implementation_result"] is True
    assert recurrence["requires_explicit_not_a_finding_label"] is True


def test_actor_specific_counts_and_ids_are_locked() -> None:
    actors = _data()["actors"]
    assert actors["FMMM"]["person_id"] == "PD-SP-P-0009"
    assert actors["JDAM"]["person_id"] == "PD-SP-P-0011"
    assert actors["LPAM"]["person_id"] == "PD-SP-P-0012"
    assert len(actors["FMMM"]["markers"]) == 8
    assert len(actors["JDAM"]["markers"]) == 10
    assert len(actors["LPAM"]["markers"]) == 8

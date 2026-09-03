#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "assets/data/aguiar-acosta-person-event-proceeding-control-v1.json"
CARETS = ROOT / "assets/data/caepr-caret-irea-ricpe-colliers-continuity-v1.json"
PEOPLE = ROOT / "assets/data/matter-identity-registry-v1.people.json"
MASTER = ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv"

control = json.loads(CONTROL.read_text(encoding="utf-8"))
carets = json.loads(CARETS.read_text(encoding="utf-8"))
people = json.loads(PEOPLE.read_text(encoding="utf-8"))
by_person = {r["id"]: r for r in people["records"]}
with MASTER.open(encoding="utf-8-sig", newline="") as fh:
    proceedings = {r["Master_ID"]: r for r in csv.DictReader(fh)}

assert control["control_id"] == "PD-AGUIAR-CARET-EVT-PROC-20260901-01"
assert carets["event_and_proceeding_control"] == "assets/data/aguiar-acosta-person-event-proceeding-control-v1.json"

rows = {r["caepr_id"]: r for r in control["people"]}
assert set(rows) == {"PD-SP-P-0088", "PD-SP-P-0095"}
assert by_person["PD-SP-P-0088"]["name"] == "Fernando Aguiar Acosta"
assert by_person["PD-SP-P-0088"]["identity_resolution"] == "CARET_CONFIRMED"
assert by_person["PD-SP-P-0095"]["name"] == "Laura Aguiar Acosta"
assert by_person["PD-SP-P-0095"]["identity_resolution"] == "CARET_CONFIRMED"

assert len(rows["PD-SP-P-0088"]["events"]) == 4
assert len(rows["PD-SP-P-0095"]["events"]) == 2
assert {e["event_id"] for p in rows.values() for e in p["events"]} == {
    "PD-SP-EVT-FAG-2023-GRUPO-ACOSTA-MATOS",
    "PD-SP-EVT-FAG-202406-07-RICPE",
    "PD-SP-EVT-FAG-202506-08-BELAGUA-ACHM",
    "PD-SP-EVT-FAG-2026-COLLIERS-DEBT-ADVISORY",
    "PD-SP-EVT-LAA-20230201-0531-MAEC-PLACEMENT",
    "PD-SP-EVT-LAA-202407-08-CANARIAN-HOSPITALITY",
}

expected_contexts = {"GC-JUD-001", "NAT-CNMV-001", "NAT-CNMV-002"}
for person in rows.values():
    contexts = person["proceeding_contexts"]
    assert {c["master_id"] for c in contexts} == expected_contexts
    for ctx in contexts:
        assert ctx["master_id"] in proceedings
        assert ctx["person_procedural_role"] == "NO_DIRECT_PROCEDURAL_ACT_LOCATED"

assert proceedings["GC-JUD-001"]["Reference"] == "Concurso ordinario 36/2012"
assert proceedings["NAT-CNMV-001"]["Reference"] == "2024136159"
assert proceedings["NAT-CNMV-002"]["Reference"] == "2024174266"
assert "contextual navigation/records-custody links only" in control["global_boundary"]
print("Aguiar Acosta caret/event/proceeding control: PASS")

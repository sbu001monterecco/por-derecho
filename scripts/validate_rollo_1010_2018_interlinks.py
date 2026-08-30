#!/usr/bin/env python3
"""Validate the Rollo 1010/2018 identity, outcome and public interlink contract."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def records(path: str) -> dict[str, dict]:
    return {item["id"]: item for item in load(path)["records"]}


people = records("assets/data/matter-identity-registry-v1.people.json")
professionals = records("assets/data/matter-identity-registry-v1.professional-people.json")
institutions = records("assets/data/matter-identity-registry-v1.institutions.json")
proceedings = records("assets/data/matter-identity-registry-v1.proceedings.json")

require(people["PD-SP-P-0012"]["name"] == "Laura Patricia Acosta Matos", "canonical Laura identity drift")
require("Laura Isabel Acosta Matos" not in people["PD-SP-P-0012"].get("aliases", []), "source error promoted as alias")
require(institutions["PD-SP-I-0024"]["name"] == "Juzgado de Instrucción nº 2 de Arrecife", "first-instance organ drift")
require(institutions["PD-SP-I-0025"]["name"] == "Audiencia Provincial de Las Palmas — Sección Segunda", "appellate organ drift")
family = proceedings["PD-SP-R-0023"]
require(family["nig"] == "3500443220180003508", "NIG drift")
nodes = {node["master_register_id"]: node for node in family["proceeding_nodes"]}
require(nodes["LZ-JUD-003"]["child_master_register_id"] == "LZ-APP-004", "first-instance child edge missing")
require(nodes["LZ-APP-004"]["parent_master_register_id"] == "LZ-JUD-003", "appeal parent edge missing")
require(nodes["LZ-APP-004"]["decision_reference"] == "Auto 804/2018", "appeal order missing")
require(family["detail_routes"]["es"] == "/es/rollo-1010-2018-auto-804-2018/", "Spanish detail route missing")
for pid in ["PD-SP-P-0096", "PD-SP-P-0097", "PD-SP-P-0098", "PD-SP-P-0099", "PD-SP-P-0100", "PD-SP-P-0101", "PD-SP-P-0102"]:
    require(professionals[pid].get("identity_resolution") == "CARET_CONFIRMED", f"{pid} not caret-confirmed")

with (ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv").open(encoding="utf-8", newline="") as handle:
    master = {row["Master_ID"]: row for row in csv.DictReader(handle)}
require(master["LZ-JUD-003"]["Reference"] == "DP 1132/2018", "first-instance master reference drift")
require(master["LZ-JUD-003"]["Secondary_Reference"] == "Diligencias Indeterminadas 1103/2018-00 (procedural origin)", "DI reference missing")
require(master["LZ-APP-004"]["Reference"] == "Rollo 1010/2018", "appeal roll missing")
require(master["LZ-APP-004"]["Secondary_Reference"] == "Auto 804/2018", "order number missing")
require(master["LZ-APP-004"]["Parent_Master_ID"] == "LZ-JUD-003", "master parent edge missing")
require(master["LZ-JUD-003"]["Linked_Proceedings"] == "LZ-APP-004", "master backlink missing")

route_markers = {
    "es/rollo-1010-2018-auto-804-2018/index.html": ["Laura Patricia Acosta Matos", "PD-SP-P-0012", "Rollo 1010/2018", "Auto 804/2018", "Sección Segunda", "../toma-control-sun-park-7-junio-2018/#rollo-1010-2018", "../registro-maestro-procedimientos/"],
    "en/rollo-1010-2018-order-804-2018/index.html": ["Laura Patricia Acosta Matos", "PD-SP-P-0012", "Roll 1010/2018", "Order 804/2018", "Section Two", "../sun-park-takeover-7-june-2018/#rollo-1010-2018", "../master-proceedings-register/"],
    "es/toma-control-sun-park-7-junio-2018/index.html": ["id=\"rollo-1010-2018\"", "Laura Patricia Acosta Matos", "../rollo-1010-2018-auto-804-2018/"],
    "en/sun-park-takeover-7-june-2018/index.html": ["id=\"rollo-1010-2018\"", "Laura Patricia Acosta Matos", "../rollo-1010-2018-order-804-2018/"],
}
for route, markers in route_markers.items():
    text = (ROOT / route).read_text(encoding="utf-8")
    for marker in markers:
        require(marker in text, f"{route}: missing {marker}")

sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
ET.fromstring(sitemap)
for route in ("/es/rollo-1010-2018-auto-804-2018/", "/en/rollo-1010-2018-order-804-2018/"):
    require(sitemap.count(f"<loc>https://sbu001monterecco.github.io/por-derecho{route}</loc>") == 1, f"sitemap canonical-route count drift for {route}")

control = (ROOT / "archive/ROLLO_1010_2018_AUTO_804_CARET_INTERLINK_CONTROL_30AUG2026.md").read_text(encoding="utf-8")
require("11/11 source-resolved objects" in control, "release caret denominator missing")
require("not an alias" in control, "Laura source-error boundary missing")

storying = (ROOT / "archive/PROCEEDINGS_FULL_IDENTITY_STORYING_GOVERNANCE_30AUG2026.md").read_text(encoding="utf-8")
require("PROCEEDINGS_FULL_IDENTITY_STORYING_GATE" in storying, "full-identity/storying governance gate missing")
for marker in ("Rollo 1010/2018", "Auto 804/2018", "3500443220180003508", "Audiencia Provincial de Las Palmas — Sección Segunda"):
    require(marker in storying, f"full-identity/storying example missing {marker}")

print("ROLLO 1010/2018 INTERLINK CONTROL: PASS")
print("- canonical chain, NIG, organ, panel and parent/child edges verified")
print("- Laura Patricia Acosta Matos identity correction enforced")
print("- bilingual decision/context/master/prism links and sitemap verified")
print("- certified-docket and authority gaps remain visible")
print("- repository-wide full-identity and storying continuity gate verified")

#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

root = load("assets/data/matter-identity-registry-v1.json")
people = load("assets/data/matter-identity-registry-v1.la-laguna-judicial-people.json")
inst = load("assets/data/matter-identity-registry-v1.la-laguna-judicial-institutions.json")
control = load("assets/data/la-laguna-judicial-actors-canonical-interlink-control-v1.json")
gaps = load("assets/data/la-laguna-judicial-actors-gap-closure-audit-v1.json")
dp = load("assets/data/dp748-2026-canonical-interlink-control-v1.json")
prof = load("assets/data/matter-identity-registry-v1.professional-people.json")
filings = load("assets/data/counsel-filing-register-v1.json")

part_total = sum(p["count"] for p in root["parts"])
assert root["counts"]["total"] == 331 == part_total
assert root["counts"]["PERSON"] == 157
assert root["counts"]["INSTITUTION"] == 41

person_ids = {r["id"]: r for r in people["records"]}
for n in range(147, 158):
    pid = f"PD-SP-P-{n:04d}"
    assert pid in person_ids
    assert person_ids[pid]["routes"]["es"].startswith("/es/registro-judicial-la-laguna/")
    assert person_ids[pid]["routes"]["en"].startswith("/en/la-laguna-judicial-register/")

inst_ids = {r["id"]: r for r in inst["records"]}
for n in range(37, 42):
    iid = f"PD-SP-I-{n:04d}"
    assert iid in inst_ids
    assert "routes" in inst_ids[iid]

assert control["public_routes"]["es"] == "/es/registro-judicial-la-laguna/"
assert control["public_routes"]["en"] == "/en/la-laguna-judicial-register/"
assert control["certified_denominator_boundary"]

gap_ids = {g["gap_id"] for g in gaps["gaps"]}
assert gap_ids == {"LL-JUD-GAP-001", "LL-JUD-GAP-002", "LL-JUD-GAP-003"}
assert all(g["search_state"].endswith("OPEN") for g in gaps["gaps"])

app = next(p for p in control["proceedings"] if p["master_id"] == "TF-APP-004")
assert app["verification"] == "UNVERIFIED_PLACEHOLDER"
assert app["judges"] == [] and app["lajs"] == []
assert dp["professional_lineage"]["judicial"]["24_mar_signatory"]["status"] == "UNRESOLVED"

prof_ids = {r["id"] for r in prof["records"]}
assert "PD-SP-P-0146" in prof_ids
assert any(r["display_name"] == "Carlos Llamas Sanz" and len(r["filings"]) == 2 for r in filings["professional_registers"])

for rel in ["es/registro-judicial-la-laguna/index.html", "en/la-laguna-judicial-register/index.html", "es/registro-identidad-materia/index.html", "en/matter-identity-registry/index.html"]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    assert "331" in text

for rel in ["es/registro-judicial-la-laguna/index.html", "en/la-laguna-judicial-register/index.html"]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    for token in ["LL-JUD-GAP-001", "LL-JUD-GAP-002", "LL-JUD-GAP-003", "PD-SP-P-0147", "PD-SP-P-0155", "PD-SP-I-0037", "PD-SP-I-0039"]:
        assert token in text

print("La Laguna judicial register validation: PASS")

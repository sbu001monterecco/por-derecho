#!/usr/bin/env python3
"""Validate whole-perimeter counsel / legal-professional Truth Machine coverage."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
REGISTER = DATA / "legal-professionals-register-v1.json"
MACHINE = DATA / "counsel-professional-interaction-truth-machine-v1.json"
SUPPLEMENT = DATA / "legal-professionals-source-discovered-supplement-20260922.json"
PIA = DATA / "ac-professional-isolation-attrition-v1.json"
CAUS = DATA / "legal-representation-ac-causation-v1.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

reg = load(REGISTER)
tm = load(MACHINE)
sup = load(SUPPLEMENT)
pia = load(PIA)
caus = load(CAUS)
errors = []

reg_ids = [r["identity_id"] for r in reg.get("records", [])]
tm_ids = [r["identity_id"] for r in tm.get("professional_records", [])]
sup_people = sup.get("verified_professionals", [])
sup_keys = [r.get("supplement_key") for r in sup_people]

if len(reg_ids) != 40:
    errors.append(f"canonical register must remain 40 in this lane, found {len(reg_ids)}")
if len(reg_ids) != len(set(reg_ids)):
    errors.append("duplicate canonical identity_id")
if set(reg_ids) != set(tm_ids):
    errors.append(f"canonical coverage mismatch: register-only={sorted(set(reg_ids)-set(tm_ids))}; machine-only={sorted(set(tm_ids)-set(reg_ids))}")
if len(sup_people) != 9 or len(set(sup_keys)) != 9:
    errors.append("supplement must contain 9 unique professional nodes")
if sup.get("denominator", {}).get("canonical_register_records") != len(reg_ids):
    errors.append("supplement canonical denominator mismatch")
if sup.get("denominator", {}).get("combined_person_analysis_nodes") != len(reg_ids) + len(sup_people):
    errors.append("supplement combined denominator mismatch")
if tm.get("coverage", {}).get("canonical_register_covered") != len(reg_ids):
    errors.append("Truth Machine canonical coverage mismatch")
if tm.get("coverage", {}).get("supplemental_professional_nodes") != len(sup_people):
    errors.append("Truth Machine supplemental count mismatch")
if tm.get("coverage", {}).get("combined_person_analysis_nodes") != len(reg_ids) + len(sup_people):
    errors.append("Truth Machine combined person denominator mismatch")
if tm.get("coverage", {}).get("missing_identity_ids") != []:
    errors.append("Truth Machine reports missing canonical identities")
if tm.get("chronology_origin") != "GARRIGUES_2012":
    errors.append("chronology origin must be Garrigues 2012")
chron = tm.get("chronology", [])
if not chron or "Garrigues" not in chron[0].get("label", ""):
    errors.append("first canonical chronology cohort must be Garrigues")
chron_ids = {pid for cohort in chron for pid in cohort.get("identity_ids", [])}
if chron_ids != set(reg_ids):
    errors.append(f"canonical chronology coverage mismatch: missing={sorted(set(reg_ids)-chron_ids)} extra={sorted(chron_ids-set(reg_ids))}")
if tm.get("no_numeric_truth_score") is not True:
    errors.append("numeric truth scores must be disabled")
if any(r.get("truth_score") is not None for r in tm.get("professional_records", [])):
    errors.append("canonical professional truth_score must remain null")
if tm.get("canonical_entity") != "AWESWELL LIMITED" or tm.get("company_number") != "07716847":
    errors.append("canonical UK Holdco identity drift")
if tm.get("source_discovered_supplement", {}).get("path") != "assets/data/legal-professionals-source-discovered-supplement-20260922.json":
    errors.append("Truth Machine supplement binding missing")
binding = reg.get("truth_machine_binding", {})
if binding.get("control_id") != "PD-TM-COUNSEL-20260922-01":
    errors.append("canonical register Truth Machine binding missing")
if set(binding.get("applies_to_identity_ids", [])) != set(reg_ids):
    errors.append("canonical register binding does not cover all canonical IDs")
if binding.get("source_discovered_supplement") != "assets/data/legal-professionals-source-discovered-supplement-20260922.json":
    errors.append("canonical register supplement pointer missing")
for obj, name in ((pia, "PIA"), (caus, "causation")):
    b = obj.get("whole_perimeter_truth_machine") or obj.get("wholePerimeterTruthMachine") or {}
    if b.get("control_id") != "PD-TM-COUNSEL-20260922-01":
        errors.append(f"{name} reverse binding missing")
proc_count = sum(1 for r in reg.get("records", []) if "procur" in r.get("role", "").lower())
if proc_count != tm.get("coverage", {}).get("procurador_total"):
    errors.append("procurador count mismatch")
public_sup = SUPPLEMENT.read_text(encoding="utf-8")
for marker in ("mail.google.com", "gmail:", "@gmail.com", "@monterecco.com"):
    if marker in public_sup:
        errors.append(f"private source locator leaked into public supplement: {marker}")
if re.search(r"\b[0-9a-f]{16}\b", public_sup, re.I):
    errors.append("probable provider/source identifier leaked into public supplement")
if "José Manuel Niederleytner García-Lliberós" not in public_sup:
    errors.append("Niederleytner canonical source-confirmed identity missing")
if "Leopoldo Cólogan Rodríguez de Azero" not in public_sup:
    errors.append("Cólogan canonical source-confirmed identity missing")
if "Tomás González Jorge" not in public_sup:
    errors.append("Tomás González Jorge source-confirmed node missing")
if "Juan Manuel Niederleiter" in public_sup and "supersed" not in public_sup.lower():
    errors.append("superseded Niederleytner shorthand not clearly corrected")

if errors:
    raise SystemExit("\n".join("FAIL: " + e for e in errors))

print(
    "PASS PD-TM-COUNSEL-20260922-01: "
    f"{len(reg_ids)} canonical + {len(sup_people)} supplemental = "
    f"{len(reg_ids)+len(sup_people)} person nodes; "
    "Garrigues 2012 origin; no numeric truth score."
)

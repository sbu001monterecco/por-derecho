#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "assets/data/legal-professionals-register-v1.json"
MACHINE = ROOT / "assets/data/counsel-professional-interaction-truth-machine-v1.json"
PIA = ROOT / "assets/data/ac-professional-isolation-attrition-v1.json"\nSUPPLEMENT = ROOT / "assets/data/legal-professionals-source-discovered-supplement-20260922.json"
CAUS = ROOT / "assets/data/legal-representation-ac-causation-v1.json"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

reg, tm, pia, caus, sup = map(load, (REGISTER, MACHINE, PIA, CAUS, SUPPLEMENT))
errors = []

reg_ids = [r["identity_id"] for r in reg["records"]]
tm_ids = [r["identity_id"] for r in tm["professional_records"]]

if len(reg_ids) != len(set(reg_ids)):
    errors.append("duplicate identity_id in legal professionals register")
if len(tm_ids) != len(set(tm_ids)):
    errors.append("duplicate identity_id in Truth Machine")
if set(reg_ids) != set(tm_ids):
    errors.append(f"coverage mismatch: register-only={sorted(set(reg_ids)-set(tm_ids))}; machine-only={sorted(set(tm_ids)-set(reg_ids))}")
if reg.get("truth_machine_binding",{}).get("control_id") != "PD-TM-COUNSEL-20260922-01":
    errors.append("professional register Truth Machine binding missing")
if set(reg.get("truth_machine_binding",{}).get("applies_to_identity_ids",[])) != set(reg_ids):
    errors.append("professional register binding does not cover all identity IDs")
if tm.get("coverage",{}).get("covered_total") != len(reg_ids):
    errors.append("machine covered_total does not equal register total")
if tm.get("coverage",{}).get("missing_identity_ids") != []:
    errors.append("machine reports missing identities")
if tm.get("chronology_origin") != "GARRIGUES_2012":
    errors.append("chronology origin must be Garrigues 2012")
chron = tm.get("chronology",[])
if not chron or "Garrigues" not in chron[0].get("label",""):
    errors.append("first chronology cohort must be Garrigues")
chron_ids = {i for c in chron for i in c.get("identity_ids",[])}
if chron_ids != set(reg_ids):
    errors.append(f"chronology coverage mismatch: missing={sorted(set(reg_ids)-chron_ids)} extra={sorted(chron_ids-set(reg_ids))}")
if tm.get("no_numeric_truth_score") is not True:
    errors.append("numeric truth scores must be disabled")
if any(r.get("truth_score") is not None for r in tm.get("professional_records",[])):
    errors.append("professional truth_score must remain null")
if tm.get("canonical_entity") != "AWESWELL LIMITED" or tm.get("company_number") != "07716847":
    errors.append("canonical UK Holdco identity drift")
for obj,name in ((pia,"PIA"),(caus,"causation")):
    b=obj.get("whole_perimeter_truth_machine") or obj.get("wholePerimeterTruthMachine") or {}
    if b.get("control_id") != "PD-TM-COUNSEL-20260922-01":
        errors.append(f"{name} reverse binding missing")
proc_count=sum(1 for r in reg["records"] if "procur" in r.get("role","").lower())
if proc_count != tm.get("coverage",{}).get("procurador_total"):
    errors.append("procurador count mismatch")

if errors:
    raise SystemExit("\n".join("FAIL: "+e for e in errors))
print(f"PASS PD-TM-COUNSEL-20260922-01: {len(reg_ids)} canonical + {len(sup_people)} supplemental professional nodes; Garrigues 2012 origin; no numeric truth score.")

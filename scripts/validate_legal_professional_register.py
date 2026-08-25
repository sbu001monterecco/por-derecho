#!/usr/bin/env python3
"""Validate the authorised Por Derecho lawyers/procuradores register."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
INDEX = DATA / "matter-identity-registry-v1.json"
REGISTER = DATA / "legal-professionals-register-v1.json"
AUTHORIZATION = ROOT / ".github" / "governance" / "records" / "LEGAL_PROFESSIONAL_REGISTER_AUTHORIZATION_20260825.md"

ALAS_REQUIRED = {
    "PD-SP-P-0041", "PD-SP-P-0042", "PD-SP-P-0043", "PD-SP-P-0044",
    "PD-SP-P-0045", "PD-SP-P-0055", "PD-SP-P-0073", "PD-SP-P-0074",
}
PROCURADOR_REQUIRED = {"PD-SP-P-0056", "PD-SP-P-0067", "PD-SP-P-0083", "PD-SP-P-0084", "PD-SP-P-0085", "PD-SP-P-0086"}
NEW_PROFESSIONAL_REQUIRED = {f"PD-SP-P-{n:04d}" for n in range(67, 83)}
PROHIBITED_ROSTER_NAMES = {"Guillermo Suárez Lacone", "Elisa Prieto", "Mª Natividad Heredia Marcos", "Yanira Alvarez"}
REQUIRED_ORGANISATIONS = {"Sixto Abogados", "Carlos Llamas Legal Compliance", "Gallego Abogados", "DWF-RCD / Rousaud Costas Duran professional perimeter", "Del Rosal, Adame & Segrelles", "DPM Abogados"}
ALLOWED_CLASSIFICATIONS = {"OUR_CURRENT_PROFESSIONAL", "OUR_FORMER_PROFESSIONAL"}
ALLOWED_TRACKS = {"CURRENT_COUNSEL", "FORMER_COUNSEL", "FORMER_COUNSEL_COLLABORATOR", "FORMER_COUNSEL_ROLE_REVIEW", "PROCURADOR_CURRENT", "PROCURADOR_FORMER"}

def load(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def fail(message: str): raise AssertionError(message)
def require(condition: bool, message: str):
    if not condition: fail(message)

def main() -> int:
    try:
        index = load(INDEX); reg = load(REGISTER)
        require(reg.get("schema") == "por-derecho.legal-professionals-register.v1", "unexpected professional-register schema")
        require(reg.get("register_id") == "PD-SP-LEGAL-PROF-001", "unexpected professional-register ID")
        require(reg.get("authorization_reference") == "USER-2026-08-25-FULLEST-LEGAL-PROFESSIONAL-LIST", "missing controlling authorization reference")
        parts=[]
        for descriptor in index.get("parts", []):
            path=DATA/descriptor["path"]; require(path.is_file(),f"missing identity part {descriptor['path']}")
            payload=load(path); records=payload.get("records",[]); require(len(records)==descriptor.get("count"),f"part count mismatch: {descriptor['path']}"); parts.extend(records)
        identities={r["id"]:r for r in parts}; require(len(identities)==len(parts),"duplicate immutable identity ID")
        counts=index.get("counts",{})
        require(counts.get("total")==187 and counts.get("PERSON")==88 and counts.get("ORGANISATION")==66,"canonical registry counts do not reflect professional roster plus authorised non-professional actor extension")
        require(len(parts)==187,"canonical registry part total is not 187")
        # The professional roster itself remains fixed and independent of later actor extensions.
        records=reg.get("records",[]); require(len(records)==40,"professional roster must remain 40 records")
        ids=[r.get("identity_id") for r in records]; require(len(ids)==len(set(ids)),"duplicate professional roster ID")
        for rid in ids: require(rid in identities,f"professional roster references unknown identity {rid}")
        require(ALAS_REQUIRED.issubset(set(ids)),"required historic counsel set incomplete")
        require(PROCURADOR_REQUIRED.issubset(set(ids)),"required procurador set incomplete")
        require(NEW_PROFESSIONAL_REQUIRED.issubset(set(identities)),"professional identity extension incomplete")
        names={r.get("public_name") for r in records}; require(not (names & PROHIBITED_ROSTER_NAMES),"prohibited or unverified roster name present")
        org_names={r.get("name") for r in identities.values() if r.get("type")=="ORGANISATION"}; require(REQUIRED_ORGANISATIONS.issubset(org_names),"required professional organisations missing")
        current=[r for r in records if r.get("track")=="CURRENT_COUNSEL"]; require(len(current)==3,"current lawyer count must remain 3")
        current_procuradoras=[r for r in records if r.get("track")=="PROCURADOR_CURRENT"]; require(len(current_procuradoras)==2,"current procuradora count must remain 2")
        for record in records:
            require(record.get("classification") in ALLOWED_CLASSIFICATIONS,f"invalid classification {record.get('identity_id')}")
            require(record.get("track") in ALLOWED_TRACKS,f"invalid track {record.get('identity_id')}")
            if record.get("track","").startswith("PROCURADOR"):
                role=(record.get("role") or "").casefold(); require("lawyer" not in role and "abogado" not in role,f"procurador track carries lawyer role: {record.get('identity_id')}")
        require(AUTHORIZATION.is_file(),"missing professional-register authorization record")
    except AssertionError as exc:
        print(f"LEGAL PROFESSIONAL REGISTER: FAIL\n - {exc}",file=sys.stderr); return 1
    print("LEGAL PROFESSIONAL REGISTER: PASS")
    print(f" - canonical identities: {len(parts)}")
    print(f" - professional roster unchanged: {len(records)}")
    print(" - current lawyers: 3; current procuradoras: 2")
    print(" - non-professional Acosta Matos actor extension does not alter professional classification")
    return 0
if __name__ == "__main__": raise SystemExit(main())
#!/usr/bin/env python3
"""Validate the synchronized Por Derecho specialist and operational control planes."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
EXPECTED = {"total":185,"PERSON":86,"ORGANISATION":66,"STRUCTURE":10,"INSTITUTION":13,"PROCEEDING":10}


def load(path: Path):
    try:
        value=json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AssertionError(f"cannot parse {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value,dict):
        raise AssertionError(f"{path.relative_to(ROOT)} root must be object")
    return value


def require(ok: bool, message: str):
    if not ok: raise AssertionError(message)


def markers(path: str, required: list[str], forbidden: list[str]|None=None):
    p=ROOT/path; require(p.is_file(),f"missing {path}"); text=p.read_text(encoding="utf-8")
    for item in required: require(item in text,f"missing {item!r} in {path}")
    for item in forbidden or []: require(item not in text,f"stale {item!r} in {path}")
    return text


def main()->int:
    try:
        index=load(DATA/"matter-identity-registry-v1.json")
        require(index.get("counts")==EXPECTED,f"identity counts drift: {index.get('counts')}")
        ids=set(); actual={key:0 for key in EXPECTED if key!="total"}
        for desc in index.get("parts",[]):
            part=load(DATA/desc["path"]); rows=part.get("records",[])
            require(len(rows)==desc["count"],f"part count mismatch: {desc['path']}")
            for row in rows:
                rid=row.get("id"); require(rid and rid not in ids,f"duplicate/empty identity: {rid}")
                ids.add(rid); actual[row["type"]]+=1
        require(len(ids)==185 and actual=={k:EXPECTED[k] for k in actual},"identity-part totals drift")

        markers("es/registro-identidad-materia/index.html",[
            'data-static-registry-counts="185-86-66-10-13-10"','data-registry-stat="TOTAL">185','../../ops/CURRENT_UNITARY_STATE.json'],
            ['data-registry-stat="TOTAL">159'])
        markers("en/matter-identity-registry/index.html",[
            'data-static-registry-counts="185-86-66-10-13-10"','data-registry-stat="TOTAL">185','../../ops/CURRENT_UNITARY_STATE.json'],
            ['data-registry-stat="TOTAL">159'])

        updates=load(DATA/"material-updates-v1.json")
        require(updates.get("control_id")=="PD-MATERIAL-UPDATES-001","material-updates ID drift")
        require(updates.get("latest_material_date")=="2026-08-25","material-update date drift")
        require(len(updates.get("entries",[]))>=4,"material update source too small")
        markers("es/actualizaciones/index.html",["Última actualización material","<strong>25 agosto 2026</strong>"])
        markers("en/updates/index.html",["Latest material update","<strong>25 August 2026</strong>"])

        unitary=load(ROOT/"ops/CURRENT_UNITARY_STATE.json")
        require(unitary.get("schema")=="por-derecho.current-unitary-state.v1","unitary schema drift")
        require(unitary.get("control_id")=="PD-UNITARY-STATE-20260825-01","unitary control ID drift")
        require(unitary.get("identity_registry",{}).get("counts")==EXPECTED,"unitary identity counts drift")
        require(unitary.get("material_updates",{}).get("latest_material_date")=="2026-08-25","unitary update date drift")
        require(re.fullmatch(r"[0-9a-f]{40}",unitary.get("repository",{}).get("source_merge_sha","")) is not None,"unitary merge SHA missing")
        require(unitary.get("repository",{}).get("operational_truth")=="ops/CURRENT_STATE.json","unitary operational pointer missing")

        current=load(ROOT/"ops/CURRENT_STATE.json")
        require(current.get("schema")=="por-derecho.operational-truth.current-state.v2","operational current-state schema drift")
        routing=current.get("specialist_state_routing",{})
        require(routing.get("unitary_case_and_evidence_state")=="ops/CURRENT_UNITARY_STATE.json","operational→unitary routing missing")
        require("Neither substitutes" in routing.get("rule",""),"two-layer non-substitution rule missing")
        require(current.get("corpus",{}).get("identity_registry",{}).get("counts")==EXPECTED,"operational identity counts drift")

        production=load(ROOT/"ops/PRODUCTION_STATUS.json")
        require(production.get("schema")=="por-derecho.operational-truth.production-status.v2","production schema drift")
        require(production.get("specialist_state_routing",{}).get("unitary_case_and_evidence_state")=="ops/CURRENT_UNITARY_STATE.json","production→unitary routing missing")
        require(production.get("deployment",{}).get("conclusion")=="success","observed Pages deployment is not successful")
        require(production.get("verification",{}).get("exact_route_content_verification")=="NOT_RECORDED_FOR_THIS_SHA","readback boundary overstated")

        ledger=load(ROOT/"ops/PR_RECONCILIATION_LEDGER.json")
        require(isinstance(ledger.get("open_pull_request_count"),int),"PR ledger count missing")
        entries={item["pr"]:item for item in ledger.get("priority_entries",[])}
        require(entries.get(1016,{}).get("state")=="REBUILD_ON_CURRENT_MAIN","PR #1016 control missing")
        require(entries.get(771,{}).get("state")=="EXTRACT_UNIQUE_DELTA","262-finca control missing")

        markers("sitemap-unitary-control-plane.xml",["registro-identidad-materia","matter-identity-registry","<lastmod>2026-08-25</lastmod>"])
        markers("robots.txt",["sitemap-unitary-control-plane.xml","sitemap-prescription-recovery.xml"])
        markers("CURRENT_UNITARY_STATE.md",["PD-UNITARY-STATE-20260825-01","185","PR #1016"])
        manifest=load(ROOT/"publication-manifests/unitary-control-plane-sync-20260825.json")
        require(manifest.get("current_state") in {"PR_OPEN","DEPLOYED","LIVE_VERIFIED"},"unitary manifest state invalid")
        require(manifest.get("control_id")==unitary.get("control_id"),"manifest/unitary control mismatch")
    except AssertionError as exc:
        print(f"UNITARY CONTROL PLANE: FAIL\n - {exc}",file=sys.stderr); return 1
    print("UNITARY CONTROL PLANE: PASS")
    print(" - operational repository/deployment truth and specialist case/evidence state remain separate")
    print(" - identity denominator: 185 / 86 / 66 / 10 / 13 / 10")
    print(" - PR #1016 remains rebuild-on-current-main")
    return 0

if __name__=="__main__": raise SystemExit(main())

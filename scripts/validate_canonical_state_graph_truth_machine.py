#!/usr/bin/env python3
"""Validate the progressive canonical state-graph overlay.

This validator proves internal referential integrity and explicit gap handling.
It does not certify that the historical corpus, court docket or actor universe is complete.
"""

from __future__ import annotations
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTROL = ROOT / "assets/data/canonical-state-graph-overlay-v1.json"

PATHS = {
    "people": ROOT / "assets/data/matter-identity-registry-v1.people.json",
    "organisations": ROOT / "assets/data/matter-identity-registry-v1.organisations.json",
    "institutions": ROOT / "assets/data/matter-identity-registry-v1.institutions.json",
    "proceedings": ROOT / "assets/data/matter-identity-registry-v1.proceedings.json",
    "complete": ROOT / "assets/data/concurso36-complete-record-v1.json",
    "court_file": ROOT / "assets/data/concurso36-court-file-v1.json",
    "decision_continuity": ROOT / "assets/data/concurso36-decision-continuity-2014-2026-v1.json",
    "binary_register": ROOT / "archive/CONCURSO_36_2012_CANONICAL_COURT_BINARY_REGISTER_17AUG2026.md",
    "judicial_laj_register": ROOT / "archive/CONCURSO_36_2012_JUDICIAL_LAJ_ACTS_MASTER_REGISTER_17AUG2026.md",
}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def records(payload):
    if isinstance(payload, list):
        return payload
    for key in ("records","items"):
        if isinstance(payload.get(key), list):
            return payload[key]
    return []

def fail(msg, failures):
    failures.append(msg)

def main():
    failures=[]
    ctl=load(CONTROL)
    if ctl.get("control_id")!="PD-CANONICAL-STATE-GRAPH-20260926-01":
        fail("unexpected control_id",failures)
    if ctl.get("completeness_claim_permitted") is not False:
        fail("completeness must remain false until certified denominator/orphan closure",failures)

    people={r["id"] for r in records(load(PATHS["people"]))}
    orgs={r["id"] for r in records(load(PATHS["organisations"]))}
    inst={r["id"] for r in records(load(PATHS["institutions"]))}
    procs={r["id"] for r in records(load(PATHS["proceedings"]))}
    complete={r.get("canonical_id") for r in records(load(PATHS["complete"]))}
    court={r.get("id") for r in records(load(PATHS["court_file"]))}
    continuity={r.get("id") for r in records(load(PATHS["decision_continuity"]))}
    binary_text=(PATHS["binary_register"].read_text(encoding="utf-8") + "\n" +
                 PATHS["judicial_laj_register"].read_text(encoding="utf-8"))

    gap_ids=[g.get("id") for g in ctl.get("open_gaps",[])]
    if len(gap_ids)!=len(set(gap_ids)) or any(not x for x in gap_ids):
        fail("open gap IDs must be unique and non-empty",failures)
    gap_set=set(gap_ids)

    event_ids=[]
    record_refs=set()
    for ev in ctl.get("critical_chain",[]):
        eid=ev.get("graph_event_id")
        event_ids.append(eid)
        if not eid:
            fail("event missing graph_event_id",failures)
        if ev.get("proceeding_id") not in procs:
            fail(f"{eid}: unresolved proceeding_id {ev.get('proceeding_id')}",failures)
        if ev.get("institution_id") not in inst:
            fail(f"{eid}: unresolved institution_id {ev.get('institution_id')}",failures)
        for edge in ev.get("actor_edges",[]):
            if edge.get("actor_id") not in people:
                fail(f"{eid}: unresolved actor {edge.get('actor_id')}",failures)
            if not edge.get("relation") or not edge.get("capacity"):
                fail(f"{eid}: actor edge lacks relation/capacity",failures)
        for edge in ev.get("organisation_edges",[]):
            if edge.get("organisation_id") not in orgs:
                fail(f"{eid}: unresolved organisation {edge.get('organisation_id')}",failures)
            if not edge.get("relation"):
                fail(f"{eid}: organisation edge lacks relation",failures)
        for edge in ev.get("institution_edges",[]):
            if edge.get("institution_id") not in inst:
                fail(f"{eid}: unresolved linked institution {edge.get('institution_id')}",failures)
            if not edge.get("relation"):
                fail(f"{eid}: institution edge lacks relation",failures)
        for rid in ev.get("record_ids",[]):
            record_refs.add(rid)
            resolved = rid in complete or rid in court or rid in continuity or rid in binary_text
            if not resolved:
                fail(f"{eid}: record ID not resolved in canonical record/court-file/continuity/binary registers: {rid}",failures)
        for gid in ev.get("open_gap_ids",[]):
            if gid not in gap_set:
                fail(f"{eid}: unknown open gap {gid}",failures)

    if len(event_ids)!=len(set(event_ids)):
        fail("duplicate graph_event_id",failures)

    required={
        "PD-SP-EVT-C36-2012-06-06-OPENING",
        "PD-SP-EVT-C36-2017-03-22-OPEN-CONVENIO",
        "PD-SP-EVT-C36-2017-04-27-CONVENIO-PACKAGE",
        "PD-SP-EVT-C36-2017-06-28-JUNTA-STATE",
        "PD-SP-EVT-C36-2017-12-19-LIQUIDATION",
        "PD-SP-EVT-C36-2018-01-18-AC-PLAN",
        "PD-SP-EVT-C36-2018-04-16-PLAN-APPROVAL",
        "PD-SP-EVT-C36-2018-06-26-PARTIAL-SUSPENSION",
    }
    missing=required-set(event_ids)
    if missing:
        fail("missing required critical-chain events: "+", ".join(sorted(missing)),failures)

    required_gaps={
        "GAP-C36-2017-JUNTA-PRIMARY",
        "GAP-C36-LIQUIDATION-DECISION-PROVENANCE",
        "GAP-CANONICAL-REMAINING-PEOPLE-IDS",
        "GAP-CANONICAL-TYPED-BACKLINK-BACKFILL",
        "GAP-CANONICAL-CERTIFIED-DENOMINATOR",
    }
    if not required_gaps.issubset(gap_set):
        fail("critical recursive gaps were dropped",failures)

    if failures:
        print("CANONICAL STATE GRAPH VALIDATION FAILED")
        for item in failures:
            print(" -",item)
        return 1
    print(f"CANONICAL STATE GRAPH OK: {len(event_ids)} critical events; {len(gap_ids)} explicit gaps; completeness not certified")
    return 0

if __name__=="__main__":
    sys.exit(main())

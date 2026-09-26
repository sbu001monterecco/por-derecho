#!/usr/bin/env python3
"""Validate the progressive canonical state-graph overlay.

This validator proves internal referential integrity and explicit gap handling.
It does not certify that the historical corpus, court docket or actor universe is complete.
"""

from __future__ import annotations
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTROL = ROOT / "assets/data/canonical-state-graph-overlay-v1.json"
HISTORY = ROOT / "assets/data/sun-park-historical-state-graph-1987-2011-v1.json"

PATHS = {
    "identity_index": ROOT / "assets/data/matter-identity-registry-v1.json",
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
    for key in ("records","items","rows"):
        if isinstance(payload.get(key), list):
            return payload[key]
    return []

def fail(msg, failures):
    failures.append(msg)

def canonical_identity_records():
    index = load(PATHS["identity_index"])
    rows = []
    for part in index.get("parts", []):
        rel = ROOT / "assets/data" / part["path"]
        rows.extend(records(load(rel)))
    return rows

def main():
    failures=[]
    ctl=load(CONTROL)
    hist=load(HISTORY)
    if ctl.get("control_id")!="PD-CANONICAL-STATE-GRAPH-20260926-01":
        fail("unexpected control_id",failures)
    if ctl.get("completeness_claim_permitted") is not False:
        fail("completeness must remain false until certified denominator/orphan closure",failures)
    if hist.get("control_id")!="PD-SP-HISTORY-STATE-GRAPH-1987-2011-20260926":
        fail("historical prequel control_id missing or changed",failures)
    prequel=ctl.get("historical_prequel",{})
    if prequel.get("path")!="assets/data/sun-park-historical-state-graph-1987-2011-v1.json":
        fail("canonical state graph must retain historical prequel pointer",failures)

    identities=canonical_identity_records()
    people={r["id"] for r in identities if r.get("type")=="PERSON"}
    orgs={r["id"] for r in identities if r.get("type")=="ORGANISATION"}
    inst={r["id"] for r in identities if r.get("type")=="INSTITUTION"}
    procs={r["id"] for r in identities if r.get("type")=="PROCEEDING"}
    org_by_id={r["id"]:r for r in identities if r.get("type")=="ORGANISATION"}

    if "PD-SP-O-0085" not in orgs or "PD-SP-O-0099" not in orgs:
        fail("JSP and Multimatrix canonical organisation nodes must remain in the canonical identity shards",failures)
    if "PD-SP-P-0166" not in people:
        fail("José Sánchez Rodríguez canonical person node missing from canonical identity shards",failures)

    aw=org_by_id.get("PD-SP-O-0001",{})
    if aw.get("name")!="AWESWELL LIMITED" or aw.get("company_number")!="07716847":
        fail("AWESWELL canonical legal-person identity drift",failures)
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


    # Historical prequel / phase-freeze integrity.
    structures={x.get("id") for x in hist.get("structures",[])}
    objectives={x.get("id") for x in hist.get("objectives",[])}
    sources={x.get("id") for x in hist.get("source_controls",[])}
    if len(structures)!=len(hist.get("structures",[])) or None in structures:
        fail("historical structure IDs must be unique and non-empty",failures)
    if len(objectives)!=len(hist.get("objectives",[])) or None in objectives:
        fail("historical objective IDs must be unique and non-empty",failures)
    if len(sources)!=len(hist.get("source_controls",[])) or None in sources:
        fail("historical source IDs must be unique and non-empty",failures)

    hist_event_ids=[]
    for phase in hist.get("phase_freezes",[]):
        for oid in phase.get("organisation_ids",[]):
            if oid not in orgs:
                fail(f"{phase.get('phase_id')}: unresolved organisation {oid}",failures)
        for sid in phase.get("structure_ids",[]):
            if sid not in structures:
                fail(f"{phase.get('phase_id')}: unresolved structure {sid}",failures)
        obj=phase.get("objective_id")
        if obj and obj not in objectives:
            fail(f"{phase.get('phase_id')}: unresolved objective {obj}",failures)
        for src in phase.get("source_ids",[]):
            if src not in sources:
                fail(f"{phase.get('phase_id')}: unresolved source {src}",failures)
        for ev in phase.get("events",[]):
            eid=ev.get("event_id")
            hist_event_ids.append(eid)
            for oid in ev.get("organisation_ids",[]):
                if oid not in orgs:
                    fail(f"{eid}: unresolved organisation {oid}",failures)
            for pid in ev.get("person_ids",[]):
                if pid not in people:
                    fail(f"{eid}: unresolved person {pid}",failures)
            for sid in ev.get("structure_ids",[]):
                if sid not in structures:
                    fail(f"{eid}: unresolved structure {sid}",failures)
            for src in ev.get("source_ids",[]):
                if src not in sources:
                    fail(f"{eid}: unresolved source {src}",failures)
    if len(hist_event_ids)!=len(set(hist_event_ids)) or any(not x for x in hist_event_ids):
        fail("historical event IDs must be unique and non-empty",failures)

    required_hist={
        "PD-SP-EVT-SP-1988-1991-CONSTRUCTION-OPENING",
        "PD-SP-EVT-SP-2008-06-AGREEMENT-MARKET-OBJECT",
        "PD-SP-EVT-SP-2008-06-18-COMPLETION-PERIMETER",
        "PD-SP-EVT-SP-2008-07-15-POST-COMPLETION-SNAPSHOT",
        "PD-SP-EVT-SP-2011-12-01-UK-HOLDCO-SUCCESSION",
        "PD-SP-EVT-SP-2012-01-03-SPANISH-PUBLICITY",
    }
    if not required_hist.issubset(set(hist_event_ids)):
        fail("historical prequel lost a required phase-transition event",failures)

    market=next((e for p in hist.get("phase_freezes",[]) for e in p.get("events",[]) if e.get("event_id")=="PD-SP-EVT-SP-2008-06-AGREEMENT-MARKET-OBJECT"),{})
    completed=next((e for p in hist.get("phase_freezes",[]) for e in p.get("events",[]) if e.get("event_id")=="PD-SP-EVT-SP-2008-06-18-COMPLETION-PERIMETER"),{})
    if "220" not in str(market.get("transaction_object_as_reported","")):
        fail("2008 whole-hotel/220-unit market object must remain explicit",failures)
    if "171" not in str(completed.get("completed_perimeter_reported","")) or "29" not in str(completed.get("completed_perimeter_reported","")):
        fail("2008 171+29 buyer-side completed perimeter must remain explicit",failures)
    if not any(g.get("id")=="GAP-SP-SAN-HOTELS-LABEL" for g in hist.get("open_gaps",[])):
        fail("unverified San Hotels label must remain an explicit source gap",failures)
    if prequel.get("handoff_event") not in set(hist_event_ids):
        fail("historical prequel handoff event does not resolve",failures)

    if failures:
        print("CANONICAL STATE GRAPH VALIDATION FAILED")
        for item in failures:
            print(" -",item)
        return 1
    print(f"CANONICAL STATE GRAPH OK: {len(hist_event_ids)} historical events + {len(event_ids)} Concurso critical events; {len(hist.get('open_gaps',[])) + len(gap_ids)} explicit gaps; completeness not certified")
    return 0

if __name__=="__main__":
    sys.exit(main())

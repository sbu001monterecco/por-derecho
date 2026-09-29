#!/usr/bin/env python3
"""Truth Machine event bus: validate immutable change envelopes and traverse review dependencies.

This control plane accelerates reopening and routing. It does not make merits,
truth, credibility, intent, guilt or liability findings.
"""
from __future__ import annotations
import json, subprocess
from collections import defaultdict, deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ALLOWED={"NEW_SOURCE","SOURCE_CHANGE","METHOD_CHANGE","CORRECTION","RELEASE_STATE_CHANGE","DEPENDENCY_CHANGE"}
LANES={"FAST","FULL","NO_PUBLIC_RELEASE"}

def blob_sha(path:Path)->str:
    return subprocess.check_output(["git","hash-object",str(path.relative_to(ROOT))],cwd=ROOT,text=True).strip()

def load_json(path:Path):
    return json.loads(path.read_text(encoding="utf-8"))

def validate_dependencies(path:Path):
    data=load_json(path); nodes={}; graph=defaultdict(set)
    if data.get("schema")!="por-derecho.truth-machine-dependencies.v1": raise ValueError("dependency schema")
    for n in data.get("nodes",[]):
        if n.get("id") in nodes: raise ValueError("duplicate dependency node")
        nodes[n["id"]]=n
    for e in data.get("edges",[]):
        if e.get("from") not in nodes or e.get("to") not in nodes: raise ValueError("unknown dependency edge endpoint")
        graph[e["from"]].add(e["to"])
    return data,nodes,graph

def traverse(starts,nodes,graph):
    seen=set(); q=deque(starts)
    while q:
        x=q.popleft()
        if x in seen: continue
        if x not in nodes: raise ValueError("unknown affected node: "+x)
        seen.add(x)
        q.extend(sorted(graph.get(x,set())-seen))
    candidates=sorted({nodes[x].get("candidate_id") for x in seen if nodes[x].get("candidate_id")})
    return sorted(seen),candidates

def validate_event(event:dict,host:str,nodes,graph):
    if event.get("schema")!="por-derecho.truth-machine-event.v1": raise ValueError("event schema")
    if event.get("event_type") not in ALLOWED: raise ValueError("event type")
    if event.get("release_lane") not in LANES: raise ValueError("release lane")
    if not event.get("event_id") or not event.get("affected_nodes"): raise ValueError("event identity/scope")
    for forbidden in ("truth_score","guilt_score","credibility_score","lie_probability"):
        if forbidden in json.dumps(event).lower(): raise ValueError("unsupported merits score field")
    pin_key=host+"_blob_sha"; refs=[]; hard=False
    for src in event.get("source_refs",[]):
        p=ROOT/src["path"]; expected=src.get(pin_key)
        if expected is None:
            refs.append({"path":src["path"],"state":"HOST_PIN_NOT_DECLARED"}); continue
        if not p.is_file():
            refs.append({"path":src["path"],"state":"MISSING"}); hard=True; continue
        actual=blob_sha(p); same=actual==expected
        refs.append({"path":src["path"],"expected":expected,"actual":actual,"state":"UNCHANGED" if same else "SOURCE_CHANGED"})
        hard |= not same
    visited,candidates=traverse(event["affected_nodes"],nodes,graph)
    return {"event_id":event["event_id"],"event_type":event["event_type"],"release_lane":event["release_lane"],
            "source_refs":refs,"dependency_nodes":visited,"reopen_candidates":candidates,
            "three_state":event["three_state"],"requires":event.get("requires",[]),
            "hard_integrity_problem":hard,"automatic_merits_promotion":False}

def run(event_dir:Path,dependency_file:Path,host:str):
    _,nodes,graph=validate_dependencies(dependency_file)
    files=sorted(event_dir.glob("TM-EVT-*.json")); seen=set(); rows=[]; hard=False
    for p in files:
        e=load_json(p)
        if e.get("event_id") in seen: raise ValueError("duplicate event id")
        seen.add(e.get("event_id")); row=validate_event(e,host,nodes,graph); hard|=row["hard_integrity_problem"]; rows.append(row)
    return {"schema":"por-derecho.truth-machine-event-bus.report.v1","host":host,"event_count":len(rows),
            "events":rows,"hard_integrity_problem":hard,
            "boundary":"Events route work and reopen dependencies; they do not create evidential corroboration or merits findings."}

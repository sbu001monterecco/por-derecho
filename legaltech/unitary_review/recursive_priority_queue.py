#!/usr/bin/env python3
"""Fail-closed recursive queue verifier and deterministic triage.

This is an activation/control-plane tool. It validates exact queued source blobs,
reopens candidates when bytes change, and applies bounded lexical candidate cues
to text sources. It does not make truth, intent, credibility, guilt or liability
findings and it does not mutate evidence or public pages.
"""
from __future__ import annotations
import argparse,json,re,subprocess
from collections import Counter
from pathlib import Path
from legaltech.unitary_review.context_integrity import candidate_cues

ROOT=Path(__file__).resolve().parents[2]

def blob_sha(path:Path)->str:
    return subprocess.check_output(["git","hash-object",str(path.relative_to(ROOT))],cwd=ROOT,text=True).strip()

def units(text:str):
    chunks=[]
    for para in re.split(r"\n\s*\n",text):
        para=para.strip()
        if not para: continue
        parts=re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÜÑ0-9«“])",para)
        chunks.extend(x.strip() for x in parts if x.strip())
    return chunks

def scan(path:Path):
    if path.suffix.lower() not in {".md",".txt",".html",".json",".js"}:
        return {"scannable":False}
    text=path.read_text(encoding="utf-8",errors="replace")
    us=units(text)
    flagged=0; marks=0; rules=Counter()
    for u in us:
        cues=candidate_cues(u)
        if cues: flagged+=1
        marks+=len(cues)
        for c in cues: rules[c["rule_id"]]+=1
    return {"scannable":True,"units":len(us),"flagged_units":flagged,
            "marker_instances":marks,"rule_counts":dict(sorted(rules.items()))}

def run(manifest:Path):
    data=json.loads(manifest.read_text(encoding="utf-8"))
    seen=set(); ranks=[]; rows=[]; hard=False
    for c in data["candidates"]:
        if c["id"] in seen: raise ValueError("duplicate candidate id")
        seen.add(c["id"]); ranks.append(c["rank"])
        srcs=[]; changed=False; missing=False
        for s in c["source_paths"]:
            p=ROOT/s["path"]
            if not p.is_file():
                srcs.append({"path":s["path"],"state":"MISSING"}); missing=True; hard=True; continue
            actual=blob_sha(p); same=actual==s["git_blob_sha"]
            if not same: changed=True; hard=True
            srcs.append({"path":s["path"],"expected_blob_sha":s["git_blob_sha"],
                         "actual_blob_sha":actual,"state":"UNCHANGED" if same else "SOURCE_CHANGED",
                         "triage":scan(p)})
        state="BLOCKED_MISSING_SOURCE" if missing else "REVIEW_REQUIRED_SOURCE_CHANGED" if changed else c["status"]
        rows.append({"rank":c["rank"],"id":c["id"],"title":c["title"],"mode":c["mode"],
                     "queue_state":state,"next_action":c["next_action"],"sources":srcs,
                     "automatic_merits_promotion":False})
    if sorted(ranks)!=ranks or len(ranks)!=len(set(ranks)): raise ValueError("ranks must be unique and ordered")
    return {"schema":"por-derecho.truth-machine-priority-queue.report.v1",
            "control":data["control"],"candidates":rows,
            "hard_integrity_problem":hard,
            "boundary":"Candidate cues and source-change signals are triage only; no truth, lie, credibility, intent, guilt or liability score."}

def main():
    p=argparse.ArgumentParser();p.add_argument("--manifest",default="assets/data/truth-machine-priority-queue-v1.json");p.add_argument("--output")
    a=p.parse_args();report=run(ROOT/a.manifest)
    raw=json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+"\n"
    if a.output: Path(a.output).write_text(raw,encoding="utf-8")
    print(raw,end="")
    raise SystemExit(2 if report["hard_integrity_problem"] else 0)

if __name__=="__main__": main()

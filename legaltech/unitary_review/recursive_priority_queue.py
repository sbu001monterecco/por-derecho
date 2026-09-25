#!/usr/bin/env python3
"""Fail-closed recursive queue verifier and deterministic triage.

Validates host-specific exact source blobs, reports mirror gaps without inventing
parity, and applies bounded candidate cues to readable text. It never promotes
truth, intent, credibility, guilt or liability and never mutates evidence.
"""
from __future__ import annotations
import argparse,json,os,re,subprocess
from collections import Counter
from pathlib import Path
from legaltech.unitary_review.context_integrity import candidate_cues

ROOT=Path(__file__).resolve().parents[2]

def detect_host():
    if os.environ.get("GITLAB_CI"): return "gitlab"
    if os.environ.get("GITHUB_ACTIONS"): return "github"
    return "github"

def blob_sha(path:Path)->str:
    return subprocess.check_output(["git","hash-object",str(path.relative_to(ROOT))],cwd=ROOT,text=True).strip()

def units(text:str):
    out=[]
    for para in re.split(r"\n\s*\n",text):
        para=para.strip()
        if not para: continue
        out.extend(x.strip() for x in re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÜÑ0-9«“])",para) if x.strip())
    return out

def scan(path:Path):
    if path.suffix.lower() not in {".md",".txt",".html",".json",".js"}: return {"scannable":False}
    us=units(path.read_text(encoding="utf-8",errors="replace")); flagged=marks=0; rules=Counter()
    for u in us:
        cues=candidate_cues(u)
        flagged+=bool(cues); marks+=len(cues)
        for c in cues: rules[c["rule_id"]]+=1
    return {"scannable":True,"units":len(us),"flagged_units":flagged,"marker_instances":marks,
            "rule_counts":dict(sorted(rules.items()))}

def run(manifest:Path,host:str):
    data=json.loads(manifest.read_text(encoding="utf-8")); seen=set(); ranks=[]; rows=[]; hard=False
    pin_key=f"{host}_blob_sha"
    for c in data["candidates"]:
        if c["id"] in seen: raise ValueError("duplicate candidate id")
        seen.add(c["id"]); ranks.append(c["rank"]); srcs=[]; changed=missing=False; gaps=0
        for s in c["sources"]:
            expected=s.get(pin_key)
            if not expected:
                gaps+=1
                srcs.append({"path":s["path"],"state":"HOST_MIRROR_GAP","host":host,
                             "gap":s.get(f"{host}_gap","NO_REVIEWED_HOST_PIN")})
                continue
            p=ROOT/s["path"]
            if not p.is_file():
                missing=True;hard=True;srcs.append({"path":s["path"],"state":"MISSING_REQUIRED_HOST_SOURCE","host":host});continue
            actual=blob_sha(p);same=actual==expected
            changed|=not same;hard|=not same
            srcs.append({"path":s["path"],"expected_blob_sha":expected,"actual_blob_sha":actual,
                         "state":"UNCHANGED" if same else "SOURCE_CHANGED","host":host,"triage":scan(p)})
        if missing: state="BLOCKED_MISSING_REQUIRED_SOURCE"
        elif changed: state="REVIEW_REQUIRED_SOURCE_CHANGED"
        elif gaps: state=c["status"]+"+HOST_PARITY_GAP"
        else: state=c["status"]
        rows.append({"rank":c["rank"],"id":c["id"],"title":c["title"],"mode":c["mode"],
                     "queue_state":state,"next_action":c["next_action"],"sources":srcs,
                     "automatic_merits_promotion":False})
    if sorted(ranks)!=ranks or len(ranks)!=len(set(ranks)): raise ValueError("ranks must be unique and ordered")
    return {"schema":"por-derecho.truth-machine-priority-queue.report.v1","control":data["control"],"host":host,
            "candidates":rows,"hard_integrity_problem":hard,
            "boundary":"Candidate cues, mirror gaps and source-change signals are triage only; no truth, lie, credibility, intent, guilt or liability score."}

def main():
    p=argparse.ArgumentParser();p.add_argument("--manifest",default="assets/data/truth-machine-priority-queue-v1.json")
    p.add_argument("--host",choices=("github","gitlab"));p.add_argument("--output")
    a=p.parse_args();report=run(ROOT/a.manifest,a.host or detect_host())
    raw=json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+"\n"
    if a.output: Path(a.output).write_text(raw,encoding="utf-8")
    print(raw,end="");raise SystemExit(2 if report["hard_integrity_problem"] else 0)
if __name__=="__main__": main()

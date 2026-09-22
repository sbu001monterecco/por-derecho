#!/usr/bin/env python3
"""Fail-closed AWESWELL identity validator for repository and outbound drafts."""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULE = ROOT / "ops/AWESWELL_CANONICAL_NAME_RULE_27AUG2026.json"
REGISTER = ROOT / "ops/CANONICAL_ENTITY_NAMES.json"
EXCEPTIONS = ROOT / "ops/AWESWELL_IDENTITY_EXCEPTION_REGISTRY_22SEP2026.json"
TEXT_SUFFIXES = {".md",".txt",".html",".htm",".json",".jsonl",".csv",".tsv",".xml",".yml",".yaml",".py",".js",".mjs",".cjs",".css"}
DISTINCT = re.compile(r"\bOSWELL\s+426\s+S\.L\.\b", re.I)

CONTROL_DEFINITION_PATHS = {
    "ops/AWESWELL_CANONICAL_NAME_RULE_27AUG2026.json",
    "ops/AWESWELL_IDENTITY_EXCEPTION_REGISTRY_22SEP2026.json",
    "ops/CANONICAL_ENTITY_NAMES.json",
    "scripts/validate_aweswell_identity.py",
}

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def variants():
    data=load_json(RULE)
    vals=data.get("forbidden_generated_aliases",[])
    vals += ["AWESWELLL"]
    return sorted(set(vals), key=len, reverse=True)

def pattern():
    return re.compile(r"(?<![A-Za-z])(?:"+"|".join(re.escape(x) for x in variants())+r")(?![A-Za-z])", re.I)

def scan_text(text: str, label: str, allow_distinct: bool=False):
    errors=[]
    rx=pattern()
    for n,line in enumerate(text.splitlines(),1):
        for hit in rx.finditer(line):
            if allow_distinct and DISTINCT.search(line):
                continue
            errors.append(f"{label}:{n}: forbidden identity variant {hit.group(0)!r}")
    return errors

def repository_files():
    out=subprocess.check_output(["git","ls-files","-z"], cwd=ROOT)
    for raw in out.split(b"\0"):
        if not raw: continue
        p=ROOT/raw.decode()
        if p.suffix.lower() in TEXT_SUFFIXES and p.is_file():
            yield p

def validate_controls():
    errors=[]
    rule=load_json(RULE); reg=load_json(REGISTER)
    records=reg.get("records",[])
    e5=next((x for x in records if x.get("id")=="E005"),None)
    if not e5 or e5.get("identifier",{}).get("value")!="07716847":
        errors.append("canonical register E005/company 07716847 missing")
    if not e5 or e5.get("official_registered_name")!="AWESWELL LIMITED":
        errors.append("canonical register official name mismatch")
    if rule.get("entity",{}).get("official_registered_name")!="AWESWELL LIMITED":
        errors.append("canonical-name rule official name mismatch")
    return errors

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--outbound", nargs="*", help="draft files; use '-' for stdin")
    ap.add_argument("--all", action="store_true", help="scan all tracked text using controlled exceptions")
    args=ap.parse_args()
    errors=validate_controls()
    if args.outbound is not None:
        targets=args.outbound or ["-"]
        for item in targets:
            text=sys.stdin.read() if item=="-" else Path(item).read_text(encoding="utf-8")
            errors += scan_text(text,item,allow_distinct=True)
    else:
        exc={x["path"]:x["category"] for x in load_json(EXCEPTIONS).get("path_exceptions",[])}
        for p in repository_files():
            rel=p.relative_to(ROOT).as_posix()
            if rel in CONTROL_DEFINITION_PATHS or rel in exc:
                continue
            errors += scan_text(p.read_text(encoding="utf-8",errors="replace"),rel,allow_distinct=True)
    if errors:
        print("AWESWELL identity validation FAILED",file=sys.stderr)
        for e in errors: print(" - "+e,file=sys.stderr)
        return 1
    print("AWESWELL identity validation PASS")
    return 0
if __name__=="__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
import json, pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
P=ROOT/"assets/data/ministerio-fiscal-canonical-register-20260919.json"
d=json.loads(P.read_text(encoding="utf-8"))
errors=[]
def unique(section,key):
    vals=[x.get(key) for x in d[section] if x.get(key)]
    dup={v for v in vals if vals.count(v)>1}
    if dup: errors.append(f"{section}.{key} duplicates: {sorted(dup)}")
unique("offices","id"); unique("entities","id"); unique("people","id"); unique("events","id"); unique("evidence","id")
office_ids={x["id"] for x in d["offices"]}
entity_ids={x["id"] for x in d["entities"]}
people_ids={x["id"] for x in d["people"]}
evidence_ids={x["id"] for x in d["evidence"]}
file_ids={x.get("master_id") or x.get("register_id") for x in d["files"]}
for sec in ("entities","people","files"):
    for x in d[sec]:
        for oid in x.get("office_ids",[]): 
            if oid not in office_ids: errors.append(f"{sec} {x.get('id') or x.get('master_id')} unknown office {oid}")
for x in d["people"]:
    for eid in x.get("entity_ids",[]):
        if eid not in entity_ids: errors.append(f"person {x['id']} unknown entity {eid}")
    for f in x.get("file_refs",[]):
        if f not in file_ids: errors.append(f"person {x['id']} unknown file {f}")
for x in d["events"]:
    for p in x.get("person_ids",[]):
        if p not in people_ids: errors.append(f"event {x['id']} unknown person {p}")
    for e in x.get("evidence_ids",[]):
        if e not in evidence_ids: errors.append(f"event {x['id']} unknown evidence {e}")
    for f in x.get("file_refs",[]):
        if f not in file_ids: errors.append(f"event {x['id']} unknown file {f}")
pub=json.dumps(d,ensure_ascii=False)
for forbidden in ("mail.google.com/mail/","#all/","thread_id","message_id"):
    if forbidden in pub: errors.append(f"public register leaks provider locator token: {forbidden}")
if not d.get("gitlab_mirror_control",{}).get("no_blind_overwrite"):
    errors.append("GitLab no-blind-overwrite control missing")
if errors:
    print("MINISTERIO FISCAL CANONICAL REGISTER: FAIL")
    print("\n".join("- "+e for e in errors))
    sys.exit(1)
print("MINISTERIO FISCAL CANONICAL REGISTER: PASS")
print(f"offices={len(d['offices'])} entities={len(d['entities'])} people={len(d['people'])} files={len(d['files'])} events={len(d['events'])} evidence={len(d['evidence'])}")
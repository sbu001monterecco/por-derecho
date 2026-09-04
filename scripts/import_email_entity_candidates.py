#!/usr/bin/env python3
"""Validate and merge a sanitised mailbox candidate batch into the review queue."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "ops" / "legaltech-entity-evidence" / "candidate-decisions.json"
ALLOWED_HITS = {"direct_sender","direct_recipient","message_body","quoted_body","attachment_text","attachment_filename","later_derivative_summary"}
ALLOWED_CLASSES = {"PRIMARY_COMMUNICATION","ATTACHMENT_PRIMARY","QUOTED_COMMUNICATION","DERIVATIVE_ADVOCACY","UNKNOWN"}
ALLOWED_GATES = {"PRIVATE_ONLY","PRIVILEGE_REVIEW","REDACTED_METADATA_ONLY"}
FORBIDDEN_KEYS = {"body","raw_body","attachment","attachment_bytes","email","email_address","phone","phone_number"}


def load(path: Path) -> dict[str, Any]:
    value=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value,dict): raise ValueError(f"{path} must contain an object")
    return value


def validate(batch: dict[str, Any]) -> list[dict[str, Any]]:
    records=batch.get("records")
    if not isinstance(records,list): raise ValueError("batch.records must be an array")
    seen=set(); output=[]
    for row in records:
        if not isinstance(row,dict): raise ValueError("candidate must be an object")
        forbidden=FORBIDDEN_KEYS.intersection(k.lower() for k in row)
        if forbidden: raise ValueError(f"raw/sensitive keys are forbidden: {sorted(forbidden)}")
        required={"candidate_id","candidate_name","message_date","hit_location","source_class","privacy_gate","fingerprint"}
        missing=required-row.keys()
        if missing: raise ValueError(f"candidate missing fields: {sorted(missing)}")
        if row["hit_location"] not in ALLOWED_HITS: raise ValueError(f"invalid hit_location: {row['hit_location']}")
        if row["source_class"] not in ALLOWED_CLASSES: raise ValueError(f"invalid source_class: {row['source_class']}")
        if row["privacy_gate"] not in ALLOWED_GATES: raise ValueError(f"invalid privacy_gate: {row['privacy_gate']}")
        if row["fingerprint"] in seen: raise ValueError(f"duplicate fingerprint: {row['fingerprint']}")
        seen.add(row["fingerprint"]); output.append(row)
    return output


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("batch",type=Path)
    parser.add_argument("--write",action="store_true",help="merge new candidates into the governed public metadata queue")
    args=parser.parse_args()
    records=validate(load(args.batch))
    if not args.write:
        print(f"PASS sanitised mailbox batch: {len(records)} candidates")
        return
    queue=load(QUEUE)
    existing_names={row.get("candidate_name") for row in queue.get("candidates",[])}
    appended=0
    for row in records:
        if row["candidate_name"] in existing_names: continue
        queue.setdefault("candidates",[]).append({
            "candidate_id":row["candidate_id"],"candidate_name":row["candidate_name"],
            "candidate_type":"UNKNOWN","decision":"MAYBE_HOLD",
            "source_channels":["gmail-sanitised-metadata"],"hit_location":row["hit_location"],
            "reason":"Credentialed mailbox discovery only; exact identity, matter role and publication basis require review.",
            "privacy_gate":row["privacy_gate"],"fingerprint":row["fingerprint"]
        })
        existing_names.add(row["candidate_name"]); appended+=1
    QUEUE.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Merged {appended} new candidates; raw mailbox content was not accepted")


if __name__ == "__main__": main()

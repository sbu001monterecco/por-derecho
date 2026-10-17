#!/usr/bin/env python3
from pathlib import Path
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
HARD=ROOT/"archive/OUTBOUND_CANONICAL_REFERENCE_AND_PACKAGE_OBJECT_HARD_GATE_30SEP2026.md"
REQUIRED_REFERENCERS=[
    ROOT/"archive/OUTBOUND_EMAIL_COMMUNICATIONS_PROTOCOL_23AUG2026.md",
    ROOT/"archive/MAXIMUM_REACH_OUTBOUND_CAMPAIGN_LAYER_23AUG2026.md",
    ROOT/"EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md",
    ROOT/"archive/prompts/RECIPIENT_SPECIFIC_OUTBOUND_EMAIL_PREPARATION_PROMPT_23AUG2026.md",
    ROOT/"CHATGPT_START_HERE.md",
    ROOT/"AGENTS.md",
]
TOKEN="OUTBOUND_CANONICAL_REFERENCE_AND_PACKAGE_OBJECT_HARD_GATE_30SEP2026.md"
errors=[]

if not HARD.exists():
    errors.append("missing outbound canonical hard gate")

for p in REQUIRED_REFERENCERS:
    if not p.exists():
        errors.append(f"missing required control file: {p.relative_to(ROOT)}")
        continue
    if TOKEN not in p.read_text(encoding="utf-8"):
        errors.append(f"{p.relative_to(ROOT)} does not reference canonical hard gate")

template=ROOT/"ops/outbound/OUTBOUND_PACKAGE_MANIFEST_TEMPLATE.json"
if not template.exists():
    errors.append("missing outbound package manifest template")
else:
    data=json.loads(template.read_text(encoding="utf-8"))
    required={"communication_id","controlling_version","source_cutoff","message_class","audience_lane","channel_status","canonical_entity_check","material_proposition_source_map","gmail_history_gate","repository_state","attachments","links","pass_flags","approval_status"}
    missing=sorted(required-set(data))
    if missing:
        errors.append(f"manifest template missing keys: {missing}")

email_re=re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}",re.I)
gmail_id_re=re.compile(r"\b1[a-f0-9]{15,}\b",re.I)
for p in sorted((ROOT/"ops/outbound").glob("*-public-safe-manifest.json")):
    data=json.loads(p.read_text(encoding="utf-8"))
    raw=p.read_text(encoding="utf-8")
    for key in ("communication_id","status","message_class","source_cutoff","attachment","discrepancy_classification","resend_decision"):
        if key not in data:
            errors.append(f"{p.relative_to(ROOT)} missing {key}")
    if email_re.search(raw):
        errors.append(f"{p.relative_to(ROOT)} exposes an email address")
    if gmail_id_re.search(raw):
        errors.append(f"{p.relative_to(ROOT)} may expose a private Gmail/message identifier")

if errors:
    print("OUTBOUND CANONICAL CONTROL: FAIL")
    for e in errors:
        print("-",e)
    sys.exit(1)
print("OUTBOUND CANONICAL CONTROL: PASS")

#!/usr/bin/env python3
from pathlib import Path
import json
import os
import sys

ROOT=Path(__file__).resolve().parents[1]
CONTROL_ID="PD-GOV-XSYS-20260924-01"
PROTOCOL=ROOT/"governance/CROSS_SYSTEM_LIVE_COORDINATION_CONTINUITY_MEMORY_PROTOCOL_24SEP2026.md"
STATE=ROOT/"ops/live-coordination/CROSS_SYSTEM_LIVE_COORDINATION_STATE_20260924.json"
AGENTS=ROOT/"AGENTS.md"
START=ROOT/"CHATGPT_START_HERE.md"
HANDOFF=ROOT/"ops/live-coordination/HANDOFF_TEMPLATE.md"

REQUIRED_PARITY={
"EXACT_PARITY","FUNCTIONAL_PARITY","PENDING_PROPAGATION","INTENTIONAL_DIVERGENCE",
"BLOCKED","STALE","SUPERSEDED","UNKNOWN"}
REQUIRED_RULES={
"NO_SILENT_DIVERGENCE","NO_SILENT_PROMOTION","CURRENT_MAIN_BEFORE_WRITE",
"ONE_LIVE_INTEGRATION_LANE","MUTATION_RECEIPTS_REQUIRED",
"MEMORY_IS_NOT_PRIMARY_EVIDENCE","NO_ALL_UPDATED_CLAIM_WITH_UNVERIFIED_EXCEPTIONS"}

def read(path):
    if not path.exists():
        raise ValueError("Missing required file: "+str(path.relative_to(ROOT)))
    return path.read_text(encoding="utf-8")

def validate():
    errors=[]
    protocol=read(PROTOCOL)
    agents=read(AGENTS)
    start=read(START)
    handoff=read(HANDOFF)
    try:
        state=json.loads(read(STATE))
    except json.JSONDecodeError as exc:
        return {"status":"FAIL","errors":["Invalid state JSON: "+str(exc)]}
    if CONTROL_ID not in protocol:
        errors.append("Protocol missing control ID")
    if state.get("control_id")!=CONTROL_ID:
        errors.append("State control ID mismatch")
    if state.get("canonical_public_repository",{}).get("control_tower_issue")!=1428:
        errors.append("Control Tower issue must remain #1428")
    if set(state.get("parity_states",[]))!=REQUIRED_PARITY:
        errors.append("Parity-state set changed or incomplete")
    if not REQUIRED_RULES.issubset(set(state.get("absolute_rules",[]))):
        errors.append("Absolute-rule set incomplete")
    gd=state.get("google_drive",{})
    if gd.get("coordination_control_doc_state")!="READBACK_VERIFIED":
        errors.append("Drive coordination control is not READBACK_VERIFIED")
    if not gd.get("coordination_control_doc_id"):
        errors.append("Drive coordination control file ID missing")
    chatgpt=state.get("chatgpt",{})
    if chatgpt.get("memory_is_evidence") is not False or chatgpt.get("memory_proves_current_state") is not False:
        errors.append("Memory boundary weakened")
    if "PARTIAL — NOT FULLY ALIGNED" not in protocol:
        errors.append("Protocol missing partial-alignment state")
    for phrase in ("objective / scope","external actions actually completed","actions not completed","readiness state"):
        if phrase not in handoff:
            errors.append("Handoff template missing: "+phrase)
    gitlab=os.environ.get("GITLAB_CI","").lower()=="true"
    mirror=state.get("gitlab_mirror",{})
    hook_exception=(gitlab and
        mirror.get("instruction_hook_state")=="BLOCKED_BY_PROTECTED_SUCCESSOR_POLICY" and
        mirror.get("parity_state")=="FUNCTIONAL_PARITY")
    for label,body in (("AGENTS",agents),("CHATGPT_START_HERE",start)):
        if CONTROL_ID not in body and not hook_exception:
            errors.append(label+" missing "+CONTROL_ID)
    return {
      "schema":"por-derecho.cross-system-coordination-validation.v1",
      "control_id":CONTROL_ID,
      "status":"PASS" if not errors else "FAIL",
      "errors":errors,
      "gitlab_protected_hook_exception":hook_exception,
      "boundary":"Structural coordination validation only."
    }

if __name__=="__main__":
    result=validate()
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if result["errors"]:
        sys.exit(1)

#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

state_path = ROOT / "ops" / "CURRENT_STATE.json"
control_path = ROOT / ".github" / "governance" / "MULTI_THREAD_COLLABORATION_AND_PUBLICATION_V2_04SEP2026.md"
gate_path = ROOT / ".github" / "governance" / "NEW_THREAD_SCOPE_AND_CONTINUITY_GATE_02SEP2026.md"
start_path = ROOT / "CURRENT_START_HERE.md"
workflow_path = ROOT / ".github" / "workflows" / "validate-multithread-collaboration-v2.yml"

for path in (state_path, control_path, gate_path, start_path, workflow_path):
    if not path.exists():
        raise SystemExit(f"missing required collaboration control: {path.relative_to(ROOT)}")

state = json.loads(state_path.read_text(encoding="utf-8"))
if state.get("schema") != "por-derecho.current-collaboration-state.v2":
    raise SystemExit("unexpected CURRENT_STATE schema")
if state.get("control_id") != "PD-MTCP-20260904-01":
    raise SystemExit("unexpected collaboration control id")
if state.get("control_tower", {}).get("issue_number") != 1428:
    raise SystemExit("Control Tower issue must be #1428")

model = state.get("operating_model", {})
required_true = {
    "parallel_workers_allowed",
    "single_active_integrator",
    "one_logical_release_one_integration_pr_norm",
}
for key in required_true:
    if model.get(key) is not True:
        raise SystemExit(f"operating_model.{key} must be true")
if model.get("worker_may_publish_independently") is not False:
    raise SystemExit("workers must not independently publish")
if state.get("post_merge_policy", {}).get("normal_content_mutation_by_ci") is not False:
    raise SystemExit("normal post-merge CI content mutation must be false")

required_fields = {
    "task",
    "canonical_ids",
    "sources",
    "corrections",
    "new_propositions",
    "open_gaps",
    "proposed_changes",
    "conflicts_with_current_main",
    "readiness",
}
if set(state.get("worker_delta_required_fields", [])) != required_fields:
    raise SystemExit("worker delta field contract drift")

control = control_path.read_text(encoding="utf-8")
gate = gate_path.read_text(encoding="utf-8")
start = start_path.read_text(encoding="utf-8")
workflow = workflow_path.read_text(encoding="utf-8")

for token in (
    "PD-MTCP-20260904-01",
    "Issue #1428",
    "Only one integrator may coordinate publication at a time",
    "do not independently publish",
):
    if token.lower() not in control.lower():
        raise SystemExit(f"control missing required token: {token}")

for document_name, text in (("new-thread gate", gate), ("CURRENT_START_HERE", start)):
    if "PD-MTCP-20260904-01" not in text:
        raise SystemExit(f"{document_name} does not route to PD-MTCP-20260904-01")
    if "ops/CURRENT_STATE.json" not in text:
        raise SystemExit(f"{document_name} does not route to ops/CURRENT_STATE.json")

for forbidden in ("git push", "contents: write", "pull-requests: write"):
    if forbidden in workflow:
        raise SystemExit(f"validator workflow must be read-only; found {forbidden}")

print("PASS: multi-thread collaboration/publication v2 control is internally consistent")

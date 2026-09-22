#!/usr/bin/env python3
import json
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError, ValidationError
except ImportError as exc:
    raise SystemExit("Federation validation requires jsonschema==4.25.1; install the pinned dependency.") from exc

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_UNITS = {"FULL_TREE_MANIFEST","STATE_ENVELOPE","RECONCILIATION_DECISION","DEPENDENCY_REVIEW_QUEUE","CONTROL_RECEIPT","PUBLIC_PROJECTION_MANIFEST","RELEASE_ENVELOPE","LIVE_READBACK_RECEIPT"}
REQUIRED_ROLES = {"RETRIEVER","EVIDENCE_ANALYST","ADVERSARIAL_REVIEWER","INTEGRATOR","PROJECTION_REVIEWER","RELEASE_VERIFIER"}
REQUIRED_RULES = {"COMPARE_COMPLETE_MANIFESTS_NOT_API_LIMITED_DIFFS","CLASSIFY_EVERY_DIFFERENCE_BEFORE_INTEGRATION","NO_WHOLESALE_MIRROR","GREEN_BUILD_IS_NOT_DEPLOYMENT_PROOF","LIVE_READBACK_IS_SEPARATE_FROM_MERGE_AND_BUILD"}

def load(path):
    if not path.exists():
        raise ValueError(f"missing required federation file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def validate(root=ROOT):
    contract=load(root/"ops/federation/PD_FEDERATION_V1.json")
    schema=load(root/"schemas/por-derecho-federation-envelope-v1.schema.json")
    example=load(root/"ops/federation/EXAMPLE_STATE_ENVELOPE.json")
    authority=contract.get("authority_boundary",{})
    if authority.get("canonical_host_migration") is not False:
        raise ValueError("canonical host migration must remain false")
    if authority.get("blind_bidirectional_mirroring") is not False:
        raise ValueError("blind bidirectional mirroring must remain false")
    if authority.get("external_action_authority") is not False:
        raise ValueError("external action authority must remain false")
    if set(contract.get("portable_exchange_units",[])) != REQUIRED_UNITS:
        raise ValueError("portable exchange unit taxonomy drift")
    roles={row.get("role") for row in contract.get("supervised_intelligence_roles",[])}
    if roles != REQUIRED_ROLES:
        raise ValueError(f"supervised role taxonomy drift: {sorted(roles)}")
    missing=REQUIRED_RULES-set(contract.get("host_bridge_rules",[]))
    if missing:
        raise ValueError(f"missing host bridge invariants: {sorted(missing)}")
    recursion=contract.get("recursive_engine",{})
    if recursion.get("max_hops") != 32:
        raise ValueError("recursive traversal must remain bounded at 32 hops")
    if recursion.get("cycle_policy") != "FAIL_CLOSED_WITH_VISITED_SET":
        raise ValueError("recursive cycle policy must fail closed")
    if not recursion.get("predecessor_required_after_genesis"):
        raise ValueError("non-genesis predecessor chain must remain mandatory")
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise ValueError(f"federation schema invalid: {exc.message}") from exc
    try:
        Draft202012Validator(schema).validate(example)
    except ValidationError as exc:
        raise ValueError(f"example envelope invalid at {list(exc.absolute_path)}: {exc.message}") from exc
    if example["iteration"] != 0 or example.get("predecessor") is not None:
        raise ValueError("genesis example must have iteration 0 and null predecessor")
    if example["recursion"]["next_action"] == "CLOSED":
        raise ValueError("bootstrap example cannot claim the federation is closed")
    return {"portable_units":len(REQUIRED_UNITS),"roles":len(REQUIRED_ROLES),"triggers":len(recursion.get("trigger_events",[])),"max_hops":recursion["max_hops"],"example_validated":1}

def main():
    try:
        stats=validate()
    except ValueError as exc:
        raise SystemExit(f"Federation bridge: FAIL — {exc}") from exc
    print("Federation bridge: PASS")
    print(" ".join(f"{k}={v}" for k,v in stats.items()))

if __name__=="__main__":
    main()

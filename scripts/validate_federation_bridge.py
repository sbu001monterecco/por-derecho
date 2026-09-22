#!/usr/bin/env python3
import json
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError, ValidationError
except ImportError as exc:
    raise SystemExit(
        "Federation bridge: FAIL "
        "class=DEPENDENCY_MISSING path=python:jsonschema observed=unavailable "
        "expected=jsonschema==4.25.1 next=install_the_pinned_schema_validator"
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_UNITS = {
    "FULL_TREE_MANIFEST","STATE_ENVELOPE","RECONCILIATION_DECISION",
    "DEPENDENCY_REVIEW_QUEUE","CONTROL_RECEIPT","PUBLIC_PROJECTION_MANIFEST",
    "RELEASE_ENVELOPE","LIVE_READBACK_RECEIPT"
}
REQUIRED_ROLES = {
    "RETRIEVER","EVIDENCE_ANALYST","ADVERSARIAL_REVIEWER",
    "INTEGRATOR","PROJECTION_REVIEWER","RELEASE_VERIFIER"
}
REQUIRED_RULES = {
    "COMPARE_COMPLETE_MANIFESTS_NOT_API_LIMITED_DIFFS",
    "CLASSIFY_EVERY_DIFFERENCE_BEFORE_INTEGRATION",
    "NO_WHOLESALE_MIRROR",
    "GREEN_BUILD_IS_NOT_DEPLOYMENT_PROOF",
    "LIVE_READBACK_IS_SEPARATE_FROM_MERGE_AND_BUILD",
}
AUTHORITY_EXPECTED = {
    "canonical_host_migration": False,
    "blind_bidirectional_mirroring": False,
    "gitlab_role": "PRIVATE_CANONICAL_WORKING_AND_RECOVERY_AUTHORITY_SUBJECT_TO_CURRENT_REPOSITORY_CONTROLS",
    "github_role": "PUBLIC_CONTINUITY_PUBLICATION_AND_INTEGRATION_SURFACE_SUBJECT_TO_CURRENT_REPOSITORY_CONTROLS",
    "chatgpt_role": "SUPERVISED_ORCHESTRATOR_CONTINUITY_AND_RECONCILIATION",
    "live_public_host_role": "DEPLOYMENT_READBACK_AUTHORITY_ONLY",
    "external_action_authority": False,
}

def fail(failure_class, path, observed, expected, next_step):
    raise ValueError(
        f"class={failure_class} path={path} observed={observed!r} "
        f"expected={expected!r} next={next_step}"
    )

def load(path):
    if not path.exists():
        fail("MISSING_FILE", str(path), "absent", "present", "restore_or_reconcile_the_required_file")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail("INVALID_JSON", str(path), str(exc), "valid_utf8_json", "repair_without_rewriting_unrelated_content")

def validate(root=ROOT):
    contract=load(root/"ops/federation/PD_FEDERATION_V1.json")
    schema=load(root/"schemas/por-derecho-federation-envelope-v1.schema.json")
    example=load(root/"ops/federation/EXAMPLE_STATE_ENVELOPE.json")

    authority=contract.get("authority_boundary",{})
    for key, expected in AUTHORITY_EXPECTED.items():
        observed=authority.get(key)
        if observed != expected:
            fail(
                "AUTHORITY_DRIFT",
                f"authority_boundary.{key}",
                observed,
                expected,
                "restore_the_reviewed_authority_boundary_or_open_a_new_governed_successor",
            )

    units=set(contract.get("portable_exchange_units",[]))
    if units != REQUIRED_UNITS:
        fail(
            "TAXONOMY_DRIFT",
            "portable_exchange_units",
            sorted(units),
            sorted(REQUIRED_UNITS),
            "reconcile_the_portable_exchange_taxonomy",
        )

    roles={row.get("role") for row in contract.get("supervised_intelligence_roles",[])}
    if roles != REQUIRED_ROLES:
        fail(
            "TAXONOMY_DRIFT",
            "supervised_intelligence_roles",
            sorted(roles),
            sorted(REQUIRED_ROLES),
            "reconcile_the_supervised_role_taxonomy",
        )

    rules=set(contract.get("host_bridge_rules",[]))
    missing=REQUIRED_RULES-rules
    if missing:
        fail(
            "BRIDGE_INVARIANT_MISSING",
            "host_bridge_rules",
            sorted(rules),
            sorted(REQUIRED_RULES),
            "restore_missing_invariants_before_integration",
        )

    recursion=contract.get("recursive_engine",{})
    if recursion.get("max_hops") != 32:
        fail(
            "RECURSION_POLICY_DRIFT",
            "recursive_engine.max_hops",
            recursion.get("max_hops"),
            32,
            "restore_bounded_recursion_or_open_a_reviewed_successor",
        )
    if recursion.get("cycle_policy") != "FAIL_CLOSED_WITH_VISITED_SET":
        fail(
            "RECURSION_POLICY_DRIFT",
            "recursive_engine.cycle_policy",
            recursion.get("cycle_policy"),
            "FAIL_CLOSED_WITH_VISITED_SET",
            "restore_fail_closed_cycle_handling",
        )
    if recursion.get("predecessor_required_after_genesis") is not True:
        fail(
            "RECURSION_POLICY_DRIFT",
            "recursive_engine.predecessor_required_after_genesis",
            recursion.get("predecessor_required_after_genesis"),
            True,
            "restore_the_predecessor_chain_requirement",
        )

    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        fail(
            "SCHEMA_INVALID",
            "schemas/por-derecho-federation-envelope-v1.schema.json",
            exc.message,
            "valid_json_schema_draft_2020_12",
            "repair_the_schema_before_validating_envelopes",
        )
    try:
        Draft202012Validator(schema).validate(example)
    except ValidationError as exc:
        fail(
            "ENVELOPE_SCHEMA_FAILURE",
            ".".join(str(x) for x in exc.absolute_path) or "<root>",
            exc.instance,
            exc.message,
            "repair_the_example_or_schema_without_weakening_constraints",
        )

    if example["iteration"] != 0 or example.get("predecessor") is not None:
        fail(
            "GENESIS_INVARIANT",
            "example.genesis",
            {"iteration":example.get("iteration"),"predecessor":example.get("predecessor")},
            {"iteration":0,"predecessor":None},
            "restore_the_genesis_envelope_invariant",
        )
    if example["recursion"]["next_action"] == "CLOSED":
        fail(
            "FALSE_CLOSURE",
            "example.recursion.next_action",
            "CLOSED",
            "REVIEW_or_other_nonterminal_state",
            "keep_bootstrap_open_until_terminal_conditions_are_proved",
        )

    return {
        "portable_units":len(REQUIRED_UNITS),
        "roles":len(REQUIRED_ROLES),
        "authority_fields":len(AUTHORITY_EXPECTED),
        "triggers":len(recursion.get("trigger_events",[])),
        "max_hops":recursion["max_hops"],
        "example_validated":1,
    }

def main():
    try:
        stats=validate()
    except ValueError as exc:
        raise SystemExit(f"Federation bridge: FAIL {exc}") from exc
    print("Federation bridge: PASS")
    print(" ".join(f"{k}={v}" for k,v in stats.items()))

if __name__=="__main__":
    main()

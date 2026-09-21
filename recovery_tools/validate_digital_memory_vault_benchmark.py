"""Validate benchmark truth-state only; never certify evidence from metadata."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

GATES = ("SCOPE", "BASELINE_ACCOUNTING", "NATIVE_RECOVERY", "CONTENT_IDENTITY",
         "USABLE_EVIDENCE", "PRIVATE_PROTECTION", "INDEPENDENT_RESTORE",
         "MEMORY_REHYDRATION", "ONGOING_INTAKE", "OFFICIAL_DOCKET")


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["State must be an object"]
    if data.get("benchmark_id") != "PD-VAULT-BENCHMARK-20260912-01":
        errors.append("Unexpected benchmark identity")
    for key in ("full", "official_court_file_complete", "whole_scope_denominator_closed"):
        if type(data.get(key)) is not bool:
            errors.append(f"{key} must be boolean")
    gates = data.get("gates")
    receipts = data.get("receipt_ids")
    if not isinstance(gates, dict) or set(gates) != set(GATES):
        return errors + ["Exactly the declared gates are required"]
    if not isinstance(receipts, dict):
        return errors + ["receipt_ids must be an object"]
    for gate, status in gates.items():
        if status not in ("OPEN", "UNVERIFIED", "PASS", "FAIL"):
            errors.append(f"Invalid gate status: {gate}")
        receipt = receipts.get(gate)
        if status == "PASS" and not (isinstance(receipt, str) and receipt.strip()):
            errors.append(f"PASS requires a reviewed receipt reference: {gate}")
    for key in ("required_native_occurrences", "verified_native_occurrences", "unresolved_required_gaps"):
        value = data.get(key)
        if value is not None and (type(value) is not int or value < 0):
            errors.append(f"{key} must be null or a nonnegative integer")
    if data.get("full"):
        required = data.get("required_native_occurrences")
        verified = data.get("verified_native_occurrences")
        if data.get("whole_scope_denominator_closed") is not True or not data.get("scope_version"):
            errors.append("Full requires a closed versioned scope")
        if type(required) is not int or type(verified) is not int or required != verified:
            errors.append("Full requires all required native occurrences verified")
        if data.get("unresolved_required_gaps") != 0:
            errors.append("Full requires zero unresolved required gaps")
        if any(gates[g] != "PASS" for g in GATES if g != "OFFICIAL_DOCKET"):
            errors.append("Full requires all held-source recovery gates to pass")
    if data.get("official_court_file_complete") and gates["OFFICIAL_DOCKET"] != "PASS":
        errors.append("Court completeness requires its separate docket gate")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", nargs="?", type=Path,
                        default=Path(__file__).resolve().parents[1] / "ops/digital-memory-vault/STATE.json")
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.state.read_text(encoding="utf-8"))
        errors = validate(data)
    except (OSError, ValueError) as exc:
        print(f"INVALID_CONTROL: {type(exc).__name__}")
        return 1
    if errors:
        print("INVALID_CONTROL: " + "; ".join(errors))
        return 1
    print("VALID_CONTROL; recovery=" + ("DECLARED_COMPLETE_REQUIRES_RECEIPT_REVIEW" if data["full"] else "NOT_COMPLETE"))
    print("Structural validation does not verify private receipts, stored bytes, encryption or restoration.")
    return 2 if args.require_complete and not data["full"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

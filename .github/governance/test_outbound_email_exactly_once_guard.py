#!/usr/bin/env python3
"""Validate the machine-readable outbound-email exactly-once guard.

This test does not connect to Gmail. It verifies the repository control's
non-negotiable invariants and simulates the one-shot authorization lock.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


HERE = Path(__file__).resolve().parent
POLICY_PATH = HERE / "outbound-email-exactly-once-guard-v1.json"


@dataclass
class ExecutionState:
    state: str = "PREPARED"
    authorization_consumed: bool = False
    outbound_mutation_count: int = 0
    mutation_lock: bool = False

    def authorize(self) -> None:
        if self.state != "PREPARED":
            raise RuntimeError(f"cannot authorize from {self.state}")
        self.state = "AUTHORIZED"

    def begin_outbound_mutation(self) -> None:
        """Atomically consume authorization before the provider call."""
        if self.state != "AUTHORIZED":
            raise RuntimeError(f"outbound mutation blocked from {self.state}")
        if self.authorization_consumed or self.mutation_lock:
            raise RuntimeError("authorization already consumed")
        if self.outbound_mutation_count != 0:
            raise RuntimeError("outbound mutation already attempted")

        self.authorization_consumed = True
        self.outbound_mutation_count = 1
        self.mutation_lock = True
        self.state = "TRANSMISSION_ATTEMPTED"

    def record_provider_success(self) -> None:
        if self.state != "TRANSMISSION_ATTEMPTED":
            raise RuntimeError(f"cannot record success from {self.state}")
        self.state = "SENT"

    def record_provider_uncertain(self) -> None:
        if self.state != "TRANSMISSION_ATTEMPTED":
            raise RuntimeError(f"cannot record uncertainty from {self.state}")
        self.state = "OUTCOME_UNKNOWN"

    def verify_read_only(self, matching_sent_messages: int) -> None:
        if self.state not in {"SENT", "OUTCOME_UNKNOWN"}:
            raise RuntimeError(f"cannot verify from {self.state}")
        if matching_sent_messages != 1:
            raise RuntimeError(
                f"verification requires exactly one matching sent message; got {matching_sent_messages}"
            )
        self.state = "VERIFIED"


def load_policy() -> dict:
    with POLICY_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_policy_invariants(policy: dict) -> None:
    invariants = policy["invariants"]
    assert invariants["maximum_outbound_mutations_per_authorization"] == 1
    assert invariants["consume_authorization_before_invocation"] is True
    assert invariants["lock_on_any_first_attempt_outcome"] is True
    assert invariants["parallel_outbound_mutations_allowed"] is False
    assert invariants["verification_must_be_read_only"] is True
    assert invariants["automatic_retry_allowed"] is False
    assert invariants["fresh_authorization_required_for_retry_or_correction"] is True

    assert "TRANSMISSION_ATTEMPTED" in policy["states"]
    assert "send" in policy["prohibited_after_first_attempt"]
    assert "forward" in policy["prohibited_after_first_attempt"]
    assert "reply" in policy["prohibited_after_first_attempt"]
    assert "search_sent_mail" in policy["read_only_verification_capabilities"]

    requirements = policy["verification_requirements"]
    assert requirements["outbound_mutation_count_must_equal"] == 1
    assert requirements["matching_sent_messages_in_duplicate_window_must_equal"] == 1


def test_first_mutation_consumes_authorization() -> None:
    execution = ExecutionState()
    execution.authorize()
    execution.begin_outbound_mutation()

    assert execution.state == "TRANSMISSION_ATTEMPTED"
    assert execution.authorization_consumed is True
    assert execution.outbound_mutation_count == 1
    assert execution.mutation_lock is True

    try:
        execution.begin_outbound_mutation()
    except RuntimeError:
        pass
    else:
        raise AssertionError("a second outbound mutation was incorrectly allowed")


def test_success_path_is_read_only_after_send() -> None:
    execution = ExecutionState()
    execution.authorize()
    execution.begin_outbound_mutation()
    execution.record_provider_success()
    execution.verify_read_only(matching_sent_messages=1)
    assert execution.state == "VERIFIED"
    assert execution.outbound_mutation_count == 1


def test_uncertain_provider_result_does_not_unlock_retry() -> None:
    execution = ExecutionState()
    execution.authorize()
    execution.begin_outbound_mutation()
    execution.record_provider_uncertain()

    try:
        execution.begin_outbound_mutation()
    except RuntimeError:
        pass
    else:
        raise AssertionError("uncertain provider result incorrectly reopened authorization")


def test_duplicate_window_blocks_verified_status() -> None:
    execution = ExecutionState()
    execution.authorize()
    execution.begin_outbound_mutation()
    execution.record_provider_success()

    try:
        execution.verify_read_only(matching_sent_messages=2)
    except RuntimeError:
        pass
    else:
        raise AssertionError("duplicate messages incorrectly passed verification")


def main() -> int:
    policy = load_policy()
    test_policy_invariants(policy)
    test_first_mutation_consumes_authorization()
    test_success_path_is_read_only_after_send()
    test_uncertain_provider_result_does_not_unlock_retry()
    test_duplicate_window_blocks_verified_status()
    print("outbound-email exactly-once guard: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

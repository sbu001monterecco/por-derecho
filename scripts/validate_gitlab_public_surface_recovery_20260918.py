#!/usr/bin/env python3
"""Validate anonymous-public GitLab recovery classifications during the outage."""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER = ROOT / "ops" / "continuity" / "GITLAB_PUBLIC_SURFACE_RECOVERY_LEDGER_20260918.json"

ALLOWED = {
    "EXACT_GITLAB_RECOVERY",
    "EXACT_ALREADY_MIRRORED",
    "FUNCTIONAL_GITHUB_EQUIVALENT",
    "PENDING_GITLAB_RESTORATION",
}


def validate() -> list[str]:
    failures: list[str] = []
    data = json.loads(LEDGER.read_text(encoding="utf-8"))

    if data.get("schema") != "por-derecho.gitlab-public-surface-recovery-ledger.v1":
        failures.append("schema_mismatch")
    if data.get("status") != "ACTIVE_PUBLIC_ONLY":
        failures.append("ledger_not_public_only")
    if data.get("authenticated_gitlab_restoration_verified") is not False:
        failures.append("authenticated_restoration_must_remain_false_without_verified_recovery")
    if not re.fullmatch(r"[0-9a-f]{40}", data.get("last_verified_gitlab_main_sha", "")):
        failures.append("last_verified_gitlab_sha_invalid")
    if set(data.get("allowed_classifications", [])) != ALLOWED:
        failures.append("classification_enum_drift")

    seen: set[str] = set()
    items = data.get("items", [])
    if not items:
        failures.append("empty_public_surface_ledger")

    for item in items:
        ident = item.get("id")
        if not ident or ident in seen:
            failures.append(f"duplicate_or_missing_id:{ident}")
        seen.add(ident)

        classification = item.get("classification")
        if classification not in ALLOWED:
            failures.append(f"invalid_classification:{ident}")

        url = item.get("gitlab_public_url", "")
        if not url.startswith("https://"):
            failures.append(f"non_https_public_url:{ident}")

        surface_type = item.get("surface_type")
        source_state = item.get("source_level_state")
        if surface_type == "GITLAB_PAGES_RENDERED_ROUTE":
            if classification in {"EXACT_GITLAB_RECOVERY", "EXACT_ALREADY_MIRRORED"}:
                failures.append(f"rendered_page_improper_exact_classification:{ident}")
            if source_state != "PENDING_GITLAB_RESTORATION":
                failures.append(f"rendered_page_source_not_pending:{ident}")

        if classification in {"EXACT_GITLAB_RECOVERY", "EXACT_ALREADY_MIRRORED"}:
            for key in ("gitlab_object_identity", "gitlab_source_sha", "byte_identity"):
                if not item.get(key):
                    failures.append(f"exact_item_missing_{key}:{ident}")

        if not item.get("provenance") or not item.get("boundary"):
            failures.append(f"missing_provenance_boundary:{ident}")

    rules = " ".join(data.get("rules", [])).lower()
    for token in (
        "authenticated gitlab restoration",
        "rendered gitlab pages output is not exact source recovery",
        "never reconstruct unavailable gitlab source/template bytes",
        "source sha",
        "force-reset",
    ):
        if token not in rules:
            failures.append(f"truth_rule_missing:{token}")

    return failures


def main() -> int:
    failures = validate()
    report = {
        "schema": "por-derecho.gitlab-public-surface-recovery-validation.v1",
        "status": "PASS" if not failures else "FAIL",
        "ledger": str(LEDGER.relative_to(ROOT)),
        "failures": failures,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())

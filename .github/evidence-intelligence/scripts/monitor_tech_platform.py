#!/usr/bin/env python3
"""Produce a public-safe health report for the Por Derecho Tech Platform."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

PIN_RE = re.compile(r"uses:\s+[^\s@]+@[a-f0-9]{40}(?:\s|$)")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"cannot parse {path}: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="artifacts/tech-platform/health.json")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    platform = repo / ".github/evidence-intelligence"
    errors: list[str] = []
    warnings: list[str] = []

    required_paths = [
        platform / "README.md",
        platform / "TECH_PLATFORM_ROADMAP.md",
        platform / "TECH_PLATFORM_FUTURE_THREAD_PROMPT.md",
        platform / "id-extension-policy.json",
        platform / "source-classes.json",
        platform / "schemas/evidence-intelligence.schema.json",
        platform / "pilots/rpl2523/corpus.json",
        platform / "pilots/rpl2523/queries.json",
        platform / "pilots/rpl2523/custody-public-summary.json",
        platform / "pilots/rpl2523/baseline-result.json",
        platform / "scripts/validate_identity_compatibility.py",
        platform / "scripts/run_rpl2523_retrieval_pilot.py",
        repo / "assets/data/matter-identity-registry-v1.json",
        repo / "assets/data/matter-identity-registry-v1.proceedings.json",
        repo / "docs/deletion-audits/2026-08-25-tech-platform-evidence-intelligence-thread.md",
        repo / ".github/workflows/evidence-intelligence-rpl2523-pilot.yml",
        repo / ".github/workflows/tech-platform-monitor.yml"
    ]

    for path in required_paths:
        if not path.exists():
            errors.append(f"missing required Tech Platform file: {path.relative_to(repo)}")

    report: dict[str, Any] = {
        "schema": "por-derecho.tech-platform-health.v1",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "github_sha": os.environ.get("GITHUB_SHA"),
        "errors": errors,
        "warnings": warnings
    }

    if not errors:
        registry = load_json(repo / "assets/data/matter-identity-registry-v1.json")
        proceedings = load_json(repo / "assets/data/matter-identity-registry-v1.proceedings.json")
        baseline = load_json(platform / "pilots/rpl2523/baseline-result.json")
        custody = load_json(platform / "pilots/rpl2523/custody-public-summary.json")
        corpus = load_json(platform / "pilots/rpl2523/corpus.json")
        queries = load_json(platform / "pilots/rpl2523/queries.json")

        if registry.get("registry_id") != "PD-SP-IDENTITY-REGISTRY-001":
            errors.append("authoritative identity registry ID drift")
        proceeding_ids = {item.get("id") for item in proceedings.get("records", [])}
        if "PD-SP-R-0002" not in proceeding_ids:
            errors.append("PD-SP-R-0002 is missing from the proceeding registry")
        if baseline.get("retrieval", {}).get("status") != "PASS" or baseline.get("retrieval", {}).get("pass_count") != 7:
            errors.append("durable RPL retrieval baseline is not 7/7 PASS")
        if corpus.get("proceeding_id") != "PD-SP-R-0002" or len(corpus.get("sources", [])) != 3:
            errors.append("RPL corpus escaped its bounded proceeding or source count")
        if len(queries.get("evaluations", [])) != 7:
            errors.append("RPL evaluation count drifted from seven")
        if len(custody.get("documents", [])) != 4:
            errors.append("public custody summary no longer records four pilot documents")
        vault = custody.get("private_vault", {})
        if vault.get("provider_locators_published") or vault.get("native_bodies_committed_to_github"):
            errors.append("public/private custody boundary is unsafe")

        pyc_files = [str(path.relative_to(repo)) for path in platform.rglob("*.pyc")]
        cache_dirs = [str(path.relative_to(repo)) for path in platform.rglob("__pycache__")]
        if pyc_files or cache_dirs:
            errors.append("compiled/cache files detected in the public Tech Platform tree")

        for workflow_rel in [
            ".github/workflows/evidence-intelligence-rpl2523-pilot.yml",
            ".github/workflows/tech-platform-monitor.yml"
        ]:
            workflow_text = (repo / workflow_rel).read_text(encoding="utf-8")
            uses_lines = [line.strip() for line in workflow_text.splitlines() if "uses:" in line]
            for line in uses_lines:
                if not PIN_RE.search(line):
                    errors.append(f"mutable or invalid Action pin in {workflow_rel}: {line}")

        last_readback = baseline.get("custody", {}).get("last_private_readback")
        cadence = int(baseline.get("custody", {}).get("private_readback_cadence_days", 30))
        try:
            last_date = date.fromisoformat(last_readback)
            age_days = (date.today() - last_date).days
            if age_days > cadence:
                warnings.append(f"private custody readback is overdue: {age_days} days old; cadence {cadence}")
        except Exception:
            errors.append("invalid private custody readback date")

        current_state_path = repo / "ops/CURRENT_STATE.json"
        if current_state_path.exists():
            try:
                state = load_json(current_state_path)
                state_date = date.fromisoformat(state.get("as_of"))
                state_age = (date.today() - state_date).days
                if state_age > 7:
                    warnings.append(f"ops/CURRENT_STATE.json is {state_age} days old")
            except Exception:
                warnings.append("ops/CURRENT_STATE.json freshness could not be evaluated")

        report.update({
            "identity_registry_id": registry.get("registry_id"),
            "identity_count": registry.get("counts", {}).get("total"),
            "controlled_proceeding": "PD-SP-R-0002",
            "controlled_source_count": len(corpus.get("sources", [])),
            "evaluation_count": len(queries.get("evaluations", [])),
            "custody_document_count": len(custody.get("documents", [])),
            "baseline_status": baseline.get("retrieval", {}).get("status"),
            "last_private_readback": last_readback
        })

    report["errors"] = errors
    report["warnings"] = warnings
    report["status"] = "FAIL" if errors else ("PASS_WITH_WARNINGS" if warnings else "PASS")

    output = repo / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Tech Platform monitor: {report['status']}; errors={len(errors)} warnings={len(warnings)}; output={output}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

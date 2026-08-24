#!/usr/bin/env python3
"""Read-only continuity and publication-safety audit for the 2018 protection/do-over workstream."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "reports/UNITARY_EVIDENCE_DIGEST_24AUG2026.md",
    "reports/2018_PROTECTION_QUESTION_AND_DO_OVER_24AUG2026.md",
    "reports/UNITARY_DIGEST_IMPLEMENTATION_INDEX_24AUG2026.md",
    "intelligence/AC_PROTECTION_ACTION_MATRIX_24AUG2026.csv",
    "intelligence/CUATRECASAS_ACTION_FOLLOW_THROUGH_MATRIX_24AUG2026.csv",
    "intelligence/JUAN_TOMAS_PARRILLA_MANDATE_ACTION_MATRIX_24AUG2026.csv",
    "intelligence/SUN_PARK_2018_TRANSACTION_DISAGGREGATION_24AUG2026.csv",
    "ops/SUN_PARK_DO_OVER_BACKLOG_24AUG2026.md",
    "ops/SUN_PARK_DO_OVER_STATUS_24AUG2026.json",
    "es/2018-proteccion-leal-masa/index.html",
    "en/2018-loyal-protection-estate/index.html",
]

EXPECTED_MATRIX_COUNTS = {
    "intelligence/AC_PROTECTION_ACTION_MATRIX_24AUG2026.csv": 16,
    "intelligence/CUATRECASAS_ACTION_FOLLOW_THROUGH_MATRIX_24AUG2026.csv": 12,
    "intelligence/JUAN_TOMAS_PARRILLA_MANDATE_ACTION_MATRIX_24AUG2026.csv": 10,
    "intelligence/SUN_PARK_2018_TRANSACTION_DISAGGREGATION_24AUG2026.csv": 14,
}

PUBLIC_FILES = [
    "es/2018-proteccion-leal-masa/index.html",
    "en/2018-loyal-protection-estate/index.html",
]

BANNED_PUBLIC_MARKERS = [
    "ANGjdJ",
    "attachment_id",
    "mail.google.com/mail/",
    "private-user-images.githubusercontent.com",
    "sbu001@",
    "patdguez@",
]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def add_check(checks: list[dict[str, Any]], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def count_csv_rows(relative_path: str) -> int:
    with (ROOT / relative_path).open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def audit() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    for relative_path in REQUIRED_FILES:
        exists = (ROOT / relative_path).is_file()
        add_check(checks, f"required file: {relative_path}", exists, "present" if exists else "missing")

    status_path = ROOT / "ops/SUN_PARK_DO_OVER_STATUS_24AUG2026.json"
    if status_path.is_file():
        try:
            status = json.loads(status_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            add_check(checks, "status JSON parses", False, str(exc))
            status = {}
        else:
            add_check(checks, "status JSON parses", True, "valid JSON")

        expected_status = {
            "workstream": "sun-park-2018-protection-and-do-over",
            "status": "active",
            "deletion_eligibility": "not_eligible",
            "publication_status": "branch_and_pr_only",
            "liability_status": "not_determined",
        }
        for key, expected in expected_status.items():
            actual = status.get(key)
            add_check(checks, f"status field {key}", actual == expected, f"expected={expected!r}; actual={actual!r}")

        order = status.get("accountability_order", [])
        expected_order = [
            "direct_private_actor_conduct",
            "court_appointed_insolvency_administrator_protection_and_accounting",
            "subsidiary_lawyer_mandate_action_and_follow_through",
            "present_day_remediation",
        ]
        add_check(checks, "accountability order preserved", order == expected_order, json.dumps(order, ensure_ascii=False))

    for relative_path, expected_rows in EXPECTED_MATRIX_COUNTS.items():
        matrix_path = ROOT / relative_path
        if not matrix_path.is_file():
            continue
        try:
            actual_rows = count_csv_rows(relative_path)
        except (OSError, csv.Error) as exc:
            add_check(checks, f"matrix readable: {relative_path}", False, str(exc))
            continue
        add_check(
            checks,
            f"matrix row count: {relative_path}",
            actual_rows >= expected_rows,
            f"expected at least {expected_rows}; actual={actual_rows}",
        )

    report_path = "reports/2018_PROTECTION_QUESTION_AND_DO_OVER_24AUG2026.md"
    if (ROOT / report_path).is_file():
        report = read_text(report_path)
        report_markers = [
            "The primary institutional focus does not absolve private actors",
            "No responsive protective action has yet been located in the accessible corpus",
            "The original communication, annex set, Registry entry, outcome, client authority and privilege status must control",
            "Do-over does **not** mean",
        ]
        for marker in report_markers:
            add_check(checks, f"report boundary: {marker[:55]}", marker in report, "present" if marker in report else "missing")

    transaction_path = "intelligence/SUN_PARK_2018_TRANSACTION_DISAGGREGATION_24AUG2026.csv"
    if (ROOT / transaction_path).is_file():
        transaction_text = read_text(transaction_path)
        for event_id in [f"TX-{index:02d}" for index in range(1, 15)]:
            add_check(checks, f"transaction lane {event_id}", event_id in transaction_text, "present" if event_id in transaction_text else "missing")
        distinct_markers = [
            "Locales transaction / EUR 400,000 component",
            "Alleged acquisition/transfer of 31 LPB fincas",
            "Licitation, adjudication, AC report and deed",
        ]
        for marker in distinct_markers:
            add_check(checks, f"distinct transaction marker: {marker}", marker in transaction_text, "present" if marker in transaction_text else "missing")

    public_markers = {
        "es/2018-proteccion-leal-masa/index.html": [
            "¿Dónde estuvo la protección leal de la masa?",
            "Los actores privados no quedan absueltos",
            "Pregunta subsidiaria: ¿dónde estuvieron los abogados?",
            "La ausencia actual de un documento en el corpus no demuestra que la actuación no existiera",
        ],
        "en/2018-loyal-protection-estate/index.html": [
            "Where was the loyal protection of the estate?",
            "The private actors are not absolved",
            "Subsidiary question: where were the lawyers?",
            "does not, by itself, prove breach by the insolvency administrator",
        ],
    }

    for relative_path in PUBLIC_FILES:
        path = ROOT / relative_path
        if not path.is_file():
            continue
        text = read_text(relative_path)
        for marker in public_markers[relative_path]:
            add_check(checks, f"public boundary {relative_path}: {marker[:50]}", marker in text, "present" if marker in text else "missing")
        for banned in BANNED_PUBLIC_MARKERS:
            add_check(checks, f"public privacy marker absent {relative_path}: {banned}", banned not in text, "absent" if banned not in text else "FOUND")

    passed = all(check["passed"] for check in checks)
    return {
        "schema_version": "1.0",
        "workstream": "sun-park-2018-protection-and-do-over",
        "passed": passed,
        "check_count": len(checks),
        "failure_count": sum(1 for check in checks if not check["passed"]),
        "checks": checks,
    }


def write_outputs(result: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary_lines = [
        "# Sun Park 2018 protection/do-over continuity audit",
        "",
        f"- Result: **{'PASS' if result['passed'] else 'FAIL'}**",
        f"- Checks: {result['check_count']}",
        f"- Failures: {result['failure_count']}",
        "- Mode: read-only; the audit does not edit, delete, commit, push or publish repository content.",
        "",
        "## Checks",
        "",
    ]
    for check in result["checks"]:
        symbol = "✅" if check["passed"] else "❌"
        summary_lines.append(f"- {symbol} **{check['name']}** — {check['detail']}")
    (output_dir / "summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        default="artifacts/sun-park-2018-protection-do-over-audit",
        help="Directory for result.json and summary.md",
    )
    args = parser.parse_args()

    result = audit()
    write_outputs(result, ROOT / args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

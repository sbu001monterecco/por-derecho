#!/usr/bin/env python3
"""Read-only deletion-safety, publication-integrity and optional live-route audit for the Laborý/CATRUDE workstream."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "ops/LABORY_CATRUDE_RECOVERY_STATUS.json"
ARCHIVES = ROOT / "evidence/sun-park/labory-catrude/archive-register.csv"
CANDIDATES = ROOT / "evidence/sun-park/labory-catrude/candidate-report-register.csv"
PAGES = [
    ROOT / "es/labory-catrude-antecedente-tecnico-historico/index.html",
    ROOT / "en/labory-catrude-historical-technical-antecedent/index.html",
]
WORKFLOW = ROOT / ".github/workflows/labory-catrude-thread-deletion-audit.yml"
PUBLIC_PREFIXES = [
    ROOT / "evidence/sun-park/labory-catrude",
    ROOT / "ops/LABORY_CATRUDE_RECOVERY_STATUS.json",
    ROOT / "ops/LABORY_CATRUDE_RECOVERY_BACKLOG.md",
    ROOT / "archive/LABORY_CATRUDE_RECOVERY_CONTINUITY_24AUG2026.md",
    *PAGES,
]
ALLOWED_CLASSIFICATIONS = {
    "POSSIBLE TARGET",
    "PROBABLE TARGET",
    "CONFIRMED TARGET",
    "RELATED BUT DIFFERENT REPORT",
    "EXCLUDED",
    "UNREADABLE / ACCESS PENDING",
}
FORBIDDEN_PUBLIC_PATTERNS = {
    "gmail_message_id": re.compile(r"\b(?:14|15|16|17|18|19)[0-9a-f]{14}\b", re.I),
    "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "private_share_locator": re.compile(r"share\.google/", re.I),
    "gmail_attachment_token": re.compile(r"ANGjdJ[-_A-Za-z0-9]+"),
}
LIVE_CHECKS = {
    "es_page": {
        "url": "https://sbu001monterecco.github.io/por-derecho/es/labory-catrude-antecedente-tecnico-historico/",
        "markers": [
            "El informe recordado como trabajo de Laborý/CATRUDE todavía no está identificado.",
            "GMAIL-ZIP-001",
            "Derecho de respuesta y solicitud documental",
        ],
    },
    "en_page": {
        "url": "https://sbu001monterecco.github.io/por-derecho/en/labory-catrude-historical-technical-antecedent/",
        "markers": [
            "The report remembered as Laborý/CATRUDE work has not yet been identified.",
            "GMAIL-ZIP-001",
            "Right of response and document request",
        ],
    },
    "archive_register": {
        "url": "https://sbu001monterecco.github.io/por-derecho/evidence/sun-park/labory-catrude/archive-register.csv",
        "markers": [
            "GMAIL-ZIP-001,1,8. Informes Periciales.zip",
            "GMAIL-ZIP-018,18,LONDON.zip",
        ],
    },
    "sitemap": {
        "url": "https://sbu001monterecco.github.io/por-derecho/sitemap-labory-catrude.xml",
        "markers": [
            "/es/labory-catrude-antecedente-tecnico-historico/",
            "/en/labory-catrude-historical-technical-antecedent/",
        ],
    },
}


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid or missing JSON: {exc}")
        return {}


def public_files() -> list[Path]:
    files: list[Path] = []
    for path in PUBLIC_PREFIXES:
        if path.is_dir():
            files.extend(item for item in path.rglob("*") if item.is_file())
        elif path.is_file():
            files.append(path)
    return sorted(set(files))


def run_live_checks(attempts: int, delay: int) -> tuple[dict, list[str]]:
    pending = dict(LIVE_CHECKS)
    results: dict[str, dict] = {}
    last_errors: dict[str, str] = {}

    for attempt in range(1, attempts + 1):
        for name, check in list(pending.items()):
            request = urllib.request.Request(
                check["url"],
                headers={"User-Agent": "por-derecho-labory-catrude-audit/1"},
            )
            try:
                with urllib.request.urlopen(request, timeout=25) as response:
                    body = response.read()
                    text = body.decode("utf-8", errors="replace")
                    missing = [marker for marker in check["markers"] if marker not in text]
                    if response.status != 200:
                        raise RuntimeError(f"HTTP {response.status}")
                    if missing:
                        raise RuntimeError(f"missing markers: {missing}")
                    results[name] = {
                        "url": check["url"],
                        "status": response.status,
                        "bytes": len(body),
                        "sha256": hashlib.sha256(body).hexdigest(),
                        "markers_verified": check["markers"],
                        "attempt": attempt,
                    }
                    pending.pop(name, None)
                    last_errors.pop(name, None)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError) as exc:
                last_errors[name] = str(exc)

        if not pending:
            break
        if attempt < attempts:
            time.sleep(delay)

    errors = [
        f"live check failed for {name} at {check['url']}: {last_errors.get(name, 'unknown error')}"
        for name, check in pending.items()
    ]
    return results, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="artifacts/labory-catrude-deletion-audit")
    parser.add_argument("--live", action="store_true", help="verify the exact public routes and markers")
    parser.add_argument("--live-attempts", type=int, default=24)
    parser.add_argument("--live-delay", type=int, default=10)
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    status = load_json(STATUS, errors)
    if status.get("target_status") != "NOT_IDENTIFIED":
        errors.append("target_status must remain NOT_IDENTIFIED unless the registers and primary evidence are updated together")
    if status.get("deletion_state") != "not eligible":
        errors.append("workstream deletion_state must be not eligible")

    try:
        rows = list(csv.DictReader(ARCHIVES.open(encoding="utf-8")))
    except Exception as exc:
        errors.append(f"cannot read archive register: {exc}")
        rows = []
    if len(rows) != 18:
        errors.append(f"archive register contains {len(rows)} rows; expected 18")
    expected = [f"GMAIL-ZIP-{index:03d}" for index in range(1, 19)]
    if [row.get("archive_id") for row in rows] != expected:
        errors.append("archive aliases must be complete and ordered GMAIL-ZIP-001 through GMAIL-ZIP-018")
    for row in rows:
        if row.get("inspection_status") != "metadata_only_not_opened":
            errors.append(f"{row.get('archive_id')}: inspection status must remain metadata_only_not_opened until bytes are opened")
        if row.get("deletion_state") != "not eligible":
            errors.append(f"{row.get('archive_id')}: deletion state is not protected")
        for key in ("archive_name", "source_date", "size_bytes", "relevance", "next_action"):
            if not row.get(key):
                errors.append(f"{row.get('archive_id')}: missing {key}")

    try:
        candidates = list(csv.DictReader(CANDIDATES.open(encoding="utf-8")))
    except Exception as exc:
        errors.append(f"cannot read candidate register: {exc}")
        candidates = []
    for candidate in candidates:
        if candidate.get("classification") not in ALLOWED_CLASSIFICATIONS:
            errors.append(f"{candidate.get('candidate_id')}: invalid classification")
    if not candidates or candidates[0].get("classification") != "POSSIBLE TARGET":
        errors.append("target candidate must remain POSSIBLE TARGET")
    if not any(candidate.get("document") == "Unidentified historical Laborý/CATRUDE report" for candidate in candidates):
        errors.append("target candidate is missing")

    for page in PAGES:
        if not page.is_file():
            errors.append(f"missing page: {page.relative_to(ROOT)}")
            continue
        text = page.read_text(encoding="utf-8")
        required = [
            "NOT IDENTIFIED" if "/en/" in str(page) else "NO IDENTIFICADO",
            "FACT:" if "/en/" in str(page) else "HECHO:",
            "DOCUMENT:" if "/en/" in str(page) else "DOCUMENTO:",
            "OPEN QUESTION:" if "/en/" in str(page) else "PREGUNTA ABIERTA:",
            "Right of response" if "/en/" in str(page) else "Derecho de respuesta",
            "site.js?v=20260824e",
        ]
        for marker in required:
            if marker not in text:
                errors.append(f"{page.relative_to(ROOT)}: missing marker {marker}")

    if not WORKFLOW.is_file():
        errors.append("scheduled workflow missing")
    else:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for marker in ("schedule:", "cron: '17 */6 * * *'", "contents: read", "workflow_dispatch:", "--live"):
            if marker not in workflow:
                errors.append(f"workflow missing {marker}")
        for forbidden in ("contents: write", "git push", "git commit", "rm -rf"):
            if forbidden in workflow.lower():
                errors.append(f"workflow must be read-only; found {forbidden}")

    for path in public_files():
        if path.suffix.lower() not in {".md", ".csv", ".json", ".html", ".yml", ".yaml", ".xml", ".txt", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for name, pattern in FORBIDDEN_PUBLIC_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)}: forbidden public {name}")

    live_results: dict[str, dict] = {}
    if args.live:
        live_results, live_errors = run_live_checks(args.live_attempts, args.live_delay)
        errors.extend(live_errors)

    result = {
        "schema": "por-derecho.labory-catrude-deletion-audit.v2",
        "status": "FAIL" if errors else "PASS",
        "target_status": status.get("target_status"),
        "deletion_state": status.get("deletion_state"),
        "archive_rows": len(rows),
        "candidate_rows": len(candidates),
        "live_mode": args.live,
        "live_checks": live_results,
        "errors": errors,
        "warnings": warnings,
        "operational_note": "Read-only audit. It does not delete, commit, push, merge or rewrite history.",
    }

    output = (ROOT / args.output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = [
        "# Laborý / CATRUDE thread-deletion audit",
        "",
        f"**Result:** {result['status']}",
        f"**Target:** {result['target_status']}",
        f"**Deletion state:** {result['deletion_state']}",
        f"**Archive rows:** {len(rows)}",
        f"**Live mode:** {args.live}",
        "",
        result["operational_note"],
    ]
    if live_results:
        summary += ["", "## Live routes"]
        summary.extend(
            f"- {name}: HTTP {item['status']} · {item['bytes']} bytes · SHA-256 `{item['sha256']}`"
            for name, item in live_results.items()
        )
    if errors:
        summary += ["", "## Errors", *[f"- {error}" for error in errors]]
    else:
        summary += [
            "",
            "## Determination",
            "",
            "This workstream remains **not eligible** for deletion because the target report is unidentified and 18 ranked archives remain uninspected at byte level.",
        ]
    (output / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

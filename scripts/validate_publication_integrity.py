#!/usr/bin/env python3
"""Repository-wide publication/deletion-safety guard for Por Derecho.

The invariant is simple: chat narration is never proof of publication. Source must be
recoverable in Git, validation must be reproducible, merge must be observable, and
LIVE VERIFIED / DELETION SAFE are states earned by evidence rather than prose.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "publication-manifests"
ORDER = [
    "DRAFT",
    "PREPARED_PENDING_MERGE",
    "REMOTE_SOURCE",
    "PR_OPEN",
    "CI_GREEN",
    "MERGED",
    "DEPLOYED",
    "LIVE_VERIFIED",
    "DELETION_SAFE",
]
VALID_STATES = set(ORDER) | {"BLOCKED_RECOVERY"}
FORBIDDEN_TEMP_NAMES = {"NOOP.tmp", "SHOULD_NOT_EXIST.tmp"}
ENCODED_SUFFIXES = {".b64", ".tar", ".gz", ".tgz", ".zip"}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def changed_files() -> list[str]:
    base = os.getenv("GITHUB_BASE_SHA", "").strip()
    head = os.getenv("GITHUB_HEAD_SHA", "HEAD").strip() or "HEAD"
    if not base or set(base) == {"0"}:
        return []
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", f"{base}...{head}"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return [line.strip() for line in out.splitlines() if line.strip()]
    except Exception:
        return []


def load_manifests(errors: list[str]) -> list[tuple[Path, dict]]:
    manifests: list[tuple[Path, dict]] = []
    if not MANIFEST_DIR.exists():
        return manifests
    for path in sorted(MANIFEST_DIR.glob("*.json")):
        try:
            manifests.append((path, json.loads(path.read_text(encoding="utf-8"))))
        except Exception as exc:
            fail(f"{path.relative_to(ROOT)}: invalid JSON: {exc}", errors)
    return manifests


def validate_manifest(path: Path, data: dict, errors: list[str]) -> None:
    rel = path.relative_to(ROOT)
    required = ["publication_id", "current_state", "expected_routes", "owner"]
    for key in required:
        if key not in data:
            fail(f"{rel}: missing required field {key!r}", errors)

    state = data.get("current_state")
    if state not in VALID_STATES:
        fail(f"{rel}: unknown current_state {state!r}", errors)
        return

    routes = data.get("expected_routes") or {}
    es = routes.get("es") or []
    en = routes.get("en") or []
    if not isinstance(es, list) or not isinstance(en, list):
        fail(f"{rel}: expected_routes.es/en must be arrays", errors)
        return
    if es or en:
        if len(es) != len(en):
            fail(f"{rel}: bilingual route parity failed ({len(es)} ES vs {len(en)} EN)", errors)
        if len(set(es + en)) != len(es + en):
            fail(f"{rel}: duplicate route paths declared", errors)

    if state == "BLOCKED_RECOVERY":
        if not data.get("blocking_reason"):
            fail(f"{rel}: BLOCKED_RECOVERY requires blocking_reason", errors)
        if not data.get("recovery_requirements"):
            fail(f"{rel}: BLOCKED_RECOVERY requires recovery_requirements", errors)
        return

    rank = ORDER.index(state)
    if rank >= ORDER.index("REMOTE_SOURCE"):
        for route in es + en:
            if not (ROOT / route).is_file():
                fail(f"{rel}: declared route missing from Git source: {route}", errors)
        for source in data.get("expected_source_files", []):
            if not (ROOT / source).is_file():
                fail(f"{rel}: declared source file missing from Git: {source}", errors)

    if rank >= ORDER.index("CI_GREEN"):
        validation = data.get("validation") or {}
        if not validation.get("evidence"):
            fail(f"{rel}: CI_GREEN or later requires validation.evidence", errors)
    if rank >= ORDER.index("MERGED") and not data.get("merge_sha"):
        fail(f"{rel}: MERGED or later requires merge_sha", errors)
    if rank >= ORDER.index("DEPLOYED") and not data.get("deployment_evidence"):
        fail(f"{rel}: DEPLOYED or later requires deployment_evidence", errors)
    if rank >= ORDER.index("LIVE_VERIFIED"):
        if not data.get("live_urls"):
            fail(f"{rel}: LIVE_VERIFIED or later requires live_urls", errors)
        if not data.get("live_verification_evidence"):
            fail(f"{rel}: LIVE_VERIFIED or later requires live_verification_evidence", errors)
    if rank >= ORDER.index("DELETION_SAFE") and not data.get("deletion_record"):
        fail(f"{rel}: DELETION_SAFE requires deletion_record", errors)


def validate_changed_files(files: list[str], manifests: list[tuple[Path, dict]], errors: list[str]) -> None:
    bootstrap_rules = []
    for _, data in manifests:
        rule = data.get("encoded_bootstrap")
        if rule:
            bootstrap_rules.append(rule)

    for rel in files:
        p = Path(rel)
        if p.name in FORBIDDEN_TEMP_NAMES or p.suffix == ".tmp":
            fail(f"forbidden temporary/placeholder artefact changed: {rel}", errors)

        if p.suffix.lower() in ENCODED_SUFFIXES and ("payload" in rel.lower() or "bootstrap" in rel.lower()):
            allowed = False
            for rule in bootstrap_rules:
                pattern = rule.get("pattern", "")
                if pattern and fnmatch.fnmatch(rel, pattern):
                    complete = bool(rule.get("complete"))
                    declared = int(rule.get("declared_parts", 0) or 0)
                    actual = len(list(ROOT.glob(pattern)))
                    if complete and declared > 0 and actual == declared:
                        allowed = True
                    else:
                        fail(
                            f"encoded bootstrap is incomplete: {rel} (declared={declared}, actual={actual}, complete={complete})",
                            errors,
                        )
                    break
            if not allowed and not any(fnmatch.fnmatch(rel, r.get("pattern", "")) for r in bootstrap_rules):
                fail(f"encoded bootstrap/payload is not an accepted publication source: {rel}", errors)


def live_check(manifests: list[tuple[Path, dict]], errors: list[str]) -> None:
    for path, data in manifests:
        state = data.get("current_state")
        if state not in {"DEPLOYED", "LIVE_VERIFIED", "DELETION_SAFE"}:
            continue
        markers = data.get("live_markers") or {}
        for url in data.get("live_urls") or []:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "por-derecho-publication-integrity/1"})
                with urllib.request.urlopen(req, timeout=20) as response:
                    body = response.read().decode("utf-8", errors="replace")
                    if response.status != 200:
                        fail(f"{path.name}: live URL returned {response.status}: {url}", errors)
                    for marker in markers.get(url, []):
                        if marker not in body:
                            fail(f"{path.name}: live marker missing at {url}: {marker!r}", errors)
            except Exception as exc:
                fail(f"{path.name}: live verification failed for {url}: {exc}", errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="also verify manifests at DEPLOYED or later against public URLs")
    args = parser.parse_args()

    errors: list[str] = []
    manifests = load_manifests(errors)
    files = changed_files()
    validate_changed_files(files, manifests, errors)
    for path, data in manifests:
        validate_manifest(path, data, errors)
    if args.live:
        live_check(manifests, errors)

    if errors:
        print("PUBLICATION INTEGRITY GATE: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1
    print(f"PUBLICATION INTEGRITY GATE: PASS ({len(manifests)} manifests; {len(files)} changed files inspected)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

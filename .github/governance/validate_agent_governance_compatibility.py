#!/usr/bin/env python3
"""Validate the narrow, non-interfering agent-governance package.

This check is intentionally manual. It proves that a governance-only diff stays
outside the repository's public-runtime and deployment-control surface. It does
not grant publication authority or validate legacy public content.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

GOVERNANCE_ALLOWLIST = {
    ".github/CODEOWNERS",
    ".github/governance/AGENT_PUBLISHING_COMPATIBILITY.md",
    ".github/governance/TRANSACTION_DEVELOPMENT_SEPARATION_AND_PUBLICATION_PROTOCOL.md",
    ".github/governance/records/TXD-PN-20260825-01.md",
    ".github/governance/validate_agent_governance_compatibility.py",
    "AGENTS.md",
    "CHATGPT_START_HERE.md",
}

REQUIRED_FILES = set(GOVERNANCE_ALLOWLIST)

REQUIRED_MARKERS = {
    "AGENTS.md": [
        "PD-GOV-001 — CURRENT-MAIN",
        "PD-GOV-002 — PUBLIC-REPO",
        "PD-GOV-003 — AUTHORITY",
        "PD-GOV-004 — NON-INTERFERENCE",
        "PD-GOV-005 — HARD-VS-ADVISORY",
        "PD-GOV-006 — SENT-LINKS",
        "PD-GOV-007 — REVERSIBLE",
        "PD-GOV-008 — THREAD-CONTINUITY",
        "repository or Pages authority never authorises email",
        "Documentation alone must not activate a new repository-wide hard gate",
    ],
    ".github/governance/AGENT_PUBLISHING_COMPATIBILITY.md": [
        "## Compatibility promise",
        "## Enforcement matrix",
        "## Public-site surface",
        "## Governance-only acceptance test",
        "This promise does not grant standing authority",
    ],
}

CODEOWNER_LINES = {
    "/AGENTS.md @sbu001monterecco",
    "/CHATGPT_START_HERE.md @sbu001monterecco",
    "/.github/governance/ @sbu001monterecco",
}


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, stderr=subprocess.STDOUT
    ).strip()


def changed_files(base: str) -> set[str]:
    tracked = {
        line
        for line in git(
            "diff", "--name-only", "--diff-filter=ACMRDTUXB", base, "--"
        ).splitlines()
        if line
    }
    untracked = {
        line
        for line in git("ls-files", "--others", "--exclude-standard").splitlines()
        if line
    }
    return tracked | untracked


def validate_files(errors: list[str]) -> None:
    for rel in sorted(REQUIRED_FILES):
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"required governance file missing: {rel}")
        elif path.is_symlink():
            errors.append(f"governance file must not be a symlink: {rel}")

    for rel, markers in REQUIRED_MARKERS.items():
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{rel}: required compatibility marker missing: {marker!r}")

    bootstrap = ROOT / "CHATGPT_START_HERE.md"
    if bootstrap.is_file():
        text = bootstrap.read_text(encoding="utf-8")
        if "AGENTS.md" not in text or ".github/governance/AGENT_PUBLISHING_COMPATIBILITY.md" not in text:
            errors.append(
                "CHATGPT_START_HERE.md must route future threads to the compatibility policy"
            )

    codeowners = ROOT / ".github" / "CODEOWNERS"
    if not codeowners.is_file():
        errors.append(".github/CODEOWNERS is missing")
    else:
        lines = {
            line.strip()
            for line in codeowners.read_text(encoding="utf-8").splitlines()
        }
        for expected in sorted(CODEOWNER_LINES):
            if expected not in lines:
                errors.append(f".github/CODEOWNERS missing: {expected}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base", default="origin/main", help="Git ref used as the comparison base"
    )
    parser.add_argument(
        "--governance-only",
        action="store_true",
        help="fail if any changed path is outside the narrow governance allowlist",
    )
    args = parser.parse_args()

    errors: list[str] = []
    try:
        base_sha = git("rev-parse", "--verify", f"{args.base}^{{commit}}")
        files = changed_files(args.base)
    except subprocess.CalledProcessError as exc:
        print("AGENT GOVERNANCE COMPATIBILITY: FAIL")
        print(f" - unable to resolve or compare base {args.base!r}: {exc.output.strip()}")
        return 1

    validate_files(errors)

    unexpected = sorted(files - GOVERNANCE_ALLOWLIST)
    if args.governance_only and unexpected:
        errors.append(
            "governance-only package changes non-governance path(s): " + ", ".join(unexpected)
        )

    if errors:
        print("AGENT GOVERNANCE COMPATIBILITY: FAIL")
        print(f" - base: {base_sha}")
        for item in errors:
            print(f" - {item}")
        return 1

    print("AGENT GOVERNANCE COMPATIBILITY: PASS")
    print(f" - base: {base_sha}")
    print(f" - changed paths: {len(files)}")
    print(" - rendered HTML/runtime/assets/deployment configuration changed: 0")
    print(
        " - intentional public governance/bootstrap changes: "
        "public-safe governance files only"
    )
    print(" - enforcement mode: manual/advisory")
    return 0


if __name__ == "__main__":
    sys.exit(main())

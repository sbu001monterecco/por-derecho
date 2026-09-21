#!/usr/bin/env python3
"""Conservative advisory public-impact shadow classifier for GitHub outage continuity.

This is a functional GitHub-side substitute while the exact GitLab MR !529
implementation is unavailable. It never authorizes CI bypass, merge, deployment
or publication. Unknown or ambiguous paths fail closed to YES_OR_UNKNOWN.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Iterable

NO_RUNTIME_PREFIXES = (
    ".github/",
    "tests/",
    "scripts/",
)
ALWAYS_PUBLIC_OR_RELEASE_SENSITIVE_PREFIXES = (
    ".github/workflows/",
)
PUBLIC_OR_RUNTIME_PREFIXES = (
    "en/",
    "es/",
    "assets/",
    "data/",
    "publication-manifests/",
    "public/",
    "site/",
)
PUBLIC_OR_RUNTIME_EXACT = {"index.html", "robots.txt", ".nojekyll"}


@dataclass(frozen=True)
class Classification:
    result: str
    reasons: tuple[str, ...]
    paths: tuple[str, ...]


def _normalise(path: str) -> str:
    value = str(PurePosixPath(path.strip()))
    return "" if value == "." else value


def classify(paths: Iterable[str]) -> Classification:
    normalised = tuple(p for p in (_normalise(x) for x in paths) if p)
    if not normalised:
        return Classification("UNKNOWN", ("no_changed_paths",), normalised)
    reasons: list[str] = []
    safe_count = 0
    for path in normalised:
        if path in PUBLIC_OR_RUNTIME_EXACT:
            reasons.append(f"public_exact:{path}")
            continue
        if path.startswith(ALWAYS_PUBLIC_OR_RELEASE_SENSITIVE_PREFIXES):
            reasons.append(f"release_sensitive:{path}")
            continue
        if path.startswith(PUBLIC_OR_RUNTIME_PREFIXES):
            reasons.append(f"public_or_runtime:{path}")
            continue
        if path.startswith(NO_RUNTIME_PREFIXES):
            safe_count += 1
            continue
        reasons.append(f"unclassified:{path}")
    if reasons:
        return Classification("YES_OR_UNKNOWN", tuple(reasons), normalised)
    if safe_count == len(normalised):
        return Classification("NO", ("all_paths_non_public_runtime",), normalised)
    return Classification("YES_OR_UNKNOWN", ("conservative_fallback",), normalised)


def git_changed_paths(base: str, head: str) -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...{head}"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return [line for line in proc.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paths", nargs="*", default=None)
    parser.add_argument("--base")
    parser.add_argument("--head")
    args = parser.parse_args()
    if args.paths is not None and (args.base or args.head):
        parser.error("use --paths OR --base/--head")
    if args.paths is not None:
        paths = args.paths
    elif args.base and args.head:
        paths = git_changed_paths(args.base, args.head)
    else:
        parser.error("provide --paths or both --base and --head")
    result = classify(paths)
    print(json.dumps({
        "schema": "por-derecho.public-impact-shadow.github-outage.v1",
        "result": result.result,
        "paths": list(result.paths),
        "reasons": list(result.reasons),
        "advisory_only": True,
        "exact_gitlab_implementation": False,
        "fail_closed": True,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

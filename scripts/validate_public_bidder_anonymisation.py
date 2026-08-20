#!/usr/bin/env python3
"""Fail if the protected third-party bidder identifier leaks into public website source.

The protected identifier is represented only by its SHA-256 digest. The validator
normalises word tokens from public-facing source files and compares their hashes;
it therefore enforces the publication rule without embedding the identifier itself
in the repository.
"""

from __future__ import annotations

import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PUBLIC_ROOTS = [ROOT / "es", ROOT / "en", ROOT / "assets"]
ROOT_FILES = [ROOT / "index.html", ROOT / "sitemap.xml", ROOT / "rss.xml"]
TEXT_SUFFIXES = {".html", ".htm", ".js", ".css", ".json", ".xml", ".md", ".txt", ".svg"}

# SHA-256 of the protected lower-case public identifier. Do not replace with plaintext.
PROTECTED_TOKEN_HASHES = {
    "33c594e4e36529842cb1344043ec59e9f4d026466fd7ba0112a635fbe30baf3e"
}

WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9_-]+", re.UNICODE)


def digest(token: str) -> str:
    return hashlib.sha256(token.casefold().encode("utf-8")).hexdigest()


def public_files():
    for base in PUBLIC_ROOTS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                yield path
    for path in ROOT_FILES:
        if path.exists():
            yield path


def main() -> int:
    failures: list[str] = []
    scanned = 0
    for path in public_files():
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            failures.append(f"READ ERROR {path.relative_to(ROOT)}: {exc}")
            continue
        for token in WORD_RE.findall(text):
            if digest(token) in PROTECTED_TOKEN_HASHES:
                failures.append(
                    f"Protected third-party bidder identifier found in public source: {path.relative_to(ROOT)}"
                )
                break

    if failures:
        print("PUBLIC BIDDER ANONYMISATION GATE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"PUBLIC BIDDER ANONYMISATION GATE: PASS ({scanned} public files scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

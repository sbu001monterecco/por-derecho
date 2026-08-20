#!/usr/bin/env python3
"""Rewrite protected bidder identifiers out of public website source.

The protected identifier is represented only by its SHA-256 digest. Public Spanish
source receives the generic label ``tercer oferente`` and public English source
receives ``third-party bidder``. The script is deterministic and idempotent.
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


def replacement_for(path: pathlib.Path) -> str:
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        return "third-party bidder"
    if rel.parts and rel.parts[0] == "es":
        return "tercer oferente"
    if rel.parts and rel.parts[0] == "en":
        return "third-party bidder"
    # Shared assets must stay language-neutral rather than naming the bidder.
    return "third-party bidder"


def rewrite_text(text: str, replacement: str) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        token = match.group(0)
        if digest(token) not in PROTECTED_TOKEN_HASHES:
            return token
        count += 1
        return replacement

    return WORD_RE.sub(repl, text), count


def main() -> int:
    changed: list[tuple[pathlib.Path, int]] = []
    for path in public_files():
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeError) as exc:
            print(f"READ ERROR {path.relative_to(ROOT)}: {exc}", file=sys.stderr)
            return 2
        rewritten, count = rewrite_text(text, replacement_for(path))
        if count:
            path.write_text(rewritten, encoding="utf-8")
            changed.append((path, count))

    if changed:
        print("PUBLIC BIDDER SOURCE REWRITE: CHANGED")
        for path, count in changed:
            print(f"- {path.relative_to(ROOT)}: {count} replacement(s)")
    else:
        print("PUBLIC BIDDER SOURCE REWRITE: NO CHANGES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Replace only protected bidder-name tokens in public website source.

The protected name token is represented only by its SHA-256 digest. Public Spanish
source receives the neutral label ``tercer oferente`` and public English source
receives ``third-party bidder``. The bid and every surrounding fact remain intact.
The operation is deterministic, idempotent and deliberately narrower than content
redaction.
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

# SHA-256 of the protected lower-case name token. Never replace this with plaintext.
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
    # Shared public assets use the neutral English label rather than the protected name.
    return "third-party bidder"


def rewrite_text(text: str, replacement: str) -> tuple[str, int]:
    """Return text with protected name tokens replaced and no other content changed."""
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        token = match.group(0)
        if digest(token) not in PROTECTED_TOKEN_HASHES:
            return token
        count += 1
        return replacement

    rewritten = WORD_RE.sub(repl, text)
    if rewritten.count("\n") != text.count("\n"):
        raise RuntimeError("Name-token rewrite changed the record's line structure")
    return rewritten, count


def main() -> int:
    changed: list[tuple[pathlib.Path, int]] = []
    for path in public_files():
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeError) as exc:
            print(f"READ ERROR {path.relative_to(ROOT)}: {exc}", file=sys.stderr)
            return 2
        try:
            rewritten, count = rewrite_text(text, replacement_for(path))
        except RuntimeError as exc:
            print(f"INVARIANT ERROR {path.relative_to(ROOT)}: {exc}", file=sys.stderr)
            return 3
        if count:
            path.write_text(rewritten, encoding="utf-8")
            changed.append((path, count))

    if changed:
        print("PUBLIC BIDDER NAME-TOKEN REWRITE: CHANGED")
        for path, count in changed:
            print(f"- {path.relative_to(ROOT)}: {count} name-token replacement(s)")
    else:
        print("PUBLIC BIDDER NAME-TOKEN REWRITE: NO CHANGES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

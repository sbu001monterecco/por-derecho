#!/usr/bin/env python3
"""Fail if the protected third-party bidder identifier leaks into public website source.

The protected identifier is represented only by its SHA-256 digest. The validator
normalises word tokens from public-facing source files or explicitly supplied public
URLs and compares their hashes; it therefore enforces the publication rule without
embedding the identifier itself in the repository.
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys
import urllib.request

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


def contains_protected_token(text: str) -> bool:
    return any(digest(token) in PROTECTED_TOKEN_HASHES for token in WORD_RE.findall(text))


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


def fetch_url(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Por-Derecho-public-bidder-anonymisation/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}")
        return response.read().decode("utf-8", "replace")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        action="append",
        default=[],
        help="Public URL to scan. Repeat for multiple URLs. When supplied, local scanning is skipped unless --also-local is used.",
    )
    parser.add_argument(
        "--also-local",
        action="store_true",
        help="Scan repository public source in addition to any --url values.",
    )
    return parser.parse_args()


def scan_local(failures: list[str]) -> int:
    scanned = 0
    for path in public_files():
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            failures.append(f"READ ERROR {path.relative_to(ROOT)}: {exc}")
            continue
        if contains_protected_token(text):
            failures.append(
                f"Protected third-party bidder identifier found in public source: {path.relative_to(ROOT)}"
            )
    return scanned


def scan_urls(urls: list[str], failures: list[str]) -> int:
    scanned = 0
    for url in urls:
        scanned += 1
        try:
            text = fetch_url(url)
        except Exception as exc:  # noqa: BLE001 - verifier should report all URL failures
            failures.append(f"URL READ ERROR {url}: {exc}")
            continue
        if contains_protected_token(text):
            failures.append(
                f"Protected third-party bidder identifier found in public URL: {url}"
            )
    return scanned


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    scanned_local = 0
    scanned_urls = 0

    if not args.url or args.also_local:
        scanned_local = scan_local(failures)
    if args.url:
        scanned_urls = scan_urls(args.url, failures)

    if failures:
        print("PUBLIC BIDDER ANONYMISATION GATE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    scope = []
    if scanned_local:
        scope.append(f"{scanned_local} local public files")
    if scanned_urls:
        scope.append(f"{scanned_urls} public URLs")
    print(f"PUBLIC BIDDER ANONYMISATION GATE: PASS ({', '.join(scope)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

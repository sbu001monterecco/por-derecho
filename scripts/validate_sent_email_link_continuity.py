#!/usr/bin/env python3
"""Validate every Por Derecho URL found in the seven-day sent-mail audit."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "publication-manifests/sent-email-link-continuity-20260824.json"
EXPECTED_BASE = "https://sbu001monterecco.github.io/por-derecho/"


class TargetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.targets: set[str] = set()
        self.canonicals: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value for key, value in attrs if value is not None}
        for key in ("id", "name"):
            if values.get(key):
                self.targets.add(values[key])
        rel = {part.lower() for part in values.get("rel", "").split()}
        if tag.lower() == "link" and "canonical" in rel and values.get("href"):
            self.canonicals.add(values["href"])


def route_file(url: str, base_url: str) -> tuple[Path, str | None]:
    parsed = urllib.parse.urlsplit(url)
    base = urllib.parse.urlsplit(base_url)
    if (parsed.scheme, parsed.netloc) != (base.scheme, base.netloc):
        raise ValueError(f"URL is outside the authoritative host: {url}")
    if not parsed.path.startswith(base.path):
        raise ValueError(f"URL is outside the project root: {url}")
    relative = urllib.parse.unquote(parsed.path[len(base.path) :])
    parts = Path(relative).parts
    if any(part in {"..", "."} for part in parts):
        raise ValueError(f"Unsafe route: {url}")
    if not relative:
        target = ROOT / "index.html"
    elif relative.endswith("/"):
        target = ROOT / relative / "index.html"
    else:
        target = ROOT / relative
    return target, urllib.parse.unquote(parsed.fragment) or None


def read_targets(path: Path) -> TargetParser:
    parser = TargetParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser


def validate_local(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    base_url = manifest.get("authoritative_base_url")
    routes = manifest.get("routes")
    if base_url != EXPECTED_BASE:
        errors.append(f"authoritative_base_url must be {EXPECTED_BASE!r}")
    if not isinstance(routes, list):
        return errors + ["routes must be a list"]
    if manifest.get("audit", {}).get("unique_por_derecho_urls") != len(routes):
        errors.append("manifest route count does not match audit.unique_por_derecho_urls")
    urls = [entry.get("url") for entry in routes if isinstance(entry, dict)]
    if len(urls) != len(set(urls)):
        errors.append("manifest URLs are not unique")
    if sum(int(entry.get("message_occurrences", 0)) for entry in routes) != manifest.get("audit", {}).get(
        "por_derecho_url_message_occurrences"
    ):
        errors.append("message occurrence total does not match the audit summary")

    for entry in routes:
        if not isinstance(entry, dict) or not isinstance(entry.get("url"), str):
            errors.append(f"invalid route entry: {entry!r}")
            continue
        url = entry["url"]
        expected_route = urllib.parse.urlsplit(url).path.removeprefix("/por-derecho/")
        if urllib.parse.urlsplit(url).fragment:
            expected_route += "#" + urllib.parse.urlsplit(url).fragment
        if entry.get("route") != expected_route:
            errors.append(f"route field does not match URL: {url}")
        try:
            target, fragment = route_file(url, base_url)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not target.is_file():
            errors.append(f"missing local target for {url}: {target.relative_to(ROOT)}")
            continue
        parser: TargetParser | None = None
        if target.suffix.lower() in {".html", ".htm"}:
            parser = read_targets(target)
        if fragment and (parser is None or fragment not in parser.targets):
            errors.append(f"missing fragment #{fragment} in {target.relative_to(ROOT)}")

        canonical_route = entry.get("canonical_route")
        if canonical_route:
            canonical_url = urllib.parse.urljoin(base_url, canonical_route)
            canonical_target, _ = route_file(canonical_url, base_url)
            if not canonical_target.is_file():
                errors.append(f"missing canonical target for {url}: {canonical_target.relative_to(ROOT)}")
            if parser is None or canonical_url not in parser.canonicals:
                errors.append(f"compatibility route lacks canonical {canonical_url}: {target.relative_to(ROOT)}")
    return errors


def fetch_live(entry: dict[str, Any], base_url: str, timeout: int) -> dict[str, Any]:
    source = urllib.parse.urlsplit(entry["url"])
    live_root = urllib.parse.urlsplit(base_url.rstrip("/") + "/")
    live_url = urllib.parse.urlunsplit(
        (live_root.scheme, live_root.netloc, live_root.path + source.path.removeprefix("/por-derecho/"), source.query, "")
    )
    request = urllib.request.Request(
        live_url,
        headers={
            "User-Agent": "Por-Derecho-Sent-Email-Link-Continuity/1.0",
            "Cache-Control": "no-cache, no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            status = response.status
    except urllib.error.HTTPError as exc:
        body = exc.read()
        status = exc.code
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"url": entry["url"], "ok": False, "error": f"{type(exc).__name__}: {exc}"}

    fragment = urllib.parse.unquote(source.fragment)
    fragment_ok = True
    if fragment:
        parser = TargetParser()
        parser.feed(body.decode("utf-8", errors="replace"))
        fragment_ok = fragment in parser.targets
    return {
        "url": entry["url"],
        "ok": status == 200 and fragment_ok,
        "status": status,
        "fragment": fragment or None,
        "fragment_ok": fragment_ok,
        "bytes": len(body),
    }


def validate_live(manifest: dict[str, Any], base_url: str, timeout: int, workers: int) -> list[dict[str, Any]]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        return list(executor.map(lambda entry: fetch_live(entry, base_url, timeout), manifest["routes"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--live-base-url")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = validate_local(manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"SENT-EMAIL LINK CONTINUITY: FAIL ({len(errors)} local errors)", file=sys.stderr)
        return 1
    print(f"LOCAL CONTINUITY: PASS ({len(manifest['routes'])} unique sent-email URLs)")

    if args.live_base_url:
        results = validate_live(manifest, args.live_base_url, args.timeout, args.workers)
        failed = [result for result in results if not result["ok"]]
        if failed:
            for result in failed:
                print(f"ERROR: live URL failed: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
            print(f"LIVE CONTINUITY: FAIL ({len(failed)}/{len(results)})", file=sys.stderr)
            return 1
        print(f"LIVE CONTINUITY: PASS ({len(results)} unique sent-email URLs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

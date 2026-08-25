#!/usr/bin/env python3
"""Read-only public-edge verification for Por Derecho Transparency Phase 1."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://sbu001monterecco.github.io/por-derecho"
URLS = {
    "en": f"{BASE}/en/por-derecho/transparency/",
    "es": f"{BASE}/es/por-derecho/transparencia/",
    "script": f"{BASE}/assets/por-derecho/por-derecho.js",
    "sitemap": f"{BASE}/sitemap-por-derecho-foundation.xml",
}
MARKERS = {
    "en": [
        "Transparency before authority.",
        "Por Derecho is an initiative in formation",
        "Gil Marer",
        "PD-SP-P-0001",
        "No independent governing body has been constituted",
        "Phase 1 introduces no new historical actor profile",
        "A consolidated present-tense statement",
        "No response is treated as an admission",
        "https://sbu001monterecco.github.io/por-derecho/es/por-derecho/transparencia/",
    ],
    "es": [
        "Transparencia antes que autoridad.",
        "Por Derecho es una iniciativa en formación",
        "Gil Marer",
        "PD-SP-P-0001",
        "No existe todavía un órgano de gobierno independiente constituido",
        "La Fase 1 no crea ninguna nueva ficha histórica",
        "Está en verificación una declaración consolidada",
        "La falta de respuesta no se trata como admisión",
        "https://sbu001monterecco.github.io/por-derecho/en/por-derecho/transparency/",
    ],
    "script": [
        "pdTransparencyLink",
        "addTransparencyHome",
        "addTransparencyStrip",
        "data-pd-transparency-phase1",
        "/por-derecho/en/por-derecho/transparency/",
        "/por-derecho/es/por-derecho/transparencia/",
    ],
    "sitemap": [
        "https://sbu001monterecco.github.io/por-derecho/en/por-derecho/transparency/",
        "https://sbu001monterecco.github.io/por-derecho/es/por-derecho/transparencia/",
    ],
}
MIN_BYTES = {"en": 12000, "es": 12000, "script": 10000, "sitemap": 3000}


def fetch(url: str, cache_token: str, attempts: int, delay: float) -> tuple[bytes, dict[str, str]]:
    parsed = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query.append(("pdtr", cache_token))
    cache_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urllib.parse.urlencode(query), parsed.fragment))
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        request = urllib.request.Request(
            cache_url,
            headers={
                "User-Agent": "Por-Derecho-Transparency-Live-Verifier/1.0",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read()
                status = getattr(response, "status", response.getcode())
                if status != 200:
                    raise RuntimeError(f"HTTP {status}")
                headers = {key.lower(): value for key, value in response.headers.items()}
                return body, headers
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError) as exc:
            last_error = exc
            if attempt < attempts:
                time.sleep(delay)
    raise RuntimeError(f"failed to fetch {url} after {attempts} attempts: {last_error}")


def verify_resource(name: str, url: str, cache_token: str, attempts: int, delay: float) -> dict[str, object]:
    body, headers = fetch(url, cache_token, attempts, delay)
    text = body.decode("utf-8", errors="replace")
    errors: list[str] = []
    if len(body) < MIN_BYTES[name]:
        errors.append(f"response too small: {len(body)} < {MIN_BYTES[name]}")
    for marker in MARKERS[name]:
        if marker not in text:
            errors.append(f"missing marker: {marker}")
    return {
        "name": name,
        "url": url,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "content_type": headers.get("content-type", ""),
        "etag": headers.get("etag", ""),
        "last_modified": headers.get("last-modified", ""),
        "markers_checked": len(MARKERS[name]),
        "passed": not errors,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-merge-sha", required=True)
    parser.add_argument("--output", default="artifacts/transparency/phase1-live-readback.json")
    parser.add_argument("--attempts", type=int, default=12)
    parser.add_argument("--delay", type=float, default=10.0)
    args = parser.parse_args()

    results: list[dict[str, object]] = []
    failures: list[str] = []
    for name, url in URLS.items():
        try:
            result = verify_resource(name, url, args.expected_merge_sha, args.attempts, args.delay)
        except Exception as exc:
            result = {
                "name": name,
                "url": url,
                "passed": False,
                "errors": [str(exc)],
            }
        results.append(result)
        if not result.get("passed"):
            failures.append(name)

    payload = {
        "schema": "por-derecho.transparency-phase1-live-readback.v1",
        "release_id": "PD-TR-20260825-01",
        "expected_merge_sha": args.expected_merge_sha,
        "verified_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "host": BASE,
        "result": "PASS" if not failures else "FAIL",
        "failed_resources": failures,
        "resources": results,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for result in results:
        state = "PASS" if result.get("passed") else "FAIL"
        print(f"{state} {result['name']}: {result['url']}")
        for error in result.get("errors", []):
            print(f"  - {error}")
    print(f"Transparency Phase 1 public-edge verification: {payload['result']} -> {output}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

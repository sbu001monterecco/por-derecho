#!/usr/bin/env python3
"""Verify the deployed Cuatrecasas/book routes from an external runner.

This validator checks the actual GitHub Pages HTTP responses, not the checked-out
working tree. It is intentionally dependency-free so it can run in GitHub
Actions and produce a compact JSON verification record.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://sbu001monterecco.github.io/por-derecho"

ROUTES: dict[str, dict[str, Any]] = {
    "book_en": {
        "path": "/en/books/four-green-houses-one-red-hotel/",
        "markers": [
            'data-publication-control="book-4gh1rh-professional-inversion-20260831"',
            "The central inversion:",
            "Maximum accountable pressure.",
            "The La Laguna–Las Palmas map.",
            'href="../../cuatrecasas-critical-gaps/"',
        ],
    },
    "book_es": {
        "path": "/es/libros/four-green-houses-one-red-hotel/",
        "markers": [
            'data-publication-control="book-4gh1rh-professional-inversion-20260831"',
            "La inversión central:",
            "Máxima presión responsable.",
            "El mapa La Laguna–Las Palmas.",
            'href="../../cuatrecasas-brechas-criticas/"',
        ],
    },
    "gaps_en": {
        "path": "/en/cuatrecasas-critical-gaps/",
        "markers": [
            'data-publication-control="cuatrecasas-critical-gaps-20260831"',
            "CG-011",
            "CG-012",
            "La Laguna → Las Palmas directional bridge",
            'href="../books/four-green-houses-one-red-hotel/"',
        ],
    },
    "gaps_es": {
        "path": "/es/cuatrecasas-brechas-criticas/",
        "markers": [
            'data-publication-control="cuatrecasas-critical-gaps-20260831"',
            "CG-011",
            "CG-012",
            "Puente direccional La Laguna → Las Palmas",
            'href="../libros/four-green-houses-one-red-hotel/"',
        ],
    },
}


def fetch_html(url: str, retries: int, timeout: int) -> tuple[int, str, str, dict[str, str]]:
    """Fetch one live URL with bounded retries and cache-busting."""
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        query = urlencode({"pd_live_verify": f"20260831-{attempt}-{int(time.time())}"})
        request_url = f"{url}?{query}"
        request = Request(
            request_url,
            headers={
                "User-Agent": "Por-Derecho-Live-Verification/1.0 (+GitHub-Actions)",
                "Accept": "text/html,application/xhtml+xml",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            },
        )
        try:
            with urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed public URLs
                status = int(response.status)
                raw = response.read()
                text = raw.decode("utf-8")
                headers = {key.lower(): value for key, value in response.headers.items()}
                return status, response.geturl(), text, headers
        except (HTTPError, URLError, TimeoutError, UnicodeDecodeError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(min(2 * attempt, 8))
    raise RuntimeError(f"failed to fetch {url} after {retries} attempts: {last_error}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--deployment-sha", required=True)
    parser.add_argument("--pages-run-id", required=True, type=int)
    parser.add_argument(
        "--output",
        default="artifacts/cuatrecasas-book-live-verification.json",
    )
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    verified_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    results: dict[str, Any] = {}
    failures: list[str] = []

    for route_id, spec in ROUTES.items():
        url = f"{base_url}{spec['path']}"
        try:
            status, final_url, html, headers = fetch_html(
                url, retries=args.retries, timeout=args.timeout
            )
        except RuntimeError as exc:
            failures.append(str(exc))
            results[route_id] = {"url": url, "ok": False, "error": str(exc)}
            continue

        missing = [marker for marker in spec["markers"] if marker not in html]
        content_type = headers.get("content-type", "")
        ok = status == 200 and "text/html" in content_type and not missing
        if not ok:
            failures.append(
                f"{route_id}: status={status}, content-type={content_type!r}, "
                f"missing={missing}"
            )

        results[route_id] = {
            "url": url,
            "final_url": final_url,
            "http_status": status,
            "content_type": content_type,
            "bytes": len(html.encode("utf-8")),
            "sha256": hashlib.sha256(html.encode("utf-8")).hexdigest(),
            "required_markers": spec["markers"],
            "missing_markers": missing,
            "ok": ok,
        }

    record = {
        "schema": "por-derecho.live-route-verification.v1",
        "control_id": "PD-4C-BOOK-LIVE-20260831-01",
        "verified_at_utc": verified_at,
        "base_url": base_url,
        "deployment_sha": args.deployment_sha,
        "pages_run_id": args.pages_run_id,
        "route_count": len(ROUTES),
        "all_routes_verified": not failures,
        "routes": results,
        "failures": failures,
        "method": "External GitHub-hosted HTTPS GET with cache-busting and exact marker checks",
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2, ensure_ascii=False))

    if failures:
        print("Live verification failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(
        f"Verified {len(ROUTES)} live routes for deployment {args.deployment_sha} "
        f"(Pages run {args.pages_run_id})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

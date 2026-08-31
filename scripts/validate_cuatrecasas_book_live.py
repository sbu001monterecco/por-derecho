#!/usr/bin/env python3
"""Verify deployed Cuatrecasas/book routes and the Four Green Houses cover.

This validator checks actual GitHub Pages HTTP responses from an external runner,
not the checked-out working tree. It verifies the established book/gap routes,
the bilingual Cuatrecasas source pages, the global loader, the self-limiting
cover insert and the exact published JPEG bytes.
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
COVER_SHA256 = "0476f4fab7e8fa15451d30d6badc81623781db3c3058edd09d3d788013062b34"
COVER_BYTES = 221210

RESOURCES: dict[str, dict[str, Any]] = {
    "book_en": {
        "path": "/en/books/four-green-houses-one-red-hotel/",
        "kind": "text",
        "content_types": ["text/html"],
        "markers": [
            'data-publication-control="book-4gh1rh-professional-inversion-20260831"',
            "The central inversion:",
            "Maximum accountable pressure.",
            "The La Laguna–Las Palmas map.",
            'href="../../cuatrecasas-critical-gaps/"',
            'src="../../../assets/book-covers/locked/four-green-houses-one-red-hotel.jpg"',
        ],
    },
    "book_es": {
        "path": "/es/libros/four-green-houses-one-red-hotel/",
        "kind": "text",
        "content_types": ["text/html"],
        "markers": [
            'data-publication-control="book-4gh1rh-professional-inversion-20260831"',
            "La inversión central:",
            "Máxima presión responsable.",
            "El mapa La Laguna–Las Palmas.",
            'href="../../cuatrecasas-brechas-criticas/"',
            'src="../../../assets/book-covers/locked/four-green-houses-one-red-hotel.jpg"',
        ],
    },
    "gaps_en": {
        "path": "/en/cuatrecasas-critical-gaps/",
        "kind": "text",
        "content_types": ["text/html"],
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
        "kind": "text",
        "content_types": ["text/html"],
        "markers": [
            'data-publication-control="cuatrecasas-critical-gaps-20260831"',
            "CG-011",
            "CG-012",
            "Puente direccional La Laguna → Las Palmas",
            'href="../libros/four-green-houses-one-red-hotel/"',
        ],
    },
    "cuatrecasas_en": {
        "path": "/en/cuatrecasas-sun-park/",
        "kind": "text",
        "content_types": ["text/html"],
        "markers": [
            "Cuatrecasas and Sun Park: position after the unitary reverse-engineering review.",
            'src="../../assets/site.js"',
        ],
    },
    "cuatrecasas_es": {
        "path": "/es/cuatrecasas-sun-park/",
        "kind": "text",
        "content_types": ["text/html"],
        "markers": [
            "Cuatrecasas y Sun Park: posición tras la redigestión unitaria.",
            'src="../../assets/site.js"',
        ],
    },
    "site_loader": {
        "path": "/assets/site.js",
        "kind": "text",
        "content_types": ["application/javascript", "text/javascript", "text/plain"],
        "markers": [
            "cuatrecasas-four-green-houses-one-red-hotel-cover-20260831.js?v=20260831a",
            "data-cuatrecasas-four-green-houses-loader",
            "loadCuatrecasasLinkedInRecord();",
            "loadCuatrecasasBookCover();",
        ],
    },
    "cover_insert_js": {
        "path": "/assets/cuatrecasas-four-green-houses-one-red-hotel-cover-20260831.js",
        "kind": "text",
        "content_types": ["application/javascript", "text/javascript", "text/plain"],
        "markers": [
            "data-four-green-houses-cover-link",
            "../books/four-green-houses-one-red-hotel/",
            "../libros/four-green-houses-one-red-hotel/",
            "../../assets/book-covers/locked/four-green-houses-one-red-hotel.jpg",
            "No Monopoly® logo, board, mascot, cards, typography or branded game pieces are used.",
        ],
    },
    "cover_jpeg": {
        "path": "/assets/book-covers/locked/four-green-houses-one-red-hotel.jpg",
        "kind": "binary",
        "content_types": ["image/jpeg"],
        "expected_sha256": COVER_SHA256,
        "expected_bytes": COVER_BYTES,
    },
}


def fetch_resource(url: str, retries: int, timeout: int) -> tuple[int, str, bytes, dict[str, str]]:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        query = urlencode({"pd_live_verify": f"20260831-cover-{attempt}-{int(time.time())}"})
        request_url = f"{url}?{query}"
        request = Request(
            request_url,
            headers={
                "User-Agent": "Por-Derecho-Live-Verification/1.1 (+GitHub-Actions)",
                "Accept": "*/*",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            },
        )
        try:
            with urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed public URLs
                return (
                    int(response.status),
                    response.geturl(),
                    response.read(),
                    {key.lower(): value for key, value in response.headers.items()},
                )
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(min(2 * attempt, 8))
    raise RuntimeError(f"failed to fetch {url} after {retries} attempts: {last_error}")


def accepted_content_type(actual: str, allowed: list[str]) -> bool:
    lowered = actual.lower()
    return any(expected.lower() in lowered for expected in allowed)


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

    for resource_id, spec in RESOURCES.items():
        url = f"{base_url}{spec['path']}"
        try:
            status, final_url, raw, headers = fetch_resource(
                url, retries=args.retries, timeout=args.timeout
            )
        except RuntimeError as exc:
            failures.append(str(exc))
            results[resource_id] = {"url": url, "ok": False, "error": str(exc)}
            continue

        content_type = headers.get("content-type", "")
        digest = hashlib.sha256(raw).hexdigest()
        size = len(raw)
        type_ok = accepted_content_type(content_type, spec["content_types"])
        missing: list[str] = []
        text_error: str | None = None

        if spec["kind"] == "text":
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                text = ""
                text_error = str(exc)
            missing = [marker for marker in spec.get("markers", []) if marker not in text]
            ok = status == 200 and type_ok and text_error is None and not missing
        else:
            expected_sha = spec.get("expected_sha256")
            expected_bytes = spec.get("expected_bytes")
            ok = (
                status == 200
                and type_ok
                and digest == expected_sha
                and size == expected_bytes
            )

        if not ok:
            failures.append(
                f"{resource_id}: status={status}, content-type={content_type!r}, "
                f"bytes={size}, sha256={digest}, missing={missing}, decode_error={text_error}"
            )

        results[resource_id] = {
            "url": url,
            "final_url": final_url,
            "http_status": status,
            "content_type": content_type,
            "bytes": size,
            "sha256": digest,
            "required_markers": spec.get("markers", []),
            "missing_markers": missing,
            "expected_sha256": spec.get("expected_sha256"),
            "expected_bytes": spec.get("expected_bytes"),
            "ok": ok,
        }

    record = {
        "schema": "por-derecho.live-route-verification.v2",
        "control_id": "PD-4C-BOOK-COVER-LIVE-20260831-02",
        "verified_at_utc": verified_at,
        "base_url": base_url,
        "deployment_sha": args.deployment_sha,
        "pages_run_id": args.pages_run_id,
        "resource_count": len(RESOURCES),
        "all_resources_verified": not failures,
        "resources": results,
        "failures": failures,
        "method": "External GitHub-hosted HTTPS GET with cache-busting, exact marker checks and exact JPEG SHA-256/byte verification",
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
        f"Verified {len(RESOURCES)} live resources for deployment {args.deployment_sha} "
        f"(Pages run {args.pages_run_id})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

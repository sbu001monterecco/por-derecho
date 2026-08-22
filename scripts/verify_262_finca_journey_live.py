#!/usr/bin/env python3
"""Read back the deployed public 262-finca journey after a main-branch release."""
from __future__ import annotations

import argparse
import json
import time
import urllib.request
from pathlib import Path


DEFAULT_BASE = "https://sbu001monterecco.github.io/por-derecho"


def fetch(url: str, timeout: int, attempt: int) -> tuple[int, str]:
    separator = "&" if "?" in url else "?"
    request = urllib.request.Request(
        f"{url}{separator}journey_livecheck={int(time.time())}-{attempt}",
        headers={
            "User-Agent": "por-derecho-262-finca-live-verifier/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status, response.read().decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--attempts", type=int, default=8)
    parser.add_argument("--interval", type=int, default=15)
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument("--output", type=Path, default=Path("artifacts/262-finca-journey-live/latest.json"))
    args = parser.parse_args()
    base = args.base.rstrip("/")
    targets = {
        "en_journey": (f"{base}/en/262-properties-journey-2008-present/", ["data-finca-journey", "The 262-property journey", "finca-journey-2008-present-20260822.js"]),
        "es_journey": (f"{base}/es/fincas-262-recorrido-2008-hoy/", ["data-finca-journey", "El recorrido de 262 fincas", "finca-journey-2008-present-20260822.js"]),
        "projection": (f"{base}/assets/data/sun-park-262-finca-journey-v1.json", ["sun-park-262-finca-journey/v1", '"total_properties": 262', "FINCA-8588-2016-06-01-DEED"]),
        "explorer_js": (f"{base}/assets/finca-journey-2008-present-20260822.js", ["data-finca-journey", "sun-park-262-finca-journey-v1.json", "textContent"]),
        "explorer_css": (f"{base}/assets/finca-journey-2008-present-20260822.css", ["fj-explorer", "fj-property-list"]),
        "governance_sitemap": (f"{base}/sitemap-case-governance.xml", ["262-properties-journey-2008-present", "fincas-262-recorrido-2008-hoy", "sun-park-forensic-map-262-properties"]),
        "en_map": (f"{base}/en/sun-park-forensic-map-262-properties/", ["262-properties-journey-2008-present"]),
        "es_map": (f"{base}/es/mapa-forense-sun-park-262-fincas/", ["fincas-262-recorrido-2008-hoy"]),
        "en_registry": (f"{base}/en/land-registry-implementation-property-by-property/", ["sun-park-forensic-map-262-properties", "262-properties-journey-2008-present"]),
        "es_registry": (f"{base}/es/implementacion-registral-finca-por-finca/", ["mapa-forense-sun-park-262-fincas", "fincas-262-recorrido-2008-hoy"]),
    }
    last: dict = {}
    for attempt in range(1, args.attempts + 1):
        checks: dict[str, bool] = {}
        details: dict[str, dict] = {}
        for name, (url, markers) in targets.items():
            try:
                status, body = fetch(url, args.timeout, attempt)
                marker_results = {marker: marker in body for marker in markers}
                checks[name] = status == 200 and all(marker_results.values())
                details[name] = {"status": status, "bytes": len(body.encode("utf-8")), "markers": marker_results}
                if name == "projection" and checks[name]:
                    projection = json.loads(body)
                    properties = projection.get("properties", [])
                    checks[name] = len(properties) == 262 and projection.get("coverage", {}).get("total_properties") == 262
                    details[name]["property_count"] = len(properties)
            except Exception as exc:  # Network propagation is expected to be transient.
                checks[name] = False
                details[name] = {"error": repr(exc)}
        last = {"attempt": attempt, "base": base, "checks": checks, "details": details}
        print(json.dumps(last, ensure_ascii=False, indent=2))
        if all(checks.values()):
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps({"status": "PASS", **last}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print("262_FINCA_JOURNEY_LIVE_VERIFIED")
            return 0
        if attempt < args.attempts:
            time.sleep(args.interval)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"status": "FAIL", **last}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

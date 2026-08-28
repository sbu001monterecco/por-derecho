#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

BASE = os.environ.get("PSR_BASE_URL", "https://sbu001monterecco.github.io/por-derecho").rstrip("/")
SCOPE = "LIVE" if BASE.startswith("https://") else "CHECKOUT"
ATTEMPTS = 30
SLEEP_SECONDS = 10
TIMEOUT_SECONDS = 25

REQUIRED = {
    "/assets/site.js": ["site-pre-treasury-154-hq-20260828.js?v=20260828a"],
    "/assets/site-pre-treasury-154-hq-20260828.js": [
        "san-telmo-attribution-correction-20260819.js?v=20260819a",
        "data-san-telmo-attribution-loader",
    ],
    "/assets/san-telmo-attribution-correction-20260819.js": [
        "Speaker correction.",
        "Corrección de atribución.",
        "Eduardo Sánchez · 08:08–08:12",
        "The programme title identifies Enrique Guerra as the guest",
        "El título del programa identifica a Enrique Guerra como invitado",
    ],
    "/en/san-telmo-ricpe-sun-park/": [
        "The direct public source",
        "Proposition-by-proposition evidence map",
        "Same hotel complex and connected project perimeter—not one undivided legal asset.",
    ],
    "/es/san-telmo-ricpe-sun-park/": [
        "La fuente pública directa",
        "Mapa probatorio, proposición por proposición",
        "El mismo complejo hotelero y perímetro de proyecto conectado; no un único activo jurídico indivisible.",
    ],
    "/sitemap-san-telmo.xml": [
        "/en/san-telmo-ricpe-sun-park/",
        "/es/san-telmo-ricpe-sun-park/",
    ],
    "/robots.txt": [
        "Sitemap: https://sbu001monterecco.github.io/por-derecho/sitemap-san-telmo.xml",
    ],
}


def fetch(path: str) -> tuple[int, str, int, str]:
    url = f"{BASE}{path}"
    separator = "&" if "?" in url else "?"
    req = urllib.request.Request(
        f"{url}{separator}pd_verify={int(time.time())}",
        headers={
            "User-Agent": "Por-Derecho-San-Telmo-Live-Verification/1.0",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
        body = response.read()
        return int(response.status), body.decode("utf-8", errors="replace"), len(body), response.headers.get("Content-Type", "")


def verify_once() -> dict[str, object]:
    resources = []
    for path, markers in REQUIRED.items():
        status, text, size, content_type = fetch(path)
        if status != 200:
            raise AssertionError(f"{path}: HTTP {status}")
        missing = [marker for marker in markers if marker not in text]
        if missing:
            raise AssertionError(f"{path}: missing {missing}")
        resources.append({"path": path, "status": status, "bytes": size, "content_type": content_type})
    return {
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "base": BASE,
        "resources": resources,
    }


failures: list[str] = []
for attempt in range(1, ATTEMPTS + 1):
    try:
        result = verify_once()
        result["attempt"] = attempt
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"SAN TELMO RENDERED ATTRIBUTION {SCOPE} VERIFICATION: PASS (attempt {attempt}/{ATTEMPTS})")
        raise SystemExit(0)
    except (AssertionError, urllib.error.URLError, TimeoutError) as exc:
        message = f"attempt {attempt}/{ATTEMPTS}: {type(exc).__name__}: {exc}"
        failures.append(message)
        print(message)
        if attempt < ATTEMPTS:
            time.sleep(SLEEP_SECONDS)

print(f"SAN TELMO RENDERED ATTRIBUTION {SCOPE} VERIFICATION: FAIL")
for failure in failures[-10:]:
    print(f" - {failure}")
raise SystemExit(1)

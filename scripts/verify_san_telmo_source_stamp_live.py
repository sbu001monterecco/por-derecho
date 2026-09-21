#!/usr/bin/env python3
"""Verify the corrected San Telmo / RICPE / Sun Park source stamp at the public edge.

The check waits for GitHub Pages propagation, then verifies the public JavaScript,
loader chain, canonical local images, an authorised Eduardo first-party portrait
source, and every principal route on which the shared component is intended to run.
"""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone

BASE = "https://sbu001monterecco.github.io/por-derecho"
ATTEMPTS = 30
SLEEP_SECONDS = 10
TIMEOUT_SECONDS = 25

SOURCE_ASSET = "/assets/san-telmo-source-stamp-20260819.js"
LOADER_ASSET = "/assets/ricpe-identity-correction-20260815.js"
SITE_ASSET = "/assets/site.js"
SITE_WRAPPER_ASSET = "/assets/site-pre-intervencion-highlight-20260820.js"
PRE_INTERVENCION_ASSET = "/assets/site-pre-intervencion-highlight-before-eg95-20260823.js"
SITE_BASE_ASSET = "/assets/site-base-20260819.js"
BORJA_ASSET = "/assets/actors/francisco-de-borja-rodriguez-batllori.jpg"
SUN_PARK_ASSET = "/assets/sun-park-mynd-yaiza.jpg"

EDUARDO_PRIMARY = (
    "https://res.cloudinary.com/rsmglobal/image/fetch/t_default/f_auto/q_auto/"
    "https%3A/www.rsm.global/spain/sites/default/files/media/01%20Global%20assets/"
    "02_Thumbnails%201240x930px/06_fotos%20profesionales/"
    "Eduardo%20S%C3%A1nchez%20%281%29.jpg"
)
EDUARDO_FALLBACK = (
    "https://abogadossantelmo.com/wp-content/uploads/2022/07/"
    "Eduardo-Sanchez-Iglesias-500x500.jpg"
)

ROUTES = [
    "/en/",
    "/es/",
    "/en/ric-private-equity-sun-park/",
    "/es/ric-private-equity-sun-park/",
    "/en/rsm/nnr4-1025c2f66/",
    "/es/rsm/nnr4-1025c2f66/",
    "/en/insolvency-36-2012-insolvency-administrator/",
    "/es/concurso-36-2012-administrador-concursal/",
    "/en/san-telmo-ricpe-sun-park/",
    "/es/san-telmo-ricpe-sun-park/",
    "/en/pwc-canarias-carlos-saavedra-sun-park/",
    "/es/pwc-canarias-carlos-saavedra-sun-park/",
    "/en/sun-park-takeover-7-june-2018/",
    "/es/toma-control-sun-park-7-junio-2018/",
    "/en/actors-parties-lawyers-representatives/",
    "/es/actores-partes-abogados-representantes/",
    "/en/community-instrumentalisation/",
    "/es/comunidad-instrumentalizacion/",
    "/en/grant-thornton/2024-04/",
    "/es/grant-thornton/2024-04/",
    "/en/grant-thornton/cuyas-canarias/",
    "/es/grant-thornton/cuyas-canarias/",
]

SOURCE_MARKERS = [
    "San Telmo partner Eduardo Sánchez stated that",
    "put clients into the RICPE investment connected to Sun Park",
    "08:08 → 08:12",
    "07:57–08:27",
    "mHn9IJU0qI4&t=488s",
    "person.eduardo-sanchez-san-telmo.primary",
    "place.sun-park-mynd-yaiza.aerial-primary",
    "person.francisco-de-borja-rodriguez-batllori.primary",
    "/assets/sun-park-mynd-yaiza.jpg",
    "/assets/actors/francisco-de-borja-rodriguez-batllori.jpg",
    "does not by itself establish Borja–Eduardo coordination",
]

LOADER_MARKERS = [
    "san-telmo-parallel-lives-red-20260819.js?v=20260819b",
    "san-telmo-source-stamp-20260819.js?v=20260819a",
]

SITE_MARKERS = ["site-pre-intervencion-highlight-20260820.js"]
SITE_WRAPPER_MARKERS = ["site-pre-intervencion-highlight-before-eg95-20260823.js"]
PRE_INTERVENCION_MARKERS = ["site-base-20260819.js"]
SITE_BASE_MARKERS = ["ricpe-identity-correction-20260815.js"]


@dataclass
class Response:
    url: str
    status: int
    content_type: str
    body: bytes

    @property
    def text(self) -> str:
        return self.body.decode("utf-8", errors="replace")


def request(url: str, *, cache_bust: bool = False) -> Response:
    if cache_bust:
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}pd_verify={int(time.time())}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 Por-Derecho-Live-Verification/1.0",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as res:  # noqa: S310
        return Response(
            url=res.geturl(),
            status=int(res.status),
            content_type=res.headers.get("Content-Type", ""),
            body=res.read(),
        )


def assert_markers(name: str, text: str, markers: list[str]) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise AssertionError(f"{name}: missing marker(s): {missing}")


def verify_local_asset(path: str, expected_content_prefix: str) -> dict[str, object]:
    response = request(BASE + path, cache_bust=True)
    if response.status != 200:
        raise AssertionError(f"{path}: HTTP {response.status}")
    if not response.content_type.lower().startswith(expected_content_prefix):
        raise AssertionError(
            f"{path}: expected content type {expected_content_prefix!r}, "
            f"received {response.content_type!r}"
        )
    if not response.body:
        raise AssertionError(f"{path}: empty response")
    return {
        "path": path,
        "status": response.status,
        "content_type": response.content_type,
        "bytes": len(response.body),
    }


def verify_eduardo_image() -> dict[str, object]:
    failures: list[str] = []
    for label, url in (("RSM primary", EDUARDO_PRIMARY), ("San Telmo fallback", EDUARDO_FALLBACK)):
        try:
            response = request(url, cache_bust=False)
            if response.status == 200 and response.content_type.lower().startswith("image/") and response.body:
                return {
                    "source": label,
                    "status": response.status,
                    "content_type": response.content_type,
                    "bytes": len(response.body),
                }
            failures.append(
                f"{label}: status={response.status}, type={response.content_type}, bytes={len(response.body)}"
            )
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{label}: {type(exc).__name__}: {exc}")
    raise AssertionError("No authorised Eduardo portrait source was reachable: " + " | ".join(failures))


def verify_routes() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for route in ROUTES:
        response = request(BASE + route, cache_bust=True)
        if response.status != 200:
            raise AssertionError(f"{route}: HTTP {response.status}")
        content_type = response.content_type.lower()
        if "text/html" not in content_type:
            raise AssertionError(f"{route}: expected text/html, received {response.content_type!r}")
        if "site.js" not in response.text:
            raise AssertionError(f"{route}: site.js loader reference not found")
        results.append({"route": route, "status": 200, "bytes": len(response.body)})
    return results


def verify_once() -> dict[str, object]:
    source = request(BASE + SOURCE_ASSET, cache_bust=True)
    if source.status != 200:
        raise AssertionError(f"source stamp: HTTP {source.status}")
    assert_markers("source stamp", source.text, SOURCE_MARKERS)

    loader = request(BASE + LOADER_ASSET, cache_bust=True)
    if loader.status != 200:
        raise AssertionError(f"loader: HTTP {loader.status}")
    assert_markers("loader", loader.text, LOADER_MARKERS)

    site = request(BASE + SITE_ASSET, cache_bust=True)
    if site.status != 200:
        raise AssertionError(f"site loader: HTTP {site.status}")
    assert_markers("site loader", site.text, SITE_MARKERS)

    site_wrapper = request(BASE + SITE_WRAPPER_ASSET, cache_bust=True)
    if site_wrapper.status != 200:
        raise AssertionError(f"site wrapper: HTTP {site_wrapper.status}")
    assert_markers("site wrapper", site_wrapper.text, SITE_WRAPPER_MARKERS)

    pre_intervencion = request(BASE + PRE_INTERVENCION_ASSET, cache_bust=True)
    if pre_intervencion.status != 200:
        raise AssertionError(f"pre-intervencion loader: HTTP {pre_intervencion.status}")
    assert_markers("pre-intervencion loader", pre_intervencion.text, PRE_INTERVENCION_MARKERS)

    site_base = request(BASE + SITE_BASE_ASSET, cache_bust=True)
    if site_base.status != 200:
        raise AssertionError(f"site base: HTTP {site_base.status}")
    assert_markers("site base", site_base.text, SITE_BASE_MARKERS)

    result = {
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "base": BASE,
        "source_stamp": {
            "status": source.status,
            "content_type": source.content_type,
            "bytes": len(source.body),
            "markers": SOURCE_MARKERS,
        },
        "loader": {
            "status": loader.status,
            "content_type": loader.content_type,
            "bytes": len(loader.body),
            "markers": LOADER_MARKERS,
        },
        "site_loader": {
            "status": site.status,
            "content_type": site.content_type,
            "bytes": len(site.body),
            "markers": SITE_MARKERS,
        },
        "site_wrapper": {
            "status": site_wrapper.status,
            "content_type": site_wrapper.content_type,
            "bytes": len(site_wrapper.body),
            "markers": SITE_WRAPPER_MARKERS,
        },
        "pre_intervencion_loader": {
            "status": pre_intervencion.status,
            "content_type": pre_intervencion.content_type,
            "bytes": len(pre_intervencion.body),
            "markers": PRE_INTERVENCION_MARKERS,
        },
        "site_base": {
            "status": site_base.status,
            "content_type": site_base.content_type,
            "bytes": len(site_base.body),
            "markers": SITE_BASE_MARKERS,
        },
        "borja": verify_local_asset(BORJA_ASSET, "image/"),
        "sun_park": verify_local_asset(SUN_PARK_ASSET, "image/"),
        "eduardo": verify_eduardo_image(),
        "routes": verify_routes(),
    }
    return result


def main() -> int:
    failures: list[str] = []
    for attempt in range(1, ATTEMPTS + 1):
        try:
            result = verify_once()
            result["attempt"] = attempt
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print(
                "SAN TELMO SOURCE STAMP LIVE VERIFICATION: PASS "
                f"({len(ROUTES)} routes; attempt {attempt}/{ATTEMPTS})"
            )
            return 0
        except (AssertionError, urllib.error.URLError, TimeoutError) as exc:
            message = f"attempt {attempt}/{ATTEMPTS}: {type(exc).__name__}: {exc}"
            failures.append(message)
            print(message, file=sys.stderr)
            if attempt < ATTEMPTS:
                time.sleep(SLEEP_SECONDS)

    print("SAN TELMO SOURCE STAMP LIVE VERIFICATION: FAIL", file=sys.stderr)
    for failure in failures[-10:]:
        print(f" - {failure}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

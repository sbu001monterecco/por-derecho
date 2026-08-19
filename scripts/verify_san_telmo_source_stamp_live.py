#!/usr/bin/env python3
"""Verify the corrected San Telmo / RICPE / Sun Park source stamp at the public edge.

The verifier has two layers:

1. HTTP/source verification of the public loader chain, source-stamp JavaScript,
   canonical images, authorised Eduardo portrait source and all controlled routes.
2. Browser verification with Playwright that the stamp actually renders, the three
   image slots load in the correct Eduardo -> Sun Park -> Borja order, the source
   timing is visible, and the homepage placement follows the 5 + AC visual.

This script does not use facial recognition. Identity is controlled by the project's
registered asset IDs and approved source mappings.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE = "https://sbu001monterecco.github.io/por-derecho"
ATTEMPTS = 18
SLEEP_SECONDS = 10
TIMEOUT_SECONDS = 25

SOURCE_ASSET = "/assets/san-telmo-source-stamp-20260819.js"
LOADER_ASSET = "/assets/ricpe-identity-correction-20260815.js"
SITE_ASSET = "/assets/site.js"
SITE_BASE_ASSET = "/assets/site-base-20260819.js"
BORJA_ASSET = "/assets/actors/francisco-de-borja-rodriguez-batllori.jpg"
SUN_PARK_ASSET = "/assets/sun-park-mynd-yaiza.jpg"

ARTIFACT_DIR = Path("artifacts/san-telmo-source-stamp-live")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

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

# The principal pages on which we prove actual browser rendering, not merely HTTP delivery.
RENDER_ROUTES = [
    "/en/",
    "/es/",
    "/en/san-telmo-ricpe-sun-park/",
    "/es/san-telmo-ricpe-sun-park/",
    "/en/ric-private-equity-sun-park/",
    "/es/ric-private-equity-sun-park/",
    "/en/insolvency-36-2012-insolvency-administrator/",
    "/es/concurso-36-2012-administrador-concursal/",
    "/en/rsm/nnr4-1025c2f66/",
    "/es/rsm/nnr4-1025c2f66/",
]

MOBILE_RENDER_ROUTES = [
    "/en/",
    "/es/",
    "/en/san-telmo-ricpe-sun-park/",
    "/es/san-telmo-ricpe-sun-park/",
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

# site.js is now a thin wrapper. The historic loader chain lives in site-base-20260819.js.
SITE_MARKERS = ["site-base-20260819.js?v=20260819a"]
SITE_BASE_MARKERS = ["ricpe-identity-correction-20260815.js?v=20260815a"]

EXPECTED_ASSET_IDS = [
    "person.eduardo-sanchez-san-telmo.primary",
    "place.sun-park-mynd-yaiza.aerial-primary",
    "person.francisco-de-borja-rodriguez-batllori.primary",
]


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
        url = f"{url}{separator}pd_verify={int(time.time() * 1000)}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 Por-Derecho-Live-Verification/2.0",
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


def verify_text_asset(path: str, markers: list[str], name: str) -> dict[str, object]:
    response = request(BASE + path, cache_bust=True)
    if response.status != 200:
        raise AssertionError(f"{name}: HTTP {response.status}")
    if not response.body:
        raise AssertionError(f"{name}: empty response")
    assert_markers(name, response.text, markers)
    return {
        "path": path,
        "status": response.status,
        "content_type": response.content_type,
        "bytes": len(response.body),
        "markers": markers,
    }


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
                    "url": response.url,
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


def browser_executable() -> str | None:
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        candidate = shutil.which(name)
        if candidate:
            return candidate
    return None


def slug_for_route(route: str) -> str:
    slug = route.strip("/") or "root"
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", slug)


def render_one(page: Any, route: str, viewport_label: str) -> dict[str, object]:
    url = f"{BASE}{route}?pd_render={int(time.time() * 1000)}"
    response = page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    if response is None or response.status != 200:
        status = None if response is None else response.status
        raise AssertionError(f"browser {route}: navigation status {status}")

    stamp = page.locator("[data-pd-st-source]")
    stamp.wait_for(state="visible", timeout=50_000)
    page.wait_for_function(
        """() => {
          const root = document.querySelector('[data-pd-st-source]');
          if (!root) return false;
          const imgs = [...root.querySelectorAll('img[data-visual-asset-id]')];
          return imgs.length === 3 && imgs.every(img => img.complete);
        }""",
        timeout=35_000,
    )

    data = page.evaluate(
        """() => {
          const stamp = document.querySelector('[data-pd-st-source]');
          const imgs = [...stamp.querySelectorAll('img[data-visual-asset-id]')].map(img => ({
            assetId: img.dataset.visualAssetId,
            src: img.currentSrc || img.src,
            naturalWidth: img.naturalWidth,
            naturalHeight: img.naturalHeight,
            complete: img.complete,
            alt: img.alt
          }));
          const five = document.querySelector('[data-pd-five-ac]');
          const parallel = document.querySelector('[data-pd-parallel-lives]');
          const sourceLink = stamp.querySelector('.pd-st-source__source a');
          const rect = stamp.getBoundingClientRect();
          return {
            text: stamp.innerText,
            assetIds: imgs.map(x => x.assetId),
            images: imgs,
            sourceHref: sourceLink ? sourceLink.href : '',
            visible: rect.width > 0 && rect.height > 0,
            width: rect.width,
            height: rect.height,
            documentScrollWidth: document.documentElement.scrollWidth,
            viewportWidth: window.innerWidth,
            followsFive: five ? Boolean(five.compareDocumentPosition(stamp) & Node.DOCUMENT_POSITION_FOLLOWING) : null,
            precedesParallel: parallel ? Boolean(stamp.compareDocumentPosition(parallel) & Node.DOCUMENT_POSITION_FOLLOWING) : null
          };
        }"""
    )

    if not data["visible"]:
        raise AssertionError(f"browser {route}: stamp is not visible")
    if data["assetIds"] != EXPECTED_ASSET_IDS:
        raise AssertionError(
            f"browser {route}: image slot order mismatch: {data['assetIds']} != {EXPECTED_ASSET_IDS}"
        )
    failed_images = [
        image
        for image in data["images"]
        if not image["complete"] or image["naturalWidth"] <= 0 or image["naturalHeight"] <= 0
    ]
    if failed_images:
        raise AssertionError(f"browser {route}: image(s) did not render: {failed_images}")

    required_text = [
        "el despacho",
        "RICPE",
        "SUN PARK",
        "08:08",
        "08:12",
        "07:57–08:27",
    ]
    missing_text = [marker for marker in required_text if marker not in data["text"]]
    if missing_text:
        raise AssertionError(f"browser {route}: missing rendered text {missing_text}")
    if "mHn9IJU0qI4" not in data["sourceHref"] or "t=488" not in data["sourceHref"]:
        raise AssertionError(f"browser {route}: source link is wrong: {data['sourceHref']}")
    if route in {"/en/", "/es/"} and data["followsFive"] is not True:
        raise AssertionError(f"browser {route}: source stamp does not follow the 5 + AC visual")
    if data["precedesParallel"] is not True:
        raise AssertionError(f"browser {route}: source stamp does not precede the analytical parallel-lives block")
    if data["documentScrollWidth"] > data["viewportWidth"] + 2:
        raise AssertionError(
            f"browser {route}: horizontal overflow {data['documentScrollWidth']} > {data['viewportWidth']}"
        )

    screenshot = ARTIFACT_DIR / f"{viewport_label}-{slug_for_route(route)}.png"
    stamp.screenshot(path=str(screenshot), animations="disabled")

    return {
        "route": route,
        "url": url,
        "viewport": viewport_label,
        "asset_ids": data["assetIds"],
        "images": data["images"],
        "source_href": data["sourceHref"],
        "follows_five": data["followsFive"],
        "precedes_parallel": data["precedesParallel"],
        "stamp_width": data["width"],
        "stamp_height": data["height"],
        "screenshot": str(screenshot),
    }


def verify_rendered_pages() -> dict[str, object]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:  # pragma: no cover - CI installation is mandatory
        raise AssertionError("Playwright is not installed; rendered verification cannot run") from exc

    executable = browser_executable()
    desktop_results: list[dict[str, object]] = []
    mobile_results: list[dict[str, object]] = []

    with sync_playwright() as playwright:
        launch_kwargs: dict[str, Any] = {
            "headless": True,
            "args": ["--no-sandbox", "--disable-dev-shm-usage"],
        }
        if executable:
            launch_kwargs["executable_path"] = executable
        browser = playwright.chromium.launch(**launch_kwargs)
        try:
            desktop = browser.new_context(viewport={"width": 1600, "height": 1200}, device_scale_factor=1)
            try:
                page = desktop.new_page()
                for route in RENDER_ROUTES:
                    desktop_results.append(render_one(page, route, "desktop"))
            finally:
                desktop.close()

            mobile = browser.new_context(
                viewport={"width": 390, "height": 844},
                device_scale_factor=1,
                is_mobile=True,
                has_touch=True,
            )
            try:
                page = mobile.new_page()
                for route in MOBILE_RENDER_ROUTES:
                    mobile_results.append(render_one(page, route, "mobile"))
            finally:
                mobile.close()
        finally:
            browser.close()

    return {
        "browser_executable": executable or "playwright-managed chromium",
        "desktop": desktop_results,
        "mobile": mobile_results,
    }


def verify_once() -> dict[str, object]:
    result = {
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "base": BASE,
        "source_stamp": verify_text_asset(SOURCE_ASSET, SOURCE_MARKERS, "source stamp"),
        "loader": verify_text_asset(LOADER_ASSET, LOADER_MARKERS, "RICPE loader"),
        "site_wrapper": verify_text_asset(SITE_ASSET, SITE_MARKERS, "site wrapper"),
        "site_base": verify_text_asset(SITE_BASE_ASSET, SITE_BASE_MARKERS, "site base loader"),
        "borja": verify_local_asset(BORJA_ASSET, "image/"),
        "sun_park": verify_local_asset(SUN_PARK_ASSET, "image/"),
        "eduardo": verify_eduardo_image(),
        "routes": verify_routes(),
    }
    result["rendered"] = verify_rendered_pages()
    return result


def main() -> int:
    failures: list[str] = []
    for attempt in range(1, ATTEMPTS + 1):
        try:
            result = verify_once()
            result["attempt"] = attempt
            report = ARTIFACT_DIR / "verification-report.json"
            report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print(
                "SAN TELMO SOURCE STAMP LIVE VERIFICATION: PASS "
                f"({len(ROUTES)} HTTP routes; {len(RENDER_ROUTES)} desktop renders; "
                f"{len(MOBILE_RENDER_ROUTES)} mobile renders; attempt {attempt}/{ATTEMPTS})"
            )
            return 0
        except (
            AssertionError,
            urllib.error.URLError,
            TimeoutError,
            OSError,
        ) as exc:
            message = f"attempt {attempt}/{ATTEMPTS}: {type(exc).__name__}: {exc}"
            failures.append(message)
            print(message, file=sys.stderr)
            if attempt < ATTEMPTS:
                time.sleep(SLEEP_SECONDS)

    failure_report = ARTIFACT_DIR / "verification-failures.json"
    failure_report.write_text(json.dumps(failures, ensure_ascii=False, indent=2), encoding="utf-8")
    print("SAN TELMO SOURCE STAMP LIVE VERIFICATION: FAIL", file=sys.stderr)
    for failure in failures[-10:]:
        print(f" - {failure}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

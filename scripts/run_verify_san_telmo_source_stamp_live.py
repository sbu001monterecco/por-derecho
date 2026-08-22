#!/usr/bin/env python3
"""Run the San Telmo live verifier with the canonical section selector.

The source-stamp stylesheet and the rendered section both carry a historical
`data-pd-st-source` attribute. Playwright strict mode therefore needs the exact
section selector rather than the broad attribute selector. This wrapper keeps the
main verifier reusable while replacing only its rendered-page function.
"""

from __future__ import annotations

import time
from typing import Any

import verify_san_telmo_source_stamp_live as base

STAMP_SELECTOR = 'section[data-pd-st-source="true"]'


def render_one(page: Any, route: str, viewport_label: str) -> dict[str, object]:
    url = f"{base.BASE}{route}?pd_render={int(time.time() * 1000)}"
    response = page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    if response is None or response.status != 200:
        status = None if response is None else response.status
        raise AssertionError(f"browser {route}: navigation status {status}")

    stamp = page.locator(STAMP_SELECTOR)
    stamp.wait_for(state="visible", timeout=50_000)
    page.wait_for_function(
        """selector => {
          const root = document.querySelector(selector);
          if (!root) return false;
          const imgs = [...root.querySelectorAll('img[data-visual-asset-id]')];
          return imgs.length === 3 && imgs.every(img => img.complete);
        }""",
        arg=STAMP_SELECTOR,
        timeout=35_000,
    )

    data = page.evaluate(
        """selector => {
          const stamp = document.querySelector(selector);
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
        }""",
        STAMP_SELECTOR,
    )

    if not data["visible"]:
        raise AssertionError(f"browser {route}: stamp is not visible")
    if data["assetIds"] != base.EXPECTED_ASSET_IDS:
        raise AssertionError(
            f"browser {route}: image slot order mismatch: "
            f"{data['assetIds']} != {base.EXPECTED_ASSET_IDS}"
        )

    failed_images = [
        image
        for image in data["images"]
        if not image["complete"] or image["naturalWidth"] <= 0 or image["naturalHeight"] <= 0
    ]
    if failed_images:
        raise AssertionError(f"browser {route}: image(s) did not render: {failed_images}")

    required_text = ["el despacho", "RICPE", "SUN PARK", "08:08", "08:12", "07:57–08:27"]
    missing_text = [marker for marker in required_text if marker not in data["text"]]
    if missing_text:
        raise AssertionError(f"browser {route}: missing rendered text {missing_text}")
    if "mHn9IJU0qI4" not in data["sourceHref"] or "t=488" not in data["sourceHref"]:
        raise AssertionError(f"browser {route}: source link is wrong: {data['sourceHref']}")
    if route in {"/en/", "/es/"} and data["followsFive"] is not True:
        raise AssertionError(f"browser {route}: source stamp does not follow the 5 + AC visual")
    if data["precedesParallel"] is not True:
        raise AssertionError(
            f"browser {route}: source stamp does not precede the analytical parallel-lives block"
        )
    if data["documentScrollWidth"] > data["viewportWidth"] + 2:
        raise AssertionError(
            f"browser {route}: horizontal overflow "
            f"{data['documentScrollWidth']} > {data['viewportWidth']}"
        )

    screenshot = base.ARTIFACT_DIR / f"{viewport_label}-{base.slug_for_route(route)}.png"
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


base.render_one = render_one

if __name__ == "__main__":
    raise SystemExit(base.main())

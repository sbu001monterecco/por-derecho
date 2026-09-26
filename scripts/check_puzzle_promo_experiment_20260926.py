#!/usr/bin/env python3
"""Read-only browser acceptance for the isolated Puzzle floating-promo experiment."""
from __future__ import annotations
import argparse
import functools
import http.server
import json
from pathlib import Path
import threading
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

ROUTES = [
    ("r33-en", "en/insolvency-36-2012-ac-opposition-lpb-appeal-september-2026/", "en"),
    ("r33-es", "es/concurso-36-2012-oposicion-ac-apelacion-lpb-septiembre-2026/", "es"),
    ("jtp-en", "en/estate-payment-counsel-independence/", "en"),
    ("jtp-es", "es/pago-masa-independencia-defensa/", "es"),
]
VIEWPORTS = [
    ("desktop", 1440, 900, False),
    ("tablet", 820, 1180, True),
    ("phone", 390, 844, True),
    ("phone-landscape", 844, 390, True),
]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def serve(root: Path):
    handler = functools.partial(QuietHandler, directory=str(root))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, f"http://127.0.0.1:{server.server_address[1]}/"


def inspect(page, width: int, height: int, lang: str):
    promo = page.locator("[data-pd-puzzle-promo]")
    promo.wait_for(state="visible", timeout=5000)
    box = promo.bounding_box()
    assert box, "promo has no bounding box"
    assert box["x"] >= -1 and box["y"] >= -1, box
    assert box["x"] + box["width"] <= width + 1, (width, box)
    assert box["y"] + box["height"] <= height + 1, (height, box)
    assert box["x"] < width / 2, ("promo is not left-anchored", box)
    close = page.locator(".pd-puzzle-promo__close").bounding_box()
    assert close and close["width"] >= 43 and close["height"] >= 43, close
    href = page.locator(".pd-puzzle-promo__link").get_attribute("href")
    expected = f"/{lang}/puzzle/#p2"
    assert expected in href, (expected, href)
    assert page.evaluate("getComputedStyle(document.querySelector('[data-pd-puzzle-promo]')).position") == "fixed"
    if width <= 700:
        assert box["width"] <= 155, box
    else:
        assert box["width"] <= 225, box
    if height <= 500:
        assert box["width"] <= 132, box
    return {"box": box, "close": close, "href": href}


def run(root: Path, output: Path):
    output.mkdir(parents=True, exist_ok=True)
    server, thread, base = serve(root)
    results = []
    failures = []
    try:
        with sync_playwright() as pw:
            for engine_name in ("chromium", "firefox", "webkit"):
                browser = getattr(pw, engine_name).launch(headless=True)
                try:
                    for route_name, route, lang in ROUTES:
                        for label, width, height, touch in VIEWPORTS:
                            context = browser.new_context(
                                viewport={"width": width, "height": height},
                                has_touch=touch,
                                locale="es-ES" if lang == "es" else "en-GB",
                                reduced_motion="reduce",
                            )
                            page = context.new_page()
                            errors = []
                            page.on("pageerror", lambda err: errors.append(str(err)))
                            row = {
                                "engine": engine_name,
                                "route": route_name,
                                "viewport": label,
                                "width": width,
                                "height": height,
                            }
                            try:
                                url = urljoin(base, route) + "?puzzlePromo=1"
                                response = page.goto(url, wait_until="domcontentloaded", timeout=60000)
                                assert response and response.ok, (url, response.status if response else None)
                                row.update(inspect(page, width, height, lang))
                                assert not errors, errors
                                shot = output / f"{engine_name}-{route_name}-{label}.png"
                                page.screenshot(path=str(shot), full_page=False)
                                row["screenshot"] = shot.name

                                # Dismissal is persistent in the same origin/context.
                                page.locator(".pd-puzzle-promo__close").click()
                                assert page.locator("[data-pd-puzzle-promo]").count() == 0
                                page.goto(urljoin(base, route), wait_until="domcontentloaded", timeout=60000)
                                page.wait_for_timeout(250)
                                assert page.locator("[data-pd-puzzle-promo]").count() == 0

                                # Explicit test override must still work after dismissal.
                                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                                row["forced_after_dismiss"] = inspect(page, width, height, lang)["href"]

                                page.emulate_media(media="print")
                                display = page.locator("[data-pd-puzzle-promo]").evaluate("(el)=>getComputedStyle(el).display")
                                assert display == "none", display
                                row["status"] = "PASS"
                            except Exception as exc:
                                row["status"] = "FAIL"
                                row["error"] = repr(exc)
                                failures.append(row.copy())
                            results.append(row)
                            context.close()
                finally:
                    browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    report = {
        "schema": "por-derecho.puzzle-promo-experiment-browser.v1",
        "status": "PASS" if not failures else "FAIL",
        "cases": len(results),
        "failures": failures,
        "results": results,
        "publication_claim": "NONE: isolated branch browser experiment only",
    }
    (output / "results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({"status": report["status"], "cases": report["cases"], "failures": len(failures)}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--output", type=Path, default=Path("artifacts/puzzle-promo-experiment-20260926"))
    args = ap.parse_args()
    run(args.root.resolve(), args.output.resolve())

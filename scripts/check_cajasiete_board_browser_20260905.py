#!/usr/bin/env python3
"""Bounded, source-specific browser checks. Does not publish or alter source pages."""
from __future__ import annotations
import argparse
import functools
import hashlib
import http.server
import json
import threading
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ('es/cajasiete-sun-park-financiacion-comparabilidad/',
          'en/cajasiete-sun-park-financing-comparability/')
REPORT = ROOT / 'ops/CAJASIETE_BOARD_BROWSER_20260905.json'

class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        if path.startswith('/por-derecho/'):
            path = path[len('/por-derecho'):]
        return super().translate_path(path)
    def log_message(self, *_args: object) -> None:
        pass

def run(base_url: str | None = None) -> dict:
    server = None
    if not base_url:
        server = http.server.ThreadingHTTPServer(
            ('127.0.0.1', 8873), functools.partial(Handler, directory=str(ROOT)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        base_url = 'http://127.0.0.1:8873/por-derecho/'
    base_url = base_url.rstrip('/') + '/'
    shots = ROOT / 'qa-cajasiete'
    shots.mkdir(exist_ok=True)
    results: list[dict] = []
    report = {'control_id': 'PD-CAJASIETE-BOARD-VISUALS-20260905',
              'base_url': base_url,
              'scope': 'Two CajaSiete routes, three engines, two widths, JavaScript on/off; new reader, original commercial anchor, image loading and page error observations. Not a whole-site or legal-proof certificate.',
              'expected_cases': 24, 'cases': results, 'status': 'INCOMPLETE'}
    try:
        with sync_playwright() as p:
            for name in ('chromium', 'firefox', 'webkit'):
                browser = getattr(p, name).launch()
                try:
                    for width in (390, 1280):
                        for js in (True, False):
                            context = browser.new_context(
                                viewport={'width': width, 'height': 900},
                                java_script_enabled=js)
                            context.set_default_timeout(15000)
                            context.set_default_navigation_timeout(20000)
                            try:
                                for route in ROUTES:
                                    key = f'{name}-{route[:2]}-{width}-js{int(js)}'
                                    row = {'engine': name, 'width': width, 'javascript': js,
                                           'route': route, 'status': 'FAIL', 'page_errors': [], 'images': []}
                                    page = context.new_page()
                                    page.on('pageerror', lambda e, row=row: row['page_errors'].append(str(e)))
                                    try:
                                        response = page.goto(base_url + route, wait_until='networkidle')
                                        assert response is not None and response.status == 200, 'Page HTTP status'
                                        section = page.locator('#board-compliance')
                                        assert section.count() == 1, 'Board reader missing or duplicated'
                                        images = section.locator('figure img')
                                        assert images.count() == 3, 'Expected three language-specific figures'
                                        for image_number, image in enumerate(images.all(), start=1):
                                            image.scroll_into_view_if_needed()
                                            deadline = time.monotonic() + 12
                                            while True:
                                                # Synchronous native-image state avoids an unbounded decode()
                                                # Promise in a context with page JavaScript disabled.
                                                state = image.evaluate('(e)=>({complete:e.complete,width:e.naturalWidth,height:e.naturalHeight,source:e.currentSrc})')
                                                if state['complete'] and state['width'] > 0:
                                                    break
                                                if time.monotonic() >= deadline:
                                                    raise AssertionError(f'Image did not load: {state}')
                                                page.wait_for_timeout(150)
                                            expected_height = 1740 if image_number == 2 else 1640
                                            assert state['width'] == 1080 and state['height'] == expected_height, state
                                            assert image.get_attribute('height') == str(expected_height), 'Declared image height differs from design'
                                            assert image.get_attribute('alt'), 'Missing image alternative text'
                                            box = image.bounding_box()
                                            assert box and box['x'] >= -2 and box['x'] + box['width'] <= width + 2, 'Image extends beyond viewport'
                                            row['images'].append(state)
                                        assert section.evaluate('(e)=>e.scrollWidth<=e.clientWidth+2'), 'New reader horizontal overflow'
                                        assert page.locator('#caja-commercial-original').count() == 1, 'Original financing route missing'
                                        for link in section.locator('a[href^="#"]').all():
                                            target = link.get_attribute('href')
                                            assert target and page.locator(target).count() >= 1, f'Missing anchor {target}'
                                        if width == 390 and not js:
                                            section.screenshot(path=str(shots / f'{key}.png'), timeout=15000)
                                        assert not row['page_errors'], row['page_errors']
                                        row['status'] = 'PASS'
                                    except Exception as exc:
                                        row['error_type'] = type(exc).__name__
                                        row['error'] = str(exc)
                                    finally:
                                        results.append(row)
                                        page.close()
                            finally:
                                context.close()
                finally:
                    browser.close()
        report['case_count'] = len(results)
        report['passed'] = sum(x['status'] == 'PASS' for x in results)
        report['status'] = 'PASS' if len(results) == 24 and report['passed'] == 24 else 'FAIL'
    except Exception as exc:
        report['fatal_error'] = f'{type(exc).__name__}: {exc}'
        report['status'] = 'FAIL'
    finally:
        if server:
            server.shutdown()
        report['source_page_sha256'] = {
            route: hashlib.sha256((ROOT / route / 'index.html').read_bytes()).hexdigest()
            for route in ROUTES}
        REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url')
    parser.add_argument('--record-only', action='store_true', help='Record failures before the workflow preserves diagnostics; final acceptance must separately require PASS.')
    args = parser.parse_args()
    result = run(args.base_url)
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if args.record_only or result['status'] == 'PASS' else 1)

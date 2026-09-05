"""Read-only media desk acceptance on an accurately mounted checkout or live host."""
from __future__ import annotations
import json, os, pathlib, subprocess, tempfile, time
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(os.environ.get('MEDIA_AUDIT_OUT', '/tmp/media-release/browser'))
OUT.mkdir(parents=True, exist_ok=True)
ROUTES = ['es/medios-trazabilidad-relato-publico/', 'en/media-public-narrative-traceability/']
BASE = os.environ.get('MEDIA_BASE_URL', '')
server = None
mount = None
if not BASE:
    mount = tempfile.TemporaryDirectory(prefix='pd-media-web-')
    (pathlib.Path(mount.name) / 'por-derecho').symlink_to(ROOT, target_is_directory=True)
    server = subprocess.Popen(['python3', '-m', 'http.server', '8765', '--bind', '127.0.0.1', '--directory', mount.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    BASE = 'http://127.0.0.1:8765/por-derecho/'
    time.sleep(1)
BASE = BASE.rstrip('/') + '/'
rows = []

def visible(heading, header, height):
    return bool(heading and heading['y'] >= 0 and heading['y'] + heading['height'] < height and (not header or heading['y'] >= header['y'] + header['height'] - 2))

try:
    with sync_playwright() as p:
        for engine in ('chromium', 'firefox', 'webkit'):
            browser = getattr(p, engine).launch()
            for route in ROUTES:
                for width, height in ((320, 844), (390, 844), (1280, 900)):
                    for javascript in (True, False):
                        key = f'{engine}-{route[:2]}-{width}-js{int(javascript)}'
                        page = browser.new_page(viewport={'width': width, 'height': height}, java_script_enabled=javascript)
                        page.set_default_timeout(15000)
                        errors = []
                        page.on('pageerror', lambda e: errors.append(str(e)))
                        row = {'case': key, 'route': route, 'engine': engine, 'width': width, 'javascript': javascript}
                        try:
                            response = page.goto(BASE + route + '#media-desk', wait_until='domcontentloaded')
                            page.wait_for_timeout(6500 if javascript else 1200)
                            assert response and response.status == 200, 'Page HTTP status'
                            desk = page.locator('#media-desk')
                            assert desk.count() == 1 and desk.is_visible(), 'Missing visible desk'
                            assert desk.locator('article.card').count() == 6, 'Six source cards'
                            assert desk.locator('form,input,textarea,script,iframe').count() == 0, 'Unexpected interactive/private capture'
                            assert desk.locator('a').count() >= 10, 'Static links missing'
                            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 2'), 'Horizontal overflow'
                            heading = page.locator('#media-desk-title').bounding_box()
                            header = page.locator('.site-header').bounding_box()
                            row['initial_heading'] = heading
                            assert visible(heading, header, height), 'Direct fragment heading obscured'
                            if javascript:
                                assert page.locator('#lpb-concurso-overreach-note').count() == 1, 'Inherited note missing'
                                assert desk.locator('#lpb-concurso-overreach-note').count() == 0, 'Inherited note inserted into desk'
                                assert page.locator('script[data-optimum-reader-journey-finish]').count() == 1, 'Duplicate inherited module'
                                if width <= 650:
                                    assert not page.locator('.main-nav').is_visible(), 'Mobile menu starts open'
                                start = page.evaluate('scrollY')
                                page.mouse.move(width // 2, min(550, height - 100))
                                page.mouse.wheel(0, 350)
                                page.wait_for_timeout(300)
                                stopped = page.evaluate('scrollY')
                                page.wait_for_timeout(600)
                                final = page.evaluate('scrollY')
                                row['reader_scroll'] = {'before': start, 'after_300ms': stopped, 'after_900ms': final}
                                assert final > start + 150, 'Wheel did not move reader into content'
                                assert abs(final - stopped) < 3, 'Reader scroll was overridden'
                                if width <= 650:
                                    page.locator('.nav-toggle').click()
                                page.locator('.main-nav a[href="#media-desk"]').click()
                                page.wait_for_timeout(900)
                                if width <= 650:
                                    assert not page.locator('.main-nav').is_visible(), 'Mobile menu did not close'
                                assert visible(page.locator('#media-desk-title').bounding_box(), page.locator('.site-header').bounding_box(), height), 'Selected link heading obscured'
                                assert not errors, 'Browser script errors: ' + str(errors)
                            page.screenshot(path=str(OUT / (key + '.png')), full_page=False, animations='disabled')
                            if engine == 'chromium' and javascript:
                                desk.screenshot(path=str(OUT / (key + '-section.png')), animations='disabled')
                            row['status'] = 'PASS'
                        except Exception as e:
                            row['status'] = 'FAIL'
                            row['error'] = str(e)
                            try:
                                page.screenshot(path=str(OUT / (key + '-failure.png')), full_page=False)
                                (OUT / (key + '-failure.html')).write_text(page.content())
                            except Exception:
                                pass
                        finally:
                            row['page_errors'] = errors
                            rows.append(row)
                            page.close()
            for lang, search, destination in [('es', 'es/buscar/', ROUTES[0]), ('en', 'en/search/', ROUTES[1])]:
                page = browser.new_page()
                row = {'case': engine + '-' + lang + '-search', 'query': 'media dashboard', 'route': search}
                try:
                    page.goto(BASE + search + '?q=media%20dashboard', wait_until='domcontentloaded')
                    page.wait_for_timeout(8500)
                    assert page.locator('#psr-search-results a[href*="' + destination + '"]').count() > 0, 'Missing canonical search result'
                    row['status'] = 'PASS'
                except Exception as e:
                    row.update(status='FAIL', error=str(e))
                rows.append(row)
                page.close()
            browser.close()
finally:
    if server:
        server.terminate()
    if mount:
        mount.cleanup()
    report = {'source_sha': os.environ.get('GITHUB_SHA'), 'base_url': BASE, 'live_host': BASE.startswith('https://sbu001monterecco.github.io/por-derecho/'), 'cases': rows, 'total': len(rows), 'passed': sum(r['status'] == 'PASS' for r in rows), 'failed': [r for r in rows if r['status'] != 'PASS']}
    (OUT / 'browser.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != 'cases'}, ensure_ascii=False, indent=2))
assert len(rows) == 42 and report['passed'] == 42, 'Media browser acceptance failed; inspect browser.json'

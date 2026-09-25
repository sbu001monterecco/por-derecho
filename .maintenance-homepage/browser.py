#!/usr/bin/env python3
"""Read-only render acceptance for the exact committed homepage candidate."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from html.parser import HTMLParser
from functools import partial
import json, shutil, sys, tempfile, threading, subprocess

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
server_root = Path(tempfile.mkdtemp())
(server_root / 'por-derecho').symlink_to(root, target_is_directory=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass
class NavLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_nav = False
        self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'nav' and a.get('id') == 'main-nav':
            self.in_nav = True
        if self.in_nav and tag == 'a' and 'href' in a:
            self.links.append(a['href'])
    def handle_endtag(self, tag):
        if tag == 'nav':
            self.in_nav = False

server = ThreadingHTTPServer(('127.0.0.1', 8765), partial(Quiet, directory=str(server_root)))
threading.Thread(target=server.serve_forever, daemon=True).start()
exe = shutil.which('google-chrome') or shutil.which('chromium')
if not exe:
    subprocess.run([sys.executable, '-m', 'playwright', 'install', '--with-deps', 'chromium'], check=True)
rows = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path=exe, args=['--no-sandbox'])
    for lang in ['en', 'es']:
        parser = NavLinks()
        parser.feed((root / lang / 'index.html').read_text())
        for width in [320, 390, 768, 1280]:
            for js in [False, True]:
                context = browser.new_context(viewport={'width': width, 'height': 900}, java_script_enabled=js, reduced_motion='reduce')
                page = context.new_page()
                page.set_default_timeout(20000)
                page.route('**/*', lambda route: route.continue_() if route.request.url.startswith('http://127.0.0.1:8765/') else route.abort())
                row = {'lang': lang, 'width': width, 'javascript': js, 'errors': []}
                try:
                    page.goto('http://127.0.0.1:8765/por-derecho/' + lang + '/', wait_until='load', timeout=60000)
                    page.wait_for_timeout(10000 if js else 500)
                    block = page.locator('section[data-five-actor-accountability-static="true"]')
                    assert block.count() == 1, 'Expected one substantive accountability block'
                    assert block.locator('[data-private-actor-card]').count() == 5, 'Expected five private cards'
                    assert block.locator('[data-institution-card]').count() == 2, 'Expected two institutional cards'
                    for item in block.locator('[data-private-actor-card], [data-institution-card]').all():
                        assert item.is_visible(), 'Hidden person card'
                        assert not item.locator('xpath=ancestor::details[not(@open)]').count(), 'Person inside closed disclosure'
                        rect = item.bounding_box()
                        assert rect and rect['width'] > 0
                        assert rect['x'] >= -2 and rect['x'] + rect['width'] <= width + 2, 'Person card overflows viewport'
                    for selector in ['.pd-five-ac__copy', '.pd-five-ac__institution-copy']:
                        sizes = block.locator(selector).evaluate_all('(es)=>es.map(e=>parseFloat(getComputedStyle(e).fontSize))')
                        assert sizes and min(sizes) >= 15.5, 'Substantive person text too small'
                    for image in block.locator('img[loading="eager"]').all():
                        assert image.evaluate('(e)=>e.complete && e.naturalWidth > 0'), 'Required source portrait failed to load'
                    assert page.locator('#economic-scope-20260925').is_visible(), 'Scope section hidden'
                    assert page.locator('[data-homepage-scope="20260925"]').is_visible(), 'Opening scope hidden'
                    assert page.locator('#main-nav').is_visible(), 'Native navigation unavailable'
                    actual = page.locator('#main-nav a').evaluate_all('(es)=>es.map(e=>e.getAttribute("href"))')
                    assert set(parser.links).issubset(actual), 'A source navigation destination was lost'
                    menu = page.locator('.pd-home-more>summary')
                    menu.click()
                    assert page.locator('.pd-home-more').get_attribute('open') is not None, 'More navigation did not open'
                    assert page.locator('.pd-home-more-links a').first.is_visible(), 'Secondary route inaccessible'
                    menu.click()
                    menu.focus()
                    page.keyboard.press('Enter')
                    assert page.locator('.pd-home-more').get_attribute('open') is not None, 'Keyboard navigation did not open'
                    page.keyboard.press('Enter')
                    row['document_width'] = page.evaluate('document.documentElement.scrollWidth')
                    assert row['document_width'] <= width + 2, 'Document has horizontal overflow'
                    if js:
                        search = page.locator('[data-canonical-home-search="20260902"]')
                        assert search.is_visible(), 'Existing search hidden'
                        assert not search.locator('xpath=ancestor::details[not(@open)]').count(), 'Search inside closed disclosure'
                        assert search.evaluate('(e)=>!!(document.querySelector("#economic-scope-20260925").compareDocumentPosition(e)&Node.DOCUMENT_POSITION_FOLLOWING)'), 'Search precedes the opening/scope'
                        page.wait_for_function('window.PorDerechoCanonicalSearch && window.PorDerechoCanonicalSearch.count > 0', timeout=30000)
                        search.locator('input').fill('Acosta')
                        assert search.locator('.canonical-search-result').count() > 0, 'Moved search no longer returns results'
                        search.locator('input').fill('')
                        assert page.locator('.psr-home-control-gateway a').count() > 0, 'Control-room gateway lost'
                        assert page.locator('.psr-utility-nav a').count() >= 2, 'Global search/control shortcuts lost'
                    row.update(private_cards=5, institution_cards=2, scope_visible=True, navigation_preserved=True, required_images_loaded=True)
                    if js and width in [390, 1280]:
                        page.evaluate('window.scrollTo(0,0)')
                        page.screenshot(path=str(out / f'{lang}-{width}-opening.png'))
                        block.locator('.pd-five-ac__cards').screenshot(path=str(out / f'{lang}-{width}-private-actors.png'))
                        block.locator('.pd-five-ac__institutional').screenshot(path=str(out / f'{lang}-{width}-institutional.png'))
                        page.locator('#economic-scope-20260925').screenshot(path=str(out / f'{lang}-{width}-scope.png'))
                except Exception as e:
                    row['errors'].append(str(e))
                    print('BROWSER_FAILURE', row, flush=True)
                    try:
                        page.evaluate('window.scrollTo(0,0)')
                        page.screenshot(path=str(out / f'{lang}-{width}-{js}-failure.png'), timeout=10000)
                    except Exception:
                        pass
                rows.append(row)
                print('BROWSER_CASE', json.dumps(row), flush=True)
                context.close()
    browser.close()
server.shutdown()
(out / 'browser-results.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
print('PD_BROWSER_RESULTS=' + json.dumps(rows), flush=True)
if any(r['errors'] for r in rows):
    sys.exit(1)

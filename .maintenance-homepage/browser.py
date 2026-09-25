#!/usr/bin/env python3
"""Read-only, exact-source render acceptance; test failures never publish a ref."""
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
    def log_message(self, *args): pass
class NavLinks(HTMLParser):
    def __init__(self):
        super().__init__(); self.in_nav = False; self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'nav' and a.get('id') == 'main-nav': self.in_nav = True
        if self.in_nav and tag == 'a' and 'href' in a: self.links.append(a['href'])
    def handle_endtag(self, tag):
        if tag == 'nav': self.in_nav = False

# Public, already-published photographic sources only; no new portrait or identity inference.
for rel in ['assets/actors/fmmm-shaila-antonio-family-editorial-display-20260922.jpg', 'assets/acosta-matos-family-hotel-plans.jpg', 'assets/actors/francisco-de-borja-rodriguez-batllori.jpg', 'assets/actors/alberto-lopez-villarrubia.jpg']:
    src = root / rel
    if src.is_file():
        dst = out / 'source-images' / src.name
        dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, dst)
server = ThreadingHTTPServer(('127.0.0.1', 8765), partial(Quiet, directory=str(server_root)))
threading.Thread(target=server.serve_forever, daemon=True).start()
exe = shutil.which('google-chrome') or shutil.which('chromium')
if not exe: subprocess.run([sys.executable, '-m', 'playwright', 'install', '--with-deps', 'chromium'], check=True)
rows = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path=exe, args=['--no-sandbox'])
    for lang in ['en', 'es']:
        parser = NavLinks(); parser.feed((root / lang / 'index.html').read_text())
        for width in [320, 390, 768, 1280]:
            for js in [False, True]:
                context = browser.new_context(viewport={'width': width, 'height': 900}, java_script_enabled=js, reduced_motion='reduce')
                page = context.new_page(); page.set_default_timeout(20000)
                page.route('**/*', lambda route: route.continue_() if route.request.url.startswith('http://127.0.0.1:8765/') else route.abort())
                row = {'lang': lang, 'width': width, 'javascript': js, 'errors': []}
                try:
                    page.goto('http://127.0.0.1:8765/por-derecho/' + lang + '/', wait_until='load', timeout=60000)
                    page.wait_for_timeout(11000 if js else 500)
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
                    diagnostics = block.locator('img[loading="eager"]').evaluate_all('''es=>es.map(e=>({src:e.currentSrc,naturalWidth:e.naturalWidth,naturalHeight:e.naturalHeight,html:e.outerHTML,ancestors:[e,...function*(n){while(n.parentElement){n=n.parentElement;yield n;}}(e)].map(n=>({tag:n.tagName,cls:n.className,opacity:getComputedStyle(n).opacity,display:getComputedStyle(n).display,visibility:getComputedStyle(n).visibility,contentVisibility:getComputedStyle(n).contentVisibility,rect:n.getBoundingClientRect().toJSON()}))}))''')
                    (out / f'{lang}-{width}-{js}-portraits.json').write_text(json.dumps(diagnostics, indent=2))
                    for image in block.locator('img[loading="eager"]').all():
                        assert image.evaluate('(e)=>e.complete && e.naturalWidth >= 100'), 'Required source portrait is absent or a placeholder'
                        assert image.is_visible(), 'Required source portrait is hidden'
                        assert image.evaluate('(e)=>{for(let n=e;n;n=n.parentElement){if(Number(getComputedStyle(n).opacity)<.95)return false;}return true;}'), 'Portrait opacity hides the source image'
                    assert page.locator('#economic-scope-20260925').is_visible(), 'Scope section hidden'
                    assert page.locator('[data-homepage-scope="20260925"]').is_visible(), 'Opening scope hidden'
                    outer = page.locator('.pd-home-nav-disclosure')
                    if js and width <= 800:
                        assert outer.count() == 1 and outer.get_attribute('open') is None, 'Phone menu must start compact'
                        row['header_height'] = page.locator('.site-header').bounding_box()['height']
                        assert row['header_height'] < 220, 'Phone header obscures first reading'
                        assert page.locator('main .hero h1').bounding_box()['y'] < 700, 'Opening displaced below first screen'
                        outer.locator(':scope > summary').click()
                    assert page.locator('#main-nav').is_visible(), 'Native navigation unavailable'
                    actual = page.locator('#main-nav a').evaluate_all('(es)=>es.map(e=>e.getAttribute("href"))')
                    assert set(parser.links).issubset(actual), 'A source navigation destination was lost'
                    menu = page.locator('.pd-home-more>summary')
                    menu.click()
                    assert page.locator('.pd-home-more').get_attribute('open') is not None, 'More navigation did not open'
                    assert page.locator('.pd-home-more-links a').first.is_visible(), 'Secondary route inaccessible'
                    menu.click(); menu.focus(); page.keyboard.press('Enter')
                    assert page.locator('.pd-home-more').get_attribute('open') is not None, 'Keyboard navigation did not open'
                    page.keyboard.press('Enter')
                    if js and width <= 800:
                        page.keyboard.press('Escape')
                        assert outer.get_attribute('open') is None, 'Escape must close phone menu'
                        outer.locator(':scope > summary').focus(); page.keyboard.press('Enter')
                        assert outer.get_attribute('open') is not None, 'Keyboard must open phone menu'
                        page.keyboard.press('Escape')
                    row['document_width'] = page.evaluate('document.documentElement.scrollWidth')
                    assert row['document_width'] <= width + 2, 'Document has horizontal overflow'
                    if js:
                        search = page.locator('[data-canonical-home-search="20260902"]')
                        assert search.is_visible(), 'Existing search hidden'
                        assert not search.locator('xpath=ancestor::details[not(@open)]').count(), 'Search inside closed disclosure'
                        assert search.evaluate('(e)=>!!(document.querySelector("#economic-scope-20260925").compareDocumentPosition(e)&Node.DOCUMENT_POSITION_FOLLOWING)'), 'Search precedes opening/scope'
                        page.wait_for_function('window.PorDerechoCanonicalSearch && window.PorDerechoCanonicalSearch.count > 0', timeout=30000)
                        search.locator('input').fill('Acosta')
                        search.locator('.canonical-search-result').first.wait_for(state='visible', timeout=15000)
                        assert search.locator('.canonical-search-result').count() > 0, 'Moved search no longer returns results'
                        search.locator('input').fill('')
                        assert page.locator('.psr-home-control-gateway a').count() > 0, 'Control-room gateway lost'
                        assert page.locator('.psr-utility-nav a').count() >= 2, 'Global shortcuts lost'
                    row.update(private_cards=5, institution_cards=2, scope_visible=True, navigation_preserved=True, required_images_loaded=True)
                    if js and width in [390, 1280]:
                        page.locator('body').click(position={'x':1,'y':1}, force=True); page.evaluate('window.scrollTo(0,0)'); page.wait_for_timeout(300)
                        page.screenshot(path=str(out / f'{lang}-{width}-opening.png'))
                        for n, image in enumerate(block.locator('img[loading="eager"]').all()):
                            image.evaluate('(e)=>e.scrollIntoView({block:"center",behavior:"instant"})'); page.wait_for_timeout(500)
                            page.screenshot(path=str(out / f'{lang}-{width}-portrait-context-{n}.png'))
                        page.locator('#economic-scope-20260925').screenshot(path=str(out / f'{lang}-{width}-scope.png'))
                except Exception as e:
                    row['errors'].append(str(e)); print('BROWSER_FAILURE', row, flush=True)
                    try:
                        page.evaluate('window.scrollTo(0,0)'); page.screenshot(path=str(out / f'{lang}-{width}-{js}-failure.png'), timeout=10000)
                    except Exception: pass
                rows.append(row); print('BROWSER_CASE', json.dumps(row), flush=True); context.close()
    browser.close()
server.shutdown()
(out / 'browser-results.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
print('PD_BROWSER_RESULTS=' + json.dumps(rows), flush=True)
if any(r['errors'] for r in rows): sys.exit(1)

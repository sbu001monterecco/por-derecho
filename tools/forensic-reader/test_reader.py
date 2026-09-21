"""Synthetic DOM smoke test; contains no private source material."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    root = Path(__file__).resolve().parent
    html = (root / 'index.html').read_text(encoding='utf-8')
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=os.environ.get('CHROMIUM', '/usr/bin/chromium'), headless=True, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1280, 'height': 900})
        errors, requests = [], []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('request', lambda request: requests.append(request.url))
        page.set_content(html)
        assert page.locator('.source').count() == 1
        page.evaluate("""() => { const n=document.querySelector('.source').firstChild.firstChild; const r=document.createRange(); r.setStart(n,2); r.setEnd(n,10); const s=getSelection(); s.removeAllRanges(); s.addRange(r); }""")
        page.locator('#capture').click()
        assert page.locator('#selection').inner_text() == 'received'
        page.locator('#category').select_option('CONTRADICTED')
        page.locator('#save').click()
        assert 'Contradiction requires' in page.locator('#status').inner_text()
        page.locator('#category').select_option('KNOWLEDGE')
        page.locator('#note').fill('Synthetic knowledge marker, not a finding.')
        page.locator('#save').click()
        assert page.locator('.card').count() == 1
        page.locator('#language').click()
        assert page.locator('html').get_attribute('lang') == 'es'
        page.set_viewport_size({'width': 390, 'height': 844})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert not errors, errors
        assert not requests, requests
        browser.close()
    print(json.dumps({'synthetic_smoke': 'PASS', 'scope': 'DOM rendering, selection, contradiction guard, editing, Spanish, mobile; not hosted PDF or legal verification'}))


if __name__ == '__main__':
    main()

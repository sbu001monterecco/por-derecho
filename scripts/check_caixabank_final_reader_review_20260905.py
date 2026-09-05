#!/usr/bin/env python3
"""Read-only homepage isolation and quick-reader visual regression checks."""
import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path.cwd()
OUT = Path(os.getenv('PD_AUDIT_OUT', '/tmp/caixabank-candidate'))
BASE = os.getenv('PD_AUDIT_BASE', 'http://127.0.0.1:8899/por-derecho/')

async def run():
    OUT.mkdir(exist_ok=True, parents=True)
    assert 'const isHome = /^' in (ROOT/'assets/home-mission-critical-20260904.js').read_text()
    rows, errors = [], []
    async with async_playwright() as p:
        for engine in ('chromium', 'firefox', 'webkit'):
            browser = await getattr(p, engine).launch()
            ctx = await browser.new_context(viewport={'width':390, 'height':900})
            for route in ('es/', 'en/', 'es/reclamacion-caixabank-valencia/', 'en/caixabank-valencia-claim/'):
                page = await ctx.new_page()
                row = {'engine':engine, 'route':route}
                try:
                    response = await page.goto(BASE+route, wait_until='domcontentloaded')
                    assert response and response.status == 200
                    await page.wait_for_timeout(3500)
                    is_home = route in ('es/', 'en/')
                    # The source intentionally creates ONE navigation rail AND ONE case-map section.
                    # The old selector counted both and incorrectly expected one total element.
                    expected = 1 if is_home else 0
                    for tag in ('nav', 'section'):
                        count = await page.locator(tag+'[data-pd-home-mission="20260904"]').count()
                        row[tag+'_count'] = count
                        assert count == expected, (engine, route, tag, count)
                    total = await page.locator('[data-pd-home-mission="20260904"]').count()
                    assert total == 2*expected, (engine, route, 'unexpected component', total)
                    if not is_home:
                        buttons = await page.locator('#caixabank-lectura-inicial .button').evaluate_all('''els=>els.map(e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return {text:e.innerText,color:s.color,background:s.backgroundColor,height:r.height}})''')
                        row['quick_read_buttons'] = buttons
                        assert buttons and all(b['color']=='rgb(19, 37, 45)' and b['background']=='rgb(255, 255, 255)' and b['height']>=44 for b in buttons), buttons
                        await page.evaluate('''()=>{document.documentElement.style.scrollBehavior='auto';const e=document.querySelector('#caixabank-lectura-inicial');window.scrollTo(0,e.getBoundingClientRect().top+window.scrollY)}''')
                    await page.screenshot(path=str(OUT/(engine+'-'+route.replace('/','_')+'quick-review.png')), full_page=False, animations='disabled')
                    row['passed'] = True
                except Exception as exc:
                    row['passed'] = False
                    row['error'] = str(exc)
                    errors.append({'engine':engine, 'route':route, 'error':str(exc)})
                    await page.screenshot(path=str(OUT/(engine+'-'+route.replace('/','_')+'failure.png')), full_page=False, animations='disabled')
                finally:
                    rows.append(row)
                    await page.close()
            await browser.close()
    result = {'passed':not errors, 'checks':rows, 'errors':errors}
    (OUT/'final-reader-review.json').write_text(json.dumps(result, indent=2))
    print('FINAL_READER_REVIEW',len(rows),'ERRORS',len(errors))
    if errors:
        raise SystemExit(1)

if __name__ == '__main__':
    asyncio.run(run())

import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const base = (process.env.PSR_BASE_URL || 'http://127.0.0.1:4173/por-derecho').replace(/\/$/, '');
const output = process.env.PSR_262_FINCA_ARTIFACT_DIR || 'artifacts/262-finca-journey-local';
const executablePath = (process.env.PSR_BROWSER_PATH || '').trim() || undefined;
fs.mkdirSync(output, { recursive: true });

const routes = [
  { name: 'en', route: '/en/262-properties-journey-2008-present/', fincaLabel: 'Registry finca', context: 'Whole-complex context — not a property event', gap: 'No source-bound property event has yet been entered for this finca.' },
  { name: 'es', route: '/es/fincas-262-recorrido-2008-hoy/', fincaLabel: 'Finca registral', context: 'Contexto del conjunto — no es un evento de finca', gap: 'Aún no se ha incorporado ningún evento de finca vinculado a fuente.' },
];
const viewports = [
  { name: 'desktop', width: 1440, height: 1050 },
  { name: 'mobile', width: 390, height: 844 },
];
const results = [];
const failures = [];

function assert(ok, message) {
  if (!ok) throw new Error(message);
}

const browser = await chromium.launch({ headless: true, executablePath });
try {
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height } });
    for (const route of routes) {
      const page = await context.newPage();
      const result = { route: route.route, viewport: viewport.name, status: 'fail' };
      try {
        const response = await page.goto(`${base}${route.route}?rendercheck=${Date.now()}`, { waitUntil: 'domcontentloaded', timeout: 45_000 });
        assert(response?.status() === 200, `HTTP ${response?.status()}`);
        await page.waitForSelector('[data-fj-property-list] button[data-finca="8588"]', { timeout: 20_000 });
        await page.waitForFunction(() => document.querySelectorAll('[data-fj-property-list] button').length === 262, null, { timeout: 20_000 });
        const body = await page.locator('body').innerText();
        assert(body.includes(route.context), 'Whole-complex context boundary missing');
        assert(body.includes('8588'), 'Default source-bound finca missing');
        assert(body.includes('DOCUMENTED') || body.includes('Documented') || body.includes('Representación'), 'Source-status labeling missing');

        await page.locator('[data-fj-finca]').selectOption('8557');
        await page.waitForFunction(() => document.querySelector('[data-fj-detail]')?.innerText.includes('707') && document.querySelector('[data-fj-detail]')?.innerText.includes('708'), null, { timeout: 10_000 });
        const conflictText = await page.locator('[data-fj-detail]').innerText();
        assert(conflictText.includes('707') && conflictText.includes('708'), '8557 crosswalk conflict not rendered');

        const search = page.locator('[data-fj-search]');
        await search.fill('8593');
        await page.waitForFunction(() => document.querySelectorAll('[data-fj-property-list] button').length === 1, null, { timeout: 10_000 });
        await page.locator('[data-fj-property-list] button[data-finca="8593"]').click();
        await page.waitForFunction(expected => document.querySelector('[data-fj-detail]')?.innerText.includes(expected), route.gap, { timeout: 10_000 });

        const metrics = await page.evaluate(() => {
          const viewport = document.documentElement.clientWidth;
          const scrollWidth = document.documentElement.scrollWidth;
          const overflow = scrollWidth > viewport + 3
            ? [...document.querySelectorAll('body *')].map(node => {
              const rect = node.getBoundingClientRect();
              return { tag: node.tagName, id: node.id, className: String(node.className || '').slice(0, 100), left: Math.round(rect.left), right: Math.round(rect.right), width: Math.round(rect.width) };
            }).filter(item => item.right > viewport + 3 || item.left < -3).slice(0, 12)
            : [];
          return { scrollWidth, clientWidth: viewport, h1: document.querySelectorAll('h1').length, listCount: document.querySelectorAll('[data-fj-property-list] button').length, overflow };
        });
        assert(metrics.h1 === 1, `Expected one H1, found ${metrics.h1}`);
        assert(metrics.scrollWidth <= metrics.clientWidth + 3, `Horizontal overflow: ${JSON.stringify(metrics.overflow)}`);
        await page.screenshot({ path: path.join(output, `${route.name}-${viewport.name}.png`), fullPage: true });
        result.status = 'pass';
        result.metrics = metrics;
      } catch (error) {
        result.error = String(error);
        failures.push(result);
        try { await page.screenshot({ path: path.join(output, `${route.name}-${viewport.name}-failure.png`), fullPage: true }); } catch {}
      } finally {
        results.push(result);
        await page.close();
      }
    }
    await context.close();
  }
} finally {
  await browser.close();
}

fs.writeFileSync(path.join(output, 'result.json'), JSON.stringify({ base, checked_at: new Date().toISOString(), results, failures }, null, 2));
if (failures.length) {
  console.error(JSON.stringify(failures, null, 2));
  process.exit(1);
}
console.log(`262-finca journey rendered checks passed: ${results.length}`);

// Render the additive programme in its real page layouts, including mobile and no-JS.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
const { execFileSync } = require('node:child_process');

(async () => {
  const base = (process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho').replace(/\/$/, '');
  const out = process.env.PSR_RESPONSE_SCREENSHOT_DIR || 'artifacts/dp1901-eg745-response-programme';
  fs.mkdirSync(out, { recursive: true });
  const state = JSON.parse(fs.readFileSync('assets/data/dp1901-eg745-fiscal-superior-action-state-20260919.json'));
  const routes = state.response_programme_publication.routes;
  if (routes.length !== 22) throw new Error('Expected the reviewed 22-route denominator');
  const report = { source_sha: execFileSync('git', ['rev-parse', 'HEAD'], { encoding: 'utf8' }).trim(), base, cases: [], failures: [], boundary: 'Chromium viewport checks, not physical-device certification. External origins blocked. Existing whole-page behavior has separate audience checks.' };
  const browser = await chromium.launch({ headless: true });
  for (const route of routes) {
    const primary = /^(es|en)\/dp-1901-2026\/$/.test(route) || /(?:fiscalia-inspeccion|public-prosecution-inspection)-exp-gub-745/.test(route);
    for (const [width, js] of [[390, true], [1440, true], ...(primary ? [[390, false]] : [])]) {
      const context = await browser.newContext({ viewport: { width, height: 1000 }, javaScriptEnabled: js });
      await context.route('**/*', r => new URL(r.request().url()).origin === new URL(base).origin ? r.continue() : r.abort());
      const page = await context.newPage();
      const item = { route, width, javascript: js };
      try {
        const response = await page.goto(`${base}/${route}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
        if (response.status() !== 200) throw new Error(`Page HTTP ${response.status()}`);
        const module = page.locator('#response-programme-20260920');
        if (await module.count() !== 1 || !await module.isVisible()) throw new Error('Programme missing or hidden');
        await module.scrollIntoViewIfNeeded();
        const box = await module.boundingBox();
        if (!box || box.width < 200 || box.x < -2 || box.x + box.width > width + 2) throw new Error(`Programme overflows viewport: ${JSON.stringify(box)}`);
        const metrics = await module.evaluate(el => ({ overflow: el.scrollWidth - el.clientWidth, cards: el.querySelectorAll('.pd-response-card').length, links: [...el.querySelectorAll('nav a')].map(a => a.href), title: el.querySelector('h2').textContent, style: getComputedStyle(el).backgroundColor }));
        if (metrics.overflow > 2 || metrics.cards !== 3 || metrics.links.length !== 3 || !metrics.title.includes('20')) throw new Error(JSON.stringify(metrics));
        for (const href of metrics.links) {
          const url = new URL(href);
          if (!url.pathname.startsWith(new URL(base).pathname + '/')) throw new Error('Link escapes repository base');
        }
        if (/^(es|en)\/dp-1901-2026\/$/.test(route)) {
          if (await module.locator('tbody tr').count() !== 13) throw new Error('Direct census row mismatch');
          await module.locator('summary').click();
          if (await module.locator('details li').count() !== 20) throw new Error('Connected census row mismatch');
          if (!await module.locator('details li').first().isVisible()) throw new Error('Connected routes do not expand');
          await module.locator('summary').click();
        }
        if (primary) await module.screenshot({ path: path.join(out, `${route.replace(/\/$/, '').replace(/\//g, '-')}-${width}-${js ? 'js' : 'nojs'}.png`) });
        item.result = 'PASS'; item.metrics = metrics;
      } catch (error) {
        item.result = 'FAIL'; item.error = String(error); report.failures.push(item);
        await page.screenshot({ path: path.join(out, `failure-${report.cases.length}.png`), fullPage: false }).catch(() => {});
      } finally { report.cases.push(item); await context.close(); }
    }
  }
  await browser.close();
  report.result = report.failures.length ? 'FAIL' : 'PASS';
  fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({ result: report.result, cases: report.cases.length, failures: report.failures, source_sha: report.source_sha }));
  if (report.failures.length) process.exitCode = 1;
})().catch(error => { console.error(error); process.exitCode = 1; });

import fs from 'node:fs/promises';
import path from 'node:path';

const { chromium } = await import(process.env.PSR_PLAYWRIGHT_PATH || 'playwright');
const baseURL = process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho';
const outputDir = path.join(process.env.PSR_SCREENSHOT_DIR || 'artifacts/audience-experience-20260823', 'counsel-selection');
const cases = [
  { lang: 'en', route: '/en/counsel-selection-transparency/', other: '/es/transparencia-seleccion-asesoria/', boundary: 'Sending does not confirm delivery, reading or acceptance.' },
  { lang: 'es', route: '/es/transparencia-seleccion-asesoria/', other: '/en/counsel-selection-transparency/', boundary: 'El envío no confirma la entrega, la lectura ni la aceptación.' },
];
const viewports = [
  { name: 'mobile', width: 390, height: 844 },
  { name: 'desktop', width: 1440, height: 1000 },
];
const results = [];
const failures = [];
await fs.mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
try {
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport });
    for (const item of cases) {
      const page = await context.newPage();
      const response = await page.goto(baseURL + item.route, { waitUntil: 'networkidle' });
      await page.locator('h1').waitFor({ state: 'visible' });
      const metrics = await page.evaluate(({ lang, boundary }) => {
        const ids = [...document.querySelectorAll('[id]')].map(node => node.id);
        const anchors = [...document.querySelectorAll('a[href^="#"]')];
        return {
          lang: document.documentElement.lang,
          control: document.body.dataset.publicControl,
          asOf: document.body.dataset.asOf,
          stats: [...document.querySelectorAll('.stats .stat strong')].map(node => node.textContent.trim()),
          noOverflow: document.documentElement.scrollWidth <= innerWidth + 1,
          uniqueIds: ids.length === new Set(ids).size,
          anchorsValid: anchors.every(node => document.getElementById(node.getAttribute('href').slice(1))),
          sendBoundary: document.body.innerText.includes(boundary),
          languageTarget: document.querySelector('.topnav .language')?.href || '',
        };
      }, item);
      const status = response?.status();
      const expectedLanguageTarget = baseURL + item.other;
      const dataResponse = await context.request.get(baseURL + '/assets/data/uk-counsel-selection-transparency-20261031.json');
      const data = await dataResponse.json();
      const countsMatch = data.candidate_institutions === 24 && data.first_contact_sent_once === 4 &&
        data.first_contact_not_sent === 20 && data.verified_engagements === 0 &&
        Object.values(data.of_not_sent).reduce((a, b) => a + b, 0) === 20;
      const passed = status === 200 && dataResponse.status() === 200 && countsMatch &&
        metrics.lang === item.lang && metrics.control === 'PD-EWPP-UKCOUNSEL-PUBLIC-20261031-01' &&
        metrics.asOf === '2026-10-31' && metrics.stats.join(',') === '24,4,20,0' &&
        metrics.noOverflow && metrics.uniqueIds && metrics.anchorsValid && metrics.sendBoundary &&
        metrics.languageTarget === expectedLanguageTarget;
      await page.screenshot({ path: path.join(outputDir, item.lang + '-' + viewport.name + '.png'), fullPage: true });
      results.push({ route: item.route, viewport: viewport.name, status, dataStatus: dataResponse.status(), countsMatch, ...metrics, passed });
      if (!passed) failures.push(item.lang + '-' + viewport.name);
      await page.close();
    }
    await context.close();
  }
} finally {
  await browser.close();
  await fs.writeFile(path.join(outputDir, 'metrics.json'), JSON.stringify(results, null, 2) + '\n');
}
if (failures.length) throw new Error('Counsel dashboard render checks failed: ' + failures.join(', '));
console.log('COUNSEL SELECTION RENDER PASSED: EN/ES desktop and mobile; status, snapshot, counts, links and overflow verified.');

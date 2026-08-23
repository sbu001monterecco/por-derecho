import fs from 'node:fs/promises';
import path from 'node:path';

const playwright = await import(process.env.PSR_PLAYWRIGHT_PATH || 'playwright');
const { chromium } = playwright;

const baseURL = process.env.PSR_BASE_URL || 'http://127.0.0.1:8765';
const outputDir = process.env.PSR_SCREENSHOT_DIR || 'artifacts/audience-experience-20260823';
const routes = [
  { lang: 'es', route: '/es/', summary: '#resumen-60-segundos', perimeters: '#perimetros-del-caso', chronology: '#historia-reconstruida' },
  { lang: 'en', route: '/en/', summary: '#sixty-second-summary', perimeters: '#case-perimeters', chronology: '#reverse-engineered-story' },
];
const viewports = [
  { name: 'mobile', width: 390, height: 844 },
  { name: 'desktop', width: 1440, height: 1000 },
];

await fs.mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const results = [];
const failures = [];

try {
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport });
    for (const item of routes) {
      const page = await context.newPage();
      await page.goto(`${baseURL}${item.route}`, { waitUntil: 'networkidle', timeout: 60_000 });
      await page.waitForTimeout(7_000);

      const metrics = await page.evaluate(({ summary, perimeters, chronology, width }) => {
        const main = document.querySelector('main');
        const directChildren = [...(main?.children || [])];
        const index = (selector) => directChildren.indexOf(document.querySelector(selector));
        const summaryNode = document.querySelector(summary);
        const audienceNode = document.querySelector('#psr-reader-intent');
        const perimeterNode = document.querySelector(perimeters);
        const chronologyNode = document.querySelector(chronology);
        const fullRecordNode = document.querySelector('[data-audience-full-record]');
        const fullRecordDetails = fullRecordNode?.querySelector('details');
        return {
          order: [index(summary), index('#psr-reader-intent'), index(perimeters), index('[data-audience-full-record]')],
          summaryTop: Math.round(summaryNode?.getBoundingClientRect().top + scrollY || -1),
          audienceCards: audienceNode?.querySelectorAll('.psr-intent-card').length || 0,
          perimeterCards: perimeterNode?.querySelectorAll('.audience-perimeter-grid > a').length || 0,
          prosecutionPanels: document.querySelectorAll('.prosecution-entry-20260821').length,
          identityVariantPresent: document.body.textContent.includes('Laura Isabel'),
          audienceOrderMarker: main?.dataset.audienceOrder || '',
          chronologyInFullRecord: Boolean(chronologyNode && fullRecordNode?.contains(chronologyNode)),
          fullRecordClosed: Boolean(fullRecordDetails && !fullRecordDetails.open),
          horizontalOverflow: document.documentElement.scrollWidth - width,
          summaryHeading: summaryNode?.querySelector('h2')?.textContent?.trim() || '',
          chronologyHeading: chronologyNode?.querySelector('h2')?.textContent?.trim() || '',
        };
      }, { summary: item.summary, perimeters: item.perimeters, chronology: item.chronology, width: viewport.width });

      const prefix = `${item.lang}/${viewport.name}`;
      if (metrics.order.some((value) => value < 0) || metrics.order.some((value, i, values) => i && value !== values[i - 1] + 1)) failures.push(`${prefix}: core sections are not consecutive: ${metrics.order.join(',')}`);
      if (metrics.audienceCards !== 4) failures.push(`${prefix}: expected 4 audience cards, got ${metrics.audienceCards}`);
      if (metrics.perimeterCards !== 5) failures.push(`${prefix}: expected 5 perimeter cards, got ${metrics.perimeterCards}`);
      if (metrics.prosecutionPanels !== 1) failures.push(`${prefix}: expected 1 prosecution panel, got ${metrics.prosecutionPanels}`);
      if (metrics.identityVariantPresent) failures.push(`${prefix}: forbidden public identity variant rendered`);
      if (metrics.audienceOrderMarker !== '20260823') failures.push(`${prefix}: runtime order marker missing`);
      if (!metrics.chronologyInFullRecord) failures.push(`${prefix}: chronology was not moved into progressive disclosure`);
      if (!metrics.fullRecordClosed) failures.push(`${prefix}: full record is not collapsed on first load`);
      if (metrics.horizontalOverflow > 2) failures.push(`${prefix}: horizontal overflow ${metrics.horizontalOverflow}px`);

      await page.screenshot({ path: path.join(outputDir, `${item.lang}-${viewport.name}-top.png`), fullPage: false });
      await page.locator('#psr-reader-intent').scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);
      await page.screenshot({ path: path.join(outputDir, `${item.lang}-${viewport.name}-audiences.png`), fullPage: false });
      await page.locator(item.perimeters).scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);
      await page.screenshot({ path: path.join(outputDir, `${item.lang}-${viewport.name}-perimeters.png`), fullPage: false });

      results.push({ route: item.route, viewport: viewport.name, ...metrics });
      await page.close();
    }
    await context.close();
  }
} finally {
  await browser.close();
}

await fs.writeFile(path.join(outputDir, 'results.json'), JSON.stringify({ baseURL, results, failures }, null, 2));
if (failures.length) {
  console.error(failures.join('\n'));
  process.exit(1);
}
console.log(`AUDIENCE RENDER VALIDATION PASSED — ${results.length} bilingual viewport checks; screenshots in ${outputDir}`);

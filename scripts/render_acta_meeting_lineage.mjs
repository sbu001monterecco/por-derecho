import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const base = (process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho').replace(/\/$/, '');
const out = process.env.PSR_SCREENSHOT_DIR || 'artifacts/acta-meeting-lineage';
const browserPath = process.env.PSR_BROWSER_PATH || undefined;

const cases = [
  ['es-overview', '/es/comunidad-instrumentalizacion/sala-documental-actas/', null, false],
  ['en-overview', '/en/community-instrumentalisation/acta-document-room/', null, false],
  ['pre-sale', '/es/comunidad-instrumentalizacion/sala-documental-actas/2008-04-29/', 'pre_sale_montelanza', true],
  ['project', '/es/comunidad-instrumentalizacion/sala-documental-actas/2012-08-10/', 'project_lpb_aweswell_gil', true],
  ['adverse-mm', '/es/comunidad-instrumentalizacion/sala-documental-actas/2011-06-22/', 'adverse_montelanza_molina', true],
  ['adverse-cam', '/es/comunidad-instrumentalizacion/sala-documental-actas/2022-02-04/', 'adverse_acosta_matos', true],
  ['mixed', '/es/comunidad-instrumentalizacion/sala-documental-actas/2008-07-15/', 'mixed_or_contested', true],
  ['unresolved', '/en/community-instrumentalisation/acta-document-room/2018-11-20-recital/', 'unresolved', false],
];

const viewports = {
  desktop: { width: 1440, height: 1000 },
  mobile: { width: 390, height: 844 },
};

fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ headless: true, ...(browserPath ? { executablePath: browserPath } : {}) });
const results = [];
const colours = new Map();
let failed = false;

try {
  for (const [name, route, perimeter, fullSource] of cases) {
    for (const [device, viewport] of Object.entries(viewports)) {
      const page = await browser.newPage({ viewportSize: viewport });
      const errors = [];
      page.on('pageerror', error => errors.push(`pageerror: ${error.message}`));
      page.on('console', message => {
        if (message.type() === 'error') errors.push(`console: ${message.text()}`);
      });
      const response = await page.goto(`${base}${route}`, { waitUntil: 'networkidle' });
      if (!response || !response.ok()) errors.push(`HTTP ${response?.status() || 'no response'}`);

      const metrics = await page.evaluate(({ expected, full }) => {
        const body = document.body;
        const ribbon = document.querySelector('.acta-perimeter-ribbon');
        const fullText = document.querySelector('.acta-full-ocr');
        const sourcePages = document.querySelectorAll('.acta-source-gallery .acta-source-page');
        const style = ribbon ? getComputedStyle(ribbon) : null;
        return {
          title: document.title,
          bodyPerimeter: body.dataset.perimeter || null,
          expected,
          ribbon: Boolean(ribbon),
          ribbonColour: style?.borderLeftColor || null,
          ribbonBackground: style?.backgroundColor || null,
          ocrChars: fullText?.textContent?.length || 0,
          sourcePages: sourcePages.length,
          full,
          overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
          previousNext: document.querySelectorAll('.acta-event-nav a').length,
        };
      }, { expected: perimeter, full: fullSource });

      if (perimeter) {
        if (metrics.bodyPerimeter !== perimeter) errors.push(`perimeter ${metrics.bodyPerimeter} != ${perimeter}`);
        if (!metrics.ribbon) errors.push('missing perimeter ribbon');
        if (!metrics.ribbonColour || !metrics.ribbonBackground) errors.push('missing computed perimeter colour');
        colours.set(perimeter, `${metrics.ribbonColour}|${metrics.ribbonBackground}`);
      }
      if (fullSource && (metrics.ocrChars < 100 || metrics.sourcePages < 1)) {
        errors.push(`incomplete embedded source layer: OCR ${metrics.ocrChars}; pages ${metrics.sourcePages}`);
      }
      if (metrics.overflow > 2) errors.push(`horizontal overflow ${metrics.overflow}px`);

      const target = perimeter ? page.locator('.acta-event-hero') : page.locator('main').first();
      await target.screenshot({ path: path.join(out, `${name}-${device}.png`) });
      results.push({ name, route, device, metrics, errors });
      if (errors.length) failed = true;
      await page.close();
    }
  }
} finally {
  await browser.close();
}

if (new Set(colours.values()).size !== colours.size) {
  failed = true;
  results.push({ name: 'colour-distinction', errors: ['two or more perimeter lanes share the same rendered colour pair'] });
}

fs.writeFileSync(path.join(out, 'result.json'), JSON.stringify({ base, colours: Object.fromEntries(colours), results }, null, 2));
if (failed) {
  console.error('ACTA rendered lineage validation failed');
  for (const item of results.filter(item => item.errors?.length)) console.error(item.name, item.device || '', item.errors.join('; '));
  process.exit(1);
}
console.log(`ACTA rendered lineage validation: PASS (${results.length} route/viewport checks; ${colours.size} distinct lanes)`);

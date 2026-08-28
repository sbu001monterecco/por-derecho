import fs from 'node:fs';
import path from 'node:path';

const playwright = await import(process.env.PSR_PLAYWRIGHT_PATH || 'playwright');
const { chromium } = playwright;

const base = (process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho').replace(/\/$/, '');
const out = process.env.PSR_SCREENSHOT_DIR || 'artifacts/post7-2022-omnidirectional-map';
const browserPath = process.env.PSR_BROWSER_PATH || undefined;

const routes = [
  ['en-takeover', '/en/sun-park-takeover-7-june-2018/'],
  ['es-takeover', '/es/toma-control-sun-park-7-junio-2018/'],
  ['en-acta', '/en/community-instrumentalisation/acta-document-room/2022-02-04/'],
  ['es-acta', '/es/comunidad-instrumentalizacion/sala-documental-actas/2022-02-04/'],
];

const viewports = {
  desktop: { width: 1440, height: 1000 },
  tablet: { width: 900, height: 1000 },
  mobile: { width: 390, height: 844 },
};

fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({
  headless: true,
  ...(browserPath ? { executablePath: browserPath } : {}),
});
const results = [];
let failed = false;

try {
  for (const [name, route] of routes) {
    for (const [device, viewport] of Object.entries(viewports)) {
      const page = await browser.newPage({ viewportSize: viewport });
      const errors = [];
      page.on('pageerror', error => errors.push(`pageerror: ${error.message}`));
      page.on('console', message => {
        if (message.type() === 'error') errors.push(`console: ${message.text()}`);
      });

      try {
        const response = await page.goto(`${base}${route}`, { waitUntil: 'networkidle', timeout: 45000 });
        if (!response || !response.ok()) errors.push(`HTTP ${response?.status() || 'no response'}`);
        const map = page.locator('.omni-acta-map');
        if (await map.count() !== 1) {
          errors.push(`expected one map, found ${await map.count()}`);
        } else {
          await map.scrollIntoViewIfNeeded();
        }

        const metrics = await page.evaluate(() => {
          const map = document.querySelector('.omni-acta-map');
          if (!map) return null;
          const statuses = [...map.querySelectorAll('.omni-status-legend [data-status]')]
            .map(node => node.getAttribute('data-status'));
          return {
            nodeCount: map.querySelectorAll('.omni-node').length,
            processCount: map.querySelectorAll('.omni-process > li').length,
            termCount: map.querySelectorAll('.omni-map-terms > .omni-term').length,
            linkCount: map.querySelectorAll('a[href]').length,
            statuses: [...new Set(statuses)].sort(),
            mapOverflow: map.scrollWidth - map.clientWidth,
            documentOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
            connectorRule: map.querySelector('.omni-connector-rule')?.textContent?.replace(/\s+/g, ' ').trim() || '',
            protectionText: [...map.querySelectorAll('.omni-term')]
              .map(node => node.textContent?.replace(/\s+/g, ' ').trim() || '')
              .find(text => /court-protected|protegidos por el juzgado/i.test(text)) || '',
          };
        });

        if (!metrics) {
          errors.push('map metrics unavailable');
        } else {
          if (metrics.nodeCount !== 8) errors.push(`nodes ${metrics.nodeCount} != 8`);
          if (metrics.processCount !== 6) errors.push(`process stages ${metrics.processCount} != 6`);
          if (metrics.termCount !== 3) errors.push(`terminology panels ${metrics.termCount} != 3`);
          if (metrics.linkCount < 15) errors.push(`links ${metrics.linkCount} < 15`);
          if (metrics.statuses.join(',') !== 'attributed,contrary,documented,inference,open') {
            errors.push(`status set mismatch: ${metrics.statuses.join(',')}`);
          }
          if (metrics.mapOverflow > 2) errors.push(`map horizontal overflow ${metrics.mapOverflow}px`);
          if (metrics.documentOverflow > 2) errors.push(`document horizontal overflow ${metrics.documentOverflow}px`);
          if (!/prove|demostrar/i.test(metrics.connectorRule)) errors.push('connector proof rule not rendered');
          if (!/protection architecture|arquitectura de protección/i.test(metrics.protectionText)) {
            errors.push('judicial-safeguards qualification not rendered');
          }
        }

        if (await map.count() === 1) {
          await map.screenshot({ path: path.join(out, `${name}-${device}.png`) });
        }
        results.push({ name, route, device, viewport, metrics, errors });
      } catch (error) {
        errors.push(String(error));
        results.push({ name, route, device, viewport, metrics: null, errors });
      } finally {
        if (errors.length) failed = true;
        await page.close();
      }
    }
  }
} finally {
  await browser.close();
}

fs.writeFileSync(path.join(out, 'result.json'), JSON.stringify({ base, routes: routes.length, viewports: Object.keys(viewports).length, results }, null, 2));

if (failed) {
  console.error('Post-7-June / 4-February omnidirectional-map render validation failed');
  for (const item of results.filter(item => item.errors.length)) {
    console.error(`${item.name} ${item.device}: ${item.errors.join('; ')}`);
  }
  process.exit(1);
}

console.log(`Post-7-June / 4-February omnidirectional-map render validation: PASS (${results.length} route/viewport checks)`);

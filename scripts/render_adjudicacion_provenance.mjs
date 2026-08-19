import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { chromium } from 'playwright';

const base = (process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho').replace(/\/$/, '');
const executablePath = process.env.PSR_BROWSER_PATH || undefined;
const outputDir = process.env.PSR_ADJUDICACION_ARTIFACT_DIR || 'artifacts/adjudicacion-provenance';

const canonicalRoutes = [
  {
    key: 'es-canonical',
    route: '/es/adjudicacion-2022-reconstruccion-documental/',
    marker: 'Control de versiones y uso previo',
    row: 'Versiones y uso previo',
  },
  {
    key: 'en-canonical',
    route: '/en/2022-adjudication-documentary-reconstruction/',
    marker: 'Version control and prior use',
    row: 'Draft versions and prior use',
  },
];

const crossLinkRoutes = [
  ['/es/actua-2018-prueba-espacial/', '/por-derecho/es/adjudicacion-2022-reconstruccion-documental/'],
  ['/en/actua-2018-spatial-test/', '/por-derecho/en/2022-adjudication-documentary-reconstruction/'],
  ['/es/acosta-matos-perimetro/', '/por-derecho/es/adjudicacion-2022-reconstruccion-documental/'],
  ['/en/acosta-matos-perimeter/', '/por-derecho/en/2022-adjudication-documentary-reconstruction/'],
  ['/es/ricpe-responsabilidad-documental/', '/por-derecho/es/adjudicacion-2022-reconstruccion-documental/'],
  ['/en/ricpe-documentary-accountability/', '/por-derecho/en/2022-adjudication-documentary-reconstruction/'],
  ['/es/acreedor-de-registro/', '/por-derecho/es/adjudicacion-2022-reconstruccion-documental/'],
  ['/en/lender-of-record/', '/por-derecho/en/2022-adjudication-documentary-reconstruction/'],
  ['/es/articulo-1535-dia-cero-antes-dia-nueve/', '/por-derecho/es/adjudicacion-2022-reconstruccion-documental/'],
  ['/en/article-1535-day-zero-before-day-nine/', '/por-derecho/en/2022-adjudication-documentary-reconstruction/'],
];

await fs.mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true, executablePath });
const context = await browser.newContext({ viewport: { width: 1440, height: 1100 } });
const results = [];

async function open(route) {
  const page = await context.newPage();
  const url = `${base}${route}`;
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  return { page, url };
}

try {
  for (const item of canonicalRoutes) {
    const { page, url } = await open(item.route);
    await page.waitForSelector('#adjudicacion-version-control[data-live-marker="adjudicacion-version-control-20260819"]', { timeout: 15000 });
    await page.waitForSelector('tr[data-adjudicacion-prior-use-row="true"]', { timeout: 15000 });
    const text = await page.locator('#adjudicacion-version-control').innerText();
    const rowText = await page.locator('tr[data-adjudicacion-prior-use-row="true"]').innerText();
    const passed = text.includes(item.marker)
      && text.includes('19')
      && rowText.includes(item.row);
    results.push({ key: item.key, url, passed, marker: item.marker, row: item.row });
    if (!passed) throw new Error(`Canonical provenance assertions failed for ${url}`);
    await page.screenshot({ path: path.join(outputDir, `${item.key}.png`), fullPage: true });
    await page.close();
  }

  for (const [route, expectedHref] of crossLinkRoutes) {
    const key = route.replace(/^\//, '').replace(/\/$/, '').replaceAll('/', '--');
    const { page, url } = await open(route);
    await page.waitForSelector('[data-adjudicacion-crosslink][data-live-marker="adjudicacion-crosslink-20260819"]', { timeout: 15000 });
    const href = await page.locator('[data-adjudicacion-crosslink] a').first().getAttribute('href');
    const text = await page.locator('[data-adjudicacion-crosslink]').innerText();
    const passed = href === expectedHref
      && /Reconstrucción de la adjudicación de 2022|The 2022 adjudication reconstruction/.test(text);
    results.push({ key, url, passed, href, expectedHref });
    if (!passed) throw new Error(`Cross-link assertions failed for ${url}: ${href}`);
    await page.close();
  }
} finally {
  await browser.close();
  await fs.writeFile(
    path.join(outputDir, 'result.json'),
    JSON.stringify({ base, status: results.every(item => item.passed) ? 'PASS' : 'FAIL', results }, null, 2),
    'utf8',
  );
}

if (!results.every(item => item.passed)) process.exit(1);
console.log(JSON.stringify({ base, status: 'PASS', checked: results.length, results }, null, 2));

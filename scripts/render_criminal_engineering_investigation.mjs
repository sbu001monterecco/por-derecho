import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { chromium } from 'playwright';

const base = (process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho').replace(/\/$/, '');
const executablePath = process.env.PSR_BROWSER_PATH || undefined;
const outputDir = process.env.PSR_CRIMINAL_ENGINEERING_ARTIFACT_DIR || 'artifacts/criminal-engineering-investigation';

const canonicalRoutes = [
  {
    key: 'es-canonical',
    route: '/es/ingenieria-forense-criminal-sun-park/',
    markers: ['ALEGACIÓN CENTRAL DE POR DERECHO', 'Las ocho fases de la presunta ingeniería', 'LAJ / oficina judicial', 'Escala de facilitación E0–E7', 'Derecho de respuesta'],
  },
  {
    key: 'en-canonical',
    route: '/en/sun-park-criminal-engineering-investigation/',
    markers: ['POR DERECHO CENTRAL ALLEGATION', 'The eight phases of the alleged engineering', 'LAJ / judicial office', 'E0–E7 enabler ladder', 'Right of response'],
  },
];

const gatewayRoutes = [
  ['/es/acosta-matos-perimetro/', 'cam', '/por-derecho/es/ingenieria-forense-criminal-sun-park/'],
  ['/en/acosta-matos-perimeter/', 'cam', '/por-derecho/en/sun-park-criminal-engineering-investigation/'],
  ['/es/ricpe-responsabilidad-documental/', 'ricpe', '/por-derecho/es/ingenieria-forense-criminal-sun-park/'],
  ['/en/ricpe-documentary-accountability/', 'ricpe', '/por-derecho/en/sun-park-criminal-engineering-investigation/'],
  ['/es/concurso-36-2012-administrador-concursal/', 'ac', '/por-derecho/es/ingenieria-forense-criminal-sun-park/'],
  ['/en/insolvency-36-2012-insolvency-administrator/', 'ac', '/por-derecho/en/sun-park-criminal-engineering-investigation/'],
  ['/es/concurso-36-2012-magistrado-juez/', 'judge', '/por-derecho/es/ingenieria-forense-criminal-sun-park/'],
  ['/en/insolvency-36-2012-mercantile-court-1/', 'judge', '/por-derecho/en/sun-park-criminal-engineering-investigation/'],
  ['/es/adjudicacion-2022-reconstruccion-documental/', 'adjudication', '/por-derecho/es/ingenieria-forense-criminal-sun-park/'],
  ['/en/2022-adjudication-documentary-reconstruction/', 'adjudication', '/por-derecho/en/sun-park-criminal-engineering-investigation/'],
  ['/es/acreedor-de-registro/', 'credit', '/por-derecho/es/ingenieria-forense-criminal-sun-park/'],
  ['/en/lender-of-record/', 'credit', '/por-derecho/en/sun-park-criminal-engineering-investigation/'],
  ['/es/ingenieria-inversa-360-cadena-sun-park/', 'adjudication', '/por-derecho/es/ingenieria-forense-criminal-sun-park/'],
  ['/en/reverse-engineering-360-sun-park-chain/', 'adjudication', '/por-derecho/en/sun-park-criminal-engineering-investigation/'],
];

await fs.mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true, executablePath });
const context = await browser.newContext({ viewport: { width: 1440, height: 1200 } });
const results = [];

async function open(route) {
  const page = await context.newPage();
  const url = `${base}${route}`;
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {});
  return { page, url };
}

try {
  for (const item of canonicalRoutes) {
    const { page, url } = await open(item.route);
    const body = await page.locator('body').innerText();
    const passed = item.markers.every(marker => body.includes(marker));
    results.push({ key: item.key, url, passed, markers: Object.fromEntries(item.markers.map(marker => [marker, body.includes(marker)])) });
    if (!passed) throw new Error(`Canonical criminal-engineering markers failed for ${url}`);
    await page.screenshot({ path: path.join(outputDir, `${item.key}.png`), fullPage: true });
    await page.close();
  }

  for (const [route, category, expectedHref] of gatewayRoutes) {
    const key = route.replace(/^\//, '').replace(/\/$/, '').replaceAll('/', '--');
    const { page, url } = await open(route);
    await page.waitForSelector(`[data-criminal-engineering-gateway][data-criminal-engineering-category="${category}"]`, { timeout: 20000 });
    const gateway = page.locator('[data-criminal-engineering-gateway]').first();
    const href = await gateway.locator('a').getAttribute('href');
    const text = await gateway.innerText();
    const passed = href === expectedHref
      && /ALEGACIÓN, NO HALLAZGO|ALLEGATION, NOT FINDING/.test(text)
      && /autoridad \+ conocimiento \+ deber|authority \+ knowledge \+ duty/.test(text);
    results.push({ key, url, category, passed, href, expectedHref });
    if (!passed) throw new Error(`Criminal-engineering gateway failed for ${url}: ${href}`);
    await page.close();
  }
} finally {
  await browser.close();
  const status = results.every(item => item.passed) ? 'PASS' : 'FAIL';
  await fs.writeFile(path.join(outputDir, 'result.json'), JSON.stringify({ base, status, checked: results.length, results }, null, 2), 'utf8');
}

if (!results.every(item => item.passed)) process.exit(1);
console.log(JSON.stringify({ base, status: 'PASS', checked: results.length, results }, null, 2));

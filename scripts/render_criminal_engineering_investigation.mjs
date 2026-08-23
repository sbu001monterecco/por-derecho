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
    markers: ['ALEGACIÓN CENTRAL DE POR DERECHO', 'Estado de prueba:', 'Hay que reconstruir si', 'Registro vivo CE-001–CE-010'],
    issueCount: 4,
  },
  {
    key: 'en-canonical',
    route: '/en/sun-park-criminal-engineering-investigation/',
    markers: ['POR DERECHO CENTRAL ALLEGATION', 'State of proof:', 'The investigation must determine whether', 'Live CE-001–CE-010 register'],
    issueCount: 4,
  },
];

const controlRoutes = [
  { key: 'es-control', route: '/es/sala-control-caso/', markers: ['Sala de Control del Caso', 'Registro vivo CE-001–CE-010'], issueCount: 10 },
  { key: 'en-control', route: '/en/case-control-room/', markers: ['Case Control Room', 'Live CE-001–CE-010 register'], issueCount: 10 },
];

const homepageRoutes = [
  { key: 'es-home', route: '/es/', markers: ['Una sola entrada para entender qué está documentado', 'Abrir Sala de Control'] },
  { key: 'en-home', route: '/en/', markers: ['One entry point for what is documented', 'Open Case Control Room'] },
];

const contextRoutes = [
  ['/es/acosta-matos-perimetro/', 'cam', 'CE-003 · CE-005 · CE-009 · CE-010'],
  ['/en/acosta-matos-perimeter/', 'cam', 'CE-003 · CE-005 · CE-009 · CE-010'],
  ['/es/ricpe-responsabilidad-documental/', 'ricpe', 'CE-005 · CE-010'],
  ['/en/ricpe-documentary-accountability/', 'ricpe', 'CE-005 · CE-010'],
  ['/es/concurso-36-2012-administrador-concursal/', 'ac', 'CE-001 · CE-002 · CE-006'],
  ['/en/insolvency-36-2012-insolvency-administrator/', 'ac', 'CE-001 · CE-002 · CE-006'],
  ['/es/concurso-36-2012-magistrado-juez/', 'judge', 'CE-002 · CE-007'],
  ['/en/insolvency-36-2012-mercantile-court-1/', 'judge', 'CE-002 · CE-007'],
  ['/es/concurso-36-2012-laj/', 'laj', 'CE-002 · CE-007'],
  ['/en/insolvency-36-2012-laj/', 'laj', 'CE-002 · CE-007'],
  ['/es/adjudicacion-2022-reconstruccion-documental/', 'adjudication', 'CE-001 · CE-002 · CE-004'],
  ['/en/2022-adjudication-documentary-reconstruction/', 'adjudication', 'CE-001 · CE-002 · CE-004'],
];

const newRoutes = [
  { key:'es-corrections', route:'/es/correcciones-control-versiones/', markers:['Correcciones materiales vigentes','LIVE_VERIFIED','Control de versiones y uso previo'] },
  { key:'en-corrections', route:'/en/corrections-version-control/', markers:['Current material corrections','LIVE_VERIFIED','Version control and prior use'] },
  { key:'es-notary', route:'/es/implementacion-notarial-protocolo-457/', markers:['protocolo 457','13.168.082,02 €','Defensa notarial más fuerte'] },
  { key:'en-notary', route:'/en/notarial-implementation-protocol-457/', markers:['Protocol 457','EUR 13,168,082.02','Strongest notarial defence'] },
  { key:'es-registry', route:'/es/implementacion-registral-finca-por-finca/', markers:['finca por finca','Cancelación solicitada','Defensa registral más fuerte'] },
  { key:'en-registry', route:'/en/land-registry-implementation-property-by-property/', markers:['property by property','Cancellation requested','Strongest Registry defence'] },
  { key:'es-updates', route:'/es/actualizaciones/', markers:['19 agosto 2026 · arquitectura del caso','Sala de Control, registro CE-001–CE-010'] },
  { key:'en-updates', route:'/en/updates/', markers:['19 August 2026 · case architecture','Case Control Room, CE-001–CE-010 register'] },
];

await fs.mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true, executablePath });
const context = await browser.newContext({ viewport: { width: 1440, height: 1200 } });
const results = [];

async function open(route) {
  const page = await context.newPage();
  const url = `${base}${route}`;
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForLoadState('networkidle', { timeout: 25000 }).catch(() => {});
  await page.waitForSelector('[data-case-hub-strip]', { timeout: 25000 });
  return { page, url };
}

async function assertNoLegacyGateways(page, url) {
  await page.waitForTimeout(250);
  const legacy360 = await page.locator('#reverse-engineering-360-gateway-20260819').count();
  const legacyCriminal = await page.locator('[data-criminal-engineering-gateway]').count();
  if (legacy360 || legacyCriminal) throw new Error(`Legacy duplicate gateway remains on ${url}: 360=${legacy360}, criminal=${legacyCriminal}`);
}

try {
  for (const item of canonicalRoutes) {
    const { page, url } = await open(item.route);
    await page.waitForSelector('[data-case-proof-panel]', { timeout: 25000 });
    await page.waitForSelector('[data-case-issue-register]', { timeout: 25000 });
    const body = await page.locator('body').innerText();
    const count = await page.locator('[data-ce-issue]').count();
    const passed = item.markers.every(marker => body.includes(marker))
      && count === item.issueCount
      && await page.locator('[data-case-evidence-legend]').count() === 1;
    results.push({ key: item.key, url, passed, issueCount: count, markers: Object.fromEntries(item.markers.map(marker => [marker, body.includes(marker)])) });
    if (!passed) throw new Error(`Canonical case architecture failed for ${url}`);
    await assertNoLegacyGateways(page, url);
    await page.screenshot({ path: path.join(outputDir, `${item.key}.png`), fullPage: true });
    await page.close();
  }

  for (const item of controlRoutes) {
    const { page, url } = await open(item.route);
    await page.waitForSelector('[data-case-issue-register]', { timeout: 25000 });
    const body = await page.locator('body').innerText();
    const count = await page.locator('[data-ce-issue]').count();
    const passed = item.markers.every(marker => body.includes(marker))
      && count === item.issueCount
      && await page.locator('[data-case-evidence-legend]').count() === 1;
    results.push({ key: item.key, url, passed, issueCount: count });
    if (!passed) throw new Error(`Control Room architecture failed for ${url}`);
    await assertNoLegacyGateways(page, url);
    await page.screenshot({ path: path.join(outputDir, `${item.key}.png`), fullPage: true });
    await page.close();
  }

  for (const item of homepageRoutes) {
    const { page, url } = await open(item.route);
    const progressiveRecord = page.locator('[data-audience-full-record] > details');
    if (await progressiveRecord.count()) await progressiveRecord.evaluate((node) => { node.open = true; });
    await page.waitForSelector('[data-case-status-band]', { timeout: 25000 });
    const body = await page.locator('body').innerText();
    const passed = item.markers.every(marker => body.includes(marker));
    results.push({ key: item.key, url, passed });
    if (!passed) throw new Error(`Homepage case status failed for ${url}`);
    await assertNoLegacyGateways(page, url);
    await page.close();
  }

  for (const [route, category, issues] of contextRoutes) {
    const key = route.replace(/^\//, '').replace(/\/$/, '').replaceAll('/', '--');
    const { page, url } = await open(route);
    await page.waitForSelector(`[data-case-context-gateway][data-case-context-category="${category}"]`, { timeout: 25000 });
    const gateway = page.locator('[data-case-context-gateway]').first();
    const text = await gateway.innerText();
    const links = await gateway.locator('a').count();
    const passed = text.includes(issues)
      && /autoridad \+ conocimiento \+ deber|authority \+ knowledge \+ duty/.test(text)
      && links === 3;
    results.push({ key, url, category, passed, links, issues });
    if (!passed) throw new Error(`Compact case context failed for ${url}`);
    await assertNoLegacyGateways(page, url);
    await page.close();
  }

  for (const item of newRoutes) {
    const { page, url } = await open(item.route);
    const body = await page.locator('body').innerText();
    const passed = item.markers.every(marker => body.includes(marker));
    results.push({ key: item.key, url, passed, markers: Object.fromEntries(item.markers.map(marker => [marker, body.includes(marker)])) });
    if (!passed) throw new Error(`New route markers failed for ${url}`);
    await assertNoLegacyGateways(page, url);
    if (/corrections|correcciones|notarial|notary|registral|registry/.test(item.key)) {
      await page.screenshot({ path: path.join(outputDir, `${item.key}.png`), fullPage: true });
    }
    await page.close();
  }
} finally {
  await browser.close();
  const status = results.every(item => item.passed) ? 'PASS' : 'FAIL';
  await fs.writeFile(path.join(outputDir, 'result.json'), JSON.stringify({ base, status, checked: results.length, results }, null, 2), 'utf8');
}

if (!results.every(item => item.passed)) process.exit(1);
console.log(JSON.stringify({ base, status: 'PASS', checked: results.length, results }, null, 2));

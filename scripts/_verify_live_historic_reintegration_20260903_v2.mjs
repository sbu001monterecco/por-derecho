import { chromium } from 'playwright';
import assert from 'node:assert/strict';

const BASE = 'https://sbu001monterecco.github.io/por-derecho';
const RELEASE_SHA = 'efbb1032b0c5e21ca892b3a9db17b3f7b4073e6c';
const SUCCESSOR_MAIN_SHA = '231d25c12108579efdf92365cf7860bf281178f5';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1440, height: 1200 } });
const page = await context.newPage();
page.setDefaultTimeout(25000);

const log = (m) => console.log(`[live-browser] ${m}`);

async function gotoOk(path, expected = []) {
  const response = await page.goto(`${BASE}${path}`, { waitUntil: 'networkidle' });
  assert(response, `No response for ${path}`);
  assert(response.status() >= 200 && response.status() < 400, `${path} returned ${response.status()}`);
  const body = await page.locator('body').innerText();
  assert(!/There isn't a GitHub Pages site here|404\s*File not found/i.test(body), `${path} rendered a Pages 404`);
  for (const token of expected) assert(body.includes(token), `${path} missing ${token}`);
  log(`ROUTE OK ${response.status()} ${path} :: ${await page.title()}`);
}

async function expect404(path) {
  const response = await page.goto(`${BASE}${path}`, { waitUntil: 'domcontentloaded' });
  assert(response, `No response for ${path}`);
  assert.equal(response.status(), 404, `${path} should be 404, got ${response.status()}`);
  log(`NEGATIVE ROUTE OK 404 ${path}`);
}

async function searchAndClick(lang, query, expectedId, expectedPath) {
  await gotoOk(`/${lang}/`, ['Por Derecho']);
  const input = page.locator('#canonical-home-search-input');
  await input.waitFor({ state: 'visible' });
  await input.fill(query);
  const result = page.locator(`a.canonical-search-result[data-search-result-id="${expectedId}"]`).first();
  await result.waitFor({ state: 'visible' });
  const href = await result.getAttribute('href');
  assert(href, `${query} result lacks href`);
  const parsed = new URL(href, BASE);
  assert(parsed.pathname.includes(expectedPath), `${query} -> ${parsed.pathname}, expected ${expectedPath}`);
  await Promise.all([page.waitForLoadState('domcontentloaded'), result.click()]);
  assert(page.url().includes(expectedPath), `${query} click landed at ${page.url()}`);
  log(`SEARCH OK ${lang} ${query} -> ${expectedId} -> ${expectedPath}`);
}

async function searchAbsent(lang, query) {
  await gotoOk(`/${lang}/`, ['Por Derecho']);
  const input = page.locator('#canonical-home-search-input');
  await input.waitFor({ state: 'visible' });
  await input.fill(query);
  await page.waitForTimeout(600);
  const count = await page.locator('a.canonical-search-result').count();
  assert.equal(count, 0, `${query} unexpectedly produced ${count} result(s)`);
  log(`SEARCH NEGATIVE OK ${lang} ${query}`);
}

async function textAsset(path) {
  const r = await context.request.get(`${BASE}${path}`, { failOnStatusCode: false });
  assert(r.status() >= 200 && r.status() < 400, `${path} returned ${r.status()}`);
  return (await r.text()).toLowerCase();
}

try {
  log(`Release proof anchor ${RELEASE_SHA}; current successor main ${SUCCESSOR_MAIN_SHA}`);

  await gotoOk('/es/', ['Por Derecho']);
  await gotoOk('/en/', ['Por Derecho']);
  await gotoOk('/es/procedimientos/gc-civ-003/', ['Diligencias Preliminares 1041/2017', '3501642120170028407', 'Juan Avello Formoso', 'Fernando Pérez Polo']);
  await gotoOk('/en/proceedings/gc-civ-003/', [
    'Diligencias Preliminares 1041/2017', 'GC-CIV-003', '3501642120170028407',
    'Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria',
    'PD-SP-I-0048', 'Juan Avello Formoso', 'PD-SP-P-0124',
    'Fernando Pérez Polo', 'PD-SP-P-0165',
    'Preceding signed Auto', '19-Feb-2018', '5-Mar-2018'
  ]);
  await gotoOk('/es/registro-autoridad-historica-las-palmas-civil/', ['Fernando Pérez Polo', 'PD-SP-P-0165', 'PD-SP-I-0048']);
  await gotoOk('/en/historic-las-palmas-civil-justice-authority-register/', ['Fernando Pérez Polo', 'PD-SP-P-0165', 'PD-SP-I-0048']);
  await gotoOk('/es/registro-maestro-procedimientos/', ['GC-CIV-003']);
  await gotoOk('/en/master-proceedings-register/', ['GC-CIV-003']);
  await gotoOk('/es/mapa-procedimientos/', ['GC-CIV-003']);
  await gotoOk('/en/proceedings-map/', ['GC-CIV-003']);

  for (const [query, id] of [
    ['Diligencias Preliminares 1041/2017', 'GC-CIV-003'],
    ['3501642120170028407', 'GC-CIV-003'],
    ['GC-CIV-003', 'GC-CIV-003']
  ]) {
    await searchAndClick('es', query, id, '/es/procedimientos/gc-civ-003/');
    await searchAndClick('en', query, id, '/en/proceedings/gc-civ-003/');
  }

  await searchAndClick('es', 'Juan Avello Formoso', 'PD-SP-P-0124', '/es/registro-identidad-profesionales-justicia/');
  await searchAndClick('en', 'Juan Avello Formoso', 'PD-SP-P-0124', '/en/justice-professionals-identity-register/');
  await searchAndClick('es', 'Fernando Pérez Polo', 'PD-SP-P-0165', '/es/registro-autoridad-historica-las-palmas-civil/');
  await searchAndClick('en', 'Fernando Pérez Polo', 'PD-SP-P-0165', '/en/historic-las-palmas-civil-justice-authority-register/');
  await searchAndClick('en', 'PD-SP-P-0165', 'PD-SP-P-0165', '/en/historic-las-palmas-civil-justice-authority-register/');
  await searchAndClick('en', '^P-0165', 'PD-SP-P-0165', '/en/historic-las-palmas-civil-justice-authority-register/');
  await searchAndClick('en', 'PD-SP-I-0048', 'PD-SP-I-0048', '/en/historic-las-palmas-civil-justice-authority-register/');
  await searchAndClick('en', '^I-0048', 'PD-SP-I-0048', '/en/historic-las-palmas-civil-justice-authority-register/');
  await searchAndClick('en', 'PD-SP-R-0001', 'PD-SP-R-0001', '/en/insolvency-36-2012-active-estate-2018-2021/');
  await searchAndClick('en', '^R-0001', 'PD-SP-R-0001', '/en/insolvency-36-2012-active-estate-2018-2021/');

  await expect404('/es/procedimientos/lz-civ-050/');
  await expect404('/en/proceedings/lz-civ-050/');
  await searchAbsent('es', 'LZ-CIV-050');
  await searchAbsent('en', 'LZ-CIV-050');

  for (const asset of ['/sitemap.xml', '/assets/data/proceedings-master-public-v1.json', '/assets/data/proceeding-page-routes-20260902.json']) {
    const text = await textAsset(asset);
    assert(!text.includes('lz-civ-050'), `${asset} still references lz-civ-050`);
    log(`NEGATIVE DATA OK ${asset}`);
  }

  log('LIVE_BROWSER_VERIFIED=PASS');
} finally {
  await browser.close();
}

import { chromium } from 'playwright';
import assert from 'node:assert/strict';

const BASE = 'https://sbu001monterecco.github.io/por-derecho';
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1440, height: 1200 },
  userAgent: 'PorDerechoReleaseVerifier/2026-09-03 Chromium'
});
const page = await context.newPage();
page.setDefaultTimeout(20000);

const log = (msg) => console.log(`[live-browser] ${msg}`);

async function gotoOk(path, expectedText = null) {
  const url = `${BASE}${path}`;
  const response = await page.goto(url, { waitUntil: 'networkidle' });
  assert(response, `No navigation response for ${url}`);
  assert(response.status() >= 200 && response.status() < 400, `${url} returned ${response.status()}`);
  const body = await page.locator('body').innerText();
  assert(!/There isn't a GitHub Pages site here|404\s*File not found/i.test(body), `${url} rendered a Pages 404 body`);
  if (expectedText) assert(body.includes(expectedText), `${url} missing expected text: ${expectedText}`);
  log(`OK ${response.status()} ${path} :: ${await page.title()}`);
}

async function expect404(path) {
  const url = `${BASE}${path}`;
  const response = await page.goto(url, { waitUntil: 'domcontentloaded' });
  assert(response, `No navigation response for ${url}`);
  assert(response.status() === 404, `${url} must be 404, got ${response.status()}`);
  log(`NEGATIVE OK 404 ${path}`);
}

async function fetchText(path) {
  const response = await context.request.get(`${BASE}${path}`, { failOnStatusCode: false });
  assert(response.status() >= 200 && response.status() < 400, `${path} returned ${response.status()}`);
  return await response.text();
}

async function searchAndClick(lang, query, expectedId, expectedPathFragment) {
  const home = `/${lang}/`;
  await gotoOk(home);
  const input = page.locator('#canonical-home-search-input');
  await input.waitFor({ state: 'visible' });
  await input.fill(query);
  const result = page.locator(`a.canonical-search-result[data-search-result-id="${expectedId}"]`);
  await result.waitFor({ state: 'visible' });
  const href = await result.getAttribute('href');
  assert(href, `Search ${lang}:${query} result ${expectedId} has no href`);
  const parsed = new URL(href, BASE);
  assert.equal(parsed.origin, new URL(BASE).origin, `Search ${query} escaped controlled site`);
  assert(parsed.pathname.includes(expectedPathFragment), `Search ${query} -> ${parsed.pathname}, expected ${expectedPathFragment}`);
  log(`SEARCH OK ${lang} ${JSON.stringify(query)} -> ${expectedId} -> ${parsed.pathname}${parsed.hash}`);
  await Promise.all([
    page.waitForLoadState('domcontentloaded'),
    result.click()
  ]);
  assert(page.url().includes(expectedPathFragment), `Search click ${query} landed at ${page.url()}`);
  const body = await page.locator('body').innerText();
  assert(body.trim().length > 100, `Search click ${query} landed on empty page`);
}

async function searchMustBeAbsent(lang, query) {
  await gotoOk(`/${lang}/`);
  const input = page.locator('#canonical-home-search-input');
  await input.waitFor({ state: 'visible' });
  await input.fill(query);
  await page.waitForTimeout(700);
  const count = await page.locator('a.canonical-search-result').count();
  assert.equal(count, 0, `Deprecated ${query} unexpectedly produced ${count} search result(s) on ${lang}`);
  const status = (await page.locator('#canonical-home-search-status').innerText()).toLowerCase();
  assert(/sin coincidencias|no matches/.test(status), `Deprecated ${query} search status was ${status}`);
  log(`SEARCH NEGATIVE OK ${lang} ${query}`);
}

try {
  // Core bilingual live routes.
  await gotoOk('/es/', 'Por Derecho');
  await gotoOk('/en/', 'Por Derecho');
  await gotoOk('/es/procedimientos/gc-civ-003/', 'Diligencias Preliminares 1041/2017');
  await gotoOk('/en/proceedings/gc-civ-003/', 'Diligencias Preliminares 1041/2017');
  await gotoOk('/es/registro-autoridad-historica-las-palmas-civil/', 'Fernando Pérez Polo');
  await gotoOk('/en/historic-las-palmas-civil-justice-authority-register/', 'Fernando Pérez Polo');
  await gotoOk('/es/registro-maestro-procedimientos/', 'GC-CIV-003');
  await gotoOk('/en/master-proceedings-register/', 'GC-CIV-003');
  await gotoOk('/es/mapa-procedimientos/', 'GC-CIV-003');
  await gotoOk('/en/proceedings-map/', 'GC-CIV-003');

  // Locked correction on the dedicated proceeding page.
  await gotoOk('/en/proceedings/gc-civ-003/', '3501642120170028407');
  const gcBody = await page.locator('body').innerText();
  for (const token of [
    'GC-CIV-003',
    'Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria',
    'PD-SP-I-0048',
    'Juan Avello Formoso',
    'PD-SP-P-0124',
    'Fernando Pérez Polo',
    'PD-SP-P-0165',
    'Preceding signed Auto',
    '19-Feb-2018',
    '5-Mar-2018'
  ]) assert(gcBody.includes(token), `GC-CIV-003 live page missing ${token}`);

  // Representative homepage search click-throughs in both languages.
  const bilingualQueries = [
    ['Diligencias Preliminares 1041/2017', 'GC-CIV-003', '/proceedings/gc-civ-003/'],
    ['3501642120170028407', 'GC-CIV-003', '/proceedings/gc-civ-003/'],
    ['GC-CIV-003', 'GC-CIV-003', '/proceedings/gc-civ-003/']
  ];
  for (const [query, id] of bilingualQueries) {
    await searchAndClick('en', query, id, '/en/proceedings/gc-civ-003/');
    await searchAndClick('es', query, id, '/es/procedimientos/gc-civ-003/');
  }

  await searchAndClick('en', 'Juan Avello Formoso', 'PD-SP-P-0124', '/en/justice-professionals-identity-register/');
  await searchAndClick('es', 'Juan Avello Formoso', 'PD-SP-P-0124', '/es/registro-identidad-profesionales-justicia/');
  await searchAndClick('en', 'Fernando Pérez Polo', 'PD-SP-P-0165', '/en/historic-las-palmas-civil-justice-authority-register/');
  await searchAndClick('es', 'Fernando Pérez Polo', 'PD-SP-P-0165', '/es/registro-autoridad-historica-las-palmas-civil/');
  await searchAndClick('en', 'PD-SP-P-0165', 'PD-SP-P-0165', '/en/historic-las-palmas-civil-justice-authority-register/');
  await searchAndClick('en', '^P-0165', 'PD-SP-P-0165', '/en/historic-las-palmas-civil-justice-authority-register/');
  await searchAndClick('en', 'Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria', 'PD-SP-I-0048', '/en/historic-las-palmas-civil-justice-authority-register/');
  await searchAndClick('en', 'PD-SP-I-0048', 'PD-SP-I-0048', '/en/historic-las-palmas-civil-justice-authority-register/');
  await searchAndClick('en', '^I-0048', 'PD-SP-I-0048', '/en/historic-las-palmas-civil-justice-authority-register/');
  await searchAndClick('en', 'PD-SP-R-0001', 'PD-SP-R-0001', '/en/insolvency-36-2012-active-estate-2018-2021/');
  await searchAndClick('en', '^R-0001', 'PD-SP-R-0001', '/en/insolvency-36-2012-active-estate-2018-2021/');
  await searchAndClick('en', 'PD-SP-O-0003', 'PD-SP-O-0003', '/en/pwc-canarias-carlos-saavedra-sun-park/');

  // Deprecated duplicate must be absent from routes and public search/data surfaces.
  await expect404('/es/procedimientos/lz-civ-050/');
  await expect404('/en/proceedings/lz-civ-050/');
  await searchMustBeAbsent('es', 'LZ-CIV-050');
  await searchMustBeAbsent('en', 'LZ-CIV-050');

  for (const path of [
    '/sitemap.xml',
    '/assets/data/proceedings-master-public-v1.json',
    '/assets/data/proceeding-page-routes-20260902.json'
  ]) {
    const text = (await fetchText(path)).toLowerCase();
    assert(!text.includes('lz-civ-050'), `${path} still references lz-civ-050`);
    log(`NEGATIVE DATA OK ${path} has no lz-civ-050`);
  }

  log('LIVE_BROWSER_VERIFIED=PASS');
} finally {
  await browser.close();
}

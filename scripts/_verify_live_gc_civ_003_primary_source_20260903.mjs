import { chromium } from 'playwright';
import assert from 'node:assert/strict';

const BASE = 'https://sbu001monterecco.github.io/por-derecho';
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1440, height: 1200 },
  userAgent: 'PorDerechoGC-CIV-003SourceVerifier/2026-09-03 Chromium'
});
const page = await context.newPage();
page.setDefaultTimeout(20000);
const log = (msg) => console.log(`[gc-civ-003-live] ${msg}`);

async function gotoBody(path) {
  const url = `${BASE}${path}`;
  const response = await page.goto(url, { waitUntil: 'networkidle' });
  assert(response, `No navigation response for ${url}`);
  assert(response.status() >= 200 && response.status() < 400, `${url} returned ${response.status()}`);
  const body = await page.locator('body').innerText();
  assert(!/There isn't a GitHub Pages site here|404\s*File not found/i.test(body), `${url} rendered a Pages 404 body`);
  log(`OK ${response.status()} ${path} :: ${await page.title()}`);
  return body;
}

async function expect404(path) {
  const response = await page.goto(`${BASE}${path}`, { waitUntil: 'domcontentloaded' });
  assert(response, `No navigation response for ${path}`);
  assert.equal(response.status(), 404, `${path} must be 404, got ${response.status()}`);
  log(`NEGATIVE OK 404 ${path}`);
}

async function searchAndClick(lang, query, expectedId, expectedPath) {
  await gotoBody(`/${lang}/`);
  const input = page.locator('#canonical-home-search-input');
  await input.waitFor({ state: 'visible' });
  await input.fill(query);
  const result = page.locator(`a.canonical-search-result[data-search-result-id="${expectedId}"]`);
  await result.waitFor({ state: 'visible' });
  const href = await result.getAttribute('href');
  assert(href, `${query} result has no href`);
  const parsed = new URL(href, BASE);
  assert(parsed.pathname.includes(expectedPath), `${query} -> ${parsed.pathname}, expected ${expectedPath}`);
  log(`SEARCH OK ${lang} ${JSON.stringify(query)} -> ${expectedId} -> ${parsed.pathname}`);
  await Promise.all([page.waitForLoadState('domcontentloaded'), result.click()]);
  assert(page.url().includes(expectedPath), `${query} click landed at ${page.url()}`);
}

async function searchAbsent(lang, query) {
  await gotoBody(`/${lang}/`);
  const input = page.locator('#canonical-home-search-input');
  await input.waitFor({ state: 'visible' });
  await input.fill(query);
  await page.waitForTimeout(700);
  const count = await page.locator('a.canonical-search-result').count();
  assert.equal(count, 0, `${query} unexpectedly produced ${count} result(s) on ${lang}`);
  log(`SEARCH NEGATIVE OK ${lang} ${query}`);
}

try {
  const es = await gotoBody('/es/procedimientos/gc-civ-003/');
  for (const token of [
    'GC-CIV-003',
    '3501642120170028407',
    'PD-SP-I-0048',
    'Juan Avello Formoso',
    'PD-SP-P-0124',
    'Fernando Pérez Polo',
    'PD-SP-P-0165',
    'FUENTE ACTUALIZADA 03-SEP-2026',
    '19-Dic-2017',
    '23-Ene-2018',
    '19-Feb-2018',
    '05-Mar-2018',
    'fuertemente trazado'
  ]) assert(es.includes(token), `Spanish GC-CIV-003 page missing ${token}`);
  assert(!es.includes('Preceding signed Auto'), 'Spanish page still contains obsolete English signed-Auto gap wording');

  const en = await gotoBody('/en/proceedings/gc-civ-003/');
  for (const token of [
    'GC-CIV-003',
    '3501642120170028407',
    'PD-SP-I-0048',
    'Juan Avello Formoso',
    'PD-SP-P-0124',
    'Fernando Pérez Polo',
    'PD-SP-P-0165',
    'SOURCE UPDATED 03-SEP-2026',
    '19-Dec-2017',
    '23-Jan-2018',
    '19-Feb-2018',
    '05-Mar-2018',
    'strongly traced'
  ]) assert(en.includes(token), `English GC-CIV-003 page missing ${token}`);
  assert(!/Preceding signed Auto\s*[;,]/i.test(en), 'English page still presents preceding signed Auto as an open gap');

  const response = await context.request.get(`${BASE}/assets/data/gc-civ-003-primary-source-state-20260903.json`, { failOnStatusCode: false });
  assert.equal(response.status(), 200, `machine source-state returned ${response.status()}`);
  const state = JSON.parse(await response.text());
  assert.equal(state.proceeding.master_id, 'GC-CIV-003');
  assert.equal(state.proceeding.nig, '3501642120170028407');
  assert.equal(state.proceeding.court.id, 'PD-SP-I-0048');
  assert.equal(state.proceeding.judge.id, 'PD-SP-P-0124');
  assert.equal(state.proceeding.laj.id, 'PD-SP-P-0165');
  assert.equal(state.historic_docket_state, 'OPEN_NOT_CERTIFIED_COMPLETE');
  assert.equal(state.closure_trace.state, 'STRONGLY_TRACED_PRIMARY_FILE_STILL_TO_RECOVER');
  assert(state.closed_gaps.some(x => x.includes('19-Dec-2017')));
  assert(state.gaps.some(x => x.gap_id === 'GC-CIV-003-GAP-20180219' && x.state === 'SOURCE_GAP'));
  assert(state.gaps.some(x => x.gap_id === 'GC-CIV-003-GAP-20180305-DECREE' && x.state === 'STRONGLY_TRACED_PRIMARY_FILE_STILL_TO_RECOVER'));
  log('MACHINE SOURCE STATE OK');

  for (const query of ['GC-CIV-003', '3501642120170028407']) {
    await searchAndClick('es', query, 'GC-CIV-003', '/es/procedimientos/gc-civ-003/');
    await searchAndClick('en', query, 'GC-CIV-003', '/en/proceedings/gc-civ-003/');
  }
  await searchAndClick('es', 'Juan Avello Formoso', 'PD-SP-P-0124', '/es/registro-identidad-profesionales-justicia/');
  await searchAndClick('en', 'Fernando Pérez Polo', 'PD-SP-P-0165', '/en/historic-las-palmas-civil-justice-authority-register/');
  await searchAndClick('en', 'PD-SP-I-0048', 'PD-SP-I-0048', '/en/historic-las-palmas-civil-justice-authority-register/');

  await expect404('/es/procedimientos/lz-civ-050/');
  await expect404('/en/proceedings/lz-civ-050/');
  await searchAbsent('es', 'LZ-CIV-050');
  await searchAbsent('en', 'LZ-CIV-050');

  for (const path of ['/sitemap.xml', '/assets/data/proceedings-master-public-v1.json', '/assets/data/proceeding-page-routes-20260902.json']) {
    const r = await context.request.get(`${BASE}${path}`, { failOnStatusCode: false });
    assert(r.status() >= 200 && r.status() < 400, `${path} returned ${r.status()}`);
    const text = (await r.text()).toLowerCase();
    assert(!text.includes('lz-civ-050'), `${path} references lz-civ-050`);
    log(`NEGATIVE DATA OK ${path}`);
  }

  log('GC_CIV_003_PRIMARY_SOURCE_LIVE_BROWSER_VERIFIED=PASS');
} finally {
  await browser.close();
}

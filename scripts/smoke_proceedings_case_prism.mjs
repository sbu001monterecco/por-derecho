import { chromium } from 'playwright';

const base = process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho';
const routes = [
  { lang: 'en', path: '/en/proceedings-map/', contrary: 'Strongest contrary', sourceScope: 'proposition-level audit path', outsideSelected: 'Outside the selected file' },
  { lang: 'es', path: '/es/mapa-procedimientos/', contrary: 'Explicación / registro contrario', sourceScope: 'ruta de auditoría de la proposición', outsideSelected: 'Fuera del expediente seleccionado' },
];

async function assertFocusedAndVisible(page, selector, label) {
  try {
    await page.waitForFunction((target) => {
      const element = document.querySelector(target);
      if (!element || document.activeElement !== element) return false;
      const rect = element.getBoundingClientRect();
      return rect.top >= -10 && rect.top < window.innerHeight * 0.7;
    }, selector);
  } catch {
    throw new Error(`${label}: target did not become focused and visible`);
  }
}

const browser = await chromium.launch({ headless: true });
try {
  for (const route of routes) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const consoleErrors = [];
    page.on('console', (message) => { if (message.type() === 'error') consoleErrors.push(message.text()); });
    page.on('pageerror', (error) => consoleErrors.push(error.message));
    const response = await page.goto(`${base}${route.path}`, { waitUntil: 'networkidle' });
    if (!response?.ok()) throw new Error(`${route.lang}: route failed with ${response?.status()}`);

    const tabs = page.locator('[role="tab"]');
    if (await tabs.count() !== 6) throw new Error(`${route.lang}: expected six semantic tabs`);

    const search = page.locator('[data-map-search]');
    await search.fill('GC-APP-004');
    await page.waitForSelector('[data-node-id="GC-APP-004"]');
    await search.fill('');
    const track = page.locator('[data-map-track]');
    await track.selectOption({ index: 1 });
    await track.selectOption('');

    await page.locator('a[href="#case-prism"]').first().click();
    await page.waitForSelector('[role="tab"][data-view="prism"][aria-selected="true"]');
    if (await page.evaluate(() => location.hash) !== '#case-prism') throw new Error(`${route.lang}: Case Prism CTA did not activate the hash view`);
    await assertFocusedAndVisible(page, '[data-view-body]', `${route.lang}: Case Prism CTA`);
    await page.goBack();
    await page.waitForSelector('[role="tab"][data-view="map"][aria-selected="true"]');
    if (await page.evaluate(() => location.hash) !== '') throw new Error(`${route.lang}: browser Back did not restore the map hash state`);
    await page.goForward();
    await page.waitForSelector('[role="tab"][data-view="prism"][aria-selected="true"]');
    await assertFocusedAndVisible(page, '[data-view-body]', `${route.lang}: forward navigation`);

    await page.waitForSelector('.pdim-prism-table tbody tr');
    const matrixRows = await page.locator('.pdim-prism-table tbody tr').count();
    const matrixCells = await page.locator('.pdim-prism-cell').count();
    const laneHeaders = await page.locator('.pdim-prism-table thead th').count();
    if (matrixRows !== 18 || matrixCells !== 216 || laneHeaders !== 13) {
      throw new Error(`${route.lang}: matrix denominator mismatch (${matrixRows} rows, ${matrixCells} cells, ${laneHeaders - 1} lanes)`);
    }
    if (await page.locator('.pdim-prism-dash').count()) throw new Error(`${route.lang}: unexplained matrix dash rendered`);
    if (await page.locator('.pdim-prism-cell small').count() !== 216) throw new Error(`${route.lang}: file-treatment labels missing`);
    const firstEvidenceLabel = await page.locator('.pdim-prism-table tbody th small').first().innerText();
    if (!firstEvidenceLabel || firstEvidenceLabel.includes('_')) throw new Error(`${route.lang}: reader-facing evidence status was not localised`);

    const audience = page.locator('[data-prism-audience]');
    if (await audience.locator('option').count() !== 9) throw new Error(`${route.lang}: audience denominator is not nine`);
    await audience.selectOption('fiscal');
    await page.waitForSelector('.pdim-prism-table tbody tr:first-child');
    const firstFiscal = await page.locator('.pdim-prism-table tbody tr:first-child th').innerText();
    if (!firstFiscal.includes('P05')) throw new Error(`${route.lang}: Fiscalía lens did not reprioritise the institutional-memory row`);

    await page.locator('.pdim-prism-cell').first().click();
    const detail = page.locator('[data-prism-detail]');
    await assertFocusedAndVisible(page, '[data-view-body] [data-prism-detail]', `${route.lang}: matrix detail`);
    if (await detail.locator('.pdim-dependency-grid > div').count() < 10) throw new Error(`${route.lang}: dependency detail is incomplete`);
    if (await detail.locator('.pdim-source-links a').count() < 1) throw new Error(`${route.lang}: controlled source links missing`);
    if (!(await detail.innerText()).includes(route.contrary)) throw new Error(`${route.lang}: contrary record missing from detail`);
    if (!(await detail.innerText()).includes(route.sourceScope)) throw new Error(`${route.lang}: proposition-level source boundary missing`);
    if (await detail.getAttribute('aria-live') !== 'polite') throw new Error(`${route.lang}: detail is not announced`);
    if (await page.locator('[data-proceedings-map] [aria-live="polite"]').count() !== 1) throw new Error(`${route.lang}: duplicate broad live regions remain`);
    const sourceHref = await detail.locator('.pdim-source-links a').first().getAttribute('href');
    if (!sourceHref) throw new Error(`${route.lang}: source href missing`);
    const sourceUrl = new URL(sourceHref);
    if (!sourceUrl.pathname.startsWith(`/por-derecho/${route.lang}/`)) throw new Error(`${route.lang}: source escaped the bilingual repository route (${sourceUrl.pathname})`);
    const sourceResponse = await page.request.get(sourceHref);
    if (!sourceResponse.ok()) throw new Error(`${route.lang}: source route returned ${sourceResponse.status()}`);

    await page.locator('[data-view-body] [data-prism-prop="P04"][data-prism-lane="calificacion"]').click();
    await page.locator('[data-view-body] [data-prism-detail] [data-trace-id="GC-APP-004"]').click();
    await page.waitForSelector('[data-trace-panel] .pdim-prism-trace [data-prism-prop]');
    await assertFocusedAndVisible(page, '[data-trace-panel]', `${route.lang}: Prism-to-trace path`);
    await page.locator('[data-trace-panel] .pdim-prism-trace [data-prism-prop]').first().click();
    await page.waitForSelector('[data-trace-panel] [data-prism-detail] .pdim-prism-detail-head');
    await assertFocusedAndVisible(page, '[data-trace-panel] [data-prism-detail]', `${route.lang}: trace-local dependency detail`);

    const prismTab = page.locator('[role="tab"][data-view="prism"]');
    await prismTab.focus();
    await prismTab.press('ArrowRight');
    await page.waitForSelector('[role="tab"][data-view="lanes"][aria-selected="true"]');
    if (await page.locator('.pdim-swimlane tbody tr').count() !== 18) throw new Error(`${route.lang}: swimlane event denominator mismatch`);
    if (await page.locator('[data-lane-heading]').count() !== 12) throw new Error(`${route.lang}: stable lane headings missing`);
    if (await page.locator('.pdim-swim-cell').count() !== 216) throw new Error(`${route.lang}: swimlane coordinate denominator mismatch`);

    await page.locator('[role="tab"][data-view="isolation"]').click();
    await page.waitForSelector('[data-isolation-id]');
    const isolation = page.locator('[data-isolation-id]');
    const fullCorpusLabels = await page.locator('.pdim-isolation-map button[aria-label]').evaluateAll((elements) => elements.map((element) => element.getAttribute('aria-label') || ''));
    if (fullCorpusLabels.some((label) => label.includes(route.outsideSelected))) throw new Error(`${route.lang}: full-corpus cells are announced as outside a selected file`);
    if (await isolation.locator('option[value="GC-APP-004"]').count() !== 1) throw new Error(`${route.lang}: exact RPL 2523 option missing`);
    if (await isolation.locator('option[value="LZ-JUD-FAM-006"], option[value="X-TAX-002"]').count()) throw new Error(`${route.lang}: unverified object admitted to exact-proceeding isolation`);
    await isolation.selectOption('GC-APP-004');
    await page.waitForSelector('.pdim-isolation-map[data-isolation-mode="isolated"]');
    if (await page.locator('.pdim-isolation-map .is-suppressed').count() < 1) throw new Error(`${route.lang}: wider corpus did not fade`);
    if (await page.locator('.pdim-isolation-map .is-suppressed button:not([disabled])').count()) throw new Error(`${route.lang}: suppressed cells remain normally focusable`);
    if (await page.locator('.pdim-isolation-map .is-suppressed small').count() !== await page.locator('.pdim-isolation-map .is-suppressed').count()) throw new Error(`${route.lang}: suppressed state lacks a textual equivalent`);
    const suppressedLabels = await page.locator('.pdim-isolation-map .is-suppressed small').allInnerTexts();
    if (suppressedLabels.some((label) => label.trim() !== route.outsideSelected)) throw new Error(`${route.lang}: suppressed-state text is not localised`);
    if (await page.locator('.pdim-isolation-grid > section').count() !== 2) throw new Error(`${route.lang}: isolation comparison missing`);
    const isolationText = await page.locator('[data-view-body]').innerText();
    if (!isolationText.includes('RPL 2523/2025')) throw new Error(`${route.lang}: exact selected identity lost`);
    await page.locator('[data-isolation-restore]').click();
    await page.waitForSelector('.pdim-isolation-map[data-isolation-mode="full"]');
    if (await isolation.inputValue() !== '__FULL__') throw new Error(`${route.lang}: full corpus was not restored`);
    if (await page.locator('.pdim-isolation-map .is-suppressed').count()) throw new Error(`${route.lang}: suppressed cells remain after restore`);

    await page.locator('[role="tab"][data-view="trace"]').click();
    await page.locator('[data-trace-select]').selectOption('GC-APP-004');
    await page.waitForSelector('.pdim-prism-trace');
    if (await page.locator('.pdim-prism-trace [data-prism-prop]').count() < 1) throw new Error(`${route.lang}: trace and Prism remain disconnected`);

    await page.setViewportSize({ width: 390, height: 844 });
    await page.locator('[role="tab"][data-view="prism"]').click();
    const stickyWidth = await page.locator('.pdim-prism-table tbody th').first().evaluate((element) => element.getBoundingClientRect().width);
    if (stickyWidth > 205) throw new Error(`${route.lang}: mobile sticky proposition column is too wide (${stickyWidth})`);
    const scrollable = await page.locator('.pdim-prism-table-wrap').evaluate((element) => element.scrollWidth > element.clientWidth);
    if (!scrollable) throw new Error(`${route.lang}: mobile matrix is not horizontally navigable`);
    if (consoleErrors.length) throw new Error(`${route.lang}: console errors: ${consoleErrors.join(' | ')}`);

    await page.close();

    for (const [hash, view] of [['#case-prism', 'prism'], ['#parallel-lanes', 'lanes'], ['#isolation-test', 'isolation']]) {
      const deepLinkPage = await browser.newPage({ viewport: { width: 1280, height: 900 } });
      const deepResponse = await deepLinkPage.goto(`${base}${route.path}${hash}`, { waitUntil: 'networkidle' });
      if (!deepResponse?.ok()) throw new Error(`${route.lang}: direct ${hash} load failed with ${deepResponse?.status()}`);
      await deepLinkPage.waitForSelector(`[role="tab"][data-view="${view}"][aria-selected="true"]`);
      await assertFocusedAndVisible(deepLinkPage, '[data-view-body]', `${route.lang}: direct ${hash}`);
      await deepLinkPage.close();
    }
    console.log(`${route.lang}: 216-cell Case Prism / swimlane / exact isolation / trace / mobile smoke PASS`);
  }
} finally {
  await browser.close();
}

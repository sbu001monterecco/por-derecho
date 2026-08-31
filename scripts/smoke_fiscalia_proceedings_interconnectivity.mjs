import { chromium } from 'playwright';

const base = process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho';
const browser = await chromium.launch({ headless: true });

function fail(message) { throw new Error(message); }

try {
  const context = await browser.newContext();
  const dataResponse = await context.request.get(`${base}/assets/data/fiscalia-proceedings-interconnectivity-v1.json`);
  if (!dataResponse.ok()) fail(`interconnectivity data returned ${dataResponse.status()}`);
  const data = await dataResponse.json();
  if (data.coverage.communication_events !== 296) fail('communication denominator is not 296');
  if (data.coverage.matter_linked_events !== 117) fail('matter-linked denominator is not 117');
  if (data.coverage.fiscalia_exact_files !== 21 || data.coverage.fiscalia_unresolved_references !== 3) fail('Fiscalía identity denominator is not 21 + 3');
  if (data.event_proceeding_edges.length !== 139 || data.event_event_edges.length !== 84) fail('graph edge denominator changed');
  if (data.priority_chains.length !== 9) fail('priority-chain denominator is not nine');
  await context.close();

  const routes = [
    { lang: 'en', path: '/en/public-prosecution-communications-proceedings/', gap: 'Next source needed', unresolved: 'Unresolved reference' },
    { lang: 'es', path: '/es/fiscalia-comunicaciones-procedimientos/', gap: 'Fuente siguiente necesaria', unresolved: 'Referencia no resuelta' },
  ];
  for (const route of routes) {
    const page = await browser.newPage({ viewport: { width: 1360, height: 900 } });
    const errors = [];
    page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
    page.on('pageerror', error => errors.push(error.message));
    const response = await page.goto(`${base}${route.path}#file=NAT-FIS-004`, { waitUntil: 'networkidle' });
    if (!response?.ok()) fail(`${route.lang}: specialist route returned ${response?.status()}`);
    await page.waitForSelector('[data-mf-files] [data-file="NAT-FIS-004"][aria-current="true"]');
    if (await page.locator('.pd-mf-metric').count() !== 6) fail(`${route.lang}: expected six headline metrics`);
    if (await page.locator('[data-mf-files] [data-file]').count() !== 25) fail(`${route.lang}: expected all + 24 file controls`);
    if (await page.locator('[data-mf-chains] .pd-mf-chain').count() !== 9) fail(`${route.lang}: expected nine priority chains`);
    const detail = page.locator('[data-mf-detail]');
    if (!(await detail.innerText()).includes('NAT-FIS-004')) fail(`${route.lang}: deep-linked file was not rendered`);
    if (!(await detail.innerText()).includes(route.gap)) fail(`${route.lang}: next-source gap is not visible`);
    if (await detail.locator('[data-event-id]').count() < 1) fail(`${route.lang}: linked event chronology is empty`);

    await page.locator('[data-mf-files] [data-file="TF-FIS-009"]').click();
    await page.waitForSelector('[data-mf-files] [data-file="TF-FIS-009"][aria-current="true"]');
    const identityState = detail.locator('.pd-mf-detail-head .eyebrow');
    if (!(await identityState.isVisible()) || !(await identityState.textContent()).includes(route.unresolved)) fail(`${route.lang}: unresolved identity state is hidden`);
    if (!(await detail.innerText()).includes(route.gap)) fail(`${route.lang}: unresolved source gate is hidden`);

    await page.locator('[data-mf-direction]').selectOption('INBOUND_FROM_INSTITUTION');
    await page.locator('[data-mf-direction]').selectOption('');
    await page.locator('[data-mf-scope]').selectOption('OUTSIDE_JUDICIAL_PROCEEDING');
    await page.locator('[data-mf-scope]').selectOption('');
    if (errors.length) fail(`${route.lang}: browser console errors: ${errors.join(' | ')}`);
    await page.close();
  }

  const master = await browser.newPage({ viewport: { width: 1360, height: 900 } });
  await master.goto(`${base}/en/master-proceedings-register/#record-GC-FIS-017`, { waitUntil: 'networkidle' });
  await master.waitForSelector('[data-master-id="GC-FIS-017"] [data-fiscalia-master-id="GC-FIS-017"]');
  const masterHref = await master.locator('[data-fiscalia-master-id="GC-FIS-017"]').getAttribute('href');
  if (!masterHref?.includes('/en/public-prosecution-communications-proceedings/#file=GC-FIS-017')) fail('Master Register reciprocal route is incorrect');
  await master.close();

  const map = await browser.newPage({ viewport: { width: 1360, height: 900 } });
  await map.goto(`${base}/en/proceedings-map/#trace-proceeding=GC-CRI-008`, { waitUntil: 'networkidle' });
  await map.waitForSelector('[data-trace-panel] [data-fiscalia-master-id="GC-CRI-008"]');
  const mapHref = await map.locator('[data-trace-panel] [data-fiscalia-master-id="GC-CRI-008"]').getAttribute('href');
  if (!mapHref?.includes('/en/public-prosecution-communications-proceedings/#file=GC-CRI-008')) fail('Proceedings Map reciprocal route is incorrect');
  await map.goto(mapHref, { waitUntil: 'networkidle' });
  await map.waitForSelector('[data-mf-files] [data-file="GC-CRI-008"][aria-current="true"]');
  if (!(await map.locator('[data-mf-detail]').innerText()).includes('GC-CRI-008')) fail('non-Fiscalía proceeding-centred communication view did not render');
  await map.close();

  console.log('Fiscalía interconnectivity browser smoke: PASS — bilingual routes, deep links, filters and reciprocal navigation verified');
} finally {
  await browser.close();
}

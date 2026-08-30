import { chromium } from 'playwright';

const base = process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho';
const routes = [
  { lang: 'en', path: '/en/proceedings-map/' },
  { lang: 'es', path: '/es/mapa-procedimientos/' },
];

const browser = await chromium.launch({ headless: true });
try {
  for (const route of routes) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const response = await page.goto(`${base}${route.path}`, { waitUntil: 'networkidle' });
    if (!response || !response.ok()) throw new Error(`${route.lang}: route failed with ${response?.status()}`);

    await page.waitForSelector('[data-proceedings-map] [data-view="prism"]', { timeout: 15000 });
    const prismTab = page.locator('[data-view="prism"]');
    const lanesTab = page.locator('[data-view="lanes"]');
    const isolationTab = page.locator('[data-view="isolation"]');
    if (await prismTab.count() !== 1 || await lanesTab.count() !== 1 || await isolationTab.count() !== 1) {
      throw new Error(`${route.lang}: missing one or more Case Prism tabs`);
    }

    await prismTab.click();
    await page.waitForSelector('.pdim-prism-table tbody tr');
    const matrixRows = await page.locator('.pdim-prism-table tbody tr').count();
    const matrixCells = await page.locator('.pdim-prism-cell').count();
    if (matrixRows < 8 || matrixCells < 12) throw new Error(`${route.lang}: Case Prism matrix too small (${matrixRows} rows, ${matrixCells} cells)`);

    const audience = page.locator('[data-prism-audience]');
    if (await audience.count() !== 1) throw new Error(`${route.lang}: reader lens missing`);
    await audience.selectOption('fiscal');
    if (await audience.inputValue() !== 'fiscal') throw new Error(`${route.lang}: reader lens did not update`);

    const firstCell = page.locator('.pdim-prism-cell').first();
    await firstCell.click();
    await page.waitForSelector('[data-prism-detail] .pdim-prism-detail-head');
    const detailText = await page.locator('[data-prism-detail]').innerText();
    if (!detailText.trim()) throw new Error(`${route.lang}: Case Prism detail is empty`);

    await lanesTab.click();
    await page.waitForSelector('.pdim-lane-timeline .pdim-lane-event');
    const laneEvents = await page.locator('.pdim-lane-timeline .pdim-lane-event').count();
    if (laneEvents < 8) throw new Error(`${route.lang}: parallel lanes missing events`);

    await isolationTab.click();
    await page.waitForSelector('.pdim-isolation-grid');
    const laneSelect = page.locator('[data-isolation-lane]');
    if (await laneSelect.count() !== 1) throw new Error(`${route.lang}: isolation lane selector missing`);
    await laneSelect.selectOption('calificacion');
    if (await laneSelect.inputValue() !== 'calificacion') throw new Error(`${route.lang}: isolation lane did not update`);
    const isolationSections = await page.locator('.pdim-isolation-grid > section').count();
    if (isolationSections !== 2) throw new Error(`${route.lang}: isolation view must expose two comparison columns`);

    const bodyText = await page.locator('[data-view-body]').innerText();
    if (!bodyText.includes('RPL 2523/2025')) throw new Error(`${route.lang}: isolation view lost the selected appellate identity`);

    await page.close();
    console.log(`${route.lang}: Case Prism / lanes / isolation smoke PASS`);
  }
} finally {
  await browser.close();
}

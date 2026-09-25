import { chromium } from 'playwright';

const base = (process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho').replace(/\/$/, '');
const cases = [
  { lang: 'es', route: '/es/concurso-36-2012-separacion-administrador-concursal-rpl-3304-2025/' },
  { lang: 'en', route: '/en/insolvency-36-2012-administrator-removal-rpl-3304-2025/' },
];
const viewports = [
  { name: 'desktop', width: 1440, height: 1000 },
  { name: 'mobile', width: 390, height: 844 },
];

const browser = await chromium.launch({ headless: true });
try {
  for (const item of cases) {
    for (const viewport of viewports) {
      const page = await browser.newPage({ viewport });
      await page.goto(`${base}${item.route}`, { waitUntil: 'networkidle' });
      const h1 = page.locator('h1');
      if (!(await h1.isVisible())) throw new Error(`${item.lang}/${viewport.name}: h1 not visible`);
      if ((await page.locator('.state-map .lane').count()) !== 2) throw new Error(`${item.lang}/${viewport.name}: expected 2 appellant lanes`);
      if ((await page.locator('.state-map .master').count()) !== 1 || !(await page.locator('.state-map .master').isVisible())) throw new Error(`${item.lang}/${viewport.name}: consolidated master panel missing or hidden`);
      if ((await page.locator('.demand-overview .metric').count()) !== 6) throw new Error(`${item.lang}/${viewport.name}: expected 6 visual metric cards`);
      if ((await page.locator('.reliefs .relief').count()) !== 6) throw new Error(`${item.lang}/${viewport.name}: expected 6 relief cards`);
      if ((await page.locator('.grounds .ground').count()) !== 7) throw new Error(`${item.lang}/${viewport.name}: expected 7 detailed ground cards`);
      if ((await page.locator('.link-grid .link-card').count()) !== 6) throw new Error(`${item.lang}/${viewport.name}: expected 6 interlink groups`);
      const bodyMetrics = await page.evaluate(() => ({ scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth }));
      if (bodyMetrics.scrollWidth > bodyMetrics.clientWidth + 2) throw new Error(`${item.lang}/${viewport.name}: horizontal overflow ${bodyMetrics.scrollWidth} > ${bodyMetrics.clientWidth}`);
      const text = await page.locator('body').innerText();
      if (!text.includes('RPL 3304/2025') || !text.includes('RPL 3319/2025') || !text.includes('222/2026')) throw new Error(`${item.lang}/${viewport.name}: critical procedural markers missing`);
      await page.close();
    }
  }
  console.log('BORJA SEPARATION RENDER SMOKE: PASS — ES/EN desktop+mobile, 2 appellant lanes, 6 metrics, 6 relief cards, 7 detailed grounds, 6 interlink groups, no horizontal overflow');
} finally {
  await browser.close();
}

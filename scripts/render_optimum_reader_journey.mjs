import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';

const baseURL = process.env.PSR_BASE_URL || 'http://127.0.0.1:8000';
const outputDir = process.env.PSR_SCREENSHOT_DIR || 'artifacts/optimum-reader-journey';

const routes = [
  { name: 'home-es', route: '/es/', home: true, hero: '.hero', screenshot: true },
  { name: 'ricpe-es', route: '/es/ric-private-equity-sun-park/', hero: '.dossier-hero', screenshot: true },
  { name: 'cnmv-es', route: '/es/cnmv-ricpe-verificacion/', hero: '.cnmv-hero', screenshot: true },
  { name: 'incentives-es', route: '/es/incentivos-regionales-gc836-p06/', hero: '.ir-hero', screenshot: true },
  { name: 'snca-es', route: '/es/snca-fondos-europeos-trazabilidad/', hero: '.eu-hero', screenshot: true },
  { name: 'community-es', route: '/es/comunidad-instrumentalizacion/', hero: '.dossier-hero' },
  { name: 'takeover-es', route: '/es/toma-control-sun-park-7-junio-2018/', hero: '.dossier-hero' },
  { name: 'funding-es', route: '/es/mismo-hotel-multiples-vidas-financieras/', hero: '.hero' },
  { name: 'cnmv-en', route: '/en/cnmv-ricpe-verification/', hero: '.cnmv-hero' },
];

const viewports = [
  { name: 'mobile', width: 390, height: 844 },
  { name: 'desktop', width: 1440, height: 1000 },
];

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

await fs.mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const results = [];

try {
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height }, locale: 'es-ES' });
    for (const item of routes) {
      const page = await context.newPage();
      const url = `${baseURL}${item.route}`;
      await page.goto(url, { waitUntil: 'networkidle', timeout: 60_000 });
      await page.waitForTimeout(6_000);

      const state = await page.evaluate(({ heroSelector, home }) => {
        const visible = (node) => {
          if (!node) return false;
          const style = getComputedStyle(node);
          return style.display !== 'none' && style.visibility !== 'hidden' && node.getBoundingClientRect().height > 0;
        };
        const main = document.querySelector('main');
        const firstVisible = main ? [...main.children].find(visible) : null;
        const ids = [...document.querySelectorAll('[id]')].map((node) => node.id);
        const duplicates = ids.filter((id, index) => ids.indexOf(id) !== index);
        const railCurrent = document.querySelectorAll('#psr-unitary-journey [aria-current="step"]').length;
        return {
          title: document.title,
          firstVisibleClass: firstVisible?.className || '',
          firstVisibleTag: firstVisible?.tagName || '',
          heroVisible: visible(document.querySelector(heroSelector)),
          hasIntent: Boolean(document.querySelector('#psr-reader-intent')),
          hasDepth: Boolean(document.querySelector('#psr-depth-switcher')),
          hasNext: Boolean(document.querySelector('#psr-next-step')),
          hasProgress: Boolean(document.querySelector('#psr-reading-progress')),
          duplicateIds: [...new Set(duplicates)],
          railCurrent,
          overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
          home,
        };
      }, { heroSelector: item.hero, home: Boolean(item.home) });

      assert(state.heroVisible, `${item.name}/${viewport.name}: recipient hero is not visible`);
      assert(state.hasProgress, `${item.name}/${viewport.name}: reading progress control missing`);
      assert(state.duplicateIds.length === 0, `${item.name}/${viewport.name}: duplicate IDs: ${state.duplicateIds.join(', ')}`);
      assert(state.railCurrent <= 1, `${item.name}/${viewport.name}: more than one current journey step`);
      assert(state.overflow <= 2, `${item.name}/${viewport.name}: horizontal overflow ${state.overflow}px`);
      if (item.home) {
        assert(state.hasIntent, `${item.name}/${viewport.name}: unified reader-intent selector missing`);
      } else {
        assert(state.hasDepth, `${item.name}/${viewport.name}: reading-depth selector missing`);
        assert(state.hasNext, `${item.name}/${viewport.name}: next-step panel missing`);
      }

      if (item.screenshot) {
        const topPath = path.join(outputDir, `${item.name}-${viewport.name}-top.png`);
        await page.screenshot({ path: topPath, fullPage: false });
        if (!item.home) {
          const next = page.locator('#psr-next-step');
          await next.scrollIntoViewIfNeeded();
          await page.waitForTimeout(350);
          const bottomPath = path.join(outputDir, `${item.name}-${viewport.name}-next.png`);
          await page.screenshot({ path: bottomPath, fullPage: false });
        }
      }

      results.push({ route: item.route, viewport: viewport.name, ...state });
      await page.close();
    }
    await context.close();
  }
} finally {
  await browser.close();
}

await fs.writeFile(path.join(outputDir, 'results.json'), JSON.stringify(results, null, 2));
console.log(`OPTIMUM READER JOURNEY RENDER TEST PASSED: ${results.length} route/viewport combinations`);

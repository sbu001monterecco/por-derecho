import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';

const baseURL = process.env.PSR_BASE_URL || 'http://127.0.0.1:8000';
const outputDir = process.env.PSR_SCREENSHOT_DIR || 'artifacts/optimum-reader-journey';

const routes = [
  {
    name: 'home-es',
    route: '/es/',
    home: true,
    hero: '.hero',
    screenshot: true,
    accountabilityHref: '#institutional-accountability-12aug',
    accountabilityLabel: 'AC y Juez',
  },
  {
    name: 'home-en',
    route: '/en/',
    home: true,
    hero: '.hero',
    screenshot: true,
    accountabilityHref: '#institutional-accountability-12aug-en',
    accountabilityLabel: 'AC & Judge',
  },
  { name: 'ricpe-es', route: '/es/ric-private-equity-sun-park/', hero: '.dossier-hero', screenshot: true },
  { name: 'cnmv-es', route: '/es/cnmv-ricpe-verificacion/', hero: '.cnmv-hero', screenshot: true },
  { name: 'incentives-es', route: '/es/incentivos-regionales-gc836-p06/', hero: '.ir-hero', screenshot: true },
  { name: 'snca-es', route: '/es/snca-fondos-europeos-trazabilidad/', hero: '.eu-hero', screenshot: true },
  { name: 'community-es', route: '/es/comunidad-instrumentalizacion/', hero: '.dossier-hero', screenshot: true },
  { name: 'takeover-es', route: '/es/toma-control-sun-park-7-junio-2018/', hero: '.dossier-hero', screenshot: true },
  { name: 'funding-es', route: '/es/mismo-hotel-multiples-vidas-financieras/', hero: '.hero', screenshot: true },
  { name: 'cnmv-en', route: '/en/cnmv-ricpe-verification/', hero: '.cnmv-hero', screenshot: true },
];

const viewports = [
  { name: 'mobile', width: 390, height: 844 },
  { name: 'tablet', width: 900, height: 1280 },
  { name: 'desktop', width: 1440, height: 1000 },
];

await fs.mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const results = [];
const errors = [];

try {
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height }, locale: 'es-ES' });
    for (const item of routes) {
      const page = await context.newPage();
      const url = `${baseURL}${item.route}`;
      await page.goto(url, { waitUntil: 'networkidle', timeout: 60_000 });
      await page.waitForTimeout(8_000);

      const state = await page.evaluate(({ heroSelector, home, viewportWidth }) => {
        const visible = (node) => {
          if (!node) return false;
          const style = getComputedStyle(node);
          return style.display !== 'none' && style.visibility !== 'hidden' && node.getBoundingClientRect().height > 0;
        };
        const main = document.querySelector('main');
        const hero = document.querySelector(heroSelector);
        const firstVisible = main ? [...main.children].find(visible) : null;
        const ids = [...document.querySelectorAll('[id]')].map((node) => node.id);
        const duplicates = ids.filter((id, index) => ids.indexOf(id) !== index);
        const railCurrent = document.querySelectorAll('#psr-unitary-journey [aria-current="step"]').length;
        const accountability = document.querySelector('.site-header .nav-accountability');
        const overflowing = [...document.querySelectorAll('body *')]
          .map((node) => {
            const rect = node.getBoundingClientRect();
            return { node, rect };
          })
          .filter(({ node, rect }) => visible(node) && (rect.right > viewportWidth + 2 || rect.left < -2))
          .slice(0, 20)
          .map(({ node, rect }) => ({
            tag: node.tagName,
            id: node.id,
            className: String(node.className || '').slice(0, 160),
            left: Math.round(rect.left),
            right: Math.round(rect.right),
            width: Math.round(rect.width),
          }));
        return {
          title: document.title,
          firstVisibleClass: firstVisible?.className || '',
          firstVisibleTag: firstVisible?.tagName || '',
          heroVisible: visible(hero),
          heroFirst: firstVisible === hero,
          hasIntent: Boolean(document.querySelector('#psr-reader-intent')),
          hasDepth: Boolean(document.querySelector('#psr-depth-switcher')),
          hasNext: Boolean(document.querySelector('#psr-next-step')),
          hasProgress: Boolean(document.querySelector('#psr-reading-progress')),
          hasMobileMenu: Boolean(document.querySelector('.site-header .nav-toggle')),
          accountabilityHref: accountability?.getAttribute('href') || '',
          accountabilityLabel: accountability?.textContent?.trim() || '',
          duplicateIds: [...new Set(duplicates)],
          railCurrent,
          overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
          overflowing,
          home,
        };
      }, { heroSelector: item.hero, home: Boolean(item.home), viewportWidth: viewport.width });

      if (item.home && viewport.width <= 1120) {
        const toggle = page.locator('.site-header .nav-toggle');
        if (await toggle.count()) {
          await toggle.click();
          await page.waitForTimeout(100);
          state.compactMenu = await page.evaluate(() => {
            const nav = document.querySelector('.site-header .main-nav');
            const accountability = nav?.querySelector('.nav-accountability');
            return {
              expanded: document.querySelector('.site-header .nav-toggle')?.getAttribute('aria-expanded') === 'true',
              open: Boolean(nav?.classList.contains('open')),
              accountabilityVisible: Boolean(accountability && accountability.getBoundingClientRect().height > 0),
            };
          });
          await toggle.click();
        }
      }

      if (item.screenshot) {
        const topPath = path.join(outputDir, `${item.name}-${viewport.name}-top.png`);
        await page.screenshot({ path: topPath, fullPage: false });
        if (item.home) {
          const intent = page.locator('#psr-reader-intent');
          if (await intent.count()) {
            await intent.scrollIntoViewIfNeeded();
            await page.waitForTimeout(350);
            await page.screenshot({ path: path.join(outputDir, `${item.name}-${viewport.name}-intent.png`), fullPage: false });
          }
        } else {
          const next = page.locator('#psr-next-step');
          if (await next.count()) {
            await next.scrollIntoViewIfNeeded();
            await page.waitForTimeout(350);
            const bottomPath = path.join(outputDir, `${item.name}-${viewport.name}-next.png`);
            await page.screenshot({ path: bottomPath, fullPage: false });
          }
        }
      }

      const prefix = `${item.name}/${viewport.name}`;
      if (!state.heroVisible) errors.push(`${prefix}: recipient hero is not visible`);
      if (!state.heroFirst) errors.push(`${prefix}: recipient hero is not the first visible main module (${state.firstVisibleClass})`);
      if (!state.hasProgress) errors.push(`${prefix}: reading progress control missing`);
      if (state.duplicateIds.length) errors.push(`${prefix}: duplicate IDs: ${state.duplicateIds.join(', ')}`);
      if (state.railCurrent > 1) errors.push(`${prefix}: more than one current journey step`);
      if (state.overflow > 2) errors.push(`${prefix}: horizontal overflow ${state.overflow}px; ${JSON.stringify(state.overflowing)}`);
      if (viewport.width <= 1120 && !state.hasMobileMenu) errors.push(`${prefix}: accessible compact menu toggle missing`);
      if (item.home) {
        if (!state.hasIntent) errors.push(`${prefix}: unified reader-intent selector missing`);
        if (state.accountabilityHref !== item.accountabilityHref) {
          errors.push(`${prefix}: accountability navigation target missing or changed (${state.accountabilityHref})`);
        }
        if (state.accountabilityLabel !== item.accountabilityLabel) {
          errors.push(`${prefix}: accountability navigation label missing or changed (${state.accountabilityLabel})`);
        }
        if (viewport.width <= 1120 && (!state.compactMenu?.expanded || !state.compactMenu?.open || !state.compactMenu?.accountabilityVisible)) {
          errors.push(`${prefix}: accountability route is not visible in the opened compact menu`);
        }
      } else {
        if (!state.hasDepth) errors.push(`${prefix}: reading-depth selector missing`);
        if (!state.hasNext) errors.push(`${prefix}: next-step panel missing`);
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
await fs.writeFile(path.join(outputDir, 'errors.json'), JSON.stringify(errors, null, 2));
if (errors.length) {
  throw new Error(`OPTIMUM READER JOURNEY RENDER TEST FAILED (${errors.length})\n- ${errors.join('\n- ')}`);
}
console.log(`OPTIMUM READER JOURNEY RENDER TEST PASSED: ${results.length} route/viewport combinations`);

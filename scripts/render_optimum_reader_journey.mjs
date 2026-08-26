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

const compactBreakpoint = 1120;
const accountabilityBackground = 'rgb(111, 36, 35)';
const accountabilityForeground = 'rgb(255, 255, 255)';

// Keep the complete route suite on the three representative profiles and run
// the bilingual homepage accountability regression on the wider device and
// breakpoint matrix. This keeps CI bounded while covering the failure surface.
const viewports = [
  { name: 'phone-modern', width: 390, height: 844, fullRouteSuite: true },
  { name: 'tablet-android-portrait', width: 900, height: 1280, fullRouteSuite: true },
  { name: 'desktop', width: 1440, height: 1000, fullRouteSuite: true },
  { name: 'phone-smallest', width: 320, height: 568 },
  { name: 'phone-android-small', width: 360, height: 800 },
  { name: 'phone-android-large', width: 412, height: 915 },
  { name: 'phone-landscape', width: 844, height: 390 },
  { name: 'tablet-standard-portrait', width: 768, height: 1024 },
  { name: 'tablet-landscape', width: 1024, height: 768 },
  { name: 'compact-boundary-minus-1', width: 1119, height: 800 },
  { name: 'compact-boundary', width: 1120, height: 800 },
  { name: 'desktop-boundary-plus-1', width: 1121, height: 800 },
  { name: 'laptop', width: 1366, height: 768 },
  { name: 'desktop-large', width: 1920, height: 1080 },
];

await fs.mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const results = [];
const errors = [];

try {
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height }, locale: 'es-ES' });
    const viewportRoutes = viewport.fullRouteSuite ? routes : routes.filter((item) => item.home);
    for (const item of viewportRoutes) {
      const page = await context.newPage();
      const url = `${baseURL}${item.route}`;
      await page.goto(url, { waitUntil: 'networkidle', timeout: 60_000 });

      const readState = () => page.evaluate(({ heroSelector, home, viewportWidth, viewportHeight }) => {
        const visible = (node) => {
          if (!node) return false;
          const style = getComputedStyle(node);
          const rect = node.getBoundingClientRect();
          return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0' && rect.width > 0 && rect.height > 0;
        };
        const main = document.querySelector('main');
        const hero = document.querySelector(heroSelector);
        const firstVisible = main ? [...main.children].find(visible) : null;
        const ids = [...document.querySelectorAll('[id]')].map((node) => node.id);
        const duplicates = ids.filter((id, index) => ids.indexOf(id) !== index);
        const railCurrent = document.querySelectorAll('#psr-unitary-journey [aria-current="step"]').length;
        const nav = document.querySelector('.site-header .main-nav');
        const toggle = document.querySelector('.site-header .nav-toggle');
        const accountabilityLinks = [...document.querySelectorAll('.site-header .main-nav .nav-accountability')];
        const accountability = accountabilityLinks[0] || null;
        const accountabilityRect = accountability?.getBoundingClientRect();
        const accountabilityStyle = accountability ? getComputedStyle(accountability) : null;
        const accountabilityHit = accountability && visible(accountability)
          ? document.elementFromPoint(
              accountabilityRect.left + accountabilityRect.width / 2,
              accountabilityRect.top + accountabilityRect.height / 2,
            )
          : null;
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
          hasMobileMenu: Boolean(toggle),
          toggleVisible: visible(toggle),
          toggleExpanded: toggle?.getAttribute('aria-expanded') || '',
          navOptimised: nav?.getAttribute('data-psr-optimised') || '',
          accountabilityCount: accountabilityLinks.length,
          accountabilityHref: accountability?.getAttribute('href') || '',
          accountabilityLabel: accountability?.textContent?.trim() || '',
          accountabilityVisible: visible(accountability),
          accountabilityBackground: accountabilityStyle?.backgroundColor || '',
          accountabilityForeground: accountabilityStyle?.color || '',
          accountabilityTargetExists: Boolean(accountability?.hash && document.querySelector(accountability.hash)),
          accountabilityTargetWidth: Math.round(accountabilityRect?.width || 0),
          accountabilityTargetHeight: Math.round(accountabilityRect?.height || 0),
          accountabilityWithinViewport: Boolean(
            accountabilityRect
            && accountabilityRect.left >= -2
            && accountabilityRect.right <= viewportWidth + 2
            && accountabilityRect.top >= -2
            && accountabilityRect.bottom <= viewportHeight + 2
          ),
          accountabilityTopmost: Boolean(
            accountability
            && accountabilityHit
            && (accountabilityHit === accountability || accountability.contains(accountabilityHit))
          ),
          duplicateIds: [...new Set(duplicates)],
          railCurrent,
          overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
          overflowing,
          home,
        };
      }, {
        heroSelector: item.hero,
        home: Boolean(item.home),
        viewportWidth: viewport.width,
        viewportHeight: viewport.height,
      });

      const beforeOptimiser = await readState();
      await page.waitForTimeout(8_500);
      const state = await readState();
      state.beforeOptimiser = beforeOptimiser;

      if (item.screenshot) {
        const topPath = path.join(outputDir, `${item.name}-${viewport.name}-top.png`);
        await page.screenshot({ path: topPath, fullPage: false });
      }

      if (item.home && viewport.width <= compactBreakpoint) {
        const toggle = page.locator('.site-header .nav-toggle');
        if (await toggle.count()) {
          await toggle.click();
          await page.waitForTimeout(100);
          state.compactMenu = await page.evaluate(() => {
            const nav = document.querySelector('.site-header .main-nav');
            const accountability = nav?.querySelector('.nav-accountability');
            const rect = accountability?.getBoundingClientRect();
            const style = accountability ? getComputedStyle(accountability) : null;
            const hit = accountability && rect
              ? document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2)
              : null;
            return {
              expanded: document.querySelector('.site-header .nav-toggle')?.getAttribute('aria-expanded') === 'true',
              open: Boolean(nav?.classList.contains('open')),
              accountabilityVisible: Boolean(accountability && rect && rect.width > 0 && rect.height > 0),
              accountabilityBackground: style?.backgroundColor || '',
              accountabilityForeground: style?.color || '',
              accountabilityTargetWidth: Math.round(rect?.width || 0),
              accountabilityTargetHeight: Math.round(rect?.height || 0),
              accountabilityWithinViewport: Boolean(
                rect
                && rect.left >= -2
                && rect.right <= innerWidth + 2
                && rect.top >= -2
                && rect.bottom <= innerHeight + 2
              ),
              accountabilityTopmost: Boolean(
                accountability
                && hit
                && (hit === accountability || accountability.contains(hit))
              ),
            };
          });
          await page.screenshot({
            path: path.join(outputDir, `${item.name}-${viewport.name}-menu-open.png`),
            fullPage: false,
          });
          await page.locator('.site-header .main-nav .nav-accountability').click();
          await page.waitForTimeout(100);
          state.accountabilityClickHash = await page.evaluate(() => location.hash);
        }
      } else if (item.home) {
        await page.locator('.site-header .main-nav .nav-accountability').click();
        await page.waitForTimeout(100);
        state.accountabilityClickHash = await page.evaluate(() => location.hash);
      }

      if (item.screenshot) {
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

      if (item.home) {
        await page.reload({ waitUntil: 'networkidle', timeout: 60_000 });
        state.reloadBeforeOptimiser = await readState();
        await page.waitForTimeout(8_500);
        await page.mouse.move(0, viewport.height - 1);
        state.reloadAfterOptimiser = await readState();

        if (viewport.width <= compactBreakpoint) {
          const toggle = page.locator('.site-header .nav-toggle');
          if (await toggle.count()) {
            await toggle.click();
            await page.waitForTimeout(100);
            state.reloadCompactMenu = await page.evaluate(() => {
              const nav = document.querySelector('.site-header .main-nav');
              const accountability = nav?.querySelector('.nav-accountability');
              const rect = accountability?.getBoundingClientRect();
              const hit = accountability && rect
                ? document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2)
                : null;
              return {
                expanded: document.querySelector('.site-header .nav-toggle')?.getAttribute('aria-expanded') === 'true',
                open: Boolean(nav?.classList.contains('open')),
                accountabilityVisible: Boolean(accountability && rect && rect.width > 0 && rect.height > 0),
                accountabilityTargetWidth: Math.round(rect?.width || 0),
                accountabilityTargetHeight: Math.round(rect?.height || 0),
                accountabilityWithinViewport: Boolean(
                  rect
                  && rect.left >= -2
                  && rect.right <= innerWidth + 2
                  && rect.top >= -2
                  && rect.bottom <= innerHeight + 2
                ),
                accountabilityTopmost: Boolean(
                  accountability
                  && hit
                  && (hit === accountability || accountability.contains(hit))
                ),
              };
            });
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
      if (viewport.width <= compactBreakpoint && !state.hasMobileMenu) errors.push(`${prefix}: accessible compact menu toggle missing`);
      if (item.home) {
        if (!state.hasIntent) errors.push(`${prefix}: unified reader-intent selector missing`);
        if (beforeOptimiser.navOptimised === '1') {
          errors.push(`${prefix}: static pre-optimiser state was not observed`);
        }
        if (state.navOptimised !== '1') {
          errors.push(`${prefix}: delayed navigation optimiser did not complete`);
        }

        for (const [phase, accountabilityState] of [
          ['before optimiser', beforeOptimiser],
          ['after optimiser', state],
          ['after reload', state.reloadAfterOptimiser],
        ]) {
          if (accountabilityState.accountabilityCount !== 1) {
            errors.push(`${prefix}/${phase}: expected exactly one accountability navigation link (${accountabilityState.accountabilityCount})`);
          }
          if (accountabilityState.accountabilityHref !== item.accountabilityHref) {
            errors.push(`${prefix}/${phase}: accountability navigation target missing or changed (${accountabilityState.accountabilityHref})`);
          }
          if (accountabilityState.accountabilityLabel !== item.accountabilityLabel) {
            errors.push(`${prefix}/${phase}: accountability navigation label missing or changed (${accountabilityState.accountabilityLabel})`);
          }
          if (!accountabilityState.accountabilityTargetExists) {
            errors.push(`${prefix}/${phase}: accountability destination fragment is missing`);
          }
          if (accountabilityState.accountabilityBackground !== accountabilityBackground) {
            errors.push(`${prefix}/${phase}: accountability button lost its burgundy background (${accountabilityState.accountabilityBackground})`);
          }
          if (accountabilityState.accountabilityForeground !== accountabilityForeground) {
            errors.push(`${prefix}/${phase}: accountability button lost its white foreground (${accountabilityState.accountabilityForeground})`);
          }
        }

        if (state.reloadAfterOptimiser.navOptimised !== '1') {
          errors.push(`${prefix}: delayed navigation optimiser did not complete after reload`);
        }
        if (state.accountabilityClickHash !== item.accountabilityHref) {
          errors.push(`${prefix}: accountability link did not reach its exact fragment (${state.accountabilityClickHash})`);
        }

        if (viewport.width <= compactBreakpoint) {
          for (const [phase, compactMenu] of [
            ['first load', state.compactMenu],
            ['reload', state.reloadCompactMenu],
          ]) {
            if (!compactMenu?.expanded || !compactMenu?.open || !compactMenu?.accountabilityVisible) {
              errors.push(`${prefix}/${phase}: accountability route is not visible in the opened compact menu`);
            }
            if (!compactMenu?.accountabilityWithinViewport) {
              errors.push(`${prefix}/${phase}: accountability route is clipped outside the opened compact menu`);
            }
            if (!compactMenu?.accountabilityTopmost) {
              errors.push(`${prefix}/${phase}: accountability route is covered and cannot receive a centre-point tap`);
            }
            if ((compactMenu?.accountabilityTargetWidth || 0) < 24 || (compactMenu?.accountabilityTargetHeight || 0) < 24) {
              errors.push(`${prefix}/${phase}: accountability touch target is below 24 CSS px (${compactMenu?.accountabilityTargetWidth}x${compactMenu?.accountabilityTargetHeight})`);
            }
          }
        } else {
          if (state.toggleVisible) errors.push(`${prefix}: compact menu toggle remains visible above the 1120px breakpoint`);
          if (!state.accountabilityVisible || !state.accountabilityWithinViewport) {
            errors.push(`${prefix}: accountability button is not fully visible on desktop`);
          }
          if (!state.accountabilityTopmost) {
            errors.push(`${prefix}: accountability button is covered and cannot receive a centre-point click`);
          }
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
console.log(`OPTIMUM READER JOURNEY RENDER TEST PASSED: ${results.length} route/viewport combinations across ${viewports.length} device profiles`);

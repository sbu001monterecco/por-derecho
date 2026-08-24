import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { chromium } from 'playwright';

const base = (process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho').replace(/\/$/, '');
const executablePath = process.env.PSR_BROWSER_PATH || undefined;
const outputDir = process.env.PSR_CALIFICACION_THESIS_ARTIFACT_DIR || 'artifacts/calificacion-criminal-misuse-thesis';

const routes = [
  { key: 'es-canonical', route: '/es/tesis-uso-criminal-procedimiento-calificacion/', variant: 'canonical', anchor: 'hero', pillars: 5, canonical: true },
  { key: 'en-canonical', route: '/en/insolvency-classification-criminal-misuse-thesis/', variant: 'canonical', anchor: 'hero', pillars: 5, canonical: true },
  { key: 'es-home', route: '/es/', variant: 'featured', anchor: 'controlling', persistent: true },
  { key: 'en-home', route: '/en/', variant: 'featured', anchor: 'controlling', persistent: true },
  { key: 'es-institutional', route: '/es/concurso-36-2012-responsabilidad-institucional/', variant: 'featured', anchor: 'hero', persistent: true },
  { key: 'en-institutional', route: '/en/insolvency-36-2012-institutional-accountability/', variant: 'featured', anchor: 'hero', persistent: true },
  { key: 'es-appeal', route: '/es/concurso-36-2012-ap-seccion-4/', variant: 'appeal', anchor: 'hero', appeal: true },
  { key: 'en-appeal', route: '/en/insolvency-36-2012-ap-section-4/', variant: 'appeal', anchor: 'hero', appeal: true },
  { key: 'es-acosta', route: '/es/acosta-matos-perimetro/', variant: 'compact', anchor: 'source-funds', acosta: true },
  { key: 'en-acosta', route: '/en/acosta-matos-perimeter/', variant: 'compact', anchor: 'source-funds', acosta: true },
  { key: 'es-ac', route: '/es/concurso-36-2012-administrador-concursal/', variant: 'compact', anchor: 'hero' },
  { key: 'en-ac', route: '/en/insolvency-36-2012-insolvency-administrator/', variant: 'compact', anchor: 'hero' },
  { key: 'es-independence', route: '/es/nota-independencia-judicial-estado-procesal-reserva-acciones/', variant: 'independence-note', anchor: 'hero' },
  { key: 'es-guided-calificacion', route: '/es/calificacion-concurso-36-2012-vidas-paralelas/', variant: 'featured', anchor: 'guided', pillars: 5 },
  { key: 'en-guided-calificacion', route: '/en/insolvency-classification-parallel-lives/', variant: 'featured', anchor: 'guided', pillars: 5 },
];

await fs.mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true, executablePath });
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
const results = [];

try {
  for (let start = 0; start < routes.length; start += 8) {
    const batch = routes.slice(start, start + 8);
    const pages = await Promise.all(batch.map(async item => {
      const page = await context.newPage();
      const pageErrors = [];
      page.on('pageerror', error => pageErrors.push(String(error)));
      const url = `${base}${item.route}`;
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {});
      return { item, page, pageErrors, url };
    }));

    await Promise.all(pages.map(({ page }) => page.waitForTimeout(38000)));

    for (const { item, page, pageErrors, url } of pages) {
      const metrics = await page.evaluate(spec => {
        const main = document.querySelector('main');
        const direct = Array.from(main?.children || []);
        const thesis = document.querySelector('[data-calificacion-misuse-thesis]');
        const hero = main?.querySelector(':scope > section:first-of-type');
        const controlling = main?.querySelector(':scope > .ac-dfa-update-section');
        const sourceFunds = main?.querySelector(':scope > .source-funds-notice-section--featured');
        const guided = main?.querySelector(':scope > #calificacion-reader-gateway');
        const anchor = spec.anchor === 'source-funds'
          ? sourceFunds
          : spec.anchor === 'guided'
            ? guided
            : spec.anchor === 'controlling'
              ? controlling
              : hero;
        const text = thesis?.textContent?.replace(/\s+/g, ' ').trim() || '';
        const style = thesis ? getComputedStyle(thesis) : null;
        const position = document.querySelector('[data-calificacion-position-objectives]');
        const positionStyle = position ? getComputedStyle(position) : null;
        const positionText = position?.textContent?.replace(/\s+/g, ' ').trim() || '';
        const rplStatus = document.querySelector('#estado-rpl-2523-2025, #rpl-2523-2025-status');
        return {
          count: document.querySelectorAll('[data-calificacion-misuse-thesis]').length,
          variant: thesis?.getAttribute('data-calificacion-misuse-thesis') || '',
          directChild: thesis?.parentElement === main,
          directIndex: direct.indexOf(thesis),
          anchorIndex: direct.indexOf(anchor),
          anchored: Boolean(anchor && anchor.nextElementSibling === thesis),
          visible: Boolean(thesis && thesis.getClientRects().length && style?.display !== 'none' && style?.visibility !== 'hidden'),
          inCollapsedRecord: Boolean(thesis?.closest('[data-audience-full-record]')),
          pillars: thesis?.querySelectorAll('.cm-thesis-pillar').length || 0,
          appealFirewall: /RPL 2523\/2025 (?:debe|must)/.test(text),
          positionCount: document.querySelectorAll('[data-calificacion-position-objectives]').length,
          positionVisible: Boolean(position && position.getClientRects().length && positionStyle?.display !== 'none' && positionStyle?.visibility !== 'hidden'),
          positionText,
          closureTests: document.querySelectorAll('.cm-closure-table tbody tr').length,
          rplStatusVisible: Boolean(rplStatus && rplStatus.getClientRects().length),
          loaderRevision: Array.from(document.scripts).find(script => script.src.includes('calificacion-criminal-misuse-thesis'))?.src || '',
          sourceFundsCount: document.querySelectorAll('[data-source-of-funds-notice="full"]').length,
          adjudicationCrosslinkCount: document.querySelectorAll('[data-adjudicacion-crosslink]').length,
          caseHubCount: document.querySelectorAll('[data-case-hub-strip]').length,
          persistentPin: main?.dataset.calificacionMisusePin || '',
        };
      }, item);

      const failures = [];
      if (metrics.count !== 1) failures.push(`thesis count=${metrics.count}`);
      if (metrics.variant !== item.variant) failures.push(`variant=${metrics.variant}`);
      if (!metrics.directChild) failures.push('thesis is not a direct main child');
      if (!metrics.anchored) failures.push(`anchor mismatch (${metrics.anchorIndex} -> ${metrics.directIndex})`);
      if (!metrics.visible) failures.push('thesis is not visible');
      if (metrics.inCollapsedRecord) failures.push('thesis is inside collapsed full record');
      if (!metrics.loaderRevision.includes('20260824d')) failures.push(`loader=${metrics.loaderRevision}`);
      if (item.pillars && metrics.pillars !== item.pillars) failures.push(`pillars=${metrics.pillars}`);
      if (metrics.positionCount !== 1) failures.push(`position/objectives count=${metrics.positionCount}`);
      if (!metrics.positionVisible) failures.push('position/objectives layer is not visible');
      if (!/(?:Our position|Nuestra posici[oó]n)/i.test(metrics.positionText)) failures.push('canonical position wording missing');
      if (item.canonical && metrics.closureTests !== 5) failures.push(`closure tests=${metrics.closureTests}`);
      if (item.canonical && !metrics.rplStatusVisible) failures.push('canonical RPL status card is not visible');
      if (item.appeal && !metrics.appealFirewall) failures.push('appeal firewall missing');
      if (item.persistent && metrics.persistentPin !== 'persistent-20260824d') failures.push(`persistent pin=${metrics.persistentPin}`);
      if (item.acosta && metrics.sourceFundsCount !== 1) failures.push(`source-funds modules=${metrics.sourceFundsCount}`);
      if (item.acosta && metrics.adjudicationCrosslinkCount !== 1) failures.push(`adjudication crosslinks=${metrics.adjudicationCrosslinkCount}`);
      if (item.acosta && metrics.caseHubCount !== 1) failures.push(`case hubs=${metrics.caseHubCount}`);
      const thesisErrors = pageErrors.filter(message => /calificacion|misuse|thesis/i.test(message));
      if (thesisErrors.length) failures.push(`page errors=${thesisErrors.join(' | ')}`);

      const passed = failures.length === 0;
      results.push({ key: item.key, url, passed, failures, pageErrors, ...metrics });
      await page.close();
    }
  }
} finally {
  await browser.close();
}

const passed = results.length === routes.length && results.every(result => result.passed);
await fs.writeFile(path.join(outputDir, 'result.json'), JSON.stringify({ base, status: passed ? 'PASS' : 'FAIL', checked: results.length, results }, null, 2), 'utf8');
if (!passed) {
  console.error(JSON.stringify({ status: 'FAIL', results: results.filter(result => !result.passed) }, null, 2));
  process.exit(1);
}
console.log(JSON.stringify({ status: 'PASS', checked: results.length, results }, null, 2));

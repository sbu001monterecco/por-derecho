import fs from 'node:fs/promises';
import path from 'node:path';

const playwright = await import(process.env.PSR_PLAYWRIGHT_PATH || 'playwright');
const { chromium } = playwright;

const baseURL = process.env.PSR_BASE_URL || 'http://127.0.0.1:8765';
const outputDir = process.env.PSR_SCREENSHOT_DIR || '/tmp/fti-meeting-point-ricpe-render';
const routes = [
  {language: 'es', route: '/es/fti-meeting-point-ricpe-alertador-continuidad/'},
  {language: 'en', route: '/en/fti-meeting-point-ricpe-whistleblower-continuity/'},
  {language: 'de', route: '/de/fti-meeting-point-ricpe-hinweisgeber-kontinuitaet/'},
];
const viewports = [
  {name: 'mobile', width: 390, height: 844},
  {name: 'desktop', width: 1440, height: 1000},
];

await fs.mkdir(outputDir, {recursive: true});
const browser = await chromium.launch({
  headless: true,
  executablePath: process.env.PSR_BROWSER_PATH || undefined,
});
const results = [];
const failures = [];

try {
  for (const viewport of viewports) {
    const context = await browser.newContext({viewport});
    for (const item of routes) {
      const page = await context.newPage();
      const consoleErrors = [];
      const pageErrors = [];
      const requestFailures = [];
      const httpErrors = [];
      page.on('console', (message) => {
        if (message.type() === 'error') consoleErrors.push(message.text());
      });
      page.on('pageerror', (error) => pageErrors.push(error.message));
      page.on('requestfailed', (request) => {
        requestFailures.push(`${request.method()} ${request.url()} — ${request.failure()?.errorText || 'failed'}`);
      });
      page.on('response', (response) => {
        const type = response.request().resourceType();
        if (response.status() >= 400 && ['document', 'script', 'stylesheet', 'fetch', 'xhr'].includes(type)) {
          httpErrors.push(`${response.status()} ${response.url()}`);
        }
      });
      await page.goto(`${baseURL}${item.route}`, {waitUntil: 'networkidle', timeout: 60_000});
      try {
        await page.waitForFunction(
          () => document.querySelectorAll('[data-fmr-watch] [data-watch-id]').length === 6
            || Boolean(document.querySelector('[data-fmr-watch] .fm-watch__error')),
          null,
          {timeout: 15_000},
        );
      } catch {
        failures.push(`${item.language}/${viewport.name}: monitor did not settle within 15 seconds`);
      }
      const metrics = await page.evaluate(({width, language}) => {
        const bodyText = document.body.textContent || '';
        const overflowCandidates = [...document.querySelectorAll('body *')]
          .map((element) => {
            const rect = element.getBoundingClientRect();
            const className = typeof element.className === 'string'
              ? element.className.trim().split(/\s+/).filter(Boolean).slice(0, 2).join('.')
              : '';
            const selector = element.id
              ? `${element.tagName.toLowerCase()}#${element.id}`
              : `${element.tagName.toLowerCase()}${className ? `.${className}` : ''}`;
            return {
              selector,
              left: Math.round(rect.left),
              right: Math.round(rect.right),
              width: Math.round(rect.width),
            };
          })
          .filter((item) => item.left < -2 || item.right > width + 2)
          .sort((a, b) => (b.right - width) - (a.right - width))
          .slice(0, 8);
        const actionMarkers = {
          es: '31 ACCIONES CONTROLADAS',
          en: '31 CONTROLLED ACTIONS',
          de: '31 KONTROLLIERTE MASSNAHMEN',
        };
        const channelId = language === 'es' ? 'ricpe' : language === 'en' ? 'ricpe' : 'kanal';
        const linkId = language === 'es' ? 'enlaces' : language === 'en' ? 'links' : 'verknuepfungen';
        return {
          control: document.body.dataset.fmrControl || '',
          language: document.body.dataset.fmrLanguage || '',
          causalNodes: document.querySelectorAll('[data-causal-node]').length,
          railItems: document.querySelectorAll('.rail > div').length,
          graphLink: Boolean(document.querySelector('a[href*="fti-meeting-point-ricpe-causal-evidence-v1.json"]')),
          caretLink: Boolean(document.querySelector('a[href*="caepr-caret-fti-meeting-point-ricpe-continuity-v1.json"]')),
          professionalCaretLink: Boolean(document.querySelector('a[href*="caepr-caret-fti-meeting-point-professional-institutional-v1.json"]')),
          actionLink: Boolean(document.querySelector('a[href*="FTI_MEETING_POINT_RICPE_CROSSBORDER_ACTION_REGISTER_27AUG2026.json"]')),
          derivedMonitorLink: Boolean(document.querySelector('a[href*="fti-meeting-point-canary-capital-control-watch-v1.json"]')),
          canonicalMonitorLink: Boolean(document.querySelector('a[href*="fti-meeting-point-canary-spain-asset-transaction-register-v1.json"]')),
          monitorRows: document.querySelectorAll('[data-fmr-watch] [data-watch-id]').length,
          monitorError: Boolean(document.querySelector('[data-fmr-watch] .fm-watch__error')),
          professionalCaretCounts: /40\s+(?:de|of|von)\s+101/i.test(bodyText) && /61\s+(?:pendientes|pending|offen)/i.test(bodyText),
          actionCount: bodyText.includes(actionMarkers[language]),
          channelCards: document.querySelectorAll(`#${channelId} .proof-grid .card`).length,
          multidirectionalLinks: document.querySelectorAll(`#${linkId} .link-grid a`).length,
          hold: bodyText.includes('HOLD'),
          documentScrollWidth: document.documentElement.scrollWidth,
          bodyScrollWidth: document.body.scrollWidth,
          horizontalOverflow: Math.max(
            document.documentElement.scrollWidth,
            document.body.scrollWidth,
          ) - width,
          overflowCandidates,
          deCnmvControlLink: language !== 'de' || Boolean(document.querySelector('#kanal a[href*="/en/cnmv-ricpe-verification/"]')),
          deRegageParity: language !== 'de' || [
            'REGAGE26e00003492334',
            'REGAGE26e00003609135',
            'REGAGE26e00003629560',
          ].every((marker) => bodyText.includes(marker)),
          deControlledHistoricTitle: language !== 'de' || bodyText.includes('el Ilmo. Sr. D. Alberto López Villarrubia^, Magistrado-Juez del entonces Juzgado de lo Mercantil n.º 1 de Las Palmas de Gran Canaria'),
          deJudicialBacklink: language !== 'de' || Boolean(document.querySelector('#richter a[href*="alberto-lopez-villarrubia-meeting-point-357-active-estate"]')),
          deEnglishRouteDisclosure: language !== 'de' || (
            document.querySelectorAll('#kette [data-causal-node][hreflang="en"]').length === 10
            && bodyText.includes('Kompatibilitätsroute')
            && bodyText.includes('kein eigenständiges deutsches Voll-Dossier')
          ),
          deLiteralDocketBackticks: language === 'de' && bodyText.includes('`1500 IN'),
        };
      }, {width: viewport.width, language: item.language});
      const prefix = `${item.language}/${viewport.name}`;
      if (metrics.control !== 'PD-FTI-MP-RICPE-CONTINUITY-20260827-01') failures.push(`${prefix}: control marker missing`);
      if (metrics.language !== item.language) failures.push(`${prefix}: language marker mismatch`);
      if (metrics.causalNodes !== 10) failures.push(`${prefix}: expected 10 causal nodes, got ${metrics.causalNodes}`);
      if (metrics.railItems !== 4) failures.push(`${prefix}: expected 4 status-rail items, got ${metrics.railItems}`);
      if (!metrics.graphLink || !metrics.caretLink || !metrics.professionalCaretLink || !metrics.actionLink) failures.push(`${prefix}: machine-control links incomplete`);
      if (!metrics.derivedMonitorLink || !metrics.canonicalMonitorLink) failures.push(`${prefix}: derived/canonical monitor links incomplete`);
      if (metrics.monitorRows !== 6 || metrics.monitorError) failures.push(`${prefix}: expected six error-free monitor rows, got ${metrics.monitorRows}`);
      if (!metrics.professionalCaretCounts) failures.push(`${prefix}: expanded 40/101 and 61-pending caret state missing`);
      if (!metrics.actionCount) failures.push(`${prefix}: 31-action marker missing`);
      if (metrics.channelCards !== 3) failures.push(`${prefix}: expected three channel evidence-state cards, got ${metrics.channelCards}`);
      if (metrics.multidirectionalLinks !== 6) failures.push(`${prefix}: expected six multidirectional links, got ${metrics.multidirectionalLinks}`);
      if (!metrics.hold) failures.push(`${prefix}: external-action hold missing`);
      if (metrics.horizontalOverflow > 2) {
        failures.push(
          `${prefix}: horizontal overflow ${metrics.horizontalOverflow}px; `
          + `candidates=${JSON.stringify(metrics.overflowCandidates)}`,
        );
      }
      if (!metrics.deCnmvControlLink) failures.push(`${prefix}: German CNMV control backlink missing`);
      if (!metrics.deRegageParity) failures.push(`${prefix}: German REGAGE identifiers/limitation parity missing`);
      if (!metrics.deControlledHistoricTitle) failures.push(`${prefix}: German page lacks exact controlled Spanish historic title`);
      if (!metrics.deJudicialBacklink) failures.push(`${prefix}: German Alberto cross-proceeding backlink missing`);
      if (!metrics.deEnglishRouteDisclosure) failures.push(`${prefix}: German English-route/compatibility disclosure incomplete`);
      if (metrics.deLiteralDocketBackticks) failures.push(`${prefix}: literal Markdown backticks remain around German dockets`);
      if (consoleErrors.length) failures.push(`${prefix}: console errors: ${consoleErrors.join(' | ')}`);
      if (pageErrors.length) failures.push(`${prefix}: page errors: ${pageErrors.join(' | ')}`);
      if (requestFailures.length) failures.push(`${prefix}: failed requests: ${requestFailures.join(' | ')}`);
      if (httpErrors.length) failures.push(`${prefix}: HTTP asset errors: ${httpErrors.join(' | ')}`);
      await page.screenshot({path: path.join(outputDir, `${item.language}-${viewport.name}.png`), fullPage: true});
      results.push({route: item.route, viewport: viewport.name, ...metrics, consoleErrors, pageErrors, requestFailures, httpErrors});
      await page.close();
    }
    await context.close();
  }
} finally {
  await browser.close();
}

await fs.writeFile(path.join(outputDir, 'results.json'), JSON.stringify({baseURL, results, failures}, null, 2));
if (failures.length) {
  console.error(failures.join('\n'));
  process.exit(1);
}
console.log(`FTI/MEETING POINT/RICPE RENDER: PASS (${results.length} route/viewport checks)`);
console.log(`Screenshots: ${outputDir}`);

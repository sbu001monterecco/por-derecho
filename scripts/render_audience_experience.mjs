import fs from 'node:fs/promises';
import path from 'node:path';

const playwright = await import(process.env.PSR_PLAYWRIGHT_PATH || 'playwright');
const { chromium } = playwright;

const baseURL = process.env.PSR_BASE_URL || 'http://127.0.0.1:8765';
const outputDir = process.env.PSR_SCREENSHOT_DIR || 'artifacts/audience-experience-20260823';
const routes = [
  { lang: 'es', route: '/es/', summary: '#resumen-60-segundos', perimeters: '#perimetros-del-caso', chronology: '#historia-reconstruida', directText: 'Gil Marer y Aweswell alegan una sola empresa continuada de criminalidad económica, desarrollada mediante adopción sucesiva y división de funciones.' },
  { lang: 'en', route: '/en/', summary: '#sixty-second-summary', perimeters: '#case-perimeters', chronology: '#reverse-engineered-story', directText: 'Gil Marer and Aweswell allege one continuing economic-criminal enterprise, advanced through successive adoption and divided functions.' },
];
const viewports = [
  { name: 'mobile', width: 390, height: 844 },
  { name: 'desktop', width: 1440, height: 1000 },
];

await fs.mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const results = [];
const failures = [];

try {
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport });
    for (const item of routes) {
      const page = await context.newPage();
      await page.goto(`${baseURL}${item.route}`, { waitUntil: 'networkidle', timeout: 60_000 });
      await page.waitForTimeout(7_000);

      const metrics = await page.evaluate(({ summary, perimeters, chronology, width, directText }) => {
        const main = document.querySelector('main');
        const directChildren = [...(main?.children || [])];
        const index = (selector) => directChildren.indexOf(document.querySelector(selector));
        const controllingNode = document.querySelector('.ac-dfa-update-section');
        const detailedNode = document.querySelector('section[data-pd-five-ac]');
        const prosecutionNode = document.querySelector('.prosecution-entry-20260821');
        const summaryNode = document.querySelector(summary);
        const audienceNode = document.querySelector('#psr-reader-intent');
        const perimeterNode = document.querySelector(perimeters);
        const chronologyNode = document.querySelector(chronology);
        const fullRecordNode = document.querySelector('[data-audience-full-record]');
        const fullRecordDetails = fullRecordNode?.querySelector('details');
        const prosecutionText = prosecutionNode?.textContent?.replace(/\s+/g, ' ').trim() || '';
        const controllingText = controllingNode?.textContent?.replace(/\s+/g, ' ').trim() || '';
        const detailedText = detailedNode?.textContent?.replace(/\s+/g, ' ').trim() || '';
        const institutionPortraits = [...(detailedNode?.querySelectorAll('.pd-five-ac__institution-portrait') || [])];
        return {
          order: [
            index('.ac-dfa-update-section'),
            index('section[data-pd-five-ac]'),
            index('[data-calificacion-misuse-thesis]'),
            index('.priority-band'),
            index('.prosecution-entry-20260821'),
            index(summary),
            index('#psr-reader-intent'),
            index(perimeters),
            index('[data-audience-full-record]'),
          ],
          summaryTop: Math.round(summaryNode?.getBoundingClientRect().top + scrollY || -1),
          audienceCards: audienceNode?.querySelectorAll('.psr-intent-card').length || 0,
          perimeterCards: perimeterNode?.querySelectorAll('.audience-perimeter-grid > a').length || 0,
          prosecutionPanels: document.querySelectorAll('.prosecution-entry-20260821').length,
          controllingPanels: document.querySelectorAll('.ac-dfa-update-section').length,
          fiveActorVisualPanels: document.querySelectorAll('section[data-pd-five-ac]').length,
          controllingMarker: controllingNode?.querySelector('[data-ac-dfa-update]')?.dataset.acDfaUpdate || '',
          controllingVisibleBeforeCollapse: Boolean(controllingNode && !fullRecordNode?.contains(controllingNode)),
          controllingFiveActorTextPresent: ['Francisco Mario Matos Matas','Antonio Cogolludo Rojas','Shaila María Cogolludo Ramos','José Daniel Acosta Matos','Laura Patricia Acosta Matos'].every(name => controllingText.includes(name)),
          controllingInstitutionalTextPresent: controllingText.includes('Alberto López Villarrubia') && (controllingText.includes('administrador concursal') || controllingText.includes('insolvency administrator')),
          fiveActorVisualMarker: detailedNode?.dataset.pdFiveAc || '',
          fiveActorFrontPageLock: detailedNode?.dataset.fiveActorFrontPageLock || '',
          keyDirectRoutePresentation: detailedNode?.dataset.keyDirectRoutePresentation || '',
          fiveActorProtectedMarker: detailedNode?.dataset.audienceProtectedFiveActorVisual || '',
          fiveActorVisualVisibleBeforeCollapse: Boolean(detailedNode && !fullRecordNode?.contains(detailedNode)),
          fiveActorCards: detailedNode?.querySelectorAll('[data-private-actor-card]').length || 0,
          institutionCards: detailedNode?.querySelectorAll('[data-institution-card]').length || 0,
          linkageRows: detailedNode?.querySelectorAll('[data-linkage-row]').length || 0,
          institutionPortraitsLoaded: institutionPortraits.length === 2 && institutionPortraits.every(image => image.complete && image.naturalWidth > 0),
          privatePortraitLoaded: Boolean(detailedNode?.querySelector('.pd-five-ac__portrait')?.complete && detailedNode?.querySelector('.pd-five-ac__portrait')?.naturalWidth > 0),
          detailedFiveActorTextPresent: ['Francisco Mario Matos Matas','Antonio Cogolludo Rojas','Shaila María Cogolludo Ramos','José Daniel Acosta Matos','Laura Patricia Acosta Matos'].every(name => detailedText.includes(name)),
          detailedInstitutionalTextPresent: detailedText.includes('Francisco de Borja Rodríguez-Batllori Laffitte') && detailedText.includes('Alberto López Villarrubia'),
          detailedActsOmissionsPresent: (detailedText.includes('comisiones') && detailedText.includes('omisiones')) || (detailedText.includes('commissions') && detailedText.includes('omissions')),
          expressAttributionMarker: prosecutionNode?.dataset.expressCriminalAttribution || '',
          protectedAttributionMarker: prosecutionNode?.dataset.audienceProtectedAttribution || '',
          attributionVisibleBeforeCollapse: Boolean(prosecutionNode && !fullRecordNode?.contains(prosecutionNode)),
          directAttributionTextPresent: prosecutionText.includes(directText),
          proofBoundaryPresent: prosecutionText.includes('Relationship is not responsibility') || prosecutionText.includes('Relación no es responsabilidad'),
          nonFindingBoundaryPresent: prosecutionText.includes('not a judicial finding') || prosecutionText.includes('no es una declaración judicial'),
          contraryRecordPresent: prosecutionText.includes('provisional dismissal') || prosecutionText.includes('archivo provisional'),
          identityVariantPresent: document.body.textContent.includes('Laura Isabel'),
          audienceOrderMarker: main?.dataset.audienceOrder || '',
          mainAttributionMarker: main?.dataset.expressCriminalAttributionVisible || '',
          mainControllingMarker: main?.dataset.fiveActorControllingAllegationVisible || '',
          mainFiveActorVisualMarker: main?.dataset.fiveActorVisualVisible || '',
          chronologyInFullRecord: Boolean(chronologyNode && fullRecordNode?.contains(chronologyNode)),
          fullRecordClosed: Boolean(fullRecordDetails && !fullRecordDetails.open),
          horizontalOverflow: document.documentElement.scrollWidth - width,
          summaryHeading: summaryNode?.querySelector('h2')?.textContent?.trim() || '',
          chronologyHeading: chronologyNode?.querySelector('h2')?.textContent?.trim() || '',
        };
      }, { summary: item.summary, perimeters: item.perimeters, chronology: item.chronology, width: viewport.width, directText: item.directText });

      const prefix = `${item.lang}/${viewport.name}`;
      if (metrics.order.some((value) => value < 0) || metrics.order.some((value, i, values) => i && value !== values[i - 1] + 1)) failures.push(`${prefix}: protected first-read sections are not consecutive: ${metrics.order.join(',')}`);
      if (metrics.audienceCards !== 4) failures.push(`${prefix}: expected 4 audience cards, got ${metrics.audienceCards}`);
      if (metrics.perimeterCards !== 5) failures.push(`${prefix}: expected 5 perimeter cards, got ${metrics.perimeterCards}`);
      if (metrics.prosecutionPanels !== 1) failures.push(`${prefix}: expected 1 prosecution panel, got ${metrics.prosecutionPanels}`);
      if (metrics.controllingPanels !== 1) failures.push(`${prefix}: expected 1 controlling five-actor panel, got ${metrics.controllingPanels}`);
      if (metrics.controllingMarker !== '20260824') failures.push(`${prefix}: controlling five-actor marker missing`);
      if (!metrics.controllingVisibleBeforeCollapse) failures.push(`${prefix}: controlling five-actor allegation is hidden in collapsed full record`);
      if (!metrics.controllingFiveActorTextPresent) failures.push(`${prefix}: controlling panel does not name all five private actors`);
      if (!metrics.controllingInstitutionalTextPresent) failures.push(`${prefix}: controlling panel omits the AC or Judge allegation`);
      if (metrics.fiveActorVisualPanels !== 1) failures.push(`${prefix}: expected 1 detailed five-actor visual, got ${metrics.fiveActorVisualPanels}`);
      if (metrics.fiveActorVisualMarker !== '20260824b') failures.push(`${prefix}: detailed five-actor visual marker missing`);
      if (metrics.fiveActorFrontPageLock !== 'express-authorization-required') failures.push(`${prefix}: express-authorization front-page preservation lock missing`);
      if (metrics.keyDirectRoutePresentation !== 'front-page') failures.push(`${prefix}: front-page presentation marker missing`);
      if (metrics.fiveActorProtectedMarker !== '20260824b') failures.push(`${prefix}: detailed five-actor visual is not protected by audience ordering`);
      if (!metrics.fiveActorVisualVisibleBeforeCollapse) failures.push(`${prefix}: detailed five-actor visual is hidden in collapsed full record`);
      if (metrics.fiveActorCards !== 5) failures.push(`${prefix}: expected 5 private actor cards, got ${metrics.fiveActorCards}`);
      if (metrics.institutionCards !== 2) failures.push(`${prefix}: expected Administrator and Judge cards, got ${metrics.institutionCards}`);
      if (metrics.linkageRows !== 5) failures.push(`${prefix}: expected 5 actor-specific linkage rows, got ${metrics.linkageRows}`);
      if (!metrics.institutionPortraitsLoaded) failures.push(`${prefix}: Administrator or Judge portrait did not load`);
      if (!metrics.privatePortraitLoaded) failures.push(`${prefix}: canonical FMMM portrait did not load`);
      if (!metrics.detailedFiveActorTextPresent) failures.push(`${prefix}: detailed visual does not name all five private actors`);
      if (!metrics.detailedInstitutionalTextPresent) failures.push(`${prefix}: detailed visual omits the Administrator or Judge identity`);
      if (!metrics.detailedActsOmissionsPresent) failures.push(`${prefix}: detailed visual omits commissions/omissions linkage`);
      if (metrics.expressAttributionMarker !== '20260824') failures.push(`${prefix}: express criminal-attribution marker missing`);
      if (metrics.protectedAttributionMarker !== '20260824') failures.push(`${prefix}: attribution is not protected by audience ordering`);
      if (!metrics.attributionVisibleBeforeCollapse) failures.push(`${prefix}: direct attribution is hidden in collapsed full record`);
      if (!metrics.directAttributionTextPresent) failures.push(`${prefix}: direct actor-specific criminal attribution text was diluted or removed`);
      if (!metrics.proofBoundaryPresent) failures.push(`${prefix}: actor-specific proof boundary missing`);
      if (!metrics.nonFindingBoundaryPresent) failures.push(`${prefix}: allegation/not-finding boundary missing`);
      if (!metrics.contraryRecordPresent) failures.push(`${prefix}: strongest contrary procedural record missing from first read`);
      if (metrics.identityVariantPresent) failures.push(`${prefix}: erroneous public identity variant rendered`);
      if (metrics.audienceOrderMarker !== '20260824') failures.push(`${prefix}: runtime order marker missing`);
      if (metrics.mainAttributionMarker !== '20260824') failures.push(`${prefix}: main attribution visibility marker missing`);
      if (metrics.mainControllingMarker !== '20260824') failures.push(`${prefix}: main controlling-allegation visibility marker missing`);
      if (metrics.mainFiveActorVisualMarker !== '20260824b') failures.push(`${prefix}: main detailed five-actor visibility marker missing`);
      if (!metrics.chronologyInFullRecord) failures.push(`${prefix}: chronology was not moved into progressive disclosure`);
      if (!metrics.fullRecordClosed) failures.push(`${prefix}: full record is not collapsed on first load`);
      if (metrics.horizontalOverflow > 2) failures.push(`${prefix}: horizontal overflow ${metrics.horizontalOverflow}px`);

      await page.screenshot({ path: path.join(outputDir, `${item.lang}-${viewport.name}-top.png`), fullPage: false });
      await page.locator('section[data-pd-five-ac]').scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);
      await page.screenshot({ path: path.join(outputDir, `${item.lang}-${viewport.name}-five-actors-ac-judge.png`), fullPage: false });
      await page.locator('.prosecution-entry-20260821').scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);
      await page.screenshot({ path: path.join(outputDir, `${item.lang}-${viewport.name}-criminal-attribution.png`), fullPage: false });
      await page.locator('#psr-reader-intent').scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);
      await page.screenshot({ path: path.join(outputDir, `${item.lang}-${viewport.name}-audiences.png`), fullPage: false });
      await page.locator(item.perimeters).scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);
      await page.screenshot({ path: path.join(outputDir, `${item.lang}-${viewport.name}-perimeters.png`), fullPage: false });

      results.push({ route: item.route, viewport: viewport.name, ...metrics });
      await page.close();
    }
    await context.close();
  }
} finally {
  await browser.close();
}

await fs.writeFile(path.join(outputDir, 'results.json'), JSON.stringify({ baseURL, results, failures }, null, 2));
if (failures.length) {
  console.error(failures.join('\n'));
  process.exit(1);
}
console.log(`AUDIENCE RENDER VALIDATION PASSED — ${results.length} bilingual viewport checks; direct attribution visible before progressive disclosure; screenshots in ${outputDir}`);

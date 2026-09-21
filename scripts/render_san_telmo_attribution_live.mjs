#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const base = (process.env.PSR_BASE_URL || 'https://sbu001monterecco.github.io/por-derecho').replace(/\/$/, '');
const browserPath = process.env.PSR_BROWSER_PATH;
const artifactDir = process.env.PSR_SAN_TELMO_ARTIFACT_DIR || 'artifacts/san-telmo-attribution-live';

if (!browserPath) {
  throw new Error('PSR_BROWSER_PATH is required');
}

fs.mkdirSync(artifactDir, { recursive: true });

const routes = [
  {
    language: 'en',
    route: '/en/',
    required: [
      'Speaker correction.',
      'Eduardo Sánchez',
      '08:08–08:12',
      'The programme title identifies Enrique Guerra as the guest',
      'Read the complete source-led dossier',
    ],
    forbidden: [
      'RIC director Enrique Guerra said that the firm placed clients into its first investment',
      'Eduardo Sánchez appears as interviewer and visible recipient of those statements',
    ],
    dossierPath: '/por-derecho/en/san-telmo-ricpe-sun-park/',
  },
  {
    language: 'es',
    route: '/es/',
    required: [
      'Corrección de atribución.',
      'Eduardo Sánchez',
      '08:08–08:12',
      'El título del programa identifica a Enrique Guerra como invitado',
      'Leer el expediente documental completo',
    ],
    forbidden: [
      'Eduardo Sánchez figura como entrevistador y receptor visible de esas manifestaciones',
    ],
    dossierPath: '/por-derecho/es/san-telmo-ricpe-sun-park/',
  },
];

const browser = await chromium.launch({
  executablePath: browserPath,
  headless: true,
  args: ['--no-sandbox', '--disable-dev-shm-usage'],
});

const results = [];
let failed = false;

try {
  for (const target of routes) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
    const url = `${base}${target.route}?pd_dom_verify=${Date.now()}`;
    const entry = {
      language: target.language,
      url,
      status: null,
      correctionApplied: false,
      required: {},
      forbidden: {},
      dossierHref: null,
      sourceHref: null,
      screenshot: null,
      error: null,
    };

    try {
      const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45_000 });
      entry.status = response?.status() ?? null;

      const selector = 'section.interview-evidence[data-pd-san-telmo-attribution="20260819"]';
      await page.waitForSelector(selector, { state: 'visible', timeout: 30_000 });
      entry.correctionApplied = true;

      const rendered = await page.locator(selector).evaluate((section) => {
        const dossierLink = section.querySelector('a.button.secondary');
        const sourceLink = section.querySelector('blockquote cite a');
        return {
          text: section.innerText,
          dossierHref: dossierLink?.href || null,
          sourceHref: sourceLink?.href || null,
          marker: section.getAttribute('data-pd-san-telmo-attribution'),
          protectedMarker: section.getAttribute('data-audience-protected-san-telmo'),
          outsideCollapsedRecord: !section.closest('[data-audience-full-record]'),
          directChildOfMain: section.parentElement === document.querySelector('main'),
        };
      });

      entry.dossierHref = rendered.dossierHref;
      entry.sourceHref = rendered.sourceHref;
      entry.marker = rendered.marker;
      entry.protectedMarker = rendered.protectedMarker;

      for (const marker of target.required) {
        entry.required[marker] = rendered.text.includes(marker);
      }
      for (const marker of target.forbidden) {
        entry.forbidden[marker] = rendered.text.includes(marker);
      }

      const dossierUrl = new URL(rendered.dossierHref || '', base);
      const dossierMatches = dossierUrl.pathname === target.dossierPath;
      const sourceMatches = Boolean(rendered.sourceHref?.includes('mHn9IJU0qI4') && rendered.sourceHref?.includes('t=488s'));
      const requiredPass = Object.values(entry.required).every(Boolean);
      const forbiddenPass = Object.values(entry.forbidden).every((present) => present === false);
      const statusPass = entry.status === 200;
      const markerPass = rendered.marker === '20260819';
      const visiblePlacementPass = rendered.protectedMarker === '20260823'
        && rendered.outsideCollapsedRecord
        && rendered.directChildOfMain;

      entry.checks = {
        http200: statusPass,
        renderedMarker: markerPass,
        visibleOutsideCollapsedRecord: visiblePlacementPass,
        requiredText: requiredPass,
        staleTextAbsent: forbiddenPass,
        dossierLink: dossierMatches,
        primarySourceLink: sourceMatches,
      };

      const screenshotPath = path.join(artifactDir, `${target.language}-homepage-san-telmo-attribution.png`);
      await page.locator(selector).screenshot({ path: screenshotPath });
      entry.screenshot = screenshotPath;
      entry.pass = Object.values(entry.checks).every(Boolean);
      if (!entry.pass) failed = true;
    } catch (error) {
      entry.error = error instanceof Error ? `${error.name}: ${error.message}` : String(error);
      entry.pass = false;
      failed = true;
    } finally {
      results.push(entry);
      await page.close();
    }
  }
} finally {
  await browser.close();
}

const successStatus = base.startsWith('https://')
  ? 'RENDERED_DOM_LIVE_VERIFIED'
  : 'RENDERED_DOM_CHECKOUT_VERIFIED';
const output = {
  status: failed ? 'RENDERED_DOM_NOT_VERIFIED' : successStatus,
  base,
  verifiedAt: new Date().toISOString(),
  results,
};

const resultPath = path.join(artifactDir, 'result.json');
fs.writeFileSync(resultPath, `${JSON.stringify(output, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(output, null, 2));

if (failed) process.exit(1);

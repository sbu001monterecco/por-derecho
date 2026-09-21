import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const base = process.env.PSR_BASE_URL || 'https://sbu001monterecco.github.io/por-derecho';
const executablePath = process.env.PSR_BROWSER_PATH;
const artifactDir = process.env.PSR_EG95_ARTIFACT_DIR || 'artifacts/fiscalia-tenerife-eg95-live';
fs.mkdirSync(artifactDir, { recursive: true });

if (!executablePath) throw new Error('PSR_BROWSER_PATH is required');

const checks = [
  {
    name: 'es-eg95',
    route: '/es/fiscalia-tenerife-eg95-2026/',
    selector: 'h1',
    needles: ['Expediente Gubernativo 95/2026', 'archivo procedimental'],
  },
  {
    name: 'en-eg95',
    route: '/en/fiscalia-tenerife-eg95-2026/',
    selector: 'h1',
    needles: ['Administrative File 95/2026', 'procedural closure'],
  },
  {
    name: 'es-dp748-propagation',
    route: '/es/fiscalia-tenerife-dp748/',
    selector: '[data-eg95-dp748-update]',
    needles: ['Fiscalía abrió y archivó el Expediente Gubernativo 95/2026', 'No es una conclusión de fondo'],
  },
  {
    name: 'es-institutional-record',
    route: '/es/registros-institucionales/',
    selector: '[data-eg95-institutional-record]',
    needles: ['Santa Cruz de Tenerife', 'EG 95/2026', 'Archivo procedimental'],
  },
  {
    name: 'en-institutional-record',
    route: '/en/institutional-records/',
    selector: '[data-eg95-institutional-record]',
    needles: ['Santa Cruz de Tenerife', 'File 95/2026', 'Procedural closure'],
  },
  {
    name: 'es-updates',
    route: '/es/actualizaciones/',
    selector: '[data-eg95-update]',
    needles: ['Fiscalía Tenerife abre y archiva EG 95/2026', 'no rechaza expresamente'],
  },
  {
    name: 'en-updates',
    route: '/en/updates/',
    selector: '[data-eg95-update]',
    needles: ['Tenerife Prosecutor opens and closes File 95/2026', 'does not expressly reject'],
  },
];

const browser = await chromium.launch({
  headless: true,
  executablePath,
  args: ['--no-sandbox', '--disable-dev-shm-usage'],
});

const context = await browser.newContext({
  viewport: { width: 1440, height: 1200 },
  ignoreHTTPSErrors: false,
});

const result = { base, verified: false, checks: [] };

try {
  for (const check of checks) {
    const page = await context.newPage();
    const url = `${base}${check.route}?eg95-render=${Date.now()}`;
    const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 });
    if (!response || response.status() !== 200) {
      throw new Error(`${check.name}: HTTP ${response ? response.status() : 'no response'}`);
    }
    await page.waitForSelector(check.selector, { timeout: 90000, state: 'attached' });
    await page.waitForTimeout(1000);
    const text = (await page.locator(check.selector).innerText()).replace(/\s+/g, ' ').trim();
    const missing = check.needles.filter((needle) => !text.includes(needle));
    await page.screenshot({
      path: path.join(artifactDir, `${check.name}.png`),
      fullPage: true,
    });
    result.checks.push({ name: check.name, route: check.route, selector: check.selector, text, missing });
    await page.close();
    if (missing.length) {
      throw new Error(`${check.name}: missing ${missing.join(' | ')}`);
    }
  }
  result.verified = true;
} finally {
  fs.writeFileSync(path.join(artifactDir, 'rendered-public-edge.json'), JSON.stringify(result, null, 2));
  await browser.close();
}

if (!result.verified) process.exit(1);
console.log('Fiscalía Tenerife EG 95/2026 rendered public edge verified');

import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const base = (process.env.PSR_BASE_URL || 'http://127.0.0.1:4173/por-derecho').replace(/\/$/, '');
const executablePath = process.env.PSR_BROWSER_PATH || undefined;
const artifactDir = process.env.PSR_AC_DFA_ARTIFACT_DIR || 'artifacts/ac-community-de-facto';
fs.mkdirSync(artifactDir, { recursive: true });

const checks = [];
const record = (name, ok, detail = '') => checks.push({ name, ok: Boolean(ok), detail });
const browser = await chromium.launch({ headless: true, executablePath });
const context = await browser.newContext({ viewport: { width: 1440, height: 1200 } });

async function inspect(name, route, assertions, screenshot) {
  const page = await context.newPage();
  try {
    const response = await page.goto(`${base}${route}?verify=${Date.now()}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
    record(`${name}: http`, response?.status() === 200, `status=${response?.status()}`);
    await page.waitForTimeout(2200);
    const body = await page.locator('body').innerText();
    for (const assertion of assertions) {
      if (assertion.text) record(`${name}: ${assertion.label}`, body.includes(assertion.text), assertion.text);
      if (assertion.selector) {
        const count = await page.locator(assertion.selector).count();
        record(`${name}: ${assertion.label}`, count >= 1, `count=${count}`);
      }
      if (assertion.href) {
        const count = await page.locator(`a[href="${assertion.href}"]`).count();
        record(`${name}: ${assertion.label}`, count >= 1, `count=${count}`);
      }
    }
    if (screenshot) await page.screenshot({ path: path.join(artifactDir, screenshot), fullPage: true });
  } catch (error) {
    record(`${name}: navigation`, false, String(error));
  } finally {
    await page.close();
  }
}

await inspect('Spanish canonical', '/es/administracion-de-hecho-comunidad-ac/', [
  { label: 'page marker', selector: '[data-ac-community-shadow-control-page="20260820"]' },
  { label: 'canonical status panel', selector: '[data-ac-dfa-canonical-status="20260820"]' },
  { label: 'Community amount', text: '718.663,24 €' },
  { label: 'bid amount', text: '1.145.798,29 €' },
  { label: 'incident answer', text: 'No se ha localizado un incidente concursal posterior' },
  { label: 'English reciprocal route', href: '../../en/de-facto-administration-community-ac/' }
], 'es-canonical.png');

await inspect('English canonical', '/en/de-facto-administration-community-ac/', [
  { label: 'page marker', selector: '[data-ac-community-shadow-control-page="20260820"]' },
  { label: 'canonical status panel', selector: '[data-ac-dfa-canonical-status="20260820"]' },
  { label: 'Community amount', text: 'EUR 718,663.24' },
  { label: 'bid amount', text: 'EUR 1,145,798.29' },
  { label: 'incident answer', text: 'No post-liquidation insolvency incident has been located' },
  { label: 'Spanish reciprocal route', href: '../../es/administracion-de-hecho-comunidad-ac/' }
], 'en-canonical.png');

await inspect('Spanish Community crosslink', '/es/comunidad-instrumentalizacion/', [
  { label: 'crosslink panel', selector: '[data-ac-dfa-crosslink="20260820"]' },
  { label: 'canonical link', href: '/por-derecho/es/administracion-de-hecho-comunidad-ac/' }
], 'es-community.png');

await inspect('English Administrator crosslink', '/en/insolvency-36-2012-insolvency-administrator/', [
  { label: 'crosslink panel', selector: '[data-ac-dfa-crosslink="20260820"]' },
  { label: 'canonical link', href: '/por-derecho/en/de-facto-administration-community-ac/' }
], 'en-administrator.png');

await inspect('Spanish control update', '/es/sala-control-caso/', [
  { label: 'update panel', selector: '[data-ac-dfa-update="20260820"]' },
  { label: 'canonical link', href: '/por-derecho/es/administracion-de-hecho-comunidad-ac/' }
], 'es-control.png');

await inspect('English criminal investigation update', '/en/sun-park-criminal-engineering-investigation/', [
  { label: 'update panel', selector: '[data-ac-dfa-update="20260820"]' },
  { label: 'canonical link', href: '/por-derecho/en/de-facto-administration-community-ac/' }
], 'en-investigation.png');

await browser.close();

const result = {
  status: checks.every(item => item.ok) ? 'RENDER_VERIFIED' : 'RENDER_FAILED',
  base,
  checked_at: new Date().toISOString(),
  checks
};
fs.writeFileSync(path.join(artifactDir, 'result.json'), JSON.stringify(result, null, 2));
console.log(JSON.stringify(result, null, 2));
if (result.status !== 'RENDER_VERIFIED') process.exit(1);

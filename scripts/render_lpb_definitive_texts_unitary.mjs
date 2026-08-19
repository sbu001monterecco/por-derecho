import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const base = (process.env.PSR_BASE_URL || 'http://127.0.0.1:4173/por-derecho').replace(/\/$/, '');
const browserPath = process.env.PSR_BROWSER_PATH || undefined;
const artifactDir = process.env.PSR_LPB_TD_ARTIFACT_DIR || 'artifacts/lpb-definitive-texts';
fs.mkdirSync(artifactDir, { recursive: true });

const checks = [];
const record = (name, ok, detail = '') => checks.push({ name, ok: Boolean(ok), detail });

const browser = await chromium.launch({ headless: true, executablePath: browserPath });
const context = await browser.newContext({ viewport: { width: 1440, height: 1200 } });

async function inspect(name, route, assertions, screenshot) {
  const page = await context.newPage();
  const url = `${base}${route}?lpb_td_verify=${Date.now()}`;
  try {
    const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    record(`${name}: http`, response?.status() === 200, `status=${response?.status()}`);
    await page.waitForTimeout(2300);
    for (const assertion of assertions) {
      if (assertion.selector) {
        const count = await page.locator(assertion.selector).count();
        record(`${name}: ${assertion.label}`, count >= (assertion.min || 1), `count=${count}`);
      }
      if (assertion.text) {
        const body = await page.locator('body').innerText();
        record(`${name}: ${assertion.label}`, body.includes(assertion.text), assertion.text);
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

await inspect('Spanish canonical', '/es/textos-definitivos-lpb-base-liquidacion/', [
  { label: 'stable page marker', selector: '[data-lpb-definitive-texts-page="20260820"]' },
  { label: 'active mass', text: '19.486.498,94 €' },
  { label: 'passive mass', text: '10.125.752,00 €' },
  { label: 'special privilege', text: '9.052.251,69 €' },
  { label: 'English reciprocal route', href: '../../en/lpb-definitive-texts-liquidation-baseline/' },
], 'es-canonical.png');

await inspect('English canonical', '/en/lpb-definitive-texts-liquidation-baseline/', [
  { label: 'stable page marker', selector: '[data-lpb-definitive-texts-page="20260820"]' },
  { label: 'active mass', text: 'EUR 19,486,498.94' },
  { label: 'passive mass', text: 'EUR 10,125,752.00' },
  { label: 'special privilege', text: 'EUR 9,052,251.69' },
  { label: 'Spanish reciprocal route', href: '../../es/textos-definitivos-lpb-base-liquidacion/' },
], 'en-canonical.png');

await inspect('Spanish adjudication propagation', '/es/adjudicacion-2022-reconstruccion-documental/', [
  { label: 'primary-source promotion panel', selector: '[data-lpb-td-primary-promotion="20260820"]' },
  { label: 'canonical link', href: '/por-derecho/es/textos-definitivos-lpb-base-liquidacion/' },
  { label: 'corrected missing-evidence wording', text: 'Paquete judicial certificado completo de los textos definitivos' },
], 'es-adjudication.png');

await inspect('English adjudication propagation', '/en/2022-adjudication-documentary-reconstruction/', [
  { label: 'primary-source promotion panel', selector: '[data-lpb-td-primary-promotion="20260820"]' },
  { label: 'canonical link', href: '/por-derecho/en/lpb-definitive-texts-liquidation-baseline/' },
  { label: 'corrected missing-evidence wording', text: 'Court-certified complete definitive-text bundle' },
], 'en-adjudication.png');

await inspect('Spanish control-room update', '/es/sala-control-caso/', [
  { label: 'unitary update card', selector: '[data-lpb-td-update="20260820"]' },
  { label: 'new route link', href: '/por-derecho/es/textos-definitivos-lpb-base-liquidacion/' },
  { label: 'source promotion in issue register', text: 'Los textos definitivos de abril de 2016' },
], 'es-control-room.png');

await inspect('English control-room update', '/en/case-control-room/', [
  { label: 'unitary update card', selector: '[data-lpb-td-update="20260820"]' },
  { label: 'new route link', href: '/por-derecho/en/lpb-definitive-texts-liquidation-baseline/' },
  { label: 'source promotion in issue register', text: 'The April 2016 definitive texts' },
], 'en-control-room.png');

await inspect('Spanish lender cross-link', '/es/acreedor-de-registro/', [
  { label: 'cross-link panel', selector: '[data-lpb-td-crosslink="20260820"]' },
  { label: 'canonical baseline link', href: '/por-derecho/es/textos-definitivos-lpb-base-liquidacion/' },
], 'es-lender.png');

await inspect('English lender cross-link', '/en/lender-of-record/', [
  { label: 'cross-link panel', selector: '[data-lpb-td-crosslink="20260820"]' },
  { label: 'canonical baseline link', href: '/por-derecho/en/lpb-definitive-texts-liquidation-baseline/' },
], 'en-lender.png');

await browser.close();

const result = {
  status: checks.every(item => item.ok) ? 'RENDER_VERIFIED' : 'RENDER_FAILED',
  base,
  checked_at: new Date().toISOString(),
  checks,
};
fs.writeFileSync(path.join(artifactDir, 'result.json'), JSON.stringify(result, null, 2));
console.log(JSON.stringify(result, null, 2));
if (result.status !== 'RENDER_VERIFIED') process.exit(1);

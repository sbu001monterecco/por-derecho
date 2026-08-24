import fs from 'node:fs';
import path from 'node:path';
const playwright = await import(process.env.PSR_PLAYWRIGHT_PATH || 'playwright');
const { chromium } = playwright;

const base = (process.env.PSR_BASE_URL || 'http://127.0.0.1:4173/por-derecho').replace(/\/$/, '');
const executablePath = process.env.PSR_BROWSER_PATH || undefined;
const artifactDir = process.env.PSR_AC_DFA_ARTIFACT_DIR || 'artifacts/ac-community-de-facto';
fs.mkdirSync(artifactDir, { recursive: true });

const checks = [];
const record = (name, ok, detail = '') => checks.push({ name, ok: Boolean(ok), detail });
const browser = await chromium.launch({ headless: true, executablePath });
const context = await browser.newContext({ viewport: { width: 1440, height: 1200 } });

async function inspect(name, route, assertions, screenshot, options = {}) {
  const page = await context.newPage();
  try {
    const response = await page.goto(`${base}${route}?verify=${Date.now()}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
    record(`${name}: http`, response?.status() === 200, `status=${response?.status()}`);
    await page.waitForTimeout(2900);
    const progressiveRecord = page.locator('[data-audience-full-record] > details');
    if (options.openProgressive !== false && await progressiveRecord.count()) await progressiveRecord.evaluate((node) => { node.open = true; });
    const body = await page.locator('body').innerText();
    for (const assertion of assertions) {
      if (assertion.text) record(`${name}: ${assertion.label}`, body.includes(assertion.text), assertion.text);
      if (assertion.selector) {
        const count = await page.locator(assertion.selector).count();
        const expected = assertion.exactCount ?? null;
        const ok = expected === null ? count >= (assertion.minCount || 1) : count === expected;
        record(`${name}: ${assertion.label}`, ok, `count=${count}${expected === null ? '' : ` expected=${expected}`}`);
      }
      if (assertion.visibleSelector) {
        const nodes = page.locator(assertion.visibleSelector);
        const count = await nodes.count();
        const expected = assertion.exactCount ?? 1;
        let visible = count === expected;
        for (let index = 0; visible && index < count; index += 1) visible = await nodes.nth(index).isVisible();
        record(`${name}: ${assertion.label}`, visible, `count=${count} expected=${expected} visible=${visible}`);
      }
      if (assertion.outsideCollapsedSelector) {
        const result = await page.locator(assertion.outsideCollapsedSelector).evaluateAll((nodes) => ({
          count: nodes.length,
          outside: nodes.every((node) => !node.closest('[data-audience-full-record] details:not([open])'))
        }));
        record(`${name}: ${assertion.label}`, result.count === (assertion.exactCount ?? 1) && result.outside, JSON.stringify(result));
      }
      if (assertion.loadedImageSelector) {
        const result = await page.locator(assertion.loadedImageSelector).evaluateAll((images) => ({
          count: images.length,
          loaded: images.every((image) => image.complete && image.naturalWidth > 0)
        }));
        record(`${name}: ${assertion.label}`, result.count === (assertion.exactCount ?? 1) && result.loaded, JSON.stringify(result));
      }
      if (assertion.href) {
        const count = await page.locator(`a[href="${assertion.href}"]`).count();
        record(`${name}: ${assertion.label}`, count >= 1, `count=${count}`);
      }
      if (assertion.title) {
        const title = await page.title();
        record(`${name}: ${assertion.label}`, title.includes(assertion.title), title);
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
  { label: 'page marker', selector: '[data-ac-community-shadow-control-page="20260824"]' },
  { label: 'one allegation spotlight', selector: '[data-ac-dfa-allegation-visibility="20260824a"]', exactCount: 1 },
  { label: 'stable allegation marker', selector: '[data-ac-dfa-visibility-stable="20260824a"]', exactCount: 1 },
  { label: 'impact chain', selector: '[data-ac-dfa-impact-chain="20260824a"]', exactCount: 1 },
  { label: 'attributed allegation headline', text: 'Cinco administradores en la sombra alegados y una habilitación institucional activa' },
  { label: 'all five named', text: 'Shaila María Cogolludo Ramos' },
  { label: 'judge named', text: 'Alberto López Villarrubia' },
  { label: 'documented category', text: 'DOCUMENTADO' },
  { label: 'attributed category', text: 'POR DERECHO ALEGA' },
  { label: 'non-adjudication category', text: 'NO ADJUDICADO' },
  { label: 'decisive evidence category', text: 'PRUEBA DECISIVA' },
  { label: 'Community amount', text: '718.663,24 €' },
  { label: 'bid amount', text: '1.145.798,29 €' },
  { label: 'incident answer', text: 'No se ha localizado un incidente concursal posterior' },
  { label: 'corrections link', href: '/por-derecho/es/correcciones-control-versiones/' },
  { label: 'updated browser title', title: 'Cinco administradores de hecho alegados' },
  { label: 'English reciprocal route', href: '../../en/de-facto-administration-community-ac/' }
], 'es-canonical.png');

await inspect('English canonical', '/en/de-facto-administration-community-ac/', [
  { label: 'page marker', selector: '[data-ac-community-shadow-control-page="20260824"]' },
  { label: 'one allegation spotlight', selector: '[data-ac-dfa-allegation-visibility="20260824a"]', exactCount: 1 },
  { label: 'stable allegation marker', selector: '[data-ac-dfa-visibility-stable="20260824a"]', exactCount: 1 },
  { label: 'impact chain', selector: '[data-ac-dfa-impact-chain="20260824a"]', exactCount: 1 },
  { label: 'attributed allegation headline', text: 'Five alleged shadow administrators and active institutional enablement' },
  { label: 'all five named', text: 'Shaila María Cogolludo Ramos' },
  { label: 'judge named', text: 'Alberto López Villarrubia' },
  { label: 'documented category', text: 'DOCUMENTED' },
  { label: 'attributed category', text: 'POR DERECHO ALLEGES' },
  { label: 'non-adjudication category', text: 'NOT ADJUDICATED' },
  { label: 'decisive evidence category', text: 'DECISIVE EVIDENCE' },
  { label: 'Community amount', text: 'EUR 718,663.24' },
  { label: 'bid amount', text: 'EUR 1,145,798.29' },
  { label: 'incident answer', text: 'No post-liquidation insolvency incident has been located' },
  { label: 'corrections link', href: '/por-derecho/en/corrections-version-control/' },
  { label: 'updated browser title', title: 'Five alleged shadow administrators' },
  { label: 'Spanish reciprocal route', href: '../../es/administracion-de-hecho-comunidad-ac/' }
], 'en-canonical.png');

await inspect('Spanish homepage visibility', '/es/', [
  { label: 'one allegation spotlight', selector: '[data-ac-dfa-allegation-visibility="20260824a"]', exactCount: 1 },
  { label: 'stable allegation marker', selector: '[data-ac-dfa-visibility-stable="20260824a"]', exactCount: 1 },
  { label: 'impact chain', selector: '[data-ac-dfa-impact-chain="20260824a"]', exactCount: 1 },
  { label: 'headline', text: 'Cinco administradores en la sombra alegados y una habilitación institucional activa' },
  { label: 'canonical link', href: '/por-derecho/es/administracion-de-hecho-comunidad-ac/' },
  { label: 'one detailed visual', selector: 'section[data-pd-five-ac="20260824b"]', exactCount: 1 },
  { label: 'detailed visual visible before collapse', visibleSelector: 'section[data-pd-five-ac="20260824b"]', exactCount: 1 },
  { label: 'detailed visual outside collapsed record', outsideCollapsedSelector: 'section[data-pd-five-ac="20260824b"]', exactCount: 1 },
  { label: 'audience protection marker', selector: 'section[data-audience-protected-five-actor-visual="20260824b"]', exactCount: 1 },
  { label: 'five private actor cards', selector: 'section[data-pd-five-ac] [data-private-actor-card]', exactCount: 5 },
  { label: 'Administrator and Judge cards', selector: 'section[data-pd-five-ac] [data-institution-card]', exactCount: 2 },
  { label: 'five complete linkage rows', selector: 'section[data-pd-five-ac] [data-linkage-row]', exactCount: 5 },
  { label: 'Administrator and Judge portraits loaded', loadedImageSelector: 'section[data-pd-five-ac] .pd-five-ac__institution-portrait', exactCount: 2 },
  { label: 'private actor canonical portrait loaded', loadedImageSelector: 'section[data-pd-five-ac] .pd-five-ac__portrait', exactCount: 1 },
  { label: 'Administrator acts and omissions', text: 'Actos afirmativos / comisiones alegadas' },
  { label: 'Judge linkage named', text: 'Alberto López Villarrubia' }
], 'es-home.png', { openProgressive: false });

await inspect('English homepage visibility', '/en/', [
  { label: 'one detailed visual', selector: 'section[data-pd-five-ac="20260824b"]', exactCount: 1 },
  { label: 'detailed visual visible before collapse', visibleSelector: 'section[data-pd-five-ac="20260824b"]', exactCount: 1 },
  { label: 'detailed visual outside collapsed record', outsideCollapsedSelector: 'section[data-pd-five-ac="20260824b"]', exactCount: 1 },
  { label: 'audience protection marker', selector: 'section[data-audience-protected-five-actor-visual="20260824b"]', exactCount: 1 },
  { label: 'five private actor cards', selector: 'section[data-pd-five-ac] [data-private-actor-card]', exactCount: 5 },
  { label: 'Administrator and Judge cards', selector: 'section[data-pd-five-ac] [data-institution-card]', exactCount: 2 },
  { label: 'five complete linkage rows', selector: 'section[data-pd-five-ac] [data-linkage-row]', exactCount: 5 },
  { label: 'Administrator and Judge portraits loaded', loadedImageSelector: 'section[data-pd-five-ac] .pd-five-ac__institution-portrait', exactCount: 2 },
  { label: 'private actor canonical portrait loaded', loadedImageSelector: 'section[data-pd-five-ac] .pd-five-ac__portrait', exactCount: 1 },
  { label: 'Administrator acts and omissions', text: 'Alleged affirmative acts / commissions' },
  { label: 'Judge linkage named', text: 'Alberto López Villarrubia' }
], 'en-home.png', { openProgressive: false });

await inspect('English criminal hub visibility', '/en/sun-park-criminal-engineering-investigation/', [
  { label: 'one allegation spotlight', selector: '[data-ac-dfa-allegation-visibility="20260824a"]', exactCount: 1 },
  { label: 'stable allegation marker', selector: '[data-ac-dfa-visibility-stable="20260824a"]', exactCount: 1 },
  { label: 'headline', text: 'Five alleged shadow administrators and active institutional enablement' },
  { label: 'canonical link', href: '/por-derecho/en/de-facto-administration-community-ac/' }
], 'en-investigation.png');

await inspect('Spanish Community route relevance', '/es/comunidad-instrumentalizacion/', [
  { label: 'one route panel', selector: '[data-ac-dfa-route-relevance="20260824a"]', exactCount: 1 },
  { label: 'stable route marker', selector: '[data-ac-dfa-visibility-stable="20260824a"]', exactCount: 1 },
  { label: 'governance route type', selector: '[data-ac-dfa-route-type="governance"]', exactCount: 1 },
  { label: 'route headline', text: 'Acusación penal rectora: cinco actores + habilitación concursal y judicial' },
  { label: 'canonical link', href: '/por-derecho/es/administracion-de-hecho-comunidad-ac/' }
], 'es-community.png');

await inspect('English Administrator route relevance', '/en/insolvency-36-2012-insolvency-administrator/', [
  { label: 'one route panel', selector: '[data-ac-dfa-route-relevance="20260824a"]', exactCount: 1 },
  { label: 'stable route marker', selector: '[data-ac-dfa-visibility-stable="20260824a"]', exactCount: 1 },
  { label: 'AC route type', selector: '[data-ac-dfa-route-type="ac"]', exactCount: 1 },
  { label: 'route headline', text: 'Controlling criminal allegation: five actors + insolvency and judicial enablement' },
  { label: 'canonical link', href: '/por-derecho/en/de-facto-administration-community-ac/' }
], 'en-administrator.png');

await inspect('Spanish adjudication transaction relevance', '/es/adjudicacion-2022-reconstruccion-documental/', [
  { label: 'one route panel', selector: '[data-ac-dfa-route-relevance="20260824a"]', exactCount: 1 },
  { label: 'stable route marker', selector: '[data-ac-dfa-visibility-stable="20260824a"]', exactCount: 1 },
  { label: 'transaction route type', selector: '[data-ac-dfa-route-type="transaction"]', exactCount: 1 },
  { label: 'category-separation wording', text: 'deuda, contingencia, responsabilidad hipotecaria, mejor postura, contraprestación y cuentas' }
], 'es-adjudication.png');

await inspect('English notarial implementation relevance', '/en/notarial-implementation-protocol-457/', [
  { label: 'one route panel', selector: '[data-ac-dfa-route-relevance="20260824a"]', exactCount: 1 },
  { label: 'stable route marker', selector: '[data-ac-dfa-visibility-stable="20260824a"]', exactCount: 1 },
  { label: 'implementation route type', selector: '[data-ac-dfa-route-type="implementation"]', exactCount: 1 },
  { label: 'implementation wording', text: 'what title, authority, calculation and testimony were presented' }
], 'en-notary.png');

await inspect('Spanish RICPE downstream boundary', '/es/ricpe-responsabilidad-documental/', [
  { label: 'one route panel', selector: '[data-ac-dfa-route-relevance="20260824a"]', exactCount: 1 },
  { label: 'stable route marker', selector: '[data-ac-dfa-visibility-stable="20260824a"]', exactCount: 1 },
  { label: 'downstream route type', selector: '[data-ac-dfa-route-type="downstream"]', exactCount: 1 },
  { label: 'no automatic transfer wording', text: 'No se transfiere conocimiento ni culpabilidad automáticamente' }
], 'es-ricpe.png');

await browser.close();

const result = {
  status: checks.every(item => item.ok) ? 'RENDER_VERIFIED' : 'RENDER_FAILED',
  base,
  checked_at: new Date().toISOString(),
  assertions: checks.length,
  checks
};
fs.writeFileSync(path.join(artifactDir, 'result.json'), JSON.stringify(result, null, 2));
console.log(JSON.stringify(result, null, 2));
if (result.status !== 'RENDER_VERIFIED') process.exit(1);

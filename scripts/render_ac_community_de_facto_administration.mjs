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
    if (JSON.stringify(assertions).includes('data-pd-five-ac')) {
      await page.locator('section[data-pd-five-ac]').waitFor({ state: 'attached', timeout: 15000 });
    }
    await page.waitForTimeout(2900);
    const progressiveRecord = page.locator('[data-audience-full-record] > details');
    if (options.openProgressive !== false && await progressiveRecord.count()) await progressiveRecord.evaluate((node) => { node.open = true; });
    const body = await page.locator('body').innerText();
    for (const assertion of assertions) {
      if (assertion.text) record(`${name}: ${assertion.label}`, body.includes(assertion.text), assertion.text);
      if (assertion.absentText) record(`${name}: ${assertion.label}`, !body.includes(assertion.absentText), assertion.absentText);
      if (assertion.textSelector) {
        const nodes = page.locator(assertion.textSelector);
        const count = await nodes.count();
        const text = count ? await nodes.first().innerText() : '';
        const normalised = text.replace(/\s+/g, ' ').trim().toLocaleLowerCase();
        const expected = assertion.includesAll || [];
        const ok = count === 1 && expected.every((value) => normalised.includes(value.toLocaleLowerCase()));
        record(`${name}: ${assertion.label}`, ok, `count=${count}; expected=${expected.join(' + ')}`);
      }
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
      if (assertion.nonEmptySelector) {
        const result = await page.locator(assertion.nonEmptySelector).evaluateAll(nodes => ({
          count: nodes.length,
          nonEmpty: nodes.every(node => (node.textContent || '').trim().length > 0)
        }));
        const expected = assertion.exactCount ?? 1;
        record(`${name}: ${assertion.label}`, result.count === expected && result.nonEmpty, JSON.stringify(result));
      }
      if (assertion.eachChildCount) {
        const result = await page.locator(assertion.eachChildCount.selector).evaluateAll((nodes, childSelector) => ({
          count: nodes.length,
          childCounts: nodes.map(node => node.querySelectorAll(childSelector).length)
        }), assertion.eachChildCount.childSelector);
        const expectedRows = assertion.eachChildCount.exactCount;
        const expectedChildren = assertion.eachChildCount.children;
        const ok = result.count === expectedRows && result.childCounts.every(count => count === expectedChildren);
        record(`${name}: ${assertion.label}`, ok, JSON.stringify(result));
      }
      if (assertion.firstReadAfterHeroSelector) {
        const selector = assertion.firstReadAfterHeroSelector;
        let waitError = '';
        try {
          await page.evaluate(() => { delete window.__pdFirstReadStableSince; });
          const settled = await page.waitForFunction((candidateSelector) => {
            const node = document.querySelector(candidateSelector);
            const main = node?.closest('main');
            const hero = main?.querySelector(':scope > .dossier-hero')
              || main?.querySelector(':scope > .hero')
              || main?.querySelector(':scope > section:first-of-type');
            const inPosition = Boolean(node && main && node.parentElement === main && hero?.nextElementSibling === node);
            if (!inPosition) {
              window.__pdFirstReadStableSince = 0;
              return false;
            }
            if (!window.__pdFirstReadStableSince) window.__pdFirstReadStableSince = performance.now();
            return performance.now() - window.__pdFirstReadStableSince >= 500;
          }, selector, { timeout: 10000 });
          await settled.dispose();
          // Sample again after a paint after proving 500 ms of continuous
          // adjacency. This remains an exact first-after-hero assertion while
          // allowing the page's documented composition guards to settle.
          await page.waitForTimeout(120);
        } catch (error) {
          waitError = String(error);
        }
        const result = await page.locator(selector).evaluate(node => {
          const main = node.closest('main');
          const hero = main?.querySelector(':scope > .dossier-hero')
            || main?.querySelector(':scope > .hero')
            || main?.querySelector(':scope > section:first-of-type');
          const next = hero?.nextElementSibling;
          return {
            direct: node.parentElement === main,
            immediatelyAfter: next === node,
            hero: hero ? `${hero.tagName.toLowerCase()}${hero.id ? `#${hero.id}` : ''}.${[...hero.classList].join('.')}` : null,
            actualNext: next ? `${next.tagName.toLowerCase()}${next.id ? `#${next.id}` : ''}.${[...next.classList].join('.')}` : null
          };
        });
        record(`${name}: ${assertion.label}`, result.direct && result.immediatelyAfter, JSON.stringify({ ...result, waitError }));
      }
      if (assertion.outsideCollapsedSelector) {
        const result = await page.locator(assertion.outsideCollapsedSelector).evaluateAll((nodes) => ({
          count: nodes.length,
          outside: nodes.every((node) => !node.closest('[data-audience-full-record] details:not([open])'))
        }));
        record(`${name}: ${assertion.label}`, result.count === (assertion.exactCount ?? 1) && result.outside, JSON.stringify(result));
      }
      if (assertion.loadedImageSelector) {
        const selector = assertion.loadedImageSelector;
        const images = page.locator(selector);
        const expected = assertion.exactCount ?? 1;
        const count = await images.count();
        let waitError = '';
        if (count === expected) {
          try {
            for (let index = 0; index < count; index += 1) {
              await images.nth(index).scrollIntoViewIfNeeded({ timeout: 5000 });
            }
            const loaded = await page.waitForFunction(({ candidateSelector, expectedCount }) => {
              const candidates = [...document.querySelectorAll(candidateSelector)];
              return candidates.length === expectedCount
                && candidates.every(image => image.complete && image.naturalWidth > 0 && image.naturalHeight > 0);
            }, { candidateSelector: selector, expectedCount: expected }, { timeout: 10000 });
            await loaded.dispose();
          } catch (error) {
            waitError = String(error);
          }
        }
        const result = await images.evaluateAll((candidates) => ({
          count: candidates.length,
          loaded: candidates.every(image => image.complete && image.naturalWidth > 0 && image.naturalHeight > 0),
          images: candidates.map(image => ({
            src: image.currentSrc || image.getAttribute('src'),
            loading: image.loading,
            complete: image.complete,
            naturalWidth: image.naturalWidth,
            naturalHeight: image.naturalHeight
          }))
        }));
        record(`${name}: ${assertion.label}`, result.count === expected && result.loaded, JSON.stringify({ ...result, waitError }));
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
  { label: 'Administrator acts and omissions', textSelector: 'section[data-pd-five-ac] [data-institution-card="administrator"]', includesAll: ['Actos afirmativos / comisiones alegadas', 'Omisiones alegadas'] },
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
  { label: 'Administrator acts and omissions', textSelector: 'section[data-pd-five-ac] [data-institution-card="administrator"]', includesAll: ['Alleged affirmative acts / commissions', 'Alleged omissions'] },
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

const lockedDirectRoutes = [
  ['Spanish canonical detailed presentation', '/es/administracion-de-hecho-comunidad-ac/', 'canonical'],
  ['English canonical detailed presentation', '/en/de-facto-administration-community-ac/', 'canonical'],
  ['Spanish PwC detailed presentation', '/es/pwc-canarias-carlos-saavedra-sun-park/', 'pwc'],
  ['English PwC detailed presentation', '/en/pwc-canarias-carlos-saavedra-sun-park/', 'pwc'],
  ['Spanish RICPE detailed presentation', '/es/ric-private-equity-sun-park/', 'ricpe'],
  ['English RICPE detailed presentation', '/en/ric-private-equity-sun-park/', 'ricpe'],
  ['Spanish Administrator detailed presentation', '/es/concurso-36-2012-administrador-concursal/', 'ac'],
  ['English Administrator detailed presentation', '/en/insolvency-36-2012-insolvency-administrator/', 'ac'],
  ['Spanish canonical Judge detailed presentation', '/es/concurso-36-2012-magistrado-juez/', 'court'],
  ['Spanish Judge detailed presentation', '/es/concurso-36-2012-juzgado-mercantil-1/', 'court'],
  ['English Judge detailed presentation', '/en/insolvency-36-2012-mercantile-court-1/', 'court'],
  ['Spanish takeover detailed presentation', '/es/toma-control-sun-park-7-junio-2018/', 'takeover'],
  ['English takeover detailed presentation', '/en/sun-park-takeover-7-june-2018/', 'takeover'],
  ['Spanish accountability detailed presentation', '/es/concurso-36-2012-responsabilidad-institucional/', 'accountability'],
  ['English accountability detailed presentation', '/en/insolvency-36-2012-institutional-accountability/', 'accountability'],
];

for (const [name, route, presentation] of lockedDirectRoutes) {
  const spanish = route.startsWith('/es/');
  const pwcGraphic = spanish
    ? 'pwc-five-actors-plus-ac-2016-knowledge-checkpoint-ES.png'
    : 'pwc-five-actors-plus-ac-2016-knowledge-checkpoint-EN.png';
  await inspect(name, route, [
    { label: 'locked detailed component', selector: `section[data-pd-five-ac="20260824b"][data-five-actor-front-page-lock="express-authorization-required"][data-key-direct-route-presentation="${presentation}"]`, exactCount: 1 },
    { label: 'detailed component visible', visibleSelector: 'section[data-pd-five-ac="20260824b"]', exactCount: 1 },
    { label: 'detailed component outside collapsed record', outsideCollapsedSelector: 'section[data-pd-five-ac="20260824b"]', exactCount: 1 },
    { label: 'detailed component is first after hero', firstReadAfterHeroSelector: 'section[data-pd-five-ac="20260824b"]' },
    { label: 'direct-route first-read pin', selector: 'section[data-direct-route-first-read-pin="20260824d"]', exactCount: 1 },
    { label: 'five private actor cards', selector: 'section[data-pd-five-ac] [data-private-actor-card]', exactCount: 5 },
    { label: 'five non-empty private descriptions', nonEmptySelector: 'section[data-pd-five-ac] [data-private-actor-card] .pd-five-ac__copy', exactCount: 5 },
    ...['fmmm', 'acr', 'smcr', 'jdam', 'lpam'].map(id => ({ label: `private actor id ${id}`, selector: `section[data-pd-five-ac] [data-private-actor-id="${id}"]`, exactCount: 1 })),
    { label: 'one Administrator card', selector: 'section[data-pd-five-ac] [data-institution-card="administrator"]', exactCount: 1 },
    { label: 'one Judge card', selector: 'section[data-pd-five-ac] [data-institution-card="judge"]', exactCount: 1 },
    { label: 'two distinct institutional role labels', nonEmptySelector: 'section[data-pd-five-ac] .pd-five-ac__institution-role', exactCount: 2 },
    { label: 'two institutional descriptions', nonEmptySelector: 'section[data-pd-five-ac] .pd-five-ac__institution-copy', exactCount: 2 },
    { label: 'four acts/omissions columns', nonEmptySelector: 'section[data-pd-five-ac] .pd-five-ac__accountability-column', exactCount: 4 },
    { label: 'two direct institutional allegations', nonEmptySelector: 'section[data-pd-five-ac] .pd-five-ac__institution-allegation', exactCount: 2 },
    { label: 'two institutional contrary boundaries', nonEmptySelector: 'section[data-pd-five-ac] .pd-five-ac__institution-boundary', exactCount: 2 },
    { label: 'five actor-specific linkage rows', selector: 'section[data-pd-five-ac] [data-linkage-row]', exactCount: 5 },
    { label: 'five complete five-cell linkage rows', eachChildCount: { selector: 'section[data-pd-five-ac] [data-linkage-row]', childSelector: '.pd-five-ac__linkage-cell', exactCount: 5, children: 5 } },
    ...['fmmm', 'acr', 'smcr', 'jdam', 'lpam'].map(id => ({ label: `linkage actor id ${id}`, selector: `section[data-pd-five-ac] [data-linkage-actor-id="${id}"]`, exactCount: 1 })),
    ...['Francisco Mario Matos Matas', 'Antonio Cogolludo Rojas', 'Shaila María Cogolludo Ramos', 'José Daniel Acosta Matos', 'Laura Patricia Acosta Matos', 'Francisco de Borja Rodríguez-Batllori Laffitte', 'Alberto López Villarrubia'].map(person => ({ label: `identity ${person}`, text: person })),
    { label: 'forbidden Laura identity absent', absentText: 'Laura Isabel' },
    { label: 'Administrator and Judge portraits loaded', loadedImageSelector: 'section[data-pd-five-ac] .pd-five-ac__institution-portrait', exactCount: 2 },
    { label: 'canonical private-actor portrait loaded', loadedImageSelector: 'section[data-pd-five-ac] .pd-five-ac__portrait', exactCount: 1 },
    { label: 'approved FMMM portrait', selector: 'section[data-pd-five-ac] img[src*="actors/francisco-mario-matos-matas.jpg"]', exactCount: 1 },
    { label: 'approved Administrator portrait', selector: 'section[data-pd-five-ac] img[src*="actors/francisco-de-borja-rodriguez-batllori.jpg"]', exactCount: 1 },
    { label: 'approved Judge portrait', selector: 'section[data-pd-five-ac] img[src*="actors/alberto-lopez-villarrubia.jpg"]', exactCount: 1 },
    { label: 'two evidence visuals loaded', loadedImageSelector: 'section[data-pd-five-ac] .pd-five-ac__evidence-visuals img', exactCount: 2 },
    { label: 'approved PwC evidence visual', selector: `section[data-pd-five-ac] img[src*="${pwcGraphic}"]`, exactCount: 1 },
    { label: 'approved family-plan evidence visual', selector: 'section[data-pd-five-ac] img[src*="acosta-matos-family-hotel-plans.jpg"]', exactCount: 1 },
    { label: 'seven reciprocal dossier links', selector: 'section[data-pd-five-ac] .pd-five-ac__links a', exactCount: 7 },
  ], null, { openProgressive: false });
}

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

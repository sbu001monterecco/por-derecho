#!/usr/bin/env node
/**
 * Sun Park Evidence & Position-Shift Atlas public-safe release tests.
 * Advisory, read-only verification: no publication, no law/merits determination.
 */
import assert from 'node:assert/strict';
import { readFileSync, existsSync, mkdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const read = p => readFileSync(path.join(root, p), 'utf8');
const publicPrefix = '/por-derecho/';
const pages = {
  en: 'en/sun-park-atlas/index.html',
  es: 'es/atlas-probatorio-sun-park/index.html'
};
const sameSiteRoutes = {
  en: ['case-control-room','actua-gesvalt-2018-valuation-comparison',
       'sun-park-forensic-map-262-properties','ric-private-equity-sun-park',
       'pwc-canarias-carlos-saavedra-sun-park','same-hotel-multiple-financial-lives',
       'ricpe-hnt-gc836-traceability'],
  es: ['sala-control-caso','comparativa-tasaciones-actua-gesvalt-2018',
       'mapa-forense-sun-park-262-fincas','ric-private-equity-sun-park',
       'pwc-canarias-carlos-saavedra-sun-park','mismo-hotel-multiples-vidas-financieras',
       'ricpe-hnt-gc836-trazabilidad']
};
const loaded = {};
const originalSvg = {
  en: '9525a21a6e26578368d03bebe10e2d2e246a14a5823bbf16d73909dfad417355',
  es: '0261759568030b519926b30e9ce8f8d569fd152ace87ba72091a01cec2841994'
};

for (const lang of ['en','es']) {
  const dataPath = `assets/atlas/atlas-public-v1.${lang}.json`;
  const data = JSON.parse(read(dataPath));
  loaded[lang] = data;
  assert.equal(data.schema,'por-derecho.sun-park-atlas.public.v1');
  assert.equal(data.locale,lang);
  assert.equal(data.tracks.length,8);
  assert.equal(data.stages.length,9);
  assert.equal(data.positions.length,3);
  assert.equal(data.valuations.length,4);
  assert.equal(data.finance.length,5);
  assert.equal(data.perimeter.reduce((n,x)=>n+x.count,0),262);
  assert.deepEqual(data.perimeter.map(x=>x.count),[54,190,18]);
  assert.deepEqual(data.stages.map(x=>x.id),Array.from({length:9},(_,i)=>'b'+(i+1)));
  assert.deepEqual(data.tracks.map(x=>x.id),
    ['rights','valuation','positions','courts','operations','finance','harm','accountability']);
  assert.ok(data.boundary.length>90);
  const candidate = JSON.stringify(data);
  for (const secret of ['docs.google.com','drive.google.com','mail.google.com','gitlab.com',
                        '/private/','/internal/', '1Eik6Ye1gNPJ','1qOiE7xzE26G']) {
    assert.ok(!candidate.includes(secret),`${lang} public data contains sensitive locator ${secret}`);
  }
  const trackIDs = new Set(data.tracks.map(t=>t.id));
  for (const stage of data.stages) {
    assert.ok(stage.tracks.every(t=>trackIDs.has(t)),`${lang} invalid stage tracks`);
    assert.ok(stage.assertion && stage.limit && stage.missing && stage.href,`${lang} incomplete stage`);
  }
  for (const node of [...data.tracks,...data.stages,...data.positions,...data.valuations]) {
    assert.ok(node.href.startsWith(publicPrefix+lang+'/'),`${lang} invalid locale/URL ${node.href}`);
    assert.ok(node.href.endsWith('/'),`${lang} missing route slash`);
    const doc = node.href.slice(publicPrefix.length)+'index.html';
    assert.ok(existsSync(path.join(root,doc)),`${lang} broken public reader route ${doc}`);
  }
  const html = read(pages[lang]);
  assert.ok(html.includes(`<html lang="${lang}">`));
  assert.ok(html.includes('id="sun-park-atlas-root"'));
  assert.ok(html.includes('class="section spa-atlas-static"'));
  assert.ok(html.includes('sun-park-atlas-v1.js'));
  assert.ok(html.includes('sun-park-atlas-v1.css'));
  assert.ok(!html.includes('../../assets/site.js'),
    `${lang} dedicated Atlas must not load inherited global site modules`);
  const other = lang==='en'?'es':'en';
  assert.ok(html.includes(`hreflang="${other}"`));
  assert.ok(html.includes(data.publicControl));
  const sha = createHash('sha256').update(readFileSync(path.join(
    root,`assets/graphics/pwc-band2-connected-economic-perimeter-20261018-${lang}.svg`))).digest('hex');
  assert.equal(sha,originalSvg[lang],`original Band 2 ${lang} asset mutated`);
}
const js = read('assets/atlas/sun-park-atlas-v1.js');
const loader = read('assets/site.js');
assert.ok(js.includes('#tres-realidades-ricpe'),'Spanish RICPE source anchor missing');
assert.ok(js.includes('#pwc-eccta-economic-fruits-20261018 figure.evidence-figure.wide'),
          'Bilingual Band 2 figure anchor missing');
assert.ok(!js.includes('spa-full-filtered-tracks'),'Hidden duplicate track cards remain');
assert.ok(loader.includes('SUN_PARK_ATLAS_CONTEXT_LOADER_20261027'));
for (const [lang,routes] of Object.entries(sameSiteRoutes)) {
  for (const slug of routes) {
    assert.ok(loader.includes(`${publicPrefix}${lang}/${slug}/`),
      `Missing ${lang} loader route ${slug}`);
  }
}
const pageSourceChecks = [
 ['en/ric-private-equity-sun-park/index.html','id="three-ricpe-realities"'],
 ['es/ric-private-equity-sun-park/index.html','id="tres-realidades-ricpe"'],
 ['en/pwc-canarias-carlos-saavedra-sun-park/index.html','id="pwc-eccta-economic-fruits-20261018"'],
 ['es/pwc-canarias-carlos-saavedra-sun-park/index.html','id="pwc-eccta-economic-fruits-20261018"'],
];
for(const [file,marker] of pageSourceChecks)assert.ok(read(file).includes(marker),file+' missing anchor '+marker);
for(const f of ['assets/atlas/sun-park-atlas-v1.js','assets/site.js'])
  execFileSync('node',['--check',f],{cwd:root,stdio:'pipe'});

const paths = [
  '/en/sun-park-atlas/','/es/atlas-probatorio-sun-park/',
  ...Object.entries(sameSiteRoutes).flatMap(([lang,routes])=>routes.map(slug=>`/${lang}/${slug}/`))
];
assert.equal(paths.length,16);
console.log('ATLAS STATIC PASS: 2 bilingual editions; 8 tracks; 9 stages; 262 fincas; 16 routes; original SVG SHA; no private locators.');

if (process.argv.includes('--browser')) {
  const { chromium } = await import('playwright');
  const browser = await chromium.launch({headless:true,args:['--no-sandbox']});
  const dir = path.join(root,'artifacts/sun-park-atlas-20261027');
  mkdirSync(dir,{recursive:true});
  const baseEnv = process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho';
  const base = baseEnv.endsWith('/') ? baseEnv.slice(0,-1) : baseEnv;
  try {
    for (const [index,route] of paths.entries()) {
      const url = base+route;
      const page = await browser.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1});
      try {
        await page.route('**/*', req => {
          const target = new URL(req.request().url());
          if (target.hostname === '127.0.0.1' || target.hostname === 'localhost') return req.continue();
          return req.abort();
        });
        const response = await page.goto(url,{waitUntil:'domcontentloaded',timeout:30000});
        assert.equal(response?.status(),200,route+' HTTP status');
        const selector='section.spa-atlas[data-sp-atlas-v1]';
        await page.waitForSelector(selector,{timeout:30000});
        const state = await page.locator(selector).first().evaluate(el=>({
          mode:el.getAttribute('data-sp-atlas-v1'),
          trackCount:el.querySelectorAll('.spa-track').length,
          stages:el.querySelectorAll('.spa-stage').length,
          positions:el.querySelectorAll('.spa-position').length,
          valuations:el.querySelectorAll('.spa-value').length
        }));
        assert.ok(state.mode,route+' missing renderer mode');
        if (index<2) {
          const previous=await page.locator('#sun-park-atlas-root').evaluate(el=>el.previousElementSibling?.className||'');
          assert.ok(previous.split(/\\s+/).includes('hero'),
            `${route} unrelated inherited page sections inserted ahead of Atlas: ${previous}`);
          assert.equal(state.mode,'full');
          assert.equal(state.trackCount,8);
          assert.equal(state.stages,9);
          assert.equal(state.positions,3);
          assert.equal(state.valuations,4);
          const filter=page.locator(`${selector} button.spa-filter[data-track="rights"]`);
          await filter.click();
          assert.equal(await filter.getAttribute('aria-pressed'),'true');
          const rights=loaded[index===0?'en':'es'].stages.filter(s=>s.tracks.includes('rights')).length;
          assert.equal(await page.locator(`${selector} .spa-stage:not([hidden])`).count(),rights);
          await page.locator(`${selector} button.spa-filter[data-track="all"]`).click();
          assert.equal(await page.locator(`${selector} .spa-stage:not([hidden])`).count(),9);
          assert.equal(await page.locator('.spa-atlas-static').isVisible(),false);
          await page.screenshot({path:path.join(dir,index===0?'atlas-en-desktop.png':'atlas-es-desktop.png'),fullPage:true});
          await page.setViewportSize({width:390,height:844});
          const width=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,viewport:innerWidth}));
          assert.ok(width.scroll<=width.viewport+8,
            `Mobile horizontal overflow: ${route} ${width.scroll}/${width.viewport}`);
          await page.screenshot({path:path.join(dir,index===0?'atlas-en-mobile.png':'atlas-es-mobile.png'),fullPage:true});
        }
        if (route.includes('pwc-canarias')) {
          assert.equal(state.mode,'band');
          assert.equal(state.stages,9);
          assert.ok(await page.locator(`${selector} .spa-detail`).count()===9);
        }
        if (route.includes('ric-private-equity')) {
          assert.equal(state.mode,'positions');
          assert.equal(state.positions,3);
          const expectedAnchor = route.startsWith('/es/') ? '#tres-realidades-ricpe' : '#three-ricpe-realities';
          const placement=await page.locator(selector).first().evaluate((el,anchor) => {
            const previous=el.previousElementSibling;
            const target=document.querySelector(anchor);
            return {adjacentToSource:!!previous && !!target && previous.contains(target),
                    previousTag:previous?.tagName||null,
                    previousId:previous?.id||null,
                    targetFound:!!target};
          },expectedAnchor);
          assert.ok(placement.adjacentToSource,
            `Wrong RICPE insertion location: ${JSON.stringify(placement)}`);
        }
        console.log('ATLAS BROWSER PASS',route,state.mode);
      } finally {await page.close();}
    }
    console.log('ATLAS BROWSER PASS: 16 routes; full-page desktop/mobile, filters, Band 2 and Spanish RICPE placement.');
  } finally {await browser.close();}
}

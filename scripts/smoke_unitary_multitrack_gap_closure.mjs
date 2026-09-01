import { chromium } from 'playwright';

const base = (process.env.PSR_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');
const executablePath = process.env.PSR_BROWSER_PATH || undefined;
const browser = await chromium.launch({ headless: true, executablePath });
const fail = (message) => { throw new Error(message); };

try {
  const context = await browser.newContext();
  const response = await context.request.get(`${base}/assets/data/unitary-multitrack-criminal-first-gap-closure-v1.json`);
  if (!response.ok()) fail(`dataset returned ${response.status()}`);
  const data = await response.json();
  if (data.tracks.length !== 18 || data.gaps.length !== 16) fail('finite track/gap denominators changed');
  if (data.reverse_chain.nodes.length !== 12 || data.evidence_classes.length !== 7) fail('reverse-chain or evidence-class denominator changed');
  if (data.criminal_threshold_hypotheses.length !== 5) fail('threshold-hypothesis denominator changed');
  if (data.authority_legitimacy_propagation.stages.length !== 10) fail('authority-propagation denominator changed');
  await context.close();

  const routes = [
    {
      lang: 'es',
      path: '/es/ingenieria-inversa-criminal-unitaria/',
      boundary: 'no declara delito',
      caret: 'El signo ^ confirma únicamente',
      lph: '/es/comunidad-instrumentalizacion/sala-documental-actas/control-lph-ciclo-juntas/',
      authority: '/es/actas-comunidad-autoridades-publicas/',
      direct: 'mecanismo criminal organizado, coordinado y continuado',
      notice: 'Primera respuesta de Intervención General',
    },
    {
      lang: 'en',
      path: '/en/unitary-criminal-reverse-engineering/',
      boundary: 'does not declare an offence',
      caret: 'The ^ marker confirms only',
      lph: '/en/community-instrumentalisation/acta-document-room/meeting-lifecycle-lph-control/',
      authority: '/en/community-actas-public-authorities/',
      direct: 'organised, coordinated and continuous criminal mechanism',
      notice: 'First Intervención General response',
    },
  ];

  for (const route of routes) {
    for (const width of [1440, 360]) {
      const page = await browser.newPage({ viewport: { width, height: 1000 } });
      const errors = [];
      page.on('pageerror', (error) => errors.push(error.message));
      page.on('console', (message) => { if (message.type() === 'error') errors.push(message.text()); });
      const navigation = await page.goto(`${base}${route.path}#unitary-gap-register`, { waitUntil: 'networkidle', timeout: 60000 });
      if (!navigation?.ok()) fail(`${route.lang}/${width}: route returned ${navigation?.status()}`);
      await page.waitForSelector('[data-ucf-gap="PD-GAP-UCF-016"]', { timeout: 30000 });
      const body = await page.locator('body').innerText();
      if (!body.includes(route.boundary) || !body.includes(route.caret)) fail(`${route.lang}/${width}: attribution or caret boundary missing`);
      if (!body.includes(route.direct) || !body.includes(route.notice)) fail(`${route.lang}/${width}: direct criminal attribution or Intervención checkpoint missing`);
      if (await page.locator('.pd-ucf-metric').count() !== 11) fail(`${route.lang}/${width}: denominator crosswalk did not render 11 metrics`);
      if (await page.locator('.pd-ucf-class').count() !== 7) fail(`${route.lang}/${width}: evidence legend did not render 7 classes`);
      if (await page.locator('[data-ucf-node]').count() !== 12) fail(`${route.lang}/${width}: reverse chain did not render 12 nodes`);
      if (await page.locator('[data-ucf-authority-stage]').count() !== 10) fail(`${route.lang}/${width}: authority chain did not render 10 stages`);
      if (await page.locator('[data-ucf-track]').count() !== 18) fail(`${route.lang}/${width}: track matrix did not render 18 tracks`);
      if (await page.locator('.pd-ucf-threshold').count() !== 5) fail(`${route.lang}/${width}: threshold matrix did not render 5 hypotheses`);
      if (await page.locator('[data-ucf-gap]').count() !== 16) fail(`${route.lang}/${width}: gap register did not render 16 gaps`);
      if (await page.locator('#evidence-PD-EV-UCF-INT-184368-2026').count() !== 1) fail(`${route.lang}/${width}: canonical Intervención evidence anchor missing`);
      await page.evaluate(() => { location.hash = '#evidence-PD-EV-UCF-INT-184368-2026'; });
      await page.waitForFunction(() => {
        const target = document.getElementById('evidence-PD-EV-UCF-INT-184368-2026');
        if (!target) return false;
        const rect = target.getBoundingClientRect();
        return rect.bottom > 0 && rect.top < innerHeight;
      });
      const hrefs = await page.locator('.pd-ucf-actions a').evaluateAll((nodes) => nodes.map((node) => node.href));
      if (!hrefs.some((href) => href.includes(route.lph))) fail(`${route.lang}/${width}: LPH reciprocal action missing`);
      if (!hrefs.some((href) => href.includes(route.authority))) fail(`${route.lang}/${width}: authority reciprocal action missing`);
      await page.locator('[data-ucf-track-class]').selectOption('NOTICE');
      if (await page.locator('[data-ucf-track]').count() !== 4) fail(`${route.lang}/${width}: NOTICE filter should show 4 tracks`);
      await page.locator('[data-ucf-track-class]').selectOption('');
      await page.locator('[data-ucf-gap-priority]').selectOption('P1');
      if (await page.locator('[data-ucf-gap]').count() !== 2) fail(`${route.lang}/${width}: P1 filter should show 2 gaps`);
      await page.locator('[data-ucf-gap-priority]').selectOption('');
      const overflow = await page.evaluate(() => ({
        width: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        offenders: Array.from(document.querySelectorAll('body *')).map((node) => {
          const rect = node.getBoundingClientRect();
          return { tag: node.tagName, className: node.className, right: Math.round(rect.right), left: Math.round(rect.left) };
        }).filter((item) => item.right > innerWidth + 2 || item.left < -2).slice(0, 12),
      }));
      if (overflow.width > 2) fail(`${route.lang}/${width}: horizontal overflow ${overflow.width}px ${JSON.stringify(overflow.offenders)}`);
      if (errors.length) fail(`${route.lang}/${width}: browser errors: ${errors.join(' | ')}`);
      await page.close();
    }
  }

  for (const [path, markers] of [
    ['/es/comunidad-instrumentalizacion/sala-documental-actas/control-lph-ciclo-juntas/', ['/es/actas-comunidad-autoridades-publicas/', '/es/ingenieria-inversa-criminal-unitaria/']],
    ['/en/community-instrumentalisation/acta-document-room/meeting-lifecycle-lph-control/', ['/en/community-actas-public-authorities/', '/en/unitary-criminal-reverse-engineering/']],
    ['/es/actas-comunidad-autoridades-publicas/', ['/es/comunidad-instrumentalizacion/sala-documental-actas/control-lph-ciclo-juntas/', '/es/ingenieria-inversa-criminal-unitaria/']],
    ['/en/community-actas-public-authorities/', ['/en/community-instrumentalisation/acta-document-room/meeting-lifecycle-lph-control/', '/en/unitary-criminal-reverse-engineering/']],
  ]) {
    const page = await browser.newPage();
    await page.goto(`${base}${path}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    const hrefs = await page.locator('a').evaluateAll((nodes) => nodes.map((node) => node.href));
    for (const marker of markers) {
      if (!hrefs.some((href) => href.includes(marker))) fail(`${path}: reciprocal marker missing ${marker}`);
    }
    await page.close();
  }

  for (const path of [
    '/es/administracion-de-hecho-comunidad-ac/',
    '/en/de-facto-administration-community-ac/',
    '/es/concurso-36-2012-analisis-penal-forense-unitario/',
    '/en/insolvency-36-2012-unitary-criminal-forensic-analysis/',
    '/es/ric-private-equity-sun-park/',
    '/en/ric-private-equity-sun-park/',
    '/es/intervencion-general-siinf-trazabilidad/',
    '/en/intervencion-general-siinf-traceability/',
  ]) {
    const page = await browser.newPage();
    await page.goto(`${base}${path}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    const reciprocal = page.locator('[data-ucf-authority-propagation-link="PD-UCF-20260901-01"]');
    if (await reciprocal.count() !== 1) fail(`${path}: authority-propagation reciprocal control missing`);
    const checkpointHrefs = await reciprocal.locator('a').evaluateAll((nodes) => nodes.map((node) => node.getAttribute('href')));
    if (!checkpointHrefs.some((value) => value?.includes('#unitary-authority-propagation'))) fail(`${path}: authority-propagation anchor missing`);
    if (!checkpointHrefs.some((value) => value?.includes('#evidence-PD-EV-UCF-INT-184368-2026'))) fail(`${path}: Intervención evidence anchor missing`);
    await page.close();
  }

  console.log('Unitary multi-track criminal-first gap-closure browser smoke: PASS');
} finally {
  await browser.close();
}

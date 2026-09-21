import { chromium } from 'playwright';

const base = process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho';
const browser = await chromium.launch({ headless: true });
const fail = (message) => { throw new Error(message); };

try {
  const context = await browser.newContext();
  const dataResponse = await context.request.get(`${base}/assets/data/community-acta-authority-interconnectivity-v1.json`);
  if (!dataResponse.ok()) fail(`dataset returned ${dataResponse.status()}`);
  const data = await dataResponse.json();
  if (data.coverage.public_acta_packages !== 20 || data.coverage.public_authority_files !== 49) fail('finite denominators are not 20 ACTAs / 49 authority files');
  if (data.coverage.evidentiary_axes !== 7 || data.parallel_2022.days_from_acta_to_deed !== 17) fail('axis or 17-day control changed');
  await context.close();

  const routes = [
    {lang:'en',path:'/en/community-actas-public-authorities/',notFinding:'not a finding'},
    {lang:'es',path:'/es/actas-comunidad-autoridades-publicas/',notFinding:'no es una conclusión'},
  ];
  for (const route of routes) {
    const page = await browser.newPage({viewport:{width:1440,height:1000}});
    const errors=[]; page.on('console',m=>{if(m.type()==='error')errors.push(m.text());}); page.on('pageerror',e=>errors.push(e.message));
    const response = await page.goto(`${base}${route.path}#authority=X-INT-004`, {waitUntil:'networkidle'});
    if (!response?.ok()) fail(`${route.lang}: route returned ${response?.status()}`);
    await page.waitForSelector('[data-ca-authority="X-INT-004"]');
    if (await page.locator('.pd-ca-metric').count() !== 6) fail(`${route.lang}: six metrics not rendered`);
    if (await page.locator('[data-ca-axis]').count() !== 7) fail(`${route.lang}: seven axes not rendered`);
    if (await page.locator('[data-ca-milestone]').count() !== 9) fail(`${route.lang}: nine parallel milestones not rendered`);
    if (!(await page.locator('[data-ca-allegation]').innerText()).toLowerCase().includes(route.notFinding)) fail(`${route.lang}: allegation boundary hidden`);
    if (!(await page.locator('[data-ca-authority="X-INT-004"]').innerText()).includes('Intervención General')) fail(`${route.lang}: Intervención file not rendered`);
    await page.locator('[data-ca-authority-search]').fill('');
    if (await page.locator('[data-ca-authority]').count() !== 49) fail(`${route.lang}: all 49 authority files not rendered`);
    await page.locator('[data-ca-group]').selectOption('LOCAL_TOURISM_WORKS');
    if (await page.locator('[data-ca-authority]').count() !== 21) fail(`${route.lang}: local/tourism group denominator changed`);
    await page.locator('[data-ca-group]').selectOption('');
    await page.evaluate(() => { location.hash = '#acta=SP-ACTA-2022-02-04'; });
    await page.waitForSelector('[data-ca-acta="SP-ACTA-2022-02-04"]');
    if (await page.locator('[data-ca-acta]').count() !== 1) fail(`${route.lang}: ACTA deep link did not filter to one record`);
    if (errors.length) fail(`${route.lang}: browser errors: ${errors.join(' | ')}`);
    await page.close();
  }

  const master = await browser.newPage();
  await master.goto(`${base}/en/master-proceedings-register/#record-X-INT-004`, {waitUntil:'networkidle'});
  await master.waitForSelector('[data-master-id="X-INT-004"] [data-community-authority-master-id="X-INT-004"]');
  const masterHref = await master.locator('[data-community-authority-master-id="X-INT-004"]').getAttribute('href');
  if (!masterHref?.includes('/en/community-actas-public-authorities/#authority=X-INT-004')) fail('Master Register reciprocal route is incorrect');
  await master.close();

  const map = await browser.newPage();
  await map.goto(`${base}/en/proceedings-map/#trace-proceeding=NAT-CNMV-001`, {waitUntil:'networkidle'});
  await map.waitForSelector('[data-trace-panel] [data-community-authority-master-id="NAT-CNMV-001"]');
  const mapHref = await map.locator('[data-community-authority-master-id="NAT-CNMV-001"]').getAttribute('href');
  if (!mapHref?.includes('/en/community-actas-public-authorities/#authority=NAT-CNMV-001')) fail('Proceedings Map reciprocal route is incorrect');
  await map.close();

  const acta = await browser.newPage();
  await acta.goto(`${base}/en/community-instrumentalisation/acta-document-room/2022-02-04/`, {waitUntil:'networkidle'});
  await acta.waitForSelector('[data-ca-reciprocal-interlink]');
  const actaHref = await acta.locator('[data-ca-reciprocal-interlink] a').getAttribute('href');
  if (!actaHref?.includes('#acta=SP-ACTA-2022-02-04')) fail('ACTA reciprocal route is incorrect');
  await acta.close();

  console.log('Community ACTA / 2022 / authority browser smoke: PASS');
} finally {
  await browser.close();
}

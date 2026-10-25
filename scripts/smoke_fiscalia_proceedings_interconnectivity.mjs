import { chromium } from 'playwright';
import { createHash } from 'node:crypto';

const base = process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho';
const browser = await chromium.launch({ headless: true });

function fail(message) { throw new Error(message); }

try {
  const context = await browser.newContext();
  const dataResponse = await context.request.get(`${base}/assets/data/fiscalia-proceedings-interconnectivity-v1.json`);
  if (!dataResponse.ok()) fail(`interconnectivity data returned ${dataResponse.status()}`);
  const data = await dataResponse.json();
  const octoberResponse = await context.request.get(`${base}/assets/data/institutional-communications-20261025.json`);
  if (!octoberResponse.ok()) fail(`October descriptor returned ${octoberResponse.status()}`);
  const octoberBytes = await octoberResponse.body();
  const october = JSON.parse(octoberBytes.toString('utf8'));
  const receiptReferences = new Set([
    'REGAGE26e00091776746', 'REGAGE26e00091777235', 'REGAGE26e00091777533',
    'REGAGE26e00091778502', 'REGAGE26e00091804140', 'REGAGE26e00091804303',
  ]);
  if (october.control_id !== 'PD-MADRID-CTBG-REGISTERED-20261025' || october.items.length !== receiptReferences.size || new Set(october.items.map(item => item.reference)).size !== receiptReferences.size || october.items.some(item => !receiptReferences.has(item.reference))) fail('finite October source cohort differs');
  const octoberIds = new Set(october.items.map(item => item.event_id));
  if (octoberIds.size !== receiptReferences.size) fail('October event identities are not distinct');
  const octoberControl = data.october_cohort_control;
  if (octoberControl?.source_descriptor_sha256 !== createHash('sha256').update(octoberBytes).digest('hex') || octoberControl.event_ids.length !== octoberIds.size || octoberControl.event_ids.some(id => !octoberIds.has(id))) fail('October projection source control differs');
  const successorIds = new Set([
    'PD-SP-EVT-0497', 'PD-SP-EVT-0498', 'PD-SP-EVT-0499',
    'PD-SP-EVT-1157', 'PD-SP-EVT-1158', 'PD-SP-EVT-1159',
  ]);
  const projectedIds = new Set(data.events.map(event => event.event_id));
  const legacyEvents = data.events.filter(event => !successorIds.has(event.event_id) && !octoberIds.has(event.event_id));
  if (projectedIds.size !== data.events.length) fail('duplicate projected communication');
  if (legacyEvents.length !== 320 || ![...successorIds].every(id => projectedIds.has(id))) fail('legacy 320 / six successor identities not preserved');
  if (data.coverage.communication_events !== 326 + octoberIds.size || data.events.length !== 326 + octoberIds.size || data.coverage.legacy_communication_events !== 326 || data.coverage.legacy_matter_linked_events !== 141) fail('legacy / October communication denominator mismatch');
  const canonicalResponse = await context.request.get(`${base}/assets/data/institutional-communications-register-v1.json`);
  if (!canonicalResponse.ok()) fail(`canonical register returned ${canonicalResponse.status()}`);
  const canonical = await canonicalResponse.json();
  const octoberCanonical = canonical.events.filter(event => String(event.source_key || '').startsWith('REGISTERED-20261025:') || octoberIds.has(event.event_id) || receiptReferences.has(event.official_reference));
  if (octoberCanonical.length !== octoberIds.size || new Set(octoberCanonical.map(event => event.event_id)).size !== octoberIds.size) fail('October canonical identity count differs');
  for (const item of october.items) {
    const source = octoberCanonical.find(event => event.event_id === item.event_id);
    const projected = data.events.find(event => event.event_id === item.event_id);
    if (!source || !projected || source.official_reference !== item.reference || source.source_key !== `REGISTERED-20261025:${item.reference}` || JSON.stringify(source.matter_references) !== JSON.stringify(item.matter_references) || projected.official_reference !== source.official_reference || JSON.stringify(projected.matter_references) !== JSON.stringify(source.matter_references)) fail('October receipt identity/reference mismatch');
    if (projected.allocation_state !== 'UNRESOLVED_PROCEEDING_ALLOCATION' || projected.proceeding_mapping_state !== 'FISCALIA_AND_TRANSPARENCY_PROCEEDING_ALLOCATION_UNRESOLVED' || !projected.mapping_boundary_en || !projected.mapping_boundary_es || !projected.unresolved_matter_references.length || projected.master_ids.some(id => id !== 'NAT-AID-001')) fail('October proceeding allocation boundary overstated');
  }
  const successors = canonical.events.filter(event => String(event.source_key || '').startsWith('SUPPLEMENTAL_20260924:'));
  if (successors.length !== successorIds.size || new Set(successors.map(event => event.event_id)).size !== successorIds.size || successors.some(event => !successorIds.has(event.event_id))) fail('source-controlled successor cohort differs');
  const platformEvents = canonical.events.filter(event => String(event.source_key || '').startsWith('PD-CPA-20260925-07:'));
  if (platformEvents.length !== 11 || new Set(platformEvents.map(event => event.event_id)).size !== 11 || platformEvents.some(event => projectedIds.has(event.event_id))) fail('platform correspondence incorrectly projected as a Fiscalia filing');
  if (data.coverage.matter_linked_events !== 141 + octoberIds.size || data.coverage.october_registered_events !== octoberIds.size || data.coverage.unresolved_proceeding_allocation_events !== octoberIds.size) fail('legacy / October matter-linked denominator differs');
  if (data.coverage.fiscalia_exact_files !== 23 || data.coverage.fiscalia_unresolved_references !== 3) fail('Fiscalía identity denominator is not 23 + 3');
  const octoberEdges = data.event_proceeding_edges.filter(edge => octoberIds.has(edge.event_id));
  const contextIds = new Set(october.items.filter(item => item.matter_references.includes('GC/836/P06')).map(item => item.event_id));
  if (data.event_proceeding_edges.length - octoberEdges.length !== 164 || data.event_event_edges.length !== 84) fail('legacy graph edge denominator changed');
  if (octoberEdges.length !== contextIds.size || contextIds.size !== 2 || octoberEdges.some(edge => !contextIds.has(edge.event_id) || edge.master_id !== 'NAT-AID-001' || edge.relationship_strength !== 'CONTEXT_OR_CITATION' || edge.operational_scope !== 'OUTSIDE_JUDICIAL_PROCEEDING')) fail('October administrative context promoted to a proceeding allocation');
  if (data.priority_chains.length !== 9) fail('priority-chain denominator is not nine');
  await context.close();

  const routes = [
    { lang: 'en', path: '/en/public-prosecution-communications-proceedings/', gap: 'Next source needed', unresolved: 'Unresolved reference', administrative: 'Administrative public-aid file', administrativeContext: 'Administrative public-aid context outside judicial proceeding', judicial: 'Linked judicial proceedings', outsideFilter: 'Outside judicial proceedings' },
    { lang: 'es', path: '/es/fiscalia-comunicaciones-procedimientos/', gap: 'Fuente siguiente necesaria', unresolved: 'Referencia no resuelta', administrative: 'Expediente administrativo de ayudas', administrativeContext: 'Contexto administrativo de ayudas fuera de procedimiento judicial', judicial: 'Procedimientos judiciales enlazados', outsideFilter: 'Fuera de procedimiento judicial' },
  ];
  for (const route of routes) {
    const page = await browser.newPage({ viewport: { width: 1360, height: 900 } });
    const errors = [];
    page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
    page.on('pageerror', error => errors.push(error.message));
    const response = await page.goto(`${base}${route.path}#file=NAT-FIS-004`, { waitUntil: 'networkidle' });
    if (!response?.ok()) fail(`${route.lang}: specialist route returned ${response?.status()}`);
    await page.waitForSelector('[data-mf-files] [data-file="NAT-FIS-004"][aria-current="true"]');
    if ((await page.locator('[data-mf-scope] option[value="OUTSIDE_JUDICIAL_PROCEEDING"]').textContent()).trim() !== route.outsideFilter) fail(`${route.lang}: outside-proceeding filter excludes administrative context in its label`);
    if (await page.locator('.pd-mf-metric').count() !== 6) fail(`${route.lang}: expected six headline metrics`);
    if (await page.locator('[data-mf-files] [data-file]').count() !== 27) fail(`${route.lang}: expected all + 26 file controls`);
    if (await page.locator('[data-mf-chains] .pd-mf-chain').count() !== 9) fail(`${route.lang}: expected nine priority chains`);
    const detail = page.locator('[data-mf-detail]');
    if (!(await detail.innerText()).includes('NAT-FIS-004')) fail(`${route.lang}: deep-linked file was not rendered`);
    if (!(await detail.innerText()).includes(route.gap)) fail(`${route.lang}: next-source gap is not visible`);
    if (await detail.locator('[data-event-id]').count() < 1) fail(`${route.lang}: linked event chronology is empty`);

    await page.locator('[data-mf-files] [data-file="TF-FIS-009"]').click();
    await page.waitForSelector('[data-mf-files] [data-file="TF-FIS-009"][aria-current="true"]');
    const identityState = detail.locator('.pd-mf-detail-head .eyebrow');
    if (!(await identityState.isVisible()) || !(await identityState.textContent()).includes(route.unresolved)) fail(`${route.lang}: unresolved identity state is hidden`);
    if (!(await detail.innerText()).includes(route.gap)) fail(`${route.lang}: unresolved source gate is hidden`);

    await page.locator('[data-mf-direction]').selectOption('INBOUND_FROM_INSTITUTION');
    await page.locator('[data-mf-direction]').selectOption('');
    await page.locator('[data-mf-scope]').selectOption('OUTSIDE_JUDICIAL_PROCEEDING');
    await page.locator('[data-mf-scope]').selectOption('');
    await page.locator('[data-mf-files] [data-file="ALL"]').click();
    const octoberItem = october.items.find(item => item.reference === 'REGAGE26e00091804140');
    await page.locator('[data-mf-search]').fill(octoberItem.reference);
    const octoberCard = detail.locator(`[data-event-id="${octoberItem.event_id}"]`);
    await octoberCard.waitFor({ state: 'visible' });
    await octoberCard.locator('summary').click();
    if (!(await octoberCard.innerText()).includes('UNRESOLVED_PROCEEDING_ALLOCATION') || !(await octoberCard.innerText()).includes(route.lang === 'es' ? 'no asignan una identidad canónica' : 'do not allocate a canonical')) fail(`${route.lang}: October unresolved proceeding mapping is hidden`);

    await page.goto(`${base}${route.path}#file=NAT-AID-001`, { waitUntil: 'networkidle' });
    await page.waitForSelector('[data-mf-files] [data-file="NAT-AID-001"][aria-current="true"]');
    if ((await detail.locator('.pd-mf-detail-head .eyebrow').innerText()).trim() !== route.administrative || (await page.locator('[data-mf-files] [data-file="NAT-AID-001"] small').innerText()).trim() !== route.administrative) fail(`${route.lang}: public-aid context is mislabeled as a judicial or Fiscalía file`);
    const judicialCount = detail.locator(':scope > .pd-mf-badges > .pd-mf-badge').last();
    if ((await judicialCount.innerText()).trim() !== `0 ${route.judicial}`) fail(`${route.lang}: administrative context inflated the judicial-proceeding count`);
    if (await detail.locator('[data-event-id]').count() !== contextIds.size) fail(`${route.lang}: public-aid context chronology differs from the two exact citation edges`);
    for (const eventId of contextIds) {
      const card = detail.locator(`[data-event-id="${eventId}"]`);
      if (!(await card.locator('.pd-mf-badges').innerText()).includes(route.administrativeContext) || !(await card.innerText()).includes('UNRESOLVED_PROCEEDING_ALLOCATION')) fail(`${route.lang}: context receipt was promoted to a prosecution allocation`);
    }
    if (errors.length) fail(`${route.lang}: browser console errors: ${errors.join(' | ')}`);
    await page.close();
  }

  for (const readerRoute of ['/en/institutional-records/', '/es/registros-institucionales/']) {
    const page = await browser.newPage({ viewport: { width: 1360, height: 900 } });
    const readerResponse = await page.goto(`${base}${readerRoute}`, { waitUntil: 'networkidle' });
    if (!readerResponse?.ok()) fail(`${readerRoute}: institutional reader returned ${readerResponse?.status()}`);
    for (const item of october.items) {
      const card = page.locator(`article#communication-${item.event_id}`);
      if (await card.count() !== 1 || !(await card.isVisible()) || !(await card.innerText()).includes(item.reference)) fail(`${readerRoute}: October receipt is missing, duplicated or absent from the visible DOM: ${item.event_id}`);
    }
    for (const reference of ['REGAGE26e00091804140', 'REGAGE26e00091804303']) {
      const item = october.items.find(entry => entry.reference === reference);
      const target = `communication-${item.event_id}`;
      const response = await page.goto(`${base}${readerRoute}#${target}`, { waitUntil: 'networkidle' });
      if (!response?.ok()) fail(`${readerRoute}: institutional reader returned ${response?.status()}`);
      const card = page.locator(`article#${target}`);
      await card.waitFor({ state: 'visible' });
      if (await card.count() !== 1 || (await card.locator('h3').innerText()).trim() !== reference || !(await card.innerText()).includes(item.event_id)) fail(`${readerRoute}: fragment did not resolve to the identified registration card`);
      const fragmentVisible = await card.evaluate((element, id) => {
        const rect = element.getBoundingClientRect();
        return location.hash === `#${id}` && rect.top < innerHeight && rect.bottom > 0;
      }, target);
      if (!fragmentVisible) fail(`${readerRoute}: ${target} did not scroll into the visible viewport`);
    }
    await page.close();
  }

  const master = await browser.newPage({ viewport: { width: 1360, height: 900 } });
  await master.goto(`${base}/en/master-proceedings-register/#record-GC-FIS-017`, { waitUntil: 'networkidle' });
  await master.waitForSelector('[data-master-id="GC-FIS-017"] [data-fiscalia-master-id="GC-FIS-017"]');
  const masterHref = await master.locator('[data-fiscalia-master-id="GC-FIS-017"]').getAttribute('href');
  if (!masterHref?.includes('/en/public-prosecution-communications-proceedings/#file=GC-FIS-017')) fail('Master Register reciprocal route is incorrect');
  await master.close();

  const map = await browser.newPage({ viewport: { width: 1360, height: 900 } });
  await map.goto(`${base}/en/proceedings-map/#trace-proceeding=GC-CRI-008`, { waitUntil: 'networkidle' });
  await map.waitForSelector('[data-trace-panel] [data-fiscalia-master-id="GC-CRI-008"]');
  const mapHref = await map.locator('[data-trace-panel] [data-fiscalia-master-id="GC-CRI-008"]').getAttribute('href');
  if (!mapHref?.includes('/en/public-prosecution-communications-proceedings/#file=GC-CRI-008')) fail('Proceedings Map reciprocal route is incorrect');
  await map.goto(mapHref, { waitUntil: 'networkidle' });
  await map.waitForSelector('[data-mf-files] [data-file="GC-CRI-008"][aria-current="true"]');
  if (!(await map.locator('[data-mf-detail]').innerText()).includes('GC-CRI-008')) fail('non-Fiscalía proceeding-centred communication view did not render');
  await map.close();

  console.log('Fiscalía interconnectivity browser smoke: PASS — bilingual routes, October receipt fragments and unresolved mapping, deep links, filters and reciprocal navigation verified');
} finally {
  await browser.close();
}

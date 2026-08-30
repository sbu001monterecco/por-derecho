import { chromium } from 'playwright';

const base = process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho';
const routes = [
  { lang: 'en', path: '/en/proceedings-map/', contrary: 'Strongest contrary', sourceScope: 'proposition-level audit path', outsideSelected: 'Outside the selected file', antiJoinder: 'joinder', nextSource: 'Next source needed', notExact: 'not an exact proceeding' },
  { lang: 'es', path: '/es/mapa-procedimientos/', contrary: 'Explicación / registro contrario', sourceScope: 'ruta de auditoría de la proposición', outsideSelected: 'Fuera del expediente seleccionado', antiJoinder: 'acumulación', nextSource: 'Siguiente fuente necesaria', notExact: 'no es un procedimiento exacto' },
];

function assertSameValues(actual, expected, label) {
  const actualSet = new Set(actual);
  const expectedSet = new Set(expected);
  const missing = [...expectedSet].filter((value) => !actualSet.has(value));
  const unexpected = [...actualSet].filter((value) => !expectedSet.has(value));
  if (actual.length !== actualSet.size || missing.length || unexpected.length) {
    throw new Error(`${label}: missing=${missing.join(',') || 'none'} unexpected=${unexpected.join(',') || 'none'} duplicates=${actual.length - actualSet.size}`);
  }
}

function expectedIsolationSets(selectedId, prism, interlinks) {
  const reconnectIds = new Set();
  const linkedPrismPropIds = new Set();

  for (const relationship of interlinks.relationships || []) {
    if (![relationship.from_master_id, relationship.to_master_id].includes(selectedId)) continue;
    reconnectIds.add(relationship.from_master_id);
    reconnectIds.add(relationship.to_master_id);
  }
  for (const cluster of interlinks.context_clusters || []) {
    if (!(cluster.member_master_ids || []).includes(selectedId)) continue;
    if (cluster.context_type === 'CASE_PRISM_PROPOSITION') {
      if (cluster.source?.record_id) linkedPrismPropIds.add(cluster.source.record_id);
    } else if (cluster.context_type === 'RECORDED_CONNECTION') {
      for (const masterId of cluster.member_master_ids || []) reconnectIds.add(masterId);
    } else {
      throw new Error(`${selectedId}: taxonomy-only or unsupported context entered isolation (${cluster.context_type})`);
    }
  }
  reconnectIds.delete(selectedId);

  const directPairs = [];
  const disappearingPropIds = [];
  for (const prop of prism.propositions || []) {
    let hasDisappearingCoordinate = false;
    for (const lane of prism.lanes || []) {
      const cell = prop.cells?.[lane.id];
      const masterIds = Array.isArray(cell?.master_ids) ? cell.master_ids : [];
      const selectedDirect = cell?.status === 'DIRECT' && masterIds.includes(selectedId);
      if (selectedDirect) directPairs.push(`${prop.id}:${lane.id}`);
      if (cell?.status === 'OUTSIDE' || selectedDirect) continue;

      // A selected proposition-cluster contributes only its own proposition,
      // never the coordinates of its co-members.  One-hop direct/Connection
      // neighbours may contribute only DIRECT coordinates; otherwise a broad
      // parent such as GC-JUD-001 makes every proposition appear connected.
      if (
        linkedPrismPropIds.has(prop.id)
        || masterIds.includes(selectedId)
        || (cell?.status === 'DIRECT' && masterIds.some((masterId) => reconnectIds.has(masterId)))
      ) {
        hasDisappearingCoordinate = true;
      }
    }
    if (hasDisappearingCoordinate) disappearingPropIds.push(prop.id);
  }
  return { directPairs, disappearingPropIds };
}

async function assertFocusedAndVisible(page, selector, label) {
  try {
    await page.waitForFunction((target) => {
      const element = document.querySelector(target);
      if (!element || document.activeElement !== element) return false;
      const rect = element.getBoundingClientRect();
      return rect.top >= -10 && rect.top < window.innerHeight * 0.7;
    }, selector, { timeout: 8000 });
  } catch {
    const diagnostic = await page.evaluate((target) => {
      const element = document.querySelector(target);
      const rect = element?.getBoundingClientRect();
      return { active: document.activeElement?.outerHTML?.slice(0, 180) || '', rect: rect ? { top: rect.top, bottom: rect.bottom, height: rect.height } : null };
    }, selector);
    throw new Error(`${label}: target did not become focused and visible (${JSON.stringify(diagnostic)})`);
  }
}

async function assertDeepLinkVisible(page, hash, label) {
  try {
    await page.waitForFunction((targetHash) => {
      const targets = [document.querySelector(targetHash), document.querySelector('[data-view-body]')].filter(Boolean);
      return targets.some((element) => {
        const rect = element.getBoundingClientRect();
        return rect.top >= -10 && rect.top < window.innerHeight * 0.8;
      });
    }, hash, { timeout: 8000 });
  } catch {
    throw new Error(`${label}: neither the canonical anchor nor its active panel entered the viewport`);
  }
}

const browser = await chromium.launch({ headless: true });
try {
  const dataContext = await browser.newContext();
  const projectionResponse = await dataContext.request.get(`${base}/assets/data/proceedings-master-public-v1.json`);
  if (!projectionResponse.ok()) throw new Error(`public proceedings projection failed with ${projectionResponse.status()}`);
  const projection = await projectionResponse.json();
  const publicRecords = Array.isArray(projection.records) ? projection.records : [];
  if (publicRecords.length !== 106) throw new Error(`expected 106 controlled public records, found ${publicRecords.length}`);
  const exactRecords = publicRecords.filter((record) => String(record.Is_Proceeding || '').trim().toUpperCase() === 'TRUE');
  const exactIds = exactRecords.map((record) => record.Master_ID);
  if (exactIds.length !== 85) throw new Error(`expected 85 exact public proceedings after aggregate-family repair, found ${exactIds.length}`);
  if (exactRecords.some((record) => /FAMILY|AGGREGATE/i.test(`${record.Record_Type || ''} ${record.Proceeding_Class || ''}`))) {
    throw new Error('public exact-proceeding denominator admits an aggregate/family object');
  }
  if (exactIds.includes('GC-APP-007')) throw new Error('aggregate removal-appeal family is still admitted as an exact proceeding');
  for (const traceOnlyId of ['GC-REF-031', 'LZ-JUD-042', 'LZ-REF-042', 'LZ-REF-044']) {
    if (!publicRecords.some((record) => record.Master_ID === traceOnlyId)) throw new Error(`${traceOnlyId}: public trace record missing`);
    if (exactIds.includes(traceOnlyId)) throw new Error(`${traceOnlyId}: source-pending record admitted to exact isolation`);
  }

  const interlinkResponse = await dataContext.request.get(`${base}/assets/data/proceedings-interlinkability-v1.json`);
  if (!interlinkResponse.ok()) throw new Error(`interlinkability registry failed with ${interlinkResponse.status()}`);
  const interlinks = await interlinkResponse.json();
  const dispositions = Array.isArray(interlinks.node_dispositions) ? interlinks.node_dispositions : [];
  assertSameValues(dispositions.map((item) => item.master_id), exactIds, 'controlled interlink disposition denominator');
  const dispositionById = new Map(dispositions.map((item) => [item.master_id, item]));
  const relationshipById = new Map((interlinks.relationships || []).map((item) => [item.id, item]));
  const clusterById = new Map((interlinks.context_clusters || []).map((item) => [item.id, item]));
  const dp3205Disposition = dispositionById.get('LZ-JUD-043');
  if (!dp3205Disposition
      || dp3205Disposition.primary_classification !== 'EXPLICIT_RELATIONSHIP_GAP'
      || (dp3205Disposition.relationship_ids || []).length
      || (dp3205Disposition.context_cluster_ids || []).length) {
    throw new Error('LZ-JUD-043 must have one edge-free explicit relationship-gap disposition');
  }
  if ((interlinks.relationships || []).some((item) => item.from_master_id === 'LZ-JUD-043' || item.to_master_id === 'LZ-JUD-043')) {
    throw new Error('LZ-JUD-043 was promoted into a direct relationship');
  }
  if ((interlinks.context_clusters || []).some((item) => (item.member_master_ids || []).includes('LZ-JUD-043'))) {
    throw new Error('LZ-JUD-043 singleton coordinate was promoted into a context cluster');
  }
  if (clusterById.has('CTX-PRISM-P19')) throw new Error('singleton P19 was materialised as a context cluster');
  const prismResponse = await dataContext.request.get(`${base}/assets/data/proceedings-case-prism-v1.json`);
  if (!prismResponse.ok()) throw new Error(`Case Prism data failed with ${prismResponse.status()}`);
  const prismData = await prismResponse.json();
  const p19 = (prismData.propositions || []).find((item) => item.id === 'P19');
  const p19Members = new Set(Object.values(p19?.cells || {}).flatMap((cell) => cell.status === 'OUTSIDE' ? [] : (cell.master_ids || [])));
  if (p19Members.size !== 1 || !p19Members.has('LZ-JUD-043')) throw new Error('P19 must remain a singleton LZ-JUD-043 coordinate');
  const exactIdSet = new Set(exactIds);
  const prismCoveredIds = new Set((prismData.propositions || []).flatMap((prop) =>
    Object.values(prop.cells || {}).flatMap((cell) =>
      cell.status === 'OUTSIDE' ? [] : (cell.master_ids || []).filter((id) => exactIdSet.has(id))
    )
  ));
  if (prismCoveredIds.size !== 25 || exactIds.length - prismCoveredIds.size !== 60) {
    throw new Error(`Case Prism exact-file content denominator mismatch (${prismCoveredIds.size}/${exactIds.length})`);
  }
  const expectedIsolationById = new Map(exactIds.map((masterId) => [
    masterId,
    expectedIsolationSets(masterId, prismData, interlinks),
  ]));
  for (const sampleId of ['GC-FIS-017', 'LZ-JUD-003', 'GC-APP-005']) {
    const sample = expectedIsolationById.get(sampleId);
    if (!sample || sample.disappearingPropIds.length >= prismData.propositions.length) {
      throw new Error(`${sampleId}: bounded one-hop isolation still expands to all ${prismData.propositions.length} propositions`);
    }
  }
  await dataContext.close();

  for (const route of routes) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const consoleErrors = [];
    page.on('console', (message) => { if (message.type() === 'error') consoleErrors.push(message.text()); });
    page.on('pageerror', (error) => consoleErrors.push(error.message));
    const response = await page.goto(`${base}${route.path}`, { waitUntil: 'networkidle' });
    if (!response?.ok()) throw new Error(`${route.lang}: route failed with ${response?.status()}`);

    const tabs = page.locator('[role="tab"]');
    if (await tabs.count() !== 6) throw new Error(`${route.lang}: expected six semantic tabs`);

    const search = page.locator('[data-map-search]');
    await search.fill('GC-APP-004');
    await page.waitForSelector('[data-node-id="GC-APP-004"]');
    await search.fill('');
    const track = page.locator('[data-map-track]');
    await track.selectOption({ index: 1 });
    await track.selectOption('');

    await page.locator('a[href="#case-prism"]').first().click();
    await page.waitForSelector('[role="tab"][data-view="prism"][aria-selected="true"]');
    if (await page.evaluate(() => location.hash) !== '#case-prism') throw new Error(`${route.lang}: Case Prism CTA did not activate the hash view`);
    await assertFocusedAndVisible(page, '[data-view-body]', `${route.lang}: Case Prism CTA`);
    await page.goBack();
    await page.waitForSelector('[role="tab"][data-view="map"][aria-selected="true"]');
    if (await page.evaluate(() => location.hash) !== '') throw new Error(`${route.lang}: browser Back did not restore the map hash state`);
    await page.goForward();
    await page.waitForSelector('[role="tab"][data-view="prism"][aria-selected="true"]');
    await assertFocusedAndVisible(page, '[data-view-body]', `${route.lang}: forward navigation`);

    await page.waitForSelector('.pdim-prism-table tbody tr');
    const matrixRows = await page.locator('.pdim-prism-table tbody tr').count();
    const matrixCells = await page.locator('.pdim-prism-cell').count();
    const laneHeaders = await page.locator('.pdim-prism-table thead th').count();
    if (matrixRows !== 19 || matrixCells !== 228 || laneHeaders !== 13) {
      throw new Error(`${route.lang}: matrix denominator mismatch (${matrixRows} rows, ${matrixCells} cells, ${laneHeaders - 1} lanes)`);
    }
    if (await page.locator('.pdim-prism-dash').count()) throw new Error(`${route.lang}: unexplained matrix dash rendered`);
    if (await page.locator('.pdim-prism-cell small').count() !== 228) throw new Error(`${route.lang}: file-treatment labels missing`);
    const firstEvidenceLabel = await page.locator('.pdim-prism-table tbody th small').first().innerText();
    if (!firstEvidenceLabel || firstEvidenceLabel.includes('_')) throw new Error(`${route.lang}: reader-facing evidence status was not localised`);

    const audience = page.locator('[data-prism-audience]');
    if (await audience.locator('option').count() !== 9) throw new Error(`${route.lang}: audience denominator is not nine`);
    await audience.selectOption('fiscal');
    await page.waitForSelector('.pdim-prism-table tbody tr:first-child');
    const firstFiscal = await page.locator('.pdim-prism-table tbody tr:first-child .pdim-prism-cell').first().getAttribute('data-prism-prop');
    if (firstFiscal !== 'P05') throw new Error(`${route.lang}: Fiscalía lens did not reprioritise the institutional-memory row`);

    await page.locator('.pdim-prism-cell').first().click();
    const detail = page.locator('[data-prism-detail]');
    await assertFocusedAndVisible(page, '[data-view-body] [data-prism-detail]', `${route.lang}: matrix detail`);
    if (await detail.locator('.pdim-dependency-grid > div').count() < 10) throw new Error(`${route.lang}: dependency detail is incomplete`);
    if (await detail.locator('.pdim-source-links a').count() < 1) throw new Error(`${route.lang}: controlled source links missing`);
    if (!(await detail.innerText()).toLowerCase().includes(route.contrary.toLowerCase())) throw new Error(`${route.lang}: contrary record missing from detail`);
    if (!(await detail.innerText()).includes(route.sourceScope)) throw new Error(`${route.lang}: proposition-level source boundary missing`);
    if (await detail.getAttribute('aria-live') !== 'polite') throw new Error(`${route.lang}: detail is not announced`);
    if (await page.locator('[data-proceedings-map] [aria-live="polite"]').count() !== 1) throw new Error(`${route.lang}: duplicate broad live regions remain`);
    const sourceHref = await detail.locator('.pdim-source-links a').first().getAttribute('href');
    if (!sourceHref) throw new Error(`${route.lang}: source href missing`);
    const sourceUrl = new URL(sourceHref);
    if (!sourceUrl.pathname.startsWith(`/por-derecho/${route.lang}/`)) throw new Error(`${route.lang}: source escaped the bilingual repository route (${sourceUrl.pathname})`);
    const sourceResponse = await page.request.get(sourceHref);
    if (!sourceResponse.ok()) throw new Error(`${route.lang}: source route returned ${sourceResponse.status()}`);

    await page.locator('[data-view-body] [data-prism-prop="P04"][data-prism-lane="calificacion"]').click();
    await page.locator('[data-view-body] [data-prism-detail] [data-trace-id="GC-APP-004"]').click();
    await page.waitForSelector('[data-trace-panel] .pdim-prism-trace [data-prism-prop]');
    await assertFocusedAndVisible(page, '[data-trace-panel]', `${route.lang}: Prism-to-trace path`);
    await page.locator('[data-trace-panel] .pdim-prism-trace [data-prism-prop]').first().click();
    await page.waitForSelector('[data-trace-panel] [data-prism-detail] .pdim-prism-detail-head');
    await assertFocusedAndVisible(page, '[data-trace-panel] [data-prism-detail]', `${route.lang}: trace-local dependency detail`);

    const prismTab = page.locator('[role="tab"][data-view="prism"]');
    await prismTab.focus();
    await prismTab.press('ArrowRight');
    await page.waitForSelector('[role="tab"][data-view="lanes"][aria-selected="true"]');
    if (await page.locator('.pdim-swimlane tbody tr').count() !== 19) throw new Error(`${route.lang}: swimlane event denominator mismatch`);
    if (await page.locator('[data-lane-heading]').count() !== 12) throw new Error(`${route.lang}: stable lane headings missing`);
    if (await page.locator('.pdim-swim-cell').count() !== 228) throw new Error(`${route.lang}: swimlane coordinate denominator mismatch`);

    await page.locator('[role="tab"][data-view="isolation"]').click();
    await page.waitForSelector('[data-isolation-id]');
    const isolation = page.locator('[data-isolation-id]');
    const isolationIds = await isolation.locator('option').evaluateAll((options) => options.map((option) => option.value).filter((value) => value !== '__FULL__'));
    assertSameValues(isolationIds, exactIds, `${route.lang}: exact-proceeding isolation denominator`);
    const renderedCoverage = await isolation.locator('option[value]:not([value="__FULL__"])').evaluateAll((options) => options.map((option) => [option.value, option.dataset.prismCoverage]));
    for (const [masterId, status] of renderedCoverage) {
      const expectedStatus = prismCoveredIds.has(masterId) ? 'covered' : 'unresolved';
      if (status !== expectedStatus) throw new Error(`${route.lang}/${masterId}: Case Prism coverage label is ${status}, expected ${expectedStatus}`);
    }
    if (renderedCoverage.filter(([, status]) => status === 'covered').length !== 25 || renderedCoverage.filter(([, status]) => status === 'unresolved').length !== 60) {
      throw new Error(`${route.lang}: visible Case Prism content coverage must remain 25 covered / 60 unresolved`);
    }
    if (await isolation.locator('option[value="GC-APP-007"]').count()) throw new Error(`${route.lang}: aggregate removal-appeal family admitted to isolation`);
    const coverageText = await page.locator('[data-isolation-coverage]').innerText();
    if (!coverageText.includes(`25/${exactIds.length}`) || !coverageText.includes('60')) throw new Error(`${route.lang}: finite 25/85 Case Prism content denominator is not visible`);
    const fullCorpusLabels = await page.locator('.pdim-isolation-map button[aria-label]').evaluateAll((elements) => elements.map((element) => element.getAttribute('aria-label') || ''));
    if (fullCorpusLabels.some((label) => label.includes(route.outsideSelected))) throw new Error(`${route.lang}: full-corpus cells are announced as outside a selected file`);
    if (await isolation.locator('option[value="GC-APP-004"]').count() !== 1) throw new Error(`${route.lang}: exact RPL 2523 option missing`);
    if (await isolation.locator('option[value="LZ-JUD-FAM-006"], option[value="X-TAX-002"]').count()) throw new Error(`${route.lang}: unverified object admitted to exact-proceeding isolation`);
    await isolation.selectOption('GC-APP-004');
    await page.waitForSelector('.pdim-isolation-map[data-isolation-mode="isolated"]');
    if (await page.locator('.pdim-isolation-map .is-suppressed').count() < 1) throw new Error(`${route.lang}: wider corpus did not fade`);
    if (await page.locator('.pdim-isolation-map .is-suppressed button:not([disabled])').count()) throw new Error(`${route.lang}: suppressed cells remain normally focusable`);
    if (await page.locator('.pdim-isolation-map .is-suppressed small').count() !== await page.locator('.pdim-isolation-map .is-suppressed').count()) throw new Error(`${route.lang}: suppressed state lacks a textual equivalent`);
    const suppressedLabels = await page.locator('.pdim-isolation-map .is-suppressed small').allInnerTexts();
    if (suppressedLabels.some((label) => label.trim() !== route.outsideSelected)) throw new Error(`${route.lang}: suppressed-state text is not localised`);
    if (await page.locator('.pdim-isolation-grid > section').count() !== 2) throw new Error(`${route.lang}: isolation comparison missing`);
    const isolationText = await page.locator('[data-view-body]').innerText();
    if (!isolationText.includes('RPL 2523/2025')) throw new Error(`${route.lang}: exact selected identity lost`);
    await page.locator('[data-isolation-restore]').click();
    await page.waitForSelector('.pdim-isolation-map[data-isolation-mode="full"]');
    if (await isolation.inputValue() !== '__FULL__') throw new Error(`${route.lang}: full corpus was not restored`);
    if (await page.locator('.pdim-isolation-map .is-suppressed').count()) throw new Error(`${route.lang}: suppressed cells remain after restore`);

    // Every exact public proceeding must remain selectable and must expose one
    // controlled disposition.  This is deliberately exhaustive rather than a
    // one-file example: a future unclassified proceeding fails both languages.
    for (const exactId of exactIds) {
      const disposition = dispositionById.get(exactId);
      await isolation.selectOption(exactId);
      await page.waitForFunction((selectedId) => {
        const panel = document.querySelector('[data-isolation-reconnection]');
        return panel && panel.textContent.includes(selectedId);
      }, exactId);
      if (await page.evaluate(() => location.hash) !== `#isolation-test=${encodeURIComponent(exactId)}`) {
        throw new Error(`${route.lang}/${exactId}: exact isolation did not produce a stable deep link`);
      }
      if (await page.locator('[data-isolation-reconnection] [data-classification="REGISTRY_NOT_AVAILABLE"]').count()) {
        throw new Error(`${route.lang}/${exactId}: interlink classification unavailable`);
      }
      if (await page.locator(`[data-isolation-unresolved] [data-interlink-disposition][data-classification="${disposition.primary_classification}"]`).count() !== 1) {
        throw new Error(`${route.lang}/${exactId}: controlled disposition not rendered exactly once`);
      }
      if (await page.locator('[data-isolation-direct]').count() !== 1 || await page.locator('[data-isolation-context]').count() !== 1 || await page.locator('[data-isolation-unresolved]').count() !== 1) {
        throw new Error(`${route.lang}/${exactId}: reconnection sections incomplete`);
      }
      const expectedIsolation = expectedIsolationById.get(exactId);
      const renderedVisiblePairs = await page.locator('.pdim-isolation-grid > section:first-child > ul > li > button[data-prism-prop][data-prism-lane]').evaluateAll((buttons) =>
        buttons.map((button) => `${button.dataset.prismProp}:${button.dataset.prismLane}`)
      );
      assertSameValues(renderedVisiblePairs, expectedIsolation.directPairs, `${route.lang}/${exactId}: visible-alone DIRECT proposition/lane set`);
      const renderedActivePairs = await page.locator('.pdim-isolation-map[data-isolation-mode="isolated"] td:not(.is-suppressed) > button[data-prism-status="DIRECT"][data-prism-prop][data-prism-lane]').evaluateAll((buttons) =>
        buttons.map((button) => `${button.dataset.prismProp}:${button.dataset.prismLane}`)
      );
      assertSameValues(renderedActivePairs, expectedIsolation.directPairs, `${route.lang}/${exactId}: active isolation-matrix DIRECT set`);
      const renderedDisappearingProps = await page.locator('.pdim-isolation-grid > section:nth-child(2) > ul > li > button[data-prism-prop][data-prism-lane]').evaluateAll((buttons) =>
        buttons.map((button) => button.dataset.prismProp)
      );
      assertSameValues(renderedDisappearingProps, expectedIsolation.disappearingPropIds, `${route.lang}/${exactId}: disappearing one-hop proposition set`);
      const relationshipIds = disposition.relationship_ids || [];
      const renderedDirect = await page.locator('[data-isolation-direct] [data-interlink-disposition][data-classification="DIRECT_PROCEDURAL_EDGE"]').count();
      if (renderedDirect !== relationshipIds.length || relationshipIds.some((id) => !relationshipById.has(id))) {
        throw new Error(`${route.lang}/${exactId}: direct relationship count/provenance mismatch (${renderedDirect}/${relationshipIds.length})`);
      }
      if (exactId === 'GC-APP-005') {
        const multiSource = page.locator('[data-isolation-direct] [data-source-assertions][data-assertion-count="2"]').filter({ hasText: 'GC-APP-006' });
        if (await multiSource.count() !== 1 || !(await multiSource.innerText()).includes('GC-APP-005')) {
          throw new Error(`${route.lang}/${exactId}: reciprocal RPL 3304/3319 canonical assertions are not both visible in isolation`);
        }
      }
      const clusterIds = disposition.context_cluster_ids || [];
      const renderedContext = await page.locator('[data-isolation-context] [data-interlink-disposition][data-classification="CONTROLLED_CONTEXTUAL_BRIDGE"]').count();
      if (renderedContext !== clusterIds.length || clusterIds.some((id) => !clusterById.has(id))) {
        throw new Error(`${route.lang}/${exactId}: contextual bridge count/provenance mismatch (${renderedContext}/${clusterIds.length})`);
      }
      if (clusterIds.length) {
        const warning = (await page.locator('[data-isolation-context] .pdim-warning').innerText()).toLowerCase();
        if (!warning.includes(route.antiJoinder.toLowerCase())) throw new Error(`${route.lang}/${exactId}: contextual bridge omits anti-joinder boundary`);
      }
      if (disposition.primary_classification === 'EXPLICIT_RELATIONSHIP_GAP') {
        const gapText = await page.locator('[data-isolation-unresolved]').innerText();
        if (!gapText.includes(route.nextSource)) throw new Error(`${route.lang}/${exactId}: explicit relationship gap omits the next source needed`);
      }
    }
    await page.locator('[data-isolation-restore]').click();
    await page.waitForSelector('.pdim-isolation-map[data-isolation-mode="full"]');

    await page.locator('[role="tab"][data-view="trace"]').click();
    const trace = page.locator('[data-trace-select]');
    const traceIds = await trace.locator('option').evaluateAll((options) => options.map((option) => option.value).filter(Boolean));
    assertSameValues(traceIds, publicRecords.map((record) => record.Master_ID), `${route.lang}: public-record trace denominator`);
    for (const exactId of exactIds) {
      await trace.selectOption(exactId);
      await page.waitForFunction((selectedId) => document.querySelector('[data-trace-panel]')?.textContent.includes(selectedId), exactId);
      if (await page.evaluate(() => location.hash) !== `#trace-proceeding=${encodeURIComponent(exactId)}`) {
        throw new Error(`${route.lang}/${exactId}: trace did not produce a stable deep link`);
      }
      if (await page.locator(`[data-trace-panel] .pdim-trace-disposition[data-classification="${dispositionById.get(exactId).primary_classification}"]`).count() !== 1) {
        throw new Error(`${route.lang}/${exactId}: trace does not expose its controlled disposition`);
      }
      const masterHref = await page.locator('[data-trace-panel] .pdim-record-backlink a').getAttribute('href');
      if (!masterHref || !masterHref.endsWith(`#record-${encodeURIComponent(exactId)}`)) {
        throw new Error(`${route.lang}/${exactId}: trace lacks its reciprocal Master Register row link`);
      }
      if (await page.locator('[data-trace-panel] .pdim-warning').count() !== 1) throw new Error(`${route.lang}/${exactId}: trace omits the contextual anti-joinder warning`);
      const traceWarning = (await page.locator('[data-trace-panel] .pdim-warning').innerText()).toLowerCase();
      if (!traceWarning.includes(route.antiJoinder.toLowerCase())) throw new Error(`${route.lang}/${exactId}: trace warning omits anti-joinder language`);
      if (exactId === 'GC-APP-005') {
        const multiSource = page.locator('[data-trace-panel] [data-source-assertions][data-assertion-count="2"]').filter({ hasText: 'GC-APP-006' });
        if (await multiSource.count() !== 1 || !(await multiSource.innerText()).includes('GC-APP-005')) {
          throw new Error(`${route.lang}/${exactId}: reciprocal RPL 3304/3319 canonical assertions are not both visible in trace`);
        }
      }
    }
    if (!traceIds.includes('GC-APP-007')) throw new Error(`${route.lang}: aggregate family reference is not independently traceable as a public record`);
    await trace.selectOption('GC-APP-007');
    await page.waitForSelector('[data-trace-panel] [data-classification="NOT_EXACT_PROCEEDING_RECORD"]');
    if (await page.locator('[data-trace-panel] [data-classification="DIRECT_PROCEDURAL_EDGE"]').count()) {
      throw new Error(`${route.lang}/GC-APP-007: aggregate family trace inferred a direct procedural edge`);
    }
    const notExactText = (await page.locator('[data-trace-panel] [data-classification="NOT_EXACT_PROCEEDING_RECORD"]').innerText()).toLowerCase();
    if (!notExactText.includes(route.notExact.toLowerCase())) throw new Error(`${route.lang}/GC-APP-007: not-exact boundary missing`);
    if (await page.evaluate(() => location.hash) !== '#trace-proceeding=GC-APP-007') throw new Error(`${route.lang}/GC-APP-007: public-record trace deep link missing`);
    await trace.selectOption('GC-APP-004');
    await page.waitForSelector('.pdim-prism-trace [data-prism-prop]');

    await page.setViewportSize({ width: 390, height: 844 });
    await page.locator('[role="tab"][data-view="prism"]').click();
    const stickyWidth = await page.locator('.pdim-prism-table tbody th').first().evaluate((element) => element.getBoundingClientRect().width);
    if (stickyWidth > 205) throw new Error(`${route.lang}: mobile sticky proposition column is too wide (${stickyWidth})`);
    const scrollable = await page.locator('.pdim-prism-table-wrap').evaluate((element) => element.scrollWidth > element.clientWidth);
    if (!scrollable) throw new Error(`${route.lang}: mobile matrix is not horizontally navigable`);
    if (consoleErrors.length) throw new Error(`${route.lang}: console errors: ${consoleErrors.join(' | ')}`);

    await page.close();

    for (const [hash, view] of [['#case-prism', 'prism'], ['#parallel-lanes', 'lanes'], ['#isolation-test', 'isolation']]) {
      const deepLinkPage = await browser.newPage({ viewport: { width: 1280, height: 900 } });
      const deepResponse = await deepLinkPage.goto(`${base}${route.path}${hash}`, { waitUntil: 'networkidle' });
      if (!deepResponse?.ok()) throw new Error(`${route.lang}: direct ${hash} load failed with ${deepResponse?.status()}`);
      await deepLinkPage.waitForSelector(`[role="tab"][data-view="${view}"][aria-selected="true"]`);
      await assertDeepLinkVisible(deepLinkPage, hash, `${route.lang}: direct ${hash}`);
      await deepLinkPage.close();
    }
    const parameterizedCases = [
      { hash: '#trace-proceeding=GC-APP-004', view: 'trace', select: '[data-trace-select]', panel: '[data-trace-panel]', id: 'GC-APP-004' },
      { hash: '#isolation-test=GC-FIS-017', view: 'isolation', select: '[data-isolation-id]', panel: '[data-isolation-reconnection]', id: 'GC-FIS-017' },
      { hash: '#trace-proceeding=LZ-JUD-043', view: 'trace', select: '[data-trace-select]', panel: '[data-trace-panel]', id: 'LZ-JUD-043', dossier: true },
      { hash: '#isolation-test=LZ-JUD-043', view: 'isolation', select: '[data-isolation-id]', panel: '[data-isolation-reconnection]', id: 'LZ-JUD-043' },
      { hash: '#trace-proceeding=GC-APP-007', view: 'trace', select: '[data-trace-select]', panel: '[data-trace-panel]', id: 'GC-APP-007', notExact: true },
    ];
    for (const coldCase of parameterizedCases) {
      const coldPage = await browser.newPage({ viewport: { width: 1280, height: 900 } });
      const coldResponse = await coldPage.goto(`${base}${route.path}${coldCase.hash}`, { waitUntil: 'networkidle' });
      if (!coldResponse?.ok()) throw new Error(`${route.lang}: cold load ${coldCase.hash} failed with ${coldResponse?.status()}`);
      await coldPage.waitForSelector(`[role="tab"][data-view="${coldCase.view}"][aria-selected="true"]`);
      await coldPage.waitForSelector(coldCase.panel);
      if (await coldPage.evaluate(() => location.hash) !== coldCase.hash) throw new Error(`${route.lang}: cold load did not preserve ${coldCase.hash}`);
      if (await coldPage.locator(coldCase.select).inputValue() !== coldCase.id) throw new Error(`${route.lang}: cold load did not select ${coldCase.id}`);
      const coldIdentity = await coldPage.locator(coldCase.panel).innerText();
      if (!coldIdentity.includes(coldCase.id) || !(await coldPage.locator(coldCase.panel).isVisible())) {
        throw new Error(`${route.lang}: cold load did not expose the visible identity ${coldCase.id}`);
      }
      if (coldCase.dossier) {
        const expectedDossier = new URL(`${base}/${route.lang === 'es' ? 'es/dp-3205-2014-arrecife/' : 'en/dp-3205-2014-arrecife/'}`).href;
        const dossierHref = await coldPage.locator(`${coldCase.panel} a.pdim-detail-link`).first().getAttribute('href');
        if (new URL(dossierHref || '', `${base}/`).href !== expectedDossier) throw new Error(`${route.lang}/LZ-JUD-043: map dossier link mismatch`);
      }
      if (coldCase.notExact) {
        const boundary = coldPage.locator('[data-trace-panel] [data-classification="NOT_EXACT_PROCEEDING_RECORD"]');
        if (await boundary.count() !== 1 || !(await boundary.innerText()).toLowerCase().includes(route.notExact.toLowerCase())) {
          throw new Error(`${route.lang}/${coldCase.id}: cold-load not-exact boundary missing`);
        }
      }
      await coldPage.close();
    }

    const invalidIsolationPage = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const invalidIsolationResponse = await invalidIsolationPage.goto(`${base}${route.path}#isolation-test=GC-APP-007`, { waitUntil: 'networkidle' });
    if (!invalidIsolationResponse?.ok()) throw new Error(`${route.lang}: aggregate isolation cold load failed with ${invalidIsolationResponse?.status()}`);
    await invalidIsolationPage.waitForSelector('[role="tab"][data-view="trace"][aria-selected="true"]');
    await invalidIsolationPage.waitForSelector('[data-trace-panel] [data-classification="NOT_EXACT_PROCEEDING_RECORD"]');
    if (await invalidIsolationPage.locator('[data-trace-select]').inputValue() !== 'GC-APP-007') {
      throw new Error(`${route.lang}: invalid aggregate isolation hash did not route to the aggregate trace`);
    }
    if (await invalidIsolationPage.evaluate(() => location.hash) !== '#trace-proceeding=GC-APP-007') {
      throw new Error(`${route.lang}: invalid aggregate isolation hash was not canonicalised`);
    }
    await invalidIsolationPage.evaluate(() => { location.hash = '#map'; });
    await invalidIsolationPage.waitForSelector('[role="tab"][data-view="map"][aria-selected="true"]');
    await invalidIsolationPage.evaluate(() => { location.hash = '#isolation-test=GC-APP-007'; });
    await invalidIsolationPage.waitForSelector('[role="tab"][data-view="trace"][aria-selected="true"]');
    await invalidIsolationPage.waitForFunction(() => location.hash === '#trace-proceeding=GC-APP-007');
    if (await invalidIsolationPage.locator('[data-trace-select]').inputValue() !== 'GC-APP-007') {
      throw new Error(`${route.lang}: hashchange aggregate isolation did not route to the aggregate trace`);
    }
    await invalidIsolationPage.close();

    const masterPath = route.lang === 'es' ? '/es/registro-maestro-procedimientos/' : '/en/master-proceedings-register/';
    const masterPage = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const masterResponse = await masterPage.goto(`${base}${masterPath}`, { waitUntil: 'networkidle' });
    if (!masterResponse?.ok()) throw new Error(`${route.lang}: Master Register failed with ${masterResponse?.status()}`);
    await masterPage.waitForSelector('tr[data-master-id]');
    const renderedMasterIds = await masterPage.locator('tr[data-master-id]').evaluateAll((rows) => rows.map((row) => row.dataset.masterId));
    assertSameValues(renderedMasterIds, publicRecords.map((record) => record.Master_ID), `${route.lang}: Master Register public denominator`);
    if (renderedMasterIds.length !== 106) throw new Error(`${route.lang}: Master Register must render 106 controlled public rows`);
    const masterTraceLinks = await masterPage.locator('tr[data-master-id]').evaluateAll((rows) => rows.map((row) => ({
      masterId: row.dataset.masterId,
      href: row.querySelector('a.pd-ref')?.href || '',
    })));
    for (const { masterId, href } of masterTraceLinks) {
      const expectedHref = new URL(`${base}${route.path}#trace-proceeding=${encodeURIComponent(masterId)}`).href;
      if (href !== expectedHref) throw new Error(`${route.lang}/${masterId}: Master row trace target mismatch (${href || 'missing'})`);
    }
    const traceOnlyRelationText = await masterPage.locator('tr[data-master-id="LZ-JUD-042"] td').nth(7).innerText();
    if (!traceOnlyRelationText.toLowerCase().includes(route.lang === 'es' ? 'sólo navegación/contexto' : 'navigation/context only')) {
      throw new Error(`${route.lang}/LZ-JUD-042: linked reference IDs lack the non-exact navigation-only qualification`);
    }
    const expectedDossier = new URL(`${base}/${route.lang === 'es' ? 'es/dp-3205-2014-arrecife/' : 'en/dp-3205-2014-arrecife/'}`).href;
    const masterDossierLink = masterPage.locator('tr[data-master-id="LZ-JUD-043"] a.pd-detail');
    const masterDossierHref = await masterDossierLink.getAttribute('href');
    if (new URL(masterDossierHref || '', `${base}/`).href !== expectedDossier) throw new Error(`${route.lang}/LZ-JUD-043: Master dossier link mismatch`);
    const expectedLineageDossier = new URL(`${base}/${route.lang === 'es' ? 'es/arrecife-1103-2018-cadena-procesal/' : 'en/arrecife-1103-2018-procedural-lineage/'}`).href;
    for (const lineageId of ['LZ-JUD-003', 'LZ-APP-004']) {
      const lineageHref = await masterPage.locator(`tr[data-master-id="${lineageId}"] a.pd-detail`).getAttribute('href');
      if (new URL(lineageHref || '', `${base}/`).href !== expectedLineageDossier) {
        throw new Error(`${route.lang}/${lineageId}: Arrecife lineage dossier link mismatch`);
      }
    }
    if (await masterPage.locator('tr[data-master-id="LZ-JUD-003"] td').nth(7).locator('a[href="#record-LZ-APP-004"]').count() !== 1) {
      throw new Error(`${route.lang}/LZ-JUD-003: reciprocal appeal row link missing`);
    }
    if (await masterPage.locator('tr[data-master-id="LZ-APP-004"] td').nth(7).locator('a[href="#record-LZ-JUD-003"]').count() !== 1) {
      throw new Error(`${route.lang}/LZ-APP-004: reciprocal origin row link missing`);
    }
    const masterIsolationLinks = await masterPage.locator('[data-isolation-master-id]').evaluateAll((links) => links.map((link) => ({
      masterId: link.dataset.isolationMasterId,
      href: link.href,
    })));
    assertSameValues(masterIsolationLinks.map((link) => link.masterId), exactIds, `${route.lang}: Master Register exact isolation-link denominator`);
    for (const { masterId, href } of masterIsolationLinks) {
      const expectedHref = new URL(`${base}${route.path}#isolation-test=${encodeURIComponent(masterId)}`).href;
      if (href !== expectedHref) throw new Error(`${route.lang}/${masterId}: Master row isolation target mismatch (${href || 'missing'})`);
    }
    const [masterDossierResponse] = await Promise.all([
      masterPage.waitForNavigation({ waitUntil: 'networkidle' }),
      masterDossierLink.click(),
    ]);
    if (!masterDossierResponse?.ok() || masterPage.url() !== expectedDossier) {
      throw new Error(`${route.lang}/LZ-JUD-043: Master dossier navigation failed (${masterDossierResponse?.status() || 'no response'})`);
    }
    await masterPage.waitForSelector('main h1');
    if (!(await masterPage.locator('main h1').innerText()).includes('3205/2014')) {
      throw new Error(`${route.lang}/LZ-JUD-043: Master dossier navigation reached the wrong record`);
    }
    await masterPage.close();

    const coldMaster = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const coldMasterHash = '#record-GC-APP-004';
    const coldMasterResponse = await coldMaster.goto(`${base}${masterPath}${coldMasterHash}`, { waitUntil: 'networkidle' });
    if (!coldMasterResponse?.ok()) throw new Error(`${route.lang}: Master cold load failed with ${coldMasterResponse?.status()}`);
    await coldMaster.waitForSelector('tr#record-GC-APP-004[data-master-id="GC-APP-004"]');
    if (await coldMaster.evaluate(() => location.hash) !== coldMasterHash) throw new Error(`${route.lang}: Master cold load did not preserve ${coldMasterHash}`);
    await assertFocusedAndVisible(coldMaster, 'tr#record-GC-APP-004[data-master-id="GC-APP-004"]', `${route.lang}: Master exact-row cold load`);
    await coldMaster.close();

    const legacyMaster = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const legacyMasterResponse = await legacyMaster.goto(`${base}${masterPath}#case-LZ-JUD-003`, { waitUntil: 'networkidle' });
    if (!legacyMasterResponse?.ok()) throw new Error(`${route.lang}: legacy Master row link failed with ${legacyMasterResponse?.status()}`);
    await legacyMaster.waitForSelector('tr#record-LZ-JUD-003[data-master-id="LZ-JUD-003"]');
    await assertFocusedAndVisible(legacyMaster, 'tr#record-LZ-JUD-003[data-master-id="LZ-JUD-003"]', `${route.lang}: legacy Master row compatibility`);
    await legacyMaster.close();

    console.log(`${route.lang}: 228-cell Case Prism / swimlane / exact isolation / trace / mobile smoke PASS`);
  }
} finally {
  await browser.close();
}

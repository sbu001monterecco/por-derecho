import { chromium } from 'playwright';

const base = process.env.PSR_BASE_URL || 'http://127.0.0.1:8000/por-derecho';
const routes = [
  {
    lang: 'en', path: '/en/proceedings-map/', contrary: 'Strongest contrary', sourceScope: 'proposition-level audit path',
    outsideSelected: 'Outside the selected file', antiJoinder: 'joinder', nextSource: 'Next source needed', notExact: 'not an exact proceeding',
    auditBoundary: 'Audit coverage means', positiveEvidence: 'Separate positive evidence', receiptBoundary: 'RECEIVED ≠ INCORPORATED IN FILE ≠ EXAMINED ≠ USED IN A DECISION',
    actorBoundary: 'Institutional receipt does not by itself prove', noUnitaryAcknowledgement: 'No unitary acknowledgement has been located in the controlled corpus.', headlineFinite: '97 of 97', headlineForbidden: 'Every materially connected file',
  },
  {
    lang: 'es', path: '/es/mapa-procedimientos/', contrary: 'Explicación / registro contrario', sourceScope: 'ruta de auditoría de la proposición',
    outsideSelected: 'Fuera del expediente seleccionado', antiJoinder: 'acumulación', nextSource: 'Siguiente fuente necesaria', notExact: 'no es un procedimiento exacto',
    auditBoundary: 'La cobertura de auditoría significa', positiveEvidence: 'Prueba positiva separada', receiptBoundary: 'RECIBIDO ≠ INCORPORADO AL EXPEDIENTE ≠ EXAMINADO ≠ UTILIZADO EN UNA DECISIÓN',
    actorBoundary: 'La recepción institucional no prueba por sí sola', noUnitaryAcknowledgement: 'No se ha localizado un reconocimiento unitario en el corpus controlado.', headlineFinite: '97 de 97', headlineForbidden: 'Todos los expedientes materialmente conectados',
  },
];

const receiptAxisAttributes = [
  ['transmission', 'data-transmission-status', 'transmission_status'],
  ['registration', 'data-registration-status', 'registration_status'],
  ['file-incorporation', 'data-file-incorporation-status', 'file_incorporation_status'],
  ['recipient-attribution', 'data-recipient-attribution-status', 'recipient_attribution_status'],
  ['examination', 'data-examination-status', 'substantive_examination_status'],
  ['decision-use', 'data-decision-use-status', 'decision_use_status'],
];

const fiscaliaAxisFields = [
  'transmission_status', 'material_received_status', 'referral_status', 'registration_status',
  'file_incorporation_status', 'recipient_attribution_status', 'substantive_examination_status',
  'decision_use_status', 'cross_file_acknowledgement_status',
];

const representativeFiniteIds = {
  directAndContext: 'LZ-TRA-027',
  contextOnly: 'LZ-TUR-008',
  explicitGap: 'CAN-OMB-001',
  fiscaliaProfile: 'NAT-FIS-004',
};

function assertSameValues(actual, expected, label) {
  const actualSet = new Set(actual);
  const expectedSet = new Set(expected);
  const missing = [...expectedSet].filter((value) => !actualSet.has(value));
  const unexpected = [...actualSet].filter((value) => !expectedSet.has(value));
  if (actual.length !== actualSet.size || missing.length || unexpected.length) {
    throw new Error(`${label}: missing=${missing.join(',') || 'none'} unexpected=${unexpected.join(',') || 'none'} duplicates=${actual.length - actualSet.size}`);
  }
}

function bilingualValue(value, lang) {
  if (typeof value === 'string') return value.trim();
  if (!value || typeof value !== 'object') return '';
  return String(value[lang] || value[`${lang === 'en' ? 'en' : 'es'}`] || '').trim();
}

function requireBilingual(value, label) {
  for (const lang of ['en', 'es']) {
    if (!bilingualValue(value, lang)) throw new Error(`${label}: missing ${lang} text`);
  }
}

function requireAxisBasis(basis, status, label) {
  if (!basis || basis.status !== status || !basis.basis_kind || !basis.source?.kind || !basis.source?.record_id) {
    throw new Error(`${label}: axis status/basis/source mismatch`);
  }
  requireBilingual({en: basis.basis_en, es: basis.basis_es}, `${label}: basis`);
  requireBilingual({en: basis.limitation_en, es: basis.limitation_es}, `${label}: limitation`);
}

async function assertFilterScope(page, applies, route, view) {
  const scope = page.locator('[data-filter-scope="map-chronology"]');
  if (await scope.count() !== 1) throw new Error(`${route.lang}/${view}: filter-scope container missing`);
  const hidden = await scope.isHidden();
  const searchDisabled = await page.locator('[data-map-search]').isDisabled();
  const trackDisabled = await page.locator('[data-map-track]').isDisabled();
  if (applies ? (hidden || searchDisabled || trackDisabled) : (!hidden || !searchDisabled || !trackDisabled)) {
    throw new Error(`${route.lang}/${view}: search/track scope is ambiguous (hidden=${hidden}, searchDisabled=${searchDisabled}, trackDisabled=${trackDisabled})`);
  }
}

function isPositiveReceiptStatus(value) {
  const token = String(value || '').trim().toUpperCase();
  return ['DOCUMENTED', 'PARTLY_DOCUMENTED', 'ROUTING_DOCUMENTED'].includes(token);
}

function expectedFiniteRelatedIds(masterId, disposition, interlinks) {
  const relationships = new Map((interlinks.relationships || []).map((item) => [item.id, item]));
  const clusters = new Map((interlinks.context_clusters || []).map((item) => [item.id, item]));
  const direct = (disposition.relationship_ids || []).map((relationshipId) => {
    const relationship = relationships.get(relationshipId);
    if (!relationship) throw new Error(`${masterId}: finite test references missing relationship ${relationshipId}`);
    return relationship.from_master_id === masterId ? relationship.to_master_id : relationship.from_master_id;
  });
  const context = (disposition.context_cluster_ids || []).flatMap((clusterId) => {
    const cluster = clusters.get(clusterId);
    if (!cluster) throw new Error(`${masterId}: finite test references missing context cluster ${clusterId}`);
    return (cluster.member_master_ids || []).filter((candidate) => candidate !== masterId);
  });
  return {direct: [...new Set(direct)].sort(), context: [...new Set(context)].sort()};
}

function assertFiniteTestData(masterId, disposition, interlinks) {
  const test = disposition?.finite_test;
  if (!test || typeof test !== 'object') throw new Error(`${masterId}: finite_test object missing`);
  if (test.id !== `FT-${masterId}`) throw new Error(`${masterId}: finite-test ID mismatch (${test.id || 'missing'})`);
  if (!test.family_template_id || test.family_taxonomy_only !== true) throw new Error(`${masterId}: finite-test family is missing or was promoted beyond taxonomy`);
  if (!test.recorded_object || !test.attribution || !Array.isArray(test.source_refs) || !test.source_refs.length) {
    throw new Error(`${masterId}: finite-test recorded object, attribution or source route is incomplete`);
  }
  for (const [index, sourceRef] of test.source_refs.entries()) {
    if (!sourceRef?.kind || !sourceRef?.status) throw new Error(`${masterId}: finite source reference ${index + 1} lacks kind/status`);
    requireBilingual({en: sourceRef.label_en, es: sourceRef.label_es}, `${masterId}: finite source reference ${index + 1}`);
  }
  requireBilingual(test.question, `${masterId}: finite question`);
  requireBilingual(test.source_needed, `${masterId}: source needed`);
  if (!test.current_source_status || !test.source_needed_status) throw new Error(`${masterId}: finite source status fields missing`);
  if (!test.competent_organ?.recorded_candidate || !test.competent_organ?.status || !test.competent_organ?.basis_field) {
    throw new Error(`${masterId}: recorded candidate organ/custodian control is incomplete`);
  }
  const contrary = test.strongest_contrary_explanation || test.contrary_explanation;
  requireBilingual(contrary, `${masterId}: strongest contrary explanation`);
  const contraryEn = bilingualValue(contrary, 'en');
  const contraryEs = bilingualValue(contrary, 'es');
  if (!contraryEn.includes('strongest hypothetical innocent or contrary explanation could be')
      || !contraryEn.includes('only if the primary record establishes that the legally competent organ applied it')
      || !contraryEn.includes('No act is attributed by this model to the recorded candidate')
      || !contraryEs.includes('explicación inocente o contraria hipotética más fuerte podría ser')
      || !contraryEs.includes('solo si la fuente primaria acredita que el órgano legalmente competente la aplicó')
      || !contraryEs.includes('Este modelo no atribuye actuación alguna al candidato registrado')) {
    throw new Error(`${masterId}: strongest contrary explanation is not hypothetical, competence-conditional and attribution-safe in both languages`);
  }
  requireBilingual(test.decision_dependency, `${masterId}: decision dependency`);
  requireBilingual(test.procedural_availability, `${masterId}: procedural availability`);
  requireBilingual(test.if_confirmed, `${masterId}: consequence if confirmed`);
  requireBilingual(test.if_refuted, `${masterId}: consequence if refuted`);
  const confirmedEn = bilingualValue(test.if_confirmed, 'en');
  const confirmedEs = bilingualValue(test.if_confirmed, 'es');
  const refutedEn = bilingualValue(test.if_refuted, 'en');
  const refutedEs = bilingualValue(test.if_refuted, 'es');
  if (!confirmedEn.startsWith('If the requested primary record confirms')
      || !confirmedEn.includes('the legally competent organ could determine within its powers')
      || !confirmedEn.includes('is not treated as competent merely because it is named in the register')
      || !confirmedEn.includes('Confirmation remains file-specific and does not establish')
      || !confirmedEs.startsWith('Si la fuente primaria solicitada confirma')
      || !confirmedEs.includes('el órgano legalmente competente podría determinar dentro de sus potestades')
      || !confirmedEs.includes('no se considera competente por el mero hecho de figurar en el registro')
      || !confirmedEs.includes('La confirmación sigue siendo específica del expediente y no acredita')) {
    throw new Error(`${masterId}: confirmed consequence is not authority-safe, conditional and file-specific in both languages`);
  }
  if (!refutedEn.startsWith('If the primary record refutes')
      || !refutedEn.includes('assessment by the legally competent organ of any file-specific consequence')
      || !refutedEn.includes('is not treated as competent or required to act by this model')
      || !refutedEs.startsWith('Si la fuente primaria refuta')
      || !refutedEs.includes('que el órgano legalmente competente valore cualquier consecuencia específica del expediente')
      || !refutedEs.includes('Este modelo no considera competente ni obliga a actuar al candidato registrado')) {
    throw new Error(`${masterId}: refuted consequence is not authority-safe, conditional and file-specific in both languages`);
  }
  if (!test.navigation?.controlled_trace_fragment?.endsWith(masterId)
      || !test.navigation?.controlled_isolation_fragment?.endsWith(masterId)
      || test.navigation?.controlled_navigation_status !== 'AVAILABLE') {
    throw new Error(`${masterId}: controlled finite-test navigation is incomplete`);
  }

  const expectedRelated = expectedFiniteRelatedIds(masterId, disposition, interlinks);
  assertSameValues(test.related_proceedings?.direct_master_ids || [], expectedRelated.direct, `${masterId}: finite direct-related IDs`);
  assertSameValues(test.related_proceedings?.context_master_ids || [], expectedRelated.context, `${masterId}: finite context-related IDs`);
  assertSameValues(test.related_proceedings?.context_cluster_ids || [], disposition.context_cluster_ids || [], `${masterId}: finite context-cluster provenance`);

  const receipt = test.receipt_knowledge;
  if (!receipt?.classification || !receipt.institutional_axes || !receipt.actor_specific) throw new Error(`${masterId}: receipt/knowledge classification missing`);
  const axisKeys = receiptAxisAttributes.map(([, , dataKey]) => dataKey);
  assertSameValues(Object.keys(receipt.institutional_axes), axisKeys, `${masterId}: six institutional receipt axes`);
  for (const axisKey of axisKeys) {
    if (!receipt.institutional_axes[axisKey]) throw new Error(`${masterId}: ${axisKey} has no controlled status`);
  }
  assertSameValues(Object.keys(receipt.institutional_axis_basis || {}), fiscaliaAxisFields, `${masterId}: nine institutional axis bases`);
  for (const axisKey of fiscaliaAxisFields) {
    const status = axisKey === 'material_received_status'
      ? receipt.institutional_axis_basis[axisKey]?.status
      : axisKey === 'referral_status'
        ? receipt.institutional_axis_basis[axisKey]?.status
        : axisKey === 'cross_file_acknowledgement_status'
          ? receipt.cross_file_acknowledgement_status
          : receipt.institutional_axes[axisKey];
    requireAxisBasis(receipt.institutional_axis_basis[axisKey], status, `${masterId}: ${axisKey}`);
  }
  if (!receipt.actor_specific.receipt_status || !receipt.actor_specific.knowledge_status || !receipt.actor_specific.source_status) {
    throw new Error(`${masterId}: actor-specific receipt/knowledge boundary is incomplete`);
  }
  if (!receipt.cross_file_acknowledgement_status || !Array.isArray(receipt.source_profile_ids) || !Array.isArray(receipt.event_refs)) {
    throw new Error(`${masterId}: receipt source-profile/event/cross-file controls are incomplete`);
  }
  requireBilingual({en: receipt.actor_specific.boundary_en, es: receipt.actor_specific.boundary_es}, `${masterId}: actor-specific boundary`);
  requireBilingual({en: receipt.limitations_en, es: receipt.limitations_es}, `${masterId}: institutional receipt limitation`);
  return {
    receiptPositive: Object.values(receipt.institutional_axes).some(isPositiveReceiptStatus),
    actorPositive: isPositiveReceiptStatus(receipt.actor_specific.source_status),
  };
}

async function assertFinitePanel(page, rootSelector, masterId, route, disposition, interlinks) {
  const panelSelector = `${rootSelector} [data-finite-test-panel][data-master-id="${masterId}"]`;
  const panel = page.locator(panelSelector);
  if (await panel.count() !== 1) throw new Error(`${route.lang}/${masterId}: expected one finite-test panel in ${rootSelector}`);
  if (await panel.getAttribute('data-finite-test-status') !== 'AUDITED') throw new Error(`${route.lang}/${masterId}: finite-test panel is not audited`);
  for (const selector of [
    '[data-finite-question]', '[data-finite-recorded-object]', '[data-finite-attribution]', '[data-finite-source-status]', '[data-finite-contrary]',
    '[data-finite-competent-organ]', '[data-finite-decision-dependency]', '[data-finite-related]',
    '[data-finite-if-confirmed]', '[data-finite-if-refuted]', '[data-institutional-receipt-treatment]',
    '[data-actor-specific-knowledge]',
  ]) {
    if (await panel.locator(selector).count() !== 1) throw new Error(`${route.lang}/${masterId}: finite panel missing unique ${selector}`);
  }
  if (await panel.locator('[data-finite-recorded-object]').getAttribute('data-recorded-object') !== disposition.finite_test.recorded_object
      || await panel.locator('[data-finite-attribution]').getAttribute('data-attribution-status') !== disposition.finite_test.attribution) {
    throw new Error(`${route.lang}/${masterId}: recorded object or controlled attribution was not rendered faithfully`);
  }
  const sourceStatus = await panel.locator('[data-finite-source-status]').getAttribute('data-finite-source-status');
  const organStatus = await panel.locator('[data-finite-competent-organ]').getAttribute('data-competent-organ-status');
  const actorStatus = await panel.locator('[data-actor-specific-knowledge]').getAttribute('data-personal-knowledge-status');
  const actorReceiptStatus = await panel.locator('[data-actor-specific-knowledge]').getAttribute('data-actor-receipt-status');
  const actorSourceStatus = await panel.locator('[data-actor-specific-knowledge]').getAttribute('data-actor-source-status');
  const crossFileStatus = await panel.locator('[data-cross-file-acknowledgement-status]').getAttribute('data-cross-file-acknowledgement-status');
  if (!sourceStatus || !organStatus || !actorStatus || !actorReceiptStatus || !actorSourceStatus || !crossFileStatus) {
    throw new Error(`${route.lang}/${masterId}: finite panel data-status fields are incomplete`);
  }
  for (const [axis, attribute] of receiptAxisAttributes) {
    const element = panel.locator(`[data-receipt-axis="${axis}"]`);
    if (await element.count() !== 1 || !(await element.getAttribute(attribute))) {
      throw new Error(`${route.lang}/${masterId}: receipt axis ${axis}/${attribute} missing`);
    }
  }
  const panelText = await panel.innerText();
  for (const boundary of [route.auditBoundary, route.receiptBoundary, route.actorBoundary]) {
    if (!panelText.includes(boundary)) throw new Error(`${route.lang}/${masterId}: finite panel omits boundary “${boundary}”`);
  }

  const expectedRelated = expectedFiniteRelatedIds(masterId, disposition, interlinks);
  const renderedDirect = await panel.locator('[data-finite-related-direct] button[data-trace-id]').evaluateAll((buttons) => buttons.map((button) => button.dataset.traceId));
  const renderedContext = await panel.locator('[data-finite-related-context] button[data-trace-id]').evaluateAll((buttons) => buttons.map((button) => button.dataset.traceId));
  assertSameValues(renderedDirect, expectedRelated.direct, `${route.lang}/${masterId}: finite-panel direct list`);
  assertSameValues(renderedContext, expectedRelated.context, `${route.lang}/${masterId}: finite-panel context list`);
  if (renderedContext.length) {
    const warning = (await panel.locator('[data-finite-related] .pdim-warning').innerText()).toLowerCase();
    if (!warning.includes(route.antiJoinder.toLowerCase())) throw new Error(`${route.lang}/${masterId}: finite contextual list omits anti-joinder boundary`);
  }
  return panel;
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
    } else if (['RECORDED_CONNECTION', 'SOURCE_CONTROLLED_CORRIDOR'].includes(cluster.context_type)) {
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
  if (publicRecords.length !== 121) throw new Error(`expected 121 controlled public records, found ${publicRecords.length}`);
  const exactRecords = publicRecords.filter((record) => String(record.Is_Proceeding || '').trim().toUpperCase() === 'TRUE');
  const exactIds = exactRecords.map((record) => record.Master_ID);
  const exactIdSet = new Set(exactIds);
  if (exactIds.length !== 97) throw new Error(`expected 97 exact public proceedings after aggregate-family repair, found ${exactIds.length}`);
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

  const finiteFamilyCatalog = interlinks.finite_test_family_catalog || {};
  assertSameValues(Object.keys(finiteFamilyCatalog), [
    'OMBUDSMAN_RECONSIDERATION', 'CRIMINAL_FILE_DECISION', 'CIVIL_FILE_DECISION',
    'FISCALIA_INSTITUTIONAL_MEMORY', 'PROFESSIONAL_SUPERVISION', 'ADMIN_AUTHORITY_TITLE_SOURCE',
    'TAX_CONTENTIOUS_CHAIN', 'REGULATORY_PUBLIC_ROUTE', 'GENERAL_EXACT_FILE_DECISION_TEST',
  ], 'finite-test family catalogue');
  for (const [familyId, label] of Object.entries(finiteFamilyCatalog)) requireBilingual(label, `finite-test family ${familyId}`);
  const finiteContract = interlinks.finite_test_contract || {};
  if (finiteContract.status !== 'COMPLETE_FOR_PUBLIC_EXACT_DENOMINATOR'
      || finiteContract.family_taxonomy_effect !== 'UI_ONLY_NO_EDGE_OR_CLUSTER_EFFECT'
      || finiteContract.family_assignment_rule !== 'CANONICAL_RECORD_TYPE_BEFORE_MIXED_STREAM_SUBSTRING'
      || finiteContract.recorded_candidate_authority_status !== 'NOT_COMPETENCE_OR_DUTY') {
    throw new Error('finite-test contract does not preserve the UI-only family / no-edge boundary');
  }
  assertSameValues(finiteContract.required_sequence || [], [
    'QUESTION', 'SOURCE_NEEDED', 'CURRENT_SOURCE_STATUS', 'COMPETENT_ORGAN', 'RELATED_PROCEEDINGS',
    'PROCEDURAL_AVAILABILITY', 'DECISION_DEPENDENCY', 'STRONGEST_CONTRARY_EXPLANATION',
    'CONSEQUENCE_IF_CONFIRMED', 'CONSEQUENCE_IF_REFUTED',
  ], 'finite-test required sequence');
  requireBilingual({en: finiteContract.boundary_en, es: finiteContract.boundary_es}, 'finite-test contract boundary');

  const receiptContract = interlinks.receipt_knowledge_contract || {};
  const receiptAxisKeys = receiptAxisAttributes.map(([, , dataKey]) => dataKey);
  assertSameValues(receiptContract.institutional_axis_ids || [], receiptAxisKeys, 'receipt/knowledge six-axis contract');
  if (receiptContract.cross_file_acknowledgement_is_separate !== true
      || receiptContract.institutional_axis_basis_required !== true
      || receiptContract.positive_axis_source_field_rule !== 'EXACT_EPISODE_FIELD_MUST_SUPPORT_AXIS_GRADE'
      || !Array.isArray(receiptContract.institutional_axis_basis_fields)
      || receiptContract.actor_specific_status_is_separate !== true
      || receiptContract.positive_source_membership_rule !== 'EXPLICIT_REVIEWED_FISCALIA_EPISODE_TO_MASTER_ID_ONLY'
      || receiptContract.raw_matter_reference_join !== 'PROHIBITED') {
    throw new Error('receipt/knowledge contract permits a raw-reference join or collapses institutional and actor-specific treatment');
  }
  assertSameValues(receiptContract.institutional_axis_basis_fields || [], [
    'status', 'basis_kind', 'basis_en', 'basis_es', 'limitation_en', 'limitation_es', 'source',
  ], 'receipt/knowledge axis-basis fields');
  requireBilingual({en: receiptContract.boundary_en, es: receiptContract.boundary_es}, 'receipt/knowledge contract boundary');
  const receiptStatusCatalog = interlinks.receipt_knowledge_status_catalog || {};
  for (const [status, label] of Object.entries(receiptStatusCatalog)) requireBilingual(label, `receipt/knowledge status ${status}`);

  let receiptPositiveCount = 0;
  let actorPositiveCount = 0;
  for (const masterId of exactIds) {
    const disposition = dispositionById.get(masterId);
    const result = assertFiniteTestData(masterId, disposition, interlinks);
    if (!finiteFamilyCatalog[disposition.finite_test.family_template_id]) {
      throw new Error(`${masterId}: finite-test family ${disposition.finite_test.family_template_id} is not catalogued`);
    }
    const receipt = disposition.finite_test.receipt_knowledge;
    for (const status of [...Object.values(receipt.institutional_axes), receipt.cross_file_acknowledgement_status,
      receipt.actor_specific.receipt_status, receipt.actor_specific.knowledge_status]) {
      if (!receiptStatusCatalog[status]) throw new Error(`${masterId}: receipt/knowledge status ${status} is not catalogued`);
    }
    if (result.receiptPositive) receiptPositiveCount += 1;
    if (result.actorPositive) actorPositiveCount += 1;
  }
  if (receiptPositiveCount !== 9 || actorPositiveCount !== 0) {
    throw new Error(`receipt/knowledge positive-evidence boundary mismatch (institutional=${receiptPositiveCount}, actor=${actorPositiveCount})`);
  }
  const actualFamilyCounts = Object.fromEntries(Object.keys(finiteFamilyCatalog).map((familyId) => [
    familyId, dispositions.filter((item) => item.finite_test.family_template_id === familyId).length,
  ]).filter(([, count]) => count));
  const expectedFamilyCounts = {
    OMBUDSMAN_RECONSIDERATION: 1, CRIMINAL_FILE_DECISION: 11, CIVIL_FILE_DECISION: 19,
    FISCALIA_INSTITUTIONAL_MEMORY: 21, PROFESSIONAL_SUPERVISION: 8,
    ADMIN_AUTHORITY_TITLE_SOURCE: 26, TAX_CONTENTIOUS_CHAIN: 4, REGULATORY_PUBLIC_ROUTE: 7,
  };
  if (JSON.stringify(actualFamilyCounts) !== JSON.stringify(expectedFamilyCounts)
      || JSON.stringify(interlinks.coverage?.finite_test_family_counts) !== JSON.stringify(expectedFamilyCounts)) {
    throw new Error(`finite-test family taxonomy denominator mismatch (${JSON.stringify(actualFamilyCounts)})`);
  }
  for (const [masterId, familyId] of Object.entries({
    'GC-CIV-027': 'CIVIL_FILE_DECISION', 'LZ-CAB-011': 'ADMIN_AUTHORITY_TITLE_SOURCE',
    'LZ-PRO-029': 'PROFESSIONAL_SUPERVISION', 'GC-GOV-019': 'ADMIN_AUTHORITY_TITLE_SOURCE',
    'GC-GOV-020': 'ADMIN_AUTHORITY_TITLE_SOURCE',
  })) {
    if (dispositionById.get(masterId)?.finite_test?.family_template_id !== familyId) {
      throw new Error(`${masterId}: finite-test family precedence is not ${familyId}`);
    }
  }

  const fiscaliaProfiles = Array.isArray(interlinks.fiscalia_response_episode_profiles) ? interlinks.fiscalia_response_episode_profiles : [];
  if (fiscaliaProfiles.length !== 9) throw new Error(`expected nine controlled Fiscalía response episodes, found ${fiscaliaProfiles.length}`);
  assertSameValues(fiscaliaProfiles.map((profile) => profile.profile_id), fiscaliaProfiles.map((profile) => `FISCALIA-RESPONSE-${profile.episode_id}`), 'Fiscalía response profile IDs');
  if (new Set(fiscaliaProfiles.map((profile) => profile.episode_id)).size !== 9) throw new Error('Fiscalía response episode IDs are not unique');
  for (const profile of fiscaliaProfiles) {
    if (!exactIdSet.has(profile.master_id)) throw new Error(`${profile.profile_id}: episode profile is not mapped to an exact public Master ID`);
    assertSameValues(Object.keys(profile.institutional_axes || {}), receiptAxisKeys, `${profile.profile_id}: six institutional axes`);
    assertSameValues(Object.keys(profile.institutional_axis_basis || {}), fiscaliaAxisFields, `${profile.profile_id}: nine institutional axis bases`);
    for (const axisKey of fiscaliaAxisFields) {
      requireAxisBasis(profile.institutional_axis_basis[axisKey], profile.institutional_axis_basis[axisKey].status, `${profile.profile_id}: ${axisKey}`);
    }
    for (const status of [...Object.values(profile.institutional_axes || {}), profile.cross_file_acknowledgement_status]) {
      if (!receiptStatusCatalog[status]) throw new Error(`${profile.profile_id}: uncatalogued receipt/knowledge status ${status}`);
    }
    for (const pair of [
      ['title_en', 'title_es'], ['source_authored_known_summary_en', 'source_authored_known_summary_es'],
      ['source_authored_request_summary_en', 'source_authored_request_summary_es'],
      ['institutional_response_en', 'institutional_response_es'], ['open_question_en', 'open_question_es'],
      ['contrary_or_limiting_record_en', 'contrary_or_limiting_record_es'],
    ]) {
      requireBilingual({en: profile[pair[0]], es: profile[pair[1]]}, `${profile.profile_id}: ${pair[0].replace(/_en$/, '')}`);
    }
    if (profile.source?.path !== 'assets/data/fiscalia-response-correspondence.json'
        || profile.source?.field !== 'episodes[]' || profile.source?.record_id !== profile.episode_id
        || !profile.attribution_boundary) {
      throw new Error(`${profile.profile_id}: controlled episode source/attribution provenance is incomplete`);
    }
    const receipt = dispositionById.get(profile.master_id)?.finite_test?.receipt_knowledge;
    if (receipt?.classification !== 'SOURCE_BACKED_INSTITUTIONAL_TRACE'
        || !receipt.source_profile_ids.includes(profile.profile_id)
        || !receipt.event_refs.some((event) => event.profile_id === profile.profile_id && event.event_id === profile.episode_id)) {
      throw new Error(`${profile.profile_id}: response episode does not round-trip through its exact-file receipt model`);
    }
  }
  const profileByEpisode = new Map(fiscaliaProfiles.map((profile) => [profile.episode_id, profile]));
  const eg745 = profileByEpisode.get('eg745-2026');
  if (eg745?.institutional_axes?.recipient_attribution_status !== 'NOT_LOCATED'
      || eg745?.cross_file_acknowledgement_status !== 'STATUS_UNRESOLVED'
      || eg745?.institutional_axis_basis?.recipient_attribution_status?.source?.field !== 'episodes[].unresolved_en/unresolved_es'
      || eg745?.institutional_axis_basis?.cross_file_acknowledgement_status?.source?.field !== 'episodes[].unresolved_en/unresolved_es') {
    throw new Error('EG745 recipient/cross-file grades overstate filing, global closure or named-file submission');
  }
  for (const episodeId of ['di22-2026', 'eg49-2026']) {
    const recipientBasis = profileByEpisode.get(episodeId)?.institutional_axis_basis?.recipient_attribution_status;
    if (recipientBasis?.source?.field !== 'episodes[].known_en/known_es') {
      throw new Error(`${episodeId}: recipient attribution does not cite the source-authored known field`);
    }
  }
  const dip2ExaminationBasis = profileByEpisode.get('dip2-2026')?.institutional_axis_basis?.substantive_examination_status;
  if (dip2ExaminationBasis?.status !== 'PARTLY_DOCUMENTED'
      || dip2ExaminationBasis?.source?.field !== 'episodes[].known_en/known_es') {
    throw new Error('DIP2 bounded examination grade does not cite the decree premise in the source-authored known field');
  }

  const fiscaliaMatrixContract = interlinks.fiscalia_office_file_matrix_contract || {};
  if (fiscaliaMatrixContract.row_denominator !== 24
      || fiscaliaMatrixContract.referral_is_not_transmission !== true
      || fiscaliaMatrixContract.direct_context_and_assets_are_separate !== true
      || fiscaliaMatrixContract.material_summary_is_not_received_inventory !== true
      || fiscaliaMatrixContract.axis_provenance_required !== true) {
    throw new Error('Fiscalía office/file matrix contract collapses a required substantive distinction');
  }
  assertSameValues(fiscaliaMatrixContract.required_independent_status_axes || [], fiscaliaAxisFields, 'Fiscalía matrix nine independent status axes');
  assertSameValues(fiscaliaMatrixContract.required_substantive_columns || [], [
    'date_or_period', 'received_or_known', 'material_allegations_evidence', 'material_received',
    'material_inventory_gap', 'related_direct_master_ids', 'related_context_master_ids', 'related_assets',
    'what_was_referred', 'what_was_actually_examined', 'institutional_response',
    'cross_file_acknowledgement_status', 'unitary_acknowledgement_status', 'strongest_contrary',
    'unanswered_or_source_gap',
  ], 'Fiscalía matrix substantive columns');
  const fiscaliaMatrix = Array.isArray(interlinks.fiscalia_office_file_matrix) ? interlinks.fiscalia_office_file_matrix : [];
  const publicFiscaliaRows = publicRecords.filter((record) => String(record.Stream || '').toUpperCase().includes('FISCAL'));
  if (fiscaliaMatrix.length !== 24) throw new Error(`expected 24 public Fiscalía office/file rows, found ${fiscaliaMatrix.length}`);
  assertSameValues(fiscaliaMatrix.map((row) => row.master_id), publicFiscaliaRows.map((record) => record.Master_ID), 'Fiscalía office/file public-row denominator');
  const publicFiscaliaById = new Map(publicFiscaliaRows.map((record) => [record.Master_ID, record]));
  const profileById = new Map(fiscaliaProfiles.map((profile) => [profile.profile_id, profile]));
  const matrixProfileIds = [];
  for (const row of fiscaliaMatrix) {
    const record = publicFiscaliaById.get(row.master_id);
    if (!record || row.reference !== record.Reference || row.is_proceeding !== record.Is_Proceeding
        || row.record_type !== record.Record_Type || row.source_status !== record.Source_Status) {
      throw new Error(`${row.master_id}: Fiscalía matrix identity/source state diverges from the public Master row`);
    }
    if (!row.origin_office || !row.current_custodian || !row.profile_status || !row.date_or_period || !Array.isArray(row.source_profile_ids)
        || !Array.isArray(row.related_master_ids) || !Array.isArray(row.related_direct_master_ids)
        || !Array.isArray(row.related_context_master_ids) || !Array.isArray(row.related_assets)
        || !Array.isArray(row.material_allegations_evidence) || !Array.isArray(row.material_received)) {
      throw new Error(`${row.master_id}: Fiscalía matrix control fields are incomplete`);
    }
    for (const relatedId of row.related_master_ids) {
      if (!publicRecords.some((recordItem) => recordItem.Master_ID === relatedId)) throw new Error(`${row.master_id}: unknown related Master ID ${relatedId}`);
    }
    assertSameValues([...row.related_direct_master_ids, ...row.related_context_master_ids], row.related_master_ids, `${row.master_id}: separated direct/context related IDs`);
    for (const evidenceItem of row.material_allegations_evidence) {
      if (!evidenceItem.kind || !evidenceItem.attribution) throw new Error(`${row.master_id}: material/evidence summary lacks kind or attribution`);
      requireBilingual({en: evidenceItem.text_en, es: evidenceItem.text_es}, `${row.master_id}: material/evidence summary`);
    }
    for (const field of [
      'received_or_known', 'requested', 'institutional_response', 'material_inventory_gap',
      'related_assets_gap', 'what_was_referred', 'what_was_actually_examined',
      'strongest_contrary', 'unanswered_or_source_gap',
    ]) {
      requireBilingual(row[field], `${row.master_id}: Fiscalía matrix ${field}`);
    }
    requireBilingual({en: row.boundary_en, es: row.boundary_es}, `${row.master_id}: Fiscalía raw-reference boundary`);
    if (!row.boundary_en.includes('does not infer') || !row.boundary_es.includes('no infiere')) {
      throw new Error(`${row.master_id}: Fiscalía row does not state the raw-reference non-inference boundary`);
    }
    const institutionalStatusFields = [...fiscaliaAxisFields, 'unitary_acknowledgement_status'];
    for (const field of institutionalStatusFields) {
      if (!row[field] || !receiptStatusCatalog[row[field]]) throw new Error(`${row.master_id}: missing/uncatalogued matrix status ${field}=${row[field] || 'missing'}`);
    }
    if (!row.related_proceedings_status || !row.related_assets_status) {
      throw new Error(`${row.master_id}: related-proceedings/assets statuses are incomplete`);
    }
    assertSameValues(Object.keys(row.institutional_axis_basis || {}), fiscaliaAxisFields, `${row.master_id}: nine matrix axis bases`);
    for (const axisKey of fiscaliaAxisFields) {
      requireAxisBasis(row.institutional_axis_basis[axisKey], row[axisKey], `${row.master_id}: ${axisKey}`);
    }
    if (row.unitary_acknowledgement_status !== 'NOT_LOCATED') {
      throw new Error(`${row.master_id}: absence of a located unitary acknowledgement was converted into a positive or global negative claim`);
    }
    if (!row.source_profile_ids.length) {
      if (row.profile_status !== 'EXPLICIT_PROFILE_GAP'
          || institutionalStatusFields.some((field) => row[field] !== 'NOT_LOCATED')) {
        throw new Error(`${row.master_id}: matrix audit coverage was conflated with positive institutional evidence`);
      }
    } else {
      if (row.profile_status !== 'SOURCE_CONTROLLED_PROFILE') throw new Error(`${row.master_id}: profiled matrix row lacks SOURCE_CONTROLLED_PROFILE status`);
      for (const profileId of row.source_profile_ids) {
        const profile = profileById.get(profileId);
        if (!profile || profile.master_id !== row.master_id) throw new Error(`${row.master_id}: matrix source profile ${profileId} lacks exact episode provenance`);
        matrixProfileIds.push(profileId);
      }
    }
  }
  if (fiscaliaMatrix.filter((row) => row.is_proceeding === 'TRUE').length !== 21
      || fiscaliaMatrix.filter((row) => row.is_proceeding === 'UNVERIFIED').length !== 3
      || matrixProfileIds.length !== 8) {
    throw new Error('Fiscalía matrix must remain 21 exact + 3 unverified rows, with eight source-profiled matrix rows');
  }
  const outsideMatrixProfiles = fiscaliaProfiles.filter((profile) => !matrixProfileIds.includes(profile.profile_id));
  if (outsideMatrixProfiles.length !== 1 || outsideMatrixProfiles[0].episode_id !== 'dp1901-2026'
      || outsideMatrixProfiles[0].master_id !== 'GC-CRI-008') {
    throw new Error('the ninth controlled Fiscalía episode must remain dp1901-2026 → GC-CRI-008 outside the 24-row Fiscalía matrix');
  }
  const gub86Row = fiscaliaMatrix.find((row) => row.master_id === 'LZ-FIS-007');
  if (gub86Row?.material_received_status !== 'NOT_LOCATED'
      || gub86Row.institutional_axis_basis?.material_received_status?.status !== 'NOT_LOCATED'
      || gub86Row.institutional_axis_basis?.material_received_status?.source?.field !== 'episodes[].unresolved_en/unresolved_es') {
    throw new Error('GUB 86/2026 must retain NOT_LOCATED received-material treatment and its unresolved-field provenance');
  }
  const dp1901ReferralBasis = outsideMatrixProfiles[0].institutional_axis_basis?.referral_status;
  if (dp1901ReferralBasis?.status !== 'ROUTING_DOCUMENTED'
      || dp1901ReferralBasis?.source?.field !== 'episodes[].known_en/known_es'
      || dp1901ReferralBasis?.source?.record_id !== 'dp1901-2026') {
    throw new Error('DP 1901/2026 referral treatment must remain sourced to the controlled known-field episode, not inferred receipt');
  }

  const coverage = interlinks.coverage || {};
  const requiredCoverage = {
    public_exact_proceeding_count: 97,
    case_prism_exact_proceeding_covered_count: 26,
    case_prism_exact_proceeding_uncovered_count: 71,
    decision_dependency_exact_coverage: 'GAP_26_OF_97',
    exact_file_decision_dependency_actionability_count: 97,
    exact_file_decision_dependency_actionability_coverage: 'VERIFIED_97_OF_97',
    exact_proceeding_full_finite_test_count: 97,
    exact_proceeding_full_finite_test_coverage: 'VERIFIED_97_OF_97',
    receipt_knowledge_classification_count: 97,
    receipt_knowledge_classification_coverage: 'VERIFIED_97_OF_97',
    receipt_knowledge_axis_provenance_count: 97,
    receipt_knowledge_axis_provenance_coverage: 'VERIFIED_97_OF_97',
    receipt_knowledge_positive_source_profile_count: 9,
    fiscalia_office_file_matrix_count: 24,
    fiscalia_office_file_matrix_coverage: 'VERIFIED_24_OF_24',
    fiscalia_office_file_matrix_substantive_column_count: 24,
    fiscalia_office_file_matrix_substantive_column_coverage: 'VERIFIED_24_OF_24',
    fiscalia_office_file_matrix_exact_count: 21,
    fiscalia_office_file_matrix_unverified_count: 3,
    fiscalia_response_episode_profile_count: 9,
    fiscalia_office_file_matrix_source_profiled_record_count: 8,
    controlled_trace_route_count: 97,
    controlled_isolation_route_count: 97,
    controlled_navigation_coverage: 'VERIFIED_97_OF_97',
    dedicated_narrative_dossier_coverage: 'PARTIAL_NOT_INFERRED',
  };
  for (const [field, expected] of Object.entries(requiredCoverage)) {
    if (coverage[field] !== expected) throw new Error(`coverage.${field}: expected ${expected}, found ${coverage[field]}`);
  }
  const treasuryRelationship = relationshipById.get('REL-LINKED_PROCEEDING-NAT-TES-001-X-WB-005');
  if (!treasuryRelationship
      || treasuryRelationship.from_master_id !== 'NAT-TES-001'
      || treasuryRelationship.to_master_id !== 'X-WB-005'
      || treasuryRelationship.relationship_class !== 'DIRECT_PROCEDURAL_EDGE') {
    throw new Error('Treasury 7/2026 to World Bank direct routing lineage is missing or misclassified');
  }
  if ((interlinks.relationships || []).some((item) =>
    [item.from_master_id, item.to_master_id].includes('NAT-TES-001')
      && [item.from_master_id, item.to_master_id].some((id) => ['LZ-TRA-028', 'NAT-AID-001'].includes(id)))) {
    throw new Error('Treasury contextual tracks were promoted into direct procedural edges');
  }
  const treasuryContext = clusterById.get('CTX-SOURCE-T7-COR-001');
  if (!treasuryContext
      || treasuryContext.context_type !== 'SOURCE_CONTROLLED_CORRIDOR'
      || treasuryContext.source?.record_id !== 'T7-COR-001') {
    throw new Error('Treasury/Resolution 28 source-controlled corridor is missing');
  }
  assertSameValues(treasuryContext.member_master_ids || [], ['NAT-TES-001', 'LZ-TRA-028'], 'Treasury/Resolution 28 contextual corridor');
  const publicMoneyContext = clusterById.get('CTX-PRISM-P18');
  if (!publicMoneyContext
      || !['NAT-TES-001', 'NAT-AID-001'].every((id) => (publicMoneyContext.member_master_ids || []).includes(id))) {
    throw new Error('Treasury and aid-programme context is missing from Case Prism proposition P18');
  }
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
  const prismCoveredIds = new Set((prismData.propositions || []).flatMap((prop) =>
    Object.values(prop.cells || {}).flatMap((cell) =>
      cell.status === 'OUTSIDE' ? [] : (cell.master_ids || []).filter((id) => exactIdSet.has(id))
    )
  ));
  if (prismCoveredIds.size !== 26 || exactIds.length - prismCoveredIds.size !== 71) {
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
    if (await page.locator('[data-proceedings-map="20260831a"]').count() !== 1) throw new Error(`${route.lang}: live renderer marker is not 20260831a`);
    const staticPrismText = await page.locator('#case-prism').innerText();
    if (!staticPrismText.includes('26') || !staticPrismText.includes('71') || !staticPrismText.includes(route.headlineFinite)
        || staticPrismText.includes(route.headlineForbidden)) {
      throw new Error(`${route.lang}: static Case Prism introduction overclaims the 26/97 shared-proposition denominator`);
    }
    if (await page.locator('a[href="#isolation-test"]').count() < 1) throw new Error(`${route.lang}: exact-file finite-test CTA missing`);
    await assertFilterScope(page, true, route, 'map');

    const search = page.locator('[data-map-search]');
    await search.fill('GC-APP-004');
    await page.waitForSelector('[data-node-id="GC-APP-004"]');
    await search.fill('');
    const track = page.locator('[data-map-track]');
    await track.selectOption({ index: 1 });
    await track.selectOption('');

    await page.locator('[role="tab"][data-view="chronology"]').click();
    await page.waitForSelector('[role="tab"][data-view="chronology"][aria-selected="true"]');
    await assertFilterScope(page, true, route, 'chronology');
    await page.locator('[role="tab"][data-view="map"]').click();
    await page.waitForSelector('[role="tab"][data-view="map"][aria-selected="true"]');
    await assertFilterScope(page, true, route, 'map-restored');

    await page.locator('a[href="#case-prism"]').first().click();
    await page.waitForSelector('[role="tab"][data-view="prism"][aria-selected="true"]');
    await assertFilterScope(page, false, route, 'prism');
    if (await page.evaluate(() => location.hash) !== '#case-prism') throw new Error(`${route.lang}: Case Prism CTA did not activate the hash view`);
    await assertFocusedAndVisible(page, '[data-view-body]', `${route.lang}: Case Prism CTA`);
    await page.goBack();
    await page.waitForSelector('[role="tab"][data-view="map"][aria-selected="true"]');
    await assertFilterScope(page, true, route, 'map-back');
    if (await page.evaluate(() => location.hash) !== '') throw new Error(`${route.lang}: browser Back did not restore the map hash state`);
    await page.goForward();
    await page.waitForSelector('[role="tab"][data-view="prism"][aria-selected="true"]');
    await assertFilterScope(page, false, route, 'prism-forward');
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
    const fiscaliaMatrixView = detail.locator('[data-fiscalia-office-file-matrix]');
    if (await fiscaliaMatrixView.count() !== 1) throw new Error(`${route.lang}: P05 detail omits the Fiscalía office/file matrix`);
    if (await fiscaliaMatrixView.getAttribute('data-row-count') !== '24'
        || await fiscaliaMatrixView.getAttribute('data-exact-count') !== '21'
        || await fiscaliaMatrixView.getAttribute('data-unverified-count') !== '3'
        || await fiscaliaMatrixView.getAttribute('data-profiled-count') !== '8'
        || await fiscaliaMatrixView.getAttribute('data-response-episode-count') !== '9') {
      throw new Error(`${route.lang}: Fiscalía matrix must distinguish 24 rows, 21 exact, three unresolved, eight profiled and nine total response episodes`);
    }
    if (await fiscaliaMatrixView.locator('[data-fiscalia-row]').count() !== 24) throw new Error(`${route.lang}: Fiscalía matrix does not render 24 rows`);
    const fiscaliaRenderedIds = await fiscaliaMatrixView.locator('[data-fiscalia-row]').evaluateAll((rows) => rows.map((row) => row.dataset.masterId));
    assertSameValues(fiscaliaRenderedIds, fiscaliaMatrix.map((row) => row.master_id), `${route.lang}: Fiscalía rendered row denominator`);
    for (const row of fiscaliaMatrix) {
      const rendered = fiscaliaMatrixView.locator(`[data-fiscalia-row][data-master-id="${row.master_id}"]`);
      if (await rendered.count() !== 1) throw new Error(`${route.lang}/${row.master_id}: Fiscalía row missing`);
      const rowAttributes = {
        'data-is-proceeding': row.is_proceeding,
        'data-record-type': row.record_type,
        'data-canonical-source-status': row.source_status,
        'data-profile-status': row.profile_status,
        'data-related-proceedings-status': row.related_proceedings_status,
        'data-related-assets-status': row.related_assets_status,
        'data-unitary-acknowledgement-status': row.unitary_acknowledgement_status,
      };
      for (const [attribute, expected] of Object.entries(rowAttributes)) {
        if (await rendered.getAttribute(attribute) !== expected) throw new Error(`${route.lang}/${row.master_id}: ${attribute} diverges from the controlled row`);
      }
      for (const selector of [
        '[data-fiscalia-date-period]', '[data-fiscalia-exactness]', '[data-fiscalia-record-type]',
        '[data-fiscalia-canonical-source]', '[data-fiscalia-profile-status]', '[data-fiscalia-material-evidence]',
        '[data-fiscalia-received-known]', '[data-fiscalia-requested]', '[data-fiscalia-institutional-response]',
        '[data-fiscalia-material-inventory]', '[data-fiscalia-material-inventory-gap]',
        '[data-fiscalia-related-direct]', '[data-fiscalia-related-context]', '[data-fiscalia-related-proceedings-status]',
        '[data-fiscalia-related-assets]', '[data-fiscalia-related-assets-gap]', '[data-fiscalia-what-referred]',
        '[data-fiscalia-what-examined]', '[data-fiscalia-axis-grid]', '[data-fiscalia-unitary-acknowledgement]',
        '[data-fiscalia-strongest-contrary]', '[data-fiscalia-unanswered-gap]', '[data-fiscalia-row-boundary]', '[data-fiscalia-source-profiles]',
      ]) {
        if (await rendered.locator(selector).count() !== 1) throw new Error(`${route.lang}/${row.master_id}: matrix row omits ${selector}`);
      }
      const renderedMaterialItems = await rendered.locator('[data-fiscalia-material-evidence-list] > li').count();
      const renderedInventoryItems = await rendered.locator('[data-fiscalia-material-inventory-list] > li').count();
      const renderedAssetItems = await rendered.locator('[data-fiscalia-related-assets-list] > li').count();
      if (renderedMaterialItems !== row.material_allegations_evidence.length || renderedInventoryItems !== row.material_received.length
          || renderedAssetItems !== row.related_assets.length) {
        throw new Error(`${route.lang}/${row.master_id}: material summary/inventory distinction is not rendered faithfully`);
      }
      const renderedDirectIds = await rendered.locator('[data-fiscalia-related-direct-list] [data-trace-id]').evaluateAll((buttons) => buttons.map((button) => button.dataset.traceId));
      const renderedContextIds = await rendered.locator('[data-fiscalia-related-context-list] [data-trace-id]').evaluateAll((buttons) => buttons.map((button) => button.dataset.traceId));
      assertSameValues(renderedDirectIds, row.related_direct_master_ids, `${route.lang}/${row.master_id}: matrix direct IDs`);
      assertSameValues(renderedContextIds, row.related_context_master_ids, `${route.lang}/${row.master_id}: matrix context IDs`);
      const rowText = await rendered.textContent();
      for (const field of ['received_or_known', 'requested', 'institutional_response', 'material_inventory_gap', 'related_assets_gap', 'what_was_referred', 'what_was_actually_examined', 'strongest_contrary', 'unanswered_or_source_gap']) {
        const expected = bilingualValue(row[field], route.lang);
        if (!expected || !rowText.includes(expected)) throw new Error(`${route.lang}/${row.master_id}: rendered matrix omits ${field}`);
      }
      for (const item of row.material_allegations_evidence) {
        const expected = item[`text_${route.lang}`];
        if (!expected || !rowText.includes(expected) || !rowText.includes(item.kind) || !rowText.includes(item.attribution)) {
          throw new Error(`${route.lang}/${row.master_id}: material/evidence item, kind or attribution is missing`);
        }
      }
      if (!rowText.includes(row.date_or_period) || !rowText.includes(row[`boundary_${route.lang}`])
          || row.source_profile_ids.some((profileId) => !rowText.includes(profileId))) {
        throw new Error(`${route.lang}/${row.master_id}: date, row boundary or source-profile provenance is missing`);
      }
      if (!rowText.includes(row.source_status) || !rowText.includes(row.profile_status) || !rowText.includes(row.is_proceeding)) {
        throw new Error(`${route.lang}/${row.master_id}: canonical source/profile/exactness distinction is not visible`);
      }
      for (const axisKey of fiscaliaAxisFields) {
        const axis = rendered.locator(`[data-fiscalia-axis="${axisKey}"]`);
        const basis = row.institutional_axis_basis[axisKey];
        if (await axis.count() !== 1
            || await axis.getAttribute('data-axis-status') !== row[axisKey]
            || await axis.getAttribute('data-axis-basis-status') !== basis.status
            || await axis.getAttribute('data-axis-basis-kind') !== basis.basis_kind
            || await axis.locator(`[data-fiscalia-axis-basis="${axisKey}"]`).count() !== 1) {
          throw new Error(`${route.lang}/${row.master_id}: ${axisKey} grade/basis attributes diverge`);
        }
        const basisText = await axis.textContent();
        const sourceProvenanceValues = Object.values(basis.source || {}).filter((value) => typeof value === 'string' && value);
        for (const expected of [
          bilingualValue({en:basis.basis_en, es:basis.basis_es}, route.lang),
          bilingualValue({en:basis.limitation_en, es:basis.limitation_es}, route.lang),
          ...sourceProvenanceValues,
        ]) {
          if (!expected || !basisText.includes(expected)) throw new Error(`${route.lang}/${row.master_id}: ${axisKey} omits its basis, limitation or provenance`);
        }
      }
    }
    const fiscaliaMatrixText = await fiscaliaMatrixView.innerText();
    if (!fiscaliaMatrixText.includes(route.noUnitaryAcknowledgement) || !fiscaliaMatrixText.includes('9')
        || !/not proof|no equivale/i.test(fiscaliaMatrixText)) {
      throw new Error(`${route.lang}: Fiscalía matrix conflates model coverage with positive evidence or omits the unitary-acknowledgement boundary`);
    }

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
    await assertFilterScope(page, false, route, 'lanes');
    if (await page.locator('.pdim-swimlane tbody tr').count() !== 19) throw new Error(`${route.lang}: swimlane event denominator mismatch`);
    if (await page.locator('[data-lane-heading]').count() !== 12) throw new Error(`${route.lang}: stable lane headings missing`);
    if (await page.locator('.pdim-swim-cell').count() !== 228) throw new Error(`${route.lang}: swimlane coordinate denominator mismatch`);

    await page.locator('[role="tab"][data-view="isolation"]').click();
    await page.waitForSelector('[data-isolation-id]');
    await assertFilterScope(page, false, route, 'isolation');
    const isolation = page.locator('[data-isolation-id]');
    const isolationIds = await isolation.locator('option').evaluateAll((options) => options.map((option) => option.value).filter((value) => value !== '__FULL__'));
    assertSameValues(isolationIds, exactIds, `${route.lang}: exact-proceeding isolation denominator`);
    const renderedCoverage = await isolation.locator('option[value]:not([value="__FULL__"])').evaluateAll((options) => options.map((option) => [option.value, option.dataset.prismCoverage]));
    for (const [masterId, status] of renderedCoverage) {
      const expectedStatus = prismCoveredIds.has(masterId) ? 'covered' : 'unresolved';
      if (status !== expectedStatus) throw new Error(`${route.lang}/${masterId}: Case Prism coverage label is ${status}, expected ${expectedStatus}`);
    }
    if (renderedCoverage.filter(([, status]) => status === 'covered').length !== 26 || renderedCoverage.filter(([, status]) => status === 'unresolved').length !== 71) {
      throw new Error(`${route.lang}: visible Case Prism content coverage must remain 26 covered / 71 unresolved`);
    }
    if (await isolation.locator('option[value="GC-APP-007"]').count()) throw new Error(`${route.lang}: aggregate removal-appeal family admitted to isolation`);
    const coverageText = await page.locator('[data-isolation-coverage]').innerText();
    if (!coverageText.includes(`26/${exactIds.length}`) || !coverageText.includes('71')) throw new Error(`${route.lang}: finite 26/97 Case Prism content denominator is not visible`);
    const finiteCoverage = page.locator('[data-finite-test-coverage]');
    if (await finiteCoverage.count() !== 1
        || await finiteCoverage.getAttribute('data-audit-count') !== '97'
        || await finiteCoverage.getAttribute('data-positive-evidence-count') !== '9') {
      throw new Error(`${route.lang}: finite-test coverage must distinguish 97 audited models from nine files with positive institutional evidence`);
    }
    const finiteCoverageText = await finiteCoverage.innerText();
    if (!finiteCoverageText.includes('97/97') || !finiteCoverageText.includes(route.auditBoundary) || !finiteCoverageText.includes(route.positiveEvidence)) {
      throw new Error(`${route.lang}: finite audit/positive-evidence boundary is not visible`);
    }
    const finiteOptionCoverage = await isolation.locator('option[value]:not([value="__FULL__"])').evaluateAll((options) => options.map((option) => [option.value, option.dataset.finiteTestCoverage]));
    if (finiteOptionCoverage.length !== 97 || finiteOptionCoverage.some(([, status]) => status !== 'audited')) {
      throw new Error(`${route.lang}: all 97 exact options must expose audited finite-test coverage`);
    }
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
      const finitePanel = await assertFinitePanel(page, '[data-isolation-reconnection]', exactId, route, disposition, interlinks);
      if (Object.values(representativeFiniteIds).includes(exactId)
          && await page.locator('[data-proceedings-map] [aria-live="polite"]').count() !== 1) {
        throw new Error(`${route.lang}/${exactId}: finite isolation state must retain exactly one polite live region`);
      }
      if (exactId === representativeFiniteIds.directAndContext) {
        if (!(disposition.relationship_ids || []).length || !(disposition.context_cluster_ids || []).length) {
          throw new Error(`${route.lang}/${exactId}: direct+context representative lost either classification`);
        }
      }
      if (exactId === representativeFiniteIds.contextOnly) {
        if ((disposition.relationship_ids || []).length || !(disposition.context_cluster_ids || []).length) {
          throw new Error(`${route.lang}/${exactId}: context-only representative was misclassified`);
        }
      }
      if (exactId === representativeFiniteIds.explicitGap) {
        if (disposition.primary_classification !== 'EXPLICIT_RELATIONSHIP_GAP'
            || (disposition.relationship_ids || []).length || (disposition.context_cluster_ids || []).length) {
          throw new Error(`${route.lang}/${exactId}: explicit no-relation gap acquired an unsupported connection`);
        }
        const gapAxisStatuses = [];
        for (const [axis, attribute] of receiptAxisAttributes) {
          gapAxisStatuses.push(await finitePanel.locator(`[data-receipt-axis="${axis}"]`).getAttribute(attribute));
        }
        if (gapAxisStatuses.some((status) => status !== 'NOT_LOCATED')) {
          throw new Error(`${route.lang}/${exactId}: audited gap model was conflated with positive receipt evidence`);
        }
      }
      if (exactId === representativeFiniteIds.fiscaliaProfile) {
        const fiscalAxisStatuses = [];
        for (const [axis, attribute] of receiptAxisAttributes) {
          fiscalAxisStatuses.push(await finitePanel.locator(`[data-receipt-axis="${axis}"]`).getAttribute(attribute));
        }
        if (!fiscalAxisStatuses.some(isPositiveReceiptStatus)) throw new Error(`${route.lang}/${exactId}: source-controlled Fiscalía profile exposes no positive institutional axis`);
        const personalStatus = await finitePanel.locator('[data-actor-specific-knowledge]').getAttribute('data-personal-knowledge-status');
        if (!/NO_ACTOR|NOT_ESTABLISHED/.test(personalStatus || '')) throw new Error(`${route.lang}/${exactId}: institutional profile was promoted into actor-specific knowledge`);
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
      const expectedContextCounterparts = new Set(clusterIds.flatMap((clusterId) =>
        (clusterById.get(clusterId)?.member_master_ids || []).filter((memberId) => memberId !== exactId && publicRecords.some((record) => record.Master_ID === memberId))
      ));
      const contextSection = page.locator('[data-isolation-context]');
      if (await contextSection.getAttribute('data-context-cluster-count') !== String(clusterIds.length)
          || await contextSection.getAttribute('data-context-counterpart-count') !== String(expectedContextCounterparts.size)) {
        throw new Error(`${route.lang}/${exactId}: context summary must count controlled clusters and unique public counterparts without inflating repeated membership`);
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
    await assertFilterScope(page, false, route, 'trace');
    const trace = page.locator('[data-trace-select]');
    const traceIds = await trace.locator('option').evaluateAll((options) => options.map((option) => option.value).filter(Boolean));
    assertSameValues(traceIds, publicRecords.map((record) => record.Master_ID), `${route.lang}: public-record trace denominator`);
    for (const exactId of exactIds) {
      const disposition = dispositionById.get(exactId);
      await trace.selectOption(exactId);
      await page.waitForFunction((selectedId) => document.querySelector('[data-trace-panel]')?.textContent.includes(selectedId), exactId);
      if (await page.evaluate(() => location.hash) !== `#trace-proceeding=${encodeURIComponent(exactId)}`) {
        throw new Error(`${route.lang}/${exactId}: trace did not produce a stable deep link`);
      }
      if (await page.locator(`[data-trace-panel] .pdim-trace-disposition[data-classification="${disposition.primary_classification}"]`).count() !== 1) {
        throw new Error(`${route.lang}/${exactId}: trace does not expose its controlled disposition`);
      }
      const finitePanel = await assertFinitePanel(page, '[data-trace-panel]', exactId, route, disposition, interlinks);
      if (Object.values(representativeFiniteIds).includes(exactId)
          && await page.locator('[data-proceedings-map] [aria-live="polite"]').count() !== 1) {
        throw new Error(`${route.lang}/${exactId}: finite trace state must retain exactly one polite live region`);
      }
      if (exactId === representativeFiniteIds.directAndContext
          && (!(disposition.relationship_ids || []).length || !(disposition.context_cluster_ids || []).length)) {
        throw new Error(`${route.lang}/${exactId}: direct+context trace representative lost either controlled relation class`);
      }
      if (exactId === representativeFiniteIds.contextOnly
          && ((disposition.relationship_ids || []).length || !(disposition.context_cluster_ids || []).length)) {
        throw new Error(`${route.lang}/${exactId}: context-only trace representative was promoted into a direct edge`);
      }
      if (exactId === representativeFiniteIds.explicitGap) {
        const axisStatuses = [];
        for (const [axis, attribute] of receiptAxisAttributes) {
          axisStatuses.push(await finitePanel.locator(`[data-receipt-axis="${axis}"]`).getAttribute(attribute));
        }
        if (axisStatuses.some((status) => status !== 'NOT_LOCATED')) {
          throw new Error(`${route.lang}/${exactId}: trace audit model was conflated with positive receipt evidence`);
        }
      }
      if (exactId === representativeFiniteIds.fiscaliaProfile) {
        const axisStatuses = [];
        for (const [axis, attribute] of receiptAxisAttributes) {
          axisStatuses.push(await finitePanel.locator(`[data-receipt-axis="${axis}"]`).getAttribute(attribute));
        }
        if (!axisStatuses.some(isPositiveReceiptStatus)) throw new Error(`${route.lang}/${exactId}: Fiscalía trace omits its source-controlled institutional evidence grades`);
        if (!/NO_ACTOR|NOT_ESTABLISHED/.test(await finitePanel.locator('[data-actor-specific-knowledge]').getAttribute('data-personal-knowledge-status') || '')) {
          throw new Error(`${route.lang}/${exactId}: Fiscalía trace promoted institutional handling into personal knowledge`);
        }
      }
      const masterHref = await page.locator('[data-trace-panel] .pdim-record-backlink a').getAttribute('href');
      if (!masterHref || !masterHref.endsWith(`#record-${encodeURIComponent(exactId)}`)) {
        throw new Error(`${route.lang}/${exactId}: trace lacks its reciprocal Master Register row link`);
      }
      const traceContextWarning = page.locator('[data-trace-panel] .pdim-rel-grid > section:nth-child(2) > .pdim-warning');
      if (await traceContextWarning.count() !== 1) throw new Error(`${route.lang}/${exactId}: trace omits the contextual anti-joinder warning`);
      const traceWarning = (await traceContextWarning.innerText()).toLowerCase();
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

    await trace.selectOption(representativeFiniteIds.fiscaliaProfile);
    await page.waitForSelector(`[data-trace-panel] [data-finite-test-panel][data-master-id="${representativeFiniteIds.fiscaliaProfile}"]`);
    await page.setViewportSize({ width: 390, height: 844 });
    const mobileFinitePanel = page.locator(`[data-trace-panel] [data-finite-test-panel][data-master-id="${representativeFiniteIds.fiscaliaProfile}"]`);
    const finiteOverflow = await mobileFinitePanel.evaluate((panel) => {
      const panelRect = panel.getBoundingClientRect();
      const offenders = [...panel.querySelectorAll('*')].filter((element) => {
        const rect = element.getBoundingClientRect();
        const style = getComputedStyle(element);
        if (style.display === 'none' || style.visibility === 'hidden' || rect.width === 0) return false;
        return rect.left < panelRect.left - 1 || rect.right > panelRect.right + 1;
      }).slice(0, 5).map((element) => ({tag: element.tagName, className: element.className, text: element.textContent.trim().slice(0, 60)}));
      return {clientWidth: panel.clientWidth, scrollWidth: panel.scrollWidth, viewportWidth: innerWidth, offenders};
    });
    if (finiteOverflow.scrollWidth > finiteOverflow.clientWidth + 1 || finiteOverflow.offenders.length) {
      throw new Error(`${route.lang}: 390x844 finite-test panel overflows (${JSON.stringify(finiteOverflow)})`);
    }
    if (await page.locator('[data-proceedings-map] [aria-live="polite"]').count() !== 1) {
      throw new Error(`${route.lang}: 390x844 finite-test trace does not retain exactly one polite live region`);
    }
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
    if (renderedMasterIds.length !== 121) throw new Error(`${route.lang}: Master Register must render 121 controlled public rows`);
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

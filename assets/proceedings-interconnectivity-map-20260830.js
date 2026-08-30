(() => {
  'use strict';

  const script = document.currentScript;
  if (!script) return;
  const assetBase = new URL('.', script.src);
  const repoBase = new URL('../', assetBase);
  const registerDataUrl = new URL('assets/data/proceedings-master-public-v1.json', repoBase).href;
  const prismUrl = new URL('assets/data/proceedings-case-prism-v1.json', repoBase).href;
  const interlinkUrl = new URL('assets/data/proceedings-interlinkability-v1.json', repoBase).href;
  const lang = (document.documentElement.lang || 'en').toLowerCase().startsWith('es') ? 'es' : 'en';
  const registerRoute = new URL(lang === 'es' ? 'es/registro-maestro-procedimientos/' : 'en/master-proceedings-register/', repoBase).href;
  const detailRoutes = {
    'LZ-JUD-043': {
      en: new URL('en/dp-3205-2014-arrecife/', repoBase).href,
      es: new URL('es/dp-3205-2014-arrecife/', repoBase).href
    }
  };

  const copy = lang === 'es' ? {
    loading: 'Construyendo el mapa desde el registro canónico…',
    error: 'No se pudo construir el mapa de procedimientos.',
    allTracks: 'Todas las vías', search: 'Buscar ID, referencia, órgano, objeto o estado…',
    map: 'Mapa por vías', chronology: 'Cronología', trace: 'Trazar un procedimiento / registro',
    prism: 'Prisma del caso', lanes: 'Vías paralelas', isolation: 'Prueba de aislamiento',
    records: 'nodos públicos', tracks: 'vías', direct: 'pares directos controlados', gaps: 'nodos con brecha abierta',
    directTitle: 'Relaciones procesales directas',
    contextTitle: 'Puentes de contexto controlados',
    why: 'Por qué están conectados', noDirect: 'No hay relación procesal directa admitida en el registro controlado para este objeto.',
    noContext: 'No hay otro puente contextual exacto en la proyección actual.',
    contextWarning: 'Contexto no significa mismo procedimiento, acumulación, coordinación, conocimiento, ilicitud ni responsabilidad.',
    source: 'Fuente/estado', gap: 'Brecha abierta', now: 'Ahora',
    approximate: 'Orden aproximado por el primer año reconocible en Date_or_Period; no implica causalidad.',
    openRegister: 'Abrir Registro Maestro', openRegisterRecord: 'Abrir este registro canónico', traceThis: 'Trazar registro', empty: 'No hay nodos que coincidan con los filtros.',
    publicBoundary: 'Esta visualización usa una proyección pública minimizada del registro canónico. No convierte referencias en procedimientos ni conexiones contextuales en hechos jurídicos.',
    audience: 'Lente del lector', proposition: 'Proposición / hecho a contrastar', status: 'Relación', treatment: 'Tratamiento en el expediente', period: 'Periodo',
    matrixLead: 'Una misma proposición, leída horizontalmente a través de procedimientos jurídicamente separados.',
    lanesLead: 'Orden cronológico de las proposiciones controladas y las vías en las que aparecen de forma directa, contextual o abierta.',
    isolationLead: 'Selecciona cualquier procedimiento exacto de la proyección pública. El modo aislado conserva únicamente el tratamiento del Prisma codificado como directamente presente en ese expediente; la reconexión muestra por separado las relaciones procesales expresas, los puentes contextuales controlados y las brechas no resueltas.',
    chooseLane: 'Seleccionar procedimiento exacto', visibleAlone: 'Permanece visible en el expediente seleccionado', disappears: 'Contexto material que desaparece al leerlo solo',
    noVisible: 'Ninguna proposición del prisma está marcada como directamente presente en este procedimiento exacto.', noOutside: 'No se identifica contexto material adicional en el prisma controlado.',
    detail: 'Detalle de la dependencia', masterIds: 'IDs canónicos relacionados', openTrace: 'Abrir traza',
    formalBoundary: 'La prueba de aislamiento es metodológica. No demuestra que el órgano recibiera, debiera admitir o debiera valorar el material externo.',
    fullCorpus: 'Corpus completo', restore: 'Restaurar corpus completo', isolatedMode: 'Modo aislado', sourceLinks: 'Fuentes públicas controladas de la proposición',
    sourceScope: 'Estas fuentes respaldan la ruta de auditoría de la proposición; no demuestran por sí solas el tratamiento en esta celda.',
    outsideSelected: 'Fuera del expediente seleccionado', insideSelected: 'Visible en el expediente seleccionado',
    evidenceStatus: 'Estado probatorio de la proposición', attribution: 'Atribución', contrary: 'Explicación / registro contrario más fuerte', sourceNeeded: 'Fuente necesaria',
    competentOrgan: 'Órgano competente', decisionDepends: 'Qué decisión podría depender', ifConfirmed: 'Si se confirma', ifRefuted: 'Si se refuta',
    representation: 'Linaje de abogado/procurador', prismConnections: 'Dependencias del Prisma para este ID', noPrismConnections: 'No hay dependencia del Prisma codificada para este ID.',
    prismUnavailable: 'La capa del Prisma no está disponible. El mapa canónico sigue accesible, pero las vistas de convergencia y aislamiento no pueden verificarse en esta carga.',
    laneSource: 'Otros estados registrados de vía/expediente', priority: 'Prioridad para esta lente', matrixCaption: 'Matriz de dependencia decisoria por proposición y vía jurídica separada',
    swimCaption: 'Cronología en vías paralelas; cada columna sigue siendo un expediente o carril institucional separado',
    exactProceedings: 'procedimientos exactos públicos', prismCovered: 'con coordenadas expresas en el Prisma', prismNotCovered: 'sin coordenada actual en el Prisma',
    coverageBoundary: 'El selector incluye todos los registros públicos marcados canónicamente como procedimientos. La cobertura del Prisma es un denominador finito y distinto: la ausencia de coordenada significa cobertura no desarrollada o no localizada, no ausencia de relación fáctica.',
    coveredGroup: 'Procedimientos con coordenadas en el Prisma', uncoveredGroup: 'Otros procedimientos exactos — sin coordenada en el Prisma',
    selectedCoverage: 'Cobertura del procedimiento seleccionado', prismCoveredSelected: 'Este procedimiento tiene tratamiento proposicional expreso en el Prisma controlado.',
    noPrismCoverageSelected: 'No hay tratamiento proposicional del Prisma codificado para este procedimiento exacto. No se infiere ninguna celda: el expediente sigue siendo trazable mediante sus campos canónicos y las brechas permanecen expresas.',
    directReconnection: 'Relaciones procesales directas para reconectar', contextReconnection: 'Puentes contextuales controlados para reconectar', unresolvedReconnection: 'Estado no resuelto / cobertura pendiente',
    noDirectSelected: 'No hay relación procesal directa codificada por ID canónico para este procedimiento.', noContextSelected: 'No hay puente contextual controlado con otro nodo público en los campos actuales.',
    directBoundary: 'Solo se muestran relaciones expresamente codificadas como padre/origen, enlace de procedimiento, recurso/revisión o enlace documentado por una fuente especializada controlada.',
    contextBoundary: 'Estos puentes proceden de valores canónicos coincidentes. Ayudan a localizar contexto; no acreditan identidad de procedimiento, acumulación, conocimiento, causalidad, ilicitud ni responsabilidad. Para evitar expansión transitiva, los miembros de una proposición no se siguen hacia otras proposiciones; un ID relacionado solo abre otra proposición mediante una coordenada DIRECTA.',
    prismCoordinate: 'Coordenada del Prisma', noPrismCoordinate: 'Sin coordenada del Prisma', selectedFileStatus: 'Estado respecto del expediente seleccionado',
    relationCount: 'relaciones', bridgeCount: 'puentes', nextSource: 'Siguiente fuente necesaria', classification: 'Clasificación controlada', provenance: 'Procedencia', limitations: 'Límites',
    interlinkUnavailable: 'El registro controlado de interconectividad no está disponible para este procedimiento. No se infiere una clasificación por ausencia.',
    notExactClassification: 'Registro público — no es un procedimiento exacto', notExactTrace: 'Este objeto público puede trazarse como registro, pero no está marcado como procedimiento exacto. No se infiere ninguna clasificación, relación procesal directa ni puente contextual.',
    sourceAssertions: 'Afirmaciones de fuente', sourceAssertion: 'afirmación',
    directVerified: 'pares con fuente verificada', directPending: 'par con fuente primaria pendiente'
  } : {
    loading: 'Building the map from the canonical register…',
    error: 'The proceedings map could not be built.',
    allTracks: 'All tracks', search: 'Search ID, reference, organ, object or status…',
    map: 'Track map', chronology: 'Chronology', trace: 'Trace one proceeding / record',
    prism: 'Case Prism', lanes: 'Parallel lanes', isolation: 'Isolation test',
    records: 'public nodes', tracks: 'tracks', direct: 'controlled direct pairs', gaps: 'nodes with an open gap',
    directTitle: 'Direct procedural relationships',
    contextTitle: 'Controlled context bridges',
    why: 'Why connected?', noDirect: 'No direct procedural relationship is admitted in the controlled registry for this object.',
    noContext: 'No other exact contextual bridge is available in the current projection.',
    contextWarning: 'Context does not mean the same proceeding, joinder, coordination, knowledge, wrongdoing or liability.',
    source: 'Source/status', gap: 'Open gap', now: 'Now',
    approximate: 'Approximate order by the first recognisable year in Date_or_Period; it does not imply causation.',
    openRegister: 'Open Master Register', openRegisterRecord: 'Open this canonical record', traceThis: 'Trace record', empty: 'No nodes match the current filters.',
    publicBoundary: 'This visualisation uses a minimised public projection of the canonical register. It does not turn references into proceedings or contextual connections into legal facts.',
    audience: 'Reader lens', proposition: 'Proposition / fact to test', status: 'Relationship', treatment: 'Treatment in file', period: 'Period',
    matrixLead: 'One proposition, read horizontally across legally separate proceedings.',
    lanesLead: 'Chronological order of the controlled propositions and the lanes in which they appear as direct, contextual or open.',
    isolationLead: 'Select any exact proceeding in the public projection. Isolated mode keeps only Case Prism treatment encoded as directly present in that file; reconnection separately shows express procedural relationships, controlled contextual bridges and unresolved gaps.',
    chooseLane: 'Select exact proceeding', visibleAlone: 'Remains visible in the selected file', disappears: 'Material context that disappears when read alone',
    noVisible: 'No proposition in this prism is marked as directly present in this exact proceeding.', noOutside: 'No additional material context is identified in the controlled prism.',
    detail: 'Dependency detail', masterIds: 'Related canonical IDs', openTrace: 'Open trace',
    formalBoundary: 'The isolation test is methodological. It does not prove that the organ received, should admit or should assess the external material.',
    fullCorpus: 'Full corpus', restore: 'Restore full corpus', isolatedMode: 'Isolated mode', sourceLinks: 'Controlled public sources for the proposition',
    sourceScope: 'These sources support the proposition-level audit path; they do not by themselves establish treatment in this cell.',
    outsideSelected: 'Outside the selected file', insideSelected: 'Visible in the selected file',
    evidenceStatus: 'Proposition evidence status', attribution: 'Attribution', contrary: 'Strongest contrary explanation / record', sourceNeeded: 'Source needed',
    competentOrgan: 'Competent organ', decisionDepends: 'What decision could depend', ifConfirmed: 'If confirmed', ifRefuted: 'If refuted',
    representation: 'Counsel/procurador lineage', prismConnections: 'Case Prism dependencies for this ID', noPrismConnections: 'No Case Prism dependency is encoded for this ID.',
    prismUnavailable: 'The Case Prism layer is unavailable. The canonical map remains accessible, but convergence and isolation views cannot be verified in this load.',
    laneSource: 'Other recorded lane/file statuses', priority: 'Priority for this lens', matrixCaption: 'Decision-dependency matrix by proposition and legally separate lane',
    swimCaption: 'Parallel-lane chronology; every column remains a separate proceeding or institutional lane',
    exactProceedings: 'exact public proceedings', prismCovered: 'with express Case Prism coordinates', prismNotCovered: 'without a current Case Prism coordinate',
    coverageBoundary: 'The selector includes every public record canonically marked as a proceeding. Case Prism coverage is a separate finite denominator: no coordinate means coverage is undeveloped or not located, not that no factual relationship exists.',
    coveredGroup: 'Proceedings with Case Prism coordinates', uncoveredGroup: 'Other exact proceedings — no Case Prism coordinate',
    selectedCoverage: 'Selected-proceeding coverage', prismCoveredSelected: 'This proceeding has express proposition treatment in the controlled Case Prism.',
    noPrismCoverageSelected: 'No Case Prism proposition treatment is encoded for this exact proceeding. No cell is inferred: the file remains traceable through its canonical fields and every gap stays explicit.',
    directReconnection: 'Direct procedural relationships for reconnection', contextReconnection: 'Controlled context bridges for reconnection', unresolvedReconnection: 'Unresolved state / coverage pending',
    noDirectSelected: 'No direct procedural relationship is encoded by canonical ID for this proceeding.', noContextSelected: 'No controlled context bridge to another public node is available in the current fields.',
    directBoundary: 'Only relationships expressly encoded as parent/origin, linked proceeding, appeal/review or documented by a controlled specialist source are shown.',
    contextBoundary: 'These bridges come from matching canonical values. They help locate context; they do not establish the same proceeding, joinder, knowledge, causation, wrongdoing or liability. To prevent transitive expansion, proposition co-members are not followed into other propositions; a related ID surfaces another proposition only through a DIRECT coordinate.',
    prismCoordinate: 'Case Prism coordinate', noPrismCoordinate: 'No Case Prism coordinate', selectedFileStatus: 'Status relative to selected file',
    relationCount: 'relationships', bridgeCount: 'bridges', nextSource: 'Next source needed', classification: 'Controlled classification', provenance: 'Provenance', limitations: 'Limitations',
    interlinkUnavailable: 'The controlled interlinkability register is unavailable for this proceeding. No classification is inferred from absence.',
    notExactClassification: 'Public record — not an exact proceeding', notExactTrace: 'This public object remains traceable as a record, but it is not marked as an exact proceeding. No classification, direct procedural relationship or contextual bridge is inferred.',
    sourceAssertions: 'Source assertions', sourceAssertion: 'assertion',
    directVerified: 'source-verified pairs', directPending: 'source-reported primary-pending pair'
  };

  const esc = (v) => String(v || '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const norm = (v) => String(v || '').trim();
  const key = (v) => norm(v).toLowerCase();
  const localized = (obj, base) => obj ? (obj[`${base}_${lang}`] || obj[lang] || obj[base] || obj.en || obj.es || '') : '';

  const firstYear = (value) => {
    const m = String(value || '').match(/\b(19|20)\d{2}\b/);
    return m ? Number(m[0]) : 9999;
  };

  const labelFor = (r) => norm(r.Reference) || norm(r.Secondary_Reference) || norm(r.Master_ID);
  const subtitleFor = (r) => [norm(r.Proceeding_Class), norm(r.Stream)].filter(Boolean).join(' · ');

  const detailUrlFor = (id) => detailRoutes[id] && detailRoutes[id][lang];
  const detailAnchor = (r, text, className = '') => {
    const url = detailUrlFor(r.Master_ID);
    return url ? `<a${className ? ` class="${className}"` : ''} href="${esc(url)}">${esc(text)}</a>` : esc(text);
  };

  const card = (r, traceButton = true) => `
    <article class="pdim-node" data-node-id="${esc(r.Master_ID)}">
      <div class="pdim-node-head"><span class="pdim-id">${detailAnchor(r, r.Master_ID)}</span><span class="pdim-state" data-state="${esc(norm(r.Is_Proceeding).toUpperCase() || 'UNVERIFIED')}">${esc(norm(r.Is_Proceeding).toUpperCase() || 'UNVERIFIED')}</span></div>
      <h3>${detailAnchor(r, labelFor(r))}</h3>
      <p class="pdim-sub">${esc(subtitleFor(r))}</p>
      <p>${esc([r.Connection, r.Object_or_Purpose].filter(Boolean).join(' — '))}</p>
      <div class="pdim-node-meta"><span>${esc(r.Date_or_Period)}</span><span>${esc(r.Origin_Organ)}</span></div>
      ${traceButton ? `<button type="button" data-trace-id="${esc(r.Master_ID)}">${copy.traceThis} →</button>` : ''}
      ${detailUrlFor(r.Master_ID) ? `<a class="pdim-detail-link" href="${esc(detailUrlFor(r.Master_ID))}">${lang === 'es' ? 'Abrir ficha bilingüe' : 'Open bilingual record'} ↗</a>` : ''}
    </article>`;

  function prismMatchesForId(prism, selected) {
    if (!prism) return [];
    return prism.propositions.flatMap((prop) => prism.lanes.flatMap((lane) => {
      const cell = prop.cells && prop.cells[lane.id];
      return cell && cell.status !== 'OUTSIDE' && Array.isArray(cell.master_ids) && cell.master_ids.includes(selected)
        ? [{prop, lane, cell}] : [];
    }));
  }

  const isExactProceeding = (record) => norm(record && record.Is_Proceeding).toUpperCase() === 'TRUE';

  function catalogLabel(catalog, token) {
    const meta = catalog && catalog[token];
    return localized(meta, 'label') || localized(meta, '') || humanToken(token);
  }

  function provenanceLabel(source) {
    if (!source) return '—';
    const direction = source.assertion_from_master_id || source.assertion_to_master_id
      ? `${norm(source.assertion_from_master_id) || '?'} → ${norm(source.assertion_to_master_id) || '?'}`
      : '';
    return [
      source.kind,
      source.source_id,
      source.path,
      source.record_id,
      source.record_master_id || source.source_record_master_id,
      source.field_or_record_id,
      source.field,
      source.value_token,
      source.assertion_relationship_type,
      source.assertion_direction,
      direction,
      source.anchor,
      source.evidence_status
    ].map(norm).filter(Boolean).join(' · ') || '—';
  }

  function provenanceHtml(item) {
    const assertions = Array.isArray(item && item.source_assertions) && item.source_assertions.length
      ? item.source_assertions
      : (item && item.source ? [item.source] : []);
    if (!assertions.length) return '';
    const count = assertions.length;
    const countLabel = count > 1 ? ` (${count} ${copy.sourceAssertions.toLowerCase()})` : ` (${count} ${copy.sourceAssertion})`;
    return `<div class="pdim-provenance" data-source-assertions data-assertion-count="${count}"><strong>${esc(copy.provenance)}${esc(countLabel)}</strong><ul>${assertions.map((source) => `<li>${esc(provenanceLabel(source))}</li>`).join('')}</ul></div>`;
  }

  function renderTrace(root, selected, byId, prism, interlinks) {
    const r = byId.get(selected); if (!r) return;
    const disposition = interlinks && (interlinks.node_dispositions || []).find((entry) => entry.master_id === selected);
    const relationshipById = new Map(((interlinks && interlinks.relationships) || []).map((relationship) => [relationship.id, relationship]));
    const clusterById = new Map(((interlinks && interlinks.context_clusters) || []).map((cluster) => [cluster.id, cluster]));
    const registryRelationships = disposition ? (disposition.relationship_ids || []).map((id) => relationshipById.get(id)).filter(Boolean) : [];
    const directHtml = registryRelationships.length ? registryRelationships.map((relationship) => {
      const otherId = relationship.from_master_id === selected ? relationship.to_master_id : relationship.from_master_id;
      const other = byId.get(otherId);
      return `<li data-interlink-disposition data-classification="DIRECT_PROCEDURAL_EDGE"><button type="button" data-trace-id="${esc(otherId)}"><strong>${esc(catalogLabel(interlinks.relationship_type_catalog, relationship.relationship_type))}</strong> · ${esc(otherId)} · ${esc(other ? labelFor(other) : otherId)}</button><p>${esc(localized(relationship, 'why'))}</p>${localized(relationship, 'limitations') ? `<small><strong>${esc(copy.limitations)}:</strong> ${esc(localized(relationship, 'limitations'))}</small>` : ''}${provenanceHtml(relationship)}</li>`;
    }).join('') : `<li class="pdim-none">${copy.noDirect}</li>`;

    const contexts = disposition ? (disposition.context_cluster_ids || []).map((id) => clusterById.get(id)).filter(Boolean) : [];
    const contextHtml = contexts.length ? contexts.map((cluster) => {
      const members = (cluster.member_master_ids || []).filter((id) => id !== selected && byId.has(id));
      return `<li data-interlink-disposition data-classification="CONTROLLED_CONTEXTUAL_BRIDGE"><strong>${esc(localized(cluster, 'label') || catalogLabel(interlinks.context_type_catalog, cluster.context_type))}</strong><p>${esc(localized(cluster, 'why'))}</p><div class="pdim-context-members">${members.map((id) => `<button type="button" data-trace-id="${esc(id)}">${esc(id)} · ${esc(labelFor(byId.get(id)))}</button>`).join('')}</div>${localized(cluster, 'limitations') ? `<small><strong>${esc(copy.limitations)}:</strong> ${esc(localized(cluster, 'limitations'))}</small>` : ''}${provenanceHtml(cluster)}</li>`;
    }).join('') : `<li class="pdim-none">${copy.noContext}</li>`;

    const prismMatches = prismMatchesForId(prism, selected);
    const prismHtml = prismMatches.length ? prismMatches.map(({prop, lane, cell}) => `
      <li><button type="button" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><strong>${esc(prop.id)} · ${esc(propTitle(prop))}</strong><span>${esc(laneLabel(lane))} · ${esc(statusLabel(prism, cell.status))} · ${esc(treatmentLabel(prism, cell.treatment))}</span></button></li>`).join('')
      : `<li class="pdim-none">${copy.noPrismConnections}</li>`;

    const holder = root.querySelector('[data-trace-panel]');
    holder.setAttribute('tabindex', '-1');
    holder.setAttribute('aria-labelledby', 'pdim-trace-result-title');
    holder.innerHTML = `
      <h2 id="pdim-trace-result-title" class="pdim-trace-result-title">${copy.trace}: ${esc(selected)}</h2>
      <div class="pdim-trace-identity">${card(r, false)}
        <dl><div><dt>${copy.source}</dt><dd>${esc(r.Source_Status || '—')}</dd></div><div><dt>${copy.gap}</dt><dd>${esc(r.Open_Reference_Gap || '—')}</dd></div><div><dt>${copy.now}</dt><dd>${esc([r.Current_Custodian, r.Status, r.Latest_Known_Event].filter(Boolean).join(' — ') || '—')}</dd></div></dl>
      </div>
      <p class="pdim-record-backlink"><a href="${esc(`${registerRoute}#record-${encodeURIComponent(selected)}`)}">${esc(copy.openRegisterRecord)} · ${esc(selected)} →</a></p>
      ${disposition ? `<section class="pdim-trace-disposition" data-interlink-disposition data-classification="${esc(disposition.primary_classification)}"><h2>${esc(copy.classification)}: ${esc(catalogLabel(interlinks.classification_catalog, disposition.primary_classification))}</h2><p>${esc(localized(disposition, 'why'))}</p>${localized(disposition, 'limitations') ? `<small><strong>${esc(copy.limitations)}:</strong> ${esc(localized(disposition, 'limitations'))}</small>` : ''}${localized(disposition, 'next_source_needed') ? `<small><strong>${esc(copy.nextSource)}:</strong> ${esc(localized(disposition, 'next_source_needed'))}</small>` : ''}</section>` : isExactProceeding(r) ? `<section class="pdim-trace-disposition" data-interlink-disposition data-classification="REGISTRY_NOT_AVAILABLE"><h2>${esc(copy.unresolvedReconnection)}</h2><p>${esc(copy.interlinkUnavailable)}</p></section>` : `<section class="pdim-trace-disposition" data-interlink-disposition data-classification="NOT_EXACT_PROCEEDING_RECORD"><h2>${esc(copy.classification)}: ${esc(copy.notExactClassification)}</h2><p>${esc(copy.notExactTrace)}</p></section>`}
      <div class="pdim-rel-grid">
        <section><h2>${copy.directTitle}</h2><ul class="pdim-rel-list">${directHtml}</ul></section>
        <section><h2>${copy.contextTitle}</h2><p class="pdim-warning">${copy.contextWarning}</p><ul class="pdim-rel-list">${contextHtml}</ul></section>
      </div>
      <section class="pdim-prism-trace"><h2>${copy.prismConnections}</h2><ul class="pdim-rel-list">${prismHtml}</ul></section>
      <div class="pdim-prism-detail" data-prism-detail aria-live="polite" tabindex="-1"><p>${prism ? esc(localized(prism.boundary, '')) : esc(copy.prismUnavailable)}</p></div>`;
    holder.focus({preventScroll:true});
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    holder.scrollIntoView({behavior: reduced ? 'auto' : 'smooth', block:'start'});
  }

  function renderMap(root, rows, filters) {
    const body = root.querySelector('[data-view-body]');
    const q = key(filters.search.value); const track = filters.track.value;
    const filtered = rows.filter((r) => {
      if (track && r.Stream !== track) return false;
      if (!q) return true;
      return key([r.Master_ID,r.Reference,r.Secondary_Reference,r.Origin_Organ,r.Current_Custodian,r.Connection,r.Object_or_Purpose,r.Status,r.Source_Status].join(' ')).includes(q);
    });
    if (!filtered.length) { body.innerHTML = `<p class="pdim-empty">${copy.empty}</p>`; return; }
    const groups = new Map(); filtered.forEach((r) => { const s = norm(r.Stream) || 'Unclassified'; if (!groups.has(s)) groups.set(s, []); groups.get(s).push(r); });
    body.innerHTML = `<div class="pdim-track-map">${Array.from(groups.entries()).sort((a,b)=>a[0].localeCompare(b[0])).map(([stream, group]) => `<section class="pdim-track"><header><h2>${esc(stream)}</h2><span>${group.length}</span></header><div class="pdim-node-grid">${group.sort((a,b)=>firstYear(a.Date_or_Period)-firstYear(b.Date_or_Period)).map((r)=>card(r)).join('')}</div></section>`).join('')}</div>`;
  }

  function renderChronology(root, rows, filters) {
    const body = root.querySelector('[data-view-body]');
    const q = key(filters.search.value); const track = filters.track.value;
    const filtered = rows.filter((r) => (!track || r.Stream === track) && (!q || key([r.Master_ID,r.Reference,r.Origin_Organ,r.Connection,r.Object_or_Purpose,r.Status].join(' ')).includes(q))).sort((a,b) => firstYear(a.Date_or_Period)-firstYear(b.Date_or_Period) || labelFor(a).localeCompare(labelFor(b)));
    body.innerHTML = `<p class="pdim-note">${copy.approximate}</p><ol class="pdim-chronology">${filtered.map((r) => `<li><time>${esc(r.Date_or_Period || '—')}</time>${card(r)}</li>`).join('')}</ol>`;
  }

  const laneLabel = (lane) => localized(lane, '') || lane.id;
  const propTitle = (prop) => localized(prop, 'title') || prop.id;
  const propQuestion = (prop) => localized(prop, 'question');
  const propPeriod = (prop) => localized(prop, 'period') || prop.period || '';
  const cellNote = (cell) => localized(cell, 'note');
  const humanToken = (value) => norm(value).replaceAll('_', ' ').toLowerCase().replace(/^./, (c) => c.toUpperCase());

  function sortedProps(prism, audience) {
    return prism.propositions.slice().sort((a, b) => {
      const ap = a.audience_priority && Number.isFinite(a.audience_priority[audience]) ? a.audience_priority[audience] : 999;
      const bp = b.audience_priority && Number.isFinite(b.audience_priority[audience]) ? b.audience_priority[audience] : 999;
      return ap - bp || Number(a.sort || 9999) - Number(b.sort || 9999) || a.id.localeCompare(b.id);
    });
  }

  function statusLabel(prism, status) {
    const meta = prism.statuses && prism.statuses[status];
    return localized(meta, '') || status;
  }

  function treatmentLabel(prism, treatment) {
    const meta = prism.treatments && prism.treatments[treatment];
    return localized(meta, '') || humanToken(treatment);
  }

  function attributionLabel(prism, attribution) {
    const meta = prism.attribution_classes && prism.attribution_classes[attribution];
    return localized(meta, '') || humanToken(attribution);
  }

  function evidenceStatusLabel(prism, status) {
    const meta = prism.evidence_statuses && prism.evidence_statuses[status];
    return localized(meta, '') || humanToken(status);
  }

  function audienceLens(prism, state) {
    return prism.audience_lenses.find((a) => a.id === state.audience) || prism.audience_lenses[0];
  }

  function sourceLinks(prism, prop) {
    const catalog = prism.source_catalog || {};
    return (prop.source_ids || []).map((id) => ({id, source: catalog[id]})).filter((item) => item.source).map(({id, source}) => {
      const href = source[`href_${lang}`] || source.href_en || source.href_es;
      const label = source[`label_${lang}`] || source.label_en || source.label_es || id;
      return `<li><a href="${esc(new URL(href, repoBase).href)}"><strong>${esc(label)}</strong><span>${esc(id)} · ${esc(evidenceStatusLabel(prism, source.evidence_status))}</span></a></li>`;
    }).join('');
  }

  function renderPrismDetail(scope, prism, propId, laneId) {
    const prop = prism.propositions.find((p) => p.id === propId);
    const lane = prism.lanes.find((l) => l.id === laneId);
    if (!prop || !lane) return;
    const cell = prop.cells && prop.cells[laneId];
    const holder = scope.querySelector('[data-prism-detail]');
    if (!holder) return;
    const ids = cell && Array.isArray(cell.master_ids) ? cell.master_ids : [];
    const action = prop.actionability || {};
    const sources = sourceLinks(prism, prop);
    const gaps = cell && Array.isArray(cell.representation_gap_ids) ? cell.representation_gap_ids : [];
    const evidenceToken = cell.evidence_status || prop.source_status || '—';
    holder.innerHTML = `
      <div class="pdim-prism-detail-head"><div><span class="pdim-id">${esc(prop.id)} · ${esc(propPeriod(prop))}</span><h3>${esc(propTitle(prop))}</h3><p>${esc(propQuestion(prop))}</p></div><div class="pdim-detail-statuses"><span class="pdim-prism-status" data-prism-status="${esc(cell.status)}">${esc(statusLabel(prism, cell.status))}</span><span class="pdim-treatment">${esc(treatmentLabel(prism, cell.treatment))}</span></div></div>
      <dl class="pdim-dependency-grid">
        <div><dt>${copy.why}</dt><dd><strong>${esc(laneLabel(lane))}</strong> — ${esc(cellNote(cell))}</dd></div>
        <div><dt>${copy.evidenceStatus}</dt><dd><span>${esc(evidenceStatusLabel(prism, evidenceToken))}</span><code>${esc(evidenceToken)}</code></dd></div>
        <div><dt>${copy.attribution}</dt><dd>${esc(attributionLabel(prism, prop.attribution))}</dd></div>
        <div><dt>${copy.contrary}</dt><dd>${esc(localized(prop.contrary_record, '') || '—')}</dd></div>
        <div><dt>${copy.decisionDepends}</dt><dd>${esc(localized(cell, 'decision') || localized(prop.decision_dependency, '') || '—')}</dd></div>
        <div><dt>${copy.sourceNeeded}</dt><dd>${esc(localized(action.source_needed, '') || '—')}</dd></div>
        <div><dt>${copy.competentOrgan}</dt><dd>${esc(localized(action.competent_organ, '') || '—')}</dd></div>
        <div><dt>${copy.ifConfirmed}</dt><dd>${esc(localized(action.if_confirmed, '') || '—')}</dd></div>
        <div><dt>${copy.ifRefuted}</dt><dd>${esc(localized(action.if_refuted, '') || '—')}</dd></div>
        <div><dt>${copy.representation}</dt><dd><code>${esc(cell.representation_lineage_status || '—')}</code>${gaps.length ? ` · ${esc(gaps.join(', '))}` : ''}</dd></div>
      </dl>
      ${sources ? `<section class="pdim-source-links"><h4>${copy.sourceLinks}</h4><p>${esc(copy.sourceScope)}</p><ul>${sources}</ul></section>` : ''}
      ${ids.length ? `<div class="pdim-prism-id-list"><strong>${copy.masterIds}</strong>${ids.map((id) => `<button type="button" data-trace-id="${esc(id)}">${esc(id)} · ${copy.openTrace}</button>${detailUrlFor(id) ? `<a class="pdim-detail-link" href="${esc(detailUrlFor(id))}">${lang === 'es' ? 'Ficha' : 'Record'} ↗</a>` : ''}`).join('')}</div>` : ''}`;
    holder.focus({preventScroll:true});
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    holder.scrollIntoView({behavior: reduced ? 'auto' : 'smooth', block:'start'});
  }

  function audienceControl(prism, state) {
    return `<label class="pdim-prism-audience">${copy.audience}<select data-prism-audience>${prism.audience_lenses.map((a) => `<option value="${esc(a.id)}"${a.id === state.audience ? ' selected' : ''}>${esc(localized(a, ''))}</option>`).join('')}</select></label>`;
  }

  function audienceQuestion(prism, state) {
    const lens = audienceLens(prism, state);
    return localized(lens, 'question');
  }

  function audiencePath(prism, state) {
    return localized(audienceLens(prism, state), 'source_path');
  }

  function renderPrism(root, prism, state) {
    const body = root.querySelector('[data-view-body]');
    const props = sortedProps(prism, state.audience);
    body.innerHTML = `
      <section class="pdim-prism-head"><div><p class="pdim-note">${esc(copy.matrixLead)}</p><p><strong>${esc(audienceQuestion(prism, state))}</strong></p><p>${esc(audiencePath(prism, state))}</p></div>${audienceControl(prism, state)}</section>
      <div class="pdim-prism-table-wrap"><table class="pdim-prism-table"><caption>${esc(copy.matrixCaption)}</caption><thead><tr><th scope="col">${copy.proposition}</th>${prism.lanes.map((lane) => `<th scope="col">${esc(laneLabel(lane))}</th>`).join('')}</tr></thead><tbody>${props.map((prop) => `<tr><th scope="row"><span>${esc(propPeriod(prop))}</span><strong>${esc(propTitle(prop))}</strong><small>${esc(evidenceStatusLabel(prism, prop.source_status || ''))}</small></th>${prism.lanes.map((lane) => { const cell = prop.cells[lane.id]; const aria = `${propTitle(prop)} · ${laneLabel(lane)} · ${statusLabel(prism, cell.status)} · ${treatmentLabel(prism, cell.treatment)}`; return `<td><button type="button" class="pdim-prism-cell" aria-label="${esc(aria)}" data-prism-status="${esc(cell.status)}" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><span>${esc(statusLabel(prism, cell.status))}</span><small>${esc(treatmentLabel(prism, cell.treatment))}</small></button></td>`; }).join('')}</tr>`).join('')}</tbody></table></div>
      <div class="pdim-prism-legend">${Object.entries(prism.statuses).map(([status, meta]) => `<span data-prism-status="${esc(status)}"><b></b>${esc(localized(meta, ''))}</span>`).join('')}</div>
      <div class="pdim-prism-detail" data-prism-detail aria-live="polite" tabindex="-1"><p>${esc(localized(prism.boundary, ''))}</p></div>`;
  }

  function renderParallelLanes(root, prism, state) {
    const body = root.querySelector('[data-view-body]');
    const props = prism.propositions.slice().sort((a,b) => Number(a.sort || 9999) - Number(b.sort || 9999));
    const priority = new Set(sortedProps(prism, state.audience).slice(0, 3).map((p) => p.id));
    body.innerHTML = `
      <section class="pdim-prism-head"><div><p class="pdim-note">${esc(copy.lanesLead)}</p><p><strong>${esc(audienceQuestion(prism, state))}</strong></p><p>${esc(audiencePath(prism, state))}</p></div>${audienceControl(prism, state)}</section>
      <div class="pdim-swimlane-wrap"><table class="pdim-swimlane"><caption>${esc(copy.swimCaption)}</caption><thead><tr><th scope="col">${copy.period}</th><th scope="col">${copy.proposition}</th>${prism.lanes.map((lane) => `<th scope="col" data-lane-heading="${esc(lane.id)}">${esc(laneLabel(lane))}</th>`).join('')}</tr></thead><tbody>${props.map((prop) => `<tr class="${priority.has(prop.id) ? 'is-lens-priority' : ''}"><th scope="row"><time>${esc(propPeriod(prop))}</time><span>${esc(prop.id)}</span>${priority.has(prop.id) ? `<b>${copy.priority}</b>` : ''}</th><td class="pdim-swim-event"><strong>${esc(propTitle(prop))}</strong><span>${esc(propQuestion(prop))}</span></td>${prism.lanes.map((lane) => { const cell = prop.cells[lane.id]; return `<td><button type="button" class="pdim-swim-cell" data-prism-status="${esc(cell.status)}" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><strong>${esc(statusLabel(prism, cell.status))}</strong><span>${esc(treatmentLabel(prism, cell.treatment))}</span></button></td>`; }).join('')}</tr>`).join('')}</tbody></table></div>
      <div class="pdim-prism-detail" data-prism-detail aria-live="polite" tabindex="-1"><p>${esc(localized(prism.boundary, ''))}</p></div>`;
  }

  function renderIsolation(root, prism, interlinks, state, byId, rows) {
    const body = root.querySelector('[data-view-body]');
    const options = rows.filter(isExactProceeding).map((record) => ({
      id: record.Master_ID,
      record,
      matches: prismMatchesForId(prism, record.Master_ID)
    })).sort((a, b) => labelFor(a.record).localeCompare(labelFor(b.record)) || a.id.localeCompare(b.id));
    const coveredOptions = options.filter((item) => item.matches.length);
    const uncoveredOptions = options.filter((item) => !item.matches.length);
    if (!state.isolationId || (state.isolationId !== '__FULL__' && !options.some((item) => item.id === state.isolationId))) state.isolationId = '__FULL__';
    const selected = options.find((item) => item.id === state.isolationId) || null;
    const relationshipById = new Map((interlinks.relationships || []).map((relationship) => [relationship.id, relationship]));
    const clusterById = new Map((interlinks.context_clusters || []).map((cluster) => [cluster.id, cluster]));
    const disposition = selected ? (interlinks.node_dispositions || []).find((entry) => entry.master_id === selected.id) : null;
    const selectedRelationships = disposition ? (disposition.relationship_ids || []).map((id) => relationshipById.get(id)).filter(Boolean) : [];
    const selectedClusters = disposition ? (disposition.context_cluster_ids || []).map((id) => clusterById.get(id)).filter(Boolean) : [];
    const reconnectIds = new Set();
    const linkedPrismPropIds = new Set();
    if (selected) {
      selectedRelationships.forEach((relationship) => {
        reconnectIds.add(relationship.from_master_id);
        reconnectIds.add(relationship.to_master_id);
      });
      selectedClusters.forEach((cluster) => {
        if (cluster.context_type === 'CASE_PRISM_PROPOSITION') {
          const propositionId = norm(cluster.source && cluster.source.record_id);
          if (propositionId) linkedPrismPropIds.add(propositionId);
        } else if (cluster.context_type === 'RECORDED_CONNECTION') {
          (cluster.member_master_ids || []).forEach((id) => reconnectIds.add(id));
        }
      });
      reconnectIds.delete(selected.id);
    }
    const props = sortedProps(prism, state.audience);
    const direct = [];
    const outside = [];
    if (selected) props.forEach((prop) => {
      const exactMatches = prism.lanes.map((lane) => ({lane, cell: prop.cells[lane.id]})).filter(({cell}) => cell.status !== 'OUTSIDE' && Array.isArray(cell.master_ids) && cell.master_ids.includes(selected.id));
      exactMatches.filter(({cell}) => cell.status === 'DIRECT').forEach(({lane, cell}) => direct.push({prop, cell, lane}));
      const sourceLanes = prism.lanes.filter((lane) => {
        const cell = prop.cells[lane.id];
        if (cell.status === 'OUTSIDE' || (cell.status === 'DIRECT' && Array.isArray(cell.master_ids) && cell.master_ids.includes(selected.id))) return false;
        if (linkedPrismPropIds.has(prop.id)) return true;
        if (!Array.isArray(cell.master_ids)) return false;
        if (cell.master_ids.includes(selected.id)) return true;
        return cell.status === 'DIRECT' && cell.master_ids.some((id) => reconnectIds.has(id));
      });
      if (sourceLanes.length) {
        const lane = sourceLanes[0];
        outside.push({prop, cell: prop.cells[lane.id], lane, sourceLanes});
      }
    });
    const item = ({prop, cell, lane, sourceLanes=[]}) => `<li><button type="button" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><span class="pdim-prism-status" data-prism-status="${esc(cell.status)}">${esc(statusLabel(prism, cell.status))}</span><strong>${esc(propTitle(prop))}</strong></button><p>${esc(cellNote(cell))}</p>${sourceLanes.length ? `<small><strong>${copy.laneSource}:</strong> ${esc(sourceLanes.map((sourceLane) => `${laneLabel(sourceLane)} — ${statusLabel(prism, prop.cells[sourceLane.id].status)}`).join(' · '))}</small>` : ''}</li>`;
    const mini = `<div class="pdim-isolation-map" data-isolation-mode="${selected ? 'isolated' : 'full'}"><table><caption>${selected ? `${copy.isolatedMode}: ${selected.id}` : copy.fullCorpus}</caption><thead><tr><th scope="col">${copy.proposition}</th>${prism.lanes.map((lane) => `<th scope="col">${esc(laneLabel(lane))}</th>`).join('')}</tr></thead><tbody>${props.map((prop) => `<tr><th scope="row">${esc(prop.id)} · ${esc(propTitle(prop))}</th>${prism.lanes.map((lane) => { const cell = prop.cells[lane.id]; const active = !selected || (cell.status === 'DIRECT' && Array.isArray(cell.master_ids) && cell.master_ids.includes(selected.id)); const selectionState = !selected ? '' : (active ? copy.insideSelected : copy.outsideSelected); const accessibleState = selectionState ? ` · ${selectionState}` : ''; const suppression = selected && !active ? ' disabled aria-disabled="true" tabindex="-1"' : ''; return `<td class="${active ? '' : 'is-suppressed'}"><button type="button"${suppression} aria-label="${esc(`${statusLabel(prism, cell.status)}${accessibleState}`)}" data-prism-status="${esc(cell.status)}" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><span>${esc(statusLabel(prism, cell.status))}</span>${selected ? `<small>${esc(selectionState)}</small>` : ''}</button></td>`; }).join('')}</tr>`).join('')}</tbody></table></div>`;
    const option = (entry) => `<option value="${esc(entry.id)}" data-prism-coverage="${entry.matches.length ? 'covered' : 'unresolved'}"${selected && entry.id === selected.id ? ' selected' : ''}>${esc(entry.id)} · ${esc(labelFor(entry.record))}${entry.matches.length ? '' : ` · ${copy.noPrismCoordinate}`}</option>`;
    const optionGroups = `${coveredOptions.length ? `<optgroup label="${esc(`${copy.coveredGroup} (${coveredOptions.length})`)}">${coveredOptions.map(option).join('')}</optgroup>` : ''}${uncoveredOptions.length ? `<optgroup label="${esc(`${copy.uncoveredGroup} (${uncoveredOptions.length})`)}">${uncoveredOptions.map(option).join('')}</optgroup>` : ''}`;
    let reconnection = '';
    if (selected) {
      const directHtml = selectedRelationships.length ? selectedRelationships.map((relationship) => {
        const otherId = relationship.from_master_id === selected.id ? relationship.to_master_id : relationship.from_master_id;
        const other = byId.get(otherId);
        const limitations = localized(relationship, 'limitations');
        return `<li data-interlink-disposition data-classification="DIRECT_PROCEDURAL_EDGE"><button type="button" data-trace-id="${esc(otherId)}"><strong>${esc(catalogLabel(interlinks.relationship_type_catalog, relationship.relationship_type))}</strong> · ${esc(otherId)} · ${esc(other ? labelFor(other) : otherId)}</button><p>${esc(localized(relationship, 'why'))}</p>${limitations ? `<small><strong>${esc(copy.limitations)}:</strong> ${esc(limitations)}</small>` : ''}${provenanceHtml(relationship)}</li>`;
      }).join('') : `<li class="pdim-none">${esc(copy.noDirectSelected)}</li>`;
      const contextLinkCount = selectedClusters.reduce((total, cluster) => total + (cluster.member_master_ids || []).filter((id) => id !== selected.id && byId.has(id)).length, 0);
      const contextHtml = selectedClusters.length ? selectedClusters.map((cluster) => {
        const members = (cluster.member_master_ids || []).filter((id) => id !== selected.id && byId.has(id));
        const limitations = localized(cluster, 'limitations');
        return `<li data-interlink-disposition data-classification="CONTROLLED_CONTEXTUAL_BRIDGE"><strong>${esc(localized(cluster, 'label') || catalogLabel(interlinks.context_type_catalog, cluster.context_type))}</strong><p>${esc(localized(cluster, 'why'))}</p><div class="pdim-context-members">${members.map((id) => `<button type="button" data-trace-id="${esc(id)}">${esc(id)} · ${esc(labelFor(byId.get(id)))}</button>`).join('')}</div>${limitations ? `<small><strong>${esc(copy.limitations)}:</strong> ${esc(limitations)}</small>` : ''}${provenanceHtml(cluster)}</li>`;
      }).join('') : `<li class="pdim-none">${esc(copy.noContextSelected)}</li>`;
      const unresolved = [];
      if (!selected.matches.length) unresolved.push(`<li data-interlink-disposition data-classification="NO_PRISM_COVERAGE"><strong>${esc(copy.noPrismCoordinate)}</strong><p>${esc(copy.noPrismCoverageSelected)}</p></li>`);
      if (disposition) {
        const classification = disposition.primary_classification;
        unresolved.push(`<li data-interlink-disposition data-classification="${esc(classification)}"><strong>${esc(copy.classification)}: ${esc(catalogLabel(interlinks.classification_catalog, classification))}</strong><p>${esc(localized(disposition, 'why'))}</p>${localized(disposition, 'limitations') ? `<small><strong>${esc(copy.limitations)}:</strong> ${esc(localized(disposition, 'limitations'))}</small>` : ''}${localized(disposition, 'next_source_needed') ? `<small><strong>${esc(copy.nextSource)}:</strong> ${esc(localized(disposition, 'next_source_needed'))}</small>` : ''}${norm(disposition.source_status) ? `<small><strong>${esc(copy.source)}:</strong> ${esc(disposition.source_status)}</small>` : ''}</li>`);
      } else unresolved.push(`<li data-interlink-disposition data-classification="REGISTRY_NOT_AVAILABLE"><strong>${esc(copy.unresolvedReconnection)}</strong><p>${esc(copy.interlinkUnavailable)}</p></li>`);
      if (selected.matches.length) unresolved.push(`<li class="pdim-none"><strong>${esc(copy.selectedCoverage)}</strong><p>${esc(copy.prismCoveredSelected)}</p></li>`);
      reconnection = `<section class="pdim-reconnection" data-isolation-reconnection aria-label="${esc(copy.selectedCoverage)}">
        <div class="pdim-reconnection-identity">${card(selected.record, false)}<div><p><strong>${esc(copy.selectedCoverage)}:</strong> ${esc(selected.matches.length ? copy.prismCoordinate : copy.noPrismCoordinate)}</p><a class="pdim-record-link" href="${esc(`${registerRoute}#record-${encodeURIComponent(selected.id)}`)}">${esc(copy.openRegisterRecord)} →</a></div></div>
        <div class="pdim-reconnection-grid">
          <section data-isolation-direct><h2>${esc(copy.directReconnection)} <small>${selectedRelationships.length} ${esc(copy.relationCount)}</small></h2><p class="pdim-boundary-note">${esc(copy.directBoundary)}</p><ul class="pdim-rel-list">${directHtml}</ul></section>
          <section data-isolation-context><h2>${esc(copy.contextReconnection)} <small>${contextLinkCount} ${esc(copy.bridgeCount)}</small></h2><p class="pdim-warning">${esc(copy.contextBoundary)}</p><ul class="pdim-rel-list">${contextHtml}</ul></section>
          <section data-isolation-unresolved><h2>${esc(copy.unresolvedReconnection)}</h2><ul class="pdim-rel-list">${unresolved.join('')}</ul></section>
        </div>
      </section>`;
    }
    body.innerHTML = `
      <section class="pdim-isolation-head"><div><p class="pdim-note">${esc(copy.isolationLead)}</p><p><strong>${esc(audienceQuestion(prism, state))}</strong></p><p class="pdim-warning">${esc(copy.formalBoundary)}</p><div class="pdim-isolation-coverage" data-isolation-coverage><strong>${coveredOptions.length}/${options.length}</strong><span>${esc(copy.prismCovered)}</span><small>${options.length} ${esc(copy.exactProceedings)} · ${uncoveredOptions.length} ${esc(copy.prismNotCovered)}</small><p>${esc(copy.coverageBoundary)}</p></div></div><div class="pdim-isolation-controls">${audienceControl(prism, state)}<label>${copy.chooseLane}<select data-isolation-id><option value="__FULL__"${selected ? '' : ' selected'}>${copy.fullCorpus}</option>${optionGroups}</select></label><button type="button" data-isolation-restore ${selected ? '' : 'disabled'}>${copy.restore}</button></div></section>
      ${reconnection}
      ${mini}
      <div class="pdim-isolation-grid"><section><h2>${selected ? copy.visibleAlone : copy.fullCorpus}</h2><ul>${selected ? (direct.length ? direct.map(item).join('') : `<li class="pdim-none">${copy.noVisible}</li>`) : `<li><strong>${props.length} ${copy.proposition.toLowerCase()}</strong><p>${esc(localized(prism.boundary, ''))}</p></li>`}</ul></section><section><h2>${copy.disappears}</h2><ul>${selected ? (outside.length ? outside.map(item).join('') : `<li class="pdim-none">${copy.noOutside}</li>`) : `<li class="pdim-none">${copy.noOutside}</li>`}</ul></section></div>
      <div class="pdim-prism-detail" data-prism-detail aria-live="polite" tabindex="-1"><p>${esc(localized(prism.boundary, ''))}</p></div>`;
  }

  async function init() {
    const root = document.querySelector('[data-proceedings-map]'); if (!root) return;
    try {
      const [registerRes, prismRes, interlinkRes] = await Promise.all([
        fetch(registerDataUrl, {cache:'no-store'}),
        fetch(prismUrl, {cache:'no-store'}).catch(() => null),
        fetch(interlinkUrl, {cache:'no-store'}).catch(() => null)
      ]);
      if (!registerRes.ok) throw new Error(`HTTP ${registerRes.status}`);
      const registerPayload = await registerRes.json();
      const rows = Array.isArray(registerPayload && registerPayload.records) ? registerPayload.records : [];
      if (!rows.length || rows.some((record) => !norm(record.Master_ID))) throw new Error('invalid public proceedings projection');
      const byId = new Map(rows.map((r) => [norm(r.Master_ID), r]));
      const tracks = Array.from(new Set(rows.map((r) => norm(r.Stream)).filter(Boolean))).sort((a,b)=>a.localeCompare(b));
      const gaps = rows.filter((r) => norm(r.Open_Reference_Gap)).length;
      let prism = null; let prismFailure = '';
      if (prismRes && prismRes.ok) {
        try {
          const candidate = await prismRes.json();
          const complete = Array.isArray(candidate.lanes) && Array.isArray(candidate.propositions) && candidate.propositions.every((prop) => candidate.lanes.every((lane) => prop.cells && prop.cells[lane.id]));
          if (!complete) throw new Error('incomplete proposition/lane denominator');
          prism = candidate;
        } catch (err) { prismFailure = err.message || String(err); }
      } else prismFailure = prismRes ? `HTTP ${prismRes.status}` : 'fetch failed';
      let interlinks = null; let interlinkFailure = '';
      if (interlinkRes && interlinkRes.ok) {
        try {
          const candidate = await interlinkRes.json();
          if (!Array.isArray(candidate.relationships) || !Array.isArray(candidate.context_clusters) || !Array.isArray(candidate.node_dispositions)) throw new Error('incomplete interlinkability registry');
          interlinks = candidate;
        } catch (err) { interlinkFailure = err.message || String(err); }
      } else interlinkFailure = interlinkRes ? `HTTP ${interlinkRes.status}` : 'fetch failed';
      const exactIds = new Set(rows.filter(isExactProceeding).map((record) => record.Master_ID));
      if (interlinks) {
        const dispositionIds = new Set(interlinks.node_dispositions.map((entry) => entry.master_id));
        const missing = Array.from(exactIds).filter((id) => !dispositionIds.has(id));
        const unexpected = Array.from(dispositionIds).filter((id) => !exactIds.has(id));
        if (missing.length || unexpected.length) {
          interlinkFailure = `interlinkability denominator mismatch (${missing.length} missing; ${unexpected.length} unexpected)`;
          interlinks = null;
        }
      }
      const decodeHashId = (value) => { try { return decodeURIComponent(value || ''); } catch (_err) { return ''; } };
      const readHash = () => {
        const raw = window.location.hash || '';
        if (raw.startsWith('#trace-proceeding=')) {
          const id = decodeHashId(raw.slice('#trace-proceeding='.length));
          return {view:'trace', id:byId.has(id) ? id : ''};
        }
        if (raw.startsWith('#isolation-test=')) {
          const id = decodeHashId(raw.slice('#isolation-test='.length));
          if (exactIds.has(id)) return {view:'isolation', id};
          if (byId.has(id)) return {view:'trace', id, canonicalize:true};
          return {view:'map', id:'', canonicalize:true};
        }
        const mapped = {'#map':'map', '#mapa':'map', '#trace-proceeding':'trace', '#case-prism':'prism', '#parallel-lanes':'lanes', '#isolation-test':'isolation'}[raw];
        return {view:mapped || 'map', id:''};
      };
      const initialHash = readHash();
      const state = { audience: 'all', isolationId: initialHash.view === 'isolation' && initialHash.id ? initialHash.id : '__FULL__', traceId: initialHash.view === 'trace' ? initialHash.id : '' };
      const viewToHash = {trace:'#trace-proceeding', prism:'#case-prism', lanes:'#parallel-lanes', isolation:'#isolation-test'};
      let view = initialHash.view;
      if (!prism && ['prism','lanes','isolation'].includes(view)) view = 'map';
      if (!interlinks && view === 'isolation') view = 'map';
      const directCoverage = interlinks && interlinks.coverage ? interlinks.coverage : {};
      const directGrade = interlinks
        ? `<small>${esc(directCoverage.direct_relationship_source_verified_pair_count)} ${esc(copy.directVerified)} · ${esc(directCoverage.direct_relationship_source_reported_pending_pair_count)} ${esc(copy.directPending)}</small>`
        : '';

      root.innerHTML = `
        <div class="pdim-stats"><div><strong>${rows.length}</strong><span>${copy.records}</span></div><div><strong>${tracks.length}</strong><span>${copy.tracks}</span></div><div><strong>${interlinks ? interlinks.relationships.length : '—'}</strong><span>${copy.direct}${directGrade}</span></div><div><strong>${gaps}</strong><span>${copy.gaps}</span></div></div>
        <div class="pdim-controls"><label>${lang==='es'?'Buscar':'Search'}<input type="search" data-map-search placeholder="${esc(copy.search)}"></label><label>${lang==='es'?'Vía':'Track'}<select data-map-track><option value="">${copy.allTracks}</option>${tracks.map((t)=>`<option>${esc(t)}</option>`).join('')}</select></label></div>
        <div class="pdim-tabs" role="tablist" aria-label="${esc(lang === 'es' ? 'Vistas del mapa de procedimientos' : 'Proceedings map views')}"><button id="pdim-tab-map" role="tab" aria-controls="pdim-view-panel" type="button" data-view="map">${copy.map}</button><button id="pdim-tab-chronology" role="tab" aria-controls="pdim-view-panel" type="button" data-view="chronology">${copy.chronology}</button><button id="pdim-tab-trace" role="tab" aria-controls="pdim-view-panel" type="button" data-view="trace">${copy.trace}</button><button id="pdim-tab-prism" role="tab" aria-controls="pdim-view-panel" type="button" data-view="prism" ${prism ? '' : 'disabled aria-disabled="true"'}>${copy.prism}</button><button id="pdim-tab-lanes" role="tab" aria-controls="pdim-view-panel" type="button" data-view="lanes" ${prism ? '' : 'disabled aria-disabled="true"'}>${copy.lanes}</button><button id="pdim-tab-isolation" role="tab" aria-controls="pdim-view-panel" type="button" data-view="isolation" ${prism && interlinks ? '' : 'disabled aria-disabled="true"'}>${copy.isolation}</button></div>
        ${prism ? '' : `<div class="pdim-prism-unavailable" role="status"><strong>${esc(copy.prismUnavailable)}</strong><small>${esc(prismFailure)}</small></div>`}
        ${interlinks ? '' : `<div class="pdim-prism-unavailable" role="status"><strong>${esc(copy.interlinkUnavailable)}</strong><small>${esc(interlinkFailure)}</small></div>`}
        <div id="pdim-view-panel" role="tabpanel" tabindex="-1" data-view-body></div>
        <section class="pdim-trace-panel" data-trace-panel></section>
        <footer class="pdim-footer"><p>${copy.publicBoundary}</p><a href="${esc(registerRoute)}">${copy.openRegister} →</a></footer>`;

      const filters = { search: root.querySelector('[data-map-search]'), track: root.querySelector('[data-map-track]') };
      const draw = (focusSelector = '') => {
        const tracePanel = root.querySelector('[data-trace-panel]');
        if (view !== 'trace' && tracePanel) tracePanel.innerHTML = '';
        if (view === 'chronology') renderChronology(root, rows, filters);
        else if (view === 'trace') {
          const body = root.querySelector('[data-view-body]');
          body.innerHTML = `<div class="pdim-picker"><label>${copy.trace}<select data-trace-select><option value="">—</option>${rows.slice().sort((a,b)=>labelFor(a).localeCompare(labelFor(b))).map((r)=>`<option value="${esc(r.Master_ID)}"${state.traceId === r.Master_ID ? ' selected' : ''}>${esc(r.Master_ID)} · ${esc(labelFor(r))}</option>`).join('')}</select></label></div>`;
          if (state.traceId && byId.has(state.traceId)) renderTrace(root, state.traceId, byId, prism, interlinks);
        } else if (view === 'prism' && prism) renderPrism(root, prism, state);
        else if (view === 'lanes' && prism) renderParallelLanes(root, prism, state);
        else if (view === 'isolation' && prism && interlinks) renderIsolation(root, prism, interlinks, state, byId, rows);
        else renderMap(root, rows, filters);
        if (focusSelector) window.requestAnimationFrame(() => root.querySelector(focusSelector)?.focus({preventScroll:true}));
      };
      const revealActivePanel = () => window.requestAnimationFrame(() => {
        const panel = root.querySelector('[data-view-body]');
        if (!panel) return;
        panel.focus({preventScroll:true});
        const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        panel.scrollIntoView({behavior: reduced ? 'auto' : 'smooth', block:'start'});
      });
      const setTabState = () => root.querySelectorAll('[data-view]').forEach((button) => {
        const selected = button.dataset.view === view;
        button.setAttribute('aria-selected', selected ? 'true' : 'false');
        button.setAttribute('tabindex', selected ? '0' : '-1');
        if (selected) root.querySelector('[data-view-body]')?.setAttribute('aria-labelledby', button.id);
      });
      const activeHash = () => {
        if (view === 'trace' && state.traceId && byId.has(state.traceId)) return `#trace-proceeding=${encodeURIComponent(state.traceId)}`;
        if (view === 'isolation' && state.isolationId !== '__FULL__' && exactIds.has(state.isolationId)) return `#isolation-test=${encodeURIComponent(state.isolationId)}`;
        return viewToHash[view] || '';
      };
      const replaceActiveHash = () => {
        const hash = activeHash();
        window.history.replaceState(null, '', hash || (window.location.pathname + window.location.search));
      };
      const activateView = (next, updateHash = true, reveal = false) => {
        if (!next || (!prism && ['prism','lanes','isolation'].includes(next))) return;
        if (next === 'isolation' && !interlinks) return;
        view = next; setTabState(); draw();
        if (reveal) revealActivePanel();
        if (updateHash) replaceActiveHash();
      };
      filters.search.addEventListener('input', () => draw()); filters.track.addEventListener('input', () => draw());
      root.querySelectorAll('[data-view]').forEach((button) => button.addEventListener('click', () => activateView(button.dataset.view)));
      root.querySelector('.pdim-tabs').addEventListener('keydown', (ev) => {
        if (!['ArrowLeft','ArrowRight','Home','End'].includes(ev.key)) return;
        const tabs = Array.from(root.querySelectorAll('[data-view]:not([disabled])'));
        const current = tabs.indexOf(document.activeElement); if (current < 0) return;
        ev.preventDefault();
        const target = ev.key === 'Home' ? 0 : ev.key === 'End' ? tabs.length - 1 : (current + (ev.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
        tabs[target].focus(); activateView(tabs[target].dataset.view);
      });
      root.addEventListener('click', (ev) => {
        const traceButton = ev.target.closest('[data-trace-id]');
        if (traceButton && byId.has(traceButton.dataset.traceId)) { state.traceId = traceButton.dataset.traceId; activateView('trace'); return; }
        const restoreButton = ev.target.closest('[data-isolation-restore]');
        if (restoreButton) { state.isolationId = '__FULL__'; draw('[data-isolation-id]'); replaceActiveHash(); return; }
        const prismButton = ev.target.closest('[data-prism-prop][data-prism-lane]');
        if (prismButton && prism) {
          const detailScope = prismButton.closest('[data-trace-panel], [data-view-body]') || root;
          renderPrismDetail(detailScope, prism, prismButton.dataset.prismProp, prismButton.dataset.prismLane);
        }
      });
      root.addEventListener('change', (ev) => {
        if (ev.target.matches('[data-trace-select]') && ev.target.value && byId.has(ev.target.value)) { state.traceId = ev.target.value; renderTrace(root, state.traceId, byId, prism, interlinks); replaceActiveHash(); }
        if (ev.target.matches('[data-prism-audience]')) { state.audience = ev.target.value || 'all'; draw('[data-prism-audience]'); }
        if (ev.target.matches('[data-isolation-id]')) { state.isolationId = exactIds.has(ev.target.value) ? ev.target.value : '__FULL__'; draw('[data-isolation-id]'); replaceActiveHash(); }
      });
      window.addEventListener('hashchange', () => {
        const parsed = readHash();
        state.traceId = parsed.view === 'trace' ? parsed.id : state.traceId;
        state.isolationId = parsed.view === 'isolation' && parsed.id ? parsed.id : '__FULL__';
        activateView(parsed.view, false, true);
        if (parsed.canonicalize) replaceActiveHash();
      });
      setTabState(); draw();
      if (initialHash.canonicalize) replaceActiveHash();
      if (initialHash.view !== 'map' || ['#map','#mapa'].includes(window.location.hash)) revealActivePanel();
    } catch (err) {
      root.innerHTML = `<div class="pdim-error"><strong>${copy.error}</strong><p>${esc(err.message || err)}</p></div>`;
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once:true}); else init();
})();

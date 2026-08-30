(() => {
  'use strict';

  const script = document.currentScript;
  if (!script) return;
  const assetBase = new URL('.', script.src);
  const repoBase = new URL('../', assetBase);
  const csvUrl = new URL('archive/PROCEEDINGS_MASTER_REGISTER.csv', repoBase).href;
  const prismUrl = new URL('assets/data/proceedings-case-prism-v1.json', repoBase).href;
  const lang = (document.documentElement.lang || 'en').toLowerCase().startsWith('es') ? 'es' : 'en';
  const registerRoute = new URL(lang === 'es' ? 'es/registro-maestro-procedimientos/' : 'en/master-proceedings-register/', repoBase).href;

  const copy = lang === 'es' ? {
    loading: 'Construyendo el mapa desde el registro canónico…',
    error: 'No se pudo construir el mapa de procedimientos.',
    allTracks: 'Todas las vías', search: 'Buscar ID, referencia, órgano, objeto o estado…',
    map: 'Mapa por vías', chronology: 'Cronología', trace: 'Trazar un procedimiento',
    prism: 'Prisma del caso', lanes: 'Vías paralelas', isolation: 'Prueba de aislamiento',
    records: 'nodos públicos', tracks: 'vías', direct: 'relaciones procesales explícitas', gaps: 'nodos con brecha abierta',
    directTitle: 'Relaciones procesales directas', incoming: 'Entrantes / hacia este nodo', outgoing: 'Salientes / desde este nodo',
    contextTitle: 'Puentes de contexto', sameTrack: 'Misma vía', sameConnection: 'Misma conexión registrada', sameGeo: 'Misma geografía',
    why: 'Por qué están conectados', noDirect: 'No hay otra relación procesal directa codificada con ID canónico en los campos públicos actuales.',
    noContext: 'No hay otro puente contextual exacto en la proyección actual.',
    contextWarning: 'Contexto no significa mismo procedimiento, acumulación, coordinación, conocimiento, ilicitud ni responsabilidad.',
    source: 'Fuente/estado', gap: 'Brecha abierta', now: 'Ahora', parent: 'Padre', child: 'Hijo', linked: 'Enlace explícito', review: 'Recurso/revisión',
    directWhyParent: 'El registro canónico identifica expresamente este procedimiento como padre/origen del otro.',
    directWhyLinked: 'El campo de procedimientos enlazados contiene expresamente el ID canónico del otro nodo.',
    directWhyReview: 'El campo de recurso/revisión contiene expresamente el ID canónico del otro nodo.',
    sameTrackWhy: 'Ambos nodos comparten la misma vía/stream registrada. Es una lente de navegación, no una relación procesal.',
    sameConnectionWhy: 'Ambos nodos tienen exactamente el mismo valor no vacío en Connection. Es contexto registrado, no una conclusión de acumulación o causalidad.',
    sameGeoWhy: 'Ambos nodos comparten la misma geografía registrada. Es contexto de navegación únicamente.',
    approximate: 'Orden aproximado por el primer año reconocible en Date_or_Period; no implica causalidad.',
    openRegister: 'Abrir Registro Maestro', traceThis: 'Trazar', empty: 'No hay nodos que coincidan con los filtros.',
    publicBoundary: 'Esta visualización es una proyección pública del mismo CSV canónico. No convierte referencias en procedimientos ni conexiones contextuales en hechos jurídicos.',
    audience: 'Lente del lector', proposition: 'Proposición / hecho a contrastar', status: 'Relación', treatment: 'Tratamiento en el expediente', period: 'Periodo',
    matrixLead: 'Una misma proposición, leída horizontalmente a través de procedimientos jurídicamente separados.',
    lanesLead: 'Orden cronológico de las proposiciones controladas y las vías en las que aparecen de forma directa, contextual o abierta.',
    isolationLead: 'Selecciona un procedimiento exacto. El modo aislado conserva solo lo directamente presente en ese expediente y atenúa el resto del corpus; la restauración permite comparar de inmediato.',
    chooseLane: 'Seleccionar procedimiento', visibleAlone: 'Permanece visible en el expediente seleccionado', disappears: 'Contexto material que desaparece al leerlo solo',
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
    swimCaption: 'Cronología en vías paralelas; cada columna sigue siendo un expediente o carril institucional separado'
  } : {
    loading: 'Building the map from the canonical register…',
    error: 'The proceedings map could not be built.',
    allTracks: 'All tracks', search: 'Search ID, reference, organ, object or status…',
    map: 'Track map', chronology: 'Chronology', trace: 'Trace one proceeding',
    prism: 'Case Prism', lanes: 'Parallel lanes', isolation: 'Isolation test',
    records: 'public nodes', tracks: 'tracks', direct: 'explicit procedural relations', gaps: 'nodes with an open gap',
    directTitle: 'Direct procedural relationships', incoming: 'Incoming / toward this node', outgoing: 'Outgoing / from this node',
    contextTitle: 'Context bridges', sameTrack: 'Same track', sameConnection: 'Same recorded connection', sameGeo: 'Same geography',
    why: 'Why connected?', noDirect: 'No other direct procedural relationship encoded with a canonical ID is currently exposed by the public fields.',
    noContext: 'No other exact contextual bridge is available in the current projection.',
    contextWarning: 'Context does not mean the same proceeding, joinder, coordination, knowledge, wrongdoing or liability.',
    source: 'Source/status', gap: 'Open gap', now: 'Now', parent: 'Parent', child: 'Child', linked: 'Explicit link', review: 'Appeal/review',
    directWhyParent: 'The canonical register expressly records one proceeding as the parent/origin of the other.',
    directWhyLinked: 'The linked-proceedings field expressly contains the other node’s canonical ID.',
    directWhyReview: 'The appeal/review field expressly contains the other node’s canonical ID.',
    sameTrackWhy: 'Both nodes share the same recorded stream/track. This is a navigation lens, not a procedural relationship.',
    sameConnectionWhy: 'Both nodes have exactly the same non-empty Connection value. This is recorded context, not a finding of joinder or causation.',
    sameGeoWhy: 'Both nodes share the same recorded geography. This is navigation context only.',
    approximate: 'Approximate order by the first recognisable year in Date_or_Period; it does not imply causation.',
    openRegister: 'Open Master Register', traceThis: 'Trace', empty: 'No nodes match the current filters.',
    publicBoundary: 'This visualisation is a public projection of the same canonical CSV. It does not turn references into proceedings or contextual connections into legal facts.',
    audience: 'Reader lens', proposition: 'Proposition / fact to test', status: 'Relationship', treatment: 'Treatment in file', period: 'Period',
    matrixLead: 'One proposition, read horizontally across legally separate proceedings.',
    lanesLead: 'Chronological order of the controlled propositions and the lanes in which they appear as direct, contextual or open.',
    isolationLead: 'Select one exact proceeding. Isolated mode keeps only what is directly present in that file and fades the wider corpus; restore it for an immediate comparison.',
    chooseLane: 'Select proceeding', visibleAlone: 'Remains visible in the selected file', disappears: 'Material context that disappears when read alone',
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
    swimCaption: 'Parallel-lane chronology; every column remains a separate proceeding or institutional lane'
  };

  const esc = (v) => String(v || '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const norm = (v) => String(v || '').trim();
  const key = (v) => norm(v).toLowerCase();
  const localized = (obj, base) => obj ? (obj[`${base}_${lang}`] || obj[lang] || obj[base] || obj.en || obj.es || '') : '';

  function parseCsv(text) {
    const table = []; let row = []; let field = ''; let quoted = false;
    for (let i = 0; i < text.length; i += 1) {
      const ch = text[i];
      if (quoted) {
        if (ch === '"' && text[i + 1] === '"') { field += '"'; i += 1; }
        else if (ch === '"') quoted = false;
        else field += ch;
      } else if (ch === '"') quoted = true;
      else if (ch === ',') { row.push(field); field = ''; }
      else if (ch === '\n') { row.push(field.replace(/\r$/, '')); table.push(row); row = []; field = ''; }
      else field += ch;
    }
    if (field.length || row.length) { row.push(field.replace(/\r$/, '')); table.push(row); }
    if (!table.length) return [];
    const headers = table.shift();
    return table.filter((r) => r.some((v) => norm(v))).map((r) => {
      const out = {}; headers.forEach((h, i) => { out[h] = r[i] || ''; }); return out;
    });
  }

  const isPublic = (r) => {
    const t = norm(r.Public_Treatment).toUpperCase();
    return !(t.includes('INTERNAL_ONLY') || t.includes('PRIVATE') || t.includes('NOT_SITE_AGGREGATED'));
  };

  const idsIn = (value, byId) => {
    const found = [];
    const text = String(value || '');
    byId.forEach((_r, id) => { if (text.includes(id)) found.push(id); });
    return found;
  };

  const firstYear = (value) => {
    const m = String(value || '').match(/\b(19|20)\d{2}\b/);
    return m ? Number(m[0]) : 9999;
  };

  const labelFor = (r) => norm(r.Reference) || norm(r.Secondary_Reference) || norm(r.Master_ID);
  const subtitleFor = (r) => [norm(r.Proceeding_Class), norm(r.Stream)].filter(Boolean).join(' · ');

  const card = (r, traceButton = true) => `
    <article class="pdim-node" data-node-id="${esc(r.Master_ID)}">
      <div class="pdim-node-head"><span class="pdim-id">${esc(r.Master_ID)}</span><span class="pdim-state" data-state="${esc(norm(r.Is_Proceeding).toUpperCase() || 'UNVERIFIED')}">${esc(norm(r.Is_Proceeding).toUpperCase() || 'UNVERIFIED')}</span></div>
      <h3>${esc(labelFor(r))}</h3>
      <p class="pdim-sub">${esc(subtitleFor(r))}</p>
      <p>${esc([r.Connection, r.Object_or_Purpose].filter(Boolean).join(' — '))}</p>
      <div class="pdim-node-meta"><span>${esc(r.Date_or_Period)}</span><span>${esc(r.Origin_Organ)}</span></div>
      ${traceButton ? `<button type="button" data-trace-id="${esc(r.Master_ID)}">${copy.traceThis} →</button>` : ''}
    </article>`;

  function buildEdges(rows, byId) {
    const edges = []; const seen = new Set();
    const add = (from, to, type, why, derived = false) => {
      if (!byId.has(from) || !byId.has(to) || from === to) return;
      const sig = [from, to, type].join('|'); if (seen.has(sig)) return; seen.add(sig);
      edges.push({ from, to, type, why, derived });
    };
    rows.forEach((r) => {
      const id = norm(r.Master_ID);
      const parent = norm(r.Parent_Master_ID);
      if (parent && byId.has(parent)) add(parent, id, 'PARENT_CHILD', copy.directWhyParent, false);
      idsIn(r.Linked_Proceedings, byId).forEach((other) => add(id, other, 'LINKED', copy.directWhyLinked, false));
      idsIn(r.Appeal_or_Review, byId).forEach((other) => add(id, other, 'REVIEW', copy.directWhyReview, false));
    });
    const priority = {PARENT_CHILD: 0, REVIEW: 1, LINKED: 2};
    const byPair = new Map();
    edges.forEach((edge) => {
      const pair = [edge.from, edge.to].sort().join('|');
      const current = byPair.get(pair);
      if (!current || priority[edge.type] < priority[current.type]) byPair.set(pair, edge);
    });
    return Array.from(byPair.values());
  }

  function relationshipLabel(edge, selected) {
    if (edge.type === 'PARENT_CHILD') return edge.from === selected ? copy.child : copy.parent;
    if (edge.type === 'REVIEW') return copy.review;
    return copy.linked;
  }

  function renderTrace(root, selected, rows, byId, edges, prism) {
    const r = byId.get(selected); if (!r) return;
    const direct = edges.filter((e) => e.from === selected || e.to === selected);
    const directHtml = direct.length ? direct.map((e) => {
      const otherId = e.from === selected ? e.to : e.from; const other = byId.get(otherId);
      return `<li><button type="button" data-trace-id="${esc(otherId)}"><strong>${esc(relationshipLabel(e, selected))}</strong> · ${esc(otherId)} · ${esc(labelFor(other))}</button><p>${esc(e.why)}</p></li>`;
    }).join('') : `<li class="pdim-none">${copy.noDirect}</li>`;

    const contexts = [];
    const addContext = (type, reason, other) => contexts.push({type, reason, other});
    rows.forEach((o) => {
      if (o.Master_ID === selected) return;
      if (norm(r.Stream) && key(r.Stream) === key(o.Stream)) addContext(copy.sameTrack, copy.sameTrackWhy, o);
      if (norm(r.Connection) && key(r.Connection) === key(o.Connection)) addContext(copy.sameConnection, copy.sameConnectionWhy, o);
      if (norm(r.Geography) && key(r.Geography) === key(o.Geography)) addContext(copy.sameGeo, copy.sameGeoWhy, o);
    });
    const uniq = new Map(); contexts.forEach((c) => { const s = `${c.type}|${c.other.Master_ID}`; if (!uniq.has(s)) uniq.set(s, c); });
    const contextHtml = uniq.size ? Array.from(uniq.values()).slice(0, 36).map((c) => `<li><button type="button" data-trace-id="${esc(c.other.Master_ID)}"><strong>${esc(c.type)}</strong> · ${esc(c.other.Master_ID)} · ${esc(labelFor(c.other))}</button><p>${esc(c.reason)}</p></li>`).join('') : `<li class="pdim-none">${copy.noContext}</li>`;

    const prismMatches = prism ? prism.propositions.flatMap((prop) => prism.lanes.flatMap((lane) => {
      const cell = prop.cells && prop.cells[lane.id];
      return cell && Array.isArray(cell.master_ids) && cell.master_ids.includes(selected) && cell.status !== 'OUTSIDE'
        ? [{prop, lane, cell}] : [];
    })) : [];
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
      ${ids.length ? `<div class="pdim-prism-id-list"><strong>${copy.masterIds}</strong>${ids.map((id) => `<button type="button" data-trace-id="${esc(id)}">${esc(id)} · ${copy.openTrace}</button>`).join('')}</div>` : ''}`;
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

  function renderIsolation(root, prism, state, byId) {
    const body = root.querySelector('[data-view-body]');
    const options = prism.lanes.flatMap((lane) => lane.master_ids.map((id) => ({lane, id, record: byId.get(id)}))).filter((item) => item.record && norm(item.record.Is_Proceeding).toUpperCase() === 'TRUE');
    if (!state.isolationId || (state.isolationId !== '__FULL__' && !options.some((item) => item.id === state.isolationId))) state.isolationId = '__FULL__';
    const selected = options.find((item) => item.id === state.isolationId) || null;
    const props = sortedProps(prism, state.audience);
    const direct = [];
    const outside = [];
    if (selected) props.forEach((prop) => {
      const selectedCell = prop.cells[selected.lane.id];
      const remains = selectedCell.status === 'DIRECT' && selectedCell.master_ids.includes(selected.id);
      const sourceLanes = prism.lanes.filter((lane) => {
        const cell = prop.cells[lane.id];
        return cell.status !== 'OUTSIDE' && !(lane.id === selected.lane.id && cell.status === 'DIRECT' && cell.master_ids.includes(selected.id));
      });
      if (remains) direct.push({prop, cell:selectedCell, lane:selected.lane});
      else if (sourceLanes.length) outside.push({prop, cell:selectedCell, lane:selected.lane, sourceLanes});
    });
    const item = ({prop, cell, lane, sourceLanes=[]}) => `<li><button type="button" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><span class="pdim-prism-status" data-prism-status="${esc(cell.status)}">${esc(statusLabel(prism, cell.status))}</span><strong>${esc(propTitle(prop))}</strong></button><p>${esc(cellNote(cell))}</p>${sourceLanes.length ? `<small><strong>${copy.laneSource}:</strong> ${esc(sourceLanes.map((sourceLane) => `${laneLabel(sourceLane)} — ${statusLabel(prism, prop.cells[sourceLane.id].status)}`).join(' · '))}</small>` : ''}</li>`;
    const mini = `<div class="pdim-isolation-map" data-isolation-mode="${selected ? 'isolated' : 'full'}"><table><caption>${selected ? `${copy.isolatedMode}: ${selected.id}` : copy.fullCorpus}</caption><thead><tr><th scope="col">${copy.proposition}</th>${prism.lanes.map((lane) => `<th scope="col">${esc(laneLabel(lane))}</th>`).join('')}</tr></thead><tbody>${props.map((prop) => `<tr><th scope="row">${esc(prop.id)} · ${esc(propTitle(prop))}</th>${prism.lanes.map((lane) => { const cell = prop.cells[lane.id]; const active = !selected || (lane.id === selected.lane.id && cell.status === 'DIRECT' && cell.master_ids.includes(selected.id)); const selectionState = !selected ? '' : (active ? copy.insideSelected : copy.outsideSelected); const accessibleState = selectionState ? ` · ${selectionState}` : ''; const suppression = selected && !active ? ' disabled aria-disabled="true" tabindex="-1"' : ''; return `<td class="${active ? '' : 'is-suppressed'}"><button type="button"${suppression} aria-label="${esc(`${statusLabel(prism, cell.status)}${accessibleState}`)}" data-prism-status="${esc(cell.status)}" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><span>${esc(statusLabel(prism, cell.status))}</span>${selected ? `<small>${esc(selectionState)}</small>` : ''}</button></td>`; }).join('')}</tr>`).join('')}</tbody></table></div>`;
    body.innerHTML = `
      <section class="pdim-isolation-head"><div><p class="pdim-note">${esc(copy.isolationLead)}</p><p><strong>${esc(audienceQuestion(prism, state))}</strong></p><p class="pdim-warning">${esc(copy.formalBoundary)}</p></div><div class="pdim-isolation-controls">${audienceControl(prism, state)}<label>${copy.chooseLane}<select data-isolation-id><option value="__FULL__"${selected ? '' : ' selected'}>${copy.fullCorpus}</option>${options.map((item) => `<option value="${esc(item.id)}"${selected && item.id === selected.id ? ' selected' : ''}>${esc(item.id)} · ${esc(labelFor(item.record))}</option>`).join('')}</select></label><button type="button" data-isolation-restore ${selected ? '' : 'disabled'}>${copy.restore}</button></div></section>
      ${mini}
      <div class="pdim-isolation-grid"><section><h2>${selected ? copy.visibleAlone : copy.fullCorpus}</h2><ul>${selected ? (direct.length ? direct.map(item).join('') : `<li class="pdim-none">${copy.noVisible}</li>`) : `<li><strong>${props.length} ${copy.proposition.toLowerCase()}</strong><p>${esc(localized(prism.boundary, ''))}</p></li>`}</ul></section><section><h2>${copy.disappears}</h2><ul>${selected ? (outside.length ? outside.map(item).join('') : `<li class="pdim-none">${copy.noOutside}</li>`) : `<li class="pdim-none">${copy.noOutside}</li>`}</ul></section></div>
      <div class="pdim-prism-detail" data-prism-detail aria-live="polite" tabindex="-1"><p>${esc(localized(prism.boundary, ''))}</p></div>`;
  }

  async function init() {
    const root = document.querySelector('[data-proceedings-map]'); if (!root) return;
    try {
      const [csvRes, prismRes] = await Promise.all([
        fetch(csvUrl, {cache:'no-store'}),
        fetch(prismUrl, {cache:'no-store'}).catch(() => null)
      ]);
      if (!csvRes.ok) throw new Error(`HTTP ${csvRes.status}`);
      const all = parseCsv(await csvRes.text()); const rows = all.filter(isPublic);
      const byId = new Map(rows.map((r) => [norm(r.Master_ID), r]));
      const edges = buildEdges(rows, byId);
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
      const state = { audience: 'all', isolationId: '__FULL__' };
      const hashToView = {'#map':'map', '#mapa':'map', '#case-prism':'prism', '#parallel-lanes':'lanes', '#isolation-test':'isolation'};
      const viewToHash = {prism:'#case-prism', lanes:'#parallel-lanes', isolation:'#isolation-test'};
      let view = hashToView[window.location.hash] && prism ? hashToView[window.location.hash] : 'map';

      root.innerHTML = `
        <div class="pdim-stats"><div><strong>${rows.length}</strong><span>${copy.records}</span></div><div><strong>${tracks.length}</strong><span>${copy.tracks}</span></div><div><strong>${edges.length}</strong><span>${copy.direct}</span></div><div><strong>${gaps}</strong><span>${copy.gaps}</span></div></div>
        <div class="pdim-controls"><label>${lang==='es'?'Buscar':'Search'}<input type="search" data-map-search placeholder="${esc(copy.search)}"></label><label>${lang==='es'?'Vía':'Track'}<select data-map-track><option value="">${copy.allTracks}</option>${tracks.map((t)=>`<option>${esc(t)}</option>`).join('')}</select></label></div>
        <div class="pdim-tabs" role="tablist" aria-label="${esc(lang === 'es' ? 'Vistas del mapa de procedimientos' : 'Proceedings map views')}"><button id="pdim-tab-map" role="tab" aria-controls="pdim-view-panel" type="button" data-view="map">${copy.map}</button><button id="pdim-tab-chronology" role="tab" aria-controls="pdim-view-panel" type="button" data-view="chronology">${copy.chronology}</button><button id="pdim-tab-trace" role="tab" aria-controls="pdim-view-panel" type="button" data-view="trace">${copy.trace}</button><button id="pdim-tab-prism" role="tab" aria-controls="pdim-view-panel" type="button" data-view="prism" ${prism ? '' : 'disabled aria-disabled="true"'}>${copy.prism}</button><button id="pdim-tab-lanes" role="tab" aria-controls="pdim-view-panel" type="button" data-view="lanes" ${prism ? '' : 'disabled aria-disabled="true"'}>${copy.lanes}</button><button id="pdim-tab-isolation" role="tab" aria-controls="pdim-view-panel" type="button" data-view="isolation" ${prism ? '' : 'disabled aria-disabled="true"'}>${copy.isolation}</button></div>
        ${prism ? '' : `<div class="pdim-prism-unavailable" role="status"><strong>${esc(copy.prismUnavailable)}</strong><small>${esc(prismFailure)}</small></div>`}
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
          body.innerHTML = `<div class="pdim-picker"><label>${copy.trace}<select data-trace-select><option value="">—</option>${rows.slice().sort((a,b)=>labelFor(a).localeCompare(labelFor(b))).map((r)=>`<option value="${esc(r.Master_ID)}">${esc(r.Master_ID)} · ${esc(labelFor(r))}</option>`).join('')}</select></label></div>`;
        } else if (view === 'prism' && prism) renderPrism(root, prism, state);
        else if (view === 'lanes' && prism) renderParallelLanes(root, prism, state);
        else if (view === 'isolation' && prism) renderIsolation(root, prism, state, byId);
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
      const activateView = (next, updateHash = true, reveal = false) => {
        if (!next || (!prism && ['prism','lanes','isolation'].includes(next))) return;
        view = next; setTabState(); draw();
        if (reveal) revealActivePanel();
        if (updateHash) {
          const hash = viewToHash[view] || `${window.location.pathname}${window.location.search}`;
          if (viewToHash[view]) window.history.replaceState(null, '', hash);
          else window.history.replaceState(null, '', window.location.pathname + window.location.search);
        }
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
        if (traceButton) { renderTrace(root, traceButton.dataset.traceId, rows, byId, edges, prism); return; }
        const restoreButton = ev.target.closest('[data-isolation-restore]');
        if (restoreButton) { state.isolationId = '__FULL__'; draw('[data-isolation-id]'); return; }
        const prismButton = ev.target.closest('[data-prism-prop][data-prism-lane]');
        if (prismButton && prism) {
          const detailScope = prismButton.closest('[data-trace-panel], [data-view-body]') || root;
          renderPrismDetail(detailScope, prism, prismButton.dataset.prismProp, prismButton.dataset.prismLane);
        }
      });
      root.addEventListener('change', (ev) => {
        if (ev.target.matches('[data-trace-select]') && ev.target.value) renderTrace(root, ev.target.value, rows, byId, edges, prism);
        if (ev.target.matches('[data-prism-audience]')) { state.audience = ev.target.value || 'all'; draw('[data-prism-audience]'); }
        if (ev.target.matches('[data-isolation-id]')) { state.isolationId = ev.target.value || '__FULL__'; draw('[data-isolation-id]'); }
      });
      window.addEventListener('hashchange', () => {
        const mapped = hashToView[window.location.hash];
        activateView(mapped || 'map', false, Boolean(mapped));
      });
      setTabState(); draw();
      if (hashToView[window.location.hash]) revealActivePanel();
    } catch (err) {
      root.innerHTML = `<div class="pdim-error"><strong>${copy.error}</strong><p>${esc(err.message || err)}</p></div>`;
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once:true}); else init();
})();

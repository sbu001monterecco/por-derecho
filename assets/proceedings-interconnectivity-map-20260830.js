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
    audience: 'Lente del lector', proposition: 'Proposición / hecho a contrastar', status: 'Estado', period: 'Periodo',
    matrixLead: 'Una misma proposición, leída horizontalmente a través de procedimientos jurídicamente separados.',
    lanesLead: 'Orden cronológico de las proposiciones controladas y las vías en las que aparecen de forma directa, contextual o abierta.',
    isolationLead: 'Selecciona una vía. La primera columna muestra lo que esa vía contiene directamente; la segunda muestra contexto material controlado que no aparece como contenido directo de esa vía.',
    chooseLane: 'Seleccionar vía', visibleAlone: 'Visible en la vía seleccionada', disappears: 'Contexto material fuera de la vía seleccionada',
    noVisible: 'No hay una proposición de este prisma marcada como directa en esta vía.', noOutside: 'No hay contexto adicional marcado para esta vía en el prisma controlado.',
    detail: 'Detalle de la dependencia', masterIds: 'IDs canónicos relacionados', openTrace: 'Abrir traza',
    formalBoundary: 'La prueba de aislamiento es metodológica. No demuestra que el órgano recibiera, debiera admitir o debiera valorar el material externo.'
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
    audience: 'Reader lens', proposition: 'Proposition / fact to test', status: 'Status', period: 'Period',
    matrixLead: 'One proposition, read horizontally across legally separate proceedings.',
    lanesLead: 'Chronological order of the controlled propositions and the lanes in which they appear as direct, contextual or open.',
    isolationLead: 'Select one lane. The first column shows what that lane contains directly; the second shows controlled material context that is not direct content of that lane.',
    chooseLane: 'Select lane', visibleAlone: 'Visible in the selected lane', disappears: 'Material context outside the selected lane',
    noVisible: 'No proposition in this prism is marked direct in this lane.', noOutside: 'No additional contextual proposition is marked for this lane in the controlled prism.',
    detail: 'Dependency detail', masterIds: 'Related canonical IDs', openTrace: 'Open trace',
    formalBoundary: 'The isolation test is methodological. It does not prove that the organ received, should admit or should assess the external material.'
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
    return edges;
  }

  function relationshipLabel(edge, selected) {
    if (edge.type === 'PARENT_CHILD') return edge.from === selected ? copy.child : copy.parent;
    if (edge.type === 'REVIEW') return copy.review;
    return copy.linked;
  }

  function renderTrace(root, selected, rows, byId, edges) {
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

    const holder = root.querySelector('[data-trace-panel]');
    holder.innerHTML = `
      <div class="pdim-trace-identity">${card(r, false)}
        <dl><div><dt>${copy.source}</dt><dd>${esc(r.Source_Status || '—')}</dd></div><div><dt>${copy.gap}</dt><dd>${esc(r.Open_Reference_Gap || '—')}</dd></div><div><dt>${copy.now}</dt><dd>${esc([r.Current_Custodian, r.Status, r.Latest_Known_Event].filter(Boolean).join(' — ') || '—')}</dd></div></dl>
      </div>
      <div class="pdim-rel-grid">
        <section><h2>${copy.directTitle}</h2><ul class="pdim-rel-list">${directHtml}</ul></section>
        <section><h2>${copy.contextTitle}</h2><p class="pdim-warning">${copy.contextWarning}</p><ul class="pdim-rel-list">${contextHtml}</ul></section>
      </div>`;
    holder.scrollIntoView({behavior:'smooth', block:'start'});
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
  const cellNote = (cell) => localized(cell, 'note');

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

  function renderPrismDetail(root, prism, propId, laneId) {
    const prop = prism.propositions.find((p) => p.id === propId);
    const lane = prism.lanes.find((l) => l.id === laneId);
    if (!prop || !lane) return;
    const cell = prop.cells && prop.cells[laneId];
    const holder = root.querySelector('[data-prism-detail]');
    if (!holder) return;
    const ids = cell && Array.isArray(cell.master_ids) ? cell.master_ids : [];
    holder.innerHTML = `
      <div class="pdim-prism-detail-head"><div><span class="pdim-id">${esc(prop.id)} · ${esc(prop.period || '')}</span><h3>${esc(propTitle(prop))}</h3></div><span class="pdim-prism-status" data-prism-status="${esc(cell ? cell.status : 'OUTSIDE')}">${esc(statusLabel(prism, cell ? cell.status : 'OUTSIDE'))}</span></div>
      <p><strong>${esc(laneLabel(lane))}</strong> — ${esc(cell ? cellNote(cell) : (lang === 'es' ? 'No hay una relación específica codificada para esta proposición y esta vía.' : 'No specific relationship is encoded for this proposition and lane.'))}</p>
      <p class="pdim-sub"><strong>${copy.why}:</strong> ${esc(propQuestion(prop))}</p>
      <p class="pdim-sub"><strong>${copy.source}:</strong> ${esc(prop.source_status || '—')}</p>
      ${ids.length ? `<div class="pdim-prism-id-list"><strong>${copy.masterIds}</strong>${ids.map((id) => `<button type="button" data-trace-id="${esc(id)}">${esc(id)} · ${copy.openTrace}</button>`).join('')}</div>` : ''}`;
  }

  function audienceControl(prism, state) {
    return `<label class="pdim-prism-audience">${copy.audience}<select data-prism-audience>${prism.audience_lenses.map((a) => `<option value="${esc(a.id)}"${a.id === state.audience ? ' selected' : ''}>${esc(localized(a, ''))}</option>`).join('')}</select></label>`;
  }

  function audienceQuestion(prism, state) {
    const lens = prism.audience_lenses.find((a) => a.id === state.audience) || prism.audience_lenses[0];
    return localized(lens, 'question');
  }

  function renderPrism(root, prism, state) {
    const body = root.querySelector('[data-view-body]');
    const props = sortedProps(prism, state.audience);
    body.innerHTML = `
      <section class="pdim-prism-head"><div><p class="pdim-note">${esc(copy.matrixLead)}</p><p><strong>${esc(audienceQuestion(prism, state))}</strong></p></div>${audienceControl(prism, state)}</section>
      <div class="pdim-prism-table-wrap"><table class="pdim-prism-table"><thead><tr><th>${copy.proposition}</th>${prism.lanes.map((lane) => `<th>${esc(laneLabel(lane))}</th>`).join('')}</tr></thead><tbody>${props.map((prop) => `<tr><th scope="row"><span>${esc(prop.period || '')}</span><strong>${esc(propTitle(prop))}</strong><small>${esc(prop.source_status || '')}</small></th>${prism.lanes.map((lane) => { const cell = prop.cells && prop.cells[lane.id]; return `<td>${cell ? `<button type="button" class="pdim-prism-cell" data-prism-status="${esc(cell.status)}" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><span>${esc(statusLabel(prism, cell.status))}</span></button>` : '<span class="pdim-prism-dash">—</span>'}</td>`; }).join('')}</tr>`).join('')}</tbody></table></div>
      <div class="pdim-prism-legend">${Object.entries(prism.statuses).map(([status, meta]) => `<span data-prism-status="${esc(status)}"><b></b>${esc(localized(meta, ''))}</span>`).join('')}</div>
      <div class="pdim-prism-detail" data-prism-detail><p>${esc(localized(prism.boundary, ''))}</p></div>`;
  }

  function renderParallelLanes(root, prism, state) {
    const body = root.querySelector('[data-view-body]');
    const props = prism.propositions.slice().sort((a,b) => Number(a.sort || 9999) - Number(b.sort || 9999));
    body.innerHTML = `
      <section class="pdim-prism-head"><div><p class="pdim-note">${esc(copy.lanesLead)}</p><p><strong>${esc(audienceQuestion(prism, state))}</strong></p></div>${audienceControl(prism, state)}</section>
      <div class="pdim-lane-timeline">${props.map((prop) => `<article class="pdim-lane-event"><div class="pdim-lane-time"><span>${esc(prop.period || '')}</span><strong>${esc(prop.id)}</strong></div><div class="pdim-lane-event-main"><h3>${esc(propTitle(prop))}</h3><p>${esc(propQuestion(prop))}</p><div class="pdim-lane-chips">${prism.lanes.map((lane) => { const cell = prop.cells && prop.cells[lane.id]; if (!cell) return ''; return `<button type="button" data-prism-status="${esc(cell.status)}" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><strong>${esc(laneLabel(lane))}</strong><span>${esc(statusLabel(prism, cell.status))}</span></button>`; }).join('')}</div></div></article>`).join('')}</div>
      <div class="pdim-prism-detail" data-prism-detail><p>${esc(localized(prism.boundary, ''))}</p></div>`;
  }

  function renderIsolation(root, prism, state) {
    const body = root.querySelector('[data-view-body]');
    if (!state.isolationLane || !prism.lanes.some((l) => l.id === state.isolationLane)) state.isolationLane = prism.lanes[0].id;
    const lane = prism.lanes.find((l) => l.id === state.isolationLane);
    const direct = [];
    const outside = [];
    prism.propositions.forEach((prop) => {
      const cell = prop.cells && prop.cells[lane.id];
      if (!cell) return;
      if (cell.status === 'DIRECT') direct.push({prop, cell});
      else if (['CONTEXT','OPEN','NOT_LOCATED'].includes(cell.status)) outside.push({prop, cell});
    });
    const item = ({prop, cell}) => `<li><button type="button" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><span class="pdim-prism-status" data-prism-status="${esc(cell.status)}">${esc(statusLabel(prism, cell.status))}</span><strong>${esc(propTitle(prop))}</strong></button><p>${esc(cellNote(cell))}</p></li>`;
    body.innerHTML = `
      <section class="pdim-isolation-head"><div><p class="pdim-note">${esc(copy.isolationLead)}</p><p class="pdim-warning">${esc(copy.formalBoundary)}</p></div><label>${copy.chooseLane}<select data-isolation-lane>${prism.lanes.map((l) => `<option value="${esc(l.id)}"${l.id === lane.id ? ' selected' : ''}>${esc(laneLabel(l))}</option>`).join('')}</select></label></section>
      <div class="pdim-isolation-grid"><section><h2>${copy.visibleAlone}</h2><ul>${direct.length ? direct.map(item).join('') : `<li class="pdim-none">${copy.noVisible}</li>`}</ul></section><section><h2>${copy.disappears}</h2><ul>${outside.length ? outside.map(item).join('') : `<li class="pdim-none">${copy.noOutside}</li>`}</ul></section></div>
      <div class="pdim-prism-detail" data-prism-detail><p>${esc(localized(prism.boundary, ''))}</p></div>`;
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
      let prism = null;
      if (prismRes && prismRes.ok) prism = await prismRes.json();
      const state = { audience: 'all', isolationLane: prism && prism.lanes.length ? prism.lanes[0].id : '' };

      root.innerHTML = `
        <div class="pdim-stats"><div><strong>${rows.length}</strong><span>${copy.records}</span></div><div><strong>${tracks.length}</strong><span>${copy.tracks}</span></div><div><strong>${edges.length}</strong><span>${copy.direct}</span></div><div><strong>${gaps}</strong><span>${copy.gaps}</span></div></div>
        <div class="pdim-controls"><label>${lang==='es'?'Buscar':'Search'}<input type="search" data-map-search placeholder="${esc(copy.search)}"></label><label>${lang==='es'?'Vía':'Track'}<select data-map-track><option value="">${copy.allTracks}</option>${tracks.map((t)=>`<option>${esc(t)}</option>`).join('')}</select></label></div>
        <div class="pdim-tabs" role="tablist"><button type="button" data-view="map" aria-selected="true">${copy.map}</button><button type="button" data-view="chronology" aria-selected="false">${copy.chronology}</button><button type="button" data-view="trace" aria-selected="false">${copy.trace}</button>${prism ? `<button type="button" data-view="prism" aria-selected="false">${copy.prism}</button><button type="button" data-view="lanes" aria-selected="false">${copy.lanes}</button><button type="button" data-view="isolation" aria-selected="false">${copy.isolation}</button>` : ''}</div>
        <div data-view-body></div>
        <section class="pdim-trace-panel" data-trace-panel aria-live="polite"></section>
        <footer class="pdim-footer"><p>${copy.publicBoundary}</p><a href="${esc(registerRoute)}">${copy.openRegister} →</a></footer>`;

      const filters = { search: root.querySelector('[data-map-search]'), track: root.querySelector('[data-map-track]') };
      let view = 'map';
      const draw = () => {
        const tracePanel = root.querySelector('[data-trace-panel]');
        if (view !== 'trace' && tracePanel) tracePanel.innerHTML = '';
        if (view === 'chronology') renderChronology(root, rows, filters);
        else if (view === 'trace') {
          const body = root.querySelector('[data-view-body]');
          body.innerHTML = `<div class="pdim-picker"><label>${copy.trace}<select data-trace-select><option value="">—</option>${rows.slice().sort((a,b)=>labelFor(a).localeCompare(labelFor(b))).map((r)=>`<option value="${esc(r.Master_ID)}">${esc(r.Master_ID)} · ${esc(labelFor(r))}</option>`).join('')}</select></label></div>`;
        } else if (view === 'prism' && prism) renderPrism(root, prism, state);
        else if (view === 'lanes' && prism) renderParallelLanes(root, prism, state);
        else if (view === 'isolation' && prism) renderIsolation(root, prism, state);
        else renderMap(root, rows, filters);
      };
      filters.search.addEventListener('input', draw); filters.track.addEventListener('input', draw);
      root.querySelectorAll('[data-view]').forEach((b) => b.addEventListener('click', () => { view = b.dataset.view; root.querySelectorAll('[data-view]').forEach((x)=>x.setAttribute('aria-selected', x===b?'true':'false')); draw(); }));
      root.addEventListener('click', (ev) => {
        const traceButton = ev.target.closest('[data-trace-id]');
        if (traceButton) { renderTrace(root, traceButton.dataset.traceId, rows, byId, edges); return; }
        const prismButton = ev.target.closest('[data-prism-prop][data-prism-lane]');
        if (prismButton && prism) renderPrismDetail(root, prism, prismButton.dataset.prismProp, prismButton.dataset.prismLane);
      });
      root.addEventListener('change', (ev) => {
        if (ev.target.matches('[data-trace-select]') && ev.target.value) renderTrace(root, ev.target.value, rows, byId, edges);
        if (ev.target.matches('[data-prism-audience]')) { state.audience = ev.target.value || 'all'; draw(); }
        if (ev.target.matches('[data-isolation-lane]')) { state.isolationLane = ev.target.value; draw(); }
      });
      draw();
    } catch (err) {
      root.innerHTML = `<div class="pdim-error"><strong>${copy.error}</strong><p>${esc(err.message || err)}</p></div>`;
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once:true}); else init();
})();

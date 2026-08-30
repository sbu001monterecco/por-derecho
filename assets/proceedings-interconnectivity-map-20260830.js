(() => {
  'use strict';

  const script = document.currentScript;
  if (!script) return;
  const assetBase = new URL('.', script.src);
  const repoBase = new URL('../', assetBase);
  const csvUrl = new URL('archive/PROCEEDINGS_MASTER_REGISTER.csv', repoBase).href;
  const lang = (document.documentElement.lang || 'en').toLowerCase().startsWith('es') ? 'es' : 'en';
  const registerRoute = new URL(lang === 'es' ? 'es/registro-maestro-procedimientos/' : 'en/master-proceedings-register/', repoBase).href;

  const copy = lang === 'es' ? {
    loading: 'Construyendo el mapa desde el registro canónico…',
    error: 'No se pudo construir el mapa de procedimientos.',
    allTracks: 'Todas las vías', search: 'Buscar ID, referencia, órgano, objeto o estado…',
    map: 'Mapa por vías', chronology: 'Cronología', trace: 'Trazar un procedimiento',
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
    publicBoundary: 'Esta visualización es una proyección pública del mismo CSV canónico. No convierte referencias en procedimientos ni conexiones contextuales en hechos jurídicos.'
  } : {
    loading: 'Building the map from the canonical register…',
    error: 'The proceedings map could not be built.',
    allTracks: 'All tracks', search: 'Search ID, reference, organ, object or status…',
    map: 'Track map', chronology: 'Chronology', trace: 'Trace one proceeding',
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
    publicBoundary: 'This visualisation is a public projection of the same canonical CSV. It does not turn references into proceedings or contextual connections into legal facts.'
  };

  const esc = (v) => String(v || '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const norm = (v) => String(v || '').trim();
  const key = (v) => norm(v).toLowerCase();

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

  function renderMap(root, rows, byId, edges, filters) {
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

  async function init() {
    const root = document.querySelector('[data-proceedings-map]'); if (!root) return;
    try {
      const res = await fetch(csvUrl, {cache:'no-store'}); if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const all = parseCsv(await res.text()); const rows = all.filter(isPublic);
      const byId = new Map(rows.map((r) => [norm(r.Master_ID), r]));
      const edges = buildEdges(rows, byId);
      const tracks = Array.from(new Set(rows.map((r) => norm(r.Stream)).filter(Boolean))).sort((a,b)=>a.localeCompare(b));
      const gaps = rows.filter((r) => norm(r.Open_Reference_Gap)).length;

      root.innerHTML = `
        <div class="pdim-stats"><div><strong>${rows.length}</strong><span>${copy.records}</span></div><div><strong>${tracks.length}</strong><span>${copy.tracks}</span></div><div><strong>${edges.length}</strong><span>${copy.direct}</span></div><div><strong>${gaps}</strong><span>${copy.gaps}</span></div></div>
        <div class="pdim-controls"><label>${lang==='es'?'Buscar':'Search'}<input type="search" data-map-search placeholder="${esc(copy.search)}"></label><label>${lang==='es'?'Vía':'Track'}<select data-map-track><option value="">${copy.allTracks}</option>${tracks.map((t)=>`<option>${esc(t)}</option>`).join('')}</select></label></div>
        <div class="pdim-tabs" role="tablist"><button type="button" data-view="map" aria-selected="true">${copy.map}</button><button type="button" data-view="chronology" aria-selected="false">${copy.chronology}</button><button type="button" data-view="trace" aria-selected="false">${copy.trace}</button></div>
        <div data-view-body></div>
        <section class="pdim-trace-panel" data-trace-panel aria-live="polite"></section>
        <footer class="pdim-footer"><p>${copy.publicBoundary}</p><a href="${esc(registerRoute)}">${copy.openRegister} →</a></footer>`;

      const filters = { search: root.querySelector('[data-map-search]'), track: root.querySelector('[data-map-track]') };
      let view = 'map';
      const draw = () => {
        if (view === 'chronology') renderChronology(root, rows, filters);
        else if (view === 'trace') {
          const body = root.querySelector('[data-view-body]');
          body.innerHTML = `<div class="pdim-picker"><label>${copy.trace}<select data-trace-select><option value="">—</option>${rows.slice().sort((a,b)=>labelFor(a).localeCompare(labelFor(b))).map((r)=>`<option value="${esc(r.Master_ID)}">${esc(r.Master_ID)} · ${esc(labelFor(r))}</option>`).join('')}</select></label></div>`;
        } else renderMap(root, rows, byId, edges, filters);
      };
      filters.search.addEventListener('input', draw); filters.track.addEventListener('input', draw);
      root.querySelectorAll('[data-view]').forEach((b) => b.addEventListener('click', () => { view = b.dataset.view; root.querySelectorAll('[data-view]').forEach((x)=>x.setAttribute('aria-selected', x===b?'true':'false')); draw(); }));
      root.addEventListener('click', (ev) => { const b = ev.target.closest('[data-trace-id]'); if (b) renderTrace(root, b.dataset.traceId, rows, byId, edges); });
      root.addEventListener('change', (ev) => { if (ev.target.matches('[data-trace-select]') && ev.target.value) renderTrace(root, ev.target.value, rows, byId, edges); });
      draw();
    } catch (err) {
      root.innerHTML = `<div class="pdim-error"><strong>${copy.error}</strong><p>${esc(err.message || err)}</p></div>`;
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once:true}); else init();
})();

(() => {
  'use strict';
  const root = document.querySelector('[data-mf-hub]');
  if (!root) return;

  const isEn = document.documentElement.lang === 'en';
  const base = location.pathname.includes('/por-derecho/') ? '/por-derecho' : '';
  const A = value => Array.isArray(value) ? value : value ? [value] : [];
  const E = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const N = value => String(value ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toUpperCase().replace(/[^A-Z0-9]+/g, ' ').trim();
  const dataUrl = path => `${base}/${path}`;
  const loadJSON = async path => {
    const response = await fetch(dataUrl(path), {cache: 'no-store'});
    if (!response.ok) throw new Error(`${path}: ${response.status}`);
    return response.json();
  };

  const T = isEn ? {
    load: 'Loading canonical Public Prosecution register…',
    error: 'The canonical register could not be loaded.',
    files: 'Prosecution files', events: 'Canonical events', offices: 'Caret offices',
    filings: 'filings', responses: 'responses / inbound acts', exact: 'exact files', pendingRefs: 'pending references',
    office: 'Office', state: 'Status', external: 'External reference', master: 'Master ID', date: 'Date', direction: 'Direction', type: 'Type', linked: 'Linked file',
    all: 'All offices', search: 'Search PD-SP-R, PD-SP-EVT, REGAGE, DI, DIP, EG, NIG, office…', more: 'Show all', less: 'Show less',
    graph: 'Open communications ↔ proceedings graph', boundary: 'Evidence boundary',
    eu: 'Separate supranational branch, outside the Spanish Ministerio Fiscal hierarchy.',
    source: 'No synthetic events are created for unlocated documents. Every located filing, response or act retains its own immutable PD-SP-EVT; every prosecution file retains a PD-SP-R separate from REGAGE/RedSARA.'
  } : {
    load: 'Cargando registro canónico del Ministerio Fiscal…',
    error: 'No se pudo cargar el registro canónico.',
    files: 'Expedientes Fiscalía', events: 'Eventos canónicos', offices: 'Oficinas ^',
    filings: 'presentaciones', responses: 'respuestas / actos de entrada', exact: 'expedientes exactos', pendingRefs: 'referencias pendientes',
    office: 'Oficina', state: 'Estado', external: 'Referencia externa', master: 'ID maestro', date: 'Fecha', direction: 'Dirección', type: 'Tipo', linked: 'Expediente',
    all: 'Todas las oficinas', search: 'Buscar PD-SP-R, PD-SP-EVT, REGAGE, DI, DIP, EG, NIG, oficina…', more: 'Mostrar todos', less: 'Mostrar menos',
    graph: 'Abrir grafo comunicaciones ↔ procedimientos', boundary: 'Límite probatorio',
    eu: 'Rama supranacional separada del Ministerio Fiscal español.',
    source: 'No se crean eventos sintéticos para documentos no localizados. Cada presentación, respuesta o acto localizado conserva su PD-SP-EVT inmutable; cada expediente conserva un PD-SP-R separado del REGAGE/RedSARA.'
  };

  const masterIds = record => [...A(record.master_register_ids), ...A(record.master_register_id)].filter(Boolean);
  const isInbound = event => N(event.direction).includes('INBOUND') || N(event.direction).includes('FROM INSTITUTION') || /ACKNOWLEDGEMENT|OFFICIAL ACT|DECISION|NOTICE/.test(N(event.record_type));
  const isOutbound = event => N(event.direction).includes('OUTBOUND') || ['REGISTRATION_RECEIPT', 'OUTBOUND_COMMUNICATION'].includes(event.record_type);
  const identityLink = id => `${base}/${isEn ? 'en/matter-identity-registry/' : 'es/registro-identidad-materia/'}#${encodeURIComponent(id)}`;
  const graphLink = () => `${base}/${isEn ? 'en/public-prosecution-communications-proceedings/' : 'es/fiscalia-comunicaciones-procedimientos/'}`;

  function badge(record) {
    const state = record?.identity_resolution || '';
    if (state === 'CARET_CONFIRMED') return ['ok', isEn ? '^ confirmed' : '^ confirmado'];
    if (state.includes('PENDING')) return ['pending', isEn ? 'caret pending' : '^ pendiente'];
    return ['neutral', isEn ? 'canonical' : 'canónico'];
  }

  function officeMatcher(institutions) {
    const labels = [];
    for (const institution of institutions) {
      for (const label of [institution.name, ...A(institution.aliases)].filter(Boolean)) labels.push([N(label), institution.id]);
    }
    labels.sort((a, b) => b[0].length - a[0].length);
    return value => {
      const key = N(value);
      if (!key) return '';
      const exact = labels.find(item => item[0] === key);
      if (exact) return exact[1];
      const partial = labels.find(item => item[0].length >= 12 && (key.includes(item[0]) || item[0].includes(key)));
      return partial ? partial[1] : '';
    };
  }

  function officeCard(id, context) {
    const {institutionById, files, events} = context;
    const institution = institutionById.get(id);
    if (!institution) return `<article class="mf-office"><strong>${E(id)}</strong><p>Identity source missing.</p></article>`;
    const officeFiles = files.filter(file => file.office_id === id);
    const officeEvents = events.filter(event => event.office_id === id || event.linked_files.some(file => file.office_id === id));
    const [cls, label] = badge(institution);
    return `<article class="mf-office" id="office-${E(id)}">
      <div class="mf-office-top"><div><span class="mf-kicker">${E(id)}</span><h3>${E(institution.name)}</h3></div><span class="mf-chip ${cls}">${E(label)}</span></div>
      <div class="mf-office-metrics"><span><b>${officeFiles.length}</b> ${E(T.files)}</span><span><b>${officeEvents.filter(isOutbound).length}</b> ${E(T.filings)}</span><span><b>${officeEvents.filter(isInbound).length}</b> ${E(T.responses)}</span></div>
      <p>${E(institution.identity_boundary || '')}</p>
      <div class="mf-links"><a href="?office=${encodeURIComponent(id)}#records">${E(T.office)}</a><a href="${E(identityLink(id))}">${E(id)} ^</a></div>
    </article>`;
  }

  function groupSection(group, context) {
    const title = group[isEn ? 'title_en' : 'title_es'] || group.title_es;
    const note = group.separate_from_ministerio_fiscal ? `<p>${E(T.eu)}</p>` : '';
    const cards = group.institution_ids.map(id => officeCard(id, context)).join('');
    return `<section class="mf-office-group"><div class="mf-group-heading"><h2>${E(title)}</h2>${note}</div><div class="mf-office-grid">${cards}</div></section>`;
  }

  function fileSearch(file) {
    return N([file.master_id, file.reference, file.secondary_reference, file.office, file.status, file.caepr?.id, file.caepr?.name, ...A(file.caepr?.aliases)].join(' '));
  }

  function eventSearch(event) {
    return N([event.event_id, event.event_date, event.direction, event.record_type, event.office, event.official_reference, ...A(event.matter_references), ...A(event.master_ids), event.office_id].join(' '));
  }

  function render(context) {
    const {config, graph, communications, institutionById, files, events, selectedOffice, duplicateCount, missingCaepr} = context;
    const denominator = communications.denominator_control || {};
    const exact = graph.coverage?.fiscalia_exact_files ?? 0;
    const unresolved = graph.coverage?.fiscalia_unresolved_references ?? 0;
    const aggregateGap = denominator.metadata_only_records_reported ?? 0;
    const fiscalEventCount = graph.coverage?.communication_events ?? events.length;
    const authorityRows = denominator.event_rows_total ?? fiscalEventCount;
    const receipts = denominator.detailed_baseline_receipt_rows_registered ?? 0;
    const officeCount = config.groups.reduce((count, group) => count + group.institution_ids.length, 0);
    const groups = config.groups.map(group => groupSection(group, context)).join('');

    root.innerHTML = `
      <section class="mf-summary">
        <div><span>${E(T.offices)}</span><strong>${officeCount}</strong></div>
        <div><span>${E(T.files)}</span><strong>${exact} + ${unresolved}</strong><small>${E(T.exact)} + ${E(T.pendingRefs)}</small></div>
        <div><span>${E(T.events)}</span><strong>${fiscalEventCount}</strong><small>${receipts} detailed REGAGE · ${authorityRows} authority-register rows</small></div>
        <div><span>Mailbox</span><strong>${denominator.mailbox_inbound_email_rows ?? 0} ↙ / ${denominator.mailbox_outbound_email_rows ?? 0} ↗</strong><small>inbound / outbound</small></div>
      </section>
      <section class="mf-integrity">
        <div><span class="mf-kicker">Integrity</span><h2>Canonical ID ↔ external reference</h2><p>${E(T.source)}</p></div>
        <div class="mf-integrity-grid">
          <div class="mf-integrity-item ${duplicateCount ? 'pending' : 'ok'}"><b>${duplicateCount ? 'OPEN' : 'PASS'}</b><span>PD-SP-EVT unique</span><code>${duplicateCount ? duplicateCount : `${events.length}/${events.length}`}</code></div>
          <div class="mf-integrity-item ${missingCaepr.length ? 'pending' : 'ok'}"><b>${missingCaepr.length ? 'OPEN' : 'PASS'}</b><span>24 Fiscalía rows → PD-SP-R</span><code>${missingCaepr.length ? E(missingCaepr.map(file => file.master_id).join(', ')) : `${files.length}/${files.length}`}</code></div>
          <div class="mf-integrity-item ${aggregateGap ? 'pending' : 'ok'}"><b>${aggregateGap ? 'OPEN' : 'PASS'}</b><span>aggregate-only RedSARA gap</span><code>${aggregateGap}</code></div>
        </div>
      </section>
      <section class="mf-numbering">
        <div><code>PD-SP-I-####</code><span>office / institution ^</span></div>
        <div><code>PD-SP-R-####</code><span>Fiscalía expediente ^</span></div>
        <div><code>PD-SP-EVT-####</code><span>filing / response / act</span></div>
        <div><code>REGAGE… / DI / DIP / EG / NIG</code><span>external official identifiers</span></div>
      </section>
      ${groups}
      <section class="mf-records" id="records">
        <div class="mf-records-head"><div><span class="mf-kicker">Cross-register view</span><h2>${E(T.files)} ↔ ${E(T.events)}</h2></div><div class="mf-controls"><a class="mf-reset" href="./#records">${E(T.all)}</a><input id="mf-search" type="search" autocomplete="off" placeholder="${E(T.search)}"></div></div>
        <div class="mf-filter-banner" id="mf-filter-banner" hidden></div>
        <div class="mf-table-wrap"><table class="mf-table" id="mf-files"><thead><tr><th>^ / CAEPR</th><th>${E(T.master)}</th><th>${E(T.external)}</th><th>${E(T.office)}</th><th>${E(T.state)}</th><th>${E(T.events)}</th></tr></thead><tbody></tbody></table></div>
        <div class="mf-events-head"><h3>${E(T.events)}</h3><button type="button" id="mf-toggle-events">${E(T.more)}</button></div>
        <div class="mf-table-wrap"><table class="mf-table" id="mf-events"><thead><tr><th>PD-SP-EVT</th><th>${E(T.date)}</th><th>${E(T.direction)}</th><th>${E(T.type)}</th><th>${E(T.office)}</th><th>${E(T.external)}</th><th>${E(T.linked)}</th></tr></thead><tbody></tbody></table></div>
        <p class="mf-no-results" id="mf-none" hidden>No matching rows.</p>
      </section>
      <section class="mf-boundary"><strong>${E(T.boundary)}.</strong> ${E(config.proof_boundaries?.[isEn ? 'en' : 'es'] || '')} <a href="${E(graphLink())}">${E(T.graph)}</a>.</section>`;
    wireTables(context);
  }

  function wireTables(context) {
    const {institutionById, files, events, selectedOffice} = context;
    const search = document.querySelector('#mf-search');
    const fileBody = document.querySelector('#mf-files tbody');
    const eventBody = document.querySelector('#mf-events tbody');
    const toggle = document.querySelector('#mf-toggle-events');
    const noResults = document.querySelector('#mf-none');
    const banner = document.querySelector('#mf-filter-banner');
    let showAll = false;

    function draw() {
      const query = N(search.value);
      if (selectedOffice) {
        const institution = institutionById.get(selectedOffice);
        banner.hidden = false;
        banner.innerHTML = institution ? `<strong>${E(selectedOffice)} ^</strong> ${E(institution.name)}` : `<strong>${E(selectedOffice)}</strong>`;
      }

      const visibleFiles = files.filter(file => (!selectedOffice || file.office_id === selectedOffice) && (!query || fileSearch(file).includes(query)));
      fileBody.innerHTML = visibleFiles.map(file => {
        const proceeding = file.caepr;
        const [cls, label] = badge(proceeding || {});
        const id = proceeding?.id || 'CAEPR GAP';
        return `<tr id="file-${E(proceeding?.id || file.master_id)}">
          <td><a href="${proceeding ? E(identityLink(proceeding.id)) : '#'}"><code>${E(id)}</code></a><br><span class="mf-chip ${cls}">${E(label)}</span></td>
          <td><code>${E(file.master_id)}</code></td>
          <td><strong>${E(file.reference || '')}</strong>${file.secondary_reference ? `<br><small>${E(file.secondary_reference)}</small>` : ''}</td>
          <td>${E(institutionById.get(file.office_id)?.name || file.office || '')}${file.office_id ? `<br><code>${E(file.office_id)}</code>` : ''}</td>
          <td><small>${E(file.identity_state || '')}</small><br>${E(file.status || '')}</td>
          <td>${E(file.counts?.events ?? file.linked_event_ids?.length ?? 0)}</td>
        </tr>`;
      }).join('');

      let visibleEvents = events.filter(event => {
        const officeMatch = !selectedOffice || event.office_id === selectedOffice || event.linked_files.some(file => file.office_id === selectedOffice);
        return officeMatch && (!query || eventSearch(event).includes(query));
      });
      visibleEvents.sort((a, b) => String(b.event_date || '').localeCompare(String(a.event_date || '')) || String(b.event_id).localeCompare(String(a.event_id)));
      const rows = (showAll || query) ? visibleEvents : visibleEvents.slice(0, 80);
      eventBody.innerHTML = rows.map(event => {
        const linked = event.linked_files.length ? event.linked_files.map(file => `<a href="#file-${E(file.caepr?.id || file.master_id)}"><code>${E(file.caepr?.id || file.master_id)}</code></a>`).join('<br>') : '—';
        return `<tr id="event-${E(event.event_id)}"><td><a href="#event-${E(event.event_id)}"><code>${E(event.event_id)}</code></a></td><td>${E(event.event_date || '')}</td><td>${E(event.direction || '')}</td><td>${E(event.record_type || '')}</td><td>${E(institutionById.get(event.office_id)?.name || event.office || '')}${event.office_id ? `<br><code>${E(event.office_id)}</code>` : ''}</td><td>${event.official_reference ? `<code>${E(event.official_reference)}</code>` : '—'}</td><td>${linked}</td></tr>`;
      }).join('');
      noResults.hidden = Boolean(visibleFiles.length || rows.length);
      toggle.hidden = visibleEvents.length <= 80 || Boolean(query);
      toggle.textContent = showAll ? T.less : `${T.more} (${visibleEvents.length})`;
    }

    search.addEventListener('input', draw);
    toggle.addEventListener('click', () => { showAll = !showAll; draw(); });
    draw();
  }

  async function init() {
    root.innerHTML = `<p class="mf-loading">${E(T.load)}</p>`;
    try {
      const [config, index, graph, communications] = await Promise.all([
        loadJSON('assets/data/ministerio-fiscal-hub-config-v1.json'),
        loadJSON('assets/data/matter-identity-registry-v1.json'),
        loadJSON('assets/data/fiscalia-proceedings-interconnectivity-v1.json'),
        loadJSON('assets/data/institutional-communications-register-v1.json')
      ]);
      const parts = index.parts.filter(part => ['INSTITUTION', 'PROCEEDING'].includes(part.type));
      const shards = await Promise.all(parts.map(part => loadJSON(`assets/data/${part.path}`)));
      const identities = shards.flatMap(shard => shard.records || []);
      const institutions = identities.filter(record => record.type === 'INSTITUTION');
      const proceedings = identities.filter(record => record.type === 'PROCEEDING');
      const institutionById = new Map(institutions.map(record => [record.id, record]));
      const proceedingByMaster = new Map();
      for (const proceeding of proceedings) for (const masterId of masterIds(proceeding)) proceedingByMaster.set(masterId, proceeding);
      const matchOffice = officeMatcher(institutions);
      const files = (graph.fiscal_files || []).map(file => {
        const caepr = proceedingByMaster.get(file.master_id) || null;
        return {...file, caepr, office_id: caepr?.competent_organ || matchOffice(file.office)};
      });
      const fileByMaster = new Map(files.map(file => [file.master_id, file]));
      const events = (graph.events || []).map(event => ({
        ...event,
        office_id: matchOffice(event.office) || (institutionById.has(event.institution_id) ? event.institution_id : ''),
        linked_files: A(event.master_ids).map(masterId => fileByMaster.get(masterId)).filter(Boolean)
      }));
      const duplicateCount = events.length - new Set(events.map(event => event.event_id)).size;
      const missingCaepr = files.filter(file => !file.caepr);
      const selectedOffice = new URLSearchParams(location.search).get('office') || '';
      render({config, index, graph, communications, institutionById, files, events, selectedOffice, duplicateCount, missingCaepr});
    } catch (error) {
      console.error(error);
      root.innerHTML = `<div class="mf-error"><strong>${E(T.error)}</strong><br><code>${E(error.message)}</code></div>`;
    }
  }

  init();
})();

(() => {
  'use strict';
  const script = document.currentScript;
  const root = document.querySelector('[data-ca-interconnectivity]');
  if (!script || !root) return;
  const repo = new URL('../', new URL('.', script.src));
  const lang = document.documentElement.lang.toLowerCase().startsWith('es') ? 'es' : 'en';
  const dataUrl = new URL('assets/data/community-acta-authority-interconnectivity-v1.json', repo);
  const masterRoute = new URL(lang === 'es' ? 'es/registro-maestro-procedimientos/' : 'en/master-proceedings-register/', repo);
  const mapRoute = new URL(lang === 'es' ? 'es/mapa-procedimientos/' : 'en/proceedings-map/', repo);
  const adjudicationRoute = new URL(lang === 'es' ? 'es/adjudicacion-2022-reconstruccion-documental/' : 'en/2022-adjudication-documentary-reconstruction/', repo);
  const t = lang === 'es' ? {
    metrics:['Paquetes ACTA/fuente','Expedientes de autoridad','Grupos institucionales','Ejes probatorios','Hitos comunitarios','Hitos de adjudicación/escritura'],
    parallel:'Vías paralelas de 2022', community:'Junta / ACTA comunitaria', adjudication:'Adjudicación / escritura',
    allegation:'Alegación atribuida — no es una conclusión', axes:'Siete ejes que no deben fusionarse',
    supported:'Lo que consta', notEstablished:'No acreditado', next:'Fuente siguiente', contrary:'Explicación contraria más fuerte',
    actas:'Registro público completo de ACTAs/minutas', authorities:'Expedientes de autoridades públicas',
    searchActa:'Buscar ACTA, fecha u órgano', searchAuthority:'Buscar ID, referencia, órgano u objeto', group:'Grupo', all:'Todos',
    source:'Fuente', status:'Estado', gap:'Brecha abierta', propositions:'Proposiciones del Prisma', axesLinked:'Ejes aplicables',
    master:'Abrir fila maestra', trace:'Abrir trazabilidad', openActa:'Abrir sala documental', noMatch:'No hay resultados.',
    temporal:'17 días entre el ACTA y la escritura 457', loading:'Cargando la proyección controlada…', error:'No se pudo cargar la interconexión.',
    boundary:'Límite', files:'expedientes', verified:'fuente primaria verificada', procedural:'procedimental verificado', open:'abierto o fuente pendiente', adjudicationPage:'Abrir reconstrucción de adjudicación'
  } : {
    metrics:['ACTA/source packages','Authority files','Institutional groups','Evidence axes','Community milestones','Adjudication/deed milestones'],
    parallel:'The 2022 parallel tracks', community:'Community meeting / ACTA', adjudication:'Adjudication / deed',
    allegation:'Attributed allegation — not a finding', axes:'Seven axes that must not be collapsed',
    supported:'What is supported', notEstablished:'Not established', next:'Next source', contrary:'Strongest contrary explanation',
    actas:'Complete public ACTA/minutes register', authorities:'Public-authority files',
    searchActa:'Search ACTA, date or body', searchAuthority:'Search ID, reference, organ or object', group:'Group', all:'All',
    source:'Source', status:'Status', gap:'Open gap', propositions:'Case Prism propositions', axesLinked:'Applicable axes',
    master:'Open master row', trace:'Open trace', openActa:'Open document room', noMatch:'No results match.',
    temporal:'17 days between the ACTA and deed 457', loading:'Loading the controlled projection…', error:'The interconnectivity projection could not be loaded.',
    boundary:'Boundary', files:'files', verified:'verified primary source', procedural:'verified procedural', open:'open or primary pending', adjudicationPage:'Open adjudication reconstruction'
  };
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const loc = (obj, stem) => obj && (obj[`${stem}_${lang}`] || obj[`${stem}_en`] || obj[`${stem}_es`] || '');
  const metric = (value, label) => `<div class="pd-ca-metric"><strong>${esc(value)}</strong><span>${esc(label)}</span></div>`;
  const internalRoute = (path) => new URL(path, repo).href;
  let data;

  function milestone(item) {
    return `<article class="pd-ca-milestone" id="${esc(item.id)}" data-ca-milestone="${esc(item.id)}"><header><time>${esc(item.date)}</time><code>${esc(item.id)}</code></header><h3>${esc(loc(item,'kind'))}</h3><p>${esc(loc(item,'safe'))}</p><details><summary>${esc(t.notEstablished)}</summary><p>${esc(loc(item,'not_established'))}</p><small>${esc(item.source_anchor)}</small></details></article>`;
  }

  function axisCard(axis) {
    return `<article class="pd-ca-axis" id="axis-${esc(axis.id)}" data-ca-axis="${esc(axis.id)}"><header><code>${esc(axis.id)}</code><span>${esc(axis.state)}</span></header><h3>${esc(loc(axis,'label'))}</h3><dl><div><dt>${esc(t.supported)}</dt><dd>${esc(loc(axis,'supported'))}</dd></div><div><dt>${esc(t.notEstablished)}</dt><dd>${esc(loc(axis,'not_established'))}</dd></div><div><dt>${esc(t.next)}</dt><dd>${esc(loc(axis,'next_source'))}</dd></div><div><dt>${esc(t.contrary)}</dt><dd>${esc(loc(axis,'contrary'))}</dd></div></dl></article>`;
  }

  function actaRows() {
    const q = root.querySelector('[data-ca-acta-search]').value.trim().toLowerCase();
    const rows = data.actas.filter((item) => !q || [item.id,item.date,item.title_en,item.title_es,item.body,item.meeting_type].join(' ').toLowerCase().includes(q));
    root.querySelector('[data-ca-actas]').innerHTML = rows.length ? rows.map((item) => `<article class="pd-ca-record" id="acta-${esc(item.id)}" data-ca-acta="${esc(item.id)}"><header><time>${esc(item.date)}</time><code>${esc(item.id)}</code></header><h3>${esc(loc(item,'title'))}</h3><p>${esc(item.body)} · ${esc(item.meeting_type)} · ${esc(item.source_pages)} pp.</p><p class="pd-ca-muted">${esc(loc(item,'limitations'))}</p><a href="${esc(internalRoute(item[`route_${lang}`]))}">${esc(t.openActa)} →</a></article>`).join('') : `<p class="pd-ca-empty">${esc(t.noMatch)}</p>`;
  }

  function authorityRows() {
    const q = root.querySelector('[data-ca-authority-search]').value.trim().toLowerCase();
    const group = root.querySelector('[data-ca-group]').value;
    const rows = data.authority_files.filter((file) => (!group || file.group_id === group) && (!q || [file.master_id,file.reference,file.organ,file.current_custodian,file.object,file.connection,file.stream].join(' ').toLowerCase().includes(q)));
    root.querySelector('[data-ca-authorities]').innerHTML = rows.length ? rows.map((file) => {
      const props = file.proposition_links.map((link) => `<span>${esc(link.proposition_id)} · ${esc(link.status)}</span>`).join('');
      return `<article class="pd-ca-authority" id="authority-${esc(file.master_id)}" data-ca-authority="${esc(file.master_id)}" data-ca-group-id="${esc(file.group_id)}"><header><code>${esc(file.master_id)}</code><span>${esc(file.source_status)}</span></header><h3>${esc(file.reference)} · ${esc(file.organ)}</h3><p>${esc(file.object || file.connection)}</p><div class="pd-ca-tags">${file.axis_ids.map((id) => `<a href="#axis=${encodeURIComponent(id)}">${esc(id)}</a>`).join('')}${props}</div><details><summary>${esc(t.boundary)}</summary><p>${esc(loc(file,'boundary'))}</p><p><strong>${esc(t.gap)}:</strong> ${esc(file.open_reference_gap || '—')}</p></details><p class="pd-ca-links"><a href="${esc(masterRoute.href)}#record-${encodeURIComponent(file.master_id)}">${esc(t.master)}</a><a href="${esc(mapRoute.href)}#trace-proceeding=${encodeURIComponent(file.master_id)}">${esc(t.trace)}</a></p></article>`;
    }).join('') : `<p class="pd-ca-empty">${esc(t.noMatch)}</p>`;
  }

  function applyHash() {
    const match = location.hash.match(/^#(authority|acta|axis)=([^&]+)/);
    if (!match) return;
    const id = decodeURIComponent(match[2]);
    if (match[1] === 'authority') {
      root.querySelector('[data-ca-authority-search]').value = id;
      root.querySelector('[data-ca-group]').value = '';
      authorityRows();
    } else if (match[1] === 'acta') {
      root.querySelector('[data-ca-acta-search]').value = id;
      actaRows();
    }
    const target = document.getElementById(`${match[1]}-${id}`);
    if (target) requestAnimationFrame(() => target.scrollIntoView({block:'center'}));
  }

  function render() {
    const c = data.coverage;
    root.innerHTML = `
      <section class="pd-ca-metrics">${metric(c.public_acta_packages,t.metrics[0])}${metric(c.public_authority_files,t.metrics[1])}${metric(c.authority_groups,t.metrics[2])}${metric(c.evidentiary_axes,t.metrics[3])}${metric(c.community_2022_milestones,t.metrics[4])}${metric(c.adjudication_and_deed_milestones,t.metrics[5])}</section>
      <section class="pd-ca-alert" data-ca-allegation><p class="eyebrow">${esc(t.allegation)}</p><p>${esc(loc(data.attributed_allegation,''))}</p><small><strong>${esc(data.attributed_allegation.status)}</strong> · ${esc(loc(data.attributed_allegation,'boundary'))}</small></section>
      <section class="pd-ca-panel" id="parallel-2022"><div class="pd-ca-section-head"><div><p class="eyebrow">2022 · ${esc(data.parallel_2022.relationship_type)}</p><h2>${esc(t.parallel)}</h2></div><strong>${esc(t.temporal)}</strong></div><p class="pd-ca-boundary">${esc(loc(data.parallel_2022,'boundary'))}</p><div class="pd-ca-parallel"><section data-ca-track="community"><h3>${esc(t.community)}</h3>${data.parallel_2022.community_track.map(milestone).join('')}</section><section data-ca-track="adjudication"><h3>${esc(t.adjudication)}</h3>${data.parallel_2022.adjudication_track.map(milestone).join('')}<a class="pd-ca-button" href="${esc(adjudicationRoute.href)}">${esc(t.adjudicationPage)} →</a></section></div></section>
      <section class="pd-ca-panel" id="evidence-axes"><div class="pd-ca-section-head"><div><p class="eyebrow">01–07</p><h2>${esc(t.axes)}</h2></div></div><div class="pd-ca-axis-grid">${data.evidentiary_axes.map(axisCard).join('')}</div></section>
      <section class="pd-ca-panel" id="actas"><div class="pd-ca-section-head"><div><p class="eyebrow">${esc(c.public_acta_packages)} / ${esc(c.public_acta_packages)}</p><h2>${esc(t.actas)}</h2></div><label>${esc(t.searchActa)}<input type="search" data-ca-acta-search></label></div><div class="pd-ca-record-grid" data-ca-actas></div></section>
      <section class="pd-ca-panel" id="authority-files"><div class="pd-ca-section-head"><div><p class="eyebrow">${esc(c.verified_primary_authority_files)} ${esc(t.verified)} · ${esc(c.verified_procedural_authority_files)} ${esc(t.procedural)} · ${esc(c.open_or_primary_pending_authority_files)} ${esc(t.open)}</p><h2>${esc(t.authorities)}</h2></div><div class="pd-ca-controls"><label>${esc(t.searchAuthority)}<input type="search" data-ca-authority-search></label><label>${esc(t.group)}<select data-ca-group><option value="">${esc(t.all)}</option>${data.authority_groups.map((group) => `<option value="${esc(group.id)}">${esc(loc(group,'label'))} · ${esc(group.record_count)} ${esc(t.files)}</option>`).join('')}</select></label></div></div><div class="pd-ca-authority-grid" data-ca-authorities></div></section>
      <section class="pd-ca-panel pd-ca-final-boundary"><h2>${esc(t.boundary)}</h2><p>${esc(loc(data,'global_boundary'))}</p></section>`;
    root.querySelector('[data-ca-acta-search]').addEventListener('input', actaRows);
    root.querySelector('[data-ca-authority-search]').addEventListener('input', authorityRows);
    root.querySelector('[data-ca-group]').addEventListener('change', authorityRows);
    actaRows(); authorityRows(); applyHash();
    addEventListener('hashchange', applyHash);
  }

  fetch(dataUrl, {cache:'no-store'}).then((response) => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }).then((payload) => { data = payload; render(); }).catch((error) => {
    root.innerHTML = `<p class="pd-ca-error">${esc(t.error)} ${esc(error.message)}</p>`;
  });
})();

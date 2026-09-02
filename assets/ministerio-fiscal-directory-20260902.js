(() => {
  const body = document.body;
  if (!body.classList.contains('pd-mfdir')) return;
  const lang = document.documentElement.lang === 'en' ? 'en' : 'es';
  const directoryUrl = body.dataset.mfDirectory;
  const communicationsUrl = body.dataset.mfCommunications;
  const view = body.dataset.mfView || 'hub';
  const target = document.querySelector('[data-mf-directory-root]');
  const esc = (s = '') => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const norm = (s = '') => String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const t = (obj, key) => obj[`${key}_${lang}`] || obj[`${key}_es`] || obj[key] || '';
  const statusClass = s => /PENDING|OPEN|UNRESOLVED|SOURCE_REQUIRED|AGGREGATE/.test(String(s)) ? 'pending' : 'verified';
  const eventStats = events => {
    const ids = new Set(events.map(e => e.event_id).filter(Boolean));
    const baseline = events.filter(e => e.cohort === 'BASELINE_REDSARA_ANEXO4_75' && e.record_type === 'REGISTRATION_RECEIPT');
    const inbound = events.filter(e => e.direction === 'INBOUND_FROM_INSTITUTION');
    const outbound = events.filter(e => e.direction === 'OUTBOUND_TO_INSTITUTION');
    return {rows: events.length, ids: ids.size, baseline: baseline.length, inbound: inbound.length, outbound: outbound.length};
  };
  const officeTerms = {
    'PD-MF-OFF-0013':['unidad de apoyo a la fiscalia europea'],
    'PD-MF-OFF-0012':['fiscalia europea'],
    'PD-MF-OFF-0002':['inspeccion fiscal'],
    'PD-MF-OFF-0003':['secretaria tecnica'],
    'PD-MF-OFF-0004':['delitos contra la administracion publica'],
    'PD-MF-OFF-0005':['fiscalia especial contra la corrupcion','anticorrupcion'],
    'PD-MF-OFF-0006':['fiscalia de la audiencia nacional','audiencia nacional'],
    'PD-MF-OFF-0007':['fiscalia de la sala de lo penal del tribunal supremo','sala de lo penal del tribunal supremo'],
    'PD-MF-OFF-0008':['fiscalia de la comunidad autonoma de canarias','fiscalia superior de canarias'],
    'PD-MF-OFF-0009':['fiscalia provincial de las palmas'],
    'PD-MF-OFF-0010':['fiscalia provincial de santa cruz de tenerife','fiscalia provincial de tenerife'],
    'PD-MF-OFF-0011':['fiscalia de area de arrecife','arrecife de lanzarote-puerto del rosario','arrecife de lanzarote–puerto del rosario'],
    'PD-MF-OFF-0014':['fiscalia provincial de valencia'],
    'PD-MF-OFF-0001':['fiscalia general del estado']
  };
  const eventOfficeId = event => {
    const office = norm(event.office || '');
    if (!office) return null;
    return Object.keys(officeTerms).find(id => officeTerms[id].some(term => office.includes(norm(term)))) || null;
  };
  const renderKpis = (d, stats) => `<div class="mf-kpis">
    <div class="mf-kpi"><strong>${stats.ids}</strong><span>${lang==='es'?'IDs canónicos de evento únicos en el registro actual':'unique canonical event IDs in the current register'}</span></div>
    <div class="mf-kpi"><strong>${stats.baseline}</strong><span>${lang==='es'?'justificantes RedSARA/REG-AGE detallados con PD-SP-EVT propio':'detailed RedSARA/REG-AGE receipts with their own PD-SP-EVT'}</span></div>
    <div class="mf-kpi"><strong>${stats.inbound}</strong><span>${lang==='es'?'filas entrantes de institución con ID de evento propio':'inbound institution rows with their own event ID'}</span></div>
    <div class="mf-kpi"><strong>${d.offices.length}</strong><span>${lang==='es'?'identidades de oficina/ruta en el directorio Ministerio Fiscal':'office/route identities in the Ministerio Fiscal directory'}</span></div>
  </div>`;
  const renderFilesTable = (files, officeMap) => `<div class="mf-table-wrap"><table class="mf-table"><thead><tr>
    <th>${lang==='es'?'ID maestro':'Master ID'}</th><th>${lang==='es'?'Referencia oficial':'Official reference'}</th><th>${lang==='es'?'Oficina/ruta':'Office/route'}</th><th>CAEPR / ^</th><th>${lang==='es'?'Estado':'State'}</th><th>${lang==='es'?'Control':'Control'}</th>
  </tr></thead><tbody>${files.map(f => `<tr id="file-${esc(f.master_id)}"><td><span class="mf-id">${esc(f.master_id)}</span></td><td><strong>${esc(f.reference)}</strong><br><span class="mf-muted">${esc(f.period)}</span></td><td>${f.office_ids.length ? f.office_ids.map(id => {const o=officeMap.get(id)||{};return esc(lang==='es'?(o.name_es||id):(o.name_en||o.name_es||id));}).join('<br>') : `<span class="mf-muted">${lang==='es'?'pendiente':'pending'}</span>`}</td><td>${f.caret_id ? `<span class="mf-id">${esc(f.caret_id)}</span>${f.verification==='CARET_PENDING'?'':' <span class="mf-caret">^</span>'}` : '—'}</td><td>${esc(t(f,'status'))}</td><td><span class="mf-status ${statusClass(f.verification)}">${esc(f.verification)}</span></td></tr>`).join('')}</tbody></table></div>`;
  const renderEventsTable = events => `<div class="mf-table-wrap"><table class="mf-table"><thead><tr><th>${lang==='es'?'Nuestro ID':'Our ID'}</th><th>${lang==='es'?'Fecha':'Date'}</th><th>${lang==='es'?'Dirección / tipo':'Direction / type'}</th><th>${lang==='es'?'Oficina':'Office'}</th><th>${lang==='es'?'Referencia oficial':'Official reference'}</th></tr></thead><tbody>${events.map(e=>`<tr id="event-${esc(e.event_id)}"><td><span class="mf-id">${esc(e.event_id)}</span></td><td>${esc(e.event_date||e.presented_local||'—')}</td><td>${esc(e.direction||'—')}<br><span class="mf-muted">${esc(e.record_type||e.layer||'—')}</span></td><td>${esc(e.office||'—')}</td><td>${e.official_reference?`<span class="mf-id">${esc(e.official_reference)}</span>`:'—'}</td></tr>`).join('')}</tbody></table></div>`;
  const renderHub = (d, stats) => {
    const officeMap = new Map(d.offices.map(o => [o.canonical_id,o]));
    target.innerHTML = `${renderKpis(d,stats)}
      <section class="mf-section mf-anchor" id="numbering"><p class="eyebrow">${lang==='es'?'Control de identidad':'Identity control'}</p><h2>${lang==='es'?'Un número nuestro para cada objeto; la referencia oficial permanece separada':'One Por Derecho number for each object; the official reference remains separate'}</h2><div class="mf-grid">
        <article class="mf-card"><h3>${lang==='es'?'Oficina / ruta':'Office / route'}</h3><p><span class="mf-id">PD-MF-OFF-####</span> <span class="mf-caret">^</span></p><p>${lang==='es'?'Identidad canónica del directorio. DIR3, si existe, queda como identificador oficial externo.':'Canonical directory identity. DIR3, where available, remains the external official identifier.'}</p></article>
        <article class="mf-card"><h3>${lang==='es'?'Expediente':'File / expediente'}</h3><p><span class="mf-id">GC-FIS / TF-FIS / LZ-FIS / NAT-FIS</span></p><p>${lang==='es'?'Se conserva el Master_ID existente; DI, DIP, EG, ST, CC/CA y NIG son referencias oficiales asociadas, no sustitutos.':'Existing Master_ID is preserved; DI, DIP, EG, ST, CC/CA and NIG are associated official references, not substitutes.'}</p></article>
        <article class="mf-card"><h3>${lang==='es'?'Comunicación / acto':'Communication / act'}</h3><p><span class="mf-id">PD-SP-EVT-####</span></p><p>${lang==='es'?'Cada escrito, justificante, respuesta, decreto, notificación, acuse o remisión probado por fuente conserva un evento estable separado de REGAGE.':'Each source-proved filing, receipt, response, decree, notice, acknowledgement or referral retains a stable event identity separate from REGAGE.'}</p></article>
      </div></section>
      <section class="mf-section mf-anchor" id="offices"><p class="eyebrow">${lang==='es'?'Jerarquía y rutas':'Hierarchy and routes'}</p><h2>${lang==='es'?'Directorio por oficina':'Office directory'}</h2><div class="mf-grid">${d.office_groups.filter(g=>g.group_key!=='unresolved').map(g=>`<article class="mf-card wide"><h3>${esc(t(g,'title'))}</h3><p>${esc(t(g,'description'))}</p><p>${d.offices.filter(o=>o.group_key===g.group_key).map(o=>`<span class="mf-id">${esc(o.canonical_id)}</span> ${esc(lang==='es'?o.name_es:o.name_en)} ${o.caret?'<span class="mf-caret">^</span>':''}`).join('<br>')}</p></article>`).join('')}</div></section>
      <section class="mf-section mf-anchor" id="expedientes"><p class="eyebrow">${lang==='es'?'Expedientes controlados':'Controlled files'}</p><h2>${lang==='es'?'Índice Ministerio Fiscal ↔ expediente':'Ministerio Fiscal ↔ file index'}</h2>${renderFilesTable(d.expedientes,officeMap)}</section>
      <section class="mf-section mf-anchor" id="gaps"><p class="eyebrow">${lang==='es'?'No ocultar los huecos':'Do not hide the gaps'}</p><h2>${lang==='es'?'Pendientes que impiden declarar completitud universal':'Open items preventing a universal completeness claim'}</h2>${d.priority_open_references.map(g=>`<div class="mf-gap"><strong>${esc(g.reference)}</strong><br><span class="mf-status pending">${esc(g.state)}</span><p>${esc(g.next)}</p></div>`).join('')}</section>`;
  };
  const renderOffices = (d, events) => {
    const officeMap = new Map(d.offices.map(o => [o.canonical_id,o]));
    const assigned = new Map();
    events.forEach(e => { const id = eventOfficeId(e); if (id) assigned.set(e.event_id,id); });
    const groupsHtml = d.office_groups.map(g => {
      const offices = d.offices.filter(o => o.group_key === g.group_key);
      const ids = new Set(offices.map(o=>o.canonical_id));
      const files = d.expedientes.filter(f => f.office_ids.some(id=>ids.has(id)) || (g.group_key==='unresolved' && !f.office_ids.length));
      const groupEvents = events.filter(e => ids.has(assigned.get(e.event_id)));
      return `<section class="mf-section mf-office-group" id="${esc(g.group_key)}"><div class="mf-office-head"><div><p class="eyebrow">${esc(g.group_key)}</p><h2>${esc(t(g,'title'))}</h2><p>${esc(t(g,'description'))}</p></div></div><div class="mf-office-list">${offices.length?offices.map(o=>`<article class="mf-office" id="${esc(o.canonical_id)}"><strong><span class="mf-id">${esc(o.canonical_id)}</span> ${o.caret?'<span class="mf-caret">^</span>':''}</strong><h3>${esc(lang==='es'?o.name_es:o.name_en)}</h3><small>${esc(o.tier)}${o.dir3?` · DIR3 ${esc(o.dir3)}`:''}</small><small>${esc(o.official_id_status)}</small></article>`).join(''):`<article class="mf-office"><strong>${lang==='es'?'Sin oficina cerrada por fuente':'No source-locked office'}</strong><p>${lang==='es'?'La referencia se mantiene abierta sin asignación especulativa.':'The reference remains open without speculative assignment.'}</p></article>`}</div>${files.length?`<h3 style="margin-top:22px">${lang==='es'?'Expedientes vinculados':'Linked files'}</h3>${renderFilesTable(files,officeMap)}`:''}${groupEvents.length?`<details style="margin-top:18px" open><summary><strong>${lang==='es'?'Eventos canónicos asignados por el campo de oficina':'Canonical events assigned from the office field'}: ${groupEvents.length}</strong></summary><div style="margin-top:10px">${renderEventsTable(groupEvents)}</div></details>`:''}</section>`;
    }).join('');
    const unmatched = events.filter(e => !assigned.has(e.event_id));
    const reconciliation = `<section class="mf-section mf-office-group" id="event-reconciliation"><p class="eyebrow">${lang==='es'?'Reconciliación de eventos':'Event reconciliation'}</p><h2>${lang==='es'?'Asignación de oficina es una capa separada':'Office assignment is a separate layer'}</h2><div class="mf-rule"><strong>${events.length - unmatched.length}/${events.length}</strong> ${lang==='es'?'eventos canónicos se pueden asignar a una oficina de este directorio usando únicamente el campo de oficina controlado. Los restantes no se adivinan ni se pierden: conservan su PD-SP-EVT en el registro canónico.':'canonical events can be assigned to a directory office using only the controlled office field. The remainder are neither guessed nor lost: they retain their PD-SP-EVT in the canonical register.'}</div>${unmatched.length?`<details style="margin-top:16px"><summary><strong>${lang==='es'?'Eventos aún no normalizados a una oficina del directorio':'Events not yet normalised to a directory office'}: ${unmatched.length}</strong></summary><div style="margin-top:10px">${renderEventsTable(unmatched)}</div></details>`:''}</section>`;
    target.innerHTML = groupsHtml + reconciliation;
  };
  Promise.all([
    fetch(directoryUrl,{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(`directory ${r.status}`);return r.json()}),
    fetch(communicationsUrl,{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(`communications ${r.status}`);return r.json()})
  ]).then(([d,c])=>{
    const events = Array.isArray(c.events) ? c.events : [];
    const stats = eventStats(events);
    if (stats.ids !== stats.rows) throw new Error('duplicate event_id detected');
    if (stats.baseline !== d.coverage_baseline.detailed_redsara_receipts_source_proved) throw new Error('RedSARA baseline mismatch');
    if (view === 'offices') renderOffices(d, events); else renderHub(d,stats);
  }).catch(err=>{target.innerHTML=`<div class="mf-error"><strong>${lang==='es'?'No se pudo cargar el directorio canónico':'Canonical directory could not be loaded'}</strong><p>${esc(err.message)}</p></div>`;});
})();

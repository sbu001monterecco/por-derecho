(() => {
  const script = document.currentScript;
  const root = document.querySelector('[data-mf-interconnectivity]');
  if (!script || !root) return;
  const base = new URL('../', new URL('.', script.src));
  const lang = document.documentElement.lang.toLowerCase().startsWith('es') ? 'es' : 'en';
  const dataUrl = new URL('assets/data/fiscalia-proceedings-interconnectivity-v1.json', base);
  const masterUrl = new URL('assets/data/proceedings-master-public-v1.json', base);
  const mapRoute = new URL(lang === 'es' ? 'es/mapa-procedimientos/' : 'en/proceedings-map/', base);
  const registerRoute = new URL(lang === 'es' ? 'es/registro-maestro-procedimientos/' : 'en/master-proceedings-register/', base);
  const t = lang === 'es' ? {
    load:'Cargando la interconexión controlada…', error:'No se pudo cargar la proyección de interconexión.',
    metrics:['Comunicaciones','Con referencia','Enlazadas','Expedientes exactos','Referencias no resueltas','Cadenas prioritarias'],
    search:'Buscar expediente, referencia, órgano o evento', direction:'Dirección', scope:'Ámbito', all:'Todos',
    files:'Expedientes y referencias de Fiscalía', timeline:'Cronología vinculada', events:'eventos', noEvents:'No hay eventos que coincidan con los filtros.',
    outbound:'Salientes', inbound:'Entrantes', acts:'Actos/decisiones', judicial:'Procedimientos judiciales enlazados', gap:'Fuente siguiente necesaria',
    exact:'Identidad canónica exacta', unresolved:'Referencia no resuelta', chains:'Nueve cadenas prioritarias',
    inside:'Dentro de procedimiento judicial', outside:'Expediente fiscal fuera del procedimiento judicial', bridge:'Puente entre expediente fiscal y procedimiento', support:'Referencia de apoyo', none:'Sin enlace a procedimiento',
    details:'Qué prueba / qué no prueba', master:'Abrir fila maestra', map:'Abrir trazabilidad', chainEvents:'eventos relacionados'
  } : {
    load:'Loading the controlled interconnectivity projection…', error:'The interconnectivity projection could not be loaded.',
    metrics:['Communications','With references','Proceeding-linked','Exact files','Unresolved references','Priority chains'],
    search:'Search file, reference, office or event', direction:'Direction', scope:'Scope', all:'All',
    files:'Fiscalía files and references', timeline:'Linked chronology', events:'events', noEvents:'No events match the current filters.',
    outbound:'Outbound', inbound:'Inbound', acts:'Acts/decisions', judicial:'Linked judicial proceedings', gap:'Next source needed',
    exact:'Exact canonical identity', unresolved:'Unresolved reference', chains:'Nine priority chains',
    inside:'Inside judicial proceeding', outside:'Fiscalía file outside judicial proceeding', bridge:'Fiscalía-to-proceeding bridge', support:'Supporting reference', none:'No proceeding link',
    details:'What it proves / does not prove', master:'Open master row', map:'Open trace', chainEvents:'related events'
  };
  const esc = (v) => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const scopeLabel = (s) => ({INSIDE_JUDICIAL_PROCEEDING:t.inside,OUTSIDE_JUDICIAL_PROCEEDING:t.outside,CROSS_FILE_BRIDGE:t.bridge,SUPPORT_REFERENCE_ONLY:t.support,NO_PROCEEDING_LINK:t.none}[s] || s);
  const routeToMaster = (id) => `${registerRoute.href}#record-${encodeURIComponent(id)}`;
  const routeToMap = (id) => `${mapRoute.href}#trace-proceeding=${encodeURIComponent(id)}`;
  let payload, masterById, selected = 'ALL';

  const parseHash = () => {
    const match = location.hash.match(/^#file=([^&]+)/);
    return match ? decodeURIComponent(match[1]) : 'ALL';
  };
  const metric = (n,label) => `<div class="pd-mf-metric"><strong>${esc(n)}</strong><span>${esc(label)}</span></div>`;

  function renderShell(){
    const c=payload.coverage;
    root.innerHTML = `
      <section class="pd-mf-metrics" aria-label="${esc(t.metrics.join(', '))}">
        ${metric(c.communication_events,t.metrics[0])}${metric(c.matter_linked_events,t.metrics[1])}${metric(c.proceeding_linked_events,t.metrics[2])}${metric(c.fiscalia_exact_files,t.metrics[3])}${metric(c.fiscalia_unresolved_references,t.metrics[4])}${metric(payload.priority_chains.length,t.metrics[5])}
      </section>
      <section class="pd-mf-panel"><div class="pd-mf-controls">
        <label>${esc(t.search)}<input type="search" data-mf-search></label>
        <label>${esc(t.direction)}<select data-mf-direction><option value="">${esc(t.all)}</option><option>OUTBOUND_TO_INSTITUTION</option><option>INBOUND_FROM_INSTITUTION</option><option>INSTITUTION_TO_INSTITUTION</option><option>SELF_ARCHIVE_CONTROL</option><option>NON_SENT_DRAFT</option></select></label>
        <label>${esc(t.scope)}<select data-mf-scope><option value="">${esc(t.all)}</option><option value="OUTSIDE_JUDICIAL_PROCEEDING">${esc(t.outside)}</option><option value="INSIDE_JUDICIAL_PROCEEDING">${esc(t.inside)}</option><option value="CROSS_FILE_BRIDGE">${esc(t.bridge)}</option><option value="SUPPORT_REFERENCE_ONLY">${esc(t.support)}</option><option value="NO_PROCEEDING_LINK">${esc(t.none)}</option></select></label>
      </div></section>
      <div class="pd-mf-layout"><aside class="pd-mf-panel"><h2>${esc(t.files)}</h2><div class="pd-mf-files" data-mf-files></div></aside><section class="pd-mf-panel" data-mf-detail aria-live="polite"></section></div>
      <section class="pd-mf-panel" id="priority-chains"><p class="eyebrow">01–09</p><h2>${esc(t.chains)}</h2><div class="pd-mf-chains" data-mf-chains></div></section>`;
    root.querySelector('[data-mf-search]').addEventListener('input', render);
    root.querySelector('[data-mf-direction]').addEventListener('change', renderDetail);
    root.querySelector('[data-mf-scope]').addEventListener('change', renderDetail);
    addEventListener('hashchange',()=>{selected=parseHash();render();});
  }

  function matchingFiles(){
    const q=root.querySelector('[data-mf-search]').value.trim().toLowerCase();
    if(!q) return payload.fiscalia_files;
    return payload.fiscalia_files.filter(f=>[f.master_id,f.reference,f.secondary_reference,f.office,f.status,f.open_reference_gap,...f.linked_event_ids].join(' ').toLowerCase().includes(q));
  }
  function currentSelection(){
    if(selected==='ALL') return null;
    const file=payload.fiscalia_files.find(f=>f.master_id===selected);
    if(file) return {...file,event_ids:file.linked_event_ids,is_fiscalia_identity:true};
    const connection=payload.by_master_id[selected];
    const record=masterById[selected];
    if(!connection||!record) return null;
    const events=payload.events.filter(e=>connection.event_ids.includes(e.event_id));
    return {master_id:selected,identity_state:'PROCEEDING_LINKED_VIEW',reference:record.Reference,office:record.Current_Custodian||record.Origin_Organ,status:record.Status,open_reference_gap:record.Open_Reference_Gap,event_ids:connection.event_ids,is_fiscalia_identity:false,linked_judicial_master_ids:[],counts:{outbound:events.filter(e=>e.direction==='OUTBOUND_TO_INSTITUTION').length,inbound:events.filter(e=>e.direction==='INBOUND_FROM_INSTITUTION').length,official_acts_or_decisions:events.filter(e=>e.record_type.startsWith('OFFICIAL_')).length,linked_judicial_proceedings:1}};
  }
  function renderFiles(){
    const files=matchingFiles();
    const allCount=payload.events.length;
    const external=currentSelection();
    const externalButton=external&&!external.is_fiscalia_identity?`<button class="pd-mf-file" data-file="${esc(external.master_id)}" aria-current="true"><span class="pd-mf-count">${external.event_ids.length}</span><strong>${esc(external.master_id)} · ${esc(external.reference)}</strong><small>${esc(t.inside)}</small></button>`:'';
    root.querySelector('[data-mf-files]').innerHTML=`<button class="pd-mf-file" data-file="ALL" aria-current="${selected==='ALL'}"><span class="pd-mf-count">${allCount}</span><strong>${esc(t.all)}</strong><small>${esc(t.timeline)}</small></button>${externalButton}`+files.map(f=>`<button class="pd-mf-file" data-file="${esc(f.master_id)}" data-state="${esc(f.identity_state)}" aria-current="${selected===f.master_id}"><span class="pd-mf-count">${f.counts.events}</span><strong>${esc(f.master_id)} · ${esc(f.reference)}</strong><small>${esc(f.office)}</small></button>`).join('');
    root.querySelectorAll('[data-file]').forEach(btn=>btn.addEventListener('click',()=>{selected=btn.dataset.file;history.replaceState(null,'',selected==='ALL'?'#file=ALL':`#file=${encodeURIComponent(selected)}`);render();}));
  }
  function filteredEvents(selection){
    const direction=root.querySelector('[data-mf-direction]').value;
    const scope=root.querySelector('[data-mf-scope]').value;
    const q=root.querySelector('[data-mf-search]').value.trim().toLowerCase();
    const ids=selection?new Set(selection.event_ids):null;
    return payload.events.filter(e=>(!ids||ids.has(e.event_id))&&(!direction||e.direction===direction)&&(!scope||e.interconnectivity_scope===scope)&&(!q||[e.event_id,e.official_reference,e.office,e.public_summary,...e.matter_references,...e.master_ids].join(' ').toLowerCase().includes(q))).sort((a,b)=>(a.event_date||'').localeCompare(b.event_date||'')||a.event_id.localeCompare(b.event_id));
  }
  function eventCard(e){
    const refs=e.master_ids.map(id=>`<a href="${esc(routeToMaster(id))}">${esc(id)}</a>`).join('');
    const proof=[...(e.proves||[]),...(e.does_not_prove||[]).map(x=>`${lang==='es'?'No prueba':'Does not prove'}: ${x}`)];
    return `<article class="pd-mf-event" data-event-id="${esc(e.event_id)}" data-direction="${esc(e.direction)}"><header><strong>${esc(e.event_date||'—')} · ${esc(e.record_type)}</strong><span class="pd-mf-code">${esc(e.event_id)}</span></header><div class="pd-mf-badges"><span class="pd-mf-badge">${esc(e.direction)}</span><span class="pd-mf-badge">${esc(scopeLabel(e.interconnectivity_scope))}</span><span class="pd-mf-badge">${esc(e.allocation_state)}</span></div><p><strong>${esc(e.official_reference||e.office||'—')}</strong>${e.public_summary?` — ${esc(e.public_summary)}`:''}</p>${refs?`<p class="pd-mf-links">${refs}</p>`:''}<details><summary>${esc(t.details)}</summary>${proof.map(x=>`<p>${esc(x)}</p>`).join('')}<p class="pd-mf-muted">${esc(e.source.status||'')}</p></details></article>`;
  }
  function renderDetail(){
    let file=currentSelection();
    if(selected!=='ALL'&&!file){selected='ALL';file=null;}
    const events=filteredEvents(file);
    const detail=root.querySelector('[data-mf-detail]');
    const head=file?`<div class="pd-mf-detail-head"><div><p class="eyebrow">${esc(file.is_fiscalia_identity?(file.identity_state==='EXACT_CANONICAL'?t.exact:t.unresolved):t.inside)}</p><h2><span class="pd-mf-code">${esc(file.master_id)}</span> · ${esc(file.reference)}</h2><p>${esc(file.office)}</p></div><div><a class="pd-mf-button" href="${esc(routeToMaster(file.master_id))}">${esc(t.master)}</a></div></div><div class="pd-mf-badges"><span class="pd-mf-badge">${file.counts.outbound} ${esc(t.outbound)}</span><span class="pd-mf-badge">${file.counts.inbound} ${esc(t.inbound)}</span><span class="pd-mf-badge">${file.counts.official_acts_or_decisions} ${esc(t.acts)}</span><span class="pd-mf-badge">${file.counts.linked_judicial_proceedings} ${esc(t.judicial)}</span></div><p>${esc(file.status)}</p>${file.open_reference_gap?`<div class="pd-mf-gap"><strong>${esc(t.gap)}:</strong> ${esc(file.open_reference_gap)}</div>`:''}${file.linked_judicial_master_ids.length?`<p class="pd-mf-links">${file.linked_judicial_master_ids.map(id=>`<a href="${esc(routeToMap(id))}">${esc(id)} · ${esc(masterById[id]?.Reference||'')}</a>`).join(' ')}</p>`:''}`:`<p class="eyebrow">${esc(t.all)}</p><h2>${esc(t.timeline)}</h2><p class="pd-mf-muted">${esc(payload.boundaries[lang])}</p>`;
    detail.innerHTML=`${head}<h3>${events.length} ${esc(t.events)}</h3><div class="pd-mf-events">${events.length?events.map(eventCard).join(''):`<p class="pd-mf-empty">${esc(t.noEvents)}</p>`}</div>`;
  }
  function renderChains(){
    root.querySelector('[data-mf-chains]').innerHTML=payload.priority_chains.map(c=>`<article class="pd-mf-chain" id="${esc(c.chain_id)}"><span class="pd-mf-code">${esc(c.chain_id)} · ${esc(c.period)}</span><h3>${esc(c[`title_${lang}`])}</h3><p class="pd-mf-muted">${esc(c.relationship_status)}</p><p>${c.master_ids.map(id=>`<a href="#file=${encodeURIComponent(id)}">${esc(id)}</a>`).join(' · ')}</p><small>${c.event_count} ${esc(t.chainEvents)}</small></article>`).join('');
  }
  function render(){renderFiles();renderDetail();renderChains();}
  async function init(){
    try{
      const [d,m]=await Promise.all([fetch(dataUrl,{cache:'no-store'}),fetch(masterUrl,{cache:'no-store'})]);
      if(!d.ok||!m.ok) throw new Error(`HTTP ${d.status}/${m.status}`);
      payload=await d.json(); const master=await m.json(); masterById=Object.fromEntries(master.records.map(r=>[r.Master_ID,r]));
      selected=parseHash();renderShell();render();
    }catch(err){root.innerHTML=`<p class="pd-mf-error">${esc(t.error)} ${esc(err.message)}</p>`;}
  }
  init();
})();

(()=>{
  'use strict';
  const d=document;
  const root=d.querySelector('[data-authority-register]');
  if(!root||root.dataset.ready==='true')return;
  root.dataset.ready='true';
  const script=d.currentScript;
  const assetBase=script?new URL('.',script.src):new URL('/por-derecho/assets/',location.origin);
  const isEs=(d.documentElement.lang||'').toLowerCase().startsWith('es');
  const copy=isEs?{
    loading:'Cargando el registro controlado…',error:'No se pudo cargar el registro controlado. La fuente canónica sigue disponible como dato público.',
    all:'Todos',filings:'Presentaciones Red SARA/AGE',responses:'Respuestas entrantes',outbound:'Otras comunicaciones salientes',
    rows:n=>`${n} filas`,search:'Buscar por ID canónico, referencia, expediente, órgano o fecha',
    source:'Fuente controlada',proof:'Qué prueba',limit:'Qué no prueba',attachments:'Índice de adjuntos',showAttachments:'Ver índice de adjuntos',
    control:'Control y límites de lectura',filing:'Presentación registral',response:'Respuesta institucional',communication:'Comunicación institucional',
    noResults:'No hay coincidencias para este filtro.',details:'Mostrar detalles',hide:'Ocultar detalles',canonical:'Registro canónico',
    status:'Estado de prueba',event:'Evento',reference:'Referencia',date:'Fecha',office:'Órgano',annexes:'Anexos indicados',notStated:'No declarado',
  }:{
    loading:'Loading the controlled register…',error:'The controlled register could not be loaded. Its canonical public data source remains available.',
    all:'All',filings:'Red SARA/AGE filings',responses:'Inbound responses',outbound:'Other outbound communications',
    rows:n=>`${n} rows`,search:'Search by canonical ID, reference, file, office or date',
    source:'Controlled source',proof:'What this proves',limit:'What this does not prove',attachments:'Attachment index',showAttachments:'View attachment index',
    control:'Reading controls and limits',filing:'Registry filing',response:'Institutional response',communication:'Institutional communication',
    noResults:'No records match this filter.',details:'Show details',hide:'Hide details',canonical:'Canonical register',
    status:'Evidence state',event:'Event',reference:'Reference',date:'Date',office:'Office',annexes:'Listed annexes',notStated:'Not stated',
  };
  const normalize=value=>String(value||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9€]+/g,' ').trim();
  const esc=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const array=value=>Array.isArray(value)?value.filter(Boolean):[];
  const eventSummary=event=>{
    const summary=isEs?event.public_summary_es:event.public_summary;
    if(summary)return summary;
    if(event.channel==='REGAGE')return isEs?'Consta la presentación registral. El contenido sustantivo y cada paso posterior requieren fuente independiente.':'The registry presentation is controlled. Substantive content and every downstream step require an independent source.';
    return isEs?'Consta un evento institucional de fuente controlada; su alcance se limita a lo que declara la fuente.':'A source-controlled institutional event is recorded; its scope is limited to what the source states.';
  };
  const eventType=event=>event.channel==='REGAGE'?copy.filing:event.direction==='INBOUND_FROM_INSTITUTION'?copy.response:copy.communication;
  const proofText=event=>{
    if(isEs&&event.proves_es)return Array.isArray(event.proves_es)?event.proves_es:[event.proves_es];
    if(!isEs&&array(event.proves).length)return event.proves;
    return event.channel==='REGAGE'
      ? [isEs?'La presentación al registro, fecha, destino declarado y metadatos de anexos que constan.':'The stated registry presentation, date, destination and listed annex metadata.']
      : [isEs?'El acto, aviso o comunicación en el alcance declarado por la fuente.':'The act, notice or communication only to the extent stated by the source.'];
  };
  const limitText=event=>{
    if(isEs&&event.does_not_prove_es)return Array.isArray(event.does_not_prove_es)?event.does_not_prove_es:[event.does_not_prove_es];
    if(!isEs&&array(event.does_not_prove).length)return event.does_not_prove;
    return [isEs?'No prueba por sí solo examen de fondo, decisión, utilización, pago, causalidad, dolo, delito ni culpabilidad.':'It does not alone prove merits examination, decision, use, payment, causation, intent, offence or guilt.'];
  };
  const sourceLabel=event=>event.source_integrity?.repository_anchor||copy.notStated;
  const filterFor=(event,active)=>active==='all'||(active==='filing'&&event.channel==='REGAGE')||(active==='response'&&event.direction==='INBOUND_FROM_INSTITUTION')||(active==='outbound'&&event.direction==='OUTBOUND_TO_INSTITUTION'&&event.channel!=='REGAGE');
  const matches=(event,query)=>{
    if(!query)return true;
    const haystack=[event.event_id,event.official_reference,event.office,event.institution_key,event.record_type,event.channel,event.direction,event.event_date,...array(event.matter_references),...array(event.legacy_evidence_ids)].join(' ');
    return normalize(haystack).includes(normalize(query));
  };
  const proofList=(label,values,kind)=>`<div class="pd-acr-proof pd-acr-proof-${kind}"><strong>${esc(label)}</strong><ul>${values.map(value=>`<li>${esc(value)}</li>`).join('')}</ul></div>`;
  const renderEvent=event=>{
    const reference=event.official_reference||event.event_id;
    const annexes=Number.isInteger(event.annex_count)?String(event.annex_count):copy.notStated;
    const tags=[eventType(event),event.record_type,event.channel,event.direction,...array(event.evidence_classes)].filter(Boolean);
    return `<article class="pd-acr-event" id="communication-${esc(event.event_id)}"><header><p class="pd-acr-kicker">${esc(event.event_id)} · ${esc(eventType(event))}</p><h2>${esc(reference)}</h2><p class="pd-acr-office">${esc(event.office||copy.notStated)}</p></header><dl class="pd-acr-meta"><div><dt>${esc(copy.date)}</dt><dd>${esc(event.presented_local||event.event_date||copy.notStated)}</dd></div><div><dt>${esc(copy.annexes)}</dt><dd>${esc(annexes)}</dd></div><div><dt>${esc(copy.source)}</dt><dd><code>${esc(sourceLabel(event))}</code></dd></div></dl><p>${esc(eventSummary(event))}</p><div class="pd-acr-tags">${tags.slice(0,7).map(tag=>`<span>${esc(tag)}</span>`).join('')}</div><details><summary>${esc(copy.details)}</summary>${proofList(copy.proof,proofText(event),'prove')}${proofList(copy.limit,limitText(event),'limit')}</details></article>`;
  };
  const run=async()=>{
    const [communicationsResult,filingsResult]=await Promise.allSettled([
      fetch(new URL('data/institutional-communications-register-v1.json?v=20260901a',assetBase)).then(response=>{if(!response.ok)throw new Error(`HTTP ${response.status}`);return response.json();}),
      fetch(new URL('data/redsara-age-filings-register-v1.json?v=20260901a',assetBase)).then(response=>{if(!response.ok)throw new Error(`HTTP ${response.status}`);return response.json();})
    ]);
    if(communicationsResult.status!=='fulfilled'||filingsResult.status!=='fulfilled'){
      root.innerHTML=`<p class="pd-acr-error">${esc(copy.error)}</p>`;
      return;
    }
    const communications=communicationsResult.value;
    const filings=filingsResult.value;
    const events=array(communications.events).slice().sort((left,right)=>String(right.presented_local||right.event_date||'').localeCompare(String(left.presented_local||left.event_date||''))||String(left.event_id).localeCompare(String(right.event_id)));
    const scope=filings.scope_and_boundary||{};
    const responseCount=events.filter(event=>event.direction==='INBOUND_FROM_INSTITUTION').length;
    const filingCount=events.filter(event=>event.channel==='REGAGE').length;
    root.innerHTML=`<section class="pd-acr-controls"><div><p class="eyebrow">${esc(copy.canonical)} · PD-SP-INSTITUTIONAL-COMMUNICATIONS-001</p><h2>${esc(copy.control)}</h2><p>${esc(scope.receipt_boundary||'')}</p><p>${esc(scope.reconciliation_boundary||'')}</p></div><dl class="pd-acr-stats"><div><dt>${esc(copy.filings)}</dt><dd>${esc(filingCount)}</dd></div><div><dt>${esc(copy.responses)}</dt><dd>${esc(responseCount)}</dd></div><div><dt>${esc(copy.attachments)}</dt><dd>${esc((filings.attachment_index||[]).length)}</dd></div></dl></section><section class="pd-acr-finder"><label for="pd-acr-search">${esc(copy.search)}</label><input id="pd-acr-search" type="search" autocomplete="off" placeholder="${esc(copy.search)}"><div class="pd-acr-filters"><button type="button" data-acr-filter="all" aria-pressed="true">${esc(copy.all)}</button><button type="button" data-acr-filter="filing" aria-pressed="false">${esc(copy.filings)}</button><button type="button" data-acr-filter="response" aria-pressed="false">${esc(copy.responses)}</button><button type="button" data-acr-filter="outbound" aria-pressed="false">${esc(copy.outbound)}</button></div><p class="pd-acr-count" aria-live="polite"></p></section><section class="pd-acr-results" aria-live="polite"></section><details class="pd-acr-attachments"><summary>${esc(copy.showAttachments)} · ${esc((filings.attachment_index||[]).length)}</summary><p>${esc(scope.attachment_boundary||'')}</p><ol>${array(filings.attachment_index).map(item=>`<li><code>${esc(item.filename)}</code><br><small>SHA-512: <code>${esc(item.sha512_as_listed)}</code> · ${esc(item.receipt_occurrences)} ${isEs?'apariciones en justificantes':'receipt occurrences'}</small></li>`).join('')}</ol></details>`;
    const input=root.querySelector('#pd-acr-search');
    const count=root.querySelector('.pd-acr-count');
    const results=root.querySelector('.pd-acr-results');
    const buttons=[...root.querySelectorAll('[data-acr-filter]')];
    let active='all';
    const render=()=>{
      const rows=events.filter(event=>filterFor(event,active)&&matches(event,input.value)).slice(0,400);
      count.textContent=copy.rows(rows.length);
      results.innerHTML=rows.length?rows.map(renderEvent).join(''):`<p class="pd-acr-empty">${esc(copy.noResults)}</p>`;
      if(location.hash.startsWith('#communication-'))d.getElementById(location.hash.slice(1))?.scrollIntoView({block:'start'});
    };
    buttons.forEach(button=>button.addEventListener('click',()=>{active=button.dataset.acrFilter||'all';buttons.forEach(item=>item.setAttribute('aria-pressed',String(item===button)));render();}));
    input.addEventListener('input',render);
    render();
  };
  run();
})();

(() => {
  'use strict';
  const root = document.querySelector('[data-identity-registry]');
  if (!root) return;

  const es = root.dataset.lang === 'es';
  const c = es ? {
    loading:'Cargando registro canónico y controles operativos…', fail:'No se pudo cargar el registro. Los JSON canónicos siguen disponibles mediante los enlaces de fuente.', actionFail:'Matriz de acciones no disponible', showing:(n,t)=>`Mostrando ${n} de ${t} identidades controladas.`, none:'Ningún registro coincide con la búsqueda y los filtros actuales.', open:'Abrir ficha →', aliases:'Alias', legacy:'Claves heredadas', notSame:'No confundir con', copy:'Copiar ID', copied:'Copiado', noActions:'Sin control activo enlazado', more:n=>`+${n} más`, defaultState:'Entrada admitida al corpus', archiveOpen:'Revisión retrospectiva abierta', archiveClosed:'Revisión retrospectiva cerrada', integrityOk:'Íntegro: IDs, recuentos y referencias internas coherentes', integrityBad:n=>`${n} incidencia${n===1?'':'s'} de integridad detectada${n===1?'':'s'}`, actions:(n,p0,p1)=>`${n} controles · ${p0} P0 · ${p1} P1`, controlDate:d=>`Fecha de control: ${d}`, export:n=>`Exportar ${n} resultado${n===1?'':'s'} en CSV`, file:'registro-identidad-materia-resultados.csv', headers:['ID','Clase','Nombre canónico','Alias','Estado de control','Claves heredadas','No confundir con','Controles activos','Ficha pública'],
    types:{ALL:'Todos',PERSON:'Persona',ORGANISATION:'Organización',STRUCTURE:'Estructura',INSTITUTION:'Institución',PROCEEDING:'Procedimiento'},
    states:{CONTROLLED_PERIMETER_LABEL_EXACT_ENTITY_MAY_REQUIRE_SOURCE:'Etiqueta de perímetro; entidad jurídica exacta pendiente de fuente',REFERENCED_LEGAL_FORM_VARIANT_UNRESOLVED:'Variante de forma jurídica citada; correspondencia exacta no resuelta'}
  } : {
    loading:'Loading canonical registry and operational controls…', fail:'The registry could not be loaded. The canonical JSON files remain available through the source links.', actionFail:'Action matrix unavailable', showing:(n,t)=>`Showing ${n} of ${t} controlled identities.`, none:'No record matches the current search and filters.', open:'Open profile →', aliases:'Aliases', legacy:'Legacy keys', notSame:'Not the same as', copy:'Copy ID', copied:'Copied', noActions:'No linked active control', more:n=>`+${n} more`, defaultState:'Entry admitted to the corpus', archiveOpen:'Retrospective archive review open', archiveClosed:'Retrospective archive review closed', integrityOk:'Integral: IDs, counts and internal references are coherent', integrityBad:n=>`${n} integrity issue${n===1?'':'s'} detected`, actions:(n,p0,p1)=>`${n} controls · ${p0} P0 · ${p1} P1`, controlDate:d=>`Control date: ${d}`, export:n=>`Export ${n} result${n===1?'':'s'} as CSV`, file:'matter-identity-registry-results.csv', headers:['ID','Class','Canonical name','Aliases','Control state','Legacy keys','Not the same as','Active controls','Public profile'],
    types:{ALL:'All',PERSON:'Person',ORGANISATION:'Organisation',STRUCTURE:'Structure',INSTITUTION:'Institution',PROCEEDING:'Proceeding'},
    states:{CONTROLLED_PERIMETER_LABEL_EXACT_ENTITY_MAY_REQUIRE_SOURCE:'Perimeter label; exact legal entity still requires source confirmation',REFERENCED_LEGAL_FORM_VARIANT_UNRESOLVED:'Referenced legal-form variant; exact match remains unresolved'}
  };

  const $ = s => root.querySelector(s), $$ = s => [...root.querySelectorAll(s)];
  const body=$('[data-registry-body]'), status=$('[data-registry-status]'), search=$('[data-registry-search]'), reset=$('[data-registry-reset]'), exp=$('[data-registry-export]');
  const typeButtons=$$('[data-type-filter]'), controlButtons=$$('[data-control-filter]'), statNodes=$$('[data-registry-stat]');
  const controlDate=$('[data-registry-control-date]'), coverage=$('[data-registry-coverage]'), actionState=$('[data-registry-actions]'), integrity=$('[data-registry-integrity]');
  const validTypes=new Set(['ALL','PERSON','ORGANISATION','STRUCTURE','INSTITUTION','PROCEEDING']);
  const validViews=new Set(['ALL','QUALIFIED','ACTION','NO_ROUTE']);
  let records=[], shown=[], matrix=null, actionsById=new Map(), type='ALL', view='ALL', matrixWarning=false;

  const norm=v=>String(v||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
  const stateLabel=r=>c.states[r.status]||(r.status?r.status.toLowerCase().replace(/_/g,' '):c.defaultState);
  const prefix=location.pathname.includes('/por-derecho/')?'/por-derecho':'';
  const routeFor=r=>{const route=r.routes&&(r.routes[root.dataset.lang]||r.routes.en||r.routes.es);if(!route)return null;if(/^https?:\/\//i.test(route))return route;return `${prefix}${route.startsWith('/')?route:`/${route}`}`;};
  const actionHub=root.dataset.actionHubUrl?new URL(root.dataset.actionHubUrl,document.baseURI).href:null;

  function indexActions(){
    actionsById=new Map();
    (matrix?.actions||[]).forEach(a=>new Set([...(a.recipients||[]),...(a.actors||[]),...(a.proceedings||[])]).forEach(id=>{
      if(!actionsById.has(id))actionsById.set(id,[]);actionsById.get(id).push(a);
    }));
    actionsById.forEach(list=>list.sort((a,b)=>String(a.priority||'').localeCompare(String(b.priority||''))||String(a.action_id).localeCompare(String(b.action_id))));
  }

  const searchText=r=>norm([r.id,r.name,r.type,r.status,stateLabel(r),...(r.aliases||[]),...(r.legacy||[]),...(r.not_same_as||[]),...(actionsById.get(r.id)||[]).flatMap(a=>[a.action_id,a.priority,a.title,a.status])].join(' '));

  function check(index,parts){
    const issues=[], all=parts.flatMap(p=>p.records||[]), ids=new Set();
    all.forEach(r=>{if(!r?.id||!r?.name||!r?.type)issues.push('required-fields');if(ids.has(r.id))issues.push(`duplicate:${r.id}`);ids.add(r.id);const fmt=index.id_formats?.[r.type];if(fmt&&!r.id.startsWith(fmt.replace('####','')))issues.push(`format:${r.id}`);});
    if(Number(index.counts?.total)!==all.length)issues.push('count:total');
    Object.entries(all.reduce((o,r)=>(o[r.type]=(o[r.type]||0)+1,o),{})).forEach(([k,n])=>{if(Number(index.counts?.[k])!==n)issues.push(`count:${k}`);});
    (index.parts||[]).forEach((p,i)=>{if(Number(p.count)!==(parts[i]?.records||[]).length)issues.push(`part:${p.path}`);});
    all.forEach(r=>(r.not_same_as||[]).forEach(id=>{if(id===r.id||!ids.has(id))issues.push(`not-same:${r.id}:${id}`);}));
    (matrix?.actions||[]).forEach(a=>[...(a.recipients||[]),...(a.actors||[]),...(a.proceedings||[])].forEach(id=>{if(!ids.has(id))issues.push(`action:${a.action_id}:${id}`);}));
    return [...new Set(issues)];
  }

  function cell(row,cls,text){const td=document.createElement('td');if(cls)td.className=cls;if(text!==undefined)td.textContent=text;row.appendChild(td);return td;}
  function meta(parent,label,values,links=false){if(!values?.length)return;const line=document.createElement('span');line.className='id-meta-line';const b=document.createElement('b');b.textContent=`${label}: `;line.appendChild(b);values.forEach((v,i)=>{if(i)line.append(' · ');if(links){const a=document.createElement('a');a.href=`?q=${encodeURIComponent(v)}#${encodeURIComponent(v)}`;a.textContent=v;line.appendChild(a);}else line.append(v);});parent.appendChild(line);}
  async function copyId(id,button){try{if(navigator.clipboard?.writeText)await navigator.clipboard.writeText(id);else{const t=document.createElement('textarea');t.value=id;document.body.appendChild(t);t.select();document.execCommand('copy');t.remove();}const old=button.textContent;button.textContent=c.copied;setTimeout(()=>button.textContent=old,1100);}catch(e){console.error(e);}}

  function renderRow(r){
    const row=document.createElement('tr');row.id=r.id;row.dataset.registryId=r.id;if(r.status)row.classList.add('is-qualified');
    const idCell=cell(row,'id-code'), permalink=document.createElement('a');permalink.className='id-permalink';permalink.href=`#${r.id}`;permalink.textContent=r.id;idCell.appendChild(permalink);const copy=document.createElement('button');copy.type='button';copy.className='id-copy';copy.textContent=c.copy;copy.onclick=()=>copyId(r.id,copy);idCell.appendChild(copy);
    const name=cell(row,'id-name'), strong=document.createElement('strong');strong.textContent=r.name;name.appendChild(strong);meta(name,c.aliases,r.aliases);meta(name,c.legacy,r.legacy);meta(name,c.notSame,r.not_same_as,true);
    const typeCell=cell(row), badge=document.createElement('span');badge.className='id-type';badge.textContent=c.types[r.type]||r.type;typeCell.appendChild(badge);
    const state=cell(row,'id-state-cell'), stateBadge=document.createElement('span');stateBadge.className=`id-state${r.status?' is-qualified':''}`;stateBadge.textContent=stateLabel(r);state.appendChild(stateBadge);if(r.status){const code=document.createElement('code');code.textContent=r.status;state.appendChild(code);}
    const actionCell=cell(row,'id-actions-cell'), actionList=actionsById.get(r.id)||[];if(!actionList.length){actionCell.textContent='—';actionCell.title=c.noActions;}else{const group=document.createElement('div');group.className='id-action-list';actionList.slice(0,4).forEach(a=>{const chip=actionHub?document.createElement('a'):document.createElement('span');chip.className=`id-action-chip ${String(a.priority||'').toLowerCase()}`;chip.textContent=a.action_id;chip.title=`${a.action_id} · ${a.priority||''} · ${a.title||''}`;if(actionHub)chip.href=actionHub;group.appendChild(chip);});if(actionList.length>4){const more=document.createElement('span');more.className='id-action-more';more.textContent=c.more(actionList.length-4);more.title=actionList.slice(4).map(a=>`${a.action_id} · ${a.title||''}`).join('\n');group.appendChild(more);}actionCell.appendChild(group);}
    const routeCell=cell(row,'id-route'), route=routeFor(r);if(route){const a=document.createElement('a');a.href=route;a.textContent=c.open;routeCell.appendChild(a);}else routeCell.textContent='—';
    return row;
  }

  function syncUrl(){const u=new URL(location.href),q=search?.value.trim()||'';q?u.searchParams.set('q',q):u.searchParams.delete('q');type!=='ALL'?u.searchParams.set('type',type):u.searchParams.delete('type');view!=='ALL'?u.searchParams.set('view',view):u.searchParams.delete('view');history.replaceState(null,'',`${u.pathname}${u.search}${u.hash}`);}
  function highlight(){root.querySelectorAll('tr.is-target').forEach(r=>r.classList.remove('is-target'));const id=decodeURIComponent(location.hash.slice(1));if(id){const row=document.getElementById(id);if(row?.closest('[data-identity-registry]')===root)row.classList.add('is-target');}}
  function render(){
    const q=norm(search?.value||'');shown=records.filter(r=>(type==='ALL'||r.type===type)&&(view==='ALL'||(view==='QUALIFIED'&&r.status)||(view==='ACTION'&&actionsById.has(r.id))||(view==='NO_ROUTE'&&!routeFor(r)))&&(!q||r._search.includes(q)));
    body.replaceChildren();if(!shown.length){const row=document.createElement('tr'),td=cell(row,'id-empty',c.none);td.colSpan=6;body.appendChild(row);}else shown.forEach(r=>body.appendChild(renderRow(r)));
    status.textContent=c.showing(shown.length,records.length);if(exp){exp.disabled=!shown.length;exp.textContent=c.export(shown.length);}typeButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.typeFilter===type)));controlButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.controlFilter===view)));syncUrl();highlight();
  }

  function stats(){const counts=records.reduce((o,r)=>(o[r.type]=(o[r.type]||0)+1,o),{}),v={TOTAL:records.length,...counts,QUALIFIED:records.filter(r=>r.status).length,ACTION_LINKED:records.filter(r=>actionsById.has(r.id)).length};statNodes.forEach(n=>n.textContent=v[n.dataset.registryStat]??0);}
  function controlPanel(index,issues){if(controlDate){const d=new Date(`${index.control_date}T00:00:00Z`),formatted=Number.isNaN(d.getTime())?index.control_date:new Intl.DateTimeFormat(es?'es-ES':'en-GB',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'}).format(d);controlDate.textContent=c.controlDate(formatted);}if(coverage)coverage.textContent=index.coverage?.archive_backfill==='OPEN'?c.archiveOpen:c.archiveClosed;if(actionState){const a=matrix?.actions||[];actionState.textContent=matrix?c.actions(a.length,a.filter(x=>x.priority==='P0').length,a.filter(x=>x.priority==='P1').length):c.actionFail;}if(integrity){const n=issues.length+(matrixWarning?1:0);integrity.textContent=n?c.integrityBad(n):c.integrityOk;integrity.classList.toggle('is-warning',Boolean(n));integrity.title=[...issues,...(matrixWarning?['action-matrix-unavailable']:[])].join('\n');}}

  function csv(){const esc=v=>`"${String(v??'').replace(/"/g,'""')}"`,rows=[c.headers,...shown.map(r=>[r.id,c.types[r.type]||r.type,r.name,(r.aliases||[]).join(' | '),stateLabel(r),(r.legacy||[]).join(' | '),(r.not_same_as||[]).join(' | '),(actionsById.get(r.id)||[]).map(a=>a.action_id).join(' | '),routeFor(r)||''])],blob=new Blob([`\uFEFF${rows.map(r=>r.map(esc).join(',')).join('\r\n')}`],{type:'text/csv;charset=utf-8'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=c.file;document.body.appendChild(a);a.click();URL.revokeObjectURL(a.href);a.remove();}
  async function json(url){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw new Error(`${url} ${r.status}`);return r.json();}

  typeButtons.forEach(b=>b.onclick=()=>{type=b.dataset.typeFilter;render();});controlButtons.forEach(b=>b.onclick=()=>{view=b.dataset.controlFilter;render();});search?.addEventListener('input',render);reset?.addEventListener('click',()=>{type=view='ALL';if(search)search.value='';history.replaceState(null,'',location.pathname);render();search?.focus();});exp?.addEventListener('click',csv);window.addEventListener('hashchange',highlight);

  (async()=>{
    status.textContent=c.loading;const params=new URLSearchParams(location.search),pt=String(params.get('type')||'').toUpperCase(),pv=String(params.get('view')||'').toUpperCase();if(validTypes.has(pt))type=pt;if(validViews.has(pv))view=pv;if(search)search.value=params.get('q')||'';
    try{const indexURL=new URL(root.dataset.indexUrl,document.baseURI),index=await json(indexURL),parts=await Promise.all((index.parts||[]).map(p=>json(new URL(p.path,indexURL))));if(root.dataset.actionUrl){try{matrix=await json(new URL(root.dataset.actionUrl,document.baseURI));}catch(e){matrixWarning=true;console.error('Matter action matrix load failed',e);}}indexActions();records=parts.flatMap(p=>p.records||[]).map(r=>({...r,_search:''}));records=records.map(r=>({...r,_search:searchText(r)})).sort((a,b)=>a.type.localeCompare(b.type)||a.name.localeCompare(b.name,root.dataset.lang,{sensitivity:'base'}));const issues=check(index,parts);stats();controlPanel(index,issues);render();}catch(e){console.error('Matter identity registry load failed',e);status.textContent=c.fail;status.classList.add('id-error');body.replaceChildren();if(integrity){integrity.textContent=c.fail;integrity.classList.add('is-warning');}}
  })();
})();

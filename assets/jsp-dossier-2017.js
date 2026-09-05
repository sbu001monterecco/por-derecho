(() => {
 'use strict';
 const root=document.querySelector('.jsp-dossier'); if(!root)return;
 const en=document.documentElement.lang==='en';
 const prefix=new URL('data/',document.currentScript.src);
 const tableHost=document.getElementById('canonical-records');
 const sourceHost=document.getElementById('source-records');
 const status=document.getElementById('registry-status');
 const el=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
 const get=async(path)=>{const response=await fetch(new URL(path,prefix),{credentials:'same-origin'});if(!response.ok)throw new Error(`${path}: HTTP ${response.status}`);return response.json();};
 const link=(href,text)=>{const a=el('a',text);a.href=href;return a;};
 const makeTable=(headings)=>{const wrap=el('div');wrap.className='scroll';const table=el('table');const thead=el('thead');const row=el('tr');headings.forEach(h=>row.append(el('th',h)));thead.append(row);table.append(thead);const body=el('tbody');table.append(body);wrap.append(table);return{wrap,body};};
 (async()=>{
  const data=await get('jsp-2017-source-relationship-register.json');
  const parts=await Promise.all(data.registry_parts.map(get));
  const records=parts.flatMap(p=>p.records);
  if(new Set(records.map(r=>r.id)).size!==records.length)throw new Error('Duplicate dossier identity');
  tableHost.replaceChildren();
  const t=makeTable(en?['Identity / canonical ID','Identity status','Source and role boundary']:['Identidad / ID canónico','Estado de identidad','Fuente y límite de capacidad']);
  records.forEach(r=>{const tr=el('tr');tr.id=r.id;const name=el('td');name.append(el('strong',r.name+(r.identity_resolution==='CARET_CONFIRMED'?'^':'')),el('br'),el('code',r.id));const state=el('td');const badge=el('span',r.identity_resolution==='CARET_CONFIRMED'?(en?'Identity confirmed':'Identidad confirmada'):(en?'Identity / docket reconciliation pending':'Identidad / expediente por conciliar'));badge.className='registry-state';state.append(badge);const detail=el('td');detail.append(el('p',(r.identity_sources||[]).join(' · ')));detail.append(el('p',r.capacity_boundary||''));tr.append(name,state,detail);t.body.append(tr);});
  tableHost.append(t.wrap);
  const reuse=makeTable(en?['Existing identity reused','Canonical ID']:['Identidad existente reutilizada','ID canónico']);
  data.existing_id_reuse.forEach(r=>{const tr=el('tr');tr.append(el('td',r.name),el('td',r.id));reuse.body.append(tr);});
  tableHost.append(el('h3',en?'Existing records reused—not duplicated':'Registros existentes reutilizados, no duplicados'),reuse.wrap);
  const confirmed=records.filter(r=>r.identity_resolution==='CARET_CONFIRMED').length;
  status.textContent=en?`${records.length} new scoped records; ${confirmed} identity-confirmed; ${records.length-confirmed} pending; ${data.existing_id_reuse.length} existing IDs reused. This is not a whole-perimeter completion certificate.`:`${records.length} registros nuevos del alcance; ${confirmed} identidades confirmadas; ${records.length-confirmed} pendientes; ${data.existing_id_reuse.length} ID existentes reutilizados. No certifica el cierre de todo el perímetro.`;
  sourceHost.replaceChildren();
  data.sources.forEach(s=>{const p=el('p');p.id=s.id;p.append(el('strong',`${s.id} · `),link(s.url,s.locator));p.append(el('br'),el('span',`${s.type} — ${s.limit}`));if(s.pdf_url)p.append(el('br'),link(s.pdf_url,en?'Official original PDF':'PDF original oficial'));sourceHost.append(p);});
  const notes=document.getElementById('open-dispositions');
  if(notes){notes.replaceChildren();data.open_dispositions.forEach(g=>{const p=el('p');p.append(el('strong',g.subject+': '),el('span',g.state+' — '+g.next_source));notes.append(p);});}
  const target=decodeURIComponent(location.hash.slice(1));if(target&&/^PD-SP-/.test(target)){const n=document.getElementById(target);if(n)n.scrollIntoView();}
 })().catch(error=>{status.textContent=en?'The registry table could not be loaded. The static dossier remains readable; use the linked canonical JSON records.':'No se ha podido cargar la tabla registral. El dossier estático sigue disponible; consulte los JSON canónicos enlazados.';status.setAttribute('role','alert');console.error('JSP dossier:',error.message);});
})();

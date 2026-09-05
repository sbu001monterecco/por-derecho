(() => {
'use strict';
const root=document.querySelector('.jsp-dossier');if(!root)return;
const en=document.documentElement.lang==='en';
const prefix=new URL('data/',document.currentScript.src);
const tableHost=document.getElementById('canonical-records'),sourceHost=document.getElementById('source-records'),status=document.getElementById('registry-status');
const el=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
const get=async path=>{const r=await fetch(new URL(path,prefix),{credentials:'same-origin'});if(!r.ok)throw new Error(`${path}: HTTP ${r.status}`);return r.json();};
const link=(href,text)=>{const a=el('a',text);a.href=href;return a;};
const makeTable=headings=>{const wrap=el('div');wrap.className='scroll';const table=el('table'),thead=el('thead'),row=el('tr');headings.forEach(h=>row.append(el('th',h)));thead.append(row);table.append(thead);const body=el('tbody');table.append(body);wrap.append(table);return{wrap,body};};
(async()=>{
 const [data,supplement]=await Promise.all([get('jsp-2017-source-relationship-register.json'),get('jsp-canonical-supplement-20260905.json')]);
 const parts=await Promise.all(supplement.registry_parts.map(get));
 const records=parts.flatMap(p=>p.records);
 const reused=supplement.reused_records;
 const allIds=[...records.map(r=>r.id),...reused.map(r=>r.id)];
 if(new Set(allIds).size!==allIds.length)throw new Error('Duplicate dossier identity');
 if(records.length!==supplement.expected_new_records||reused.length!==supplement.expected_reused_records)throw new Error('Dossier denominator mismatch');
 tableHost.replaceChildren();
 const t=makeTable(en?['Identity / canonical ID','Identity status','Source and role boundary']:['Identidad / ID canónico','Estado de identidad','Fuente y límite de capacidad']);
 records.forEach(r=>{const tr=el('tr');tr.id=r.id;const name=el('td');name.append(el('strong',r.name+(r.identity_resolution==='CARET_CONFIRMED'?'^':'')),el('br'),el('code',r.id));const state=el('td'),badge=el('span',r.identity_resolution==='CARET_CONFIRMED'?(en?'Identity confirmed':'Identidad confirmada'):(en?'Identity, mandate or docket reconciliation pending':'Identidad, mandato o expediente por conciliar'));badge.className='registry-state';state.append(badge);const detail=el('td');detail.append(el('p',(r.identity_sources||[]).join(' · ')),el('p',r.capacity_boundary||''));tr.append(name,state,detail);t.body.append(tr);});
 tableHost.append(t.wrap);
 const reuse=makeTable(en?['Existing identity reused','Canonical ID']:['Identidad existente reutilizada','ID canónico']);
 reused.forEach(r=>{const tr=el('tr');tr.id=r.id;tr.append(el('td',r.name),el('td',r.id));reuse.body.append(tr);});
 tableHost.append(el('h3',en?'Existing records reused—not duplicated':'Registros existentes reutilizados, no duplicados'),reuse.wrap);
 const confirmed=records.filter(r=>r.identity_resolution==='CARET_CONFIRMED').length;
 status.textContent=en?`${records.length} new source-bounded records: ${confirmed} identity-confirmed and ${records.length-confirmed} pending; ${reused.length} existing IDs reused. ${allIds.length} dossier identities. This does not certify all identities, roles, transactions or the whole perimeter.`:`${records.length} registros nuevos delimitados por fuentes: ${confirmed} identidades confirmadas y ${records.length-confirmed} pendientes; ${reused.length} ID existentes reutilizados. ${allIds.length} identidades del dossier. No certifica todas las identidades, capacidades, operaciones ni todo el perímetro.`;
 sourceHost.replaceChildren();
 const sourceRows=[...data.sources,...supplement.additional_sources];
 sourceRows.forEach(s=>{const p=el('p');p.id=s.id;p.append(el('strong',`${s.id} · `),link(s.url,s.locator),el('br'),el('span',`${s.type} — ${s.limit}`));if(s.pdf_url)p.append(el('br'),link(s.pdf_url,en?'Official original PDF':'PDF original oficial'));sourceHost.append(p);});
 sourceHost.append(el('p',en?'Extended execution and source-level qualifications:':'Ejecución ampliada y niveles de fuente:'),link('../../archive/JSP_CANONICAL_DOSSIER_SOURCE_CONTROL_05SEP2026.md',en?'Read the executed research supplement':'Leer el suplemento de investigación ejecutada'));
 const notes=document.getElementById('open-dispositions');
 if(notes){notes.replaceChildren();data.open_dispositions.forEach(g=>{const p=el('p');p.append(el('strong',g.subject+': '),el('span',g.state+' — '+g.next_source));notes.append(p);});notes.append(el('h3',en?'Prioritised production gaps':'Lagunas documentales priorizadas'));supplement.gaps.forEach(g=>{const p=el('p');p.id=g.id;p.append(el('strong',`${g.id} · ${g.priority} · `),el('span',en?g.en:g.es));notes.append(p);});}
 const target=decodeURIComponent(location.hash.slice(1));const resolved=supplement.retired_candidate_ids[target]||target;if(resolved&&/^PD-SP-/.test(resolved)){const n=document.getElementById(resolved);if(n)n.scrollIntoView();}
})().catch(error=>{status.textContent=en?'The registry table could not be loaded. The static dossier remains readable; use the linked canonical JSON records.':'No se ha podido cargar la tabla registral. El dossier estático sigue disponible; consulte los JSON canónicos enlazados.';status.setAttribute('role','alert');console.error('JSP dossier:',error.message);});
})();

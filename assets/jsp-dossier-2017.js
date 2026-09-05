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
 // Original-source reader is independent of the registry fetch: an unavailable
 // JSON table must never remove the official evidence or its always-visible link.
 const notice=document.getElementById('notice');
 if(notice&&!document.getElementById('official-notice-capture')){
  const section=el('section');section.id='official-notice-capture';
  section.append(el('h2',en?'The evidence itself: complete official page':'La prueba documental: página oficial completa'));
  section.append(el('p',en?'BORME no. 152 · 10 August 2017 · printed page 8556 · BORME-C-2017-7368. Read item Five together with the introduction, dates and named administrator. The publication is an agenda supplement, not the meeting minutes.':'BORME núm. 152 · 10 agosto 2017 · página 8556 · BORME-C-2017-7368. Lea el punto Quinto junto con la introducción, las fechas y el administrador identificado. Es un complemento de convocatoria, no el acta de la junta.'));
  const quote=el('blockquote');quote.lang='es';
  quote.append(el('p','«venta del Complejo Sun Park y de la mayoría de las participaciones de Explobeach»'),el('p','«ampliando las ya dadas en pasadas Juntas Generales»'));
  section.append(quote);
  section.append(el('p',en?'These are two exact, separately marked excerpts from item Five. The complete paragraph and all other agenda items remain in the official original below. This reading panel is not a facsimile, certified copy, signature or AI-generated document.':'Son dos extractos literales separados del punto Quinto. El párrafo completo y los demás puntos se conservan en el original oficial siguiente. Este panel de lectura no es un facsímil, copia certificada, firma ni documento generado como prueba.'));
  const original='https://www.boe.es/borme/dias/2017/08/10/pdfs/BORME-C-2017-7368.pdf';
  const links=el('p');links.className='actions';
  const pdfLink=link(original,en?'Open the complete original PDF':'Abrir el PDF original completo');pdfLink.className='button';
  const htmlLink=link('https://www.boe.es/diario_borme/txt.php?id=BORME-C-2017-7368',en?'Official searchable text':'Texto oficial accesible');htmlLink.className='button';
  links.append(pdfLink,htmlLink);section.append(links);
  const frame=el('iframe');frame.id='official-notice-frame';frame.src=original+'#page=1&zoom=page-width';frame.title=en?'Complete official BORME notice, page 8556':'Anuncio BORME oficial completo, página 8556';frame.loading='lazy';frame.referrerPolicy='no-referrer';frame.style.cssText='display:block;width:100%;height:850px;max-height:85vh;min-height:420px;border:1px solid #b4c2ce;background:#fff';
  section.append(frame);
  section.append(el('p',en?'The embedded viewer loads the actual BOE-hosted PDF. Some mobile browsers or source-host restrictions may prevent inline display; the two links above remain available. A successful website load alone is not proof that a third-party PDF viewer rendered.':'El visor carga el PDF real alojado por el BOE. Algunos móviles o restricciones del servidor pueden impedir la vista incrustada; los dos enlaces anteriores siguen disponibles. Cargar esta página no demuestra por sí solo que el visor externo haya mostrado el PDF.'));
  notice.insertAdjacentElement('afterend',section);
  const actions=document.querySelector('header .actions');if(actions){const a=link('#official-notice-capture',en?'Read the evidence on this page':'Ver la prueba en esta página');a.className='button';actions.append(a);}
 }
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
  const target=decodeURIComponent(location.hash.slice(1));if(target&&(/^(PD-SP-|official-notice-capture)/.test(target))){const n=document.getElementById(target);if(n)n.scrollIntoView();}
 })().catch(error=>{status.textContent=en?'The registry table could not be loaded. The static dossier remains readable; use the linked canonical JSON records.':'No se ha podido cargar la tabla registral. El dossier estático sigue disponible; consulte los JSON canónicos enlazados.';status.setAttribute('role','alert');console.error('JSP dossier:',error.message);});
})();

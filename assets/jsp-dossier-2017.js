(() => {
 'use strict';
 const root=document.querySelector('.jsp-dossier'); if(!root)return;
 const en=document.documentElement.lang==='en';
 const scriptURL=document.currentScript.src;
 const prefix=new URL('data/',scriptURL);
 const evidenceURL=name=>new URL('evidence/jsp-2017/'+name,scriptURL).href;
 const tableHost=document.getElementById('canonical-records');
 const sourceHost=document.getElementById('source-records');
 const status=document.getElementById('registry-status');
 const el=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
 const get=async(path)=>{const response=await fetch(new URL(path,prefix),{credentials:'same-origin'});if(!response.ok)throw new Error(`${path}: HTTP ${response.status}`);return response.json();};
 const link=(href,text)=>{const a=el('a',text);a.href=href;return a;};
 const makeTable=(headings)=>{const wrap=el('div');wrap.className='scroll';const table=el('table');const thead=el('thead');const row=el('tr');headings.forEach(h=>row.append(el('th',h)));thead.append(row);table.append(thead);const body=el('tbody');table.append(body);wrap.append(table);return{wrap,body};};
 // Evidence is independent of the registry fetch. Its original links remain
 // available even when a JSON table or an embedded PDF viewer cannot load.
 const notice=document.getElementById('notice');
 if(notice&&!document.getElementById('official-notice-capture')){
  const section=el('section');section.id='official-notice-capture';
  section.append(el('h2',en?'The evidence itself: complete official page':'La prueba documental: página oficial completa'));
  section.append(el('p',en?'BORME no. 152 · 10 August 2017 · printed page 8556 · BORME-C-2017-7368. Read item Five together with the introduction, dates and named administrator. The publication is an agenda supplement, not the meeting minutes.':'BORME núm. 152 · 10 agosto 2017 · página 8556 · BORME-C-2017-7368. Lea el punto Quinto junto con la introducción, las fechas y el administrador identificado. Es un complemento de convocatoria, no el acta de la junta.'));
  const quote=el('blockquote');quote.lang='es';
  quote.append(el('p','«venta del Complejo Sun Park y de la mayoría de las participaciones de Explobeach»'),el('p','«ampliando las ya dadas en pasadas Juntas Generales»'));
  section.append(quote);
  section.append(el('p',en?'These are two exact, separately marked excerpts from item Five. The complete paragraph and other agenda items remain in the original. The images below are unannotated pixel renderings of that official PDF, not AI-generated evidence, a recreated notice or a certified copy.':'Son dos extractos literales separados del punto Quinto. El párrafo completo y los demás puntos se conservan en el original. Las imágenes siguientes son reproducciones de píxeles del PDF oficial, sin anotaciones; no son prueba generada por IA, un anuncio reconstruido ni copia certificada.'));
  const imageItems=[
   {name:'borme-c-2017-7368-item-five.webp',id:'jsp-evidence-item-five',width:1025,height:116,title:en?'Item Five — exact source crop':'Punto Quinto — recorte de la fuente',caption:en?'The complete item-five paragraph, cropped from page 8556. Open the image at full size to read it on a small screen. The full page below preserves the surrounding context.':'Párrafo completo del punto Quinto, recortado de la página 8556. Abra la imagen a tamaño completo para leerla en una pantalla pequeña. La página íntegra siguiente conserva el contexto.'},
   {name:'borme-c-2017-7368-full-page.webp',id:'jsp-evidence-full-page',width:893,height:1263,title:en?'Complete official page — source-derived image':'Página oficial íntegra — imagen derivada de la fuente',caption:en?'Complete one-page notice, including the request, other agenda items, dates and named administrator. Lossless WebP encoding preserves the rendered pixels; the native PDF remains the controlling source.':'Anuncio íntegro de una página, con el requerimiento, otros puntos, fechas y administrador identificado. La codificación WebP sin pérdida conserva los píxeles renderizados; el PDF nativo sigue siendo la fuente de referencia.'}
  ];
  imageItems.forEach(item=>{
   const figure=el('figure');figure.style.cssText='margin:24px 0;max-width:100%';figure.id=item.id;
   figure.append(el('h3',item.title));
   const a=link(evidenceURL(item.name),'');a.target='_blank';a.rel='noopener';
   const img=el('img');img.src=evidenceURL(item.name);img.alt=item.title;img.width=item.width;img.height=item.height;img.decoding='async';img.loading='eager';img.dataset.evidenceSource='JSP-2017-S01';img.style.cssText='display:block;width:100%;height:auto;border:1px solid #b4c2ce;background:white';a.append(img);figure.append(a,el('figcaption',item.caption));section.append(figure);
  });
  const original='https://www.boe.es/borme/dias/2017/08/10/pdfs/BORME-C-2017-7368.pdf';
  const links=el('p');links.className='actions';
  [[evidenceURL('BORME-C-2017-7368.pdf'),en?'Preserved native PDF (same bytes)':'PDF nativo conservado (mismos bytes)'],[original,en?'Original PDF at the BOE':'PDF original en el BOE'],['https://www.boe.es/diario_borme/txt.php?id=BORME-C-2017-7368',en?'Official searchable text':'Texto oficial accesible'],[new URL('jsp-official-images-provenance-20260905.json',prefix).href,en?'Image provenance and checksums':'Procedencia de imágenes y huellas']].forEach(([href,label])=>{const a=link(href,label);a.className='button';links.append(a);});
  section.append(links);
  const frame=el('iframe');frame.id='official-notice-frame';frame.src=evidenceURL('BORME-C-2017-7368.pdf')+'#page=1&zoom=page-width';frame.title=en?'Preserved official BORME PDF, page 8556':'PDF BORME oficial conservado, página 8556';frame.loading='lazy';frame.referrerPolicy='no-referrer';frame.style.cssText='display:block;width:100%;height:850px;max-height:85vh;min-height:420px;border:1px solid #b4c2ce;background:#fff';section.append(frame);
  section.append(el('p',en?'The same-host PDF is a byte-identical preserved copy of the BOE download, not a new certificate. A browser may not display PDFs inline; the genuine images and direct original links remain available. This notice proves the published request, not that the meeting occurred, the sale terms, a completed title chain or criminal responsibility.':'El PDF del mismo servidor es una copia conservada idéntica en bytes a la descarga del BOE, no una nueva certificación. Un navegador puede no mostrar PDF incrustados; las imágenes auténticas y los enlaces al original siguen disponibles. El anuncio acredita el requerimiento publicado, no la celebración de la junta, las condiciones de venta, una cadena dominical completada o responsabilidad penal.'));
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
  const target=decodeURIComponent(location.hash.slice(1));if(target&&(/^(PD-SP-|official-notice-capture|jsp-evidence-)/.test(target))){const n=document.getElementById(target);if(n)n.scrollIntoView();}
 })().catch(error=>{status.textContent=en?'The registry table could not be loaded. The static dossier remains readable; use the linked canonical JSON records.':'No se ha podido cargar la tabla registral. El dossier estático sigue disponible; consulte los JSON canónicos enlazados.';status.setAttribute('role','alert');console.error('JSP dossier:',error.message);});
})();

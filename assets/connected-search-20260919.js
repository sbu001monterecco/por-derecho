(()=>{
'use strict';
const d=document;
const isEs=/\/es\//.test(location.pathname);
const text={
  title:isEs?'Escaneo profundo de texto y conexiones':'Deep text + connections scan',
  intro:isEs?'Opcional: lee únicamente las páginas actualmente desplegadas en este GitHub Pages y busca dentro de su texto visible. También muestra enlaces internos salientes. No consulta GitLab ni fuentes privadas.':'Optional: reads only pages currently deployed on this GitHub Pages site and searches their visible text. It also reports outgoing same-project links. It does not query GitLab or private sources.',
  start:isEs?'Escanear páginas desplegadas':'Scan deployed pages',
  cancel:isEs?'Cancelar':'Cancel',
  need:isEs?'Escriba al menos 2 caracteres antes del escaneo profundo.':'Enter at least 2 characters before deep scan.',
  scanning:(done,total)=>isEs?`Escaneando ${done}/${total} rutas…`:`Scanning ${done}/${total} routes…`,
  done:(matches,total)=>isEs?`Escaneo terminado: ${matches} coincidencias en ${total} rutas legibles.`:`Scan complete: ${matches} matches across ${total} readable routes.`,
  stopped:isEs?'Escaneo cancelado.':'Scan cancelled.',
  links:isEs?'Conexiones internas':'Internal connections',
  none:isEs?'Sin coincidencias textuales en las páginas leídas.':'No text matches in the pages read.',
  boundary:isEs?'El escaneo es una ayuda de descubrimiento. Una coincidencia o enlace no prueba una relación jurídica, conocimiento, control, causalidad ni responsabilidad.':'This scan is a discovery aid. A text match or link does not prove a legal relationship, knowledge, control, causation or responsibility.'
};
const norm=s=>(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/\s+/g,' ').trim();
const esc=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const projectMarker='/por-derecho/';
let controller=null;
const cache=new Map();
const sameProjectLinks=(doc,base)=>{
  const out=new Set();
  for(const a of doc.querySelectorAll('a[href]')){
    try{
      const u=new URL(a.getAttribute('href'),base);
      if(u.origin!==location.origin||!u.pathname.includes(projectMarker))continue;
      const path=u.pathname.slice(u.pathname.indexOf(projectMarker)+projectMarker.length).replace(/^\/+|\/+$/g,'')+'/';
      if(path&&!path.startsWith('assets/')&&!path.startsWith('archive/'))out.add(path);
    }catch{}
  }
  return [...out];
};
async function readEntry(entry,signal){
  if(cache.has(entry.path))return cache.get(entry.path);
  const root=new URL('../../',location.href);
  const url=new URL(entry.path,root);
  const r=await fetch(url,{signal,credentials:'same-origin'});
  if(!r.ok||!/text\/html/i.test(r.headers.get('content-type')||'text/html'))throw new Error('not-html');
  const html=await r.text();
  const doc=new DOMParser().parseFromString(html,'text/html');
  doc.querySelectorAll('script,style,noscript,svg').forEach(n=>n.remove());
  const body=doc.querySelector('main')||doc.body;
  const value={entry,text:norm(body?.textContent||''),links:sameProjectLinks(doc,url)};
  cache.set(entry.path,value);
  return value;
}
function score(textValue,q){
  const phrase=norm(q); const tokens=phrase.split(' ').filter(Boolean);
  if(!phrase||!tokens.length)return 0;
  let s=0,from=0;
  while((from=textValue.indexOf(phrase,from))>=0){s+=40;from+=Math.max(1,phrase.length);}
  for(const t of tokens){let i=0,c=0;while((i=textValue.indexOf(t,i))>=0&&c<20){c++;i+=Math.max(1,t.length);}s+=c*4;}
  return s;
}
function install(){
  const form=d.getElementById('psr-search-form');
  const input=d.getElementById('psr-search-input');
  if(!form||!input||d.getElementById('psr-deep-scan'))return;
  const wrap=d.createElement('section');
  wrap.id='psr-deep-scan';
  wrap.innerHTML=`<div class="psr-deep-box"><h2>${text.title}</h2><p>${text.intro}</p><div class="psr-deep-actions"><button type="button" data-deep-start>${text.start}</button><button type="button" data-deep-cancel hidden>${text.cancel}</button></div><p data-deep-progress aria-live="polite"></p><div data-deep-results></div><p class="psr-deep-boundary"><strong>${isEs?'Límite':'Boundary'}.</strong> ${text.boundary}</p></div>`;
  form.closest('.shell')?.append(wrap);
  const style=d.createElement('style');
  style.textContent='.psr-deep-box{margin-top:2rem;border:1px solid rgba(19,37,45,.18);border-radius:14px;padding:1rem;background:#fff}.psr-deep-actions{display:flex;gap:.6rem;flex-wrap:wrap}.psr-deep-result{border-top:1px solid rgba(19,37,45,.14);padding:.85rem 0}.psr-deep-result h3{margin:.15rem 0}.psr-deep-meta{font-size:.86rem;opacity:.8}.psr-deep-links{font-size:.9rem}.psr-deep-links a{margin-right:.55rem}.psr-deep-boundary{border-left:4px solid #8c6b2f;padding-left:.8rem}.psr-deep-box button{padding:.65rem .9rem;font-weight:700}';
  d.head.append(style);
  const start=wrap.querySelector('[data-deep-start]'),cancel=wrap.querySelector('[data-deep-cancel]'),progress=wrap.querySelector('[data-deep-progress]'),results=wrap.querySelector('[data-deep-results]');
  start.addEventListener('click',async()=>{
    const q=input.value.trim();
    if(q.length<2){progress.textContent=text.need;return;}
    start.disabled=true;cancel.hidden=false;results.innerHTML='';controller=new AbortController();
    try{
      const api=window.PorDerechoUnitaryShell;
      if(!api?.loadEntries)throw new Error('search-api-unavailable');
      const raw=await api.loadEntries();
      const map=new Map();
      raw.forEach(e=>{if(e?.path&&!map.has(e.path))map.set(e.path,e);});
      const entries=[...map.values()];
      let done=0,readable=0; const found=[]; let cursor=0;
      const worker=async()=>{
        while(cursor<entries.length&&!controller.signal.aborted){
          const idx=cursor++,entry=entries[idx];
          try{
            const page=await readEntry(entry,controller.signal);readable++;
            const s=score(page.text,q);
            if(s>0)found.push({...page,score:s});
          }catch(e){if(e?.name==='AbortError')return;}
          done++; if(done%10===0||done===entries.length)progress.textContent=text.scanning(done,entries.length);
        }
      };
      await Promise.all(Array.from({length:8},worker));
      if(controller.signal.aborted){progress.textContent=text.stopped;return;}
      found.sort((a,b)=>b.score-a.score||a.entry.title.localeCompare(b.entry.title));
      const rows=found.slice(0,80);
      progress.textContent=text.done(found.length,readable);
      results.innerHTML=rows.length?rows.map(x=>{
        const root=new URL('../../',location.href); const href=new URL(x.entry.path,root).href;
        const links=x.links.slice(0,8).map(p=>`<a href="${new URL(p,root).href}">${esc(p)}</a>`).join('');
        return `<article class="psr-deep-result"><h3><a href="${href}">${esc(x.entry.title||x.entry.path)}</a></h3><div class="psr-deep-meta">${esc(x.entry.path)} · score ${x.score} · ${x.links.length} ${text.links.toLowerCase()}</div>${links?`<div class="psr-deep-links"><strong>${text.links}:</strong> ${links}</div>`:''}</article>`;
      }).join(''):`<p>${text.none}</p>`;
    }catch(e){if(e?.name!=='AbortError')progress.textContent=String(e?.message||e);}
    finally{start.disabled=false;cancel.hidden=true;controller=null;}
  });
  cancel.addEventListener('click',()=>controller?.abort());
}
if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',()=>setTimeout(install,0),{once:true});else setTimeout(install,0);
})();
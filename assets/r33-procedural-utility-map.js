(()=>{'use strict';
const rootFromPath=()=>{const p=location.pathname;const m=p.match(/^(.*?)(?:\/en\/|\/es\/)/);return (m?m[1]:'').replace(/\/$/,'');};
const abs=(route)=>rootFromPath()+route;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pick=(v,lang)=>v&&typeof v==='object'&&!Array.isArray(v)?(v[lang]??v.en??''):v;
function render(el,d){
 const lang=(el.dataset.lang||document.documentElement.lang||'en').toLowerCase().startsWith('es')?'es':'en';
 const laneById=Object.fromEntries(d.lanes.map(x=>[x.id,x]));
 const title=lang==='es'?'R33 como mapa de utilidad procesal':'R33 as a procedural-utility map';
 const sub=lang==='es'?'Hecho → prueba → actor/capacidad → vía → siguiente producción':'Fact → evidence → actor/capacity → lane → next production';
 const why=lang==='es'?'Por qué importa':'Why it matters';
 const next=lang==='es'?'Siguiente prueba que cierra el salto':'Next proof that closes the gap';
 const gatewayTitle=lang==='es'?'Abrir expedientes conectados':'Open connected case files';
 const lanes=d.lanes.map(l=>`<article class="r33-lane ${esc(l.tone)}"><div class="role">${esc(pick(l.role,lang))}</div><h3>${esc(pick(l.label,lang))}</h3><p>${esc(pick(l.test,lang))}</p><p><a href="${esc(abs(l.routes[lang]))}">${lang==='es'?'Abrir vía':'Open lane'} →</a></p></article>`).join('');
 const issues=d.issues.map(i=>{
   const chips=i.lanes.map(id=>{const l=laneById[id];return `<a class="r33-chip" data-lane="${esc(id)}" href="${esc(abs(l.routes[lang]))}">${esc(pick(l.label,lang))}</a>`}).join('');
   const extra=(i.extra_routes?.[lang]||[]).map(r=>`<a class="r33-chip" href="${esc(abs(r))}">${lang==='es'?'Fuente relacionada':'Related source'} ↗</a>`).join('');
   return `<article class="r33-issue" id="r33-utility-${esc(i.id)}"><div class="r33-issue-top"><h4>${esc(pick(i.label,lang))}</h4><span class="r33-pages">${lang==='es'?'págs.':'pp.'} ${esc(i.pages)} · ${esc(i.count)} ${lang==='es'?'unidades':'units'}</span></div><p><strong>${why}.</strong> ${esc(pick(i.why,lang))}</p><div class="r33-lane-tags">${chips}${extra}</div><div class="r33-proof"><strong>${next}</strong>${esc(pick(i.next,lang))}</div></article>`;
 }).join('');
 const gateways=d.gateways[lang].map(g=>`<a href="${esc(abs(g.route))}">${esc(g.label)} →</a>`).join('');
 el.innerHTML=`<div class="r33-util-head"><div class="r33-util-spine"><div class="eyebrow">${esc(d.document.id)} · ${esc(d.control)}</div><h2>${title}</h2><p>${sub}</p><div class="r33-util-equation"><span>R33</span><b>→</b><span>${d.document.pages} ${lang==='es'?'páginas':'pages'}</span><b>→</b><span>${d.document.statement_propositions} ${lang==='es'?'proposiciones':'propositions'}</span><b>→</b><span>${lang==='es'?'uso procesal separado':'separate procedural use'}</span></div></div><div class="r33-util-boundary"><strong>${esc(pick(d.boundary,lang))}</strong></div></div><div class="r33-util-lanes">${lanes}</div><div class="r33-util-section-title"><h3>${lang==='es'?'Siete puertas probatorias':'Seven evidential gateways'}</h3><p>${lang==='es'?'No son siete cargos ni siete conclusiones. Son siete rutas de prueba.':'Not seven charges or conclusions. Seven routes for proof.'}</p></div><div class="r33-issues">${issues}</div><h3 style="margin:1.15rem 0 .35rem">${gatewayTitle}</h3><div class="r33-util-gateways">${gateways}</div><p class="r33-util-note">${lang==='es'?'Los enlaces cruzan evidencia; no fusionan procedimientos. La responsabilidad sigue siendo individual y fuente-específica.':'Links connect evidence; they do not merge proceedings. Responsibility remains individual and source-specific.'}</p>`;
}
async function init(){
 for(const el of document.querySelectorAll('[data-r33-procedural-utility]')){
   const src=el.dataset.src||'../../assets/data/r33-procedural-utility-map-v1.json';
   try{const r=await fetch(src,{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status);render(el,await r.json());}
   catch(e){el.innerHTML='<div class="r33-util-error">'+((el.dataset.lang||'en').startsWith('es')?'Mapa procesal no disponible en este momento.':'Procedural map unavailable at this moment.')+'</div>';}
 }
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();

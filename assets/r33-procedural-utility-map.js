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
// PD-R33-SOURCE-CORRECTIONS-20261023-01: additive reader layer; source PDFs remain untouched.
function renderCorrection(){
 if(!document.querySelector('[data-r33-procedural-utility]')||document.getElementById('r33-source-corrections-20261023'))return;
 const es=document.documentElement.lang.toLowerCase().startsWith('es');
 const copy=es?{
 title:'R33: correcciones de fuente y alcance · 23 octubre 2026',
 intro:'Actualización de lectura, no nueva ejecución de la Máquina de Verdad ni resolución judicial. Se mantienen las alegaciones expresas, la prueba contraria y los documentos originales.',
 points:[
 ['Fecha corregida · AC-CLM-003','El Auto citado en R33, págs. 17–18, es de 8 de febrero de 2018 (P08); el 15 de febrero corresponde a la petición separada del AC (P09). La petición no acredita por sí sola que se concedieran intereses. Se conserva el carácter adverso del Auto para la tesis del crédito litigioso.'],
 ['Página 5 · clasificación analítica vigente','La revisión de fuentes de 25 de septiembre califica la generalización sobre la salida de letrados como INFERENCIA ENGAÑOSA / GENERALIZACIÓN CAUSAL NO SUSTENTADA. Es una clasificación del proyecto, no un fallo judicial. La renuncia y disculpa auténticas de Joaquín se conservan; no explican por sí solas todos los cambios de defensa ni prueban que todos fueran causados por el AC.'],
 ['Contexto y aviso','Las capturas de las págs. 3–4 contienen tanto acusaciones como límites expresos de prueba. El correo de 29 de abril de 2016, reproducido en pág. 20, contiene agradecimiento por colaboración y aviso de una controversia sobre cuotas y contabilidad. Ninguno de esos elementos debe eliminar al otro; el aviso no acredita la verdad de cada afirmación.'],
 ['Cuentas, autoridad y derechos separados','La entrega de material contable no acredita todos los libros y soportes exigibles; una carencia concreta tampoco demuestra ausencia total de colaboración. Deben cotejarse fechas, documentos, actos, facultades, resoluciones adversas y explicaciones lícitas. La masa de LPB no absorbe los derechos independientes de Gil Marer, AWESWELL LIMITED ni de otras personas o entidades.'],
 ['Cifras de la pasada registrada','276 proposiciones, 482 registros y 179 proposiciones marcadas corresponden a la pasada registrada de 25 de septiembre de 2026: 64,9 % es carga de revisión, no tasa de mentira. La revisión posterior conserva cero conclusiones firmadas de falsedad literal y cero de falsedad consciente. No se afirma una nueva ejecución completa, trazado monetario concluido ni autenticación judicial.'],
 ['Audiencia Provincial','Las afirmaciones de R33 se atribuyen al AC, no a los magistrados que conocen del recurso. Esta corrección no formula acusación contra ellos ni certifica el estado actual de los recursos.']]
 }:{
 title:'R33: source and scope corrections · 23 October 2026',
 intro:'Reader update, not a new Truth Machine run or judicial determination. Express allegations, contrary evidence and original documents remain preserved.',
 points:[
 ['Corrected date · AC-CLM-003','The order cited at R33 pp.17–18 is dated 8 February 2018 (P08); 15 February identifies the separate AC petition (P09). The petition does not itself establish an award of interest. The order remains adverse evidence for the litigated-credit argument.'],
 ['Page 5 · current analytical classification','The 25 September source review classifies the inference about successive lawyers leaving as MISLEADING INFERENCE / UNSUPPORTED CAUSAL GENERALISATION. This is the project’s classification, not a judicial finding. Joaquín’s authentic withdrawal and apology remain preserved; they do not explain every change of counsel or prove that all departures were caused by the AC.'],
 ['Context and notice','The screenshots at pp.3–4 contain both allegations and express proof limitations. The 29 April 2016 email reproduced at p.20 contains thanks for cooperation and notice of a dispute about fees and accounts. Neither element should erase the other; notice does not prove every assertion true.'],
 ['Accounts, authority and separate rights','Delivery of accounting material does not establish completeness of statutory books and supporting records; a specific missing item does not establish total non-cooperation. Dates, documents, acts, powers, adverse rulings and lawful explanations require comparison. LPB’s estate does not absorb the independent rights of Gil Marer, AWESWELL LIMITED or other persons and entities.'],
 ['Recorded run figures','276 propositions, 482 records and 179 marked propositions refer to the recorded 25 September 2026 run: 64.9% is review load, not a lie rate. The subsequent source review retains zero signed-off literal-falsehood and zero knowingly-false determinations. No fresh complete run, completed money trace or judicial authentication is claimed.'],
 ['Audiencia Provincial','R33’s assertions are attributed to the AC, not the appellate judges. This correction makes no accusation against them and does not certify the current status of the appeals.']]
 };
 const section=document.createElement('section');section.id='r33-source-corrections-20261023';section.className='section alt';
 section.innerHTML=`<div class="shell"><div class="sourcebox"><p class="eyebrow">PD-R33-SOURCE-CORRECTIONS-20261023-01</p><h2>${esc(copy.title)}</h2><p>${esc(copy.intro)}</p>${copy.points.map(([h,p])=>`<h3>${esc(h)}</h3><p>${esc(p)}</p>`).join('')}<p><a href="${esc(abs('/ops/continuity/R33_SOURCE_CORRECTIONS_20261023.md'))}">${es?'Control de corrección y fuentes':'Correction control and sources'}</a> · <a href="${esc(abs('/ops/continuity/R33_METHOD_STACK_SOURCE_REVIEW_20260925.md'))}">${es?'Revisión de fuentes de 25 septiembre':'25 September source review'}</a></p></div></div>`;
 const hero=document.querySelector('main .hero');if(hero)hero.after(section);else document.querySelector('[data-r33-procedural-utility]').before(section);
 const historical=document.querySelector('#maquina-verdad-visual .notice strong, #truth-machine-visual .notice strong');
 if(historical)historical.textContent=es?'Pasada registrada el 25 de septiembre de 2026.':'Run recorded on 25 September 2026.';
}

async function init(){
 renderCorrection();
 for(const el of document.querySelectorAll('[data-r33-procedural-utility]')){
   const src=el.dataset.src||'../../assets/data/r33-procedural-utility-map-v1.json';
   try{const r=await fetch(src,{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status);render(el,await r.json());}
   catch(e){el.innerHTML='<div class="r33-util-error">'+((el.dataset.lang||'en').startsWith('es')?'Mapa procesal no disponible en este momento.':'Procedural map unavailable at this moment.')+'</div>';}
 }
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();

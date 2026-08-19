
(()=>{
'use strict';
const body=document.body;
const lang=document.documentElement.lang==='en'?'en':'es';
const view=body.dataset.view||'root';
const dataUrl=body.dataset.json;
const q=(s,r=document)=>r.querySelector(s);
const qa=(s,r=document)=>[...r.querySelectorAll(s)];
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const loc=v=>v&&typeof v==='object'&&!Array.isArray(v)?(v[lang]??v.es??v.en??''):v??'';
const fmtDate=v=>{
  if(!v)return lang==='es'?'No localizada':'Not located';
  if(/^\d{4}-\d{2}-\d{2}$/.test(v)){
    const [y,m,d]=v.split('-').map(Number);
    return new Intl.DateTimeFormat(lang==='es'?'es-ES':'en-GB',{day:'numeric',month:'short',year:'numeric',timeZone:'UTC'}).format(new Date(Date.UTC(y,m-1,d)));
  }
  return v;
};
const T={
 es:{
  loading:'Cargando expediente abierto…',error:'No se pudo cargar el conjunto de datos.',
  known:'Qué sabemos',unknown:'Qué no sabemos',verify:'Qué debe verificarse',decision:'Decisión humana necesaria ahora',
  options:'Opciones disponibles',rights:'Derechos activados',document:'Documento que debe producirse',next:'Qué sucede después',
  evidence:'EVIDENCIA',history:'¿CÓMO LLEGAMOS AQUÍ?',now:'AHORA',future:'¿QUÉ DEBE OCURRIR AHORA?',rightsCompetence:'DERECHOS + COMPETENCIA',
  modules:'Once módulos materiales',openMethod:'Método abierto; expediente protegido',respondent:'Posición del profesional',counter:'Mejor explicación contraria',
  strengthen:'Fortalecería la preocupación',weaken:'La debilitaría',resolve:'Podría resolverla',verifyExplanation:'Exigiría verificación',
  missing:'Documento decisivo ausente',alternative:'Resultado alternativo razonable',sources:'Fuentes',noGuilt:'Sin hallazgo de culpabilidad',
  cutoff:'Mostrar expediente hasta',current:'Corte seleccionado',allEvents:'Eventos visibles',sourceState:'Estado documental',
  fileFilter:'Expediente/asignación',statusFilter:'Estado',search:'Buscar',all:'Todos',stage:'Etapa',
  allegation:'Alegación',referenced:'Referenciado',received:'Recibido',registered:'Registrado',deduplicated:'Deduplicado',
  assigned:'Asignado',reviewed:'Revisado',transferred:'Trasladado',contradicted:'Contradicho',verified:'Verificado',
  considered:'Considerado',decisionUse:'Usado / descartado',publicLimit:'Límite público',
  selectNode:'Seleccione un nodo para abrir su puerta humana.',humanGate:'Puerta de decisión humana',owner:'Responsable',
  requirements:'Requisitos',gateOpen:'La puerta permanece abierta: ninguna rama produce efectos sin decisión humana.',
  gateReady:'Comprobaciones de demostración completas. Sigue siendo necesaria una decisión, motivación y firma humanas.',
  gateChecks:['Competencia confirmada','Fuentes identificadas','Audiencia/contradicción tratadas','Temporalidad tratada','Alternativas y razones registradas'],
  routeOptions:'Rutas posibles',noExecution:'Ensayo local: no ejecuta actuaciones ni modifica expedientes.',
  urgency:'Protección urgente',urgencyQuestion:'Pregunta distinta del fondo',currentRisk:'Riesgo actual',reliability:'Fiabilidad',
  exposure:'Exposición',irreversibility:'Irreversibilidad',competence:'Competencia',hearing:'Audiencia',proportionality:'Proporcionalidad',
  distinctRoutes:'Rutas competenciales distintas',ladder:'Escalera de proporcionalidad',
  models:'Biblioteca de modelos',selectModel:'Seleccione un modelo',draft:'BORRADOR DOCENTE — NO OFICIAL — REVISIÓN Y FIRMA HUMANAS',
  fieldLabels:{competentBody:'Órgano competente',background:'Antecedentes',question:'Pregunta',facts:'Hechos',evidenceFor:'Prueba favorable',evidenceAgainst:'Prueba contraria',respondentPosition:'Posición profesional',timing:'Temporalidad',rights:'Derechos',alternatives:'Alternativas',reasons:'Motivación',notification:'Notificación',appeal:'Recurso',humanSignature:'Firma humana'},
  placeholder:'Completar con fuentes, razones y límites del expediente verificado.',
  chapters:'Capítulos del manual',socratic:'Preguntas socráticas',hypotheticals:'Hipótesis alternativas',errors:'Errores frecuentes',
  correction:'Correcciones de transparencia',blind:'Modo ciego',blindOn:'Identidades funcionales activadas',blindOff:'Identidades visibles',
  resultCount:'resultados',invariant1:'Registrado ≠ revisado',invariant2:'Revisado ≠ verificado',invariant3:'Verificado ≠ suficiente',invariant4:'Suficiente ≠ culpabilidad'
 },
 en:{
  loading:'Loading open file…',error:'The dataset could not be loaded.',
  known:'What we know',unknown:'What we do not know',verify:'What must be verified',decision:'Human decision required now',
  options:'Available options',rights:'Rights activated',document:'Document that must be produced',next:'What happens next',
  evidence:'EVIDENCE',history:'HOW DID WE GET HERE?',now:'NOW',future:'WHAT MUST HAPPEN NEXT?',rightsCompetence:'RIGHTS + COMPETENCE',
  modules:'Eleven substantive modules',openMethod:'Open method; protected file',respondent:'Professional position',counter:'Strongest contrary explanation',
  strengthen:'Would strengthen concern',weaken:'Would weaken it',resolve:'Could resolve it',verifyExplanation:'Would require verification',
  missing:'Decisive missing document',alternative:'Reasonable alternative outcome',sources:'Sources',noGuilt:'No finding of culpability',
  cutoff:'Show the file through',current:'Selected cut-off',allEvents:'Visible events',sourceState:'Document state',
  fileFilter:'File/assignment',statusFilter:'Status',search:'Search',all:'All',stage:'Stage',
  allegation:'Allegation',referenced:'Referenced',received:'Received',registered:'Registered',deduplicated:'Deduplicated',
  assigned:'Assigned',reviewed:'Reviewed',transferred:'Transferred',contradicted:'Contradicted',verified:'Verified',
  considered:'Considered',decisionUse:'Used / discarded',publicLimit:'Public limit',
  selectNode:'Select a node to open its human gate.',humanGate:'Human decision gate',owner:'Owner',
  requirements:'Requirements',gateOpen:'The gate remains open: no branch produces effects without a human decision.',
  gateReady:'Demonstration checks completed. Human decision, reasons and signature are still required.',
  gateChecks:['Competence confirmed','Sources identified','Hearing/contradiction addressed','Timing addressed','Alternatives and reasons recorded'],
  routeOptions:'Possible routes',noExecution:'Local rehearsal: it executes nothing and changes no file.',
  urgency:'Urgent protection',urgencyQuestion:'A question separate from the merits',currentRisk:'Current risk',reliability:'Reliability',
  exposure:'Exposure',irreversibility:'Irreversibility',competence:'Competence',hearing:'Hearing',proportionality:'Proportionality',
  distinctRoutes:'Distinct competence routes',ladder:'Proportionality ladder',
  models:'Model-document library',selectModel:'Select a model',draft:'TEACHING DRAFT — NON-OFFICIAL — HUMAN REVIEW AND SIGNATURE',
  fieldLabels:{competentBody:'Competent body',background:'Background',question:'Question',facts:'Facts',evidenceFor:'Evidence supporting',evidenceAgainst:'Evidence against',respondentPosition:'Professional position',timing:'Timing',rights:'Rights',alternatives:'Alternatives',reasons:'Reasons',notification:'Notification',appeal:'Appeal',humanSignature:'Human signature'},
  placeholder:'Complete with sources, reasons and limits from the verified file.',
  chapters:'Casebook chapters',socratic:'Socratic questions',hypotheticals:'Alternative hypotheticals',errors:'Common errors',
  correction:'Transparency corrections',blind:'Blind mode',blindOn:'Functional identities enabled',blindOff:'Identities visible',
  resultCount:'results',invariant1:'Registered ≠ reviewed',invariant2:'Reviewed ≠ verified',invariant3:'Verified ≠ sufficient',invariant4:'Sufficient ≠ culpability'
 }
}[lang];

const statusClass=v=>{
 const s=String(v??'').toLowerCase();
 if(v===true||['yes','done','confirmed','official','receipt','legal-reference','official-status'].some(x=>s.includes(x)))return 'yes';
 if(v===false||s==='n/a'||s.includes('not-applicable'))return 'no';
 if(s.includes('risk')||s.includes('blocked')||s.includes('dip79'))return 'risk';
 if(s.includes('open')||s.includes('partial')||s.includes('probable')||s.includes('pending'))return 'open';
 if(s.includes('not-located')||s.includes('not-publicly')||s.includes('unknown')||s.includes('certif'))return 'unknown';
 return 'official';
};
const statusText=v=>{
 if(v===true)return lang==='es'?'Sí':'Yes';
 if(v===false)return lang==='es'?'No':'No';
 const map={
  'n/a':lang==='es'?'N/A':'N/A',
  'not-located':lang==='es'?'No localizado':'Not located',
  'not-publicly-established':lang==='es'?'No acreditado públicamente':'Not publicly established',
  'partial':lang==='es'?'Parcial':'Partial',
  'open':lang==='es'?'Pendiente':'Open',
  'probable':lang==='es'?'Probable · certificar':'Probable · certify',
  'risk':lang==='es'?'Riesgo':'Risk',
  'blocked':lang==='es'?'Bloqueado':'Blocked',
  'receipt':lang==='es'?'Acuse verificado':'Receipt verified',
  'copy-in-other-package':lang==='es'?'Copia dentro de otro paquete':'Copy in another package',
  'autonomous-receipt-not-isolated':lang==='es'?'Acuse autónomo no aislado':'Autonomous receipt not isolated',
  'dip79-only-unless-relevance-decided':lang==='es'?'Solo DIP 79 salvo decisión expresa':'DIP 79 only absent an express relevance decision',
  'not-independently-established':lang==='es'?'No establecido de forma independiente':'Not independently established',
  'blocked-pending-relevance':lang==='es'?'Bloqueado hasta decidir relevancia':'Blocked pending a relevance decision',
  'blocked-pending-assignment':lang==='es'?'Bloqueado hasta asignación':'Blocked pending assignment',
  'assignment-to-certify':lang==='es'?'Asignación por certificar':'Assignment to certify'
 };
 const k=String(v??'');
 return map[k]||k.replaceAll('-',' ');
};
const tag=(v)=>`<span class="ok-stage ${statusClass(v)}">${esc(statusText(v))}</span>`;
const list=(arr)=>`<ul>${(arr||[]).map(x=>`<li>${esc(loc(x))}</li>`).join('')}</ul>`;
const byId=(arr,id)=>arr.find(x=>x.id===id);

function setupNav(){
 const b=q('.pw-nav-toggle'),n=q('#pw-nav');
 if(b&&n)b.addEventListener('click',()=>{const on=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',String(!on));n.classList.toggle('open',!on)});
 const blind=q('#ok-blind');
 if(blind)blind.addEventListener('click',()=>{
   const on=body.classList.toggle('ok-blind');
   blind.setAttribute('aria-pressed',String(on));
   blind.textContent='◐ '+(on?T.blindOn:T.blindOff);
   qa('[data-real][data-blind]').forEach(el=>el.textContent=on?el.dataset.blind:el.dataset.real);
 });
}
function renderStatus(d){
 const el=q('[data-status-grid]');if(!el)return;
 const entries=[
  [lang==='es'?'Fase documentada':'Documented phase',lang==='es'?'Información previa abierta':'Preliminary information opened'],
  [lang==='es'?'Último acto oficial localizado':'Latest official act located','RS-002600 · '+fmtDate(d.officialStatus.outgoingRegistrationDate)],
  [lang==='es'?'Respuesta profesional pública':'Public professional response',loc(d.respondentPosition.caution)],
  [lang==='es'?'Control ordinario':'Ordinary control',fmtDate(d.officialStatus.ordinaryControlDate)]
 ];
 el.innerHTML=entries.map(([a,b])=>`<div class="ok-status"><small>${esc(a)}</small><strong>${esc(b)}</strong></div>`).join('');
}
function renderNow(d){
 const el=q('#now-junction');if(!el)return;
 el.innerHTML=`
  <article class="ok-now-card evidence"><div class="ok-arrow-label">${esc(T.evidence)}</div><h3>${esc(T.known)} / ${esc(T.unknown)}</h3><div class="pw-grid-2"><div><strong>${esc(T.known)}</strong>${list(d.now.known)}</div><div><strong>${esc(T.unknown)}</strong>${list(d.now.unknown)}</div></div></article>
  <article class="ok-now-card history"><div class="ok-arrow-label">${esc(T.history)}</div><h3>${esc(lang==='es'?'Reconstrucción inversa':'Reverse reconstruction')}</h3><p>${esc(lang==='es'?'Partir del estado presente, retroceder hasta cada acto y mostrar solo la información disponible en esa fecha.':'Start from the present state, move backward to each act and show only information available at that date.')}</p><a class="pw-button small secondary" href="${esc(body.dataset.chronology)}">${esc(lang==='es'?'Abrir cronología':'Open chronology')}</a></article>
  <div class="ok-now-centre"><div><small>DIP 80/2026</small><strong>${esc(T.now)}</strong><p>${esc(loc(d.now.humanDecision))}</p></div></div>
  <article class="ok-now-card next"><div class="ok-arrow-label">${esc(T.future)}</div><h3>${esc(T.decision)}</h3><p>${esc(loc(d.now.humanDecision))}</p><a class="pw-button small warn" href="${esc(body.dataset.tree)}">${esc(lang==='es'?'Abrir árbol':'Open tree')}</a></article>
  <article class="ok-now-card rights"><div class="ok-arrow-label">${esc(T.rightsCompetence)}</div><h3>${esc(T.rights)}</h3><p>${esc(loc(d.now.rights))}</p><p><strong>${esc(T.document)}:</strong> ${esc(loc(d.now.document))}</p></article>`;
}
function renderFirstAnswers(d){
 const el=q('#first-screen-answers');if(!el)return;
 const rows=[
  [T.known,d.now.known],[T.unknown,d.now.unknown],[T.verify,d.now.verify],
  [T.decision,[d.now.humanDecision]],[T.options,d.now.options.map(id=>byId(d.decisionNodes,id)?.title).filter(Boolean)],
  [T.rights,[d.now.rights]],[T.document,[d.now.document]],[T.next,[d.now.next]]
 ];
 el.innerHTML=rows.map((r,i)=>`<article class="ok-answer"><span>${i+1}</span><h3>${esc(r[0])}</h3>${list(r[1])}</article>`).join('');
}
function renderModules(d){
 const el=q('#module-grid');if(!el)return;
 el.innerHTML=d.modules.map((m,i)=>`
 <details class="ok-module" ${i===0?'open':''}>
  <summary><span class="ok-module-number">${m.number}</span><span class="ok-module-title"><strong>${esc(loc(m.title))}</strong><small>${esc(loc(m.status))}</small></span><span class="ok-module-caret">+</span></summary>
  <div class="ok-module-body">
   <div class="ok-module-question">${esc(loc(m.question))}</div>
   <div class="ok-view-grid">
    <div class="ok-view-cell"><strong>${esc(T.respondent)}</strong><p>${esc(loc(m.respondent))}</p></div>
    <div class="ok-view-cell"><strong>${esc(T.counter)}</strong><p>${esc(loc(m.counterEvidence))}</p></div>
    <div class="ok-view-cell strengthen"><strong>${esc(T.strengthen)}</strong><p>${esc(loc(m.changeView.strengthen))}</p></div>
    <div class="ok-view-cell weaken"><strong>${esc(T.weaken)}</strong><p>${esc(loc(m.changeView.weaken))}</p></div>
    <div class="ok-view-cell resolve"><strong>${esc(T.resolve)}</strong><p>${esc(loc(m.changeView.resolve))}</p></div>
    <div class="ok-view-cell verify"><strong>${esc(T.verifyExplanation)}</strong><p>${esc(loc(m.changeView.verify))}</p></div>
    <div class="ok-view-cell missing"><strong>${esc(T.missing)}</strong><p>${esc(loc(m.changeView.missing))}</p></div>
    <div class="ok-view-cell alternative"><strong>${esc(T.alternative)}</strong><p>${esc(loc(m.changeView.alternative))}</p></div>
   </div>
   <p><strong>${esc(T.sources)}:</strong> ${(m.sourceIds||[]).map(x=>`<span class="pw-source-tag">${esc(x)}</span>`).join(' ')}</p>
  </div>
 </details>`).join('');
}
function renderCorrections(d){
 const el=q('#corrections');if(!el)return;
 el.innerHTML=d.corrections.map(c=>`<article class="ok-correction"><strong>${esc(fmtDate(c.date))} · ${esc(T.correction)}</strong><p>${esc(loc(c.title))}</p></article>`).join('');
}

function renderChronology(d){
 const el=q('#chronology-app');if(!el)return;
 const events=[...d.events].sort((a,b)=>a.date.localeCompare(b.date));
 el.innerHTML=`<div class="ok-time-control"><strong>${esc(T.cutoff)}</strong><input id="ok-time-range" type="range" min="0" max="${events.length-1}" value="${events.length-1}" step="1"><output id="ok-time-output" class="ok-time-now"></output></div><div id="ok-event-list" class="ok-timeline"></div>`;
 const range=q('#ok-time-range',el),out=q('#ok-time-output',el),listEl=q('#ok-event-list',el);
 const draw=()=>{
   const idx=Number(range.value),cut=events[idx].date,visible=events.filter(x=>x.date<=cut).reverse();
   out.textContent=fmtDate(cut);
   listEl.innerHTML=visible.map(e=>`<article class="ok-event" data-status="${esc(e.status)}"><time>${esc(loc(e.dateLabel)||fmtDate(e.date))}</time><h3>${esc(loc(e.title))}</h3><p>${tag(e.status)} ${(e.sourceIds||[]).map(x=>`<span class="pw-source-tag">${esc(x)}</span>`).join(' ')}</p></article>`).join('');
 };
 range.addEventListener('input',draw);draw();
}

function renderTree(d){
 const tree=q('#decision-tree'),gateEl=q('#human-gate');if(!tree||!gateEl)return;
 tree.innerHTML=d.decisionNodes.map((n,i)=>`
  <article class="ok-node" data-node="${esc(n.id)}">
   <button type="button" aria-expanded="false"><span class="ok-node-index">${i+1}</span><span class="ok-node-title"><strong>${esc(loc(n.title))}</strong><small>${esc(loc(n.question))}</small></span><span>＋</span></button>
   <div class="ok-node-body"><strong>${esc(T.routeOptions)}</strong><div class="ok-options">${loc(n.options).map(x=>`<span class="ok-option">${esc(x)}</span>`).join('')}</div><p class="ok-file-lock">🔒 ${esc(T.noExecution)}</p></div>
  </article>`).join('');
 const showGate=(node)=>{
   const g=byId(d.humanGates,node.humanGateId);
   gateEl.innerHTML=`<span class="ok-gate-lock">🔒 ${esc(T.humanGate)}</span><h3>${esc(loc(g.title))}</h3><p>${esc(loc(node.question))}</p><dl><div><dt>${esc(T.owner)}</dt><dd>${esc(loc(g.owner))}</dd></div><div><dt>${esc(T.requirements)}</dt><dd>${esc(loc(g.requirements))}</dd></div></dl><div class="ok-gate-checks">${T.gateChecks.map((x,i)=>`<label><input type="checkbox" data-gate-check="${i}"><span>${esc(x)}</span></label>`).join('')}</div><div class="ok-gate-result">${esc(T.gateOpen)}</div>`;
   const checks=qa('[data-gate-check]',gateEl),result=q('.ok-gate-result',gateEl);
   checks.forEach(c=>c.addEventListener('change',()=>{result.textContent=checks.every(x=>x.checked)?T.gateReady:T.gateOpen}));
 };
 qa('.ok-node',tree).forEach((node,i)=>{
   const button=q('button',node),data=d.decisionNodes[i];
   button.addEventListener('click',()=>{
    const open=node.classList.toggle('open');button.setAttribute('aria-expanded',String(open));
    qa('.ok-node',tree).filter(x=>x!==node).forEach(x=>{x.classList.remove('open');q('button',x).setAttribute('aria-expanded','false')});
    showGate(data);
   });
 });
 gateEl.innerHTML=`<span class="ok-gate-lock">🔒 ${esc(T.humanGate)}</span><h3>${esc(T.selectNode)}</h3><p>${esc(T.noExecution)}</p>`;
}

const stageKeys=['allegation','referenced','received','registered','deduplicated','assigned','reviewed','transferred','contradicted','verified','considered','decisionUse'];
function renderEvidence(d){
 const app=q('#evidence-app');if(!app)return;
 const files=[...new Set(d.documents.map(x=>x.file).filter(Boolean))];
 app.innerHTML=`<div class="ok-invariants"><div class="ok-invariant">${esc(T.invariant1)}</div><div class="ok-invariant">${esc(T.invariant2)}</div><div class="ok-invariant">${esc(T.invariant3)}</div><div class="ok-invariant">${esc(T.invariant4)}</div></div>
 <div class="ok-evidence-controls">
  <label>${esc(T.search)}<input id="ok-ev-search" type="search"></label>
  <label>${esc(T.fileFilter)}<select id="ok-ev-file"><option value="">${esc(T.all)}</option>${files.map(x=>`<option>${esc(x)}</option>`).join('')}</select></label>
  <label>${esc(T.statusFilter)}<select id="ok-ev-status"><option value="">${esc(T.all)}</option>${stageKeys.map(k=>`<option value="${k}">${esc(T[k])}</option>`).join('')}</select></label>
  <strong id="ok-ev-count"></strong>
 </div><div class="pw-table-wrap"><table class="ok-evidence-table"><thead><tr><th>${esc(T.sources)}</th>${stageKeys.map(k=>`<th>${esc(T[k])}</th>`).join('')}<th>${esc(T.publicLimit)}</th></tr></thead><tbody id="ok-ev-body"></tbody></table></div>`;
 const search=q('#ok-ev-search'),file=q('#ok-ev-file'),status=q('#ok-ev-status'),tbody=q('#ok-ev-body'),count=q('#ok-ev-count');
 const draw=()=>{
   const needle=search.value.trim().toLowerCase(),fv=file.value,sv=status.value;
   const docs=d.documents.filter(x=>{
    const text=[x.id,loc(x.title),x.reference,x.file].join(' ').toLowerCase();
    const statusMatch=!sv||!['',false,null,undefined,'n/a','not-applicable'].includes(x.status?.[sv]);
    return(!needle||text.includes(needle))&&(!fv||x.file===fv)&&statusMatch;
   });
   count.textContent=`${docs.length} ${T.resultCount}`;
   tbody.innerHTML=docs.map(x=>`<tr><td><strong>${esc(x.id)}</strong><br>${esc(loc(x.title))}<br><small>${esc(x.classification||'')} · ${esc(x.reference||'')}</small>${x.file==='DIP-79-2026'?`<div class="ok-file-lock">🔒 ${esc(lang==='es'?'Separación DIP 79: no usar en DIP 80 sin decisión expresa.':'DIP 79 separation: do not use in DIP 80 without an express decision.')}</div>`:''}</td>${stageKeys.map(k=>`<td>${tag(x.status?.[k]??false)}</td>`).join('')}<td>${esc(loc(x.publicLimit||x.note))}</td></tr>`).join('');
 };
 [search,file,status].forEach(x=>x.addEventListener(x===search?'input':'change',draw));draw();
}

function polygonPoints(values,cx,cy,r){
 const n=values.length;
 return values.map((v,i)=>{const a=(-Math.PI/2)+(i*2*Math.PI/n),rr=r*v/100;return `${(cx+Math.cos(a)*rr).toFixed(1)},${(cy+Math.sin(a)*rr).toFixed(1)}`}).join(' ');
}
function renderUrgent(d){
 const app=q('#urgent-app');if(!app)return;
 const labels=[T.currentRisk,T.reliability,T.exposure,T.irreversibility,T.competence,T.hearing,T.proportionality];
 const vals=labels.map((_,i)=>Object.values(d.urgentProtection.radar)[i]);
 const cx=230,cy=220,r=150,n=labels.length;
 let grids='',axes='',texts='';
 [25,50,75,100].forEach(p=>grids+=`<polygon class="ok-radar-grid" points="${polygonPoints(Array(n).fill(p),cx,cy,r)}"></polygon>`);
 labels.forEach((lab,i)=>{const a=(-Math.PI/2)+(i*2*Math.PI/n),x=cx+Math.cos(a)*(r+28),y=cy+Math.sin(a)*(r+28);axes+=`<line class="ok-radar-axis" x1="${cx}" y1="${cy}" x2="${cx+Math.cos(a)*r}" y2="${cy+Math.sin(a)*r}"></line>`;texts+=`<text class="ok-radar-label" x="${x}" y="${y}" text-anchor="${x<cx-15?'end':x>cx+15?'start':'middle'}">${esc(lab)}</text>`});
 app.innerHTML=`<div class="ok-radar-layout"><svg class="ok-radar-svg" viewBox="0 0 460 440" role="img" aria-label="${esc(T.urgency)}">${grids}${axes}<polygon class="ok-radar-area" points="${polygonPoints(vals,cx,cy,r)}"></polygon>${texts}</svg><div><span class="pw-status-badge judgment">${esc(T.urgencyQuestion)}</span><h2>${esc(loc(d.urgentProtection.question))}</h2><p>${esc(loc(d.urgentProtection.status))}</p><div class="ok-route-grid">${d.urgentProtection.routes.map(x=>`<article class="ok-route"><small>${esc(loc(x.authority))}</small><h3>${esc(x.id)}</h3><p>${esc(loc(x.scope))}</p>${tag(x.status)}</article>`).join('')}</div></div></div><h2>${esc(T.ladder)}</h2><ol class="ok-ladder">${d.urgentProtection.proportionality.map(x=>`<li>${esc(loc(x))}</li>`).join('')}</ol>`;
}

function renderModels(d){
 const app=q('#models-app');if(!app)return;
 app.innerHTML=`<div class="ok-model-grid"><div class="ok-model-list">${d.modelDecisions.map((m,i)=>`<button class="ok-model-button ${i===0?'active':''}" data-model="${esc(m.id)}">${esc(loc(m.title))}</button>`).join('')}</div><article id="ok-model-paper" class="ok-model-paper"></article></div>`;
 const paper=q('#ok-model-paper',app);
 const draw=(m)=>{
  paper.innerHTML=`<p class="pw-status-badge judgment">${esc(T.draft)}</p><h2>${esc(loc(m.title))}</h2><p>${esc(lang==='es'?'Ejemplo estructural. No representa una actuación, posición ni decisión de ICALPA.':'Structural example. It does not represent an ICALPA act, position or decision.')}</p>${m.fields.map(f=>`<div class="ok-model-field"><strong>${esc(T.fieldLabels[f]||f)}</strong><p>${esc(T.placeholder)}</p></div>`).join('')}`;
 };
 qa('[data-model]',app).forEach(b=>b.addEventListener('click',()=>{qa('[data-model]',app).forEach(x=>x.classList.remove('active'));b.classList.add('active');draw(byId(d.modelDecisions,b.dataset.model))}));
 draw(d.modelDecisions[0]);
}
function renderClassroom(d){
 const app=q('#classroom-app');if(!app)return;
 app.innerHTML=`<h2>${esc(T.chapters)}</h2><div class="ok-chapter-grid">${d.classroom.chapters.map((c,i)=>`<details class="ok-chapter" ${i===0?'open':''}><summary>${c.number}. ${esc(loc(c.title))}</summary><div><p>${esc(loc(c.theory))}</p><strong>${esc(lang==='es'?'Ejercicio':'Exercise')}</strong><p>${esc(loc(c.exercise))}</p></div></details>`).join('')}</div>
 <div class="ok-teaching-grid pw-section"><article class="ok-teaching-card"><h3>${esc(T.socratic)}</h3><ol>${d.classroom.socraticQuestions.map(x=>`<li>${esc(loc(x))}</li>`).join('')}</ol></article><article class="ok-teaching-card"><h3>${esc(T.hypotheticals)}</h3>${d.classroom.hypotheticals.map(x=>`<div class="ok-hypothetical"><strong>${esc(loc(x.title))}</strong><p>${esc(loc(x.question))}</p></div>`).join('')}</article><article class="ok-teaching-card"><h3>${esc(T.errors)}</h3><ul>${d.classroom.commonErrors.map(x=>`<li>${esc(loc(x))}</li>`).join('')}</ul></article></div>`;
}

async function boot(){
 setupNav();
 const loader=q('#ok-app');if(loader)loader.innerHTML=`<div class="ok-loader">${esc(T.loading)}</div>`;
 try{
  const res=await fetch(dataUrl,{cache:'no-store'});if(!res.ok)throw new Error(`${res.status}`);
  const d=await res.json();
  renderStatus(d);
  if(view==='root'){renderNow(d);renderFirstAnswers(d);renderModules(d);renderCorrections(d)}
  if(view==='chronology')renderChronology(d);
  if(view==='decision-tree')renderTree(d);
  if(view==='evidence-atlas')renderEvidence(d);
  if(view==='urgent-protection')renderUrgent(d);
  if(view==='models')renderModels(d);
  if(view==='classroom')renderClassroom(d);
  if(loader)loader.remove();
 }catch(err){
  if(loader)loader.innerHTML=`<div class="ok-error"><strong>${esc(T.error)}</strong><br>${esc(err.message)}</div>`;
  console.error(err);
 }
}
boot();
})();

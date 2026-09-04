(() => {
  'use strict';
  const path = location.pathname.replace(/\/index\.html$/, '/');
  const isEN = document.documentElement.lang?.toLowerCase().startsWith('en') || path.includes('/en/');
  const kinds = [
    ['dp1901','/dp-1901-2026/'],
    ['dp1956','/dp-1956-2026/'],
    ['c24', isEN ? '/control-24-insolvency-judge-complaint-36-2012/' : '/control-24-denuncia-juez-concurso-36-2012/']
  ];
  const current = kinds.find(([_,frag]) => path.includes(frag));
  if (!current || document.querySelector('[data-three-track-enhancement]')) return;
  const root = '/por-derecho/' + (isEN ? 'en/' : 'es/');
  const routes = {
    dp1901: root + 'dp-1901-2026/',
    dp1956: root + 'dp-1956-2026/',
    c24: root + (isEN ? 'control-24-insolvency-judge-complaint-36-2012/' : 'control-24-denuncia-juez-concurso-36-2012/'),
    data: '/por-derecho/data/three-track-full-digitisation-20260904.json'
  };
  const t = isEN ? {
    eyebrow:'FULL DIGITISATION · SOURCE-CONTROLLED · THREE CONNECTED ROUTES',
    title:'Read the same Sun Park chronology through three different legal questions.',
    intro:'The two criminal proceedings and Control 24 now share one visual evidence spine. Each lane keeps its own actor, duty, procedural status and evidential threshold. The purpose is non-fragmented reading without procedural conflation.',
    source:'Full digitisation', open:'Open route', current:'CURRENT PAGE',
    lanes:[
      ['DP 1901/2026','Private actors / Control 21','69-page base complaint + 9 July expansion. Public layer indexes actors, entities, chronology, allegation types, evidence sources, requested measures, limitations and open proof.','12 Jul 2026 order: five-day referral to the Prosecution Service concerning admission; not itself a later merits decision.'],
      ['DP 1956/2026','Insolvency Administrator / Control 22','55-page operative complaint, digitised page by page into actor-duty, knowledge, preservation, accounting, implementation, requested measures, contrary explanations and open documentary bridges.','Provisional dismissal communicated 21 Jul 2026; not acquittal or final merits exoneration.'],
      ['Control 24','Judicial decisions / supervision','79-page signed package + 10-page dependent supplement. Five modules: funded exit, credit/threshold, OB REM/non-validation, bidding/adjudication and legal-entity identity.','Presented 18 Jun 2026 under daily locator 24; formal court allocation, NIG and present criminal status remain unverified.']
    ],
    events:[
      ['2011–2016','Community authority, debt/vote, operation and notice'],
      ['2017–Jun 2018','CAM/credit entry, measurements/access, security, funded exit'],
      ['7 Jun 2018','Alleged material change of access/control'],
      ['2018–2019','OB REM, €400,000 and 24 Oct 2019 non-validation'],
      ['2020–2022','Credit/threshold, estate, bidding, adjudication and deed'],
      ['2022–2026','HNT/MYND, RIC/RICPE, operation, institutional handling']
    ],
    q:['Who created, used or benefited from the private authority/control route?','What did the Insolvency Administrator know, verify, report, preserve, account for or leave uncorrected?','What reached the court, which decisions followed, and what documentary bridge explains their effects?'],
    boundary:'Shared evidence does not transfer knowledge, intent, causation, guilt or liability. Related does not mean consolidated. Filing does not mean admission. Later title, operation or financing does not validate predecessor authority.'
  } : {
    eyebrow:'DIGITALIZACIÓN ÍNTEGRA · FUENTE CONTROLADA · TRES VÍAS CONECTADAS',
    title:'Una misma cronología Sun Park, tres preguntas jurídicas distintas.',
    intro:'Las dos diligencias penales y Control 24 comparten ahora una columna probatoria visual. Cada vía conserva sujeto, deber, estado procesal y umbral probatorio propios. El objetivo es una lectura no fragmentada sin fusión procesal.',
    source:'Digitalización íntegra', open:'Abrir vía', current:'PÁGINA ACTUAL',
    lanes:[
      ['DP 1901/2026','Actores privados / Control 21','Denuncia base de 69 páginas + ampliación de 9 de julio. La capa pública indexa actores, entidades, cronología, tipos de alegación, fuentes, diligencias solicitadas, límites y prueba pendiente.','Providencia 12/07/2026: traslado a Fiscalía por cinco días sobre admisión; no equivale por sí sola a resolución posterior de fondo.'],
      ['DP 1956/2026','Administrador Concursal / Control 22','Denuncia operativa de 55 páginas, digitalizada página a página en deberes, conocimiento, preservación, contabilidad, implementación, diligencias, explicaciones alternativas y puentes documentales abiertos.','Sobreseimiento provisional comunicado 21/07/2026; no absolución ni exoneración definitiva de fondo.'],
      ['Control 24','Resoluciones / supervisión judicial','Paquete firmado de 79 páginas + aportación dependiente de 10 páginas. Cinco módulos: salida financiada, crédito/umbral, OB REM/no convalidación, licitación/adjudicación e identidad societaria.','Presentado 18/06/2026 bajo localizador diario 24; reparto, NIG y estado penal actual siguen sin verificación primaria.']
    ],
    events:[
      ['2011–2016','Autoridad comunitaria, deuda/voto, explotación y avisos'],
      ['2017–jun 2018','Entrada CAM/crédito, mediciones/acceso, seguridad y salida financiada'],
      ['7 jun 2018','Cambio material de acceso/control alegado'],
      ['2018–2019','OB REM, €400.000 y no convalidación de 24 oct 2019'],
      ['2020–2022','Crédito/umbral, masa, licitación, adjudicación y escritura'],
      ['2022–2026','HNT/MYND, RIC/RICPE, explotación y tratamiento institucional']
    ],
    q:['¿Quién creó, usó o se benefició de la ruta privada de autoridad/control?','¿Qué conoció, verificó, comunicó, preservó, contabilizó o dejó sin corregir el Administrador Concursal?','¿Qué llegó al órgano judicial, qué decisiones siguieron y qué puente documental explica sus efectos?'],
    boundary:'La prueba compartida no transfiere conocimiento, dolo, causalidad, culpabilidad ni responsabilidad. Relacionado no significa acumulado. Presentación no significa admisión. Título, explotación o financiación posteriores no validan la autoridad precedente.'
  };
  const style=document.createElement('style');
  style.textContent=`.pd3e{max-width:1180px;margin:2rem auto;padding:0 1rem}.pd3e-wrap{border:1px solid #cbd3d7;border-radius:22px;overflow:hidden;background:#fff;box-shadow:0 16px 44px rgba(19,37,45,.10)}.pd3e-head{padding:1.5rem;background:linear-gradient(135deg,#112832,#334d58 60%,#735e28);color:white}.pd3e-head *{color:white}.pd3e-ey{font-size:.72rem;font-weight:900;letter-spacing:.09em}.pd3e-grid{display:grid;grid-template-columns:.78fr 2.22fr}.pd3e-spine{padding:1rem;background:#f4f0e7}.pd3e-event{display:grid;grid-template-columns:95px 1fr;gap:.55rem;padding:.65rem 0;border-top:1px solid #d9d3c5;font-size:.84rem}.pd3e-event strong{color:#8b3e34}.pd3e-lanes{display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem;padding:1rem}.pd3e-lane{border:1px solid #ccd4d7;border-radius:15px;padding:1rem;display:flex;flex-direction:column}.pd3e-lane.active{border:2px solid #c49538;box-shadow:0 0 0 4px rgba(196,149,56,.13)}.pd3e-tag{font-size:.68rem;font-weight:900;letter-spacing:.07em;color:#8b3e34;text-transform:uppercase}.pd3e-q{font-weight:800;font-size:.91rem}.pd3e-status{background:#f1f6f7;border-left:4px solid #37647b;padding:.65rem;font-size:.83rem}.pd3e-actions{margin-top:auto;display:flex;gap:.45rem;flex-wrap:wrap}.pd3e-actions a{background:#13252d;color:#fff;text-decoration:none;border-radius:999px;padding:.48rem .7rem;font-size:.77rem;font-weight:850}.pd3e-actions a.secondary{background:#eee8dc;color:#13252d}.pd3e-bound{margin:0 1rem 1rem;padding:.8rem;border-left:5px solid #c49538;background:#fff8e9;font-size:.9rem}@media(max-width:900px){.pd3e-grid,.pd3e-lanes{grid-template-columns:1fr}}`;
  document.head.appendChild(style);
  const active = current[0]==='dp1901'?0:current[0]==='dp1956'?1:2;
  const section=document.createElement('section'); section.className='pd3e'; section.dataset.threeTrackEnhancement='20260904';
  section.innerHTML=`<div class="pd3e-wrap"><div class="pd3e-head"><div class="pd3e-ey">${t.eyebrow}</div><h2>${t.title}</h2><p>${t.intro}</p></div><div class="pd3e-grid"><aside class="pd3e-spine"><h3>${isEN?'Shared factual spine':'Columna factual compartida'}</h3>${t.events.map(e=>`<div class="pd3e-event"><strong>${e[0]}</strong><span>${e[1]}</span></div>`).join('')}</aside><div class="pd3e-lanes">${t.lanes.map((l,i)=>`<article class="pd3e-lane ${i===active?'active':''}"><div class="pd3e-tag">${i===active?t.current:l[1]}</div><h3>${l[0]}</h3><p class="pd3e-q">${t.q[i]}</p><p>${l[2]}</p><p class="pd3e-status">${l[3]}</p><div class="pd3e-actions"><a href="${[routes.dp1901,routes.dp1956,routes.c24][i]}">${t.open}</a><a class="secondary" href="${routes.data}">${t.source}</a></div></article>`).join('')}</div></div><div class="pd3e-bound"><strong>${t.boundary}</strong></div></div>`;
  const main=document.querySelector('main'); if(!main) return;
  const first=main.querySelector('section'); first?.after(section) || main.prepend(section);
})();
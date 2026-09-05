(() => {
  'use strict';
  const p = location.pathname.replace(/\/+$/, '/');
  if (!p.endsWith('/en/puzzle/') && !p.endsWith('/es/puzzle/')) return;
  if (document.querySelector('[data-pd-puzzle-continuity="20260905a"]')) return;

  const script = document.currentScript;
  if (!script) return;
  const root = new URL('../', script.src);
  const lang = p.includes('/es/') ? 'es' : 'en';
  const DATA = new URL('../data/puzzle/puzzle-public-interest-alertador-20260905.json', script.src).href;
  const GUIDE = new URL('../data/puzzle/puzzle-reading-guide-2026.json', script.src).href;

  const tx = lang === 'es' ? {
    baseline:'Línea base judicial de lectura',
    baselineText:'La narración de control vigente del PUZZLE es la capa acompañante/aportación de 21 de julio de 2026 para DP 1956/2026 y DP 1901/2026. El mapa de 32 páginas sigue siendo el PUZZLE histórico de junio de 2024. Los escritos de junio de 2026 son fuentes procesales anteriores, no la narración actual del visor.',
    receipt:'Límite procesal', receiptText:'Los documentos recuperados se identifican como «presentación 21/07/2026». Esa cabecera no sustituye por sí sola un justificante registral, índice judicial certificado, resolución de admisión o pronunciamiento de fondo.',
    capacities:'Capacidad declarada y dimensión pública',
    capacityText:'Gil Marer presenta esta reconstrucción en dos capacidades declaradas: como persona directamente interesada que afirma perjuicio económico y afectación de sus intereses jurídicos/económicos, y como alertador/informante de interés público que ha comunicado hechos a juzgados, fiscalías, reguladores y autoridades. Esta descripción no determina automáticamente la protección estatutaria de ningún régimen.',
    foreign:'Aweswell Limited se presenta separadamente como inversor extranjero / interés económico británico en España. Esa condición no se confunde con la condición de alertador de Gil Marer.',
    funds:'Dimensión de interés público y fondos públicos',
    fundsRule:'La interfaz distingue instrumento público documentado, contacto institucional, alegación de Por Derecho, pregunta abierta sobre fondos públicos y mero contexto. No se afirma uso, pérdida o desvío de fondos públicos sin identificar instrumento, beneficiario, importe, decisión y efecto económico.',
    original:'Original auténtico', open:'Abrir PDF original', download:'Descargar PDF original', pending:'PDF original pendiente de materialización pública',
    pendingText:'El original exacto está controlado por 32 páginas, 50.046.618 bytes y SHA-256 e441bdb368c0092d5b15ca5ee911eeac266540bde54817e424f3075f4c5fdd47. No se sustituye por un archivo parecido, capturas o una reconstrucción.',
    fallback:'Navegación resiliente', fallbackText:'Aunque el navegador no pueda incrustar PDFs, la guía de lectura, capítulos, notas, interlinks y estado probatorio deben seguir siendo utilizables. Use los controles del visor y los enlaces de evidencia debajo.',
    frameworks:'Marco de protección — sujeto a requisitos',
    eu:'UE · Directiva 2019/1937: contexto laboral/profesional y demás requisitos de ámbito.',
    spain:'España · Ley 2/2023: contexto laboral/profesional y demás requisitos legales; el perjuicio económico por sí solo no basta.',
    germany:'Alemania · HinSchG: solo si concurren el nexo profesional, ámbito material y demás requisitos aplicables.',
    uk:'Reino Unido · ERA 1996/PIDA 1998: protección principalmente vinculada a trabajadores y protected disclosures; ciudadanía o interés económico británico por sí solos no bastan.'
  } : {
    baseline:'Judicial reading baseline',
    baselineText:'The controlling PUZZLE narration is the 21 July 2026 companion/aportación layer for DP 1956/2026 and DP 1901/2026. The 32-page map remains the historical June-2024 PUZZLE. The June-2026 pleadings are earlier procedural sources, not the current viewer narration.',
    receipt:'Procedural limit', receiptText:'Recovered documents identify themselves as “presentation 21/07/2026”. That heading does not itself replace a registry receipt, certified court index, admission ruling or merits determination.',
    capacities:'Declared capacity and public-interest dimension',
    capacityText:'Gil Marer presents this reconstruction in two declared capacities: as a directly interested person who asserts economic harm and affected legal/economic interests, and as a public-interest reporter/alertador who has reported matters to courts, prosecutors, regulators and public authorities. This description does not automatically determine statutory protected-informant status under any regime.',
    foreign:'Aweswell Limited is presented separately as a foreign investor / UK economic-interest actor in Spain. That status is not collapsed into Gil Marer’s asserted alertador capacity.',
    funds:'Public-interest and public-funds dimension',
    fundsRule:'The interface distinguishes documented public instruments, institutional contact, Por Derecho allegations, open public-funds questions and context only. It does not assert use, loss or diversion of public funds without the instrument, beneficiary, amount, decision and economic effect.',
    original:'Authentic original', open:'Open original PDF', download:'Download original PDF', pending:'Original PDF pending public materialisation',
    pendingText:'The exact original is controlled as 32 pages, 50,046,618 bytes and SHA-256 e441bdb368c0092d5b15ca5ee911eeac266540bde54817e424f3075f4c5fdd47. It is not replaced by a near-match, screenshots or reconstruction.',
    fallback:'Resilient navigation', fallbackText:'Even if a browser cannot embed PDFs, the reading guide, chapter navigation, notes, interlinks and evidential status must remain usable. Use the viewer controls and evidence links below.',
    frameworks:'Protection frameworks — subject to statutory conditions',
    eu:'EU · Directive 2019/1937: work-related context plus the Directive’s other scope/protection requirements.',
    spain:'Spain · Law 2/2023: labour/professional context plus other statutory conditions; economic injury alone is not treated as sufficient.',
    germany:'Germany · HinSchG: only if the professional nexus, material scope and other applicable requirements are met.',
    uk:'United Kingdom · ERA 1996/PIDA 1998: principally worker/protected-disclosure based; British citizenship or UK economic interest alone is not sufficient.'
  };

  const esc = (v='') => String(v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const addCSS = () => {
    if (document.getElementById('pd-puzzle-continuity-style')) return;
    const s=document.createElement('style'); s.id='pd-puzzle-continuity-style';
    s.textContent='.pd-puzzle-continuity{max-width:1500px;margin:1.25rem auto;padding:1rem clamp(1rem,2.5vw,2rem);border:1px solid rgba(128,128,128,.32);border-radius:16px;background:var(--surface,#fff);color:inherit}.pd-puzzle-continuity h2{margin:.2rem 0 .75rem}.pd-puzzle-continuity__grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:.8rem}.pd-puzzle-continuity__card{border:1px solid rgba(128,128,128,.26);border-radius:12px;padding:.9rem;background:rgba(128,128,128,.04)}.pd-puzzle-continuity__warn{border-left:5px solid #a56c00;padding:.75rem 1rem;background:rgba(165,108,0,.08);margin:.8rem 0}.pd-puzzle-continuity__actions{display:flex;gap:.6rem;flex-wrap:wrap;margin:.8rem 0}.pd-puzzle-continuity__actions a{padding:.6rem .8rem;border:1px solid currentColor;border-radius:9px;font-weight:800;text-decoration:none}.pd-puzzle-continuity__actions a[aria-disabled="true"]{opacity:.5;pointer-events:none}.pd-puzzle-continuity code{overflow-wrap:anywhere}';
    document.head.appendChild(s);
  };

  Promise.all([fetch(DATA,{cache:'no-store'}).then(r=>r.json()),fetch(GUIDE,{cache:'no-store'}).then(r=>r.json())]).then(([data,guide])=>{
    addCSS();
    const main=document.querySelector('main'); if(!main) return;
    const pdfUrl=new URL(guide.document.assetPath,root).href;
    const section=document.createElement('section'); section.className='pd-puzzle-continuity'; section.dataset.pdPuzzleContinuity='20260905a';
    section.innerHTML=`<p><strong>PD-PUZZLE-GOV-20260905-01</strong></p><h2>${esc(tx.baseline)}</h2><p>${esc(tx.baselineText)}</p><div class="pd-puzzle-continuity__warn"><strong>${esc(tx.receipt)}.</strong> ${esc(tx.receiptText)}</div><div class="pd-puzzle-continuity__grid"><article class="pd-puzzle-continuity__card"><h3>${esc(tx.capacities)}</h3><p>${esc(tx.capacityText)}</p><p>${esc(tx.foreign)}</p></article><article class="pd-puzzle-continuity__card"><h3>${esc(tx.frameworks)}</h3><ul><li>${esc(tx.eu)}</li><li>${esc(tx.spain)}</li><li>${esc(tx.germany)}</li><li>${esc(tx.uk)}</li></ul></article><article class="pd-puzzle-continuity__card"><h3>${esc(tx.funds)}</h3><p>${esc(tx.fundsRule)}</p><ul>${data.public_interest_perimeter.map(x=>`<li><strong>${esc(x.label)}</strong> · ${esc(x.status)}<br>${esc(x.question)}</li>`).join('')}</ul></article><article class="pd-puzzle-continuity__card"><h3>${esc(tx.original)}</h3><p>${esc(tx.pendingText)}</p><div class="pd-puzzle-continuity__actions"><a data-pd-puzzle-open href="${esc(pdfUrl)}" target="_blank" rel="noopener">${esc(tx.open)}</a><a data-pd-puzzle-download href="${esc(pdfUrl)}" download="PUZZLE-2024-original.pdf">${esc(tx.download)}</a></div><p><code>${esc(guide.document.sha256)}</code></p></article></div><div class="pd-puzzle-continuity__warn"><strong>${esc(tx.fallback)}.</strong> ${esc(tx.fallbackText)}</div>`;
    const viewer=document.querySelector('[data-pd-puzzle-viewer]');
    if(viewer) viewer.insertAdjacentElement('afterend',section); else main.prepend(section);

    const enhance=()=>{
      const toolbarPdf=document.querySelector('[data-original-pdf]');
      if(toolbarPdf){ toolbarPdf.setAttribute('download','PUZZLE-2024-original.pdf'); toolbarPdf.textContent=tx.download; }
      const state=document.querySelector('[data-pd-puzzle-viewer]')?.dataset.pdfState;
      if(state==='missing') section.querySelectorAll('[data-pd-puzzle-open],[data-pd-puzzle-download]').forEach(a=>{a.setAttribute('aria-disabled','true');a.title=tx.pending;});
      if(state==='ready') section.querySelectorAll('[data-pd-puzzle-open],[data-pd-puzzle-download]').forEach(a=>a.removeAttribute('aria-disabled'));
    };
    enhance();
    let tries=0; const timer=setInterval(()=>{enhance(); if(++tries>20) clearInterval(timer);},250);
  }).catch(err=>console.warn('Puzzle continuity layer unavailable',err));
})();

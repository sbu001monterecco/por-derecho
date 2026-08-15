(() => {
  const path = location.pathname;
  const isEs = path.includes('/es/');
  const firstSection = document.querySelector('main .section');
  if (!firstSection || document.querySelector('[data-accountability-backlog]')) return;

  const style = document.createElement('style');
  style.textContent = `.ab-wrap{margin:1.2rem 0 1.8rem}.ab-title{font-size:1.35rem;margin:.2rem 0 .75rem}.ab-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.65rem}.ab-step,.ab-compare{background:#fff;border:1px solid rgba(20,35,45,.16);border-radius:14px;padding:.9rem}.ab-step strong{display:block;font-size:.78rem;letter-spacing:.05em;text-transform:uppercase;margin-bottom:.25rem}.ab-arrow{text-align:center;font-weight:900;align-self:center}.ab-note{margin:.8rem 0 0;padding:.8rem 1rem;border-left:4px solid #315c7b;background:#f5f7f8}.ab-compare-grid{display:grid;grid-template-columns:1fr auto 1fr;gap:.65rem;align-items:stretch}.ab-vs{align-self:center;font-weight:900;text-align:center}.ab-open{border-left:4px solid #c89432}.ab-safe{font-size:.9rem;opacity:.85}@media(max-width:720px){.ab-compare-grid{grid-template-columns:1fr}.ab-vs{transform:none}}`;
  document.head.appendChild(style);

  const box = document.createElement('section');
  box.dataset.accountabilityBacklog = 'true';
  box.className = 'ab-wrap';

  const flows = {
    judge: isEs ? {
      title:'Matriz visual: qué estaba ante el juez y qué explica el siguiente paso',
      steps:[['1 · EN AUTOS','Escrito / prueba identificable'],['2 · OBJETO','Qué cuestión jurídica se sometió'],['3 · DECISIÓN','Qué resolvió expresamente'],['4 · NO DECIDIDO','Qué quedó fuera o abierto'],['5 · DESPUÉS','Qué resolución o acto explica el siguiente salto']],
      note:'La visualización evita dos atajos: que “estar en autos” equivalga automáticamente a conocimiento personal, y que una decisión adversa pruebe sesgo. El expediente certificado debe permitir reconstruir la secuencia.'
    } : {
      title:'Visual matrix: what was before the judge and what explains the next step',
      steps:[['1 · IN THE FILE','Identifiable filing / evidence'],['2 · ISSUE','Legal question submitted'],['3 · DECISION','What was expressly decided'],['4 · NOT DECIDED','What remained outside/open'],['5 · NEXT','What later order or act explains the next step']],
      note:'This avoids two shortcuts: treating material in the file as automatic proof of personal knowledge, and treating an adverse ruling as proof of bias. The certified record should reconstruct the sequence.'
    },
    ap: isEs ? {
      title:'Segunda instancia: expediente útil antes que narrativa total',
      steps:[['RECURSO','Qué resolución se apela'],['EXPEDIENTE','Qué piezas llegaron a la Sala'],['PRUEBA','Qué documento adicional se pidió'],['COMPETENCIA','Qué puede revisar la Sección 4ª'],['RESULTADO','Qué cuestión puede corregir o confirmar']],
      note:'La Sala no investiga de novo toda la historia. La presión documental correcta es comprobar que el material necesario para resolver lo apelado está completo, utilizable y trazable.'
    } : {
      title:'Second instance: usable record before total narrative',
      steps:[['APPEAL','What ruling is appealed'],['RECORD','What reached the chamber'],['EVIDENCE','What additional material was sought'],['REMIT','What Section 4 can review'],['RESULT','What can be corrected or confirmed']],
      note:'The chamber does not investigate the whole history de novo. The proper documentary test is whether the material needed to decide the appeal is complete, usable and traceable.'
    },
    yaiza: isEs ? {
      title:'La cadena municipal que debe poder reconstruirse',
      steps:[['ACTOR','Quién fue tratado como titular / promotor / explotador'],['FUENTE','Qué documento sustentó esa atribución'],['PERÍMETRO','Qué fincas o unidades abarcaba'],['ACTO','Licencia / obra / tributo / comunicación'],['MATKATOR','Cómo se trató al titular extraconcursal']],
      note:'Una denominación o tratamiento administrativo no altera por sí solo la propiedad civil o registral. La pregunta es qué base documental utilizó el Ayuntamiento para cada acto.'
    } : {
      title:'The municipal chain that should be reconstructable',
      steps:[['ACTOR','Who was treated as owner / promoter / operator'],['SOURCE','What document supported it'],['PERIMETER','Which properties or units it covered'],['ACT','Licence / works / tax / communication'],['MATKATOR','How the non-insolvent owner was treated']],
      note:'Administrative treatment does not by itself alter civil or registered title. The question is what documentary basis the municipality used for each act.'
    },
    intervencion: isEs ? {
      title:'Competencia y remisión: una salida fuera de perímetro debe dejar rastro',
      steps:[['RECIBIDO','Qué comunicación entró'],['PERÍMETRO','Qué parte asumió Intervención'],['FUERA','Qué parte consideró ajena'],['REMISIÓN','A qué órgano la derivó'],['RECEPCIÓN / RESULTADO','Qué asiento demuestra llegada y tratamiento']],
      note:'“Fuera de competencia” puede ser jurídicamente correcto. La cuestión auditable es si delimitación, remisión, recepción y resultado quedaron documentados.'
    } : {
      title:'Remit and referral: an out-of-scope issue should leave a trail',
      steps:[['RECEIVED','What communication entered'],['REMIT','What Intervención took on'],['OUTSIDE','What it treated as outside remit'],['REFERRAL','Where it was sent'],['RECEIPT / RESULT','What record proves arrival and treatment']],
      note:'“Outside remit” may be legally correct. The auditable question is whether delimitation, referral, receipt and outcome were documented.'
    },
    snca: isEs ? {
      title:'“Se verificó” debe poder descomponerse',
      steps:[['ALERTA','Qué hecho se comunicó'],['FUENTE','Qué registro o documento se consultó'],['COMPROBACIÓN','Qué se verificó concretamente'],['RESULTADO','Qué encontró el SNCA'],['ACTUACIÓN','Qué preservó, remitió o decidió']],
      note:'Una alerta no prueba fraude. Tampoco una referencia genérica a “verificaciones” permite saber qué se comprobó. El expediente 141-2026-IRR02 debería permitir reconstruir esa cadena.'
    } : {
      title:'“Verified” should be decomposable',
      steps:[['ALERT','What fact was reported'],['SOURCE','What record/document was checked'],['CHECK','What was actually verified'],['RESULT','What SNCA found'],['ACTION','What was preserved, referred or decided']],
      note:'An alert does not prove fraud. Nor does a generic reference to “checks” show what was examined. File 141-2026-IRR02 should permit reconstruction of that chain.'
    }
  };

  let cfg = null;
  if (path.includes('concurso-36-2012-magistrado-juez') || path.includes('insolvency-36-2012-judge')) cfg = flows.judge;
  else if (path.includes('concurso-36-2012-ap-seccion-4') || path.includes('insolvency-36-2012-ap-section-4')) cfg = flows.ap;
  else if (path.includes('yaiza-trazabilidad-institucional') || path.includes('yaiza-institutional-traceability')) cfg = flows.yaiza;
  else if (path.includes('intervencion-general-siinf-trazabilidad') || path.includes('intervencion-general-siinf-traceability')) cfg = flows.intervencion;
  else if (path.includes('snca-fondos-europeos-trazabilidad') || path.includes('snca-eu-funds-traceability')) cfg = flows.snca;

  if (cfg) {
    box.innerHTML = `<div class="shell"><h2 class="ab-title">${cfg.title}</h2><div class="ab-grid">${cfg.steps.map(([a,b])=>`<div class="ab-step"><strong>${a}</strong><span>${b}</span></div>`).join('')}</div><p class="ab-note">${cfg.note}</p></div>`;
    firstSection.parentNode.insertBefore(box, firstSection.nextSibling);
    return;
  }

  if (path.includes('ricpe-responsabilidad-documental') || path.includes('ricpe-documentary-accountability')) {
    const t = isEs ? {
      title:'La comparación que debe mantenerse visible',
      left:'PRESENTACIÓN / EXPECTATIVA DE INVERSIÓN',
      ltext:'Qué decía el material al inversor en esa fecha sobre proyecto, activo, adquisición y condiciones.',
      right:'TÍTULO / CONDICIONALIDAD DOCUMENTADA',
      rtext:'Qué acreditaban entonces los documentos sobre propiedad efectiva, adquisición judicial pendiente, terceros y due diligence.',
      note:'La diferencia entre representación y estado jurídico no prueba por sí sola engaño. La prueba es comparar texto, fecha, destinatario, condición y conocimiento real.'
    } : {
      title:'The comparison that should remain visible',
      left:'INVESTMENT PRESENTATION / EXPECTATION',
      ltext:'What investor material said at that date about the project, asset, acquisition and conditions.',
      right:'DOCUMENTED TITLE / CONDITIONALITY',
      rtext:'What contemporaneous documents showed about effective ownership, pending judicial acquisition, third parties and due diligence.',
      note:'A difference between presentation and legal status does not by itself prove deception. The test is text, date, audience, condition and actual knowledge.'
    };
    box.innerHTML = `<div class="shell"><h2 class="ab-title">${t.title}</h2><div class="ab-compare-grid"><div class="ab-compare"><strong>${t.left}</strong><p>${t.ltext}</p></div><div class="ab-vs">↔</div><div class="ab-compare ab-open"><strong>${t.right}</strong><p>${t.rtext}</p></div></div><p class="ab-note">${t.note}</p></div>`;
    firstSection.parentNode.insertBefore(box, firstSection.nextSibling);
  }
})();
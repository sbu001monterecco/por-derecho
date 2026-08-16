(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const esCal = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const enCal = path.endsWith('/en/insolvency-classification-parallel-lives/');
  const esRec = path.endsWith('/es/objetivos-recuperacion-restitucion/');
  const enRec = path.endsWith('/en/recovery-restitution-objectives/');
  if (!esCal && !enCal && !esRec && !enRec) return;
  if (document.querySelector('[data-cal-counter-record-20260816]')) return;

  const es = esCal || esRec;
  const c = es ? {
    kicker: 'CONTRARREGISTRO DOCUMENTAL · QUÉ EXISTÍA MIENTRAS SE CONSTRUÍA LA ACUSACIÓN',
    title: 'No basta con leer la acusación. Hay que leer, al mismo tiempo, lo que se estaba haciendo para salvar y recuperar el negocio.',
    lead: 'El expediente de calificación no puede evaluarse de forma aislada de la prueba contemporánea de viabilidad, financiación, explotación, protección patrimonial y recuperación. Este bloque no declara que cada plan tuviera éxito; exige que la acusación se confronte con el registro que existía al mismo tiempo.',
    items: [
      ['1 JUN 2012 · MEMORIA LPB', 'La propia memoria concursal identifica la viabilidad mediante un convenio de quita y espera con acreedores. La entrada en concurso no se presenta en esa fuente como abandono del negocio.'],
      ['29 MAR / 17 ABR 2017 · CONVENIO Y PLAN DE VIABILIDAD', 'El documento declara como objetivos conservar la actividad y satisfacer a los acreedores; registra garantía/recapitalización de Aweswell, trabajo de refinanciación y una estructura operativa/comercial con operadores.'],
      ['2017 · GMAIL, PLANES, VALORACIÓN Y FINANCIACIÓN', 'La correspondencia documenta trabajo continuado sobre plan de negocio, datos de crecimiento, valoración, term sheet/bridge finance, operadores, distribución e inversores. Negociación no equivale a cierre, pero sí contradice una lectura de pasividad o abandono.'],
      ['DIC 2018 · PROTECCIÓN DE ACTIVOS Y REGISTRO', 'La correspondencia documenta recursos, avisos al Registro, revisión de servidumbres/ob rem, búsqueda de escrituras y actuaciones para proteger o impugnar consecuencias patrimoniales durante el conflicto de liquidación.'],
      ['ENE 2019 · DI 248', 'La ampliación incorporada al expediente registra la posición de que se estaban realizando actuaciones para concluir el concurso por la vía del antiguo art. 176 LC y que se había obtenido la financiación necesaria. Eso no prueba que cada borrador histórico fuese presentado; sí prueba que esa posición existía contemporáneamente.'],
      ['2019–2026 · OPOSICIÓN, RECURSO, PRESERVACIÓN Y RECUPERACIÓN', 'La oposición formal, los recursos, las objeciones sobre deuda/valor/título, la preservación de prueba y las vías judiciales, fiscales, regulatorias y administrativas muestran una continuidad de actuación que debe examinarse junto al relato de culpabilidad.']
    ],
    thesis: 'La pregunta que debe responder cualquier análisis serio',
    thesisBody: '<strong>Si la acusación describía obstrucción, falta de colaboración, fracaso o conducta culpable, ¿qué sabía cada actor de este contrarregistro contemporáneo y cómo lo trató?</strong> La comparación correcta es: acusación → actuación contemporánea → fuente primaria → conocimiento del actor → tratamiento judicial → apelación → efecto patrimonial y remedio.',
    boundary: '<strong>Límite:</strong> planes, term sheets, proyecciones, negociaciones y escritos de parte no se convierten por este bloque en financiación ejecutada, convenio aprobado, éxito económico ni prueba de delito. Su relevancia es que forman parte del registro contemporáneo que debe ser confrontado, no borrado.',
    status: 'Estado de fuente',
    statusBody: 'El informe de calificación de la AC de 11 de febrero de 2019, de 47 páginas, ya ha sido leído íntegramente. Permanecen abiertos la reconciliación completa de anexos, la prueba de qué documentación contradictoria estuvo efectivamente ante cada actor, la vista/notificación de 2023, el expediente completo de apelación y la ejecución real de determinados instrumentos de rescate.'
  } : {
    kicker: 'DOCUMENTARY COUNTER-RECORD · WHAT EXISTED WHILE THE ACCUSATION WAS BEING BUILT',
    title: 'The accusation cannot be read alone. It must be read beside what was being done to save and recover the business.',
    lead: 'The classification record cannot fairly be assessed in isolation from contemporaneous evidence of viability, finance, operation, asset protection and recovery. This block does not claim every plan succeeded; it requires the accusation to be tested against the record that existed at the same time.',
    items: [
      ['1 JUN 2012 · LPB MEMORANDUM', 'The insolvency memorandum itself identifies a creditor arrangement as the viability route. In that source, entry into insolvency is not presented as abandonment of the business.'],
      ['29 MAR / 17 APR 2017 · CONVENIO AND VIABILITY PLAN', 'The document states that its objectives were to preserve business activity and satisfy creditors; it records Aweswell guarantee/recapitalisation, refinancing work and an operator/commercial structure.'],
      ['2017 · GMAIL, BUSINESS PLANS, VALUATION AND FINANCE', 'Correspondence documents sustained work on business planning, operating-growth data, valuation, term-sheet/bridge finance, operators, distribution and investors. Negotiation is not closing, but it is material evidence against a narrative of passivity or abandonment.'],
      ['DEC 2018 · ASSET AND REGISTRY PROTECTION', 'Correspondence documents appeals, Registry notices, servitude/ob-rem review, deed recovery and steps intended to protect or challenge patrimonial consequences during the liquidation conflict.'],
      ['JAN 2019 · DI 248', 'The expansion placed in the file records the position that steps were being taken to conclude the insolvency under former Article 176 LC and that necessary financing had been obtained. This does not prove every historical draft was filed; it does prove that position existed contemporaneously.'],
      ['2019–2026 · OPPOSITION, APPEAL, PRESERVATION AND RECOVERY', 'Formal opposition, appeals, debt/value/title objections, evidence preservation and judicial, prosecutorial, regulatory and administrative routes show continuing action that must be examined alongside the culpability narrative.']
    ],
    thesis: 'The question any serious analysis must answer',
    thesisBody: '<strong>If the accusation described obstruction, non-collaboration, failure or culpable conduct, what did each actor know about this contemporaneous counter-record, and how was it treated?</strong> The correct comparison is: allegation → contemporaneous act → primary source → actor knowledge → judicial treatment → appeal → patrimonial consequence and remedy.',
    boundary: '<strong>Boundary:</strong> plans, term sheets, projections, negotiations and party filings do not become executed funding, an approved convenio, economic success or proof of crime by appearing here. Their relevance is that they form part of the contemporaneous record that must be confronted rather than erased.',
    status: 'Source status',
    statusBody: 'The insolvency administrator’s 47-page classification report of 11 February 2019 has now been read in full. Still open are complete annex reconciliation, proof of which contrary documents were actually before each actor, the 2023 hearing/service record, the complete appellate record and actual execution/performance of particular rescue instruments.'
  };

  const style = document.createElement('style');
  style.textContent = `
    .calcr{padding:0 0 2.2rem}.calcr-wrap{max-width:1080px;margin:0 auto}.calcr-box{background:#111f26;color:#fff;border-radius:20px;padding:1.35rem;border:1px solid rgba(255,255,255,.12);box-shadow:0 14px 34px rgba(19,37,45,.12)}
    .calcr-kicker{font-size:.73rem;font-weight:900;letter-spacing:.1em;text-transform:uppercase;color:#d8c492}.calcr-box h2{font-size:clamp(1.65rem,3.4vw,2.35rem);line-height:1.08;margin:.35rem 0 .75rem}.calcr-box>p{color:#e7ecee}
    .calcr-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;margin:1rem 0}.calcr-card{background:#fff;color:#17242a;border-radius:14px;padding:1rem;border-top:4px solid #9a7536}.calcr-card strong{display:block;font-size:.78rem;letter-spacing:.055em;text-transform:uppercase;margin-bottom:.4rem;color:#71572d}
    .calcr-thesis{background:#f2eee2;color:#17242a;border-radius:14px;padding:1rem 1.1rem;margin-top:.8rem}.calcr-status{border:1px solid rgba(255,255,255,.24);border-radius:14px;padding:1rem 1.1rem;margin-top:.8rem}.calcr-status h3,.calcr-thesis h3{margin:.1rem 0 .45rem}.calcr-boundary{font-size:.88rem;color:#d6dde0;margin-top:.85rem}
    @media(max-width:820px){.calcr-grid{grid-template-columns:1fr}.calcr-box{border-radius:0}}
  `;
  document.head.appendChild(style);

  const cards = c.items.map(([h,b]) => `<article class="calcr-card"><strong>${h}</strong><span>${b}</span></article>`).join('');
  const section = document.createElement('section');
  section.className = 'section calcr';
  section.dataset.calCounterRecord20260816 = '1';
  section.innerHTML = `<div class="shell calcr-wrap"><div class="calcr-box"><div class="calcr-kicker">${c.kicker}</div><h2>${c.title}</h2><p>${c.lead}</p><div class="calcr-grid">${cards}</div><div class="calcr-thesis"><h3>${c.thesis}</h3><p>${c.thesisBody}</p></div><div class="calcr-status"><h3>${c.status}</h3><p>${c.statusBody}</p></div><p class="calcr-boundary">${c.boundary}</p></div></div>`;

  const recovery = document.querySelector('[data-cal-recovery-adversity-20260816]');
  const opening = document.querySelector('[data-calificacion-opening-20260816]');
  const hero = document.querySelector('main .hero');
  if (recovery) recovery.insertAdjacentElement('afterend', section);
  else if (opening) opening.insertAdjacentElement('afterend', section);
  else if (hero) hero.insertAdjacentElement('afterend', section);
})();

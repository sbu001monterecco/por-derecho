(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const esCal = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const enCal = path.endsWith('/en/insolvency-classification-parallel-lives/');
  const esRec = path.endsWith('/es/objetivos-recuperacion-restitucion/');
  const enRec = path.endsWith('/en/recovery-restitution-objectives/');
  if (!esCal && !enCal && !esRec && !enRec) return;
  if (document.querySelector('[data-cal-recovery-adversity-20260816]')) return;

  const es = esCal || esRec;
  const cal = esCal || enCal;
  const c = es ? {
    kicker: 'RECUPERACIÓN A TRAVÉS DE LA ADVERSIDAD · AGENCIA DOCUMENTADA',
    title: 'La calificación es sólo una parte de la historia: mientras se nos acusaba, intentábamos conservar, financiar, explotar, proteger y recuperar el negocio.',
    lead: 'Esta cronología no afirma que cada intento tuviera éxito ni que el Concurso 36/2012 esté ya formalmente concluido. Muestra algo más básico y comprobable: qué actuaciones contemporáneas se realizaron para preservar actividad, valor, activos, ingresos y remedios mientras avanzaban la liquidación, la calificación y los conflictos de control/título.',
    rows: [
      ['2012', 'VIABILIDAD / PROTECCIÓN', 'La memoria de 1 de junio de 2012 ya sitúa la viabilidad en un convenio con acreedores. La secuencia art. 5 bis → concurso voluntario fue utilizada como vía de protección frente a la crisis y la ejecución, no como una declaración de abandono.', 'Documento contemporáneo · resultado futuro no presumido'],
      ['2012–2016', 'OPERAR / MANTENER / DOCUMENTAR', 'Sun Park continuó como realidad económica. El expediente contiene explotación, mantenimiento y producción contable/documental. La controversia posterior sobre suficiencia jurídica de la contabilidad no equivale a “no hubo actividad” ni “no se entregó nada”.', 'Hechos y fuentes repartidos por el expediente'],
      ['2017', 'CONVENIO + FINANCIACIÓN + OPERADOR', 'El plan de viabilidad de abril de 2017 dice que su objetivo era conservar la actividad y pagar acreedores; registra garantía/recapitalización de Aweswell, negociación de refinanciación y un arrendamiento de cinco años negociado con operador británico y operador local. Gmail de 2017 documenta además plan de negocio, term sheet, valoración, datos de crecimiento y trabajo con operadores/inversores.', 'Plan/negociaciones verificadas · proyecciones y cierres no presumidos'],
      ['2017–2018', 'PROTEGER ACTIVOS / CONTROL / REGISTRO', 'Mientras crecía el conflicto de acceso, control y liquidación, la correspondencia muestra recursos, avisos al Registro, revisión de servidumbres/ob rem, búsqueda de escrituras y actuaciones para impedir o impugnar consecuencias patrimoniales que se consideraban irreversibles.', 'Actividad jurídica contemporánea · validez final de cada objeción separada'],
      ['ENE 2019', 'SALIDA FINANCIADA DEL CONCURSO', 'La ampliación de DI 248 registra la afirmación contemporánea de que se estaban realizando actuaciones para concluir el concurso por la vía del antiguo art. 176 LC y que se había obtenido la financiación necesaria.', 'Registro primario de la afirmación · no equivale a probar cada escrito histórico como presentado'],
      ['2019', 'OPONERSE A LA CALIFICACIÓN', 'Gil/LPB no consintieron el relato AC/Fiscal: formularon oposición y ya entonces acusaron a la AC de faltar a la verdad en extremos materiales. La controversia actual no nació en 2026.', 'Oposición formal documentada'],
      ['2020–2023', 'DEUDA / VALOR / TÍTULO / RECURSO', 'Continuaron advertencias e impugnaciones sobre deuda, intereses, valor, perímetro de titularidad y realización; después de la Sentencia 163/2023 se interpusieron recursos de apelación.', 'Actuaciones documentadas · resultado de apelación pendiente/notificación no localizada'],
      ['2025–2026', 'PRESERVAR / TRAZAR / ESCALAR', 'La recuperación pasó también por preservar prueba y activar vías judiciales, Fiscalía, regulatorias, administrativas, profesionales y de fondos públicos. Los registros y remisiones acreditan actuación; no prueban por sí solos el fondo de las denuncias.', 'Registro/recepción ≠ mérito'],
      ['AHORA', 'CONCLUSIÓN + RESTITUCIÓN + INGRESOS + DAÑOS', 'El objetivo sigue siendo la conclusión legal del Concurso 36/2012 y, donde exista vía, recuperar/restaurar negocio, hotel, activos, derechos, ingresos/frutos y causas de acción; compensar daños no reversibles; y depurar responsabilidad actor por actor según prueba.', 'Objetivo vigente · cuantificación final y remedios dependen de prueba/jurisdicción']
    ],
    planes: [
      ['CONCURSAL · LPB', 'Masa, valor, ingresos, deuda, causas de acción y conclusión/restauración.'],
      ['EXTRACONCURSAL · MATKATOR / TERCEROS', 'Propiedad, posesión, acceso, uso, obras y frutos que no quedan absorbidos automáticamente por LPB.'],
      ['TRANSFRONTERIZO · AWESWELL', 'Capital, valor inversor, financiación, costes de recuperación y remedios que cruzan fronteras.']
    ],
    question: 'La prueba que ordena esta página',
    questionBody: '<strong>Mientras el relato de calificación hablaba de obstrucción, falta de colaboración o conducta culpable, ¿qué estaba haciendo contemporáneamente el mismo lado para salvar, financiar, operar, proteger o recuperar el negocio?</strong> Cada contraste debe resolverse con: acusación → actuación contemporánea → fuente primaria → conocimiento del actor → decisión judicial → estado de apelación → consecuencia de recuperación.',
    current: 'Lo que seguimos buscando',
    currentBody: 'Conclusión legal del concurso; restitución o recuperación de los activos y derechos que correspondan; hotel/business recovery cuando jurídicamente proceda; rendición de cuentas sobre explotación e ingresos; recuperación de frutos/ingresos demostrables; daños causalmente probados; corrección de efectos judiciales, documentales, registrales o administrativos que sigan operando; y responsabilidad civil, penal, regulatoria, disciplinaria o administrativa sólo donde sus elementos se acrediten de forma independiente.',
    guard: '<strong>Control de credibilidad:</strong> los planes, term sheets, proyecciones, estimaciones de daños y estructuras de recuperación prueban actividad, intención y programa de trabajo en la medida de su fuente; no se publican aquí como resultados cerrados, financiación ejecutada ni quantum adjudicado. La persistencia se demuestra por los actos, no por el adjetivo “heroico”.',
    recoveryBtn: 'Abrir objetivos de recuperación y restitución →',
    calBtn: 'Abrir auditoría de Calificación →',
    reciprocalTitle: 'La Calificación es un obstáculo de recuperación, no el final de la historia.',
    reciprocalBody: 'El hub de recuperación y la auditoría de Calificación deben leerse juntos. La Sentencia 163/2023 es materialmente adversa y está recurrida; la auditoría separa lo que aceptó, rechazó o estrechó, mientras esta página explica qué debe probarse, corregirse, restituirse, contabilizarse y compensarse para reconstruir la posición patrimonial legítima.'
  } : {
    kicker: 'RECOVERY THROUGH ADVERSITY · DOCUMENTED AGENCY',
    title: 'The classification is only one part of the story: while accusations were being made, we were trying to preserve, finance, operate, protect and recover the business.',
    lead: 'This chronology does not say every attempt succeeded or that Insolvency 36/2012 has already formally ended. It shows something more basic and testable: the contemporaneous steps taken to preserve activity, value, assets, income and remedies while liquidation, classification and control/title disputes were unfolding.',
    rows: [
      ['2012', 'VIABILITY / PROTECTION', 'The 1 June 2012 insolvency memorandum already identified a creditor arrangement as the viability route. The Article 5 bis → voluntary-insolvency sequence was used as a protective/restructuring route, not as a declaration of abandonment.', 'Contemporaneous document · future outcome not presumed'],
      ['2012–2016', 'OPERATE / MAINTAIN / DOCUMENT', 'Sun Park continued as an economic reality. The record contains operation, maintenance and accounting/document production. The later dispute over legal sufficiency of accounting is not the same as “no activity” or “nothing was delivered”.', 'Facts and sources distributed across the record'],
      ['2017', 'CONVENIO + FINANCE + OPERATOR', 'The April 2017 viability plan says its objectives were to preserve activity and pay creditors; it records Aweswell guarantee/recapitalisation, refinancing work and a negotiated five-year lease with a British tour operator and local operator. 2017 Gmail also documents business-plan, term-sheet, valuation, operating-growth and operator/investor work.', 'Plans/negotiations verified · projections and closings not presumed'],
      ['2017–2018', 'PROTECT ASSETS / CONTROL / REGISTRY', 'As access, control and liquidation conflicts intensified, correspondence shows appeals, Registry notices, servitude/ob-rem review, deed recovery and attempts to prevent or challenge patrimonial consequences regarded as irreversible.', 'Contemporaneous legal activity · final validity of each objection kept separate'],
      ['JAN 2019', 'FINANCED INSOLVENCY EXIT', 'The DI 248 expansion records the contemporaneous assertion that steps were being taken to conclude the insolvency under former Article 176 LC and that the necessary financing had been obtained.', 'Primary record of the assertion · not proof every historical draft was filed'],
      ['2019', 'OPPOSE THE CLASSIFICATION', 'Gil/LPB did not accept the AC/Fiscal narrative: they formally opposed it and already accused the AC of materially departing from the truth. The present dispute was not invented in 2026.', 'Formal opposition documented'],
      ['2020–2023', 'DEBT / VALUE / TITLE / APPEAL', 'Warnings and challenges continued on debt, interest, value, title perimeter and realisation; after Judgment 163/2023, appeals were filed.', 'Actions documented · appellate outcome pending/no terminating notification located'],
      ['2025–2026', 'PRESERVE / TRACE / ESCALATE', 'Recovery also moved through evidence preservation and judicial, prosecutorial, regulatory, administrative, professional and public-funds routes. Registrations and referrals prove action, not the merits of the underlying allegations.', 'Registration/receipt ≠ merits'],
      ['NOW', 'CONCLUSION + RESTITUTION + INCOME + DAMAGES', 'The objective remains lawful conclusion of Insolvency 36/2012 and, where a legal route exists, recovery/restoration of the business, hotel interests, assets, rights, income/fruits and causes of action; compensation for irreversible harm; and actor-specific accountability according to proof.', 'Current objective · final quantum/remedies depend on evidence and jurisdiction']
    ],
    planes: [
      ['INSOLVENCY · LPB', 'Estate, value, income, debt, causes of action and conclusion/restoration.'],
      ['EXTRA-INSOLVENCY · MATKATOR / THIRD PARTIES', 'Property, possession, access, use, works and fruits not automatically absorbed into LPB.'],
      ['CROSS-BORDER · AWESWELL', 'Capital, investor value, financing, recovery costs and cross-border remedies.']
    ],
    question: 'The test that organises this page',
    questionBody: '<strong>While the classification narrative spoke of obstruction, non-collaboration or culpable conduct, what was the same side contemporaneously doing to save, finance, operate, protect or recover the business?</strong> Each contrast should be resolved through: allegation → contemporaneous act → primary source → actor knowledge → judicial treatment → appeal status → recovery consequence.',
    current: 'What we are still seeking',
    currentBody: 'Lawful conclusion of the insolvency; restitution/recovery of assets and rights where available; hotel/business recovery where legally possible; accounting for exploitation and income; recovery of provable fruits/income; causally proved damages; correction of continuing judicial, documentary, registry or administrative effects; and civil, criminal, regulatory, disciplinary or administrative accountability only where the elements are independently evidenced.',
    guard: '<strong>Credibility control:</strong> plans, term sheets, projections, damages estimates and recovery structures prove activity, intention and programme only to the extent of their source; they are not published here as closed transactions, executed funding or adjudicated quantum. Persistence is shown by acts, not by the adjective “heroic”.',
    recoveryBtn: 'Open recovery and restitution objectives →',
    calBtn: 'Open the Classification evidence audit →',
    reciprocalTitle: 'The Classification is a recovery obstacle, not the end of the story.',
    reciprocalBody: 'The recovery hub and Classification audit should be read together. Judgment 163/2023 is materially adverse and appealed; the audit separates what it accepted, rejected or narrowed, while this page explains what must be proved, corrected, restored, accounted for and compensated to rebuild the lawful patrimonial position.'
  };

  const style = document.createElement('style');
  style.textContent = `
    .rta{padding:0 0 2.3rem}.rta-wrap{max-width:1080px;margin:0 auto}.rta-box{background:#fff;border:2px solid #365a49;border-radius:20px;padding:1.4rem;box-shadow:0 12px 34px rgba(19,37,45,.07)}
    .rta-kicker{font-size:.75rem;letter-spacing:.09em;text-transform:uppercase;font-weight:900;color:#526b59}.rta-box h2{font-size:clamp(1.75rem,3.8vw,2.55rem);line-height:1.07;margin:.4rem 0 .8rem}.rta-box h3{margin:1.1rem 0 .5rem}
    .rta-timeline{display:grid;gap:.65rem;margin:1rem 0}.rta-row{display:grid;grid-template-columns:95px 170px 1fr;gap:.85rem;border:1px solid rgba(19,37,45,.14);border-radius:14px;padding:.9rem;background:#fafaf8}.rta-year{font-weight:900}.rta-act{font-size:.78rem;font-weight:900;letter-spacing:.055em;text-transform:uppercase;color:#6b5841}.rta-status{display:block;font-size:.78rem;color:#666;margin-top:.35rem}
    .rta-planes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin:1rem 0}.rta-plane{background:#f3efe4;border-radius:14px;padding:1rem;border-top:4px solid #8c6b2f}.rta-plane strong{display:block;margin-bottom:.35rem}
    .rta-question{background:#10252e;color:#fff;border-radius:14px;padding:1rem 1.1rem}.rta-current{background:#edf1ed;border-left:5px solid #526b59;border-radius:14px;padding:1rem 1.1rem;margin-top:.8rem}.rta-guard{font-size:.9rem;color:#555;margin-top:.85rem}.rta-actions{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:1rem}
    .rta-recip{margin:1.2rem auto;max-width:1080px;background:#fff;border:1px solid rgba(19,37,45,.17);border-left:6px solid #526b59;border-radius:15px;padding:1.1rem 1.2rem}.rta-recip h2{margin:.2rem 0 .55rem}
    @media(max-width:820px){.rta-row{grid-template-columns:1fr}.rta-planes{grid-template-columns:1fr}.rta-box{border-radius:0}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.className = cal ? 'section rta' : 'section';
  section.dataset.calRecoveryAdversity20260816 = '1';

  if (cal) {
    const rows = c.rows.map(([y,a,b,s]) => `<article class="rta-row"><div class="rta-year">${y}</div><div class="rta-act">${a}</div><div>${b}<span class="rta-status">${s}</span></div></article>`).join('');
    const planes = c.planes.map(([h,b]) => `<article class="rta-plane"><strong>${h}</strong><span>${b}</span></article>`).join('');
    const recoveryHref = es ? '../objetivos-recuperacion-restitucion/' : '../recovery-restitution-objectives/';
    section.innerHTML = `<div class="shell rta-wrap"><div class="rta-box"><div class="rta-kicker">${c.kicker}</div><h2>${c.title}</h2><p>${c.lead}</p><div class="rta-timeline">${rows}</div><div class="rta-planes">${planes}</div><div class="rta-question"><h3>${c.question}</h3><p>${c.questionBody}</p></div><div class="rta-current"><h3>${c.current}</h3><p>${c.currentBody}</p></div><p class="rta-guard">${c.guard}</p><div class="rta-actions"><a class="button secondary" href="${recoveryHref}">${c.recoveryBtn}</a></div></div></div>`;
    const opening = document.querySelector('[data-calificacion-opening-20260816]');
    const hero = document.querySelector('.hero.cal-hero') || document.querySelector('main .hero');
    if (opening) opening.insertAdjacentElement('afterend', section);
    else if (hero) hero.insertAdjacentElement('afterend', section);
    return;
  }

  const calHref = es ? '../calificacion-concurso-36-2012-vidas-paralelas/' : '../insolvency-classification-parallel-lives/';
  section.innerHTML = `<div class="shell"><div class="rta-recip"><div class="rta-kicker">${c.kicker}</div><h2>${c.reciprocalTitle}</h2><p>${c.reciprocalBody}</p><a class="button secondary" href="${calHref}">${c.calBtn}</a></div></div>`;
  const hero = document.querySelector('.rr-hero') || document.querySelector('main .hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
})();

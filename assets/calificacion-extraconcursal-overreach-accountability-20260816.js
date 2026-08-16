(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const esPaths = new Set([
    '/por-derecho/es/calificacion-concurso-36-2012-vidas-paralelas/',
    '/por-derecho/es/concurso-36-2012-administrador-concursal/',
    '/por-derecho/es/concurso-36-2012-magistrado-juez/',
    '/por-derecho/es/concurso-36-2012-juzgado-mercantil-1/',
    '/por-derecho/es/concurso-36-2012-responsabilidad-institucional/',
    '/por-derecho/es/fiscalia-dip-2-2026/',
    '/por-derecho/es/toma-control-sun-park-7-junio-2018/',
    '/por-derecho/es/acosta-matos-perimetro/'
  ]);
  const enPaths = new Set([
    '/por-derecho/en/insolvency-classification-parallel-lives/',
    '/por-derecho/en/insolvency-36-2012-insolvency-administrator/',
    '/por-derecho/en/insolvency-36-2012-mercantile-court-1/',
    '/por-derecho/en/insolvency-36-2012-institutional-accountability/',
    '/por-derecho/en/fiscalia-dip-2-2026/',
    '/por-derecho/en/sun-park-takeover-7-june-2018/',
    '/por-derecho/en/acosta-matos-perimeter/'
  ]);

  const es = esPaths.has(path);
  const en = enPaths.has(path);
  if (!es && !en) return;
  if (document.querySelector('[data-extraconcursal-overreach-20260816]')) return;

  const d = es ? {
    eyebrow: '2018 · PERÍMETRO EXTRACONCURSAL · CONTROL MATERIAL · CALIFICACIÓN',
    title: 'El concurso era de LPB. El hotel entero no estaba en concurso.',
    lead: '<strong>Ésta es la distinción patrimonial que cambia la lectura causal.</strong> El Concurso 36/2012 afectaba a Luchy Playa Blanca, S.L.U. y a su patrimonio. Sun Park seguía siendo un hotel de titularidad y derechos fragmentados: bienes LPB, fincas de Matkator y terceros, elementos comunes y derechos de explotación con fuentes jurídicas distintas. Ser acreedor de LPB —o propietario de determinadas unidades— no convertía por sí solo a Construcciones Acosta Matos, S.A. en dueño o poseedor legal del hotel entero.',
    allegationTitle: 'ALEGACIÓN DE PARTE — FORMULADA CONTEMPORÁNEAMENTE',
    allegation: '<strong>LPB/Aweswell/Gil Marer sostienen que CAM protagonizó en junio de 2018 una toma de control clandestina, forzada y no autorizada, y la califican jurídicamente de ilícita/fraudulenta.</strong> Esa caracterización se publica como alegación, no como una condena o hecho penal ya declarado. Lo documentalmente relevante es que la disputa sobre posesión, cadenas, seguridad, accesos y exclusión aparece en comunicaciones de los días inmediatamente posteriores al 7 de junio, no como una teoría creada años después.',
    verifiedTitle: 'LO QUE EL REGISTRO YA OBLIGA A EXPLICAR',
    verified: [
      ['LPB ≠ HOTEL ENTERO', 'La masa de LPB no absorbía por arrastre las fincas de Matkator/terceros ni convertía toda la plataforma hotelera en patrimonio concursal.'],
      ['7 JUN 2018 · UMBRAL MATERIAL', 'El registro controlado soporta un cambio de control/acceso/seguridad de facto antes de la adjudicación formal de 2022. El alcance finca por finca sigue sujeto a prueba.'],
      ['25 JUN 2018 · CORREO DEL AC', '<strong>Un abogado dejó constancia contemporánea de que la contraparte utilizaba como soporte un correo de Francisco de Borja Rodríguez-Batllori Laffitte, Administrador Concursal, solicitando seguridad para el complejo.</strong> Esto no prueba por sí solo que el AC autorizara cada acto posterior, pero sitúa su intervención en el centro del análisis de autoridad y perímetro.'],
      ['VERSIÓN LIMITATIVA DE BORJA', 'También debe conservarse la evidencia contraria: un abogado informó que Borja sostenía que la seguridad había sido acordada por la Comunidad y que CAM sólo había entrado en sus propias unidades y zonas comunes, no en apartamentos de LPB. Esa versión debe contrastarse con actas, llaves, seguridad, policía, fincas y accesos.']
    ],
    keysTitle: 'LLAVES: UNA ALEGACIÓN IMPORTANTE QUE TODAVÍA EXIGE LA CADENA PRIMARIA',
    keys: '<strong>No afirmamos todavía como hecho verificado que Borja entregara físicamente “las llaves del hotel” a CAM.</strong> El registro sí conecta su petición de seguridad con la controversia de control y demuestra que la contraparte invocaba su correo. Falta cerrar la cadena: instrucciones del AC, contrato de seguridad, inventarios de llaves/códigos, cerrajero, autorizantes, guardias, CCTV, actas de Comunidad y atestados. Si esa cadena acredita una entrega o habilitación más amplia, la conclusión deberá actualizarse.',
    causationTitle: 'LA PREGUNTA QUE LA CALIFICACIÓN NO PUEDE SALTARSE',
    causation: '<strong>No se puede imputar automáticamente al deudor no hacer aquello que materialmente ya no podía controlar.</strong> Para cada acusación posterior al 7 de junio —deterioro, falta de explotación, ingresos, mantenimiento, acceso, documentación, rescate o agravación— hay que identificar quién tenía realmente las llaves, la seguridad, el acceso, el personal, la capacidad de operar y la posibilidad de producir o conservar la prueba. Y después separar qué perjuicio pertenecía a la masa de LPB y cuál era extraconcursal.',
    extraTitle: 'EL PERJUICIO EXTRACONCURSAL NO DESAPARECE DENTRO DEL CONCURSO',
    extra: 'Si un mecanismo nacido alrededor del concurso o de un acreedor de LPB afectó materialmente bienes de Matkator, unidades de terceros, derechos de explotación, recepción, sistemas comunes, clientes, reservas, personal, financiación o la posición inversora de Aweswell, ese perjuicio debe analizarse en su propio plano patrimonial. <strong>La alegación de desbordamiento consiste precisamente en que una autoridad limitada al patrimonio de LPB habría servido —por acción, tolerancia, error o falta de corrección, según se pruebe actor por actor— como puente práctico hacia un hotel jurídicamente más amplio.</strong>',
    actorsTitle: 'TRES RESPONSABILIDADES QUE NO DEBEN CONFUNDIRSE',
    actors: [
      ['ADMINISTRADOR CONCURSAL · FRANCISCO DE BORJA RODRÍGUEZ-BATLLORI LAFFITTE', '<strong>Debe explicarse el perímetro exacto de su petición de seguridad.</strong> ¿Qué pretendía proteger? ¿Quién recibió instrucciones? ¿Qué sabía de llaves, cerraduras, recepción, personal y fincas ajenas? Cuando su correo empezó a ser utilizado por la contraparte como soporte de su actuación, ¿limitó, corrigió, objetó o exigió restitución? La cuestión no es sólo si “sabía” del conflicto: es qué hizo para conservar la masa sin extender el control sobre derechos ajenos.'],
      ['FISCAL RICARDO DE MOSTEYRÍN SAMPALO · 12 MAR 2019', '<strong>Primero debe probarse qué material de junio/julio de 2018 estaba efectivamente ante Fiscalía.</strong> Si la evidencia del cambio de control y del perímetro extraconcursal estaba en el expediente, una posición adversa de Calificación que no confronte esa causalidad alternativa requiere explicación. Si no estaba, hay que identificar la ruptura de transmisión; no inventar conocimiento personal.'],
      ['MAGISTRADO ALBERTO LÓPEZ VILLARRUBIA · SENTENCIA 163/2023', '<strong>Debe reconstruirse qué prueba estaba en el expediente antes del 28 de septiembre de 2023.</strong> Si el tribunal disponía de la evidencia del control material y aun así atribuyó perjuicios posteriores a Gil/LPB/Pink sin reconciliar quién tenía capacidad real ni separar masa y derechos extraconcursales, ése es un problema concreto de motivación, causalidad y tutela a revisar en apelación e institucionalmente. Por sí solo no prueba prevaricación, corrupción ni connivencia.']
    ],
    testTitle: 'TEST DE DIEZ PREGUNTAS PARA CADA IMPUTACIÓN POSTERIOR AL 7 DE JUNIO',
    test: ['¿Qué bien o derecho estaba implicado?','¿Era masa LPB, bien de tercero, elemento común o derecho operativo?','¿Quién tenía título formal?','¿Quién tenía posesión jurídica?','¿Quién tenía llaves, seguridad y acceso material?','¿Quién podía realmente ejecutar la conducta exigida?','¿Qué hicieron CAM, Comunidad/seguridad y AC?','¿Qué prueba estaba ante Fiscal y juez en la fecha relevante?','¿Qué pérdida es concursal y cuál extraconcursal?','¿Qué explicación alternativa fue considerada y descartada?'],
    rule: '<strong>Regla de publicación:</strong> acreedor ≠ propietario del hotel; seguridad ≠ posesión ilimitada; control de facto ≠ título; adjudicación de 2022 ≠ autorización retroactiva; alegación de fraude ≠ hecho penal probado. Pero esas cautelas tampoco permiten borrar el hecho causal de que el control material cambió antes del título y que la intervención de seguridad del AC forma parte del expediente que debe explicarse.',
    source: 'Control documental: CALIFICACION_EXTRACONCURSAL_TAKEOVER_OVERREACH_AC_JUDGE_FISCAL_CONTROL_16AUG2026.md · P19_SUN_PARK_MATERIAL_CONTROL_POSSESSION_CONTINUITY_MEETING_POINT_15AUG2026.md · CR-018 / CR-042 · ME-063. Marco histórico: Ley 22/2003, arts. 43, 76 y 80. Fuentes contemporáneas de correo de junio/julio de 2018 preservadas en el registro privado.',
    links: [
      ['Dossier 7 junio 2018 →', '../toma-control-sun-park-7-junio-2018/'],
      ['Administrador Concursal →', '../concurso-36-2012-administrador-concursal/'],
      ['Magistrado / juez →', '../concurso-36-2012-magistrado-juez/'],
      ['Calificación →', '../calificacion-concurso-36-2012-vidas-paralelas/'],
      ['Fiscalía →', '../fiscalia-dip-2-2026/']
    ]
  } : {
    eyebrow: '2018 · EXTRACONCURSAL PERIMETER · MATERIAL CONTROL · CLASSIFICATION',
    title: 'LPB was in insolvency proceedings. The whole hotel was not.',
    lead: '<strong>This patrimonial distinction changes the causation analysis.</strong> Insolvency Proceeding 36/2012 concerned Luchy Playa Blanca, S.L.U. and its estate. Sun Park remained a hotel built across fragmented property and rights: LPB assets, Matkator/third-party property, common elements and operating rights with separate legal sources. Being LPB’s creditor — or owner of defined units — did not by itself make Construcciones Acosta Matos, S.A. owner or legal possessor of the whole hotel.',
    allegationTitle: 'PARTY ALLEGATION — MADE CONTEMPORANEOUSLY',
    allegation: '<strong>LPB/Aweswell/Gil Marer allege that CAM carried out a clandestine, forcible and unauthorised takeover/control in June 2018 and legally characterise it as unlawful/fraudulent.</strong> That characterisation is published as an allegation, not as an adjudicated criminal fact. What the contemporaneous record does establish is that possession, chains, security, access and exclusion were being disputed in communications immediately after 7 June, rather than being a theory created years later.',
    verifiedTitle: 'WHAT THE RECORD ALREADY REQUIRES TO BE EXPLAINED',
    verified: [
      ['LPB ≠ WHOLE HOTEL', 'LPB’s estate did not automatically absorb Matkator/third-party property or turn the whole hotel platform into insolvency-estate property.'],
      ['7 JUN 2018 · MATERIAL THRESHOLD', 'The controlled record supports a de facto material/access/security control shift before the formal 2022 adjudication. Exact asset-by-asset reach remains subject to proof.'],
      ['25 JUN 2018 · IA EMAIL', '<strong>Contemporaneous counsel recorded that the opposing side relied on an email from Francisco de Borja Rodríguez-Batllori Laffitte, the Insolvency Administrator, requesting security for the complex.</strong> This does not by itself prove that the IA authorised every subsequent act, but it places his intervention at the centre of the authority/perimeter analysis.'],
      ['BORJA’S LIMITING ACCOUNT', 'Adverse evidence must also remain visible: counsel reported that Borja said security had been approved by the Community and that CAM had entered only its own units and common areas, not LPB apartments. That account must be tested against minutes, keys, security, police, property and access evidence.']
    ],
    keysTitle: 'KEYS: AN IMPORTANT ALLEGATION THAT STILL REQUIRES THE PRIMARY CHAIN',
    keys: '<strong>We do not yet state as verified fact that Borja physically handed “the hotel keys” to CAM.</strong> The record does connect his security request to the control controversy and shows that the opposing side invoked his email. The missing chain is finite: IA instructions, security contract, key/code inventories, locksmith work, authorisers, guards, CCTV, Community records and police reports. If that chain proves a broader handover or enabling act, the conclusion must be updated.',
    causationTitle: 'THE QUESTION THE CLASSIFICATION CANNOT SKIP',
    causation: '<strong>A debtor cannot automatically be blamed for failing to do what it no longer had the material capacity to control.</strong> For every post-7-June allegation — deterioration, non-operation, income, maintenance, access, documents, rescue failure or aggravation — the analysis must identify who actually controlled keys, security, access, staff, operations and evidence. It must then separate loss to LPB’s estate from extraconcursal loss.',
    extraTitle: 'EXTRACONCURSAL HARM DOES NOT DISAPPEAR INSIDE THE INSOLVENCY',
    extra: 'If a mechanism arising around LPB’s insolvency or an LPB creditor materially affected Matkator property, third-party units, operating rights, reception, common systems, guests, bookings, staff, financing or Aweswell’s investor position, that harm requires its own patrimonial analysis. <strong>The alleged overreach is precisely that authority limited to LPB’s estate may have become — through action, tolerance, error or failure to correct, as each actor is proved — a practical bridge into a legally wider hotel.</strong>',
    actorsTitle: 'THREE RESPONSIBILITIES THAT MUST NOT BE COLLAPSED',
    actors: [
      ['INSOLVENCY ADMINISTRATOR · FRANCISCO DE BORJA RODRÍGUEZ-BATLLORI LAFFITTE', '<strong>The exact perimeter of his security request requires explanation.</strong> What was he trying to protect? Who received instructions? What did he know about keys, locks, reception, staff and third-party property? Once his email was being used by the opposing side to support its actions, did he limit, correct, object or seek restoration? The issue is not merely whether he knew there was a dispute; it is what he did to preserve the estate without extending control into other people’s rights.'],
      ['PROSECUTOR RICARDO DE MOSTEYRÍN SAMPALO · 12 MAR 2019', '<strong>First establish which June/July 2018 materials were actually before the prosecution.</strong> If the material-control and extraconcursal-perimeter evidence was in the file, an adverse classification position that did not confront that alternative causation requires explanation. If it was not, identify the transmission failure rather than invent personal knowledge.'],
      ['JUDGE ALBERTO LÓPEZ VILLARRUBIA · JUDGMENT 163/2023', '<strong>Reconstruct what evidence was in the record before 28 September 2023.</strong> If the court had the material-control evidence yet attributed later harm to Gil/LPB/Pink without reconciling actual capacity or separating estate and extraconcursal rights, that is a concrete reasoning, causation and effective-judicial-protection issue for appeal and institutional review. By itself it does not prove prevarication, corruption or collusion.']
    ],
    testTitle: 'TEN-QUESTION TEST FOR EVERY POST-7-JUNE ACCUSATION',
    test: ['What asset or right was involved?','Was it LPB estate property, third-party property, a common element or an operating right?','Who held formal title?','Who held legal possession?','Who controlled keys, security and material access?','Who could actually perform the conduct demanded?','What did CAM, Community/security and the IA do?','What evidence was before the Prosecutor and Judge at the relevant date?','Which loss is insolvency-estate loss and which is extraconcursal?','What alternative explanation was considered and rejected?'],
    rule: '<strong>Publication rule:</strong> creditor ≠ hotel owner; security ≠ unlimited possession; de facto control ≠ title; 2022 adjudication ≠ retroactive authority; fraud allegation ≠ proven criminal fact. But those safeguards do not permit the causal fact to be erased: material control changed before title, and the IA’s security intervention forms part of the record that must be explained.',
    source: 'Documentary control: CALIFICACION_EXTRACONCURSAL_TAKEOVER_OVERREACH_AC_JUDGE_FISCAL_CONTROL_16AUG2026.md · P19_SUN_PARK_MATERIAL_CONTROL_POSSESSION_CONTINUITY_MEETING_POINT_15AUG2026.md · CR-018 / CR-042 · ME-063. Historical framework: Insolvency Act 22/2003, arts. 43, 76 and 80. Contemporaneous June/July 2018 email sources are preserved in the private evidence record.',
    links: [
      ['7 June 2018 dossier →', '../sun-park-takeover-7-june-2018/'],
      ['Insolvency Administrator →', '../insolvency-36-2012-insolvency-administrator/'],
      ['Mercantile Court / Judge →', '../insolvency-36-2012-mercantile-court-1/'],
      ['Classification →', '../insolvency-classification-parallel-lives/'],
      ['Prosecution →', '../fiscalia-dip-2-2026/']
    ]
  };

  const section = document.createElement('section');
  section.className = 'section extraconcursal-overreach-panel';
  section.setAttribute('data-extraconcursal-overreach-20260816', '');
  section.innerHTML = `
    <div class="shell">
      <div class="section-head">
        <div><p class="kicker">${d.eyebrow}</p><h2>${d.title}</h2></div>
        <p>${d.lead}</p>
      </div>
      <aside class="eo-allegation"><span>${d.allegationTitle}</span><p>${d.allegation}</p></aside>
      <h3>${d.verifiedTitle}</h3>
      <div class="eo-grid eo-grid-4">${d.verified.map(([h,b]) => `<article><h4>${h}</h4><p>${b}</p></article>`).join('')}</div>
      <aside class="eo-keys"><h3>${d.keysTitle}</h3><p>${d.keys}</p></aside>
      <div class="eo-causal"><h3>${d.causationTitle}</h3><p>${d.causation}</p></div>
      <div class="eo-extra"><h3>${d.extraTitle}</h3><p>${d.extra}</p></div>
      <h3>${d.actorsTitle}</h3>
      <div class="eo-grid eo-grid-3">${d.actors.map(([h,b]) => `<article><h4>${h}</h4><p>${b}</p></article>`).join('')}</div>
      <div class="eo-test"><h3>${d.testTitle}</h3><ol>${d.test.map(x => `<li>${x}</li>`).join('')}</ol></div>
      <aside class="eo-rule">${d.rule}</aside>
      <p class="eo-source">${d.source}</p>
      <div class="actions">${d.links.map(([t,h]) => `<a class="button secondary" href="${h}">${t}</a>`).join('')}</div>
    </div>`;

  const style = document.createElement('style');
  style.textContent = `
    .extraconcursal-overreach-panel{border-block:1px solid rgba(138,108,53,.35);background:linear-gradient(180deg,rgba(138,108,53,.08),rgba(19,37,45,.02))}
    .extraconcursal-overreach-panel h3{margin-top:2rem}
    .eo-allegation,.eo-keys,.eo-rule{padding:1.15rem 1.25rem;margin:1.25rem 0;border:1px solid rgba(138,108,53,.45);border-radius:14px;background:rgba(255,248,233,.7)}
    .eo-allegation span{display:inline-block;font-weight:800;letter-spacing:.06em;font-size:.78rem;margin-bottom:.35rem}
    .eo-keys{border-color:rgba(136,61,45,.45);background:rgba(136,61,45,.07)}
    .eo-causal,.eo-extra{padding:1.3rem 0;border-top:1px solid rgba(19,37,45,.18)}
    .eo-grid{display:grid;gap:1rem;margin:1rem 0 1.75rem}
    .eo-grid article{padding:1.05rem;border:1px solid rgba(19,37,45,.16);border-radius:14px;background:rgba(255,255,255,.65)}
    .eo-grid h4{margin:.1rem 0 .5rem;font-size:.93rem;line-height:1.3}
    .eo-grid p{margin:0}
    .eo-test{padding:1.1rem 1.2rem;border-radius:14px;background:rgba(19,37,45,.06)}
    .eo-test ol{columns:2;column-gap:2.25rem;padding-left:1.25rem}
    .eo-test li{break-inside:avoid;margin:.4rem 0;padding-right:.5rem}
    .eo-source{font-size:.82rem;opacity:.75;margin-top:1rem}
    @media(min-width:760px){.eo-grid-4{grid-template-columns:repeat(2,minmax(0,1fr))}.eo-grid-3{grid-template-columns:repeat(3,minmax(0,1fr))}}
    @media(max-width:759px){.eo-test ol{columns:1}}
  `;
  document.head.appendChild(style);

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector('.dossier-hero, .page-hero, .hero');
  if (hero && hero.parentNode === main) hero.insertAdjacentElement('afterend', section);
  else main.insertAdjacentElement('afterbegin', section);
})();
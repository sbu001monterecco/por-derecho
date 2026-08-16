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
    kicker: 'CONTRARREGISTRO DOCUMENTAL · NORMALIZACIÓN COMERCIAL + EXPLOTACIÓN + REFINANCIACIÓN + SALIDA',
    title: 'No era un “rescate” de un hotel comercialmente muerto. Era una arquitectura para normalizar la explotación, financiar la salida y devolver a LPB capacidad empresarial.',
    lead: 'La calificación no puede evaluarse separando la renta, el hotel, la Comunidad, el control material, la financiación y la salida del concurso en expedientes mentales distintos. En junio de 2018 existía una estructura comercial desarrollada. La cuestión causal —por qué fue necesaria y por qué no llegó a materializarse— debe atribuirse actor por actor y no darse por demostrada de antemano.',
    items: [
      ['1 JUN 2012 · MEMORIA LPB', 'La propia memoria concursal identifica una vía de continuidad y pago a acreedores. La entrada en concurso no se presenta en esa fuente como abandono del negocio.'],
      ['29 MAR / 17 ABR 2017 · CONVENIO Y VIABILIDAD', 'Los documentos registran como objetivos conservar la actividad y satisfacer a acreedores, con garantía/recapitalización de Aweswell, refinanciación y estructura operativa/comercial.'],
      ['6 JUN 2018 · OPERADOR + SALIDA INTERCONECTADOS', 'Existe un contrato hotelero firmado. El instrumento facialmente identifica como partes a la Comunidad de Propietarios de Sun Park y Clubotel La Dorada, S.L.; la correspondencia de la operación describe a ONA como operador previsto y el contrato menciona OnaSystem. La adenda suspensiva vinculó la eficacia del contrato a ingresar en Mercantil nº1 fondos suficientes para que LPB saliera del concurso y a una resolución favorable de la Junta de propietarios.'],
      ['8 JUN 2018 · PAQUETE PROFESIONAL', 'La correspondencia financiera reúne plan de negocio, due diligence de Cuatrecasas, tasación ECO presentada en la operación en aproximadamente 25,6 M€, garantías, financiación puente en estructuración y una alternativa de adquisición de 26 M€ atribuida a la SOCIMI Elaia. Es prueba de trabajo comercial desarrollado, no de que todos los instrumentos estuvieran cerrados.'],
      ['12 JUN 2018 · FINANCIACIÓN AVANZADA, PERO CONDICIONADA', 'Stoneweg llamó al adjunto “Oferta Vinculante”; el documento primario se titula “Oferta Vinculante Condicionada”, emitida por Varia Structured Opportunities a Aweswell. Contemplaba hasta 15,5 M€, con 13,84 M€ para deuda concursal/contra la masa, pero dependía, entre otras condiciones, de autorización judicial para hipotecas, certificado de deuda de la AC, tasación/DD y aprobación interna del financiador.'],
      ['13 JUN 2018 · JUZGADO + AC', 'El relato contemporáneo de Daniel Irigoyen dice que expuso al Juez una vía coordinada entre fondo, socio/sociedad y explotadora para concluir el concurso pagando la deuda, y después la trató con la AC. Según ese relato, el Juez permitió explorarla y pidió presentar la solicitud. Es evidencia profesional contemporánea, no acta judicial ni prueba de que cada anexo fuera formalmente incorporado.'],
      ['12 FEB 2019 · CONTINUIDAD DEL OPERADOR', 'Una adenda firmada al contrato de junio muestra que la relación seguía siendo trabajada. Registra entonces un complejo deteriorado/sin actividad hotelera y la disposición de Clubotel La Dorada a invertir un mínimo de 1 M€ antes de la posesión. El documento acredita la condición descrita; no establece quién causó el deterioro.'],
      ['2019–2026 · OPOSICIÓN, APELACIÓN Y RECUPERACIÓN', 'La oposición formal, los recursos, las objeciones sobre deuda/valor/título y las vías de preservación y recuperación muestran continuidad de actuación. Deben leerse junto a la acusación, no como inmunidad frente a cualquier reproche adverso.']
    ],
    thesis: 'La pregunta unitaria que debe responderse',
    thesisBody: '<strong>¿Qué ocurrió con una arquitectura comercial cuya ejecución dependía parcialmente de actuaciones del Juzgado y de la AC —incluidas autorización hipotecaria, cifra/certificación de deuda y tratamiento procesal— mientras el mismo hotel sufría un conflicto simultáneo de Comunidad, acceso, seguridad y control material?</strong> Gil Marer alega que la necesidad de esa estructura extraordinaria derivó de la interferencia de actores privados, la disfunción de gobierno/comunidad, decisiones de la AC y tratamiento judicial. La existencia de la estructura está documentada; esa causalidad y el fracaso de cierre deben demostrarse actor por actor.',
    boundary: '<strong>Límites obligatorios:</strong> no afirmar que LPB contrató facialmente directamente con ONA cuando el documento firmado nombra Comunidad + Clubotel La Dorada; no convertir a Clubotel y ONA en una sola entidad sin fuente; no llamar a la oferta VSO financiación incondicional o ya desembolsada; no afirmar que todos los documentos se presentaron al Juez sin LexNET/asiento; no atribuir a nadie la causa del deterioro de febrero de 2019 sólo por la adenda; no convertir el permiso reportado del Juez para explorar la salida en prueba de que la operación debía aprobarse.',
    status: 'Estado de fuente y siguiente prueba',
    statusBody: 'Ya están bajo control el contrato de 6-Jun, su adenda suspensiva, la correspondencia del paquete de 8-Jun, la oferta VSO de 12-Jun, el relato de Irigoyen de 13-Jun y la adenda de operador de 12-Feb-2019. Siguen abiertos: relación jurídica ONA↔Clubotel; autoridad real de la Comunidad y anexos finca/licencia; aceptación/comité/desembolso VSO; certificado de deuda AC; escrito exacto presentado tras el 13-Jun, anexos, proveído y exigencia de depósito/garantía; y comunicaciones que expliquen por qué no cerró la estructura.'
  } : {
    kicker: 'DOCUMENTARY COUNTER-RECORD · COMMERCIAL NORMALISATION + OPERATION + REFINANCING + EXIT',
    title: 'This was not a “rescue” of a commercially dead hotel. It was an architecture intended to normalise operation, finance exit and restore LPB’s business capacity.',
    lead: 'The classification cannot fairly separate rent, the hotel, the Community, material control, finance and insolvency exit into disconnected analytical files. By June 2018 a developed commercial structure existed. The causal question — why it became necessary and why it did not complete — must be allocated actor by actor rather than assumed in advance.',
    items: [
      ['1 JUN 2012 · LPB MEMORANDUM', 'The insolvency memorandum itself identifies a continuity and creditor-payment route. In that source, entry into insolvency is not presented as abandonment of the business.'],
      ['29 MAR / 17 APR 2017 · CONVENIO AND VIABILITY', 'The documents record preservation of activity and creditor satisfaction as objectives, with Aweswell guarantee/recapitalisation, refinancing and an operating/commercial structure.'],
      ['6 JUN 2018 · OPERATOR + EXIT INTERLOCKED', 'A signed hotel-industry lease exists. Facially, the legal parties are the Sun Park Owners’ Community and Clubotel La Dorada, S.L.; transaction correspondence described ONA as the intended operator and the contract refers to OnaSystem. The signed suspensive addendum linked effectiveness to sufficient money being paid into Mercantil nº1 to permit LPB to leave insolvency and to a favourable owners’ resolution.'],
      ['8 JUN 2018 · PROFESSIONAL TRANSACTION STACK', 'Finance correspondence brings together a business plan, Cuatrecasas due diligence, an ECO valuation presented in the transaction at about €25.6m, security, bridge-finance structuring and a separate €26m acquisition route attributed to SOCIMI Elaia. This is evidence of developed commercial work, not proof every instrument had closed.'],
      ['12 JUN 2018 · ADVANCED, BUT CONDITIONAL FINANCE', 'Stoneweg described the attachment as an “Oferta Vinculante”; the primary instrument is titled “Oferta Vinculante Condicionada”, issued by Varia Structured Opportunities to Aweswell. It contemplated up to €15.5m, including €13.84m for insolvency/estate debt, but depended among other conditions on judicial mortgage authority, an AC debt certificate, valuation/DD and lender internal approval.'],
      ['13 JUN 2018 · COURT + AC', 'Daniel Irigoyen’s contemporaneous account says he presented a route coordinating fund, shareholder/company and operator to conclude the insolvency by paying debt, then discussed it with the AC. According to his account, the Judge allowed the route to be explored and requested an application. This is contemporaneous professional evidence, not judicial minutes or proof every attachment was formally lodged.'],
      ['12 FEB 2019 · OPERATOR CONTINUITY', 'A signed addendum to the June contract shows the operator structure continued to be worked. It records a then deteriorated/non-operating complex and Clubotel La Dorada’s willingness to invest at least €1m before possession. The document proves the condition described; it does not establish who caused the deterioration.'],
      ['2019–2026 · OPPOSITION, APPEAL AND RECOVERY', 'Formal opposition, appeals, debt/value/title objections and preservation/recovery routes show continuing action. They must be read beside the accusation, not treated as immunity from every adverse finding.']
    ],
    thesis: 'The unitary question that now has to be answered',
    thesisBody: '<strong>What happened to a commercial architecture whose performance depended partly on court and AC outputs — including mortgage authority, debt certification/quantification and procedural treatment — while the same hotel was simultaneously affected by Community, access, security and material-control conflict?</strong> Gil Marer alleges that the need for this extraordinary structure arose from private-actor interference, Community/governance dysfunction, AC decisions and judicial handling. The existence of the structure is documented; that causation and the failure to close must be proved actor by actor.',
    boundary: '<strong>Mandatory boundaries:</strong> do not say LPB facially contracted directly with ONA when the signed instrument names Community + Clubotel La Dorada; do not merge Clubotel and ONA without a source; do not describe the VSO offer as unconditional or already drawn; do not say every document was filed with the Judge without LexNET/docket proof; do not assign the cause of the February-2019 deterioration from the addendum alone; and do not convert the reported judicial permission to explore exit into proof that the transaction had to be approved.',
    status: 'Source status and next proof',
    statusBody: 'Now controlled: the 6-Jun contract and suspensive addendum, 8-Jun package correspondence, 12-Jun VSO offer, Irigoyen’s 13-Jun account and 12-Feb-2019 operator addendum. Still open: ONA↔Clubotel legal relationship; actual Community authority and finca/licence annexes; VSO acceptance/committee/drawdown; AC debt certificate; exact post-13-Jun filing, annexes, court order and deposit/guarantee requirement; and communications explaining why the structure did not complete.'
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
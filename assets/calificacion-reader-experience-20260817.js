(() => {
  'use strict';

  const route = window.location.pathname.replace(/\/+$/, '') + '/';
  const isEs = route.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const isEn = route.endsWith('/en/insolvency-classification-parallel-lives/');
  if (!isEs && !isEn) return;

  const main = document.querySelector('main');
  if (!main) return;

  const t = isEs ? {
    gatewayEyebrow: 'LECTURA GUIADA · 30 SEGUNDOS / 90 SEGUNDOS / EXPEDIENTE',
    gatewayTitle: 'Primero: qué decidió la sentencia. Después: qué prueba cada acusación.',
    gatewayLead: 'La página conserva la acusación completa, pero ordena la lectura para que una persona que llega desde LinkedIn pueda distinguir inmediatamente la decisión adversa, lo rechazado o estrechado, el estado de apelación, la prueba contraria y el umbral de conocimiento atribuido a cada actor.',
    status: [
      ['Primera instancia', 'Sentencia 163/2023 · materialmente adversa'],
      ['Apelación', 'RPL 2523/2025 · sin resolución terminal localizada en el corpus controlado'],
      ['Auditoría serial', 'A01–A05 completas · A06 es la siguiente unidad'],
      ['Fuente central', 'Informe AC de 47 páginas leído y cruzado íntegramente']
    ],
    cards: [
      ['Lo adverso', 'La sentencia declaró culpable el concurso de LPB e impuso consecuencias personales y patrimoniales graves. La página no lo oculta.'],
      ['Lo que no validó', 'La misma sentencia rechazó, corrigió o redujo ramas materiales del paquete AC/Fiscal. No existe una validación judicial unitaria de todo lo alegado.'],
      ['La pregunta central', 'Para pasar de error a falsedad consciente o prevaricación hay que probar: conclusión exacta → documento contrario → transmisión → conocimiento → tratamiento u omisión.']
    ],
    nav: [
      ['Resultado exacto', '#canonical-calificacion-map'],
      ['Lectura de 90 segundos', '#calificacion-professional-read'],
      ['Auditorías A01–A06', '#calificacion-serial-index'],
      ['Prueba ante el actor', '#evidence-before-actor'],
      ['Acusación al Magistrado', '#judge-accusation'],
      ['Contexto conectado', '#calificacion-wider-context'],
      ['Correcciones', '#what-would-change-our-view']
    ],
    direct: 'La acusación permanece íntegra y visible. La mejora consiste en hacer que el lector llegue a ella después de ver la arquitectura probatoria, no en rebajarla.',
    serialEyebrow: 'AUDITORÍA SERIAL · ÍNDICE DE NAVEGACIÓN',
    serialTitle: 'Seis unidades distintas: no mezclar lo rechazado, lo estrechado y lo que sigue adverso',
    serialLead: 'Cada tarjeta conserva el hecho adverso más fuerte, el tratamiento judicial y la evidencia todavía abierta. Las auditorías completas A01–A04 están debajo en formato desplegable; A05 está completada en el registro canónico y A06 es la siguiente unidad.',
    serial: [
      ['A01', 'Colaboración', 'CONTRADICHA / ESTRECHADA', 'La ausencia global de cooperación no sobrevive intacta; permanece una cuestión documental más estrecha y recurrida.', '#audit-a01'],
      ['A02', 'Créditos frente a terceros', 'CAUSALIDAD AMPLIA RECHAZADA', 'El salto desde saldos de cobro incierto hasta salida del concurso fue rechazado; queda una cuestión soporte-documental.', '#audit-a02'],
      ['A03', 'PINK · renta · explotación', 'ADVERSA / RECURRIDA', 'Celebrar el contrato no fue declarado culpable; el impago, la falta de reclamación, causalidad y complicidad sí quedaron adversos.', '#audit-a03'],
      ['A04', 'Contabilidad', 'ADVERSA / RECURRIDA', 'Existía material contable; el pronunciamiento adverso se concentra en el Libro Diario estatutario durante el concurso.', '#audit-a04'],
      ['A05', 'Cobros exteriores / connivencia', 'RECHAZADA · TRAZA ABIERTA', 'El alzamiento fue rechazado; sigue abierta la ruta real cliente → procesador → banco → aplicación económica.', '#canonical-calificacion-map'],
      ['A06', 'Depósito de €19.140,25', 'SIGUIENTE AUDITORÍA', 'Rama rechazada en primera instancia; debe auditarse separadamente sin fusionarla con A05.', '#canonical-calificacion-map']
    ],
    evidenceEyebrow: 'MATRIZ CENTRAL · EVIDENCIA ANTE EL ACTOR',
    evidenceTitle: 'La diferencia entre que un documento exista y que una persona pueda demostrarse conocedora de él',
    evidenceLead: 'La acusación más grave depende de este puente. La tabla no convierte custodia institucional en lectura personal y no convierte una incompatibilidad documental en delito sin acreditar el elemento subjetivo.',
    gradeLabels: [
      ['PROBADO ANTE EL ACTOR', 'Existe un puente documental directo suficiente.'],
      ['INFERENCIA FUERTE DE TRANSMISIÓN', 'Un registro contemporáneo atribuye comunicación directa, pero falta certificación oficial completa.'],
      ['SÓLO DISPONIBLE INSTITUCIONALMENTE', 'Constaba en el expediente o institución; no se presume lectura personal.'],
      ['TODAVÍA NO PROBADO', 'No se ha localizado un puente de transmisión suficiente.']
    ],
    evidenceHeaders: ['Proposición discutida', 'Fuente contraria o de control', 'AC', 'Fiscalía', 'Magistrado / Juzgado', 'Límite actual'],
    evidenceRows: [
      ['La formulación global de “no colaboración”', 'Los propios informes AC reconocen asistencia, respuestas, diarios PDF, balances y material económico/operativo.', 'PROBADO ANTE EL ACTOR', 'PROBADO: el informe AC fue formalmente trasladado en la sección sexta', 'PROBADO: el informe integraba el expediente y la sentencia trató la cuestión', 'No prueba que cada entrega fuera puntual o jurídicamente suficiente; sí impide describir una ausencia simple de cooperación.'],
      ['Arquitectura de salida y normalización de junio de 2018', 'Instrumentos de operador, financiación condicionada, garantías, tasación, due diligence y relatos contemporáneos de Irigoyen y Carlos Sanz.', 'INFERENCIA FUERTE: Irigoyen registra reunión directa con la AC', 'TODAVÍA NO PROBADO', 'INFERENCIA FUERTE: Irigoyen registra reunión directa; no existe todavía acta judicial ni prueba de lectura de cada anexo', 'Prueba actividad y aviso contemporáneo; no prueba cierre, desembolso ni presentación formal de todo el paquete.'],
      ['Convenio, viabilidad y plan de pagos de 2017', 'Acuse LexNET de 27 de abril de 2017.', 'TODAVÍA NO PROBADO proposición por proposición', 'TODAVÍA NO PROBADO', 'SÓLO DISPONIBLE INSTITUCIONALMENTE: presentación formal al órgano judicial; lectura personal no presumida', 'La presentación formal contradice abandono simple, pero no demuestra aceptación judicial ni viabilidad final.'],
      ['Vida externa CAM/RICPE del hotel antes de 2023', 'Reposición de 4 de febrero de 2021 y diligencia de 17 de febrero, registro 918/2021.', 'TODAVÍA NO PROBADO', 'TODAVÍA NO PROBADO', 'SÓLO DISPONIBLE INSTITUCIONALMENTE: la cuestión entró en el procedimiento; lectura de cada anexo no probada', 'Sirve para capacidad, contexto y causalidad; no prueba por sí sola la verdad de cada alegación RICPE/CAM.']
    ],
    evidenceBoundary: '<strong>Regla:</strong> disponibilidad institucional ≠ conocimiento personal. Error o valoración discutible ≠ prevaricación. La acusación de Gil se fortalece únicamente donde el puente documental permite demostrar conocimiento suficiente de la realidad contraria.',
    contextEyebrow: 'CONTEXTO CONECTADO · DESPLEGABLE',
    contextTitle: 'Control material, CGPJ, CaixaBank, elEconomista y múltiples vidas financieras',
    contextLead: 'Estas capas son relevantes, pero no deben impedir que el lector comprenda primero el resultado de la calificación y su prueba central. Se preservan completas en este expediente desplegable y en sus páginas específicas.',
    contextSummary: 'Abrir el contexto conectado completo',
    correctionEyebrow: 'CORRECCIÓN · RÉPLICA · FALSABILIDAD',
    correctionTitle: 'Qué podría cambiar esta evaluación',
    correctionLead: 'Por Derecho modificará, limitará o retirará una conclusión cuando una fuente primaria suficiente demuestre que:',
    correctionItems: [
      'un documento contrario atribuido a un actor no estaba realmente en su poder ni en el expediente pertinente;',
      'una trazabilidad bancaria o de pagos acredita una ruta actualmente tratada como no probada;',
      'el acta, grabación o testimonio certificado de la vista altera materialmente la reconstrucción publicada;',
      'una resolución de apelación modifica o revoca el tratamiento de primera instancia;',
      'una explicación documental lícita resuelve una incompatibilidad actualmente abierta;',
      'una identidad, fecha, cantidad, entidad o situación procesal publicada es incorrecta.'
    ],
    replyTitle: 'Correcciones y derecho de respuesta',
    replyBody: 'Toda persona, entidad u organismo identificado puede señalar la proposición exacta cuestionada, proponer su corrección y aportar la fuente primaria correspondiente. Una discrepancia interpretativa se publicará como respuesta, no como corrección factual. Las correcciones verificadas deben quedar fechadas y versionadas.',
    replyLink: 'Enviar corrección documentada',
    footer: 'Actualizado 17 de agosto de 2026 · lectura y composición UX revisadas.'
  } : {
    gatewayEyebrow: 'GUIDED READING · 30 SECONDS / 90 SECONDS / FULL RECORD',
    gatewayTitle: 'First: what the judgment decided. Then: what each allegation can prove.',
    gatewayLead: 'The page preserves the complete allegation while ordering the reading so that a visitor arriving from LinkedIn can immediately distinguish the adverse judgment, what was rejected or narrowed, the appeal status, contrary evidence and the knowledge threshold attributed to each actor.',
    status: [
      ['First instance', 'Judgment 163/2023 · materially adverse'],
      ['Appeal', 'RPL 2523/2025 · no terminating decision located in the controlled corpus'],
      ['Serial audit', 'A01–A05 complete · A06 is the next unit'],
      ['Core source', 'The AC’s 47-page report has been read and fully cross-walked']
    ],
    cards: [
      ['The adverse result', 'The judgment declared LPB’s insolvency culpable and imposed serious personal and financial consequences. The page does not conceal that.'],
      ['What it did not validate', 'The same judgment rejected, corrected or narrowed material branches of the AC/Fiscal package. There was no unitary judicial validation of everything alleged.'],
      ['The central question', 'Moving from error to knowing falsehood or prevarication requires proof of: exact finding → contrary document → transmission → knowledge → treatment or omission.']
    ],
    nav: [
      ['Exact result', '#canonical-calificacion-map'],
      ['90-second read', '#calificacion-professional-read'],
      ['A01–A06 audits', '#calificacion-serial-index'],
      ['Evidence before actor', '#evidence-before-actor'],
      ['Accusation against Judge', '#judge-accusation'],
      ['Connected context', '#calificacion-wider-context'],
      ['Corrections', '#what-would-change-our-view']
    ],
    direct: 'The accusation remains complete and visible. The improvement is to bring the reader to it after the evidential architecture has been shown, not to dilute it.',
    serialEyebrow: 'SERIAL AUDIT · NAVIGATION INDEX',
    serialTitle: 'Six distinct units: do not merge what was rejected, narrowed and what remains adverse',
    serialLead: 'Each card preserves the strongest adverse fact, judicial treatment and evidence still open. The full A01–A04 audits appear below as expandable records; A05 is complete in the canonical record and A06 is the next unit.',
    serial: [
      ['A01', 'Collaboration', 'CONTRADICTED / NARROWED', 'The global absence-of-cooperation account does not survive intact; a narrower document issue remains appealed.', '#audit-a01'],
      ['A02', 'Third-party receivables', 'BROAD CAUSATION REJECTED', 'The leap from uncertain receivables to insolvency exit was rejected; a narrower support-document issue remains.', '#audit-a02'],
      ['A03', 'PINK · rent · operation', 'ADVERSE / APPEALED', 'Entering the contract was not held culpable; nonpayment, non-recovery, causation and complicity remained adverse.', '#audit-a03'],
      ['A04', 'Accounting', 'ADVERSE / APPEALED', 'Accounting material existed; the adverse finding focuses on the statutory Daily Journal during insolvency.', '#audit-a04'],
      ['A05', 'Overseas receipts / collusion', 'REJECTED · TRACE OPEN', 'The concealment branch was rejected; the actual customer → processor → bank → economic-application route remains open.', '#canonical-calificacion-map'],
      ['A06', '€19,140.25 deposit', 'NEXT AUDIT', 'Rejected at first instance; it must be audited separately rather than merged into A05.', '#canonical-calificacion-map']
    ],
    evidenceEyebrow: 'CENTRAL MATRIX · EVIDENCE BEFORE THE ACTOR',
    evidenceTitle: 'The difference between a document existing and proving that a person knew it',
    evidenceLead: 'The most serious allegation depends on this bridge. The table does not convert institutional custody into personal reading or a documentary incompatibility into an offence without evidence of the subjective element.',
    gradeLabels: [
      ['PROVED BEFORE ACTOR', 'A sufficient direct documentary bridge exists.'],
      ['STRONG TRANSMISSION INFERENCE', 'A contemporaneous record attributes direct communication, but complete official certification is absent.'],
      ['INSTITUTIONALLY AVAILABLE ONLY', 'It was in the institutional or court record; personal reading is not presumed.'],
      ['NOT YET PROVED', 'No sufficient transmission bridge has been located.']
    ],
    evidenceHeaders: ['Disputed proposition', 'Contrary/control source', 'AC', 'Fiscalía', 'Judge / Court', 'Present boundary'],
    evidenceRows: [
      ['The global “non-collaboration” portrayal', 'The AC’s own reports acknowledge attendance, responses, PDF journals, trial balances and economic/operating material.', 'PROVED BEFORE ACTOR', 'PROVED: the AC report was formally transferred in the classification section', 'PROVED: the report formed part of the record and the judgment treated the issue', 'This does not prove every delivery was timely or legally sufficient; it prevents a simple absence-of-cooperation portrayal.'],
      ['June 2018 exit and commercial-normalisation architecture', 'Operator instruments, conditional finance, security, valuation, due diligence and the contemporaneous Irigoyen/Carlos Sanz accounts.', 'STRONG INFERENCE: Irigoyen records a direct AC meeting', 'NOT YET PROVED', 'STRONG INFERENCE: Irigoyen records a direct meeting; no judicial minute or proof of reading every annex', 'It proves activity and contemporaneous notice, not closing, drawdown or formal filing of the full package.'],
      ['2017 arrangement, viability and payment plans', '27 April 2017 LexNET acknowledgement.', 'NOT YET PROVED proposition by proposition', 'NOT YET PROVED', 'INSTITUTIONALLY AVAILABLE ONLY: formally filed with the court; personal reading is not presumed', 'Formal filing contradicts simple abandonment, but does not prove judicial acceptance or final viability.'],
      ['CAM/RICPE external hotel project before 2023', '4 February 2021 reposición and 17 February registry action 918/2021.', 'NOT YET PROVED', 'NOT YET PROVED', 'INSTITUTIONALLY AVAILABLE ONLY: the issue entered the proceeding; reading of each annex is unproved', 'Relevant to capacity, context and causation; it does not itself prove every CAM/RICPE allegation.']
    ],
    evidenceBoundary: '<strong>Rule:</strong> institutional availability ≠ personal knowledge. Error or disputed evaluation ≠ prevarication. Gil’s accusation becomes stronger only where the documentary bridge can establish sufficient knowledge of the contrary reality.',
    contextEyebrow: 'CONNECTED CONTEXT · EXPANDABLE',
    contextTitle: 'Material control, CGPJ, CaixaBank, elEconomista and multiple financial lives',
    contextLead: 'These layers matter, but they should not prevent the reader from first understanding the classification result and its central evidence. They remain complete in this expandable record and on their dedicated pages.',
    contextSummary: 'Open the complete connected context',
    correctionEyebrow: 'CORRECTION · REPLY · FALSIFIABILITY',
    correctionTitle: 'What could change this assessment',
    correctionLead: 'Por Derecho will amend, narrow or withdraw a conclusion where sufficient primary evidence demonstrates that:',
    correctionItems: [
      'contrary material attributed to an actor was not actually received or present in the relevant record;',
      'bank or payment tracing establishes a route presently treated as unproved;',
      'the certified hearing record materially changes the published reconstruction;',
      'an appellate judgment changes or reverses the first-instance treatment;',
      'a lawful documentary explanation resolves a presently open incompatibility;',
      'a published identity, date, amount, entity or procedural status is incorrect.'
    ],
    replyTitle: 'Corrections and right of reply',
    replyBody: 'Every identified person, entity or institution may identify the exact proposition disputed, propose a correction and provide the relevant primary source. A disagreement of interpretation will be published as a response rather than a factual correction. Verified corrections should be dated and versioned.',
    replyLink: 'Send a documented correction',
    footer: 'Updated 17 August 2026 · reading order and UX composition reviewed.'
  };

  let applying = false;
  let settleTimer = null;

  const topBlock = (node) => {
    if (!node) return null;
    let el = node;
    while (el.parentElement && el.parentElement !== main) el = el.parentElement;
    return el.parentElement === main ? el : null;
  };

  const block = (selector) => topBlock(document.querySelector(selector));

  const blockByHeading = (...terms) => {
    const lowered = terms.map((term) => term.toLowerCase());
    return [...main.children].find((child) => {
      if (!child.matches('section,details')) return false;
      if (child.id === 'calificacion-reader-gateway' || child.id === 'calificacion-wider-context') return false;
      const heading = child.querySelector('h2');
      const text = (heading?.textContent || '').toLowerCase();
      return lowered.some((term) => text.includes(term));
    }) || null;
  };

  const ensureStyle = () => {
    if (document.getElementById('calificacion-reader-experience-style')) return;
    const style = document.createElement('style');
    style.id = 'calificacion-reader-experience-style';
    style.textContent = `
      html{scroll-behavior:smooth}
      #calificacion-reader-gateway,#calificacion-serial-index,#evidence-before-actor,#what-would-change-our-view,#judge-accusation,#calificacion-professional-read,#calificacion-wider-context{scroll-margin-top:5rem}
      .cal-ux-gateway{background:#10252e;color:#fff;padding:2rem 0 2.3rem;border-top:1px solid rgba(255,255,255,.12)}
      .cal-ux-wrap{max-width:1080px;margin:0 auto}
      .cal-ux-eyebrow{font-size:.76rem;letter-spacing:.09em;text-transform:uppercase;font-weight:900;color:#d7c38d;margin:0 0 .45rem}
      .cal-ux-gateway h2{font-size:clamp(1.85rem,4vw,2.85rem);line-height:1.06;margin:.25rem 0 .75rem;color:#fff}
      .cal-ux-lead{font-size:1.04rem;line-height:1.62;max-width:970px;color:#e7edef}
      .cal-ux-status{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem;margin:1.15rem 0}
      .cal-ux-status div{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.18);border-radius:14px;padding:.85rem}
      .cal-ux-status strong{display:block;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:#dcc99a;margin-bottom:.3rem}
      .cal-ux-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin:1rem 0}
      .cal-ux-card{background:#fff;color:#13252d;border-radius:15px;padding:1rem;border-top:5px solid #8c6b2f}
      .cal-ux-card strong{display:block;margin-bottom:.38rem}
      .cal-ux-nav{position:sticky;top:.45rem;z-index:20;display:flex;gap:.45rem;overflow-x:auto;padding:.65rem;margin:1rem 0;background:rgba(16,37,46,.96);border:1px solid rgba(255,255,255,.2);border-radius:14px;backdrop-filter:blur(8px)}
      .cal-ux-nav a{flex:0 0 auto;color:#fff;text-decoration:none;border:1px solid rgba(255,255,255,.34);border-radius:999px;padding:.48rem .72rem;font-size:.82rem;font-weight:800}
      .cal-ux-nav a:hover,.cal-ux-nav a:focus-visible{background:#fff;color:#13252d;outline:none}
      .cal-ux-direct{margin:1rem 0 0;padding:.85rem 1rem;border-left:5px solid #d7c38d;background:rgba(255,255,255,.08);border-radius:12px;color:#fff}
      .cal-ux-section{padding:2.5rem 0;background:#f5f3ed}
      .cal-ux-section.alt{background:#fff}
      .cal-ux-section h2{font-size:clamp(1.65rem,3.5vw,2.45rem);line-height:1.1;margin:.25rem 0 .7rem}
      .cal-ux-serial-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin:1rem 0}
      .cal-ux-serial-card{display:block;background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:15px;padding:1rem;text-decoration:none;color:#13252d;border-top:5px solid #13252d}
      .cal-ux-serial-card:hover,.cal-ux-serial-card:focus-visible{transform:translateY(-2px);box-shadow:0 10px 24px rgba(19,37,45,.1);outline:none}
      .cal-ux-code{display:inline-block;font-size:.72rem;letter-spacing:.07em;font-weight:900;color:#6b5841;margin-right:.35rem}
      .cal-ux-pill{display:inline-block;border-radius:999px;padding:.18rem .48rem;font-size:.67rem;letter-spacing:.04em;text-transform:uppercase;font-weight:900;background:#eee5d4;color:#5d4921;margin:.35rem 0 .5rem}
      .cal-ux-audit{margin:.8rem auto;max-width:1080px;border:1px solid rgba(19,37,45,.18);border-radius:16px;overflow:hidden;background:#fff}
      .cal-ux-audit>summary{display:grid;grid-template-columns:auto 1fr auto;gap:.7rem;align-items:center;cursor:pointer;padding:1rem 1.1rem;background:#f6f4ee;color:#13252d}
      .cal-ux-audit>summary:hover,.cal-ux-audit>summary:focus-visible{background:#ece8de;outline:none}
      .cal-ux-audit>summary strong{line-height:1.3}
      .cal-ux-audit[open]>summary{border-bottom:1px solid rgba(19,37,45,.14)}
      .cal-ux-audit>section{margin:0!important;padding-top:1.2rem!important}
      .cal-ux-grades{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem;margin:1rem 0}
      .cal-ux-grade{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:13px;padding:.85rem;border-top:4px solid #526b59}
      .cal-ux-grade strong{display:block;font-size:.72rem;letter-spacing:.055em;text-transform:uppercase;margin-bottom:.35rem}
      .cal-ux-table-wrap{overflow-x:auto;margin:1rem 0;border-radius:14px}
      .cal-ux-table{width:100%;min-width:1040px;border-collapse:separate;border-spacing:0;font-size:.88rem;background:#fff}
      .cal-ux-table th,.cal-ux-table td{padding:.72rem;vertical-align:top;text-align:left;border-right:1px solid #dfe3e3;border-bottom:1px solid #dfe3e3;line-height:1.45}
      .cal-ux-table th{background:#13252d;color:#fff}
      .cal-ux-table td:first-child{border-left:1px solid #dfe3e3;font-weight:750}
      .cal-ux-boundary{background:#13252d;color:#fff;border-radius:14px;padding:1rem 1.1rem;margin-top:1rem}
      #calificacion-wider-context{padding:2rem 0;background:#f3efe4}
      .cal-ux-context-box{max-width:1120px;margin:0 auto}
      .cal-ux-context-box>details{background:#fff;border:2px solid #13252d;border-radius:18px;overflow:hidden}
      .cal-ux-context-box>details>summary{cursor:pointer;padding:1.1rem 1.25rem;font-weight:900;color:#13252d;background:#f8f7f2}
      .cal-ux-context-box>details>summary:hover,.cal-ux-context-box>details>summary:focus-visible{background:#ece8de;outline:none}
      .cal-ux-context-intro{padding:1rem 1.25rem;border-bottom:1px solid rgba(19,37,45,.12)}
      .cal-ux-context-body>section{margin:0!important}
      .cal-ux-correction-grid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(280px,.65fr);gap:1rem;margin-top:1rem}
      .cal-ux-correction-card{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:15px;padding:1rem}
      .cal-ux-correction-card ul{padding-left:1.2rem}
      .cal-ux-correction-card li{margin:.5rem 0;line-height:1.5}
      .cal-ux-reply{background:#13252d;color:#fff;border-radius:15px;padding:1rem 1.1rem}
      .cal-ux-reply h3{color:#fff;margin-top:0}
      .cal-ux-reply a{display:inline-block;margin-top:.5rem;color:#13252d;background:#fff;border-radius:999px;padding:.55rem .8rem;text-decoration:none;font-weight:800}
      body.cal-ux-ready main>.hero.cal-hero{padding-bottom:1.4rem}
      @media(max-width:900px){.cal-ux-status,.cal-ux-grades{grid-template-columns:repeat(2,minmax(0,1fr))}.cal-ux-cards,.cal-ux-serial-grid{grid-template-columns:1fr 1fr}.cal-ux-correction-grid{grid-template-columns:1fr}.cal-ux-audit>summary{grid-template-columns:auto 1fr}.cal-ux-audit>summary .cal-ux-pill{grid-column:2}}
      @media(max-width:620px){.cal-ux-status,.cal-ux-cards,.cal-ux-serial-grid,.cal-ux-grades{grid-template-columns:1fr}.cal-ux-gateway{padding-top:1.4rem}.cal-ux-nav{border-radius:0;margin-inline:-1rem}.cal-ux-audit{border-radius:0}.cal-ux-audit>summary{grid-template-columns:1fr}.cal-ux-audit>summary .cal-ux-pill{grid-column:auto}.cal-ux-context-box>details{border-radius:0}}
      @media print{.cal-ux-nav{display:none}.cal-ux-audit{break-inside:avoid}.cal-ux-context-box>details{border:1px solid #000}.cal-ux-context-box>details>summary{display:none}.cal-ux-context-box>details:not([open])>.cal-ux-context-intro,.cal-ux-context-box>details:not([open])>.cal-ux-context-body{display:block}}
    `;
    document.head.appendChild(style);
  };

  const ensureGateway = () => {
    let section = document.getElementById('calificacion-reader-gateway');
    if (section) return section;
    section = document.createElement('section');
    section.id = 'calificacion-reader-gateway';
    section.className = 'section cal-ux-gateway';
    const statuses = t.status.map(([h, b]) => `<div><strong>${h}</strong><span>${b}</span></div>`).join('');
    const cards = t.cards.map(([h, b]) => `<article class="cal-ux-card"><strong>${h}</strong><span>${b}</span></article>`).join('');
    const nav = t.nav.map(([label, href]) => `<a href="${href}">${label}</a>`).join('');
    section.innerHTML = `<div class="shell cal-ux-wrap"><p class="cal-ux-eyebrow">${t.gatewayEyebrow}</p><h2>${t.gatewayTitle}</h2><p class="cal-ux-lead">${t.gatewayLead}</p><div class="cal-ux-status">${statuses}</div><div class="cal-ux-cards">${cards}</div><nav class="cal-ux-nav" aria-label="${isEs ? 'Navegación de la página de calificación' : 'Classification page navigation'}">${nav}</nav><p class="cal-ux-direct">${t.direct}</p></div>`;
    return section;
  };

  const ensureSerialIndex = () => {
    let section = document.getElementById('calificacion-serial-index');
    if (section) return section;
    section = document.createElement('section');
    section.id = 'calificacion-serial-index';
    section.className = 'section cal-ux-section';
    const cards = t.serial.map(([code, title, status, body, href]) => `<a class="cal-ux-serial-card" href="${href}"><span class="cal-ux-code">${code}</span><strong>${title}</strong><span class="cal-ux-pill">${status}</span><span>${body}</span></a>`).join('');
    section.innerHTML = `<div class="shell cal-ux-wrap"><p class="cal-ux-eyebrow" style="color:#6b5841">${t.serialEyebrow}</p><h2>${t.serialTitle}</h2><p>${t.serialLead}</p><div class="cal-ux-serial-grid">${cards}</div></div>`;
    return section;
  };

  const ensureEvidenceMatrix = () => {
    let section = document.getElementById('evidence-before-actor');
    if (section) return section;
    section = document.createElement('section');
    section.id = 'evidence-before-actor';
    section.className = 'section cal-ux-section alt';
    const grades = t.gradeLabels.map(([h, b]) => `<div class="cal-ux-grade"><strong>${h}</strong><span>${b}</span></div>`).join('');
    const head = t.evidenceHeaders.map((h) => `<th>${h}</th>`).join('');
    const rows = t.evidenceRows.map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join('')}</tr>`).join('');
    section.innerHTML = `<div class="shell cal-ux-wrap"><p class="cal-ux-eyebrow" style="color:#6b5841">${t.evidenceEyebrow}</p><h2>${t.evidenceTitle}</h2><p>${t.evidenceLead}</p><div class="cal-ux-grades">${grades}</div><div class="cal-ux-table-wrap" role="region" tabindex="0" aria-label="${isEs ? 'Matriz de evidencia ante cada actor' : 'Evidence-before-actor matrix'}"><table class="cal-ux-table"><thead><tr>${head}</tr></thead><tbody>${rows}</tbody></table></div><div class="cal-ux-boundary">${t.evidenceBoundary}</div></div>`;
    return section;
  };

  const ensureCorrections = () => {
    let section = document.getElementById('what-would-change-our-view');
    if (section) return section;
    section = document.createElement('section');
    section.id = 'what-would-change-our-view';
    section.className = 'section cal-ux-section';
    const items = t.correctionItems.map((item) => `<li>${item}</li>`).join('');
    section.innerHTML = `<div class="shell cal-ux-wrap"><p class="cal-ux-eyebrow" style="color:#6b5841">${t.correctionEyebrow}</p><h2>${t.correctionTitle}</h2><div class="cal-ux-correction-grid"><article class="cal-ux-correction-card"><p>${t.correctionLead}</p><ul>${items}</ul></article><aside class="cal-ux-reply"><h3>${t.replyTitle}</h3><p>${t.replyBody}</p><a href="mailto:sbu001@monterecco.com?subject=${encodeURIComponent(isEs ? 'Corrección documentada — Calificación LPB' : 'Documented correction — LPB Classification')}">${t.replyLink}</a></aside></div></div>`;
    return section;
  };

  const ensureContext = () => {
    let section = document.getElementById('calificacion-wider-context');
    if (section) return section;
    section = document.createElement('section');
    section.id = 'calificacion-wider-context';
    section.className = 'section';
    section.innerHTML = `<div class="shell cal-ux-context-box"><p class="cal-ux-eyebrow" style="color:#6b5841">${t.contextEyebrow}</p><h2>${t.contextTitle}</h2><p>${t.contextLead}</p><details><summary>${t.contextSummary}</summary><div class="cal-ux-context-intro"><p>${t.contextLead}</p></div><div class="cal-ux-context-body"></div></details></div>`;
    return section;
  };

  const foldGroup = (id, code, status, selectors) => {
    let details = document.getElementById(id);
    if (!details) {
      const candidates = selectors.map((selector) => block(selector)).filter(Boolean);
      if (!candidates.length) return null;
      details = document.createElement('details');
      details.id = id;
      details.className = 'cal-ux-audit';
      const heading = candidates[0].querySelector('h2')?.textContent?.trim() || code;
      details.innerHTML = `<summary><span class="cal-ux-code">${code}</span><strong>${heading}</strong><span class="cal-ux-pill">${status}</span></summary>`;
      candidates[0].parentNode.insertBefore(details, candidates[0]);
    }
    selectors.forEach((selector) => {
      const candidate = block(selector);
      if (candidate && candidate !== details && !details.contains(candidate)) details.appendChild(candidate);
    });
    return details;
  };

  const moveAfter = (cursor, node) => {
    if (!cursor || !node || cursor === node) return cursor;
    cursor.insertAdjacentElement('afterend', node);
    return node;
  };

  const collectContext = (context) => {
    const body = context.querySelector('.cal-ux-context-body');
    if (!body) return;
    const selectors = [
      '#caixabank-borja-witness-control',
      '#lpam-magistrado-source-control',
      '#lpam-cgpj169-calificacion-unitary',
      '[data-cal-creditor-control-20260816]',
      '[data-extraconcursal-force-20260816]',
      '[data-borja-security-source-upgrade-20260816]',
      '#calificacion-eleconomista-collateral-use',
      '#same-asset-multiple-financial-lives-16aug2026',
      '#eleconomista'
    ];
    const items = selectors.map((selector) => block(selector)).filter(Boolean);
    [
      blockByHeading(isEs ? 'Una vida procesal dentro del concurso' : 'One procedural life'),
      blockByHeading(isEs ? 'La calificación y la vida económica del hotel' : 'The classification and the hotel’s economic life'),
      blockByHeading(isEs ? 'El mismo hotel puede aparecer' : 'The same hotel can appear')
    ].filter(Boolean).forEach((item) => items.push(item));
    [...new Set(items)].forEach((item) => {
      if (item !== context && !body.contains(item)) body.appendChild(item);
    });
  };

  const updateFooter = () => {
    const footerLine = [...document.querySelectorAll('.site-footer .small')].find((el) => /Actualizado|Updated/i.test(el.textContent || ''));
    if (footerLine) footerLine.textContent = t.footer;
  };

  const apply = () => {
    if (applying) return;
    applying = true;
    try {
      ensureStyle();
      const hero = topBlock(main.querySelector('.hero.cal-hero, .hero'));
      if (!hero) return;

      const gateway = ensureGateway();
      const criminalMisuse = block('[data-calificacion-misuse-thesis]');
      const serial = ensureSerialIndex();
      const evidence = ensureEvidenceMatrix();
      const corrections = ensureCorrections();
      const context = ensureContext();

      const canonical = block('#canonical-calificacion-map');
      const professional = block('[data-cal-professional-read="1"]');
      if (professional) professional.id = 'calificacion-professional-read';
      const legal = block('.explain');
      const contradictions = block('#contradictions');
      const radical = block('[data-calificacion-radical-20260816]');

      const a01 = foldGroup('audit-a01', 'A01', isEs ? 'CONTRADICHA / ESTRECHADA' : 'CONTRADICTED / NARROWED', ['[data-cal-allegation01-20260816]']);
      const a02 = foldGroup('audit-a02', 'A02', isEs ? 'CAUSALIDAD AMPLIA RECHAZADA' : 'BROAD CAUSATION REJECTED', ['[data-cal-allegation02-20260816]']);
      const a03 = foldGroup('audit-a03', 'A03', isEs ? 'ADVERSA / RECURRIDA' : 'ADVERSE / APPEALED', ['[data-cal-allegation03-20260816]', '[data-a03-unitary-causation-20260816]']);
      const a04 = foldGroup('audit-a04', 'A04', isEs ? 'ADVERSA / RECURRIDA' : 'ADVERSE / APPEALED', ['[data-cal-allegation04-20260816]', '[data-cal-a04-cls-bdo-correction-20260816]']);

      const recovery = block('[data-cal-recovery-adversity-20260816]');
      const counter = block('[data-cal-counter-record-20260816]');
      const priorKnowledge = block('#prior-judicial-knowledge-rescue-link');
      const opening = block('[data-calificacion-opening-20260816]');
      const judge = block('[data-approved-judge-accusation-20260816]');
      if (judge) judge.id = 'judge-accusation';
      const amount = block('[data-calificacion-3032010-20260816]');
      const judicialAdoption = block('[data-cal-judicial-adoption-20260816]');
      const actors = block('#actors');
      const di248 = block('#di248');
      const fiscalResponse = block('[data-eg49-fiscal-response-20260816]');
      const fiscalBridge = block('#cal-fiscal-chain-2012-2019-2026');
      const primaryClosures = block('#cal-primary-source-closures-20260816');

      collectContext(context);

      const ordered = [
        gateway,
        criminalMisuse,
        canonical,
        professional,
        legal,
        contradictions,
        radical,
        serial,
        a01,
        a02,
        a03,
        a04,
        evidence,
        recovery,
        counter,
        priorKnowledge,
        opening,
        judge,
        amount,
        judicialAdoption,
        actors,
        di248,
        fiscalResponse,
        fiscalBridge,
        primaryClosures,
        corrections,
        context
      ].filter(Boolean);

      let cursor = hero;
      ordered.forEach((node) => { cursor = moveAfter(cursor, node); });
      updateFooter();
      document.body.classList.add('cal-ux-ready');
      document.body.dataset.calificacionReaderExperience = '20260817a';
    } finally {
      applying = false;
    }
  };

  const schedule = () => {
    window.clearTimeout(settleTimer);
    settleTimer = window.setTimeout(apply, 60);
  };

  const observer = new MutationObserver(schedule);
  observer.observe(main, { childList: true, subtree: false });

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply, { once: true });
  else apply();
  window.addEventListener('load', () => {
    apply();
    window.setTimeout(apply, 350);
    window.setTimeout(apply, 1400);
    window.setTimeout(() => observer.disconnect(), 6000);
  }, { once: true });
})();

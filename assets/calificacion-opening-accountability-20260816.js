(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const enCal = path.endsWith('/en/insolvency-classification-parallel-lives/');
  const esCal = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const enAp = path.endsWith('/en/insolvency-36-2012-ap-section-4/');
  const esAp = path.endsWith('/es/concurso-36-2012-ap-seccion-4/');
  if (!enCal && !esCal && !enAp && !esAp) return;
  if (document.querySelector('[data-calificacion-opening-20260816]')) return;

  const es = esCal || esAp;
  const style = document.createElement('style');
  style.textContent = `
    .cal-open{padding:2rem 0}.cal-open-wrap{max-width:1120px;margin:0 auto}.cal-kicker{font-size:.76rem;letter-spacing:.09em;text-transform:uppercase;font-weight:800;opacity:.78}
    .cal-status,.cal-thesis,.cal-boundary,.cal-adverse{border-radius:18px;padding:1.25rem 1.35rem}.cal-status{background:#f3efe4;border:1px solid #cabb9d}.cal-status h3{margin:.35rem 0 .55rem}
    .cal-thesis{margin-top:1rem;background:#101f26;color:#fff;border:1px solid rgba(255,255,255,.12)}.cal-thesis h2{font-size:clamp(1.9rem,4.2vw,3rem);line-height:1.06;margin:.45rem 0 .9rem}.cal-thesis p{max-width:980px}.cal-thesis strong{color:#fff}
    .cal-objective{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.85rem;margin-top:1rem}.cal-objective article,.cal-inversion article{background:#fff;color:#13252d;border-radius:14px;padding:1rem;border-top:4px solid #8c6b2f}.cal-objective h3,.cal-inversion h3{margin:.1rem 0 .45rem;font-size:1.03rem}.cal-objective p,.cal-inversion p{margin:.35rem 0}
    .cal-flow{margin-top:1rem;background:#fff;color:#13252d;border-radius:14px;padding:1rem 1.1rem;border-left:5px solid #7e2929;font-weight:700;line-height:1.55}
    .cal-inversion{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.85rem;margin-top:1rem}.cal-inversion article{border-top-color:#7e2929}.cal-inversion small{display:block;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#7e2929;margin-bottom:.35rem}
    .cal-adverse{margin-top:1rem;background:#fff;border:1px solid rgba(19,37,45,.17)}.cal-adverse h3,.cal-boundary h3{margin:.2rem 0 .55rem}.cal-adverse ul{margin:.55rem 0 0;padding-left:1.15rem}.cal-adverse li{margin:.35rem 0}
    .cal-boundary{margin-top:1rem;background:#fbf7ed;border-left:5px solid #8c6b2f}.cal-source{font-size:.88rem;opacity:.78;margin-top:.9rem}
    @media(max-width:900px){.cal-objective,.cal-inversion{grid-template-columns:1fr}.cal-thesis{border-radius:0}.cal-open{padding-top:1rem}}
  `;
  document.head.appendChild(style);

  const status = es ? {
    kicker: 'ESTADO ACTUAL DEL RECURSO',
    title: 'Audiencia Provincial de Las Palmas · Sección Cuarta · RPL 2523/2025',
    body: '<strong>Último estado verificado: pendiente de decisión/notificación.</strong> La correspondencia formal identifica el recurso y el 13 de mayo de 2026 se comunicó que deliberación y fallo se habían fijado para el <strong>4 de junio de 2026</strong>. En la búsqueda controlada hasta el 16 de agosto de 2026 no se ha localizado sentencia de apelación ni resolución terminal.'
  } : {
    kicker: 'CURRENT APPEAL STATUS',
    title: 'Audiencia Provincial de Las Palmas · Fourth Section · RPL 2523/2025',
    body: '<strong>Latest verified status: awaiting appellate decision/notification.</strong> Formal correspondence identifies the appeal and on 13 May 2026 it was reported that deliberation and judgment had been fixed for <strong>4 June 2026</strong>. The controlled search through 16 August 2026 located no appellate judgment or terminating resolution.'
  };

  const section = document.createElement('section');
  section.className = 'section cal-open';
  section.dataset.calificacionOpening20260816 = '1';

  const statusHtml = `<div class="cal-status"><div class="cal-kicker">${status.kicker}</div><h3>${status.title}</h3><p>${status.body}</p></div>`;
  if (enAp || esAp) {
    section.innerHTML = `<div class="shell cal-open-wrap">${statusHtml}</div>`;
  } else {
    const d = es ? {
      kicker: 'TESIS CENTRAL · EXPOSICIÓN TOTAL · INVERSIÓN DE LA VERDAD Y DESVÍO DEL FOCO',
      title: 'Mi tesis: la Calificación convirtió hechos que exigían examinar a terceros, a la Comunidad y a la propia administración concursal en una acusación personal contra nosotros.',
      lead1: '<strong>En términos de culpabilidad personal, mi posición es inequívoca: las acusaciones contra nosotros son falsas.</strong> No porque sostenga que cada dato bruto fue inventado. Esta página publica también los hechos que nos perjudican. Lo que denuncio es la transformación: un hecho real, incompleto o discutido se separa del sistema que lo produjo, se omite quién debía, quién controlaba, quién podía actuar y qué hizo la propia Administración Concursal, y después ese fragmento reaparece como culpa de Gil, LPB, Pink o Patricia.',
      lead2: 'Por eso la tesis unitaria no es “todo era perfecto”. Es más precisa y más grave: <strong>inversión de agencia, inversión causal y desvío del objeto de investigación.</strong> Donde el expediente exigía preguntar por terceros deudores, gobernanza de la Comunidad, control material, decisiones de recuperación, capacidad real de actuación y vías documentadas de continuidad/salida, la Calificación desplazó el centro de gravedad hacia nuestra supuesta obstrucción, pasividad o culpabilidad.',
      objectiveTitle: 'Objetivo de esta página',
      objectives: [
        ['Exponerlo todo', 'Publicar cada alegación de la AC, incluso la más adversa, y también las ramas en las que la propia AC dijo que no constaba nada.'],
        ['Separar hecho de culpabilidad', 'Un dato puede ser verdadero y, aun así, no probar quién causó el daño, quién podía evitarlo ni que exista dolo o culpa grave.'],
        ['Reconstruir el sistema', 'Examinar hotel, Comunidad, créditos, operación, contabilidad, acceso, financiación, AC, terceros y capacidad real como una sola cadena causal.'],
        ['Localizar la inversión', 'Preguntar en cada acusación quién aparece convertido de acreedor, perjudicado o actor limitado en supuesto causante del perjuicio.'],
        ['Localizar el desvío', 'Identificar qué deuda, actor, decisión, recuperación, conflicto, control o alternativa desaparece del foco cuando se formula la acusación.'],
        ['Probar conocimiento antes de intención', 'Sólo después de acreditar qué documento tuvo cada actor puede graduarse sobreafirmación, falsedad consciente, finalidad o eventual responsabilidad.']
      ],
      flow: 'HECHO BRUTO → CONTEXTO OMITIDO → PODER/CAPACIDAD REAL → AGENCIA INVERTIDA → CAUSALIDAD ATRIBUIDA → CULPABILIDAD → USO INSTITUCIONAL → QUÉ QUEDÓ FUERA DEL FOCO',
      examplesTitle: 'Cómo se manifiesta la inversión en el expediente',
      examples: [
        ['Créditos debidos a LPB', 'Dinero que terceros debían a LPB fue convertido en culpabilidad por no cobro. La Sentencia 163/2023 rechazó la construcción general de culpa grave/causalidad y corrigió expresamente la tesis de que LPB “se debía a sí misma” parte del crédito CEXP. El problema estrecho de soportes documentales permanece recurrido.'],
        ['Cooperación y documentación', 'La narrativa global de no colaboración convive con respuestas detalladas y documentación reconocida por la propia AC. La sentencia la estrecha: no equipara entrega imperfecta con ausencia total de cooperación.'],
        ['Contabilidad', 'El expediente no sostiene honestamente “no había contabilidad”: la AC reconoce diarios y balances. Permanece un fallo adverso más estrecho sobre el Libro Diario estatutario durante el concurso, actualmente recurrido.'],
        ['Pink, operación y rentas', 'La racionalidad del contrato, la economía real del hotel, los costes, la gobernanza y la cobrabilidad no son lo mismo que la existencia de rentas impagadas. El fallo adverso sobre no cobro y €3.032.010,34 existe y está recurrido; precisamente por eso debe auditarse sin simplificar la cadena causal.'],
        ['Continuidad, financiación y salida', 'El propio expediente y fuentes contemporáneas documentan plan de viabilidad, recapitalización, operadores, financiación, valoración y arquitectura de normalización/salida. Eso no prueba que cada operación hubiera cerrado, pero contradice una lectura de mera pasividad o abandono.'],
        ['Papeles procesales invertidos', 'Mientras Gil/Aweswell pedían investigar el perímetro AC/CAM en DI 248/2018, la posición fiscal adversa de la Calificación fue después invocada al archivar esa denuncia. La secuencia documenta un problema de circularidad/arrastre de marco; no prueba por sí sola concertación personal.']
      ],
      adverseTitle: 'Lo adverso que esta tesis no esconde',
      adverse: [
        'Sentencia 163/2023 mantiene en primera instancia un pronunciamiento adverso por no cobro de rentas y fija €3.032.010,34; está recurrido.',
        'Mantiene un pronunciamiento adverso sobre el Libro Diario durante el concurso; está recurrido.',
        'Mantiene una falta de colaboración más estrecha sobre soportes de determinados créditos; está recurrida.',
        'La presentación tardía fue aceptada como causa respecto de Uri Omid, no respecto de Gil.',
        'Que otras ramas fueran rechazadas o corregidas no convierte automáticamente los fallos que sobreviven en falsos ni prueba intención criminal.'
      ],
      boundaryTitle: 'Límite de apelación y de publicación',
      boundary: '<strong>RPL 2523/2025 corresponde a la Audiencia Provincial y debe resolverse desde el expediente judicial.</strong> Esta página no pide a ningún magistrado decidir desde una web ni fuera de autos. Su función es otra: trazabilidad documental, preservación pública, corrección de afirmaciones, comparación de fuentes y exposición completa de las preguntas que siguen abiertas mientras la sentencia de primera instancia continúa produciendo efectos.',
      source: 'Control interno: CALIFICACION_UNITARY_TRUTH_INVERSION_DIVERSION_THESIS_16AUG2026.md + CALIFICACION_AC_REPORT_RADICAL_TRANSPARENCY_LEDGER_16AUG2026.md. Las calificaciones de falsedad consciente, instrumentalización o responsabilidad penal permanecen como alegaciones de parte salvo resolución competente.'
    } : {
      kicker: 'CENTRAL THESIS · COMPLETE EXPOSURE · TRUTH INVERSION AND DIVERSION OF SCRUTINY',
      title: 'My thesis: the Classification turned facts that required scrutiny of third parties, the Community and the insolvency administration itself into a personal accusation against us.',
      lead1: '<strong>As a proposition of personal culpability, my position is unequivocal: the accusations against us are false.</strong> That does not mean I say every raw fact was invented. This page also publishes the facts that cut against us. What I challenge is the transformation: a real, incomplete or disputed fact is detached from the system that produced it; who owed, who controlled, who could act and what the Insolvency Administration itself did are omitted; the fragment then reappears as culpability of Gil, LPB, Pink or Patricia.',
      lead2: 'The unitary thesis is therefore not “everything was perfect”. It is more exact and more serious: <strong>inversion of agency, inversion of causation and diversion of the object of scrutiny.</strong> Where the record required questions about third-party debtors, Community governance, material control, recovery decisions, real capacity to act and documented continuity/exit work, the Classification shifted the centre of gravity to alleged obstruction, passivity or culpability on our side.',
      objectiveTitle: 'Objective of this page',
      objectives: [
        ['Expose everything', 'Publish every AC allegation, including the strongest adverse allegation, and also the statutory branches where the AC itself said nothing was known.'],
        ['Separate fact from culpability', 'A raw fact can be true and still fail to prove who caused the harm, who could prevent it, or gross fault/intent.'],
        ['Reconstruct the system', 'Test hotel, Community, receivables, operation, accounting, access, finance, AC decisions, third parties and real capacity as one causal chain.'],
        ['Locate the inversion', 'For each allegation ask who was converted from creditor, injured party or constrained actor into the supposed cause of the harm.'],
        ['Locate the diversion', 'Identify which debt, actor, decision, recovery step, conflict, control fact or alternative disappears from view when the accusation is framed.'],
        ['Prove knowledge before intent', 'Only after proving what material was before each actor should the page grade overstatement, knowing falsehood, purpose or possible liability.']
      ],
      flow: 'RAW FACT → OMITTED CONTEXT → REAL POWER/CAPACITY → INVERTED AGENCY → ATTRIBUTED CAUSATION → CULPABILITY → INSTITUTIONAL REUSE → WHAT DISAPPEARED FROM SCRUTINY',
      examplesTitle: 'How the inversion appears in the record',
      examples: [
        ['Receivables owed to LPB', 'Money owed by third parties to LPB was converted into culpability for non-collection. Judgment 163/2023 rejected the general gross-fault/causation construction and expressly corrected the theory that LPB effectively owed itself part of the CEXP receivable. A narrower support-document issue remains appealed.'],
        ['Cooperation and documents', 'The global non-cooperation narrative coexists with detailed responses and material acknowledged by the AC itself. The judgment narrows the issue: imperfect production is not the same proposition as total refusal to cooperate.'],
        ['Accounting', 'The record cannot honestly be reduced to “there were no accounts”: the AC acknowledges journals and balances. A narrower adverse finding about the statutory Daily Journal during the insolvency remains and is appealed.'],
        ['Pink, operation and rent', 'Contract rationality, real hotel economics, costs, governance and collectability are not the same thing as unpaid rent. The adverse first-instance finding on non-collection and €3,032,010.34 exists and is appealed; that is precisely why the causal chain must be audited rather than simplified.'],
        ['Continuity, finance and exit', 'The adverse record and contemporaneous sources document viability planning, recapitalisation, operators, finance, valuation and a commercial-normalisation/exit architecture. That does not prove every transaction would have closed, but it contradicts a simple story of passivity or abandonment.'],
        ['Reversed procedural roles', 'While Gil/Aweswell were asking for investigation of the AC/CAM perimeter in DI 248/2018, the adverse Fiscal classification position was later invoked in archiving that complaint. The sequence supports a circularity/frame-inheritance question; it does not by itself prove personal coordination.']
      ],
      adverseTitle: 'Adverse facts this thesis does not hide',
      adverse: [
        'Judgment 163/2023 retains a first-instance adverse finding on rent non-collection and awards €3,032,010.34; it is appealed.',
        'It retains an adverse finding concerning the statutory Daily Journal during the insolvency; it is appealed.',
        'It retains a narrower non-cooperation finding concerning support for specified receivables; it is appealed.',
        'Late filing was accepted as a cause as to Uri Omid, not Gil.',
        'Rejection or correction of other branches does not automatically make every surviving finding false or prove criminal intent.'
      ],
      boundaryTitle: 'Appeal and publication boundary',
      boundary: '<strong>RPL 2523/2025 is for the Audiencia Provincial to decide from the judicial record.</strong> This page does not ask any magistrate to decide from a website or outside the record. Its purpose is documentary traceability, public preservation, correction, source comparison and complete exposure of the questions that remain open while the first-instance judgment continues to have effects.',
      source: 'Internal control: CALIFICACION_UNITARY_TRUTH_INVERSION_DIVERSION_THESIS_16AUG2026.md + CALIFICACION_AC_REPORT_RADICAL_TRANSPARENCY_LEDGER_16AUG2026.md. Knowing-falsehood, instrumentalisation and criminal-liability characterisations remain party allegations unless established by a competent decision.'
    };

    const objectiveCards = d.objectives.map(x => `<article><h3>${x[0]}</h3><p>${x[1]}</p></article>`).join('');
    const inversionCards = d.examples.map(x => `<article><small>${x[0]}</small><p>${x[1]}</p></article>`).join('');
    const adverseItems = d.adverse.map(x => `<li>${x}</li>`).join('');

    section.innerHTML = `<div class="shell cal-open-wrap">
      ${statusHtml}
      <div class="cal-thesis">
        <div class="cal-kicker">${d.kicker}</div>
        <h2>${d.title}</h2>
        <p>${d.lead1}</p>
        <p>${d.lead2}</p>
        <h3>${d.objectiveTitle}</h3>
        <div class="cal-objective">${objectiveCards}</div>
        <div class="cal-flow">${d.flow}</div>
        <h3 style="margin-top:1.25rem">${d.examplesTitle}</h3>
        <div class="cal-inversion">${inversionCards}</div>
      </div>
      <div class="cal-adverse"><h3>${d.adverseTitle}</h3><ul>${adverseItems}</ul></div>
      <div class="cal-boundary"><h3>${d.boundaryTitle}</h3><p>${d.boundary}</p></div>
      <p class="cal-source">${d.source}</p>
    </div>`;
  }

  const hero = document.querySelector('main .hero') || document.querySelector('main');
  if (hero) hero.insertAdjacentElement('afterend', section);
})();
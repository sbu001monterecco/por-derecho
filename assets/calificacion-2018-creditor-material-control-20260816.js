(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const es = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const en = path.endsWith('/en/insolvency-classification-parallel-lives/');
  if (!es && !en) return;
  if (document.querySelector('[data-cal-creditor-control-20260816]')) return;

  const d = es ? {
    eyebrow: '2018 · ACREEDOR + CONTROL MATERIAL · CAUSALIDAD A REHACER',
    title: 'El acreedor pasó a un plano de posesión/control material antes de la adjudicación',
    lead: '<strong>Construcciones Acosta Matos, S.A. ya era acreedor hipotecario reconocido.</strong> El registro documental sitúa el <strong>7 de junio de 2018</strong> como umbral de posesión/control material de facto sobre Sun Park. <strong>No hemos localizado una entrega judicial del conjunto hotelero que autorizara ese control en esa fecha.</strong> Esa secuencia obliga a preguntar quién tenía realmente capacidad para operar, conservar, dar acceso, generar ingresos, ejecutar un rescate o causar/evitar deterioro.',
    definition: '<strong>“Lender in possession” se usa aquí sólo como comparación funcional.</strong> No es una categoría jurídica española que atribuyamos a CAM: significa, descriptivamente, <em>acreedor garantizado + control/posesión material de facto</em>. Tampoco equivale a propiedad. La pregunta jurídica española es qué título o autoridad amparó cada acto concreto de control.',
    statuses: [
      ['HECHO DOCUMENTADO', '20 OCT 2017 → 8 FEB 2018', 'PH122 cedió el crédito a CAM y el Juzgado Mercantil reconoció después a CAM como titular de los importes hipotecarios.'],
      ['UMBRAL DE CONTROL', '7 JUN 2018', 'El expediente de control/posesión sitúa aquí el cambio material de control. El alcance exacto por actor, finca y periodo sigue sujeto a prueba.'],
      ['PREGUNTA ABIERTA', 'AUTORIZACIÓN PREVIA', 'No se ha localizado una entrega u orden judicial del conjunto hotelero que autorice ese control en o antes del 7 de junio. Si existe, debe identificarse por fecha, términos y perímetro.']
    ],
    timelineTitle: 'La secuencia que no debe comprimirse',
    timeline: [
      ['20 OCT 2017', 'PH122 → CAM', 'Cesión del crédito. Ser acreedor no convierte por sí solo a CAM en propietario del hotel.'],
      ['8 FEB 2018', 'CAM reconocido como titular del crédito', 'El Juzgado reconoce los importes hipotecarios cedidos. El derecho de crédito y el derecho a la posesión siguen siendo cuestiones distintas.'],
      ['7 JUN 2018', 'Umbral de control material', 'El registro sitúa el paso a un control/posesión práctica de facto. Aquí cambia la línea de base causal.'],
      ['26 JUN 2018', 'Suspensión judicial posterior', 'La suspensión llega después del umbral de control. Una resolución posterior no demuestra por sí sola autorización previa ni regulariza retrospectivamente cada acto anterior.']
    ],
    calTitle: 'Por qué esto cambia severamente la lectura de la calificación',
    calIntro: 'La calificación no puede atribuir causalidad sólo desde la titularidad formal o desde quién tenía un deber abstracto. Tiene que incorporar <strong>capacidad real de actuación</strong>. Desde el 7 de junio, cada imputación debe pasar por un test pre/post-control.',
    calCards: [
      ['1 · COLABORACIÓN', '<strong>¿Quién podía realmente entregar, permitir o producir?</strong> Si llaves, zonas, personal, seguridad, documentación operativa o acceso físico estaban bajo control ajeno, no puede imputarse automáticamente al deudor una omisión que materialmente dependía de otro actor. Esto no borra retrasos documentales reales; obliga a separar capacidad de culpa.'],
      ['2 · PINK / RENTAS / EXPLOTACIÓN', '<strong>No puede existir una sola línea causal continua si cambió el controlador material.</strong> Deben separarse el periodo previo al 7 de junio, el evento de control, la explotación posterior, los operadores posteriores y la adjudicación formal. Quién podía generar ingresos, admitir huéspedes, conservar habitaciones o contratar operación es parte del nexo causal.'],
      ['3 · AGRAVACIÓN DE LA INSOLVENCIA', '<strong>Cualquier deterioro o pérdida posterior necesita un contrafactual de control.</strong> Antes de decir que Gil/LPB agravó la insolvencia hay que probar qué seguía pudiendo controlar después del 7 de junio y qué había pasado al control práctico de CAM u otros actores individualizados.'],
      ['4 · AC / ADMINISTRACIÓN DE LA MASA', '<strong>La actuación de la AC pasa al centro del análisis.</strong> ¿Qué sabía antes del 7 de junio? ¿Qué autorizó el nodo de seguridad del 18 de mayo? ¿Consintió, toleró, se opuso o pidió restitución? ¿Exigió inventario de llaves, rendición de ingresos, frutos, gastos, obras o acceso?'],
      ['5 · JUEZ / SENTENCIA 163/2023', '<strong>El control material sólo puede imputarse al conocimiento judicial si se prueba que la evidencia estaba ante el juez.</strong> Si lo estaba, debe auditarse si la sentencia atribuyó agravación sin integrar al controlador material. Una omisión causal puede ser error apelable o cuestión de responsabilidad institucional; no prueba por sí sola prevaricación.'],
      ['6 · ART. 166 LC · TERCEROS', '<strong>La condición de acreedor/controlador no hace automáticamente “cómplice” a CAM.</strong> Pero sí obliga a preguntar si algún acto concreto que fundó la culpabilidad tuvo cooperación de terceros con el grado subjetivo exigido y por qué esa participación fue —o no fue— individualizada.']
    ],
    concursoTitle: 'Lo que obliga a reabrir en el resto del Concurso 36/2012',
    concursoCards: [
      ['CONSERVACIÓN', 'Inventario y estado pre/post 7 de junio: quién podía inspeccionar, mantener, reparar, asegurar y preservar la masa.'],
      ['EJECUCIÓN / GARANTÍA', 'El crédito garantizado daba derechos de acreedor, pero no responde por sí mismo a la pregunta distinta: qué autoridad permitía tomar control material del activo.'],
      ['VALORACIÓN', 'La inspección/valoración de mayo-junio de 2018 debe leerse junto al cambio de acceso/control: quién podía mostrar, medir, conservar o alterar el activo y con qué información.'],
      ['RESCATE / SALIDA FINANCIADA', 'Si el evento de control dificultó operación, diligencia de inversores, financiación o una salida del concurso, pasa a ser variable causal en la pérdida de valor y en el fracaso del rescate.'],
      ['PUJAS / ADJUDICACIÓN', 'Control práctico prolongado antes de una venta posterior puede generar ventajas de información, acceso o operación que deben compararse con las de otros interesados. No invalida automáticamente la adjudicación: exige prueba.'],
      ['CUENTAS / FRUTOS / BENEFICIO', 'Hay que reconstruir ingresos, reservas, rentas, pagos de operadores, seguridad, obras, suministros, capex y cualquier beneficio obtenido o gasto soportado durante la posesión/control previo a la adjudicación.']
    ],
    parallelTitle: 'Las vidas paralelas fuera del concurso no desaparecen porque el mismo hotel sea el escenario',
    parallelIntro: 'Sun Park no puede tratarse como si todo derecho físico, societario y económico perteneciera a LPB. El control material del hotel abre —o refuerza— carriles jurídicos separados que deben conservar su propia titularidad, jurisdicción, prueba y remedio.',
    parallel: [
      ['LPB · VIDA CONCURSAL', 'Masa activa, acreedores, garantía, rescate, valoración, venta, rendición de cuentas y causalidad de la calificación.'],
      ['MATKATOR / TERCEROS', '<strong>Crédito contra LPB ≠ título sobre activos de terceros.</strong> Cada finca/unidad debe seguir la cadena propietario → título → posesión → uso → obras → ingresos → situación actual.'],
      ['COMUNIDAD / SEGURIDAD', 'Actas, votos, mandato de seguridad, llaves, guardias y zonas comunes tienen una cadena de autoridad propia. Un acuerdo de seguridad no se presume transferencia de propiedad ni de posesión ilimitada.'],
      ['OPERADORES / COMERCIALIZACIÓN', 'Lava Verde, Club Sei, Meeting Point y cualquier operador posterior requieren contrato, inventario, autoridad, reservas, comisiones, pagos y periodo. La explotación posterior puede demostrar control, pero no el título originario del 7 de junio.'],
      ['OBRAS / RICPE / INCENTIVOS / FONDOS', 'Licencias, proyectos, financiación o apoyo público pueden probar cómo se representó el activo y quién se benefició después. No convierten retroactivamente el control de 2018 en propiedad ni curan por sí solos un defecto de título/posesión privada.'],
      ['AWESWELL / PÉRDIDA INVERSORA', 'Si el control material bloqueó rescate, explotación de activos separados o financiación, la pérdida del inversor puede existir en un plano distinto de la pérdida de la masa de LPB. Debe evitarse doble recuperación y probarse el nexo.']
    ],
    defenceTitle: 'La defensa más fuerte — y lo que todavía queda después de aceptarla',
    defence: '<strong>Defensa posible:</strong> CAM puede sostener que el acceso/control fue consentido, limitado a seguridad, amparado por la Comunidad o por sus derechos de garantía, que LPB conservó acceso real, que no había explotación efectiva que interrumpir, o que decisiones judiciales posteriores reconocieron/regularizaron la situación. <strong>Lo que queda:</strong> identificar la autoridad vigente el 7 de junio; su perímetro exacto; quién tenía llaves/guardias/acceso; qué consentía cada propietario; qué hizo la AC; qué ingresos/gastos/obras produjo el periodo; y qué cambió para rescate, valor, operación y pujas.',
    productionTitle: 'Prueba finita que cerraría la controversia',
    production: [
      'Orden, entrega o autorización judicial vigente en o antes del 7 de junio de 2018 que ampare el control del conjunto hotelero, si existe.',
      'Acta, contrato e instrucciones completas del nodo Comunidad/seguridad de 18 de mayo de 2018.',
      'Registro de llaves, cerraduras, códigos, guardias, autorizantes, facturas, CCTV y accesos.',
      'PMS/reservas, ingresos, pagos de operadores, suministros, obras, capex y contabilidad de frutos/gastos desde el cambio de control hasta la adjudicación formal.',
      'Mapa finca por finca de LPB, Matkator y terceros y prueba de consentimiento/autoridad respecto de cada una.',
      'Qué prueba del evento de control estaba realmente ante la AC, Fiscal y juez al formular o adoptar cada conclusión de la calificación.'
    ],
    rule: '<strong>Regla temporal:</strong> adjudicación posterior ≠ autorización retroactiva. <strong>Regla patrimonial:</strong> acreedor ≠ propietario. <strong>Regla probatoria:</strong> control material ≠ responsabilidad colectiva del “perímetro”. <strong>Regla penal:</strong> error u omisión causal ≠ delito sin prueba independiente del elemento subjetivo.',
    source: 'Control interno: CALIFICACION_2018_CREDITOR_IN_MATERIAL_POSSESSION_CONTROL_LEDGER_16AUG2026.md · P19_SUN_PARK_MATERIAL_CONTROL_POSSESSION_CONTINUITY_MEETING_POINT_15AUG2026.md · PH122_CAM_ASSIGNMENT_ART1535_PUBLICATION_CONTROL_16AUG2026.md · RECOVERY_CAUSATION_MATRIX_CONCURSO36_15AUG2026.md. Marco legal contrastado con la Ley 22/2003 aplicable en 2018 (arts. 40, 43, 55–57, 155, 164, 166 y 172) y Código Civil (posesión/frutos).',
    links: [
      ['Control material 7 junio 2018 →', '../toma-control-sun-park-7-junio-2018/'],
      ['Acreedor de registro →', '../acreedor-de-registro/'],
      ['Convergencia venta-acreedor →', '../convergencia-venta-acreedor/'],
      ['Perímetro Acosta Matos →', '../acosta-matos-perimetro/']
    ]
  } : {
    eyebrow: '2018 · CREDITOR + MATERIAL CONTROL · CAUSATION TO BE REBUILT',
    title: 'The creditor moved into material possession/control before adjudication',
    lead: '<strong>Construcciones Acosta Matos, S.A. was already the recognised holder of mortgage credits.</strong> The documentary record places <strong>7 June 2018</strong> as a threshold of de facto material possession/control over Sun Park. <strong>We have not located a judicial delivery of the whole hotel authorising that control on that date.</strong> That sequence requires the case to ask who actually had the capacity to operate, preserve, give access, generate income, execute a rescue or cause/prevent deterioration.',
    definition: '<strong>“Lender in possession” is used here only as a functional comparison.</strong> We do not present it as a Spanish legal status attributed to CAM: descriptively it means <em>secured creditor + de facto material possession/control</em>. Nor does it mean ownership. The Spanish-law question is what title or authority supported each concrete act of control.',
    statuses: [
      ['DOCUMENTED FACT', '20 OCT 2017 → 8 FEB 2018', 'PH122 assigned the credit to CAM and the Mercantile Court later recognised CAM as holder of the mortgage-credit amounts.'],
      ['CONTROL THRESHOLD', '7 JUN 2018', 'The possession/control record places the material shift here. Exact scope by actor, asset and period remains evidence-controlled.'],
      ['OPEN QUESTION', 'PRIOR AUTHORITY', 'No judicial delivery/order of the whole hotel authorising that control on or before 7 June has been located. If one exists, it should be identified by date, terms and perimeter.']
    ],
    timelineTitle: 'The sequence that must not be compressed',
    timeline: [
      ['20 OCT 2017', 'PH122 → CAM', 'Credit assignment. Becoming creditor did not by itself make CAM owner of the hotel.'],
      ['8 FEB 2018', 'CAM recognised as credit holder', 'The Court recognises the assigned mortgage-credit amounts. Credit rights and possession remain distinct questions.'],
      ['7 JUN 2018', 'Material-control threshold', 'The record places the shift to practical de facto possession/control here. This changes the causal baseline.'],
      ['26 JUN 2018', 'Later judicial suspension', 'The suspension follows the control threshold. A later order does not by itself prove prior authority or retrospectively regularise every earlier act.']
    ],
    calTitle: 'Why this materially changes the classification analysis',
    calIntro: 'The classification cannot attribute causation only by formal title or abstract duty. It must incorporate <strong>actual capacity to act</strong>. From 7 June onward, every allegation should pass through a pre/post-control test.',
    calCards: [
      ['1 · COLLABORATION', '<strong>Who could actually deliver, permit or produce?</strong> If keys, areas, staff, security interfaces, operating records or physical access were controlled by another actor, an omission materially dependent on that actor cannot automatically be attributed to the debtor. This does not erase real documentary delays; it separates capacity from fault.'],
      ['2 · PINK / RENT / OPERATION', '<strong>There cannot be one continuous causal line if the material controller changed.</strong> The pre-7 June period, the control event, later operation, later operators and formal adjudication must be separated. Who could generate income, admit guests, preserve rooms or contract operation is part of causation.'],
      ['3 · AGGRAVATION OF INSOLVENCY', '<strong>Any later deterioration or lost opportunity needs a control counterfactual.</strong> Before attributing aggravation to Gil/LPB, the analysis must prove what they could still control after 7 June and what had moved into the practical control of CAM or separately identified actors.'],
      ['4 · AC / ESTATE ADMINISTRATION', '<strong>The AC’s conduct moves to the centre of the analysis.</strong> What did the AC know before 7 June? What did the 18 May security node authorise? Did he consent, tolerate, oppose or seek restoration? Did he require a keys/access inventory or an account of revenues, fruits, expenses, works and access?'],
      ['5 · JUDGE / JUDGMENT 163/2023', '<strong>Material control can be attributed to judicial knowledge only if the evidence-before-actor chain is proved.</strong> If it was before the Judge, the audit asks whether the judgment attributed aggravation without integrating the material controller. A causal omission may be appellate error or an accountability issue; it is not self-proving prevaricación.'],
      ['6 · FORMER ART. 166 · THIRD PARTIES', '<strong>Creditor/controller status does not automatically make CAM an “accomplice”.</strong> It does require the finite question whether a culpability-grounding act involved third-party cooperation with the required subjective threshold and why that participation was — or was not — individualised.']
    ],
    concursoTitle: 'What this requires the rest of Concurso 36/2012 to re-test',
    concursoCards: [
      ['PRESERVATION', 'Pre/post-7 June inventory and condition: who could inspect, maintain, repair, insure and preserve the active estate.'],
      ['ENFORCEMENT / SECURITY', 'Secured-credit status gave creditor rights, but does not itself answer the different question: what authority permitted material control of the asset.'],
      ['VALUATION', 'The May/June 2018 inspection/valuation sequence should be read beside the access/control shift: who could show, measure, preserve or alter the asset, and with what information.'],
      ['RESCUE / FINANCED EXIT', 'If control impaired operation, investor diligence, finance or a route out of insolvency, it becomes a causal variable in value loss and rescue failure.'],
      ['BIDDING / ADJUDICATION', 'Long practical control before later sale can create information, access or operating advantages that must be compared with other interested parties. It does not automatically invalidate adjudication: proof is required.'],
      ['ACCOUNTS / FRUITS / BENEFIT', 'Reconstruct income, bookings, operator payments, security, works, utilities, capex and any benefit received or cost borne during pre-adjudication possession/control.']
    ],
    parallelTitle: 'Parallel lives outside the insolvency do not disappear because the same hotel is the physical setting',
    parallelIntro: 'Sun Park cannot be treated as though every physical, corporate and economic right belonged to LPB. Material control of the hotel opens — or strengthens — separate legal tracks that must preserve their own ownership, jurisdiction, evidence and remedy.',
    parallel: [
      ['LPB · INSOLVENCY LIFE', 'Active estate, creditors, security, rescue, valuation, sale, accounts and classification causation.'],
      ['MATKATOR / THIRD PARTIES', '<strong>Credit against LPB ≠ title to third-party assets.</strong> Each unit/property must follow owner → title → possession → use → works → income → current status.'],
      ['COMMUNITY / SECURITY', 'Minutes, votes, security mandate, keys, guards and common areas have their own authority chain. A security decision is not presumed to transfer ownership or unlimited possession.'],
      ['OPERATORS / COMMERCIALISATION', 'Lava Verde, Club Sei, Meeting Point and later operators require contract, inventory, authority, bookings, commissions, payments and period. Later operation can evidence control, but not the original legal basis on 7 June.'],
      ['WORKS / RICPE / INCENTIVES / FUNDS', 'Licences, projects, financing or public support can show how the asset was represented and who later benefited. They do not retroactively turn 2018 control into ownership or cure a private title/possession defect.'],
      ['AWESWELL / INVESTOR LOSS', 'If material control blocked rescue, operation of separate assets or financing, investor loss may sit on a different plane from LPB-estate loss. Causation and double recovery must be controlled.']
    ],
    defenceTitle: 'The strongest defence — and what remains even after accepting it',
    defence: '<strong>Possible defence:</strong> CAM may say access/control was consensual, security-limited, authorised by the Community or by security rights, that LPB retained meaningful access, that no effective hotel operation was interrupted, or that later court decisions recognised/regularised the position. <strong>What remains:</strong> identify the authority operative on 7 June; its exact perimeter; who held keys/guards/access; what each owner consented to; what the AC did; what income/costs/works arose; and what changed for rescue, value, operation and bidding.',
    productionTitle: 'Finite evidence that would close the controversy',
    production: [
      'Any judicial order, delivery or authorisation effective on or before 7 June 2018 supporting whole-hotel control, if it exists.',
      'Complete minutes, contract and instructions for the 18 May 2018 Community/security node.',
      'Keys, locks, codes, guards, authorisers, invoices, CCTV and access logs.',
      'PMS/bookings, income, operator payments, utilities, works, capex and accounting for fruits/expenses from the control shift to formal adjudication.',
      'Property-by-property map of LPB, Matkator and third parties, plus consent/authority for each.',
      'What evidence of the control event was actually before the AC, Prosecutor and Judge when each classification proposition was made or adopted.'
    ],
    rule: '<strong>Temporal rule:</strong> later adjudication ≠ retrospective authority. <strong>Property rule:</strong> creditor ≠ owner. <strong>Evidence rule:</strong> material control ≠ collective liability of a “perimeter”. <strong>Criminal-law rule:</strong> causal error or omission ≠ offence without independent proof of the subjective element.',
    source: 'Internal control: CALIFICACION_2018_CREDITOR_IN_MATERIAL_POSSESSION_CONTROL_LEDGER_16AUG2026.md · P19_SUN_PARK_MATERIAL_CONTROL_POSSESSION_CONTINUITY_MEETING_POINT_15AUG2026.md · PH122_CAM_ASSIGNMENT_ART1535_PUBLICATION_CONTROL_16AUG2026.md · RECOVERY_CAUSATION_MATRIX_CONCURSO36_15AUG2026.md. Legal frame checked against Ley 22/2003 applicable in 2018 (Arts 40, 43, 55–57, 155, 164, 166 and 172) and Civil Code possession/fruits rules.',
    links: [
      ['7 June 2018 material control →', '../../es/toma-control-sun-park-7-junio-2018/'],
      ['Lender of record →', '../lender-of-record/'],
      ['Sale-lender convergence →', '../sale-lender-convergence/'],
      ['Acosta Matos perimeter →', '../acosta-matos-perimeter/']
    ]
  };

  const style = document.createElement('style');
  style.textContent = `
    .clp18{padding:1rem 0 2.6rem}.clp18-wrap{max-width:1080px;margin:0 auto}.clp18-box{background:#fff;border:2px solid #13252d;border-radius:22px;padding:1.45rem;box-shadow:0 16px 38px rgba(19,37,45,.08)}
    .clp18-eyebrow{font-size:.76rem;letter-spacing:.09em;text-transform:uppercase;font-weight:900;color:#7b2e2e}.clp18 h2{font-size:clamp(1.8rem,3.8vw,2.65rem);line-height:1.05;margin:.4rem 0 .85rem}.clp18-lead{font-size:1.08rem}.clp18-def{background:#f3efe4;border-left:6px solid #8c6b2f;border-radius:14px;padding:1rem 1.1rem;margin:1rem 0}
    .clp18-status{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin:1.15rem 0}.clp18-status article{border:1px solid rgba(19,37,45,.16);border-radius:15px;padding:1rem;background:#fafafa}.clp18-status b,.clp18-card b,.clp18-life b{display:block;font-size:.74rem;letter-spacing:.065em;text-transform:uppercase;color:#6b5841;margin-bottom:.35rem}.clp18-status strong{display:block;margin-bottom:.35rem}
    .clp18-timeline{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem;margin:1rem 0 1.4rem}.clp18-time{background:#13252d;color:#fff;border-radius:14px;padding:1rem}.clp18-time time{font-weight:900;color:#d6b16b;font-size:.78rem}.clp18-time strong{display:block;margin:.35rem 0}.clp18-time p{margin:0;font-size:.91rem;color:#eef1f1}
    .clp18-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem;margin:1rem 0 1.45rem}.clp18-card{border-radius:15px;padding:1rem;background:#f6f7f7;border-top:4px solid #526b59}.clp18-card p{margin:0}.clp18-sub{margin-top:1.5rem}.clp18-lifegrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin:1rem 0}.clp18-life{border:1px solid rgba(19,37,45,.16);border-radius:14px;padding:1rem;background:#fff}.clp18-defence{background:#f5e7e4;border-left:6px solid #7b2e2e;border-radius:14px;padding:1rem 1.1rem;margin:1.2rem 0}.clp18-prod{background:#10252e;color:#fff;border-radius:16px;padding:1.1rem 1.2rem}.clp18-prod h3{margin-top:0}.clp18-prod li{margin:.45rem 0}.clp18-rule{border:1px dashed #8c6b2f;border-radius:14px;padding:1rem;margin:1rem 0;background:#fffaf0}.clp18-links{display:flex;flex-wrap:wrap;gap:.55rem;margin-top:1rem}.clp18-source{font-size:.84rem;color:#5b6265;margin-top:.9rem}
    @media(max-width:820px){.clp18-status,.clp18-timeline,.clp18-lifegrid,.clp18-grid{grid-template-columns:1fr}.clp18-box{border-radius:0}}
  `;
  document.head.appendChild(style);

  const statuses = d.statuses.map(([a,b,c]) => `<article><b>${a}</b><strong>${b}</strong><div>${c}</div></article>`).join('');
  const timeline = d.timeline.map(([a,b,c]) => `<article class="clp18-time"><time>${a}</time><strong>${b}</strong><p>${c}</p></article>`).join('');
  const calCards = d.calCards.map(([a,b]) => `<article class="clp18-card"><b>${a}</b><p>${b}</p></article>`).join('');
  const concursoCards = d.concursoCards.map(([a,b]) => `<article class="clp18-card"><b>${a}</b><p>${b}</p></article>`).join('');
  const parallel = d.parallel.map(([a,b]) => `<article class="clp18-life"><b>${a}</b><div>${b}</div></article>`).join('');
  const production = d.production.map(x => `<li>${x}</li>`).join('');
  const links = d.links.map(([label,href]) => `<a class="button secondary" href="${href}">${label}</a>`).join('');

  const section = document.createElement('section');
  section.className = 'section clp18';
  section.dataset.calCreditorControl20260816 = '1';
  section.innerHTML = `<div class="shell clp18-wrap"><div class="clp18-box">
    <div class="clp18-eyebrow">${d.eyebrow}</div><h2>${d.title}</h2><p class="clp18-lead">${d.lead}</p><div class="clp18-def">${d.definition}</div>
    <div class="clp18-status">${statuses}</div>
    <h3 class="clp18-sub">${d.timelineTitle}</h3><div class="clp18-timeline">${timeline}</div>
    <h3 class="clp18-sub">${d.calTitle}</h3><p>${d.calIntro}</p><div class="clp18-grid">${calCards}</div>
    <h3 class="clp18-sub">${d.concursoTitle}</h3><div class="clp18-grid">${concursoCards}</div>
    <h3 class="clp18-sub">${d.parallelTitle}</h3><p>${d.parallelIntro}</p><div class="clp18-lifegrid">${parallel}</div>
    <div class="clp18-defence"><h3>${d.defenceTitle}</h3><p>${d.defence}</p></div>
    <div class="clp18-prod"><h3>${d.productionTitle}</h3><ol>${production}</ol></div>
    <div class="clp18-rule">${d.rule}</div><div class="clp18-links">${links}</div><p class="clp18-source">${d.source}</p>
  </div></div>`;

  const anchor = document.querySelector('[data-calificacion-radical-20260816]');
  if (anchor) anchor.insertAdjacentElement('afterend', section);
  else {
    const opening = document.querySelector('[data-calificacion-opening-20260816]');
    if (opening) opening.insertAdjacentElement('afterend', section);
    else {
      const hero = document.querySelector('.hero.cal-hero') || document.querySelector('main .hero');
      if (hero) hero.insertAdjacentElement('afterend', section);
    }
  }
})();

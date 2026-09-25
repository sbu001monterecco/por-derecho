(() => {
  const script = document.currentScript;
  if (!script || !document.body) return;

  const cleanPath = location.pathname.replace(/^\/por-derecho/, '').replace(/\/+$/, '/') || '/';
  const isEn = cleanPath.startsWith('/en/');

  const fullRoutes = new Set([
    '/es/ric-private-equity-sun-park/',
    '/es/ricpe-responsabilidad-documental/',
    '/en/ric-private-equity-sun-park/',
    '/en/ricpe-documentary-accountability/'
  ]);
  const compactRoutes = new Set([
    '/es/cnmv-ricpe-verificacion/',
    '/es/concurso-36-2012-administrador-concursal/',
    '/es/concurso-36-2012-responsabilidad-institucional/',
    '/es/acosta-matos-perimetro/',
    '/es/toma-control-sun-park-7-junio-2018/',
    '/es/cadena-instrumentalizacion-ric-fondos-incentivos/',
    '/es/incentivos-regionales-gc836-p06/',
    '/es/snca-fondos-europeos-trazabilidad/',
    '/es/icalpa-recorrido-denuncia-deontologica/',
    '/es/mismo-hotel-multiples-vidas-financieras/',
    '/en/cnmv-ricpe-verification/',
    '/en/insolvency-36-2012-insolvency-administrator/',
    '/en/insolvency-36-2012-institutional-accountability/',
    '/en/acosta-matos-perimeter/',
    '/en/sun-park-takeover-7-june-2018/',
    '/en/institutionalisation-chain-ric-eu-incentives/',
    '/en/regional-incentives-gc836-p06/',
    '/en/snca-eu-funds-traceability/',
    '/en/icalpa-complaint-roadmap/',
    '/en/same-hotel-multiple-financial-lives/'
  ]);

  const full = fullRoutes.has(cleanPath);
  if (!full && !compactRoutes.has(cleanPath)) return;
  if (document.getElementById('institutional-genealogy-2020-2024')) return;

  const css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = new URL('ricpe-santelmo-institutional-genealogy-20260818.css?v=20260818a', script.src).href;
  document.head.appendChild(css);

  const t = isEn ? {
    kicker: 'INSTITUTIONAL GENEALOGY · SOURCE-STATUS CONTROL',
    title: 'A&G, RICPE, the insolvency administrator, San Telmo and RSM: dates before conclusions.',
    intro: 'The reader must be able to see which entities are legally distinct, which relationships are documented, which public events are separate, and which proposed links remain unproved. Professional proximity is a verification trigger, not a finding of wrongdoing.',
    rule: '<strong>Reading rule:</strong> relationship → possible knowledge question → possible duty → evidence of compliance/non-compliance → only then possible breach.',
    legendSolid: 'legal lineage', legendDouble: 'formal relationship', legendDotted: 'documented interaction', legendOpen: 'open / unproved',
    legalLine: 'Legal vehicle line', servicesLine: 'Separate promoter / services line', professionalLine: 'Professional chronology',
    agCap: 'A&G Capital Investment Partners', agCapSub: 'S.C.R., S.A. · original legal-vehicle denomination',
    ricCap: 'RIC Capital Investment Partners', ricCapSub: 'same SCR · later denomination',
    ricpe: 'RIC Private Equity Investment Partners', ricpeSub: 'same SCR · CNMV no. 295',
    agAsesores: 'A&G Asesores Legales, Financieros y Tributarios', agAsesoresSub: 'separate legal/professional entity · RIC promoter/services line',
    notSame: 'NOT THE SAME LEGAL ENTITY',
    borja: 'Francisco de Borja Rodríguez-Batllori Laffitte', borjaSub: 'Concurso 36/2012 insolvency administrator · archived-CV A&G Asesores proposition (primary CV queued)',
    santelmo: 'San Telmo Abogados y Economistas', santelmoSub: 'documented professional/shareholding/economic relationship in the controlled chronology; primary corporate chain queued',
    rsm: 'RSM Spain · 2024', rsmSub: 'San Telmo professional-team integration/incorporation; do not call this a legal merger/absorption without primary proof',
    eventsTitle: 'Two public events. Keep them separate.', eventsSub: 'EVENT IDs prevent the record from collapsing into a single “San Telmo/RICPE webinar”.',
    event2020: 'RICPE investor presentation', event2020Body: 'Sun Park appears in RICPE’s investment/project presentation with Enrique Guerra and Acosta Matos in the controlled audiovisual/material record. The event itself does not establish that San Telmo organised or advised it.',
    event2021: '#UnCaféenSanTelmo · Enrique Guerra', event2021Body: 'San Telmo hosted/published the interview with Enrique Guerra in his RICPE context. The record does not establish that the insolvency administrator prepared, organised or attended it.',
    notSameEvent: 'NOT THE SAME EVENT',
    evidence2020: 'Evidence boundary', evidence2021: 'Evidence boundary',
    whatKnown: 'What the chain can show', whatUnknown: 'What it does not establish',
    knownItems: ['Different A&G legal/professional lines must remain separate.', 'The 11-Nov-2020 RICPE event and 30-Nov-2021 San Telmo event are distinct objects.', 'Enrique Guerra’s RICPE functions and 20-Jul-2021 certification sit on a dated RICPE chronology.', 'The AC–San Telmo relationship is a conflict/disclosure verification question only to the extent supported by source and date.'],
    unknownItems: ['No established direct prior professional relationship between Borja and Enrique Guerra.', 'No proof that San Telmo advised or organised the 2020 RICPE event.', 'No proof that the AC organised or attended the 2021 event.', 'No proof that the unnamed “abandoned complex in Lanzarote” in the 2021 event was Sun Park.', 'No inference of conflict, coordination, breach or crime merely from professional proximity.', 'RSM’s later 2024 integration does not create retrospective responsibility for earlier conduct.'],
    gapsTitle: 'Four finite evidence gaps',
    gaps: [
      ['ST-GAP-01 · A&G CV', 'Recover the primary archived CV and exact legal entity/dates behind the 2009–2010 A&G Asesores proposition.'],
      ['ST-GAP-02 · San Telmo corporate chain', 'Recover primary partner/shareholding records through July 2024, including the stated 500 participaciones and transfer.'],
      ['ST-GAP-03 · 2021 event production', 'Recover invitation, agenda, production/client/conflict records and communications that prove or exclude AC knowledge or participation.'],
      ['ST-GAP-04 · Lanzarote asset identity', 'Use the audiovisual and contextual record to identify or exclude Sun Park as the unnamed complex.']
    ],
    openFull: 'Open complete institutional chronology', data: 'Machine-readable control data',
    compactKicker: 'INSTITUTIONAL CHAIN · TWO-EVENT CONTROL',
    compactTitle: 'Do not collapse professional history and two separate public events into one connection.',
    directOpen: 'Borja ↔ Enrique Guerra direct link', directOpenSub: 'NOT ESTABLISHED · primary evidence required',
    miniAandG: 'A&G lines', miniAandGSub: 'SCR legal lineage ≠ A&G Asesores identity',
    miniBorja: 'AC / Borja', miniBorjaSub: 'Concurso 36/2012 · dated professional history',
    miniSanTelmo: 'San Telmo', miniSanTelmoSub: '2021 host/publisher; AC relationship separately source-controlled',
    miniRsm: 'RSM · 2024', miniRsmSub: 'later integration, not retrospective responsibility',
    miniWarning: '<strong>Boundary:</strong> the 2020 RICPE presentation and 2021 San Telmo interview are separate events. The unnamed Lanzarote complex is not labelled Sun Park without source closure.'
  } : {
    kicker: 'GENEALOGÍA INSTITUCIONAL · CONTROL DE ESTADO PROBATORIO',
    title: 'A&G, RICPE, el Administrador Concursal, San Telmo y RSM: fechas antes que conclusiones.',
    intro: 'El lector debe poder ver qué entidades son jurídicamente distintas, qué relaciones están documentadas, qué actos públicos son separados y qué nexos propuestos siguen sin probar. La proximidad profesional activa una comprobación; no constituye un hallazgo de conducta impropia.',
    rule: '<strong>Regla de lectura:</strong> relación → posible cuestión de conocimiento → posible deber → prueba de cumplimiento/incumplimiento → sólo entonces posible infracción.',
    legendSolid: 'línea jurídica', legendDouble: 'relación formal', legendDotted: 'interacción documentada', legendOpen: 'abierto / no probado',
    legalLine: 'Línea jurídica del vehículo', servicesLine: 'Línea promotora / servicios separada', professionalLine: 'Cronología profesional',
    agCap: 'A&G Capital Investment Partners', agCapSub: 'S.C.R., S.A. · denominación original de la línea jurídica del vehículo',
    ricCap: 'RIC Capital Investment Partners', ricCapSub: 'misma SCR · denominación posterior',
    ricpe: 'RIC Private Equity Investment Partners', ricpeSub: 'misma SCR · CNMV nº 295',
    agAsesores: 'A&G Asesores Legales, Financieros y Tributarios', agAsesoresSub: 'persona jurídica/profesional separada · línea promotora/servicios RIC',
    notSame: 'NO ES LA MISMA PERSONA JURÍDICA',
    borja: 'Francisco de Borja Rodríguez-Batllori Laffitte', borjaSub: 'Administrador Concursal · Concurso 36/2012 · proposición de CV archivado sobre A&G Asesores (CV primario pendiente)',
    santelmo: 'San Telmo Abogados y Economistas', santelmoSub: 'relación profesional/societaria/económica documentada en la cronología controlada; cadena corporativa primaria pendiente',
    rsm: 'RSM Spain · 2024', rsmSub: 'integración/incorporación del equipo profesional de San Telmo; no llamar fusión/absorción jurídica sin prueba primaria',
    eventsTitle: 'Dos actos públicos. No deben fusionarse.', eventsSub: 'Los IDs de evento impiden convertir el expediente en un único “webinar San Telmo/RICPE”.',
    event2020: 'Presentación RICPE a inversores', event2020Body: 'Sun Park figura en la presentación de inversión/proyectos de RICPE con Enrique Guerra y Acosta Matos en el corpus audiovisual/material controlado. El acto no acredita que San Telmo lo organizara o asesorara.',
    event2021: '#UnCaféenSanTelmo · Enrique Guerra', event2021Body: 'San Telmo alojó/publicó la entrevista a Enrique Guerra en su contexto RICPE. El registro no acredita que el Administrador Concursal preparara, organizara o asistiera al acto.',
    notSameEvent: 'NO ES EL MISMO ACTO',
    evidence2020: 'Límite probatorio', evidence2021: 'Límite probatorio',
    whatKnown: 'Qué puede mostrar la cadena', whatUnknown: 'Qué no establece',
    knownItems: ['Las distintas líneas A&G deben permanecer jurídicamente separadas.', 'El acto RICPE de 11-nov-2020 y el acto San Telmo de 30-nov-2021 son objetos probatorios distintos.', 'Las funciones RICPE de Enrique Guerra y la certificación de 20-jul-2021 forman una cronología fechada.', 'La relación AC–San Telmo plantea una comprobación de conflicto/revelación sólo en la medida sustentada por fuente y fecha.'],
    unknownItems: ['No se ha establecido una relación profesional directa previa entre Borja y Enrique Guerra.', 'No consta que San Telmo asesorara u organizara el acto RICPE de 2020.', 'No consta que el AC organizara o asistiera al acto San Telmo de 2021.', 'No consta que el “complejo abandonado en Lanzarote” sin identificar del acto de 2021 fuese Sun Park.', 'La proximidad profesional no prueba por sí sola conflicto, coordinación, infracción o delito.', 'La posterior integración en RSM en 2024 no crea responsabilidad retrospectiva por hechos anteriores.'],
    gapsTitle: 'Cuatro lagunas probatorias finitas',
    gaps: [
      ['ST-GAP-01 · CV A&G', 'Recuperar el CV archivado primario y la entidad jurídica/fechas exactas tras la proposición A&G Asesores 2009–2010.'],
      ['ST-GAP-02 · cadena societaria San Telmo', 'Recuperar registros primarios de socio/participaciones hasta julio de 2024, incluidas las 500 participaciones y su transmisión descrita.'],
      ['ST-GAP-03 · producción del acto 2021', 'Recuperar invitación, agenda, producción, clientes/conflictos y comunicaciones que confirmen o excluyan conocimiento o participación del AC.'],
      ['ST-GAP-04 · identidad del activo Lanzarote', 'Usar el audiovisual y el contexto para identificar o excluir Sun Park como el complejo no nombrado.']
    ],
    openFull: 'Abrir la cronología institucional completa', data: 'Datos de control legibles por máquina',
    compactKicker: 'CADENA INSTITUCIONAL · CONTROL DE DOS ACTOS',
    compactTitle: 'No confunda una historia profesional y dos actos públicos distintos con una sola conexión.',
    directOpen: 'Nexo directo Borja ↔ Enrique Guerra', directOpenSub: 'NO ESTABLECIDO · requiere prueba primaria',
    miniAandG: 'Líneas A&G', miniAandGSub: 'línea jurídica SCR ≠ identidad con A&G Asesores',
    miniBorja: 'AC / Borja', miniBorjaSub: 'Concurso 36/2012 · historia profesional fechada',
    miniSanTelmo: 'San Telmo', miniSanTelmoSub: 'anfitrión/editor 2021; relación AC controlada por separado',
    miniRsm: 'RSM · 2024', miniRsmSub: 'integración posterior, no responsabilidad retrospectiva',
    miniWarning: '<strong>Límite:</strong> la presentación RICPE de 2020 y la entrevista San Telmo de 2021 son actos distintos. El complejo de Lanzarote no se etiqueta como Sun Park sin cierre probatorio.'
  };

  const canonicalHref = new URL('../ric-private-equity-sun-park/#genealogia', location.href).href;
  const dataHref = new URL('data/ricpe-santelmo-institutional-genealogy-v1.json', script.src).href;

  const list = items => `<ul>${items.map(x => `<li>${x}</li>`).join('')}</ul>`;
  const gaps = t.gaps.map(([name, text]) => `<div class="ig-gap"><strong>${name}</strong>${text}</div>`).join('');

  const fullMarkup = `
    <div class="ig-shell">
      <div class="ig-head">
        <div><p class="ig-kicker">${t.kicker}</p><h2>${t.title}</h2><p class="ig-intro">${t.intro}</p></div>
        <div class="ig-rule">${t.rule}</div>
      </div>
      <div class="ig-legend" aria-label="${isEn ? 'Relationship legend' : 'Leyenda de relaciones'}">
        <span><i></i>${t.legendSolid}</span><span class="double"><i></i>${t.legendDouble}</span><span class="dotted"><i></i>${t.legendDotted}</span><span class="open"><i></i>${t.legendOpen}</span>
      </div>
      <div class="ig-grid">
        <article class="ig-lane"><h3>${t.legalLine}</h3>
          <div class="ig-node"><strong>${t.agCap}</strong><small>${t.agCapSub}</small></div><div class="ig-connector">↓</div>
          <div class="ig-node"><strong>${t.ricCap}</strong><small>${t.ricCapSub}</small></div><div class="ig-connector">↓</div>
          <div class="ig-node"><strong>${t.ricpe}</strong><small>${t.ricpeSub}</small></div>
        </article>
        <article class="ig-lane"><h3>${t.servicesLine}</h3>
          <div class="ig-node"><strong>${t.agAsesores}</strong><small>${t.agAsesoresSub}</small></div><div class="ig-connector open">≠</div>
          <div class="ig-node not-established"><strong>${t.notSame}</strong><small>${isEn ? 'Do not bridge the two A&G lines by shorthand.' : 'No unir las dos líneas A&G mediante abreviatura.'}</small></div>
          <details><summary>${isEn ? 'Why this matters' : 'Por qué importa'}</summary><p>${isEn ? 'A shared A&G label cannot substitute for a corporate identity, mandate or knowledge chain.' : 'Una etiqueta A&G compartida no sustituye identidad societaria, mandato ni cadena de conocimiento.'}</p></details>
        </article>
        <article class="ig-lane"><h3>${t.professionalLine}</h3>
          <div class="ig-node open"><strong>${t.borja}</strong><small>${t.borjaSub}</small></div><div class="ig-connector double">⇓</div>
          <div class="ig-node"><strong>${t.santelmo}</strong><small>${t.santelmoSub}</small></div><div class="ig-connector">↓</div>
          <div class="ig-node"><strong>${t.rsm}</strong><small>${t.rsmSub}</small></div>
        </article>
      </div>
      <div class="ig-event-wrap">
        <div class="ig-event-title"><h3>${t.eventsTitle}</h3><span>${t.eventsSub}</span></div>
        <div class="ig-events">
          <article class="ig-event"><time>EVENT-RICPE-2020-11-11 · 11 NOV 2020</time><h4>${t.event2020}</h4><p>${t.event2020Body}</p><details><summary>${t.evidence2020}</summary>${list(isEn ? ['RICPE event ≠ San Telmo event.', 'Public presentation proves what was represented, not the truth of every underlying title proposition.', 'No San Telmo adviser/organiser role is established for this event.'] : ['Acto RICPE ≠ acto San Telmo.', 'La presentación pública prueba lo manifestado, no la veracidad de toda premisa de título.', 'No se ha establecido un papel de San Telmo como asesor/organizador de este acto.'])}</details></article>
          <div class="ig-not-same">${t.notSameEvent}</div>
          <article class="ig-event"><time>EVENT-SANTELMO-2021-11-30 · 30 NOV 2021</time><h4>${t.event2021}</h4><p>${t.event2021Body}</p><details><summary>${t.evidence2021}</summary>${list(isEn ? ['San Telmo host/publisher and Enrique Guerra interviewee are the documented public interaction.', 'Direct Borja–Guerra professional relationship: NOT ESTABLISHED.', 'Unnamed Lanzarote complex = Sun Park: OPEN.'] : ['San Telmo como anfitrión/editor y Enrique Guerra como entrevistado son la interacción pública documentada.', 'Relación profesional directa Borja–Guerra: NO ESTABLECIDA.', 'Complejo de Lanzarote sin nombrar = Sun Park: ABIERTO.'])}</details></article>
        </div>
      </div>
      <div class="ig-boundaries">
        <article class="known"><h3>${t.whatKnown}</h3>${list(t.knownItems)}</article>
        <article class="unknown"><h3>${t.whatUnknown}</h3>${list(t.unknownItems)}</article>
      </div>
      <div class="ig-open-evidence"><h3>${t.gapsTitle}</h3><div class="ig-gap-grid">${gaps}</div></div>
      <div class="ig-cta"><a class="ig-link" href="${canonicalHref}">${t.openFull} →</a><a class="ig-link secondary" href="${dataHref}">${t.data} →</a></div>
    </div>`;

  const compactMarkup = `
    <div class="ig-shell">
      <div class="ig-head"><div><p class="ig-kicker">${t.compactKicker}</p><h2>${t.compactTitle}</h2><p class="ig-intro">${t.intro}</p></div></div>
      <div class="ig-mini-chain">
        <div class="ig-mini"><small>01</small><strong>${t.miniAandG}</strong><small>${t.miniAandGSub}</small></div>
        <div class="ig-mini"><small>02</small><strong>${t.miniBorja}</strong><small>${t.miniBorjaSub}</small></div>
        <div class="ig-mini"><small>03</small><strong>${t.miniSanTelmo}</strong><small>${t.miniSanTelmoSub}</small></div>
        <div class="ig-mini not-established"><small>04</small><strong>${t.directOpen}</strong><small>${t.directOpenSub}</small></div>
        <div class="ig-mini"><small>05</small><strong>${t.miniRsm}</strong><small>${t.miniRsmSub}</small></div>
      </div>
      <div class="ig-mini-events">
        <article class="ig-mini-event"><time>EVENT-RICPE-2020-11-11</time><strong>${t.event2020}</strong><p>${t.event2020Body}</p></article>
        <article class="ig-mini-event"><time>EVENT-SANTELMO-2021-11-30</time><strong>${t.event2021}</strong><p>${t.event2021Body}</p></article>
      </div>
      <div class="ig-mini-warning">${t.miniWarning}</div>
      <div class="ig-cta"><a class="ig-link" href="${canonicalHref}">${t.openFull} →</a><a class="ig-link secondary" href="${dataHref}">${t.data} →</a></div>
    </div>`;

  const section = document.createElement('section');
  section.id = 'institutional-genealogy-2020-2024';
  section.className = `section ig26${full ? '' : ' compact'}`;
  section.setAttribute('data-source-control', 'ricpe-santelmo-institutional-genealogy-v1');
  section.innerHTML = full ? fullMarkup : compactMarkup;

  const main = document.querySelector('main');
  if (!main) return;

  if (full) {
    const genealogy = document.getElementById('genealogia');
    if (genealogy && genealogy.parentNode) {
      genealogy.insertAdjacentElement('afterend', section);
      return;
    }
  }

  const firstSection = main.querySelector(':scope > section');
  const thesis = main.querySelector('[data-calificacion-misuse-thesis]');
  if (thesis || firstSection) (thesis || firstSection).insertAdjacentElement('afterend', section);
  else main.prepend(section);
})();

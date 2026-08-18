(() => {
  const path = window.location.pathname;
  const integrationMarker = 'CGPJ_ALERT_VISUAL_INTEGRATION_V1';

  const isSpanish = path.includes('/es/');
  const isEnglish = path.includes('/en/');
  const visualHref = isSpanish
    ? '/por-derecho/es/cgpj-alerta-irreversibilidad/'
    : '/por-derecho/en/cgpj-alert-to-irreversibility/';

  const bridgeRoutes = [
    {
      match: '/es/cgpj-comision-permanente-sala-lectura/',
      target: '.rr-hero',
      kicker: 'MAPA VISUAL · LEER JUNTO A LOS SIETE NÚCLEOS',
      title: 'Alerta RICPE 2021 → tratamiento concursal → título → irreversibilidad',
      body: 'El mapa coloca la alerta, la oposición de CAM y de la Administración Concursal, el conocimiento judicial documentado, la bifurcación de enero de 2022 y el tempo hasta testimonio, escritura y Registro en una sola secuencia. Después abre, como consecuencias separadas y no como conocimiento judicial histórico automático, los carriles RIC/RICPE, incentivo regional/FEDER, transformación física y daño extraconcursal de Matkator/terceros.',
      cta: 'Abrir mapa visual completo →'
    },
    {
      match: '/en/cgpj-permanent-commission-reader-room/',
      target: '.rr-hero',
      kicker: 'VISUAL MAP · READ WITH THE SEVEN NUCLEI',
      title: '2021 RICPE alert → insolvency treatment → title → irreversibility',
      body: 'The map places the alert, CAM and Insolvency Administration opposition, documented judicial availability, the January 2022 decisional fork and the tempo to testimony, deed and Registry in one sequence. It then opens RIC/RICPE, regional-incentive/FEDER, physical-transformation and Matkator/third-party extra-insolvency consequences as separate downstream lanes, not automatic historical judicial knowledge.',
      cta: 'Open the full visual map →'
    },
    {
      match: '/es/concurso-36-2012-magistrado-juez/',
      target: '.hero',
      kicker: 'CONTEXTO VISUAL · NO ES UNA NUEVA IMPUTACIÓN',
      title: 'Ver dónde la alerta entra en la matriz de conocimiento y qué ocurrió después',
      body: 'La relevancia para el Magistrado no nace de todo lo que ocurrió después. El mapa separa el momento en que la alerta RICPE/título/perímetro fue puesta en el expediente de las consecuencias posteriores —Registro, obras, financiación, incentivos y explotación— y pregunta qué control independiente concilió ambos planos antes de cada paso difícilmente reversible.',
      cta: 'Ver alerta → decisión → irreversibilidad →'
    },
    {
      match: '/en/insolvency-36-2012-mercantile-court-1/',
      target: '.hero',
      kicker: 'VISUAL CONTEXT · NOT A NEW ALLEGATION',
      title: 'See where the alert enters the knowledge matrix and what happened afterwards',
      body: 'The judge-facing relevance does not arise from everything that happened later. The map separates the point at which the RICPE/title/perimeter alert entered the record from later Registry, works, finance, incentives and operation, and asks what independent control reconciled those planes before each hard-to-reverse step.',
      cta: 'View alert → decision → irreversibility →'
    },
    {
      match: '/es/cgpj-supervision-masa-activa/',
      target: '.ms-hero',
      kicker: 'VISUAL · PROTECCIÓN DEL ACTIVO E IRREVERSIBILIDAD',
      title: 'La supervisión se entiende mejor viendo cuándo aumentó el coste de corregir',
      body: 'El mapa conecta la alerta con los controles de masa activa, el tratamiento de la Administración Concursal y la secuencia que terminó en título, Registro, reforma, financiación y explotación. Las consecuencias posteriores se muestran como contexto de irreversibilidad, no como prueba automática de conocimiento o intención judicial anterior.',
      cta: 'Abrir mapa de irreversibilidad →'
    },
    {
      match: '/en/cgpj-insolvency-estate-supervision/',
      target: '.ms-hero',
      kicker: 'VISUAL · ESTATE PROTECTION AND IRREVERSIBILITY',
      title: 'Supervision is easier to assess when the rising cost of correction is visible',
      body: 'The map connects the alert to estate-protection controls, Insolvency Administration treatment and the sequence ending in title, Registry, refurbishment, finance and operation. Later consequences are shown as irreversibility context, not automatic proof of earlier judicial knowledge or intent.',
      cta: 'Open the irreversibility map →'
    },
    {
      match: '/es/ric-private-equity-sun-park/',
      target: '#alerta-2021-que-se-comunico',
      kicker: 'PUENTE AL CGPJ · CUÁNDO LA CUESTIÓN EXTERNA ENTRA EN EL CONCURSO',
      title: 'La relevancia judicial empieza por la incorporación documentada, no por la existencia de RICPE',
      body: 'Este mapa muestra el punto exacto en el que la cuestión RICPE/título/perímetro deja de ser sólo contexto externo y pasa a formar parte del problema concursal documentado. Después separa los efectos posteriores —RIC, incentivo regional, FEDER, HNT/MYND— para evitar convertirlos retroactivamente en conocimiento judicial.',
      cta: 'Ver el puente RICPE → Concurso → resultado →'
    },
    {
      match: '/en/ric-private-equity-sun-park/',
      target: '#alerta-2021-que-se-comunico, #alert-2021-what-was-communicated',
      kicker: 'CGPJ BRIDGE · WHEN THE EXTERNAL ISSUE ENTERS THE INSOLVENCY',
      title: 'Judicial relevance begins with documented incorporation, not with RICPE merely existing',
      body: 'The map identifies the point at which the RICPE/title/perimeter issue moves from external context into the documented insolvency problem. It then keeps later RIC, regional-incentive, FEDER and HNT/MYND consequences separate so they are not retroactively converted into judicial knowledge.',
      cta: 'View RICPE → insolvency → outcome bridge →'
    },
    {
      match: '/es/cadena-instrumentalizacion-ric-fondos-incentivos/',
      target: 'main > section:first-of-type',
      kicker: 'CONTEXTO CGPJ · RELIANCE PÚBLICO POSTERIOR',
      title: 'Los fondos e incentivos aparecen después en el mapa, no como conocimiento judicial histórico',
      body: 'El vínculo con el CGPJ es de consecuencia, dependencia institucional e irreversibilidad salvo que una fuente pruebe incorporación anterior al expediente judicial. El mapa mantiene separadas RIC, incentivo regional y conexión FEDER y exige el expediente de cada sistema antes de inferir solapamiento, irregularidad o causalidad.',
      cta: 'Ver dónde encajan los fondos en la secuencia →'
    },
    {
      match: '/en/institutionalisation-chain-ric-eu-incentives/',
      target: 'main > section:first-of-type',
      kicker: 'CGPJ CONTEXT · LATER PUBLIC RELIANCE',
      title: 'Public funding and incentives sit downstream in the map, not as historical judicial knowledge',
      body: 'Their CGPJ relevance is consequence, institutional reliance and irreversibility unless a source proves earlier incorporation into the judicial file. The map keeps RIC, regional incentive and the identified FEDER connection separate and requires each underlying file before inferring overlap, irregularity or causation.',
      cta: 'See where public funding enters the sequence →'
    },
    {
      match: '/es/ricpe-idoneidad-series-f-g/',
      target: 'main > section:first-of-type',
      kicker: 'CONTEXTO CGPJ · CAPAS FINANCIERAS POSTERIORES',
      title: 'Series F/G se muestran como reliance y trazabilidad posteriores',
      body: 'El mapa no usa la coexistencia de instrumentos como prueba de doble financiación. La conecta al resultado posterior para mostrar por qué la trazabilidad de título, elegibilidad, uso y control se vuelve más importante una vez consolidada la operación.',
      cta: 'Abrir mapa causal completo →'
    },
    {
      match: '/en/ricpe-idoneidad-series-f-g/',
      target: 'main > section:first-of-type',
      kicker: 'CGPJ CONTEXT · LATER FINANCIAL LAYERS',
      title: 'Series F/G are shown as later reliance and traceability layers',
      body: 'The map does not use coexistence of instruments as proof of double financing. It connects them to the later result to show why title, eligibility, use and control traceability becomes more important once the operation is consolidated.',
      cta: 'Open the full causal map →'
    },
    {
      match: '/es/toma-control-sun-park-7-junio-2018/',
      target: '#perimetros-juridicos',
      kicker: 'PUENTE EXTRACONCURSAL · MATKATOR Y TERCEROS',
      title: 'La visualización convierte el límite LPB / fuera de LPB en una pregunta de supervisión',
      body: 'El mapa no afirma que el Juzgado transmitiera bienes de Matkator. Pregunta qué puente jurídico autorizó cada efecto material alegado fuera de la masa —acceso, obras, uso, ingresos o integración operativa— y quién lo verificó.',
      cta: 'Ver el carril extraconcursal en el mapa →'
    },
    {
      match: '/en/sun-park-takeover-7-june-2018/',
      target: '#perimetros-juridicos, #legal-perimeters',
      kicker: 'EXTRA-INSOLVENCY BRIDGE · MATKATOR AND THIRD PARTIES',
      title: 'The visual turns the LPB / outside-LPB boundary into a supervision question',
      body: 'The map does not state that the Court transferred Matkator property. It asks what legal bridge authorised each alleged practical effect outside the estate — access, works, use, revenue or operational integration — and who verified it.',
      cta: 'View the extra-insolvency lane →'
    },
    {
      matchExact: '/por-derecho/es/',
      target: '#institutional-accountability-12aug',
      kicker: 'CGPJ · LECTURA INSTITUCIONAL VISUAL',
      title: 'Una entrada directa a la secuencia alerta → decisión → irreversibilidad',
      body: 'Para lectores institucionales, el mapa evita recorrer primero toda la historia: empieza por la alerta RICPE 2021, su oposición y tratamiento concursal, y sólo después abre las consecuencias RICPE, fondos/incentivos, operación y perímetro extraconcursal.',
      cta: 'Abrir mapa CGPJ →'
    },
    {
      matchExact: '/por-derecho/en/',
      target: '#institutional-accountability-12aug-en',
      kicker: 'CGPJ · VISUAL INSTITUTIONAL READ',
      title: 'A direct route through alert → decision → irreversibility',
      body: 'For institutional readers, the map avoids forcing a tour of the entire case first: it starts with the 2021 RICPE alert, opposition and insolvency treatment, then opens the later RICPE, public-funding, operation and extra-insolvency consequences.',
      cta: 'Open CGPJ map →'
    }
  ];

  const route = bridgeRoutes.find((item) => item.matchExact ? path === item.matchExact : path.includes(item.match));
  if (route && !document.querySelector('[data-cgpj-alert-visual-bridge]')) {
    const target = document.querySelector(route.target);
    if (target) {
      const section = document.createElement('section');
      section.className = 'section alt';
      section.dataset.cgpjAlertVisualBridge = integrationMarker;
      section.innerHTML = `
        <div class="shell">
          <aside style="border-left:5px solid #315c7b;background:#f4f7f8;padding:1.15rem 1.25rem;border-radius:14px">
            <p class="kicker" style="margin-top:0">${route.kicker}</p>
            <h2 style="margin:.25rem 0 .65rem">${route.title}</h2>
            <p>${route.body}</p>
            <div class="actions" style="margin-top:.9rem"><a class="button" href="${visualHref}">${route.cta}</a></div>
          </aside>
        </div>`;
      target.insertAdjacentElement('afterend', section);
    }
  }

  const es = path.includes('/es/mensaje-abierto-cgpj/');
  const en = path.includes('/en/open-message-cgpj/');
  if (!es && !en) return;
  if (document.querySelector('[data-cgpj-regage-28jul]')) return;

  const target = document.querySelector('#caso, #case');
  if (!target) return;

  const box = document.createElement('aside');
  box.dataset.cgpjRegage28jul = 'true';
  box.className = 'cg-note';
  box.style.marginTop = '1.25rem';
  box.innerHTML = es
    ? `<strong>Actualización documental · cronología verificada a 16 de agosto de 2026.</strong> El archivo original de DI 169/2026 fue acordado el <strong>14 de mayo</strong>. El recurso fue firmado y formalmente presentado por AGE/RedSARA el <strong>15 de junio de 2026</strong> bajo <code>REGAGE26e00056359487</code>, con cuatro archivos. La Sección de Recursos comunicó después que el recurso había tenido entrada en el CGPJ el <strong>18 de junio</strong>, que se tramitaba como <strong>Alzada 286/2026</strong> y que el escrito presentado el <strong>15 de julio</strong> quedaba unido al expediente. Una notificación oficial 060 añade un tercer estado registral para el recurso: el <strong>22 de junio</strong> figura como enviado a destino al Registro General del CGPJ. Esos estados distintos no prueban por sí solos irregularidad; el índice y la trazabilidad interna deben reconciliarlos. El acuerdo del Promotor de <strong>10 de julio</strong> se mantuvo en el archivo del 14 de mayo y su texto primario no acredita una remisión al Servicio de Inspección. El módulo específico LPAM–Magistrado no figura entre los cuatro archivos del justificante de 15 de junio; su primera presentación formal actualmente verificada en la alzada es la aportación de <strong>28 de julio</strong>, <code>REGAGE26e00069061338</code>, con cinco PDF. El justificante del 28 de julio identifica la Unidad de Registro y Archivo; una notificación 060 del <strong>30 de julio</strong> registra su envío al Registro General del CGPJ. <strong>Presentación o encaminamiento registral ≠ incorporación al expediente ≠ examen ≠ aceptación ≠ veracidad de las alegaciones.</strong> La unión del escrito de 15 de julio sí fue expresamente confirmada por Recursos; no se ha localizado confirmación equivalente de incorporación o examen sustantivo del paquete de 28 de julio. Hasta el 16 de agosto no se ha localizado en el correo revisado una resolución sustantiva posterior de la Alzada 286/2026.`
    : `<strong>Documentary update · chronology verified to 16 August 2026.</strong> The original DI 169/2026 archive was agreed on <strong>14 May</strong>. The appeal was signed and formally presented through AGE/RedSARA on <strong>15 June 2026</strong> under <code>REGAGE26e00056359487</code>, with four files. The CGPJ Appeals Section later stated that the appeal had entered the CGPJ on <strong>18 June</strong>, was being processed as <strong>Appeal 286/2026</strong>, and that the filing presented on <strong>15 July</strong> was joined to the appellate record. An official 060 notice adds a third registry state for the appeal: on <strong>22 June</strong> it is recorded as sent to destination at the CGPJ General Registry. Those distinct states do not by themselves prove irregularity; the administrative index and internal routing record are needed to reconcile them. The Promotor's <strong>10 July</strong> agreement remained with the 14 May archive and its primary text does not establish a referral to the Inspection Service. The specific LPAM–Judge module is not among the four files listed on the 15 June receipt; its first currently verified formal presentation in the appeal route is the <strong>28 July</strong> five-PDF supplement, <code>REGAGE26e00069061338</code>. The 28 July receipt identifies the Registry and Archive Unit; an official 060 notice dated <strong>30 July</strong> records onward routing to the CGPJ General Registry. <strong>Presentation or registry routing ≠ incorporation into the file ≠ examination ≠ acceptance ≠ truth of the allegations.</strong> Joinder of the 15 July filing was expressly confirmed by Appeals; no equivalent confirmation of incorporation or substantive examination of the 28 July package has been located. Through 16 August, no later substantive Appeal 286/2026 decision was located in the reviewed email.`;

  const shell = target.querySelector('.shell');
  if (shell) shell.appendChild(box);
})();

(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/+$/, '');
  const isEnDossier = path.endsWith('/en/sun-park-takeover-7-june-2018');
  const isEsDossier = path.endsWith('/es/toma-control-sun-park-7-junio-2018');
  const isEnHome = /\/en$/.test(path);
  const isEsHome = /\/es$/.test(path);
  if (!isEnDossier && !isEsDossier && !isEnHome && !isEsHome) return;

  const isEs = isEsDossier || isEsHome;
  const lang = isEs ? 'es' : 'en';
  const marker = `/${lang}`;
  const markerIndex = path.lastIndexOf(marker);
  const root = markerIndex >= 0 ? path.slice(0, markerIndex) : '';
  const link = (suffix = '') => `${root}/${lang}/${suffix}`;

  const routes = isEs ? {
    home: link(''),
    dossier: link('toma-control-sun-park-7-junio-2018/'),
    business: `${link('')}#plataforma-construida-2011-2018`,
    ownership: link('comunidad-instrumentalizacion/'),
    precursor: `${link('toma-control-sun-park-7-junio-2018/')}#preparacion`,
    day: `${link('toma-control-sun-park-7-junio-2018/')}#hechos-7-junio`,
    after: `${link('toma-control-sun-park-7-junio-2018/')}#desplazamiento-beneficio`,
    multiple: link('mismo-hotel-multiples-vidas-financieras/'),
    calificacion: link('calificacion-concurso-36-2012-vidas-paralelas/'),
    community: link('comunidad-instrumentalizacion/'),
    lava: link('lava-verde-club-sei-meeting-point/'),
    ricpe: link('ric-private-equity-sun-park/'),
    recovery: link('objetivos-recuperacion-restitucion/')
  } : {
    home: link(''),
    dossier: link('sun-park-takeover-7-june-2018/'),
    business: `${link('')}#platform-built-2011-2018`,
    ownership: link('community-instrumentalisation/'),
    precursor: `${link('sun-park-takeover-7-june-2018/')}#preparation`,
    day: `${link('sun-park-takeover-7-june-2018/')}#events-of-7-june`,
    after: `${link('sun-park-takeover-7-june-2018/')}#displacement-and-benefit`,
    multiple: link('same-hotel-multiple-financial-lives/'),
    calificacion: link('insolvency-classification-parallel-lives/'),
    community: link('community-instrumentalisation/'),
    lava: link('lava-verde-club-sei-meeting-point/'),
    ricpe: link('ric-private-equity-sun-park/'),
    recovery: link('recovery-restitution-objectives/')
  };

  const t = isEs ? {
    title: '7 junio 2018: el día en que las líneas jurídica, física, operativa y comercial dejaron de coincidir.',
    lead: 'El expediente controlado acredita un cambio material en acceso, seguridad y control práctico. El título formal sobre el principal perímetro LPB llegó años después. Esta página mantiene separados esos hechos y permite seguir, en paralelo, qué ocurrió con el hotel, el concurso, los derechos de terceros, la operación, la financiación y las representaciones posteriores.',
    homeEyebrow: '7 JUNIO 2018 · EL PUNTO DE INFLEXIÓN',
    homeTitle: 'Un hotel en funcionamiento, un concurso, propiedad fragmentada y un proyecto emergente convergieron alrededor de una fecha.',
    homeLead: 'La prueba apoya un cambio material en acceso y control práctico; el título formal sobre las fincas LPB llegó años después. El dossier separa lo ocurrido antes, el propio 7 de junio y las consecuencias posteriores.',
    explore: 'Explorar el punto de inflexión',
    multiple: 'Ver las vidas paralelas del mismo hotel',
    before: 'ANTES DEL 7 DE JUNIO',
    beforeShort: 'Hotel operativo · clientes · equipo · mantenimiento · financiación/salida · títulos fragmentados.',
    hinge: '7 JUNIO 2018',
    hingeShort: 'Cambio material de acceso/seguridad/control práctico. No es una fecha de título integral.',
    after: 'DESPUÉS',
    afterShort: 'Acceso, clientes, personal, inspecciones, proyecto, relato, financiación y título siguieron cronologías distintas.',
    gatewayEyebrow: 'DOSSIER DE CONVERGENCIA · LECTURA CONTROLADA',
    fourClocks: 'Cuatro relojes que no avanzaron juntos',
    fourClocksLead: 'La pregunta no es qué relato “gana”, sino qué documento autorizó cada transición en su fecha y qué sabía cada actor en ese momento.',
    clocks: [
      ['RELOJ JURÍDICO / TÍTULO', 'Concurso 36/2012 → liquidación / impugnaciones / suspensión → adjudicación → escritura / inscripción.'],
      ['RELOJ FÍSICO / OPERATIVO', 'Hotel en funcionamiento → accesos / mediciones previas → 7-Jun cambio práctico → exclusión / disrupción → obras / operación sucesora.'],
      ['RELOJ COMERCIAL / FINANCIERO', 'Sun Park → reposicionamiento → Lava Verde → Club Sei / Meeting Point → RICPE → HNT / MYND → financiación / ayudas.'],
      ['RELOJ INSTITUCIONAL / CONOCIMIENTO', 'Comunidad / AC / Juzgado / Fiscalía / CNMV / RIC / turismo / incentivos-FEDER → qué recibió cada uno, cuándo y qué hizo.']
    ],
    rule: 'Regla de lectura: recepción ≠ examen ≠ conocimiento personal ≠ deber ≠ decisión ≠ responsabilidad.',
    beforeAfterTitle: 'Antes → 7 de junio → después',
    beforeItems: ['hotel ocupado/activo según la prueba controlada', 'clientes, relaciones de estancia y demanda repetida', 'personal, mantenimiento y capacidad de servicio', 'reformas graduales y rutas de operador/financiación', 'propiedad fragmentada; LPB seguía en concurso', 'no existía la adjudicación/título LPB de 2022'],
    dayItems: ['cambios de acceso y seguridad documentados', 'cerraduras/bombines/cadenas/candados donde la fuente lo sostiene', 'presencia/implantación de seguridad privada', 'exclusión del acceso normal', 'autoridad invocada y perímetro jurídico a reconciliar', 'alcance finca por finca todavía abierto'],
    afterItems: ['quién controló qué accesos y áreas', 'qué ocurrió con personal, clientes y pertenencias', 'reservas, contacto con clientes y socios comerciales', 'quién pudo inspeccionar, medir, mantener o ejecutar obras', 'Lava Verde / Club Sei / RICPE y otras representaciones posteriores', 'cómo llegaron después adjudicación, escritura, financiación y MYND'],
    controlTitle: 'Control antes del título',
    controlCopy: 'El título posterior no responde por sí solo qué autoridad existía para actos anteriores. A la inversa, la prueba de control práctico anterior al título no establece por sí sola criminalidad. Cada acto se contrasta con la autoridad, el perímetro y los derechos existentes en su propia fecha.',
    didNotTitle: 'Lo que el 7 de junio no decidió',
    didNot: [
      'No convirtió a CAM, por sí mismo, en titular del hotel entero ni de todas las fincas de LPB, Matkator o terceros.',
      'No transforma una facultad de seguridad o preservación en una autorización universal de posesión, desalojo, explotación u obras.',
      'No prueba por sí solo intención común, delito, financiación ilícita ni causalidad entre todos los carriles posteriores.',
      'La principal testigo actualmente utilizada no sitúa a JDAM físicamente en Sun Park el 7 de junio de 2018.'
    ],
    adverse: 'Evidencia adversa que también debe verse: la Sentencia AP 89/2014 es material adverso respecto de 18 unidades determinadas; y Fiscalía archivó DI 248/2018 en mayo de 2019. Esos resultados se conservan junto a la prueba posterior y no se borran por discrepancia con nuestra tesis.',
    parallelTitle: 'Vidas paralelas del mismo hotel',
    parallelLead: 'Qué era o cómo se trataba el mismo lugar físico/económico ante distintos marcos.',
    parallels: ['Activo concursal LPB', 'Hotel operativo de propiedad mixta', 'Sitio de reforma bajo control práctico', 'Proyecto hotelero comercial', 'Proposición de inversión', 'Proyecto regulado / con apoyo público cuando conste', 'Hotel sucesor HNT / MYND Yaiza'],
    pressureTitle: 'Carriles de presión convergentes',
    pressureLead: 'Mecanismos jurídicamente distintos que podían alterar la posición fáctica de otros carriles.',
    pressures: ['Acreedor / Concurso', 'Comunidad · deuda · voto · seguridad', 'Propiedad / título', 'Acceso / seguridad / control', 'Operación · clientes · personal', 'Rescate / financiación', 'Proyecto / comercialización', 'Regulación / ayudas públicas', 'Relato / medios / percepción pública'],
    bridge: 'Para afirmar un efecto entre carriles exigimos: evento fuente → actor/autoridad → puente jurídico o económico → derecho/opción afectado → consecuencia → estado probatorio → vacío o contrafactual. La proximidad temporal no sustituye ese puente.',
    thresholdTitle: '¿Qué cruzó el umbral?',
    thresholdLead: 'La cuestión económica es mayor que quién tenía las llaves. Es qué ocurrió con cada capa de una plataforma hotelera en funcionamiento cuando cambió el control práctico.',
    thresholdGroups: [
      ['ACTIVO E INFRAESTRUCTURA', 'Fincas LPB; Matkator/terceros cuando corresponda; recepción; zonas comerciales, comunes y de servicio.'],
      ['CAPACIDAD OPERATIVA', 'Acceso; personal/gestión in situ; mantenimiento; sistemas, registros y capacidad física de operar.'],
      ['CLIENTES Y COMUNIDAD', 'Huéspedes/residentes; SunRockers / Holiday Living; repetición; reservas futuras; relaciones con clientes.'],
      ['INFRAESTRUCTURA COMERCIAL', 'Demanda directa; distribución; relaciones con operadores; marca; rutas de contacto; goodwill/datos cuando sean probables jurídicamente.'],
      ['CAPACIDAD DE RECUPERACIÓN', 'Operador; inspección/due diligence; refinanciación/salida; conservación; mejora del valor.']
    ],
    audienceTitle: 'El mismo hotel ante públicos distintos',
    audienceLead: 'La comparación no presume engaño. Pregunta qué se representó, por quién, en qué fecha, sobre qué perímetro y qué documento conciliaba esa versión con las demás.',
    audienceHeaders: ['Público / institución', 'Pregunta de reconciliación', 'Control'],
    audiences: [
      ['Juzgado Mercantil / AC', '¿Qué activos estaban realmente en la masa y quién tenía capacidad material para preservarlos, operar, producir registros o generar ingresos?', 'Masa LPB ≠ hotel entero; custodia institucional ≠ conocimiento personal.'],
      ['Comunidad / CEXP / propietarios', '¿Quién podía votar, contratar seguridad, aprobar obras o representar qué derechos?', 'Gobernanza común ≠ título universal ni agencia automática de CAM.'],
      ['Clientes / personal', '¿Quién podía admitir, excluir, instruir, contactar y comunicar sobre Sun Park?', 'Separar hecho operativo, contrato, posesión y título.'],
      ['Operadores / compradores / financiadores', '¿Qué inventario, control, acceso y autoridad se les presentaba?', 'Oferta/due diligence ≠ cierre; medir acceso real y condiciones.'],
      ['RICPE / CNMV / inversores', '¿Qué propiedad, disponibilidad, obras, valor y madurez se representaron?', 'Comparar fecha, entidad, reserva y título real de ese momento.'],
      ['Yaiza / Cabildo / turismo', '¿Qué propiedad, promotor, consentimiento y proyecto soportaron licencias, obras o actividad?', 'Expediente administrativo específico, no inferencia por marca.'],
      ['RIC / incentivos / FEDER', '¿Qué beneficiario, gasto, activo, empleo y financiación se declaró?', 'Capas financieras distintas; no asumir doble financiación por coexistencia.'],
      ['Fiscalía / medios / público', '¿Qué versión del hotel, control y conflicto recibió cada receptor?', 'Recepción/archivo/publicación son hechos separados de la verdad de la alegación.']
    ],
    exitsTitle: 'Usa el 7 de junio como intercambiador, no como callejón sin salida',
    exits: [
      ['1 · Qué era Sun Park', 'Hotel, SunRockers, Holiday Living y plataforma comercial.', 'business'],
      ['2 · Quién tenía qué', 'LPB, Matkator, terceros, Comunidad/CEXP y entrada de CAM.', 'ownership'],
      ['3 · Antes del 7 de junio', 'Acceso, mediciones, seguridad y preparación Oct-2017–May-2018.', 'precursor'],
      ['4 · El propio 7 de junio', 'Reconstrucción acto por acto y fuente por fuente.', 'day'],
      ['5 · Después del cambio práctico', 'Clientes, personal, socios, acceso, identidad y proyecto.', 'after'],
      ['6 · Vidas paralelas', 'Concurso, Comunidad, control, proyecto, RICPE, incentivos, MYND y recuperación.', 'multiple'],
      ['7 · Calificación', 'Cómo el control material afecta capacidad, causalidad y acusaciones posteriores.', 'calificacion'],
      ['8 · Recuperación', 'Restitución, daños diferenciados y reconstrucción futura.', 'recovery']
    ],
    sourceNote: 'Este módulo reorganiza la lectura de fuentes ya controladas. No crea un nuevo hallazgo primario ni convierte alegaciones en hechos. El dossier está diseñado para que una fuente adversa pueda limitar o corregir cada carril.'
  } : {
    title: '7 June 2018: the day the legal, physical, operational and commercial timelines stopped matching.',
    lead: 'The controlled record supports a material change in access, security and practical control. Formal title to the principal LPB perimeter came years later. This page keeps those propositions separate and lets the reader trace, in parallel, what happened to the hotel, the insolvency, third-party rights, operation, finance and later representations.',
    homeEyebrow: '7 JUNE 2018 · THE HINGE',
    homeTitle: 'A functioning hotel, an insolvency, fragmented ownership and an emerging redevelopment project converged around one date.',
    homeLead: 'The record supports a material change in practical access and control; formal title to the LPB properties followed years later. The dossier separates what existed before, what changed on 7 June and what followed.',
    explore: 'Explore the hinge',
    multiple: 'See the same hotel’s parallel lives',
    before: 'BEFORE 7 JUNE',
    beforeShort: 'Operating hotel · customers · team · maintenance · exit/finance · fragmented titles.',
    hinge: '7 JUNE 2018',
    hingeShort: 'Material access/security/practical-control shift. Not a whole-hotel title date.',
    after: 'AFTER',
    afterShort: 'Access, customers, staff, inspections, project, narrative, finance and title followed different clocks.',
    gatewayEyebrow: 'CONVERGENCE DOSSIER · CONTROLLED READING',
    fourClocks: 'Four clocks that did not move together',
    fourClocksLead: 'The question is not which story “wins”, but which document authorised each transition on its date and what each actor knew at that time.',
    clocks: [
      ['LEGAL / TITLE CLOCK', 'Insolvency 36/2012 → liquidation / challenges / suspension → adjudication → deed / registration.'],
      ['PHYSICAL / OPERATIONAL CLOCK', 'Operating hotel → precursor access / measurement → 7-Jun practical shift → exclusion / disruption → works / successor operation.'],
      ['COMMERCIAL / FINANCIAL CLOCK', 'Sun Park → repositioning → Lava Verde → Club Sei / Meeting Point → RICPE → HNT / MYND → finance / support.'],
      ['INSTITUTIONAL / KNOWLEDGE CLOCK', 'Community / AC / Court / Fiscalía / CNMV / RIC / tourism / incentive-FEDER bodies → what each received, when and what each did.']
    ],
    rule: 'Reading rule: receipt ≠ examination ≠ personal knowledge ≠ duty ≠ decision ≠ responsibility.',
    beforeAfterTitle: 'Before → 7 June → after',
    beforeItems: ['hotel occupied/active on the controlled record', 'customers, stay relationships and repeat demand', 'staff, maintenance and service capacity', 'gradual improvement and operator/finance routes', 'fragmented title; LPB remained in insolvency', 'no 2022 LPB adjudication/title yet'],
    dayItems: ['documented access and security changes', 'locks/cylinders/chains/padlocks where supported', 'private-security presence/implementation', 'exclusion from normal access', 'authority relied upon and legal perimeter to reconcile', 'finca-by-finca reach still open'],
    afterItems: ['who controlled which access and areas', 'what happened to staff, customers and belongings', 'bookings, customer contact and commercial partners', 'who could inspect, measure, maintain or carry out works', 'Lava Verde / Club Sei / RICPE and later representations', 'how adjudication, deed, finance and MYND arrived later'],
    controlTitle: 'Control before title',
    controlCopy: 'Later title cannot by itself answer what authority existed for earlier acts. Conversely, evidence of practical control before title does not by itself establish criminality. Each act is tested against the authority, perimeter and rights existing on its own date.',
    didNotTitle: 'What 7 June did not decide',
    didNot: [
      'It did not, by itself, make CAM owner of the whole hotel or of every LPB, Matkator or third-party property.',
      'It does not turn a security or preservation power into a universal possession, eviction, operation or works mandate.',
      'It does not by itself prove common intent, an offence, unlawful finance or causation across every later lane.',
      'The principal witness presently relied upon does not place JDAM physically at Sun Park on 7 June 2018.'
    ],
    adverse: 'Adverse evidence must remain visible: AP Judgment 89/2014 is adverse primary material concerning 18 defined units; and Fiscalía archived DI 248/2018 in May 2019. Those outcomes sit beside later evidence and are not erased because they do not support our thesis.',
    parallelTitle: 'Parallel lives of the same hotel',
    parallelLead: 'What the same physical/economic place was, or was treated as, under different frameworks.',
    parallels: ['LPB insolvency asset', 'Mixed-ownership operating hotel', 'Redevelopment site under practical control', 'Commercial hotel project', 'Investment proposition', 'Regulated / publicly supported project where evidenced', 'Successor HNT / MYND Yaiza hotel'],
    pressureTitle: 'Converging pressure tracks',
    pressureLead: 'Legally distinct mechanisms capable of altering the factual position relied upon in other lanes.',
    pressures: ['Creditor / insolvency', 'Community · debt · vote · security', 'Property / title', 'Access / security / control', 'Operation · customers · staff', 'Rescue / finance', 'Project / commercialisation', 'Regulation / public support', 'Narrative / media / public perception'],
    bridge: 'To claim a cross-lane effect we require: source event → actor/authority → legal or economic bridge → affected right/option → consequence → evidence status → gap/counterfactual. Chronological proximity is not the bridge.',
    thresholdTitle: 'What crossed the threshold?',
    thresholdLead: 'The economic question is larger than who held the keys. It is what happened to each layer of a functioning hospitality platform once practical control changed.',
    thresholdGroups: [
      ['ASSET & INFRASTRUCTURE', 'LPB properties; Matkator/third parties where relevant; reception; commercial, common and service areas.'],
      ['OPERATING CAPACITY', 'Access; staff/on-site management; maintenance; systems, records and physical ability to operate.'],
      ['CUSTOMER & COMMUNITY PLATFORM', 'Guests/residents; SunRockers / Holiday Living; repeat demand; future bookings; customer relationships.'],
      ['COMMERCIAL INFRASTRUCTURE', 'Direct demand; distribution; operator relationships; brand; contact routes; goodwill/data where lawfully provable.'],
      ['RECOVERY CAPACITY', 'Operator implementation; inspection/due diligence; refinancing/exit; preservation; improvement of value.']
    ],
    audienceTitle: 'The same hotel before different audiences',
    audienceLead: 'Comparison does not presume deception. It asks what was represented, by whom, when, over which perimeter and what document reconciled that version with the others.',
    audienceHeaders: ['Audience / institution', 'Reconciliation question', 'Control'],
    audiences: [
      ['Mercantile Court / AC', 'What assets were actually in the estate and who had material capacity to preserve, operate, produce records or generate income?', 'LPB estate ≠ whole hotel; institutional custody ≠ personal knowledge.'],
      ['Community / CEXP / owners', 'Who could vote, retain security, approve works or represent which rights?', 'Common governance ≠ universal title or automatic CAM agency.'],
      ['Customers / staff', 'Who could admit, exclude, instruct, contact and communicate about Sun Park?', 'Separate operational fact, contract, possession and title.'],
      ['Operators / buyers / financiers', 'What inventory, control, access and authority were they shown?', 'Offer/due diligence ≠ closing; test actual access and conditions.'],
      ['RICPE / CNMV / investors', 'What ownership, availability, works, value and maturity were represented?', 'Compare date, legal person, caveat and actual title then.'],
      ['Yaiza / Cabildo / tourism', 'What ownership, promoter, consent and project supported licences, works or activity?', 'Specific administrative file, not inference from brand.'],
      ['RIC / incentives / FEDER', 'What beneficiary, spend, asset, employment and financing were declared?', 'Distinct finance layers; coexistence is not duplicate funding.'],
      ['Fiscalía / media / public', 'Which version of the hotel, control and dispute did each recipient receive?', 'Receipt/archive/publication are separate from truth of an allegation.']
    ],
    exitsTitle: 'Use 7 June as an interchange, not a dead-end article',
    exits: [
      ['1 · What Sun Park was', 'Hotel, SunRockers, Holiday Living and the commercial platform.', 'business'],
      ['2 · Who held what', 'LPB, Matkator, third parties, Community/CEXP and CAM’s entry.', 'ownership'],
      ['3 · Before 7 June', 'Access, measurement, security and preparation from Oct-2017 to May-2018.', 'precursor'],
      ['4 · 7 June itself', 'Act-by-act, source-by-source reconstruction.', 'day'],
      ['5 · After practical control changed', 'Customers, staff, partners, access, identity and project.', 'after'],
      ['6 · Parallel lives', 'Insolvency, Community, control, project, RICPE, incentives, MYND and recovery.', 'multiple'],
      ['7 · Classification', 'How material control affects capacity, causation and later accusations.', 'calificacion'],
      ['8 · Recovery', 'Restitution, differentiated damages and rebuilding the future.', 'recovery']
    ],
    sourceNote: 'This module reorganises the reading of already controlled sources. It creates no new primary finding and does not convert allegations into facts. The dossier is designed so adverse evidence can narrow or correct every lane.'
  };

  const css = `
    .j7-shell{width:min(1180px,calc(100% - 36px));margin-inline:auto}.j7-hub{padding:68px 0;background:linear-gradient(180deg,#f4f0e7 0%,#fff 48%,#edf2f0 100%);color:#13252d}.j7-home{padding:42px 0 50px;background:#13252d;color:#f8f4ea}.j7-eyebrow{margin:0 0 10px;font-size:.78rem;font-weight:800;letter-spacing:.13em;text-transform:uppercase}.j7-home .j7-eyebrow{color:#d7b66a}.j7-hub .j7-eyebrow{color:#7c5b17}.j7-home h2,.j7-hub h2,.j7-hub h3{margin-top:0}.j7-home h2{max-width:900px;font-size:clamp(1.8rem,3vw,3rem);line-height:1.06}.j7-home p,.j7-hub p{line-height:1.62}.j7-home-lead{max-width:930px;font-size:1.08rem;color:#e4e9e6}.j7-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}.j7-action{display:inline-flex;align-items:center;justify-content:center;padding:12px 16px;border:1px solid currentColor;border-radius:999px;font-weight:800;text-decoration:none}.j7-home .j7-action:first-child{background:#f8f4ea;color:#13252d;border-color:#f8f4ea}.j7-home .j7-action:last-child{color:#f8f4ea}.j7-mini-flow{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1px;margin-top:30px;background:#6d7a77;border:1px solid #6d7a77}.j7-mini-flow article{padding:19px;background:#172d36}.j7-mini-flow strong{display:block;color:#d7b66a;font-size:.77rem;letter-spacing:.1em}.j7-mini-flow span{display:block;margin-top:7px;color:#eef1ef;line-height:1.45}.j7-gateway-head{max-width:920px}.j7-gateway-head h2{font-size:clamp(2rem,4vw,3.8rem);line-height:1.02}.j7-gateway-head>p:last-child{font-size:1.13rem;max-width:900px}.j7-rule{margin:22px 0 0;padding:15px 18px;border-left:5px solid #a77718;background:#fff8e7;font-weight:700}.j7-clocks{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:34px 0 20px}.j7-clock{padding:20px;border:1px solid #cbd5d1;background:#fff;border-radius:14px}.j7-clock strong{display:block;margin-bottom:10px;font-size:.77rem;letter-spacing:.08em;color:#7c5b17}.j7-section{margin-top:54px}.j7-section-head{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(260px,.8fr);gap:28px;align-items:end;margin-bottom:22px}.j7-section-head h3{font-size:clamp(1.55rem,2.4vw,2.35rem)}.j7-triptych{display:grid;grid-template-columns:1fr 1.08fr 1fr;border:1px solid #bac7c2;background:#bac7c2;gap:1px}.j7-state{padding:24px;background:#fff}.j7-state.is-hinge{background:#13252d;color:#f7f4eb}.j7-state h4{margin:0 0 16px;font-size:.82rem;letter-spacing:.12em}.j7-state.is-hinge h4{color:#e0bd6d}.j7-state ul,.j7-plain-list{margin:0;padding-left:18px}.j7-state li,.j7-plain-list li{margin:8px 0;line-height:1.42}.j7-title-gap{display:grid;grid-template-columns:1fr auto 1.2fr auto 1fr;gap:10px;align-items:center;margin-top:22px;padding:24px;border-radius:14px;background:#fff;border:1px solid #bac7c2}.j7-date{padding:16px;border-radius:10px;background:#edf2f0}.j7-date strong{display:block;font-size:1.04rem}.j7-date span{display:block;margin-top:4px;font-size:.86rem}.j7-arrow{font-size:1.5rem;font-weight:900;color:#7c5b17}.j7-control-copy{margin-top:14px;padding:18px 20px;background:#fff;border-left:5px solid #13252d}.j7-caution-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.j7-caution{padding:24px;border-radius:14px;background:#fff;border:1px solid #cbd5d1}.j7-caution.adverse{background:#fff6f0;border-color:#d8b8a9}.j7-caution strong{display:block;margin-bottom:10px}.j7-dual{display:grid;grid-template-columns:1fr 1fr;gap:16px}.j7-panel{padding:24px;border-radius:14px;background:#fff;border:1px solid #cbd5d1}.j7-tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}.j7-tag{padding:7px 10px;border-radius:999px;background:#edf2f0;font-size:.88rem}.j7-bridge{margin-top:16px;padding:17px 19px;background:#13252d;color:#f7f4eb;border-radius:12px}.j7-threshold-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}.j7-threshold{padding:18px;background:#fff;border:1px solid #cbd5d1;border-radius:12px}.j7-threshold strong{display:block;margin-bottom:8px;font-size:.76rem;letter-spacing:.07em;color:#7c5b17}.j7-table-wrap{overflow:auto;border:1px solid #bac7c2;border-radius:12px;background:#fff}.j7-table{width:100%;min-width:860px;border-collapse:collapse}.j7-table th,.j7-table td{padding:15px 16px;text-align:left;vertical-align:top;border-bottom:1px solid #d9e0dd;line-height:1.42}.j7-table th{background:#13252d;color:#fff;font-size:.78rem;letter-spacing:.06em}.j7-table tr:last-child td{border-bottom:0}.j7-exits{display:grid;grid-template-columns:repeat(4,1fr);gap:11px}.j7-exit{display:block;padding:19px;border:1px solid #cbd5d1;border-radius:12px;background:#fff;color:inherit;text-decoration:none}.j7-exit strong{display:block;margin-bottom:7px}.j7-exit span{font-size:.92rem;line-height:1.42}.j7-exit:hover,.j7-exit:focus-visible{border-color:#7c5b17;box-shadow:0 0 0 3px rgba(167,119,24,.14)}.j7-source-note{margin-top:26px;padding-top:18px;border-top:1px solid #bac7c2;font-size:.9rem;color:#53625d}.takeover-page .dossier-hero .j7-reframed-title{max-width:950px}.takeover-page .dossier-hero .j7-reframed-lead{max-width:930px}
    @media(max-width:900px){.j7-clocks{grid-template-columns:1fr 1fr}.j7-section-head{grid-template-columns:1fr}.j7-threshold-grid{grid-template-columns:1fr 1fr}.j7-exits{grid-template-columns:1fr 1fr}.j7-title-gap{grid-template-columns:1fr}.j7-arrow{transform:rotate(90deg);justify-self:center}.j7-mini-flow,.j7-triptych{grid-template-columns:1fr}.j7-caution-grid,.j7-dual{grid-template-columns:1fr}}
    @media(max-width:560px){.j7-shell{width:min(100% - 24px,1180px)}.j7-hub{padding:46px 0}.j7-clocks,.j7-threshold-grid,.j7-exits{grid-template-columns:1fr}.j7-home{padding:34px 0 40px}.j7-state,.j7-panel,.j7-caution{padding:19px}}
    @media print{.j7-home{background:#fff;color:#000}.j7-home .j7-action{color:#000;border-color:#000}.j7-hub{background:#fff}.j7-table-wrap{overflow:visible}.j7-table{min-width:0}.j7-exit{break-inside:avoid}}
  `;

  if (!document.getElementById('j7-convergence-style')) {
    const style = document.createElement('style');
    style.id = 'j7-convergence-style';
    style.textContent = css;
    document.head.appendChild(style);
  }

  const list = (items) => `<ul class="j7-plain-list">${items.map((x) => `<li>${x}</li>`).join('')}</ul>`;

  const buildHome = () => {
    if (document.getElementById('j7-home-hinge')) return;
    const priority = document.querySelector('.priority-band');
    if (!priority) return;
    const section = document.createElement('section');
    section.className = 'j7-home';
    section.id = 'j7-home-hinge';
    section.setAttribute('aria-labelledby', 'j7-home-title');
    section.innerHTML = `
      <div class="j7-shell">
        <p class="j7-eyebrow">${t.homeEyebrow}</p>
        <h2 id="j7-home-title">${t.homeTitle}</h2>
        <p class="j7-home-lead">${t.homeLead}</p>
        <div class="j7-mini-flow" aria-label="${t.beforeAfterTitle}">
          <article><strong>${t.before}</strong><span>${t.beforeShort}</span></article>
          <article><strong>${t.hinge}</strong><span>${t.hingeShort}</span></article>
          <article><strong>${t.after}</strong><span>${t.afterShort}</span></article>
        </div>
        <div class="j7-actions"><a class="j7-action" href="${routes.dossier}">${t.explore} →</a><a class="j7-action" href="${routes.multiple}">${t.multiple} →</a></div>
      </div>`;
    priority.insertAdjacentElement('afterend', section);
  };

  const buildDossier = () => {
    if (document.getElementById('j7-convergence-hub')) return;
    const hero = document.querySelector('.dossier-hero');
    const main = document.querySelector('main');
    if (!main || !hero) return;

    const heroEyebrow = hero.querySelector('.eyebrow');
    const heroTitle = hero.querySelector('h1');
    const heroLead = hero.querySelector('.lead');
    if (heroEyebrow) heroEyebrow.textContent = t.gatewayEyebrow;
    if (heroTitle) {
      heroTitle.textContent = t.title;
      heroTitle.classList.add('j7-reframed-title');
    }
    if (heroLead) {
      heroLead.textContent = t.lead;
      heroLead.classList.add('j7-reframed-lead');
    }

    const target = document.querySelector('#legal-perimeters') || hero.nextElementSibling;
    const section = document.createElement('section');
    section.className = 'j7-hub';
    section.id = 'j7-convergence-hub';
    section.setAttribute('aria-labelledby', 'j7-convergence-title');

    const clockCards = t.clocks.map(([name, body]) => `<article class="j7-clock"><strong>${name}</strong><span>${body}</span></article>`).join('');
    const thresholdCards = t.thresholdGroups.map(([name, body]) => `<article class="j7-threshold"><strong>${name}</strong><span>${body}</span></article>`).join('');
    const audienceRows = t.audiences.map(([audience, q, control]) => `<tr><td><strong>${audience}</strong></td><td>${q}</td><td>${control}</td></tr>`).join('');
    const exitCards = t.exits.map(([name, body, key]) => `<a class="j7-exit" href="${routes[key]}"><strong>${name}</strong><span>${body}</span></a>`).join('');

    section.innerHTML = `
      <div class="j7-shell">
        <div class="j7-gateway-head">
          <p class="j7-eyebrow">${t.gatewayEyebrow}</p>
          <h2 id="j7-convergence-title">${t.fourClocks}</h2>
          <p>${t.fourClocksLead}</p>
        </div>
        <div class="j7-clocks">${clockCards}</div>
        <p class="j7-rule">${t.rule}</p>

        <section class="j7-section" id="j7-before-after" aria-labelledby="j7-before-after-title">
          <div class="j7-section-head"><div><p class="j7-eyebrow">${t.beforeAfterTitle}</p><h3 id="j7-before-after-title">${t.title}</h3></div><p>${t.lead}</p></div>
          <div class="j7-triptych">
            <article class="j7-state"><h4>${t.before}</h4>${list(t.beforeItems)}</article>
            <article class="j7-state is-hinge"><h4>${t.hinge}</h4>${list(t.dayItems)}</article>
            <article class="j7-state"><h4>${t.after}</h4>${list(t.afterItems)}</article>
          </div>
        </section>

        <section class="j7-section" id="j7-control-before-title" aria-labelledby="j7-control-title">
          <div class="j7-section-head"><div><p class="j7-eyebrow">2018 → 2022</p><h3 id="j7-control-title">${t.controlTitle}</h3></div><p>${t.controlCopy}</p></div>
          <div class="j7-title-gap" role="group" aria-label="${t.controlTitle}">
            <div class="j7-date"><strong>7 JUN 2018</strong><span>${isEs ? 'umbral de control material' : 'material-control threshold'}</span></div><span class="j7-arrow" aria-hidden="true">→</span>
            <div class="j7-date"><strong>${isEs ? 'más de 3,5 años' : 'more than 3.5 years'}</strong><span>${isEs ? 'los relojes siguen separados' : 'the clocks remain separate'}</span></div><span class="j7-arrow" aria-hidden="true">→</span>
            <div><div class="j7-date"><strong>26 JAN 2022</strong><span>${isEs ? 'umbral de adjudicación judicial' : 'judicial adjudication threshold'}</span></div><div class="j7-date" style="margin-top:8px"><strong>21 FEB 2022</strong><span>${isEs ? 'escritura / transmisión formal' : 'deed / formal transmission'}</span></div></div>
          </div>
          <p class="j7-control-copy"><strong>${t.controlTitle}.</strong> ${t.controlCopy}</p>
        </section>

        <section class="j7-section" aria-labelledby="j7-not-decided-title">
          <div class="j7-caution-grid">
            <article class="j7-caution"><strong id="j7-not-decided-title">${t.didNotTitle}</strong>${list(t.didNot)}</article>
            <article class="j7-caution adverse"><strong>${isEs ? 'Contrapesos que no se ocultan' : 'Counterweights that are not hidden'}</strong><p>${t.adverse}</p></article>
          </div>
        </section>

        <section class="j7-section" aria-labelledby="j7-parallel-title">
          <div class="j7-dual">
            <article class="j7-panel"><p class="j7-eyebrow">${isEs ? 'QUÉ ERA / CÓMO SE TRATABA' : 'WHAT IT WAS / HOW IT WAS TREATED'}</p><h3 id="j7-parallel-title">${t.parallelTitle}</h3><p>${t.parallelLead}</p><div class="j7-tags">${t.parallels.map((x) => `<span class="j7-tag">${x}</span>`).join('')}</div></article>
            <article class="j7-panel"><p class="j7-eyebrow">${isEs ? 'QUÉ ACTUABA SOBRE ÉL' : 'WHAT WAS ACTING ON IT'}</p><h3>${t.pressureTitle}</h3><p>${t.pressureLead}</p><div class="j7-tags">${t.pressures.map((x) => `<span class="j7-tag">${x}</span>`).join('')}</div></article>
          </div>
          <p class="j7-bridge">${t.bridge}</p>
        </section>

        <section class="j7-section" aria-labelledby="j7-threshold-title">
          <div class="j7-section-head"><div><p class="j7-eyebrow">${isEs ? 'PLATAFORMA COMPLETA' : 'FULL PLATFORM'}</p><h3 id="j7-threshold-title">${t.thresholdTitle}</h3></div><p><strong>${t.thresholdLead}</strong></p></div>
          <div class="j7-threshold-grid">${thresholdCards}</div>
        </section>

        <section class="j7-section" id="j7-audiences" aria-labelledby="j7-audiences-title">
          <div class="j7-section-head"><div><p class="j7-eyebrow">${isEs ? 'RECONCILIACIÓN ENTRE PÚBLICOS' : 'AUDIENCE RECONCILIATION'}</p><h3 id="j7-audiences-title">${t.audienceTitle}</h3></div><p>${t.audienceLead}</p></div>
          <div class="j7-table-wrap" tabindex="0" aria-label="${t.audienceTitle}"><table class="j7-table"><thead><tr>${t.audienceHeaders.map((h) => `<th scope="col">${h}</th>`).join('')}</tr></thead><tbody>${audienceRows}</tbody></table></div>
        </section>

        <section class="j7-section" aria-labelledby="j7-exits-title">
          <div class="j7-section-head"><div><p class="j7-eyebrow">${isEs ? 'NAVEGACIÓN' : 'NAVIGATION'}</p><h3 id="j7-exits-title">${t.exitsTitle}</h3></div><p>${isEs ? 'Cada salida conserva un perímetro distinto. Las conexiones deben demostrarse, no suponerse.' : 'Each exit preserves a distinct perimeter. Connections must be shown, not assumed.'}</p></div>
          <div class="j7-exits">${exitCards}</div>
          <p class="j7-source-note">${t.sourceNote}</p>
        </section>
      </div>`;

    if (target && target.parentNode) target.parentNode.insertBefore(section, target);
    else hero.insertAdjacentElement('afterend', section);
  };

  if (isEnHome || isEsHome) buildHome();
  if (isEnDossier || isEsDossier) buildDossier();
})();

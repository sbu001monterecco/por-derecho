/* CLIFFE-JONES / YHB / CO-OPERATIVE RELATIONSHIP AND RESPONSIBILITY MAP — 22 AUGUST 2026 */
(() => {
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };

  const path = normalise(location.pathname);
  const enRoute = '/en/sun-park-takeover-7-june-2018/camel-travel-lanzarote-information/';
  const esRoute = '/es/toma-control-sun-park-7-junio-2018/camel-travel-lanzarote-information/';
  const en = path.endsWith(enRoute);
  const es = path.endsWith(esRoute);
  if ((!en && !es) || document.querySelector('[data-cliffe-jones-map="20260822"]')) return;

  const prefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const links = {
    acosta: en ? `${prefix}en/acosta-matos-perimeter/` : `${prefix}es/acosta-matos-perimetro/`,
    jdam: en ? `${prefix}en/architecture-documentary-node-jdam/` : `${prefix}es/arquitectura-nodo-documental-jdam/`,
    media: en ? `${prefix}en/media-public-narrative-traceability/` : `${prefix}es/medios-trazabilidad-relato-publico/`,
    takeover: en ? `${prefix}en/sun-park-takeover-7-june-2018/` : `${prefix}es/toma-control-sun-park-7-junio-2018/`
  };

  const c = en ? {
    nav: 'Relationship map',
    action: 'Open relationship map',
    eyebrow: 'Side record · relationship, responsibility and booking infrastructure · updated 22 August 2026',
    title: 'One couple, two public-facing businesses and a Co-operative travel-sales chain.',
    intro: 'The visual separates common operation, publication decisions, booking infrastructure, alleged successor benefit and the proof required before responsibility can be transferred from one node to another.',
    rootK: 'Common proprietors / operators',
    rootT: 'Mike and Julie Cliffe-Jones',
    rootP: 'The connected and public record identifies the same couple behind Lanzarote Information and Camel Travel. That common operation permits scrutiny of conflicts, disclosure, editorial care and commercial benefit; it does not make every company, consortium or publisher the same legal person.',
    liK: 'Destination publishing',
    liT: 'Lanzarote Information',
    li: ['Destination-information publisher.', 'Historical paid promoter of Sun Park; connected records directly verify substantial promotional work from at least 2015 into 2017.', 'Publisher of the continuing materially adverse Sun Park article under the predecessor name.'],
    camelK: 'Travel sales',
    camelT: 'Camel Travel',
    camel: ['Travel-sales business operated by the same couple.', 'Historically traded through Your Holiday Booking; Mike used a YHB address and Co-operative-linked signature when introducing Sun Park for flight packaging in 2015.', 'Current public contact material identifies the YHB administration team and booking-reference infrastructure.', 'Current disclosures describe travel sales through Co-op Travel Services Ltd and the Co-operative travel consortium chain.'],
    yhbT: 'Your Holiday Booking / booking infrastructure',
    yhbP: 'Midcounties confirmed on the 7 November 2024 call that Camel was not separately listed as a consortium agent but traded under Your Holiday Booking, which Midcounties identified as its consortium agent or member.',
    coopT: 'Co-op Travel Services Ltd / consortium control',
    midK: 'Historical controlling society',
    midP: 'The Midcounties Co-operative — Companies House records it as the former person with significant control, ceasing on 26 January 2026.',
    centralK: 'Current controlling society',
    centralP: 'Central England Co-operative Limited — notified as active person with significant control on 26 January 2026, with 75%+ share and voting control and the right to appoint or remove directors.',
    effectK: 'Documented same-asset contrast',
    effectT: 'One physical property · two public narratives',
    effectP: 'The predecessor Sun Park name retained severe adverse material while Camel promoted the refurbished same property as MYND Yaiza and invited quotation requests. Capability to generate successor benefit is documented; a completed booking, commission, payment or instruction is not.',
    attribK: 'Project Sun Rock attribution · evidence tiers kept separate',
    attribT: 'The strongest publishable responsibility position.',
    perimeterK: '1 · Alleged principal-benefit perimeter',
    perimeterT: 'Acosta Matos-linked successor perimeter',
    perimeterP: 'Project Sun Rock attributes its strongest principal-responsibility and successor-benefit hypothesis to this perimeter within the wider alleged transfer of possession, operation, reputation and value. The dual-publication record was capable of benefiting the successor narrative and sales route. Benefit alone is not responsibility, and the present record does not prove that CAM, HNT, Canarian Hospitality or MYND commissioned, paid for, instructed or coordinated either publication.',
    jdamK: '2 · Strongest derivative / vicarious-responsibility test',
    jdamT: 'José Daniel Acosta Matos (JDAM)',
    jdamP: 'Project Sun Rock seeks the strongest derivative attribution the evidence can sustain. Responsibility would follow only if act-specific records establish agency or principal status, operational control, commissioning, adoption, knowing facilitation, ratification after notice, connected benefit or another legally recognised duty and failure to act. Surname, architecture role or professional exposure alone does not prove control of the media or travel-sales conduct.',
    directK: '3 · Direct editorial and commercial decisions',
    directT: 'Mike and Julie / Lanzarote Information / Camel Travel',
    directP: 'They remain directly answerable for their own publication, disclosure, quotation-route, correction and preservation decisions. Project Sun Rock alleges lack of reasonable care and reckless disregard if severe predecessor claims were maintained or amplified after material notice without proportionate verification, correction, fair successor context or disclosure while the connected travel business promoted the successor. No court or regulator finding of recklessness is stated.',
    oversightK: '4 · Agency, supervision and institutional care',
    oversightT: 'YHB · Co-op Travel Services · Midcounties · Central England Co-operative',
    oversightP: 'The evidence establishes a sales and administration chain, not automatic responsibility for Lanzarote Information’s editorial content. Vicarious, supervisory or governance responsibility depends on the actual agreements, delegated authority, controls, knowledge, complaints, preservation, ratification, benefit and the response after notice. A connected 31 March 2025 email states that Midcounties completed an internal investigation; its scope and outcome remain unpublished.',
    ampK: 'Independent amplification and verification lane',
    ampT: 'BBC and other later publishers or amplifiers',
    ampP: 'They are not ownership nodes in Camel’s booking chain. Project Sun Rock alleges potential lack of care or reckless disregard only where a publisher had material notice, access to contrary evidence and a realistic opportunity to correct or contextualise but failed to do so. That route requires a publisher-specific knowledge, reliance, counterfactual and causation record; it is not an adjudicated finding or vicarious responsibility for the Cliffe-Jones businesses.',
    testsK: 'Responsibility cannot travel by association alone',
    testsT: 'Six bridges must be tested before vicarious or derivative responsibility is asserted as fact.',
    tests: [['Agency or employment', 'Authorised or apparent mandate.'], ['Operational control', 'Publication, booking code, CRM, merchant flow and correction power.'], ['Commissioning or supply', 'Access, text, images, hospitality, referral terms or payment.'], ['Adoption or ratification', 'Adoption, retained benefit or refusal to correct after adequate notice.'], ['Coordinated purpose', 'Communications and timing showing a common objective rather than parallel conduct.'], ['Connected benefit and causation', 'Enquiries, bookings, commissions, reputation or value and the challenged conduct’s causal contribution.']],
    boundaryT: 'Controlling evidential boundary',
    boundaryP: 'Documented operation, current corporate control and the existence of an investigation are stated as facts. Recklessness, knowing facilitation, principal responsibility, vicarious responsibility and coordinated purpose remain attributed allegations or conditional legal inferences unless the missing control, instruction, knowledge, benefit and causation records establish them.',
    sourceT: 'Source and capacity controls',
    sourceP: 'Current public records separately describe YHB brand and administration, Co-op Travel Services agency activity, consortium membership and the 26 January 2026 change of corporate control. Those capacities must not be collapsed.',
    statusEarlier: 'Paid promotion and wider commercial work directly verified from at least 2015 into 2017',
    statusLimit: 'No proof yet of CAM/JDAM instruction, MYND payment, completed booking, commission or a proved vicarious-liability bridge',
    openAcosta: 'Open Acosta Matos perimeter', openJdam: 'Open JDAM documentary node', openMedia: 'Open media-verification record', openTakeover: 'Return to the full 7 June dossier', companies: 'Companies House control record', camel: 'Camel current booking-chain disclosure', central: 'Central Co-op transfer context'
  } : {
    nav: 'Mapa de relaciones',
    action: 'Abrir mapa de relaciones',
    eyebrow: 'Registro lateral · relación, responsabilidad e infraestructura de reservas · actualizado 22 agosto 2026',
    title: 'Una pareja, dos negocios visibles al público y una cadena cooperativa de venta de viajes.',
    intro: 'La visualización separa operación común, decisiones editoriales, infraestructura de reservas, beneficio sucesor alegado y la prueba necesaria antes de trasladar responsabilidad de un nodo a otro.',
    rootK: 'Titulares / operadores comunes',
    rootT: 'Mike y Julie Cliffe-Jones',
    rootP: 'El registro conectado y público identifica a la misma pareja detrás de Lanzarote Information y Camel Travel. Esa operación común permite examinar conflictos, revelación, cuidado editorial y beneficio comercial; no convierte a cada sociedad, consorcio o editor en la misma persona jurídica.',
    liK: 'Publicación sobre el destino',
    liT: 'Lanzarote Information',
    li: ['Editor de información sobre el destino.', 'Promotor histórico pagado de Sun Park; los registros conectados verifican directamente trabajo promocional sustancial al menos desde 2015 hasta 2017.', 'Editor del artículo materialmente adverso que continúa publicado bajo el nombre predecesor Sun Park.'],
    camelK: 'Venta de viajes',
    camelT: 'Camel Travel',
    camel: ['Negocio de venta de viajes operado por la misma pareja.', 'Históricamente operó a través de Your Holiday Booking; Mike utilizó una dirección YHB y una firma vinculada a Co-operative Travel al presentar Sun Park para paquetes con vuelos en 2015.', 'El contacto público actual identifica al equipo administrativo YHB y su infraestructura de referencias de reserva.', 'Las revelaciones actuales describen ventas mediante Co-op Travel Services Ltd y la cadena de consorcios cooperativos de viaje.'],
    yhbT: 'Your Holiday Booking / infraestructura de reservas',
    yhbP: 'Midcounties confirmó en la llamada de 7 de noviembre de 2024 que Camel no figuraba por separado como agente del consorcio, sino que operaba bajo Your Holiday Booking, identificado por Midcounties como su agente o miembro del consorcio.',
    coopT: 'Co-op Travel Services Ltd / control del consorcio',
    midK: 'Sociedad controladora histórica',
    midP: 'The Midcounties Co-operative — Companies House la registra como antigua persona con control significativo, cesando el 26 de enero de 2026.',
    centralK: 'Sociedad controladora actual',
    centralP: 'Central England Co-operative Limited — notificada como persona activa con control significativo el 26 de enero de 2026, con más del 75% de acciones y votos y derecho a nombrar o cesar administradores.',
    effectK: 'Contraste documentado sobre el mismo activo',
    effectT: 'Un inmueble físico · dos relatos públicos',
    effectP: 'El nombre predecesor Sun Park conservó material gravemente adverso, mientras Camel promocionó el mismo inmueble reformado como MYND Yaiza e invitó a solicitar presupuestos. Está documentada la capacidad de generar beneficio para el sucesor; no lo están una reserva completada, comisión, pago o instrucción.',
    attribK: 'Atribución de Project Sun Rock · niveles probatorios separados',
    attribT: 'La posición de responsabilidad más fuerte que puede publicarse.',
    perimeterK: '1 · Perímetro principal de beneficio alegado',
    perimeterT: 'Perímetro sucesor vinculado a Acosta Matos',
    perimeterP: 'Project Sun Rock atribuye a este perímetro su hipótesis más intensa de responsabilidad principal y beneficio sucesor dentro de la transferencia más amplia alegada de posesión, explotación, reputación y valor. El registro de doble publicación era apto para beneficiar el relato y la vía de ventas del sucesor. El beneficio por sí solo no equivale a responsabilidad y el registro actual no prueba que CAM, HNT, Canarian Hospitality o MYND encargaran, pagaran, instruyeran o coordinaran ninguna publicación.',
    jdamK: '2 · Prueba más intensa de responsabilidad derivada / vicaria',
    jdamT: 'José Daniel Acosta Matos (JDAM)',
    jdamP: 'Project Sun Rock sostiene la atribución derivada más fuerte que pueda sostener la prueba. La responsabilidad seguiría únicamente si registros específicos acreditan agencia o condición de principal, control operativo, encargo, adopción, facilitación consciente, ratificación tras el aviso, beneficio conectado u otro deber jurídico reconocido y su incumplimiento. El apellido, función arquitectónica o exposición profesional por sí solos no prueban control sobre medios o venta de viajes.',
    directK: '3 · Decisiones editoriales y comerciales directas',
    directT: 'Mike y Julie / Lanzarote Information / Camel Travel',
    directP: 'Responden directamente por sus propias decisiones de publicación, revelación, vía de presupuestos, corrección y conservación. Project Sun Rock alega falta de cuidado razonable y desprecio temerario si se mantuvieron o amplificaron afirmaciones severas sobre el predecesor tras recibir aviso material, sin verificación, corrección, contexto justo sobre el sucesor o revelación proporcionadas, mientras el negocio de viajes conectado promocionaba al sucesor. No se afirma una declaración judicial o regulatoria de temeridad.',
    oversightK: '4 · Agencia, supervisión y cuidado institucional',
    oversightT: 'YHB · Co-op Travel Services · Midcounties · Central England Co-operative',
    oversightP: 'La prueba establece una cadena de venta y administración, no responsabilidad automática por el contenido editorial de Lanzarote Information. La responsabilidad vicaria, supervisora o de gobernanza depende de los contratos reales, autoridad delegada, controles, conocimiento, quejas, preservación, ratificación, beneficio y respuesta tras el aviso. Un correo conectado de 31 de marzo de 2025 afirma que Midcounties completó una investigación interna; su alcance y resultado no se han publicado.',
    ampK: 'Vía independiente de amplificación y verificación',
    ampT: 'BBC y otros editores o amplificadores posteriores',
    ampP: 'No son nodos de propiedad en la cadena de reservas de Camel. Project Sun Rock alega posible falta de cuidado o desprecio temerario solo cuando un editor tenía aviso material, acceso a prueba contraria y oportunidad realista de corregir o contextualizar, pero no lo hizo. Esa vía exige un registro específico de conocimiento, dependencia, contrafactual y causalidad; no es una declaración judicial ni responsabilidad vicaria por los negocios Cliffe-Jones.',
    testsK: 'La responsabilidad no viaja por mera asociación',
    testsT: 'Deben comprobarse seis puentes antes de afirmar como hecho responsabilidad vicaria o derivada.',
    tests: [['Agencia o empleo', 'Mandato autorizado o aparente.'], ['Control operativo', 'Publicación, código de reserva, CRM, flujo mercantil y poder de corrección.'], ['Encargo o suministro', 'Acceso, texto, imágenes, hospitalidad, términos de referencia o pago.'], ['Adopción o ratificación', 'Adopción, beneficio retenido o negativa a corregir tras aviso suficiente.'], ['Finalidad coordinada', 'Comunicaciones y fechas que muestren objetivo común, no conducta paralela.'], ['Beneficio conectado y causalidad', 'Consultas, reservas, comisiones, reputación o valor y contribución causal de la conducta impugnada.']],
    boundaryT: 'Límite probatorio rector',
    boundaryP: 'La operación documentada, el control societario actual y la existencia de una investigación se exponen como hechos. Temeridad, facilitación consciente, responsabilidad principal, responsabilidad vicaria y finalidad coordinada siguen siendo alegaciones atribuidas o inferencias jurídicas condicionales salvo que los registros ausentes de control, instrucción, conocimiento, beneficio y causalidad las acrediten.',
    sourceT: 'Controles de fuente y capacidad',
    sourceP: 'Los registros públicos actuales describen por separado la marca y administración YHB, actividad de agencia de Co-op Travel Services, pertenencia al consorcio y cambio de control societario de 26 de enero de 2026. Esas capacidades no deben confundirse.',
    statusEarlier: 'Promoción pagada y trabajo comercial más amplio verificados directamente al menos desde 2015 hasta 2017',
    statusLimit: 'Sin prueba todavía de instrucción CAM/JDAM, pago MYND, reserva completada, comisión o puente probado de responsabilidad vicaria',
    openAcosta: 'Abrir perímetro Acosta Matos', openJdam: 'Abrir nodo documental JDAM', openMedia: 'Abrir registro de verificación de medios', openTakeover: 'Volver al dossier completo del 7 de junio', companies: 'Registro de control en Companies House', camel: 'Revelación actual de la cadena de reservas de Camel', central: 'Contexto de la transferencia a Central Co-op'
  };

  const bullets = items => `<ul>${items.map(item => `<li>${item}</li>`).join('')}</ul>`;
  const section = document.createElement('section');
  section.className = 'section alt cj-map';
  section.id = en ? 'relationship-map' : 'mapa-relaciones';
  section.dataset.cliffeJonesMap = '20260822';
  section.innerHTML = `<div class="shell">
    <header class="cj-head"><p class="kicker">${c.attribK}</p><h2>${c.title}</h2><p>${c.intro}</p></header>
    <div class="cj-tree" role="group" aria-label="${c.title}">
      <article class="cj-node cj-root"><span>${c.rootK}</span><h3>${c.rootT}</h3><p>${c.rootP}</p></article>
      <div class="cj-branches">
        <article class="cj-node cj-li"><span>${c.liK}</span><h3>${c.liT}</h3>${bullets(c.li)}</article>
        <article class="cj-node cj-camel"><span>${c.camelK}</span><h3>${c.camelT}</h3>${bullets(c.camel)}
          <div class="cj-chain"><strong>${c.yhbT}</strong><p>${c.yhbP}</p><strong>${c.coopT}</strong>
            <div class="cj-control"><div><span>${c.midK}</span><p>${c.midP}</p></div><div><span>${c.centralK}</span><p>${c.centralP}</p></div></div>
          </div>
        </article>
      </div>
      <article class="cj-effect"><span>${c.effectK}</span><h3>${c.effectT}</h3><p>${c.effectP}</p></article>
    </div>
    <header class="cj-head cj-attrib-head"><p class="kicker">${c.attribK}</p><h2>${c.attribT}</h2><p>${c.boundaryP}</p></header>
    <div class="cj-responsibility">
      <article class="cj-card cj-perimeter"><span>${c.perimeterK}</span><h3>${c.perimeterT}</h3><p>${c.perimeterP}</p><a href="${links.acosta}">${c.openAcosta} →</a></article>
      <article class="cj-card cj-jdam"><span>${c.jdamK}</span><h3>${c.jdamT}</h3><p>${c.jdamP}</p><a href="${links.jdam}">${c.openJdam} →</a></article>
      <article class="cj-card cj-direct"><span>${c.directK}</span><h3>${c.directT}</h3><p>${c.directP}</p></article>
      <article class="cj-card cj-oversight"><span>${c.oversightK}</span><h3>${c.oversightT}</h3><p>${c.oversightP}</p></article>
    </div>
    <article class="cj-amplifier"><span>${c.ampK}</span><h3>${c.ampT}</h3><p>${c.ampP}</p><div class="cj-links"><a href="${links.media}">${c.openMedia} →</a><a href="${links.takeover}">${c.openTakeover} →</a></div></article>
    <header class="cj-head cj-test-head"><p class="kicker">${c.testsK}</p><h2>${c.testsT}</h2></header>
    <div class="cj-tests">${c.tests.map(([name,text],i)=>`<article><span>0${i+1}</span><h3>${name}</h3><p>${text}</p></article>`).join('')}</div>
    <aside class="cj-boundary"><strong>${c.boundaryT}</strong><p>${c.boundaryP}</p></aside>
    <details class="cj-sources"><summary>${c.sourceT}</summary><p>${c.sourceP}</p><div class="cj-links"><a href="https://find-and-update.company-information.service.gov.uk/company/08903986/persons-with-significant-control" rel="external noopener">${c.companies} →</a><a href="https://cameltravel.co.uk/contact/" rel="external noopener">${c.camel} →</a><a href="https://www.centralcoop.co.uk/our-coop/" rel="external noopener">${c.central} →</a></div></details>
  </div>`;

  const position = document.querySelector(en ? '#position' : '#posicion');
  const chronology = document.querySelector(en ? '#chronology' : '#cronologia');
  if (position) position.insertAdjacentElement('afterend', section);
  else if (chronology) chronology.insertAdjacentElement('beforebegin', section);
  else document.querySelector('main')?.append(section);

  const nav = document.querySelector('#main-nav');
  if (nav && !nav.querySelector(`a[href="#${section.id}"]`)) {
    const a = document.createElement('a'); a.href = `#${section.id}`; a.textContent = c.nav; nav.prepend(a);
  }
  const actions = document.querySelector('.dossier-hero .actions');
  if (actions && !actions.querySelector(`a[href="#${section.id}"]`)) {
    const a = document.createElement('a'); a.className = 'button secondary'; a.href = `#${section.id}`; a.textContent = c.action; actions.append(a);
  }
  const eyebrow = document.querySelector('.dossier-hero .eyebrow');
  if (eyebrow) eyebrow.textContent = c.eyebrow;
  const status = [...document.querySelectorAll('.dossier-status > div')];
  if (status[1]?.querySelector('strong')) status[1].querySelector('strong').textContent = c.statusEarlier;
  if (status[3]?.querySelector('strong')) status[3].querySelector('strong').textContent = c.statusLimit;

  const style = document.createElement('style');
  style.dataset.cliffeJonesMapStyle = '20260822';
  style.textContent = `
    .cj-map{position:relative;overflow:hidden;background:linear-gradient(180deg,#f4f1ea,#edf4f3)}
    .cj-map:before{content:"RELATIONSHIP";position:absolute;right:-1rem;top:1rem;font-size:clamp(4rem,11vw,10rem);font-weight:900;letter-spacing:-.07em;color:rgba(19,37,45,.035);pointer-events:none}
    html[lang="es"] .cj-map:before{content:"RELACIONES"}
    .cj-head{position:relative;max-width:980px}.cj-head>p:last-child{font-size:1.04rem;line-height:1.65}
    .cj-tree,.cj-responsibility,.cj-amplifier,.cj-tests,.cj-boundary,.cj-sources{position:relative;z-index:1}
    .cj-tree{margin-top:1.2rem;padding:1.1rem;border:1px solid rgba(19,37,45,.14);border-radius:20px;background:rgba(255,255,255,.74);box-shadow:0 1rem 3rem rgba(19,37,45,.08)}
    .cj-node,.cj-card,.cj-tests article{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:15px;padding:1rem;box-shadow:0 .55rem 1.4rem rgba(19,37,45,.05)}
    .cj-node>span,.cj-card>span,.cj-effect>span,.cj-amplifier>span,.cj-control span{display:block;margin-bottom:.4rem;font-size:.73rem;font-weight:900;letter-spacing:.075em;text-transform:uppercase;color:#315c7b}
    .cj-node h3,.cj-card h3,.cj-effect h3,.cj-amplifier h3,.cj-tests h3{margin:.15rem 0 .5rem}.cj-node p,.cj-card p,.cj-effect p,.cj-amplifier p,.cj-tests p{line-height:1.55}
    .cj-node ul{margin:.5rem 0 0;padding-left:1.15rem}.cj-node li{margin:.4rem 0;line-height:1.45}
    .cj-root{max-width:620px;margin:0 auto 2rem;text-align:center;border-top:5px solid #13252d}
    .cj-branches{display:grid;grid-template-columns:1fr 1.35fr;gap:1rem}.cj-li{border-top:5px solid #a67616}.cj-camel{border-top:5px solid #245c49}
    .cj-chain{margin-top:1rem;padding:.9rem;border-radius:12px;background:#eef5f3}.cj-chain>strong{display:block;margin:.55rem 0 .25rem}.cj-control{display:grid;grid-template-columns:1fr 1fr;gap:.65rem;margin-top:.7rem}.cj-control>div{padding:.8rem;border:1px solid rgba(19,37,45,.12);border-radius:10px;background:#fff}
    .cj-effect{margin-top:1rem;padding:1rem;border:2px dashed #8c6b2f;border-radius:15px;background:#fffaf0}
    .cj-attrib-head,.cj-test-head{margin-top:2rem}.cj-responsibility{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem}.cj-card{border-left:6px solid #315c7b}.cj-perimeter{border-left-color:#8c2f2c;background:linear-gradient(145deg,#fff,#fff5f2)}.cj-jdam{border-left-color:#6b4f7d;background:linear-gradient(145deg,#fff,#f8f3fb)}.cj-direct{border-left-color:#a65e22}.cj-oversight{border-left-color:#35737b}
    .cj-card a,.cj-links a{font-weight:850;text-decoration-thickness:.1em;text-underline-offset:.18em}.cj-amplifier{margin-top:1rem;padding:1rem 1.1rem;border-radius:15px;background:#13252d;color:#fff}.cj-amplifier>span{color:#f1ce8c}.cj-amplifier a{color:#fff}
    .cj-links{display:flex;flex-wrap:wrap;gap:.6rem 1rem;margin-top:.7rem}.cj-tests{display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem}.cj-tests article>span{display:grid;place-items:center;width:2rem;height:2rem;border-radius:50%;background:#13252d;color:#fff;font-weight:900;font-size:.72rem}
    .cj-boundary{margin-top:1rem;padding:1rem 1.1rem;border-left:6px solid #13252d;border-radius:0 14px 14px 0;background:#13252d;color:#fff}.cj-boundary strong{color:#f1ce8c;text-transform:uppercase;letter-spacing:.07em}.cj-boundary p{margin:.4rem 0 0;line-height:1.6}
    .cj-sources{margin-top:1rem;padding:.9rem 1rem;border:1px solid rgba(19,37,45,.16);border-radius:14px;background:#fff}.cj-sources summary{cursor:pointer;font-weight:900}.cj-sources p{line-height:1.55}
    @media(max-width:820px){.cj-branches,.cj-responsibility,.cj-control,.cj-tests{grid-template-columns:1fr}.cj-tree{padding:.8rem}}
    @media(prefers-reduced-motion:no-preference){.cj-node,.cj-card,.cj-tests article{transition:transform .18s ease,box-shadow .18s ease}.cj-node:hover,.cj-card:hover,.cj-tests article:hover{transform:translateY(-2px);box-shadow:0 .9rem 2rem rgba(19,37,45,.1)}}
  `;
  document.head.append(style);
})();

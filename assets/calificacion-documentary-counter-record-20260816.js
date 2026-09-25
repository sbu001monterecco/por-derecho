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
    kicker: 'CONTRARREGISTRO DOCUMENTAL · ONA HOTELS · PROPIEDAD + EXPLOTACIÓN + FINANCIACIÓN + SALIDA',
    title: 'LPB no era “el hotel entero”: era la concursada y principal sociedad propietaria dentro de un complejo de propiedad mixta. La explotación hotelera era una capa jurídica distinta.',
    lead: 'En junio de 2018 no había simplemente una “empresa hotelera insolvente” buscando un rescate. Había que coordinar accionista, concursada/propietaria, otros propietarios, explotación hotelera, operador profesional, financiación, garantías y salida procesal. Esa arquitectura —y qué conoció cada actor— es material para contrastar las conclusiones posteriores de la calificación.',
    items: [
      ['6 JUN 2018 · CLUBOTEL / ONA HOTELS COMO ANCLA OPERATIVA', 'El contrato de arrendamiento de industria firmado identifica como partes a la Comunidad de Propietarios Sun Park nº1 y Clubotel La Dorada, S.L. en el lado operador. Sus antecedentes describen además la explotación histórica a través de la distinta Comunidad de Explotación. El propio contrato hace visible que propiedad, gobierno y explotación no eran la misma capa jurídica.'],
      ['LPB · CONCURSADA + PRINCIPAL PROPIETARIA, NO TODO EL HOTEL', 'LPB era la deudora concursada y, funcionalmente, la principal sociedad propietaria inmobiliaria dentro de un perímetro de propiedad mixta. Una certificación posterior de 2021 registra 190 de 262 fincas a LPB, 54 a CAM y 18 a terceros; sirve para demostrar la estructura mixta, no para retrotraer automáticamente ese porcentaje exacto a junio de 2018.'],
      ['CUATRECASAS · MUCHO MÁS QUE DUE DILIGENCE', 'La correspondencia documenta DD y revisión registral, pero también trabajo sobre los contratos con ONA, garantías provisionales y posteriores, term sheets/documentación financiera, coordinación con financiadores y escritos/estrategia para cuantificar la deuda y articular la salida del concurso.'],
      ['12 JUN 2018 · GARANTÍAS PROVISIONALES', 'La correspondencia jurídica describe expresamente garantías “provisionales” mientras no podía constituirse todavía la hipoteca post-salida. El paquete cubría valor disponible mediante participaciones, garantías, activos y derechos de crédito. La falta de hipoteca de LPB en esa fase no equivale a ausencia de security package.'],
      ['13 JUN 2018 · DANIEL IRIGOYEN · COORDINACIÓN JURÍDICA', 'Irigoyen —magistrado de carrera y especialista mercantil que constaba en excedencia voluntaria y que en 2018 ejercía como abogado— escribió que se presentó ante el Juez como abogado encargado de coordinar inversor, sociedad accionista, concursada y hotelero. No era simplemente “el abogado de ONA”: su propio relato describe una misión transversal de salida.'],
      ['13 JUN 2018 · JUZGADO + AC', 'Según ese relato contemporáneo, explicó una vía para pagar la deuda concursal, concluir el procedimiento y devolver autonomía a LPB; el Juez permitió explorarla y pidió promover la solicitud, y después Irigoyen trató la vía con la AC. Es evidencia profesional contemporánea, no acta judicial ni prueba de que cada anexo fuera formalmente incorporado.'],
      ['AGO 2018 · OTRA RUTA, TERM SHEET VINCULANTE EJECUTADO', 'Una ruta financiera distinta alcanzó un Binding Term Sheet firmado. Su finalidad expresa era financiar deuda reconocida de LPB para sacarla del proceso de liquidación/concurso. Contemplaba además, bajo condiciones, posible adquisición de activos minoritarios para recomponer el perímetro operativo.'],
      ['GARANTÍA ESCALONADA · PRUEBA PRIMARIA', 'Ese term sheet distingue literalmente “Security Package on closing” y “Security Package once the Company exits liquidation”. Prevé garantías al cierre y el compromiso de constituir la hipoteca de LPB una vez fuera de liquidación. La estructura por etapas forma parte del propio documento.']
    ],
    thesis: 'La pregunta unitaria que debe responderse',
    thesisBody: '<strong>¿Mantuvo la calificación separadas las capas jurídicas —accionista, LPB como concursada/propietaria, otros propietarios, explotación, operador y Comunidades— al atribuir rentas, falta de colaboración y causalidad; y cómo se reconciliaron sus conclusiones posteriores con una salida comercial que en 2018 fue explicada al Juzgado precisamente como coordinación entre inversor, accionista, concursada y hotelero?</strong>',
    boundary: '<strong>Límites obligatorios:</strong> “propco” es una descripción funcional, no una categoría societaria formal; no convertir la certificación 190/262 de 2021 en porcentaje exacto de junio de 2018; no llamar JV formal a la alianza sin contrato de joint venture; no confundir LPB con todo el hotel ni negar que pudiera tener derechos de renta/explotación propios; no llamar incondicional a una financiación condicionada; y no convertir el permiso reportado para explorar la salida en obligación judicial de aprobarla.',
    status: 'Estado de fuente y siguiente prueba',
    statusBody: 'Controlados: contrato hotelero firmado de 6-Jun; separación Comunidad de Propietarios / explotación / Clubotel; relato de Irigoyen de 13-Jun; paquete profesional y garantías provisionales; trabajo transaccional de Cuatrecasas; rutas financieras paralelas y term sheet posterior ejecutado con garantías escalonadas. Abiertos: mapa de titularidad exacto a junio de 2018, eventual contrato formal de JV, escrito/anexos/asiento tras 13-Jun, cifra/certificación de deuda AC, contabilidad operador-rentas y expediente certificado de la vista.',
    link: '../ona-hotels-salida-concurso-36-2012/',
    linkText: 'Ver dossier: ONA Hotels y salida planificada →'
  } : {
    kicker: 'DOCUMENTARY COUNTER-RECORD · ONA HOTELS · OWNERSHIP + OPERATION + FINANCE + EXIT',
    title: 'LPB was not “the whole hotel”: it was the insolvent debtor and principal property-owning company within a mixed-ownership complex. Hotel exploitation was a distinct legal layer.',
    lead: 'By June 2018 this was not simply an “insolvent hotel company” seeking rescue. The exit required coordination of shareholder, insolvent/property company, other owners, hotel exploitation, professional operator, finance, security and court exit mechanics. That architecture — and what each actor knew — is material when testing the later classification findings.',
    items: [
      ['6 JUN 2018 · CLUBOTEL / ONA HOTELS AS OPERATING ANCHOR', 'The signed hotel-industry lease facially identifies Comunidad de Propietarios Sun Park nº1 and Clubotel La Dorada, S.L. on the operator side. Its recitals also describe the separate historical exploitation layer through Comunidad de Explotación. The contract itself makes clear that ownership, governance and exploitation were distinct legal layers.'],
      ['LPB · INSOLVENT + PRINCIPAL OWNER, NOT THE WHOLE HOTEL', 'LPB was the insolvent debtor and, functionally, the principal property-owning company within a mixed-ownership perimeter. A later 2021 certification records 190 of 262 properties to LPB, 54 to CAM and 18 to third parties; it proves mixed ownership structurally but should not be back-projected as an exact June-2018 percentage.'],
      ['CUATRECASAS · FAR MORE THAN DUE DILIGENCE', 'The correspondence documents DD/registry work, but also ONA contract work, provisional and later security structuring, term sheets/finance documentation, financier coordination and court/insolvency work directed at quantifying the debt and advancing the exit.'],
      ['12 JUN 2018 · PROVISIONAL SECURITY', 'Legal correspondence expressly describes “provisional” security while the post-exit mortgage could not yet be created. The package covered available value through shares, guarantees, assets and credit rights. The absence of an LPB mortgage at that stage is not the same as absence of a security package.'],
      ['13 JUN 2018 · DANIEL IRIGOYEN · LEGAL COORDINATION', 'Irigoyen —a career magistrate and mercantile specialist recorded on voluntary leave and practising as a lawyer in 2018— wrote that he presented himself to the Judge as the lawyer tasked with coordinating investor, shareholder company, insolvent company and hotel operator. His own account describes a cross-transaction exit mandate, not merely “ONA’s lawyer”.'],
      ['13 JUN 2018 · COURT + AC', 'According to that contemporaneous account, he explained a route to pay insolvency debt, conclude the proceeding and restore LPB autonomy; the Judge allowed it to be explored and requested the application be pursued, after which Irigoyen discussed the route with the AC. This is contemporaneous professional evidence, not judicial minutes or proof every attachment was formally lodged.'],
      ['AUG 2018 · ANOTHER ROUTE, EXECUTED BINDING TERM SHEET', 'A different finance route reached a signed Binding Term Sheet. Its express purpose was to finance recognised LPB debt so the company could leave liquidation/insolvency. Subject to conditions, it also contemplated potential acquisition of minority-held assets to rebuild the operating perimeter.'],
      ['STAGED SECURITY · PRIMARY DOCUMENT', 'That term sheet literally separates “Security Package on closing” from “Security Package once the Company exits liquidation”. It provides closing security and an undertaking to create the LPB mortgage after exit. The staged architecture is in the document itself.']
    ],
    thesis: 'The unitary question that now has to be answered',
    thesisBody: '<strong>Did the classification keep the legal layers separate — shareholder, LPB as insolvent/property owner, other owners, exploitation, operator and Communities — when attributing rent, non-collaboration and causation; and how were its later findings reconciled with a commercial exit that in 2018 was explained to the Court precisely as coordination among investor, shareholder, insolvent company and hotel operator?</strong>',
    boundary: '<strong>Mandatory boundaries:</strong> “propco” is functional shorthand, not a formal company-law category; do not back-project the later 190/262 certification as an exact June-2018 percentage; do not call the alliance a formal JV without a JV instrument; do not confuse LPB with the whole hotel or deny it could hold its own rent/exploitation rights; do not call conditional finance unconditional; and do not convert reported judicial permission to explore exit into a duty to approve it.',
    status: 'Source status and next proof',
    statusBody: 'Controlled: signed 6-Jun hotel contract; Comunidad/property/exploitation/Clubotel separation; Irigoyen’s 13-Jun account; professional transaction package and provisional security; Cuatrecasas transaction work; parallel finance routes and later executed staged-security term sheet. Open: exact June-2018 ownership map, any formal JV instrument, post-13-Jun filing/annex/docket proof, AC debt figure/certificate, operator/rent accounting and the certified hearing record.',
    link: '../ona-hotels-insolvency-exit-36-2012/',
    linkText: 'Read dossier: ONA Hotels and planned exit →'
  };

  const style = document.createElement('style');
  style.textContent = `
    .calcr{padding:0 0 2.2rem}.calcr-wrap{max-width:1080px;margin:0 auto}.calcr-box{background:#111f26;color:#fff;border-radius:20px;padding:1.35rem;border:1px solid rgba(255,255,255,.12);box-shadow:0 14px 34px rgba(19,37,45,.12)}
    .calcr-kicker{font-size:.73rem;font-weight:900;letter-spacing:.1em;text-transform:uppercase;color:#d8c492}.calcr-box h2{font-size:clamp(1.65rem,3.4vw,2.35rem);line-height:1.08;margin:.35rem 0 .75rem}.calcr-box>p{color:#e7ecee}
    .calcr-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;margin:1rem 0}.calcr-card{background:#fff;color:#17242a;border-radius:14px;padding:1rem;border-top:4px solid #9a7536}.calcr-card strong{display:block;font-size:.78rem;letter-spacing:.055em;text-transform:uppercase;margin-bottom:.4rem;color:#71572d}
    .calcr-thesis{background:#f2eee2;color:#17242a;border-radius:14px;padding:1rem 1.1rem;margin-top:.8rem}.calcr-status{border:1px solid rgba(255,255,255,.24);border-radius:14px;padding:1rem 1.1rem;margin-top:.8rem}.calcr-status h3,.calcr-thesis h3{margin:.1rem 0 .45rem}.calcr-boundary{font-size:.88rem;color:#d6dde0;margin-top:.85rem}.calcr-link{display:inline-block;margin-top:.9rem;padding:.65rem .85rem;border-radius:999px;background:#fff;color:#17242a!important;font-weight:800;text-decoration:none}
    @media(max-width:820px){.calcr-grid{grid-template-columns:1fr}.calcr-box{border-radius:0}}
  `;
  document.head.appendChild(style);

  const cards = c.items.map(([h,b]) => `<article class="calcr-card"><strong>${h}</strong><span>${b}</span></article>`).join('');
  const section = document.createElement('section');
  section.className = 'section calcr';
  section.dataset.calCounterRecord20260816 = '1';
  section.innerHTML = `<div class="shell calcr-wrap"><div class="calcr-box"><div class="calcr-kicker">${c.kicker}</div><h2>${c.title}</h2><p>${c.lead}</p><div class="calcr-grid">${cards}</div><div class="calcr-thesis"><h3>${c.thesis}</h3><p>${c.thesisBody}</p></div><div class="calcr-status"><h3>${c.status}</h3><p>${c.statusBody}</p></div><p class="calcr-boundary">${c.boundary}</p><a class="calcr-link" href="${c.link}">${c.linkText}</a></div></div>`;

  const recovery = document.querySelector('[data-cal-recovery-adversity-20260816]');
  const opening = document.querySelector('[data-calificacion-opening-20260816]');
  const hero = document.querySelector('main .hero');
  if (recovery) recovery.insertAdjacentElement('afterend', section);
  else if (opening) opening.insertAdjacentElement('afterend', section);
  else if (hero) hero.insertAdjacentElement('afterend', section);
})();
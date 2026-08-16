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
    kicker: 'CONTRARREGISTRO DOCUMENTAL · ALIANZA ONA · EXPLOTACIÓN + FINANCIACIÓN + SALIDA',
    title: 'No era un “rescate” de un hotel comercialmente muerto. Era una arquitectura para normalizar la explotación, financiar la salida y devolver a LPB capacidad empresarial.',
    lead: 'La calificación no puede separar renta, hotel, Comunidad, control material, financiación y salida del concurso en expedientes mentales distintos. En junio de 2018 existía una estructura comercial desarrollada en torno a un operador hotelero, plan de negocio, due diligence, tasación, garantías y financiación externa. La causalidad —por qué fue necesaria y por qué no se materializó— debe probarse actor por actor.',
    items: [
      ['6 JUN 2018 · OPERADOR + SALIDA INTERCONECTADOS', 'Existe un instrumento hotelero firmado y un plan de negocio. La correspondencia de la operación describe a ONA como operador previsto; la identidad jurídica de las partes del contrato debe mantenerse separada. La adenda suspensiva vinculaba la eficacia operativa a fondos suficientes para que LPB pudiera salir del concurso.'],
      ['8 JUN 2018 · PAQUETE PROFESIONAL', 'La correspondencia reúne plan de negocio, due diligence de Cuatrecasas, tasación ECO presentada en la operación en aproximadamente 25,6 M€, garantías, financiación puente en estructuración y una vía alternativa de transacción. Es prueba de trabajo comercial desarrollado, no de que todos los instrumentos estuvieran cerrados.'],
      ['12 JUN 2018 · GARANTÍAS PROVISIONALES', 'La correspondencia jurídica describe expresamente garantías “provisionales” mientras no podía constituirse todavía la hipoteca post-salida. El paquete cubría valor disponible mediante participaciones, garantías, activos y derechos de crédito. La falta de hipoteca de LPB en esa fase no equivale a ausencia de security package.'],
      ['JUN 2018 · FINANCIACIÓN AVANZADA, PERO CONDICIONADA', 'Una ruta financiera llegó a documentación avanzada con condiciones materiales. La asesoría jurídica advirtió después que esa ruta seguía condicionada y no constituía todavía un “safe harbor”. Este contrahecho se mantiene visible.'],
      ['13 JUN 2018 · JUZGADO + AC', 'El relato contemporáneo de Daniel Irigoyen dice que expuso al Juez una vía coordinada entre fondo, socio/sociedad y explotadora para concluir el concurso pagando la deuda, y después la trató con la AC. Según ese relato, el Juez permitió explorarla y pidió promover la solicitud. Es evidencia profesional contemporánea, no acta judicial ni prueba de que cada anexo fuera formalmente incorporado.'],
      ['AGO 2018 · OTRA RUTA, TERM SHEET VINCULANTE EJECUTADO', 'Una ruta financiera distinta alcanzó un Binding Term Sheet firmado. Su finalidad expresa era financiar deuda reconocida de LPB para sacarla del proceso de liquidación/concurso. Contemplaba además, bajo condiciones, posible adquisición de activos minoritarios para recomponer el perímetro operativo.'],
      ['GARANTÍA ESCALONADA · PRUEBA PRIMARIA', 'Ese term sheet distingue literalmente “Security Package on closing” y “Security Package once the Company exits liquidation”. Prevé garantías al cierre y el compromiso de constituir la hipoteca de LPB una vez fuera de liquidación. La estructura por etapas forma parte del propio documento.'],
      ['SEP 2018 · LA FINANCIACIÓN SIGUIÓ AVANZANDO', 'La correspondencia posterior transmite el term sheet ejecutado y registra trabajo entre asesores sobre la documentación de financiación y garantías. La proposición pública no depende de nombrar prestamistas: existieron rutas paralelas y sucesivas antes y después del 13-Jun.']
    ],
    thesis: 'La pregunta unitaria que debe responderse',
    thesisBody: '<strong>¿Qué ocurrió con una arquitectura comercial destinada a pagar la deuda, concluir el concurso, activar una explotación hotelera profesional y reducir la fragmentación de unidades, cuya ejecución dependía en parte de la cifra de deuda, tratamiento procesal y garantías que sólo podían completarse por etapas?</strong> Gil Marer alega que la necesidad de esa estructura extraordinaria derivó de interferencia privada, disfunción de gobierno/explotación, actuaciones de la AC y tratamiento judicial. La arquitectura está documentada; esa causalidad y el fracaso de cierre deben demostrarse actor por actor.',
    boundary: '<strong>Límites obligatorios:</strong> no fusionar ONA y la entidad firmante del contrato sin fuente; no llamar incondicional a una ruta que tenía condiciones; no afirmar que todos los documentos se presentaron al Juez sin LexNET/asiento; no identificar prestamistas cuando su identidad no es necesaria; no convertir la estructura escalonada de garantías en prueba de desembolso; y no convertir el permiso reportado para explorar la salida en obligación judicial de aprobarla.',
    status: 'Estado de fuente y siguiente prueba',
    statusBody: 'Controlados: instrumento hotelero y adenda suspensiva de 6-Jun; paquete de 8-Jun; correspondencia sobre garantías provisionales; ruta financiera condicionada de junio; relato de Irigoyen de 13-Jun; y una ruta posterior con Binding Term Sheet ejecutado que separa garantías de cierre y garantías post-salida. Abiertos: escrito exacto presentado tras 13-Jun, anexos/asiento, cifra/certificación de deuda AC, ledger condición-por-condición de cada ruta, y paquete primario completo de la operación Monte Lanza–Multimatrix de 2008.',
    link: '../ona-hotels-salida-concurso-36-2012/',
    linkText: 'Ver dossier: alianza ONA y salida planificada →'
  } : {
    kicker: 'DOCUMENTARY COUNTER-RECORD · ONA ALLIANCE · OPERATION + FINANCE + EXIT',
    title: 'This was not a “rescue” of a commercially dead hotel. It was an architecture intended to normalise operation, finance exit and restore LPB’s business capacity.',
    lead: 'The classification cannot fairly separate rent, the hotel, the Community, material control, finance and insolvency exit into disconnected analytical files. By June 2018 a developed commercial structure existed around a hotel operator, business plan, due diligence, valuation, security and external finance. Causation — why it became necessary and why it did not complete — must be proved actor by actor.',
    items: [
      ['6 JUN 2018 · OPERATOR + EXIT INTERLOCKED', 'A signed hotel instrument and business plan existed. Transaction correspondence described ONA as the intended operator; the legal identity of the contract parties must remain separate. The suspensive addendum linked operational effectiveness to sufficient money being available for LPB to leave the insolvency process.'],
      ['8 JUN 2018 · PROFESSIONAL TRANSACTION STACK', 'Finance correspondence brings together a business plan, Cuatrecasas due diligence, an ECO valuation presented in the transaction at about EUR 25.6m, security, bridge-finance structuring and an alternative transaction route. This proves developed commercial work, not that every instrument had closed.'],
      ['12 JUN 2018 · PROVISIONAL SECURITY', 'Legal correspondence expressly describes “provisional” security while the post-exit mortgage could not yet be created. The package covered available value through shares, guarantees, assets and credit rights. The absence of an LPB mortgage at that stage is not the same as absence of a security package.'],
      ['JUN 2018 · ADVANCED BUT CONDITIONAL FINANCE', 'One finance route reached advanced documentation with material conditions. Counsel later warned that the route remained conditional and was not yet a “safe harbor”. That counterevidence stays visible.'],
      ['13 JUN 2018 · COURT + AC', 'Daniel Irigoyen’s contemporaneous account says he presented a route coordinating fund, shareholder/company and operator to conclude the insolvency by paying debt, then discussed it with the AC. According to his account, the Judge allowed the route to be explored and requested that the application be pursued. This is contemporaneous professional evidence, not judicial minutes or proof every attachment was formally lodged.'],
      ['AUG 2018 · ANOTHER ROUTE, EXECUTED BINDING TERM SHEET', 'A different finance route reached a signed Binding Term Sheet. Its express purpose was to finance recognised LPB debt so the company could leave liquidation/insolvency. Subject to conditions, it also contemplated potential acquisition of minority-held assets to rebuild the operating perimeter.'],
      ['STAGED SECURITY · PRIMARY DOCUMENT', 'That term sheet literally separates “Security Package on closing” from “Security Package once the Company exits liquidation”. It provides closing security and an undertaking to create the LPB mortgage after exit. The staged architecture is in the document itself.'],
      ['SEP 2018 · FINANCE WORK CONTINUED', 'Later correspondence transmits the executed term sheet and records adviser work on financing and security documents. The public proposition does not depend on naming lenders: parallel and successive routes existed before and after 13 June.']
    ],
    thesis: 'The unitary question that now has to be answered',
    thesisBody: '<strong>What happened to a commercial architecture intended to pay debt, conclude insolvency, activate professional hotel operation and reduce unit fragmentation, where performance depended partly on the debt figure, procedural treatment and security that could only be completed in stages?</strong> Gil Marer alleges that the need for this extraordinary structure arose from private interference, governance/operation dysfunction, AC conduct and judicial handling. The architecture is documented; that causation and the failure to close must be proved actor by actor.',
    boundary: '<strong>Mandatory boundaries:</strong> do not merge ONA with the contract signatory entity without a source; do not call a conditional route unconditional; do not say every document was filed with the Judge without LexNET/docket proof; do not identify lenders when identity is unnecessary; do not turn staged security into proof of drawdown; and do not convert reported judicial permission to explore exit into a duty to approve it.',
    status: 'Source status and next proof',
    statusBody: 'Controlled: the 6-Jun hotel instrument/suspensive addendum; 8-Jun transaction package; provisional-security correspondence; a conditional June finance route; Irigoyen’s 13-Jun account; and a later executed Binding Term Sheet separating closing and post-exit security. Open: exact post-13-Jun filing and docket proof, AC debt figure/certificate, a condition-by-condition ledger for each finance route, and the complete primary 2008 Monte Lanza–Multimatrix transaction package.',
    link: '../ona-hotels-insolvency-exit-36-2012/',
    linkText: 'Read dossier: ONA alliance and planned exit →'
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
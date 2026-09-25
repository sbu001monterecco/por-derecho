(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const esRoutes = [
    '/por-derecho/es/calificacion-concurso-36-2012-vidas-paralelas/',
    '/por-derecho/es/toma-control-sun-park-7-junio-2018/',
    '/por-derecho/es/concurso-36-2012-administrador-concursal/',
    '/por-derecho/es/concurso-36-2012-magistrado-juez/',
    '/por-derecho/es/concurso-36-2012-juzgado-mercantil-1/',
    '/por-derecho/es/concurso-36-2012-responsabilidad-institucional/',
    '/por-derecho/es/carta-abierta-ministerio-fiscal/',
    '/por-derecho/es/dp-1901-2026/'
  ];
  const enRoutes = [
    '/por-derecho/en/insolvency-classification-parallel-lives/',
    '/por-derecho/en/sun-park-takeover-7-june-2018/',
    '/por-derecho/en/insolvency-36-2012-insolvency-administrator/',
    '/por-derecho/en/insolvency-36-2012-mercantile-court-1/',
    '/por-derecho/en/insolvency-36-2012-institutional-accountability/',
    '/por-derecho/en/open-letter-public-prosecution-service/'
  ];

  const es = esRoutes.includes(path);
  const en = enRoutes.includes(path);
  if (!es && !en) return;
  if (document.querySelector('[data-borja-security-source-upgrade-20260816]')) return;

  const d = es ? {
    eyebrow: '25 JUN 2018 · CONTROL DE FUENTE CONTEMPORÁNEA',
    title: 'La contraparte estaba utilizando el propio correo de seguridad del Administrador Concursal como soporte en la disputa de control.',
    lead: 'Un informe por correo del abogado Cristo Pimentel, fechado el 25 de junio de 2018, dejó constancia de que la contraparte había aportado al procedimiento de Arrecife un correo de <strong>Francisco de Borja Rodríguez-Batllori Laffitte</strong>, Administrador Concursal, en el que —según el abogado— se solicitaba contratar un servicio de seguridad para el <strong>complejo</strong> para evitar su deterioro.',
    points: [
      ['QUÉ AÑADE', '<strong>La cuestión ya no es sólo si el AC conocía una toma de control ajena.</strong> Su propia intervención de seguridad formaba parte del material que la contraparte invocaba para sostener su posición en la controversia de acceso/control.'],
      ['QUÉ NO PRUEBA', '<strong>No demuestra todavía que Borja entregara físicamente las llaves del hotel a CAM</strong>, ni que ordenara cada rotura de cerradura, exclusión o acto de acceso. Esa cadena sigue necesitando correo nativo, instrucciones, contrato de seguridad, inventarios de llaves/códigos, cerrajero, guardias y atestados.'],
      ['VERSIÓN CONTRARIA', 'También se conserva la explicación comunicada por Borja a través de otro abogado el 8 de junio: que la seguridad había sido acordada por la Comunidad y que CAM no había entrado en apartamentos de LPB, sino en unidades propias y zonas comunes. <strong>Ambas versiones deben confrontarse con la prueba primaria.</strong>'],
      ['VALORACIÓN DE PARTE', 'El abogado de LPB describió entonces la actuación de la contraparte como “fraudulenta”. <strong>Esa palabra es una valoración jurídica/de parte, no una declaración judicial de fraude.</strong>']
    ],
    question: '<strong>Pregunta central para el AC:</strong> ¿qué autorizó exactamente, para qué perímetro, a quién, con qué instrucciones y con qué efectos sobre seguridad, llaves, cerraduras, accesos, recepción, mantenimiento y bienes o derechos que no pertenecían a la masa de LPB?',
    causation: '<strong>Consecuencia para la Calificación:</strong> si después del 7 de junio se atribuyen a Gil/LPB/Pink deterioro, falta de operación, pérdida de ingresos, falta de mantenimiento, falta de documentación o fracaso de rescate, primero debe determinarse quién tenía la capacidad material real para acceder, excluir, operar, mantener y producir esa documentación, y qué parte del perjuicio era concursal o extraconcursal.',
    source: 'Fuente controlada interna: correo contemporáneo de abogado de 25-06-2018 y comunicaciones de 7–11-06-2018. Correcciones CR-018 y CR-042. La cadena primaria de llaves/seguridad permanece abierta.'
  } : {
    eyebrow: '25 JUN 2018 · CONTEMPORANEOUS SOURCE CONTROL',
    title: 'The opposing side was relying on the Insolvency Administrator’s own security email in the control dispute.',
    lead: 'A contemporaneous email report from lawyer Cristo Pimentel, dated 25 June 2018, records that the opposing side had put before the Arrecife proceeding an email from <strong>Francisco de Borja Rodríguez-Batllori Laffitte</strong>, the Insolvency Administrator, which — as counsel described it — requested that a security service be hired for the <strong>complex</strong> to prevent deterioration.',
    points: [
      ['WHAT THIS ADDS', '<strong>The issue is no longer only whether the IA knew about somebody else’s takeover.</strong> His own security intervention formed part of the material the opposing side invoked to support its position in the access/control dispute.'],
      ['WHAT IT DOES NOT PROVE', '<strong>It does not yet prove that Borja physically handed the hotel keys to CAM</strong>, or that he ordered every lock change, exclusion or access act. That chain still requires the native email, instructions, security contract, key/code inventories, locksmith, guard and police records.'],
      ['CONTRARY ACCOUNT', 'The repository also preserves the explanation attributed to Borja through counsel on 8 June: that security had been approved by the Community and CAM had not entered LPB apartments, only its own units and common areas. <strong>Both accounts must be tested against the primary record.</strong>'],
      ['PARTY CHARACTERISATION', 'LPB’s lawyer at the time described the opposing conduct as “fraudulent”. <strong>That word is a party/legal characterisation, not a judicial finding of fraud.</strong>']
    ],
    question: '<strong>Core question for the IA:</strong> what exactly did he authorise, for what perimeter, to whom, under what instructions, and with what effects on security, keys, locks, access, reception, maintenance and property or rights outside LPB’s insolvency estate?',
    causation: '<strong>Classification consequence:</strong> if post-7-June deterioration, non-operation, lost revenue, maintenance failure, document non-production or rescue failure is attributed to Gil/LPB/Pink, the analysis must first establish who actually had the material capacity to access, exclude, operate, maintain and produce records, and which harm belonged to the estate versus extraconcursal rights.',
    source: 'Controlled internal source: contemporaneous counsel email dated 25-06-2018 and 7–11-06-2018 communications. Corrections CR-018 and CR-042. The primary keys/security chain remains open.'
  };

  const section = document.createElement('section');
  section.className = 'section borja-security-source-upgrade';
  section.setAttribute('data-borja-security-source-upgrade-20260816', '');
  section.innerHTML = `
    <div class="shell">
      <div class="section-head">
        <div><p class="kicker">${d.eyebrow}</p><h2>${d.title}</h2></div>
        <p>${d.lead}</p>
      </div>
      <div class="bssu-grid">${d.points.map(([h,b]) => `<article><h3>${h}</h3><p>${b}</p></article>`).join('')}</div>
      <aside class="bssu-question">${d.question}</aside>
      <p class="bssu-causation">${d.causation}</p>
      <p class="bssu-source">${d.source}</p>
    </div>`;

  const style = document.createElement('style');
  style.textContent = `
    .borja-security-source-upgrade{border-block:1px solid rgba(138,108,53,.3);background:rgba(138,108,53,.055)}
    .bssu-grid{display:grid;gap:1rem;margin:1.2rem 0}
    .bssu-grid article{padding:1rem 1.05rem;border:1px solid rgba(19,37,45,.16);border-radius:14px;background:rgba(255,255,255,.72)}
    .bssu-grid h3{font-size:.9rem;letter-spacing:.04em;margin:.05rem 0 .45rem}
    .bssu-grid p{margin:0}
    .bssu-question{padding:1.1rem 1.2rem;border-left:4px solid currentColor;background:rgba(19,37,45,.055);margin:1.25rem 0}
    .bssu-causation{font-size:1.02rem}
    .bssu-source{font-size:.8rem;opacity:.72}
    @media(min-width:760px){.bssu-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
  `;
  document.head.appendChild(style);

  const mount = () => {
    if (section.isConnected) return;
    const primary = document.querySelector('[data-extraconcursal-force-20260816]');
    if (primary) {
      primary.insertAdjacentElement('afterend', section);
      return;
    }
    const main = document.querySelector('main');
    if (!main) return;
    const hero = main.querySelector('.dossier-hero, .page-hero, .hero');
    if (hero && hero.parentNode === main) hero.insertAdjacentElement('afterend', section);
    else main.insertAdjacentElement('afterbegin', section);
  };

  mount();
  if (!section.isConnected) setTimeout(mount, 0);
})();
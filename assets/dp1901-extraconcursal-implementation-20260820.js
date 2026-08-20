(() => {
  const marker = 'data-dp1901-extraconcursal-20260820';
  if (document.documentElement.hasAttribute(marker)) return;
  document.documentElement.setAttribute(marker, 'true');

  const path = window.location.pathname.replace(/index\.html$/, '');
  const isES = /\/es\//.test(path);
  const root = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const lang = isES ? 'es' : 'en';
  const dedicated = isES ? `${root}es/matkator-nucleo-extraconcursal/` : `${root}en/matkator-extraconcursal-core/`;

  const copy = isES ? {
    homeTitle: 'DP 1901/2026 · el núcleo privado y extraconcursal',
    homeLead: 'La cuestión actual no es sólo qué ocurrió dentro del concurso de LPB. La cuestión sometida a contraste es si una posición limitada —dominical, crediticia o comunitaria— fue convertida en autoridad documental, control físico, presentación hotelera unitaria, explotación MYND, financiación/incentivos e ingresos retenidos, afectando también a Matkator, Aweswell y otros patrimonios no concursales.',
    boundary: 'No se presenta como declaración de culpabilidad. Se presenta como una ruta de investigación material, finita y patrimonialmente diferenciada que debe confirmarse o descartarse con fuentes primarias.',
    button: 'Abrir el núcleo extraconcursal',
    chain: 'finca → título → autoridad → acceso → obra → habitación/PMS → ingreso → rendición → beneficiario',
    takeoverTitle: 'Por qué el 7 de junio importa para DP 1901/2026',
    takeoverText: 'La toma material no es sólo un problema posesorio o concursal. Es el punto en el que la apariencia documental pudo convertirse en control extraconcursal: seguridad, llaves, cerraduras, accesos, exclusión, mediciones, proyectos, obras y posterior explotación. La pregunta es qué bienes no LPB, qué unidades Matkator, qué derechos Aweswell y qué ingresos quedaron afectados.',
    mechanismTitle: 'El mecanismo finito que debe comprobarse',
    ricTitle: 'RIC / FEDER / incentivos: la pregunta segura',
    ricText: 'No se afirma aquí que fondos públicos o europeos se pagaran irregularmente. La pregunta documental es qué título, disponibilidad, promotor, propiedad, licencia, obras, actividad, empleo y documentos de proyecto se aportaron a HNT, RPE/RICPE, AEAT, Gobierno de Canarias, organismos de incentivos/FEDER, financiadores e inversores.',
    fiscalTitle: 'Fiscalía / DP 1901: actividad formal no equivale a investigación material',
    fiscalText: 'La cuestión no es si existió actividad formal, registros, remisiones o archivos. La cuestión es si existe una investigación material equivalente sobre título, autoridad, acceso, documentos originales, obras, operación, ingresos y beneficiarios. Si existe, debe identificarse; si no existe, debe asignarse.',
    proofTitle: 'Yaiza como motor de prueba pública',
    proofText: 'IBI, basura, recaudación, sujeto pasivo, pagador, Catastro, licencias, primera ocupación, proyectos, presentador, poder, firmante, finca afectada, comprobación municipal y efecto producido.'
  } : {
    homeTitle: 'DP 1901/2026 · the private and extraconcursal core',
    homeLead: 'The current question is not only what happened inside LPB’s insolvency. The question for verification is whether a limited ownership, credit or Community position was converted into documentary authority, physical control, whole-hotel presentation, MYND operation, financing/incentives and retained income, also affecting Matkator, Aweswell and other non-estate patrimonies.',
    boundary: 'This is not presented as a finding of guilt. It is a finite, material and patrimonially differentiated investigation route that must be confirmed or excluded through primary sources.',
    button: 'Open the extraconcursal core',
    chain: 'unit → title → authority → access → works → room/PMS → income → accounting → beneficiary',
    takeoverTitle: 'Why 7 June matters for DP 1901/2026',
    takeoverText: 'The material takeover is not only a possession or insolvency issue. It is the point where documentary appearance may have become extraconcursal control: security, keys, locks, access, exclusion, measurements, projects, works and later operation. The question is which non-LPB assets, Matkator units, Aweswell rights and income flows were affected.',
    mechanismTitle: 'The finite mechanism to verify',
    ricTitle: 'RIC / FEDER / incentives: the safe question',
    ricText: 'This does not assert that public or European funds were irregularly paid. The documentary question is what title, availability, promoter, ownership, licence, works, activity, employment and project documents were supplied to HNT, RPE/RICPE, AEAT, the Government of the Canary Islands, incentive/FEDER bodies, financiers and investors.',
    fiscalTitle: 'Prosecution / DP 1901: formal activity is not material investigation',
    fiscalText: 'The issue is not whether formal activity, filings, remissions or archives existed. The issue is whether an equivalent material investigation exists into title, authority, access, original documents, works, operation, income and beneficiaries. If it exists, it should be identified; if it does not, it should be assigned.',
    proofTitle: 'Yaiza as a public proof engine',
    proofText: 'IBI/property tax, waste charges, collection, taxpayer, payer, Cadastre, licences, first occupation, projects, presenter, power, signatory, affected property, municipal verification and effect produced.'
  };

  const steps = isES ? [
    ['Posición limitada', 'Una posición dominical, crediticia o comunitaria limitada no equivale por sí sola a autoridad sobre todo el hotel.'],
    ['Autoridad documental aparente', 'Actas, censo, voto, deuda, certificados, representación, cargos, poderes y banca comunitaria deben comprobarse en origen.'],
    ['Control material', 'Seguridad, llaves, cerraduras, accesos, exclusión, mediciones, pilotos, proyectos y obras pudieron convertir apariencia en control físico.'],
    ['Presentación unitaria', 'El establecimiento fue presentado comercial, técnica y financieramente como proyecto hotelero completo.'],
    ['Transferencia y operación', 'Debe reconstruirse qué activos y derechos pasaron realmente a CAM-HNT y a Canarian Hospitality/MYND.'],
    ['Monetización y beneficiario', 'Reservas, ingresos, contratos, financiación, incentivos, costes, aumento de valor, cuentas y beneficiarios finales.']
  ] : [
    ['Limited position', 'A limited ownership, credit or Community position is not by itself authority over the whole hotel.'],
    ['Apparent documentary authority', 'Minutes, census, votes, debt, certificates, representation, offices, powers and Community banking must be checked at origin.'],
    ['Material control', 'Security, keys, locks, access, exclusion, measurements, pilots, projects and works may have converted appearance into physical control.'],
    ['Whole-hotel presentation', 'The establishment was presented commercially, technically and financially as a complete hotel project.'],
    ['Transfer and operation', 'The real assets and rights in the CAM-HNT and Canarian Hospitality/MYND chain must be reconstructed.'],
    ['Monetisation and beneficiary', 'Reservations, income, contracts, financing, incentives, costs, value uplift, accounts and final beneficiaries.']
  ];

  const style = document.createElement('style');
  style.textContent = `
    .dp1901-panel{margin:2.2rem auto;padding:1.45rem;border:1px solid rgba(168,130,72,.36);border-radius:1rem;background:linear-gradient(135deg,rgba(255,250,240,.98),rgba(245,238,222,.92));box-shadow:0 18px 44px rgba(18,33,41,.08)}
    .dp1901-panel .kicker{margin:0 0 .35rem;text-transform:uppercase;letter-spacing:.12em;font-size:.72rem;font-weight:800;color:#8a6a3d}
    .dp1901-panel h2,.dp1901-panel h3{margin:.15rem 0 .75rem;color:#18252a;font-family:Georgia,'Times New Roman',serif;line-height:1.15}
    .dp1901-panel h2{font-size:clamp(1.65rem,3vw,2.5rem)}
    .dp1901-panel h3{font-size:clamp(1.35rem,2.4vw,2rem)}
    .dp1901-panel p{color:#33454d;line-height:1.68;max-width:70rem}
    .dp1901-boundary{margin-top:1rem;padding:1rem;border-left:4px solid #a88248;background:rgba(255,255,255,.72);border-radius:.7rem;color:#33454d;line-height:1.6}
    .dp1901-chain{margin:1rem 0;padding:.85rem 1rem;border-radius:999px;background:#13252d;color:#fff;font-weight:800;line-height:1.5;display:inline-block}
    .dp1901-steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin-top:1.1rem}
    .dp1901-step{padding:1rem;border:1px solid rgba(24,37,42,.12);border-radius:.85rem;background:rgba(255,255,255,.75)}
    .dp1901-step strong{display:block;color:#18252a;margin-bottom:.35rem}.dp1901-step span{display:block;color:#536268;line-height:1.55;font-size:.92rem}
    .dp1901-mini-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin-top:1rem}.dp1901-mini{padding:1rem;border-radius:.85rem;background:#fff;border:1px solid rgba(24,37,42,.12)}
    .dp1901-mini strong{display:block;color:#18252a;margin-bottom:.35rem}.dp1901-mini span{color:#536268;line-height:1.58;font-size:.94rem}
    .dp1901-panel .button{margin-top:1rem}.dp1901-home{max-width:1180px}.dp1901-route{max-width:1180px}
    @media(max-width:850px){.dp1901-steps,.dp1901-mini-grid{grid-template-columns:1fr}.dp1901-chain{border-radius:.85rem}}
  `;
  document.head.appendChild(style);

  function panel(id, html, cls='') {
    if (document.getElementById(id)) return null;
    const el = document.createElement('section');
    el.className = `dp1901-panel ${cls}`.trim();
    el.id = id;
    el.innerHTML = html;
    return el;
  }
  function after(selector, element) {
    const anchor = document.querySelector(selector);
    if (anchor && element) anchor.insertAdjacentElement('afterend', element);
  }
  function before(selector, element) {
    const anchor = document.querySelector(selector);
    if (anchor && element) anchor.insertAdjacentElement('beforebegin', element);
  }
  function stepGrid() {
    return `<div class="dp1901-steps">${steps.map(([a,b])=>`<article class="dp1901-step"><strong>${a}</strong><span>${b}</span></article>`).join('')}</div>`;
  }

  const homeES = /\/es\/?$/.test(path) || /\/por-derecho\/es\/?$/.test(path);
  const homeEN = /\/en\/?$/.test(path) || /\/por-derecho\/en\/?$/.test(path);
  if (homeES || homeEN) {
    const home = panel('dp1901-extraconcursal-home', `
      <div class="shell dp1901-home">
        <p class="kicker">DP 1901/2026 · ${isES ? 'ruta de investigación actual' : 'current investigation route'}</p>
        <h2>${copy.homeTitle}</h2>
        <p>${copy.homeLead}</p>
        <div class="dp1901-chain">${copy.chain}</div>
        <div class="dp1901-boundary"><strong>${isES ? 'Límite público:' : 'Public boundary:'}</strong> ${copy.boundary}</div>
        <div class="dp1901-mini-grid"><article class="dp1901-mini"><strong>${copy.fiscalTitle}</strong><span>${copy.fiscalText}</span></article><article class="dp1901-mini"><strong>${copy.proofTitle}</strong><span>${copy.proofText}</span></article></div>
        <a class="button" href="${dedicated}">${copy.button}</a>
      </div>
    `, 'dp1901-home-section');
    before(isES ? '#resumen-60-segundos' : '#sixty-second-summary', home);
  }

  if (/toma-control-sun-park-7-junio-2018|sun-park-takeover-7-june-2018/.test(path)) {
    after(isES ? '#perimetros-juridicos' : '#legal-perimeters', panel('dp1901-takeover-link', `
      <div class="shell dp1901-route"><p class="kicker">DP 1901/2026</p><h3>${copy.takeoverTitle}</h3><p>${copy.takeoverText}</p><div class="dp1901-chain">${copy.chain}</div><a class="button" href="${dedicated}">${copy.button}</a></div>
    `));
  }

  if (/comunidad-instrumentalizacion|community-instrumentalisation/.test(path)) {
    after(isES ? '#resumen' : '#summary', panel('dp1901-community-mechanism', `
      <div class="shell dp1901-route"><p class="kicker">DP 1901/2026</p><h3>${copy.mechanismTitle}</h3><p>${isES ? 'La instrumentalización comunitaria debe conectarse ahora con una secuencia privada y extraconcursal finita, no sólo con una disputa interna de comunidad.' : 'Community instrumentalisation must now be connected to a finite private and extraconcursal sequence, not only to an internal Community dispute.'}</p>${stepGrid()}<a class="button" href="${dedicated}">${copy.button}</a></div>
    `));
  }

  if (/ric-private-equity-sun-park/.test(path)) {
    after(isES ? '#pregunta-unitaria' : '#unitary-question', panel('dp1901-ric-safe-question', `
      <div class="shell dp1901-route"><p class="kicker">DP 1901/2026 · ${isES ? 'financiación e incentivos' : 'finance and incentives'}</p><h3>${copy.ricTitle}</h3><p>${copy.ricText}</p><div class="dp1901-boundary"><strong>${isES ? 'Matriz de conciliación:' : 'Reconciliation matrix:'}</strong> ${copy.chain}</div></div>
    `));
  }

  if (/actualizaciones|updates|institucional|institutional|fiscalia|prosecution|yaiza|cabildo/.test(path)) {
    const main = document.querySelector('main .section, main section, main');
    if (main && !document.getElementById('dp1901-public-authority-checklist')) {
      main.insertAdjacentElement('afterend', panel('dp1901-public-authority-checklist', `
        <div class="shell dp1901-route"><p class="kicker">DP 1901/2026 · ${isES ? 'control público' : 'public control'}</p><h3>${copy.fiscalTitle}</h3><p>${copy.fiscalText}</p><div class="dp1901-mini-grid"><article class="dp1901-mini"><strong>${copy.proofTitle}</strong><span>${copy.proofText}</span></article><article class="dp1901-mini"><strong>${isES ? 'Producción o certificación' : 'Production or certification'}</strong><span>${isES ? 'Informe fiscal, corpus documental, instrucciones, visado, remisión, acuse, resolución posterior, Matkator, Comunidad, acceso, Catastro, Cabildo/Yaiza, obras, operación, ingresos y actores privados.' : 'Fiscal report, document corpus, instructions, review, remittance, receipt, later order, Matkator, Community, access, Cadastre, Cabildo/Yaiza, works, operation, income and private actors.'}</span></article></div></div>
      `));
    }
  }
})();
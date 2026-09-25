(() => {
  const path = window.location.pathname;
  if (path.includes('/via-residual-articulo-1535/') || path.includes('/residual-article-1535-pathway/')) return;

  const targets = [
    '/retracto-credito-litigioso-1041-2017/',
    '/litigious-credit-retracto-1041-2017/',
    '/acreedor-de-registro/',
    '/lender-of-record/',
    '/insolvencia-lpb/',
    '/lpb-insolvency/',
    '/convergencia-venta-acreedor/',
    '/sale-lender-convergence/',
    '/acosta-matos-perimetro/',
    '/acosta-matos-perimeter/',
    '/patron-efectos-favorables-acosta-matos/',
    '/acosta-matos-favourable-effect-pattern/',
    '/concurso-36-2012-administrador-concursal/',
    '/insolvency-36-2012-insolvency-administrator/',
    '/concurso-36-2012-magistrado-juez/',
    '/insolvency-36-2012-mercantile-court-1/',
    '/concurso-36-2012-responsabilidad-institucional/',
    '/insolvency-36-2012-institutional-accountability/',
    '/toma-control-sun-park-7-junio-2018/',
    '/sun-park-takeover-7-june-2018/',
    '/mismo-hotel-multiples-vidas-financieras/',
    '/same-hotel-multiple-financial-lives/',
    '/ricpe-responsabilidad-documental/',
    '/ricpe-documentary-accountability/',
    '/cadena-instrumentalizacion-ric-fondos-incentivos/',
    '/institutionalisation-chain-ric-eu-incentives/',
    '/objetivos-recuperacion-restitucion/',
    '/recovery-restitution-objectives/'
  ];
  if (!targets.some(fragment => path.includes(fragment))) return;
  if (document.querySelector('[data-art1535-reserve-pathway]')) return;

  const isEn = path.includes('/en/');
  const copy = isEn ? {
    eyebrow: 'THE RESERVE CARD · UPSTREAM DEPENDENCY',
    title: 'One question remains upstream of everything else.',
    body: `What if CAM's route into the later hotel position began with a credit that LPB could lawfully have extinguished on CAM's own acquisition-cost basis? Por Derecho does not say Article 1535 automatically gives LPB the hotel. It treats the unresolved PH122→CAM credit position as a <strong>reserve restoration pathway</strong> that can require the later chain to be recalculated from the beginning.`,
    flow: 'PH122 credit → CAM recognition → insolvency leverage → adjudication/dación → CAM/HNT → finance/refurbishment → MYND',
    test: '<strong>Bridge-removal test:</strong> assume effective Article 1535 exercise at the relevant time, reimburse CAM its acquisition price plus the statutory additions, extinguish the assigned credit, and then ask which later rights survive independently.',
    trigger: '<strong>P0 trigger issue:</strong> the nine days run from the assignee’s demand for payment. The trigger history has to be reconstructed before the position can responsibly be described as expired—or before any new step is taken that might provoke a fresh trigger.',
    limit: 'This is not an established “freeze-the-clock” doctrine. Literal exercise, restoration of a frustrated position and equivalent-value restitution are alternative routes still requiring adjudication.',
    cta: 'Open the residual Article 1535 pathway',
    href: '/por-derecho/en/residual-article-1535-pathway/'
  } : {
    eyebrow: 'LA CARTA DE RESERVA · DEPENDENCIA AGUAS ARRIBA',
    title: 'Una pregunta permanece aguas arriba de todo lo demás.',
    body: `¿Y si la ruta de CAM hacia la posición posterior en el hotel comenzó con un crédito que LPB podía extinguir legalmente sobre la base del propio precio de adquisición de CAM? Por Derecho no afirma que el art. 1535 entregue automáticamente el hotel a LPB. Trata la posición PH122→CAM no resuelta como una <strong>vía residual de restitución</strong> capaz de obligar a recalcular la cadena posterior desde el principio.`,
    flow: 'crédito PH122 → reconocimiento CAM → palanca concursal → adjudicación/dación → CAM/HNT → financiación/reforma → MYND',
    test: '<strong>Prueba de retirada del puente:</strong> supóngase un ejercicio eficaz del art. 1535 en el momento relevante, reembólsese a CAM su precio de adquisición más los conceptos legales, extíngase el crédito cedido y pregúntese qué derechos posteriores sobreviven de forma independiente.',
    trigger: '<strong>Cuestión P0 del disparador:</strong> los nueve días corren desde que el cesionario reclama el pago. Hay que reconstruir esa historia antes de poder describir responsablemente la posición como caducada —o antes de realizar un nuevo paso que pudiera provocar un disparador fresco.',
    limit: 'No se publica como doctrina ya establecida un “derecho a congelar el reloj”. Ejercicio literal, restauración de una posición frustrada y restitución por valor equivalente son vías alternativas que todavía requieren determinación judicial.',
    cta: 'Abrir la vía residual del art. 1535',
    href: '/por-derecho/es/via-residual-articulo-1535/'
  };

  const style = document.createElement('style');
  style.textContent = `
    .art1535-reserve{max-width:1100px;margin:1.4rem auto;padding:0 1rem}.art1535-reserve__inner{position:relative;overflow:hidden;background:#17242b;color:#fff;border-radius:18px;padding:1.25rem 1.35rem;border:1px solid rgba(255,230,168,.28);box-shadow:0 10px 30px rgba(0,0,0,.08)}
    .art1535-reserve__inner:before{content:'1535';position:absolute;right:-.3rem;top:-1.4rem;font-size:6rem;font-weight:900;line-height:1;color:rgba(255,255,255,.045);pointer-events:none}.art1535-reserve__eyebrow{font-size:.75rem;font-weight:900;letter-spacing:.09em;color:#ffe6a8;margin:0 0 .35rem}.art1535-reserve h2{color:#fff;margin:.2rem 0 .6rem;font-size:clamp(1.35rem,2.5vw,2rem)}.art1535-reserve p{max-width:980px}.art1535-reserve__flow{background:rgba(255,255,255,.08);border-radius:12px;padding:.75rem .9rem;font-weight:750;margin:.8rem 0}.art1535-reserve__test{border-left:4px solid #ffe6a8;padding-left:.9rem}.art1535-reserve__limit{font-size:.91rem;color:#d8e1e5}.art1535-reserve a{display:inline-block;margin-top:.35rem;color:#17242b;background:#ffe6a8;border-radius:999px;padding:.55rem .9rem;font-weight:850;text-decoration:none}.art1535-reserve a:hover{text-decoration:underline}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.className = 'art1535-reserve';
  section.dataset.art1535ReservePathway = 'true';
  section.innerHTML = `<div class="art1535-reserve__inner"><p class="art1535-reserve__eyebrow">${copy.eyebrow}</p><h2>${copy.title}</h2><p>${copy.body}</p><div class="art1535-reserve__flow">${copy.flow}</div><p class="art1535-reserve__test">${copy.test}</p><p>${copy.trigger}</p><p class="art1535-reserve__limit">${copy.limit}</p><a href="${copy.href}">${copy.cta} →</a></div>`;

  const hero = document.querySelector('main > .dossier-hero, main > .hero, main > section.hero, main > .mhero');
  const thesis = document.querySelector('main [data-calificacion-misuse-thesis]');
  if ((thesis || hero)?.parentNode) (thesis || hero).insertAdjacentElement('afterend', section);
  else {
    const main = document.querySelector('main');
    if (main) main.insertBefore(section, main.firstChild);
  }
})();

// Global 360° reverse-engineering gateway loader. This reserve module is already loaded
// site-wide through the CAM pattern chain, so this keeps the new dependency analysis
// available without duplicating the assets/site.js loader graph.
(() => {
  const current = document.currentScript;
  if (!current || document.querySelector('script[data-reverse-engineering-360-loader]')) return;
  const script = document.createElement('script');
  script.src = new URL('reverse-engineering-360-20260819.js?v=20260819a', current.src).href;
  script.async = false;
  script.dataset.reverseEngineering360Loader = 'true';
  document.head.appendChild(script);
})();

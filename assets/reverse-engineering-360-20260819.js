(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const isEs = path.includes('/por-derecho/es/');
  const isEn = path.includes('/por-derecho/en/');
  if (!isEs && !isEn) return;

  const dedicated = path.includes('/ingenieria-inversa-360-cadena-sun-park/') || path.includes('/reverse-engineering-360-sun-park-chain/');
  if (dedicated) return;

  const relevant = [
    'articulo-1535','article-1535','retracto','credito-litigioso','litigious-credit','acreedor-de-registro','lender-of-record',
    'acosta-matos','concurso-36-2012','insolvency-36-2012','administrador-concursal','insolvency-administrator','insolvencia-lpb','lpb-insolvency',
    'recuperacion-restitucion','recovery-restitution','convergencia-venta-acreedor','sale-lender-convergence','matkator','extraconcursal',
    'comunidad','community','explotacion','exploitation','ricpe','ric-private-equity','fondos-incentivos','funding','mismo-hotel','same-hotel',
    'institutionalisation-chain','toma-control','takeover','hnt','mynd'
  ];
  if (!relevant.some(fragment => path.includes(fragment))) return;

  const id = 'reverse-engineering-360-gateway-20260819';
  if (document.getElementById(id)) return;

  const style = document.createElement('style');
  style.textContent = `
    #${id}{background:#eef3f4}
    #${id} .re360{max-width:1120px;margin:0 auto;background:#fff;border:1px solid rgba(19,37,45,.18);border-radius:18px;padding:1.1rem 1.25rem;box-shadow:0 10px 26px rgba(19,37,45,.07)}
    #${id} .re360-label{display:inline-block;background:#13252d;color:#fff;border-radius:999px;padding:.3rem .62rem;font-size:.73rem;font-weight:850;letter-spacing:.05em;text-transform:uppercase}
    #${id} h2{margin:.6rem 0;color:#13252d}
    #${id} .re360-rule{background:#fff8e8;border-left:5px solid #8c6b2f;border-radius:0 12px 12px 0;padding:.8rem 1rem;margin:.8rem 0}
    #${id} a.re360-cta{display:inline-block;background:#13252d;color:#fff;text-decoration:none;font-weight:800;border-radius:999px;padding:.58rem .86rem;margin-top:.35rem}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.id = id;
  section.className = 'section';
  if (isEs) {
    section.innerHTML = `<div class="shell"><div class="re360"><span class="re360-label">INGENIERÍA INVERSA 360°</span><h2>El presente no prueba el pasado.</h2><p>Este expediente forma parte de una cadena más amplia que se analiza en ambos sentidos: desde el estado actual de Sun Park/MYND hacia atrás, identificando cada puente jurídico y económico; y desde cada nodo histórico hacia delante, comprobando qué actos posteriores dependen realmente de él.</p><div class="re360-rule"><strong>Prueba de retirada:</strong> quite hipotéticamente el nodo controvertido. ¿Qué derechos posteriores sobreviven con un título independiente y cuáles dependían de ese puente? Para el art. 1535, la micro-regla es: <strong>no Día Nueve sin probar Día Cero.</strong></div><a class="re360-cta" href="/por-derecho/es/ingenieria-inversa-360-cadena-sun-park/">Abrir análisis unitario 360° →</a></div></div>`;
  } else {
    section.innerHTML = `<div class="shell"><div class="re360"><span class="re360-label">360° REVERSE ENGINEERING</span><h2>The present does not prove the past.</h2><p>This dossier sits inside a wider chain analysed in both directions: from today's Sun Park/MYND end-state backwards through each legal and economic bridge, and from each historical node forwards to test which later acts genuinely depend on it.</p><div class="re360-rule"><strong>Removal test:</strong> hypothetically take the contested node away. Which later rights survive on an independent title, and which depended on that bridge? For Article 1535, the micro-rule is: <strong>no Day Nine without proving Day Zero.</strong></div><a class="re360-cta" href="/por-derecho/en/reverse-engineering-360-sun-park-chain/">Open the unitary 360° analysis →</a></div></div>`;
  }

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector(':scope > .hero, :scope > section.hero, :scope > .dossier-hero, :scope > .cnmv-hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else main.insertAdjacentElement('afterbegin', section);
})();

// Global alleged criminal-engineering investigation loader. It is deliberately separate
// from the neutral 360° dependency gateway: the new layer states Por Derecho's allegation
// strongly while preserving actor-specific proof, the strongest defence and no-finding labels.
(() => {
  const current = document.currentScript;
  if (!current || document.querySelector('script[data-criminal-engineering-investigation-loader]')) return;
  const script = document.createElement('script');
  script.src = new URL('criminal-engineering-investigation-20260819.js?v=20260819a', current.src).href;
  script.async = false;
  script.dataset.criminalEngineeringInvestigationLoader = 'true';
  document.head.appendChild(script);
})();

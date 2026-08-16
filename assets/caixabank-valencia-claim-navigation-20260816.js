(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const routes = {
    en: [
      '/en/lender-of-record/',
      '/en/sale-lender-convergence/',
      '/en/lender-of-record/litigious-credit-hidden-deed/'
    ],
    es: [
      '/es/acreedor-de-registro/',
      '/es/convergencia-venta-acreedor/',
      '/es/acreedor-de-registro/credito-litigioso-escritura/'
    ]
  };
  const matches = (suffix) => path.endsWith(suffix);
  const isEn = routes.en.some(matches);
  const isEs = routes.es.some(matches);
  if (!isEn && !isEs) return;
  if (document.getElementById('valencia-banking-claim-chain-link')) return;

  const main = document.querySelector('main');
  const hero = main && main.querySelector('.hero, .dossier-hero');
  if (!main || !hero) return;

  const section = document.createElement('section');
  section.id = 'valencia-banking-claim-chain-link';
  section.className = 'section alt';
  section.innerHTML = isEn
    ? `<div class="shell"><div class="section-head"><div><p class="kicker">Connected recovery lane · Valencia</p><h2>The banking-liability claim now has its own evidence page</h2></div><p>Read it beside this lender / possession chain, not as a substitute for it.</p></div><article class="thesis-block"><p>The pending Valencia proceeding tests the historic banking and financial-product relationship. This chain separately tests later mortgage-credit ownership, enforcement, possession and title. A later assignment cannot retrospectively answer every earlier banking question, and the banking claim does not automatically decide every later creditor or possession issue.</p><p><strong>Current controlled distinction:</strong> the dedicated claim page identifies the present defendant and records the pleaded recovery, current trial date and the corrected origin of the Administrador Concursal witness evidence. The present lender-origin page may continue to describe the defendant generically because the legal identities and roles at different dates must not be collapsed.</p><p><a class="button" href="${path.includes('/lender-of-record/litigious-credit-hidden-deed/') ? '../../caixabank-valencia-claim/' : '../caixabank-valencia-claim/'}">Open the dedicated Valencia banking claim →</a></p></article></div>`
    : `<div class="shell"><div class="section-head"><div><p class="kicker">Vía de recuperación conectada · Valencia</p><h2>La reclamación bancaria ya tiene una página probatoria propia</h2></div><p>Debe leerse junto a esta cadena acreedor / posesión, no en sustitución de ella.</p></div><article class="thesis-block"><p>El procedimiento pendiente de Valencia examina la relación bancaria y del producto financiero históricos. Esta cadena examina por separado la titularidad posterior del crédito hipotecario, ejecución, posesión y título. Una cesión posterior no resuelve retrospectivamente todas las cuestiones bancarias anteriores, y la reclamación bancaria no decide automáticamente todos los episodios posteriores de acreedor o posesión.</p><p><strong>Distinción controlada actual:</strong> la página específica identifica a la demandada actual y recoge la recuperación reclamada, fecha de juicio vigente y el origen corregido de la testifical del Administrador Concursal. La página general de origen bancario puede seguir describiendo genéricamente a la demandada porque las identidades y funciones jurídicas en fechas distintas no deben confundirse.</p><p><a class="button" href="${path.includes('/acreedor-de-registro/credito-litigioso-escritura/') ? '../../reclamacion-caixabank-valencia/' : '../reclamacion-caixabank-valencia/'}">Abrir la reclamación bancaria de Valencia →</a></p></article></div>`;

  hero.insertAdjacentElement('afterend', section);
})();

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
    ? `<div class="shell"><div class="section-head"><div><p class="kicker">Connected recovery lane · Valencia</p><h2>The mortgage/swap package now has a full 360 evidence page</h2></div><p>Read it beside this lender / possession chain, not as a substitute for it.</p></div><article class="thesis-block"><p>The dedicated page reconstructs the €8.6m mortgage, €5m structured swap, 2010 novation/second mortgage, €405,000 pledge, account application and Bankia enforcement. It records the exact corporate lane <strong>Caja Insular → BFA → Bankia → CaixaBank</strong> and keeps the later mortgage-asset lane <strong>Bankia → SAREB → PH122 → CAM</strong> separate. Haya is a documented servicer/interlocutor, not a proved credit holder.</p><p><strong>Controlled liability rule:</strong> CaixaBank's universal succession to Bankia is documented, but underlying product liability, limitation, causation and quantum remain contested. A later assignment cannot retrospectively cure an earlier error; the pending banking claim does not automatically decide every later title or possession issue.</p><p><a class="button" href="${path.includes('/lender-of-record/litigious-credit-hidden-deed/') ? '../../caixabank-valencia-claim/' : '../caixabank-valencia-claim/'}">Open the dedicated Valencia banking claim →</a></p></article></div>`
    : `<div class="shell"><div class="section-head"><div><p class="kicker">Vía de recuperación conectada · Valencia</p><h2>El paquete hipoteca/swap ya tiene una página probatoria 360</h2></div><p>Debe leerse junto a esta cadena acreedor / posesión, no en sustitución de ella.</p></div><article class="thesis-block"><p>La página específica reconstruye la hipoteca de 8,6 M€, el swap estructurado de 5 M€, la novación/segunda hipoteca de 2010, la prenda de 405.000 €, la imputación de cuentas y la ejecución Bankia. Registra la cadena corporativa exacta <strong>Caja Insular → BFA → Bankia → CaixaBank</strong> y mantiene separada la cadena posterior del activo <strong>Bankia → SAREB → PH122 → CAM</strong>. Haya es servicer/interlocutor documentado, no titular probado.</p><p><strong>Regla controlada de responsabilidad:</strong> la sucesión universal de Bankia por CaixaBank está documentada, pero responsabilidad del producto, prescripción, causalidad y cuantía siguen controvertidas. Una cesión posterior no sana retrospectivamente un error anterior; la reclamación bancaria pendiente no decide automáticamente cada episodio posterior de título o posesión.</p><p><a class="button" href="${path.includes('/acreedor-de-registro/credito-litigioso-escritura/') ? '../../reclamacion-caixabank-valencia/' : '../reclamacion-caixabank-valencia/'}">Abrir la reclamación bancaria de Valencia →</a></p></article></div>`;

  hero.insertAdjacentElement('afterend', section);
})();

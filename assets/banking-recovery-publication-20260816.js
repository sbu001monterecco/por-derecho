(() => {
  const run = () => {
    const path = window.location.pathname;
    const es = path.endsWith('/es/acreedor-de-registro/') || path.endsWith('/es/acreedor-de-registro/index.html');
    const en = path.endsWith('/en/lender-of-record/') || path.endsWith('/en/lender-of-record/index.html');
    if (!es && !en) return;
    if (document.querySelector('[data-banking-recovery-publication="art1535"]')) return;

    const main = document.querySelector('main');
    if (!main) return;
    const firstSection = main.querySelector('.section');
    if (!firstSection) return;

    const section = document.createElement('section');
    section.className = 'section alt';
    section.dataset.bankingRecoveryPublication = 'art1535';
    const href = es ? 'credito-litigioso-escritura/' : 'litigious-credit-hidden-deed/';
    section.innerHTML = es
      ? `<div class="shell"><article class="thesis-block"><p class="kicker">Expediente específico · cesión 20 octubre 2017</p><h2>PH122 → Construcciones Acosta Matos: escritura, precio, cuantía y artículo 1535</h2><p>La documentación primaria permite separar la controversia cuantificada previa a la cesión, el requerimiento posterior de escritura y precio, la diligencia preliminar admitida el 19 de diciembre de 2017 y el Auto adverso de 8 de febrero de 2018 que rechazó la tesis de crédito litigioso pero limitó la sustitución al cambio de titular sin alterar cuantías.</p><p><strong>La cuestión técnica del artículo 1535 permanece abierta a la prueba procesal exacta anterior a la cesión.</strong></p><p><a class="button" href="${href}">Abrir el expediente de cesión y art. 1535 →</a></p></article></div>`
      : `<div class="shell"><article class="thesis-block"><p class="kicker">Specific record · 20 October 2017 assignment</p><h2>PH122 → Construcciones Acosta Matos: deed, price, amount and Article 1535</h2><p>The primary record now separates the quantified pre-assignment dispute, the later demand for the deed and price, the preliminary measure allowed on 19 December 2017, and the adverse 8 February 2018 order rejecting the litigious-credit theory while limiting substitution to a change of creditor without changing recognised amounts.</p><p><strong>The technical Article 1535 question remains open to the exact pre-assignment procedural record.</strong></p><p><a class="button" href="${href}">Open the assignment and Article 1535 record →</a></p></article></div>`;
    firstSection.parentNode.insertBefore(section, firstSection);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
})();

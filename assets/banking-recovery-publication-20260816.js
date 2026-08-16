(() => {
  const run = () => {
    const path = window.location.pathname;
    const es = path.endsWith('/es/acreedor-de-registro/') || path.endsWith('/es/acreedor-de-registro/index.html');
    const en = path.endsWith('/en/lender-of-record/') || path.endsWith('/en/lender-of-record/index.html');
    if (!es && !en) return;
    if (document.querySelector('[data-banking-recovery-publication="gateway"]')) return;

    const main = document.querySelector('main');
    if (!main) return;
    const firstSection = main.querySelector('.section');
    if (!firstSection) return;

    const section = document.createElement('section');
    section.className = 'section alt';
    section.dataset.bankingRecoveryPublication = 'gateway';
    section.innerHTML = es
      ? `<div class="shell"><div class="section-head"><div><p class="kicker">Expedientes específicos · publicación 16 agosto 2026</p><h2>Tres rutas para no confundir insolvencia, convergencia y cesión de crédito</h2></div><p>El expediente bancario principal conserva la cronología completa. Estas páginas separan tres cuestiones que requieren pruebas y límites propios.</p></div><div class="grid-3"><article class="path-card primary"><h3>Insolvencia LPB*</h3><p>Qué sociedad entró en Concurso 36/2012, por qué el asterisco importa, la corrección de 158 fincas y por qué superávit patrimonial no equivale automáticamente a ausencia de insolvencia de tesorería.</p><p><a class="button" href="../insolvencia-lpb/">Abrir Insolvencia LPB* →</a></p></article><article class="path-card"><h3>Venta + acreedor: convergencia</h3><p>Cómo propiedad, financiación, explotación, ejecución y concurso convergieron alrededor del mismo hotel sin convertirse en un solo perímetro jurídico o una responsabilidad colectiva.</p><p><a class="button" href="../convergencia-venta-acreedor/">Abrir convergencia →</a></p></article><article class="path-card"><h3>PH122 → CAM / art. 1535</h3><p>Escritura, precio, cuantía, diligencia preliminar de 2017 y Auto adverso de febrero de 2018. La cuestión técnica del art. 1535 permanece abierta a la prueba procesal exacta.</p><p><a class="button" href="credito-litigioso-escritura/">Abrir cesión y art. 1535 →</a></p></article></div></div>`
      : `<div class="shell"><div class="section-head"><div><p class="kicker">Specific records · published 16 August 2026</p><h2>Three routes to keep insolvency, convergence and credit assignment separate</h2></div><p>The main banking record preserves the full chronology. These pages separate three questions requiring their own evidence and limits.</p></div><div class="grid-3"><article class="path-card primary"><h3>LPB Insolvency*</h3><p>Which company entered Insolvency 36/2012, why the asterisk matters, the 158-property correction and why an asset surplus does not automatically exclude cash-flow insolvency.</p><p><a class="button" href="../lpb-insolvency/">Open LPB Insolvency* →</a></p></article><article class="path-card"><h3>Sale + lender convergence</h3><p>How property, finance, operation, enforcement and insolvency converged around the same hotel without becoming one legal perimeter or collective responsibility.</p><p><a class="button" href="../sale-lender-convergence/">Open convergence →</a></p></article><article class="path-card"><h3>PH122 → CAM / Article 1535</h3><p>Deed, price, amount, the 2017 preliminary measure and the adverse February 2018 order. The technical Article 1535 question remains open to the exact procedural record.</p><p><a class="button" href="litigious-credit-hidden-deed/">Open assignment and Article 1535 →</a></p></article></div></div>`;
    firstSection.parentNode.insertBefore(section, firstSection);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
})();

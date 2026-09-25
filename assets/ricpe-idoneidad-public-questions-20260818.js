(() => {
  const path = window.location.pathname.replace(/\/+$/, '/') || '/';
  const esPage = '/por-derecho/es/ricpe-idoneidad-series-f-g/';
  const enPage = '/por-derecho/en/ricpe-idoneidad-series-f-g/';
  const relevant = new Set([
    '/por-derecho/es/ric-private-equity-sun-park/',
    '/por-derecho/en/ric-private-equity-sun-park/',
    '/por-derecho/es/ricpe-responsabilidad-documental/',
    '/por-derecho/en/ricpe-documentary-accountability/',
    '/por-derecho/es/cadena-instrumentalizacion-ric-fondos-incentivos/',
    '/por-derecho/en/institutionalisation-chain-ric-eu-incentives/',
    '/por-derecho/es/mismo-hotel-multiples-vidas-financieras/',
    '/por-derecho/en/same-hotel-multiple-financial-lives/',
    '/por-derecho/es/cnmv-ricpe-verificacion/',
    '/por-derecho/en/cnmv-ricpe-verification/',
    '/por-derecho/es/actualizaciones/',
    '/por-derecho/en/updates/'
  ]);

  const isEnglish = path.includes('/en/');
  const href = isEnglish ? enPage : esPage;

  const escapeHtml = (value) => String(value).replace(/[&<>'"]/g, (ch) => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]));

  const patchStaleRenderedText = () => {
    if (!path.includes('/cadena-instrumentalizacion-ric-fondos-incentivos/')) return;
    const oldText = 'El expediente controlado atribuye €6.573.703,10 total Series F/G a cuentas auditadas 2023; el desglose exacto permanece abierto.';
    const newText = 'Las cuentas auditadas 2023 permiten ya desglosar €6.573.703,10: Serie F — Hotel MYND Yaiza, €1.598.849,32; Serie G — MYND Yaiza Creación de empleo, €4.974.853,78. Lo abierto es el alcance exacto de la autorización y el uso/documentación subyacente de cada fase.';
    document.querySelectorAll('p').forEach((p) => {
      if (p.textContent.trim() === oldText) p.textContent = newText;
    });
  };

  const buildPanel = () => {
    const section = document.createElement('section');
    section.className = 'section ricpe-idoneidad-public-question';
    section.dataset.publicQuestion = 'ricpe-idoneidad-series-f-g-20260818';
    section.style.background = '#f4f1ea';
    section.style.borderTop = '6px solid #8c2f2c';
    section.style.borderBottom = '1px solid rgba(19,37,45,.12)';

    if (isEnglish) {
      section.innerHTML = `
        <div class="shell" style="max-width:1180px">
          <p class="eyebrow">OPEN DOCUMENTARY QUESTION · 18 AUGUST 2026</p>
          <h2 style="max-width:29ch">€1.598m Series F for the hotel project; €4.975m Series G for employment. Which authorisation covered which phase — and what did the first money actually finance?</h2>
          <p style="max-width:84ch"><strong>Documented accounting position:</strong> RICPE's audited 2023 accounts distinguish Series F — Hotel MYND Yaiza (€1,598,849.32) from Series G — MYND Yaiza Employment Creation (€4,974,853.78). They also report the Government of the Canary Islands idoneidad on 1 December 2022, reform financing in 2022 and hotel opening on 16 December 2022. This is a reconciliation question, not a finding of illegality.</p>
          <p style="max-width:84ch"><strong>The public-file question:</strong> did Decree 224/2022 and the AEAT binding report of 17 November 2022 expressly cover Series F, Series G, or both? If the first €1.598m financed refurbishment when the hotel was already at the point of opening after reform/transformation, which invoices, liabilities, prior eligible expenditure or bridge financing did it finance, and under which rule?</p>
          <div class="actions"><a class="button" href="${escapeHtml(href)}">Open the authority-by-authority question ledger →</a></div>
          <p style="font-size:.88rem;max-width:90ch"><strong>Right of reply:</strong> any authority, RICPE, CAM, HNT or other source able to supply the application, decree, AEAT report, amendments, loan documents, invoices or an alternative reconciliation is invited to do so. Verified corrections will be published with equivalent prominence.</p>
        </div>`;
    } else {
      section.innerHTML = `
        <div class="shell" style="max-width:1180px">
          <p class="eyebrow">CUESTIÓN DOCUMENTAL ABIERTA · 18 AGOSTO 2026</p>
          <h2 style="max-width:29ch">Serie F: 1,598 M€ para el proyecto hotelero. Serie G: 4,975 M€ para empleo. ¿Qué autorización cubrió cada fase y qué financió realmente el primer dinero?</h2>
          <p style="max-width:84ch"><strong>Posición contable documentada:</strong> las cuentas auditadas 2023 de RICPE distinguen la Serie F — Hotel MYND Yaiza (1.598.849,32 €) de la Serie G — MYND Yaiza Creación de empleo (4.974.853,78 €). También refieren idoneidad del Gobierno de Canarias el 1 de diciembre de 2022, financiación de reforma en 2022 y apertura del hotel el 16 de diciembre de 2022. Es una cuestión de conciliación documental, no una declaración de ilegalidad.</p>
          <p style="max-width:84ch"><strong>La pregunta del expediente público:</strong> ¿el Decreto 224/2022 y el informe vinculante AEAT de 17 de noviembre de 2022 amparaban expresamente la Serie F, la Serie G o ambas? Si los primeros 1,598 M€ financiaron reforma cuando el hotel ya estaba en el punto de apertura tras su reforma/transformación, ¿qué facturas, obligaciones, gasto elegible previo o financiación puente financiaron y bajo qué regla?</p>
          <div class="actions"><a class="button" href="${escapeHtml(href)}">Abrir el registro de preguntas por autoridad →</a></div>
          <p style="font-size:.88rem;max-width:90ch"><strong>Derecho de respuesta:</strong> cualquier autoridad, RICPE, CAM, HNT u otra fuente que pueda aportar la solicitud, decreto, informe AEAT, modificaciones, préstamos, facturas o una conciliación alternativa está invitada a hacerlo. Las correcciones verificadas se publicarán con relevancia equivalente.</p>
        </div>`;
    }
    return section;
  };

  const inject = () => {
    patchStaleRenderedText();
    if (!relevant.has(path) || document.querySelector('[data-public-question="ricpe-idoneidad-series-f-g-20260818"]')) return;
    const panel = buildPanel();
    const hero = document.querySelector('main > .hero, main > .dossier-hero, main > section:first-child');
    if (hero && hero.parentNode) hero.insertAdjacentElement('afterend', panel);
    else (document.querySelector('main') || document.body).prepend(panel);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject, { once: true });
  else inject();
})();

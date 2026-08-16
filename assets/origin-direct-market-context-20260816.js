(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const isEnglish = path.endsWith('/en/community-instrumentalisation/');
  const isSpanish = path.endsWith('/es/comunidad-instrumentalizacion/');
  if (!isEnglish && !isSpanish) return;
  if (document.getElementById('banking-origin-direct-market-context')) return;

  const hero = document.querySelector('main .hero');
  if (!hero) return;

  const section = document.createElement('section');
  section.className = 'section alt';
  section.id = 'banking-origin-direct-market-context';

  section.innerHTML = isEnglish
    ? `
      <div class="shell">
        <div class="section-head">
          <div>
            <p class="kicker">Origin and trading context</p>
            <h2>The Community dispute did not occur inside a vacuum</h2>
          </div>
          <p>The controlled record now connects the owner-conflict track to the disputed 2011–2012 banking premise, the defensive LPB filing and Aweswell's direct-to-market response.</p>
        </div>
        <article class="thesis-block">
          <p><strong>Separate legal perimeters:</strong> LPB was the debtor in Concurso 36/2012. Matkator was not. The Comunidad de Explotación del Complejo Sun Park was a separate operating structure and was not automatically placed under the insolvency administrator or court merely because LPB entered insolvency.</p>
          <p><strong>Trading consequence alleged:</strong> the Monte Lanza/Molina minority-dissident perimeter materially disrupted unitary hotel operation and contributed to difficulty maintaining conventional tour-operator distribution. Contemporaneous business records independently confirm that Gil Marer and the Aweswell management team built direct reservations, repeat-customer marketing, call handling, sales reporting, booking and payment systems and external-operator relationships.</p>
          <p><strong>Causation discipline:</strong> the records prove the direct-market platform existed. They do not yet prove that every operator decision resulted solely from the internal dispute. Any responsibility of the insolvency administrator or court for extraconcursal harm must be traced through specific acts, omissions, authorisations, knowledge and available corrective powers—not assumed from a general concursal mandate.</p>
        </article>
        <p class="source-policy"><a href="../lender-of-record/">Read the banking-origin and lender-of-record chapter</a>, including the 2012 enforcement and auction trigger, the current anonymised Valencia proceeding and the distinction between the banking claim and the concursal accounting reconciliation.</p>
      </div>`
    : `
      <div class="shell">
        <div class="section-head">
          <div>
            <p class="kicker">Contexto de origen y explotación</p>
            <h2>El conflicto comunitario no ocurrió de forma aislada</h2>
          </div>
          <p>El expediente controlado conecta ahora la vía del conflicto entre propietarios con la premisa bancaria discutida de 2011–2012, el concurso defensivo de LPB y la respuesta directa al mercado de Aweswell.</p>
        </div>
        <article class="thesis-block">
          <p><strong>Perímetros jurídicos separados:</strong> LPB era la deudora en el Concurso 36/2012. Matkator no lo era. La Comunidad de Explotación del Complejo Sun Park era una estructura operativa separada y no quedó automáticamente sometida a la administración concursal o al juzgado por el solo hecho de que LPB entrara en concurso.</p>
          <p><strong>Consecuencia comercial alegada:</strong> el perímetro minoritario disidente Monte Lanza/Molina alteró materialmente la explotación unitaria del hotel y contribuyó a dificultar la distribución convencional mediante turoperadores. Los registros empresariales contemporáneos confirman de forma independiente que Gil Marer y el equipo de Aweswell desarrollaron reservas directas, marketing de repetición, atención de llamadas, informes de ventas, sistemas de reserva y pago y relaciones con operadores externos.</p>
          <p><strong>Disciplina causal:</strong> los registros prueban que existía una plataforma directa al mercado. Todavía no prueban que cada decisión de un operador se debiera exclusivamente al conflicto interno. Cualquier responsabilidad de la administración concursal o del juzgado por daño extraconcursal debe vincularse a actos, omisiones, autorizaciones, conocimiento y facultades correctoras concretas, y no presumirse de un mandato concursal general.</p>
        </article>
        <p class="source-policy"><a href="../acreedor-de-registro/">Consultar el capítulo sobre origen bancario y acreedor de registro</a>, incluido el detonante de ejecución y subasta de 2012, el procedimiento actual de Valencia anonimizado y la distinción entre la reclamación bancaria y la conciliación contable concursal.</p>
      </div>`;

  hero.insertAdjacentElement('afterend', section);
})();

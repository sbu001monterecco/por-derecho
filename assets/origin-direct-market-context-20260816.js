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
          <p>Primary records now connect the owner-conflict track to a February-2012 restructuring plan, the 158-property auction schedule, the defensive LPB filing and a direct-market business already under development before the concurso.</p>
        </div>
        <article class="thesis-block">
          <p><strong>Separate legal perimeters:</strong> LPB was the debtor in Concurso 36/2012. Matkator was not. The Comunidad de Explotación del Complejo Sun Park was a separate operating structure and was not automatically placed under the insolvency administrator or court merely because LPB entered insolvency.</p>
          <p><strong>Documented trading architecture:</strong> the 28-February-2012 viability plan describes Summers Villages, Sun Park Living and a proposed tour-operator lane. Later records independently support direct reservations, repeat-customer marketing, call handling, sales reporting, booking and payment systems and external-operator negotiations.</p>
          <p><strong>Trading consequence alleged:</strong> the Monte Lanza/Molina minority-dissident perimeter materially disrupted unitary operation and contributed to conventional-distribution difficulty. The records establish that a direct-market platform existed; they do not yet prove that every operator decision resulted solely from the internal dispute.</p>
          <p><strong>Institutional boundary:</strong> any responsibility of the insolvency administrator or court for extraconcursal harm must be traced through specific acts, omissions, authorisations, notice, legal capacity and available corrective powers—not assumed from a general concursal mandate.</p>
        </article>
        <p class="source-policy"><a href="../lender-of-record/">Read the corrected banking-origin chapter</a>, including the primary 158-property auction schedule, the acquisition and registry chronology, the current anonymised Valencia proceeding and the distinction between banking liability and concursal accounting.</p>
      </div>`
    : `
      <div class="shell">
        <div class="section-head">
          <div>
            <p class="kicker">Contexto de origen y explotación</p>
            <h2>El conflicto comunitario no ocurrió de forma aislada</h2>
          </div>
          <p>Los documentos primarios conectan ahora el conflicto de propietarios con un plan de reestructuración de febrero de 2012, la subasta de 158 fincas, el concurso defensivo de LPB y una actividad directa al mercado ya en desarrollo antes del concurso.</p>
        </div>
        <article class="thesis-block">
          <p><strong>Perímetros jurídicos separados:</strong> LPB era la deudora en el Concurso 36/2012. Matkator no lo era. La Comunidad de Explotación del Complejo Sun Park era una estructura operativa separada y no quedó automáticamente sometida a la administración concursal o al juzgado por el solo hecho de que LPB entrara en concurso.</p>
          <p><strong>Arquitectura comercial documentada:</strong> el plan de viabilidad de 28 de febrero de 2012 describe Summers Villages, Sun Park Living y una vía proyectada con turoperadores. Registros posteriores respaldan reservas directas, marketing de repetición, atención telefónica, informes de ventas, sistemas de reserva y pago y negociaciones con operadores externos.</p>
          <p><strong>Consecuencia comercial alegada:</strong> el perímetro minoritario disidente Monte Lanza/Molina alteró materialmente la explotación unitaria y contribuyó a dificultar la distribución convencional. Los documentos acreditan que existía una plataforma directa; todavía no prueban que cada decisión de un operador se debiera exclusivamente al conflicto interno.</p>
          <p><strong>Límite institucional:</strong> cualquier responsabilidad de la administración concursal o del juzgado por daño extraconcursal debe vincularse a actos, omisiones, autorizaciones, conocimiento, capacidad jurídica y facultades correctoras concretas, no presumirse de un mandato concursal general.</p>
        </article>
        <p class="source-policy"><a href="../acreedor-de-registro/">Consultar el capítulo bancario corregido</a>, incluida la subasta primaria de 158 fincas, la cronología de adquisición e inscripción, el procedimiento actual de Valencia anonimizado y la distinción entre responsabilidad bancaria y contabilidad concursal.</p>
      </div>`;

  hero.insertAdjacentElement('afterend', section);
})();

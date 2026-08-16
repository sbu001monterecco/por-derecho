(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const isEnglish = path.endsWith('/en/community-instrumentalisation/');
  const isSpanish = path.endsWith('/es/comunidad-instrumentalizacion/');
  if (!isEnglish && !isSpanish) return;
  if (document.getElementById('banking-origin-direct-market-context')) return;

  const hero = document.querySelector('main .hero, main .dossier-hero');
  if (!hero) return;

  const section = document.createElement('section');
  section.className = 'section alt';
  section.id = 'banking-origin-direct-market-context';

  section.innerHTML = isEnglish
    ? `
      <div class="shell">
        <div class="section-head">
          <div>
            <p class="kicker">Origin, trading and legal-perimeter context</p>
            <h2>The Community dispute did not occur inside the LPB insolvency estate</h2>
          </div>
          <p>Primary records connect the owner-conflict track to a February-2012 restructuring plan, the 158-property auction schedule, the defensive LPB filing and a direct-to-market business already under development before the concurso.</p>
        </div>
        <article class="thesis-block">
          <p><strong>Separate legal perimeters:</strong> LPB was the debtor in Concurso 36/2012. Matkator was not. The Comunidad de Explotación del Complejo Sun Park was a separate operating structure and did not automatically fall under the insolvency administrator or court merely because LPB entered insolvency.</p>
          <p><strong>Documented trading architecture:</strong> the 28-February-2012 viability plan describes Summers Villages, Sun Park Living and a proposed tour-operator lane. Later records independently support direct reservations, repeat-customer marketing, call handling, sales reporting, booking and payment systems, customer reactivation and external-operator negotiations. That evidence supports a real direct-to-market response intended to reduce dependence on conventional intermediaries while the hotel faced internal operating and ownership friction.</p>
          <p><strong>Minority conflict and commercial effect:</strong> contemporaneous proceedings and later records establish a genuine dispute around minority owners, unitary exploitation, possession and operating control. The case advanced by Gil Marer and related parties is that the Monte Lanza/Molina perimeter materially aggravated normal hotel trading and conventional distribution. The evidence presently supports the existence of the conflict and the direct-market adaptation; it does not yet prove that every tour-operator decision, lost booking or item of loss was caused solely by that perimeter.</p>
          <p><strong>Practical effect is not the same as legal perimeter:</strong> the fact that Matkator and the Comunidad were outside LPB's insolvency estate does not mean concursal decisions could never affect them in practice. The question is whether a specific authorisation, procedural decision, omission or failure to correct known conduct produced an identifiable extraconcursal effect. That chain must be proved actor by actor.</p>
          <p><strong>Institutional-accountability question:</strong> the record therefore has to test both affirmative acts and legally material inaction by the insolvency administrator, court and other office-holders where they had notice and a relevant power. It should not convert that investigation into a finding of collusion, bad faith or unlawful enabling without the specific duty, knowledge, act or omission, capacity, causation and available remedy being shown.</p>
        </article>
        <p class="source-policy"><a href="../lender-of-record/">Read the corrected banking-origin chapter</a>, including the primary 158-property auction schedule, the acquisition and registry chronology, the current anonymised Valencia proceeding and the distinction between banking liability, concursal accounting and extraconcursal effect.</p>
      </div>`
    : `
      <div class="shell">
        <div class="section-head">
          <div>
            <p class="kicker">Contexto de origen, explotación y perímetro jurídico</p>
            <h2>El conflicto de la Comunidad no ocurrió dentro de la masa concursal de LPB</h2>
          </div>
          <p>Los documentos primarios conectan el conflicto de propietarios con un plan de reestructuración de febrero de 2012, la subasta de 158 fincas, el concurso defensivo de LPB y una actividad directa al mercado ya en desarrollo antes del concurso.</p>
        </div>
        <article class="thesis-block">
          <p><strong>Perímetros jurídicos separados:</strong> LPB era la deudora en el Concurso 36/2012. Matkator no lo era. La Comunidad de Explotación del Complejo Sun Park era una estructura operativa separada y no quedó automáticamente sometida a la administración concursal o al juzgado por el solo hecho de que LPB entrara en concurso.</p>
          <p><strong>Arquitectura comercial documentada:</strong> el plan de viabilidad de 28 de febrero de 2012 describe Summers Villages, Sun Park Living y una vía proyectada con turoperadores. Registros posteriores respaldan reservas directas, marketing de repetición, atención telefónica, informes de ventas, sistemas de reserva y pago, reactivación de clientes y negociaciones con operadores externos. Esa prueba respalda una respuesta real «directa al mercado» destinada a reducir la dependencia de intermediarios convencionales mientras el hotel afrontaba fricción interna de explotación y propiedad.</p>
          <p><strong>Conflicto minoritario y efecto comercial:</strong> procedimientos contemporáneos y registros posteriores acreditan la existencia de un conflicto real en torno a propietarios minoritarios, unidad de explotación, posesión y control operativo. La tesis sostenida por Gil Marer y partes relacionadas es que el perímetro Monte Lanza/Molina agravó materialmente la explotación normal y la distribución convencional. La prueba disponible respalda la existencia del conflicto y la adaptación comercial directa; todavía no demuestra que cada decisión de un turoperador, reserva perdida o partida de daño se debiera exclusivamente a ese perímetro.</p>
          <p><strong>Efecto práctico no equivale a perímetro jurídico:</strong> que Matkator y la Comunidad estuvieran fuera de la masa de LPB no significa que decisiones concursales nunca pudieran afectarles en la práctica. La cuestión es si una autorización, decisión procesal, omisión o falta de corrección concreta produjo un efecto extraconcursal identificable. Esa cadena debe probarse actor por actor.</p>
          <p><strong>Pregunta de responsabilidad institucional:</strong> el expediente debe examinar tanto actos positivos como inacciones jurídicamente relevantes de la administración concursal, el juzgado y otros responsables cuando existían conocimiento y facultades pertinentes. Esa investigación no debe convertirse en una conclusión de colusión, mala fe o favorecimiento ilícito sin acreditar el deber, conocimiento, acto u omisión, capacidad, causalidad y remedio disponible concretos.</p>
        </article>
        <p class="source-policy"><a href="../acreedor-de-registro/">Consultar el capítulo bancario corregido</a>, incluida la subasta primaria de 158 fincas, la cronología de adquisición e inscripción, el procedimiento actual de Valencia anonimizado y la distinción entre responsabilidad bancaria, contabilidad concursal y efecto extraconcursal.</p>
      </div>`;

  hero.insertAdjacentElement('afterend', section);
})();

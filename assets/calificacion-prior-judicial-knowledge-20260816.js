(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const esPath = '/por-derecho/es/calificacion-concurso-36-2012-vidas-paralelas/';
  const enPath = '/por-derecho/en/insolvency-classification-parallel-lives/';
  const isEs = path === esPath;
  const isEn = path === enPath;
  if (!isEs && !isEn) return;
  if (document.getElementById('prior-judicial-knowledge-rescue-link')) return;

  const hero = document.querySelector('main .hero');
  if (!hero) return;

  const section = document.createElement('section');
  section.id = 'prior-judicial-knowledge-rescue-link';
  section.className = 'section alt';

  if (isEs) {
    section.innerHTML = `
      <div class="shell record">
        <p class="eyebrow">NUEVA CAPA PROBATORIA · QUÉ SABÍA EL JUZGADO</p>
        <h2>Antes de la Sentencia 163/2023 ya existía un historial documentado de rescate, viabilidad, pago y defensa de LPB</h2>
        <p>Un acuse LexNET prueba que el 27 de abril de 2017 entraron en el Concurso 36/2012 una propuesta de convenio, un plan de viabilidad y un plan de pagos. Un correo profesional enviado la misma noche del 13 de junio de 2018 relata además que el juez fue informado personalmente de una vía financiada para pagar la deuda concursal, coordinar un fondo y una cadena hotelera, recuperar la autonomía de LPB y defender sus intereses frente a actores privados.</p>
        <p>La prueba contemporánea de ONA, reforma y financiación hace que esa estrategia sea comercialmente concreta. La cuestión relevante para la calificación no es afirmar que todo intento de rescate elimina cualquier posible incumplimiento, sino comprobar cada fundamento adverso contra lo que el órgano judicial ya había recibido y lo que el juez había sido informado personalmente.</p>
        <p><strong>Esta capa no declara probado ningún delito.</strong> Separa conocimiento previo, inferencia y los elementos penales que tendrían que acreditarse de forma independiente.</p>
        <p class="linkrow"><a class="button" href="./conocimiento-previo-rescate/">Ver la cronología y matriz probatoria completa →</a></p>
      </div>`;
  } else {
    section.innerHTML = `
      <div class="shell record">
        <p class="eyebrow">NEW EVIDENCE LAYER · WHAT THE COURT KNEW</p>
        <h2>Before Judgment 163/2023 there was already a documented LPB rescue, viability, payment and defence history</h2>
        <p>A LexNET acknowledgement proves that on 27 April 2017 a composition proposal, viability plan and payment plan entered Insolvency 36/2012. A professional email sent on the night of 13 June 2018 further records that the judge was personally informed of a financed route to pay the insolvency debt, coordinate a fund and hotel chain, restore LPB's autonomy and defend its interests against private actors.</p>
        <p>Contemporaneous ONA, refurbishment and financing evidence makes that strategy commercially concrete. The point for the classification is not that every rescue attempt automatically defeats every possible breach, but that each adverse ground must be tested against what the court had already received and what the judge had reportedly been told personally.</p>
        <p><strong>This evidence layer does not declare any criminal offence proved.</strong> It separates prior knowledge, inference and the criminal elements that would require independent proof.</p>
        <p class="linkrow"><a class="button" href="./prior-judicial-knowledge-rescue/">See the full chronology and evidence matrix →</a></p>
      </div>`;
  }

  hero.insertAdjacentElement('afterend', section);
})();

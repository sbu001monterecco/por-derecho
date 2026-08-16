(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const es = path.includes('/por-derecho/es/');
  const en = path.includes('/por-derecho/en/');
  if (!es && !en) return;

  const calEs = '/por-derecho/es/calificacion-concurso-36-2012-vidas-paralelas/';
  const calEn = '/por-derecho/en/insolvency-classification-parallel-lives/';
  const updateEs = '/por-derecho/es/actualizaciones/';
  const updateEn = '/por-derecho/en/updates/';
  const related = new Set([
    calEs,
    calEn,
    '/por-derecho/es/comunidad-instrumentalizacion/',
    '/por-derecho/en/community-instrumentalisation/',
    '/por-derecho/es/toma-control-sun-park-7-junio-2018/',
    '/por-derecho/en/sun-park-takeover-7-june-2018/',
    '/por-derecho/es/convergencia-venta-acreedor/',
    '/por-derecho/en/sale-lender-convergence/',
    '/por-derecho/es/reclamacion-caixabank-valencia/',
    '/por-derecho/en/caixabank-valencia-claim/',
    '/por-derecho/es/concurso-36-2012-responsabilidad-institucional/',
    '/por-derecho/en/insolvency-36-2012-institutional-accountability/',
    '/por-derecho/es/cuaderno-juridico/control-judicial-prevaricacion/',
    '/por-derecho/en/legal-notebook/judicial-control-prevaricacion/'
  ]);

  if (!related.has(path) && path !== updateEs && path !== updateEn) return;
  if (document.getElementById('cal-fiscal-chain-2012-2019-2026')) return;

  const style = document.createElement('style');
  style.textContent = `
    .cf-chain{border-top:1px solid rgba(19,37,45,.14)}
    .cf-chain .cf-intro{max-width:900px}
    .cf-chain-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;margin:1.2rem 0}
    .cf-chain-card{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:16px;padding:1.05rem 1.1rem;border-top:5px solid #6b5841}
    .cf-chain-card strong.cf-date{display:block;font-size:.76rem;letter-spacing:.07em;text-transform:uppercase;color:#6b5841;margin-bottom:.4rem}
    .cf-chain-card h3{margin:.2rem 0 .55rem;font-size:1.08rem}
    .cf-chain-lock{background:#13252d;color:#fff;border-radius:17px;padding:1.15rem 1.3rem;margin:1.1rem 0}
    .cf-chain-lock a{color:#fff;text-decoration:underline}
    .cf-chain-links{display:flex;flex-wrap:wrap;gap:.55rem;margin-top:.9rem}
    .cf-chain-links a{display:inline-block;border:1px solid rgba(19,37,45,.24);border-radius:999px;padding:.42rem .7rem;text-decoration:none}
    .cf-update{background:#f3efe4;border-left:5px solid #8c6b2f;border-radius:14px;padding:1.15rem 1.25rem;margin:1.5rem 0}
    @media(max-width:860px){.cf-chain-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.id = 'cal-fiscal-chain-2012-2019-2026';
  section.className = 'section alt cf-chain';

  const isCal = path === calEs || path === calEn;
  const isUpdate = path === updateEs || path === updateEn;

  if (isUpdate) {
    section.innerHTML = es ? `
      <div class="shell record">
        <div class="cf-update">
          <p class="eyebrow">16 AGO 2026 · ACTUALIZACIÓN DOCUMENTAL</p>
          <h2>Calificación: nuevo puente documental 2012 → 2019 → 2026</h2>
          <p>Se incorpora una nueva capa probatoria que conecta el litigio de propietarios minoritarios anterior al concurso, las objeciones contemporáneas de 2019 sobre la realización separada de activos vinculados y las denuncias presentadas ante Fiscalía en enero–febrero de 2026. El punto más fuerte no es una acusación posterior: el escrito de 13 de mayo de 2019 reproduce el lenguaje del propio Plan/AC describiendo la propuesta como adquisición <strong>unitaria de la unidad productiva</strong> y las fincas comunes/vinculadas como no explotables comercialmente de forma independiente.</p>
          <p><strong>Control:</strong> las denuncias penales son alegaciones y solicitudes de investigación, no declaraciones de delito ni de responsabilidad. La referencia de un escrito de 8 de febrero a un decreto de Fiscalía de Tenerife de 27 de enero permanece pendiente de verificación mediante el decreto firmado.</p>
          <p><a href="../calificacion-concurso-36-2012-vidas-paralelas/#puente-2012-2019-2026">Ver la actualización en la página de Calificación →</a></p>
        </div>
      </div>` : `
      <div class="shell record">
        <div class="cf-update">
          <p class="eyebrow">16 AUG 2026 · DOCUMENTARY UPDATE</p>
          <h2>Classification: new 2012 → 2019 → 2026 documentary bridge</h2>
          <p>A new evidence layer connects pre-insolvency minority-owner litigation, the contemporaneous 2019 objections to separate disposal of linked assets, and criminal complaints submitted to prosecutors in January–February 2026. The strongest point is not a later accusation: the 13 May 2019 filing reproduces the Plan/IA's own description of the proposal as a <strong>unitary acquisition of the production unit</strong> and of the linked/common properties as lacking independent commercial exploitation.</p>
          <p><strong>Control:</strong> criminal complaints are allegations and requests for investigation, not findings of an offence or responsibility. An 8 February filing's reference to a 27 January Tenerife prosecution decree remains pending verification from the signed decree.</p>
          <p><a href="../insolvency-classification-parallel-lives/#puente-2012-2019-2026">See the update on the Classification page →</a></p>
        </div>
      </div>`;
  } else if (isCal) {
    section.innerHTML = es ? `
      <div class="shell record" id="puente-2012-2019-2026">
        <p class="eyebrow">NUEVO PUENTE DOCUMENTAL · 2012 → 2019 → 2026</p>
        <h2>La calificación no puede leerse como si el conflicto operativo, la unidad económica del hotel y las objeciones a la liquidación hubieran aparecido después</h2>
        <p class="cf-intro">Un nuevo paquete de fuentes añade tres capas cronológicas distintas. Juntas no prueban una instrumentalización penal de la calificación; sí obligan a contrastar cualquier relato causal del concurso con un conflicto propietario–operador anterior a junio de 2012, con el lenguaje unitario de la propia arquitectura de liquidación y con objeciones contemporáneas que ya estaban formalmente planteadas en 2019.</p>
        <div class="cf-chain-grid">
          <article class="cf-chain-card"><strong class="cf-date">23 FEB 2012</strong><h3>Litigio de minorías antes del concurso</h3><p>En el Juicio Verbal 1260/2011 del JPI nº 4 de Arrecife, la parte demandante amplió una acción de desahucio contra <strong>Monterecco Sun Park, S.L.</strong> tras afirmar que había conocido un cambio en la explotación. Es un documento de parte, no una sentencia sobre el fondo; pero fija que el conflicto operador/unidades existía antes del concurso de LPB.</p></article>
          <article class="cf-chain-card"><strong class="cf-date">14 ENE + 13 MAY 2019</strong><h3>DI 248, OB REM y la propia descripción unitaria</h3><p>La ampliación de DI 248 pidió investigar al perímetro AC/CAM y dejó constancia de una vía financiada de salida. Meses después, Aweswell impugnó la realización separada de fincas vinculadas. Su escrito reproduce el Plan/AC describiendo la oferta de CAM como una <strong>“oferta de adquisición unitaria de la unidad productiva”</strong> y diciendo que recepción, restaurante, bar, piscina, jardines y otras dotaciones no tenían aprovechamiento comercial independiente.</p></article>
          <article class="cf-chain-card"><strong class="cf-date">ENE–FEB 2026</strong><h3>Solicitud de revisión penal externa</h3><p>Una familia de denuncias y ampliaciones pidió a Fiscalía examinar, entre otras cuestiones, la supervisión judicial del AC, la relación entre unidad hotelera/deuda/operación, y la separación del paquete financiero histórico. Esos escritos prueban presentación de una tesis y solicitud de investigación; <strong>no prueban prevaricación, fraude, fabricación ni coordinación criminal</strong>.</p></article>
        </div>
        <div class="cf-chain-lock"><strong>Qué cambia en la lectura de la calificación.</strong><p>El expediente adverso contra Gil debe contrastarse también con la cronología preconcursal, con la disputa contemporánea de 2018–2019 y con el reconocimiento documental de una lógica económica unitaria en el propio Plan. Esto refuerza una pregunta de causalidad y conocimiento institucional; no sustituye la apelación ni convierte una alegación penal en un hecho probado.</p><p><strong>Fuente pendiente clave:</strong> un escrito de 8 de febrero de 2026 afirma que Fiscalía de Tenerife dictó el 27 de enero un decreto en Diligencias 20/2026. Esa afirmación seguirá identificada como <em>alegación contenida en un escrito</em> hasta recuperar el decreto firmado.</p></div>
        <div class="cf-chain-links">
          <a href="../comunidad-instrumentalizacion/">Comunidad e instrumentalización</a>
          <a href="../toma-control-sun-park-7-junio-2018/">7 junio 2018</a>
          <a href="../convergencia-venta-acreedor/">Venta / acreedor</a>
          <a href="../reclamacion-caixabank-valencia/">Valencia / CaixaBank</a>
          <a href="../concurso-36-2012-responsabilidad-institucional/">Responsabilidad institucional</a>
          <a href="../cuaderno-juridico/control-judicial-prevaricacion/">Control judicial / prevaricación</a>
        </div>
      </div>` : `
      <div class="shell record" id="puente-2012-2019-2026">
        <p class="eyebrow">NEW DOCUMENTARY BRIDGE · 2012 → 2019 → 2026</p>
        <h2>The classification cannot be read as though the operational conflict, the hotel's economic unity and objections to liquidation appeared only afterwards</h2>
        <p class="cf-intro">A new source bundle adds three distinct chronological layers. Together they do not prove criminal instrumentalisation of the classification; they do require any causation account of LPB's insolvency to be tested against an owner–operator conflict predating June 2012, the liquidation architecture's own unitary language, and contemporaneous objections already formally raised in 2019.</p>
        <div class="cf-chain-grid">
          <article class="cf-chain-card"><strong class="cf-date">23 FEB 2012</strong><h3>Minority-owner litigation before insolvency</h3><p>In Verbal Proceedings 1260/2011 before First Instance Court no. 4 Arrecife, the claimant side expanded an eviction action against <strong>Monterecco Sun Park, S.L.</strong> after saying it had learned of a change in operation. It is a party pleading, not a merits judgment; but it fixes the operator/unit conflict before LPB's insolvency.</p></article>
          <article class="cf-chain-card"><strong class="cf-date">14 JAN + 13 MAY 2019</strong><h3>DI 248, OB REM and the record's own unitary description</h3><p>The DI 248 expansion asked prosecutors to investigate the IA/CAM perimeter and recorded a claimed financed exit route. Months later Aweswell opposed separate realisation of linked properties. Its filing reproduces the Plan/IA description of CAM's proposal as an <strong>“oferta de adquisición unitaria de la unidad productiva”</strong> and states that reception, restaurant, bar, pool, gardens and other common facilities had no independent commercial exploitation.</p></article>
          <article class="cf-chain-card"><strong class="cf-date">JAN–FEB 2026</strong><h3>Request for external criminal-law review</h3><p>A family of complaints and expansions asked prosecutors to examine, among other matters, judicial supervision of the IA, the relationship between hotel unity/debt/operation, and separation of the historic financing package. Those filings prove that a theory was presented and investigation requested; they <strong>do not prove prevarication, fraud, fabrication or criminal coordination</strong>.</p></article>
        </div>
        <div class="cf-chain-lock"><strong>What this changes in reading the classification.</strong><p>The adverse case against Gil must also be tested against the pre-insolvency chronology, the contemporaneous 2018–2019 dispute and documentary recognition of a unitary economic logic in the Plan itself. That strengthens a causation and institutional-knowledge question; it does not replace the appeal or turn a criminal allegation into a proved fact.</p><p><strong>Key source still missing:</strong> an 8 February 2026 filing says Tenerife prosecutors issued a 27 January decree in Investigations 20/2026. That proposition remains labelled as <em>an allegation reported in a filing</em> until the signed decree is recovered.</p></div>
        <div class="cf-chain-links">
          <a href="../community-instrumentalisation/">Community instrumentalisation</a>
          <a href="../sun-park-takeover-7-june-2018/">7 June 2018</a>
          <a href="../sale-lender-convergence/">Sale / lender convergence</a>
          <a href="../caixabank-valencia-claim/">Valencia / CaixaBank</a>
          <a href="../insolvency-36-2012-institutional-accountability/">Institutional accountability</a>
          <a href="../legal-notebook/judicial-control-prevaricacion/">Judicial control / prevaricación</a>
        </div>
      </div>`;
  } else {
    section.innerHTML = es ? `
      <div class="shell record">
        <p class="eyebrow">PUENTE DOCUMENTAL · 2012 → 2019 → 2026</p>
        <h2>Una misma cuestión aparece desde tres ángulos documentales distintos</h2>
        <p>El nuevo paquete fuente incorpora: <strong>(1)</strong> litigio de propietarios minoritarios contra el operador antes del concurso; <strong>(2)</strong> DI 248 y la oposición de 2019 a la realización separada de activos vinculados, incluyendo la reproducción del lenguaje del Plan que describía una adquisición unitaria de la unidad productiva; y <strong>(3)</strong> denuncias de enero–febrero de 2026 que piden a Fiscalía revisar las hipótesis judiciales, comunitarias y financieras.</p>
        <p><strong>Control probatorio:</strong> los escritos de denuncia prueban qué se alegó y qué se pidió investigar, no que el delito denunciado se haya cometido. El lenguaje unitario reproducido en 2019 debe contrastarse con el Plan, oferta, tasación, escrituras y resoluciones originales.</p>
        <p><a href="../calificacion-concurso-36-2012-vidas-paralelas/#puente-2012-2019-2026">Ver el puente completo y su efecto sobre la calificación →</a></p>
      </div>` : `
      <div class="shell record">
        <p class="eyebrow">DOCUMENTARY BRIDGE · 2012 → 2019 → 2026</p>
        <h2>The same issue now appears through three different documentary angles</h2>
        <p>The new source bundle adds: <strong>(1)</strong> minority-owner litigation against the operator before insolvency; <strong>(2)</strong> DI 248 and the 2019 objection to separate disposal of linked assets, including reproduced Plan language describing a unitary acquisition of the production unit; and <strong>(3)</strong> January–February 2026 complaints asking prosecutors to review judicial, Community and financial hypotheses.</p>
        <p><strong>Evidence control:</strong> the complaints prove what was alleged and what investigators were asked to examine, not that the alleged offence occurred. The unitary language reproduced in 2019 must ultimately be checked against the original Plan, offer, valuation, deeds and signed orders.</p>
        <p><a href="../insolvency-classification-parallel-lives/#puente-2012-2019-2026">See the full bridge and its relevance to the classification →</a></p>
      </div>`;
  }

  const hero = document.querySelector('main .hero');
  const main = document.querySelector('main');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else if (main) main.insertAdjacentElement('afterbegin', section);
})();

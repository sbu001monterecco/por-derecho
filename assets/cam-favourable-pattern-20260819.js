(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const id = 'cam-favourable-pattern-19aug2026';
  if (document.getElementById(id)) return;

  const esTargets = [
    '/por-derecho/es/concurso-36-2012-administrador-concursal/',
    '/por-derecho/es/concurso-36-2012-magistrado-juez/',
    '/por-derecho/es/concurso-36-2012-responsabilidad-institucional/',
    '/por-derecho/es/acosta-matos-perimetro/',
    '/por-derecho/es/retracto-credito-litigioso-1041-2017/',
    '/por-derecho/es/toma-control-sun-park-7-junio-2018/',
    '/por-derecho/es/mismo-hotel-multiples-vidas-financieras/'
  ];
  const enTargets = [
    '/por-derecho/en/insolvency-36-2012-insolvency-administrator/',
    '/por-derecho/en/insolvency-36-2012-mercantile-court-1/',
    '/por-derecho/en/insolvency-36-2012-institutional-accountability/',
    '/por-derecho/en/acosta-matos-perimeter/',
    '/por-derecho/en/litigious-credit-retracto-1041-2017/',
    '/por-derecho/en/sun-park-takeover-7-june-2018/',
    '/por-derecho/en/same-hotel-multiple-financial-lives/'
  ];

  const isEs = esTargets.some(route => path.endsWith(route));
  const isEn = enTargets.some(route => path.endsWith(route));
  if (!isEs && !isEn) return;

  const style = document.createElement('style');
  style.textContent = `
    #${id}{background:#f4f1ea}
    #${id} .cam-pattern-box{max-width:1120px;margin:0 auto}
    #${id} .cam-pattern-shell{background:#3c1715;color:#fff;border-radius:20px;padding:1.3rem 1.45rem;box-shadow:0 12px 30px rgba(19,37,45,.12)}
    #${id} .cam-pattern-label{display:block;color:#f1c6be;font-size:.76rem;font-weight:850;letter-spacing:.08em;text-transform:uppercase;margin-bottom:.55rem}
    #${id} h2{color:#fff;margin:.15rem 0 .7rem}
    #${id} .cam-pattern-lead{font-size:1.05rem;line-height:1.55;margin:.2rem 0 1rem}
    #${id} .cam-pattern-flow{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);border-radius:13px;padding:.9rem 1rem;font-weight:800;letter-spacing:.01em}
    #${id} .cam-pattern-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.7rem;margin:1rem 0}
    #${id} .cam-pattern-grid article{background:#fff;color:#13252d;border-radius:13px;padding:.85rem}
    #${id} .cam-pattern-grid h3{margin:.05rem 0 .35rem;font-size:1rem}
    #${id} .cam-pattern-question{background:#fff8e8;color:#13252d;border-left:5px solid #8c6b2f;border-radius:0 12px 12px 0;padding:.9rem 1rem;margin:.9rem 0}
    #${id} .cam-pattern-boundary{font-size:.92rem;color:#f7e4df;margin:.8rem 0}
    #${id} .cam-pattern-actions{display:flex;gap:.65rem;flex-wrap:wrap;margin-top:1rem}
    #${id} .cam-pattern-actions a{display:inline-block;border-radius:999px;padding:.65rem 1rem;font-weight:800;text-decoration:none;background:#fff;color:#13252d}
    #${id} .cam-pattern-actions a.secondary{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.55)}
    @media(max-width:850px){#${id} .cam-pattern-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.id = id;
  section.className = 'section';
  section.innerHTML = isEs ? `
    <div class="shell cam-pattern-box"><div class="cam-pattern-shell">
      <span class="cam-pattern-label">PATRÓN UNITARIO · EFECTO ≠ INTENCIÓN PROBADA</span>
      <h2>Otra vez el mismo beneficiario: medir la dirección del efecto.</h2>
      <p class="cam-pattern-lead">El retracto 1041/2017 añade un hito temprano a una secuencia posterior de control, liquidación, adjudicación y continuidad comercial. La pregunta ya no es sólo si una decisión aislada fue correcta: es por qué episodios distintos producen repetidamente ventajas para el perímetro Acosta Matos mientras LPB pierde información, opciones, control, competencia o capacidad de reversión.</p>
      <div class="cam-pattern-flow">PROTECCIÓN LPB → ACTO/OMISIÓN AC → RESPUESTA JUDICIAL → GANANCIA CAM → PÉRDIDA LPB → ¿BENEFICIO DE LA MASA?</div>
      <div class="cam-pattern-grid">
        <article><h3>AC · test de lealtad</h3><p>Cuando el resultado favorece a CAM, ¿qué análisis contemporáneo muestra el beneficio equivalente para LPB y la masa?</p></article>
        <article><h3>Juez · asimetría de intervención</h3><p>¿Qué intensidad de verificación se usó para consolidar posiciones CAM y cuál se usó para disclosure, restitución o protección solicitada por LPB?</p></article>
        <article><h3>Coordinación · indicio, no hallazgo</h3><p>La repetición crea fuertes ópticas de convergencia funcional. Para probar coordinación hacen falta comunicaciones, instrucciones, influencia o acuerdo, no sólo resultados alineados.</p></article>
      </div>
      <div class="cam-pattern-question"><strong>Pregunta de presión:</strong> “¿Cómo ayuda a LPB matar la vía de retracto?” No presupone que el retracto fuera ganador; exige explicar por qué perder una opción judicial ya admitida era mejor para la masa que conservarla.</div>
      <p class="cam-pattern-boundary"><strong>Escalera:</strong> efecto repetido → posible incumplimiento/disloyal administration → posible administración desleal → posible influencia/prevaricación → posible actuación concertada. Cada escalón exige prueba adicional; ninguno se presume por el anterior.</p>
      <div class="cam-pattern-actions"><a href="/por-derecho/es/patron-efectos-favorables-acosta-matos/">Abrir patrón completo →</a><a class="secondary" href="/por-derecho/es/retracto-credito-litigioso-1041-2017/">DP 1041 / retracto</a></div>
    </div></div>` : `
    <div class="shell cam-pattern-box"><div class="cam-pattern-shell">
      <span class="cam-pattern-label">UNITARY PATTERN · EFFECT ≠ PROVEN INTENT</span>
      <h2>The same beneficiary again: measure the direction of effect.</h2>
      <p class="cam-pattern-lead">PP 1041/retracto adds an early node to the later control, liquidation, adjudication and commercial-continuity sequence. The question is no longer only whether one isolated decision was correct: it is why distinct episodes repeatedly advantage the Acosta Matos perimeter while LPB loses information, optionality, control, competition or reversibility.</p>
      <div class="cam-pattern-flow">LPB PROTECTION → ADMINISTRATOR ACT/OMISSION → JUDICIAL RESPONSE → CAM GAIN → LPB LOSS → ESTATE BENEFIT?</div>
      <div class="cam-pattern-grid">
        <article><h3>Administrator · loyalty test</h3><p>Where an outcome benefits CAM, what contemporaneous analysis identifies the equivalent benefit to LPB and the estate?</p></article>
        <article><h3>Court · intervention asymmetry</h3><p>What intensity of verification was used to consolidate CAM positions and what was used for disclosure, restitution or protection sought by LPB?</p></article>
        <article><h3>Coordination · indication, not finding</h3><p>Recurrence creates strong optics of functional convergence. Proving coordination requires communications, instructions, influence or agreement, not aligned outcomes alone.</p></article>
      </div>
      <div class="cam-pattern-question"><strong>Pressure test:</strong> “How does killing the retracto route help LPB?” It does not assume the retracto would win; it requires an explanation for why losing an already-admitted judicial option was better for the estate than preserving it.</div>
      <p class="cam-pattern-boundary"><strong>Ladder:</strong> repeated effect → possible duty breach/disloyal administration → possible criminal administración desleal → possible influence/prevaricación → possible concerted action. Each level requires additional evidence; none is presumed from the level below.</p>
      <div class="cam-pattern-actions"><a href="/por-derecho/en/acosta-matos-favourable-effect-pattern/">Open full pattern →</a><a class="secondary" href="/por-derecho/en/litigious-credit-retracto-1041-2017/">PP 1041 / retracto</a></div>
    </div></div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector(':scope > .hero, :scope > section.hero, :scope > .dossier-hero, :scope > .cnmv-hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else main.insertAdjacentElement('afterbegin', section);
})();

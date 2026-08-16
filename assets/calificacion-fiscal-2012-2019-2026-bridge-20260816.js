(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const es = path.includes('/por-derecho/es/');
  const en = path.includes('/por-derecho/en/');
  if (!es && !en) return;

  const calEs = '/por-derecho/es/calificacion-concurso-36-2012-vidas-paralelas/';
  const calEn = '/por-derecho/en/insolvency-classification-parallel-lives/';
  const updateEs = '/por-derecho/es/actualizaciones/';
  const updateEn = '/por-derecho/en/updates/';

  const community = new Set([
    '/por-derecho/es/comunidad-instrumentalizacion/',
    '/por-derecho/en/community-instrumentalisation/',
    '/por-derecho/es/insolvencia-lpb/',
    '/por-derecho/en/lpb-insolvency/'
  ]);
  const ac = new Set([
    '/por-derecho/es/concurso-36-2012-administrador-concursal/',
    '/por-derecho/en/insolvency-36-2012-insolvency-administrator/'
  ]);
  const judge = new Set([
    '/por-derecho/es/concurso-36-2012-magistrado-juez/',
    '/por-derecho/es/concurso-36-2012-juzgado-mercantil-1/',
    '/por-derecho/en/insolvency-36-2012-mercantile-court-1/',
    '/por-derecho/es/cuaderno-juridico/control-judicial-prevaricacion/',
    '/por-derecho/en/legal-notebook/judicial-control-prevaricacion/'
  ]);
  const fiscal = new Set([
    '/por-derecho/es/carta-abierta-ministerio-fiscal/',
    '/por-derecho/en/open-letter-public-prosecution-service/',
    '/por-derecho/es/dp-1901-2026/'
  ]);
  const control = new Set([
    '/por-derecho/es/toma-control-sun-park-7-junio-2018/',
    '/por-derecho/en/sun-park-takeover-7-june-2018/',
    '/por-derecho/es/acosta-matos-perimetro/',
    '/por-derecho/en/acosta-matos-perimeter/'
  ]);
  const recovery = new Set([
    '/por-derecho/es/objetivos-recuperacion-restitucion/',
    '/por-derecho/en/recovery-restitution-objectives/',
    '/por-derecho/es/concurso-36-2012-responsabilidad-institucional/',
    '/por-derecho/en/insolvency-36-2012-institutional-accountability/'
  ]);
  const lender = new Set([
    '/por-derecho/es/convergencia-venta-acreedor/',
    '/por-derecho/en/sale-lender-convergence/',
    '/por-derecho/es/reclamacion-caixabank-valencia/',
    '/por-derecho/en/caixabank-valencia-claim/'
  ]);

  const related = new Set([
    calEs, calEn,
    ...community, ...ac, ...judge, ...fiscal, ...control, ...recovery, ...lender
  ]);
  if (!related.has(path) && path !== updateEs && path !== updateEn) return;
  if (document.getElementById('cal-fiscal-chain-2012-2019-2026')) return;

  const calHref = es ? calEs : calEn;
  const style = document.createElement('style');
  style.textContent = `
    .cf-chain{border-top:1px solid rgba(19,37,45,.14)}
    .cf-chain .cf-intro{max-width:930px}
    .cf-chain-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:1.2rem 0}
    .cf-chain-card{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:16px;padding:1.05rem 1.1rem;border-top:5px solid #6b5841}
    .cf-chain-card strong.cf-date{display:block;font-size:.76rem;letter-spacing:.07em;text-transform:uppercase;color:#6b5841;margin-bottom:.4rem}
    .cf-chain-card h3{margin:.2rem 0 .55rem;font-size:1.08rem}
    .cf-chain-lock{background:#13252d;color:#fff;border-radius:17px;padding:1.15rem 1.3rem;margin:1.1rem 0}
    .cf-chain-lock a{color:#fff;text-decoration:underline}
    .cf-chain-triad{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin:1rem 0}
    .cf-chain-triad>div{background:#f5f1e8;border:1px solid rgba(19,37,45,.13);border-radius:14px;padding:.95rem}
    .cf-chain-triad strong{display:block;margin-bottom:.35rem}
    .cf-chain-status{border-left:5px solid #8c6b2f;background:#fbf8f1;padding:1rem 1.1rem;margin:1rem 0;border-radius:12px}
    .cf-chain-links{display:flex;flex-wrap:wrap;gap:.55rem;margin-top:.9rem}
    .cf-chain-links a{display:inline-block;border:1px solid rgba(19,37,45,.24);border-radius:999px;padding:.42rem .7rem;text-decoration:none}
    .cf-update{background:#f3efe4;border-left:5px solid #8c6b2f;border-radius:14px;padding:1.15rem 1.25rem;margin:1.5rem 0}
    @media(max-width:860px){.cf-chain-grid,.cf-chain-triad{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.id = 'cal-fiscal-chain-2012-2019-2026';
  section.className = 'section alt cf-chain';

  const isCal = path === calEs || path === calEn;
  const isUpdate = path === updateEs || path === updateEn;

  if (isUpdate) {
    section.innerHTML = es ? `
      <div class="shell record"><div class="cf-update">
        <p class="eyebrow">16 AGO 2026 · CALIFICACIÓN · ACTUALIZACIÓN DOCUMENTAL</p>
        <h2>Tres denuncias de enero, tres preguntas verificables</h2>
        <p>La fuente ya controlada se ha reforzado públicamente sin duplicar evidencia: <strong>13 enero</strong>, supervisión judicial de la Administración Concursal; <strong>24 enero</strong>, causalidad unidad hotelera/Comunidad y el aviso alegado de 12/07/2016 sobre €2.874.076,19 de pasivo; <strong>25 enero</strong>, matriz de contradicción entre deuda de mantenimiento, estado operativo y posterior relato de ruina/reforma.</p>
        <p><strong>Control:</strong> son denuncias y solicitudes de investigación. No son hallazgos de prevaricación, fabricación de deuda, fraude ni coordinación criminal. La ampliación subida como <code>(3)</code> es binariamente idéntica a la fuente CF-03 ya archivada: no cuenta como corroboración adicional.</p>
        <p><a href="${calEs}#puente-2012-2019-2026">Abrir el análisis completo de Calificación →</a></p>
      </div></div>` : `
      <div class="shell record"><div class="cf-update">
        <p class="eyebrow">16 AUG 2026 · CLASSIFICATION · DOCUMENTARY UPDATE</p>
        <h2>Three January complaints, three verifiable questions</h2>
        <p>The controlled source family is now surfaced more clearly without duplicating evidence: <strong>13 January</strong>, judicial supervision of the Insolvency Administrator; <strong>24 January</strong>, hotel-unity/Community causation and the alleged 12-Jul-2016 warning concerning €2,874,076.19 of liabilities; <strong>25 January</strong>, a contradiction matrix between maintenance debt, operating condition and the later ruin/refurbishment narrative.</p>
        <p><strong>Control:</strong> these are complaints and requests for investigation, not findings of prevarication, fabricated debt, fraud or criminal coordination. The newly uploaded <code>(3)</code> copy is byte-for-byte identical to already archived CF-03 and is not additional corroboration.</p>
        <p><a href="${calEn}#puente-2012-2019-2026">Open the full Classification analysis →</a></p>
      </div></div>`;
  } else if (isCal) {
    section.innerHTML = es ? `
      <div class="shell record" id="puente-2012-2019-2026">
        <p class="eyebrow">PUENTE DOCUMENTAL · 2012 → 2019 → ENERO 2026</p>
        <h2>La calificación debe probar su causalidad contra todo el sistema, no sólo contra el último síntoma</h2>
        <p class="cf-intro">El conjunto documental no demuestra que la Calificación haya sido instrumentalizada penalmente. Sí obliga a contrastar la atribución adversa a Gil/Pink con tres capas que ya existían fuera de esa conclusión: conflicto operador–unidades anterior al concurso, la propia lógica unitaria de la arquitectura de liquidación y preguntas formalmente planteadas en 2026 sobre supervisión, pasivo y coherencia económica.</p>
        <div class="cf-chain-grid">
          <article class="cf-chain-card"><strong class="cf-date">23 FEB 2012</strong><h3>El conflicto operador/unidades precede al concurso</h3><p>En JV 1260/2011 se amplió una acción contra Monterecco Sun Park tras un cambio alegado de explotación. Es un escrito de parte, no una resolución sobre el fondo, pero fija una controversia operativa anterior a junio de 2012.</p></article>
          <article class="cf-chain-card"><strong class="cf-date">14 ENE + 13 MAY 2019</strong><h3>DI 248, OB REM y unidad productiva</h3><p>La ampliación de DI 248 dejó formalizada la objeción contemporánea. El escrito de 13 mayo reproduce el Plan/AC describiendo la oferta como <strong>“oferta de adquisición unitaria de la unidad productiva”</strong> y las dotaciones comunes/vinculadas como carentes de aprovechamiento comercial independiente. El Plan original sigue siendo la fuente superior para su efecto jurídico exacto.</p></article>
        </div>
        <h3>Enero de 2026: tres documentos, tres preguntas que pueden contestarse con expedientes</h3>
        <div class="cf-chain-triad">
          <div><strong>13 enero · supervisión judicial</strong>La denuncia cuestiona que se reconociera la potestad de supervisión de oficio de la AC y, a la vez, se rechazara examinar el fondo por ausencia de indicios. <em>Pregunta:</em> ¿qué comprobación sustantiva se realizó antes de concluir que no había base para actuar de oficio?</div>
          <div><strong>24 enero · aviso de 2016 / pasivo</strong>La denuncia afirma que el 12/07/2016 se advirtió a la AC de al menos <strong>€2.874.076,19</strong> de pasivo supuestamente inflado. <em>Pregunta:</em> ¿se recibió el burofax, con qué anexos, qué se verificó y cómo se reconciliaron esas partidas?</div>
          <div><strong>25 enero · “tres realidades”</strong>La ampliación contrapone deuda comunitaria por mantenimiento, evidencia alegada de operación/mantenimiento y el posterior relato de ruina/reforma. <em>Pregunta:</em> ¿qué documentos contables, tasaciones, actas y gastos hacen compatibles —o incompatibles— esas tres descripciones?</div>
        </div>
        <div class="cf-chain-lock"><strong>Límite probatorio no negociable.</strong><p>La teoría de “validación recíproca” del escrito de 25 enero es una alegación. La convergencia puede justificar investigación o inferencia; <strong>no sustituye la prueba actor por actor</strong>: poder/deber → conocimiento verificado → comunicación/adopción/uso → acto u omisión → beneficio/consecuencia → causalidad → caracterización jurídica.</p></div>
        <div class="cf-chain-status"><strong>La conclusión adversa sigue visible.</strong> Sentencia 163/2023 continúa siendo materialmente adversa en la rama superviviente de falta posterior de reclamación de rentas / culpa grave / causalidad y complicidad de Pink, y está recurrida. Estos escritos no la revocan; amplían el contrarregistro causal que debe ser contrastado.</div>
        <div class="cf-chain-links">
          <a href="/por-derecho/es/comunidad-instrumentalizacion/">Comunidad</a>
          <a href="/por-derecho/es/concurso-36-2012-administrador-concursal/">Administrador Concursal</a>
          <a href="/por-derecho/es/concurso-36-2012-magistrado-juez/">Magistrado / Juzgado</a>
          <a href="/por-derecho/es/carta-abierta-ministerio-fiscal/">Ministerio Fiscal</a>
          <a href="/por-derecho/es/toma-control-sun-park-7-junio-2018/">Control 7 junio 2018</a>
          <a href="/por-derecho/es/objetivos-recuperacion-restitucion/">Recuperación</a>
        </div>
      </div>` : `
      <div class="shell record" id="puente-2012-2019-2026">
        <p class="eyebrow">DOCUMENTARY BRIDGE · 2012 → 2019 → JANUARY 2026</p>
        <h2>The classification causation case must be tested against the whole system, not only its last symptom</h2>
        <p class="cf-intro">The source family does not prove that the Classification was criminally instrumentalised. It does require the adverse attribution to Gil/Pink to be tested against three layers that pre-date or sit outside that conclusion: pre-insolvency operator/unit conflict, the liquidation architecture's own unitary logic, and formal 2026 questions concerning supervision, liabilities and economic consistency.</p>
        <div class="cf-chain-grid">
          <article class="cf-chain-card"><strong class="cf-date">23 FEB 2012</strong><h3>The operator/unit conflict predates insolvency</h3><p>In JV 1260/2011 a claim was expanded against Monterecco Sun Park following an alleged change of operation. It is a party pleading, not a merits ruling, but it fixes an operational dispute before June 2012.</p></article>
          <article class="cf-chain-card"><strong class="cf-date">14 JAN + 13 MAY 2019</strong><h3>DI 248, OB REM and the production unit</h3><p>The DI 248 expansion formally preserved the contemporaneous objection. The 13 May filing reproduces the Plan/IA describing the offer as an <strong>“oferta de adquisición unitaria de la unidad productiva”</strong> and the linked/common facilities as lacking independent commercial exploitation. The original Plan remains the superior source for exact legal effect.</p></article>
        </div>
        <h3>January 2026: three documents, three questions answerable from records</h3>
        <div class="cf-chain-triad">
          <div><strong>13 January · judicial supervision</strong>The complaint challenges the combination of recognising ex-officio IA supervisory power while declining merits examination for want of indicia. <em>Question:</em> what substantive verification occurred before concluding there was no basis to act ex officio?</div>
          <div><strong>24 January · 2016 warning / liabilities</strong>The complaint says that on 12-Jul-2016 the IA was warned of at least <strong>€2,874,076.19</strong> in allegedly inflated liabilities. <em>Question:</em> was the burofax received, with which annexes, what was verified, and how were those items reconciled?</div>
          <div><strong>25 January · “three realities”</strong>The expansion contrasts Community maintenance debt, alleged evidence of continued operation/maintenance, and the later ruin/refurbishment narrative. <em>Question:</em> which accounts, valuations, minutes and expenditure records make those descriptions compatible—or incompatible?</div>
        </div>
        <div class="cf-chain-lock"><strong>Non-negotiable evidence limit.</strong><p>The 25 January filing's “reciprocal validation” theory is an allegation. Convergence may justify investigation or inference; it <strong>does not replace actor-specific proof</strong>: power/duty → verified knowledge → communication/adoption/use → act/omission → benefit/consequence → causation → legal characterisation.</p></div>
        <div class="cf-chain-status"><strong>The adverse result remains visible.</strong> Judgment 163/2023 remains materially adverse on the surviving later rent-recovery / gross-fault / causation branch and Pink complicity, and it is appealed. These filings do not reverse it; they expand the causal counter-record that must be tested.</div>
        <div class="cf-chain-links">
          <a href="/por-derecho/en/community-instrumentalisation/">Community</a>
          <a href="/por-derecho/en/insolvency-36-2012-insolvency-administrator/">Insolvency Administrator</a>
          <a href="/por-derecho/en/insolvency-36-2012-mercantile-court-1/">Court / Judge</a>
          <a href="/por-derecho/en/open-letter-public-prosecution-service/">Public Prosecution Service</a>
          <a href="/por-derecho/en/sun-park-takeover-7-june-2018/">7 June 2018 control</a>
          <a href="/por-derecho/en/recovery-restitution-objectives/">Recovery</a>
        </div>
      </div>`;
  } else if (community.has(path)) {
    section.innerHTML = es ? `
      <div class="shell record"><p class="eyebrow">ENERO 2026 · COMUNIDAD / CAUSALIDAD</p><h2>La cuestión no es repetir “deuda falsa”, sino reconciliar tres registros económicos</h2><p>Las denuncias de 24–25 enero alegan que la deuda comunitaria de mantenimiento, el estado operativo/mantenido del hotel y el posterior relato de ruina/reforma no pueden aceptarse simultáneamente sin comprobar sus documentos de soporte. Esa incompatibilidad es <strong>una hipótesis de investigación</strong>, no una declaración del sitio de que las cuentas o certificaciones fueran falsas.</p><p>La prueba finita es: cuentas y presupuestos aprobados, facturas, bancos, modelos fiscales, actas, cuotas/votos, tasaciones 2017–2018, gastos reales de las explotadoras y trazabilidad del aviso alegado de 12/07/2016 a la AC.</p><p><a href="${calEs}#puente-2012-2019-2026">Ver su efecto sobre la Calificación →</a></p></div>` : `
      <div class="shell record"><p class="eyebrow">JANUARY 2026 · COMMUNITY / CAUSATION</p><h2>The question is not to repeat “fabricated debt”, but to reconcile three economic records</h2><p>The 24–25 January complaints allege that Community maintenance debt, the hotel's operating/maintained condition and the later ruin/refurbishment narrative cannot simply be accepted together without testing their supporting records. That incompatibility is <strong>an investigative hypothesis</strong>, not a website finding that the accounts or certificates were false.</p><p>The finite proof set is: approved accounts/budgets, invoices, banks, tax records, minutes, quotas/votes, 2017–2018 valuations, actual operator expenditure and traceability of the alleged 12-Jul-2016 warning to the IA.</p><p><a href="${calEn}#puente-2012-2019-2026">See its relevance to the Classification →</a></p></div>`;
  } else if (ac.has(path)) {
    section.innerHTML = es ? `
      <div class="shell record"><p class="eyebrow">ENERO 2026 · AC · CONOCIMIENTO Y RECONCILIACIÓN</p><h2>Un aviso cuantificado alegado exige una respuesta documental, no una inferencia</h2><p>La denuncia de 24 enero afirma que el 12/07/2016 se puso en conocimiento de la Administración Concursal un pasivo supuestamente inflado en al menos <strong>€2.874.076,19</strong>. La denuncia no sustituye el burofax original. La pregunta verificable es si fue recibido, con qué anexos, qué partidas se contrastaron y cómo se reflejó el resultado en el pasivo y en decisiones posteriores.</p><p>La denuncia de 13 enero añade una cuestión distinta sobre la supervisión judicial de la AC. Ninguna de las dos convierte una discrepancia, omisión alegada o resolución adversa en administración desleal o prevaricación probadas.</p><p><a href="${calEs}#puente-2012-2019-2026">Abrir la matriz completa →</a></p></div>` : `
      <div class="shell record"><p class="eyebrow">JANUARY 2026 · IA · KNOWLEDGE AND RECONCILIATION</p><h2>An alleged quantified warning calls for a documentary answer, not an inference</h2><p>The 24 January complaint says that on 12-Jul-2016 the Insolvency Administrator was notified that liabilities were allegedly inflated by at least <strong>€2,874,076.19</strong>. The complaint is not the original burofax. The verifiable question is whether it was received, with which annexes, which items were tested and how the result was reflected in the liabilities and later decisions.</p><p>The 13 January complaint adds a separate question about judicial supervision of the IA. Neither converts a dispute, alleged omission or adverse ruling into proved disloyal administration or prevarication.</p><p><a href="${calEn}#puente-2012-2019-2026">Open the full matrix →</a></p></div>`;
  } else if (judge.has(path)) {
    section.innerHTML = es ? `
      <div class="shell record"><p class="eyebrow">13 ENE 2026 · DENUNCIA DE SUPERVISIÓN JUDICIAL</p><h2>Una denuncia de prevaricación no es una prueba de prevaricación</h2><p>El escrito de 13 enero pide a Fiscalía investigar la tensión que el denunciante ve entre reconocer facultades de supervisión de oficio sobre la AC y no entrar al examen sustantivo de los hechos por no apreciar previamente indicios. La cuestión publicable es finita: <strong>qué hechos y documentos se verificaron realmente antes de decidir que no procedía activar esa supervisión de oficio</strong>.</p><p>Las resoluciones de 12/09/2025 y 11/11/2025 deben leerse por su texto primario y con sus vías de recurso. Resultado adverso, error alegado o razonamiento circular no equivalen por sí solos a una resolución injusta a sabiendas.</p><p><a href="${calEs}#puente-2012-2019-2026">Ver la conexión con Calificación →</a></p></div>` : `
      <div class="shell record"><p class="eyebrow">13 JAN 2026 · JUDICIAL-SUPERVISION COMPLAINT</p><h2>A prevarication complaint is not proof of prevarication</h2><p>The 13 January filing asks prosecutors to investigate the tension the complainant sees between recognising ex-officio supervisory powers over the IA and declining substantive examination because sufficient indicia were not first perceived. The publishable question is finite: <strong>which facts and records were actually verified before deciding there was no basis to activate that ex-officio supervision</strong>.</p><p>The 12-Sep-2025 and 11-Nov-2025 rulings must be read from their primary text and with their appellate routes. An adverse result, alleged error or alleged circular reasoning does not by itself establish a knowingly unjust judicial decision.</p><p><a href="${calEn}#puente-2012-2019-2026">See the Classification connection →</a></p></div>`;
  } else if (fiscal.has(path)) {
    section.innerHTML = es ? `
      <div class="shell record"><p class="eyebrow">ENERO 2026 · FISCALÍA · AVISO NO ES HALLAZGO</p><h2>Lo que las denuncias prueban es presentación, contenido y solicitud de diligencias</h2><p>Los escritos de 13, 24 y 25 enero preservan formalmente tres familias de cuestiones: supervisión judicial de la AC; causalidad unidad hotelera/Comunidad/pasivo; y la contradicción alegada entre mantenimiento, operación y posterior ruina/reforma. <strong>Su presentación no demuestra aceptación fiscal ni investigación de cada proposición.</strong></p><p>El siguiente nivel probatorio es trazable: número de expediente/recepción, órgano asignado, diligencias practicadas, documentos requeridos, razón de archivo/remisión si la hubo y cualquier decisión posterior.</p><p><a href="${calEs}#puente-2012-2019-2026">Ver la arquitectura completa →</a></p></div>` : `
      <div class="shell record"><p class="eyebrow">JANUARY 2026 · PROSECUTION · NOTICE IS NOT A FINDING</p><h2>What the complaints prove is submission, content and requested investigative steps</h2><p>The 13, 24 and 25 January filings formally preserve three question families: judicial supervision of the IA; hotel-unity/Community/liability causation; and the alleged contradiction between maintenance, operation and the later ruin/refurbishment narrative. <strong>Submission does not prove prosecutorial acceptance or investigation of every proposition.</strong></p><p>The next evidential layer is traceable: file/receipt reference, assigned office, measures actually performed, records requested, any reasoned archive/referral and later decision.</p><p><a href="${calEn}#puente-2012-2019-2026">See the full architecture →</a></p></div>`;
  } else if (control.has(path)) {
    section.innerHTML = es ? `
      <div class="shell record"><p class="eyebrow">25 ENE 2026 · CONTROL 2018 · CONTRADICCIÓN A COMPROBAR</p><h2>El relato de “ruina” posterior al cambio de control debe compararse con el registro anterior, no asumirse</h2><p>La ampliación de 25 enero plantea que el mantenimiento comunitario reclamado, el estado previo que atribuye a tasaciones/operación y el posterior cierre/reforma forman una contradicción. Esto es una <strong>matriz de prueba</strong>, no una conclusión de sabotaje, coacción o falsedad.</p><p>La comparación debe respetar las cuatro capas ya controladas: título formal, posesión legal, control material/de facto y posesión práctica hotelera alegada. El control material de 7 junio 2018 no es por sí solo título sobre todo el hotel.</p><p><a href="${calEs}#puente-2012-2019-2026">Ver la causalidad en Calificación →</a></p></div>` : `
      <div class="shell record"><p class="eyebrow">25 JAN 2026 · 2018 CONTROL · CONTRADICTION TO TEST</p><h2>The post-control “ruin” narrative must be compared with the earlier record, not assumed</h2><p>The 25 January expansion argues that claimed Community maintenance, the prior condition it attributes to valuations/operation and the later closure/refurbishment narrative form a contradiction. This is an <strong>evidence matrix</strong>, not a finding of sabotage, coercion or falsehood.</p><p>The comparison must preserve the four controlled layers: formal title, legal possession, material/de facto control and alleged practical hotel-wide possession. The 7 June 2018 material-control transition is not by itself title to the whole hotel.</p><p><a href="${calEn}#puente-2012-2019-2026">See the causation analysis in Classification →</a></p></div>`;
  } else if (recovery.has(path)) {
    section.innerHTML = es ? `
      <div class="shell record"><p class="eyebrow">ENERO 2026 · RECUPERACIÓN / RESPONSABILIDAD</p><h2>Estas denuncias sirven mejor como mapa de producción que como catálogo de delitos</h2><p>La utilidad patrimonial del conjunto es identificar documentos capaces de confirmar, reducir o descartar daño y causalidad: burofax y anexos de 12/07/2016, cuentas y bancos de Comunidad, tasaciones 2017–2018, gastos reales de explotación, expediente de supervisión de la AC y respuesta institucional a cada aviso.</p><p>La cuantificación debe seguir separando <strong>LPB concursal</strong>, <strong>Matkator/terceros extraconcursales</strong> y <strong>Aweswell/transfronterizo</strong>; una misma cronología no fusiona titulares ni daños.</p><p><a href="${calEs}#puente-2012-2019-2026">Abrir el contrarregistro de Calificación →</a></p></div>` : `
      <div class="shell record"><p class="eyebrow">JANUARY 2026 · RECOVERY / ACCOUNTABILITY</p><h2>These complaints work better as a production map than as an offence catalogue</h2><p>Their patrimonial value is to identify records capable of confirming, narrowing or excluding damage and causation: the 12-Jul-2016 burofax/annexes, Community accounts/banks, 2017–2018 valuations, actual operating expenditure, the IA-supervision record and institutional response to each notice.</p><p>Quantum must continue to separate <strong>LPB insolvency-estate</strong>, <strong>Matkator/third-party extraconcursal</strong> and <strong>Aweswell/cross-border</strong> planes; a shared chronology does not merge right-holders or losses.</p><p><a href="${calEn}#puente-2012-2019-2026">Open the Classification counter-record →</a></p></div>`;
  } else {
    section.innerHTML = es ? `
      <div class="shell record"><p class="eyebrow">PUENTE DOCUMENTAL · 2012 → 2019 → 2026</p><h2>La unidad económica aparece en documentos distintos; la criminalidad no se presume</h2><p>El paquete conecta litigio preconcursal, objeciones contemporáneas de 2019 y denuncias de enero de 2026. Su fuerza está en las preguntas que permite verificar, no en convertir alegaciones posteriores en hechos. El lenguaje unitario reproducido en 2019 debe compararse con Plan, oferta, tasación, escrituras y resoluciones originales.</p><p><a href="${calEs}#puente-2012-2019-2026">Ver el puente completo →</a></p></div>` : `
      <div class="shell record"><p class="eyebrow">DOCUMENTARY BRIDGE · 2012 → 2019 → 2026</p><h2>Economic unity appears across different records; criminality is not presumed</h2><p>The bundle connects pre-insolvency litigation, contemporaneous 2019 objections and January-2026 complaints. Its strength lies in the questions it makes verifiable, not in converting later allegations into facts. The unitary language reproduced in 2019 must be checked against the original Plan, offer, valuation, deeds and signed orders.</p><p><a href="${calEn}#puente-2012-2019-2026">See the full bridge →</a></p></div>`;
  }

  const hero = document.querySelector('main .hero');
  const main = document.querySelector('main');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else if (main) main.insertAdjacentElement('afterbegin', section);
})();
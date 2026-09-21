(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const es = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const en = path.endsWith('/en/insolvency-classification-parallel-lives/');
  if (!es && !en) return;
  if (document.querySelector('[data-cal-professional-read="1"]')) return;

  const style = document.createElement('style');
  style.textContent = `
    .cal-proread{padding:1.5rem 0 2rem;background:#f6f4ee}.cal-proread-wrap{max-width:1080px;margin:0 auto}.cal-proread-head{background:#fff;border:2px solid #13252d;border-radius:20px;padding:1.35rem 1.45rem}.cal-proread .eyebrow{margin-bottom:.35rem}.cal-proread h2{margin:.2rem 0 .6rem;font-size:clamp(1.6rem,3.5vw,2.35rem)}.cal-proread-intro{max-width:880px}.cal-pro-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;margin-top:1rem}.cal-pro-card{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:16px;padding:1.05rem}.cal-pro-card h3{margin:.1rem 0 .65rem}.cal-pro-card li{margin:.45rem 0}.cal-pro-card.fact{border-top:5px solid #526b59}.cal-pro-card.q{border-top:5px solid #8c6b2f}.cal-pro-card.gap{border-top:5px solid #6b6b6b}.cal-actor-test{margin-top:1rem;background:#13252d;color:#fff;border-radius:16px;padding:1.1rem 1.2rem}.cal-actor-test strong{display:block;margin-bottom:.45rem}.cal-actor-test code{white-space:normal;color:#fff;font-family:inherit;font-weight:800}.cal-boundary{margin-top:1rem;background:#fff;border-left:5px solid #8c6b2f;border-radius:14px;padding:1rem 1.15rem}.cal-defence{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin-top:1rem}.cal-defence article{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:14px;padding:.95rem}.cal-defence h4{margin:.1rem 0 .45rem}.cal-status-key{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:1rem}.cal-status-key span{font-size:.72rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase;border-radius:999px;padding:.25rem .55rem;background:#fff;border:1px solid rgba(19,37,45,.18)}
    @media(max-width:860px){.cal-pro-grid,.cal-defence{grid-template-columns:1fr}.cal-proread-head{border-radius:0}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.className = 'cal-proread';
  section.dataset.calProfessionalRead = '1';

  const esHtml = `<div class="shell cal-proread-wrap"><div class="cal-proread-head">
    <p class="eyebrow">LECTURA PROFESIONAL · 90 SEGUNDOS</p>
    <h2>Antes de la acusación: qué está documentado, qué se pregunta y qué sigue abierto</h2>
    <p class="cal-proread-intro">Esta página contiene una acusación grave de Gil Marer. No pide que se acepte por autoridad personal. El método es colocar cada conclusión adversa junto al documento contrario, probar cuándo llegó al actor correspondiente y separar hecho, inferencia y acusación.</p>
    <div class="cal-pro-grid">
      <article class="cal-pro-card fact"><h3>5 proposiciones documentadas</h3><ol>
        <li>La Sentencia 163/2023 es materialmente adversa y está recurrida.</li>
        <li>El informe de calificación de 47 páginas del Administrador Concursal ha sido leído y cruzado íntegramente con el resto del expediente controlado.</li>
        <li>La propia sentencia rechazó o redujo de alcance partes relevantes del paquete AC/Fiscal, mientras mantuvo otras conclusiones adversas.</li>
        <li>Existe un contrarregistro contemporáneo de continuidad, financiación, explotación, preservación y salida del concurso, incluido el paquete comercial articulado en torno al perímetro ONA/Clubotel.</li>
        <li>DI 248/2018 y la calificación quedaron documentalmente conectados mediante actuaciones del Ministerio Fiscal, lo que permite formular preguntas concretas de circularidad y revisión independiente.</li>
      </ol></article>
      <article class="cal-pro-card q"><h3>5 preguntas finitas</h3><ol>
        <li>¿Qué material contrario estaba efectivamente ante el AC cuando formuló cada alegación?</li>
        <li>¿Qué material contrario estaba ante el Fiscal Ricardo de Mosteyrín cuando firmó su dictamen?</li>
        <li>¿Qué material contrario estaba ante el magistrado Alberto López Villarrubia al firmar la Sentencia 163/2023?</li>
        <li>¿Por qué fueron rechazadas o estrechadas unas acusaciones mientras sobrevivieron otras conclusiones adversas?</li>
        <li>¿Qué resolución terminal existe, si alguna, en el RPL 2523/2025 y cuál es exactamente su efecto?</li>
      </ol></article>
      <article class="cal-pro-card gap"><h3>3 lagunas que siguen abiertas</h3><ol>
        <li>Matriz completa de transmisión y conocimiento, proposición por proposición, para AC, Fiscal y Juez.</li>
        <li>Expediente certificado completo de la vista/servicio de 25 de julio de 2023 y su tratamiento probatorio.</li>
        <li>Expediente de apelación completo y cualquier resolución terminal posterior que todavía no conste en el corpus controlado.</li>
      </ol></article>
    </div>
    <div class="cal-actor-test"><strong>PRUEBA CENTRAL: EVIDENCIA ANTE EL ACTOR</strong><code>CONCLUSIÓN / ALEGACIÓN → DOCUMENTO CONTRARIO → FECHA → TRANSMISIÓN → GRADO DE CONOCIMIENTO → TRATAMIENTO U OMISIÓN → CONSECUENCIA → MEJOR EXPLICACIÓN ALTERNATIVA → QUÉ QUEDA DESPUÉS DE ACEPTARLA</code></div>
    <div class="cal-defence">
      <article><h4>Defensa más fuerte del Juez</h4><p>Un desacuerdo probatorio o un error jurídico no demuestra prevaricación.</p><p><strong>Qué queda:</strong> identificar sólo aquellas proposiciones en las que el material contrario pueda probarse ante el Juez y explicar por qué la incompatibilidad seguiría siendo material incluso aceptando la explicación judicial más favorable.</p></article>
      <article><h4>Defensa más fuerte del AC</h4><p>Existieron retrasos, documentación discutida y problemas reales de cobro.</p><p><strong>Qué queda:</strong> si hechos adversos más estrechos fueron ampliados a un relato global de no colaboración y causalidad pese a material contrario dentro de su propia administración.</p></article>
      <article><h4>Defensa más fuerte del Fiscal</h4><p>La referencia a dolo o culpa del “administrador concursal” puede ser un error de redacción.</p><p><strong>Qué queda:</strong> identificar el sujeto pretendido y comprobar si el resto de la individualización y causalidad sigue siendo fiable después de aceptar esa explicación.</p></article>
    </div>
    <div class="cal-boundary"><strong>Límite de no interferencia en la apelación.</strong><p>El RPL 2523/2025 corresponde a la Audiencia Provincial y debe resolverse desde su expediente judicial. Esta página no pide a ningún magistrado que decida desde la web ni fuera de las actuaciones. Su función es trazabilidad documental, corrección pública y preservación de preguntas verificables.</p></div>
    <div class="cal-status-key"><span>Hecho documentado</span><span>Conclusión de primera instancia</span><span>Recurrido</span><span>Rechazado / estrechado</span><span>Alegación de parte</span><span>Inferencia basada en evidencia</span><span>Evidencia abierta</span></div>
  </div></div>`;

  const enHtml = `<div class="shell cal-proread-wrap"><div class="cal-proread-head">
    <p class="eyebrow">90-SECOND PROFESSIONAL READ</p>
    <h2>Before the accusation: what is documented, what is being asked, and what remains open</h2>
    <p class="cal-proread-intro">This page contains a serious allegation by Gil Marer. It does not ask the reader to accept it on personal authority. The method is to place each adverse proposition beside contrary evidence, prove when that material reached the relevant actor, and separate fact, inference and allegation.</p>
    <div class="cal-pro-grid">
      <article class="cal-pro-card fact"><h3>5 documented propositions</h3><ol>
        <li>Judgment 163/2023 is materially adverse and under appeal.</li>
        <li>The Insolvency Administrator's 47-page classification report has been read in full and cross-walked against the controlled record.</li>
        <li>The judgment itself rejected or narrowed material parts of the AC/Fiscal package while retaining other adverse findings.</li>
        <li>A contemporaneous counter-record exists of continuity, finance, hotel operation, preservation and insolvency-exit work, including the commercial package around the ONA/Clubotel perimeter.</li>
        <li>DI 248/2018 and the classification proceeding are documentarily connected through Ministerio Fiscal acts, allowing finite questions about circularity and independent review.</li>
      </ol></article>
      <article class="cal-pro-card q"><h3>5 finite questions</h3><ol>
        <li>What contrary material was actually before the AC when each allegation was made?</li>
        <li>What contrary material was before Fiscal Ricardo de Mosteyrín when he signed his opinion?</li>
        <li>What contrary material was before Magistrate-Judge Alberto López Villarrubia when Judgment 163/2023 was signed?</li>
        <li>Why were some allegations rejected or narrowed while other adverse findings survived?</li>
        <li>What terminating decision exists, if any, in RPL 2523/2025 and what is its exact legal effect?</li>
      </ol></article>
      <article class="cal-pro-card gap"><h3>3 evidence gaps still treated as open</h3><ol>
        <li>Complete proposition-by-proposition transmission and knowledge matrix for AC, Fiscal and Judge.</li>
        <li>Complete certified 25 July 2023 hearing/service record and its evidential treatment.</li>
        <li>Complete appellate record and any later terminating decision not yet present in the controlled corpus.</li>
      </ol></article>
    </div>
    <div class="cal-actor-test"><strong>CENTRAL TEST: EVIDENCE BEFORE THE ACTOR</strong><code>FINDING / ALLEGATION → CONTRARY SOURCE → DATE → TRANSMISSION → KNOWLEDGE GRADE → TREATMENT / OMISSION → CONSEQUENCE → STRONGEST ALTERNATIVE EXPLANATION → WHAT REMAINS AFTER ACCEPTING IT</code></div>
    <div class="cal-defence">
      <article><h4>Judge's strongest defence</h4><p>Evidential disagreement or legal error does not establish judicial prevarication.</p><p><strong>What remains:</strong> isolate only propositions where contrary material can be proved before the Judge and explain why the incompatibility remains material even after accepting the strongest reasonable judicial explanation.</p></article>
      <article><h4>AC's strongest defence</h4><p>There were real delays, documentation disputes and collection problems.</p><p><strong>What remains:</strong> whether narrower adverse facts were expanded into a global non-collaboration/causation narrative despite contrary material within the administration itself.</p></article>
      <article><h4>Fiscal's strongest defence</h4><p>The reference to intent or fault of the “insolvency administrator” may be a drafting error.</p><p><strong>What remains:</strong> identify the intended subject and test whether the remaining individualisation and causation stay reliable after accepting that explanation.</p></article>
    </div>
    <div class="cal-boundary"><strong>Appeal non-interference boundary.</strong><p>RPL 2523/2025 is for the Audiencia Provincial to determine from its judicial record. This page does not ask any magistrate to decide from the website or outside the proceedings. Its purpose is documentary traceability, public correction and preservation of verifiable questions.</p></div>
    <div class="cal-status-key"><span>Documented fact</span><span>First-instance finding</span><span>Appealed</span><span>Rejected / narrowed</span><span>Party allegation</span><span>Evidence-based inference</span><span>Open evidence</span></div>
  </div></div>`;

  section.innerHTML = es ? esHtml : enHtml;
  const opening = document.querySelector('[data-calificacion-opening-20260816]');
  const hero = document.querySelector('.hero.cal-hero') || document.querySelector('main .hero');
  if (opening && opening.parentNode) opening.parentNode.insertBefore(section, opening);
  else if (hero && hero.parentNode) hero.insertAdjacentElement('afterend', section);
})();
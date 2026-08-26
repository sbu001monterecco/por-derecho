/* PROSECUTION-PUBLIC-ENTRY-20260824
 * Public-safe first-read layer for the unitary criminal-evidence architecture.
 * It preserves Gil Marer / Aweswell's direct actor-specific criminal attribution
 * without converting it into an adjudicated finding or a collective presumption.
 */
(() => {
  const normalise = value => {
    let path = (value || '/').replace(/\/index\.html$/i, '/');
    if (!path.endsWith('/')) path += '/';
    return path.toLowerCase();
  };
  const path = normalise(location.pathname);
  const isEn = document.documentElement.lang === 'en' || /\/en\//.test(path);
  const isEs = !isEn;
  const isHome = /\/(es|en)\/$/.test(path);
  const isUnitaryCriminal = path.endsWith('/es/ingenieria-inversa-criminal-unitaria/') || path.endsWith('/en/unitary-criminal-reverse-engineering/');
  if (!isHome && !isUnitaryCriminal) return;

  const style = document.createElement('style');
  style.dataset.prosecutionPublicEntryStyle = '20260824';
  style.textContent = `
    .prosecution-entry-20260821{padding:clamp(2.8rem,6vw,5rem) 0;background:#f3f0e9;border-top:1px solid rgba(19,37,45,.12);border-bottom:1px solid rgba(19,37,45,.12)}
    .prosecution-entry-20260821 .pe-head{max-width:72rem;margin-bottom:1.2rem}
    .prosecution-entry-20260821 .pe-kicker{font-size:.74rem;letter-spacing:.09em;text-transform:uppercase;font-weight:900;color:#8c2f2c}
    .prosecution-entry-20260821 h2{font-size:clamp(2rem,4vw,3.25rem);line-height:1.04;margin:.3rem 0 .8rem;color:#13252d}
    .prosecution-entry-20260821 .pe-lead{font-size:1.08rem;line-height:1.62;max-width:70rem}
    .prosecution-entry-20260821 .pe-attribution{border-left:7px solid #8c2f2c;background:#fff4f2;padding:1rem 1.15rem;border-radius:12px;margin:1rem 0;line-height:1.58}
    .prosecution-entry-20260821 .pe-proof-rule{border-left:6px solid #8c6b2f;background:#fff;padding:1rem 1.15rem;border-radius:12px;margin:1rem 0 1.35rem;line-height:1.55}
    .prosecution-entry-20260821 .pe-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.75rem}
    .prosecution-entry-20260821 .pe-card{background:#fff;border:1px solid rgba(19,37,45,.16);border-top:4px solid #13252d;border-radius:13px;padding:1rem}
    .prosecution-entry-20260821 .pe-card:first-child{border-top-color:#8c2f2c}.prosecution-entry-20260821 .pe-card:nth-child(2){border-top-color:#8c6b2f}.prosecution-entry-20260821 .pe-card:nth-child(3){border-top-color:#5b5578}.prosecution-entry-20260821 .pe-card:nth-child(4){border-top-color:#526b59}
    .prosecution-entry-20260821 .pe-card b{display:block;color:#6d5527;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.35rem}
    .prosecution-entry-20260821 .pe-card strong{display:block;line-height:1.25;margin-bottom:.45rem;color:#13252d}
    .prosecution-entry-20260821 .pe-card span{font-size:.88rem;line-height:1.45}
    .prosecution-entry-20260821 .pe-reg{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:.6rem;margin:1rem 0}
    .prosecution-entry-20260821 .pe-stat{background:#13252d;color:#fff;border-radius:11px;padding:.8rem}
    .prosecution-entry-20260821 .pe-stat strong{display:block;font-size:1.55rem;line-height:1}.prosecution-entry-20260821 .pe-stat span{display:block;font-size:.72rem;opacity:.84;margin-top:.3rem}
    .prosecution-entry-20260821 .pe-limit{font-size:.88rem;line-height:1.5;border-left:5px solid #526b59;padding:.7rem .85rem;background:#fff;border-radius:9px}
    .prosecution-entry-20260821 .pe-actions{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:1rem}.prosecution-entry-20260821 .pe-actions a{display:inline-block;padding:.68rem .9rem;border-radius:8px;background:#13252d;color:#fff;text-decoration:none;font-weight:800}.prosecution-entry-20260821 .pe-actions a.secondary{background:#fff;color:#13252d;border:1px solid #13252d}
    .prosecution-reading-control-20260821{margin:1rem auto 2rem;max-width:1120px;border:2px solid #8c6b2f;border-left-width:7px;border-radius:14px;background:#fffdf8;padding:1.1rem 1.25rem;line-height:1.56}
    .prosecution-reading-control-20260821 h2{font-size:1.35rem;margin:.1rem 0 .55rem;color:#13252d}.prosecution-reading-control-20260821 p{margin:.5rem 0}.prosecution-reading-control-20260821 a{font-weight:850}
    @media(max-width:900px){.prosecution-entry-20260821 .pe-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.prosecution-entry-20260821 .pe-reg{grid-template-columns:repeat(2,minmax(0,1fr))}}
    @media(max-width:560px){.prosecution-entry-20260821 .pe-grid,.prosecution-entry-20260821 .pe-reg{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const prefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const mapHref = isEn ? `${prefix}en/unitary-criminal-evidence-map/` : `${prefix}es/mapa-probatorio-penal-unitario/`;
  const correctionsHref = isEn ? `${prefix}en/corrections-version-control/` : `${prefix}es/correcciones-control-versiones/`;
  const camHref = isEn
    ? `${prefix}en/cam-creditor-control-shadow-administration-judicial-omission/`
    : `${prefix}es/control-acreedor-cam-administracion-hecho-omision-judicial/`;

  const mountHome = () => {
    if (!isHome || document.querySelector('[data-prosecution-entry-20260824]')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const section = document.createElement('section');
    section.className = 'prosecution-entry-20260821';
    section.dataset.prosecutionEntry20260824 = 'true';
    section.dataset.expressCriminalAttribution = '20260824';
    section.setAttribute('aria-label', isEn ? 'Express criminal attribution and proof control' : 'Atribución penal expresa y control probatorio');
    section.innerHTML = isEn ? `
      <div class="shell">
        <div class="pe-head"><span class="pe-kicker">Express attributed criminal theory · individual proof · no collective conviction</span><h2>One alleged enterprise; separately proved actors, acts and offences.</h2><p class="pe-lead">The attribution is direct. The evidence, contrary record, missing proof and adjudication status are separate. No audience-first summary may weaken the accusation into a concern, possible lead or neutral chronology; no accusation may be presented as a conviction.</p></div>
        <div class="pe-attribution"><strong>Attributed criminal theory · not a judicial finding.</strong> Gil Marer and Aweswell allege one continuing economic-criminal enterprise, advanced through successive adoption and divided functions. The theory does not itself prove a statutory criminal organisation or group under Criminal Code Articles 570 bis or 570 ter, an original pact, any person’s participation or guilt. Each actor and each offence require separate proof of their historical elements, conduct, capacity or duty, knowledge, intent where required, causal contribution and contrary material. This is only a factual allegation of connection: it does not characterise the conduct as a continuing or permanent offence or alter completion, any participation window or limitation period for any specific offence. Within that attributed theory, Gil Marer and Aweswell directly accuse Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila María Cogolludo Ramos, José Daniel Acosta Matos and Laura Patricia Acosta Matos of operating, by 2018 at the latest, as a coordinated de facto or shadow-administration structure over Luchy Playa Blanca’s patrimonial and business sphere and the integrated hotel platform, through acts inside the formal insolvency and outside its recorded perimeter. Gil separately accuses the insolvency administrator of affirmative enablement through emails, meetings, requests, authorisations, decisions, implementation, adoption and ratification, as well as omissions; and Judge Alberto López Villarrubia of decisions, refusals, evidential closures, delay and omissions allegedly preserving the mechanism and sabotaging or frustrating a developed, finance-backed exit. Those person-specific allegations remain subject to the proof rule below.</div>
        <div class="pe-proof-rule"><strong>Controlling proof rule:</strong> actor → express allegation → alleged act or omission → capacity/duty → supporting source → contrary or exculpatory material → missing proof → procedural/adjudication status → alleged effect or benefit. <strong>Relationship is not responsibility; missing proof does not erase the allegation.</strong></div>
        <div class="pe-grid">
          <article class="pe-card"><b>1 · five private actors</b><strong>Shadow administration, direct instruction and coordinated implementation alleged</strong><span>Debt/voting, access/security, works, information, finance, operation, income, title and outcome are mapped person by person. Native mandate and command-chain proof remains required.</span></article>
          <article class="pe-card"><b>2 · insolvency administrator</b><strong>Affirmative acts and an Article 11 omission route are tested separately</strong><span>Affirmative participation requires its own act and Articles 28–29 basis. Omission under Article 11 applies only to a result offence where a specific legal or contractual duty, or prior creation of risk, a real capacity to prevent, equivalence to causing the result and counterfactual causal contribution are proved. Later conduct cannot retroactively create participation in an already completed offence.</span></article>
          <article class="pe-card"><b>3 · judicial conduct</b><strong>Articles 446–449 and procedural fraud remain distinct alternatives</strong><span>Article 446 requires a knowingly unjust judgment or decision; 447 gross negligence or inexcusable ignorance; 448 refusal to adjudicate; and 449 malicious delay. The competent actor—judge or magistrate versus LAJ or other official—must be identified. Induced judicial error and knowing judicial injustice are alternatives unless different stages or actors are proved.</span></article>
          <article class="pe-card"><b>4 · adverse record</b><strong>Dismissal, valid rights and innocent explanations preserved</strong><span>The 2018 provisional dismissal and appeal, possible valid CAM credit/unit title, later adjudication and all exculpatory records remain visible and accurately scoped.</span></article>
        </div>
        <div class="pe-reg"><div class="pe-stat"><strong>360</strong><span>REG-AGE records in analysed snapshot</span></div><div class="pe-stat"><strong>80</strong><span>destination labels</span></div><div class="pe-stat"><strong>319</strong><span>Recibido</span></div><div class="pe-stat"><strong>15</strong><span>Enviado</span></div><div class="pe-stat"><strong>26</strong><span>Rechazado</span></div></div>
        <div class="pe-limit"><strong>Non-finding and registry-status limit:</strong> a direct party accusation is not a judicial finding. SENT ≠ DELIVERED ≠ RECEIVED ≠ ACKNOWLEDGED ≠ JOINED ≠ ADMITTED ≠ INVESTIGATED ≠ ACCEPTED ≠ ENDORSED ≠ PROVED.</div>
        <div class="pe-actions"><a href="${camHref}">Open the CAM direct-attribution and proof matrix →</a><a class="secondary" href="${mapHref}">Open the eight-package evidence map</a><a class="secondary" href="${correctionsHref}">Corrections and contrary evidence</a></div>
      </div>` : `
      <div class="shell">
        <div class="pe-head"><span class="pe-kicker">Teoría penal atribuida expresa · prueba individual · ninguna condena colectiva</span><h2>Una empresa alegada; actores, actos y delitos probados por separado.</h2><p class="pe-lead">La atribución es directa. La prueba, el registro contrario, la prueba pendiente y el estado de adjudicación son campos separados. Ningún resumen orientado a la audiencia puede rebajar la acusación a preocupación, posible indicio o cronología neutral; ninguna acusación puede presentarse como condena.</p></div>
        <div class="pe-attribution"><strong>Teoría penal atribuida · no hallazgo judicial.</strong> Gil Marer y Aweswell alegan una sola empresa continuada de criminalidad económica, desarrollada mediante adopción sucesiva y división de funciones. La teoría no prueba por sí sola una organización o grupo criminal conforme a los artículos 570 bis o 570 ter del Código Penal, un pacto originario, la participación de persona alguna ni culpabilidad. Cada actor y cada delito requieren prueba separada de sus elementos históricos, conducta, capacidad o deber, conocimiento, intención cuando sea exigible, contribución causal y material contrario. Esta es solo una alegación fáctica de conexión: no califica los hechos como delito continuado o permanente ni altera la consumación, la ventana de participación o la prescripción de ningún delito concreto. Dentro de esa teoría atribuida, Gil Marer y Aweswell acusan directamente a Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila María Cogolludo Ramos, José Daniel Acosta Matos y Laura Patricia Acosta Matos de operar, a más tardar en 2018, como una estructura coordinada de administradores de hecho o en la sombra sobre la esfera patrimonial y empresarial de Luchy Playa Blanca y la plataforma hotelera integrada, mediante actos dentro del concurso formal y fuera de su perímetro registrado. Gil acusa separadamente al administrador concursal de habilitación afirmativa por correos, reuniones, peticiones, autorizaciones, decisiones, implementación, adopción y ratificación, además de omisiones; y al Magistrado-Juez Alberto López Villarrubia de resoluciones, negativas, cierres probatorios, demoras y omisiones que habrían preservado el mecanismo y saboteado o frustrado una salida desarrollada y respaldada por financiación. Esas alegaciones personales siguen sujetas a la regla probatoria siguiente.</div>
        <div class="pe-proof-rule"><strong>Regla probatoria rectora:</strong> actor → acusación expresa → acto u omisión atribuido → capacidad/deber → fuente de apoyo → material contrario o exculpatorio → prueba pendiente → estado procesal/adjudicativo → efecto o beneficio atribuido. <strong>Relación no es responsabilidad; la prueba pendiente no borra la acusación.</strong></div>
        <div class="pe-grid">
          <article class="pe-card"><b>1 · cinco actores privados</b><strong>Se alega administración en la sombra, instrucción directa y ejecución coordinada</strong><span>Deuda/voto, acceso/seguridad, obras, información, financiación, operación, ingresos, título y resultado se mapean persona por persona. Sigue exigiéndose prueba nativa de mandato y cadena de mando.</span></article>
          <article class="pe-card"><b>2 · administrador concursal</b><strong>Los actos afirmativos y la omisión del artículo 11 se prueban por rutas separadas</strong><span>La participación afirmativa exige acto propio y encaje en los artículos 28–29. La omisión del artículo 11 solo opera para un delito de resultado si se prueban deber específico legal o contractual, o creación previa del riesgo, capacidad real de impedir, equivalencia con causar el resultado y contribución causal contrafactual. La conducta posterior no crea retroactivamente participación en un delito ya consumado.</span></article>
          <article class="pe-card"><b>3 · conducta judicial</b><strong>Los artículos 446–449 y el fraude procesal son alternativas distintas</strong><span>El artículo 446 exige sentencia o resolución injusta dictada a sabiendas; el 447, imprudencia grave o ignorancia inexcusable; el 448, negativa a juzgar; y el 449, retardo malicioso. Debe identificarse al actor competente—juez o magistrado frente a LAJ u otro funcionario. Error judicial inducido e injusticia judicial consciente son alternativas salvo que se prueben fases o actores distintos.</span></article>
          <article class="pe-card"><b>4 · registro adverso</b><strong>Se conservan archivo, derechos válidos y explicaciones inocentes</strong><span>El archivo provisional de 2018 y su apelación, posibles derechos válidos de crédito/títulos CAM, adjudicación posterior y toda prueba exculpatoria permanecen visibles y delimitados.</span></article>
        </div>
        <div class="pe-reg"><div class="pe-stat"><strong>360</strong><span>registros REG-AGE en el snapshot analizado</span></div><div class="pe-stat"><strong>80</strong><span>etiquetas de destino</span></div><div class="pe-stat"><strong>319</strong><span>Recibido</span></div><div class="pe-stat"><strong>15</strong><span>Enviado</span></div><div class="pe-stat"><strong>26</strong><span>Rechazado</span></div></div>
        <div class="pe-limit"><strong>Límite de no declaración y estado registral:</strong> una acusación directa de parte no es una declaración judicial. ENVIADO ≠ ENTREGADO ≠ RECIBIDO ≠ ACUSADO ≠ UNIDO ≠ ADMITIDO ≠ INVESTIGADO ≠ ACEPTADO ≠ RESPALDADO ≠ PROBADO.</div>
        <div class="pe-actions"><a href="${camHref}">Abrir la matriz CAM de atribución directa y prueba →</a><a class="secondary" href="${mapHref}">Abrir el mapa de ocho paquetes</a><a class="secondary" href="${correctionsHref}">Correcciones y prueba contraria</a></div>
      </div>`;
    const anchor = document.querySelector('.priority-band');
    const before = document.querySelector('#resumen-60-segundos, #sixty-second-summary');
    if (anchor) anchor.insertAdjacentElement('afterend', section);
    else if (before) before.insertAdjacentElement('beforebegin', section);
    else main.prepend(section);
  };

  const mountCriminalReadingControl = () => {
    if (!isUnitaryCriminal || document.querySelector('[data-prosecution-reading-control-20260821]')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const box = document.createElement('aside');
    box.className = 'prosecution-reading-control-20260821';
    box.dataset.prosecutionReadingControl20260821 = 'true';
    box.setAttribute('role', 'note');
    box.innerHTML = isEn ? `
      <h2>Reading control — direct attribution and proof are separate</h2>
      <p>Gil Marer / Aweswell's actor-specific accusations remain direct. Any numeric strength score is only an <strong>evidence-prioritisation indicator</strong>, not a probability, conviction, criminal-liability score or statement that every element is established. Contrary evidence and innocent explanations remain part of the same method.</p>
      <p>The current public-safe controlling map is <a href="${mapHref}">Eight mechanisms. Individual proof. No collective conviction →</a>.</p>` : `
      <h2>Control de lectura — atribución directa y prueba son campos separados</h2>
      <p>Las acusaciones actor-específicas de Gil Marer / Aweswell siguen siendo directas. Cualquier puntuación numérica es únicamente un <strong>indicador de priorización probatoria</strong>, no una probabilidad, condena, puntuación de responsabilidad penal ni afirmación de que todo elemento esté acreditado. La prueba contraria y las explicaciones inocentes forman parte del mismo método.</p>
      <p>El mapa público de control actual es <a href="${mapHref}">Ocho mecanismos. Prueba individual. Ninguna condena colectiva →</a>.</p>`;
    const hero = main.querySelector('.hero');
    if (hero) hero.insertAdjacentElement('afterend', box);
    else main.prepend(box);
  };

  const replaceText = (root, pairs) => {
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    for (const node of nodes) {
      let value = node.nodeValue;
      for (const [from, to] of pairs) {
        if (value.includes(from)) value = value.replace(from, to);
      }
      if (value !== node.nodeValue) node.nodeValue = value;
    }
  };

  const applySpanishSourceCorrections = () => {
    if (!isHome || !isEs) return;
    replaceText(document.querySelector('main'), [
      [
        'Autos incompatibles en octubre, aclaración en enero, testimonios y escritura en febrero e inscripción a favor de CAM en abril de 2022.',
        'Dos resoluciones de 15 de octubre de 2021 aparecen en aparente tensión; sus originales firmados, objeto y contexto procesal deben conciliarse. Después constan aclaraciones en enero, testimonios y escritura en febrero e inscripción a favor de CAM en abril de 2022.'
      ],
      [
        'No se ha localizado un auto de posesión o desalojo a favor de CAM.',
        'No se ha localizado en el expediente examinado un auto que entregara a CAM la posesión del conjunto Sun Park el 7 de junio de 2018.'
      ],
      [
        'La reunión separada de Las Palmas de 11 de junio documenta a PwC analizando cuentas y contratos de 2008–2015 con representantes de la Comunidad.',
        'La reunión separada de Las Palmas se sitúa el 10 de junio de 2016 según la cadena contemporánea; una transcripción derivada posterior fue rotulada 11JUN2016.'
      ]
    ]);
  };

  const apply = () => {
    mountHome();
    mountCriminalReadingControl();
    applySpanishSourceCorrections();
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply, { once: true });
  else apply();
  // The site has an inherited dynamic loader chain. Repeat only to catch late-rendered legacy modules.
  setTimeout(apply, 500);
  setTimeout(apply, 1500);
})();

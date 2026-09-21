(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const id = 'ac-loyalty-breakpoint-19aug2026';
  if (document.getElementById(id)) return;

  const isEs = path.includes('/por-derecho/es/');
  const isEn = path.includes('/por-derecho/en/');
  if (!isEs && !isEn) return;

  const utilityFragments = [
    '/buscar/', '/search/', '/aviso-legal-privacidad/', '/legal-privacy/',
    '/actualizaciones/', '/updates/', '/libros/', '/books/', '/libro/', '/book/'
  ];
  if (utilityFragments.some(fragment => path.includes(fragment))) return;

  const groups = {
    community: ['comunidad', 'community', 'actas', 'cexp', 'explotacion', 'exploitation', 'pwc-canarias', 'jonathan-simo'],
    administrator: ['administrador-concursal', 'insolvency-administrator', 'grant-thornton', '/rsm/'],
    cam: ['acosta-matos', 'sale-lender-convergence', 'convergencia-venta-acreedor'],
    retracto: ['retracto', 'article-1535', 'articulo-1535', 'litigious-credit'],
    takeover: ['toma-control', 'takeover', 'actua-2018', 'sunpark264'],
    judge: ['magistrado-juez', 'mercantile-court-1', 'responsabilidad-institucional', 'institutional-accountability', 'cgpj-supervision'],
    recovery: ['recuperacion-restitucion', 'recovery-restitution', 'quien-debe-responder', 'who-must-answer'],
    downstream: ['ricpe', 'mismo-hotel', 'same-hotel', 'fondos-incentivos', 'institutionalisation-chain', 'incentivos-regionales', 'feder', 'mynd', 'orion'],
    insolvency: ['insolvencia-lpb', 'lpb-insolvency', 'calificacion-concurso', 'qualification-insolvency']
  };
  const has = key => groups[key].some(fragment => path.includes(fragment));
  const isCore = Object.keys(groups).some(has);

  const style = document.createElement('style');
  style.textContent = `
    #${id}{background:#f5f3ee}
    #${id} .aclb-wrap{max-width:1120px;margin:0 auto}
    #${id} .aclb-card{background:#17242b;color:#fff;border-radius:18px;padding:1.15rem 1.3rem;box-shadow:0 10px 28px rgba(19,37,45,.10)}
    #${id} .aclb-label{display:block;font-size:.75rem;font-weight:850;letter-spacing:.08em;text-transform:uppercase;color:#ffe6a8;margin-bottom:.4rem}
    #${id} h2{color:#fff;margin:.1rem 0 .55rem;font-size:1.35rem}
    #${id} h3{margin:.05rem 0 .25rem;font-size:.95rem}
    #${id} p{line-height:1.55;margin:.4rem 0}
    #${id} .aclb-flow{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:.8rem .9rem;margin:.8rem 0;font-weight:750}
    #${id} .aclb-thresholds{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.55rem;margin:.8rem 0}
    #${id} .aclb-thresholds article{background:#fff;color:#17242b;border-radius:11px;padding:.7rem}
    #${id} .aclb-test{background:#fff8e7;color:#17242b;border-left:5px solid #9b7428;border-radius:0 11px 11px 0;padding:.8rem .9rem;margin:.8rem 0}
    #${id} .aclb-route{background:rgba(255,255,255,.08);border-radius:11px;padding:.8rem .9rem;margin:.7rem 0}
    #${id} .aclb-boundary{font-size:.9rem;color:#f1dfdb;margin-top:.65rem}
    #${id} .aclb-actions{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:.85rem}
    #${id} .aclb-actions a{display:inline-block;background:#fff;color:#17242b;text-decoration:none;font-weight:800;border-radius:999px;padding:.58rem .88rem}
    #${id} .aclb-actions a.secondary{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.5)}
    #${id}.compact .aclb-card{padding:.9rem 1.1rem}
    #${id}.compact h2{font-size:1.12rem}
    @media(max-width:900px){#${id} .aclb-thresholds{grid-template-columns:repeat(2,minmax(0,1fr))}}
    @media(max-width:620px){#${id} .aclb-thresholds{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const routeTextEs = () => {
    if (has('community')) return '<strong>Aplicación aquí — pre-CAM:</strong> separar la arquitectura privada/Comunidad de 2008–2017 de la función concursal. ¿Qué posiciones de deuda, voto, acceso, explotación o autoridad recibió la AC, cuáles verificó independientemente y cuáles terminó convirtiendo en realidad material o concursal?';
    if (has('administrator')) return '<strong>Aplicación aquí — dossier principal:</strong> puntuar cada acto material L0–L6. No basta preguntar si perjudicó a LPB; hay que identificar la fuente del poder, el interés de la masa, el problema de la parte adversa que resolvió y el beneficio concreto para LPB.';
    if (has('cam')) return '<strong>Aplicación aquí — sucesión/adopción:</strong> ¿qué creó CAM por sí mismo y qué heredó o adoptó de una arquitectura adversa ya existente? ¿Qué actos de la AC fueron necesarios para transformar esa arquitectura en crédito, acceso, control, liquidación o adjudicación?';
    if (has('retracto')) return '<strong>Aplicación aquí — poder derivado del deudor:</strong> CAM no podía por sí mismo cesar al abogado de LPB ni controlar las instrucciones procesales de LPB. La AC sí tenía facultades derivadas del concurso. ¿Se usaron en interés documentado de la masa o, funcionalmente, para retirar un obstáculo al perímetro adverso? La instrucción concreta del desistimiento sigue abierta.';
    if (has('takeover')) return '<strong>Aplicación aquí — control material:</strong> ¿qué parte del control de hecho dependió de maquinaria de Comunidad, seguridad, acceso o autorizaciones de la AC? La respuesta debe ser finca por finca y separar poder concursal, propiedad, posesión y derechos extraconcursales.';
    if (has('judge')) return '<strong>Aplicación aquí — supervisión:</strong> ¿en qué momento, si alguno, la independencia de la AC dejó de ser una premisa que podía darse por supuesta y pasó a requerir comprobación, contraste, abstención, separación o supervisión judicial reforzada?';
    if (has('recovery')) return '<strong>Aplicación aquí — remedios:</strong> si se prueba un punto de quiebre, no sigue una nulidad global automática. Deben mapearse, acto por acto y titular por titular, autoridad, ineficacia/nulidad cuando proceda, indefensión, restitución, enriquecimiento injusto, contabilidad, daños y restauración de posiciones perdidas.';
    if (has('downstream')) return '<strong>Aplicación aquí — dependencia aguas abajo:</strong> HNT, MYND, RICPE, RIC, incentivos y otras capas no quedan invalidadas por asociación. Debe identificarse qué posición posterior depende de un acto previo de la AC y cuál se sostiene sobre un título jurídico independiente.';
    if (has('insolvency')) return '<strong>Aplicación aquí — interés del concurso:</strong> para cada decisión de masa, liquidación, adjudicación, cuenta o calificación, identificar qué beneficio obtuvo LPB/la masa y si la decisión se tomó antes o después de un eventual punto material de conflicto o pérdida de independencia.';
    return '<strong>Aplicación transversal:</strong> donde aparezca una decisión, omisión o certificación de la AC, preguntar quién tenía el problema, qué poder concursal lo resolvió, quién obtuvo el beneficio y qué recibió LPB/la masa.';
  };

  const routeTextEn = () => {
    if (has('community')) return '<strong>Application here — pre-CAM:</strong> separate the 2008–2017 private/Community architecture from the insolvency office. Which debt, voting, access, exploitation or authority positions reached the administrator, which were independently verified, and which were turned into material or insolvency reality?';
    if (has('administrator')) return '<strong>Application here — principal dossier:</strong> score every material act L0–L6. Do not ask only whether LPB was harmed; identify the source of power, estate interest, adverse-party problem solved and concrete LPB benefit.';
    if (has('cam')) return '<strong>Application here — succession/adoption:</strong> what did CAM create independently and what did it inherit or adopt from an already-existing adverse architecture? Which administrator-controlled acts were necessary to convert that architecture into credit, access, control, liquidation or adjudication?';
    if (has('retracto')) return '<strong>Application here — debtor-derived power:</strong> CAM could not itself remove LPB’s lawyer or control LPB’s litigation instructions. The administrator possessed insolvency-derived powers. Were they used for a documented estate interest or functionally to remove an obstacle confronting the adverse perimeter? The specific withdrawal instruction remains open.';
    if (has('takeover')) return '<strong>Application here — material control:</strong> what part of de facto control depended on Community machinery, security, access or administrator authority? The answer must be finca/right-holder specific and separate insolvency power, title, possession and extraconcursal rights.';
    if (has('judge')) return '<strong>Application here — supervision:</strong> at what point, if any, did administrator independence cease to be a premise that could safely be assumed and become a matter requiring verification, contrast, abstention, separation or enhanced judicial supervision?';
    if (has('recovery')) return '<strong>Application here — remedies:</strong> a proved breakpoint would not create automatic global nullity. Map authority, invalidity/ineffectiveness where available, indefension, restitution, unjust enrichment, accounting, damages and restoration act by act and claimant by claimant.';
    if (has('downstream')) return '<strong>Application here — downstream dependency:</strong> HNT, MYND, RICPE, RIC, incentives and other layers are not invalid by association. Identify which later position depends on an earlier administrator-controlled act and which rests on an independent legal basis.';
    if (has('insolvency')) return '<strong>Application here — insolvency interest:</strong> for each estate, liquidation, adjudication, accounts or qualification decision, identify the benefit to LPB/the estate and whether the act occurred before or after any material conflict/independence breakpoint.';
    return '<strong>Cross-cutting application:</strong> wherever an administrator decision, omission or certification appears, ask whose problem it solved, what insolvency power supplied the solution, who benefited and what LPB/the estate received.';
  };

  const section = document.createElement('section');
  section.id = id;
  section.className = `section${isCore ? '' : ' compact'}`;

  if (isEs) {
    section.innerHTML = isCore ? `
      <div class="shell aclb-wrap"><div class="aclb-card">
        <span class="aclb-label">LEALTAD · CONFLICTO · INDEPENDENCIA · HIPÓTESIS DE AGENCIA FUNCIONAL</span>
        <h2>¿Cuándo, si ocurrió, las facultades confiadas a la AC para proteger a LPB empezaron a funcionar en favor del perímetro adverso?</h2>
        <p>La reconstrucción no empieza con Acosta Matos. Retrocede a la fractura de la venta/explotación de 2008 y al perímetro Monte Lanza/Molina/Comunidad, y pregunta después si CAM entró en un terreno neutral o adoptó y amplificó una arquitectura adversa ya existente con conocimiento, apoyo o cooperación de la Administración Concursal.</p>
        <div class="aclb-flow">2008 → perímetro pre-CAM → deuda / votos / acceso → actos u omisiones AC → CAM → crédito / control → junio 2018 → liquidación / adjudicación → HNT / MYND / financiación</div>
        <div class="aclb-thresholds">
          <article><h3>1 · Lealtad</h3><p>¿Cuándo deja de ser sostenible una explicación de administración leal de LPB/la masa?</p></article>
          <article><h3>2 · Conflicto</h3><p>¿Cuándo conoce o debe reconocer la AC una alineación material con intereses adversos?</p></article>
          <article><h3>3 · Independencia</h3><p>¿Cuándo exige la situación revelación, abstención, sustitución o supervisión reforzada?</p></article>
          <article><h3>4 · Agencia funcional</h3><p>¿Cuándo, si acaso, pasa de efecto/conflicto a implementar conscientemente objetivos que el adversario necesitaba poder concursal para conseguir?</p></article>
        </div>
        <div class="aclb-test"><strong>Power-source test:</strong> ¿se utilizó una facultad confiada a la AC para LPB/la masa para producir un resultado que la parte adversa no podía producir legítimamente por sí misma? Después: ¿qué problema ajeno resolvió, quién lo pidió, quién ganó y qué beneficio documentado recibió LPB?</div>
        <div class="aclb-route">${routeTextEs()}</div>
        <p class="aclb-boundary"><strong>Límite:</strong> “agencia funcional/de facto” es una etiqueta forense de Por Derecho, no una doctrina autónoma que se dé por establecida. No se publica como hecho que la AC fuera agente formal de Molina/CAM, que existiera colusión, ni que todos sus actos sean nulos. El nivel más alto exige comunicaciones, instrucciones, representación, acuerdo, contraprestación o planificación común.</p>
        <div class="aclb-actions"><a href="/por-derecho/es/administrador-concursal-punto-quiebre-lealtad/">Abrir análisis completo →</a><a class="secondary" href="/por-derecho/es/retracto-credito-litigioso-1041-2017/">Caso de prueba DP 1041</a></div>
      </div></div>` : `
      <div class="shell aclb-wrap"><div class="aclb-card">
        <span class="aclb-label">PREGUNTA GLOBAL DE CONTROL</span>
        <h2>Lealtad → conflicto → independencia → posible agencia funcional adversa.</h2>
        <p>Por Derecho reconstruye si las facultades de la AC siguieron sirviendo al interés de LPB/la masa o si, en algún punto, empezaron a resolver funcionalmente los problemas de un perímetro privado adverso. ${routeTextEs()}</p>
        <p class="aclb-boundary">La hipótesis no equivale a una agencia formal, colusión probada o nulidad global.</p>
        <div class="aclb-actions"><a href="/por-derecho/es/administrador-concursal-punto-quiebre-lealtad/">Ver la prueba transversal →</a></div>
      </div></div>`;
  } else {
    section.innerHTML = isCore ? `
      <div class="shell aclb-wrap"><div class="aclb-card">
        <span class="aclb-label">LOYALTY · CONFLICT · INDEPENDENCE · FUNCTIONAL-AGENCY HYPOTHESIS</span>
        <h2>When, if ever, did powers entrusted to the administrator to protect LPB begin functioning for the adverse perimeter?</h2>
        <p>The reconstruction does not begin with Acosta Matos. It runs back to the fracture of the 2008 sale/operating structure and the Monte Lanza/Molina/Community perimeter, then asks whether CAM entered neutral ground or knowingly adopted and amplified an existing adverse architecture with administrator support or cooperation.</p>
        <div class="aclb-flow">2008 → pre-CAM perimeter → debt / votes / access → administrator acts or omissions → CAM → credit / control → June 2018 → liquidation / adjudication → HNT / MYND / finance</div>
        <div class="aclb-thresholds">
          <article><h3>1 · Loyalty</h3><p>When does a loyal LPB/estate-interest explanation cease to be sustainable?</p></article>
          <article><h3>2 · Conflict</h3><p>When does the administrator know or have reason to recognise material alignment with adverse interests?</p></article>
          <article><h3>3 · Independence</h3><p>When do disclosure, abstention, replacement or enhanced supervision become necessary?</p></article>
          <article><h3>4 · Functional agency</h3><p>When, if ever, does the pattern move from effect/conflict to knowing implementation of objectives that required insolvency power?</p></article>
        </div>
        <div class="aclb-test"><strong>Power-source test:</strong> was a power entrusted to the administrator for LPB/the estate used to produce an outcome the adverse party could not itself lawfully produce? Then ask whose problem it solved, who requested it, who gained and what documented benefit LPB received.</div>
        <div class="aclb-route">${routeTextEn()}</div>
        <p class="aclb-boundary"><strong>Boundary:</strong> “functional/de facto agency” is a Por Derecho forensic label, not an asserted standalone legal doctrine. It is not published as a finding of formal agency, collusion or global invalidity. The highest level requires communications, instructions, representation, agreement, consideration or common planning.</p>
        <div class="aclb-actions"><a href="/por-derecho/en/insolvency-administrator-loyalty-breakpoint/">Open full analysis →</a><a class="secondary" href="/por-derecho/en/litigious-credit-retracto-1041-2017/">PP 1041 test case</a></div>
      </div></div>` : `
      <div class="shell aclb-wrap"><div class="aclb-card">
        <span class="aclb-label">GLOBAL CONTROL QUESTION</span>
        <h2>Loyalty → conflict → independence → possible adverse functional agency.</h2>
        <p>Por Derecho reconstructs whether administrator powers continued serving LPB/the estate or at some point began functionally solving problems for an adverse private perimeter. ${routeTextEn()}</p>
        <p class="aclb-boundary">The hypothesis is not equivalent to formal agency, proven collusion or global invalidity.</p>
        <div class="aclb-actions"><a href="/por-derecho/en/insolvency-administrator-loyalty-breakpoint/">Open cross-cutting test →</a></div>
      </div></div>`;
  }

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector(':scope > .hero, :scope > section.hero, :scope > .dossier-hero, :scope > .cnmv-hero, :scope > .rr-hero');
  const thesis = main.querySelector('[data-calificacion-misuse-thesis]');
  if (thesis || hero) (thesis || hero).insertAdjacentElement('afterend', section);
  else main.insertAdjacentElement('afterbegin', section);
})();

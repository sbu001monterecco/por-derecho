/* PROSECUTION-PUBLIC-ENTRY-20260821
 * Public-safe entry layer for the unitary criminal-evidence architecture.
 * This module sharpens evidential navigation; it does not convert allegations,
 * institutional receipt, relationship, benefit, chronology or legal error into guilt.
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
  style.dataset.prosecutionPublicEntryStyle = '20260821';
  style.textContent = `
    .prosecution-entry-20260821{padding:clamp(2.8rem,6vw,5rem) 0;background:#f3f0e9;border-top:1px solid rgba(19,37,45,.12);border-bottom:1px solid rgba(19,37,45,.12)}
    .prosecution-entry-20260821 .pe-head{max-width:68rem;margin-bottom:1.5rem}
    .prosecution-entry-20260821 .pe-kicker{font-size:.74rem;letter-spacing:.09em;text-transform:uppercase;font-weight:850;color:#6d5527}
    .prosecution-entry-20260821 h2{font-size:clamp(2rem,4vw,3.25rem);line-height:1.04;margin:.3rem 0 .8rem;color:#13252d}
    .prosecution-entry-20260821 .pe-lead{font-size:1.08rem;line-height:1.62;max-width:64rem}
    .prosecution-entry-20260821 .pe-proof-rule{border-left:6px solid #8c6b2f;background:#fff;padding:1rem 1.15rem;border-radius:12px;margin:1rem 0 1.35rem;line-height:1.55}
    .prosecution-entry-20260821 .pe-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.75rem}
    .prosecution-entry-20260821 .pe-card{background:#fff;border:1px solid rgba(19,37,45,.16);border-top:4px solid #13252d;border-radius:13px;padding:1rem}
    .prosecution-entry-20260821 .pe-card b{display:block;color:#6d5527;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.35rem}
    .prosecution-entry-20260821 .pe-card strong{display:block;line-height:1.25;margin-bottom:.45rem;color:#13252d}
    .prosecution-entry-20260821 .pe-card span{font-size:.88rem;line-height:1.45}
    .prosecution-entry-20260821 .pe-reg{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:.6rem;margin:1rem 0}
    .prosecution-entry-20260821 .pe-stat{background:#13252d;color:#fff;border-radius:11px;padding:.8rem}
    .prosecution-entry-20260821 .pe-stat strong{display:block;font-size:1.55rem;line-height:1}.prosecution-entry-20260821 .pe-stat span{display:block;font-size:.72rem;opacity:.84;margin-top:.3rem}
    .prosecution-entry-20260821 .pe-limit{font-size:.88rem;line-height:1.5;border-left:5px solid #8c2f2c;padding:.7rem .85rem;background:#fff;border-radius:9px}
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

  const mountHome = () => {
    if (!isHome || document.querySelector('[data-prosecution-entry-20260821]')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const section = document.createElement('section');
    section.className = 'prosecution-entry-20260821';
    section.dataset.prosecutionEntry20260821 = 'true';
    section.setAttribute('aria-label', isEn ? 'Criminal-law evidence lens' : 'Lente probatoria penal');
    section.innerHTML = isEn ? `
      <div class="shell">
        <div class="pe-head"><span class="pe-kicker">Criminal-law lens · evidence before attribution</span><h2>Eight evidence packages — not a collective accusation.</h2><p class="pe-lead">Por Derecho asks competent authorities to test a connected economic-criminal hypothesis through finite primary records. The method is deliberately falsifiable: a lawful explanation or contrary document that defeats an inference belongs in the same record as evidence that supports it.</p></div>
        <div class="pe-proof-rule"><strong>Individual attribution only:</strong> act → capacity/authority → authorship/instruction → knowledge → intent where required → use/reliance → prejudice → benefit → causation → correction or continuation after notice. <strong>Relationship is not responsibility.</strong></div>
        <div class="pe-grid">
          <article class="pe-card"><b>PKG-A · PP1041</b><strong>Who authorised the withdrawal filed in LPB's name?</strong><span>Produce instruction, author, power, LexNET record, LPB hearing, insolvency authority and estate-interest rationale.</span></article>
          <article class="pe-card"><b>PKG-B · debt → vote</b><strong>Was the debt used to affect voting rights validly built?</strong><span>Service, legal debtor, allocation, due date, certificate, no duplication, vote consequence and later external use.</span></article>
          <article class="pe-card"><b>PKG-C · 7 June</b><strong>What converted security authority into material control?</strong><span>Security does not by itself authorise locks, keys, exclusion, private-unit intervention, possession, works or operation.</span></article>
          <article class="pe-card"><b>PKG-H · notice → conduct</b><strong>What happened after each documented notice?</strong><span>Exact proposition, source, competence, later act, correction/non-correction, benefit and causally linked prejudice.</span></article>
        </div>
        <div class="pe-reg"><div class="pe-stat"><strong>360</strong><span>REG-AGE records in analysed snapshot</span></div><div class="pe-stat"><strong>80</strong><span>destination labels</span></div><div class="pe-stat"><strong>319</strong><span>Recibido</span></div><div class="pe-stat"><strong>15</strong><span>Enviado</span></div><div class="pe-stat"><strong>26</strong><span>Rechazado</span></div></div>
        <div class="pe-limit"><strong>Registry status limit:</strong> SENT ≠ DELIVERED ≠ RECEIVED ≠ ACKNOWLEDGED ≠ JOINED ≠ ADMITTED ≠ INVESTIGATED ≠ ACCEPTED ≠ ENDORSED ≠ PROVED. The snapshot covers 7 December 2025–15 August 2026; it is a transmission/chronology layer, not a merits finding.</div>
        <div class="pe-actions"><a href="${mapHref}">Open the eight-package evidence map →</a><a class="secondary" href="${correctionsHref}">Corrections and contrary evidence</a></div>
      </div>` : `
      <div class="shell">
        <div class="pe-head"><span class="pe-kicker">Lente penal · prueba antes de atribución</span><h2>Ocho paquetes probatorios — no una acusación colectiva.</h2><p class="pe-lead">Por Derecho pide a las autoridades competentes comprobar una hipótesis económico-penal conectada mediante documentos primarios finitos. El método es deliberadamente falsable: una explicación lícita o documento contrario que destruya una inferencia debe figurar junto a la prueba que la apoya.</p></div>
        <div class="pe-proof-rule"><strong>Atribución individual únicamente:</strong> acto → capacidad/autoridad → autoría/instrucción → conocimiento → intención cuando proceda → uso/confianza → perjuicio → beneficio → causalidad → corrección o continuación después del aviso. <strong>Relación no es responsabilidad.</strong></div>
        <div class="pe-grid">
          <article class="pe-card"><b>PKG-A · PP1041</b><strong>¿Quién autorizó el desistimiento presentado en nombre de LPB?</strong><span>Produzca instrucción, autor, poder, registro LexNET, audiencia de LPB, autoridad concursal y razón contemporánea de interés de la masa.</span></article>
          <article class="pe-card"><b>PKG-B · deuda → voto</b><strong>¿La deuda utilizada para afectar el voto estaba válidamente construida?</strong><span>Servicio, deudor legal, reparto, vencimiento, certificado, no duplicación, consecuencia electoral y uso externo posterior.</span></article>
          <article class="pe-card"><b>PKG-C · 7 junio</b><strong>¿Qué convirtió autoridad de seguridad en control material?</strong><span>Seguridad no autoriza por sí sola cerraduras, llaves, exclusión, intervención de fincas privadas, posesión, obras o explotación.</span></article>
          <article class="pe-card"><b>PKG-H · aviso → conducta</b><strong>¿Qué ocurrió después de cada aviso documentado?</strong><span>Proposición exacta, fuente, competencia, acto posterior, corrección/no corrección, beneficio y perjuicio causal.</span></article>
        </div>
        <div class="pe-reg"><div class="pe-stat"><strong>360</strong><span>registros REG-AGE en el snapshot analizado</span></div><div class="pe-stat"><strong>80</strong><span>etiquetas de destino</span></div><div class="pe-stat"><strong>319</strong><span>Recibido</span></div><div class="pe-stat"><strong>15</strong><span>Enviado</span></div><div class="pe-stat"><strong>26</strong><span>Rechazado</span></div></div>
        <div class="pe-limit"><strong>Límite del estado registral:</strong> ENVIADO ≠ ENTREGADO ≠ RECIBIDO ≠ ACUSADO ≠ UNIDO ≠ ADMITIDO ≠ INVESTIGADO ≠ ACEPTADO ≠ RESPALDADO ≠ PROBADO. El snapshot cubre 7 diciembre 2025–15 agosto 2026; es una capa de transmisión/cronología, no una decisión de fondo.</div>
        <div class="pe-actions"><a href="${mapHref}">Abrir el mapa de ocho paquetes →</a><a class="secondary" href="${correctionsHref}">Correcciones y prueba contraria</a></div>
      </div>`;
    const anchor = document.querySelector('.priority-band');
    const before = document.querySelector('#resumen-60-segundos');
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
      <h2>Reading control — scores are triage, not probability of guilt</h2>
      <p>Any numeric strength score on this page is an internal/public <strong>evidence-prioritisation indicator only</strong>. It is not a probability, judicial finding, criminal-liability score or statement that every legal element is established. Offence labels are investigative hypotheses requiring actor-specific proof.</p>
      <p>The current public-safe controlling map is <a href="${mapHref}">Eight mechanisms. Individual proof. No collective conviction →</a>. Contrary evidence and legitimate explanations must be given equal methodological access.</p>` : `
      <h2>Control de lectura — las puntuaciones son triaje, no probabilidad de culpabilidad</h2>
      <p>Cualquier puntuación numérica de fuerza en esta página es únicamente un <strong>indicador de priorización probatoria</strong>. No es una probabilidad, hallazgo judicial, puntuación de responsabilidad penal ni afirmación de que todos los elementos del tipo estén acreditados. Las etiquetas de delito son hipótesis investigativas que exigen prueba individual.</p>
      <p>El mapa público de control actual es <a href="${mapHref}">Ocho mecanismos. Prueba individual. Ninguna condena colectiva →</a>. La prueba contraria y las explicaciones legítimas deben tener el mismo acceso metodológico.</p>`;
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

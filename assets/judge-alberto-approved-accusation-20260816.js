(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const routes = {
    esCal: '/por-derecho/es/calificacion-concurso-36-2012-vidas-paralelas/',
    enCal: '/por-derecho/en/insolvency-classification-parallel-lives/',
    esJudge: '/por-derecho/es/concurso-36-2012-magistrado-juez/',
    esCourt: '/por-derecho/es/concurso-36-2012-juzgado-mercantil-1/',
    enJudge: '/por-derecho/en/insolvency-36-2012-mercantile-court-1/'
  };

  const isEs = path === routes.esCal || path === routes.esJudge || path === routes.esCourt;
  const isEn = path === routes.enCal || path === routes.enJudge;
  if (!isEs && !isEn) return;
  if (document.querySelector('[data-approved-judge-accusation-20260816]')) return;

  // Correct stale shorthand in the older opening without weakening the allegation.
  const replacements = isEs
    ? [['una vía financiada para intentar concluir el concurso', 'una vía estructurada y financiable para intentar concluir el concurso']]
    : [['a contemporaneously recorded financed route to seek conclusion of the insolvency', 'a contemporaneously recorded structured and financeable route to seek conclusion of the insolvency']];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach((node) => {
    let text = node.nodeValue;
    replacements.forEach(([from, to]) => { text = text.split(from).join(to); });
    if (text !== node.nodeValue) node.nodeValue = text;
  });

  const style = document.createElement('style');
  style.textContent = `
    .judge-approved{padding:2rem 0;background:#f4f1e8}
    .judge-approved-wrap{max-width:1080px;margin:0 auto}
    .judge-approved-grid{display:grid;grid-template-columns:minmax(260px,.72fr) minmax(0,1.55fr);gap:1.35rem;align-items:start}
    .judge-approved-photo{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:18px;overflow:hidden;position:sticky;top:1rem}
    .judge-approved-photo img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;object-position:center 42%}
    .judge-approved-photo figcaption{padding:.8rem .9rem;font-size:.82rem;line-height:1.35;color:#586267}
    .judge-approved-card{background:#101f26;color:#fff;border-radius:20px;padding:1.45rem 1.55rem;border-top:6px solid #8c2f2f}
    .judge-approved-card h2{font-size:clamp(1.85rem,3.7vw,2.8rem);line-height:1.06;margin:.35rem 0 1rem}
    .judge-approved-card p{line-height:1.62;margin:.82rem 0}
    .judge-approved-card strong{color:#fff}
    .judge-approved-kicker{font-size:.76rem;letter-spacing:.09em;text-transform:uppercase;font-weight:800;color:#ddc7a0}
    .judge-approved-core{font-size:1.12rem;border-left:5px solid #d8c38e;padding:.2rem 0 .2rem 1rem;margin:1rem 0 1.2rem}
    .judge-approved-boundary{margin-top:1.15rem;background:#fff;color:#13252d;border-radius:15px;padding:1rem 1.1rem}
    .judge-approved-boundary h3{margin:.1rem 0 .55rem;font-size:1.05rem}
    .judge-approved-boundary p{margin:.45rem 0;line-height:1.5}
    .judge-approved-actions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;margin-top:1rem}
    .judge-approved-actions article{background:#fff;color:#13252d;border-radius:14px;padding:.95rem;border:1px solid rgba(19,37,45,.14)}
    .judge-approved-actions h3{font-size:1rem;margin:0 0 .45rem}
    .judge-approved-actions p{font-size:.93rem;margin:0;line-height:1.45}
    .judge-approved-card a{color:#fff;text-decoration:underline}
    .judge-approved-note{font-size:.86rem;opacity:.82}
    @media(max-width:850px){.judge-approved-grid{grid-template-columns:1fr}.judge-approved-photo{position:static;max-width:620px}.judge-approved-actions{grid-template-columns:1fr}.judge-approved-card{border-radius:0}.judge-approved{padding-top:1rem}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.className = 'section judge-approved';
  section.dataset.approvedJudgeAccusation20260816 = '1';

  const photo = isEs
    ? `<figure class="judge-approved-photo"><img src="${asset('alberto-lopez-villarrubia-supplied-16aug2026.jpg')}" alt="Fotografía suministrada para la página de rendición de cuentas del magistrado Alberto López Villarrubia"><figcaption>Fotografía suministrada por Gil Marer para este expediente público. La identificación utilizada por Por Derecho procede del registro documental y de la atribución del suministrador, no de reconocimiento facial realizado por ChatGPT.</figcaption></figure>`
    : `<figure class="judge-approved-photo"><img src="${asset('alberto-lopez-villarrubia-supplied-16aug2026.jpg')}" alt="Photograph supplied for the accountability page concerning Magistrate-Judge Alberto López Villarrubia"><figcaption>Photograph supplied by Gil Marer for this public dossier. Por Derecho's identification comes from the documentary record and the supplier's attribution, not facial identification performed by ChatGPT.</figcaption></figure>`;

  if (isEs) {
    section.innerHTML = `<div class="shell judge-approved-wrap"><div class="judge-approved-grid">${photo}<div>
      <article class="judge-approved-card">
        <div class="judge-approved-kicker">MI ACUSACIÓN APROBADA · LENGUAJE CLARO · PREVARICACIÓN JUDICIAL ALEGADA</div>
        <h2>Acuso al magistrado Alberto López Villarrubia de convertir conscientemente un relato materialmente falso y selectivo en conclusiones judiciales punitivas contra mí.</h2>
        <p class="judge-approved-core"><strong>No sostengo simplemente que se equivocó.</strong> Mi acusación es que, cuando firmó la Sentencia 163/2023, el Juzgado llevaba años siendo confrontado con un registro que mostraba intentos de preservar LPB, mantener vivo el negocio hotelero, obtener financiación, pagar o aclarar las deudas, buscar una salida legal del concurso, impugnar deuda e intereses y proteger activos de LPB y de terceros frente a actores privados.</p>
        <p>En junio de 2018 existió además un intento documentado contemporáneamente de llevar al Juzgado una <strong>vía estructurada y financiable</strong> para pagar el pasivo concursal, devolver autonomía a LPB y continuar la explotación. Sostengo que ese historial es fundamentalmente incompatible con la imagen posterior de que yo simplemente obstruí, no colaboré, abandoné la empresa o agravé deliberadamente su insolvencia.</p>
        <p>Mi acusación es que el magistrado López Villarrubia no se limitó a no corregir el relato del Administrador Concursal. En la Sentencia 163/2023 <strong>adoptó selectivamente partes de ese relato como conclusiones judiciales propias</strong>, aunque la propia sentencia rechazó o redujo sustancialmente otras acusaciones importantes de la Administración Concursal y del Ministerio Fiscal.</p>
        <p>Impugno especialmente las conclusiones relativas a <strong>Pink Canary, las rentas no cobradas, la supuesta falta de colaboración, la causalidad del perjuicio concursal y la condena de €3.032.010,34</strong>. Exijo que esas conclusiones se coloquen junto al expediente completo y se reconstruyan línea por línea.</p>
        <p>Le acuso también de haber presidido un proceso en el que advertencias reiteradas sobre <strong>cálculo de deuda, titularidad de activos, control material del hotel, obras, liquidación, bienes de terceros, conducta del Administrador Concursal e intentos de rescate</strong> no recibieron, en mi acusación, el escrutinio y la protección judicial efectivos que requerían, mientras se permitía avanzar a decisiones con consecuencias cada vez más difíciles de revertir.</p>
        <p><strong>Mi acusación penal es de prevaricación judicial:</strong> sostengo que dictó a sabiendas una sentencia injusta. En lenguaje corriente, le acuso de saber que partes materiales del relato fáctico y causal que estaba adoptando no podían conciliarse justamente con el expediente que tenía ante sí y, aun así, firmar la sentencia e imponer consecuencias personales y patrimoniales graves.</p>
        <div class="judge-approved-boundary"><h3>Lo que esta acusación no pretende saltarse</h3><p>No afirmo que toda decisión adversa pruebe un delito, que cada documento del expediente fuera necesariamente leído personalmente por el magistrado, ni que estén probados corrupción, pago, connivencia o un acuerdo secreto con actores privados. Son proposiciones distintas y requieren prueba propia.</p><p><strong>Lo que sí sostengo es más preciso y más grave:</strong> creo que el expediente puede demostrar, proposición por proposición, que conocía suficiente realidad contraria como para que las conclusiones adversas que sobrevivieron en la Sentencia 163/2023 no puedan explicarse simplemente como un malentendido inocente.</p></div>
        <p>Esta acusación <strong>no ha sido establecida judicialmente</strong>. Es mi acusación. Pido que se contraste con el expediente certificado completo, la grabación y acta de la vista, los documentos efectivamente recibidos por el órgano judicial y la cronología de qué sabía el Juzgado y cuándo.</p>
        <p class="judge-approved-note">Referencia jurídica de la acusación: Código Penal, art. 446 — juez o magistrado que, <em>a sabiendas</em>, dicta sentencia o resolución injusta. <a href="https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444" rel="external noopener">Texto consolidado del BOE →</a></p>
      </article>
      <div class="judge-approved-actions">
        <article><h3>Umbral de prueba</h3><p>Conclusión judicial exacta → prueba primaria contraria → recepción/conocimiento → tratamiento u omisión → explicación alternativa → consecuencia.</p></article>
        <article><h3>Regla de la apelación</h3><p>La decisión de la Audiencia Provincial importa jurídicamente. Estratégicamente, sólo una exoneración sustantiva y limpia cerrará para Gil la cuestión de responsabilidad institucional de la AP.</p></article>
      </div>
    </div></div></div>`;
  } else {
    section.innerHTML = `<div class="shell judge-approved-wrap"><div class="judge-approved-grid">${photo}<div>
      <article class="judge-approved-card">
        <div class="judge-approved-kicker">MY APPROVED ACCUSATION · PLAIN ENGLISH · ALLEGED JUDICIAL PREVARICATION</div>
        <h2>I accuse Magistrate-Judge Alberto López Villarrubia of knowingly converting a materially false and selective insolvency narrative into punitive judicial findings against me.</h2>
        <p class="judge-approved-core"><strong>I am not simply saying that a judge got the case wrong.</strong> My accusation is that, by the time he signed Judgment 163/2023, the court had already been confronted over years with a record showing attempts to preserve LPB, keep the hotel business alive, obtain financing, pay or clarify debts, find a lawful exit from insolvency, challenge debt and interest calculations, and protect company and third-party assets from private actors.</p>
        <p>In June 2018 there was also a contemporaneously documented attempt to put before the court a <strong>structured and financeable route</strong> to pay the insolvency liabilities, restore LPB's independence and continue operating the hotel. I say that history is fundamentally incompatible with the later picture of me as someone who simply obstructed, failed to cooperate, abandoned the company or deliberately aggravated its insolvency.</p>
        <p>My accusation is that Judge López Villarrubia did not merely fail to correct the insolvency administrator's account. In Judgment 163/2023 he <strong>adopted selected parts of that account as his own judicial findings</strong>, even though other important accusations made by the insolvency administrator and the prosecutor were rejected or substantially narrowed by the judgment itself.</p>
        <p>I particularly challenge the findings concerning <strong>Pink Canary, unpaid rent, alleged non-cooperation, causation of insolvency damage and the €3,032,010.34 award</strong>. I say those findings must now be placed beside the complete documentary record and reconstructed line by line.</p>
        <p>I also accuse him, more broadly, of having presided over a process in which repeated warnings about <strong>debt calculation, asset ownership, physical control of the hotel, works, liquidation, third-party property, the conduct of the insolvency administrator and attempts to rescue the company</strong> did not receive, in my accusation, the effective judicial protection or scrutiny they required, while decisions with increasingly irreversible consequences were allowed to proceed.</p>
        <p><strong>My criminal allegation is judicial prevarication:</strong> that he knowingly issued an unjust judgment. In ordinary English, I am accusing him of knowing that material parts of the factual and causal case he was adopting could not fairly be reconciled with the record before the court, yet signing the judgment and imposing serious personal and financial consequences anyway.</p>
        <div class="judge-approved-boundary"><h3>What this accusation does not skip over</h3><p>I am not saying that every adverse decision proves a crime, that every document in the court file was necessarily personally read by him, or that I have proved corruption, payment, collusion or a secret agreement with private parties. Those are separate propositions requiring separate evidence.</p><p><strong>What I am saying is narrower and more serious:</strong> I believe the documentary record can show, proposition by proposition, that he knew enough about the contrary reality for the surviving adverse findings in Judgment 163/2023 not to be explained simply as an innocent misunderstanding.</p></div>
        <p>This accusation <strong>has not been judicially established</strong>. It is my accusation. I am asking for it to be tested against the complete certified court record, the hearing record, the documents actually received by the court and the chronology of what the court knew and when.</p>
        <p class="judge-approved-note">Legal reference for the allegation: Spanish Criminal Code, Article 446 — a judge or magistrate who <em>knowingly</em> issues an unjust judgment or resolution. <a href="https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444" rel="external noopener">Consolidated BOE text →</a></p>
      </article>
      <div class="judge-approved-actions">
        <article><h3>Proof threshold</h3><p>Exact judicial proposition → contrary primary evidence → receipt/knowledge → treatment or omission → alternative explanation → consequence.</p></article>
        <article><h3>Appeal rule</h3><p>The Audiencia Provincial decision matters legally. Strategically, only a substantively clean exoneration closes Gil's AP institutional-accountability question.</p></article>
      </div>
    </div></div></div>`;
  }

  const opening = document.querySelector('[data-calificacion-opening-20260816]');
  const hero = document.querySelector('main .hero');
  if (opening && opening.parentNode) opening.insertAdjacentElement('afterend', section);
  else if (hero) hero.insertAdjacentElement('afterend', section);
  else document.querySelector('main')?.prepend(section);

  function asset(filename) {
    const base = document.querySelector('script[src*="site.js"]')?.src || window.location.href;
    return new URL(filename, base).href;
  }
})();
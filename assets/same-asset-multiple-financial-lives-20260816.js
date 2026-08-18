(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const id = 'same-asset-multiple-financial-lives-16aug2026';
  const outreachId = 'same-asset-witness-outreach-16aug2026';
  const isEs = path.includes('/es/');
  const outreachTarget = /cadena-instrumentalizacion-ric-fondos-incentivos|institutionalisation-chain-ric-eu-incentives|acosta-matos-perimetro|acosta-matos-perimeter/.test(path);

  const insertOutreach = () => {
    if (!outreachTarget || document.getElementById(outreachId)) return;
    const main = document.querySelector('main');
    if (!main) return;

    const style = document.createElement('style');
    style.textContent = `
      #${outreachId}{background:#f4f1ea}
      #${outreachId} .witness-box{max-width:1080px;margin:0 auto}
      #${outreachId} .witness-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1rem 0}
      #${outreachId} .witness-card{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:16px;padding:1rem}
      #${outreachId} .witness-card h3{margin-top:0}
      #${outreachId} .witness-card a{display:inline-block;border-radius:999px;padding:.65rem 1rem;font-weight:750;text-decoration:none;background:#13252d;color:#fff}
      #${outreachId} .witness-rule{border-left:5px solid #8c6b2f;background:#f3efe4;border-radius:12px;padding:1rem 1.15rem}
      @media(max-width:850px){#${outreachId} .witness-grid{grid-template-columns:1fr}}
    `;
    document.head.appendChild(style);

    const section = document.createElement('section');
    section.id = outreachId;
    section.className = 'section alt';
    section.innerHTML = isEs ? `
      <div class="shell witness-box">
        <h2>Trabajadores, testigos e informantes: responsabilidad individual</h2>
        <p>Investigar empresas, financiación, propiedad, control o decisiones no convierte a sus trabajadores en responsables. Quien conoció hechos por su trabajo puede ayudar a confirmar, corregir o refutar esta cadena mediante conservación y comunicación lícitas.</p>
        <div class="witness-grid">
          <article class="witness-card"><h3>MYND / Canarian Hospitality</h3><p>Invitación a personal actual o anterior, separando expresamente empleo, conocimiento y responsabilidad individual.</p><a href="/por-derecho/es/carta-abierta-trabajadores-mynd-yaiza/">Carta a trabajadores MYND →</a></article>
          <article class="witness-card"><h3>Construcciones Acosta Matos</h3><p>Invitación a preservar información y utilizar cauces lícitos, sin atribuir responsabilidad por el mero vínculo laboral.</p><a href="/por-derecho/es/carta-abierta-trabajadores-acosta-matos/">Carta a trabajadores Acosta Matos →</a></article>
        </div>
        <p class="witness-rule"><strong>Regla:</strong> conocer no equivale a participar. Informar no autoriza extraer documentos, acceder ilícitamente a sistemas ni alterar pruebas. La responsabilidad debe probarse mediante actos propios.</p>
      </div>` : `
      <div class="shell witness-box">
        <h2>Workers, witnesses and informants: individual responsibility</h2>
        <p>Investigating companies, finance, property, control or decisions does not make their workers responsible. A person with relevant workplace knowledge may help confirm, correct or refute the chain through lawful preservation and reporting.</p>
        <div class="witness-grid">
          <article class="witness-card"><h3>MYND / Canarian Hospitality</h3><p>An invitation to current and former personnel, expressly separating employment, knowledge and individual responsibility.</p><a href="/por-derecho/en/open-letter-workers-mynd-yaiza/">Letter to MYND workers →</a></article>
          <article class="witness-card"><h3>Construcciones Acosta Matos</h3><p>An invitation to preserve information and use lawful channels, without attributing responsibility from employment alone.</p><a href="/por-derecho/en/open-letter-workers-acosta-matos/">Letter to Acosta Matos workers →</a></article>
        </div>
        <p class="witness-rule"><strong>Rule:</strong> knowledge is not participation. Reporting does not authorise taking documents, unlawfully accessing systems or altering evidence. Responsibility must be established through each person's own acts.</p>
      </div>`;
    main.insertAdjacentElement('beforeend', section);
  };

  insertOutreach();
  if (document.getElementById(id)) return;

  const dedicatedRecipientRoutes = [
    '/es/mismo-hotel-multiples-vidas-financieras/',
    '/en/same-hotel-multiple-financial-lives/',
    '/es/cnmv-ricpe-verificacion/',
    '/en/cnmv-ricpe-verification/',
    '/es/snca-fondos-europeos-trazabilidad/',
    '/en/snca-eu-funds-traceability/',
    '/es/incentivos-regionales-gc836-p06/',
    '/en/regional-incentives-gc836-p06/',
    '/es/ric-private-equity-sun-park/',
    '/en/ric-private-equity-sun-park/'
  ];
  if (dedicatedRecipientRoutes.some(route => path.endsWith(route))) return;

  const targets = [
    /\/por-derecho\/es\/?$/,
    /\/por-derecho\/en\/?$/,
    /calificacion-concurso-36-2012-vidas-paralelas|insolvency-classification-parallel-lives/,
    /ricpe-responsabilidad-documental|ricpe-documentary-accountability/,
    /cadena-instrumentalizacion-ric-fondos-incentivos|institutionalisation-chain-ric-eu-incentives/,
    /acosta-matos-perimetro|acosta-matos-perimeter/,
    /objetivos-recuperacion-restitucion|recovery-restitution-objectives/,
    /concurso-36-2012|lpb-insolvency/,
    /comunidad-instrumentalizacion|community-instrumentalisation/
  ];
  if (!targets.some(pattern => pattern.test(path))) return;

  const isCalificacion = /calificacion-concurso-36-2012-vidas-paralelas|insolvency-classification-parallel-lives/.test(path);
  const style = document.createElement('style');
  style.textContent = `
    #${id}{background:#f4f1ea}
    #${id} .same-asset-box{max-width:1120px;margin:0 auto}
    #${id} .same-asset-allegation{background:#3c1715;color:#fff;border-radius:20px;padding:1.3rem 1.45rem;box-shadow:0 12px 30px rgba(19,37,45,.12)}
    #${id} .same-asset-label{display:block;font-size:.76rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#f1c6be;margin-bottom:.55rem}
    #${id} h2{margin:.15rem 0 .75rem;color:#fff}
    #${id} .same-asset-lead{font-size:1.05rem;line-height:1.55;margin:.2rem 0 1rem}
    #${id} .same-asset-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem;margin:1rem 0}
    #${id} .same-asset-grid div{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:13px;padding:.8rem}
    #${id} .same-asset-grid strong{display:block;margin-bottom:.25rem}
    #${id} .same-asset-control{background:#fff;color:#13252d;border-radius:13px;padding:.9rem 1rem;margin:.9rem 0}
    #${id} .same-asset-control strong{color:#8c2f2c}
    #${id} .same-asset-actions{display:flex;gap:.65rem;flex-wrap:wrap;margin-top:1rem}
    #${id} .same-asset-actions a{display:inline-block;border-radius:999px;padding:.65rem 1rem;font-weight:750;text-decoration:none;background:#fff;color:#13252d}
    #${id} .same-asset-actions a.secondary{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.55)}
    @media(max-width:850px){#${id} .same-asset-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.id = id;
  section.className = 'section';
  const calEs = `<div class="same-asset-control"><strong>Por qué pertenece a la Calificación.</strong> Si se atribuye a Gil Marer la generación o agravación de la insolvencia, el análisis causal debe incluir las vidas posteriores del mismo hotel y determinar quién creó, preservó, desplazó o aprovechó valor.</div>`;
  const calEn = `<div class="same-asset-control"><strong>Why this belongs in the classification record.</strong> If Gil Marer is accused of generating or aggravating insolvency, causation must include the same hotel's later lives and identify who created, preserved, displaced or benefited from value.</div>`;

  section.innerHTML = isEs ? `
    <div class="shell same-asset-box"><div class="same-asset-allegation">
      <span class="same-asset-label">ALEGACIÓN UNITARIA · NO HALLAZGO JUDICIAL O AUDITOR</span>
      <h2>Mismo hotel, múltiples vidas financieras.</h2>
      <p class="same-asset-lead">Project Sun Rock alega doble o triple financiación y reutilización de una base sustancialmente coincidente —Hotel Sun Park/MYND Yaiza, activos, obras, costes, valor y empleo— entre el Concurso 36/2012, la Comunidad, RICPE/RIC, HNT, GC/836/P06, FEDER y la explotación actual. La separación jurídica no sustituye una conciliación finca por finca, factura por factura, empleo por empleo y euro por euro.</p>
      <div class="same-asset-grid">
        <div><strong>20 julio 2021</strong>Posición documentada dentro de RICPE: 54 CAM, 190 LPB y 18 terceros; titularidad condicionada y DD incompleta.</div>
        <div><strong>≈ €6,57m</strong>Folleto: €6.570.713,56. Reconstrucción separada de cuentas: €6.573.703,10. Diferencia €2.989,54 abierta.</div>
        <div><strong>€3.440.914,20 / 60</strong>Subvención y compromiso de empleo publicados en GC/836/P06.</div>
        <div><strong>FEDER</strong>Identificado; operación, porcentaje, gasto certificado, pago y controles pendientes.</div>
      </div>
      ${isCalificacion ? calEs : ''}
      <div class="same-asset-control"><strong>Estado de prueba.</strong> Alegación sustentada por anclajes documentales; no es resolución, auditoría cerrada ni condena. Las capas ≈€4,5m Comunidad, ≈€4,9m/≈86 empleos y ≈50 FTE siguen pendientes de fuente nativa o conciliación.</div>
      <div class="same-asset-actions"><a href="/por-derecho/es/mismo-hotel-multiples-vidas-financieras/">Abrir expediente unitario</a><a class="secondary" href="/por-derecho/es/ricpe-responsabilidad-documental/">Controles RICPE</a></div>
    </div></div>` : `
    <div class="shell same-asset-box"><div class="same-asset-allegation">
      <span class="same-asset-label">UNITARY ALLEGATION · NOT A JUDICIAL OR AUDIT FINDING</span>
      <h2>Same hotel, multiple financial lives.</h2>
      <p class="same-asset-lead">Project Sun Rock alleges double or triple funding and repeated use of a substantially overlapping base — the Sun Park/MYND Yaiza hotel, assets, works, costs, value and employment — across Insolvency 36/2012, the Community, RICPE/RIC, HNT, GC/836/P06, ERDF and current operation. Legal separation does not replace property-by-property, invoice-by-invoice, job-by-job and euro-by-euro reconciliation.</p>
      <div class="same-asset-grid">
        <div><strong>20 July 2021</strong>Position documented within RICPE: 54 CAM, 190 LPB and 18 third-party; conditional title and incomplete DD.</div>
        <div><strong>≈ €6.57m</strong>Prospectus: €6,570,713.56. Separate accounts reconstruction: €6,573,703.10. €2,989.54 difference open.</div>
        <div><strong>€3,440,914.20 / 60</strong>Published GC/836/P06 subsidy and employment commitment.</div>
        <div><strong>ERDF</strong>Identified; operation, rate, certified expenditure, payment and controls remain open.</div>
      </div>
      ${isCalificacion ? calEn : ''}
      <div class="same-asset-control"><strong>Evidence status.</strong> A substantiated allegation anchored in documents; not a decision, completed audit or conviction. The ≈€4.5m Community, ≈€4.9m/≈86-job and ≈50-FTE layers still require native sourcing or reconciliation.</div>
      <div class="same-asset-actions"><a href="/por-derecho/en/same-hotel-multiple-financial-lives/">Open unitary record</a><a class="secondary" href="/por-derecho/en/ricpe-documentary-accountability/">RICPE controls</a></div>
    </div></div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector(':scope > .dossier-hero, :scope > .cnmv-hero, :scope > .hero, :scope > section.hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else main.insertAdjacentElement('afterbegin', section);
})();
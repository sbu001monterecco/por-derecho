(() => {
  const path = window.location.pathname.replace(/\/+$/, '/') || '/';
  const fullRoutes = [
    '/en/lpb-solvency-record/',
    '/es/expediente-solvencia-lpb/',
    '/en/insolvency-classification-parallel-lives/',
    '/es/calificacion-concurso-36-2012-vidas-paralelas/'
  ];
  const compactRoutes = [
    '/en/recovery-restitution-objectives/',
    '/es/objetivos-recuperacion-restitucion/',
    '/en/insolvency-36-2012-insolvency-administrator/',
    '/es/concurso-36-2012-administrador-concursal/',
    '/en/insolvency-36-2012-institutional-accountability/',
    '/es/concurso-36-2012-responsabilidad-institucional/'
  ];
  const isFull = fullRoutes.some((route) => path.endsWith(route));
  const isCompact = !isFull && compactRoutes.some((route) => path.endsWith(route));
  if (!isFull && !isCompact) return;

  const isEs = path.includes('/es/');
  const siteBase = 'https://sbu001monterecco.github.io/por-derecho';
  const filingPdf = 'https://find-and-update.company-information.service.gov.uk/company/07716847/filing-history/MzUyMTkzNjc5NGFkaXF6a2N4/document?download=0&format=pdf';
  const filingHistory = 'https://find-and-update.company-information.service.gov.uk/company/07716847/filing-history';
  const accountsPage = isEs ? `${siteBase}/es/expediente-solvencia-lpb/` : `${siteBase}/en/lpb-solvency-record/`;
  const classificationPage = isEs ? `${siteBase}/es/calificacion-concurso-36-2012-vidas-paralelas/` : `${siteBase}/en/insolvency-classification-parallel-lives/`;

  const addStyles = () => {
    if (document.getElementById('aweswell-accounts-incorporation-styles')) return;
    const style = document.createElement('style');
    style.id = 'aweswell-accounts-incorporation-styles';
    style.textContent = `
      .aw-incorporation{--aw-ink:#13252d;--aw-gold:#c89432;--aw-green:#526b59;--aw-paper:#f6f2e8;--aw-red:#8b443c}
      .aw-incorporation .aw-shell{max-width:1120px;margin:0 auto}
      .aw-incorporation .aw-panel{border:1px solid rgba(19,37,45,.18);border-top:7px solid var(--aw-gold);border-radius:20px;background:#fff;padding:1.35rem 1.45rem;box-shadow:0 12px 34px rgba(19,37,45,.08)}
      .aw-incorporation .aw-eyebrow{font-size:.75rem;font-weight:900;letter-spacing:.085em;text-transform:uppercase;color:#6b5841;margin:0 0 .45rem}
      .aw-incorporation h2{margin:.1rem 0 .7rem;color:var(--aw-ink);font-size:clamp(1.65rem,3vw,2.45rem);line-height:1.1}
      .aw-incorporation .aw-lead{font-size:1.08rem;line-height:1.58;margin:.2rem 0 1rem}
      .aw-incorporation .aw-status{display:flex;flex-wrap:wrap;gap:.45rem;margin:.85rem 0 1.15rem;padding:0;list-style:none}
      .aw-incorporation .aw-status li{border-radius:999px;padding:.34rem .68rem;font-size:.69rem;font-weight:900;letter-spacing:.045em;text-transform:uppercase;background:#e7eee9;color:var(--aw-ink)}
      .aw-incorporation .aw-status li.pending{background:#f0dfdc;color:#6e302a}
      .aw-incorporation .aw-call{border-left:6px solid var(--aw-gold);background:var(--aw-paper);border-radius:14px;padding:1rem 1.15rem;margin:1rem 0}
      .aw-incorporation .aw-call strong{display:block;margin-bottom:.35rem;color:var(--aw-ink)}
      .aw-incorporation .aw-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.85rem;margin:1rem 0}
      .aw-incorporation .aw-card{border:1px solid rgba(19,37,45,.15);border-radius:14px;padding:1rem;background:#fff}
      .aw-incorporation .aw-card h3{margin:0 0 .45rem;color:var(--aw-ink);font-size:1.03rem}
      .aw-incorporation .aw-card p:last-child,.aw-incorporation .aw-card ol:last-child{margin-bottom:0}
      .aw-incorporation .aw-card ol{padding-left:1.25rem}
      .aw-incorporation .aw-boundary{background:#13252d;color:#fff;border-radius:14px;padding:1rem 1.15rem;margin:1rem 0}
      .aw-incorporation .aw-boundary strong{color:#f2dfb9}
      .aw-incorporation .aw-actions{display:flex;flex-wrap:wrap;gap:.55rem;margin-top:1rem}
      .aw-incorporation .aw-actions a{display:inline-block;border-radius:999px;padding:.66rem .9rem;text-decoration:none;font-weight:850;background:var(--aw-ink);color:#fff;border:1px solid var(--aw-ink)}
      .aw-incorporation .aw-actions a.secondary{background:#fff;color:var(--aw-ink)}
      .aw-incorporation .aw-small{font-size:.88rem;color:#555}
      .aw-incorporation.aw-compact .aw-panel{padding:1.1rem 1.2rem}
      .aw-incorporation.aw-compact h2{font-size:clamp(1.35rem,2.4vw,1.9rem)}
      @media(max-width:760px){.aw-incorporation .aw-grid{grid-template-columns:1fr}.aw-incorporation .aw-panel{padding:1.05rem}}
    `;
    document.head.appendChild(style);
  };

  const fullEnglish = `
    <div class="aw-panel" role="region" aria-labelledby="aw-incorporation-title">
      <p class="aw-eyebrow">AWESWELL · PARENT OF LPB · OFFICIAL UK FILING · CALIFICACIÓN</p>
      <h2 id="aw-incorporation-title">Formal evidential request: acknowledge, incorporate and expressly assess</h2>
      <p class="aw-lead">Por Derecho calls on the competent court and, where procedurally applicable, the Provincial Court hearing the pending calificación appeal to formally acknowledge the official Companies House filing of Aweswell Limited’s <em>Consolidated Provisional Group Statutory Accounts for the year ended 31 July 2025</em>; receive the filed English version, the Board-authorised Spanish translation, the filing record and the supporting board and accounting materials; incorporate them insofar as procedurally permissible; test them against the primary record and independent forensic accounting; and issue an express, reasoned determination on their procedural status, relevance, scope and probative weight.</p>
      <ul class="aw-status" aria-label="Current evidential status">
        <li>Officially filed in the UK</li>
        <li>Spanish version Board-authorised</li>
        <li>Incorporation requested</li>
        <li class="pending">Admissibility and weight pending</li>
      </ul>
      <div class="aw-call"><strong>The request is stronger and more precise than “accept the accounts”.</strong>It is a request to acknowledge the official filing, admit or otherwise incorporate it through the legally available route, assess it with the underlying evidence, and give reasons. If the proposed route is unavailable, the decision should identify the proper route through which the accounts, subsidiary records and independent expert reconstruction can be considered. Silent non-engagement is not a reasoned assessment.</div>
      <div class="aw-grid">
        <article class="aw-card"><h3>What the filing is relevant to</h3><p>Accounting conduct and access to records; Aweswell’s continuous parent, creditor and funding role; cooperation and non-abandonment; patrimonial coverage and date-specific liquidity; rescue and creditor-payment alternatives; productive-unit and platform value; causation; and the alleged generation or aggravation of insolvency.</p></article>
        <article class="aw-card"><h3>What the court is asked to determine</h3><ol><li>whether and under what procedural title the material enters the record;</li><li>the propositions for which it may properly be considered;</li><li>what primary or expert evidence is still required;</li><li>its relevance to the accounting, solvency and cooperation allegations;</li><li>whether the existing narrative should be confirmed, qualified, reconsidered or corrected; and</li><li>the proper alternative route if incorporation is refused.</li></ol></article>
        <article class="aw-card"><h3>Why it cannot be reduced to an irrelevant foreign document</h3><p>Aweswell is LPB’s UK parent and sole shareholder and records its asserted creditor, funding, foreign-investor and recovery roles. The filing was expressly prepared as a provisional parent-level statutory, accounting-continuity and rights-preservation record under materially constrained Spanish reporting conditions.</p></article>
        <article class="aw-card"><h3>Supporting evidential package</h3><p>The filing should be read with the historic accounts and ledgers, concurso asset-and-liability figures, definitive texts, the 100% convenio, financing efforts, professional valuations, operating and platform records, record-access requests, subsidiary-account preparation attempts, the Board resolution and an independent forensic-accounting report.</p></article>
      </div>
      <div class="aw-boundary"><strong>Strict boundary.</strong> This is not a request to treat Companies House as auditor or adjudicator, to accept every directors’ statement as proven, to replace LPB’s Spanish annual accounts, to establish title to every unit, or to reverse Sentencia 163/2023 by means of a foreign filing. The accounts are an official, dated and bilingual evidential anchor. Their propositions must be tested, not ignored.</div>
      <p class="aw-small"><strong>Controlled terminology:</strong> the filed title is reproduced accurately. For explanatory purposes, Por Derecho also describes the document as Aweswell’s filed provisional parent-level group accounts and continuity record, pending independent confirmation of the technical scope of “consolidated”.</p>
      <div class="aw-actions">
        <a href="${filingPdf}" rel="external noopener">Official Companies House PDF</a>
        <a class="secondary" href="${filingHistory}" rel="external noopener">Official filing history</a>
        <a class="secondary" href="${accountsPage}">Accounts and LPB solvency record</a>
        <a class="secondary" href="${classificationPage}">Calificación record</a>
      </div>
    </div>`;

  const fullSpanish = `
    <div class="aw-panel" role="region" aria-labelledby="aw-incorporation-title">
      <p class="aw-eyebrow">AWESWELL · MATRIZ DE LPB · PRESENTACIÓN OFICIAL EN REINO UNIDO · CALIFICACIÓN</p>
      <h2 id="aw-incorporation-title">Solicitud probatoria formal: reconocer, incorporar y valorar expresamente</h2>
      <p class="aw-lead">Por Derecho solicita al órgano judicial competente y, cuando resulte procesalmente procedente, a la Audiencia Provincial que conoce del recurso de apelación pendiente en materia de calificación, que reconozcan formalmente el depósito oficial en Companies House de las <em>Cuentas estatutarias consolidadas provisionales del grupo de Aweswell Limited correspondientes al ejercicio cerrado a 31 de julio de 2025</em>; que tengan por aportadas la versión inglesa oficialmente depositada, la traducción española autorizada por el Consejo, la constancia del depósito y la documentación societaria y contable de apoyo; que las incorporen por el cauce procesal disponible; que las contrasten con los documentos primarios y una pericial contable independiente; y que dicten un pronunciamiento expreso y motivado sobre su estatuto procesal, relevancia, alcance y valor probatorio.</p>
      <ul class="aw-status" aria-label="Estado probatorio actual">
        <li>Depositadas oficialmente en Reino Unido</li>
        <li>Versión española autorizada</li>
        <li>Incorporación solicitada</li>
        <li class="pending">Admisibilidad y valor pendientes</li>
      </ul>
      <div class="aw-call"><strong>La petición es más fuerte y precisa que pedir que las cuentas sean simplemente “aceptadas”.</strong>Se solicita reconocer el depósito oficial, admitirlas o incorporarlas por el cauce jurídicamente disponible, valorarlas junto con las pruebas subyacentes y razonar la decisión. Si el cauce propuesto no fuera posible, la resolución debe identificar la vía adecuada para examinar las cuentas, los registros de las filiales y la reconstrucción pericial independiente. El silencio no constituye una valoración motivada.</div>
      <div class="aw-grid">
        <article class="aw-card"><h3>Materias para las que son relevantes</h3><p>Conducta contable y acceso a registros; papel continuado de Aweswell como matriz, acreedor y financiador; colaboración y no abandono; cobertura patrimonial y liquidez por fechas; alternativas de convenio y pago a acreedores; valor de la unidad productiva y de la plataforma; causalidad; y alegada generación o agravación de la insolvencia.</p></article>
        <article class="aw-card"><h3>Pronunciamientos solicitados</h3><ol><li>si el material se incorpora y bajo qué título procesal;</li><li>respecto de qué proposiciones puede ser valorado;</li><li>qué prueba primaria o pericial adicional resulta necesaria;</li><li>su relevancia para las alegaciones contables, de solvencia y colaboración;</li><li>si el relato existente debe confirmarse, matizarse, reconsiderarse o corregirse; y</li><li>el cauce alternativo adecuado si se rechaza la incorporación.</li></ol></article>
        <article class="aw-card"><h3>Por qué no puede reducirse a un documento extranjero irrelevante</h3><p>Aweswell es la matriz británica y accionista único de LPB y deja constancia de sus posiciones reclamadas como acreedor, financiador, inversor extranjero y principal de recuperación. La presentación fue preparada expresamente como registro estatutario provisional, de continuidad contable y de preservación de derechos a nivel de matriz bajo condiciones españolas de información materialmente restringidas.</p></article>
        <article class="aw-card"><h3>Paquete probatorio de contraste</h3><p>La presentación debe leerse con las cuentas y libros históricos, las cifras concursales de activo y pasivo, los textos definitivos, el convenio del 100 %, los esfuerzos de financiación, las valoraciones profesionales, los registros de explotación y plataforma, las solicitudes de acceso, los intentos de formular cuentas de filiales, el acuerdo del Consejo y una pericial contable independiente.</p></article>
      </div>
      <div class="aw-boundary"><strong>Límite estricto.</strong> No se solicita tratar a Companies House como auditor o juzgador, aceptar sin prueba todas las manifestaciones de los administradores, sustituir las cuentas anuales españolas de LPB, acreditar la titularidad de todas las fincas ni revocar la Sentencia 163/2023 mediante una presentación extranjera. Las cuentas constituyen un anclaje probatorio oficial, fechado y bilingüe. Sus proposiciones deben contrastarse, no ignorarse.</div>
      <p class="aw-small"><strong>Terminología controlada:</strong> se reproduce fielmente el título depositado. A efectos explicativos, Por Derecho también lo describe como las cuentas provisionales de grupo presentadas a nivel de la matriz y su registro de continuidad, pendiente de confirmación independiente del alcance técnico del término «consolidadas».</p>
      <div class="aw-actions">
        <a href="${filingPdf}" rel="external noopener">PDF oficial de Companies House</a>
        <a class="secondary" href="${filingHistory}" rel="external noopener">Historial oficial de depósitos</a>
        <a class="secondary" href="${accountsPage}">Cuentas y expediente de solvencia de LPB</a>
        <a class="secondary" href="${classificationPage}">Expediente de calificación</a>
      </div>
    </div>`;

  const compactEnglish = `
    <div class="aw-panel" role="region" aria-labelledby="aw-incorporation-compact-title">
      <p class="aw-eyebrow">OFFICIAL AWESWELL FILING · FORMAL REQUEST OPEN</p>
      <h2 id="aw-incorporation-compact-title">Acknowledge, incorporate and expressly assess the parent-level accounts in the calificación</h2>
      <p>Por Derecho requests a reasoned procedural and evidential determination—not automatic acceptance as true. The official filing, Board-authorised Spanish version, supporting primary records and independent forensic accounting should be considered through the legally available route. If that route is refused, the proper alternative route should be identified expressly.</p>
      <div class="aw-actions"><a href="${accountsPage}">Open the full request</a><a class="secondary" href="${filingPdf}" rel="external noopener">Official filing</a></div>
    </div>`;

  const compactSpanish = `
    <div class="aw-panel" role="region" aria-labelledby="aw-incorporation-compact-title">
      <p class="aw-eyebrow">PRESENTACIÓN OFICIAL DE AWESWELL · SOLICITUD FORMAL ABIERTA</p>
      <h2 id="aw-incorporation-compact-title">Reconocer, incorporar y valorar expresamente las cuentas de la matriz en la calificación</h2>
      <p>Por Derecho solicita un pronunciamiento procesal y probatorio motivado, no una aceptación automática como verdad. El depósito oficial, la versión española autorizada por el Consejo, los documentos primarios y una pericial contable independiente deben examinarse por el cauce legalmente disponible. Si se rechaza dicho cauce, debe identificarse expresamente la vía alternativa adecuada.</p>
      <div class="aw-actions"><a href="${accountsPage}">Abrir la solicitud completa</a><a class="secondary" href="${filingPdf}" rel="external noopener">Depósito oficial</a></div>
    </div>`;

  const mount = () => {
    if (document.getElementById('aweswell-accounts-calificacion-incorporation')) return;
    const main = document.querySelector('main');
    if (!main) return;
    addStyles();
    const section = document.createElement('section');
    section.id = 'aweswell-accounts-calificacion-incorporation';
    section.className = `section aw-incorporation${isCompact ? ' aw-compact' : ''}`;
    section.innerHTML = `<div class="shell aw-shell">${isFull ? (isEs ? fullSpanish : fullEnglish) : (isEs ? compactSpanish : compactEnglish)}</div>`;
    const firstSection = Array.from(main.children).find((node) => node.tagName === 'SECTION');
    const thesis = main.querySelector('[data-calificacion-misuse-thesis]');
    if (thesis || firstSection) (thesis || firstSection).insertAdjacentElement('afterend', section);
    else main.prepend(section);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, { once: true });
  else mount();
  window.setTimeout(mount, 1200);
})();

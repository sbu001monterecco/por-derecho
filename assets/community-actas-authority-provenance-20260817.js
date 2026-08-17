(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/+$/, '/');
  const isES = path.includes('/es/');
  const lang = isES ? 'es' : 'en';

  const routes = {
    esHub: '/por-derecho/es/comunidad-instrumentalizacion/',
    enHub: '/por-derecho/en/community-instrumentalisation/',
    esActas: '/por-derecho/es/comunidad-instrumentalizacion/actas-2011-2022/',
    enActas: '/por-derecho/en/community-instrumentalisation/minutes-2011-2022/'
  };

  const onHub = path === routes.esHub || path === routes.enHub;
  const onActas = path === routes.esActas || path === routes.enActas;

  const relevantContextRoutes = [
    '/por-derecho/es/toma-control-sun-park-7-junio-2018/',
    '/por-derecho/en/sun-park-takeover-7-june-2018/',
    '/por-derecho/es/concurso-36-2012-administrador-concursal/',
    '/por-derecho/en/insolvency-36-2012-insolvency-administrator/',
    '/por-derecho/es/calificacion-concurso-36-2012-vidas-paralelas/',
    '/por-derecho/en/insolvency-classification-parallel-lives/',
    '/por-derecho/es/acosta-matos-perimetro/',
    '/por-derecho/en/acosta-matos-perimeter/',
    '/por-derecho/es/ricpe-responsabilidad-documental/',
    '/por-derecho/en/ricpe-documentary-accountability/',
    '/por-derecho/es/mismo-hotel-multiples-vidas-financieras/',
    '/por-derecho/en/same-hotel-multiple-financial-lives/',
    '/por-derecho/es/yaiza-trazabilidad-institucional/',
    '/por-derecho/en/yaiza-institutional-traceability/',
    '/por-derecho/es/cabildo-lanzarote-turismo-trazabilidad/',
    '/por-derecho/en/cabildo-lanzarote-tourism-traceability/'
  ];
  const onContextRoute = relevantContextRoutes.includes(path);

  if (!onHub && !onActas && !onContextRoute) return;

  const source = {
    alimarket: 'https://www.alimarket.es/hoteles/noticia/m3292003/monte-lanza-vende-el-aparthotel--sun-park--a-la-inversora-israeli-multimatrix',
    acta20080429: 'https://drive.google.com/file/d/1Ups4s_2TcHyCByxSiK-WIx-ieEdciVbe/view?usp=drivesdk',
    cexp200805: 'https://drive.google.com/file/d/1CEJLnY3r5kM_WBk6YWiZjIalNlCfeToA/view?usp=drivesdk',
    acta20160426: 'https://drive.google.com/file/d/1YMnEVDQj7r1E2aWgWL2Ne9b5gYP6ZRbd/view?usp=drivesdk',
    acta20180518: 'https://drive.google.com/file/d/16j_xD-lvEbtR-_23_8nIS2bOkRn4SFr8/view?usp=drivesdk'
  };

  const copy = {
    es: {
      originKicker: 'Prólogo documental · 2008 antes del punto de ruptura de 2011',
      originTitle: 'Antes de discutir quién podía decidir, hay que mostrar qué se vendía y cómo se organizó la explotación.',
      originLead: 'El registro contemporáneo de 2008 y los instrumentos primarios sitúan el punto de partida: Sun Park se presentaba al mercado como una operación hotelera transferida al perímetro Multimatrix, mientras la propiedad seguía estructurada finca por finca y la explotación se articulaba mediante CEXP. Esa diferencia explica por qué una mayoría dominical no equivale automáticamente a autoridad universal de una Comunidad.',
      pressBadge: 'Fuente contemporánea independiente',
      pressTitle: '16 julio 2008 · Alimarket anuncia Monte Lanza → Multimatrix',
      pressText: 'Alimarket comunicó que Monte Lanza había alcanzado en junio de 2008 un acuerdo con el inversor israelí Multimatrix sobre la propiedad y explotación de Sun Park. Es un punto de referencia sobre lo que se comunicó al mercado; no prueba por sí solo que cada finca se transmitiera ni que cada vendedor cumpliera todas sus obligaciones.',
      correctionBadge: 'Corrección de entidades',
      correctionTitle: 'LPB y CEXP deben nombrarse con precisión',
      correctionText: 'Cuando la identidad jurídica importa, LPB es Luchy Playa Blanca, S.L.U. La descripción periodística de CEXP como “S.L.” no gobierna: los estatutos primarios de mayo de 2008 describen a los propietarios participantes constituyendo una “comunidad civil” para la explotación. CEXP, la Comunidad de Propietarios y LPB no son una sola entidad.',
      minorityBadge: 'Hipótesis abierta · no elevar a hecho',
      minorityTitle: 'El perímetro minoritario / “c.23%” necesita un mapa vendedor-finca',
      minorityText: 'La tesis del proyecto es que una minoría —descrita históricamente como circa 23%— no completó o incumplió la venta prevista y que después esa fractura alimentó conflictos de explotación, deuda, voto y autoridad. El porcentaje y el incumplimiento contractual deben cerrarse vendedor por vendedor y finca por finca. Hasta entonces, la formulación pública correcta es una minoría o aproximadamente una cuarta parte pendiente de reconciliación documental.',
      sourceButtons: ['Alimarket 2008', 'Acta 29-abr-2008', 'Estatutos/CEXP mayo 2008'],
      matrixTitle: 'ORIGEN DE AUTORIDAD CONTROVERTIDO — 22 JUNIO 2011',
      matrixIntro: 'No pedimos al lector que acepte la palabra “fabricación”. Separamos lo que registra el documento, la alegación de Gil Marer, el estado procesal adverso y la prueba que aún falta.',
      verified: 'VERIFICADO EN EL REGISTRO',
      allegation: 'ALEGACIÓN DE GIL MARER',
      legal: 'ESTADO / PRUEBA ADVERSA',
      open: 'PRUEBA ABIERTA',
      verifiedText: 'La cronología controlada registra una gran cuota LPB, deuda comunitaria atribuida, exclusión de voto, decisiones por el grupo habilitado y oposición LPB. Cada porcentaje debe citarse con su propio documento y denominador.',
      allegationText: 'Gil Marer sostiene que esa combinación produjo una base de autoridad materialmente falsa o inválida que luego se propagó. Es una alegación investigable; no se publica como condena ni como falsedad penal establecida.',
      legalText: 'Los acuerdos de 2011 fueron impugnados y existen resultados procesales adversos a LPB que deben publicarse. Un resultado sobre impugnación o cautelares no convierte automáticamente en correcta cada cifra de deuda, cada certificación ni cada uso posterior.',
      openText: 'Libro original, convocatorias, poderes, audio, cálculo finca por finca de la deuda, servicio/notificación y cadena de transmisión/uso posterior.',
      authorityLabel: 'Autoridad / procedencia',
      sourceLabel: 'Fuente primaria',
      directSource: 'Abrir fuente',
      restrictedSource: 'Copia primaria controlada · enlace público no fijado en este pase',
      acta2016Authority: 'La propia acta de 2016 remite expresamente a los pleitos sobre las juntas de 2-feb y 22-jun-2011. Registra 89,727% representado, LPB 72,976% y sólo 11,039% con voto. Esto conecta documentalmente el marco 2011 con deuda, cuentas, certificados y reclamaciones posteriores.',
      acta2018Authority: 'El acta primaria registra 86,715% representado, LPB 72,976%, CAM 13,034% y sólo 0,385% con voto; el punto de seguridad/acceso llega a la junta a petición de LPB representada por el AC. No es, por su texto facial, una entrega judicial de todo el hotel a CAM.',
      no2019: 'Control negativo: no se ha localizado un acta comunitaria de 2019 en el conjunto revisado. El Auto de 24-oct-2019 es un acto judicial y no debe convertirse retroactivamente en “acta” o consentimiento comunitario.',
      acta2022Authority: 'Nodo de autoridad/proyecto: la página controla una acta de 4-feb-2022 con roles concentrados de presidencia, proyecto, representación, administración/banco y deuda. Antes de publicar un botón de fuente directa, debe recuperarse de nuevo el ID exacto del original y reconciliar acta/audio/anexos, título, voto, conflicto y pagos.',
      contextTitle: '¿De dónde venía la autoridad invocada?',
      contextText: 'Este episodio no debe leerse aislado. El dossier de actas reconstruye la cadena 2008 → 2011 → 2016 → 2018 → 2022 y separa cuota dominical, derecho de voto, deuda atribuida, seguridad/acceso y título independiente. Use el acta concreta como fuente de procedencia, no como sustituto de prueba del resultado posterior.',
      contextButton: 'Abrir cadena de actas y autoridad'
    },
    en: {
      originKicker: 'Documentary prologue · 2008 before the 2011 rupture point',
      originTitle: 'Before asking who could decide, show what was being sold and how operation was organised.',
      originLead: 'The contemporary 2008 record and primary instruments establish the starting point: Sun Park was presented to the market as a hotel operation transferred into the Multimatrix perimeter while title remained divided property by property and operation was organised through CEXP. That distinction explains why a majority ownership share does not automatically become universal Community authority.',
      pressBadge: 'Independent contemporary source',
      pressTitle: '16 July 2008 · Alimarket reports Monte Lanza → Multimatrix',
      pressText: 'Alimarket reported that Monte Lanza had reached a June-2008 agreement with Israeli investor Multimatrix concerning Sun Park property and operation. It is evidence of what the specialist market was told; it does not by itself prove that every property was conveyed or that every seller completed every obligation.',
      correctionBadge: 'Entity correction',
      correctionTitle: 'LPB and CEXP must be identified precisely',
      correctionText: 'Where exact legal identity matters, LPB is Luchy Playa Blanca, S.L.U. The press description of CEXP as an “S.L.” does not control: the primary May-2008 statutes describe participating owners constituting a “comunidad civil” for operation. CEXP, the Owners’ Community and LPB are not one legal entity.',
      minorityBadge: 'Open hypothesis · do not upgrade',
      minorityTitle: 'The minority / “c.23%” perimeter requires a seller-by-property map',
      minorityText: 'The project position is that a minority —historically described as circa 23%— did not complete or breached the contemplated sale and that the fracture later fed operation, debt, voting and authority disputes. The percentage and breach characterisation must be proved seller by seller and property by property. Until then, the public-safe description is a minority or approximately one-quarter perimeter requiring documentary reconciliation.',
      sourceButtons: ['Alimarket 2008', '29-Apr-2008 minutes', 'May-2008 CEXP statutes'],
      matrixTitle: 'DISPUTED ORIGIN OF AUTHORITY — 22 JUNE 2011',
      matrixIntro: 'The reader is not asked to accept the word “fabrication”. The site separates what the record says, Gil Marer’s allegation, adverse procedural status and the evidence still required.',
      verified: 'VERIFIED IN THE RECORD',
      allegation: 'GIL MARER’S ALLEGATION',
      legal: 'STATUS / ADVERSE EVIDENCE',
      open: 'OPEN EVIDENCE',
      verifiedText: 'The controlled chronology records a very large LPB ownership share, attributed Community debt, voting exclusion, decisions by the vote-qualified pool and LPB objection. Each percentage must be tied to its own document and denominator.',
      allegationText: 'Gil Marer alleges that this combination produced a materially false or invalid basis of authority that later propagated. That is an investigable allegation; it is not published as a conviction or established criminal falsity.',
      legalText: 'The 2011 resolutions were challenged and there are procedural outcomes adverse to LPB that must remain visible. An outcome on challenge/interim relief does not automatically validate every later debt figure, certificate or downstream use.',
      openText: 'Original minute book, notices, proxies, audio, property-by-property debt calculation, service/notification and the later transmission/reliance chain.',
      authorityLabel: 'Authority / provenance',
      sourceLabel: 'Primary source',
      directSource: 'Open source',
      restrictedSource: 'Controlled primary copy · no public source link fixed in this pass',
      acta2016Authority: 'The 2016 minute itself expressly recounts the litigation over the 2-Feb and 22-Jun-2011 meetings. It records 89.727% represented, LPB 72.976% and only 11.039% vote-qualified, creating a documentary bridge from the 2011 framework into later accounts, debt, certificates and claims.',
      acta2018Authority: 'The primary minute records 86.715% represented, LPB 72.976%, CAM 13.034% and only 0.385% vote-qualified; security/access was brought to the meeting at LPB’s request through the insolvency administrator. On its face it is not a judicial delivery of the whole hotel to CAM.',
      no2019: 'Negative-evidence control: no 2019 Community minutes have been located in the reviewed source set. The 24-Oct-2019 non-validation order is a judicial act and must not be turned retroactively into Community minutes or consent.',
      acta2022Authority: 'Authority/project node: the controlled page records 4-Feb-2022 minutes with concentrated roles across presidency, project, representation, administration/banking and debt. Before adding a direct-source button, re-recover the exact primary ID and reconcile the minutes/audio/annexes, title, voting, conflict and payments.',
      contextTitle: 'Where did the asserted authority come from?',
      contextText: 'This episode should not be read in isolation. The minutes dossier reconstructs the 2008 → 2011 → 2016 → 2018 → 2022 chain and separates ownership share, voting entitlement, attributed debt, security/access and independent title. Use the precise minutes as provenance evidence, not as a substitute for proof of the later result.',
      contextButton: 'Open minutes and authority chain'
    }
  }[lang];

  const style = document.createElement('style');
  style.textContent = `
    .sp-origin-provenance{border-top:1px solid rgba(20,50,58,.16);border-bottom:1px solid rgba(20,50,58,.16)}
    .sp-origin-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;margin-top:1.4rem}
    .sp-origin-card{padding:1.15rem;border:1px solid rgba(20,50,58,.16);border-radius:18px;background:rgba(255,255,255,.72);box-shadow:0 12px 32px rgba(16,40,48,.06)}
    .sp-origin-card h3{margin:.6rem 0 .55rem;font-size:1.08rem;line-height:1.3}.sp-origin-card p{margin:.45rem 0}
    .sp-source-actions{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:1rem}
    .sp-matrix-provenance{margin:1rem 0 1.5rem;padding:1.2rem;border:2px solid rgba(132,62,43,.38);border-radius:20px;background:linear-gradient(135deg,rgba(255,248,242,.96),rgba(255,255,255,.96))}
    .sp-matrix-provenance h3{margin:.25rem 0 .5rem}.sp-matrix-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.75rem;margin-top:1rem}
    .sp-matrix-grid>div{padding:.9rem;border-radius:14px;background:#fff;border:1px solid rgba(20,50,58,.13)}
    .sp-matrix-grid strong{display:block;font-size:.78rem;letter-spacing:.04em;margin-bottom:.35rem}.sp-matrix-grid span{font-size:.92rem;line-height:1.45}
    .sp-row-provenance{margin-top:.75rem;padding:.7rem .8rem;border-left:4px solid rgba(25,86,102,.55);background:rgba(240,247,249,.72);font-size:.9rem;line-height:1.45}
    .sp-row-provenance strong{display:block;margin-bottom:.25rem}.sp-row-provenance .sp-inline-source{display:inline-block;margin-top:.35rem;font-weight:700}
    .sp-context-bridge{margin:1rem auto 1.5rem;max-width:1180px;padding:1rem 1.1rem;border-radius:18px;border:1px solid rgba(20,50,58,.18);background:linear-gradient(135deg,rgba(238,247,249,.96),rgba(255,255,255,.96))}
    .sp-context-bridge h2,.sp-context-bridge h3{margin:.1rem 0 .45rem}.sp-context-bridge p{margin:.35rem 0 .7rem}
    .sp-evidence-id{display:inline-block;margin-top:.35rem;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.75rem;opacity:.74}
    @media(max-width:900px){.sp-origin-grid,.sp-matrix-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const actaHref = isES
    ? '/por-derecho/es/comunidad-instrumentalizacion/actas-2011-2022/'
    : '/por-derecho/en/community-instrumentalisation/minutes-2011-2022/';

  function originSection() {
    const section = document.createElement('section');
    section.className = 'section alt sp-origin-provenance';
    section.id = 'origen-2008-autoridad';
    section.innerHTML = `
      <div class="shell">
        <div class="section-head">
          <div><p class="kicker">${copy.originKicker}</p><h2>${copy.originTitle}</h2></div>
          <p>${copy.originLead}</p>
        </div>
        <div class="sp-origin-grid">
          <article class="sp-origin-card">
            <span class="evidence-badge document">${copy.pressBadge}</span>
            <h3>${copy.pressTitle}</h3>
            <p>${copy.pressText}</p>
            <span class="sp-evidence-id">SP-PRESS-2008-07-16</span>
          </article>
          <article class="sp-origin-card">
            <span class="evidence-badge correction">${copy.correctionBadge}</span>
            <h3>${copy.correctionTitle}</h3>
            <p>${copy.correctionText}</p>
            <span class="sp-evidence-id">SP-ACTA-2008-04-29 · SP-CEXP-2008-05</span>
          </article>
          <article class="sp-origin-card">
            <span class="evidence-badge question-badge">${copy.minorityBadge}</span>
            <h3>${copy.minorityTitle}</h3>
            <p>${copy.minorityText}</p>
            <span class="sp-evidence-id">OPEN: seller/finca completion map</span>
          </article>
        </div>
        <div class="sp-source-actions">
          <a class="button secondary" href="${source.alimarket}" rel="external noopener">${copy.sourceButtons[0]}</a>
          <a class="button secondary" href="${source.acta20080429}" rel="external noopener">${copy.sourceButtons[1]}</a>
          <a class="button secondary" href="${source.cexp200805}" rel="external noopener">${copy.sourceButtons[2]}</a>
          ${onHub ? `<a class="button" href="${actaHref}#sp-acta-2011-06-22">${copy.contextButton}</a>` : ''}
        </div>
      </div>`;
    return section;
  }

  function findChronologySection() {
    return document.querySelector('#cronologia') || document.querySelector('#chronology');
  }

  function insertOrigin() {
    const main = document.querySelector('main');
    if (!main || document.querySelector('#origen-2008-autoridad')) return;
    const target = onActas
      ? (document.querySelector('#perimetro') || document.querySelector('#perimeter') || findChronologySection())
      : (document.querySelector('#resumen') || document.querySelector('#summary') || main.querySelector('.section'));
    if (target) target.parentNode.insertBefore(originSection(), target);
    else main.appendChild(originSection());
  }

  function tagRowsAndAddProvenance() {
    if (!onActas) return;
    const rows = Array.from(document.querySelectorAll('table.document-status tbody tr'));
    if (!rows.length) return;

    const matchRow = (needles) => rows.find(row => needles.some(n => row.textContent.toLowerCase().includes(n.toLowerCase())));

    const r2011 = matchRow(isES ? ['22 junio 2011'] : ['22 june 2011']);
    const r2016 = matchRow(isES ? ['26 abril 2016'] : ['26 april 2016']);
    const r2018 = matchRow(isES ? ['18 mayo 2018'] : ['18 may 2018']);
    const r2019 = matchRow(['2019']);
    const r2022 = matchRow(isES ? ['4 febrero 2022'] : ['4 february 2022']);

    if (r2011) {
      r2011.id = 'sp-acta-2011-06-22';
      const box = document.createElement('div');
      box.className = 'sp-matrix-provenance';
      box.innerHTML = `
        <span class="evidence-badge representation-badge">SP-ACTA-2011-06-22</span>
        <h3>${copy.matrixTitle}</h3>
        <p>${copy.matrixIntro}</p>
        <div class="sp-matrix-grid">
          <div><strong>${copy.verified}</strong><span>${copy.verifiedText}</span></div>
          <div><strong>${copy.allegation}</strong><span>${copy.allegationText}</span></div>
          <div><strong>${copy.legal}</strong><span>${copy.legalText}</span></div>
          <div><strong>${copy.open}</strong><span>${copy.openText}</span></div>
        </div>`;
      const tableWrap = r2011.closest('.control-table-wrap') || r2011.closest('section');
      if (tableWrap && !document.querySelector('.sp-matrix-provenance')) tableWrap.parentNode.insertBefore(box, tableWrap);
    }

    const append = (row, id, text, href) => {
      if (!row) return;
      row.id = id;
      const cell = row.cells && row.cells.length ? row.cells[row.cells.length - 1] : null;
      if (!cell || cell.querySelector('.sp-row-provenance')) return;
      const note = document.createElement('div');
      note.className = 'sp-row-provenance';
      note.innerHTML = `<strong>${copy.authorityLabel}</strong>${text}${href ? `<br><a class="sp-inline-source" href="${href}" rel="external noopener">${copy.sourceLabel}: ${copy.directSource} →</a>` : `<br><span class="sp-inline-source">${copy.restrictedSource}</span>`}<br><span class="sp-evidence-id">${id.toUpperCase().replace('SP-ACTA-','SP-ACTA-')}</span>`;
      cell.appendChild(note);
    };

    append(r2016, 'sp-acta-2016-04-26', copy.acta2016Authority, source.acta20160426);
    append(r2018, 'sp-acta-2018-05-18', copy.acta2018Authority, source.acta20180518);
    append(r2019, 'sp-no-acta-2019', copy.no2019, null);
    append(r2022, 'sp-acta-2022-02-04', copy.acta2022Authority, null);
  }

  function insertContextBridge() {
    if (!onContextRoute || document.querySelector('.sp-context-bridge')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const hero = main.querySelector('.dossier-hero');
    const bridge = document.createElement('aside');
    bridge.className = 'sp-context-bridge';
    bridge.innerHTML = `
      <span class="evidence-badge document">2008 → 2011 → 2016 → 2018 → 2022</span>
      <h3>${copy.contextTitle}</h3>
      <p>${copy.contextText}</p>
      <a class="button secondary" href="${actaHref}#sp-acta-2011-06-22">${copy.contextButton} →</a>`;
    if (hero && hero.nextSibling) hero.parentNode.insertBefore(bridge, hero.nextSibling);
    else main.insertBefore(bridge, main.firstChild);
  }

  function updateDocumentMetadata() {
    if (!onActas) return;
    if (isES) {
      document.title = 'Actas Sun Park 2011–2022 con origen 2008 — deuda, voto y autoridad';
    } else {
      document.title = 'Sun Park minutes 2011–2022 with 2008 origin — debt, voting and authority';
    }
  }

  const run = () => {
    insertOrigin();
    tagRowsAndAddProvenance();
    insertContextBridge();
    updateDocumentMetadata();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
})();
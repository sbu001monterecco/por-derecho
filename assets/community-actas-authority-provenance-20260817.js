(() => {
  'use strict';

  const rawPath = window.location.pathname.replace(/\/+$/, '');
  const ends = suffix => rawPath.endsWith(suffix.replace(/\/+$/, ''));
  const isES = rawPath.includes('/es/');
  const lang = isES ? 'es' : 'en';

  const onHub = ends('/es/comunidad-instrumentalizacion') || ends('/en/community-instrumentalisation');
  const onActas = ends('/es/comunidad-instrumentalizacion/actas-2011-2022') || ends('/en/community-instrumentalisation/minutes-2011-2022');

  const contextSuffixes = [
    '/es/toma-control-sun-park-7-junio-2018',
    '/en/sun-park-takeover-7-june-2018',
    '/es/concurso-36-2012-administrador-concursal',
    '/en/insolvency-36-2012-insolvency-administrator',
    '/es/calificacion-concurso-36-2012-vidas-paralelas',
    '/en/insolvency-classification-parallel-lives',
    '/es/acosta-matos-perimetro',
    '/en/acosta-matos-perimeter',
    '/es/ricpe-responsabilidad-documental',
    '/en/ricpe-documentary-accountability',
    '/es/mismo-hotel-multiples-vidas-financieras',
    '/en/same-hotel-multiple-financial-lives',
    '/es/yaiza-trazabilidad-institucional',
    '/en/yaiza-institutional-traceability',
    '/es/cabildo-lanzarote-turismo-trazabilidad',
    '/en/cabildo-lanzarote-tourism-traceability'
  ];
  const onContextRoute = contextSuffixes.some(ends);

  if (!onHub && !onActas && !onContextRoute) return;

  const alimarket = 'https://www.alimarket.es/hoteles/noticia/m3292003/monte-lanza-vende-el-aparthotel--sun-park--a-la-inversora-israeli-multimatrix';
  const actaHref = isES
    ? '/por-derecho/es/comunidad-instrumentalizacion/actas-2011-2022/#sp-acta-2011-06-22'
    : '/por-derecho/en/community-instrumentalisation/minutes-2011-2022/#sp-acta-2011-06-22';

  const t = {
    es: {
      originKicker: 'Prólogo documental · 2008 antes del punto de ruptura de 2011',
      originTitle: 'Antes de discutir quién podía decidir, hay que mostrar qué se vendía y cómo se organizó la explotación.',
      originLead: 'El registro contemporáneo de 2008 y los instrumentos primarios sitúan el punto de partida: Sun Park se presentaba al mercado como una operación hotelera transferida al perímetro Multimatrix, mientras la titularidad seguía estructurada finca por finca y la explotación se articulaba mediante CEXP. Unidad hotelera, titularidad, Comunidad de Propietarios, CEXP y LPB son planos distintos.',
      pressBadge: 'Fuente contemporánea independiente',
      pressTitle: '16 julio 2008 · Alimarket anuncia Monte Lanza → Multimatrix',
      pressText: 'Alimarket comunicó que Monte Lanza había alcanzado en junio de 2008 un acuerdo con el inversor israelí Multimatrix sobre la propiedad y explotación de Sun Park. Es prueba de lo comunicado al mercado; no prueba por sí sola que cada finca se transmitiera ni que cada vendedor cumpliera todas sus obligaciones.',
      correctionBadge: 'Corrección de entidades',
      correctionTitle: 'LPB y CEXP deben nombrarse con precisión',
      correctionText: 'Cuando la identidad jurídica importa, LPB es Luchy Playa Blanca, S.L.U. La descripción periodística de CEXP como “S.L.” no gobierna: los estatutos primarios de mayo de 2008 describen a los propietarios participantes constituyendo una “comunidad civil” para la explotación. CEXP no debe confundirse con la Comunidad de Propietarios ni con LPB.',
      minorityBadge: 'Hipótesis abierta · no elevar a hecho',
      minorityTitle: 'El perímetro minoritario / “c.23%” necesita un mapa vendedor-finca',
      minorityText: 'La tesis del proyecto es que una minoría —descrita históricamente como circa 23%— no completó o incumplió la venta prevista y que esa fractura alimentó conflictos posteriores de explotación, deuda, voto y autoridad. El porcentaje y el incumplimiento contractual deben cerrarse vendedor por vendedor y finca por finca. Hasta entonces: minoría o aproximadamente una cuarta parte pendiente de reconciliación documental.',
      publicSource: 'Abrir Alimarket 2008',
      privateSource: 'Fuente primaria controlada · copia pública expurgada pendiente',
      chainButton: 'Abrir cadena completa de actas y autoridad',
      matrixTitle: 'ORIGEN DE AUTORIDAD CONTROVERTIDO — 22 JUNIO 2011',
      matrixIntro: 'La página no pide aceptar la palabra “fabricación”. Separa lo que registra el documento, la alegación de Gil Marer, el estado procesal adverso y la prueba que todavía falta.',
      verified: 'VERIFICADO EN EL REGISTRO',
      allegation: 'ALEGACIÓN DE GIL MARER',
      legal: 'ESTADO / PRUEBA ADVERSA',
      open: 'PRUEBA ABIERTA',
      verifiedText: 'La cronología controlada registra una gran cuota LPB, deuda comunitaria atribuida, exclusión de voto, decisiones por el grupo habilitado y oposición LPB. Cada porcentaje debe citarse con su propio documento y denominador.',
      allegationText: 'Gil Marer sostiene que esa combinación produjo una base de autoridad materialmente falsa o inválida que luego se propagó. Es una alegación investigable; no una condena ni una falsedad penal establecida.',
      legalText: 'Los acuerdos de 2011 fueron impugnados y existen resultados procesales adversos a LPB que deben permanecer visibles. Esos resultados no convierten automáticamente en correcta cada deuda, certificado o uso posterior.',
      openText: 'Libro original, convocatorias, poderes, audio, cálculo finca por finca de la deuda, notificaciones y cadena de transmisión/uso posterior.',
      authority: 'Autoridad / procedencia',
      acta2016: 'La propia acta de 26-abr-2016 remite expresamente a los pleitos sobre las juntas de 2-feb y 22-jun-2011. Registra 89,727% representado, LPB 72,976% y sólo 11,039% con voto. Es un puente documental entre la arquitectura de 2011 y las cuentas, deuda, certificados y reclamaciones posteriores.',
      acta2018: 'El acta primaria de 18-may-2018 registra 86,715% representado, LPB 72,976%, CAM 13,034% y sólo 0,385% con voto; el punto de seguridad/acceso llega a la junta a petición de LPB representada por el AC. Por su texto facial no es una entrega judicial de todo el hotel a CAM.',
      no2019: 'Control negativo: no se ha localizado un acta comunitaria de 2019 en el conjunto revisado. El Auto de 24-oct-2019 es un acto judicial y no debe convertirse retroactivamente en acta o consentimiento comunitario.',
      acta2022: 'Nodo de autoridad/proyecto: el dossier controla un acta de 4-feb-2022 con roles concentrados de presidencia, proyecto, representación, administración/banco y deuda. Antes de publicar una reproducción, debe recuperarse de nuevo el original exacto y conciliar acta/audio/anexos, título, voto, conflicto y pagos.',
      contextTitle: '¿De dónde venía la autoridad invocada?',
      contextText: 'Este episodio no debe leerse aislado. El dossier reconstruye 2008 → 2011 → 2016 → 2018 → 2022 y separa cuota dominical, derecho de voto, deuda atribuida, seguridad/acceso y título independiente. Un acta explica procedencia; no sustituye la prueba del resultado posterior.',
      sourceSafety: 'Las actas primarias se conservan como fuentes controladas. Esta página no enlaza copias sin expurgar que contienen identificadores personales; las reproducciones públicas deben ser redactadas y trazables a la fuente.'
    },
    en: {
      originKicker: 'Documentary prologue · 2008 before the 2011 rupture point',
      originTitle: 'Before asking who could decide, show what was being sold and how operation was organised.',
      originLead: 'The contemporary 2008 record and primary instruments establish the starting point: Sun Park was presented to the market as a hotel operation transferred into the Multimatrix perimeter while title remained divided property by property and operation was organised through CEXP. Hotel unity, title, the Owners’ Community, CEXP and LPB are distinct planes.',
      pressBadge: 'Independent contemporary source',
      pressTitle: '16 July 2008 · Alimarket reports Monte Lanza → Multimatrix',
      pressText: 'Alimarket reported that Monte Lanza had reached a June-2008 agreement with Israeli investor Multimatrix concerning Sun Park property and operation. It evidences what the specialist market was told; it does not by itself prove that every property was conveyed or every seller completed every obligation.',
      correctionBadge: 'Entity correction',
      correctionTitle: 'LPB and CEXP must be identified precisely',
      correctionText: 'Where exact legal identity matters, LPB is Luchy Playa Blanca, S.L.U. The press description of CEXP as an “S.L.” does not control: the primary May-2008 statutes describe participating owners constituting a “comunidad civil” for operation. CEXP must not be merged with the Owners’ Community or LPB.',
      minorityBadge: 'Open hypothesis · do not upgrade',
      minorityTitle: 'The minority / “c.23%” perimeter requires a seller-by-property map',
      minorityText: 'The project position is that a minority —historically described as circa 23%— did not complete or breached the contemplated sale and that the fracture later fed operation, debt, voting and authority disputes. The percentage and breach characterisation must be proved seller by seller and property by property. Until then: a minority or approximately one-quarter perimeter requiring documentary reconciliation.',
      publicSource: 'Open Alimarket 2008',
      privateSource: 'Controlled primary source · public redacted copy pending',
      chainButton: 'Open full minutes and authority chain',
      matrixTitle: 'DISPUTED ORIGIN OF AUTHORITY — 22 JUNE 2011',
      matrixIntro: 'The page does not ask the reader to accept the word “fabrication”. It separates what the record says, Gil Marer’s allegation, adverse procedural status and the evidence still required.',
      verified: 'VERIFIED IN THE RECORD',
      allegation: 'GIL MARER’S ALLEGATION',
      legal: 'STATUS / ADVERSE EVIDENCE',
      open: 'OPEN EVIDENCE',
      verifiedText: 'The controlled chronology records a very large LPB share, attributed Community debt, voting exclusion, decisions by the vote-qualified pool and LPB objection. Each percentage must be tied to its own document and denominator.',
      allegationText: 'Gil Marer alleges that this combination produced a materially false or invalid basis of authority that later propagated. That is an investigable allegation, not a conviction or established criminal falsity.',
      legalText: 'The 2011 resolutions were challenged and procedural outcomes adverse to LPB must remain visible. Those outcomes do not automatically validate every later debt figure, certificate or downstream use.',
      openText: 'Original minute book, notices, proxies, audio, property-by-property debt calculation, notifications and the later transmission/reliance chain.',
      authority: 'Authority / provenance',
      acta2016: 'The 26-Apr-2016 minute itself expressly recounts litigation over the 2-Feb and 22-Jun-2011 meetings. It records 89.727% represented, LPB 72.976% and only 11.039% vote-qualified, creating a documentary bridge from the 2011 architecture into later accounts, debt, certificates and claims.',
      acta2018: 'The primary 18-May-2018 minute records 86.715% represented, LPB 72.976%, CAM 13.034% and only 0.385% vote-qualified; security/access was brought to the meeting at LPB’s request through the insolvency administrator. On its face it is not a judicial delivery of the whole hotel to CAM.',
      no2019: 'Negative-evidence control: no 2019 Community minutes have been located in the reviewed source set. The 24-Oct-2019 non-validation order is a judicial act and must not be turned retroactively into Community minutes or consent.',
      acta2022: 'Authority/project node: the dossier controls 4-Feb-2022 minutes with concentrated roles across presidency, project, representation, administration/banking and debt. Before publishing a reproduction, re-recover the exact original and reconcile the minutes/audio/annexes, title, voting, conflict and payments.',
      contextTitle: 'Where did the asserted authority come from?',
      contextText: 'This episode should not be read in isolation. The dossier reconstructs 2008 → 2011 → 2016 → 2018 → 2022 and separates ownership share, voting entitlement, attributed debt, security/access and independent title. Minutes evidence provenance; they do not substitute for proof of the later result.',
      sourceSafety: 'Primary minutes are preserved as controlled sources. This page does not link unredacted copies containing personal identifiers; public reproductions must be redacted and traceable to the source.'
    }
  }[lang];

  const style = document.createElement('style');
  style.textContent = `
    .sp-origin-provenance{border-top:1px solid rgba(20,50,58,.16);border-bottom:1px solid rgba(20,50,58,.16)}
    .sp-origin-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;margin-top:1.4rem}
    .sp-origin-card{padding:1.15rem;border:1px solid rgba(20,50,58,.16);border-radius:18px;background:rgba(255,255,255,.72);box-shadow:0 12px 32px rgba(16,40,48,.06)}
    .sp-origin-card h3{margin:.6rem 0 .55rem;font-size:1.08rem;line-height:1.3}.sp-origin-card p{margin:.45rem 0}
    .sp-source-actions{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:1rem}.sp-source-safety{margin-top:.8rem;font-size:.9rem;opacity:.83}
    .sp-matrix-provenance{margin:1rem 0 1.5rem;padding:1.2rem;border:2px solid rgba(132,62,43,.38);border-radius:20px;background:linear-gradient(135deg,rgba(255,248,242,.96),rgba(255,255,255,.96))}
    .sp-matrix-provenance h3{margin:.25rem 0 .5rem}.sp-matrix-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.75rem;margin-top:1rem}
    .sp-matrix-grid>div{padding:.9rem;border-radius:14px;background:#fff;border:1px solid rgba(20,50,58,.13)}
    .sp-matrix-grid strong{display:block;font-size:.78rem;letter-spacing:.04em;margin-bottom:.35rem}.sp-matrix-grid span{font-size:.92rem;line-height:1.45}
    .sp-row-provenance{margin-top:.75rem;padding:.7rem .8rem;border-left:4px solid rgba(25,86,102,.55);background:rgba(240,247,249,.72);font-size:.9rem;line-height:1.45}
    .sp-row-provenance strong{display:block;margin-bottom:.25rem}.sp-private-source{display:inline-block;margin-top:.35rem;font-weight:700;opacity:.8}
    .sp-context-bridge{margin:1rem auto 1.5rem;max-width:1180px;padding:1rem 1.1rem;border-radius:18px;border:1px solid rgba(20,50,58,.18);background:linear-gradient(135deg,rgba(238,247,249,.96),rgba(255,255,255,.96))}
    .sp-context-bridge h3{margin:.1rem 0 .45rem}.sp-context-bridge p{margin:.35rem 0 .7rem}.sp-evidence-id{display:inline-block;margin-top:.35rem;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.75rem;opacity:.74}
    @media(max-width:900px){.sp-origin-grid,.sp-matrix-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  function originSection() {
    const section = document.createElement('section');
    section.className = 'section alt sp-origin-provenance';
    section.id = 'origen-2008-autoridad';
    section.innerHTML = `
      <div class="shell">
        <div class="section-head"><div><p class="kicker">${t.originKicker}</p><h2>${t.originTitle}</h2></div><p>${t.originLead}</p></div>
        <div class="sp-origin-grid">
          <article class="sp-origin-card"><span class="evidence-badge document">${t.pressBadge}</span><h3>${t.pressTitle}</h3><p>${t.pressText}</p><span class="sp-evidence-id">SP-PRESS-2008-07-16</span></article>
          <article class="sp-origin-card"><span class="evidence-badge correction">${t.correctionBadge}</span><h3>${t.correctionTitle}</h3><p>${t.correctionText}</p><span class="sp-evidence-id">SP-ACTA-2008-04-29 · SP-CEXP-2008-05</span><br><span class="sp-private-source">${t.privateSource}</span></article>
          <article class="sp-origin-card"><span class="evidence-badge question-badge">${t.minorityBadge}</span><h3>${t.minorityTitle}</h3><p>${t.minorityText}</p><span class="sp-evidence-id">ME-COM-001</span></article>
        </div>
        <div class="sp-source-actions"><a class="button secondary" href="${alimarket}" rel="external noopener">${t.publicSource}</a>${onHub ? `<a class="button" href="${actaHref}">${t.chainButton}</a>` : ''}</div>
        <p class="sp-source-safety"><strong>${t.sourceSafety}</strong></p>
      </div>`;
    return section;
  }

  function insertOrigin() {
    if (document.querySelector('#origen-2008-autoridad')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const target = onActas
      ? (document.querySelector('#perimetro') || document.querySelector('#perimeter') || document.querySelector('#cronologia') || document.querySelector('#chronology'))
      : (document.querySelector('#resumen') || document.querySelector('#summary') || main.querySelector('.section'));
    if (target) target.parentNode.insertBefore(originSection(), target); else main.appendChild(originSection());
  }

  function rowByDate(dateNeedles, extraNeedles = []) {
    const rows = Array.from(document.querySelectorAll('table.document-status tbody tr'));
    return rows.find(row => {
      const text = row.textContent.toLowerCase();
      return dateNeedles.some(n => text.includes(n.toLowerCase())) && extraNeedles.every(n => text.includes(n.toLowerCase()));
    });
  }

  function addRowProvenance(row, id, text) {
    if (!row) return;
    row.id = id;
    const cell = row.cells && row.cells.length ? row.cells[row.cells.length - 1] : null;
    if (!cell || cell.querySelector('.sp-row-provenance')) return;
    const note = document.createElement('div');
    note.className = 'sp-row-provenance';
    note.innerHTML = `<strong>${t.authority}</strong>${text}<br><span class="sp-private-source">${t.privateSource}</span><br><span class="sp-evidence-id">${id.toUpperCase()}</span>`;
    cell.appendChild(note);
  }

  function tagActas() {
    if (!onActas) return;
    const r2011 = rowByDate(isES ? ['22 junio 2011'] : ['22 june 2011']);
    const r2016 = rowByDate(isES ? ['26 abril 2016'] : ['26 april 2016']);
    const r2018 = rowByDate(isES ? ['18 mayo 2018'] : ['18 may 2018']);
    const r2019 = rowByDate(['2019'], isES ? ['sin acta comunitaria localizada'] : ['no community minutes located']);
    const r2022 = rowByDate(isES ? ['4 febrero 2022'] : ['4 february 2022']);

    if (r2011) {
      r2011.id = 'sp-acta-2011-06-22';
      if (!document.querySelector('.sp-matrix-provenance')) {
        const box = document.createElement('aside');
        box.className = 'sp-matrix-provenance';
        box.innerHTML = `<span class="evidence-badge representation-badge">SP-ACTA-2011-06-22</span><h3>${t.matrixTitle}</h3><p>${t.matrixIntro}</p><div class="sp-matrix-grid"><div><strong>${t.verified}</strong><span>${t.verifiedText}</span></div><div><strong>${t.allegation}</strong><span>${t.allegationText}</span></div><div><strong>${t.legal}</strong><span>${t.legalText}</span></div><div><strong>${t.open}</strong><span>${t.openText}</span></div></div>`;
        const wrap = r2011.closest('.control-table-wrap') || r2011.closest('section');
        if (wrap && wrap.parentNode) wrap.parentNode.insertBefore(box, wrap);
      }
    }

    addRowProvenance(r2016, 'sp-acta-2016-04-26', t.acta2016);
    addRowProvenance(r2018, 'sp-acta-2018-05-18', t.acta2018);
    addRowProvenance(r2019, 'sp-no-acta-2019', t.no2019);
    addRowProvenance(r2022, 'sp-acta-2022-02-04', t.acta2022);
  }

  function insertContextBridge() {
    if (!onContextRoute || document.querySelector('.sp-context-bridge')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const hero = main.querySelector('.dossier-hero');
    const bridge = document.createElement('aside');
    bridge.className = 'sp-context-bridge';
    bridge.innerHTML = `<span class="evidence-badge document">2008 → 2011 → 2016 → 2018 → 2022</span><h3>${t.contextTitle}</h3><p>${t.contextText}</p><a class="button secondary" href="${actaHref}">${t.chainButton} →</a>`;
    if (hero && hero.nextSibling) hero.parentNode.insertBefore(bridge, hero.nextSibling); else main.insertBefore(bridge, main.firstChild);
  }

  function updateTitle() {
    if (!onActas) return;
    document.title = isES
      ? 'Actas Sun Park 2011–2022 con origen 2008 — deuda, voto y autoridad'
      : 'Sun Park minutes 2011–2022 with 2008 origin — debt, voting and authority';
  }

  function run() { insertOrigin(); tagActas(); insertContextBridge(); updateTitle(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true }); else run();
})();
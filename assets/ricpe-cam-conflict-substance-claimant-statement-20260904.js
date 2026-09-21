(() => {
  'use strict';
  const path = location.pathname.replace(/\/index\.html$/, '/');
  const relevant = path.includes('/ric-private-equity-sun-park/')
    || path.includes('/ricpe-')
    || path.includes('/acosta-matos-')
    || path.includes('/acosta-matos-perimet')
    || path.includes('/reclamacion-caixabank-valencia/')
    || path.includes('/caixabank-valencia-claim/')
    || path.includes('/uria');
  if (!relevant || document.querySelector('[data-ricpe-cam-conflict-substance-statement]')) return;

  const isEnglish = document.documentElement.lang === 'en' || path.includes('/en/');
  const main = document.querySelector('main');
  if (!main) return;
  const prefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const ricpe = isEnglish ? `${prefix}en/ric-private-equity-sun-park/` : `${prefix}es/ric-private-equity-sun-park/`;
  const controls = isEnglish ? `${prefix}en/ricpe-documentary-accountability/` : `${prefix}es/ricpe-responsabilidad-documental/`;
  const caix = isEnglish ? `${prefix}en/caixabank-valencia-claim/` : `${prefix}es/reclamacion-caixabank-valencia/`;

  const style = document.createElement('style');
  style.dataset.ricpeCamConflictSubstanceStyle = '20260904';
  style.textContent = `
    [data-ricpe-cam-conflict-substance-statement]{margin:1.15rem auto;border:2px solid #9a6418;border-left-width:8px;background:#fffaf0;border-radius:16px;padding:1.15rem 1.25rem;box-shadow:0 10px 28px rgba(20,30,35,.07)}
    [data-ricpe-cam-conflict-substance-statement] .kicker{margin:0 0 .35rem;color:#754707;font-weight:950;letter-spacing:.08em;text-transform:uppercase;font-size:.72rem}
    [data-ricpe-cam-conflict-substance-statement] h2{margin:.1rem 0 .65rem;font-size:clamp(1.45rem,3vw,2.25rem);line-height:1.06}
    [data-ricpe-cam-conflict-substance-statement] p{line-height:1.56;margin:.55rem 0}
    [data-ricpe-cam-conflict-substance-statement] .grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;margin:.9rem 0}
    [data-ricpe-cam-conflict-substance-statement] .card{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:12px;padding:.8rem}
    [data-ricpe-cam-conflict-substance-statement] .card strong{display:block;margin-bottom:.25rem}
    [data-ricpe-cam-conflict-substance-statement] .status{display:inline-block;margin-top:.55rem;padding:.32rem .58rem;border-radius:999px;background:#754707;color:#fff;font-size:.69rem;font-weight:900;letter-spacing:.04em}
    [data-ricpe-cam-conflict-substance-statement] .links{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:.8rem}
    [data-ricpe-cam-conflict-substance-statement] .links a{display:inline-block;text-decoration:none;font-weight:900;border-radius:999px;padding:.48rem .68rem;background:#13252d;color:#fff}
    @media(max-width:760px){[data-ricpe-cam-conflict-substance-statement] .grid{grid-template-columns:1fr}}
  `;
  document.head.append(style);

  const section = document.createElement('section');
  section.className = 'shell';
  section.dataset.ricpeCamConflictSubstanceStatement = '20260904';
  section.setAttribute('aria-label', isEnglish ? 'Gil Marer allegation concerning the substance of RICPE and CAM conflict controls' : 'Alegación de Gil Marer sobre la sustancia de los controles de conflicto RICPE y CAM');

  section.innerHTML = isEnglish ? `
    <p class="kicker">GIL MARER · CURRENT ALLEGATION · FORMALITY IS NOT SUBSTANCE</p>
    <h2>CAM's conflict disclosure and abstention are documented. Gil Marer alleges they were cosmetic and did not establish independent control.</h2>
    <p><strong>Documented fact:</strong> RICPE's later audited accounts say Construcciones Acosta Matos disclosed a related-party conflict, abstained from the relevant shareholder/Board deliberations and votes, and that RICPE's Control Unit issued a favourable report. Por Derecho preserves those facts.</p>
    <p><strong>Gil Marer's allegation:</strong> those formal acts were, in his words, “lip service”. He alleges that the conduct before and after them — including the 2020 investor presentation, the materially narrower 20–21 July 2021 ownership / due-diligence position, the later revival and financing of MYND Yaiza, the overlapping governance/professional perimeter, and RICPE's 27 August 2026 decision to close his whistleblower communication without opening an internal investigation — requires the formal conflict process to be tested for substantive independence, completeness and truthfulness rather than treated as exonerating merely because a declaration and abstention existed.</p>
    <div class="grid">
      <div class="card"><strong>What is proved</strong>Formal conflict disclosure/abstention and a favourable Control Unit process were recorded; later financing materialised.</div>
      <div class="card"><strong>What Gil alleges</strong>The formalities did not cure the underlying lack of independence and were cosmetic within a wider mutually reinforcing network of conduct.</div>
      <div class="card"><strong>What is not adjudicated</strong>No court or regulator is represented here as having found RICPE, CAM, Uría or their officers dishonest, collusive or criminally liable.</div>
      <div class="card"><strong>What must be produced</strong>The declaration, minutes, recusals, Control Unit report and inputs, title/insolvency analysis, RICPE/Uría/PwC files, risk records, guarantees, corrections, investor communications and re-approval chronology.</div>
    </div>
    <p><strong>Evidence test:</strong> the issue is not whether paperwork labelled “conflict” existed. It is whether decision-makers were genuinely independent, received the complete Sun Park ownership/insolvency record, corrected earlier investor representations where necessary, and could demonstrate why the later investment was approved on a fully informed basis.</p>
    <p><strong>27 August 2026 status:</strong> RICPE's ethics channel closed Gil Marer's communication at preliminary admissibility stage without opening an internal investigation, stating that it had not identified sufficiently concrete objective indicia. The same closure expressly left open future assessment of new concrete, objectively verifiable evidence. Por Derecho treats that as a preliminary non-investigation decision, not as a merits finding that the allegations are false.</p>
    <span class="status">CLAIMANT / WHISTLEBLOWER ALLEGATION — DOCUMENT-TESTABLE — NOT AN ADJUDICATED FINDING</span>
    <div class="links"><a href="${ricpe}">RICPE / Sun Park unitary dossier →</a><a href="${controls}">RICPE documentary controls →</a><a href="${caix}">Live CaixaBank branch →</a></div>
  ` : `
    <p class="kicker">GIL MARER · ALEGACIÓN ACTUAL · LA FORMALIDAD NO ES LA SUSTANCIA</p>
    <h2>La declaración de conflicto y abstención de CAM están documentadas. Gil Marer alega que fueron cosméticas y no acreditan un control independiente.</h2>
    <p><strong>Hecho documentado:</strong> las cuentas auditadas posteriores de RICPE dicen que Construcciones Acosta Matos declaró un conflicto de parte vinculada, se abstuvo en las deliberaciones y votaciones correspondientes de Junta/Consejo y que la Unidad de Control de RICPE emitió informe favorable. Por Derecho conserva esos hechos.</p>
    <p><strong>Alegación de Gil Marer:</strong> esos actos formales fueron, en sus palabras, <em>“lip service”</em> —cumplimiento meramente aparente—. Alega que la conducta anterior y posterior —incluidas la presentación a inversores de 2020, la posición materialmente más estrecha de 20–21 de julio de 2021 sobre titularidad y due diligence, la posterior reactivación y financiación de MYND Yaiza, el perímetro superpuesto de gobernanza y profesionales y la decisión de RICPE de 27 de agosto de 2026 de cerrar su comunicación de alertador sin abrir investigación interna— obliga a comprobar la independencia, integridad y veracidad sustantivas del proceso de conflicto, en lugar de tratarlo como exculpatorio por la mera existencia de una declaración y una abstención.</p>
    <div class="grid">
      <div class="card"><strong>Lo acreditado</strong>Constan formalmente declaración/abstención de conflicto y un proceso favorable de la Unidad de Control; la financiación posterior se materializó.</div>
      <div class="card"><strong>Lo que alega Gil</strong>Las formalidades no subsanaron la falta de independencia subyacente y fueron cosméticas dentro de una red más amplia de conductas mutuamente reforzadas.</div>
      <div class="card"><strong>Lo no adjudicado</strong>No se presenta a ningún tribunal o regulador como autor de una conclusión de deshonestidad, concertación o responsabilidad penal de RICPE, CAM, Uría o sus cargos.</div>
      <div class="card"><strong>Lo que debe producirse</strong>Declaración, actas, abstenciones, informe e inputs de la Unidad de Control, análisis de título/concurso, expedientes RICPE/Uría/PwC, riesgo, garantías, correcciones, comunicaciones a inversores y cronología de re-aprobación.</div>
    </div>
    <p><strong>Prueba decisiva:</strong> la cuestión no es si existía un papel llamado “conflicto”. Es si quienes decidieron eran realmente independientes, recibieron el expediente completo de titularidad y concurso de Sun Park, corrigieron cuando procedía las representaciones anteriores a inversores y pueden demostrar por qué la inversión posterior fue aprobada sobre una base plenamente informada.</p>
    <p><strong>Estado 27 agosto 2026:</strong> el Canal Ético de RICPE cerró la comunicación de Gil Marer en fase preliminar de admisibilidad sin abrir investigación interna, afirmando que no había identificado indicios objetivos suficientemente concretos. El propio cierre dejó expresamente abierta una futura valoración de nueva evidencia concreta, objetivamente verificable y relevante. Por Derecho lo trata como una decisión preliminar de no investigar, no como una resolución de fondo que declare falsas las alegaciones.</p>
    <span class="status">ALEGACIÓN DEL PERJUDICADO / ALERTADOR — VERIFICABLE DOCUMENTALMENTE — NO ADJUDICADA</span>
    <div class="links"><a href="${ricpe}">Dossier unitario RICPE / Sun Park →</a><a href="${controls}">Controles documentales RICPE →</a><a href="${caix}">Rama CaixaBank en curso →</a></div>
  `;

  const anchor = document.querySelector('#pregunta-unitaria') || document.querySelector('#caixabank-concurso-cam-linkage') || main.querySelector(':scope > section:first-of-type');
  if (anchor) anchor.insertAdjacentElement('afterend', section);
  else main.prepend(section);
})();

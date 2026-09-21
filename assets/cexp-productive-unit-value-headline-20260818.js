(() => {
  'use strict';

  const path = (window.location.pathname.replace(/\/+$/, '') || '/') + '/';
  const isEs = path.includes('/es/');
  const acRoutes = [
    '/en/insolvency-36-2012-insolvency-administrator/',
    '/es/concurso-36-2012-administrador-concursal/'
  ];
  const fullRoutes = [
    '/en/lpb-solvency-record/',
    '/es/expediente-solvencia-lpb/',
    '/en/lpb-insolvency/',
    '/es/insolvencia-lpb/',
    '/en/insolvency-classification-parallel-lives/',
    '/es/calificacion-concurso-36-2012-vidas-paralelas/',
    '/en/community-instrumentalisation/',
    '/es/comunidad-instrumentalizacion/',
    '/en/recovery-restitution-objectives/',
    '/es/objetivos-recuperacion-restitucion/'
  ];
  const compactRoutes = [
    '/en/insolvency-36-2012-institutional-accountability/',
    '/es/concurso-36-2012-responsabilidad-institucional/',
    '/en/acosta-matos-perimeter/',
    '/es/acosta-matos-perimetro/',
    '/en/same-hotel-multiple-financial-lives/',
    '/es/mismo-hotel-multiples-vidas-financieras/',
    '/en/sun-park-takeover-7-june-2018/',
    '/es/toma-control-sun-park-7-junio-2018/',
    '/en/ricpe-documentary-accountability/',
    '/es/ricpe-responsabilidad-documental/',
    '/en/actua-2018-spatial-test/',
    '/es/actua-2018-prueba-espacial/',
    '/en/sun-park-forensic-map-262-properties/',
    '/es/mapa-forense-sun-park-262-fincas/'
  ];

  const isAc = acRoutes.some(route => path.endsWith(route));
  const isFull = !isAc && fullRoutes.some(route => path.endsWith(route));
  const isCompact = !isAc && !isFull && compactRoutes.some(route => path.endsWith(route));
  if (!isAc && !isFull && !isCompact) return;
  if (document.getElementById('cexp-productive-unit-value-headline')) return;

  const base = 'https://sbu001monterecco.github.io/por-derecho';
  const links = isEs ? {
    solvency: `${base}/es/expediente-solvencia-lpb/`,
    community: `${base}/es/comunidad-instrumentalizacion/`,
    classification: `${base}/es/calificacion-concurso-36-2012-vidas-paralelas/`,
    ac: `${base}/es/concurso-36-2012-administrador-concursal/`,
    actua: `${base}/es/actua-2018-prueba-espacial/`,
    recovery: `${base}/es/objetivos-recuperacion-restitucion/`
  } : {
    solvency: `${base}/en/lpb-solvency-record/`,
    community: `${base}/en/community-instrumentalisation/`,
    classification: `${base}/en/insolvency-classification-parallel-lives/`,
    ac: `${base}/en/insolvency-36-2012-insolvency-administrator/`,
    actua: `${base}/en/actua-2018-spatial-test/`,
    recovery: `${base}/en/recovery-restitution-objectives/`
  };

  const addStyles = () => {
    if (document.getElementById('cexp-productive-unit-value-headline-styles')) return;
    const style = document.createElement('style');
    style.id = 'cexp-productive-unit-value-headline-styles';
    style.textContent = `
      .cvh{--ink:#13252d;--gold:#c89432;--paper:#f6f1e6;--red:#8b443c;--green:#526b59}
      .cvh .cvh-shell{max-width:1120px;margin:0 auto}
      .cvh .cvh-panel{border:1px solid rgba(19,37,45,.2);border-top:9px solid var(--gold);border-radius:20px;background:#fff;padding:1.35rem 1.45rem;box-shadow:0 13px 34px rgba(19,37,45,.08)}
      .cvh .cvh-kicker{margin:0 0 .4rem;font-size:.73rem;letter-spacing:.085em;text-transform:uppercase;font-weight:950;color:#6b5841}
      .cvh h2{margin:.05rem 0 .7rem;color:var(--ink);font-size:clamp(1.65rem,3.1vw,2.55rem);line-height:1.08}
      .cvh .cvh-lead{font-size:1.08rem;line-height:1.58;margin:.25rem 0 1rem}
      .cvh .cvh-maxim{display:grid;grid-template-columns:1fr auto 1fr;gap:.8rem;align-items:center;margin:1rem 0}
      .cvh .cvh-maxim div{border-radius:15px;padding:1rem;background:var(--ink);color:#fff;text-align:center;font-weight:900}
      .cvh .cvh-maxim div:last-child{background:var(--paper);color:var(--ink);border:1px solid rgba(19,37,45,.16)}
      .cvh .cvh-maxim span{font-size:1.9rem;font-weight:950;color:var(--gold)}
      .cvh .cvh-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.85rem;margin:1rem 0}
      .cvh .cvh-card{border:1px solid rgba(19,37,45,.15);border-radius:14px;padding:1rem;background:#fff}
      .cvh .cvh-card h3{margin:0 0 .42rem;color:var(--ink);font-size:1.03rem}
      .cvh .cvh-card p:last-child,.cvh .cvh-card ul:last-child,.cvh .cvh-card ol:last-child{margin-bottom:0}
      .cvh .cvh-card ul,.cvh .cvh-card ol{padding-left:1.2rem}
      .cvh .cvh-audit{background:var(--ink);color:#fff;border-radius:15px;padding:1.05rem 1.15rem;margin:1rem 0}
      .cvh .cvh-audit strong{color:#f1ddb6}
      .cvh .cvh-request{border-left:7px solid var(--gold);background:var(--paper);border-radius:14px;padding:1rem 1.15rem;margin:1rem 0}
      .cvh .cvh-boundary{border-left:5px solid var(--red);background:#fff7f5;border-radius:14px;padding:1rem 1.15rem;margin:1rem 0}
      .cvh .cvh-status{display:flex;flex-wrap:wrap;gap:.42rem;list-style:none;padding:0;margin:.8rem 0}
      .cvh .cvh-status li{border-radius:999px;padding:.3rem .58rem;font-size:.68rem;letter-spacing:.04em;text-transform:uppercase;font-weight:900;background:#e4ebe6;color:var(--ink)}
      .cvh .cvh-status li.open{background:#eee5d4}
      .cvh .cvh-actions{display:flex;flex-wrap:wrap;gap:.55rem;margin-top:.9rem}
      .cvh .cvh-actions a{display:inline-block;text-decoration:none;border-radius:999px;padding:.64rem .88rem;background:var(--ink);color:#fff;border:1px solid var(--ink);font-weight:850}
      .cvh .cvh-actions a.secondary{background:#fff;color:var(--ink)}
      .cvh.cvh-compact .cvh-panel{padding:1.05rem 1.2rem;border-top-width:7px}
      .cvh.cvh-compact h2{font-size:clamp(1.32rem,2.5vw,1.9rem)}
      .cvh.cvh-ac .cvh-panel{border-top-color:var(--red)}
      .cvh.cvh-ac .cvh-request{border-left-color:var(--red)}
      @media(max-width:800px){.cvh .cvh-grid,.cvh .cvh-maxim{grid-template-columns:1fr}.cvh .cvh-maxim span{text-align:center;transform:rotate(90deg)}}
      @media(max-width:620px){.cvh .cvh-panel{padding:1rem}}
    `;
    document.head.appendChild(style);
  };

  const enFull = `
    <div class="cvh-panel">
      <p class="cvh-kicker">THE OMITTED VALUE · CEXP · PRODUCTIVE UNIT · CONCURSO 36/2012</p>
      <h2>LPB was the debtor. CEXP was outside the estate. Its economic value was not outside the insolvency analysis.</h2>
      <p class="cvh-lead"><strong>The group’s central valuation case is wider than undervaluation of individual LPB properties.</strong> It is that the insolvency process did not adequately identify, reconstruct, value and integrate LPB’s legally and economically attributable interest in the unified Sun Park hotel productive unit organised through the Comunidad de Explotación del Complejo Sun Park (CEXP): participation and exploitation rights, income and receivables, operating contracts and infrastructure, maintenance economics, going-concern uplift, rescue capacity and related recovery claims.</p>
      <ul class="cvh-status"><li>Source-supported group position</li><li class="open">Complete AC-file proposition map still required</li><li class="open">Independent productive-unit valuation required</li></ul>
      <div class="cvh-maxim"><div>LPB REGISTERED-PROPERTY VALUE</div><span>≠</span><div>LPB’S FULL ATTRIBUTABLE ECONOMIC VALUE</div></div>
      <div class="cvh-grid">
        <article class="cvh-card"><h3>What CEXP changes</h3><p>CEXP was a non-corporate operating/exploitation structure, not simply another LPB asset. Its separation from the estate did not make LPB’s participation, receivables, income rights, contractual position or the going-concern value added to LPB’s properties economically irrelevant.</p></article>
        <article class="cvh-card"><h3>What must remain separate</h3><p>Registered title, CEXP participation, exploitation authority, productive-unit value and ownership of particular cash flows are distinct questions. The exercise is to identify LPB’s attributable value, not to pull all CEXP or third-party property into LPB’s estate.</p></article>
        <article class="cvh-card"><h3>The calificación asymmetry</h3><p>The adverse case measured downstream rent/non-collection and operator economics. A reciprocal analysis must also measure upstream inventory, operating capacity, Community debt/voting, maintenance and staff costs, access/control, actual receipts, AC decisions and the causes that may have impaired income.</p></article>
        <article class="cvh-card"><h3>The valuation consequence</h3><p>The current ACTÚA/GESVALT reconstruction makes the issue concrete: the Liquidation Plan used ACTÚA values, while GESVALT separately criticised ACTÚA and later produced a €25.647m ECO valuation. Productive-unit and going-concern economics must therefore be reconciled with the property-by-property estate perimeter, not silently substituted by one another.</p></article>
      </div>
      <div class="cvh-request"><strong>Required determination.</strong> The complete record should state what LPB legally held through or against CEXP; what income, receivables, contracts, inventory and operating functions were attributable to it; what material LPB/Aweswell sought to place before the AC and Court; how the AC treated that material; and what effect the resulting valuation had on solvency, rescue, liquidation, adjudication, surplus and the calificación.</div>
      <div class="cvh-boundary"><strong>Evidence boundary.</strong> The current record strongly supports the existence and materiality of the CEXP/productive-unit valuation issue. It does not yet justify the global statement that no productive-unit component was ever considered, or that deliberate suppression is proved. The stronger controlled allegation is that the value was <em>not adequately identified, reconstructed, valued and integrated</em>, subject to a final dated document-by-document audit.</div>
      <div class="cvh-actions"><a href="${links.solvency}">LPB value and accounts</a><a class="secondary" href="${links.community}">CEXP / Community record</a><a class="secondary" href="${links.classification}">Calificación</a><a class="secondary" href="${links.actua}">ACTÚA / GESVALT valuation test</a></div>
    </div>`;

  const esFull = `
    <div class="cvh-panel">
      <p class="cvh-kicker">EL VALOR OMITIDO · CEXP · UNIDAD PRODUCTIVA · CONCURSO 36/2012</p>
      <h2>LPB era la concursada. La CEXP estaba fuera de la masa. Su valor económico no podía quedar fuera del análisis concursal.</h2>
      <p class="cvh-lead"><strong>La tesis central de valoración del grupo va más allá de la infravaloración de las fincas individuales de LPB.</strong> Sostiene que el concurso no identificó, reconstruyó, valoró e integró adecuadamente el interés jurídica y económicamente atribuible a LPB en la unidad productiva hotelera unitaria de Sun Park articulada a través de la Comunidad de Explotación del Complejo Sun Park (CEXP): participación y derechos de explotación, ingresos y créditos, contratos e infraestructura operativa, economía de mantenimiento, prima de empresa en funcionamiento, capacidad de rescate y acciones conexas.</p>
      <ul class="cvh-status"><li>Posición del grupo apoyada en fuentes</li><li class="open">Pendiente mapa completo del expediente AC</li><li class="open">Pendiente valoración pericial independiente</li></ul>
      <div class="cvh-maxim"><div>VALOR DE LAS FINCAS REGISTRALES DE LPB</div><span>≠</span><div>VALOR ECONÓMICO ÍNTEGRO ATRIBUIBLE A LPB</div></div>
      <div class="cvh-grid">
        <article class="cvh-card"><h3>Qué cambia la CEXP</h3><p>La CEXP era una estructura no societaria de explotación, no simplemente otro activo de LPB. Que estuviera fuera de la masa no hacía irrelevantes la participación de LPB, sus créditos, sus derechos de ingresos, su posición contractual ni la prima de empresa en funcionamiento que la explotación añadía a sus inmuebles.</p></article>
        <article class="cvh-card"><h3>Qué debe permanecer separado</h3><p>Titularidad registral, participación CEXP, autoridad de explotación, valor de unidad productiva y titularidad de flujos concretos son cuestiones distintas. El ejercicio consiste en identificar el valor atribuible a LPB, no en incorporar a la masa toda la CEXP o bienes de terceros.</p></article>
        <article class="cvh-card"><h3>La asimetría de la calificación</h3><p>La tesis adversa midió aguas abajo renta/no cobro y economía del operador. Un análisis recíproco debe medir también inventario explotable, capacidad operativa, deuda/voto comunitarios, mantenimiento y personal, acceso/control, cobros reales, decisiones de la AC y causas que pudieron deteriorar los ingresos.</p></article>
        <article class="cvh-card"><h3>La consecuencia de valoración</h3><p>La reconstrucción ACTÚA/GESVALT lo hace concreto: el Plan de Liquidación utilizó valores ACTÚA, mientras GESVALT criticó separadamente ACTÚA y después produjo una tasación ECO de 25,647 M€. La economía de la unidad productiva y de empresa en funcionamiento debe conciliarse con el perímetro finca por finca, no sustituirse silenciosamente una por otra.</p></article>
      </div>
      <div class="cvh-request"><strong>Pronunciamiento necesario.</strong> El expediente completo debe fijar qué tenía jurídicamente LPB a través de o frente a la CEXP; qué ingresos, créditos, contratos, inventario y funciones operativas le eran atribuibles; qué material intentaron aportar LPB/Aweswell ante la AC y el Juzgado; cómo fue tratado; y qué efecto tuvo la valoración resultante sobre solvencia, rescate, liquidación, adjudicación, sobrante y calificación.</div>
      <div class="cvh-boundary"><strong>Límite probatorio.</strong> El registro actual respalda con fuerza la existencia y materialidad de la cuestión CEXP/unidad productiva. Todavía no permite afirmar globalmente que nunca se considerara componente alguno ni que esté probada una supresión deliberada. La alegación controlada más fuerte es que el valor <em>no fue adecuadamente identificado, reconstruido, valorado e integrado</em>, pendiente de una auditoría final documento por documento y fecha por fecha.</div>
      <div class="cvh-actions"><a href="${links.solvency}">Valor y cuentas de LPB</a><a class="secondary" href="${links.community}">Expediente CEXP / Comunidad</a><a class="secondary" href="${links.classification}">Calificación</a><a class="secondary" href="${links.actua}">Prueba de valoración ACTÚA / GESVALT</a></div>
    </div>`;

  const enAc = `
    <div class="cvh-panel">
      <p class="cvh-kicker">HEADLINE AC ACCOUNTABILITY CONTROL · CEXP PRODUCTIVE-UNIT VALUE</p>
      <h2>The AC accountability question is not complete until it answers what happened to LPB’s attributable value in the CEXP productive unit.</h2>
      <p class="cvh-lead">The Administrator’s role must be tested not only against individual properties, debt, offers and adjudication, but against the hotel as an operating economic system. The group’s case is that LPB’s participation, income rights, receivables, operating dependencies, going-concern uplift and productive-unit rescue value were not adequately identified, reconstructed, valued and integrated before the case moved through liquidation and later calificación.</p>
      <div class="cvh-audit"><strong>The controlling AC audit:</strong> NOTICE → POWER/DUTY → CEXP MATERIAL RECEIVED → VALUE IDENTIFIED → VALUATION METHOD → PROTECTION/PURSUIT → LIQUIDATION USE → CONSEQUENCE FOR LPB → REASONED RESPONSE.</div>
      <div class="cvh-grid">
        <article class="cvh-card"><h3>1 · Knowledge</h3><p>What did the AC know about CEXP’s provenance, LPB participation, the unitary operation, Community debt/voting disputes, operator arrangements, hotel income, maintenance burden and competing explanation for impaired rent?</p></article>
        <article class="cvh-card"><h3>2 · Power and responsibility</h3><p>Which CEXP-related matters were estate rights requiring identification, collection, protection or valuation; which were extraconcursal; and which indirectly affected the market/going-concern value of LPB’s estate?</p></article>
        <article class="cvh-card"><h3>3 · Valuation and rescue</h3><p>What productive-unit methodology was used before the Liquidation Plan, CAM offer and adjudication? How were ACTÚA, the GESVALT critique, the later €25.647m ECO appraisal, operating income and rescue/refinancing alternatives reconciled?</p></article>
        <article class="cvh-card"><h3>4 · Reciprocity in the calificación</h3><p>If rent non-collection and operator economics are used adversely, the same record should address upstream impediments to income and the AC’s own knowledge, decisions, access/security role and response to the CEXP/Community conflict.</p></article>
      </div>
      <div class="cvh-request"><strong>Specific records required.</strong> Complete Article 75 report and annexes; inventory and creditor lists; liquidation plan and amendments; quarterly reports and rendering of accounts; valuation instructions and reports; CEXP material received from LPB/Aweswell; correspondence and record-access requests; operating/rent ledgers; and the document trail showing why each productive-unit component was included, excluded or treated outside the estate.</div>
      <div class="cvh-boundary"><strong>Fairness control.</strong> This does not establish that the AC intentionally suppressed value or that every CEXP asset belonged to LPB. The AC could rely on statutory powers, court orders, the liquidation plan and information then available. The issue is narrower and testable: whether LPB’s attributable productive-unit value was fully identified, protected and valued, and whether any omission materially affected creditor recovery, liquidation or the calificación.</div>
      <div class="cvh-actions"><a href="${links.solvency}">LPB value record</a><a class="secondary" href="${links.community}">CEXP evidence</a><a class="secondary" href="${links.actua}">ACTÚA / GESVALT</a><a class="secondary" href="${links.classification}">Calificación</a></div>
    </div>`;

  const esAc = `
    <div class="cvh-panel">
      <p class="cvh-kicker">CONTROL CENTRAL DE RESPONSABILIDAD AC · VALOR DE LA UNIDAD PRODUCTIVA CEXP</p>
      <h2>La revisión de la AC no está completa mientras no responda qué ocurrió con el valor atribuible a LPB en la unidad productiva articulada mediante la CEXP.</h2>
      <p class="cvh-lead">La actuación de la Administración Concursal debe examinarse no sólo frente a fincas aisladas, deuda, ofertas y adjudicación, sino frente al hotel como sistema económico operativo. La tesis del grupo es que la participación de LPB, sus derechos de ingresos, créditos, dependencias operativas, prima de empresa en funcionamiento y valor de rescate de la unidad productiva no fueron adecuadamente identificados, reconstruidos, valorados e integrados antes de que el procedimiento avanzara por liquidación y posterior calificación.</p>
      <div class="cvh-audit"><strong>Auditoría AC controlante:</strong> CONOCIMIENTO → PODER/DEBER → MATERIAL CEXP RECIBIDO → VALOR IDENTIFICADO → MÉTODO DE VALORACIÓN → PROTECCIÓN/EJERCICIO → USO EN LIQUIDACIÓN → CONSECUENCIA PARA LPB → RESPUESTA MOTIVADA.</div>
      <div class="cvh-grid">
        <article class="cvh-card"><h3>1 · Conocimiento</h3><p>¿Qué sabía la AC sobre la procedencia de CEXP, participación de LPB, explotación unitaria, disputas de deuda/voto comunitarios, contratos de operador, ingresos hoteleros, carga de mantenimiento y explicación competidora de la pérdida de renta?</p></article>
        <article class="cvh-card"><h3>2 · Poder y responsabilidad</h3><p>¿Qué materias CEXP eran derechos de la masa que exigían identificación, cobro, protección o valoración; cuáles eran extraconcursales; y cuáles afectaban indirectamente al valor de mercado/empresa en funcionamiento de la masa de LPB?</p></article>
        <article class="cvh-card"><h3>3 · Valoración y rescate</h3><p>¿Qué metodología de unidad productiva se utilizó antes del Plan de Liquidación, oferta CAM y adjudicación? ¿Cómo se conciliaron ACTÚA, la crítica de GESVALT, la posterior ECO de 25,647 M€, los ingresos operativos y las alternativas de rescate/refinanciación?</p></article>
        <article class="cvh-card"><h3>4 · Reciprocidad en la calificación</h3><p>Si el no cobro de renta y la economía del operador se utilizan en contra, el mismo expediente debe analizar los impedimentos aguas arriba a la generación de ingresos y el conocimiento, decisiones, papel de acceso/seguridad y respuesta de la propia AC al conflicto CEXP/Comunidad.</p></article>
      </div>
      <div class="cvh-request"><strong>Registros concretos necesarios.</strong> Informe art. 75 y anexos; inventario y listas de acreedores; plan de liquidación y modificaciones; informes trimestrales y rendición de cuentas; encargos y valoraciones; material CEXP recibido de LPB/Aweswell; correspondencia y solicitudes de acceso; libros de explotación/renta; y trazabilidad que explique por qué cada componente de unidad productiva fue incluido, excluido o tratado fuera de la masa.</div>
      <div class="cvh-boundary"><strong>Control de equidad.</strong> Esto no acredita que la AC suprimiera intencionadamente valor ni que todo activo CEXP perteneciera a LPB. La AC podía apoyarse en sus funciones legales, resoluciones judiciales, plan de liquidación e información disponible. La cuestión es más estrecha y comprobable: si se identificó, protegió y valoró íntegramente el valor de unidad productiva atribuible a LPB y si cualquier omisión afectó materialmente a la recuperación de acreedores, la liquidación o la calificación.</div>
      <div class="cvh-actions"><a href="${links.solvency}">Expediente de valor LPB</a><a class="secondary" href="${links.community}">Prueba CEXP</a><a class="secondary" href="${links.actua}">ACTÚA / GESVALT</a><a class="secondary" href="${links.classification}">Calificación</a></div>
    </div>`;

  const enCompact = `
    <div class="cvh-panel">
      <p class="cvh-kicker">CEXP PRODUCTIVE-UNIT VALUE · CROSS-SITE CONTROL</p>
      <h2>One hotel was valued and commercially used as a productive unit; LPB’s attributable CEXP economics cannot be reduced to isolated property title.</h2>
      <p>The controlling issue is whether LPB’s participation, income rights, receivables, going-concern uplift and related claims were fully identified and integrated in Concurso 36/2012. This is a source-supported allegation requiring complete AC-file and independent valuation verification.</p>
      <div class="cvh-actions"><a href="${links.solvency}">Full value analysis</a><a class="secondary" href="${links.community}">CEXP record</a></div>
    </div>`;

  const esCompact = `
    <div class="cvh-panel">
      <p class="cvh-kicker">VALOR UNIDAD PRODUCTIVA CEXP · CONTROL TRANSVERSAL</p>
      <h2>Un mismo hotel fue valorado y explotado comercialmente como unidad productiva; la economía CEXP atribuible a LPB no puede reducirse a titularidad registral aislada.</h2>
      <p>La cuestión controlante es si la participación, ingresos, créditos, prima de empresa en funcionamiento y acciones conexas de LPB fueron plenamente identificados e integrados en el Concurso 36/2012. Es una alegación apoyada en fuentes que exige verificación con el expediente AC completo y una valoración independiente.</p>
      <div class="cvh-actions"><a href="${links.solvency}">Análisis completo de valor</a><a class="secondary" href="${links.community}">Expediente CEXP</a></div>
    </div>`;

  const mount = () => {
    if (document.getElementById('cexp-productive-unit-value-headline')) return;
    const main = document.querySelector('main');
    if (!main) return;
    addStyles();
    const section = document.createElement('section');
    section.id = 'cexp-productive-unit-value-headline';
    section.className = `section cvh${isAc ? ' cvh-ac' : ''}${isCompact ? ' cvh-compact' : ''}`;
    const body = isAc ? (isEs ? esAc : enAc) : isFull ? (isEs ? esFull : enFull) : (isEs ? esCompact : enCompact);
    section.innerHTML = `<div class="shell cvh-shell">${body}</div>`;

    const preferred = document.getElementById('aweswell-accounts-calificacion-incorporation');
    const thesis = main.querySelector('[data-calificacion-misuse-thesis]');
    if (preferred) preferred.insertAdjacentElement('afterend', section);
    else if (thesis) thesis.insertAdjacentElement('afterend', section);
    else {
      const first = Array.from(main.children).find(node => node.tagName === 'SECTION');
      if (first) first.insertAdjacentElement('afterend', section);
      else main.prepend(section);
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, { once: true });
  else mount();
  window.setTimeout(mount, 1700);
})();

(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const isEs = path.includes('/por-derecho/es/');
  const isEn = path.includes('/por-derecho/en/');
  if (!isEs && !isEn) return;

  const exactRoutes = [
    '/es/administrador-concursal-puerta-credito-titulo/',
    '/en/insolvency-administrator-credit-to-title-gatekeeper/',
    '/es/pacto-comisorio-arquitectura-credito-titulo/',
    '/en/pacto-comisorio-credit-to-title-architecture/',
    '/es/perimetro-ph122-cerberus-haya-bankia-externo/',
    '/en/ph122-cerberus-haya-bankia-external-perimeter/',
    '/es/acreedor-de-registro/responsabilidad/',
    '/en/lender-of-record/liability/',
    '/es/administrador-concursal-punto-quiebre-lealtad/',
    '/en/insolvency-administrator-loyalty-breakpoint/',
    '/es/concurso-36-2012-administrador-concursal/',
    '/en/insolvency-36-2012-insolvency-administrator/',
    '/es/convergencia-venta-acreedor/',
    '/en/sale-lender-convergence/'
  ];
  const routeMatch = exactRoutes.some(route => path.includes(route));
  const thematicMatch = [
    '/1041-', '/retracto-', '/litigious-credit-', '/article-1535', '/articulo-1535'
  ].some(fragment => path.includes(fragment));
  const dedicated = path.includes('/es/desistimiento-pp1041-autoridad-autenticidad-beneficio/') ||
    path.includes('/en/pp1041-withdrawal-authority-authenticity-benefit/');
  if (!routeMatch && !thematicMatch && !dedicated) return;

  const replacementsEs = [
    ['LPB desistió después y el procedimiento terminó por ese desistimiento.', 'Después se presentó un desistimiento en nombre de LPB y el procedimiento terminó por esa presentación; el expediente disponible no acredita que LPB adoptara voluntariamente esa decisión.'],
    ['El Decreto de 5 marzo 2018 registra el desistimiento de LPB', 'El Decreto de 5 marzo 2018 registra que se solicitó un desistimiento en nombre de LPB'],
    ['El Decreto posterior prueba que LPB desistió y que el procedimiento terminó por esa causa.', 'El Decreto posterior prueba que se presentó un desistimiento en nombre de LPB y que el procedimiento terminó por esa presentación; no identifica todavía quién lo instruyó, redactó, firmó o presentó ni acredita una voluntad auténtica de LPB.'],
    ['LPB posteriormente desistió', 'posteriormente se presentó un desistimiento en nombre de LPB'],
    ['LPB desistió', 'se presentó un desistimiento en nombre de LPB']
  ];
  const replacementsEn = [
    ['LPB then withdrew, and the proceeding ended because of that withdrawal.', "A withdrawal was then filed in LPB's name, and the proceeding ended on that filing; the available record does not establish that LPB voluntarily adopted that decision."],
    ["The 5 March 2018 decree records LPB's withdrawal", "The 5 March 2018 decree records that a withdrawal was requested in LPB's name"],
    ['The later decree proves that LPB withdrew and that the proceeding ended on that basis.', "The later decree proves that a withdrawal was filed in LPB's name and that the proceeding ended on that filing; it does not yet identify who instructed, drafted, signed or filed it or establish an authentic LPB decision."],
    ['LPB subsequently withdrew', "a withdrawal was subsequently filed in LPB's name"],
    ['LPB withdrew', "a withdrawal was filed in LPB's name"]
  ];

  const replaceTextNodes = root => {
    const replacements = isEs ? replacementsEs : replacementsEn;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        const parent = node.parentElement;
        if (!parent || ['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEXTAREA'].includes(parent.tagName)) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(node => {
      let value = node.nodeValue || '';
      replacements.forEach(([from, to]) => {
        value = value.split(from).join(to);
      });
      node.nodeValue = value;
    });
  };

  const style = document.createElement('style');
  style.textContent = `
    #pp1041-authority-correction{background:#fff1f1;padding:1.2rem 0;border-top:4px solid #7c1010;border-bottom:4px solid #7c1010}
    #pp1041-authority-correction .pp1041-wrap{max-width:1120px;margin:0 auto;padding:0 1rem}
    #pp1041-authority-correction .pp1041-red{background:#7c1010;color:#fff;border:3px solid #e55252;border-radius:18px;padding:1.2rem 1.35rem;box-shadow:0 14px 34px rgba(78,5,5,.22)}
    #pp1041-authority-correction .pp1041-label{display:block;color:#ffd8a3;font-size:.76rem;font-weight:900;letter-spacing:.09em;text-transform:uppercase;margin-bottom:.35rem}
    #pp1041-authority-correction h2{color:#fff;margin:.1rem 0 .65rem;font-size:clamp(1.35rem,2.5vw,2rem)}
    #pp1041-authority-correction p{color:#fff;line-height:1.62;margin:.55rem 0}
    #pp1041-authority-correction strong{color:#fff0b6}
    #pp1041-authority-correction .pp1041-proof{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.28);border-radius:12px;padding:.85rem .95rem;margin:.8rem 0}
    #pp1041-authority-correction .pp1041-boundary{font-size:.9rem;color:#ffe8e8}
    #pp1041-authority-correction a{display:inline-block;margin-top:.55rem;background:#fff;color:#641010;text-decoration:none;font-weight:900;border-radius:999px;padding:.62rem .92rem}
  `;
  document.head.appendChild(style);

  const inject = () => {
    const main = document.querySelector('main') || document.body;
    replaceTextNodes(main);
    if (dedicated || document.getElementById('pp1041-authority-correction')) return;

    const section = document.createElement('section');
    section.id = 'pp1041-authority-correction';
    section.setAttribute('role', 'alert');
    section.setAttribute('aria-live', 'polite');

    if (isEs) {
      section.innerHTML = `
        <div class="pp1041-wrap"><div class="pp1041-red">
          <span class="pp1041-label">CORRECCIÓN CENTRAL · PP 1041/2017 · AUTORIDAD, AUTENTICIDAD Y BENEFICIO</span>
          <h2>No está acreditado que LPB desistiera voluntariamente. Está acreditado que se presentó un desistimiento en su nombre.</h2>
          <div class="pp1041-proof"><strong>Cadena primaria:</strong> el 12 enero 2018 el Juzgado ordenó a CAM exhibir la escritura PH122→CAM y revelar precio, fecha de pago y costes; CAM invocó después la necesidad de conformidad de la Administración Concursal; el 25 enero el Administrador cesó al letrado que había obtenido esa orden y controló al procurador; un desistimiento fue presentado en nombre de LPB; el Decreto de 5 marzo terminó la vía y mostró al propio Administrador como abogado de LPB.</div>
          <p><strong>Alegación formal de Por Derecho:</strong> el desistimiento fue una atribución procesal falsa e ilegítima a LPB, no una voluntad auténtica de la concursada; se produjo sin autorización del juez del concurso localizada hasta hoy, en perjuicio deliberado de LPB y de la masa, y eliminó una vía capaz de revelar el precio de adquisición del crédito y preservar una salida de reducción/extinción de deuda y viabilidad.</p>
          <p>Por Derecho sostiene que el Administrador actuó en este episodio como <strong>agente funcional de facto del perímetro CAM/Acosta Matos</strong>, para el beneficio objetivo de ese perímetro y de sus decisores/beneficiarios a determinar, incluidos José Daniel Acosta Matos y Laura Patricia Acosta Matos. La tesis exige obtener instrucciones, comunicaciones, conflictos, autorización judicial, metadatos LexNET, firma, presentación y beneficio; no se presenta como condena penal firme.</p>
          <p class="pp1041-boundary">La Ley Concursal entonces aplicable exigía autorización del juez del concurso para que la Administración Concursal desistiera de un procedimiento en trámite bajo suspensión de facultades. No se ha localizado todavía esa autorización en el material disponible. El expediente certificado del Juzgado debe resolverlo.</p>
          <a href="/por-derecho/es/desistimiento-pp1041-autoridad-autenticidad-beneficio/">Abrir el expediente unitario en rojo →</a>
        </div></div>`;
    } else {
      section.innerHTML = `
        <div class="pp1041-wrap"><div class="pp1041-red">
          <span class="pp1041-label">CENTRAL CORRECTION · PP 1041/2017 · AUTHORITY, AUTHENTICITY AND BENEFIT</span>
          <h2>It is not established that LPB voluntarily withdrew. It is established that a withdrawal was filed in LPB's name.</h2>
          <div class="pp1041-proof"><strong>Primary chain:</strong> on 12 January 2018 the Court ordered CAM to produce the PH122→CAM deed and disclose price, payment date and costs; CAM then invoked the need for Insolvency Administrator conformity; on 25 January the Administrator removed the lawyer who had obtained that order and controlled the procurator; a withdrawal was filed in LPB's name; the 5 March decree ended the route and listed the Administrator himself as LPB's lawyer.</div>
          <p><strong>Por Derecho's formal allegation:</strong> the withdrawal was a false and illegitimate procedural attribution to LPB, not an authentic decision of the insolvent company; it occurred without any insolvency-judge authorisation located to date, deliberately harmed LPB and the estate, and eliminated a route capable of revealing the credit-acquisition price and preserving a debt-reduction/extinguishment and viability exit.</p>
          <p>Por Derecho alleges that in this episode the Administrator acted as a <strong>de facto functional agent for the CAM/Acosta Matos perimeter</strong>, for the objective benefit of that perimeter and decision-makers/beneficiaries to be determined, including José Daniel Acosta Matos and Laura Patricia Acosta Matos. The case requires the instruction, communications, conflicts, judicial authorisation, LexNET metadata, signature, filing and benefit records; it is not presented as a final criminal conviction.</p>
          <p class="pp1041-boundary">The then-applicable Insolvency Act required insolvency-court authorisation for the Administrator to withdraw pending proceedings where the debtor's powers were suspended. No such authorisation has yet been located in the available material. The certified court file must resolve the point.</p>
          <a href="/por-derecho/en/pp1041-withdrawal-authority-authenticity-benefit/">Open the unitary red record →</a>
        </div></div>`;
    }

    const hero = main.querySelector('.hero');
    if (hero) hero.insertAdjacentElement('afterend', section);
    else main.prepend(section);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject, { once: true });
  } else {
    inject();
  }
})();

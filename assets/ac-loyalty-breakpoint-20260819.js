(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const id = 'ac-loyalty-breakpoint-19aug2026';
  if (document.getElementById(id)) return;

  const isEs = path.includes('/por-derecho/es/');
  const isEn = path.includes('/por-derecho/en/');
  if (!isEs && !isEn) return;

  const utilityFragments = [
    '/buscar/', '/search/', '/aviso-legal-privacidad/', '/legal-privacy/',
    '/actualizaciones/', '/updates/', '/libros/', '/books/'
  ];
  if (utilityFragments.some(fragment => path.includes(fragment))) return;

  const coreFragments = [
    'administrador-concursal', 'insolvency-administrator',
    'acosta-matos', 'retracto', 'article-1535', 'articulo-1535',
    'comunidad', 'community', 'actas', 'explotacion', 'exploitation',
    'toma-control', 'takeover', 'mismo-hotel', 'same-hotel',
    'insolvencia-lpb', 'lpb-insolvency', 'convergencia-venta-acreedor', 'sale-lender-convergence',
    'responsabilidad-institucional', 'institutional-accountability',
    'recuperacion-restitucion', 'recovery-restitution',
    'ricpe', 'fondos-incentivos', 'institutionalisation-chain'
  ];
  const isCore = coreFragments.some(fragment => path.includes(fragment));

  const style = document.createElement('style');
  style.textContent = `
    #${id}{background:#f5f3ee}
    #${id} .aclb-wrap{max-width:1120px;margin:0 auto}
    #${id} .aclb-card{background:#17242b;color:#fff;border-radius:18px;padding:1.05rem 1.25rem;box-shadow:0 10px 28px rgba(19,37,45,.10)}
    #${id} .aclb-label{display:block;font-size:.75rem;font-weight:850;letter-spacing:.08em;text-transform:uppercase;color:#ffe6a8;margin-bottom:.4rem}
    #${id} h2{color:#fff;margin:.1rem 0 .55rem;font-size:1.3rem}
    #${id} p{line-height:1.55;margin:.4rem 0}
    #${id} .aclb-flow{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:.8rem .9rem;margin:.8rem 0;font-weight:750}
    #${id} .aclb-boundary{font-size:.9rem;color:#f1dfdb;margin-top:.65rem}
    #${id} .aclb-actions{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:.85rem}
    #${id} .aclb-actions a{display:inline-block;background:#fff;color:#17242b;text-decoration:none;font-weight:800;border-radius:999px;padding:.58rem .88rem}
    #${id} .aclb-actions a.secondary{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.5)}
    #${id}.compact .aclb-card{padding:.9rem 1.1rem}
    #${id}.compact h2{font-size:1.12rem}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.id = id;
  section.className = `section${isCore ? '' : ' compact'}`;

  if (isEs) {
    section.innerHTML = isCore ? `
      <div class="shell aclb-wrap"><div class="aclb-card">
        <span class="aclb-label">PREGUNTA TRANSVERSAL · PUNTO DE QUIEBRE DE LEALTAD</span>
        <h2>¿Cuándo dejó la AC —si ocurrió— de administrar lealmente para LPB y empezó a funcionar en interés de partes adversas?</h2>
        <p>La prueba no empieza con Acosta Matos. Debe retroceder a la fractura de la venta/explotación de 2008 y al perímetro privado Monte Lanza/Molina, y después determinar si CAM simplemente heredó ese conflicto o si lo adoptó y amplificó con conocimiento, apoyo o cooperación de la Administración Concursal.</p>
        <div class="aclb-flow">2008 → arquitectura privada adversa → deuda / votos / acceso → actos u omisiones AC → entrada CAM → crédito / control → junio 2018 → liquidación / adjudicación</div>
        <p><strong>Prueba de validez:</strong> si existía ya un conflicto material antes de que la AC controlara abogados, accesos, recuperación o retractos/tanteos de LPB, ¿qué actos posteriores dependían de ese poder y qué eficacia jurídica conservan?</p>
        <p class="aclb-boundary"><strong>Límite:</strong> Por Derecho plantea una hipótesis de conflicto y continuidad funcional. No publica como hecho que la AC fuera agente de la familia Molina o de CAM, ni que existiera colusión, ni que todo acto posterior sea automáticamente nulo.</p>
        <div class="aclb-actions"><a href="/por-derecho/es/administrador-concursal-punto-quiebre-lealtad/">Abrir análisis completo →</a><a class="secondary" href="/por-derecho/es/retracto-credito-litigioso-1041-2017/">Aplicarlo a DP 1041</a></div>
      </div></div>` : `
      <div class="shell aclb-wrap"><div class="aclb-card">
        <span class="aclb-label">PREGUNTA GLOBAL DE CONTROL</span>
        <h2>¿Dónde está el punto de quiebre de lealtad de la Administración Concursal?</h2>
        <p>En cada tramo de esta historia, Por Derecho pregunta si la AC seguía actuando para LPB/la masa o si comenzó a validar o ejecutar funcionalmente intereses privados adversos. La respuesta debe reconstruirse desde el perímetro pre-CAM hasta Acosta Matos, acto por acto.</p>
        <div class="aclb-actions"><a href="/por-derecho/es/administrador-concursal-punto-quiebre-lealtad/">Ver la prueba transversal →</a></div>
      </div></div>`;
  } else {
    section.innerHTML = isCore ? `
      <div class="shell aclb-wrap"><div class="aclb-card">
        <span class="aclb-label">CROSS-CUTTING QUESTION · LOYALTY BREAKPOINT</span>
        <h2>When, if ever, did the insolvency administration stop administering loyally for LPB and begin functioning in the interests of adverse parties?</h2>
        <p>The test does not start with Acosta Matos. It must run backwards to the fracture of the 2008 sale/operating architecture and the Monte Lanza/Molina private perimeter, then determine whether CAM merely inherited that conflict or knowingly adopted and amplified it with administrator support or cooperation.</p>
        <div class="aclb-flow">2008 → adverse private architecture → debt / votes / access → administrator acts or omissions → CAM entry → credit / control → June 2018 → liquidation / adjudication</div>
        <p><strong>Validity test:</strong> if a material conflict already existed before the administrator controlled LPB's lawyers, access, recovery routes or retracto/tanteo protections, which later acts depended on that power and what legal effect do they retain?</p>
        <p class="aclb-boundary"><strong>Boundary:</strong> Por Derecho advances a conflict/functional-continuity hypothesis. It does not publish as fact that the administrator was an agent of Molina-family interests or CAM, that collusion is established, or that every later act is automatically void.</p>
        <div class="aclb-actions"><a href="/por-derecho/en/insolvency-administrator-loyalty-breakpoint/">Open full analysis →</a><a class="secondary" href="/por-derecho/en/litigious-credit-retracto-1041-2017/">Apply it to PP 1041</a></div>
      </div></div>` : `
      <div class="shell aclb-wrap"><div class="aclb-card">
        <span class="aclb-label">GLOBAL CONTROL QUESTION</span>
        <h2>Where is the insolvency administrator's loyalty breakpoint?</h2>
        <p>At every stage, Por Derecho asks whether the administrator was still acting for LPB/the estate or had begun validating or functionally implementing adverse private interests. The answer must be reconstructed from the pre-CAM perimeter through Acosta Matos, act by act.</p>
        <div class="aclb-actions"><a href="/por-derecho/en/insolvency-administrator-loyalty-breakpoint/">Open cross-cutting test →</a></div>
      </div></div>`;
  }

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector(':scope > .hero, :scope > section.hero, :scope > .dossier-hero, :scope > .cnmv-hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else main.insertAdjacentElement('afterbegin', section);
})();

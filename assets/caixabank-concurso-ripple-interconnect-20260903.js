(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const localPath = path.startsWith('/por-derecho/') ? path : `/por-derecho${path.startsWith('/') ? '' : '/'}${path}`;
  if (document.documentElement.dataset.caixaConcursoRipple === '20260903b') return;

  const routes = new Set([
    '/por-derecho/es/reclamacion-caixabank-valencia/',
    '/por-derecho/en/caixabank-valencia-claim/',
    '/por-derecho/es/insolvencia-lpb/',
    '/por-derecho/en/lpb-insolvency/',
    '/por-derecho/es/acreedor-de-registro/',
    '/por-derecho/en/lender-of-record/',
    '/por-derecho/es/convergencia-venta-acreedor/',
    '/por-derecho/en/sale-lender-convergence/',
    '/por-derecho/es/objetivos-recuperacion-restitucion/',
    '/por-derecho/en/recovery-restitution-objectives/',
    '/por-derecho/es/concurso-36-2012-separacion-administrador-concursal-rpl-3304-2025/',
    '/por-derecho/en/insolvency-36-2012-administrator-removal-rpl-3304-2025/',
    '/por-derecho/es/concurso-36-2012-administrador-concursal/',
    '/por-derecho/en/insolvency-36-2012-insolvency-administrator/',
    '/por-derecho/es/concurso-36-2012-separacion-ac-honorarios/',
    '/por-derecho/en/insolvency-36-2012-administrator-removal-fees/'
  ]);
  if (!routes.has(localPath)) return;
  document.documentElement.dataset.caixaConcursoRipple = '20260903b';

  const es = localPath.includes('/es/');
  const base = '/por-derecho';
  const hub = es ? `${base}/es/caixabank-concurso-efecto-domino/` : `${base}/en/caixabank-insolvency-ripple/`;
  const caixa = es ? `${base}/es/reclamacion-caixabank-valencia/` : `${base}/en/caixabank-valencia-claim/`;
  const concurso = es ? `${base}/es/insolvencia-lpb/` : `${base}/en/lpb-insolvency/`;
  const creditor = es ? `${base}/es/convergencia-venta-acreedor/` : `${base}/en/sale-lender-convergence/`;
  const recovery = es ? `${base}/es/objetivos-recuperacion-restitucion/` : `${base}/en/recovery-restitution-objectives/`;
  const separation = es ? `${base}/es/concurso-36-2012-separacion-administrador-concursal-rpl-3304-2025/` : `${base}/en/insolvency-36-2012-administrator-removal-rpl-3304-2025/`;

  const style = document.createElement('style');
  style.textContent = `
  .pd-ripple{margin:1.2rem auto;max-width:1180px;padding:0 1rem}.pd-ripple-box{background:#fff;border:1px solid rgba(19,37,45,.17);border-radius:18px;padding:1.25rem;box-shadow:0 14px 34px rgba(19,37,45,.08)}
  .pd-ripple-head{display:grid;grid-template-columns:1.5fr 1fr;gap:1rem;align-items:start}.pd-ripple-head h2{margin:.2rem 0 .55rem}.pd-ripple-kicker{font-size:.78rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#7b571e}
  .pd-domino{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:.5rem;margin:1rem 0}.pd-node{position:relative;background:#f7f3e8;border:1px solid #dfd0ab;border-radius:12px;padding:.75rem;font-size:.86rem;font-weight:750;min-height:92px}.pd-node:not(:last-child)::after{content:'→';position:absolute;right:-.48rem;top:35%;z-index:2;font-size:1.25rem;color:#8c6b2f;background:#fff;border-radius:99px;padding:0 .08rem}.pd-limit{background:#fff8e8;border-left:5px solid #8c6b2f;padding:.8rem 1rem;margin:.8rem 0;font-size:.92rem}.pd-links{display:flex;flex-wrap:wrap;gap:.5rem}.pd-links a{display:inline-block;padding:.45rem .65rem;border:1px solid #17313a;border-radius:999px;text-decoration:none;font-size:.86rem}.pd-source{display:grid;grid-template-columns:140px 1fr;gap:.8rem;align-items:center;background:#f4f7f8;border-radius:12px;padding:.8rem}.pd-source img{width:100%;border-radius:8px;border:1px solid #ccd4d7}.pd-risk{border-left:5px solid #8c2f2c;background:#fff5f4;padding:.8rem 1rem;margin:.8rem 0}.pd-ripple sup{font-weight:900;color:#8c2f2c}@media(max-width:850px){.pd-ripple-head{grid-template-columns:1fr}.pd-domino{grid-template-columns:1fr}.pd-node{min-height:0}.pd-node:not(:last-child)::after{content:'↓';right:50%;top:auto;bottom:-.85rem}.pd-source{grid-template-columns:95px 1fr}}
  `;
  document.head.appendChild(style);

  const isCaixa = localPath.endsWith(es ? '/es/reclamacion-caixabank-valencia/' : '/en/caixabank-valencia-claim/');
  const isSeparation = localPath.includes('separacion-administrador-concursal-rpl-3304-2025') || localPath.includes('administrator-removal-rpl-3304-2025');
  const section = document.createElement('section');
  section.className = 'pd-ripple';
  section.setAttribute('data-caixabank-concurso-ripple', '20260903b');
  const courtCard = isCaixa ? (es
    ? `<div class="pd-source"><a href="${base}/es/reclamacion-caixabank-valencia/senalamiento-28-enero-2027/"><img src="${base}/assets/evidence/caixabank-valencia-1859-2023-diligencia-06nov2025-p1-publica.jpg" alt="Diligencia judicial pública, 6 de noviembre de 2025"></a><div><strong>Fuente procesal primaria visible.</strong><p>La diligencia firmada el 6 de noviembre de 2025 fija la vista de ORD 1859/2023-9 para el <strong>28 de enero de 2027 a las 10:00</strong>. <a href="${base}/es/reclamacion-caixabank-valencia/senalamiento-28-enero-2027/">Abrir las dos páginas públicas redactadas →</a></p></div></div>`
    : `<div class="pd-source"><a href="${base}/es/reclamacion-caixabank-valencia/senalamiento-28-enero-2027/"><img src="${base}/assets/evidence/caixabank-valencia-1859-2023-diligencia-06nov2025-p1-publica.jpg" alt="Public court diligence, 6 November 2025"></a><div><strong>Visible primary procedural source.</strong><p>The signed 6 November 2025 diligence sets ORD 1859/2023-9 for <strong>28 January 2027 at 10:00</strong>. <a href="${base}/es/reclamacion-caixabank-valencia/senalamiento-28-enero-2027/">Open the two redacted public court pages →</a></p></div></div>`) : '';
  const risk = isSeparation ? (es
    ? `<div class="pd-risk"><strong>Riesgo institucional alegado · no hecho adjudicado.</strong> Por Derecho y Aweswell alegan un patrón de obstrucción de vías de salida o recuperación económica del concurso. Sobre esa tesis, la permanencia de Francisco de Borja Rodríguez-Batllori Laffitte como administrador concursal durante cualquier resultado material de CaixaBank conservaría su capacidad institucional para intervenir en la posterior implementación concursal. Esta conexión explica urgencia y riesgo; <strong>no demuestra intención futura de sabotaje, concierto con el órgano judicial ni nulidad automática</strong>.</div>`
    : `<div class="pd-risk"><strong>Alleged institutional risk · not an adjudicated fact.</strong> Por Derecho and Aweswell allege a pattern of obstruction affecting routes out of, or economic recovery from, the insolvency. On that case theory, Francisco de Borja Rodríguez-Batllori Laffitte remaining insolvency administrator through any material CaixaBank outcome would preserve his institutional capacity to participate in later insolvency implementation. This explains claimed urgency and risk; it <strong>does not prove future intent to obstruct, concert with the court, or automatic invalidity</strong>.</div>`) : '';
  section.innerHTML = es ? `<div class="pd-ripple-box"><div class="pd-ripple-head"><div><div class="pd-ripple-kicker">INTERCONEXIÓN OBLIGATORIA · CAIXABANK ↔ CONCURSO 36/2012</div><h2>Una relación económica adquirió múltiples vidas jurídicas.</h2><p>Cualquier sentencia, nulidad, ajuste, workout o acuerdo en Valencia debe analizarse hacia atrás hasta el paquete 2008–2012 y hacia delante hasta concurso, crédito transferido, posesión, recuperación y rendición de cuentas. La continuidad económica <strong>no fusiona capacidades jurídicas</strong>.</p></div><p><a class="button" href="${hub}">Abrir mapa unitario y escenarios →</a></p></div>${courtCard}<div class="pd-domino"><div class="pd-node">1 · Resultado CaixaBank<br><small>sentencia / nulidad / acuerdo / ajuste</small></div><div class="pd-node">2 · Mayor bancario<br><small>swap · suelo · prenda · interés · cuentas</small></div><div class="pd-node">3 · 2011–2012<br><small>mora · vencimiento · ejecución</small></div><div class="pd-node">4 · Concurso 36/2012<br><small>importe · clasificación · pagos · decisiones</small></div><div class="pd-node">5 · Bankia→SAREB→PH122→CAM<br><small>qué derecho/importe pasó realmente</small></div><div class="pd-node">6 · Recuperación / separación AC<br><small>efectos y responsabilidades actor por actor</small></div></div><div class="pd-limit"><strong>Regla de indeclinabilidad analítica:</strong> ningún carril puede resolver sus cifras ignorando los demás cuando dependen del mismo saldo, pago, activo o acto. <strong>Regla jurídica:</strong> cada flecha significa posible revisión consecuencial, no nulidad automática.</div>${risk}<div class="pd-links"><a href="${caixa}">CaixaBank / Valencia</a><a href="${concurso}">Concurso LPB</a><a href="${creditor}">Cadena acreedor / posesión</a><a href="${recovery}">Recuperación</a><a href="${separation}">Separación AC · RPL 3304/3319</a><a href="${base}/es/registro-identidad-profesionales-justicia/">Registro ^</a></div></div>`
    : `<div class="pd-ripple-box"><div class="pd-ripple-head"><div><div class="pd-ripple-kicker">MANDATORY INTERCONNECTION · CAIXABANK ↔ INSOLVENCY 36/2012</div><h2>One economic relationship acquired multiple legal lives.</h2><p>Any judgment, nullity, adjustment, workout or settlement in Valencia must be tested backward against the 2008–2012 package and forward through insolvency, transferred credit, possession, recovery and accountability. Economic continuity <strong>does not merge legal capacities</strong>.</p></div><p><a class="button" href="${hub}">Open unitary map and scenarios →</a></p></div>${courtCard}<div class="pd-domino"><div class="pd-node">1 · CaixaBank outcome<br><small>judgment / nullity / settlement / adjustment</small></div><div class="pd-node">2 · Bank ledger<br><small>swap · floor · pledge · interest · accounts</small></div><div class="pd-node">3 · 2011–2012<br><small>default · acceleration · enforcement</small></div><div class="pd-node">4 · Insolvency 36/2012<br><small>amount · ranking · payments · decisions</small></div><div class="pd-node">5 · Bankia→SAREB→PH122→CAM<br><small>what right/amount actually travelled</small></div><div class="pd-node">6 · Recovery / AC removal<br><small>effects and responsibility actor by actor</small></div></div><div class="pd-limit"><strong>Analytical non-declinability rule:</strong> no track may determine figures while ignoring another track that depends on the same balance, payment, asset or act. <strong>Legal rule:</strong> each arrow means potential consequential review, not automatic invalidity.</div>${risk}<div class="pd-links"><a href="${caixa}">CaixaBank / Valencia</a><a href="${concurso}">LPB insolvency</a><a href="${creditor}">Creditor / possession chain</a><a href="${recovery}">Recovery</a><a href="${separation}">AC removal · RPL 3304/3319</a><a href="${base}/en/justice-professionals-identity-register/">^ register</a></div></div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector('.hero, .dossier-hero, section');
  if (hero && hero.parentElement === main) hero.insertAdjacentElement('afterend', section);
  else main.insertAdjacentElement('afterbegin', section);
})();
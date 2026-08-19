(() => {
  const path = location.pathname.replace(/\/+$/, '/');
  const isEs = path.includes('/es/');
  const id = 'public-authority-case-reconstruction-gateway-17aug2026';
  if (document.getElementById(id)) return;

  const dedicatedRoutes = [
    '/es/reconstruccion-unitaria-autoridades-publicas/',
    '/en/public-authority-unitary-case-reconstruction/',
    '/es/cnmv-ricpe-verificacion/',
    '/en/cnmv-ricpe-verification/',
    '/es/snca-fondos-europeos-trazabilidad/',
    '/en/snca-eu-funds-traceability/',
    '/es/incentivos-regionales-gc836-p06/',
    '/en/regional-incentives-gc836-p06/',
    '/es/ric-private-equity-sun-park/',
    '/en/ric-private-equity-sun-park/'
  ];
  if (dedicatedRoutes.some(route => path.endsWith(route))) return;

  const targets = [
    /\/por-derecho\/es\/?$/,
    /\/por-derecho\/en\/?$/,
    /registros-institucionales|institutional-records/,
    /yaiza-trazabilidad-institucional|yaiza-institutional-traceability/,
    /cabildo-lanzarote-turismo-trazabilidad|cabildo-lanzarote-tourism-traceability/,
    /cadena-instrumentalizacion-ric-fondos-incentivos|institutionalisation-chain-ric-eu-incentives/,
    /mismo-hotel-multiples-vidas-financieras|same-hotel-multiple-financial-lives/,
    /ricpe-responsabilidad-documental|ricpe-documentary-accountability/,
    /fiscalia-dip-2-2026|dp-1901-2026/,
    /concurso-36-2012-responsabilidad-institucional|insolvency-36-2012-institutional-accountability/,
    /concurso-36-2012-juzgado-mercantil-1|insolvency-36-2012-mercantile-court-1/,
    /concurso-36-2012-administrador-concursal|insolvency-36-2012-insolvency-administrator/,
    /comunidad-instrumentalizacion|community-instrumentalisation/,
    /toma-control-sun-park-7-junio-2018|sun-park-takeover-7-june-2018/,
    /calificacion-concurso-36-2012-vidas-paralelas|insolvency-classification-parallel-lives/
  ];
  if (!targets.some(re => re.test(path))) return;

  const main = document.querySelector('main');
  if (!main) return;

  const style = document.createElement('style');
  style.textContent = `
    #${id}{padding:.85rem 0;background:#eef2f1;border-top:1px solid rgba(19,37,45,.12);border-bottom:1px solid rgba(19,37,45,.12)}
    #${id} .par-inner{display:grid;grid-template-columns:1fr auto;gap:1rem;align-items:center}
    #${id} .par-kicker{font-size:.7rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#6b5841;margin:0 0 .25rem}
    #${id} h2{font-size:1.05rem;margin:0 0 .28rem;color:#13252d}
    #${id} p{font-size:.88rem;line-height:1.45;margin:0;max-width:860px;color:#38464b}
    #${id} .par-badges{display:flex;gap:.35rem;flex-wrap:wrap;margin-top:.5rem}
    #${id} .par-badge{font-size:.64rem;font-weight:850;letter-spacing:.035em;text-transform:uppercase;background:#fff;border:1px solid rgba(19,37,45,.18);border-radius:999px;padding:.2rem .42rem;color:#13252d}
    #${id} a.par-open{display:inline-block;text-decoration:none;white-space:nowrap;background:#13252d;color:#fff;border-radius:999px;padding:.65rem .9rem;font-size:.82rem;font-weight:850}
    @media(max-width:820px){#${id} .par-inner{grid-template-columns:1fr}#${id} a.par-open{justify-self:start}}
    @media print{#${id}{display:none!important}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.id = id;
  section.setAttribute('aria-label', isEs ? 'Vista para autoridades y revisión independiente' : 'Public authority and independent review view');
  section.innerHTML = isEs ? `
    <div class="shell par-inner">
      <div><p class="par-kicker">VISTA PROFESIONAL · AUTORIDADES / AUDITORES / FISCALÍA / JUZGADOS</p><h2>Reconstrucción unitaria: una fuente factual, distintas competencias.</h2><p>Siga finca → voto → autoridad → deuda/derecho → recepción institucional → consecuencia, con estados de prueba, evidencia contraria y análisis forense separado de la validez civil o concursal.</p><div class="par-badges"><span class="par-badge">Expediente abierto</span><span class="par-badge">IDs canónicos</span><span class="par-badge">Evidencia contraria</span><span class="par-badge">Competencias separadas</span><span class="par-badge">No exige aceptar la teoría global</span></div></div>
      <a class="par-open" href="/por-derecho/es/reconstruccion-unitaria-autoridades-publicas/">Abrir revisión independiente →</a>
    </div>` : `
    <div class="shell par-inner">
      <div><p class="par-kicker">PROFESSIONAL VIEW · AUTHORITIES / AUDITORS / PROSECUTORS / COURTS</p><h2>Unitary reconstruction: one factual layer, different lawful competences.</h2><p>Follow property → vote → authority → debt/right → institutional receipt → consequence, with evidence status, contrary material and forensic analysis separated from civil or insolvency validity.</p><div class="par-badges"><span class="par-badge">Open file</span><span class="par-badge">Canonical IDs</span><span class="par-badge">Contrary evidence</span><span class="par-badge">Separate competences</span><span class="par-badge">No need to adopt the global theory</span></div></div>
      <a class="par-open" href="/por-derecho/en/public-authority-unitary-case-reconstruction/">Open independent review →</a>
    </div>`;

  const hero = main.querySelector(':scope > .dossier-hero, :scope > .cnmv-hero, :scope > .hero, :scope > section.hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else main.insertAdjacentElement('afterbegin', section);
})();

// 19-Aug-2026: unitary Control 22/24 liability layer. Kept as an independent loader so
// the criminal/institutional module is available on CAM and DP1956 routes even when
// the public-authority gateway above intentionally returns early on a given page.
(() => {
  if (document.querySelector('script[data-control22-24-unitary]')) return;
  const script = document.createElement('script');
  script.src = new URL('control22-24-unitary-liability-20260819.js?v=20260819a', document.currentScript?.src || location.href).href;
  script.async = false;
  script.dataset.control22_24Unitary = '1';
  document.head.appendChild(script);
})();
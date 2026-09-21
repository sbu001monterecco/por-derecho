(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const lang = (document.documentElement.lang || (path.includes('/en/') ? 'en' : 'es')).toLowerCase().startsWith('en') ? 'en' : 'es';
  const canonical = lang === 'en'
    ? '/por-derecho/en/matkator-8584-hotel-title-remate-restitution/'
    : '/por-derecho/es/matkator-8584-titulo-hotel-remate-restitucion/';
  if (path.includes('/matkator-8584-titulo-hotel-remate-restitucion/') || path.includes('/matkator-8584-hotel-title-remate-restitution/')) return;

  const exactRelevant = [
    '/es/digest-penal-unitario-2026-09-03/','/en/unitary-criminal-digest-2026-09-03/',
    '/es/etj-163-2020/','/en/etj-163-2020/',
    '/es/dp-748-2026/','/en/dp-748-2026/',
    '/es/cambiario-1048-2019/','/en/cambiario-1048-2019/',
    '/es/cuatrecasas-sun-park/','/en/cuatrecasas-sun-park/',
    '/es/cuatrecasas-dp748-accion-civil/','/en/cuatrecasas-dp748-civil-action/',
    '/es/matkator-dp552-dp711-etj163-continuidad/','/en/matkator-dp552-dp711-etj163-continuity/',
    '/es/registro-activos-derechos-matkator/','/en/matkator-asset-rights-register/',
    '/es/ingenieria-inversa-360-cadena-sun-park/','/en/reverse-engineering-360-sun-park-chain/',
    '/es/ingenieria-forense-criminal-sun-park/','/en/sun-park-criminal-engineering-investigation/',
    '/es/toma-control-sun-park-7-junio-2018/','/en/sun-park-takeover-7-june-2018/',
    '/es/adjudicacion-2022-reconstruccion-documental/','/en/2022-adjudication-documentary-reconstruction/'
  ];
  const relevantFragments = [
    'concurso-36-2012','insolvency-36-2012','ona-hotels','calificacion','rpl-2523','rpl-3304','rpl-3319',
    'administrador-concursal','acosta-matos','hotel-new-trend','canarian-hospitality','mynd',
    'ricpe','ric-private-equity','feder','incentivos','intervencion','aeat','onif','cnmv',
    'fiscalia','eg-745','yaiza','asset-recovery','recuperacion-activos'
  ];
  const isHome = /\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(path);
  const isRelevant = exactRelevant.some(p => path.includes(p)) || relevantFragments.some(f => path.includes(f));
  if (!isHome && !isRelevant) return;

  const addStyle = () => {
    if (document.getElementById('pd-mat8584-critical-style')) return;
    const style = document.createElement('style');
    style.id = 'pd-mat8584-critical-style';
    style.textContent = `
      .pd-mat8584-critical{background:linear-gradient(135deg,#10262d,#173d42 68%,#75581d);color:#fff;padding:2.25rem 0;position:relative;z-index:1}
      .pd-mat8584-critical h2{color:#fff;max-width:980px;margin:.25rem 0 .7rem}.pd-mat8584-critical p{color:#e8efee;max-width:1050px;line-height:1.62}
      .pd-mat8584-critical .pd-mat8584-ey{font-size:.74rem;font-weight:850;letter-spacing:.055em;text-transform:uppercase;color:#f2d47b}
      .pd-mat8584-critical .pd-mat8584-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.7rem;margin:1rem 0}
      .pd-mat8584-critical .pd-mat8584-card{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.24);border-radius:14px;padding:.9rem}
      .pd-mat8584-critical .pd-mat8584-card strong{display:block;color:#f2d47b;margin-bottom:.25rem}
      .pd-mat8584-critical .pd-mat8584-links{display:flex;gap:.55rem;flex-wrap:wrap;margin-top:1rem}
      .pd-mat8584-critical .pd-mat8584-links a{display:inline-block;background:#f2d47b;color:#10262d;text-decoration:none;border-radius:999px;padding:.55rem .8rem;font-weight:850}
      .pd-mat8584-critical .pd-mat8584-boundary{border-left:4px solid #f2d47b;padding-left:.85rem;font-size:.9rem;color:#dce8e6}
      .pd-mat8584-home{margin:1.25rem auto;border-radius:22px;overflow:hidden;max-width:1180px;box-shadow:0 18px 44px rgba(16,38,45,.22)}
      @media(max-width:780px){.pd-mat8584-critical .pd-mat8584-grid{grid-template-columns:1fr}.pd-mat8584-critical{padding:1.65rem 0}}
    `;
    document.head.appendChild(style);
  };

  const es = {
    eyebrow: 'ACTUALIZACIÓN CRÍTICA · FINCA 8584 · REMATE · RESTITUCIÓN',
    title: 'No se ejecuta un apartamento autónomo: se dispone de un título integrado en un hotel regulado.',
    intro: 'La titularidad de Matkator es el anclaje de derechos de propiedad, acceso, explotación, contabilidad, prueba y restitución respecto de un espacio que se alega integrado en MYND Yaiza. Por eso la adjudicación puede causar un perjuicio propio antes de cualquier cesión posterior.',
    cards: [
      ['Título ≠ habitación','La finca puede subsistir registralmente mientras su espacio físico, acceso, inventario e ingresos se integran en el hotel.'],
      ['Adjudicación ≠ daño sólo por cesión','La pérdida del título puede fragmentar daños y dificultar acceso, cuentas, restauración y restitución.'],
      ['Formal ≠ beneficiario real','Adjudicatario, cesionario y beneficiario terminal deben identificarse por separado; el perímetro CAM/HNT/Canarian Hospitality es la hipótesis específica, no un hecho probado.']
    ],
    boundary: 'Procesos separados, conexión probatoria real: DP 711 trata la conducta física/operativa alegada; ETJ 163 la disposición actual; DP 748 la posible relevancia penal autónoma; Concurso 36/2012 las consecuencias de unidad productiva, recuperación y rendición de cuentas. No se afirma culpabilidad ni concierto.',
    main: 'Abrir control canónico',
    etj: 'ETJ 163', dp: 'DP 748', mat: 'DP 711 / Matkator', c36: 'Concurso 36/2012', acosta: 'Acosta Matos'
  };
  const en = {
    eyebrow: 'CRITICAL UPDATE · FINCA 8584 · REMATE · RESTITUTION',
    title: 'The execution does not concern an autonomous apartment: it disposes of a title embedded in a regulated hotel.',
    intro: 'Matkator’s title anchors property, access, operation, accounting, evidential and restitution rights over space alleged to have been integrated into MYND Yaiza. Adjudication may therefore create its own injury before any later cession.',
    cards: [
      ['Title ≠ room','The finca may remain registered while its physical space, access, inventory and revenue are integrated into the hotel.'],
      ['Adjudication ≠ cession-only harm','Loss of title may fragment injury and impair access, accounts, restoration and restitution.'],
      ['Formal recipient ≠ real beneficiary','Adjudicatee, assignee and terminal beneficiary must be separated; CAM/HNT/Canarian Hospitality is the specific hypothesis, not a proved fact.']
    ],
    boundary: 'Separate proceedings, real evidential connection: DP 711 concerns the alleged physical/operational conduct; ETJ 163 the current disposition; DP 748 possible autonomous criminal relevance; Concurso 36/2012 productive-unit, recovery and accountability consequences. No guilt or concert is stated as established.',
    main: 'Open canonical control',
    etj: 'ETJ 163', dp: 'DP 748', mat: 'DP 711 / Matkator', c36: 'Concurso 36/2012', acosta: 'Acosta Matos'
  };
  const t = lang === 'en' ? en : es;
  const hrefs = lang === 'en' ? {
    etj:'/por-derecho/en/etj-163-2020/', dp:'/por-derecho/en/dp-748-2026/', mat:'/por-derecho/en/matkator-dp552-dp711-etj163-continuity/',
    c36:'/por-derecho/en/insolvency-36-2012-liquidation-plan-judge-laj-audit/', acosta:'/por-derecho/en/acosta-matos-perimeter/'
  } : {
    etj:'/por-derecho/es/etj-163-2020/', dp:'/por-derecho/es/dp-748-2026/', mat:'/por-derecho/es/matkator-dp552-dp711-etj163-continuidad/',
    c36:'/por-derecho/es/concurso-36-2012-auditoria-plan-liquidacion-juez-laj/', acosta:'/por-derecho/es/acosta-matos-perimetro/'
  };

  const render = () => {
    if (document.querySelector('[data-matkator-8584-critical-update]')) return;
    addStyle();
    const section = document.createElement('section');
    section.className = 'pd-mat8584-critical' + (isHome ? ' pd-mat8584-home' : '');
    section.setAttribute('data-matkator-8584-critical-update','20260903');
    section.innerHTML = `<div class="shell"><p class="pd-mat8584-ey">${t.eyebrow}</p><h2>${t.title}</h2><p>${t.intro}</p><div class="pd-mat8584-grid">${t.cards.map(c=>`<article class="pd-mat8584-card"><strong>${c[0]}</strong><span>${c[1]}</span></article>`).join('')}</div><p class="pd-mat8584-boundary">${t.boundary}</p><div class="pd-mat8584-links"><a href="${canonical}">${t.main}</a><a href="${hrefs.etj}">${t.etj}</a><a href="${hrefs.dp}">${t.dp}</a><a href="${hrefs.mat}">${t.mat}</a><a href="${hrefs.c36}">${t.c36}</a><a href="${hrefs.acosta}">${t.acosta}</a></div></div>`;
    if (isHome) {
      const main = document.querySelector('main');
      if (main) {
        const first = main.querySelector('section');
        if (first && first.nextSibling) main.insertBefore(section, first.nextSibling); else main.prepend(section);
      }
    } else {
      const footer = document.querySelector('footer');
      if (footer && footer.parentNode) footer.parentNode.insertBefore(section, footer); else document.body.appendChild(section);
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render, {once:true}); else render();
})();

(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const lang = (document.documentElement.lang || (path.includes('/en/') ? 'en' : 'es'))
    .toLowerCase().startsWith('en') ? 'en' : 'es';

  const c22Route = lang === 'en'
    ? '/por-derecho/en/control-22-insolvency-administrator-complaint/'
    : '/por-derecho/es/control-22-denuncia-administrador-concursal/';
  const c24Route = lang === 'en'
    ? '/por-derecho/en/control-24-insolvency-judge-complaint-36-2012/'
    : '/por-derecho/es/control-24-denuncia-juez-concurso-36-2012/';
  const dp1956Route = lang === 'en'
    ? '/por-derecho/en/dp-1956-2026/'
    : '/por-derecho/es/dp-1956-2026/';
  const judgeRoute = lang === 'en'
    ? '/por-derecho/en/insolvency-36-2012-mercantile-court-1/'
    : '/por-derecho/es/concurso-36-2012-magistrado-juez/';
  const registerRoute = '/por-derecho/data/control-22-24-interconnection-register.json';

  const ownRoutes = [
    '/es/control-22-denuncia-administrador-concursal/',
    '/en/control-22-insolvency-administrator-complaint/',
    '/es/control-24-denuncia-juez-concurso-36-2012/',
    '/en/control-24-insolvency-judge-complaint-36-2012/'
  ];
  if (ownRoutes.some(route => path.includes(route))) return;

  const relevantFragments = [
    'dp-1956-2026',
    'dp-1901-2026',
    'concurso-36-2012-administrador-concursal',
    'insolvency-36-2012-insolvency-administrator',
    'concurso-36-2012-magistrado-juez',
    'insolvency-36-2012-mercantile-court-1',
    'concurso-36-2012-separacion-ac-honorarios',
    'insolvency-36-2012-administrator-removal-fees',
    'cgpj-supervision-masa-activa',
    'cgpj-insolvency-estate-supervision',
    'cgpj-comision-permanente-sala-lectura',
    'cgpj-permanent-commission-reader-room',
    'fiscalia-dip-2-2026',
    'ona-hotels-salida-concurso-36-2012',
    'ona-hotels-insolvency-exit-36-2012',
    'unitary-criminal-digest-2026-09-03',
    'unitary-criminal-reverse-engineering',
    'insolvency-36-2012-unitary-criminal-forensic-analysis',
    'concurso-36-2012-auditoria-plan-liquidacion-juez-laj',
    'concurso-36-2012-liquidation-plan-judge-laj-audit'
  ];

  const isHome = /\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(path);
  if (!isHome && !relevantFragments.some(fragment => path.includes(fragment))) return;

  const copy = lang === 'en' ? {
    eyebrow: 'PROCEDURAL IDENTITY · CONTROL 22 / DP 1956 · CONTROL 24',
    title: 'The administrator and judicial-supervision complaints are now digitised and connected without consolidation.',
    lead: 'Control 22 is a filing locator later associated with DP 1956/2026. Control 24 is a separate complaint concerning the insolvency judge; its official destination and outcome remain unconfirmed. Control 24 is not itself a formal private-prosecution complaint, although the complainant treats it as the documentary basis of that route.',
    boundary: 'Related does not mean consolidated. Shared evidence does not transfer knowledge, intent, causation, guilt or liability. Filed does not mean admitted or proven.',
    c22: 'Open Control 22',
    dp: 'Open DP 1956',
    c24: 'Open Control 24',
    judge: 'Open judge record',
    register: 'Structured register'
  } : {
    eyebrow: 'IDENTIDAD PROCESAL · CONTROL 22 / DP 1956 · CONTROL 24',
    title: 'Las denuncias relativas al Administrador Concursal y a la supervisión judicial están digitalizadas e interconectadas sin acumulación.',
    lead: 'Control 22 es un localizador de presentación posteriormente asociado a DP 1956/2026. Control 24 es una denuncia separada relativa al juez del concurso; su destino y resultado oficiales siguen sin confirmarse. Control 24 no es por sí mismo una querella formal, aunque el denunciante lo trata como base documental de esa vía.',
    boundary: 'Relacionado no significa acumulado. La prueba compartida no transfiere conocimiento, dolo, causalidad, culpabilidad o responsabilidad. Presentado no significa admitido ni probado.',
    c22: 'Abrir Control 22',
    dp: 'Abrir DP 1956',
    c24: 'Abrir Control 24',
    judge: 'Abrir registro del juez',
    register: 'Registro estructurado'
  };

  const addStyle = () => {
    if (document.getElementById('pd-control-22-24-style')) return;
    const style = document.createElement('style');
    style.id = 'pd-control-22-24-style';
    style.textContent = `
      .pd-c2224{background:linear-gradient(135deg,#17272e,#43303a 66%,#73571d);color:#fff;padding:2.1rem 0;position:relative;z-index:1}
      .pd-c2224.pd-c2224-home{max-width:1180px;margin:1.25rem auto;border-radius:22px;overflow:hidden;box-shadow:0 18px 44px rgba(15,34,42,.22)}
      .pd-c2224 h2{color:#fff;max-width:1050px;margin:.25rem 0 .65rem}.pd-c2224 p{color:#f0f3f3;max-width:1120px;line-height:1.62}
      .pd-c2224-ey{font-size:.73rem;font-weight:850;letter-spacing:.07em;text-transform:uppercase;color:#f2d57b}
      .pd-c2224-boundary{border-left:4px solid #f2d57b;padding-left:.85rem;font-size:.92rem}
      .pd-c2224-links{display:flex;gap:.52rem;flex-wrap:wrap;margin-top:1rem}
      .pd-c2224-links a{display:inline-block;background:#f2d57b;color:#17272e;text-decoration:none;border-radius:999px;padding:.52rem .78rem;font-weight:850}
      @media(max-width:780px){.pd-c2224{padding:1.55rem 0}.pd-c2224.pd-c2224-home{margin:1rem .7rem}}
    `;
    document.head.appendChild(style);
  };

  const render = () => {
    if (document.querySelector('[data-control-22-24-interlink]')) return;
    addStyle();
    const section = document.createElement('section');
    section.className = 'pd-c2224' + (isHome ? ' pd-c2224-home' : '');
    section.setAttribute('data-control-22-24-interlink', '20260904');
    section.innerHTML = `<div class="shell"><p class="pd-c2224-ey">${copy.eyebrow}</p><h2>${copy.title}</h2><p>${copy.lead}</p><p class="pd-c2224-boundary">${copy.boundary}</p><div class="pd-c2224-links"><a href="${c22Route}">${copy.c22}</a><a href="${dp1956Route}">${copy.dp}</a><a href="${c24Route}">${copy.c24}</a><a href="${judgeRoute}">${copy.judge}</a><a href="${registerRoute}">${copy.register}</a></div></div>`;

    const main = document.querySelector('main');
    if (isHome && main) {
      const sections = main.querySelectorAll(':scope > section');
      if (sections.length > 1) main.insertBefore(section, sections[1]);
      else main.appendChild(section);
      return;
    }

    const footer = document.querySelector('footer');
    if (footer && footer.parentNode) footer.parentNode.insertBefore(section, footer);
    else if (main) main.appendChild(section);
    else document.body.appendChild(section);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', render, { once: true });
  } else {
    render();
  }
})();

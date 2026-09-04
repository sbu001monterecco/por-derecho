(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const lang = (document.documentElement.lang || (path.includes('/en/') ? 'en' : 'es'))
    .toLowerCase().startsWith('en') ? 'en' : 'es';

  const hubRoutes = [
    '/es/concurso-36-2012-triangulo-responsabilidad/',
    '/en/concurso-36-2012-accountability-triangle/'
  ];
  if (hubRoutes.some(route => path.includes(route))) return;

  const relevantFragments = [
    'dp-1901-2026', 'dp-1956-2026',
    'control-22-denuncia-administrador-concursal', 'control-22-insolvency-administrator-complaint',
    'control-24-denuncia-juez-concurso-36-2012', 'control-24-insolvency-judge-complaint-36-2012',
    'concurso-36-2012-administrador-concursal', 'insolvency-36-2012-insolvency-administrator',
    'concurso-36-2012-magistrado-juez', 'insolvency-36-2012-mercantile-court-1',
    'concurso-36-2012-separacion-ac-honorarios', 'insolvency-36-2012-administrator-removal-fees',
    'calificacion-rpl-2523', 'insolvency-classification',
    'cgpj-supervision-masa-activa', 'cgpj-insolvency-estate-supervision',
    'cgpj-comision-permanente-sala-lectura', 'cgpj-permanent-commission-reader-room',
    'fiscalia-dip-2-2026', 'public-prosecution',
    'mapa-procedimientos', 'proceedings-map',
    'registro-maestro-procedimientos', 'master-proceedings-register',
    'reconstruccion-unitaria-autoridades-publicas', 'public-authority-unitary-case-reconstruction',
    'ona-hotels-salida-concurso-36-2012', 'ona-hotels-insolvency-exit-36-2012',
    'unitary-criminal-digest-2026-09-03', 'unitary-criminal-reverse-engineering',
    'concurso-36-2012-auditoria-plan-liquidacion-juez-laj',
    'concurso-36-2012-liquidation-plan-judge-laj-audit'
  ];
  const isHome = /\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(path);
  if (!isHome && !relevantFragments.some(fragment => path.includes(fragment))) return;

  const routes = lang === 'en' ? {
    hub: '/por-derecho/en/concurso-36-2012-accountability-triangle/',
    private: '/por-derecho/en/dp-1901-2026/',
    c22: '/por-derecho/en/control-22-insolvency-administrator-complaint/',
    ac: '/por-derecho/en/insolvency-36-2012-insolvency-administrator/',
    dp1956: '/por-derecho/en/dp-1956-2026/',
    removal: '/por-derecho/en/insolvency-36-2012-administrator-removal-fees/',
    c24: '/por-derecho/en/control-24-insolvency-judge-complaint-36-2012/',
    judge: '/por-derecho/en/insolvency-36-2012-mercantile-court-1/',
    cgpj: '/por-derecho/en/cgpj-permanent-commission-reader-room/',
    fiscalia: '/por-derecho/en/fiscalia-dip-2-2026/',
    rpl: '/por-derecho/en/calificacion-rpl-2523-evidence-map/',
    register: '/por-derecho/data/concurso36-accountability-triangle-v1.json'
  } : {
    hub: '/por-derecho/es/concurso-36-2012-triangulo-responsabilidad/',
    private: '/por-derecho/es/dp-1901-2026/',
    c22: '/por-derecho/es/control-22-denuncia-administrador-concursal/',
    ac: '/por-derecho/es/concurso-36-2012-administrador-concursal/',
    dp1956: '/por-derecho/es/dp-1956-2026/',
    removal: '/por-derecho/es/concurso-36-2012-separacion-ac-honorarios/',
    c24: '/por-derecho/es/control-24-denuncia-juez-concurso-36-2012/',
    judge: '/por-derecho/es/concurso-36-2012-magistrado-juez/',
    cgpj: '/por-derecho/es/cgpj-comision-permanente-sala-lectura/',
    fiscalia: '/por-derecho/es/fiscalia-dip-2-2026/',
    rpl: '/por-derecho/es/calificacion-rpl-2523-mapa-prueba/',
    register: '/por-derecho/data/concurso36-accountability-triangle-v1.json'
  };

  const copy = lang === 'en' ? {
    eyebrow: 'INSOLVENCY 36/2012 · THREE DISTINCT ACCOUNTABILITY VERTICES',
    title: 'Private actors, the Insolvency Administrator and the insolvency judge are interconnected without being consolidated.',
    lead: 'Control 21 / DP 1901, Control 22 / DP 1956 and Control 24 arise around the same documentary nucleus. Each track retains its own identity, competence, standard, evidence and outcome.',
    perimeter: 'PROSECUTION SERVICE / OVERSIGHT PERIMETER',
    perimeterNote: 'Claimant hypothesis: neutralisation or ineffectiveness · not established',
    private: 'PRIVATE ACTORS',
    privateRef: 'Control 21 · NEXUS 36 · DP 1901',
    ac: 'INSOLVENCY ADMINISTRATOR',
    acRef: 'Control 22 · DP 1956',
    acSub: 'ICALPA 80 · removal · fees',
    judge: 'INSOLVENCY JUDGE',
    judgeRef: 'Control 24 · 18 + 25 June',
    judgeSub: 'CGPJ 169 · Appeal 286 · DIP 2',
    nucleus: 'COMMON NUCLEUS · INSOLVENCY 36/2012',
    boundary: 'Arrows are typed evidential, supervisory or alleged-effect links. They are not proof of joinder, common knowledge, concert, guilt or shared liability. Control 24 is canonical for continuity but is not a NIG, DP number, reparto decision, confirmed proceeding or formal querella. The Control 22 → DP 1956 certified bridge remains open.',
    open: 'Open full triangle',
    c22: 'Control 22',
    c24: 'Control 24',
    cgpj: 'CGPJ 169 / Appeal 286',
    fiscalia: 'DIP 2/2026',
    removal: 'AC removal / fees',
    rpl: 'RPL 2523',
    register: 'Canonical graph'
  } : {
    eyebrow: 'CONCURSO 36/2012 · TRES VÉRTICES DE RESPONSABILIDAD SEPARADOS',
    title: 'Actores privados, Administrador Concursal y Magistrado-Juez están interconectados sin quedar acumulados.',
    lead: 'Control 21 / DP 1901, Control 22 / DP 1956 y Control 24 nacen alrededor del mismo núcleo documental. Cada vía conserva identidad, competencia, estándar, prueba y resultado propios.',
    perimeter: 'FISCALÍA / PERÍMETRO DE SUPERVISIÓN',
    perimeterNote: 'Hipótesis del denunciante: neutralización o ineficacia · no está probado',
    private: 'ACTORES PRIVADOS',
    privateRef: 'Control 21 · NEXUS 36 · DP 1901',
    ac: 'ADMINISTRADOR CONCURSAL',
    acRef: 'Control 22 · DP 1956',
    acSub: 'ICALPA 80 · separación · honorarios',
    judge: 'MAGISTRADO-JUEZ',
    judgeRef: 'Control 24 · 18 + 25 junio',
    judgeSub: 'CGPJ 169 · Alzada 286 · DIP 2',
    nucleus: 'NÚCLEO COMÚN · CONCURSO 36/2012',
    boundary: 'Las flechas son enlaces probatorios, de supervisión o de efecto alegado. No prueban acumulación, conocimiento común, concierto, culpabilidad ni responsabilidad compartida. Control 24 es canónico para continuidad, pero no es NIG, DP, reparto, causa confirmada ni querella formal. El puente certificado Control 22 → DP 1956 sigue abierto.',
    open: 'Abrir triángulo completo',
    c22: 'Control 22',
    c24: 'Control 24',
    cgpj: 'CGPJ 169 / Alzada 286',
    fiscalia: 'DIP 2/2026',
    removal: 'Separación / honorarios AC',
    rpl: 'RPL 2523',
    register: 'Grafo canónico'
  };

  const addStyle = () => {
    if (document.getElementById('pd-c36-triangle-style')) return;
    const style = document.createElement('style');
    style.id = 'pd-c36-triangle-style';
    style.textContent = `
      .pd-c36tri{background:linear-gradient(135deg,#10252e,#2f3b46 62%,#6b4e1d);color:#fff;padding:2.15rem 0;position:relative;z-index:1}
      .pd-c36tri.pd-c36tri-home{max-width:1180px;margin:1.25rem auto;border-radius:22px;overflow:hidden;box-shadow:0 18px 44px rgba(15,34,42,.24)}
      .pd-c36tri h2{color:#fff;max-width:1080px;margin:.25rem 0 .65rem}.pd-c36tri p{color:#eef3f3;max-width:1120px;line-height:1.62}
      .pd-c36tri-ey{font-size:.73rem;font-weight:900;letter-spacing:.07em;text-transform:uppercase;color:#f2d57b}
      .pd-c36tri-visual{overflow-x:auto;background:rgba(3,19,24,.42);border:1px solid rgba(255,255,255,.18);border-radius:18px;padding:.6rem;margin:1rem 0}
      .pd-c36tri-visual svg{display:block;width:100%;min-width:720px;height:auto}.pd-c36tri-node rect{stroke-width:2.6}.pd-c36tri-node text{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;pointer-events:none}.pd-c36tri-node:hover rect,.pd-c36tri-node:focus rect{stroke:#f2d57b;filter:brightness(1.1)}
      .pd-c36tri-boundary{border-left:4px solid #f2d57b;padding-left:.85rem;font-size:.91rem}
      .pd-c36tri-links{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1rem}.pd-c36tri-links a{display:inline-block;background:#f2d57b;color:#17272e;text-decoration:none;border-radius:999px;padding:.5rem .75rem;font-weight:850}
      @media(max-width:780px){.pd-c36tri{padding:1.55rem 0}.pd-c36tri.pd-c36tri-home{margin:1rem .7rem}}
    `;
    document.head.appendChild(style);
  };

  const render = () => {
    if (document.querySelector('[data-concurso36-accountability-triangle]')) return;
    addStyle();
    const section = document.createElement('section');
    section.className = 'pd-c36tri' + (isHome ? ' pd-c36tri-home' : '');
    section.setAttribute('data-concurso36-accountability-triangle', '20260904b');
    section.innerHTML = `<div class="shell"><p class="pd-c36tri-ey">${copy.eyebrow}</p><h2>${copy.title}</h2><p>${copy.lead}</p><div class="pd-c36tri-visual"><svg viewBox="0 0 960 590" role="img" aria-label="${copy.title}"><ellipse cx="480" cy="277" rx="440" ry="238" fill="none" stroke="#e0bd60" stroke-width="3" stroke-dasharray="12 10"/><text x="480" y="527" text-anchor="middle" fill="#f2d57b" font-size="18" font-weight="850">${copy.perimeter}</text><text x="480" y="553" text-anchor="middle" fill="#eef3f3" font-size="14">${copy.perimeterNote}</text><line x1="480" y1="174" x2="235" y2="356" stroke="#aec0c4" stroke-width="4"/><line x1="245" y1="397" x2="715" y2="397" stroke="#aec0c4" stroke-width="4"/><line x1="725" y1="356" x2="500" y2="174" stroke="#aec0c4" stroke-width="4"/><a class="pd-c36tri-node" href="${routes.private}"><rect x="315" y="48" width="330" height="125" rx="18" fill="#6b2c2c" stroke="#fff"/><text x="480" y="88" text-anchor="middle" fill="#fff" font-size="22" font-weight="900">${copy.private}</text><text x="480" y="124" text-anchor="middle" fill="#f8dfa0" font-size="17" font-weight="800">${copy.privateRef}</text></a><a class="pd-c36tri-node" href="${routes.ac}"><rect x="55" y="342" width="360" height="140" rx="18" fill="#7a581d" stroke="#fff"/><text x="235" y="382" text-anchor="middle" fill="#fff" font-size="21" font-weight="900">${copy.ac}</text><text x="235" y="417" text-anchor="middle" fill="#f8dfa0" font-size="17" font-weight="800">${copy.acRef}</text><text x="235" y="451" text-anchor="middle" fill="#fff" font-size="15">${copy.acSub}</text></a><a class="pd-c36tri-node" href="${routes.judge}"><rect x="545" y="342" width="360" height="140" rx="18" fill="#24546a" stroke="#fff"/><text x="725" y="382" text-anchor="middle" fill="#fff" font-size="21" font-weight="900">${copy.judge}</text><text x="725" y="417" text-anchor="middle" fill="#f8dfa0" font-size="17" font-weight="800">${copy.judgeRef}</text><text x="725" y="451" text-anchor="middle" fill="#fff" font-size="15">${copy.judgeSub}</text></a><a class="pd-c36tri-node" href="${routes.hub}"><rect x="315" y="225" width="330" height="92" rx="46" fill="#0e3039" stroke="#f2d57b"/><text x="480" y="280" text-anchor="middle" fill="#fff" font-size="19" font-weight="900">${copy.nucleus}</text></a></svg></div><p class="pd-c36tri-boundary">${copy.boundary}</p><div class="pd-c36tri-links"><a href="${routes.hub}">${copy.open}</a><a href="${routes.c22}">${copy.c22}</a><a href="${routes.c24}">${copy.c24}</a><a href="${routes.cgpj}">${copy.cgpj}</a><a href="${routes.fiscalia}">${copy.fiscalia}</a><a href="${routes.removal}">${copy.removal}</a><a href="${routes.rpl}">${copy.rpl}</a><a href="${routes.register}">${copy.register}</a></div></div>`;

    const main = document.querySelector('main');
    if (main) {
      const first = main.querySelector(':scope > section');
      if (first && first.nextSibling) main.insertBefore(section, first.nextSibling);
      else main.appendChild(section);
    } else {
      const footer = document.querySelector('footer');
      if (footer && footer.parentNode) footer.parentNode.insertBefore(section, footer);
      else document.body.appendChild(section);
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', render, { once: true });
  } else {
    render();
  }
})();

(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const lang = (document.documentElement.lang || (path.includes('/en/') ? 'en' : 'es')).toLowerCase().startsWith('en') ? 'en' : 'es';
  const relevant = [
    'dp-1901-2026','control-22-','dp-1956-2026','control-24-','gc-hc-010',
    'concurso-36-2012-administrador-concursal','insolvency-36-2012-insolvency-administrator',
    'concurso-36-2012-magistrado-juez','insolvency-36-2012-mercantile-court-1',
    'concurso-36-2012-separacion-ac-honorarios','insolvency-36-2012-administrator-removal-fees',
    'cgpj-supervision-masa-activa','cgpj-insolvency-estate-supervision','fiscalia-dip-2-2026',
    'registros-institucionales','institutional-records','concurso-36-2012-ap-seccion-4','insolvency-36-2012-ap-section-4',
    'unitary-criminal','reconstruccion-unitaria'
  ];
  const isHome = /\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(path);
  if (!isHome && !relevant.some(fragment => path.includes(fragment))) return;

  const routes = lang === 'en' ? {
    private: '/por-derecho/en/dp-1901-2026/', ac: '/por-derecho/en/control-22-insolvency-administrator-complaint/',
    dp1956: '/por-derecho/en/dp-1956-2026/', judge: '/por-derecho/en/control-24-insolvency-judge-complaint-36-2012/',
    gc: '/por-derecho/en/proceedings/gc-hc-010/', cgpj: '/por-derecho/en/cgpj-insolvency-estate-supervision/',
    fiscal: '/por-derecho/en/fiscalia-dip-2-2026/', icalpa: '/por-derecho/en/institutional-records-bar-bodies-2026/',
    removal: '/por-derecho/en/insolvency-36-2012-administrator-removal-fees/', rpl: '/por-derecho/en/insolvency-36-2012-ap-section-4/',
    register: '/por-derecho/data/concurso-36-2012-triangle-register-v1.json'
  } : {
    private: '/por-derecho/es/dp-1901-2026/', ac: '/por-derecho/es/control-22-denuncia-administrador-concursal/',
    dp1956: '/por-derecho/es/dp-1956-2026/', judge: '/por-derecho/es/control-24-denuncia-juez-concurso-36-2012/',
    gc: '/por-derecho/es/procedimientos/gc-hc-010/', cgpj: '/por-derecho/es/cgpj-supervision-masa-activa/',
    fiscal: '/por-derecho/es/fiscalia-dip-2-2026/', icalpa: '/por-derecho/es/registros-institucionales-colegios-abogacia-2026/',
    removal: '/por-derecho/es/concurso-36-2012-separacion-ac-honorarios/', rpl: '/por-derecho/es/concurso-36-2012-ap-seccion-4/',
    register: '/por-derecho/data/concurso-36-2012-triangle-register-v1.json'
  };

  const copy = lang === 'en' ? {
    eyebrow: 'CONCURSO 36/2012 · CANONICAL INTERCONNECTION MAP', title: 'Three accountability vertices, one factual nucleus — separate proceedings.',
    private: 'PRIVATE ACTORS', privateSub: 'Control 21 · NEXUS 36 · DP 1901/2026', ac: 'INSOLVENCY ADMINISTRATOR', acSub: 'Control 22 · DP 1956 · ICALPA 80 · removal / fees',
    judge: 'CONCURSO JUDGE', judgeSub: 'Control 24 · GC-HC-010 · 25 Jun supplement · CGPJ 169/286',
    fiscal: 'PROSECUTION / OVERSIGHT PERIMETER', fiscalSub: 'DIP 2/2026 · separate routes · neutralisation alleged by the reporting party',
    boundary: 'Interlinked does not mean consolidated. Shared evidence does not transfer knowledge, intent, causation, guilt or liability. Control 24 is Decanato daily no. 24; allocation/status remain unknown. Control 22 is not DP 1956 without the primary allocation bridge.',
    rpl: 'RPL 2523/2025 · classification appeal', register: 'Open canonical graph'
  } : {
    eyebrow: 'CONCURSO 36/2012 · MAPA CANÓNICO DE INTERCONEXIÓN', title: 'Tres vértices de responsabilidad, un núcleo fáctico — procedimientos separados.',
    private: 'ACTORES PRIVADOS', privateSub: 'Control 21 · NEXUS 36 · DP 1901/2026', ac: 'ADMINISTRADOR CONCURSAL', acSub: 'Control 22 · DP 1956 · ICALPA 80 · separación / honorarios',
    judge: 'JUEZ DEL CONCURSO', judgeSub: 'Control 24 · GC-HC-010 · ampliación 25 jun · CGPJ 169/286',
    fiscal: 'FISCALÍA / PERÍMETRO DE SUPERVISIÓN', fiscalSub: 'DIP 2/2026 · vías separadas · neutralización alegada por el denunciante',
    boundary: 'Interconectado no significa acumulado. La prueba compartida no transfiere conocimiento, dolo, causalidad, culpabilidad o responsabilidad. Control 24 es el registro diario n.º 24 del Decanato; reparto/estado siguen desconocidos. Control 22 no es DP 1956 sin el puente primario de reparto.',
    rpl: 'RPL 2523/2025 · apelación de calificación', register: 'Abrir grafo canónico'
  };

  const addStyle = () => {
    if (document.getElementById('pd-c36tri-style')) return;
    const style = document.createElement('style'); style.id = 'pd-c36tri-style'; style.textContent = `
      .pd-c36tri{padding:clamp(2rem,5vw,4rem) 0;background:#101f26;color:#fff}.pd-c36tri.pd-c36tri-home{margin:1.25rem auto;max-width:1180px;border-radius:24px;overflow:hidden;box-shadow:0 22px 50px rgba(0,0,0,.22)}
      .pd-c36tri h2{color:#fff;max-width:920px;margin:.25rem 0 1rem}.pd-c36tri-ey{color:#f0cf75;font-weight:900;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase}.pd-c36tri-boundary{border-left:4px solid #f0cf75;padding:.8rem 1rem;background:rgba(255,255,255,.06);line-height:1.55}
      .pd-c36tri svg{width:100%;height:auto;display:block;margin:1.4rem 0;background:#f7f4ec;border-radius:20px}.pd-c36tri svg a{text-decoration:none}.pd-c36tri svg .node{fill:#fff;stroke:#18343e;stroke-width:2}.pd-c36tri svg .nodeTitle{font:800 20px system-ui,sans-serif;fill:#12262e}.pd-c36tri svg .nodeSub{font:600 12px system-ui,sans-serif;fill:#4c5c62}.pd-c36tri svg .line{stroke:#8a6b20;stroke-width:3}.pd-c36tri svg .perim{fill:none;stroke:#9e3d35;stroke-width:3;stroke-dasharray:10 8}.pd-c36tri svg .perimText{font:800 16px system-ui,sans-serif;fill:#7c302a}.pd-c36tri svg .perimSub{font:600 11px system-ui,sans-serif;fill:#604844}.pd-c36tri svg .core{font:900 17px system-ui,sans-serif;fill:#18343e}
      .pd-c36tri-links{display:flex;gap:.55rem;flex-wrap:wrap}.pd-c36tri-links a{background:#f0cf75;color:#12262e!important;border-radius:999px;padding:.55rem .8rem;text-decoration:none;font-weight:850}
      @media(max-width:760px){.pd-c36tri{padding:1.5rem 0}.pd-c36tri.pd-c36tri-home{margin:1rem .7rem}.pd-c36tri svg .nodeTitle{font-size:15px}.pd-c36tri svg .nodeSub{font-size:9px}.pd-c36tri svg .perimText{font-size:12px}.pd-c36tri svg .perimSub{font-size:8px}}
    `; document.head.appendChild(style);
  };

  const render = () => {
    if (document.querySelector('[data-concurso36-triangle]')) return;
    document.querySelectorAll('[data-control-22-24-interlink]').forEach(el => el.remove());
    addStyle();
    const section = document.createElement('section');
    section.className = 'pd-c36tri' + (isHome ? ' pd-c36tri-home' : '');
    section.setAttribute('data-concurso36-triangle','20260904');
    section.innerHTML = `<div class="shell"><p class="pd-c36tri-ey">${copy.eyebrow}</p><h2>${copy.title}</h2>
      <svg viewBox="0 0 1100 690" role="img" aria-label="${copy.title}">
        <path class="perim" d="M70 85 Q550 10 1030 85 L1030 615 Q550 680 70 615 Z"/>
        <text class="perimText" x="550" y="58" text-anchor="middle">${copy.fiscal}</text><text class="perimSub" x="550" y="77" text-anchor="middle">${copy.fiscalSub}</text>
        <line class="line" x1="550" y1="180" x2="300" y2="455"/><line class="line" x1="550" y1="180" x2="800" y2="455"/><line class="line" x1="300" y1="455" x2="800" y2="455"/>
        <text class="core" x="550" y="345" text-anchor="middle">CONCURSO ORDINARIO 36/2012</text>
        <a href="${routes.private}"><rect class="node" x="350" y="105" width="400" height="115" rx="18"/><text class="nodeTitle" x="550" y="150" text-anchor="middle">${copy.private}</text><text class="nodeSub" x="550" y="178" text-anchor="middle">${copy.privateSub}</text></a>
        <a href="${routes.ac}"><rect class="node" x="80" y="410" width="440" height="125" rx="18"/><text class="nodeTitle" x="300" y="455" text-anchor="middle">${copy.ac}</text><text class="nodeSub" x="300" y="485" text-anchor="middle">${copy.acSub}</text></a>
        <a href="${routes.judge}"><rect class="node" x="580" y="410" width="440" height="125" rx="18"/><text class="nodeTitle" x="800" y="455" text-anchor="middle">${copy.judge}</text><text class="nodeSub" x="800" y="485" text-anchor="middle">${copy.judgeSub}</text></a>
        <a href="${routes.fiscal}"><rect class="node" x="355" y="570" width="390" height="70" rx="16"/><text class="nodeTitle" x="550" y="605" text-anchor="middle">DIP 2/2026 · CGPJ · ICALPA</text><text class="nodeSub" x="550" y="625" text-anchor="middle">oversight / prosecutorial perimeter · separate routes</text></a>
      </svg>
      <p class="pd-c36tri-boundary">${copy.boundary}</p><div class="pd-c36tri-links"><a href="${routes.gc}">GC-HC-010 / Control 24</a><a href="${routes.dp1956}">DP 1956/2026</a><a href="${routes.icalpa}">ICALPA 80/2026</a><a href="${routes.removal}">${lang==='en'?'AC removal / fees':'Separación / honorarios AC'}</a><a href="${routes.cgpj}">CGPJ 169/286</a><a href="${routes.rpl}">${copy.rpl}</a><a href="${routes.register}">${copy.register}</a></div></div>`;
    const main = document.querySelector('main'); const footer = document.querySelector('footer');
    if (isHome && main) { const sections = main.querySelectorAll(':scope > section'); if (sections.length > 1) main.insertBefore(section, sections[1]); else main.appendChild(section); }
    else if (footer && footer.parentNode) footer.parentNode.insertBefore(section, footer); else if (main) main.appendChild(section); else document.body.appendChild(section);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render, {once:true}); else render();
})();

(() => {
  const path = window.location.pathname.replace(/index\.html$/, '');
  const targets = [
    '/es/ric-private-equity-sun-park/',
    '/en/ric-private-equity-sun-park/',
    '/es/orion-ricpe-continuidad/',
    '/en/orion-ricpe-platform-continuity/',
    '/es/portfolio-orion-trazabilidad/',
    '/en/portfolio-orion-traceability/',
    '/es/ricpe-responsabilidad-documental/',
    '/en/ricpe-documentary-accountability/',
    '/es/san-telmo-ricpe-sun-park/',
    '/en/san-telmo-ricpe-sun-park/',
    '/es/pwc-canarias-carlos-saavedra-sun-park/',
    '/en/pwc-canarias-carlos-saavedra-sun-park/',
    '/es/grant-thornton/2024-04/',
    '/en/grant-thornton/2024-04/',
    '/es/rsm/nnr4-1025c2f66/',
    '/en/rsm/nnr4-1025c2f66/',
    '/es/actualizaciones/',
    '/en/updates/'
  ];

  const matched = targets.some((route) => path.endsWith(route));
  if (!matched) return;

  const isEnglish = /\/en\//.test(path);
  const statusHref = isEnglish
    ? '/por-derecho/en/cnmv-ricpe-verification/'
    : '/por-derecho/es/cnmv-ricpe-verificacion/';

  const copy = isEnglish
    ? {
        label: 'CNMV · verified procedural update',
        title: 'Email sent · REGAGE26e00074329732 registered · receipt followed up',
        body: 'The 20 August 2026 cross-border communication is now traceable through both email and the AGE registry. A substantive CNMV acknowledgement, corpus incorporation, functional file linkage, preservation confirmation and process owner remain pending. Gil Marer does not currently act for LPB.',
        link: 'Open verified status and 360 action control →'
      }
    : {
        label: 'CNMV · actualización procesal verificada',
        title: 'Correo enviado · REGAGE26e00074329732 registrado · justificante remitido',
        body: 'La comunicación transfronteriza de 20 de agosto de 2026 ya es trazable por correo y por registro AGE. Permanecen pendientes el acuse sustantivo de la CNMV, la incorporación al corpus, la vinculación funcional, la confirmación de preservación y la unidad responsable. Gil Marer no comparece actualmente por LPB.',
        link: 'Abrir estado verificado y control 360 →'
      };

  const style = document.createElement('style');
  style.textContent = `
    .cnmv-regage-cross-site{background:#edf3ee;border-block:1px solid #9bb3a2;padding:1.05rem 0;color:#172b34}
    .cnmv-regage-cross-site__inner{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:1.25rem;align-items:center}
    .cnmv-regage-cross-site__label{margin:0 0 .28rem;font-size:.68rem;letter-spacing:.09em;text-transform:uppercase;font-weight:900;color:#496653}
    .cnmv-regage-cross-site h2{margin:0 0 .35rem;font-size:clamp(1.08rem,2vw,1.42rem);line-height:1.18}
    .cnmv-regage-cross-site p{margin:0;max-width:82ch;font-size:.88rem;line-height:1.55}
    .cnmv-regage-cross-site a{display:inline-flex;align-items:center;justify-content:center;border-radius:999px;background:#13252d;color:#fff;text-decoration:none;font-weight:850;padding:.7rem .9rem;white-space:nowrap}
    @media(max-width:760px){.cnmv-regage-cross-site__inner{grid-template-columns:1fr}.cnmv-regage-cross-site a{justify-self:start;white-space:normal}}
  `;
  document.head.appendChild(style);

  const inject = () => {
    if (document.querySelector('[data-cnmv-regage-status="20260820"]')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const firstSection = main.querySelector(':scope > section');
    if (!firstSection) return;

    const section = document.createElement('section');
    section.className = 'cnmv-regage-cross-site';
    section.dataset.cnmvRegageStatus = '20260820';
    section.setAttribute('aria-label', copy.label);
    section.innerHTML = `
      <div class="shell cnmv-regage-cross-site__inner">
        <div>
          <p class="cnmv-regage-cross-site__label">${copy.label}</p>
          <h2>${copy.title}</h2>
          <p>${copy.body}</p>
        </div>
        <a href="${statusHref}">${copy.link}</a>
      </div>`;
    firstSection.insertAdjacentElement('afterend', section);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject, { once: true });
  } else {
    inject();
  }
})();

(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const localPath = path.startsWith('/por-derecho/') ? path : `/por-derecho${path.startsWith('/') ? '' : '/'}${path}`;

  // The dedicated 3304/3319 dossier contains a full SHA-256 and several
  // long procedural identifiers. Keep those source-integrity strings visible
  // without allowing them to widen a mobile viewport.
  const dossierRoutes = new Set([
    '/por-derecho/es/concurso-36-2012-separacion-administrador-concursal-rpl-3304-2025/',
    '/por-derecho/en/insolvency-36-2012-administrator-removal-rpl-3304-2025/'
  ]);
  if (dossierRoutes.has(localPath) && !document.querySelector('[data-borja-separation-responsive-fix="20260902"]')) {
    const style = document.createElement('style');
    style.setAttribute('data-borja-separation-responsive-fix', '20260902');
    style.textContent = `
      .mono{overflow-wrap:anywhere;word-break:break-word;max-width:100%}
      .panel,.ground,.metric,.relief,.link-card,.lane,.master{min-width:0}
      .panel a,.ground a,.link-card a{overflow-wrap:anywhere}
    `;
    document.head.appendChild(style);
  }

  // Spanish social-publication companion: preserve the controlled dossier as
  // the source of truth while giving the user a reusable incremental LinkedIn queue.
  if (localPath === '/por-derecho/es/concurso-36-2012-separacion-administrador-concursal-rpl-3304-2025/'
      && !document.querySelector('[data-borja-separation-linkedin-series="20260902"]')) {
    const series = document.createElement('section');
    series.setAttribute('data-borja-separation-linkedin-series', '20260902');
    series.className = 'section';
    series.innerHTML = `<div class="shell"><div style="border-left:7px solid #315c7b;background:#fff;padding:1.15rem 1.3rem;box-shadow:0 10px 26px rgba(19,37,45,.08)"><p class="eyebrow">SERIE LINKEDIN · PUBLICACIÓN INCREMENTAL</p><h2 style="margin-top:.25rem">Ocho publicaciones listas, cada una enlazada de nuevo al expediente documental.</h2><p>La serie empieza con la notificación recibida el 2 de septiembre de 2026 y avanza por la demanda de 58 páginas, los límites de primera instancia, la acumulación 3319→3304, los carriles penal/disciplinario y las conexiones diferenciadas con Grant Thornton España, RSM Spain y el perímetro Acosta Matos.</p><p><strong>Las etiquetas institucionales no equivalen a una imputación colectiva:</strong> se utilizan por trazabilidad, contexto y derecho de respuesta.</p><p><a class="button" href="/por-derecho/es/concurso-36-2012-separacion-administrador-concursal-rpl-3304-2025/linkedin-serie/">Abrir la serie LinkedIn lista para copiar →</a></p></div></div>`;
    const main = document.querySelector('main');
    if (main) {
      const hero = main.querySelector('.hero, .dossier-hero, section');
      if (hero && hero.parentElement === main) hero.insertAdjacentElement('afterend', series);
      else main.insertAdjacentElement('afterbegin', series);
    }
  }

  const routes = new Set([
    '/por-derecho/es/concurso-36-2012-separacion-ac-honorarios/',
    '/por-derecho/es/concurso-36-2012-administrador-concursal/',
    '/por-derecho/es/concurso-36-2012-ap-seccion-4/',
    '/por-derecho/en/insolvency-36-2012-administrator-removal-fees/',
    '/por-derecho/en/insolvency-36-2012-insolvency-administrator/',
    '/por-derecho/en/insolvency-36-2012-ap-section-4/'
  ]);
  if (!routes.has(localPath)) return;
  if (document.querySelector('[data-borja-separation-rpl3304-inbound="20260902"]')) return;

  const isEs = localPath.includes('/es/');
  const href = isEs
    ? '/por-derecho/es/concurso-36-2012-separacion-administrador-concursal-rpl-3304-2025/'
    : '/por-derecho/en/insolvency-36-2012-administrator-removal-rpl-3304-2025/';
  const section = document.createElement('section');
  section.setAttribute('data-borja-separation-rpl3304-inbound', '20260902');
  section.className = 'section';
  section.innerHTML = isEs
    ? `<div class="shell"><div style="border-left:7px solid #bd8730;background:#fff;padding:1.15rem 1.3rem;box-shadow:0 10px 26px rgba(19,37,45,.08)"><p class="eyebrow">ESTADO PROCESAL CONSOLIDADO · RPL 3304/2025</p><h2 style="margin-top:.25rem">Aweswell recurrió; LPB recurrió independientemente; ambos recursos están acumulados.</h2><p><strong>RPL 3319/2025 no terminó por una derrota de Aweswell sobre el fondo.</strong> El rollo separado quedó absorbido procesalmente por RPL 3304/2025, que es el vehículo apelativo consolidado vivo según el estado documental controlado.</p><p><a class="button" href="${href}">Abrir el expediente dedicado de convergencia 3304/3319 →</a></p></div></div>`
    : `<div class="shell"><div style="border-left:7px solid #bd8730;background:#fff;padding:1.15rem 1.3rem;box-shadow:0 10px 26px rgba(19,37,45,.08)"><p class="eyebrow">CONSOLIDATED PROCEDURAL STATE · RPL 3304/2025</p><h2 style="margin-top:.25rem">Aweswell appealed; LPB independently appealed; both appeals are accumulated.</h2><p><strong>RPL 3319/2025 did not end because Aweswell lost on the merits.</strong> The separate roll was procedurally absorbed into RPL 3304/2025, the live consolidated appellate vehicle according to the controlled documentary state.</p><p><a class="button" href="${href}">Open the dedicated 3304/3319 convergence dossier →</a></p></div></div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector('.hero, .dossier-hero, section');
  if (hero && hero.parentElement === main) hero.insertAdjacentElement('afterend', section);
  else main.insertAdjacentElement('afterbegin', section);
})();
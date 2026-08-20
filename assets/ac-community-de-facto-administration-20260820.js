(() => {
  'use strict';

  const run = () => {
    const pathname = window.location.pathname.replace(/\/+$/, '/');
    const isEs = pathname.includes('/por-derecho/es/');
    const isEn = pathname.includes('/por-derecho/en/');
    if (!isEs && !isEn) return;

    const base = '/por-derecho';
    const canonical = isEs
      ? `${base}/es/administracion-de-hecho-comunidad-ac/`
      : `${base}/en/de-facto-administration-community-ac/`;
    const isCanonical = pathname === canonical;
    const isHome = pathname === `${base}/${isEs ? 'es' : 'en'}/`;
    const isUpdates = /\/(actualizaciones|updates)\//.test(pathname);
    const isControl = /\/(sala-control-caso|case-control-room|ingenieria-forense-criminal-sun-park|sun-park-criminal-engineering-investigation)\//.test(pathname);

    const copy = isEs ? {
      kicker: 'CONTROL DE HECHO · DEUDA · ACCESO · TEXTOS DEFINITIVOS',
      title: 'Nueva reconstrucción: funciones privadas de gestión y dependencia de la AC',
      body: 'La evidencia documenta control privado de deuda, voto, seguridad, acceso y mantenimiento, junto con peticiones, autorizaciones o uso por la Administración Concursal. La coordinación está probada en episodios concretos; la colusión criminal y el estatuto pleno de administrador de hecho no lo están.',
      action: 'Abrir reconstrucción forense →',
      crossTitle: 'Administración material y Textos Definitivos',
      crossBody: 'Esta página debe leerse junto con la matriz que separa gestión privada documentada, autorización de la AC, deuda comunitaria móvil, cambios formales de los Textos Definitivos y los elementos penales todavía no probados.',
      incident: 'No se ha localizado un incidente posterior a la liquidación que amplíe el total privilegiado o convierta las cifras posteriores de Comunidad/intereses en crédito definitivo; el índice certificado completo sigue pendiente.',
      label: 'Investigación activa · no culpabilidad'
    } : {
      kicker: 'DE FACTO CONTROL · DEBT · ACCESS · DEFINITIVE TEXTS',
      title: 'New reconstruction: private management functions and Administrator reliance',
      body: 'The evidence documents private control of debt, voting, security, access and maintenance, together with requests, authorisations or use by the Insolvency Administration. Coordination is proved in specific episodes; criminal collusion and full de facto-administrator status are not.',
      action: 'Open forensic reconstruction →',
      crossTitle: 'Material administration and definitive texts',
      crossBody: 'Read this page with the matrix separating documented private management, Administrator authorisation, mobile Community debt, formal definitive-text changes and the criminal elements that remain unproved.',
      incident: 'No post-liquidation incident has been located that enlarges the privileged total or turns later Community/interest figures into definitive credit; the complete certified index remains outstanding.',
      label: 'Active investigation · no guilt finding'
    };

    const ensureStyles = () => {
      if (document.getElementById('ac-community-de-facto-styles')) return;
      const style = document.createElement('style');
      style.id = 'ac-community-de-facto-styles';
      style.textContent = `
        .ac-dfa-panel{max-width:1120px;margin:0 auto;border-left:5px solid #8c2f2c;background:#fff7f5;border-radius:16px;padding:1.1rem 1.25rem}
        .ac-dfa-panel h2{margin:.15rem 0 .55rem}.ac-dfa-panel p:last-child{margin-bottom:0}
        .ac-dfa-kicker{margin:0 0 .4rem;font-size:.76rem;letter-spacing:.08em;text-transform:uppercase;font-weight:850;color:#8c2f2c}
        .ac-dfa-label{display:inline-block;border:1px solid #8c2f2c;border-radius:999px;padding:.25rem .65rem;font-size:.78rem;font-weight:850;margin:.4rem 0}
        .ac-dfa-cross{max-width:1120px;margin:0 auto;border-left:5px solid #536d79;background:#f4f8fa;border-radius:14px;padding:1rem 1.2rem}
        .ac-dfa-cross h2{margin:.1rem 0 .45rem}.ac-dfa-cross p:last-child{margin-bottom:0}
        .ac-dfa-update{max-width:1120px;margin:0 auto;background:#13252d;color:#fff;border-radius:16px;padding:1.1rem 1.25rem}.ac-dfa-update h2{margin:.1rem 0 .45rem;color:#fff}.ac-dfa-update a{color:#fff;font-weight:850}
      `;
      document.head.appendChild(style);
    };

    const makeSection = (className, html) => {
      const section = document.createElement('section');
      section.className = `section ${className}`;
      section.dataset.acCommunityShadowControl = '20260820';
      section.innerHTML = `<div class="shell">${html}</div>`;
      return section;
    };

    const insertAfterHero = section => {
      const main = document.querySelector('main');
      if (!main) return;
      const hero = main.querySelector(':scope > .hero, :scope > .dossier-hero, :scope > .mhero, :scope > section.hero, :scope > section.dossier-hero');
      if (hero) hero.insertAdjacentElement('afterend', section);
      else if (main.firstElementChild) main.firstElementChild.insertAdjacentElement('afterend', section);
      else main.appendChild(section);
    };

    const routeRelevant = () => {
      if (isCanonical || isHome || isUpdates || isControl) return false;
      return /(comunidad-instrumentalizacion|community-instrumentalisation|concurso-36-2012-administrador-concursal|insolvency-36-2012-insolvency-administrator|administrador-concursal-punto-quiebre|insolvency-administrator-loyalty-breakpoint|administrador-concursal-puerta-credito-titulo|insolvency-administrator-credit-to-title-gatekeeper|textos-definitivos-lpb|lpb-definitive-texts|adjudicacion-2022|2022-adjudication|toma-control-sun-park|sun-park-takeover|acosta-matos-perimetro|acosta-matos-perimeter|calificacion-concurso|insolvency-classification|concurso-36-2012-laj|insolvency-36-2012-laj|mercantile-court-1|magistrado-juez)/i.test(pathname);
    };

    const insertUpdate = () => {
      if (!(isHome || isUpdates || isControl) || document.querySelector('[data-ac-dfa-update]')) return;
      ensureStyles();
      const section = makeSection('ac-dfa-update-section', `
        <aside class="ac-dfa-update" data-ac-dfa-update="20260820">
          <p class="ac-dfa-kicker" style="color:#f2c7c1">${copy.kicker}</p>
          <h2>${copy.title}</h2>
          <p>${copy.body}</p>
          <p><a href="${canonical}">${copy.action}</a></p>
        </aside>`);
      insertAfterHero(section);
    };

    const insertCross = () => {
      if (!routeRelevant() || document.querySelector('[data-ac-dfa-crosslink]')) return;
      ensureStyles();
      const section = makeSection('ac-dfa-cross-section', `
        <aside class="ac-dfa-cross" data-ac-dfa-crosslink="20260820" role="note">
          <p class="ac-dfa-kicker">${copy.kicker}</p>
          <h2>${copy.crossTitle}</h2>
          <p>${copy.crossBody}</p>
          <p><strong>${copy.incident}</strong></p>
          <p><a href="${canonical}">${copy.action}</a></p>
        </aside>`);
      insertAfterHero(section);
    };

    const insertCanonicalContext = () => {
      if (!isCanonical || document.querySelector('[data-ac-dfa-canonical-status]')) return;
      ensureStyles();
      const section = makeSection('ac-dfa-canonical-section', `
        <aside class="ac-dfa-panel" data-ac-dfa-canonical-status="20260820" role="note">
          <p class="ac-dfa-kicker">${copy.kicker}</p>
          <span class="ac-dfa-label">${copy.label}</span>
          <p>${copy.incident}</p>
        </aside>`);
      insertAfterHero(section);
    };

    insertCanonicalContext();
    insertUpdate();
    insertCross();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
  window.setTimeout(run, 1800);
})();

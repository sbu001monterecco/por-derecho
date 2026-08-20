(() => {
  'use strict';
  const run = () => {
    const pathname = window.location.pathname.replace(/\/+$/, '/');
    const isEs = pathname.includes('/por-derecho/es/');
    const isEn = pathname.includes('/por-derecho/en/');
    if (!isEs && !isEn) return;
    const base = '/por-derecho';
    const canonical = isEs
      ? `${base}/es/reforma-derrama-suministros-sun-park/`
      : `${base}/en/sun-park-refurbishment-levy-utilities/`;
    const isCanonical = pathname === canonical;
    const isHome = pathname === `${base}/${isEs ? 'es' : 'en'}/`;
    const isUpdates = /\/(actualizaciones|updates)\//.test(pathname);
    const relevant = /(toma-control-sun-park|sun-park-takeover|ingenieria-inversa-360|reverse-engineering-360|ingenieria-forense-criminal|criminal-engineering|comunidad-instrumentalizacion|community-instrumentalisation|administracion-de-hecho-comunidad-ac|de-facto-administration-community-ac|concurso-36-2012-administrador-concursal|insolvency-36-2012-administrator|adjudicacion-2022|2022-adjudication|ric-private-equity|multiple-financial-lives|multiples-vidas-financieras|yaiza|cabildo|public-authority|reconstruccion-unitaria)/i.test(pathname);
    const copy = isEs ? {
      kicker: '7 JUNIO 2018 · TOMA MATERIAL → OBRAS → FORMALIZACIÓN 2022',
      title: 'No separe la reforma de la toma de control.',
      body: 'La unidad de análisis es una sola: hotel vivo y salida ONA/Lagune/financiación → preparación → toma material mediante fuerza sobre los accesos → exclusión e interrupción → deterioro, obras y reconfiguración → proyecto e inversores antes del título → formalización y apertura. La prueba finca por finca define derechos; no fragmenta la causalidad.',
      action: 'Abrir reconstrucción unitaria →',
      label: 'Hipótesis criminal unitaria · prueba actor por actor',
      boundary: 'No se presume que las obras fueran neutrales o separables. Tampoco se declara que toda obra fuera delictiva: la independencia lícita o la función criminal deben probarse en cada nodo.'
    } : {
      kicker: '7 JUNE 2018 · MATERIAL TAKEOVER → WORKS → 2022 FORMALISATION',
      title: 'Do not separate the refurbishment from the takeover.',
      body: 'There is one analytical unit: living hotel and ONA/Lagune/funded exit → preparation → force-based access takeover → exclusion and interruption → deterioration, works and reconfiguration → project and investors before title → formalisation and opening. Property-by-property proof defines rights; it does not fragment causation.',
      action: 'Open unitary reconstruction →',
      label: 'Unitary criminal hypothesis · actor-specific proof',
      boundary: 'The works are not presumed neutral or severable. Nor is every work declared criminal: lawful independence or criminal function must be proved at each node.'
    };
    const styles = () => {
      if (document.getElementById('refurbishment-unitary-styles')) return;
      const style = document.createElement('style');
      style.id = 'refurbishment-unitary-styles';
      style.textContent = `.ref-unitary{max-width:1120px;margin:0 auto;border-left:6px solid #8c2f2c;background:#fff4f1;border-radius:15px;padding:1.05rem 1.2rem}.ref-unitary h2{margin:.15rem 0 .5rem}.ref-unitary-kicker{margin:0 0 .35rem;font-size:.75rem;font-weight:850;letter-spacing:.07em;text-transform:uppercase;color:#8c2f2c}.ref-unitary-label{display:inline-block;border:1px solid currentColor;border-radius:999px;padding:.23rem .62rem;font-size:.75rem;font-weight:850}.ref-unitary-dark{background:#13252d;color:#fff;border-left:0}.ref-unitary-dark h2,.ref-unitary-dark a{color:#fff}.ref-unitary-boundary{font-size:.9rem;opacity:.9}`;
      document.head.appendChild(style);
    };
    const section = html => {
      const el = document.createElement('section');
      el.className = 'section';
      el.innerHTML = `<div class="shell">${html}</div>`;
      return el;
    };
    const insert = el => {
      const main = document.querySelector('main'); if (!main) return;
      const hero = main.querySelector(':scope > .hero, :scope > .dossier-hero, :scope > section.hero, :scope > section.dossier-hero');
      if (hero) hero.insertAdjacentElement('afterend', el);
      else if (main.firstElementChild) main.firstElementChild.insertAdjacentElement('afterend', el);
      else main.appendChild(el);
    };
    if (isCanonical && !document.querySelector('[data-refurbishment-unitary-canonical]')) {
      styles(); insert(section(`<aside class="ref-unitary" data-refurbishment-unitary-canonical="20260820b"><p class="ref-unitary-kicker">${copy.kicker}</p><span class="ref-unitary-label">${copy.label}</span><p>${copy.boundary}</p></aside>`));
    }
    if ((isHome || isUpdates || relevant) && !isCanonical && !document.querySelector('[data-refurbishment-unitary-update]')) {
      styles(); insert(section(`<aside class="ref-unitary ${isHome || isUpdates ? 'ref-unitary-dark' : ''}" data-refurbishment-unitary-update="20260820b" data-refurbishment-unitary-crosslink="20260820b"><p class="ref-unitary-kicker">${copy.kicker}</p><h2>${copy.title}</h2><p>${copy.body}</p><p class="ref-unitary-boundary">${copy.boundary}</p><p><a href="${canonical}">${copy.action}</a></p></aside>`));
    }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, {once:true}); else run();
  window.setTimeout(run, 1800);
})();

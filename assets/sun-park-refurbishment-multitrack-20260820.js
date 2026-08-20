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
    const isControl = /\/(ingenieria-inversa-360-cadena-sun-park|reverse-engineering-360-sun-park-chain|ingenieria-forense-criminal-sun-park|sun-park-criminal-engineering-investigation|reconstruccion-unitaria-autoridades-publicas|public-authority-unitary-case-reconstruction)\//.test(pathname);
    const copy = isEs ? {
      kicker: 'REFORMA · DERRAMA · TÍTULO · CUMPLIMIENTO 2022',
      title: 'La adjudicación de 2022 no convierte el pasado en una hoja en blanco',
      body: 'Nueva reconstrucción en cinco carriles: relato de inicio limpio a contrastar, registro previo al título, procesos 2022 de regularización/financiación/apertura, verificación actor por actor y resultado físico/económico.',
      action: 'Abrir reconstrucción multitrack →',
      cross: 'Lea este expediente junto con la reconstrucción de reforma y derrama: separa lo que se afirmó desde 2022 de lo que ya había ocurrido o estaba en disputa antes del título.',
      label: 'Investigación activa · no culpabilidad'
    } : {
      kicker: 'REFURBISHMENT · LEVY · TITLE · 2022 COMPLIANCE',
      title: 'The 2022 adjudication did not turn the past into a blank page',
      body: 'New five-track reconstruction: clean-start account to test, pre-title record, parallel 2022 regularisation/finance/opening processes, actor-specific verification and the physical/economic result.',
      action: 'Open multitrack reconstruction →',
      cross: 'Read this dossier with the refurbishment and levy reconstruction: it separates what was asserted from 2022 from what had already happened or was disputed before title.',
      label: 'Active investigation · no guilt finding'
    };
    const relevant = /(comunidad-instrumentalizacion|community-instrumentalisation|administracion-de-hecho-comunidad-ac|de-facto-administration-community-ac|toma-control-sun-park|sun-park-takeover|acosta-matos-perimetro|acosta-matos-perimeter|mismo-hotel-multiples-vidas-financieras|same-hotel-multiple-financial-lives|adjudicacion-2022|2022-adjudication|yaiza-trazabilidad|yaiza-institutional|cabildo-lanzarote|ric-private-equity|concurso-36-2012-administrador-concursal|insolvency-36-2012-administrator|cadena-instrumentalizacion|funding|reconstruccion-unitaria|public-authority)/i.test(pathname);
    const styles = () => {
      if (document.getElementById('refurbishment-multitrack-styles')) return;
      const style = document.createElement('style');
      style.id = 'refurbishment-multitrack-styles';
      style.textContent = `.ref-multi{max-width:1120px;margin:0 auto;border-left:6px solid #8c2f2c;background:#fff7f5;border-radius:15px;padding:1.05rem 1.2rem}.ref-multi h2{margin:.15rem 0 .5rem}.ref-multi-kicker{margin:0 0 .35rem;font-size:.75rem;font-weight:850;letter-spacing:.07em;text-transform:uppercase;color:#8c2f2c}.ref-multi-label{display:inline-block;border:1px solid #8c2f2c;border-radius:999px;padding:.23rem .62rem;font-size:.75rem;font-weight:850}.ref-multi-dark{background:#13252d;color:#fff;border-left:0}.ref-multi-dark h2,.ref-multi-dark a{color:#fff}`;
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
    if (isCanonical && !document.querySelector('[data-refurbishment-multitrack-canonical]')) {
      styles(); insert(section(`<aside class="ref-multi" data-refurbishment-multitrack-canonical="20260820"><p class="ref-multi-kicker">${copy.kicker}</p><span class="ref-multi-label">${copy.label}</span><p>${copy.cross}</p></aside>`));
    }
    if ((isHome || isUpdates || isControl) && !document.querySelector('[data-refurbishment-multitrack-update]')) {
      styles(); insert(section(`<aside class="ref-multi ref-multi-dark" data-refurbishment-multitrack-update="20260820"><p class="ref-multi-kicker" style="color:#f2c7c1">${copy.kicker}</p><h2>${copy.title}</h2><p>${copy.body}</p><p><a href="${canonical}">${copy.action}</a></p></aside>`));
    }
    if (!isCanonical && relevant && !document.querySelector('[data-refurbishment-multitrack-crosslink]')) {
      styles(); insert(section(`<aside class="ref-multi" data-refurbishment-multitrack-crosslink="20260820"><p class="ref-multi-kicker">${copy.kicker}</p><h2>${copy.title}</h2><p>${copy.cross}</p><p><a href="${canonical}">${copy.action}</a></p></aside>`));
    }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, {once:true}); else run();
  window.setTimeout(run, 1800);
})();

(() => {
  const path = location.pathname.replace(/\/index\.html$/, '/').replace(/\/+$/, '/');
  if (!/(?:\/por-derecho)?\/(?:es|en)\/$/.test(path)) return;

  let observer;
  let scheduled = false;

  const deduplicate = (selector) => {
    const nodes = [...document.querySelectorAll(selector)];
    nodes.slice(1).forEach((node) => node.remove());
  };

  const placeAfter = (node, reference) => {
    if (!node || !reference || reference.nextElementSibling === node) return;
    reference.insertAdjacentElement('afterend', node);
  };

  const ensureFullRecord = (main, isEnglish, coreNodes) => {
    let wrapper = main.querySelector(':scope > [data-audience-full-record]');
    if (!wrapper) {
      wrapper = document.createElement('section');
      wrapper.className = 'audience-full-record';
      wrapper.dataset.audienceFullRecord = '20260823';
      wrapper.innerHTML = `<details><summary class="shell"><span>${isEnglish ? 'Continue into the full record' : 'Continuar con el expediente completo'}</span><strong>${isEnglish ? 'Reverse chronology, operating platform, recovery, institutions, future and source register' : 'Cronología inversa, plataforma operativa, recuperación, instituciones, futuro y registro de fuentes'}</strong><em>${isEnglish ? 'Open the complete page' : 'Abrir la página completa'}</em></summary><div data-audience-full-record-content></div></details>`;
    }
    const content = wrapper.querySelector('[data-audience-full-record-content]');
    const protectedNodes = new Set([...coreNodes, wrapper].filter(Boolean));
    for (const child of [...main.children]) {
      if (!protectedNodes.has(child)) content.appendChild(child);
    }
    return wrapper;
  };

  const openHashTarget = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    const target = document.getElementById(id);
    const details = target?.closest('[data-audience-full-record] details');
    if (!details) return;
    details.open = true;
    requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
  };

  const reconcile = () => {
    scheduled = false;
    const main = document.querySelector('main');
    if (!main) return;

    observer?.disconnect();
    deduplicate('.prosecution-entry-20260821');
    deduplicate('[data-prosecution-entry-20260821]');

    const isEnglish = document.documentElement.lang === 'en';
    const hero = main.querySelector(':scope > #inicio, :scope > #home, :scope > .hero');
    const priority = main.querySelector(':scope > .priority-band');
    const prosecution = main.querySelector(':scope > .prosecution-entry-20260821, :scope > [data-prosecution-entry-20260821]');
    const summary = document.getElementById(isEnglish ? 'sixty-second-summary' : 'resumen-60-segundos');
    const audiences = document.getElementById('psr-reader-intent');
    const perimeters = document.getElementById(isEnglish ? 'case-perimeters' : 'perimetros-del-caso');
    const sourceFunds = main.querySelector('.source-funds-notice-section');
    const sanTelmo = main.querySelector('section.interview-evidence[data-pd-san-telmo-attribution="20260819"]');
    const coreSections = [hero, priority, prosecution, summary, audiences, perimeters];
    if (sourceFunds) coreSections.push(sourceFunds);
    if (sanTelmo) coreSections.push(sanTelmo);

    let anchor = priority || hero;
    for (const section of [prosecution, summary, audiences, perimeters]) {
      if (section && anchor) {
        placeAfter(section, anchor);
        anchor = section;
      }
    }
    const fullRecord = ensureFullRecord(main, isEnglish, coreSections);
    placeAfter(fullRecord, perimeters || audiences || summary || prosecution || anchor);
    if (sourceFunds) placeAfter(sourceFunds, fullRecord);
    if (sanTelmo) {
      sanTelmo.classList.add('shell');
      placeAfter(sanTelmo, sourceFunds || fullRecord);
      sanTelmo.dataset.audienceProtectedSanTelmo = '20260823';
    }

    if (prosecution) {
      prosecution.dataset.audienceProtectedAttribution = '20260823';
      if (prosecution.closest('[data-audience-full-record]')) {
        placeAfter(prosecution, priority || hero);
      }
    }

    main.dataset.audienceOrder = '20260823';
    main.dataset.expressCriminalAttributionVisible = prosecution ? '20260823' : 'pending';
    main.dataset.sanTelmoAttributionVisible = sanTelmo ? '20260823' : 'pending';
    observer?.observe(main, { childList: true });
    openHashTarget();
  };

  const schedule = () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(reconcile);
  };

  const start = () => {
    const main = document.querySelector('main');
    if (!main) return;
    observer = new MutationObserver(schedule);
    observer.observe(main, { childList: true });
    window.addEventListener('hashchange', openHashTarget);
    document.addEventListener('pd:san-telmo-attribution-ready', schedule);
    document.addEventListener('click', (event) => {
      const link = event.target.closest('a[href^="#"]');
      if (!link) return;
      const target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
      const details = target?.closest('[data-audience-full-record] details');
      if (details) details.open = true;
    });
    reconcile();
    [500, 1700, 3500, 6000].forEach((delay) => setTimeout(reconcile, delay));
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
})();

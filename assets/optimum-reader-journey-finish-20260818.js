(() => {
  const path = location.pathname.replace(/\/+$/, '/') || '/';
  const isEn = /\/en\//.test(path);
  const lang = isEn ? 'en' : 'es';
  const root = `/por-derecho/${lang}/`;
  const p = (slug = '') => `${root}${slug}`;
  const t = (es, en) => isEn ? en : es;

  const updatesUrl = p(isEn ? 'updates/' : 'actualizaciones/');
  const collaborateUrl = p(isEn ? 'collaborate/' : 'colaborar/');
  const cnmvUrl = p(isEn ? 'cnmv-ricpe-verification/' : 'cnmv-ricpe-verificacion/');
  const fundingUrl = p(isEn ? 'same-hotel-multiple-financial-lives/' : 'mismo-hotel-multiples-vidas-financieras/');
  const ricpeControlsUrl = p(isEn ? 'ricpe-documentary-accountability/' : 'ricpe-responsabilidad-documental/');
  const controlUrl = p(isEn ? 'sun-park-takeover-7-june-2018/' : 'toma-control-sun-park-7-junio-2018/');
  const actasUrl = p(isEn ? 'community-instrumentalisation/minutes-2011-2022/' : 'comunidad-instrumentalizacion/actas-2011-2022/');

  const ensureMobileMenu = () => {
    const header = document.querySelector('.site-header');
    const nav = header?.querySelector('.main-nav');
    if (!header || !nav || header.querySelector('.nav-toggle')) return;
    if (!nav.id) nav.id = 'main-nav';
    const button = document.createElement('button');
    button.className = 'nav-toggle';
    button.type = 'button';
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-controls', nav.id);
    button.textContent = t('Menú', 'Menu');
    const close = () => {
      nav.classList.remove('open');
      button.setAttribute('aria-expanded', 'false');
    };
    button.addEventListener('click', () => {
      const open = !nav.classList.contains('open');
      nav.classList.toggle('open', open);
      button.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', (event) => {
      if (event.target.closest('a')) close();
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') close();
    });
    nav.insertAdjacentElement('beforebegin', button);
  };

  const navLink = (href, label, extra = '') => `<a ${extra} href="${href}">${label}</a>`;

  const simplifyHeaderNavigation = () => {
    const nav = document.querySelector('.site-header .main-nav');
    if (!nav || nav.dataset.psrOptimised === '1') return;
    let html = null;
    if (new RegExp(`/por-derecho/${lang}/?$`).test(path)) {
      html = [
        navLink(isEn ? '#sixty-second-summary' : '#resumen-60-segundos', t('Caso', 'Case')),
        navLink('#recuperacion', t('Recuperación', 'Recovery')),
        navLink('#registro', t('Evidencia', 'Evidence')),
        navLink('#mapa-institucional', t('Instituciones', 'Institutions')),
        navLink(
          isEn ? '#institutional-accountability-12aug-en' : '#institutional-accountability-12aug',
          t('AC y Juez', 'AC & Judge'),
          'class="nav-accountability"'
        ),
        navLink('#futuro', t('Futuro', 'Future')),
        navLink(updatesUrl, t('Actualizaciones', 'Updates'), 'class="nav-update"'),
        navLink(collaborateUrl, t('Colaborar', 'Collaborate')),
        navLink(isEn ? '../es/' : '../en/', isEn ? 'ES' : 'EN', `class="language-link" lang="${isEn ? 'es' : 'en'}"`)
      ].join('');
    } else if (/\/ric-private-equity-sun-park\/$/.test(path)) {
      html = [
        navLink('#psr-ricpe-cockpit', t('Resumen', 'Overview')),
        navLink('#psr-ricpe-five-docs', t('Qué cambió', 'What changed')),
        navLink(ricpeControlsUrl, t('Controles', 'Controls')),
        navLink(cnmvUrl, 'CNMV'),
        navLink(fundingUrl, t('Fondos', 'Funding')),
        navLink('#respuesta', t('Respuesta', 'Response')),
        navLink(updatesUrl, t('Actualizaciones', 'Updates'), 'class="nav-update"'),
        navLink(isEn ? '../../es/ric-private-equity-sun-park/' : '../../en/ric-private-equity-sun-park/', isEn ? 'ES' : 'EN', `class="language-link" lang="${isEn ? 'es' : 'en'}"`)
      ].join('');
    } else if (/\/(comunidad-instrumentalizacion|community-instrumentalisation)\/$/.test(path)) {
      html = [
        navLink('#resumen', t('Resumen', 'Overview')),
        navLink(actasUrl, t('Actas', 'Minutes')),
        navLink('#pwc-2016', 'PwC 2016'),
        navLink('#psr-community-to-ricpe', t('Puente RICPE', 'RICPE bridge')),
        navLink(controlUrl, t('7 junio', '7 June')),
        navLink('#prueba-pendiente', t('Prueba pendiente', 'Evidence gaps')),
        navLink(updatesUrl, t('Actualizaciones', 'Updates'), 'class="nav-update"'),
        navLink(isEn ? '../../es/comunidad-instrumentalizacion/' : '../../en/community-instrumentalisation/', isEn ? 'ES' : 'EN', `class="language-link" lang="${isEn ? 'es' : 'en'}"`)
      ].join('');
    } else if (/\/(toma-control-sun-park-7-junio-2018|sun-park-takeover-7-june-2018)\/$/.test(path)) {
      html = [
        navLink('#perimetros-juridicos', t('Perímetros', 'Perimeters')),
        navLink('#sun-park-no-estaba-abandonado', t('Actividad', 'Activity')),
        navLink('#salida-financiada-ona', 'ONA'),
        navLink('#hechos-7-junio', t('Hechos', 'Events')),
        navLink('#administrador-y-juez', t('AC y Juez', 'Administrator / Court')),
        navLink('#proyecto-antes-del-titulo', 'RICPE'),
        navLink('#prueba-pendiente', t('Prueba', 'Evidence')),
        navLink(isEn ? '../../es/toma-control-sun-park-7-junio-2018/' : '../../en/sun-park-takeover-7-june-2018/', isEn ? 'ES' : 'EN', `class="language-link" lang="${isEn ? 'es' : 'en'}"`)
      ].join('');
    }
    if (html) {
      nav.dataset.psrOptimised = '1';
      nav.innerHTML = html;
    }
  };

  const simplifyHomeHero = () => {
    if (!new RegExp(`/por-derecho/${lang}/?$`).test(path)) return;
    const actions = document.querySelector('main > .hero .actions');
    if (!actions || actions.dataset.psrOptimised === '1') return;
    actions.dataset.psrOptimised = '1';
    actions.innerHTML = `<a class="button" href="#psr-reader-intent">${t('Elegir mi ruta', 'Choose my route')}</a><a class="button secondary" href="${isEn ? '#sixty-second-summary' : '#resumen-60-segundos'}">${t('Caso en 60 segundos', 'Case in 60 seconds')}</a>`;
  };

  const movePrefaceModulesAfterHero = () => {
    const main = document.querySelector('main');
    const hero = main?.querySelector(':scope > .dossier-hero, :scope > .cnmv-hero, :scope > .eu-hero, :scope > .ir-hero, :scope > .hero, :scope > section.hero');
    if (!main || !hero) return;
    const before = [];
    for (const child of [...main.children]) {
      if (child === hero) break;
      before.push(child);
    }
    if (!before.length) return;
    let cursor = document.getElementById('psr-depth-switcher') || hero;
    for (const node of before) {
      cursor.insertAdjacentElement('afterend', node);
      cursor = node;
    }
  };

  const sectionId = (section, fallback) => {
    if (!section) return null;
    if (!section.id) section.id = fallback;
    return `#${section.id}`;
  };

  const addPractitionerShortcuts = () => {
    const hero = document.querySelector('main > .ir-hero, main > .eu-hero');
    if (!hero || hero.querySelector('.psr-hero-shortcuts')) return;
    const lead = hero.querySelector('.lead');
    if (!lead) return;
    const cardSelector = hero.classList.contains('ir-hero') ? '.ir-card' : '.eu-card';
    const sections = [...document.querySelectorAll('main > section')];
    const quickSection = sections.find((section) => section.querySelectorAll(cardSelector).length >= 6);
    const decisionSection = sections.find((section) => section.querySelector('.ok-decision'));
    const practice = document.querySelector(isEn ? '#open-practice' : '#practica-abierta');
    const quick = sectionId(quickSection, 'psr-practitioner-seven-minute');
    const decision = sectionId(decisionSection, 'psr-practitioner-decision-tree');
    const links = document.createElement('div');
    links.className = 'psr-hero-shortcuts';
    links.innerHTML = `${quick ? `<a href="${quick}">${t('Revisión en 7 minutos', '7-minute review')}</a>` : ''}${decision ? `<a href="${decision}">${t('Árbol de decisión', 'Decision tree')}</a>` : ''}${practice ? `<a href="#${practice.id}">${t('Buena práctica / advertencia', 'Good practice / warning')}</a>` : ''}`;
    lead.insertAdjacentElement('afterend', links);
  };

  const alignJourneyRailMobile = () => {
    if (!matchMedia('(max-width: 640px)').matches) return;
    const rail = document.getElementById('psr-unitary-journey');
    const scroller = rail?.querySelector('.shell');
    const current = rail?.querySelector('[aria-current="step"]');
    if (!scroller || !current) return;
    scroller.scrollTo({ left: Math.max(0, current.offsetLeft - 10), behavior: 'auto' });
  };

  const restoreDeepLink = () => {
    if (!location.hash) return;
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!target) return;
    requestAnimationFrame(() => target.scrollIntoView({ block: 'start', behavior: 'auto' }));
  };

  const apply = () => {
    simplifyHeaderNavigation();
    simplifyHomeHero();
    ensureMobileMenu();
    movePrefaceModulesAfterHero();
    addPractitionerShortcuts();
    alignJourneyRailMobile();
    restoreDeepLink();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => setTimeout(apply, 5600), { once: true });
  else setTimeout(apply, 5600);
  setTimeout(apply, 7200);
})();

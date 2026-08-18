(() => {
  const path = location.pathname.replace(/\/+$/, '/') || '/';
  const isEn = /\/en\//.test(path);
  const t = (es, en) => isEn ? en : es;

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

  const ensureIdByHeading = (patterns, fallback) => {
    for (const section of document.querySelectorAll('main > section')) {
      const heading = section.querySelector('h1,h2,h3')?.textContent?.trim() || '';
      if (patterns.some((pattern) => pattern.test(heading))) {
        if (!section.id) section.id = fallback;
        return `#${section.id}`;
      }
    }
    return null;
  };

  const addPractitionerShortcuts = () => {
    const hero = document.querySelector('main > .ir-hero, main > .eu-hero');
    if (!hero || hero.querySelector('.psr-hero-shortcuts')) return;
    const lead = hero.querySelector('.lead');
    if (!lead) return;
    const isIncentives = hero.classList.contains('ir-hero');
    const quick = ensureIdByHeading(
      isIncentives ? [/caso en 7 minutos/i, /case in 7 minutes/i] : [/caso en 7 minutos/i, /case in 7 minutes/i],
      'psr-practitioner-seven-minute'
    );
    const decision = ensureIdByHeading([/árbol de decisión/i, /decision tree/i], 'psr-practitioner-decision-tree');
    const practice = document.querySelector(isEn ? '#open-practice' : '#practica-abierta');
    const links = document.createElement('div');
    links.className = 'psr-hero-shortcuts';
    links.innerHTML = `${quick ? `<a href="${quick}">${t('Revisión en 7 minutos', '7-minute review')}</a>` : ''}${decision ? `<a href="${decision}">${t('Árbol de decisión', 'Decision tree')}</a>` : ''}${practice ? `<a href="#${practice.id}">${t('Buena práctica / advertencia', 'Good practice / warning')}</a>` : ''}`;
    lead.insertAdjacentElement('afterend', links);
  };

  const restoreDeepLink = () => {
    if (!location.hash) return;
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!target) return;
    requestAnimationFrame(() => target.scrollIntoView({ block: 'start', behavior: 'auto' }));
  };

  const apply = () => {
    ensureMobileMenu();
    addPractitionerShortcuts();
    restoreDeepLink();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => setTimeout(apply, 5600), { once: true });
  else setTimeout(apply, 5600);
  setTimeout(apply, 7200);
})();

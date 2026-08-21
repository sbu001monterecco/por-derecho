(() => {
  const ready = (callback) => {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', callback, { once: true });
    else callback();
  };

  const normalisePath = (value) => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };

  const repoPrefix = () => (location.pathname.includes('/por-derecho/') ? '/por-derecho/' : '/');

  const linkExists = (container, href) => {
    const expected = normalisePath(new URL(href, location.origin).pathname);
    return [...container.querySelectorAll('a[href]')].some((link) => {
      const actual = normalisePath(new URL(link.getAttribute('href'), location.href).pathname);
      return actual === expected;
    });
  };

  const addLink = (container, item, selector) => {
    if (!container || linkExists(container, item.href)) return;
    const link = document.createElement('a');
    link.href = item.href;
    link.textContent = item.label;
    if (item.current && normalisePath(location.pathname).endsWith(item.route)) link.setAttribute('aria-current', 'page');
    const before = selector ? container.querySelector(selector) : null;
    container.insertBefore(link, before || null);
  };

  ready(() => {
    if (document.querySelector('[data-sitewide-discovery-nav-mounted]')) return;
    document.documentElement.dataset.sitewideDiscoveryNavMounted = '20260821';

    const path = normalisePath(location.pathname);
    const lang = (document.documentElement.lang || '').toLowerCase();
    const isSpanish = lang.startsWith('es') || path.includes('/es/');
    const prefix = repoPrefix();
    const entries = isSpanish
      ? [
          { href: `${prefix}es/buscar/`, label: 'Buscar', route: '/es/buscar/', current: true },
          { href: `${prefix}es/indice-web/`, label: 'Indice', route: '/es/indice-web/', current: true },
          { href: `${prefix}es/por-derecho/`, label: 'Por Derecho', route: '/es/por-derecho/' },
        ]
      : [
          { href: `${prefix}en/search/`, label: 'Search', route: '/en/search/', current: true },
          { href: `${prefix}en/site-index/`, label: 'Site Index', route: '/en/site-index/', current: true },
          { href: `${prefix}en/por-derecho/`, label: 'Foundation', route: '/en/por-derecho/' },
        ];

    document.querySelectorAll('.main-nav').forEach((nav) => {
      entries.forEach((item) => addLink(nav, item, '.language-link,[hreflang]'));
    });

    document.querySelectorAll('.priority-links').forEach((band) => {
      entries.slice(0, 2).forEach((item) => addLink(band, item, '[href*="updates/"],[href*="actualizaciones/"],[data-series-fg-priority]'));
    });
  });
})();

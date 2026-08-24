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
    document.documentElement.dataset.sitewideDiscoveryNavMounted = '20260822';

    const path = normalisePath(location.pathname);
    const lang = (document.documentElement.lang || '').toLowerCase();
    const isSpanish = lang.startsWith('es') || path.includes('/es/');
    const prefix = repoPrefix();
    const entries = isSpanish
      ? [
          { href: `${prefix}es/buscar/`, label: 'Buscar', route: '/es/buscar/', current: true },
          { href: `${prefix}es/indice-web/`, label: 'Indice', route: '/es/indice-web/', current: true },
          { href: `${prefix}es/por-derecho/`, label: 'Por Derecho', route: '/es/por-derecho/' },
          { href: `${prefix}es/por-que-debe-importar-al-reino-unido/`, label: 'Por qué UK', route: '/es/por-que-debe-importar-al-reino-unido/', current: true },
        ]
      : [
          { href: `${prefix}en/search/`, label: 'Search', route: '/en/search/', current: true },
          { href: `${prefix}en/site-index/`, label: 'Site Index', route: '/en/site-index/', current: true },
          { href: `${prefix}en/por-derecho/`, label: 'Foundation', route: '/en/por-derecho/' },
          { href: `${prefix}en/why-the-uk-should-care/`, label: 'Why the UK?', route: '/en/why-the-uk-should-care/', current: true },
        ];

    document.querySelectorAll('.main-nav').forEach((nav) => {
      entries.forEach((item) => addLink(nav, item, '.language-link,[hreflang]'));
    });

    document.querySelectorAll('.priority-links').forEach((band) => {
      entries.slice(0, 2).forEach((item) => addLink(band, item, '[href*="updates/"],[href*="actualizaciones/"],[data-series-fg-priority]'));
    });

    if (!document.querySelector('[data-why-uk-home-gateway]')) {
      const homeRoute = isSpanish ? '/es/' : '/en/';
      if (path.endsWith(homeRoute)) {
        const anchor = document.querySelector(isSpanish ? '#plataforma-construida-2011-2018' : '#platform-built-2011-2018');
        if (anchor) {
          const section = document.createElement('section');
          section.className = 'section';
          section.dataset.whyUkHomeGateway = '20260822';
          const href = isSpanish
            ? `${prefix}es/por-que-debe-importar-al-reino-unido/`
            : `${prefix}en/why-the-uk-should-care/`;
          const eyebrow = isSpanish
            ? 'Sociedad británica · inversión española · daño transfronterizo'
            : 'British company · Spanish investment · cross-border harm';
          const title = isSpanish
            ? 'Por qué el Reino Unido debe mirar más allá del hotel de Lanzarote'
            : 'Why the United Kingdom should look beyond the Lanzarote hotel';
          section.innerHTML = `<div class="shell"><a class="dossier-link side-dossier-gateway" href="${href}"><span>${eyebrow}</span><strong>${title}</strong><i aria-hidden="true">→</i></a></div>`;
          anchor.insertAdjacentElement('afterend', section);
        }
      }
    }
  });
})();

/* PUBLIC-OUTREACH-CLARITY-ROUTE-LOADER-20260821 */
(() => {
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path.toLowerCase();
  };
  const path = normalise(location.pathname);
  const routes = [
    '/es/carta-abierta-trabajadores-acosta-matos/',
    '/en/open-letter-workers-acosta-matos/',
    '/es/carta-abierta-trabajadores-mynd-yaiza/',
    '/en/open-letter-workers-mynd-yaiza/',
    '/es/colaborar/',
    '/en/collaborate/'
  ];
  if (!routes.some(route => path.endsWith(route))) return;
  if (document.querySelector('script[data-public-outreach-clarity-loader]')) return;

  const current = document.currentScript;
  if (!current) return;
  const module = document.createElement('script');
  module.src = new URL('public-outreach-clarity-20260821.js?v=20260821a', current.src).href;
  module.async = false;
  module.dataset.publicOutreachClarityLoader = '20260821';
  document.head.appendChild(module);
})();

/* CLIFFE-JONES-RELATIONSHIP-RESPONSIBILITY-MAP-ROUTE-LOADER-20260822 */
(() => {
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path.toLowerCase();
  };
  const path = normalise(location.pathname);
  const routes = [
    '/en/sun-park-takeover-7-june-2018/camel-travel-lanzarote-information/',
    '/es/toma-control-sun-park-7-junio-2018/camel-travel-lanzarote-information/'
  ];
  if (!routes.some(route => path.endsWith(route))) return;
  if (document.querySelector('script[data-cliffe-jones-relationship-map-loader]')) return;

  const current = document.currentScript;
  if (!current) return;
  const module = document.createElement('script');
  module.src = new URL('cliffe-jones-relationship-responsibility-map-20260822.js?v=20260822a', current.src).href;
  module.async = false;
  module.dataset.cliffeJonesRelationshipMapLoader = '20260822';
  document.head.appendChild(module);
})();

/* CAM-DIRECT-INSTRUCTION-SHADOW-ADMIN-JUDICIAL-OMISSION-ROUTE-LOADER-20260823 */
(() => {
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path.toLowerCase();
  };
  const path = normalise(location.pathname);
  const routes = [
    '/en/sun-park-takeover-7-june-2018/',
    '/es/toma-control-sun-park-7-junio-2018/',
    '/en/insolvency-classification-parallel-lives/',
    '/es/calificacion-concurso-36-2012-vidas-paralelas/',
    '/en/acosta-matos-perimeter/',
    '/es/acosta-matos-perimetro/',
    '/en/insolvency-36-2012-insolvency-administrator/',
    '/es/concurso-36-2012-administrador-concursal/',
    '/en/insolvency-36-2012-mercantile-court-1/',
    '/es/concurso-36-2012-magistrado-juez/',
    '/en/lender-of-record/liability/',
    '/es/acreedor-de-registro/responsabilidad/',
    '/en/de-facto-administration-community-ac/',
    '/es/administracion-de-hecho-comunidad-ac/',
    '/en/sun-park-criminal-engineering-investigation/',
    '/es/ingenieria-forense-criminal-sun-park/',
    '/en/unitary-criminal-reverse-engineering/',
    '/es/ingenieria-inversa-criminal-unitaria/'
  ];
  if (!routes.some(route => path.endsWith(route))) return;
  if (document.querySelector('script[data-cam-direct-instruction-loader]')) return;

  const current = document.currentScript;
  if (!current) return;
  const module = document.createElement('script');
  module.src = new URL('cam-direct-instruction-shadow-admin-judicial-omission-20260823.js?v=20260824a', current.src).href;
  module.async = false;
  module.dataset.camDirectInstructionLoader = '20260824';
  document.head.appendChild(module);
})();

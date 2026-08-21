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

/* PRIVACY-FIRST-PUBLIC-RECORD-AI-ASSISTANT-20260821 */
(async () => {
  if (location.pathname.toLowerCase().includes('/admin/')) return;
  const current = document.currentScript;
  if (!current || document.querySelector('script[data-psr-ai-assistant-loader]')) return;

  let config = { enabled: true, apiBase: '' };
  try {
    const response = await fetch(new URL('chatbot-config-20260821.json?v=20260821a', current.src).href, { cache: 'no-store' });
    if (response.ok) config = { ...config, ...(await response.json()) };
  } catch {}
  window.PSR_CHAT_CONFIG = { ...(window.PSR_CHAT_CONFIG || {}), ...config };
  if (config.enabled === false) return;

  // GitHub Pages is static and cannot safely hold the API key. On that host the
  // widget is activated only when an external function-capable API base is
  // deliberately configured. Function-capable Netlify/custom app hosts can use
  // the same-origin /api routes with an empty apiBase.
  const configuredBase = String(window.PSR_CHAT_CONFIG?.apiBase || '').trim();
  const staticGitHubHost = location.hostname.endsWith('github.io');
  if (staticGitHubHost && !configuredBase) return;

  const syncActivePrivacyDisclosure = () => {
    const lang = (document.documentElement.lang || '').toLowerCase();
    const isEs = lang.startsWith('es') || location.pathname.includes('/es/');
    document.querySelectorAll('.status-list div').forEach((row) => {
      const label = (row.querySelector('dt')?.textContent || '').toLowerCase();
      if (!/funcionamiento actual|current site operation/.test(label)) return;
      const dd = row.querySelector('dd');
      if (dd) dd.textContent = isEs
        ? 'Asistente IA habilitado; analítica agregada solo con consentimiento separado; sin cookies no esenciales propias'
        : 'AI assistant enabled; aggregate analytics only with separate consent; no site-set non-essential cookies';
    });
    document.querySelectorAll('.privacy-table tr').forEach((row) => {
      const label = (row.querySelector('th')?.textContent || '').toLowerCase();
      if (!/cookies y analítica|cookies and analytics/.test(label)) return;
      const td = row.querySelector('td');
      if (td) td.innerHTML = isEs
        ? 'El asistente IA puede funcionar sin analítica. La analítica del asistente solo se activa mediante una casilla separada y almacena agregados diarios sin pregunta, transcripción, respuesta, IP ni identificador persistente. El sitio no instala cookies no esenciales propias para esta función. Consulte el <a href="../asistente-ia-privacidad/">aviso específico del asistente IA</a>.'
        : 'The AI assistant can operate without analytics. Assistant analytics are activated only through a separate checkbox and store daily aggregates without the question, transcript, answer, IP address or persistent identifier. The site does not set its own non-essential cookies for this function. See the <a href="../ai-assistant-privacy/">AI assistant privacy notice</a>.';
    });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', syncActivePrivacyDisclosure, { once: true });
  else syncActivePrivacyDisclosure();

  const css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = new URL('chatbot-widget-20260821.css?v=20260821a', current.src).href;
  css.dataset.psrAiAssistantCss = '20260821';
  document.head.appendChild(css);

  const module = document.createElement('script');
  module.src = new URL('chatbot-widget-20260821.js?v=20260821a', current.src).href;
  module.async = false;
  module.dataset.psrAiAssistantLoader = '20260821';
  document.head.appendChild(module);
})();

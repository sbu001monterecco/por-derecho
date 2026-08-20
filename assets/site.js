(() => {
  const current = document.currentScript;
  if (!current) return;

  // Preserve and execute the complete pre-highlight site loader unchanged.
  const prior = document.createElement('script');
  prior.src = new URL('site-pre-intervencion-highlight-20260820.js?v=20260820a', current.src).href;
  prior.async = false;
  prior.setAttribute('data-pre-intervencion-site-loader', 'true');
  document.head.appendChild(prior);

  // Highlight the 24-Feb-2026 Integrity Commission consideration and the protected-assets
  // Justice referral recorded by the signed 5-Mar-2026 Intervención General response.
  const protectedAssets = document.createElement('script');
  protectedAssets.src = new URL('intervencion-protected-assets-highlight-20260820.js?v=20260820a', current.src).href;
  protectedAssets.async = false;
  protectedAssets.setAttribute('data-intervencion-protected-assets-loader', 'true');
  document.head.appendChild(protectedAssets);
})();


/* SOURCE-OF-FUNDS-NOTICE-20260820 */
(() => {
  const current = document.currentScript;
  const base = current && current.src ? new URL('.', current.src) : new URL('/assets/', location.href);
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalise(location.pathname);
  const exact = new Map([
    ['/es/', ['full', '#historia-reconstruida', 'after']],
    ['/en/', ['full', null, 'append']],
    ['/es/ric-private-equity-sun-park/', ['full', '#respuesta', 'before']],
    ['/en/ric-private-equity-sun-park/', ['full', '#response', 'before']],
    ['/es/mismo-hotel-multiples-vidas-financieras/', ['full', null, 'append']],
    ['/en/same-hotel-multiple-financial-lives/', ['full', null, 'append']],
    ['/es/acosta-matos-perimetro/', ['full', null, 'append']],
    ['/en/acosta-matos-perimeter/', ['full', null, 'append']],
    ['/es/objetivos-recuperacion-restitucion/', ['full', '#vias', 'before']],
    ['/en/recovery-restitution-objectives/', ['full', null, 'append']],
    ['/es/cadena-instrumentalizacion-ric-fondos-incentivos/', ['full', null, 'append']],
    ['/en/institutionalisation-chain-ric-eu-incentives/', ['full', null, 'append']],
    ['/es/ricpe-responsabilidad-documental/', ['compact', null, 'append']],
    ['/en/ricpe-documentary-accountability/', ['compact', null, 'append']],
    ['/es/pwc-canarias-carlos-saavedra-sun-park/', ['compact', null, 'append']],
    ['/en/pwc-canarias-carlos-saavedra-sun-park/', ['compact', null, 'append']],
    ['/es/rsm/nnr4-1025c2f66/', ['compact', null, 'append']],
    ['/en/rsm/nnr4-1025c2f66/', ['compact', null, 'append']],
    ['/es/grant-thornton/cuyas-canarias/', ['compact', null, 'append']],
    ['/en/grant-thornton/cuyas-canarias/', ['compact', null, 'append']],
    ['/es/grant-thornton/2024-04/', ['compact', null, 'append']],
    ['/en/grant-thornton/2024-04/', ['compact', null, 'append']],
    ['/es/actores-partes-abogados-representantes/', ['compact', null, 'append']],
    ['/en/actors-parties-lawyers-representatives/', ['compact', null, 'append']],
    ['/es/san-telmo-ricpe-sun-park/', ['compact', null, 'append']],
    ['/en/san-telmo-ricpe-sun-park/', ['compact', null, 'append']]
  ]);
  const match = [...exact.entries()].find(([suffix]) => path.endsWith(suffix));
  if (!match || document.querySelector('[data-source-of-funds-notice]')) return;

  const [variant, selector, position] = match[1];
  const section = document.createElement('section');
  section.className = 'section source-funds-notice-section';
  section.setAttribute('aria-label', document.documentElement.lang === 'en'
    ? 'Source of funds and professional services notice'
    : 'Aviso sobre procedencia de fondos y servicios profesionales');
  const shell = document.createElement('div');
  shell.className = 'shell';
  const mount = document.createElement('div');
  mount.dataset.sourceOfFundsNotice = variant;
  shell.append(mount);
  section.append(shell);

  const anchor = selector ? document.querySelector(selector) : null;
  const main = document.querySelector('main');
  if (!main) return;
  if (anchor && position === 'before') anchor.insertAdjacentElement('beforebegin', section);
  else if (anchor && position === 'after') anchor.insertAdjacentElement('afterend', section);
  else main.append(section);

  const component = document.createElement('script');
  component.src = new URL('source-of-funds-notice-20260820.js', base).href;
  component.dataset.sourceFundsComponent = '20260820';
  document.head.append(component);
})();

/* AC-COMMUNITY-DE-FACTO-ADMINISTRATION-LOADERS-20260820 */
(() => {
  const current = document.currentScript;
  if (!current) return;
  const base = new URL('.', current.src);

  const baseModule = document.createElement('script');
  baseModule.src = new URL('ac-community-de-facto-administration-20260820.js?v=20260820b', base).href;
  baseModule.async = false;
  baseModule.setAttribute('data-ac-community-de-facto-administration-loader', 'true');
  document.head.appendChild(baseModule);

  const visibility = document.createElement('script');
  visibility.src = new URL('ac-de-facto-knowing-facilitation-visibility-20260820.js?v=20260820b', base).href;
  visibility.async = false;
  visibility.setAttribute('data-ac-de-facto-knowing-facilitation-visibility-loader', 'true');
  document.head.appendChild(visibility);

  const stability = document.createElement('script');
  stability.src = new URL('ac-de-facto-knowing-facilitation-stability-20260820.js?v=20260820b', base).href;
  stability.async = false;
  stability.setAttribute('data-ac-de-facto-knowing-facilitation-stability-loader', 'true');
  document.head.appendChild(stability);
})();

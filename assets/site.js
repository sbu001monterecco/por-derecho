(() => {
  const current = document.currentScript;
  if (!current) return;

  // Preserve and execute the complete pre-highlight site loader unchanged.
  const prior = document.createElement('script');
  prior.src = new URL('site-pre-intervencion-highlight-20260820.js?v=20260824d', current.src).href;
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
    ['/es/ric-private-equity-sun-park/', ['full', 'main > section:first-of-type', 'after', true]],
    ['/en/ric-private-equity-sun-park/', ['full', 'main > section:first-of-type', 'after', true]],
    ['/es/mismo-hotel-multiples-vidas-financieras/', ['full', null, 'append']],
    ['/en/same-hotel-multiple-financial-lives/', ['full', null, 'append']],
    ['/es/acosta-matos-perimetro/', ['full', 'main > section:first-of-type', 'after', true]],
    ['/en/acosta-matos-perimeter/', ['full', 'main > section:first-of-type', 'after', true]],
    ['/es/objetivos-recuperacion-restitucion/', ['full', '#vias', 'before']],
    ['/en/recovery-restitution-objectives/', ['full', null, 'append']],
    ['/es/cadena-instrumentalizacion-ric-fondos-incentivos/', ['full', 'main > section:first-of-type', 'after', true]],
    ['/en/institutionalisation-chain-ric-eu-incentives/', ['full', 'main > section:first-of-type', 'after', true]],
    ['/es/ricpe-responsabilidad-documental/', ['full', 'main > section:first-of-type', 'after', true]],
    ['/en/ricpe-documentary-accountability/', ['full', 'main > section:first-of-type', 'after', true]],
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
    ['/es/continuidad-defensa-letrados/', ['compact', null, 'append']],
    ['/en/counsel-defence-continuity/', ['compact', null, 'append']],
    ['/es/san-telmo-ricpe-sun-park/', ['compact', null, 'append']],
    ['/en/san-telmo-ricpe-sun-park/', ['compact', null, 'append']]
  ]);
  const match = [...exact.entries()].find(([suffix]) => path.endsWith(suffix));
  const placeSourceFundsNotice = () => {
  if (!match || document.querySelector('[data-source-of-funds-notice]')) return;

  const [variant, selector, position, showEmailGraphics = false] = match[1];
  const section = document.createElement('section');
  section.className = 'section source-funds-notice-section';
  if (showEmailGraphics) section.classList.add('source-funds-notice-section--featured');
  section.setAttribute('aria-label', document.documentElement.lang === 'en'
    ? 'Source of funds and professional services notice'
    : 'Aviso sobre procedencia de fondos y servicios profesionales');
  const shell = document.createElement('div');
  shell.className = 'shell';
  const mount = document.createElement('div');
  mount.dataset.sourceOfFundsNotice = variant;

  if (showEmailGraphics) {
    const isEnglish = document.documentElement.lang === 'en';
    const notice = new URL(isEnglish
      ? '../en/source-of-funds-professional-services-notice/'
      : '../es/aviso-procedencia-fondos-servicios-profesionales/', base);
    const graphicData = isEnglish
      ? [
          {
            src: 'evidence/email-used-20260822/san-telmo-ricpe-sun-park-stamp-v1-EN.png?v=20260822g',
            alt: 'San Telmo, RICPE and Sun Park professional-overlap and traceability graphic',
            caption: 'San Telmo · RICPE · Sun Park'
          },
          {
            src: 'evidence/email-used-20260822/pwc-five-actors-plus-ac-2016-knowledge-checkpoint-EN.png?v=20260822g',
            alt: 'PwC five-actor and Acosta Matos 2016 professional knowledge checkpoint graphic',
            caption: 'PwC · five actors + IA · open the 15–26 April 2016 chain',
            href: new URL('../en/evidence-pwc-sun-park-meeting-21-april-2016/#sequence', base).href,
            ariaLabel: 'PwC 2016 professional-knowledge checkpoint. The client made the penal-route decision and PwC acknowledged it; this is not an independent PwC finding that any named person committed an offence. Open the complete 15–26 April 2016 chain.'
          }
        ]
      : [
          {
            src: 'evidence/email-used-20260822/san-telmo-ricpe-sun-park-stamp-v1-ES.png?v=20260822g',
            alt: 'Gráfico San Telmo, RICPE y Sun Park sobre solapamiento profesional y trazabilidad',
            caption: 'San Telmo · RICPE · Sun Park'
          },
          {
            src: 'evidence/email-used-20260822/pwc-five-actors-plus-ac-2016-knowledge-checkpoint-ES.png?v=20260822g',
            alt: 'Gráfico PwC, cinco actores y Acosta Matos sobre el punto de conocimiento profesional de 2016',
            caption: 'PwC · cinco actores + AC · abrir cadena 15–26 abril 2016',
            href: new URL('../es/evidencia-pwc-junta-sun-park-21-abril-2016/#secuencia', base).href,
            ariaLabel: 'Punto de conocimiento profesional PwC de 2016. El cliente decidió e instruyó seguir la vía penal y PwC acusó recibo; no es una conclusión independiente de PwC de que una persona nombrada cometiera delito. Abrir la cadena completa de 15–26 abril 2016.'
          }
        ];
    const intro = document.createElement('header');
    intro.className = 'source-funds-email-graphics-intro';
    const introKicker = document.createElement('p');
    introKicker.className = 'source-funds-email-graphics-intro__kicker';
    introKicker.textContent = isEnglish
      ? 'Documented professional traceability checkpoint'
      : 'Punto documentado de trazabilidad profesional';
    const introTitle = document.createElement('h2');
    introTitle.textContent = isEnglish
      ? 'Two documentary graphics. One verification question.'
      : 'Dos gráficos documentales. Una cuestión de verificación.';
    const introLead = document.createElement('p');
    introLead.textContent = isEnglish
      ? 'Examine the professional, hotel and funding perimeter before acting. Select either source-controlled graphic, then read the preservation notice immediately below.'
      : 'Examine el perímetro profesional, hotelero y financiero antes de actuar. Seleccione cualquiera de los gráficos de fuente controlada y lea después el aviso de preservación situado inmediatamente debajo.';
    intro.append(introKicker, introTitle, introLead);

    const graphics = document.createElement('div');
    graphics.className = 'source-funds-email-graphics';
    graphics.dataset.emailGraphics = '20260822';
    graphicData.forEach(item => {
      const link = document.createElement('a');
      link.className = 'source-funds-email-graphic';
      link.href = item.href || `${notice.href}#${isEnglish ? 'scope' : 'alcance'}`;
      link.setAttribute('aria-label', item.ariaLabel || `${item.caption} — ${isEnglish ? 'read the full professional notice' : 'leer el aviso profesional completo'}`);
      const image = document.createElement('img');
      image.src = new URL(item.src, base).href;
      image.alt = item.alt;
      image.width = 1800;
      image.height = 1200;
      image.loading = item.loading || 'eager';
      if (!item.loading) image.fetchPriority = 'high';
      image.decoding = 'async';
      const caption = document.createElement('span');
      caption.textContent = item.caption;
      link.append(image, caption);
      graphics.append(link);
    });
    shell.append(intro, graphics);
  }

  shell.append(mount);
  section.append(shell);

  const anchor = selector ? document.querySelector(selector) : null;
  const main = document.querySelector('main');
  if (!main) return;
  if (anchor && position === 'before') anchor.insertAdjacentElement('beforebegin', section);
  else if (anchor && position === 'after') anchor.insertAdjacentElement('afterend', section);
  else main.append(section);

  if (showEmailGraphics && position === 'after') {
    const pinFeaturedSection = () => {
      const opening = document.querySelector('main > section:first-of-type');
      if (opening && opening.nextElementSibling !== section) {
        opening.insertAdjacentElement('afterend', section);
      }
    };
    const placementGuard = new MutationObserver(pinFeaturedSection);
    placementGuard.observe(main, { childList: true });
    window.addEventListener('load', pinFeaturedSection, { once: true });
    pinFeaturedSection();
  }

  const component = document.createElement('script');
  component.src = new URL('source-of-funds-notice-20260820.js?v=20260822d', base).href;
  component.dataset.sourceFundsComponent = '20260820';
  document.head.append(component);
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', placeSourceFundsNotice, { once: true });
  } else {
    placeSourceFundsNotice();
  }
})();

/* AC-COMMUNITY-DE-FACTO-ADMINISTRATION-LOADERS-20260824 */
(() => {
  const current = document.currentScript;
  if (!current) return;
  const base = new URL('.', current.src);

  const baseModule = document.createElement('script');
  baseModule.src = new URL('ac-community-de-facto-administration-20260820.js?v=20260824a', base).href;
  baseModule.async = false;
  baseModule.setAttribute('data-ac-community-de-facto-administration-loader', 'true');
  document.head.appendChild(baseModule);

  const visibility = document.createElement('script');
  visibility.src = new URL('ac-de-facto-knowing-facilitation-visibility-20260820.js?v=20260824a', base).href;
  visibility.async = false;
  visibility.setAttribute('data-ac-de-facto-knowing-facilitation-visibility-loader', 'true');
  document.head.appendChild(visibility);

  const stability = document.createElement('script');
  stability.src = new URL('ac-de-facto-knowing-facilitation-stability-20260820.js?v=20260824a', base).href;
  stability.async = false;
  stability.setAttribute('data-ac-de-facto-knowing-facilitation-stability-loader', 'true');
  document.head.appendChild(stability);
})();

/* ONSITE-APPROACHES-GATEWAY-20260820 */
(() => {
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalise(location.pathname);
  const routes = new Set([
    '/es/toma-control-sun-park-7-junio-2018/',
    '/en/sun-park-takeover-7-june-2018/',
    '/es/acosta-matos-perimetro/',
    '/en/acosta-matos-perimeter/'
  ]);
  const matched = [...routes].find(route => path.endsWith(route));
  if (!matched || document.querySelector('[data-onsite-approaches-gateway]')) return;

  const isEnglish = document.documentElement.lang === 'en';
  const basePrefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const target = isEnglish
    ? `${basePrefix}en/pre-7-june-2018-approaches-sun-park-onsite-manager/`
    : `${basePrefix}es/contactos-previos-responsable-in-situ-sun-park/`;

  const section = document.createElement('section');
  section.className = 'section alt';
  section.dataset.onsiteApproachesGateway = '20260820';
  section.innerHTML = `<div class="shell"><a class="dossier-link side-dossier-gateway" href="${target}"><span>${isEnglish ? 'Anonymised primary-evidence dossier · pre-7 June 2018' : 'Dossier probatorio anonimizado · antes del 7 de junio de 2018'}</span><strong>${isEnglish ? 'Repeated access approaches, a certified concealment proposal, sworn refusals and the unresolved implementation question' : 'Contactos repetidos, propuesta certificada de ocultación, negativas bajo declaración y la cuestión no resuelta de su ejecución'}</strong><i aria-hidden="true">→</i></a></div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const anchor = isEnglish ? document.querySelector('#events-of-7-june') : document.querySelector('#hechos-7-junio');
  if (anchor) anchor.insertAdjacentElement('beforebegin', section);
  else main.append(section);
})();

/* ASSET-RECOVERY-INTERVENTION-20260821 */
(() => {
  const current = document.currentScript;
  if (!current || document.querySelector('script[data-asset-recovery-intervention-loader]')) return;
  const module = document.createElement('script');
  module.src = new URL('asset-recovery-preservation-20260821.js?v=20260821a', current.src).href;
  module.async = false;
  module.setAttribute('data-asset-recovery-intervention-loader', '20260821');
  document.head.appendChild(module);
})();

/* TRACEABILITY-CROSSLINKS-AND-CGPJ-RECEIPT-20260821 */
(() => {
  const current = document.currentScript;
  if (!current || document.querySelector('script[data-traceability-crosslinks-loader]')) return;
  const module = document.createElement('script');
  module.src = new URL('traceability-crosslinks-20260821.js?v=20260821d', current.src).href;
  module.async = false;
  module.setAttribute('data-traceability-crosslinks-loader', '20260821');
  document.head.appendChild(module);
})();

/* SITEWIDE-DISCOVERY-NAV-20260821 */
(() => {
  const current = document.currentScript;
  if (!current || document.querySelector('script[data-sitewide-discovery-nav-loader]')) return;
  const module = document.createElement('script');
  module.src = new URL('sitewide-discovery-nav-20260821.js?v=20260824a', current.src).href;
  module.async = false;
  module.setAttribute('data-sitewide-discovery-nav-loader', '20260824');
  document.head.appendChild(module);
})();

/* PROSECUTION-PUBLIC-ENTRY-20260824 */
(() => {
  const current = document.currentScript;
  if (!current || document.querySelector('script[data-prosecution-public-entry-loader]')) return;
  const module = document.createElement('script');
  module.src = new URL('prosecution-public-entry-20260821.js?v=20260824a', current.src).href;
  module.async = false;
  module.setAttribute('data-prosecution-public-entry-loader', '20260824');
  document.head.appendChild(module);
})();

/* SUN-PARK-JUNTA-PWC-WARNING-20260822 */
(() => {
  const current = document.currentScript;
  if (!current || document.querySelector('script[data-junta-pwc-warning-loader]')) return;
  const module = document.createElement('script');
  module.src = new URL('sun-park-junta-pwc-warning-20260822.js?v=20260822c', current.src).href;
  module.async = false;
  module.setAttribute('data-junta-pwc-warning-loader', '20260822');
  document.head.appendChild(module);
})();

/* AUTHOR-REPORTING-PERSON-ALERTADOR-NOTICE-20260822 */
(() => {
  const current = document.currentScript;
  if (!current || document.querySelector('script[data-alertador-notice-loader]')) return;
  const module = document.createElement('script');
  module.src = new URL('alertador-notice-20260822.js?v=20260823a', current.src).href;
  module.async = false;
  module.setAttribute('data-alertador-notice-loader', '20260822');
  document.head.appendChild(module);
})();

/* PWC-VISUAL-APRIL-CHAIN-LINK-20260822 */
(() => {
  const current = document.currentScript;
  if (!current || document.querySelector('script[data-pwc-chain-link-loader]')) return;
  const module = document.createElement('script');
  module.src = new URL('pwc-visual-chain-link-20260822.js?v=20260822a', current.src).href;
  module.async = false;
  module.setAttribute('data-pwc-chain-link-loader', '20260822');
  document.head.appendChild(module);
})();

/* INHERITED-LOADER-VALIDATION-SENTINELS
case-information-architecture-20260819.js
jdam-architecture-colegios-20260820.js
playa-blanca-concept-home-20260820.js
palacete-san-bernardo-historica-marco.webp
san-telmo-attribution-correction-20260819.js?v=20260819a
data-san-telmo-attribution-loader
The executable loader chain for these modules remains in site-pre-intervencion-highlight-20260820.js.
*/

/* AUDIENCE-EXPERIENCE-ORDER-AND-DEDUPLICATION-20260823 */
(() => {
  const current = document.currentScript;
  if (!current || document.querySelector('script[data-audience-experience-loader]')) return;
  const module = document.createElement('script');
  module.src = new URL('audience-experience-order-20260823.js?v=20260824b', current.src).href;
  module.async = false;
  module.setAttribute('data-audience-experience-loader', '20260823');
  document.head.appendChild(module);
})();

/* CALIFICACION-CRIMINAL-MISUSE-THESIS-20260824 */
(() => {
  const current = document.currentScript;
  if (!current || document.querySelector('script[data-calificacion-misuse-thesis-loader]')) return;
  const module = document.createElement('script');
  module.src = new URL('calificacion-criminal-misuse-thesis-20260824.js?v=20260824d1', current.src).href;
  module.async = false;
  module.setAttribute('data-calificacion-misuse-thesis-loader', '20260824');
  document.head.appendChild(module);
})();

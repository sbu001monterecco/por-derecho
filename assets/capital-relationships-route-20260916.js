(() => {
  'use strict';
  const current = document.currentScript;
  const path = location.pathname.replace(/index\.html$/, '').replace(/\/+$/, '/');
  const isEN = /\/en\//.test(path) || document.documentElement.lang?.toLowerCase().startsWith('en');
  const root = '/por-derecho/' + (isEN ? 'en/' : 'es/');
  const capitalPath = root + (isEN ? 'capital-relationships/' : 'relaciones-de-capital/');
  const supported = new Set(isEN ? [
    '/por-derecho/en/strategic-financial-relationship/',
    '/por-derecho/en/platform-scale/',
    '/por-derecho/en/montana-roja/',
    '/por-derecho/en/open-letter-lanzarote/',
    '/por-derecho/en/collaborate/',
    '/por-derecho/en/capital-relationships/'
  ] : [
    '/por-derecho/es/relacion-financiera-estrategica/',
    '/por-derecho/es/escala-plataforma/',
    '/por-derecho/es/montana-roja/',
    '/por-derecho/es/carta-abierta-lanzarote/',
    '/por-derecho/es/colaborar/',
    '/por-derecho/es/relaciones-de-capital/'
  ]);
  if (!supported.has(path) || document.querySelector('[data-capital-route="20260916"]')) return;

  const ensureCss = () => {
    if (document.querySelector('link[data-capital-route-css="20260916"]') || document.querySelector('link[href*="capital-relationships-20260916.css"]')) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = new URL('capital-relationships-20260916.css?v=20260916a', current.src).href;
    link.dataset.capitalRouteCss = '20260916';
    document.head.appendChild(link);
  };
  ensureCss();

  const nav = document.querySelector('.main-nav');
  if (nav && !nav.querySelector(`a[href="${capitalPath}"]`) && !nav.querySelector('a[href*="capital-relationships/"]') && !nav.querySelector('a[href*="relaciones-de-capital/"]')) {
    const a = document.createElement('a');
    a.href = capitalPath;
    a.className = 'cr-nav-link';
    a.textContent = 'Capital';
    const language = nav.querySelector('.language-link');
    if (language) nav.insertBefore(a, language); else nav.appendChild(a);
  }

  const marker = document.createElement('span');
  marker.hidden = true;
  marker.dataset.capitalRoute = '20260916';
  document.body.appendChild(marker);

  if (path === capitalPath) return;

  if (/\/(?:collaborate|colaborar)\/$/.test(path)) {
    const calls = document.querySelector('.collab-calls');
    const existing = document.querySelector('[data-capital-collab="20260916"]');
    if (calls && !existing) {
      const card = document.createElement('article');
      card.className = 'collab-call';
      card.id = isEN ? 'capital-calls' : 'convocatoria-capital';
      card.dataset.collabTrack = 'future';
      card.dataset.capitalCollab = '20260916';
      card.innerHTML = isEN ? `
        <span class="collab-call-index">04A</span><div><div class="collab-call-meta"><span>The Future</span><span class="open">Selective</span></div><h3>Private capital relationship</h3><p>For a principal, single-family office, hotel-owning family, institutional/professional capital provider or trusted introducer who wants to test fit without a public securities offer or public investment terms.</p></div><div class="collab-call-details"><div><strong>Useful position</strong><span>Actual principal/decision-maker or a trusted person able to make a specific introduction</span></div><div><strong>Working boundary</strong><span>Public architecture first; role, jurisdiction and communication basis checked before restricted material</span></div></div><a href="${capitalPath}">Open the capital-relationship gateway →</a>` : `
        <span class="collab-call-index">04A</span><div><div class="collab-call-meta"><span>El Futuro</span><span class="open">Selectivo</span></div><h3>Relación privada de capital</h3><p>Para un principal, single-family office, familia propietaria de hoteles, proveedor institucional/profesional de capital o introductor de confianza que quiera comprobar el encaje sin oferta pública de valores ni condiciones públicas de inversión.</p></div><div class="collab-call-details"><div><strong>Posición útil</strong><span>Principal/decisor real o persona de confianza capaz de realizar una introducción concreta</span></div><div><strong>Límite de trabajo</strong><span>Primero arquitectura pública; función, jurisdicción y base de comunicación antes de material restringido</span></div></div><a href="${capitalPath}">Abrir la puerta de relaciones de capital →</a>`;
      const future = document.querySelector('#future-calls');
      if (future) future.after(card); else calls.appendChild(card);
    }
    return;
  }

  const copy = isEN ? {
    strong: 'Private capital relationship — public doorway only.',
    text: 'If a principal, institution or trusted introducer sees a potential fit, the next step is role and jurisdiction screening followed by an appropriate private process—not public investment terms or a subscription form.',
    cta: 'Open Capital Relationships →'
  } : {
    strong: 'Relación privada de capital — sólo puerta pública.',
    text: 'Si un principal, institución o introductor de confianza aprecia un posible encaje, el siguiente paso es comprobar función y jurisdicción y continuar por un proceso privado adecuado, no publicar condiciones de inversión ni un formulario de suscripción.',
    cta: 'Abrir Relaciones de Capital →'
  };

  const box = document.createElement('aside');
  box.className = 'cr-inline-gateway';
  box.dataset.capitalInline = '20260916';
  box.innerHTML = `<strong>${copy.strong}</strong><p>${copy.text}</p><a href="${capitalPath}">${copy.cta}</a>`;
  const selectors = isEN ? [
    ['strategic-financial-relationship', '.sfr-status'],
    ['platform-scale', '.ps-page-meta'],
    ['open-letter-lanzarote', '.lz-page-meta'],
    ['montana-roja', '.mr-readiness']
  ] : [
    ['relacion-financiera-estrategica', '.sfr-status'],
    ['escala-plataforma', '.ps-page-meta'],
    ['carta-abierta-lanzarote', '.lz-page-meta'],
    ['montana-roja', '.mr-readiness']
  ];
  const match = selectors.find(([slug]) => path.includes(`/${slug}/`));
  const anchor = match ? document.querySelector(match[1]) : null;
  if (anchor) {
    const placement = path.includes('/montana-roja/') ? (anchor.closest('section') || anchor) : anchor;
    placement.insertAdjacentElement('afterend', box);
  } else {
    document.querySelector('main')?.insertAdjacentElement('afterbegin', box);
  }
})();

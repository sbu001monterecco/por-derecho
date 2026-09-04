(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  if (!/\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(path)) return;

  const lang = (document.documentElement.lang || (path.includes('/en/') ? 'en' : 'es'))
    .toLowerCase().startsWith('en') ? 'en' : 'es';
  const normalise = value => String(value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[–—]/g, '-')
    .replace(/[^a-z0-9^]+/g, ' ')
    .trim()
    .replace(/\s+/g, ' ');

  const c22Terms = [
    'control 22','dp 1956','1956 2026','nig 3501643220260016826','iup li2026016921',
    'denuncia administrador concursal','insolvency administrator complaint','borja rodriguez batllori',
    'francisco de borja rodriguez batllori laffitte','administrador concursal denuncia',
    'sobreseimiento provisional administrador concursal','complaint control 22'
  ];
  const c24Terms = [
    'control 24','denuncia juez concurso','judge complaint insolvency 36 2012','alberto lopez villarrubia',
    'querella juez','querella magistrado','formal private prosecution complaint judge','tsjc control 24',
    '18 junio 2026 juez','25 junio 2026 complemento','denuncia magistrado concurso 36 2012'
  ];
  const sharedTerms = [
    'control 22 control 24','denuncias concurso 36 2012','acciones contra juez administrador concursal',
    'dp 1901 dp 1956 control 24','criminal complaints insolvency 36 2012','interconexion control 22 24'
  ];

  const matches = (query, terms) => {
    const q = normalise(query);
    if (q.length < 2) return false;
    return terms.some(term => {
      const t = normalise(term);
      return t.includes(q) || q.includes(t);
    });
  };

  const definitions = lang === 'en' ? [
    {
      id: 'CONTROL-22-DP1956-20260904',
      terms: c22Terms.concat(sharedTerms),
      href: '/por-derecho/en/control-22-insolvency-administrator-complaint/',
      badge: 'Complaint digitisation',
      code: 'CONTROL 22 · DP 1956/2026',
      title: 'Control 22 · insolvency-administrator complaint and DP 1956/2026',
      summary: '55-page complaint, later DP 1956 association, provisional dismissal, no filed appeal verified, actor-specific duty and accounting modules.'
    },
    {
      id: 'CONTROL-24-JUDGE-20260904',
      terms: c24Terms.concat(sharedTerms),
      href: '/por-derecho/en/control-24-insolvency-judge-complaint-36-2012/',
      badge: 'Judge-related complaint',
      code: 'CONTROL 24 · 18/25 JUNE 2026',
      title: 'Control 24 · complaint concerning the judge in Insolvency 36/2012',
      summary: '79-page signed package, 25 June supplement, five documentary modules, official allocation/outcome still unconfirmed, and formal private-complaint boundary.'
    }
  ] : [
    {
      id: 'CONTROL-22-DP1956-20260904',
      terms: c22Terms.concat(sharedTerms),
      href: '/por-derecho/es/control-22-denuncia-administrador-concursal/',
      badge: 'Digitalización de denuncia',
      code: 'CONTROL 22 · DP 1956/2026',
      title: 'Control 22 · denuncia sobre el Administrador Concursal y DP 1956/2026',
      summary: 'Denuncia de 55 páginas, asociación posterior a DP 1956, sobreseimiento provisional, recurso presentado no verificado y módulos de deber y contabilidad.'
    },
    {
      id: 'CONTROL-24-JUDGE-20260904',
      terms: c24Terms.concat(sharedTerms),
      href: '/por-derecho/es/control-24-denuncia-juez-concurso-36-2012/',
      badge: 'Denuncia relativa al juez',
      code: 'CONTROL 24 · 18/25 JUNIO 2026',
      title: 'Control 24 · denuncia relativa al juez del Concurso 36/2012',
      summary: 'Paquete firmado de 79 páginas, complemento de 25 de junio, cinco módulos documentales, reparto/resultado oficial no confirmado y límite respecto de la querella.'
    }
  ];

  const augment = () => {
    const input = document.querySelector('#canonical-home-search-input');
    const results = document.querySelector('.canonical-search-results');
    const status = document.querySelector('.canonical-search-status');
    if (!input || !results) return false;

    let added = 0;
    definitions.forEach(definition => {
      const existing = results.querySelector(`[data-search-result-id="${definition.id}"]`);
      if (!matches(input.value, definition.terms)) {
        if (existing) existing.remove();
        return;
      }
      if (existing) return;

      const card = document.createElement('a');
      card.className = 'canonical-search-result';
      card.href = definition.href;
      card.setAttribute('data-search-result-id', definition.id);
      card.innerHTML = `<span class="canonical-search-result-top"><span class="canonical-search-badge">${definition.badge}</span><span class="canonical-search-id">${definition.code}</span></span><strong>${definition.title}</strong><small>${definition.summary}</small>`;
      results.prepend(card);
      added += 1;
    });

    if (added > 0) {
      results.hidden = false;
      if (status) status.textContent = lang === 'en'
        ? 'Control 22 / Control 24 records located.'
        : 'Registros Control 22 / Control 24 localizados.';
    }
    return true;
  };

  const install = (attempt = 0) => {
    const input = document.querySelector('#canonical-home-search-input');
    const form = document.querySelector('.canonical-search-form');
    if (!input || !form) {
      if (attempt < 50) window.setTimeout(() => install(attempt + 1), 80);
      return;
    }
    input.addEventListener('input', () => window.setTimeout(augment, 0));
    form.addEventListener('submit', () => window.setTimeout(augment, 0));
    window.setTimeout(augment, 0);
  };

  install();
})();

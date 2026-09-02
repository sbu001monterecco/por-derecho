(() => {
  'use strict';

  const current = document.currentScript;
  if (!current) return;
  const pathname = window.location.pathname.replace(/\/index\.html$/, '/');
  const isHome = /\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(pathname);
  if (!isHome) return;

  const lang = (document.documentElement.lang || 'es').toLowerCase().startsWith('en') ? 'en' : 'es';
  const normalise = (value) => String(value || '')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
    .replace(/[–—]/g, '-').replace(/[^a-z0-9^]+/g, ' ').trim().replace(/\s+/g, ' ');
  const terms = [
    'borja', 'rodriguez batllori', 'separacion administrador concursal',
    'insolvency administrator removal', 'rpl 3304 2025', 'rpl 3319 2025',
    'aweswell', 'luchy playa blanca', 'articulo 100 trlc', 'article 100 trlc',
    'articulo 101 trlc', 'article 101 trlc', 'decreto 222 2026', 'decree 222 2026'
  ];
  const href = lang === 'es'
    ? '/por-derecho/es/concurso-36-2012-separacion-administrador-concursal-rpl-3304-2025/'
    : '/por-derecho/en/insolvency-36-2012-administrator-removal-rpl-3304-2025/';

  const matches = (query) => {
    const q = normalise(query);
    if (q.length < 2) return false;
    return terms.some((term) => normalise(term).includes(q) || q.includes(normalise(term)));
  };

  const augment = () => {
    const input = document.querySelector('#canonical-home-search-input');
    const results = document.querySelector('.canonical-search-results');
    const status = document.querySelector('.canonical-search-status');
    if (!input || !results) return false;
    const existing = results.querySelector('[data-search-result-id="BORJA-SEPARATION-RPL3304"]');
    if (!matches(input.value)) {
      if (existing) existing.remove();
      return true;
    }
    if (existing) return true;
    const card = document.createElement('a');
    card.className = 'canonical-search-result';
    card.href = href;
    card.setAttribute('data-search-result-id', 'BORJA-SEPARATION-RPL3304');
    card.innerHTML = lang === 'es'
      ? '<span class="canonical-search-result-top"><span class="canonical-search-badge">Expediente procesal</span><span class="canonical-search-id">GC-APP-005 ↔ GC-APP-006</span></span><strong>Separación del Administrador Concursal · RPL 3304/2025 consolidado</strong><small>Aweswell originó y recurrió; LPB recurrió independientemente; RPL 3319/2025 quedó acumulado en el rollo vivo RPL 3304/2025.</small>'
      : '<span class="canonical-search-result-top"><span class="canonical-search-badge">Procedural dossier</span><span class="canonical-search-id">GC-APP-005 ↔ GC-APP-006</span></span><strong>Insolvency Administrator removal · consolidated RPL 3304/2025</strong><small>Aweswell originated and appealed; LPB independently appealed; RPL 3319/2025 was accumulated into live RPL 3304/2025.</small>';
    results.prepend(card);
    results.hidden = false;
    if (status && !/resultado|result/i.test(status.textContent || '')) {
      status.textContent = lang === 'es' ? 'Expediente procesal localizado.' : 'Procedural dossier located.';
    }
    return true;
  };

  const install = (attempt = 0) => {
    const input = document.querySelector('#canonical-home-search-input');
    const form = document.querySelector('.canonical-search-form');
    if (!input || !form) {
      if (attempt < 20) window.setTimeout(() => install(attempt + 1), 50);
      return;
    }
    input.addEventListener('input', () => window.setTimeout(augment, 0));
    form.addEventListener('submit', () => window.setTimeout(augment, 0));
    window.setTimeout(augment, 0);
  };
  install();
})();

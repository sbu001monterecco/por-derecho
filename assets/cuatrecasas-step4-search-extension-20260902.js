(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const pathname = window.location.pathname.replace(/\/index\.html$/, '/');
  const isHome = /\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(pathname);
  if (!isHome) return;

  const lang = (document.documentElement.lang || 'es').toLowerCase().startsWith('en') ? 'en' : 'es';
  const normalise = (value) => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[–—]/g, '-').replace(/[^a-z0-9^]+/g, ' ').trim().replace(/\s+/g, ' ');
  const terms = ['cuatrecasas','step 4','why step 4','mandate inversion','inversion mandato','matkator','etj 163 2020','pagares','aweswell','special situations','linkedin cuatrecasas','fee enforcement','ejecucion honorarios'];
  const href = lang === 'es' ? '/por-derecho/es/cuatrecasas-mandato-continuidad-ric/#inversion-mandato' : '/por-derecho/en/cuatrecasas-sun-park/#why-step4';
  const matches = (query) => {
    const q = normalise(query);
    if (q.length < 2) return false;
    return terms.some(term => normalise(term).includes(q) || q.includes(normalise(term)));
  };

  const augment = () => {
    const input = document.querySelector('#canonical-home-search-input');
    const results = document.querySelector('.canonical-search-results');
    const status = document.querySelector('.canonical-search-status');
    if (!input || !results) return false;
    const existing = results.querySelector('[data-search-result-id="CUATRECASAS-WHY-STEP4"]');
    if (!matches(input.value)) { if (existing) existing.remove(); return true; }
    if (existing) return true;
    const card = document.createElement('a');
    card.className = 'canonical-search-result';
    card.href = href;
    card.setAttribute('data-search-result-id', 'CUATRECASAS-WHY-STEP4');
    card.innerHTML = lang === 'es'
      ? '<span class="canonical-search-result-top"><span class="canonical-search-badge">Publicación + expediente</span><span class="canonical-search-id">PD-PUB-CUAT-LINKEDIN-WHY-STEP4-20260902</span></span><strong>Cuatrecasas · ¿por qué ir directamente al Step 4?</strong><small>Mandato → pagarés/honorarios → Matkator → ETJ 163/2020 → pasarela económica Aweswell, con límites probatorios y de personalidad jurídica.</small>'
      : '<span class="canonical-search-result-top"><span class="canonical-search-badge">Publication + dossier</span><span class="canonical-search-id">PD-PUB-CUAT-LINKEDIN-WHY-STEP4-20260902</span></span><strong>Cuatrecasas · Why go straight to Step 4?</strong><small>Mandate → fee instruments → Matkator → ETJ 163/2020 → Aweswell economic gateway, with evidential and corporate-personality boundaries.</small>';
    results.prepend(card); results.hidden = false;
    if (status) status.textContent = lang === 'es' ? 'Nodo Cuatrecasas / Step 4 localizado.' : 'Cuatrecasas / Step 4 node located.';
    return true;
  };
  const install = (attempt = 0) => {
    const input = document.querySelector('#canonical-home-search-input');
    const form = document.querySelector('.canonical-search-form');
    if (!input || !form) { if (attempt < 20) window.setTimeout(() => install(attempt + 1), 50); return; }
    input.addEventListener('input', () => window.setTimeout(augment, 0));
    form.addEventListener('submit', () => window.setTimeout(augment, 0));
    window.setTimeout(augment, 0);
  };
  install();
})();

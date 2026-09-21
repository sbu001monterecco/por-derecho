(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  if (!/\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(path)) return;
  const lang = (document.documentElement.lang || 'es').toLowerCase().startsWith('en') ? 'en' : 'es';
  const normalise = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[–—]/g,'-').replace(/[^a-z0-9^]+/g,' ').trim().replace(/\s+/g,' ');
  const terms = [
    'finca 8584','8584','matkator','hotel title','titulo hotelero','remate','cesion del remate','adjudicacion','restitucion','restitution',
    'etj 163 2020','dp 748 2026','dp 711 2025','dp 552 2025','cuatrecasas','acosta matos','hotel new trend','hnt','canarian hospitality','mynd yaiza',
    'concurso 36 2012','unidad de explotacion','unity of operation','beneficiario real','real beneficiary','title is not the room','el titulo no es la habitacion'
  ];
  const href = lang === 'en' ? '/por-derecho/en/matkator-8584-hotel-title-remate-restitution/' : '/por-derecho/es/matkator-8584-titulo-hotel-remate-restitucion/';
  const matches = query => {
    const q = normalise(query);
    if (q.length < 2) return false;
    return terms.some(term => normalise(term).includes(q) || q.includes(normalise(term)));
  };
  const augment = () => {
    const input = document.querySelector('#canonical-home-search-input');
    const results = document.querySelector('.canonical-search-results');
    const status = document.querySelector('.canonical-search-status');
    if (!input || !results) return false;
    const id = 'MATKATOR-8584-HOTEL-TITLE-RESTITUTION-20260903';
    const existing = results.querySelector(`[data-search-result-id="${id}"]`);
    if (!matches(input.value)) { if (existing) existing.remove(); return true; }
    if (existing) return true;
    const card = document.createElement('a');
    card.className = 'canonical-search-result';
    card.href = href;
    card.setAttribute('data-search-result-id', id);
    card.innerHTML = lang === 'en'
      ? '<span class="canonical-search-result-top"><span class="canonical-search-badge">Canonical multitrack control</span><span class="canonical-search-id">PD-MAT8584-UCC-20260903-01</span></span><strong>Finca 8584 · the title is not the room</strong><small>Hotel title, adjudication, cession, restitution, DP 748, ETJ 163, DP 711, Concurso 36/2012 and the Acosta/HNT real-beneficiary hypothesis.</small>'
      : '<span class="canonical-search-result-top"><span class="canonical-search-badge">Control canónico multitrack</span><span class="canonical-search-id">PD-MAT8584-UCC-20260903-01</span></span><strong>Finca 8584 · el título no es la habitación</strong><small>Título hotelero, adjudicación, cesión, restitución, DP 748, ETJ 163, DP 711, Concurso 36/2012 e hipótesis de beneficiario real Acosta/HNT.</small>';
    results.prepend(card); results.hidden = false;
    if (status) status.textContent = lang === 'en' ? 'Finca 8584 hotel-title control located.' : 'Control de título hotelero finca 8584 localizado.';
    return true;
  };
  const install = (attempt = 0) => {
    const input = document.querySelector('#canonical-home-search-input');
    const form = document.querySelector('.canonical-search-form');
    if (!input || !form) { if (attempt < 40) window.setTimeout(() => install(attempt + 1), 75); return; }
    input.addEventListener('input', () => window.setTimeout(augment, 0));
    form.addEventListener('submit', () => window.setTimeout(augment, 0));
    window.setTimeout(augment, 0);
  };
  install();
})();

(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  if (!/\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(path)) return;
  const lang = (document.documentElement.lang || 'es').toLowerCase().startsWith('en') ? 'en' : 'es';
  const normalise = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[–—]/g,'-').replace(/[^a-z0-9^]+/g,' ').trim().replace(/\s+/g,' ');
  const terms = [
    'hotel fincas','fincas hoteleras','matkator fincas','finca 8584','finca 8588','8584','8588','title system','sistema de titulos',
    'title on title injury','title-on-title injury','lesion titulo sobre titulo','finca sobre finca','legal violence','violencia juridica',
    'unidad de explotacion','unity of exploitation','titulo habilitante','owner consent','consentimiento propietario',
    'cuatrecasas estafa procesal','completed procedural fraud','estafa procesal consumada','la laguna concurso 36 2012','cross proceeding instrumentality',
    'acosta matos hotel titles','hnt mynd titles','apropiacion fincas','appropriated hotel units','hotel title denominator',
    'aweswell lpb matkator injury','fraude concursal','procedural fraud insolvency'
  ];
  const href = lang === 'en'
    ? '/por-derecho/en/hotel-fincas-asset-classification-title-on-title-injury/'
    : '/por-derecho/es/fincas-hoteleras-clasificacion-lesion-titulo-sobre-titulo/';
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
    const id = 'HOTEL-FINCA-TITLE-SYSTEM-20260903';
    const existing = results.querySelector(`[data-search-result-id="${id}"]`);
    if (!matches(input.value)) { if (existing) existing.remove(); return true; }
    if (existing) return true;
    const card = document.createElement('a');
    card.className = 'canonical-search-result';
    card.href = href;
    card.setAttribute('data-search-result-id', id);
    card.innerHTML = lang === 'en'
      ? '<span class="canonical-search-result-top"><span class="canonical-search-badge">Canonical class control</span><span class="canonical-search-id">PD-HOTEL-FINCA-UCC-20260903-01</span></span><strong>All hotel fincas · asset classification and title-on-title injury</strong><small>Fincas 8584 and 8588, every Matkator title, the whole hotel denominator, alleged completed procedural fraud, La Laguna–Concurso 36/2012 instrumentality and Acosta/HNT multitrack effects.</small>'
      : '<span class="canonical-search-result-top"><span class="canonical-search-badge">Control canónico de clase</span><span class="canonical-search-id">PD-HOTEL-FINCA-UCC-20260903-01</span></span><strong>Todas las fincas hoteleras · clasificación y lesión título-sobre-título</strong><small>Fincas 8584 y 8588, todos los títulos Matkator, denominador completo del hotel, estafa procesal consumada alegada, instrumentalidad La Laguna–Concurso 36/2012 y efectos multitrack Acosta/HNT.</small>';
    results.prepend(card);
    results.hidden = false;
    if (status) status.textContent = lang === 'en' ? 'Hotel-finca title-system control located.' : 'Control del sistema de fincas hoteleras localizado.';
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

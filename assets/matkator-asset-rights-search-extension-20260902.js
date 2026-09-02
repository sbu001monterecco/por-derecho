(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const pathname = window.location.pathname.replace(/\/index\.html$/, '/');
  const segments = pathname.split('/').filter(Boolean);
  const isHome = segments.length === 0
    || (segments.length === 1 && ['por-derecho','es','en'].includes(segments[0]))
    || (segments.length === 2 && segments[0] === 'por-derecho' && ['es','en'].includes(segments[1]));
  if (!isHome) return;

  const lang = (document.documentElement.lang || 'es').toLowerCase().startsWith('en') ? 'en' : 'es';
  const normalise = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[–—]/g,'-').replace(/[^a-z0-9]+/g,' ').trim().replace(/\s+/g,' ');
  const terms = [
    'matkator','markator','matkartor','matkator assets','matkator rights','asset rights register','registro activos derechos matkator',
    'finca 8584','8 584','apartment 758','apartamento 758','finca 8588','8 588','apartment 510','apartamento 510',
    'etj 163 2020','remate matkator','mandate inversion','inversion mandato','debtor perimeter','perimetro deudor','achilles heel','gateway','special situations','pagares'
  ];
  const href = lang === 'es'
    ? '/por-derecho/es/registro-activos-derechos-matkator/'
    : '/por-derecho/en/matkator-asset-rights-register/';

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
    const existing = results.querySelector('[data-search-result-id="MATKATOR-ASSET-RIGHTS-20260902"]');
    if (!matches(input.value)) {
      if (existing) existing.remove();
      return true;
    }
    if (existing) return true;
    const card = document.createElement('a');
    card.className = 'canonical-search-result';
    card.href = href;
    card.setAttribute('data-search-result-id','MATKATOR-ASSET-RIGHTS-20260902');
    card.innerHTML = lang === 'es'
      ? '<span class="canonical-search-result-top"><span class="canonical-search-badge">Registro patrimonial</span><span class="canonical-search-id">PD-REG-MATKATOR-ASSETS-RIGHTS-20260902</span></span><strong>Matkator · activos, derechos y perímetro de ejecución</strong><small>Finca 8.584 = objeto ETJ actual; finca 8.588 = activo histórico separado; cuentas, créditos y derechos procesales clasificados sin confundir LPB o Aweswell con Matkator.</small>'
      : '<span class="canonical-search-result-top"><span class="canonical-search-badge">Patrimonial register</span><span class="canonical-search-id">PD-REG-MATKATOR-ASSETS-RIGHTS-20260902</span></span><strong>Matkator · assets, rights and execution perimeter</strong><small>Finca 8,584 = current ETJ object; finca 8,588 = separate historical asset; accounts, receivables and procedural rights classified without conflating LPB or Aweswell with Matkator.</small>';
    results.prepend(card);
    results.hidden = false;
    if (status) status.textContent = lang === 'es' ? 'Registro patrimonial localizado.' : 'Patrimonial register located.';
    return true;
  };

  const install = (attempt = 0) => {
    const input = document.querySelector('#canonical-home-search-input');
    const form = document.querySelector('.canonical-search-form');
    if (!input || !form) {
      if (attempt < 25) window.setTimeout(() => install(attempt + 1), 60);
      return;
    }
    input.addEventListener('input', () => window.setTimeout(augment,0));
    form.addEventListener('submit', () => window.setTimeout(augment,0));
    window.setTimeout(augment,0);
  };
  install();
})();

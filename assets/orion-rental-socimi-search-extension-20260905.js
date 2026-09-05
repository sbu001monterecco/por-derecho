(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  if (!/\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(path)) return;
  const lang = (document.documentElement.lang || 'es').toLowerCase().startsWith('en') ? 'en' : 'es';
  const normalise = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[–—]/g,'-').replace(/[^a-z0-9^]+/g,' ').trim().replace(/\s+/g,' ');
  const terms = [
    'orion','orion rental','orion rental socimi','socimi','agm','agm canary asset management','pamalexsha','francisco mario matos matas','fmmm',
    'jose daniel acosta matos','jdam','enrique guerra','ricpe orion','ric private equity orion','hinojeros','hinojeros iii',
    'predatory inclusion','inclusion depredadora','shield and sword','escudo y espada','illicit shield','escudo ilicito','house of cards','casa de naipes',
    'clandestine non compliance','incumplimiento clandestino','chronic deliberate concealment','ocultacion deliberada cronica','non disclosure','falta de divulgacion',
    'forced collaborator','colaborador forzado','pamalexsha agm','acosta matos orion','fmmm orion'
  ];
  const href = lang === 'en' ? '/por-derecho/en/orion-rental-socimi/' : '/por-derecho/es/orion-rental-socimi/';
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
    const id = 'PD-SP-O-0027-ORION-RENTAL-SOCIMI';
    const existing = results.querySelector(`[data-search-result-id="${id}"]`);
    if (!matches(input.value)) { if (existing) existing.remove(); return true; }
    if (existing) return true;
    const card = document.createElement('a');
    card.className = 'canonical-search-result';
    card.href = href;
    card.setAttribute('data-search-result-id', id);
    card.innerHTML = lang === 'en'
      ? '<span class="canonical-search-result-top"><span class="canonical-search-badge">Corporate continuity dossier</span><span class="canonical-search-id">PD-SP-O-0027</span></span><strong>Orion Rental SOCIMI · AGM / RICPE / Acosta Matos / FMMM continuity</strong><small>Audited governance and related-party chain; Gil Marer\'s attributed “predatory inclusion / shield and sword” thesis; disclosure and due-diligence proof gates.</small>'
      : '<span class="canonical-search-result-top"><span class="canonical-search-badge">Dossier de continuidad societaria</span><span class="canonical-search-id">PD-SP-O-0027</span></span><strong>Orion Rental SOCIMI · continuidad AGM / RICPE / Acosta Matos / FMMM</strong><small>Cadena auditada de gobierno y partes vinculadas; tesis atribuida de Gil Marer de “inclusión depredadora / escudo y espada”; pruebas de divulgación y diligencia debida.</small>';
    results.prepend(card);
    results.hidden = false;
    if (status) status.textContent = lang === 'en' ? 'Orion Rental SOCIMI dossier located.' : 'Dossier Orion Rental SOCIMI localizado.';
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

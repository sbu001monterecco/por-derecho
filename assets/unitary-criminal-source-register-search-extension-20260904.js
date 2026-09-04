(() => {
  'use strict';

  // UNITARY-CRIMINAL-SOURCE-REGISTER-SEARCH-20260904
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

  const baselineTerms = [
    'redsara','red sara','regage','registro penal fuentes','registro fuentes penales',
    'criminal source register','redsara criminal source register','75 comunicaciones','75 communications',
    '75 regage','154 paginas','154 pages','125 sha 512','sha 512 attachments','anexo 4 ministerio fiscal',
    'annex 4 ministerio fiscal','pd redsara mf register 20260903 01','regage26e00004212180',
    'regage26e00004639835','regage26e00005026215','regage26e00005031882','regage26e00006380826',
    'regage26e00006889281','regage26e00007274391','regage26e00009989396','regage26e00010347207'
  ];
  const continuityTerms = [
    'continuidad ministerio fiscal','ministerio fiscal continuity','fiscalia redsara continuidad',
    'redsara continuity','post anexo redsara','post annex redsara','97 registros','97 registrations',
    '90 recibidos 7 rechazados','90 received 7 rejected','denominador posterior','later denominator',
    'email sent draft self archive fiscalia','pd mf continuity 20260904 01','regage26e00070237051',
    'regage26e00070235399','regage26e00070234288'
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
      id: 'PD-REDSARA-MF-REGISTER-20260903-01',
      terms: baselineTerms,
      href: '/por-derecho/en/criminal-source-register/',
      badge: 'Source provenance',
      code: '75 REGAGE · 125 SHA-512',
      title: 'RedSARA criminal-source register',
      summary: 'Searchable public-safe baseline: 75 registered communications, 125 attachment hashes and 9/9 current PDFs matched byte-for-byte to the 154-page Annex 4 source.'
    },
    {
      id: 'PD-MF-CONTINUITY-20260904-01',
      terms: continuityTerms,
      href: '/por-derecho/en/ministerio-fiscal-redsara-continuity/',
      badge: 'Prosecution continuity',
      code: '75 + 22 · LATER OPEN',
      title: 'Ministerio Fiscal / RedSARA continuity',
      summary: 'Additive chronology separating the 75-receipt baseline, 22 later registrations, later formal checkpoints, SENT email and Fiscalía responses without inventing a final later denominator.'
    }
  ] : [
    {
      id: 'PD-REDSARA-MF-REGISTER-20260903-01',
      terms: baselineTerms,
      href: '/por-derecho/es/registro-fuentes-penales/',
      badge: 'Procedencia de fuentes',
      code: '75 REGAGE · 125 SHA-512',
      title: 'Registro penal de fuentes RedSARA',
      summary: 'Línea base pública y minimizada con búsqueda: 75 comunicaciones registradas, 125 huellas de anexos y 9/9 PDFs actuales cotejados byte a byte con el Anexo 4 de 154 páginas.'
    },
    {
      id: 'PD-MF-CONTINUITY-20260904-01',
      terms: continuityTerms,
      href: '/por-derecho/es/ministerio-fiscal-continuidad-redsara/',
      badge: 'Continuidad Fiscalía',
      code: '75 + 22 · POSTERIOR ABIERTO',
      title: 'Continuidad Ministerio Fiscal / RedSARA',
      summary: 'Cronología aditiva que separa la línea base de 75 justificantes, 22 registros posteriores, checkpoints formales posteriores, email SENT y respuestas de Fiscalía sin inventar un denominador final.'
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
        ? 'RedSARA / Ministerio Fiscal source records located.'
        : 'Registros de fuentes RedSARA / Ministerio Fiscal localizados.';
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

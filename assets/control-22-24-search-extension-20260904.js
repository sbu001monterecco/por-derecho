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

  const triangleTerms = [
    'concurso 36 2012','concurso ordinario 36 2012','insolvency 36 2012','accountability triangle',
    'triangulo responsabilidad','triangulo concurso','private actors ac judge','actores privados administrador juez',
    'control 21','nexus 36','nexus36','dp 1901 2026','control 22','dp 1956 2026','control 24',
    '18 june 2026','18 junio 2026','25 june 2026','25 junio 2026','cgpj 169 2026','di 169 2026',
    'alzada 286 2026','recurso de alzada 286 2026','dip 2 2026','icalpa 80 2026','dip 80 2026',
    'separacion administrador concursal','removal insolvency administrator','honorarios administrador concursal',
    'rpl 2523 2025','rpl 3304 2025','rpl 3319 2025','rpl 421 2026','fiscalia neutralizada',
    'prosecution neutralised','interconexion procedimientos','interconnectivity proceedings'
  ];
  const c22Terms = [
    'control 22','dp 1956','1956 2026','nig 3501643220260016826','iup li2026016921',
    'denuncia administrador concursal','insolvency administrator complaint','borja rodriguez batllori',
    'francisco de borja rodriguez batllori laffitte','administrador concursal denuncia',
    'sobreseimiento provisional administrador concursal','complaint control 22'
  ];
  const c24Terms = [
    'control 24','denuncia juez concurso','judge complaint insolvency 36 2012','alberto lopez villarrubia',
    'querella juez','querella magistrado','formal private prosecution complaint judge','tsjc control 24',
    '18 junio 2026 juez','18 june 2026 judge','25 junio 2026 complemento','25 june 2026 supplement',
    'denuncia magistrado concurso 36 2012','cgpj 169','alzada 286','dip 2 2026'
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
      id: 'CONCURSO36-ACCOUNTABILITY-TRIANGLE-20260904',
      terms: triangleTerms,
      href: '/por-derecho/en/concurso-36-2012-accountability-triangle/',
      badge: 'Canonical interconnectivity graph',
      code: 'CONTROLS 21 · 22 · 24',
      title: 'Insolvency 36/2012 · private actors, Administrator and judge',
      summary: 'Interactive triangle linking DP 1901, DP 1956, Control 24, CGPJ 169, Appeal 286, DIP 2, ICALPA 80, removal/fees and RPL 2523 while preserving separate identities and evidence states.'
    },
    {
      id: 'CONTROL-22-DP1956-20260904',
      terms: c22Terms,
      href: '/por-derecho/en/control-22-insolvency-administrator-complaint/',
      badge: 'Administrator complaint',
      code: 'CONTROL 22 · DP 1956/2026',
      title: 'Control 22 · insolvency-administrator complaint and DP 1956/2026',
      summary: 'Filing locator and related criminal route, provisional dismissal, certified reparto bridge still required, plus links to ICALPA 80 and removal/fees.'
    },
    {
      id: 'CONTROL-24-JUDGE-20260904',
      terms: c24Terms,
      href: '/por-derecho/en/control-24-insolvency-judge-complaint-36-2012/',
      badge: 'Canonical judge-related intake record',
      code: 'CONTROL 24 · 18/25 JUNE 2026',
      title: 'Control 24 · complaint concerning the judge in Insolvency 36/2012',
      summary: 'Complaint filed on 18 June, dependent 25 June supplement, official allocation/outcome unresolved, linked without merger to CGPJ 169, Appeal 286 and DIP 2.'
    }
  ] : [
    {
      id: 'CONCURSO36-ACCOUNTABILITY-TRIANGLE-20260904',
      terms: triangleTerms,
      href: '/por-derecho/es/concurso-36-2012-triangulo-responsabilidad/',
      badge: 'Grafo canónico de interconexión',
      code: 'CONTROLES 21 · 22 · 24',
      title: 'Concurso 36/2012 · actores privados, Administrador y juez',
      summary: 'Triángulo interactivo que enlaza DP 1901, DP 1956, Control 24, CGPJ 169, Alzada 286, DIP 2, ICALPA 80, separación/honorarios y RPL 2523 preservando identidades y estados probatorios.'
    },
    {
      id: 'CONTROL-22-DP1956-20260904',
      terms: c22Terms,
      href: '/por-derecho/es/control-22-denuncia-administrador-concursal/',
      badge: 'Denuncia relativa al Administrador',
      code: 'CONTROL 22 · DP 1956/2026',
      title: 'Control 22 · denuncia sobre el Administrador Concursal y DP 1956/2026',
      summary: 'Localizador de presentación y vía penal relacionada, sobreseimiento provisional, puente de reparto certificado aún requerido y enlaces a ICALPA 80 y separación/honorarios.'
    },
    {
      id: 'CONTROL-24-JUDGE-20260904',
      terms: c24Terms,
      href: '/por-derecho/es/control-24-denuncia-juez-concurso-36-2012/',
      badge: 'Registro canónico relativo al juez',
      code: 'CONTROL 24 · 18/25 JUNIO 2026',
      title: 'Control 24 · denuncia relativa al juez del Concurso 36/2012',
      summary: 'Denuncia presentada el 18 de junio, complemento dependiente de 25 de junio, reparto/resultado oficial sin resolver y enlace sin fusión a CGPJ 169, Alzada 286 y DIP 2.'
    }
  ];

  const augment = () => {
    const input = document.querySelector('#canonical-home-search-input');
    const results = document.querySelector('.canonical-search-results');
    const status = document.querySelector('.canonical-search-status');
    if (!input || !results) return false;

    let visible = 0;
    definitions.forEach(definition => {
      const existing = results.querySelector(`[data-search-result-id="${definition.id}"]`);
      if (!matches(input.value, definition.terms)) {
        if (existing) existing.remove();
        return;
      }
      visible += 1;
      if (existing) return;
      const card = document.createElement('a');
      card.className = 'canonical-search-result';
      card.href = definition.href;
      card.setAttribute('data-search-result-id', definition.id);
      card.innerHTML = `<span class="canonical-search-result-top"><span class="canonical-search-badge">${definition.badge}</span><span class="canonical-search-id">${definition.code}</span></span><strong>${definition.title}</strong><small>${definition.summary}</small>`;
      results.prepend(card);
    });

    if (visible > 0) {
      results.hidden = false;
      if (status) status.textContent = lang === 'en'
        ? 'Insolvency 36/2012 accountability graph located.'
        : 'Grafo de responsabilidad de Concurso 36/2012 localizado.';
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

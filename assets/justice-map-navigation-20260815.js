(() => {
  const path = location.pathname;
  const isEs = path.includes('/es/');
  const isJustice = path.includes('/justicia-registro-institucional/') || path.includes('/justice-institutional-record/');
  const target = isEs ? '/por-derecho/es/justicia-registro-institucional/' : '/por-derecho/en/justice-institutional-record/';
  const label = isEs ? 'Mapa de Justicia' : 'Justice Map';

  if (!isJustice) {
    document.querySelectorAll('.main-nav').forEach(nav => {
      if (nav.querySelector('[data-justice-map-link]')) return;
      const a = document.createElement('a');
      a.href = target;
      a.textContent = label;
      a.dataset.justiceMapLink = 'true';
      const language = nav.querySelector('.language-link');
      if (language) nav.insertBefore(a, language); else nav.appendChild(a);
    });
  }

  const isInstitutional = path.includes('/registros-institucionales/') || path.includes('/institutional-records/');
  if (isInstitutional && !document.querySelector('[data-justice-map-callout]')) {
    const main = document.querySelector('main');
    if (!main) return;
    const box = document.createElement('section');
    box.dataset.justiceMapCallout = 'true';
    box.style.cssText = 'background:#e9e4d9;border-top:1px solid rgba(19,37,45,.15);border-bottom:1px solid rgba(19,37,45,.15);padding:1rem 0';
    const text = isEs
      ? '<strong>Nuevo mapa de Justicia:</strong> vea en una sola secuencia qué conoció Fiscalía, qué respuesta está documentada, qué quedó abierto y qué ocurrió después — sin convertir cronología en causalidad.'
      : '<strong>New Justice Map:</strong> see in one sequence what the prosecution service knew, what response is documented, what remained open and what happened next — without converting chronology into causation.';
    box.innerHTML = `<div class="shell"><p style="margin:0">${text} <a href="${target}" style="font-weight:800">${isEs ? 'Abrir mapa →' : 'Open map →'}</a></p></div>`;
    main.insertBefore(box, main.firstChild);
  }
})();

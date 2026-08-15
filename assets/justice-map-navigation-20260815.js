(() => {
  const path = location.pathname;
  const isEs = path.includes('/es/');
  const isJustice = path.includes('/justicia-registro-institucional/') || path.includes('/justice-institutional-record/');
  const target = isEs ? '/por-derecho/es/justicia-registro-institucional/' : '/por-derecho/en/justice-institutional-record/';
  const openMessage = isEs ? '/por-derecho/es/carta-abierta-ministerio-fiscal/' : '/por-derecho/en/open-letter-public-prosecution-service/';
  const label = isEs ? 'Mapa de Justicia' : 'Justice Map';

  // Institutional mark routing: the Ministerio Fiscal mark is an identifier, not an endorsement.
  // One click opens the neutral Justice/MF hub; the open message is featured there as a separate editorial layer.
  document.querySelectorAll('a.identity-logo-card').forEach(card => {
    const img = card.querySelector('img[src*="ministerio-fiscal.png"]');
    if (!img) return;
    card.href = target;
    card.setAttribute('aria-label', isEs
      ? 'Abrir el centro de Justicia y Ministerio Fiscal'
      : 'Open the Justice and Public Prosecution Service hub');
    card.dataset.mfHubLink = 'true';
    const copy = card.querySelector('.identity-logo-copy small');
    if (copy) copy.textContent = isEs
      ? 'Mapa, expedientes, respuestas documentadas y mensaje abierto'
      : 'Map, proceedings, documented responses and open message';
  });

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

  // Justice/MF hub: make the evidence-first open message impossible to miss without turning the mark itself into advocacy.
  if (isJustice && !document.querySelector('[data-mf-open-message-feature]')) {
    const heroShell = document.querySelector('.jm-hero .shell');
    if (heroShell) {
      const feature = document.createElement('aside');
      feature.dataset.mfOpenMessageFeature = 'true';
      feature.setAttribute('aria-label', isEs ? 'Mensaje abierto al Ministerio Fiscal' : 'Open message to the Public Prosecution Service');
      feature.style.cssText = 'margin-top:1.35rem;background:#fff;color:#13252d;border-radius:16px;padding:1.15rem 1.25rem;max-width:72rem;box-shadow:0 8px 24px rgba(0,0,0,.12);border-left:5px solid #c89432';
      feature.innerHTML = isEs
        ? '<div style="font-size:.75rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#8f2d27">Mensaje abierto · lectura en 60 segundos</div><h2 style="font-size:clamp(1.35rem,3vw,2rem);line-height:1.1;margin:.35rem 0 .55rem;color:#13252d">¿Cuando se invirtieron las acusaciones, se invirtió también el escrutinio?</h2><p style="margin:.2rem 0 .8rem;max-width:65rem">La reconstrucción 2013–2026 distingue hechos documentados, decisiones, remisiones, lagunas y preguntas abiertas. No pide aceptar una acusación: pide comprobar si la prueba posterior recibió una reconsideración acumulativa y verificable.</p><p style="margin:0"><a href="' + openMessage + '" style="font-weight:900">Abrir el mensaje y la visualización →</a></p>'
        : '<div style="font-size:.75rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#8f2d27">Open message · 60-second read</div><h2 style="font-size:clamp(1.35rem,3vw,2rem);line-height:1.1;margin:.35rem 0 .55rem;color:#13252d">When the allegations reversed, did the scrutiny reverse too?</h2><p style="margin:.2rem 0 .8rem;max-width:65rem">The 2013–2026 reconstruction separates documented facts, decisions, referrals, evidence gaps and open questions. It does not ask readers to accept an accusation; it asks whether later evidence received cumulative, verifiable reconsideration.</p><p style="margin:0"><a href="' + openMessage + '" style="font-weight:900">Open the message and visualisation →</a></p>';
      heroShell.appendChild(feature);
    }
  }

  const isInstitutional = path.includes('/registros-institucionales/') || path.includes('/institutional-records/');
  if (isInstitutional && !document.querySelector('[data-justice-map-callout]')) {
    const main = document.querySelector('main');
    if (!main) return;
    const box = document.createElement('section');
    box.dataset.justiceMapCallout = 'true';
    box.style.cssText = 'background:#e9e4d9;border-top:1px solid rgba(19,37,45,.15);border-bottom:1px solid rgba(19,37,45,.15);padding:1rem 0';
    const text = isEs
      ? '<strong>Centro Justicia + Ministerio Fiscal:</strong> vea la secuencia completa de conocimiento, respuesta, remisiones y preguntas abiertas; el mensaje abierto está destacado al entrar.'
      : '<strong>Justice + Public Prosecution hub:</strong> see the full sequence of knowledge, response, referrals and open questions; the open message is featured on entry.';
    box.innerHTML = `<div class="shell"><p style="margin:0">${text} <a href="${target}" style="font-weight:800">${isEs ? 'Abrir centro →' : 'Open hub →'}</a> · <a href="${openMessage}" style="font-weight:800">${isEs ? 'Mensaje abierto →' : 'Open message →'}</a></p></div>`;
    main.insertBefore(box, main.firstChild);
  }
})();

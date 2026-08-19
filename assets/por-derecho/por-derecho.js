(() => {
  const navToggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');
  if (navToggle && nav) {
    navToggle.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(open));
    });
  }

  const path = window.location.pathname.replace(/\/+$/, '/');
  const isSpanish = /\/es\//.test(path);
  const siteBase = path.startsWith('/por-derecho/') ? '/por-derecho/' : '/';
  const labHref = isSpanish
    ? `${siteBase}es/por-derecho/laboratorio-de-casos/`
    : `${siteBase}en/por-derecho/case-lab/`;

  if (nav && !nav.querySelector('[data-case-lab-link]')) {
    const link = document.createElement('a');
    link.href = labHref;
    link.dataset.caseLabLink = '';
    link.textContent = isSpanish ? 'Laboratorio' : 'Case Lab';
    if (/laboratorio-de-casos|case-lab/.test(path)) link.setAttribute('aria-current', 'page');
    const formation = Array.from(nav.querySelectorAll('a')).find((item) =>
      /#formacion|#education/.test(item.getAttribute('href') || '')
    );
    nav.insertBefore(link, formation || nav.querySelector('.pd-language') || null);
  }

  const isLanding = /\/(es|en)\/por-derecho\/$/.test(path);
  if (isLanding && !document.getElementById('case-lab-gateway')) {
    const target = document.getElementById(isSpanish ? 'formacion' : 'education');
    if (target) {
      const section = document.createElement('section');
      section.className = 'pd-section alt';
      section.id = 'case-lab-gateway';
      section.innerHTML = isSpanish
        ? `<div class="pd-shell pd-split"><div><p class="pd-kicker">Laboratorio de casos · simulación íntegramente ficticia</p><h2 class="pd-section-title">Caso Prisma: ver la metodología trabajar sobre un expediente completo</h2><p class="pd-lead">Una simulación profesional de 10–15 minutos con doce unidades, varios perímetros jurídicos, documentos bloqueados por fecha, cuatro perspectivas profesionales y resultados que pueden confirmar, reestructurar o despejar una preocupación.</p><div class="pd-actions"><a class="pd-button" href="${labHref}">Entrar en el Laboratorio →</a><a class="pd-button secondary" href="como-funciona/">Abrir el demostrador rápido</a></div></div><aside class="pd-legal-boundary"><h3>Frontera expresa</h3><p>Parque Prisma es un escenario compuesto y sintético. No es Sun Park, no anonimiza un asunto real y no predetermina ninguna conclusión sobre el expediente en vivo.</p></aside></div>`
        : `<div class="pd-shell pd-split"><div><p class="pd-kicker">Case Laboratory · wholly fictional simulation</p><h2 class="pd-section-title">Case Prism: watch the methodology work across a complete record</h2><p class="pd-lead">A 10–15 minute professional simulation with twelve units, several legal perimeters, time-locked documents, four professional viewpoints and outcomes that can validate, restructure or clear a concern.</p><div class="pd-actions"><a class="pd-button" href="${labHref}">Enter the Case Lab →</a><a class="pd-button secondary" href="how-it-works/">Open the quick demonstrator</a></div></div><aside class="pd-legal-boundary"><h3>Express boundary</h3><p>Prism Park is a composite synthetic scenario. It is not Sun Park, it does not anonymise a real matter and it predetermines no conclusion about the live record.</p></aside></div>`;
      target.before(section);
    }
  }

  const decisions = document.querySelectorAll('[data-decision]');
  const output = document.querySelector('[data-decision-output]');
  const audit = document.querySelector('[data-audit]');
  decisions.forEach((button) => {
    button.addEventListener('click', () => {
      decisions.forEach((item) => item.setAttribute('aria-pressed', 'false'));
      button.setAttribute('aria-pressed', 'true');
      if (output) {
        output.innerHTML = `<strong>${button.dataset.title}</strong><br>${button.dataset.output}`;
      }
      if (audit) {
        const li = document.createElement('li');
        li.textContent = `${button.dataset.audit}: se conserva la advertencia y la motivación humana.`;
        audit.prepend(li);
      }
    });
  });

  const resolvedToggle = document.querySelector('[data-resolved-toggle]');
  const resolvedPanel = document.querySelector('[data-resolved-panel]');
  if (resolvedToggle && resolvedPanel) {
    resolvedToggle.addEventListener('click', () => {
      const willOpen = resolvedPanel.hasAttribute('hidden');
      resolvedPanel.toggleAttribute('hidden');
      resolvedToggle.setAttribute('aria-expanded', String(willOpen));
      resolvedToggle.textContent = willOpen ? resolvedToggle.dataset.close : resolvedToggle.dataset.open;
    });
  }
})();

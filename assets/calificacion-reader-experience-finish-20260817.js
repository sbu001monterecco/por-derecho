(() => {
  'use strict';

  const route = window.location.pathname.replace(/\/+$/, '') + '/';
  const isEs = route.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const isEn = route.endsWith('/en/insolvency-classification-parallel-lives/');
  if (!isEs && !isEn) return;

  const main = document.querySelector('main');
  if (!main) return;

  let running = false;
  let timer = null;

  const topBlock = (node) => {
    if (!node) return null;
    let el = node;
    while (el.parentElement && el.parentElement !== main) el = el.parentElement;
    return el.parentElement === main ? el : null;
  };

  const block = (selector) => topBlock(document.querySelector(selector));

  const byHeading = (...terms) => {
    const needles = terms.map((term) => term.toLowerCase());
    return [...main.children].find((child) => {
      if (!child.matches('section,details')) return false;
      const text = (child.querySelector('h2')?.textContent || '').toLowerCase();
      return needles.some((needle) => text.includes(needle));
    }) || null;
  };

  const moveAfter = (anchor, node) => {
    if (!anchor || !node || anchor === node) return anchor;
    anchor.insertAdjacentElement('afterend', node);
    return node;
  };

  const fold = (section, id, label) => {
    if (!section) return null;
    const existing = document.getElementById(id);
    if (existing) return existing;
    const details = document.createElement('details');
    details.id = id;
    details.className = 'cal-ux-audit cal-ux-supplement';
    details.innerHTML = `<summary><span class="cal-ux-code">+</span><strong>${label}</strong><span class="cal-ux-pill">${isEs ? 'MATERIAL COMPLETO' : 'FULL MATERIAL'}</span></summary>`;
    section.parentNode.insertBefore(details, section);
    details.appendChild(section);
    return details;
  };

  const revealHash = () => {
    if (!window.location.hash) return;
    let target = null;
    try { target = document.querySelector(window.location.hash); } catch (_) { return; }
    if (!target) return;
    const details = target.matches('details') ? target : target.closest('details');
    if (details) details.open = true;
  };

  const apply = () => {
    if (running) return;
    running = true;
    try {
      const gateway = block('#calificacion-reader-gateway');
      if (!gateway) return;

      const legal = block('.explain');
      const statusRule = byHeading(
        isEs ? 'Una sentencia adversa no debe ocultarse' : 'An adverse judgment must not be hidden',
        isEs ? 'Una sentencia adversa' : 'An adverse first-instance judgment'
      );
      if (legal && statusRule) moveAfter(legal, statusRule);

      const evidence = block('#evidence-before-actor');
      const method = byHeading(
        isEs ? '“Mintieron sobre lo que hice' : '“They lied about what I did',
        isEs ? 'Cómo comprueba Por Derecho esa alegación' : 'How Por Derecho tests that allegation'
      );
      if (evidence && method) evidence.parentNode.insertBefore(method, evidence);

      const counter = block('[data-cal-counter-record-20260816]') || block('[data-cal-recovery-adversity-20260816]');
      const staticRescue = block('#rescue');
      const rescueFold = fold(
        staticRescue,
        'additional-recovery-chronology',
        isEs ? 'Cronología adicional de preservación, explotación y salida · 2012–2026' : 'Additional preservation, operation and exit chronology · 2012–2026'
      );
      if (counter && rescueFold) moveAfter(counter, rescueFold);

      const actors = block('#actors');
      const motive = byHeading(
        isEs ? 'Móvil: lo que los documentos permiten investigar' : 'Motive: what the documents permit',
        isEs ? 'Móvil:' : 'Motive:'
      );
      if (actors && motive) moveAfter(actors, motive);

      const context = block('#calificacion-wider-context');
      const contextBody = context?.querySelector('.cal-ux-context-body');
      const duplicateDecision = byHeading(
        isEs ? 'Qué hace —y qué no hace— la Sentencia 163/2023' : 'What Judgment 163/2023 does—and does not do',
        isEs ? 'Qué hace' : 'What Judgment 163/2023 does'
      );
      if (contextBody && duplicateDecision && !contextBody.contains(duplicateDecision)) contextBody.prepend(duplicateDecision);

      const questions = byHeading(
        isEs ? 'Preguntas finitas antes de elevar más las conclusiones' : 'Finite questions before any stronger conclusion',
        isEs ? 'Preguntas finitas' : 'Finite questions'
      );
      const docbox = block('.docbox');
      const corrections = block('#what-would-change-our-view');
      if (corrections) {
        if (questions) corrections.parentNode.insertBefore(questions, corrections);
        if (docbox) corrections.parentNode.insertBefore(docbox, corrections);
      }

      const finalRule = byHeading(
        isEs ? 'La regla de esta página' : 'The rule of this page',
        isEs ? 'La regla' : 'The rule'
      );
      if (corrections && finalRule) moveAfter(corrections, finalRule);
      if (finalRule && context) moveAfter(finalRule, context);

      revealHash();
      document.body.dataset.calificacionReaderExperienceFinish = '20260817a';
    } finally {
      running = false;
    }
  };

  const schedule = () => {
    window.clearTimeout(timer);
    timer = window.setTimeout(apply, 80);
  };

  const observer = new MutationObserver(schedule);
  observer.observe(main, { childList: true, subtree: false });

  document.addEventListener('click', (event) => {
    const link = event.target.closest?.('a[href^="#"]');
    if (!link) return;
    let target = null;
    try { target = document.querySelector(link.getAttribute('href')); } catch (_) { return; }
    const details = target?.matches('details') ? target : target?.closest('details');
    if (details) details.open = true;
  });
  window.addEventListener('hashchange', revealHash);

  apply();
  window.addEventListener('load', () => {
    apply();
    window.setTimeout(apply, 450);
    window.setTimeout(apply, 1800);
    window.setTimeout(apply, 6500);
    window.setTimeout(() => observer.disconnect(), 9000);
  }, { once: true });
})();

/* MASTER MYND only: preserve the approved reading order without hiding any context. */
(() => {
  'use strict';
  const path = location.pathname.replace(/\/+$/, '/') ;
  const lists = {
    '/por-derecho/en/acosta-matos-family/': ['master-mynd-record', 'family-source-continuity'],
    '/por-derecho/es/acosta-matos-familia/': ['master-mynd', 'arquitectura-engaños', 'alegacion', 'dos-atribuciones', 'arquitecto', 'fotografia-planos', 'llamada-2018', 'cronologia', 'respuesta-2025', 'familia-responsabilidad', 'gobierno-societario', 'origen-intervencion', 'metodologia', 'pregunta-unitaria', 'fuentes']
  };
  const ids = lists[path];
  if (!ids) return;
  const main = document.querySelector('main');
  if (!main) return;
  const approved = ids.map(id => document.getElementById(id));
  if (approved.some(node => !node || node.parentElement !== main)) {
    console.error('MASTER MYND reading-order contract: an approved source section is missing or displaced.');
    return;
  }
  const observer = new MutationObserver(reconcile);
  function reconcile() {
    const current = Array.from(main.children);
    const contextual = current.filter(node => !approved.includes(node));
    const expected = approved.concat(contextual);
    if (expected.every((node, index) => node === current[index])) return;
    observer.disconnect();
    // Moving the existing nodes preserves their text, IDs, links and event handlers.
    // No source node or inherited contextual section is removed, hidden or rewritten.
    expected.forEach(node => main.appendChild(node));
    observer.observe(main, {childList: true});
  }
  reconcile();
  observer.observe(main, {childList: true});
})();

(() => {
  const filters = Array.from(document.querySelectorAll('[data-collab-filter]'));
  const calls = Array.from(document.querySelectorAll('[data-collab-track]'));
  if (!filters.length || !calls.length) return;

  filters.forEach((button) => {
    button.addEventListener('click', () => {
      const selected = button.dataset.collabFilter;
      filters.forEach((item) => item.setAttribute('aria-pressed', item === button ? 'true' : 'false'));
      calls.forEach((call) => {
        call.hidden = selected !== 'all' && call.dataset.collabTrack !== selected;
      });
    });
  });
})();

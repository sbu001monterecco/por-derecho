(() => {
  'use strict';

  const VERSION = '20260824a';
  // Public-edge source marker: data.acDfaVisibilityStability
  let scheduled = false;

  const removePanel = panel => {
    const section = panel.closest('section');
    if (section && section.querySelectorAll('[data-ac-dfa-allegation-visibility], [data-ac-dfa-route-relevance]').length === 1) {
      section.remove();
    } else {
      panel.remove();
    }
  };

  const keepOne = (selector, preserve) => {
    const panels = Array.from(document.querySelectorAll(selector));
    if (!panels.length) return;
    const retained = panels[0];
    preserve(retained);
    panels.slice(1).forEach(removePanel);
  };

  const stabilise = () => {
    scheduled = false;
    keepOne('[data-ac-dfa-allegation-visibility]', panel => {
      panel.dataset.acDfaUpdate = '20260824';
      panel.dataset.acDfaCanonicalStatus = '20260824';
      panel.dataset.acDfaVisibilityStable = VERSION;
    });
    keepOne('[data-ac-dfa-route-relevance]', panel => {
      panel.dataset.acDfaCrosslink = '20260824';
      panel.dataset.acDfaVisibilityStable = VERSION;
    });
    document.documentElement.dataset.acDfaVisibilityStability = VERSION;
  };

  const schedule = () => {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(stabilise);
  };

  const start = () => {
    stabilise();
    const observer = new MutationObserver(schedule);
    observer.observe(document.body, { childList: true, subtree: true });
    [250, 650, 1250, 1950, 2600].forEach(delay => window.setTimeout(stabilise, delay));
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
})();

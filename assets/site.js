(() => {
  const current = document.currentScript;
  if (!current) return;

  const loadTreasuryVisual = () => {
    if (document.querySelector('script[data-treasury-154-hq-loader]')) return;
    const visual = document.createElement('script');
    visual.src = new URL('treasury-154-hq-visual-20260828.js?v=20260828c', current.src).href;
    visual.async = false;
    visual.setAttribute('data-treasury-154-hq-loader', '20260828');
    document.head.appendChild(visual);
  };

  // Preserve the complete site loader that existed before this visual update.
  const prior = document.createElement('script');
  prior.src = new URL('site-pre-treasury-154-hq-20260828.js?v=20260828a', current.src).href;
  prior.async = false;
  prior.setAttribute('data-pre-treasury-154-site-loader', '20260828');
  prior.addEventListener('load', loadTreasuryVisual, { once: true });
  prior.addEventListener('error', loadTreasuryVisual, { once: true });
  document.head.appendChild(prior);
})();

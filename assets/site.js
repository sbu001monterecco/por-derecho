(() => {
  const current = document.currentScript;
  if (!current) return;

  // Preserve and execute the complete current-main site loader unchanged.
  const prior = document.createElement('script');
  prior.src = new URL('site-pre-fiscalia-eg95-20260823.js?v=20260823a', current.src).href;
  prior.async = false;
  prior.setAttribute('data-pre-fiscalia-eg95-site-loader', '20260823');
  document.head.appendChild(prior);

  // Propagate the source-controlled EG 95/2026 procedural update.
  const eg95 = document.createElement('script');
  eg95.src = new URL('fiscalia-eg95-propagation-20260823.js?v=20260823a', current.src).href;
  eg95.async = false;
  eg95.setAttribute('data-fiscalia-eg95-propagation-loader', '20260823');
  document.head.appendChild(eg95);
})();

(() => {
  const current = document.currentScript;
  if (!current) return;

  // Preserve and execute the complete pre-highlight site loader unchanged.
  const prior = document.createElement('script');
  prior.src = new URL('site-pre-intervencion-highlight-20260820.js?v=20260820a', current.src).href;
  prior.async = false;
  prior.setAttribute('data-pre-intervencion-site-loader', 'true');
  document.head.appendChild(prior);

  // Highlight the 24-Feb-2026 Integrity Commission consideration and the protected-assets
  // Justice referral recorded by the signed 5-Mar-2026 Intervención General response.
  const protectedAssets = document.createElement('script');
  protectedAssets.src = new URL('intervencion-protected-assets-highlight-20260820.js?v=20260820a', current.src).href;
  protectedAssets.async = false;
  protectedAssets.setAttribute('data-intervencion-protected-assets-loader', 'true');
  document.head.appendChild(protectedAssets);
})();
/* COMPATIBILITY-WRAPPER-20260827: preserve the complete prior loader, then add RICPE/CNMV closure state. */
(() => {
  const current = document.currentScript;
  if (!current) return;
  const base = new URL('.', current.src);

  const prior = document.createElement('script');
  prior.src = new URL('site-pre-intervencion-highlight-original-20260827.js?v=20260827a', base).href;
  prior.async = false;
  prior.setAttribute('data-site-pre-intervencion-original-loader', '20260827');
  document.head.appendChild(prior);

  const closure = document.createElement('script');
  closure.src = new URL('ricpe-cnmv-closure-update-20260827.js?v=20260827a', base).href;
  closure.async = false;
  closure.setAttribute('data-ricpe-cnmv-closure-loader', '20260827');
  document.head.appendChild(closure);
})();

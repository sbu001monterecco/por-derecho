(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;

  const loadPublication = () => {
    const path = location.pathname.replace(/index\.html$/, '').replace(/\/+$/, '/');
    if (path !== '/por-derecho/en/' && path !== '/por-derecho/en/cuatrecasas-sun-park/') return;
    if (document.querySelector('script[data-cuatrecasas-edgeworth-publication-loader]')) return;
    const script = document.createElement('script');
    script.src = new URL('cuatrecasas-edgeworth-linkedin-20260916.js?v=20260916a', current.src).href;
    script.async = false;
    script.setAttribute('data-cuatrecasas-edgeworth-publication-loader', '20260916a');
    document.head.appendChild(script);
  };

  const preserved = document.createElement('script');
  preserved.src = new URL('site-pre-cuatrecasas-edgeworth-20260916.js?v=20260916a', current.src).href;
  preserved.async = false;
  preserved.setAttribute('data-pre-cuatrecasas-edgeworth-site-loader', '20260916a');
  preserved.addEventListener('load', loadPublication, { once: true });
  preserved.addEventListener('error', loadPublication, { once: true });
  document.head.appendChild(preserved);
})();

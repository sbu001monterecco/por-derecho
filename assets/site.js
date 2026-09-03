(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;

  const loadMatkator8584Release = () => {
    if (!document.querySelector('script[data-matkator-8584-multitrack-loader]')) {
      const module = document.createElement('script');
      module.src = new URL('matkator-8584-hotel-title-multitrack-20260903.js?v=20260903a', current.src).href;
      module.async = false;
      module.setAttribute('data-matkator-8584-multitrack-loader','20260903a');
      document.head.appendChild(module);
    }
    if (!document.querySelector('script[data-matkator-8584-search-loader]')) {
      const search = document.createElement('script');
      search.src = new URL('matkator-8584-search-extension-20260903.js?v=20260903a', current.src).href;
      search.async = false;
      search.setAttribute('data-matkator-8584-search-loader','20260903a');
      document.head.appendChild(search);
    }
  };

  const legacy = document.createElement('script');
  legacy.src = new URL('site-pre-matkator-8584-20260903.js?v=20260903a', current.src).href;
  legacy.async = false;
  legacy.setAttribute('data-pre-matkator-8584-site-loader','20260903a');
  legacy.addEventListener('load', loadMatkator8584Release, {once:true});
  legacy.addEventListener('error', loadMatkator8584Release, {once:true});
  document.head.appendChild(legacy);
})();

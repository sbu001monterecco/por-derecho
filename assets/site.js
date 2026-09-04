(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;

  const load = (file, marker, version) => {
    if (document.querySelector(`script[${marker}]`)) return;
    const script = document.createElement('script');
    script.src = new URL(`${file}?v=${version}`, current.src).href;
    script.async = false;
    script.setAttribute(marker, version);
    document.head.appendChild(script);
  };

  const loadControl2224Release = () => {
    load('control-22-24-interlink-20260904.js', 'data-control-22-24-interlink-loader', '20260904a');
    load('control-22-24-search-extension-20260904.js', 'data-control-22-24-search-loader', '20260904a');
  };

  const loadHotelFincaSystem = () => {
    load('hotel-finca-title-system-interlink-20260903.js', 'data-hotel-finca-system-interlink-loader', '20260903a');
    load('hotel-finca-title-system-search-extension-20260903.js', 'data-hotel-finca-system-search-loader', '20260903a');
  };

  const loadMatkator8584Release = () => {
    load('matkator-8584-hotel-title-multitrack-20260903.js', 'data-matkator-8584-multitrack-loader', '20260903a');
    load('matkator-8584-search-extension-20260903.js', 'data-matkator-8584-search-loader', '20260903a');
    loadHotelFincaSystem();
    loadControl2224Release();
  };

  const legacy = document.createElement('script');
  legacy.src = new URL('site-pre-matkator-8584-20260903.js?v=20260903a', current.src).href;
  legacy.async = false;
  legacy.setAttribute('data-pre-matkator-8584-site-loader','20260903a');
  legacy.addEventListener('load', loadMatkator8584Release, {once:true});
  legacy.addEventListener('error', loadMatkator8584Release, {once:true});
  document.head.appendChild(legacy);
})();

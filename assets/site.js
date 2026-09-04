(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;

  /*
   * Compatibility marker for the inherited loader chain.
   * site-pre-matkator-8584-20260903.js transitively executes the preserved
   * site-pre-treasury-154-hq-20260828.js?v=20260828a release; do not load it
   * a second time here because that would duplicate inherited runtime modules.
   */

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
    load('three-track-page-enhancement-20260904.js', 'data-three-track-page-enhancement-loader', '20260904b');
    load('unitary-criminal-source-register-search-extension-20260904.js', 'data-unitary-criminal-source-register-search-loader', '20260904a');
    load('home-mission-critical-20260904.js', 'data-home-mission-critical-loader', '20260904a');
    load('caixabank-valencia-concurso-cam-linkage-20260904.js', 'data-caixabank-valencia-concurso-cam-linkage-loader', '20260904a');
    load('caixabank-valencia-lawyer-dataroom-unitary-20260904.js', 'data-caixabank-valencia-lawyer-dataroom-unitary-loader', '20260904a');
    load('caixabank-valencia-lawyer-dataroom-deeplinks-20260904.js', 'data-caixabank-valencia-lawyer-dataroom-deeplinks-loader', '20260904a');
    load('caixabank-valencia-unitary-inbound-interlinks-20260904.js', 'data-caixabank-valencia-unitary-inbound-interlinks-loader', '20260904a');
    load('caixabank-valencia-full-source-pdfs-20260904.js', 'data-caixabank-valencia-full-source-pdfs-loader', '20260904b');
    load('caixabank-borja-witness-claimant-clarification-20260904.js', 'data-borja-witness-claimant-clarification-loader', '20260904a');
    load('ricpe-cam-conflict-substance-claimant-statement-20260904.js', 'data-ricpe-cam-conflict-substance-statement-loader', '20260904a');
    load('uria-ricpe-caixabank-source-register-20260904.js', 'data-uria-ricpe-caixabank-source-register-loader', '20260904a');
    load('uria-haya-puzzle-integration-20260904.js', 'data-uria-haya-puzzle-integration-loader', '20260904b');
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

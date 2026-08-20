(() => {
  const current = document.currentScript;
  if (!current) return;
  const load = (file, marker) => {
    const script = document.createElement('script');
    script.src = new URL(file, current.src).href;
    script.async = false;
    if (marker) script.setAttribute(marker, 'true');
    document.head.appendChild(script);
  };
  load('site-base-20260819.js?v=20260819a');
  load('case-information-architecture-20260819.js?v=20260819b', 'data-case-information-architecture-loader');
  load('unitary-criminal-reverse-engineering-20260820.js?v=20260820a', 'data-unitary-criminal-loader');
  load('san-telmo-attribution-correction-20260819.js?v=20260819a', 'data-san-telmo-attribution-loader');
  load('adjudicacion-provenance-cross-site-20260819.js?v=20260820a', 'data-adjudicacion-provenance-loader');
  load('ac-community-de-facto-administration-20260820.js?v=20260820b', 'data-ac-community-de-facto-loader');
  load('ac-de-facto-knowing-facilitation-visibility-20260820.js?v=20260820b', 'data-ac-de-facto-knowing-facilitation-visibility-loader');
  load('ac-de-facto-knowing-facilitation-stability-20260820.js?v=20260820b', 'data-ac-de-facto-knowing-facilitation-stability-loader');
  load('cnmv-regage-status-cross-site-20260820.js?v=20260820a', 'data-cnmv-regage-status-loader');
  load('jdam-architecture-colegios-20260820.js?v=20260820a', 'data-jdam-architecture-colegios-loader');
  load('palacete-visuals-20260820.js?v=20260820a', 'data-palacete-visuals-loader');
})();
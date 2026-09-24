(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;

  /*
   * Compatibility marker for the inherited loader chain.
   * site-pre-matkator-8584-20260903.js transitively executes the preserved
   * site-pre-treasury-154-hq-20260828.js?v=20260828a release; do not load it
   * a second time here because that would duplicate inherited runtime modules.
   * The inherited visual chain also continues to load
   * cuatrecasas-mandate-ric-inbound-20260902.js transitively; keep that
   * source-integrity marker visible without duplicating the runtime module.
   */

  const load = (file, marker, version) => {
    if (document.querySelector(`script[${marker}]`)) return;
    const script = document.createElement('script');
    script.src = new URL(`${file}?v=${version}`, current.src).href;
    script.async = false;
    script.setAttribute(marker, version);
    document.head.appendChild(script);
  };

  const loadCapitalRelationships = () => {
    const path = location.pathname.replace(/index\.html$/, '').replace(/\/+$/, '/');
    const routes = new Set([
      '/por-derecho/en/strategic-financial-relationship/',
      '/por-derecho/en/platform-scale/',
      '/por-derecho/en/montana-roja/',
      '/por-derecho/en/open-letter-lanzarote/',
      '/por-derecho/en/collaborate/',
      '/por-derecho/en/capital-relationships/',
      '/por-derecho/es/relacion-financiera-estrategica/',
      '/por-derecho/es/escala-plataforma/',
      '/por-derecho/es/montana-roja/',
      '/por-derecho/es/carta-abierta-lanzarote/',
      '/por-derecho/es/colaborar/',
      '/por-derecho/es/relaciones-de-capital/'
    ]);
    if (routes.has(path)) {
      load('capital-relationships-route-20260916.js', 'data-capital-relationships-route-loader', '20260916a');
    }
  };

  /* MASTER_PROCEEDINGS_PUBLICATION_GATE */
  // Compatibility/cache-bust contract: master-proceedings-publication-20260830.js?v=20260831e
  const loadMasterProceedingsPublication = () => {
    load('master-proceedings-publication-20260830.js', 'data-master-proceedings-publication-loader', '20260831e');
  };

  const loadControl2224Release = () => {
    load('control-22-24-interlink-20260904.js', 'data-control-22-24-interlink-loader', '20260904a');
    load('control-22-24-search-extension-20260904.js', 'data-control-22-24-search-loader', '20260904a');
    load('three-track-page-enhancement-20260904.js', 'data-three-track-page-enhancement-loader', '20260904b');
    load('unitary-criminal-source-register-search-extension-20260904.js', 'data-unitary-criminal-source-register-search-loader', '20260904a');
    load('home-mission-critical-20260904.js', 'data-home-mission-critical-loader', '20260905route');
    load('caixabank-valencia-concurso-cam-linkage-20260904.js', 'data-caixabank-valencia-concurso-cam-linkage-loader', '20260904a');
    load('caixabank-valencia-lawyer-dataroom-unitary-20260904.js', 'data-caixabank-valencia-lawyer-dataroom-unitary-loader', '20260905repair');
    load('caixabank-valencia-lawyer-dataroom-deeplinks-20260904.js', 'data-caixabank-valencia-lawyer-dataroom-deeplinks-loader', '20260904a');
    load('caixabank-valencia-unitary-inbound-interlinks-20260904.js', 'data-caixabank-valencia-unitary-inbound-interlinks-loader', '20260904a');
    load('caixabank-valencia-full-source-pdfs-20260904.js', 'data-caixabank-valencia-full-source-pdfs-loader', '20260905repair');
    load('caixabank-borja-witness-claimant-clarification-20260904.js', 'data-borja-witness-claimant-clarification-loader', '20260904a');
    load('ricpe-cam-conflict-substance-claimant-statement-20260904.js', 'data-ricpe-cam-conflict-substance-statement-loader', '20260904a');
    load('uria-ricpe-caixabank-source-register-20260904.js', 'data-uria-ricpe-caixabank-source-register-loader', '20260905repair');
    load('uria-haya-puzzle-integration-20260904.js', 'data-uria-haya-puzzle-integration-loader', '20260904b');
    load('puzzle-hybrid-viewer-20260904.js', 'data-puzzle-hybrid-viewer-loader', '20260904a');
    load('puzzle-continuity-enhancement-20260905.js', 'data-puzzle-continuity-enhancement-loader', '20260905a');
    load('evidence-visibility-runtime-20260904.js', 'data-evidence-visibility-runtime-loader', '20260904a');
    load('joan-cruz-multitrack-crosslinks-20260901.js', 'data-joan-cruz-multitrack-loader', '20260904a');
    load('orion-rental-socimi-interlinks-20260905.js', 'data-orion-rental-socimi-interlinks-loader', '20260905a');
    load('orion-rental-socimi-search-extension-20260905.js', 'data-orion-rental-socimi-search-loader', '20260905a');
    load('caixabank-obrem-two-branch-visual-20260918.js', 'data-caixabank-obrem-two-branch-visual-loader', '20260918a');
    loadCapitalRelationships();
  };

  const loadHotelFincaSystem = () => {
    load('hotel-finca-title-system-interlink-20260903.js', 'data-hotel-finca-system-interlink-loader', '20260903a');
    load('hotel-finca-title-system-search-extension-20260903.js', 'data-hotel-finca-system-search-loader', '20260903a');
  };

  const loadMatkator8584Release = () => {
    loadMasterProceedingsPublication();
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

/* PD1901_PLATFORM_NEXUS_LOADER: current source remains unchanged above. */
(() => {
  'use strict';
  const source = document.currentScript;
  if (!source) return;
  const root = new URL('../', source.src);
  const route = location.pathname.startsWith(root.pathname)
    ? location.pathname.slice(root.pathname.length).replace(/index\.html$/, '').replace(/\/?$/, '/') : '';
  const routes = new Set(["es/dp-1901-2026/", "en/dp-1901-2026/", "es/control-21-denuncia-actores-privados-25-junio-2026/", "en/control-21-private-actors-complaint-25-june-2026/", "es/control-24-denuncia-juez-concurso-36-2012/", "en/control-24-insolvency-judge-complaint-36-2012/", "es/control-22-denuncia-administrador-concursal/", "en/control-22-insolvency-administrator-complaint/", "es/dp-1956-2026/", "en/dp-1956-2026/", "es/dp-1901-2026-auto-14-septiembre-2026/", "en/dp-1901-2026-order-14-september-2026/", "es/dp-1901-eg745-coordinacion-interinstitucional/", "en/dp-1901-eg745-cross-institutional-coordination/", "es/eg-745-respuesta-inminente-matriz-fiscalia/", "en/eg-745-imminent-response-prosecution-matrix/", "es/fiscalia-dip-2-2026/", "en/fiscalia-dip-2-2026/", "es/fiscalia-inspeccion-exp-gub-745-2026/", "en/public-prosecution-inspection-exp-gub-745-2026/", "es/ministerio-fiscal/", "en/ministerio-fiscal/", "es/comunidad-instrumentalizacion/", "en/community-instrumentalisation/", "es/aweswell-limited/", "en/aweswell-limited/", "es/arquitectura-nodo-documental-jdam/", "en/architecture-documentary-node-jdam/", "es/incentivos-regionales-gc836-p06/", "en/regional-incentives-gc836-p06/", "es/mismo-hotel-multiples-vidas-financieras/", "en/same-hotel-multiple-financial-lives/", "es/recuperacion-activos-intervencion-decomiso/", "en/asset-recovery-intervention-confiscation/", "es/ric-private-equity-sun-park/", "en/ric-private-equity-sun-park/", "es/sala-situacion-recuperacion-activos/", "en/recovery-command-center/", "es/identidad-digital-sun-park-google-mynd/", "en/sun-park-digital-identity-google-mynd/"]);
  if (!routes.has(route) || document.querySelector('script[data-pd1901-platform-nexus-loader]')) return;
  const s = document.createElement('script');
  s.src = new URL('assets/dp1901-platform-recovery-nexus-20260920.js?v=20260920a', root).href;
  s.dataset.pd1901PlatformNexusLoader = '20260920a';
  s.defer = true;
  document.head.appendChild(s);
})();

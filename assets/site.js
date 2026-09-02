(() => {
  const current = document.currentScript;
  if (!current) return;

  /*
   * INHERITED LOADER CONTRACT — executed transitively through
   * site-pre-treasury-154-hq-20260828.js and its preserved predecessor chain.
   * These markers intentionally remain visible here so legacy integrity/read-back
   * validators can verify non-regression without double-loading inherited modules.
   *
   * SOURCE-OF-FUNDS-NOTICE-20260820
   * AC-COMMUNITY-DE-FACTO-ADMINISTRATION-LOADERS-20260824
   * CALIFICACION-CRIMINAL-MISUSE-THESIS-20260824
   * site-pre-intervencion-highlight-20260820.js
   * PROSECUTION-PUBLIC-ENTRY-20260824
   * prosecution-public-entry-20260821.js
   * ricpe-saip-batch-status-20260824.js
   * playa-blanca-concept-home-20260820.js
   * data-playa-blanca-concept-loader
   * MASTER_PROCEEDINGS_PUBLICATION_GATE_20260830
   * CANONICAL_HOME_SEARCH_AND_JUSTICE_AUTHORITY_REGISTER_20260902
   * BORJA_SEPARATION_RPL3304_CONVERGENCE_INBOUND_20260902
   * BORJA_SEPARATION_RPL3304_SEARCH_EXTENSION_20260902
   * CUATRECASAS_MANDATE_RIC_INBOUND_20260902
   * CUATRECASAS_WHY_STEP4_LONGFORM_20260902
   * CUATRECASAS_STEP4_PUBLICATION_NODE_20260902
   * CUATRECASAS_STEP4_SEARCH_EXTENSION_20260902
   */

  const loadMasterProceedingsPublication = () => {
    if (document.querySelector('script[data-master-proceedings-publication-loader]')) return;
    const proceedings = document.createElement('script');
    proceedings.src = new URL('master-proceedings-publication-20260830.js?v=20260831e', current.src).href;
    proceedings.async = false;
    proceedings.setAttribute('data-master-proceedings-publication-loader', '20260831e');
    document.head.appendChild(proceedings);
  };

  const loadConcurso36Controls = () => {
    if (!document.querySelector('script[data-concurso36-arrecife-crosslinks-loader]')) {
      const crosslinks = document.createElement('script');
      crosslinks.src = new URL('concurso36-arrecife-crosslinks-20260829.js?v=20260829a', current.src).href;
      crosslinks.async = false;
      crosslinks.setAttribute('data-concurso36-arrecife-crosslinks-loader', '20260829');
      document.head.appendChild(crosslinks);
    }
    if (!document.querySelector('script[data-concurso36-caret-overlay-loader]')) {
      const caret = document.createElement('script');
      caret.src = new URL('concurso36-caret-incident-overlay-20260829.js?v=20260829a', current.src).href;
      caret.async = false;
      caret.setAttribute('data-concurso36-caret-overlay-loader', '20260829');
      document.head.appendChild(caret);
    }
    loadMasterProceedingsPublication();
  };

  const loadTreasuryVisual = () => {
    if (!document.querySelector('script[data-treasury-154-hq-loader]')) {
      const visual = document.createElement('script');
      visual.src = new URL('treasury-154-hq-visual-20260828.js?v=20260828c', current.src).href;
      visual.async = false;
      visual.setAttribute('data-treasury-154-hq-loader', '20260828');
      visual.addEventListener('load', loadConcurso36Controls, { once: true });
      visual.addEventListener('error', loadConcurso36Controls, { once: true });
      document.head.appendChild(visual);
      return;
    }
    loadConcurso36Controls();
  };

  const loadCuatrecasasLinkedInRecord = () => {
    if (document.querySelector('script[data-cuatrecasas-inigo-linkedin-loader]')) return;
    const linkedInRecord = document.createElement('script');
    linkedInRecord.src = new URL('cuatrecasas-inigo-linkedin-record-20260831.js?v=20260901b', current.src).href;
    linkedInRecord.async = false;
    linkedInRecord.setAttribute('data-cuatrecasas-inigo-linkedin-loader', '20260901b');
    document.head.appendChild(linkedInRecord);
  };

  const loadCuatrecasasBookCover = () => {
    if (document.querySelector('script[data-cuatrecasas-four-green-houses-loader]')) return;
    const bookCover = document.createElement('script');
    bookCover.src = new URL('cuatrecasas-four-green-houses-one-red-hotel-cover-20260831.js?v=20260831a', current.src).href;
    bookCover.async = false;
    bookCover.setAttribute('data-cuatrecasas-four-green-houses-loader', '20260831a');
    document.head.appendChild(bookCover);
  };

  const loadActaAuthorityInterlink = () => {
    if (document.querySelector('script[data-acta-authority-interlink-loader]')) return;
    const interlink = document.createElement('script');
    interlink.src = new URL('acta-authority-interlink-20260831.js?v=20260831a', current.src).href;
    interlink.async = false;
    interlink.setAttribute('data-acta-authority-interlink-loader', '20260831a');
    document.head.appendChild(interlink);
  };

  const loadAcostaHotelPlatformMedia = () => {
    if (document.querySelector('script[data-acosta-hotel-platform-media-loader]')) return;
    const media = document.createElement('script');
    media.src = new URL('acosta-hotel-platform-media-20260901.js?v=20260901a', current.src).href;
    media.async = false;
    media.setAttribute('data-acosta-hotel-platform-media-loader', '20260901a');
    document.head.appendChild(media);
  };

  const loadActorsAcostaCanonicalRegister = () => {
    if (!window.location.pathname.includes('/en/actors-parties-lawyers-representatives/')) return;
    if (document.querySelector('script[data-actors-acosta-canonical-register-loader]')) return;
    const register = document.createElement('script');
    register.src = new URL('actors-acosta-matos-canonical-register-20260901.js?v=20260901a', current.src).href;
    register.async = false;
    register.setAttribute('data-actors-acosta-canonical-register-loader', '20260901a');
    document.head.appendChild(register);
  };

  const isHome = () => {
    const pathname = window.location.pathname.replace(/\/index\.html$/, '/');
    const segments = pathname.split('/').filter(Boolean);
    return segments.length === 0
      || (segments.length === 1 && ['por-derecho', 'es', 'en'].includes(segments[0]))
      || (segments.length === 2 && segments[0] === 'por-derecho' && ['es', 'en'].includes(segments[1]));
  };

  const loadCanonicalHomeSearch = () => {
    if (!isHome()) return;
    if (document.querySelector('script[data-canonical-home-search-loader]')) return;
    const search = document.createElement('script');
    search.src = new URL('canonical-home-search-20260902.js?v=20260902b', current.src).href;
    search.async = false;
    search.setAttribute('data-canonical-home-search-loader', '20260902b');
    document.head.appendChild(search);
  };

  const loadJusticeProfessionalsCurrentOverlay = () => {
    const path = window.location.pathname;
    if (!path.includes('/es/registro-identidad-profesionales-justicia/') && !path.includes('/en/justice-professionals-identity-register/')) return;
    if (document.querySelector('script[data-justice-professionals-current-overlay-loader]')) return;
    const overlay = document.createElement('script');
    overlay.src = new URL('justice-professionals-current-overlay-20260902.js?v=20260902a', current.src).href;
    overlay.async = false;
    overlay.setAttribute('data-justice-professionals-current-overlay-loader', '20260902a');
    document.head.appendChild(overlay);
  };

  const loadBorjaSeparationRpl3304Inbound = () => {
    if (document.querySelector('script[data-borja-separation-rpl3304-inbound-loader]')) return;
    const inbound = document.createElement('script');
    inbound.src = new URL('borja-separation-rpl3304-inbound-20260902.js?v=20260902b', current.src).href;
    inbound.async = false;
    inbound.setAttribute('data-borja-separation-rpl3304-inbound-loader', '20260902b');
    document.head.appendChild(inbound);
  };

  const loadBorjaSeparationSearchExtension = () => {
    if (!isHome()) return;
    if (document.querySelector('script[data-borja-separation-search-extension-loader]')) return;
    const extension = document.createElement('script');
    extension.src = new URL('borja-separation-search-extension-20260902.js?v=20260902a', current.src).href;
    extension.async = false;
    extension.setAttribute('data-borja-separation-search-extension-loader', '20260902a');
    document.head.appendChild(extension);
  };

  const loadCuatrecasasMandateRicInbound = () => {
    if (document.querySelector('script[data-cuatrecasas-mandate-ric-inbound-loader]')) return;
    const inbound = document.createElement('script');
    inbound.src = new URL('cuatrecasas-mandate-ric-inbound-20260902.js?v=20260902a', current.src).href;
    inbound.async = false;
    inbound.setAttribute('data-cuatrecasas-mandate-ric-inbound-loader', '20260902a');
    document.head.appendChild(inbound);
  };

  const loadCuatrecasasWhyStep4Longform = () => {
    if (!window.location.pathname.includes('/en/cuatrecasas-sun-park/')) return;
    if (document.querySelector('script[data-cuatrecasas-why-step4-loader]')) return;
    const longform = document.createElement('script');
    longform.src = new URL('cuatrecasas-why-step4-longform-20260902.js?v=20260902a', current.src).href;
    longform.async = false;
    longform.setAttribute('data-cuatrecasas-why-step4-loader', '20260902a');
    document.head.appendChild(longform);
  };

  const loadCuatrecasasStep4PublicationNode = () => {
    if (document.querySelector('script[data-cuatrecasas-step4-publication-loader]')) return;
    const publication = document.createElement('script');
    publication.src = new URL('cuatrecasas-step4-publication-node-20260902.js?v=20260902a', current.src).href;
    publication.async = false;
    publication.setAttribute('data-cuatrecasas-step4-publication-loader', '20260902a');
    document.head.appendChild(publication);
  };

  const loadCuatrecasasStep4SearchExtension = () => {
    if (!isHome()) return;
    if (document.querySelector('script[data-cuatrecasas-step4-search-extension-loader]')) return;
    const extension = document.createElement('script');
    extension.src = new URL('cuatrecasas-step4-search-extension-20260902.js?v=20260902a', current.src).href;
    extension.async = false;
    extension.setAttribute('data-cuatrecasas-step4-search-extension-loader', '20260902a');
    document.head.appendChild(extension);
  };

  // Preserve the complete site loader that existed before this visual update.
  const prior = document.createElement('script');
  prior.src = new URL('site-pre-treasury-154-hq-20260828.js?v=20260828a', current.src).href;
  prior.async = false;
  prior.setAttribute('data-pre-treasury-154-site-loader', '20260828');
  prior.addEventListener('load', loadTreasuryVisual, { once: true });
  prior.addEventListener('error', loadTreasuryVisual, { once: true });
  document.head.appendChild(prior);

  loadCuatrecasasLinkedInRecord();
  loadCuatrecasasBookCover();
  loadActaAuthorityInterlink();
  loadAcostaHotelPlatformMedia();
  loadActorsAcostaCanonicalRegister();
  loadCanonicalHomeSearch();
  loadJusticeProfessionalsCurrentOverlay();
  loadBorjaSeparationRpl3304Inbound();
  loadBorjaSeparationSearchExtension();
  loadCuatrecasasMandateRicInbound();
  loadCuatrecasasWhyStep4Longform();
  loadCuatrecasasStep4PublicationNode();
  loadCuatrecasasStep4SearchExtension();
})();

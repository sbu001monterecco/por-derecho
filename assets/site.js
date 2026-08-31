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
   */

  const loadMasterProceedingsPublication = () => {
    if (document.querySelector('script[data-master-proceedings-publication-loader]')) return;
    const proceedings = document.createElement('script');
    proceedings.src = new URL('master-proceedings-publication-20260830.js?v=20260831a', current.src).href;
    proceedings.async = false;
    proceedings.setAttribute('data-master-proceedings-publication-loader', '20260831a');
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
    linkedInRecord.src = new URL('cuatrecasas-inigo-linkedin-record-20260831.js?v=20260831a', current.src).href;
    linkedInRecord.async = false;
    linkedInRecord.setAttribute('data-cuatrecasas-inigo-linkedin-loader', '20260831a');
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

  // Preserve the complete site loader that existed before this visual update.
  const prior = document.createElement('script');
  prior.src = new URL('site-pre-treasury-154-hq-20260828.js?v=20260828a', current.src).href;
  prior.async = false;
  prior.setAttribute('data-pre-treasury-154-site-loader', '20260828');
  prior.addEventListener('load', loadTreasuryVisual, { once: true });
  prior.addEventListener('error', loadTreasuryVisual, { once: true });
  document.head.appendChild(prior);

  // Documentary Cuatrecasas/LinkedIn insert. The asset self-limits to the
  // bilingual Cuatrecasas Sun Park pages and is idempotent on repeated loads.
  loadCuatrecasasLinkedInRecord();

  // Four Green Houses / One Red Hotel visual. The asset self-limits to the
  // bilingual Cuatrecasas Sun Park pages and links to the existing book route.
  loadCuatrecasasBookCover();
})();

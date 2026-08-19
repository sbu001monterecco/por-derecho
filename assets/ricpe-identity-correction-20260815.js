(() => {
  const current = document.currentScript;
  if (!current) return;

  const load = (filename, onload) => {
    const script = document.createElement('script');
    script.src = new URL(filename, current.src).href;
    script.async = false;
    if (onload) script.addEventListener('load', onload, { once: true });
    document.head.appendChild(script);
  };

  // Preserve the established identity/vital-status correction and then add the
  // 2019–2024 RICPE–Acosta Matos relationship reconstruction. The second layer
  // makes explicit that the 11-Nov-2020 webinar is one public node within a
  // wider sequence of meetings, advisers, investors, diligence, risk review,
  // formalisation and monitoring.
  load('ricpe-identity-correction-core-20260815.js?v=20260818a', () => {
    load('ricpe-relationship-network-20260818.js?v=20260818a');
  });

  // Shared actor-family / PwC knowledge visualization.
  // One backend component drives the homepage, canonical PwC page and canonical RICPE page.
  // Canonical relationships: Antonio Cogolludo Rojas is Shaila's father;
  // Francisco Mario Matos Matas and Shaila María Cogolludo Ramos are husband and wife.
  load('homepage-actor-family-pwc-note-20260819.js?v=20260819b');

  // Dominant San Telmo / RICPE same-asset parallel-lives visual.
  // Reused on the homepage actor map, RSM NNR4, RICPE and Insolvency Administrator pages.
  load('san-telmo-parallel-lives-red-20260819.js?v=20260819a');

  // RSM NNR4 chronology/read-back update for the newly recovered 30-Nov-2021 San Telmo/RICPE finding.
  load('rsm-san-telmo-current-update-20260819.js?v=20260819a');
})();
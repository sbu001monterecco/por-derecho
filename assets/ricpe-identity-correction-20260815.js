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
  // 2019–2024 RICPE–Acosta Matos relationship reconstruction.
  load('ricpe-identity-correction-core-20260815.js?v=20260818a', () => {
    load('ricpe-relationship-network-20260818.js?v=20260818a');
  });

  // Shared actor-family / PwC knowledge visualization.
  // Version c carries the source-led 2011/2014 chronology locks for FMMM, Antonio and Shaila.
  load('homepage-actor-family-pwc-note-20260819.js?v=20260819c');

  // Canonical historical lock notice for the full public people / representatives register.
  load('sun-park-canonical-actor-history-lock-20260819.js?v=20260819a');

  // Canonical same-asset / parallel-lives visual. One component serves homepage,
  // RICPE, RSM, San Telmo, Insolvency Administrator, Grant Thornton and principal
  // parallel-lives / accountability / reconstruction pages in EN and ES.
  load('san-telmo-parallel-lives-red-20260819.js?v=20260819b');

  // RSM NNR4 chronology/read-back update for the recovered 30-Nov-2021 San Telmo/RICPE finding.
  load('rsm-san-telmo-current-update-20260819.js?v=20260819a');
})();
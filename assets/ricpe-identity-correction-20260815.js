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

  // Canonical 5 + AC control-chain design: five private actors remain distinct from
  // the court-appointed Insolvency Administrator, with the 7-Jun-2018 control hinge,
  // eight-stage economic chain, judicial-protection boundary and 2016 PwC notice checkpoint.
  load('homepage-actor-family-pwc-note-20260819.js?v=20260824a');

  // Canonical historical lock notice for the full public people / representatives register.
  load('sun-park-canonical-actor-history-lock-20260819.js?v=20260819a');

  // Preserve the established parallel-lives analysis and then place the source-stamped
  // Eduardo → Sun Park → Borja visual immediately before it on every controlled route.
  load('san-telmo-parallel-lives-red-20260819.js?v=20260819b', () => {
    load('san-telmo-source-stamp-20260819.js?v=20260819a');
  });

  // RSM NNR4 chronology/read-back update for the recovered 30-Nov-2021 San Telmo/RICPE finding.
  load('rsm-san-telmo-current-update-20260819.js?v=20260819a');
})();

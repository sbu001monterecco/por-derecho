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

  // Homepage identity/relationship correction and PwC 2016 knowledge checkpoint.
  // Canonical relationships: Antonio Cogolludo Rojas is Shaila's father;
  // Francisco Mario Matos Matas and Shaila María Cogolludo Ramos are husband and wife.
  load('homepage-actor-family-pwc-note-20260819.js?v=20260819a');
})();
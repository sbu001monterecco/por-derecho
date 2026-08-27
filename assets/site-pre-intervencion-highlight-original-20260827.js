(() => {
  const current = document.currentScript;
  if (!current) return;

  // Preserve and execute the complete established pre-Intervención loader unchanged.
  const prior = document.createElement('script');
  prior.src = new URL('site-pre-intervencion-highlight-before-eg95-20260823.js?v=20260824e', current.src).href;
  prior.async = false;
  prior.setAttribute('data-pre-fiscalia-eg95-pre-intervencion-loader', '20260823');
  document.head.appendChild(prior);

  // Add the source-controlled Fiscalía Tenerife EG 95/2026 propagation layer.
  const eg95 = document.createElement('script');
  eg95.src = new URL('fiscalia-eg95-propagation-20260823.js?v=20260823a', current.src).href;
  eg95.async = false;
  eg95.setAttribute('data-fiscalia-eg95-propagation-loader', '20260823');
  document.head.appendChild(eg95);

  // Claim-specific limitation/prescription/caducity, damages, restitution and interim-relief control.
  // This is deliberately independent from the criminal module: it prevents a blanket “criminal case freezes everything” rule.
  const prescriptionRecovery = document.createElement('script');
  prescriptionRecovery.src = new URL('prescription-caducity-recovery-20260826.js?v=20260826a', current.src).href;
  prescriptionRecovery.async = false;
  prescriptionRecovery.setAttribute('data-prescription-caducity-recovery-loader', '20260826');
  document.head.appendChild(prescriptionRecovery);
})();

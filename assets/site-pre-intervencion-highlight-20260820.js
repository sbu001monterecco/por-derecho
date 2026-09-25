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

  // Add the dated RICPE/CNMV Ethics Channel closure layer. The layer is route-scoped
  // and exits without changing any page outside the four canonical RICPE/CNMV routes.
  const ricpeCnmvClosure = document.createElement('script');
  ricpeCnmvClosure.src = new URL('ricpe-cnmv-closure-update-20260827.js?v=20260827a', current.src).href;
  ricpeCnmvClosure.async = false;
  ricpeCnmvClosure.setAttribute('data-ricpe-cnmv-closure-loader', '20260827');
  document.head.appendChild(ricpeCnmvClosure);

  // Add reciprocal discovery between the FTI/Meeting Point and RICPE/CNMV
  // evidence lanes. This is route-scoped and never performs an external act.
  const ftiMeetingPointRicpe = document.createElement('script');
  ftiMeetingPointRicpe.src = new URL('fti-meeting-point-ricpe-continuity-20260827.js?v=20260827a', current.src).href;
  ftiMeetingPointRicpe.async = false;
  ftiMeetingPointRicpe.setAttribute('data-fti-meeting-point-ricpe-loader', '20260827');
  document.head.appendChild(ftiMeetingPointRicpe);
})();

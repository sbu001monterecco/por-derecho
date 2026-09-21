(() => {
  const CONTROL = 'PD-FTI-MP-RICPE-CONTINUITY-20260827-01';
  const TARGETS = [
    '/es/lava-verde-club-sei-meeting-point/',
    '/en/lava-verde-club-sei-meeting-point/',
    '/es/fti-touristik-meeting-point-insolvencia-preconcurso-bluesea/',
    '/en/fti-touristik-meeting-point-insolvency-preinsolvency-bluesea/',
    '/es/cuaderno-juridico/meeting-point-357-2024-trazabilidad-judicial/',
    '/en/legal-notebook/meeting-point-357-2024-judicial-traceability/',
    '/es/alberto-lopez-villarrubia-meeting-point-357-masa-activa/',
    '/en/alberto-lopez-villarrubia-meeting-point-357-active-estate/',
    '/es/ric-private-equity-sun-park/',
    '/en/ric-private-equity-sun-park/',
    '/es/ricpe-hnt-gc836-trazabilidad/',
    '/en/ricpe-hnt-gc836-traceability/',
    '/es/cnmv-ricpe-verificacion/',
    '/en/cnmv-ricpe-verification/',
    '/es/ona-hotels-salida-concurso-36-2012/expediente-unitario-abril-2018-octubre-2019/',
    '/en/ona-hotels-insolvency-exit-36-2012/unitary-record-april-2018-october-2019/'
  ];

  const run = () => {
    const path = window.location.pathname.replace(/\/index\.html$/, '/');
    if (!TARGETS.some((target) => path.endsWith(target))) return;
    if (document.querySelector(`[data-fmr-inbound="${CONTROL}"]`)) return;

    const language = path.includes('/es/') ? 'es' : 'en';
    const href = language === 'es'
      ? '/por-derecho/es/fti-meeting-point-ricpe-alertador-continuidad/'
      : '/por-derecho/en/fti-meeting-point-ricpe-whistleblower-continuity/';
    const copy = language === 'es'
      ? {
          eyebrow: 'NUEVA RECONSTRUCCIÓN TRANSFRONTERIZA',
          title: 'FTI, Meeting Point y RICPE: prueba causal, cierre del canal y 27 acciones',
          body: 'La nueva espina criminal-first conecta el nexo local con tres insolvencias alemanas, 357/2024, Auren, SEPI/FASEE, BLUESEA y la última escalada RICPE/CNMV. Distingue hecho, inferencia, alegación, contraprueba y producción.',
          link: 'Abrir reconstrucción y registro de acciones →'
        }
      : {
          eyebrow: 'NEW CROSS-BORDER RECONSTRUCTION',
          title: 'FTI, Meeting Point and RICPE: causal proof, channel closure and 27 actions',
          body: 'The new criminal-first spine connects the local nexus with three German insolvencies, 357/2024, Auren, SEPI/FASEE, BLUESEA and the latest RICPE/CNMV escalation. It separates fact, inference, allegation, counterrecord and production.',
          link: 'Open the reconstruction and action register →'
        };

    const section = document.createElement('section');
    section.dataset.fmrInbound = CONTROL;
    section.setAttribute('aria-label', copy.title);
    section.style.cssText = 'background:#f3efe5;border-block:1px solid #d7cebd;padding:1.5rem 0;';
    section.innerHTML = `<div class="shell"><p style="margin:0 0 .35rem;font-size:.72rem;font-weight:900;letter-spacing:.06em;color:#963f2f">${copy.eyebrow}</p><h2 style="margin:.15rem 0 .6rem;font-size:clamp(1.35rem,2.7vw,2rem)">${copy.title}</h2><p style="max-width:75rem;margin:.35rem 0 .8rem">${copy.body}</p><p style="margin:0"><a href="${href}"><strong>${copy.link}</strong></a></p></div>`;

    const main = document.querySelector('main');
    if (!main) return;
    const firstSection = main.querySelector(':scope > section');
    if (firstSection && firstSection.nextSibling) main.insertBefore(section, firstSection.nextSibling);
    else main.appendChild(section);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, {once: true});
  else run();
})();

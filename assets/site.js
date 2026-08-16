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

  load('justice-map-navigation-20260815.js?v=20260815d', () => {
    load('concursal-accountability-navigation-20260815.js?v=20260815a', () => {
      load('site-accountability-20260814.js?v=20260815a', () => {
        load('accountability-evidence-grammar-20260815.js?v=20260815a', () => {
          load('institutional-accountability-spotlights-20260815.js?v=20260815a', () => {
            load('institutional-accountability-backlog-20260815.js?v=20260815a', () => {
              load('media-accountability-navigation-20260815.js?v=20260815a', () => {
                load('media-followup-pressrelease-fiscal-20260815.js?v=20260815a', () => {
                  load('canarias7-preview-fix-20260815.js?v=20260815a');
                });
              });
            });
          });
        });
        load('ricpe-identity-correction-20260815.js?v=20260815a', () => {
          load('police-evidence-preservation-20260815.js?v=20260815a', () => {
            load('police-regage-drilldown-20260815.js?v=20260815a', () => {
              load('police-context-explainer-20260815.js?v=20260815a', () => {
                load('book-foundation-20260815.js?v=20260815b', () => {
                  load('books-portfolio-20260815.js?v=20260815c');
                  // Book pages now carry the authoritative locked JPG cover in their HTML.
                  // Do not load the legacy SVG router here: it overwrites the correct cover after first paint.
                });
              });
            });
          });
        });
      });
    });
  });

  // Independent media-mark loader: do not make this depend on any other helper chain.
  load('media-publication-marks-20260815.js?v=20260815a');

  // Canary Council of Bar Associations institutional mark and source-controlled status record.
  load('ccca-institutional-mark-20260816.js?v=20260816a');

  // Canonical RICPE routing, 15-Aug chronology, legacy-dossier banner and SNCA FEDER boundary.
  load('canonical-routing-chronology-20260815.js?v=20260815a');

  // Banking-origin, direct-market and extraconcursal-perimeter bridge for the Community dossiers.
  load('origin-direct-market-context-20260816.js?v=20260816b');

  // Current banking-recovery publication routes plus the 2011-2012 default/enforcement evidence boundary.
  load('banking-recovery-publication-20260816.js?v=20260816b');

  // Dedicated Valencia banking-recovery page links across lender-of-record, possession/convergence and PH122→CAM chain pages.
  load('caixabank-valencia-claim-navigation-20260816.js?v=20260816a');

  // Source-controlled CaixaBank→Aweswell adhesion sequence for Borja, propagated to Valencia, lender, AC, Calificación and AP pages.
  load('caixabank-borja-witness-context-20260816.js?v=20260816a');

  // Companies House continuity: UK Monterecco Sun Park Limited renamed Aweswell Limited, same company no. 07716847.
  load('aweswell-monterecco-name-continuity-20260816.js?v=20260816a', () => {
    // Separate Spanish-company continuity: Monterecco Sun Park, S.L. renamed Pink Canary Services, S.L., same NIF B76564517.
    load('pink-canary-monterecco-spanish-continuity-20260816.js?v=20260816a');
  });

  // Controlled direct invitation naming Rosa María Dorta Perdomo as a historical identification lead only.
  load('rosa-dorta-direct-open-letter-20260816.js?v=20260816a');

  // LinkedIn professional-profile capture for Lourdes Castillejo on her ES/EN open-letter pages.
  load('lourdes-linkedin-profile-20260816.js?v=20260816a');

  // Verified 28-Jul-2026 AGE/RedSARA presentation in CGPJ Alzada 286/2026; presentation is not examination or merits.
  load('cgpj-alzada-regage-20260816.js?v=20260816a');

  // Calificacion: current appellate status and first-person accountability opening, source-complete AC crosswalk,
  // Allegation 01 collaboration audit, Allegation 02 third-party-credit audit, Allegation 03 Pink/rent operating audit,
  // then its non-fragmented Community/private-actor/AC causation layer before the €3.032m and institutional modules.
  load('calificacion-opening-accountability-20260816.js?v=20260816b', () => {
    load('calificacion-report-radical-transparency-20260816.js?v=20260816a', () => {
      load('calificacion-allegation01-collaboration-audit-20260816.js?v=20260816a', () => {
        load('calificacion-allegation02-thirdparty-credits-audit-20260816.js?v=20260816a', () => {
          load('calificacion-allegation03-pink-rent-operating-audit-20260816.js?v=20260816a', () => {
            load('calificacion-allegation03-unitary-community-ac-causation-20260816.js?v=20260816a', () => {
              load('calificacion-3032010-fabrication-allegation-20260816.js?v=20260816a', () => {
                load('calificacion-judicial-adoption-private-actor-bridge-20260816.js?v=20260816a', () => {
                  load('calificacion-fiscal-eg49-response-20260816.js?v=20260816a');
                });
              });
            });
          });
        });
      });
    });
  });

  // Community dossier cross-link into the non-fragmented Allegation-03 causation analysis.
  load('calificacion-a03-community-bridge-20260816.js?v=20260816a');

  // Calificacion: 2018 recognised secured-credit holder plus de facto material-control threshold;
  // separates creditor status, physical control, later adjudication and pre/post-control causation.
  // Loaded after the AC crosswalk so its insertion after that module becomes the causal baseline before serial allegation audits.
  load('calificacion-2018-creditor-material-control-20260816.js?v=20260816a');

  // Calificacion/recovery: documented positive-agency chronology and reciprocal recovery-through-adversity bridge.
  load('calificacion-recovery-through-adversity-20260816.js?v=20260816a');

  // Calificacion/recovery: force the contemporaneous rescue/finance/operation/protection counter-record into the public reading order.
  load('calificacion-documentary-counter-record-20260816.js?v=20260816a');

  // Calificacion: surface the verified 2017 court-record rescue filing and the 2018 reported direct judicial notice on the ES/EN landing pages.
  load('calificacion-prior-judicial-knowledge-20260816.js?v=20260816a');

  // Calificacion: supersede stale static wording that still described the now-complete 47-page AC report as outstanding.
  load('calificacion-source-status-correction-20260816.js?v=20260816a');
})();

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
                });
              });
            });
          });
        });
      });
    });
  });

  load('media-publication-marks-20260815.js?v=20260815a');
  load('ccca-institutional-mark-20260816.js?v=20260816a');
  load('canonical-routing-chronology-20260815.js?v=20260815a');
  load('origin-direct-market-context-20260816.js?v=20260816b');
  load('banking-recovery-publication-20260816.js?v=20260816b');
  load('caixabank-valencia-claim-navigation-20260816.js?v=20260816a');
  load('caixabank-borja-witness-context-20260816.js?v=20260816a');

  load('aweswell-monterecco-name-continuity-20260816.js?v=20260816a', () => {
    load('pink-canary-monterecco-spanish-continuity-20260816.js?v=20260816a');
  });

  load('rosa-dorta-direct-open-letter-20260816.js?v=20260816a');
  load('lourdes-linkedin-profile-20260816.js?v=20260816a');
  load('cgpj-alzada-regage-20260816.js?v=20260816a');
  load('lpam-magistrado-source-control-20260816.js?v=20260816a');

  load('calificacion-opening-accountability-20260816.js?v=20260816b', () => {
    load('calificacion-professional-read-20260816.js?v=20260816a');
    load('judge-alberto-approved-accusation-20260816.js?v=20260816a');
    load('calificacion-report-radical-transparency-20260816.js?v=20260816a', () => {
      load('calificacion-allegation01-collaboration-audit-20260816.js?v=20260816a', () => {
        load('calificacion-allegation02-thirdparty-credits-audit-20260816.js?v=20260816a', () => {
          load('calificacion-allegation03-pink-rent-operating-audit-20260816.js?v=20260816a', () => {
            load('calificacion-allegation03-unitary-community-ac-causation-20260816.js?v=20260816a', () => {
              load('calificacion-allegation04-accounting-audit-20260816.js?v=20260816a', () => {
                load('calificacion-allegation04-cls-bdo-correction-20260816.js?v=20260816a', () => {
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
    });
  });

  load('calificacion-a03-community-bridge-20260816.js?v=20260816a');
  load('calificacion-2018-creditor-material-control-20260816.js?v=20260816a');
  load('extraconcursal-force-authority-laundering-20260816.js?v=20260816a');
  load('extraconcursal-borja-security-source-upgrade-20260816.js?v=20260816a');
  load('calificacion-recovery-through-adversity-20260816.js?v=20260816a');
  load('calificacion-documentary-counter-record-20260816.js?v=20260816c');
  load('calificacion-prior-judicial-knowledge-20260816.js?v=20260816b');
  load('calificacion-source-status-correction-20260816.js?v=20260816a');
  load('calificacion-fiscal-2012-2019-2026-bridge-20260816.js?v=20260816b', () => {
    load('calificacion-primary-source-closures-20260816.js?v=20260816a');
  });
  load('calificacion-eleconomista-collateral-use-20260816.js?v=20260816a');
})();

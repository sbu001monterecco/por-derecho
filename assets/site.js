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
  load('origin-direct-market-context-20260816.js?v=20260816a');

  // Current banking-recovery publication routes, beginning with the PH122→CAM assignment / Article 1535 dossier.
  load('banking-recovery-publication-20260816.js?v=20260816a');

  // Companies House continuity: UK Monterecco Sun Park Limited renamed Aweswell Limited, same company no. 07716847.
  load('aweswell-monterecco-name-continuity-20260816.js?v=20260816a', () => {
    // Separate Spanish-company continuity: Monterecco Sun Park, S.L. renamed Pink Canary Services, S.L., same NIF B76564517.
    load('pink-canary-monterecco-spanish-continuity-20260816.js?v=20260816a');
  });

  // Controlled direct invitation naming Rosa María Dorta Perdomo as a historical identification lead only.
  load('rosa-dorta-direct-open-letter-20260816.js?v=20260816a');

  // LinkedIn professional-profile capture for Lourdes Castillejo on her ES/EN open-letter pages.
  load('lourdes-linkedin-profile-20260816.js?v=20260816a');
})();
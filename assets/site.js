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
})();
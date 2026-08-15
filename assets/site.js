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
        load('accountability-evidence-grammar-20260815.js?v=20260815a');
        load('ricpe-identity-correction-20260815.js?v=20260815a', () => {
          load('police-evidence-preservation-20260815.js?v=20260815a', () => {
            load('police-regage-drilldown-20260815.js?v=20260815a', () => {
              load('police-context-explainer-20260815.js?v=20260815a', () => {
                load('book-foundation-20260815.js?v=20260815b', () => {
                  load('books-portfolio-20260815.js?v=20260815c');
                  load('book-cover-router-20260815.js?v=20260815a');
                });
              });
            });
          });
        });
      });
    });
  });
})();
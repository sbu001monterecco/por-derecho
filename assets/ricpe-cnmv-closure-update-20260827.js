/* RICPE-CNMV-CLOSURE-WRAPPER-20260827 */
(() => {
  const current = document.currentScript;
  if (!current) return;

  const original = document.createElement('script');
  original.src = new URL('ricpe-cnmv-closure-update-original-20260827.js?v=20260827b', current.src).href;
  original.async = false;
  original.setAttribute('data-ricpe-cnmv-closure-original', '20260827');
  document.head.appendChild(original);

  const visuals = document.createElement('script');
  visuals.src = new URL('ricpe-cnmv-visual-evidence-20260827.js?v=20260827b', current.src).href;
  visuals.async = false;
  visuals.setAttribute('data-ricpe-cnmv-visual-evidence-loader', '20260827');
  document.head.appendChild(visuals);

  const perimeter = document.createElement('script');
  perimeter.src = new URL('ricpe-perimeter-media-20260827.js?v=20260827a', current.src).href;
  perimeter.async = false;
  perimeter.setAttribute('data-ricpe-perimeter-media-loader', '20260827');
  document.head.appendChild(perimeter);
})();

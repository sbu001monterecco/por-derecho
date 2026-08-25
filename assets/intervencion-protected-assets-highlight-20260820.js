(() => {
  if (window.__pdIntervencionProtectedAssets20260820) return;
  window.__pdIntervencionProtectedAssets20260820 = true;
  const current = document.currentScript;
  const path = window.location.pathname;
  const isEn = /\/en\//.test(path);
  const assetName = `intervencion-integridad-bienes-protegidos-${isEn ? 'en' : 'es'}.svg`;
  const assetUrl = current ? new URL(assetName, current.src).href : `/por-derecho/assets/${assetName}`;
  const pngName = `intervencion-integridad-bienes-protegidos-${isEn ? 'en' : 'es'}.png`;
  const style = document.createElement('style');
  style.textContent = `
    .pd-intervencion-asset{margin:1.35rem 0 1.7rem;padding:0;background:#fff;border:1px solid rgba(19,37,45,.15);border-radius:18px;overflow:hidden;box-shadow:0 18px 42px rgba(16,37,46,.13)}
    .pd-intervencion-asset img{display:block;width:100%;height:auto;background:#0a1b28}
    .pd-intervencion-asset figcaption{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:1rem;align-items:center;padding:.9rem 1rem 1rem;border-top:1px solid rgba(19,37,45,.12);color:#334950;font-size:.9rem;line-height:1.55}
    .pd-intervencion-asset .pd-ipa-caption strong{color:#13252d}
    .pd-intervencion-asset .pd-ipa-actions{display:flex;flex-wrap:wrap;gap:.55rem;justify-content:flex-end}
    .pd-intervencion-asset .pd-ipa-actions a,.pd-intervencion-asset .pd-ipa-actions button{appearance:none;border:1px solid rgba(19,37,45,.22);background:#f7f4ed;color:#13252d;border-radius:999px;padding:.55rem .8rem;font:inherit;font-weight:850;text-decoration:none;cursor:pointer}
    .pd-intervencion-asset .pd-ipa-actions button{background:#13252d;color:#fff;border-color:#13252d}
    .pd-intervencion-asset.compact figcaption{font-size:.84rem}
    @media(max-width:760px){.pd-intervencion-asset figcaption{grid-template-columns:1fr}.pd-intervencion-asset .pd-ipa-actions{justify-content:flex-start}}
  `;
  document.head.appendChild(style);

  const figure = (compact=false) => `<figure class="pd-intervencion-asset${compact ? ' compact' : ''}" data-intervencion-protected-assets-highlight>
    <a href="${assetUrl}" target="_blank" rel="noopener" aria-label="${isEn ? 'Open documented institutional milestone visual' : 'Abrir visual del hito institucional documentado'}"><img src="${assetUrl}" width="1600" height="900" loading="lazy" alt="${isEn ? '24 February 2026 — Integrity Commission — assets under judicial or insolvency protection' : '24 febrero 2026 — Comisión para Integridad Pública — bienes bajo tutela judicial o concursal'}"></a>
    <figcaption><span class="pd-ipa-caption"><strong>${isEn ? 'Reusable source-controlled visual.' : 'Visual reutilizable controlado por fuente.'}</strong> ${isEn ? 'The 5 March General Intervention response records Commission consideration on 24 February and an anonymised Justice referral concerning the protected-assets issue. The visual does not convert that routing into a merits finding.' : 'La respuesta de 5 de marzo de la Intervención General deja constancia del examen por la Comisión el 24 de febrero y del traslado anonimizado a Justicia sobre la cuestión de los bienes protegidos. El visual no convierte ese traslado en una resolución de fondo.'}</span><span class="pd-ipa-actions"><a href="${assetUrl}" target="_blank" rel="noopener">${isEn ? 'Open / share SVG' : 'Abrir / compartir SVG'}</a><button type="button" data-intervencion-download-png>${isEn ? 'Download PNG' : 'Descargar PNG'}</button></span></figcaption>
  </figure>`;

  const downloadPng = async () => {
    try {
      const svg = await fetch(assetUrl, {cache:'no-store'}).then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.text(); });
      const blob = new Blob([svg], {type:'image/svg+xml;charset=utf-8'});
      const src = URL.createObjectURL(blob);
      const img = new Image();
      await new Promise((resolve, reject) => { img.onload = resolve; img.onerror = reject; img.src = src; });
      const canvas = document.createElement('canvas'); canvas.width = 1600; canvas.height = 900;
      const ctx = canvas.getContext('2d'); ctx.drawImage(img, 0, 0, 1600, 900); URL.revokeObjectURL(src);
      const png = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
      if (!png) throw new Error('PNG export failed');
      const pngUrl = URL.createObjectURL(png); const a = document.createElement('a'); a.href = pngUrl; a.download = pngName; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(pngUrl), 1500);
    } catch (err) { window.open(assetUrl, '_blank', 'noopener'); }
  };

  const inject = () => {
    if (/\/(es\/registros-institucionales|en\/institutional-records)\/?(?:index\.html)?$/.test(path)) {
      const intervention = document.querySelector('#gobcan-intervencion');
      if (intervention && !document.querySelector('[data-intervencion-protected-assets-highlight]')) intervention.insertAdjacentHTML('afterend', figure(false));
    }
    const home = /\/por-derecho\/(es|en)\/?(?:index\.html)?$/.test(path) || /^\/(es|en)\/?(?:index\.html)?$/.test(path);
    if (home && !document.querySelector('[data-intervencion-protected-assets-highlight]')) {
      const card = Array.from(document.querySelectorAll('.authority-card')).find(c => /intervenci[oó]n general|general intervention/i.test(c.textContent || ''));
      if (card) card.insertAdjacentHTML('afterend', figure(true));
    }
    if (/\/(es|en)\/ric-private-equity-sun-park\/?(?:index\.html)?$/.test(path) && !document.querySelector('[data-intervencion-protected-assets-highlight]')) {
      const anchor = document.querySelector('#pregunta-unitaria');
      if (anchor) anchor.insertAdjacentHTML('afterend', `<section class="section alt" data-intervencion-asset-section><div class="shell">${figure(false)}</div></section>`);
    }
    document.querySelectorAll('[data-intervencion-download-png]').forEach(btn => btn.addEventListener('click', downloadPng));
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject, {once:true}); else inject();
})();

/* CRIMINAL-FIRST-ACTION-PRESSURE-20260825 */
(() => {
  const current = document.currentScript;
  if (!current || document.querySelector('script[data-criminal-first-action-pressure-loader]')) return;
  const module = document.createElement('script');
  module.src = new URL('criminal-first-action-pressure-20260825.js?v=20260825a', current.src).href;
  module.async = false;
  module.setAttribute('data-criminal-first-action-pressure-loader', '20260825');
  document.head.appendChild(module);
})();
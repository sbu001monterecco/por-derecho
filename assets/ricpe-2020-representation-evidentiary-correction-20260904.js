(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const siteRoot = new URL('../', current.src);
  const rootPath = siteRoot.pathname.replace(/\/+$/, '/');
  const pathname = window.location.pathname.replace(/\/index\.html$/, '/').replace(/\/+$/, '/');
  const relative = pathname.startsWith(rootPath) ? pathname.slice(rootPath.length) : pathname.replace(/^\/+/, '');
  if (!new Set(['es/ric-private-equity-sun-park/', 'en/ric-private-equity-sun-park/']).has(relative)) return;

  const apply = () => {
    const container = document.querySelector('.reality-conclusion');
    const paragraph = container?.querySelector('p');
    if (!paragraph || paragraph.dataset.evidentiaryCorrection === '20260904') return;
    const original = paragraph.textContent || '';
    if (relative.startsWith('es/') && original.includes('eran materialmente falsas cuando se pronunciaron')) {
      paragraph.innerHTML = '<strong>Por Derecho sostiene que, aplicadas a Sun Park, las afirmaciones de dominio integral y ausencia de cargas realizadas en el webinar de 11 de noviembre de 2020 eran materialmente falsas cuando se pronunciaron.</strong> Es una alegación atribuida a Gil Marer, apoyada en la posterior versión de CAM/RICPE y en que el título LPB no se otorgó hasta febrero de 2022; no es una conclusión judicial ni prueba por sí sola conocimiento, intención, engaño o responsabilidad de una persona concreta.';
      const label = container.querySelector('span');
      if (label) label.textContent = 'Alegación documental de Por Derecho · no conclusión judicial';
      paragraph.dataset.evidentiaryCorrection = '20260904';
    }
    if (relative.startsWith('en/') && original.includes('were materially false when spoken')) {
      paragraph.innerHTML = '<strong>Por Derecho alleges that, as applied to Sun Park, the claims of whole ownership and absence of encumbrances made in the 11 November 2020 webinar were materially false when spoken.</strong> This is a position attributed to Gil Marer, relying on CAM/RICPE\'s later account and the fact that LPB title was not conveyed until February 2022; it is not a judicial finding and does not by itself prove any identified person\'s knowledge, intent, deception or liability.';
      const label = container.querySelector('span');
      if (label) label.textContent = 'Por Derecho documentary allegation · not a judicial finding';
      paragraph.dataset.evidentiaryCorrection = '20260904';
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply, { once: true });
  else apply();
  window.setTimeout(apply, 500);
})();

(() => {
  const path = location.pathname.replace(/\/+$/, '/');
  const isEn = /\/en\//.test(path);
  const t = (es, en) => isEn ? en : es;
  const root = `/por-derecho/${isEn ? 'en' : 'es'}/`;

  const apply = () => {
    if (/\/ric-private-equity-sun-park\/$/.test(path)) {
      const hero = document.querySelector('.dossier-hero');
      if (hero) {
        const eyebrow = hero.querySelector('.eyebrow');
        if (eyebrow) eyebrow.textContent = t('Comunicación formal presentada · 17 agosto 2026 · registro unitario', 'Formal communication submitted · 17 August 2026 · unitary record');
        const lead = hero.querySelector('.lead');
        if (lead) lead.textContent = t('Gobernanza, título, conflictos, due diligence, capital y respuesta en la transformación de Sun Park en MYND Yaiza.', 'Governance, title, conflicts, due diligence, capital and response in the transformation of Sun Park into MYND Yaiza.');
        const actions = hero.querySelector('.actions');
        if (actions && !actions.dataset.psrSimplified) {
          actions.dataset.psrSimplified = '1';
          actions.innerHTML = `
            <a class="button" href="#psr-ricpe-cockpit">${t('Lectura Consejo / Compliance · 7 min', 'Board / Compliance read · 7 min')}</a>
            <a class="button secondary" href="#psr-ricpe-five-docs">${t('5 documentos decisivos', '5 decisive documents')}</a>
            <a class="button secondary" href="#pregunta-unitaria">${t('Abrir expediente completo', 'Open full dossier')}</a>`;
        }
      }
    }

    if (/\/(comunidad-instrumentalizacion|community-instrumentalisation)\/$/.test(path)) {
      const hero = document.querySelector('.dossier-hero');
      if (hero) {
        const actions = hero.querySelector('.actions');
        if (actions && !actions.dataset.psrSimplified) {
          actions.dataset.psrSimplified = '1';
          actions.innerHTML = `
            <a class="button" href="#resumen">${t('Entenderlo en 2 minutos', 'Understand it in 2 minutes')}</a>
            <a class="button secondary" href="${root}${isEn ? 'community-instrumentalisation/minutes-2011-2022/' : 'comunidad-instrumentalizacion/actas-2011-2022/'}">${t('Auditar actas y autoridad', 'Audit minutes and authority')}</a>
            <a class="button secondary" href="${root}ric-private-equity-sun-park/">${t('Seguir la cadena hacia RICPE', 'Follow the chain to RICPE')}</a>`;
        }
      }
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => setTimeout(apply, 900), { once: true });
  else setTimeout(apply, 900);
  setTimeout(apply, 1800);
})();

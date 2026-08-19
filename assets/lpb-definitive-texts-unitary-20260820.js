(() => {
  'use strict';

  const run = () => {
    const pathname = window.location.pathname.replace(/\/+$/, '/');
    const isEs = pathname.includes('/por-derecho/es/');
    const isEn = pathname.includes('/por-derecho/en/');
    if (!isEs && !isEn) return;

    const base = '/por-derecho';
    const canonical = isEs
      ? `${base}/es/textos-definitivos-lpb-base-liquidacion/`
      : `${base}/en/lpb-definitive-texts-liquidation-baseline/`;
    const isCanonical = pathname === canonical;
    const isAdjudication = /\/(adjudicacion-2022-reconstruccion-documental|2022-adjudication-documentary-reconstruction)\//.test(pathname);
    const isHome = pathname === `${base}/${isEs ? 'es' : 'en'}/`;
    const isUpdates = /\/(actualizaciones|updates)\//.test(pathname);
    const isControl = /\/(sala-control-caso|case-control-room|ingenieria-forense-criminal-sun-park|sun-park-criminal-engineering-investigation)\//.test(pathname);

    const copy = isEs ? {
      eyebrow: 'PROMOCIÓN A FUENTE PRIMARIA · 20 AGOSTO 2026',
      title: 'Los textos definitivos y la base de liquidación de LPB ya están reconstruidos como cadena primaria.',
      body: 'El informe de 2013, el escrito y la lista definitiva de 2016, la modificación de titular de febrero de 2018 y el plan que se remite al inventario elevado a definitivo permiten fijar el punto de partida. Sigue pendiente conciliarlo con deuda pagadera, escritura, Registro y cuentas finales.',
      action: 'Abrir la base documental →',
      metrics: ['19.486.498,94 € activo definitivo', '10.125.752,00 € pasivo definitivo', '9.052.251,69 € privilegio especial'],
      boundary: 'Clasificación concursal, cobertura hipotecaria, deuda pagadera, contraprestación y resultado de realización son magnitudes distintas.',
      crossTitle: 'Base de liquidación LPB',
      crossBody: 'Antes de valorar la adjudicación, el crédito, la actuación de la AC, la tasación o la implementación notarial/registral, parta del informe 2013 + textos/lista 2016 + modificación 2018 + inventario definitivo.',
      updateTitle: 'Nueva base primaria: textos definitivos de LPB',
      updateBody: 'Se localizó y controló la cadena documental sobre la que el propio plan de liquidación decía operar. También se preservan las inconsistencias internas del escrito de 2016 y los documentos que aún faltan para cerrar la certificación y las cuentas.',
      updateAction: 'Ver reconstrucción y cifras →'
    } : {
      eyebrow: 'PRIMARY-SOURCE PROMOTION · 20 AUGUST 2026',
      title: 'LPB’s definitive texts and liquidation baseline are now reconstructed as a primary-source chain.',
      body: 'The 2013 report, the 2016 filing and definitive list, the February 2018 holder modification and the plan referring back to the inventory made definitive establish the starting point. Reconciliation with payable debt, deed, Registry and final accounts remains outstanding.',
      action: 'Open the documentary baseline →',
      metrics: ['EUR 19,486,498.94 definitive active mass', 'EUR 10,125,752.00 definitive passive mass', 'EUR 9,052,251.69 special privilege'],
      boundary: 'Insolvency classification, mortgage coverage, payable debt, consideration and realisation outcome are distinct quantities.',
      crossTitle: 'LPB liquidation baseline',
      crossBody: 'Before assessing the adjudication, credit, Administrator, appraisal or notarial/Registry implementation, start with the 2013 report + 2016 definitive filing/list + 2018 modification + definitive inventory.',
      updateTitle: 'New primary baseline: LPB definitive texts',
      updateBody: 'The documentary chain on which the liquidation plan itself said it operated is now located and controlled. The 2016 filing’s internal inconsistencies and the still-missing certification and accounting documents are preserved visibly.',
      updateAction: 'Open reconstruction and figures →'
    };

    const ensureStyles = () => {
      if (document.getElementById('lpb-definitive-texts-unitary-styles')) return;
      const style = document.createElement('style');
      style.id = 'lpb-definitive-texts-unitary-styles';
      style.textContent = `
        .lpb-td-panel{max-width:1120px;margin:0 auto;border-left:5px solid #2f6b58;background:#f4fbf7;border-radius:16px;padding:1.1rem 1.25rem}
        .lpb-td-panel h2{margin:.15rem 0 .55rem}.lpb-td-panel p:last-child{margin-bottom:0}
        .lpb-td-kicker{margin:0 0 .4rem;font-size:.76rem;letter-spacing:.08em;text-transform:uppercase;font-weight:850;color:#2f6b58}
        .lpb-td-metrics{display:flex;gap:.55rem;flex-wrap:wrap;margin:.85rem 0}.lpb-td-metrics span{border:1px solid #6f9688;border-radius:999px;padding:.3rem .68rem;background:#fff;font-size:.82rem;font-weight:800}
        .lpb-td-boundary{font-size:.88rem;opacity:.82}.lpb-td-link{font-weight:850}
        .lpb-td-crosslink{max-width:1120px;margin:0 auto;border-left:5px solid #536d79;background:#f4f8fa;border-radius:14px;padding:1rem 1.2rem}
        .lpb-td-crosslink h2{margin:.1rem 0 .45rem}.lpb-td-crosslink p:last-child{margin-bottom:0}
        .lpb-td-update{max-width:1120px;margin:0 auto;background:#13252d;color:#fff;border-radius:16px;padding:1.1rem 1.25rem}.lpb-td-update h2{margin:.1rem 0 .45rem;color:#fff}.lpb-td-update a{color:#fff;font-weight:850}
      `;
      document.head.appendChild(style);
    };

    const makeSection = (className, html) => {
      const section = document.createElement('section');
      section.className = `section ${className}`;
      section.dataset.lpbDefinitiveTextsUnitary = '20260820';
      section.innerHTML = `<div class="shell">${html}</div>`;
      return section;
    };

    const insertAfterHero = section => {
      const main = document.querySelector('main');
      if (!main) return;
      const hero = main.querySelector(':scope > .hero, :scope > .dossier-hero, :scope > .mhero, :scope > section.hero, :scope > section.dossier-hero');
      if (hero) hero.insertAdjacentElement('afterend', section);
      else if (main.firstElementChild) main.firstElementChild.insertAdjacentElement('afterend', section);
      else main.appendChild(section);
    };

    const insertAdjudicationPromotion = () => {
      if (!isAdjudication || document.querySelector('[data-lpb-td-primary-promotion]')) return;
      ensureStyles();
      const section = makeSection('lpb-td-primary-section', `
        <aside class="lpb-td-panel" data-lpb-td-primary-promotion="20260820" role="note">
          <p class="lpb-td-kicker">${copy.eyebrow}</p>
          <h2>${copy.title}</h2>
          <p>${copy.body}</p>
          <div class="lpb-td-metrics">${copy.metrics.map(item => `<span>${item}</span>`).join('')}</div>
          <p class="lpb-td-boundary"><strong>${copy.boundary}</strong></p>
          <p><a class="lpb-td-link" href="${canonical}">${copy.action}</a></p>
        </aside>`);
      insertAfterHero(section);
    };

    const relevantRoute = () => {
      if (isCanonical || isAdjudication || isHome || isUpdates || isControl) return false;
      return /(acreedor-de-registro|lender-of-record|administrador-concursal|insolvency-administrator|insolvencia-lpb|lpb-insolvency|actua-2018|valuation|implementacion-notarial|notarial-implementation|implementacion-registral|land-registry-implementation|articulo-1535|article-1535|mercantile-court-1|magistrado-juez|concurso-36-2012-laj|insolvency-36-2012-laj|correcciones-control-versiones|corrections-version-control)/i.test(pathname);
    };

    const insertCrosslink = () => {
      if (!relevantRoute() || document.querySelector('[data-lpb-td-crosslink]')) return;
      ensureStyles();
      const section = makeSection('lpb-td-crosslink-section', `
        <aside class="lpb-td-crosslink" data-lpb-td-crosslink="20260820" role="note">
          <h2>${copy.crossTitle}</h2>
          <p>${copy.crossBody}</p>
          <p><a href="${canonical}">${copy.action}</a></p>
        </aside>`);
      insertAfterHero(section);
    };

    const insertUpdate = () => {
      if (!(isHome || isUpdates || isControl) || document.querySelector('[data-lpb-td-update]')) return;
      ensureStyles();
      const section = makeSection('lpb-td-update-section', `
        <aside class="lpb-td-update" data-lpb-td-update="20260820">
          <p class="lpb-td-kicker" style="color:#d7eadf">${copy.eyebrow}</p>
          <h2>${copy.updateTitle}</h2>
          <p>${copy.updateBody}</p>
          <p><a href="${canonical}">${copy.updateAction}</a></p>
        </aside>`);
      insertAfterHero(section);
    };

    const applyTextCorrections = () => {
      const replacements = isEs ? [
        ['Textos definitivos completos;', 'Paquete judicial certificado completo de los textos definitivos;'],
        ['Lista definitiva completa, modificaciones, liquidación a 21/02/2022 y resolución que sustenta cada componente.', 'Textos y lista definitivos primarios localizados; faltan el paquete judicial certificado, Anexo 2, asiento/providencia, modificaciones posteriores, liquidación a 21/02/2022 y resolución que sustenta cada componente.']
      ] : [
        ['Complete definitive creditor texts;', 'Court-certified complete definitive-text bundle;'],
        ['Complete definitive list, modifications, 21 February 2022 payoff and the decision supporting each component.', 'Primary definitive filing and list located; the certified court bundle, Annex 2, filing receipt/order, later modifications, 21 February 2022 payoff and the decision supporting each component remain outstanding.']
      ];
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      const nodes = [];
      while (walker.nextNode()) nodes.push(walker.currentNode);
      nodes.forEach(node => {
        let value = node.nodeValue;
        replacements.forEach(([from, to]) => { value = value.replace(from, to); });
        if (value !== node.nodeValue) node.nodeValue = value;
      });
    };

    if (isCanonical) document.documentElement.dataset.lpbDefinitiveTextsUnitary = '20260820';
    applyTextCorrections();
    insertAdjudicationPromotion();
    insertCrosslink();
    insertUpdate();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
  window.setTimeout(run, 1800);
})();

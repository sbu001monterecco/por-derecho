(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const id = 'retracto-tanteo-four-track-19aug2026';
  if (document.getElementById(id)) return;

  const isEs = path.includes('/por-derecho/es/');
  const isEn = path.includes('/por-derecho/en/');
  if (!isEs && !isEn) return;

  const relevant = [
    'retracto', 'article-1535', 'articulo-1535', 'acreedor-de-registro', 'lender-of-record',
    'acosta-matos', 'comunidad', 'community', 'explotacion', 'exploitation', 'actas',
    'administrador-concursal', 'insolvency-administrator', 'toma-control', 'takeover',
    'insolvencia-lpb', 'lpb-insolvency', 'convergencia-venta-acreedor', 'sale-lender-convergence',
    'recuperacion-restitucion', 'recovery-restitution', 'mismo-hotel', 'same-hotel',
    'ricpe', 'ric-private-equity', 'fondos-incentivos', 'institutionalisation-chain'
  ];
  if (!relevant.some(fragment => path.includes(fragment))) return;

  const isDedicated = path.includes('/retracto-tanteo-cuatro-vias/') || path.includes('/retracto-tanteo-four-tracks/');
  if (isDedicated) return;

  // Primary-source correction lock: body 8-Feb; judge signature 9-Feb;
  // LAJ signature 14-Feb; later notification/file label 15-Feb.
  // Do not touch five-day remedies belonging to the 5-Mar-2018 decree or 13-May-2024 ordering act.
  document.querySelectorAll('main p, main li, main td, main .question, main .card').forEach(el => {
    const text = el.textContent || '';
    const lower = text.toLowerCase();
    const hasControlledDate = lower.includes('8 feb') || lower.includes('8 de febrero') ||
      lower.includes('15 feb') || lower.includes('15 de febrero');
    const isCreditorAuto = hasControlledDate && (lower.includes('cam') || lower.includes('credit') ||
      lower.includes('acreedor') || lower.includes('mercantil') || lower.includes('commercial court'));
    if (!isCreditorAuto) return;
    let html = el.innerHTML;
    const replacements = [
      ['five-day <code>recurso de reposición</code> without suspensive effect', '20-day <code>recurso de apelación</code> under Article 97 bis.2 of the then-applicable Insolvency Law'],
      ['five-day recurso de reposición without suspensive effect', '20-day recurso de apelación under Article 97 bis.2 of the then-applicable Insolvency Law'],
      ['five-day recurso de reposicion without suspensive effect', '20-day recurso de apelación under Article 97 bis.2 of the then-applicable Insolvency Law'],
      ['recurso de reposición de cinco días', 'recurso de apelación en el plazo de veinte días conforme al art. 97 bis.2 LC'],
      ['recurso de reposicion de cinco dias', 'recurso de apelación en el plazo de veinte días conforme al art. 97 bis.2 LC']
    ];
    let changed = false;
    replacements.forEach(([from, to]) => {
      if (html.includes(from)) {
        html = html.replaceAll(from, to);
        changed = true;
      }
    });
    if (changed) el.innerHTML = html;
  });

  const isCreditRoute = path.includes('retracto-credito-litigioso-1041-2017') ||
    path.includes('litigious-credit-retracto-1041-2017') ||
    path.includes('via-residual-articulo-1535') ||
    path.includes('residual-article-1535-pathway') ||
    path.includes('credito-litigioso-escritura') ||
    path.includes('litigious-credit-hidden-deed');

  const style = document.createElement('style');
  style.textContent = `
    main code{overflow-wrap:anywhere;word-break:break-word;white-space:normal;max-width:100%}
    #${id}{background:#eef3f4}
    #${id} .rt-wrap{max-width:1120px;margin:0 auto}
    #${id} .rt-shell{background:#fff;border:1px solid rgba(19,37,45,.18);border-radius:18px;padding:1.15rem 1.3rem;box-shadow:0 10px 26px rgba(19,37,45,.08)}
    #${id} .rt-label{display:inline-block;background:#3c1715;color:#fff;border-radius:999px;padding:.3rem .62rem;font-size:.74rem;font-weight:850;letter-spacing:.06em;text-transform:uppercase}
    #${id} h2{margin:.65rem 0 .6rem;color:#13252d}
    #${id} .rt-lead{font-size:1.05rem;line-height:1.55}
    #${id} .rt-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;margin:1rem 0}
    #${id} .rt-card{border:1px solid #d9e1e3;border-radius:13px;padding:.85rem .95rem;background:#f9fbfb;min-width:0}
    #${id} .rt-card strong{display:block;color:#3c1715;margin-bottom:.3rem}
    #${id} .rt-warning{background:#fff8e8;border-left:5px solid #8c6b2f;border-radius:0 12px 12px 0;padding:.85rem 1rem;margin:.9rem 0}
    #${id} .rt-law{background:#f6eeee;border:1px solid #d9b3ae;border-radius:12px;padding:.85rem 1rem;margin:.9rem 0}
    #${id} .rt-actions{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:.9rem}
    #${id} .rt-actions a{display:inline-block;background:#13252d;color:#fff;text-decoration:none;font-weight:800;border-radius:999px;padding:.58rem .86rem;overflow-wrap:anywhere}
    #${id} .rt-small{font-size:.91rem;color:#4d5a5f}
    @media(max-width:780px){#${id} .rt-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.id = id;
  section.className = 'section';

  if (isEs) {
    section.innerHTML = `
      <div class="shell rt-wrap"><div class="rt-shell">
        <span class="rt-label">NO CONFUNDIR · CUATRO VÍAS DISTINTAS</span>
        <h2>${isCreditRoute ? 'DP 1041 es la vía del crédito. Existe además un trabajo separado sobre transmisiones de unidades.' : 'No hay un único “retracto”: cada operación exige su propia base jurídica.'}</h2>
        <p class="rt-lead">DP 1041/2017 trató la cesión PH122→CAM de <strong>crédito hipotecario</strong> y la posible aplicación del art. 1535 CC. Separadamente, en mayo–junio de 2018 consta un trabajo jurídico sobre posibles derechos de adquisición preferente/retracto relativos a <strong>intereses inmobiliarios individuales</strong> de Sun Park. La existencia de ese segundo trabajo está documentada; la existencia, base, titularidad y plazo de un derecho ejercitable debe probarse operación por operación.</p>
        <div class="rt-grid">
          <div class="rt-card"><strong>RTA · Crédito / art. 1535 / DP 1041</strong><span>Cesión PH122→CAM. Objeto: crédito. No describe ventas de apartamentos/locales.</span></div>
          <div class="rt-card"><strong>RTB · Trabajo jurídico de unidades · 2018</strong><span>Los abogados analizaron tanteo/retracto de LUCHY frente a unidades adquiridas a minoritarios por un tercero, identificado entonces como “CAM?” en una comunicación.</span></div>
          <div class="rt-card"><strong>RTC · Comuneros · arts. 1522–1524 CC</strong><span>Sólo es candidato cuando se vende a un extraño una cuota indivisa de la misma cosa común. No nace por ser propietarios de apartamentos distintos.</span></div>
          <div class="rt-card"><strong>RTD · Contrato / turismo / explotación</strong><span>Estatutos, título horizontal, arquitectura de 2008, CEXP, unidad de explotación e instrumentos concursales deben revisarse por separado.</span></div>
        </div>
        <div class="rt-law"><strong>Corrección jurídica importante:</strong> la DT única.4 de la Ley canaria 5/1999 que fue investigada por los abogados no era una base operativa en 2018: la Ley 2/2000 la había suprimido y la STC 28/2012 la declaró inconstitucional y nula. Por eso el derecho válido —si existía— debe encontrarse en otra base aplicable a la operación concreta.</div>
        <div class="rt-warning"><strong>Fincas que ahora requieren prueba específica:</strong> 8.499; 8.500 (pro indiviso y, por ello, candidata prioritaria para análisis art. 1522); 8.706; 8.718 (secuencia de adquisiciones de mayo de 2018); y 8.501. Ninguna se etiqueta automáticamente como “retractable”.</div>
        <p class="rt-small"><strong>AC / causalidad:</strong> el C5 de DP 1041 sólo prueba que la AC causó el fin del mandato formal específico de Cristo para LPB en esa vía. No se traslada automáticamente a los derechos sobre unidades: cada uno exige demostrar titular, control, conocimiento, plazo, acción/omisión, perjuicio y beneficio para CAM.</p>
        <div class="rt-actions"><a href="/por-derecho/es/retracto-tanteo-cuatro-vias/">Abrir mapa completo de las cuatro vías →</a>${isCreditRoute ? '<a href="/por-derecho/es/via-residual-articulo-1535/">Volver a la vía residual art. 1535</a>' : ''}</div>
      </div></div>`;
  } else {
    section.innerHTML = `
      <div class="shell rt-wrap"><div class="rt-shell">
        <span class="rt-label">DO NOT CONFUSE · FOUR DISTINCT TRACKS</span>
        <h2>${isCreditRoute ? 'PP 1041 is the credit route. A separate unit-transfer legal workstream also existed.' : 'There is no single “retracto”: each transaction needs its own legal basis.'}</h2>
        <p class="rt-lead">PP 1041/2017 concerned the PH122→CAM assignment of <strong>mortgage credit</strong> and the possible application of Civil Code Article 1535. Separately, in May–June 2018 the legal team investigated possible preferential-acquisition/retracto remedies concerning <strong>individual Sun Park property interests</strong>. That second workstream is documented; the existence, basis, holder and timing of any enforceable right must be proved transaction by transaction.</p>
        <div class="rt-grid">
          <div class="rt-card"><strong>RTA · Credit / Article 1535 / PP 1041</strong><span>PH122→CAM assignment. Object: credit. It does not describe apartment/local sales.</span></div>
          <div class="rt-card"><strong>RTB · 2018 unit-rights legal workstream</strong><span>Counsel analysed a LUCHY tanteo/retracto concerning units acquired from minority owners by a third party, contemporaneously written as “CAM?”.</span></div>
          <div class="rt-card"><strong>RTC · Co-owners · Civil Code 1522–1524</strong><span>Candidate only when an undivided share in the same common property is sold to an outsider. It does not arise merely because different apartments share common elements.</span></div>
          <div class="rt-card"><strong>RTD · Contract / tourism / exploitation</strong><span>Statutes, horizontal title, 2008 architecture, CEXP, single-operation rules and insolvency instruments require independent review.</span></div>
        </div>
        <div class="rt-law"><strong>Important legal correction:</strong> paragraph 4 of the sole transitional provision of Canary Law 5/1999, investigated by counsel, was not an operative 2018 basis: Law 2/2000 had removed it and Constitutional Court judgment 28/2012 declared it unconstitutional and void. Any valid right must therefore be found in another legal basis applicable to the specific transaction.</div>
        <div class="rt-warning"><strong>Fincas now requiring transaction-specific testing:</strong> 8,499; 8,500 (pro indiviso and therefore a priority Article 1522 candidate); 8,706; 8,718 (May 2018 acquisition sequence); and 8,501. None is automatically labelled retractable.</div>
        <p class="rt-small"><strong>Administrator / causation:</strong> the PP 1041 C5 finding only proves AC causation of the end of Cristo's specific formal LPB mandate in that workstream. It does not automatically transfer to unit rights: each requires proof of holder, control, knowledge, deadline, act/omission, loss and CAM-side benefit.</p>
        <div class="rt-actions"><a href="/por-derecho/en/retracto-tanteo-four-tracks/">Open the full four-track map →</a>${isCreditRoute ? '<a href="/por-derecho/en/residual-article-1535-pathway/">Return to the residual Article 1535 pathway</a>' : ''}</div>
      </div></div>`;
  }

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector(':scope > .hero, :scope > section.hero, :scope > .dossier-hero, :scope > .cnmv-hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else main.insertAdjacentElement('afterbegin', section);
})();

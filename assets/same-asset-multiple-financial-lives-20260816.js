(() => {
  const path = window.location.pathname;
  const id = 'same-asset-multiple-financial-lives-16aug2026';
  if (document.getElementById(id)) return;

  const excluded = [
    '/es/mismo-hotel-multiples-vidas-financieras/',
    '/en/same-hotel-multiple-financial-lives/'
  ];
  if (excluded.some((item) => path.includes(item))) return;

  const targets = [
    /\/por-derecho\/es\/?$/,
    /\/por-derecho\/en\/?$/,
    /calificacion-concurso-36-2012-vidas-paralelas/,
    /insolvency-classification-parallel-lives/,
    /ricpe-responsabilidad-documental/,
    /ricpe-documentary-accountability/,
    /cadena-instrumentalizacion-ric-fondos-incentivos/,
    /institutionalisation-chain-ric-eu-incentives/,
    /acosta-matos-perimetro/,
    /acosta-matos-perimeter/,
    /cnmv-ricpe-verificacion/,
    /cnmv-ricpe-verification/,
    /snca-fondos-europeos-trazabilidad/,
    /snca-eu-funds-traceability/,
    /ric-private-equity-sun-park/,
    /objetivos-recuperacion-restitucion/,
    /recovery-restitution-objectives/,
    /concurso-36-2012/,
    /lpb-insolvency/,
    /comunidad-instrumentalizacion/,
    /community-instrumentalisation/
  ];
  if (!targets.some((pattern) => pattern.test(path))) return;

  const isEs = path.includes('/es/');
  const isCalificacion = /calificacion-concurso-36-2012-vidas-paralelas|insolvency-classification-parallel-lives/.test(path);

  const style = document.createElement('style');
  style.textContent = `
    #${id}{background:#f4f1ea}
    #${id} .same-asset-box{max-width:1120px;margin:0 auto}
    #${id} .same-asset-allegation{background:#3c1715;color:#fff;border-radius:20px;padding:1.3rem 1.45rem;box-shadow:0 12px 30px rgba(19,37,45,.12)}
    #${id} .same-asset-label{display:block;font-size:.76rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#f1c6be;margin-bottom:.55rem}
    #${id} h2{margin:.15rem 0 .75rem;color:#fff}
    #${id} .same-asset-lead{font-size:1.05rem;line-height:1.55;margin:.2rem 0 1rem}
    #${id} .same-asset-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem;margin:1rem 0}
    #${id} .same-asset-grid div{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:13px;padding:.8rem}
    #${id} .same-asset-grid strong{display:block;margin-bottom:.25rem}
    #${id} .same-asset-control{background:#fff;color:#13252d;border-radius:13px;padding:.9rem 1rem;margin:.9rem 0}
    #${id} .same-asset-control strong{color:#8c2f2c}
    #${id} .same-asset-actions{display:flex;gap:.65rem;flex-wrap:wrap;margin-top:1rem}
    #${id} .same-asset-actions a{display:inline-block;border-radius:999px;padding:.65rem 1rem;font-weight:750;text-decoration:none;background:#fff;color:#13252d}
    #${id} .same-asset-actions a.secondary{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.55)}
    @media(max-width:850px){#${id} .same-asset-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.id = id;
  section.className = 'section';

  const calEs = `
    <div class="same-asset-control"><strong>Por qué pertenece a la Calificación.</strong> Si se atribuye a Gil Marer la generación o agravación de la insolvencia, el análisis causal no puede aislar esa acusación de las vidas posteriores del mismo hotel: obras, financiación, apoyo público, empleo, explotación y valor desarrollados mientras el perímetro LPB seguía bajo protección concursal. Debe determinarse qué conocieron y qué hicieron el Administrador Concursal, Fiscalía y Juzgado, y quién creó, preservó, desplazó o aprovechó valor.</div>`;
  const calEn = `
    <div class="same-asset-control"><strong>Why this belongs in the classification record.</strong> If Gil Marer is accused of generating or aggravating insolvency, causation cannot be isolated from the same hotel’s later lives: works, finance, public support, employment, operation and value developed while the LPB perimeter remained under insolvency protection. The record must establish what the Insolvency Administrator, Fiscalía and Court knew and did, and who created, preserved, displaced or benefited from value.</div>`;

  if (isEs) {
    section.innerHTML = `
      <div class="shell same-asset-box">
        <div class="same-asset-allegation">
          <span class="same-asset-label">ALEGACIÓN UNITARIA · 16 AGOSTO 2026 · NO HALLAZGO JUDICIAL</span>
          <h2>Mismo hotel, múltiples vidas financieras.</h2>
          <p class="same-asset-lead">Project Sun Rock alega doble o triple financiación y reutilización de una base sustancialmente coincidente —Hotel Sun Park/MYND Yaiza, activos, obras, costes, valor y empleo— entre el Concurso 36/2012, la Comunidad, RICPE/RIC, HNT, GC/836/P06, FEDER y la explotación actual. La separación jurídica de cada instrumento no sustituye una conciliación finca por finca, factura por factura, empleo por empleo y euro por euro.</p>
          <div class="same-asset-grid">
            <div><strong>20 julio 2021</strong>RICPE: 54 CAM, 190 LPB, 18 terceros; titularidad condicionada y DD incompleta.</div>
            <div><strong>€6.573.703,10</strong>Total RICPE/HNT atribuido al registro controlado; desglose exacto abierto.</div>
            <div><strong>€3.440.914,20 / 60</strong>Subvención y empleo publicados en GC/836/P06.</div>
            <div><strong>FEDER</strong>Identificado; porcentaje, gasto, pago y controles pendientes.</div>
          </div>
          ${isCalificacion ? calEs : ''}
          <div class="same-asset-control"><strong>Estado de prueba.</strong> La alegación es expresa y sustentada por anclajes documentales; no se presenta como resolución judicial, auditoría cerrada ni condena. Las capas alegadas de ≈€4,5m Comunidad, ≈€4,9m/≈86 empleos y ≈50 FTE requieren ingestión o reconciliación nativa completa.</div>
          <div class="same-asset-actions"><a href="/por-derecho/es/mismo-hotel-multiples-vidas-financieras/">Abrir el expediente unitario</a><a class="secondary" href="/por-derecho/es/ricpe-responsabilidad-documental/">Cadena de controles RICPE</a></div>
        </div>
      </div>`;
  } else {
    section.innerHTML = `
      <div class="shell same-asset-box">
        <div class="same-asset-allegation">
          <span class="same-asset-label">UNITARY ALLEGATION · 16 AUGUST 2026 · NOT A JUDICIAL FINDING</span>
          <h2>Same hotel, multiple financial lives.</h2>
          <p class="same-asset-lead">Project Sun Rock alleges double or triple funding and repeated use of a substantially overlapping base — Sun Park/MYND Yaiza hotel, assets, works, costs, value and employment — across Insolvency 36/2012, the Community, RICPE/RIC, HNT, GC/836/P06, ERDF and current operation. Legal separation of the instruments does not replace a property-by-property, invoice-by-invoice, job-by-job and euro-by-euro reconciliation.</p>
          <div class="same-asset-grid">
            <div><strong>20 July 2021</strong>RICPE: 54 CAM, 190 LPB, 18 third-party; conditional title and incomplete DD.</div>
            <div><strong>€6,573,703.10</strong>Attributed RICPE/HNT total in the controlled record; exact split open.</div>
            <div><strong>€3,440,914.20 / 60</strong>Published GC/836/P06 subsidy and employment commitment.</div>
            <div><strong>ERDF</strong>Identified; percentage, expenditure, payment and controls remain open.</div>
          </div>
          ${isCalificacion ? calEn : ''}
          <div class="same-asset-control"><strong>Evidence status.</strong> The allegation is express and supported by documentary anchors; it is not presented as a judicial finding, completed audit or conviction. The alleged ≈€4.5m Community, ≈€4.9m/≈86-job and ≈50-FTE layers require complete native ingestion or reconciliation.</div>
          <div class="same-asset-actions"><a href="/por-derecho/en/same-hotel-multiple-financial-lives/">Open the unitary record</a><a class="secondary" href="/por-derecho/en/ricpe-documentary-accountability/">RICPE control chain</a></div>
        </div>
      </div>`;
  }

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector(':scope > .hero, :scope > section.hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else main.insertAdjacentElement('afterbegin', section);
})();

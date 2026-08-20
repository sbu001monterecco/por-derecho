(() => {
  'use strict';

  const run = () => {
    const pathname = window.location.pathname.replace(/\/+$/, '');
    const isSpanish = /\/es(?:\/|$)/.test(pathname);
    const isEnglish = /\/en(?:\/|$)/.test(pathname);
    if (!isSpanish && !isEnglish) return;

    const canonical = isSpanish
      ? '/por-derecho/es/adjudicacion-2022-reconstruccion-documental/'
      : '/por-derecho/en/2022-adjudication-documentary-reconstruction/';
    const canonicalPath = canonical.replace(/\/+$/, '');
    const isCanonical = pathname === canonicalPath;

    const copy = isSpanish ? {
      versionTitle: 'Control de versiones, fuentes y uso previo',
      versionLead: 'Se conservan varias versiones internas no idénticas de estos trabajos. Versiones relacionadas fueron remitidas a asesores jurídicos en marzo de 2026. Esa circulación acredita consulta y conocimiento interno, pero no acredita por sí misma presentación judicial, admisión, debate ni decisión.',
      versionRule: 'La fuente de mayor rango controla: el Auto firmado de 25/01/2021 y el Edicto de 29/01/2021 corrigen la ontología de cifras; la escritura de 21/02/2022 sigue pendiente de re-vinculación primaria en esta revisión.',
      establishedTitle: 'Lo que sí queda establecido',
      established: [
        'El Auto de 25/01/2021 explica el paso de 3.079.104,66 € de demora al límite hipotecario de 3.182.000 € mediante devengo diario posterior.',
        'El Edicto de 29/01/2021 separa 13.168.082,02 € de componentes hipotecarios, 400.000 € de bienes no hipotecados y 1.145.798,29 € de cuotas comunitarias.',
        'Existe una propuesta documentada de un tercer oferente por 14,8 M€; su identidad se mantiene anonimizada en la publicación.'
      ],
      notEstablishedTitle: 'Lo que esas fuentes todavía no establecen',
      notEstablished: [
        'Que el umbral de un tercero fuera automáticamente el crédito concursal reconocido o la contraprestación de CAM.',
        'Que el tercer oferente cumpliera todos los requisitos, acreditara fondos o debiera resultar adjudicatario.',
        'El contenido exacto de la escritura de 21/02/2022 hasta re-vincular la copia primaria/certificada y su protocolo completo.'
      ],
      initialPublication: 'Publicación inicial: 19 agosto 2026',
      evidenceReview: 'Última revisión probatoria: 20 agosto 2026',
      correction: 'Corrección: funciones de las cifras, estado de la escritura y tercer oferente anonimizado',
      validationMatter: 'Jerarquía de fuentes y competencia',
      validationStatus: 'Auto y Edicto primarios localizados; propuesta de tercero documentada; escritura primaria pendiente de re-vinculación',
      validationNext: 'Completar autos definitivos, testimonios, escritura, cálculo de intereses, licitación, 400.000 € y rendición final',
      linkTitle: 'Reconstrucción de la adjudicación de 2022',
      linkAction: 'Abrir la reconstrucción documental →',
      cross: {
        valuation: 'Las valoraciones son piezas probatorias, pero no determinan por sí solas la adjudicación. La reconstrucción separa crédito reconocido, responsabilidad hipotecaria, umbral del tercer oferente, venta de 400.000 € y eventual contraprestación notarial.',
        perimeter: 'La continuidad CAM/JDAM → HNT/MYND debe separar control material, competencia real, adjudicación judicial, escritura, registro y sucesión societaria. Un tercer oferente documentó una propuesta de 14,8 M€; su tratamiento procesal sigue bajo reconstrucción.',
        finance: 'Las valoraciones, necesidades de inversión y fuentes de financiación posteriores aportan contexto y contraste; no convierten por sí solas el umbral competitivo o una oferta de tercero en precio jurídico de realización o remanente.',
        credit: 'Crédito concursal reconocido, límites hipotecarios, umbral exigido al tercer oferente y eventual deuda compensada en escritura son magnitudes distintas. La reconstrucción las sigue componente por componente.',
        premises: 'Los 400.000 € por bienes no hipotecados constituyen una línea separada de los componentes hipotecarios de 13.168.082,02 € y exigen su propio rastro bancario, contable, notarial y registral.',
        procedure: 'La propuesta documentada de un tercer oferente por 14,8 M€ convierte la competencia de 2021 en un punto de control real. El expediente debe mostrar su presentación, requisitos, licitación, desenlace y efecto para la masa.',
        generic: 'La página específica reconstruye oferta, competencia, crédito, autos, escritura, 400.000 € y cuentas sin convertir umbrales o hipótesis en conclusiones judiciales.'
      }
    } : {
      versionTitle: 'Version, source and prior-use control',
      versionLead: 'Several non-identical internal versions of this work are preserved. Related versions were circulated to legal advisers in March 2026. That circulation proves internal consultation and awareness, but does not by itself prove filing, admission, argument or judicial determination.',
      versionRule: 'The highest-ranked source controls: the signed 25 January 2021 order and 29 January court notice correct the number ontology; the 21 February 2022 deed still requires primary rebinding in this review.',
      establishedTitle: 'What is established',
      established: [
        'The 25 January 2021 order explains the move from EUR 3,079,104.66 in default interest to the EUR 3,182,000 mortgage cap through later daily accrual.',
        'The 29 January 2021 notice separates EUR 13,168,082.02 in mortgage components, EUR 400,000 for non-mortgaged assets and EUR 1,145,798.29 in community fees.',
        'A documented EUR 14.8m proposal by a third-party bidder exists; the bidder identity is anonymised in the public record.'
      ],
      notEstablishedTitle: 'What those sources do not yet establish',
      notEstablished: [
        'That a third-party threshold automatically became recognised insolvency credit or CAM consideration.',
        'That the third-party bidder met every condition, proved funds or should have received the adjudication.',
        'The exact content of the 21 February 2022 deed until the primary/certified copy and complete protocol are rebound.'
      ],
      initialPublication: 'Initial publication: 19 August 2026',
      evidenceReview: 'Latest evidence review: 20 August 2026',
      correction: 'Correction: legal functions of figures, deed source status and anonymised third-party bidder',
      validationMatter: 'Source hierarchy and competition',
      validationStatus: 'Primary order and notice located; third-party proposal documented; primary deed rebinding still open',
      validationNext: 'Complete final orders, testimonios, deed, interest calculation, licitation, EUR 400,000 and final accounts',
      linkTitle: 'The 2022 adjudication reconstruction',
      linkAction: 'Open the documentary reconstruction →',
      cross: {
        valuation: 'Valuations are evidential inputs, but do not by themselves determine the adjudication. The reconstruction separates recognised credit, mortgage liability, the third-party threshold, the EUR 400,000 sale and any later notarial consideration.',
        perimeter: 'CAM/JDAM → HNT/MYND continuity must distinguish physical control, real competition, judicial adjudication, deed, registration and corporate succession. A third-party bidder documented a EUR 14.8m proposal; its procedural treatment remains under reconstruction.',
        finance: 'Later valuations, investment needs and funding sources provide context and comparison; they do not by themselves convert a competitive threshold or third-party offer into the legally relevant realisation price or a surplus.',
        credit: 'Recognised insolvency credit, mortgage caps, the threshold imposed on a third-party bidder and any debt later set off in the deed are distinct quantities requiring component-by-component reconstruction.',
        premises: 'The EUR 400,000 non-mortgaged-assets line is separate from the EUR 13,168,082.02 mortgage components and requires its own banking, accounting, notarial and Registry trail.',
        procedure: 'The documented EUR 14.8m third-party proposal makes the 2021 competition a real control point. The file should show filing, conditions, licitation, outcome and estate effect.',
        generic: 'The dedicated page reconstructs offer, competition, credit, orders, deed, EUR 400,000 line and accounts without turning thresholds or hypotheses into judicial findings.'
      }
    };

    const addStyles = () => {
      if (document.getElementById('adjudicacion-provenance-styles')) return;
      const style = document.createElement('style');
      style.id = 'adjudicacion-provenance-styles';
      style.textContent = `
        .adjudicacion-provenance-panel{max-width:1120px;margin:0 auto}
        .adjudicacion-provenance-box{border-left:5px solid #536d79;background:#f4f8fa;border-radius:14px;padding:1rem 1.2rem}
        .adjudicacion-provenance-box h2,.adjudicacion-provenance-box h3{margin-top:0}
        .adjudicacion-provenance-columns{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem}
        .adjudicacion-provenance-columns>div{background:#fff;border:1px solid #d9dfdf;border-radius:12px;padding:.9rem}
        .adjudicacion-provenance-columns ul{margin-bottom:0}
        .adjudicacion-provenance-meta{display:flex;gap:.55rem;flex-wrap:wrap;margin-top:1rem}
        .adjudicacion-provenance-meta span{display:inline-block;border:1px solid #7b8c94;border-radius:999px;padding:.28rem .65rem;font-size:.82rem;font-weight:700}
        .adjudicacion-crosslink{max-width:1120px;margin:0 auto;border-left:5px solid #8c6b2f;background:#f3efe4;border-radius:14px;padding:1rem 1.2rem}
        .adjudicacion-crosslink h2{margin-top:0}
        .adjudicacion-crosslink p:last-child{margin-bottom:0}
        @media(max-width:800px){.adjudicacion-provenance-columns{grid-template-columns:1fr}}
      `;
      document.head.appendChild(style);
    };

    const insertCanonicalProvenance = () => {
      if (!isCanonical || document.getElementById('adjudicacion-version-control')) return;
      const main = document.querySelector('main');
      if (!main) return;
      addStyles();

      const section = document.createElement('section');
      section.className = 'section';
      section.id = 'adjudicacion-version-control';
      section.dataset.liveMarker = 'adjudicacion-version-control-20260820';
      section.innerHTML = `
        <div class="shell adjudicacion-provenance-panel">
          <div class="adjudicacion-provenance-box">
            <h2>${copy.versionTitle}</h2>
            <p>${copy.versionLead}</p>
            <p><strong>${copy.versionRule}</strong></p>
            <div class="adjudicacion-provenance-columns">
              <div><h3>${copy.establishedTitle}</h3><ul>${copy.established.map(item => `<li>${item}</li>`).join('')}</ul></div>
              <div><h3>${copy.notEstablishedTitle}</h3><ul>${copy.notEstablished.map(item => `<li>${item}</li>`).join('')}</ul></div>
            </div>
            <div class="adjudicacion-provenance-meta" aria-label="Publication and correction history">
              <span>${copy.initialPublication}</span>
              <span>${copy.evidenceReview}</span>
              <span>${copy.correction}</span>
            </div>
          </div>
        </div>`;

      const directSections = Array.from(main.children).filter(node => node.tagName === 'SECTION');
      const scopeSection = directSections.find(node => /Límite de esta página|Scope limit/.test(node.textContent || ''));
      if (scopeSection) scopeSection.insertAdjacentElement('afterend', section);
      else if (directSections[0]) directSections[0].insertAdjacentElement('afterend', section);
      else main.prepend(section);

      const validationHeading = Array.from(main.querySelectorAll('h2')).find(node => /Estado de validación|Validation status/.test(node.textContent || ''));
      const validationSection = validationHeading && validationHeading.closest('section');
      const tbody = validationSection && validationSection.querySelector('tbody');
      if (tbody && !tbody.querySelector('[data-adjudicacion-prior-use-row]')) {
        const row = document.createElement('tr');
        row.dataset.adjudicacionPriorUseRow = 'true';
        row.innerHTML = `<td>${copy.validationMatter}</td><td>${copy.validationStatus}</td><td>${copy.validationNext}</td>`;
        tbody.appendChild(row);
      }
    };

    const routeType = () => {
      const rules = [
        [/actua-2018|valoracion|valuation|gesvalt/i, 'valuation'],
        [/acosta-matos-perimetro|acosta-matos-perimeter/i, 'perimeter'],
        [/ricpe-responsabilidad-documental|ricpe-documentary-accountability|ric-private-equity-sun-park/i, 'finance'],
        [/acreedor-de-registro|lender-of-record/i, 'credit'],
        [/locales|premises/i, 'premises'],
        [/administrador-concursal|insolvency-administrator|articulo-1535|article-1535|ingenieria-inversa-360|reverse-engineering-360|calificacion-concurso-36-2012|insolvency-36-2012/i, 'procedure']
      ];
      const match = rules.find(([pattern]) => pattern.test(pathname));
      if (match) return match[1];
      const text = document.body ? document.body.innerText : '';
      if (/400[.,]000/.test(text) && /locales|premises|unencumbered/i.test(text)) return 'premises';
      if (/13[.,]168[.,]082|protocolo 457|protocol 457/i.test(text)) return 'generic';
      return null;
    };

    const insertCrossLink = () => {
      if (isCanonical || document.querySelector('[data-adjudicacion-crosslink]')) return;
      const type = routeType();
      if (!type) return;
      const main = document.querySelector('main');
      if (!main) return;
      addStyles();

      const section = document.createElement('section');
      section.className = 'section adjudicacion-crosslink-section';
      section.dataset.adjudicacionCrosslink = type;
      section.dataset.liveMarker = 'adjudicacion-crosslink-20260820';
      section.innerHTML = `
        <div class="shell">
          <aside class="adjudicacion-crosslink" role="note">
            <h2>${copy.linkTitle}</h2>
            <p>${copy.cross[type] || copy.cross.generic}</p>
            <p><a class="button secondary" href="${canonical}">${copy.linkAction}</a></p>
          </aside>
        </div>`;

      const hero = main.querySelector(':scope > .hero, :scope > .dossier-hero, :scope > section.hero, :scope > section.dossier-hero');
      if (hero) hero.insertAdjacentElement('afterend', section);
      else if (main.firstElementChild) main.firstElementChild.insertAdjacentElement('afterend', section);
      else main.appendChild(section);
    };

    insertCanonicalProvenance();
    insertCrossLink();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
})();

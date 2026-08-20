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
      versionRule: 'La fuente de mayor rango controla: el Auto firmado de 25/01/2021, el Edicto de 29/01/2021 y la escritura n.º 457 de 21/02/2022 están ahora vinculados como fuentes primarias. La escritura verifica 13.168.082,02 € como deuda que sirve de contraprestación de la dación; no verifica por sí sola que esa sea la cuantía jurídicamente correcta del crédito privilegiado final.',
      establishedTitle: 'Lo que sí queda establecido',
      established: [
        'El Auto de 25/01/2021 explica el paso de 3.079.104,66 € de demora al límite hipotecario de 3.182.000 € mediante devengo diario posterior.',
        'El Edicto de 29/01/2021 separa 13.168.082,02 € de componentes hipotecarios, 400.000 € de bienes no hipotecados y 1.145.798,29 € de cuotas comunitarias.',
        'La escritura n.º 457 de 21/02/2022 verifica 13.168.082,02 € como deuda que sirve de contraprestación de la dación de las fincas hipotecadas.',
        'Existe una propuesta documentada de un tercer oferente por 14,8 M€; únicamente su nombre se mantiene anonimizado en la publicación y la oferta y su contexto permanecen visibles.'
      ],
      notEstablishedTitle: 'Lo que esas fuentes todavía no establecen',
      notEstablished: [
        'Que el umbral de un tercero se convirtiera automáticamente y sin puente jurídico adicional en crédito concursal definitivamente reconocido.',
        'Que el tercer oferente cumpliera todos los requisitos, acreditara fondos o debiera resultar adjudicatario.',
        'Que la escritura n.º 457 cure por sí sola la compraventa de locales/piscinas de 2018 no convalidada en 2019 o reconcilie automáticamente los 400.000 €.',
        'Que las cancelaciones, pagos, comunicación al Juzgado y rendición final se ejecutaran exactamente como se prevé en la escritura sin sus fuentes posteriores.'
      ],
      initialPublication: 'Publicación inicial: 19 agosto 2026',
      evidenceReview: 'Última revisión probatoria: 20 agosto 2026',
      correction: 'Corrección: escritura primaria recuperada; funciones de cifras y nombre del tercer oferente anonimizado',
      validationMatter: 'Jerarquía de fuentes y competencia',
      validationStatus: 'Auto, Edicto y escritura primaria localizados; propuesta de tercero documentada y únicamente su nombre anonimizado públicamente',
      validationNext: 'Completar autos definitivos, testimonios, cálculo de intereses, licitación, 400.000 €, comunicación/Registro y rendición final',
      linkTitle: 'Reconstrucción de la adjudicación de 2022',
      linkAction: 'Abrir la reconstrucción documental →',
      cross: {
        valuation: 'La escritura n.º 457 verifica 13.168.082,02 € como deuda que sirve de contraprestación de la dación. Eso no convierte por sí solo responsabilidad hipotecaria, tasación o umbral competitivo en crédito concursal definitivamente correcto: cada función debe reconciliarse.',
        perimeter: 'La continuidad CAM/JDAM → HNT/MYND debe separar control material, competencia real, adjudicación, escritura, Registro y sucesión societaria. La escritura n.º 457 cierra la dación de fincas hipotecadas, no responde automáticamente al problema separado de locales/piscinas y 400.000 €.',
        finance: 'Las valoraciones, necesidades de inversión y fuentes de financiación posteriores aportan contexto. La escritura verifica la deuda declarada como contraprestación de la dación; no resuelve por sí sola su clasificación concursal, el proceso competitivo ni un eventual remanente.',
        credit: 'Crédito reconocido, límites hipotecarios, umbral exigido al tercer oferente y deuda declarada como contraprestación en escritura son magnitudes jurídicamente distintas, aunque dos fuentes usen la misma cifra de 13.168.082,02 €.',
        premises: 'Los 400.000 € por bienes no hipotecados constituyen una línea separada. Las secciones operativas revisadas de la escritura n.º 457 tratan la dación de fincas hipotecadas y no suministran por sí solas la conciliación del negocio de locales/piscinas de 2018.',
        procedure: 'La propuesta documentada de un tercer oferente por 14,8 M€ convierte la competencia de 2021 en un punto de control real. La escritura añade otro control: debía comunicarse al Juzgado en cinco días naturales y activar la cadena de cancelación que ahora debe trazarse.',
        generic: 'La página específica reconstruye oferta, competencia, deuda, Autos, escritura primaria, 400.000 €, Registro y cuentas sin convertir una coincidencia numérica en conclusión jurídica automática.'
      }
    } : {
      versionTitle: 'Version, source and prior-use control',
      versionLead: 'Several non-identical internal versions of this work are preserved. Related versions were circulated to legal advisers in March 2026. That circulation proves internal consultation and awareness, but does not by itself prove filing, admission, argument or judicial determination.',
      versionRule: 'The highest-ranked source controls: the signed 25 January 2021 order, the 29 January court notice and deed no. 457 dated 21 February 2022 are now bound as primary sources. The deed verifies EUR 13,168,082.02 as debt serving as consideration for the dación; it does not by itself verify that amount as the legally correct final privileged credit.',
      establishedTitle: 'What is established',
      established: [
        'The 25 January 2021 order explains the move from EUR 3,079,104.66 in default interest to the EUR 3,182,000 mortgage cap through later daily accrual.',
        'The 29 January 2021 notice separates EUR 13,168,082.02 in mortgage components, EUR 400,000 for non-mortgaged assets and EUR 1,145,798.29 in community fees.',
        'Deed no. 457 dated 21 February 2022 verifies EUR 13,168,082.02 as debt serving as consideration for the dación of the mortgaged properties.',
        "A documented EUR 14.8m proposal by a third-party bidder exists; only the bidder's name is anonymised in the public record and the bid and its context remain visible."
      ],
      notEstablishedTitle: 'What those sources do not yet establish',
      notEstablished: [
        'That a third-party threshold automatically became finally recognised insolvency credit without an additional legal bridge.',
        'That the third-party bidder met every condition, proved funds or should have received the adjudication.',
        'That deed no. 457 automatically cured the separate 2018 premises/pools transaction that was not validated in 2019 or reconciled the EUR 400,000.',
        'That cancellations, payments, court communication and final accounts occurred exactly as contemplated without their downstream sources.'
      ],
      initialPublication: 'Initial publication: 19 August 2026',
      evidenceReview: 'Latest evidence review: 20 August 2026',
      correction: 'Correction: primary deed recovered; legal functions of figures and anonymised third-party bidder name',
      validationMatter: 'Source hierarchy and competition',
      validationStatus: 'Primary order, notice and deed located; third-party proposal documented and only its name publicly anonymised',
      validationNext: 'Complete final orders, testimonios, interest calculation, licitation, EUR 400,000, court/Registry chain and final accounts',
      linkTitle: 'The 2022 adjudication reconstruction',
      linkAction: 'Open the documentary reconstruction →',
      cross: {
        valuation: 'Deed no. 457 verifies EUR 13,168,082.02 as debt serving as consideration for the dación. That does not by itself transform mortgage liability, appraisal or the competitive threshold into finally correct recognised insolvency credit; each function must be reconciled.',
        perimeter: 'CAM/JDAM → HNT/MYND continuity must distinguish physical control, real competition, adjudication, deed, registration and corporate succession. Deed no. 457 closes the mortgaged-property dación; it does not automatically answer the separate premises/pools and EUR 400,000 issue.',
        finance: 'Later valuations, investment needs and funding sources provide context. The deed verifies the debt stated as consideration for the dación; it does not by itself resolve insolvency classification, the competitive process or any residual.',
        credit: 'Recognised credit, mortgage caps, the threshold imposed on a third-party bidder and debt stated as consideration in the deed are legally distinct quantities even where two sources use the same EUR 13,168,082.02 figure.',
        premises: 'The EUR 400,000 non-mortgaged-assets line remains separate. The reviewed operative portions of deed no. 457 address the mortgaged-property dación and do not by themselves reconcile the 2018 premises/pools transaction.',
        procedure: 'The documented EUR 14.8m third-party proposal makes the 2021 competition a real control point. The deed adds another: it required communication to the court within five calendar days and set out a cancellation route that now needs to be traced.',
        generic: 'The dedicated page reconstructs offer, competition, debt, orders, the primary deed, EUR 400,000 line, Registry and accounts without turning numerical identity into an automatic legal conclusion.'
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

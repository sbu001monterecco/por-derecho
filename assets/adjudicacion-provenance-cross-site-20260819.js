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
      versionTitle: 'Control de versiones y uso previo',
      versionLead: 'Se conservan varias versiones internas no idénticas de estos trabajos. Versiones relacionadas fueron remitidas a asesores jurídicos en marzo de 2026. Esa circulación acredita consulta y conocimiento interno, pero no acredita por sí misma presentación judicial, admisión, debate ni decisión.',
      versionRule: 'La eventual novedad procesal de cada hecho o argumento debe comprobarse frente al expediente judicial, los escritos anteriores y las resoluciones dictadas.',
      establishedTitle: 'Lo que sí queda establecido',
      established: [
        'Existen versiones internas distintas y su procedencia se conserva separadamente.',
        'Versiones relacionadas circularon entre asesores jurídicos en marzo de 2026.',
        'La reconstrucción pública incorpora las correcciones derivadas de las fuentes primarias.'
      ],
      notEstablishedTitle: 'Lo que no queda establecido por esa circulación',
      notEstablished: [
        'Que alguna versión fuera presentada, admitida, debatida o resuelta judicialmente.',
        'Que todos los hechos o argumentos fueran procesalmente nuevos en 2026.',
        'Que los asesores respaldaran las conclusiones o remedios propuestos.'
      ],
      initialPublication: 'Publicación inicial: 19 agosto 2026',
      evidenceReview: 'Última revisión probatoria: 19 agosto 2026',
      correction: 'Corrección: procedencia y circulación previa de versiones no idénticas',
      validationMatter: 'Versiones y uso previo',
      validationStatus: 'Versiones relacionadas remitidas a asesores; presentación o uso judicial no acreditados',
      validationNext: 'Comparar versión por versión con el expediente, escritos anteriores, correspondencia y resoluciones',
      linkTitle: 'Reconstrucción de la adjudicación de 2022',
      linkAction: 'Abrir la reconstrucción documental →',
      cross: {
        valuation: 'La metodología y representatividad de ACTÚA o de otras valoraciones son piezas probatorias, pero no determinan por sí solas la nulidad de la adjudicación. La oferta, la deuda, la escritura y las cuentas deben conciliarse por separado.',
        perimeter: 'La continuidad CAM/JDAM → HNT/MYND debe separar control material, adjudicación judicial, escritura, registro y sucesión societaria. La reconstrucción de 2022 fija esas fronteras.',
        finance: 'Las valoraciones, necesidades de inversión y fuentes de financiación posteriores aportan contexto y contraste; no prueban por sí solas el importe jurídico de realización ni un remanente concursal.',
        credit: 'La clasificación concursal del crédito, los límites hipotecarios y la deuda utilizada como contraprestación en 2022 son magnitudes distintas que deben reconstruirse componente por componente.',
        premises: 'La venta de fincas no hipotecadas por 400.000 € constituye una línea separada de la dación de los 159 apartamentos hipotecados y exige su propio rastro bancario, contable y registral.',
        procedure: 'La reconstrucción de 2022 muestra por qué no existe un remedio universal para todo el perímetro: cada acto, consecuencia y titular afectado requiere su propio análisis procesal.',
        generic: 'La página específica concilia la oferta, el crédito, el auto, la escritura, los 400.000 € y las cuentas sin convertir hipótesis internas en conclusiones judiciales.'
      }
    } : {
      versionTitle: 'Version control and prior use',
      versionLead: 'Several non-identical internal versions of this work are preserved. Related versions were circulated to legal advisers in March 2026. That circulation proves internal consultation and awareness, but does not by itself prove filing, admission, argument or judicial determination.',
      versionRule: 'The procedural novelty of each fact or argument must be tested against the court record, previous submissions and existing decisions.',
      establishedTitle: 'What is established',
      established: [
        'Different internal versions exist and their provenance is preserved separately.',
        'Related versions circulated among legal advisers in March 2026.',
        'The public reconstruction incorporates corrections required by the primary sources.'
      ],
      notEstablishedTitle: 'What that circulation does not establish',
      notEstablished: [
        'That any version was filed, admitted, argued or judicially decided.',
        'That every fact or argument was procedurally new in 2026.',
        'That the advisers endorsed the proposed conclusions or remedies.'
      ],
      initialPublication: 'Initial publication: 19 August 2026',
      evidenceReview: 'Latest evidence review: 19 August 2026',
      correction: 'Correction: provenance and prior circulation of non-identical versions',
      validationMatter: 'Draft versions and prior use',
      validationStatus: 'Related versions sent to advisers; filing or judicial use not established',
      validationNext: 'Compare every version with the court docket, previous submissions, correspondence and decisions',
      linkTitle: 'The 2022 adjudication reconstruction',
      linkAction: 'Open the documentary reconstruction →',
      cross: {
        valuation: 'The methodology and representativeness of ACTÚA or other valuations are evidential inputs, but do not by themselves determine nullity. The offer, debt, deed and accounts must be reconciled separately.',
        perimeter: 'The CAM/JDAM → HNT/MYND continuity must distinguish physical control, judicial adjudication, deed, registration and corporate succession. The 2022 reconstruction fixes those boundaries.',
        finance: 'Later valuations, investment needs and funding sources provide context and comparison; they do not by themselves prove the legally relevant realisation amount or an insolvency surplus.',
        credit: 'The insolvency classification of the credit, mortgage caps and the debt used as consideration in 2022 are distinct quantities requiring component-by-component reconstruction.',
        premises: 'The EUR 400,000 sale of unencumbered properties is a separate line from the dación of the 159 mortgaged apartments and requires its own banking, accounting and register trail.',
        procedure: 'The 2022 reconstruction shows why there is no universal remedy for the whole perimeter: each act, consequence and affected right-holder requires its own procedural analysis.',
        generic: 'The dedicated page reconciles the offer, credit, order, deed, EUR 400,000 line and accounts without turning internal hypotheses into judicial findings.'
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
      section.dataset.liveMarker = 'adjudicacion-version-control-20260819';
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
      section.dataset.liveMarker = 'adjudicacion-crosslink-20260819';
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

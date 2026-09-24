(() => {
  const current = document.currentScript;
  if (!current) return;

  // Preserve the site's established loader unchanged, but move it behind this thin wrapper.
  const base = document.createElement('script');
  base.src = new URL('site-base-20260819.js?v=20260819a', current.src).href;
  base.async = false;
  document.head.appendChild(base);

  // Unitary case navigation, CE-001–CE-010 tracker, visible corrections and compact context gateway.
  const caseArchitecture = document.createElement('script');
  caseArchitecture.src = new URL('case-information-architecture-20260819.js?v=20260819b', current.src).href;
  caseArchitecture.async = false;
  caseArchitecture.setAttribute('data-case-information-architecture-loader', 'true');
  document.head.appendChild(caseArchitecture);

  const unitaryCriminal=document.createElement('script');
  unitaryCriminal.src=new URL('unitary-criminal-reverse-engineering-20260820.js?v=20260820a',current.src).href;
  unitaryCriminal.async=false;
  unitaryCriminal.setAttribute('data-unitary-criminal-loader','unitary-criminal-reverse-engineering-20260820');
  document.head.appendChild(unitaryCriminal);

  // Correct the San Telmo speaker attribution on the bilingual homepages without changing the retained image.
  const attribution = document.createElement('script');
  attribution.src = new URL('san-telmo-attribution-correction-20260819.js?v=20260819a', current.src).href;
  attribution.async = false;
  attribution.setAttribute('data-san-telmo-attribution-loader', 'true');
  document.head.appendChild(attribution);

  // Keep the 2022 adjudication reconstruction source-controlled across relevant pages.
  // Public treatment deliberately refers only to an anonymised third-party bidder.
  const adjudication = document.createElement('script');
  adjudication.src = new URL('adjudicacion-provenance-cross-site-20260819.js?v=20260820a', current.src).href;
  adjudication.async = false;
  adjudication.setAttribute('data-adjudicacion-provenance-loader', 'true');
  document.head.appendChild(adjudication);

  // Cross-site source-controlled reconstruction of Community/private functional management,
  // AC authorisation/reliance, mobile Community debt and the definitive-text incident answer.
  const deFactoAdministration = document.createElement('script');
  deFactoAdministration.src = new URL('ac-community-de-facto-administration-20260820.js?v=20260820b', current.src).href;
  deFactoAdministration.async = false;
  deFactoAdministration.setAttribute('data-ac-community-de-facto-loader', 'true');
  document.head.appendChild(deFactoAdministration);

  // Stronger attributed-allegation visibility layer. It upgrades the existing panels rather than
  // creating a competing narrative, and adds route-specific relevance across governance, AC,
  // material control, liquidation, judicial, implementation and downstream-reliance pages.
  const deFactoVisibility = document.createElement('script');
  deFactoVisibility.src = new URL('ac-de-facto-knowing-facilitation-visibility-20260820.js?v=20260820b', current.src).href;
  deFactoVisibility.async = false;
  deFactoVisibility.setAttribute('data-ac-de-facto-knowing-facilitation-visibility-loader', 'true');
  document.head.appendChild(deFactoVisibility);

  // Preserve the base-module markers on the upgraded panels and remove any duplicate caused by
  // delayed cross-site reruns. This keeps one canonical allegation panel per relevant route.
  const deFactoVisibilityStability = document.createElement('script');
  deFactoVisibilityStability.src = new URL('ac-de-facto-knowing-facilitation-stability-20260820.js?v=20260820b', current.src).href;
  deFactoVisibilityStability.async = false;
  deFactoVisibilityStability.setAttribute('data-ac-de-facto-knowing-facilitation-stability-loader', 'true');
  document.head.appendChild(deFactoVisibilityStability);

  // Propagate the verified 20-Aug-2026 CNMV email/REGAGE state across the connected RICPE,
  // Orion, Portfolio and professional-custody routes without duplicating the canonical record.
  const cnmvRegageStatus = document.createElement('script');
  cnmvRegageStatus.src = new URL('cnmv-regage-status-cross-site-20260820.js?v=20260820a', current.src).href;
  cnmvRegageStatus.async = false;
  cnmvRegageStatus.setAttribute('data-cnmv-regage-status-loader', 'true');
  document.head.appendChild(cnmvRegageStatus);

  const isPalacete = /\/es\/fundacion-por-derecho\/palacete-por-derecho\/?(?:index\.html)?$/.test(window.location.pathname);
  if (!isPalacete) return;

  const style = document.createElement('style');
  style.textContent = `
    .pd-visual-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.15rem;margin:2.2rem 0 1rem}
    .pd-visual{margin:0;background:#fff;border:1px solid rgba(24,37,42,.14);border-radius:1rem;overflow:hidden;box-shadow:0 18px 45px rgba(20,30,35,.08)}
    .pd-visual img{display:block;width:100%;height:auto}
    .pd-visual figcaption{padding:1rem 1.1rem;font-size:.82rem;line-height:1.55;color:#536268}
    .pd-visual-tag{display:block;margin-bottom:.4rem;text-transform:uppercase;letter-spacing:.1em;font-size:.67rem;font-weight:800;color:#8a6a3d}
    .pd-visual-note{font-size:.82rem;line-height:1.6;color:#657278;max-width:58rem;margin:1rem 0 0}
    .pd-concept-vision{margin-top:2.5rem;padding-top:2rem;border-top:1px solid rgba(24,37,42,.14)}
    .pd-concept-vision h3{font-family:Georgia,'Times New Roman',serif;font-size:clamp(1.7rem,3vw,2.7rem);line-height:1.1;color:#18252a;margin:.3rem 0 .8rem}
    .pd-concept-vision>p{max-width:58rem;line-height:1.7;color:#405159}
    .pd-concept-vision .pd-visual{background:#102a33;border-color:rgba(168,130,72,.38)}
    .pd-concept-vision .pd-visual figcaption{color:rgba(255,255,255,.84)}
    .pd-concept-vision .pd-visual-tag{color:#e5cfa5}
    @media(max-width:700px){.pd-visual-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const inject = () => {
    const bio = document.querySelector('#biografia .pd-intro');
    if (bio && !document.querySelector('.pd-history-visuals')) {
      bio.insertAdjacentHTML('afterend', `
        <div class="pd-history-visuals">
          <div class="pd-visual-grid" aria-label="Memoria visual histórica de San Bernardo 27">
            <figure class="pd-visual">
              <img src="../../../assets/palacete-san-bernardo-historica-marco.webp" width="520" height="691" loading="eager" alt="Fotografía real del cuadro histórico conservado en San Bernardo 27">
              <figcaption><span class="pd-visual-tag">Memoria visual · fotografía real</span>La imagen histórica tal como se conserva y se muestra dentro de San Bernardo 27. Su presencia física en la casa forma parte de la memoria que queremos recibir y preservar.</figcaption>
            </figure>
            <figure class="pd-visual">
              <img src="../../../assets/palacete-san-bernardo-historica-detalle.webp" width="520" height="691" loading="eager" alt="Detalle de la fotografía histórica conservada en San Bernardo 27">
              <figcaption><span class="pd-visual-tag">Archivo familiar · detalle</span>Acercamiento a la fotografía antigua. La identificación exacta de la casa representada, la fecha y su relación con la historia familiar se confirmarán con la familia antes de cualquier versión pública definitiva.</figcaption>
            </figure>
          </div>
          <p class="pd-visual-note"><strong>Dos niveles de evidencia, sin mezclarlos:</strong> estas son fotografías reales del material histórico conservado en el inmueble. No son recreaciones ni imágenes generadas. La interpretación histórica de lo que aparece permanece abierta a la validación de la familia y de fuentes documentales adicionales.</p>
        </div>`);
    }

    const use = document.querySelector('#uso .pd-use-grid');
    if (use && !document.querySelector('.pd-concept-vision')) {
      use.insertAdjacentHTML('afterend', `
        <div class="pd-concept-vision" id="vision-conceptual">
          <p class="pd-kicker">Visión de futuro</p>
          <h3>Imaginar el futuro sin confundirlo con el presente.</h3>
          <p>Estos estudios visuales exploran cómo San Bernardo podría convertirse en una casa institucional de estándar internacional: gravedad de Mayfair y Belgravia, disciplina de la City, energía intelectual y tecnológica de Manhattan y una identidad canaria y atlántica inequívoca. La azotea se plantea como un espacio funcional de trabajo, conversación, lectura, descanso y vida institucional.</p>
          <div class="pd-visual-grid" aria-label="Estudios conceptuales de Palacete Por Derecho">
            <figure class="pd-visual">
              <img src="../../../assets/palacete-por-derecho-vision-01.webp" width="700" height="467" loading="lazy" alt="Estudio conceptual del futuro uso de San Bernardo 27 por Fundación Por Derecho">
              <figcaption><span class="pd-visual-tag">Visualización conceptual · no aprobada</span>Estudio de visión sobre el edificio real y su entorno: biblioteca, Salón San Bernardo, Sala de Trazabilidad, Patronato, jardín y azotea funcional.</figcaption>
            </figure>
            <figure class="pd-visual">
              <img src="../../../assets/palacete-por-derecho-vision-02.webp" width="700" height="394" loading="lazy" alt="Segundo estudio conceptual del futuro Palacete Por Derecho">
              <figcaption><span class="pd-visual-tag">Estudio de uso · no representa el estado actual</span>Exploración del Palacete Por Derecho como casa embajadorial, académica y tecnológica: el frente para recibir, el corazón para pensar y gobernar, y la infraestructura digital y de IA casi invisible.</figcaption>
            </figure>
          </div>
          <p class="pd-visual-note"><strong>Límite:</strong> estas imágenes son herramientas de pensamiento y comunicación. No representan una obra autorizada, un proyecto arquitectónico aprobado, una distribución definitiva ni el estado actual del inmueble o del espacio público circundante.</p>
        </div>`);
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject, { once: true });
  } else {
    inject();
  }
})();

// PD-RECOVERY-BRIDGE-CRIMINAL-FILINGS-20260906
// Reconstructed additive bridge, not the missing original September loader.
// The preceding preserved loader and the two source-qualified modules are unchanged.
(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const entries = [
    ['criminal-filings-corpus-interlink-20260904.js', 'data-criminal-filings-corpus-interlink-loader'],
    ['criminal-filings-corpus-search-extension-20260904.js', 'data-criminal-filings-corpus-search-loader']
  ];
  for (const [file, marker] of entries) {
    const url = new URL(file + '?v=20260904a', current.src);
    const loaded = Array.from(document.scripts).some(s => {
      try { return s.src && new URL(s.src, current.src).pathname === url.pathname; }
      catch (_) { return false; }
    });
    if (loaded || document.querySelector('script[' + marker + ']')) continue;
    const script = document.createElement('script');
    script.src = url.href;
    script.async = false;
    script.setAttribute(marker, '20260904a');
    document.head.appendChild(script);
  }
})();

// PD-RECORDING-EVIDENCE-CONTINUITY-20260909
// Canonical 10-Jun-2016 date/provenance/completeness correction for the existing bilingual reader.
(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const url = new URL('recording-evidence-continuity-20260909.js?v=20260909a', current.src);
  const loaded = Array.from(document.scripts).some(script => {
    try { return script.src && new URL(script.src, current.src).pathname === url.pathname; }
    catch (_) { return false; }
  });
  if (loaded || document.querySelector('script[data-recording-evidence-continuity-loader]')) return;
  const script = document.createElement('script');
  script.src = url.href;
  script.async = false;
  script.setAttribute('data-recording-evidence-continuity-loader', '20260909a');
  document.head.appendChild(script);
})();

// PD-CAIXABANK-RAMIFICATIONS-20260909
// Source-statused first-read module for the CaixaBank Valencia claim and recovery routes.
(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const url = new URL('caixabank-borja-witness-context-20260816.js?v=20260909b', current.src);
  const loaded = Array.from(document.scripts).some(script => {
    try { return script.src && new URL(script.src, current.src).pathname === url.pathname; }
    catch (_) { return false; }
  });
  if (loaded || document.querySelector('script[data-caixabank-ramifications-loader]')) return;
  const script = document.createElement('script');
  script.src = url.href;
  script.async = false;
  script.setAttribute('data-caixabank-ramifications-loader', '20260909b');
  document.head.appendChild(script);
})();

// PD-SUN-PARK-HISTORY-20260910
// Source-controlled History/homepage bridge: hotel geometry, ownership chain, ^ links and material-source viewers.
(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const url = new URL('sun-park-history-bridge-20260910.js?v=20260910a', current.src);
  const loaded = Array.from(document.scripts).some(script => {
    try { return script.src && new URL(script.src, current.src).pathname === url.pathname; }
    catch (_) { return false; }
  });
  if (loaded || document.querySelector('script[data-sun-park-history-bridge-loader]')) return;
  const script = document.createElement('script');
  script.src = url.href;
  script.async = false;
  script.setAttribute('data-sun-park-history-bridge-loader', '20260910a');
  document.head.appendChild(script);
})();

// PD-UNITARY-RECOVERY-OS-CROSS-SITE-20260910
// Loads the already source-controlled recovery operating system only on relevant case routes.
// The bridge adds contextual CAM/HNT, RICPE, authority-routing and prosecutor-first deep links;
// it does not send, file, restrain, decide or promote a candidate action.
(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const url = new URL('recovery-operating-system-cross-site-20260910.js?v=20260910b', current.src);
  const loaded = Array.from(document.scripts).some(script => {
    try { return script.src && new URL(script.src, current.src).pathname === url.pathname; }
    catch (_) { return false; }
  });
  if (loaded || document.querySelector('script[data-recovery-os-cross-site-loader]')) return;
  const script = document.createElement('script');
  script.src = url.href;
  script.async = false;
  script.setAttribute('data-recovery-os-cross-site-loader', '20260910b');
  document.head.appendChild(script);
})();

// PD-SUN-PARK-VALUATION-OFFER-INTERCONNECT-20260910
// Additive cross-site module. Keeps prior audited loaders intact while propagating the corrected
// 262-finca topology, ACTÚA/GESVALT incident, CAM-offer/Plan route and source-status boundaries across connected pages.
(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const url = new URL('sun-park-valuation-offer-interconnect-20260910.js?v=20260910a', current.src);
  const loaded = Array.from(document.scripts).some(script => {
    try { return script.src && new URL(script.src, current.src).pathname === url.pathname; }
    catch (_) { return false; }
  });
  if (loaded || document.querySelector('script[data-sun-park-valuation-offer-interconnect-loader]')) return;
  const script = document.createElement('script');
  script.src = url.href;
  script.async = false;
  script.setAttribute('data-sun-park-valuation-offer-interconnect-loader', '20260910a');
  document.head.appendChild(script);
})();

// PD-CAM-OFFER-PLAN-EXECUTION-DOCUMENT-ROOM-20260911
// Adds a source-room overlay to the offer/Plan, 2022 execution, CAM-filings and Concurso 36/2012 routes.
// It distinguishes recovered primary sources from public-safe derivatives and unresolved downstream proof.
(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const url = new URL('cam-offer-plan-execution-document-room-20260911.js?v=20260911a', current.src);
  const loaded = Array.from(document.scripts).some(script => {
    try { return script.src && new URL(script.src, current.src).pathname === url.pathname; }
    catch (_) { return false; }
  });
  if (loaded || document.querySelector('script[data-cam-offer-plan-execution-document-room-loader]')) return;
  const script = document.createElement('script');
  script.src = url.href;
  script.async = false;
  script.setAttribute('data-cam-offer-plan-execution-document-room-loader', '20260911a');
  document.head.appendChild(script);
})();

// PD-EU-DIRECTIVE-2026-1021-CONTINUITY-20260911
// Additive current-EU-law discovery and finite reciprocal context. The modules are self-limiting,
// preserve historical-law/non-retroactivity boundaries, and do not create a merits or jurisdiction finding.
(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const entries = [
    ['eu-directive-2026-1021-crosslink-20260911.js?v=20260911b', 'data-eu-directive-2026-1021-crosslink-loader'],
    ['eu-directive-2026-1021-search-extension-20260911.js?v=20260911b', 'data-eu-directive-2026-1021-search-loader']
  ];
  for (const [file, marker] of entries) {
    const url = new URL(file, current.src);
    const loaded = Array.from(document.scripts).some(script => {
      try { return script.src && new URL(script.src, current.src).pathname === url.pathname; }
      catch (_) { return false; }
    });
    if (loaded || document.querySelector(`script[${marker}]`)) continue;
    const script = document.createElement('script');
    script.src = url.href;
    script.async = false;
    script.setAttribute(marker, '20260911b');
    document.head.appendChild(script);
  }
})();

 // PD-SECURITY-IMPAIRMENT-CAUSATION-20260924:START
(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const path = window.location.pathname;
  if (!/(7-junio|7-june|salida-financiada|funded-ona|ona-hotels|acreedor|lender-of-record|administrador-concursal-puerta-credito|insolvency-administrator-credit-to-title|adjudicacion-2022|2022-adjudication|cexp-(?:cadena|operation)|comunidad-instrumentalizacion|community-instrumentalisation|control-material|material-control|masa-activa|active-estate|oferta-acosta-matos|offer-liquidation-plan|garantia-deterioro|security-impairment)/i.test(path)) return;
  const url = new URL('security-impairment-track-20260924.js?v=20260924b', current.src);
  if (document.querySelector('script[data-security-impairment-track-loader]')) return;
  const s = document.createElement('script');
  s.src = url.href;
  s.async = false;
  s.setAttribute('data-security-impairment-track-loader', '20260924b');
  document.head.appendChild(s);
})();
// PD-SECURITY-IMPAIRMENT-CAUSATION-20260924:END

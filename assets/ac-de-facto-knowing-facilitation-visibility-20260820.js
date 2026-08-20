(() => {
  'use strict';

  const VERSION = '20260820b';

  const run = () => {
    const pathname = window.location.pathname.replace(/\/+$/, '/');
    const isEs = pathname.includes('/por-derecho/es/');
    const isEn = pathname.includes('/por-derecho/en/');
    if (!isEs && !isEn) return;

    const base = '/por-derecho';
    const canonical = isEs
      ? `${base}/es/administracion-de-hecho-comunidad-ac/`
      : `${base}/en/de-facto-administration-community-ac/`;
    const corrections = isEs
      ? `${base}/es/correcciones-control-versiones/`
      : `${base}/en/corrections-version-control/`;
    const isCanonical = pathname === canonical;
    const isHome = pathname === `${base}/${isEs ? 'es' : 'en'}/`;
    const isUpdates = /\/(actualizaciones|updates)\//.test(pathname);
    const isControlRoom = /\/(sala-control-caso|case-control-room)\//.test(pathname);
    const isCriminalHub = /\/(ingenieria-forense-criminal-sun-park|sun-park-criminal-engineering-investigation)\//.test(pathname);
    const isCore = isCanonical || isHome || isUpdates || isControlRoom || isCriminalHub;

    const excluded = /(fundacion-por-derecho|foundation-por-derecho|palacete|books|libros|collaborate|colaborar|about|sobre-nosotros|legal-privacy|aviso-legal|buscar|search|contact|contacto)/i.test(pathname);
    if (excluded && !isCore) return;

    const copy = isEs ? {
      label: 'ALEGACIÓN ATRIBUIDA · INVESTIGACIÓN FORENSE ACTIVA',
      headline: 'Alegación transversal: administración de hecho y facilitación consciente',
      core: 'Por Derecho alega que actores privados ejercieron funciones estables de gestión sobre autoridad comunitaria, deuda, voto, acceso, seguridad, mantenimiento y control práctico, y que la Administración Concursal solicitó, autorizó, adoptó, utilizó, dependió de o permitió operar partes esenciales de esa arquitectura sin una delimitación, verificación, nombramiento o rendición de cuentas suficientes.',
      boundary: 'La evidencia documenta funciones y dependencias concretas. La administración de hecho plena, el conocimiento criminal, la facilitación consciente, la estafa procesal, la falsedad y la prevaricación siguen sometidos a prueba actor por actor; no se presentan como hechos declarados.',
      documentedTitle: 'DOCUMENTADO',
      documented: 'Funciones privadas recurrentes sobre deuda, voto, acceso, seguridad y mantenimiento; petición, asistencia, autorizaciones y uso documental por la AC en episodios concretos.',
      allegedTitle: 'POR DERECHO ALEGA',
      alleged: 'Que esa estructura operó como gestión material no reconocida y que la AC la habilitó, adoptó o utilizó con conocimiento suficiente para exigir una investigación de facilitación consciente.',
      notProvedTitle: 'NO PROBADO',
      notProved: 'Pacto criminal, estatuto pleno de administrador de hecho, falsedad consciente de un documento concreto, doble cargo general, culpabilidad judicial o conocimiento automático de actores posteriores.',
      evidenceTitle: 'PRUEBA DECISIVA',
      evidence: 'Índice judicial certificado; autoridad, cuentas e invoices de Comunidad; cruce proveedor–pagador–recargo; comunicaciones nativas; logs de seguridad/acceso; cálculos, cuentas finales, escritura y Registro.',
      whyTitle: 'Por qué afecta a todo el caso',
      chain: ['Autoridad comunitaria', 'Deuda y voto', 'Acceso, seguridad y mantenimiento', 'Control material', 'Plan, licitación y textos definitivos', 'Adjudicación, título, operación y financiación'],
      open: 'Abrir la reconstrucción completa →',
      corrections: 'Correcciones y derecho de respuesta →',
      routeTitle: 'Esta alegación cambia la pregunta de esta página',
      route: {
        governance: 'Aquí la cuestión es si nombramientos, votos, certificados y custodia documental dieron apariencia de autoridad a una gestión privada no suficientemente acreditada.',
        ac: 'Aquí la cuestión es qué solicitó, autorizó, verificó, adoptó o permitió la AC, con qué independencia, límites, contabilidad y conocimiento.',
        control: 'Aquí la cuestión es quién tuvo llaves, acceso, seguridad, mantenimiento, instrucciones, financiación y beneficio antes y después del título formal.',
        transaction: 'Aquí la cuestión es si deuda, contingencia, responsabilidad hipotecaria, mejor postura, contraprestación y cuentas se mantuvieron jurídicamente separadas o funcionaron como una sola carga favorable al adquirente.',
        judicial: 'Aquí la cuestión es qué conoció cada órgano, qué prueba y contradicción tuvo, qué decidió realmente y qué dejó sin resolver. Los efectos favorables repetidos no prueban por sí solos prevaricación.',
        implementation: 'Aquí la cuestión es qué título, autoridad, cálculo y testimonio se presentó, qué se comprobó y cómo se convirtió en escritura, cancelación e inscripción finca por finca.',
        downstream: 'Aquí la cuestión es qué diligencia debida, conflicto, condición, dispensa, desembolso, verificación y corrección se realizó sobre una posición de título/control afectada por la alegación. No se transfiere conocimiento ni culpabilidad automáticamente.',
        recovery: 'Aquí la cuestión es qué daño y beneficio son atribuibles a cada función, qué contrafactual es realista y qué remedio puede corregir cada eslabón sin doble recuperación.',
        generic: 'La alegación exige reconstruir autoridad, función, conocimiento, beneficio y causalidad antes de tratar el resultado como jurídicamente estable.'
      }
    } : {
      label: 'ATTRIBUTED ALLEGATION · ACTIVE FORENSIC INVESTIGATION',
      headline: 'Cross-cutting allegation: de facto management and knowing facilitation',
      core: 'Por Derecho alleges that private actors exercised recurring management functions over Community authority, debt, voting, access, security, maintenance and practical control, and that the Insolvency Administration requested, authorised, adopted, used, relied upon or allowed essential parts of that architecture to operate without sufficient delimitation, verification, appointment or accounting.',
      boundary: 'The evidence documents specific functions and dependencies. Full de facto-administrator status, criminal knowledge, knowing facilitation, procedural fraud, falsity and prevarication remain to be proved actor by actor and are not presented as adjudicated facts.',
      documentedTitle: 'DOCUMENTED',
      documented: 'Recurring private functions over debt, voting, access, security and maintenance; Administrator request, attendance, identified authorisations and documentary use in specific episodes.',
      allegedTitle: 'POR DERECHO ALLEGES',
      alleged: 'That the structure operated as unrecognised material management and that the Administrator enabled, adopted or used it with sufficient knowledge to require a knowing-facilitation investigation.',
      notProvedTitle: 'NOT PROVED',
      notProved: 'Criminal agreement, full administrator-in-fact status, knowing falsity of a specific document, blanket double charging, judicial guilt or automatic knowledge of later actors.',
      evidenceTitle: 'DECISIVE EVIDENCE',
      evidence: 'Certified docket; native Community authority, accounts and invoices; vendor–payer–recharge crosswalk; native communications; security/access logs; calculations, final accounts, deed and Registry chain.',
      whyTitle: 'Why it affects the entire case',
      chain: ['Community authority', 'Debt and voting', 'Access, security and maintenance', 'Material control', 'Plan, bidding and definitive texts', 'Adjudication, title, operation and finance'],
      open: 'Open the complete reconstruction →',
      corrections: 'Corrections and right of reply →',
      routeTitle: 'This allegation changes the question on this page',
      route: {
        governance: 'The question here is whether appointments, voting, certificates and record custody gave an appearance of authority to private management that was not sufficiently established.',
        ac: 'The question here is what the Administrator requested, authorised, verified, adopted or allowed, with what independence, limits, accounting and knowledge.',
        control: 'The question here is who held keys, access, security, maintenance, instructions, funding and benefit before and after formal title.',
        transaction: 'The question here is whether debt, contingency, mortgage responsibility, better-bid thresholds, consideration and accounts remained legally separate or operated as one acquirer-favouring burden.',
        judicial: 'The question here is what each body knew, what evidence and adversarial process it had, what it actually decided and what remained unresolved. Repeated favourable effects do not by themselves prove prevarication.',
        implementation: 'The question here is what title, authority, calculation and testimony were presented, what was checked and how they became deed, cancellation and property-by-property registration.',
        downstream: 'The question here is what due diligence, conflict control, condition, waiver, drawdown, verification and correction addressed a title/control position affected by the allegation. Knowledge or guilt is not transferred automatically.',
        recovery: 'The question here is which harm and benefit are attributable to each function, what counterfactual is realistic and which remedy corrects each link without double recovery.',
        generic: 'The allegation requires authority, function, knowledge, benefit and causation to be reconstructed before the outcome is treated as legally stable.'
      }
    };

    const routeType = () => {
      const rules = [
        ['governance', /(comunidad-instrumentalizacion|community-instrumentalisation|actas-2011-2022|minutes-2011-2022|autoridad-comunidad|community-authority|cexp)/i],
        ['ac', /(concurso-36-2012-administrador-concursal|insolvency-36-2012-insolvency-administrator|administrador-concursal-punto-quiebre|insolvency-administrator-loyalty-breakpoint|administrador-concursal-puerta-credito-titulo|insolvency-administrator-credit-to-title-gatekeeper|\/rsm\/|san-telmo)/i],
        ['control', /(toma-control-sun-park|sun-park-takeover|acosta-matos-perimetro|acosta-matos-perimeter|matkator|262-fincas|262-property|control-possession|material-control)/i],
        ['transaction', /(textos-definitivos-lpb|lpb-definitive-texts|adjudicacion-2022|2022-adjudication|acreedor-de-registro|lender-of-record|insolvencia-lpb|lpb-insolvency|articulo-1535|article-1535|convergencia-venta-acreedor|sale-lender-convergence|locales|premises|400000|400-000|accounting|cuentas)/i],
        ['judicial', /(calificacion-concurso|insolvency-classification|magistrado-juez|mercantile-court-1|concurso-36-2012-laj|insolvency-36-2012-laj|cgpj|audiencia-provincial|provincial-court|fiscalia|prosecutor)/i],
        ['implementation', /(implementacion-notarial|notarial-implementation|protocolo-457|protocol-457|implementacion-registral|land-registry-implementation)/i],
        ['downstream', /(ricpe|ric-private-equity|mismo-hotel|same-hotel|multiple-financial|financiacion|funding|fondos-incentivos|eu-incentives|cnmv|portfolio-orion|orion|mynd|hotel-new-trend|regional-incentives|feder)/i],
        ['recovery', /(objetivos-recuperacion|recovery-restitution|causation|causalidad|damages|danos)/i]
      ];
      const match = rules.find(([, pattern]) => pattern.test(pathname));
      return match ? match[0] : 'generic';
    };

    const ensureStyles = () => {
      if (document.getElementById('ac-dfa-knowing-visibility-styles')) return;
      const style = document.createElement('style');
      style.id = 'ac-dfa-knowing-visibility-styles';
      style.textContent = `
        .ac-kf-spotlight{max-width:1120px;margin:0 auto;border:2px solid #8c2f2c;border-left-width:7px;background:linear-gradient(135deg,#fff7f5 0%,#fff 100%);border-radius:18px;padding:1.15rem 1.3rem;box-shadow:0 14px 34px rgba(140,47,44,.09)}
        .ac-kf-spotlight h2{margin:.15rem 0 .6rem;font-size:clamp(1.45rem,2.7vw,2.25rem)}
        .ac-kf-label{display:inline-block;border-radius:999px;padding:.28rem .68rem;background:#8c2f2c;color:#fff;font-size:.75rem;font-weight:900;letter-spacing:.06em}
        .ac-kf-boundary{border-left:4px solid #536d79;background:#f4f8fa;border-radius:10px;padding:.8rem .9rem;margin:.9rem 0}
        .ac-kf-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.75rem;margin:1rem 0}
        .ac-kf-card{background:#fff;border:1px solid #d9dfdf;border-radius:13px;padding:.82rem}.ac-kf-card strong{display:block;font-size:.76rem;letter-spacing:.05em;margin-bottom:.35rem}.ac-kf-card p{margin:0;font-size:.9rem;line-height:1.48}
        .ac-kf-chain{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:.45rem;align-items:stretch;margin:.8rem 0}.ac-kf-step{position:relative;background:#13252d;color:#fff;border-radius:11px;padding:.72rem .65rem;font-size:.78rem;font-weight:800;text-align:center;display:grid;place-items:center;min-height:68px}.ac-kf-step:not(:last-child):after{content:'→';position:absolute;right:-.38rem;top:50%;transform:translateY(-50%);z-index:2;color:#8c2f2c;background:#fff;border-radius:50%;width:1rem;height:1rem;display:grid;place-items:center;font-size:.72rem}
        .ac-kf-actions{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:.9rem}.ac-kf-actions a{font-weight:850}
        .ac-kf-route{max-width:1120px;margin:0 auto;border-left:6px solid #8c2f2c;background:#fff7f5;border-radius:15px;padding:1rem 1.15rem}.ac-kf-route h2{margin:.1rem 0 .45rem}.ac-kf-route p:last-child{margin-bottom:0}
        @media(max-width:1050px){.ac-kf-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.ac-kf-chain{grid-template-columns:repeat(3,minmax(0,1fr))}.ac-kf-step:nth-child(3):after{display:none}}
        @media(max-width:680px){.ac-kf-grid,.ac-kf-chain{grid-template-columns:1fr}.ac-kf-step:after{display:none!important}}
      `;
      document.head.appendChild(style);
    };

    const fullSpotlight = () => `
      <aside class="ac-kf-spotlight" data-ac-dfa-allegation-visibility="${VERSION}" role="note">
        <span class="ac-kf-label">${copy.label}</span>
        <h2>${copy.headline}</h2>
        <p>${copy.core}</p>
        <div class="ac-kf-boundary"><strong>${copy.boundary}</strong></div>
        <div class="ac-kf-grid">
          <div class="ac-kf-card"><strong>${copy.documentedTitle}</strong><p>${copy.documented}</p></div>
          <div class="ac-kf-card"><strong>${copy.allegedTitle}</strong><p>${copy.alleged}</p></div>
          <div class="ac-kf-card"><strong>${copy.notProvedTitle}</strong><p>${copy.notProved}</p></div>
          <div class="ac-kf-card"><strong>${copy.evidenceTitle}</strong><p>${copy.evidence}</p></div>
        </div>
        <h3>${copy.whyTitle}</h3>
        <div class="ac-kf-chain" data-ac-dfa-impact-chain="${VERSION}">${copy.chain.map(item => `<div class="ac-kf-step">${item}</div>`).join('')}</div>
        <div class="ac-kf-actions"><a href="${canonical}">${copy.open}</a><a href="${corrections}">${copy.corrections}</a></div>
      </aside>`;

    const routePanel = type => `
      <aside class="ac-kf-route" data-ac-dfa-route-relevance="${VERSION}" data-ac-dfa-route-type="${type}" role="note">
        <span class="ac-kf-label">${copy.label}</span>
        <h2>${copy.routeTitle}</h2>
        <p><strong>${copy.headline}.</strong> ${copy.route[type] || copy.route.generic}</p>
        <div class="ac-kf-boundary">${copy.boundary}</div>
        <div class="ac-kf-actions"><a href="${canonical}">${copy.open}</a><a href="${corrections}">${copy.corrections}</a></div>
      </aside>`;

    const wrap = html => {
      const section = document.createElement('section');
      section.className = 'section ac-kf-visibility-section';
      section.dataset.acDfaKnowingVisibilitySection = VERSION;
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

    const replaceExisting = (selector, html) => {
      const existing = document.querySelector(selector);
      if (!existing) return false;
      ensureStyles();
      const section = existing.closest('section');
      const shell = section && section.querySelector(':scope > .shell');
      if (shell) shell.innerHTML = html;
      else existing.outerHTML = html;
      if (section) section.dataset.acDfaKnowingVisibilitySection = VERSION;
      return true;
    };

    const activateCore = () => {
      ensureStyles();
      if (isCanonical) {
        document.title = isEs
          ? 'Alegación: administración de hecho y facilitación consciente | Project Sun Rock'
          : 'Allegation: de facto management and knowing facilitation | Project Sun Rock';
        const meta = document.querySelector('meta[name="description"]');
        if (meta) meta.setAttribute('content', copy.core);
      }
      const replaced = replaceExisting('[data-ac-dfa-update], [data-ac-dfa-canonical-status]', fullSpotlight());
      if (!replaced && !document.querySelector('[data-ac-dfa-allegation-visibility]')) insertAfterHero(wrap(fullSpotlight()));
    };

    const activateRoute = () => {
      const type = routeType();
      ensureStyles();
      const html = routePanel(type);
      const replaced = replaceExisting('[data-ac-dfa-crosslink]', html);
      if (!replaced && !document.querySelector('[data-ac-dfa-route-relevance]')) insertAfterHero(wrap(html));
    };

    document.documentElement.dataset.acDfaKnowingFacilitationVisibility = VERSION;
    if (isCore) activateCore();
    else activateRoute();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
  window.setTimeout(run, 500);
  window.setTimeout(run, 1900);
})();

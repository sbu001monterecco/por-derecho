(() => {
  'use strict';

  const VERSION = '20260824a';

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
      label: 'ACUSACIÓN PENAL DIRECTA DE GIL MARER · CINCO + AC + JUEZ',
      headline: 'Cinco administradores en la sombra alegados y una habilitación institucional activa',
      core: 'Gil Marer acusa directamente a Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila María Cogolludo Ramos, José Daniel Acosta Matos y Laura Patricia Acosta Matos de haber operado, a más tardar en 2018, como una estructura coordinada de administradores de hecho o en la sombra sobre la esfera patrimonial y empresarial de Luchy Playa Blanca y la plataforma hotelera integrada, mediante actos dentro del concurso formal y fuera de su perímetro registrado.',
      boundary: 'Gil atribuye al administrador concursal correos, reuniones, peticiones, autorizaciones, decisiones, implementación, adopción y ratificación, además de omisiones; y al Magistrado-Juez Alberto López Villarrubia resoluciones, negativas, cierres, demoras y omisiones que habrían preservado el mecanismo y saboteado o frustrado una salida desarrollada y respaldada por financiación. Es una acusación penal directa, no una condena ni un hecho penal declarado.',
      documentedTitle: 'DOCUMENTADO',
      documented: 'Funciones recurrentes sobre deuda/voto, acceso, seguridad, llaves y mantenimiento; petición, autorizaciones y ratificación del AC en episodios concretos; informe contemporáneo de una reunión Irigoyen–juez el 13 de junio de 2018.',
      allegedTitle: 'GIL ALEGA DIRECTAMENTE',
      alleged: 'Administración material coordinada por los cinco; habilitación afirmativa y omisiva del AC; y actos y omisiones judiciales que preservaron el resultado. Gil alega un aparato coercitivo de gobierno paralelo y control patrimonial, funcionalmente comparable a un acreedor en posesión, que impidió pagar/refinanciar la deuda al degradar o bloquear el paquete de garantías y las autorizaciones de salida.',
      notProvedTitle: 'NO ADJUDICADO',
      notProved: 'Responsabilidad penal individual, pacto y dolo común, estatuto jurídico pleno, prevaricación, causalidad criminal, visitas judiciales adicionales, que toda condición de tercero estuviera aprobada o cierre inevitable de la salida financiada.',
      evidenceTitle: 'PRUEBA DECISIVA',
      evidence: 'Ledger que separe condiciones bajo control de Aweswell, condiciones de financiador/contraparte y outputs controlados por AC/juez/actores adversos; paquete de garantías intacto, cifra de deuda, autoridad, acceso, valoración, aprobaciones, consignación y causalidad de cada vía.',
      whyTitle: 'Por qué afecta a todo el caso',
      chain: ['Autoridad comunitaria', 'Deuda y voto', 'Acceso, llaves y seguridad', 'Control material y obras', 'Salida financiable', 'Liquidación, título, operación e ingresos'],
      open: 'Abrir acusación, prueba y contradicción →',
      corrections: 'Correcciones y derecho de respuesta →',
      routeTitle: 'Acusación penal rectora: cinco actores + habilitación concursal y judicial',
      route: {
        governance: 'Aquí la cuestión es si nombramientos, votos, certificados y custodia documental dieron apariencia de autoridad a una gestión privada no suficientemente acreditada.',
        ac: 'Gil no alega mera omisión: atribuye a la AC correos, reuniones, peticiones, autorizaciones, decisiones, implementación, adopción y ratificación, además de fallos de delimitación, supervisión, restauración y rendición de cuentas.',
        control: 'Aquí la cuestión es quién tuvo llaves, acceso, seguridad, mantenimiento, instrucciones, financiación y beneficio antes y después del título formal.',
        transaction: 'Aquí la cuestión es si deuda, contingencia, responsabilidad hipotecaria, mejor postura, contraprestación y cuentas se mantuvieron jurídicamente separadas o funcionaron como una sola carga favorable al adquirente.',
        judicial: 'Gil atribuye a Alberto López Villarrubia resoluciones, negativas, cierres, demoras y omisiones que habrían preservado el control y saboteado o frustrado la salida financiable. Cada acto exige prueba ante el juez, deber, injusticia, conocimiento y causalidad.',
        implementation: 'Aquí la cuestión es qué título, autoridad, cálculo y testimonio se presentó, qué se comprobó y cómo se convirtió en escritura, cancelación e inscripción finca por finca.',
        downstream: 'Aquí la cuestión es qué diligencia debida, conflicto, condición, dispensa, desembolso, verificación y corrección se realizó sobre una posición de título/control afectada por la alegación. No se transfiere conocimiento ni culpabilidad automáticamente.',
        recovery: 'Aquí la cuestión es qué daño y beneficio son atribuibles a cada función, qué contrafactual es realista y qué remedio puede corregir cada eslabón sin doble recuperación.',
        generic: 'La alegación exige reconstruir autoridad, función, conocimiento, beneficio y causalidad antes de tratar el resultado como jurídicamente estable.'
      }
    } : {
      label: 'GIL MARER’S DIRECT CRIMINAL ALLEGATION · FIVE + AC + JUDGE',
      headline: 'Five alleged shadow administrators and active institutional enablement',
      core: 'Gil Marer directly accuses Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila María Cogolludo Ramos, José Daniel Acosta Matos and Laura Patricia Acosta Matos of operating, by 2018 at the latest, as a coordinated de facto or shadow-administration structure over Luchy Playa Blanca’s patrimonial and business sphere and the integrated hotel platform, through acts inside the formal insolvency and outside its recorded perimeter.',
      boundary: 'Gil attributes to the insolvency administrator emails, meetings, requests, authorisations, decisions, implementation, adoption and ratification, as well as omissions; and to Judge Alberto López Villarrubia decisions, refusals, closures, delay and omissions that allegedly preserved the mechanism and sabotaged or frustrated a developed, finance-backed exit. This is a direct criminal accusation, not a conviction or adjudicated criminal fact.',
      documentedTitle: 'DOCUMENTED',
      documented: 'Recurring functions over debt/voting, access, security, keys and maintenance; Administrator request, authorisations and ratification in specific episodes; a contemporary report of one Irigoyen–judge meeting on 13 June 2018.',
      allegedTitle: 'GIL DIRECTLY ALLEGES',
      alleged: 'Coordinated material administration by the five; affirmative and omissive AC enablement; and judicial acts and omissions that preserved the outcome. Gil alleges a coercive parallel-governance and asset-control apparatus, functionally comparable to a lender in possession, which obstructed debt payment/refinancing by degrading or blocking the security package and exit authorisations.',
      notProvedTitle: 'NOT ADJUDICATED',
      notProved: 'Individual criminal liability, common agreement and intent, full legal status, prevaricación, criminal causation, further judicial visits, approval of every third-party condition or inevitable completion of the funded exit.',
      evidenceTitle: 'DECISIVE EVIDENCE',
      evidence: 'A ledger separating conditions within Aweswell’s control, lender/counterparty conditions and outputs controlled by the AC/court/adverse actors; intact collateral, debt figure, authority, access, valuation, approvals, deposit and route-specific causation.',
      whyTitle: 'Why it affects the entire case',
      chain: ['Community authority', 'Debt and voting', 'Access, keys and security', 'Material control and works', 'Financeable exit', 'Liquidation, title, operation and income'],
      open: 'Open allegation, evidence and contradiction →',
      corrections: 'Corrections and right of reply →',
      routeTitle: 'Controlling criminal allegation: five actors + insolvency and judicial enablement',
      route: {
        governance: 'The question here is whether appointments, voting, certificates and record custody gave an appearance of authority to private management that was not sufficiently established.',
        ac: 'Gil does not allege omission alone: he attributes to the Administrator emails, meetings, requests, authorisations, decisions, implementation, adoption and ratification, as well as failures to delimit, supervise, restore and account.',
        control: 'The question here is who held keys, access, security, maintenance, instructions, funding and benefit before and after formal title.',
        transaction: 'The question here is whether debt, contingency, mortgage responsibility, better-bid thresholds, consideration and accounts remained legally separate or operated as one acquirer-favouring burden.',
        judicial: 'Gil attributes to Alberto López Villarrubia decisions, refusals, closures, delay and omissions that allegedly preserved control and sabotaged or frustrated the financeable exit. Each act requires evidence before the judge, duty, injustice, knowledge and causation.',
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
        .ac-kf-spotlight{max-width:1120px;margin:0 auto;border:4px solid #8c2f2c;border-left-width:10px;background:linear-gradient(135deg,#fff7f2 0%,#fff 100%);border-radius:20px;padding:clamp(1.15rem,3vw,1.65rem);box-shadow:0 20px 48px rgba(81,16,18,.2)}
        .ac-kf-spotlight h2{max-width:28ch;margin:.2rem 0 .7rem;color:#651819;font-size:clamp(1.75rem,4vw,3rem);line-height:1.03}
        .ac-kf-spotlight>p{max-width:70rem;font-size:1.02rem;line-height:1.62}.ac-kf-label{display:inline-block;border-radius:999px;padding:.34rem .72rem;background:#8c2f2c;color:#fff;font-size:.75rem;font-weight:900;letter-spacing:.06em}
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
          ? 'Cinco administradores de hecho alegados, AC y juez | Project Sun Rock'
          : 'Five alleged shadow administrators, AC and judge | Project Sun Rock';
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

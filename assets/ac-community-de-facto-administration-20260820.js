(() => {
  'use strict';

  const run = () => {
    const pathname = window.location.pathname.replace(/\/+$/, '/');
    const isEs = pathname.includes('/por-derecho/es/');
    const isEn = pathname.includes('/por-derecho/en/');
    if (!isEs && !isEn) return;

    const base = '/por-derecho';
    const canonical = isEs
      ? `${base}/es/administracion-de-hecho-comunidad-ac/`
      : `${base}/en/de-facto-administration-community-ac/`;
    const isCanonical = pathname === canonical;
    const isHome = pathname === `${base}/${isEs ? 'es' : 'en'}/`;
    const isUpdates = /\/(actualizaciones|updates)\//.test(pathname);
    const isControl = /\/(sala-control-caso|case-control-room|ingenieria-forense-criminal-sun-park|sun-park-criminal-engineering-investigation|reconstruccion-unitaria-autoridades-publicas|public-authority-unitary-case-reconstruction|mapa-probatorio-penal-unitario|unitary-criminal-evidence-map)\//.test(pathname);

    const copy = isEs ? {
      kicker: 'ACUSACIÓN PENAL RECTORA · CINCO ACTORES + AC + JUEZ',
      title: 'Gil Marer alega una administración de hecho encubierta y una habilitación institucional activa',
      body: 'Gil Marer acusa directamente a Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila María Cogolludo Ramos, José Daniel Acosta Matos y Laura Patricia Acosta Matos de haber operado, a más tardar en 2018, como una estructura coordinada de administradores de hecho o en la sombra sobre la esfera patrimonial y empresarial de Luchy Playa Blanca y la plataforma hotelera integrada, mediante actos dentro del concurso formal y fuera de su perímetro registrado. Alega que el administrador concursal la habilitó mediante correos, reuniones, peticiones, autorizaciones, decisiones, adopción y ratificación, además de omisiones; y atribuye al Magistrado-Juez D. Alberto López Villarrubia resoluciones, negativas, demoras y omisiones que preservaron el mecanismo y sabotearon o frustraron una salida desarrollada y respaldada por financiación. Es la acusación penal directa de Gil, no una condena ni un hecho penal declarado.',
      boundary: 'Control financiero: Gil sostiene que Aweswell había cumplido o podía cumplir las condiciones bajo su control y que el bloqueo operativo recaía en preservar y entregar el paquete de garantías, obtener cifra/certificación de deuda y autoridad concursal/judicial, y conservar acceso, explotación, valoración y colateral; atribuye su destrucción o impedimento al mecanismo privado, concursal y judicial. Los documentos conservan condiciones y aprobaciones de terceros: la atribución no es una conclusión judicial ni prueba de desembolso.',
      action: 'Abrir acusación, prueba y contradicción →',
      crossTitle: 'Acusación rectora: cinco administradores de hecho alegados + habilitación institucional',
      crossBody: 'Lea esta página con la matriz unitaria: deuda y voto, acceso y seguridad, mantenimiento, obras y valoración, información, salida financiada, operación, ingresos y resultado; actos y omisiones del administrador concursal; y actos, negativas, demoras y omisiones judiciales atribuidos por Gil.',
      incident: 'No se ha localizado un incidente posterior a la liquidación que amplíe el total privilegiado o convierta las cifras posteriores de Comunidad/intereses en crédito definitivo; el índice certificado completo sigue pendiente.',
      label: 'Acusación directa de Gil · no declaración judicial'
    } : {
      kicker: 'CONTROLLING CRIMINAL ALLEGATION · FIVE ACTORS + AC + JUDGE',
      title: 'Gil Marer alleges concealed de facto administration and active institutional enablement',
      body: 'Gil Marer directly accuses Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila María Cogolludo Ramos, José Daniel Acosta Matos and Laura Patricia Acosta Matos of operating, by 2018 at the latest, as a coordinated de facto or shadow-administration structure over Luchy Playa Blanca’s patrimonial and business sphere and the integrated hotel platform, through acts inside the formal insolvency and outside its recorded perimeter. He alleges that the insolvency administrator enabled it through emails, meetings, requests, authorisations, decisions, adoption and ratification, as well as omissions; and attributes to Magistrate-Judge Alberto López Villarrubia decisions, refusals, delay and omissions that preserved the mechanism and sabotaged or frustrated a developed, finance-backed exit. This is Gil’s direct criminal allegation, not a conviction or adjudicated criminal fact.',
      boundary: 'Finance control: Gil says Aweswell had performed or could perform the conditions within its control and that the operative block lay in preserving and delivering the security package, obtaining the debt figure/certification and insolvency/court authority, and maintaining access, operation, valuation and collateral; he attributes their destruction or prevention to the private, insolvency and judicial mechanism. The documents retain third-party conditions and approvals: the attribution is not a judicial finding or proof of drawdown.',
      action: 'Open allegation, evidence and contradiction →',
      crossTitle: 'Controlling allegation: five alleged shadow administrators + institutional enablement',
      crossBody: 'Read this page with the unitary matrix: debt and voting, access and security, maintenance, works and valuation, information, funded exit, operation, income and outcome; acts and omissions by the insolvency administrator; and judicial acts, refusals, delays and omissions attributed by Gil.',
      incident: 'No post-liquidation incident has been located that enlarges the privileged total or turns later Community/interest figures into definitive credit; the complete certified index remains outstanding.',
      label: 'Gil’s direct accusation · no judicial finding'
    };

    const ensureStyles = () => {
      if (document.getElementById('ac-community-de-facto-styles')) return;
      const style = document.createElement('style');
      style.id = 'ac-community-de-facto-styles';
      style.textContent = `
        .ac-dfa-panel{max-width:1120px;margin:0 auto;border-left:5px solid #8c2f2c;background:#fff7f5;border-radius:16px;padding:1.1rem 1.25rem}
        .ac-dfa-panel h2{margin:.15rem 0 .55rem}.ac-dfa-panel p:last-child{margin-bottom:0}
        .ac-dfa-kicker{margin:0 0 .4rem;font-size:.76rem;letter-spacing:.08em;text-transform:uppercase;font-weight:850;color:#8c2f2c}
        .ac-dfa-label{display:inline-block;border:1px solid #8c2f2c;border-radius:999px;padding:.25rem .65rem;font-size:.78rem;font-weight:850;margin:.4rem 0}
        .ac-dfa-cross{max-width:1120px;margin:0 auto;border-left:5px solid #536d79;background:#f4f8fa;border-radius:14px;padding:1rem 1.2rem}
        .ac-dfa-cross h2{margin:.1rem 0 .45rem}.ac-dfa-cross p:last-child{margin-bottom:0}
        .ac-dfa-update{max-width:1120px;margin:0 auto;background:linear-gradient(135deg,#2b0b0d 0%,#681718 58%,#931f1f 100%);color:#fff;border:3px solid #f0d2c9;border-radius:20px;padding:clamp(1.15rem,3vw,1.8rem);box-shadow:0 1.1rem 3rem rgba(49,11,12,.24)}.ac-dfa-update h2{max-width:28ch;margin:.1rem 0 .65rem;color:#fff;font-size:clamp(1.7rem,4vw,3rem);line-height:1.03}.ac-dfa-update p{max-width:72rem;line-height:1.58}.ac-dfa-update a{display:inline-block;color:#fff;font-weight:900}.ac-dfa-boundary{margin:.8rem 0;padding:.72rem .82rem;border-left:5px solid #e1b35f;background:rgba(20,10,10,.34);border-radius:8px;font-size:.84rem}
      `;
      document.head.appendChild(style);
    };

    const makeSection = (className, html) => {
      const section = document.createElement('section');
      section.className = `section ${className}`;
      section.dataset.acCommunityShadowControl = '20260824';
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

    const routeRelevant = () => {
      if (isCanonical || isHome || isUpdates || isControl) return false;
      return /(comunidad-instrumentalizacion|community-instrumentalisation|concurso-36-2012-administrador-concursal|insolvency-36-2012-insolvency-administrator|administrador-concursal-punto-quiebre|insolvency-administrator-loyalty-breakpoint|administrador-concursal-puerta-credito-titulo|insolvency-administrator-credit-to-title-gatekeeper|textos-definitivos-lpb|lpb-definitive-texts|adjudicacion-2022|2022-adjudication|toma-control-sun-park|sun-park-takeover|acosta-matos-perimetro|acosta-matos-perimeter|calificacion-concurso|insolvency-classification|concurso-36-2012-laj|insolvency-36-2012-laj|mercantile-court-1|magistrado-juez)/i.test(pathname);
    };

    const insertUpdate = () => {
      if (!(isHome || isUpdates || isControl) || document.querySelector('[data-ac-dfa-update]')) return;
      ensureStyles();
      const section = makeSection('ac-dfa-update-section', `
        <aside class="ac-dfa-update" data-ac-dfa-update="20260824" aria-label="${copy.kicker}">
          <p class="ac-dfa-kicker" style="color:#f2c7c1">${copy.kicker}</p>
          <h2>${copy.title}</h2>
          <p>${copy.body}</p>
          <p class="ac-dfa-boundary"><strong>${copy.boundary}</strong></p>
          <p><a href="${canonical}">${copy.action}</a></p>
        </aside>`);
      insertAfterHero(section);
    };

    const insertCross = () => {
      if (!routeRelevant() || document.querySelector('[data-ac-dfa-crosslink]')) return;
      ensureStyles();
      const section = makeSection('ac-dfa-cross-section', `
        <aside class="ac-dfa-cross" data-ac-dfa-crosslink="20260820" role="note">
          <p class="ac-dfa-kicker">${copy.kicker}</p>
          <h2>${copy.crossTitle}</h2>
          <p>${copy.crossBody}</p>
          <p><strong>${copy.boundary}</strong></p>
          <p><strong>${copy.incident}</strong></p>
          <p><a href="${canonical}">${copy.action}</a></p>
        </aside>`);
      insertAfterHero(section);
    };

    const insertCanonicalContext = () => {
      if (!isCanonical || document.querySelector('[data-ac-dfa-canonical-status]')) return;
      ensureStyles();
      const section = makeSection('ac-dfa-canonical-section', `
        <aside class="ac-dfa-panel" data-ac-dfa-canonical-status="20260820" role="note">
          <p class="ac-dfa-kicker">${copy.kicker}</p>
          <span class="ac-dfa-label">${copy.label}</span>
          <p>${copy.incident}</p>
        </aside>`);
      insertAfterHero(section);
    };

    insertCanonicalContext();
    insertUpdate();
    insertCross();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
  window.setTimeout(run, 1800);
})();

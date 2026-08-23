/* CAM DIRECT INSTRUCTION / CREDITOR CONTROL / AC APPROVAL / JUDICIAL OMISSION — 23 AUGUST 2026 */
(() => {
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path.toLowerCase();
  };
  const path = normalise(location.pathname);
  const routes = [
    '/en/sun-park-takeover-7-june-2018/',
    '/es/toma-control-sun-park-7-junio-2018/',
    '/en/insolvency-classification-parallel-lives/',
    '/es/calificacion-concurso-36-2012-vidas-paralelas/',
    '/en/acosta-matos-perimeter/',
    '/es/acosta-matos-perimetro/',
    '/en/insolvency-36-2012-insolvency-administrator/',
    '/es/concurso-36-2012-administrador-concursal/',
    '/en/insolvency-36-2012-mercantile-court-1/',
    '/es/concurso-36-2012-magistrado-juez/',
    '/en/lender-of-record/liability/',
    '/es/acreedor-de-registro/responsabilidad/',
    '/en/de-facto-administration-community-ac/',
    '/es/administracion-de-hecho-comunidad-ac/',
    '/en/sun-park-criminal-engineering-investigation/',
    '/es/ingenieria-forense-criminal-sun-park/',
    '/en/unitary-criminal-reverse-engineering/',
    '/es/ingenieria-inversa-criminal-unitaria/'
  ];
  if (!routes.some(route => path.endsWith(route))) return;

  const render = () => {
    if (document.querySelector('[data-cam-criminal-lead="20260823"]')) return;
    const en = path.includes('/en/') || document.documentElement.lang === 'en';
    const prefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
    const href = en
      ? `${prefix}en/cam-creditor-control-shadow-administration-judicial-omission/`
      : `${prefix}es/control-acreedor-cam-administracion-hecho-omision-judicial/`;
    const c = en ? {
      eyebrow: 'CRIMINAL-LEAD CONVERGENCE · UPDATED 23 AUGUST 2026',
      title: 'Direct instruction, creditor in possession, de facto administration and institutional omission',
      lead: 'Gil Marer and Aweswell allege that the 7 June 2018 physical operation was directly instructed or coordinated by CAM-perimeter actors; criminally enabled, approved or ratified by the insolvency administrator; and preserved through judicial omission amounting, in Gil’s allegation, to omissionary judicial prevarication.',
      directK: 'Allegation 1 · private instruction',
      directT: 'CAM / JDAM / FMMM / relevant Laura actor',
      directP: 'The allegation is that secured credit, isolated title and Community/security authority were deliberately converted into whole-hotel physical control. Contemporaneous emails place a CAM lawyer identified as “Laura Matos” and Community personnel at the event; earlier filed material places JDAM/FMMM in the access-and-control sequence. The native instruction chain remains a production demand.',
      acK: 'Allegation 2 · insolvency administrator',
      acT: 'Criminal approval, enablement or ratification',
      acP: 'The administrator is linked to the 18 May security-authority route and later acknowledged a narrower access authorisation while denying the main lock takeover. Gil alleges that the authority was knowingly designed, tolerated, ratified or not reversed in a legally equivalent way. Scope, knowledge, power to act and intent remain decisive.',
      judgeK: 'Allegation 3 · court',
      judgeT: 'Omissionary judicial prevarication',
      judgeP: 'Gil alleges that resolutions, refusals, delay or omissions knowingly preserved the private-control result. The legal test requires an exact judicial act, evidence before the judge, competence and duty, objective injustice or malicious delay, knowledge, purpose and causation. An adverse or incomplete ruling is not automatically criminal.',
      identityT: 'Attribution control — Laura Patricia Acosta Matos',
      identityP: 'The public record identifies Laura Patricia Acosta Matos. Gil attributes responsibility to LPAM, but mandate, exact instructions, knowledge, purpose and any criminal responsibility remain actor-specific allegations requiring independent proof.',
      documentedT: 'What is already documented',
      documentedP: 'Contemporaneous emails; same-day videos and photographs; pre-event and same-day criminal pleadings; the 18 May Community/security node; the creditor/title record; later control and project benefit; and institutional decisions or omissions. These evidence types support making and investigating the allegations—not treating guilt as adjudicated.',
      contraryT: 'Contrary record preserved',
      contraryP: 'The 2018 criminal proceedings were provisionally dismissed and that result was upheld on appeal. The administrator denied the principal lock-takeover instruction and described narrower access. CAM had valid creditor rights and may have held valid individual titles. Later adjudication remains legally distinct and non-retroactive.',
      open: 'Open the complete criminal-allegation and proof matrix',
      badge: 'Allegation ≠ adjudicated finding',
      nav: 'Criminal lead'
    } : {
      eyebrow: 'CONVERGENCIA DE LÍNEA PENAL · ACTUALIZADO 23 AGOSTO 2026',
      title: 'Instrucción directa, acreedor en posesión, administración de hecho y omisión institucional',
      lead: 'Gil Marer y Aweswell alegan que la operación física de 7 de junio de 2018 fue instruida o coordinada directamente por actores del perímetro CAM; habilitada, aprobada o ratificada penalmente por el administrador concursal; y preservada mediante omisión judicial constitutiva, según la alegación de Gil, de prevaricación judicial por omisión.',
      directK: 'Alegación 1 · instrucción privada',
      directT: 'CAM / JDAM / FMMM / actor Laura pertinente',
      directP: 'La alegación es que crédito garantizado, títulos aislados y autoridad de Comunidad/seguridad se convirtieron deliberadamente en control físico de todo el hotel. Correos contemporáneos sitúan a una abogada CAM identificada como “Laura Matos” y personal de la Comunidad en el acto; material anterior presentado sitúa a JDAM/FMMM en la secuencia de acceso y control. La cadena nativa de instrucciones sigue siendo un requerimiento de producción.',
      acK: 'Alegación 2 · administrador concursal',
      acT: 'Aprobación, habilitación o ratificación penal',
      acP: 'El administrador está vinculado a la vía de autoridad de seguridad de 18 de mayo y después reconoció una autorización de acceso más limitada mientras negaba la toma principal de cerraduras. Gil alega que la autoridad fue diseñada, tolerada, ratificada conscientemente o no revertida de manera jurídicamente equivalente. Alcance, conocimiento, poder de actuación e intención son decisivos.',
      judgeK: 'Alegación 3 · juzgado',
      judgeT: 'Prevaricación judicial por omisión',
      judgeP: 'Gil alega que resoluciones, negativas, demoras u omisiones preservaron conscientemente el resultado de control privado. El test jurídico exige acto judicial exacto, prueba ante el juez, competencia y deber, injusticia objetiva o demora maliciosa, conocimiento, finalidad y causalidad. Una resolución adversa o incompleta no es automáticamente penal.',
      identityT: 'Control de atribución — Laura Patricia Acosta Matos',
      identityP: 'El registro público identifica a Laura Patricia Acosta Matos. Gil atribuye responsabilidad a LPAM, pero mandato, instrucciones exactas, conocimiento, finalidad y cualquier responsabilidad penal siguen siendo alegaciones actor-específicas que exigen prueba independiente.',
      documentedT: 'Lo que ya está documentado',
      documentedP: 'Correos contemporáneos; vídeos y fotos del mismo día; denuncias anteriores y coetáneas; nodo Comunidad/seguridad de 18 de mayo; registro de crédito/título; control y beneficio de proyecto posteriores; y decisiones u omisiones institucionales. Estos tipos de prueba permiten formular e investigar las alegaciones, no tratar la culpabilidad como declarada.',
      contraryT: 'Registro contrario preservado',
      contraryP: 'Las diligencias penales de 2018 fueron archivadas provisionalmente y el resultado se confirmó en apelación. El administrador negó la instrucción de la toma principal y describió un acceso más limitado. CAM tenía derechos acreedores válidos y puede haber tenido títulos individuales válidos. La adjudicación posterior es jurídicamente distinta y no retroactiva.',
      open: 'Abrir la matriz completa de alegación penal y prueba',
      badge: 'Alegación ≠ declaración judicial',
      nav: 'Línea penal'
    };

    const section = document.createElement('section');
    section.className = 'section alt cam-criminal-lead';
    section.dataset.camCriminalLead = '20260823';
    section.innerHTML = `<div class="shell">
      <header class="camcl-head"><p class="kicker">${c.eyebrow}</p><h2>${c.title}</h2><p class="camcl-lead">${c.lead}</p><span class="camcl-badge">${c.badge}</span></header>
      <div class="camcl-grid">
        <article><span>${c.directK}</span><h3>${c.directT}</h3><p>${c.directP}</p></article>
        <article><span>${c.acK}</span><h3>${c.acT}</h3><p>${c.acP}</p></article>
        <article><span>${c.judgeK}</span><h3>${c.judgeT}</h3><p>${c.judgeP}</p></article>
      </div>
      <div class="camcl-split"><article class="camcl-identity"><h3>${c.identityT}</h3><p>${c.identityP}</p></article><article><h3>${c.documentedT}</h3><p>${c.documentedP}</p></article><article class="camcl-contrary"><h3>${c.contraryT}</h3><p>${c.contraryP}</p></article></div>
      <a class="dossier-link camcl-link" href="${href}"><span>${c.eyebrow}</span><strong>${c.open}</strong><i aria-hidden="true">→</i></a>
    </div>`;

    const style = document.createElement('style');
    style.dataset.camCriminalLeadStyle = '20260823';
    style.textContent = `
      .cam-criminal-lead{position:relative;overflow:hidden;background:linear-gradient(145deg,#f7f1ed,#edf3f3)}
      .cam-criminal-lead:before{content:"CONTROL";position:absolute;right:-.04em;top:.05em;font-size:clamp(5rem,14vw,12rem);font-weight:900;letter-spacing:-.07em;color:rgba(19,37,45,.035);pointer-events:none}
      .camcl-head{position:relative;max-width:1000px}.camcl-head h2{max-width:900px}.camcl-lead{font-size:1.08rem;line-height:1.67;max-width:980px}.camcl-badge{display:inline-block;margin:.5rem 0 1rem;border-radius:999px;padding:.35rem .65rem;background:#13252d;color:#fff;font-size:.73rem;font-weight:900;letter-spacing:.06em;text-transform:uppercase}
      .camcl-grid{position:relative;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.9rem}.camcl-grid article,.camcl-split article{border:1px solid rgba(19,37,45,.15);border-radius:15px;background:#fff;padding:1rem;box-shadow:0 .65rem 1.6rem rgba(19,37,45,.05)}
      .camcl-grid article{border-top:5px solid #8c2f2c}.camcl-grid article:nth-child(2){border-top-color:#8c6b2f}.camcl-grid article:nth-child(3){border-top-color:#5b5578}.camcl-grid span{display:block;margin-bottom:.35rem;font-size:.72rem;font-weight:900;text-transform:uppercase;letter-spacing:.07em;color:#7b2e2e}.camcl-grid h3,.camcl-split h3{margin:.15rem 0 .5rem}.camcl-grid p,.camcl-split p{line-height:1.57}
      .camcl-split{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.9rem;margin:1rem 0}.camcl-identity{border-left:6px solid #8c6b2f!important;background:#fffaf0!important}.camcl-contrary{border-left:6px solid #526b59!important;background:#f3f7f5!important}.camcl-link{margin-top:.7rem}
      @media(max-width:900px){.camcl-grid,.camcl-split{grid-template-columns:1fr}}
    `;
    document.head.appendChild(style);

    const hero = document.querySelector('main .hero, main .dossier-hero, main > section');
    const main = document.querySelector('main');
    if (!main) return;
    if (hero) hero.insertAdjacentElement('afterend', section); else main.prepend(section);

    const nav = document.querySelector('.main-nav');
    if (nav && !nav.querySelector(`a[href="${href}"]`)) {
      const a = document.createElement('a'); a.href = href; a.textContent = c.nav;
      const language = nav.querySelector('.language-link,[hreflang]');
      nav.insertBefore(a, language || null);
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render, { once: true });
  else render();
})();

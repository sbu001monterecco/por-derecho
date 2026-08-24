/* FIVE-ACTOR SHADOW ADMINISTRATION / AC COMMISSION + OMISSION / JUDICIAL ACT + OMISSION — 24 AUGUST 2026 */
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
    if (document.querySelector('[data-cam-criminal-lead="20260824"]')) return;
    const en = path.includes('/en/') || document.documentElement.lang === 'en';
    const prefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
    const href = en
      ? `${prefix}en/cam-creditor-control-shadow-administration-judicial-omission/`
      : `${prefix}es/control-acreedor-cam-administracion-hecho-omision-judicial/`;
    const controlHref = `${prefix}assets/data/cam-nondilution-thread-closeout-v1.json`;
    const c = en ? {
      eyebrow: 'EXPRESS CRIMINAL ATTRIBUTION · UPDATED 24 AUGUST 2026',
      title: 'Five alleged shadow administrators, affirmative insolvency enablement and direct judicial-culpability allegation',
      lead: 'Gil Marer and Aweswell directly allege that five identified private actors operated, by 2018 at the latest, as a coordinated de facto or shadow-administration structure over Luchy Playa Blanca’s patrimonial and business sphere and the integrated hotel platform, through conduct inside the formal insolvency and outside its recorded perimeter; that the insolvency administrator criminally enabled the structure by affirmative acts as well as omissions; and that Judge Alberto López Villarrubia preserved it through specified decisions, refusals, delay and omissions, thereby allegedly sabotaging or frustrating a developed, finance-backed exit. These are the controlling direct criminal allegations—not merely questions, and not adjudicated findings.',
      directK: 'Direct criminal allegation 1 · private shadow administration',
      directT: 'FMMM · Antonio · Shaila · JDAM · Laura Patricia',
      directP: 'Gil directly accuses Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila María Cogolludo Ramos, José Daniel Acosta Matos and Laura Patricia Acosta Matos of coordinating functions across debt and voting, access and security, keys, maintenance, works and valuation, information, finance and exit, operation, income, title and outcome. The contemporaneous email source literal describes the CAM lawyer as <span data-source-literal>“Laura Matos”</span>; the repository’s canonical identity is Laura Patricia Acosta Matos. Function, instruction, knowledge, intent and causation remain actor-specific production demands.',
      acK: 'Direct criminal allegation 2 · insolvency administrator',
      acT: 'Affirmative criminal enablement plus omission',
      acP: 'Gil directly alleges that the administrator supplied and used the authority route through emails, meetings, requests, authorisations, decisions, implementation, adoption and ratification, and also failed to delimit, supervise, restore, reverse and account. The administrator’s denial and narrower-access account remain material contrary evidence. Scope, knowledge, power and duty, intent and causation remain decisive proof questions.',
      judgeK: 'Direct criminal allegation 3 · court',
      judgeT: 'Affirmative judicial acts, omissions and alleged sabotage of the exit',
      judgeP: 'Gil directly alleges that specified decisions, refusals, evidential closures, delays and omissions by Judge Alberto López Villarrubia knowingly preserved the private-control result and sabotaged or frustrated a developed, multi-route, finance-backed exit. Gil characterises the sequence as knowing judicial prevarication under the legally applicable forms; that is his direct allegation, not an adjudicated finding. The 13 June 2018 Irigoyen report supports one direct judge meeting; further visits remain unproved. Each act requires the evidence then before the judge, competence and duty, objective injustice or malicious delay, knowledge, purpose and causation.',
      identityT: 'Attribution and source-fidelity control — Laura Patricia Acosta Matos',
      identityP: 'Laura Patricia Acosta Matos is the canonical identity and Gil directly attributes actor-specific participation and responsibility to her. Identity, mandate, presence, exact instructions, knowledge, purpose and criminal responsibility remain separate fields. A source literal is preserved as written and is not silently rewritten as the canonical identity.',
      documentedT: 'What is already documented',
      documentedP: 'Contemporaneous emails; same-day videos and photographs; pre-event and same-day criminal pleadings; the 18 May Community/security node; the creditor/title record; later control and project benefit; and institutional decisions or omissions. These evidence classes make the direct allegations concrete and publishable as attributed allegations; they do not make guilt adjudicated.',
      contraryT: 'Contrary record preserved',
      contraryP: 'The 2018 criminal proceedings were provisionally dismissed and that result was upheld on appeal. The administrator denied the principal lock-takeover instruction and described narrower access. CAM had valid creditor rights and may have held valid individual titles. Later adjudication remains legally distinct and non-retroactive.',
      open: 'Open the complete direct criminal-attribution and proof matrix',
      badge: 'Direct allegation ≠ adjudicated finding',
      nav: 'Criminal attribution',
      control: 'Publication control: merged, publicly verified and recoverable without the originating chat. Open evidence remains identified.',
      controlLabel: 'Open the machine-readable closeout record'
    } : {
      eyebrow: 'ATRIBUCIÓN PENAL EXPRESA · ACTUALIZADO 24 AGOSTO 2026',
      title: 'Cinco administradores en la sombra alegados, habilitación concursal afirmativa y atribución directa de culpabilidad judicial',
      lead: 'Gil Marer y Aweswell alegan directamente que cinco actores privados identificados operaron, a más tardar en 2018, como una estructura coordinada de administradores de hecho o en la sombra sobre la esfera patrimonial y empresarial de Luchy Playa Blanca y la plataforma hotelera integrada, mediante conductas dentro del concurso formal y fuera de su perímetro registrado; que el administrador concursal habilitó penalmente la estructura mediante actos afirmativos y omisiones; y que el Magistrado-Juez Alberto López Villarrubia la preservó mediante resoluciones, negativas, demoras y omisiones concretas, saboteando o frustrando con ello una salida desarrollada y respaldada por financiación. Son las acusaciones penales directas rectoras, no meras preguntas ni declaraciones judiciales.',
      directK: 'Atribución penal directa 1 · administración privada en la sombra',
      directT: 'FMMM · Antonio · Shaila · JDAM · Laura Patricia',
      directP: 'Gil acusa directamente a Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila María Cogolludo Ramos, José Daniel Acosta Matos y Laura Patricia Acosta Matos de coordinar funciones sobre deuda y voto, acceso y seguridad, llaves, mantenimiento, obras y valoración, información, financiación y salida, operación, ingresos, título y resultado. El literal de fuente del correo contemporáneo describe a la abogada CAM como <span data-source-literal>“Laura Matos”</span>; la identidad canónica es Laura Patricia Acosta Matos. Función, instrucción, conocimiento, intención y causalidad siguen siendo requerimientos actor-específicos de producción.',
      acK: 'Atribución penal directa 2 · administrador concursal',
      acT: 'Habilitación penal afirmativa más omisión',
      acP: 'Gil alega directamente que el administrador suministró y utilizó la vía de autoridad mediante correos, reuniones, peticiones, autorizaciones, decisiones, implementación, adopción y ratificación, y que además omitió delimitar, supervisar, restaurar, revertir y rendir cuentas. La negativa del administrador y su explicación de acceso más limitado permanecen como prueba contraria material. Alcance, conocimiento, poder y deber, intención y causalidad siguen siendo cuestiones probatorias decisivas.',
      judgeK: 'Atribución penal directa 3 · juzgado',
      judgeT: 'Actos judiciales afirmativos, omisiones y sabotaje alegado de la salida',
      judgeP: 'Gil alega directamente que resoluciones, negativas, cierres probatorios, demoras y omisiones concretas del Magistrado-Juez Alberto López Villarrubia preservaron conscientemente el control privado y sabotearon o frustraron una salida desarrollada, multivía y respaldada por financiación. Gil califica la secuencia como prevaricación judicial consciente en las modalidades jurídicamente aplicables; es una alegación directa, no una conclusión judicial. El informe Irigoyen de 13 de junio de 2018 sustenta una reunión directa con el juez; otras visitas siguen sin probarse. Cada acto exige prueba entonces ante el juez, competencia y deber, injusticia objetiva o demora maliciosa, conocimiento, finalidad y causalidad.',
      identityT: 'Control de atribución y fidelidad de fuente — Laura Patricia Acosta Matos',
      identityP: 'Laura Patricia Acosta Matos es la identidad canónica y Gil le atribuye directamente participación y responsabilidad actor-específica. Identidad, mandato, presencia, instrucciones exactas, conocimiento, finalidad y responsabilidad penal son campos separados. El literal de una fuente se conserva como fue escrito y no se sustituye silenciosamente por la identidad canónica.',
      documentedT: 'Lo que ya está documentado',
      documentedP: 'Correos contemporáneos; vídeos y fotos del mismo día; denuncias anteriores y coetáneas; nodo Comunidad/seguridad de 18 de mayo; registro de crédito/título; control y beneficio de proyecto posteriores; y decisiones u omisiones institucionales. Estas clases de prueba hacen concretas y publicables como atribuidas las acusaciones directas; no convierten la culpabilidad en declarada.',
      contraryT: 'Registro contrario preservado',
      contraryP: 'Las diligencias penales de 2018 fueron archivadas provisionalmente y el resultado se confirmó en apelación. El administrador negó la instrucción de la toma principal y describió un acceso más limitado. CAM tenía derechos acreedores válidos y puede haber tenido títulos individuales válidos. La adjudicación posterior es jurídicamente distinta y no retroactiva.',
      open: 'Abrir la matriz completa de atribución penal directa y prueba',
      badge: 'Acusación directa ≠ declaración judicial',
      nav: 'Atribución penal',
      control: 'Control de publicación: fusionado, verificado públicamente y recuperable sin el chat de origen. La prueba pendiente sigue identificada.',
      controlLabel: 'Abrir el registro de cierre legible por máquina'
    };

    const section = document.createElement('section');
    section.className = 'section alt cam-criminal-lead';
    section.dataset.camCriminalLead = '20260824';
    section.innerHTML = `<div class="shell">
      <header class="camcl-head"><p class="kicker">${c.eyebrow}</p><h2>${c.title}</h2><p class="camcl-lead">${c.lead}</p><span class="camcl-badge">${c.badge}</span><p class="camcl-control">${c.control} <a href="${controlHref}">${c.controlLabel}</a>.</p></header>
      <div class="camcl-grid">
        <article><span>${c.directK}</span><h3>${c.directT}</h3><p>${c.directP}</p></article>
        <article><span>${c.acK}</span><h3>${c.acT}</h3><p>${c.acP}</p></article>
        <article><span>${c.judgeK}</span><h3>${c.judgeT}</h3><p>${c.judgeP}</p></article>
      </div>
      <div class="camcl-split"><article class="camcl-identity"><h3>${c.identityT}</h3><p>${c.identityP}</p></article><article><h3>${c.documentedT}</h3><p>${c.documentedP}</p></article><article class="camcl-contrary"><h3>${c.contraryT}</h3><p>${c.contraryP}</p></article></div>
      <a class="dossier-link camcl-link" href="${href}"><span>${c.eyebrow}</span><strong>${c.open}</strong><i aria-hidden="true">→</i></a>
    </div>`;

    const style = document.createElement('style');
    style.dataset.camCriminalLeadStyle = '20260824';
    style.textContent = `
      .cam-criminal-lead{position:relative;overflow:hidden;background:linear-gradient(145deg,#f7f1ed,#edf3f3)}
      .cam-criminal-lead:before{content:"CONTROL";position:absolute;right:-.04em;top:.05em;font-size:clamp(5rem,14vw,12rem);font-weight:900;letter-spacing:-.07em;color:rgba(19,37,45,.035);pointer-events:none}
      .camcl-head{position:relative;max-width:1000px}.camcl-head h2{max-width:900px}.camcl-lead{font-size:1.08rem;line-height:1.67;max-width:980px}.camcl-badge{display:inline-block;margin:.5rem 0 1rem;border-radius:999px;padding:.35rem .65rem;background:#13252d;color:#fff;font-size:.73rem;font-weight:900;letter-spacing:.06em;text-transform:uppercase}.camcl-control{max-width:920px;margin:.2rem 0 1.15rem;padding:.7rem .85rem;border-left:4px solid #526b59;background:rgba(255,255,255,.72);font-size:.88rem;line-height:1.5}.camcl-control a{font-weight:800}
      .camcl-grid{position:relative;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.9rem}.camcl-grid article,.camcl-split article{border:1px solid rgba(19,37,45,.15);border-radius:15px;background:#fff;padding:1rem;box-shadow:0 .65rem 1.6rem rgba(19,37,45,.05)}
      .camcl-grid article{border-top:5px solid #8c2f2c}.camcl-grid article:nth-child(2){border-top-color:#8c6b2f}.camcl-grid article:nth-child(3){border-top-color:#5b5578}.camcl-grid span{display:block;margin-bottom:.35rem;font-size:.72rem;font-weight:900;text-transform:uppercase;letter-spacing:.07em;color:#7b2e2e}.camcl-grid h3,.camcl-split h3{margin:.15rem 0 .5rem}.camcl-grid p,.camcl-split p{line-height:1.57}
      .camcl-split{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.9rem;margin:1rem 0}.camcl-identity{border-left:6px solid #8c6b2f!important;background:#fffaf0!important}.camcl-contrary{border-left:6px solid #526b59!important;background:#f3f7f5!important}.camcl-link{margin-top:.7rem}
      [data-source-literal]{font-style:italic;text-decoration:underline dotted;text-underline-offset:.18em}
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

(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const isEN = document.documentElement.lang?.toLowerCase().startsWith('en') || path.includes('/en/');
  const isHome = /^\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(path);
  if (!isHome || document.querySelector('[data-pd-home-future="20260916"]')) return;

  const section = document.querySelector(isEN ? '#future' : '#futuro');
  if (!section) return;

  const root = '/por-derecho/' + (isEN ? 'en/' : 'es/');
  const routes = {
    montana: root + 'montana-roja/',
    scale: root + (isEN ? 'platform-scale/' : 'escala-plataforma/'),
    relationship: root + (isEN ? 'strategic-financial-relationship/' : 'relacion-financiera-estrategica/'),
    capital: root + (isEN ? 'capital-relationships/' : 'relaciones-de-capital/')
  };

  const t = isEN ? {
    intro: 'Sun Rock has made the strategic decision to re-establish a hotel position in Playa Blanca. Montaña Roja is the preferred current route being actively pursued; the transaction and delivery route still have to be proven. The wider platform is built asset by asset, with Aweswell Limited as UK HoldCo / Sponsor and ring-fenced ProjectCos beneath Sun Rock.',
    kicker: 'CURRENT STRATEGIC DIRECTION · PLAYA BLANCA · PLATFORM · RELATIONSHIP',
    title: 'The intention is clear. Execution remains disciplined.',
    cards: [
      ['01 · PLAYA BLANCA', 'Playa Blanca is an active objective, not a speculative theme.', 'Montaña Roja is the preferred current route. Due diligence now determines what must be acquired or controlled and whether the project can be delivered on its ordinary legal, planning, technical, economic and financial merits.', routes.montana, 'Open Montaña Roja'],
      ['02 · PLATFORM SCALE', 'A €150m-class hospitality platform in the making.', '~560–600 hotel units · €40–58m annual revenue · €10–18m operating EBITDA · €125–200m indicative gross hotel assets. Illustrative stabilised management scenario only—not a forecast, current NAV, current valuation, committed financing or present collateral.', routes.scale, 'Open platform scale'],
      ['03 · FINANCIAL RELATIONSHIP', 'Family · Aweswell · Sun Rock · ring-fenced ProjectCos.', 'A long-term institution can have three independent reasons to engage: family/private wealth, Aweswell/Sun Rock corporate banking and separately underwritten hotel projects. One relationship does not collapse credit risks or imply that every desk or capital pool will invest.', routes.relationship, 'Open relationship architecture'],
      ['04 · CAPITAL RELATIONSHIPS', 'A private conversation begins with fit, not public terms.', 'A principal, family office, hotel-owning family, institutional/professional capital provider or trusted introducer can understand the public doorway before role, jurisdiction, communication basis, confidentiality and diligence are handled privately. No public investment or subscription route.', routes.capital, 'Open capital gateway']
    ],
    boundary: 'HARD BOUNDARY · SUN PARK RECOVERY AND MONTAÑA ROJA REMAIN LEGALLY AND FINANCIALLY INDEPENDENT. UNRESOLVED RECOVERY IS NOT ADDED TO THE HOTEL-ASSET RANGE AND IS NOT ORDINARY PROJECT DEBT-SERVICE SUPPORT.',
    audience: '<strong>Who this is for:</strong> hotel/property principals, sophisticated family capital, private-wealth and corporate-banking teams, hotel-finance/private-credit, institutional counterparties and trusted direct introducers able to assess either a long-term relationship or a specific ring-fenced asset. This public page is informational only: there is no public investment route, retail subscription or representation of committed financing.',
    conversationKicker: 'Institutional relationship',
    conversationTitle: 'Start with architecture, then use the controlled doorway.',
    conversationText: 'A first conversation can test fit across family/private wealth, Aweswell/Sun Rock corporate banking, a ring-fenced ProjectCo or a wider principal-capital relationship. The public site stops before investment terms: role, jurisdiction, legal communication basis, confidentiality and diligence belong in the private process.',
    capitalButton: 'Capital relationships',
    relationshipButton: 'Strategic financial relationship'
  } : {
    intro: 'Sun Rock ha tomado la decisión estratégica de restablecer una posición hotelera en Playa Blanca. Montaña Roja es la vía preferente actual que se está impulsando activamente; la operación y la vía de ejecución todavía deben demostrarse. La plataforma se construye activo por activo, con Aweswell Limited como HoldCo británica / Sponsor y ProjectCos segregadas bajo Sun Rock.',
    kicker: 'DIRECCIÓN ESTRATÉGICA ACTUAL · PLAYA BLANCA · PLATAFORMA · RELACIÓN',
    title: 'La intención es clara. La ejecución sigue siendo disciplinada.',
    cards: [
      ['01 · PLAYA BLANCA', 'Playa Blanca es un objetivo activo, no una hipótesis abstracta.', 'Montaña Roja es la vía preferente actual. La due diligence determina ahora qué debe adquirirse o controlarse y si el proyecto puede ejecutarse conforme a sus propios méritos jurídicos, urbanísticos, técnicos, económicos y financieros.', routes.montana, 'Abrir Montaña Roja'],
      ['02 · ESCALA DE PLATAFORMA', 'Una plataforma hotelera de clase ~€150m en formación.', '~560–600 unidades hoteleras · €40–58m de ingresos anuales · €10–18m de EBITDA operativo · €125–200m de activos hoteleros brutos indicativos. Escenario de gestión estabilizado e ilustrativo solamente: no es previsión, NAV actual, valoración actual, financiación comprometida ni garantía presente.', routes.scale, 'Abrir escala de plataforma'],
      ['03 · RELACIÓN FINANCIERA', 'Familia · Aweswell · Sun Rock · ProjectCos segregadas.', 'Una institución de largo plazo puede tener tres razones independientes para relacionarse: patrimonio privado/familiar, banca corporativa de Aweswell/Sun Rock y proyectos hoteleros analizados por separado. Una relación no fusiona riesgos de crédito ni implica que todas las mesas o bolsas de capital vayan a invertir.', routes.relationship, 'Abrir arquitectura relacional'],
      ['04 · RELACIONES DE CAPITAL', 'Una conversación privada empieza por el encaje, no por condiciones públicas.', 'Un principal, family office, familia propietaria de hoteles, proveedor institucional/profesional de capital o introductor de confianza puede entender primero la puerta pública; función, jurisdicción, base de comunicación, confidencialidad y diligencia se gestionan después en privado. Sin vía pública de inversión o suscripción.', routes.capital, 'Abrir puerta de capital']
    ],
    boundary: 'LÍMITE FIRME · LA RECUPERACIÓN DE SUN PARK Y MONTAÑA ROJA PERMANECEN JURÍDICA Y FINANCIERAMENTE INDEPENDIENTES. LAS RECUPERACIONES NO RESUELTAS NO SE SUMAN AL RANGO DE ACTIVOS HOTELEROS NI SON SOPORTE ORDINARIO DEL SERVICIO DE DEUDA DEL PROYECTO.',
    audience: '<strong>A quién se dirige:</strong> a empresarios hoteleros o inmobiliarios, capital familiar sofisticado, equipos de banca privada y corporativa, financiación hotelera/crédito privado, contrapartes institucionales e introductores directos de confianza capaces de evaluar una relación de largo plazo o un activo segregado concreto. Esta página pública es meramente informativa: no existe vía pública de inversión, suscripción minorista ni afirmación de financiación comprometida.',
    conversationKicker: 'Relación institucional',
    conversationTitle: 'Empezar por la arquitectura y después utilizar la puerta controlada.',
    conversationText: 'Una primera conversación puede comprobar el encaje en patrimonio privado/familiar, banca corporativa de Aweswell/Sun Rock, una ProjectCo segregada o una relación más amplia de capital principal. La web pública termina antes de las condiciones: función, jurisdicción, base jurídica de comunicación, confidencialidad y diligencia pertenecen al proceso privado.',
    capitalButton: 'Relaciones de capital',
    relationshipButton: 'Relación financiera estratégica'
  };

  const style = document.createElement('style');
  style.id = 'pd-home-future-institutional-style';
  style.textContent = `
    .pd-home-future-bridge{margin:1.25rem 0 2rem;border:1px solid rgba(19,47,56,.14);border-radius:26px;overflow:hidden;background:#fff;box-shadow:0 18px 42px rgba(13,47,56,.08)}
    .pd-home-future-head{padding:clamp(1.25rem,3vw,2rem);background:linear-gradient(135deg,#0d2f38,#1e5660 60%,#7b5c24);color:#fff}
    .pd-home-future-head *{color:#fff}.pd-home-future-head span{display:block;font-size:.7rem;font-weight:900;letter-spacing:.09em;color:#f4d98c;text-transform:uppercase}
    .pd-home-future-head h3{font-size:clamp(1.8rem,3.4vw,2.75rem);line-height:1.05;letter-spacing:-.025em;margin:.42rem 0 0;max-width:22ch}
    .pd-home-future-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:rgba(13,47,56,.12)}
    .pd-home-future-card{background:#fff;padding:1.2rem;display:flex;flex-direction:column;min-height:330px}
    .pd-home-future-card .tag{font-size:.7rem;font-weight:900;letter-spacing:.08em;color:#8a6330;text-transform:uppercase}
    .pd-home-future-card h4{font-size:1.2rem;line-height:1.2;color:#132f38;margin:.45rem 0 .65rem}
    .pd-home-future-card p{color:#4a5d63;line-height:1.58;font-size:.9rem;margin:0 0 1rem}
    .pd-home-future-card a{margin-top:auto;align-self:flex-start;text-decoration:none;background:#132f38;color:#fff;border-radius:999px;padding:.52rem .76rem;font-size:.8rem;font-weight:850}
    .pd-home-future-boundary{padding:.9rem 1.15rem;background:#fff6dc;color:#654711;border-top:1px solid #ead19a;font-size:.77rem;font-weight:900;letter-spacing:.035em;line-height:1.45}
    @media(max-width:1050px){.pd-home-future-grid{grid-template-columns:1fr 1fr}.pd-home-future-card{min-height:270px}}
    @media(max-width:700px){.pd-home-future-grid{grid-template-columns:1fr}.pd-home-future-card{min-height:0}}
  `;
  document.head.appendChild(style);

  const head = section.querySelector('.section-head');
  const intro = head?.querySelector(':scope > p');
  if (intro) intro.textContent = t.intro;

  const bridge = document.createElement('div');
  bridge.className = 'pd-home-future-bridge';
  bridge.dataset.pdHomeFuture = '20260916';
  bridge.innerHTML = `
    <div class="pd-home-future-head"><span>${t.kicker}</span><h3>${t.title}</h3></div>
    <div class="pd-home-future-grid">
      ${t.cards.map(card => `<article class="pd-home-future-card"><div class="tag">${card[0]}</div><h4>${card[1]}</h4><p>${card[2]}</p><a href="${card[3]}">${card[4]} →</a></article>`).join('')}
    </div>
    <div class="pd-home-future-boundary">${t.boundary}</div>`;
  head?.after(bridge);

  const audience = section.querySelector('.audience-note p');
  if (audience) audience.innerHTML = t.audience;

  const conversation = section.querySelector('.private-conversation');
  if (conversation) {
    conversation.innerHTML = `
      <div><p class="kicker">${t.conversationKicker}</p><h3>${t.conversationTitle}</h3><p>${t.conversationText}</p></div>
      <div class="actions"><a class="button" href="${routes.capital}">${t.capitalButton}</a><a class="button secondary" href="${routes.relationship}">${t.relationshipButton}</a></div>`;
  }
})();

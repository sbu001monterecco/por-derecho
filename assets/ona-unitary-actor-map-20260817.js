(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const es = path.endsWith('/es/ona-hotels-salida-concurso-36-2012/');
  const en = path.endsWith('/en/ona-hotels-insolvency-exit-36-2012/');
  if (!es && !en) return;
  if (document.querySelector('[data-ona-unitary-map-20260817]')) return;

  const style = document.createElement('style');
  style.textContent = `
    .ona-unitary{padding:1.2rem 0 2rem;background:#f6f4ee}.ona-unitary-wrap{max-width:1080px;margin:0 auto}.ona-unitary-box{background:#fff;border:2px solid #13252d;border-radius:20px;padding:1.35rem 1.45rem}.ona-unitary-box h2{margin:.2rem 0 .65rem;font-size:clamp(1.55rem,3.2vw,2.25rem)}.ona-unitary-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin-top:1rem}.ona-unitary-card{border:1px solid rgba(19,37,45,.16);border-radius:14px;padding:.95rem;background:#fafafa}.ona-unitary-card strong{display:block;margin-bottom:.35rem}.ona-unitary-card.anchor{border-top:5px solid #526b59}.ona-unitary-card.owner{border-top:5px solid #8c6b2f}.ona-unitary-card.legal{border-top:5px solid #13252d}.ona-unitary-note{margin-top:1rem;padding:1rem 1.1rem;background:#13252d;color:#fff;border-radius:14px}.ona-unitary-boundary{margin-top:.8rem;font-size:.9rem;color:#555}@media(max-width:820px){.ona-unitary-grid{grid-template-columns:1fr}.ona-unitary-box{border-radius:0}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.className = 'ona-unitary';
  section.dataset.onaUnitaryMap20260817 = '1';
  section.innerHTML = es ? `<div class="shell ona-unitary-wrap"><div class="ona-unitary-box">
    <p class="eyebrow">QUIÉN ERA QUIÉN · LA ARQUITECTURA REAL DE 2018</p>
    <h2>No era una sola empresa, un solo activo ni una sola función</h2>
    <p>La salida propuesta tenía que coordinar capas jurídicamente distintas. <strong>LPB era la concursada y, en términos funcionales, la principal sociedad propietaria inmobiliaria dentro de un complejo de propiedad mixta; no era “el hotel entero” ni equivalía a la explotación hotelera.</strong></p>
    <div class="ona-unitary-grid">
      <article class="ona-unitary-card owner"><strong>Aweswell / LPB</strong><span>Aweswell estaba en el lado accionista/inversor. LPB era la deudora concursada y principal propietaria inmobiliaria, junto a otros propietarios jurídicamente distintos.</span></article>
      <article class="ona-unitary-card anchor"><strong>Clubotel La Dorada / ONA Hotels</strong><span>El contrato firmado de 6-Jun-2018 coloca a Clubotel La Dorada, S.L. en el lado operador. ONA Hotels era el <em>ancla operativa</em> de la salida, no necesariamente el líder jurídico o financiero de cada componente.</span></article>
      <article class="ona-unitary-card"><strong>Propiedad ≠ explotación</strong><span>El propio contrato distingue la Comunidad de Propietarios de la histórica Comunidad de Explotación. La propiedad, el gobierno del complejo y la explotación hotelera eran capas distintas.</span></article>
      <article class="ona-unitary-card legal"><strong>Daniel Irigoyen</strong><span>Magistrado de carrera y especialista mercantil que constaba en excedencia voluntaria; en 2018 actuaba como abogado. Su relato de 13-Jun dice que ante el Juez se presentó para coordinar inversor, sociedad accionista, concursada y hotelero.</span></article>
      <article class="ona-unitary-card legal"><strong>Cuatrecasas</strong><span>No sólo DD: trabajó en contratos con ONA, revisión inmobiliaria/registral, garantías, term sheets y documentación financiera, coordinación transaccional y escritos/estrategia para cuantificar la deuda y avanzar la salida.</span></article>
      <article class="ona-unitary-card"><strong>Financiación + garantías</strong><span>Existieron rutas externas paralelas y sucesivas. La documentación distingue garantías provisionales/pre-salida y garantías posteriores, incluida la hipoteca de LPB cuando pudiera constituirse.</span></article>
    </div>
    <div class="ona-unitary-note"><strong>La descripción más precisa:</strong> una <strong>arquitectura coordinada de salida articulada alrededor de ONA Hotels como ancla operativa</strong>, con Aweswell/LPB en el lado accionista/deudor/propietario, financiación externa y un equipo jurídico-transaccional.</div>
    <p class="ona-unitary-boundary"><strong>Límite:</strong> no se presenta como un “joint venture” formal sin localizar un contrato de JV. Una certificación posterior de 2021 confirma propiedad mixta (190 fincas LPB, 54 CAM y 18 terceros sobre 262), pero ese porcentaje exacto no se retrotrae automáticamente a junio de 2018.</p>
  </div></div>` : `<div class="shell ona-unitary-wrap"><div class="ona-unitary-box">
    <p class="eyebrow">WHO WAS WHO · THE REAL 2018 ARCHITECTURE</p>
    <h2>This was not one company, one asset or one legal function</h2>
    <p>The proposed exit had to coordinate legally distinct layers. <strong>LPB was the insolvent debtor and, functionally, the principal property-owning company within a mixed-ownership complex; it was not “the whole hotel” and was not legally identical to hotel exploitation.</strong></p>
    <div class="ona-unitary-grid">
      <article class="ona-unitary-card owner"><strong>Aweswell / LPB</strong><span>Aweswell sat on the shareholder/investor side. LPB was the insolvent debtor and principal property owner alongside other legally distinct owners.</span></article>
      <article class="ona-unitary-card anchor"><strong>Clubotel La Dorada / ONA Hotels</strong><span>The signed 6-Jun-2018 contract places Clubotel La Dorada, S.L. on the operator side. ONA Hotels was the <em>operating anchor</em>, not necessarily legal or financial leader of every component.</span></article>
      <article class="ona-unitary-card"><strong>Ownership ≠ exploitation</strong><span>The contract itself distinguishes the Community of Owners from the historical exploitation Community. Property, complex governance and hotel exploitation were distinct layers.</span></article>
      <article class="ona-unitary-card legal"><strong>Daniel Irigoyen</strong><span>A career magistrate and mercantile specialist recorded on voluntary leave; in 2018 he was acting as a lawyer. His 13-Jun account says he presented himself to the Judge to coordinate investor, shareholder company, insolvent company and hotel operator.</span></article>
      <article class="ona-unitary-card legal"><strong>Cuatrecasas</strong><span>Far more than DD: ONA contracts, property/registry review, security structuring, term sheets and finance documents, transaction coordination and court/insolvency work directed at quantifying the debt and advancing exit.</span></article>
      <article class="ona-unitary-card"><strong>Finance + security</strong><span>Parallel and successive external routes existed. The documents distinguish provisional/pre-exit security from later security, including the LPB mortgage once it could be created.</span></article>
    </div>
    <div class="ona-unitary-note"><strong>The most precise description:</strong> an <strong>ONA Hotels-centred coordinated exit architecture</strong>, with Aweswell/LPB on the shareholder/debtor/property side, external finance and a legal/transaction team.</div>
    <p class="ona-unitary-boundary"><strong>Boundary:</strong> this is not described as a formal joint venture unless a JV instrument is located. A later 2021 certification confirms mixed ownership (190 LPB, 54 CAM and 18 third-party properties out of 262), but that exact ratio is not automatically back-projected to June 2018.</p>
  </div></div>`;

  const hero = document.querySelector('.hero.ona-hero') || document.querySelector('main .hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
})();
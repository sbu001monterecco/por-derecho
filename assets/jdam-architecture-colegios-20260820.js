(() => {
  const path = window.location.pathname.replace(/index\.html$/, '');
  const es = path.includes('/es/');
  const target = es ? '/por-derecho/es/arquitectura-nodo-documental-jdam/' : '/por-derecho/en/architecture-documentary-node-jdam/';
  const label = es ? 'Arquitectura' : 'Architecture';
  const title = es ? 'Arquitectura como nodo documental' : 'Architecture as a documentary node';
  const text = es
    ? 'El visado de 25/02/2022 se integra en una cadena que conecta autoridad aparente, encargo, proyecto, Yaiza, turismo, inversión, financiación, RIC/REF, incentivos, operación y prueba judicial. El registro separa hechos, alegaciones, límites y preguntas finitas para COALZ y COAGC.'
    : 'The 25 February 2022 visado sits within a chain connecting apparent authority, commission, project, Yaiza, tourism, investment, finance, RIC/REF, public support, operation and judicial evidence. The record separates facts, allegations, limits and finite questions for COALZ and COAGC.';
  const relevant = [
    '/es/', '/en/', 'acosta-matos-perimetro', 'acosta-matos-perimeter',
    'comunidad-instrumentalizacion', 'community-instrumentalisation',
    'mismo-hotel-multiples-vidas-financieras', 'same-hotel-multiple-financial-lives',
    'ric-private-equity-sun-park', 'ricpe-responsabilidad-documental', 'ricpe-documentary-accountability',
    'san-telmo-ricpe-sun-park', 'pwc-canarias-carlos-saavedra-sun-park',
    'pwc-canary-islands-carlos-saavedra-sun-park', 'grant-thornton/2024-04',
    'rsm/nnr4-1025c2f66', 'cabildo-lanzarote-turismo-trazabilidad',
    'cabildo-lanzarote-tourism-traceability', 'actualizaciones', 'updates'
  ].some(x => path === '/por-derecho' + x || path.includes(x));

  const style = document.createElement('style');
  style.textContent = `.jdam-architecture-gateway{max-width:1120px;margin:1.5rem auto;padding:1.15rem 1.25rem;border-radius:16px;background:#f6f1e5;border:1px solid rgba(19,37,45,.18);border-left:6px solid #9a6813;box-sizing:border-box}.jdam-architecture-gateway strong{display:block;font-size:1.2rem;margin-bottom:.35rem}.jdam-architecture-gateway p{margin:.35rem 0 .75rem;line-height:1.55}.jdam-architecture-gateway a{font-weight:850}.jdam-update{border-left-color:#9a6813!important}`;
  document.head.appendChild(style);

  const inject = () => {
    document.querySelectorAll('.main-nav').forEach(nav => {
      if (nav.querySelector('[data-jdam-architecture-nav]')) return;
      const a = document.createElement('a');
      a.href = target; a.textContent = label; a.dataset.jdamArchitectureNav = 'true';
      const lang = nav.querySelector('.language-link');
      if (lang) nav.insertBefore(a, lang); else nav.appendChild(a);
    });

    if (relevant && !path.includes('arquitectura-nodo-documental-jdam') && !path.includes('architecture-documentary-node-jdam') && !document.querySelector('.jdam-architecture-gateway')) {
      const box = document.createElement('aside');
      box.className = 'jdam-architecture-gateway';
      box.setAttribute('data-jdam-architecture-gateway','2026-08-20');
      box.innerHTML = `<strong>${title}</strong><p>${text}</p><a href="${target}">${es ? 'Abrir el registro JDAM / COALZ / COAGC →' : 'Open the JDAM / COALZ / COAGC record →'}</a>`;
      const hero = document.querySelector('main .hero, main section');
      if (hero) hero.insertAdjacentElement('afterend', box);
    }

    const updates = document.querySelector('.updates-page main');
    if (updates && !document.querySelector('#jdam-arquitectura-colegios-20ago')) {
      const section = document.createElement('section');
      section.className = 'updates-section';
      section.innerHTML = `<div class="shell"><section class="date-group"><h2>20 ${es?'agosto':'August'} 2026 · ${es?'arquitectura y deontología':'architecture and professional conduct'}</h2><div class="update-stream"><article class="material-update institutional jdam-update" id="jdam-arquitectura-colegios-20ago"><div class="update-meta"><span class="new">${es?'Nuevo':'New'}</span><span>JDAM</span><span>COALZ / COAGC</span></div><h3>${title}</h3><p>${text}</p><p>${es?'COALZ recibió tres entradas en julio y trasladó el material a su Junta. El 20 de agosto se remitió una ampliación en el hilo previo. COAGC recibió una comunicación separada y una redistribución por los cuatro canales funcionales utilizados en julio. Envío no equivale a investigación abierta ni decisión de fondo.':'COALZ received three July entries and passed the material to its Board. A supplemental communication was sent in the existing thread on 20 August. COAGC received a separate communication and redistribution through the four functional channels used in July. Sending does not mean an investigation or merits decision.'}</p><div class="update-actions"><a class="button" href="${target}">${es?'Abrir registro →':'Open record →'}</a></div></article></div></section></div>`;
      updates.insertBefore(section, updates.firstChild.nextSibling || updates.firstChild);
      const status = document.querySelector('.update-status strong');
      if (status) status.textContent = es ? '20 agosto 2026' : '20 August 2026';
    }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject, {once:true}); else inject();
})();
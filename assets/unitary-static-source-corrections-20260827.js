(() => {
  if (window.__pdUnitaryStaticSourceCorrections20260827) return;
  window.__pdUnitaryStaticSourceCorrections20260827 = true;

  const normalise = value => {
    let p = value.replace(/\/index\.html$/, '/');
    if (!p.endsWith('/')) p += '/';
    return p;
  };
  const path = normalise(location.pathname);
  const isEn = document.documentElement.lang === 'en';
  const basePrefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const bridgeHref = isEn ? `${basePrefix}en/five-documentary-bridges/` : `${basePrefix}es/cinco-puentes-documentales/`;
  const bridgeLabel = isEn ? 'Five documentary bridges' : 'Cinco puentes documentales';

  const addBridgeAction = actions => {
    if (!actions || actions.querySelector('[data-five-bridges-action]')) return;
    const a = document.createElement('a');
    a.className = 'button secondary';
    a.href = bridgeHref;
    a.dataset.fiveBridgesAction = '20260827';
    a.textContent = bridgeLabel;
    actions.appendChild(a);
  };

  const correctCommunity = () => {
    const enRoute = path.endsWith('/en/community-instrumentalisation/');
    const esRoute = path.endsWith('/es/comunidad-instrumentalizacion/');
    if (!enRoute && !esRoute) return;
    const banner = document.querySelector('.community-takeover-banner');
    if (banner) {
      const strongs = [...banner.querySelectorAll('strong')];
      const target = strongs.find(el => /NO POSSESSION OR EVICTION ORDER|NINGÚN AUTO DE POSESIÓN O DESALOJO/i.test(el.textContent || ''));
      if (target) {
        target.textContent = enRoute
          ? "NO POSSESSION OR EVICTION ORDER IN CAM'S FAVOUR HAS BEEN LOCATED IN THE REVIEWED RECORD"
          : 'NO SE HA LOCALIZADO EN EL EXPEDIENTE REVISADO UN AUTO DE POSESIÓN O DESALOJO A FAVOR DE CAM';
        target.dataset.controlledNoOrderWording = '20260827';
      }
      const intro = banner.querySelector('div span');
      if (intro) intro.textContent = enRoute ? '7 June 2018 · reviewed-record limit' : '7 junio 2018 · límite del expediente revisado';
      if (!banner.querySelector('[data-five-bridges-inline]')) {
        const p = document.createElement('p');
        p.dataset.fiveBridgesInline = '20260827';
        p.innerHTML = enRoute
          ? `<strong>Primary-record test:</strong> absence from the reviewed corpus is not proof of universal non-existence. The controlling question is what judicial, insolvency-administration or private authority actually supported the material-control change. <a href="${bridgeHref}">Open the five documentary bridges →</a>`
          : `<strong>Prueba de expediente primario:</strong> la ausencia en el corpus revisado no demuestra inexistencia universal. La cuestión rectora es qué autoridad judicial, concursal o privada sustentó realmente el cambio de control material. <a href="${bridgeHref}">Abrir los cinco puentes documentales →</a>`;
        banner.appendChild(p);
      }
    }
    addBridgeAction(document.querySelector('.dossier-hero .actions'));
  };

  const correctHomepage = () => {
    const home = /\/(en|es)\/$/.test(path);
    if (!home) return;
    const judgeName = document.querySelector('[data-institution-card="judge"] .pd-five-ac__institution-name');
    if (judgeName) {
      judgeName.textContent = isEn
        ? 'Ilmo. Sr. D. Alberto López Villarrubia — Magistrate-Judge of the then Commercial Court No. 1 of Las Palmas de Gran Canaria'
        : 'Ilmo. Sr. D. Alberto López Villarrubia, Magistrado-Juez del entonces Juzgado de lo Mercantil n.º 1 de Las Palmas de Gran Canaria';
      judgeName.dataset.controlledJudicialTitle = '20260827';
    }
    const role = document.querySelector('[data-institution-card="judge"] .pd-five-ac__institution-role');
    if (role) {
      role.textContent = isEn
        ? 'Historical role · judicial supervision and effective judicial protection · court title controlled by date'
        : 'Función histórica · supervisión judicial y tutela judicial efectiva · denominación del órgano controlada por fecha';
    }
    addBridgeAction(document.querySelector('.hero .actions'));
    const firstRead = document.querySelector('.pd-five-ac');
    if (firstRead && !document.querySelector('[data-five-bridges-home-gateway]')) {
      const section = document.createElement('section');
      section.className = 'section';
      section.dataset.fiveBridgesHomeGateway = '20260827';
      section.innerHTML = `<div class="shell"><aside class="pressure-maxim"><strong>${isEn ? 'Five finite tests' : 'Cinco pruebas finitas'}</strong><span>${isEn ? 'Instead of asking the reader to accept the whole theory at once, require the primary record that connects each conversion of authority, debt, control, title and value.' : 'En lugar de pedir al lector que acepte toda la tesis de una vez, exija el documento primario que conecta cada conversión de autoridad, deuda, control, título y valor.'} <a href="${bridgeHref}" style="color:inherit;font-weight:900">${bridgeLabel} →</a></span></aside></div>`;
      firstRead.insertAdjacentElement('afterend', section);
    }
  };

  const run = () => {
    correctCommunity();
    correctHomepage();
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, {once:true});
  else run();
})();

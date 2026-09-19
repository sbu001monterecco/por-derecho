(() => {
  'use strict';

  const normalise = value => {
    let p = value.replace(/\/index\.html$/, '/');
    if (!p.endsWith('/')) p += '/';
    return p;
  };
  const path = normalise(location.pathname);
  const routes = new Set([
    '/es/comunidad-instrumentalizacion/',
    '/en/community-instrumentalisation/',
    '/es/actores-partes-abogados-representantes/',
    '/en/actors-parties-lawyers-representatives/'
  ]);
  const matched = [...routes].find(r => path.endsWith(r));
  if (!matched || document.querySelector('[data-montelanza-accounts-discovery]')) return;

  const isEn = document.documentElement.lang === 'en';
  const target = isEn
    ? '/por-derecho/en/monte-lanza-2012-accounts/'
    : '/por-derecho/es/cuentas-monte-lanza-2012/';

  const section = document.createElement('section');
  section.className = 'section alt';
  section.dataset.montelanzaAccountsDiscovery = '20260919';
  section.innerHTML = `
    <div class="shell">
      <aside class="pressure-maxim" role="note">
        <strong>${isEn ? 'Primary source now digitised: Monte Lanza S.L. accounts' : 'Fuente primaria ya digitalizada: cuentas de Monte Lanza S.L.'}</strong>
        <span>${isEn
          ? 'The 30-page corporate/registry package preserves Monte Lanza’s own accounting statement about the 17 June 2008 sale, cessation of activity and placement of transferred assets at the purchaser’s disposal for exploitation. The source proves the company statement; it does not by itself prove later title, authority, fraud or criminal liability.'
          : 'El paquete corporativo/registral de 30 páginas conserva la propia declaración contable de Monte Lanza sobre la compraventa de 17 de junio de 2008, el cese de actividad y la puesta de los activos cedidos a disposición del adquirente para su explotación. La fuente prueba la declaración de la sociedad; no prueba por sí sola título posterior, autoridad, fraude ni responsabilidad penal.'
        }</span>
        <a class="button secondary" href="${target}">${isEn ? 'Open source package →' : 'Abrir paquete fuente →'}</a>
      </aside>
    </div>`;
  const main = document.querySelector('main');
  if (!main) return;
  const anchor = isEn ? document.querySelector('#structural-error') : document.querySelector('#error-estructural');
  if (anchor) anchor.insertAdjacentElement('afterend', section);
  else main.append(section);
})();

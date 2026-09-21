(() => {
  'use strict';
  const path = location.pathname.replace(/\/+$/, '/') || '/';
  const targets = new Map([
    ['/por-derecho/es/acosta-matos-perimetro/', {lang:'es', href:'../acosta-matos-plataforma-hotelera/'}],
    ['/por-derecho/es/ric-private-equity-sun-park/', {lang:'es', href:'../acosta-matos-plataforma-hotelera/'}],
    ['/por-derecho/es/ricpe-hnt-gc836-trazabilidad/', {lang:'es', href:'../acosta-matos-plataforma-hotelera/'}],
    ['/por-derecho/es/mismo-hotel-multiples-vidas-financieras/', {lang:'es', href:'../acosta-matos-plataforma-hotelera/'}],
    ['/por-derecho/en/acosta-matos-perimeter/', {lang:'en', href:'../acosta-matos-hotel-platform/'}],
    ['/por-derecho/en/ric-private-equity-sun-park/', {lang:'en', href:'../acosta-matos-hotel-platform/'}],
    ['/por-derecho/en/ricpe-hnt-gc836-traceability/', {lang:'en', href:'../acosta-matos-hotel-platform/'}],
    ['/por-derecho/en/same-hotel-multiple-financial-lives/', {lang:'en', href:'../acosta-matos-hotel-platform/'}]
  ]);
  const cfg = targets.get(path);
  if (!cfg || document.querySelector('[data-acosta-hotel-platform-media-link]')) return;

  const main = document.querySelector('main');
  if (!main) return;
  const section = document.createElement('section');
  section.className = 'section alt';
  section.setAttribute('data-acosta-hotel-platform-media-link', '20260901');
  const es = cfg.lang === 'es';
  section.innerHTML = `
    <div class="shell" style="max-width:1080px">
      <p class="eyebrow">${es ? 'NUEVO REGISTRO VISUAL · PD-DMA' : 'NEW VISUAL RECORD · PD-DMA'}</p>
      <h2>${es ? '12 hoteles · 2.500 habitaciones · +100 M€: separar ventas hoteleras, facturación propia y funciones de plataforma' : '12 hotels · 2,500 rooms · €100m+: separating hotel sales, own turnover and platform roles'}</h2>
      <p>${es ? 'La página bilingüe publica la caricatura controlada, su versión inglesa, dos variantes corregidas inspiradas en conceptos anteriores y el registro de hashes. Distingue propiedad, gestión, marca, capital, RIC/RICPE, construcción, mandato y cobertura mediática.' : 'The bilingual page publishes the controlled caricature, its English companion, two corrected variants inspired by earlier concepts and the hash register. It separates ownership, management, brand, capital, RIC/RICPE, construction, mandate and media coverage.'}</p>
      <p><strong>${es ? 'Límite:' : 'Boundary:'}</strong> ${es ? 'estar dentro de la misma plataforma visual no prueba propiedad común, conocimiento compartido ni responsabilidad.' : 'appearing within the same visual platform does not prove common ownership, shared knowledge or responsibility.'}</p>
      <p><a class="button" href="${cfg.href}">${es ? 'Abrir plataforma hotelera y activos PD-DMA →' : 'Open hotel platform and PD-DMA assets →'}</a></p>
    </div>`;
  main.appendChild(section);
})();

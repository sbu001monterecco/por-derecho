(() => {
  'use strict';
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalise(location.pathname);
  const isEnglish = document.documentElement.lang === 'en';
  const targets = new Set([
    '/es/comunidad-instrumentalizacion/',
    '/en/community-instrumentalisation/',
    '/es/comunidad-instrumentalizacion/actas-2011-2022/',
    '/en/community-instrumentalisation/minutes-2011-2022/',
    '/es/acosta-matos-perimetro/',
    '/en/acosta-matos-perimeter/',
    '/es/actores-privados-per-comunero-administracion-de-hecho/',
    '/en/private-actors-related-party-community-de-facto-administration/',
    '/es/ingenieria-inversa-360-cadena-sun-park/',
    '/en/reverse-engineering-360-sun-park-chain/',
    '/es/toma-control-sun-park-7-junio-2018/',
    '/en/sun-park-takeover-7-june-2018/',
    '/es/actualizaciones/',
    '/en/updates/'
  ]);
  if (![...targets].some(route => path.endsWith(route))) return;
  if (document.querySelector('[data-montelanza-governance-origin]')) return;

  const prefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const href = isEnglish
    ? `${prefix}en/montelanza-accounts-2008/`
    : `${prefix}es/montelanza-cuentas-2008/`;
  const copy = isEnglish ? {
    eyebrow: 'NEW PRIMARY-SOURCE BASELINE · 2008 → 2011',
    title: 'Montelanza’s 2008 accounts identify the governance-succession bridge that must be produced.',
    body: 'The accounts show a real tourism operator, a EUR 1.368m 17-June sale represented as placing transferred assets with the purchaser for operation, parallel apartment sales and an option over 11 unsold premises. They do not prove criminal capture. They show the “before” structure and sharpen the question of how title, CEXP authority, operation, books, costs and owner representation became the 2011 Community architecture later relied on for debt, voting, access and CAM’s entry.',
    boundary: 'Source boundary: the Registry scan controls; purchaser identity, deeds, property schedules, CEXP succession and criminal intent remain open.',
    action: 'Open the complete accounts and transition analysis →'
  } : {
    eyebrow: 'NUEVA FUENTE PRIMARIA · 2008 → 2011',
    title: 'Las cuentas Montelanza 2008 identifican el puente de sucesión de gobierno que debe producirse.',
    body: 'Las cuentas muestran una empresa turística real, una venta de 1,368 M€ el 17 de junio presentada como puesta de activos a disposición del adquirente para explotación, ventas paralelas de apartamentos y una opción sobre 11 locales no vendidos. No prueban una captura criminal. Fijan la estructura “antes” y precisan cómo título, autoridad CEXP, explotación, libros, gastos y representación de propietarios llegaron a la arquitectura comunitaria de 2011 después utilizada para deuda, voto, acceso y entrada de CAM.',
    boundary: 'Límite: controla el escaneo registral; siguen abiertos comprador, escrituras, fincas, sucesión CEXP y dolo criminal.',
    action: 'Abrir cuentas completas y análisis de transición →'
  };

  if (!document.getElementById('montelanza-governance-origin-style')) {
    const style = document.createElement('style');
    style.id = 'montelanza-governance-origin-style';
    style.textContent = '.ml-origin{max-width:1120px;margin:0 auto;border-left:6px solid #8c6b2f;background:#fff8e8;border-radius:0 16px 16px 0;padding:1.1rem 1.25rem}.ml-origin h2{margin:.25rem 0 .55rem}.ml-origin-eyebrow{margin:0;font-size:.72rem;font-weight:900;letter-spacing:.07em;text-transform:uppercase;color:#77591d}.ml-origin-boundary{border-top:1px solid rgba(19,37,45,.18);padding-top:.7rem;font-size:.9rem;color:#4f5c61}.ml-origin a{font-weight:850}';
    document.head.appendChild(style);
  }
  const section = document.createElement('section');
  section.className = 'section';
  section.dataset.montelanzaGovernanceOrigin = '20260821';
  section.innerHTML = `<div class="shell"><aside class="ml-origin"><p class="ml-origin-eyebrow">${copy.eyebrow}</p><h2>${copy.title}</h2><p>${copy.body}</p><p class="ml-origin-boundary"><strong>${copy.boundary}</strong></p><p><a href="${href}">${copy.action}</a></p></aside></div>`;
  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector(':scope > .hero, :scope > .hero-q, :scope > section.hero, :scope > section.hero-q');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else main.insertAdjacentElement('afterbegin', section);
})();

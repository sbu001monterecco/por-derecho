(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/+$/, '/') || '/';
  const relevant = [
    '/en/insolvency-36-2012-court-record/',
    '/en/sun-park-takeover-7-june-2018/',
    '/en/insolvency-36-2012-insolvency-administrator/',
    '/en/insolvency-36-2012-mercantile-court-1/',
    '/en/cuatrecasas-sun-park/',
    '/en/daniel-irigoyen-insolvency-knowledge/',
    '/en/ona-funded-exit-continuity-criminal-analysis/',
    '/en/insolvency-36-2012-continuity-governance-7-june/',
    '/en/insolvency-36-2012-piece-7-garrigues/',
    '/en/insolvency-36-2012-piece-8-monterecco-contract/',
    '/en/insolvency-36-2012-community-authority/',
    '/en/de-facto-administration-community-ac/',
    '/en/community-instrumentalisation/',
    '/en/unitary-criminal-evidence-map/',
    '/en/sun-park-criminal-engineering-investigation/',
    '/es/concurso-36-2012-registro-procesal/',
    '/es/toma-control-sun-park-7-junio-2018/',
    '/es/concurso-36-2012-administrador-concursal/',
    '/es/concurso-36-2012-juzgado-mercantil-1/',
    '/es/concurso-36-2012-magistrado-juez/',
    '/es/cuatrecasas-sun-park/',
    '/es/daniel-irigoyen-conocimiento-concursal/',
    '/es/fuente-profesional-2018-conocimiento-concursal/',
    '/es/ona-salida-financiada-continuidad-penal/',
    '/es/concurso-36-2012-continuidad-gobernanza-7-junio/',
    '/es/concurso-36-2012-pieza-7-garrigues/',
    '/es/concurso-36-2012-pieza-8-contrato-monterecco/',
    '/es/concurso-36-2012-autoridad-comunidad/',
    '/es/administracion-de-hecho-comunidad-ac/',
    '/es/comunidad-instrumentalizacion/',
    '/es/mapa-probatorio-penal-unitario/',
    '/es/ingenieria-forense-criminal-sun-park/'
  ];

  const matched = relevant.some(route => path.endsWith(route));
  if (!matched || document.querySelector('[data-concurso36-arrecife-return]')) return;

  const spanish = path.includes('/es/');
  const href = spanish
    ? '/por-derecho/es/concurso-36-2012-puente-arrecife-mercantil/'
    : '/por-derecho/en/insolvency-36-2012-arrecife-mercantile-bridge/';

  const section = document.createElement('section');
  section.className = 'section';
  section.setAttribute('data-concurso36-arrecife-return', '20260829');
  section.innerHTML = `
    <div class="shell" style="max-width:1120px">
      <div style="border:2px solid #b7832f;border-left-width:9px;background:#fff8e9;border-radius:14px;padding:1rem 1.15rem">
        <p style="margin:.05rem 0 .35rem;font-weight:900;letter-spacing:.06em;text-transform:uppercase;font-size:.78rem;color:#6d4b16">${spanish ? 'PUENTE PROBATORIO BIDIRECCIONAL · CONCURSO 36/2012' : 'BIDIRECTIONAL EVIDENCE BRIDGE · INSOLVENCY 36/2012'}</p>
        <p style="margin:.2rem 0 .65rem">${spanish
          ? 'Este carril está conectado al puente Arrecife ↔ Concurso: exhorto de 2 mayo, respuesta recibida 11 junio, evento separado de 7 junio, conocimiento AC, DP 1132/2018, salida financiada y gap LexNET. La conexión no transfiere conocimiento, intención o responsabilidad entre actores.'
          : 'This track is connected to the Arrecife ↔ Insolvency bridge: 2-May exhorto, response received 11 June, separate 7-June event, IA knowledge, DP 1132/2018, funded exit and LexNET gap. The connection does not transfer knowledge, intent or liability between actors.'}</p>
        <a href="${href}" style="font-weight:900">${spanish ? 'Abrir Arrecife ↔ Concurso 36/2012 →' : 'Open Arrecife ↔ Insolvency 36/2012 →'}</a>
      </div>
    </div>`;

  const footer = document.querySelector('footer');
  if (footer && footer.parentNode) footer.parentNode.insertBefore(section, footer);
  else (document.querySelector('main') || document.body).appendChild(section);
})();

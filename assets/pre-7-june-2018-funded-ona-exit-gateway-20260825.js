(() => {
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalise(location.pathname);
  const routes = new Set([
    '/en/ona-hotels-insolvency-exit-36-2012/',
    '/es/ona-hotels-salida-concurso-36-2012/',
    '/en/sun-park-takeover-7-june-2018/',
    '/es/toma-control-sun-park-7-junio-2018/',
    '/en/same-hotel-multiple-financial-lives/',
    '/es/mismo-hotel-multiples-vidas-financieras/',
    '/en/daniel-irigoyen-insolvency-knowledge/',
    '/es/daniel-irigoyen-conocimiento-concursal/'
  ]);
  if (![...routes].some(route => path.endsWith(route))) return;
  if (document.querySelector('[data-pre7-funded-ona-gateway]')) return;

  const isEnglish = document.documentElement.lang === 'en';
  const prefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const target = isEnglish
    ? `${prefix}en/pre-7-june-2018-funded-ona-exit/`
    : `${prefix}es/salida-financiada-ona-antes-7-junio-2018/`;

  const section = document.createElement('section');
  section.className = 'section';
  section.dataset.pre7FundedOnaGateway = '20260825';
  section.innerHTML = `<div class="shell"><a class="dossier-link side-dossier-gateway" href="${target}"><span>${isEnglish ? 'Dedicated controlled-cutoff dossier · close of 6 June 2018' : 'Dossier específico con corte controlado · cierre del 6 de junio de 2018'}</span><strong>${isEnglish ? 'The funded ONA exit was already in execution: signed operator package, EUR 26m acquisition route, concurrent bridge tracks, staged security, due diligence and specialist court-exit work' : 'La salida financiada con ONA ya estaba en ejecución: paquete de operador firmado, ruta de adquisición por 26 M EUR, vías puente concurrentes, garantías escalonadas, due diligence y trabajo especializado de salida concursal'}</strong><i aria-hidden="true">→</i></a></div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector(':scope > section:first-of-type');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else main.prepend(section);
})();

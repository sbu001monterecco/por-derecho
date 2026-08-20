(() => {
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalise(location.pathname);
  const routes = new Set([
    '/es/toma-control-sun-park-7-junio-2018/',
    '/en/sun-park-takeover-7-june-2018/',
    '/es/contactos-previos-responsable-in-situ-sun-park/',
    '/en/pre-7-june-2018-approaches-sun-park-onsite-manager/',
    '/es/comunidad-instrumentalizacion/',
    '/en/community-instrumentalisation/',
    '/es/acosta-matos-perimetro/',
    '/en/acosta-matos-perimeter/'
  ]);
  if (![...routes].some(route => path.endsWith(route))) return;
  if (document.querySelector('[data-ac-security-request-gateway]')) return;
  const isEnglish = document.documentElement.lang === 'en';
  const basePrefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const target = isEnglish
    ? `${basePrefix}en/insolvency-administrator-security-request-sun-park-27-february-2018/`
    : `${basePrefix}es/solicitud-seguridad-administracion-concursal-sun-park-27-febrero-2018/`;
  const section = document.createElement('section');
  section.className = 'section';
  section.dataset.acSecurityRequestGateway = '20260821';
  section.innerHTML = `<div class="shell"><a class="dossier-link side-dossier-gateway" href="${target}"><span>${isEnglish ? 'Primary document · 27 February 2018 · public redacted searchable PDF' : 'Documento primario · 27 febrero 2018 · PDF público redactado y buscable'}</span><strong>${isEnglish ? 'The insolvency administrator’s request to route security through a Community meeting—and the limits of what that request proves' : 'La solicitud de la administración concursal para canalizar la seguridad mediante una junta y los límites de lo que prueba'}</strong><i aria-hidden="true">→</i></a></div>`;
  const main = document.querySelector('main');
  if (!main) return;
  const candidates = isEnglish
    ? ['#events-of-7-june','#chronology','#scope','#community']
    : ['#hechos-7-junio','#cronologia','#alcance','#comunidad'];
  const anchor = candidates.map(selector => document.querySelector(selector)).find(Boolean);
  if (anchor) anchor.insertAdjacentElement('beforebegin', section);
  else main.append(section);
})();

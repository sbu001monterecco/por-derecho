(() => {
  const path = location.pathname.replace(/\/index\.html$/,'/').toLowerCase();
  if (document.querySelector('[data-joan-cruz-multitrack-20260901]')) return;
  const isEn = document.documentElement.lang === 'en';
  const base = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const routes = [
    '/es/toma-control-sun-park-7-junio-2018/','/en/sun-park-takeover-7-june-2018/',
    '/es/mismo-hotel-multiples-vidas-financieras/','/en/same-hotel-multiple-financial-lives/',
    '/es/lava-verde-club-sei-meeting-point/','/en/lava-verde-club-sei-meeting-point/',
    '/es/acosta-matos-perimetro/','/en/acosta-matos-perimeter/',
    '/es/actores-partes-abogados-representantes/','/en/actors-parties-lawyers-representatives/',
    '/es/calificacion-concurso-36-2012-vidas-paralelas/','/en/insolvency-classification-36-2012-parallel-lives/'
  ];
  if (!routes.some(r => path.endsWith(r))) return;
  const main = document.querySelector('main'); if (!main) return;
  const s = document.createElement('section'); s.className='section alt'; s.dataset.joanCruzMultitrack20260901='true';
  const person = isEn ? `${base}en/joan-cruz-nuez/` : `${base}es/joan-cruz-nuez/`;
  const event = isEn ? `${base}en/sun-park-1-march-2018-joan-cruz/` : `${base}es/sun-park-1-marzo-2018-joan-cruz/`;
  const takeover = isEn ? `${base}en/sun-park-takeover-7-june-2018/` : `${base}es/toma-control-sun-park-7-junio-2018/`;
  const lives = isEn ? `${base}en/same-hotel-multiple-financial-lives/` : `${base}es/mismo-hotel-multiples-vidas-financieras/`;
  s.innerHTML = isEn ? `<div class="shell"><p class="kicker">PRE-7 JUNE PRECURSOR · ACTOR/EVENT/ASSET CROSS-LINK</p><h2>Joan Cruz Nuez^ / 1 March 2018 now sits inside the same-hotel multitrack chronology.</h2><p>The 1 March photographic package is <strong>98 days before</strong> the 7 June physical-control event. Preserved witness material also recalls pre-7 June visits involving Acosta and Joan/representatives, while a 22 March transcript records access, exploitation, Community, security and target-control language with the speakers' identities unresolved in its body. This supports testing a planned/preparatory trajectory; it does <strong>not</strong> establish direct Joan↔AC or Joan↔judge coordination.</p><p><a href="${person}"><strong>Joan dossier →</strong></a> · <a href="${event}">1 March evidence →</a> · <a href="${takeover}">7 June →</a> · <a href="${lives}">parallel lives of the same asset →</a></p></div>` : `<div class="shell"><p class="kicker">PRECURSOR PRE-7 JUNIO · INTERLINK ACTOR/EVENTO/ACTIVO</p><h2>Joan Cruz Nuez^ / 1 marzo 2018 entra en la cronología multitrack del mismo hotel.</h2><p>El paquete del 1 de marzo precede en <strong>98 días</strong> al control físico del 7 de junio. Material testifical preservado recuerda además visitas pre-7 junio con Acosta y Joan/representantes, mientras una transcripción de 22 marzo registra lenguaje de acceso, explotación, Comunidad, seguridad y fecha objetivo con la identidad de las voces no resuelta en su cuerpo. Esto sustenta contrastar una trayectoria planificada/preparatoria; <strong>no</strong> establece coordinación directa Joan↔AC o Joan↔juez.</p><p><a href="${person}"><strong>Dossier Joan →</strong></a> · <a href="${event}">evidencia 1 marzo →</a> · <a href="${takeover}">7 junio →</a> · <a href="${lives}">vidas paralelas del mismo activo →</a></p></div>`;
  const hero = main.querySelector('section');
  if (hero) hero.insertAdjacentElement('afterend',s); else main.prepend(s);
})();
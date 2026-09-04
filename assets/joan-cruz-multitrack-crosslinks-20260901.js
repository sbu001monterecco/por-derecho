(() => {
  const path = location.pathname.replace(/\/index\.html$/,'/').toLowerCase();
  if (document.querySelector('[data-joan-cruz-multitrack-20260901]')) return;
  const isEn = document.documentElement.lang === 'en';
  const base = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const routes = [
    '/es/sun-park-1-marzo-2018-joan-cruz/','/en/sun-park-1-march-2018-joan-cruz/',
    '/es/investigacion-privada-2018-meeting-point/','/en/private-investigation-2018-meeting-point/',
    '/es/toma-control-sun-park-7-junio-2018/','/en/sun-park-takeover-7-june-2018/',
    '/es/mismo-hotel-multiples-vidas-financieras/','/en/same-hotel-multiple-financial-lives/',
    '/es/lava-verde-club-sei-meeting-point/','/en/lava-verde-club-sei-meeting-point/',
    '/es/fti-touristik-meeting-point-insolvencia-preconcurso-bluesea/','/en/fti-touristik-meeting-point-insolvency-preinsolvency-bluesea/',
    '/es/acosta-matos-perimetro/','/en/acosta-matos-perimeter/',
    '/es/actores-partes-abogados-representantes/','/en/actors-parties-lawyers-representatives/',
    '/es/calificacion-concurso-36-2012-vidas-paralelas/','/en/insolvency-classification-36-2012-parallel-lives/'
  ];
  if (!routes.some(r => path.endsWith(r))) return;
  const main = document.querySelector('main'); if (!main) return;
  const s = document.createElement('section'); s.className='section alt'; s.dataset.joanCruzMultitrack20260901='true';
  const person = isEn ? `${base}en/joan-cruz-nuez/` : `${base}es/joan-cruz-nuez/`;
  const event = isEn ? `${base}en/sun-park-1-march-2018-joan-cruz/` : `${base}es/sun-park-1-marzo-2018-joan-cruz/`;
  const privateInvestigation = isEn ? `${base}en/private-investigation-2018-meeting-point/` : `${base}es/investigacion-privada-2018-meeting-point/`;
  const takeover = isEn ? `${base}en/sun-park-takeover-7-june-2018/` : `${base}es/toma-control-sun-park-7-junio-2018/`;
  const lava = isEn ? `${base}en/lava-verde-club-sei-meeting-point/` : `${base}es/lava-verde-club-sei-meeting-point/`;
  const fti = isEn ? `${base}en/fti-touristik-meeting-point-insolvency-preinsolvency-bluesea/` : `${base}es/fti-touristik-meeting-point-insolvencia-preconcurso-bluesea/`;
  s.innerHTML = isEn
    ? `<div class="shell"><p class="kicker">JOAN CRUZ^ · MEETING POINT / ACOSTA MATOS CONTINUITY</p><h2>The 1 March 2018 Sun Park node belongs in a longer owner–operator–developer chronology.</h2><p>Primary corporate records place Joan Cruz in Meeting Point Hotelmanagement (Canaries) and Meeting Point Investment before 2018; contemporaneous reporting places him as LABRANDA Hotels &amp; Resorts director general at Hotel LABRANDA Marieta in 2016, while Acosta Matos identifies Grupo Patrimonial Acosta Matos as owner of that hotel project. The separate 1 March Sun Park evidence, later Lava Verde / Club Sei sequence, HKI Sun Park capture and BLUESEA/Meeting Point continuity therefore support testing prior commercial familiarity and project preparation. They do <strong>not</strong> establish Joan Cruz's identity from the photographs, the purpose or authority of the 1 March visit, an advance Sun Park/Club Sei contract, criminal coordination, fraud or conspiracy.</p><p><a href="${person}"><strong>Joan Cruz continuity dossier →</strong></a> · <a href="${event}">1 March evidence →</a> · <a href="${privateInvestigation}">8 May 2018 investigation →</a> · <a href="${takeover}">7 June →</a> · <a href="${lava}">Lava Verde / Club Sei →</a> · <a href="${fti}">FTI → BLUESEA →</a></p></div>`
    : `<div class="shell"><p class="kicker">JOAN CRUZ^ · CONTINUIDAD MEETING POINT / ACOSTA MATOS</p><h2>El nodo Sun Park de 1 marzo 2018 debe leerse dentro de una cronología más larga propietario–operador–desarrollador.</h2><p>Registros mercantiles primarios sitúan a Joan Cruz en Meeting Point Hotelmanagement (Canaries) y Meeting Point Investment antes de 2018; información contemporánea lo identifica como director general de LABRANDA Hotels &amp; Resorts en Hotel LABRANDA Marieta en 2016, mientras Acosta Matos identifica a Grupo Patrimonial Acosta Matos como propietario de ese proyecto hotelero. La evidencia separada de 1 marzo en Sun Park, la secuencia posterior Lava Verde / Club Sei, la captura HKI de Sun Park y la continuidad BLUESEA/Meeting Point justifican por tanto contrastar familiaridad comercial previa y preparación de proyecto. <strong>No</strong> acreditan la identidad de Joan Cruz a partir de las fotografías, la finalidad o autoridad de la visita de 1 marzo, un contrato previo Sun Park/Club Sei, coordinación criminal, fraude ni conspiración.</p><p><a href="${person}"><strong>Dossier de continuidad Joan Cruz →</strong></a> · <a href="${event}">evidencia 1 marzo →</a> · <a href="${privateInvestigation}">investigación 8 mayo 2018 →</a> · <a href="${takeover}">7 junio →</a> · <a href="${lava}">Lava Verde / Club Sei →</a> · <a href="${fti}">FTI → BLUESEA →</a></p></div>`;
  const hero = main.querySelector('section');
  if (hero) hero.insertAdjacentElement('afterend',s); else main.prepend(s);
})();
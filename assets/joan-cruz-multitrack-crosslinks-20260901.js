(() => {
  const path = location.pathname.replace(/\/index\.html$/,'/').toLowerCase();
  if (document.querySelector('[data-joan-cruz-multitrack-20260901]')) return;
  const isEn = document.documentElement.lang === 'en';
  const base = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const routes = [
    '/es/joan-cruz-nuez/','/en/joan-cruz-nuez/',
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
    ? `<div class="shell"><p class="kicker">JOAN CRUZ^ · PRIMARY 2018 WITNESS CORROBORATION · CONTINUITY</p><h2>The Sun Park node is now supported by a contemporaneous sworn-witness chronology as well as the longer Meeting Point / Acosta Matos relationship.</h2><p>A 25 June 2018 court-recorded witness statement in DP 1132/2018 describes repeated February/March visits to Sun Park by a person the witness called <strong>“JOAN”</strong> with a person called DANIEL: measurements with a plan, showing the hotel to three other men and later checking installations for refurbishment. The witness also linked specified court-file photograph ranges to visits, measurements and refurbishment checking. Separate 7–8 May 2018 material had already identified and investigated <strong>Joan Cruz Nuez</strong> and his HKI/Meeting Point history before the 7 June control event.</p><p><strong>Boundary:</strong> the sworn act itself says “JOAN”, gives no surname and says the witness did not know his role. The combined sources therefore support a <em>corroborated identity/continuity route</em>, not facial recognition, an automatic surname finding, proof of access authority/illegality, an advance operator contract, fraud or conspiracy.</p><p><a href="${person}"><strong>Joan Cruz continuity dossier →</strong></a> · <a href="${event}">1 March + sworn witness evidence →</a> · <a href="${privateInvestigation}">8 May investigation →</a> · <a href="${takeover}">7 June →</a> · <a href="${lava}">Lava Verde / Club Sei →</a> · <a href="${fti}">FTI → BLUESEA →</a></p></div>`
    : `<div class="shell"><p class="kicker">JOAN CRUZ^ · CORROBORACIÓN TESTIFICAL PRIMARIA 2018 · CONTINUIDAD</p><h2>El nodo Sun Park cuenta ahora con una cronología testifical judicial contemporánea además de la relación más larga Meeting Point / Acosta Matos.</h2><p>Una declaración testifical judicial de 25 junio 2018 en DP 1132/2018 describe visitas repetidas a Sun Park en febrero/marzo por una persona a la que el testigo llama <strong>“JOAN”</strong> junto a una persona llamada DANIEL: mediciones con un plano, mostrar el hotel a otros tres hombres y comprobar después instalaciones para una reforma. El testigo relaciona además rangos concretos de fotografías del expediente con visitas, mediciones y comprobación para reforma. Material separado de 7–8 mayo 2018 ya había identificado e investigado a <strong>Joan Cruz Nuez</strong> y su trayectoria HKI/Meeting Point antes del evento de control de 7 junio.</p><p><strong>Límite:</strong> el acta testifical dice “JOAN”, no aporta apellido y afirma que el testigo desconocía su cargo. El conjunto sostiene por tanto una <em>ruta corroborada de identidad/continuidad</em>, no reconocimiento facial, una identificación automática por apellido, prueba de autorización/ilicitud del acceso, contrato previo de operador, fraude ni conspiración.</p><p><a href="${person}"><strong>Dossier de continuidad Joan Cruz →</strong></a> · <a href="${event}">1 marzo + evidencia testifical →</a> · <a href="${privateInvestigation}">investigación 8 mayo →</a> · <a href="${takeover}">7 junio →</a> · <a href="${lava}">Lava Verde / Club Sei →</a> · <a href="${fti}">FTI → BLUESEA →</a></p></div>`;
  const hero = main.querySelector('section');
  if (hero) hero.insertAdjacentElement('afterend',s); else main.prepend(s);
})();
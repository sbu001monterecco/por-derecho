(() => {
  const path = location.pathname;
  const es = /\/es\//.test(path);
  const marker = 'dp1901-routing-collision-20260919';
  if (document.querySelector('[data-dp1901-routing-collision]')) return;
  const target = document.querySelector('main') || document.body;
  if (!target) return;
  const base = (() => {
    const m = path.match(/^(.*?)(?:\/en\/|\/es\/)/);
    return m ? m[1] : '';
  })();
  const href = (p) => base + p;
  const copy = es ? {
    kicker:'TRAZABILIDAD COMÚN · DP 1901/2026',
    title:'Dos escritos autónomos. Un expediente con dos identidades documentadas. Falta el puente.',
    intro:'La separación de Ref. 21 y Ref. 24 está documentada. También lo están la presentación de material privado bajo DP 1901 el 9 de julio, la vinculación oficial con DIP 2 el 12 de julio, el informe Fiscal de 29 de julio y el Auto de 14 de septiembre. Lo que no está producido es el acto o evento que explique la relación entre ambos carriles y DP 1901.',
    boundary:'Este módulo no atribuye autoría, intención, manipulación ni irregularidad penal. La dirección de la colisión sigue sin certificarse. La afirmación de que Ref. 24 seguía intacta, sin escanear y sin asignar el 25 de junio es la declaración presencial expresa del compareciente; no sustituye la certificación electrónica pendiente.',
    links:[
      ['Ref. 21 · denuncia autónoma de actores privados','/es/control-21-denuncia-actores-privados-25-junio-2026/'],
      ['DP 1901 · expediente central','/es/dp-1901-2026/'],
      ['Auto 14 septiembre','/es/dp-1901-2026-auto-14-septiembre-2026/'],
      ['Respuesta CGPJ propuesta · 19 sep','/es/dp-1901-2026-auto-14-septiembre-2026/#response-full'],
      ['E.G. 745/2026','/es/fiscalia-inspeccion-exp-gub-745-2026/'],
      ['Ref. 24 · notitia dirigida al TSJC','/es/control-24-denuncia-juez-concurso-36-2012/'],
      ['DIP 2/2026','/es/fiscalia-dip-2-2026/'],
      ['CGPJ · Comisión Permanente','/es/cgpj-comision-permanente-sala-lectura/'],
      ['TSJC · Exp. Gub. 38/2026','/es/tsj-canarias-exp-gub-38-2026/'],
      ['Actores privados','/es/actores-privados-per-comunero-administracion-de-hecho/']
    ],
    asks:['¿Qué escrito creó DP 1901 y cuándo se asoció cada documento?','¿Qué diferencia documentada hubo con Ref. 22 / DP 1956, y qué ocurrió con la ruta TSJC de Ref. 24?','¿Qué objeto constaba en el sistema el 9, 12 y 29 de julio y el 14 de septiembre?','¿Qué corpus exacto recibió Fiscalía?','¿Dónde quedó la denuncia autónoma de Ref. 21?','¿Qué ocurrió con Ref. 24 y por qué terminó asociada al mismo DP?']
  } : {
    kicker:'COMMON TRACEABILITY · DP 1901/2026',
    title:'Two autonomous filings. One case with two documented identities. The bridge is still missing.',
    intro:'The separation of Ref. 21 and Ref. 24 is documented. So are the 9 July physical tender of private-actor material under DP 1901, the official 12 July DIP 2 linkage, the 29 July prosecution report and the 14 September order. What is not produced is the act or system event explaining the relationship between the two lanes and DP 1901.',
    boundary:'This module does not attribute authorship, intent, manipulation or criminal wrongdoing. The direction of the collision remains uncertified. The statement that Ref. 24 remained untouched, unscanned and unallocated on 25 June is the complainant’s express firsthand account; it does not replace the outstanding electronic-history certification.',
    links:[
      ['Ref. 21 · autonomous private-actor complaint','/en/control-21-private-actors-complaint-25-june-2026/'],
      ['DP 1901 · central file','/en/dp-1901-2026/'],
      ['14 September order','/en/dp-1901-2026-order-14-september-2026/'],
      ['Proposed CGPJ response · 19 Sep','/en/dp-1901-2026-order-14-september-2026/#response-full'],
      ['E.G. 745/2026','/en/public-prosecution-inspection-exp-gub-745-2026/'],
      ['Ref. 24 · TSJC-directed notitia','/en/control-24-insolvency-judge-complaint-36-2012/'],
      ['DIP 2/2026','/en/fiscalia-dip-2-2026/'],
      ['CGPJ · Permanent Commission','/en/cgpj-permanent-commission-reader-room/'],
      ['TSJC · Exp. Gub. 38/2026','/en/tsj-canarias-exp-gub-38-2026/'],
      ['Private-actor layer','/en/private-actors-per-community-member-de-facto-administration/']
    ],
    asks:['Which filing created DP 1901 and when was each document associated?','What recorded difference explains Ref. 22 / DP 1956 handling and what happened to Ref. 24’s TSJC route?','What object did the system record on 9, 12 and 29 July and 14 September?','What exact corpus did the Public Prosecution Service receive?','Where did the autonomous Ref. 21 complaint go?','What happened to Ref. 24 and why did it become associated with the same DP?']
  };
  const section = document.createElement('section');
  section.dataset.dp1901RoutingCollision = marker;
  section.className = 'dp1901-collision-shell';
  section.innerHTML = `
    <style>
      .dp1901-collision-shell{max-width:1180px;margin:2rem auto;padding:0 1rem;font-family:inherit}
      .dp1901-collision-card{background:#fbfaf6;border:1px solid #d9dfdf;border-radius:18px;padding:1.25rem;box-shadow:0 14px 38px rgba(25,38,45,.07)}
      .dp1901-collision-kicker{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;font-weight:800;color:#6d5626}
      .dp1901-collision-card h2{margin:.35rem 0 .7rem;font-size:clamp(1.55rem,2.7vw,2.35rem);line-height:1.12}
      .dp1901-collision-grid{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(280px,.75fr);gap:1.15rem;align-items:start}
      .dp1901-collision-grid img{width:100%;height:auto;border-radius:14px;border:1px solid #cfd8d8;background:white}
      .dp1901-collision-links{display:grid;gap:.55rem}
      .dp1901-collision-links a{display:block;padding:.72rem .82rem;border:1px solid #cbd6d7;border-radius:11px;text-decoration:none;background:white;font-weight:700}
      .dp1901-collision-asks{margin:.8rem 0 0;padding-left:1.25rem}
      .dp1901-collision-asks li{margin:.42rem 0}
      .dp1901-collision-boundary{margin-top:1rem;padding:.8rem 1rem;border-left:4px solid #9d2d2d;background:#fff4f2}
      @media(max-width:760px){.dp1901-collision-grid{grid-template-columns:1fr}}
    </style>
    <div class="dp1901-collision-card">
      <div class="dp1901-collision-kicker">${copy.kicker}</div>
      <h2>${copy.title}</h2>
      <p>${copy.intro}</p>
      <div class="dp1901-collision-grid">
        <div><img src="${href('/assets/visuals/dp1901-routing-collision-20260919.svg')}" alt="${copy.title}"></div>
        <div>
          <div class="dp1901-collision-links">${copy.links.map(([label,url])=>`<a href="${href(url)}">${label} →</a>`).join('')}</div>
          <ol class="dp1901-collision-asks">${copy.asks.map(x=>`<li>${x}</li>`).join('')}</ol>
        </div>
      </div>
      <div class="dp1901-collision-boundary"><strong>${es?'Límite probatorio':'Evidence boundary'}:</strong> ${copy.boundary}</div>
    </div>`;
  const hero = target.querySelector('section');
  if (hero && hero.parentNode === target) hero.insertAdjacentElement('afterend', section);
  else target.insertBefore(section, target.firstChild);
})();


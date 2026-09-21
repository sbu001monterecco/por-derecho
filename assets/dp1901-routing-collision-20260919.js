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
    title:'Ref. 21 was the private-actor filing contemporaneously mapped to DP 1901. The later Ref. 24 association bridge is still missing.',
    intro:'The 25 June Ref. 21 private-actor filing is documented by its stamped cover and a same-day 11:23 email to Procuradora María Díaz Vecino. The 9 July correspondence expressly maps 1901 to CAM/private Community actors and 1956 to the insolvency administrator, while private-actor material was physically tendered under DP 1901. The official 12 July DIP 2 linkage, 29 July prosecution report and 14 September order then show a later identity collision. What is not produced is the court-system event trail and the act explaining the later Ref. 24 association.',
    boundary:'This module does not attribute authorship, intent, manipulation or criminal wrongdoing. Gil’s Ref. 21 → DP 1901 account is contemporaneously corroborated by the 25 June procuradora email and 9 July operational mapping. The official electronic creation/reparto event and the later Ref. 24 association mechanism remain to be certified. The statement that Ref. 24 remained untouched, unscanned and unallocated on 25 June is the complainant’s express firsthand account.',
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


/* dp1901-shame-editorial-20260921: additive dossier-only teaser */
(()=>{
 const match=location.pathname.match(/^(.*)\/(en|es)\/dp-1901-2026\/(?:index\.html)?$/);
 if(!match||document.getElementById("shame-editorial-20260921"))return;
 const target=document.querySelector("main");if(!target)return;
 const htmlByLanguage={"en": "\n<!-- dp1901-shame-editorial-20260921:start -->\n<section id=\"shame-editorial-20260921\" style=\"padding:1.6rem 1rem;background:#f6f2e9;color:#202224;border-block:1px solid #c7bdb0\"><div style=\"max-width:1120px;margin:auto;display:flex;gap:24px;align-items:center;flex-wrap:wrap\"><a href=\"shame-has-left-the-building/\" style=\"flex:0 0 150px\"><img src=\"../../assets/visuals/dp1901-shame-20260921/shame-has-left-the-building.avif\" width=\"150\" height=\"212\" loading=\"lazy\" alt=\"Editorial satire: a generic judge and prosecutor expel the ghostly figure of Shame; their shadows metaphorically bury Lady Justice, distinct Ref. 21 and Ref. 24 folders, and tablets for effective judicial protection, legality, impartiality and the rule of law.\" style=\"width:150px;height:auto\"></a><div style=\"flex:1 1 280px\"><p style=\"font-weight:bold;color:#96231d;letter-spacing:.08em;margin:0\">SATIRE / SÁTIRA · EDITORIAL METAPHOR</p><h2 style=\"margin:.5rem 0;font-size:1.8rem\">Shame has left the building.</h2><p>It didn’t leave. It was thrown out. Image, author’s post, documentary context and source boundaries.</p><p><a href=\"shame-has-left-the-building/\"><strong>Open the English landing page →</strong></a> · <a href=\"../../es/dp-1901-2026/la-verguenza-no-se-fue/\">Español</a></p><small>Generic figures; AI-generated editorial image, not a factual depiction. Manual LinkedIn publication only.</small></div></div></section>\n<!-- dp1901-shame-editorial-20260921:end -->\n", "es": "\n<!-- dp1901-shame-editorial-20260921:start -->\n<section id=\"shame-editorial-20260921\" style=\"padding:1.6rem 1rem;background:#f6f2e9;color:#202224;border-block:1px solid #c7bdb0\"><div style=\"max-width:1120px;margin:auto;display:flex;gap:24px;align-items:center;flex-wrap:wrap\"><a href=\"la-verguenza-no-se-fue/\" style=\"flex:0 0 150px\"><img src=\"../../assets/visuals/dp1901-shame-20260921/la-verguenza-no-se-fue.avif\" width=\"150\" height=\"212\" loading=\"lazy\" alt=\"Sátira editorial: un juez y una fiscal genéricos expulsan al espectro de la Vergüenza; sus sombras entierran metafóricamente a la Justicia, las carpetas separadas Ref. 21 y Ref. 24 y las garantías de tutela judicial efectiva, legalidad, imparcialidad y Estado de Derecho.\" style=\"width:150px;height:auto\"></a><div style=\"flex:1 1 280px\"><p style=\"font-weight:bold;color:#96231d;letter-spacing:.08em;margin:0\">SÁTIRA · METÁFORA EDITORIAL</p><h2 style=\"margin:.5rem 0;font-size:1.8rem\">La vergüenza no se fue.</h2><p>La echaron a patadas. Imagen, publicación del autor, contexto documental y límites de las fuentes.</p><p><a href=\"la-verguenza-no-se-fue/\"><strong>Abrir la página de la edición española →</strong></a> · <a href=\"../../en/dp-1901-2026/shame-has-left-the-building/\">English</a></p><small>Figuras genéricas; imagen editorial generada con IA, no representación de hechos físicos. Publicación manual en LinkedIn.</small></div></div></section>\n<!-- dp1901-shame-editorial-20260921:end -->\n"};
 target.insertAdjacentHTML("afterbegin",htmlByLanguage[match[2]]);
})();

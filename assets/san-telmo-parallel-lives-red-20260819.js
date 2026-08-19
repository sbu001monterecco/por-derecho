(()=>{
  const d=document;
  const path=location.pathname.replace(/\/+$/,'/');
  const es=/\/es\//.test(path);
  const isHome=/\/(en|es)\/$/.test(path);
  const isRicpe=/\/(en|es)\/ric-private-equity-sun-park\/$/.test(path);
  const isRsm=/\/(en|es)\/rsm\/nnr4-1025c2f66\/$/.test(path);
  const isAc=/\/en\/insolvency-36-2012-insolvency-administrator\/$/.test(path)||/\/es\/concurso-36-2012-administrador-concursal\/$/.test(path);
  if(!isHome&&!isRicpe&&!isRsm&&!isAc)return;
  const base=es?'/por-derecho/es/':'/por-derecho/en/';

  const c=es?{
    kicker:'HALLAZGO DOCUMENTAL DOMINANTE · SAN TELMO ↔ RIC PRIVATE EQUITY · 30 NOV 2021',
    title:'MISMO HOTEL. MISMO PERIODO. MISMO PERÍMETRO DE DESPACHO. DOS VIDAS PROFESIONALES EN PARALELO.',
    asset:'SUN PARK / MYND YAIZA · EL MISMO ACTIVO',
    leftK:'VIDA JUDICIAL / CONCURSAL',
    leftN:'Francisco de Borja Rodríguez-Batllori Laffitte',
    leftR:'ADMINISTRADOR CONCURSAL · CONCURSO 36/2012 · SAN TELMO',
    leftT:'El activo seguía dentro de la vida concursal y bajo el perímetro de actuación del Administrador Concursal.',
    rightK:'VIDA INVERSORA / FINANCIERA',
    rightN:'Eduardo Sánchez',
    rightR:'SOCIO · SAN TELMO ABOGADOS · 30 NOV 2021',
    quote:'“NOSOTROS EN EL DESPACHO … METIMOS UNOS CUANTOS CLIENTES”',
    rightT:'en la inversión RICPE conectada con el proyecto hotelero Acosta Matos / Sun Park, en conversación directa con Enrique Guerra, Director General de RIC Private Equity.',
    impact:'MIENTRAS UN SOCIO DE SAN TELMO OCUPABA EL PAPEL DE ADMINISTRADOR CONCURSAL EN EL CONCURSO QUE AFECTABA A SUN PARK, OTRO SOCIO DE SAN TELMO RECONOCIÓ QUE EL DESPACHO HABÍA INTRODUCIDO CLIENTES COMO INVERSORES EN LA INVERSIÓN RICPE CONECTADA CON ESE MISMO HOTEL.',
    proof:'Esto acredita la conexión despacho–clientes/inversores–RICPE con el perímetro de inversión Sun Park. No acredita por sí solo una transmisión Borja→Eduardo de información concursal, coordinación entre ambos ni ilicitud: esas son cuestiones separadas que deben resolverse con los registros del despacho, conflictos/KYC, comunicaciones, facturación, códigos de asunto y accesos.',
    livesTitle:'UN MISMO HOTEL · CUATRO VIDAS PARALELAS QUE DEBEN RECONCILIARSE',
    lives:[
      ['1 · VIDA CONCURSAL','Concurso 36/2012 · Juzgado · Administrador Concursal · liquidación · acreedores'],
      ['2 · VIDA DE CONTROL','Comunidad · acceso · voto · explotación · cinco actores · control de información'],
      ['3 · VIDA DE INVERSIÓN','CAM · RICPE · clientes/inversores introducidos por San Telmo · due diligence · financiación · reforma'],
      ['4 · VIDA DE PROPIEDAD / OPERACIÓN','CAM → HNT → MYND Yaiza · continuidad patrimonial y operativa']
    ],
    question:'¿QUIÉN SABÍA QUE EL MISMO HOTEL ESTABA VIVIENDO TODAS ESTAS VIDAS EN PARALELO?',
    q2:'¿Quién tenía los documentos? ¿Quién introdujo inversores? ¿Quién controlaba el expediente concursal? ¿Quién representaba la propiedad? ¿Quién aprobaba la inversión? ¿Quién reconcilió —o no reconcilió— los registros paralelos?',
    rsm:'RSM SPAIN · NNR4-1025C2F66 · 2026',
    rsmT:'La revisión de Ethics & Independence tiene ahora una prueba concreta de no-fragmentación: preservar, identificar, reconciliar y explicar qué muestran los registros heredados de San Telmo sobre ambas vidas profesionales.',
    acLink:'Ver Administrador Concursal →',ricpeLink:'Ver RICPE / Sun Park →',rsmLink:'Ver expediente RSM →'
  }:{
    kicker:'DOMINANT DOCUMENTARY FINDING · SAN TELMO ↔ RIC PRIVATE EQUITY · 30 NOV 2021',
    title:'SAME HOTEL. SAME PERIOD. SAME LAW-FIRM PERIMETER. TWO PARALLEL PROFESSIONAL LIVES.',
    asset:'SUN PARK / MYND YAIZA · THE SAME ASSET',
    leftK:'JUDICIAL / INSOLVENCY LIFE',
    leftN:'Francisco de Borja Rodríguez-Batllori Laffitte',
    leftR:'INSOLVENCY ADMINISTRATOR · CONCURSO 36/2012 · SAN TELMO',
    leftT:'The asset remained inside the insolvency life and within the Insolvency Administrator’s professional perimeter.',
    rightK:'INVESTMENT / FINANCING LIFE',
    rightN:'Eduardo Sánchez',
    rightR:'PARTNER · SAN TELMO ABOGADOS · 30 NOV 2021',
    quote:'“NOSOTROS EN EL DESPACHO … METIMOS UNOS CUANTOS CLIENTES”',
    rightT:'into the RICPE investment connected with the Acosta Matos / Sun Park hotel project, in direct discussion with Enrique Guerra, Director General of RIC Private Equity.',
    impact:'WHILE ONE SAN TELMO PARTNER OCCUPIED THE INSOLVENCY-ADMINISTRATOR ROLE IN THE INSOLVENCY AFFECTING SUN PARK, ANOTHER SAN TELMO PARTNER ACKNOWLEDGED THAT THE FIRM HAD PUT CLIENTS IN AS INVESTORS IN THE RICPE INVESTMENT CONNECTED TO THAT SAME HOTEL.',
    proof:'This establishes the law-firm/client-investor/RICPE connection to the Sun Park investment perimeter. It does not, by itself, establish Borja→Eduardo transfer of insolvency information, coordination between them, or unlawfulness: those are separate questions to be resolved from firm records, conflicts/KYC, communications, billing, matter codes and access records.',
    livesTitle:'ONE HOTEL · FOUR PARALLEL LIVES THAT MUST BE RECONCILED',
    lives:[
      ['1 · INSOLVENCY LIFE','Concurso 36/2012 · Court · Insolvency Administrator · liquidation · creditors'],
      ['2 · CONTROL LIFE','Community · access · voting · exploitation · five actors · information control'],
      ['3 · INVESTMENT LIFE','CAM · RICPE · San Telmo-introduced clients/investors · due diligence · financing · renovation'],
      ['4 · OWNERSHIP / OPERATING LIFE','CAM → HNT → MYND Yaiza · ownership and operational continuity']
    ],
    question:'WHO KNEW THAT THE SAME HOTEL WAS LIVING ALL THESE LIVES IN PARALLEL?',
    q2:'Who held the documents? Who introduced investors? Who controlled the insolvency file? Who represented ownership? Who approved the investment? Who reconciled — or failed to reconcile — the parallel records?',
    rsm:'RSM SPAIN · NNR4-1025C2F66 · 2026',
    rsmT:'The Ethics & Independence review now has a concrete non-fragmentation test: preserve, identify, reconcile and explain what the San Telmo legacy records show about both professional lives.',
    acLink:'See Insolvency Administrator →',ricpeLink:'See RICPE / Sun Park →',rsmLink:'See RSM case →'
  };

  const addStyle=()=>{
    if(d.querySelector('style[data-pd-parallel-lives]'))return;
    const s=d.createElement('style');s.dataset.pdParallelLives='20260819a';
    s.textContent=`
      .pd-parallel{margin:1.1rem auto 2rem;width:min(calc(100% - 2rem),1180px);border:4px solid #a40000;border-radius:16px;background:#fff;box-shadow:0 10px 28px rgba(64,0,0,.14);overflow:hidden;color:#17242b}
      .pd-parallel__head{padding:1rem 1.15rem .9rem;background:#fff7f5}.pd-parallel__k{font-size:.76rem;font-weight:1000;letter-spacing:.08em;text-transform:uppercase;color:#b00000}.pd-parallel__title{margin:.32rem 0 0;font-size:clamp(1.55rem,3vw,2.65rem);line-height:1.02;font-weight:1000;color:#9d0000}.pd-parallel__asset{text-align:center;padding:.6rem 1rem;background:#131f27;color:#fff;font-weight:1000;letter-spacing:.06em}
      .pd-parallel__collision{display:grid;grid-template-columns:1fr 90px 1fr;gap:.75rem;padding:1rem}.pd-parallel__node{border:1px solid #d9c5c1;border-radius:13px;padding:1rem;background:#fff}.pd-parallel__node--left{border-top:7px solid #17242b}.pd-parallel__node--right{border-top:7px solid #b00000}.pd-parallel__nodeK{font-size:.72rem;font-weight:1000;letter-spacing:.07em;color:#6b777c;text-transform:uppercase}.pd-parallel__node h3{margin:.3rem 0 .2rem;font-size:1.17rem;line-height:1.15}.pd-parallel__role{font-size:.79rem;font-weight:950;color:#7e1515}.pd-parallel__quote{margin:.75rem 0;padding:.72rem;border-radius:9px;background:#b00000;color:#fff;font-size:clamp(1rem,2vw,1.35rem);font-weight:1000;line-height:1.12}.pd-parallel__same{display:flex;align-items:center;justify-content:center;text-align:center;font-weight:1000;color:#a40000;font-size:.8rem;line-height:1.15}.pd-parallel__same:before,.pd-parallel__same:after{content:'↔';display:block;font-size:1.7rem;margin:.2rem}
      .pd-parallel__impact{padding:.9rem 1.1rem;background:#a40000;color:#fff;font-weight:1000;font-size:clamp(1rem,1.8vw,1.35rem);line-height:1.25;text-align:center}.pd-parallel__proof{margin:0;padding:.85rem 1.1rem;background:#fff2df;border-bottom:1px solid #ead4b1;font-size:.88rem;line-height:1.45}.pd-parallel__lives{padding:1rem 1.1rem}.pd-parallel__lives h3{margin:0 0 .75rem;text-align:center;color:#8f0000}.pd-parallel__lifeGrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.65rem}.pd-parallel__life{padding:.8rem;border:1px solid #d7dfe2;border-radius:10px;background:#f8fafb}.pd-parallel__life strong{display:block;margin-bottom:.3rem;font-size:.82rem;color:#17242b}.pd-parallel__life span{font-size:.78rem;line-height:1.35;color:#4e6068}.pd-parallel__question{padding:.9rem 1.05rem;background:#131f27;color:#fff;text-align:center}.pd-parallel__question strong{display:block;color:#ffb3ad;font-size:clamp(1.05rem,2vw,1.45rem)}.pd-parallel__question span{display:block;margin-top:.35rem;font-size:.86rem;line-height:1.4}.pd-parallel__rsm{padding:.9rem 1.05rem;border-top:4px solid #b00000;background:#f4f6f7}.pd-parallel__rsm strong{display:block;color:#a40000;font-size:1rem}.pd-parallel__links{padding:0 1.05rem 1rem}.pd-parallel__links a{display:inline-block;margin:.45rem .65rem 0 0;font-weight:900;text-decoration:none}
      .actor-grid>.pd-parallel{grid-column:1/-1;width:100%;margin:.9rem 0}
      @media(max-width:900px){.pd-parallel__collision{grid-template-columns:1fr}.pd-parallel__same{min-height:46px}.pd-parallel__same:before,.pd-parallel__same:after{display:inline;content:'↕';margin:0 .4rem}.pd-parallel__lifeGrid{grid-template-columns:1fr 1fr}}
      @media(max-width:620px){.pd-parallel{width:min(calc(100% - 1rem),1180px);border-width:3px}.pd-parallel__head,.pd-parallel__collision,.pd-parallel__lives{padding:.8rem}.pd-parallel__lifeGrid{grid-template-columns:1fr}.pd-parallel__impact{padding:.8rem;font-size:1rem}.pd-parallel__proof{padding:.75rem .8rem}}
    `;d.head.appendChild(s);
  };

  const html=()=>`<div class="pd-parallel__head"><div class="pd-parallel__k">${c.kicker}</div><h2 class="pd-parallel__title">${c.title}</h2></div><div class="pd-parallel__asset">${c.asset}</div><div class="pd-parallel__collision"><article class="pd-parallel__node pd-parallel__node--left"><div class="pd-parallel__nodeK">${c.leftK}</div><h3>${c.leftN}</h3><div class="pd-parallel__role">${c.leftR}</div><p>${c.leftT}</p></article><div class="pd-parallel__same">${es?'MISMO ACTIVO':'SAME ASSET'}</div><article class="pd-parallel__node pd-parallel__node--right"><div class="pd-parallel__nodeK">${c.rightK}</div><h3>${c.rightN}</h3><div class="pd-parallel__role">${c.rightR}</div><div class="pd-parallel__quote">${c.quote}</div><p>${c.rightT}</p></article></div><div class="pd-parallel__impact">${c.impact}</div><p class="pd-parallel__proof"><strong>${es?'Límite probatorio:':'Evidential boundary:'}</strong> ${c.proof}</p><div class="pd-parallel__lives"><h3>${c.livesTitle}</h3><div class="pd-parallel__lifeGrid">${c.lives.map(x=>`<div class="pd-parallel__life"><strong>${x[0]}</strong><span>${x[1]}</span></div>`).join('')}</div></div><div class="pd-parallel__question"><strong>${c.question}</strong><span>${c.q2}</span></div>${isRsm?`<div class="pd-parallel__rsm"><strong>${c.rsm}</strong><span>${c.rsmT}</span></div>`:''}<div class="pd-parallel__links"><a href="${base}${es?'concurso-36-2012-administrador-concursal/':'insolvency-36-2012-insolvency-administrator/'}">${c.acLink}</a><a href="${base}ric-private-equity-sun-park/">${c.ricpeLink}</a><a href="${base}rsm/nnr4-1025c2f66/">${c.rsmLink}</a></div>`;

  const build=()=>{if(d.querySelector('[data-pd-parallel-lives]'))return null;const box=d.createElement('section');box.className='pd-parallel';box.dataset.pdParallelLives='true';box.innerHTML=html();return box};
  const place=()=>{
    const box=build();if(!box)return;
    if(isHome){
      const grid=d.querySelector('.actor-grid');if(!grid)return;
      const pwc=grid.querySelector('[data-home-actor-family-pwc]');pwc?pwc.insertAdjacentElement('beforebegin',box):grid.appendChild(box);
      setTimeout(()=>{const p=grid.querySelector('[data-home-actor-family-pwc]');if(p&&box.nextElementSibling!==p)p.insertAdjacentElement('beforebegin',box)},1000);
      return;
    }
    if(isRsm){const q=d.querySelector('main .section.alt');q?q.insertAdjacentElement('afterend',box):(d.querySelector('main .hero')||d.querySelector('main')).insertAdjacentElement('afterend',box);return;}
    const hero=d.querySelector('.dossier-hero,.hero');
    const insert=()=>{const rep=d.querySelector('[data-pd-actor-replica]');if(isRicpe&&rep)rep.insertAdjacentElement('afterend',box);else if(hero)hero.insertAdjacentElement('afterend',box);else (d.querySelector('main')||d.body).prepend(box)};
    insert();if(isRicpe)setTimeout(()=>{const rep=d.querySelector('[data-pd-actor-replica]');if(rep&&rep.nextElementSibling!==box)rep.insertAdjacentElement('afterend',box)},1100);
  };
  const run=()=>{addStyle();place()};
  if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',run,{once:true});else run();
})();
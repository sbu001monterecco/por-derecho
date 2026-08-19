(()=>{
  const d=document;
  const path=location.pathname.replace(/\/+$/,'/');
  const es=/\/es\//.test(path);
  const isHome=/\/(en|es)\/$/.test(path);
  const isRicpe=/\/(en|es)\/ric-private-equity-sun-park\/$/.test(path);
  const isRsm=/\/(en|es)\/rsm\/nnr4-1025c2f66\/$/.test(path);
  const isAc=/\/en\/insolvency-36-2012-insolvency-administrator\/$/.test(path)||/\/es\/concurso-36-2012-administrador-concursal\/$/.test(path);
  const isSanTelmo=/\/(en|es)\/san-telmo-ricpe-sun-park\/$/.test(path);
  const isGrantThornton=/\/(en|es)\/grant-thornton\/(2024-04|cuyas-canarias|linkedin-21dec2024|linkedin-21dic2024)\/$/.test(path);
  const parallelRoutes=es?[
    'mismo-hotel-multiples-vidas-financieras','calificacion-concurso-36-2012-vidas-paralelas','ricpe-responsabilidad-documental',
    'orion-ricpe-continuidad','ingenieria-inversa-360-cadena-sun-park','acosta-matos-perimetro','quien-debe-responder-que',
    'administrador-concursal-punto-quiebre-lealtad','concurso-36-2012-responsabilidad-institucional','cnmv-ricpe-verificacion'
  ]:[
    'same-hotel-multiple-financial-lives','insolvency-classification-parallel-lives','ricpe-documentary-accountability',
    'orion-ricpe-platform-continuity','reverse-engineering-360-sun-park-chain','acosta-matos-perimeter','who-should-answer-what',
    'insolvency-administrator-loyalty-breakpoint','insolvency-36-2012-institutional-accountability','cnmv-ricpe-verification'
  ];
  const isParallel=parallelRoutes.some(r=>path.endsWith('/'+r+'/'));
  if(!isHome&&!isRicpe&&!isRsm&&!isAc&&!isSanTelmo&&!isGrantThornton&&!isParallel)return;
  const base=es?'/por-derecho/es/':'/por-derecho/en/';

  const c=es?{
    kicker:'HALLAZGO DOCUMENTAL DOMINANTE · SAN TELMO ↔ RIC PRIVATE EQUITY · 30 NOV 2021',
    title:'MISMO HOTEL. MISMO PERIODO. MISMO PERÍMETRO DE DESPACHO. DOS VIDAS PROFESIONALES EN PARALELO.',
    asset:'SUN PARK / MYND YAIZA · EL MISMO ACTIVO',
    leftK:'VIDA JUDICIAL / CONCURSAL',leftN:'Francisco de Borja Rodríguez-Batllori Laffitte',leftR:'ADMINISTRADOR CONCURSAL · CONCURSO 36/2012 · SAN TELMO',
    leftT:'Sun Park seguía dentro de la vida concursal y del perímetro profesional del Administrador Concursal.',
    rightK:'VIDA INVERSORA / FINANCIERA',rightN:'Eduardo Sánchez',rightR:'SOCIO · SAN TELMO ABOGADOS · 30 NOV 2021',
    quote:'“NOSOTROS EN EL DESPACHO … METIMOS UNOS CUANTOS CLIENTES”',
    rightT:'en la inversión RICPE conectada con el proyecto hotelero Acosta Matos / Sun Park, en conversación directa con Enrique Guerra, Director General de RIC Private Equity.',
    impact:'MIENTRAS UN SOCIO DE SAN TELMO OCUPABA EL PAPEL DE ADMINISTRADOR CONCURSAL EN EL CONCURSO QUE AFECTABA A SUN PARK, OTRO SOCIO DE SAN TELMO RECONOCIÓ QUE EL DESPACHO HABÍA INTRODUCIDO CLIENTES COMO INVERSORES EN LA INVERSIÓN RICPE CONECTADA CON ESE MISMO HOTEL.',
    proof:'Esto acredita la conexión despacho–clientes/inversores–RICPE con el perímetro de inversión Sun Park. No acredita por sí solo una transmisión Borja→Eduardo de información concursal, coordinación entre ambos ni ilicitud: esas cuestiones deben resolverse con registros de conflicto/KYC, comunicaciones, facturación, códigos de asunto, accesos y expedientes.',
    livesTitle:'UN MISMO HOTEL · CUATRO VIDAS PARALELAS QUE DEBEN RECONCILIARSE',
    lives:[['1 · VIDA CONCURSAL','Concurso 36/2012 · Juzgado · Administrador Concursal · liquidación · acreedores'],['2 · VIDA DE CONTROL','Comunidad · acceso · voto · explotación · cinco actores · control de información'],['3 · VIDA DE INVERSIÓN','CAM · RICPE · clientes/inversores introducidos por San Telmo · due diligence · financiación · reforma'],['4 · VIDA DE PROPIEDAD / OPERACIÓN','CAM → HNT → MYND Yaiza · continuidad patrimonial y operativa']],
    question:'¿QUIÉN SABÍA QUE EL MISMO HOTEL ESTABA VIVIENDO TODAS ESTAS VIDAS EN PARALELO?',
    q2:'¿Quién tenía los documentos? ¿Quién introdujo inversores? ¿Quién controlaba el expediente concursal? ¿Quién representaba la propiedad? ¿Quién aprobaba la inversión? ¿Quién reconcilió —o no reconcilió— los registros paralelos?',
    rsmH:'RSM SPAIN · NNR4-1025C2F66 · PRUEBA DE NO FRAGMENTACIÓN',rsmT:'La revisión de Ethics & Independence debe preservar, identificar, reconciliar y explicar qué muestran los registros heredados de San Telmo sobre la vida concursal y la vida inversora del mismo activo.',
    gtH:'GRANT THORNTON · MEMORIA DE CONFLICTO 2020 → PERÍMETRO PROFESIONAL / COMERCIAL 2023–2025',gtT:'Grant Thornton ya recibió en 2020 un control de conflicto que identificaba a Borja y a CAM/Sun Park. El hallazgo San Telmo–RICPE de 2021 hace más concreta la reconciliación posterior: si esa memoria de conflicto estaba disponible o fue consultada cuando comenzó o continuó la relación Cuyás / Grant Thornton Canarias, y qué registros se preservaron. Esto no convierte a Grant Thornton en participante del evento San Telmo/RICPE.',
    sanH:'SAN TELMO · COLISIÓN PROFESIONAL SOBRE EL MISMO ACTIVO',sanT:'Este es el puente canónico San Telmo: una vida profesional corresponde a la administración concursal; la otra, a la declaración contemporánea de otro socio de que el despacho introdujo clientes en la inversión RICPE conectada con el mismo hotel. La transmisión de información y la coordinación son cuestiones probatorias separadas.',
    acH:'ADMINISTRADOR CONCURSAL · PREGUNTA DE RECONCILIACIÓN',acT:'La cuestión para el perímetro del AC es qué sabía, qué documentos tenía y qué separación real existía entre el expediente concursal y la vida inversora del mismo activo dentro del entorno profesional San Telmo.',
    ricpeH:'RIC PRIVATE EQUITY · MISMO ACTIVO / VIDA INVERSORA',ricpeT:'El registro inversor debe reconciliar quién introdujo inversores, qué proyecto se les asignó, qué título y propiedad se comprobaron y qué conocían RICPE, CAM y sus asesores mientras Sun Park seguía en la vida concursal.',
    genericH:'RECONCILIACIÓN UNITARIA · MISMO ACTIVO',genericT:'Esta página debe leerse junto con las otras vidas del activo. Ninguna cronología aislada explica por sí sola el resultado final.',
    acLink:'Administrador Concursal →',ricpeLink:'RICPE / Sun Park →',rsmLink:'RSM NNR4 →',sanLink:'San Telmo / RICPE →',gtLink:'Grant Thornton →',sameLink:'Vidas paralelas →'
  }:{
    kicker:'DOMINANT DOCUMENTARY FINDING · SAN TELMO ↔ RIC PRIVATE EQUITY · 30 NOV 2021',
    title:'SAME HOTEL. SAME PERIOD. SAME LAW-FIRM PERIMETER. TWO PARALLEL PROFESSIONAL LIVES.',
    asset:'SUN PARK / MYND YAIZA · THE SAME ASSET',
    leftK:'JUDICIAL / INSOLVENCY LIFE',leftN:'Francisco de Borja Rodríguez-Batllori Laffitte',leftR:'INSOLVENCY ADMINISTRATOR · CONCURSO 36/2012 · SAN TELMO',
    leftT:'Sun Park remained inside the insolvency life and within the Insolvency Administrator’s professional perimeter.',
    rightK:'INVESTMENT / FINANCING LIFE',rightN:'Eduardo Sánchez',rightR:'PARTNER · SAN TELMO ABOGADOS · 30 NOV 2021',
    quote:'“NOSOTROS EN EL DESPACHO … METIMOS UNOS CUANTOS CLIENTES”',
    rightT:'into the RICPE investment connected with the Acosta Matos / Sun Park hotel project, in direct discussion with Enrique Guerra, Director General of RIC Private Equity.',
    impact:'WHILE ONE SAN TELMO PARTNER OCCUPIED THE INSOLVENCY-ADMINISTRATOR ROLE IN THE INSOLVENCY AFFECTING SUN PARK, ANOTHER SAN TELMO PARTNER ACKNOWLEDGED THAT THE FIRM HAD PUT CLIENTS IN AS INVESTORS IN THE RICPE INVESTMENT CONNECTED TO THAT SAME HOTEL.',
    proof:'This establishes the law-firm/client-investor/RICPE connection to the Sun Park investment perimeter. It does not, by itself, establish Borja→Eduardo transfer of insolvency information, coordination between them, or unlawfulness: those questions must be resolved from conflicts/KYC, communications, billing, matter codes, access and matter records.',
    livesTitle:'ONE HOTEL · FOUR PARALLEL LIVES THAT MUST BE RECONCILED',
    lives:[['1 · INSOLVENCY LIFE','Concurso 36/2012 · Court · Insolvency Administrator · liquidation · creditors'],['2 · CONTROL LIFE','Community · access · voting · exploitation · five actors · information control'],['3 · INVESTMENT LIFE','CAM · RICPE · San Telmo-introduced clients/investors · due diligence · financing · renovation'],['4 · OWNERSHIP / OPERATING LIFE','CAM → HNT → MYND Yaiza · ownership and operational continuity']],
    question:'WHO KNEW THAT THE SAME HOTEL WAS LIVING ALL THESE LIVES IN PARALLEL?',
    q2:'Who held the documents? Who introduced investors? Who controlled the insolvency file? Who represented ownership? Who approved the investment? Who reconciled — or failed to reconcile — the parallel records?',
    rsmH:'RSM SPAIN · NNR4-1025C2F66 · NON-FRAGMENTATION TEST',rsmT:'The Ethics & Independence review should preserve, identify, reconcile and explain what the San Telmo legacy records show about the insolvency and investor lives of the same asset.',
    gtH:'GRANT THORNTON · 2020 CONFLICT MEMORY → 2023–2025 PROFESSIONAL / COMMERCIAL PERIMETER',gtT:'Grant Thornton already received a 2020 conflict check identifying Borja and CAM/Sun Park. The 2021 San Telmo–RICPE finding sharpens the later reconciliation: whether that conflict memory was available or consulted when the Cuyás / Grant Thornton Canarias relationship began or continued, and what records were preserved. This does not make Grant Thornton a participant in the San Telmo/RICPE event.',
    sanH:'SAN TELMO · SAME-ASSET PROFESSIONAL COLLISION',sanT:'This is the canonical San Telmo bridge: one professional life concerns the insolvency administration; the other concerns another partner’s contemporaneous statement that the firm put clients into the RICPE investment connected with the same hotel. Information transfer and coordination remain separate evidential questions.',
    acH:'INSOLVENCY ADMINISTRATOR · RECONCILIATION QUESTION',acT:'The AC-perimeter question is what was known, what records were held and what real separation existed between the insolvency file and the same asset’s investor life within the San Telmo professional environment.',
    ricpeH:'RIC PRIVATE EQUITY · SAME ASSET / INVESTMENT LIFE',ricpeT:'The investor record must reconcile who introduced investors, which project they entered, what title/ownership was checked and what RICPE, CAM and advisers knew while Sun Park remained in the insolvency life.',
    genericH:'UNITARY RECONCILIATION · SAME ASSET',genericT:'This page must be read against the asset’s other parallel lives. No isolated chronology explains the final result by itself.',
    acLink:'Insolvency Administrator →',ricpeLink:'RICPE / Sun Park →',rsmLink:'RSM NNR4 →',sanLink:'San Telmo / RICPE →',gtLink:'Grant Thornton →',sameLink:'Parallel lives →'
  };

  const pageFooter=()=>{
    if(isRsm)return [c.rsmH,c.rsmT];
    if(isGrantThornton)return [c.gtH,c.gtT];
    if(isSanTelmo)return [c.sanH,c.sanT];
    if(isAc)return [c.acH,c.acT];
    if(isRicpe)return [c.ricpeH,c.ricpeT];
    return [c.genericH,c.genericT];
  };

  const addStyle=()=>{
    if(d.querySelector('style[data-pd-parallel-lives]'))return;
    const s=d.createElement('style');s.dataset.pdParallelLives='20260819b';s.textContent=`
      .pd-parallel{margin:1.1rem auto 2rem;width:min(calc(100% - 2rem),1180px);border:4px solid #a40000;border-radius:16px;background:#fff;box-shadow:0 10px 28px rgba(64,0,0,.14);overflow:hidden;color:#17242b}.pd-parallel__head{padding:1rem 1.15rem .9rem;background:#fff7f5}.pd-parallel__k{font-size:.76rem;font-weight:1000;letter-spacing:.08em;text-transform:uppercase;color:#b00000}.pd-parallel__title{margin:.32rem 0 0;font-size:clamp(1.55rem,3vw,2.65rem);line-height:1.02;font-weight:1000;color:#9d0000}.pd-parallel__asset{text-align:center;padding:.6rem 1rem;background:#131f27;color:#fff;font-weight:1000;letter-spacing:.06em}.pd-parallel__collision{display:grid;grid-template-columns:1fr 90px 1fr;gap:.75rem;padding:1rem}.pd-parallel__node{border:1px solid #d9c5c1;border-radius:13px;padding:1rem;background:#fff}.pd-parallel__node--left{border-top:7px solid #17242b}.pd-parallel__node--right{border-top:7px solid #b00000}.pd-parallel__nodeK{font-size:.72rem;font-weight:1000;letter-spacing:.07em;color:#6b777c;text-transform:uppercase}.pd-parallel__node h3{margin:.3rem 0 .2rem;font-size:1.17rem;line-height:1.15}.pd-parallel__role{font-size:.79rem;font-weight:950;color:#7e1515}.pd-parallel__quote{margin:.75rem 0;padding:.72rem;border-radius:9px;background:#b00000;color:#fff;font-size:clamp(1rem,2vw,1.35rem);font-weight:1000;line-height:1.12}.pd-parallel__same{display:flex;align-items:center;justify-content:center;text-align:center;font-weight:1000;color:#a40000;font-size:.8rem;line-height:1.15}.pd-parallel__same:before,.pd-parallel__same:after{content:'↔';display:block;font-size:1.7rem;margin:.2rem}.pd-parallel__impact{padding:.9rem 1.1rem;background:#a40000;color:#fff;font-weight:1000;font-size:clamp(1rem,1.8vw,1.35rem);line-height:1.25;text-align:center}.pd-parallel__proof{margin:0;padding:.85rem 1.1rem;background:#fff2df;border-bottom:1px solid #ead4b1;font-size:.88rem;line-height:1.45}.pd-parallel__lives{padding:1rem 1.1rem}.pd-parallel__lives h3{margin:0 0 .75rem;text-align:center;color:#8f0000}.pd-parallel__lifeGrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.65rem}.pd-parallel__life{padding:.8rem;border:1px solid #d7dfe2;border-radius:10px;background:#f8fafb}.pd-parallel__life strong{display:block;margin-bottom:.3rem;font-size:.82rem}.pd-parallel__life span{font-size:.78rem;line-height:1.35;color:#4e6068}.pd-parallel__question{padding:.9rem 1.05rem;background:#131f27;color:#fff;text-align:center}.pd-parallel__question strong{display:block;color:#ffb3ad;font-size:clamp(1.05rem,2vw,1.45rem)}.pd-parallel__question span{display:block;margin-top:.35rem;font-size:.86rem;line-height:1.4}.pd-parallel__context{padding:.9rem 1.05rem;border-top:4px solid #b00000;background:#f4f6f7}.pd-parallel__context strong{display:block;color:#a40000;font-size:1rem}.pd-parallel__context span{display:block;margin-top:.28rem;line-height:1.42}.pd-parallel__links{padding:0 1.05rem 1rem}.pd-parallel__links a{display:inline-block;margin:.45rem .65rem 0 0;font-weight:900;text-decoration:none}.actor-grid>.pd-parallel{grid-column:1/-1;width:100%;margin:.9rem 0}@media(max-width:900px){.pd-parallel__collision{grid-template-columns:1fr}.pd-parallel__same{min-height:46px}.pd-parallel__same:before,.pd-parallel__same:after{display:inline;content:'↕';margin:0 .4rem}.pd-parallel__lifeGrid{grid-template-columns:1fr 1fr}}@media(max-width:620px){.pd-parallel{width:min(calc(100% - 1rem),1180px);border-width:3px}.pd-parallel__head,.pd-parallel__collision,.pd-parallel__lives{padding:.8rem}.pd-parallel__lifeGrid{grid-template-columns:1fr}.pd-parallel__impact{padding:.8rem;font-size:1rem}.pd-parallel__proof{padding:.75rem .8rem}}
    `;d.head.appendChild(s);
  };

  const html=()=>{const f=pageFooter();return `<div class="pd-parallel__head"><div class="pd-parallel__k">${c.kicker}</div><h2 class="pd-parallel__title">${c.title}</h2></div><div class="pd-parallel__asset">${c.asset}</div><div class="pd-parallel__collision"><article class="pd-parallel__node pd-parallel__node--left"><div class="pd-parallel__nodeK">${c.leftK}</div><h3>${c.leftN}</h3><div class="pd-parallel__role">${c.leftR}</div><p>${c.leftT}</p></article><div class="pd-parallel__same">${es?'MISMO ACTIVO':'SAME ASSET'}</div><article class="pd-parallel__node pd-parallel__node--right"><div class="pd-parallel__nodeK">${c.rightK}</div><h3>${c.rightN}</h3><div class="pd-parallel__role">${c.rightR}</div><div class="pd-parallel__quote">${c.quote}</div><p>${c.rightT}</p></article></div><div class="pd-parallel__impact">${c.impact}</div><p class="pd-parallel__proof"><strong>${es?'Límite probatorio:':'Evidential boundary:'}</strong> ${c.proof}</p><div class="pd-parallel__lives"><h3>${c.livesTitle}</h3><div class="pd-parallel__lifeGrid">${c.lives.map(x=>`<div class="pd-parallel__life"><strong>${x[0]}</strong><span>${x[1]}</span></div>`).join('')}</div></div><div class="pd-parallel__question"><strong>${c.question}</strong><span>${c.q2}</span></div><div class="pd-parallel__context"><strong>${f[0]}</strong><span>${f[1]}</span></div><div class="pd-parallel__links"><a href="${base}${es?'concurso-36-2012-administrador-concursal/':'insolvency-36-2012-insolvency-administrator/'}">${c.acLink}</a><a href="${base}ric-private-equity-sun-park/">${c.ricpeLink}</a><a href="${base}san-telmo-ricpe-sun-park/">${c.sanLink}</a><a href="${base}rsm/nnr4-1025c2f66/">${c.rsmLink}</a><a href="${base}grant-thornton/2024-04/">${c.gtLink}</a><a href="${base}${es?'mismo-hotel-multiples-vidas-financieras/':'same-hotel-multiple-financial-lives/'}">${c.sameLink}</a></div>`};
  const build=()=>{if(d.querySelector('section[data-pd-parallel-lives="true"]'))return null;const box=d.createElement('section');box.className='pd-parallel';box.dataset.pdParallelLives='true';box.innerHTML=html();return box};
  const place=()=>{const box=build();if(!box)return;if(isHome){const five=d.querySelector('section[data-pd-five-ac]');if(five){five.insertAdjacentElement('afterend',box);return}const intro=d.querySelector('.actor-intro');if(intro){intro.insertAdjacentElement('beforebegin',box);return}}const hero=d.querySelector('.dossier-hero,.hero,main>section:first-child');if(hero)hero.insertAdjacentElement('afterend',box);else{const main=d.querySelector('main');main?main.prepend(box):d.body.prepend(box)}};
  const run=()=>{addStyle();place()};if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',run,{once:true});else run();
})();
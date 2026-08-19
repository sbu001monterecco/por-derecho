(()=>{
  const d=document;
  const path=location.pathname.replace(/\/+$/,'/');
  const isHome=/(\/en\/|\/es\/)$/.test(path);
  const isPwc=/(\/en\/|\/es\/)pwc-canarias-carlos-saavedra-sun-park\/$/.test(path);
  const isRicpe=/(\/en\/|\/es\/)ric-private-equity-sun-park\/$/.test(path);
  if(!isHome&&!isPwc&&!isRicpe)return;
  const es=/\/es\//.test(path);

  const copy=es?{
    relation:{
      fmmm:'ESPOSO DE SHAILA MARÍA COGOLLUDO RAMOS',
      antonio:'PADRE DE SHAILA MARÍA COGOLLUDO RAMOS',
      shaila:'HIJA DE ANTONIO COGOLLUDO ROJAS · ESPOSA DE FRANCISCO MARIO MATOS MATAS'
    },
    chronology:{
      fmmm:'ADMINISTRADOR DE LA COMUNIDAD DOCUMENTADO DESDE EL 22 JUN 2011 → AL MENOS 2022',
      antonio:'DOCUMENTADO EN EL PERÍMETRO COMUNIDAD SUN PARK / PAMANIL DESDE EL 10 ABR 2014 → CONTINUIDAD POSTERIOR',
      shaila:'DOCUMENTADA EN EL PERÍMETRO DE COMUNICACIONES PAMANIL / COMUNIDAD DESDE EL 8 ABR 2014 → CONTINUIDAD POSTERIOR',
      jdam:'2017–2018 entrada en el perímetro → 2022 control → continuidad posterior',
      laura:'2017–2018 función legal/concursal y acceso → 2022 representación CAM → continuidad posterior'
    },
    chronologyBoundary:'FECHAS MÍNIMAS BLOQUEADAS: acreditan implicación no más tarde de la fecha indicada; no afirman que ese fuera el primer día real.',
    noteK:'2016 · PUNTO DE CONTROL DE CONOCIMIENTO PROFESIONAL · PWC / CARLOS SAAVEDRA',
    quote:'“LA VÍA PENAL CONTRA ESTA GENTE”',
    note:'Mientras PwC/Carlos Saavedra asesoraban sobre Sun Park y la controversia de la Comunidad, el cliente comunicó alegaciones graves sobre el perímetro entonces adverso y dio una instrucción expresa de acudir a la vía penal. PwC respondió “Tomamos nota de vuestra decisión” —Carlos en copia— y posteriormente confirmó contacto directo con el Administrador Concursal.',
    why:'Acredita que las preocupaciones sobre la estructura de Comunidad/control estaban siendo planteadas contemporáneamente a asesores profesionales externos en 2016, no reconstruidas sólo años después.',
    boundary:'Límite: no significa que PwC determinara de forma independiente que FMMM, Antonio Cogolludo, Shaila Cogolludo o cualquier otra persona hubiera cometido un delito.',
    actorTitle:'Perímetro Comunidad/control relacionado con el punto de conocimiento PwC',
    pagePwc:'Este bloque fija visualmente el perímetro histórico y corrige las fechas mínimas de Antonio y Shaila mediante fuentes de 2014.',
    pageRicpe:'Este bloque muestra por qué el conocimiento previo de PwC y la historia anterior de la Comunidad importan para los controles, conflictos y due diligence posteriores.',
    homeLink:'Ver mapa principal de actores →',
    pwcLink:'Ver expediente PwC / Carlos 2016 →',
    ricpeLink:'Ver expediente RICPE / Sun Park →',
    registerLink:'Ver registro canónico de personas, entidades y representantes →'
  }:{
    relation:{
      fmmm:'HUSBAND OF SHAILA MARÍA COGOLLUDO RAMOS',
      antonio:'FATHER OF SHAILA MARÍA COGOLLUDO RAMOS',
      shaila:'DAUGHTER OF ANTONIO COGOLLUDO ROJAS · WIFE OF FRANCISCO MARIO MATOS MATAS'
    },
    chronology:{
      fmmm:'COMMUNITY ADMINISTRATOR DOCUMENTED BY 22 JUN 2011 → AT LEAST 2022',
      antonio:'DOCUMENTED IN THE SUN PARK COMMUNITY / PAMANIL PERIMETER BY 10 APR 2014 → LATER CONTINUITY',
      shaila:'DOCUMENTED IN THE PAMANIL / COMMUNITY COMMUNICATIONS PERIMETER BY 8 APR 2014 → LATER CONTINUITY',
      jdam:'2017–2018 entry into perimeter → 2022 control → later continuity',
      laura:'2017–2018 legal/insolvency and access role → 2022 CAM representation → later continuity'
    },
    chronologyBoundary:'LOCKED MINIMUM DATES: they prove involvement no later than the stated date; they do not claim that date was the actor’s true first day.',
    noteK:'2016 · PROFESSIONAL KNOWLEDGE CHECKPOINT · PWC / CARLOS SAAVEDRA',
    quote:'“LA VÍA PENAL CONTRA ESTA GENTE”',
    note:'While PwC/Carlos Saavedra were advising on Sun Park and the Community dispute, the client communicated serious allegations concerning the then-adverse perimeter and expressly instructed that the response proceed through the penal route. PwC recorded “Tomamos nota de vuestra decisión” —Carlos copied— and later confirmed direct contact with the Insolvency Administrator.',
    why:'It establishes that concerns about the Community/control structure were being raised contemporaneously with external professional advisers in 2016, rather than being reconstructed only years later.',
    boundary:'Boundary: this does not mean PwC independently determined that FMMM, Antonio Cogolludo, Shaila Cogolludo or any other person had committed a crime.',
    actorTitle:'Community/control perimeter connected to the PwC knowledge checkpoint',
    pagePwc:'This block fixes the historical perimeter visually and corrects Antonio and Shaila’s minimum dates from primary 2014 sources.',
    pageRicpe:'This block shows why PwC’s prior knowledge and the earlier Community history matter to later controls, conflicts and due-diligence questions.',
    homeLink:'See the main actor map →',
    pwcLink:'See the full 2016 PwC / Carlos record →',
    ricpeLink:'See the RICPE / Sun Park record →',
    registerLink:'See the canonical people, entities and representatives register →'
  };

  const base=es?'/por-derecho/es/':'/por-derecho/en/';
  const registerRoute=base+(es?'actores-partes-abogados-representantes/':'actors-parties-lawyers-representatives/');

  const ensureStyle=()=>{
    if(d.querySelector('style[data-pd-actor-visual]'))return;
    const style=d.createElement('style');
    style.dataset.pdActorVisual='20260819c';
    style.textContent=`
      .pd-rel{display:block;margin:.65rem 0 .45rem;padding:.52rem .62rem;border:1px solid #c74b43;border-radius:9px;background:#fff4f1;color:#7e2929;font-size:.76rem;font-weight:950;line-height:1.25;letter-spacing:.02em;overflow-wrap:anywhere}
      .pd-chron{display:block;margin:.45rem 0 .6rem;padding:.55rem .62rem;border-radius:8px;background:#13252d;color:#fff;font-size:.76rem;font-weight:950;line-height:1.25;overflow-wrap:anywhere}
      .pd-history-lock{grid-column:1/-1;margin:.65rem 0 0;padding:.65rem .8rem;border-left:6px solid #9a6a20;background:#fff4d7;border-radius:9px;font-size:.78rem;font-weight:900;line-height:1.35;color:#3f3321}
      .pd-pwc-home,.pd-actor-replica{margin-top:.9rem;padding:1rem 1.1rem;border:3px solid #a32620;border-radius:16px;background:#fff8f5;box-shadow:0 6px 20px rgba(19,37,45,.09);min-width:0}
      .pd-pwc-home{grid-column:1/-1}.pd-pwc-home__k,.pd-actor-replica__k{font-size:.76rem;font-weight:950;letter-spacing:.07em;color:#a32620;text-transform:uppercase}.pd-pwc-home__q,.pd-actor-replica__q{font-size:clamp(1.45rem,3vw,2.45rem);line-height:1.03;font-weight:1000;color:#a32620;margin:.45rem 0 .65rem;overflow-wrap:anywhere}.pd-pwc-home__grid,.pd-actor-replica__body{display:grid;grid-template-columns:1.5fr 1fr;gap:1rem}.pd-pwc-home p,.pd-actor-replica p{margin:.4rem 0}.pd-pwc-home__why,.pd-actor-replica__why{padding:.7rem .8rem;border-left:5px solid #9a6a20;background:#fff4d7;border-radius:9px}.pd-pwc-home__boundary,.pd-actor-replica__boundary{font-size:.88rem;color:#53656d}.pd-pwc-home a,.pd-actor-replica a{display:inline-block;margin:.55rem .65rem 0 0;font-weight:900;text-decoration:none}
      .pd-actor-replica{width:min(calc(100% - 2rem),74rem);margin:1rem auto 2rem}.pd-actor-replica__intro{margin:.3rem 0 .8rem;color:#53656d}.pd-actor-replica__actors{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.7rem;margin:.9rem 0}.pd-actor-replica__actors article{min-width:0;padding:.85rem;border:1px solid #dbcfc9;border-top:5px solid #a32620;border-radius:12px;background:#fff}.pd-actor-replica__actors strong{display:block;font-size:1rem;line-height:1.2}.pd-actor-replica__actors small{display:block;margin-top:.4rem;color:#53656d;line-height:1.35;font-weight:750}.pd-actor-replica__relation{display:block;margin-top:.55rem;padding:.45rem .55rem;border-radius:8px;background:#fff0ec;color:#7e2929;font-size:.73rem;font-weight:900;line-height:1.25;overflow-wrap:anywhere}
      @media(max-width:980px){.actor-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}.pd-actor-replica__actors{grid-template-columns:repeat(2,minmax(0,1fr))}.pd-actor-replica__actors article:last-child{grid-column:1/-1}}
      @media(max-width:760px){.actor-grid{grid-template-columns:1fr!important}.pd-pwc-home__grid,.pd-actor-replica__body,.pd-actor-replica__actors{grid-template-columns:1fr}.pd-actor-replica__actors article:last-child{grid-column:auto}.pd-pwc-home,.pd-actor-replica{padding:.9rem;border-width:2px;border-radius:12px}.pd-pwc-home__q,.pd-actor-replica__q{font-size:clamp(1.35rem,8vw,2rem)}.pd-rel,.pd-chron{font-size:.73rem}.pd-actor-replica a{display:block;width:fit-content}}
      @media(max-width:390px){.pd-pwc-home,.pd-actor-replica{padding:.75rem}.pd-pwc-home__q,.pd-actor-replica__q{font-size:1.35rem}.pd-actor-replica{width:min(calc(100% - 1rem),74rem)}}
    `;
    d.head.appendChild(style);
  };

  const renderHome=()=>{
    const grid=d.querySelector('.actor-grid');
    if(!grid||d.querySelector('[data-home-actor-family-pwc]'))return;
    const cards=[...grid.querySelectorAll('article')];
    const find=n=>cards.find(c=>(c.textContent||'').includes(n));
    const f=find('Francisco Mario Matos Matas');
    const a=find('Antonio Cogolludo Rojas');
    const s=find('Shaila María Cogolludo Ramos');
    const j=find('José Daniel Acosta Matos');
    const l=find('Laura Patricia Acosta Matos');
    if(!f||!a||!s)return;
    const add=(card,rel,chron)=>{
      const name=card.querySelector('strong');
      if(name&&rel&&!card.querySelector('.pd-rel')){const r=d.createElement('span');r.className='pd-rel';r.textContent=rel;name.insertAdjacentElement('afterend',r)}
      if(chron&&!card.querySelector('.pd-chron')){const c=d.createElement('span');c.className='pd-chron';c.textContent=chron;(card.querySelector('.pd-rel')||name).insertAdjacentElement('afterend',c)}
    };
    add(f,copy.relation.fmmm,copy.chronology.fmmm);add(a,copy.relation.antonio,copy.chronology.antonio);add(s,copy.relation.shaila,copy.chronology.shaila);if(j)add(j,null,copy.chronology.jdam);if(l)add(l,null,copy.chronology.laura);
    const lock=d.createElement('div');lock.className='pd-history-lock';lock.dataset.pdActorHistoryLock='true';lock.textContent=copy.chronologyBoundary;grid.appendChild(lock);
    const note=d.createElement('aside');note.className='pd-pwc-home';note.dataset.homeActorFamilyPwc='true';
    note.innerHTML=`<div class="pd-pwc-home__k">${copy.noteK}</div><div class="pd-pwc-home__q">${copy.quote}</div><div class="pd-pwc-home__grid"><div><p>${copy.note}</p><a href="${base}pwc-canarias-carlos-saavedra-sun-park/">${copy.pwcLink}</a><a href="${base}ric-private-equity-sun-park/">${copy.ricpeLink}</a><a href="${registerRoute}">${copy.registerLink}</a></div><div><p class="pd-pwc-home__why"><strong>${copy.why}</strong></p><p class="pd-pwc-home__boundary">${copy.boundary}</p></div></div>`;
    grid.appendChild(note);
  };

  const renderReplica=()=>{
    if(d.querySelector('[data-pd-actor-replica]'))return;
    const hero=d.querySelector('.dossier-hero');
    if(!hero)return;
    const box=d.createElement('section');box.className='pd-actor-replica';box.dataset.pdActorReplica=isPwc?'pwc':'ricpe';
    const context=isPwc?copy.pagePwc:copy.pageRicpe;
    box.innerHTML=`<div class="pd-actor-replica__k">${copy.noteK}</div><div class="pd-actor-replica__q">${copy.quote}</div><p class="pd-actor-replica__intro"><strong>${copy.actorTitle}.</strong> ${context}</p><p class="pd-history-lock">${copy.chronologyBoundary}</p><div class="pd-actor-replica__actors"><article><strong>Francisco Mario Matos Matas (FMMM)</strong><span class="pd-actor-replica__relation">${copy.relation.fmmm}</span><small>${copy.chronology.fmmm}</small></article><article><strong>Antonio Cogolludo Rojas</strong><span class="pd-actor-replica__relation">${copy.relation.antonio}</span><small>${copy.chronology.antonio}</small></article><article><strong>Shaila María Cogolludo Ramos</strong><span class="pd-actor-replica__relation">${copy.relation.shaila}</span><small>${copy.chronology.shaila}</small></article></div><div class="pd-actor-replica__body"><div><p>${copy.note}</p><a href="${base}">${copy.homeLink}</a>${isRicpe?`<a href="${base}pwc-canarias-carlos-saavedra-sun-park/">${copy.pwcLink}</a>`:`<a href="${base}ric-private-equity-sun-park/">${copy.ricpeLink}</a>`}<a href="${registerRoute}">${copy.registerLink}</a></div><div><p class="pd-actor-replica__why"><strong>${copy.why}</strong></p><p class="pd-actor-replica__boundary">${copy.boundary}</p></div></div>`;
    hero.insertAdjacentElement('afterend',box);
    const pin=()=>{if(hero.nextElementSibling!==box)hero.insertAdjacentElement('afterend',box)};
    setTimeout(pin,250);setTimeout(pin,900);
  };

  const render=()=>{ensureStyle();if(isHome)renderHome();else renderReplica();};
  if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',render,{once:true});else render();
})();
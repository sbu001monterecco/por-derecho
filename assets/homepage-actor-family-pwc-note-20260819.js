(()=>{
  const d=document;
  const path=location.pathname.replace(/\/+$/,'/');
  const en=path.endsWith('/en/');
  const es=path.endsWith('/es/');
  if(!en&&!es)return;

  const copy=es?{
    relation:{
      fmmm:'ESPOSO DE SHAILA MARÍA COGOLLUDO RAMOS',
      antonio:'PADRE DE SHAILA MARÍA COGOLLUDO RAMOS',
      shaila:'HIJA DE ANTONIO COGOLLUDO ROJAS · ESPOSA DE FRANCISCO MARIO MATOS MATAS'
    },
    chronology:{
      fmmm:'2011 → al menos 2022 documentado',
      antonio:'2018 → continuidad posterior en el perímetro empresarial documentada',
      shaila:'2017 → continuidad posterior en el perímetro empresarial documentada',
      jdam:'2017–2018 entrada en el perímetro → 2022 control → continuidad posterior',
      laura:'2017–2018 función legal/concursal y acceso → 2022 representación CAM → continuidad posterior'
    },
    noteK:'2016 · PUNTO DE CONTROL DE CONOCIMIENTO PROFESIONAL · PWC / CARLOS SAAVEDRA',
    quote:'“LA VÍA PENAL CONTRA ESTA GENTE”',
    note:'Mientras PwC/Carlos Saavedra asesoraban sobre Sun Park y la controversia de la Comunidad, el cliente comunicó alegaciones graves sobre el perímetro entonces adverso y dio una instrucción expresa de acudir a la vía penal. PwC respondió “Tomamos nota de vuestra decisión” —Carlos en copia— y posteriormente confirmó contacto directo con el Administrador Concursal.',
    why:'Por qué aparece junto a FMMM y los Cogolludo: acredita que las preocupaciones sobre la estructura de Comunidad/control estaban siendo planteadas contemporáneamente a asesores profesionales externos en 2016, no reconstruidas sólo años después.',
    boundary:'Límite: no significa que PwC determinara de forma independiente que FMMM, Antonio Cogolludo, Shaila Cogolludo o cualquier otra persona hubiera cometido un delito.',
    link:'Ver expediente PwC / Carlos 2016 →'
  }:{
    relation:{
      fmmm:'HUSBAND OF SHAILA MARÍA COGOLLUDO RAMOS',
      antonio:'FATHER OF SHAILA MARÍA COGOLLUDO RAMOS',
      shaila:'DAUGHTER OF ANTONIO COGOLLUDO ROJAS · WIFE OF FRANCISCO MARIO MATOS MATAS'
    },
    chronology:{
      fmmm:'2011 → at least 2022 documented',
      antonio:'2018 → later documented business-perimeter continuity',
      shaila:'2017 → later documented business-perimeter continuity',
      jdam:'2017–2018 entry into perimeter → 2022 control → later continuity',
      laura:'2017–2018 legal/insolvency and access role → 2022 CAM representation → later continuity'
    },
    noteK:'2016 · PROFESSIONAL KNOWLEDGE CHECKPOINT · PWC / CARLOS SAAVEDRA',
    quote:'“LA VÍA PENAL CONTRA ESTA GENTE”',
    note:'While PwC/Carlos Saavedra were advising on Sun Park and the Community dispute, the client communicated serious allegations concerning the then-adverse perimeter and expressly instructed that the response proceed through the penal route. PwC recorded “Tomamos nota de vuestra decisión” —Carlos copied— and later confirmed direct contact with the Insolvency Administrator.',
    why:'Why this sits beside FMMM and the Cogolludos: it establishes that concerns about the Community/control structure were being raised contemporaneously with external professional advisers in 2016, rather than being reconstructed only years later.',
    boundary:'Boundary: this does not mean PwC independently determined that FMMM, Antonio Cogolludo, Shaila Cogolludo or any other person had committed a crime.',
    link:'See the full 2016 PwC / Carlos record →'
  };

  const render=()=>{
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

    const style=d.createElement('style');
    style.textContent=`
      .pd-rel{display:block;margin:.65rem 0 .45rem;padding:.52rem .62rem;border:1px solid #c74b43;border-radius:9px;background:#fff4f1;color:#7e2929;font-size:.76rem;font-weight:950;line-height:1.25;letter-spacing:.02em}
      .pd-chron{display:block;margin:.45rem 0 .6rem;padding:.5rem .62rem;border-radius:8px;background:#13252d;color:#fff;font-size:.78rem;font-weight:900;line-height:1.25}
      .pd-pwc-home{grid-column:1/-1;margin-top:.9rem;padding:1rem 1.1rem;border:3px solid #a32620;border-radius:16px;background:#fff8f5;box-shadow:0 6px 20px rgba(19,37,45,.09)}
      .pd-pwc-home__k{font-size:.76rem;font-weight:950;letter-spacing:.07em;color:#a32620}.pd-pwc-home__q{font-size:clamp(1.45rem,3vw,2.45rem);line-height:1;font-weight:1000;color:#a32620;margin:.45rem 0 .65rem}.pd-pwc-home__grid{display:grid;grid-template-columns:1.5fr 1fr;gap:1rem}.pd-pwc-home p{margin:.4rem 0}.pd-pwc-home__why{padding:.7rem .8rem;border-left:5px solid #9a6a20;background:#fff4d7;border-radius:9px}.pd-pwc-home__boundary{font-size:.88rem;color:#53656d}.pd-pwc-home a{display:inline-block;margin-top:.55rem;font-weight:900;text-decoration:none}
      @media(max-width:760px){.pd-pwc-home__grid{grid-template-columns:1fr}}
    `;
    d.head.appendChild(style);

    const add=(card,rel,chron)=>{
      const name=card.querySelector('strong');
      if(name&&rel){const r=d.createElement('span');r.className='pd-rel';r.textContent=rel;name.insertAdjacentElement('afterend',r)}
      if(chron){const c=d.createElement('span');c.className='pd-chron';c.textContent=chron;(card.querySelector('.pd-rel')||name).insertAdjacentElement('afterend',c)}
    };
    add(f,copy.relation.fmmm,copy.chronology.fmmm);
    add(a,copy.relation.antonio,copy.chronology.antonio);
    add(s,copy.relation.shaila,copy.chronology.shaila);
    if(j)add(j,null,copy.chronology.jdam);
    if(l)add(l,null,copy.chronology.laura);

    const note=d.createElement('aside');
    note.className='pd-pwc-home';note.dataset.homeActorFamilyPwc='true';
    note.innerHTML=`<div class="pd-pwc-home__k">${copy.noteK}</div><div class="pd-pwc-home__q">${copy.quote}</div><div class="pd-pwc-home__grid"><div><p>${copy.note}</p><a href="${es?'pwc-canarias-carlos-saavedra-sun-park/':'pwc-canarias-carlos-saavedra-sun-park/'}">${copy.link}</a></div><div><p class="pd-pwc-home__why"><strong>${copy.why}</strong></p><p class="pd-pwc-home__boundary">${copy.boundary}</p></div></div>`;
    grid.appendChild(note);
  };
  if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',render,{once:true});else render();
})();

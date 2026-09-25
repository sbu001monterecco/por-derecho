(()=>{
  const d=document;
  const path=location.pathname.replace(/\/+$/,'/');
  const es=/\/es\//.test(path);
  const isRegister=/\/en\/actors-parties-lawyers-representatives\/$/.test(path)||/\/es\/actores-partes-abogados-representantes\/$/.test(path);
  if(!isRegister)return;
  const copy=es?{
    k:'CORRECCIÓN HISTÓRICA BLOQUEADA · FUENTES PRIMARIAS 2011–2014',
    t:'Antonio y Shaila estaban dentro del perímetro Sun Park / Comunidad antes de 2016.',
    intro:'Las fechas anteriores de 2017/2018 eran demasiado tardías. El registro canónico distingue una fecha mínima probada de una supuesta “entrada”.',
    cards:[
      ['ASUNCIÓN AIZPURÚA SÁNCHEZ · AAS','Presidenta de la Comunidad desde, como mínimo, el 2 feb 2011.','LOCKED_CANONICAL / LOCKED_MINIMUM_DATE'],
      ['FRANCISCO MARIO MATOS MATAS · FMMM','Administrador de la Comunidad documentado el 22 jun 2011.','LOCKED_MINIMUM_DATE'],
      ['SHAILA MARÍA COGOLLUDO RAMOS','Firma una comunicación de Pamanil a los comuneros, por órdenes de la presidenta Asunción, el 8 abr 2014.','LOCKED_MINIMUM_DATE'],
      ['ANTONIO COGOLLUDO ROJAS','Representa a Cristina Molina Petit en la Junta del 10 abr 2014 y aparece en el perímetro Pamanil/FMMM.','LOCKED_MINIMUM_DATE']
    ],
    b:'Una fecha mínima prueba que la implicación existía no más tarde de ese día. Una fuente más antigua puede moverla antes; ningún resumen posterior puede moverla hacia adelante.'
  }:{
    k:'LOCKED HISTORICAL CORRECTION · PRIMARY SOURCES 2011–2014',
    t:'Antonio and Shaila were inside the Sun Park / Community perimeter before 2016.',
    intro:'The former 2017/2018 labels were too late. The canonical register separates a proved minimum date from a claimed “entry” date.',
    cards:[
      ['ASUNCIÓN AIZPURÚA SÁNCHEZ · AAS','Community President by, at the latest, 2 Feb 2011.','LOCKED_CANONICAL / LOCKED_MINIMUM_DATE'],
      ['FRANCISCO MARIO MATOS MATAS · FMMM','Documented as Community Administrator on 22 Jun 2011.','LOCKED_MINIMUM_DATE'],
      ['SHAILA MARÍA COGOLLUDO RAMOS','Signed a Pamanil communication to Community owners, on President Asunción’s instructions, on 8 Apr 2014.','LOCKED_MINIMUM_DATE'],
      ['ANTONIO COGOLLUDO ROJAS','Represented Cristina Molina Petit at the 10 Apr 2014 meeting and appears in the Pamanil/FMMM perimeter.','LOCKED_MINIMUM_DATE']
    ],
    b:'A minimum date proves involvement no later than that day. An older source may move it earlier; a later summary may not move it forward.'
  };
  const style=d.createElement('style');
  style.dataset.pdCanonicalHistoryLock='20260819a';
  style.textContent=`
    .pd-canonical-lock{margin:1rem auto 2rem;width:min(calc(100% - 2rem),1180px);border:3px solid #9d0000;border-radius:16px;background:#fff8f5;box-shadow:0 8px 24px rgba(80,0,0,.12);overflow:hidden}
    .pd-canonical-lock__head{padding:1rem 1.1rem;background:#9d0000;color:#fff}.pd-canonical-lock__k{font-size:.74rem;font-weight:950;letter-spacing:.08em;text-transform:uppercase;color:#ffd4cf}.pd-canonical-lock h2{margin:.35rem 0 .3rem;font-size:clamp(1.35rem,2.7vw,2.2rem);line-height:1.05}.pd-canonical-lock__intro{margin:.25rem 0 0}
    .pd-canonical-lock__grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem;padding:1rem}.pd-canonical-lock__grid article{padding:.85rem;border:1px solid #decac4;border-top:6px solid #9d0000;border-radius:11px;background:#fff}.pd-canonical-lock__grid strong{display:block;line-height:1.2}.pd-canonical-lock__grid span{display:block;margin:.45rem 0;font-size:.84rem;line-height:1.4}.pd-canonical-lock__grid small{font-weight:900;color:#8d1d18}.pd-canonical-lock__boundary{margin:0;padding:.8rem 1rem;background:#fff1d6;border-top:1px solid #e7d0aa;font-size:.86rem;font-weight:800;line-height:1.4}
    @media(max-width:900px){.pd-canonical-lock__grid{grid-template-columns:1fr 1fr}}@media(max-width:620px){.pd-canonical-lock{width:min(calc(100% - 1rem),1180px)}.pd-canonical-lock__grid{grid-template-columns:1fr;padding:.75rem}.pd-canonical-lock__head{padding:.85rem}}
  `;
  d.head.appendChild(style);
  const box=d.createElement('section');
  box.className='pd-canonical-lock';
  box.dataset.pdCanonicalHistoryLock='true';
  box.innerHTML=`<div class="pd-canonical-lock__head"><div class="pd-canonical-lock__k">${copy.k}</div><h2>${copy.t}</h2><p class="pd-canonical-lock__intro">${copy.intro}</p></div><div class="pd-canonical-lock__grid">${copy.cards.map(x=>`<article><strong>${x[0]}</strong><span>${x[1]}</span><small>${x[2]}</small></article>`).join('')}</div><p class="pd-canonical-lock__boundary">${copy.b}</p>`;
  const hero=d.querySelector('main .hero');
  if(hero)hero.insertAdjacentElement('afterend',box);else (d.querySelector('main')||d.body).prepend(box);
})();
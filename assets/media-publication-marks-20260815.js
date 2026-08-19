(() => {
  const path = window.location.pathname;
  const isEs = path.includes('/es/');
  const isHomeEs = /\/por-derecho\/es\/?$/.test(path);
  const isHomeEn = /\/por-derecho\/en\/?$/.test(path);
  const isWho = path.includes('/es/quien-debe-responder-que/') || path.includes('/en/who-should-answer-what/');
  const mediaPath = ['/canarias7-','/eleconomista-','/hosteltur-sun-park-mynd-yaiza/','/la-voz-lanzarote-sun-park-mynd-yaiza/','/medios-trazabilidad-relato-publico/','/media-public-narrative-traceability/'].some(p=>path.includes(p));
  if (!(isHomeEs || isHomeEn || isWho || mediaPath)) return;

  const css=document.createElement('style');css.textContent=`
  .media-marks-wrap{margin:1.4rem 0}.media-marks-kicker{font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;font-weight:800;opacity:.72;margin:0 0 .65rem}.media-marks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem;max-width:920px}.media-mark{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.95rem 1.1rem;border:1px solid rgba(19,37,45,.18);border-radius:14px;background:#fff;text-decoration:none;color:inherit;box-shadow:0 7px 22px rgba(19,37,45,.06)}.media-mark:hover{transform:translateY(-1px);box-shadow:0 10px 26px rgba(19,37,45,.1)}.media-mark-name{font-size:1.08rem;font-weight:900}.media-mark-name.eco,.media-mark-name.voz{font-family:Georgia,'Times New Roman',serif}.media-mark small{display:block;margin-top:.28rem;font-size:.75rem;opacity:.68;font-weight:600}.media-marks-note{font-size:.82rem;line-height:1.45;opacity:.72;max-width:920px;margin:.65rem 0 0}.media-switcher{padding:1rem 0;background:#f4f1ea;border-top:1px solid rgba(19,37,45,.08);border-bottom:1px solid rgba(19,37,45,.08)}
  .media-home-gateway{padding:1.25rem 0;background:#13252d;color:#fff}.media-home-gateway .media-home-inner{display:flex;align-items:center;justify-content:space-between;gap:1.5rem}.media-home-gateway h2{margin:.1rem 0 .35rem;font-size:1.4rem}.media-home-gateway p{margin:0;max-width:780px;opacity:.88}.media-home-gateway a{display:inline-block;white-space:nowrap;border:1px solid rgba(255,255,255,.42);border-radius:999px;padding:.72rem 1rem;color:#fff;text-decoration:none;font-weight:800}
  @media(max-width:700px){.media-marks{grid-template-columns:1fr}.media-home-gateway .media-home-inner{display:block}.media-home-gateway a{margin-top:.9rem}}`;
  document.head.appendChild(css);

  const r=isEs?{
    c7:'../canarias7-articulo-30mayo2022/',eco:'../eleconomista-javier-romera-enero2025/',host:'../hosteltur-sun-park-mynd-yaiza/',voz:'../la-voz-lanzarote-sun-park-mynd-yaiza/',hub:'../medios-trazabilidad-relato-publico/',title:'Medios · trazabilidad editorial',subs:['30/05/2022 · publicación/despublicación','Enero 2025 · verificación/no publicación','Sun Park / MYND Yaiza · alcance de la transformación','2022–23 · fuente, atribución y perímetro'],note:'Identificación editorial; no implica aval, afiliación ni condición de autoridad pública.',homeTitle:'Medios y relato público',homeText:'Qué se publicó sobre Acosta Matos, RICPE, Canarian Hospitality y MYND; qué fuente sustentó cada afirmación y qué merece hoy aclaración, actualización o rectificación.',homeCta:'Ver mapa de medios →'
  }:{
    c7:'../canarias7-article-30may2022/',eco:'../eleconomista-javier-romera-january2025/',host:'../hosteltur-sun-park-mynd-yaiza/',voz:'../la-voz-lanzarote-sun-park-mynd-yaiza/',hub:'../media-public-narrative-traceability/',title:'Media · editorial traceability',subs:['30 May 2022 · publication/unpublishing','January 2025 · verification/non-publication','Sun Park / MYND Yaiza · meaning of transformation','2022–23 · source, attribution and perimeter'],note:'Editorial identification only; no endorsement, affiliation or public-authority status is implied.',homeTitle:'Media and the public narrative',homeText:'What was published about Acosta Matos, RICPE, Canarian Hospitality and MYND; which source supported each proposition and what now merits clarification, updating or correction.',homeCta:'Open media map →'
  };

  if(isHomeEs || isHomeEn){
    if(document.querySelector('[data-media-home-gateway]'))return;
    const section=document.createElement('section');section.className='media-home-gateway';section.dataset.mediaHomeGateway='true';section.innerHTML=`<div class="shell media-home-inner"><div><p class="media-marks-kicker">${r.title}</p><h2>${r.homeTitle}</h2><p>${r.homeText}</p></div><a href="${r.hub}">${r.homeCta}</a></div>`;
    const priority=document.querySelector('.priority-band');const hero=document.querySelector('main .hero');(priority||hero)?.insertAdjacentElement('afterend',section);return;
  }

  const wrap=document.createElement('div');wrap.className='media-marks-wrap';const items=[[r.c7,'CANARIAS7','',r.subs[0]],[r.eco,'elEconomista','eco',r.subs[1]],[r.host,'HOSTELTUR','',r.subs[2]],[r.voz,'La Voz de Lanzarote','voz',r.subs[3]]];wrap.innerHTML=`<p class="media-marks-kicker">${r.title}</p><div class="media-marks">${items.map(x=>`<a class="media-mark" href="${x[0]}"><span><span class="media-mark-name ${x[2]}">${x[1]}</span><small>${x[3]}</small></span><span>→</span></a>`).join('')}</div><p class="media-marks-note">${r.note} <a href="${r.hub}">${isEs?'Mapa completo':'Full map'} →</a></p>`;
  const hero=document.querySelector('main .hero,main .mhero');if(!hero)return;const section=document.createElement('section');section.className=isWho?'section alt':'media-switcher';const shell=document.createElement('div');shell.className='shell';shell.appendChild(wrap);section.appendChild(shell);hero.insertAdjacentElement('afterend',section);
})();

// Global adjudication-provenance loader. This file is already loaded independently on every page
// through assets/site.js; keep the documentary correction and reciprocal route layer outside the
// media-specific route gate above.
(() => {
  const current = document.currentScript;
  if (!current || document.querySelector('script[data-adjudicacion-provenance-loader]')) return;
  const script = document.createElement('script');
  script.src = new URL('adjudicacion-provenance-cross-site-20260819.js?v=20260819a', current.src).href;
  script.async = false;
  script.dataset.adjudicacionProvenanceLoader = 'true';
  document.head.appendChild(script);
})();

(()=>{
  const d=document;
  const path=location.pathname.replace(/\/+$/,'/');
  const es=/\/es\//.test(path);
  const exact=[
    '/en/','/es/',
    '/en/ric-private-equity-sun-park/','/es/ric-private-equity-sun-park/',
    '/en/rsm/nnr4-1025c2f66/','/es/rsm/nnr4-1025c2f66/',
    '/en/insolvency-36-2012-insolvency-administrator/','/es/concurso-36-2012-administrador-concursal/',
    '/en/san-telmo-ricpe-sun-park/','/es/san-telmo-ricpe-sun-park/',
    '/en/pwc-canarias-carlos-saavedra-sun-park/','/es/pwc-canarias-carlos-saavedra-sun-park/',
    '/en/sun-park-takeover-7-june-2018/','/es/toma-control-sun-park-7-junio-2018/',
    '/en/actors-parties-lawyers-representatives/','/es/actores-partes-abogados-representantes/',
    '/en/community-instrumentalisation/','/es/comunidad-instrumentalizacion/'
  ].map(x=>'/por-derecho'+x);
  const fragments=[
    'same-hotel-multiple-financial-lives','mismo-hotel-multiples-vidas-financieras',
    'insolvency-classification-parallel-lives','calificacion-concurso-36-2012-vidas-paralelas',
    'ricpe-documentary-accountability','ricpe-responsabilidad-documental',
    'reverse-engineering-360-sun-park-chain','ingenieria-inversa-360-cadena-sun-park',
    'acosta-matos-perimeter','acosta-matos-perimetro','who-should-answer-what','quien-debe-responder-que',
    'insolvency-administrator-loyalty-breakpoint','administrador-concursal-punto-quiebre-lealtad',
    'insolvency-36-2012-institutional-accountability','concurso-36-2012-responsabilidad-institucional',
    'cnmv-ricpe-verification','cnmv-ricpe-verificacion','grant-thornton/'
  ];
  if(!exact.includes(path)&&!fragments.some(x=>path.includes('/'+x)))return;
  const edu='https://res.cloudinary.com/rsmglobal/image/fetch/t_default/f_auto/q_auto/https%3A/www.rsm.global/spain/sites/default/files/media/01%20Global%20assets/02_Thumbnails%201240x930px/06_fotos%20profesionales/Eduardo%20S%C3%A1nchez%20%281%29.jpg';
  const eduFallback='https://abogadossantelmo.com/wp-content/uploads/2022/07/Eduardo-Sanchez-Iglesias-500x500.jpg';
  const sun='/por-derecho/assets/sun-park-mynd-yaiza.jpg?v=20260819a';
  const borja='/por-derecho/assets/actors/francisco-de-borja-rodriguez-batllori.jpg?v=20260819a';
  const source='https://www.youtube.com/watch?v=mHn9IJU0qI4&t=488s';
  const t=es?{
    lead:'El socio de San Telmo Eduardo Sánchez manifestó que «el despacho» introdujo clientes en la inversión RICPE conectada con Sun Park.',
    lead2:'San Telmo partner Eduardo Sánchez stated that “el despacho” put clients into the RICPE investment connected to Sun Park.',
    banner:'UN MISMO HOTEL. UN MISMO PERÍMETRO PROFESIONAL SAN TELMO. DOS VIDAS PROFESIONALES EN PARALELO.',
    banner2:'ONE HOTEL. ONE SAN TELMO PROFESSIONAL PERIMETER. TWO PARALLEL PROFESSIONAL LIVES.',
    partner:'SOCIO DE SAN TELMO',same:'EL MISMO HOTEL',ac:'ADMINISTRADOR CONCURSAL',investment:'INVERSIÓN RICPE',sameAsset:'MISMO ACTIVO',
    source:'FUENTE: «Enrique Guerra, en #UnCaféenSanTelmo» · San Telmo Abogados y Economistas · 30 nov 2021 · la manifestación empieza en 08:08 y se completa en 08:12 · contexto 07:57–08:27 · transcripción pp. 29–30 de 85.',
    watch:'Ver la fuente desde 08:08 →',
    q:'¿QUÉ CONTROLES DE CONFLICTO, SEPARACIÓN DE EXPEDIENTES, KYC, ACCESO E INFORMACIÓN EXISTÍAN — Y DÓNDE ESTÁN LOS REGISTROS?',
    q2:'What conflict, file-separation, KYC, access and information controls existed — and where are the records?',
    boundary:'Manifestación directa controlada por fuentes. Acredita la conexión contemporánea San Telmo–RICPE–Sun Park. No acredita por sí sola coordinación Borja–Eduardo, transmisión de información concursal, ilicitud ni responsabilidad.'
  }:{
    lead:'San Telmo partner Eduardo Sánchez stated that “el despacho” put clients into the RICPE investment connected to Sun Park.',
    lead2:'El socio de San Telmo Eduardo Sánchez manifestó que «el despacho» introdujo clientes en la inversión RICPE conectada con Sun Park.',
    banner:'ONE HOTEL. ONE SAN TELMO PROFESSIONAL PERIMETER. TWO PARALLEL PROFESSIONAL LIVES.',
    banner2:'UN MISMO HOTEL. UN MISMO PERÍMETRO PROFESIONAL SAN TELMO. DOS VIDAS PROFESIONALES EN PARALELO.',
    partner:'SAN TELMO PARTNER',same:'THE SAME HOTEL',ac:'INSOLVENCY ADMINISTRATOR',investment:'RICPE INVESTMENT',sameAsset:'SAME ASSET',
    source:'SOURCE: “Enrique Guerra, en #UnCaféenSanTelmo” · San Telmo Abogados y Economistas · 30 Nov 2021 · statement begins at 08:08 and completes at 08:12 · context 07:57–08:27 · transcript pp. 29–30 of 85.',
    watch:'Watch the source from 08:08 →',
    q:'WHAT CONFLICT, FILE-SEPARATION, KYC, ACCESS AND INFORMATION CONTROLS EXISTED — AND WHERE ARE THE RECORDS?',
    q2:'¿Qué controles de conflicto, separación de expedientes, KYC, acceso e información existían — y dónde están los registros?',
    boundary:'Source-controlled direct statement. It establishes the contemporaneous San Telmo–RICPE–Sun Park connection. It does not by itself establish Borja–Eduardo coordination, transfer of insolvency information, unlawfulness or liability.'
  };
  const style=()=>{
    if(d.querySelector('style[data-pd-st-source]'))return;
    const s=d.createElement('style');s.dataset.pdStSource='20260819a';s.textContent=`
      .pd-st-source{width:min(calc(100% - 2rem),1180px);margin:1rem auto 2rem;border:4px solid #920e12;border-radius:18px;overflow:hidden;background:#f6f0e4;color:#111820;box-shadow:0 12px 34px rgba(72,0,0,.17);scroll-margin-top:5.5rem}.pd-st-source *{box-sizing:border-box}.pd-st-source__head{padding:1rem 1.2rem;background:#10161b;text-align:center}.pd-st-source__head strong{display:block;color:#fff;font-size:clamp(1.35rem,3vw,2.55rem);line-height:1.08}.pd-st-source__head span{display:block;margin-top:.38rem;color:#e0af4e;font-size:clamp(.9rem,1.9vw,1.3rem);font-weight:950;line-height:1.18}.pd-st-source__banner{padding:.64rem 1rem;background:#850b0e;color:#fff;text-align:center;font-size:clamp(.9rem,1.8vw,1.22rem);font-weight:1000;line-height:1.25}.pd-st-source__banner small{display:block;margin-top:.18rem;color:#e5b452;font-size:.78em}.pd-st-source__grid{display:grid;grid-template-columns:minmax(0,1fr) 90px minmax(0,1.45fr) 112px minmax(0,1fr);gap:.55rem;align-items:center;padding:1rem}.pd-st-source__card{min-width:0;border:2px solid #111820;border-radius:10px;background:#fff;overflow:hidden;box-shadow:0 3px 0 rgba(0,0,0,.15)}.pd-st-source__cardHead{min-height:4.9rem;display:flex;flex-direction:column;justify-content:center;padding:.5rem;background:#111820;text-align:center}.pd-st-source__cardHead strong{color:#fff;font-size:clamp(.8rem,1.55vw,1.05rem);line-height:1.04}.pd-st-source__cardHead span{margin-top:.25rem;color:#e0af4e;font-size:.67rem;font-weight:950;line-height:1.15}.pd-st-source__photo{display:block;width:100%;height:255px;object-fit:cover;border-top:3px solid #d6a641;background:#e8ebed}.pd-st-source__borja .pd-st-source__photo{object-fit:contain;padding:.35rem;background:#f3f3f3}.pd-st-source__arrow{min-height:5rem;display:grid;place-items:center;padding:.4rem .15rem;background:#b51218;color:#fff;text-align:center;font-size:.69rem;font-weight:1000;line-height:1.15;clip-path:polygon(0 20%,72% 20%,72% 0,100% 50%,72% 100%,72% 80%,0 80%)}.pd-st-source__bridge{position:relative;min-height:6rem;display:grid;place-items:center;text-align:center;font-size:.68rem;font-weight:1000}.pd-st-source__bridge:before{content:'';position:absolute;left:0;right:16px;top:50%;border-top:5px dotted #111820}.pd-st-source__bridge:after{content:'';position:absolute;right:0;top:calc(50% - 10px);border-left:18px solid #111820;border-top:10px solid transparent;border-bottom:10px solid transparent}.pd-st-source__bridge span{position:relative;z-index:1;padding:.35rem .43rem;border:1px solid #d2a341;border-radius:7px;background:#ffe9b5}.pd-st-source__quote{margin:0 4.5%;padding:.8rem 1rem;border:3px solid #a40000;border-radius:12px;background:#fff;text-align:center}.pd-st-source__quote strong{display:block;color:#9e1115;font-size:clamp(1.35rem,3.1vw,2.45rem);line-height:1}.pd-st-source__quote span{display:block;margin-top:.35rem;font-size:clamp(.78rem,1.55vw,1.06rem);font-weight:950;line-height:1.25}.pd-st-source__time{display:inline-flex!important;margin:.55rem auto 0!important;padding:.32rem .58rem;border-radius:999px;background:#111820;color:#fff;font-size:.72rem!important;letter-spacing:.05em}.pd-st-source__source{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:.8rem;align-items:center;margin:.8rem 3.5% 0;padding:.72rem .85rem;border:1px solid #d3a23c;border-radius:10px;background:#ffe7ac}.pd-st-source__source strong{font-size:.82rem;line-height:1.38}.pd-st-source__source a{display:inline-flex;padding:.52rem .68rem;border-radius:8px;background:#8f0000;color:#fff;text-decoration:none;font-size:.72rem;font-weight:950;white-space:nowrap}.pd-st-source__question{margin-top:.8rem;padding:.72rem 1rem;background:#111820;color:#fff;text-align:center;font-size:clamp(.82rem,1.65vw,1.04rem);font-weight:950;line-height:1.35}.pd-st-source__question span{display:block;margin-top:.22rem;color:#e0af4e}.pd-st-source__boundary{margin:0;padding:.68rem 1rem;background:#d9a941;color:#17120a;text-align:center;font-size:.76rem;font-weight:800;line-height:1.38}@media(max-width:900px){.pd-st-source__grid{grid-template-columns:1fr}.pd-st-source__arrow{min-height:3.5rem;clip-path:polygon(20% 0,80% 0,80% 35%,100% 35%,50% 100%,0 35%,20% 35%)}.pd-st-source__bridge{min-height:3.7rem}.pd-st-source__bridge:before{left:50%;right:auto;top:0;bottom:13px;border-top:0;border-left:5px dotted #111820}.pd-st-source__bridge:after{right:calc(50% - 9px);top:auto;bottom:0;border-left:10px solid transparent;border-right:10px solid transparent;border-top:18px solid #111820;border-bottom:0}.pd-st-source__photo{height:auto;max-height:360px}.pd-st-source__source{grid-template-columns:1fr}.pd-st-source__source a{width:fit-content}}@media(max-width:620px){.pd-st-source{width:min(calc(100% - 1rem),1180px);border-width:3px}.pd-st-source__head,.pd-st-source__grid{padding:.75rem}.pd-st-source__quote{margin:0 .7rem;padding:.68rem}.pd-st-source__source{margin:.7rem .7rem 0;padding:.65rem}.pd-st-source__source a{width:100%;justify-content:center}.pd-st-source__question,.pd-st-source__boundary{padding:.62rem .72rem}}
    `;d.head.appendChild(s);
  };
  const html=()=>`<header class="pd-st-source__head"><strong>${t.lead}</strong><span>${t.lead2}</span></header><div class="pd-st-source__banner">${t.banner}<small>${t.banner2}</small></div><div class="pd-st-source__grid"><article class="pd-st-source__card"><div class="pd-st-source__cardHead"><strong>EDUARDO SÁNCHEZ</strong><span>${t.partner}</span></div><img class="pd-st-source__photo" data-eduardo data-visual-asset-id="person.eduardo-sanchez-san-telmo.primary" src="${edu}" width="512" height="512" referrerpolicy="no-referrer" loading="eager" decoding="async" alt="Eduardo Sánchez"></article><div class="pd-st-source__arrow">${t.investment}</div><article class="pd-st-source__card"><div class="pd-st-source__cardHead"><strong>SUN PARK / MYND YAIZA</strong><span>${t.same}</span></div><img class="pd-st-source__photo" data-visual-asset-id="place.sun-park-mynd-yaiza.aerial-primary" src="${sun}" width="1400" height="1048" loading="eager" decoding="async" alt="Sun Park / MYND Yaiza"></article><div class="pd-st-source__bridge"><span>CONCURSO 36/2012<br>${t.sameAsset}</span></div><article class="pd-st-source__card pd-st-source__borja"><div class="pd-st-source__cardHead"><strong>FRANCISCO DE BORJA<br>RODRÍGUEZ-BATLLORI LAFFITTE</strong><span>${t.ac}</span></div><img class="pd-st-source__photo" data-visual-asset-id="person.francisco-de-borja-rodriguez-batllori.primary" src="${borja}" width="135" height="151" loading="eager" decoding="async" alt="Francisco de Borja Rodríguez-Batllori Laffitte"></article></div><div class="pd-st-source__quote"><strong>“EL DESPACHO” / “THE FIRM”</strong><span>“bueno, nosotros en el despacho… en esa primera inversión… metimos unos cuantos clientes”</span><span class="pd-st-source__time">08:08 → 08:12 · CONTEXT / CONTEXTO 07:57–08:27</span></div><div class="pd-st-source__source"><strong>${t.source}</strong><a href="${source}" target="_blank" rel="noopener">${t.watch}</a></div><div class="pd-st-source__question">${t.q}<span>${t.q2}</span></div><p class="pd-st-source__boundary">${t.boundary}</p>`;
  const mount=()=>{
    if(d.querySelector('section[data-pd-st-source="true"]'))return;
    style();
    const box=d.createElement('section');box.className='pd-st-source';box.dataset.pdStSource='true';box.dataset.visualAssetId='composite.san-telmo-ricpe-sun-park-stamp-v1';box.innerHTML=html();
    const old=d.querySelector('section[data-pd-parallel-lives="true"]');
    if(old)old.insertAdjacentElement('beforebegin',box);
    else{const five=d.querySelector('section[data-pd-five-ac]');const hero=d.querySelector('.dossier-hero,.hero,main>section:first-child');const target=five||hero;if(target)target.insertAdjacentElement('afterend',box);else(d.querySelector('main')||d.body).prepend(box)}
    const e=box.querySelector('[data-eduardo]');if(e)e.addEventListener('error',()=>{if(e.src!==eduFallback)e.src=eduFallback;else{e.alt=es?'Retrato no disponible; identidad y fuente registradas.':'Portrait unavailable; identity and source registered.';e.style.objectFit='contain'}},{once:false});
  };
  if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',()=>setTimeout(mount,80),{once:true});else setTimeout(mount,80);
})();
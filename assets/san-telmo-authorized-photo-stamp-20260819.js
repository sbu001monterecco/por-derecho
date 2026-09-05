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

  const copy=es?{
    alt:'Colisión documental San Telmo, RIC Private Equity y Sun Park: Eduardo Sánchez, el mismo hotel Sun Park y Francisco de Borja Rodríguez-Batllori Laffitte, Administrador Concursal. La manifestación controlada por fuentes atribuye a Eduardo Sánchez que el despacho introdujo clientes en la inversión RICPE conectada con Sun Park; no acredita por sí sola coordinación, transmisión de información, ilicitud ni responsabilidad.',
    caption:'Imágenes autorizadas y bloqueadas por activo: Eduardo Sánchez → Sun Park, el mismo hotel → Francisco de Borja Rodríguez-Batllori Laffitte, Administrador Concursal. Manifestación directa controlada por fuentes; derecho de respuesta y corrección con prominencia equivalente.'
  }:{
    alt:'San Telmo, RIC Private Equity and Sun Park documentary collision: Eduardo Sánchez, the same Sun Park hotel and Francisco de Borja Rodríguez-Batllori Laffitte, Insolvency Administrator. The source-controlled statement attributes to Eduardo Sánchez that the firm put clients into the RICPE investment connected to Sun Park; it does not by itself prove coordination, information transfer, unlawfulness or liability.',
    caption:'Authorized, asset-locked images: Eduardo Sánchez → Sun Park, the same hotel → Francisco de Borja Rodríguez-Batllori Laffitte, Insolvency Administrator. Source-controlled direct statement; equivalent-prominence right of reply and correction.'
  };

  const addStyle=()=>{
    if(d.querySelector('style[data-pd-santelmo-photo-stamp]'))return;
    const style=d.createElement('style');
    style.dataset.pdSantelmoPhotoStamp='20260819a';
    style.textContent=`
      .pd-santelmo-photo-stamp{width:min(calc(100% - 2rem),1180px);margin:1.25rem auto 1.6rem;padding:.55rem;border:3px solid #8f0f12;border-radius:16px;background:#0c1116;box-shadow:0 1rem 2.8rem rgba(49,11,12,.20);scroll-margin-top:6rem}
      .pd-santelmo-photo-stamp img{display:block;width:100%;height:auto;border-radius:10px;background:#fffdf8}
      .pd-santelmo-photo-stamp figcaption{padding:.65rem .75rem .35rem;color:#ead7b2;font-size:.72rem;line-height:1.4;text-align:center}
      @media(max-width:760px){.pd-santelmo-photo-stamp{width:min(calc(100% - 1rem),1180px);margin:.8rem auto 1.1rem;padding:.35rem;border-width:2px;border-radius:11px}.pd-santelmo-photo-stamp img{border-radius:7px}.pd-santelmo-photo-stamp figcaption{font-size:.66rem;text-align:left}}
    `;
    d.head.appendChild(style);
  };

  const mount=()=>{
    if(d.querySelector('[data-pd-santelmo-photo-stamp]'))return true;
    const parallel=d.querySelector('.pd-parallel');
    const hero=d.querySelector('.dossier-hero, main > .hero, .hero');
    const anchor=parallel||hero;
    if(!anchor)return false;
    addStyle();
    const figure=d.createElement('figure');
    figure.className='pd-santelmo-photo-stamp';
    figure.dataset.pdSantelmoPhotoStamp='20260819a';
    figure.dataset.visualAssetId='composite.san-telmo-ricpe-sun-park-stamp-v1';
    const img=d.createElement('img');
    img.src='/por-derecho/assets/composites/san-telmo-ricpe-sun-park-stamp-v1.svg?v=20260819a';
    img.alt=copy.alt;
    img.loading=isSanTelmo?'eager':'lazy';
    img.decoding='async';
    img.dataset.visualAssetId='composite.san-telmo-ricpe-sun-park-stamp-v1';
    const cap=d.createElement('figcaption');
    cap.textContent=copy.caption;
    figure.append(img,cap);
    if(parallel)parallel.insertAdjacentElement('beforebegin',figure);else hero.insertAdjacentElement('afterend',figure);
    return true;
  };

  const render=()=>{
    if(mount())return;
    let n=0;
    const timer=setInterval(()=>{n+=1;if(mount()||n>20)clearInterval(timer)},150);
  };
  if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',render,{once:true});else render();
})();

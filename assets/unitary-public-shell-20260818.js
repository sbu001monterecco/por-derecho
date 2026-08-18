(()=>{
  'use strict';
  const d=document;
  const VERSION='20260818a';
  if(window.PorDerechoUnitaryShell?.version===VERSION){window.PorDerechoUnitaryShell.init?.();return;}
  const script=d.currentScript;
  const assetBase=script?new URL('.',script.src):new URL('/por-derecho/assets/',location.origin);
  const projectRoot=new URL('../',assetBase);
  const lang=(d.documentElement.lang||location.pathname.includes('/es/')?'es':'en').toLowerCase().startsWith('es')?'es':'en';
  const isEs=lang==='es';
  const strings=isEs?{
    case:'Caso',search:'Buscar',caseLong:'Sala de control',searchLong:'Buscar en el sitio',evidence:'Prueba',institutions:'Instituciones',proceedings:'Procedimientos',updates:'Actualizaciones',about:'Por Derecho',openControl:'Abrir sala de control',gateway:'Una sola puerta para leer el caso como sistema: hechos, prueba, preguntas abiertas, responsables de respuesta y qué podría cambiar la interpretación.',count:n=>`${n} resultado${n===1?'':'s'}`,empty:'No hay coincidencias en el índice controlado. Pruebe un nombre, fecha, procedimiento, finca o importe.',all:'Todo',caseType:'Caso',evidenceType:'Prueba',institutionType:'Institución',proceedingType:'Procedimiento',financeType:'Financiación',routeType:'Ruta',indexed:'Busca el índice canónico y todas las rutas del sitemap. Los alias controlados mejoran la localización de personas, procedimientos, cifras y conceptos.'
  }:{
    case:'Case',search:'Search',caseLong:'Case control room',searchLong:'Search the site',evidence:'Evidence',institutions:'Institutions',proceedings:'Proceedings',updates:'Updates',about:'Por Derecho',openControl:'Open case control room',gateway:'One door into the case as a system: facts, evidence, open questions, answer-holders and what could change the interpretation.',count:n=>`${n} result${n===1?'':'s'}`,empty:'No match in the controlled index. Try a name, date, proceeding, property number or amount.',all:'All',caseType:'Case',evidenceType:'Evidence',institutionType:'Institution',proceedingType:'Proceeding',financeType:'Finance',routeType:'Route',indexed:'Searches the canonical index and every sitemap route. Controlled aliases improve discovery of people, proceedings, amounts and concepts.'
  };
  const urls={
    control:new URL(isEs?'es/sala-control-caso/':'en/case-control-room/',projectRoot).href,
    search:new URL(isEs?'es/buscar/':'en/search/',projectRoot).href,
    home:new URL(`${lang}/`,projectRoot).href,
    proceedings:new URL(isEs?'es/cuaderno-juridico/':'en/legal-notebook/',projectRoot).href,
    updates:new URL(isEs?'es/actualizaciones/':'en/updates/',projectRoot).href,
    about:new URL(isEs?'es/':'en/about/',projectRoot).href,
    other:new URL(isEs?'en/':'es/',projectRoot).href
  };
  const isHome=()=>new URL(location.href).pathname.replace(/\/+$/,'/')===new URL(urls.home).pathname;
  const isControl=()=>/\/(case-control-room|sala-control-caso)\/?$/i.test(location.pathname);
  const isSearch=()=>/\/(search|buscar)\/?$/i.test(location.pathname);
  const excludedUtility=()=>/\/(aviso-legal|aviso-legal-privacidad|privacy|privacidad|contacto|contact|faq)\/?$/i.test(location.pathname);
  const ensureCss=()=>{
    if(d.querySelector('link[data-psr-unitary-shell-css]'))return;
    const link=d.createElement('link');link.rel='stylesheet';link.href=new URL('unitary-public-shell-20260818.css?v=20260818a',assetBase).href;link.dataset.psrUnitaryShellCss='true';d.head.appendChild(link);
  };
  const addUtility=()=>{
    if(excludedUtility()||isControl()||isSearch()||d.querySelector('.psr-utility-nav'))return;
    const nav=d.createElement('nav');nav.className='psr-utility-nav';nav.setAttribute('aria-label',isEs?'Accesos globales':'Global shortcuts');
    nav.innerHTML=`<a href="${urls.control}" title="${strings.caseLong}">${strings.case}<span> · ${isEs?'control':'control'}</span></a><a href="${urls.search}" title="${strings.searchLong}">${strings.search}<span> · /</span></a>`;
    d.body.appendChild(nav);
  };
  const simplifyHomeNav=()=>{
    if(!isHome())return;
    const nav=d.querySelector('#main-nav.main-nav,.main-nav#main-nav');if(!nav||nav.dataset.psrConsolidatedNav==='true')return;
    const evidence='#record',institutions='#institutional-map';
    nav.dataset.psrConsolidatedNav='true';
    nav.innerHTML=`<a class="psr-nav-primary" href="${urls.control}">${strings.case}</a><a class="psr-nav-evidence" href="${evidence}">${strings.evidence}</a><a class="psr-nav-institutions" href="${institutions}">${strings.institutions}</a><a href="${urls.proceedings}">${strings.proceedings}</a><a href="${urls.updates}">${strings.updates}</a><a href="${urls.about}">${strings.about}</a><a class="psr-nav-search" href="${urls.search}">${strings.search}</a><a class="language-link" href="${urls.other}" hreflang="${isEs?'en':'es'}">${isEs?'EN':'ES'}</a>`;
    if(!d.querySelector('.psr-home-control-gateway')){
      const gateway=d.createElement('aside');gateway.className='psr-home-control-gateway';gateway.setAttribute('aria-label',strings.caseLong);
      gateway.innerHTML=`<div class="shell psr-gateway-inner"><p><strong>${strings.caseLong}.</strong> ${strings.gateway}</p><a href="${urls.control}">${strings.openControl} →</a></div>`;
      const priority=d.querySelector('.priority-band');const hero=d.querySelector('main .hero');(priority||hero)?.insertAdjacentElement('afterend',gateway);
    }
  };
  const normalize=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9€]+/g,' ').trim();
  const escapeHtml=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const humanize=path=>{
    const bits=path.replace(/^\/+|\/+$/g,'').split('/');const slug=bits[bits.length-1]||bits[bits.length-2]||'';
    return slug.replace(/-/g,' ').replace(/\b\w/g,m=>m.toUpperCase());
  };
  const loadEntries=async()=>{
    let curated=[];
    try{const r=await fetch(new URL('data/unitary-route-registry-v1.json?v=20260818a',assetBase));if(r.ok)curated=await r.json();}catch{}
    const seen=new Set(curated.map(x=>x.path));
    try{
      const r=await fetch(new URL('../sitemap.xml?v=20260818a',assetBase));
      if(r.ok){const xml=new DOMParser().parseFromString(await r.text(),'application/xml');
        [...xml.querySelectorAll('loc')].forEach(loc=>{try{const u=new URL(loc.textContent.trim());const marker='/por-derecho/';const i=u.pathname.indexOf(marker);if(i<0)return;const path=u.pathname.slice(i+marker.length).replace(/^\/+|\/+$/g,'')+'/';if(!path.startsWith(`${lang}/`)||seen.has(path))return;seen.add(path);curated.push({lang,path,title:humanize(path),type:'route',summary:'',tags:[],aliases:[]});}catch{}});
      }
    }catch{}
    return curated.filter(x=>x.lang===lang);
  };
  const scoreEntry=(entry,q)=>{
    if(!q)return 1;
    const n=normalize(q);const tokens=n.split(/\s+/).filter(Boolean);if(!tokens.length)return 1;
    const title=normalize(entry.title),summary=normalize(entry.summary),path=normalize(entry.path),tags=normalize((entry.tags||[]).join(' ')),aliases=normalize((entry.aliases||[]).join(' '));
    let score=0;
    if(title===n)score+=180;if(title.includes(n))score+=90;if(aliases.includes(n))score+=85;if(tags.includes(n))score+=55;if(path.includes(n))score+=45;if(summary.includes(n))score+=30;
    tokens.forEach(t=>{if(title.includes(t))score+=24;if(aliases.includes(t))score+=22;if(tags.includes(t))score+=15;if(path.includes(t))score+=10;if(summary.includes(t))score+=8;});
    return score;
  };
  const initSearch=async()=>{
    const input=d.getElementById('psr-search-input'),results=d.getElementById('psr-search-results');if(!input||!results||input.dataset.ready==='true')return;
    input.dataset.ready='true';const count=d.getElementById('psr-search-count');const form=d.getElementById('psr-search-form');const filters=[...d.querySelectorAll('[data-search-filter]')];let active='all';
    const entries=await loadEntries();
    const render=()=>{
      const q=input.value.trim();let rows=entries.map(e=>({e,score:scoreEntry(e,q)})).filter(x=>x.score>0&&(active==='all'||x.e.type===active)).sort((a,b)=>b.score-a.score||a.e.title.localeCompare(b.e.title)).slice(0,80);
      if(count)count.textContent=strings.count(rows.length);
      if(!rows.length){results.innerHTML=`<div class="psr-search-empty">${strings.empty}</div>`;return;}
      results.innerHTML=rows.map(({e})=>{const href=new URL(e.path,projectRoot).href;const meta=[e.type,...(e.tags||[]).slice(0,3)].filter(Boolean).map(x=>`<span>${escapeHtml(x)}</span>`).join('');return `<article class="psr-search-result"><h2><a href="${href}">${escapeHtml(e.title)}</a></h2>${e.summary?`<p>${escapeHtml(e.summary)}</p>`:''}<div class="psr-search-meta">${meta}</div></article>`;}).join('');
    };
    filters.forEach(btn=>btn.addEventListener('click',()=>{active=btn.dataset.searchFilter||'all';filters.forEach(b=>b.setAttribute('aria-pressed',String(b===btn)));render();}));
    form?.addEventListener('submit',ev=>{ev.preventDefault();const u=new URL(location.href);if(input.value.trim())u.searchParams.set('q',input.value.trim());else u.searchParams.delete('q');history.replaceState(null,'',u);render();});
    input.addEventListener('input',render);
    const initial=new URL(location.href).searchParams.get('q')||'';input.value=initial;render();
    d.addEventListener('keydown',ev=>{if(ev.key==='/'&&!/input|textarea|select/i.test(d.activeElement?.tagName||'')){ev.preventDefault();input.focus();}});
  };
  const init=()=>{
    ensureCss();d.documentElement.dataset.psrUnitaryShellVersion=VERSION;simplifyHomeNav();addUtility();initSearch();
  };
  window.PorDerechoUnitaryShell={version:VERSION,init,urls,loadEntries};
  if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',init,{once:true});else init();
  window.setTimeout(init,1800);
})();

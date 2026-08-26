(()=>{
  'use strict';
  const d=document;
  const VERSION='20260826a';
  if(window.PorDerechoUnitaryShell?.version===VERSION){window.PorDerechoUnitaryShell.init?.();return;}
  const script=d.currentScript;
  const assetBase=script?new URL('.',script.src):new URL('/por-derecho/assets/',location.origin);
  const projectRoot=new URL('../',assetBase);
  const lang=((d.documentElement.lang||'').toLowerCase().startsWith('es')||location.pathname.includes('/es/'))?'es':'en';
  const isEs=lang==='es';
  const strings=isEs?{
    case:'Caso',search:'Buscar',caseLong:'Sala de control',searchLong:'Buscar en el sitio',evidence:'Prueba',institutions:'Instituciones',accountability:'AC y Juez',proceedings:'Procedimientos',updates:'Actualizaciones',about:'Por Derecho',openControl:'Abrir sala de control',gateway:'Una sola puerta para leer el caso como sistema: hechos, prueba, preguntas abiertas, responsables de respuesta y qué podría cambiar la interpretación.',count:n=>`${n} resultado${n===1?'':'s'}`,empty:'No hay coincidencias en el índice controlado. Pruebe un nombre, fecha, procedimiento, finca o importe.'
  }:{
    case:'Case',search:'Search',caseLong:'Case control room',searchLong:'Search the site',evidence:'Evidence',institutions:'Institutions',accountability:'AC & Judge',proceedings:'Proceedings',updates:'Updates',about:'Por Derecho',openControl:'Open case control room',gateway:'One door into the case as a system: facts, evidence, open questions, answer-holders and what could change the interpretation.',count:n=>`${n} result${n===1?'':'s'}`,empty:'No match in the controlled index. Try a name, date, proceeding, property number or amount.'
  };
  const urls={
    control:new URL(isEs?'es/sala-control-caso/':'en/case-control-room/',projectRoot).href,
    search:new URL(isEs?'es/buscar/':'en/search/',projectRoot).href,
    home:new URL(`${lang}/`,projectRoot).href,
    proceedings:new URL(isEs?'es/cuaderno-juridico/':'en/legal-notebook/',projectRoot).href,
    updates:new URL(isEs?'es/actualizaciones/':'en/updates/',projectRoot).href,
    about:new URL(isEs?'es/sobre-nosotros/':'en/about/',projectRoot).href,
    other:new URL(isEs?'en/':'es/',projectRoot).href
  };
  const isHome=()=>new URL(location.href).pathname.replace(/\/+$/,'/')===new URL(urls.home).pathname;
  const isControl=()=>/\/(case-control-room|sala-control-caso)\/?$/i.test(location.pathname);
  const isSearch=()=>/\/(search|buscar)\/?$/i.test(location.pathname);
  const excludedUtility=()=>/\/(aviso-legal|aviso-legal-privacidad|privacy|privacidad|contacto|contact|faq)\/?$/i.test(location.pathname);
  const ensureCss=()=>{
    if(!d.querySelector('link[data-psr-unitary-shell-css]')){
      const link=d.createElement('link');link.rel='stylesheet';link.href=new URL('unitary-public-shell-20260818.css?v=20260819a',assetBase).href;link.dataset.psrUnitaryShellCss='true';d.head.appendChild(link);
    }
    if(!d.querySelector('link[data-psr-unitary-shell-a11y-css]')){
      const aux=d.createElement('link');aux.rel='stylesheet';aux.href=new URL('unitary-public-shell-20260818.a11y.css?v=20260819a',assetBase).href;aux.dataset.psrUnitaryShellA11yCss='true';d.head.appendChild(aux);
    }
  };
  const addUtility=()=>{
    if(excludedUtility()||isControl()||isSearch()||d.querySelector('.psr-utility-nav'))return;
    const nav=d.createElement('nav');nav.className='psr-utility-nav';nav.setAttribute('aria-label',isEs?'Accesos globales':'Global shortcuts');
    nav.innerHTML=`<a href="${urls.control}" title="${strings.caseLong}">${strings.case}<span> · control</span></a><a href="${urls.search}" title="${strings.searchLong}">${strings.search}<span> · /</span></a>`;
    d.body.appendChild(nav);
  };
  const simplifyHomeNav=()=>{
    if(!isHome())return;
    const nav=d.querySelector('#main-nav.main-nav,.main-nav#main-nav');if(!nav||(nav.dataset.psrConsolidatedNav==='true'&&nav.querySelector('.nav-accountability')))return;
    nav.dataset.psrConsolidatedNav='true';
    nav.innerHTML=`<a class="psr-nav-primary" href="${urls.control}">${strings.case}</a><a class="psr-nav-evidence" href="#record">${strings.evidence}</a><a class="psr-nav-institutions" href="#institutional-map">${strings.institutions}</a><a class="nav-accountability" href="${isEs?'#institutional-accountability-12aug':'#institutional-accountability-12aug-en'}">${strings.accountability}</a><a href="${urls.proceedings}">${strings.proceedings}</a><a href="${urls.updates}">${strings.updates}</a><a href="${urls.about}">${strings.about}</a><a class="psr-nav-search" href="${urls.search}">${strings.search}</a><a class="language-link" href="${urls.other}" hreflang="${isEs?'en':'es'}">${isEs?'EN':'ES'}</a>`;
    if(!d.querySelector('.psr-home-control-gateway')){
      const gateway=d.createElement('aside');gateway.className='psr-home-control-gateway';gateway.setAttribute('aria-label',strings.caseLong);
      gateway.innerHTML=`<div class="shell psr-gateway-inner"><p><strong>${strings.caseLong}.</strong> ${strings.gateway}</p><a href="${urls.control}">${strings.openControl} →</a></div>`;
      const priority=d.querySelector('.priority-band');const hero=d.querySelector('main .hero');(priority||hero)?.insertAdjacentElement('afterend',gateway);
    }
  };
  const normalize=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9€]+/g,' ').trim();
  const escapeHtml=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const humanize=path=>{const bits=path.replace(/^\/+|\/+$/g,'').split('/');const slug=bits[bits.length-1]||bits[bits.length-2]||'';return slug.replace(/-/g,' ').replace(/\b\w/g,m=>m.toUpperCase());};
  const localProjectUrl=raw=>{
    try{
      const u=new URL(raw,projectRoot);const marker='/por-derecho/';const i=u.pathname.indexOf(marker);
      if(i>=0)return new URL(u.pathname.slice(i+marker.length)+u.search,projectRoot).href;
      if(u.origin===location.origin&&u.pathname.startsWith(projectRoot.pathname))return u.href;
    }catch{}
    return null;
  };
  const loadEntries=async()=>{
    let curated=[];
    for(const file of ['data/unitary-route-registry-v1.json','data/unitary-route-registry-sync-20260819.json']){
      try{const r=await fetch(new URL(`${file}?v=20260823a`,assetBase));if(r.ok){const data=await r.json();if(Array.isArray(data))curated.push(...data);}}catch{}
    }
    const seen=new Set(curated.map(x=>x.path));
    const ingest=xmlText=>{
      const xml=new DOMParser().parseFromString(xmlText,'application/xml');
      [...xml.querySelectorAll('url > loc')].forEach(loc=>{
        try{
          const u=new URL(loc.textContent.trim());const marker='/por-derecho/';const i=u.pathname.indexOf(marker);if(i<0)return;
          const path=u.pathname.slice(i+marker.length).replace(/^\/+|\/+$/g,'')+'/';
          if(!path.startsWith(`${lang}/`)||seen.has(path))return;
          seen.add(path);curated.push({lang,path,title:humanize(path),type:'route',summary:'',tags:[],aliases:[]});
        }catch{}
      });
    };
    const sitemapUrls=new Set([new URL('../sitemap.xml?v=20260823a',assetBase).href]);
    try{
      const r=await fetch(new URL('../robots.txt?v=20260823a',assetBase));
      if(r.ok){
        const text=await r.text();
        text.split(/\r?\n/).forEach(line=>{
          const m=line.match(/^\s*Sitemap:\s*(\S+)\s*$/i);if(!m)return;
          const local=localProjectUrl(m[1]);if(local)sitemapUrls.add(local);
        });
      }
    }catch{}
    const fetched=await Promise.allSettled([...sitemapUrls].map(async url=>{const r=await fetch(url);if(!r.ok)throw new Error(`HTTP ${r.status}`);return r.text();}));
    fetched.forEach(result=>{if(result.status==='fulfilled')ingest(result.value);});
    return curated.filter(x=>x.lang===lang);
  };
  const scoreEntry=(entry,q)=>{
    if(!q)return 1;
    const n=normalize(q),tokens=n.split(/\s+/).filter(Boolean);if(!tokens.length)return 1;
    const title=normalize(entry.title),summary=normalize(entry.summary),path=normalize(entry.path),tags=normalize((entry.tags||[]).join(' ')),aliases=normalize((entry.aliases||[]).join(' '));
    let score=0;if(title===n)score+=180;if(title.includes(n))score+=90;if(aliases.includes(n))score+=85;if(tags.includes(n))score+=55;if(path.includes(n))score+=45;if(summary.includes(n))score+=30;
    tokens.forEach(t=>{if(title.includes(t))score+=24;if(aliases.includes(t))score+=22;if(tags.includes(t))score+=15;if(path.includes(t))score+=10;if(summary.includes(t))score+=8;});return score;
  };
  const initSearch=async()=>{
    const input=d.getElementById('psr-search-input'),results=d.getElementById('psr-search-results');if(!input||!results||input.dataset.ready==='true')return;
    input.dataset.ready='true';const count=d.getElementById('psr-search-count'),form=d.getElementById('psr-search-form'),filters=[...d.querySelectorAll('[data-search-filter]')];let active='all';const entries=await loadEntries();
    const render=()=>{
      const q=input.value.trim();const rows=entries.map(e=>({e,score:scoreEntry(e,q)})).filter(x=>x.score>0&&(active==='all'||x.e.type===active)).sort((a,b)=>b.score-a.score||a.e.title.localeCompare(b.e.title)).slice(0,80);
      if(count)count.textContent=strings.count(rows.length);if(!rows.length){results.innerHTML=`<div class="psr-search-empty">${strings.empty}</div>`;return;}
      results.innerHTML=rows.map(({e})=>{const href=new URL(e.path,projectRoot).href;const meta=[e.type,...(e.tags||[]).slice(0,3)].filter(Boolean).map(x=>`<span>${escapeHtml(x)}</span>`).join('');return `<article class="psr-search-result"><h2><a href="${href}">${escapeHtml(e.title)}</a></h2>${e.summary?`<p>${escapeHtml(e.summary)}</p>`:''}<div class="psr-search-meta">${meta}</div></article>`;}).join('');
    };
    filters.forEach(btn=>btn.addEventListener('click',()=>{active=btn.dataset.searchFilter||'all';filters.forEach(b=>b.setAttribute('aria-pressed',String(b===btn)));render();}));
    form?.addEventListener('submit',ev=>{ev.preventDefault();const u=new URL(location.href);if(input.value.trim())u.searchParams.set('q',input.value.trim());else u.searchParams.delete('q');history.replaceState(null,'',u);render();});
    input.addEventListener('input',render);input.value=new URL(location.href).searchParams.get('q')||'';render();
    d.addEventListener('keydown',ev=>{if(ev.key==='/'&&!/input|textarea|select/i.test(d.activeElement?.tagName||'')){ev.preventDefault();input.focus();}});
  };
  const init=()=>{ensureCss();d.documentElement.dataset.psrUnitaryShellVersion=VERSION;simplifyHomeNav();addUtility();initSearch();};
  window.PorDerechoUnitaryShell={version:VERSION,init,urls,loadEntries};
  if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',init,{once:true});else init();window.setTimeout(init,1800);
})();

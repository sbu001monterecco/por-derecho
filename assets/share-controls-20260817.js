(()=>{
  const d=document;
  if(window.PorDerechoShare?.version==='20260817b'){
    window.PorDerechoShare.init(d);
    return;
  }

  const script=d.currentScript;
  if(script && !d.querySelector('link[data-pd-share-styles]')){
    const css=d.createElement('link');
    css.rel='stylesheet';
    css.href=new URL('share-controls-20260817.css?v=20260817b',script.src).href;
    css.dataset.pdShareStyles='true';
    d.head.appendChild(css);
  }

  // Shared bridge for the source-controlled A&G / RICPE / San Telmo / RSM genealogy.
  // The renderer is route-gated and is a no-op outside its defined ES/EN institutional surfaces.
  if(script && !d.querySelector('script[data-pd-ricpe-santelmo-genealogy]')){
    const genealogy=d.createElement('script');
    genealogy.src=new URL('ricpe-santelmo-institutional-genealogy-20260818.js?v=20260818a',script.src).href;
    genealogy.async=false;
    genealogy.dataset.pdRicpeSantelmoGenealogy='true';
    d.head.appendChild(genealogy);
  }

  const lang=(d.documentElement.lang||'en').toLowerCase().startsWith('es')?'es':'en';
  const strings=lang==='es'?{
    label:'Compartir esta página',linkedin:'LinkedIn',whatsapp:'WhatsApp',email:'Email',copy:'Copiar enlace',copied:'Enlace copiado',copyPrompt:'Copiar enlace:'
  }:{
    label:'Share this page',linkedin:'LinkedIn',whatsapp:'WhatsApp',email:'Email',copy:'Copy link',copied:'Link copied',copyPrompt:'Copy link:'
  };

  const canonical=()=>{
    const declared=d.querySelector('link[rel="canonical"]')?.href;
    if(declared) return declared;
    const u=new URL(location.href);
    u.search='';u.hash='';
    return u.href;
  };
  const cleanAnchor=(value='')=>String(value).replace(/^#/,'').trim();
  const objectUrl=(scope)=>{
    const explicit=scope?.dataset.shareUrl;
    let base=explicit?new URL(explicit,canonical()).href:canonical();
    const anchor=cleanAnchor(scope?.dataset.shareAnchor||scope?.dataset.shareId||'');
    if(anchor){const u=new URL(base);u.hash=anchor;base=u.href;}
    return base;
  };
  const pageTitle=()=>d.querySelector('h1')?.textContent?.trim()||d.title;
  const pageHook=()=>d.querySelector('[data-share-hook]')?.textContent?.trim()||d.querySelector('meta[name="description"]')?.content||'';
  const payload=(scope)=>{
    const title=scope?.dataset.shareTitle?.trim()||pageTitle();
    const hook=scope?.dataset.shareHook?.trim()||pageHook();
    const url=objectUrl(scope);
    return {title,hook,url,text:hook?`${title} — ${hook}`:title};
  };
  const bind=(scope)=>{
    if(!scope||scope.dataset.shareInitialized==='true') return;
    scope.dataset.shareInitialized='true';
    const p=payload(scope);
    scope.querySelectorAll('[data-share-linkedin]').forEach(a=>a.href=`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(p.url)}`);
    scope.querySelectorAll('[data-share-whatsapp]').forEach(a=>a.href=`https://wa.me/?text=${encodeURIComponent(`${p.text} ${p.url}`)}`);
    scope.querySelectorAll('[data-share-email]').forEach(a=>a.href=`mailto:?subject=${encodeURIComponent(p.title)}&body=${encodeURIComponent(`${p.text}\n\n${p.url}`)}`);
    scope.querySelectorAll('[data-copy-link]').forEach(b=>{
      b.addEventListener('click',async()=>{
        const old=b.textContent;
        try{
          await navigator.clipboard.writeText(p.url);
          b.textContent=b.dataset.copied||strings.copied;
          b.setAttribute('aria-live','polite');
          setTimeout(()=>{b.textContent=old;b.removeAttribute('aria-live');},1800);
        }catch{
          prompt(strings.copyPrompt,p.url);
        }
      });
    });
  };

  const excluded=()=>/\/(aviso-legal-privacidad|privacy|contacto|contact|faq)(\/|$)/i.test(location.pathname);
  const isLanguageHome=()=>/\/por-derecho\/(es|en)\/?$/i.test(location.pathname);

  const buildDefault=()=>{
    if(excluded()||!d.querySelector('main')||d.querySelector('.book-share,[data-share-scope],.share-controls')) return;
    const section=d.createElement('section');
    section.className='pd-share-section';
    section.setAttribute('aria-label',strings.label);
    section.innerHTML=`<div class="shell"><div class="share-controls" data-share-scope><p class="share-controls__label">${strings.label}</p><div class="share-controls__actions"><a data-share-linkedin target="_blank" rel="noopener">${strings.linkedin}</a><a data-share-whatsapp target="_blank" rel="noopener">${strings.whatsapp}</a><a data-share-email>${strings.email}</a><button type="button" data-copy-link data-copied="${strings.copied}">${strings.copy}</button></div></div></div>`;
    const main=d.querySelector('main');
    if(isLanguageHome()){
      const priority=d.querySelector('.priority-band');
      const hero=d.querySelector('.hero');
      const anchor=priority||hero;
      if(anchor) anchor.insertAdjacentElement('afterend',section); else main.prepend(section);
    }else{
      main.appendChild(section);
    }
  };

  const init=(root=d)=>{
    buildDefault();
    const scopes=new Set();
    root.querySelectorAll?.('.book-share,[data-share-scope],.share-controls').forEach(el=>scopes.add(el));
    scopes.forEach(bind);
  };

  window.PorDerechoShare={version:'20260817b',init,canonical,payload};
  if(d.readyState==='loading') d.addEventListener('DOMContentLoaded',()=>init(d),{once:true}); else init(d);
})();

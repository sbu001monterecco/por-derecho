(() => {
  'use strict';
  if (window.__pdOwnerCourtNetworkHomepage20260826) return;
  window.__pdOwnerCourtNetworkHomepage20260826 = true;
  const path=location.pathname.replace(/index\.html$/,'');
  const isHome=/\/por-derecho\/(es|en)\/?$/.test(path)||/^\/(es|en)\/?$/.test(path);
  if(!isHome)return;
  const isEn=/\/en\/?$/.test(path)||document.documentElement.lang==='en';
  const prefix=path.includes('/por-derecho/')?'/por-derecho':'';
  const target=isEn?`${prefix}/en/matter-identity-registry/non-lpb-matkator-owner-network/`:`${prefix}/es/registro-identidad-materia/perimetro-propietarios-no-lpb-matkator/`;
  const updateRoute=isEn?`${prefix}/en/updates/`:`${prefix}/es/actualizaciones/`;
  const copy=isEn?{
    marker:'Latest material update',old:'25 August 2026',date:'26 August 2026',
    kicker:'26 AUGUST 2026 · MATERIAL UPDATE',title:'Owners, parties and later continuity—without collective attribution.',
    body:'The new source-graded network separates the seven AP 89/2014 claimant-owners from the wider Montelanza/Molina perimeter, individualises the Celia Guillén and Manuel Molina Climent propositions, and groups the Acosta Matos family/business block while keeping every person, company, power, date and act separate.',
    link:'Open the owner and court-party network',updates:'All material updates'
  }:{
    marker:'Última actualización material',old:'25 agosto 2026',date:'26 agosto 2026',
    kicker:'26 AGOSTO 2026 · ACTUALIZACIÓN MATERIAL',title:'Propietarios, partes y continuidad posterior—sin atribución colectiva.',
    body:'La nueva red source-graded separa los siete demandantes propietarios de AP 89/2014 del perímetro Montelanza/Molina más amplio, individualiza las proposiciones de Celia Guillén y Manuel Molina Climent y agrupa el bloque familia/empresa Acosta Matos manteniendo separadas cada persona, sociedad, poder, fecha y actuación.',
    link:'Abrir la red de propietarios y partes',updates:'Todas las actualizaciones'
  };
  const updateDate=()=>{
    const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
    let node;
    while((node=walker.nextNode())){
      const text=node.nodeValue||'';
      if(text.includes(copy.marker)&&text.includes(copy.old)){
        node.nodeValue=text.replace(copy.old,copy.date);
        const parent=node.parentElement;
        if(parent)parent.dataset.ownerCourtNetworkUpdateDate='20260826';
        return parent;
      }
    }
    return null;
  };
  const addGateway=anchor=>{
    if(document.querySelector('[data-owner-court-network-homepage-gateway]'))return;
    const section=document.createElement('section');
    section.dataset.ownerCourtNetworkHomepageGateway='20260826';
    section.style.cssText='background:#f3f0e9;padding:2.3rem 0;border-top:1px solid rgba(19,37,45,.12);border-bottom:1px solid rgba(19,37,45,.12)';
    const shell=document.createElement('div');shell.className='shell';
    const kicker=document.createElement('p');kicker.className='eyebrow';kicker.textContent=copy.kicker;
    const heading=document.createElement('h2');heading.textContent=copy.title;heading.style.cssText='max-width:24ch;margin:.35rem 0 .8rem';
    const body=document.createElement('p');body.textContent=copy.body;body.style.cssText='max-width:78rem;line-height:1.55';
    const nav=document.createElement('p');nav.style.cssText='display:flex;flex-wrap:wrap;gap:.8rem;margin-top:1rem';
    const main=document.createElement('a');main.href=target;main.textContent=`${copy.link} →`;main.style.fontWeight='900';
    const updates=document.createElement('a');updates.href=updateRoute;updates.textContent=`${copy.updates} →`;updates.style.fontWeight='900';
    nav.append(main,updates);shell.append(kicker,heading,body,nav);section.appendChild(shell);
    const host=anchor?.closest('section')||document.querySelector('main > section:first-of-type');
    if(host)host.insertAdjacentElement('afterend',section);else document.querySelector('main')?.prepend(section);
  };
  const run=()=>{const anchor=updateDate();addGateway(anchor)};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run,{once:true});else run();
})();
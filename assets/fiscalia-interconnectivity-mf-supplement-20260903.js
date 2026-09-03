(() => {
  const script=document.currentScript, root=document.querySelector('[data-mf-interconnectivity]'); if(!script||!root)return;
  const lang=document.documentElement.lang.toLowerCase().startsWith('es')?'es':'en';
  const base=new URL('../',new URL('.',script.src));
  const dataUrl=new URL('assets/data/fiscalia-proceedings-interconnectivity-supplement-20260903.json',base);
  const fullText=new URL(lang==='es'?'es/ministerio-fiscal/expedientes/eg-352-2025/':'en/public-prosecution-service/files/eg-352-2025/',base);
  const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let event=null;
  function shouldShow(){const m=location.hash.match(/^#file=([^&]+)/);const f=m?decodeURIComponent(m[1]):'ALL';return f==='ALL'||f==='GC-FIS-015';}
  function inject(){
    if(!event||!shouldShow())return;
    const list=root.querySelector('.pd-mf-events'); if(!list||list.querySelector('[data-event-id="PD-SP-EVT-0158"]'))return;
    const article=document.createElement('article'); article.className='pd-mf-event'; article.dataset.eventId=event.event_id; article.dataset.direction=event.direction;
    article.innerHTML=`<header><strong>${esc(event.event_date)} · ${esc(event.record_type)}</strong><span class="pd-mf-code">${esc(event.event_id)}</span></header><div class="pd-mf-badges"><span class="pd-mf-badge">${esc(event.direction)}</span><span class="pd-mf-badge">${lang==='es'?'SUPLEMENTO 03-09-2026':'03-09-2026 SUPPLEMENT'}</span></div><p><strong>${esc(event.official_reference)}</strong> — ${esc(event.public_summary)}</p><p class="pd-mf-links"><a href="${esc(fullText.href)}">${lang==='es'?'Texto íntegro comprobado':'Checked full text'}</a> · <span class="pd-mf-code">GC-FIS-015</span></p><details><summary>${lang==='es'?'Qué prueba / qué no prueba':'What it proves / does not prove'}</summary>${(event.proves||[]).map(x=>`<p>${esc(x)}</p>`).join('')}${(event.does_not_prove||[]).map(x=>`<p>${lang==='es'?'No prueba':'Does not prove'}: ${esc(x)}</p>`).join('')}</details>`;
    list.prepend(article);
    const h3=list.previousElementSibling; if(h3&&/^\d+/.test(h3.textContent)){const n=parseInt(h3.textContent,10);h3.textContent=h3.textContent.replace(/^\d+/,String(n+1));}
  }
  fetch(dataUrl,{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(String(r.status));return r.json()}).then(d=>{event=d.events&&d.events[0];inject();new MutationObserver(inject).observe(root,{childList:true,subtree:true});addEventListener('hashchange',()=>setTimeout(inject,0));}).catch(()=>{});
})();

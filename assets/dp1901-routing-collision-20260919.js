(function(){
  const current=document.currentScript;
  if(!current) return;
  const dataUrl=new URL('data/dp1901-routing-collision-v1.json',current.src);
  const siteRoot=new URL('../',current.src);
  const siteUrl=value=>new URL(String(value||'').replace(/^\//,''),siteRoot).href;
  const esc=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const style=document.createElement('style');
  style.textContent=`
  .dp1901-collision{max-width:1120px;margin:2rem auto;padding:0 1rem}.dp1901-collision .box{border:1px solid #cfd8dc;border-radius:18px;background:#fff;box-shadow:0 16px 42px rgba(20,30,35,.08);overflow:hidden}
  .dp1901-collision .head{padding:1.1rem 1.25rem;background:#f5f7f8;border-bottom:1px solid #dde5e8}.dp1901-collision h2{margin:.1rem 0 .35rem;font-size:1.5rem}.dp1901-collision .head p{margin:.25rem 0;color:#3d4a50}
  .dp1901-collision .timeline{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:.55rem;padding:1rem}.dp1901-collision .node{border:1px solid #d9e0e3;border-radius:12px;padding:.75rem;background:#fff;text-decoration:none;color:inherit;min-height:122px}.dp1901-collision .node:hover{box-shadow:0 8px 22px rgba(20,30,35,.09)}.dp1901-collision .date{font-size:.78rem;font-weight:700;color:#59666d}.dp1901-collision .label{font-weight:800;margin:.25rem 0}.dp1901-collision .detail{font-size:.86rem;line-height:1.35;color:#4b565c}
  .dp1901-collision .tone-ochre{border-top:5px solid #a7772a}.dp1901-collision .tone-blue{border-top:5px solid #486d8f}.dp1901-collision .tone-grey{border-top:5px solid #7a858b}.dp1901-collision .tone-charcoal{border-top:5px solid #2f363a}.dp1901-collision .tone-navy{border-top:5px solid #173f5f}
  .dp1901-collision .missing{margin:0 1rem 1rem;padding:.85rem 1rem;border:2px dashed #a63f35;border-radius:12px;background:#fff9f7;font-weight:700}.dp1901-collision .questions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.65rem;padding:0 1rem 1rem}.dp1901-collision .q{padding:.7rem .8rem;border-left:4px solid #7e8c92;background:#f7f9fa}
  .dp1901-collision .visuals{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.65rem;padding:0 1rem 1rem}.dp1901-collision .visuals a{display:block;text-decoration:none;color:inherit;border:1px solid #d9e0e3;border-radius:10px;overflow:hidden;background:#fff}.dp1901-collision .visuals img{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;background:#f4f5f6}.dp1901-collision .visuals span{display:block;padding:.55rem;font-size:.8rem}
  .dp1901-collision .boundary{padding:.9rem 1rem;border-top:1px solid #dde5e8;background:#fafbfb;font-size:.9rem;color:#4d5960}
  @media(max-width:900px){.dp1901-collision .timeline{grid-template-columns:repeat(2,minmax(0,1fr))}.dp1901-collision .visuals{grid-template-columns:repeat(2,minmax(0,1fr))}}
  @media(max-width:600px){.dp1901-collision .timeline,.dp1901-collision .questions,.dp1901-collision .visuals{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);
  fetch(dataUrl).then(r=>r.json()).then(d=>{
    document.querySelectorAll('[data-dp1901-collision]').forEach(el=>{
      const es=(document.documentElement.lang||'').toLowerCase().startsWith('es');
      const nodes=d.nodes.filter(n=>['REF24','REF21','DP1901_JUL9','DP1901_JUL12','FISCAL29','AUTO14'].includes(n.id));
      const questions=es?d.questions.es:d.questions.en;
      const html=`<div class="box"><div class="head"><div style="font-size:.78rem;font-weight:800;letter-spacing:.08em;color:#6a4b13">${es?'TRAZABILIDAD COMÚN · DP 1901/2026':'SHARED TRACEABILITY · DP 1901/2026'}</div><h2>${es?'Dos escritos autónomos. Un DP con dos identidades documentadas. Falta el puente.':'Two autonomous filings. One DP with two documented identities. The bridge is missing.'}</h2><p>${esc(es?d.summary.es:d.summary.en)}</p></div><div class="timeline">${nodes.map(n=>`<a class="node tone-${esc(n.tone)}" href="${esc(siteUrl(es?n.route_es:n.route_en))}"><div class="date">${esc(n.date)}</div><div class="label">${esc(es?n.label_es:n.label_en)}</div><div class="detail">${esc(es?n.detail_es:n.detail_en)}</div></a>`).join('')}</div><div class="missing">${es?'DOCUMENTO / EVENTO PUENTE NO PRODUCIDO — reparto · unión · reasignación · remisión · reclasificación · segregación':'BRIDGE DOCUMENT / EVENT NOT PRODUCED — allocation · joinder · reassignment · remittal · reclassification · segregation'}</div><div class="questions">${questions.map((q,i)=>`<div class="q"><strong>${i+1}.</strong> ${esc(q)}</div>`).join('')}</div><div class="visuals">${d.visuals.map(v=>`<a href="${esc(siteUrl(v.src))}"><img loading="lazy" src="${esc(siteUrl(v.src))}" alt=""><span>${esc(es?v.label_es:v.label_en)}</span></a>`).join('')}</div><div class="boundary">${esc(es?d.boundaries.es:d.boundaries.en)}</div></div>`;
      el.classList.add('dp1901-collision'); el.innerHTML=html;
    });
  }).catch(()=>{});
})();
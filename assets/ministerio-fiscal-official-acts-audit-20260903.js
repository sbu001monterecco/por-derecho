(() => {
  const root=document.querySelector('[data-mf-acts-audit]'); if(!root)return;
  const lang=document.documentElement.lang==='en'?'en':'es';
  const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const base=root.dataset.base||'';
  const n=id=>{const m=/PD-SP-EVT-(\d+)/.exec(id||''); return m?+m[1]:-1};
  const files=['institutional-communications-register-v1.json','institutional-communications-register-mf-supplement-20260903.json','ministerio-fiscal-official-acts-audit-v1.json'];
  Promise.all(files.map(f=>fetch(base+f,{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(f+' '+r.status);return r.json()}))).then(([c,s,a])=>{
    const all=[...(c.events||[]),...(s.events||[])];
    const scope=all.filter(e=>(n(e.event_id)>=76&&n(e.event_id)<=140)||e.event_id==='PD-SP-EVT-0158').sort((x,y)=>(x.event_date||'').localeCompare(y.event_date||'')||x.event_id.localeCompare(y.event_id));
    const cat=e=>(a.overrides[e.event_id]?.category||a.default_31aug_separate_row_state);
    const counts={A:0,B:0,C:0,D:0,E:a.source_gaps.length,F:a.historical_recovery.length}; scope.forEach(e=>counts[cat(e)]++);
    const rows=scope.map(e=>{const ov=a.overrides[e.event_id]||{}, special=e.event_id==='PD-SP-EVT-0158'; return `<tr id="${esc(e.event_id)}"><td><a href="#${esc(e.event_id)}"><span class="mf-id">${esc(e.event_id)}</span></a></td><td>${esc(e.event_date||'—')}</td><td>${esc(e.record_type||'—')}</td><td>${esc(e.office||'—')}</td><td>${esc(e.official_reference||'—')}</td><td><strong>${esc(cat(e))}</strong><br><small>${esc(ov.reason||a.default_reason)}</small></td><td>${special?`<a href="${lang==='es'?'../expedientes/eg-352-2025/':'../files/eg-352-2025/'}">${lang==='es'?'texto íntegro':'full text'}</a> · <span class="mf-id">PD-SP-CUST-0001</span>`:'—'}</td></tr>`}).join('');
    const gaps=[...a.source_gaps,...a.historical_recovery].map(g=>`<li><strong>${esc(g.category)} · ${esc(g.reference)}</strong> — ${esc(g.next_source)}</li>`).join('');
    root.innerHTML=`<div class="mf-kpis">${Object.entries(counts).map(([k,v])=>`<div class="mf-kpi"><strong>${v}</strong><span>${k}</span></div>`).join('')}</div><div class="mf-rule"><strong>${lang==='es'?'Verificación live separada.':'Separate live verification.'}</strong> ${lang==='es'?'La categoría A exige despliegue y apertura directa de la URL pública; la presencia en Git no se trata como prueba live.':'Category A requires deployment and direct opening of the public URL; Git presence is not treated as live proof.'}</div><div class="mf-table-wrap"><table class="mf-table"><thead><tr><th>ID</th><th>${lang==='es'?'Fecha':'Date'}</th><th>${lang==='es'?'Tipo':'Type'}</th><th>${lang==='es'?'Oficina':'Office'}</th><th>${lang==='es'?'Referencia':'Reference'}</th><th>${lang==='es'?'Categoría':'Category'}</th><th>${lang==='es'?'Texto / custodia':'Text / custody'}</th></tr></thead><tbody>${rows}</tbody></table></div><h2>${lang==='es'?'Brechas E/F que impiden completitud universal':'E/F gaps preventing universal completeness'}</h2><ul>${gaps}</ul>`;
  }).catch(err=>root.innerHTML=`<p class="mf-error">${esc(err.message)}</p>`);
})();

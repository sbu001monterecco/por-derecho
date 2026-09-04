(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  if (!/\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(path)) return;
  const lang = (document.documentElement.lang || (path.includes('/en/') ? 'en' : 'es')).toLowerCase().startsWith('en') ? 'en' : 'es';
  const normalise = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[–—]/g,'-').replace(/[^a-z0-9^]+/g,' ').trim().replace(/\s+/g,' ');
  const terms = [
    'control 21','control 22','control 24','nexus 36','gc hc 010','gc-hc-010','dp 1901 2026','dp 1956 2026',
    '18 june 2026','18 junio 2026','25 june 2026','25 junio 2026','cgpj 169 2026','di 169 2026','alzada 286 2026',
    'recurso de alzada 286 2026','dip 2 2026','fiscalia dip 2 2026','icalpa 80 2026','dip 80 2026',
    'separacion administrador concursal','administrator removal','honorarios administrador concursal','administrator fees',
    'rpl 2523 2025','apelacion calificacion','classification appeal','concurso 36 2012','insolvency 36 2012','triangle concurso','triangulo concurso'
  ].map(normalise);
  const matches = q => { const n = normalise(q); return n.length > 1 && terms.some(t => t.includes(n) || n.includes(t)); };
  const def = lang === 'en' ? {
    id:'C36-TRIANGLE-20260904', href:'/por-derecho/data/concurso-36-2012-triangle-register-v1.json', badge:'Canonical graph', code:'CONCURSO 36/2012 · CONTROLS 21 · 22 · 24',
    title:'Private actors ↔ insolvency administrator ↔ Concurso judge',
    summary:'Canonical interconnection graph with Control 24/GC-HC-010, CGPJ 169/286, DIP 2/2026, ICALPA 80/2026, AC removal/fees and RPL 2523/2025. Related routes remain procedurally separate.'
  } : {
    id:'C36-TRIANGLE-20260904', href:'/por-derecho/data/concurso-36-2012-triangle-register-v1.json', badge:'Grafo canónico', code:'CONCURSO 36/2012 · CONTROLES 21 · 22 · 24',
    title:'Actores privados ↔ Administrador Concursal ↔ Juez del Concurso',
    summary:'Grafo canónico con Control 24/GC-HC-010, CGPJ 169/286, DIP 2/2026, ICALPA 80/2026, separación/honorarios AC y RPL 2523/2025. Las vías relacionadas siguen procesalmente separadas.'
  };
  const augment = () => {
    const input = document.querySelector('#canonical-home-search-input'); const results = document.querySelector('.canonical-search-results'); const status = document.querySelector('.canonical-search-status');
    if (!input || !results) return;
    const existing = results.querySelector(`[data-search-result-id="${def.id}"]`);
    if (!matches(input.value)) { if (existing) existing.remove(); return; }
    if (!existing) { const card=document.createElement('a'); card.className='canonical-search-result'; card.href=def.href; card.setAttribute('data-search-result-id',def.id); card.innerHTML=`<span class="canonical-search-result-top"><span class="canonical-search-badge">${def.badge}</span><span class="canonical-search-id">${def.code}</span></span><strong>${def.title}</strong><small>${def.summary}</small>`; results.prepend(card); }
    results.hidden=false; if(status) status.textContent=lang==='en'?'Concurso 36/2012 triangle located.':'Triángulo de Concurso 36/2012 localizado.';
  };
  const install=(attempt=0)=>{const input=document.querySelector('#canonical-home-search-input'); const form=document.querySelector('.canonical-search-form'); if(!input||!form){if(attempt<50)window.setTimeout(()=>install(attempt+1),80);return;} input.addEventListener('input',()=>window.setTimeout(augment,0)); form.addEventListener('submit',()=>window.setTimeout(augment,0)); window.setTimeout(augment,0);};
  install();
})();

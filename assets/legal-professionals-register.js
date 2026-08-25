(() => {
  'use strict';
  const root = document.querySelector('[data-legal-professionals]');
  if (!root) return;
  const lang = root.dataset.lang === 'es' ? 'es' : 'en';
  const copy = lang === 'es' ? {
    loading:'Cargando registro profesional…', failure:'No se pudo cargar el registro profesional.',
    showing:(n,t)=>`Mostrando ${n} de ${t} profesionales autorizados.`, none:'Sin resultados.',
    firm:'Firma / práctica', role:'Función', status:'Estado de evidencia', scope:'Ámbito documentado', id:'ID inmutable',
    groups:{CURRENT_COUNSEL:'Abogados actuales',FORMER_COUNSEL:'Abogados anteriores',FORMER_COUNSEL_COLLABORATOR:'Colaboradores jurídicos anteriores',FORMER_COUNSEL_ROLE_REVIEW:'Profesionales anteriores — alcance del mandato en revisión',PROCURADOR_CURRENT:'Procuradoras actuales',PROCURADOR_FORMER:'Procuradores/as anteriores'},
    classifications:{OUR_CURRENT_PROFESSIONAL:'Profesional actual de nuestro lado',OUR_FORMER_PROFESSIONAL:'Profesional anterior de nuestro lado'},
    note:'La inclusión en esta lista acredita una función profesional documentada o una conexión profesional expresamente marcada como pendiente de cierre. No convierte al profesional en parte del perímetro de propiedad/reclamación ni transfiere conducta o responsabilidad del cliente.'
  } : {
    loading:'Loading professional register…', failure:'The professional register could not be loaded.',
    showing:(n,t)=>`Showing ${n} of ${t} authorised professionals.`, none:'No results.',
    firm:'Firm / practice', role:'Role', status:'Evidence status', scope:'Documented scope', id:'Immutable ID',
    groups:{CURRENT_COUNSEL:'Current lawyers',FORMER_COUNSEL:'Former lawyers',FORMER_COUNSEL_COLLABORATOR:'Former legal collaborators',FORMER_COUNSEL_ROLE_REVIEW:'Former professionals — mandate scope under review',PROCURADOR_CURRENT:'Current procuradoras',PROCURADOR_FORMER:'Former procuradores'},
    classifications:{OUR_CURRENT_PROFESSIONAL:'Current project-side professional',OUR_FORMER_PROFESSIONAL:'Former project-side professional'},
    note:'Inclusion in this list records a documented professional role or a professional connection expressly marked as awaiting closure. It does not place the professional in the ownership/claimant perimeter and does not transfer client conduct or responsibility.'
  };
  const status = root.querySelector('[data-prof-status]');
  const search = root.querySelector('[data-prof-search]');
  const list = root.querySelector('[data-prof-list]');
  const stats = [...root.querySelectorAll('[data-prof-stat]')];
  const note = root.querySelector('[data-prof-note]');
  if (note) note.textContent = copy.note;
  let register, identityById, organisationById;
  const norm = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
  async function fetchJson(value, base=document.baseURI) {
    const url = new URL(value, base); const response = await fetch(url,{cache:'no-store'});
    if (!response.ok) throw new Error(`${url.pathname} ${response.status}`);
    return {url,data:await response.json()};
  }
  function render() {
    const q = norm(search?.value || '');
    const records = (register.records || []).filter(r => !q || norm([r.public_name,r.role,r.track,r.evidence_status,r.matter_scope,...(r.firm_ids||[]).map(id=>organisationById.get(id)?.name||id)].join(' ')).includes(q));
    status.textContent = copy.showing(records.length, register.records.length);
    const counts = {TOTAL:register.records.length,CURRENT_COUNSEL:0,FORMER_COUNSEL:0,PROCURADOR_CURRENT:0,PROCURADOR_FORMER:0};
    register.records.forEach(r=>{if(r.track==='CURRENT_COUNSEL')counts.CURRENT_COUNSEL++;else if(r.track==='PROCURADOR_CURRENT')counts.PROCURADOR_CURRENT++;else if(r.track==='PROCURADOR_FORMER')counts.PROCURADOR_FORMER++;else counts.FORMER_COUNSEL++;});
    stats.forEach(node=>node.textContent=counts[node.dataset.profStat]??0);
    list.replaceChildren();
    if (!records.length) { const p=document.createElement('p'); p.className='prof-empty'; p.textContent=copy.none; list.appendChild(p); return; }
    const order=['CURRENT_COUNSEL','FORMER_COUNSEL','FORMER_COUNSEL_COLLABORATOR','FORMER_COUNSEL_ROLE_REVIEW','PROCURADOR_CURRENT','PROCURADOR_FORMER'];
    for (const track of order) {
      const rows=records.filter(r=>r.track===track); if(!rows.length) continue;
      const section=document.createElement('section'); section.className='prof-group';
      const h=document.createElement('h2'); h.textContent=copy.groups[track]||track; section.appendChild(h);
      const grid=document.createElement('div'); grid.className='prof-grid';
      rows.sort((a,b)=>a.public_name.localeCompare(b.public_name,lang,{sensitivity:'base'})).forEach(r=>{
        const article=document.createElement('article'); article.className='prof-card'; article.id=r.identity_id;
        const header=document.createElement('header'); const title=document.createElement('h3'); title.textContent=r.public_name; const code=document.createElement('code'); code.textContent=r.identity_id; header.append(title,code); article.appendChild(header);
        const firmNames=(r.firm_ids||[]).map(id=>organisationById.get(id)?.name||id);
        const dl=document.createElement('dl');
        [[copy.role,r.role],[copy.firm,firmNames.length?firmNames.join(' · '):'—'],[copy.status,r.evidence_status],[copy.scope,r.matter_scope]].forEach(([k,v])=>{const dt=document.createElement('dt');dt.textContent=k;const dd=document.createElement('dd');dd.textContent=v;dl.append(dt,dd);});
        article.appendChild(dl);
        if (/REVIEW|OPEN/.test(r.evidence_status)) article.classList.add('is-review');
        grid.appendChild(article);
      });
      section.appendChild(grid); list.appendChild(section);
    }
  }
  search?.addEventListener('input',render);
  (async()=>{
    status.textContent=copy.loading;
    try {
      const [regResult,indexResult]=await Promise.all([fetchJson(root.dataset.registerUrl),fetchJson(root.dataset.indexUrl)]);
      register=regResult.data; const index=indexResult.data;
      const parts=await Promise.all((index.parts||[]).map(p=>fetchJson(p.path,indexResult.url)));
      const all=parts.flatMap(p=>p.data.records||[]); identityById=new Map(all.map(r=>[r.id,r])); organisationById=new Map(all.filter(r=>r.type==='ORGANISATION').map(r=>[r.id,r]));
      register.records.forEach(r=>{if(!identityById.has(r.identity_id))throw new Error(`Unknown identity ${r.identity_id}`);});
      render();
      const requested=decodeURIComponent(location.hash.slice(1)); if(requested){setTimeout(()=>document.getElementById(requested)?.scrollIntoView({behavior:'smooth',block:'center'}),80);}
    } catch(error) { console.error(error); status.textContent=copy.failure; status.classList.add('prof-error'); }
  })();
})();

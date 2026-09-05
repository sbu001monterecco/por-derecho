/* Existing source graph only: rendering does not upgrade an evidential grade. */
(() => {
 'use strict';
 const root=document.querySelector('[data-convergence-app]'); if(!root)return;
 const lang=document.documentElement.lang.startsWith('es')?'es':'en';
 const t=(es,en)=>lang==='es'?es:en;
 const local=v=>typeof v==='string'?v:v&&typeof v==='object'?(v[lang]||v.en||v.es||''):v==null?'':String(v);
 const field=(v,k)=>local(v[k+'_'+lang]||v[k]);
 const id=n=>String(n.key||n.id), title=n=>field(n,'label')||field(n,'name')||id(n);
 const grade=e=>String(e.grade||e.type||e.evidence_status||'OPEN_NOT_LOCATED');
 const from=e=>String(e.from||e.source), to=e=>String(e.to||e.target);
 const node=(tag,text,cls)=>{const n=document.createElement(tag);if(text)n.textContent=text;if(cls)n.className=cls;return n;};
 const choose=(modern,legacy)=>root.querySelector(modern)||root.querySelector(legacy);
 function safeURL(v){
  if(typeof v!=='string'||!v||/^(?:javascript|data):/i.test(v)||v.startsWith('//'))return null;
  if(/^https?:/i.test(v)||v.startsWith('#'))return v;
  const p=v.replace(/^\/?por-derecho\//,'').replace(/^\//,'');
  if(!p.includes('/')&&!/\.[a-z0-9]{2,6}(?:[?#]|$)/i.test(p))return null;
  return p.startsWith('.github/')?'https://github.com/sbu001monterecco/por-derecho/blob/main/'+p:'/por-derecho/'+p;
 }
 function link(text,value){const u=safeURL(value),n=node(u?'a':'span',text);if(u)n.href=u;return n;}
 async function get(u){const r=await fetch(u,{credentials:'omit'});if(!r.ok)throw Error('HTTP '+r.status);return r.json();}
 const graphURL=new URL(root.dataset.graphUrl,location.href);
 async function parts(g,kind){
  if(Array.isArray(g[kind]))return g[kind];
  const descriptors=g[(kind==='nodes'?'node':'edge')+'_parts']||[];
  return (await Promise.all(descriptors.map(async p=>{const d=await get(new URL(p.path,graphURL));const rows=d[kind]||d.records;if(!Array.isArray(rows)||(Number.isInteger(p.count)&&rows.length!==p.count))throw Error('Source count mismatch');return rows;}))).flat();
 }
 async function run(){
  const g=await get(graphURL),nodes=await parts(g,'nodes'),edges=await parts(g,'edges');
  const byID=new Map(nodes.map(n=>[id(n),n]));
  if(!nodes.length||!edges.length||byID.size!==nodes.length||edges.some(e=>!byID.has(from(e))||!byID.has(to(e))))throw Error('Graph identity mismatch');
  const controls={stage:choose('#fc-stage','[data-fc-stage]'),grade:choose('#fc-grade','[data-fc-type]'),group:choose('#fc-group','[data-fc-group]'),search:choose('#fc-search','[data-fc-search]')};
  const status=choose('#fc-status','[data-fc-stats]'),table=choose('#fc-edge-table','[data-fc-table]'),detail=choose('#fc-detail','[data-fc-inspector]');
  let svg=root.querySelector('[data-fc-svg]');const canvas=root.querySelector('#fc-graph-canvas');
  if(!svg&&canvas){svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.dataset.fcSvg='';svg.setAttribute('role','img');canvas.replaceChildren(svg);}
  if(!status||!table||!detail||!svg)throw Error('Required graph control missing');
  const sources=Array.isArray(g.sources)?g.sources:[],sourceMap=new Map(sources.map(s=>[s.id,s]));
  function sourceRefs(parent,list){for(const raw of list||[]){const s=typeof raw==='string'?(sourceMap.get(raw)||{id:raw}):raw;parent.append(link(field(s,'title')||local(s.label)||s.id||String(raw),s.url||s.path||s.route||s.href),document.createTextNode(' '));}}
  function options(select,rows){if(!select)return;select.replaceChildren(new Option(t('Todos','All'),'all'));for(const [value,text] of rows)select.add(new Option(text,String(value)));}
  options(controls.stage,(g.stages||[]).map(s=>[s.id,field(s,'label')||String(s.id)]));
  options(controls.grade,[...new Set(edges.map(grade))].sort().map(k=>[k,field((g.grades||{})[k]||{},'label')||k]));
  options(controls.group,[...new Set(nodes.map(n=>String(n.group||'')))].filter(Boolean).sort().map(k=>[k,k]));
  function inspect(n){
   detail.replaceChildren(node('h3',title(n)),node('p',n.registry_id||n.entity_id||''),node('p',field(n,'role')||field(n,'summary')),node('p',field(n,'limit')||field(n,'limitation')));
   const route=n['route_'+lang]||(n.routes||{})[lang];if(route)detail.append(link(t('Abrir registro documental','Open documentary record'),route));
   const refs=node('p');sourceRefs(refs,n.sources||n.source_ids||[]);detail.append(refs);
  }
  const stages=choose('#fc-stage-grid','[data-fc-groups]');
  if(stages){stages.replaceChildren();for(const s of g.stages||[]){const card=node('section','', 'fc-stage-card');card.append(node('h3',field(s,'label')),node('p',s.period||''));for(const n of nodes.filter(n=>String(n.stage)===String(s.id))){const b=node('button',title(n));b.type='button';b.addEventListener('click',()=>inspect(n));card.append(b);}stages.append(card);}}
  const inference=choose('#fc-current-inference','[data-fc-convergence]');if(inference)inference.replaceChildren(node('p',local(g.strongest_current_inference)));
  const open=root.querySelector('#fc-open-production');if(open)open.replaceChildren(...(g.highest_value_open_proof||[]).map(v=>node('li',local(v))));
  const sp=choose('#fc-sources','[data-fc-sources]');if(sp){sp.replaceChildren();sourceRefs(sp,sources);sp.append(link(t('Registro canónico y fuentes de cada relación','Canonical registry and individual relationship sources'),'assets/data/acosta-matos-functional-convergence-map-v2.json'));}
  const NS='http://www.w3.org/2000/svg';
  const S=(tag,a,text)=>{const n=document.createElementNS(NS,tag);for(const[k,v]of Object.entries(a))n.setAttribute(k,String(v));if(text)n.textContent=text;return n;};
  function draw(){
   const stage=controls.stage?.value||'all',gr=controls.grade?.value||'all',group=controls.group?.value||'all',query=(controls.search?.value||'').toLocaleLowerCase();
   const visible=edges.filter(e=>{
    const a=byID.get(from(e)),b=byID.get(to(e));
    return(gr==='all'||grade(e)===gr)&&(stage==='all'||[a,b].some(n=>String(n.stage)===stage))&&(group==='all'||[a,b].some(n=>String(n.group)===group))&&(!query||[title(a),title(b),field(e,'proposition'),field(e,'label'),e.id].join(' ').toLocaleLowerCase().includes(query));
   });
   status.textContent=`${nodes.length} ${t('nodos','nodes')} · ${visible.length}/${edges.length} ${t('relaciones','relationships')}`;
   table.replaceChildren(...visible.map(e=>{
    const tr=node('tr','', 'fc-evidence-row');tr.dataset.edgeId=String(e.id||'');
    const cells=[`${title(byID.get(from(e)))} → ${title(byID.get(to(e)))}`,`${e.id||''} · ${e.period||e.date||''}`,field((g.grades||{})[grade(e)]||{},'label')||grade(e),field(e,'proposition')||field(e,'label'),[field(e,'limit'),field(e,'limitation'),field(e,'contrary'),field(e,'open_proof')].filter(Boolean).join('\n')];
    for(const v of cells)tr.append(node('td',v));const last=node('td');sourceRefs(last,e.sources||e.source_ids||[]);tr.append(last);return tr;
   }));
   const positions=new Map(nodes.map((n,i)=>[id(n),{x:30+(i%4)*345,y:50+Math.floor(i/4)*125}]));
   svg.setAttribute('viewBox',`0 0 1440 ${Math.ceil(nodes.length/4)*125+80}`);svg.replaceChildren(S('title',{},t('Relaciones documentales: las flechas no prueban causalidad','Documentary relationships: arrows do not prove causation')));
   for(const e of visible){const a=positions.get(from(e)),b=positions.get(to(e)),l=S('line',{x1:a.x+120,y1:a.y+30,x2:b.x+120,y2:b.y+30,class:'fc-graph-edge'});l.append(S('title',{},`${e.id||''} · ${grade(e)}`));svg.append(l);}
   for(const n of nodes){const p=positions.get(id(n)),item=S('g',{transform:`translate(${p.x},${p.y})`,tabindex:0,role:'button','aria-label':title(n),'data-node-id':id(n),class:'fc-graph-node'});item.append(S('rect',{width:265,height:62,rx:8}),S('text',{x:10,y:25},title(n).slice(0,34)),S('text',{x:10,y:47,class:'fc-node-id'},n.registry_id||n.entity_id||''));item.addEventListener('click',()=>inspect(n));item.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();inspect(n);}});svg.append(item);}
   root.dataset.graphState='ready';root.dataset.renderedNodes=String(nodes.length);root.dataset.renderedEdges=String(visible.length);
  }
  for(const c of Object.values(controls))c?.addEventListener(c.tagName==='INPUT'?'input':'change',draw);
  choose('#fc-reset','[data-fc-reset]')?.addEventListener('click',()=>{for(const c of Object.values(controls))if(c)c.value=c.tagName==='INPUT'?'':'all';draw();});
  draw();
 }
 run().catch(e=>{root.dataset.graphState='error';const p=choose('#fc-status','[data-fc-stats]');if(p)p.textContent=t('No se pudo cargar la visualización. Consulte la edición documental inferior.','Visualization could not be loaded. Consult the documentary edition below.');console.error('Convergence source:',e.message);});
})();

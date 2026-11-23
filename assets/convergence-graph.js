/* Render the existing v2 evidence graph. Never change the source grades or infer identity. */
(() => {
 'use strict';
 const app=document.querySelector('[data-convergence-app]');if(!app)return;
 const lang=document.documentElement.lang==='es'?'es':'en';
 const text=(en,es)=>lang==='es'?es:en;
 const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const local=path=>'../../../'+(path||'assets/data/matter-identity-registry-v1.json').replace(/^\/por-derecho\//,'').replace(/^\//,'');
 const detail=app.querySelector('[data-detail]'), grid=app.querySelector('[data-stage-grid]');
 const payloadNode=document.getElementById('convergence-render-payload');
 let data;
 try {data=JSON.parse(payloadNode.textContent);}catch(_){detail.textContent=text('Map data unavailable. Use the source JSON and full matrix below.','Datos no disponibles. Consulte JSON fuente y matriz íntegra.');return;}
 const {nodes,edges,manifest}=data, nodeMap=new Map(nodes.map(n=>[n.key,n]));
 let grade='ALL',selected=null,query='',timer=null,spineIndex=0;
 const norm=x=>String(x).normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 const visibleEdges=()=>edges.filter(e=>(grade==='ALL'||e.grade===grade)&&(!selected||e.from===selected||e.to===selected));
 const gradeLabel=g=>manifest.grades[g]?.['label_'+lang]||g;
 const label=key=>nodeMap.get(key)?.['label_'+lang]||key;
 function sourceLinks(e){return (e.sources||[]).map(p=>`<a href="${esc(local(p))}">${esc(p)}</a>`).join('<br>');}
 function edgeHTML(e){return `<article class="fc-edge-detail" data-edge-id="${esc(e.id)}"><h4>${esc(e.id)} · ${esc(label(e.from))} → ${esc(label(e.to))}</h4><p><strong>${esc(gradeLabel(e.grade))}</strong> · ${esc(e.period)}</p><p>${esc(e.proposition[lang])}</p><p><strong>${text('Limit','Límite')}:</strong> ${esc(e.limit[lang])}</p><p>${sourceLinks(e)}</p></article>`;}
 function draw(){
  const svg=app.querySelector('[data-connectors]'),canvas=app.querySelector('[data-graph-canvas]');
  svg.replaceChildren();if(innerWidth<850)return;
  const box=canvas.getBoundingClientRect();svg.setAttribute('viewBox',`0 0 ${box.width} ${box.height}`);svg.setAttribute('width',box.width);svg.setAttribute('height',box.height);
  for(const e of visibleEdges()){
   const from=grid.querySelector(`[data-node-key="${CSS.escape(e.from)}"]`),to=grid.querySelector(`[data-node-key="${CSS.escape(e.to)}"]`);
   if(!from||!to||from.hidden||to.hidden)continue;
   const a=from.getBoundingClientRect(),b=to.getBoundingClientRect(),x1=a.right-box.left,y1=a.top+a.height/2-box.top,x2=b.left-box.left,y2=b.top+b.height/2-box.top;
   const path=document.createElementNS('http://www.w3.org/2000/svg','path');
   path.setAttribute('d',`M${x1},${y1} C${x1+30},${y1} ${x2-30},${y2} ${x2},${y2}`);
   path.setAttribute('class',`fc-connector ${selected?'is-selected':''}`);
   if(e.grade!=='DIRECT_DOCUMENTARY')path.setAttribute('stroke-dasharray','5 4');
   svg.appendChild(path);
  }
 }
 function render(){
  grid.innerHTML=manifest.stages.map(stage=>`<section class="fc-stage"><h3>${esc(stage['label_'+lang])}</h3><p>${esc(stage.period)}</p>${nodes.filter(n=>n.stage===stage.id).map(n=>`<button class="fc-node" type="button" data-node-key="${esc(n.key)}" aria-pressed="${n.key===selected}" ${query&&!norm(n['label_'+lang]+' '+n.registry_id+' '+n['summary_'+lang]+' '+(n.search_aliases||[]).join(' ')).includes(query)?'hidden':''}><strong>${esc(n['label_'+lang])}</strong><small>${esc(n.registry_id)} · ${esc(n.date)}</small><span>${esc(n['summary_'+lang])}</span></button>`).join('')}</section>`).join('');
  const related=visibleEdges();
  if(selected){const n=nodeMap.get(selected);detail.innerHTML=`<h3>${esc(n['label_'+lang])}</h3><p>${esc(n.registry_id)}</p><a href="${esc(local(n['route_'+lang]))}">${text('Open full source-controlled actor route','Abrir ruta completa con fuentes')}</a><p>${text('Incoming and outgoing edges are shown together, retaining each source grade and limit.','Se muestran juntos enlaces entrantes y salientes, conservando grado y límite de cada fuente.')}</p>`+related.map(edgeHTML).join('');}
  else detail.innerHTML=`<h3>${text('Select an actor or source node','Seleccione actor o nodo fuente')}</h3><p>${esc(manifest.reading_rule)}</p><p>${nodes.length} ${text('nodes','nodos')} · ${related.length} / ${edges.length} ${text('bridges in the selected grade','puentes en el grado seleccionado')}</p><p>${text('The full matrix below remains available without JavaScript. These grades are inherited from the controlled source; this renderer makes no new evidential finding.','La matriz completa permanece disponible sin JavaScript. Los grados proceden de la fuente controlada; el visor no formula un nuevo hallazgo.')}</p>`;
  app.querySelectorAll('[data-stat]').forEach(el=>el.textContent=String(el.dataset.stat==='TOTAL'?edges.length:edges.filter(e=>e.grade===el.dataset.stat).length));
  app.querySelectorAll('[data-grade-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.gradeFilter===grade)));
  requestAnimationFrame(draw);
 }
 grid.addEventListener('click',e=>{const button=e.target.closest('[data-node-key]');if(button){selected=selected===button.dataset.nodeKey?null:button.dataset.nodeKey;render();}});
 app.querySelectorAll('[data-grade-filter]').forEach(b=>b.addEventListener('click',()=>{grade=b.dataset.gradeFilter;render();}));
 app.querySelector('[data-graph-search]').addEventListener('input',e=>{query=norm(e.target.value).trim();render();});
 const play=app.querySelector('[data-play-spine]');
 function stop(){clearInterval(timer);timer=null;play.setAttribute('aria-pressed','false');}
 play.addEventListener('click',()=>{
  if(timer){stop();return;}
  function step(){selected=manifest.primary_spine[spineIndex++%manifest.primary_spine.length];grade='ALL';render();}
  step();if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  play.setAttribute('aria-pressed','true');timer=setInterval(()=>{if(spineIndex>=manifest.primary_spine.length){stop();return;}step();},2500);
 });
 app.querySelector('[data-clear-selection]').addEventListener('click',()=>{stop();selected=null;grade='ALL';query='';spineIndex=0;app.querySelector('[data-graph-search]').value='';render();});
 window.addEventListener('resize',draw);document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
 render();app.dataset.convergenceReady='true';
})();

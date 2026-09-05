/* Source-bound compatibility runtime. Renders existing evidence; never re-grades it. */
(() => {
  'use strict';
  const root = document.querySelector('[data-convergence-app]');
  if (!root) return;
  const lang = document.documentElement.lang.startsWith('es') ? 'es' : 'en';
  const t = (es, en) => lang === 'es' ? es : en;
  const local = value => typeof value === 'string' ? value : value && (value[lang] || value.en || value.es) || '';
  const field = (value, name) => local(value[name + '_' + lang] || value[name]);
  const key = n => String(n.key || n.id);
  const grade = e => String(e.grade || e.type || e.evidence_status || 'OPEN_NOT_LOCATED');
  const label = n => field(n, 'label') || field(n, 'name') || key(n);
  const el = (tag, text, cls) => { const n = document.createElement(tag); if (text) n.textContent = text; if (cls) n.className = cls; return n; };
  const url = value => {
    if (typeof value !== 'string' || !value || /^(javascript|data):/i.test(value)) return null;
    if (value.startsWith('//')) return null;
    if (/^https?:/i.test(value)) return value;
    if (value.startsWith('#')) return value;
    const path = value.replace(/^\/?por-derecho\//, '').replace(/^\//, '');
    if (!path.includes('/') && !/\.[a-z0-9]{2,6}(?:[?#]|$)/i.test(path)) return null;
    if (path.startsWith('.github/')) return 'https://github.com/sbu001monterecco/por-derecho/blob/main/' + path;
    return '/por-derecho/' + path;
  };
  const link = (text, value) => { const target = url(value); const a = el(target ? 'a' : 'span', text); if (target) a.href = target; return a; };
  const get = async value => { const r = await fetch(value, {credentials:'omit'}); if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); };
  const graphURL = new URL(root.dataset.graphUrl, location.href);
  const loadParts = async (g, name) => {
    if (Array.isArray(g[name])) return g[name];
    const parts = g[(name === 'nodes' ? 'node' : 'edge') + '_parts'] || [];
    return (await Promise.all(parts.map(async p => {
      const part = await get(new URL(p.path, graphURL));
      const rows = part[name] || part.records;
      if (!Array.isArray(rows) || (typeof p.count === 'number' && rows.length !== p.count)) throw new Error('Part/count mismatch');
      return rows;
    }))).flat();
  };
  const sourceLinks = (container, list, sourceMap) => {
    for (const item of list || []) {
      const s = typeof item === 'string' ? sourceMap.get(item) || {id:item, path:item} : item;
      const value = s.url || s.path || s.route || s.href;
      const title = field(s,'title') || s.label || s.id || String(item);
      container.append(link(local(title), value), document.createTextNode(' '));
    }
  };
  async function start() {
    const graph = await get(graphURL);
    const nodes = await loadParts(graph, 'nodes');
    const edges = await loadParts(graph, 'edges');
    if (!nodes.length || !edges.length) throw new Error('Empty source graph');
    const byKey = new Map(nodes.map(n => [key(n), n]));
    if (byKey.size !== nodes.length || edges.some(e => !byKey.has(String(e.from || e.source)) || !byKey.has(String(e.to || e.target)))) throw new Error('Duplicate node or orphan edge');
    const sources = Array.isArray(graph.sources) ? graph.sources : [];
    const sourceMap = new Map(sources.map(s => [s.id,s]));
    const typeSelect = root.querySelector('[data-fc-type]');
    const nodeSelect = root.querySelector('[data-fc-node]');
    const stats = root.querySelector('[data-fc-stats]');
    const all = t('Todos','All');
    if (typeSelect) {
      typeSelect.replaceChildren(new Option(all,'ALL'));
      for (const g of [...new Set(edges.map(grade))].sort()) typeSelect.add(new Option(field((graph.grades || {})[g] || {},'label') || g,g));
    }
    if (nodeSelect) {
      nodeSelect.replaceChildren(new Option(all,'ALL'));
      for (const n of nodes) nodeSelect.add(new Option(label(n),key(n)));
    }
    const table = root.querySelector('[data-fc-table]');
    const inspector = root.querySelector('[data-fc-inspector]');
    const describe = n => {
      if (!inspector) return;
      inspector.replaceChildren(el('h3',label(n)),el('p',n.registry_id || n.entity_id || ''),el('p',field(n,'summary') || field(n,'role')),el('p',n.date || n.period || ''));
      const route = n['route_' + lang] || (n.routes || {})[lang];
      if (route) inspector.append(link(t('Abrir registro documental','Open documentary record'),route));
    };
    const draw = () => {
      const selectedType = typeSelect ? typeSelect.value : 'ALL';
      const selectedNode = nodeSelect ? nodeSelect.value : 'ALL';
      const filtered = edges.filter(e => (selectedType === 'ALL' || grade(e) === selectedType) && (selectedNode === 'ALL' || [String(e.from || e.source),String(e.to || e.target)].includes(selectedNode)));
      if (stats) stats.textContent = `${nodes.length} ${t('nodos','nodes')} · ${filtered.length}/${edges.length} ${t('relaciones documentales','documentary relationships')}`;
      if (table) {
        const entries = filtered.map(e => {
          const row = el('article','', 'fc-evidence-row'); row.dataset.edgeId = String(e.id || '');
          const from = byKey.get(String(e.from || e.source)), to = byKey.get(String(e.to || e.target));
          row.append(el('h3',`${label(from)} → ${label(to)}`),el('p',`${e.id || ''} · ${grade(e)} · ${e.period || e.date || ''}`));
          for (const name of ['proposition','label','investigative_significance','limit','limitation','contrary','open_proof']) {
            const text = field(e,name); if (text) row.append(el('p',text));
          }
          const refs = el('p'); sourceLinks(refs,e.sources || e.source_ids || [],sourceMap); row.append(refs); return row;
        });
        table.replaceChildren(...entries);
      }
      const svg = root.querySelector('[data-fc-svg]');
      if (svg) {
        const ns = 'http://www.w3.org/2000/svg';
        const make = (tag,attrs,text) => { const e = document.createElementNS(ns,tag); for (const [k,v] of Object.entries(attrs)) e.setAttribute(k,String(v)); if (text) e.textContent=text; return e; };
        const positions = new Map(nodes.map((n,i) => [key(n),{x:90+(i%4)*330,y:65+Math.floor(i/4)*125}]));
        svg.setAttribute('viewBox',`0 0 1440 ${Math.ceil(nodes.length/4)*125+80}`);svg.replaceChildren();
        svg.append(make('title',{},t('Relaciones del registro; la dirección no acredita causalidad o culpabilidad','Registry relationships; direction does not establish causation or guilt')));
        for (const e of filtered) {
          const a = positions.get(String(e.from || e.source)), b = positions.get(String(e.to || e.target));
          const l = make('line',{x1:a.x+110,y1:a.y+28,x2:b.x+110,y2:b.y+28,'class':'fc-graph-edge'});
          l.append(make('title',{},`${e.id || ''} · ${grade(e)} · ${field(e,'proposition') || field(e,'label')}`));svg.append(l);
        }
        for (const n of nodes) {
          const p = positions.get(key(n));const group = make('g',{transform:`translate(${p.x},${p.y})`,tabindex:0,role:'button','aria-label':label(n),'data-node-id':key(n),'class':'fc-graph-node'});
          group.append(make('rect',{width:245,height:62,rx:8}),make('text',{x:10,y:25},label(n).slice(0,34)),make('text',{x:10,y:47,'class':'fc-node-id'},n.registry_id || n.entity_id || ''));
          group.addEventListener('click',()=>describe(n)); group.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();describe(n);}});svg.append(group);
        }
      }
      root.dataset.renderedNodes=String(nodes.length);root.dataset.renderedEdges=String(filtered.length);root.dataset.graphState='ready';
    };
    const groups = root.querySelector('[data-fc-groups]');
    if (groups) groups.replaceChildren(...(graph.groups || graph.stages || []).map(g=>el('p',field(g,'label') || field(g,'title') || g.id)));
    const conclusion=root.querySelector('[data-fc-convergence]');
    if (conclusion && graph.strongest_current_inference) conclusion.replaceChildren(el('p',local(graph.strongest_current_inference)));
    const sourcePanel=root.querySelector('[data-fc-sources]');
    if(sourcePanel){sourcePanel.replaceChildren();sourceLinks(sourcePanel,sources,sourceMap);sourcePanel.append(link(t('Registro de fuentes de la visualización','Visualization source registry'),'assets/data/acosta-matos-functional-convergence-map-v2.json'));}
    typeSelect?.addEventListener('change',draw);nodeSelect?.addEventListener('change',draw);
    root.querySelector('[data-fc-reset]')?.addEventListener('click',()=>{if(typeSelect)typeSelect.value='ALL';if(nodeSelect)nodeSelect.value='ALL';draw();});
    root.querySelector('[data-fc-export]')?.addEventListener('click',()=>{const blob=new Blob([JSON.stringify({graph_id:graph.graph_id,control_date:graph.control_date,reading_rule:graph.reading_rule,nodes,edges},null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='por-derecho-convergence-source.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);});
    draw();
  }
  start().catch(error=>{root.dataset.graphState='error';const panel=root.querySelector('[data-fc-stats]');if(panel)panel.textContent=t('No se pudo cargar el registro. Consulte la edición documental inferior.','The registry could not be loaded. Consult the documentary edition below.');console.error('Convergence source loading failed:',error.message);});
})();

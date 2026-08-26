(() => {
  'use strict';
  const root = document.querySelector('[data-identity-registry]');
  if (!root) return;

  const lang = root.dataset.lang === 'es' ? 'es' : 'en';
  const copy = lang === 'es' ? {
    loading: 'Cargando registro, acciones y grafo…',
    failure: 'No se pudo cargar el control operativo completo. Los JSON canónicos siguen disponibles mediante los enlaces de fuente.',
    showing: (shown,total) => `Mostrando ${shown} de ${total} identidades controladas.`,
    noResults: 'Ningún registro coincide con la búsqueda y los filtros actuales.',
    open: 'Abrir ficha →',
    graph: 'Abrir mapa →',
    actionHub: 'Abrir acciones →',
    aliases: 'Alias',
    legacy: 'Claves heredadas',
    distinctions: 'No confundir con',
    resolution: 'Resolución de identidad',
    actions: 'Acciones enlazadas',
    graphLinks: 'Grafo de convergencia',
    publicSurface: 'Superficie pública',
    unresolvedQuestion: 'Prueba de identidad pendiente',
    none: 'Ninguno',
    routeRegistry: 'ruta del registro',
    routeGraph: 'ruta del grafo',
    noRoute: 'Sin ficha pública',
    copyId: 'Copiar ID',
    copyLink: 'Copiar enlace directo',
    copied: 'Copiado',
    downloadJson: 'Exportar filtro JSON',
    downloadCsv: 'Exportar filtro CSV',
    filterLabels: {ALL:'todos',P0:'P0',ACTION:'acción',GRAPH:'grafo',UNRESOLVED:'identidad abierta',NO_ROUTE:'sin ficha',DISTINCTION:'distinción'},
    types: {ALL:'Todos',PERSON:'Persona',ORGANISATION:'Organización',STRUCTURE:'Estructura',INSTITUTION:'Institución',PROCEEDING:'Procedimiento'},
    roles: {recipient:'destinatario',actor:'actor',proceeding:'procedimiento'},
    statuses: {CANONICAL:'Canónica',CONTROLLED_PERIMETER_LABEL_EXACT_ENTITY_MAY_REQUIRE_SOURCE:'Entidad exacta abierta',REFERENCED_LEGAL_FORM_VARIANT_UNRESOLVED:'Forma jurídica abierta'},
    actionTitles: {
      'PD-SP-ACT-0001':'Corpus comunitario y voto de 2011','PD-SP-ACT-0002':'Mandatos y entregas profesionales','PD-SP-ACT-0003':'Nombramiento, independencia y conflicto del AC','PD-SP-ACT-0004':'Punto de conocimiento de 2016','PD-SP-ACT-0005':'Seguridad, acceso y llaves 2017–2018','PD-SP-ACT-0006':'Crédito, título, voto y pagos CAM','PD-SP-ACT-0007':'Salida financiada y valor de la masa','PD-SP-ACT-0008':'Locales y destino del precio','PD-SP-ACT-0009':'Ingresos hoteleros y control de activos','PD-SP-ACT-0010':'Diligencia del proyecto posterior','PD-SP-ACT-0011':'Expediente judicial y trazabilidad','PD-SP-ACT-0012':'Preservación fiscal y policial','PD-SP-ACT-0013':'Revisión profesional y de conflictos','PD-SP-ACT-0014':'Corrección y prueba adversa','PD-SP-ACT-0015':'Recuperación y daños por titular'
    }
  } : {
    loading: 'Loading registry, actions and graph…',
    failure: 'The complete operational control could not be loaded. The canonical JSON files remain available through the source links.',
    showing: (shown,total) => `Showing ${shown} of ${total} controlled identities.`,
    noResults: 'No record matches the current search and filters.',
    open: 'Open profile →',
    graph: 'Open map →',
    actionHub: 'Open actions →',
    aliases: 'Aliases',
    legacy: 'Legacy keys',
    distinctions: 'Not the same as',
    resolution: 'Identity resolution',
    actions: 'Linked actions',
    graphLinks: 'Convergence graph',
    publicSurface: 'Public surface',
    unresolvedQuestion: 'Outstanding identity proof',
    none: 'None',
    routeRegistry: 'registry route',
    routeGraph: 'graph route',
    noRoute: 'No public profile',
    copyId: 'Copy ID',
    copyLink: 'Copy direct link',
    copied: 'Copied',
    downloadJson: 'Export filtered JSON',
    downloadCsv: 'Export filtered CSV',
    filterLabels: {ALL:'all',P0:'P0',ACTION:'action',GRAPH:'graph',UNRESOLVED:'open identity',NO_ROUTE:'no profile',DISTINCTION:'distinction'},
    types: {ALL:'All',PERSON:'Person',ORGANISATION:'Organisation',STRUCTURE:'Structure',INSTITUTION:'Institution',PROCEEDING:'Proceeding'},
    roles: {recipient:'recipient',actor:'actor',proceeding:'proceeding'},
    statuses: {CANONICAL:'Canonical',CONTROLLED_PERIMETER_LABEL_EXACT_ENTITY_MAY_REQUIRE_SOURCE:'Exact entity open',REFERENCED_LEGAL_FORM_VARIANT_UNRESOLVED:'Legal-form variant open'},
    actionTitles: {}
  };

  const tableBody = root.querySelector('[data-registry-body]');
  const statusNode = root.querySelector('[data-registry-status]');
  const search = root.querySelector('[data-registry-search]');
  const typeButtons = [...root.querySelectorAll('[data-type-filter]')];
  const operationalButtons = [...root.querySelectorAll('[data-operational-filter]')];
  const typeStats = [...root.querySelectorAll('[data-registry-stat]')];
  const opStats = [...root.querySelectorAll('[data-op-stat]')];
  const dialog = root.querySelector('[data-identity-dialog]');
  const dialogBody = root.querySelector('[data-dialog-body]');
  const snackbar = root.querySelector('[data-snackbar]');
  const projectPrefix = location.pathname.includes('/por-derecho/') ? '/por-derecho' : '';

  let records = [];
  let registryIndex = null;
  let actionMatrix = null;
  let graph = null;
  let operational = null;
  let activeType = 'ALL';
  let activeOperational = 'ALL';
  let lastShown = [];

  const normalise = value => String(value || '')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();

  const absoluteRoute = route => {
    if (!route) return null;
    if (/^https?:\/\//i.test(route)) return route;
    return `${projectPrefix}${route.startsWith('/') ? route : `/${route}`}`;
  };

  const fetchJson = async (value, base = document.baseURI) => {
    const url = new URL(value, base);
    const response = await fetch(url, {cache:'no-store'});
    if (!response.ok) throw new Error(`${url.pathname} ${response.status}`);
    return {url, data: await response.json()};
  };

  const loadGraph = async value => {
    const indexResult = await fetchJson(value);
    const index = indexResult.data;
    const nodeParts = await Promise.all((index.node_parts || []).map(part => fetchJson(part.path, indexResult.url)));
    const edgeParts = await Promise.all((index.edge_parts || []).map(part => fetchJson(part.path, indexResult.url)));
    const nodes = nodeParts.flatMap(result => result.data.nodes || []);
    const edges = edgeParts.flatMap(result => result.data.edges || []);
    return {index, nodes, edges};
  };

  const actionTitle = action => copy.actionTitles[action.action_id] || action.title || action.action_id;

  function buildOperationalRecords(baseRecords) {
    const byId = new Map(baseRecords.map(record => [record.id, record]));
    const actionMap = new Map();
    const unresolvedMap = new Map([
      ...(operational.exact_identity_queue || []),
      ...(operational.proceeding_identity_queue || [])
    ].map(item => [item.id, item]));
    const nodeByKey = new Map((graph.nodes || []).map(node => [node.key, node]));
    const graphMap = new Map();

    const addAction = (id, action, role) => {
      if (!byId.has(id)) return;
      const bucket = actionMap.get(id) || new Map();
      const existing = bucket.get(action.action_id) || {
        action_id: action.action_id,
        priority: action.priority,
        status: action.status,
        title: actionTitle(action),
        roles: []
      };
      if (!existing.roles.includes(role)) existing.roles.push(role);
      bucket.set(action.action_id, existing);
      actionMap.set(id, bucket);
    };

    for (const action of actionMatrix.actions || []) {
      for (const id of action.recipients || []) addAction(id, action, 'recipient');
      for (const id of action.actors || []) addAction(id, action, 'actor');
      for (const id of action.proceedings || []) addAction(id, action, 'proceeding');
    }

    const addGraph = (id, kind, value) => {
      if (!id || !byId.has(id)) return;
      const bucket = graphMap.get(id) || {nodes:[], edges:[]};
      if (kind === 'node') bucket.nodes.push(value);
      else bucket.edges.push(value);
      graphMap.set(id, bucket);
    };

    for (const node of graph.nodes || []) addGraph(node.registry_id, 'node', node);
    for (const edge of graph.edges || []) {
      const from = nodeByKey.get(edge.from);
      const to = nodeByKey.get(edge.to);
      addGraph(from?.registry_id, 'edge', {...edge, direction:'out', counterpart_id:to?.registry_id});
      addGraph(to?.registry_id, 'edge', {...edge, direction:'in', counterpart_id:from?.registry_id});
    }

    return baseRecords.map(record => {
      const actions = [...(actionMap.get(record.id)?.values() || [])]
        .sort((a,b) => (a.priority === b.priority ? a.action_id.localeCompare(b.action_id) : a.priority.localeCompare(b.priority)));
      const graphInfo = graphMap.get(record.id) || {nodes:[], edges:[]};
      const registryRoute = record.routes && (record.routes[lang] || record.routes.en || record.routes.es);
      const graphNode = graphInfo.nodes.find(node => node[`route_${lang}`] || node.route_en || node.route_es);
      const graphRoute = graphNode && (graphNode[`route_${lang}`] || graphNode.route_en || graphNode.route_es);
      const route = registryRoute || graphRoute || null;
      const routeSource = registryRoute ? 'registry' : graphRoute ? 'graph' : null;
      const resolutionKey = record.identity_resolution || record.status || 'CANONICAL';
      const unresolved = !['CANONICAL', 'CARET_CONFIRMED'].includes(resolutionKey);
      const p0 = actions.some(action => action.priority === 'P0');
      const distinction = Boolean(record.not_same_as?.length);
      const openQuestion = unresolvedMap.get(record.id) || null;
      const searchText = normalise([
        record.id, record.name, record.type, resolutionKey,
        ...(record.aliases || []), ...(record.legacy || []), ...(record.not_same_as || []),
        ...actions.flatMap(action => [action.action_id, action.title, ...action.roles]),
        ...graphInfo.nodes.flatMap(node => [node.key,node.label_es,node.label_en,node.summary_es,node.summary_en]),
        ...graphInfo.edges.flatMap(edge => [edge.id,edge.grade,edge.proposition?.es,edge.proposition?.en]),
        openQuestion?.question_es, openQuestion?.question_en
      ].join(' '));
      return {
        ...record,
        _actions: actions,
        _graph: graphInfo,
        _route: route,
        _routeSource: routeSource,
        _resolutionKey: resolutionKey,
        _unresolved: unresolved,
        _p0: p0,
        _actionLinked: actions.length > 0,
        _graphLinked: graphInfo.nodes.length > 0 || graphInfo.edges.length > 0,
        _distinction: distinction,
        _openQuestion: openQuestion,
        _search: searchText
      };
    });
  }

  const statValue = key => {
    const values = {
      TOTAL: records.length,
      ACTION_LINKED: records.filter(r => r._actionLinked).length,
      P0_LINKED: records.filter(r => r._p0).length,
      GRAPH_LINKED: records.filter(r => r._graphLinked).length,
      UNRESOLVED: records.filter(r => r._unresolved).length,
      WITH_ROUTE: records.filter(r => r._route).length,
      WITHOUT_ROUTE: records.filter(r => !r._route).length,
      DISTINCTIONS: records.filter(r => r._distinction).length
    };
    if (key === 'P0_ROUTE_COVERAGE') {
      const p0 = records.filter(r => r._p0);
      return `${p0.filter(r => r._route).length}/${p0.length}`;
    }
    return values[key] ?? 0;
  };

  function renderStats() {
    const values = {TOTAL:registryIndex.counts?.total || records.length, ...(registryIndex.counts || {})};
    typeStats.forEach(node => {
      const key = node.dataset.registryStat;
      node.textContent = values[key] ?? records.filter(record => record.type === key).length;
    });
    opStats.forEach(node => { node.textContent = statValue(node.dataset.opStat); });

    const totalPercent = records.length ? Math.round((records.filter(r => r._route).length / records.length) * 100) : 0;
    const p0Records = records.filter(r => r._p0);
    const p0Percent = p0Records.length ? Math.round((p0Records.filter(r => r._route).length / p0Records.length) * 100) : 0;
    root.querySelectorAll('[data-route-percent]').forEach(node => node.textContent = `${totalPercent}%`);
    root.querySelectorAll('[data-route-progress]').forEach(node => node.style.width = `${totalPercent}%`);
    root.querySelectorAll('[data-p0-route-percent]').forEach(node => node.textContent = `${p0Percent}%`);
    root.querySelectorAll('[data-p0-route-progress]').forEach(node => node.style.width = `${p0Percent}%`);
  }

  const resolutionLabel = record => {
    const configured = operational.resolution_statuses?.[record._resolutionKey];
    return configured?.[`label_${lang}`] || copy.statuses[record._resolutionKey] || record._resolutionKey;
  };

  function makeBadge(text, className) {
    const span = document.createElement('span');
    span.className = `id-badge ${className}`;
    span.textContent = text;
    return span;
  }

  function showSnackbar(message = copy.copied) {
    if (!snackbar) return;
    snackbar.textContent = message;
    snackbar.classList.add('show');
    clearTimeout(showSnackbar.timer);
    showSnackbar.timer = setTimeout(() => snackbar.classList.remove('show'), 1400);
  }

  async function copyText(text) {
    try { await navigator.clipboard.writeText(text); }
    catch {
      const area = document.createElement('textarea');
      area.value = text; area.style.position = 'fixed'; area.style.opacity = '0';
      document.body.appendChild(area); area.select(); document.execCommand('copy'); area.remove();
    }
    showSnackbar();
  }

  const currentFilterLabel = () => {
    const parts = [];
    if (activeType !== 'ALL') parts.push(copy.types[activeType] || activeType);
    if (activeOperational !== 'ALL') parts.push(copy.filterLabels[activeOperational] || activeOperational);
    return parts.length ? ` · ${parts.join(' / ')}` : '';
  };

  function recordPasses(record, query) {
    if (activeType !== 'ALL' && record.type !== activeType) return false;
    if (activeOperational === 'P0' && !record._p0) return false;
    if (activeOperational === 'ACTION' && !record._actionLinked) return false;
    if (activeOperational === 'GRAPH' && !record._graphLinked) return false;
    if (activeOperational === 'UNRESOLVED' && !record._unresolved) return false;
    if (activeOperational === 'NO_ROUTE' && record._route) return false;
    if (activeOperational === 'DISTINCTION' && !record._distinction) return false;
    return !query || record._search.includes(query);
  }

  function sortedFilteredRecords() {
    const query = normalise(search?.value || '');
    return records.filter(record => recordPasses(record, query)).sort((a,b) => {
      const priorityA = Number(a._p0) * 8 + Number(a._unresolved) * 4 + Number(a._actionLinked) * 2 + Number(a._graphLinked);
      const priorityB = Number(b._p0) * 8 + Number(b._unresolved) * 4 + Number(b._actionLinked) * 2 + Number(b._graphLinked);
      return priorityB - priorityA || a.type.localeCompare(b.type) || a.name.localeCompare(b.name, lang, {sensitivity:'base'});
    });
  }

  function makeCell(row, className) {
    const td = document.createElement('td');
    if (className) td.className = className;
    row.appendChild(td);
    return td;
  }

  function openRecord(id, updateHash = true) {
    const record = records.find(item => item.id === id);
    if (!record || !dialog || !dialogBody) return;
    if (updateHash) history.replaceState(null, '', `#${encodeURIComponent(record.id)}`);
    renderDialog(record);
    if (typeof dialog.showModal === 'function') dialog.showModal(); else dialog.setAttribute('open','');
  }

  function renderTable() {
    const shown = sortedFilteredRecords();
    lastShown = shown;
    tableBody.replaceChildren();
    if (!shown.length) {
      const row = document.createElement('tr');
      const cell = makeCell(row, 'id-empty');
      cell.colSpan = 7;
      cell.textContent = copy.noResults;
      tableBody.appendChild(row);
    } else {
      for (const record of shown) {
        const row = document.createElement('tr');
        row.id = record.id;
        row.dataset.identityId = record.id;

        const idCell = makeCell(row, 'id-code');
        const copyButton = document.createElement('button');
        copyButton.className = 'id-copy';
        copyButton.type = 'button';
        copyButton.textContent = record.id;
        copyButton.title = copy.copyId;
        copyButton.addEventListener('click', () => copyText(record.id));
        idCell.appendChild(copyButton);

        const nameCell = makeCell(row, 'id-name');
        const nameButton = document.createElement('button');
        nameButton.type = 'button';
        nameButton.className = 'id-name-button';
        const strong = document.createElement('strong');
        strong.textContent = record.name;
        nameButton.appendChild(strong);
        nameButton.addEventListener('click', () => openRecord(record.id));
        nameCell.appendChild(nameButton);
        if (record.aliases?.length) {
          const aliases = document.createElement('span');
          aliases.className = 'id-aliases';
          aliases.textContent = `${copy.aliases}: ${record.aliases.join(' · ')}`;
          nameCell.appendChild(aliases);
        }

        const typeCell = makeCell(row);
        const typeBadge = document.createElement('span');
        typeBadge.className = 'id-type';
        typeBadge.textContent = copy.types[record.type] || record.type;
        typeCell.appendChild(typeBadge);

        const stateCell = makeCell(row);
        stateCell.appendChild(makeBadge(resolutionLabel(record), record._unresolved ? 'unresolved' : 'canonical'));
        if (record._p0) stateCell.appendChild(makeBadge('P0','p0'));
        else if (record._actionLinked) stateCell.appendChild(makeBadge(lang === 'es' ? 'Acción' : 'Action','action'));
        if (record._graphLinked) stateCell.appendChild(makeBadge(lang === 'es' ? 'Grafo' : 'Graph','graph'));
        if (!record._route) stateCell.appendChild(makeBadge(lang === 'es' ? 'Sin ficha' : 'No profile','no-route'));
        if (record._distinction) stateCell.appendChild(makeBadge(lang === 'es' ? 'Distinción' : 'Distinction','distinction'));

        const actionCell = makeCell(row);
        if (!record._actions.length) actionCell.textContent = '—';
        else {
          record._actions.slice(0,3).forEach(action => {
            const link = document.createElement('a');
            link.className = `id-action-chip ${action.priority === 'P0' ? 'p0' : ''}`;
            link.href = root.dataset.actionPage;
            link.textContent = action.action_id;
            link.title = `${action.title} · ${action.roles.map(role => copy.roles[role] || role).join(', ')}`;
            actionCell.appendChild(link);
          });
          if (record._actions.length > 3) {
            const more = document.createElement('span');
            more.className = 'id-muted';
            more.textContent = `+${record._actions.length - 3}`;
            actionCell.appendChild(more);
          }
        }

        const graphCell = makeCell(row);
        if (!record._graphLinked) graphCell.textContent = '—';
        else {
          const link = document.createElement('a');
          link.className = 'id-graph-chip';
          link.href = root.dataset.graphPage;
          link.textContent = `${record._graph.nodes.length}N · ${record._graph.edges.length}E`;
          link.title = copy.graph;
          graphCell.appendChild(link);
        }

        const routeCell = makeCell(row, 'id-route');
        if (record._route) {
          const link = document.createElement('a');
          link.href = absoluteRoute(record._route);
          link.textContent = copy.open;
          routeCell.appendChild(link);
          const source = document.createElement('span');
          source.className = 'id-route-source';
          source.textContent = record._routeSource === 'registry' ? copy.routeRegistry : copy.routeGraph;
          routeCell.appendChild(source);
        } else {
          routeCell.appendChild(makeBadge(copy.noRoute,'no-route'));
        }
        tableBody.appendChild(row);
      }
    }
    statusNode.textContent = `${copy.showing(shown.length, records.length)}${currentFilterLabel()}`;
  }

  function renderDialog(record) {
    dialogBody.replaceChildren();
    const header = document.createElement('div');
    header.className = 'id-dialog-header';
    const heading = document.createElement('div');
    const eyebrow = document.createElement('p');
    eyebrow.className = 'id-kicker'; eyebrow.textContent = record.id;
    const title = document.createElement('h2'); title.textContent = record.name;
    heading.append(eyebrow,title);
    const close = document.createElement('button');
    close.className = 'id-dialog-close'; close.type = 'button'; close.setAttribute('aria-label', lang === 'es' ? 'Cerrar' : 'Close'); close.textContent = '×';
    close.addEventListener('click', () => dialog.close());
    header.append(heading,close);
    dialogBody.appendChild(header);

    const grid = document.createElement('div');
    grid.className = 'id-dialog-grid';

    const addCard = (titleText, contents) => {
      const card = document.createElement('section'); card.className = 'id-dialog-card';
      const h = document.createElement('h3'); h.textContent = titleText; card.appendChild(h);
      card.appendChild(contents); grid.appendChild(card);
    };

    const identityList = document.createElement('ul'); identityList.className = 'id-dialog-list';
    const fields = [
      [copy.resolution, resolutionLabel(record)],
      [copy.aliases, record.aliases?.join(' · ') || copy.none],
      [copy.legacy, record.legacy?.join(' · ') || copy.none]
    ];
    fields.forEach(([label,value]) => { const li = document.createElement('li'); li.innerHTML = `<strong>${label}:</strong> `; li.append(document.createTextNode(value)); identityList.appendChild(li); });
    if (record.not_same_as?.length) {
      const li = document.createElement('li'); li.innerHTML = `<strong>${copy.distinctions}:</strong> `;
      li.append(document.createTextNode(record.not_same_as.map(id => records.find(r => r.id === id)?.name || id).join(' · ')));
      identityList.appendChild(li);
    }
    if (record._openQuestion) {
      const li = document.createElement('li'); li.innerHTML = `<strong>${copy.unresolvedQuestion}:</strong> `;
      li.append(document.createTextNode(record._openQuestion[`question_${lang}`] || record._openQuestion.question_en || ''));
      identityList.appendChild(li);
    }
    addCard(lang === 'es' ? 'Control de identidad' : 'Identity control', identityList);

    const actionList = document.createElement('ul'); actionList.className = 'id-dialog-list';
    if (!record._actions.length) { const li = document.createElement('li'); li.textContent = copy.none; actionList.appendChild(li); }
    else record._actions.forEach(action => {
      const li = document.createElement('li');
      const a = document.createElement('a'); a.href = root.dataset.actionPage; a.textContent = `${action.action_id} · ${action.title}`;
      li.appendChild(a);
      li.append(document.createTextNode(` — ${action.priority}; ${action.roles.map(role => copy.roles[role] || role).join(', ')}`));
      actionList.appendChild(li);
    });
    addCard(copy.actions, actionList);

    const graphList = document.createElement('ul'); graphList.className = 'id-dialog-list';
    if (!record._graphLinked) { const li = document.createElement('li'); li.textContent = copy.none; graphList.appendChild(li); }
    else {
      record._graph.nodes.forEach(node => { const li = document.createElement('li'); li.textContent = `${node.key} · ${node.date || ''} · ${node[`summary_${lang}`] || node.summary_en || ''}`; graphList.appendChild(li); });
      record._graph.edges.slice(0,12).forEach(edge => {
        const counterpart = records.find(r => r.id === edge.counterpart_id)?.name || edge.counterpart_id || '';
        const li = document.createElement('li');
        li.textContent = `${edge.id} · ${edge.grade} · ${counterpart}: ${edge.proposition?.[lang] || edge.proposition?.en || ''}`;
        graphList.appendChild(li);
      });
    }
    addCard(copy.graphLinks, graphList);

    const routeList = document.createElement('ul'); routeList.className = 'id-dialog-list';
    if (record._route) {
      const li = document.createElement('li'); const a = document.createElement('a'); a.href = absoluteRoute(record._route); a.textContent = copy.open; li.appendChild(a); routeList.appendChild(li);
    } else { const li = document.createElement('li'); li.textContent = copy.noRoute; routeList.appendChild(li); }
    addCard(copy.publicSurface, routeList);

    dialogBody.appendChild(grid);
    const actions = document.createElement('div'); actions.className = 'id-dialog-actions';
    const copyIdButton = document.createElement('button'); copyIdButton.type='button'; copyIdButton.textContent=copy.copyId; copyIdButton.addEventListener('click',()=>copyText(record.id));
    const copyLinkButton = document.createElement('button'); copyLinkButton.type='button'; copyLinkButton.textContent=copy.copyLink; copyLinkButton.addEventListener('click',()=>copyText(`${location.origin}${location.pathname}#${record.id}`));
    actions.append(copyIdButton,copyLinkButton);
    if (record._route) { const routeLink = document.createElement('a'); routeLink.className='primary'; routeLink.href=absoluteRoute(record._route); routeLink.textContent=copy.open; actions.appendChild(routeLink); }
    if (record._graphLinked) { const graphLink = document.createElement('a'); graphLink.href=root.dataset.graphPage; graphLink.textContent=copy.graph; actions.appendChild(graphLink); }
    dialogBody.appendChild(actions);
  }

  function setOperationalFilter(value) {
    activeOperational = value;
    operationalButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.operationalFilter === value)));
    renderTable();
  }

  function renderQueue(selector, items, metaFor) {
    const list = root.querySelector(`[data-queue-list="${selector}"]`);
    const count = root.querySelector(`[data-queue-count="${selector}"]`);
    if (!list || !count) return;
    count.textContent = items.length;
    list.replaceChildren();
    items.slice(0,16).forEach(item => {
      const record = item.record || item;
      const button = document.createElement('button'); button.type='button'; button.className='id-queue-item';
      const code = document.createElement('code'); code.textContent=record.id;
      const name = document.createElement('span'); name.textContent=record.name;
      const meta = document.createElement('small'); meta.textContent=metaFor(item,record);
      button.append(code,name,meta); button.addEventListener('click',()=>openRecord(record.id)); list.appendChild(button);
    });
  }

  function renderQueues() {
    const p0 = records.filter(r => r._p0).sort((a,b)=>b._actions.length-a._actions.length || a.name.localeCompare(b.name,lang));
    renderQueue('p0',p0,(_,r)=>`${r._actions.filter(a=>a.priority==='P0').length} P0`);

    const unresolved = (operational.exact_identity_queue || []).map(item => ({...item,record:records.find(r=>r.id===item.id)})).filter(item=>item.record);
    renderQueue('unresolved',unresolved,(item)=>item.priority);

    const noRoute = records.filter(r=>!r._route).sort((a,b)=>Number(b._p0)-Number(a._p0) || Number(b._actionLinked)-Number(a._actionLinked) || a.name.localeCompare(b.name,lang));
    renderQueue('no-route',noRoute,(_,r)=>r._p0?'P0':r._actionLinked?(lang==='es'?'acción':'action'):r.type);

    const distinctions = records.filter(r=>r._distinction).sort((a,b)=>a.name.localeCompare(b.name,lang));
    renderQueue('distinction',distinctions,(_,r)=>`${r.not_same_as.length} ≠`);
  }

  function renderOperationalActions() {
    const target = root.querySelector('[data-registry-action-list]');
    if (!target) return;
    target.replaceChildren();
    (operational.actions || []).forEach(action => {
      const card = document.createElement('article'); card.className='id-action-card';
      const header = document.createElement('header');
      const code = document.createElement('code'); code.textContent=action.action_id;
      const priority = document.createElement('span'); priority.className=`id-priority ${action.priority.toLowerCase()}`; priority.textContent=action.priority;
      header.append(code,priority);
      const h = document.createElement('h3'); h.textContent=action[`title_${lang}`] || action.title_en;
      const p = document.createElement('p'); p.textContent=action[`description_${lang}`] || action.description_en;
      card.append(header,h,p); target.appendChild(card);
    });
  }

  function renderExtensions() {
    const target = root.querySelector('[data-extension-list]');
    if (!target) return;
    target.replaceChildren();
    (operational.extension_namespaces || []).forEach(namespace => {
      const card = document.createElement('article'); card.className='id-extension';
      const code = document.createElement('code'); code.textContent=namespace.pattern;
      const strong = document.createElement('strong'); strong.textContent=namespace.type;
      const small = document.createElement('small'); small.textContent=namespace[`purpose_${lang}`] || namespace.purpose_en;
      card.append(code,strong,small); target.appendChild(card);
    });
  }

  function exportRecords(format) {
    const rows = lastShown.map(record => ({
      id: record.id,
      name: record.name,
      type: record.type,
      aliases: record.aliases || [],
      resolution_status: record._resolutionKey,
      p0: record._p0,
      actions: record._actions.map(action => action.action_id),
      graph_nodes: record._graph.nodes.map(node => node.key),
      graph_edges: record._graph.edges.map(edge => edge.id),
      public_route: record._route || null,
      not_same_as: record.not_same_as || []
    }));
    let body, mime, extension;
    if (format === 'csv') {
      const headers = ['id','name','type','resolution_status','p0','actions','graph_nodes','graph_edges','public_route','aliases','not_same_as'];
      const quote = value => `"${String(value ?? '').replace(/"/g,'""')}"`;
      body = [headers.join(','),...rows.map(row=>headers.map(key=>quote(Array.isArray(row[key])?row[key].join('|'):row[key])).join(','))].join('\n');
      mime='text/csv;charset=utf-8'; extension='csv';
    } else {
      body=JSON.stringify({registry_id:registryIndex.registry_id,operational_control:operational.control_id,filters:{type:activeType,operational:activeOperational,query:search?.value||''},records:rows},null,2);
      mime='application/json;charset=utf-8'; extension='json';
    }
    const blob = new Blob([body],{type:mime}); const url=URL.createObjectURL(blob); const a=document.createElement('a');
    a.href=url; a.download=`matter-identity-registry-filter-${new Date().toISOString().slice(0,10)}.${extension}`; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(url),1000);
  }

  typeButtons.forEach(button => button.addEventListener('click', () => {
    activeType = button.dataset.typeFilter;
    typeButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    renderTable();
  }));
  operationalButtons.forEach(button => button.addEventListener('click', () => setOperationalFilter(button.dataset.operationalFilter)));
  root.querySelectorAll('[data-queue-filter]').forEach(button => button.addEventListener('click',()=>setOperationalFilter(button.dataset.queueFilter)));
  root.querySelector('[data-export-json]')?.addEventListener('click',()=>exportRecords('json'));
  root.querySelector('[data-export-csv]')?.addEventListener('click',()=>exportRecords('csv'));
  search?.addEventListener('input',renderTable);
  dialog?.addEventListener('close',()=>{ if (location.hash && /^#PD-SP-/.test(location.hash)) history.replaceState(null,'',location.pathname+location.search); });

  async function load() {
    statusNode.textContent = copy.loading;
    try {
      const registryResult = await fetchJson(root.dataset.indexUrl);
      registryIndex = registryResult.data;
      const [partResults,actionResult,graphResult,operationalResult] = await Promise.all([
        Promise.all((registryIndex.parts || []).map(part=>fetchJson(part.path,registryResult.url))),
        fetchJson(root.dataset.actionsUrl),
        loadGraph(root.dataset.graphUrl),
        fetchJson(root.dataset.operationalUrl)
      ]);
      actionMatrix = actionResult.data;
      graph = graphResult;
      operational = operationalResult.data;
      const baseRecords = partResults.flatMap(result=>result.data.records || []);
      records = buildOperationalRecords(baseRecords);
      renderStats(); renderQueues(); renderOperationalActions(); renderExtensions(); renderTable();
      const requested = decodeURIComponent(location.hash.replace(/^#/,''));
      if (requested && records.some(record=>record.id===requested)) setTimeout(()=>openRecord(requested,false),80);
    } catch (error) {
      console.error('Matter identity operational registry load failed',error);
      statusNode.textContent = copy.failure;
      statusNode.classList.add('id-error');
      tableBody.replaceChildren();
    }
  }

  window.addEventListener('hashchange',()=>{
    const requested=decodeURIComponent(location.hash.replace(/^#/,''));
    if (requested && records.some(record=>record.id===requested)) openRecord(requested,false);
  });
  load();
})();

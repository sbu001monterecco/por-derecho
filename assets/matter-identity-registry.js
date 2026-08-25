(() => {
  'use strict';
  const root = document.querySelector('[data-identity-registry]');
  if (!root) return;

  const lang = root.dataset.lang === 'es' ? 'es' : 'en';
  const copy = lang === 'es' ? {
    loading: 'Cargando registro canónico…',
    failure: 'No se pudo cargar el registro. El JSON canónico permanece disponible mediante el enlace de fuente.',
    showing: (shown,total) => `Mostrando ${shown} de ${total} identidades controladas.`,
    noResults: 'Ningún registro coincide con la búsqueda y el filtro actuales.',
    open: 'Abrir ficha →',
    aliases: 'Alias',
    types: {ALL:'Todos',PERSON:'Persona',ORGANISATION:'Organización',STRUCTURE:'Estructura',INSTITUTION:'Institución',PROCEEDING:'Procedimiento'}
  } : {
    loading: 'Loading canonical registry…',
    failure: 'The registry could not be loaded. The canonical JSON remains available through the source link.',
    showing: (shown,total) => `Showing ${shown} of ${total} controlled identities.`,
    noResults: 'No record matches the current search and filter.',
    open: 'Open profile →',
    aliases: 'Aliases',
    types: {ALL:'All',PERSON:'Person',ORGANISATION:'Organisation',STRUCTURE:'Structure',INSTITUTION:'Institution',PROCEEDING:'Proceeding'}
  };

  const tableBody = root.querySelector('[data-registry-body]');
  const status = root.querySelector('[data-registry-status]');
  const search = root.querySelector('[data-registry-search]');
  const filterButtons = [...root.querySelectorAll('[data-type-filter]')];
  const statNodes = [...root.querySelectorAll('[data-registry-stat]')];
  let records = [];
  let activeType = 'ALL';

  const normalise = value => String(value || '')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();

  const projectPrefix = location.pathname.includes('/por-derecho/') ? '/por-derecho' : '';
  const routeFor = record => {
    const route = record.routes && (record.routes[lang] || record.routes.en || record.routes.es);
    if (!route) return null;
    if (/^https?:\/\//i.test(route)) return route;
    return `${projectPrefix}${route.startsWith('/') ? route : `/${route}`}`;
  };

  const textIndex = record => normalise([
    record.id, record.name, record.type,
    ...(record.aliases || []), ...(record.legacy || []),
    ...(record.not_same_as || [])
  ].join(' '));

  function renderStats(index) {
    const values = {TOTAL:index.counts?.total || records.length, ...(index.counts || {})};
    statNodes.forEach(node => {
      const key = node.dataset.registryStat;
      node.textContent = values[key] ?? records.filter(r => r.type === key).length;
    });
  }

  function makeCell(row, className, text) {
    const td = document.createElement('td');
    if (className) td.className = className;
    if (text !== undefined) td.textContent = text;
    row.appendChild(td);
    return td;
  }

  function render() {
    const query = normalise(search?.value || '');
    const shown = records.filter(record => {
      if (activeType !== 'ALL' && record.type !== activeType) return false;
      return !query || record._search.includes(query);
    });

    tableBody.replaceChildren();
    if (!shown.length) {
      const row = document.createElement('tr');
      const cell = makeCell(row, 'id-empty', copy.noResults);
      cell.colSpan = 5;
      tableBody.appendChild(row);
    } else {
      shown.forEach(record => {
        const row = document.createElement('tr');
        makeCell(row, 'id-code', record.id);

        const nameCell = makeCell(row, 'id-name');
        const strong = document.createElement('strong');
        strong.textContent = record.name;
        nameCell.appendChild(strong);
        if (record.aliases?.length) {
          const aliases = document.createElement('span');
          aliases.className = 'id-aliases';
          aliases.textContent = `${copy.aliases}: ${record.aliases.join(' · ')}`;
          nameCell.appendChild(aliases);
        }

        const typeCell = makeCell(row);
        const badge = document.createElement('span');
        badge.className = 'id-type';
        badge.textContent = copy.types[record.type] || record.type;
        typeCell.appendChild(badge);

        makeCell(row, 'id-aliases', (record.legacy || []).join(' · ') || '—');

        const routeCell = makeCell(row, 'id-route');
        const route = routeFor(record);
        if (route) {
          const link = document.createElement('a');
          link.href = route;
          link.textContent = copy.open;
          routeCell.appendChild(link);
        } else {
          routeCell.textContent = '—';
        }
        tableBody.appendChild(row);
      });
    }
    status.textContent = copy.showing(shown.length, records.length);
  }

  filterButtons.forEach(button => button.addEventListener('click', () => {
    activeType = button.dataset.typeFilter;
    filterButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    render();
  }));
  search?.addEventListener('input', render);

  async function load() {
    status.textContent = copy.loading;
    try {
      const indexURL = new URL(root.dataset.indexUrl, document.baseURI);
      const indexResponse = await fetch(indexURL, {cache:'no-store'});
      if (!indexResponse.ok) throw new Error(`index ${indexResponse.status}`);
      const index = await indexResponse.json();
      const parts = await Promise.all((index.parts || []).map(async part => {
        const response = await fetch(new URL(part.path, indexURL), {cache:'no-store'});
        if (!response.ok) throw new Error(`${part.path} ${response.status}`);
        return response.json();
      }));
      records = parts.flatMap(part => part.records || [])
        .map(record => ({...record, _search:textIndex(record)}))
        .sort((a,b) => a.type.localeCompare(b.type) || a.name.localeCompare(b.name, lang, {sensitivity:'base'}));
      renderStats(index);
      render();
    } catch (error) {
      console.error('Matter identity registry load failed', error);
      status.textContent = copy.failure;
      status.classList.add('id-error');
      tableBody.replaceChildren();
    }
  }

  load();
})();
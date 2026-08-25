(() => {
  'use strict';
  const root = document.querySelector('[data-spanish-professional-register]');
  if (!root) return;

  const lang = root.dataset.lang === 'es' ? 'es' : 'en';
  const copy = lang === 'es' ? {
    loading: 'Cargando el registro profesional y de participantes…',
    failure: 'No se pudo cargar el registro controlado. El JSON canónico permanece disponible en la sección de fuentes.',
    showing: (shown,total) => `Mostrando ${shown} de ${total} personas clasificadas.`,
    noResults: 'Ninguna persona coincide con la búsqueda y el filtro actuales.',
    firm: 'Firma / perímetro', period: 'Periodo', limit: 'Límite de atribución',
    categories: {
      ALL:'Todo', CURRENT_SPANISH_COUNSEL:'Abogados actuales', FORMER_SPANISH_COUNSEL:'Abogados anteriores',
      SPANISH_LEGAL_CONTACT_SCOPE_REVIEW:'Alcance por revisar', PROCURADOR:'Procuradores', OTHER_LAWYER_IN_MATTER:'Otros abogados',
      REPRESENTATIVE_IN_MATTER:'Representantes', OTHER_PROFESSIONAL_ADVISER:'Otros asesores', HOTEL_RECOVERY_PROFESSIONAL:'Salida / hotel',
      COMMUNITY_ORGAN_ACTOR:'Órgano comunitario', HISTORICAL_OWNER_COMMUNITY_PARTICIPANT:'Propietarios / Comunidad',
      LATER_CORPORATE_PROJECT_OFFICER:'Actores corporativos posteriores', HISTORICAL_CORPORATE_OFFICER:'Cargo corporativo histórico'
    }
  } : {
    loading: 'Loading the professional and participant register…',
    failure: 'The controlled register could not be loaded. The canonical JSON remains available in the source section.',
    showing: (shown,total) => `Showing ${shown} of ${total} classified people.`,
    noResults: 'No person matches the current search and filter.',
    firm: 'Firm / perimeter', period: 'Period', limit: 'Attribution boundary',
    categories: {
      ALL:'All', CURRENT_SPANISH_COUNSEL:'Current counsel', FORMER_SPANISH_COUNSEL:'Former counsel',
      SPANISH_LEGAL_CONTACT_SCOPE_REVIEW:'Scope review', PROCURADOR:'Procuradores', OTHER_LAWYER_IN_MATTER:'Other lawyers',
      REPRESENTATIVE_IN_MATTER:'Representatives', OTHER_PROFESSIONAL_ADVISER:'Other advisers', HOTEL_RECOVERY_PROFESSIONAL:'Exit / hotel',
      COMMUNITY_ORGAN_ACTOR:'Community organ', HISTORICAL_OWNER_COMMUNITY_PARTICIPANT:'Owners / Community',
      LATER_CORPORATE_PROJECT_OFFICER:'Later corporate actors', HISTORICAL_CORPORATE_OFFICER:'Historic corporate officer'
    }
  };

  const status = root.querySelector('[data-spr-status]');
  const grid = root.querySelector('[data-spr-grid]');
  const search = root.querySelector('[data-spr-search]');
  const filters = [...root.querySelectorAll('[data-spr-filter]')];
  const entityGrid = root.querySelector('[data-spr-entities]');
  const reviewTable = root.querySelector('[data-spr-review-body]');
  let data = null;
  let records = [];
  let active = 'ALL';

  const normalise = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
  const categoryClass = category => {
    if (category === 'CURRENT_SPANISH_COUNSEL') return 'current';
    if (category === 'FORMER_SPANISH_COUNSEL' || category === 'PROCURADOR' || category === 'OTHER_LAWYER_IN_MATTER') return 'former';
    if (category.includes('REVIEW')) return 'review';
    if (category.includes('OWNER') || category === 'COMMUNITY_ORGAN_ACTOR') return 'owner';
    if (category.includes('CORPORATE')) return 'corporate';
    return 'adviser';
  };
  const textIndex = record => normalise([record.id,record.public_name,record.category,record.period,record.role_es,record.role_en,record.boundary_es,record.boundary_en,record.classification,record.evidence_status].join(' '));

  function renderStats() {
    const count = category => records.filter(r => r.category === category).length;
    const values = {
      TOTAL: records.length,
      CURRENT: count('CURRENT_SPANISH_COUNSEL'),
      FORMER: count('FORMER_SPANISH_COUNSEL'),
      LEGAL_OTHER: records.filter(r => ['PROCURADOR','OTHER_LAWYER_IN_MATTER','REPRESENTATIVE_IN_MATTER','SPANISH_LEGAL_CONTACT_SCOPE_REVIEW'].includes(r.category)).length,
      ADVISERS: records.filter(r => ['OTHER_PROFESSIONAL_ADVISER','HOTEL_RECOVERY_PROFESSIONAL'].includes(r.category)).length,
      OWNERS: records.filter(r => ['COMMUNITY_ORGAN_ACTOR','HISTORICAL_OWNER_COMMUNITY_PARTICIPANT'].includes(r.category)).length
    };
    root.querySelectorAll('[data-spr-stat]').forEach(node => node.textContent = values[node.dataset.sprStat] ?? 0);
  }

  function renderRecords() {
    const query = normalise(search?.value || '');
    const shown = records.filter(record => (active === 'ALL' || record.category === active) && (!query || record._search.includes(query)));
    grid.replaceChildren();
    if (!shown.length) {
      const empty = document.createElement('p'); empty.className = 'spr-empty'; empty.textContent = copy.noResults; grid.appendChild(empty);
    } else {
      shown.forEach(record => {
        const card = document.createElement('article'); card.className = 'spr-card'; card.id = record.id;
        const header = document.createElement('header');
        const code = document.createElement('code'); code.textContent = record.id;
        const badge = document.createElement('span'); badge.className = `spr-badge ${categoryClass(record.category)}`; badge.textContent = copy.categories[record.category] || record.category;
        header.append(code,badge);
        const h = document.createElement('h3'); h.textContent = record.public_name;
        const meta = document.createElement('p'); meta.className = 'spr-meta';
        const parts = [];
        if (record.period) parts.push(`${copy.period}: ${record.period}`);
        if (record.firm_id) parts.push(`${copy.firm}: ${record.firm_id}`);
        meta.textContent = parts.join(' · ');
        const role = document.createElement('p'); role.className = 'spr-role'; role.textContent = record[`role_${lang}`] || record.role_en || '';
        const limit = document.createElement('p'); limit.className = 'spr-limit'; limit.innerHTML = `<strong>${copy.limit}:</strong> `;
        limit.append(document.createTextNode(record[`boundary_${lang}`] || record.boundary_en || ''));
        card.append(header,h,meta,role,limit); grid.appendChild(card);
      });
    }
    status.textContent = copy.showing(shown.length,records.length);
  }

  function renderEntities() {
    if (!entityGrid) return;
    entityGrid.replaceChildren();
    (data.hotel_operator_entities || []).forEach(entity => {
      const card = document.createElement('article'); card.className = 'spr-entity';
      const code = document.createElement('code'); code.textContent = entity.id;
      const name = document.createElement('strong'); name.textContent = entity.label;
      const p = document.createElement('p'); p.textContent = entity[`capacity_${lang}`] || entity.capacity_en;
      card.append(code,name,p); entityGrid.appendChild(card);
    });
  }

  function renderReviews() {
    if (!reviewTable) return;
    reviewTable.replaceChildren();
    (data.consulted_or_proposal_only_not_former_counsel || []).forEach(item => {
      const tr = document.createElement('tr');
      const name = document.createElement('td'); name.textContent = item.label;
      const state = document.createElement('td'); state.textContent = item.status;
      const boundary = document.createElement('td'); boundary.textContent = item[`boundary_${lang}`] || item.boundary_en;
      tr.append(name,state,boundary); reviewTable.appendChild(tr);
    });
  }

  filters.forEach(button => button.addEventListener('click', () => {
    active = button.dataset.sprFilter;
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    renderRecords();
  }));
  search?.addEventListener('input',renderRecords);

  async function load() {
    status.textContent = copy.loading;
    try {
      const response = await fetch(new URL(root.dataset.registerUrl,document.baseURI),{cache:'no-store'});
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      data = await response.json();
      records = (data.records || []).map(record => ({...record,_search:textIndex(record)}));
      renderStats(); renderRecords(); renderEntities(); renderReviews();
    } catch (error) {
      console.error('Spanish professional register load failed',error);
      status.textContent = copy.failure;
      status.classList.add('spr-warning');
      grid.replaceChildren();
    }
  }
  load();
})();